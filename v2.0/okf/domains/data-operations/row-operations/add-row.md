---
type: API Endpoint
title: Add Row
description: Inserts a single row into a table.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - row-operations
  - post
  - data
api:
  operation_id: addRow
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows"
  domain: data-operations
  group: row-operations
  oauth_scopes:
    - ZohoAnalytics.data.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Add Row permission on the view."
  error_codes:
    - 7092
    - 7104
    - 7137
    - 7164
    - 7165
    - 7301
    - 7405
    - 7512
    - 7515
    - 8016
    - 8504
    - 8535
    - 101021
  openapi:
    file: "/references/openapi/data-operations-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1rows/post"
    config_schema: AddRowConfig
    response_schema: AddRowResponse
  sdk_examples: "/sdk-examples/data-operations/row-operations/add-row.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows`** - Add Row (Row Operations / Data Operations).

Inserts a single row into a table.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `addRow` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.data.create`](../../../foundations/oauth-scopes.md#zohoanalyticsdatacreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Add Row permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1rows/post`; CONFIG schema `AddRowConfig`; response schema `AddRowResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.data.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `columns` | JSONObject | **Yes** | — | Column name → value map for the new row. Up to **300** columns. Column names are matched **case-insensitively** against the table's display names. Names that do not match any column are not an error — they are returned in `invalidColumns` and the rest of the row is still inserted. At least one name must match, otherwise `8016`. |
| `dateFormat` | String | No | — | Default date pattern applied to **all** date/date-time values in `columns`, e.g. `dd-MMM-yyyy`. Overridden per column by `columnDateFormat`. |
| `columnDateFormat` | JSONObject | No | — | Per-column date pattern overrides — column name → date pattern. 1–300 entries. Takes precedence over `dateFormat` for the columns it names. An unparseable pattern fails with `7512`. |

> Values for lookup (reference) columns must match an existing value in the parent table, otherwise the request fails with [`7515`](../../../foundations/error-codes.md#error-7515).

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Add row"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.addedColumns` | JSONObject | The column name → value pairs that were actually written, echoed with the casing **as sent** in the request. **All values are strings**, even for numeric, boolean, and date columns. Present for a normal insert. |
| `data.invalidColumns` | JSONObject | The column name → value pairs from the request that did **not** match any column in the table. **Always present**; an empty object `{}` when every name matched. A non-empty value here is not an error — those values were silently skipped and the row was still inserted. |

> The response does not return the ID or row number of the inserted row.

# Examples

## Sample Requests

**Case 1 — Simple row insert**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000081001/rows HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "columns": {
        "Region": "East",
        "Product": "Fruits and Vegetables",
        "Sales": "3928.38"
    }
}
```

**Case 2 — Row insert with a default date format and per-column overrides**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000081001/rows HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "columns": {
        "Region": "East",
        "Sales": "1000",
        "Order Date": "01-Jan-2026",
        "Ship Date": "15/01/2026"
    },
    "dateFormat": "dd-MMM-yyyy",
    "columnDateFormat": {
        "Ship Date": "dd/MM/yyyy"
    }
}
```

**Case 3 — White Label / Client Portal workspace**

```http
POST /restapi/v2/workspaces/466206000000071009/views/466206000000081009/rows HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "columns": {
        "Region": "West",
        "Sales": "2500"
    }
}
```

## Sample Responses

**HTTP 200 OK — Simple insert (Case 1)**

```json
{
    "status": "success",
    "summary": "Add row",
    "data": {
        "addedColumns": {
            "Region": "East",
            "Product": "Fruits and Vegetables",
            "Sales": "3928.38"
        },
        "invalidColumns": {}
    }
}
```

**HTTP 200 OK — Insert where one column name did not match the table**

```json
{
    "status": "success",
    "summary": "Add row",
    "data": {
        "addedColumns": {
            "Region": "East",
            "Sales": "1000"
        },
        "invalidColumns": {
            "Regoin": "East"
        }
    }
}
```

**HTTP 400 Bad Request — The target view is not a table**

