"""Extract a normalised API model from each Zoho Analytics SDK source tree.

Every SDK carries structured doc comments in its own dialect (Javadoc, XML doc,
epydoc, godoc, phpDoc, JSDoc, YARD). This module parses all seven into one shape
so the documentation generator can treat them identically:

    Api(language, classes=[ApiClass(name, summary, methods=[ApiMethod(...)])])

The parsers are deliberately line-oriented rather than AST-based: the sources are
single large files per language with a consistent house style, and a real parser
for seven languages would be far more machinery than the job needs.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import paths  # noqa: E402

# The five API surfaces every SDK exposes, in the order they should be documented.
# Keys are the canonical names; values are the per-language type names.
SURFACES = ["AnalyticsClient", "OrgAPI", "WorkspaceAPI", "ViewAPI", "BulkAPI"]

SURFACE_SUMMARY = {
    "AnalyticsClient": (
        "The entry point. Holds the OAuth credentials, manages the access token "
        "lifecycle, carries transport configuration (timeouts, proxy, custom "
        "headers) and hands out the four scoped instances below."
    ),
    "OrgAPI": (
        "Organization-scoped calls: users, roles, admins, subscription and "
        "resource usage, organization-wide workspace listings and "
        "organization-wide security controls."
    ),
    "WorkspaceAPI": (
        "Workspace-scoped calls: views, folders, tags, query tables, variables, "
        "slideshows, email schedules, data alerts, backups, linked workspaces, "
        "sharing, workspace membership and workspace security controls."
    ),
    "ViewAPI": (
        "View-scoped calls: rows, columns, formulas, lookups, publishing, "
        "private links, tags, alerts and per-view metadata."
    ),
    "BulkAPI": (
        "Data movement: synchronous import and export, batched import for large "
        "files, and asynchronous (job-based) import and export."
    ),
}


@dataclass
class Param:
    name: str
    type: str = ""
    desc: str = ""


@dataclass
class ApiMethod:
    name: str
    signature: str
    summary: str = ""
    params: list[Param] = field(default_factory=list)
    returns: str = ""
    return_type: str = ""
    throws: list[Param] = field(default_factory=list)
    note: str = ""
    internal: bool = False


@dataclass
class ApiClass:
    name: str
    summary: str = ""
    methods: list[ApiMethod] = field(default_factory=list)


@dataclass
class Api:
    language: str
    classes: list[ApiClass] = field(default_factory=list)

    def surface(self, name: str) -> ApiClass | None:
        for c in self.classes:
            if c.name == name:
                return c
        return None


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _clean(text: str) -> str:
    """Collapse whitespace and strip doc-comment markup noise."""
    text = re.sub(r"<code>(.*?)</code>", r"`\1`", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("C{None}", "`null`")
    return re.sub(r"\s+", " ", text).strip()


# Transport and token-store plumbing. These are public by language convention
# (Python has no leading underscore, Ruby declares no `private`) but they are not
# API surface: they are what the documented methods call underneath.
_INTERNAL_NAMES = {
    "sendapirequest", "sendimportapirequest", "sendexportapirequest",
    "sendbatchimportapirequest", "submitrequest", "submitimportrequest",
    "submitexportrequest", "getrequestobj", "initpoolmanager",
    "handlev2request", "handleimportrequest", "handleexportrequest",
    "handlebatchimportrequest", "handleimportresponseerrors",
    "handleresponseerrors", "extracterrorfromresponse", "createhttpclient",
    "createrequest", "addheaders", "isoauthexpired", "ensureaccesstoken",
    "regenerateaccesstoken", "regenerateanalyticsoauthtoken",
    "regenerateoauthtoken", "setupfrombuilder", "tokenfilepath",
    "derivefilekey", "derivetokenkey", "encrypttoken", "decrypttoken",
    "encryptandwritefile", "decryptandreadfile", "keyforrefreshtoken",
    "savetokentostore", "loadtokenfromstore", "cleanupobsoletetokenfiles",
    "getjsonresponse", "close", "importdatainbatches", "self",
}


def _is_internal(summary: str, name: str) -> bool:
    if name.startswith("_"):
        return True
    if name.replace("_", "").lower() in _INTERNAL_NAMES:
        return True
    low = summary.lower()
    return "internal" in low or "internally used" in low


def _fold_signatures(lines: list[str], opener: str) -> list[str]:
    """Join a declaration whose parameter list wraps onto following lines.

    Every parser below matches `name(args)` on a single physical line. Several
    SDK sources wrap long parameter lists, which silently hid those methods
    from the generated reference. Folding keeps the list the same length -
    consumed continuation lines become empty - so the line indexes the callers
    compute (class_at, docstring lookups) stay valid.
    """
    rx = re.compile(opener)
    out = list(lines)
    for i, line in enumerate(out):
        if not rx.match(line) or line.count("(") <= line.count(")"):
            continue
        joined = line.rstrip()
        depth = joined.count("(") - joined.count(")")
        j = i + 1
        while j < len(out) and depth > 0:
            nxt = out[j].strip()
            joined += " " + nxt
            depth += nxt.count("(") - nxt.count(")")
            out[j] = ""
            j += 1
        out[i] = joined
    return out


class _Scanner:
    """Walks a source file, tracking which class each line belongs to."""

    def __init__(self, path: Path, class_re: str, sig_opener: str = ""):
        self.lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        if sig_opener:
            self.lines = _fold_signatures(self.lines, sig_opener)
        self.bounds: list[tuple[int, str]] = []
        rx = re.compile(class_re)
        for i, line in enumerate(self.lines):
            m = rx.match(line)
            if m:
                self.bounds.append((i, m.group(1)))

    def class_at(self, idx: int) -> str:
        name = ""
        for start, cname in self.bounds:
            if start <= idx:
                name = cname
            else:
                break
        return name


def _collect(api: Api, buckets: dict[str, list[ApiMethod]]) -> None:
    for surface in SURFACES:
        methods = buckets.get(surface, [])
        if not methods:
            continue
        seen: set[str] = set()
        unique: list[ApiMethod] = []
        for m in methods:
            if m.internal:
                continue
            # Overloads collapse to one entry; keep the richest-documented one.
            if m.name in seen:
                prev = next(u for u in unique if u.name == m.name)
                if len(m.summary) > len(prev.summary):
                    unique[unique.index(prev)] = m
                continue
            seen.add(m.name)
            unique.append(m)
        unique.sort(key=lambda m: m.name.lower())
        api.classes.append(
            ApiClass(surface, SURFACE_SUMMARY[surface], unique)
        )


# --------------------------------------------------------------------------
# Java  -- Javadoc
# --------------------------------------------------------------------------

def parse_java() -> Api:
    api = Api("java")
    buckets: dict[str, list[ApiMethod]] = {}
    src = paths.sdk_root() / "java/source/com/zoho/analytics/client"
    files = {
        "AnalyticsClient": "AnalyticsClient.java",
        "OrgAPI": "OrgAPI.java",
        "WorkspaceAPI": "WorkspaceAPI.java",
        "ViewAPI": "ViewAPI.java",
        "BulkAPI": "BulkAPI.java",
    }
    sig_re = re.compile(
        r"^\s*public\s+(?!class)(?:static\s+)?([\w<>\[\],.\s]+?)\s+(\w+)\s*\(([^)]*)\)"
    )
    for surface, fname in files.items():
        path = src / fname
        if not path.exists():
            continue
        lines = _fold_signatures(
            path.read_text(encoding="utf-8").splitlines(), r"^\s*public\s"
        )
        out: list[ApiMethod] = []
        doc: list[str] = []
        in_doc = False
        for raw in lines:
            s = raw.strip()
            if s.startswith("/**"):
                in_doc, doc = True, []
                continue
            if in_doc:
                if s.startswith("*/"):
                    in_doc = False
                else:
                    doc.append(re.sub(r"^\*\s?", "", s))
                continue
            m = sig_re.match(raw)
            if not m:
                if s and not s.startswith(("//", "@", "}", "{")):
                    doc = []
                continue
            rtype, name, args = m.group(1).strip(), m.group(2), m.group(3)
            if name == files[surface].split(".")[0]:
                doc = []
                continue
            out.append(_from_javadoc(name, rtype, args, doc))
            doc = []
        buckets[surface] = out
    _collect(api, buckets)
    return api


def _from_javadoc(name: str, rtype: str, args: str, doc: list[str]) -> ApiMethod:
    summary_lines, params, throws, ret = [], [], [], ""
    for line in doc:
        pm = re.match(r"@param\s+(\w+)\s*(.*)", line)
        tm = re.match(r"@throws\s+(\w+)\s*(.*)", line)
        rm = re.match(r"@return\s*(.*)", line)
        if pm:
            params.append(Param(pm.group(1), desc=_clean(pm.group(2))))
        elif tm:
            throws.append(Param(tm.group(1), desc=_clean(tm.group(2))))
        elif rm:
            ret = _clean(rm.group(1))
        elif line.startswith("@"):
            continue
        elif params or throws or ret:
            if params:
                params[-1].desc = _clean(params[-1].desc + " " + line)
        else:
            summary_lines.append(line)
    summary = _clean(" ".join(summary_lines))
    sig = f"{rtype} {name}({_clean(args)})"
    return ApiMethod(
        name=name, signature=sig, summary=summary, params=params,
        returns=ret, return_type=rtype, throws=throws,
        internal=_is_internal(summary, name),
    )


# --------------------------------------------------------------------------
# C#  -- XML doc comments
# --------------------------------------------------------------------------

def parse_csharp() -> Api:
    api = Api("csharp")
    buckets: dict[str, list[ApiMethod]] = {}
    sc = _Scanner(
        paths.sdk_root() / "csharp/source/AnalyticsClient.cs",
        r"^\s*(?:public|internal)\s+(?:sealed\s+)?class\s+(\w+)",
        r"^\s*public\s",
    )
    sig_re = re.compile(
        r"^\s*public\s+(?!class)(?:static\s+)?(?:virtual\s+)?"
        r"([\w<>\[\],.\s?]+?)\s+(\w+)\s*\(([^)]*)\)"
    )
    doc: list[str] = []
    for i, raw in enumerate(sc.lines):
        s = raw.strip()
        if s.startswith("///"):
            doc.append(re.sub(r"^///\s?", "", s))
            continue
        m = sig_re.match(raw)
        if not m:
            if s and not s.startswith(("//", "[", "{", "}")):
                doc = []
            continue
        rtype, name, args = m.group(1).strip(), m.group(2), m.group(3)
        cls = sc.class_at(i)
        if cls not in SURFACES or name == cls:
            doc = []
            continue
        blob = "\n".join(doc)
        summary = _clean(_tag(blob, "summary"))
        ret = _clean(_tag(blob, "returns"))
        params = [
            Param(pn, desc=_clean(pd))
            for pn, pd in re.findall(r'<param name="(\w+)">(.*?)</param>', blob, re.S)
        ]
        buckets.setdefault(cls, []).append(
            ApiMethod(
                name=name, signature=f"{rtype} {name}({_clean(args)})",
                summary=summary, params=params, returns=ret, return_type=rtype,
                internal=_is_internal(summary, name),
            )
        )
        doc = []
    _collect(api, buckets)
    return api


def _tag(blob: str, tag: str) -> str:
    m = re.search(rf"<{tag}>(.*?)</{tag}>", blob, re.S)
    return m.group(1) if m else ""


# --------------------------------------------------------------------------
# Python  -- epydoc field lists
# --------------------------------------------------------------------------

def parse_python() -> Api:
    api = Api("python")
    buckets: dict[str, list[ApiMethod]] = {}
    sc = _Scanner(paths.sdk_root() / "python/source/AnalyticsClient.py", r"^\s*class\s+(\w+)",
                   r"^\s*def\s")
    sig_re = re.compile(r"^(\s*)def\s+(\w+)\s*\(self,?\s*([^)]*)\)\s*:")
    i = 0
    while i < len(sc.lines):
        m = sig_re.match(sc.lines[i])
        if not m:
            i += 1
            continue
        name, args = m.group(2), m.group(3)
        cls = sc.class_at(i)
        if cls not in SURFACES or name.startswith("_"):
            i += 1
            continue
        doc, j = _py_docstring(sc.lines, i + 1)
        summary, params, ret, rtype, throws = _from_epydoc(doc)
        buckets.setdefault(cls, []).append(
            ApiMethod(
                name=name, signature=f"{name}({_clean(args)})", summary=summary,
                params=params, returns=ret, return_type=rtype, throws=throws,
                internal=_is_internal(summary, name),
            )
        )
        i = j
    _collect(api, buckets)
    return api


def _py_docstring(lines: list[str], start: int) -> tuple[list[str], int]:
    i = start
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines) or not lines[i].strip().startswith(('"""', "'''")):
        return [], start
    quote = lines[i].strip()[:3]
    body = [lines[i].strip()[3:]]
    if body[0].endswith(quote):
        return [body[0][: -3].strip()], i + 1
    i += 1
    while i < len(lines) and quote not in lines[i]:
        body.append(lines[i].strip())
        i += 1
    return [b for b in body if b is not None], i + 1


