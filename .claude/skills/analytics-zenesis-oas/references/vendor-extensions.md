# The ten `x-zenesis-*` extensions — authoring reference

Authoritative sources in the repository: `tools/zenesis-oas/rules.json` (the rules),
`tools/zenesis-oas/docs/CONVERSION.md` (what each action does),
`KNOWN_VENDOR_KEYS` in `tools/validate_api_docs.py` (the allow-list).

An `x-zenesis-*` key that is not one of these ten is a **hard validation error**. That is
deliberate: the alternative is a key silently dropped from every published artefact.

Current usage across the ten v2.0 specs, as a sanity check on what is normal:

| Key | Occurrences |
|---|---|
| `x-zenesis-enums-desc` | 210 |
| `x-zenesis-statuscodes` | 180 |
| `x-zenesis-title` | 177 |
| `x-zenesis-sections` | 154 |
| `x-zenesis-usecase-tag` | 92 |
| `x-zenesis-shared-note` | 46 |
| `x-zenesis-security` | 13 |
| `x-zenesis-doc` | 11 |
| `x-zenesis-description-pageName` | 2 |
| `x-zenesis-shared-notes` | 1 |

The published `oas/` carries **no** `x-zenesis-*` key at all — only `x-enumDescriptions` (210) and
`x-enum-varnames` (93), both produced by `enum_descriptions`.

---

## `x-zenesis-title` — operation

The renderer's title. Must equal `summary` exactly; the converter drops it after verifying that
(`verify: equals_sibling`), and warns when it does not — because the difference would be lost.

```jsonc
"summary": "Update Email Schedule",
"x-zenesis-title": "Update Email Schedule"
```

This string is also the **join key** with the markdown `## N. Title`. Three places, one string.

---

## `x-zenesis-statuscodes` — on the **success** response

An error-code catalogue. The only vendor key that carries API documentation nobody else has, which
is why it is folded into the operation description rather than dropped.

```jsonc
"responses": {
  "200": {
    "description": "Successfully updated the email schedule.",
    "content": { "application/json": { "schema": { "$ref": "#/components/schemas/UpdateEmailScheduleResponse" } } },
    "x-zenesis-statuscodes": [
      { "name": "7103",
        "description": "METAOBJECTNOTPRESENT — Workspace not found.",
        "resolution": "Verify <workspace-id> and the ZANALYTICS-ORGID header." },
      { "name": "8000",
        "description": "DUPLICATESCHEDULE — Another schedule in the workspace already uses the requested scheduleName.",
        "resolution": "Choose a different name." }
    ]
  }
}
```

Rules:

- **It sits on the success response**, even though every entry is an error. The validator errors if
  it sits on `4XX`, `500` or anywhere else; the converter and the OKF builder look nowhere else.
- `name` is the numeric code as a **string**.
- `description` opens with the `UPPER_SNAKE` constant, then an em dash, then the reason.
- `resolution` is one actionable sentence, in the imperative.
- `fold_status_codes` renders it as a Markdown table appended to the operation description under the
  heading `Error codes`; it skips and warns if that heading is already present, so re-running never
  duplicates it.
- The same rows must appear in the markdown `### Error Codes` table. OKF merges both, markdown rows
  first, then statuscodes not already present, then `8535` and `7005` if absent.

---

## `x-zenesis-security` — operation

Rate limits. No standard OpenAPI field holds them and every caller needs them, so they are rendered
as prose.

```jsonc
"x-zenesis-security": { "throttles": [ { "duration": 60, "threshold": 7, "lock-period": 300 } ] }
```

All three values are **seconds / request counts**, never minutes. The above renders as:

> **Rate limit**
>
> - Up to 7 requests per 60 seconds. Exceeding this blocks further calls for 300 seconds.

Any key other than `throttles` produces a warning, so a future addition is not silently discarded.
Keep it consistent with the markdown `| **Rate Limit** |` attribute row — OKF reads both.

---

## `x-zenesis-sections` — operation

HTML note blocks, keyed by the renderer slot they belong to and then by an index string:

```jsonc
"x-zenesis-sections": {
  "apiRequestParameters": {
    "1": {
      "type": "editor",
      "value": "<blockquote>Note:<br>\n<span style=\"font-weight:normal;\">\n<ul>\n<li>The COLUMNS array must hold at least one column. An empty array is rejected.</li>\n<li>Column names must be unique within the table. Duplicate names fail with error 7128.</li>\n</ul>\n</span></blockquote>"
    }
  }
}
```

| Slot | Rendered by OKF under |
|---|---|
| `apiRequestParameters` | `# Request` → `## Notes from the OpenAPI specification` |
| `apiRequest` | same |
| `apiInfo` | same |
| `apiResponseParameters` | `# Response` → `## Notes from the OpenAPI specification` |
| `apiResponseCodes` | same |

The HTML converter handles exactly the vocabulary Zenesis uses — `<b> <strong> <code> <ul> <li>
<br> <p> <blockquote> <span>`. It is **not** a general HTML converter; a new tag passes through as
plain text with the tag stripped.

`fold_sections` converts each block to Markdown and appends it to the operation `description`,
**unless the operation already covers that text** (`skip_covered: true`). Across the ten v2.0 specs
that skips 122 blocks as duplicates and preserves 70 that a plain `drop` would have lost.

