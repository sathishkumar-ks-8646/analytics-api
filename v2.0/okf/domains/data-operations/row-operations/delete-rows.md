---
type: API Endpoint
title: Delete Row
description: Deletes rows from the specified table.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - row-operations
  - delete
  - data
api:
  operation_id: deleteRows
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows"
  domain: data-operations
  group: row-operations
  oauth_scopes:
    - ZohoAnalytics.data.delete
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Delete All Rows permission on the view."
  error_codes:
    - 7092
    - 7104
    - 7137
    - 7164
    - 7165
    - 7301
    - 7330
    - 7405
    - 8062
    - 8131
    - 8504
    - 8535
  openapi:
    file: "/references/openapi/data-operations-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1rows/delete"
    config_schema: DeleteRowsConfig
    response_schema: DeleteRowsResponse
  sdk_examples: "/sdk-examples/data-operations/row-operations/delete-rows.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows`** - Delete Row (Row Operations / Data Operations).

Deletes the rows of a table that match a filter, or every row.

> **Note on the permission.** This API is gated on the **Delete All Rows** permission, not the row-level Delete Row permission — and that holds even when `criteria` targets a single row. A user granted only Delete Row on a shared view cannot call this API and receives [`7301`](../../../foundations/error-codes.md#error-7301).

From the OpenAPI specification:

Deletes rows from the specified table. Note: While OpenAPI generally discourages request bodies for DELETE operations, this API supports it for detailed filtering.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deleteRows` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.data.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsdatadelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Delete All Rows permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1rows/delete`; CONFIG schema `DeleteRowsConfig`; response schema `DeleteRowsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.data.delete`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

CONFIG is **mandatory** for this API. Exactly one of `criteria` or `deleteAllRows` must be supplied.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `criteria` | String | Conditional* | — | Filter selecting the rows to delete. See [`criteria` Syntax](overview.md#criteria-syntax). |
| `deleteAllRows` | Boolean | Conditional* | `false` | When `true`, every row in the table is deleted. |

\* **Exactly one** of `criteria` or `deleteAllRows: true` must be sent. Supplying both, or neither, fails with [`8131`](../../../foundations/error-codes.md#error-8131) `INVALID_DELETE_CRITERIA_CONFIGURATION`.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Delete row"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.deletedRows` | Number | How many rows were deleted. **`0` is a normal success**, meaning the criteria matched nothing. This is the only field returned — there is no `invalidColumns` counterpart, because delete takes no `columns`. |

# Examples

## Sample Requests

**Case 1 — `criteria` only: delete the rows of one region**

```http
DELETE /restapi/v2/workspaces/466206000000071000/views/466206000000081001/rows HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "criteria": "\"Region\"='West'"
}
```

**Case 2 — Delete every row in the table**

```http
DELETE /restapi/v2/workspaces/466206000000071000/views/466206000000081001/rows HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "deleteAllRows": true
}
```

**Case 3 — White Label / Client Portal workspace**

```http
DELETE /restapi/v2/workspaces/466206000000071009/views/466206000000081009/rows HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "criteria": "\"Status\"='Closed'"
}
```

## Sample Responses

**HTTP 200 OK — Rows matched and were deleted (Cases 1 and 3)**

```json
{
    "status": "success",
    "summary": "Delete row",
    "data": {
        "deletedRows": 27
    }
}
```

**HTTP 200 OK — Nothing matched the criteria**

```json
{
    "status": "success",
    "summary": "Delete row",
    "data": {
        "deletedRows": 0
    }
}
```

**HTTP 400 Bad Request — Both `criteria` and `deleteAllRows` sent (or neither)**

```json
{
    "status": "failure",
    "summary": "INVALID_DELETE_CRITERIA_CONFIGURATION",
    "data": {
        "errorCode": 8131,
        "errorMessage": "Invalid criteria configuration for deleting data."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Delete Row](../../../sdk-examples/data-operations/row-operations/delete-rows.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Gated on Delete All Rows permission** | Even a single-row delete requires the Delete All Rows permission. This is the one place where the Row APIs' permission does not match the operation's name. |
| **`criteria` and `deleteAllRows` are mutually exclusive and jointly required** | Sending both, or neither, fails with `8131`. Omitting `criteria` does not delete everything — it errors. |
| **`deletedRows: 0` is a success, not a failure** | A criteria matching nothing returns HTTP 200. Check the count rather than the status code. |
| **Irreversible** | Deleted rows are not recoverable through the API; there is no row-level trash. `deleteAllRows: true` empties the table in one call. |
| **The table itself survives** | Only rows are removed — the table, its columns, its formulas, and everything built on it remain. To remove the table, use [Delete View](../../views-management/view-operations/delete-view.md). |
| **Shared users are silently constrained** | Their share filter criteria is ANDed with the supplied `criteria`, so a shared user calling `deleteAllRows: true` deletes only the rows within their own filtered slice. |
| **No stream-table restriction** | Unlike Add Row and Update Row, delete does not run the stream-table check, so `101021` does not apply here. |
| **Concurrency guard** | If another row-write request is still being processed for the same table, the call fails with `8062`. |
| **Dependency chain** | [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>` → [Get Columns](../../data-modeling-and-schema/columns/overview.md) (for `criteria` names) → Delete Row. |

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
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user cannot delete rows from this view. | Ensure the user is an Account Admin, Organization Admin, Workspace Admin, View Owner, or has **Delete All Rows** permission on the view. |
| [7330](../../../foundations/error-codes.md#error-7330) | 400 | `UNKNOWN_COLUMN_IN_FILTERCRITERIA` — A column referenced in `criteria` does not exist in the table. | Verify the column names in `criteria` via [Get Columns](../../data-modeling-and-schema/columns/overview.md). |
| [7405](../../../foundations/error-codes.md#error-7405) | 400 | `DML_NOT_ALLOWED` — Row modification is not allowed for this table. | Use a table that permits DML. |
| [8062](../../../foundations/error-codes.md#error-8062) | 400 | `ADD_ROW_REQUEST_STILL_IN_PROGRESS` — Another row-write request for this table is still being processed. | Retry after the in-flight request completes. |
| [8131](../../../foundations/error-codes.md#error-8131) | 400 | `INVALID_DELETE_CRITERIA_CONFIGURATION` — Both `criteria` and `deleteAllRows` were sent, or neither was. | Send exactly one of the two. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` was not sent. | Send a CONFIG object containing `criteria` or `deleteAllRows`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.data.delete`. |

# Related

- [Row Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Add Row](add-row.md), [Update Row](update-rows.md).
- [SDK examples](../../../sdk-examples/data-operations/row-operations/delete-rows.md).
