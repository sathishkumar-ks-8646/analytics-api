#!/usr/bin/env python3
"""Generate the SDK documentation for every language.

Writes, into each `<lang>/docs/`:

  * markdown sources (`*.md`) -- the authored form, readable on their own
  * rendered HTML siblings (`*.html`) -- the published form, openable straight
    from the filesystem with no server or tooling
  * `assets/docs.css`, `assets/docs.js`

Markdown links point at `.md`; the renderer rewrites them to `.html` so both
trees navigate correctly. Run from anywhere:

    python3 tools/sdkdocs/build.py            # all languages
    python3 tools/sdkdocs/build.py --lang go  # one language
    python3 tools/sdkdocs/build.py --check    # validate without writing
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import content  # noqa: E402
import extract  # noqa: E402
import md as mdlib  # noqa: E402
import theme  # noqa: E402
from langs import LANGS, ORDER, Lang  # noqa: E402

V2 = Path(__file__).resolve().parents[2]
BUILT = date.today().isoformat()

REFERENCE = [
    ("analytics-client", "AnalyticsClient"),
    ("org-api", "OrgAPI"),
    ("workspace-api", "WorkspaceAPI"),
    ("view-api", "ViewAPI"),
    ("bulk-api", "BulkAPI"),
]


@dataclass
class Page:
    path: str          # e.g. "guides/importing-data"
    title: str         # nav + <title>
    kicker: str        # editorial eyebrow
    lede: str
    section: str       # nav grouping
    body: str = ""     # markdown


# ----------------------------------------------------------------------
# reference pages, generated from the parsed SDK sources
# ----------------------------------------------------------------------

def reference_markdown(lang: Lang, api: extract.Api, surface: str) -> str:
    cls = api.surface(surface)
    if cls is None or not cls.methods:
        return f"# {surface}\n\nThis surface is not present in the {lang.name} SDK.\n"

    # The summary is used as the page lede, so it is not repeated here.
    out = [f"# {surface}", ""]

    if surface == "AnalyticsClient":
        out += [
            "```" + lang.fence,
            lang.snippets["construct"],
            "```",
            "",
            "::: danger Construct this once",
            "Creating a client per request exhausts the OAuth token allowance within "
            "ten calls. See [Authentication](../authentication.md#the-access-token-throttle).",
            ":::",
            "",
        ]
    else:
        out += [
            "```" + lang.fence,
            lang.snippets["instances"],
            "```",
            "",
        ]

    out += [
        f"`{surface}` exposes **{len(cls.methods)} methods**. "
        f"Method names are {lang.naming.rstrip('.')} and identifiers are "
        f"{lang.id_type.split('.')[0].lower()}.",
        "",
        "## Methods",
        "",
    ]

    # Compact index so a 100-method page stays navigable.
    links = ", ".join(f"[`{m.name}`](#{mdlib.slugify(m.name)})" for m in cls.methods)
    out += [links, ""]

    for m in cls.methods:
        out.append(f"### {m.name}")
        out.append("")
        out.append("```" + lang.fence)
        out.append(m.signature)
        out.append("```")
        out.append("")
        if m.summary:
            out.append(m.summary)
            out.append("")
        if m.params:
            has_types = any(p.type for p in m.params)
            if has_types:
                out.append("| Parameter | Type | Description |")
                out.append("|---|---|---|")
                for p in m.params:
                    out.append(f"| `{p.name}` | {_code(p.type)} | {p.desc or '—'} |")
            else:
                out.append("| Parameter | Description |")
                out.append("|---|---|")
                for p in m.params:
                    out.append(f"| `{p.name}` | {p.desc or '—'} |")
            out.append("")
        if m.returns:
            rt = f" ({_code(m.return_type)})" if m.return_type and len(m.return_type) < 40 else ""
            out.append(f"**Returns**{rt} — {m.returns}")
            out.append("")
        if m.throws:
            raised = "; ".join(f"`{t.name}`" for t in m.throws)
            out.append(f"**Raises** — {raised}")
            out.append("")

    out += [
        "## Related",
        "",
        "- [Errors](../errors.md) — the failure envelope and codes worth branching on.",
        "- [Limits](../limits.md) — throttles and quotas that apply to these calls.",
    ]
    return "\n".join(out) + "\n"


def _code(text: str) -> str:
    return f"`{text}`" if text else "—"


# ----------------------------------------------------------------------
# page set
# ----------------------------------------------------------------------

def pages_for(lang: Lang, api: extract.Api) -> list[Page]:
    total = sum(len(c.methods) for c in api.classes)
    pages = [
        Page("index", "Introduction", f"Zoho Analytics · {lang.name}",
             f"The {lang.name} client for Zoho Analytics REST API v2 — "
             f"{total} methods across five scoped surfaces.",
             "Overview", content.index(lang)),
        Page("getting-started", "Getting started", "Start here",
             f"Install the SDK, construct a client, and make a first authenticated call.",
             "Overview", content.getting_started(lang)),
        Page("authentication", "Authentication", "Credentials",
             "OAuth tokens, scopes, data centers — and the token throttle that "
             "breaks integrations which construct a client per request.",
             "Essentials", content.authentication(lang)),
        Page("configuration", "Configuration", "Client settings",
             "Timeouts, proxies, regions and per-request configuration.",
             "Essentials", content.configuration(lang)),
        Page("errors", "Errors", "Failure handling",
             "The response envelope, HTTP statuses, and the error codes worth "
             "branching on.",
             "Essentials", content.errors(lang)),
        Page("limits", "Limits", "Quotas & throttles",
             "Token throttles, per-operation limits, concurrency guards and plan quotas.",
             "Essentials", content.limits(lang)),
        Page("guides/importing-data", "Importing data", "Guide",
             "Synchronous, batched and job-based imports, with the limits and "
             "response shapes for each.",
             "Guides", content.importing(lang)),
        Page("guides/exporting-data", "Exporting data", "Guide",
             "Synchronous export and the asynchronous job flow, including polling "
             "and expiry.",
             "Guides", content.exporting(lang)),
    ]
    for slug, surface in REFERENCE:
        cls = api.surface(surface)
        count = len(cls.methods) if cls else 0
        pages.append(
            Page(f"reference/{slug}", surface, "Reference",
                 (cls.summary if cls else "").split(".")[0] + f". {count} methods.",
                 "Reference", reference_markdown(lang, api, surface))
        )
    return pages


# ----------------------------------------------------------------------
# HTML shell
# ----------------------------------------------------------------------

def _rel(path: str) -> str:
    depth = path.count("/")
    return "../" * depth if depth else ""


def _nav(pages: list[Page], current: str) -> str:
    out = ['<nav class="nav" aria-label="Documentation">']
    seen: list[str] = []
    for p in pages:
        if p.section not in seen:
            if seen:
                out.append("</ul>")
            out.append(f"<h2>{html.escape(p.section)}</h2><ul>")
            seen.append(p.section)
        href = _rel(current) + p.path + ".html"
        aria = ' aria-current="page"' if p.path == current else ""
        out.append(f'<li><a href="{href}"{aria}>{html.escape(p.title)}</a></li>')
    out.append("</ul></nav>")
    return "".join(out)


def _crumbs(page: Page, rel: str) -> str:
    bits = [f'<a href="{rel}index.html">Docs</a>']
    if "/" in page.path:
        bits.append('<span aria-hidden="true">/</span>')
        bits.append(f"<span>{html.escape(page.section)}</span>")
    bits.append('<span aria-hidden="true">/</span>')
    bits.append(f"<span>{html.escape(page.title)}</span>")
    return "".join(bits)


def _index_rail(toc: list[tuple[int, str, str]]) -> str:
    if len(toc) < 2:
        return ""
    items = "".join(
        f'<li class="lvl-{lvl}"><a href="#{slug}">{html.escape(text)}</a></li>'
        for lvl, slug, text in toc
    )
    return (
        '<nav class="index" aria-label="On this page">'
        "<h2>On this page</h2>"
        f"<ul>{items}</ul></nav>"
    )


def _pager(pages: list[Page], i: int, rel: str) -> str:
    prev_p = pages[i - 1] if i > 0 else None
    next_p = pages[i + 1] if i < len(pages) - 1 else None
    if not prev_p and not next_p:
        return ""
    out = ['<nav class="pager" aria-label="Pagination">']
    if prev_p:
        out.append(
            f'<a href="{rel}{prev_p.path}.html" rel="prev">'
            f"<span>Previous</span><strong>{html.escape(prev_p.title)}</strong></a>"
        )
    else:
        out.append("<span></span>")
    if next_p:
        out.append(
            f'<a href="{rel}{next_p.path}.html" rel="next">'
            f"<span>Next</span><strong>{html.escape(next_p.title)}</strong></a>"
        )
    out.append("</nav>")
    return "".join(out)


def render_page(lang: Lang, pages: list[Page], i: int) -> str:
    page = pages[i]
    rel = _rel(page.path)
    body_md = page.body

    # The <h1> is lifted into the editorial page header, so drop it from the body.
    body_md = re.sub(r"^#\s+.*\n", "", body_md, count=1)
    body_html, toc = mdlib.render(body_md)

    kind = "reference" if page.path.startswith("reference/") else "page"
    title = f"{page.title} · Zoho Analytics {lang.name} SDK"

    return f"""<!DOCTYPE html>
