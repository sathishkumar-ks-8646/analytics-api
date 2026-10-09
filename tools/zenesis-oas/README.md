# zenesis-oas

Move OpenAPI documents between their two shapes - the Zenesis-flavoured source that drives the
documentation site, and the clean, vendor-neutral OpenAPI 3.x that is published - **in either
direction**, and show where the two disagree.

```
       ZENESIS                                              ANALYTICS
<repo>/vN.N/zenesis-oas/        ──  to-analytics  ──►   <repo>/vN.N/oas/
      (the source)              ◄──  to-zenesis   ──    (the published copy; mirrored to zoho/analytics-oas)
                                ──    compare     ──
```

Every command names the two sides the same way and reads left to right - the
first path is where the content comes from, the second is where it goes. Only
`to-zenesis` reads its second path as well, because the Zenesis document is the
base of the merge.

No dependencies, no network, no config required to start.

## The two sides

Both sides live in this repository, one directory per API version. `VERSION` selects the version
directory (default `v2.0`); `make paths` prints what everything resolves to.

| Variable | Path in this repository | What it is |
| --- | --- | --- |
| `ZENESIS` | `<repo>/vN.N/zenesis-oas/` (and its `common/`) | the source, with the `x-zenesis-*` keys |
| `ANALYTICS` | `<repo>/vN.N/oas/` (and its `common/`) | the published, vendor-neutral copy |

```bash
make -C tools/zenesis-oas paths          # which paths am I about to read?
make -C tools/zenesis-oas inventory      # what vendor keys are in the source?
make -C tools/zenesis-oas to-analytics   # ZENESIS   -> ANALYTICS (the ten domain files, in place)
make -C tools/zenesis-oas compare        # ZENESIS   vs ANALYTICS: where do they disagree today?
make -C tools/zenesis-oas to-zenesis     # ANALYTICS -> ZENESIS: carry those differences back into the source
make -C tools/zenesis-oas check          # inventory + tests + verify, this is what CI runs
```

**No command takes an argument.** `VERSION=v3.0` switches every path to another version directory.
`ZENESIS` and `ANALYTICS` can still be overridden to point at a checkout elsewhere.

**`ANALYTICS/common/` is maintained by hand.** Every published specification references
`vN.N/oas/common/zoho-analytics-api-common.json` by the absolute URL of the zoho/analytics-oas
repository, and that file is placed there deliberately rather than regenerated. `make to-analytics`
therefore writes only the ten domain files into `ANALYTICS/`; the converted common file goes to
`dist/oas/vN.N/common/` and `make common-diff` shows what it would change.

## Requirements

Python 3.8 or newer. That is the entire list - the package imports only the
standard library, so it runs on any build agent without a pip install.

Nothing else: both sides are directories of this repository.

## The problem this solves

A Zenesis spec is already valid OpenAPI 3.1 - vendor extensions are legal
anywhere, and every conformant tool ignores keys beginning with `x-`. So this
is not a format conversion. It is a *separation*, and it does these jobs:

1. **Removes renderer-only decoration** so the published spec carries no
   Zenesis-specific keys.
2. **Rewrites private conventions into ecosystem ones.** `x-zenesis-enums-desc`
   becomes `x-enumDescriptions` (which Redocly renders) and `x-enum-varnames`
   (which SDK generators read to emit `Delimiter.COMMA` instead of
   `Delimiter._0`).
3. **Fixes what is actually wrong.** Zenesis stores the short label of an
   Example Object in `description` and the long prose in `summary`, which is
   the reverse of the specification. Any standard renderer shows those the
   wrong way round. The converter swaps them back.
4. **Rescues content that has nowhere standard to live.** Error-code tables,
   rate limits and HTML note blocks are folded into the operation description
   as Markdown, so they reach Swagger UI, SDK docs and MCP tool descriptions
   instead of being deleted.
5. **Puts examples where a schema reader can see them.** A Zenesis spec keeps
   its examples on the operation and the shape they illustrate in
   `components/schemas`, so anything that renders a schema on its own shows no
   sample value. The converter copies each operation's first example down the
   `$ref` chain into the schemas it describes.
6. **Repoints the shared components.** Every spec references the common file
   by absolute URL, and the two repositories keep it at different depths -
   `vN.N/zenesis-oas/common/` in the source, `vN.N/common/` in the published
   copy, which has no `zenesis-oas/` level. `common_ref` in `rules.json` names
   both URLs and the converter swaps them, so nobody edits 361 URLs by hand
   after each run.

The whole point is that nothing is lost quietly. Content that would vanish
gets either rewritten into a standard field or reported as a warning.

## The other direction

Fixes get made where the problem is noticed, and sometimes that is the
published copy - a reviewer corrects an enum in `analytics-oas` because that is
the file their generator read. That edit has to come back to the source or the
next `to-analytics` run erases it.

