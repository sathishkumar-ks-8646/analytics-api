---
type: API Endpoint
title: Get Workspace Info
description: Returns the metadata of the specified workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-operations
  - get
  - metadata
api:
  operation_id: getWorkspaceDetails
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}"
  domain: workspace-management
  group: workspace-operations
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: not-required
  config_parameter:
    location: query
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be a Workspace Admin, or a Shared User, or a Group Member of the workspace, or any user with at least Read permission on a view within the workspace. Account Admins and Organization Admins also have access."
  error_codes:
    - 7103
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}/get"
    config_schema: GetWorkspaceInfoConfig
    response_schema: GetWorkspaceDetailsResponse
  sdk_examples: "/sdk-examples/workspace-management/workspace-operations/get-workspace-details.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}`** - Get Workspace Info (Workspace Operations / Workspace Management).

Returns metadata for the specified workspace. The calling user must have at least some level of access to the workspace (Workspace Admin, or any view in the workspace shared with them). An optional `withUserRoleInfo` flag enriches the response with the calling user's role details within the workspace.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getWorkspaceDetails` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | Not required (user-scoped API) |
| Permission required | The authenticated user must be a Workspace Admin, or a Shared User, or a Group Member of the workspace, or any user with at least Read permission on a view within the workspace. Account Admins and Organization Admins also have access. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - optional |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}/get`; CONFIG schema `GetWorkspaceInfoConfig`; response schema `GetWorkspaceDetailsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | - | Not required | This API is user-scoped and works across all organizations of the caller. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | The ID of the workspace. It can be obtained using any of the workspace list APIs. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameter

CONFIG is optional.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `withUserRoleInfo` | Boolean | No | `false` | When `false` (default): returns only workspace metadata. When `true`: additionally includes a `userRoleInfo` object in the response describing the calling user's role within the workspace — their role name, role ID, and whether they are assigned a custom role. |

## Notes from the OpenAPI specification

- The **data.workspaces** key of the response holds a single JSONObject and not a JSONArray. This differs from the Get All, the Get Owned and the Get Shared Workspace List APIs.
- Setting **withUserRoleInfo** to false, which is the default, returns the workspace metadata alone and is the fastest response option.
- Setting **withUserRoleInfo** to true adds the **userRoleInfo** object to the response. An Account Admin gets the role name Account Admin with roleId 0 and isCustomRoleUser false, an Organization Admin gets the role name Organization Admin with roleId 0, and a custom role user gets isCustomRoleUser true along with the ID and the display name of the custom role. For a shared user with no workspace level role, the role name may reflect their view level access role.
- The workspace secret key is not returned by this API. Use the Get Workspace Secret Key API to retrieve it.
- This API is available to any user who has at least one view of the workspace shared with them, in addition to the Workspace Admins, the Account Admins and the Organization Admins.
- The **ZANALYTICS-ORGID** header is not required for this API, as the organization is resolved from the workspace ID.
- As this is a GET request, the CONFIG value should be stringified and URL encoded before it is sent.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `data.workspaces` | Object | A single workspace info object. |
| `workspaces.workspaceId` | String | Unique workspace identifier. |
| `workspaces.workspaceName` | String | Display name of the workspace. |
| `workspaces.workspaceDesc` | String | Description. Empty string `""` if not set. |
| `workspaces.createdTime` | String | Unix timestamp (milliseconds) of workspace creation. |
| `workspaces.createdBy` | String | Email of the user who created the workspace. |
| `workspaces.orgId` | String | Organisation ID that owns this workspace. |
| `workspaces.userRoleInfo` | Object | *(Present only when `withUserRoleInfo=true`.)* The calling user's role details within this workspace. |
| `userRoleInfo.isCustomRoleUser` | Boolean | `true` if the calling user is assigned a custom role in this workspace. `false` for standard roles. |
| `userRoleInfo.roleId` | Number | Numeric identifier of the user's role. `0` for standard org roles (Account Admin, Org Admin, etc.). Non-zero for custom roles. |
| `userRoleInfo.roleName` | String | Display name of the calling user's role. Examples: `"Account Admin"`, `"Organization Admin"`, `"Workspace Admin"`, `"User"`, `"Viewer"`, or a custom role name. |

