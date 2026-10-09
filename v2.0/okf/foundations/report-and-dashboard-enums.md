---
type: Reference
title: Report and dashboard enumerations
description: Every enumerated CONFIG value shared by the Zoho Analytics REST API v2 report and dashboard endpoints - chart types, axis types and which report type accepts them, aggregate operations and the column data types they apply to, filter types, dashboard card types and the layout grid rules.
tags:
  - zoho-analytics
  - rest-api-v2
  - reports
  - dashboards
  - enumerations
  - charts
sources:
  - id: oas-reports-dashboards
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: "team:zoho-analytics-api-docs"
  - id: md-reports
    resource: "/domains/reports-and-dashboards/reports/overview.md"
    title: Reports - group overview
  - id: md-dashboards
    resource: "/domains/reports-and-dashboards/dashboards/overview.md"
    title: Dashboards - group overview
  - id: team-visual-api
    resource: "https://www.zoho.com/analytics/api/v2/"
    title: "Visual APIs - Documentation (Zoho Analytics API team, internal hand-off, 2026-10)"
    author: "team:zoho-analytics-api-docs"
  - id: team-dashboard-api
    resource: "https://www.zoho.com/analytics/api/v2/"
    title: "Dashboard APIs - Documentation (Zoho Analytics API team, internal hand-off, 2026-10)"
    author: "team:zoho-analytics-api-docs"
generated:
  by: claude-opus-5/claude-code
  at: 2026-10-05T00:00:00Z
status: stable
---

# Summary

The six report and dashboard endpoints share one CONFIG vocabulary. This document is the single place that vocabulary is enumerated, so the endpoint documents can name a value without repeating the whole list.

| Endpoint | Uses |
|---|---|
| [Create Visual (report)](../domains/reports-and-dashboards/reports/create-report.md) · [Update Visual](../domains/reports-and-dashboards/reports/update-report.md) | `reportType`, `chartType`, `axisColumns[].type`, `axisColumns[].operation`, `filters`, `userFilters` |
| [Read Visual metadata](../domains/reports-and-dashboards/reports/get-report-metadata.md) | the same values, in the response |
| [Create Dashboard](../domains/reports-and-dashboards/dashboards/create-dashboard.md) · [Update Dashboard](../domains/reports-and-dashboards/dashboards/update-dashboard.md) | `layout.*.type`, grid rules, `themes`, `settings` |
| [Read Dashboard metadata](../domains/reports-and-dashboards/dashboards/get-dashboard-metadata.md) | the same values, in the response |

A *report* is called a **view**, a **visual** and an **analysis view** interchangeably across request fields, responses and error messages. All three mean the same object.

The values here are the API team's Dashboard and Visual API documents, which are the source of truth for this family. Where they previously disagreed with the OpenAPI enumerations, the specifications in [`/references/openapi/`](../references/openapi/reports-dashboards-grouped-api.json) were corrected to match - see [Source and precedence](#source-and-precedence).

# Report Types

`reportType` is required on create and update. Lowercase only.

| Value | Creates |
|---|---|
| `chart` | A chart view. `chartType` is then required. |
| `pivot` | A pivot table. |
| `summary` | A summary view. |

# Chart Types

`chartType` applies only when `reportType` is `chart`; it is ignored otherwise. All values are lowercase, and spaces are part of the value. The 47 values below are the complete enumeration, and are the `enum` the [OpenAPI specification](../references/openapi/reports-dashboards-grouped-api.json) validates against.

| Family | Values |
|---|---|
| Area | `area`, `area with points`, `area without points`, `smooth area`, `smooth area with points`, `smooth area without points`, `stacked area`, `stacked area with points`, `stacked smooth area`, `stacked smooth area with points`, `stacked smooth area without points` |
| Bar | `bar`, `horizontal bar`, `stacked bar`, `horizontal stacked bar` |
| Bubble | `bubble`, `packed bubble` |
| Combo | `combo`, `combo bar with smooth line` |
| Funnel and pyramid | `funnel`, `pyramid` |
| Line | `line`, `line with points`, `line without points`, `smooth line`, `smooth line with points`, `smooth line without points`, `step` |
| Map | `map area`, `map bubble`, `map filled`, `map pie`, `map pie bubble`, `map bubble pie`, `map scatter`, `geo heat map` |
| Pie and ring | `pie`, `ring`, `semi pie`, `semi ring` |
| Scatter | `scatter` |
| Web | `web`, `web with fill`, `web without fill` |
| Heat map | `heat map` |
| Other | `butterfly`, `table chart` |

