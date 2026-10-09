---
type: API Endpoint
title: Get View List
description: Returns a list of views accessible to the authenticated user within a specific workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - view-operations
  - get
  - metadata
api:
  operation_id: getViews
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views"
  domain: views-management
  group: view-operations
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: query
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or a Shared User, or a Group Member, or any user with Read permission on the workspace."
  error_codes:
    - 7103
    - 7301
    - 8119
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views/get"
    config_schema: GetViewListConfig
    response_schema: GetViewsResponse
  sdk_examples: "/sdk-examples/views-management/view-operations/get-views.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/views`** - Get View List (View Operations / Views Management).

Returns a list of views accessible to the authenticated user within a specific workspace. Supports filtering by view type, name keyword, created/modified by user, and pagination with sorting.

From the OpenAPI specification:

Returns a list of views accessible to the authenticated user within a specific workspace. Supports filtering by view type, name keyword, created/modified by user, and pagination with sorting.

The result can be narrowed by view type, by a keyword matched against the view name, and by the user who created or last modified the view, and it can be paged and sorted. The scope of the list depends on the caller: an admin receives every view in the workspace, while a shared user or group member receives only the views shared with them.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getViews` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/views` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organization ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or a Shared User, or a Group Member, or any user with Read permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - optional |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views/get`; CONFIG schema `GetViewListConfig`; response schema `GetViewsResponse` |

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

## CONFIG Parameter

The CONFIG parameter is optional. When provided, it is a JSON object passed as a **query parameter** named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `viewTypes` | JSONArray of Integer | No | All types | Filters the result to include only the specified view types. Each element must be an integer from the view type table below. When omitted, all view types accessible to the user are returned. Maximum 8 entries. |
| `keyword` | String | No | `null` | Filters views by a case-insensitive partial match on the view name. For example, `"Sales"` returns views whose names contain `"Sales"`. When omitted, no name filter is applied. |
| `startIndex` | Integer | No | `null` | Zero-based index of the first record to return. Used for pagination. When omitted, results start from index 0. |
| `noOfResult` | Integer | No | `null` | Maximum number of views to return. When omitted, all matching views are returned. Use in combination with `startIndex` to paginate through large workspaces. |
| `sortedColumn` | Integer | No | `0` | Column to sort results by. Allowed values: `0` = Name (default), `1` = Created time, `2` = Last modified time. Values outside `0–2` result in error **8119**. |
| `sortedOrder` | Integer | No | `0` | Sort direction. Allowed values: `0` = Ascending (default), `1` = Descending. Values outside `0–1` result in error **8119**. |
| `criteriaZuid` | Long | No | `null` | Filters views to only those created or last modified by the user with this ZUID (Zoho User ID). When omitted, views from all users are returned. Use this to view a specific user's contributions within a workspace. |

### View Type Reference

| Integer | `viewType` in Response | Description |
|---------|----------------------|-------------|
| `0` | `Table` | Base data table |
| `1` | `Report` | Tabular view (grid-style report) |
| `2` | `AnalysisView` | Chart / analysis view |
| `3` | `Pivot` | Pivot table |
| `4` | `SummaryView` | Summary view |
| `5` | `TableView` | Custom tabular view |
| `6` | `QueryTable` | Query / SQL-based virtual table |
| `7` | `Dashboard` | Dashboard (includes tabbed dashboards) |
| `9` | `Tab` | A tab within a tabbed dashboard |

## Notes from the OpenAPI specification

- The CONFIG parameter is optional. Without it, every view accessible to the calling user is returned. As this is a GET request, the value must be stringified and URL encoded before it is sent.
- Each integer in **viewTypes** corresponds to the **viewType** string of the same name in the response - 0 Table, 1 Report, 2 AnalysisView, 3 Pivot, 4 SummaryView, 5 TableView, 6 QueryTable, 7 Dashboard, 9 Tab. At most 8 entries are accepted.
- A **sortedColumn** outside 0 to 2, or a **sortedOrder** outside 0 to 1, fails with error 8119.
- A filter that matches nothing - an excluded view type, an unmatched keyword, a **startIndex** past the end of the result set, or a **criteriaZuid** with no views in the workspace - returns HTTP 200 with an empty **views** array. No error is raised.
- A shared user sees only the views shared explicitly with them, and a group member additionally sees the views shared with their group. **sharedBy** names the user who shared each view, and is an empty string for Workspace, Account and Organization Admins.
- **isFavorite** is user specific. It reflects whether the requesting user has marked the view as a favorite, not a global property of the view.
- **parentViewId** holds the ID of the base table for an analysis view, and is an empty string for tables and dashboards.
- Dashboard tabs are returned as entries of their own when **viewTypes** includes 9, each carrying **parentViewId** set to its parent dashboard. Send **viewTypes** as [7] to get the dashboard entries alone.
- **lastModifiedTime** covers both data changes and design changes.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `viewId` | String | Unique identifier of the view. |
| `viewName` | String | Display name of the view. |
| `viewDesc` | String | Description of the view. Empty string if none. |
| `viewType` | String | Type of the view. See View Type Reference table above. |
| `parentViewId` | String | ID of the parent table for analysis views. Empty string for Tables and Dashboards. |
| `folderId` | String | ID of the folder containing this view within the workspace. |
| `createdTime` | String | Creation timestamp in epoch milliseconds. |
| `createdBy` | String | Email address of the user who created the view. |
| `lastModifiedTime` | String | Last modification timestamp in epoch milliseconds (covers both data and design changes). |
| `lastModifiedBy` | String | Email address of the user who last modified the view. |
| `isFavorite` | Boolean | `true` if the requesting user has marked this view as a favourite. User-specific. |
| `sharedBy` | String | Email of the user who shared the view with the current user. Empty string for Workspace Admins and Account/Org Admins. |

# Examples

## Sample Requests

**Case 1 — Get all views (no filter)**

```http
GET /restapi/v2/workspaces/466206000000071000/views HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Get only dashboards and tables, sorted by last modified time (newest first)**