`to-zenesis` does that by machine. It is a three-way merge, not an inverse
function: the source is converted, the result is compared with the edited
published document, and every difference is written onto the source at the same
location - with four translations on the way:

| In the published document | Written to the source as |
| --- | --- |
| `enum` / `x-enumDescriptions` changed | `enum`, and `x-zenesis-enums-desc` rebuilt positionally from the map |
| Example Object `summary` / `description` edited | the two fields swapped back for the renderer |
| a `$ref` to the published common file | the same `$ref` to the source common file |
| an operation `description` edited **above** the folded Notes / Error codes / Rate limit | the source `description` |

What cannot come back is reported and left alone: an edit *inside* the folded
blocks (that text lives in `x-zenesis-sections`, `x-zenesis-statuscodes` or
`x-zenesis-security`; edit those), and an edit to a schema example the converter
seeded from a call site that the call site does not reproduce. After writing,
the merged source is converted once more and compared with the published
document; anything that still differs is listed, so you know exactly what to
finish by hand.

```
  reports-dashboards-grouped-api.json            40 edit(s) carried
  ...
  x-zenesis-enums-desc rebuilt from x-enumDescriptions  7
```

Review with `git diff vN.N/zenesis-oas`, then update `vN.N/md/` and the samples
in `vN.N/zenesis-oas-samples/` to match - those are prose and code, and the tool does not
touch them.

## Commands

`ZENESIS` is always the Zenesis-flavoured side and `ANALYTICS` the clean one.
Each may be a single `.json` file or a directory; two directories are paired
file by file on name.

| Command | Reads | Writes |
| --- | --- | --- |
| `to-analytics ZENESIS ANALYTICS` | `ZENESIS` | `ANALYTICS`. Exits non-zero if any file produced warnings. `convert` is an alias. |
| `to-zenesis ANALYTICS ZENESIS --in-place` | **both** - `ANALYTICS` for the edits, `ZENESIS` as the base of the merge | `ZENESIS`, over itself (or `--out PATH` to leave it alone). Exits non-zero when something could not be carried. |

| `compare ZENESIS ANALYTICS` | both | nothing. `--json` for tooling. Exits non-zero when there are differences, so it doubles as a drift check. |
| `inventory ZENESIS` | `ZENESIS` | nothing. Lists every vendor key with counts and an example location; exits non-zero if any key has no rule. **Run this first when adding specs.** |
| `overlay ZENESIS --out DIR` | `ZENESIS` | `DIR`. The Overlay 1.0.0 documents that turn converted output back into the source. |
| `verify ZENESIS [--overlays DIR]` | both | nothing. Proves `converted + overlays == original`, byte for byte. |

Every command prints the paths it is reading and writing before it starts, so
the direction is never in doubt:

```
  reading  v2.0/oas                                 clean OpenAPI, for the edits it carries
           v2.0/zenesis-oas                          the Zenesis source, as the base of the merge
  writing  v2.0/zenesis-oas                          the merged Zenesis source, in place
```

Every command accepts `--rules FILE`; without it, `./rules.json` is used when
present, else the built-in rules.

The shared components file converts too - its Example Objects carry the same
swapped fields - which is why `make to-analytics` also writes `dist/common/`,
and `make to-zenesis` / `make compare` also look at `ANALYTICS/common/`. Note
the depth differs by repository: the source keeps it at
`vN.N/zenesis-oas/common/`, the published copy at `vN.N/common/`.

## Updating either side

Edit the source in `vN.N/zenesis-oas/` and re-check:

```bash
make -C tools/zenesis-oas inventory      # does every vendor key still have a rule?
make -C tools/zenesis-oas check          # tests + verify
make -C tools/zenesis-oas to-analytics   # regenerate vN.N/oas/
make -C tools/zenesis-oas compare        # must report no differences afterwards
```

If `verify` reports `round trip lost data`, the vendor-key content of that spec changed and the
committed overlay is stale: run `make overlays`, re-run `make verify`, and commit the regenerated
overlays (`overlays/vN.N/`) with the change. That diff *is* the review of what changed.

`make inventory` ends in one of two ways.

**Every key already has a rule.** Nothing to do - `make to-analytics` handles it.

**A key has no rule.** Inventory marks it `<-- NOT IN rules.json` and exits 1.
Add an entry to `rules.json` choosing how to handle it, and to `KNOWN_VENDOR_KEYS` in
`tools/validate_api_docs.py`. See [docs/CONVERSION.md](docs/CONVERSION.md) for the available
actions. Only a key needing a genuinely new *transform* requires Python.

This is the mechanism that keeps the tool from rotting as Zenesis grows new
conventions. A new key can never be dropped silently.

## A new API version

Every version directory holds both sides, so one variable switches everything:

```bash
make -C tools/zenesis-oas check to-analytics VERSION=v3.0   # v3.0/zenesis-oas -> v3.0/oas
make -C tools/zenesis-oas compare            VERSION=v3.0
```

