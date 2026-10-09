---
type: Reference
title: Report and dashboard enumerations
description: Every enumerated CONFIG value shared by the Zoho Analytics REST API v2 report and dashboard endpoints - chart types, axis types and which report type accepts them, operations and the column data types they apply to, filter operations and types, user-filter widgets, dashboard card types and the layout grid rules.
tags:
  - zoho-analytics
  - rest-api-v2
  - reports
  - dashboards
  - enumerations
  - charts
sources:
  - id: md-reports
    resource: "/domains/reports-and-dashboards/reports/overview.md"
    title: Reports - group overview (the Reports source document and its appendices)
  - id: md-dashboards
    resource: "/domains/reports-and-dashboards/dashboards/overview.md"
    title: Dashboards - group overview (the Dashboards source document and its appendices)
  - id: oas-reports-dashboards
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: "team:zoho-analytics-api-docs"
generated:
  at: {{NOW}}
status: stable
---

# Summary

The report and dashboard endpoints share one CONFIG vocabulary. This document is the single place that vocabulary is enumerated, so the endpoint documents can name a value without repeating the whole list. The source documents of the Reports and Dashboards groups are the source of truth; the OpenAPI enumerations in [`/references/openapi/`](/references/openapi/reports-dashboards-grouped-api.json) are kept equal to them.

| Endpoint | Uses |
|---|---|
| [Create Report](/domains/reports-and-dashboards/reports/create-report.md) · [Update Report](/domains/reports-and-dashboards/reports/update-report.md) | `reportType`, `chartType`, `axisColumns[].type`, `axisColumns[].operation`, `filters`, `userFilters` |
| [Read Report Metadata](/domains/reports-and-dashboards/reports/get-report-metadata.md) | the same values in the response - lowercase axis types, reverse-derived operations |
| [Create Dashboard](/domains/reports-and-dashboards/dashboards/create-dashboard.md) · [Update Dashboard](/domains/reports-and-dashboards/dashboards/update-dashboard.md) | card `type`, grid rules, `themes`, `settings` |
| [Read Dashboard Metadata](/domains/reports-and-dashboards/dashboards/get-dashboard-metadata.md) | the same values in the response |

A *report* is called a **visual**, an **analysis view** and simply a **view** interchangeably across request fields, responses and error messages. All four terms mean the same object.

# Report Types

`reportType` is required on create and update. Lowercase only (`Chart` is rejected with `8509`).

| Value | Creates |
|---|---|
| `chart` | A chart. `chartType` is then required in practice. |
| `pivot` | A pivot table with row, column and data shelves. |
| `summary` | A summary view with grouping and aggregate columns. |

Read Report Metadata may return `widget` for widget-backed views; Create and Update reject it.

# Chart Types

`chartType` applies only when `reportType` is `chart`. It is matched case-insensitively; only letters, digits and spaces are allowed (no hyphens or underscores, max 50 characters). An unrecognised name raises `8144`; omitting it, or sending an empty string, makes the server choose a chart automatically.

| Family | Accepted values |
|---|---|
| Area | `area`, `area with points`, `area without points`, `area with markers`, `area without markers`, `smooth area`, `smooth area with points`, `smooth area without points`, `smooth area with markers`, `smooth area without markers` |
| Stacked area | `stacked area`, `stacked area with points`, `stacked smooth area`, `stacked smooth area with points`, `stacked smooth area without points`, `stacked smooth area with markers`, `stacked smooth area without markers` |
| Bar | `bar`, `horizontal bar`, `stacked bar`, `horizontal stacked bar`, `butterfly` |
| Line | `line`, `line with points`, `line without points`, `line with markers`, `line without markers`, `smooth line`, `smooth line with points`, `smooth line without points`, `smooth line with markers`, `smooth line without markers`, `step` |
| Pie family | `pie`, `ring`, `semi pie`, `semi ring`, `funnel`, `pyramid` |
| Bubble and scatter | `bubble`, `packed bubble`, `scatter` |
| Combo | `combo`, `combo bar with smooth line` |
| Map | `map area`, `map filled`, `map bubble`, `map pie`, `map pie bubble`, `map bubble pie`, `map scatter`, `geo heat map` |
| Web | `web`, `web with fill`, `web without fill` |
| Other | `heat map`, `table chart` |

