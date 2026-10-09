---
type: API Endpoint
title: Get Org List
description: Returns the list of Zoho Analytics organisations that the authenticated user belongs to.
resource: https://analyticsapi.zoho.com/restapi/v2/orgs
tags:
  - zoho-analytics
  - rest-api-v2
  - organization-management
  - org-info-and-settings
  - get
  - metadata
api:
  operation_id: getOrganizations
  method: GET
  path: "/restapi/v2/orgs"
  domain: organization-management
  group: org-info-and-settings
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: not-required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: Any authenticated Zoho Analytics user.
  error_codes:
    - 8535
  openapi:
    file: "/references/openapi/org-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1orgs/get"
    config_schema: null
    response_schema: GetOrganizationsResponse
  sdk_examples: "/sdk-examples/organization-management/org-info-and-settings/get-organizations.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/org-management-grouped-api.json"
    title: OpenAPI 3 specification - org-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

**GET `/restapi/v2/orgs`** - Get Org List (Organization Info & Settings / Organization Management).

Returns the list of Zoho Analytics organisations that the authenticated user belongs to. For each organisation, the response includes the user's role within that organisation, the number of workspaces, and plan details.

This is a **user-scoped** API — no `ZANALYTICS-ORGID` header is required. The result reflects the caller's membership across all organisations, not the contents of a single organisation.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getOrganizations` |
| HTTP method | GET |
| URL | `/restapi/v2/orgs` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | Not required (user-scoped API) - user-scoped, returns data across all organisations. |
| Permission required | Any authenticated Zoho Analytics user. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`org-management-grouped-api.json`](../../../references/openapi/org-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1orgs/get`; response schema `GetOrganizationsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | - | Not required | This API is user-scoped and works across all organizations of the caller. |

## Path Parameters

This endpoint has no path parameters.

## CONFIG Parameter

The CONFIG parameter is optional. When provided, it is passed as a query parameter named `CONFIG`.

> **Note:** The `getOrgsConfig` template exposes only one field. All other filtering is implicit — the API always returns only the organisations the authenticated user is a member of.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| *(none)* | — | — | — | This API takes no CONFIG fields. |

> If you do not need any filtering, omit CONFIG entirely — the API returns all accessible organisations.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `orgs` | Array | List of organisations the user belongs to. Empty array if the user has no Analytics org membership. |
| `orgs[].orgId` | String | Unique identifier of the organisation. Use this as the `ZANALYTICS-ORGID` header value in workspace-scoped APIs. |
| `orgs[].orgName` | String | Display name of the organisation. |
| `orgs[].orgDesc` | String | Description of the organisation. Empty string if not set. |
| `orgs[].createdBy` | String | Email address of the user who created (owns) this organisation. |
| `orgs[].createdByZuId` | String | Zoho User ID of the organisation creator. |
| `orgs[].planName` | String | Current subscription plan name for this organisation (e.g., `"Enterprise"`, `"Premium"`, `"Basic"`). |
| `orgs[].isDefault` | Boolean | `true` if this is the calling user's default organisation. Only one org per user can have `isDefault: true`. |
| `orgs[].numberOfWorkspaces` | Integer | Number of workspaces visible to the user. For admins: all workspaces in the org. For other roles: only workspaces shared with the user. |
| `orgs[].role` | String | The calling user's role in this organisation. Possible values: `"Account Admin"`, `"Organization Admin"`, `"User"`. |

## Notes from the OpenAPI specification

- Only active organisations are returned. Organisations that are expired or blocked are suppressed from the response.
- A user who holds no Zoho Analytics organisation membership receives HTTP 200 with an empty `orgs` array. No error is raised.
- Only one entry in the list can have `isDefault` set to true. When the user belongs to a single organisation, that organisation is always the default.
- `numberOfWorkspaces` is role dependent. For the Account Admin and Organization Admin roles it is the total number of workspaces in the organisation. For every other role it is the number of workspaces shared with the user.
- A user who is an Account Admin in one organisation and a regular user in another sees both organisations in the list, with `role` and `numberOfWorkspaces` differing per entry.

# Examples

## Sample Requests

**Case 1 — Get all organisations for the authenticated user**

```http
GET /restapi/v2/orgs HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

**Case 2 — Account Admin who owns one org and is a member of others**

```http
GET /restapi/v2/orgs HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Account Admin user in a single org**
```json
{
  "status": "success",
  "summary": "Get organizations",
  "data": {
    "orgs": [
      {
        "orgId": "64036181",
        "orgName": "acme-analytics",
        "orgDesc": "",
        "createdBy": "admin@acme.com",
        "createdByZuId": "64035928",
        "planName": "Enterprise",
        "isDefault": true,
        "numberOfWorkspaces": 41,
        "role": "Account Admin"
      }
    ]
  }
}
```

**Case 2 — Org Admin user who belongs to multiple organisations**
```json
{
  "status": "success",
  "summary": "Get organizations",
  "data": {
    "orgs": [
      {
        "orgId": "64036201",
        "orgName": "dev-team-analytics",
        "orgDesc": "",
        "createdBy": "orgadmin@dev.com",
        "createdByZuId": "64036024",
        "planName": "Premium",
        "isDefault": false,
        "numberOfWorkspaces": 1,
        "role": "Account Admin"
      },
      {
        "orgId": "64036181",
        "orgName": "acme-analytics",
        "orgDesc": "",
        "createdBy": "admin@acme.com",
        "createdByZuId": "64035928",
        "planName": "Enterprise",
        "isDefault": false,
        "numberOfWorkspaces": 41,
        "role": "Organization Admin"
      }
    ]
  }
}
```

**Case 3 — Shared User in another user's org (shows workspaces shared with them)**
```json
{
  "status": "success",
  "summary": "Get organizations",
  "data": {
    "orgs": [
      {
        "orgId": "64036287",
        "orgName": "shared-user-own-org",
        "orgDesc": "",
        "createdBy": "shareduser@test.com",
        "createdByZuId": "64036387",
        "planName": "Premium",
        "isDefault": false,
        "numberOfWorkspaces": 3,
        "role": "Account Admin"
      },
      {
        "orgId": "64036181",
        "orgName": "acme-analytics",
        "orgDesc": "",
        "createdBy": "admin@acme.com",
        "createdByZuId": "64035928",
        "planName": "Enterprise",
        "isDefault": false,
        "numberOfWorkspaces": 18,
        "role": "User"
      }
    ]
  }
}
```

> **`numberOfWorkspaces` interpretation:** For Account Admin and Organization Admin roles, this is the total count of all workspaces in the org. For all other roles (`User`, `Workspace Admin`, etc.), this is the count of workspaces that have been **shared** with the user within that org — not the total workspace count.

**Case 4 — User with no Zoho Analytics organisation memberships**
```json
{
  "status": "success",
  "summary": "Get organizations",
  "data": {
    "orgs": []
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Org List](../../../sdk-examples/organization-management/org-info-and-settings/get-organizations.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Organization Info & Settings overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Organization Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Resource Details](get-resource-details.md), [Get Subscription Details](get-subscription-details.md), [Get Meta Details From Name](get-meta-details.md).
- [SDK examples](../../../sdk-examples/organization-management/org-info-and-settings/get-organizations.md).
