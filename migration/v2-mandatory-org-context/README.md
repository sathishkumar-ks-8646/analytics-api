# migration/mandatory-org-context

The customer-facing migration guide for the Zoho Analytics REST API v2 move to
**mandatory organization context**: eight cross-organization endpoints replaced by
three organization-scoped ones, and two more endpoints that now require the
`ZANALYTICS-ORGID` header.

This folder is the guide *we publish to API consumers*. It is not internal notes —
write it for a developer outside the company who has to change their code.

> **The deprecated endpoints are switched off in March 2027.** That date appears on
> every page of the guide and must stay accurate. If it moves, change
> `REMOVAL_DEADLINE` in `build.py` and re-render; the strip at the top of every page,
> the footer and the hero all read from that one constant.

## What is in here

```
mandatory-org-context/
├── README.md                   you are here — how the folder works
├── build.py                    renders every *.md into an *.html sibling
├── zoho.svg                    the Zoho lettermark, inlined into every masthead
├── assets/
│   ├── migration.css           the design system
│   └── migration.js            theme toggle, copy buttons, filter, scrollspy
│
├── index.md          index.html             00  Start here
├── 01-why-org-context.md     .html          01  Why organization context is mandatory
├── 02-whats-changed.md       .html          02  What changed
├── 03-endpoint-migration.md  .html          03  Endpoint migration
├── 04-sdk-migration.md       .html          04  SDK migration
├── 05-knowledge-bases.md     .html          05  Knowledge bases & tools
├── 06-timeline.md            .html          06  Timeline & deprecation
└── 07-troubleshooting.md     .html          07  Troubleshooting & FAQ
```

**Markdown is the authored form. HTML is generated.** Edit the `.md` files and
re-run `build.py`; never hand-edit an `.html` file, because the next build
overwrites it. Both trees are independently navigable: the markdown links to
`.md`, and the renderer rewrites those to `.html` on the way out.

Open `index.html` in a browser straight from the filesystem — there is no server,
no build step for the reader, no webfonts and no network calls.

## Building

```bash
cd migration/mandatory-org-context

python3 build.py            # render every page
python3 build.py --check    # validate only, write nothing
```

`--check` verifies that every page has an `# H1`, that every internal link points
at a file that exists, and that every `#anchor` resolves to a real heading. It
exits non-zero if anything is wrong, so it is safe to run in CI.

No third-party dependencies — standard library only, same as the rest of the
repository's tooling.

## Writing a page

Front matter is optional and carries one key:

```markdown
---
description: One sentence. Becomes the <meta name="description">.
---

# Page title

The first paragraph after the H1 becomes the page lede.
```

The markdown subset the renderer understands:

| Syntax | Renders as |
|---|---|
| `## 3. Section title` | A numbered section with an `id`, and an entry in the right-hand table of contents. The number shows in the margin; the `id` is the slug of the title **without** the number. |
| `### Title`, `#### Title` | Sub-headings, each with an `id`. |
| `- item`, `1. item` | Lists. One level of nesting is supported. |
| <code>&#124; a &#124; b &#124;</code> | A GFM pipe table. Prefix a header cell with `^` to make that column narrow and non-wrapping. |
| `~~cell~~` in a table | Struck through in the "removed" red — for an old endpoint or method. |
| `++cell++` in a table | Bold in the "new" green — for its replacement. |
| ` ```lang ` | A code block with a copy button. |
| `:::kind Title` … `:::` | A callout. `kind` is `danger`, `warn`, `good`, `info` or `sunset`. |
| A line starting with `<` | A raw HTML block, passed through. `.md` links inside it are still rewritten to `.html`. |

### The `:::sunset` callout

Use it wherever a reader might otherwise think an old endpoint is still a
reasonable choice. It renders with a fixed **Deprecated** badge and the red
signal colour:

```markdown
:::sunset
`GET /restapi/v2/recentviews` is **deprecated** and switches off in **March 2027**.
:::
```

It is deliberately repetitive across the guide. Leave it that way — readers
arrive at individual chapters from search engines and internal links, not only
through `index.html`, so each page has to carry the warning on its own.

## The design system

The aesthetic is **Swiss technical**: a strict grid, hairline rules instead of
shadows, square corners, a tight grotesque against a neutral body face,
`decimal-leading-zero` section numbers and generous whitespace. No gradients, no
rounded cards, no webfonts, no framework.

Zoho's four brand colours are used as **semantic signals**, never as decoration:

| Colour | Token | Means |
|---|---|---|
| Red `#e42527` | `--zoho-red` | Removed, deprecated, will break |
| Yellow `#f9b21d` | `--zoho-yellow` | Action required, the deadline |
| Green `#089949` | `--zoho-green` | The new, correct way |
| Blue `#226db4` | `--zoho-blue` | Reference, neutral information |

The four-segment bar (`.spine`) in the page heads, the hero and the footer is the
only ornament in the system, and it always stands for those four signals.

The masthead carries the **Zoho lettermark** from `zoho.svg`. `build.py` inlines
it rather than referencing it with `<img>`, and rewrites its hardcoded black fill
to `currentColor`, so one asset serves both themes without a duplicate file or a
CSS filter. Replace `zoho.svg` and the change appears on every page at the next
build — but keep it a single-colour path, because it inherits `color` and any
baked-in fill will not adapt to the dark theme.

Each brand hue has an accessible text variant (`--sig-removed`, `--sig-warn`,
`--sig-new`, `--sig-info`) for anything that has to be legible; the brand hue
itself is reserved for fills, rules and bars. **Every text/background pair in
both themes meets WCAG AA (4.5:1).** If you change a colour, re-check it:

```bash
python3 - <<'EOF'
def lum(h):
    h = h.lstrip('#'); r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def ratio(a, b):
    la, lb = lum(a), lum(b); hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)
print(round(ratio('#b7141a', '#fbfaf7'), 2))   # must be >= 4.5
EOF
```

Light and dark themes are both defined. The theme follows the system preference
and can be overridden with the toggle in the masthead, which persists to
`localStorage`.

## Accessibility notes

Keep these when editing:

- A skip link to `#main` is the first focusable element on every page.
- The section navigation collapses behind a labelled toggle below 880 px.
- Every interactive control has an accessible name.
- Nothing conveys meaning by colour alone — the signal colours always accompany a
  word (`removed`, `changed`, `Deprecated`) or a strike-through.
- `prefers-reduced-motion` disables smooth scrolling and the copy-button fade.
- A print stylesheet drops the navigation and renders code blocks on white.

## Keeping it true

The guide states specific facts — endpoint paths, error codes, CONFIG limits,
response field names, SDK method signatures. They are drawn from the v2 sources
in this repository:

| Fact | Source of truth |
|---|---|
| Endpoint paths, CONFIG, errors | `v2.0/zenesis-oas/*.json` |
| Narrative behaviour | `v2.0/md/01 · Organization Management/ORG_LEVEL_LISTINGS.md` |
| SDK method names and signatures | `v2.0/sdk/<lang>/source/` |
| OKF bundle version and counts | `v2.0/okf/manifest.json` |
| What changed and when | `CHANGELOG.md`, *Unreleased* |

If any of those change, update this guide in the same commit.