On read, `chartType` is reverse-derived from storage: where several names share one stored pair the returned name is one of them (`area` / `area without points` / `area without markers`; `line` / `line with points` / `line with markers`; `map area` / `map filled`; `web` / `web with fill`), and for `stacked area without points` / `stacked area without markers` the key is omitted.

# Axis Types

The `type` of an `axisColumns` entry passes a pattern check *before* it is matched against the report type: exactly the spellings below are accepted. Using a type outside its report family raises `8170`.

| Accepted spellings | Valid for | Notes |
|---|---|---|
| `xaxis`, `xAxis`, `XAxis` | `chart` | Primary dimension axis. Required for charts (`7701`). |
| `yaxis`, `yAxis`, `YAxis` | `chart` | Measure axis. Required for charts. Maximum 15 (`7727`). |
| `textaxis`, `textAxis` | `chart` | Text/label axis. |
| `coloraxis`, `colorAxis` | `chart` | Colour-encoding axis. Cannot coexist with multiple Y axes (`7703`). |
| `sizeaxis` | `chart` | Size-encoding axis for bubble charts. **Lowercase only** - `sizeAxis` is rejected with `8509`. |
| `latlng`, `latLng` | `chart` | Latitude/longitude pair for map charts. |
| `tooltip`, `toolTip` | `chart` | Extra columns surfaced in the tooltip. |
| `custom` | `chart` | Custom-visual field slot. |
| `row` | `pivot` | Row grouping shelf. |
| `column` | `pivot` | Column grouping shelf. |
| `data` | `pivot` | Measure shelf. At least one is required. |
| `groupby`, `groupBy` | `summary` | Dimension grouping shelf. |
| `summarize` | `summary` | Aggregate shelf. |

Read Report Metadata always returns the type **lowercase** (`xaxis`, `yaxis`, `coloraxis`, `textaxis`, `groupby`, `tooltip`, `latlng`). A `tooltip` column may come back as `group`, which Create and Update reject with `8509`.

# Operations

`axisColumns[].operation` is pattern-checked as letters only (`8509` otherwise); a value that is not in the map for the column's data type raises `8166`. `std` is **not** a valid axis operation - use `stddev` (`std` is accepted only in `filters`).

| Column and shelf | Operations |
|---|---|
| Numeric column on a chart | `sum`, `min`, `max`, `average`, `avg`, `stddev`, `median`, `mode`, `percentile`, `count`, `variance`, `dc`, `distinctcount`, `measure`, `dimension`, `range`, `actual`, `geo` |
| Numeric column on a pivot `data` shelf | `sum`, `min`, `max`, `average`, `stddev`, `median`, `mode`, `percentile`, `count`, `variance`, `dc`, `distinctcount` - `avg` is **not** accepted here |
| Numeric column on a pivot `row` / `column` shelf | `dimension`, `range` only |
| Text, email, URL, multi-line column | `actual`, `count`, `dc`, `distinctcount`, `geo` |
| Date column on a chart - grouping | `year`, `quarter`, `month`, `week`, `weekday`, `day`, `hour` |
| Date column on a chart - absolute grouping | `quarteryear` (alias `absquarter`), `monthyear` (alias `absmonth`), `weekyear` (alias `absweek`), `fulldate`, `datetime` |
| Date column on a chart - aggregates | `count`, `distinctcount`, `maxdate`, `mindate` |
| Date column - distinct-count variants | `ydc`, `mydc`, `wydc`, `qydc`, `ddc`, `dtdc`, `qdc`, `wdc`, `wddc`, `dmdc`, `hdc`, `mdc` |
| Date column on a pivot `data` shelf | `maxdate`, `mindate`, `count`, `distinctcount`, and the distinct-count variants |
| Date column on a pivot `row` / `column` shelf | the grouping operations (no aggregates) |

