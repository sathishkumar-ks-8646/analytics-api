---
type: API Group
title: Workspace Backup & Restore
description: "APIs for listing and triggering workspace backups, downloading a backup, restoring a workspace from one, and tracking the status of either job."
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-backup-and-restore
  - api-group
api:
  domain: workspace-management
  group: workspace-backup-and-restore
  endpoint_count: 6
  endpoints:
    - operation_id: getWorkspaceBackups
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/backups"
      doc: "/domains/workspace-management/workspace-backup-and-restore/get-workspace-backups.md"
    - operation_id: backupWorkspaceNow
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/backups"
      doc: "/domains/workspace-management/workspace-backup-and-restore/backup-workspace-now.md"
    - operation_id: downloadWorkspaceBackup
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/download"
      doc: "/domains/workspace-management/workspace-backup-and-restore/download-workspace-backup.md"
    - operation_id: restoreWorkspaceFromBackup
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/restore"
      doc: "/domains/workspace-management/workspace-backup-and-restore/restore-workspace-from-backup.md"
    - operation_id: getWorkspaceBackupStatus
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/status"
      doc: "/domains/workspace-management/workspace-backup-and-restore/get-workspace-backup-status.md"
    - operation_id: getWorkspaceRestoreStatus
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/restores/{restore-id}/status"
      doc: "/domains/workspace-management/workspace-backup-and-restore/get-workspace-restore-status.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-20T17:34:40Z
generated:
  by: process:build_okf
  at: 2026-10-23T07:58:54Z
status: stable
---

# Summary

This document covers the V2 **Workspace Backup and Restore** REST APIs of Zoho Analytics — the APIs that list a workspace's backups, start a backup on demand, track its progress, download a backup file, restore the workspace from a backup, and track the restore.

APIs for listing and triggering workspace backups, downloading a backup, restoring a workspace from one, and tracking the status of either job.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Workspace Backups](get-workspace-backups.md) | GET | `/restapi/v2/workspaces/{workspace-id}/backups` | `getWorkspaceBackups` | `ZohoAnalytics.metadata.read` | 200 |
| [Backup Workspace Now](backup-workspace-now.md) | POST | `/restapi/v2/workspaces/{workspace-id}/backups` | `backupWorkspaceNow` | `ZohoAnalytics.metadata.create` | 200 |
| [Download Workspace Backup](download-workspace-backup.md) | GET | `/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/download` | `downloadWorkspaceBackup` | `ZohoAnalytics.metadata.read` | 200 |
| [Restore Workspace from Backup](restore-workspace-from-backup.md) | POST | `/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/restore` | `restoreWorkspaceFromBackup` | `ZohoAnalytics.metadata.create` | 200 |
| [Get Workspace Backup Status](get-workspace-backup-status.md) | GET | `/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/status` | `getWorkspaceBackupStatus` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Workspace Restore Status](get-workspace-restore-status.md) | GET | `/restapi/v2/workspaces/{workspace-id}/restores/{restore-id}/status` | `getWorkspaceRestoreStatus` | `ZohoAnalytics.metadata.read` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is a Workspace Backup in Zoho Analytics?

A workspace backup is a point-in-time copy of a workspace — its structure (tables, views, configuration) and, optionally, its data — stored as a single `.wsbkp` archive. A workspace keeps a small, rolling set of backups. They are created by the workspace's backup schedule or on demand through [Backup Workspace Now](backup-workspace-now.md). A backup can be downloaded, or used to return **the same workspace** to the state it captured.

