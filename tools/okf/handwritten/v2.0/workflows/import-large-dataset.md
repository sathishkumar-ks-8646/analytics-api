---
type: Playbook
title: Load data into a table (small, large and very large files)
description: Choose between synchronous import, asynchronous import job and batch import, then create or fill a table and verify the result.
tags:
  - zoho-analytics
  - rest-api-v2
  - workflow
  - playbook
  - import
  - bulk
  - tables
sources:
  - id: markdown-docs
    resource: /domains/index.md
    title: API domain and group overviews in this bundle
generated:
  at: {{NOW}}
status: stable
---

# Goal

Get rows from a CSV, JSON, XML, Excel or Parquet payload into a new or existing Zoho Analytics table, choosing the right endpoint for the payload size.

# Decision

| Payload | New table | Existing table |
|---|---|---|
| Up to 20 MB file or 10,000,000 characters of text, result wanted inline | [Import Data into a New Table](/domains/data-operations/sync-data-import/import-data-new-table.md) | [Import Data into an Existing Table](/domains/data-operations/sync-data-import/import-data-existing-table.md) |
| Up to 100 MB file | [Create Import Job for a New Table](/domains/data-operations/async-data-import/create-import-job-new-table.md) | [Create Import Job for an Existing Table](/domains/data-operations/async-data-import/create-import-job-existing-table.md) |
| Larger than 100 MB (CSV only) | [Batch Import Data into New Table](/domains/data-operations/async-data-import/batch-import-new-table.md) | [Batch Import Data into Existing Table](/domains/data-operations/async-data-import/batch-import-existing-table.md) |

# Prerequisites

- Token scope `ZohoAnalytics.data.create` (new table) or the import scope named by the endpoint.
- Create Table permission on the workspace for new tables; for existing tables the share permission matching `importType` (`importAppend`, `importAddOrUpdate`, `importDeleteAllAdd`) unless you are a Workspace, Organization or Account Admin.
- `workspaceId`, and `viewId` of the target table for existing-table imports.

# Steps (synchronous and asynchronous)

1. **Build CONFIG.** New table: `{"tableName":"Sales","fileType":"csv","autoIdentify":true}`. Existing table: `{"importType":"UPDATEADD","fileType":"csv","autoIdentify":true,"matchingColumns":["Order ID"]}`. Add `onError` (`ABORT`, `SKIPROW`, `SETCOLUMNEMPTY`), `dateFormat`, separators or `columnDataTypes` as needed (see [Import options](/foundations/import-options-and-enums.md)).
2. **Send the request** as `multipart/form-data` with parts `CONFIG` and `FILE` (or, synchronous only, `DATA` holding the raw text). Set `Content-Type` accordingly.
3. **Read the result.** Synchronous: the response holds `totalRowCount`, `successRowCount`, `warnings`, `importErrors` and, for a new table, `data.viewId`. Asynchronous: keep `data.jobId`, poll [Get Import Job Details](/domains/data-operations/async-data-import/get-import-job-details.md) until `jobCode` `1004` or `1003`, then read the same counts.
4. **Verify** with [Get Table Metadata](/domains/data-modeling-and-schema/table-and-schema/get-table-metadata.md) (columns and types) or a small [synchronous export](/domains/data-operations/sync-data-export/export-data-view.md).

# Steps (batch import)

1. Split the CSV into batches under 100 MB each.
2. First request: CONFIG with `"batchKey":"start"`, `"isLastBatch":false` and the **full** import configuration. Keep the returned `batchKey` and `jobId`.
3. Middle requests: CONFIG with the returned `batchKey` and `"isLastBatch":false`.
4. Last request: `"isLastBatch":true`. `APPEND`/`UPDATEADD` commit per batch; `TRUNCATEADD` commits at the end.
5. Poll Get Import Job Details with `jobId`.

# Failure Handling

`7232` unparseable value under `ABORT` (fix data or use `SKIPROW`), `8079` missing CSV attributes with `autoIdentify:false`, `7092` table locked by another batch import (wait), `7137` target is not a table, `7337` batch job already closed.

# Related

- [Import options and enumerations](/foundations/import-options-and-enums.md)
- [Asynchronous jobs](/foundations/asynchronous-jobs.md)
- [Row Operations](/domains/data-operations/row-operations/overview.md) for single-row changes
