---
type: API Endpoint
title: Change Workspace Users Status
description: Activates or deactivates one or more users in the specified workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/users/status"
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - workspace-users
  - put
  - usermanagement
api:
  operation_id: changeWorkspaceUsersStatus
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/users/status"
  domain: users-and-groups
  group: workspace-users
  oauth_scopes:
    - ZohoAnalytics.usermanagement.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: The authenticated user must be the Account Admin of the organisation that owns the workspace.
  error_codes:
    - 7103
    - 7301
    - 8060
    - 8061
    - 8119
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1users~1status/put"
    config_schema: ChangeWorkspaceUsersStatusConfig
    response_schema: null
  sdk_examples: "/sdk-examples/users-and-groups/workspace-users/change-workspace-users-status.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/user-groups-grouped-api.json"
    title: OpenAPI 3 specification - user-groups-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**PUT `/restapi/v2/workspaces/{workspace-id}/users/status`** - Change Workspace Users Status (Workspace Users / Users & Groups).

Activates or deactivates one or more users in the specified workspace. The `operation` field is mandatory and determines whether users are activated or deactivated.

- **Activate** (`"activate"`): Restores a deactivated user's access to the workspace.
- **Deactivate** (`"deactivate"`): Suspends access without removing the user. Their role and permissions are preserved and restored upon reactivation.

> **Permission note:** This API is restricted to the **Account Admin** only, regardless of the workspace-level role. Workspace Admins and Organization Admins cannot call this API.

> **Confirmed account requirement:** The calling user's Zoho account must be confirmed (email-verified) to invoke this API.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `changeWorkspaceUsersStatus` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/users/status` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.usermanagement.update`](../../../foundations/oauth-scopes.md#zohoanalyticsusermanagementupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be the Account Admin of the organisation that owns the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1users~1status/put`; CONFIG schema `ChangeWorkspaceUsersStatusConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.usermanagement.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameter

CONFIG is **mandatory**. It must be sent as a form-encoded body parameter named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `emailIds` | Array of Strings | **Yes** | — | List of email addresses whose status should be changed. Max 1000 entries. |
| `operation` | String | **Yes** | — | The status operation to perform. Allowed values: `"activate"` (restore access) or `"deactivate"` (suspend access). Any other value fails with error **8119**. |
| `domainName` | String | No | `null` | Client portal domain for portal-scoped operations. When provided, the status change applies to users within that specific portal domain. |

## Notes from the OpenAPI specification

- The Zoho account of the calling user must be confirmed (email verified) to invoke this API.
- This API is restricted to the Account Admin of the organization that owns the workspace. Workspace Admins and Organization Admins cannot invoke it and receive error code **7301**.
- A maximum of 1000 email addresses can be sent in a single request.
- The **operation** value is case-sensitive. Only **activate** and **deactivate** in lower case are valid - any other value, including **Activate** or **ACTIVATE**, fails with error code **8119** before any change is made.
- The operation is idempotent. Activating an already-active user, or deactivating an already-inactive user, succeeds silently.
- All the shares, roles and permissions of a deactivated user are preserved and are restored on reactivation.
- Always specify **domainName** when the users belong to a client portal domain.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Deactivate a user in the workspace**

```http
PUT /restapi/v2/workspaces/466206000000071000/users/status HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["on.leave@acme.com"],"operation":"deactivate"}
```

**Case 2 — Reactivate multiple users**

```http
PUT /restapi/v2/workspaces/466206000000071000/users/status HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["user1@acme.com","user2@acme.com"],"operation":"activate"}
```

**Case 3 — Client Portal: deactivate a portal user**

```http
PUT /restapi/v2/workspaces/466206000000071000/users/status HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["portal.user@client.com"],"operation":"deactivate","domainName":"reports.clientbrand.com"}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

**Permission denied (Workspace Admin or Org Admin attempting this API)**

```json
{
  "status": "failure",
  "summary": "SECURITY_NOT_PERMITTED",
  "data": {
    "errorCode": 7301,
    "errorMessage": "You do not have the permission to do this operation. Only Account Admin has the permission."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Change Workspace Users Status](../../../sdk-examples/users-and-groups/workspace-users/change-workspace-users-status.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Change Workspace Users Status returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Account Admin only** | Only Account Admins can call this API. Workspace Admins attempting this call will receive error 7301. |
| **`operation` values are case-sensitive** | Only `"activate"` and `"deactivate"` (lowercase) are valid. `"Activate"` or `"ACTIVATE"` will fail with error 8119. |
| **Idempotent status change** | Activating an already-active user or deactivating an already-inactive user both succeed silently. |
| **User data is preserved during deactivation** | All shares, roles, and permissions are retained. Reactivating the user restores their access exactly as it was. |
| **Dependency** | User email addresses → Get Workspace Users. `operation` must be `"activate"` or `"deactivate"`. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not the Account Admin of the organisation. Only Account Admin can change workspace user status. | Use the Account Admin credentials. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | The specified `domainName` does not exist. | Provide a valid client portal domain name. |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | The specified `domainName` does not belong to the org's Account Admin. | Use a domain administered by the Account Admin. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | Invalid value for `operation`. Only `"activate"` and `"deactivate"` are accepted. | Pass exactly `"activate"` or `"deactivate"` in the `operation` field. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.usermanagement.update`. |

# Related

- [Workspace Users overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Workspace Users](get-workspace-users.md), [Add Workspace Users](add-workspace-users.md), [Remove Workspace Users](delete-workspace-users.md), [Change Workspace Users Role](change-workspace-users-role.md), [Get Workspace Admins](get-workspace-admins.md), [Add Workspace Admins](add-workspace-admins.md), [Remove Workspace Admins](remove-workspace-admins.md).
- [SDK examples](../../../sdk-examples/users-and-groups/workspace-users/change-workspace-users-status.md).