# Examples

## Sample Requests

**Case 1 — Basic workspace info (no role info)**

```http
GET /restapi/v2/workspaces/466206000000071000 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

**Case 2 — With calling user's role info**

```http
GET /restapi/v2/workspaces/466206000000071000 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
Content-Type: application/x-www-form-urlencoded

CONFIG={"withUserRoleInfo":true}
```

**Case 3 — Client Portal / White Label user getting workspace info**

```http
GET /restapi/v2/workspaces/38190000004180410 HTTP/1.1
Host: analytics.clientbrand.com
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Basic workspace info**
```json
{
  "status": "success",
  "summary": "Get workspace details",
  "data": {
    "workspaces": {
      "workspaceId": "466206000000071000",
      "workspaceName": "Sales Analytics",
      "workspaceDesc": "Sales reporting workspace for all regions",
      "createdTime": "1619175390377",
      "createdBy": "admin@acme.com",
      "orgId": "700000123456"
    }
  }
}
```

**Case 2 — With `withUserRoleInfo=true` (Account Admin caller)**
```json
{
  "status": "success",
  "summary": "Get workspace details",
  "data": {
    "workspaces": {
      "workspaceId": "466206000000071000",
      "workspaceName": "Sales Analytics",
      "workspaceDesc": "Sales reporting workspace for all regions",
      "createdTime": "1619175390377",
      "createdBy": "admin@acme.com",
      "orgId": "700000123456",
      "userRoleInfo": {
        "isCustomRoleUser": false,
        "roleId": 0,
        "roleName": "Account Admin"
      }
    }
  }
}
```

**Case 3 — With `withUserRoleInfo=true` (custom role user)**
```json
{
  "status": "success",
  "summary": "Get workspace details",
  "data": {
    "workspaces": {
      "workspaceId": "466206000000071000",
      "workspaceName": "Sales Analytics",
      "workspaceDesc": "Sales reporting workspace for all regions",
      "createdTime": "1619175390377",
      "createdBy": "admin@acme.com",
      "orgId": "700000123456",
      "userRoleInfo": {
        "isCustomRoleUser": true,
        "roleId": 466206000000090001,
        "roleName": "AnalystRole"
      }
    }
  }
}
```

> **`data.workspaces` is a single object, not an array.** Unlike the list APIs (Get All / Owned / Shared), this returns workspace details as a single JSON object under `workspaces`.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Workspace Info](../../../sdk-examples/workspace-management/workspace-operations/get-workspace-details.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`withUserRoleInfo=false` (default)** | Returns standard workspace metadata only. Fastest response option. |
| **`withUserRoleInfo=true` adds `userRoleInfo` object** | The additional object contains `isCustomRoleUser` (boolean), `roleId` (numeric), and `roleName` (string). Account Admins and Org Admins return `roleId: 0`; custom role users return the custom role's ID and display name. |
| **`workspaceKey` is NOT returned** | Get Workspace Info does not expose the secret key. Use Get Workspace Secret Key for that. |
| **Accessible to shared users with READ permission** | Unlike other workspace management APIs, this API is available to any user who has at least one view shared with them in the workspace (in addition to Workspace Admins). |
| **Comparison with list APIs** | Get Workspace Info returns richer metadata for a single known workspace. Use the list APIs to discover workspace IDs, then this API for detailed info on a specific workspace. |
| **Dependency** | Workspace ID → any workspace list API. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have any access to the specified workspace. The user must be a workspace admin or have at least one view shared with them in this workspace. | Verify the user has been added to the workspace or has a view shared with them. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Workspace Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Workspace](create-workspace.md), [Copy Workspace](copy-workspace.md), [Rename Workspace](rename-workspace.md), [Delete Workspace](delete-workspace.md), [Export as Template](export-as-template.md), [Get All Workspace List](get-all-workspaces.md), [Get Owned Workspace List](get-owned-workspaces.md), [Get Shared Workspace List](get-shared-workspaces.md), [Get Workspace Secret Key](get-workspace-secret-key.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-operations/get-workspace-details.md).
