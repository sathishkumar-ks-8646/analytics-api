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
  api_units:
    api_id: 2031
    action: CREATE_ANALYSISVIEW
    category: METADATA
    units: 5
    units_basis: per_request
    units_note: "5 units per request"
    category_frequency_limit: 60 requests/minute
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
  permission_required: "Account Admin, Organization Admin, Workspace Owner or Workspace Admin; a Custom Role user whose role grants Create Report on the base table; or a shared / group user holding Create Report permission. The caller must additionally be able to read the base table and every column the report uses. See Permission Model."
  error_codes:
    - 7016
    - 7103
    - 7111
    - 7137
    - 7138
    - 7301
    - 7309
    - 7324
    - 7362
    - 7701
    - 7703
    - 7705
    - 7706
    - 7725
    - 7727
    - 8008
    - 8050
    - 8051
    - 8052
    - 8053
    - 8055
    - 8056
    - 8057
    - 8058
    - 8059
    - 8144
    - 8162
    - 8164
    - 8166
    - 8167
    - 8168
    - 8169
    - 8170
    - 8179
    - 8187
    - 8188
    - 8201
    - 8250
    - 8251
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
    - 8544
    - 8547
    - 14037
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
    last_modified: 2026-10-26T11:33:28Z
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/reports`** - Create Report (Reports (Analysis Views) / Reports & Dashboards).

Builds a new chart, pivot or summary view on an existing table and returns its view ID. Use the
returned `viewId` as `<report-id>` in [Read Report Metadata](get-report-metadata.md) and
[Update Report](update-report.md).

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createReport` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/reports` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | Account Admin, Organization Admin, Workspace Owner or Workspace Admin; a Custom Role user whose role grants Create Report on the base table; or a shared / group user holding Create Report permission. The caller must additionally be able to read the base table and every column the report uses. See Permission Model. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| API units | 5 units per request - action `CREATE_ANALYSISVIEW` (api-id `2031`), **METADATA** category. See [API units](../../../foundations/api-units.md). |
| Frequency limit | 60 requests/minute across all **METADATA**-category calls of the organization. See [API units](../../../foundations/api-units.md#unit-categories-and-frequency-limits). |
| OpenAPI | [`reports-dashboards-grouped-api.json`](../../../references/openapi/reports-dashboards-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1reports/post`; CONFIG schema `CreateReportConfig`; response schema `CreateReportResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID, shown in the Zoho Analytics UI under Settings > Organisation. See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace in which the analysis view is created. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

CONFIG is **mandatory** for this API. It is sent as a form-encoded body parameter; maximum encoded size
10,000,000 characters.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `baseTableName` | String | **Yes** | — | Display name of the table or query table the report is built on, 1–100 characters. Matched **exactly and case-sensitively** (`7138` otherwise; `7137` when the name is not a table or query table). **Cannot be changed after creation.** |
| `title` | String | **Yes** | — | Report name, 1–100 characters (`8507` above 100). Leading and trailing spaces are trimmed. Whitespace-only raises `7016`. Must not match the name of any other object in the workspace — table, query table, report or dashboard (`7111`). Can be changed later with [Update Report](update-report.md). |
| `reportType` | String (enum) | **Yes** | — | The report family, lowercase only (`8509` otherwise). **Cannot be changed after creation.** See [`reportType` Values](#reporttype-values). |
| `axisColumns` | JSONArray | **Yes** | — | The drop-field configuration, 1–1000 entries (`8052` above 1000). See [`axisColumns` Fields](#axiscolumns-fields). |
| `description` | String | No | — | Free-text description, max 250 characters. Stored as sent. |
| `folderId` | Long | No | The workspace's default folder | Folder to create the report in. Must be a folder of this workspace (`7362`). **Ignored** for shared / group users — see [Permission Model](overview.md#permission-model). **Cannot be changed later** through these APIs. |
| `chartType` | String (enum) | No | Chosen automatically | Applies to `chart` only. Matched case-insensitively; letters, digits and spaces only, max 50 characters. An unrecognised value raises `8144`. For `pivot` and `summary`, omit it: a valid value is ignored, an unrecognised value still raises `8144`. The 57 accepted values are listed in [`chartType` Values](overview.md#charttype-values) (Appendix E). |
| `isAxisMerge` | Boolean | No | `false` | Charts only. Merge Y-axis columns onto shared axes. Must be `true` whenever `mergeAxisInfo` contains an entry (`8050`). |
| `mergeAxisInfo` | JSONArray | No | — | Charts only. Up to 10 groups of Y-axis columns that share one axis. See [`mergeAxisInfo` Fields](#mergeaxisinfo-fields). |
| `filters` | JSONArray | No | — | Static filter criteria baked into the report, 0–1000 entries. See [`filters` Fields](#filters-fields). |
| `userFilters` | JSONArray | No | — | Interactive filter widgets shown to viewers, 0–1000 entries. See [`userFilters` Fields](#userfilters-fields). |

> **`chartType` is not checked against the shelves.** The server does not reject a chart type that
> cannot be drawn from the supplied `axisColumns`; the type is saved as sent and the renderer falls back
> to a compatible chart when the report is opened. Choose a chart type whose shelves your `axisColumns`
> fill.

### `reportType` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `chart` | A chart. | Needs a shelf combination that forms a drawable chart — at minimum one X-axis and one Y-axis column for most chart types (`7701`). |
| `pivot` | A pivot table. | Needs at least one `row`, `column` or `data` column (`7706`). |
| `summary` | A summary view. | Needs at least one `groupBy` or `summarize` column (`7705`). |

### `axisColumns` Fields

Each entry places one column on one shelf.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `type` | String (enum) | **Yes** | — | The shelf. Only the exact spellings in [Axis Type Values](overview.md#axis-type-values) are accepted (`8509`); a valid spelling used with the wrong `reportType` raises `8170`. |
| `columnName` | String | **Yes** | — | Column display name, max 1000 characters. Matched **case-insensitively**. An unknown name raises `8050`. |
| `operation` | String (enum) | **Yes** for table columns | — | Aggregation or date grouping, letters only, matched case-insensitively. Ignored for aggregate formula columns. See [Axis Operation Values](overview.md#axis-operation-values) (`8166` for an operation not valid for the column and shelf). |
| `tableName` | String | No* | Base table | Display name of the table owning the column, max 100 characters, matched **exactly**. A table not joined to the base table raises `8059`. |
| `displayName` | String | No | — | Max 250 characters. Chart: the axis label shown for this column. Pivot / summary: the column header. |
| `sort` | String (enum) | No | — | `asc` or `desc`, lowercase (`8509` otherwise). **Chart and summary:** only the first entry in `axisColumns` that carries `sort` is applied; later `sort` keys are ignored. **Pivot:** applied on every entry that carries it. |
| `rangeSize` | Number | No* | — | Bin width, a JSON number greater than `0`. Allowed only when `operation` is `range` on a Numeric column (`8162` otherwise). |
| `geoRole` | String (enum) | No* | — | Geographic role, used with `operation: "geo"`. See [Geo Role Values](overview.md#geo-role-values). |
| `windowFunction` | JSONObject | No | — | Max 1000 characters. Running total, percentage, difference or moving calculation on a measure. See [`windowFunction` Fields](#windowfunction-fields). |

\* `tableName` is required when the column belongs to a table joined to the base table. `rangeSize`
applies only to `range`. `geoRole` is required when `operation` is `geo` on a Plain Text or Number
column.

### `windowFunction` Fields

A window function can be attached to an `axisColumns` entry that holds a **measure**:

| Report | Entries that accept `windowFunction` |
|---|---|
| `chart` | Numeric column with any operation except `dimension` and `range`; Text column with `count`, `dc` or `distinctcount`; Date column with `count`, `distinctcount` or a date distinct-count variant; numeric aggregate formula column. |
| `pivot` | An entry on the `data` shelf holding a Numeric column, a Text column, a Date column with `count`, or a numeric aggregate formula column. |
| `summary` | None. `windowFunction` is ignored. |

On any other entry, `windowFunction` is ignored.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `type` | String (enum) | **Yes** | — | The calculation, matched case-insensitively (`8169` otherwise). See [Window Function Type Values](overview.md#window-function-type-values). |
| `baseField` | String | No* | — | Name of the reference column. Required by every type marked *Needs base field* (`8253`). See [Base Field Rules](#base-field-rules). |
| `baseFieldPosition` | String (enum) | No* | — | Shelf of `baseField` in this report, matched case-insensitively. Required whenever `baseField` is required (`8051`). Chart: `xAxis`, `yAxis`, `colorAxis`, `textAxis`, `latLng`, `toolTip`, `sizeaxis`. Pivot: `row`, `column`, `data`. |
| `baseTable` | String | No | Table of the measure column | Table owning `baseField`. See [Base Field Rules](#base-field-rules). |
| `baseFunction` | String | No | — | `operation` of the `baseField` entry. See [Base Field Rules](#base-field-rules). |
| `percentileVal` | Integer | No | `50` | 0–100 (`8544` otherwise). Used only when the entry's `operation` is `percentile`. |
| `movingCalculation` | JSONObject | No* | — | Required when `type` is `movingcalc` (`8051`). See [`movingCalculation` Fields](#movingcalculation-fields). |

\* `baseField` and `baseFieldPosition` are required for `runtotal`, `difffrom`, `pctofprevval`,
`pctdifffrom`, `hundredpctgrp` and `movingcalc`. `movingCalculation` is required for `movingcalc`.

### `movingCalculation` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `calculation` | String (enum) | **Yes** | — | `average`, `sum`, `min` or `max`, case-insensitive (`8169` otherwise). |
| `previous` | Integer | **Yes** | — | Number of preceding values in the window. |
| `next` | Integer | **Yes** | — | Number of following values in the window. |
| `includeCurrent` | Boolean | **Yes** | — | Include the current value in the window. |
| `includeNull` | Boolean | **Yes** | — | Include null values in the window. |

#### Base Field Rules

- The base field must itself be an entry in `axisColumns`, placed on the shelf named by
  `baseFieldPosition`, and it must be a **dimension**:
  - Chart: a Text column with `operation` `actual` or `geo`, or a Date column with a grouping
    operation (not `count` or a distinct count).
  - Pivot: any entry on the `row` or `column` shelf.
- A base field that is not a dimension entry in `axisColumns` raises [`8057`](../../../foundations/error-codes.md#error-8057); one placed on a different
  shelf from `baseFieldPosition` raises [`8058`](../../../foundations/error-codes.md#error-8058).
- When `baseTable` is omitted, `baseField` is looked up in the same table as the measure column.
- When **all four** of `baseField`, `baseTable`, `baseFieldPosition` and `baseFunction` are supplied,
  the base field is located by matching an `axisColumns` entry whose `tableName`, `columnName`,
  `operation` and `type` equal `baseTable`, `baseField`, `baseFunction` and `baseFieldPosition`
  **exactly** (case-sensitive). Every `axisColumns` entry up to and including the matching one must
  carry both `tableName` and `operation`; if an earlier entry lacks either, or no entry matches, the call
  fails with [`8051`](../../../foundations/error-codes.md#error-8051).

### `mergeAxisInfo` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `axisIndex` | JSONArray of Integer | **Yes** | — | **1-based positions in the `axisColumns` array** of the columns to merge (the first entry of `axisColumns` is `1`). Each value 0–100. An empty array makes the entry a no-op. |
| `labelName` | String | No | — | Max 250 characters. Label of the merged axis. |

Every position must point at an entry whose `type` is a Y axis (`yaxis`, `yAxis`, `YAxis`); every column
in one group must be a measure — a Numeric column with an aggregate operation, or a `count` / distinct
count of any column — and all columns in a group must be of the same kind. Each violation raises
[`8050`](../../../foundations/error-codes.md#error-8050).

### `filters` Fields

Static criteria applied every time the report renders. Viewers cannot change them.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `columnName` | String | **Yes** | — | Column to filter on, max 1000 characters, matched case-insensitively. |
| `operation` | String (enum) | **Yes** | — | How the column is interpreted before the criteria is applied. See [Static Filter Operation and Type Values](overview.md#static-filter-operation-and-type-values). Required even for aggregate formula columns (send `aggregate`). |
| `filterType` | String (enum) | **Yes** | — | Shape of the criteria. See [Static Filter Operation and Type Values](overview.md#static-filter-operation-and-type-values). Required even where its value is not used (`relative` date filters — send `common`). |
| `values` | JSONArray of String | **Yes** | — | Criteria values. Format depends on `filterType` — see [Filter Value Formats](overview.md#filter-value-formats). Serialised array limited to 1,000 characters. Send `[]` for `wildcard` filters. |
| `exclude` | Boolean | **Yes** | — | `true` excludes the listed values, `false` includes them. Must be a JSON boolean. |
| `tableName` | String | No* | Base table | Table owning the column, max 1000 characters, matched exactly. A table not joined to the base table raises `8059`. |
| `rankingColumn` | String | No | — | Used only with `filterType: "ranking"` on a Numeric column: the Text or Date column (in the same table) whose members are ranked by the filtered measure. A Numeric ranking column raises `8055`. |
| `rankingColumnDateSubType` | String (enum) | No | `year` | Used only when `rankingColumn` is a Date column: `year`, `quarter`, `month`, `week`, `date` or `datetime`. |
| `wildcard` | JSONObject | No* | — | Required when `filterType` is `wildcard` (`8051`). See [`wildcard` Fields](#wildcard-fields). |

\* `tableName` is required for columns of joined tables. `wildcard` is required for `filterType:
"wildcard"`.

### `wildcard` Fields

Text columns with `operation: "actual"` only. **Create only** — Update rejects wildcard filters with
[`8192`](../../../foundations/error-codes.md#error-8192).

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `criteria` | JSONArray | **Yes** | — | 1–15 entries (`8179` when empty). Each is `{"operation": "<op>", "value": "<text>"}`, both keys mandatory; `value` max 5,000 characters. See [Wildcard Operation Values](overview.md#wildcard-operation-values). |
| `expression` | String | **Yes** | — | How the criteria combine, max 100 characters. Must match the pattern `^\(\s*(\d+\s*(OR\|AND)\s*)*\d+\s*\)$` (`8509` otherwise): wrapped in one pair of parentheses, criteria referenced by 1-based index, each index used exactly once, in ascending order, for example `"(1 AND 2 OR 3)"`. Indexes out of order raise `8187`; an index count different from the criteria count raises `8188`. |

### `userFilters` Fields

Interactive filter widgets rendered alongside the report. The rules depend on the column category and,
for dates, on `operation` — see [User Filter Rules by Column](overview.md#user-filter-rules-by-column).

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `columnName` | String | **Yes** | — | Column to expose, max 1000 characters, matched case-insensitively. |
| `tableName` | String | No* | Base table | Table owning the column, matched exactly. A table not joined to the base table raises `8059`. |
| `operation` | String (enum) | Conditional | — | See [User Filter Rules by Column](overview.md#user-filter-rules-by-column). |
| `compType` | String (enum) | Conditional | — | Widget type: `singleSelect`, `multiSelect`, `slider` or `dateRange`, exact case (`8509` otherwise). A missing required `compType` raises `8253`; a `compType` not valid for the column raises `8250`. |
| `filterType` | String (enum) | Conditional | — | Criteria shape. See [User Filter Rules by Column](overview.md#user-filter-rules-by-column). |
| `isallval` | Boolean | No | Derived from `values` | `true`: the widget lists all values and `values` is ignored. `false`: the widget is restricted to `values`, which must be non-empty (`8050`). Omitted: `false` when `values` is non-empty, `true` otherwise. |
| `values` | JSONArray of String | Conditional | — | Selectable values. Required when `isallval` is `false`. Serialised array limited to 1,000 characters. |
| `defaultFilterValues` | JSONArray of String | No | — | Values pre-selected when the report opens. At most 1 value unless `compType` is `multiSelect` (`8166`). Validated with the same rules as `values`; need not be a subset of `values`. May not contain `Others` or more than one `${...}` variable (`8166`). A range-picker default may also be `"from <date>"` or `"to <date>"`. |
| `exclude` | Boolean | No | `false` | `true` makes the widget exclude the selected values. Not allowed on a range picker (`8050`). |
| `behaviour` | String (enum) | No | — | Which values the widget lists when other filters are applied: `ListAllValues`, `ListRelevantValues` or `ListOnlyRelevantValues`, exact case. Not allowed on `slider`, `dateRange` or `relative` user filters (`8008`). |

\* `tableName` is required for columns of joined tables.

## Notes from the OpenAPI specification

This is a workspace-scoped API. The **ZANALYTICS-ORGID** header carrying the organization ID that owns the workspace is mandatory.

This API is not available on white-label / custom domains. Call the standard REST host for your data centre (**analyticsapi.zoho.com**, **analyticsapi.zoho.eu**, ...).

The CONFIG parameter must be sent as a URL encoded JSON string in a form field named **CONFIG**, with the content type **application/x-www-form-urlencoded**.

**chartType**, **isAxisMerge** and **mergeAxisInfo** apply only when **reportType** is chart. **mergeAxisInfo** is required when merging and **isAxisMerge** must be true whenever it is non-empty.

The CONFIG parameter has a maximum encoded size of 10,000,000 characters. Each of **axisColumns**, **filters** and **userFilters** holds at most 1000 entries (8052).

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary: `"Create Chart View"`, `"Create Pivot View"` or `"Create Summary View"`, by `reportType`. |
| `data` | JSONObject | Response payload wrapper. |
| `data.viewId` | String | ID of the new report, serialised as a **string**. **Always present** on success. Use it as `<report-id>`. |

## Notes from the OpenAPI specification

Axis **type** values are returned in lowercase (**xaxis**, **yaxis**, **coloraxis**, **textaxis**, **groupby**, **tooltip**, **latlng**) whatever casing was sent; all of those are accepted on write. A **tooltip** column may be returned as **group**, which Create and Update reject with 8509.

# Examples

## Sample Requests

**Case 1 — Bar chart, region on X and summed sales on Y (minimal)**

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
        {"type": "xAxis", "columnName": "Region", "operation": "actual"},
        {"type": "yAxis", "columnName": "Sales", "operation": "sum", "sort": "desc"}
    ]
}
```

