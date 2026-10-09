---
type: API Endpoint
title: Read Report Metadata
description: "Returns the stored definition of a chart, pivot or summary view."
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
  permission_required: Design Modify on the report. A read-only shared user cannot call this endpoint.
  error_codes:
    - 7103
    - 7104
    - 7106
    - 7301
    - 7319
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
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata`** - Read Report Metadata (Reports (Analysis Views) / Reports & Dashboards).

Returns the stored definition of a chart, pivot or summary view.

> This API has no CONFIG parameter. All input is in the URL path.

From the OpenAPI specification:

Returns the stored definition of a chart, pivot or summary view.

Permission required: Design Modify on the report. A read-only shared user cannot call this endpoint.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getReportMetadata` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingread) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | Design Modify on the report. A read-only shared user cannot call this endpoint. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| Custom domain | Not permitted. |
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
| `{view-id}` | string | ID of the report (view) whose metadata is returned. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

This is a workspace-scoped API. The **ZANALYTICS-ORGID** header carrying the organization ID that owns the workspace is mandatory.

This API is not available on white-label / custom domains. Call the standard REST host for your data centre (**analyticsapi.zoho.com**, **analyticsapi.zoho.eu**, ...).

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Notes from the OpenAPI specification

The **reportConfig** returned by Read Report Metadata is a summary of the stored definition, not a Create or Update payload. It omits **folderId**, **settings**, **drillActionConfig**, **modifiedPaths**, every per-column **displayName**, **sort**, **rangeSize**, **windowFunction**, **format** and **geoRole**, the **wildcard**, **rankingColumn** and **additionalDetails** of filters, and every user-filter key except **tableName**, **columnName** and **operation**. Remove **baseTableName** and add **reportType** before using it as an update payload; for anything beyond trivial edits keep the CONFIG you submitted at create time and modify that.

Axis **type** values are returned in lowercase (**xaxis**, **yaxis**, **coloraxis**, **textaxis**, **groupby**, **tooltip**, **latlng**) whatever casing was sent; all of those are accepted on write. A **tooltip** column may be returned as **group**, which Create and Update reject with 8509.

# Examples

## Sample Requests

```http
GET /restapi/v2/workspaces/466206000000071000/reports/466206000000105001/metadata HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK**

```json
{
  "status": "success",
  "summary": "Get analysis view metadata",
  "data": {
    "reportConfig": {
      "title": "Sales Trend",
      "description": "Monthly trend, excluding returns",
      "reportType": "chart",
      "chartType": "line",
      "baseTableName": "Sales",
      "isAxisMerge": false,
      "axisColumns": [
        { "type": "xaxis", "columnName": "Order Date", "tableName": "Sales", "operation": "monthyear" },
        { "type": "yaxis", "columnName": "Sales",      "tableName": "Sales", "operation": "sum" }
      ],
      "filters": [
        {
          "tableName": "Sales",
          "columnName": "Status",
          "operation": "actual",
          "filterType": "individualvalues",
          "values": ["Returned"],
          "exclude": true
        }
      ],
      "userFilters": [
        {
          "tableName": "Sales",
          "columnName": "Product Category",
          "operation": "actual"
        }
      ]
    }
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Read Report Metadata](../../../sdk-examples/reports-and-dashboards/reports/get-report-metadata.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

> **The response is not a round-trippable CONFIG.** It is a *summary* of the stored definition, and it
> omits most of what Update accepts. In particular, `userFilters` entries come back with only
> `tableName`, `columnName` and `operation` — the widget type, criteria shape, values, default
> selections, exclusion flag and listing behaviour are all absent. Feeding this response straight back
> into [Update Report](update-report.md) will **rebuild every user filter with default behaviour** and
> drop all per-column formatting, sorting and window functions. See
> [Round-tripping a report](overview.md#round-tripping-a-report) for the full list of what is lost and what
> changes value on the way out.

What is and is not returned:

| Section | Returned | Not returned |
|---|---|---|
| Top level | `title`, `description`, `reportType`, `chartType`¹, `baseTableName`, `isAxisMerge`, `mergeAxisInfo` | `folderId`, `settings`, `drillActionConfig`, `modifiedPaths` |
| `axisColumns[]` | `type`, `columnName`, `tableName`, `operation` | `displayName`, `sort`, `rangeSize`, `windowFunction`, `format`, `geoRole` |
| `filters[]` | `tableName`, `columnName`, `operation`, `filterType`, `values`, `exclude` | `wildcard`, `rankingColumn`, `rankingColumnDateSubType`, `additionalDetails` |
| `userFilters[]` | `tableName`, `columnName`, `operation` | everything else |

¹ `chartType` is present only when the stored chart and sub-chart types map back to a known name; it is
omitted otherwise.

Calling this endpoint on a table, query table, dashboard or any non-analysis view raises **8021**.

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The report does not exist or has been deleted. | Verify `<report-id>`. |
| [7106](../../../foundations/error-codes.md#error-7106) | 404 | The report does not exist or has been deleted. | Verify `<report-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The caller lacks Design Modify permission on the report. | Grant edit access. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The report belongs to a different workspace. | Make the two path IDs consistent. |
| [8021](../../../foundations/error-codes.md#error-8021) | 400 | The target is not a chart, pivot or summary view. | Use a report ID, not a table or dashboard. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Refresh with scope `ZohoAnalytics.modeling.read`. |

# Related

- [Reports (Analysis Views) overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Reports & Dashboards](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Report](create-report.md), [Update Report](update-report.md).
- [SDK examples](../../../sdk-examples/reports-and-dashboards/reports/get-report-metadata.md).
