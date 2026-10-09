---
type: API Endpoint
title: Get Workspace Users
description: "Returns the list of all the users who have access to the specified workspace, along with their workspace-level role and active status."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/users"
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - workspace-users
  - get
  - usermanagement
api:
  operation_id: getWorkspaceUsers
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/users"
  domain: users-and-groups
  group: workspace-users
  oauth_scopes:
    - ZohoAnalytics.usermanagement.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access.
  error_codes:
    - 7103
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1users/get"
    config_schema: null
    response_schema: GetWorkspaceUsersResponse
  sdk_examples: "/sdk-examples/users-and-groups/workspace-users/get-workspace-users.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/users`** - Get Workspace Users (Workspace Users / Users & Groups).

Returns the list of all users who have access to the specified workspace, along with their workspace-level role and active status.

The response includes the Account Admin, Organisation Admins, Workspace Admins, standard Users, and any users assigned to custom roles. When the org's Account Admin is a Client Portal Admin, each user entry also includes a `domainName` field indicating which portal domain the user was added through.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getWorkspaceUsers` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/users` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.usermanagement.read`](../../../foundations/oauth-scopes.md#zohoanalyticsusermanagementread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1users/get`; response schema `GetWorkspaceUsersResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.usermanagement.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- The calling user must be a Workspace Admin of the workspace. Account Admins and Organization Admins also have access, and an Organization Admin can view any workspace in their organization.
- Deactivated users continue to be listed in the response with **status** set to **false**. They are not removed from the workspace on deactivation.
- Users assigned to a custom role are listed with **role** set to the exact custom role name defined in the organization, and not to a numeric identifier.
- The **domainName** field is returned for every user only when the Account Admin of the organization is also a Client Portal Admin. Standard users then show the default Zoho Analytics domain, and portal users show their portal's custom domain.
- The email addresses returned by this API are the input for the Add Workspace Users, Remove Workspace Users, Change Workspace Users Status and Change Workspace Users Role APIs.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `data.users` | Array | All users with access to this workspace. |
| `users[].emailId` | String | Email address of the user. |
| `users[].status` | Boolean | `true` = active (can access the workspace). `false` = deactivated (access suspended). |
| `users[].role` | String | Workspace-level role. Values: `"Account Admin"`, `"Organization Admin"`, `"Workspace Admin"`, `"User"`, or a custom role name defined in the org. |
| `users[].domainName` | String | *(Present only when Account Admin is a Client Portal Admin.)* The portal domain the user was added through. |

# Examples

## Sample Requests

**Case 1 — Account Admin listing all workspace users**

```http
GET /restapi/v2/workspaces/466206000000071000/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Workspace Admin listing users for their workspace**

```http
GET /restapi/v2/workspaces/466206000000071000/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — Client Portal Admin listing workspace users (portal context)**

```http
GET /restapi/v2/workspaces/466206000000071000/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Standard org (no client portal) — users with mixed roles**
```json
{
  "status": "success",
  "summary": "Get workspace users",
  "data": {
    "users": [
      { "emailId": "admin@acme.com", "status": true, "role": "Account Admin" },
      { "emailId": "orgadmin@acme.com", "status": true, "role": "Organization Admin" },
      { "emailId": "wsadmin1@acme.com", "status": true, "role": "Workspace Admin" },
      { "emailId": "wsadmin2@acme.com", "status": true, "role": "Workspace Admin" },
      { "emailId": "user1@acme.com", "status": true, "role": "User" },
      { "emailId": "user2@acme.com", "status": false, "role": "User" }
    ]
  }
}
```

**Case 2 — Workspace with custom role users and deactivated users**
```json
{
  "status": "success",
  "summary": "Get workspace users",
  "data": {
    "users": [
      { "emailId": "admin@acme.com", "status": true, "role": "Account Admin" },
      { "emailId": "orgadmin@acme.com", "status": true, "role": "Organization Admin" },
      { "emailId": "wsadmin@acme.com", "status": true, "role": "Workspace Admin" },
      { "emailId": "analyst1@acme.com", "status": true, "role": "AnalystRole" },
      { "emailId": "analyst2@acme.com", "status": false, "role": "AnalystRole" },
      { "emailId": "user1@acme.com", "status": true, "role": "User" }
    ]
  }
}
```

**Case 3 — Client Portal Admin response (users include `domainName`)**

When the Account Admin is a Client Portal Admin, the response includes `domainName` for every user, allowing the admin to distinguish which portal domain each user was added through.

```json
{
  "status": "success",
  "summary": "Get workspace users",
  "data": {
    "users": [
      { "emailId": "admin@acme.com", "status": true, "role": "Account Admin", "domainName": "analytics.zoho.com" },
      { "emailId": "orgadmin@acme.com", "status": true, "role": "Organization Admin", "domainName": "analytics.zoho.com" },
      { "emailId": "wsadmin@acme.com", "status": true, "role": "Workspace Admin", "domainName": "analytics.zoho.com" },
      { "emailId": "portal.user1@client.com", "status": true, "role": "User", "domainName": "reports.clientbrand.com" },
      { "emailId": "portal.user2@client.com", "status": false, "role": "User", "domainName": "reports.clientbrand.com" }
    ]
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Workspace Users](../../../sdk-examples/users-and-groups/workspace-users/get-workspace-users.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`domainName` in response** | Only present in each user entry when the Account Admin is a Client Portal Admin. Standard org responses return users without `domainName`. |
| **Deactivated users are included** | Users with `status: false` (deactivated) still appear in the list. They are not removed from the workspace upon deactivation. |
| **Custom role users** | Users with a custom role appear in the list with `role` set to the exact custom role name as defined in the org. |
| **Dependency for other APIs** | User email addresses returned here are needed as input for Add Workspace Users, Remove Workspace Users, Change Workspace Users Status, Change Workspace Users Role, and as reference when managing groups. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not a Workspace Admin, Account Admin, or Organization Admin of the workspace. | Ensure the caller has at least Workspace Admin access to the workspace. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.usermanagement.read`. |

# Related

- [Workspace Users overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Add Workspace Users](add-workspace-users.md), [Remove Workspace Users](delete-workspace-users.md), [Change Workspace Users Status](change-workspace-users-status.md), [Change Workspace Users Role](change-workspace-users-role.md), [Get Workspace Admins](get-workspace-admins.md), [Add Workspace Admins](add-workspace-admins.md), [Remove Workspace Admins](remove-workspace-admins.md).
- [SDK examples](../../../sdk-examples/users-and-groups/workspace-users/get-workspace-users.md).
