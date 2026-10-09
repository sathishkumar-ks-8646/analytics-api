---
type: API Endpoint
title: Add Workspace Users
description: Adds one or more users to the specified workspace with a given workspace-level role.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/users"
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - workspace-users
  - post
  - usermanagement
api:
  operation_id: addWorkspaceUsers
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/users"
  domain: users-and-groups
  group: workspace-users
  oauth_scopes:
    - ZohoAnalytics.usermanagement.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access.
  error_codes:
    - 7103
    - 7301
    - 7550
    - 8060
    - 8061
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1users/post"
    config_schema: AddWorkspaceUsersConfig
    response_schema: null
  sdk_examples: "/sdk-examples/users-and-groups/workspace-users/add-workspace-users.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/users`** - Add Workspace Users (Workspace Users / Users & Groups).

Adds one or more users to the specified workspace with a given workspace-level role. Supports two modes:

- **Simple mode** — add a flat list of emails all with the same role.
- **Bulk mode** — add multiple groups of users, each group with a different role or domain, in a single request. Up to 20 groups per request.

> **Confirmed account requirement:** The calling user's Zoho account must be confirmed (email-verified) to invoke this API.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `addWorkspaceUsers` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/users` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.usermanagement.create`](../../../foundations/oauth-scopes.md#zohoanalyticsusermanagementcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1users/post`; CONFIG schema `AddWorkspaceUsersConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.usermanagement.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameter

CONFIG is **mandatory**. It must be sent as a form-encoded body parameter named `CONFIG`.

**Simple mode** (single role for all emails):

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `emailIds` | Array of Strings | **Yes** | — | List of email addresses to add. Max 1000 entries. |
| `role` | String | No | `"USER"` | Workspace-level role to assign. Allowed values: `"WORKSPACEADMIN"` (Workspace Admin), `"USER"` (standard user), or the exact name of a custom role defined in the org. When omitted, defaults to `"USER"`. |
| `domainName` | String | No | `null` | Client portal domain for portal-scoped additions. When omitted, users are added in the standard Zoho Analytics domain context. |

**Bulk mode** (different roles or domains per group):

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `users` | Array of Objects | **Yes** | — | Up to 20 user-group objects. Each object contains `emailIds` (required), `role`, and optionally `domainName`. When `users` is present, the root `emailIds`/`role`/`domainName` fields are ignored. |
| `users[].emailIds` | Array of Strings | **Yes** | — | Email addresses for this group. Max 1000 per group. |
| `users[].role` | String | No | `"USER"` | Workspace-level role for this group. Same allowed values as simple mode. |
| `users[].domainName` | String | No | `null` | Portal domain for this group. Allows adding users from different portals in one request. |

## Notes from the OpenAPI specification

- The Zoho account of the calling user must be confirmed (email verified) to invoke this API.
- The calling user must be a Workspace Admin of the workspace. Account Admins and Organization Admins also have access.
- A maximum of 1000 email addresses can be sent in a single list, and a maximum of 20 groups can be sent in the **users** array. Split larger operations into multiple calls.
- When **role** is not provided, the users are added with the workspace-level **USER** role.
- Adding a user who already has access to the workspace updates their role to the specified role. Re-adding a user with the role they already hold succeeds silently.
- A custom role name must exactly match an existing custom role defined in the organization. An unknown role name fails with error code **7550**.
- Always specify **domainName** for portal users. Portal-only users do not exist in the standard Zoho Analytics domain, and an addition attempted without the domain may fail.
- No prerequisite API call is needed to construct the request. Invoke Get Workspace Users afterwards to verify the additions.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Simple mode: add two standard users**

```http
POST /restapi/v2/workspaces/466206000000071000/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["alice@acme.com","bob@acme.com"],"role":"USER"}
```

**Case 2 — Simple mode: add a Workspace Admin**

```http
POST /restapi/v2/workspaces/466206000000071000/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["wsadmin@acme.com"],"role":"WORKSPACEADMIN"}
```

**Case 3 — Bulk mode: add two groups with different roles in one call**

```http
POST /restapi/v2/workspaces/466206000000071000/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"users":[{"emailIds":["lead.analyst@acme.com"],"role":"WORKSPACEADMIN"},{"emailIds":["viewer1@acme.com","viewer2@acme.com"],"role":"USER"}]}
```

**Case 4 — Client Portal: add portal users with a specific domain**

```http
POST /restapi/v2/workspaces/466206000000071000/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["portal.user@client.com"],"role":"USER","domainName":"reports.clientbrand.com"}
```

**Case 5 — Bulk mode with mixed portal domains**

```http
POST /restapi/v2/workspaces/466206000000071000/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"users":[{"emailIds":["user1@client.com","user2@client.com"],"role":"USER","domainName":"reports.clientbrand.com"},{"emailIds":["partner@partner.io"],"role":"USER","domainName":"analytics.partnerportal.io"}]}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Add Workspace Users](../../../sdk-examples/users-and-groups/workspace-users/add-workspace-users.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Add Workspace Users returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **`role` defaults to `"USER"` if omitted** | When `role` is not specified in a user entry, the user is added with the workspace-level User role. |
| **Adding an existing workspace user** | If the user is already in the workspace, their role is updated to the specified role. This is idempotent for the same role — re-adding with the same role succeeds silently. |
| **Custom role must exist in the org** | The `role` value must exactly match an existing custom role name. Invalid role names fail with error 7550. |
| **Portal users require `domainName`** | Portal-only users do not exist in the standard Zoho Analytics domain. Always specify `domainName` when adding users who belong to a portal domain. |
| **Bulk mode maximum: 20 groups per request** | Each element in the `users` array can have different `emailIds` and `role`. The array is capped at 20 entries — split larger operations. |
| **Dependency** | No prerequisite API call needed to construct the request. To verify additions, call Get Workspace Users afterward. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not a Workspace Admin, Account Admin, or Organization Admin of the workspace. | Ensure the caller has at least Workspace Admin access. |
| [7550](../../../foundations/error-codes.md#error-7550) | 400 | The specified `role` name does not exist as a custom role in the org. | Use `"WORKSPACEADMIN"`, `"USER"`, or an exact custom role name from the org. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | The specified `domainName` does not exist. | Provide a valid client portal domain name configured for the org. |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | The specified `domainName` does not belong to the org's Account Admin. | Use a domain administered by the Account Admin of this organisation. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.usermanagement.create`. |

# Related

- [Workspace Users overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Workspace Users](get-workspace-users.md), [Remove Workspace Users](delete-workspace-users.md), [Change Workspace Users Status](change-workspace-users-status.md), [Change Workspace Users Role](change-workspace-users-role.md), [Get Workspace Admins](get-workspace-admins.md), [Add Workspace Admins](add-workspace-admins.md), [Remove Workspace Admins](remove-workspace-admins.md).
- [SDK examples](../../../sdk-examples/users-and-groups/workspace-users/add-workspace-users.md).
