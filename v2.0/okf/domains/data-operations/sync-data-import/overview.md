---
type: API Group
title: Synchronous Data Import
description: APIs for importing data directly into new or existing tables.
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - sync-data-import
  - api-group
api:
  domain: data-operations
  group: sync-data-import
  endpoint_count: 2
  endpoints:
    - operation_id: importDataNewTable
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/data"
      doc: "/domains/data-operations/sync-data-import/import-data-new-table.md"
    - operation_id: importDataExistingTable
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data"
      doc: "/domains/data-operations/sync-data-import/import-data-existing-table.md"
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

This document covers the two **synchronous** data-import REST APIs of Zoho Analytics — the APIs that upload a CSV/JSON/XML/Excel payload and load it into a workspace, either by creating a new table or by writing into an existing one, and return the import result in the same HTTP response.

APIs for importing data directly into new or existing tables.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Import Data into a New Table (Synchronous)](import-data-new-table.md) | POST | `/restapi/v2/workspaces/{workspace-id}/data` | `importDataNewTable` | `ZohoAnalytics.data.create` | 200 |
| [Import Data into an Existing Table (Synchronous)](import-data-existing-table.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data` | `importDataExistingTable` | `ZohoAnalytics.data.create` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is a "Synchronous" import?

Both APIs accept the data **in the request itself** and return the outcome — rows loaded, columns detected, per-row errors — in the response body. There is no job to poll and no callback: when the call returns, the import has already finished (or already failed).

| | Synchronous import (this document) | Asynchronous / bulk import |
|---|---|---|
| **Endpoint** | `POST /workspaces/<id>/data` and `POST /workspaces/<id>/views/<id>/data` | `POST /bulk/workspaces/...` |
| **Result** | Returned inline in the same response | A job ID to poll |
| **Payload size** | Small to medium (see [Supplying the Data](overview.md#supplying-the-data)) | Large files |
| **Callback** | Not supported | Supported |

The two APIs here differ only in their **destination**:

| API | Destination | Key CONFIG attribute |
|-----|-------------|----------------------|
| [Import Data into a New Table (Synchronous)](import-data-new-table.md) | Creates a **new table** in the workspace and loads the data into it | `tableName` |
| [Import Data into an Existing Table (Synchronous)](import-data-existing-table.md) | Writes into an **existing table** | `importType` |

> Notes that apply to both APIs:
> - Both are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`) and use the scope **`ZohoAnalytics.data.create`**.
> - Both require the `ZANALYTICS-ORGID` header.
> - Both are **available in Client Portal / White Label contexts**.
> - `CONFIG` is **mandatory** for both, and the data must be supplied either as a `FILE` upload or as a `DATA` parameter — see [Supplying the Data](overview.md#supplying-the-data).
> - Neither API accepts a `criteria` attribute. Which rows are loaded is decided by the file's contents and by `skipTop`, not by a filter expression.

---

# How the Two APIs Relate

The two imports are two halves of one workflow, joined by the `viewId` that the first one produces.

```
 [Get View List]  ─────────────► <view-id> of an existing table
        │                                   │
        │                                   ▼
        │                    2. Import into an Existing Table
        │                       (APPEND / TRUNCATEADD / UPDATEADD)
        ▼
 1. Import into a New Table  ──► data.viewId  ──────────┘
        (creates the table)          │
                                     ▼
                          [Row APIs] [Export APIs] [Sharing] …
```

| Relationship | Detail |
|---|---|
| **The new-table import produces what the existing-table import consumes** | `data.viewId` from [Import Data into a New Table (Synchronous)](import-data-new-table.md) is the `<view-id>` for every later call — subsequent imports into the same table, the [Row APIs](../row-operations/overview.md), exports, sharing, and so on. It is returned **only** by that API. |
| **The new-table import is create-once** | Re-running [Import Data into a New Table (Synchronous)](import-data-new-table.md) with the same `tableName` fails with `7111`, because the table already exists. Loading more data into that table is the job of [Import Data into an Existing Table (Synchronous)](import-data-existing-table.md). |
| **`importType` exists only on the existing-table import** | A new table is always populated by a straight load, so [Import Data into a New Table (Synchronous)](import-data-new-table.md) has no `importType`. The response reports it as `APPEND` for consistency. |
| **The two have different permission models** | [Import Data into a New Table (Synchronous)](import-data-new-table.md) is gated on creating tables in the workspace; [Import Data into an Existing Table (Synchronous)](import-data-existing-table.md) is gated per `importType` on the target table. See [Permission Model](overview.md#permission-model). |
| **Everything else is shared** | `fileType`, `autoIdentify`, `onError`, parsing options, date/number formats, and the whole response shape are identical between them. |

## Typical sequences

| Goal | Calls |
|------|-------|
| Load a brand-new dataset | [Import Data into a New Table (Synchronous)](import-data-new-table.md) → keep `data.viewId` |
| Add this month's rows to that dataset | [Import Data into an Existing Table (Synchronous)](import-data-existing-table.md) with `importType: "APPEND"` |
| Replace the dataset wholesale | [Import Data into an Existing Table (Synchronous)](import-data-existing-table.md) with `importType: "TRUNCATEADD"` |
| Merge updates by key | [Import Data into an Existing Table (Synchronous)](import-data-existing-table.md) with `importType: "UPDATEADD"` + `matchingColumns` |
| Verify what landed | [Get View Details](../../views-management/view-operations/get-view-details.md) or [Get Columns](../../data-modeling-and-schema/columns/overview.md) on the `viewId` |

---

# Supplying the Data

The payload is sent in **one** of two ways. Both APIs accept both modes.

| Mode | Parameter | Limit | Notes |
|------|-----------|-------|-------|
| **File upload** | `FILE` | **20 MB** (20480 KB) | `multipart/form-data`. The file is antivirus-scanned before it is read. The filename may not contain characters outside the permitted set. |
| **Pasted data** | `DATA` | **10,000,000 characters** | The raw file content sent as a form parameter. Exceeding the limit fails with `8139`. |

> If `DATA` is present and non-empty it is used; otherwise the uploaded `FILE` is read. The `fileType` attribute tells the parser how to interpret whichever one you send — it is not inferred from the file's extension.

---

# Permission Model

The two APIs are gated differently, and the requirement for [Import Data into an Existing Table (Synchronous)](import-data-existing-table.md) **changes with `importType`**.

## Import Data into a New Table (Synchronous)

The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with **Create Table** permission on the workspace.

## Import Data into an Existing Table (Synchronous)

The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user holding the import permission that corresponds to the `importType` being used:

| `importType` | Permission required on the table | Equivalent share permission |
|--------------|----------------------------------|------------------------------|
| `APPEND` | Append Import | `importAppend` |
| `UPDATEADD` | Add or Update Import | `importAddOrUpdate` |
| `TRUNCATEADD` | Truncate and Add Import | `importDeleteAllAdd` |

> A user granted only `importAppend` can run an `APPEND` import on a shared table but receives [`7301`](../../../foundations/error-codes.md#error-7301) for a `TRUNCATEADD` on the same table. Grant the specific import permissions through the [Sharing APIs](../../share-and-publish/sharing/share-views.md#permissions-fields).

---

# Table Preconditions (Existing-Table Import)

Before an existing-table import runs, the target table is checked:

| Condition | Error |
|-----------|-------|
| The table must not be a snapshot table | `7165` |
| The table must not be a system table | `7164` |
| No batch import may be holding a DDL lock on the table | `7092` |
| The table must belong to the workspace in the URL | `7319` |
| The caller's IP must be within the workspace's permitted range, when IP restriction is enabled | `7301` |

The new-table import has no such checks — there is no existing table yet — but the `tableName` must be unused in the workspace ([`7111`](../../../foundations/error-codes.md#error-7111)).

---

# API-Specific Notes and Behaviours

## Import Data into a New Table (Synchronous)

- **It is the only source of the new table's `viewId`.** Everything downstream — further imports, [Row APIs](../row-operations/overview.md), exports, sharing — needs that ID, and it appears in no other response. Capture it from `data.viewId` on the very first call.
- **Create-once, by design.** A second call with the same `tableName` fails with [`7111`](../../../foundations/error-codes.md#error-7111) rather than appending. The API deliberately refuses to guess whether you meant "create" or "load more"; the latter is [Import Data into an Existing Table (Synchronous)](import-data-existing-table.md).
- **`onError` defaults to the strictest setting.** `ABORT` means one bad cell in a 100,000-row file leaves you with no table and a [`7232`](../../../foundations/error-codes.md#error-7232). For unattended loading, choose `SKIPROW` or `SETCOLUMNEMPTY` deliberately and then read `importErrors`.
- **`columnDetails` is the type-inference report, and it matters most here.** A new table's column types are decided by this one call and are awkward to change afterwards. When `autoIdentify` is `true`, always check that `Sales` came back as `Currency` rather than `Plain Text` — a wrong `thousandSeparator` is the usual cause.
- **`autoIdentify: false` turns two optional attributes into mandatory ones.** `delimiter` and `quoted` must both be present for CSV, and their absence surfaces as [`8079`](../../../foundations/error-codes.md#error-8079) rather than as a validation message about `autoIdentify`.
- **HTTP 200 does not mean every row landed.** `successRowCount` and `warnings` are the real success indicators.
- **Dependency chain:** [Get Workspace List](../../workspace-management/workspace-operations/overview.md) → Import into a New Table → `data.viewId` → everything else.

## Import Data into an Existing Table (Synchronous)

- **Its permission requirement is a function of `importType`.** Four import modes map to four distinct permissions, so [`7301`](../../../foundations/error-codes.md#error-7301) here means "not allowed to do *this kind* of import", not "not allowed to import". This is the single most common source of confusion with this API — check the [Permission Model](overview.md#permission-model) table before assuming a token or role problem.
- **`TRUNCATEADD` is destructive and unguarded.** It deletes every existing row before writing, with no dry-run, no confirmation, and no row-level trash. Combined with `onError: "ABORT"`, a malformed file can leave the table emptier than it started.
- **`UPDATEADD` matches on values, not identity.** `matchingColumns` names the columns whose values form the key; there is no row ID involved. A column name that does not exist fails with [`7107`](../../../foundations/error-codes.md#error-7107), and `matchNulls` decides whether empty source values participate in the match.
- **It cannot change an existing column's type.** `columnDataTypes` entries for columns already in the table are silently discarded, so this attribute only affects columns the import introduces.
- **No `viewId` in the response**, since the destination was already known — the response is otherwise identical to that of [Import Data into a New Table (Synchronous)](import-data-new-table.md).
- **The table is DDL-locked for the duration**, so concurrent structural changes are blocked and a competing import fails with [`7092`](../../../foundations/error-codes.md#error-7092).
- **Dependency chain:** [Import Data into a New Table (Synchronous)](import-data-new-table.md) or [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>` → [Get Columns](../../data-modeling-and-schema/columns/overview.md) → Import Data into an Existing Table (Synchronous).

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Both APIs return HTTP 200 with a body** | Neither returns 204. The full import result — counts, detected types, and per-line errors — is delivered inline, because these are the synchronous imports. |
| **Failure responses share one shape** | `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name (e.g. `IMPORT_ABORTED`), not a localised sentence. |
| **`summary` is `"Import data"` for both** | The success summary does not distinguish new-table from existing-table imports. Use the presence of `viewId`, or `importSummary.importOperation`, to tell them apart. |
| **`importOperation` is the discriminator** | `"created"` from the new-table import, `"updated"` from the existing-table import. It is the only field in `importSummary` that differs structurally between the two APIs. |
| **`viewId` is conditionally present** | Returned only by the new-table import. Test for the key rather than assuming it. |
| **A 200 can still hide data loss** | `successRowCount < totalRowCount` means rows were skipped; `warnings > 0` means values were reset to empty. Neither raises an error, so both must be checked explicitly. |
| **`importErrors` is HTML, not data** | It is a fragment of `<nobr>…</NOBR><br>` markup describing each offending line, field, and value. Display or log it — do not parse it. It is always present, empty (`""`) when the import was clean. |
| **`columnDetails` uses display labels, not type codes** | Values are human-readable names such as `"Plain Text"`, `"Positive Number"`, `"Decimal Number"`, `"Currency"`, `"Percentage"`, `"Date"`, `"E-Mail"`, `"URL"`, `"Geo Column"` — not the `dataType` codes accepted by `columnDataTypes` on the request side. The two vocabularies do not round-trip. |
| **Counts are native numbers** | `totalColumnCount`, `selectedColumnCount`, `totalRowCount`, `successRowCount`, and `warnings` are genuine JSON numbers; `viewId` is a string. |
| **`importType` is echoed in upper case** | Regardless of the casing sent, and including the synthetic `"APPEND"` reported by the new-table import. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7092](../../../foundations/error-codes.md#error-7092) | 400 | DDLLOCKSINCEIMPORTINPROGRESS — A batch import is holding a lock in this workspace. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7107](../../../foundations/error-codes.md#error-7107) | 400 | The specified column does not exist in the table. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | METADBOBJECTNAMEDUPLICATED — An object with this tableName already exists. |
| [7164](../../../foundations/error-codes.md#error-7164) | 400 | SYSTEMTABLEDATAMOD — System table data cannot be modified. |
| [7165](../../../foundations/error-codes.md#error-7165) | 400 | SNAPSHOTTABLEDATAMOD — Snapshot table data cannot be modified. |
| [7208](../../../foundations/error-codes.md#error-7208) | 400 | IMPORTFILENUMBEROFFIELDSEXCEEDSSIZE — A row contains more fields than the header defines. |
| [7232](../../../foundations/error-codes.md#error-7232) | 400 | IMPORTABORTED — A value could not be parsed and onError is ABORT. errorMessage carries the per-line detail. |
| [7248](../../../foundations/error-codes.md#error-7248) | 400 | INVALIDFILECONTENT — The payload could not be parsed as the declared fileType. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7478](../../../foundations/error-codes.md#error-7478) | 400 | MORETHANMAXCOLUMN — The source has more columns than a table can hold. |
| [7512](../../../foundations/error-codes.md#error-7512) | 400 | INVALIDDATEFORMAT — A date pattern could not be parsed. |
| [8046](../../../foundations/error-codes.md#error-8046) | 400 | INVALIDCOLUMNSSELECTED — A name in selectedColumns is not present in the source data. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | A required attribute (expression or formulaName) is missing from CONFIG. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | INVALIDVALUEFORATTRIBUTE — fileType, onError, delimiter, quoted, thousandSeparator, or decimalSeparator is outside its permitted set. |
| [8139](../../../foundations/error-codes.md#error-8139) | 400 | PASTEDDATALIMITEXCEEDED — The DATA parameter exceeds 10,000,000 characters. |
| [8148](../../../foundations/error-codes.md#error-8148) | 400 | Separator configuration errors. |
| [8149](../../../foundations/error-codes.md#error-8149) | 400 | DECIMALANDTHOUSANDCOLUMNSEPARATORLEGNTHVALIDATION — A columnSeparators entry has fewer than two values. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | LESSTHANMINOCCURANCE — CONFIG was not sent. |
| [8516](../../../foundations/error-codes.md#error-8516) | 400 | UNABLETOPARSEDATATYPE — A CONFIG value has the wrong JSON type. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |

# Related

- [Data Operations](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
