---
type: API Group
title: Asynchronous Data Export
description: APIs for creating export jobs and downloading generated exports.
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - async-data-export
  - api-group
api:
  domain: data-operations
  group: async-data-export
  endpoint_count: 4
  endpoints:
    - operation_id: createExportJobSQLQuery
      method: GET
      path: "/restapi/v2/bulk/workspaces/{workspace-id}/data"
      doc: "/domains/data-operations/async-data-export/create-export-job-sql-query.md"
    - operation_id: createExportJobViewId
      method: GET
      path: "/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data"
      doc: "/domains/data-operations/async-data-export/create-export-job-view-id.md"
    - operation_id: getExportJobDetails
      method: GET
      path: "/restapi/v2/bulk/workspaces/{workspace-id}/exportjobs/{job-id}"
      doc: "/domains/data-operations/async-data-export/get-export-job-details.md"
    - operation_id: downloadExportedData
      method: GET
      path: "/restapi/v2/bulk/workspaces/{workspace-id}/exportjobs/{job-id}/data"
      doc: "/domains/data-operations/async-data-export/download-exported-data.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-operations-grouped-api.json"
    title: OpenAPI 3 specification - data-operations-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

This document covers the four **asynchronous data export** REST APIs of Zoho Analytics — the APIs that hand the export off to a background job, hand you back a job ID, and let you collect the finished file later.

