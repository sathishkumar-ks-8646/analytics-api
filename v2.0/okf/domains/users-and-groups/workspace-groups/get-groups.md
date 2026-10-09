---
type: API Endpoint
title: Get Group List
description: "Returns all the groups defined in the specified workspace, along with their descriptions and current member lists."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/groups"
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - workspace-groups
  - get
  - share
api:
  operation_id: getGroups
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/groups"
  domain: users-and-groups
  group: workspace-groups
  oauth_scopes:
    - ZohoAnalytics.share.read
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
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1groups/get"
    config_schema: null
    response_schema: GetGroupsResponse
  sdk_examples: "/sdk-examples/users-and-groups/workspace-groups/get-groups.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/groups`** - Get Group List (Workspace Groups / Users & Groups).

Returns all groups defined in the specified workspace, along with their descriptions and current member lists.

When the Account Admin is a Client Portal Admin, each group entry includes a `domainName` field indicating which portal domain the group was created for. Custom domain users (users visiting via a portal URL) see only the groups that belong to their portal domain.

> This API has no CONFIG parameter.

From the OpenAPI specification:

Returns all the groups defined in the specified workspace, along with their descriptions and current member lists.

Groups are named collections of users within a workspace. A view shared with a group is accessible to every current and future member of that group, which makes groups the way to manage view-level sharing permissions in bulk.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getGroups` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/groups` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.share.read`](../../../foundations/oauth-scopes.md#zohoanalyticsshareread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1groups/get`; response schema `GetGroupsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.share.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- The calling user must be a Workspace Admin of the workspace. Account Admins and Organization Admins also have access.
- Groups are scoped to a single workspace. A group created in one workspace is not accessible in another workspace.
- The **domainName** field is returned in each group entry only when the Account Admin of the organization is also a Client Portal Admin. Standard organization responses do not include it.
- A user accessing Zoho Analytics through a client portal URL sees only the groups that belong to their portal domain. The full list across all domain contexts is visible only to Workspace Admins and Client Portal Admins.
- The **groupId** values returned here are required as the group-id path parameter in the Rename Group, Add Group Members, Remove Group Members, Delete Group and Get Group Details APIs.
- A WL Workspace Admin in a disabled-workspace portal context cannot invoke any of the group APIs and receives error code **7301**.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `data.groups` | Array | All groups defined in this workspace. An empty array when no groups exist. |
| `groups[].groupId` | String | Unique identifier for the group. Use this value as `<group-id>` in all group-specific API calls. |
| `groups[].groupName` | String | Display name of the group. Unique within the workspace. |
| `groups[].groupDesc` | String | Optional description. Empty string `""` when not set. |
| `groups[].groupMembers` | Array of Strings | Email addresses of all current group members. Empty array when the group has no members. |
| `groups[].domainName` | String | *(Present only when Account Admin is a Client Portal Admin.)* The portal domain this group was created for. |

# Examples

## Sample Requests

**Case 1 — Account Admin listing all groups in a workspace**

```http
GET /restapi/v2/workspaces/466206000000071000/groups HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Workspace Admin listing groups in their workspace**

```http
GET /restapi/v2/workspaces/466206000000071000/groups HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — Client Portal Admin listing groups (includes portal domain context)**

```http
GET /restapi/v2/workspaces/466206000000071000/groups HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Standard org (no Client Portal) — multiple groups with different membership**
```json
{
  "status": "success",
  "summary": "Get groups",
  "data": {
    "groups": [
      {
        "groupId": "320862000000276835",
        "groupName": "Finance Team",
        "groupDesc": "Finance department workspace users",
        "groupMembers": ["alice@acme.com"]
      },
      {
        "groupId": "320862000000286056",
        "groupName": "Analytics Team",
        "groupDesc": "",
        "groupMembers": ["bob@acme.com", "carol@acme.com", "dave@acme.com"]
      }
    ]
  }
}
```

**Case 2 — Workspace with one empty group (no members yet)**
```json
{
  "status": "success",
  "summary": "Get groups",
  "data": {
    "groups": [
      {
        "groupId": "320862000000310001",
        "groupName": "Onboarding",
        "groupDesc": "New joiners pending workspace access",
        "groupMembers": []
      }
    ]
  }
}
```

**Case 3 — Client Portal Admin response (each group includes `domainName`)**

When the Account Admin is a Client Portal Admin, every group entry includes `domainName` so the admin can distinguish standard org groups from portal-domain groups.

```json
{
  "status": "success",
  "summary": "Get groups",
  "data": {
    "groups": [
      {
        "groupId": "38190000004182920",
        "groupName": "Portal Analysts",
        "groupDesc": "",
        "domainName": "reports.clientbrand.com",
        "groupMembers": ["portal.user1@client.com", "portal.user2@client.com"]
      },
      {
        "groupId": "38190000004189049",
        "groupName": "Internal Team",
        "groupDesc": "",
        "domainName": "analytics.zoho.com",
        "groupMembers": ["analyst@acme.com"]
      }
    ]
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Group List](../../../sdk-examples/users-and-groups/workspace-groups/get-groups.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Filtered by portal domain for custom domain users** | Users accessing via a portal URL only see groups that belong to their portal domain. The full group list (across all domains) is only visible to Workspace Admins and Client Portal Admins. |
| **`domainName` in response** | Only included in each group object when the Account Admin is a Client Portal Admin. Standard org responses do not include `domainName`. |
| **Dependency for other APIs** | The `groupId` values returned here are required in the URL (`<group-id>`) for Rename Group, Add Group Members, Remove Group Members, Delete Group, and Get Group Details. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not a Workspace Admin, Account Admin, or Organization Admin of the workspace. | Ensure the caller has at least Workspace Admin access. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.share.read`. |

# Related

- [Workspace Groups overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Group](create-group.md), [Rename Group](rename-group.md), [Add Group Members](add-group-members.md), [Remove Group Members](remove-group-members.md), [Delete Group](delete-group.md), [Get Group Details](get-group-details.md).
- [SDK examples](../../../sdk-examples/users-and-groups/workspace-groups/get-groups.md).