def _from_epydoc(doc: list[str]) -> tuple[str, list[Param], str, str, list[Param]]:
    summary, params, throws = [], {}, []
    ret, rtype = "", ""
    order: list[str] = []
    for line in doc:
        pm = re.match(r"@param\s+(\w+)\s*:\s*(.*)", line)
        tm = re.match(r"@type\s+(\w+)\s*:\s*(.*)", line)
        rm = re.match(r"@return\s*:?\s*(.*)", line)
        rt = re.match(r"@rtype\s*:\s*(.*)", line)
        em = re.match(r"@raise\s+(\w+)\s*:\s*(.*)", line)
        if pm:
            key = pm.group(1)
            if key not in params:
                params[key] = Param(key)
                order.append(key)
            params[key].desc = _clean(pm.group(2))
        elif tm:
            key = tm.group(1)
            if key not in params:
                params[key] = Param(key)
                order.append(key)
            params[key].type = _clean(tm.group(2))
        elif rm:
            ret = _clean(rm.group(1))
        elif rt:
            rtype = _clean(rt.group(1))
        elif em:
            throws.append(Param(em.group(1), desc=_clean(em.group(2))))
        elif line.startswith("@"):
            continue
        elif not params and not ret:
            summary.append(line)
    return _clean(" ".join(summary)), [params[k] for k in order], ret, rtype, throws


