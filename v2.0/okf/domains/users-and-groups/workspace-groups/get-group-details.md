---
type: API Endpoint
title: Get Group Details
description: "Returns the full details of a single group - its name, description and complete member list."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/groups/{group-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - workspace-groups
  - get
  - share
api:
  operation_id: getGroupDetails
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/groups/{group-id}"
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
    - 7338
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1groups~1{group-id}/get"
    config_schema: null
    response_schema: GetGroupDetailsResponse
  sdk_examples: "/sdk-examples/users-and-groups/workspace-groups/get-group-details.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}`** - Get Group Details (Workspace Groups / Users & Groups).

Returns the full details of a single group — its name, description, and complete member list.

For Client Portal Admins or users visiting via a custom portal domain URL, the response also includes `domainName` indicating which portal domain the group belongs to.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getGroupDetails` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.share.read`](../../../foundations/oauth-scopes.md#zohoanalyticsshareread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1groups~1{group-id}/get`; response schema `GetGroupDetailsResponse` |

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
| `{group-id}` | string | ID of the group. | [How to obtain](../../../foundations/identifiers.md#group-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- The calling user must be a Workspace Admin of the workspace. Account Admins and Organization Admins also have access.
- The **data.groups** value of this API is a single object, unlike the Get Group List API, where it is an array.
- The **domainName** field is returned when the Account Admin of the organization is also a Client Portal Admin, or when the request is made through a custom portal domain URL. This is broader than the Get Group List API, which returns it only for Client Portal Admins.
- Use the Get Group List API to discover the **groupId** values, and then this API for the details of a specific group.
- Read the current **groupDesc** from this API before invoking the Rename Group API, since that API resets the description when it is not supplied.
- The group-id in the request URI must belong to the workspace in the request URI. A group from another workspace fails with error code **7338**.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `data.groups` | Object | A single group object (not an array — unlike the list API). |
| `groups.groupId` | String | Unique identifier of the group. |
| `groups.groupName` | String | Current display name of the group. |
| `groups.groupDesc` | String | Current description. Empty string `""` when not set. |
| `groups.groupMembers` | Array of Strings | Email addresses of all current members. |
| `groups.domainName` | String | *(Present when Account Admin is a Client Portal Admin, or when accessed via a custom portal domain URL.)* The portal domain this group belongs to. |

# Examples

## Sample Requests

**Case 1 — Get details of a specific group**

```http
GET /restapi/v2/workspaces/466206000000071000/groups/320862000000286056 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Client Portal Admin fetching details of a portal-domain group**

```http
GET /restapi/v2/workspaces/466206000000071000/groups/38190000004182920 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Standard org group details**
```json
{
  "status": "success",
  "summary": "Get group details",
  "data": {
    "groups": {
      "groupId": "320862000000286056",
      "groupName": "Analytics Team",
      "groupDesc": "Cross-functional analytics stakeholders",
      "groupMembers": ["bob@acme.com", "carol@acme.com", "dave@acme.com"]
    }
  }
}
```

**Case 2 — Client Portal Admin response (includes `domainName`)**
```json
{
  "status": "success",
  "summary": "Get group details",
  "data": {
    "groups": {
      "groupId": "38190000004182920",
      "groupName": "Portal Analysts",
      "groupDesc": "",
      "domainName": "reports.clientbrand.com",
      "groupMembers": ["portal.user1@client.com", "portal.user2@client.com"]
    }
  }
}
```

**Case 3 — Invalid or cross-workspace group ID**
```json
{
  "status": "failure",
  "summary": "GRPID_NOT_BELONGS_TO_DB",
  "data": {
    "errorCode": 7338,
    "errorMessage": "Group(s) does not belongs to current workspace"
  }
}
```

> **`data.groups` is an object, not an array.** Unlike Get Group List (which returns `groups` as an array), Get Group Details returns `groups` as a single JSON object.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Group Details](../../../sdk-examples/users-and-groups/workspace-groups/get-group-details.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **More detailed than Get Group List** | Returns a single group object with its full member list, description, and (when applicable) portal domain name. Use Get Group List to discover `groupId` values, then call this API for details on a specific group. |
| **`domainName` visibility** | Included in the response when the Account Admin is a Client Portal Admin **or** when the request is made via a custom portal domain URL — broader than Get Group List (which only shows `domainName` for Client Portal Admins). |
| **Response structure difference from Get Group List** | Get Group List returns `data.groups` (array). Get Group Details returns a single group object directly under `data`. |
| **Dependency** | `<group-id>` → Get Group List. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not a Workspace Admin, Account Admin, or Organization Admin of the workspace. | Ensure the caller has at least Workspace Admin access. |
| [7338](../../../foundations/error-codes.md#error-7338) | 400 | The specified `<group-id>` does not belong to this workspace. | Retrieve the correct group ID from Get Group List. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.share.read`. |

# Related

- [Workspace Groups overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Group List](get-groups.md), [Create Group](create-group.md), [Rename Group](rename-group.md), [Add Group Members](add-group-members.md), [Remove Group Members](remove-group-members.md), [Delete Group](delete-group.md).
- [SDK examples](../../../sdk-examples/users-and-groups/workspace-groups/get-group-details.md).
