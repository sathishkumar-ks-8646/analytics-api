---
type: API Endpoint
title: Get Shared Workspace List
description: Returns all workspaces that have been shared with the authenticated user from other organisations.
resource: https://analyticsapi.zoho.com/restapi/v2/workspaces/shared
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-operations
  - get
  - metadata
api:
  operation_id: getSharedWorkspaces
  method: GET
  path: "/restapi/v2/workspaces/shared"
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
    pointer: "#/paths/~1restapi~1v2~1workspaces~1shared/get"
    config_schema: null
    response_schema: GetSharedWorkspacesResponse
  sdk_examples: "/sdk-examples/workspace-management/workspace-operations/get-shared-workspaces.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/shared`** - Get Shared Workspace List (Workspace Operations / Workspace Management).

Returns all workspaces that have been shared with the authenticated user from **other organisations**. Workspaces in the user's own organisation are not included — use Get All Workspace List to see both owned and shared together.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getSharedWorkspaces` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/shared` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | Not required (user-scoped API) |
| Permission required | Any authenticated Zoho Analytics user. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1shared/get`; response schema `GetSharedWorkspacesResponse` |

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

- This API returns only the workspaces shared with the requesting user by users from other organizations. The workspaces present in the organization of the requesting user are not included.
- The result of this API is a subset of the result of the Get All Workspace List API.
- The scope is resolved from the identity of the requesting user. The **ZANALYTICS-ORGID** header is not required for this API.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `data.workspaces` | Array | Workspaces from other organisations shared with the calling user. Empty array if no workspaces are shared. |
| `workspaces[].workspaceId` | String | Unique workspace identifier. |
| `workspaces[].workspaceName` | String | Workspace display name. |
| `workspaces[].workspaceDesc` | String | Description. Empty string if not set. |
| `workspaces[].orgId` | String | Organisation ID of the workspace owner (not the caller's org). |
| `workspaces[].createdTime` | String | Unix timestamp (milliseconds) of workspace creation. |
| `workspaces[].createdBy` | String | Email of the user who created the workspace. |
| `workspaces[].isDefault` | Boolean | `true` if this is the source organisation's default workspace. |

# Examples

## Sample Requests

**Case 1 — User listing workspaces shared with them**

```http
GET /restapi/v2/workspaces/shared HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — User has access to workspaces in two other organisations**
```json
{
  "status": "success",
  "summary": "Get shared workspaces",
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
      }
    ]
  }
}
```

**Case 2 — User has no shared workspaces**
```json
{
  "status": "success",
  "summary": "Get shared workspaces",
  "data": {
    "workspaces": []
  }
}
```

**Case 3 — Client Portal user seeing their portal's workspace**
```json
{
  "status": "success",
  "summary": "Get shared workspaces",
  "data": {
    "workspaces": [
      {
        "workspaceId": "38190000004180410",
        "workspaceName": "Client Analytics Portal",
        "workspaceDesc": "",
        "orgId": "57058019",
        "createdTime": "1697525603846",
        "createdBy": "admin@brandco.com",
        "isDefault": false
      }
    ]
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Shared Workspace List](../../../sdk-examples/workspace-management/workspace-operations/get-shared-workspaces.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Returns workspaces from other orgs** | This API returns workspaces that have been shared with the calling user by users from other organisations. Workspaces within the caller's own org are not included. |
| **`ZANALYTICS-ORGID` not required** | The scope is cross-org and determined from the caller's identity, not an org header. |
| **Relationship to Get All Workspace List** | The results of this API are a subset of what Get All Workspace List returns (the shared-from-other-orgs portion). |
| **Dependency** | No dependencies on other APIs for the request. |

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
- Other endpoints in this group: [Create Workspace](create-workspace.md), [Copy Workspace](copy-workspace.md), [Rename Workspace](rename-workspace.md), [Delete Workspace](delete-workspace.md), [Export as Template](export-as-template.md), [Get All Workspace List](get-all-workspaces.md), [Get Owned Workspace List](get-owned-workspaces.md), [Get Workspace Secret Key](get-workspace-secret-key.md), [Get Workspace Info](get-workspace-details.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-operations/get-shared-workspaces.md).
