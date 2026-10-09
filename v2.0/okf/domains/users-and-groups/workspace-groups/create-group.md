---
type: API Endpoint
title: Create Group
description: Creates a new group in the specified workspace and adds the initial members to it.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/groups"
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - workspace-groups
  - post
  - share
api:
  operation_id: createGroup
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/groups"
  domain: users-and-groups
  group: workspace-groups
  oauth_scopes:
    - ZohoAnalytics.share.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access.
  error_codes:
    - 7103
    - 7282
    - 7301
    - 8060
    - 8061
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1groups/post"
    config_schema: CreateGroupConfig
    response_schema: CreateGroupResponse
  sdk_examples: "/sdk-examples/users-and-groups/workspace-groups/create-group.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/groups`** - Create Group (Workspace Groups / Users & Groups).

Creates a new group in the specified workspace and optionally adds initial members to it. The group name must be unique within the workspace. An optional invitation email can be sent to the initial members at creation time.

> **Confirmed account requirement:** The calling user's Zoho account must be confirmed (email-verified) to invoke this API.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createGroup` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/groups` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.share.create`](../../../foundations/oauth-scopes.md#zohoanalyticssharecreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1groups/post`; CONFIG schema `CreateGroupConfig`; response schema `CreateGroupResponse` |

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

## CONFIG Parameter

CONFIG is **mandatory**. It must be sent as a form-encoded body parameter named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `groupName` | String | **Yes** | — | Display name for the new group. Must be unique within the workspace. Empty or blank values are rejected. |
| `emailIds` | Array of Strings | **Yes** | — | Email addresses of the initial group members. Min 1, max 1000 entries. Members must already be workspace users (or members of the specified portal domain). |
| `groupDesc` | String | No | `""` | A short description of the group's purpose. Max 200 characters. When omitted, defaults to an empty string. |
| `domainName` | String | No | `null` | Client portal domain for portal-scoped groups. When provided, the group is associated with the specified portal domain. All `emailIds` must belong to users within that portal domain. When omitted, the group is created in the standard Zoho Analytics domain context. |
| `inviteMail` | Boolean | No | `false` | When `false` (default): no email is sent to the initial members. When `true`: an invitation email is sent to all newly added group members informing them of their group access. |
| `mailSubject` | String | No | `""` | Custom subject line for the invitation email. Only relevant when `inviteMail` is `true`. Max 500 characters. |
| `mailMessage` | String | No | `""` | Custom message body for the invitation email. Supports basic HTML. Only relevant when `inviteMail` is `true`. Max 5000 characters. |

## Notes from the OpenAPI specification

- The Zoho account of the calling user must be confirmed (email verified) to invoke this API.
- The calling user must be a Workspace Admin of the workspace. Account Admins and Organization Admins also have access.
- The group name must be unique within the workspace. A duplicate name fails with error code **7282**. The same name can exist in different workspaces.
- A minimum of 1 and a maximum of 1000 email addresses can be sent. The users must already be members of the workspace, or of the specified client portal domain.
- No duplicate check is performed on **emailIds** at creation - the same address listed more than once results in a single membership.
- The **domainName** association is set at creation only and cannot be changed afterwards. To move a group to a different portal domain, delete it and create it again.
- When **domainName** is provided, every email address must belong to a user within that portal domain. Standard Zoho Analytics domain users cannot be added to a portal-domain group. When it is omitted, an org-wide group is created and any workspace user can be a member.
- When **inviteMail** is set to true without **mailSubject** or **mailMessage**, the invitation is sent with a system generated subject and message.
- A failure in delivering the invitation email does not roll back the operation. The group and its members are created even when the email cannot be delivered.
- Only the new **groupId** is returned. Use the Get Group Details API to retrieve the full group record.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `data.groupId` | String | Unique identifier of the newly created group. Use this as `<group-id>` in subsequent group API calls. |

# Examples

## Sample Requests

**Case 1 — Create a group with initial members and no invitation email**

```http
POST /restapi/v2/workspaces/466206000000071000/groups HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"groupName":"Finance Team","emailIds":["alice@acme.com","bob@acme.com"]}
```

**Case 2 — Create a group with a description and send an invitation email**

```http
POST /restapi/v2/workspaces/466206000000071000/groups HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"groupName":"Analytics Team","groupDesc":"Cross-functional analytics stakeholders","emailIds":["carol@acme.com","dave@acme.com"],"inviteMail":true,"mailSubject":"You've been added to the Analytics Team group","mailMessage":"Hi,<br>You now have access to the Analytics workspace group. Please log in to view your shared reports."}
```

**Case 3 — Client Portal: create a group scoped to a portal domain**

```http
POST /restapi/v2/workspaces/466206000000071000/groups HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"groupName":"Portal Analysts","emailIds":["portal.user1@client.com","portal.user2@client.com"],"domainName":"reports.clientbrand.com","inviteMail":true}
```

## Sample Responses

**HTTP 200 OK** — Group created successfully.

```json
{
  "status": "success",
  "summary": "Create group",
  "data": {
    "groupId": "320862000000295001"
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Group](../../../sdk-examples/users-and-groups/workspace-groups/create-group.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`domainName` is set at creation only** | Once a group is created with a `domainName`, that portal domain association cannot be changed. To change the domain, delete the group and recreate it. |
| **Omitting `domainName`** | Creates an org-wide group. All workspace users (regardless of portal domain) can be added as members. |
| **`emailIds` members at creation** | These users are added as initial group members. The same email appearing multiple times is handled as a single addition. |
| **`inviteMail=true` does not block creation** | If email delivery fails, the group and its members are still created. Email failures do not roll back the operation. |
| **Response** | Only the new `groupId` is returned. Use Get Group Details to retrieve the full group record. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7282](../../../foundations/error-codes.md#error-7282) | 400 | A group with the same name already exists in this workspace. Group names must be unique per workspace. | Choose a different name for the group. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not a Workspace Admin, Account Admin, or Organization Admin of the workspace. | Ensure the caller has at least Workspace Admin access. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | The specified `domainName` does not exist. | Provide a valid client portal domain name configured for the org. |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | The specified `domainName` does not belong to the org's Account Admin. | Use a domain administered by the Account Admin of this organisation. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.share.create`. |

# Related

- [Workspace Groups overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Group List](get-groups.md), [Rename Group](rename-group.md), [Add Group Members](add-group-members.md), [Remove Group Members](remove-group-members.md), [Delete Group](delete-group.md), [Get Group Details](get-group-details.md).
- [SDK examples](../../../sdk-examples/users-and-groups/workspace-groups/create-group.md).