APIs for creating export jobs and downloading generated exports.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Create Export Job using SQL Query (Asynchronous)](create-export-job-sql-query.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/data` | `createExportJobSQLQuery` | `ZohoAnalytics.data.read` | 200 |
| [Create Export Job using View ID (Asynchronous)](create-export-job-view-id.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data` | `createExportJobViewId` | `ZohoAnalytics.data.read` | 200 |
| [Get Export Job Details](get-export-job-details.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/exportjobs/{job-id}` | `getExportJobDetails` | `ZohoAnalytics.data.read` | 200 |
| [Download Exported Data](download-exported-data.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/exportjobs/{job-id}/data` | `downloadExportedData` | `ZohoAnalytics.data.read` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is an "Asynchronous" export?

An asynchronous export is a three-step conversation. You create a job, you find out when it has finished, and then you download the file. Nothing is produced inside the first request.

```
 1/2. Create Export Job  ──►  jobId
                                │
                                ▼
      3. Get Export Job Details ──► jobCode 1001/1002 → keep polling
                                │
                                ├─► jobCode 1003 → the job failed, stop
                                │
                                └─► jobCode 1004 → downloadUrl + expiryTime
                                                        │
                                                        ▼
                                          4. Download Exported Data
```

The trade for that extra round trip is that the restrictions of the synchronous export disappear.

| | Asynchronous export (this document) | [Synchronous export](../sync-data-export/overview.md) |
|---|---|---|
| **Endpoint prefix** | `/restapi/v2/bulk/workspaces/...` | `/restapi/v2/workspaces/...` |
| **First response** | A JSON envelope containing `jobId` | The exported file itself |
| **Number of calls** | Three (create, poll, download) | One |
| **Dashboards, Query Tables, live-connect views** | **Supported** | Rejected with `8133` |
| **Tables above one million rows** | **Supported** | Rejected with `8133` |
| **Ad-hoc SQL query as the source** | **Supported** | Not available on the view endpoint |
| **`callbackUrl`** | **Supported** | Not supported |
| **Payload ceiling** | None imposed on the job | 100 MB |

---

# How the Four APIs Relate

These four are not four independent APIs. They are one pipeline, and the `jobId` produced by either creation API is the only thing that connects them.

```
 [Get View List] ─────► <view-id> ──┐
                                    │
 [Get Columns] ──► column names ────┤
   (selectedColumns)                │
                                    ▼
                    2. Create Export Job using View ID  ──┐
                                                          │
 [Create Query Table] / any SQL SELECT ──► sqlQuery       ├──► data.jobId
                                    │                     │
                                    ▼                     │
                    1. Create Export Job using SQL Query ─┘
                                                          │
                        ┌─────────────────────────────────┘
                        ▼
              3. Get Export Job Details  ◄──── poll until jobCode = 1004
                        │                      (or let callbackUrl tell you)
                        │
                        ├──► data.downloadUrl  ──┐
                        └──► data.expiryTime     │
                                                 ▼
                                    4. Download Exported Data
                                       (returns the file)
```

| Relationship | Detail |
|--------------|--------|
| **`jobId` is produced once and consumed twice** | Both creation APIs return it in `data.jobId`. It is the `<job-id>` path segment for [Get Export Job Details](get-export-job-details.md) and for [Download Exported Data](download-exported-data.md). It appears in no other API's response — capture it from the create call. |
| **`downloadUrl` is exactly the Download Exported Data endpoint** | [Get Export Job Details](get-export-job-details.md) returns a fully-qualified URL that resolves to [Download Exported Data](download-exported-data.md) for the same workspace and job. Following `downloadUrl` and calling the endpoint yourself are the same operation. |
| **Downloading before the job finishes is an error, not a wait** | [Download Exported Data](download-exported-data.md) does not block. It fails with `8121` while the job is queued and `8122` while it is running. The poll in [Get Export Job Details](get-export-job-details.md) is mandatory, not advisory. |
| **The two creation APIs differ only in their source** | One takes a saved view via `<view-id>`, the other an ad-hoc `sqlQuery`. Both feed the identical job pipeline, and steps 3 and 4 cannot tell them apart. |
| **Their CONFIG sets are close but not identical** | `criteria` and `applyDefaultUF` exist only for the view export; `sqlQuery` and `tableCriteriaList` only for the SQL query export. See [Filtering: `criteria` and `tableCriteriaList`](overview.md#filtering-criteria-and-tablecriterialist). |
| **`<view-id>` comes from elsewhere** | Get it from [Get View List](../../views-management/view-operations/get-views.md), from [Import Data into a New Table (Synchronous)](../sync-data-import/import-data-new-table.md), or from [Create Query Table](../../data-modeling-and-schema/query-tables/create-query-table.md). |
| **`selectedColumns` takes column display names** | Fetch them with [Get Columns](../../data-modeling-and-schema/columns/overview.md). An unmatched name fails the create call with `8015`; the job is never created. |
| **Export permission is granted by the sharing APIs** | The `export` share permission set by [Share Views](../../share-and-publish/sharing/share-views.md) is what both creation APIs check. For a SQL query export it is checked on **every table the query touches**. See [Permission Model](overview.md#permission-model). |
| **`callbackUrl` replaces the poll, it does not replace step 4** | The callback fires when the job reaches a terminal state and carries the same fields as [Get Export Job Details](get-export-job-details.md), but you still have to call [Download Exported Data](download-exported-data.md) to get the bytes. |
| **The job is owned by its creator** | Only the user who created the job can poll or download it. See [Permission Model](overview.md#permission-model). |
| **The same CONFIG vocabulary as the synchronous export** | Formats, delimiters, page setup, and image options carry identical meanings and value sets to [Export Data from a View](../sync-data-export/export-data-view.md). A CONFIG proven there works here. |
| **Nothing consumes the exported file** | Export is read-only and terminal. Getting data back *into* a table is [Synchronous Data Import](../sync-data-import/overview.md) or [Asynchronous & Batch Data Import](../async-data-import/overview.md). |

## Typical sequences

**Export a dashboard as a PDF — impossible synchronously, routine here**

```
[Get View List] → <view-id> of a dashboard
   → Create Export Job using View ID   {"responseFormat":"pdf","dashboardLayout":1}
   → Get Export Job Details (poll)     jobCode 1004
   → Download Exported Data
```

**Export a joined result set that no saved view represents**

```
Create Export Job using SQL Query   {"sqlQuery":"SELECT ...","responseFormat":"csv"}
   → Get Export Job Details (poll)  jobCode 1004
   → Download Exported Data
```

**Fire and forget, with a callback instead of a poll**

```
Create Export Job using View ID   {"responseFormat":"csv","callbackUrl":"https://..."}
   → (your endpoint receives an HTTP POST carrying jobCode and downloadUrl)
   → Download Exported Data
```

---

# Limitations

These are the limits that apply with **default settings**. A request that exceeds one is rejected, not queued.

| Limitation | Value | Enforced by |
|------------|-------|-------------|
| **Simultaneous export jobs** | **5** per organization. A job counts against the limit while it is queued or running. | `8132` |
| **Export job retention** | **72 hours** from the moment the job is **created** — not from when it completes. After that the job record and the exported file are removed, and both [Get Export Job Details](get-export-job-details.md) and [Download Exported Data](download-exported-data.md) behave as though the job never existed. | `expiryTime` in the response, then `8120` / `jobCode` `1005` |
| **Job visibility** | An export job can be polled and downloaded **only by the user who created it**. An Account Admin cannot collect another user's job. | `8124` |
| **SQL query length** | **100,000** characters for `sqlQuery`. | `8507` |
| **SQL query result rows** | **800,000** rows. A row limit is appended to the query automatically. | Truncated silently |
| **`tableCriteriaList` entries** | **0–25** objects. | `8547` |
| **`selectedColumns` entries** | **1–300** column names. | `8547` |
| **`CONFIG` length** | **200,000** characters for the SQL query export, **100,000** for the view export. | `8507` |
| **`password` length** | **6–256** characters. | `8188` |
| **`callbackUrl` length** | **10,000** characters, and the host must be publicly reachable. | `8125`, `8126`, `8127` |
| **Image dimensions** | Width **250–2000** px, height **200–2000** px. | `7803` |
| **PDF cells** | **1,000,000** (visible columns × rows). | `7827` |
| **XLS rows per sheet** | **65,536** | `7806` |
| **XLS columns per sheet** | **256** | `7807` |
| **XLS characters per cell** | **32,767** | `7808` |

## Format restrictions

| Restriction | Behaviour |
|-------------|-----------|
| **A dashboard can only be exported as `pdf` or `html`** | Any other `responseFormat` fails with `8119`. |
| **`image` is only valid for chart views** | Any other view type fails with `8014`, and a SQL query export can never produce an image. |
| **A SQL query export is always a flat sheet** | `image` is unavailable, and the dashboard-only page-setup attributes have nothing to act on. |

> **Poll and download promptly, then persist.** Because the whole job — record and file — lives for 72 hours from creation, an integration that needs a durable copy must download inside that window and store the file itself. Nothing is recoverable afterwards.

---

# Job Codes and Polling

[Get Export Job Details](get-export-job-details.md) reports progress through `jobCode`, with `jobStatus` carrying the matching human-readable text.

| `jobCode` | `jobStatus` | Meaning | What to do |
|-----------|-------------|---------|------------|
| `1001` | `JOB NOT INITIATED` | The job has been accepted and queued but has not started. | Wait a few seconds and poll again. |
| `1002` | `JOB IN PROGRESS` | The job is being processed. | Wait a few seconds and poll again. |
| `1003` | `ERROR OCCURRED` | The job stopped because of an error. | Stop polling. The job will never complete; create a new one. |
| `1004` | `JOB COMPLETED` | The file is ready. | Read `downloadUrl` and `expiryTime`, then call [Download Exported Data](download-exported-data.md). |
| `1005` | `JOB NOT FOUND` | No job exists for this ID — it was never created, or it has passed its 72-hour retention. | Stop polling. Verify the job ID. |

`1003` and `1005` are terminal, exactly like `1004`. Only `1001` and `1002` justify another poll.

> `downloadUrl` and `expiryTime` are present **only** when `jobCode` is `1004`. Test for the keys rather than assuming them.

---

# The `callbackUrl` Attribute

`callbackUrl` is an optional attribute of both creation APIs. It saves you the poll.

| Effect | Detail |
|--------|--------|
| **You get notified instead of polling** | When the job reaches a terminal state, Zoho Analytics sends an **HTTP POST** to your URL with `Content-Type: application/json`. |
| **The body is the job details, unwrapped** | The payload is the same object that [Get Export Job Details](get-export-job-details.md) returns as its `data` — `jobId`, `jobCode`, `jobStatus`, and, on success, `downloadUrl` and `expiryTime`. It is **not** wrapped in the `status` / `summary` / `data` envelope. |
| **It fires on failure too** | The callback is sent whether the job completed or errored. Read `jobCode` to tell which: `1004` means the file is ready, `1003` means it is not. |

Rules and constraints:

- The URL must be a well-formed, publicly reachable `http`/`https` address, at most 10,000 characters. A malformed URL is rejected with [`8125`](../../../foundations/error-codes.md#error-8125).
- URLs resolving to a **private or internal IP address** are rejected with [`8127`](../../../foundations/error-codes.md#error-8127) — the callback cannot be pointed at a LAN host.
- If the endpoint cannot be reached while the request is being validated, the create call fails with [`8126`](../../../foundations/error-codes.md#error-8126) and no job is created.
- Your endpoint should answer with a 2xx status. A non-2xx response is recorded as a delivery failure.
- **Delivery is attempted once.** There is no retry, and a failed callback does not affect the job — the file is still there to download.
- The callback is a **notification, not a guarantee**. Keep [Get Export Job Details](get-export-job-details.md) as the fallback, and remember the 72-hour window.

---

# Permission Model

| API | Who may call it |
|-----|-----------------|
| [Create Export Job using SQL Query (Asynchronous)](create-export-job-sql-query.md) | An Account Admin or Organization Admin, or a Workspace Admin, or any user with **Export** permission on **every table the query references**. |
| [Create Export Job using View ID (Asynchronous)](create-export-job-view-id.md) | An Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with **Export** permission on the view. |
| [Get Export Job Details](get-export-job-details.md) | **Only the user who created the job.** Any other user, including an Account Admin, receives `8124`. |
| [Download Exported Data](download-exported-data.md) | **Only the user who created the job.** Any other user, including an Account Admin, receives `8124`. |

Further gates on the two creation APIs:

| Gate | Behaviour |
|------|-----------|
| **Verified email** | The calling user's primary email address must be verified, otherwise `7565`. This applies to the two creation APIs only; polling and downloading do not require it. |
| **Organization security controls** | If the organization has disabled export, every create call fails with `8088` regardless of role or permissions. |

Two attributes behave differently for a caller who does not administer the workspace:

| Attribute | Account Admin / Organization Admin / Workspace Admin | Any other user |
|-----------|------------------------------------------------------|----------------|
| `showPersonalCols` | Honoured. Default `false`, so columns marked as personal data are **excluded** unless you ask for them. | Ignored. Personal-data columns are included, because a shared user only ever sees the columns already shared to them. |
| `criteria` (view export) | Applied as sent. | Applied, then **ANDed** with the share filter criteria configured for that user. A shared user can never widen their slice with a broad `criteria`. |

---

# Filtering: `criteria` and `tableCriteriaList`

The two creation APIs filter rows in different ways, and neither accepts the other's attribute.

| API | Filtering attribute |
|-----|---------------------|
| [Create Export Job using View ID (Asynchronous)](create-export-job-view-id.md) | `criteria` — one filter expression, evaluated against the view. |
| [Create Export Job using SQL Query (Asynchronous)](create-export-job-sql-query.md) | `tableCriteriaList` — a per-table filter list. Row selection otherwise belongs in the `WHERE` clause of `sqlQuery` itself. |

## `criteria` syntax

`criteria` is a SQL-like filter expression that selects which rows are exported. Column names are quoted with double quotes and string literals with single quotes:

```
"Region"='East'
"SalesTable"."Region"='East'
"Sales">1000 and "Region"='West'
"Region" in ('East','West') and "Order Date">='01-Jan-2026'
```

Notes that matter in practice:

- Omitting `criteria` exports **every row** the caller is entitled to see.
- A column named in `criteria` must exist in the view, otherwise the create call fails with [`7330`](../../../foundations/error-codes.md#error-7330).
- A table name that is not part of the view fails with [`7332`](../../../foundations/error-codes.md#error-7332).
- A malformed expression fails with [`7331`](../../../foundations/error-codes.md#error-7331); one that parses but cannot be converted to SQL fails with [`7327`](../../../foundations/error-codes.md#error-7327).
- Aggregate functions (`sum`, `avg`, `count`, …) are not permitted — they fail with [`7333`](../../../foundations/error-codes.md#error-7333).
- For a **tabular view**, only columns of its own base table may be referenced; anything else fails with [`7543`](../../../foundations/error-codes.md#error-7543).
- For a **shared user**, the share filter criteria is ANDed automatically — see [Permission Model](overview.md#permission-model).
- The expression is validated **before** the job is created, so a bad `criteria` produces an error response and no `jobId`.
- Because `criteria` travels inside the `CONFIG` query parameter, it must be JSON-escaped and then URL-encoded. Double quotes around column names become `\"` in JSON and `%22` on the wire.
- The same grammar is used by [Update Row](../row-operations/update-rows.md), [Delete Row](../row-operations/delete-rows.md), and [Export Data from a View](../sync-data-export/export-data-view.md).

## `tableCriteriaList` structure

`tableCriteriaList` applies one filter expression per participating table, and the filters are pushed into the generated query.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tableCriteriaList[].viewId` | Long | **Yes** | ID of a table that the query references. Must belong to `<workspace-id>`, otherwise `7571`. |
| `tableCriteriaList[].criteria` | String | **Yes** | Filter expression for that table, using the same grammar as `criteria` above. |

- 0 to 25 entries. More fails with [`8547`](../../../foundations/error-codes.md#error-8547).
- Every `viewId` listed must actually be involved in `sqlQuery`, otherwise [`7836`](../../../foundations/error-codes.md#error-7836).
- Both fields are mandatory inside each object; omitting either fails the create call with [`8079`](../../../foundations/error-codes.md#error-8079).

---

# Shared CONFIG Attributes

Everything in this section applies to **both** creation APIs. The attributes unique to each are listed in that API's own section.

## Common to every format

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `responseFormat` | String | No | `"csv"` | Output format. One of `csv`, `json`, `xml`, `xls`, `pdf`, `html`, `image` (case-insensitive). Any other value fails with `8001`. |
| `password` | String | No | — | Protects the exported file with a password. 6 to 256 characters; shorter fails with `8188`. Changes the delivery format — see [Password Protection](overview.md#password-protection). |
| `selectedColumns` | JSONArray of String | No | — | Column **display names** to export, in the order given, 1–300 entries. An unmatched name fails with `8015`. Omit to export all eligible columns. |
| `showHiddenCols` | Boolean | No | `true` (`false` for `html`) | Whether columns hidden in the view are included. A column named explicitly in `selectedColumns` is always included, hidden or not. |
| `showPersonalCols` | Boolean | No | `false` | Whether columns marked as personal data are included. Honoured only for administering users — see [Permission Model](overview.md#permission-model). |
| `includeHeader` | Boolean | No | `true` | Whether a header row of column names is written. Applies to `csv`, `xls`, `pdf`, and `html`. |
| `includeRowNums` | Boolean | No | `false` | Prefixes each record with a sequential `Row Number` value. |
| `includeRowIds` | Boolean | No | `false` | Equivalent to `includeRowNums` — both feed the same switch, so sending either one enables the row-number column. |
| `callbackUrl` | String | No | — | URL notified when the job reaches a terminal state. Maximum 10,000 characters. See [The `callbackUrl` Attribute](overview.md#the-callbackurl-attribute). |
| `validateSystemTags` | Boolean | No | `true` | When `true`, the request is rejected with `8241` if the source carries a restricted **DATA_WARNING** system tag — applied directly, or inherited through lineage from a parent data source or table. Send `false` to acknowledge and proceed. Only relevant when System Tags are enabled for the organization. |

## CSV specific

Applicable when `responseFormat` is `csv`.

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `delimiter` | Integer | No | `0` (comma) | Field separator. `0` Comma, `1` Tab, `2` Semicolon, `3` Space, `4` Pipe. Any other value fails with `8119`. |
| `recordDelimiter` | Integer | No | `0` (DOS) | Line ending. `0` DOS (`\r\n`), `1` UNIX (`\n`), `2` MAC (`\r`). Any other value fails with `8119`. |
| `quoted` | Integer | No | — | Text qualifier wrapped around values. `0` single quote, `1` double quote. Omit for no qualifier. |

## JSON and XML specific

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `keyValueFormat` | Boolean | No | `true` for `json`, `false` for `xml` | Chooses the record shape. `true` emits each row as column-name/value pairs; `false` emits a wrapped envelope with a separate column list and rows as positional arrays. See [Exported File Structure by Format](download-exported-data.md#exported-file-structure-by-format). |

## PDF specific

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `paperSize` | Integer | No | `4` (A4) | `0` Letter, `1` Legal, `2` Tabloid, `3` A3, `4` A4, `5` Auto-fit width. For a **dashboard** the range is `0`–`4` and the default is `2` (Tabloid). Outside the range fails with `8119`. |
| `paperStyle` | String | No | `"Portrait"` | `"Portrait"` or `"Landscape"` (case-insensitive). |
| `topMargin` | Float | No | `0.25` | Top margin in inches, `0`–`1` inclusive. Outside fails with `7801`. |
| `bottomMargin` | Float | No | `0.25` | Bottom margin in inches, `0`–`1`. |
| `leftMargin` | Float | No | `0.25` | Left margin in inches, `0`–`1`. |
| `rightMargin` | Float | No | `0.25` | Right margin in inches, `0`–`1`. |
| `showTitle` | Integer | No | `0` (top) | Where the title is placed. `0` Top, `1` Bottom, `2` Do not include. |
| `showDesc` | Integer | No | `0` (top) | Where the description is placed. `0` Top, `1` Bottom, `2` Do not include. |
| `columnWidthRatio` | Integer | No | `1` | Column sizing. `0` proportional to the widths set in the view, `1` sized to content, `2` all columns equal. |
| `exportLanguage` | Integer | No | `0` (English) | Font set used for rendering text. `0` English, `1` Chinese, `2` Japanese, `3` European, `4` Korean. Pick the one matching your data, otherwise non-Latin characters may not render. |
| `leftHeader` | Integer | No | `1` (Title) | Content of the top-left page-header slot. See [Header and Footer Slot Values](overview.md#header-and-footer-slot-values). |
| `centerHeader` | Integer | No | `0` (Blank) | Content of the top-centre page-header slot. |
| `rightHeader` | Integer | No | `2` (Date) | Content of the top-right page-header slot. |
| `leftFooter` | Integer | No | `0` (Blank) | Content of the bottom-left page-footer slot. |
| `centerFooter` | Integer | No | `3` (Page number) | Content of the bottom-centre page-footer slot. |
| `rightFooter` | Integer | No | `0` (Blank) | Content of the bottom-right page-footer slot. |
| `leftHeaderText` | String | No | — | Custom text for the top-left slot. Read only when `leftHeader` is `5`. |
| `centerHeaderText` | String | No | — | Custom text for the top-centre slot. Read only when `centerHeader` is `5`. |
| `rightHeaderText` | String | No | — | Custom text for the top-right slot. Read only when `rightHeader` is `5`. |
| `leftFooterText` | String | No | — | Custom text for the bottom-left slot. Read only when `leftFooter` is `5`. |
| `centerFooterText` | String | No | — | Custom text for the bottom-centre slot. Read only when `centerFooter` is `5`. |
| `rightFooterText` | String | No | — | Custom text for the bottom-right slot. Read only when `rightFooter` is `5`. |

### Header and Footer Slot Values

The same seven values apply to every one of the six slots.

| Value | Content placed in the slot |
|-------|----------------------------|
| `0` | Blank |
| `1` | View title |
| `2` | Export date |
| `3` | Page number |
| `4` | Page number with total (`3 of 12`) |
| `5` | The custom text from the matching `…Text` attribute |
| `6` | Logo |

Any other value fails with [`8119`](../../../foundations/error-codes.md#error-8119). When a slot is set to `1`, the source's own title is substituted and the matching `…Text` attribute is ignored.

## HTML specific

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `includeTitle` | Integer | No | `0` (top) | Where the title is placed. `0` Top, `1` Bottom, `2` Do not include. |
| `includeDesc` | Integer | No | `0` (top) | Where the description is placed. `0` Top, `1` Bottom, `2` Do not include. |
| `columnWidthRatio` | Integer | No | `2` | Column sizing. `0` proportional to the widths set in the view, `1` sized to content, `2` all columns equal. Note the default differs from PDF. |

## XLS specific

`xls` adds no attributes of its own beyond `includeHeader`. It uses `selectedColumns`, `showHiddenCols`, `showPersonalCols`, `includeRowNums`, `password`, and the relevant filter attribute.

## Password Protection

Sending `password` changes **how** the file is delivered, not only whether it is locked. The `Content-Type` of [Download Exported Data](download-exported-data.md) reflects this:

| `responseFormat` | Result when `password` is sent |
|------------------|--------------------------------|
| `csv`, `json`, `xml`, `html`, `image` | The file is placed inside a **password-protected ZIP archive**; the download returns `application/zip`. |
| `xls` | The workbook itself is encrypted. `Content-Type` stays `application/vnd.ms-excel`. |
| `pdf` | The PDF itself is encrypted, with printing and copying permitted. `Content-Type` stays `application/pdf`. |

---

# API-Specific Notes and Behaviours

## Create Export Job using SQL Query (Asynchronous)

- **It is the only way to export a result set that no saved view represents.** Joins, unions, and aggregations can be expressed inline instead of being materialised as a query table first.
- **Permission is evaluated per participating table.** A [`7301`](../../../foundations/error-codes.md#error-7301) here is about one table inside the statement, so the diagnosis is "which table" rather than "which user". Resolve the tables the query touches before blaming the token.
- **The 800,000-row cap is silent.** A statement that would return more is truncated and the job still reports `1004`. If completeness matters, constrain the statement so the result is provably under the cap, or count first.
- **`tableCriteriaList` is not a substitute for `WHERE`.** It exists to apply per-table restrictions on top of the statement. For ordinary row selection the `WHERE` clause is simpler and has no 25-entry ceiling.
- **`CONFIG` is mandatory, unlike its sibling.** There is no default source to fall back on.
- **`image` is structurally impossible.** A query result is a sheet, so [`8014`](../../../foundations/error-codes.md#error-8014) is not a bug.
- **Dependency chain:** any SQL `SELECT` over the workspace's tables → Create Export Job using SQL Query (Asynchronous) → `data.jobId` → [Get Export Job Details](get-export-job-details.md) → [Download Exported Data](download-exported-data.md).

## Create Export Job using View ID (Asynchronous)

- **This is the answer to every [`8133`](../../../foundations/error-codes.md#error-8133) from the synchronous export.** Dashboards, query tables, live-connect views, and large tables are all exportable here. When the synchronous call refuses, switch endpoints rather than trying different formats.
- **Dashboards behave differently from every other view type.** The format is restricted to `pdf` and `html`, the paper defaults change, and three extra attributes (`generateTOC`, `dashboardLayout`, `zoomFactor`) become meaningful. They do nothing for any other view type.
- **A dashboard export may not be a single file.** HTML dashboards and multi-tab dashboard PDFs come back as ZIP archives. Code that assumes one file per job will break on exactly the view type this API exists to serve.
- **`CONFIG` is optional.** A bare call queues a full CSV export, which makes this the shortest possible way to schedule a whole-view dump.
- **`selectedColumns` silently does nothing for charts, pivots, summary views, and dashboards.** Only tables and tabular views honour it.
- **`criteria` is validated up front.** A bad expression costs you an error response, not a wasted job.
- **Page setup is shared with Email Schedules.** `paperSize`, `paperStyle`, the four margins, `showTitle`, `showDesc`, `exportLanguage`, and the six header/footer slots use the same value sets as [Create Email Schedule](../../schedules-and-alerts/email-schedules/create-email-schedule.md).
- **Dependency chain:** [Get View List](../../views-management/view-operations/get-views.md) + [Get Columns](../../data-modeling-and-schema/columns/overview.md) → Create Export Job using View ID (Asynchronous) → `data.jobId` → [Get Export Job Details](get-export-job-details.md) → [Download Exported Data](download-exported-data.md).

## Get Export Job Details

- **HTTP status and job status are independent.** A failed job is reported as `200` / `success` / `jobCode` `1003`. An integration that only inspects HTTP codes will treat a failed export as a success and then get [`8123`](../../../foundations/error-codes.md#error-8123) from the download.
- **Two terminal codes look like progress and are not.** `1003` and `1005` never change. Polling either forever is the most common mistake with this pipeline.
- **`expiryTime` counts from creation.** The window shrinks while the job runs, so a slow job leaves less time to collect. Read `expiryTime` rather than adding 72 hours to the moment you saw `1004`.
- **`expiryTime` is epoch milliseconds in a **string**.** So is `jobId`, and so is `jobCode`. Nothing in `data` is a JSON number.
- **The response says nothing about the export itself.** No format, no row count, no size. Keep your own record of what the job was for.
- **Prefer `callbackUrl` when you can host an endpoint.** It carries the same fields, removes the poll entirely, and fires on failure too.
- **Dependency chain:** either creation API → `data.jobId` → Get Export Job Details → `data.downloadUrl` → [Download Exported Data](download-exported-data.md).

## Download Exported Data

- **It is the second API in this suite whose success response is not JSON.** The other is [Export Data from a View](../sync-data-export/export-data-view.md). Check the HTTP status first, parse JSON only on failure, and read `Content-Type` to handle the success body.
- **Its error codes are a state machine, not noise.** [`8121`](../../../foundations/error-codes.md#error-8121), [`8122`](../../../foundations/error-codes.md#error-8122), [`8123`](../../../foundations/error-codes.md#error-8123), [`8120`](../../../foundations/error-codes.md#error-8120), and [`8124`](../../../foundations/error-codes.md#error-8124) each identify one job state precisely, which means a client can drive the whole pipeline from download errors alone if it prefers that to polling.
- **No `Content-Disposition` header.** There is no server-suggested filename, and the extension is not derivable from the URL. Record the `responseFormat` you requested.
- **`application/zip` has three separate causes** — a password, an HTML dashboard, or a multi-tab dashboard PDF. Do not treat ZIP as evidence that a password was set.
- **Downloads are idempotent within the window.** Re-downloading is safe and does not consume the job.
- **Dependency chain:** [Get Export Job Details](get-export-job-details.md) → `jobCode` `1004` → Download Exported Data → the file.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Three APIs return JSON, one returns a file** | The two creation APIs and [Get Export Job Details](get-export-job-details.md) return the standard envelope. [Download Exported Data](download-exported-data.md) returns the exported file itself. |
| **No API in this document returns 204** | All four answer `200` on success. |
| **Failure responses share one shape** | `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name (for example `EXPORT_JOB_NOT_COMPLETED`), not a localised sentence. |
| **Both creation APIs share one success `summary`** | `"Create bulk export job"`. It does not distinguish the view export from the SQL query export. |
| **`Get Export Job Details` always has `summary` `"Fetch export job info"`** | Including when the job it reports on has failed. |
| **Every value inside `data` is a string** | `jobId`, `jobCode`, `jobStatus`, `downloadUrl`, and `expiryTime` are all JSON strings, never numbers. |
| **`downloadUrl` and `expiryTime` are conditional** | Present only when `jobCode` is `"1004"`. Test for the keys. |
| **`downloadUrl` is absolute and region-aware** | It is built from the server URL serving the request, so it already points at the correct data centre. Prefer it over hand-assembling the path. |
| **A `200` from a creation API does not mean the export worked** | It means the job was accepted. The outcome is only visible through `jobCode`. |
| **All exported cell values are strings** | In the JSON and XML formats, numeric, currency, percentage, and date columns are exported as formatted strings following the column's display settings. |
| **The downloaded body is not compressed in transit** | No `Content-Encoding` is applied. A `application/zip` body is an archive by design, not a transport encoding. |
| **An empty export is still a completed job** | A `criteria` matching nothing yields `jobCode` `1004` and a header-only CSV, `{"data":[]}`, or an empty `<rows/>`. It is not an error. |

---

# Enum Reference

Every enumerated attribute of the two creation APIs in one place. An out-of-range value fails with [`8119`](../../../foundations/error-codes.md#error-8119) unless noted otherwise.

**`responseFormat`** — default `csv`; invalid values fail with [`8001`](../../../foundations/error-codes.md#error-8001)

| Value | Output | Available on |
|-------|--------|--------------|
| `csv` | Delimited text file | Both creation APIs |
| `json` | JSON document | Both |
| `xml` | XML document | Both |
| `xls` | Excel workbook | Both |
| `pdf` | PDF document | Both |
| `html` | HTML fragment | Both |
| `image` | PNG or JPEG image | View export only, **chart views only** |

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

**`paperSize`** — PDF page size, default `4` (default `2` for a dashboard)

| Value | Page size |
|-------|-----------|
| `0` | Letter |
| `1` | Legal |
| `2` | Tabloid |
| `3` | A3 |
| `4` | A4 |
| `5` | Auto-fit — width grows with the number of visible columns. **Not available for a dashboard.** |

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

**`dashboardLayout`** — dashboard PDF layout, default `1`

| Value | Layout |
|-------|--------|
| `0` | Each report on its own page |
| `1` | The layout as it appears in the dashboard |

**`imageFormat`** — default `png`; invalid values fail with [`8017`](../../../foundations/error-codes.md#error-8017)

| Value | Image type |
|-------|------------|
| `png` | PNG |
| `jpg` | JPEG |
| `jpeg` | JPEG |

**`jobCode`** — response value of [Get Export Job Details](get-export-job-details.md)

| Value | `jobStatus` | Terminal |
|-------|-------------|----------|
| `1001` | `JOB NOT INITIATED` | No |
| `1002` | `JOB IN PROGRESS` | No |
| `1003` | `ERROR OCCURRED` | Yes |
| `1004` | `JOB COMPLETED` | Yes |
| `1005` | `JOB NOT FOUND` | Yes |

---

# CONFIG Attribute Availability by API

`✓` accepted, `–` not accepted by that API.

| Attribute | Create Export Job using SQL Query | Create Export Job using View ID |
|-----------|:---------------------------------:|:-------------------------------:|
| `sqlQuery` | ✓ **mandatory** | – |
| `tableCriteriaList` | ✓ | – |
| `criteria` | – | ✓ |
| `applyDefaultUF` | – | ✓ |
| `generateTOC`, `dashboardLayout`, `zoomFactor` | – | ✓ (dashboards only) |
| `imageFormat`, `width`, `height`, `title`, `description`, `legend` | – | ✓ (chart views only) |
| `responseFormat` | ✓ | ✓ |
| `password` | ✓ | ✓ |
| `selectedColumns` | ✓ | ✓ |
| `showHiddenCols` | ✓ | ✓ |
| `showPersonalCols` | ✓ | ✓ |
| `includeHeader` | ✓ | ✓ |
| `includeRowNums` / `includeRowIds` | ✓ | ✓ |
| `callbackUrl` | ✓ | ✓ |
| `validateSystemTags` | ✓ | ✓ |
| `delimiter`, `recordDelimiter`, `quoted` | ✓ | ✓ |
| `keyValueFormat` | ✓ | ✓ |
| `paperSize`, `paperStyle`, margins, `showTitle`, `showDesc` | ✓ | ✓ |
| `columnWidthRatio`, `exportLanguage` | ✓ | ✓ |
| header / footer slots and their `…Text` | ✓ | ✓ |
| `includeTitle`, `includeDesc` | ✓ | ✓ |

[Get Export Job Details](get-export-job-details.md) and [Download Exported Data](download-exported-data.md) take no CONFIG attributes at all.

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7327](../../../foundations/error-codes.md#error-7327) | 400 | FILTERCRITERIAINVALID — criteria parsed but could not be converted into a query. |
| [7330](../../../foundations/error-codes.md#error-7330) | 400 | UNKNOWNCOLUMNINFILTERCRITERIA — A column named in criteria does not exist in the view. |
| [7331](../../../foundations/error-codes.md#error-7331) | 400 | FILTERCRITERIAPARSEERROR — criteria is syntactically malformed. |
| [7332](../../../foundations/error-codes.md#error-7332) | 400 | UNKNOWNTABLEINFILTERCRITERIA — A table qualifier in criteria is not part of the view. |
| [7333](../../../foundations/error-codes.md#error-7333) | 400 | INVALIDGROUPFUNCUSEINFILTERCRITERIA — An aggregate function was used in criteria. |
| [7401](../../../foundations/error-codes.md#error-7401) | 400 | The SQL statement is not a valid/allowed SQL construct. |
| [7543](../../../foundations/error-codes.md#error-7543) | 400 | ONLYBASETABLECOLINTABULARFILTERCRITERIA — criteria on a tabular view referenced a column outside its base table. |
| [7565](../../../foundations/error-codes.md#error-7565) | 400 | UNVERIFIEDEMAIL — The calling user's primary email address is not verified. |
| [7571](../../../foundations/error-codes.md#error-7571) | 400 | UNKNOWNVIEWIDPASSED — A tableCriteriaList[].viewId does not exist in this workspace. |
| [7801](../../../foundations/error-codes.md#error-7801) | 400 | MARGINVALUEEXCEEDS — A PDF margin is outside 0–1 inches. |
| [7803](../../../foundations/error-codes.md#error-7803) | 400 | INVALIDDIMENSION — width or height is outside the permitted image range. |
| [7824](../../../foundations/error-codes.md#error-7824) | 400 | EXPORTREQBLOCKED — Export has been blocked for this workspace. |
| [7827](../../../foundations/error-codes.md#error-7827) | 400 | EXPPDFRECORDLIMIT — The PDF exceeds 1,000,000 cells. |
| [7835](../../../foundations/error-codes.md#error-7835) | 400 | NOTABLESINVOLVEDINSQLEXPORT — The statement references no table. |
| [7836](../../../foundations/error-codes.md#error-7836) | 400 | GIVENTABLENOTINVOLVEDINSQLEXPORT — A tableCriteriaList[].viewId is not used by the statement. |
| [7837](../../../foundations/error-codes.md#error-7837) | 400 | INVOLVEDTABLEDOESNOTHAVEPERMISSION — A table used by the query has no matching tableCriteriaList entry where one is required. |
| [8001](../../../foundations/error-codes.md#error-8001) | 400 | INVALIDRESPFORMAT — responseFormat is not a supported value. |
| [8014](../../../foundations/error-codes.md#error-8014) | 400 | APIIMAGERESPONSENOTPOSSIBLE — image was requested for a view that is not a chart. |
| [8015](../../../foundations/error-codes.md#error-8015) | 400 | APIEXPORTCOLUMNNOTPRESENT — A name in selectedColumns does not match any column in the view. |
| [8017](../../../foundations/error-codes.md#error-8017) | 400 | INVALIDIMAGEFORMAT — imageFormat is not png, jpg, or jpeg. |
| [8077](../../../foundations/error-codes.md#error-8077) | 400 | EMPTYJSONCONFIGURATION — CONFIG was not sent, or was sent empty. |
| [8078](../../../foundations/error-codes.md#error-8078) | 400 | EMPTYJSONATTRIBUTEFOUND — A mandatory attribute was sent blank. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | A required attribute (expression or formulaName) is missing from CONFIG. |
| [8088](../../../foundations/error-codes.md#error-8088) | 400 | SECURITYCONTROLSFEATUREDISABLED — Export is disabled for the organization. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | INVALIDVALUEFORATTRIBUTE — fileType, onError, delimiter, quoted, thousandSeparator, or decimalSeparator is outside its permitted set. |
| [8120](../../../foundations/error-codes.md#error-8120) | 404 | EXPORTJOBNOTFOUND — No export job exists for the given ID (HTTP 404). |
| [8121](../../../foundations/error-codes.md#error-8121) | 400 | EXPORTJOBNOTINITIATED — The job is queued but has not started (jobCode 1001). |
| [8122](../../../foundations/error-codes.md#error-8122) | 400 | EXPORTJOBNOTCOMPLETED — The job is still running (jobCode 1002). |
| [8123](../../../foundations/error-codes.md#error-8123) | 400 | EXPORTJOBERROROCCURRED — The job failed (jobCode 1003). |
| [8124](../../../foundations/error-codes.md#error-8124) | 403 | EXPORTJOBACCESSDENIED — The caller did not create this job (HTTP 403). |
| [8125](../../../foundations/error-codes.md#error-8125) | 400 | Callback URL is malformed, unreachable, or private. |
| [8126](../../../foundations/error-codes.md#error-8126) | 400 | Callback URL is malformed, unreachable, or private. |
| [8127](../../../foundations/error-codes.md#error-8127) | 400 | Callback URL is malformed, unreachable, or private. |
| [8128](../../../foundations/error-codes.md#error-8128) | 400 | INTERNALERRORONINITIATINGEXPORT — The job could not be queued. |
| [8132](../../../foundations/error-codes.md#error-8132) | 400 | ASYNCEXPORTLIMITEXCEEDED — 5 export jobs are already queued or running for the organization. |
| [8188](../../../foundations/error-codes.md#error-8188) | 400 | EXPORTINVALIDPASSWORD — password is blank or shorter than 6 characters. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | SYSTEMTAGDATAWARNINGV2VALIDATIONCONFIRMATION — The view carries a restricted DATAWARNING system tag. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | MORETHANMAXLENGTH — roleName exceeds 30 characters, or permissions exceeds its size limit. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |
| [8547](../../../foundations/error-codes.md#error-8547) | 400 | ARRAYSIZEOUTOFRANGE — selectedColumns is empty or holds more than 300 entries. |

# Related

- [Data Operations](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
