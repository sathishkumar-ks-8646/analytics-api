# 03 - Source document format the generator expects

The generator is a parser with fixed expectations. Content that does not follow these shapes is not
lost, but it lands in the wrong section or is ignored. Check the existing sections in the same file and
copy their shape exactly.

## A. Markdown reference file (`<VERSION>/md/<domain folder>/<GROUP>.md`)

One file per API group. Structure:

```markdown
# Zoho Analytics V2 REST API — <Group name>          <- H1, ignored except as a title hint

<preamble paragraphs>                                 <- becomes the group overview Summary

## What is a "<Thing>"?                               <- optional concept sections: copied to the group overview
## Index                                              <- skipped by the generator
| # | API Name | Method | URL | ...                   <- keep it updated for humans anyway

## 1. <Endpoint Title>                                <- ENDPOINT SECTION, see below
## 2. <Endpoint Title>
...
## Appendix A – Common HTTP Headers                   <- skipped (covered by foundations)
## Appendix B – OAuth Scope Summary                   <- skipped (covered by foundations)
## Appendix C – API-Specific Notes and Behaviours     <- copied to the group overview as "API-Specific Notes and Behaviours"
## Appendix D – General Response Payload Notes        <- copied likewise
```

The generator recognises an endpoint section by the heading regex `^## (\d+)\. (.+)$`. The number
is used to resolve intra-document links such as `(#3-get-export-job-details)`, so keep the numbering
contiguous and update the `## Index` table and any `#N-slug` links when inserting a section.

### A.1 Endpoint section skeleton

```markdown
## 5. Create Widget

One or two paragraphs describing the endpoint.               <- intro -> "# Summary"

> Optional callouts also belong to the intro.

| Attribute | Value |                                          <- ATTRIBUTE TABLE (parsed, then removed from the intro)
|-----------|-------|
| **Method** | POST |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/widgets` |
| **OAuth Scope** | `ZohoAnalytics.modeling.create` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the workspace. |
| **Permission Required** | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Widget permission on the workspace. |
| **Rate Limit** | 20 requests per user per minute (10-minute lockout on breach). |   <- optional

### CONFIG Parameters                                            <- request block (also accepted: "CONFIG Parameter")

CONFIG is **mandatory** for this API.                            <- the words mandatory/optional are read as a fallback

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `widgetName` | String | **Yes** | — | Display name. Max 50 characters. Duplicate names fail with `7104`. |
| `folderId` | Long | No | default folder | Folder to place the widget in. |

#### `mode` Values                                               <- sub-tables use H4; they become H3 in the bundle

| Value | Meaning |
|-------|---------|
| `0` | ... |

### Sample Requests

**Case 1 — Minimal create**

```http
POST /restapi/v2/workspaces/137687000271334001/widgets HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"widgetName":"Sales widget"}
```

### Sample Responses

**HTTP 200 OK — Minimal create (Case 1)**                        <- the "HTTP NNN" in a bold line before a ```json block
```json                                                          <- is how the error catalog learns HTTP statuses
{ "status": "success", "summary": "Create widget", "data": { "widgetId": "137687000006991601" } }
```

**HTTP 403 Forbidden — Caller lacks permission**
```json
{ "status": "failure", "summary": "SECURITY_NOT_PERMITTED", "data": { "errorCode": 7301, "errorMessage": "..." } }
```

### Response Fields                                              <- also accepted: "Response Field Reference" as H3 or as H4 inside Sample Responses

| Field | Type | Description |
|-------|------|-------------|
| `data.widgetId` | String | ID of the new widget. |

### Notes & Behaviour                                            <- also accepted: Notes, Behaviour, Special Cases and Caveats

| Aspect | Detail |
|--------|--------|
| **Not idempotent** | Calling twice with the same name fails with `7104`. |
| **Dependency** | `<workspace-id>` → [Get All Workspace List](WORKSPACE_OPERATIONS_API_DOC_INFO.md#6-get-all-workspace-list). |

### Error Codes

| Code | Reason | Solution |                                    <- header text is free; the first cell must be the numeric code
|------|--------|----------|
| 7104 | `META_OBJECT_NOT_PRESENT` — Folder not found. | Verify `folderId`. |
| 7301 | `SECURITY_NOT_PERMITTED` — Caller lacks Create Widget permission. | Ask a Workspace Admin. |
| 8535 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |
```

