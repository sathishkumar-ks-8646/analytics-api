---
type: API Endpoint
title: Get Org Workspaces
description: Returns the workspaces of one organisation that the calling user can reach.
resource: https://analyticsapi.zoho.com/restapi/v2/orgs/workspaces
tags:
  - zoho-analytics
  - rest-api-v2
  - organization-management
  - org-level-listings
  - get
  - metadata
api:
  operation_id: getOrgWorkspaces
  method: GET
  path: "/restapi/v2/orgs/workspaces"
  domain: organization-management
  group: org-level-listings
  api_units:
    api_id: 3043
    action: GET_WORKSPACES
    category: METADATA
    units: 0.1
    units_basis: per_request
    units_note: "0.1 units per request"
    category_frequency_limit: 60 requests/minute
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an active user of the organisation. Account Admins and Organization Admins see every active workspace; other users see only the workspaces shared with them."
  error_codes:
    - 7301
    - 8083
    - 8084
    - 8535
  openapi:
    file: "/references/openapi/org-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1orgs~1workspaces/get"
    config_schema: null
    response_schema: GetOrgWorkspacesResponse
  sdk_examples: "/sdk-examples/organization-management/org-level-listings/get-org-workspaces.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/org-management-grouped-api.json"
    title: OpenAPI 3 specification - org-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T10:58:51Z
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

**GET `/restapi/v2/orgs/workspaces`** - Get Org Workspaces (Org-Level Listings / Organization Management).

Returns the workspaces of one organisation that the caller can reach. Supplies the `workspaceId` values used by [Get Org Dashboards](get-org-dashboards.md) and by every workspace-scoped API.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

From the OpenAPI specification:

Returns the workspaces of one organisation that the calling user can reach. The organisation is chosen with the `ZANALYTICS-ORGID` header and everything else is worked out from the identity of the caller.

An Account Admin or an Organization Admin receives every active workspace of the organisation; every other user receives only the workspaces shared with them. The result is therefore per caller: the same URL and header return different lists for different tokens. The `workspaceId` values returned here are the input of the Get Org Dashboards API and of every workspace-scoped API.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getOrgWorkspaces` |
| HTTP method | GET |
| URL | `/restapi/v2/orgs/workspaces` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the organisation whose workspaces are listed. |
| Permission required | The authenticated user must be an active user of the organisation. Account Admins and Organization Admins see every active workspace; other users see only the workspaces shared with them. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| API units | 0.1 units per request - action `GET_WORKSPACES` (api-id `3043`), **METADATA** category. See [API units](../../../foundations/api-units.md). |
| Frequency limit | 60 requests/minute across all **METADATA**-category calls of the organization. See [API units](../../../foundations/api-units.md#unit-categories-and-frequency-limits). |
| OpenAPI | [`org-management-grouped-api.json`](../../../references/openapi/org-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1orgs~1workspaces/get`; response schema `GetOrgWorkspacesResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID, shown in the Zoho Analytics UI under Settings > Organisation. See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

This endpoint has no path parameters.

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- An Account Admin and an Organization Admin receive every active workspace of the organisation. Every other user receives only the workspaces shared with them, directly or by an email address matching their account.
- An Organization Admin, or any other user, whose primary email address is not verified receives an empty list. This does not apply to the Account Admin.
- Workspaces created by certain internal services are not listed for any caller, whatever the role.
- An empty list is a valid answer. It means that nothing is visible to this caller, not that the organisation is empty. Do not use the list as an inventory unless the caller is an Account Admin or an Organization Admin.
- The call is allowed on a Client Portal or White Label domain, where the list holds only the workspaces enabled for the requesting domain.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get org workspaces"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.workspaces` | JSONArray | The workspaces visible to the caller. **Always present**; `[]` when none. |
| `data.workspaces[].workspaceId` | String | Workspace ID. Returned as a string. |
| `data.workspaces[].workspaceName` | String | Workspace name. |
| `data.workspaces[].workspaceDesc` | String | Workspace description; `""` when none. |
| `data.workspaces[].orgId` | String | ID of the organisation that owns the workspace. |
| `data.workspaces[].createdTime` | String | Creation time as **epoch milliseconds, returned as a string**, for example `"1718361737000"`. |
| `data.workspaces[].createdBy` | String | Email address of the workspace owner. The key is omitted when no address can be resolved. |
| `data.workspaces[].isDefault` | Boolean | `true` when this is the **calling user's** default workspace. It is a per-user setting, not a property of the workspace. At most one entry is `true`, and none is when the caller has no default workspace or the default is in another organisation. |