`common_ref` in `rules.json` names the `v2.0` common file on both sides. For
another version, point `--rules` at a copy with the `vN.N` URLs - or make the
Makefile derive them, once there is a second version to derive for.

## Configuring behaviour

`rules.json` holds one entry per vendor extension, plus the common-file URLs:

```json
{
  "vendor_prefix": "x-zenesis-",
  "unknown_key_policy": "warn",
  "common_ref": {
    "source":    "https://raw.githubusercontent.com/sathishkumar-ks-8646/analytics-api/refs/heads/main/v2.0/zenesis-oas/common/zoho-analytics-api-common.json",
    "published": "https://raw.githubusercontent.com/zoho/analytics-oas/refs/heads/main/v2.0/common/zoho-analytics-api-common.json"
  },
  "options": {
    "unswap_examples": true,
    "emit_enum_varnames": true,
    "propagate_examples": true
  },
  "rules": {
    "x-zenesis-title": { "action": "drop", "verify": "equals_sibling", "sibling": "summary" },
    "x-zenesis-enums-desc": { "action": "enum_descriptions" },
    "x-zenesis-statuscodes": { "action": "fold_status_codes", "heading": "Error codes" }
  }
}
```

Actions: `drop`, `keep`, `enum_descriptions`, `fold_sections`,
`fold_status_codes`, `fold_throttles`.
`unknown_key_policy`: `warn` (default), `drop`, `keep`, `error`.

`options` switch off the three transforms that are not driven by a vendor key:
`unswap_examples` (fix the swapped example fields), `emit_enum_varnames`
(`x-enum-varnames` for integer enums) and `propagate_examples` (seed component
schemas from their first call site). All three default to on. Omit
`common_ref` to leave `$ref`s untouched.

## Warnings are the product

The converter never guesses. When something looks wrong it says so and leaves
the data alone rather than producing plausible-looking damage.

- A `x-zenesis-title` that differs from `summary` → the text would be lost
- Prose in `x-zenesis-sections` that appears nowhere else in the operation
- An `enum` whose length does not match its label array → dropped, not aligned by guess
- An example where `summary` is already shorter than `description` → left untouched
- Any vendor key with no rule
- In reverse: an edit inside folded text, an enum value with no label, an edit
  to derived content that its origin does not reproduce

`make to-analytics`, `make to-zenesis` and `make verify` exit non-zero when
warnings appear, so these block a release rather than scrolling past in a log.

## Repository layout

```
<repo>/
  vN.N/
    zenesis-oas/          the source Zenesis JSON                       ZENESIS
      common/             the components those specs share              ZENESIS/common
    oas/                  the published, vendor-neutral copy            ANALYTICS
      common/             its copy of the shared components, by hand    ANALYTICS/common
  dist/oas/vN.N/common/   converted common file, for `make common-diff` <- gitignored
  tools/zenesis-oas/      this tool
    Makefile              the targets above; REPO and VERSION resolve every path
    rules.json            how each vendor key is handled, and the two common-file URLs
    overlays/vN.N/        generated Overlay 1.0.0, committed so vendor drift shows in review
    zenesis_oas/          the package
    tests/                standard-library test suite
    docs/CONVERSION.md    what every rule does
```

## Should I use the converter or an overlay?

The converter, almost always.

An [OpenAPI Overlay](https://spec.openapis.org/overlay/v1.0.0.html) is a
declarative document of `target`/`update` actions applied to a base spec. This
repo generates overlays, but only as an *audit artifact*: they prove the
conversion is lossless, and a diff in `overlays/` during review shows exactly
when someone introduced a new Zenesis convention.

Overlays cannot replace the converter, for two reasons. Their targets are
JSONPath pointers into one specific document, so they are not reusable across
files. And their actions carry literal values, not transforms - an overlay can
delete a key but cannot convert a positional array into a keyed map or swap two
fields.

The overlays describe the vendor-key separation only; the `$ref` URL swap is a
prefix replacement with an exact inverse, covered by the unit tests, and
`verify` leaves it out so the overlays stay about content.

## Publishing

`vN.N/oas/` is what users consume - the ten domain files and `oas/common/`. It is copied into
`vN.N/` of zoho/analytics-oas as it is: the `$ref`s already point at that repository's raw URL.
`make compare` must report no differences before you copy.

**`to-analytics` before `to-zenesis`.** `to-zenesis` treats whatever is in `vN.N/oas/` as the newer
text for any field it can carry, so run it only after an edit was deliberately made on that side.
`make compare` first: every line it lists is either something to regenerate or something to carry
back, and you decide which.

## Development

```bash
make -C tools/zenesis-oas test         # unit tests
cd tools/zenesis-oas && python3 -m unittest discover -s tests -v
cd tools/zenesis-oas && pip install -e .   # optional, gives you a `zenesis-oas` command
```
