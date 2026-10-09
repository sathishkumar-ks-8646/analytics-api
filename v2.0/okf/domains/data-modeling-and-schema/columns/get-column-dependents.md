---
type: API Endpoint
title: Get Column Dependents
description: "Returns every view, custom formula column and aggregate formula that depends on the specified column."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/dependents"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - columns
  - get
  - metadata
api:
  operation_id: getColumnDependents
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/dependents"
  domain: data-modeling-and-schema
  group: columns
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: The authenticated user must be a Workspace Admin of the specified workspace.
  error_codes:
    - 7107
    - 7301
    - 7319
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1columns~1{column-id}~1dependents/get"
    config_schema: null
    response_schema: GetColumnDependentsResponse
  sdk_examples: "/sdk-examples/data-modeling-and-schema/columns/get-column-dependents.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/dependents`** - Get Column Dependents (Columns / Data Modeling & Schema).

Returns all views, custom formula columns, and aggregate formulas that depend on the specified column. Use this before deleting or renaming a column to understand the full impact.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getColumnDependents` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/dependents` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1columns~1{column-id}~1dependents/get`; response schema `GetColumnDependentsResponse` |

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
| `{column-id}` | string | ID of the column. | [How to obtain](../../../foundations/identifiers.md#column-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `views` | Array | List of views (reports, charts, pivot tables, query tables) that use this column. Empty array if none. |
| `views[].viewId` | String | Unique ID of the dependent view. |
| `views[].viewName` | String | Display name of the dependent view. |
| `views[].viewTypeId` | Integer | Numeric type ID: `1` = Report (Tabular), `2` = Chart, `3` = Pivot, `4` = Summary, `6` = Query Table. |
| `views[].reportType` | String | Human-readable type label: `"Report"`, `"Chart"`, `"PivotView"`, `"SummaryView"`, `"QueryTable"`. |
| `customFormulas` | Array | Formula columns in the same table whose expression uses this column. Empty array if none. |
| `customFormulas[].columnId` | String | Column ID of the formula column. |
| `customFormulas[].columnName` | String | Display name of the formula column. |
| `aggregateFormulas` | Array | Aggregate formula metrics that use this column. Empty array if none. |

## Notes from the OpenAPI specification

- Call this API before any destructive column operation. When views or customFormulas are non-empty, setting deleteDependentViews to true in the Delete Column API permanently removes all of those objects.
- Unlike the other column APIs, which also accept a user with Design Modify permission, this API requires full Workspace Admin access.
- The views array can list the same view more than once when the column is used in several ways within that view, for example as both a filter and a display column of a query table.
- Obtain the view-id from the Get View List API and the column-id from the Get Table Metadata API.

# Examples

## Sample Requests

**Case 1 — Get all dependents for a column**

```http
GET /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns/7617000000508026/dependents HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Workspace Admin checking a currency column's dependents before deletion**

```http
GET /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns/7617000000508030/dependents HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Column used in views and a custom formula**

```json
{
  "status": "success",
  "summary": "Get column dependents",
  "data": {
    "views": [
      {
        "viewId": "221641000006857125",
        "viewName": "Monthly Sales QT",
        "viewTypeId": 6,
        "reportType": "QueryTable"
      },
      {
        "viewId": "221641000006856603",
        "viewName": "Sales Tabular View",
        "viewTypeId": 1,
        "reportType": "Report"
      },
      {
        "viewId": "221641000006856594",
        "viewName": "Sales by Region",
        "viewTypeId": 2,
        "reportType": "Chart"
      },
      {
        "viewId": "221641000006856601",
        "viewName": "Sales Pivot",
        "viewTypeId": 3,
        "reportType": "PivotView"
      }
    ],
    "customFormulas": [
      {
        "columnId": "221641000006856615",
        "columnName": "Profit Margin"
      }
    ],
    "aggregateFormulas": []
  }
}
```

**Case 2 — Column with no dependents**

```json
{
  "status": "success",
  "summary": "Get column dependents",
  "data": {
    "views": [],
    "customFormulas": [],
    "aggregateFormulas": []
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Column Dependents](../../../sdk-examples/data-modeling-and-schema/columns/get-column-dependents.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Use before delete** | Always call this API before calling Delete Column to understand the full cascade impact. If `views` or `customFormulas` are non-empty, setting `deleteDependentViews: true` in Delete Column will permanently remove all those objects. |
| **Workspace Admin only** | Unlike most column APIs which accept users with Design Modify permission, this API requires full Workspace Admin access. |
| **`views` may contain duplicates** | The same view can appear multiple times if it uses the column in multiple ways (e.g., a query table that both filters and displays the column). |
| **Dependency** | `<view-id>` → Get View List. `<column-id>` → Get Table Metadata. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7107](../../../foundations/error-codes.md#error-7107) | 400 | The specified column does not exist in the table. | Verify `<column-id>` using Get Table Metadata. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Only Workspace Admins can call this API. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view ID does not belong to the specified workspace. | Confirm the `<view-id>` belongs to the workspace in the URL. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Columns overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Add Column](add-column.md), [Rename Column](rename-column.md), [Delete Column](delete-column.md), [Hide Columns](hide-columns.md), [Show Columns](show-columns.md), [Sort Data by Columns](sort-data-by-columns.md), [Reorder Columns](reorder-columns.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/columns/get-column-dependents.md).
