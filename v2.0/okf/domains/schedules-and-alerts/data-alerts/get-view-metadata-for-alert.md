---
type: API Endpoint
title: Get View Metadata For Alert
description: "Returns everything needed to construct a rule for a report: its alertable columns with their viewColumnIndex, the operator and rule-type catalogues each column permits, the chart thresholds on each column, and the view-level anomaly definitions."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts/metadata"
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - data-alerts
  - get
  - metadata
api:
  operation_id: getViewMetadataForAlert
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts/metadata"
  domain: schedules-and-alerts
  group: data-alerts
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the view's workspace, or hold the CREATEALERT (Manage Data Alerts) permission on that specific view."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 7319
    - 7387
    - 8060
    - 8083
    - 8245
    - 8535
  openapi:
    file: "/references/openapi/schedules-alerts-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1alerts~1metadata/get"
    config_schema: null
    response_schema: GetViewMetadataForAlertResponse
  sdk_examples: "/sdk-examples/schedules-and-alerts/data-alerts/get-view-metadata-for-alert.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/schedules-alerts-grouped-api.json"
    title: OpenAPI 3 specification - schedules-alerts-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T10:54:58Z
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts/metadata`** - Get View Metadata For Alert (Data Alerts / Schedules & Alerts).

Returns everything needed to construct a rule for a report: its alertable columns with their `viewColumnIndex`, the operator and rule-type catalogues each column permits, the chart thresholds on each column, and the view-level anomaly definitions. **This is the only source of `viewColumnIndex`** — call it before every [Create Alert](create-alert.md) or [Update Alert](update-alert.md).

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getViewMetadataForAlert` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts/metadata` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the view's workspace, or hold the CREATEALERT (Manage Data Alerts) permission on that specific view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`schedules-alerts-grouped-api.json`](../../../references/openapi/schedules-alerts-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1alerts~1metadata/get`; response schema `GetViewMetadataForAlertResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID, shown in the Zoho Analytics UI under Settings > Organisation. See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | `"Get view metadata for alert"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.viewType` | String | View type token — `AnalysisView`, `Pivot` or `SummaryView`. These are the internal type names, not the UI labels ("Chart View", "Pivot View", "Summary View"). Any other type is refused with `8245` before this response is built. |
| `data.viewColumns` | JSONArray | One entry per column of the view that can take part in an alert. **Always present.** |
| `viewColumns[].viewColumnIndex` | String | The positional index identifying this column in a write request (`rules[].viewColumnIndex`, `rowAxis`, `columnAxis`, and `values[0]` for `type: "column"`). **The only column identifier the Alert APIs accept** — see [The viewColumnIndex Contract](overview.md#the-viewcolumnindex-contract). |
| `viewColumns[].axis` | String | Axis the column occupies in the view — `X`, `Y`, and so on. |
| `viewColumns[].axisType` | String | Axis role — `XAXIS`, `YAXIS`, `COLOR`, `TOOLTIP`, … |
| `viewColumns[].axisDisplayName` | String | Display name of the column as the report shows it. Use this for a user-facing column picker. |
| `viewColumns[].operation` | String | Aggregation or date bucket applied to the column — `SUM`, `GROUP`, `YEAR`, `ABSQUARTER`, `ABSMONTH`, `ABSWEEK`, `DATE`, `TIMESTAMP`, `MEACATEGORY`, `GEO`, … It is what decides the date-bucket operators and, for the view's X axis, the contents of `allowedAnomalyOperators`. |
| `viewColumns[].dataType` | String | The column's **original** data type — `PLAIN`, `NUMBER`, `DATE`, `TIMESTAMP`, … Informative only: the operator catalogue is computed server-side from fields that are not all exposed here, so never derive operators from `dataType` yourself. |
| `viewColumns[].viewId` | String | Id of the view (or of the underlying table, for a base-layer column) the column belongs to. |
| `viewColumns[].formulaId` | String | Id of the backing formula when the column is a formula column; empty string otherwise. |
| `viewColumns[].geoRole` | Number | Geo role of the column. **Conditional** — present only for geo columns. Role `1` (geometry) narrows `allowedOperators` to `isn` / `notisn`. |
| `viewColumns[].thresholds` | JSONArray of String | Chart threshold **display names** configured on this column, sorted by their internal property order (`T1`, `T2`, …). `[]` when the column has none. A value from this array is what a `type: "threshold"` rule puts in `values[0]`. An empty array is also the reason `threshold` is absent from `allowedRuleTypes`. |
| `viewColumns[].allowedOperators` | JSONArray of String | Every `rules[].operator` token legal for this column, already narrowed by its data type, aggregation and geo role. **Treat it as the authoritative allow-list** — an operator outside it fails with `8119`. Token meanings: [Enum and Value Reference](overview.md#enum-and-value-reference). |
| `viewColumns[].allowedRuleTypes` | JSONArray of String | Which `rules[].type` values this column supports: `constant` always; `column` only when the view has **at least two** NUMBER columns and this column is one of them; `threshold` only when `thresholds` is non-empty. A type outside this list fails with `8119`. |
| `data.anomalies` | JSONArray | Anomaly definitions configured on the view. **Always present**; `[]` when the view has none, in which case anomaly alerts cannot be created on it. |
| `anomalies[].viewColumnIndex` | String | The column the anomaly is defined on. **Conditional** — omitted when the underlying column reference cannot be resolved to an index. |
| `anomalies[].anomalyName` | String | The name to send as `rules[].anomaly.name`. Must match exactly, otherwise `32000042`. |
| `data.allowedAnomalyOperators` | JSONArray of String | Operators legal for an anomaly rule on **this view** — a view-level property, not a per-column one. Derived from the X axis: a `YEAR` bucket yields the yearly tokens, `ABSMONTH` the monthly ones, `DATE` / `TIMESTAMP` the full day-level set. `["sinceLastAlert"]` when the view has anomalies but no date-bucketed X axis; `[]` when `anomalies` is empty. **Always present.** |

# Examples

## Sample Requests

**Case 1 — Chart report with thresholds and an anomaly definition**

```http
GET /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts/metadata HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Tabular report: a view type that cannot carry an alert (rejected)**

