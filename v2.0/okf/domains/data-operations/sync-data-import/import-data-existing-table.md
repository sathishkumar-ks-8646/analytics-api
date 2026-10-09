---
type: API Endpoint
title: Import Data into an Existing Table (Synchronous)
description: Use Bulk APIs to import data into an existing specified table synchronously.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - sync-data-import
  - post
  - data
api:
  operation_id: importDataExistingTable
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data"
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
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user holding the import permission that matches the requested importType — see Permission Model."
  error_codes:
    - 7092
    - 7104
    - 7107
    - 7164
    - 7165
    - 7208
    - 7232
    - 7248
    - 7301
    - 7319
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
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1data/post"
    config_schema: ImportConfigExistingTable
    response_schema: ExistImportSuccessResponse
  sdk_examples: "/sdk-examples/data-operations/sync-data-import/import-data-existing-table.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data`** - Import Data into an Existing Table (Synchronous) (Synchronous Data Import / Data Operations).

Loads the uploaded data into an existing table, appending, replacing, or merging according to `importType`.

From the OpenAPI specification:

Use Bulk APIs to import data into an existing specified table synchronously.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `importDataExistingTable` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.data.create`](../../../foundations/oauth-scopes.md#zohoanalyticsdatacreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user holding the import permission that matches the requested importType — see Permission Model. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` part of a `multipart/form-data` body - **mandatory** |
| Request Content-Type | `multipart/form-data` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1data/post`; CONFIG schema `ImportConfigExistingTable`; response schema `ExistImportSuccessResponse` |

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
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

CONFIG is **mandatory**. This API takes the same options as [Import Data into a New Table (Synchronous)](import-data-new-table.md), with `tableName` replaced by `importType` and `matchingColumns` added.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `importType` | String (enum) | **Yes** | — | How the incoming rows are combined with the existing ones. See [`importType` Values](#importtype-values). Case-insensitive. |
| `fileType` | String (enum) | **Yes** | — | Format of the payload. See [`fileType` Values](import-data-new-table.md#filetype-values). |
| `autoIdentify` | Boolean | **Yes** | — | As in the new-table import — when `false`, `delimiter` and `quoted` become mandatory for CSV. |
| `matchingColumns` | JSONArray of String | Conditional* | — | Columns used to match an incoming row against an existing one. 1–100 entries; every name must already exist in the table (`7107` otherwise). |
| `onError` | String (enum) | No | `ABORT` | See [`onError` Values](import-data-new-table.md#onerror-values). |
| `selectedColumns` | JSONArray of String | No | all columns | Import only these columns from the source. 1–300 entries. |
| `skipTop` | Integer | No | `0` | Number of leading rows to ignore. |
| `delimiter` | Integer (enum) | Conditional | `0` | CSV field separator, `0`–`4`. Mandatory when `autoIdentify` is `false`. |
| `quoted` | Integer (enum) | Conditional | `2` | CSV quote character, `0`–`2`. Mandatory when `autoIdentify` is `false`. |
| `commentChar` | String | No | none | Lines starting with this character are ignored. CSV only. |
| `thousandSeparator` | Integer (enum) | No | auto | See [Number Separator Values](import-data-new-table.md#number-separator-values). |
| `decimalSeparator` | Integer (enum) | No | auto | See [Number Separator Values](import-data-new-table.md#number-separator-values). |
| `columnSeparators` | JSONObject | No | — | Per-column separator overrides. |
| `dateFormat` | String | No | auto | Default date pattern. |
| `columnDateFormat` | JSONObject | No | — | Per-column date pattern overrides. |
| `columnTimeFormat` | JSONObject | No | — | Per-column time pattern overrides. |
| `columnDurationFormat` | JSONObject | No | — | Per-column duration pattern overrides. |
| `columnDataTypes` | JSONArray | No | — | Explicit data types. **Entries naming a column that already exists in the table are discarded** — an existing column keeps its established type. |
| `matchNulls` | Boolean | No | `false` | Treat empty source values as nulls when matching rows. Relevant to `UPDATEADD`. |
| `updateNullForNegativeValues` | Boolean | No | `false` | Store null instead of a negative value in columns that do not accept one. |
| `retainColumnNames` | Boolean | No | `false` | For JSON/XML, keep the source's original key names. |
| `importHiddenRows` | Boolean | No | `false` | For Excel sources, include hidden rows. |
| `importHiddenColumns` | Boolean | No | `false` | For Excel sources, include hidden columns. |

\* `matchingColumns` is **mandatory** when `importType` is `UPDATEADD`, and ignored for `APPEND` and `TRUNCATEADD`.

### `importType` Values

| Value | Behaviour | Needs `matchingColumns` |
|-------|-----------|-------------------------|
| `APPEND` | Adds every incoming row to the table, keeping all existing rows. | No |
| `TRUNCATEADD` | Deletes **all** existing rows, then adds the incoming ones. | No |
| `UPDATEADD` | Updates rows whose `matchingColumns` values match an incoming row; adds the rest as new rows. | **Yes** |

> These three modes are the complete supported set. Any other value is rejected with [`8119`](../../../foundations/error-codes.md#error-8119), whose message names the permitted values.

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
| `summary` | String | Localised operation summary. `"Import data"`. |
| `data` | JSONObject | Response payload wrapper. |
| `data.importSummary` | JSONObject | Counts describing what was loaded — same shape as in [Import Data into a New Table (Synchronous)](import-data-new-table.md). |
| `importSummary.importType` | String | The `importType` that was applied, in **upper case**. |
| `importSummary.totalColumnCount` | Number | Columns found in the source data. |
| `importSummary.selectedColumnCount` | Number | Columns actually imported. |
| `importSummary.totalRowCount` | Number | Data rows found in the source. |
| `importSummary.successRowCount` | Number | Rows actually written. |
| `importSummary.warnings` | Number | Count of values reset or flagged during the load. |
| `importSummary.importOperation` | String | Always `"updated"` for this API — an existing table was written to rather than created. |
| `data.columnDetails` | JSONObject | Column name → assigned data type label. For an existing table these are the table's established types. |
| `data.importErrors` | String | Per-line warnings and resets as an HTML fragment. Always present; `""` when clean. |

> **`viewId` is not returned by this API** — the target table's ID was already supplied in the URL.

# Examples

## Sample Requests

**Case 1 — Append a new batch of rows**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000776558/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: multipart/form-data; boundary=----ZohoBoundary

------ZohoBoundary
Content-Disposition: form-data; name="CONFIG"

{
    "importType": "APPEND",
    "fileType": "CSV",
    "autoIdentify": true
}
------ZohoBoundary
Content-Disposition: form-data; name="FILE"; filename="sales-march.csv"
Content-Type: text/csv

Date,Region,Product,Sales,Cost
01 March 2026,West,Fruits and Vegetables,4120.10,210.00
------ZohoBoundary--
```

