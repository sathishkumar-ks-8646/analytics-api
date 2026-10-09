---
type: API Endpoint
title: Get Report Metadata
description: "Retrieves the full configuration metadata of an existing analysis view - a chart, a pivot table or a summary view - in the specified workspace."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata"
tags:
  - zoho-analytics
  - rest-api-v2
  - reports-and-dashboards
  - reports
  - get
  - modeling
api:
  operation_id: getReportMetadata
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata"
  domain: reports-and-dashboards
  group: reports
  oauth_scopes:
    - ZohoAnalytics.modeling.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or the View Owner, or any user with Design Modify permission on the view."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 8021
    - 8535
  openapi:
    file: "/references/openapi/reports-dashboards-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1reports~1{view-id}~1metadata/get"
    config_schema: null
    response_schema: GetReportMetadataResponse
  sdk_examples: "/sdk-examples/reports-and-dashboards/reports/get-report-metadata.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata`** - Get Report Metadata (Reports (Analysis Views) / Reports & Dashboards).

> This API has no `CONFIG` request parameter. All inputs are provided via URL path parameters.

From the OpenAPI specification:

Retrieves the full configuration metadata of an existing analysis view - a chart, a pivot table or a summary view - in the specified workspace. The response carries the report type, the chart sub-type, the axis column definitions, the applied filters and the visualization settings exactly as they are stored.

The returned `reportConfig` is structurally identical to the Create Analysis View CONFIG, which makes this API the first step of any safe update or clone workflow.

The authenticated user must be an Account Admin or an Organization Admin, or the View Owner, or any user with Design Modify permission on the view.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getReportMetadata` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingread) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or the View Owner, or any user with Design Modify permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`reports-dashboards-grouped-api.json`](../../../references/openapi/reports-dashboards-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1reports~1{view-id}~1metadata/get`; response schema `GetReportMetadataResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace that contains the analysis view. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the analysis view whose metadata is retrieved. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

This is a workspace-scoped API. The **ZANALYTICS-ORGID** header carrying the organization ID that owns the workspace is mandatory. A workspaceKey in the format **orgid/workspacename** (for example, 700000123456/Sales_Analytics) may be used in place of the numeric workspace ID in the URL path.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success` or `failure`. |
| `summary` | string | Always `"Get analysis view metadata"` on success. |
| `data.reportConfig` | JSONObject | The full configuration of the analysis view as stored. |
| `data.reportConfig.title` | string | Display name of the view. |
| `data.reportConfig.description` | string | Description of the view (omitted if empty). |
| `data.reportConfig.reportType` | string | View type: `chart`, `pivot`, or `summary`. |
| `data.reportConfig.chartType` | string | Chart sub-type (e.g., `bar`, `line`, `pie`, `bubble`, `stacked bar`, `heat map`). Present for `chart` views. |
| `data.reportConfig.baseTableName` | string | The name of the base table the view is built on. |
| `data.reportConfig.isAxisMerge` | boolean | `true` if multiple y-axes are merged onto a single axis. |
| `data.reportConfig.axisColumns` | JSONArray | Array of axis column objects defining the view's dimensions and measures. |
| `data.reportConfig.filters` | JSONArray | Array of data filter objects applied to the view. Omitted if no filters exist. |
| `data.reportConfig.userFilters` | JSONArray | Array of user-interactive filter objects. Omitted if none exist. |
| `data.reportConfig.settings` | JSONObject | Layout and theme settings. Omitted if no settings are configured. |

## Notes from the OpenAPI specification

Axis type values are spelled the same way in every direction. The Create and Update CONFIG accept the camelCase forms (**xAxis**, **yAxis**, **colorAxis**, **sizeAxis**, **textAxis**, **groupBy**, **summarize**) and Get Report Metadata returns them in that same form. When building a Create or Update CONFIG from a Get Report Metadata response, copy the axis type values verbatim.

Update Analysis View performs a full configuration reset, not a patch.
- Every axis column, filter, user filter and settings entry is replaced with the values sent in the CONFIG.
- Fields that are not provided revert to their empty defaults - omitting **axisColumns**, **filters** or **userFilters** clears them.
- **description** is cleared if it is omitted.
- Always fetch the current state with Get Report Metadata, modify it, then send the complete configuration back.

