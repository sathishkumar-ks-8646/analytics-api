---
type: API Endpoint
title: Get View Details
description: Returns the metadata of a single view identified by its view ID.
resource: "https://analyticsapi.zoho.com/restapi/v2/views/{view-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - view-operations
  - get
  - metadata
api:
  operation_id: getViewDetails
  method: GET
  path: "/restapi/v2/views/{view-id}"
  domain: views-management
  group: view-operations
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: not-required
  config_parameter:
    location: query
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must have at least Read Only permission on the view. This includes Account Admins, Organization Admins, Workspace Admins, View Owners, and any user with Read Only or higher access to the view."
  error_codes:
    - 7104
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1views~1{view-id}/get"
    config_schema: GetViewDetailsConfig
    response_schema: GetViewDetailsResponse
  sdk_examples: "/sdk-examples/views-management/view-operations/get-view-details.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**GET `/restapi/v2/views/{view-id}`** - Get View Details (View Operations / Views Management).

Returns detailed metadata for a single view identified by its view ID. Unlike the Get View List API, this API does not require a workspace ID in the URL — the view is resolved directly by its ID. Optionally returns extended metadata including column definitions and involved views.

> **No workspace ID in the URL:** This endpoint resolves the view globally by `<view-id>`. The workspace is derived from the view's metadata. This is different from all other workspace-scoped APIs in this document.

From the OpenAPI specification:

Returns the metadata of a single view identified by its view ID. The view is resolved globally, so unlike the other APIs in this module no workspace ID is needed in the URL - the workspace is derived from the view itself.

