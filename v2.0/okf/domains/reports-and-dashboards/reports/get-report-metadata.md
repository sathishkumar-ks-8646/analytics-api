---
type: API Endpoint
title: Read Report Metadata
description: "Returns a summary of the stored definition of a chart, pivot or summary view."
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
  api_units:
    api_id: 3052
    action: GET_REPORT_METADATA
    category: METADATA
    units: 0.1
    units_basis: per_request
    units_note: "0.1 units per request"
    category_frequency_limit: 60 requests/minute
  oauth_scopes:
    - ZohoAnalytics.modeling.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The report's owner, or a user holding Design Modify on the report: Account Admin, Organization Admin, Workspace Owner, Workspace Admin, or a shared / group / Custom Role user granted edit rights. A read-only shared user cannot call this endpoint."
  error_codes:
    - 7103
    - 7104
    - 7106
    - 7301
    - 7309
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
    last_modified: 2026-10-26T11:33:28Z
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata`** - Read Report Metadata (Reports (Analysis Views) / Reports & Dashboards).

Returns a summary of the stored definition of a chart, pivot or summary view. The `<report-id>` comes
from [Create Report](create-report.md) (`data.viewId`) or from the workspace's view list.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getReportMetadata` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The report's owner, or a user holding Design Modify on the report: Account Admin, Organization Admin, Workspace Owner, Workspace Admin, or a shared / group / Custom Role user granted edit rights. A read-only shared user cannot call this endpoint. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| API units | 0.1 units per request - action `GET_REPORT_METADATA` (api-id `3052`), **METADATA** category. See [API units](../../../foundations/api-units.md). |
| Frequency limit | 60 requests/minute across all **METADATA**-category calls of the organization. See [API units](../../../foundations/api-units.md#unit-categories-and-frequency-limits). |
| OpenAPI | [`reports-dashboards-grouped-api.json`](../../../references/openapi/reports-dashboards-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1reports~1{view-id}~1metadata/get`; response schema `GetReportMetadataResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID, shown in the Zoho Analytics UI under Settings > Organisation. See [Identifiers](../../../foundations/identifiers.md). |

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

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get analysis view metadata"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.reportConfig` | JSONObject | The stored definition. **Always present** on success. |
| `data.reportConfig.title` | String | Report name. **Always present.** |
| `data.reportConfig.description` | String | Report description. **Absent** when no description is stored. |
| `data.reportConfig.reportType` | String | `chart`, `pivot`, `summary`, or `widget` for widget views. **Always present.** |
| `data.reportConfig.chartType` | String | Chart reports only, and only when the stored chart maps to a name — the *Returned on read* column of [`chartType` Values](overview.md#charttype-values). |
| `data.reportConfig.baseTableName` | String | Display name of the base table. **Always present.** |
| `data.reportConfig.isAxisMerge` | Boolean | Present when stored — always for charts created through [Create Report](create-report.md). |
| `data.reportConfig.axisColumns` | JSONArray | Present when the report has axis columns. |
| `axisColumns[].type` | String | Lowercase shelf name — see [Values that change across a round trip](overview.md#values-that-change-across-a-round-trip). **Absent** for widget views. |
| `axisColumns[].columnName` | String | Column display name. For a distinct-count or variance column, the **source** column's name. |
| `axisColumns[].tableName` | String | Table display name. **Always present**, even when omitted on write. |
| `axisColumns[].operation` | String | See [Axis Operations on Read](overview.md#axis-operations-on-read). |
| `data.reportConfig.mergeAxisInfo` | JSONArray | Charts with `isAxisMerge: true` only. One merge object, repeated — see [`mergeAxisInfo` on Read](overview.md#mergeaxisinfo-on-read). |
| `data.reportConfig.filters` | JSONArray | Present when the report has static filters. |
| `filters[].tableName` | String | Table display name. |
| `filters[].columnName` | String | Column display name. |
| `filters[].operation` | String | See [Values that change across a round trip](overview.md#values-that-change-across-a-round-trip). |
| `filters[].filterType` | String | See [Values that change across a round trip](overview.md#values-that-change-across-a-round-trip). |
| `filters[].values` | JSONArray of String | The stored display text split on commas. |
| `filters[].exclude` | Boolean | Whether the filter excludes its values. |
| `data.reportConfig.userFilters` | JSONArray | Present when the report has user filters. |
| `userFilters[].tableName` | String | Table display name. |
| `userFilters[].columnName` | String | Column display name. |
| `userFilters[].operation` | String | See [Values that change across a round trip](overview.md#values-that-change-across-a-round-trip). |

No other key is returned.

## Notes from the OpenAPI specification

The **reportConfig** returned by Read Report Metadata is a summary of the stored definition, not a Create or Update payload. It omits **folderId**, **settings**, **drillActionConfig**, **modifiedPaths**, every per-column **displayName**, **sort**, **rangeSize**, **windowFunction**, **format** and **geoRole**, the **wildcard**, **rankingColumn** and **additionalDetails** of filters, and every user-filter key except **tableName**, **columnName** and **operation**. Remove **baseTableName** and add **reportType** before using it as an update payload; for anything beyond trivial edits keep the CONFIG you submitted at create time and modify that.

Axis **type** values are returned in lowercase (**xaxis**, **yaxis**, **coloraxis**, **textaxis**, **groupby**, **tooltip**, **latlng**) whatever casing was sent; all of those are accepted on write. A **tooltip** column may be returned as **group**, which Create and Update reject with 8509.

# Examples

## Sample Requests

**Case 1 — Read a chart's definition**

```http
GET /restapi/v2/workspaces/466206000000071000/reports/466206000000105001/metadata HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Read a table ID instead of a report ID (rejected)**

```http
GET /restapi/v2/workspaces/466206000000071000/reports/466206000000071023/metadata HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — Chart with a static filter and a user filter (Case 1)**

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
                {"type": "xaxis", "columnName": "Order Date", "tableName": "Sales", "operation": "absmonth"},
                {"type": "yaxis", "columnName": "Sales", "tableName": "Sales", "operation": "sum"}
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
                {"tableName": "Sales", "columnName": "Product Category", "operation": "actual"}
            ]
        }
    }
}
```

**HTTP 400 Bad Request — The ID is not a report (Case 2)**

```json
{
    "status": "failure",
    "summary": "INVALID_VIEW_TYPE_IN_REQUEST",
    "data": {
        "errorCode": 8021,
        "errorMessage": "Invalid view type found in the request."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Read Report Metadata](../../../sdk-examples/reports-and-dashboards/reports/get-report-metadata.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Lossy summary** | The response omits every write-only field and normalises many values. It is **not** an Update payload — see [Round-tripping a Report](overview.md#round-tripping-a-report). |
| **Merged-axis charts** | `mergeAxisInfo` is returned in read form, not write form — see [`mergeAxisInfo` on Read](overview.md#mergeaxisinfo-on-read). |
| **Read-only** | Safe to repeat; nothing is changed. |
| **Client Portal / White Label** | Not available on Client Portal / White Label domains. Call the standard API host. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Create Report](create-report.md) → `data.viewId` (or the workspace's view list) → `<report-id>` → Read Report Metadata → `reportConfig` for inspection. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — The report does not exist. | Verify `<report-id>`. |
| [7106](../../../foundations/error-codes.md#error-7106) | 404 | `META_OBJECT_NOT_PRESENT` — The report has been deleted. | Verify `<report-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not the owner and lacks Design Modify permission on the report. | Grant the caller edit access to the report. |
| [7309](../../../foundations/error-codes.md#error-7309) | 400 | `SECURITY_NEEDS_LOGIN` — `Authorization` header absent. | Send `Authorization: Zoho-oauthtoken <token>`. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The report belongs to a different workspace. | Make `<workspace-id>` and `<report-id>` consistent. |
| [8021](../../../foundations/error-codes.md#error-8021) | 400 | `INVALID_VIEW_TYPE_IN_REQUEST` — The target is a table, query table or dashboard, not a report. | Use a report ID. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.read`. |

# Related

- [Reports (Analysis Views) overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Reports & Dashboards](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Report](create-report.md), [Update Report](update-report.md).
- [SDK examples](../../../sdk-examples/reports-and-dashboards/reports/get-report-metadata.md).
- [API units](../../../foundations/api-units.md) - unit cost, unit categories and frequency limits for every endpoint.
