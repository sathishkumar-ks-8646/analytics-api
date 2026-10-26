---
name: analytics-zenesis-oas
description: Author or fix the Zenesis OpenAPI 3.1 specifications in <VERSION>/zenesis-oas/ of the analytics-api repository from the markdown reference in <VERSION>/md/ - operations, CONFIG schemas, examples, error responses, parameters and the ten x-zenesis-* vendor extensions. Use when adding or changing an endpoint's OpenAPI operation, a CONFIG attribute or enum, an error-code table, a rate limit or a note block; when validate_api_docs.py complains about tags, success responses, 4XX/500, statuscodes placement, vendor keys or remote $refs; or when a title/spec mismatch breaks the OKF join.
---

# Author the Zenesis OpenAPI specifications from the markdown

`<VERSION>/zenesis-oas/` holds **one OpenAPI 3.1 document per domain**, named
`<domain-slug>-grouped-api.json` where `<domain-slug>` is the domain's `slug` in
`<VERSION>/manifest.json`. No script derives these from the markdown — **you write them**, section by
section, to the contract below. Everything downstream (`oas/`, `okf/`, `postman/`) reads them.

The slug is a contract with every consumer. Never rename an existing file.

## 1. Document skeleton

```jsonc
{
  "openapi": "3.1.0",
  "info": {
    "title": "Zoho Analytics API",
    "version": "v2",
    "description": "API for <Domain title> in Zoho Analytics — <one clause naming what it covers>."
  },
  "servers": [ { "url": "https://analyticsapi.zoho.com" } ],
  "tags": [
    { "name": "Email Schedules", "description": "APIs for creating, updating, triggering, and deleting email schedules, and retrieving schedule details." }
  ],
  "paths": { "/restapi/v2/...": { "get": { /* operation */ } } },
  "components": {
    "parameters":      { "org-id": {}, "workspace-id": {}, "view-id": {} },
    "securitySchemes": { "iam-oauth2-schema": {} },
    "schemas":         { "<Op>Config": {}, "<Op>Response": {} }
  }
}
```

Hard requirements the validator enforces:

- `openapi` must start with `3.` (every file today is `3.1.0`), and `info` and `paths` must exist.
- Every path starts with `/`.
- **`tags[]` must declare exactly the tags the manifest lists for this domain** — one per API group,
  no more, no fewer. Every operation must carry its group's tag; an operation with no tag belongs
  to no group and is an error. A tag with no markdown group is an error too.
- `info.description` and each `tags[].description` are not decoration: the OKF builder renders them
  as the **domain overview** and the **group overview** headers.

## 2. One operation, field by field, derived from the markdown section

Markdown section → operation. Read this table with
`tools/okf/agent-guide/03-source-document-format.md` open for the markdown side.

