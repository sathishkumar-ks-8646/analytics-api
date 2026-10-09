---
type: API Endpoint
title: Rename Folder
description: Updates the name and/or description of an existing folder.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-folders
  - put
  - modeling
api:
  operation_id: renameFolder
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}"
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
    - 7140
    - 7144
    - 7301
    - 7414
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1folders~1{folder-id}/put"
    config_schema: RenameFolderConfig
    response_schema: null
  sdk_examples: "/sdk-examples/workspace-management/workspace-folders/rename-folder.md"
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

**PUT `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}`** - Rename Folder (Workspace Folders / Workspace Management).

Updates the name and/or description of an existing folder. If `folderDesc` is omitted from the request, the folder's existing description is **reset to an empty string**.

> **Important:** Always include `folderDesc` in the request if you want to preserve the existing description. Omitting this field will clear it.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `renameFolder` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Folder permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1folders~1{folder-id}/put`; CONFIG schema `RenameFolderConfig` |

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

| Parameter | Type | Mandatory | Default | Max Length | Description |
|-----------|------|-----------|---------|------------|-------------|
| `folderName` | String | Yes | — | 200 | New name for the folder. Must be unique within the workspace. |
| `folderDesc` | String | No | `""` | 250 | New description for the folder. **Omitting this field resets the description to an empty string.** |

## Notes from the OpenAPI specification

- Rename Folder returns a bare HTTP 204 No Content on success. There is no response body and no **status** or **summary** JSON to parse, so check only the HTTP status code. A JSON payload is returned only on failure.
- When folderDesc is omitted, the existing description of the folder is permanently reset to an empty string. This is intentional behaviour and not a defect. Always read the current folderDesc using the Get Folder List API and pass it back when only the name has to be changed.
- Renaming the folder to its existing name succeeds without an error.
- The folderName should be unique within the workspace. Renaming to a name that is already in use fails with error code 7140, and an empty name fails with error code 7414.
- The folderName can hold a maximum of 200 characters and the folderDesc can hold a maximum of 250 characters.
- The folder-id in the request URL should be obtained using the Get Folder List API.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Rename a folder and preserve its description**

```http
PUT /restapi/v2/workspaces/466206000000071000/folders/7617000071955001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"folderName":"Annual Sales Analysis","folderDesc":"All sales-related reports and dashboards"}
```

**Case 2 — Rename a folder and update its description**

```http
PUT /restapi/v2/workspaces/466206000000071000/folders/7617000071955001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"folderName":"FY2025 Sales","folderDesc":"Fiscal year 2025 sales reports"}
```

**Case 3 — White label portal user renaming a folder**

```http
PUT /restapi/v2/workspaces/466206000000071000/folders/7617000071955001 HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"folderName":"Client Dashboard","folderDesc":"Customer-facing dashboards"}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

```
HTTP/1.1 204 No Content
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Rename Folder](../../../sdk-examples/workspace-management/workspace-folders/rename-folder.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Rename Folder returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **`folderDesc` is RESET on omission** | If `folderDesc` is not included in the request, the folder's existing description is permanently overwritten with an empty string. This is the most common mistake with this API — always include the current `folderDesc` value (read from Get Folder List) if you only intend to change the name. |
| **Renaming to the same name** | Succeeds without error (idempotent for the name). |
| **Name uniqueness** | The new `folderName` must not already be in use by another folder in the same workspace. |
| **Dependency** | `<folder-id>` in the URL must be obtained from Get Folder List. Read the current `folderDesc` from Get Folder List before calling this API if you want to preserve it. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7140](../../../foundations/error-codes.md#error-7140) | 400 | A folder with the same name already exists in the workspace. | Use a unique folder name within the workspace. |
| [7144](../../../foundations/error-codes.md#error-7144) | 400 | The specified folder does not exist. | Verify the folder ID using the Get Folder List API. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Create Folder permission on the workspace. |
| [7414](../../../foundations/error-codes.md#error-7414) | 400 | Folder name cannot be empty. | Provide a non-empty value for `folderName`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Workspace Folders overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Folder List](get-folders.md), [Create Folder](create-folder.md), [Delete Folder](delete-folder.md), [Change Folder Hierarchy](change-folder-hierarchy.md), [Change Folder Position](change-folder-position.md), [Move Views To Folder](move-views-to-folder.md), [Make Default Folder](make-default-folder.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-folders/rename-folder.md).
