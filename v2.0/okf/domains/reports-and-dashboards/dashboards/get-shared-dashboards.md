---
type: API Endpoint
title: Get Shared Dashboards
description: "Returns all dashboards that have been shared with the authenticated user across every organization and workspace, as a single views array."
resource: https://analyticsapi.zoho.com/restapi/v2/dashboards/shared
tags:
  - zoho-analytics
  - rest-api-v2
  - reports-and-dashboards
  - dashboards
  - get
  - metadata
api:
  operation_id: getSharedDashboards
  method: GET
  path: "/restapi/v2/dashboards/shared"
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
    pointer: "#/paths/~1restapi~1v2~1dashboards~1shared/get"
    config_schema: null
    response_schema: GetDashboardListResponse
  sdk_examples: "/sdk-examples/reports-and-dashboards/dashboards/get-shared-dashboards.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

**GET `/restapi/v2/dashboards/shared`** - Get Shared Dashboards (Dashboards / Reports & Dashboards).

> This API has no request body parameters. All context is derived from the OAuth token.

From the OpenAPI specification:

Returns all dashboards that have been shared with the authenticated user across every organization and workspace, as a single `views` array. Unlike Get All Dashboards, this endpoint returns only shared dashboards, and it is also available on custom domains.

This API has no request parameters; all context is derived from the OAuth token. The authenticated user may be any active Zoho Analytics user.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getSharedDashboards` |
| HTTP method | GET |
| URL | `/restapi/v2/dashboards/shared` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | Not required (user-scoped API) |
| Permission required | The authenticated user must be any active Zoho Analytics user. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`reports-dashboards-grouped-api.json`](../../../references/openapi/reports-dashboards-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1dashboards~1shared/get`; response schema `GetDashboardListResponse` |

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
| `summary` | string | Always `"Get shared dashboards"` on success. |
| `data.views` | JSONArray | List of dashboards shared with the authenticated user. Each item follows the same field structure as in [Get All Dashboards](get-dashboards.md) (see [Response Field Reference — per-dashboard item](get-dashboards.md)). The `sharedBy` field is always populated for shared dashboards. |

# Examples

## Sample Requests

**Case 1: Retrieve all dashboards shared with the authenticated user**

```http
GET /restapi/v2/dashboards/shared HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

**Case 2: Same request on a custom domain**

```http
GET /restapi/v2/dashboards/shared HTTP/1.1
Host: analytics.example.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

## Sample Responses

**Case 1 – Success: user has multiple shared dashboards**

```http
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8

{
  "status": "success",
  "summary": "Get shared dashboards",
  "data": {
    "views": [
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
      },
      {
        "viewId": "466206000000410055",
        "viewName": "Supply Chain Dashboard",
        "viewDesc": "Inventory and logistics metrics",
        "viewType": "Dashboard",
        "parentViewId": "",
        "folderId": "466206000000400000",
        "createdTime": "1714780800000",
        "createdBy": "carol@example.com",
        "lastModifiedTime": "1719993600000",
        "lastModifiedBy": "carol@example.com",
        "isFavorite": true,
        "sharedBy": "carol@example.com",
        "workspaceId": "466206000000400000",
        "orgId": "700000998877"
      }
    ]
  }
}
```

**Case 2 – Success: user has one shared dashboard marked as favorite**

```json
{
  "status": "success",
  "summary": "Get shared dashboards",
  "data": {
    "views": [
      {
        "viewId": "466206000000200010",
        "viewName": "Regional Sales Tracker",
        "viewDesc": "Sales performance by region",
        "viewType": "Dashboard",
        "parentViewId": "",
        "folderId": "466206000000190000",
        "createdTime": "1720512000000",
        "createdBy": "dave@example.com",
        "lastModifiedTime": "1722067200000",
        "lastModifiedBy": "dave@example.com",
        "isFavorite": true,
        "sharedBy": "dave@example.com",
        "workspaceId": "466206000000190000",
        "orgId": "700000123456"
      }
    ]
  }
}
```

**Case 3 – Success: no dashboards have been shared with the user**

```json
{
  "status": "success",
  "summary": "Get shared dashboards",
  "data": {
    "views": []
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Shared Dashboards](../../../sdk-examples/reports-and-dashboards/dashboards/get-shared-dashboards.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission to retrieve shared dashboards. | Ensure the request uses a valid OAuth token for an active Zoho Analytics user. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid OAuth token. | Provide a valid, non-expired OAuth token in the `Authorization` header. |

# Related

- [Dashboards overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Reports & Dashboards](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Dashboard](create-dashboard.md), [Read Dashboard Metadata](get-dashboard-metadata.md), [Update Dashboard](update-dashboard.md), [Get All Dashboards](get-dashboards.md), [Get Owned Dashboards](get-owned-dashboards.md).
- [SDK examples](../../../sdk-examples/reports-and-dashboards/dashboards/get-shared-dashboards.md).