| Markdown | Operation field | Rule |
|---|---|---|
| `## N. <Title>` | `summary` **and** `x-zenesis-title` | **Identical strings.** The validator warns if they differ (the converter drops the title and the text is lost); the OKF builder joins endpoints on this string. |
| — | `operationId` | camelCase, derived from the title (`Update Email Schedule` → `updateEmailSchedule`). **Unique across every file in the version.** Becomes the OKF endpoint filename via an acronym-aware kebab (`createAutoMLAnalysis` → `create-auto-ml-analysis`). |
| the intro paragraph(s) | `description` | Plain prose, no markdown links, no HTML. The first sentence becomes the OKF frontmatter `description`. If it shares fewer than 55% of its words with the markdown intro, OKF appends it under "From the OpenAPI specification:" — so keep it a faithful condensation, not a second description. |
| `\| **Method** \|` | the method key under the path | lower-case: `get`, `post`, `put`, `delete`. |
| `\| **URL** \|` | the path key | `<workspace-id>` in the markdown becomes `{workspace-id}` in the path template. |
| the group | `tags: ["<tag>"]` | the manifest `tag` of the group, declared in `tags[]`. |
| `\| **OAuth Scope** \|` | `security: [{ "iam-oauth2-schema": ["<scope>"] }]` | one array entry per scope. Also add the scope with a one-line purpose to `components.securitySchemes.iam-oauth2-schema.flows.authorizationCode.scopes`. |
| `\| **ZANALYTICS-ORGID Header** \|` | `parameters: [{ "$ref": "#/components/parameters/org-id" }]` | `required: true` on the shared `org-id` parameter means mandatory. For an **optional** org header use the file's `org-id-optional` variant (`workspace-management` defines one) or an inline parameter with `required: false` (`views-management` has one). A few files — `data-operations`, `reports-dashboards` — declare the header inline on the operation instead of via a `$ref`; follow whichever the neighbouring operations in that file use. |
| `<placeholder>` in the URL | `parameters: [{ "$ref": "#/components/parameters/<name>" }]` | one per placeholder, `in: path`, `required: true`. Reuse the shared parameter; its `description` becomes the row in `/foundations/identifiers.md`. |
| `\| **Permission Required** \|` | *nothing* | Permissions live in the markdown only; OKF reads the row directly. Do not invent a vendor key for it. |
| `\| **Rate Limit** \|` | `x-zenesis-security.throttles[0]` | `{ "duration": 60, "threshold": 7, "lock-period": 300 }`, all in **seconds**. |
| `### CONFIG Parameters` table | `components.schemas.<Op>Config` + the CONFIG carrier | see §3 and §4. |
| `#### <field> Values` sub-tables | `enum` + `x-zenesis-enums-desc` | see §5. |
| `### Sample Requests` → `**Case N — label**` | `examples.<camelCaseKey>` on the CONFIG carrier | see §6. |
| `### Sample Responses` → `**HTTP 200 OK — label**` | `responses.200...examples.<key>` | see §6. |
| `### Response Fields` table | `components.schemas.<Op>Response` | model the whole envelope: `status`, `summary`, `data`. |
| `### Error Codes` table | `x-zenesis-statuscodes` **on the success response** | see §7. |
| `### Notes & Behaviour`, extra `###` blocks | `x-zenesis-sections` *(optional)* | HTML note blocks; see §8. Prefer leaving behaviour in the markdown — the OKF bundle carries it verbatim. |
| the endpoint is retired | `"deprecated": true` | plus a note in the markdown section; OKF writes `status: deprecated`. |

### Worked skeleton (form CONFIG, the common case)

```jsonc
"/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}": {
  "put": {
    "operationId": "updateEmailSchedule",
    "summary": "Update Email Schedule",
    "description": "Updates an existing schedule's name, run period, recipients, or email content. Read Schedule ID Lifecycle first — this call can replace the schedule's ID.",
    "tags": ["Email Schedules"],
    "x-zenesis-title": "Update Email Schedule",
    "security": [ { "iam-oauth2-schema": ["ZohoAnalytics.modeling.update"] } ],
    "parameters": [
      { "$ref": "#/components/parameters/org-id" },
      { "$ref": "#/components/parameters/workspace-id" },
      { "$ref": "#/components/parameters/schedule-id" }
    ],
    "requestBody": { /* §3 */ },
    "responses": {
      "200": {
        "description": "Successfully updated the email schedule.",
        "content": { "application/json": {
          "schema": { "$ref": "#/components/schemas/UpdateEmailScheduleResponse" },
          "examples": { /* §6 */ }
        } },
        "x-zenesis-statuscodes": [ /* §7 */ ]
      },
      "4XX": { "$ref": "<common_ref>#/components/responses/CommonErrorResponse" },
      "500": { "$ref": "<common_ref>#/components/responses/UnexpectedErrorResponse" }
    }
  }
}
```

`<common_ref>` is literally the URL in `<VERSION>/manifest.json`:
`https://raw.githubusercontent.com/zoho/analytics-oas/refs/heads/main/v2.0/common/zoho-analytics-api-common.json`.
Any other remote `$ref` is a hard error. See `references/worked-example.md` for the same endpoint
shown end to end: markdown section → operation → what each knowledge base makes of it.

## 3. Where CONFIG travels — four shapes, pick exactly one