## Notes from the OpenAPI specification

- The list is ordered with the newest workspace first, by creation time. There is no sort parameter and no paging - the whole list is returned in one response.
- **isDefault** belongs to the caller, not to the workspace. At most one entry is true, and none is when the caller has no default workspace or the default is in another organisation. Do not store it as a workspace attribute.
- **workspaceId**, **orgId** and **createdTime** are JSON strings. Keep them as strings and do not parse the IDs as 32-bit integers.
- Some builds return additional fields. Ignore unrecognised keys rather than validating against a closed schema.

# Examples

## Sample Requests

**Case 1 — List the workspaces visible to the caller**

```http
GET /restapi/v2/orgs/workspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal: request sent through the portal domain (list limited to the portal's workspaces)**

```http
GET /restapi/v2/orgs/workspaces HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — Two workspaces, one of them the caller's default**

```json
{
    "status": "success",
    "summary": "Get org workspaces",
    "data": {
        "workspaces": [
            {
                "workspaceId": "137687000271334001",
                "workspaceName": "Sales Analysis",
                "workspaceDesc": "Quarterly sales dashboards",
                "orgId": "700000123456",
                "createdTime": "1718361737000",
                "createdBy": "jane.doe@example.com",
                "isDefault": true
            },
            {
                "workspaceId": "466206000000071000",
                "workspaceName": "Support Metrics",
                "workspaceDesc": "",
                "orgId": "700000123456",
                "createdTime": "1707286805000",
                "createdBy": "jane.doe@example.com",
                "isDefault": false
            }
        ]
    }
}
```

**HTTP 200 OK — Nothing visible to the caller**

```json
{
    "status": "success",
    "summary": "Get org workspaces",
    "data": {
        "workspaces": []
    }
}
```

**HTTP 404 Not Found — No organisation exists with the ID in the header**

```json
{
    "status": "failure",
    "summary": "ORGID_NOT_EXIST",
    "data": {
        "errorCode": 8084,
        "errorMessage": "Organization id 700000999999 is not exist."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Org Workspaces](../../../sdk-examples/organization-management/org-level-listings/get-org-workspaces.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Read-only and idempotent** | Changes nothing. Repeating the call returns the current list. |
| **Per-caller result** | Account Admins and Organization Admins receive every active workspace. Everyone else receives only workspaces shared with them. Workspaces created by certain internal services are never listed. The same URL and header therefore return different lists for different tokens. |
| **Empty list is not an error** | A user with nothing shared, or an Organization Admin or other user whose primary email address is not verified, receives `"workspaces": []`. |
| **Order** | Newest workspace first, by creation time. There is no sort parameter. |
| **No paging** | The whole list is returned in one response. |
| **`isDefault` belongs to the caller** | Two users see different `isDefault` flags for the same workspace. Do not store it as a workspace attribute. |
| **Ids are strings** | `workspaceId`, `orgId` and `createdTime` are JSON strings. Keep them as strings; do not parse IDs as 32-bit integers. |
| **Client Portal / White Label** | Allowed. The list holds only the workspaces enabled for the requesting domain. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | Organization ID (Zoho Analytics UI → **Settings → Organisation**) → `ZANALYTICS-ORGID` → Get Org Workspaces → `workspaceId` for [Get Org Dashboards](get-org-dashboards.md) and for every workspace-scoped API. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an active user of the organisation named in the header. | Use the organisation the user belongs to, or ask an Account Admin to add the user to the organisation. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| [8084](../../../foundations/error-codes.md#error-8084) | 404 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Read the Organization ID from **Settings → Organisation** in the Zoho Analytics UI. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Org-Level Listings overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Organization Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Org Dashboards](get-org-dashboards.md), [Get Org Recent Items](get-org-recent-items.md).
- [SDK examples](../../../sdk-examples/organization-management/org-level-listings/get-org-workspaces.md).
- [API units](../../../foundations/api-units.md) - unit cost, unit categories and frequency limits for every endpoint.
