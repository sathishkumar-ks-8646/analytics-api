---
type: API Endpoint
title: Delete Workspace
description: "Permanently deletes the specified workspace and all of its contents — tables, views, dashboards, formulas, import configurations, and all sharing settings."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-operations
  - delete
  - modeling
api:
  operation_id: deleteWorkspace
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}"
  domain: workspace-management
  group: workspace-operations
  oauth_scopes:
    - ZohoAnalytics.modeling.delete
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 204
  response_content_types: []
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace.
  error_codes:
    - 7103
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}/delete"
    config_schema: null
    response_schema: null
  sdk_examples: "/sdk-examples/workspace-management/workspace-operations/delete-workspace.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}`** - Delete Workspace (Workspace Operations / Workspace Management).

Permanently deletes the specified workspace and all of its contents — tables, views, dashboards, formulas, import configurations, and all sharing settings. This operation is irreversible.

> This API accepts an optional CONFIG parameter. No CONFIG fields are required for standard use.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deleteWorkspace` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingdelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 204 with no body |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}/delete` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.delete`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | The ID of the workspace. It can be obtained using any of the workspace list APIs. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- Delete Workspace returns a bare HTTP 204 No Content on success. There is no response body and no **status** or **summary** JSON to parse, so check only the HTTP status code. A JSON payload is returned only on failure.
- The deletion is permanent. There is no trash or recycle mechanism for workspaces, and the workspace along with all its views, data, import configurations and sharing settings cannot be recovered.
- All the sharing configurations of the workspace are removed. Users who had access to the views in this workspace lose that access at the moment of deletion.
- The workspace level admin role of the Workspace Admins is removed. Their organization membership and their access to the other workspaces are not affected.
- Any scheduled or in-progress data import job in the workspace is cancelled.
- This API accepts an optional CONFIG parameter. No CONFIG key is required for the standard use of this API.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Delete a workspace**

```http
DELETE /restapi/v2/workspaces/466206000000071000 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Delete Workspace](../../../sdk-examples/workspace-management/workspace-operations/delete-workspace.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Delete Workspace returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Permanent deletion — no recycle bin** | Once deleted, the workspace and all its views, data, import configurations, and sharing settings cannot be recovered. |
| **All access revoked immediately** | Users who had access to views in this workspace lose that access at the moment of deletion. |
| **Workspace Admins' org membership unaffected** | Deleting a workspace removes the users' workspace-level admin role but does not affect their org-level membership or other workspace access. |
| **Active import jobs are cancelled** | Any scheduled or in-progress data imports are stopped. |
| **`CONFIG` parameter is optional** | If no CONFIG is provided, the deletion proceeds with defaults. |
| **Dependency** | Workspace ID → any workspace list API. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not an Account Admin or Organization Admin. | Ensure the caller has Account Admin or Org Admin access. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.delete`. |

# Related

- [Workspace Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Workspace](create-workspace.md), [Copy Workspace](copy-workspace.md), [Rename Workspace](rename-workspace.md), [Export as Template](export-as-template.md), [Get All Workspace List](get-all-workspaces.md), [Get Owned Workspace List](get-owned-workspaces.md), [Get Shared Workspace List](get-shared-workspaces.md), [Get Workspace Secret Key](get-workspace-secret-key.md), [Get Workspace Info](get-workspace-details.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-operations/delete-workspace.md).
