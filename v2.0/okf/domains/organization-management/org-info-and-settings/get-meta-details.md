---
type: API Endpoint
title: Get Meta Details From Name
description: "Resolves a workspace, and optionally a view within it, by name and returns the corresponding IDs."
resource: https://analyticsapi.zoho.com/restapi/v2/metadetails
tags:
  - zoho-analytics
  - rest-api-v2
  - organization-management
  - org-info-and-settings
  - get
  - metadata
api:
  operation_id: getMetaDetails
  method: GET
  path: "/restapi/v2/metadetails"
  domain: organization-management
  group: org-info-and-settings
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: query
    required: true
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must have at least Read access on the specified workspace (for workspace-only lookup), or Read access on the specific view (for view lookup). Workspace Admins, Account Admins, Organization Admins, and any user with at least one shared view in the workspace can call this API."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/org-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1metadetails/get"
    config_schema: GetMetaDetailsConfig
    response_schema: GetMetaDetailsResponse
  sdk_examples: "/sdk-examples/organization-management/org-info-and-settings/get-meta-details.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/org-management-grouped-api.json"
    title: OpenAPI 3 specification - org-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**GET `/restapi/v2/metadetails`** - Get Meta Details From Name (Organization Info & Settings / Organization Management).

Resolves a workspace (and optionally a view) **by name** to return its numeric IDs. This is useful when you know the human-readable names of a workspace and view but need their IDs to call other workspace-scoped or view-scoped APIs.

- When only `workspaceName` is provided: returns the workspace ID, description, and org ID.
- When both `workspaceName` and `viewName` are provided: additionally returns the view's ID, description, and type.

> **Name uniqueness:** Workspace names are unique within an organisation. View names are unique within a workspace. This API performs an exact, case-sensitive match on the provided names.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getMetaDetails` |
| HTTP method | GET |
| URL | `/restapi/v2/metadetails` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID in which the workspace exists. |
| Permission required | The authenticated user must have at least Read access on the specified workspace (for workspace-only lookup), or Read access on the specific view (for view lookup). Workspace Admins, Account Admins, Organization Admins, and any user with at least one shared view in the workspace can call this API. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - **mandatory** |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`org-management-grouped-api.json`](../../../references/openapi/org-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1metadetails/get`; CONFIG schema `GetMetaDetailsConfig`; response schema `GetMetaDetailsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

This endpoint has no path parameters.

## CONFIG Parameter

CONFIG is **mandatory** for this API. It must be sent as a query parameter named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `workspaceName` | String | **Yes** | — | The exact display name of the workspace to look up. Must match the workspace name as it appears in the Zoho Analytics UI, including case. Maximum length: 50 characters. |
| `viewName` | String | No | — | The exact display name of a view within the workspace. When provided, the response additionally includes the view's ID, type, and description. When omitted, only workspace information is returned. Maximum length: 50 characters. |

## Notes from the OpenAPI specification

- Workspace names are unique within an organisation and view names are unique within a workspace. The match is exact and case sensitive, so `Sales Analytics` and `sales analytics` are treated as different names.
- The lookup is scoped to the organisation sent in the `ZANALYTICS-ORGID` header. A workspace of the same name in a different organisation is not found, and the request fails with error code 7104.
- When `viewName` is sent and the view does not exist in the workspace, the request fails with error code 7104. Workspace metadata is not returned in failure responses.
- When `viewName` is sent, permission is checked against the view. If the view is not accessible to the user, the request fails with error code 7301 even when the user can see the workspace.
- A workspace-only lookup succeeds only when at least one view in the workspace is shared with the user. If the workspace holds views but none are shared with the user, the request fails with error code 7301.
- This API is the recommended way to bootstrap name-based integrations. Resolve `workspaceId` and `viewId` here and pass them to downstream APIs, instead of hard-coding numeric IDs that can change across environments.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `data.workspaces.workspaceId` | String | Numeric ID of the workspace. Use this as `<workspace-id>` in workspace-scoped API URLs. |
| `data.workspaces.workspaceName` | String | Display name of the workspace (echoed from the request). |
| `data.workspaces.workspaceDesc` | String | Description of the workspace. Empty string if not set. |
| `data.workspaces.orgId` | String | Organisation ID that owns this workspace. |
| `data.views` | Object | Present only when `viewName` was included in the request. |
| `data.views.viewId` | String | Numeric ID of the view. Use this as `<view-id>` in view-scoped API URLs. |
| `data.views.viewName` | String | Display name of the view (echoed from the request). |
| `data.views.viewDesc` | String | Description of the view. Empty string if not set. |
| `data.views.viewType` | String | Type of the view (e.g., `"Table"`, `"AnalysisView"`, `"Pivot"`, `"SummaryView"`, `"Query Table"`, `"Dashboard"`). |

# Examples

## Sample Requests

**Case 1 — Look up a workspace by name only**

```http
GET /restapi/v2/metadetails?CONFIG={"workspaceName":"Sales Analytics"} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Look up a workspace and a specific view within it**