**Guidance:** prefer putting behaviour in the markdown `### Notes & Behaviour` table, which the OKF
bundle carries verbatim. Use `x-zenesis-sections` when the renderer needs the note in a specific
slot, and accept that roughly two thirds of existing blocks merely restate the description.

---

## `x-zenesis-enums-desc` — schema property

A **positional array parallel to `enum`**. Reordering `enum` silently shifts every label, so always
edit the two together.

```jsonc
// integer-coded enum
"enum": [0, 1, 2],
"x-zenesis-enums-desc": ["COMMA", "TAB", "SEMICOLON"]
```

becomes, downstream:

```jsonc
"enum": [0, 1, 2],
"x-enumDescriptions": { "0": "COMMA", "1": "TAB", "2": "SEMICOLON" },
"x-enum-varnames": ["COMMA", "TAB", "SEMICOLON"]
```

`x-enumDescriptions` is Redocly's spelling and renders as an option table. `x-enum-varnames` is
emitted **only for integer-coded enums**, where the labels are symbolic names rather than prose, so
SDK generators produce `Delimiter.COMMA` instead of `Delimiter._0`.

For a string enum the labels are prose and only `x-enumDescriptions` is emitted:

```jsonc
"enum":                 ["PLAIN",      "MULTI_LINE", "EMAIL"],
"x-zenesis-enums-desc": ["Plain text", "Multi line", "Email address"]
```

`enum_descriptions` refuses and warns on: a length mismatch, duplicate enum values, or no sibling
`enum`. Mirror the same values in the markdown's `#### <field> Values` sub-table.

---

## `x-zenesis-usecase-tag` — operation or example

Groups request variants in the renderer. Dropped downstream.

```jsonc
"x-zenesis-usecase-tag": ["csv"]
```

On an operation it names the use cases; on an example it says which use case that example belongs to.

---

## `x-zenesis-doc` — operation

Renderer layout config. Dropped downstream, so it never affects a published artefact.

```jsonc
"x-zenesis-doc": {
  "show": true,
  "usecaseTags": {
    "single": { "name": "Single Column Attributes",
                "description": "<p>Applicable when a <strong>single column</strong> is added.</p>" },
    "bulk":   { "name": "Bulk Column Attributes",
                "description": "<p>Applicable when several columns are added in one request.</p>" }
  }
}
```

---

## `x-zenesis-shared-note` / `x-zenesis-shared-notes`

`reports-dashboards` carries a note catalogue at `components["x-zenesis-shared-notes"]`:

```jsonc
"components": {
  "x-zenesis-shared-notes": {
    "description": "Canonical text of the notes that apply to more than one API in this module...",
    "notes": { "axisTypeCasing": "<blockquote>Note:<br>...</blockquote>" }
  }
}
```

Each use site carries a **materialised copy** of the note inside its `x-zenesis-sections`, tagged
with `x-zenesis-shared-note` naming the catalogue key. All 43 references resolve and every
materialised value is byte-identical to its catalogue entry today, so both keys are dropped: the
prose is already inline and `fold_sections` carries it into the description.

> **The invariant is not checked.** The converter only ever reads the inlined copy. Editing the
> catalogue without propagating to every use site changes nothing downstream and nothing warns.
> Edit the catalogue entry first, then propagate it to every operation that references the key.

---

## `x-zenesis-description-pageName` — operation

Renderer page name. Dropped downstream.

---

## Adding an eleventh key

`make -C tools/zenesis-oas inventory VERSION=<V>` names any key without a rule and exits non-zero —
run it after editing a spec, before the key reaches a build.

| The key is… | Rule to add in `rules.json` |
|---|---|
| a duplicate of a standard field | `{"action": "drop", "verify": "equals_sibling", "sibling": "<field>"}` |
| HTML restating prose already present | `{"action": "drop", "verify": "text_covered", "text_fields": ["value"]}` |
| pure renderer layout config | `{"action": "drop"}` |
| real vendor data to publish | `{"action": "keep"}` |
| content needing a new shape | a new handler (Python) |

A new handler is a function in `tools/zenesis-oas/zenesis_oas/rules.py` with the signature
`(node, key, value, ctx, path, report)`, registered in `HANDLERS`, plus a test in
`tools/zenesis-oas/tests/test_zenesis_oas.py`.

Whichever you choose, also add the key to `KNOWN_VENDOR_KEYS` in `tools/validate_api_docs.py`, then
`make -C tools/zenesis-oas overlays VERSION=<V>` and commit the regenerated overlays — a diff there
is the code-review signal that a new vendor convention appeared.

## Retiring a rule instead

Several rules exist only because the Zenesis renderer needs something it should not. Each can be
retired by changing the renderer, which is strictly better than converting around it forever:

| Change the renderer to… | Retires |
|---|---|
| read `summary` as the example label and `description` as the prose | 83 field swaps |
| fall back to `summary` when `x-zenesis-title` is absent | 32 duplicate titles |
| read `x-enumDescriptions` | 79 positional arrays |
| stop requiring `x-zenesis-sections` (the prose is already in `description`) | 18 HTML blocks |

The example swap is the one worth doing regardless: it is the only item that produces genuinely
*wrong* output in standard tooling rather than merely redundant output.
