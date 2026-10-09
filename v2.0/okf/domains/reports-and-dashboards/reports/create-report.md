---
type: API Endpoint
title: Create Report
description: "Builds a new chart, pivot or summary view on an existing table and returns its view ID."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/reports"
tags:
  - zoho-analytics
  - rest-api-v2
  - reports-and-dashboards
  - reports
  - post
  - modeling
api:
  operation_id: createReport
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/reports"
  domain: reports-and-dashboards
  group: reports
  oauth_scopes:
    - ZohoAnalytics.modeling.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "Workspace Admin / Organization Admin, or a shared or group user holding Create Report permission on the base table."
  error_codes:
    - 7005
    - 7016
    - 7111
    - 7138
    - 7301
    - 7362
    - 7701
    - 7703
    - 7727
    - 8008
    - 8021
    - 8050
    - 8051
    - 8052
    - 8057
    - 8059
    - 8092
    - 8144
    - 8147
    - 8162
    - 8166
    - 8167
    - 8168
    - 8170
    - 8191
    - 8250
    - 8252
    - 8253
    - 8254
    - 8255
    - 8256
    - 8257
    - 8258
    - 8504
    - 8507
    - 8509
    - 8516
    - 8517
    - 8534
    - 8535
    - 8542
  openapi:
    file: "/references/openapi/reports-dashboards-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1reports/post"
    config_schema: CreateReportConfig
    response_schema: CreateReportResponse
  sdk_examples: "/sdk-examples/reports-and-dashboards/reports/create-report.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/reports`** - Create Report (Reports (Analysis Views) / Reports & Dashboards).

Builds a new chart, pivot or summary view on an existing table and returns its view ID.

From the OpenAPI specification:

Builds a new chart, pivot or summary view on an existing table and returns its view ID.