The OKF builder records this as `config_loc`; Postman builds the request from it.

**`query`** — GET endpoints. CONFIG is a query parameter, stringified and URL-encoded by the caller.

```jsonc
{
  "name": "CONFIG", "in": "query", "required": false,
  "description": "Configuration that filters, paginates and sorts the list. As this is a GET request, the value must be stringified and URL encoded before it is sent.",
  "schema": { "$ref": "#/components/schemas/GetQueryTablesConfig" },
  "style": "form", "explode": false,
  "examples": { "keywordSearch": { /* §6 */ } }
}
```

**`form`** — POST / PUT / DELETE with a body. The `encoding` block is required: it declares that the
form field holds JSON.

```jsonc
"requestBody": {
  "required": true,
  "content": { "application/x-www-form-urlencoded": {
    "schema": { "type": "object", "required": ["CONFIG"],
                "properties": { "CONFIG": { "$ref": "#/components/schemas/UpdateEmailScheduleConfig" } } },
    "encoding": { "CONFIG": { "contentType": "application/json" } },
    "examples": { /* §6 */ }
  } }
}
```

**`multipart`** — imports. `FILE` and `DATA` become the OKF "Other Body Parts" section and the
Postman `formdata` parts.

```jsonc
"requestBody": {
  "description": "Sent as multipart/form-data. CONFIG is mandatory and must be sent as a form field along with either FILE or DATA - exactly one of the two.",
  "required": true,
  "content": { "multipart/form-data": {
    "schema": { "type": "object", "required": ["CONFIG"], "properties": {
      "FILE":   { "type": "string", "format": "binary", "description": "The file to be imported. Maximum allowed file size is 20 MB. Send either FILE or DATA, not both." },
      "DATA":   { "type": "string", "description": "The raw string to be imported, in the format declared by fileType in CONFIG. Send either FILE or DATA, not both." },
      "CONFIG": { "$ref": "#/components/schemas/ImportConfigNewTable" }
    } },
    "encoding": { "FILE": { "contentType": "application/octet-stream" },
                  "DATA": { "contentType": "text/plain" },
                  "CONFIG": { "contentType": "application/json" } },
    "examples": { /* §6 */ }
  } }
}
```

**`none`** — no CONFIG at all. Omit the parameter and the request body entirely.

Mandatory vs optional is read from the `required` list (`form`/`multipart`) or the parameter's
`required` flag (`query`) — it must agree with the markdown's "CONFIG is **mandatory**/**optional**"
sentence.

## 4. Schema authoring

- **Names.** `<OperationTitleWithoutSpaces>Config` and `...Response` (`UpdateEmailScheduleConfig`,
  `UpdateEmailScheduleResponse`). Nested shapes get a descriptive name of their own
  (`ScheduleDetails`, `ScheduleCc`, `CcEmailIds`) and are referenced with a local `$ref`.
- Give every object schema a `title` equal to its component name and a one-sentence `description`.
  Both surface in Swagger UI, SDK model docs and MCP tool descriptions.
- Each property: `type`, `description` (the markdown Description cell, rewritten as prose without
  markdown links), `default` when the markdown has one, `enum` when the markdown lists values.
- `required` lists exactly the markdown rows whose Mandatory cell is `**Yes**`.
- **Reuse before you add.** Check `components.parameters` and existing schemas first; a shared
  `$ref` keeps the identifiers document and the SDK models coherent.
- Model the **whole response envelope** — `status`, `summary`, `data` — not just `data`.
- Keep 2-space indent, a trailing newline, and key order close to the neighbours so the diff stays
  reviewable.

## 5. Enums and their labels

`x-zenesis-enums-desc` is a **positional array parallel to `enum`**. Reordering `enum` silently
shifts every label.

```jsonc
"dataType": {
  "type": "string",
  "description": "The data type to be applied to the column.",
  "enum":                  ["PLAIN",      "MULTI_LINE", "EMAIL",         "NUMBER"],
  "x-zenesis-enums-desc":  ["Plain text", "Multi line", "Email address", "Whole number"]
}
```