```json
{
    "status": "failure",
    "summary": "NOT_A_TABLE",
    "data": {
        "errorCode": 7137,
        "errorMessage": "Sales Overview is not a table."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Add Row](../../../sdk-examples/data-operations/row-operations/add-row.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **One row per call** | There is no batch form of this API. To load many rows, use the Data Import APIs — looping Add Row is far slower and consumes one API unit per row. |
| **Unknown columns are skipped, not rejected** | A misspelled column name lands in `invalidColumns` and the insert still succeeds with the remaining columns. Always inspect `invalidColumns`; an empty `{}` is the only confirmation that the whole row was written as intended. |
| **At least one column must match** | If *no* supplied name matches a table column the call fails with `8016`, since there would be nothing to insert. |
| **Column matching is case-insensitive** | `"region"`, `"Region"`, and `"REGION"` all resolve to the same column. The response echoes the casing you sent, not the table's. |
| **Values are strings in both directions** | Send `"Sales": "1000"`, not `"Sales": 1000`, and expect `"1000"` back. |
| **Date parsing precedence** | `columnDateFormat` for that specific column, else `dateFormat`, else the column's own configured format. |
| **Lookup columns are validated** | A value that does not exist in the parent table fails the whole insert with `7515`. |
| **Row-limit and plan checks apply** | The insert is checked against the organization's row allowance before it is written. |
| **No `criteria`** | Insert has nothing to filter; the attribute is not accepted. |
| **Dependency chain** | [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>` → [Get Columns](../../data-modeling-and-schema/columns/overview.md) (to confirm column names) → Add Row. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7092](../../../foundations/error-codes.md#error-7092) | 400 | `DDL_LOCK_SINCE_IMPORT_IN_PROGRESS` — A batch import is holding a lock on this table. | Retry once the import has finished. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — The view does not exist. | Verify `<view-id>`. |
| [7137](../../../foundations/error-codes.md#error-7137) | 400 | `NOT_A_TABLE` — The target view is not a table. | Target a table; reports, dashboards, and query tables cannot accept rows. |
| [7164](../../../foundations/error-codes.md#error-7164) | 400 | `SYSTEM_TABLE_DATA_MOD` — System table data cannot be modified. | System tables are managed by Zoho Analytics. Target a user-created table instead. |
| [7165](../../../foundations/error-codes.md#error-7165) | 400 | `SNAPSHOT_TABLE_DATAMOD` — Snapshot table data cannot be modified. | Target a non-snapshot table. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user cannot add rows to this view. | Ensure the user is an Account Admin, Organization Admin, Workspace Admin, View Owner, or has Add Row permission on the view. |
| [7405](../../../foundations/error-codes.md#error-7405) | 400 | `DML_NOT_ALLOWED` — Row modification is not allowed for this table. | Use a table that permits DML. |
| [7512](../../../foundations/error-codes.md#error-7512) | 400 | `INVALID_DATE_FORMAT` — A pattern in `dateFormat` / `columnDateFormat` could not be parsed. | Supply a valid date pattern such as `dd-MMM-yyyy`. |
| [7515](../../../foundations/error-codes.md#error-7515) | 400 | `UNKNOWN_LOOKUP_VALUE` — A value for a lookup column does not exist in the parent table. | Add the value to the parent table first, or send an existing one. |
| [8016](../../../foundations/error-codes.md#error-8016) | 400 | `API_NO_COLUMN_PRESENT` — None of the supplied column names matched a column in the table. | Check the names via [Get Columns](../../data-modeling-and-schema/columns/overview.md). |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` was not sent, or `columns` is missing. | Send a CONFIG object containing `columns`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.data.create`. |
| [101021](../../../foundations/error-codes.md#error-101021) | 400 | `NOT_A_STREAM_TABLE` — Row operations are not supported on a stream table. | Target a non-stream table. |

# Related

- [Row Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Update Row](update-rows.md), [Delete Row](delete-rows.md).
- [SDK examples](../../../sdk-examples/data-operations/row-operations/add-row.md).
