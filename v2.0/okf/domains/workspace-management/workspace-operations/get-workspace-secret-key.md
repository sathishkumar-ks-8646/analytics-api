---
type: API Endpoint
title: Get Workspace Secret Key
description: Returns the secret key for the specified workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/secretkey"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-operations
  - get
  - metadata
api:
  operation_id: getWorkspaceSecretKey
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/secretkey"
  domain: workspace-management
  group: workspace-operations
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: query
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace.
  error_codes:
    - 7103
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1secretkey/get"
    config_schema: GetWorkspaceSecretKeyConfig
    response_schema: GetWorkspaceSecretKeyResponse
  sdk_examples: "/sdk-examples/workspace-management/workspace-operations/get-workspace-secret-key.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/secretkey`** - Get Workspace Secret Key (Workspace Operations / Workspace Management).

Returns the secret key for the specified workspace. This key is used as the `workspaceKey` parameter when performing a cross-organisation Copy Workspace operation — it authorises the copying of the workspace to a different organisation.

The key can optionally be regenerated, which invalidates the previous key. Any previously shared `workspaceKey` values become invalid after regeneration.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getWorkspaceSecretKey` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/secretkey` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - optional |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1secretkey/get`; CONFIG schema `GetWorkspaceSecretKeyConfig`; response schema `GetWorkspaceSecretKeyResponse` |

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

## CONFIG Parameter

CONFIG is optional. It must be sent as a query parameter or form-encoded body parameter named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `regenerateKey` | Boolean | No | `false` | When `false` (default): returns the existing secret key without modification. When `true`: generates a new random secret key, stores it as the workspace's new secret key, and returns it. The previous key is permanently invalidated — any party that held the old key can no longer copy this workspace using it. |

## Notes from the OpenAPI specification

- Setting **regenerateKey** to false, which is the default, is safe to invoke repeatedly. The existing key is returned each time, and a key is generated on the first call when none exists.
- Setting **regenerateKey** to true invalidates the previous key immediately. A cross-organization copy attempted with the old key after regeneration fails with error code 8024. A copy operation that had already started before the regeneration is not affected, as the key is validated only at the start of the copy.
- The workspace secret key is returned only by this API. It is not present in the response of the Get Workspace Info, the Get All Workspace List or any other API.
- Only the Account Admins and the Organization Admins of the organization that owns the workspace can retrieve the key.
- As this is a GET request, the CONFIG value should be stringified and URL encoded before it is sent.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `data.workspaceKey` | String | The workspace's current secret key (hex string). Pass this as `workspaceKey` in the Copy Workspace CONFIG when copying to a different organisation. |

# Examples

## Sample Requests

**Case 1 — Retrieve the existing secret key**

```http
GET /restapi/v2/workspaces/466206000000071000/secretkey HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Regenerate and retrieve a new secret key**

```http
GET /restapi/v2/workspaces/466206000000071000/secretkey HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"regenerateKey":true}
```

## Sample Responses

**HTTP 200 OK** — Key returned (or regenerated and returned).

```json
{
  "status": "success",
  "summary": "Get workspace secretkey",
  "data": {
    "workspaceKey": "02aee9b66f299843c961d3712fe09684"
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Workspace Secret Key](../../../sdk-examples/workspace-management/workspace-operations/get-workspace-secret-key.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`regenerateKey=false` (default) is safe to call repeatedly** | Returns the current key each time. If no key has been generated yet, one is created on the first call. |
| **`regenerateKey=true` invalidates the old key immediately** | Any cross-org copy attempt using the old key after regeneration will fail with error 8024. In-progress copy operations started before regeneration are not affected. |
| **Key is never in other API responses** | The workspace secret key is not returned by Get Workspace Info, Get All Workspace List, or any other API — only this dedicated endpoint returns it. |
| **Dependency** | Workspace ID → any workspace list API. The returned key is used as `workspaceKey` in Copy Workspace. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not an Account Admin or Organization Admin. | Ensure the caller has Account Admin or Org Admin access. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Workspace Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Workspace](create-workspace.md), [Copy Workspace](copy-workspace.md), [Rename Workspace](rename-workspace.md), [Delete Workspace](delete-workspace.md), [Export as Template](export-as-template.md), [Get All Workspace List](get-all-workspaces.md), [Get Owned Workspace List](get-owned-workspaces.md), [Get Shared Workspace List](get-shared-workspaces.md), [Get Workspace Info](get-workspace-details.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-operations/get-workspace-secret-key.md).
