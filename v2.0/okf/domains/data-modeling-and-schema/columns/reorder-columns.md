---
type: API Endpoint
title: Reorder Columns
description: Changes the display order of the columns of the specified table.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/reorder"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - columns
  - put
  - modeling
api:
  operation_id: reorderColumns
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/reorder"
  domain: data-modeling-and-schema
  group: columns
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the view."
  error_codes:
    - 7301
    - 7319
    - 8179
    - 8180
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1columns~1reorder/put"
    config_schema: ReorderColumnsConfig
    response_schema: null
  sdk_examples: "/sdk-examples/data-modeling-and-schema/columns/reorder-columns.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**PUT `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/reorder`** - Reorder Columns (Columns / Data Modeling & Schema).

Changes the display order of all columns in the specified table. The complete set of non-system column IDs must be supplied in the desired order — this API does not support reordering a partial subset of columns.

> **Not available in custom-domain (White Label) contexts.** This API cannot be called via a portal domain URL. It is only accessible through the standard `analyticsapi.zoho.com` host.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `reorderColumns` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/reorder` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1columns~1reorder/put`; CONFIG schema `ReorderColumnsConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

| Parameter | Type | Mandatory | Max Items | Default | Description |
|-----------|------|-----------|-----------|---------|-------------|
| `columns` | JSONArray of String | **Yes** | 300 | — | Complete, ordered array of column IDs (as strings) representing the new display order. Must include **every** non-system column of the table — omitting even one returns error 8179. Duplicate IDs are silently de-duplicated (only the first occurrence is kept). |

> **All non-system columns required, not a subset.** Unlike Hide/Show Columns, this API requires the full column list on every call. System columns (e.g., `ROWID`, audit columns) are excluded from the required set and cannot be reordered.

## Notes from the OpenAPI specification

- This API returns HTTP 204 No Content with no response body on success. There is no status or summary key to parse - treat the HTTP status code as the sole success indicator.
- The full column set is required on every call. Unlike the Hide Columns and Show Columns APIs, this one rejects a partial list with error 8179, so a column cannot be moved without also listing every other column in its existing position.
- System columns, such as the row ID and the audit columns, are excluded from the required set and cannot be reordered.
- The order of the array defines the display order. The position of each ID becomes the new left-to-right position of that column.
- Column IDs must be sent as quoted strings, not as integers.
- A duplicate ID is de-duplicated and only its first occurrence is used, so the array is treated as an ordered set.
- A column ID that is not present in the table returns error 8180.
- This API is disabled for white label portal contexts. Calls made through a custom portal domain fail.
- Obtain the column IDs from the Get Table Metadata API, excluding the system columns, and call it again afterwards to confirm the new column positions.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Reorder all columns in a 3-column table**

```http
PUT /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns/reorder HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"columns":["7617000000508027","7617000000508025","7617000000508026"]}
```

**Case 2 — Move the last column of a 4-column table to the first position**

```http
PUT /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns/reorder HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"columns":["7617000000508028","7617000000508025","7617000000508026","7617000000508027"]}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Reorder Columns](../../../sdk-examples/data-modeling-and-schema/columns/reorder-columns.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Reorder Columns returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Not available on custom domains** | This API is disabled for white label portal contexts. Calls made through a portal domain URL will fail. |
| **Full column set required** | Every non-system column ID in the table must be present in `columns`, or the request fails with error 8179 listing the missing IDs. Partial reordering is not supported. |
| **`columns` array order defines display order** | The position of each ID in the array becomes its new left-to-right display position (1-indexed internally). |
| **`columns` values are strings** | Column IDs must be quoted strings (e.g., `["7617000000508027"]`), not integers. |
| **Duplicate IDs are de-duplicated** | If the same column ID appears more than once, only its first occurrence is used; the array is treated as an ordered set. |
| **Column IDs must belong to the view** | Any column ID not present in the table returns error 8180. |
| **Verify result** | Use Get Table Metadata to confirm the new `columnOrder`/position values after calling this API. |
| **Dependency** | `<view-id>` → Get View List. `columns` array values → Get Table Metadata (use `columnId` strings, excluding system columns). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Design Modify permission on the view. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view ID does not belong to the specified workspace. | Confirm the `<view-id>` is correct. |
| [8179](../../../foundations/error-codes.md#error-8179) | 403 | One or more required (non-system) columns are missing from the `columns` array. | Include every non-system column ID of the table in `columns`, not just the ones being moved. |
| [8180](../../../foundations/error-codes.md#error-8180) | 403 | One or more column IDs in the `columns` array do not belong to this view. | Verify all column IDs using Get Table Metadata. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Columns overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Add Column](add-column.md), [Rename Column](rename-column.md), [Delete Column](delete-column.md), [Hide Columns](hide-columns.md), [Show Columns](show-columns.md), [Get Column Dependents](get-column-dependents.md), [Sort Data by Columns](sort-data-by-columns.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/columns/reorder-columns.md).