```http
GET /restapi/v2/workspaces/137687000271334001/views/137687000006991705/alerts/metadata HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — Chart with a dimension column, a measure column carrying two thresholds, and one anomaly**

```json
{
    "status": "success",
    "summary": "Get view metadata for alert",
    "data": {
        "viewType": "AnalysisView",
        "viewColumns": [
            {
                "viewColumnIndex": "1",
                "axis": "X",
                "axisType": "XAXIS",
                "axisDisplayName": "Region",
                "operation": "GROUP",
                "dataType": "PLAIN",
                "viewId": "137687000006991601",
                "formulaId": "",
                "thresholds": [],
                "allowedOperators": ["is", "isnot", "isn", "notisn"],
                "allowedRuleTypes": ["constant"]
            },
            {
                "viewColumnIndex": "2",
                "axis": "Y",
                "axisType": "YAXIS",
                "axisDisplayName": "Sales",
                "operation": "SUM",
                "dataType": "NUMBER",
                "viewId": "137687000006991601",
                "formulaId": "",
                "thresholds": ["T1", "T2"],
                "allowedOperators": ["is", "isnot", "gt", "lt", "gte", "lte", "btw", "notbtw", "isn", "notisn"],
                "allowedRuleTypes": ["constant", "column", "threshold"]
            },
            {
                "viewColumnIndex": "3",
                "axis": "Y",
                "axisType": "YAXIS",
                "axisDisplayName": "Profit",
                "operation": "SUM",
                "dataType": "NUMBER",
                "viewId": "137687000006991601",
                "formulaId": "",
                "thresholds": [],
                "allowedOperators": ["is", "isnot", "gt", "lt", "gte", "lte", "btw", "notbtw", "isn", "notisn"],
                "allowedRuleTypes": ["constant", "column"]
            }
        ],
        "anomalies": [
            {
                "viewColumnIndex": "2",
                "anomalyName": "Sales Spike"
            }
        ],
        "allowedAnomalyOperators": ["sinceLastAlert"]
    }
}
```

**HTTP 200 OK — Chart with no thresholds and no anomalies**

```json
{
    "status": "success",
    "summary": "Get view metadata for alert",
    "data": {
        "viewType": "AnalysisView",
        "viewColumns": [
            {
                "viewColumnIndex": "1",
                "axis": "X",
                "axisType": "XAXIS",
                "axisDisplayName": "Order Date",
                "operation": "ABSMONTH",
                "dataType": "DATE",
                "viewId": "137687000006991601",
                "formulaId": "",
                "thresholds": [],
                "allowedOperators": ["is", "isnot", "curMonth", "prevMonth", "prevNMonths", "lastNMonths", "nextMonth", "nextNMonths"],
                "allowedRuleTypes": ["constant"]
            }
        ],
        "anomalies": [],
        "allowedAnomalyOperators": []
    }
}
```

**HTTP 400 Bad Request — Failure paired with Case 2**

```json
{
    "status": "failure",
    "summary": "INVALID_VIEW_TYPE_FOR_OPERATION",
    "data": {
        "errorCode": 8245,
        "errorMessage": "Invalid view type. This operation can only be performed using the following view(s): Charts, Pivots, Summary Views"
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get View Metadata For Alert](../../../sdk-examples/schedules-and-alerts/data-alerts/get-view-metadata-for-alert.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **The only source of `viewColumnIndex`** | The Alert APIs never accept or return internal column ids, so a rule cannot be built correctly without this call. Full rules in [The viewColumnIndex Contract](overview.md#the-viewcolumnindex-contract). |
| **View type is checked first** | A view that is not `AnalysisView`, `Pivot` or `SummaryView` fails with `8245` before any column metadata is gathered. This is the cheapest way to test whether a report can carry an alert at all. |
| **`allowedOperators` and `allowedRuleTypes` are per column** | They mirror exactly what the alert dialog enables in the product UI. Picking from them is what avoids `8119` on the subsequent write. |
| **`allowedAnomalyOperators` is per view** | It depends only on the X axis's date bucket, so it is emitted once at the top level rather than per column. |
| **`anomalies` is surfaced once** | The underlying payload repeats the anomaly list on every column entry; this API hoists it to the top level. Do not look for it inside `viewColumns[]`. |
| **`thresholds` carries display names, not property names** | You send `"T1"`, not the internal `chart.threshold1`. The translation happens server-side on write and is reversed on [Get Alert Configuration](get-alert-configuration.md). |
| **It reads structure, not data** | No rows are scanned, so calling it before every write is cheap. |
| **No CONFIG, no paging** | Every alertable column of the view is returned in one response. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>` → Get View Metadata For Alert → `viewColumnIndex` / `thresholds` / `anomalyName` → [Create Alert](create-alert.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — View not found. | Verify `<view-id>` via [Get View List](../../views-management/view-operations/get-views.md). |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is neither the DB Owner nor a holder of `CREATEALERT` on this view, or the request arrived through a custom domain the workspace is not bound to. | Authenticate as the DB Owner or a user with Manage Data Alerts on that view, from the standard API host. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The view does not belong to the workspace in the URL. | Make `<workspace-id>` and `<view-id>` consistent. |
| [7387](../../../foundations/error-codes.md#error-7387) | 400 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not belong to the organisation in `ZANALYTICS-ORGID`. | Send the organisation id that owns the workspace. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use a domain you have purchased from Zoho Analytics, or the standard API host. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| [8245](../../../foundations/error-codes.md#error-8245) | 404 | `INVALID_VIEW_TYPE_FOR_OPERATION` — The view is not a Chart, Pivot Table or Summary View. | Alerts are supported only on those three report types; pick a different view. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Data Alerts overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Schedules & Alerts](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Alerts In Workspace](get-alerts-in-workspace.md), [Get Alerts In View](get-alerts-in-view.md), [Get Alert Configuration](get-alert-configuration.md), [Create Alert](create-alert.md), [Update Alert](update-alert.md), [Delete Alerts](delete-alerts.md), [Change Alert Status](change-alert-status.md), [Run Alert](run-alert.md), [Get Alert Events](get-alert-events.md).
- [SDK examples](../../../sdk-examples/schedules-and-alerts/data-alerts/get-view-metadata-for-alert.md).
