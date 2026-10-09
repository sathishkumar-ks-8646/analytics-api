---
type: API Endpoint
title: Import Data into a New Table (Synchronous)
description: "Creates a new table in the workspace from the uploaded data and returns the new table's ID along with the import result."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/data"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - sync-data-import
  - post
  - data
api:
  operation_id: importDataNewTable
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/data"
  domain: data-operations
  group: sync-data-import
  oauth_scopes:
    - ZohoAnalytics.data.create
  org_id_header: required
  config_parameter:
    location: multipart
    required: true
  request_content_type: multipart/form-data
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Table permission on the workspace."
  error_codes:
    - 7092
    - 7111
    - 7208
    - 7232
    - 7248
    - 7301
    - 7478
    - 7512
    - 8046
    - 8079
    - 8119
    - 8139
    - 8148
    - 8149
    - 8504
    - 8516
    - 8535
  openapi:
    file: "/references/openapi/data-operations-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1data/post"
    config_schema: ImportConfigNewTable
    response_schema: ImportSuccessResponse
  sdk_examples: "/sdk-examples/data-operations/sync-data-import/import-data-new-table.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-operations-grouped-api.json"
    title: OpenAPI 3 specification - data-operations-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/data`** - Import Data into a New Table (Synchronous) (Synchronous Data Import / Data Operations).

Creates a new table in the workspace from the uploaded data and returns the new table's ID along with the import result.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `importDataNewTable` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/data` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.data.create`](../../../foundations/oauth-scopes.md#zohoanalyticsdatacreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Table permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` part of a `multipart/form-data` body - **mandatory** |
| Request Content-Type | `multipart/form-data` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1data/post`; CONFIG schema `ImportConfigNewTable`; response schema `ImportSuccessResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.data.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `multipart/form-data; boundary=...` | Required | CONFIG and the payload (FILE or DATA) are sent as form parts. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