The **reportConfig** object returned by Get Report Metadata is structurally identical to the Create CONFIG, so it can be used directly as a clone template. Change **title** to a value that is unique in the workspace, keep **baseTableName**, and verify that every **columnName** and **tableName** exists in the target workspace's base table before posting.

# Examples

## Sample Requests

**Case 1: Retrieve metadata for a bar chart view**

```http
GET /restapi/v2/workspaces/466206000000071000/reports/466206000000105001/metadata HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2: Retrieve metadata for a pivot or summary view**

```http
GET /restapi/v2/workspaces/466206000000071000/reports/466206000000106002/metadata HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**Case 1: Simple bar chart — basic axis configuration**

A chart view with a single x-axis (product dimension) and a single y-axis (aggregated sales). Demonstrates the minimum `reportConfig` structure returned for a standard vertical bar chart.

```http
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8

{
  "status": "success",
  "summary": "Get analysis view metadata",
  "data": {
    "reportConfig": {
      "title": "Bar Chart Report",
      "description": "Vertical bar chart",
      "reportType": "chart",
      "chartType": "bar",
      "baseTableName": "Sales",
      "isAxisMerge": false,
      "axisColumns": [
        {
          "type": "xAxis",
          "columnName": "Product",
          "tableName": "Sales",
          "operation": "actual"
        },
        {
          "type": "yAxis",
          "columnName": "Sales",
          "tableName": "Sales",
          "operation": "sum"
        }
      ]
    }
  }
}
```

**Case 2: Bubble chart — multiple axis types (xAxis, yAxis, sizeAxis)**

A bubble chart using three axis types. The `sizeAxis` entry controls the bubble size (average cost). Demonstrates how multi-axis charts are represented in `axisColumns`.

```http
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8

{
  "status": "success",
  "summary": "Get analysis view metadata",
  "data": {
    "reportConfig": {
      "title": "Bubble Chart",
      "description": "Bubble chart visualization",
      "reportType": "chart",
      "chartType": "bubble",
      "baseTableName": "Sales",
      "isAxisMerge": false,
      "axisColumns": [
        {
          "type": "xAxis",
          "columnName": "Product",
          "tableName": "Sales",
          "operation": "actual"
        },
        {
          "type": "yAxis",
          "columnName": "Sales",
          "tableName": "Sales",
          "operation": "sum"
        },
        {
          "type": "sizeAxis",
          "columnName": "Cost",
          "tableName": "Sales",
          "operation": "avg"
        }
      ]
    }
  }
}
```

**Case 3: Stacked bar chart with color axis — three-dimensional grouping**

A stacked bar chart that uses a `colorAxis` entry to split bars by a categorical dimension (Product), in addition to x-axis (year) and y-axis (sum of sales). Demonstrates how color-based grouping is stored in the axis column list.

```http
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8

{
  "status": "success",
  "summary": "Get analysis view metadata",
  "data": {
    "reportConfig": {
      "title": "Stacked Bar Chart",
      "description": "Stacked vertical bar chart",
      "reportType": "chart",
      "chartType": "stacked bar",
      "baseTableName": "Sales",
      "isAxisMerge": false,
      "axisColumns": [
        {
          "type": "xAxis",
          "columnName": "Date",
          "tableName": "Sales",
          "operation": "year"
        },
        {
          "type": "yAxis",
          "columnName": "Sales",
          "tableName": "Sales",
          "operation": "sum"
        },
        {
          "type": "colorAxis",
          "columnName": "Product",
          "tableName": "Sales",
          "operation": "actual"
        }
      ]
    }
  }
}
```

**Case 4: Chart with date filter applied — `filters` array in response**

A bar chart that has a date-range filter applied (years 2012 and 2013). Demonstrates how `filters` appear in the returned `reportConfig` when the view was saved with active data filters.

```http
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8

{
  "status": "success",
  "summary": "Get analysis view metadata",
  "data": {
    "reportConfig": {
      "title": "Date Filter Chart",
      "reportType": "chart",
      "chartType": "bar",
      "baseTableName": "Sales",
      "isAxisMerge": false,
      "axisColumns": [
        {
          "type": "xAxis",
          "columnName": "Date",
          "tableName": "Sales",
          "operation": "year"
        },
        {
          "type": "yAxis",
          "columnName": "Sales",
          "tableName": "Sales",
          "operation": "sum"
        }
      ],
      "filters": [
        {
          "tableName": "Sales",
          "columnName": "Date",
          "operation": "actual",
          "filterType": "year",
          "values": ["2012", "2013"],
          "exclude": false
        }
      ]
    }
  }
}
```

