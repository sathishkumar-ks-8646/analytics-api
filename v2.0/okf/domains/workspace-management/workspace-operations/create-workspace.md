---
type: API Endpoint
title: Create Workspace
description: Creates a new empty workspace in the specified organization.
resource: https://analyticsapi.zoho.com/restapi/v2/workspaces
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-operations
  - post
  - modeling
api:
  operation_id: createWorkspace
  method: POST
  path: "/restapi/v2/workspaces"
  domain: workspace-management
  group: workspace-operations
  oauth_scopes:
    - ZohoAnalytics.modeling.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the target organisation.
  error_codes:
    - 7301
    - 7951
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces/post"
    config_schema: CreateWorkspaceConfig
    response_schema: CreateWorkspaceResponse
  sdk_examples: "/sdk-examples/workspace-management/workspace-operations/create-workspace.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces`** - Create Workspace (Workspace Operations / Workspace Management).

Creates a new empty workspace in the specified organisation. The workspace is created with no tables, views, or users — content must be added through subsequent APIs.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createWorkspace` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID in which the workspace will be created. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the target organisation. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces/post`; CONFIG schema `CreateWorkspaceConfig`; response schema `CreateWorkspaceResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

This endpoint has no path parameters.

## CONFIG Parameter

CONFIG is **mandatory**. It must be sent as a form-encoded body parameter named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `workspaceName` | String | **Yes** | — | Name for the new workspace. Must be unique within the organisation. Max 50 characters. |
| `workspaceDesc` | String | No | `""` | Optional description of the workspace's purpose. Max 250 characters. |

## Notes from the OpenAPI specification

- The **workspaceName** should be unique within the organization. Creating a workspace with a name that is already in use fails with error code 7111.
- The **workspaceName** can hold a maximum of 50 characters and the **workspaceDesc** can hold a maximum of 250 characters. Exceeding these limits is rejected during parameter validation.
- When **workspaceDesc** is omitted, the description is stored as an empty string. It can be updated later using the Rename Workspace API.
- The response data holds only the **workspaceId**. Use the Get Workspace Info or the Get All Workspace List API to retrieve the complete workspace record.
- The workspace secret key is not generated at creation time. Use the Get Workspace Secret Key API when the key is needed for a cross-organization copy.
- The number of workspaces that can be created depends on the subscription plan of the organization. Reaching the limit fails with error code 7951.
- Organization Admins are allowed to create workspaces within their organization.
- The workspace is created with no tables or views. The content has to be added using the subsequent APIs.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `data.workspaceId` | String | Unique identifier of the newly created workspace. Use this as `<workspace-id>` in all subsequent workspace-specific API calls. |

# Examples

## Sample Requests

**Case 1 — Create a minimal workspace with name only**

```http
POST /restapi/v2/workspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"workspaceName":"Sales Analytics"}
```

**Case 2 — Create a workspace with a description**

```http
POST /restapi/v2/workspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"workspaceName":"HR Analytics","workspaceDesc":"Workspace for HR team dashboards and headcount reports"}
```

## Sample Responses

**HTTP 200 OK** — Workspace created successfully.

```json
{
  "status": "success",
  "summary": "Create workspace",
  "data": {
    "workspaceId": "466206000000295001"
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Workspace](../../../sdk-examples/workspace-management/workspace-operations/create-workspace.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Response returns only `workspaceId`** | The response data contains only the newly created workspace's ID. Call Get Workspace Info or Get All Workspace List to retrieve the full workspace record. |
| **`workspaceDesc` defaults to empty string** | If omitted, the description is stored as `""`. This value can be updated later via Rename Workspace. |
| **`workspaceKey` not in create response** | The workspace secret key is not generated at creation time. Use Get Workspace Secret Key when you need the key for cross-org copy operations. |
| **Dependency** | No dependencies on other APIs for the request. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not an Account Admin or Organization Admin. | Ensure the caller has Account Admin or Organization Admin privileges in the target organisation. |
| [7951](../../../foundations/error-codes.md#error-7951) | 400 | The organisation has reached its workspace creation limit based on the current subscription plan. | Upgrade the plan or delete unused workspaces before creating a new one. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |

# Related

- [Workspace Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Copy Workspace](copy-workspace.md), [Rename Workspace](rename-workspace.md), [Delete Workspace](delete-workspace.md), [Export as Template](export-as-template.md), [Get All Workspace List](get-all-workspaces.md), [Get Owned Workspace List](get-owned-workspaces.md), [Get Shared Workspace List](get-shared-workspaces.md), [Get Workspace Secret Key](get-workspace-secret-key.md), [Get Workspace Info](get-workspace-details.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-operations/create-workspace.md).
