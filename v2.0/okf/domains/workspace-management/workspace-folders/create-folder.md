---
type: API Endpoint
title: Create Folder
description: Creates a new folder in the specified workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/folders"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-folders
  - post
  - modeling
api:
  operation_id: createFolder
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/folders"
  domain: workspace-management
  group: workspace-folders
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
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Folder permission on the workspace."
  error_codes:
    - 7140
    - 7144
    - 7301
    - 7414
    - 7496
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1folders/post"
    config_schema: CreateFolderConfig
    response_schema: CreateFolderResponse
  sdk_examples: "/sdk-examples/workspace-management/workspace-folders/create-folder.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/folders`** - Create Folder (Workspace Folders / Workspace Management).

Creates a new folder in the specified workspace. The folder can optionally be created as a sub-folder of an existing top-level folder and can be designated as the default folder upon creation.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createFolder` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/folders` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Folder permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1folders/post`; CONFIG schema `CreateFolderConfig`; response schema `CreateFolderResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | The ID of the workspace. It can be obtained using any of the workspace list APIs. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

| Parameter | Type | Mandatory | Default | Max Length | Description |
|-----------|------|-----------|---------|------------|-------------|
| `folderName` | String | Yes | — | 200 | Name of the folder to create. Must be unique within the workspace. |
| `folderDesc` | String | No | `""` | 250 | Description for the folder. |
| `parentFolderId` | Long | No | `-1` (root) | — | ID of an existing top-level folder to create this folder under. Omit or pass `-1` to create a top-level folder. |
| `makeDefaultFolder` | Boolean | No | `false` | — | If `true`, the newly created folder becomes the default folder for the workspace. |

## Notes from the OpenAPI specification

- The folderName should be unique within the workspace. Creating a folder with a name that is already in use fails with error code 7140, and an empty name fails with error code 7414.
- The folderName can hold a maximum of 200 characters and the folderDesc can hold a maximum of 250 characters.
- When folderDesc is omitted, the description is stored as an empty string and not as null.
- When parentFolderId is omitted or set to -1, the folder is created at the root level.
- Exactly one level of nesting is supported. The parentFolderId should refer to a root level folder, and nesting inside an existing sub-folder fails with error code 7496.
- Setting makeDefaultFolder to true triggers the Make Default Folder operation internally. The folder that was the default until then loses its isDefault status.
- The response data holds only the folderId. Use the Get Folder List API to retrieve the complete folder record, covering the name, the description, the index, the default status and the parent folder.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

# Examples

## Sample Requests

**Case 1 — Create a top-level folder**

```http
POST /restapi/v2/workspaces/466206000000071000/folders HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"folderName":"Sales Analysis","folderDesc":"All sales-related reports and dashboards"}
```

**Case 2 — Create a sub-folder under an existing parent folder**

```http
POST /restapi/v2/workspaces/466206000000071000/folders HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"folderName":"Q1 Reports","folderDesc":"Q1 breakdown","parentFolderId":7617000071955001}
```

**Case 3 — Create a top-level folder and immediately set it as the default**

```http
POST /restapi/v2/workspaces/466206000000071000/folders HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"folderName":"Main Workspace","makeDefaultFolder":true}
```

**Case 4 — White label portal user with Create Folder permission**

```http
POST /restapi/v2/workspaces/466206000000071000/folders HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"folderName":"Client Reports","folderDesc":"Reports shared with the client"}
```

## Sample Responses

**HTTP 200 OK**

```json
{
  "status": "success",
  "summary": "Create folder",
  "data": {
    "folderId": "7617000071955010"
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Folder](../../../sdk-examples/workspace-management/workspace-folders/create-folder.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Response returns only `folderId`** | The response data contains only the newly created folder's ID. To retrieve the full folder record (name, description, index, parent), call Get Folder List after creation. |
| **`folderDesc` defaults to empty string** | If `folderDesc` is omitted, it is stored as `""` — not `null`. This is the initial value and does not affect subsequent Rename operations. |
| **`parentFolderId` defaults to root** | If omitted or set to `-1`, the folder is created at the root level. |
| **`makeDefaultFolder=true` side effect** | Triggers Make Default Folder internally. The previously marked default folder loses its `isDefault: true` status. |
| **One level of nesting only** | The `parentFolderId` must reference a root-level folder. Attempting to nest inside an existing sub-folder is rejected with error 7496. |
| **Dependency** | If creating a sub-folder, obtain the target `folderId` from Get Folder List. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7140](../../../foundations/error-codes.md#error-7140) | 400 | A folder with the same name already exists in the workspace. | Use a unique folder name within the workspace. |
| [7144](../../../foundations/error-codes.md#error-7144) | 400 | The specified `parentFolderId` does not exist. | Verify the `parentFolderId` value using the Get Folder List API. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Create Folder permission on the workspace. |
| [7414](../../../foundations/error-codes.md#error-7414) | 400 | Folder name cannot be empty. | Provide a non-empty value for `folderName`. |
| [7496](../../../foundations/error-codes.md#error-7496) | 400 | Maximum subfolder nesting depth exceeded. | Sub-folders cannot themselves have children. Only one level of nesting is supported. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Workspace Folders overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Folder List](get-folders.md), [Rename Folder](rename-folder.md), [Delete Folder](delete-folder.md), [Change Folder Hierarchy](change-folder-hierarchy.md), [Change Folder Position](change-folder-position.md), [Move Views To Folder](move-views-to-folder.md), [Make Default Folder](make-default-folder.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-folders/create-folder.md).
