---
type: API Endpoint
title: Delete Folder
description: Deletes the specified folder from the workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-folders
  - delete
  - modeling
api:
  operation_id: deleteFolder
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}"
  domain: workspace-management
  group: workspace-folders
  oauth_scopes:
    - ZohoAnalytics.modeling.delete
  org_id_header: required
  config_parameter:
    location: form
    required: false
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Folder permission on the workspace."
  error_codes:
    - 7144
    - 7277
    - 7301
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1folders~1{folder-id}/delete"
    config_schema: DeleteFolderConfig
    response_schema: null
  sdk_examples: "/sdk-examples/workspace-management/workspace-folders/delete-folder.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}`** - Delete Folder (Workspace Folders / Workspace Management).

Deletes the specified folder from the workspace. By default, views inside the folder are preserved and moved out before deletion. You can optionally request that all views inside the folder be deleted as well.

> **Dependent Views:** If a folder contains a table that has dependent child views (reports or dashboards built on top of that table), deletion will fail unless `deleteDependentViews` is set to `true`.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deleteFolder` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingdelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Folder permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - optional |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1folders~1{folder-id}/delete`; CONFIG schema `DeleteFolderConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.delete`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | The ID of the workspace. It can be obtained using any of the workspace list APIs. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{folder-id}` | string | The ID of the folder. It can be obtained using the Get Folder List API. | [How to obtain](../../../foundations/identifiers.md#folder-id) |

## CONFIG Parameters

| Parameter | Type | Mandatory | Default | Max Length | Description |
|-----------|------|-----------|---------|------------|-------------|
| `deleteDependentViews` | Boolean | No | `false` | — | If `true`, all views inside the folder (including dependent child views of any tables) are permanently deleted along with the folder. If `false`, the API will fail if the folder contains tables that have dependent views. |

## Notes from the OpenAPI specification

- Delete Folder returns a bare HTTP 204 No Content on success. There is no response body and no **status** or **summary** JSON to parse, so check only the HTTP status code. A JSON payload is returned only on failure.
- When deleteDependentViews is omitted or set to false, the views present inside the folder are not deleted. They are retained and become accessible at the root level of the workspace, and only the folder container is removed.
- When the folder holds a table that has dependent child reports or dashboards, deletion with deleteDependentViews set to false fails with error code 7277. Either delete the dependent views first, or set deleteDependentViews to true.
- Setting deleteDependentViews to true permanently deletes all the views inside the folder, including the tables and their child reports and dashboards. This cannot be undone.
- Deleting the current default folder is allowed. The workspace holds no default folder until the Make Default Folder API is invoked.
- The folder-id in the request URL should be obtained using the Get Folder List API.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Delete an empty folder**

```http
DELETE /restapi/v2/workspaces/466206000000071000/folders/7617000071955005 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={}
```

**Case 2 — Delete a folder and all its views**

```http
DELETE /restapi/v2/workspaces/466206000000071000/folders/7617000071955005 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"deleteDependentViews":true}
```

**Case 3 — White label portal user deleting a folder**

```http
DELETE /restapi/v2/workspaces/466206000000071000/folders/7617000071955005 HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

```
HTTP/1.1 204 No Content
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Delete Folder](../../../sdk-examples/workspace-management/workspace-folders/delete-folder.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Delete Folder returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Views are preserved by default** | When `deleteDependentViews` is omitted (`false`), views inside the folder are not deleted — they are kept and become accessible at the workspace root level. Only the folder container is removed. |
| **Blocked when dependent views exist** | If the folder contains a table that has dependent child reports or dashboards, deletion with `deleteDependentViews=false` fails with error 7277. Either delete the dependent views first, or set `deleteDependentViews=true`. |
| **`deleteDependentViews=true` is permanent** | All views inside the folder, including tables and their child reports/dashboards, are permanently deleted. This cannot be undone. |
| **Deleting the current default folder** | Allowed. After deletion the workspace has no default folder until Make Default Folder is called. |
| **Dependency** | `<folder-id>` in the URL must be obtained from Get Folder List. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7144](../../../foundations/error-codes.md#error-7144) | 400 | The specified folder does not exist. | Verify the folder ID using the Get Folder List API. |
| [7277](../../../foundations/error-codes.md#error-7277) | 400 | The folder contains tables that have dependent child views; deletion blocked. | Set `deleteDependentViews` to `true` to delete the folder along with all dependent views, or manually delete the dependent views first. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Create Folder permission on the workspace. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Workspace Folders overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Folder List](get-folders.md), [Create Folder](create-folder.md), [Rename Folder](rename-folder.md), [Change Folder Hierarchy](change-folder-hierarchy.md), [Change Folder Position](change-folder-position.md), [Move Views To Folder](move-views-to-folder.md), [Make Default Folder](make-default-folder.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-folders/delete-folder.md).
