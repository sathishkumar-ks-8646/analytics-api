---
type: API Endpoint
title: Get Folder List
description: "Returns all folders in the specified workspace, including their names, descriptions, display order, default status, and parent folder references."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/folders"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-folders
  - get
  - metadata
api:
  operation_id: getFolders
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/folders"
  domain: workspace-management
  group: workspace-folders
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or a Shared User or Group Member with at least READ permission on one or more views in the workspace."
  error_codes:
    - 7301
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1folders/get"
    config_schema: null
    response_schema: GetFoldersResponse
  sdk_examples: "/sdk-examples/workspace-management/workspace-folders/get-folders.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/folders`** - Get Folder List (Workspace Folders / Workspace Management).

Returns all folders in the specified workspace, including their names, descriptions, display order, default status, and parent folder references. Shared users and group members receive a filtered list containing only the folders that include at least one view they have access to.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getFolders` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/folders` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or a Shared User or Group Member with at least READ permission on one or more views in the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1folders/get`; response schema `GetFoldersResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | The ID of the workspace. It can be obtained using any of the workspace list APIs. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- Workspace Admins receive every folder of the workspace. Shared users and group members receive a filtered list holding only the folders that contain at least one view they have access to. When a view inside a sub-folder is accessible to the user, both the sub-folder and its parent folder are included.
- The folders array is returned empty when the workspace holds no folder, or when the requesting user has access to no view in the workspace.
- The parentFolderId is always returned as a quoted string and not as a number. The value -1 indicates that the folder is at the root level and has no parent.
- The folders are sorted by folderIndex within their hierarchy level. The default folder always holds folderIndex as -1.
- Exactly one folder of a workspace holds isDefault as true at any point in time.
- Exactly one level of nesting is supported. A root level folder can hold sub-folders, and a sub-folder cannot hold children of its own.
- This API is the entry point for all the other folder APIs. The folderId values returned here are used as the folder-id in the request URL of the Rename Folder, Delete Folder, Change Folder Hierarchy, Change Folder Position and Make Default Folder APIs, as the parentFolderId in the Create Folder and Change Folder Hierarchy APIs, as the referenceFolderId in the Change Folder Position API, and as the folderId in the Move Views To Folder API.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `folderId` | String | Unique ID of the folder. |
| `folderName` | String | Display name of the folder. |
| `folderDesc` | String | Description of the folder. Empty string if none set. |
| `folderIndex` | Integer | Sort position of the folder within its level. `-1` indicates the default folder. |
| `isDefault` | Boolean | `true` if this is the workspace's current default folder. |
| `parentFolderId` | String | ID of the parent folder. `"-1"` means the folder is at the top level (root). |

# Examples

## Sample Requests

**Case 1 — Workspace Admin listing all folders**

```http
GET /restapi/v2/workspaces/466206000000071000/folders HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Shared User listing accessible folders (filtered response)**

```http
GET /restapi/v2/workspaces/466206000000071000/folders HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — White label portal user listing folders**

```http
GET /restapi/v2/workspaces/466206000000071000/folders HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Workspace Admin — workspace with nested folders**
```json
{
  "status": "success",
  "summary": "Get folders",
  "data": {
    "folders": [
      {
        "folderId": "7617000000508002",
        "folderName": "Tables & Reports",
        "folderDesc": "Default Folder",
        "folderIndex": -1,
        "isDefault": true,
        "parentFolderId": "-1"
      },
      {
        "folderId": "7617000071955001",
        "folderName": "Parent folder 1",
        "folderDesc": "",
        "folderIndex": 0,
        "isDefault": false,
        "parentFolderId": "-1"
      },
      {
        "folderId": "7617000071955003",
        "folderName": "Sub folder 1",
        "folderDesc": "",
        "folderIndex": 2,
        "isDefault": false,
        "parentFolderId": "7617000071955001"
      },
      {
        "folderId": "7617000071955002",
        "folderName": "Parent folder 2",
        "folderDesc": "",
        "folderIndex": 1,
        "isDefault": false,
        "parentFolderId": "-1"
      },
      {
        "folderId": "7617000071955004",
        "folderName": "Sub folder 2",
        "folderDesc": "",
        "folderIndex": 2,
        "isDefault": false,
        "parentFolderId": "7617000071955002"
      }
    ]
  }
}
```

**Case 2 — Shared User — filtered list (only folders containing accessible views)**
```json
{
  "status": "success",
  "summary": "Get folders",
  "data": {
    "folders": [
      {
        "folderId": "137687000000471834",
        "folderName": "Tables & Reports",
        "folderDesc": "Default Folder",
        "folderIndex": -1,
        "isDefault": true,
        "parentFolderId": "-1"
      },
      {
        "folderId": "137687000097308304",
        "folderName": "Parent folder 1",
        "folderDesc": "",
        "folderIndex": 0,
        "isDefault": false,
        "parentFolderId": "-1"
      },
      {
        "folderId": "137687000097308305",
        "folderName": "Sub folder 1",
        "folderDesc": "",
        "folderIndex": 2,
        "isDefault": false,
        "parentFolderId": "137687000097308304"
      }
    ]
  }
}
```

**Case 3 — Workspace with only the default folder**
```json
{
  "status": "success",
  "summary": "Get folders",
  "data": {
    "folders": [
      {
        "folderId": "13193000000302867",
        "folderName": "Tables & Reports",
        "folderDesc": "",
        "folderIndex": -1,
        "isDefault": true,
        "parentFolderId": "-1"
      }
    ]
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Folder List](../../../sdk-examples/workspace-management/workspace-folders/get-folders.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Filtered response for shared users** | Workspace Admins see all folders. Shared Users and Group Members receive only folders that contain at least one view they can access. If a user can access a view inside a sub-folder, both the sub-folder and its parent folder are included in their response. |
| **`parentFolderId` is a string** | Returned as a quoted string (e.g. `"-1"`), not a numeric. `"-1"` means the folder is at root level with no parent. |
| **`folderIndex` ordering** | Folders are sorted by `folderIndex` within their level. The default folder always has `folderIndex: -1`. |
| **Empty workspace** | If the workspace has no folders, the `folders` array is returned empty (`[]`). |
| **Dependency for other APIs** | The `folderId` values returned here are required as: `<folder-id>` in the URL for Rename Folder, Delete Folder, Change Folder Hierarchy, Change Folder Position, and Make Default Folder; `parentFolderId` in Create Folder; `referenceFolderId` in Change Folder Position. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin, or has at least READ access to one or more views in the workspace. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Workspace Folders overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Folder](create-folder.md), [Rename Folder](rename-folder.md), [Delete Folder](delete-folder.md), [Change Folder Hierarchy](change-folder-hierarchy.md), [Change Folder Position](change-folder-position.md), [Move Views To Folder](move-views-to-folder.md), [Make Default Folder](make-default-folder.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-folders/get-folders.md).