# --------------------------------------------------------------------------
# Go  -- block comments above the receiver function
# --------------------------------------------------------------------------

def parse_go() -> Api:
    api = Api("go")
    buckets: dict[str, list[ApiMethod]] = {}
    path = paths.sdk_root() / "go/source/zoho/pkg/analyticsclient/analyticsclient.go"
    lines = _fold_signatures(
        path.read_text(encoding="utf-8").splitlines(), r"^\s*func\s"
    )
    sig_re = re.compile(
        r"^\s*func\s+\((\w+)\s+\*?(\w+)\)\s+([A-Z]\w*)\s*\(([^)]*)\)\s*(.*)$"
    )
    doc: list[str] = []
    in_doc = False
    for raw in lines:
        s = raw.strip()
        if s.startswith("/*"):
            in_doc, doc = True, []
            continue
        if in_doc:
            if s.startswith("*/"):
                in_doc = False
            else:
                doc.append(s)
            continue
        m = sig_re.match(raw)
        if not m:
            if s and not s.startswith("//"):
                doc = []
            continue
        recv_type, name, args, tail = m.group(2), m.group(3), m.group(4), m.group(5)
        cls = "AnalyticsClient" if recv_type == "Client" else recv_type
        if cls not in SURFACES:
            doc = []
            continue
        rtype = _clean(tail.rstrip("{").strip())
        arg_names = [
            a.strip().split()[0]
            for a in args.split(",")
            if a.strip() and a.strip().split()
        ]
        summary, params, ret = _from_godoc(name, doc, arg_names, rtype)
        buckets.setdefault(cls, []).append(
            ApiMethod(
                name=name, signature=f"{name}({_clean(args)}) {rtype}",
                summary=summary, params=params, returns=ret, return_type=rtype,
                internal=_is_internal(summary, name),
            )
        )
        doc = []
    _collect(api, buckets)
    return api


