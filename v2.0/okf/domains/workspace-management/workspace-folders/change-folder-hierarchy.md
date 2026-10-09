---
type: API Endpoint
title: Change Folder Hierarchy
description: "Changes the hierarchical position of a folder, either by promoting a sub-folder to the root level or by nesting an existing root level folder under another root level folder."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/move"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-folders
  - put
  - modeling
api:
  operation_id: changeFolderHierarchy
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/move"
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
    - 8119
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1folders~1{folder-id}~1move/put"
    config_schema: ChangeFolderHierarchyConfig
    response_schema: null
  sdk_examples: "/sdk-examples/workspace-management/workspace-folders/change-folder-hierarchy.md"
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

**PUT `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/move`** - Change Folder Hierarchy (Workspace Folders / Workspace Management).

Changes the hierarchical position of a folder — either promoting a sub-folder to a top-level folder, or nesting an existing top-level folder under another top-level folder.

The `hierarchy` parameter controls the direction of the change:

| `hierarchy` Value | Meaning |
|-------------------|---------|
| `0` | Promote: Move the specified sub-folder up to become a top-level (root-level) folder. |
| `1` | Nest: Move the specified top-level folder to become a sub-folder of the folder specified by `parentFolderId`. |

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `changeFolderHierarchy` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/move` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Folder permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1folders~1{folder-id}~1move/put`; CONFIG schema `ChangeFolderHierarchyConfig` |

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
| `hierarchy` | Integer | Yes | — | Direction of the hierarchy change. `0` = promote sub-folder to top level; `1` = nest under a parent folder. |
| `parentFolderId` | Long | **Yes when `hierarchy=1`** | — | ID of the top-level folder to become the parent. Required only when `hierarchy` is `1`. |

## Notes from the OpenAPI specification

- Change Folder Hierarchy returns a bare HTTP 204 No Content on success. There is no response body and no **status** or **summary** JSON to parse, so check only the HTTP status code. A JSON payload is returned only on failure.
- When hierarchy is set to 0, the parentFolderId should not be sent. The parent link of the folder is removed and it becomes a root level folder.
- When hierarchy is set to 1, the parentFolderId is mandatory. Omitting it results in an error.
- The parentFolderId should refer to a root level folder, that is, a folder whose own parentFolderId is -1. A folder cannot be nested inside an existing sub-folder, as exactly one level of nesting is supported.
- Only the values 0 and 1 are accepted for hierarchy. Any other value fails with error code 8119 before any change is made.
- Both the folder-id in the request URL and the parentFolderId should be obtained using the Get Folder List API. Verify that the parentFolderId target is a root level folder before invoking this API.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Promote a sub-folder to top-level (hierarchy=0)**

```http
PUT /restapi/v2/workspaces/466206000000071000/folders/7617000071955003/move HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"hierarchy":0}
```

**Case 2 — Nest a top-level folder under another folder (hierarchy=1)**

```http
PUT /restapi/v2/workspaces/466206000000071000/folders/7617000071955002/move HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"hierarchy":1,"parentFolderId":7617000071955001}
```

**Case 3 — White label portal user changing folder hierarchy**

```http
PUT /restapi/v2/workspaces/466206000000071000/folders/7617000071955002/move HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"hierarchy":1,"parentFolderId":7617000071955001}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

```
HTTP/1.1 204 No Content
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Change Folder Hierarchy](../../../sdk-examples/workspace-management/workspace-folders/change-folder-hierarchy.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Change Folder Hierarchy returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **`hierarchy=0` — no `parentFolderId` needed** | When promoting a sub-folder to root level, `parentFolderId` must not be provided. The folder's parent link is removed and it becomes a root-level folder. |
| **`hierarchy=1` — `parentFolderId` is mandatory** | When nesting, both fields are required. Omitting `parentFolderId` when `hierarchy=1` results in an error. |
| **`parentFolderId` must be a root-level folder** | You cannot nest a folder inside an existing sub-folder. The folder given by `parentFolderId` must be at root level (its own `parentFolderId` is `"-1"`). |
| **Only `0` and `1` are valid** | Any other integer value for `hierarchy` immediately returns error 8119 before any database change is made. |
| **Dependency** | Both `<folder-id>` (the folder to move) and `parentFolderId` (when `hierarchy=1`) must be obtained from Get Folder List. Verify the `parentFolderId` target is a root-level folder before calling. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7144](../../../foundations/error-codes.md#error-7144) | 400 | The specified folder or parent folder does not exist. | Verify the folder IDs using the Get Folder List API. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Create Folder permission on the workspace. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | Invalid value for `hierarchy`. Only `0` and `1` are accepted. | Use `0` to promote a sub-folder to root level, or `1` to nest a folder under a parent. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Workspace Folders overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Folder List](get-folders.md), [Create Folder](create-folder.md), [Rename Folder](rename-folder.md), [Delete Folder](delete-folder.md), [Change Folder Position](change-folder-position.md), [Move Views To Folder](move-views-to-folder.md), [Make Default Folder](make-default-folder.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-folders/change-folder-hierarchy.md).
