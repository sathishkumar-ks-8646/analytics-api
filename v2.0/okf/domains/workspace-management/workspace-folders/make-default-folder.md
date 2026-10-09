---
type: API Endpoint
title: Make Default Folder
description: Sets the specified folder as the default folder of the workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/default"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-folders
  - put
  - modeling
api:
  operation_id: makeDefaultFolder
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/default"
  domain: workspace-management
  group: workspace-folders
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Folder permission on the workspace."
  error_codes:
    - 7144
    - 7301
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1folders~1{folder-id}~1default/put"
    config_schema: null
    response_schema: null
  sdk_examples: "/sdk-examples/workspace-management/workspace-folders/make-default-folder.md"
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

**PUT `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/default`** - Make Default Folder (Workspace Folders / Workspace Management).

Sets the specified folder as the default folder for the workspace. The previous default folder (if any) loses its default status. Every workspace has exactly one default folder at all times.

> This API has no CONFIG parameter.

From the OpenAPI specification:

Sets the specified folder as the default folder of the workspace. The default folder is where a new view is placed when no folder is selected explicitly. The folder that was the default until then loses that status, as a workspace holds exactly one default folder at any point in time.

This API is idempotent. Invoking it on a folder that is already the default folder succeeds without error.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `makeDefaultFolder` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/default` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Folder permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 204 with no body |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1folders~1{folder-id}~1default/put` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | The ID of the workspace. It can be obtained using any of the workspace list APIs. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{folder-id}` | string | The ID of the folder. It can be obtained using the Get Folder List API. | [How to obtain](../../../foundations/identifiers.md#folder-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- Make Default Folder returns a bare HTTP 204 No Content on success. There is no response body and no **status** or **summary** JSON to parse, so check only the HTTP status code. A JSON payload is returned only on failure.
- The folder that was the default until then immediately loses its isDefault status. A workspace holds exactly one default folder at any point in time.
- This API is idempotent. Invoking it on a folder that is already the default folder succeeds without error and makes no change.
- Use the Get Folder List API after invoking this API to confirm that isDefault is true on the intended folder.
- The folder-id in the request URL should be obtained using the Get Folder List API.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Set a top-level folder as the default**

```http
PUT /restapi/v2/workspaces/466206000000071000/folders/7617000071955001/default HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Set a sub-folder as the default**

```http
PUT /restapi/v2/workspaces/466206000000071000/folders/7617000071955003/default HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — White label portal user setting the default folder**

```http
PUT /restapi/v2/workspaces/466206000000071000/folders/7617000071955001/default HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

```
HTTP/1.1 204 No Content
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Make Default Folder](../../../sdk-examples/workspace-management/workspace-folders/make-default-folder.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Make Default Folder returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Replaces the current default** | The previously marked default folder immediately loses its `isDefault: true` status. There is always exactly one default folder per workspace. |
| **Idempotent** | Calling this API on a folder that is already the default succeeds without error and makes no changes. |
| **No request body** | This API requires no CONFIG parameter. The folder is identified solely by `<folder-id>` in the URL. |
| **Verify with Get Folder List** | After calling this API, use Get Folder List to confirm `isDefault: true` is on the correct folder. |
| **Dependency** | `<folder-id>` in the URL must be obtained from Get Folder List. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7144](../../../foundations/error-codes.md#error-7144) | 400 | The specified folder does not exist. | Verify the folder ID using the Get Folder List API. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Create Folder permission on the workspace. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Workspace Folders overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Folder List](get-folders.md), [Create Folder](create-folder.md), [Rename Folder](rename-folder.md), [Delete Folder](delete-folder.md), [Change Folder Hierarchy](change-folder-hierarchy.md), [Change Folder Position](change-folder-position.md), [Move Views To Folder](move-views-to-folder.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-folders/make-default-folder.md).
