---
type: API Group
title: Reports (Analysis Views)
description: "APIs for creating a report (chart, pivot or summary view) on an existing table, reading the stored definition back, and rebuilding it."
tags:
  - zoho-analytics
  - rest-api-v2
  - reports-and-dashboards
  - reports
  - api-group
api:
  domain: reports-and-dashboards
  group: reports
  endpoint_count: 3
  endpoints:
    - operation_id: createReport
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/reports"
      doc: "/domains/reports-and-dashboards/reports/create-report.md"
    - operation_id: getReportMetadata
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata"
      doc: "/domains/reports-and-dashboards/reports/get-report-metadata.md"
    - operation_id: updateReport
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/reports/{view-id}"
      doc: "/domains/reports-and-dashboards/reports/update-report.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-20T17:34:40Z
generated:
  by: process:build_okf
  at: 2026-10-23T07:58:54Z
status: stable
---

# Summary

This document covers the V2 **Report** REST APIs of Zoho Analytics — the APIs that create a chart,
pivot or summary view on a table, read back its stored definition, and rebuild it from a new
definition.

APIs for creating a report (chart, pivot or summary view) on an existing table, reading the stored definition back, and rebuilding it. A report is also called a visual, an analysis view or simply a view in API responses and error messages.

A report is defined almost entirely by its drop fields - the `axisColumns` array, where each entry says which column goes on which shelf with which operation; filters, user filters, window functions and formatting hang off that core. The three endpoints are not available on white-label / custom domains, and Update is a full replacement, never a patch.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Create Report](create-report.md) | POST | `/restapi/v2/workspaces/{workspace-id}/reports` | `createReport` | `ZohoAnalytics.modeling.create` | 200 |
| [Read Report Metadata](get-report-metadata.md) | GET | `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata` | `getReportMetadata` | `ZohoAnalytics.modeling.read` | 200 |
| [Update Report](update-report.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}` | `updateReport` | `ZohoAnalytics.modeling.update` | 204 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is a "Report" in Zoho Analytics?

A **report** (also called a *visual*, an *analysis view*, or a *view* in API responses and error
messages) is a saved visualisation built on one table or query table of a workspace, optionally using
columns of the tables joined to it. The API manages three report families:

| `reportType` | What it produces |
|---|---|
| `chart` | A chart — one of the 57 chart types in [`chartType` Values](overview.md#charttype-values). |
| `pivot` | A pivot table with `row`, `column` and `data` shelves. |
| `summary` | A summary view with `groupBy` and `summarize` shelves. |

A report is defined almost entirely by its **drop fields** — the `axisColumns` array, where each entry
says *which column* goes on *which shelf* with *which operation*. Filters and user filters hang off that
core.

| Part | CONFIG attribute(s) | Notes |
|------|--------------------|-------|
| **Where it is built** | `baseTableName` | The table or query table. **Cannot be changed after creation.** |
| **What it is called** | `title`, `description` | Both can be changed with [Update Report](update-report.md). |
| **What kind of report** | `reportType`, `chartType` | `reportType` **cannot be changed after creation.** |
| **What it shows** | `axisColumns` | Columns, shelves, operations, sorting, window functions, geo roles. |
| **Shared Y axes** | `isAxisMerge`, `mergeAxisInfo` | Charts only. |
| **What it always filters out** | `filters` | Static criteria; viewers cannot change them. |
| **What viewers can filter** | `userFilters` | Interactive filter widgets shown with the report. |
| **Where it is stored** | `folderId` | Create only. A report cannot be moved through these APIs. |

# Column Categories

Every rule in this document that depends on a column's data type uses one of these four categories.

| Category | Column data types |
|---|---|
| **Text** | Plain Text, Multi Line Text, Email, URL, Boolean (Decision Box), Geo, Time |
| **Numeric** | Number, Positive Number, Decimal Number, Currency, Percent, Auto Number, Duration |
| **Date** | Date, Date-Time |
| **Aggregate formula** | A workspace aggregate formula column, referenced by its name. Only **numeric** aggregate formulas are supported. |

> **The single most important behaviour:** [Update Report](update-report.md) is a **full replacement**,
> and [Read Report Metadata](get-report-metadata.md) returns a **lossy summary**. Writing a read
> response back through Update silently destroys user-filter configuration, sorting, window functions
> and geo roles. See [Round-tripping a Report](overview.md#round-tripping-a-report) before writing any
> read-modify-write integration.

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`). All three APIs use the `ZohoAnalytics.modeling` scope group — see [OAuth scopes](../../../foundations/oauth-scopes.md).
> - All three APIs are **workspace-scoped** (`/restapi/v2/workspaces/<workspace-id>/...`) and require the `ZANALYTICS-ORGID` header.
> - `ZohoAnalytics_Server_URI` depends on the data centre (for example `analyticsapi.zoho.com` or `analyticsapi.zoho.eu`).
> - **All three APIs are disabled in Client Portal / White Label request contexts.** Call the standard API host for your data centre.
> - **Only the keys documented here are accepted.** Any other key — at the top level of `CONFIG` or inside any nested object — is rejected with [`8542`](../../../foundations/error-codes.md#error-8542). Key names are case-sensitive.
> - None of these APIs moves, copies or deletes a report. Renaming is possible only through [Update Report](update-report.md) (`title`).

---

# Round-tripping a Report

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
2. **Never send `baseTableName` to Update.** Remove it from anything you assembled from a read ([`8542`](../../../foundations/error-codes.md#error-8542)).
3. **Re-send every `filters` and `userFilters` entry you want to keep.** Omitting the array deletes it.
4. **`mergeAxisInfo` is not returned in write form.** The read returns one merge object repeated, with `axisIndex` as stored — see [`mergeAxisInfo` on Read](overview.md#mergeaxisinfo-on-read). Rebuild `mergeAxisInfo` from your own copy of the Create CONFIG.

## Values that change across a round trip

The read reconstructs every value from storage. Where several inputs share one stored form, the read
always returns the **same** one, listed below.

| Key | What the read returns |
|---|---|
| `title`, `baseTableName`, `columnName`, `tableName` | The object's current display name, in its stored casing. |
| `description` | The stored text. The key is **absent** when no description is stored. |
| `chartType` | One fixed name per stored chart — the *Returned on read* column of [`chartType` Values](overview.md#charttype-values). |
| `axisColumns[].type` | Lowercase: `xaxis`, `yaxis`, `coloraxis`, `textaxis`, `sizeaxis`, `latlng`, `tooltip`, `row`, `column`, `data`, `groupby`, `summarize`. All are valid on write. |
| `axisColumns[].operation` | See [Axis Operations on Read](overview.md#axis-operations-on-read). |
| `filters[].operation` | Numeric: `actual` for `measure` / `dimension` / `actual`; `std` for `std` / `stddev`; `aggregate` for `variance` / `dc` / `distinctcount` / `aggregate`; otherwise the operation sent. Text `actual`: `actual`. Text `count` / `dc` / `distinctcount`: stored as numeric filters and returned as `count` / `aggregate`. Date: `actual` for `actual` / `range` / `daterange`; `seasonal`; `relative`. |
| `filters[].filterType` | Numeric: `individualvalues`, `range`, `ranking`, `rankingpct`. Text: `individualvalues` (also for `individual`), `wildcard`. Date — absolute and seasonal filters: `year` (also for `common`), `quarteryear` (for every quarter type), `absmonth` (for every month type), `week` (for `weekyear` / `absweek` / `week`), `date` (for `fulldate` / `date`), `datetime`, `daterange` (also for `range`), `weekday`, `day`, `hour`. Relative filters: `year`. A seasonal `quarter` / `month` filter therefore reads back with an absolute-looking `filterType`; keep your own copy of the original `filterType`. |
| `filters[].values` | The stored display text split on commas, each piece trimmed, empty pieces dropped. **A value containing a comma is split into several values.** |
| `filters[].exclude` | Boolean. |
| `userFilters[].operation` | Text: `actual`. Numeric: `actual`, `sum`, `min`, `max`, `average`, `std`, `count`, `distinctcount`. Date: `year`, `absquarter`, `absmonth`, `absweek`, `fulldate`, `datetime`, `range`, or the string `"null"` for seasonal day / hour / weekday and relative filters. **None of the date values is a valid write `operation`** (`actual`, `seasonal`, `relative`, `dateRange`) — re-submitting raises `8166`. |
| `reportType` | `chart`, `pivot`, `summary`, or `widget` for widget views. `widget` is rejected on write with `8509`. |

### Axis Operations on Read

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

### `mergeAxisInfo` on Read

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

# Limitations

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

# Permission Model

| Role | Create Report | Read Report Metadata | Update Report |
|------|---------------|----------------------|---------------|
| Account Admin / Organization Admin / Workspace Owner / Workspace Admin | Yes — `folderId` honoured. | Yes | Yes |
| Report owner | — | Yes | Yes |
| Custom role with **Create Report** on the base table | Yes — `folderId` honoured. Without the permission: `7324`. | Only with **Design Modify** on the report. | **No** — `7301`. |
| Shared / group user with **Create Report** permission | Yes — **`folderId` is ignored**; the report appears under the caller's *My Reports*. | Only with **Design Modify** on the report. | **No** — `7301`, even with Design Modify. |
| Read-only shared user | No — `7301`. | No — `7301`. | No — `7301`. |

Every caller must also be able to read the base table and every column the report uses ([`7301`](../../../foundations/error-codes.md#error-7301) for the
table, [`7725`](../../../foundations/error-codes.md#error-7725) for a column).

---

# API-Specific Notes and Behaviours

## Create Report

- **`title` is effectively the identity.** It is mandatory ([`8051`](../../../foundations/error-codes.md#error-8051)), must be unique across every object
  in the workspace ([`7111`](../../../foundations/error-codes.md#error-7111)). It can be changed later with [Update Report](update-report.md).
- **`chartType` is not checked against the shelves.** An incompatible chart type is saved as sent; the
  renderer falls back to a compatible chart when the report is opened.
- **Only the first `sort` counts in charts and summaries.** Put the `sort` on the column you want sorted
  and nowhere else.
- **Every chart window function except `normal` and `pctoftotal` needs a base field.** `runtotal`
  without `baseField` fails with [`8253`](../../../foundations/error-codes.md#error-8253).
- **`geoRole` is case-sensitive and mandatory on Plain Text and Number columns.** Send it lowercase.
- **Date filter `operation` values are case-sensitive.** `"Actual"` raises [`8166`](../../../foundations/error-codes.md#error-8166).
- **The range-picker user filter requires `operation: "dateRange"` exactly.** `range` and `daterange`
  are rejected.
- **Shared users cannot choose a folder.** `folderId` is ignored for them without error.
- **Dependency chain:** workspace list → `<workspace-id>` → view list → `baseTableName`, column names,
  `folderId` → Create Report → `data.viewId`.

## Read Report Metadata

- **It is an inspection endpoint, not an export.** The response omits every write-only key and
  normalises values — see [Round-tripping a Report](overview.md#round-tripping-a-report).
- **Merged-axis charts return `mergeAxisInfo` in read form** — one object repeated, `axisIndex` as stored.
  See [`mergeAxisInfo` on Read](overview.md#mergeaxisinfo-on-read).
- **Distinct-count and variance columns return the source column** with `distinctcount`, `variance` or
  the date distinct-count variant as `operation`.
- **`description` is absent, not empty,** when none is stored.
- **Dependency chain:** [Create Report](create-report.md) → `data.viewId` → Read Report Metadata.

## Update Report

- **Full replacement, not a patch.** Omitting `filters`, `userFilters` or `description` clears them;
  omitting `chartType` lets the server choose; omitting `isAxisMerge` turns merging off.
- **Owner or admin only.** Shared, group and Custom Role users are rejected with [`7301`](../../../foundations/error-codes.md#error-7301), even with
  Design Modify permission.
- **`folderId` always fails** ([`8145`](../../../foundations/error-codes.md#error-8145)), even when it equals the current folder.
- **`title` renames the report — without a uniqueness check.** Update does not trim the name and does
  not raise [`7111`](../../../foundations/error-codes.md#error-7111); check that no other object in the workspace uses the name before renaming.
- **Wildcard filters cannot be updated** ([`8192`](../../../foundations/error-codes.md#error-8192)).
- **Dependency chain:** [Create Report](create-report.md) → `data.viewId` and the Create CONFIG →
  Update Report.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Which endpoints return 204** | [Update Report](update-report.md) returns **204 No Content** with no body on success. |
| **Which endpoints return a body** | [Create Report](create-report.md) returns `data.viewId`; [Read Report Metadata](get-report-metadata.md) returns `data.reportConfig`. |
| **Failure responses always carry a body** | Even for the 204 API, errors return `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name, not a localised sentence. |
| **All IDs are strings** | `data.viewId` is serialised as a JSON **string** even though the value is numeric. Parse it as a string or long — never as a native JSON number — to avoid precision loss. |
| **Conditional keys** | In `reportConfig`, `description`, `chartType`, `isAxisMerge`, `axisColumns`, `filters` and `userFilters` are omitted when there is nothing stored; `mergeAxisInfo` appears only when `isAxisMerge` is `true`. |
| **Responses are extensible** | Some builds return additional fields. Ignore unrecognised keys rather than validating against a closed schema. |

---

# Enum and Value Reference

Consolidated lookup for every enum used by [Create Report](create-report.md) and
[Update Report](update-report.md). Values are listed exhaustively: a value not listed here is not
supported.

### `chartType` Values

`chartType` is matched case-insensitively. Only letters, digits and spaces are allowed — no hyphens or
underscores. The accepted values are exactly the 57 below; any other value raises [`8144`](../../../foundations/error-codes.md#error-8144). Names in the
same *Equivalent names* group produce an identical stored chart, and [Read Report Metadata](get-report-metadata.md) returns the name in the *Returned on read* column for all of them.

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

Not accepted (raise [`8144`](../../../foundations/error-codes.md#error-8144)): `stacked area without points`, `stacked area without markers`,
`stacked area with markers`.

Omitting `chartType` makes the server choose a chart type automatically.

### Axis Type Values

The `type` value in an `axisColumns` entry must be one of these exact spellings. Any other spelling raises
[`8509`](../../../foundations/error-codes.md#error-8509); a valid spelling used with the wrong `reportType` raises [`8170`](../../../foundations/error-codes.md#error-8170).

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
column for most chart types ([`7701`](../../../foundations/error-codes.md#error-7701)). A pivot needs at least one `row`, `column` or `data` column
([`7706`](../../../foundations/error-codes.md#error-7706)); a summary needs at least one `groupBy` or `summarize` column ([`7705`](../../../foundations/error-codes.md#error-7705)).

### Axis Operation Values

The valid `operation` for an `axisColumns` entry depends on the column category ([Column
categories](overview.md#column-categories)) **and** on the shelf. Operations are matched case-insensitively and must
contain letters only. Send only the operations listed here. An operation outside the list raises
[`8166`](../../../foundations/error-codes.md#error-8166), with one exception: on the pivot `row` / `column` and summary `groupBy` shelves the operation of
a Text column is not checked and is always treated as `actual`.

#### Chart (every chart shelf)

| Category | Accepted operations |
|---|---|
| Text | `actual` (group by value), `count`, `dc` (alias `distinctcount`), `geo` |
| Numeric | `sum`, `min`, `max`, `average` (alias `avg`), `stddev`, `median`, `mode`, `percentile`, `count`, `variance`, `dc` (alias `distinctcount`), `measure` (un-aggregated value), `dimension` (each value as a category), `range` (numeric bins; honours `rangeSize`), `geo` |
| Date | Grouping: `year`, `quarter`, `month`, `week`, `weekday`, `day`, `hour` (seasonal), `quarteryear` (alias `absquarter`), `monthyear` (alias `absmonth`), `weekyear` (alias `absweek`), `fulldate`, `datetime` (absolute). Aggregates: `count`, `distinctcount`, `ydc`, `qydc`, `mydc`, `wydc`, `ddc`, `dtdc`, `qdc`, `mdc`, `wdc`, `wddc`, `dmdc`, `hdc` |
| Aggregate formula | `operation` is not required and is ignored. |

`percentile` computes the percentile given by `windowFunction.percentileVal` (default 50).

#### Pivot

| Category | `row` / `column` | `data` |
|---|---|---|
| Text | `actual` | `count`, `dc` (alias `distinctcount`) |
| Numeric | `dimension`, `range` | `sum`, `min`, `max`, `average`, `stddev`, `median`, `mode`, `percentile`, `count`, `variance`, `dc` (alias `distinctcount`) |
| Date | The date grouping operations of the chart table | `count`, `distinctcount` and the date distinct-count variants of the chart table |
| Aggregate formula | Not allowed (`8053`) | `operation` ignored |

#### Summary

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

### Window Function Type Values

`type` is matched case-insensitively. *Needs base field* means `baseField` and `baseFieldPosition` are
required — see [Base Field Rules](create-report.md#base-field-rules).

#### Chart Window Function Types

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

#### Pivot Window Function Types

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

### Geo Role Values

`geoRole` is matched **case-sensitively** — send it in lowercase exactly as listed. Geo operations are
valid on chart reports only.

| Column type | Valid `geoRole` values | Placement |
|---|---|---|
| Plain Text | **Required**: `continent`, `country`, `state`, `province`, `county`, `district`, `city`, `zipcode`, `airport` | `xAxis` only (`8258` otherwise) |
| Number, Positive Number, Decimal Number | **Required**: `latitude`, `longitude` | Any chart shelf |
| Geo (column already typed with a geo role) | Optional. If sent, a value from the Plain Text row; the column's own role is used. | `xAxis` only (`8258` otherwise) |

Rules, each enforced with its own error:

- `geo` on a column type not listed above raises [`8255`](../../../foundations/error-codes.md#error-8255).
- `latitude` / `longitude` on a text column, or a place role on a numeric column, raises [`8254`](../../../foundations/error-codes.md#error-8254).
- At most **one** text geo column on the X axis, and at most **one** numeric geo column on each of the
  X and Y axes ([`8256`](../../../foundations/error-codes.md#error-8256)).
- A text geo column on X and a numeric geo column on Y cannot coexist ([`8257`](../../../foundations/error-codes.md#error-8257)).

### Wildcard Operation Values

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

Uppercase only ([`8509`](../../../foundations/error-codes.md#error-8509) otherwise).

### Static Filter Operation and Type Values

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
- An `operation` outside the list raises [`8166`](../../../foundations/error-codes.md#error-8166); a `filterType` outside the list raises [`8167`](../../../foundations/error-codes.md#error-8167).

### User Filter Rules by Column

| Column / operation | `operation` | `compType` | `filterType` | `values` / `defaultFilterValues` format | `exclude` | `behaviour` |
|---|---|---|---|---|---|---|
| Text | Optional; if sent, `actual` | **Required**: `singleSelect` \| `multiSelect` | Optional; if sent, `individualvalues` | Any strings | Allowed | Allowed |
| Numeric — slider | **Required**: `sum` \| `min` \| `max` \| `avg` \| `std` \| `stddev` \| `count` \| `dc` \| `actual` | **Required**: `slider` | Not used | Not used — a slider always covers the full value range; `values` and `isallval` are ignored. Do not send `defaultFilterValues` (more than one value raises `8166`). | Allowed | **Not allowed** (`8008`) |
| Numeric — select list | Optional; if sent, `actual` | **Required**: `multiSelect` | **Required** when `isallval` is `false`: `individualvalues` \| `range` \| `ranking` \| `rankingpct` | As the numeric rows of [Filter Value Formats](overview.md#filter-value-formats) | Allowed | Allowed |
| Date — absolute | **Required**: `actual` | **Required**: `singleSelect` \| `multiSelect` | **Required**: `year` \| `quarteryear` \| `monthyear` \| `weekyear` \| `fulldate` \| `datetime` (aliases: `quarter` = `quarteryear`, `month` = `monthyear`, `week` = `weekyear`, `date` = `fulldate`) | As the absolute date rows of [Filter Value Formats](overview.md#filter-value-formats) | Allowed | Allowed |
| Date — seasonal | **Required**: `seasonal` | **Required**: `singleSelect` \| `multiSelect` | **Required**: `quarter` \| `month` \| `week` \| `weekday` \| `day` \| `hour` | As the seasonal rows of [Filter Value Formats](overview.md#filter-value-formats) | Allowed | Allowed |
| Date — relative | **Required**: `relative` | **Required**: `singleSelect` \| `multiSelect` | **Required**; send `common` (the value is not used) | Relative phrases — see [Filter Value Formats](overview.md#filter-value-formats). `values` is always required; `isallval` is ignored. | Allowed | **Not allowed** (`8008`) |
| Date — range picker | **Required**: `dateRange` (exact case) | `dateRange` (may be omitted when `values` is sent) | Optional; if sent, `range` (lowercase) | Exactly **one** value: `"<from> to <to>"`, each date in one of the [user-filter date formats](overview.md#user-filter-date-formats) | **Not allowed** (`8050`) | **Not allowed** (`8008`) |
| Aggregate formula | Not used | Not used | Not used | Not used — the widget is always a slider over the full range | Allowed | Not used |

**`isallval` resolution.** If `isallval` is omitted, the server derives it from `values`: a non-empty
`values` array implies `isallval: false`, an absent or empty one implies `isallval: true`. When you send
`isallval: true` *and* a non-empty `values` array, `isallval` wins and the values are ignored. Sending
`isallval: false` with an absent or empty `values` array raises [`8050`](../../../foundations/error-codes.md#error-8050).

**`defaultFilterValues`** is validated with the same rules as `values` for the same column and
operation. It does not have to be a subset of `values`. It may not contain `Others` or more than one
`${…}` variable ([`8166`](../../../foundations/error-codes.md#error-8166)). A range-picker default may also be `"from <date>"` or `"to <date>"`.

#### User Filter Date Formats

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
> letters `to` (`October`) cannot be parsed and raises [`8168`](../../../foundations/error-codes.md#error-8168).

### Filter Value Formats

Each value is a JSON string. A value that does not match its format raises [`8168`](../../../foundations/error-codes.md#error-8168) unless noted.

#### Text and numeric

| `filterType` | Format | Example `values` |
|---|---|---|
| `individualvalues` (Text) | Any string; exact value match. | `["East", "West"]` |
| `individualvalues` (Boolean column) | `true`, `false`, `1`, `0`, `yes`, `no`, `Yes`, `No` — exactly these spellings. | `["true"]` |
| `individualvalues` (Numeric) | The exact stored value, unformatted and unrounded. If the stored value is `0.89123`, send `0.89123`. A non-number raises `8164`. | `["100", "200.5"]` |
| `range` (Numeric) | `"<n> to <m>"`, `"<n> - <m>"` (spaces around the hyphen), `"<n> and below"`, `"<n> and above"`. Case-insensitive. | `["1000 and below"]`, `["200000 to 300000"]`, `["500000 and above"]` |
| `ranking` | `"Top <N>"` or `"Bottom <N>"`, N a positive integer, one space. Case-insensitive. | `["Top 2"]`, `["Bottom 10"]` |
| `rankingpct` | As `ranking`; N is a percentage (1–100). | `["Top 10"]` |
| `wildcard` | `values` is unused — send `[]`. The criteria live in the `wildcard` object. | `[]` |

#### Date — absolute (`operation: "actual"`)

| `filterType` | Format | Example `values` |
|---|---|---|
| `year` | Four-digit year. | `["2012", "2023"]` |
| `quarteryear` | `Q<1-4> <yyyy>`. | `["Q1 2020", "Q2 2023"]` |
| `monthyear` | `<Mon> <yyyy>` with a three-letter English month (case-insensitive) and one space. | `["Aug 2012", "Jan 2013"]` |
| `weekyear` | `W<ww> <yyyy>`, week 01–53. | `["W03 2012", "W52 2023"]` |
| `fulldate` | `dd MMM yyyy` with a three-letter English month. | `["27 Jan 2023", "20 Mar 2023"]` |
| `datetime` | `dd MMM yyyy HH:mm:ss` (24-hour). | `["27 Jan 2023 00:00:00"]` |
| `daterange` | `"from <datetime>"`, `"to <datetime>"`, `"<datetime> to <datetime>"`, or `"<datetime> - <datetime>"`; each `<datetime>` as `dd MMM yyyy HH:mm:ss`. A date that cannot be parsed raises `8251`. | `["from 10 Dec 2013 00:00:00"]`, `["10 Mar 2012 00:00:00 to 10 Dec 2012 00:00:00"]`, `["to 11 Mar 2013 00:00:00"]` |

#### Date — seasonal (`operation: "seasonal"`)

| `filterType` | Format | Example `values` |
|---|---|---|
| `quarter` | `Q1`–`Q4`. | `["Q1", "Q3"]` |
| `month` | `Jan`, `Feb`, `Mar`, `Apr`, `May`, `Jun`, `Jul`, `Aug`, `Sep`, `Oct`, `Nov`, `Dec` — exact case. | `["Jan", "Feb"]` |
| `week` | `Week <N>`, N 1–53, capital `W`, no leading zero. | `["Week 2", "Week 3"]` |
| `weekday` | `Sun`, `Mon`, `Tue`, `Wed`, `Thu`, `Fri`, `Sat` — exact case. | `["Sun", "Mon"]` |
| `day` | Two-digit day of the month, `01`–`31`. | `["01", "15", "31"]` |
| `hour` | Two-digit hour, `00`–`23`. | `["00", "13", "23"]` |

#### Date — relative (`operation: "relative"`)

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

# CONFIG Attribute Availability by API

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

[Read Report Metadata](get-report-metadata.md) takes no CONFIG.

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7016](../../../foundations/error-codes.md#error-7016) | 400 | OBJECT_NAME_EMPTY - title is empty or whitespace-only. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7106](../../../foundations/error-codes.md#error-7106) | 404 | META_OBJECT_NOT_PRESENT - The report has been deleted. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | METADBOBJECTNAMEDUPLICATED — An object with this tableName already exists. |
| [7137](../../../foundations/error-codes.md#error-7137) | 400 | NOTATABLE — The target view is not a table. |
| [7138](../../../foundations/error-codes.md#error-7138) | 400 | METAOBJECTNOTPRESENT — A tableName in vudColumns / drillColumns is not a table involved in this view. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7309](../../../foundations/error-codes.md#error-7309) | 400 | SECURITYNEEDSLOGIN — No authentication was supplied. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7324](../../../foundations/error-codes.md#error-7324) | 400 | PERMISSION_DENIED_FOR_DOMAINUSER - A Custom Role user's role does not grant Create Report on the base table. |
| [7362](../../../foundations/error-codes.md#error-7362) | 400 | NO_SUCH_FOLDER_IN_DB - folderId does not exist in the workspace. |
| [7701](../../../foundations/error-codes.md#error-7701) | 400 | DROP_X_Y - The chart's shelves do not form a drawable chart; typically no X-axis or no Y-axis column. |
| [7703](../../../foundations/error-codes.md#error-7703) | 400 | REMOVE_CLR_FIELD - Multiple Y-axis columns in a shelf combination that does not support them, typically with a colorAxis column or with no X-axis column. |
| [7705](../../../foundations/error-codes.md#error-7705) | 400 | DROP_SUMMARY - A summary report has no groupBy and no summarize column. |
| [7706](../../../foundations/error-codes.md#error-7706) | 400 | DROP_PIVOT - A pivot report has no row, column or data column. |
| [7725](../../../foundations/error-codes.md#error-7725) | 400 | ILLEGAL_COLUMN - The caller is not permitted to access a column used in the report. |
| [7727](../../../foundations/error-codes.md#error-7727) | 400 | Y_EXCEED_LIMIT - More than 15 Y-axis columns on a chart. |
| [8008](../../../foundations/error-codes.md#error-8008) | 400 | UNKNOWN_PARAMETER - behaviour was supplied on a slider, dateRange or relative user filter. |
| [8021](../../../foundations/error-codes.md#error-8021) | 400 | INVALID_VIEW_TYPE_IN_REQUEST - The target is a table, query table or dashboard, not a report. |
| [8050](../../../foundations/error-codes.md#error-8050) | 400 | INVALID_VALUE - A value is invalid: an unknown column name; an explicit null for any key; an empty columnName; a mergeAxisInfo rule violation; mergeAxisInfo without isAxisMerge: true; isallval: false with no values; an invalid user-filter operation or filterType; exclude: true on a range-picker user filter. |
| [8051](../../../foundations/error-codes.md#error-8051) | 400 | VALUE_NOT_PRESENT - A mandatory key is missing: title, reportType, axisColumns, an axis type or operation, a filter's filterType, values, exclude or operation, windowFunction.type, baseFieldPosition, movingCalculation or one of its keys, a wildcard object, mergeAxisInfo[].axisIndex; or the four-key base-field lookup found no matching entry. |
| [8052](../../../foundations/error-codes.md#error-8052) | 400 | COLUMN_COUNT_EXCEEDED - More than 1000 entries in axisColumns, filters or userFilters. |
| [8053](../../../foundations/error-codes.md#error-8053) | 400 | AGGREGATE_COLUMN_INVALID_FIELD - In a pivot or summary report, an aggregate formula column is placed on row, column or groupBy. |
| [8055](../../../foundations/error-codes.md#error-8055) | 400 | NUMERIC_RANKING_COLUMN - rankingColumn names a Numeric column. |
| [8056](../../../foundations/error-codes.md#error-8056) | 400 | NOT_ALLOWED - pctoftotal on an average, stddev, variance, dc or distinctcount column, or on an aggregate formula. |
| [8057](../../../foundations/error-codes.md#error-8057) | 400 | NOT_ALLOWED_BASEFIELD - windowFunction.baseField is not a dimension entry of axisColumns. |
| [8058](../../../foundations/error-codes.md#error-8058) | 400 | The organisation ID provided in ZANALYTICS-DEST-ORGID does not exist. |
| [8059](../../../foundations/error-codes.md#error-8059) | 400 | UNRELATED_TABLE - A tableName is not a table joined to the base table. |
| [8144](../../../foundations/error-codes.md#error-8144) | 406 | INVALID_GRAPH_TYPE - chartType is not a value from chartType Values. |
| [8145](../../../foundations/error-codes.md#error-8145) | 406 | FOLDERID_CANNOT_BE_UPDATED - folderId was supplied. |
| [8162](../../../foundations/error-codes.md#error-8162) | 400 | RANGE_SIZE_NOT_SUPPORTED_FOR_THIS_OPERATION - rangeSize was supplied on an operation other than range. |
| [8164](../../../foundations/error-codes.md#error-8164) | 400 | FILTER_COLUMN_DATATYPE_MISMATCH - A numeric individualvalues filter value is not a valid number for the column. |
| [8166](../../../foundations/error-codes.md#error-8166) | 400 | INVALID OPERATION FOR THE COLUMN - The operation is not valid for the column's category and shelf; or a defaultFilterValues entry is invalid. |
| [8167](../../../foundations/error-codes.md#error-8167) | 400 | INVALID FILTER TYPE FOR THE GIVEN OPERATION - The filterType is not valid for the column category and operation. |
| [8168](../../../foundations/error-codes.md#error-8168) | 400 | INVALID CRITERIA FORMAT FOR THE COLUMN - A values entry does not match the format for its filterType. |
| [8169](../../../foundations/error-codes.md#error-8169) | 400 | INVALID WINDOW TYPE FOR THE COLUMN - windowFunction.type or movingCalculation.calculation is not a valid value. |
| [8170](../../../foundations/error-codes.md#error-8170) | 400 | INVALID AXIS TYPE FOR THE REPORT - An axis type is not valid for the chosen reportType. |
| [8179](../../../foundations/error-codes.md#error-8179) | 403 | DONTHAVEPERMISSIONTOCREATETAGS — The caller is not an Account Admin, Organization Admin, or Workspace Admin. |
| [8187](../../../foundations/error-codes.md#error-8187) | 400 | ADVFILTER_EXPRESSION_ORDER_CHANGE - Criteria indexes in wildcard.expression are out of order. |
| [8188](../../../foundations/error-codes.md#error-8188) | 400 | EXPORTINVALIDPASSWORD — password is blank or shorter than 6 characters. |
| [8192](../../../foundations/error-codes.md#error-8192) | 400 | TRUSTED_DOMAINS_WITHOUT_DOMAIN_RESTRICTION - trustedDomains was sent for a section whose domain restriction is off or is being switched off. |
| [8201](../../../foundations/error-codes.md#error-8201) | 400 | INVALIDCONFIGURATIONREMOVEVIEWSLINKEDWITHTAG — viewIds is empty or absent and dissociateAll is not true. |
| [8250](../../../foundations/error-codes.md#error-8250) | 400 | INVALID_UF_COMP_TYPE - compType is not valid for the column category or operation. |
| [8251](../../../foundations/error-codes.md#error-8251) | 400 | INCORRECT_DATE_VALUE - A date in a date-range static filter could not be parsed. |
| [8253](../../../foundations/error-codes.md#error-8253) | 400 | RESTORE_ALREADY_IN_PROGRESS - A restore is running for this workspace. |
| [8254](../../../foundations/error-codes.md#error-8254) | 400 | INVALID_VALUE_FOR_ATTRIBUTE_FOR_COLUMN - latitude / longitude on a text column, or a place role on a numeric column. |
| [8255](../../../foundations/error-codes.md#error-8255) | 400 | INVALID_KEY_GIVEN - operation: "geo" on a column type that cannot be geocoded. |
| [8256](../../../foundations/error-codes.md#error-8256) | 404 | GEO_COL_COUNT_EXCEEDED - More than one text geo column on X, or more than one numeric geo column on one axis. |
| [8257](../../../foundations/error-codes.md#error-8257) | 400 | GEO_COL_COUNT_EXCEEDED_CATEGORICAL - A text geo column on X coexists with a numeric geo column on Y. |
| [8258](../../../foundations/error-codes.md#error-8258) | 400 | GEO_COL_CATEGORY_ONLY_X - A text geo column was placed on a shelf other than X. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | LESSTHANMINOCCURANCE — CONFIG was not sent. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | MORETHANMAXLENGTH — roleName exceeds 30 characters, or permissions exceeds its size limit. |
| [8509](../../../foundations/error-codes.md#error-8509) | 400 | PATTERNNOTMATCHED — roleName contains disallowed characters, or accessType is not one of the three values. |
| [8516](../../../foundations/error-codes.md#error-8516) | 400 | UNABLETOPARSEDATATYPE — A CONFIG value has the wrong JSON type. |
| [8517](../../../foundations/error-codes.md#error-8517) | 400 | DATATYPE_NOT_MATCHED - A value has the wrong JSON type: exclude: "yes", isAxisMerge: 1, folderId: "abc". |
| [8534](../../../foundations/error-codes.md#error-8534) | 400 | JSONPARSEERROR — CONFIG is not valid JSON. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |
| [8542](../../../foundations/error-codes.md#error-8542) | 400 | EXTRA_KEY_FOUND_IN_JSON - A key not listed in this document is present. |
| [8544](../../../foundations/error-codes.md#error-8544) | 400 | OUT_OF_RANGE - An integer is outside its range: percentileVal outside 0-100, a mergeAxisInfo index outside 0-100. |
| [8547](../../../foundations/error-codes.md#error-8547) | 400 | ARRAYSIZEOUTOFRANGE — selectedColumns is empty or holds more than 300 entries. |
| [14037](../../../foundations/error-codes.md#error-14037) | 400 | DISABLED_COLUMNS_USED - A disabled column is used in the report. |

# Related

- [Reports & Dashboards](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
