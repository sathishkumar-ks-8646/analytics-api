---
type: API Group
title: Asynchronous & Batch Data Import
description: APIs for creating and monitoring asynchronous import jobs and batch imports.
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - async-data-import
  - api-group
api:
  domain: data-operations
  group: async-data-import
  endpoint_count: 5
  endpoints:
    - operation_id: createImportJobNewTable
      method: POST
      path: "/restapi/v2/bulk/workspaces/{workspace-id}/data"
      doc: "/domains/data-operations/async-data-import/create-import-job-new-table.md"
    - operation_id: createImportJobExistingTable
      method: POST
      path: "/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data"
      doc: "/domains/data-operations/async-data-import/create-import-job-existing-table.md"
    - operation_id: batchImportNewTable
      method: POST
      path: "/restapi/v2/bulk/workspaces/{workspace-id}/data/batch"
      doc: "/domains/data-operations/async-data-import/batch-import-new-table.md"
    - operation_id: batchImportExistingTable
      method: POST
      path: "/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data/batch"
      doc: "/domains/data-operations/async-data-import/batch-import-existing-table.md"
    - operation_id: getImportJobDetails
      method: GET
      path: "/restapi/v2/bulk/workspaces/{workspace-id}/importjobs/{job-id}"
      doc: "/domains/data-operations/async-data-import/get-import-job-details.md"
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

This document covers the five **bulk** data-import REST APIs of Zoho Analytics — the APIs that hand a large payload to the server, get back a **job ID**, and let you track that job to completion.

Unlike the [synchronous import APIs](../sync-data-import/overview.md), none of these APIs returns the import result directly. Every one of them returns a job reference, and the outcome is retrieved later through [Get Import Job Details](get-import-job-details.md) or delivered to a [callback URL](overview.md#the-callbackurl-attribute).

APIs for creating and monitoring asynchronous import jobs and batch imports.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Create Import Job for a New Table (Asynchronous)](create-import-job-new-table.md) | POST | `/restapi/v2/bulk/workspaces/{workspace-id}/data` | `createImportJobNewTable` | `ZohoAnalytics.data.create` | 200 |
| [Create Import Job for an Existing Table (Asynchronous)](create-import-job-existing-table.md) | POST | `/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data` | `createImportJobExistingTable` | `ZohoAnalytics.data.create` | 200 |
| [Batch Import Data into New Table](batch-import-new-table.md) | POST | `/restapi/v2/bulk/workspaces/{workspace-id}/data/batch` | `batchImportNewTable` | `ZohoAnalytics.data.create` | 200 |
| [Batch Import Data into Existing Table](batch-import-existing-table.md) | POST | `/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data/batch` | `batchImportExistingTable` | `ZohoAnalytics.data.create` | 200 |
| [Get Import Job Details](get-import-job-details.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/importjobs/{job-id}` | `getImportJobDetails` | `ZohoAnalytics.data.create` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# The two families

The five APIs fall into two families that solve different problems, plus one shared monitoring API.

| | **Asynchronous Import** | **Batch Import** |
|---|---|---|
| **APIs** | [Create Import Job for a New Table (Asynchronous)](create-import-job-new-table.md)<br>[Create Import Job for an Existing Table (Asynchronous)](create-import-job-existing-table.md) | [Batch Import Data into New Table](batch-import-new-table.md)<br>[Batch Import Data into Existing Table](batch-import-existing-table.md) |
| **Calls per import** | **One** — the whole file in a single request | **Many** — one request per batch, all sharing one job |
| **Data size** | Up to 100 MB in total | Unlimited in total; **each batch** up to 100 MB |
| **File formats** | CSV, JSON, XML, Excel, Parquet, Geometry | **CSV only** |
| **Returns** | `jobId` | `batchKey` **and** `jobId` |
| **Use when** | The file fits in one request | The dataset is too large for one request and must be split |
| **Monitored by** | [Get Import Job Details](get-import-job-details.md) | [Get Import Job Details](get-import-job-details.md) |

> **Choosing between them.** If your file is under 100 MB, use the asynchronous import — it is one call. Reach for batch import only when the dataset genuinely will not fit, because it requires you to split the file, carry a `batchKey` across calls, and explicitly close the job.

> Notes that apply to all five APIs:
> - All are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`) and use the **`data`** scope family — see [OAuth scopes](../../../foundations/oauth-scopes.md).
> - All require the `ZANALYTICS-ORGID` header.
> - All are **available in Client Portal / White Label contexts**.
> - The four import APIs send the payload as a `FILE` part in a `multipart/form-data` request, together with a `CONFIG` part. They do **not** accept a `DATA` parameter — pasted data is a synchronous-import feature only.
> - All five return **HTTP 200** with a JSON body. None returns 204.
> - None accepts a `criteria` attribute. Which rows are loaded is decided by the file's contents and by `skipTop`.

