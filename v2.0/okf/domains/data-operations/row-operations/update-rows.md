---
type: API Endpoint
title: Update Row
description: Updates rows in the specified table.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - row-operations
  - put
  - data
api:
  operation_id: updateRows
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows"
  domain: data-operations
  group: row-operations
  oauth_scopes:
    - ZohoAnalytics.data.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Update Row permission on the view. When addIfNotExist triggers an insert, Add Row permission is additionally required."
  error_codes:
    - 7092
    - 7104
    - 7137
    - 7164
    - 7165
    - 7301
    - 7330
    - 7405
    - 7512
    - 7515
    - 8016
    - 8062
    - 8130
    - 8504
    - 8535
    - 101021
  openapi:
    file: "/references/openapi/data-operations-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1rows/put"
    config_schema: UpdateRowsConfig
    response_schema: UpdateRowsResponse
  sdk_examples: "/sdk-examples/data-operations/row-operations/update-rows.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-operations-grouped-api.json"
    title: OpenAPI 3 specification - data-operations-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**PUT `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows`** - Update Row (Row Operations / Data Operations).

Updates the rows of a table that match a filter, or every row. Can optionally insert a row when nothing matches.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `updateRows` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.data.update`](../../../foundations/oauth-scopes.md#zohoanalyticsdataupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Update Row permission on the view. When addIfNotExist triggers an insert, Add Row permission is additionally required. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1rows/put`; CONFIG schema `UpdateRowsConfig`; response schema `UpdateRowsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.data.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

CONFIG is **mandatory** for this API. Exactly one of `criteria` or `updateAllRows` must be supplied.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `columns` | JSONObject | **Yes** | — | Column name → new value map. Up to **300** columns. Matched case-insensitively; unmatched names are returned in `invalidColumns` rather than rejected. |
| `criteria` | String | Conditional* | — | Filter selecting the rows to update. See [`criteria` Syntax](overview.md#criteria-syntax). |
| `updateAllRows` | Boolean | Conditional* | `false` | When `true`, every row in the table is updated. |
| `addIfNotExist` | Boolean | No | `false` | When `true` and **no row matches `criteria`**, a new row is inserted from `columns` instead. Requires Add Row permission. Has no effect when rows do match. |
| `dateFormat` | String | No | — | Default date pattern for all date/date-time values in `columns`. |
| `columnDateFormat` | JSONObject | No | — | Per-column date pattern overrides. 1–300 entries. Takes precedence over `dateFormat`. |

\* **Exactly one** of `criteria` or `updateAllRows: true` must be sent. Supplying both, or neither, fails with [`8130`](../../../foundations/error-codes.md#error-8130) `INVALID_UPDATE_CRITERIA_CONFIGURATION`.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Update row"` for this API — the same string whether rows were updated or a row was inserted via `addIfNotExist`. |
| `data` | JSONObject | Response payload wrapper. |
| `data.updatedColumns` | JSONObject | The column name → value pairs that were applied, echoed with the casing as sent. **All values are strings.** |
| `data.updatedRows` | Number | How many existing rows were changed. **`0` is a normal success**, meaning the criteria matched nothing. It is also `0` when `addIfNotExist` inserted a row instead. |
| `data.newRowAdded` | Boolean | **Present only** when `addIfNotExist` caused an insert, in which case it is `true`. Absent on a normal update — test for key presence, not for a `false` value. |
| `data.invalidColumns` | JSONObject | Column name → value pairs that matched no column in the table. Always present; `{}` when everything matched. |

# Examples

## Sample Requests

**Case 1 — `criteria` only: update the rows of one region**

```http
PUT /restapi/v2/workspaces/466206000000071000/views/466206000000081001/rows HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "columns": {
        "Region": "East_1"
    },
    "criteria": "\"Region\"='East'"
}
```

**Case 2 — Update every row in the table**

```http
PUT /restapi/v2/workspaces/466206000000071000/views/466206000000081001/rows HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "columns": {
        "Status": "Processed"
    },
    "updateAllRows": true
}
```

**Case 3 — Update-or-insert with date handling clubbed together**

```http
PUT /restapi/v2/workspaces/466206000000071000/views/466206000000081001/rows HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "columns": {
        "Region": "North",
        "Sales": "2100",
        "Order Date": "01-Jan-2026"
    },
    "criteria": "\"Region\"='North'",
    "addIfNotExist": true,
    "dateFormat": "dd-MMM-yyyy"
}
```

**Case 4 — White Label / Client Portal workspace**

```http
PUT /restapi/v2/workspaces/466206000000071009/views/466206000000081009/rows HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "columns": {
        "Status": "Reviewed"
    },
    "criteria": "\"Region\"='West'"
}
```

## Sample Responses

**HTTP 200 OK — Rows matched and were updated (Cases 1, 2 and 4)**

```json
{
    "status": "success",
    "summary": "Update row",
    "data": {
        "updatedColumns": {
            "Region": "East_1"
        },
        "updatedRows": 27,
        "invalidColumns": {}
    }
}
```

**HTTP 200 OK — Nothing matched the criteria (no rows changed)**

```json
{
    "status": "success",
    "summary": "Update row",
    "data": {
        "updatedColumns": {
            "Region": "East_1"
        },
        "updatedRows": 0,
        "invalidColumns": {}
    }
}
```

