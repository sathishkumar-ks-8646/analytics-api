#!/usr/bin/env python3
"""
OKF v0.2 conformance and hygiene checks for a bundle directory.

Checks that every non-reserved markdown file has parseable frontmatter with a non-empty `type`,
that reserved files (index.md, log.md) follow their structure, that no `resource` points outside
the bundle, and that every internal link and anchor resolves.

Usage:
    python3 validate.py [bundle-directory]

With no argument it looks for the bundle next to this script: the highest-numbered ./v<N>
(./v2, ./v3, ...), then ./bundle, ./zoho-analytics-rest-api-v2, or the current directory if
that is itself a bundle root.

Audience: maintainers and contributors. Consumers of the bundle do not need to run this; it exists
so that continuous integration can refuse to publish a bundle that is malformed or has broken links.
"""
import os, re, sys, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Version bundles live in top-level v<N>/ directories and are discovered per base directory,
# so adding v3/ needs no change here. These are the fallbacks tried after them.
LEGACY_BUNDLE_DIRS = ('bundle', 'zoho-analytics-rest-api-v2', '.')


def version_dirs(base):
    """Names of the v<N> bundle directories under base, newest first."""
    names = [os.path.basename(p) for p in glob.glob(os.path.join(base, 'v[0-9]*'))
             if os.path.isdir(p)]
    return sorted(names, key=lambda n: int(re.match(r'v(\d+)', n).group(1)), reverse=True)


def is_bundle(d):
    """A bundle root is a directory whose index.md declares okf_version."""
    idx = os.path.join(d, 'index.md')
    return os.path.isfile(idx) and 'okf_version' in open(idx, encoding='utf-8').read(400)


def find_bundle():
    if len(sys.argv) > 1:
        d = os.path.abspath(sys.argv[1])
        if not os.path.isdir(d):
            sys.exit(f'not a directory: {sys.argv[1]}')
        if not is_bundle(d):
            sys.exit(f'not an OKF bundle root (no index.md declaring okf_version): {sys.argv[1]}')
        return d
    for base in (os.getcwd(), ROOT):
        for name in version_dirs(base) + list(LEGACY_BUNDLE_DIRS):
            d = os.path.abspath(os.path.join(base, name))
            if os.path.isdir(d) and is_bundle(d):
                return d
    sys.exit('no OKF bundle found. Pass the bundle directory as an argument, '
             'for example: python3 ' + os.path.basename(__file__) + ' v2')


OUT = find_bundle()
RESERVED = ('index.md', 'log.md')
# OKF v0.2 §7: an actor is `<producer>/<version>`, `human:<id>` or `process:<id>`.
ACTOR_RE = re.compile(r'^(?:human:[\w.-]+|process:[\w.-]+|[\w.-]+/[\w.-]+)$')

def parse_frontmatter(text):
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not m: return None, text
    return m.group(1), text[m.end():]

def headings(text):
    out, fence = [], False
    for line in text.split('\n'):
        if line.startswith('```'): fence = not fence
        if not fence:
            mm = re.match(r'^#{1,6} (.+)$', line)
            if mm: out.append(mm.group(1))
    return out

def slugify(s):
    s = re.sub(r'`', '', s).strip().lower()
    s = re.sub(r'[^a-z0-9 _-]', '', s)
    return s.replace(' ', '-')

try:
    import yaml
except ImportError:
    yaml = None

def frontmatter_error(fm):
    """Why this frontmatter block fails to parse, or None. Renderers that parse frontmatter
    (GitHub included) show a parse error in place of the whole document, so this is fatal."""
    if yaml is not None:
        try:
            yaml.safe_load(fm)
        except Exception as e:
            return str(e).replace('\n', ' ')[:160]
        return None
    # Without PyYAML, check the plain-scalar shapes a hand-written document can introduce:
    # ': ' or a trailing ':' reads as a nested mapping key, ' #' truncates the value at a comment.
    for line in fm.split('\n'):
        m = re.match(r'^\s*(?:- )?[A-Za-z_][\w.-]*: (\S.*)$', line)
        if not m or m.group(1)[0] in '"\'[{|>&*':
            continue
        v = m.group(1).rstrip()
        if ': ' in v or v.endswith(':'):
            return f'unquoted scalar reads as a nested mapping; quote it: {line.strip()[:100]}'
        if ' #' in v:
            return f'unquoted scalar is truncated at a comment; quote it: {line.strip()[:100]}'
    return None