**Case 2 — Merge updates by key, with parsing options clubbed together**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000776558/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: multipart/form-data; boundary=----ZohoBoundary

------ZohoBoundary
Content-Disposition: form-data; name="CONFIG"

{
    "importType": "UPDATEADD",
    "fileType": "CSV",
    "autoIdentify": false,
    "delimiter": 0,
    "quoted": 2,
    "matchingColumns": ["Region", "Product"],
    "matchNulls": true,
    "thousandSeparator": 0,
    "decimalSeparator": 0,
    "dateFormat": "dd MMM yyyy",
    "onError": "SETCOLUMNEMPTY"
}
------ZohoBoundary
Content-Disposition: form-data; name="FILE"; filename="sales-corrections.csv"
Content-Type: text/csv

...
------ZohoBoundary--
```

**Case 3 — Replace the table's contents entirely, using pasted data**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000776558/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "importType": "TRUNCATEADD",
    "fileType": "CSV",
    "autoIdentify": true,
    "selectedColumns": ["Region", "Sales"],
    "skipTop": 1
}&DATA=Region,Sales%0AWest,3928.38%0AEast,1250.00
```

**Case 4 — White Label / Client Portal workspace**

```http
POST /restapi/v2/workspaces/466206000000071009/views/466206000000776599/data HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "importType": "APPEND",
    "fileType": "CSV",
    "autoIdentify": true
}&DATA=Region,Sales%0AWest,3928.38
```

## Sample Responses

**HTTP 200 OK — Append into an existing table (Case 1)**