# Axis Types

Each entry of `axisColumns` carries a `type` that says what role the column plays. Which types are legal depends on `reportType` - a `pivot` report has no `xAxis`, and a `chart` has no `row`.

| Axis type | `chart` | `pivot` | `summary` | Role |
|---|:---:|:---:|:---:|---|
| `xAxis` | yes | no | no | Primary categorical/dimension axis. |
| `yAxis` | yes | no | no | Measure axis. At most 15 columns. |
| `textAxis` | yes | no | no | Text label axis, for chart types that support one. |
| `colorAxis` | yes | no | no | Colour-encoding axis. Cannot coexist with multiple `yAxis` columns - that combination fails with `7703`. |
| `sizeAxis` | yes | no | no | Size-encoding axis, used by bubble charts. |
| `tooltip` | yes | no | no | Column surfaced in the hover tooltip. |
| `row` | no | yes | no | Row grouping axis. |
| `column` | no | yes | no | Column grouping axis. |
| `data` | no | yes | no | Measure axis. Requires an aggregate `operation`. |
| `groupBy` | no | no | yes | Dimension grouping axis; the column must be non-numeric. At most 20 columns. |
| `summarize` | no | no | yes | Measure axis. Requires an aggregate `operation`. |
| `custom` | yes | yes | yes | Producer-defined role. |

# Operations

`axisColumns[].operation` says how the column is aggregated or how a date is bucketed. The value must suit the column's data type.

| Column data type | Operations that apply |
|---|---|
| Numeric (positive integer, decimal, number) | `sum`, `avg`, `min`, `max`, `std`, `count`, `dc`, `actual`, `geo` |
| Plain text, email, URL, multi-line (dimensions) | `actual`, `count`, `dc`, `geo` |
| Date | `actual`, `year`, `quarteryear`, `monthyear`, `weekyear`, `fulldate`, `datetime`, `quarter`, `month`, `week`, `weekday`, `day`, `hour`, `count`, `dc` |

The OpenAPI specification additionally accepts `variance`, `percentile`, `dimension`, `range`, `absQuarter` and `seasonal`. They are not described in the source documents, so treat them as present but unverified.

Rules that hold regardless of type:

1. Aggregates (`sum`, `avg`, `std`) cannot be applied to a date or text column.
2. Date bucketing operations (`year`, `month`, `quarter`, …) cannot be applied to a numeric or text column.
3. `geo` applies to a text column with a categorical `geoRole`, or to a numeric column with `geoRole` of `latitude` or `longitude`.
4. In a `pivot` report the `data` axis needs an aggregate; `row` and `column` take dimensional operations.
5. In a `summary` report `groupBy` takes dimensional operations and `summarize` takes aggregates.

`geoRole` accepts `latitude`, `longitude` or `location`. `sort` accepts `asc` or `desc`.

# Dashboard Card Types

`layout` is a JSON object keyed by card index strings (`"1"`, `"2"`, …). Every card carries `type`, `width`, `height`, `left` and `top`; the type decides which further fields are required.

| `type` | Also requires | Notes |
|---|---|---|
| `VIEW` | `viewName`, and optionally `properties` | Embeds a saved view by **display name**. The name must resolve to a view the caller can see, otherwise `7481`. `properties` may be `{}`. |
| `HTML` | `content` | Raw HTML. An absent or null `content` fails with `7483`. |
| `TITLE` | `content` | Heading card. |
| `PARA` | `content` | Paragraph card. |
| `IMAGE` | `content` | Image URL or base64 data URI. |
| `EMBED` | `content` | External URL or iframe markup. |
| `USERFILTERS` | nothing beyond the positional fields | Renders the interactive filter panel for the user filters of the embedded views. |
| `DELETED` | nothing | Tombstone for a card removed from the layout. |

# Dashboard Layout Grid

The canvas is a grid **80 units wide**, with unbounded height.

| Rule | Detail |
|---|---|
| Horizontal bound | `left + width` must not exceed `80`. `left` is 0-based, so its maximum is `79`. |
| No overlap | Two cards may not occupy the same grid cell. |
| Card count | A dashboard holds at most **100** cards. |
| Value type | `width`, `height`, `left` and `top` must be plain integers. Strings, floats and `null` are rejected. |
| Minimum size | `width` and `height` are at least `2`. `USERFILTERS` needs at least `3` height and `HTML` at least `5`. |
| Replacement semantics | On [Update Dashboard](../domains/reports-and-dashboards/dashboards/update-dashboard.md) the `layout` object **replaces** the previous layout in full - any card absent from the new object is removed. |

