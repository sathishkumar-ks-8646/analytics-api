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
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

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
> [Update is destructive](update-report.md#update-is-destructive) before writing any update integration.

---

APIs for creating a report (chart, pivot or summary view) on an existing table, reading the stored definition back, and rebuilding it. A report is also called a visual, an analysis view or simply a view in API responses and error messages.

A report is defined almost entirely by its drop fields - the `axisColumns` array, where each entry says which column goes on which shelf with which operation; filters, user filters, window functions and formatting hang off that core. The three endpoints are not available on white-label / custom domains, and Update is a full replacement, never a patch.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Create Report](create-report.md) | POST | `/restapi/v2/workspaces/{workspace-id}/reports` | `createReport` | `ZohoAnalytics.modeling.create` | 200 |
| [Read Report Metadata](get-report-metadata.md) | GET | `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata` | `getReportMetadata` | `ZohoAnalytics.modeling.read` | 200 |
| [Update Report](update-report.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}` | `updateReport` | `ZohoAnalytics.modeling.update` | 204 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# Round-tripping a report

[Read Report Metadata](get-report-metadata.md) is an **inspection** endpoint. Its response is a summary
of the stored definition, not a Create or Update payload. Feeding it back into Update is the most common
and most damaging mistake against this API: the call succeeds, and the report quietly loses most of its
configuration.

**If you need read-modify-write, retain the CONFIG you submitted at create time and modify that.**

## Written but never returned

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

## Values that change across a round trip

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

## Keys that must be removed before an update

| Key | Why |
|---|---|
| `baseTableName` | Returned by the read, rejected by Update with **8542**. |

And `reportType` must be **added** if you are assembling an update payload from anything that omits it —
it is mandatory on Update and must match the stored view type.

> **Axis-merged reports cannot be read at all.** When `isAxisMerge` is `true` the metadata call currently
> fails with an internal error while assembling `mergeAxisInfo`. Do not build a read-modify-write flow
> that depends on reading a merged-axis report.

---

# Chart Types

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

# Axis Types

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

# Operations

The valid `operation` for an `axisColumns` entry depends on the column's data type **and** on where the
column sits.

## Numeric columns on a chart

`sum`, `min`, `max`, `average`, `avg`, `stddev`, `median`, `mode`, `percentile`, `count`, `variance`,
`dc`, `distinctcount`, `measure`, `dimension`, `range`, `actual`, `geo`.

`dimension` and `range` convert the measure into a dimension; `range` is the one that honours
`rangeSize`. Window functions are not available on either.

## Numeric columns in a pivot

- On `data`: `sum`, `min`, `max`, `average`, `stddev`, `median`, `mode`, `percentile`, `count`,
  `variance`, `dc`, `distinctcount`. **`avg` is not accepted here — use `average`.**
- On `row` / `column`: only `dimension` and `range`. `actual` is not valid in these positions.

## Text, email, URL and multi-line columns

`actual`, `count`, `dc`, `distinctcount`, `geo`. `actual` is the plain grouping operation.

## Date columns on a chart

- Grouping: `year`, `quarter`, `month`, `week`, `weekday`, `day`, `hour`
- Absolute grouping: `quarteryear` (alias `absquarter`), `monthyear` (alias `absmonth`),
  `weekyear` (alias `absweek`), `fulldate`, `datetime`
- Aggregates: `count`, `distinctcount`, `maxdate`, `mindate`
- Date distinct-count variants: `ydc`, `mydc`, `wydc`, `qydc`, `ddc`, `dtdc`, `qdc`, `wdc`, `wddc`,
  `dmdc`, `hdc`, `mdc`

## Date columns in a pivot

- On `data`: `maxdate`, `mindate`, `count`, `distinctcount`, and the date distinct-count variants.
- On `row` / `column`: the grouping operations listed above (no aggregates).

> `std` is **not** a valid axis operation — the standard-deviation operation is `stddev`. (`std` *is*
> accepted in the `filters` array, which uses a separate, more permissive map.)

> `axisColumns[].operation` is pattern-checked as letters only. Any value containing a digit, hyphen or
> underscore is rejected with **8509** before the maps above are consulted.

An operation that is not in the map for the column's data type raises **8166**.

---

# Filter Operations and Types

## Static filters (`filters`)

| Column type | `operation` | `filterType` |
|---|---|---|
| Numeric | `measure`, `dimension`, `sum`, `min`, `max`, `average`, `stddev`, `std`, `count`, `variance`, `dc`, `distinctcount`, `median`, `mode`, `actual`, `aggregate` | `individualvalues`, `range`, `ranking`, `rankingpct` |
| Text | `actual`, `count`, `dc`, `distinctcount`, `geo` | `individualvalues` (alias `individual`), `wildcard` |
| Date — absolute | `actual`, `range`, `daterange` | `year`, `quarter`, `month`, `week`, `weekday`, `day`, `hour`, `quarteryear` (alias `absquarter`), `monthyear` (alias `absmonth`), `weekyear` (alias `absweek`), `date`, `fulldate`, `datetime`, `range`, `daterange`, `common` |
| Date — seasonal | `seasonal` | `quarter`, `month`, `week`, `weekday`, `day`, `hour` |
| Date — relative | `relative` | `common`, `year`, `quarter`, `month`, `week`, `day`, `hour` |

Values are matched case-insensitively; `individualValues` and `individualvalues` both work.

## User filters (`userFilters`)

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

# Filter Value Formats

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

# Operational Notes and Failure Cases

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

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. |
| [7016](../../../foundations/error-codes.md#error-7016) | 400 | title is empty or whitespace-only. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7106](../../../foundations/error-codes.md#error-7106) | 404 | The report does not exist or has been deleted. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | METADBOBJECTNAMEDUPLICATED — An object with this tableName already exists. |
| [7138](../../../foundations/error-codes.md#error-7138) | 400 | baseTableName does not resolve to a table in this workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7362](../../../foundations/error-codes.md#error-7362) | 400 | folderId does not exist in the workspace. |
| [7701](../../../foundations/error-codes.md#error-7701) | 400 | A chart report has no X-axis or no Y-axis column. |
| [7703](../../../foundations/error-codes.md#error-7703) | 400 | A colorAxis column is present alongside more than one Y-axis column. |
| [7727](../../../foundations/error-codes.md#error-7727) | 400 | More than 15 Y-axis columns on a chart. |
| [8008](../../../foundations/error-codes.md#error-8008) | 400 | behaviour was supplied on a daterange or relative user filter. |
| [8021](../../../foundations/error-codes.md#error-8021) | 400 | The pivot or summary structure is invalid — no data column in a pivot, too many data or groupBy columns, or a column in a position its type cannot occupy. On Update, also raised when reportType does not match the stored view's type. |
| [8050](../../../foundations/error-codes.md#error-8050) | 400 | A value is invalid — unknown columnName, an operation incompatible with the column, a null axisColumns. |
| [8051](../../../foundations/error-codes.md#error-8051) | 400 | A required field is missing — title, reportType, axisColumns, or a mandatory key inside an axis/filter object. |
| [8052](../../../foundations/error-codes.md#error-8052) | 400 | More than 1000 entries in axisColumns, filters or userFilters. |
| [8057](../../../foundations/error-codes.md#error-8057) | 400 | The column named in windowFunction.baseField cannot be used as a base field here. |
| [8059](../../../foundations/error-codes.md#error-8059) | 400 | The tableName is not part of the workspace or is not joined to the base table. |
| [8092](../../../foundations/error-codes.md#error-8092) | 400 | reportType resolves to a view kind that cannot be saved standalone. |
| [8144](../../../foundations/error-codes.md#error-8144) | 400 | chartType is not a recognised chart name. |
| [8145](../../../foundations/error-codes.md#error-8145) | 400 | folderId was supplied. |
| [8147](../../../foundations/error-codes.md#error-8147) | 400 | settings was supplied for a non-pivot report. |
| [8162](../../../foundations/error-codes.md#error-8162) | 400 | rangeSize was supplied as a string, or on an operation that does not support ranges. |
| [8166](../../../foundations/error-codes.md#error-8166) | 400 | The operation is incompatible with the column's data type. |
| [8167](../../../foundations/error-codes.md#error-8167) | 400 | The filterType is not valid for the column type + operation combination. |
| [8168](../../../foundations/error-codes.md#error-8168) | 400 | A values entry does not match the expected format for the filterType. |
| [8170](../../../foundations/error-codes.md#error-8170) | 400 | An axis type is not valid for the chosen reportType. |
| [8191](../../../foundations/error-codes.md#error-8191) | 400 | An invalid date value was supplied to a date filter. |
| [8250](../../../foundations/error-codes.md#error-8250) | 400 | compType is not applicable to the column category — e.g. slider on a dimension, singleSelect on a measure. |
| [8252](../../../foundations/error-codes.md#error-8252) | 400 | reportType is absent or null. |
| [8253](../../../foundations/error-codes.md#error-8253) | 400 | A mandatory userFilters key is missing, typically compType or filterType. |
| [8254](../../../foundations/error-codes.md#error-8254) | 400 | A geoRole value is wrong for the column type. |
| [8255](../../../foundations/error-codes.md#error-8255) | 400 | geoRole was supplied on a column that cannot be geocoded. |
| [8256](../../../foundations/error-codes.md#error-8256) | 400 | More than one geo operation on the same axis. |
| [8257](../../../foundations/error-codes.md#error-8257) | 400 | A numeric geo column coexists with a categorical geo column. |
| [8258](../../../foundations/error-codes.md#error-8258) | 400 | A categorical geo column was placed on an axis other than X. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | LESSTHANMINOCCURANCE — CONFIG was not sent. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | MORETHANMAXLENGTH — roleName exceeds 30 characters, or permissions exceeds its size limit. |
| [8509](../../../foundations/error-codes.md#error-8509) | 400 | PATTERNNOTMATCHED — roleName contains disallowed characters, or accessType is not one of the three values. |
| [8516](../../../foundations/error-codes.md#error-8516) | 400 | UNABLETOPARSEDATATYPE — A CONFIG value has the wrong JSON type. |
| [8517](../../../foundations/error-codes.md#error-8517) | 400 | A field has the wrong JSON data type — exclude: "yes", isAxisMerge: "maybe", compType: 123. |
| [8534](../../../foundations/error-codes.md#error-8534) | 400 | JSONPARSEERROR — CONFIG is not valid JSON. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |
| [8542](../../../foundations/error-codes.md#error-8542) | 400 | An unknown key is present in CONFIG, or a windowFunction is mis-configured. |

# Related

- [Reports & Dashboards](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
