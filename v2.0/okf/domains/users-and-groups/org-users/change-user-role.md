---
type: API Endpoint
title: Change User Role
description: Changes the org-level role of one or more users in the specified organization.
resource: https://analyticsapi.zoho.com/restapi/v2/users/role
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - org-users
  - put
  - usermanagement
api:
  operation_id: changeUserRole
  method: PUT
  path: "/restapi/v2/users/role"
  domain: users-and-groups
  group: org-users
  oauth_scopes:
    - ZohoAnalytics.usermanagement.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the specified organisation.
  error_codes:
    - 6089
    - 7103
    - 7301
    - 8060
    - 8061
    - 8114
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1users~1role/put"
    config_schema: ChangeUserRoleConfig
    response_schema: null
  sdk_examples: "/sdk-examples/users-and-groups/org-users/change-user-role.md"
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

**PUT `/restapi/v2/users/role`** - Change User Role (Organization Users / Users & Groups).

Changes the org-level role of one or more users in the specified organisation. Role changes take effect immediately — the user's access permissions across all workspaces adjust to reflect the new role.

> **Confirmed account requirement:** The calling user's Zoho account must be confirmed (email-verified) to invoke this API.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `changeUserRole` |
| HTTP method | PUT |
| URL | `/restapi/v2/users/role` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.usermanagement.update`](../../../foundations/oauth-scopes.md#zohoanalyticsusermanagementupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID where the role change should apply. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the specified organisation. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1users~1role/put`; CONFIG schema `ChangeUserRoleConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.usermanagement.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

This endpoint has no path parameters.

## CONFIG Parameter

CONFIG is **mandatory**. It must be sent as a form-encoded body parameter named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `emailIds` | Array of Strings | **Yes** | — | List of email addresses whose role should be changed. Maximum 1000 per request. All specified email addresses must already be members of this organisation; non-members cause the request to fail with error **8114**. The same target role is applied to all users in the list. |
| `role` | String | **Yes** | — | The new org-level role to assign to all specified users. Allowed values: `"USER"` (standard user), `"ORGADMIN"` (Organization Admin), `"VIEWER"` (read-only Viewer). **Note:** Organization Admins calling this API can only assign `"USER"` or `"VIEWER"` — they cannot promote users to `"ORGADMIN"`. Only Account Admins can assign the `"ORGADMIN"` role. |
| `domainName` | String | No | `null` | Custom domain name for client portal-based role changes. When omitted, the standard org context is used. When provided, the role change applies within the specified custom portal domain. **Note:** The `"ORGADMIN"` role cannot be assigned via a custom domain; this combination will fail with error **6089**. |

## Notes from the OpenAPI specification

- The Zoho account of the calling user must be confirmed (email verified) to invoke this API.
- A maximum of 1000 email addresses can be sent in a single request. The same role is applied to every user in the list.
- Organization Admins can assign only the **USER** and **VIEWER** roles. Promoting a user to **ORGADMIN** can be done only by the Account Admin of the organization, and any other caller fails with error code **7301**.
- The **ORGADMIN** role cannot be assigned along with **domainName**. This combination always fails with error code **6089**, irrespective of the role of the calling user.
- Every email address in the list must already be a member of the organization. Non-members cause the request to fail with error code **8114**.
- The operation is idempotent. Applying the role that a user already holds succeeds silently and raises no error.
- The role of a deactivated user can be changed. The new role takes effect when the user is reactivated.
- Demoting an Organization Admin removes their org-wide management capabilities immediately, but does not affect their workspace-level permissions.
- Setting the **VIEWER** role for a user who owns workspaces makes them read-only at the org level, but does not transfer the workspaces they own. They may continue to hold Workspace Admin access on those workspaces.
- A role change performed within a client portal domain is scoped to that portal. The role of the user in the main organization and in other portals is unaffected.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Promote a user to Organization Admin**

```http
PUT /restapi/v2/users/role HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["analyst@example.com"],"role":"ORGADMIN"}
```

**Case 2 — Downgrade multiple users to Viewer role**

```http
PUT /restapi/v2/users/role HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["contractor1@example.com","contractor2@example.com"],"role":"VIEWER"}
```

**Case 3 — Reset an Org Admin back to standard User**

```http
PUT /restapi/v2/users/role HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["formeradmin@example.com"],"role":"USER"}
```

**Case 4 — Change role of a user within a specific Client Portal domain**

Role changes within a portal domain are scoped to that portal. The user's role on the main org or other portals is unaffected.

```http
PUT /restapi/v2/users/role HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["portal.user@client.com"],"role":"VIEWER","domainName":"reports.clientbrand.com"}
```

> **Note:** `"ORGADMIN"` cannot be assigned via `domainName`. This combination always fails with error **6089** regardless of the caller's role.

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Change User Role](../../../sdk-examples/users-and-groups/org-users/change-user-role.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Change User Role returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |

## Role Values Reference

| `role` Value | Display Name | Description |
|-------------|--------------|-------------|
| `"USER"` | User | Standard user. Can own and manage workspaces they create, and access workspaces shared with them. |
| `"ORGADMIN"` | Organization Admin | Can manage users and workspaces across the org. Cannot exceed Account Admin privileges. Account Admin only. |
| `"VIEWER"` | Viewer | Read-only access. Can view reports and dashboards shared with them but cannot create or modify data. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6089](../../../foundations/error-codes.md#error-6089) | 400 | Attempted to assign `"ORGADMIN"` role via `domainName` (custom domain). | Omit `domainName` when assigning the Org Admin role. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Organisation not found. | Verify the `ZANALYTICS-ORGID` header value. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not an Account Admin or Organization Admin. | Ensure the caller has the required org-level role. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | The specified `domainName` does not exist. | Provide a valid client portal domain name configured for the org. |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | The specified `domainName` does not belong to the calling user or the org's Account Admin. | Use a domain name administered by the Account Admin of this organisation. |
| [8114](../../../foundations/error-codes.md#error-8114) | 400 | One or more specified email addresses are not members of this organisation. | Verify all email IDs using Get Users before calling this API. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.usermanagement.update`. |

# Related

- [Organization Users overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Users](get-users.md), [Add Users](add-users.md), [Remove Users](remove-users.md), [Activate Users](activate-users.md), [Deactivate Users](de-activate-users.md), [Get Org Admins](get-org-admins.md).
- [SDK examples](../../../sdk-examples/users-and-groups/org-users/change-user-role.md).
