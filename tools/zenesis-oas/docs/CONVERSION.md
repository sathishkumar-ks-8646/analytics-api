# Conversion reference

What each rule does, how to add one, what to fix upstream, how the common-file
`$ref` is handled, and how the reverse direction decides what it can carry.

## Actions

### `drop`

Removes the key. Optionally verifies first, and warns instead of staying quiet
when the check fails.

```json
{ "action": "drop", "verify": "equals_sibling", "sibling": "summary" }
{ "action": "drop", "verify": "text_covered", "text_fields": ["value"] }
{ "action": "drop" }
```

| `verify` | Checks |
| --- | --- |
| `equals_sibling` | The value is identical to a named sibling field. Warns if not, since the difference would be lost. |
| `text_covered` | Prose in `text_fields` already appears in the enclosing operation's `description` / `summary` / `title`, following local `$ref`s. Warns if not. |
| *(omitted)* | Nothing. Use for pure renderer config with no prose. |

### `keep`

Leaves the key in place. Use for genuine vendor data you want in the published
spec.

### `enum_descriptions`

`x-zenesis-enums-desc` is a positional array parallel to `enum`. Reordering the
enum silently shifts every label. This action rewrites it as a keyed map:

```jsonc
// before
"enum": [0, 1, 2],
"x-zenesis-enums-desc": ["COMMA", "TAB", "SEMICOLON"]

// after
"enum": [0, 1, 2],
"x-enumDescriptions": { "0": "COMMA", "1": "TAB", "2": "SEMICOLON" },
"x-enum-varnames": ["COMMA", "TAB", "SEMICOLON"]
```

`x-enumDescriptions` is Redocly's spelling and renders as an option table.
`x-enum-varnames` is emitted only for integer-coded enums, where the labels are
symbolic *names* rather than prose — SDK generators read it to produce
`Delimiter.COMMA` instead of `Delimiter._0`.

Refuses and warns on: length mismatch, duplicate enum values, no sibling `enum`.
Set `options.emit_enum_varnames` to `false` to suppress the second key.

### `fold_sections`

`x-zenesis-sections` holds HTML note blocks. Roughly two thirds restate the
operation description; the rest carry constraints that exist nowhere else --
204-with-no-body behaviour, permission requirements, axis-casing rules.

Each block is converted to Markdown and appended to the enclosing operation's
description, **unless** the operation already covers that text. Across the ten
Zoho Analytics specs that means 122 blocks skipped as duplicates, 97 sections
fully redundant, and 70 blocks preserved that a plain `drop` would have lost.

```json
{ "action": "fold_sections", "heading": "Notes", "skip_covered": true, "text_fields": ["value"] }
```

Set `skip_covered` to `false` to fold everything regardless, or switch the
action to `drop` with `verify: text_covered` to delete instead and be warned
about what is lost.

The HTML converter handles exactly the vocabulary Zenesis uses -- `<b>`,
`<code>`, `<li>`, `<ul>`, `<br>`, `<blockquote>`, `<span>`. It is not a general
HTML converter. A new tag would pass through as plain text with the tag
stripped.

### `fold_throttles`

`x-zenesis-security` carries rate limits:

```json
{ "throttles": [{ "duration": 60, "threshold": 7, "lock-period": 300 }] }
```

No standard OpenAPI field holds rate limits, and every caller needs them, so
they are rendered as prose on the operation:

> **Rate limit**
>
> - Up to 7 requests per 60 seconds. Exceeding this blocks further calls for 300 seconds.

Warns if any key other than `throttles` appears, so a future addition is not
silently discarded.

### `fold_status_codes`

`x-zenesis-statuscodes` is an error-code catalogue: a list of
`{name, description, resolution}`. This is real API documentation, so deleting
it would strip content that developers and AI agents need.

The action renders it as a Markdown table appended to the enclosing
**operation** description. Note it appears on the `200` response in the source
specs even though every entry is an error, which is why the table goes on the
operation rather than the response it was attached to.

```json
{ "action": "fold_status_codes", "heading": "Error codes" }
```

Skips and warns if the description already contains the heading, so re-running
never duplicates the table.

## Schema examples

