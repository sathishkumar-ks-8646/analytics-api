---
type: Reference
title: Export formats and enumerations
description: Every enumerated CONFIG attribute shared by the Zoho Analytics REST API v2 export endpoints and email schedules - responseFormat, CSV delimiters, PDF page setup, header and footer slots, image options, email exportType - with default values and error codes.
tags:
  - zoho-analytics
  - rest-api-v2
  - export
  - enums
  - csv
  - pdf
  - formats
sources:
  - id: md-sync-export
    resource: /domains/data-operations/sync-data-export/overview.md
    title: Synchronous Data Export - group overview
  - id: md-async-export
    resource: /domains/data-operations/async-data-export/overview.md
    title: Asynchronous Data Export - group overview
  - id: md-email
    resource: /domains/schedules-and-alerts/email-schedules/overview.md
    title: Email Schedules - group overview
generated:
  at: {{NOW}}
status: stable
---

# Summary

The synchronous export, the two asynchronous export jobs and the email schedules share one vocabulary for output format and layout. A CONFIG proven on one works on the others, with the exceptions noted. Out-of-range enumerated values fail with `8119` unless a specific code is listed.

# responseFormat (exports)

Default `csv`; invalid values fail with `8001`.

| Value | Output | Notes |
|---|---|---|
| `csv` | Delimited text | Options: `delimiter`, `recordDelimiter`, `quoted`. |
| `json` | JSON document | |
| `xml` | XML document | |
| `xls` | Excel workbook | Limits: 65,536 rows per sheet (`7806`), 256 columns (`7807`), 32,767 characters per cell (`7808`). |
| `pdf` | PDF document | Page setup options below; 1,000,000 cell limit (`7827`). |
| `html` | HTML fragment | `includeTitle`, `includeDesc`, `columnWidthRatio`. |
| `image` | PNG or JPEG | **Chart views only** (`8014` otherwise). `imageFormat`, width and height options. |

Synchronous export additionally rejects dashboards, query tables, live-connect views and tables above 1,000,000 rows with `8133`; use the asynchronous export for those. Total synchronous payload limit 100 MB (`7830`).

# CSV Options

| Attribute | Default | Values |
|---|---|---|
| `delimiter` | `0` | `0` comma, `1` tab, `2` semicolon, `3` space, `4` pipe |
| `recordDelimiter` | `0` | `0` DOS `\r\n`, `1` UNIX `\n`, `2` MAC `\r` |
| `quoted` | none | `0` single quote, `1` double quote |

# PDF Options

| Attribute | Default | Values |
|---|---|---|
| `paperSize` | `4` | `0` Letter, `1` Legal, `2` Tabloid, `3` A3, `4` A4, `5` Auto-fit (width grows with visible columns) |
| `paperStyle` | `Portrait` | `Portrait`, `Landscape` |
| `showTitle`, `showDesc` | `0` | `0` top, `1` bottom, `2` do not include |
| `columnWidthRatio` | `1` (PDF), `2` (HTML) | `0` proportional to view widths, `1` sized to content, `2` all equal |
| `exportLanguage` | `0` | `0` English, `1` Chinese, `2` Japanese, `3` European, `4` Korean font set |
| `dashboardLayout` | - | Dashboard export layout (asynchronous export only) |

Header and footer slots `leftHeader`, `centerHeader`, `rightHeader`, `leftFooter`, `centerFooter`, `rightFooter`:

| Value | Content |
|---|---|
| `0` | Blank |
| `1` | View title |
| `2` | Export date |
| `3` | Page number |
| `4` | Page number with total |
| `5` | Custom text from the matching `...Text` attribute (for example `leftHeaderText`) |
| `6` | Logo |

Defaults: `leftHeader` `1`, `centerHeader` `0`, `rightHeader` `2`, `leftFooter` `0`, `centerFooter` `3`, `rightFooter` `0`.

# HTML Options

`includeTitle`, `includeDesc` use the same `0` top / `1` bottom / `2` omit values as the PDF title options; `columnWidthRatio` defaults to `2`.

# Image Options

| Attribute | Default | Values |
|---|---|---|
| `imageFormat` | `png` | `png`, `jpg`, `jpeg` (`8017` otherwise) |
| `width` | - | 250 to 2000 pixels (`7803` outside) |
| `height` | - | 200 to 2000 pixels (`7803` outside) |

# Common Attributes

| Attribute | Purpose |
|---|---|
| `criteria` | Row filter, view exports only. See [Filter criteria syntax](/foundations/filter-criteria-syntax.md). |
| `selectedColumns` | 1 to 300 column display names to include (`8547` on count, `8015` on an unknown name). Honoured for tables and tabular views; ignored for charts, pivots and summaries. |
| `applyDefaultUF` | Apply the view's default user-filter values. |
| `showPersonalCols` | Include personal-data columns (admins only; default `false`). |
| `password` | Password-protects the exported file, 6 to 256 characters (`8188`). |
| `sqlQuery`, `tableCriteriaList` | SQL export job only. |
| `callbackUrl` | Asynchronous jobs only. See [Asynchronous jobs](/foundations/asynchronous-jobs.md). |

# Email Schedule exportType

| Value | Meaning | Restrictions |
|---|---|---|
| `CSV` | Comma-separated file | Not for dashboards. |
| `XLS` | Excel workbook | Exactly one view (`8037`); not for dashboards. |
| `PDF` | PDF document | All view types including dashboards. |
| `HTML` | HTML, attached or inline (`emailAsInline`) | All view types including dashboards. |
| `IMG` | Image | Chart views only (`8036`); not for dashboards. |

A dashboard schedule may contain only that one view (`8034`) and only `PDF` or `HTML` (`8035`).

# Related

- [Synchronous Data Export](/domains/data-operations/sync-data-export/overview.md)
- [Asynchronous Data Export](/domains/data-operations/async-data-export/overview.md)
- [Email Schedules](/domains/schedules-and-alerts/email-schedules/overview.md)