---

# Limitations

These limits apply to every API in this document. They are hard limits — a request that exceeds one is rejected, not queued.

| Limitation | Value | Enforced by |
|------------|-------|-------------|
| **Maximum file size** | **100 MB** per uploaded file. For batch import this is **per batch**, not per job. | Rejected at upload |
| **Simultaneous import jobs** | **5** per organization. A job counts against the limit while it is queued or running. | `8134` |
| **Batches per batch-import job** | **100** | `7336` |
| **Import job summary retention** | **1 hour** after the job completes or fails. After that the summary is gone and [Get Import Job Details](get-import-job-details.md) can no longer return it. | `expiryTime` in the response |
| **Batch import file format** | **CSV only.** JSON, XML, Excel, Parquet, and Geometry are not supported by the batch APIs. | — |
| **Batch import ordering** | Batches are committed in the order they are received. A batch cannot be re-sent or reordered once accepted. | `7337`, `7338` |
| **Job visibility** | An import job can be queried **only by the user who created it**. | `8138` |

> **Poll, then persist.** Because the summary lives for one hour, an integration that needs a durable record of what was imported must read [Get Import Job Details](get-import-job-details.md) while the job is fresh and store the result itself.

---

# Workflow of the Asynchronous Import API

## 1. Create the import job

Call [Create Import Job for a New Table (Asynchronous)](create-import-job-new-table.md) or [Create Import Job for an Existing Table (Asynchronous)](create-import-job-existing-table.md). A unique **`jobId`** comes back in the response and is the reference for everything that follows.

## 2. Check the job status

Call [Get Import Job Details](get-import-job-details.md) with that `jobId`, periodically — **every 10 seconds** is a reasonable cadence. The response carries a **`jobCode`** describing the current state.

## JOBCODE and status messages

| JOBCODE | Status message | Description |
|---------|----------------|-------------|
| **1001** | `JOB NOT INITIATED` | Job creation acknowledged but not yet started. Retry after a short delay. |
| **1002** | `JOB IN PROGRESS` | The job is currently being processed. Continue polling. |
| **1003** | `ERROR OCCURRED` | An error occurred during the import. Stop polling and check the error message. |
| **1004** | `JOB COMPLETED` | The import finished successfully. The import summary is available in the response. |
| **1005** | `JOB NOT FOUND` | The `jobId` is not valid. Stop polling and verify it. |

## Handling each JOBCODE

| JOBCODE | What to do |
|---------|-----------|
| `1001` or `1002` | Wait a few seconds and repeat the status check. |
| `1003` | **Stop polling.** Inspect `jobInfo` for the error detail. |
| `1004` | **Stop polling.** The job is complete and `jobInfo` holds the import summary. |
| `1005` | **Stop polling.** Verify the `jobId` — it is invalid, or the job has passed its retention window. |

> `jobCode` is returned as a **string** (`"1004"`), not as a number.

---

# Workflow of the Batch Import API

Batch import splits one logical import across many HTTP calls that all feed a single job.

