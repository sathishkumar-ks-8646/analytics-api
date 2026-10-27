"""A small, deterministic Markdown -> HTML renderer.

Only the subset the generator actually emits is supported, which keeps the
output predictable and lets the renderer own things a general-purpose library
would not: stable heading anchors, `.md` -> `.html` link rewriting so the
markdown tree and the HTML tree are both independently navigable, and the
`::: callout` block used for notes, warnings and limits.

Supported: ATX headings, paragraphs, GFM pipe tables, fenced code, ordered and
unordered lists (one level of nesting), blockquotes, horizontal rules, callouts,
and inline code / bold / italic / links / autolinks.
"""

from __future__ import annotations

import html
import re

CALLOUT_KINDS = {
    "note": "Note",
    "warning": "Warning",
    "danger": "Critical",
    "limit": "Limit",
    "tip": "Tip",
}

_INLINE_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC = re.compile(r"(?<![\*\w])\*([^*\n]+)\*(?!\*)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_ANGLE_LINK = re.compile(r"<(https?://[^>\s]+)>")
_AUTOLINK = re.compile(r"(?<![\"\(=])\bhttps?://[^\s<>\)\]]+")


def slugify(text: str) -> str:
    text = re.sub(r"`", "", text)
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s_]+", "-", text) or "section"


def _rewrite_href(href: str) -> str:
    """Markdown sources link to .md; the HTML tree links to .html."""
    if href.startswith(("http://", "https://", "#", "mailto:")):
        return href
    if "#" in href:
        path, frag = href.split("#", 1)
        frag = "#" + frag
    else:
        path, frag = href, ""
    if path.endswith(".md"):
        path = path[:-3] + ".html"
    return path + frag


def inline(text: str) -> str:
    """Render inline markup. Code spans are protected from other rules."""
    spans: list[str] = []

    def stash(m: re.Match[str]) -> str:
        spans.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00{len(spans) - 1}\x00"

    text = _INLINE_CODE.sub(stash, text)

    # <https://...> must be resolved before escaping, or the closing angle
    # bracket becomes &gt; and is absorbed into the URL.
    def stash_angle(m: re.Match[str]) -> str:
        url = html.escape(m.group(1), quote=True)
        spans.append(f'<a href="{url}" rel="noopener noreferrer">{url}</a>')
        return f"\x00{len(spans) - 1}\x00"

    text = _ANGLE_LINK.sub(stash_angle, text)
    text = html.escape(text, quote=False)

    text = _LINK.sub(
        lambda m: f'<a href="{html.escape(_rewrite_href(m.group(2)), quote=True)}">{m.group(1)}</a>',
        text,
    )
    text = _AUTOLINK.sub(
        lambda m: f'<a href="{m.group(0)}" rel="noopener noreferrer">{m.group(0)}</a>',
        text,
    )
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    text = _ITALIC.sub(r"<em>\1</em>", text)

    return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], text)


