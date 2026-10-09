---
type: API Endpoint
title: Move Views To Folder
description: "Moves one or more views (tables, reports, dashboards) into the specified destination folder within the workspace."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/movetofolder"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-folders
  - put
  - modeling
api:
  operation_id: moveViewsToFolder
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/views/movetofolder"
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
    - 7319
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1movetofolder/put"
    config_schema: MoveViewsToFolderConfig
    response_schema: null
  sdk_examples: "/sdk-examples/workspace-management/workspace-folders/move-views-to-folder.md"
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

**PUT `/restapi/v2/workspaces/{workspace-id}/views/movetofolder`** - Move Views To Folder (Workspace Folders / Workspace Management).

Moves one or more views (tables, reports, dashboards) into the specified destination folder within the workspace. All views must belong to the same workspace. Up to 1000 view IDs can be moved in a single request.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `moveViewsToFolder` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/movetofolder` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Folder permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1movetofolder/put`; CONFIG schema `MoveViewsToFolderConfig` |

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

## CONFIG Parameters

| Parameter | Type | Mandatory | Default | Max Items | Description |
|-----------|------|-----------|---------|-----------|-------------|
| `folderId` | Long | Yes | — | — | ID of the destination folder. |
| `viewIds` | JSONArray of Long | Yes | — | 1000 | Array of view IDs to move into the destination folder. |

## Notes from the OpenAPI specification

- Move Views To Folder returns a bare HTTP 204 No Content on success. There is no response body and no **status** or **summary** JSON to parse, so check only the HTTP status code. A JSON payload is returned only on failure.
- This operation is transactional. Either all the specified views are moved or none of them are. A single view ID that does not belong to the workspace fails the entire request with error code 7319 before any view is moved.
- A maximum of 1000 view IDs can be moved in a single request. Split the operation into multiple requests when more views have to be moved.
- The destination folder can be a root level folder or a sub-folder.
- There is no restriction on the type of the view. Tables, reports and dashboards can all be moved.
- The folderId should be obtained using the Get Folder List API, and the viewIds should be obtained using the Get View List API for the workspace.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Move a single view to a folder**

```http
PUT /restapi/v2/workspaces/466206000000071000/views/movetofolder HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"folderId":7617000071955001,"viewIds":[7617000000510001]}
```

**Case 2 — Move multiple views to a folder in bulk**

```http
PUT /restapi/v2/workspaces/466206000000071000/views/movetofolder HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"folderId":7617000071955001,"viewIds":[7617000000510001,7617000000510002,7617000000510003]}
```

**Case 3 — White label portal user moving views to a folder**

```http
PUT /restapi/v2/workspaces/466206000000071000/views/movetofolder HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"folderId":7617000071955001,"viewIds":[7617000000510004,7617000000510005]}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

```
HTTP/1.1 204 No Content
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Move Views To Folder](../../../sdk-examples/workspace-management/workspace-folders/move-views-to-folder.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Move Views To Folder returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Transactional — all or nothing** | Either all specified views are moved, or none. A single invalid `viewId` (not belonging to the workspace) causes the entire request to fail with error 7319 before any views are moved. |
| **Maximum 1000 views per request** | For workspaces requiring more than 1000 moves, split into multiple calls. |
| **Destination can be any level** | Views can be moved to both root-level folders and sub-folders. |
| **No restriction on view type** | Tables, reports, and dashboards can all be moved. |
| **Dependency** | `folderId` must be obtained from Get Folder List. `viewIds` must be obtained from the Get View List API for the workspace. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7144](../../../foundations/error-codes.md#error-7144) | 400 | The specified destination folder does not exist. | Verify the `folderId` using the Get Folder List API. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Create Folder permission on the workspace. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | One or more view IDs do not belong to the specified workspace. | Ensure all view IDs in `viewIds` belong to the workspace identified by `<workspace-id>`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Workspace Folders overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Folder List](get-folders.md), [Create Folder](create-folder.md), [Rename Folder](rename-folder.md), [Delete Folder](delete-folder.md), [Change Folder Hierarchy](change-folder-hierarchy.md), [Change Folder Position](change-folder-position.md), [Make Default Folder](make-default-folder.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-folders/move-views-to-folder.md).