```
 Split the source CSV into batches, each under 100 MB
        │
        ▼
 POST …/data/batch      CONFIG: {"batchKey":"start", "isLastBatch":false, …full config…}
        │                        ── the server opens the job ──
        ▼
   response: { "batchKey": "1694703482470_…_SalesTable", "jobId": "1767024000008787011" }
        │
        ├── POST …/data/batch   CONFIG: {"batchKey":"<returned key>", "isLastBatch":false}   ← repeat per batch
        │
        ▼
   POST …/data/batch      CONFIG: {"batchKey":"<returned key>", "isLastBatch":true}
        │                        ── closes the job ──
        ▼
 GET …/importjobs/<jobId>   ← poll until jobCode is 1004 or 1003
```

| Step | Rule |
|------|------|
| **First batch** | Send `batchKey: "start"`. This is the only call that carries the full import configuration — `tableName`/`importType`, `autoIdentify`, and every parsing option are read here and here only. |
| **Response of the first batch** | Returns the real `batchKey` **and** the `jobId`. Keep both. |
| **Follow-up batches** | Send the returned `batchKey`. Only `batchKey` and `isLastBatch` are read; any other configuration in the CONFIG of a follow-up batch is ignored. |
| **Final batch** | Send `isLastBatch: true`. This closes the job — no further batch can be added (`7337`). |
| **Monitoring** | Use the `jobId` with [Get Import Job Details](get-import-job-details.md), exactly as for an asynchronous import. |

## When the data actually lands

| `importType` | Commit behaviour |
|--------------|------------------|
| `APPEND`, `UPDATEADD` | Each batch is committed as it is received. Data becomes visible progressively. |
| `TRUNCATEADD` | Nothing is committed until the final batch arrives. The existing rows are replaced in one step at the end. |

> Scheduled processing of the remaining batches begins automatically once the first batch has been imported, and batch order is preserved throughout.

---

# The `callbackUrl` Attribute

`callbackUrl` is an optional attribute of the asynchronous import CONFIG. It changes two things.

| Effect | Detail |
|--------|--------|
| **You get notified instead of polling** | When the job reaches a terminal state, Zoho Analytics sends an **HTTP POST** to your URL with `Content-Type: application/json`. The body is **exactly the same payload** that [Get Import Job Details](get-import-job-details.md) would return for that job — same `jobId`, `jobCode`, `jobStatus`, and `jobInfo` fields. |
| **The job is always processed asynchronously** | Without a callback, a small upload may be handled inline and finish almost immediately. Supplying `callbackUrl` **forces the job onto the asynchronous pipeline** regardless of file size, so the `jobId` is always meaningful and the callback always fires. |

Rules and constraints:

