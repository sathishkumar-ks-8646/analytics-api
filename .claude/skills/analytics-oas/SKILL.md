---
name: analytics-oas
description: Build and verify the vendor-neutral OpenAPI 3.1 documents in <VERSION>/oas/ of the analytics-api repository from <VERSION>/zenesis-oas/ using tools/zenesis-oas. Use when regenerating oas/, when "make compare" reports differences, when overlays changed or "round trip lost data", when a fix made in a published spec must be carried back upstream (to-zenesis), when the hand-maintained oas/common/ file is out of step, or when deciding what a new x-zenesis-* key should convert to.
---

# Build `<VERSION>/oas/` from `<VERSION>/zenesis-oas/`

`<VERSION>/oas/` is the **published, vendor-neutral** OpenAPI 3.1 shape — what Swagger UI, Redoc,
`openapi-generator`, MCP servers and the `zoho/analytics-oas` repository consume. It is produced by
`tools/zenesis-oas` from the Zenesis specifications, one domain file at a time.

**Never hand-edit `<VERSION>/oas/`.** The converter rewrites the ten domain files wholesale.
`<VERSION>/oas/common/` is the single exception — see §5.

No command takes an argument. `VERSION` selects the version directory (default `v2.0`); `REPO` is
derived from the Makefile's own location, so it works from any working directory.

```bash
make -C tools/zenesis-oas paths VERSION=v2.0      # show what the variables resolve to
make -C tools/zenesis-oas help
```

## 1. The commands

| Command | Reads | Writes |
|---|---|---|
| `make -C tools/zenesis-oas inventory` | `zenesis-oas/` | nothing — lists every vendor extension, **exits non-zero if any has no rule** |
| `make -C tools/zenesis-oas to-analytics` | `zenesis-oas/` | `oas/` — the ten domain files, in place |
| `make -C tools/zenesis-oas compare` | both | nothing — every difference with its path and both values; **exit 1 when there are any** |
| `make -C tools/zenesis-oas to-zenesis` | `oas/` and `zenesis-oas/` | `zenesis-oas/`, in place (or `OUT=dir`) |
| `make -C tools/zenesis-oas common-diff` | `zenesis-oas/common/` | nothing — the diff the hand-placed `oas/common/` would need |
| `make -C tools/zenesis-oas overlays` | `zenesis-oas/` | `tools/zenesis-oas/overlays/<V>/` |
| `make -C tools/zenesis-oas verify` | `zenesis-oas/` + overlays | nothing — proves the conversion is lossless |
| `make -C tools/zenesis-oas test` | — | nothing — unit tests |
| `make -C tools/zenesis-oas check` | | `inventory` + `test` + `verify` — **what CI runs** |

The normal build, which is what `pipeline.py --only oas` runs:

```bash
make -C tools/zenesis-oas check        VERSION=<V>    # → "All checks passed for <V>."
make -C tools/zenesis-oas to-analytics VERSION=<V>
make -C tools/zenesis-oas compare      VERSION=<V>    # → "No differences."
```

`compare` after `to-analytics` is not redundant: it proves the files on disk are exactly what the
converter produces, so a hand edit or a stale file is caught.

## 2. What the conversion does

Every transformation is driven by `tools/zenesis-oas/rules.json`. The converter only ever **removes
vendor keys, adds two enum keys beside them, swaps two fields inside Example Objects, appends to
operation descriptions, and seeds `examples` on component schemas** — it never moves or renames
anything else. That invariant is what makes the reverse direction possible.