**Case 2 — Line chart in a folder, with a static filter and a user filter**

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
        {"type": "xAxis", "columnName": "Order Date", "operation": "monthyear"},
        {"type": "yAxis", "columnName": "Sales", "operation": "sum"}
    ],
    "filters": [
        {
            "columnName": "Status",
            "tableName": "Sales",
            "operation": "actual",
            "filterType": "individualvalues",
            "values": ["Returned"],
            "exclude": true
        }
    ],
    "userFilters": [
        {
            "columnName": "Product Category",
            "tableName": "Sales",
            "operation": "actual",
            "compType": "multiSelect",
            "filterType": "individualvalues",
            "isallval": false,
            "values": ["Furniture", "Grocery"],
            "defaultFilterValues": ["Furniture"],
            "behaviour": "ListAllValues"
        }
    ]
}
```

**Case 3 — Pivot**

```http
POST /restapi/v2/workspaces/466206000000071000/reports HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "baseTableName": "Sales",
    "title": "Sales Pivot",
    "reportType": "pivot",
    "axisColumns": [
        {"type": "row", "columnName": "Region", "operation": "actual"},
        {"type": "column", "columnName": "Order Date", "operation": "year"},
        {"type": "data", "columnName": "Sales", "operation": "sum"}
    ]
}
```

**Case 4 — Summary report**

```http
POST /restapi/v2/workspaces/466206000000071000/reports HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "baseTableName": "Sales",
    "title": "Sales Summary",
    "reportType": "summary",
    "axisColumns": [
        {"type": "groupBy", "columnName": "Region", "operation": "actual"},
        {"type": "summarize", "columnName": "Sales", "operation": "sum"},
        {"type": "summarize", "columnName": "Profit", "operation": "average"}
    ]
}
```

**Case 5 — Running total with a window function**

`runtotal` needs a base field: the dimension along which the total accumulates.

```http
POST /restapi/v2/workspaces/466206000000071000/reports HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "baseTableName": "Sales",
    "title": "Cumulative Sales",
    "reportType": "chart",
    "chartType": "line",
    "axisColumns": [
        {"type": "xAxis", "columnName": "Order Date", "operation": "monthyear"},
        {
            "type": "yAxis",
            "columnName": "Sales",
            "operation": "sum",
            "windowFunction": {"type": "runtotal", "baseField": "Order Date", "baseFieldPosition": "xAxis"}
        }
    ]
}
```

**Case 6 — Three-month moving average**

```http
POST /restapi/v2/workspaces/466206000000071000/reports HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "baseTableName": "Sales",
    "title": "Sales 3-Month Moving Average",
    "reportType": "chart",
    "chartType": "line",
    "axisColumns": [
        {"type": "xAxis", "columnName": "Order Date", "operation": "monthyear"},
        {
            "type": "yAxis",
            "columnName": "Sales",
            "operation": "sum",
            "windowFunction": {
                "type": "movingcalc",
                "baseField": "Order Date",
                "baseFieldPosition": "xAxis",
                "movingCalculation": {
                    "calculation": "average",
                    "previous": 2,
                    "next": 0,
                    "includeCurrent": true,
                    "includeNull": false
                }
            }
        }
    ]
}
```

**Case 7 — Map chart with a geo role**

```http
POST /restapi/v2/workspaces/466206000000071000/reports HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "baseTableName": "Sales",
    "title": "Sales by Country",
    "reportType": "chart",
    "chartType": "map area",
    "axisColumns": [
        {"type": "xAxis", "columnName": "Country", "operation": "geo", "geoRole": "country"},
        {"type": "yAxis", "columnName": "Sales", "operation": "sum"}
    ]
}
```

**Case 8 — Wildcard filter**

```http
POST /restapi/v2/workspaces/466206000000071000/reports HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "baseTableName": "Sales",
    "title": "Enterprise Accounts",
    "reportType": "chart",
    "chartType": "bar",
    "axisColumns": [
        {"type": "xAxis", "columnName": "Customer", "operation": "actual"},
        {"type": "yAxis", "columnName": "Sales", "operation": "sum"}
    ],
    "filters": [
        {
            "columnName": "Customer",
            "operation": "actual",
            "filterType": "wildcard",
            "exclude": false,
            "values": [],
            "wildcard": {
                "criteria": [
                    {"operation": "CONTAINS", "value": "Corp"},
                    {"operation": "STARTS_WITH", "value": "Acme"}
                ],
                "expression": "(1 OR 2)"
            }
        }
    ]
}
```

**Case 9 — Merged Y axes**

```http
POST /restapi/v2/workspaces/466206000000071000/reports HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "baseTableName": "Sales",
    "title": "Revenue and Cost",
    "reportType": "chart",
    "chartType": "line",
    "axisColumns": [
        {"type": "xAxis", "columnName": "Order Date", "operation": "monthyear"},
        {"type": "yAxis", "columnName": "Sales", "operation": "sum"},
        {"type": "yAxis", "columnName": "Cost", "operation": "sum"}
    ],
    "isAxisMerge": true,
    "mergeAxisInfo": [
        {"axisIndex": [2, 3], "labelName": "Amount"}
    ]
}
```

**Case 10 — Date user filters: range picker and relative**

```http
POST /restapi/v2/workspaces/466206000000071000/reports HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "baseTableName": "Sales",
    "title": "Sales by Year",
    "reportType": "chart",
    "chartType": "bar",
    "axisColumns": [
        {"type": "xAxis", "columnName": "Order Date", "operation": "year"},
        {"type": "yAxis", "columnName": "Sales", "operation": "sum"}
    ],
    "userFilters": [
        {
            "columnName": "Order Date",
            "operation": "dateRange",
            "compType": "dateRange",
            "filterType": "range",
            "values": ["18 Mar 2019 to 10 Sep 2025"],
            "defaultFilterValues": ["18 Mar 2024 to 01 Jan 2025"]
        },
        {
            "columnName": "Ship Date",
            "operation": "relative",
            "compType": "multiSelect",
            "filterType": "common",
            "values": ["This Year", "Last Year", "Last 3 Months"]
        }
    ]
}
```

**Case 11 — Unrecognised chart type (rejected)**

```http
POST /restapi/v2/workspaces/466206000000071000/reports HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "baseTableName": "Sales",
    "title": "Stacked Area Attempt",
    "reportType": "chart",
    "chartType": "stacked area without points",
    "axisColumns": [
        {"type": "xAxis", "columnName": "Order Date", "operation": "year"},
        {"type": "yAxis", "columnName": "Sales", "operation": "sum"}
    ]
}
```

## Sample Responses

**HTTP 200 OK — Chart created (Cases 1–2 and 5–10)**

```json
{
    "status": "success",
    "summary": "Create Chart View",
    "data": {
        "viewId": "466206000000105001"
    }
}
```

**HTTP 200 OK — Pivot created (Case 3)**

```json
{
    "status": "success",
    "summary": "Create Pivot View",
    "data": {
        "viewId": "466206000000105002"
    }
}
```

**HTTP 200 OK — Summary created (Case 4)**

```json
{
    "status": "success",
    "summary": "Create Summary View",
    "data": {
        "viewId": "466206000000105003"
    }
}
```

**HTTP 406 Not Acceptable — Unrecognised chart type (Case 11)**

```json
{
    "status": "failure",
    "summary": "INVALID_GRAPH_TYPE",
    "data": {
        "errorCode": 8144,
        "errorMessage": "Invalid graph type : stacked area without points"
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Report](../../../sdk-examples/reports-and-dashboards/reports/create-report.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Not idempotent** | Every successful call creates a new report. Repeating a call with the same `title` fails with `7111` (or `8201` while the first call is still being saved). |
| **All-or-nothing** | The create is transactional: when any error is returned, no report is created. |
| **Case sensitivity** | `baseTableName` and `tableName` are matched exactly. `columnName`, `chartType`, `operation` (except date filter operations) and window-function names are case-insensitive. `reportType`, axis `type`, `sort`, `geoRole`, `compType` and `behaviour` must be sent exactly as documented. |
| **`chartType` versus shelves** | Not validated — see the note under [CONFIG Parameters](#config-parameters). |
| **`sort`** | Chart and summary reports apply only the first `sort` in `axisColumns`. |
| **`folderId` for shared users** | Ignored without error — see [Permission Model](overview.md#permission-model). |
| **Write-only fields** | `folderId`, `displayName`, `sort`, `rangeSize`, `windowFunction`, `geoRole`, `wildcard`, `rankingColumn`, `rankingColumnDateSubType` and every user-filter key except `columnName`, `tableName` and `operation` are never returned by [Read Report Metadata](get-report-metadata.md). |
| **Client Portal / White Label** | Not available on Client Portal / White Label domains. Call the standard API host. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | Workspace list → `<workspace-id>` and `orgId`; the workspace's view list → `baseTableName`, column names, `folderId` → Create Report → `data.viewId` → [Read Report Metadata](get-report-metadata.md) / [Update Report](update-report.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7016](../../../foundations/error-codes.md#error-7016) | 400 | `OBJECT_NAME_EMPTY` — `title` is empty or whitespace-only. | Supply a non-empty `title`. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | `META_DBOBJECT_NAME_DUPLICATED` — An object with this `title` already exists in the workspace. | Choose a `title` not used by any table, report or dashboard in the workspace. |
| [7137](../../../foundations/error-codes.md#error-7137) | 400 | `NOT_A_TABLE` — `baseTableName` names an object that is not a table or query table. | Use a table or query table. |
| [7138](../../../foundations/error-codes.md#error-7138) | 400 | `META_OBJECT_NOT_PRESENT` — `baseTableName` does not match a table in this workspace (matching is case-sensitive). | Use the exact table display name. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller cannot read the base table, or lacks Create Report permission on the workspace. | Call as a user with Create Report permission and read access to the base table. |
| [7309](../../../foundations/error-codes.md#error-7309) | 400 | `SECURITY_NEEDS_LOGIN` — `Authorization` header absent. | Send `Authorization: Zoho-oauthtoken <token>`. |
| [7324](../../../foundations/error-codes.md#error-7324) | 400 | `PERMISSION_DENIED_FOR_DOMAINUSER` — A Custom Role user's role does not grant Create Report on the base table. | Grant Create Report in the role. |
| [7362](../../../foundations/error-codes.md#error-7362) | 400 | `NO_SUCH_FOLDER_IN_DB` — `folderId` does not exist in the workspace. | Supply a folder ID of this workspace, or omit `folderId`. |
| [7701](../../../foundations/error-codes.md#error-7701) | 400 | `DROP_X_Y` — The chart's shelves do not form a drawable chart; typically no X-axis or no Y-axis column. | Add the missing shelf. |
| [7703](../../../foundations/error-codes.md#error-7703) | 400 | `REMOVE_CLR_FIELD` — Multiple Y-axis columns in a shelf combination that does not support them, typically with a `colorAxis` column or with no X-axis column. | Drop the colour axis, add an X axis, or reduce to one Y axis. |
| [7705](../../../foundations/error-codes.md#error-7705) | 400 | `DROP_SUMMARY` — A summary report has no `groupBy` and no `summarize` column. | Add at least one. |
| [7706](../../../foundations/error-codes.md#error-7706) | 400 | `DROP_PIVOT` — A pivot report has no `row`, `column` or `data` column. | Add at least one. |
| [7725](../../../foundations/error-codes.md#error-7725) | 400 | `ILLEGAL_COLUMN` — The caller is not permitted to access a column used in the report. | Share the column with the caller, or remove it. |
| [7727](../../../foundations/error-codes.md#error-7727) | 400 | `Y_EXCEED_LIMIT` — More than 15 Y-axis columns on a chart. | Reduce to 15 or fewer. |
| [8008](../../../foundations/error-codes.md#error-8008) | 400 | `UNKNOWN_PARAMETER` — `behaviour` was supplied on a `slider`, `dateRange` or `relative` user filter. | Remove `behaviour` from that user filter. |
| [8050](../../../foundations/error-codes.md#error-8050) | 400 | `INVALID_VALUE` — A value is invalid: an unknown column name; an explicit `null` for any key; an empty `columnName`; a `mergeAxisInfo` rule violation; `mergeAxisInfo` without `isAxisMerge: true`; `isallval: false` with no `values`; an invalid user-filter `operation` or `filterType`; `exclude: true` on a range-picker user filter. | Check names and values against this document. |
| [8051](../../../foundations/error-codes.md#error-8051) | 400 | `VALUE_NOT_PRESENT` — A mandatory key is missing: `title`, `reportType`, `axisColumns`, an axis `type` or `operation`, a filter's `filterType`, `values`, `exclude` or `operation`, `windowFunction.type`, `baseFieldPosition`, `movingCalculation` or one of its keys, a `wildcard` object, `mergeAxisInfo[].axisIndex`; or the four-key base-field lookup found no matching entry. | Add the missing key. |
| [8052](../../../foundations/error-codes.md#error-8052) | 400 | `COLUMN_COUNT_EXCEEDED` — More than 1000 entries in `axisColumns`, `filters` or `userFilters`. | Reduce the array size. |
| [8053](../../../foundations/error-codes.md#error-8053) | 400 | `AGGREGATE_COLUMN_INVALID_FIELD` — In a pivot or summary report, an aggregate formula column is placed on `row`, `column` or `groupBy`. | Place it on `data` or `summarize`. |
| [8055](../../../foundations/error-codes.md#error-8055) | 400 | `NUMERIC_RANKING_COLUMN` — `rankingColumn` names a Numeric column. | Use a Text or Date column. |
| [8056](../../../foundations/error-codes.md#error-8056) | 400 | `NOT_ALLOWED` — `pctoftotal` on an `average`, `stddev`, `variance`, `dc` or `distinctcount` column, or on an aggregate formula. | Choose another window function type. |
| [8057](../../../foundations/error-codes.md#error-8057) | 400 | `NOT_ALLOWED_BASEFIELD` — `windowFunction.baseField` is not a dimension entry of `axisColumns`. | Add the base field to `axisColumns` as a dimension. |
| [8058](../../../foundations/error-codes.md#error-8058) | 400 | `BASEFIELD_INVALID_AXIS` — `windowFunction.baseField` sits on a different shelf from `baseFieldPosition`. | Correct `baseFieldPosition`. |
| [8059](../../../foundations/error-codes.md#error-8059) | 400 | `UNRELATED_TABLE` — A `tableName` is not a table joined to the base table. | Use a table reachable from the base table. |
| [8144](../../../foundations/error-codes.md#error-8144) | 406 | `INVALID_GRAPH_TYPE` — `chartType` is not a value from [`chartType` Values](overview.md#charttype-values). | Use an accepted chart type, or omit `chartType`. |
| [8162](../../../foundations/error-codes.md#error-8162) | 400 | `RANGE_SIZE_NOT_SUPPORTED_FOR_THIS_OPERATION` — `rangeSize` was supplied on an operation other than `range`. | Use `rangeSize` only with `operation: "range"`. |
| [8164](../../../foundations/error-codes.md#error-8164) | 400 | `FILTER_COLUMN_DATATYPE_MISMATCH` — A numeric `individualvalues` filter value is not a valid number for the column. | Send the exact stored numeric value. |
| [8166](../../../foundations/error-codes.md#error-8166) | 400 | `INVALID OPERATION FOR THE COLUMN` — The `operation` is not valid for the column's category and shelf; or a `defaultFilterValues` entry is invalid. | See [Axis Operation Values](overview.md#axis-operation-values) and [Static Filter Operation and Type Values](overview.md#static-filter-operation-and-type-values). |
| [8167](../../../foundations/error-codes.md#error-8167) | 400 | `INVALID FILTER TYPE FOR THE GIVEN OPERATION` — The `filterType` is not valid for the column category and `operation`. | See [Static Filter Operation and Type Values](overview.md#static-filter-operation-and-type-values). |
| [8168](../../../foundations/error-codes.md#error-8168) | 400 | `INVALID CRITERIA FORMAT FOR THE COLUMN` — A `values` entry does not match the format for its `filterType`. | See [Filter Value Formats](overview.md#filter-value-formats). |
| [8169](../../../foundations/error-codes.md#error-8169) | 400 | `INVALID WINDOW TYPE FOR THE COLUMN` — `windowFunction.type` or `movingCalculation.calculation` is not a valid value. | See [Window Function Type Values](overview.md#window-function-type-values). |
| [8170](../../../foundations/error-codes.md#error-8170) | 400 | `INVALID AXIS TYPE FOR THE REPORT` — An axis `type` is not valid for the chosen `reportType`. | See [Axis Type Values](overview.md#axis-type-values). |
| [8179](../../../foundations/error-codes.md#error-8179) | 403 | `ADVFILTER_EXPRESSION_NO_CRITERIAS` — `wildcard.criteria` is empty. | Supply 1–15 criteria. |
| [8187](../../../foundations/error-codes.md#error-8187) | 400 | `ADVFILTER_EXPRESSION_ORDER_CHANGE` — Criteria indexes in `wildcard.expression` are out of order. | Reference criteria as 1, 2, 3 … in order. |
| [8188](../../../foundations/error-codes.md#error-8188) | 400 | `ADVFILTER_EXPRESSION_LENGTH_MISMATCH` — The number of indexes in `wildcard.expression` differs from the number of criteria. | Reference every criterion exactly once. |
| [8201](../../../foundations/error-codes.md#error-8201) | 400 | `DUPL_DISPLAY_NAME` — Another report with the same `title` is being created at the same moment. | Retry with a unique `title`. |
| [8250](../../../foundations/error-codes.md#error-8250) | 400 | `INVALID_UF_COMP_TYPE` — `compType` is not valid for the column category or operation. | See [User Filter Rules by Column](overview.md#user-filter-rules-by-column). |
| [8251](../../../foundations/error-codes.md#error-8251) | 400 | `INCORRECT_DATE_VALUE` — A date in a date-range static filter could not be parsed. | Use the date formats in [Filter Value Formats](overview.md#filter-value-formats). |
| [8253](../../../foundations/error-codes.md#error-8253) | 400 | `REQUIRED PARAM IS MISSING` — A required key is missing: `windowFunction.baseField`, user-filter `compType`, or user-filter `filterType` where [User Filter Rules by Column](overview.md#user-filter-rules-by-column) marks it required. | Add the key. |
| [8254](../../../foundations/error-codes.md#error-8254) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE_FOR_COLUMN` — `latitude` / `longitude` on a text column, or a place role on a numeric column. | See [Geo Role Values](overview.md#geo-role-values). |
| [8255](../../../foundations/error-codes.md#error-8255) | 400 | `INVALID_KEY_GIVEN` — `operation: "geo"` on a column type that cannot be geocoded. | Use a Plain Text, Number, Positive Number, Decimal Number or Geo column. |
| [8256](../../../foundations/error-codes.md#error-8256) | 404 | `GEO_COL_COUNT_EXCEEDED` — More than one text geo column on X, or more than one numeric geo column on one axis. | Keep one geo column per axis. |
| [8257](../../../foundations/error-codes.md#error-8257) | 400 | `GEO_COL_COUNT_EXCEEDED_CATEGORICAL` — A text geo column on X coexists with a numeric geo column on Y. | Use one or the other. |
| [8258](../../../foundations/error-codes.md#error-8258) | 400 | `GEO_COL_CATEGORY_ONLY_X` — A text geo column was placed on a shelf other than X. | Move it to `xAxis`. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` is missing, or `baseTableName` is absent. | Send `CONFIG` with `baseTableName`. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | `MORE_THAN_MAX_LENGTH` — A string exceeds its limit: `title` 100, `description` 250, `chartType` 50, axis `displayName` 250, `columnName` 1000, axis `tableName` 100, `windowFunction` object 1000, serialised `values` / `defaultFilterValues` array 1000. | Shorten the value. |
| [8509](../../../foundations/error-codes.md#error-8509) | 400 | `PATTERN_NOT_MATCHED` — A value does not match its pattern: `reportType: "Chart"`, `type: "sizeAxis"`, `sort: "descending"`, a `chartType` with a hyphen, `compType: "multiselect"`, a wildcard `expression` without parentheses, a wildcard `operation` in lowercase. | Use the exact accepted values. |
| [8516](../../../foundations/error-codes.md#error-8516) | 400 | `UNABLE_TO_PARSE_DATA_TYPE` — A numeric value could not be parsed, for example `rangeSize` sent as an array. | Send a plain number. |
| [8517](../../../foundations/error-codes.md#error-8517) | 400 | `DATATYPE_NOT_MATCHED` — A value has the wrong JSON type: `exclude: "yes"`, `isAxisMerge: 1`, `folderId: "abc"`. | Use JSON booleans, numbers and strings as documented. |
| [8534](../../../foundations/error-codes.md#error-8534) | 400 | `JSON_PARSE_ERROR` — `CONFIG` is not valid JSON, or a key has the wrong structure (`axisColumns` as `{}`, `values` as a string, `mergeAxisInfo` as an object). | Arrays must be `[]`, objects `{}`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |
| [8542](../../../foundations/error-codes.md#error-8542) | 400 | `EXTRA_KEY_FOUND_IN_JSON` — A key not listed in this document is present. | Remove the key. |
| [8544](../../../foundations/error-codes.md#error-8544) | 400 | `OUT_OF_RANGE` — An integer is outside its range: `percentileVal` outside 0–100, a `mergeAxisInfo` index outside 0–100. | Use a value inside the range. |
| [8547](../../../foundations/error-codes.md#error-8547) | 400 | `ARRAY_SIZE_OUT_OF_RANGE` — More than 15 entries in `wildcard.criteria`. | Reduce the array size. |
| [14037](../../../foundations/error-codes.md#error-14037) | 400 | `DISABLED_COLUMNS_USED` — A disabled column is used in the report. | Enable the column, or remove it. |

# Related

- [Reports (Analysis Views) overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Reports & Dashboards](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Read Report Metadata](get-report-metadata.md), [Update Report](update-report.md).
- [SDK examples](../../../sdk-examples/reports-and-dashboards/reports/create-report.md).
- [API units](../../../foundations/api-units.md) - unit cost, unit categories and frequency limits for every endpoint.