class Renderer:
    def __init__(self) -> None:
        self.toc: list[tuple[int, str, str]] = []

    # -- block helpers -----------------------------------------------------

    def _heading(self, level: int, text: str) -> str:
        slug = slugify(text)
        base = slug
        n = 2
        while any(s == slug for _, s, _ in self.toc):
            slug = f"{base}-{n}"
            n += 1
        if level in (2, 3):
            self.toc.append((level, slug, re.sub(r"`", "", text)))
        inner = inline(text)
        anchor = (
            f'<a class="anchor" href="#{slug}" aria-label="Link to this section">#</a>'
        )
        return f'<h{level} id="{slug}">{inner}{anchor}</h{level}>'

    def _table(self, rows: list[str]) -> str:
        def cells(line: str) -> list[str]:
            line = line.strip()
            if line.startswith("|"):
                line = line[1:]
            if line.endswith("|"):
                line = line[:-1]
            return [c.strip() for c in line.split("|")]

        head = cells(rows[0])
        aligns = []
        for spec in cells(rows[1]):
            left, right = spec.startswith(":"), spec.endswith(":")
            aligns.append("center" if left and right else "right" if right else "left")
        out = ['<div class="table-scroll" tabindex="0" role="region" aria-label="Table">', "<table>", "<thead><tr>"]
        for i, h in enumerate(head):
            a = aligns[i] if i < len(aligns) else "left"
            out.append(f'<th scope="col" class="ta-{a}">{inline(h)}</th>')
        out.append("</tr></thead><tbody>")
        for row in rows[2:]:
            if not row.strip():
                continue
            out.append("<tr>")
            for i, c in enumerate(cells(row)):
                a = aligns[i] if i < len(aligns) else "left"
                out.append(f'<td class="ta-{a}">{inline(c)}</td>')
            out.append("</tr>")
        out.append("</tbody></table></div>")
        return "".join(out)

    def _list(self, items: list[tuple[int, str]], ordered: bool) -> str:
        """Nested lists belong inside the parent <li>, not beside it."""
        tag = "ol" if ordered else "ul"
        out = [f"<{tag}>"]
        depth = 0
        li_open = False
        for ind, text in items:
            lvl = 1 if ind >= 2 else 0
            while lvl > depth:
                # Keep the parent <li> open and nest the sublist within it.
                out.append(f"<{tag}>")
                depth += 1
                li_open = False
            while lvl < depth:
                if li_open:
                    out.append("</li>")
                    li_open = False
                out.append(f"</{tag}>")
                depth -= 1
                li_open = True  # the enclosing <li> is still open
            if li_open:
                out.append("</li>")
            out.append(f"<li>{inline(text)}")
            li_open = True
        while depth > 0:
            if li_open:
                out.append("</li>")
                li_open = False
            out.append(f"</{tag}>")
            depth -= 1
            li_open = True
        if li_open:
            out.append("</li>")
        out.append(f"</{tag}>")
        return "".join(out)

    # -- main --------------------------------------------------------------

    def render(self, text: str) -> str:
        lines = text.replace("\t", "    ").split("\n")
        out: list[str] = []
        i = 0
        para: list[str] = []

        def flush() -> None:
            if para:
                out.append(f"<p>{inline(' '.join(para))}</p>")
                para.clear()

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            if not stripped:
                flush()
                i += 1
                continue

            # fenced code
            if stripped.startswith("```"):
                flush()
                lang = stripped[3:].strip() or "text"
                i += 1
                body: list[str] = []
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    body.append(lines[i])
                    i += 1
                i += 1
                code = html.escape("\n".join(body))
                label = html.escape(lang)
                out.append(
                    f'<figure class="code" data-lang="{label}">'
                    f'<figcaption><span>{label}</span>'
                    f'<button class="copy" type="button" data-copy '
                    f'aria-label="Copy {label} code to clipboard">Copy</button></figcaption>'
                    f'<pre tabindex="0"><code class="language-{label}">{code}</code></pre>'
                    f"</figure>"
                )
                continue

            # callout
            if stripped.startswith(":::"):
                flush()
                spec = stripped[3:].strip()
                parts = spec.split(" ", 1)
                kind = parts[0].lower() if parts and parts[0] else "note"
                title = parts[1] if len(parts) > 1 else CALLOUT_KINDS.get(kind, "Note")
                i += 1
                body = []
                while i < len(lines) and not lines[i].strip().startswith(":::"):
                    body.append(lines[i])
                    i += 1
                i += 1
                inner = Renderer().render("\n".join(body))
                label = CALLOUT_KINDS.get(kind, "Note")
                out.append(
                    f'<aside class="callout callout--{kind}" role="note" '
                    f'aria-label="{html.escape(label)}">'
                    f'<p class="callout__kind">{html.escape(label)}</p>'
                    f'<p class="callout__title">{inline(title)}</p>'
                    f'<div class="callout__body">{inner}</div></aside>'
                )
                continue

            # heading
            hm = re.match(r"^(#{1,5})\s+(.*)$", stripped)
            if hm:
                flush()
                out.append(self._heading(len(hm.group(1)), hm.group(2).strip()))
                i += 1
                continue

            # horizontal rule
            if re.fullmatch(r"-{3,}|\*{3,}", stripped):
                flush()
                out.append("<hr>")
                i += 1
                continue

            # table
            if "|" in stripped and i + 1 < len(lines) and re.search(
                r"^\s*\|?[\s:|-]+\|[\s:|-]*$", lines[i + 1]
            ):
                flush()
                rows = []
                while i < len(lines) and "|" in lines[i] and lines[i].strip():
                    rows.append(lines[i])
                    i += 1
                out.append(self._table(rows))
                continue

            # blockquote
            if stripped.startswith(">"):
                flush()
                quote = []
                while i < len(lines) and lines[i].strip().startswith(">"):
                    quote.append(re.sub(r"^\s*>\s?", "", lines[i]))
                    i += 1
                out.append(f"<blockquote>{Renderer().render(chr(10).join(quote))}</blockquote>")
                continue

            # lists
            lm = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", line)
            if lm:
                flush()
                ordered = lm.group(2).endswith(".")
                items: list[tuple[int, str]] = []
                while i < len(lines):
                    m2 = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", lines[i])
                    if m2 and m2.group(2).endswith(".") == ordered:
                        items.append((len(m2.group(1)), m2.group(3)))
                        i += 1
                    elif lines[i].strip() and lines[i].startswith("  ") and items:
                        ind, prev = items[-1]
                        items[-1] = (ind, prev + " " + lines[i].strip())
                        i += 1
                    else:
                        break
                out.append(self._list(items, ordered))
                continue

            para.append(stripped)
            i += 1

        flush()
        return "".join(out)


def render(text: str) -> tuple[str, list[tuple[int, str, str]]]:
    r = Renderer()
    body = r.render(text)
    return body, r.toc
