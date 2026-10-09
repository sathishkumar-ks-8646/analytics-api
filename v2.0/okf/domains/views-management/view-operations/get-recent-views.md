---
type: API Endpoint
title: Get Recent Views
description: "Returns the views most recently accessed by the authenticated user, ordered with the most recent first."
resource: https://analyticsapi.zoho.com/restapi/v2/recentviews
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - view-operations
  - get
  - metadata
api:
  operation_id: getRecentViews
  method: GET
  path: "/restapi/v2/recentviews"
  domain: views-management
  group: view-operations
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: not-required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: Any authenticated Zoho Analytics user.
  error_codes:
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1recentviews/get"
    config_schema: null
    response_schema: GetRecentViewsResponse
  sdk_examples: "/sdk-examples/views-management/view-operations/get-recent-views.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**GET `/restapi/v2/recentviews`** - Get Recent Views (View Operations / Views Management).

Returns a list of views recently accessed by the authenticated user across **all workspaces** the user has access to, sorted by access time (most recently accessed first). This is a user-scoped, cross-workspace API — no workspace ID is required in the URL.

> This API has no CONFIG parameter. Results are personal to the calling user — different users calling this API see their own respective recent view history.

From the OpenAPI specification:

Returns the views most recently accessed by the authenticated user, ordered with the most recent first.

The API is user-scoped and spans workspaces: views from every workspace and organization the user can reach are returned together in one list, each carrying the workspace it belongs to. No workspace ID is needed in the URL, and the history returned is personal to the token used to make the call.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getRecentViews` |
| HTTP method | GET |
| URL | `/restapi/v2/recentviews` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | Not required (user-scoped API) - this API is user-scoped and not tied to a single workspace or organisation. |
| Permission required | Any authenticated Zoho Analytics user. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1recentviews/get`; response schema `GetRecentViewsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | - | Not required | This API is user-scoped and works across all organizations of the caller. |

## Path Parameters

This endpoint has no path parameters.

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- This API has no CONFIG parameter and takes no workspace ID. **ZANALYTICS-ORGID** is not required either, because the API is user-scoped rather than tied to one workspace or organization.
- The result is strictly per user. Two different OAuth tokens return two different histories, each belonging to the user the token was issued for.
- Views from every workspace and organization the user can reach are returned in a single list. **workspaceId** and **workspaceName** tell them apart.
- The list is ordered by **viewLastAccessedTime** descending, so the most recently opened view comes first.
- Only views that are currently active and currently accessible are returned. A view deleted after it was accessed, or one later unshared from the user, drops out of the list.
- A user with no view history receives HTTP 200 with an empty **views** array.
- **viewLastAccessedTime** is an epoch timestamp in milliseconds returned as a string. Divide it by 1000 to obtain epoch seconds.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `data.views` | Array | List of recently accessed views, sorted by `viewLastAccessedTime` descending (most recent first). Empty array if the user has no recent view history. |
| `views[].viewId` | String | Unique ID of the view. |
| `views[].viewName` | String | Display name of the view. |
| `views[].viewType` | String | View type string (same format as Get View List API). |
| `views[].workspaceId` | String | ID of the workspace containing this view. |
| `views[].workspaceName` | String | Display name of the workspace. Useful for disambiguation when views from multiple workspaces appear in the result. |
| `views[].viewLastAccessedTime` | String | Epoch milliseconds timestamp of when the calling user last accessed this view. |

# Examples

## Sample Requests

**Case 1 — Get my recent views**

```http
GET /restapi/v2/recentviews HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

**Case 2 — Same API, shared user context (only sees views shared with them)**

```http
GET /restapi/v2/recentviews HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Workspace Admin with mixed view types across workspaces**
```json
{
  "status": "success",
  "summary": "Get recent views",
  "data": {
    "views": [
      {
        "viewId": "137687000000005744",
        "viewName": "Column Sales",
        "viewType": "Table",
        "workspaceId": "137687000000005620",
        "workspaceName": "Q3 Sales Workspace",
        "viewLastAccessedTime": "1623165599255"
      },
      {
        "viewId": "137687000001859027",
        "viewName": "tabular_1",
        "viewType": "Report",
        "workspaceId": "137687000001859022",
        "workspaceName": "DBOwner-Backup",
        "viewLastAccessedTime": "1622797899143"
      },
      {
        "viewId": "137687000001859035",
        "viewName": "dashboard1",
        "viewType": "Dashboard",
        "workspaceId": "137687000001859022",
        "workspaceName": "DBOwner-Backup",
        "viewLastAccessedTime": "1622741330331"
      },
      {
        "viewId": "137687000001859030",
        "viewName": "summary",
        "viewType": "SummaryView",
        "workspaceId": "137687000001859022",
        "workspaceName": "DBOwner-Backup",
        "viewLastAccessedTime": "1622741297744"
      },
      {
        "viewId": "137687000001859029",
        "viewName": "pivot1",
        "viewType": "Pivot",
        "workspaceId": "137687000001859022",
        "workspaceName": "DBOwner-Backup",
        "viewLastAccessedTime": "1622741261238"
      }
    ]
  }
}
```

**Case 2 — Shared user (only sees views accessible to them)**
```json
{
  "status": "success",
  "summary": "Get recent views",
  "data": {
    "views": [
      {
        "viewId": "138022000000002005",
        "viewName": "Sales",
        "viewType": "Table",
        "workspaceId": "138022000000002015",
        "workspaceName": "SharedUser Sales",
        "viewLastAccessedTime": "1607076349147"
      },
      {
        "viewId": "138022000000002105",
        "viewName": "Cost Across Years by Region",
        "viewType": "AnalysisView",
        "workspaceId": "138022000000002015",
        "workspaceName": "SharedUser Sales",
        "viewLastAccessedTime": "1606987675756"
      }
    ]
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Recent Views](../../../sdk-examples/views-management/view-operations/get-recent-views.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [View Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Save As View](save-as-view.md), [Copy Views](copy-views.md), [Create Similar Views](create-similar-views.md), [Rename View](rename-view.md), [Delete View](delete-view.md), [Get View List](get-views.md), [Get View Details](get-view-details.md), [Get View URL](get-view-url.md), [Get View Dependents](get-view-dependents.md).
- [SDK examples](../../../sdk-examples/views-management/view-operations/get-recent-views.md).
