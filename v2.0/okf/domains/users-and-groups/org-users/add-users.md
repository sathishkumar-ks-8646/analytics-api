---
type: API Endpoint
title: Add Users
description: Adds one or more users to the specified organization.
resource: https://analyticsapi.zoho.com/restapi/v2/users
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - org-users
  - post
  - usermanagement
api:
  operation_id: addUsers
  method: POST
  path: "/restapi/v2/users"
  domain: users-and-groups
  group: org-users
  oauth_scopes:
    - ZohoAnalytics.usermanagement.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the specified organisation.
  error_codes:
    - 6004
    - 6026
    - 6071
    - 6089
    - 7103
    - 7301
    - 8060
    - 8061
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1users/post"
    config_schema: AddUsersConfig
    response_schema: null
  sdk_examples: "/sdk-examples/users-and-groups/org-users/add-users.md"
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

**POST `/restapi/v2/users`** - Add Users (Organization Users / Users & Groups).

Adds one or more users to the specified organisation. The invited users receive an email notification. If the users are new to Zoho, they are prompted to create a Zoho account before accepting the invitation.

> **Confirmed account requirement:** The calling user's Zoho account must be confirmed (email-verified) to invoke this API.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `addUsers` |
| HTTP method | POST |
| URL | `/restapi/v2/users` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.usermanagement.create`](../../../foundations/oauth-scopes.md#zohoanalyticsusermanagementcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID to add users to. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the specified organisation. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1users/post`; CONFIG schema `AddUsersConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.usermanagement.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

This endpoint has no path parameters.

## CONFIG Parameter

CONFIG is **mandatory**. It must be sent as a form-encoded body parameter named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `emailIds` | Array of Strings | **Yes** | — | List of email addresses to invite. Maximum of 1000 email IDs per request. Each entry must be a valid email address. |
| `role` | String | No | `"USER"` | The org-level role to assign to the added users. Allowed values: `"USER"` (standard user), `"ORGADMIN"` (Organization Admin), `"VIEWER"` (read-only Viewer). When omitted, defaults to `"USER"`. **Note:** Organization Admins calling this API can only assign `"USER"` or `"VIEWER"` roles — they cannot assign `"ORGADMIN"`. Only Account Admins can grant the Org Admin role. |
| `domainName` | String | No | `null` | Custom domain name for client portal-based user management. When provided, the user is added in the context of the specified custom portal domain. When omitted, users are added to the standard Zoho Analytics org. **Note:** The `"ORGADMIN"` role cannot be assigned via a custom domain (`domainName`); this combination will fail with error **6089**. |

## Notes from the OpenAPI specification

- The Zoho account of the calling user must be confirmed (email verified) to invoke this API.
- A maximum of 1000 email addresses can be sent in a single request.
- The request is applied as a single batch. If any email address in the list is already a member of the organization, the request fails with error code **6071** and none of the users are added.
- When **role** is not provided, the invited users join with the **USER** role.
- Organization Admins can assign only the **USER** and **VIEWER** roles. Only the Account Admin of the organization can assign the **ORGADMIN** role.
- The **ORGADMIN** role cannot be assigned along with **domainName**. This combination always fails with error code **6089**, irrespective of the role of the calling user.
- If the addition would exceed the user seat limit of the plan, the request fails with error code **6004** before any user is added. Free plans do not support additional users and fail with error code **6026**.
- An invited user is not listed by the Get Users API until they accept the invitation and join the organization.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Add two users with default User role**

```http
POST /restapi/v2/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["alice@example.com","bob@example.com"]}
```

**Case 2 — Add a user with Viewer role**

```http
POST /restapi/v2/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["viewer@example.com"],"role":"VIEWER"}
```

**Case 3 — Add a user with Org Admin role (Account Admin only)**

```http
POST /restapi/v2/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["orgadmin@example.com"],"role":"ORGADMIN"}
```

**Case 4 — Add users to a specific Client Portal domain**

When the Account Admin manages multiple client portals, this scopes the addition to a single portal. Users added this way are associated with that portal domain and appear as portal users in the Get Users response.

```http
POST /restapi/v2/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["client.user1@client.com","client.user2@client.com"],"role":"USER","domainName":"reports.clientbrand.com"}
```

**Case 5 — Add a Viewer to a specific Client Portal domain**

```http
POST /restapi/v2/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["readonly.client@client.com"],"role":"VIEWER","domainName":"reports.clientbrand.com"}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Add Users](../../../sdk-examples/users-and-groups/org-users/add-users.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Add Users returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6004](../../../foundations/error-codes.md#error-6004) | 400 | Adding these users would exceed the organisation's user seat limit under the current plan. | Upgrade the plan to accommodate more users, or remove unused user accounts before adding new ones. |
| [6026](../../../foundations/error-codes.md#error-6026) | 400 | The current plan does not support adding extra users (free plan restriction). | Upgrade to a paid plan to invite additional users. |
| [6071](../../../foundations/error-codes.md#error-6071) | 400 | One or more of the specified email addresses is already a member of this organisation. | Remove already-existing email addresses from the `emailIds` list and retry. |
| [6089](../../../foundations/error-codes.md#error-6089) | 400 | Attempted to assign `"ORGADMIN"` role via a custom domain (`domainName`). Organization Admin role cannot be assigned through a custom portal domain. | Omit `domainName` when assigning the `"ORGADMIN"` role, or use a different role for domain-based additions. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Organisation not found. | Verify the `ZANALYTICS-ORGID` header value. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not an Account Admin or Organization Admin of the organisation. | Ensure the caller has the required role. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | The specified `domainName` does not exist. | Provide a valid client portal domain name configured for the org. |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | The specified `domainName` does not belong to the calling user or the org's Account Admin. | Use a domain name that is administered by the Account Admin of this organisation. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.usermanagement.create`. |

# Related

- [Organization Users overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Users](get-users.md), [Remove Users](remove-users.md), [Activate Users](activate-users.md), [Deactivate Users](de-activate-users.md), [Change User Role](change-user-role.md), [Get Org Admins](get-org-admins.md).
- [SDK examples](../../../sdk-examples/users-and-groups/org-users/add-users.md).