```json
{
    "status": "success",
    "summary": "Import data",
    "data": {
        "importSummary": {
            "importType": "APPEND",
            "totalColumnCount": 9,
            "selectedColumnCount": 9,
            "totalRowCount": 6,
            "successRowCount": 6,
            "warnings": 0,
            "importOperation": "updated"
        },
        "columnDetails": {
            "plainCol": "Plain Text",
            "emailCol": "E-Mail",
            "intCol": "Number",
            "numCol": "Positive Number",
            "decCol": "Decimal Number",
            "curCol": "Currency",
            "perCol": "Percentage",
            "dateCol": "Date",
            "boolCol": "Plain Text"
        },
        "importErrors": ""
    }
}
```

**HTTP 200 OK — `UPDATEADD` merge (Case 2)**

```json
{
    "status": "success",
    "summary": "Import data",
    "data": {
        "importSummary": {
            "importType": "UPDATEADD",
            "totalColumnCount": 9,
            "selectedColumnCount": 9,
            "totalRowCount": 6,
            "successRowCount": 6,
            "warnings": 0,
            "importOperation": "updated"
        },
        "columnDetails": {
            "plainCol": "Plain Text",
            "emailCol": "E-Mail",
            "intCol": "Number",
            "numCol": "Positive Number",
            "decCol": "Decimal Number",
            "curCol": "Currency",
            "perCol": "Percentage",
            "dateCol": "Date",
            "boolCol": "Plain Text"
        },
        "importErrors": ""
    }
}
```

**HTTP 200 OK — Rows loaded with per-value warnings**

```json
{
    "status": "success",
    "summary": "Import data",
    "data": {
        "importSummary": {
            "importType": "TRUNCATEADD",
            "totalColumnCount": 5,
            "selectedColumnCount": 5,
            "totalRowCount": 100,
            "successRowCount": 100,
            "warnings": 3,
            "importOperation": "updated"
        },
        "columnDetails": {
            "Region": "Plain Text",
            "State": "Geo Column",
            "Sales": "Currency",
            "Cost": "Currency",
            "Date": "Date"
        },
        "importErrors": "<nobr>[Line: 6 Field:  4] (andhara pradesh) -WARNING: Invalid GEO LOCATION</NOBR><br><nobr>[Line: 7 Field:  4] (utter pradesh) -WARNING: Invalid GEO LOCATION</NOBR><br>"
    }
}
```

**HTTP 400 Bad Request — A name in `matchingColumns` does not exist in the table**

```json
{
    "status": "failure",
    "summary": "META_OBJECT_NOT_PRESENT",
    "data": {
        "errorCode": 7107,
        "errorMessage": "The column Regoin is not present."
    }
}
```

**HTTP 403 Forbidden — The user lacks the import permission for this `importType`**