<html lang="en" data-kind="{kind}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(page.lede)}">
<meta name="color-scheme" content="light dark">
{theme.FONT_LINK}
<link rel="stylesheet" href="{rel}assets/docs.css">
<script>
// Applied before paint so a dark-mode reload does not flash light.
(function(){{try{{var t=localStorage.getItem('za-sdk-docs-theme');
if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="shell">
<aside class="rail" data-open="false">
  <a class="brand" href="{rel}index.html">
    <span class="brand__mark">Zoho Analytics</span>
    <span class="brand__name">REST API v2</span>
    <span class="brand__lang">{html.escape(lang.name)} SDK</span>
  </a>
  {_nav(pages, page.path)}
</aside>
<div class="main">
  <div class="topbar">
    <button class="ctl nav-toggle" type="button" data-nav-toggle
            aria-expanded="false" aria-label="Toggle navigation">Menu</button>
    <p class="crumbs">{_crumbs(page, rel)}</p>
    <div class="controls">
      <button class="ctl" type="button" data-theme-toggle aria-pressed="false">
        <span data-theme-label>Dark</span>
      </button>
    </div>
  </div>
  <div class="layout">
    <main class="article" id="main" tabindex="-1">
      <header class="page-head">
        <p class="page-head__kicker">{html.escape(page.kicker)}</p>
        <h1>{html.escape(page.title)}</h1>
        <p class="page-head__lede">{html.escape(page.lede)}</p>
      </header>
      {body_html}
      {_pager(pages, i, rel)}
      <footer class="foot">
        <span>Zoho Analytics {html.escape(lang.name)} SDK &middot; REST API v2</span>
        <span>Generated {BUILT}</span>
      </footer>
    </main>
    {_index_rail(toc)}
  </div>
</div>
</div>
<script src="{rel}assets/docs.js" defer></script>
</body>
</html>
"""


# ----------------------------------------------------------------------
# validation
# ----------------------------------------------------------------------

def validate(root: Path, pages: list[Page]) -> list[str]:
    problems: list[str] = []
    known = {p.path + ".html" for p in pages}
    for p in pages:
        base = Path(p.path).parent
        for m in re.finditer(r"\]\(([^)\s]+)\)", p.body):
            href = m.group(1)
            if href.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target, _, frag = href.partition("#")
            if not target:
                continue
            if not target.endswith(".md"):
                problems.append(f"{p.path}: link to non-markdown target {href!r}")
                continue
            resolved = (base / target.replace(".md", ".html")).as_posix()
            resolved = re.sub(r"^\./", "", resolved)
            # normalise ../
            parts: list[str] = []
            for seg in resolved.split("/"):
                if seg == "..":
                    if parts:
                        parts.pop()
                elif seg != ".":
                    parts.append(seg)
            resolved = "/".join(parts)
            if resolved not in known:
                problems.append(f"{p.path}: broken link {href!r} -> {resolved}")
    return problems


# ----------------------------------------------------------------------
# build
# ----------------------------------------------------------------------

def build_lang(key: str, write: bool) -> tuple[int, list[str]]:
    lang = LANGS[key]
    api = extract.load(key)
    pages = pages_for(lang, api)
    problems = validate(V2 / key / "docs", pages)

    if not write:
        return len(pages), problems

    out = V2 / key / "docs"
    if out.exists():
        shutil.rmtree(out)
    (out / "assets").mkdir(parents=True)
    (out / "guides").mkdir()
    (out / "reference").mkdir()

    (out / "assets" / "docs.css").write_text(theme.css(), encoding="utf-8")
    (out / "assets" / "docs.js").write_text(theme.js(), encoding="utf-8")

    for i, page in enumerate(pages):
        (out / (page.path + ".md")).write_text(page.body, encoding="utf-8")
        (out / (page.path + ".html")).write_text(
            render_page(lang, pages, i), encoding="utf-8"
        )
    return len(pages), problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lang", choices=ORDER, help="build one language")
    ap.add_argument("--check", action="store_true", help="validate without writing")
    args = ap.parse_args()

    failures = theme.check_contrast()
    if failures:
        print("Contrast check FAILED:")
        for f in failures:
            print("   ", f)
        return 1
    print(f"Contrast  : all text pairs pass WCAG AA (light + dark)")

    targets = [args.lang] if args.lang else ORDER
    total_problems = 0
    for key in targets:
        count, problems = build_lang(key, write=not args.check)
        total_problems += len(problems)
        status = "checked" if args.check else "written"
        api = extract.load(key)
        methods = sum(len(c.methods) for c in api.classes)
        print(f"{LANGS[key].name:<9} {count:>2} pages {status}, {methods:>3} methods documented"
              + (f"  [{len(problems)} link problems]" if problems else ""))
        for p in problems:
            print("     ", p)

    if total_problems:
        print(f"\n{total_problems} link problem(s).")
        return 1
    print("\nLinks     : every internal link resolves.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