The converter rewrites it to a keyed map `x-enumDescriptions` (Redocly's spelling, renders as an
option table) and, **for integer-coded enums only**, `x-enum-varnames` so SDK generators emit
`Delimiter.COMMA` instead of `Delimiter._0`. It refuses and warns on a length mismatch, duplicate
enum values, or no sibling `enum`.

Edit the two arrays together, always, and keep them aligned index by index.

## 6. Examples — and the field swap you must reproduce

Zenesis Example Objects carry the **short label in `description`** and the **sentence in `summary`** —
the inverse of the OpenAPI convention. The converter un-swaps them for the published spec
(`options.unswap_examples`). **Author them swapped**, matching every neighbour:

```jsonc
"examples": {
  "changeFrequency": {
    "description": "Change frequency",
    "summary": "Renames the schedule and switches it to run every day at 10:30.",
    "value": { "CONFIG": { "scheduleName": "Daily Sales Overview",
                           "scheduleDetails": { "calendarFrequency": "daily", "hour": 10, "minute": 30 } } }
  }
}
```

- One example key per `**Case N — label**` in `### Sample Requests`; the key is a camelCase slug of
  the label (`changeFrequency`, `updateRecipients`, `fileImport`, `paginatedList`).
- `description` = the case label. `summary` = one sentence saying what the call does.
- `value` wraps the payload in `{ "CONFIG": { ... } }` for `form` and `multipart`; for a `query`
  CONFIG the value **is** the CONFIG object, unwrapped.
- Success-response examples go under `responses.200.content.application/json.examples` with the same
  swap, and their `value` is the full envelope (`status`, `summary`, `data`).
- **The first example is load-bearing**: Postman puts it on the request as the ready-to-send CONFIG,
  and the converter's `propagate_examples` pass copies it onto the component schema that describes
  it (never overwriting one an author wrote, never into `oneOf`/`anyOf` branches). Put the most
  representative case first.
- `x-zenesis-usecase-tag` may appear on an example to tag a variant (`["csv"]`); it is dropped
  downstream.

## 7. Error codes

The `### Error Codes` table becomes `x-zenesis-statuscodes`, an array of
`{name, description, resolution}` placed **on the success response** — not on `4XX`. The validator
errors if it sits anywhere else; the converter folds it into the operation description as a table,
and OKF merges it with the markdown table into `/foundations/error-codes.md`.

```jsonc
"x-zenesis-statuscodes": [
  { "name": "7812",
    "description": "SCHEDULEDELETED — No schedule exists with the given <schedule-id>. Commonly a stale ID after an earlier update regenerated it.",
    "resolution": "Re-resolve the current ID via Get Email Schedules." }
]
```