**Case 5: Combo chart with axis merge enabled — `isAxisMerge: true`**

A combo chart where two y-axes (Sales and Cost) are merged onto a single axis. The `isAxisMerge` flag is `true` and both y-axis columns appear in `axisColumns`. Demonstrates the axis merge configuration as persisted.

```http
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8

{
  "status": "success",
  "summary": "Get analysis view metadata",
  "data": {
    "reportConfig": {
      "title": "Chart With Axis Merge",
      "description": "Chart with axis merge enabled",
      "reportType": "chart",
      "chartType": "combo",
      "baseTableName": "Sales",
      "isAxisMerge": true,
      "axisColumns": [
        {
          "type": "xAxis",
          "columnName": "Date",
          "tableName": "Sales",
          "operation": "year"
        },
        {
          "type": "yAxis",
          "columnName": "Sales",
          "tableName": "Sales",
          "operation": "sum"
        },
        {
          "type": "yAxis",
          "columnName": "Cost",
          "tableName": "Sales",
          "operation": "sum"
        }
      ]
    }
  }
}
```

**Case 6: Chart with multiple wildcard filters — multiple `filters` entries**

A bar chart saved with two wildcard filters on different columns (Product and Region). Demonstrates how multiple filter objects are returned in the `filters` array when wildcard filtering is applied.

```http
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8

{
  "status": "success",
  "summary": "Get analysis view metadata",
  "data": {
    "reportConfig": {
      "title": "V2_Chart Multiple Wildcard Filters",
      "description": "Chart with multiple wildcard filters on different columns",
      "reportType": "chart",
      "chartType": "bar",
      "baseTableName": "Sales",
      "isAxisMerge": false,
      "axisColumns": [
        {
          "type": "xAxis",
          "columnName": "Product",
          "tableName": "Sales",
          "operation": "actual"
        },
        {
          "type": "yAxis",
          "columnName": "Sales",
          "tableName": "Sales",
          "operation": "sum"
        }
      ],
      "filters": [
        {
          "tableName": "Sales",
          "columnName": "Product",
          "operation": "actual",
          "filterType": "wildcard",
          "values": [],
          "exclude": false
        },
        {
          "tableName": "Sales",
          "columnName": "Region",
          "operation": "actual",
          "filterType": "wildcard",
          "values": [],
          "exclude": false
        }
      ]
    }
  }
}
```

**Case 7: Heat map chart — using colorAxis as the value measure**

A heat map chart where the color axis encodes the aggregated sales value, and the x/y axes represent product and year dimensions respectively. Demonstrates an alternate use of `colorAxis` as the primary measure axis.

```http
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8

{
  "status": "success",
  "summary": "Get analysis view metadata",
  "data": {
    "reportConfig": {
      "title": "Heat Map Chart",
      "description": "Heat map visualization",
      "reportType": "chart",
      "chartType": "heat map",
      "baseTableName": "Sales",
      "isAxisMerge": false,
      "axisColumns": [
        {
          "type": "xAxis",
          "columnName": "Product",
          "tableName": "Sales",
          "operation": "actual"
        },
        {
          "type": "yAxis",
          "columnName": "Date",
          "tableName": "Sales",
          "operation": "year"
        },
        {
          "type": "colorAxis",
          "columnName": "Sales",
          "tableName": "Sales",
          "operation": "sum"
        }
      ]
    }
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Report Metadata](../../../sdk-examples/reports-and-dashboards/reports/get-report-metadata.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Provide a valid `workspace-id` in the URL. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The specified view does not exist in the workspace. | Ensure the `view-id` in the URL corresponds to an existing analysis view. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission to view this report's metadata. | Ensure the user is an **Account Admin**, **Organization Admin**, **View Owner**, or has **Design Modify** permission on the view. |
| [8021](../../../foundations/error-codes.md#error-8021) | 400 | Invalid view type for the requested operation. | Ensure the target view is an analysis view (chart, pivot, or summary). |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid OAuth token. | Provide a valid, non-expired OAuth token in the `Authorization` header. |

# Related

- [Reports (Analysis Views) overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Reports & Dashboards](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Analysis View](create-report.md), [Update Analysis View](update-report.md).
- [SDK examples](../../../sdk-examples/reports-and-dashboards/reports/get-report-metadata.md).