```json
{
    "status": "failure",
    "summary": "SECURITY_NOT_PERMITTED",
    "data": {
        "errorCode": 7301,
        "errorMessage": "You (RestapiNotPermittedUser V2) do not have the permission to do this operation. "
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Import Data into an Existing Table (Synchronous)](../../../sdk-examples/data-operations/sync-data-import/import-data-existing-table.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **The required permission depends on `importType`** | This is the behaviour most likely to produce an unexpected `7301`. Append, truncate-and-add, and add-or-update are four *separate* permissions, so a user who can append may still be refused a truncate. See [Permission Model](overview.md#permission-model). |
| **`TRUNCATEADD` deletes first** | Every existing row is removed before the incoming rows are written. If the import then fails mid-way, the table can be left with fewer rows than it started with. There is no dry-run. |
| **`UPDATEADD` requires `matchingColumns`** | Without it the call fails; with a name that is not a real column it fails with `7107`. The match is on the named columns' values, not on any row ID. |
| **Existing columns keep their types** | `columnDataTypes` entries that name a column already present in the table are dropped, so this attribute only influences columns the import is adding. |
| **`onError: "ABORT"` is still the default** | A single unparseable value aborts the whole import and rolls it back. |
| **A clean HTTP 200 is not a clean import** | Compare `successRowCount` with `totalRowCount` and check `warnings`. |
| **The table is DDL-locked during the import** | Concurrent structural changes are blocked while the load runs, and a load attempted while another import holds the lock fails with `7092`. |
| **Snapshot and system tables are rejected** | `7165` and `7164` respectively — see [Table Preconditions](overview.md#table-preconditions-existing-table-import). |
| **No `criteria`** | Which rows are affected is decided by `importType` and `matchingColumns`, not by a filter expression. |
| **Dependency chain** | [Import Data into a New Table (Synchronous)](import-data-new-table.md) or [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>` → [Get Columns](../../data-modeling-and-schema/columns/overview.md) (to pick `matchingColumns`) → Import Data into an Existing Table (Synchronous). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7092](../../../foundations/error-codes.md#error-7092) | 400 | `DDL_LOCK_SINCE_IMPORT_IN_PROGRESS` — Another import is holding a DDL lock on this table. | Retry once it has finished. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — The view does not exist. | Verify `<view-id>`. |
| [7107](../../../foundations/error-codes.md#error-7107) | 400 | `META_OBJECT_NOT_PRESENT` — A column named in `matchingColumns` is not present in the table. | Verify the names via [Get Columns](../../data-modeling-and-schema/columns/overview.md). |
| [7164](../../../foundations/error-codes.md#error-7164) | 400 | `SYSTEM_TABLE_DATA_MOD` — System table data cannot be modified. | Target a user-created table instead. |
| [7165](../../../foundations/error-codes.md#error-7165) | 400 | `SNAPSHOT_TABLE_DATAMOD` — Snapshot table data cannot be modified. | Target a non-snapshot table. |
| [7208](../../../foundations/error-codes.md#error-7208) | 400 | `IMPORT_FILE_NUMBER_OF_FIELDS_EXCEEDS_SIZE` — A row contains more fields than expected. | Correct the source data or the `delimiter`. |
| [7232](../../../foundations/error-codes.md#error-7232) | 400 | `IMPORT_ABORTED` — A value could not be parsed and `onError` is `ABORT`. | Fix the data, or resend with `SKIPROW` / `SETCOLUMNEMPTY`. |
| [7248](../../../foundations/error-codes.md#error-7248) | 400 | `INVALID_FILE_CONTENT` — The payload could not be parsed as the declared `fileType`. | Check that `fileType` matches the content. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user lacks the import permission matching `importType`, or is outside the workspace's permitted IP range. | Grant the specific import permission (see [Permission Model](overview.md#permission-model)), or use an `importType` the user is allowed. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The table does not belong to the specified workspace. | Ensure `<workspace-id>` and `<view-id>` are consistent. |
| [7478](../../../foundations/error-codes.md#error-7478) | 400 | `MORE_THAN_MAX_COLUMN` — The source has more columns than the table can hold. | Reduce the columns, or use `selectedColumns`. |
| [7512](../../../foundations/error-codes.md#error-7512) | 400 | `INVALID_DATE_FORMAT` — A date pattern could not be parsed. | Supply a valid pattern. |
| [8046](../../../foundations/error-codes.md#error-8046) | 400 | `INVALID_COLUMNS_SELECTED` — A name in `selectedColumns` is not present in the source data. | Match the names to the source's header row. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — A mandatory attribute is missing — commonly `matchingColumns` for `UPDATEADD`, or `delimiter`/`quoted` when `autoIdentify` is `false`. | The message names the attribute. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE` — `importType`, `fileType`, `onError`, `delimiter`, `quoted`, `thousandSeparator`, or `decimalSeparator` is outside its permitted set. | The message names the attribute and the allowed values. |
| [8139](../../../foundations/error-codes.md#error-8139) | 400 | `PASTED_DATA_LIMIT_EXCEEDED` — The `DATA` parameter exceeds 10,000,000 characters. | Send the payload as a `FILE` upload instead. |
| [8148](../../../foundations/error-codes.md#error-8148) | 400 | `DECIMAL_AND_THOUSAND_SEPARATOR_SAME` — The thousand and decimal separators are the same character. | Choose different separators. |
| [8149](../../../foundations/error-codes.md#error-8149) | 400 | `DECIMAL_AND_THOUSAND_COLUMN_SEPARATOR_LEGNTH_VALIDATION` — A `columnSeparators` entry has fewer than two values. | Send `[thousandSeparator, decimalSeparator]` per column. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` was not sent, or a mandatory key is missing. | Send a complete CONFIG object. |
| [8516](../../../foundations/error-codes.md#error-8516) | 400 | `UNABLE_TO_PARSE_DATA_TYPE` — A CONFIG value has the wrong JSON type. | Check booleans and integers are sent as such. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.data.create`. |

# Related

- [Synchronous Data Import overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Import Data into a New Table (Synchronous)](import-data-new-table.md).
- [SDK examples](../../../sdk-examples/data-operations/sync-data-import/import-data-existing-table.md).