def _from_godoc(
    name: str, doc: list[str], arg_names: list[str], rtype: str
) -> tuple[str, list[Param], str]:
    """godoc here has no @tags, so params vs returns is decided by the signature.

    Named return values carry the result (minus the always-present
    `serverexception`); anything matching a parameter name is a parameter. The
    comment frequently documents only the parameters, so the return description
    falls back to the declared return names.
    """
    summary, documented = "", {}
    for line in doc:
        if not line:
            continue
        head = re.match(rf"{re.escape(name)}\s*-\s*(.*)", line)
        if head:
            summary = _clean(head.group(1))
            continue
        kv = re.match(r"(\w+)\s+-\s+(.*)", line)
        if kv:
            documented[kv.group(1)] = _clean(kv.group(2))

    params = [
        Param(a, desc=documented.get(a, "")) for a in arg_names if a != "serverexception"
    ]

    # Named return values live inside the trailing parenthesised tuple.
    returns = ""
    tuple_m = re.match(r"\((.*)\)\s*$", rtype)
    if tuple_m:
        named = []
        for part in tuple_m.group(1).split(","):
            bits = part.strip().split()
            if len(bits) >= 2 and bits[0] != "serverexception":
                named.append((bits[0], " ".join(bits[1:])))
        chunks = [
            documented.get(n) or f"`{n}` ({t})" for n, t in named
        ]
        returns = "; ".join(chunks)
    return summary, params, returns


