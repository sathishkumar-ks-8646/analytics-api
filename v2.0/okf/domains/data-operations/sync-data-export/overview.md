---
type: API Group
title: Synchronous Data Export
description: APIs for exporting view data directly.
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - sync-data-export
  - api-group
api:
  domain: data-operations
  group: sync-data-export
  endpoint_count: 1
  endpoints:
    - operation_id: exportDataView
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data"
      doc: "/domains/data-operations/sync-data-export/export-data-view.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-operations-grouped-api.json"
    title: OpenAPI 3 specification - data-operations-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

This document covers the **synchronous data export** REST API of Zoho Analytics — the API that reads a view and streams the exported file back in the same HTTP response.

APIs for exporting view data directly.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Export Data from a View](export-data-view.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data` | `exportDataView` | `ZohoAnalytics.data.read` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is a "Synchronous" export?

This API returns **the exported file itself** as the response body. There is no job to create, no status to poll, and no download link to follow: when the call returns, the bytes of the CSV, JSON, XML, XLS, PDF, HTML, or image file are already in your hands.

That convenience is also its constraint. Because the file must be produced inside a single request, the API is deliberately restricted to views that can be rendered quickly — see [Limitations](overview.md#limitations).

| | Synchronous export (this document) | Asynchronous export |
|---|---|---|
| **Endpoint** | `GET /workspaces/<id>/views/<id>/data` | `GET /bulk/workspaces/<id>/views/<id>/data` |
| **Response body** | The exported file | A JSON envelope containing a `jobId` |
| **Number of calls** | One | Create the job, poll it, then download |
| **Dashboards, Query Tables, live-connect views** | Not supported | Supported |
| **Tables above the row limit** | Not supported | Supported |
| **`callbackUrl`** | Not supported | Supported |

---

# How This API Relates to the Other APIs

This API is a **terminal consumer**: it produces a file and changes nothing. Everything it needs is an ID or a name produced by some other API.

```
 [Get View List]  ─────────────────►  <view-id>
        │                                  │
        │                                  ▼
 [Get Columns] ──► column display names ──►  1. Export Data from a View
        │              (selectedColumns)     (GET .../views/<view-id>/data)
        │                                  │
        │                                  ├──► CSV / JSON / XML / XLS
        │                                  ├──► PDF / HTML
        │                                  └──► PNG / JPEG (charts only)
        │
        └──► Sharing decides whether the caller has Export permission at all
```

| Relationship | Detail |
|--------------|--------|
| **`<view-id>` comes from elsewhere** | This API never returns a view ID; it consumes one. Get it from [Get View List](../../views-management/view-operations/get-views.md), or from the response of [Import Data into a New Table (Synchronous)](../sync-data-import/import-data-new-table.md), or from [Create Query Table](../../data-modeling-and-schema/query-tables/create-query-table.md). |
| **`selectedColumns` takes column *display names*, not IDs** | Fetch them with [Get Columns](../../data-modeling-and-schema/columns/overview.md). A name that does not match any column in the view fails with `8015` — the whole export fails, nothing partial is returned. |
| **Export permission is granted by the sharing APIs** | The `export` share permission set by [Share Views](../../share-and-publish/sharing/share-views.md) is exactly the permission this API checks. See [Permission Model](overview.md#permission-model). |
| **Hidden and personal-data columns are decided at design time** | Whether a column is hidden, or marked as personal data, is set through the column APIs; this export only chooses whether to *include* such columns. See [Get Columns](../../data-modeling-and-schema/columns/overview.md). |
| **`criteria` shares its grammar with the Row APIs** | The same filter-expression syntax used by [Update Row](../row-operations/update-rows.md) and [Delete Row](../row-operations/delete-rows.md) applies here — see [`criteria` Syntax](overview.md#criteria-syntax). |
| **Restricted views must go through the asynchronous export** | Dashboards, Query Tables, live-connect views, and large tables are rejected here with `8133`. They are handled by the bulk export APIs under `/restapi/v2/bulk/...`. |
| **The same export settings drive Email Schedules** | Page setup, paper size, margins, header/footer slots, and `exportLanguage` carry the same meanings and the same value sets in [Create Email Schedule](../../schedules-and-alerts/email-schedules/create-email-schedule.md). A page layout tuned here can be reused there. |
| **It has no reverse operation** | Export is read-only. Getting data *into* a table is [Synchronous Data Import](../sync-data-import/overview.md) or [Asynchronous & Batch Data Import](../async-data-import/overview.md). |

## Typical sequences

**Export one report as a filtered CSV**

```
[Get View List] → <view-id> → Export Data from a View
                              CONFIG={"responseFormat":"csv","criteria":"..."}
```

**Export a chart as a PNG for embedding in a report**

```
[Get View List] → <view-id> of a chart → Export Data from a View
                                         CONFIG={"responseFormat":"image","imageFormat":"png"}
```

**Export only three columns of a table, password protected**

```
[Get Columns] → column display names → Export Data from a View
                                       CONFIG={"selectedColumns":[...],"password":"..."}
```

---

# Limitations

These are the limits that apply to this API with **default settings**.

## Views that cannot be exported synchronously

| Restriction | Behaviour |
|-------------|-----------|
| **Tables with more than 1,000,000 rows** | Rejected with `8133`. Use the asynchronous export instead. |
| **Dashboards** (including dashboard tabs) | Rejected with `8133`. |
| **Query Tables** | Rejected with `8133`. |
| **Views belonging to a live-connect workspace** | Rejected with `8133`. |

All four are checked **before** any CONFIG validation, so a request that trips one of them fails with [`8133`](../../../foundations/error-codes.md#error-8133) even if the CONFIG is also malformed.

## Format restrictions

| Restriction | Behaviour |
|-------------|-----------|
| **`image` is only valid for chart views** | Any other view type fails with `8014`. |
| **`imageFormat` accepts only `png`, `jpg`, `jpeg`** | Anything else fails with `8017`. |
| **Image width must be 250–2000 px, height 200–2000 px** | Outside that range fails with `7803`. |
| **`selectedColumns` is honoured only for tables and tabular views** | For charts, pivots, and summary views the attribute is accepted and ignored — the view's own column layout decides what is exported. |

## Size and volume limits

| Limit | Value | Error |
|-------|-------|-------|
| Total exported payload | 100 MB | `7830` |
| PDF cells (visible columns × rows) | 1,000,000 | `7827` |
| XLS rows per sheet | 65,536 | `7806` |
| XLS columns per sheet | 256 | `7807` |
| XLS characters per cell | 32,767 | `7808` |
| `CONFIG` length | 100,000 characters | `8507` |
| `selectedColumns` entries | 1–300 | `8547` |
| `password` length | 6–256 characters | `8188` |

## Attributes that belong to other export APIs

The following are **not** applicable to this API, because the views or features they configure are not reachable here:

| Attribute | Why it does nothing here |
|-----------|--------------------------|
| `callbackUrl` | Callbacks exist only for the asynchronous export; this API has no job to notify about. |
| `generateTOC`, `dashboardLayout`, `zoomFactor` | Dashboard-only page-setup attributes. Dashboards cannot be exported synchronously. |

---

# Permission Model

| API | Who may call it |
|-----|-----------------|
| [Export Data from a View](export-data-view.md) | An Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with **Export** permission on the view. |

Two further gates apply on top of the permission check:

| Gate | Behaviour |
|------|-----------|
| **Verified email** | The calling user's primary email address must be verified, otherwise `7565`. |
| **Organization security controls** | If the organization has disabled export, every call fails with `8088`, regardless of the caller's role or permissions. |

Two attributes behave differently depending on whether the caller administers the workspace:

| Attribute | Account Admin / Organization Admin / Workspace Admin | Any other user |
|-----------|------------------------------------------------------|----------------|
| `showPersonalCols` | Honoured. Default `false`, so columns marked as personal data are **excluded** unless you ask for them. | Ignored. Personal-data columns are included, because a shared user only ever sees the columns already shared to them. |
| `criteria` | Applied as sent. | Applied, then **ANDed** with the share filter criteria configured for that user. A shared user can never widen their slice of the table with a broad `criteria`. |

---

# `criteria` Syntax

`criteria` is a SQL-like filter expression that selects which rows are exported. Column names are quoted with double quotes and string literals with single quotes:

```
"Region"='East'
"SalesTable"."Region"='East'
"Sales">1000 and "Region"='West'
"Region" in ('East','West') and "Order Date">='01-Jan-2026'
```

Notes that matter in practice:

- Omitting `criteria` exports **every row** the caller is entitled to see.
- A column named in `criteria` must exist in the view, otherwise the request fails with [`7330`](../../../foundations/error-codes.md#error-7330).
- A table name that is not part of the view fails with [`7332`](../../../foundations/error-codes.md#error-7332).
- A syntactically malformed expression fails with [`7331`](../../../foundations/error-codes.md#error-7331); an expression that parses but cannot be converted to SQL fails with [`7327`](../../../foundations/error-codes.md#error-7327).
- Aggregate functions (`sum`, `avg`, `count`, …) are not permitted in `criteria` — they fail with [`7333`](../../../foundations/error-codes.md#error-7333).
- For a **tabular view**, only columns of its own base table may be referenced; anything else fails with [`7543`](../../../foundations/error-codes.md#error-7543).
- For a **shared user**, the share filter criteria is ANDed automatically — see [Permission Model](overview.md#permission-model).
- Because `criteria` travels inside the `CONFIG` query parameter, it must be JSON-escaped and then URL-encoded. Double quotes around column names become `\"` in JSON and `%22` on the wire.
- When `responseFormat` is `json` or `xml` with `keyValueFormat` set to `false`, the criteria you sent is echoed back in the response envelope.

---

# API-Specific Notes and Behaviours

## Export Data from a View

- **This is the only API in the suite whose success response is not JSON.** Everything else in the V2 surface returns either a `status`/`summary`/`data` envelope or an empty `204`. Here the success body is the file. Write client code that checks the HTTP status first, parses JSON only on failure, and reads `Content-Type` to decide how to handle the success body.
- **No `Content-Disposition` header is returned.** There is no server-suggested filename. Derive one yourself from the view name and the format, and remember that a password-protected `csv` arrives as a ZIP.
- **The view type decides more than the format does.** `image` needs a chart; dashboards and query tables are unavailable entirely; `selectedColumns` only applies to tables and tabular views. Establish the view type once via [Get View List](../../views-management/view-operations/get-views.md) and drive the CONFIG from it, rather than probing formats until one succeeds.
- **[`8133`](../../../foundations/error-codes.md#error-8133) is a routing signal, not a bug.** It means "this view belongs to the asynchronous export". Treat it as a branch in the integration — fall back to the bulk export APIs — rather than as an error to retry.
- **`keyValueFormat` inverts between JSON and XML.** JSON defaults to key-value pairs; XML defaults to the wrapped `<column name="…">` envelope. An integration that sets neither gets two structurally unrelated documents from the same view. Set it explicitly whenever both formats are in play.
- **`keyValueFormat: true` for XML produces a fragment, not a document.** No `<?xml?>` declaration, no `<response>` root. Strict XML parsers will need the `keyValueFormat: false` shape, which is also the safer choice when column names contain spaces or punctuation.
- **`criteria` is the single most useful attribute for staying inside the limits.** The row-count ceiling, the PDF cell ceiling, and the 100 MB payload ceiling are all evaluated on what the export actually produces, so a narrowing `criteria` is what turns an unexportable view into an exportable one.
- **Password protection changes the response content type.** For `csv`, `json`, `xml`, `html`, and `image` the payload becomes a ZIP. This is the most common cause of "the exported file is corrupt" reports.
- **`showPersonalCols` is a convenience for administrators, not an access control.** For any other caller it is ignored and personal columns are included. Column-level restriction for shared users belongs in [Share Views](../../share-and-publish/sharing/share-views.md).
- **Page-setup values are shared with Email Schedules.** `paperSize`, `paperStyle`, the four margins, `showTitle`, `showDesc`, `exportLanguage`, and the six header/footer slots use the same value sets as [Create Email Schedule](../../schedules-and-alerts/email-schedules/create-email-schedule.md). A layout proven here can be transplanted there unchanged.
- **Dependency chain:** [Get View List](../../views-management/view-operations/get-views.md) + [Get Columns](../../data-modeling-and-schema/columns/overview.md) → Export Data from a View → the exported file. Nothing consumes this API's output within the V2 surface; it is the end of the line.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Success is HTTP 200 with a file body** | Not `204`, and not a JSON envelope. The body is the export itself. |
| **Failure responses share one shape** | `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name (for example `SYNC_EXPORT_NOT_ALLOWED`), not a localised sentence. |
| **`Content-Type` is the only descriptive header** | It is derived from `responseFormat`, or replaced by `application/zip` when `password` wraps the file. |
| **The body is not compressed** | No `Content-Encoding` is applied to the synchronous export; the bytes on the wire are the file's own bytes. |
| **All cell values are strings in JSON and XML** | Numeric, currency, percentage, and date columns are exported as formatted strings, following the column's display settings — not as JSON numbers. |
| **Column keys use display names** | Both JSON shapes and both XML shapes key on the column's display name as shown in the view, which is also what `selectedColumns` expects on the request side. |
| **`Row Number` is a synthetic field** | When enabled, it is a sequential counter over the exported rows. It is not the table's internal row identifier and will not match across two exports with different `criteria`. |
| **An empty export is still well-formed** | `{"data":[]}`, `<rows></rows>`, or a header-only CSV. Check for emptiness explicitly; no error is raised. |
| **`response.criteria` is conditionally present** | It appears in the `keyValueFormat: false` JSON and XML envelopes only when a `criteria` was actually sent. Test for the key. |
| **Binary formats carry no metadata in the payload** | `xls`, `pdf`, and image responses expose nothing about row counts or applied filters. If you need that, run the export in `json` first, or read the counts from the source view. |

---

# Enum Reference

Every enumerated attribute of this API in one place. An out-of-range value fails with [`8119`](../../../foundations/error-codes.md#error-8119) unless noted otherwise.

**`responseFormat`** — default `csv`; invalid values fail with [`8001`](../../../foundations/error-codes.md#error-8001)

| Value | Output |
|-------|--------|
| `csv` | Delimited text file |
| `json` | JSON document |
| `xml` | XML document |
| `xls` | Excel workbook |
| `pdf` | PDF document |
| `html` | HTML fragment |
| `image` | PNG or JPEG image — **chart views only** |

**`delimiter`** — CSV field separator, default `0`

| Value | Separator |
|-------|-----------|
| `0` | Comma |
| `1` | Tab |
| `2` | Semicolon |
| `3` | Space |
| `4` | Pipe |

**`recordDelimiter`** — CSV line ending, default `0`

| Value | Line ending |
|-------|-------------|
| `0` | DOS (`\r\n`) |
| `1` | UNIX (`\n`) |
| `2` | MAC (`\r`) |

**`quoted`** — CSV text qualifier, no default

| Value | Qualifier |
|-------|-----------|
| `0` | Single quote |
| `1` | Double quote |

**`paperSize`** — PDF page size, default `4`

| Value | Page size |
|-------|-----------|
| `0` | Letter |
| `1` | Legal |
| `2` | Tabloid |
| `3` | A3 |
| `4` | A4 |
| `5` | Auto-fit — width grows with the number of visible columns |

**`paperStyle`** — PDF orientation, default `Portrait`

| Value | Orientation |
|-------|-------------|
| `Portrait` | Upright |
| `Landscape` | Sideways |

**`showTitle`, `showDesc`** (PDF) and **`includeTitle`, `includeDesc`** (HTML) — default `0`

| Value | Placement |
|-------|-----------|
| `0` | Top |
| `1` | Bottom |
| `2` | Do not include |

**`columnWidthRatio`** — default `1` for PDF, `2` for HTML

| Value | Column sizing |
|-------|---------------|
| `0` | Proportional to the widths set in the view |
| `1` | Sized to content |
| `2` | All columns equal |

**`exportLanguage`** — PDF font set, default `0`

| Value | Font set |
|-------|----------|
| `0` | English |
| `1` | Chinese |
| `2` | Japanese |
| `3` | European |
| `4` | Korean |

**`leftHeader`, `centerHeader`, `rightHeader`, `leftFooter`, `centerFooter`, `rightFooter`** — PDF page-header and page-footer slots

| Value | Content |
|-------|---------|
| `0` | Blank |
| `1` | View title |
| `2` | Export date |
| `3` | Page number |
| `4` | Page number with total |
| `5` | Custom text from the matching `…Text` attribute |
| `6` | Logo |

Defaults: `leftHeader` `1`, `centerHeader` `0`, `rightHeader` `2`, `leftFooter` `0`, `centerFooter` `3`, `rightFooter` `0`.

**`imageFormat`** — default `png`; invalid values fail with [`8017`](../../../foundations/error-codes.md#error-8017)

| Value | Image type |
|-------|------------|
| `png` | PNG |
| `jpg` | JPEG |
| `jpeg` | JPEG |

---

# Attribute Applicability by `responseFormat`

`✓` applicable, `–` accepted but has no effect for that format.

| Attribute | csv | json | xml | xls | pdf | html | image |
|-----------|:---:|:----:|:---:|:---:|:---:|:----:|:-----:|
| `criteria` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `password` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `validateSystemTags` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `selectedColumns` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – |
| `showHiddenCols` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – |
| `showPersonalCols` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – |
| `includeHeader` | ✓ | – | – | ✓ | ✓ | ✓ | – |
| `includeRowNums` / `includeRowIds` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – |
| `applyDefaultUF` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – |
| `delimiter`, `recordDelimiter`, `quoted` | ✓ | – | – | – | – | – | – |
| `keyValueFormat` | – | ✓ | ✓ | – | – | – | – |
| `paperSize`, `paperStyle`, margins | – | – | – | – | ✓ | – | – |
| `showTitle`, `showDesc` | – | – | – | – | ✓ | – | – |
| `exportLanguage` | – | – | – | – | ✓ | – | – |
| header / footer slots and their `…Text` | – | – | – | – | ✓ | – | – |
| `includeTitle`, `includeDesc` | – | – | – | – | – | ✓ | – |
| `columnWidthRatio` | – | – | – | – | ✓ | ✓ | – |
| `imageFormat`, `width`, `height` | – | – | – | – | – | – | ✓ |
| `title`, `description`, `legend` | – | – | – | – | – | – | ✓ |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7327](../../../foundations/error-codes.md#error-7327) | 400 | criteria parsed but could not be converted into a query. |
| [7330](../../../foundations/error-codes.md#error-7330) | 400 | A column named in criteria does not exist in the view. |
| [7331](../../../foundations/error-codes.md#error-7331) | 400 | criteria is syntactically malformed. |
| [7332](../../../foundations/error-codes.md#error-7332) | 400 | A table qualifier in criteria is not part of the view. |
| [7333](../../../foundations/error-codes.md#error-7333) | 400 | An aggregate function was used in criteria. |
| [7543](../../../foundations/error-codes.md#error-7543) | 400 | criteria on a tabular view referenced a column outside its base table. |
| [7565](../../../foundations/error-codes.md#error-7565) | 400 | The calling user's primary email address is not verified. |
| [7801](../../../foundations/error-codes.md#error-7801) | 400 | A PDF margin is outside 0–1 inches. |
| [7803](../../../foundations/error-codes.md#error-7803) | 400 | width or height is outside the permitted image range. |
| [7806](../../../foundations/error-codes.md#error-7806) | 400 | The XLS export exceeds the per-sheet cell limit. |
| [7807](../../../foundations/error-codes.md#error-7807) | 400 | More than 256 columns were requested for an XLS export. |
| [7808](../../../foundations/error-codes.md#error-7808) | 400 | A single cell exceeds 32,767 characters. |
| [7809](../../../foundations/error-codes.md#error-7809) | 400 | The XLS export produced no data. |
| [7824](../../../foundations/error-codes.md#error-7824) | 400 | Export has been blocked for this workspace. |
| [7827](../../../foundations/error-codes.md#error-7827) | 400 | The PDF exceeds 1,000,000 cells. |
| [7830](../../../foundations/error-codes.md#error-7830) | 400 | The exported payload exceeds 100 MB. |
| [8001](../../../foundations/error-codes.md#error-8001) | 400 | responseFormat is not a supported value. |
| [8014](../../../foundations/error-codes.md#error-8014) | 400 | image was requested for a view that is not a chart. |
| [8015](../../../foundations/error-codes.md#error-8015) | 400 | A name in selectedColumns does not match any column in the view. |
| [8017](../../../foundations/error-codes.md#error-8017) | 400 | imageFormat is not png, jpg, or jpeg. |
| [8088](../../../foundations/error-codes.md#error-8088) | 400 | Export is disabled for the organization. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | Invalid value for attribute. |
| [8133](../../../foundations/error-codes.md#error-8133) | 400 | The view is a dashboard, a query table, a live-connect view, or a table above the row limit. |
| [8188](../../../foundations/error-codes.md#error-8188) | 400 | password is blank or shorter than 6 characters. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | The view carries a restricted DATAWARNING system tag. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | roleName exceeds 30 characters, or the serialized permissions object exceeds its size limit. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |
| [8547](../../../foundations/error-codes.md#error-8547) | 400 | viewIds is empty or has more than 1000 entries. |

# Related

- [Data Operations](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