By default only the base attributes are returned. Setting `withInvolvedMetaInfo` to `true` adds extended metadata whose shape depends on the view type: column definitions and a row count for tables and query tables, the tab structure for a tabbed dashboard, and the list of parent views for an analysis view or a regular dashboard. Some of those extended fields are restricted to Workspace Admins.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getViewDetails` |
| HTTP method | GET |
| URL | `/restapi/v2/views/{view-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | Not required (user-scoped API) |
| Permission required | The authenticated user must have at least Read Only permission on the view. This includes Account Admins, Organization Admins, Workspace Admins, View Owners, and any user with Read Only or higher access to the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - optional |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1views~1{view-id}/get`; CONFIG schema `GetViewDetailsConfig`; response schema `GetViewDetailsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | - | Not required | This API is user-scoped and works across all organizations of the caller. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameter

The CONFIG parameter is optional. When provided, it is a JSON object passed as a **query parameter** named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `withInvolvedMetaInfo` | Boolean | No | `false` | When `false` (default): returns only the basic view attributes (ID, name, description, type, workspace, org, timestamps). When `true`: returns extended metadata depending on the view type — see the **Extended Metadata by View Type** table below. For extended data that is restricted to Workspace Admins (column details, row count, involved view list), non-admin users still get the base fields; the restricted extended fields are returned as `null` or omitted for non-admins. |

### Extended Metadata by View Type (`withInvolvedMetaInfo=true`)

| View Type | Additional Fields Returned | Admin-Only? |
|-----------|---------------------------|------------|
| **Table** | `columns` (array of column details), `rowCount` (integer) | `rowCount` is Workspace Admin only; `columns` is returned for all users with access |
| **QueryTable** | `columns` (array of column details), `rowCount`, `involvedViews` (parent tables used in the query) | `rowCount` and `involvedViews` are Workspace Admin only |
| **Tabbed Dashboard** | `tabs` (array of tab objects, each with `tabId`, `tabName`, and `involvedViews`) | Workspace Admin only |
| **Analysis View / Pivot / Summary / Regular Dashboard** | `involvedViews` (parent tables/views the view is built on) | Workspace Admin only |

## Notes from the OpenAPI specification

- This endpoint resolves the view globally by **view-id**. No workspace ID is needed in the URL and the workspace is derived from the view metadata, unlike every other workspace-scoped API in this module.
- **ZANALYTICS-ORGID** is not required by the framework for this API, though sending it is harmless and is recommended for consistency.
- The CONFIG parameter is optional. As this is a GET request, the value must be stringified and URL encoded before it is sent.
- With **withInvolvedMetaInfo** as false, only the base attributes of the view are returned.
- With **withInvolvedMetaInfo** as true the extended fields depend on the view type. A Table returns **columns** and **rowCount**; a QueryTable returns **columns**, **rowCount** and **involvedViews**; a tabbed dashboard returns **tabs**; an analysis view, pivot, summary view or regular dashboard returns **involvedViews**.
- **rowCount**, **involvedViews** and **tabs** are restricted to Workspace Admins. A non-admin receives them as null, while **columns** is still returned for the views they can access.
- **rowCount** is 0 for a Live Connect table regardless of the volume of remote data, and such a view also carries **isLive** as true.
- **isTabbedDashboard** is present only on a dashboard that uses a tabbed layout. It is returned even when **withInvolvedMetaInfo** is false, whereas **tabs** is not.
- **parentViewId** is present only when **viewType** is Tab, where it holds the ID of the parent tabbed dashboard.
- Requesting a dashboard tab by its own view ID returns the tab's basic info. The views it contains are returned only with **withInvolvedMetaInfo** as true and Workspace Admin rights.
- A view owner who is not a Workspace Admin still receives the timestamp and creator fields, but the admin-restricted extended fields are omitted.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Present When | Description |
|-------|------|-------------|-------------|
| `viewId` | String | Always | Unique identifier of the view. |
| `viewName` | String | Always | Display name. |
| `viewDesc` | String | Always | Description. Empty string if none. |
| `viewType` | String | Always | View type string. See the View Type Reference table in [Get View List](get-views.md). |
| `workspaceId` | String | Always | Workspace this view belongs to. |
| `orgId` | String | Always | Organisation this view belongs to. |
| `createdTime` | String | When user has at least workspace access | Creation timestamp in epoch milliseconds. |
| `createdBy` | String | When user has at least workspace access | Email of the view creator. |
| `createdByName` | String | When user has at least workspace access | Full name of the view creator. |
| `createdByZuId` | String | When user has at least workspace access | ZUID of the view creator. |
| `lastDesignModifiedTime` | String | When user has at least workspace access | Last design change timestamp in epoch milliseconds. |
| `lastDesignModifiedBy` | String | When user has at least workspace access | Email of last design modifier. |
| `lastDesignModifiedByName` | String | When user has at least workspace access | Full name of last design modifier. |
| `lastDesignModifiedByZuId` | String | When user has at least workspace access | ZUID of last design modifier. |
| `isTabbedDashboard` | Boolean | Dashboards that are tabbed | `true` when the dashboard uses tabbed layout. Absent for regular dashboards. |
| `parentViewId` | String | Dashboard Tabs only | ID of the parent Tabbed Dashboard. |
| `isLive` | Boolean | Live-connected non-dashboard views | `true` if the view is backed by a Live Connect data source. |
| `rowCount` | Long | Tables & QueryTables, `withInvolvedMetaInfo=true`, Workspace Admin only | Number of rows in the table. `0` for Remote DB (Live Connect) tables. |
| `columns` | Array | Tables & QueryTables, `withInvolvedMetaInfo=true` | Column metadata array. See Column Fields table below. |
| `involvedViews` | Array | Analysis views, regular dashboards, QueryTables, `withInvolvedMetaInfo=true`, Workspace Admin only | Parent tables or views that this view is built on. |
| `tabs` | Array | Tabbed Dashboards, `withInvolvedMetaInfo=true`, Workspace Admin only | Array of tab objects with their contained views. |

### Column Fields (within `columns` array)

| Field | Type | Description |
|-------|------|-------------|
| `columnId` | String | Unique identifier of the column. |
| `columnName` | String | Display name of the column. |
| `dataType` | String | Internal data type identifier (e.g., `PLAIN`, `DATE_AS_DATE`, `CURRENCY`). |
| `dataTypeId` | Integer | Numeric data type ID. |
| `dataTypeName` | String | Human-readable data type name (e.g., `"Plain Text"`, `"Date"`, `"Currency"`). |
| `columnIndex` | Integer | 1-based position of the column in the table. |
| `columnDesc` | String | Column description. |
| `columnMaxSize` | Integer | Maximum storage size of the column. |
| `isNullable` | Boolean | `true` if the column allows null values. |
| `defaultValue` | String | Default value for the column. Empty string if none. |
| `pkTableName` | String | Name of the referenced table if this column is a lookup (foreign key). Empty string otherwise. |
| `pkColumnName` | String | Name of the referenced column for a lookup. Empty string otherwise. |
| `formulaDisplayName` | String | Formula expression display name for formula columns. Empty for regular columns. |
| `isHidden` | Boolean | `true` if the column is hidden from the view. |
| `sortedOrder` | Integer | Sort direction applied to this column: `0` = none, `1` = ascending, `-1` = descending. |
| `sortedIndex` | Integer | Position in the sort priority if multiple columns are sorted. `-1` if not in sort order. |
| `dateFormat` | String | Date format string (e.g., `"dd MMMM, yyyy"`). Present only for date columns. |
| `currencyFormat` | String | Currency format string. Present only for currency columns. |
| `thousandSeparator` | String | Thousand separator character for numeric columns. |
| `decimalSeparator` | String | Decimal separator character for numeric columns. |
| `decimalPlaces` | Integer | Number of decimal places for numeric columns. |

# Examples

## Sample Requests

**Case 1 — Get basic details of a table**

```http
GET /restapi/v2/views/137687000000471835 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

**Case 2 — Get extended metadata for a table (with columns)**

```http
GET /restapi/v2/views/137687000000471835?CONFIG={"withInvolvedMetaInfo":true} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

**Case 3 — Get details of a tabbed dashboard with tab info**

```http
GET /restapi/v2/views/137687000015400002?CONFIG={"withInvolvedMetaInfo":true} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

## Sample Responses

**Case 1 — Basic view info (Table)**
```json
{
  "status": "success",
  "summary": "Get view details",
  "data": {
    "views": {
      "viewId": "137687000000471835",
      "viewName": "Sales",
      "viewDesc": "",
      "viewType": "Table",
      "workspaceId": "137687000000471833",
      "orgId": "64036181",
      "createdTime": "1619175390377",
      "createdBy": "admin@example.com",
      "createdByName": "RestapiAdmin V2",
      "createdByZuId": "64035928",
      "lastDesignModifiedTime": "1619175390377",
      "lastDesignModifiedBy": "admin@example.com",
      "lastDesignModifiedByName": "RestapiAdmin V2",
      "lastDesignModifiedByZuId": "64035928"
    }
  }
}
```

**Case 2 — Extended info for a Table with columns (`withInvolvedMetaInfo=true`)**
```json
{
  "status": "success",
  "summary": "Get view details",
  "data": {
    "views": {
      "viewId": "137687000000471835",
      "viewName": "Sales",
      "viewDesc": "",
      "viewType": "Table",
      "workspaceId": "137687000000471833",
      "orgId": "64036181",
      "createdTime": "1619175390377",
      "createdBy": "admin@example.com",
      "createdByName": "RestapiAdmin V2",
      "createdByZuId": "64035928",
      "lastDesignModifiedTime": "1619175390377",
      "lastDesignModifiedBy": "admin@example.com",
      "lastDesignModifiedByName": "RestapiAdmin V2",
      "lastDesignModifiedByZuId": "64035928",
      "rowCount": 4820,
      "columns": [
        {
          "columnId": "137687000000471840",
          "columnName": "Date",
          "dataType": "DATE_AS_DATE",
          "dataTypeId": 22,
          "dataTypeName": "Date",
          "columnIndex": 1,
          "columnDesc": "",
          "columnMaxSize": 19,
          "isNullable": true,
          "defaultValue": "",
          "pkTableName": "",
          "pkColumnName": "",
          "formulaDisplayName": "",
          "dateFormat": "dd MMMM, yyyy",
          "isHidden": false,
          "sortedOrder": 0,
          "sortedIndex": -1
        },
        {
          "columnId": "137687000000471841",
          "columnName": "Region",
          "dataType": "PLAIN",
          "dataTypeId": 1,
          "dataTypeName": "Plain Text",
          "columnIndex": 2,
          "columnDesc": "",
          "columnMaxSize": 253,
          "isNullable": true,
          "defaultValue": "",
          "pkTableName": "",
          "pkColumnName": "",
          "formulaDisplayName": "",
          "isHidden": false,
          "sortedOrder": 0,
          "sortedIndex": -1
        }
      ]
    }
  }
}
```

**Case 3 — Tabbed Dashboard with tabs and involved views (`withInvolvedMetaInfo=true`, Workspace Admin)**
```json
{
  "status": "success",
  "summary": "Get view details",
  "data": {
    "views": {
      "viewId": "137687000015400002",
      "viewName": "TabbedDashboard",
      "viewDesc": "",
      "viewType": "Dashboard",
      "workspaceId": "137687000000471833",
      "orgId": "64036181",
      "createdTime": "1650282725951",
      "createdBy": "admin@example.com",
      "createdByName": "RestapiAdmin V2",
      "createdByZuId": "64035928",
      "lastDesignModifiedTime": "1650282868999",
      "lastDesignModifiedBy": "admin@example.com",
      "lastDesignModifiedByName": "RestapiAdmin V2",
      "lastDesignModifiedByZuId": "64035928",
      "isTabbedDashboard": true,
      "tabs": [
        {
          "tabId": "137687000015400051",
          "tabName": "Tab1",
          "involvedViews": [
            { "viewId": "137687000000471835", "viewName": "Sales", "viewType": "Table" },
            { "viewId": "137687000000471839", "viewName": "ProfitindifferentProducts.", "viewType": "Pivot View" },
            { "viewId": "137687000000471842", "viewName": "SalesVsProfit", "viewType": "Chart View" }
          ]
        },
        {
          "tabId": "137687000015400059",
          "tabName": "Tab2",
          "involvedViews": [
            { "viewId": "137687000000471836", "viewName": "Average Sales in a Day", "viewType": "Chart View" },
            { "viewId": "137687000000471840", "viewName": "Sales and Profit in each Region", "viewType": "Chart View" }
          ]
        }
      ]
    }
  }
}
```

**Case 4 — Dashboard Tab (individual tab within a tabbed dashboard)**
```json
{
  "status": "success",
  "summary": "Get view details",
  "data": {
    "views": {
      "viewId": "137687000015400059",
      "viewName": "Tab2",
      "viewDesc": "",
      "viewType": "Tab",
      "workspaceId": "137687000000471833",
      "orgId": "64036181",
      "createdTime": "1650282855067",
      "createdBy": "admin@example.com",
      "createdByName": "RestapiAdmin V2",
      "createdByZuId": "64035928",
      "lastDesignModifiedTime": "1650282868991",
      "lastDesignModifiedBy": "admin@example.com",
      "lastDesignModifiedByName": "RestapiAdmin V2",
      "lastDesignModifiedByZuId": "64035928",
      "parentViewId": "137687000015400002"
    }
  }
}
```

> **Note on `parentViewId` for Dashboard Tabs:** When the view is a Tab (`viewType: "Tab"`), the `parentViewId` field is present and contains the ID of the parent Tabbed Dashboard. For all other view types, this field is absent.

**Case 5 — QueryTable with involved parent tables (`withInvolvedMetaInfo=true`, Workspace Admin)**
```json
{
  "status": "success",
  "summary": "Get view details",
  "data": {
    "views": {
      "viewId": "137687000000471848",
      "viewName": "SalesQT",
      "viewDesc": "SQL-joined query table",
      "viewType": "QueryTable",
      "workspaceId": "137687000000471833",
      "orgId": "64036181",
      "createdTime": "1619175390377",
      "createdBy": "admin@example.com",
      "createdByName": "RestapiAdmin V2",
      "createdByZuId": "64035928",
      "lastDesignModifiedTime": "1619175390377",
      "lastDesignModifiedBy": "admin@example.com",
      "lastDesignModifiedByName": "RestapiAdmin V2",
      "lastDesignModifiedByZuId": "64035928",
      "rowCount": 0,
      "columns": [
        {
          "columnId": "137687000000471860",
          "columnName": "Cost",
          "dataType": "CURRENCY",
          "dataTypeId": 7,
          "dataTypeName": "Currency",
          "columnIndex": 1,
          "columnDesc": "",
          "columnMaxSize": 19,
          "isNullable": true,
          "defaultValue": "",
          "pkTableName": "",
          "pkColumnName": "",
          "formulaDisplayName": "",
          "isHidden": false,
          "sortedOrder": 0,
          "sortedIndex": -1
        }
      ],
      "involvedViews": [
        { "viewId": "137687000000471835", "viewName": "Sales", "viewType": "Table" },
        { "viewId": "137687000000471836", "viewName": "Products", "viewType": "Table" }
      ]
    }
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get View Details](../../../sdk-examples/views-management/view-operations/get-view-details.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | View not found. | Verify `<view-id>` is valid and accessible. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have Read Only permission on the view. | Ensure the user has been granted at least Read Only access to the view. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [View Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Save As View](save-as-view.md), [Copy Views](copy-views.md), [Create Similar Views](create-similar-views.md), [Rename View](rename-view.md), [Delete View](delete-view.md), [Get View List](get-views.md), [Get View URL](get-view-url.md), [Get View Dependents](get-view-dependents.md), [Get Recent Views](get-recent-views.md).
- [SDK examples](../../../sdk-examples/views-management/view-operations/get-view-details.md).
