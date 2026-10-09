---
type: API Endpoint
title: Get My Permissions
description: Returns the permissions that the requesting user holds on the specified view.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share/mypermissions"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - sharing
  - get
  - share
api:
  operation_id: getUserPermissions
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share/mypermissions"
  domain: share-and-publish
  group: sharing
  oauth_scopes:
    - ZohoAnalytics.share.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "Any authenticated user with at least Read-Only access to <view-id> (i.e., any user the view has been shared with, or the view's owner/Workspace Admin)."
  error_codes:
    - 7301
  openapi:
    file: "/references/openapi/share-publish-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1share~1mypermissions/get"
    config_schema: null
    response_schema: GetUserPermissionsResponse
  sdk_examples: "/sdk-examples/share-and-publish/sharing/get-user-permissions.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/share-publish-grouped-api.json"
    title: OpenAPI 3 specification - share-publish-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share/mypermissions`** - Get My Permissions (Sharing / Share & Publish).

Returns the effective permission set the **calling user** currently has on a specific view.

> This API has no CONFIG parameter.

> **Deprecated alias:** `/restapi/v2/workspaces/<workspace-id>/views/<view-id>/share/mypermissions` is the original path for this same API and continues to function, but is deprecated in favor of `/share/userpermissions`. New integrations should use `/share/userpermissions`.

From the OpenAPI specification:

Returns the permissions that the requesting user holds on the specified view. The permissions returned are the effective ones, whether they were granted directly to the user or inherited through a group.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getUserPermissions` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share/mypermissions` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.share.read`](../../../foundations/oauth-scopes.md#zohoanalyticsshareread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | Any authenticated user with at least Read-Only access to <view-id> (i.e., any user the view has been shared with, or the view's owner/Workspace Admin). See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1share~1mypermissions/get`; response schema `GetUserPermissionsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.share.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- The permissions are returned for the user whose access token is used in the request, not for an arbitrary user.
- The endpoint path retains the `mypermissions` segment.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `permissions` | JSONObject | The calling user's effective permission set on `<view-id>`. Same booleans as [`permissions` Fields](share-views.md#permissions-fields); a Workspace Admin/owner is granted all applicable permissions as `true` by default. `accessAdminPresets` and `createPreset` may additionally appear as `true` for users with preset-related access even without other write permissions. |

# Examples

## Sample Requests

**Case 1 — Current path**

```http
GET /restapi/v2/workspaces/137687000271334001/views/137687000006991601/share/userpermissions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Deprecated alias (still functional)**

```http
GET /restapi/v2/workspaces/137687000271334001/views/137687000006991601/share/mypermissions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — Workspace Admin (full permissions)**

```json
{
    "status": "success",
    "summary": "Get user permissions",
    "data": {
        "permissions": {
            "read": true,
            "export": true,
            "vud": true,
            "addRow": true,
            "updateRow": true,
            "deleteRow": true,
            "deleteAllRows": true,
            "importAppend": true,
            "importAddOrUpdate": true,
            "importDeleteAllAdd": true,
            "importDeleteUpdateAdd": true,
            "drillDown": true,
            "share": true,
            "discussion": true,
            "insight": false
        }
    }
}
```

**HTTP 200 OK — Shared user with read-only + VUD + drill-down (Client Portal)**

```json
{
    "status": "success",
    "summary": "Get user permissions",
    "data": {
        "permissions": {
            "read": true,
            "export": true,
            "vud": true,
            "addRow": false,
            "updateRow": false,
            "deleteRow": false,
            "deleteAllRows": false,
            "importAppend": false,
            "importAddOrUpdate": false,
            "importDeleteAllAdd": false,
            "importDeleteUpdateAdd": false,
            "drillDown": true,
            "share": false,
            "discussion": false,
            "insight": false
        }
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get My Permissions](../../../sdk-examples/share-and-publish/sharing/get-user-permissions.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Self-service only** | This API always reports the *calling* user's own permissions — there is no parameter to check another user's permissions; use [Get Shared Details](get-shared-details-for-views.md) (as the Workspace Admin) to inspect other users' shares. |
| **Two equivalent paths** | `/share/mypermissions` (deprecated) and `/share/userpermissions` (current) return an identical response — both map to the same underlying `getUserPermissions` implementation. |
| **Owner/Admin sees full access** | For a view's owner or the Workspace Admin, all applicable permission booleans are returned as `true` even though no explicit share record exists for them. |
| **Dependency** | [Get Views](../../views-management/view-operations/overview.md) → `viewId` → Get My Permissions. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The calling user has no access at all to `<view-id>` (view does not belong to the workspace, or user has neither ownership nor a share). | Verify `<view-id>` belongs to `<workspace-id>` and that the calling user has been shared this view. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Sharing overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Workspace Shared Details](get-workspace-shared-details.md), [Share Views](share-views.md), [Update Shared Details](update-shared-details-for-view.md), [Get Shared Details](get-shared-details-for-views.md), [Remove Shared Views](remove-share.md).
- [SDK examples](../../../sdk-examples/share-and-publish/sharing/get-user-permissions.md).