CONFIG is **mandatory**. The three attributes at the top of the table are required; everything below is optional.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `tableName` | String | **Yes** | — | Name of the table to create. Must be **unused in the workspace** (`7111` otherwise). |
| `fileType` | String (enum) | **Yes** | — | Format of the payload. See [`fileType` Values](#filetype-values). |
| `autoIdentify` | Boolean | **Yes** | — | When `true`, Zoho Analytics detects the CSV delimiter, quote character, and column data types itself. When `false`, `delimiter` and `quoted` become **mandatory**. See [`autoIdentify` and CSV Parsing](#autoidentify-and-csv-parsing). |
| `onError` | String (enum) | No | `ABORT` | What to do when a value cannot be parsed into its column's data type. See [`onError` Values](#onerror-values). |
| `selectedColumns` | JSONArray of String | No | all columns | Import only these columns from the source. 1–300 entries. |
| `skipTop` | Integer | No | `0` | Number of leading rows to ignore before the header row. |
| `delimiter` | Integer (enum) | Conditional | `0` | CSV field separator. **Mandatory when `autoIdentify` is `false`** and `fileType` is CSV. Values `0`–`4`; anything else fails with `8119`. |
| `quoted` | Integer (enum) | Conditional | `2` | CSV quote character. **Mandatory when `autoIdentify` is `false`** and `fileType` is CSV. Values `0`–`2`. |
| `commentChar` | String | No | none | Lines beginning with this character are ignored. CSV only. |
| `thousandSeparator` | Integer (enum) | No | auto | Grouping separator used in numeric values. See [Number Separator Values](#number-separator-values). |
| `decimalSeparator` | Integer (enum) | No | auto | Decimal separator used in numeric values. See [Number Separator Values](#number-separator-values). |
| `columnSeparators` | JSONObject | No | — | Per-column separator overrides — column name → `[thousandSeparator, decimalSeparator]`, both as strings. The array must have at least two entries (`8149`), and the two separators must differ (`8148`). |
| `dateFormat` | String | No | auto | Default date pattern for all date columns, e.g. `dd-MMM-yyyy`. An unparseable pattern fails with `7512`. |
| `columnDateFormat` | JSONObject | No | — | Per-column date pattern overrides — column name → pattern. 1–300 entries. Takes precedence over `dateFormat`. |
| `columnTimeFormat` | JSONObject | No | — | Per-column time pattern overrides. An invalid pattern is rejected. |
| `columnDurationFormat` | JSONObject | No | — | Per-column duration pattern overrides. An invalid pattern is rejected. |
| `columnDataTypes` | JSONArray | No | auto-detected | Explicit data types for columns instead of letting Zoho Analytics infer them. Up to 500 entries. See [`columnDataTypes` Fields](#columndatatypes-fields). |
| `matchNulls` | Boolean | No | `false` | Treat empty values in the source as nulls when matching. |
| `updateNullForNegativeValues` | Boolean | No | `false` | Store a null instead of the value when a negative number is found in a column that does not accept one. |
| `retainColumnNames` | Boolean | No | `false` | For JSON/XML imports, keep the source's original key names as column names instead of normalising them. |
| `importHiddenRows` | Boolean | No | `false` | For Excel sources, include rows hidden in the sheet. |
| `importHiddenColumns` | Boolean | No | `false` | For Excel sources, include columns hidden in the sheet. |

> `matchingColumns` is **not** used by this API — there are no existing rows to match against.

### `fileType` Values

`CSV`, `JSON`, `XML`, `XLS`, `XLSX`, `PARQUET`, `GEOMETRY`. Case-insensitive.

> The parsing attributes `delimiter`, `quoted`, and `commentChar` apply to **CSV only** and are ignored for every other type.

### `autoIdentify` and CSV Parsing

| `autoIdentify` | Effect |
|----------------|--------|
| `true` | Zoho Analytics detects the delimiter, quote character, and each column's data type from the content. `delimiter` and `quoted` become optional overrides. |
| `false` | Nothing is inferred. `delimiter` and `quoted` are **mandatory** for CSV — omitting either fails with `8079`. |

### `onError` Values

| Value | Behaviour | Effect on the response |
|-------|-----------|------------------------|
| `ABORT` | **Default.** The whole import is rolled back on the first unparseable value. | The call **fails** with `7232`, and `errorMessage` carries the per-line detail. Nothing is imported. |
| `SKIPROW` | The offending row is skipped; the rest are imported. | HTTP 200. `successRowCount` is lower than `totalRowCount`; skipped lines are listed in `importErrors`. |
| `SETCOLUMNEMPTY` | The offending value is stored as empty; the rest of the row is imported. | HTTP 200. `warnings` is incremented and the reset values are listed in `importErrors`. |

### Number Separator Values

| `thousandSeparator` | Character | | `decimalSeparator` | Character |
|--------------------:|-----------|---|-------------------:|-----------|
| `0` | Comma `,` | | `0` | Dot `.` |
| `1` | Dot `.` | | `1` | Comma `,` |
| `2` | Space | | | |
| `3` | Single quote `'` | | | |
| `4` | None | | | |

> The thousand and decimal separators must resolve to **different** characters, otherwise the import fails with [`8148`](../../../foundations/error-codes.md#error-8148).

### `columnDataTypes` Fields

A JSONArray of objects, one per column whose type you want to fix explicitly:

| Field | Type | Mandatory | Description |
|-------|------|-----------|--------------|
| `columnName` | String | **Yes** | Name of the column in the source data. |
| `dataType` | String | **Yes** | The Zoho Analytics data type to assign, e.g. `PLAIN`, `NUMBER`, `DECIMAL_NUMBER`, `CURRENCY`, `DATE`, `EMAIL`, `URL`. |
| `geoRole` | String | No | Geographic role, when `dataType` is a geo type. |

## Other Body Parts

| Part | Type | Description |
|---|---|---|
| `FILE` | string (binary) | The file to be imported. Maximum allowed file size is 20 MB. Send either FILE or DATA, not both. |
| `DATA` | string | The raw string to be imported, in the format declared by fileType in CONFIG. Send either FILE or DATA, not both. |

## Notes from the OpenAPI specification

The CSV specific attributes - commentChar, delimiter and quoted - are mandatory if autoIdentify is set to false.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Import data"` for both import APIs. |
| `data` | JSONObject | Response payload wrapper. |
| `data.viewId` | String | ID of the **newly created table**, as a string. **Returned only by this API** — the existing-table import omits it. This is the `<view-id>` for every follow-up call. |
| `data.importSummary` | JSONObject | Counts describing what was loaded. |
| `importSummary.importType` | String | Always `"APPEND"` for a new-table import — the table was empty, so the data was simply added. |
| `importSummary.totalColumnCount` | Number | Columns found in the source data. |
| `importSummary.selectedColumnCount` | Number | Columns actually imported. Lower than `totalColumnCount` when `selectedColumns` was used. |
| `importSummary.totalRowCount` | Number | Data rows found in the source. |
| `importSummary.successRowCount` | Number | Rows actually written. Lower than `totalRowCount` when `onError: "SKIPROW"` dropped rows. |
| `importSummary.warnings` | Number | Count of values that were reset or flagged — driven mainly by `onError: "SETCOLUMNEMPTY"` and by soft validation failures such as an unrecognised geo value. |
| `importSummary.importOperation` | String | `"created"` for this API (a new table was created); `"updated"` for the existing-table import. |
| `data.columnDetails` | JSONObject | Column name → **assigned data type**, as a display label (`"Plain Text"`, `"Number"`, `"Positive Number"`, `"Decimal Number"`, `"Currency"`, `"Percentage"`, `"Date"`, `"E-Mail"`, `"URL"`, `"Geo Column"`, …). This is how you confirm what Zoho Analytics inferred when `autoIdentify` was `true`. |
| `data.importErrors` | String | Per-line warnings and resets as an **HTML fragment** (`<nobr>[Line: 6 Field:  4] (andhara pradesh) -WARNING: Invalid GEO LOCATION</NOBR><br>…`). **Always present**; an empty string `""` when the import was completely clean. Not machine-readable — display it or log it rather than parsing it. |

# Examples

## Sample Requests

**Case 1 — Auto-identified CSV upload, minimal configuration**

```http
POST /restapi/v2/workspaces/466206000000071000/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: multipart/form-data; boundary=----ZohoBoundary

------ZohoBoundary
Content-Disposition: form-data; name="CONFIG"

{
    "tableName": "SalesData",
    "fileType": "CSV",
    "autoIdentify": true
}
------ZohoBoundary
Content-Disposition: form-data; name="FILE"; filename="sales.csv"
Content-Type: text/csv

Date,Region,Product,Sales,Cost
12 April 2020,West,Fruits and Vegetables,3928.38,200.05
------ZohoBoundary--
```

**Case 2 — Explicit CSV parsing options clubbed together (no auto-identify)**

```http
POST /restapi/v2/workspaces/466206000000071000/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: multipart/form-data; boundary=----ZohoBoundary

------ZohoBoundary
Content-Disposition: form-data; name="CONFIG"

{
    "tableName": "SalesDataStrict",
    "fileType": "CSV",
    "autoIdentify": false,
    "delimiter": 0,
    "quoted": 2,
    "commentChar": "#",
    "skipTop": 2,
    "thousandSeparator": 0,
    "decimalSeparator": 0,
    "dateFormat": "dd MMM yyyy",
    "onError": "SKIPROW"
}
------ZohoBoundary
Content-Disposition: form-data; name="FILE"; filename="sales.csv"
Content-Type: text/csv

...
------ZohoBoundary--
```

**Case 3 — Pasted JSON data with explicit column data types and selected columns**

```http
POST /restapi/v2/workspaces/466206000000071000/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "tableName": "RegionSummary",
    "fileType": "JSON",
    "autoIdentify": true,
    "selectedColumns": ["Region", "Sales"],
    "columnDataTypes": [
        { "columnName": "Sales", "dataType": "CURRENCY" }
    ],
    "retainColumnNames": true,
    "onError": "SETCOLUMNEMPTY"
}&DATA=[{"Region":"West","Sales":"3928.38"},{"Region":"East","Sales":"1250.00"}]
```

**Case 4 — White Label / Client Portal workspace**

```http
POST /restapi/v2/workspaces/466206000000071009/data HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "tableName": "PortalSales",
    "fileType": "CSV",
    "autoIdentify": true
}&DATA=Region,Sales%0AWest,3928.38
```

## Sample Responses

**HTTP 200 OK — Table created and every row loaded (Case 1)**

```json
{
    "status": "success",
    "summary": "Import data",
    "data": {
        "viewId": "466206000000776558",
        "importSummary": {
            "importType": "APPEND",
            "totalColumnCount": 7,
            "selectedColumnCount": 7,
            "totalRowCount": 755,
            "successRowCount": 755,
            "warnings": 0,
            "importOperation": "created"
        },
        "columnDetails": {
            "Date": "Date",
            "Region": "Plain Text",
            "Product Category": "Plain Text",
            "Product": "Plain Text",
            "Customer Name": "Plain Text",
            "Sales": "Currency",
            "Cost": "Currency"
        },
        "importErrors": ""
    }
}
```

**HTTP 200 OK — `onError: "SETCOLUMNEMPTY"`: bad values blanked and reported (Case 3)**

```json
{
    "status": "success",
    "summary": "Import data",
    "data": {
        "viewId": "466206000000776560",
        "importSummary": {
            "importType": "APPEND",
            "totalColumnCount": 2,
            "selectedColumnCount": 2,
            "totalRowCount": 2,
            "successRowCount": 2,
            "warnings": 1,
            "importOperation": "created"
        },
        "columnDetails": {
            "Region": "Plain Text",
            "Sales": "Currency"
        },
        "importErrors": "<nobr>[Line: 2 Field:  1] (Hello) -RESET : Invalid NUMBER value</NOBR><br>"
    }
}
```

**HTTP 400 Bad Request — `onError: "ABORT"` (the default) and the file has a bad value**

```json
{
    "status": "failure",
    "summary": "IMPORT_ABORTED",
    "data": {
        "errorCode": 7232,
        "errorMessage": "<nobr>[Line: 2 Field:  1] (West) -ERROR: Invalid NUMBER value</NOBR><br><nobr>The data found at the row 2 has invalid data for the given configuration</NOBR><BR>"
    }
}
```

**HTTP 400 Bad Request — A table with this name already exists**

```json
{
    "status": "failure",
    "summary": "META_DBOBJECT_NAME_DUPLICATED",
    "data": {
        "errorCode": 7111,
        "errorMessage": "An object with the name SalesData already exists in this workspace."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Import Data into a New Table (Synchronous)](../../../sdk-examples/data-operations/sync-data-import/import-data-new-table.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Synchronous — the result is final when the call returns** | There is no job ID, no polling, and no callback. A 200 means the rows are already in the table. |
| **`data.viewId` is the handoff** | It is the only place the new table's ID is produced. Store it — every later operation on that table needs it. |
| **Create-once** | Re-posting the same `tableName` fails with `7111`. Subsequent loads go through [Import Data into an Existing Table (Synchronous)](import-data-existing-table.md). |
| **`onError` decides whether a bad value is fatal** | The default `ABORT` turns a single unparseable cell into a failed import with **nothing** written. Use `SKIPROW` or `SETCOLUMNEMPTY` for tolerant loading, and read `importErrors` afterwards. |
| **A clean HTTP 200 is not a clean import** | Check `successRowCount` against `totalRowCount`, and `warnings` against `0`. Both can indicate silently dropped or blanked data. |
| **`columnDetails` is the type-inference report** | With `autoIdentify: true` the types are guessed from the data. Inspect this map — a column that should be `Currency` but came back `Plain Text` usually means the separators were wrong. |
| **`autoIdentify: false` makes two attributes mandatory** | `delimiter` and `quoted` must both be supplied for CSV, otherwise `8079`. |
| **Parsing attributes are CSV-only** | `delimiter`, `quoted`, and `commentChar` are ignored for JSON, XML, Excel, Parquet, and Geometry sources. |
| **Column-count ceiling** | A source with more columns than the table format permits fails with `7478`, and a row with more fields than expected fails with `7208`. |
| **No `criteria`** | Row selection is by file content and `skipTop` only. |
| **No callback** | Callback notification belongs to the asynchronous/bulk import APIs; the synchronous ones return everything inline. |
| **Dependency chain** | [Get Workspace List](../../workspace-management/workspace-operations/overview.md) → `<workspace-id>` → Import Data into a New Table (Synchronous) → `data.viewId` → [Import Data into an Existing Table (Synchronous)](import-data-existing-table.md), [Row APIs](../row-operations/overview.md), [Get Columns](../../data-modeling-and-schema/columns/overview.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7092](../../../foundations/error-codes.md#error-7092) | 400 | `DDL_LOCK_SINCE_IMPORT_IN_PROGRESS` — A batch import is holding a lock in this workspace. | Retry once the import has finished. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | `META_DBOBJECT_NAME_DUPLICATED` — An object with this `tableName` already exists in the workspace. | Choose a different name, or import into the existing table with [Import Data into an Existing Table (Synchronous)](import-data-existing-table.md). |
| [7208](../../../foundations/error-codes.md#error-7208) | 400 | `IMPORT_FILE_NUMBER_OF_FIELDS_EXCEEDS_SIZE` — A row contains more fields than the header defines. | Correct the source data, or set the right `delimiter`. |
| [7232](../../../foundations/error-codes.md#error-7232) | 400 | `IMPORT_ABORTED` — A value could not be parsed and `onError` is `ABORT`. `errorMessage` carries the per-line detail. | Fix the data, or resend with `onError` set to `SKIPROW` or `SETCOLUMNEMPTY`. |
| [7248](../../../foundations/error-codes.md#error-7248) | 400 | `INVALID_FILE_CONTENT` — The payload could not be parsed as the declared `fileType`. | Check that `fileType` matches the actual content. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user cannot create tables in this workspace. | Ensure the user is an Account Admin, Organization Admin, Workspace Admin, or has Create Table permission. |
| [7478](../../../foundations/error-codes.md#error-7478) | 400 | `MORE_THAN_MAX_COLUMN` — The source has more columns than a table can hold. | Reduce the columns, or use `selectedColumns` to import a subset. |
| [7512](../../../foundations/error-codes.md#error-7512) | 400 | `INVALID_DATE_FORMAT` — A pattern in `dateFormat` / `columnDateFormat` could not be parsed. | Supply a valid date pattern such as `dd-MMM-yyyy`. |
| [8046](../../../foundations/error-codes.md#error-8046) | 400 | `INVALID_COLUMNS_SELECTED` — A name in `selectedColumns` is not present in the source data. | Match the names to the source's header row. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — A mandatory attribute is missing; with `autoIdentify: false` this is usually `delimiter` or `quoted`. | The message names the attribute. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE` — `fileType`, `onError`, `delimiter`, `quoted`, `thousandSeparator`, or `decimalSeparator` is outside its permitted set. | The message names the attribute and the allowed values. |
| [8139](../../../foundations/error-codes.md#error-8139) | 400 | `PASTED_DATA_LIMIT_EXCEEDED` — The `DATA` parameter exceeds 10,000,000 characters. | Send the payload as a `FILE` upload instead. |
| [8148](../../../foundations/error-codes.md#error-8148) | 400 | `DECIMAL_AND_THOUSAND_SEPARATOR_SAME` — The thousand and decimal separators resolve to the same character. | Choose different separators. |
| [8149](../../../foundations/error-codes.md#error-8149) | 400 | `DECIMAL_AND_THOUSAND_COLUMN_SEPARATOR_LEGNTH_VALIDATION` — A `columnSeparators` entry has fewer than two values. | Send `[thousandSeparator, decimalSeparator]` for each column. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` was not sent, or a mandatory key is missing at the template level. | Send a complete CONFIG object. |
| [8516](../../../foundations/error-codes.md#error-8516) | 400 | `UNABLE_TO_PARSE_DATA_TYPE` — A CONFIG value has the wrong JSON type. | Check that booleans are booleans and integers are integers. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.data.create`. |

# Related

- [Synchronous Data Import overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Import Data into an Existing Table (Synchronous)](import-data-existing-table.md).
- [SDK examples](../../../sdk-examples/data-operations/sync-data-import/import-data-new-table.md).