# --------------------------------------------------------------------------
# PHP  -- phpDoc
# --------------------------------------------------------------------------

def parse_php() -> Api:
    api = Api("php")
    buckets: dict[str, list[ApiMethod]] = {}
    sc = _Scanner(paths.sdk_root() / "php/source/AnalyticsClient.php", r"^\s*class\s+(\w+)",
                   r"^\s*(?:public\s+|protected\s+|private\s+)?function\s")
    sig_re = re.compile(r"^\s*(?:public\s+)?function\s+(\w+)\s*\(([^)]*)\)")
    doc: list[str] = []
    in_doc = False
    for i, raw in enumerate(sc.lines):
        s = raw.strip()
        if s.startswith("/**"):
            in_doc, doc = True, []
            continue
        if in_doc:
            if s.startswith("*/"):
                in_doc = False
            else:
                doc.append(re.sub(r"^\*\s?", "", s))
            continue
        m = sig_re.match(raw)
        if not m:
            continue
        name, args = m.group(1), m.group(2)
        cls = sc.class_at(i)
        if cls not in SURFACES or name.startswith("__"):
            doc = []
            continue
        summary, params, ret, throws = _from_phpdoc(doc)
        buckets.setdefault(cls, []).append(
            ApiMethod(
                name=name, signature=f"{name}({_clean(args)})", summary=summary,
                params=params, returns=ret, throws=throws,
                internal=_is_internal(summary, name),
            )
        )
        doc = []
    _collect(api, buckets)
    return api


def _from_phpdoc(doc: list[str]) -> tuple[str, list[Param], str, list[Param]]:
    summary, params, throws, ret = [], [], [], ""
    for line in doc:
        pm = re.match(r"@param\s+(\S+)\s+\$(\w+)\s*(.*)", line)
        tm = re.match(r"@throws\s+(\w+)\s*(.*)", line)
        rm = re.match(r"@return\s+(\S+)\s*(.*)", line)
        if pm:
            params.append(Param(pm.group(2), _clean(pm.group(1)), _clean(pm.group(3))))
        elif tm:
            throws.append(Param(tm.group(1), desc=_clean(tm.group(2))))
        elif rm:
            ret = _clean(rm.group(2)) or _clean(rm.group(1))
        elif line.startswith("@"):
            continue
        elif not params and not ret:
            summary.append(line)
    return _clean(" ".join(summary)), params, ret, throws


# --------------------------------------------------------------------------
# Node.js  -- JSDoc
# --------------------------------------------------------------------------

def parse_node() -> Api:
    api = Api("nodejs")
    buckets: dict[str, list[ApiMethod]] = {}
    sc = _Scanner(paths.sdk_root() / "nodejs/source/AnalyticsClient.js", r"^\s*class\s+(\w+)",
                   r"^\s{4}(?:async\s+)?\w+\s*\(")
    # Most methods put the opening brace on the same line, a few on the next.
    sig_re = re.compile(r"^\s{4}(?:async\s+)?(\w+)\s*\(([^)]*)\)\s*\{?\s*$")
    doc: list[str] = []
    in_doc = False
    for i, raw in enumerate(sc.lines):
        s = raw.strip()
        if s.startswith("/**"):
            in_doc, doc = True, []
            continue
        if in_doc:
            if s.startswith("*/"):
                in_doc = False
            else:
                doc.append(re.sub(r"^\*\s?", "", s))
            continue
        m = sig_re.match(raw)
        if not m:
            continue
        name, args = m.group(1), m.group(2)
        cls = sc.class_at(i)
        if cls not in SURFACES or name in {"constructor", "if", "for", "while", "catch", "switch"}:
            doc = []
            continue
        summary, params, ret, throws = _from_jsdoc(doc)
        buckets.setdefault(cls, []).append(
            ApiMethod(
                name=name, signature=f"{name}({_clean(args)})", summary=summary,
                params=params, returns=ret, throws=throws,
                internal=_is_internal(summary, name),
            )
        )
        doc = []
    _collect(api, buckets)
    return api