**HTTP 200 OK — `addIfNotExist` inserted a row because nothing matched (Case 3)**

```json
{
    "status": "success",
    "summary": "Update row",
    "data": {
        "newRowAdded": true,
        "updatedColumns": {
            "Region": "North",
            "Sales": "2100",
            "Order Date": "01-Jan-2026"
        },
        "updatedRows": 0,
        "invalidColumns": {}
    }
}
```

**HTTP 400 Bad Request — Both `criteria` and `updateAllRows` sent (or neither)**

```json
{
    "status": "failure",
    "summary": "INVALID_UPDATE_CRITERIA_CONFIGURATION",
    "data": {
        "errorCode": 8130,
        "errorMessage": "Invalid criteria configuration for updating data."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Update Row](../../../sdk-examples/data-operations/row-operations/update-rows.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`criteria` and `updateAllRows` are mutually exclusive and jointly required** | Sending both, or neither, fails with `8130`. There is no implicit "update everything" default — omitting `criteria` does not update all rows, it errors. |
| **`updatedRows: 0` is a success, not a failure** | A criteria that matches nothing returns HTTP 200. Check `updatedRows` rather than relying on the status code to detect a no-op. |
| **`addIfNotExist` converts the call into an insert** | When it fires, the response switches shape: `newRowAdded: true` appears, the applied values come back under `updatedColumns` (not `addedColumns`), and `updatedRows` stays `0`. The caller needs Add Row permission as well as Update Row. |
| **The insert path is a plain insert** | `addIfNotExist` does not merge into a partially matching row — it writes exactly the `columns` supplied, so any column not listed takes its default or stays empty. |
| **Shared users are silently constrained** | Their share filter criteria is ANDed with the supplied `criteria`, so `updatedRows` may be lower than expected without any error being raised. |
| **Unknown columns are skipped, not rejected** | Same behaviour as Add Row — inspect `invalidColumns`. |
| **Values are strings in both directions** | Send `"Sales": "2000"` and expect `"2000"` back. |
| **Concurrency guard** | If another row-write request is still being processed for the same table, the call fails with `8062`. Retry after a short delay. |
| **Dependency chain** | [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>` → [Get Columns](../../data-modeling-and-schema/columns/overview.md) (for `criteria` and `columns` names) → Update Row. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7092](../../../foundations/error-codes.md#error-7092) | 400 | `DDL_LOCK_SINCE_IMPORT_IN_PROGRESS` — A batch import is holding a lock on this table. | Retry once the import has finished. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — The view does not exist. | Verify `<view-id>`. |
| [7137](../../../foundations/error-codes.md#error-7137) | 400 | `NOT_A_TABLE` — The target view is not a table. | Target a table. |
| [7164](../../../foundations/error-codes.md#error-7164) | 400 | `SYSTEM_TABLE_DATA_MOD` — System table data cannot be modified. | Target a user-created table instead. |
| [7165](../../../foundations/error-codes.md#error-7165) | 400 | `SNAPSHOT_TABLE_DATAMOD` — Snapshot table data cannot be modified. | Target a non-snapshot table. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user cannot update rows in this view, or lacks Add Row permission when `addIfNotExist` fires. | Ensure the user has Update Row permission — and Add Row permission too if `addIfNotExist` is used. |
| [7330](../../../foundations/error-codes.md#error-7330) | 400 | `UNKNOWN_COLUMN_IN_FILTERCRITERIA` — A column referenced in `criteria` does not exist in the table. | Verify the column names in `criteria` via [Get Columns](../../data-modeling-and-schema/columns/overview.md). |
| [7405](../../../foundations/error-codes.md#error-7405) | 400 | `DML_NOT_ALLOWED` — Row modification is not allowed for this table. | Use a table that permits DML. |
| [7512](../../../foundations/error-codes.md#error-7512) | 400 | `INVALID_DATE_FORMAT` — A pattern in `dateFormat` / `columnDateFormat` could not be parsed. | Supply a valid date pattern. |
| [7515](../../../foundations/error-codes.md#error-7515) | 400 | `UNKNOWN_LOOKUP_VALUE` — A value for a lookup column does not exist in the parent table. | Send an existing lookup value. |
| [8016](../../../foundations/error-codes.md#error-8016) | 400 | `API_NO_COLUMN_PRESENT` — None of the supplied column names matched a column in the table. | Check the names via [Get Columns](../../data-modeling-and-schema/columns/overview.md). |
| [8062](../../../foundations/error-codes.md#error-8062) | 400 | `ADD_ROW_REQUEST_STILL_IN_PROGRESS` — Another row-write request for this table is still being processed. | Retry after the in-flight request completes. |
| [8130](../../../foundations/error-codes.md#error-8130) | 400 | `INVALID_UPDATE_CRITERIA_CONFIGURATION` — Both `criteria` and `updateAllRows` were sent, or neither was. | Send exactly one of the two. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` was not sent, or `columns` is missing. | Send a CONFIG object containing `columns`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.data.update`. |
| [101021](../../../foundations/error-codes.md#error-101021) | 400 | `NOT_A_STREAM_TABLE` — Row operations are not supported on a stream table. | Target a non-stream table. |

# Related

- [Row Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Add Row](add-row.md), [Delete Row](delete-rows.md).
- [SDK examples](../../../sdk-examples/data-operations/row-operations/update-rows.md).
