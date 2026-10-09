# 02 - Bundle structure and content placement

The bundle root is `<VERSION>/okf/`. It is an OKF v0.2 bundle: every non-reserved `.md`
file has YAML frontmatter that starts with `type`; `index.md` and `log.md` are reserved listing files
(the root `index.md` carries `okf_version: "0.2"`); links beginning with `/` are bundle-relative.

```
bundle/
├── index.md                       root listing (generated: write_root_index)
├── log.md                         update log (generated: write_log)
├── manifest.json                  name, version, okf_version, counts, entry points (generated: bundle_manifest)
├── overview.md                    API Overview            (handwritten/overview.md)
├── how-to-use-this-bundle.md      Guide                   (handwritten/how-to-use-this-bundle.md)
├── endpoint-catalog.md            API Catalog             (generated: render_endpoint_catalog)
├── foundations/                   cross-cutting rules     (mix: 13 handwritten, 7 generated)
├── domains/<domain>/              API Domain overview + groups
│   └── <group>/                   API Group overview + one API Endpoint file per operation
├── workflows/                     Playbooks               (tools/okf/handwritten/<VERSION>/workflows/*.md)
├── sdk-examples/<domain>/<group>/ SDK Example per operation (generated: render_sdk)
└── references/
    ├── openapi/*.json             copies of <VERSION>/zenesis-oas/*.json + zoho-analytics-api-common.json
    └── endpoint-catalog.json      machine-readable catalog (generated: catalog_json)
```

Every directory gets an `index.md` from `write_indexes()`, listing `overview.md` first, then concepts
(title and description from their frontmatter), then subdirectories.

## Concept types and where each comes from

| Type | Path pattern | Produced by | Source of the content |
|---|---|---|---|
| `API Overview` | `/overview.md` | copy of handwritten | Hand-written prose. Counts in it are typed by hand; update when domains or endpoint totals change. |
| `Guide` | `/how-to-use-this-bundle.md` | copy of handwritten | Hand-written. Describes the frontmatter contract; keep in step with the builder. |
| `API Catalog` | `/endpoint-catalog.md` | `render_endpoint_catalog` | All endpoints; fully generated. |
| `API Domain` | `/domains/<domain>/overview.md` | `render_domain_overview` | `info.description` and `tags[].description` of the domain's OpenAPI file, plus generated group and endpoint tables. |
| `API Group` | `/domains/<domain>/<group>/overview.md` | `render_group_overview` | The markdown file's preamble (text between the H1 and `## Index`) and every non-endpoint `##` section except `Index`, `Appendix A`, `Appendix B`; appendix headings lose their `Appendix X -` prefix. Plus a generated endpoints table and the union of error codes used in the group. |
| `API Endpoint` | `/domains/<domain>/<group>/<kebab(operationId)>.md` | `render_endpoint` | One `## N. Title` markdown section joined with one OpenAPI operation. See the section map below. |
| `SDK Example` | `/sdk-examples/<domain>/<group>/<kebab(operationId)>.md` | `render_sdk` | `zenesis-oas-samples/<domain>-grouped-api-samples.json[path][method]`, one `##` per language in the order cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge. |
| `Playbook` | `/workflows/<name>.md` | copy of handwritten | Hand-written multi-endpoint procedures. |
| `Error Catalog` | `/foundations/error-codes.md` | `render_error_catalog` | Aggregated from every endpoint's Error Codes table, every OpenAPI `x-zenesis-statuscodes`, sample failure responses (for HTTP status and summary constants) and the common examples file. |
| `Reference` (generated) | `/foundations/{error-codes-quick-reference,oauth-scopes,rate-limits-and-quotas,permission-matrix,identifiers}.md` | `render_error_quick_reference`, `render_scopes`, `render_rate_limits`, `render_permission_matrix`, `render_identifiers` | Scopes from the common file; throttles from OpenAPI `x-zenesis-security` and markdown `**Rate Limit**` rows; permissions from each endpoint's `**Permission Required**` row; identifiers from OpenAPI path and header parameters plus the `ID_SOURCES` table in the builder. |
| `Reference`, `Concept`, `Authentication` (hand-written) | `/foundations/*.md` (the other 13 files) | copy of handwritten | Hand-written from the markdown reference; **not** regenerated when the sources change, so they need a manual review whenever a rule they describe changes. |

Handwritten foundation files: `authentication`, `data-centers`, `request-conventions`,
`response-envelope`, `http-status-codes`, `roles-and-permissions`, `filter-criteria-syntax`,
`asynchronous-jobs`, `white-label-client-portal`, `export-formats-and-enums`, `import-options-and-enums`,
`glossary`, `sdk-clients`.

## The API Endpoint document, section by section

Body sections are H1 and always appear in this order. Subsections are H2. Markdown `####` headings from
the source become `###`.

