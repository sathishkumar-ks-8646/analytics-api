---
type: API Endpoint
title: Change Workspace Users Role
description: Changes the workspace-level role of one or more users in the specified workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/users/role"
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - workspace-users
  - put
  - usermanagement
api:
  operation_id: changeWorkspaceUsersRole
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/users/role"
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
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace.
  error_codes:
    - 7103
    - 7301
    - 7550
    - 8060
    - 8061
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1users~1role/put"
    config_schema: ChangeWorkspaceUsersRoleConfig
    response_schema: null
  sdk_examples: "/sdk-examples/users-and-groups/workspace-users/change-workspace-users-role.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/user-groups-grouped-api.json"
    title: OpenAPI 3 specification - user-groups-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**PUT `/restapi/v2/workspaces/{workspace-id}/users/role`** - Change Workspace Users Role (Workspace Users / Users & Groups).

Changes the workspace-level role of one or more users in the specified workspace. Supports the same two modes as Add Workspace Users:

- **Simple mode** — change all specified emails to the same role.
- **Bulk mode** — change multiple groups of users to different roles in one request (up to 20 groups).

> **Permission note:** This API requires **Account Admin or Organization Admin** access. Workspace Admins cannot call this API.

> **Confirmed account requirement:** The calling user's Zoho account must be confirmed (email-verified) to invoke this API.

From the OpenAPI specification:

Changes the workspace-level role of one or more users in the specified workspace.

The users can be supplied in two ways - as a flat list of email addresses that all move to a single role, or as up to 20 groups of users that each move to their own role and client portal domain.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `changeWorkspaceUsersRole` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/users/role` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.usermanagement.update`](../../../foundations/oauth-scopes.md#zohoanalyticsusermanagementupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1users~1role/put`; CONFIG schema `ChangeWorkspaceUsersRoleConfig` |

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

**Simple mode:**

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `emailIds` | Array of Strings | **Yes** | — | Email addresses whose role should be changed. Max 1000 entries. |
| `role` | String | **Yes** | — | New workspace-level role. Allowed values: `"WORKSPACEADMIN"`, `"USER"`, or a custom role name defined in the org. |
| `domainName` | String | No | `null` | Portal domain for portal-scoped role changes. |

**Bulk mode:**

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `users` | Array of Objects | **Yes** | — | Up to 20 user-group objects. Each object requires `emailIds` and `role`. |
| `users[].emailIds` | Array of Strings | **Yes** | — | Email addresses for this group. Max 1000 per group. |
| `users[].role` | String | **Yes** | — | New role for this group. Same allowed values as simple mode. |
| `users[].domainName` | String | No | `null` | Portal domain for this group. |

## Notes from the OpenAPI specification

- The Zoho account of the calling user must be confirmed (email verified) to invoke this API.
- This API requires Account Admin or Organization Admin access. Workspace Admins cannot invoke it and receive error code **7301**, which prevents a Workspace Admin from promoting themselves or demoting other admins.
- A maximum of 1000 email addresses can be sent in a single list, and a maximum of 20 groups can be sent in the **users** array. Split larger operations into multiple calls.
- A custom role name must exactly match an existing custom role defined in the organization. An unknown role name fails with error code **7550**.
- The operation is idempotent. Applying the role that a user already holds succeeds silently.
- Assigning the **USER** role to a current Workspace Admin removes their admin capabilities immediately, while their workspace access continues as a regular user.
- Always specify **domainName** for portal users, so that the correct portal user record is updated. Without it, the change is attempted in the standard Zoho Analytics domain.
- **VIEWER** is an org-level role and is not a valid workspace-level role value. At workspace level, org-level Viewers are listed as **User**.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Promote a user to Workspace Admin**

```http
PUT /restapi/v2/workspaces/466206000000071000/users/role HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["senior.analyst@acme.com"],"role":"WORKSPACEADMIN"}
```

**Case 2 — Bulk mode: change two groups to different roles**

```http
PUT /restapi/v2/workspaces/466206000000071000/users/role HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"users":[{"emailIds":["user1@acme.com","user2@acme.com"],"role":"WORKSPACEADMIN"},{"emailIds":["user3@acme.com","user4@acme.com"],"role":"USER"}]}
```

**Case 3 — Assign a custom role**

```http
PUT /restapi/v2/workspaces/466206000000071000/users/role HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["analyst@acme.com"],"role":"AnalystRole"}
```

**Case 4 — Client Portal: change role of a portal user**

```http
PUT /restapi/v2/workspaces/466206000000071000/users/role HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["portal.user@client.com"],"role":"USER","domainName":"reports.clientbrand.com"}
```

**Case 5 — Bulk mode with mixed portal domains**

```http
PUT /restapi/v2/workspaces/466206000000071000/users/role HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"users":[{"emailIds":["user1@client.com"],"role":"WORKSPACEADMIN","domainName":"reports.clientbrand.com"},{"emailIds":["partner@partner.io"],"role":"USER","domainName":"analytics.partnerportal.io"}]}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Change Workspace Users Role](../../../sdk-examples/users-and-groups/workspace-users/change-workspace-users-role.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Change Workspace Users Role returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Requires Account Admin or Organization Admin** | Workspace Admins cannot change user roles. This prevents Workspace Admins from self-promoting or demoting other admins. |
| **Same role assignment is idempotent** | Setting a user to the role they already have succeeds without error. |
| **Demoting a Workspace Admin** | Assigning `"USER"` to a current Workspace Admin removes their admin capabilities immediately. Their workspace access continues as a regular User. |
| **`role` value must be a valid workspace role** | Use `"WORKSPACEADMIN"`, `"USER"`, or the exact name of a custom role defined in the org. Invalid values fail with error 7550. |
| **Portal users require `domainName`** | Specify `domainName` for users in a portal domain to ensure the correct user record is updated. |
| **Bulk mode maximum: 20 entries** | The `users` array is capped at 20 entries per request. Split larger operations into multiple calls. |
| **Dependency** | User email addresses → Get Workspace Users. Valid role names for custom roles → org-level role management APIs. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not an Account Admin or Organization Admin of the organisation. Workspace Admins cannot call this API. | Use Account Admin or Organization Admin credentials. |
| [7550](../../../foundations/error-codes.md#error-7550) | 400 | The specified `role` name does not exist as a custom role in the org. | Use `"WORKSPACEADMIN"`, `"USER"`, or an exact custom role name. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | The specified `domainName` does not exist. | Provide a valid client portal domain name. |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | The specified `domainName` does not belong to the org's Account Admin. | Use a domain administered by the Account Admin. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.usermanagement.update`. |

# Related

- [Workspace Users overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Workspace Users](get-workspace-users.md), [Add Workspace Users](add-workspace-users.md), [Remove Workspace Users](delete-workspace-users.md), [Change Workspace Users Status](change-workspace-users-status.md), [Get Workspace Admins](get-workspace-admins.md), [Add Workspace Admins](add-workspace-admins.md), [Remove Workspace Admins](remove-workspace-admins.md).
- [SDK examples](../../../sdk-examples/users-and-groups/workspace-users/change-workspace-users-role.md).
