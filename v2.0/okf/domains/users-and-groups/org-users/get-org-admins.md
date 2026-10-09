---
type: API Endpoint
title: Get Org Admins
description: Returns the email addresses of the users who currently hold the Organization Admin role in the specified organization.
resource: https://analyticsapi.zoho.com/restapi/v2/orgadmins
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - org-users
  - get
  - share
api:
  operation_id: getOrgAdmins
  method: GET
  path: "/restapi/v2/orgadmins"
  domain: users-and-groups
  group: org-users
  oauth_scopes:
    - ZohoAnalytics.share.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: The authenticated user must be the Account Admin of the specified organisation.
  error_codes:
    - 7103
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1orgadmins/get"
    config_schema: null
    response_schema: GetOrgAdminsResponse
  sdk_examples: "/sdk-examples/users-and-groups/org-users/get-org-admins.md"
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

**GET `/restapi/v2/orgadmins`** - Get Org Admins (Organization Users / Users & Groups).

Returns the list of email addresses of users who currently hold the **Organization Admin** role in the specified organisation. This is a read-only API accessible only to the Account Admin of the organisation.

> **Access restriction:** Unlike the other user management APIs which are accessible to both Account Admin and Organization Admin, this API is **restricted to Account Admin only**. Organization Admins cannot call this API.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getOrgAdmins` |
| HTTP method | GET |
| URL | `/restapi/v2/orgadmins` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.share.read`](../../../foundations/oauth-scopes.md#zohoanalyticsshareread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID whose Org Admins to retrieve. |
| Permission required | The authenticated user must be the Account Admin of the specified organisation. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1orgadmins/get`; response schema `GetOrgAdminsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.share.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

This endpoint has no path parameters.

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- Unlike the other organization user management APIs, which can be invoked by both the Account Admin and the Organization Admins, this API is restricted to the Account Admin of the organization. An Organization Admin invoking this API fails with error code **7301**.
- When no Organization Admin has been assigned, the API returns HTTP 200 with an empty **orgAdmins** array.
- The users listed here are the users whose role was set to **ORGADMIN** using the Add Users or Change User Role API.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `data.orgAdmins` | Array of Strings | Email addresses of all users who currently hold the Organization Admin role in the org. Returns an empty array if no Org Admins are currently assigned. |

# Examples

## Sample Requests

**Case 1 — Account Admin listing all Org Admins**

```http
GET /restapi/v2/orgadmins HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Organisation with one Org Admin**
```json
{
  "status": "success",
  "summary": "Get org admins",
  "data": {
    "orgAdmins": [
      "orgadmin@example.com"
    ]
  }
}
```

**Case 2 — Organisation with multiple Org Admins**
```json
{
  "status": "success",
  "summary": "Get org admins",
  "data": {
    "orgAdmins": [
      "orgadmin1@example.com",
      "orgadmin2@example.com",
      "regional.admin@example.com"
    ]
  }
}
```

**Case 3 — Organisation with no Org Admins assigned**
```json
{
  "status": "success",
  "summary": "Get org admins",
  "data": {
    "orgAdmins": []
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Org Admins](../../../sdk-examples/users-and-groups/org-users/get-org-admins.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Organisation not found. | Verify the `ZANALYTICS-ORGID` header value. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The calling user is not the Account Admin of the organisation. | This API is strictly restricted to the Account Admin. Organization Admins and other roles cannot call this endpoint. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.share.read`. |

# Related

- [Organization Users overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Users](get-users.md), [Add Users](add-users.md), [Remove Users](remove-users.md), [Activate Users](activate-users.md), [Deactivate Users](de-activate-users.md), [Change User Role](change-user-role.md).
- [SDK examples](../../../sdk-examples/users-and-groups/org-users/get-org-admins.md).
