---
type: Concept
title: Asynchronous jobs (export and import)
description: How background jobs work in Zoho Analytics REST API v2 - job creation, jobCode states, polling, callbackUrl notifications, batch import keys, retention and ownership rules.
tags:
  - zoho-analytics
  - rest-api-v2
  - asynchronous
  - jobs
  - polling
  - callback
  - bulk
sources:
  - id: md-async-export
    resource: /domains/data-operations/async-data-export/overview.md
    title: Asynchronous Data Export - group overview
  - id: md-async-import
    resource: /domains/data-operations/async-data-import/overview.md
    title: Asynchronous & Batch Data Import - group overview
generated:
  at: {{NOW}}
status: stable
---

# Summary

Large data movements run as **jobs** under the `/restapi/v2/bulk/...` prefix. A creation call validates the request, returns a `jobId` immediately, and the work happens in the background. You then either **poll** the job-details endpoint or receive an **HTTP POST callback**, and for exports you finally **download** the file. Synchronous alternatives exist for small payloads (see [Synchronous Data Export](/domains/data-operations/sync-data-export/overview.md) and [Synchronous Data Import](/domains/data-operations/sync-data-import/overview.md)).

# Lifecycle

```text
Create job  ──►  jobId
                  │
                  ▼
Get job details ──► jobCode 1001 / 1002  → wait, poll again
                  │
                  ├─► jobCode 1003        → failed; create a new job
                  │
                  └─► jobCode 1004        → done; export: downloadUrl + expiryTime
                                             import: row counts and import errors
```

# Job Codes

| `jobCode` | `jobStatus` | Meaning | Action |
|---|---|---|---|
| `1001` | `JOB NOT INITIATED` | Accepted and queued. | Poll again after a few seconds. |
| `1002` | `JOB IN PROGRESS` | Running. | Poll again after a few seconds. |
| `1003` | `ERROR OCCURRED` | Terminal failure. | Stop polling; read the error details; create a new job after fixing the cause. |
| `1004` | `JOB COMPLETED` | Terminal success. | Export: read `downloadUrl` and `expiryTime`, then download. Import: read the result counts. |
| `1005` | `JOB NOT FOUND` | No such job: never created, wrong ID, or past retention. | Stop polling; verify the ID. |

`downloadUrl` and `expiryTime` are present **only** when `jobCode` is `1004`; test for the keys.

# Endpoints

| Step | Export | Import |
|---|---|---|
| Create | [Create Export Job using View ID](/domains/data-operations/async-data-export/create-export-job-view-id.md), [Create Export Job using SQL Query](/domains/data-operations/async-data-export/create-export-job-sql-query.md) | [Create Import Job for a New Table](/domains/data-operations/async-data-import/create-import-job-new-table.md), [Create Import Job for an Existing Table](/domains/data-operations/async-data-import/create-import-job-existing-table.md), Batch Import (new / existing table) |
| Monitor | [Get Export Job Details](/domains/data-operations/async-data-export/get-export-job-details.md) | [Get Import Job Details](/domains/data-operations/async-data-import/get-import-job-details.md) |
| Collect | [Download Exported Data](/domains/data-operations/async-data-export/download-exported-data.md) | Not needed; data is in the table. |

# Polling Rules

- Poll every few seconds with modest backoff; jobs for small views finish in seconds, large exports can take minutes.
- Downloading before completion is an **error, not a wait**: `8121` while queued, `8122` while running.
- Only the **creator** of a job can poll or download it; anyone else, including an Account Admin, receives `8124`.
- Export jobs and their files are retained for **72 hours from creation**; afterwards the job answers `1005` or `8120`.
- At most **5 export jobs** may be queued or running per organization (`8132`).

# callbackUrl

Both export creation endpoints and the import job endpoints accept an optional `callbackUrl`.

- When the job reaches a terminal state, Zoho Analytics sends **one** `HTTP POST` with `Content-Type: application/json` to the URL. The body is the job-details `data` object (`jobId`, `jobCode`, `jobStatus`, and for a successful export `downloadUrl`, `expiryTime`), **not** wrapped in the `status`/`summary`/`data` envelope.
- It fires on failure too; read `jobCode`.
- Constraints: well-formed public `http`/`https` URL, at most 10,000 characters (`8125` if malformed), not a private or internal IP (`8127`), reachable at request time (`8126`, and the job is not created).
- Respond with a 2xx. Delivery is attempted **once**, with no retry; a failed callback does not affect the job. Keep polling as the fallback.
- The callback replaces the poll, not the download.

# Batch Import

When a CSV does not fit in one 100 MB request, use the batch endpoints: send the first batch with `batchKey: "start"` and the full CONFIG; the response returns the real `batchKey` and the `jobId`; send following batches with that `batchKey` and `isLastBatch: false`; close with `isLastBatch: true` (no further batches, `7337`). `APPEND` and `UPDATEADD` commit each batch as it arrives; `TRUNCATEADD` commits everything at the end. Monitor with Get Import Job Details. Details: [Asynchronous & Batch Data Import](/domains/data-operations/async-data-import/overview.md).

# Related

- [Rate limits and quotas](/foundations/rate-limits-and-quotas.md)
- [Export formats and enums](/foundations/export-formats-and-enums.md)
- [Import options and enums](/foundations/import-options-and-enums.md)
- Workflow: [Export a view or dashboard asynchronously](/workflows/export-data-asynchronously.md)