`layoutType` selects a column preset at creation: `0` free form, `1` single column, `2` two columns, `3` three columns, `4` four columns.

# Filter Types

`filters` holds static criteria baked into the report; `userFilters` holds the interactive widgets shown to a viewer. `filterType` must suit the column and its operation.

| `filterType` | Applies to | Value format |
|---|---|---|
| `individualValues` | numeric or text, `actual` | `["100", "200"]`, `["East", "West"]` |
| `range` | numeric, `actual` | `"1000 and below"`, `"200000 to 300000"`, `"500000 and above"` |
| `ranking` | numeric, `actual` | `"Top 2"`, `"Top 5"`, `"Bottom 10"` |
| `year` | date, `actual` | `"2012"`, `"2023"` |
| `quarteryear` | date, `actual` | `"Q1 2020"`, `"Q2 2023"` |
| `monthyear` | date, `actual` | `"Aug 2012"` - three-letter month abbreviations only |
| `weekyear` | date, `actual` | `"W03 2012"` |
| `fulldate` or `date` | date, `actual` | `"27 Jan, 2023"` - three-letter month abbreviations only |
| `datetime` | date, `actual` | `"27 Jan 2023 00:00:00"` |
| `dateRange` | date, `range` | `"from 10 Dec 2013 00:00:00"`, `"10 Mar 2012 00:00:00 to 10 Dec 2012 00:00:00"`, `"to 11 Mar 2013 00:00:00"` |
| `quarter` | date, `seasonal` | `"Q1"` … `"Q4"` |
| `month` | date, `seasonal` | `"Jan"` … `"Dec"` |
| `week` | date, `seasonal` | `"Week 2"` |
| `weekDay` | date, `seasonal` | `"Sun"` … `"Sat"` |
| `day` | date, `seasonal` | `"01"`, `"15"`, `"31"` |
| `hour` | date, `seasonal` | `"10"`, `"13"`, `"23"` |
| `wildcard` | text, `actual` | requires a `wildcard` object |

Rules specific to `userFilters`:

1. A `dateRange` operation takes a single-element `values` array of the form `"DD Mon YYYY to DD Mon YYYY"`. Both `compType` and `filterType` must be absent.
2. A `relative` operation requires `filterType: "common"`. Values look like `"This Year"`, `"Last Month"`, `"Last 2 Years"`, or `"Last N <unit>"` / `"Next N <unit>"`.
3. A numeric measure filter using the `slider` `compType` takes numbers, not strings.
4. `behaviour` does not apply to `dateRange` or `relative`; supplying it returns `8008`.

# Source and Precedence

This document and the OpenAPI specifications in [`/references/openapi/`](../references/openapi/reports-dashboards-grouped-api.json) are both derived from the API team's **Dashboard APIs** and **Visual APIs** documents, which are the source of truth for this endpoint family.

Five points where the previous OpenAPI enumerations disagreed with those documents were resolved in favour of the documents, and the specifications were corrected:

| Field | Was | Now |
|---|---|---|
| `axisColumns[].operation` | `average`, `distinctCount`, `stdDev`, `monthYear`, `dateTime` | `avg`, `dc`, `std`, `monthyear`, `datetime` |
| `axisColumns[].operation` | no date sub-type values beyond `year`/`quarter`/`month` | adds `quarteryear`, `weekyear`, `week`, `weekday`, `fulldate`, `day`, `hour` |
| `axisColumns[].type` | `sizeaxis` | `sizeAxis` |
| dashboard `displayName` | `maxLength: 100` | `maxLength: 200` |
| report `title`, `axisColumns` | optional | required on create |
| dashboard card `width`, `height` | `minimum: 1` | `minimum: 2` |

Two values the specification carries that the source documents do not describe - the `tooltip` and `custom` axis types, and the `PARA` and `DELETED` card types - were **kept**, because the documents enumerate what a caller may send rather than asserting that nothing else is accepted. Removing them could reject a request the service still honours. Confirm them against the service before relying on either.

# Related

- [Reports](../domains/reports-and-dashboards/reports/overview.md) and [Dashboards](../domains/reports-and-dashboards/dashboards/overview.md) - the group overviews.
- [Filter criteria syntax](filter-criteria-syntax.md) - the grammar of the `criteria` expression used by report filters.
- [Export formats and enumerations](export-formats-and-enums.md) · [Import options and enumerations](import-options-and-enums.md) - the equivalent vocabularies for the export and import families.
- [Error code catalog](error-codes.md)