Permission required: Workspace Admin / Organization Admin, or a shared or group user holding Create Report permission on the base table.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createReport` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/reports` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | Workspace Admin / Organization Admin, or a shared or group user holding Create Report permission on the base table. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| Content-Type | `application/x-www-form-urlencoded` |
| Custom domain | Not permitted. |
| OpenAPI | [`reports-dashboards-grouped-api.json`](../../../references/openapi/reports-dashboards-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1reports/post`; CONFIG schema `CreateReportConfig`; response schema `CreateReportResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace in which the analysis view is created. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameter

`CONFIG` is a JSON object sent as a form-encoded body parameter. Maximum encoded size 10,000,000
characters.

| Field | Type | Mandatory | Constraints | Description |
|-------|------|-----------|-------------|-------------|
| `baseTableName` | String | **Yes** | 1–100 characters | Display name of the table, query table or pipeline table the report is built on. |
| `reportType` | String | **Yes** | `chart` \| `pivot` \| `summary` (lowercase) | The report family. |
| `axisColumns` | JSONArray | **Yes** | Max 1000 entries | The drop-field configuration. See [`axisColumns`](#axiscolumns). |
| `title` | String | No | Max 100 characters; unique within the workspace | Report name. Required in practice — omitting it creates an unnamed view and most callers will hit **7016** or **8051**. |
| `description` | String | No | Max 250 characters | Free-text description. |
| `folderId` | Long | No | Must exist in the workspace | Folder to create the report in. Omitted → the workspace's default folder. |
| `chartType` | String | Conditional | Letters, digits and spaces only; max 50 | Required in practice when `reportType` is `chart`. Matched case-insensitively. Omitted or unrecognisable-as-empty → the server picks `BEST`. Ignored for pivot and summary. See [Chart Types](overview.md#chart-types). |
| `isAxisMerge` | Boolean | No | `true` / `false` | Merge multiple Y axes onto one shared axis. |
| `mergeAxisInfo` | **JSONArray** | Conditional | Max 10 entries | Required when merging. Each entry is `{"axisIndex":[<int 0-100>, …], "labelName":"<max 250 chars>"}`. If this array is non-empty, `isAxisMerge` **must** be `true`. |
| `filters` | JSONArray | No | Max 1000 entries | Static filter criteria baked into the report. See [`filters`](#filters). |
| `userFilters` | JSONArray | No | Max 1000 entries | Interactive filter widgets shown to viewers. See [`userFilters`](#userfilters). |
| `settings` | JSONObject | No | **Pivot reports only** | Layout and theme settings. Supplying this for a chart or summary raises **8147**. See [`settings`](#settings-pivot-only). |
| `drillActionConfig` | JSONObject | No | Max 10 actions | Custom drill-through actions. See [`drillActionConfig`](#drillactionconfig). |
| `modifiedPaths` | JSONObject | No | — | Explicit join-path selection, used when two tables are reachable by more than one relationship path. Map of path key → array of view IDs. |

## Notes from the OpenAPI specification

This is a workspace-scoped API. The **ZANALYTICS-ORGID** header carrying the organization ID that owns the workspace is mandatory.

This API is not available on white-label / custom domains. Call the standard REST host for your data centre (**analyticsapi.zoho.com**, **analyticsapi.zoho.eu**, ...).

The CONFIG parameter must be sent as a URL encoded JSON string in a form field named **CONFIG**, with the content type **application/x-www-form-urlencoded**.

**chartType**, **isAxisMerge** and **mergeAxisInfo** apply only when **reportType** is chart. **mergeAxisInfo** is required when merging and **isAxisMerge** must be true whenever it is non-empty.

The CONFIG parameter has a maximum encoded size of 10,000,000 characters. Each of **axisColumns**, **filters** and **userFilters** holds at most 1000 entries (8052).

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Notes from the OpenAPI specification

Axis **type** values are returned in lowercase (**xaxis**, **yaxis**, **coloraxis**, **textaxis**, **groupby**, **tooltip**, **latlng**) whatever casing was sent; all of those are accepted on write. A **tooltip** column may be returned as **group**, which Create and Update reject with 8509.

# Examples

## Sample Requests

**Case 1 — Bar chart, region on X and summed sales on Y**

```http
POST /restapi/v2/workspaces/466206000000071000/reports HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
  "baseTableName": "Sales",
  "title": "Sales by Region",
  "reportType": "chart",
  "chartType": "bar",
  "axisColumns": [
    { "type": "xAxis", "columnName": "Region", "operation": "actual" },
    { "type": "yAxis", "columnName": "Sales",  "operation": "sum", "sort": "desc" }
  ]
}
```

**Case 2 — Chart with a static filter and a user filter**

```http
POST /restapi/v2/workspaces/466206000000071000/reports HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
  "baseTableName": "Sales",
  "title": "Sales Trend",
  "description": "Monthly trend, excluding returns",
  "folderId": 466206000000094005,
  "reportType": "chart",
  "chartType": "line",
  "axisColumns": [
    { "type": "xAxis", "columnName": "Order Date", "operation": "monthyear" },
    { "type": "yAxis", "columnName": "Sales", "operation": "sum" }
  ],
  "filters": [
    {
      "columnName": "Status", "tableName": "Sales",
      "operation": "actual", "filterType": "individualvalues",
      "values": ["Returned"], "exclude": true
    }
  ],
  "userFilters": [
    {
      "columnName": "Product Category", "tableName": "Sales",
      "operation": "actual", "compType": "multiSelect",
      "filterType": "individualvalues",
      "isallval": false,
      "values": ["Furniture", "Grocery"],
      "defaultFilterValues": ["Furniture"],
      "behaviour": "ListAllValues"
    }
  ]
}
```

**Case 3 — Pivot with a theme**

```
CONFIG={
  "baseTableName": "Sales",
  "title": "Sales Pivot",
  "reportType": "pivot",
  "axisColumns": [
    { "type": "row",    "columnName": "Region",     "operation": "actual" },
    { "type": "column", "columnName": "Order Date", "operation": "year"   },
    { "type": "data",   "columnName": "Sales",      "operation": "sum"    }
  ],
  "settings": { "themes": { "themeType": 3, "themeColor": "#2A6FDB", "themeFontSize": 12 } }
}
```

**Case 4 — Summary report**

```
CONFIG={
  "baseTableName": "Sales",
  "title": "Sales Summary",
  "reportType": "summary",
  "axisColumns": [
    { "type": "groupBy",   "columnName": "Region", "operation": "actual" },
    { "type": "summarize", "columnName": "Sales",  "operation": "sum"    },
    { "type": "summarize", "columnName": "Profit", "operation": "average" }
  ]
}
```

**Case 5 — Running total with a window function**

```
CONFIG={
  "baseTableName": "Sales",
  "title": "Cumulative Sales",
  "reportType": "chart",
  "chartType": "line",
  "axisColumns": [
    { "type": "xAxis", "columnName": "Order Date", "operation": "monthyear" },
    { "type": "yAxis", "columnName": "Sales", "operation": "sum",
      "windowFunction": { "type": "runtotal" } }
  ]
}
```

**Case 6 — Map chart with geo roles**

```
CONFIG={
  "baseTableName": "Sales",
  "title": "Sales by Country",
  "reportType": "chart",
  "chartType": "map area",
  "axisColumns": [
    { "type": "xAxis", "columnName": "Country", "operation": "geo", "geoRole": "country" },
    { "type": "yAxis", "columnName": "Sales",   "operation": "sum" }
  ]
}
```

**Case 7 — Wildcard filter**

```
CONFIG={
  "baseTableName": "Sales",
  "title": "Enterprise Accounts",
  "reportType": "chart",
  "chartType": "bar",
  "axisColumns": [
    { "type": "xAxis", "columnName": "Customer", "operation": "actual" },
    { "type": "yAxis", "columnName": "Sales", "operation": "sum" }
  ],
  "filters": [
    {
      "columnName": "Customer", "operation": "actual", "filterType": "wildcard",
      "exclude": false, "values": [],
      "wildcard": {
        "criteria": [
          { "operation": "CONTAINS",    "value": "Corp" },
          { "operation": "STARTS_WITH", "value": "Acme" }
        ],
        "expression": "(1 OR 2)"
      }
    }
  ]
}
```

## Sample Responses

**HTTP 200 OK**

The `summary` string varies with `reportType`: `Create Chart View`, `Create Pivot View` or
`Create Summary View`.

```json
{
  "status": "success",
  "summary": "Create Chart View",
  "data": {
    "viewId": "466206000000105001"
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Report](../../../sdk-examples/reports-and-dashboards/reports/create-report.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

## `axisColumns`

Each entry places one column on one shelf.

| Key | Type | Mandatory | Constraints | Description |
|-----|------|-----------|-------------|-------------|
| `type` | String | **Yes** | See [Axis Types](overview.md#axis-types) | Which shelf the column goes on. **Case-sensitivity matters** — see the appendix. |
| `columnName` | String | **Yes** | Max 1000 | Column display name. Matched case-insensitively. |
| `operation` | String | **Yes** | Letters only; see [Operations](overview.md#operations) | Aggregation or date-grouping applied to the column. |
| `tableName` | String | No | Max 100 | Table the column belongs to. Required when the column comes from a joined (lookup) table; may be omitted for base-table columns. |
| `columnId` | Long | No | — | Alternative to `columnName`. |
| `tableId` | Long | No | — | Alternative to `tableName`. |
| `displayName` | String | No | Max 250 | Override label for the column. |
| `sort` | String | No | `asc` \| `desc` | Sort direction for this shelf entry. |
| `rangeSize` | Double | No | JSON number | Bin width for `range` grouping on a numeric column. Must be a number, not a quoted string (**8162**) and not an array (**8516**). |
| `geoRole` | String | Conditional | See [Geo columns](#geo-columns) | Required when `operation` is `geo`. |
| `windowFunction` | JSONObject | No | See [Window functions](#window-functions) | Running / moving / difference calculation. |
| `format` | JSONObject | No | See below | Number, currency and date formatting for this column. |

**`format` sub-keys:** `displayName`, `type`, `currencyFormat`, `alignment`, `dateFormat`, `unitsList`,
`displayLabel` (strings); `thousandSeparator`, `decimalPlaces`, `decimalSeparator`, `numberingType`
(integers); `showSymbol`, `showNegativeSign`, `userLocale` (booleans).

### Window functions

| Sub-key | Type | Description |
|---------|------|-------------|
| `type` | String | The calculation. **Chart reports:** `normal`, `runtotal`, `pctoftotal`, `difffrom`, `pctdifffrom`, `pctofprevval`, `hundredpctgrp`, `movingcalc` (alias `movingcalculation`). **Pivot reports:** `normal`, `pctofrow`, `pctofcol`, `pctofparrow`, `pctofparcol`, `pctoftotal`, `runtotal`, `difffrom`, `pctdifffrom`, `pctofprevval`. |
| `baseField` | String | Reference column, required by `difffrom`, `pctdifffrom` and `movingcalc`. |
| `baseTable` | String | Table owning `baseField`. |
| `baseFieldPosition` | String | Shelf the reference field sits on, e.g. `xAxis`. |
| `baseFunction` | String | Operation applied to `baseField`. |
| `percentileVal` | Integer | 0–100; used with the `percentile` operation. |
| `movingCalculation` | JSONObject | Required when `type` is `movingcalc`. `{"calculation":"average"\|"sum"\|"min"\|"max", "previous":<int>, "next":<int>, "includeCurrent":<bool>, "includeNull":<bool>}`. |

> `pctoftotal` is not available on columns whose `operation` is `average`, `stddev`, `variance`, `dc` or
> `distinctcount`.

> Window functions apply to measure columns. They are not available on a date column unless its
> operation is `count`, and not on numeric columns bucketed with `dimension` or `range`.

### Geo columns

Set `operation` to `geo` and supply `geoRole`:

| Column type | Valid `geoRole` values | Placement |
|---|---|---|
| Plain text / categorical | `continent`, `country`, `state`, `province`, `county`, `district`, `city`, `zipcode`, `airport` | **X axis only** (**8258** otherwise) |
| Numeric | `latitude`, `longitude` | X or Y axis |

Limits, each enforced with its own error:

- At most **one** categorical geo column on the X axis (**8256**).
- At most **one** numeric geo column per axis (**8256**).
- A categorical geo on X and a numeric geo on Y cannot coexist (**8257**).
- `latitude` / `longitude` on a text column, or a place role on a numeric column, raises **8254**.
- `geoRole` on a column that cannot be geocoded raises **8255**.

## `filters`

Static criteria applied every time the report renders. Viewers cannot change them.

| Key | Type | Mandatory | Description |
|-----|------|-----------|-------------|
| `columnName` | String | **Yes** | Column to filter on. |
| `operation` | String | **Yes** | How the column is interpreted before the criteria is applied. See [Filter Operations and Types](overview.md#filter-operations-and-types). |
| `filterType` | String | **Yes** | Shape of the criteria. See [Filter Operations and Types](overview.md#filter-operations-and-types). |
| `values` | JSONArray | **Yes** | Criteria values, as strings. Format depends on `filterType` — see [Filter Value Formats](overview.md#filter-value-formats). |
| `exclude` | Boolean | **Yes** | `true` excludes the listed values, `false` includes them. Must be a JSON boolean. |
| `tableName` | String | No | Table owning the column; needed for joined-table columns. |
| `columnId` / `tableId` | Long | No | ID-based alternatives to the name keys. |
| `rankingColumn` | String | No | Measure column that drives the rank, for `ranking` / `rankingpct`. |
| `rankingColumnDateSubType` | String | No | Date sub-type of the ranking column. |
| `wildcard` | JSONObject | Conditional | Required when `filterType` is `wildcard`. See below. |
| `additionalDetails` | JSONObject | No | `{"type":"userFilter"\|"timeLineFilter"\|"drillThrough"\|"reportAsFilter", "label":"…", "isFromDashboard":<bool>, "fromViewId":<long>}`. |

**`wildcard`:**

| Sub-key | Type | Description |
|---|---|---|
| `criteria` | JSONArray | Up to 15 entries. Each is `{"operation": …, "value": "<max 5000 chars>"}` with `operation` one of `CONTAINS`, `DOES_NOT_CONTAIN`, `IS`, `IS_NOT`, `STARTS_WITH`, `DOES_NOT_START_WITH`, `ENDS_WITH`, `DOES_NOT_END_WITH`. |
| `expression` | String | How the criteria combine, referenced by 1-based index. **The expression must be wrapped in parentheses**: `"(1 AND 2 OR 3)"`. Without the parentheses it is rejected with **8509**. Max 100 characters. |

## `userFilters`

Interactive filter widgets rendered alongside the report.

| Key | Type | Mandatory | Description |
|-----|------|-----------|-------------|
| `columnName` | String | **Yes** | Column to expose. Matched case-insensitively. |
| `operation` | String | Conditional | Mandatory for date and numeric columns; ignored for text columns, which are always `actual`. Dates: `actual`, `seasonal`, `relative`, `range`, `daterange`. Numerics: `sum`, `min`, `max`, `average`, `stddev`, `std`, `count`, `variance`, `dc`, `distinctcount`, `median`, `mode`, `measure`, `dimension`, `actual`, `aggregate`. |
| `compType` | String | Conditional | Widget type: `singleSelect`, `multiSelect`, `slider`, `dateRange`. `slider` is measure-only; `singleSelect` / `multiSelect` are for dimensions and dates. A mismatch raises **8250**; a missing required `compType` raises **8253**. |
| `filterType` | String | Conditional | Criteria shape. Required for measures and for date `actual` / `seasonal` operations. See [Filter Operations and Types](overview.md#filter-operations-and-types). |
| `isallval` | Boolean | No | Whether the filter defaults to "all values". See the resolution rule below. |
| `values` | JSONArray | Conditional | Selectable / preselected values. Required when `isallval` is `false`. |
| `defaultFilterValues` | JSONArray | No | Values preselected on load. Must be a subset of `values`. |
| `exclude` | Boolean | No | Defaults to `false`. Not allowed with the `daterange` operation. |
| `behaviour` | String | No | `ListAllValues`, `ListRelevantValues`, `ListOnlyRelevantValues`. **Not applicable** to `daterange` or `relative` operations — supplying it there raises **8008**. |
| `tableName` | String | No | Table owning the column. Resolved from the join graph when omitted. |

> **`isallval` resolution.** If `isallval` is omitted, the server derives it from `values`: a non-empty
> `values` array implies `isallval: false`, an absent or empty one implies `isallval: true`. When you send
> `isallval: true` *and* a non-empty `values` array, `isallval` wins and the values are ignored.

> **Numeric criteria must be exact.** Values are compared as stored, not rounded. If the stored value is
> `0.89123`, the filter value must be `0.89123`; `0.9` will not match.

## `settings` (pivot only)

```json
{
  "layout": { "defaultWidth": 120 },
  "themes": {
    "compactIndent": 1,
    "themeType": 3,
    "themeColor": "#2A6FDB",
    "themeFontSize": 12,
    "themeRowSpacing": 2,
    "fontColor": "#1A1A1A"
  }
}
```

| Key | Range |
|---|---|
| `layout.defaultWidth` | 1–1000 |
| `themes.compactIndent` | 0–3 |
| `themes.themeType` | 1–7 |
| `themes.themeFontSize` | 5–24 |
| `themes.themeRowSpacing` | 1–3 |
| `themes.themeColor`, `themes.fontColor` | `#RRGGBB` or `#RGB` |

Supplying `settings` on a `chart` or `summary` report raises **8147**.

## `drillActionConfig`

Create only — this key is not accepted on Update.

```json
{
  "drillActionsConfig": [
    {
      "id": "1",
      "name": "Open in CRM",
      "urlString": "https://crm.example.com/deal",
      "methodType": "GET",
      "params": [{ "key": "region", "value": "${Region}" }],
      "headers": [],
      "formData": [],
      "body": "",
      "bodyType": "none"
    }
  ]
}
```

Up to 10 actions. `name` max 50 characters, `urlString` max 2000, `body` max 50,000.

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | A `null` element inside `axisColumns` or `filters`. | Ensure every array element is a JSON object. |
| [7016](../../../foundations/error-codes.md#error-7016) | 400 | `title` is empty or whitespace-only. | Supply a non-empty title. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | A view with this `title` already exists in the workspace. | Choose a unique title. |
| [7138](../../../foundations/error-codes.md#error-7138) | 400 | `baseTableName` does not resolve to a table in this workspace. | Use the exact table display name. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The caller lacks Create Report permission on the workspace. | Grant the permission. |
| [7362](../../../foundations/error-codes.md#error-7362) | 400 | `folderId` does not exist in the workspace. | Supply a valid folder ID or omit the key. |
| [7701](../../../foundations/error-codes.md#error-7701) | 400 | A chart report has no X-axis or no Y-axis column. | Add at least one of each. |
| [7703](../../../foundations/error-codes.md#error-7703) | 400 | A `colorAxis` column is present alongside more than one Y-axis column. | Drop the colour axis, or reduce to one Y axis. |
| [7727](../../../foundations/error-codes.md#error-7727) | 400 | More than 15 Y-axis columns on a chart. | Reduce to 15 or fewer. |
| [8008](../../../foundations/error-codes.md#error-8008) | 400 | `behaviour` was supplied on a `daterange` or `relative` user filter. | Remove `behaviour`. |
| [8021](../../../foundations/error-codes.md#error-8021) | 400 | The pivot or summary structure is invalid — no `data` column in a pivot, too many `data` or `groupBy` columns, or a column in a position its type cannot occupy. On **Update**, also raised when `reportType` does not match the stored view's type. | Review the axis configuration. |
| [8050](../../../foundations/error-codes.md#error-8050) | 400 | A value is invalid — unknown `columnName`, an operation incompatible with the column, a `null` `axisColumns`. | Check column names and operations. |
| [8051](../../../foundations/error-codes.md#error-8051) | 400 | A required field is missing — `title`, `reportType`, `axisColumns`, or a mandatory key inside an axis/filter object. | Add the missing field. |
| [8052](../../../foundations/error-codes.md#error-8052) | 400 | More than 1000 entries in `axisColumns`, `filters` or `userFilters`. | Reduce the array size. |
| [8057](../../../foundations/error-codes.md#error-8057) | 400 | The column named in `windowFunction.baseField` cannot be used as a base field here. | Choose a different reference column. |
| [8059](../../../foundations/error-codes.md#error-8059) | 400 | The `tableName` is not part of the workspace or is not joined to the base table. | Use a table reachable through the join graph. |
| [8092](../../../foundations/error-codes.md#error-8092) | 400 | `reportType` resolves to a view kind that cannot be saved standalone. | Use `chart`, `pivot` or `summary`. |
| [8144](../../../foundations/error-codes.md#error-8144) | 400 | `chartType` is not a recognised chart name. | See [Chart Types](overview.md#chart-types). |
| [8147](../../../foundations/error-codes.md#error-8147) | 400 | `settings` was supplied for a non-pivot report. | Remove `settings`, or change `reportType` to `pivot`. |
| [8162](../../../foundations/error-codes.md#error-8162) | 400 | `rangeSize` was supplied as a string, or on an operation that does not support ranges. | Send a JSON number, and only with `range` grouping. |
| [8166](../../../foundations/error-codes.md#error-8166) | 400 | The `operation` is incompatible with the column's data type. | See [Operations](overview.md#operations). |
| [8167](../../../foundations/error-codes.md#error-8167) | 400 | The `filterType` is not valid for the column type + `operation` combination. | See [Filter Operations and Types](overview.md#filter-operations-and-types). |
| [8168](../../../foundations/error-codes.md#error-8168) | 400 | A `values` entry does not match the expected format for the `filterType`. | See [Filter Value Formats](overview.md#filter-value-formats). |
| [8170](../../../foundations/error-codes.md#error-8170) | 400 | An axis `type` is not valid for the chosen `reportType`. | See [Axis Types](overview.md#axis-types). |
| [8191](../../../foundations/error-codes.md#error-8191) | 400 | An invalid date value was supplied to a date filter. | Use the documented date formats. |
| [8250](../../../foundations/error-codes.md#error-8250) | 400 | `compType` is not applicable to the column category — e.g. `slider` on a dimension, `singleSelect` on a measure. | Match the widget to the column type. |
| [8252](../../../foundations/error-codes.md#error-8252) | 400 | `reportType` is absent or `null`. | Supply `chart`, `pivot` or `summary`. |
| [8253](../../../foundations/error-codes.md#error-8253) | 400 | A mandatory `userFilters` key is missing, typically `compType` or `filterType`. | Add the missing key. |
| [8254](../../../foundations/error-codes.md#error-8254) | 400 | A `geoRole` value is wrong for the column type. | `latitude`/`longitude` for numeric columns; place roles for text columns. |
| [8255](../../../foundations/error-codes.md#error-8255) | 400 | `geoRole` was supplied on a column that cannot be geocoded. | Remove `geoRole`, or use a geocodable column. |
| [8256](../../../foundations/error-codes.md#error-8256) | 400 | More than one geo operation on the same axis. | Keep one geo column per axis. |
| [8257](../../../foundations/error-codes.md#error-8257) | 400 | A numeric geo column coexists with a categorical geo column. | Use one or the other. |
| [8258](../../../foundations/error-codes.md#error-8258) | 400 | A categorical geo column was placed on an axis other than X. | Move it to `xAxis`. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `baseTableName` is absent, or the `CONFIG` parameter itself is missing. | Send `CONFIG` with `baseTableName`. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | `title` exceeds 100 characters, `description` exceeds 250, or an axis `displayName` exceeds 250. | Shorten the value. |
| [8509](../../../foundations/error-codes.md#error-8509) | 400 | An enumerated or pattern-constrained value does not match — `reportType: "Chart"` (must be lowercase), `type: "sizeAxis"` (must be `sizeaxis`), `sort: "descending"`, a wildcard `expression` without parentheses. | Use the exact accepted values. |
| [8516](../../../foundations/error-codes.md#error-8516) | 400 | `rangeSize` was supplied as an array. | Send a plain number. |
| [8517](../../../foundations/error-codes.md#error-8517) | 400 | A field has the wrong JSON data type — `exclude: "yes"`, `isAxisMerge: "maybe"`, `compType: 123`. | Use real JSON booleans and strings. |
| [8534](../../../foundations/error-codes.md#error-8534) | 400 | `CONFIG` is malformed, or a key has the wrong structural type — `axisColumns` as `{}`, `mergeAxisInfo` as an object, `values` as a bare string. | Arrays must be `[]`, objects `{}`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Refresh with scope `ZohoAnalytics.modeling.create`. |
| [8542](../../../foundations/error-codes.md#error-8542) | 400 | An unknown key is present in `CONFIG`, or a `windowFunction` is mis-configured. | Remove the key; check `windowFunction.type` against [the list](#window-functions). |

# Related

- [Reports (Analysis Views) overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Reports & Dashboards](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Read Report Metadata](get-report-metadata.md), [Update Report](update-report.md).
- [SDK examples](../../../sdk-examples/reports-and-dashboards/reports/create-report.md).
