---
type: API Endpoint
title: Add Group Members
description: Adds one or more users to an existing group.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members"
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - workspace-groups
  - post
  - share
api:
  operation_id: addGroupMembers
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members"
  domain: users-and-groups
  group: workspace-groups
  oauth_scopes:
    - ZohoAnalytics.share.create
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
    - 7338
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1groups~1{group-id}~1members/post"
    config_schema: GroupMembersConfig
    response_schema: null
  sdk_examples: "/sdk-examples/users-and-groups/workspace-groups/add-group-members.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/user-groups-grouped-api.json"
    title: OpenAPI 3 specification - user-groups-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members`** - Add Group Members (Workspace Groups / Users & Groups).

Adds one or more users to an existing group. Users must already have access to the workspace (or the portal domain the group belongs to) before they can be added as group members. An optional invitation email can be sent to the newly added members.

> **Note:** There is no explicit `domainName` field for this API. The group itself carries its domain association (set at creation). The domain context is automatically resolved from the group's identity. Members to be added must be users within the domain that the group belongs to.

> **Confirmed account requirement:** The calling user's Zoho account must be confirmed (email-verified) to invoke this API.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `addGroupMembers` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.share.create`](../../../foundations/oauth-scopes.md#zohoanalyticssharecreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1groups~1{group-id}~1members/post`; CONFIG schema `GroupMembersConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.share.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{group-id}` | string | ID of the group. | [How to obtain](../../../foundations/identifiers.md#group-id) |

## CONFIG Parameter

CONFIG is **mandatory**. It must be sent as a form-encoded body parameter named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `emailIds` | Array of Strings | **Yes** | — | Email addresses to add to the group. Min 1, max 1000 entries. All users must be existing workspace members within the group's domain context. |
| `inviteMail` | Boolean | No | `false` | When `false` (default): no email is sent. When `true`: an invitation email is sent to all newly added members informing them of their group access. If a user was already a group member, no email is sent for that user — only genuinely new additions receive the email. |
| `mailSubject` | String | No | `""` | Custom subject line for the invitation email. Only relevant when `inviteMail` is `true`. Max 500 characters. |
| `mailMessage` | String | No | `""` | Custom message body for the invitation email. Supports basic HTML. Only relevant when `inviteMail` is `true`. Max 5000 characters. |

## Notes from the OpenAPI specification

- The Zoho account of the calling user must be confirmed (email verified) to invoke this API.
- The calling user must be a Workspace Admin of the workspace. Account Admins and Organization Admins also have access.
- A minimum of 1 and a maximum of 1000 email addresses can be sent in a single request.
- The users must already have been added to the workspace using the Add Workspace Users API before they can be added to a group.
- This API has no **domainName** attribute. The client portal domain context is resolved automatically from the group, which carries the domain association set at creation. The members to be added must be users within that domain.
- Email addresses that are already members of the group are skipped silently and no error is raised. Only genuinely new members receive an invitation email when **inviteMail** is set to true.
- When **inviteMail** is set to true without **mailSubject** or **mailMessage**, the invitation is sent with a system generated subject and message.
- A failure in delivering the invitation email does not roll back the addition. The members are added even when the email cannot be delivered.
- Adding a member immediately grants them access to every view that is currently shared with the group.
- The group-id in the request URI must belong to the workspace in the request URI. A group from another workspace fails with error code **7338**.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Add members silently**

```http
POST /restapi/v2/workspaces/466206000000071000/groups/320862000000276835/members HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["eve@acme.com","frank@acme.com"]}
```

**Case 2 — Add a member and send an invitation email with custom message**

```http
POST /restapi/v2/workspaces/466206000000071000/groups/320862000000276835/members HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["grace@acme.com"],"inviteMail":true,"mailSubject":"You've been added to Finance Team","mailMessage":"Hi Grace,<br>You now have group access to Finance Team reports. Please log in to view them."}
```

**Case 3 — Client Portal: add a portal user to a portal-domain group**

For groups scoped to a portal domain, add members who belong to that same portal domain. The domain association is carried by the group itself — no `domainName` field is needed in the request.

```http
POST /restapi/v2/workspaces/466206000000071000/groups/38190000004182920/members HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["portal.user3@client.com"],"inviteMail":true}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Add Group Members](../../../sdk-examples/users-and-groups/workspace-groups/add-group-members.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Add Group Members returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Members must already be workspace users** | Users must have been added to the workspace (via Add Workspace Users) before they can be added to a group. |
| **Adding an existing member is silently skipped** | If a user is already in the group, they are not added again and no error is raised. Only genuinely new members receive an invitation email when `inviteMail=true`. |
| **No `domainName` in this request** | The portal domain context is inherited from the group itself (set at creation). Do not include `domainName` when adding members. |
| **`inviteMail=true` does not block the add** | Email delivery failures do not roll back the member addition. |
| **Dependency** | `<group-id>` → Get Group List. User email addresses → Get Workspace Users. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not a Workspace Admin, Account Admin, or Organization Admin of the workspace. | Ensure the caller has at least Workspace Admin access. |
| [7338](../../../foundations/error-codes.md#error-7338) | 400 | The specified `<group-id>` does not belong to this workspace. | Verify the group ID using Get Group List. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.share.create`. |

# Related

- [Workspace Groups overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Group List](get-groups.md), [Create Group](create-group.md), [Rename Group](rename-group.md), [Remove Group Members](remove-group-members.md), [Delete Group](delete-group.md), [Get Group Details](get-group-details.md).
- [SDK examples](../../../sdk-examples/users-and-groups/workspace-groups/add-group-members.md).
