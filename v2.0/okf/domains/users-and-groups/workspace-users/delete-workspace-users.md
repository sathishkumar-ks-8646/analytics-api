---
type: API Endpoint
title: Remove Workspace Users
description: Removes one or more users from the specified workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/users"
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - workspace-users
  - delete
  - usermanagement
api:
  operation_id: deleteWorkspaceUsers
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/users"
  domain: users-and-groups
  group: workspace-users
  oauth_scopes:
    - ZohoAnalytics.usermanagement.delete
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
    - 8060
    - 8061
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1users/delete"
    config_schema: DeleteWorkspaceUsersConfig
    response_schema: null
  sdk_examples: "/sdk-examples/users-and-groups/workspace-users/delete-workspace-users.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/user-groups-grouped-api.json"
    title: OpenAPI 3 specification - user-groups-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**DELETE `/restapi/v2/workspaces/{workspace-id}/users`** - Remove Workspace Users (Workspace Users / Users & Groups).

Removes one or more users from the specified workspace. Removed users lose all access to this workspace immediately. Their membership in the organisation and access to other workspaces is unaffected.

> **Confirmed account requirement:** The calling user's Zoho account must be confirmed (email-verified) to invoke this API.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deleteWorkspaceUsers` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/users` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.usermanagement.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsusermanagementdelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1users/delete`; CONFIG schema `DeleteWorkspaceUsersConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.usermanagement.delete`. See [Authentication](../../../foundations/authentication.md). |
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
| `emailIds` | Array of Strings | **Yes** | — | List of email addresses to remove from the workspace. Max 1000 entries. |
| `domainName` | String | No | `null` | Client portal domain for portal-scoped removal. When provided, removes users who were added via that specific portal domain. When omitted, removes users from the standard Zoho Analytics domain context. |

## Notes from the OpenAPI specification

- The Zoho account of the calling user must be confirmed (email verified) to invoke this API.
- The calling user must be a Workspace Admin of the workspace. Account Admins and Organization Admins also have access.
- A maximum of 1000 email addresses can be sent in a single request.
- This API removes the entire workspace access of the user, including the shared views, the group memberships within the workspace, and the Workspace Admin role if they hold it. All the view-level and workspace-level permissions of the user are deleted immediately.
- To revoke only the Workspace Admin role and leave the user in the workspace as a regular user, use the Remove Workspace Admins API instead.
- Always specify **domainName** when removing portal users. Without it, the lookup is performed in the standard Zoho Analytics domain and a portal-only user will not be found.
- Verify the membership using the Get Workspace Users API before invoking this API. The behaviour for a user who is not in the workspace depends on the domain context.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Remove a single user from the workspace**

```http
DELETE /restapi/v2/workspaces/466206000000071000/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["contractor@acme.com"]}
```

**Case 2 — Remove multiple users at once**

```http
DELETE /restapi/v2/workspaces/466206000000071000/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["user1@acme.com","user2@acme.com","user3@acme.com"]}
```

**Case 3 — Client Portal: remove a portal user from a specific domain**

```http
DELETE /restapi/v2/workspaces/466206000000071000/users HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["former.client@client.com"],"domainName":"reports.clientbrand.com"}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Remove Workspace Users](../../../sdk-examples/users-and-groups/workspace-users/delete-workspace-users.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Remove Workspace Users returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Removes user completely from the workspace** | Unlike [Remove Workspace Admins](remove-workspace-admins.md), which only demotes, this API removes the user's entire workspace access — including any shared views, group memberships within the workspace, and admin role if applicable. |
| **All sharing permissions revoked** | All view-level and workspace-level access for the removed user is deleted immediately. |
| **Portal users require `domainName`** | If the user was added via a portal domain, specify the same `domainName` to target the correct user record. Without `domainName`, the lookup is done in the standard domain and the portal user will not be found. |
| **Dependency** | User email addresses → Get Workspace Users. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not a Workspace Admin, Account Admin, or Organization Admin of the workspace. | Ensure the caller has at least Workspace Admin access. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | The specified `domainName` does not exist. | Provide a valid client portal domain name. |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | The specified `domainName` does not belong to the org's Account Admin. | Use a domain administered by the Account Admin of this organisation. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.usermanagement.delete`. |

# Related

- [Workspace Users overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Workspace Users](get-workspace-users.md), [Add Workspace Users](add-workspace-users.md), [Change Workspace Users Status](change-workspace-users-status.md), [Change Workspace Users Role](change-workspace-users-role.md), [Get Workspace Admins](get-workspace-admins.md), [Add Workspace Admins](add-workspace-admins.md), [Remove Workspace Admins](remove-workspace-admins.md).
- [SDK examples](../../../sdk-examples/users-and-groups/workspace-users/delete-workspace-users.md).
