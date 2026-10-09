---
type: API Endpoint
title: Get All Dashboards
description: Returns all dashboards accessible to the authenticated user - both those owned by the user and those shared with them - across every organization and workspace.
resource: https://analyticsapi.zoho.com/restapi/v2/dashboards
tags:
  - zoho-analytics
  - rest-api-v2
  - reports-and-dashboards
  - dashboards
  - get
  - metadata
api:
  operation_id: getDashboards
  method: GET
  path: "/restapi/v2/dashboards"
  domain: reports-and-dashboards
  group: dashboards
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: not-required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: The authenticated user must be any active Zoho Analytics user.
  error_codes:
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/reports-dashboards-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1dashboards/get"
    config_schema: null
    response_schema: GetDashboardsResponse
  sdk_examples: "/sdk-examples/reports-and-dashboards/dashboards/get-dashboards.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**GET `/restapi/v2/dashboards`** - Get All Dashboards (Dashboards / Reports & Dashboards).

> This API has no request body parameters. All context is derived from the OAuth token.

From the OpenAPI specification:

Returns all dashboards accessible to the authenticated user - both those owned by the user and those shared with them - across every organization and workspace. The response groups the results into two separate lists, `ownedViews` and `sharedViews`.

This API has no request parameters; all context is derived from the OAuth token. The authenticated user may be any active Zoho Analytics user.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getDashboards` |
| HTTP method | GET |
| URL | `/restapi/v2/dashboards` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | Not required (user-scoped API) |
| Permission required | The authenticated user must be any active Zoho Analytics user. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`reports-dashboards-grouped-api.json`](../../../references/openapi/reports-dashboards-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1dashboards/get`; response schema `GetDashboardsResponse` |

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

This is a user service level API - it returns dashboards across every organization the caller belongs to.
- The **ZANALYTICS-ORGID** header is not required.
- The OAuth token must be issued with user level scope.

Get Shared Dashboards is available on custom domains. Get All Dashboards and Get Owned Dashboards are disabled on custom domains. The workspace-scoped dashboard APIs are accessible on custom domains subject to additional permission checks.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success` or `failure`. |
| `summary` | string | Always `"Get all dashboards"` on success. |
| `data.ownedViews` | JSONArray | List of dashboards owned by the authenticated user. |
| `data.sharedViews` | JSONArray | List of dashboards shared with the authenticated user. |

Each item in `ownedViews` and `sharedViews` has the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `viewId` | string | Unique ID of the dashboard. |
| `viewName` | string | Display name of the dashboard. |
| `viewDesc` | string | Description of the dashboard. Empty string if none. |
| `viewType` | string | Always `"Dashboard"` for dashboard entries. |
| `parentViewId` | string | ID of the parent view, if any. Empty string if none. |
| `folderId` | string | ID of the folder containing the dashboard. |
| `createdTime` | string | Dashboard creation timestamp in epoch milliseconds. |
| `createdBy` | string | Email address of the dashboard owner/creator. |
| `lastModifiedTime` | string | Last modification timestamp in epoch milliseconds. |
| `lastModifiedBy` | string | Email address of the user who last modified the dashboard. |
| `isFavorite` | boolean | `true` if the dashboard is marked as a favorite by the requesting user. |
| `sharedBy` | string | Email of the user who shared this dashboard. Present in shared entries; empty string in owned entries. |
| `workspaceId` | string | ID of the workspace containing the dashboard. |
| `orgId` | string | ID of the organization the workspace belongs to. |

# Examples

## Sample Requests

**Case 1: Retrieve all dashboards for the authenticated user**

```http
GET /restapi/v2/dashboards HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

**Case 2: Same request from a different data center (EU)**

```http
GET /restapi/v2/dashboards HTTP/1.1
Host: analyticsapi.zoho.eu
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
```

## Sample Responses

**Case 1 – Success: user has both owned and shared dashboards**

```http
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8

{
  "status": "success",
  "summary": "Get all dashboards",
  "data": {
    "ownedViews": [
      {
        "viewId": "466206000000105001",
        "viewName": "Executive Sales Dashboard",
        "viewDesc": "High-level sales KPIs for the executive team",
        "viewType": "Dashboard",
        "parentViewId": "",
        "folderId": "466206000000071005",
        "createdTime": "1719820800000",
        "createdBy": "alice@example.com",
        "lastModifiedTime": "1722499200000",
        "lastModifiedBy": "alice@example.com",
        "isFavorite": true,
        "sharedBy": "",
        "workspaceId": "466206000000071000",
        "orgId": "700000123456"
      },
      {
        "viewId": "466206000000108003",
        "viewName": "Marketing Campaign Overview",
        "viewDesc": "",
        "viewType": "Dashboard",
        "parentViewId": "",
        "folderId": "466206000000071000",
        "createdTime": "1720080000000",
        "createdBy": "alice@example.com",
        "lastModifiedTime": "1720080000000",
        "lastModifiedBy": "alice@example.com",
        "isFavorite": false,
        "sharedBy": "",
        "workspaceId": "466206000000071000",
        "orgId": "700000123456"
      }
    ],
    "sharedViews": [
      {
        "viewId": "466206000000200010",
        "viewName": "Finance Overview",
        "viewDesc": "Finance team quarterly dashboard",
        "viewType": "Dashboard",
        "parentViewId": "",
        "folderId": "466206000000190001",
        "createdTime": "1718640000000",
        "createdBy": "bob@example.com",
        "lastModifiedTime": "1721001600000",
        "lastModifiedBy": "bob@example.com",
        "isFavorite": false,
        "sharedBy": "bob@example.com",
        "workspaceId": "466206000000190000",
        "orgId": "700000123456"
      }
    ]
  }
}
```

**Case 2 – Success: user has only owned dashboards (empty shared list)**

```json
{
  "status": "success",
  "summary": "Get all dashboards",
  "data": {
    "ownedViews": [
      {
        "viewId": "466206000000105001",
        "viewName": "Executive Sales Dashboard",
        "viewDesc": "High-level sales KPIs",
        "viewType": "Dashboard",
        "parentViewId": "",
        "folderId": "466206000000071005",
        "createdTime": "1719820800000",
        "createdBy": "alice@example.com",
        "lastModifiedTime": "1722499200000",
        "lastModifiedBy": "alice@example.com",
        "isFavorite": true,
        "sharedBy": "",
        "workspaceId": "466206000000071000",
        "orgId": "700000123456"
      }
    ],
    "sharedViews": []
  }
}
```

**Case 3 – Success: user has no dashboards at all**

```json
{
  "status": "success",
  "summary": "Get all dashboards",
  "data": {
    "ownedViews": [],
    "sharedViews": []
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get All Dashboards](../../../sdk-examples/reports-and-dashboards/dashboards/get-dashboards.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission to retrieve dashboards. | Ensure the request uses a valid OAuth token for an active Zoho Analytics user. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid OAuth token. | Provide a valid, non-expired OAuth token in the `Authorization` header. |

# Related

- [Dashboards overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Reports & Dashboards](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Dashboard](create-dashboard.md), [Read Dashboard Metadata](get-dashboard-metadata.md), [Update Dashboard](update-dashboard.md), [Get Owned Dashboards](get-owned-dashboards.md), [Get Shared Dashboards](get-shared-dashboards.md).
- [SDK examples](../../../sdk-examples/reports-and-dashboards/dashboards/get-dashboards.md).
