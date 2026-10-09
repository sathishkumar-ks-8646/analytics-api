---
type: API Endpoint
title: Get Workspace Admins
description: Returns the list of users who currently hold the Workspace Admin role in the specified workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/admins"
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - workspace-users
  - get
  - share
api:
  operation_id: getWorkspaceAdmins
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/admins"
  domain: users-and-groups
  group: workspace-users
  oauth_scopes:
    - ZohoAnalytics.share.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace.
  error_codes:
    - 7103
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1admins/get"
    config_schema: null
    response_schema: GetWorkspaceAdminsResponse
  sdk_examples: "/sdk-examples/users-and-groups/workspace-users/get-workspace-admins.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/admins`** - Get Workspace Admins (Workspace Users / Users & Groups).

Returns the list of users who currently hold the **Workspace Admin** role in the specified workspace. When the org's Account Admin is a Client Portal Admin, the response groups admins by portal domain — showing standard org admins and portal-domain admins separately, each with a `domainName`.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getWorkspaceAdmins` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/admins` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.share.read`](../../../foundations/oauth-scopes.md#zohoanalyticsshareread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1admins/get`; response schema `GetWorkspaceAdminsResponse` |

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

- The calling user must be an Account Admin or an Organization Admin of the organization that owns the workspace. Workspace Admins and regular users cannot invoke this API.
- Only workspace-level admins are listed. Account Admins and Organization Admins are not returned here, even though they have effective admin access to the workspace.
- **workspaceAdmins** is always an array. In a standard organization it holds a single entry without **domainName**. When the Account Admin is also a Client Portal Admin, it holds one entry per domain context - one for the standard Zoho Analytics domain and one for each client portal domain - each carrying its **domainName**.
- The Get Workspace Users API returns all the users of the workspace including its admins, whereas this API returns only the admin subset. Use this API when only the admin list is needed, for example before invoking Remove Workspace Admins.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `workspaceAdmins` | Array | One or two admin group objects. |
| `workspaceAdmins[].adminMembers` | Array of Strings | Email addresses of users with Workspace Admin role in this domain context. |
| `workspaceAdmins[].domainName` | String | *(Present only for Client Portal Admin orgs.)* The portal domain this admin group belongs to. |

# Examples

## Sample Requests

**Case 1 — Account Admin listing workspace admins**

```http
GET /restapi/v2/workspaces/466206000000071000/admins HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Org Admin listing workspace admins**

```http
GET /restapi/v2/workspaces/466206000000071000/admins HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — Client Portal Admin listing workspace admins by domain**

```http
GET /restapi/v2/workspaces/466206000000071000/admins HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Standard org (no Client Portal) — single group**
```json
{
  "status": "success",
  "summary": "Get workspace admins",
  "data": {
    "workspaceAdmins": [
      {
        "adminMembers": ["wsadmin@acme.com"]
      }
    ]
  }
}
```

**Case 2 — Multiple Workspace Admins**
```json
{
  "status": "success",
  "summary": "Get workspace admins",
  "data": {
    "workspaceAdmins": [
      {
        "adminMembers": ["wsadmin1@acme.com", "wsadmin2@acme.com", "wsadmin3@acme.com"]
      }
    ]
  }
}
```

**Case 3 — Client Portal Admin response (admins grouped by domain)**

When the Account Admin is a Client Portal Admin, the response returns two groups: one for standard Zoho Analytics domain admins, and one for the client portal domain admins. Each group includes a `domainName` field.

```json
{
  "status": "success",
  "summary": "Get workspace admins",
  "data": {
    "workspaceAdmins": [
      {
        "adminMembers": ["wsadmin@acme.com"],
        "domainName": "analytics.zoho.com"
      },
      {
        "adminMembers": ["portal.admin@client.com"],
        "domainName": "reports.clientbrand.com"
      }
    ]
  }
}
```

> **`workspaceAdmins` is always an array.** In a standard org (non-portal), it has one entry without `domainName`. For Client Portal Admins, it has two entries — one per domain context — each with `domainName`.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Workspace Admins](../../../sdk-examples/users-and-groups/workspace-users/get-workspace-admins.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Returns workspace-level admins only** | This API lists users who have the Workspace Admin role. Account Admins and Org Admins are not listed here even though they have effective workspace-level admin access. |
| **`domainName` per admin group** | When the Account Admin is a Client Portal Admin, the response groups admins by domain (`workspaceAdmins` contains entries for the standard domain and each portal domain). |
| **Relationship to Get Workspace Users** | Get Workspace Users returns all users including admins; this API returns only the admins subset. Use this API when you only need the admin list (e.g., before calling Remove Workspace Admins). |
| **Dependency for other APIs** | Admin email addresses returned here are needed as input for Remove Workspace Admins. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not an Account Admin or Organization Admin of the organisation. | Workspace Admins and regular users cannot call this API. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.share.read`. |

# Related

- [Workspace Users overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Workspace Users](get-workspace-users.md), [Add Workspace Users](add-workspace-users.md), [Remove Workspace Users](delete-workspace-users.md), [Change Workspace Users Status](change-workspace-users-status.md), [Change Workspace Users Role](change-workspace-users-role.md), [Add Workspace Admins](add-workspace-admins.md), [Remove Workspace Admins](remove-workspace-admins.md).
- [SDK examples](../../../sdk-examples/users-and-groups/workspace-users/get-workspace-admins.md).