- The URL must be a well-formed, publicly reachable `http`/`https` address. A malformed URL is rejected with [`8125`](../../../foundations/error-codes.md#error-8125).
- URLs resolving to a **private or internal IP address** are rejected with [`8127`](../../../foundations/error-codes.md#error-8127) — the callback cannot be pointed at a LAN host.
- If the endpoint cannot be reached at validation time, the request fails with [`8126`](../../../foundations/error-codes.md#error-8126).
- Your endpoint should respond with a 2xx status. A non-2xx response is logged as a delivery failure.
- The callback is a **notification, not a guarantee** — always keep [Get Import Job Details](get-import-job-details.md) as a fallback, and remember the summary is only retained for one hour.

> `callbackUrl` is accepted by the two **asynchronous** import APIs and by the **first batch** of a batch import. It has no effect on follow-up batches.

---

# Permission Model

| API | Who may call it |
|-----|-----------------|
| [Create Import Job for a New Table (Asynchronous)](create-import-job-new-table.md), [Batch Import Data into New Table](batch-import-new-table.md) | An Account Admin or Organization Admin, or a Workspace Admin, or any user with **Create Table** permission on the workspace. |
| [Create Import Job for an Existing Table (Asynchronous)](create-import-job-existing-table.md), [Batch Import Data into Existing Table](batch-import-existing-table.md) | An Account Admin or Organization Admin, or a Workspace Admin, or any user holding the import permission matching the requested `importType` — see below. |
| [Get Import Job Details](get-import-job-details.md) | **Only the user who created the job.** Any other user, including an Account Admin, receives `8138`. |

## Import permission by `importType`

| `importType` | Permission required on the table | Equivalent share permission |
|--------------|----------------------------------|------------------------------|
| `APPEND` | Append Import | `importAppend` |
| `UPDATEADD` | Add or Update Import | `importAddOrUpdate` |
| `TRUNCATEADD` | Truncate and Add Import | `importDeleteAllAdd` |

> A user granted only `importAppend` can run an `APPEND` import but receives [`7301`](../../../foundations/error-codes.md#error-7301) for a `TRUNCATEADD` on the same table. Grant the specific import permissions through the [Sharing APIs](../../share-and-publish/sharing/share-views.md#permissions-fields).

---

# Shared CONFIG Attributes

All four import APIs draw on the same parsing and formatting options. They are listed once here and referenced from each API.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `onError` | String (enum) | `ABORT` | What to do when a value cannot be parsed. See [`onError` Values](overview.md#onerror-values). |
| `selectedColumns` | JSONArray of String | all columns | Import only these columns from the source. 1–300 entries. |
| `skipTop` | Integer | `0` | Number of leading rows to ignore before the header row. |
| `delimiter` | Integer (enum) | `0` | CSV field separator, `0`–`4`. **Mandatory when `autoIdentify` is `false`.** |
| `quoted` | Integer (enum) | `2` | CSV quote character, `0`–`2`. **Mandatory when `autoIdentify` is `false`.** |
| `commentChar` | String | none | Lines beginning with this character are ignored. CSV only. **Mandatory when `autoIdentify` is `false`.** |
| `thousandSeparator` | Integer (enum) | auto | Grouping separator in numeric values. See [Number Separator Values](overview.md#number-separator-values). |
| `decimalSeparator` | Integer (enum) | auto | Decimal separator in numeric values. See [Number Separator Values](overview.md#number-separator-values). |
| `columnSeparators` | JSONObject | — | Per-column separator overrides — column name → `[thousandSeparator, decimalSeparator]`, both as strings. Needs at least two entries (`8149`), and the two must differ (`8148`). |
| `dateFormat` | String | auto | Default date pattern for all date columns, e.g. `dd-MMM-yyyy`. An unparseable pattern fails with `7512`. |
| `columnDateFormat` | JSONObject | — | Per-column date pattern overrides. 1–300 entries. Takes precedence over `dateFormat`. |
| `columnTimeFormat` | JSONObject | — | Per-column time pattern overrides. |
| `columnDurationFormat` | JSONObject | — | Per-column duration pattern overrides. |
| `columnDataTypes` | JSONArray | auto-detected | Explicit data types instead of inference. Up to 500 entries. See [`columnDataTypes` Fields](overview.md#columndatatypes-fields). |
| `matchNulls` | Boolean | `false` | Treat empty source values as nulls when matching rows. Relevant to `UPDATEADD`. |
| `updateNullForNegativeValues` | Boolean | `false` | Store null instead of a negative value in columns that do not accept one. |
| `retainColumnNames` | Boolean | `false` | For JSON/XML sources, keep the original key names as column names. |
| `importHiddenRows` | Boolean | `false` | For Excel sources, include rows hidden in the sheet. |
| `importHiddenColumns` | Boolean | `false` | For Excel sources, include columns hidden in the sheet. |
| `callbackUrl` | String | — | Notification endpoint. See [The `callbackUrl` Attribute](overview.md#the-callbackurl-attribute). |

### `fileType` Values

`CSV`, `JSON`, `XML`, `XLS`, `XLSX`, `PARQUET`, `GEOMETRY`. Case-insensitive.

> Applies to the **asynchronous** import APIs only. The batch import APIs accept **CSV only** and have no `fileType` attribute.
>
> `delimiter`, `quoted`, and `commentChar` apply to CSV sources only and are ignored for every other type.

### `onError` Values

| Value | Behaviour | Effect on the job |
|-------|-----------|-------------------|
| `ABORT` | **Default.** The whole import is rolled back on the first unparseable value. | The job ends with `jobCode` `1003`; nothing is imported. |
| `SKIPROW` | The offending row is skipped; the rest are imported. | `jobCode` `1004`. `successRowCount` is lower than `totalRowCount`; skipped lines appear in `importErrors`. |
| `SETCOLUMNEMPTY` | The offending value is stored as empty; the rest of the row is imported. | `jobCode` `1004`. `warnings` is incremented and the reset values appear in `importErrors`. |

### Number Separator Values

| `thousandSeparator` | Character | | `decimalSeparator` | Character |
|--------------------:|-----------|---|-------------------:|-----------|
| `0` | Comma `,` | | `0` | Dot `.` |
| `1` | Dot `.` | | `1` | Comma `,` |
| `2` | Space | | | |
| `3` | Single quote `'` | | | |
| `4` | None | | | |

> The thousand and decimal separators must resolve to **different** characters, otherwise the import fails with [`8148`](../../../foundations/error-codes.md#error-8148).

### `columnDataTypes` Fields

| Field | Type | Mandatory | Description |
|-------|------|-----------|--------------|
| `columnName` | String | **Yes** | Name of the column in the source data. |
| `dataType` | String | **Yes** | Zoho Analytics data type, e.g. `PLAIN`, `NUMBER`, `DECIMAL_NUMBER`, `CURRENCY`, `DATE`, `EMAIL`, `URL`. |
| `geoRole` | String | No | Geographic role, when `dataType` is a geo type. |

> For an **existing-table** import, entries naming a column that already exists are discarded — an existing column keeps its established type.

---

# API-Specific Notes and Behaviours

## Create Import Job for a New Table (Asynchronous)

- **The one-call answer for files up to 100 MB.** Everything [Import Data into a New Table (Synchronous)](../sync-data-import/import-data-new-table.md) does, but without holding the connection open — at the cost of having to poll.
- **The created table's `viewId` is deferred.** It is not in this response; it arrives in `jobInfo.viewId` once `jobCode` reaches `1004`. Integrations that immediately need the table ID must poll before they can continue.
- **Name collisions fail fast.** `tableName` uniqueness is checked at job-creation time, so [`7111`](../../../foundations/error-codes.md#error-7111) is synchronous rather than a wasted job.
- **`callbackUrl` is what makes the job genuinely asynchronous.** Without it a small upload may be handled inline; with it the job always runs through the asynchronous pipeline so the callback can fire.
- **The 5-job ceiling is organization-wide.** It counts every queued or running job across the whole organization, including abandoned batch jobs that were never closed — a common cause of an unexpected [`8134`](../../../foundations/error-codes.md#error-8134).
- **Dependency chain:** [Get Workspace List](../../workspace-management/workspace-operations/overview.md) → Create Import Job → `jobId` → [Get Import Job Details](get-import-job-details.md) → `jobInfo.viewId`.

## Create Import Job for an Existing Table (Asynchronous)

- **Its permission requirement is a function of `importType`.** Three import modes map to three distinct permissions, so a [`7301`](../../../foundations/error-codes.md#error-7301) means "not allowed to do *this kind* of import", not "not allowed to import at all".
- **`TRUNCATEADD` is riskier here than in batch form.** The single-call version deletes the existing rows and then loads; because the work is asynchronous, a job that fails afterwards leaves the table emptier than it started. [Batch Import Data into Existing Table](batch-import-existing-table.md) defers the delete until the final batch, which is safer for large replacements.
- **Validation is split across two phases.** Structural errors (`importType`, `matchingColumns`, permissions) fail synchronously; data errors surface later as `jobCode` `1003`. A 200 here proves only that the *configuration* was acceptable.
- **`UPDATEADD` matches on values.** `matchingColumns` names the columns whose values form the key; there is no row ID involved.
- **Existing columns keep their types.** `columnDataTypes` only influences columns the import adds.
- **Dependency chain:** [Get View List](../../views-management/view-operations/get-views.md) → [Get Columns](../../data-modeling-and-schema/columns/overview.md) → Create Import Job → `jobId` → [Get Import Job Details](get-import-job-details.md).

## Batch Import Data into New Table

- **It is a stateful protocol, not a single call.** `"start"` opens the job, the returned `batchKey` threads the batches together, and `isLastBatch: true` closes it. Getting any of the three wrong is the main failure mode, which is why [`7337`](../../../foundations/error-codes.md#error-7337) and [`7338`](../../../foundations/error-codes.md#error-7338) exist.
- **The first batch is the only one that configures anything.** `tableName`, `autoIdentify`, `onError`, and every parsing option are read once. Sending different values on batch three changes nothing and gives no warning.
- **An unclosed job is a leaked resource.** Without a final batch the job never commits and keeps occupying one of the five concurrent slots until it expires. Always send the closing batch, even on an error path.
- **CSV only, with a per-batch ceiling.** There is no `fileType`; each batch may be up to 100 MB and a job may hold up to 100 batches.
- **Order is fixed at upload time.** Batches commit in the order received, and none can be re-sent or reordered.
- **Dependency chain:** first batch (`"start"`) → `batchKey` + `jobId` → follow-up batches → final batch → [Get Import Job Details](get-import-job-details.md) → `jobInfo.viewId`.

## Batch Import Data into Existing Table

- **The `batchKey` is bound to one table.** Sending a batch for the right key but the wrong `<view-id>` fails with [`7340`](../../../foundations/error-codes.md#error-7340) — a validation that the new-table variant has no need for.
- **Commit timing differs by `importType`, and it matters.** `APPEND` and `UPDATEADD` commit each batch as it lands, so the table changes progressively and a half-finished job leaves partial data. `TRUNCATEADD` holds everything until the final batch, which makes it the safer way to replace a large table.
- **The permission check happens on the first batch**, against the `importType` declared there.
- **Configuration is read once**, exactly as in the new-table variant.
- **The job must be closed.** An abandoned job holds a concurrent-job slot and, for `TRUNCATEADD`, never applies any of the uploaded data.
- **Dependency chain:** [Get View List](../../views-management/view-operations/get-views.md) → [Get Columns](../../data-modeling-and-schema/columns/overview.md) → first batch → follow-up batches → final batch → [Get Import Job Details](get-import-job-details.md).

## Get Import Job Details

- **The single monitoring endpoint for all four import APIs.** Whatever created the job — one call or fifty batches, new table or existing — this is how you learn the outcome.
- **Two independent success signals, and conflating them is the classic bug.** `status` is the API call's result; `jobCode` is the import's result. A completely failed import returns `"status": "success"` with `jobCode` `1003`, so code that checks only the HTTP status will report success for a failed load.
- **`jobInfo` only exists in terminal states.** Polling code must handle its absence for `1001` and `1002`.
- **It is the delivery point for a new table's `viewId`.** For a new-table job this response is the only place that ID appears.
- **Strictly private to the job's creator.** [`8138`](../../../foundations/error-codes.md#error-8138) for everyone else including admins — so the account that creates jobs must also be the account that polls them.
- **`1005` is ambiguous by design.** It covers both an invalid `jobId` and a job whose one-hour summary retention has lapsed. Persist the summary if you need it beyond that window.
- **It needs a `create` scope despite being a GET** — see [OAuth scopes](../../../foundations/oauth-scopes.md).
- **Dependency chain:** [Create Import Job for a New Table (Asynchronous)](create-import-job-new-table.md), [Create Import Job for an Existing Table (Asynchronous)](create-import-job-existing-table.md), [Batch Import Data into New Table](batch-import-new-table.md), or [Batch Import Data into Existing Table](batch-import-existing-table.md) → `jobId` → Get Import Job Details.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **All five APIs return HTTP 200 with a body** | None returns 204. The four import APIs return a job reference; the monitoring API returns job state. |
| **Failure responses share one shape** | `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name (e.g. `BATCH_IMPORT_INVALID_KEY`), not a localised sentence. |
| **`status` describes the call, `jobCode` describes the import** | The most important distinction in this document. An import that failed entirely is reported as `"status": "success"` with `jobCode` `"1003"`. |
| **`summary` does not distinguish the four import APIs** | All four return `"Create bulk import job"`, including every batch of a batch job. Use the presence of `batchKey` to tell a batch response from an asynchronous one. |
| **All IDs and codes are strings** | `jobId`, `batchKey`, `viewId`, `jobCode`, and `expiryTime` are JSON **strings**, even though `jobCode` and `expiryTime` are numeric in nature. Compare `jobCode` against `"1004"`, not `1004`. |
| **Counts are native numbers** | Inside `importSummary`, `totalColumnCount`, `selectedColumnCount`, `totalRowCount`, `successRowCount`, and `warnings` are genuine JSON numbers. |
| **Conditionally present keys** | `jobInfo` and `expiryTime` appear only in terminal states; `batchKey` only for batch jobs; `jobInfo.viewId` only for new-table jobs; `jobInfo.errorCode` / `errorMessage` only on failure. Test for key presence rather than assuming a fixed schema. |
| **A completed job can still have lost data** | Within `jobInfo`, compare `successRowCount` with `totalRowCount` and check `warnings` — `jobCode` `1004` only means the job ran to completion, not that every row landed. |
| **`importErrors` is HTML, not data** | A fragment of `<nobr>…</NOBR><br>` markup describing each offending line, field, and value. Display or log it; do not parse it. |
| **`columnDetails` uses display labels** | Values such as `"Plain Text"`, `"Positive Number"`, `"Currency"`, `"Geo Column"` — not the `dataType` codes accepted by `columnDataTypes` on the request side. The two vocabularies do not round-trip. |
| **The summary is transient** | Everything under `jobInfo` disappears one hour after the job finishes. Store what you need. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7092](../../../foundations/error-codes.md#error-7092) | 400 | A DDL lock is active on the table. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7107](../../../foundations/error-codes.md#error-7107) | 400 | The specified column does not exist in the table. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | A view with the given viewName already exists in this workspace. |
| [7164](../../../foundations/error-codes.md#error-7164) | 400 | The table is a snapshot table and its columns cannot be renamed. |
| [7165](../../../foundations/error-codes.md#error-7165) | 400 | Snapshot table data cannot be modified. |
| [7203](../../../foundations/error-codes.md#error-7203) | 400 | No file was uploaded for this batch, or it is empty. |
| [7248](../../../foundations/error-codes.md#error-7248) | 400 | The payload could not be parsed as the declared fileType. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7336](../../../foundations/error-codes.md#error-7336) | 400 | More than 100 batches were sent for one job. |
| [7337](../../../foundations/error-codes.md#error-7337) | 400 | A batch was sent after isLastBatch: true. |
| [7338](../../../foundations/error-codes.md#error-7338) | 400 | The specified group-id does not belong to this workspace. |
| [7340](../../../foundations/error-codes.md#error-7340) | 400 | The batchKey belongs to a different table. |
| [7478](../../../foundations/error-codes.md#error-7478) | 400 | The number of columns exceeds the maximum allowed for a table. |
| [7512](../../../foundations/error-codes.md#error-7512) | 400 | A date pattern could not be parsed. |
| [8046](../../../foundations/error-codes.md#error-8046) | 400 | A name in selectedColumns is not present in the source data. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | A mandatory attribute is missing from the configuration. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | Invalid value for attribute. |
| [8125](../../../foundations/error-codes.md#error-8125) | 400 | Callback URL is malformed, unreachable, or private. |
| [8126](../../../foundations/error-codes.md#error-8126) | 400 | Callback URL is malformed, unreachable, or private. |
| [8127](../../../foundations/error-codes.md#error-8127) | 400 | Callback URL is malformed, unreachable, or private. |
| [8134](../../../foundations/error-codes.md#error-8134) | 400 | The maximum number of simultaneous import jobs is in progress. |
| [8137](../../../foundations/error-codes.md#error-8137) | 400 | No import job exists with this ID. |
| [8138](../../../foundations/error-codes.md#error-8138) | 403 | The job was created by a different user. |
| [8148](../../../foundations/error-codes.md#error-8148) | 400 | Separator configuration errors. |
| [8149](../../../foundations/error-codes.md#error-8149) | 400 | A columnSeparators entry has fewer than two values. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | CONFIG was not sent. |
| [8516](../../../foundations/error-codes.md#error-8516) | 400 | A CONFIG value has the wrong JSON type. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |

# Related

- [Data Operations](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