`dimension` and `range` convert a measure into a dimension; `range` honours `rangeSize` (a JSON number: a string raises `8162`, an array `8516`). Window functions are not available on either, nor on a date column unless its operation is `count`.

On read, operations are reverse-derived: `average`/`avg`, `absquarter`/`quarteryear`, `absmonth`/`monthyear`, `absweek`/`weekyear`, `actual`/`geo` and `variance`/`dc`/`distinctcount` collapse, and all thirteen date distinct-count operations share one stored marker.

## Geo roles

Set `operation` to `geo` and supply `geoRole`:

| Column type | `geoRole` | Placement |
|---|---|---|
| Text / categorical | `continent`, `country`, `state`, `province`, `county`, `district`, `city`, `zipcode`, `airport` | X axis only (`8258` otherwise) |
| Numeric | `latitude`, `longitude` | X or Y axis |

At most one categorical geo column on X and one numeric geo column per axis (`8256`); the two kinds cannot coexist (`8257`); a role that does not suit the column type raises `8254`; a column that cannot be geocoded raises `8255`. `geoRole` is not returned by Read Report Metadata, so a geo column cannot be round-tripped.

## Window functions

`windowFunction.type`: chart reports accept `normal`, `runtotal`, `pctoftotal`, `difffrom`, `pctdifffrom`, `pctofprevval`, `hundredpctgrp`, `movingcalc` (alias `movingcalculation`); pivot reports accept `normal`, `pctofrow`, `pctofcol`, `pctofparrow`, `pctofparcol`, `pctoftotal`, `runtotal`, `difffrom`, `pctdifffrom`, `pctofprevval`. `difffrom`, `pctdifffrom` and `movingcalc` need `baseField`; `movingcalc` needs `movingCalculation` (`calculation` one of `average`, `sum`, `min`, `max`). `pctoftotal` is not available on `average`, `stddev`, `variance`, `dc` or `distinctcount` columns.

# Filter Operations and Types

## Static filters (`filters`)

Every entry needs `columnName`, `operation`, `filterType`, `values` (strings) and `exclude` (a JSON boolean). Values are matched case-insensitively. A mismatch between column type, `operation` and `filterType` raises `8167`; a value in the wrong shape raises `8168` (`8191` for malformed dates).

| Column type | `operation` | `filterType` |
|---|---|---|
| Numeric | `measure`, `dimension`, `sum`, `min`, `max`, `average`, `stddev`, `std`, `count`, `variance`, `dc`, `distinctcount`, `median`, `mode`, `actual`, `aggregate` | `individualvalues`, `range`, `ranking`, `rankingpct` |
| Text | `actual`, `count`, `dc`, `distinctcount`, `geo` | `individualvalues` (alias `individual`), `wildcard` |
| Date - absolute | `actual`, `range`, `daterange` | `year`, `quarter`, `month`, `week`, `weekday`, `day`, `hour`, `quarteryear` (alias `absquarter`), `monthyear` (alias `absmonth`), `weekyear` (alias `absweek`), `date`, `fulldate`, `datetime`, `range`, `daterange`, `common` |
| Date - seasonal | `seasonal` | `quarter`, `month`, `week`, `weekday`, `day`, `hour` |
| Date - relative | `relative` | `common`, `year`, `quarter`, `month`, `week`, `day`, `hour` |

A `wildcard` filter carries a `wildcard` object: up to 15 `criteria` entries, each `{"operation": ..., "value": "<max 5000>"}` with `operation` one of `CONTAINS`, `DOES_NOT_CONTAIN`, `IS`, `IS_NOT`, `STARTS_WITH`, `DOES_NOT_START_WITH`, `ENDS_WITH`, `DOES_NOT_END_WITH`, and an `expression` that combines them by 1-based index and **must be wrapped in parentheses** (`"(1 AND 2 OR 3)"`, max 100 characters; `8509` without the parentheses).

## User filters (`userFilters`)