```http
GET /restapi/v2/metadetails?CONFIG={"workspaceName":"Sales Analytics","viewName":"Revenue Trend"} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — Shared user resolving the ID of a view they have access to**

```http
GET /restapi/v2/metadetails?CONFIG={"workspaceName":"V2Api_WhiteLabelUsers_analytics","viewName":"ChartWL1"} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
ZANALYTICS-ORGID: 700000789012
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Workspace-only lookup**
```json
{
  "status": "success",
  "summary": "Get meta details",
  "data": {
    "workspaces": {
      "workspaceId": "320862000000625871",
      "workspaceName": "Sales Analytics",
      "workspaceDesc": "",
      "orgId": "106044221"
    }
  }
}
```

**Case 2 — Workspace and view lookup (Admin user)**
```json
{
  "status": "success",
  "summary": "Get meta details",
  "data": {
    "workspaces": {
      "workspaceId": "38190000004180410",
      "workspaceName": "Sales Analytics",
      "workspaceDesc": "Main sales reporting workspace",
      "orgId": "57058019"
    },
    "views": {
      "viewId": "38190000004180412",
      "viewName": "Revenue Trend",
      "viewDesc": "",
      "viewType": "AnalysisView"
    }
  }
}
```

**Case 3 — Shared user resolving a view they have access to**
```json
{
  "status": "success",
  "summary": "Get meta details",
  "data": {
    "workspaces": {
      "workspaceId": "38190000004180410",
      "workspaceName": "V2Api_WhiteLabelUsers_analytics",
      "workspaceDesc": "",
      "orgId": "57058019"
    },
    "views": {
      "viewId": "38190000004180412",
      "viewName": "ChartWL1",
      "viewDesc": "",
      "viewType": "AnalysisView"
    }
  }
}
```

**Case 4 — Permission denied (user has no access to the workspace or view)**

```json
{
  "status": "failure",
  "summary": "SECURITY_NOT_PERMITTED",
  "data": {
    "errorCode": 7301,
    "errorMessage": "You do not have the permission to get information. You need to have READ permission to do this operation."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Meta Details From Name](../../../sdk-examples/organization-management/org-info-and-settings/get-meta-details.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Organisation not found. | Verify the `ZANALYTICS-ORGID` header value. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | Workspace or view not found by the provided name. | Verify the exact spelling and case of `workspaceName` and `viewName`. Names are case-sensitive. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have Read access on the workspace or view. | Ensure the workspace or view is shared with the user, or the user has Workspace Admin / Account Admin / Organization Admin role. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Organization Info & Settings overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Organization Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Org List](get-organizations.md), [Get Resource Details](get-resource-details.md), [Get Subscription Details](get-subscription-details.md).
- [SDK examples](../../../sdk-examples/organization-management/org-info-and-settings/get-meta-details.md).