def _from_jsdoc(doc: list[str]) -> tuple[str, list[Param], str, list[Param]]:
    summary, params, throws, ret = [], [], [], ""
    for line in doc:
        pm = re.match(r"@param\s+\{([^}]*)\}\s+([\w.]+)(?:\s*=\s*\S+?)?\s*-?\s*(.*)", line)
        rm = re.match(r"@returns?\s+\{([^}]*)\}\s*(.*)", line)
        tm = re.match(r"@throws\s+\{([^}]*)\}\s*(.*)", line)
        if pm:
            params.append(
                Param(pm.group(2), _clean(pm.group(1)), _clean(pm.group(3)).lstrip("{} -"))
            )
        elif rm:
            ret = _clean(rm.group(2)) or _clean(rm.group(1))
        elif tm:
            throws.append(Param(tm.group(1), desc=_clean(tm.group(2))))
        elif line.startswith("@"):
            continue
        elif not params and not ret:
            summary.append(line)
    return _clean(" ".join(summary)), params, ret, throws


# --------------------------------------------------------------------------
# Ruby  -- YARD
# --------------------------------------------------------------------------

def parse_ruby() -> Api:
    api = Api("ruby")
    buckets: dict[str, list[ApiMethod]] = {}
    path = paths.sdk_root() / "ruby/source/lib/zoho_analytics_client.rb"
    lines = path.read_text(encoding="utf-8").splitlines()
    # Ruby nests `class Builder` inside `AnalyticsClient`, so class membership has
    # to follow indentation rather than "most recent class declaration wins".
    # Builder is the client's construction API, so it is folded into AnalyticsClient.
    stack: list[tuple[int, str]] = []
    owner: list[str] = []
    cls_re = re.compile(r"^(\s*)(?:class|module)\s+(\w+)")
    end_re = re.compile(r"^(\s*)end\b")
    for raw in lines:
        cm = cls_re.match(raw)
        if cm:
            stack.append((len(cm.group(1)), cm.group(2)))
            owner.append(stack[-1][1])
            continue
        em = end_re.match(raw)
        if em and stack and len(em.group(1)) == stack[-1][0]:
            stack.pop()
        # WorkspaceAPI and ViewAPI are nested inside OrgAPI, which is itself
        # nested inside AnalyticsClient, so the *innermost* surface owns the method.
        inner = next((n for _, n in reversed(stack) if n in SURFACES), "")
        owner.append(inner or (stack[-1][1] if stack else ""))

    sig_re = re.compile(r"^\s*def\s+(?:self\.)?(\w+[?!]?)\s*(?:\(([^)]*)\))?")
    doc: list[str] = []
    for i, raw in enumerate(lines):
        s = raw.strip()
        if s.startswith("#"):
            doc.append(re.sub(r"^#\s?", "", s))
            continue
        m = sig_re.match(raw)
        if not m:
            if s:
                doc = []
            continue
        name, args = m.group(1), m.group(2) or ""
        cls = owner[i] if i < len(owner) else ""
        if cls not in SURFACES or name in {"initialize", "build"}:
            doc = []
            continue
        summary, params, ret, rtype = _from_yard(doc)
        buckets.setdefault(cls, []).append(
            ApiMethod(
                name=name, signature=f"{name}({_clean(args)})", summary=summary,
                params=params, returns=ret, return_type=rtype,
                internal=_is_internal(summary, name),
            )
        )
        doc = []
    _collect(api, buckets)
    return api


def _from_yard(doc: list[str]) -> tuple[str, list[Param], str, str]:
    summary, params, ret, rtype = [], [], "", ""
    for line in doc:
        pm = re.match(r"@param\s+(\w+)\s*\[([^\]]*)\]\s*(.*)", line)
        rm = re.match(r"@return\s*\[([^\]]*)\]\s*(.*)", line)
        if pm:
            params.append(Param(pm.group(1), _clean(pm.group(2)), _clean(pm.group(3))))
        elif rm:
            rtype = _clean(rm.group(1))
            ret = _clean(rm.group(2)) or rtype
        elif line.startswith("@"):
            continue
        elif not params and not ret:
            summary.append(line)
    return _clean(" ".join(summary)), params, ret, rtype


PARSERS = {
    "java": parse_java,
    "csharp": parse_csharp,
    "python": parse_python,
    "go": parse_go,
    "php": parse_php,
    "nodejs": parse_node,
    "ruby": parse_ruby,
}


def load(language: str) -> Api:
    return PARSERS[language]()


if __name__ == "__main__":
    for lang in PARSERS:
        api = load(lang)
        total = sum(len(c.methods) for c in api.classes)
        documented = sum(
            1 for c in api.classes for m in c.methods if m.summary
        )
        per = ", ".join(f"{c.name}:{len(c.methods)}" for c in api.classes)
        print(f"{lang:<8} {total:>4} methods ({documented} documented)  {per}")
