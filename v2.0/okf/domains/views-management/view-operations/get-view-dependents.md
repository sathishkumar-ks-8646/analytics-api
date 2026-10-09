---
type: API Endpoint
title: Get View Dependents
description: Returns every active view that depends on the specified view.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/dependents"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - view-operations
  - get
  - metadata
api:
  operation_id: getViewDependents
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/dependents"
  domain: views-management
  group: view-operations
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin, Organization Admin, or Workspace Admin."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 7319
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1dependents/get"
    config_schema: null
    response_schema: GetViewDependentsResponse
  sdk_examples: "/sdk-examples/views-management/view-operations/get-view-dependents.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/dependents`** - Get View Dependents (View Operations / Views Management).

Returns all active views that **depend on** the specified view. A dependent view is any view that cannot exist independently without the specified source view — for example, a chart built on a table, a pivot built on a query table, or a query table built on another query table. Useful before a Delete operation to understand the full impact.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getViewDependents` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/dependents` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organization ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin, Organization Admin, or Workspace Admin. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1dependents/get`; response schema `GetViewDependentsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- This API has no CONFIG parameter. The only inputs are the **workspace-id** and **view-id** path parameters.
- What counts as a dependent varies by the type of the source view. A **table** returns every analysis view, query table and pipeline table built on it directly or transitively, plus the dashboards that contain any of them. A **query table** returns the views built on it directly and transitively, the dashboards containing them, and the parent query tables that reference it in their SQL. An **analysis view, pivot table or summary view** returns the dashboards that embed it. A **dashboard** returns an empty list, since dashboards are leaf nodes of the dependency graph. A **dashboard tab** returns the views embedded within that tab.
- The full transitive chain is returned, not just the direct dependents. For a table feeding a query table feeding a chart placed on a dashboard, all of them are listed - the result is the complete set of views that would break if the source view were deleted.
- Dashboard tabs are never listed as dependents. The parent tabbed dashboard is listed instead. Use the Get View Details API with **withInvolvedMetaInfo** as true to inspect the contents of an individual tab.
- Only downstream views are returned. The tables that the source view itself depends on are not listed; use the Get View Details API for those.
- Only active views are returned. Views that have been moved to Trash are excluded.
- A view with no dependents returns HTTP 200 with an empty **views** array. No error is raised.
- The **viewType** labels here differ from those of the Get View List API - a chart appears as Chart View rather than AnalysisView. Use **viewTypeId** when the integer type code is needed.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `data.views` | Array | List of views that depend on the specified view. Empty array if no dependents exist. |
| `views[].viewId` | String | Unique ID of the dependent view. |
| `views[].viewName` | String | Display name of the dependent view. |
| `views[].viewTypeId` | Integer | Integer type code. See the View Type Reference table in [Get View List](get-views.md). |
| `views[].viewType` | String | Human-readable type label (e.g., `"Chart View"`, `"Pivot View"`, `"Query Table"`, `"Dashboard"`). Note: these labels differ slightly from the `viewType` string in the Get View List response (e.g., `"Chart View"` here vs `"AnalysisView"` in listing). |

# Examples

## Sample Requests

**Case 1 — Get dependents of a table**

```http
GET /restapi/v2/workspaces/466206000000071000/views/466206000000105001/dependents HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Get dependents of a query table**

```http
GET /restapi/v2/workspaces/466206000000071000/views/466206000000115006/dependents HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — Get dependents of a dashboard (expected: empty)**

```http
GET /restapi/v2/workspaces/466206000000071000/views/466206000000109002/dependents HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Table with chart and pivot dependents, and a dashboard that embeds them**
```json
{
  "status": "success",
  "summary": "Get view dependents",
  "data": {
    "views": [
      {
        "viewId": "466206000000105010",
        "viewName": "Revenue Trend",
        "viewTypeId": 2,
        "viewType": "Chart View"
      },
      {
        "viewId": "466206000000105011",
        "viewName": "Sales by Region",
        "viewTypeId": 3,
        "viewType": "Pivot View"
      },
      {
        "viewId": "466206000000105012",
        "viewName": "Monthly Summary",
        "viewTypeId": 4,
        "viewType": "Summary View"
      },
      {
        "viewId": "466206000000109002",
        "viewName": "Executive Dashboard",
        "viewTypeId": 7,
        "viewType": "Dashboard"
      }
    ]
  }
}
```

**Case 2 — Query Table with child query table and analysis views**
```json
{
  "status": "success",
  "summary": "Get view dependents",
  "data": {
    "views": [
      {
        "viewId": "466206000000115010",
        "viewName": "SalesQT_Child",
        "viewTypeId": 6,
        "viewType": "Query Table"
      },
      {
        "viewId": "466206000000115011",
        "viewName": "QT_Chart_Analysis",
        "viewTypeId": 2,
        "viewType": "Chart View"
      },
      {
        "viewId": "466206000000115012",
        "viewName": "QT_Pivot_Analysis",
        "viewTypeId": 3,
        "viewType": "Pivot View"
      }
    ]
  }
}
```

**Case 3 — Dashboard (no dependents)**
```json
{
  "status": "success",
  "summary": "Get view dependents",
  "data": {
    "views": []
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get View Dependents](../../../sdk-examples/views-management/view-operations/get-view-dependents.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

## Dependency Resolution Rules

| Source View Type | What is Returned as Dependents |
|-----------------|-------------------------------|
| **Table** | All analysis views (charts, pivots, summaries, tabular views), query tables, and pipeline tables built directly or transitively on this table. Also includes any **dashboards** that contain any of those dependent views. |
| **Query Table** | All views built on this query table (direct), plus views built on those views (transitive). Dashboards containing any of those views. Also returns parent query tables that reference this query table in their SQL. |
| **Analysis View / Pivot / Summary** | Any dashboards that embed this view. No child views (analysis views cannot be parents themselves). |
| **Dashboard** | Empty list — dashboards have no dependents in the view graph. |
| **Dashboard Tab** | Any views embedded within this tab. |

> **Important:** Dashboard **Tabs** themselves are **never listed** as dependents. The response lists the parent Dashboard object instead. Individual tabs are excluded from the dependent list.

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | View not found. | Verify `<view-id>` exists in the workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not a Workspace Admin, Account Admin, or Organization Admin. | Ensure the user has Workspace Admin or higher role in this workspace. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | View does not belong to the specified workspace. | Verify both `<workspace-id>` and `<view-id>` are consistent. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [View Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Save As View](save-as-view.md), [Copy Views](copy-views.md), [Create Similar Views](create-similar-views.md), [Rename View](rename-view.md), [Delete View](delete-view.md), [Get View List](get-views.md), [Get View Details](get-view-details.md), [Get View URL](get-view-url.md), [Get Recent Views](get-recent-views.md).
- [SDK examples](../../../sdk-examples/views-management/view-operations/get-view-dependents.md).