- `name` is the numeric code **as a string**.
- `description` opens with the `UPPER_SNAKE` constant, an em dash, then the reason.
- `resolution` is one actionable sentence.
- Mirror the same rows in the markdown `### Error Codes` table, and when the HTTP status matters add
  a sample response labelled `**HTTP NNN ...**` above a ```json block containing `"errorCode": N` —
  that bold line is how the catalog learns the status. Otherwise it falls back to `DEFAULT_HTTP`
  or 400.
- Never hand-write a link to the error catalog. A backticked 4-to-6-digit code in prose is
  auto-linked.

## 8. The ten vendor extensions

Only these may appear. An unknown `x-zenesis-*` key is a **hard error** in
`tools/validate_api_docs.py` — by design, so it cannot be dropped silently downstream.

| Key | Where | Carries | Converter action |
|---|---|---|---|
| `x-zenesis-title` | operation | the markdown title | `drop`, after verifying it equals `summary` |
| `x-zenesis-statuscodes` | **success** response | error-code catalogue | `fold_status_codes` → table in the operation description |
| `x-zenesis-security` | operation | `{throttles:[{duration, threshold, lock-period}]}` in seconds | `fold_throttles` → "Rate limit" prose |
| `x-zenesis-sections` | operation | HTML note blocks under `apiRequestParameters`, `apiRequest`, `apiInfo`, `apiResponseParameters`, `apiResponseCodes`, each `{ "<n>": { "type": "editor", "value": "<html>" } }` | `fold_sections` → appended to the description unless already covered |
| `x-zenesis-enums-desc` | schema property | positional enum labels | `enum_descriptions` → `x-enumDescriptions` / `x-enum-varnames` |
| `x-zenesis-usecase-tag` | operation / example | renderer use-case grouping | `drop` |
| `x-zenesis-doc` | operation | renderer layout config | `drop` |
| `x-zenesis-shared-note` | section block | the key it was materialised from | `drop` |
| `x-zenesis-shared-notes` | `components` | the note catalogue (reports-dashboards only) | `drop` |
| `x-zenesis-description-pageName` | operation | renderer page name | `drop` |

`x-zenesis-sections` HTML is converted by a converter that knows exactly the Zenesis vocabulary:
`<b> <strong> <code> <ul> <li> <br> <p> <blockquote> <span>`. A new tag passes through stripped.

**Shared notes:** in `reports-dashboards`, `components["x-zenesis-shared-notes"].notes.<key>` is the
canonical text and each use site carries a materialised copy inside its `x-zenesis-sections` tagged
with `x-zenesis-shared-note`. The converter only ever reads the inlined copy, so **editing the
catalogue without propagating to every use site silently does nothing.** Propagate, always.

Adding an eleventh key is a deliberate act: add the rule to `tools/zenesis-oas/rules.json`, the name
to `KNOWN_VENDOR_KEYS` in `tools/validate_api_docs.py`, a handler in
`tools/zenesis-oas/zenesis_oas/rules.py` if it needs a new shape, and a test. See
`references/vendor-extensions.md`.

## 9. The common file

`<VERSION>/zenesis-oas/common/zoho-analytics-api-common.json` is the authored copy of the shared
components. Edit it here, never in `<VERSION>/oas/common/`.

- `components.securitySchemes.iam-oauth2-schema.flows.authorizationCode.scopes` is the **full scope
  list** and drives `/foundations/oauth-scopes.md`. A new scope goes in here.
- `components.responses.CommonErrorResponse` and `UnexpectedErrorResponse` are what every operation
  `$ref`s; the validator errors if either is missing.
- `components.examples.*` supply summary constants for common error codes.
- Only `zoho-analytics-api-common.json` (and a `README.md`) may live in that directory.
- Show the maintainer what to mirror: `make -C tools/zenesis-oas common-diff`.

## 10. Verify

```bash
python3 tools/validate_api_docs.py --strict --version <V>   # must print errors=0 warnings=0
make -C tools/zenesis-oas inventory VERSION=<V>              # any vendor key without a rule
make -C tools/zenesis-oas check    VERSION=<V>               # inventory + tests + lossless round trip
python3 tools/api-agent/pipeline.py --version <V>            # then the whole chain
```

### Checklist before you call it done

- [ ] `summary` == `x-zenesis-title` == the markdown `## N. Title`, character for character
- [ ] `operationId` is camelCase and unique across every file in the version
- [ ] the operation carries its group's tag, and that tag is declared in `tags[]`
- [ ] `security` names the same scope the markdown attribute table names, and the scope exists in the
      common file
- [ ] every URL placeholder has a path parameter, every one `$ref`s a shared parameter where one exists
- [ ] exactly one success response (`200`/`201`/`204`), plus `4XX` and `500` `$ref`ing `common_ref` —
      and no `default`
- [ ] `x-zenesis-statuscodes` is on the success response and mirrors the markdown `### Error Codes`
      table
- [ ] `required` lists match the markdown Mandatory column
- [ ] `enum` and `x-zenesis-enums-desc` are the same length and aligned
- [ ] examples are **swapped** (`description` = label, `summary` = sentence) and the most
      representative one is first
- [ ] no vendor key outside the ten
- [ ] no internal class, template or XML attribute name anywhere in the prose
- [ ] the samples file has an entry for this exact path template and lower-case method
      (→ `analytics-oas-samples`)
