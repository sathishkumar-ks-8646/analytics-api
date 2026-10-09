---
type: API Endpoint
title: Export Data from a View
description: Use Bulk APIs to export data from the specified view synchronously.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - sync-data-export
  - get
  - data
api:
  operation_id: exportDataView
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data"
  domain: data-operations
  group: sync-data-export
  oauth_scopes:
    - ZohoAnalytics.data.read
  org_id_header: required
  config_parameter:
    location: query
    required: false
  success_status: 200
  response_content_types:
    - text/csv
    - application/json
    - application/xml
    - application/vnd.ms-excel
    - application/pdf
    - text/html
    - image/png
    - image/jpeg
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Export permission on the view."
  error_codes:
    - 7104
    - 7301
    - 7327
    - 7330
    - 7331
    - 7332
    - 7333
    - 7543
    - 7565
    - 7801
    - 7803
    - 7806
    - 7807
    - 7808
    - 7809
    - 7824
    - 7827
    - 7830
    - 8001
    - 8014
    - 8015
    - 8017
    - 8088
    - 8119
    - 8133
    - 8188
    - 8241
    - 8507
    - 8535
    - 8547
  openapi:
    file: "/references/openapi/data-operations-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1data/get"
    config_schema: ExportConfig
    response_schema: null
  sdk_examples: "/sdk-examples/data-operations/sync-data-export/export-data-view.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-operations-grouped-api.json"
    title: OpenAPI 3 specification - data-operations-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data`** - Export Data from a View (Synchronous Data Export / Data Operations).

Exports the data of a view and returns the generated file in the response body.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace that owns the view. |
| `<view-id>` | Long | ID of the view to export. Must belong to `<workspace-id>`, otherwise the call fails. |

Because this is a `GET`, `CONFIG` is passed as a **query parameter** holding a stringified, URL-encoded JSON object:

```
GET /restapi/v2/workspaces/466206000000071000/views/466206000000072000/data?CONFIG=%7B%22responseFormat%22%3A%22csv%22%7D
```

From the OpenAPI specification:

Use Bulk APIs to export data from the specified view synchronously.

Note: Export Data API is restricted for certain resources (given below). For these cases, use the Asynchronous Export APIs instead:

  - Tables having more than one million rows.
  - Tables and Views from live connect workspaces.
  - Dashboard and QueryTable view types.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `exportDataView` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.data.read`](../../../foundations/oauth-scopes.md#zohoanalyticsdataread) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Export permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - optional |
| Success response | HTTP 200 - `text/csv`, `application/json`, `application/xml`, `application/vnd.ms-excel`, `application/pdf`, `text/html`, `image/png`, `image/jpeg` |
| Content-Type | Varies with `responseFormat` — see [Response Structure by Format](#response-structure-by-format) |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1data/get`; CONFIG schema `ExportConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.data.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

See the CONFIG schema in the OpenAPI specification referenced in the Endpoint table.

## Notes from the OpenAPI specification

Export Data API is restricted for the resources given below. For these, use the Asynchronous Export APIs instead.
- Tables having more than one million rows.
- Tables and Views from live connect workspaces.
- Dashboard and Query Table view types.

This is a GET request, so the CONFIG value is sent as a query parameter. The JSONObject must be stringified and URL encoded before it is appended to the request URL.

# Response

## Success Response

HTTP `200` with content type `text/csv`, `application/json`, `application/xml`, `application/vnd.ms-excel`, `application/pdf`, `text/html`, `image/png`, `image/jpeg`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

The success body is a file, not a JSON envelope, so there are structured fields to document only for the JSON and XML formats.

**JSON with `keyValueFormat: true` (the default for `json`)**

| Field | Type | Description |
|-------|------|-------------|
| `data` | Array | One entry per exported row, in export order. Empty when nothing matched `criteria`. |
| `data[].<Column Name>` | String | One key per exported column, named by its **display name** exactly as it appears in the view. Values are strings, including for numeric and date columns. |
| `data[].Row Number` | String | Present only when `includeRowNums` or `includeRowIds` is `true`. A sequential counter starting at `1`, written as the first key of each object. |

**JSON with `keyValueFormat: false`**

| Field | Type | Description |
|-------|------|-------------|
| `response` | Object | Envelope wrapping the whole payload. |
| `response.uri` | String | The request path that produced this export. |
| `response.action` | String | Always `"EXPORT"`. |
| `response.criteria` | String | Echo of the `criteria` that was applied. **Present only when a criteria was sent** — test for the key rather than assuming it. |
| `response.result` | Object | The data itself. |
| `response.result.column_order` | Array of String | Exported column display names, in the order the row arrays follow. When `includeRowNums` is `true`, `"Row Number"` is the first entry. |
| `response.result.rows` | Array of Array | One inner array per row, positionally aligned with `column_order`. All values are strings. |

**XML with `keyValueFormat: false` (the default for `xml`)**

| Element / Attribute | Description |
|---------------------|-------------|
| `<response>` | Root element. |
| `response/@uri` | The request path that produced this export. |
| `response/@action` | Always `EXPORT`. |
| `<result>` | Wrapper around the rows. |
| `<rows>` | Container of `<row>` elements. |
| `<row>` | One exported row. |
| `<column name="…">` | One per exported column. The `name` attribute carries the column display name; the element text carries the value. |

**XML with `keyValueFormat: true`**

| Element | Description |
|---------|-------------|
| `<result>` | Root element. There is **no** XML declaration and **no** `<response>` wrapper in this shape. |
| `<rows>` | Container of `<row>` elements. |
| `<row>` | One exported row. |
| `<ColumnName>` | One element per column, **named after the column itself**. Column names containing characters that are not valid in an XML element name make this shape unusable — prefer `keyValueFormat: false` for such views. |

**Response headers**

| Header | Description |
|--------|-------------|
| `Content-Type` | The only header that describes the payload. Set from `responseFormat`, or to `application/zip` when `password` wraps the file — see [Response Structure by Format](#response-structure-by-format). |
| `Content-Disposition` | **Not sent.** This API returns no filename suggestion, so the client must name the downloaded file itself. |

# Examples

## Sample Requests

For readability the `CONFIG` values below are shown as plain JSON. On the wire each must be stringified and URL-encoded, as in [Request conventions](../../../foundations/request-conventions.md).

**Case 1 — `criteria` alone: export only the rows that match a filter**

```http
GET /restapi/v2/workspaces/466206000000071000/views/466206000000072000/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

```json
{
  "responseFormat": "csv",
  "criteria": "\"SalesTable\".\"Region\"='East'"
}
```

The response is a CSV containing only the East-region rows. Every other attribute takes its default: comma-separated, DOS line endings, header row present, hidden columns included, personal-data columns excluded.

**Case 2 — a fully configured CSV export**

Covers column selection, the three CSV delimiter attributes, the row-number column, and password protection in one call.

```http
GET /restapi/v2/workspaces/466206000000071000/views/466206000000072000/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

```json
{
  "responseFormat": "csv",
  "selectedColumns": ["Region", "Product", "Sales"],
  "delimiter": 1,
  "recordDelimiter": 1,
  "quoted": 1,
  "includeHeader": true,
  "includeRowNums": true,
  "showHiddenCols": false,
  "showPersonalCols": false,
  "password": "Zoho@123"
}
```

Because `password` is present, the body is a **ZIP archive** containing the tab-separated file, and `Content-Type` is `application/zip`.

**Case 3 — a fully configured PDF export**

Covers paper setup, all four margins, title and description placement, column sizing, language, and the header/footer slots.

```http
GET /restapi/v2/workspaces/466206000000071000/views/466206000000073000/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

```json
{
  "responseFormat": "pdf",
  "paperSize": 4,
  "paperStyle": "Landscape",
  "topMargin": 0.5,
  "bottomMargin": 0.5,
  "leftMargin": 0.25,
  "rightMargin": 0.25,
  "showTitle": 0,
  "showDesc": 2,
  "columnWidthRatio": 2,
  "exportLanguage": 0,
  "leftHeader": 1,
  "centerHeader": 0,
  "rightHeader": 2,
  "leftFooter": 5,
  "leftFooterText": "Confidential — Internal Use Only",
  "centerFooter": 4,
  "rightFooter": 0,
  "includeHeader": true
}
```

**Case 4 — JSON and XML with the two record shapes**

```json
{
  "responseFormat": "json",
  "keyValueFormat": true,
  "includeRowNums": false,
  "showHiddenCols": false
}
```

```json
{
  "responseFormat": "xml",
  "keyValueFormat": false,
  "selectedColumns": ["Region", "Sales"]
}
```

**Case 5 — a chart as an image**

```json
{
  "responseFormat": "image",
  "imageFormat": "png",
  "width": 1200,
  "height": 800,
  "title": true,
  "description": false,
  "legend": true
}
```

## Sample Responses

**HTTP 200 OK — `responseFormat: "csv"`**

```
Content-Type: text/csv

Region,Product,Sales
East,Laptop,145000
East,Monitor,38200
East,Keyboard,4750
```

**HTTP 200 OK — `responseFormat: "json"`, `keyValueFormat: true` (the default)**

```json
{
  "data": [
    {
      "Region": "East",
      "Product": "Laptop",
      "Sales": "145000"
    },
    {
      "Region": "East",
      "Product": "Monitor",
      "Sales": "38200"
    }
  ]
}
```

**HTTP 200 OK — `responseFormat: "json"`, `keyValueFormat: false`**

```json
{
  "response": {
    "uri": "/restapi/v2/workspaces/466206000000071000/views/466206000000072000/data",
    "action": "EXPORT",
    "criteria": "\"SalesTable\".\"Region\"='East'",
    "result": {
      "column_order": ["Region", "Product", "Sales"],
      "rows": [
        ["East", "Laptop", "145000"],
        ["East", "Monitor", "38200"]
      ]
    }
  }
}
```

**HTTP 200 OK — `responseFormat: "xml"`, `keyValueFormat: false` (the default)**

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<response uri="/restapi/v2/workspaces/466206000000071000/views/466206000000072000/data" action="EXPORT">
<result>
<rows>
<row>
<column name="Region">East</column>
<column name="Product">Laptop</column>
<column name="Sales">145000</column>
</row>
</rows>
</result>
</response>
```

**HTTP 200 OK — `responseFormat: "xml"`, `keyValueFormat: true`**

```xml
<result>
<rows>
<row>
<Region>East</Region>
<Product>Laptop</Product>
<Sales>145000</Sales>
</row>
</rows>
</result>
```

**HTTP 200 OK — `responseFormat: "csv"` with `includeRowNums: true`**

```
Row Number,Region,Product,Sales
1,East,Laptop,145000
2,East,Monitor,38200
```

**HTTP 200 OK — binary formats**

`xls`, `pdf`, and `image` return raw binary. Only the headers are meaningful to read:

```
Content-Type: application/pdf

%PDF-1.4
… binary …
```

**HTTP 400 Bad Request — the view cannot be exported synchronously**

```json
{
  "status": "failure",
  "summary": "SYNC_EXPORT_NOT_ALLOWED",
  "data": {
    "errorCode": 8133,
    "errorMessage": "This view cannot be exported synchronously. Use the asynchronous export API instead."
  }
}
```

**HTTP 400 Bad Request — a name in `selectedColumns` does not exist**

```json
{
  "status": "failure",
  "summary": "API_EXPORT_COLUMN_NOT_PRESENT",
  "data": {
    "errorCode": 8015,
    "errorMessage": "The column Revenue is not present in this view."
  }
}
```

**HTTP 400 Bad Request — `image` requested for a non-chart view**

```json
{
  "status": "failure",
  "summary": "API_IMAGE_RESPONSE_NOT_POSSIBLE",
  "data": {
    "errorCode": 8014,
    "errorMessage": "Image response is possible only for chart views."
  }
}
```

**HTTP 403 Forbidden — the caller lacks Export permission**

```json
{
  "status": "failure",
  "summary": "SECURITY_NOT_PERMITTED",
  "data": {
    "errorCode": 7301,
    "errorMessage": "You do not have the permission to perform this operation."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Export Data from a View](../../../sdk-examples/data-operations/sync-data-export/export-data-view.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **`CONFIG` is optional** | A bare `GET .../data` with no query string exports the entire view as CSV, comma-separated, with a header row, hidden columns included, and personal-data columns excluded. |
| **`responseFormat` is optional too** | Sending a `CONFIG` without `responseFormat` yields CSV. |
| **The response body is the file, not a wrapper** | Unlike every other API in this suite, a successful call returns no `status` / `summary` / `data` envelope. Only **failures** use the JSON envelope. A client must therefore branch on the HTTP status before attempting to parse the body as JSON. |
| **Restriction checks run before CONFIG validation** | A dashboard exported as `csv` fails with `8133`, not with a format error, because the view-type gate is evaluated first. |
| **An empty result is a success** | A `criteria` that matches nothing returns `200` with a header-only CSV, or `{"data":[]}`, or an empty `<rows/>`. It is not an error. |
| **All exported values are strings** | In both JSON shapes, numbers, dates, and currency values come back quoted, formatted per the column's display settings rather than as raw storage values. |
| **`includeRowIds` and `includeRowNums` are the same switch** | Sending either enables the leading `Row Number` field. Sending both is harmless. |
| **`showHiddenCols` defaults differ by format** | `true` for `csv`, `json`, `xml`, `xls`, and `pdf`; `false` for `html`. Set it explicitly when the same integration produces more than one format. |
| **`columnWidthRatio` defaults differ by format** | `1` for `pdf`, `2` for `html`. Same value set, different default. |
| **`selectedColumns` overrides `showHiddenCols` for the columns it names** | A hidden column listed in `selectedColumns` is exported even when `showHiddenCols` is `false`. |
| **`selectedColumns` also sets the column order** | Columns come out in the order listed, not in the view's own order. |
| **`password` shorter than 6 characters is rejected outright** | `8188` fires during validation, before any data is read. |
| **The whole export is atomic from the caller's point of view** | Because validation happens up front and the file is streamed afterwards, a validation failure yields a clean JSON error and no partial file. A size limit tripped mid-stream (`7830`) resets the buffer and returns the error instead. |
| **Personal-data handling is role-dependent** | For a non-administering caller, `showPersonalCols` is ignored and personal columns are included. Do not rely on this attribute as a redaction mechanism for shared users — see [Permission Model](overview.md#permission-model). |
| **Dashboard-only page-setup attributes are silently ignored** | `generateTOC`, `dashboardLayout`, and `zoomFactor` describe multi-view dashboard PDFs, which this API cannot produce. |
| **Dependency chain:** | [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>`; [Get Columns](../../data-modeling-and-schema/columns/overview.md) → `selectedColumns` names → Export Data from a View → the file. |

## CONFIG Parameters — Common to Every Format

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `responseFormat` | String | No | `"csv"` | Output format. One of `csv`, `json`, `xml`, `xls`, `pdf`, `html`, `image` (case-insensitive). Any other value fails with `8001`. |
| `criteria` | String | No | — | Filter expression selecting the rows to export. Omit to export every row. See [`criteria` Syntax](overview.md#criteria-syntax). |
| `password` | String | No | — | Protects the exported file with a password. Minimum 6 characters, maximum 256; shorter values fail with `8188`. Changes the delivery format — see [Password Protection](#password-protection). |
| `selectedColumns` | JSONArray of String | No | — | Column **display names** to export, in the order given, 1–300 entries. Only honoured for tables and tabular views. An unmatched name fails with `8015`. Omit to export all eligible columns. |
| `showHiddenCols` | Boolean | No | `true` (`false` for `html`) | Whether columns hidden in the view are included. A column named explicitly in `selectedColumns` is always included, hidden or not. |
| `showPersonalCols` | Boolean | No | `false` | Whether columns marked as personal data are included. Honoured only for Account Admins, Organization Admins, and Workspace Admins — see [Permission Model](overview.md#permission-model). |
| `includeHeader` | Boolean | No | `true` | Whether a header row of column names is written. Applies to `csv`, `xls`, `pdf`, and `html`. |
| `includeRowNums` | Boolean | No | `false` | Prefixes each record with a sequential `Row Number` value. |
| `includeRowIds` | Boolean | No | `false` | Equivalent to `includeRowNums` — both feed the same switch, so sending either one enables the row-number column. |
| `applyDefaultUF` | Boolean | No | `false` | Applies the view's saved default user filters before exporting. Meaningful for tabular views. |
| `validateSystemTags` | Boolean | No | `true` | When `true`, the request is rejected with `8241` if the view carries a restricted **DATA_WARNING** system tag — applied directly, or inherited through lineage from a parent data source or table. Send `false` to acknowledge the warning and proceed. Only relevant when System Tags are enabled for the organization. |

## CONFIG Parameters — CSV Specific

Applicable when `responseFormat` is `csv`.

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `delimiter` | Integer | No | `0` (comma) | Field separator. `0` Comma, `1` Tab, `2` Semicolon, `3` Space, `4` Pipe. Any other value fails with `8119`. |
| `recordDelimiter` | Integer | No | `0` (DOS) | Line ending. `0` DOS (`\r\n`), `1` UNIX (`\n`), `2` MAC (`\r`). Any other value fails with `8119`. |
| `quoted` | Integer | No | — | Text qualifier wrapped around values. `0` single quote, `1` double quote. Omit for no qualifier. Any other value fails with `8119`. |

## CONFIG Parameters — JSON and XML Specific

Applicable when `responseFormat` is `json` or `xml`.

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `keyValueFormat` | Boolean | No | `true` for `json`, `false` for `xml` | Chooses the record shape. `true` emits each row as column-name/value pairs; `false` emits a wrapped envelope with a separate column list and rows as positional arrays. The two shapes are structurally different — see [Response Structure by Format](#response-structure-by-format). |

## CONFIG Parameters — PDF Specific

Applicable when `responseFormat` is `pdf`.

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `paperSize` | Integer | No | `4` (A4) | `0` Letter, `1` Legal, `2` Tabloid, `3` A3, `4` A4, `5` Auto-fit width. Outside `0`–`5` fails with `8119`. |
| `paperStyle` | String | No | `"Portrait"` | `"Portrait"` or `"Landscape"` (case-insensitive). Anything else fails with `8119`. |
| `topMargin` | Float | No | `0.25` | Top margin in inches, `0`–`1` inclusive. Outside that range fails with `7801`. |
| `bottomMargin` | Float | No | `0.25` | Bottom margin in inches, `0`–`1`. |
| `leftMargin` | Float | No | `0.25` | Left margin in inches, `0`–`1`. |
| `rightMargin` | Float | No | `0.25` | Right margin in inches, `0`–`1`. |
| `showTitle` | Integer | No | `0` (top) | Where the view title is placed. `0` Top, `1` Bottom, `2` Do not include. Outside `0`–`2` fails with `8119`. |
| `showDesc` | Integer | No | `0` (top) | Where the view description is placed. `0` Top, `1` Bottom, `2` Do not include. |
| `columnWidthRatio` | Integer | No | `1` | Column sizing. `0` proportional to the widths set in the view, `1` sized to content, `2` all columns equal. Outside `0`–`2` fails with `8119`. |
| `exportLanguage` | Integer | No | `0` (English) | Font set used for rendering text. `0` English, `1` Chinese, `2` Japanese, `3` European, `4` Korean. Pick the one matching your data, otherwise non-Latin characters may not render. |
| `leftHeader` | Integer | No | `1` (Title) | Content of the top-left page-header slot. See [Header and Footer Slot Values](#header-and-footer-slot-values). |
| `centerHeader` | Integer | No | `0` (Blank) | Content of the top-centre page-header slot. |
| `rightHeader` | Integer | No | `2` (Date) | Content of the top-right page-header slot. |
| `leftFooter` | Integer | No | `0` (Blank) | Content of the bottom-left page-footer slot. |
| `centerFooter` | Integer | No | `3` (Page number) | Content of the bottom-centre page-footer slot. |
| `rightFooter` | Integer | No | `0` (Blank) | Content of the bottom-right page-footer slot. |
| `leftHeaderText` | String | No | — | Custom text for the top-left slot. Read only when `leftHeader` is `5`. |
| `centerHeaderText` | String | No | — | Custom text for the top-centre slot. Read only when `centerHeader` is `5`. |
| `rightHeaderText` | String | No | — | Custom text for the top-right slot. Read only when `rightHeader` is `5`. |
| `leftFooterText` | String | No | — | Custom text for the bottom-left slot. Read only when `leftFooter` is `5`. |
| `centerFooterText` | String | No | — | Custom text for the bottom-centre slot. Read only when `centerFooter` is `5`. |
| `rightFooterText` | String | No | — | Custom text for the bottom-right slot. Read only when `rightFooter` is `5`. |

### Header and Footer Slot Values

The same six values apply to every one of the six slots.

| Value | Content placed in the slot |
|-------|----------------------------|
| `0` | Blank |
| `1` | View title |
| `2` | Export date |
| `3` | Page number |
| `4` | Page number with total (`3 of 12`) |
| `5` | The custom text from the matching `…Text` attribute |
| `6` | Logo |

Any other value fails with [`8119`](../../../foundations/error-codes.md#error-8119). When a slot is set to `1`, the view's own title is substituted and the matching `…Text` attribute is ignored.

## CONFIG Parameters — HTML Specific

Applicable when `responseFormat` is `html`.

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `includeTitle` | Integer | No | `0` (top) | Where the view title is placed. `0` Top, `1` Bottom, `2` Do not include. Outside `0`–`2` fails with `8119`. |
| `includeDesc` | Integer | No | `0` (top) | Where the view description is placed. `0` Top, `1` Bottom, `2` Do not include. |
| `columnWidthRatio` | Integer | No | `2` | Column sizing. `0` proportional to the widths set in the view, `1` sized to content, `2` all columns equal. Note the default differs from PDF. |

## CONFIG Parameters — Image Specific

Applicable when `responseFormat` is `image`. Valid **only for chart views**; any other view type fails with [`8014`](../../../foundations/error-codes.md#error-8014).

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `imageFormat` | String | No | `"png"` | `"png"`, `"jpg"`, or `"jpeg"` (case-insensitive). Anything else fails with `8017`. |
| `width` | Integer | No | `500` | Image width in pixels, `250`–`2000`. Outside that range fails with `7803`. |
| `height` | Integer | No | `400` | Image height in pixels, `200`–`2000`. Outside that range fails with `7803`. |
| `title` | Boolean | No | `false` | Whether the chart title is drawn on the image. |
| `description` | Boolean | No | `false` | Whether the chart description is drawn on the image. |
| `legend` | Boolean | No | `true` | Whether the chart legend is drawn on the image. |

## CONFIG Parameters — XLS

`xls` takes no format-specific attributes. It uses the common set: `selectedColumns`, `includeHeader`, `showHiddenCols`, `showPersonalCols`, `includeRowNums`, `criteria`, and `password`.

## Password Protection

Sending `password` changes **how** the file is delivered, not only whether it is locked:

| `responseFormat` | Result when `password` is sent |
|------------------|--------------------------------|
| `csv`, `json`, `xml`, `html`, `image` | The file is placed inside a **password-protected ZIP archive**. The response `Content-Type` becomes `application/zip`. |
| `xls` | The workbook itself is encrypted. `Content-Type` stays `application/vnd.ms-excel`. |
| `pdf` | The PDF itself is encrypted, with printing and copying permitted. `Content-Type` stays `application/pdf`. |

A client that always writes the body to `export.csv` will therefore write a ZIP archive under a `.csv` name as soon as a password is added. Branch on the response `Content-Type`.

## Response Structure by Format

| `responseFormat` | `Content-Type` | Body |
|------------------|----------------|------|
| `csv` | `text/csv` | Delimited text. Optional header row, optional leading `Row Number` field. |
| `json` (`keyValueFormat: true`) | `application/json` | `{"data":[ {…}, … ]}` — one object per row, keyed by column display name. |
| `json` (`keyValueFormat: false`) | `application/json` | `{"response":{"uri":…,"action":"EXPORT","result":{"column_order":[…],"rows":[[…]]}}}` |
| `xml` (`keyValueFormat: false`) | `application/xml` | `<?xml …?><response …><result><rows><row><column name="…">…</column></row></rows></result></response>` |
| `xml` (`keyValueFormat: true`) | `application/xml` | `<result><rows><row><ColumnName>…</ColumnName></row></rows></result>` — no XML declaration and no `<response>` wrapper. |
| `xls` | `application/vnd.ms-excel` | Binary workbook. |
| `pdf` | `application/pdf` | Binary PDF. |
| `html` | `text/html` | An HTML fragment containing the rendered table. |
| `image` | `image/png` or `image/jpeg` | Binary image. |
| any of the above **with `password`** | `application/zip`, or the native type for `xls` and `pdf` | See [Password Protection](#password-protection). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — The view does not exist. | Verify `<view-id>` with [Get View List](../../views-management/view-operations/get-views.md). |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller lacks Export permission on the view, or the view does not belong to `<workspace-id>`. | Ensure the caller is an Account Admin, Organization Admin, Workspace Admin, or View Owner, or holds Export permission on the view. |
| [7327](../../../foundations/error-codes.md#error-7327) | 400 | `FILTER_CRITERIA_INVALID` — `criteria` parsed but could not be converted into a query. | Simplify the expression and check operator and value types. |
| [7330](../../../foundations/error-codes.md#error-7330) | 400 | `UNKNOWN_COLUMN_IN_FILTERCRITERIA` — A column named in `criteria` does not exist in the view. | Check the name against [Get Columns](../../data-modeling-and-schema/columns/overview.md). |
| [7331](../../../foundations/error-codes.md#error-7331) | 400 | `FILTERCRITERIA_PARSE_ERROR` — `criteria` is syntactically malformed. | Check quoting: double quotes around column names, single quotes around string literals. |
| [7332](../../../foundations/error-codes.md#error-7332) | 400 | `UNKNOWN_TABLE_IN_FILTERCRITERIA` — A table qualifier in `criteria` is not part of the view. | Qualify columns only with tables the view actually uses. |
| [7333](../../../foundations/error-codes.md#error-7333) | 400 | `INVALID_GROUP_FUNC_USE_IN_FILTERCRITERIA` — An aggregate function was used in `criteria`. | Remove `sum`, `avg`, `count`, and similar functions; filter on raw column values instead. |
| [7543](../../../foundations/error-codes.md#error-7543) | 400 | `ONLY_BASETABLE_COL_IN_TABULAR_FILTERCRITERIA` — `criteria` on a tabular view referenced a column outside its base table. | Filter using only the base table's own columns. |
| [7565](../../../foundations/error-codes.md#error-7565) | 400 | `UNVERIFIED_EMAIL` — The calling user's primary email address is not verified. | Verify the account's primary email address and retry. |
| [7801](../../../foundations/error-codes.md#error-7801) | 400 | `MARGIN_VALUE_EXCEEDS` — A PDF margin is outside `0`–`1` inches. | Send a value between `0` and `1`. |
| [7803](../../../foundations/error-codes.md#error-7803) | 400 | `INVALID_DIMENSION` — `width` or `height` is outside the permitted image range. | Use `width` 250–2000 and `height` 200–2000. |
| [7806](../../../foundations/error-codes.md#error-7806) | 400 | `XLS_CELL_LIMIT_EXCEEDS` — The XLS export exceeds the per-sheet cell limit. | Narrow the export with `criteria` or `selectedColumns`, or export as CSV. |
| [7807](../../../foundations/error-codes.md#error-7807) | 400 | `XLS_COL_LIMIT_EXCEEDS` — More than 256 columns were requested for an XLS export. | Reduce the column count with `selectedColumns`, or export as CSV. |
| [7808](../../../foundations/error-codes.md#error-7808) | 400 | `XLS_CELL_CHAR_LIMIT_EXCEEDS` — A single cell exceeds 32,767 characters. | Exclude the offending column, or export as CSV. |
| [7809](../../../foundations/error-codes.md#error-7809) | 400 | `XLS_NO_DATA` — The XLS export produced no data. | Widen or remove `criteria`. |
| [7824](../../../foundations/error-codes.md#error-7824) | 400 | `EXPORT_REQ_BLOCKED` — Export has been blocked for this workspace. | Contact Zoho Analytics support using the address in the error message. |
| [7827](../../../foundations/error-codes.md#error-7827) | 400 | `EXP_PDF_RECORD_LIMIT` — The PDF exceeds 1,000,000 cells (visible columns × rows). | Narrow the export with `criteria` or `selectedColumns`, or choose a non-paginated format. |
| [7830](../../../foundations/error-codes.md#error-7830) | 400 | `EXP_ALL_RECORD_LIMIT` — The exported payload exceeds 100 MB. | Split the export with `criteria`, or use the asynchronous export. |
| [8001](../../../foundations/error-codes.md#error-8001) | 400 | `INVALID_RESP_FORMAT` — `responseFormat` is not a supported value. | Send one of `csv`, `json`, `xml`, `xls`, `pdf`, `html`, `image`. |
| [8014](../../../foundations/error-codes.md#error-8014) | 400 | `API_IMAGE_RESPONSE_NOT_POSSIBLE` — `image` was requested for a view that is not a chart. | Export charts as images; use `pdf` or `html` for tables and reports. |
| [8015](../../../foundations/error-codes.md#error-8015) | 400 | `API_EXPORT_COLUMN_NOT_PRESENT` — A name in `selectedColumns` does not match any column in the view. | Check the display names with [Get Columns](../../data-modeling-and-schema/columns/overview.md). |
| [8017](../../../foundations/error-codes.md#error-8017) | 400 | `INVALID_IMAGE_FORMAT` — `imageFormat` is not `png`, `jpg`, or `jpeg`. | Send one of the three supported values. |
| [8088](../../../foundations/error-codes.md#error-8088) | 400 | `SECURITY_CONTROLS_FEATURE_DISABLED` — Export has been disabled for the organization by an administrator. | Ask an Organization Admin to re-enable export in the organization's security controls. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE` — A numeric or enumerated attribute is outside its permitted set. The message names the attribute and the accepted values. | Correct the value; see [Enum Reference](overview.md#enum-reference). |
| [8133](../../../foundations/error-codes.md#error-8133) | 400 | `SYNC_EXPORT_NOT_ALLOWED` — The view is a dashboard, a query table, a live-connect view, or a table above the row limit. | Use the asynchronous export API for this view. |
| [8188](../../../foundations/error-codes.md#error-8188) | 400 | `EXPORT_INVALID_PASSWORD` — `password` is empty, blank, or shorter than 6 characters. | Send a password of 6–256 characters. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | `SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION` — The view carries a restricted DATA_WARNING system tag. | Review the warning, then resend with `"validateSystemTags": false`. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | `MORE_THAN_MAX_LENGTH` — `CONFIG` exceeds 100,000 characters. | Shorten `criteria` or `selectedColumns`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.data.read`. |
| [8547](../../../foundations/error-codes.md#error-8547) | 400 | `ARRAY_SIZE_OUT_OF_RANGE` — `selectedColumns` is empty or holds more than 300 entries. | Send between 1 and 300 column names, or omit the attribute. |

# Related

- [Synchronous Data Export overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- [SDK examples](../../../sdk-examples/data-operations/sync-data-export/export-data-view.md).