| Concept | Where it appears | Notes |
|---------|------------------|-------|
| **Backup** | `backupId` | One stored copy of the workspace. Identified by a numeric ID returned by [Get Workspace Backups](get-workspace-backups.md) or [Backup Workspace Now](backup-workspace-now.md). |
| **Backup mode** | `backupMode` | `STRUCTURE_AND_DATA` or `STRUCTURE`. Fixed when the backup is taken. See [`backupMode` Values](overview.md#backupmode-values). |
| **Backup status** | `status` of [Get Workspace Backup Status](get-workspace-backup-status.md) | `IN_PROGRESS`, `SUCCESS`, `DELETED`, `FAILED`, `RETAINED`, `UNDO_BACKUP`. See [Backup `status` Values](overview.md#backup-status-values). |
| **Restore** | `restoreId` | One restore operation started by [Restore Workspace from Backup](restore-workspace-from-backup.md). It has its **own ID**, which is not the `backupId`. |
| **Restore mode** | `restoreMode` | What to restore from the backup. Defaults to the backup's own mode. See [`restoreMode` Values](overview.md#restoremode-values). |
| **Restore status** | `status` of [Get Workspace Restore Status](get-workspace-restore-status.md) | `INIT`, `SUCCESS`, `FAILURE`. See [Restore `status` Values](overview.md#restore-status-values). |

> **The single most important behaviour:** both [Backup Workspace Now](backup-workspace-now.md) and [Restore Workspace from Backup](restore-workspace-from-backup.md) are **asynchronous**. They return `200 OK` with `status: IN_PROGRESS` as soon as the work is queued, not when it is finished. A `200` from the restore API does **not** mean the workspace has been restored. Poll the matching status API until it leaves the in-progress state. See [Backup and Restore Lifecycle](overview.md#backup-and-restore-lifecycle).

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`). The read APIs use `ZohoAnalytics.metadata.read`; the two write APIs use `ZohoAnalytics.metadata.create` — see [OAuth scopes](../../../foundations/oauth-scopes.md).
> - All six APIs are **workspace-scoped** (`/restapi/v2/workspaces/<workspace-id>/...`) and require the `ZANALYTICS-ORGID` header.
> - `ZohoAnalytics_Server_URI` depends on the data centre (`analyticsapi.zoho.com`, `.eu`, etc.).
> - **All six APIs are disabled in Client Portal / White Label request contexts** and return [`7301`](../../../foundations/error-codes.md#error-7301).
> - **Only Account Admins and Organization Admins may call them.** Workspace Admins and custom-role users are refused with [`7301`](../../../foundations/error-codes.md#error-7301) — see [Permission Model](overview.md#permission-model).
> - **The organisation's plan must include Backup.** Otherwise every API returns [`6025`](../../../foundations/error-codes.md#error-6025).
> - API-unit cost per call: [Get Workspace Backups](get-workspace-backups.md) 1, [Backup Workspace Now](backup-workspace-now.md) 5, [Download Workspace Backup](download-workspace-backup.md) 1, [Restore Workspace from Backup](restore-workspace-from-backup.md) 10, [Get Workspace Backup Status](get-workspace-backup-status.md) 0.5, [Get Workspace Restore Status](get-workspace-restore-status.md) 0.5.
> - None of these APIs accepts a `criteria` attribute. There is no search, filter, sort or paging parameter.

---

# Backup and Restore Lifecycle

The two long-running operations follow the same pattern. Never treat the first response as the outcome.

| Step | Backup | Restore |
|------|--------|---------|
| 1. Start | [Backup Workspace Now](backup-workspace-now.md) → `backupId`, `status: IN_PROGRESS` | [Restore Workspace from Backup](restore-workspace-from-backup.md) → `restoreId`, `status: IN_PROGRESS` |
| 2. Poll | [Get Workspace Backup Status](get-workspace-backup-status.md) with the `backupId` | [Get Workspace Restore Status](get-workspace-restore-status.md) with the **`restoreId`** |
| 3. Finished when | `status` is `SUCCESS` (or `FAILED`) | `status` is `SUCCESS` (or `FAILURE`) |
| 4. Then | [Download Workspace Backup](download-workspace-backup.md), or use the backup for a restore | Read the workspace as normal |

**IDs are not interchangeable.** The restore status URL takes the `restoreId` returned by the restore call. Passing a `backupId` there returns [`8256`](../../../foundations/error-codes.md#error-8256). Passing a `restoreId` to the backup status URL returns [`8245`](../../../foundations/error-codes.md#error-8245).

**A restore returns the workspace to the state captured in the backup.** The request needs `"confirmRestore": true` for that reason; without it nothing is queued ([`8249`](../../../foundations/error-codes.md#error-8249)). A restore of a `STRUCTURE_AND_DATA` backup restores the workspace data as it was at backup time, so data loaded afterwards is not preserved. Take a fresh backup first if you may need to come back (note that only a small number of backups is kept — see [Limitations](overview.md#limitations)).

**Only one backup or restore runs per workspace at a time.** A second request while one is running is refused: [`8257`](../../../foundations/error-codes.md#error-8257) (backup running), [`8253`](../../../foundations/error-codes.md#error-8253) (restore running). Starting a backup is also refused while a connector sync is running ([`8255`](../../../foundations/error-codes.md#error-8255)).

**Reading the backup list can retire old backups.** [Get Workspace Backups](get-workspace-backups.md) marks backups beyond the newest three as `DELETED` as a side effect of the read. A backup that was restorable before the call can be gone afterwards. See [Limitations](overview.md#limitations).

**Restore pre-checks happen before the response.** The server downloads and validates the backup file while handling the restore request, so a `200` also means the file passed validation and the restore has been scheduled. A restore starts shortly afterwards (the scheduler delay defaults to 30 seconds) and the workspace is locked from the moment it is queued.

---

# Limitations

These are the limits that apply with **default settings**.

| Limitation | Value | Enforced by |
|------------|-------|-------------|
| **Callers** | Account Admins and Organization Admins only. | `7301` |
| **Plan** | The organisation's plan must include the Backup feature. | `6025` |
| **Backups retained** | The newest **3** backups. Older ones are marked `DELETED` when the backup list is read. | — |
| **Restore window** | A backup can be restored for **30 days** after it was created. After that, restore is refused. The window is a server setting. | `8248` |
| **Concurrency** | One backup or restore at a time per workspace. | `8257`, `8253` |
| **Backup during a connector sync** | Not allowed. | `8255` |
| **Restore across workspaces** | Not possible. A backup can only be restored into the workspace it was taken from. | `8245` |
| **Restoring a deleted or failed backup** | Not possible. | `8247` |
| **Restoring `STRUCTURE_AND_DATA` from a `STRUCTURE` backup** | Not possible — the backup holds no data. | `8254` |
| **Download format** | One `.wsbkp` archive per backup. No partial or per-table download. | — |
| **Deleting a backup** | **Not possible** through the API. | — |
| **`CONFIG` length** | **5,000** characters for [Backup Workspace Now](backup-workspace-now.md); **1,000** for [Restore Workspace from Backup](restore-workspace-from-backup.md). | — |

> **Request-format limits are enforced before the request reaches the handler.** A malformed `CONFIG`, a non-boolean `confirmRestore`, or an over-long `CONFIG` is rejected at that layer, not by one of the codes in the Error Codes tables below.

---

# Permission Model

| Role | May do | Notes |
|------|--------|-------|
| Account Admin / Organization Admin | All six APIs. | Authorisation is evaluated against the organisation that owns the workspace in the URL. |
| Workspace Admin | Nothing in this document. | Refused with `7301`, even for a workspace they administer. |
| Custom role, any permission | Nothing in this document. | Refused with `7301`. |
| Any user on a Client Portal / White Label domain | Nothing in this document. | Refused with `7301`; the APIs are disabled on those domains. |

> Both write APIs need the `ZohoAnalytics.metadata.create` scope, even though a restore overwrites existing workspace state. A token without it cannot start a backup or a restore.

---

# API-Specific Notes and Behaviours

## Get Workspace Backups

- **Use `isReadyToDownload`, not `isFailed`, to choose a usable backup.** `isFailed` is `true` for anything not ready.
- **Read the workspace-level flags defensively.** They are absent when the workspace has no backup information.
- **The read can retire old backups.** Backups beyond the newest three are marked `DELETED`.
- **Dependency chain:** [Workspace Operations](../workspace-operations/overview.md) → `<workspace-id>` → Get Workspace Backups.

## Backup Workspace Now

- **Treat `200` as "queued".** Poll [Get Workspace Backup Status](get-workspace-backup-status.md).
- **Check before retrying.** The call is not idempotent; a retry can create a second backup.
- **Dependency chain:** [Workspace Operations](../workspace-operations/overview.md) → `<workspace-id>` → Backup Workspace Now → `backupId` → Get Workspace Backup Status.

## Download Workspace Backup

- **Branch on the HTTP status before parsing.** Success is a file, failure is JSON.
- **Only `SUCCESS` backups download.** Every other state returns [`8246`](../../../foundations/error-codes.md#error-8246).
- **Dependency chain:** [Get Workspace Backup Status](get-workspace-backup-status.md) → Download Workspace Backup.

## Restore Workspace from Backup

- **This changes the workspace.** `confirmRestore: true` is required, and the workspace is locked while the restore runs.
- **Keep the `restoreId`.** It, and not the `backupId`, identifies the operation for polling.
- **Choose the backup first.** Check `isReadyToDownload`, creation date (30-day window) and `backupMode` before calling.
- **Dependency chain:** [Get Workspace Backups](get-workspace-backups.md) → Restore Workspace from Backup → `restoreId` → [Get Workspace Restore Status](get-workspace-restore-status.md).

## Get Workspace Backup Status

- **Stop polling on any value other than `IN_PROGRESS`.**
- **Dependency chain:** [Backup Workspace Now](backup-workspace-now.md) → Get Workspace Backup Status.

## Get Workspace Restore Status

- **`INIT` is the running state.** Stop on `SUCCESS` or `FAILURE`.
- **Dependency chain:** [Restore Workspace from Backup](restore-workspace-from-backup.md) → Get Workspace Restore Status.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Which endpoints return which body** | All APIs return `200 OK`. Five return the JSON envelope `{"status", "summary", "data"}`; [Download Workspace Backup](download-workspace-backup.md) returns the binary file with no envelope. |
| **Failure responses always carry a JSON body** | Including for the download API. `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name, not a localised sentence. |
| **IDs are strings** | `backupId` and `restoreId` are returned as JSON strings. |
| **Two `status` fields** | The envelope's `status` is `success` or `failure`. `data.status` on the polling and start APIs is the progress state. |
| **Start APIs return the initial state only** | `data.status` is `IN_PROGRESS` on the two POST APIs, whatever happens later. |
| **List response can be minimal** | [Get Workspace Backups](get-workspace-backups.md) returns only `backups: []` for a workspace with no backup information. |
| **Key order is not guaranteed** | Read by name, not position. |
| **Responses are extensible** | Some builds return additional fields. Ignore unrecognised keys rather than validating against a closed schema. |

---

# Enum and Value Reference

### `backupMode` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `STRUCTURE_AND_DATA` | The backup holds the workspace structure and its data. | Default for [Backup Workspace Now](backup-workspace-now.md). |
| `STRUCTURE` | The backup holds the structure only; no data. | Cannot be restored with `restoreMode: STRUCTURE_AND_DATA` (`8254`). |

### `restoreMode` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `STRUCTURE_AND_DATA` | Restore the structure and the data. | Only for a `STRUCTURE_AND_DATA` backup; refused for a `STRUCTURE` backup (`8254`). |
| `STRUCTURE` | Restore the structure only. | Allowed for either kind of backup. |

> Omit `restoreMode` to use the backup's own mode.

### Backup `status` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `IN_PROGRESS` | The backup is being created. | Cannot be downloaded or restored (`8246`). |
| `SUCCESS` | The backup completed. | The only state that can be downloaded or restored. |
| `DELETED` | The backup was retired, for example by the three-backup retention. | Cannot be downloaded (`8246`) or restored (`8247`). |
| `FAILED` | The backup failed. | Cannot be downloaded (`8246`) or restored (`8247`). |
| `RETAINED` | Internal state. | Cannot be downloaded or restored through this API (`8246`). |
| `UNDO_BACKUP` | Internal state. | Cannot be downloaded or restored through this API (`8246`). |

### Restore `status` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `INIT` | The restore is queued or running. | Response only. Keep polling. |
| `SUCCESS` | The restore completed. | Response only. Final. |
| `FAILURE` | The restore failed. | Response only. Final. |

---

# CONFIG Attribute Availability by API

| Attribute | Backup Workspace Now | Restore Workspace from Backup |
|-----------|---|---|
| `backupMode` | ✔ | — |
| `confirmRestore` | — | ✔ |
| `restoreMode` | — | ✔ |

> The other four APIs take no CONFIG.

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [6025](../../../foundations/error-codes.md#error-6025) | 400 | BACKUP_NOT_ALLOWED - The organisation's plan does not include Backup. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [8077](../../../foundations/error-codes.md#error-8077) | 400 | EMPTY_JSON_CONFIGURATION - CONFIG is present but empty. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | CONFIG is not valid JSON, was not URL-encoded correctly, contains an unsupported key, or violates a type or length constraint. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | The ZANALYTICS-ORGID header is missing from a request that requires it. |
| [8084](../../../foundations/error-codes.md#error-8084) | 400 | ORGID_NOT_EXIST - No organisation exists with the given ID. |
| [8245](../../../foundations/error-codes.md#error-8245) | 404 | BACKUP_NOT_FOUND - The backup does not exist, or does not belong to this workspace. |
| [8246](../../../foundations/error-codes.md#error-8246) | 400 | INVALID_MASTER_WORKSPACE_MAPPING - <workspace-id> is itself linked as a client of another master. |
| [8247](../../../foundations/error-codes.md#error-8247) | 400 | LINK_WORKSPACES_INCOMPATIBLE_WORKSPACES - At least one candidate failed the compatibility check. Nothing was linked. |
| [8248](../../../foundations/error-codes.md#error-8248) | 400 | SANDBOX_NOT_MAPPED_TO_MASTER_WORKSPACE - One or more sandboxIds are not linked to this master. The message names them. |
| [8249](../../../foundations/error-codes.md#error-8249) | 400 | INVALID_CONFIGURATION_REMOVE_LINKED_WORKSPACES - sandboxIds was supplied with scope: "ALL", or omitted with scope: "SELECTED". |
| [8251](../../../foundations/error-codes.md#error-8251) | 400 | INCORRECT_DATE_VALUE - A date in a date-range static filter could not be parsed. |
| [8253](../../../foundations/error-codes.md#error-8253) | 400 | RESTORE_ALREADY_IN_PROGRESS - A restore is running for this workspace. |
| [8254](../../../foundations/error-codes.md#error-8254) | 400 | INVALID_VALUE_FOR_ATTRIBUTE_FOR_COLUMN - latitude / longitude on a text column, or a place role on a numeric column. |
| [8255](../../../foundations/error-codes.md#error-8255) | 400 | INVALID_KEY_GIVEN - operation: "geo" on a column type that cannot be geocoded. |
| [8256](../../../foundations/error-codes.md#error-8256) | 404 | GEO_COL_COUNT_EXCEEDED - More than one text geo column on X, or more than one numeric geo column on one axis. |
| [8257](../../../foundations/error-codes.md#error-8257) | 400 | GEO_COL_COUNT_EXCEEDED_CATEGORICAL - A text geo column on X coexists with a numeric geo column on Y. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |

# Related

- [Workspace Management](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
