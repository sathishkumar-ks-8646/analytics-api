---
type: API Endpoint
title: Get Users
description: "Returns the list of all the users who are members of the specified organization, along with their current status and org-level role."
resource: https://analyticsapi.zoho.com/restapi/v2/users
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - org-users
  - get
  - usermanagement
api:
  operation_id: getUsers
  method: GET
  path: "/restapi/v2/users"
  domain: users-and-groups
  group: org-users
  oauth_scopes:
    - ZohoAnalytics.usermanagement.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the specified organisation.
  error_codes:
    - 7103
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1users/get"
    config_schema: null
    response_schema: GetUsersResponse
  sdk_examples: "/sdk-examples/users-and-groups/org-users/get-users.md"
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

**GET `/restapi/v2/users`** - Get Users (Organization Users / Users & Groups).

Returns the list of all users who are members of the specified organisation, along with their current status (active/inactive) and org-level role.

> This API has no CONFIG parameter.

From the OpenAPI specification:

Returns the list of all the users who are members of the specified organization, along with their current status and org-level role.

The org-level role governs what the user can do across the entire organization. It is distinct from the workspace-level role, which governs what the user can do within a specific workspace and is managed using the workspace sharing APIs.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getUsers` |
| HTTP method | GET |
| URL | `/restapi/v2/users` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.usermanagement.read`](../../../foundations/oauth-scopes.md#zohoanalyticsusermanagementread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID whose user list to retrieve. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the specified organisation. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1users/get`; response schema `GetUsersResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.usermanagement.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

This endpoint has no path parameters.

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- Both the Account Admin and the Organization Admins of the organization can invoke this API.
- Deactivated users continue to be listed in the response with **status** set to **false**. They are not removed from the list.
- A user who has been invited but has not yet accepted the invitation is not listed until they accept and join the organization.
- The **domainName** field is returned for every user only when the Account Admin of the organization is also a Client Portal Admin. When the Account Admin is not a Client Portal Admin, only **emailId**, **status** and **role** are returned.
- A user added through a client portal domain is scoped to that portal. Such users access Zoho Analytics only through the branded portal URL and do not appear as standard organization members.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `data.users` | Array | List of all users in the organisation. |
| `users[].emailId` | String | Email address of the user. |
| `users[].status` | Boolean | `true` if the user is currently active (can log in and use the org). `false` if the user has been deactivated. |
| `users[].role` | String | The user's current org-level role. Possible values: `"Account Admin"`, `"Organization Admin"`, `"User"`, `"Viewer"`. |
| `users[].domainName` | String | *(Present only when the Account Admin is also a Client Portal Admin.)* The portal domain through which this user was added. Users added via the standard org show the default analytics domain URL. Users added via a custom client portal show that portal's domain URL. |

# Examples

## Sample Requests

**Case 1 — Account Admin listing all org users**

```http
GET /restapi/v2/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Org Admin listing users for their org**

```http
GET /restapi/v2/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
ZANALYTICS-ORGID: 700000654321
```

**Case 3 — Account Admin who is also a Client Portal Admin (users include `domainName` field)**

```http
GET /restapi/v2/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Org with mixed roles (Account Admin perspective)**
```json
{
  "status": "success",
  "summary": "Get users",
  "data": {
    "users": [
      {
        "emailId": "admin@acme.com",
        "status": true,
        "role": "Account Admin"
      },
      {
        "emailId": "orgadmin@acme.com",
        "status": true,
        "role": "Organization Admin"
      },
      {
        "emailId": "analyst@acme.com",
        "status": true,
        "role": "User"
      },
      {
        "emailId": "viewer1@acme.com",
        "status": true,
        "role": "Viewer"
      },
      {
        "emailId": "inactive.user@acme.com",
        "status": false,
        "role": "User"
      }
    ]
  }
}
```

**Case 2 — Org with only a few members (no Org Admins)**
```json
{
  "status": "success",
  "summary": "Get users",
  "data": {
    "users": [
      {
        "emailId": "owner@example.com",
        "status": true,
        "role": "Account Admin"
      },
      {
        "emailId": "user1@example.com",
        "status": true,
        "role": "User"
      },
      {
        "emailId": "viewer@example.com",
        "status": true,
        "role": "Viewer"
      }
    ]
  }
}
```

**Case 3 — Client Portal Admin response (each user entry includes `domainName`)**

When the Account Admin is also a Client Portal Admin, the response includes a `domainName` field for every user indicating which portal domain they belong to. Users added via the standard Zoho Analytics domain show the default analytics domain, while users added via a custom client portal show their portal's domain URL.

```json
{
  "status": "success",
  "summary": "Get users",
  "data": {
    "users": [
      {
        "emailId": "admin@example.com",
        "status": true,
        "role": "Account Admin",
        "domainName": "analytics.zoho.com"
      },
      {
        "emailId": "standard.user@example.com",
        "status": true,
        "role": "User",
        "domainName": "analytics.zoho.com"
      },
      {
        "emailId": "portal.user1@client.com",
        "status": true,
        "role": "User",
        "domainName": "reports.clientbrand.com"
      },
      {
        "emailId": "portal.user2@client.com",
        "status": true,
        "role": "Viewer",
        "domainName": "reports.clientbrand.com"
      },
      {
        "emailId": "portal.user3@partner.com",
        "status": false,
        "role": "User",
        "domainName": "analytics.partnerportal.io"
      }
    ]
  }
}
```

> **`domainName` in response:** Only present when the Account Admin is a Client Portal Admin. The value distinguishes which portal domain each user was added through — allowing the admin to identify users by their portal context. Users added via the standard org (without a custom domain) show the default Zoho Analytics domain.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Users](../../../sdk-examples/users-and-groups/org-users/get-users.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Organisation not found. | Verify the `ZANALYTICS-ORGID` header value. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not an Account Admin or Organization Admin of the organisation. | Only Account Admins and Organization Admins can list org users. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.usermanagement.read`. |

# Related

- [Organization Users overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Add Users](add-users.md), [Remove Users](remove-users.md), [Activate Users](activate-users.md), [Deactivate Users](de-activate-users.md), [Change User Role](change-user-role.md), [Get Org Admins](get-org-admins.md).
- [SDK examples](../../../sdk-examples/users-and-groups/org-users/get-users.md).