| Vendor key | Action | Effect on `oas/` |
|---|---|---|
| `x-zenesis-title` | `drop` (verify it equals `summary`) | gone; warns if the two differed, because that text is then lost |
| `x-zenesis-doc`, `x-zenesis-usecase-tag`, `x-zenesis-shared-note`, `x-zenesis-shared-notes`, `x-zenesis-description-pageName` | `drop` | gone — pure renderer config |
| `x-zenesis-sections` | `fold_sections` | each HTML block converted to Markdown and appended to the operation `description` under `Notes`, **unless already covered** (`skip_covered`) |
| `x-zenesis-statuscodes` | `fold_status_codes` | rendered as a Markdown table appended to the **operation** description under `Error codes`; skipped with a warning if the heading is already there, so re-running never duplicates |
| `x-zenesis-security` | `fold_throttles` | rendered as "Rate limit" prose: *Up to 7 requests per 60 seconds. Exceeding this blocks further calls for 300 seconds.* |
| `x-zenesis-enums-desc` | `enum_descriptions` | becomes `x-enumDescriptions` (keyed map, Redocly's spelling) and, for integer-coded enums, `x-enum-varnames` |

Plus two passes that have no vendor key behind them:

- **`unswap_examples`** — Zenesis Example Objects carry the label in `description` and the sentence
  in `summary`. The converter swaps them back to the OpenAPI convention. Author them swapped; the
  conversion fixes it.
- **`propagate_examples`** — walks every call site (request bodies, response media types, **and
  Parameter Objects**, which matters because GET operations put CONFIG in a query parameter),
  following local `$ref`s one hop, and writes each example fragment onto the component schema that
  describes it. It deliberately will **not**: overwrite a schema that already has `example`/`examples`;
  invent a key where no call site has one; push into an `oneOf`/`anyOf` branch (it does push into
  every `allOf` branch); or edit through an external `$ref`. "First" means first in document order —
  paths, then operations, then request body before responses — so the result is stable across runs.

Finally the **common-file `$ref` prefix** is replaced with the published URL in every `$ref` (the
`#/components/...` pointer after it is untouched). Local `#/...` refs never match.

The result: the ten published files carry **no `x-zenesis-*` key at all** — only
`x-enumDescriptions` and `x-enum-varnames`.

Full detail: `tools/zenesis-oas/docs/CONVERSION.md`. For authoring the input side, see the
`analytics-zenesis-oas` skill.

## 3. Overlays — the proof, and the review signal

`make overlays` writes two OpenAPI Overlay 1.0.0 documents per spec into
`tools/zenesis-oas/overlays/<V>/`:

- `<name>.live.overlay.json` — genuine Zenesis config (`x-zenesis-usecase-tag`, `x-zenesis-doc`)
- `<name>.compat.overlay.json` — everything else, with an `x-migration` note on each action saying
  what to change so it can be deleted

They are **derived by diffing the original against the converted output**, so they are complete by
construction — the generator cannot forget a rule the converter applies. `make verify` reapplies
them and asserts byte equality with the source, which is what proves the conversion lossless.

**Commit them.** A diff in `overlays/` during code review is the signal that somebody added a new
vendor convention. If `verify` reports `round trip lost data`, the vendor-key content changed: run
`make -C tools/zenesis-oas overlays VERSION=<V>` and commit the regenerated directory.

There is also `strip-zenesis.overlay.json` — the blanket "remove every vendor key" overlay.

## 4. The reverse direction — `to-zenesis`

Carries an edit made to a published document back into its Zenesis source. A three-way merge:

```
base      the Zenesis source as it stands
expected  convert(base)            what the published document should look like
actual    the published document   as somebody edited it
```

Wherever `actual` differs from `expected`, that is an edit, applied to `base` at the same JSONPath.
Four cases are translated as they are written:

| Edit in the published document | Written to the source |
|---|---|
| `enum` / `x-enumDescriptions` / `x-enum-varnames` changed | `enum` as edited; `x-zenesis-enums-desc` rebuilt as `[labels[str(v)] for v in enum]`. A value with no label **warns and leaves the labels alone** — a positional array cannot have a gap. `x-enum-varnames` is never written back |
| `summary` / `description` on an Example Object | written through the same swap, so the long text lands back in `summary` |
| a `$ref` using the published common-file URL | the same `$ref` with the source URL |
| an operation `description` | the published description is `source + "\n\n" + folded blocks`. If the edit leaves the folded tail intact, the new head becomes the source description. **If it touches the tail the edit is refused with a warning** — that text lives in `x-zenesis-sections` / `-statuscodes` / `-security`, and writing Markdown into `description` would duplicate it on the next conversion |

Everything else — scalars, lists, added keys, removed keys, whole new schemas — is copied as is,
with the same translations applied recursively.

Two things are deliberately **not** carried: derived content (a component schema's `examples` seeded
by `propagate_examples` — edit the call-site example instead, and it follows on the next conversion)
and folded prose (edit the vendor key).

After merging, the tool converts the merged source once more and compares. Anything still different
is printed under `still differs` and the exit code is 1 — that is your hand-finishing list.

```bash
make -C tools/zenesis-oas to-zenesis VERSION=<V>              # writes over zenesis-oas/, review with git diff
make -C tools/zenesis-oas to-zenesis VERSION=<V> OUT=/tmp/z   # or write elsewhere, leaving the source untouched
```

Then re-run the full pipeline — the Zenesis side is upstream of `okf/` and `postman/` too.

## 5. The common file — the one hand-placed exception

```
<V>/zenesis-oas/common/zoho-analytics-api-common.json   SOURCE, authored, edit this
<V>/oas/common/zoho-analytics-api-common.json           PUBLISHED, placed by hand, never regenerated
```

`to-analytics` writes **only the ten domain files**; it never touches `oas/common/`. To see what the
hand-placed copy would need:

```bash
make -C tools/zenesis-oas common-diff VERSION=<V>
```

The conversion goes to a temporary directory; nothing is written into the repository. Report the
diff to the maintainer who owns that file; do not apply it yourself.

Every specification on both sides `$ref`s that file by **one absolute URL** — `common_ref` in
`<V>/manifest.json`:

```
https://raw.githubusercontent.com/zoho/analytics-oas/refs/heads/main/v2.0/common/zoho-analytics-api-common.json
```

Source and published happen to be the same URL today; `rules.json` names both under `common_ref`
and swaps one for the other, so they can diverge without any spec changing. **Never hand-change a
`$ref` URL** — `tools/validate_api_docs.py` errors on any remote `$ref` that is not `common_ref`.

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `inventory` exits non-zero, `x-zenesis-… <-- NOT IN rules.json` | a vendor key with no rule | add the rule to `rules.json` **and** the key to `KNOWN_VENDOR_KEYS` in `tools/validate_api_docs.py`; see `analytics-zenesis-oas` → `references/vendor-extensions.md` |
| `verify`: `round trip lost data` | vendor-key content changed | `make overlays VERSION=<V>` and commit `overlays/<V>/` |
| `compare` lists differences right after `to-analytics` | `oas/` was hand-edited, or a file is stale | re-run `to-analytics`; if the edit was deliberate, carry it back with `to-zenesis` |
| `x-zenesis-title … != summary` warning | the two drifted | make them identical — this also breaks the OKF join |
| `enum_descriptions` refuses | length mismatch, duplicate enum values, or no sibling `enum` | realign the positional array with `enum` |
| `fold_throttles` warns about an unknown key | something other than `throttles` under `x-zenesis-security` | use only `throttles` |
| `remote $ref targets …` from the source validator | a copied `$ref` points at the wrong URL | restore `common_ref` |
| `ZENESIS=… does not exist` / `ANALYTICS=… does not exist` | wrong `VERSION` | `make -C tools/zenesis-oas paths VERSION=<V>` |
| the common file differs | `oas/common/` is hand-placed | `make common-diff`, hand it to the maintainer |

## 7. After a successful build

`oas/` feeds `okf/` (`/references/openapi/` copies, schema names) and `postman/` (CONFIG examples,
header parameters, multipart parts). Continue the chain:

```bash
python3 tools/api-agent/pipeline.py --version <V> --from okf
```

To publish: copy `<V>/oas/` as is into `zoho/analytics-oas` `<V>/`, **after** `compare` reports no
differences. Its `$ref`s already use that repository's raw URL.
