---
type: API Endpoint
title: Change Folder Position
description: Reorders a folder by moving it to just above another specified folder at the same hierarchy level.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/reorder"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-folders
  - put
  - modeling
api:
  operation_id: changeFolderPosition
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/reorder"
  domain: workspace-management
  group: workspace-folders
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Folder permission on the workspace."
  error_codes:
    - 7144
    - 7301
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1folders~1{folder-id}~1reorder/put"
    config_schema: ChangeFolderPositionConfig
    response_schema: null
  sdk_examples: "/sdk-examples/workspace-management/workspace-folders/change-folder-position.md"
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

**PUT `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/reorder`** - Change Folder Position (Workspace Folders / Workspace Management).

Reorders a folder by moving it to just above another specified folder at the same hierarchy level. Both folders must be at the same level (both top-level or both sub-folders of the same parent).

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `changeFolderPosition` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/reorder` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Folder permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1folders~1{folder-id}~1reorder/put`; CONFIG schema `ChangeFolderPositionConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | The ID of the workspace. It can be obtained using any of the workspace list APIs. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{folder-id}` | string | The ID of the folder. It can be obtained using the Get Folder List API. | [How to obtain](../../../foundations/identifiers.md#folder-id) |

## CONFIG Parameters

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `referenceFolderId` | Long | Yes | — | ID of the folder that the target folder should be placed immediately above. |

## Notes from the OpenAPI specification

- Change Folder Position returns a bare HTTP 204 No Content on success. There is no response body and no **status** or **summary** JSON to parse, so check only the HTTP status code. A JSON payload is returned only on failure.
- The folder identified by the folder-id in the request URL is placed immediately above the folder given in referenceFolderId in the sorted list.
- Both the folders should be at the same hierarchy level, that is, both at the root level or both sub-folders of the same parent. Reordering across levels is not supported and produces unexpected results.
- The folderIndex values of the affected folders are recalculated after this operation. Use the Get Folder List API to confirm the new ordering.
- Both the folder-id in the request URL and the referenceFolderId should be obtained using the Get Folder List API.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Move a folder above another folder**

```http
PUT /restapi/v2/workspaces/466206000000071000/folders/7617000071955002/reorder HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"referenceFolderId":7617000071955001}
```

**Case 2 — Reorder a sub-folder within its parent**

```http
PUT /restapi/v2/workspaces/466206000000071000/folders/7617000071955004/reorder HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"referenceFolderId":7617000071955003}
```

**Case 3 — White label portal user reordering folders**

```http
PUT /restapi/v2/workspaces/466206000000071000/folders/7617000071955002/reorder HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"referenceFolderId":7617000071955001}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

```
HTTP/1.1 204 No Content
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Change Folder Position](../../../sdk-examples/workspace-management/workspace-folders/change-folder-position.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Change Folder Position returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Moves folder to immediately above the reference** | After this operation, the target folder (identified by `<folder-id>`) appears directly above `referenceFolderId` in the sorted list. |
| **Both folders must be at the same hierarchy level** | Both the target folder and `referenceFolderId` must be either both root-level or both sub-folders of the same parent. Cross-level reordering is not supported and will produce unexpected results. |
| **`folderIndex` is updated** | After this call, `folderIndex` values for affected folders are recalculated. Use Get Folder List to confirm the new ordering. |
| **Dependency** | Both `<folder-id>` (folder to reorder) and `referenceFolderId` (the position anchor) must be obtained from Get Folder List. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7144](../../../foundations/error-codes.md#error-7144) | 400 | The specified folder or reference folder does not exist. | Verify the folder IDs using the Get Folder List API. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Create Folder permission on the workspace. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Workspace Folders overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Folder List](get-folders.md), [Create Folder](create-folder.md), [Rename Folder](rename-folder.md), [Delete Folder](delete-folder.md), [Change Folder Hierarchy](change-folder-hierarchy.md), [Move Views To Folder](move-views-to-folder.md), [Make Default Folder](make-default-folder.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-folders/change-folder-position.md).