errors, warnings = [], []
docs = {}
for dirpath, dirnames, filenames in os.walk(OUT):
    rel_dir = os.path.relpath(dirpath, OUT)
    if 'index.md' not in filenames:
        warnings.append(f'missing index.md in {rel_dir}')
    for f in filenames:
        p = os.path.join(dirpath, f)
        relp = '/' + os.path.relpath(p, OUT).replace(os.sep, '/')
        if not f.endswith('.md'):
            docs[relp] = None; continue
        text = open(p, encoding='utf-8').read()
        fm, body = parse_frontmatter(text)
        docs[relp] = (fm, body, text)
        if f in RESERVED:
            if f == 'index.md' and fm is not None and rel_dir != '.':
                errors.append(f'{relp}: index.md must not carry frontmatter except at bundle root')
            if fm is None and not re.search(r'(?m)^# ', body):
                warnings.append(f'{relp}: reserved file has no section heading')
            continue
        if fm is None:
            errors.append(f'{relp}: missing YAML frontmatter'); continue
        fm_err = frontmatter_error(fm)
        if fm_err:
            errors.append(f'{relp}: frontmatter is not valid YAML: {fm_err}')
        if not re.search(r'(?m)^type: \S', fm):
            errors.append(f'{relp}: frontmatter has no non-empty type')
        for key in ('title', 'description'):
            if not re.search(rf'(?m)^{key}: \S', fm):
                warnings.append(f'{relp}: frontmatter missing {key}')
        if '{{' in fm: errors.append(f'{relp}: unexpanded template placeholder in frontmatter')
        # An endpoint whose authorization requirement is blank is worse than one with no
        # document: the permission matrix renders it as "-" and a reader concludes the call
        # needs nothing. The group overview's Permission Model table is the source to fill it from.
        if re.search(r'(?m)^type: API Endpoint\s*$', fm):
            pr = re.search(r'(?m)^\s+permission_required:[ \t]*"?(.*?)"?[ \t]*$', fm)
            if not pr or not pr.group(1).strip():
                errors.append(f'{relp}: API Endpoint has empty api.permission_required')
        if re.search(r'(?m)^\|\s*Permission required\s*\|\s*See group overview', body):
            errors.append(f'{relp}: "Permission required" row is an unresolved placeholder')
        # OKF v0.2 SS5.2: `by` is REQUIRED inside `generated`, and SS7 fixes the actor spelling.
        # Trust tiers (SS5.3) are derived from the actor prefix, so an actorless `generated`
        # block leaves a consumer unable to tell a machine build from a hand-authored document.
        gen = re.search(r'(?m)^generated:\n((?:[ \t]+.*\n?)*)', fm)
        if gen:
            by = re.search(r'(?m)^\s+by:[ \t]*"?([^"\n]*?)"?\s*$', gen.group(1))
            if not by or not by.group(1):
                errors.append(f'{relp}: generated.by is required (OKF v0.2 §5.2)')
            elif not ACTOR_RE.match(by.group(1)):
                errors.append(f'{relp}: generated.by is not an OKF §7 actor '
                              f'(<producer>/<version>, human:<id> or process:<id>): {by.group(1)}')
        for by in re.findall(r'(?m)^\s+-?\s*by:[ \t]*"?([^"\n]*?)"?\s*$', fm):
            if by and not ACTOR_RE.match(by):
                warnings.append(f'{relp}: actor is not an OKF §7 form: {by}')
        for res in re.findall(r'(?m)^\s+resource: "?([^"\n]+?)"?\s*$', fm) + re.findall(r'(?m)^resource: "?([^"\n]+?)"?\s*$', fm):
            if res.startswith(('http://', 'https://')): continue
            if res.startswith('/') and os.path.exists(os.path.join(OUT, res.lstrip('/'))): continue
            errors.append(f'{relp}: resource outside the bundle or missing: {res}')

# The permission matrix is generated from every endpoint's api.permission_required. A "-"
# in the last column means a row lost its source value, which reads as "no permission needed".
mx = docs.get('/foundations/permission-matrix.md')
if mx:
    for i, line in enumerate(mx[2].split('\n'), 1):
        if line.startswith('| [') and re.search(r'\|\s*-\s*\|\s*$', line):
            errors.append(f'/foundations/permission-matrix.md:{i}: empty permission cell')

# link check
anchors = {}
for relp, v in docs.items():
    if v: anchors[relp] = {slugify(h) for h in headings(v[1])}
broken = []
for relp, v in docs.items():
    if not v: continue
    fence = False
    for line in v[2].split('\n'):
        if line.startswith('```'): fence = not fence
        if fence: continue
        for label, target in re.findall(r'\[([^\]]*)\]\(([^)\s]+)\)', line):
            if target.startswith(('http://', 'https://', 'mailto:')): continue
            path, _, anchor = target.partition('#')
            if path == '':
                if anchor and anchor not in anchors.get(relp, set()) and not re.match(r'^error-\d+$', anchor):
                    broken.append((relp, target, 'anchor'))
                continue
            if path.startswith('/'):
                # A leading slash resolves against the *site* root in every markdown renderer,
                # not the bundle root, so these 404 as soon as the bundle sits in a subdirectory.
                broken.append((relp, target, 'bundle-root-absolute; use a document-relative path'))
                continue
            if path.endswith('/'):
                broken.append((relp, target, 'bare directory; link its index.md'))
                continue
            tgt = os.path.normpath(os.path.join(os.path.dirname(relp), path)).replace(os.sep, '/')
            if not tgt.startswith('/'): tgt = '/' + tgt
            if tgt.endswith('/'): tgt += 'index.md'
            if tgt not in docs:
                if os.path.isdir(os.path.join(OUT, tgt.lstrip('/'))): continue
                broken.append((relp, target, 'file'))
            elif anchor and docs[tgt] and anchor not in anchors.get(tgt, set()):
                broken.append((relp, target, 'anchor'))

concepts = sum(1 for p, v in docs.items() if v and os.path.basename(p) not in RESERVED)
print(f'bundle={os.path.relpath(OUT, os.getcwd())} files={len(docs)} concepts={concepts} errors={len(errors)} warnings={len(warnings)} broken_links={len(broken)}')
for e in errors: print('ERROR', e)
for w in warnings[:40]: print('WARN ', w)
import collections
bt = collections.Counter((b[2]) for b in broken); print('broken by kind:', dict(bt))
for b in broken[:60]: print('LINK ', b)
sys.exit(1 if errors or broken else 0)
