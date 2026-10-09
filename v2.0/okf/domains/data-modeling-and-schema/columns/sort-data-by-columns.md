---
type: API Endpoint
title: Sort Data by Columns
description: Sets the default sort order for the rows of the specified table.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data/sort"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - columns
  - put
  - modeling
api:
  operation_id: sortDataByColumns
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data/sort"
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
    - 8119
    - 8180
    - 8182
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1data~1sort/put"
    config_schema: SortDataByColumnsConfig
    response_schema: null
  sdk_examples: "/sdk-examples/data-modeling-and-schema/columns/sort-data-by-columns.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**PUT `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data/sort`** - Sort Data by Columns (Columns / Data Modeling & Schema).

Sets the default sort order for rows in the specified table view. Supports two operational modes:

- **Set sort:** Provide a `columns` array (column IDs) and a `sortOrder` to apply ascending or descending sort by the specified columns.
- **Reset sort:** Provide `resetSort: true` to clear all current sort settings on the table.

> **Not available in custom-domain (White Label) contexts.** This API cannot be called via a portal domain URL. It is only accessible through the standard `analyticsapi.zoho.com` host.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `sortDataByColumns` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data/sort` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1data~1sort/put`; CONFIG schema `SortDataByColumnsConfig` |

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
| `columns` | JSONArray of String | **Yes** (when setting sort) | 300 | — | Ordered array of column IDs (as strings) to sort by. The first ID is the primary sort key, subsequent IDs are secondary sort keys. |
| `sortOrder` | Integer | **Yes** (when setting sort) | — | — | Sort direction applied to **all** columns in the `columns` array. `1` = Ascending (A→Z, 0→9). `2` = Descending (Z→A, 9→0). |
| `resetSort` | Boolean | **Yes** (when resetting) | — | `false` | If `true`, clears all sort settings on the table. Must **not** be combined with `sortOrder` or `columns` — doing so returns error 8182. |

> **`sortOrder` values:** Only `1` (Ascending) and `2` (Descending) are valid. Any other integer returns error 8119.

> **`resetSort` vs sort fields:** `resetSort: true` and `sortOrder` are mutually exclusive. Including both in the same request returns error 8182.

## Notes from the OpenAPI specification

- This API returns HTTP 204 No Content with no response body on success. There is no status or summary key to parse - treat the HTTP status code as the sole success indicator.
- This API is disabled for white label portal contexts. Calls made through a custom portal domain fail.
- The sortOrder value applies uniformly to every column in the columns array. Sorting different columns in different directions is not supported through this API - use a report or a query table configuration instead.
- The order of the columns array defines the sort priority. The first column ID is the primary sort key and the remaining IDs are the secondary and tertiary keys.
- Column IDs must be sent as quoted strings, not as integers.
- Sending resetSort together with sortOrder or columns returns error 8182 and no change is made. After a reset, every column reports sortedOrder as 0 and sortedIndex as -1.
- A column ID that is not present in the table returns error 8180.
- Use the Get Table Metadata API afterwards to confirm the sortedOrder and sortedIndex values of the affected columns.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Sort by a single column ascending**

```http
PUT /restapi/v2/workspaces/466206000000071000/views/7617000000508001/data/sort HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"columns":["7617000000508025"],"sortOrder":1}
```

**Case 2 — Sort by multiple columns (primary: Date descending, secondary: Region ascending)**

> Note: When multiple columns are in `columns`, the same `sortOrder` applies to all. To sort different columns in different directions, this is not supported in a single call. Use a query table or report for mixed sort directions.

```http
PUT /restapi/v2/workspaces/466206000000071000/views/7617000000508001/data/sort HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"columns":["7617000000508025","7617000000508026"],"sortOrder":2}
```

**Case 3 — Reset all sort settings**

```http
PUT /restapi/v2/workspaces/466206000000071000/views/7617000000508001/data/sort HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"resetSort":true}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Sort Data by Columns](../../../sdk-examples/data-modeling-and-schema/columns/sort-data-by-columns.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Sort Data by Columns returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Not available on custom domains** | This API is disabled for white label portal contexts. Calls made through a portal domain URL will fail. |
| **`sortOrder` applies to all columns uniformly** | All columns in the `columns` array are sorted in the same direction. Mixed sort directions (e.g., column A ascending, column B descending) are not supported via this API. |
| **`columns` array order defines sort priority** | The first column ID is the primary sort key; subsequent IDs are secondary, tertiary, etc. |
| **`columns` values are strings** | Column IDs must be quoted strings (e.g., `["7617000000508025"]`), not integers. |
| **`resetSort: true` with `sortOrder` is invalid** | Including both `resetSort: true` and `sortOrder` in the same CONFIG returns error 8182 before any changes are made. |
| **Column IDs must belong to the view** | Any column ID not present in the table returns error 8180. |
| **Verify result** | Use Get Table Metadata to confirm `sortedOrder` and `sortedIndex` values on the affected columns after calling this API. |
| **Dependency** | `<view-id>` → Get View List. `columns` array values → Get Table Metadata (use `columnId` strings). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Design Modify permission on the view. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view ID does not belong to the specified workspace. | Confirm the `<view-id>` is correct. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | Invalid value for `sortOrder`. Only `1` (Ascending) and `2` (Descending) are accepted. | Use `1` for ascending or `2` for descending. |
| [8180](../../../foundations/error-codes.md#error-8180) | 403 | One or more column IDs in the `columns` array do not belong to this view. | Verify all column IDs using Get Table Metadata. |
| [8182](../../../foundations/error-codes.md#error-8182) | 403 | `resetSort: true` and `sortOrder` cannot be used together. | Use either `resetSort: true` (with no other fields) or `columns` + `sortOrder` (without `resetSort`). |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Columns overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Add Column](add-column.md), [Rename Column](rename-column.md), [Delete Column](delete-column.md), [Hide Columns](hide-columns.md), [Show Columns](show-columns.md), [Get Column Dependents](get-column-dependents.md), [Reorder Columns](reorder-columns.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/columns/sort-data-by-columns.md).
