# Zoho Analytics V2 REST API — Reports

A **report** (also called a *visual*, an *analysis view*, or simply a *view* in API responses and error
messages — the four terms are interchangeable) is a saved visualisation built on top of a table. Zoho
Analytics exposes three report families through this API:

| `reportType` | What it produces |
|---|---|
| `chart` | A chart — bar, line, pie, map, bubble, heat map, and so on. |
| `pivot` | A pivot table with row, column and data shelves. |
| `summary` | A summary view with grouping and aggregate columns. |

A report is defined almost entirely by its **drop fields** — the `axisColumns` array, where each entry
says *which column* goes on *which shelf* with *which operation*. Everything else (filters, user filters,
window functions, formatting) hangs off that core.

> **These APIs are blocked on white-label / custom domains.** All three endpoints are declared
> `custom-domain-disable`. Call the standard REST host for your data centre
> (`analyticsapi.zoho.com`, `analyticsapi.zoho.eu`, …).

> **Update is a full replacement.** Whatever you send becomes the report. Omitting `filters` clears the
> filters; omitting `description` clears the description. See
> [Update is destructive](#update-is-destructive) before writing any update integration.

---

## Index

| # | API Name | Method | URL |
|---|----------|--------|-----|
| 1 | [Create Report](#1-create-report) | POST | `/restapi/v2/workspaces/<workspace-id>/reports` |
| 2 | [Read Report Metadata](#2-read-report-metadata) | GET | `/restapi/v2/workspaces/<workspace-id>/reports/<report-id>/metadata` |
| 3 | [Update Report](#3-update-report) | PUT | `/restapi/v2/workspaces/<workspace-id>/reports/<report-id>` |

---

## Round-tripping a report

[Read Report Metadata](#2-read-report-metadata) is an **inspection** endpoint. Its response is a summary
of the stored definition, not a Create or Update payload. Feeding it back into Update is the most common
and most damaging mistake against this API: the call succeeds, and the report quietly loses most of its
configuration.

**If you need read-modify-write, retain the CONFIG you submitted at create time and modify that.**

### Written but never returned

Every key below is accepted on write and is absent from the read response. A read-modify-write cycle
destroys all of them.

| Section | Keys lost |
|---|---|
| Top level | `folderId`, `settings` (all pivot layout and theme properties), `drillActionConfig`, `modifiedPaths` |
| `axisColumns[]` | `displayName`, `sort`, `rangeSize`, `windowFunction`, `format`, `geoRole` |
| `filters[]` | `wildcard` (all criteria and the expression), `rankingColumn`, `rankingColumnDateSubType`, `additionalDetails` |
| `userFilters[]` | `compType`, `filterType`, `isallval`, `values`, `defaultFilterValues`, `exclude`, `behaviour` |

Two consequences are worth calling out:

- **User filters are reduced to three keys** — `tableName`, `columnName`, `operation`. Writing the read
  response back rebuilds every user filter with default behaviour: sliders become select lists,
  date-range pickers become single selects, restricted value lists become "all values", and
  pre-selections and exclusions are dropped.
- **A geo column cannot be round-tripped.** `operation: "geo"` is returned but `geoRole` is not, and
  `geo` without `geoRole` is invalid — so the update fails outright.

### Values that change across a round trip

| Key | Behaviour |
|---|---|
| `axisColumns[].type` | Always returned **lowercase** (`xaxis`, `yaxis`, `coloraxis`, `textaxis`, `groupby`, `tooltip`, `latlng`) regardless of the casing you sent. All of those are accepted on write. The exception: a `tooltip` column may be returned as `group`, which the schema rejects with **8509**. |
| `chartType` | Reverse-derived from storage, not stored verbatim. Where several names share one stored chart/sub-chart pair the returned name is one of them, not necessarily yours: `area` / `area without points` / `area without markers`; `line` / `line with points` / `line with markers`; `map area` / `map filled`; `web` / `web with fill`. For `stacked area without points` and `stacked area without markers` the key is **omitted entirely**. |
| `axisColumns[].operation` | Also reverse-derived. Aliases collapse — `average`/`avg`, `absquarter`/`quarteryear`, `absmonth`/`monthyear`, `absweek`/`weekyear`, `actual`/`geo`, and `variance`/`dc`/`distinctcount` — and all thirteen date distinct-count operations (`distinctcount`, `ydc`, `mydc`, `wydc`, `qydc`, `ddc`, `dtdc`, `qdc`, `wdc`, `wddc`, `dmdc`, `hdc`, `mdc`) share one stored marker, so the returned one may compute a **different** distinct count from the one you created. An unrecognised stored operation is reported as `actual`. |
| `filters[].operation` | Date filters created with `actual`, `range` or `daterange` share one stored value and may be returned as any of the three. |
| `filters[].filterType` | Several input values share one stored sub-type and collapse on read: `{absquarter, quarteryear, quarter}`, `{absmonth, monthyear, month}`, `{absweek, weekyear, week}`, `{date, fulldate}`, `{range, daterange}`, `{year, common}`. An **absolute** `monthyear` filter can be reported as a **seasonal** `month` filter — re-submitting that changes what the report shows. |
| `filters[].values` | Reconstructed by splitting the stored display criteria on commas. **Any filter value containing a comma is split into several values**, and surrounding whitespace is lost. |
| `userFilters[].operation` | For **date** columns the read puts a `filterType`-shaped value into this field — `year`, `monthyear`, `fulldate`, `datetime`, `range`, and so on. These are **not** valid `operation` values on write (which takes `actual`, `seasonal`, `relative`, `range`, `daterange`), so re-submitting raises **8166**. For numeric columns, aliases collapse as above. |
| `reportType` | May be returned as `widget` for widget-backed views, which Create and Update both reject with **8509**. |
| `tableName` | Always returned on every axis column and filter, even where you omitted it. The returned value is valid on write. |
| `columnName` | Returned in the column's stored display casing; matched case-insensitively on write. |

### Keys that must be removed before an update

| Key | Why |
|---|---|
| `baseTableName` | Returned by the read, rejected by Update with **8542**. |

And `reportType` must be **added** if you are assembling an update payload from anything that omits it —
it is mandatory on Update and must match the stored view type.

> **Axis-merged reports cannot be read at all.** When `isAxisMerge` is `true` the metadata call currently
> fails with an internal error while assembling `mergeAxisInfo`. Do not build a read-modify-write flow
> that depends on reading a merged-axis report.

---

## 1. Create Report

Builds a new chart, pivot or summary view on an existing table and returns its view ID.

| Attribute | Value |
|-----------|-------|
| **Method** | POST |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/reports` |
| **OAuth Scope** | `ZohoAnalytics.modeling.create` |
| **ZANALYTICS-ORGID Header** | **Mandatory** |
| **Content-Type** | `application/x-www-form-urlencoded` |
| **Permission Required** | Workspace Admin / Organization Admin, or a shared or group user holding **Create Report** permission on the base table. |
| **Custom domain** | Not permitted. |

### CONFIG Parameter

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
| `chartType` | String | Conditional | Letters, digits and spaces only; max 50 | Required in practice when `reportType` is `chart`. Matched case-insensitively. Omitted or unrecognisable-as-empty → the server picks `BEST`. Ignored for pivot and summary. See [Appendix A](#appendix-a--chart-types). |
| `isAxisMerge` | Boolean | No | `true` / `false` | Merge multiple Y axes onto one shared axis. |
| `mergeAxisInfo` | **JSONArray** | Conditional | Max 10 entries | Required when merging. Each entry is `{"axisIndex":[<int 0-100>, …], "labelName":"<max 250 chars>"}`. If this array is non-empty, `isAxisMerge` **must** be `true`. |
| `filters` | JSONArray | No | Max 1000 entries | Static filter criteria baked into the report. See [`filters`](#filters). |
| `userFilters` | JSONArray | No | Max 1000 entries | Interactive filter widgets shown to viewers. See [`userFilters`](#userfilters). |
| `settings` | JSONObject | No | **Pivot reports only** | Layout and theme settings. Supplying this for a chart or summary raises **8147**. See [`settings`](#settings-pivot-only). |
| `drillActionConfig` | JSONObject | No | Max 10 actions | Custom drill-through actions. See [`drillActionConfig`](#drillactionconfig). |
| `modifiedPaths` | JSONObject | No | — | Explicit join-path selection, used when two tables are reachable by more than one relationship path. Map of path key → array of view IDs. |

### `axisColumns`

Each entry places one column on one shelf.

| Key | Type | Mandatory | Constraints | Description |
|-----|------|-----------|-------------|-------------|
| `type` | String | **Yes** | See [Appendix B](#appendix-b--axis-types) | Which shelf the column goes on. **Case-sensitivity matters** — see the appendix. |
| `columnName` | String | **Yes** | Max 1000 | Column display name. Matched case-insensitively. |
| `operation` | String | **Yes** | Letters only; see [Appendix C](#appendix-c--operations) | Aggregation or date-grouping applied to the column. |
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

#### Window functions

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

#### Geo columns

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

### `filters`

Static criteria applied every time the report renders. Viewers cannot change them.

| Key | Type | Mandatory | Description |
|-----|------|-----------|-------------|
| `columnName` | String | **Yes** | Column to filter on. |
| `operation` | String | **Yes** | How the column is interpreted before the criteria is applied. See [Appendix D](#appendix-d--filter-operations-and-types). |
| `filterType` | String | **Yes** | Shape of the criteria. See [Appendix D](#appendix-d--filter-operations-and-types). |
| `values` | JSONArray | **Yes** | Criteria values, as strings. Format depends on `filterType` — see [Appendix E](#appendix-e--filter-value-formats). |
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

### `userFilters`

Interactive filter widgets rendered alongside the report.

| Key | Type | Mandatory | Description |
|-----|------|-----------|-------------|
| `columnName` | String | **Yes** | Column to expose. Matched case-insensitively. |
| `operation` | String | Conditional | Mandatory for date and numeric columns; ignored for text columns, which are always `actual`. Dates: `actual`, `seasonal`, `relative`, `range`, `daterange`. Numerics: `sum`, `min`, `max`, `average`, `stddev`, `std`, `count`, `variance`, `dc`, `distinctcount`, `median`, `mode`, `measure`, `dimension`, `actual`, `aggregate`. |
| `compType` | String | Conditional | Widget type: `singleSelect`, `multiSelect`, `slider`, `dateRange`. `slider` is measure-only; `singleSelect` / `multiSelect` are for dimensions and dates. A mismatch raises **8250**; a missing required `compType` raises **8253**. |
| `filterType` | String | Conditional | Criteria shape. Required for measures and for date `actual` / `seasonal` operations. See [Appendix D](#appendix-d--filter-operations-and-types). |
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

### `settings` (pivot only)

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

### `drillActionConfig`

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

### Sample Requests

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

### Sample Response

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

### Error Codes

| Error-Code | Reason | Solution |
|-----------:|--------|----------|
| 8504 | `baseTableName` is absent, or the `CONFIG` parameter itself is missing. | Send `CONFIG` with `baseTableName`. |
| 7138 | `baseTableName` does not resolve to a table in this workspace. | Use the exact table display name. |
| 7016 | `title` is empty or whitespace-only. | Supply a non-empty title. |
| 7111 | A view with this `title` already exists in the workspace. | Choose a unique title. |
| 8507 | `title` exceeds 100 characters, `description` exceeds 250, or an axis `displayName` exceeds 250. | Shorten the value. |
| 8252 | `reportType` is absent or `null`. | Supply `chart`, `pivot` or `summary`. |
| 8092 | `reportType` resolves to a view kind that cannot be saved standalone. | Use `chart`, `pivot` or `summary`. |
| 8144 | `chartType` is not a recognised chart name. | See [Appendix A](#appendix-a--chart-types). |
| 8147 | `settings` was supplied for a non-pivot report. | Remove `settings`, or change `reportType` to `pivot`. |
| 7362 | `folderId` does not exist in the workspace. | Supply a valid folder ID or omit the key. |
| 8051 | A required field is missing — `title`, `reportType`, `axisColumns`, or a mandatory key inside an axis/filter object. | Add the missing field. |
| 8050 | A value is invalid — unknown `columnName`, an operation incompatible with the column, a `null` `axisColumns`. | Check column names and operations. |
| 8052 | More than 1000 entries in `axisColumns`, `filters` or `userFilters`. | Reduce the array size. |
| 8170 | An axis `type` is not valid for the chosen `reportType`. | See [Appendix B](#appendix-b--axis-types). |
| 7701 | A chart report has no X-axis or no Y-axis column. | Add at least one of each. |
| 7703 | A `colorAxis` column is present alongside more than one Y-axis column. | Drop the colour axis, or reduce to one Y axis. |
| 7727 | More than 15 Y-axis columns on a chart. | Reduce to 15 or fewer. |
| 8021 | The pivot or summary structure is invalid — no `data` column in a pivot, too many `data` or `groupBy` columns, or a column in a position its type cannot occupy. On **Update**, also raised when `reportType` does not match the stored view's type. | Review the axis configuration. |
| 8166 | The `operation` is incompatible with the column's data type. | See [Appendix C](#appendix-c--operations). |
| 8167 | The `filterType` is not valid for the column type + `operation` combination. | See [Appendix D](#appendix-d--filter-operations-and-types). |
| 8168 | A `values` entry does not match the expected format for the `filterType`. | See [Appendix E](#appendix-e--filter-value-formats). |
| 8191 | An invalid date value was supplied to a date filter. | Use the documented date formats. |
| 8057 | The column named in `windowFunction.baseField` cannot be used as a base field here. | Choose a different reference column. |
| 8059 | The `tableName` is not part of the workspace or is not joined to the base table. | Use a table reachable through the join graph. |
| 8162 | `rangeSize` was supplied as a string, or on an operation that does not support ranges. | Send a JSON number, and only with `range` grouping. |
| 8516 | `rangeSize` was supplied as an array. | Send a plain number. |
| 8250 | `compType` is not applicable to the column category — e.g. `slider` on a dimension, `singleSelect` on a measure. | Match the widget to the column type. |
| 8253 | A mandatory `userFilters` key is missing, typically `compType` or `filterType`. | Add the missing key. |
| 8008 | `behaviour` was supplied on a `daterange` or `relative` user filter. | Remove `behaviour`. |
| 8254 | A `geoRole` value is wrong for the column type. | `latitude`/`longitude` for numeric columns; place roles for text columns. |
| 8255 | `geoRole` was supplied on a column that cannot be geocoded. | Remove `geoRole`, or use a geocodable column. |
| 8256 | More than one geo operation on the same axis. | Keep one geo column per axis. |
| 8257 | A numeric geo column coexists with a categorical geo column. | Use one or the other. |
| 8258 | A categorical geo column was placed on an axis other than X. | Move it to `xAxis`. |
| 8509 | An enumerated or pattern-constrained value does not match — `reportType: "Chart"` (must be lowercase), `type: "sizeAxis"` (must be `sizeaxis`), `sort: "descending"`, a wildcard `expression` without parentheses. | Use the exact accepted values. |
| 8517 | A field has the wrong JSON data type — `exclude: "yes"`, `isAxisMerge: "maybe"`, `compType: 123`. | Use real JSON booleans and strings. |
| 8534 | `CONFIG` is malformed, or a key has the wrong structural type — `axisColumns` as `{}`, `mergeAxisInfo` as an object, `values` as a bare string. | Arrays must be `[]`, objects `{}`. |
| 8542 | An unknown key is present in `CONFIG`, or a `windowFunction` is mis-configured. | Remove the key; check `windowFunction.type` against [the list](#window-functions). |
| 7005 | A `null` element inside `axisColumns` or `filters`. | Ensure every array element is a JSON object. |
| 7301 | The caller lacks Create Report permission on the workspace. | Grant the permission. |
| 8535 | Invalid or expired OAuth token. | Refresh with scope `ZohoAnalytics.modeling.create`. |

---

## 2. Read Report Metadata

Returns the stored definition of a chart, pivot or summary view.

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/reports/<report-id>/metadata` |
| **OAuth Scope** | `ZohoAnalytics.modeling.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** |
| **Permission Required** | **Design Modify** on the report. A read-only shared user cannot call this endpoint. |
| **Custom domain** | Not permitted. |

> This API has no CONFIG parameter. All input is in the URL path.

### Behaviour

> **The response is not a round-trippable CONFIG.** It is a *summary* of the stored definition, and it
> omits most of what Update accepts. In particular, `userFilters` entries come back with only
> `tableName`, `columnName` and `operation` — the widget type, criteria shape, values, default
> selections, exclusion flag and listing behaviour are all absent. Feeding this response straight back
> into [Update Report](#3-update-report) will **rebuild every user filter with default behaviour** and
> drop all per-column formatting, sorting and window functions. See
> [Round-tripping a report](#round-tripping-a-report) for the full list of what is lost and what
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

### Sample Request

```http
GET /restapi/v2/workspaces/466206000000071000/reports/466206000000105001/metadata HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Sample Response

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

### Error Codes

| Error-Code | Reason | Solution |
|-----------:|--------|----------|
| 7103 | Workspace not found. | Verify `<workspace-id>`. |
| 7104 / 7106 | The report does not exist or has been deleted. | Verify `<report-id>`. |
| 7319 | The report belongs to a different workspace. | Make the two path IDs consistent. |
| 8021 | The target is not a chart, pivot or summary view. | Use a report ID, not a table or dashboard. |
| 7301 | The caller lacks Design Modify permission on the report. | Grant edit access. |
| 8535 | Invalid or expired OAuth token. | Refresh with scope `ZohoAnalytics.modeling.read`. |

---

## 3. Update Report

Rebuilds an existing report from a fresh CONFIG.

| Attribute | Value |
|-----------|-------|
| **Method** | PUT |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/reports/<report-id>` |
| **OAuth Scope** | `ZohoAnalytics.modeling.update` |
| **ZANALYTICS-ORGID Header** | **Mandatory** |
| **Content-Type** | `application/x-www-form-urlencoded` |
| **Permission Required** | **Design Modify** on the report — the owner, a Workspace Admin, an Organization Admin, or a shared or group user granted edit rights. |
| **Custom domain** | Not permitted. |

### Update is destructive

The report is rebuilt from scratch on every call. There is no field-level patching.

| Omit this | And this happens |
|---|---|
| `filters` | All static filters are removed. |
| `userFilters` | All user filters are removed. |
| `description` | The description is **cleared** — `description` is written unconditionally, so an absent key stores `null`. |
| `chartType` | The chart type falls back to the server's `BEST` selection. |
| `axisColumns` | The call fails — `axisColumns` is mandatory. |

Always [read the current definition](#2-read-report-metadata) first — while remembering that the read
response is lossy. For anything beyond trivial edits, keep your own copy of the CONFIG you used at
create time and modify that instead — see [Round-tripping a report](#round-tripping-a-report).

### CONFIG Parameter

| Field | Mandatory | How it differs from Create |
|-------|-----------|----------------------------|
| `reportType` | **Yes** | Must match the stored view's type. A mismatch raises **8021**. |
| `axisColumns` | **Yes** | Identical structure to Create. |
| `title` | No | **Accepted but ignored.** The server overwrites it with the stored display name. A report cannot be renamed through this endpoint. |
| `description` | No | Accepted. Omitting it clears the existing description. |
| `chartType`, `isAxisMerge`, `mergeAxisInfo`, `filters`, `userFilters`, `settings` | No | Identical to Create. |
| `folderId` | No | Accepted by the schema, but the report cannot be moved. Supplying it raises **8145**. Omit it. |
| `baseTableName` | **Not accepted** | Rejected with **8542**. The base table cannot be changed. |
| `drillActionConfig`, `modifiedPaths` | **Not accepted** | Rejected with **8542**. |
| `objId` | No | Accepted by the schema but inert — the server always uses `<report-id>` from the URL. |

### Sample Requests

**Case 1 — Change the chart type and re-sort**

```http
PUT /restapi/v2/workspaces/466206000000071000/reports/466206000000105001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
  "reportType": "chart",
  "chartType": "stacked bar",
  "description": "Monthly trend, excluding returns",
  "axisColumns": [
    { "type": "xAxis", "columnName": "Order Date", "operation": "monthyear" },
    { "type": "yAxis", "columnName": "Sales", "operation": "sum", "sort": "asc" }
  ]
}
```

**Case 2 — Widen a filter, keeping everything else**

Note that `userFilters` has to be re-sent in full even though it is unchanged; omitting it would delete it.

```
CONFIG={
  "reportType": "chart",
  "chartType": "line",
  "description": "Monthly trend, excluding returns",
  "axisColumns": [
    { "type": "xAxis", "columnName": "Order Date", "operation": "monthyear" },
    { "type": "yAxis", "columnName": "Sales", "operation": "sum" }
  ],
  "filters": [
    { "columnName": "Status", "operation": "actual", "filterType": "individualvalues",
      "values": ["Returned", "Cancelled"], "exclude": true }
  ],
  "userFilters": [
    { "columnName": "Product Category", "operation": "actual",
      "compType": "multiSelect", "filterType": "individualvalues", "isallval": true }
  ]
}
```

**Case 3 — Strip all filters off a report**

```
CONFIG={
  "reportType": "pivot",
  "axisColumns": [
    { "type": "row",  "columnName": "Region", "operation": "actual" },
    { "type": "data", "columnName": "Sales",  "operation": "sum"    }
  ]
}
```

### Sample Response

**HTTP 204 No Content** — no response body is returned on success.

```
HTTP/1.1 204 No Content
```

### Error Codes

Update runs the same validation as Create, so every code in the
[Create Report error table](#error-codes) can be returned. Codes specific to Update or with different
triggers:

| Error-Code | Reason | Solution |
|-----------:|--------|----------|
| 7104 / 7106 | The report does not exist, has been deleted, or the caller cannot edit it. | Verify `<report-id>` and the caller's permission. |
| 8021 | `reportType` does not match the stored view's type, or the target is not an analysis view at all. | Send the report's actual type. |
| 8145 | `folderId` was supplied. | Remove `folderId` — reports cannot be moved through this endpoint. |
| 8542 | `baseTableName`, `drillActionConfig`, `modifiedPaths` or any other key outside the Update schema is present. | Remove the key. |
| 7301 | The caller lacks Design Modify permission on the report. | Grant edit access. |
| 8535 | Invalid or expired OAuth token. | Refresh with scope `ZohoAnalytics.modeling.update`. |

---

## Appendix A – Chart Types

`chartType` is matched case-insensitively. Only letters, digits and spaces are allowed — no hyphens or
underscores.

| Family | Accepted values |
|---|---|
| Area | `area`, `area with points`, `area without points`, `area with markers`, `area without markers`, `smooth area`, `smooth area with points`, `smooth area without points`, `smooth area with markers`, `smooth area without markers` |
| Stacked area | `stacked area`, `stacked area with points`, `stacked smooth area`, `stacked smooth area with points`, `stacked smooth area without points`, `stacked smooth area with markers`, `stacked smooth area without markers` |
| Bar | `bar`, `horizontal bar`, `stacked bar`, `horizontal stacked bar`, `butterfly` |
| Line | `line`, `line with points`, `line without points`, `line with markers`, `line without markers`, `smooth line`, `smooth line with points`, `smooth line without points`, `smooth line with markers`, `smooth line without markers`, `step` |
| Pie family | `pie`, `ring`, `semi pie`, `semi ring`, `funnel`, `pyramid` |
| Bubble & scatter | `bubble`, `packed bubble`, `scatter` |
| Combo | `combo`, `combo bar with smooth line` |
| Map | `map area`, `map filled`, `map bubble`, `map pie`, `map pie bubble`, `map bubble pie`, `map scatter`, `geo heat map` |
| Web | `web`, `web with fill`, `web without fill` |
| Other | `heat map`, `table chart` |

Omitting `chartType` (or sending an empty string) makes the server choose a chart automatically rather
than raising an error.

---

## Appendix B – Axis Types

The `type` value in an `axisColumns` entry must pass a pattern check *before* it is matched against the
report type. The pattern accepts the exact spellings below and no others.

| Accepted spellings | Valid for | Notes |
|---|---|---|
| `xaxis`, `xAxis`, `XAxis` | `chart` | Primary dimension axis. Required for charts (**7701**). |
| `yaxis`, `yAxis`, `YAxis` | `chart` | Measure axis. Required for charts. Maximum 15 (**7727**). |
| `textaxis`, `textAxis` | `chart` | Text/label axis. |
| `coloraxis`, `colorAxis` | `chart` | Colour-encoding axis. Cannot coexist with multiple Y axes (**7703**). |
| `sizeaxis` | `chart` | Size-encoding axis for bubble charts. **Lowercase only** — `sizeAxis` is rejected with **8509**. |
| `latlng`, `latLng` | `chart` | Latitude/longitude pair for map charts. |
| `tooltip`, `toolTip` | `chart` | Extra columns surfaced in the tooltip. |
| `custom` | `chart` | Custom-visual field slot. |
| `row` | `pivot` | Row grouping shelf. |
| `column` | `pivot` | Column grouping shelf. |
| `data` | `pivot` | Measure shelf. At least one is required. |
| `groupby`, `groupBy` | `summary` | Dimension grouping shelf. |
| `summarize` | `summary` | Aggregate shelf. |

Using an axis type outside its report family raises **8170**.

---

## Appendix C – Operations

The valid `operation` for an `axisColumns` entry depends on the column's data type **and** on where the
column sits.

### Numeric columns on a chart

`sum`, `min`, `max`, `average`, `avg`, `stddev`, `median`, `mode`, `percentile`, `count`, `variance`,
`dc`, `distinctcount`, `measure`, `dimension`, `range`, `actual`, `geo`.

`dimension` and `range` convert the measure into a dimension; `range` is the one that honours
`rangeSize`. Window functions are not available on either.

### Numeric columns in a pivot

- On `data`: `sum`, `min`, `max`, `average`, `stddev`, `median`, `mode`, `percentile`, `count`,
  `variance`, `dc`, `distinctcount`. **`avg` is not accepted here — use `average`.**
- On `row` / `column`: only `dimension` and `range`. `actual` is not valid in these positions.

### Text, email, URL and multi-line columns

`actual`, `count`, `dc`, `distinctcount`, `geo`. `actual` is the plain grouping operation.

### Date columns on a chart

- Grouping: `year`, `quarter`, `month`, `week`, `weekday`, `day`, `hour`
- Absolute grouping: `quarteryear` (alias `absquarter`), `monthyear` (alias `absmonth`),
  `weekyear` (alias `absweek`), `fulldate`, `datetime`
- Aggregates: `count`, `distinctcount`, `maxdate`, `mindate`
- Date distinct-count variants: `ydc`, `mydc`, `wydc`, `qydc`, `ddc`, `dtdc`, `qdc`, `wdc`, `wddc`,
  `dmdc`, `hdc`, `mdc`

### Date columns in a pivot

- On `data`: `maxdate`, `mindate`, `count`, `distinctcount`, and the date distinct-count variants.
- On `row` / `column`: the grouping operations listed above (no aggregates).

> `std` is **not** a valid axis operation — the standard-deviation operation is `stddev`. (`std` *is*
> accepted in the `filters` array, which uses a separate, more permissive map.)

> `axisColumns[].operation` is pattern-checked as letters only. Any value containing a digit, hyphen or
> underscore is rejected with **8509** before the maps above are consulted.

An operation that is not in the map for the column's data type raises **8166**.

---

## Appendix D – Filter Operations and Types

### Static filters (`filters`)

| Column type | `operation` | `filterType` |
|---|---|---|
| Numeric | `measure`, `dimension`, `sum`, `min`, `max`, `average`, `stddev`, `std`, `count`, `variance`, `dc`, `distinctcount`, `median`, `mode`, `actual`, `aggregate` | `individualvalues`, `range`, `ranking`, `rankingpct` |
| Text | `actual`, `count`, `dc`, `distinctcount`, `geo` | `individualvalues` (alias `individual`), `wildcard` |
| Date — absolute | `actual`, `range`, `daterange` | `year`, `quarter`, `month`, `week`, `weekday`, `day`, `hour`, `quarteryear` (alias `absquarter`), `monthyear` (alias `absmonth`), `weekyear` (alias `absweek`), `date`, `fulldate`, `datetime`, `range`, `daterange`, `common` |
| Date — seasonal | `seasonal` | `quarter`, `month`, `week`, `weekday`, `day`, `hour` |
| Date — relative | `relative` | `common`, `year`, `quarter`, `month`, `week`, `day`, `hour` |

Values are matched case-insensitively; `individualValues` and `individualvalues` both work.

### User filters (`userFilters`)

| Column type | `operation` | `compType` | `filterType` |
|---|---|---|---|
| Text | `actual` (implied; the key is ignored) | `singleSelect`, `multiSelect` | not required |
| Numeric | `sum`, `min`, `max`, `average`, `stddev`, `std`, `count`, `variance`, `dc`, `distinctcount`, `median`, `mode`, `measure`, `dimension`, `actual`, `aggregate` | `slider`, `multiSelect` | **required** — `individualvalues`, `range`, `ranking`, `rankingpct` |
| Date — absolute | `actual` | `singleSelect`, `multiSelect` | **required** — as the absolute list above |
| Date — seasonal | `seasonal` | `singleSelect`, `multiSelect` | **required** — `quarter`, `month`, `week`, `weekday`, `day`, `hour` |
| Date — relative | `relative` | `singleSelect`, `multiSelect` | `common` |
| Date — range | `daterange` / `range` | `dateRange` | not required |

`behaviour` (`ListAllValues`, `ListRelevantValues`, `ListOnlyRelevantValues`) applies to the select-style
widgets only. Supplying it with `daterange` or `relative` raises **8008**. `exclude: true` is not allowed
with `daterange`.

---

## Appendix E – Filter Value Formats

| `filterType` | Example `values` |
|---|---|
| `individualvalues` (text) | `["East", "West"]` |
| `individualvalues` (numeric) | `["100", "200"]` — exact stored values, no rounding |
| `range` (numeric) | `["1000 and below"]`, `["200000 to 300000"]`, `["500000 and above"]` |
| `ranking` | `["Top 2"]`, `["Bottom 10"]` |
| `rankingpct` | `["Top 10"]` (interpreted as a percentage) |
| `year` | `["2012", "2023"]` |
| `quarteryear` | `["Q1 2020", "Q2 2023"]` |
| `monthyear` | `["Aug 2012", "Jan 2013"]` — three-letter month abbreviations only |
| `weekyear` | `["W03 2012", "W02 2023"]` |
| `fulldate` / `date` | `["27 Jan, 2023", "20 Mar, 2023"]` |
| `datetime` | `["27 Jan 2023 00:00:00"]` |
| `daterange` / `range` (date) | `["from 10 Dec 2013 00:00:00"]`, `["10 Mar 2012 00:00:00 to 10 Dec 2012 00:00:00"]`, `["to 11 Mar 2013 00:00:00"]` |
| `quarter` (seasonal) | `["Q1", "Q3"]` |
| `month` (seasonal) | `["Jan", "Feb"]` |
| `week` (seasonal) | `["Week 2", "Week 3"]` |
| `weekday` (seasonal) | `["Sun", "Mon"]` |
| `day` (seasonal) | `["01", "15", "31"]` |
| `hour` (seasonal) | `["10", "13", "23"]` |
| `common` (relative) | `["This Year"]`, `["Last Month"]`, `["Last 2 Years"]`, `["Last 13 years"]` — `Last N <unit>` and `Next N <unit>` are both accepted |
| `wildcard` | `values` is unused; the criteria live in the `wildcard` object |

A value that does not match the expected shape raises **8168** (or **8191** for malformed dates).

---

## Appendix F – Common HTTP Headers

| Header | Value | Required | Notes |
|--------|-------|----------|-------|
| `Authorization` | `Zoho-oauthtoken <oauth-token>` | **Mandatory** | OAuth 2.0 access token of the calling user. |
| `ZANALYTICS-ORGID` | Organization ID | **Mandatory** | Organization ID that owns the workspace. |
| `Content-Type` | `application/x-www-form-urlencoded` | POST / PUT | `CONFIG` is a form-encoded body parameter on Create and Update. Read takes no parameters. |

---

## Appendix G – OAuth Scope Summary

| API | Method | Scope |
|-----|--------|-------|
| Create Report | POST | `ZohoAnalytics.modeling.create` |
| Read Report Metadata | GET | `ZohoAnalytics.modeling.read` |
| Update Report | PUT | `ZohoAnalytics.modeling.update` |

---

## Appendix H – Operational Notes and Failure Cases

| Scenario | Behaviour |
|----------|-----------|
| `reportType: "Chart"` (capitalised) | **8509**. The pattern accepts lowercase only. |
| `type: "sizeAxis"` | **8509**. Only the all-lowercase `sizeaxis` is accepted, unlike the other axis names which accept camel case. |
| Wildcard `expression: "1 AND 2"` | **8509**. The expression must be parenthesised: `"(1 AND 2)"`. |
| `mergeAxisInfo` sent as an object | **8534**. It is an array of merge-group objects. |
| `mergeAxisInfo` non-empty but `isAxisMerge` absent or `false` | Rejected — `isAxisMerge` must be `true` whenever merge groups are present. |
| `settings` on a chart or summary | **8147**. Settings are pivot-only. |
| `avg` as a pivot `data` operation | **8166**. Use `average`; the `avg` alias exists only for charts. |
| `actual` on a numeric column in a pivot `row` | **8166**. Pivot row/column positions accept only `dimension` and `range` for numeric columns. |
| Column name differs only by case from the stored name | Resolves correctly — column lookup is case-insensitive. |
| `title` sent on Update | Silently ignored. Use a rename API instead. |
| `description` omitted on Update | The existing description is cleared. |
| `folderId` sent on Update | **8145**, even when it matches the report's current folder. |
| Read metadata, then PUT it back unchanged | The report is rebuilt, but all user-filter configuration, column formatting, sorting and window functions are lost. Do not use the metadata response as an update payload. |
| Report created on a table the caller cannot read | **7301** during column validation. |
| More than 1000 entries in any of the three arrays | **8052**. |