| Column type | `operation` | `compType` | `filterType` |
|---|---|---|---|
| Text | `actual` (implied; the key is ignored) | `singleSelect`, `multiSelect` | not required |
| Numeric | `sum`, `min`, `max`, `average`, `stddev`, `std`, `count`, `variance`, `dc`, `distinctcount`, `median`, `mode`, `measure`, `dimension`, `actual`, `aggregate` | `slider`, `multiSelect` | required - `individualvalues`, `range`, `ranking`, `rankingpct` |
| Date - absolute | `actual` | `singleSelect`, `multiSelect` | required - the absolute list above |
| Date - seasonal | `seasonal` | `singleSelect`, `multiSelect` | required - `quarter`, `month`, `week`, `weekday`, `day`, `hour` |
| Date - relative | `relative` | `singleSelect`, `multiSelect` | `common` |
| Date - range | `daterange` / `range` | `dateRange` | not required |

`behaviour` (`ListAllValues`, `ListRelevantValues`, `ListOnlyRelevantValues`) applies to the select-style widgets only; with `daterange` or `relative` it raises `8008`. A `compType` that does not suit the column raises `8250`; a missing required key raises `8253`. `exclude: true` is not allowed with `daterange`. If `isallval` is omitted it is derived from `values` (non-empty implies `false`); when `isallval` is `true`, `values` is ignored.

Read Report Metadata reduces every user filter to `tableName`, `columnName` and `operation`, and for date columns puts a `filterType`-shaped value into `operation` that Update rejects with `8166`.

## Filter value formats

| `filterType` | Example `values` |
|---|---|
| `individualvalues` (text) | `["East", "West"]` |
| `individualvalues` (numeric) | `["100", "200"]` - exact stored values, no rounding |
| `range` (numeric) | `["1000 and below"]`, `["200000 to 300000"]`, `["500000 and above"]` |
| `ranking` | `["Top 2"]`, `["Bottom 10"]` |
| `rankingpct` | `["Top 10"]` (a percentage) |
| `year` | `["2012", "2023"]` |
| `quarteryear` | `["Q1 2020", "Q2 2023"]` |
| `monthyear` | `["Aug 2012", "Jan 2013"]` - three-letter month abbreviations only |
| `weekyear` | `["W03 2012", "W02 2023"]` |
| `fulldate` / `date` | `["27 Jan, 2023", "20 Mar, 2023"]` |
| `datetime` | `["27 Jan 2023 00:00:00"]` |
| `daterange` / `range` (date) | `["from 10 Dec 2013 00:00:00"]`, `["10 Mar 2012 00:00:00 to 10 Dec 2012 00:00:00"]`, `["to 11 Mar 2013 00:00:00"]` |
| `quarter`, `month`, `week`, `weekday`, `day`, `hour` (seasonal) | `["Q1", "Q3"]`, `["Jan", "Feb"]`, `["Week 2"]`, `["Sun", "Mon"]`, `["01", "15"]`, `["10", "23"]` |
| `common` (relative) | `["This Year"]`, `["Last Month"]`, `["Last 2 Years"]` - `Last N <unit>` and `Next N <unit>` |
| `wildcard` | `values` is unused; the criteria live in the `wildcard` object |

# Dashboard Card Types

`layout` is written as a **JSON-encoded string** and read back as a JSON object keyed by string card IDs (`"1"`, `"2"`, ...). The keys carry no meaning beyond uniqueness; the read API renumbers cards from `"1"` in storage order. Every card carries `type`, `width`, `height`, `left` and `top`.

| `type` | Extra fields | Min height | Min width | Notes |
|---|---|---:|---:|---|
| `VIEW` | `viewName` | 5 | 10 | Embeds a saved report by display name, matched case-insensitively. The view must exist (`8027`) and be readable by the caller (`7481`). `properties` on a VIEW card is ignored. |
| `HTML` | `content` | 1 | 5 | Free HTML block, XSS-filtered before storage. |
| `TITLE` | `content` | 3 | 5 | Heading card. |
| `PARA` | `content` | 1 | 5 | Paragraph / text card. |
| `IMAGE` | `content` | 3 | 5 | Image card. A digits-only `content` is a stored file ID. |
| `EMBED` | `content` | 5 | 5 | External URL / iframe embed. |
| `USERFILTERS` | - | 1 | **80** | The interactive filter panel. Must span the full grid width. |
| `DELETED` | `viewId` (optional) | 5 | 10 | Placeholder left behind when an embedded view is removed. Present in read responses with `respContent`; accepted on write for round-tripping. |

