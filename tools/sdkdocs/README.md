# SDK documentation generator

Builds `<VERSION>/sdk/<lang>/docs/` for all seven SDKs from one source of truth.
Replaces the seven different tool outputs that used to live there (docfx, godoc,
JSDoc, phpDocumentor, epydoc, YARD), which looked nothing like each other and
carried none of the operational guidance.

Run it from the repository root. Like every other tool here it is
version-agnostic and takes `--version`:

```bash
python3 tools/sdkdocs/build.py                    # `latest` from manifest.json
python3 tools/sdkdocs/build.py --version v2.0     # a specific version
python3 tools/sdkdocs/build.py --lang go          # one language
python3 tools/sdkdocs/build.py --check            # validate, write nothing
```

No third-party dependencies — standard library only.

## Version layout

The generator itself knows nothing about v2. Two things carry the version:

| What | Where |
|---|---|
| The SDK sources it reads and the docs it writes | `<VERSION>/sdk/<lang>/` |
| The code snippets it embeds in the prose pages | `tools/sdkdocs/<VERSION>/snippets.py` |

`paths.py` resolves the first from `--version`; `langs.load_snippets()` loads the
second. **Supporting a new API version is: add `tools/sdkdocs/v3.0/snippets.py`.**
Nothing else changes — and if you forget, the build stops with a message naming
the file it wanted rather than rendering pages with holes in them.

## What it produces

Each `<lang>/docs/` gets 13 pages as **both** `.md` and `.html` siblings:

```
index              getting-started     authentication    configuration
errors             limits              guides/importing-data
guides/exporting-data                  reference/{analytics-client,org-api,
                                       workspace-api,view-api,bulk-api}
assets/docs.css    assets/docs.js
```

Markdown is the authored form and links to `.md`; the renderer rewrites those to
`.html`, so the markdown tree and the HTML tree are each independently
navigable. The HTML opens straight from the filesystem — no server, no build
step for the reader.

## Modules

| File | Responsibility |
|---|---|
| `paths.py` | The only module that knows the repository layout. Resolves `<VERSION>/sdk` from `--version`. |
| `extract.py` | Parses all seven doc-comment dialects into one `Api` model. |
| `langs.py` | Per-language profile: naming, construction, error surface, install notes. Version-independent. |
| `<VERSION>/snippets.py` | The 14 code snippets per language for that API version. **The only version-bound input.** |
| `content.py` | Shared page prose, parameterised by language. |
| `md.py` | Markdown → HTML. Stable anchors, `.md`→`.html` rewriting, `::: callout` blocks. |
| `theme.py` | Palette, type scale, CSS and JS. Also the WCAG contrast check. |
| `build.py` | Assembles pages, renders the shell, validates, writes. |

## Where content comes from

- **Reference pages** are generated from the doc comments in `<lang>/source/`.
  Fix a docstring there and rebuild; do not edit the generated markdown.
- **Code snippets** in `tools/sdkdocs/<VERSION>/snippets.py` mirror the verified
  sample programs under `<VERSION>/sdk/<lang>/sample/`. If a sample changes,
  change the snippet too.
- **Prose** (auth, errors, limits, guides) is authored in `content.py` and drawn
  from `<VERSION>/okf/foundations/`. It is shared across versions, so it still
  carries a few v2-era specifics — an example export URL, some error codes. When
  a second version lands, lift those into the version folder rather than
  branching `content.py`.

## Checks the build runs

1. **Contrast** — every text colour pair is verified against WCAG 2.1 AA in both
   themes. The build fails if any pair regresses.
2. **Links** — every internal markdown link must resolve to a generated page.

Both run on `--check` too, so this is safe to wire into CI.

## Design

Swiss / International Typographic: hairline rules rather than cards, one
vermillion signal colour, a three-font system (Archivo for structure, Source
Serif 4 for prose, JetBrains Mono for data), and a strict type scale. Fonts load
from Google Fonts with real fallback stacks, so the pages still read correctly
offline.

Accessibility: skip link, one `<h1>` per page, landmark roles, `aria-current`
on navigation, visible focus rings, 44px minimum control targets, keyboard-
reachable table scroll regions, `prefers-reduced-motion`, `prefers-color-scheme`
with a persisted manual override, and a print stylesheet. JavaScript is
progressive enhancement only — every page is fully readable and navigable
without it.