Not a rule -- there is no vendor key behind it. `propagate_examples` (an
`options` flag, on by default) runs after every rule has been applied.

A Zenesis spec keeps its examples at the call site and the shape they
illustrate in `components/schemas`:

```jsonc
// paths./data.put.requestBody.content['application/x-www-form-urlencoded']
"schema":   { "properties": { "CONFIG": { "$ref": "#/components/schemas/UpdateRowsConfig" } } },
"examples": { "updateMatching": { "value": { "CONFIG": { "columns": { "Sales": "2000" },
                                                         "criteria": "..." } } } }
```

Swagger UI's Schemas panel, `openapi-generator` model docs and MCP tool
descriptions render `UpdateRowsConfig` on its own, with no sample value --
even though the document holds one a few lines away. The pass walks the schema
and the example together and writes each fragment onto the component that
describes it:

```jsonc
// components.schemas.UpdateRowsConfig
"required": ["columns"],
"examples": [{ "columns": { "Sales": "2000" }, "criteria": "..." }]
```

It reads every `get` / `put` / `post` / `delete` (and the other four methods),
from three places: request body media types, response media types, and
Parameter Objects -- the last matters because the `GET` operations put their
`CONFIG` in a query parameter rather than a body. Local `$ref`s to shared
parameters, responses and examples are followed one hop.

Four things it deliberately does not do:

- **Overwrite.** A schema that already has `example` or `examples` keeps
  exactly what the author wrote. 142 of the 471 hits across the ten specs are
  skips for this reason.
- **Invent.** A call site with no example contributes nothing; the key is
  omitted rather than written as an empty list. Two schemas in
  `data-operations` still have no example, because nothing demonstrates them.
- **Guess a branch.** `allOf` composes one shape, so the value is pushed into
  every branch. `oneOf` / `anyOf` choose between shapes, and picking wrong
  would publish an example that does not validate, so they are left alone.
- **Leave the document.** An external `$ref` resolves to nothing here; writing
  the example would mean editing a file this repo does not own.

"First" means first in document order -- paths, then operations, then request
body before responses -- so two operations sharing a schema give the same
result on every run, and the winner is the one a reader meets first.

Set `options.propagate_examples` to `false` to skip the pass entirely.

## The common-file `$ref`

Not a rule either. Every spec references the shared components file by
absolute URL, and that URL differs between the source and the published copy:

```
source     https://raw.githubusercontent.com/sathishkumar-ks-8646/analytics-api/refs/heads/main/v2.0/zenesis-oas/common/zoho-analytics-api-common.json
published  https://raw.githubusercontent.com/zoho/analytics-oas/refs/heads/main/v2.0/common/zoho-analytics-api-common.json
```

The depth differs because the source repository groups the common file with the
specifications that reference it (`vN.N/zenesis-oas/common/`) while the
published repository has no `zenesis-oas/` level (`vN.N/common/`).

`common_ref` in `rules.json` names both. `to-analytics` replaces the source
prefix with the published one in every `$ref` (the `#/components/...` pointer
after it is untouched); `to-zenesis` does the reverse on anything it writes
into the source. Local `$ref`s (`#/...`) never match and are left alone.

`verify` and `overlay` run the conversion with the swap switched off. The
overlays describe the vendor-key separation; a prefix replacement with an
exact inverse would only add two actions per operation to them and prove
nothing. The inverse is asserted in the unit tests instead.

## Adding a rule for a new key

`make inventory` names any key without a rule. Then decide:

| The key is... | Use |
| --- | --- |
| A duplicate of a standard field | `drop` with `verify: equals_sibling` |
| HTML restating prose already present | `drop` with `verify: text_covered` |
| Pure renderer layout config | `drop` |
| Real vendor data to publish | `keep` |
| Content needing a new shape | a new handler in `rules.py` |

Only the last requires Python: add a function to `zenesis_oas/rules.py` with
the signature `(node, key, value, ctx, path, report)` and register it in
`HANDLERS`. Add a test in `tests/test_zenesis_oas.py` alongside it.

## Fixing the source instead

Several rules exist only because the Zenesis renderer needs something it should
not. Each of these can be retired by changing the renderer, which is strictly
better than converting around it forever:

| Change the renderer to... | Retires |
| --- | --- |
| Read `summary` as the example label and `description` as the prose | 83 field swaps |
| Fall back to `summary` when `x-zenesis-title` is absent | 32 duplicate titles |
| Read `x-enumDescriptions` | 79 positional arrays |
| Stop requiring `x-zenesis-sections` (the prose is already in `description`) | 18 HTML blocks |

The swap is the one worth doing regardless of everything else in this repo. It
is the only item that produces genuinely *wrong* output in standard tooling
rather than merely redundant output.

## Shared notes

`reports-dashboards` carries a note catalogue at
`$.components['x-zenesis-shared-notes']`, and each use site tags its copy with
`x-zenesis-shared-note` naming the catalogue key.

All 43 references resolve, and every materialised `value` is byte-identical to
its catalogue entry, so both keys are dropped: the prose is already inline at
each use site and `fold_sections` carries it into the description. If that
invariant ever breaks -- a note edited in the catalogue but not propagated --
the converter will not notice, because it only ever reads the inlined copy.
Keep the propagation step in the authoring workflow.

## The reverse direction

`to-zenesis` carries edits made to a published document back into its Zenesis
source. It is a three-way merge:

```
base      the Zenesis source as it stands
expected  convert(base)             what the published document should look like
actual    the published document    as somebody edited it
```

Wherever `actual` differs from `expected`, that is an edit, and it is applied
to `base` at the same JSONPath. The structures line up because the converter
only ever removes vendor keys, adds the two enum keys beside them, swaps two
fields inside Example Objects, appends to operation descriptions, and seeds
`examples` on component schemas - it never moves or renames anything else.

Four places need translating as they are written:

| Edit in the published document | What is written to the source |
| --- | --- |
| `enum`, `x-enumDescriptions` or `x-enum-varnames` changed on a schema | `enum` as edited; `x-zenesis-enums-desc` rebuilt as `[labels[str(v)] for v in enum]`. A value with no label is a warning and the labels are left as they were - a positional array cannot have a gap. `x-enum-varnames` is derived from the labels and never written back. |
| `summary` / `description` edited on an Example Object | Written through the same swap the converter applied, so the long text lands back in `summary` for the renderer. Detected on the `examples` map, exactly where `convert` swaps. |
| a `$ref` using the published common-file URL | The same `$ref` with the source URL (`common_ref`). |
| an operation `description` edited | The published description is `source + "\n\n" + folded blocks`. If the edit leaves the folded tail intact, the new head becomes the source description. If it touches the tail, the edit is refused with a warning: that text lives in `x-zenesis-sections`, `x-zenesis-statuscodes` or `x-zenesis-security`, and writing Markdown into `description` would duplicate it on the next conversion. |

Everything else - scalars, lists, added keys, removed keys, whole new schemas -
is copied as it is, after the same translations are applied recursively to the
new fragment (a new schema arriving with `x-enumDescriptions` is stored with
`x-zenesis-enums-desc`).

Two things are deliberately not carried:

- **Derived content.** A component schema's `examples` that the converter
  seeded from a call site is not in the source. If the published copy edits
  both the call-site example and the seeded one consistently, the call-site
  edit is carried and the seeded one follows on the next conversion - no
  warning. If only the seeded one was edited, that is a warning: the origin
  must change.
- **Folded prose**, as above.

After the merge the tool converts the merged source once more and compares it
with the published document. Anything still different is printed under
`still differs`, so the hand-finishing list is explicit and the exit code is 1.

`compare` is the same comparison without the merge: `convert(source)` against
the published document, every difference listed with its path and both values.

## Overlays

`make overlays` writes two documents per spec:

- `<name>.live.overlay.json` — genuine Zenesis config (`x-zenesis-usecase-tag`,
  `x-zenesis-doc`)
- `<name>.compat.overlay.json` — everything else, with an `x-migration` note on
  each action explaining what to change so it can be deleted

They are derived by diffing the original against the converted output, so they
are complete by construction — the generator cannot forget a rule the converter
applies. `make verify` reapplies them and asserts byte equality with the source.

Commit them. A diff in `overlays/` during code review is the signal that
somebody added a new vendor convention.