| Section | Content | Source |
|---|---|---|
| `# Summary` | Bold one-liner `**METHOD path** - Title (Group / Domain)`, then the markdown intro (the text before the first `###`, minus the attribute table). If the OpenAPI `description` shares fewer than 55% of its words with the intro, it is appended under "From the OpenAPI specification:". | markdown intro, OpenAPI `description` |
| `# Endpoint` | Attribute table: Operation ID, HTTP method, URL, Base URL, OAuth scope (linked), ZANALYTICS-ORGID header, Permission required, CONFIG parameter (location and mandatory flag), Request Content-Type, Success response, Rate limit, any other `**Key**` rows from the markdown attribute table, OpenAPI pointer with schema names. | OpenAPI operation + markdown attribute table |
| `# Request` / `## Headers` | Authorization, ZANALYTICS-ORGID (required/optional/not required), extra header params such as ZANALYTICS-DEST-ORGID, Content-Type when CONFIG is a body. | OpenAPI `parameters` (in: header) + markdown ORGID row |
| `## Path Parameters` | One row per `{placeholder}` with the OpenAPI description and a link to `/foundations/identifiers.md#<name>`. | OpenAPI `parameters` (in: path), dereferenced |
| `## CONFIG Parameters` (or the markdown's own heading) | Every markdown `###` block classified as *request*: `CONFIG Parameter(s)`, `URL Parameters`, `FIELDS FOR CONFIG JSON`, `Sample values for CONFIG parameter`, `Query Parameters`, `Request Parameters`, `Request Body`. Verbatim, headings shifted up one level, links rewritten. | markdown |
| `## Other Body Parts` | Non-CONFIG multipart parts (`FILE`, `DATA`). | OpenAPI `requestBody` schema properties |
| `## Notes from the OpenAPI specification` | `x-zenesis-sections.apiRequestParameters / apiRequest / apiInfo` HTML converted to bullets. | OpenAPI |
| `# Response` / `## Success Response` | HTTP 200 with content types, or HTTP 204 no-body text. | OpenAPI `responses` |
| `## Response Fields` | Markdown blocks classified as *response-fields* (`Response Fields`, `Response Field Reference`, `Response Structure`), plus any `#### Response Field Reference` lifted out of a Sample Responses block. | markdown |
| `## Notes from the OpenAPI specification` | `x-zenesis-sections.apiResponseParameters / apiResponseCodes`. | OpenAPI |
| `# Examples` / `## Sample Requests`, `## Sample Responses` | Verbatim markdown blocks. | markdown |
| `## SDK Examples` | Link to the SDK Example concept, listing the languages present. | samples file |
| `# Notes & Behaviour` | Markdown blocks classified as *notes* (`Notes & Behaviour`, `Notes`, `Behaviour`, `Special Cases and Caveats`), then every unrecognised `###` block under its own heading. | markdown |
| `# Error Codes` | Merged table: markdown Error Codes rows first, then OpenAPI `x-zenesis-statuscodes` not already present, then 8535 and 7005 if absent. Each code links to `/foundations/error-codes.md#error-<code>`; HTTP column from observed sample responses or the `DEFAULT_HTTP` table. | markdown + OpenAPI |
| `# Related` | Group overview, domain overview, foundations links, sibling endpoints, SDK examples. | generated |

### API Endpoint frontmatter

```yaml
type: API Endpoint
title: <markdown title>
description: <first sentence of the OpenAPI description, else of the markdown intro>
resource: https://analyticsapi.zoho.com<path template>
tags: [zoho-analytics, rest-api-v2, <domain>, <group>, <method>, <scope families...>]
api:
  operation_id: <OpenAPI operationId, or MD_ONLY_OPS value>
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
  permission_required: <markdown Permission Required text, markdown stripped>
  rate_limit: <text>                                                            # when documented
  error_codes: [ints]
  openapi: { file: /references/openapi/<file>, pointer: "#/paths/<escaped path>/<method>", config_schema: <name>, response_schema: <name> }
  sdk_examples: /sdk-examples/<domain>/<group>/<name>.md                        # when samples exist
sources:
  - { id: openapi-spec, resource: /references/openapi/<file>, title: ..., author: team:zoho-analytics-api-docs, last_modified: <mtime> }
generated: { at: <build time> }
status: stable | deprecated      # deprecated when the OpenAPI operation has deprecated: true
```

Rules enforced on every frontmatter: no `generated.by`; empty lists and null values are dropped;
every `resource` is a bundle-internal path that exists or an `http(s)` URL.

## Naming rules

| Thing | Rule | Example |
|---|---|---|
| Domain directory | `DOMAINS[i][1]` slug | `data-operations` |
| Group directory | slug from `DOMAINS` groups | `async-data-export` |
| Endpoint file | `kebab(operationId)`; acronym-aware: `createAutoMLAnalysis` becomes `create-auto-ml-analysis` | `create-export-job-sql-query.md` |
| SDK example file | same name as the endpoint file, under `/sdk-examples/` | |
| Heading anchors | GitHub style: lower-case, drop punctuation except hyphens, spaces to hyphens | `"White Label / Client Portal Behaviour"` becomes `#white-label--client-portal-behaviour` |
| Error catalog anchors | `#error-<code>` | `/foundations/error-codes.md#error-7301` |
| Identifier anchors | `#<parameter-name>` | `/foundations/identifiers.md#workspace-id` |
| Scope anchors | slug of the scope | `/foundations/oauth-scopes.md#zohoanalyticsdataread` |
