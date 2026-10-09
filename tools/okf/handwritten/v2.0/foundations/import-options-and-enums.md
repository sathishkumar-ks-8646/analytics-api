---
type: Reference
title: Import options and enumerations
description: The CONFIG vocabulary shared by the Zoho Analytics REST API v2 import endpoints - importType modes, fileType, autoIdentify, onError, number separators, columnDataTypes, matchingColumns, payload limits, and the permission each mode needs.
tags:
  - zoho-analytics
  - rest-api-v2
  - import
  - enums
  - csv
  - json
  - bulk
sources:
  - id: md-sync-import
    resource: /domains/data-operations/sync-data-import/overview.md
    title: Synchronous Data Import - group overview
  - id: md-async-import
    resource: /domains/data-operations/async-data-import/overview.md
    title: Asynchronous & Batch Data Import - group overview
generated:
  at: {{NOW}}
status: stable
---

# Summary

Six endpoints load data into tables. They share the same CONFIG vocabulary and differ in size limits, synchronicity and destination.

| Endpoint | Destination | Synchronous | Payload | Formats |
|---|---|---|---|---|
| [Import Data into a New Table](/domains/data-operations/sync-data-import/import-data-new-table.md) | New table (`tableName`) | Yes, result in response | `FILE` up to 20 MB or `DATA` up to 10,000,000 characters | CSV, JSON, XML, XLS, XLSX, Parquet, Geometry |
| [Import Data into an Existing Table](/domains/data-operations/sync-data-import/import-data-existing-table.md) | Existing table (`importType`) | Yes | Same | Same |
| [Create Import Job for a New Table](/domains/data-operations/async-data-import/create-import-job-new-table.md) | New table | No, returns `jobId` | `FILE` up to 100 MB | CSV, JSON, XML, Excel, Parquet, Geometry |
| [Create Import Job for an Existing Table](/domains/data-operations/async-data-import/create-import-job-existing-table.md) | Existing table | No | `FILE` up to 100 MB | Same |
| Batch Import into New / Existing Table | New or existing table | No, many requests share one job | Unlimited total, each batch up to 100 MB | **CSV only** |

Choose synchronous import for small files when you want the result inline, the asynchronous job for files up to 100 MB, and batch import only when the data will not fit in one request. See [Asynchronous jobs](/foundations/asynchronous-jobs.md).

# importType (existing-table imports)

| Value | Behaviour | Needs `matchingColumns` | Share permission required |
|---|---|---|---|
| `APPEND` | Adds every incoming row; keeps existing rows. | No | `importAppend` |
| `TRUNCATEADD` | Deletes all existing rows, then adds the incoming ones. | No | `importDeleteAllAdd` |
| `UPDATEADD` | Updates rows whose `matchingColumns` values match an incoming row; adds the rest. | **Yes** | `importAddOrUpdate` |

Any other value fails with `8119`. Workspace Admins, Account Admins and Organization Admins bypass the share-permission requirement.

# fileType

`CSV`, `JSON`, `XML`, `XLS`, `XLSX`, `PARQUET`, `GEOMETRY` (case-insensitive). The type is **not inferred from the file name**. The CSV parsing attributes `delimiter`, `quoted` and `commentChar` apply to CSV only. Batch import accepts CSV only.

# autoIdentify and CSV Parsing

| `autoIdentify` | Effect |
|---|---|
| `true` | Zoho Analytics detects the delimiter, quote character and each column's data type; `delimiter` and `quoted` become optional overrides. |
| `false` | Nothing is inferred; `delimiter` and `quoted` are **mandatory** for CSV (`8079` if missing). |

Other parsing attributes: `skipTop` (number of leading lines to ignore), `commentChar`, `dateFormat` (Java date pattern applied to date columns), `thousandSeparator` and `decimalSeparator` (below).

# onError

| Value | Behaviour | Effect on the response |
|---|---|---|
| `ABORT` | **Default.** Whole import rolled back on the first unparseable value. | Fails with `7232`; `errorMessage` carries per-line detail. Nothing imported. |
| `SKIPROW` | The offending row is skipped. | HTTP 200; `successRowCount` lower than `totalRowCount`; skipped lines listed in `importErrors`. |
| `SETCOLUMNEMPTY` | The offending value is stored empty; the rest of the row is imported. | HTTP 200; `warnings` incremented; reset values listed in `importErrors`. |

# Number Separators

| `thousandSeparator` | Character | `decimalSeparator` | Character |
|---|---|---|---|
| `0` | Comma `,` | `0` | Dot `.` |
| `1` | Dot `.` | `1` | Comma `,` |
| `2` | Space | | |
| `3` | Single quote `'` | | |
| `4` | None | | |

The two separators must resolve to different characters (`8148` otherwise).

# columnDataTypes

An array of objects fixing the type of specific columns instead of relying on detection:

| Field | Mandatory | Description |
|---|---|---|
| `columnName` | Yes | Column name in the source data. |
| `dataType` | Yes | Zoho Analytics data type, for example `PLAIN`, `MULTI_LINE`, `NUMBER`, `POSITIVE_NUMBER`, `DECIMAL_NUMBER`, `CURRENCY`, `PERCENT`, `DATE`, `BOOLEAN`, `EMAIL`, `URL`, `AUTO_NUMBER`, geo types. |
| `geoRole` | No | Geographic role when `dataType` is a geo type. |

# Result Fields

Successful imports report `totalRowCount`, `successRowCount`, `warnings`, `importErrors` and the table's `viewId` (`data.viewId` for new tables) plus detected column types. Read `successRowCount` against `totalRowCount` even on HTTP 200 when `onError` is not `ABORT`.

# Preconditions and Common Failures

| Condition | Code |
|---|---|
| Target is not a table (report, dashboard, query table) | `7137` |
| Table locked by a running batch import (DDL lock) | `7092` |
| `DATA` exceeds 10,000,000 characters | `8139` |
| Mandatory CSV attributes missing with `autoIdentify: false` | `8079` |
| Unparseable value with `onError: ABORT` | `7232` |
| Unparseable date pattern | `7512` |
| Batch job already closed by `isLastBatch: true` | `7337` |

# Related

- [Synchronous Data Import](/domains/data-operations/sync-data-import/overview.md)
- [Asynchronous & Batch Data Import](/domains/data-operations/async-data-import/overview.md)
- [Row Operations](/domains/data-operations/row-operations/overview.md) for single-row writes
- Workflow: [Load a large dataset](/workflows/import-large-dataset.md)