`content` must be non-empty on every card type that needs it: an absent key, `null` and `""` all raise `7483`.

# Dashboard Layout Grid

The canvas is **80 units wide** with unbounded height. The rules are enforced in this order, each with its own error code:

| # | Rule | Error |
|---|---|---|
| 1 | All five positional fields present | `7479` |
| 2 | `width`, `height`, `left`, `top` are JSON integers and `type` is a JSON string | `7486` |
| 3 | `type` is one of the eight card types | `7485` |
| 4 | `left >= 0`, `top >= 0`, `width > 1`, `height > 1`, `left + width <= 80` | `7480` |
| 5 | The card meets the per-type minimum size | `7512` |
| 6 | Non-`VIEW`, non-`USERFILTERS` cards carry a non-empty `content` | `7483` |
| 7 | `VIEW` cards resolve to a view that exists and that the caller can read | `8027`, `7481` |
| 8 | No two cards overlap | `7482` |
| 9 | At most 100 cards | `7484` |
| 10 | At least one card is not a `USERFILTERS` card | `9001` |

`layoutType` set to `1`, `2`, `3` or `4` switches the server into auto-layout: the geometry you supply is discarded and a full-width `USERFILTERS` card, one `HTML` card per `content` value and one `VIEW` card per distinct `viewName` are generated in that many columns. Omitting `layoutType`, or sending `0`, keeps the layout as submitted; other values raise `8509`. On Update, each supplied section (`layout`, `themes`, `settings`) **replaces** the stored one in full.

# Dashboard Settings and Themes

`settings` flags (`allowDrillDown`, `hideColumnOptions`, `smartAlignCharts`, `enableSortMenu`, `reportAsFilter`, `showContextualOptions`, `allowVUD`, `allowInsights`, `allowEmbedInsights`, `fitToWidth`, `enableGlobalUF`, `enableGlobalValueUF`, `applyImmediateUF`, `timeSlicer`, `mapSync`) take `"true"` / `"false"`; `layoutType` is one of `web`, `custom_width`, `tabloid_1056`, `letter_816`, `a4_797`, `a3_1123` (`mobile` is not valid); `layoutWidth` is a string of 1-4 digits; `allowExport` holds `csv`, `excel`, `html`, `image`, `pdf`, `zohoSheet` (an omitted sub-key is stored as `"false"`); `allowAllExport` is a single master switch.

`themes` is either the default theme (`{"default": "true"}` and nothing else, `7493` otherwise) or an explicit theme whose `type` (`solid`, `gradient`, `image`) decides which sub-object and which `card` keys are required (`7491`, `7492`). Colours are `#RRGGBB` or `#RGB` only (`8509`); `card.border.width` is written to all four edges; `chartEffect.apply` is `1` or `2`, with `chartEffect.type` forbidden for `1` (`7513`) and required for `2` (`7514`); `palette` is accepted but unsupported. The full key list with ranges is in the Create Dashboard document.

# Related

- [Reports](/domains/reports-and-dashboards/reports/overview.md) and [Dashboards](/domains/reports-and-dashboards/dashboards/overview.md) - the group overviews, including the round-tripping rules.
- [Filter criteria syntax](/foundations/filter-criteria-syntax.md) - the grammar of the `criteria` expression used by exports and shares.
- [Export formats and enumerations](/foundations/export-formats-and-enums.md) · [Import options and enumerations](/foundations/import-options-and-enums.md) - the equivalent vocabularies for the export and import families.
- [Error code catalog](/foundations/error-codes.md)
