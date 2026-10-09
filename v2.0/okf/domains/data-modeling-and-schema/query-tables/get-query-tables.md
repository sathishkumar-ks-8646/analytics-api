---
type: API Endpoint
title: Get Query Tables
description: Returns the list of query tables in the specified workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/querytables"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - query-tables
  - get
  - metadata
api:
  operation_id: getQueryTables
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/querytables"
  domain: data-modeling-and-schema
  group: query-tables
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: query
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Query Table permission on the workspace."
  error_codes:
    - 7301
    - 8119
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1querytables/get"
    config_schema: GetQueryTablesConfig
    response_schema: GetQueryTablesResponse
  sdk_examples: "/sdk-examples/data-modeling-and-schema/query-tables/get-query-tables.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/querytables`** - Get Query Tables (Query Tables / Data Modeling & Schema).

Returns a paginated, filterable, sortable list of all query tables in the workspace.

From the OpenAPI specification:

Returns the list of query tables in the specified workspace. The list can be filtered by name or by creator, sorted, and paginated through the CONFIG parameter.

The view IDs returned by this API are the entry point for the Edit Query Table and the Get Query Table Details APIs.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getQueryTables` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/querytables` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Query Table permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - optional |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1querytables/get`; CONFIG schema `GetQueryTablesConfig`; response schema `GetQueryTablesResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

CONFIG is optional for this API — omitting it returns the full, unfiltered, default-sorted list.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `keyword` | String | No | — | Filters the list to query tables whose name contains this keyword (case-insensitive substring match). |
| `startIndex` | Integer | No | `1` | 1-based index of the first record to return, for pagination. |
| `noOfResult` | Integer | No | `20` | Number of records to return per page. Only applied when `startIndex` is also provided. |
| `sortedColumn` | Integer (enum) | No | `0` | Column to sort by. See [Sort Column Values](#sort-column-values) below. Valid range: `0`–`2`. |
| `sortedOrder` | Integer (enum) | No | `0` | Sort direction. See [Sort Order Values](#sort-order-values) below. Valid range: `0`–`1`. |
| `criteriaZuid` | Long | No | — | Filters the list to query tables created by the specified user (Zoho User ID). |

### Sort Column Values

| `sortedColumn` Value | Sorts By |
|-----------------------|----------|
| `0` (default) | Display name (alphabetical) |
| `1` | Created time |
| `2` | Last modified time |

### Sort Order Values

| `sortedOrder` Value | Direction |
|------------------------|-----------|
| `0` (default) | Ascending |
| `1` | Descending |

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `viewId` | String | Unique ID of the query table. Use this as `<querytable-id>` in Edit/Get Details APIs. |
| `viewName` | String | Display name of the query table. |
| `viewDesc` | String | Description of the query table. Empty string if not set. |
| `viewType` | String | Always `"QueryTable"` for entries in this list. |
| `parentViewId` | String | Empty for query tables (no parent view concept applies). |
| `folderId` | String | ID of the folder containing this query table. |
| `createdTime` | String | Epoch milliseconds when the query table was created. |
| `createdBy` | String | Email address of the creator. |
| `lastModifiedTime` | String | Epoch milliseconds of the last design modification. |
| `lastModifiedBy` | String | Email address of the last modifier. |
| `isFavorite` | Boolean | Whether the calling user has marked this query table as a favourite. |
| `sharedBy` | String | Email of the user who shared this query table with the caller, if applicable. Empty if owned by the caller. |
| `workspaceId` | String | ID of the workspace. |
| `orgId` | String | ID of the organisation. |

## Notes from the OpenAPI specification

- CONFIG is entirely optional. Omitting it returns the full list of query tables, up to the default page size, sorted by name in ascending order.
- Pagination needs both startIndex and noOfResult. Sending noOfResult on its own has no effect.
- sortedColumn and sortedOrder are strict enumerations. A value outside 0 to 2 for sortedColumn, or outside 0 to 1 for sortedOrder, returns error 8119.
- The keyword filter matches the display name only. It does not match the description or the text of the SQL query.
- The viewId values of this response are used as the querytable-id path parameter of the Edit Query Table and the Get Query Table Details APIs, so no separate ID resolution call is needed.

# Examples

## Sample Requests

**Case 1 — Get all query tables (no filters)**

```http
GET /restapi/v2/workspaces/20868000000040672/querytables HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Search by keyword, sorted by last modified time, descending**

```http
GET /restapi/v2/workspaces/20868000000040672/querytables HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"keyword":"Sales","sortedColumn":2,"sortedOrder":1}
```

**Case 3 — Paginated request (page 2, 10 per page)**

```http
GET /restapi/v2/workspaces/20868000000040672/querytables HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"startIndex":11,"noOfResult":10}
```

## Sample Responses

**HTTP 200 OK**

```json
{
  "status": "success",
  "summary": "Get query tables",
  "data": {
    "queryTables": [
      {
        "viewId": "20868000000040794",
        "viewName": "Multi_Table",
        "viewDesc": "",
        "viewType": "QueryTable",
        "parentViewId": "",
        "folderId": "20868000000041715",
        "createdTime": "1781069354934",
        "createdBy": "sales.admin@zylker.com",
        "lastModifiedTime": "1781069400680",
        "lastModifiedBy": "sales.admin@zylker.com",
        "isFavorite": false,
        "sharedBy": "",
        "workspaceId": "20868000000040672",
        "orgId": "700000123456"
      },
      {
        "viewId": "20868000000040782",
        "viewName": "Regional_Sales_QT",
        "viewDesc": "",
        "viewType": "QueryTable",
        "parentViewId": "",
        "folderId": "20868000000041715",
        "createdTime": "1781069354934",
        "createdBy": "sales.admin@zylker.com",
        "lastModifiedTime": "1781069417733",
        "lastModifiedBy": "sales.admin@zylker.com",
        "isFavorite": false,
        "sharedBy": "",
        "workspaceId": "20868000000040672",
        "orgId": "700000123456"
      }
    ]
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Query Tables](../../../sdk-examples/data-modeling-and-schema/query-tables/get-query-tables.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **CONFIG is optional** | Omitting CONFIG entirely returns the full list of query tables (up to the default page size) sorted by name ascending. |
| **`noOfResult` only applies with `startIndex`** | Providing `noOfResult` alone without `startIndex` has no pagination effect; both must be supplied together to page through results. |
| **`sortedColumn` and `sortedOrder` are strict enums** | Values outside `0`–`2` for `sortedColumn` or `0`–`1` for `sortedOrder` return error 8119. |
| **`keyword` matches only the display name** | Substring search does not match the description or SQL query text. |
| **Dependency** | `viewId` values from this response are used as `<querytable-id>` for Edit Query Table and Get Query Table Details. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Create Query Table permission on the workspace. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | Invalid value for `sortedColumn` or `sortedOrder`. | Use `0`–`2` for `sortedColumn` and `0`–`1` for `sortedOrder`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Query Tables overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Query Table](create-query-table.md), [Edit Query Table](edit-query-table.md), [Get Query Table Details](get-query-table-details.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/query-tables/get-query-tables.md).
