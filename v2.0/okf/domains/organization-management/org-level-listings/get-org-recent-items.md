---
type: API Endpoint
title: Get Org Recent Items
description: "Returns the views the calling user opened most recently in one organisation, of any view type, newest first."
resource: https://analyticsapi.zoho.com/restapi/v2/orgs/recentitems
tags:
  - zoho-analytics
  - rest-api-v2
  - organization-management
  - org-level-listings
  - get
  - metadata
api:
  operation_id: getOrgRecentItems
  method: GET
  path: "/restapi/v2/orgs/recentitems"
  domain: organization-management
  group: org-level-listings
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an active user of the organisation. Only the caller's own history is returned."
  error_codes:
    - 7301
    - 8083
    - 8084
    - 8535
  openapi:
    file: "/references/openapi/org-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1orgs~1recentitems/get"
    config_schema: null
    response_schema: GetOrgRecentItemsResponse
  sdk_examples: "/sdk-examples/organization-management/org-level-listings/get-org-recent-items.md"
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

**GET `/restapi/v2/orgs/recentitems`** - Get Org Recent Items (Org-Level Listings / Organization Management).

Returns the views the caller opened most recently in one organisation, of any view type, newest first. At most 20 items.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

From the OpenAPI specification:

Returns the views the calling user opened most recently in one organisation, of any view type, newest first. At most 20 items are returned.

The API reads the own history of the caller and keeps the entries whose workspace is visible to them. It applies no view-level check, so an entry can refer to a view the caller can no longer open; treat the `viewId` as a hint and handle a refusal when you open it.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getOrgRecentItems` |
| HTTP method | GET |
| URL | `/restapi/v2/orgs/recentitems` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the organisation whose recent items are listed. |
| Permission required | The authenticated user must be an active user of the organisation. Only the caller's own history is returned. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`org-management-grouped-api.json`](../../../references/openapi/org-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1orgs~1recentitems/get`; response schema `GetOrgRecentItemsResponse` |

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

- Each user has an independent list. The request cannot read the recent items of another user.
- Entries are kept when their workspace is visible to the caller, exactly as the Get Org Workspaces API works it out. This API does not re-check view-level access, so an entry can refer to a view the caller can no longer open.
- At most 20 entries are returned, newest first. There is no paging, no limit attribute and no type filter.
- When the caller has no visible workspace in the organisation the list is empty; the existence of the organisation is still checked and an unknown ID fails with error 8084.
- The call costs 1 API unit, ten times the cost of the other org-level listings.
- The call is allowed on a Client Portal or White Label domain, where the entries are limited to the workspaces enabled for that domain.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get recent views"` for this API — the same text as the workspace-level recent-views API; the endpoint is told apart by its URL, not by `summary`. |
| `data` | JSONObject | Response payload wrapper. |
| `data.views` | JSONArray | The caller's recent items, newest first. **Always present**; `[]` when none. |
| `data.views[].viewId` | String | View ID. |
| `data.views[].viewName` | String | View name as recorded in the recent-items entry. |
| `data.views[].viewType` | String | The view's type. See [`viewType` Values](overview.md#viewtype-values). |
| `data.views[].workspaceId` | String | ID of the workspace that holds the view. |
| `data.views[].workspaceName` | String | Workspace name as recorded in the recent-items entry. |
| `data.views[].viewLastAccessedTime` | String | When the caller last opened the view, as epoch milliseconds returned as a string. |

## Notes from the OpenAPI specification

- Tables, reports, dashboards and the other view types appear together in one list.
- **viewName** and **workspaceName** are stored in the recent-items record and are not looked up live.
- **summary** reads Get recent views, the same text as the workspace-level recent-views listing. The endpoint is told apart by its URL rather than by **summary**.
- Some builds return additional fields. Ignore unrecognised keys rather than validating against a closed schema.

# Examples

## Sample Requests

**Case 1 — The caller's recent items in one organisation**

```http
GET /restapi/v2/orgs/recentitems HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal: request sent through the portal domain (list limited to the portal's workspaces)**

```http
GET /restapi/v2/orgs/recentitems HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — Three recent items**

```json
{
    "status": "success",
    "summary": "Get recent views",
    "data": {
        "views": [
            {
                "viewId": "466206000000106002",
                "viewName": "Support Overview",
                "viewType": "Dashboard",
                "workspaceId": "466206000000071000",
                "workspaceName": "Support Metrics",
                "viewLastAccessedTime": "1720100000000"
            },
            {
                "viewId": "137687000006991601",
                "viewName": "Revenue by Region",
                "viewType": "AnalysisView",
                "workspaceId": "137687000271334001",
                "workspaceName": "Sales Analysis",
                "viewLastAccessedTime": "1720090000000"
            },
            {
                "viewId": "466206000000105001",
                "viewName": "Tickets",
                "viewType": "Table",
                "workspaceId": "466206000000071000",
                "workspaceName": "Support Metrics",
                "viewLastAccessedTime": "1720000000000"
            }
        ]
    }
}
```

**HTTP 200 OK — No recent items in the caller's visible workspaces**

```json
{
    "status": "success",
    "summary": "Get recent views",
    "data": {
        "views": []
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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Org Recent Items](../../../sdk-examples/organization-management/org-level-listings/get-org-recent-items.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Read-only and idempotent** | Changes nothing. Costs 1 API unit, ten times the other two APIs. |
| **The caller's own history** | Each user has an independent list. The request cannot read another user's recent items. |
| **Workspace-filtered only** | Entries are kept when their workspace is visible to the caller ([Get Org Workspaces](get-org-workspaces.md)). This API does not re-check view-level access, so an entry can refer to a view the caller can no longer open. Treat the `viewId` as a hint and handle a refusal when you open it. |
| **Fixed size** | At most 20 entries. There is no paging, `limit` or type filter. |
| **All view types** | Tables, reports, dashboards and the other types listed in [`viewType` Values](overview.md#viewtype-values) appear together. |
| **Names come from the history entry** | `viewName` and `workspaceName` are stored in the recent-items record; they are not looked up live. |
| **Nothing visible → empty list** | When the caller has no visible workspace in the organisation, the list is `[]`; the organisation's existence is still checked (`8084`). |
| **Client Portal / White Label** | Allowed. Entries are limited to workspaces enabled for the requesting domain. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | Organization ID (Zoho Analytics UI → **Settings → Organisation**) → `ZANALYTICS-ORGID` → Get Org Recent Items. |

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
- Other endpoints in this group: [Get Org Workspaces](get-org-workspaces.md), [Get Org Dashboards](get-org-dashboards.md).
- [SDK examples](../../../sdk-examples/organization-management/org-level-listings/get-org-recent-items.md).
