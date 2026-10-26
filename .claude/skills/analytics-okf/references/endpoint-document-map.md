# The API Endpoint document — what lands where

One `## N. Title` markdown section joined with one OpenAPI operation produces one
`/domains/<domain>/<group>/<kebab(operationId)>.md`. Body sections are **H1** and always appear in
this order; subsections are H2; markdown `####` headings from the source become `###`.

| Section | Content | Source |
|---|---|---|
| `# Summary` | bold one-liner `**METHOD path** - Title (Group / Domain)`, then the markdown intro (everything before the first `###`, minus the attribute table). If the OpenAPI `description` shares fewer than **55%** of its words with the intro, it is appended under "From the OpenAPI specification:" | markdown intro + OpenAPI `description` |
| `# Endpoint` | attribute table: Operation ID, HTTP method, URL, Base URL, OAuth scope (linked), ZANALYTICS-ORGID header, Permission required, CONFIG parameter (location + mandatory flag), Request Content-Type, Success response, Rate limit, **any other `**Key**` row from the markdown attribute table**, OpenAPI pointer with schema names | OpenAPI operation + markdown attribute table |
| `# Request` → `## Headers` | Authorization, ZANALYTICS-ORGID (required / optional / not required), extra header params such as `ZANALYTICS-DEST-ORGID`, Content-Type when CONFIG is a body | OpenAPI `parameters` (`in: header`) + the markdown ORGID row |
| `## Path Parameters` | one row per `{placeholder}` with the OpenAPI description and a link to `/foundations/identifiers.md#<name>` | OpenAPI `parameters` (`in: path`), dereferenced |
| `## CONFIG Parameters` *(or the markdown's own heading)* | every markdown `###` block classified as **request** — verbatim, headings shifted up one level, links rewritten | markdown |
| `## Other Body Parts` | non-CONFIG multipart parts (`FILE`, `DATA`) | OpenAPI `requestBody` schema properties |
| `## Notes from the OpenAPI specification` | `x-zenesis-sections.apiRequestParameters / apiRequest / apiInfo`, HTML → bullets | OpenAPI |
| `# Response` → `## Success Response` | HTTP 200 with content types, or HTTP 204 no-body text | OpenAPI `responses` |
| `## Response Fields` | markdown blocks classified as **response-fields**, plus any `#### Response Field Reference` lifted out of a Sample Responses block | markdown |
| `## Notes from the OpenAPI specification` | `x-zenesis-sections.apiResponseParameters / apiResponseCodes` | OpenAPI |
| `# Examples` → `## Sample Requests`, `## Sample Responses` | verbatim markdown blocks | markdown |
| `## SDK Examples` | link to the SDK Example concept, listing the languages present | samples file |
| `# Notes & Behaviour` | markdown blocks classified as **notes**, then **every unrecognised `###` block under its own heading** | markdown |
| `# Error Codes` | merged table: markdown rows first, then `x-zenesis-statuscodes` rows not already present, then `8535` and `7005` if absent. Each code links to `/foundations/error-codes.md#error-<code>`; the HTTP column comes from observed sample responses or the `DEFAULT_HTTP` table | markdown + OpenAPI |
| `# Related` | group overview, domain overview, foundations links, sibling endpoints, SDK examples | generated |

## `###` block classification

The block's **name** decides where it lands. Use these exact names.

| Class | Recognised `###` names |
|---|---|
| request | `CONFIG Parameters`, `CONFIG Parameter`, `URL Parameters`, `FIELDS FOR CONFIG JSON`, `Sample values for CONFIG parameter`, `Query Parameters`, `Request Parameters`, `Request Body` |
| sample requests | `Sample Request`, `Sample Requests` |
| sample responses | `Sample Response`, `Sample Responses` |
| response fields | `Response Fields`, `Response Field Reference`, `Response Structure` (also as `####` inside Sample Responses) |
| notes | `Notes & Behaviour`, `Notes`, `Behaviour`, `Special Cases and Caveats` |
| error codes | `Error Codes` |
| *anything else* | kept under `# Notes & Behaviour` with its own heading — the fallback bucket |

Sub-tables inside a `###` block use `####`. **Never use `##` inside an endpoint section** — it starts
a new one.

## Frontmatter contract

```yaml
type: API Endpoint
title: <markdown title>
description: <first sentence of the OpenAPI description, else of the markdown intro>
resource: https://analyticsapi.zoho.com<path template>
tags: [zoho-analytics, rest-api-v2, <domain>, <group>, <method>, <scope families...>]
api:
  operation_id: <OpenAPI operationId, or the MD_ONLY_OPS value>
  method: GET|POST|PUT|DELETE
  path: /restapi/v2/...
  domain: <domain slug>
  group: <group slug>
  oauth_scopes: [...]
  org_id_header: required | optional | not-required
  config_parameter: { location: query|form|multipart|none, required: true|false }
  request_content_type: application/x-www-form-urlencoded | multipart/form-data   # when a body exists
  success_status: 200 | 204
  response_content_types: [...]
  permission_required: <the markdown Permission Required text, markdown stripped>
  rate_limit: <text>                                   # when documented
  error_codes: [ints]
  openapi:
    file: /references/openapi/<file>
    pointer: "#/paths/<escaped path>/<method>"
    config_schema: <name>
    response_schema: <name>
  sdk_examples: /sdk-examples/<domain>/<group>/<name>.md     # when samples exist
sources:
  - id: openapi-spec
    resource: /references/openapi/<file>
    title: ...
    author: team:zoho-analytics-api-docs
    last_modified: <mtime>
generated:
  at: <build time>
status: stable | deprecated
```

Enforced on every frontmatter block: **no `generated.by`**; empty lists and null values are dropped;
every `resource` is a bundle-internal path that exists or an `http(s)` URL; `status` stays last.

`api.*` is also the contract the Postman generator reads out of
`/references/endpoint-catalog.json` — an empty `permission_required` or a missing
`config_parameter.location` degrades the collection too.

## Attribute-table parsing

Rows of the form `| **Key** | value |`. Recognised keys:

| Key | Aliases |
|---|---|
| `Method` | `HTTP Method`, `METHOD` |
| `URL` | — |
| `OAuth Scope` | `OAUTHSCOPE` |
| `ZANALYTICS-ORGID Header` | `Mandatory Header` |
| `Permission Required` | `PERMISSION REQUIRED` |
| `Rate Limit` | — |

Unknown keys are copied into the `# Endpoint` table as extra rows — useful, not an error.

**ORGID header value:** starts with `Mandatory`/`Required` → `required`; starts with `Optional` →
`optional`; contains `Not required` → `not-required`. Text after an em dash becomes the note.

**URL placeholders:** write `<workspace-id>`; the generator converts to `{workspace-id}` for
markdown-only endpoints. Where the OpenAPI operation exists, its path wins.

## HTTP status detection for error codes

A **bold line containing `HTTP <3 digits>`** immediately followed by a ```json block containing
`"errorCode": N` records status N for code N:

```markdown
**HTTP 403 Forbidden — Caller lacks permission**
```json
{ "status": "failure", "summary": "SECURITY_NOT_PERMITTED", "data": { "errorCode": 7301, "errorMessage": "..." } }
```
```

Without it the catalog falls back to `DEFAULT_HTTP`, else 400.

Error-table rows: the **first cell must be a code** — `7104`, `**7104**`, or several (`8085 / 8086`).
Second cell the reason, third the solution. A backticked `UPPER_SNAKE` constant at the start of the
reason becomes that code's summary constant.

## Naming rules

| Thing | Rule | Example |
|---|---|---|
| domain directory | the `okf.slug` of the domain in `<V>/manifest.json` | `data-operations` |
| group directory | the group's `okf.slug` | `async-data-export` |
| endpoint file | `kebab(operationId)`, **acronym-aware** | `createAutoMLAnalysis` → `create-auto-ml-analysis.md` |
| SDK example file | the same name, under `/sdk-examples/` | |
| heading anchors | GitHub style: lower-case, punctuation dropped except hyphens, spaces → hyphens | `White Label / Client Portal Behaviour` → `#white-label--client-portal-behaviour` |
| error catalog anchors | `#error-<code>` | `/foundations/error-codes.md#error-7301` |
| identifier anchors | `#<parameter-name>` | `/foundations/identifiers.md#workspace-id` |
| scope anchors | slug of the scope | `/foundations/oauth-scopes.md#zohoanalyticsdataread` |

## The other concept types

| Type | Path | Built from |
|---|---|---|
| `API Overview` | `/overview.md` | handwritten — **counts in it are typed by hand**; update when totals change |
| `Guide` | `/how-to-use-this-bundle.md` | handwritten — describes the frontmatter contract; keep in step with the builder |
| `API Catalog` | `/endpoint-catalog.md` | fully generated from every endpoint |
| `API Domain` | `/domains/<domain>/overview.md` | the spec's `info.description` + `tags[].description`, plus generated group and endpoint tables |
| `API Group` | `/domains/<domain>/<group>/overview.md` | the markdown preamble (between the H1 and `## Index`) and every non-endpoint `##` section except `Index`, `Appendix A`, `Appendix B` — appendix headings lose their `Appendix X -` prefix — plus a generated endpoints table and the union of the group's error codes |
| `SDK Example` | `/sdk-examples/<domain>/<group>/<name>.md` | the samples file, one `##` per language in the order cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge |
| `Playbook` | `/workflows/<name>.md` | handwritten multi-endpoint procedures — **also drive the Postman playbook tables** |
| `Error Catalog` | `/foundations/error-codes.md` | every endpoint's Error Codes table + every `x-zenesis-statuscodes` + sample failure responses + the common examples file |
| `Reference` (generated) | `/foundations/{error-codes-quick-reference,oauth-scopes,rate-limits-and-quotas,permission-matrix,identifiers}.md` | scopes from the common file; throttles from `x-zenesis-security` and markdown `**Rate Limit**` rows; permissions from each `**Permission Required**` row; identifiers from path/header parameters plus `ID_SOURCES` |
| `Reference` / `Concept` / `Authentication` (handwritten) | the other 15 `/foundations/*.md` | copied as is — **not** regenerated, so review them whenever a rule they describe changes |