```http
GET /restapi/v2/workspaces/466206000000071000/views?CONFIG={"viewTypes":[7,0],"sortedColumn":2,"sortedOrder":1} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — Keyword search with pagination**

```http
GET /restapi/v2/workspaces/466206000000071000/views?CONFIG={"keyword":"Revenue","startIndex":0,"noOfResult":10,"sortedColumn":0,"sortedOrder":0} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 4 — Get views created or modified by a specific user**

```http
GET /restapi/v2/workspaces/466206000000071000/views?CONFIG={"criteriaZuid":64035928,"sortedColumn":1,"sortedOrder":1} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Mixed view types (Admin user)**
```json
{
  "status": "success",
  "summary": "Get views",
  "data": {
    "views": [
      {
        "viewId": "137687000000471835",
        "viewName": "Sales",
        "viewDesc": "",
        "viewType": "Table",
        "parentViewId": "",
        "folderId": "137687000000471834",
        "createdTime": "1619175390377",
        "createdBy": "admin@example.com",
        "lastModifiedTime": "1683178935825",
        "lastModifiedBy": "admin@example.com",
        "isFavorite": false,
        "sharedBy": ""
      },
      {
        "viewId": "137687000000471836",
        "viewName": "Average Sales in a Day",
        "viewDesc": "",
        "viewType": "AnalysisView",
        "parentViewId": "137687000000471835",
        "folderId": "137687000000471834",
        "createdTime": "1619175390377",
        "createdBy": "admin@example.com",
        "lastModifiedTime": "1619175390377",
        "lastModifiedBy": "admin@example.com",
        "isFavorite": false,
        "sharedBy": ""
      },
      {
        "viewId": "137687000000471844",
        "viewName": "Dashboard",
        "viewDesc": "",
        "viewType": "Dashboard",
        "parentViewId": "",
        "folderId": "137687000000471834",
        "createdTime": "1619175390377",
        "createdBy": "admin@example.com",
        "lastModifiedTime": "1619175390377",
        "lastModifiedBy": "admin@example.com",
        "isFavorite": false,
        "sharedBy": ""
      }
    ]
  }
}
```

**Case 2 — Shared user response (only views shared with that user)**
```json
{
  "status": "success",
  "summary": "Get views",
  "data": {
    "views": [
      {
        "viewId": "137687000000471835",
        "viewName": "Sales",
        "viewDesc": "",
        "viewType": "Table",
        "parentViewId": "",
        "folderId": "137687000000471834",
        "createdTime": "1619175390377",
        "createdBy": "admin@example.com",
        "lastModifiedTime": "1683178935825",
        "lastModifiedBy": "admin@example.com",
        "isFavorite": false,
        "sharedBy": "admin@example.com"
      }
    ]
  }
}
```

> **Note on `sharedBy`:** For Workspace Admins and Account/Org Admins, `sharedBy` is always empty (`""`). For Shared Users and Group Members, `sharedBy` contains the email address of the user who explicitly shared the view with them.

> **Note on `isFavorite`:** This field is user-specific. It reflects whether the requesting user has marked this view as a favourite. It is not a global property of the view.

> **Note on `parentViewId`:** For analysis views (charts, pivots, summaries), this is the ID of the base table the view is built on. For tables and dashboards, it is an empty string (`""`).

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get View List](../../../sdk-examples/views-management/view-operations/get-views.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission to list views in this workspace. | Ensure the user has at least Read permission on the workspace. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | Invalid value for `sortedColumn` (must be 0–2) or `sortedOrder` (must be 0–1). | Use only the documented integer values for sort parameters. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [View Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Save As View](save-as-view.md), [Copy Views](copy-views.md), [Create Similar Views](create-similar-views.md), [Rename View](rename-view.md), [Delete View](delete-view.md), [Get View Details](get-view-details.md), [Get View URL](get-view-url.md), [Get View Dependents](get-view-dependents.md), [Get Recent Views](get-recent-views.md).
- [SDK examples](../../../sdk-examples/views-management/view-operations/get-views.md).
