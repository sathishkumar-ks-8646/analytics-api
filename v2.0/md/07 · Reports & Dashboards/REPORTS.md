# Zoho Analytics V2 REST API — Reports

This document covers the V2 **Report** REST APIs of Zoho Analytics — the APIs that create a chart,
pivot or summary view on a table, read back its stored definition, and rebuild it from a new
definition.

## What is a "Report" in Zoho Analytics?

A **report** (also called a *visual*, an *analysis view*, or a *view* in API responses and error
messages) is a saved visualisation built on one table or query table of a workspace, optionally using
columns of the tables joined to it. The API manages three report families:

| `reportType` | What it produces |
|---|---|
| `chart` | A chart — one of the 57 chart types in [`chartType` Values](#charttype-values). |
| `pivot` | A pivot table with `row`, `column` and `data` shelves. |
| `summary` | A summary view with `groupBy` and `summarize` shelves. |

A report is defined almost entirely by its **drop fields** — the `axisColumns` array, where each entry
says *which column* goes on *which shelf* with *which operation*. Filters and user filters hang off that
core.

| Part | CONFIG attribute(s) | Notes |
|------|--------------------|-------|
| **Where it is built** | `baseTableName` | The table or query table. **Cannot be changed after creation.** |
| **What it is called** | `title`, `description` | Both can be changed with [Update Report](#3-update-report). |
| **What kind of report** | `reportType`, `chartType` | `reportType` **cannot be changed after creation.** |
| **What it shows** | `axisColumns` | Columns, shelves, operations, sorting, window functions, geo roles. |
| **Shared Y axes** | `isAxisMerge`, `mergeAxisInfo` | Charts only. |
| **What it always filters out** | `filters` | Static criteria; viewers cannot change them. |
| **What viewers can filter** | `userFilters` | Interactive filter widgets shown with the report. |
| **Where it is stored** | `folderId` | Create only. A report cannot be moved through these APIs. |

## Column Categories

Every rule in this document that depends on a column's data type uses one of these four categories.

| Category | Column data types |
|---|---|
| **Text** | Plain Text, Multi Line Text, Email, URL, Boolean (Decision Box), Geo, Time |
| **Numeric** | Number, Positive Number, Decimal Number, Currency, Percent, Auto Number, Duration |
| **Date** | Date, Date-Time |
| **Aggregate formula** | A workspace aggregate formula column, referenced by its name. Only **numeric** aggregate formulas are supported. |

> **The single most important behaviour:** [Update Report](#3-update-report) is a **full replacement**,
> and [Read Report Metadata](#2-read-report-metadata) returns a **lossy summary**. Writing a read
> response back through Update silently destroys user-filter configuration, sorting, window functions
> and geo roles. See [Round-tripping a Report](#round-tripping-a-report) before writing any
> read-modify-write integration.

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`). All three APIs use the `ZohoAnalytics.modeling` scope group — see [Appendix B](#appendix-b--oauth-scope-summary).
> - All three APIs are **workspace-scoped** (`/restapi/v2/workspaces/<workspace-id>/...`) and require the `ZANALYTICS-ORGID` header.
> - `ZohoAnalytics_Server_URI` depends on the data centre (for example `analyticsapi.zoho.com` or `analyticsapi.zoho.eu`).
> - **All three APIs are disabled in Client Portal / White Label request contexts.** Call the standard API host for your data centre.
> - **Only the keys documented here are accepted.** Any other key — at the top level of `CONFIG` or inside any nested object — is rejected with `8542`. Key names are case-sensitive.
> - None of these APIs moves, copies or deletes a report. Renaming is possible only through [Update Report](#3-update-report) (`title`).

---

## Index

| # | API Name | Method | URL | API Units |
|---|----------|--------|-----|----------|
| 1 | [Create Report](#1-create-report) | POST | `/restapi/v2/workspaces/<workspace-id>/reports` | 5 |
| 2 | [Read Report Metadata](#2-read-report-metadata) | GET | `/restapi/v2/workspaces/<workspace-id>/reports/<report-id>/metadata` | 0.1 |
| 3 | [Update Report](#3-update-report) | PUT | `/restapi/v2/workspaces/<workspace-id>/reports/<report-id>` | 5 |

> **Note on method overloading:** `PUT /reports/<report-id>` (Update) rebuilds the report. There is no
> `GET /reports/<report-id>`; the definition is read from the `/metadata` sub-path.

---

## Round-tripping a Report

**The read response is not an update payload. Writing it back succeeds and quietly strips the report.**

| What the read does | Result of writing it back |
|---|---|
| Omits `displayName`, `sort`, `rangeSize`, `windowFunction`, `geoRole` from every axis column | **All axis labels, sorting, bins and window functions are removed.** A `geo` column on a Plain Text or Number column **fails**, because `geoRole` is mandatory there. |
| Reduces every user filter to `tableName`, `columnName`, `operation` | **Every user filter is rebuilt with default behaviour, or fails** — date user filters come back with a `filterType`-shaped `operation` that raises `8166`. |
| Omits the `wildcard` object but returns `filterType: "wildcard"` | **The update fails** — wildcard filters cannot be updated (`8192`). |
| Returns `dc` columns as `distinctcount` | No effect — the two operations are aliases. |
| Returns `baseTableName` | **The update fails** with `8542`. |
| Omits `folderId` | No effect — Update cannot change the folder. |

The rule the server applies is: **Update rebuilds the report from exactly what you send; the read
reconstructs only the columns, operations, filters and filter values.**

Practical consequences:

1. **Keep your own copy of the CONFIG you sent to Create, and modify that.** It is the only complete
   record of the report.
2. **Never send `baseTableName` to Update.** Remove it from anything you assembled from a read (`8542`).
3. **Re-send every `filters` and `userFilters` entry you want to keep.** Omitting the array deletes it.
4. **`mergeAxisInfo` is not returned in write form.** The read returns one merge object repeated, with `axisIndex` as stored — see [`mergeAxisInfo` on Read](#mergeaxisinfo-on-read). Rebuild `mergeAxisInfo` from your own copy of the Create CONFIG.

### Values that change across a round trip

The read reconstructs every value from storage. Where several inputs share one stored form, the read
always returns the **same** one, listed below.

| Key | What the read returns |
|---|---|
| `title`, `baseTableName`, `columnName`, `tableName` | The object's current display name, in its stored casing. |
| `description` | The stored text. The key is **absent** when no description is stored. |
| `chartType` | One fixed name per stored chart — the *Returned on read* column of [`chartType` Values](#charttype-values). |
| `axisColumns[].type` | Lowercase: `xaxis`, `yaxis`, `coloraxis`, `textaxis`, `sizeaxis`, `latlng`, `tooltip`, `row`, `column`, `data`, `groupby`, `summarize`. All are valid on write. |
| `axisColumns[].operation` | See [Axis Operations on Read](#axis-operations-on-read). |
| `filters[].operation` | Numeric: `actual` for `measure` / `dimension` / `actual`; `std` for `std` / `stddev`; `aggregate` for `variance` / `dc` / `distinctcount` / `aggregate`; otherwise the operation sent. Text `actual`: `actual`. Text `count` / `dc` / `distinctcount`: stored as numeric filters and returned as `count` / `aggregate`. Date: `actual` for `actual` / `range` / `daterange`; `seasonal`; `relative`. |
| `filters[].filterType` | Numeric: `individualvalues`, `range`, `ranking`, `rankingpct`. Text: `individualvalues` (also for `individual`), `wildcard`. Date — absolute and seasonal filters: `year` (also for `common`), `quarteryear` (for every quarter type), `absmonth` (for every month type), `week` (for `weekyear` / `absweek` / `week`), `date` (for `fulldate` / `date`), `datetime`, `daterange` (also for `range`), `weekday`, `day`, `hour`. Relative filters: `year`. A seasonal `quarter` / `month` filter therefore reads back with an absolute-looking `filterType`; keep your own copy of the original `filterType`. |
| `filters[].values` | The stored display text split on commas, each piece trimmed, empty pieces dropped. **A value containing a comma is split into several values.** |
| `filters[].exclude` | Boolean. |
| `userFilters[].operation` | Text: `actual`. Numeric: `actual`, `sum`, `min`, `max`, `average`, `std`, `count`, `distinctcount`. Date: `year`, `absquarter`, `absmonth`, `absweek`, `fulldate`, `datetime`, `range`, or the string `"null"` for seasonal day / hour / weekday and relative filters. **None of the date values is a valid write `operation`** (`actual`, `seasonal`, `relative`, `dateRange`) — re-submitting raises `8166`. |
| `reportType` | `chart`, `pivot`, `summary`, or `widget` for widget views. `widget` is rejected on write with `8509`. |

#### Axis Operations on Read

| Stored operation | Returned `operation` |
|---|---|
| Text group by | `actual` |
| `geo` | `geo` on a Text column; `actual` on a Numeric column |
| `count` | `count` |
| `dc` / `distinctcount` (Text, Numeric or Date column) | `distinctcount`, with the source column's `columnName` |
| `variance` | `variance`, with the source column's `columnName` |
| Date distinct-count variants `ydc`, `qydc`, `mydc`, `wydc`, `ddc`, `dtdc`, `qdc`, `mdc`, `wdc`, `wddc`, `dmdc`, `hdc` | The same name, with the source column's `columnName` |
| Aggregate formula column | `actual` |
| Numeric `sum`, `min`, `max`, `stddev`, `median`, `mode`, `percentile` | The same name |
| Numeric `average` / `avg` | `average` |
| Numeric `measure`, `dimension`, `range` | The same name |
| Date `year`, `quarter`, `month`, `week`, `weekday`, `day`, `hour`, `fulldate`, `datetime` | The same name |
| Date `quarteryear` / `absquarter` | `quarteryear` |
| Date `monthyear` / `absmonth` | `absmonth` |
| Date `weekyear` / `absweek` | `weekyear` on chart shelves; `absweek` on pivot `row` / `column` and summary `groupBy` |

#### `mergeAxisInfo` on Read

For a chart with `isAxisMerge: true`, `mergeAxisInfo` is a JSONArray holding **one merge object,
repeated** once for each stored merge property (merge configuration, axis labels, chart description).
Read the first entry; ignore the rest. The object contains:

| Field | Type | Description |
|-------|------|-------------|
| `axisIndex` | String or JSONArray of Integer | When a merge configuration is stored: the stored configuration as a **string**, for example `"[[2,3],[4]]"` — a JSON array of groups of 1-based `axisColumns` positions, including each un-merged Y-axis column as a one-entry group. Otherwise: a JSONArray of the positions of all Y-axis columns. |
| `labelName` | String | The label of a merge group. When several groups have labels, only **one** label is returned. Absent when no label is stored. |
| `description` | String | The chart description set in the Zoho Analytics UI. Absent when none is stored. |

`mergeAxisInfo` is absent when `isAxisMerge` is `false`.

---

## Limitations

These are the limits that apply with **default settings**.

| Limitation | Value | Enforced by |
|------------|-------|-------------|
| **`CONFIG` size** | **10,000,000** characters, encoded. | `8507` |
| **`axisColumns` entries** | **1–1000.** | `8052` |
| **Y-axis columns per chart** | **15.** | `7727` |
| **`filters` entries** | **0–1000.** | `8052` |
| **`userFilters` entries** | **0–1000.** | `8052` |
| **`mergeAxisInfo` entries** | **10.** Rejected by the request schema. | — |
| **`wildcard.criteria` entries** | **1–15.** | `8547` / `8179` |
| **Serialised `values` / `defaultFilterValues` array** | **1,000** characters per array. | `8507` |
| **`title`** | **100** characters. | `8507` |
| **`description`** | **250** characters. | `8507` |
| **`chartType`** | **50** characters, letters, digits and spaces only. | `8507` / `8509` |
| **Static wildcard filters on Update** | **Not possible.** | `8192` |
| **Moving or re-basing a report** | **Not possible** through these APIs. | `8145` / `8542` |

> **`axisColumns` counts every entry,** including tooltip and colour columns. The 15-column Y-axis limit
> counts entries whose `type` is a Y axis only.

---

## Permission Model

| Role | Create Report | Read Report Metadata | Update Report |
|------|---------------|----------------------|---------------|
| Account Admin / Organization Admin / Workspace Owner / Workspace Admin | Yes — `folderId` honoured. | Yes | Yes |
| Report owner | — | Yes | Yes |
| Custom role with **Create Report** on the base table | Yes — `folderId` honoured. Without the permission: `7324`. | Only with **Design Modify** on the report. | **No** — `7301`. |
| Shared / group user with **Create Report** permission | Yes — **`folderId` is ignored**; the report appears under the caller's *My Reports*. | Only with **Design Modify** on the report. | **No** — `7301`, even with Design Modify. |
| Read-only shared user | No — `7301`. | No — `7301`. | No — `7301`. |

Every caller must also be able to read the base table and every column the report uses (`7301` for the
table, `7725` for a column).

---

## 1. Create Report

Builds a new chart, pivot or summary view on an existing table and returns its view ID. Use the
returned `viewId` as `<report-id>` in [Read Report Metadata](#2-read-report-metadata) and
[Update Report](#3-update-report).

| Attribute | Value |
|-----------|-------|
| **Method** | POST |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/reports` |
| **OAuth Scope** | `ZohoAnalytics.modeling.create` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the workspace. |
| **Permission Required** | Account Admin, Organization Admin, Workspace Owner or Workspace Admin; a Custom Role user whose role grants **Create Report** on the base table; or a shared / group user holding **Create Report** permission. The caller must additionally be able to read the base table and every column the report uses. See [Permission Model](#permission-model). |
| **API Units** | 5 units per request — gateway action `CREATE_ANALYSISVIEW` (api-id `2031`), **METADATA** unit category. |
| **Frequency Limit** | 60 requests/minute shared across every **METADATA**-category call of the organisation. |

### CONFIG Parameters

CONFIG is **mandatory** for this API. It is sent as a form-encoded body parameter; maximum encoded size
10,000,000 characters.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `baseTableName` | String | **Yes** | — | Display name of the table or query table the report is built on, 1–100 characters. Matched **exactly and case-sensitively** (`7138` otherwise; `7137` when the name is not a table or query table). **Cannot be changed after creation.** |
| `title` | String | **Yes** | — | Report name, 1–100 characters (`8507` above 100). Leading and trailing spaces are trimmed. Whitespace-only raises `7016`. Must not match the name of any other object in the workspace — table, query table, report or dashboard (`7111`). Can be changed later with [Update Report](#3-update-report). |
| `reportType` | String (enum) | **Yes** | — | The report family, lowercase only (`8509` otherwise). **Cannot be changed after creation.** See [`reportType` Values](#reporttype-values). |
| `axisColumns` | JSONArray | **Yes** | — | The drop-field configuration, 1–1000 entries (`8052` above 1000). See [`axisColumns` Fields](#axiscolumns-fields). |
| `description` | String | No | — | Free-text description, max 250 characters. Stored as sent. |
| `folderId` | Long | No | The workspace's default folder | Folder to create the report in. Must be a folder of this workspace (`7362`). **Ignored** for shared / group users — see [Permission Model](#permission-model). **Cannot be changed later** through these APIs. |
| `chartType` | String (enum) | No | Chosen automatically | Applies to `chart` only. Matched case-insensitively; letters, digits and spaces only, max 50 characters. An unrecognised value raises `8144`. For `pivot` and `summary`, omit it: a valid value is ignored, an unrecognised value still raises `8144`. The 57 accepted values are listed in [`chartType` Values](#charttype-values) (Appendix E). |
| `isAxisMerge` | Boolean | No | `false` | Charts only. Merge Y-axis columns onto shared axes. Must be `true` whenever `mergeAxisInfo` contains an entry (`8050`). |
| `mergeAxisInfo` | JSONArray | No | — | Charts only. Up to 10 groups of Y-axis columns that share one axis. See [`mergeAxisInfo` Fields](#mergeaxisinfo-fields). |
| `filters` | JSONArray | No | — | Static filter criteria baked into the report, 0–1000 entries. See [`filters` Fields](#filters-fields). |
| `userFilters` | JSONArray | No | — | Interactive filter widgets shown to viewers, 0–1000 entries. See [`userFilters` Fields](#userfilters-fields). |

> **`chartType` is not checked against the shelves.** The server does not reject a chart type that
> cannot be drawn from the supplied `axisColumns`; the type is saved as sent and the renderer falls back
> to a compatible chart when the report is opened. Choose a chart type whose shelves your `axisColumns`
> fill.

#### `reportType` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `chart` | A chart. | Needs a shelf combination that forms a drawable chart — at minimum one X-axis and one Y-axis column for most chart types (`7701`). |
| `pivot` | A pivot table. | Needs at least one `row`, `column` or `data` column (`7706`). |
| `summary` | A summary view. | Needs at least one `groupBy` or `summarize` column (`7705`). |

#### `axisColumns` Fields

Each entry places one column on one shelf.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `type` | String (enum) | **Yes** | — | The shelf. Only the exact spellings in [Axis Type Values](#axis-type-values) are accepted (`8509`); a valid spelling used with the wrong `reportType` raises `8170`. |
| `columnName` | String | **Yes** | — | Column display name, max 1000 characters. Matched **case-insensitively**. An unknown name raises `8050`. |
| `operation` | String (enum) | **Yes** for table columns | — | Aggregation or date grouping, letters only, matched case-insensitively. Ignored for aggregate formula columns. See [Axis Operation Values](#axis-operation-values) (`8166` for an operation not valid for the column and shelf). |
| `tableName` | String | No* | Base table | Display name of the table owning the column, max 100 characters, matched **exactly**. A table not joined to the base table raises `8059`. |
| `displayName` | String | No | — | Max 250 characters. Chart: the axis label shown for this column. Pivot / summary: the column header. |
| `sort` | String (enum) | No | — | `asc` or `desc`, lowercase (`8509` otherwise). **Chart and summary:** only the first entry in `axisColumns` that carries `sort` is applied; later `sort` keys are ignored. **Pivot:** applied on every entry that carries it. |
| `rangeSize` | Number | No* | — | Bin width, a JSON number greater than `0`. Allowed only when `operation` is `range` on a Numeric column (`8162` otherwise). |
| `geoRole` | String (enum) | No* | — | Geographic role, used with `operation: "geo"`. See [Geo Role Values](#geo-role-values). |
| `windowFunction` | JSONObject | No | — | Max 1000 characters. Running total, percentage, difference or moving calculation on a measure. See [`windowFunction` Fields](#windowfunction-fields). |

\* `tableName` is required when the column belongs to a table joined to the base table. `rangeSize`
applies only to `range`. `geoRole` is required when `operation` is `geo` on a Plain Text or Number
column.

#### `windowFunction` Fields

A window function can be attached to an `axisColumns` entry that holds a **measure**:

| Report | Entries that accept `windowFunction` |
|---|---|
| `chart` | Numeric column with any operation except `dimension` and `range`; Text column with `count`, `dc` or `distinctcount`; Date column with `count`, `distinctcount` or a date distinct-count variant; numeric aggregate formula column. |
| `pivot` | An entry on the `data` shelf holding a Numeric column, a Text column, a Date column with `count`, or a numeric aggregate formula column. |
| `summary` | None. `windowFunction` is ignored. |

On any other entry, `windowFunction` is ignored.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `type` | String (enum) | **Yes** | — | The calculation, matched case-insensitively (`8169` otherwise). See [Window Function Type Values](#window-function-type-values). |
| `baseField` | String | No* | — | Name of the reference column. Required by every type marked *Needs base field* (`8253`). See [Base Field Rules](#base-field-rules). |
| `baseFieldPosition` | String (enum) | No* | — | Shelf of `baseField` in this report, matched case-insensitively. Required whenever `baseField` is required (`8051`). Chart: `xAxis`, `yAxis`, `colorAxis`, `textAxis`, `latLng`, `toolTip`, `sizeaxis`. Pivot: `row`, `column`, `data`. |
| `baseTable` | String | No | Table of the measure column | Table owning `baseField`. See [Base Field Rules](#base-field-rules). |
| `baseFunction` | String | No | — | `operation` of the `baseField` entry. See [Base Field Rules](#base-field-rules). |
| `percentileVal` | Integer | No | `50` | 0–100 (`8544` otherwise). Used only when the entry's `operation` is `percentile`. |
| `movingCalculation` | JSONObject | No* | — | Required when `type` is `movingcalc` (`8051`). See [`movingCalculation` Fields](#movingcalculation-fields). |

\* `baseField` and `baseFieldPosition` are required for `runtotal`, `difffrom`, `pctofprevval`,
`pctdifffrom`, `hundredpctgrp` and `movingcalc`. `movingCalculation` is required for `movingcalc`.

#### `movingCalculation` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `calculation` | String (enum) | **Yes** | — | `average`, `sum`, `min` or `max`, case-insensitive (`8169` otherwise). |
| `previous` | Integer | **Yes** | — | Number of preceding values in the window. |
| `next` | Integer | **Yes** | — | Number of following values in the window. |
| `includeCurrent` | Boolean | **Yes** | — | Include the current value in the window. |
| `includeNull` | Boolean | **Yes** | — | Include null values in the window. |

##### Base Field Rules

- The base field must itself be an entry in `axisColumns`, placed on the shelf named by
  `baseFieldPosition`, and it must be a **dimension**:
  - Chart: a Text column with `operation` `actual` or `geo`, or a Date column with a grouping
    operation (not `count` or a distinct count).
  - Pivot: any entry on the `row` or `column` shelf.
- A base field that is not a dimension entry in `axisColumns` raises `8057`; one placed on a different
  shelf from `baseFieldPosition` raises `8058`.
- When `baseTable` is omitted, `baseField` is looked up in the same table as the measure column.
- When **all four** of `baseField`, `baseTable`, `baseFieldPosition` and `baseFunction` are supplied,
  the base field is located by matching an `axisColumns` entry whose `tableName`, `columnName`,
  `operation` and `type` equal `baseTable`, `baseField`, `baseFunction` and `baseFieldPosition`
  **exactly** (case-sensitive). Every `axisColumns` entry up to and including the matching one must
  carry both `tableName` and `operation`; if an earlier entry lacks either, or no entry matches, the call
  fails with `8051`.

#### `mergeAxisInfo` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `axisIndex` | JSONArray of Integer | **Yes** | — | **1-based positions in the `axisColumns` array** of the columns to merge (the first entry of `axisColumns` is `1`). Each value 0–100. An empty array makes the entry a no-op. |
| `labelName` | String | No | — | Max 250 characters. Label of the merged axis. |

Every position must point at an entry whose `type` is a Y axis (`yaxis`, `yAxis`, `YAxis`); every column
in one group must be a measure — a Numeric column with an aggregate operation, or a `count` / distinct
count of any column — and all columns in a group must be of the same kind. Each violation raises
`8050`.

#### `filters` Fields

Static criteria applied every time the report renders. Viewers cannot change them.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `columnName` | String | **Yes** | — | Column to filter on, max 1000 characters, matched case-insensitively. |
| `operation` | String (enum) | **Yes** | — | How the column is interpreted before the criteria is applied. See [Static Filter Operation and Type Values](#static-filter-operation-and-type-values). Required even for aggregate formula columns (send `aggregate`). |
| `filterType` | String (enum) | **Yes** | — | Shape of the criteria. See [Static Filter Operation and Type Values](#static-filter-operation-and-type-values). Required even where its value is not used (`relative` date filters — send `common`). |
| `values` | JSONArray of String | **Yes** | — | Criteria values. Format depends on `filterType` — see [Filter Value Formats](#filter-value-formats). Serialised array limited to 1,000 characters. Send `[]` for `wildcard` filters. |
| `exclude` | Boolean | **Yes** | — | `true` excludes the listed values, `false` includes them. Must be a JSON boolean. |
| `tableName` | String | No* | Base table | Table owning the column, max 1000 characters, matched exactly. A table not joined to the base table raises `8059`. |
| `rankingColumn` | String | No | — | Used only with `filterType: "ranking"` on a Numeric column: the Text or Date column (in the same table) whose members are ranked by the filtered measure. A Numeric ranking column raises `8055`. |
| `rankingColumnDateSubType` | String (enum) | No | `year` | Used only when `rankingColumn` is a Date column: `year`, `quarter`, `month`, `week`, `date` or `datetime`. |
| `wildcard` | JSONObject | No* | — | Required when `filterType` is `wildcard` (`8051`). See [`wildcard` Fields](#wildcard-fields). |

\* `tableName` is required for columns of joined tables. `wildcard` is required for `filterType:
"wildcard"`.

#### `wildcard` Fields

Text columns with `operation: "actual"` only. **Create only** — Update rejects wildcard filters with
`8192`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `criteria` | JSONArray | **Yes** | — | 1–15 entries (`8179` when empty). Each is `{"operation": "<op>", "value": "<text>"}`, both keys mandatory; `value` max 5,000 characters. See [Wildcard Operation Values](#wildcard-operation-values). |
| `expression` | String | **Yes** | — | How the criteria combine, max 100 characters. Must match the pattern `^\(\s*(\d+\s*(OR\|AND)\s*)*\d+\s*\)$` (`8509` otherwise): wrapped in one pair of parentheses, criteria referenced by 1-based index, each index used exactly once, in ascending order, for example `"(1 AND 2 OR 3)"`. Indexes out of order raise `8187`; an index count different from the criteria count raises `8188`. |

#### `userFilters` Fields

Interactive filter widgets rendered alongside the report. The rules depend on the column category and,
for dates, on `operation` — see [User Filter Rules by Column](#user-filter-rules-by-column).

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `columnName` | String | **Yes** | — | Column to expose, max 1000 characters, matched case-insensitively. |
| `tableName` | String | No* | Base table | Table owning the column, matched exactly. A table not joined to the base table raises `8059`. |
| `operation` | String (enum) | Conditional | — | See [User Filter Rules by Column](#user-filter-rules-by-column). |
| `compType` | String (enum) | Conditional | — | Widget type: `singleSelect`, `multiSelect`, `slider` or `dateRange`, exact case (`8509` otherwise). A missing required `compType` raises `8253`; a `compType` not valid for the column raises `8250`. |
| `filterType` | String (enum) | Conditional | — | Criteria shape. See [User Filter Rules by Column](#user-filter-rules-by-column). |
| `isallval` | Boolean | No | Derived from `values` | `true`: the widget lists all values and `values` is ignored. `false`: the widget is restricted to `values`, which must be non-empty (`8050`). Omitted: `false` when `values` is non-empty, `true` otherwise. |
| `values` | JSONArray of String | Conditional | — | Selectable values. Required when `isallval` is `false`. Serialised array limited to 1,000 characters. |
| `defaultFilterValues` | JSONArray of String | No | — | Values pre-selected when the report opens. At most 1 value unless `compType` is `multiSelect` (`8166`). Validated with the same rules as `values`; need not be a subset of `values`. May not contain `Others` or more than one `${...}` variable (`8166`). A range-picker default may also be `"from <date>"` or `"to <date>"`. |
| `exclude` | Boolean | No | `false` | `true` makes the widget exclude the selected values. Not allowed on a range picker (`8050`). |
| `behaviour` | String (enum) | No | — | Which values the widget lists when other filters are applied: `ListAllValues`, `ListRelevantValues` or `ListOnlyRelevantValues`, exact case. Not allowed on `slider`, `dateRange` or `relative` user filters (`8008`). |

\* `tableName` is required for columns of joined tables.

### Sample Requests

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

### Sample Responses

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

### Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary: `"Create Chart View"`, `"Create Pivot View"` or `"Create Summary View"`, by `reportType`. |
| `data` | JSONObject | Response payload wrapper. |
| `data.viewId` | String | ID of the new report, serialised as a **string**. **Always present** on success. Use it as `<report-id>`. |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Not idempotent** | Every successful call creates a new report. Repeating a call with the same `title` fails with `7111` (or `8201` while the first call is still being saved). |
| **All-or-nothing** | The create is transactional: when any error is returned, no report is created. |
| **Case sensitivity** | `baseTableName` and `tableName` are matched exactly. `columnName`, `chartType`, `operation` (except date filter operations) and window-function names are case-insensitive. `reportType`, axis `type`, `sort`, `geoRole`, `compType` and `behaviour` must be sent exactly as documented. |
| **`chartType` versus shelves** | Not validated — see the note under [CONFIG Parameters](#config-parameters). |
| **`sort`** | Chart and summary reports apply only the first `sort` in `axisColumns`. |
| **`folderId` for shared users** | Ignored without error — see [Permission Model](#permission-model). |
| **Write-only fields** | `folderId`, `displayName`, `sort`, `rangeSize`, `windowFunction`, `geoRole`, `wildcard`, `rankingColumn`, `rankingColumnDateSubType` and every user-filter key except `columnName`, `tableName` and `operation` are never returned by [Read Report Metadata](#2-read-report-metadata). |
| **Client Portal / White Label** | Not available on Client Portal / White Label domains. Call the standard API host. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | Workspace list → `<workspace-id>` and `orgId`; the workspace's view list → `baseTableName`, column names, `folderId` → Create Report → `data.viewId` → [Read Report Metadata](#2-read-report-metadata) / [Update Report](#3-update-report). |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7016 | `OBJECT_NAME_EMPTY` — `title` is empty or whitespace-only. | Supply a non-empty `title`. |
| 7103 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| 7111 | `META_DBOBJECT_NAME_DUPLICATED` — An object with this `title` already exists in the workspace. | Choose a `title` not used by any table, report or dashboard in the workspace. |
| 7137 | `NOT_A_TABLE` — `baseTableName` names an object that is not a table or query table. | Use a table or query table. |
| 7138 | `META_OBJECT_NOT_PRESENT` — `baseTableName` does not match a table in this workspace (matching is case-sensitive). | Use the exact table display name. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller cannot read the base table, or lacks Create Report permission on the workspace. | Call as a user with Create Report permission and read access to the base table. |
| 7309 | `SECURITY_NEEDS_LOGIN` — `Authorization` header absent. | Send `Authorization: Zoho-oauthtoken <token>`. |
| 7324 | `PERMISSION_DENIED_FOR_DOMAINUSER` — A Custom Role user's role does not grant Create Report on the base table. | Grant Create Report in the role. |
| 7362 | `NO_SUCH_FOLDER_IN_DB` — `folderId` does not exist in the workspace. | Supply a folder ID of this workspace, or omit `folderId`. |
| 7701 | `DROP_X_Y` — The chart's shelves do not form a drawable chart; typically no X-axis or no Y-axis column. | Add the missing shelf. |
| 7703 | `REMOVE_CLR_FIELD` — Multiple Y-axis columns in a shelf combination that does not support them, typically with a `colorAxis` column or with no X-axis column. | Drop the colour axis, add an X axis, or reduce to one Y axis. |
| 7705 | `DROP_SUMMARY` — A summary report has no `groupBy` and no `summarize` column. | Add at least one. |
| 7706 | `DROP_PIVOT` — A pivot report has no `row`, `column` or `data` column. | Add at least one. |
| 7725 | `ILLEGAL_COLUMN` — The caller is not permitted to access a column used in the report. | Share the column with the caller, or remove it. |
| 7727 | `Y_EXCEED_LIMIT` — More than 15 Y-axis columns on a chart. | Reduce to 15 or fewer. |
| 8008 | `UNKNOWN_PARAMETER` — `behaviour` was supplied on a `slider`, `dateRange` or `relative` user filter. | Remove `behaviour` from that user filter. |
| 8050 | `INVALID_VALUE` — A value is invalid: an unknown column name; an explicit `null` for any key; an empty `columnName`; a `mergeAxisInfo` rule violation; `mergeAxisInfo` without `isAxisMerge: true`; `isallval: false` with no `values`; an invalid user-filter `operation` or `filterType`; `exclude: true` on a range-picker user filter. | Check names and values against this document. |
| 8051 | `VALUE_NOT_PRESENT` — A mandatory key is missing: `title`, `reportType`, `axisColumns`, an axis `type` or `operation`, a filter's `filterType`, `values`, `exclude` or `operation`, `windowFunction.type`, `baseFieldPosition`, `movingCalculation` or one of its keys, a `wildcard` object, `mergeAxisInfo[].axisIndex`; or the four-key base-field lookup found no matching entry. | Add the missing key. |
| 8052 | `COLUMN_COUNT_EXCEEDED` — More than 1000 entries in `axisColumns`, `filters` or `userFilters`. | Reduce the array size. |
| 8053 | `AGGREGATE_COLUMN_INVALID_FIELD` — In a pivot or summary report, an aggregate formula column is placed on `row`, `column` or `groupBy`. | Place it on `data` or `summarize`. |
| 8055 | `NUMERIC_RANKING_COLUMN` — `rankingColumn` names a Numeric column. | Use a Text or Date column. |
| 8056 | `NOT_ALLOWED` — `pctoftotal` on an `average`, `stddev`, `variance`, `dc` or `distinctcount` column, or on an aggregate formula. | Choose another window function type. |
| 8057 | `NOT_ALLOWED_BASEFIELD` — `windowFunction.baseField` is not a dimension entry of `axisColumns`. | Add the base field to `axisColumns` as a dimension. |
| 8058 | `BASEFIELD_INVALID_AXIS` — `windowFunction.baseField` sits on a different shelf from `baseFieldPosition`. | Correct `baseFieldPosition`. |
| 8059 | `UNRELATED_TABLE` — A `tableName` is not a table joined to the base table. | Use a table reachable from the base table. |
| 8144 | `INVALID_GRAPH_TYPE` — `chartType` is not a value from [`chartType` Values](#charttype-values). | Use an accepted chart type, or omit `chartType`. |
| 8162 | `RANGE_SIZE_NOT_SUPPORTED_FOR_THIS_OPERATION` — `rangeSize` was supplied on an operation other than `range`. | Use `rangeSize` only with `operation: "range"`. |
| 8164 | `FILTER_COLUMN_DATATYPE_MISMATCH` — A numeric `individualvalues` filter value is not a valid number for the column. | Send the exact stored numeric value. |
| 8166 | `INVALID OPERATION FOR THE COLUMN` — The `operation` is not valid for the column's category and shelf; or a `defaultFilterValues` entry is invalid. | See [Axis Operation Values](#axis-operation-values) and [Static Filter Operation and Type Values](#static-filter-operation-and-type-values). |
| 8167 | `INVALID FILTER TYPE FOR THE GIVEN OPERATION` — The `filterType` is not valid for the column category and `operation`. | See [Static Filter Operation and Type Values](#static-filter-operation-and-type-values). |
| 8168 | `INVALID CRITERIA FORMAT FOR THE COLUMN` — A `values` entry does not match the format for its `filterType`. | See [Filter Value Formats](#filter-value-formats). |
| 8169 | `INVALID WINDOW TYPE FOR THE COLUMN` — `windowFunction.type` or `movingCalculation.calculation` is not a valid value. | See [Window Function Type Values](#window-function-type-values). |
| 8170 | `INVALID AXIS TYPE FOR THE REPORT` — An axis `type` is not valid for the chosen `reportType`. | See [Axis Type Values](#axis-type-values). |
| 8179 | `ADVFILTER_EXPRESSION_NO_CRITERIAS` — `wildcard.criteria` is empty. | Supply 1–15 criteria. |
| 8187 | `ADVFILTER_EXPRESSION_ORDER_CHANGE` — Criteria indexes in `wildcard.expression` are out of order. | Reference criteria as 1, 2, 3 … in order. |
| 8188 | `ADVFILTER_EXPRESSION_LENGTH_MISMATCH` — The number of indexes in `wildcard.expression` differs from the number of criteria. | Reference every criterion exactly once. |
| 8201 | `DUPL_DISPLAY_NAME` — Another report with the same `title` is being created at the same moment. | Retry with a unique `title`. |
| 8250 | `INVALID_UF_COMP_TYPE` — `compType` is not valid for the column category or operation. | See [User Filter Rules by Column](#user-filter-rules-by-column). |
| 8251 | `INCORRECT_DATE_VALUE` — A date in a date-range static filter could not be parsed. | Use the date formats in [Filter Value Formats](#filter-value-formats). |
| 8253 | `REQUIRED PARAM IS MISSING` — A required key is missing: `windowFunction.baseField`, user-filter `compType`, or user-filter `filterType` where [User Filter Rules by Column](#user-filter-rules-by-column) marks it required. | Add the key. |
| 8254 | `INVALID_VALUE_FOR_ATTRIBUTE_FOR_COLUMN` — `latitude` / `longitude` on a text column, or a place role on a numeric column. | See [Geo Role Values](#geo-role-values). |
| 8255 | `INVALID_KEY_GIVEN` — `operation: "geo"` on a column type that cannot be geocoded. | Use a Plain Text, Number, Positive Number, Decimal Number or Geo column. |
| 8256 | `GEO_COL_COUNT_EXCEEDED` — More than one text geo column on X, or more than one numeric geo column on one axis. | Keep one geo column per axis. |
| 8257 | `GEO_COL_COUNT_EXCEEDED_CATEGORICAL` — A text geo column on X coexists with a numeric geo column on Y. | Use one or the other. |
| 8258 | `GEO_COL_CATEGORY_ONLY_X` — A text geo column was placed on a shelf other than X. | Move it to `xAxis`. |
| 8504 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` is missing, or `baseTableName` is absent. | Send `CONFIG` with `baseTableName`. |
| 8507 | `MORE_THAN_MAX_LENGTH` — A string exceeds its limit: `title` 100, `description` 250, `chartType` 50, axis `displayName` 250, `columnName` 1000, axis `tableName` 100, `windowFunction` object 1000, serialised `values` / `defaultFilterValues` array 1000. | Shorten the value. |
| 8509 | `PATTERN_NOT_MATCHED` — A value does not match its pattern: `reportType: "Chart"`, `type: "sizeAxis"`, `sort: "descending"`, a `chartType` with a hyphen, `compType: "multiselect"`, a wildcard `expression` without parentheses, a wildcard `operation` in lowercase. | Use the exact accepted values. |
| 8516 | `UNABLE_TO_PARSE_DATA_TYPE` — A numeric value could not be parsed, for example `rangeSize` sent as an array. | Send a plain number. |
| 8517 | `DATATYPE_NOT_MATCHED` — A value has the wrong JSON type: `exclude: "yes"`, `isAxisMerge: 1`, `folderId: "abc"`. | Use JSON booleans, numbers and strings as documented. |
| 8534 | `JSON_PARSE_ERROR` — `CONFIG` is not valid JSON, or a key has the wrong structure (`axisColumns` as `{}`, `values` as a string, `mergeAxisInfo` as an object). | Arrays must be `[]`, objects `{}`. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |
| 8542 | `EXTRA_KEY_FOUND_IN_JSON` — A key not listed in this document is present. | Remove the key. |
| 8544 | `OUT_OF_RANGE` — An integer is outside its range: `percentileVal` outside 0–100, a `mergeAxisInfo` index outside 0–100. | Use a value inside the range. |
| 8547 | `ARRAY_SIZE_OUT_OF_RANGE` — More than 15 entries in `wildcard.criteria`. | Reduce the array size. |
| 14037 | `DISABLED_COLUMNS_USED` — A disabled column is used in the report. | Enable the column, or remove it. |

---

## 2. Read Report Metadata

Returns a summary of the stored definition of a chart, pivot or summary view. The `<report-id>` comes
from [Create Report](#1-create-report) (`data.viewId`) or from the workspace's view list.

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/reports/<report-id>/metadata` |
| **OAuth Scope** | `ZohoAnalytics.modeling.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the workspace. |
| **Permission Required** | The report's owner, or a user holding **Design Modify** on the report: Account Admin, Organization Admin, Workspace Owner, Workspace Admin, or a shared / group / Custom Role user granted edit rights. A read-only shared user cannot call this endpoint. |
| **API Units** | 0.1 units per request — gateway action `GET_REPORT_METADATA` (api-id `3052`), **METADATA** unit category. |
| **Frequency Limit** | 60 requests/minute shared across every **METADATA**-category call of the organisation. |

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

### Sample Requests

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

### Sample Responses

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

### Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get analysis view metadata"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.reportConfig` | JSONObject | The stored definition. **Always present** on success. |
| `data.reportConfig.title` | String | Report name. **Always present.** |
| `data.reportConfig.description` | String | Report description. **Absent** when no description is stored. |
| `data.reportConfig.reportType` | String | `chart`, `pivot`, `summary`, or `widget` for widget views. **Always present.** |
| `data.reportConfig.chartType` | String | Chart reports only, and only when the stored chart maps to a name — the *Returned on read* column of [`chartType` Values](#charttype-values). |
| `data.reportConfig.baseTableName` | String | Display name of the base table. **Always present.** |
| `data.reportConfig.isAxisMerge` | Boolean | Present when stored — always for charts created through [Create Report](#1-create-report). |
| `data.reportConfig.axisColumns` | JSONArray | Present when the report has axis columns. |
| `axisColumns[].type` | String | Lowercase shelf name — see [Values that change across a round trip](#values-that-change-across-a-round-trip). **Absent** for widget views. |
| `axisColumns[].columnName` | String | Column display name. For a distinct-count or variance column, the **source** column's name. |
| `axisColumns[].tableName` | String | Table display name. **Always present**, even when omitted on write. |
| `axisColumns[].operation` | String | See [Axis Operations on Read](#axis-operations-on-read). |
| `data.reportConfig.mergeAxisInfo` | JSONArray | Charts with `isAxisMerge: true` only. One merge object, repeated — see [`mergeAxisInfo` on Read](#mergeaxisinfo-on-read). |
| `data.reportConfig.filters` | JSONArray | Present when the report has static filters. |
| `filters[].tableName` | String | Table display name. |
| `filters[].columnName` | String | Column display name. |
| `filters[].operation` | String | See [Values that change across a round trip](#values-that-change-across-a-round-trip). |
| `filters[].filterType` | String | See [Values that change across a round trip](#values-that-change-across-a-round-trip). |
| `filters[].values` | JSONArray of String | The stored display text split on commas. |
| `filters[].exclude` | Boolean | Whether the filter excludes its values. |
| `data.reportConfig.userFilters` | JSONArray | Present when the report has user filters. |
| `userFilters[].tableName` | String | Table display name. |
| `userFilters[].columnName` | String | Column display name. |
| `userFilters[].operation` | String | See [Values that change across a round trip](#values-that-change-across-a-round-trip). |

No other key is returned.

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Lossy summary** | The response omits every write-only field and normalises many values. It is **not** an Update payload — see [Round-tripping a Report](#round-tripping-a-report). |
| **Merged-axis charts** | `mergeAxisInfo` is returned in read form, not write form — see [`mergeAxisInfo` on Read](#mergeaxisinfo-on-read). |
| **Read-only** | Safe to repeat; nothing is changed. |
| **Client Portal / White Label** | Not available on Client Portal / White Label domains. Call the standard API host. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Create Report](#1-create-report) → `data.viewId` (or the workspace's view list) → `<report-id>` → Read Report Metadata → `reportConfig` for inspection. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7103 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| 7104 | `META_OBJECT_NOT_PRESENT` — The report does not exist. | Verify `<report-id>`. |
| 7106 | `META_OBJECT_NOT_PRESENT` — The report has been deleted. | Verify `<report-id>`. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not the owner and lacks Design Modify permission on the report. | Grant the caller edit access to the report. |
| 7309 | `SECURITY_NEEDS_LOGIN` — `Authorization` header absent. | Send `Authorization: Zoho-oauthtoken <token>`. |
| 7319 | `OBJID_NOT_BELONGS_TO_DB` — The report belongs to a different workspace. | Make `<workspace-id>` and `<report-id>` consistent. |
| 8021 | `INVALID_VIEW_TYPE_IN_REQUEST` — The target is a table, query table or dashboard, not a report. | Use a report ID. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.read`. |

---

## 3. Update Report

Rebuilds an existing report from a fresh CONFIG and returns no body. The `<report-id>` comes from
[Create Report](#1-create-report) (`data.viewId`) or from the workspace's view list.

| Attribute | Value |
|-----------|-------|
| **Method** | PUT |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/reports/<report-id>` |
| **OAuth Scope** | `ZohoAnalytics.modeling.update` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the workspace. |
| **Permission Required** | The report's **owner**, an Account Admin, an Organization Admin, the Workspace Owner or a Workspace Admin. Any other caller — including a shared, group or Custom Role user holding Design Modify — is rejected with `7301`. The caller must also be able to read the base table. |
| **API Units** | 5 units per request — gateway action `UPDATE_ANALYSISVIEW` (api-id `2032`), **METADATA** unit category. |
| **Frequency Limit** | 60 requests/minute shared across every **METADATA**-category call of the organisation. |

### CONFIG Parameters

CONFIG is **mandatory** for this API. Maximum encoded size 10,000,000 characters. **Every call replaces
the whole definition** — omitted attributes are cleared, not kept.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `reportType` | String (enum) | **Yes** | — | Must equal the stored report's type (`8021` otherwise). See [`reportType` Values](#reporttype-values). |
| `axisColumns` | JSONArray | **Yes** | — | The complete new drop-field configuration, as in [`axisColumns` Fields](#axiscolumns-fields). Every axis-column key not re-sent is removed. |
| `description` | String | No | Cleared | Max 250 characters. **Omitting it clears the stored description** (stored as an empty string). |
| `chartType` | String (enum) | No | Chosen automatically | As in Create. Omitting it lets the server choose the chart type. |
| `isAxisMerge` | Boolean | No | `false` | As in Create. Omitting it turns axis merging off. |
| `mergeAxisInfo` | JSONArray | No | — | As in Create — see [`mergeAxisInfo` Fields](#mergeaxisinfo-fields). |
| `filters` | JSONArray | No | Cleared | As in Create — see [`filters` Fields](#filters-fields) — except that `filterType: "wildcard"` is rejected with `8192`. **Omitting it removes every static filter.** |
| `userFilters` | JSONArray | No | Cleared | As in Create — see [`userFilters` Fields](#userfilters-fields). **Omitting it removes every user filter.** |
| `title` | String | No | Stored name | New report name, 1–100 characters (`8507` above 100); empty or whitespace-only raises `7016`. Omitted → the stored name is kept. Sent → **the report is renamed.** Unlike Create, Update neither trims the name nor checks it for uniqueness: make sure no other object in the workspace has this name, otherwise two objects share it. |

> **Not accepted on Update:** `folderId` raises `8145` — even when it equals the report's current folder
> — and `baseTableName` raises `8542`. A report cannot be moved or re-based through this API.

### Sample Requests

**Case 1 — Change the chart type and re-sort (minimal)**

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
        {"type": "xAxis", "columnName": "Order Date", "operation": "monthyear"},
        {"type": "yAxis", "columnName": "Sales", "operation": "sum", "sort": "asc"}
    ]
}
```

**Case 2 — Widen a filter, keeping everything else**

`userFilters` has to be re-sent in full even though it is unchanged; omitting it would delete it.

```http
PUT /restapi/v2/workspaces/466206000000071000/reports/466206000000105001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "reportType": "chart",
    "chartType": "line",
    "description": "Monthly trend, excluding returns",
    "axisColumns": [
        {"type": "xAxis", "columnName": "Order Date", "operation": "monthyear"},
        {"type": "yAxis", "columnName": "Sales", "operation": "sum"}
    ],
    "filters": [
        {
            "columnName": "Status",
            "operation": "actual",
            "filterType": "individualvalues",
            "values": ["Returned", "Cancelled"],
            "exclude": true
        }
    ],
    "userFilters": [
        {
            "columnName": "Product Category",
            "operation": "actual",
            "compType": "multiSelect",
            "filterType": "individualvalues",
            "isallval": true
        }
    ]
}
```

**Case 3 — Strip all filters off a pivot**

```http
PUT /restapi/v2/workspaces/466206000000071000/reports/466206000000105002 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "reportType": "pivot",
    "axisColumns": [
        {"type": "row", "columnName": "Region", "operation": "actual"},
        {"type": "data", "columnName": "Sales", "operation": "sum"}
    ]
}
```

**Case 4 — Attempt to move the report to another folder (rejected)**

```http
PUT /restapi/v2/workspaces/466206000000071000/reports/466206000000105001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "reportType": "chart",
    "folderId": 466206000000094005,
    "axisColumns": [
        {"type": "xAxis", "columnName": "Order Date", "operation": "monthyear"},
        {"type": "yAxis", "columnName": "Sales", "operation": "sum"}
    ]
}
```

### Sample Responses

**HTTP 204 No Content — Report rebuilt (Cases 1–3)** — No response body is returned on success.

```
HTTP/1.1 204 No Content
```

**HTTP 406 Not Acceptable — `folderId` supplied (Case 4)**

```json
{
    "status": "failure",
    "summary": "FOLDERID_CANNOT_BE_UPDATED",
    "data": {
        "errorCode": 8145,
        "errorMessage": "Folder ID cannot be updated with analysisview API."
    }
}
```

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Full replacement** | The report is rebuilt from exactly what you send. There is no field-level patching. |
| **What omission clears** | `filters` → all static filters removed. `userFilters` → all user filters removed. `description` → cleared. `chartType` → chosen automatically. `isAxisMerge` → off. Every axis-column key not re-sent (`displayName`, `sort`, `rangeSize`, `geoRole`, `windowFunction`) → removed. The chart legend is reset to its default position and title. |
| **What is kept** | The report's ID, owner, folder, creation time and sharing — and its name when `title` is omitted. |
| **Arrays replace, never merge** | `axisColumns`, `filters`, `userFilters` and `mergeAxisInfo` replace the stored arrays wholesale. |
| **Idempotent** | Sending the same CONFIG twice produces the same report. |
| **All-or-nothing** | The update is transactional: when any error is returned, the report is unchanged. |
| **Renaming** | Sending `title` renames the report. Update performs no name-uniqueness check and no trimming, so `7111`, `8201` and `7362` never occur — check uniqueness yourself before renaming. |
| **Do not build the CONFIG from a read** | See [Round-tripping a Report](#round-tripping-a-report). |
| **Client Portal / White Label** | Not available on Client Portal / White Label domains. Call the standard API host. |
| **Dependency chain** | [Create Report](#1-create-report) → `data.viewId` → `<report-id>` → Update Report; keep the Create CONFIG as the base for the new CONFIG. |

### Error Codes

Update runs the same validation as [Create Report](#1-create-report), so every code in that table except
`7111`, `7137`, `7138`, `7324`, `7362`, `8201` and `8504` can be returned. The codes specific to Update,
or with different triggers:

| Code | Reason | Solution |
|------|--------|----------|
| 7103 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| 7106 | `META_OBJECT_NOT_PRESENT` — The report does not exist or has been deleted. | Verify `<report-id>`. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not the report's owner, an Account Admin, an Organization Admin, the Workspace Owner or a Workspace Admin. | Call as one of those users. |
| 7319 | `OBJID_NOT_BELONGS_TO_DB` — The report belongs to a different workspace. | Make `<workspace-id>` and `<report-id>` consistent. |
| 8021 | `INVALID_VIEW_TYPE_IN_REQUEST` — `reportType` does not match the stored report's type, or the target is not a report. | Send the report's actual `reportType`. |
| 8145 | `FOLDERID_CANNOT_BE_UPDATED` — `folderId` was supplied. | Remove `folderId`. |
| 8192 | `ADVFILTER_UPDATE_HANDLING` — A `filters` entry uses `filterType: "wildcard"`. | Wildcard filters can only be set at create time. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.update`. |
| 8542 | `EXTRA_KEY_FOUND_IN_JSON` — `baseTableName` or any other key outside the Update schema is present. | Remove the key. |

---

## Appendix A – Common HTTP Headers

| Header | Value | Required | Description |
|--------|-------|----------|-------------|
| `Authorization` | `Zoho-oauthtoken <oauth-token>` | **Mandatory** | OAuth 2.0 access token of the calling user. Must carry the scope matching the operation (see [Appendix B](#appendix-b--oauth-scope-summary)). Absent → `7309`; invalid or expired → `8535`. |
| `ZANALYTICS-ORGID` | Organization ID string | **Mandatory** | Organization ID of the workspace that owns the report. Obtainable from workspace listing responses as the `orgId` field. |
| `Content-Type` | `application/x-www-form-urlencoded` | Conditional | Required only for the APIs that send a CONFIG body: [Create Report](#1-create-report) and [Update Report](#3-update-report). [Read Report Metadata](#2-read-report-metadata) sends no payload. |
| `Host` | `analyticsapi.zoho.com` (or the data-centre equivalent) | **Mandatory** | The standard API host. Client Portal / White Label domains are not accepted by these APIs. |

> **`ZANALYTICS-DEST-ORGID` is not used by any API in this document.**

Example:

```http
POST /restapi/v2/workspaces/466206000000071000/reports HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"baseTableName":"Sales","title":"Sales by Region","reportType":"chart","chartType":"bar","axisColumns":[{"type":"xAxis","columnName":"Region","operation":"actual"},{"type":"yAxis","columnName":"Sales","operation":"sum"}]}
```

---

## Appendix B – OAuth Scope Summary

| API | HTTP Method | Scope |
|-----|-------------|-------|
| Create Report | POST | `ZohoAnalytics.modeling.create` |
| Read Report Metadata | GET | `ZohoAnalytics.modeling.read` |
| Update Report | PUT | `ZohoAnalytics.modeling.update` |

> All three APIs use the `ZohoAnalytics.modeling` scope group. Discovering the `<workspace-id>`, the
> base table name, column names and `folderId` uses the workspace and view listing APIs, which may
> require additional scopes — request them in the same consent.

---

## Appendix C – API-Specific Notes and Behaviours

### Create Report

- **`title` is effectively the identity.** It is mandatory (`8051`), must be unique across every object
  in the workspace (`7111`). It can be changed later with [Update Report](#3-update-report).
- **`chartType` is not checked against the shelves.** An incompatible chart type is saved as sent; the
  renderer falls back to a compatible chart when the report is opened.
- **Only the first `sort` counts in charts and summaries.** Put the `sort` on the column you want sorted
  and nowhere else.
- **Every chart window function except `normal` and `pctoftotal` needs a base field.** `runtotal`
  without `baseField` fails with `8253`.
- **`geoRole` is case-sensitive and mandatory on Plain Text and Number columns.** Send it lowercase.
- **Date filter `operation` values are case-sensitive.** `"Actual"` raises `8166`.
- **The range-picker user filter requires `operation: "dateRange"` exactly.** `range` and `daterange`
  are rejected.
- **Shared users cannot choose a folder.** `folderId` is ignored for them without error.
- **Dependency chain:** workspace list → `<workspace-id>` → view list → `baseTableName`, column names,
  `folderId` → Create Report → `data.viewId`.

### Read Report Metadata

- **It is an inspection endpoint, not an export.** The response omits every write-only key and
  normalises values — see [Round-tripping a Report](#round-tripping-a-report).
- **Merged-axis charts return `mergeAxisInfo` in read form** — one object repeated, `axisIndex` as stored.
  See [`mergeAxisInfo` on Read](#mergeaxisinfo-on-read).
- **Distinct-count and variance columns return the source column** with `distinctcount`, `variance` or
  the date distinct-count variant as `operation`.
- **`description` is absent, not empty,** when none is stored.
- **Dependency chain:** [Create Report](#1-create-report) → `data.viewId` → Read Report Metadata.

### Update Report

- **Full replacement, not a patch.** Omitting `filters`, `userFilters` or `description` clears them;
  omitting `chartType` lets the server choose; omitting `isAxisMerge` turns merging off.
- **Owner or admin only.** Shared, group and Custom Role users are rejected with `7301`, even with
  Design Modify permission.
- **`folderId` always fails** (`8145`), even when it equals the current folder.
- **`title` renames the report — without a uniqueness check.** Update does not trim the name and does
  not raise `7111`; check that no other object in the workspace uses the name before renaming.
- **Wildcard filters cannot be updated** (`8192`).
- **Dependency chain:** [Create Report](#1-create-report) → `data.viewId` and the Create CONFIG →
  Update Report.

---

## Appendix D – General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Which endpoints return 204** | [Update Report](#3-update-report) returns **204 No Content** with no body on success. |
| **Which endpoints return a body** | [Create Report](#1-create-report) returns `data.viewId`; [Read Report Metadata](#2-read-report-metadata) returns `data.reportConfig`. |
| **Failure responses always carry a body** | Even for the 204 API, errors return `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name, not a localised sentence. |
| **All IDs are strings** | `data.viewId` is serialised as a JSON **string** even though the value is numeric. Parse it as a string or long — never as a native JSON number — to avoid precision loss. |
| **Conditional keys** | In `reportConfig`, `description`, `chartType`, `isAxisMerge`, `axisColumns`, `filters` and `userFilters` are omitted when there is nothing stored; `mergeAxisInfo` appears only when `isAxisMerge` is `true`. |
| **Responses are extensible** | Some builds return additional fields. Ignore unrecognised keys rather than validating against a closed schema. |

---

## Appendix E – Enum and Value Reference

Consolidated lookup for every enum used by [Create Report](#1-create-report) and
[Update Report](#3-update-report). Values are listed exhaustively: a value not listed here is not
supported.

#### `chartType` Values

`chartType` is matched case-insensitively. Only letters, digits and spaces are allowed — no hyphens or
underscores. The accepted values are exactly the 57 below; any other value raises `8144`. Names in the
same *Equivalent names* group produce an identical stored chart, and [Read Report Metadata](#2-read-report-metadata) returns the name in the *Returned on read* column for all of them.

| Family | Accepted value | Equivalent names | Returned on read |
|---|---|---|---|
| Area | `area` | `area`, `area without points`, `area without markers` | `area` |
|  | `area without points` | ↑ | `area` |
|  | `area without markers` | ↑ | `area` |
|  | `area with points` | `area with points`, `area with markers` | `area with points` |
|  | `area with markers` | ↑ | `area with points` |
| Smooth area | `smooth area` | `smooth area`, `smooth area without points`, `smooth area without markers` | `smooth area without points` |
|  | `smooth area without points` | ↑ | `smooth area without points` |
|  | `smooth area without markers` | ↑ | `smooth area without points` |
|  | `smooth area with points` | `smooth area with points`, `smooth area with markers` | `smooth area with points` |
|  | `smooth area with markers` | ↑ | `smooth area with points` |
| Stacked area | `stacked area` | — | `stacked area` |
|  | `stacked area with points` | — | `stacked area with points` |
| Stacked smooth area | `stacked smooth area` | `stacked smooth area`, `stacked smooth area without points`, `stacked smooth area without markers` | `stacked smooth area` |
|  | `stacked smooth area without points` | ↑ | `stacked smooth area` |
|  | `stacked smooth area without markers` | ↑ | `stacked smooth area` |
|  | `stacked smooth area with points` | `stacked smooth area with points`, `stacked smooth area with markers` | `stacked smooth area with markers` |
|  | `stacked smooth area with markers` | ↑ | `stacked smooth area with markers` |
| Bar | `bar` | — | `bar` |
|  | `horizontal bar` | — | `horizontal bar` |
|  | `stacked bar` | — | `stacked bar` |
|  | `horizontal stacked bar` | — | `horizontal stacked bar` |
|  | `butterfly` | — | `butterfly` |
| Line | `line` | `line`, `line with points`, `line with markers` | `line` |
|  | `line with points` | ↑ | `line` |
|  | `line with markers` | ↑ | `line` |
|  | `line without points` | `line without points`, `line without markers` | `line without points` |
|  | `line without markers` | ↑ | `line without points` |
| Smooth line | `smooth line` | `smooth line`, `smooth line with points`, `smooth line with markers` | `smooth line` |
|  | `smooth line with points` | ↑ | `smooth line` |
|  | `smooth line with markers` | ↑ | `smooth line` |
|  | `smooth line without points` | `smooth line without points`, `smooth line without markers` | `smooth line without points` |
|  | `smooth line without markers` | ↑ | `smooth line without points` |
|  | `step` | — | `step` |
| Pie family | `pie` | — | `pie` |
|  | `ring` | — | `ring` |
|  | `semi pie` | — | `semi pie` |
|  | `semi ring` | — | `semi ring` |
|  | `funnel` | — | `funnel` |
|  | `pyramid` | — | `pyramid` |
| Bubble & scatter | `bubble` | — | `bubble` |
|  | `packed bubble` | — | `packed bubble` |
|  | `scatter` | — | `scatter` |
| Combo | `combo` | — | `combo` |
|  | `combo bar with smooth line` | — | `combo bar with smooth line` |
| Map | `map area` | `map area`, `map filled` | `map filled` |
|  | `map filled` | ↑ | `map filled` |
|  | `map bubble` | — | `map bubble` |
|  | `map pie` | — | `map pie` |
|  | `map pie bubble` | `map pie bubble`, `map bubble pie` | `map pie bubble` |
|  | `map bubble pie` | ↑ | `map pie bubble` |
|  | `map scatter` | — | `map scatter` |
|  | `geo heat map` | — | `geo heat map` |
| Web | `web` | `web`, `web with fill` | `web with fill` |
|  | `web with fill` | ↑ | `web with fill` |
|  | `web without fill` | — | `web without fill` |
| Other | `heat map` | — | `heat map` |
|  | `table chart` | — | `table chart` |

Not accepted (raise `8144`): `stacked area without points`, `stacked area without markers`,
`stacked area with markers`.

Omitting `chartType` makes the server choose a chart type automatically.

#### Axis Type Values

The `type` value in an `axisColumns` entry must be one of these exact spellings. Any other spelling raises
`8509`; a valid spelling used with the wrong `reportType` raises `8170`.

| Accepted spellings | Valid for | Notes |
|---|---|---|
| `xaxis`, `xAxis`, `XAxis` | `chart` | Primary dimension axis. |
| `yaxis`, `yAxis`, `YAxis` | `chart` | Measure axis. Maximum 15 (`7727`). |
| `textaxis`, `textAxis` | `chart` | Text / label axis. |
| `coloraxis`, `colorAxis` | `chart` | Colour-encoding axis. |
| `sizeaxis` | `chart` | Size-encoding axis for bubble charts. **Lowercase only** — `sizeAxis` is rejected with `8509`. |
| `latlng`, `latLng` | `chart` | Latitude / longitude pair for map charts. |
| `tooltip`, `toolTip` | `chart` | Extra columns surfaced in the tooltip. |
| `row` | `pivot` | Row grouping shelf. |
| `column` | `pivot` | Column grouping shelf. |
| `data` | `pivot` | Measure shelf. |
| `groupby`, `groupBy` | `summary` | Dimension grouping shelf. |
| `summarize` | `summary` | Aggregate shelf. |

A chart needs a shelf combination that forms a drawable chart — at minimum one X-axis and one Y-axis
column for most chart types (`7701`). A pivot needs at least one `row`, `column` or `data` column
(`7706`); a summary needs at least one `groupBy` or `summarize` column (`7705`).

#### Axis Operation Values

The valid `operation` for an `axisColumns` entry depends on the column category ([Column
categories](#column-categories)) **and** on the shelf. Operations are matched case-insensitively and must
contain letters only. Send only the operations listed here. An operation outside the list raises
`8166`, with one exception: on the pivot `row` / `column` and summary `groupBy` shelves the operation of
a Text column is not checked and is always treated as `actual`.

##### Chart (every chart shelf)

| Category | Accepted operations |
|---|---|
| Text | `actual` (group by value), `count`, `dc` (alias `distinctcount`), `geo` |
| Numeric | `sum`, `min`, `max`, `average` (alias `avg`), `stddev`, `median`, `mode`, `percentile`, `count`, `variance`, `dc` (alias `distinctcount`), `measure` (un-aggregated value), `dimension` (each value as a category), `range` (numeric bins; honours `rangeSize`), `geo` |
| Date | Grouping: `year`, `quarter`, `month`, `week`, `weekday`, `day`, `hour` (seasonal), `quarteryear` (alias `absquarter`), `monthyear` (alias `absmonth`), `weekyear` (alias `absweek`), `fulldate`, `datetime` (absolute). Aggregates: `count`, `distinctcount`, `ydc`, `qydc`, `mydc`, `wydc`, `ddc`, `dtdc`, `qdc`, `mdc`, `wdc`, `wddc`, `dmdc`, `hdc` |
| Aggregate formula | `operation` is not required and is ignored. |

`percentile` computes the percentile given by `windowFunction.percentileVal` (default 50).

##### Pivot

| Category | `row` / `column` | `data` |
|---|---|---|
| Text | `actual` | `count`, `dc` (alias `distinctcount`) |
| Numeric | `dimension`, `range` | `sum`, `min`, `max`, `average`, `stddev`, `median`, `mode`, `percentile`, `count`, `variance`, `dc` (alias `distinctcount`) |
| Date | The date grouping operations of the chart table | `count`, `distinctcount` and the date distinct-count variants of the chart table |
| Aggregate formula | Not allowed (`8053`) | `operation` ignored |

##### Summary

| Category | `groupBy` | `summarize` |
|---|---|---|
| Text | `actual` | `count`, `dc` (alias `distinctcount`) |
| Numeric | `dimension`, `range` | `sum`, `min`, `max`, `average`, `stddev`, `median`, `mode`, `percentile`, `count`, `variance`, `dc` (alias `distinctcount`) |
| Date | The date grouping operations of the chart table | `count`, `distinctcount` and the date distinct-count variants of the chart table |
| Aggregate formula | Not allowed (`8053`) | `operation` ignored |

> `avg` is accepted only in chart reports. Pivot and summary reports require `average`.

> `std` is **not** a valid axis operation — the standard-deviation operation is `stddev`. (`std` *is*
> accepted in `filters` and slider `userFilters`.)

**Date distinct-count variants** — the distinct count of the date column's values after truncating them
to the named unit:

| Operation | Distinct count of |
|---|---|
| `distinctcount` | Distinct date values |
| `ydc` | Years |
| `qydc` | Quarter-years |
| `mydc` | Month-years |
| `wydc` | Week-years |
| `ddc` | Full dates |
| `dtdc` | Date-times |
| `qdc` | Quarters (seasonal) |
| `mdc` | Months (seasonal) |
| `wdc` | Weeks (seasonal) |
| `wddc` | Weekdays |
| `dmdc` | Days of the month |
| `hdc` | Hours |

#### Window Function Type Values

`type` is matched case-insensitively. *Needs base field* means `baseField` and `baseFieldPosition` are
required — see [Base Field Rules](#base-field-rules).

##### Chart Window Function Types

| `type` | Calculation | Needs base field |
|---|---|:---:|
| `normal` | No calculation (plain value). | No |
| `pctoftotal` | Percentage of total. Not supported when the entry's `operation` is `average`, `avg`, `stddev`, `variance`, `dc` or `distinctcount`, or when the column is an aggregate formula. All of these except `avg` raise `8056`. | No |
| `runtotal` | Running total. | Yes |
| `difffrom` | Difference from the previous value. | Yes |
| `pctofprevval` | Percentage of the previous value. | Yes |
| `pctdifffrom` | Percentage difference from the previous value. | Yes |
| `hundredpctgrp` | 100 % within each group. | Yes |
| `movingcalc` (alias `movingcalculation`) | Moving calculation over a window of neighbouring values. | Yes |

##### Pivot Window Function Types

| `type` | Calculation | Needs base field |
|---|---|:---:|
| `normal` | No calculation (plain value). | No |
| `pctofrow` | Percentage of row total. | No |
| `pctofcol` | Percentage of column total. | No |
| `pctoftotal` | Percentage of grand total. | No |
| `pctofparrow` | Percentage of parent row total. | No |
| `pctofparcol` | Percentage of parent column total. | No |
| `runtotal` | Running total. | Yes |
| `difffrom` | Difference from the previous value. | Yes |
| `pctofprevval` | Percentage of the previous value. | Yes |
| `pctdifffrom` | Percentage difference from the previous value. | Yes |

#### Geo Role Values

`geoRole` is matched **case-sensitively** — send it in lowercase exactly as listed. Geo operations are
valid on chart reports only.

| Column type | Valid `geoRole` values | Placement |
|---|---|---|
| Plain Text | **Required**: `continent`, `country`, `state`, `province`, `county`, `district`, `city`, `zipcode`, `airport` | `xAxis` only (`8258` otherwise) |
| Number, Positive Number, Decimal Number | **Required**: `latitude`, `longitude` | Any chart shelf |
| Geo (column already typed with a geo role) | Optional. If sent, a value from the Plain Text row; the column's own role is used. | `xAxis` only (`8258` otherwise) |

Rules, each enforced with its own error:

- `geo` on a column type not listed above raises `8255`.
- `latitude` / `longitude` on a text column, or a place role on a numeric column, raises `8254`.
- At most **one** text geo column on the X axis, and at most **one** numeric geo column on each of the
  X and Y axes (`8256`).
- A text geo column on X and a numeric geo column on Y cannot coexist (`8257`).

#### Wildcard Operation Values

| Value | Meaning |
|-------|---------|
| `CONTAINS` | The value contains the text. |
| `DOES_NOT_CONTAIN` | The value does not contain the text. |
| `IS` | The value equals the text. |
| `IS_NOT` | The value does not equal the text. |
| `STARTS_WITH` | The value starts with the text. |
| `DOES_NOT_START_WITH` | The value does not start with the text. |
| `ENDS_WITH` | The value ends with the text. |
| `DOES_NOT_END_WITH` | The value does not end with the text. |

Uppercase only (`8509` otherwise).

#### Static Filter Operation and Type Values

| Column category | `operation` | `filterType` |
|---|---|---|
| Numeric | `measure`, `dimension`, `actual` (all three filter on the row value), `sum`, `min`, `max`, `average`, `stddev`, `std`, `count`, `median`, `mode`, `variance`, `dc`, `distinctcount`, `aggregate` | `individualvalues`, `range`, `ranking`, `rankingpct` |
| Text | `actual` | `individualvalues` (alias `individual`), `wildcard` |
| Text | `count`, `dc`, `distinctcount` | `individualvalues`, `range`, `ranking`, `rankingpct` (numeric formats) |
| Date — absolute | `actual` (aliases `range`, `daterange`) | `year`, `quarteryear` (aliases `absquarter`, `quarter`), `monthyear` (aliases `absmonth`, `month`), `weekyear` (aliases `absweek`, `week`), `fulldate` (alias `date`), `datetime`, `daterange` (alias `range`) |
| Date — seasonal | `seasonal` | `quarter`, `month`, `week`, `weekday`, `day`, `hour` |
| Date — relative | `relative` | Required, value not used — send `common` |
| Aggregate formula | Not used — send `aggregate` | `individualvalues`, `range`, `ranking`, `rankingpct` |

- `operation` and `filterType` are matched case-insensitively, **except** date `operation` values, which
  must be lowercase exactly as listed.
- An `operation` outside the list raises `8166`; a `filterType` outside the list raises `8167`.

#### User Filter Rules by Column

| Column / operation | `operation` | `compType` | `filterType` | `values` / `defaultFilterValues` format | `exclude` | `behaviour` |
|---|---|---|---|---|---|---|
| Text | Optional; if sent, `actual` | **Required**: `singleSelect` \| `multiSelect` | Optional; if sent, `individualvalues` | Any strings | Allowed | Allowed |
| Numeric — slider | **Required**: `sum` \| `min` \| `max` \| `avg` \| `std` \| `stddev` \| `count` \| `dc` \| `actual` | **Required**: `slider` | Not used | Not used — a slider always covers the full value range; `values` and `isallval` are ignored. Do not send `defaultFilterValues` (more than one value raises `8166`). | Allowed | **Not allowed** (`8008`) |
| Numeric — select list | Optional; if sent, `actual` | **Required**: `multiSelect` | **Required** when `isallval` is `false`: `individualvalues` \| `range` \| `ranking` \| `rankingpct` | As the numeric rows of [Filter Value Formats](#filter-value-formats) | Allowed | Allowed |
| Date — absolute | **Required**: `actual` | **Required**: `singleSelect` \| `multiSelect` | **Required**: `year` \| `quarteryear` \| `monthyear` \| `weekyear` \| `fulldate` \| `datetime` (aliases: `quarter` = `quarteryear`, `month` = `monthyear`, `week` = `weekyear`, `date` = `fulldate`) | As the absolute date rows of [Filter Value Formats](#filter-value-formats) | Allowed | Allowed |
| Date — seasonal | **Required**: `seasonal` | **Required**: `singleSelect` \| `multiSelect` | **Required**: `quarter` \| `month` \| `week` \| `weekday` \| `day` \| `hour` | As the seasonal rows of [Filter Value Formats](#filter-value-formats) | Allowed | Allowed |
| Date — relative | **Required**: `relative` | **Required**: `singleSelect` \| `multiSelect` | **Required**; send `common` (the value is not used) | Relative phrases — see [Filter Value Formats](#filter-value-formats). `values` is always required; `isallval` is ignored. | Allowed | **Not allowed** (`8008`) |
| Date — range picker | **Required**: `dateRange` (exact case) | `dateRange` (may be omitted when `values` is sent) | Optional; if sent, `range` (lowercase) | Exactly **one** value: `"<from> to <to>"`, each date in one of the [user-filter date formats](#user-filter-date-formats) | **Not allowed** (`8050`) | **Not allowed** (`8008`) |
| Aggregate formula | Not used | Not used | Not used | Not used — the widget is always a slider over the full range | Allowed | Not used |

**`isallval` resolution.** If `isallval` is omitted, the server derives it from `values`: a non-empty
`values` array implies `isallval: false`, an absent or empty one implies `isallval: true`. When you send
`isallval: true` *and* a non-empty `values` array, `isallval` wins and the values are ignored. Sending
`isallval: false` with an absent or empty `values` array raises `8050`.

**`defaultFilterValues`** is validated with the same rules as `values` for the same column and
operation. It does not have to be a subset of `values`. It may not contain `Others` or more than one
`${…}` variable (`8166`). A range-picker default may also be `"from <date>"` or `"to <date>"`.

##### User Filter Date Formats

Dates in a `dateRange` user filter are parsed against these patterns, in order, with English month names
(case-insensitive):

| Pattern | Example |
|---|---|
| `yyyy-MM-dd HH:mm:ss` | `2024-03-18 00:00:00` |
| `yyyy-MM-dd` | `2024-03-18` |
| `dd MMM yyyy` | `18 Mar 2024` |
| `MMM dd, yyyy` | `Mar 18, 2024` |
| `MM/dd/yyyy` | `03/18/2024` |
| `dd/MM/yyyy` | `18/03/2024` — only when the value is not also a valid `MM/dd/yyyy` date |

> Use three-letter month abbreviations in date strings. A `"to <date>"` default whose date contains the
> letters `to` (`October`) cannot be parsed and raises `8168`.

#### Filter Value Formats

Each value is a JSON string. A value that does not match its format raises `8168` unless noted.

##### Text and numeric

| `filterType` | Format | Example `values` |
|---|---|---|
| `individualvalues` (Text) | Any string; exact value match. | `["East", "West"]` |
| `individualvalues` (Boolean column) | `true`, `false`, `1`, `0`, `yes`, `no`, `Yes`, `No` — exactly these spellings. | `["true"]` |
| `individualvalues` (Numeric) | The exact stored value, unformatted and unrounded. If the stored value is `0.89123`, send `0.89123`. A non-number raises `8164`. | `["100", "200.5"]` |
| `range` (Numeric) | `"<n> to <m>"`, `"<n> - <m>"` (spaces around the hyphen), `"<n> and below"`, `"<n> and above"`. Case-insensitive. | `["1000 and below"]`, `["200000 to 300000"]`, `["500000 and above"]` |
| `ranking` | `"Top <N>"` or `"Bottom <N>"`, N a positive integer, one space. Case-insensitive. | `["Top 2"]`, `["Bottom 10"]` |
| `rankingpct` | As `ranking`; N is a percentage (1–100). | `["Top 10"]` |
| `wildcard` | `values` is unused — send `[]`. The criteria live in the `wildcard` object. | `[]` |

##### Date — absolute (`operation: "actual"`)

| `filterType` | Format | Example `values` |
|---|---|---|
| `year` | Four-digit year. | `["2012", "2023"]` |
| `quarteryear` | `Q<1-4> <yyyy>`. | `["Q1 2020", "Q2 2023"]` |
| `monthyear` | `<Mon> <yyyy>` with a three-letter English month (case-insensitive) and one space. | `["Aug 2012", "Jan 2013"]` |
| `weekyear` | `W<ww> <yyyy>`, week 01–53. | `["W03 2012", "W52 2023"]` |
| `fulldate` | `dd MMM yyyy` with a three-letter English month. | `["27 Jan 2023", "20 Mar 2023"]` |
| `datetime` | `dd MMM yyyy HH:mm:ss` (24-hour). | `["27 Jan 2023 00:00:00"]` |
| `daterange` | `"from <datetime>"`, `"to <datetime>"`, `"<datetime> to <datetime>"`, or `"<datetime> - <datetime>"`; each `<datetime>` as `dd MMM yyyy HH:mm:ss`. A date that cannot be parsed raises `8251`. | `["from 10 Dec 2013 00:00:00"]`, `["10 Mar 2012 00:00:00 to 10 Dec 2012 00:00:00"]`, `["to 11 Mar 2013 00:00:00"]` |

##### Date — seasonal (`operation: "seasonal"`)

| `filterType` | Format | Example `values` |
|---|---|---|
| `quarter` | `Q1`–`Q4`. | `["Q1", "Q3"]` |
| `month` | `Jan`, `Feb`, `Mar`, `Apr`, `May`, `Jun`, `Jul`, `Aug`, `Sep`, `Oct`, `Nov`, `Dec` — exact case. | `["Jan", "Feb"]` |
| `week` | `Week <N>`, N 1–53, capital `W`, no leading zero. | `["Week 2", "Week 3"]` |
| `weekday` | `Sun`, `Mon`, `Tue`, `Wed`, `Thu`, `Fri`, `Sat` — exact case. | `["Sun", "Mon"]` |
| `day` | Two-digit day of the month, `01`–`31`. | `["01", "15", "31"]` |
| `hour` | Two-digit hour, `00`–`23`. | `["00", "13", "23"]` |

##### Date — relative (`operation: "relative"`)

Phrases are case-insensitive, words separated by exactly one space. `<unit>` is one of `Year`,
`Quarter`, `Month`, `Week`, `Day`, `Hour`; `<units>` is the singular or plural form (`Years`,
`Quarters`, `Months`, `Weeks`, `Days`, `Hours`); `N` is a positive integer.

| Phrase | Meaning | Examples |
|---|---|---|
| `Today` | The current day. | `["Today"]` |
| `Yesterday` | The previous day. | `["Yesterday"]` |
| `This <unit>` (`Year`, `Quarter`, `Month`, `Week`, `Hour` — singular only) | The current period. | `["This Year"]`, `["This Month"]` |
| `Last <units>` / `Previous <units>` | The previous complete period (both words mean the same here). | `["Last Year"]`, `["Previous Month"]` |
| `Next <units>` | The next period. | `["Next Week"]` |
| `Last N <units>` | The last N periods **including** the current one. | `["Last 2 Years"]`, `["Last 13 years"]` |
| `Previous N <units>` | The N complete periods before the current one (**excluding** it). | `["Previous 3 Months"]` |
| `Next N <units>` | The next N periods. | `["Next 6 Hours"]` |
| `Year to Date`, `Quarter to Date`, `Month to Date` | From the start of the current period to today. | `["Year to Date"]` |

---

## Appendix F – CONFIG Attribute Availability by API

| Attribute | Create Report | Update Report |
|-----------|---|---|
| `baseTableName` | **Yes** | — (`8542`) |
| `title` | **Yes** | No — omission keeps the name; sending it renames the report |
| `reportType` | **Yes** | **Yes** — must match the stored type |
| `axisColumns` | **Yes** | **Yes** |
| `description` | No | No — omission clears |
| `folderId` | No | — (`8145`) |
| `chartType` | No | No — omission resets to automatic |
| `isAxisMerge` | No | No — omission resets to `false` |
| `mergeAxisInfo` | No | No |
| `filters` | No | No — omission clears; no `wildcard` (`8192`) |
| `userFilters` | No | No — omission clears |

[Read Report Metadata](#2-read-report-metadata) takes no CONFIG.

---

## Appendix G – API Units and Frequency Limits

Every call deducts **API units** from the organisation's plan allowance and is counted against a **per-minute request ceiling** shared by all APIs in the same unit category. Both are keyed off the internal gateway action (`api-id`) that the request method and URL resolve to.

| # | API Name | Gateway Action (api-id) | Unit Category | Units | Charged |
|---|----------|-------------------------|---------------|-------|---------|
| 1 | [Create Report](#1-create-report) | `CREATE_ANALYSISVIEW` (2031) | METADATA | 5 | per request |
| 2 | [Read Report Metadata](#2-read-report-metadata) | `GET_REPORT_METADATA` (3052) | METADATA | 0.1 | per request |
| 3 | [Update Report](#3-update-report) | `UPDATE_ANALYSISVIEW` (2032) | METADATA | 5 | per request |

### How the cost is computed

```
units charged = (rows processed / rows basis) * configured units      # row-based APIs
units charged = configured units                                      # everything else
```

Row-based costs are not rounded up to a whole block — processing 250 rows at a rate of 3 units per 1000 rows costs `0.75` units. Units are charged on the rows **actually processed**, after the operation runs, so a partially completed import is still charged for the rows it wrote.

### Frequency limits

| Unit category | Requests per minute | Used by this document |
|---------------|---------------------|-----------------------|
| `DML` | 100 | — |
| `BULK` | 40 | — |
| `METADATA` | 60 | Yes |

The ceiling is per organisation, shared by every API in that category, and is scaled by a plan-specific multiplier — the figures above are the base configuration. Exceeding it fails the request with an API-frequency error, which is independent of running out of units.

The current allocation, usage and remainder of API units for the organisation are returned by the **Get Resource Details** API under `resourceName: "apiUnits"`. Fractional usage is normal. The complete cross-document table is in [API Units and Rate Limits](../API_UNITS_AND_RATE_LIMITS.md).
