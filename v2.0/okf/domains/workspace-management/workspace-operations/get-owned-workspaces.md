---
type: API Endpoint
title: Get Owned Workspace List
description: "Returns all workspaces owned by (created within) the authenticated user's organisation."
resource: https://analyticsapi.zoho.com/restapi/v2/workspaces/owned
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-operations
  - get
  - metadata
api:
  operation_id: getOwnedWorkspaces
  method: GET
  path: "/restapi/v2/workspaces/owned"
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
  permission_required: The authenticated user must be the Account Admin of the organisation.
  error_codes:
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1owned/get"
    config_schema: null
    response_schema: GetOwnedWorkspacesResponse
  sdk_examples: "/sdk-examples/workspace-management/workspace-operations/get-owned-workspaces.md"
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

**GET `/restapi/v2/workspaces/owned`** - Get Owned Workspace List (Workspace Operations / Workspace Management).

Returns all workspaces owned by (created within) the authenticated user's organisation. This is an admin-scoped API — only the Account Admin can call it, and it returns all workspaces in the org regardless of sharing.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getOwnedWorkspaces` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/owned` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | Not required (user-scoped API) |
| Permission required | The authenticated user must be the Account Admin of the organisation. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1owned/get`; response schema `GetOwnedWorkspacesResponse` |

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

- This API can be invoked only by the Account Admin of the organization. Organization Admins and Workspace Admins invoking this API fail with error code 7301.
- The API returns all the workspaces present in the organization of the requesting Account Admin, including the workspaces that the Account Admin did not create and does not administer directly.
- The organization scope is resolved from the session of the requesting user. The **ZANALYTICS-ORGID** header is not required for this API.
- The Get All Workspace List API differs from this API. It returns the owned and the shared workspaces of the requesting user across all the organizations, and it can be invoked by any user.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `data.workspaces` | Array | All workspaces in the calling Account Admin's organisation. |
| `workspaces[].workspaceId` | String | Unique workspace identifier. |
| `workspaces[].workspaceName` | String | Workspace display name. |
| `workspaces[].workspaceDesc` | String | Description. Empty string `""` if not set. |
| `workspaces[].orgId` | String | Organisation ID. Always the Account Admin's org. |
| `workspaces[].createdTime` | String | Unix timestamp (milliseconds) when the workspace was created. |
| `workspaces[].createdBy` | String | Email of the user who created the workspace. |
| `workspaces[].isDefault` | Boolean | `true` if this is the organisation's default workspace. |

# Examples

## Sample Requests

**Case 1 — Account Admin listing all org-owned workspaces**

```http
GET /restapi/v2/workspaces/owned HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

## Sample Responses

**HTTP 200 OK**

```json
{
  "status": "success",
  "summary": "Get owned workspaces",
  "data": {
    "workspaces": [
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
    ]
  }
}
```

> **Difference from Get All Workspace List:** Get Owned Workspace List returns only workspaces belonging to the Account Admin's own organisation. It is restricted to Account Admin access only. Get All Workspace List includes both owned and shared workspaces from all organisations and is accessible to any user.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Owned Workspace List](../../../sdk-examples/workspace-management/workspace-operations/get-owned-workspaces.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Account Admin only** | Unlike Get All Workspace List (which any user can call), this API is restricted to Account Admins. It returns all workspaces under the caller's entire organisation, not just those the caller personally created. |
| **`ZANALYTICS-ORGID` not required** | The org scope is determined from the Account Admin's session. |
| **Relationship to Get All Workspace List** | Get Owned Workspace List is a superset for Account Admins — it includes workspaces the Account Admin may not directly own or have Workspace Admin access to, but are within their org. |
| **Dependency** | No dependencies on other APIs for the request. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not the Account Admin. Organization Admins and Workspace Admins cannot call this API. | Use Account Admin credentials. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Workspace Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Workspace](create-workspace.md), [Copy Workspace](copy-workspace.md), [Rename Workspace](rename-workspace.md), [Delete Workspace](delete-workspace.md), [Export as Template](export-as-template.md), [Get All Workspace List](get-all-workspaces.md), [Get Shared Workspace List](get-shared-workspaces.md), [Get Workspace Secret Key](get-workspace-secret-key.md), [Get Workspace Info](get-workspace-details.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-operations/get-owned-workspaces.md).
