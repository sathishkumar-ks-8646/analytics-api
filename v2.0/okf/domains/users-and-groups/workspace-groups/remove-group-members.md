---
type: API Endpoint
title: Remove Group Members
description: Removes one or more members from a group.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members"
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - workspace-groups
  - delete
  - share
api:
  operation_id: removeGroupMembers
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members"
  domain: users-and-groups
  group: workspace-groups
  oauth_scopes:
    - ZohoAnalytics.share.delete
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
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1groups~1{group-id}~1members/delete"
    config_schema: GroupMembersRemovalConfig
    response_schema: null
  sdk_examples: "/sdk-examples/users-and-groups/workspace-groups/remove-group-members.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members`** - Remove Group Members (Workspace Groups / Users & Groups).

Removes one or more members from a group. Removed users lose any view-level access that was granted exclusively through group membership in this group. Their other access (workspace membership, direct sharing on views, membership in other groups) is unaffected.

> **Confirmed account requirement:** The calling user's Zoho account must be confirmed (email-verified) to invoke this API.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `removeGroupMembers` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.share.delete`](../../../foundations/oauth-scopes.md#zohoanalyticssharedelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1groups~1{group-id}~1members/delete`; CONFIG schema `GroupMembersRemovalConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.share.delete`. See [Authentication](../../../foundations/authentication.md). |
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
| `emailIds` | Array of Strings | **Yes** | — | Email addresses of the members to remove from the group. Min 1, max 1000 entries. |
| `notifyUser` | Boolean | No | `false` | When `false` (default): removal is silent — no email is sent to the removed members. When `true`: a notification email is sent to each removed member informing them that their group access has been revoked. |

## Notes from the OpenAPI specification

- The Zoho account of the calling user must be confirmed (email verified) to invoke this API.
- The calling user must be a Workspace Admin of the workspace. Account Admins and Organization Admins also have access.
- A minimum of 1 and a maximum of 1000 email addresses can be sent in a single request.
- An email address that is not a member of the group is ignored silently, and the remaining valid members are still processed.
- Removing every member of a group is allowed. The group continues to exist with no members and can be repopulated or deleted later.
- This API has no **domainName** attribute. The client portal domain context is inherited from the group.
- A failure in delivering the notification email does not roll back the removal. The members are removed even when the email cannot be delivered.
- If the only path a removed user had to a shared view was through this group, they lose that access immediately. Access held through a direct share or through another group that shares the same view is retained.
- The group-id in the request URI must belong to the workspace in the request URI. A group from another workspace fails with error code **7338**.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Remove a member silently**

```http
DELETE /restapi/v2/workspaces/466206000000071000/groups/320862000000276835/members HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["alice@acme.com"]}
```

**Case 2 — Remove multiple members and send a notification email**

```http
DELETE /restapi/v2/workspaces/466206000000071000/groups/320862000000276835/members HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["alice@acme.com","bob@acme.com"],"notifyUser":true}
```

**Case 3 — Client Portal: remove a portal user from a portal-domain group**

```http
DELETE /restapi/v2/workspaces/466206000000071000/groups/38190000004182920/members HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["portal.user2@client.com"]}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Remove Group Members](../../../sdk-examples/users-and-groups/workspace-groups/remove-group-members.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Remove Group Members returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Removing a non-member is silently ignored** | If an email address is not a member of the group, the operation proceeds without error for the remaining valid members. |
| **Impact on view sharing** | If the removed user's only access to a shared view was through this group, they lose that access immediately. Access via direct sharing or other groups is not affected. |
| **`notifyUser=true` does not block removal** | Email delivery failures do not roll back the member removal. |
| **No `domainName` in this request** | Portal domain context is inherited from the group. |
| **Dependency** | `<group-id>` → Get Group List. Member emails → Get Group Details. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not a Workspace Admin, Account Admin, or Organization Admin of the workspace. | Ensure the caller has at least Workspace Admin access. |
| [7338](../../../foundations/error-codes.md#error-7338) | 400 | The specified `<group-id>` does not belong to this workspace. | Verify the group ID using Get Group List. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.share.delete`. |

# Related

- [Workspace Groups overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Group List](get-groups.md), [Create Group](create-group.md), [Rename Group](rename-group.md), [Add Group Members](add-group-members.md), [Delete Group](delete-group.md), [Get Group Details](get-group-details.md).
- [SDK examples](../../../sdk-examples/users-and-groups/workspace-groups/remove-group-members.md).