### A.2 Parsing rules that matter

| Element | Rule |
|---|---|
| Attribute table | Rows of the form `| **Key** | value |`. Recognised keys: `Method` (also `HTTP Method`, `METHOD`), `URL`, `OAuth Scope` (`OAUTHSCOPE`), `ZANALYTICS-ORGID Header` (`Mandatory Header`), `Permission Required` (`PERMISSION REQUIRED`), `Rate Limit`. Unknown keys are copied into the Endpoint table as extra rows. |
| ORGID header value | Starts with `Mandatory`/`Required` -> `required`; starts with `Optional` -> `optional`; contains `Not required` -> `not-required`. Text after an em dash is shown as the note. |
| URL placeholders | Write `<workspace-id>`; the generator converts to `{workspace-id}` for markdown-only endpoints. OpenAPI paths win when the operation exists. |
| `###` block names | Classified by slug: request blocks (`CONFIG Parameter(s)`, `URL Parameters`, `FIELDS FOR CONFIG JSON`, `Sample values for CONFIG parameter`, `Query Parameters`, `Request Parameters`, `Request Body`), `Sample Request(s)`, `Sample Response(s)`, response-field blocks, notes blocks, `Error Codes`. Anything else is kept under `# Notes & Behaviour` with its own heading. Use these exact names. |
| Error table rows | First cell must be a code (`7104`, `**7104**`, or several: `8085 / 8086`). Second cell reason, third cell solution. A backticked `UPPER_SNAKE` constant at the start of the reason becomes the code's summary constant. |
| HTTP status detection | A bold line containing `HTTP <3 digits>` immediately followed by a ```json block with `"errorCode": N` records status N for that code. Without it the catalog falls back to `DEFAULT_HTTP` or 400. |
| Error codes in prose | Any `` `NNNN` `` (4 to 6 digits) that is a known code becomes a link to the catalog automatically. Do not hand-write catalog links. |
| Links to other endpoints in the same file | `[Title](#N-slug)` where N is the section number. |
| Links to other files | `[Title](<GROUP>_API_DOC_INFO.md#N-slug)` using the legacy name pattern: `VIEW_OPERATIONS_API_DOC_INFO.md`, `COLUMNS_API_DOC_INFO.md`, `ROW_API_DOC_INFO.md`, `ORG_INFO_API_DOC_INFO.md`, `TRASH_API_DOC_INFO.md`, `SLIDESHOW_API_DOC_INFO.md`, `EMBEDURL_API_DOC_INFO.md`, `DOMAIN_AND_WHITELABEL_API_DOC_INFO.md`, `AUTOML_API_DOC_INFO.md`, otherwise `<MD FILE STEM>_API_DOC_INFO.md`. The generator rewrites them to bundle paths and replaces the label if it is the file name. |
| Links to a concept section | `[text](#permission-model)` or `[text](OTHER_API_DOC_INFO.md#permission-model)` resolve to the group overview. `#appendix-a--common-http-headers` and `#appendix-b--oauth-scope-summary` resolve to the foundations. |
| Headings inside blocks | Use `####` for sub-tables inside a `###` block. Never use `##` inside an endpoint section; it starts a new section. |
| Code fences | Use ```http for requests, ```json for bodies. Fences are never touched by the heading shifter or the link rewriter. |
| Case headings | `**Case N — description**` before each sample request; `**HTTP NNN <reason> — description**` before each sample response. |
| Internal names | Never mention Java classes, XML security attributes, template names or file names of the documentation system in prose. |

## B. OpenAPI file (`<VERSION>/zenesis-oas/<domain>-grouped-api.json`)

OpenAPI 3.0 JSON. Fields the generator reads from each operation:

| Field | Used for |
|---|---|
| `x-zenesis-title` (fallback `summary`) | Join key with the markdown title (via `TITLE_MAP` if they differ). |
| `operationId` | Endpoint file name (kebab-case), catalog, SDK doc, manifest. Must be unique across all files. |
| `description` | Frontmatter `description` (first sentence) and, when different enough, an extra Summary paragraph. |
| `tags[0]` | Group description lookup in the file's top-level `tags[]`. |
| `security[].iam-oauth2-schema` | `api.oauth_scopes`, scope docs, permission matrix. |
| `parameters[]` | `$ref` to `#/components/parameters/<name>` or inline. `in: path` rows, `in: header` rows (name `ZANALYTICS-ORGID` is the org header; `required` decides required/optional), `name: CONFIG, in: query` marks a query CONFIG. |
| `requestBody.content.<type>.schema.properties.CONFIG` | Marks a form (`application/x-www-form-urlencoded`) or multipart CONFIG; `required` list decides the flag; other properties become "Other Body Parts". |
| `responses.200|201|204` | Success status, content types, JSON response schema name. |
| `responses.*.x-zenesis-statuscodes[]` | `{name, description, resolution}` error rows merged into the endpoint table and the catalog. |
| `x-zenesis-sections.<apiRequestParameters|apiRequest|apiInfo|apiResponseParameters|apiResponseCodes>.<n>.value` | HTML notes converted to markdown bullets. Supported tags: `ul li b strong code br p blockquote span`. |
| `x-zenesis-security.throttles[0]` | `{duration, threshold, lock-period}` in seconds -> rate limit text. |
| `deprecated: true` | `status: deprecated` in frontmatter. |
| `components.parameters.*` | Descriptions for the identifiers document. |
| `components.schemas.*` | Copied verbatim in `/references/openapi/`; names surface in the Endpoint table. |

Error responses should use `"4XX"` and `"500"` pointing at the common file's `CommonErrorResponse` and
`UnexpectedErrorResponse` (existing files use an absolute GitHub raw URL for that `$ref`; keep the same form).

## C. SDK samples (`<VERSION>/zenesis-oas-samples/<domain>-grouped-api-samples.json`)

```json
{
  "/restapi/v2/workspaces/{workspace-id}/widgets": {
    "post": {
      "Curl":   { "snippets": [ { "code": "curl ..." } ] },
      "C#":     { "snippets": [ { "code": "..." } ] },
      "Go":     { "snippets": [ { "code": "..." } ] },
      "Java":   { "snippets": [ { "code": "..." } ] },
      "Php":    { "snippets": [ { "code": "..." } ] },
      "Python": { "snippets": [ { "code": "..." } ] },
      "Node":   { "snippets": [ { "code": "..." } ] },
      "Ruby":   { "snippets": [ { "code": "..." } ] },
      "Deluge": { "snippets": [ { "code": "..." } ] }
    }
  }
}
```

Keys must match the OpenAPI path template and lower-case method exactly. Language keys must be spelled
as above (`LANG_FENCE` in the builder). More than one snippet per language renders as numbered variants.
An operation with no samples entry simply gets no SDK Example document and no `api.sdk_examples`.

## D. Common file (`<VERSION>/zenesis-oas/common/zoho-analytics-api-common.json`)

`components.securitySchemes.iam-oauth2-schema.flows.authorizationCode.scopes` is the full scope list
(drives `/foundations/oauth-scopes.md`). `components.examples.*` supply summary constants for common
error codes. Copied verbatim to `/references/openapi/zoho-analytics-api-common.json`.
