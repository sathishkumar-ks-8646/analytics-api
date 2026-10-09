---
type: API Endpoint
title: Rename Workspace
description: Updates the name and the description of an existing workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-operations
  - put
  - modeling
api:
  operation_id: renameWorkspace
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}"
  domain: workspace-management
  group: workspace-operations
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace.
  error_codes:
    - 7103
    - 7111
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}/put"
    config_schema: RenameWorkspaceConfig
    response_schema: null
  sdk_examples: "/sdk-examples/workspace-management/workspace-operations/rename-workspace.md"
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

**PUT `/restapi/v2/workspaces/{workspace-id}`** - Rename Workspace (Workspace Operations / Workspace Management).

Updates the name and/or description of an existing workspace. Both fields are replaced atomically — if `workspaceDesc` is omitted, the description is **reset to an empty string** (the previous value is not preserved).

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `renameWorkspace` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}/put`; CONFIG schema `RenameWorkspaceConfig` |

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

## CONFIG Parameter

CONFIG is **mandatory**. It must be sent as a form-encoded body parameter named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `workspaceName` | String | **Yes** | — | New name for the workspace. Must be unique within the organisation. Max 50 characters. |
| `workspaceDesc` | String | No | `""` | New description for the workspace. Max 250 characters. When omitted, the description is **reset to an empty string** — the existing description is not preserved. Always pass the existing description if you only intend to rename. |

## Notes from the OpenAPI specification

- Rename Workspace returns a bare HTTP 204 No Content on success. There is no response body and no **status** or **summary** JSON to parse, so check only the HTTP status code. A JSON payload is returned only on failure.
- When **workspaceDesc** is omitted, the existing description of the workspace is permanently reset to an empty string. Always pass the current description, read using the Get Workspace Info API, when only the name has to be changed.
- Renaming the workspace to its existing name succeeds without an error.
- The **workspaceName** should be unique within the organization. Renaming to a name that is already in use fails with error code 7111.
- The **workspaceName** can hold a maximum of 50 characters and the **workspaceDesc** can hold a maximum of 250 characters. Exceeding these limits is rejected during parameter validation.
- The name and the description are replaced atomically. Both values in the request overwrite the stored values.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Rename only (description will be cleared if not provided)**

```http
PUT /restapi/v2/workspaces/466206000000071000 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"workspaceName":"Global Sales Analytics"}
```

**Case 2 — Rename and update description simultaneously**

```http
PUT /restapi/v2/workspaces/466206000000071000 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"workspaceName":"Global Sales Analytics","workspaceDesc":"Consolidated sales reporting for all regions"}
```

**Case 3 — Update description only (pass the existing name to avoid renaming)**

```http
PUT /restapi/v2/workspaces/466206000000071000 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"workspaceName":"Sales Analytics","workspaceDesc":"Updated: Q3 2025 consolidated sales reporting"}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Rename Workspace](../../../sdk-examples/workspace-management/workspace-operations/rename-workspace.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Rename Workspace returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **`workspaceDesc` is RESET on omission** | If `workspaceDesc` is not included in the request, the workspace's existing description is permanently overwritten with an empty string. Always include the current `workspaceDesc` value (read from Get Workspace Info) to preserve it. |
| **Renaming to the same name** | Succeeds without error (idempotent for the name). |
| **Name must be unique within the org** | The new name must not be in use by another workspace in the same organisation. |
| **Dependency** | Workspace ID → any workspace list API or Get Workspace Info. Current `workspaceDesc` → Get Workspace Info. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | The new workspace name is already used by another workspace in the organisation. | Choose a name not already in use. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not an Account Admin or Organization Admin. | Ensure the caller has Account Admin or Org Admin access. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.update`. |

# Related

- [Workspace Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Workspace](create-workspace.md), [Copy Workspace](copy-workspace.md), [Delete Workspace](delete-workspace.md), [Export as Template](export-as-template.md), [Get All Workspace List](get-all-workspaces.md), [Get Owned Workspace List](get-owned-workspaces.md), [Get Shared Workspace List](get-shared-workspaces.md), [Get Workspace Secret Key](get-workspace-secret-key.md), [Get Workspace Info](get-workspace-details.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-operations/rename-workspace.md).
