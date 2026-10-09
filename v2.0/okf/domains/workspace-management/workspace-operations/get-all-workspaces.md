---
type: API Endpoint
title: Get All Workspace List
description: "Returns all workspaces accessible to the authenticated user — both workspaces they own or administer, and workspaces shared with them."
resource: https://analyticsapi.zoho.com/restapi/v2/workspaces
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-operations
  - get
  - metadata
api:
  operation_id: getAllWorkspaces
  method: GET
  path: "/restapi/v2/workspaces"
  domain: workspace-management
  group: workspace-operations
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
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces/get"
    config_schema: null
    response_schema: GetAllWorkspacesResponse
  sdk_examples: "/sdk-examples/workspace-management/workspace-operations/get-all-workspaces.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces`** - Get All Workspace List (Workspace Operations / Workspace Management).

Returns all workspaces accessible to the authenticated user — both workspaces they own or administer, and workspaces shared with them. The response separates owned and shared workspaces into two distinct arrays.

This API is user-scoped: it returns only workspaces that the calling user has any level of access to — it does not return every workspace in the organisation. Account Admins see all workspaces in their org in the owned list.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getAllWorkspaces` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | Not required (user-scoped API) |
| Permission required | Any authenticated Zoho Analytics user. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces/get`; response schema `GetAllWorkspacesResponse` |

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

- This API combines the results of the Get Owned Workspace List and the Get Shared Workspace List APIs for the requesting user.
- The API is scoped to the user and not to the organization. It returns only the workspaces that the requesting user has some level of access to, across all the organizations. Account Admins see all the workspaces of their organization in the owned list.
- The **ZANALYTICS-ORGID** header is not required for this API.
- The **workspaceId** values returned by this API are the primary source of the workspace IDs used in all the workspace specific API calls.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `data.ownedWorkspaces` | Array | Workspaces where the calling user is the owner (Account Admin) or admin (Org Admin, Workspace Admin). Empty array if none. |
| `data.sharedWorkspaces` | Array | Workspaces from other organisations where views have been shared with the calling user, but the user does not administer the workspace. Empty array if none. |
| `workspaces[].workspaceId` | String | Unique workspace identifier. |
| `workspaces[].workspaceName` | String | Workspace display name. |
| `workspaces[].workspaceDesc` | String | Description. Empty string `""` if not set. |
| `workspaces[].orgId` | String | Organisation ID that owns this workspace. |
| `workspaces[].createdTime` | String | Unix timestamp (milliseconds) when the workspace was created. |
| `workspaces[].createdBy` | String | Email address of the user who created the workspace. |
| `workspaces[].isDefault` | Boolean | `true` if this is the organisation's default workspace. `false` for all other workspaces. |

# Examples

## Sample Requests

**Case 1 — Account Admin fetching all accessible workspaces**

```http
GET /restapi/v2/workspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

**Case 2 — Shared user fetching their workspace access list**

```http
GET /restapi/v2/workspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Account Admin (owns all org workspaces, none shared from other orgs)**
```json
{
  "status": "success",
  "summary": "Get all workspaces",
  "data": {
    "ownedWorkspaces": [
      {
        "workspaceId": "466206000000071000",
        "workspaceName": "Sales Analytics",
        "workspaceDesc": "Sales reporting workspace",
        "orgId": "700000123456",
        "createdTime": "1619175390377",
        "createdBy": "admin@acme.com",
        "isDefault": false
      },
      {
        "workspaceId": "466206000000080000",
        "workspaceName": "HR Analytics",
        "workspaceDesc": "",
        "orgId": "700000123456",
        "createdTime": "1622097563854",
        "createdBy": "admin@acme.com",
        "isDefault": false
      }
    ],
    "sharedWorkspaces": []
  }
}
```

**Case 2 — Shared user with access to workspaces in multiple orgs**
```json
{
  "status": "success",
  "summary": "Get all workspaces",
  "data": {
    "ownedWorkspaces": [
      {
        "workspaceId": "138022000000002015",
        "workspaceName": "My Personal Workspace",
        "workspaceDesc": "",
        "orgId": "700000999888",
        "createdTime": "1606987644675",
        "createdBy": "shareduser@example.com",
        "isDefault": false
      }
    ],
    "sharedWorkspaces": [
      {
        "workspaceId": "466206000000071000",
        "workspaceName": "Sales Analytics",
        "workspaceDesc": "Sales reporting workspace",
        "orgId": "700000123456",
        "createdTime": "1619175390377",
        "createdBy": "admin@acme.com",
        "isDefault": false
      }
    ]
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get All Workspace List](../../../sdk-examples/workspace-management/workspace-operations/get-all-workspaces.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Returns both owned and shared workspaces** | This API combines the results of Get Owned Workspace List and Get Shared Workspace List for the calling user. |
| **`ZANALYTICS-ORGID` not required** | This API does not require the org ID header because it returns workspaces scoped to the calling user's access, across any org they have access to. |
| **`isDefault` and `isFavourite` in response** | The response indicates whether each workspace is the user's current default or in their favourites list, as set by the Workspace Preferences APIs. |
| **Dependency for other APIs** | The `workspaceId` values returned here are the primary source for all workspace-specific API calls. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Workspace Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Workspace](create-workspace.md), [Copy Workspace](copy-workspace.md), [Rename Workspace](rename-workspace.md), [Delete Workspace](delete-workspace.md), [Export as Template](export-as-template.md), [Get Owned Workspace List](get-owned-workspaces.md), [Get Shared Workspace List](get-shared-workspaces.md), [Get Workspace Secret Key](get-workspace-secret-key.md), [Get Workspace Info](get-workspace-details.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-operations/get-all-workspaces.md).
