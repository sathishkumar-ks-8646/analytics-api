# Zoho Analytics V2 REST API — Workspace Backup and Restore

This document covers the V2 **Workspace Backup and Restore** REST APIs of Zoho Analytics — the APIs that list a workspace's backups, start a backup on demand, track its progress, download a backup file, restore the workspace from a backup, and track the restore.

## What is a Workspace Backup in Zoho Analytics?

A workspace backup is a point-in-time copy of a workspace — its structure (tables, views, configuration) and, optionally, its data — stored as a single `.wsbkp` archive. A workspace keeps a small, rolling set of backups. They are created by the workspace's backup schedule or on demand through [Backup Workspace Now](#2-backup-workspace-now). A backup can be downloaded, or used to return **the same workspace** to the state it captured.

| Concept | Where it appears | Notes |
|---------|------------------|-------|
| **Backup** | `backupId` | One stored copy of the workspace. Identified by a numeric ID returned by [Get Workspace Backups](#1-get-workspace-backups) or [Backup Workspace Now](#2-backup-workspace-now). |
| **Backup mode** | `backupMode` | `STRUCTURE_AND_DATA` or `STRUCTURE`. Fixed when the backup is taken. See [`backupMode` Values](#backupmode-values). |
| **Backup status** | `status` of [Get Workspace Backup Status](#5-get-workspace-backup-status) | `IN_PROGRESS`, `SUCCESS`, `DELETED`, `FAILED`, `RETAINED`, `UNDO_BACKUP`. See [Backup `status` Values](#backup-status-values). |
| **Restore** | `restoreId` | One restore operation started by [Restore Workspace from Backup](#4-restore-workspace-from-backup). It has its **own ID**, which is not the `backupId`. |
| **Restore mode** | `restoreMode` | What to restore from the backup. Defaults to the backup's own mode. See [`restoreMode` Values](#restoremode-values). |
| **Restore status** | `status` of [Get Workspace Restore Status](#6-get-workspace-restore-status) | `INIT`, `SUCCESS`, `FAILURE`. See [Restore `status` Values](#restore-status-values). |

> **The single most important behaviour:** both [Backup Workspace Now](#2-backup-workspace-now) and [Restore Workspace from Backup](#4-restore-workspace-from-backup) are **asynchronous**. They return `200 OK` with `status: IN_PROGRESS` as soon as the work is queued, not when it is finished. A `200` from the restore API does **not** mean the workspace has been restored. Poll the matching status API until it leaves the in-progress state. See [Backup and Restore Lifecycle](#backup-and-restore-lifecycle).

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`). The read APIs use `ZohoAnalytics.metadata.read`; the two write APIs use `ZohoAnalytics.metadata.create` — see [Appendix B](#appendix-b--oauth-scope-summary).
> - All six APIs are **workspace-scoped** (`/restapi/v2/workspaces/<workspace-id>/...`) and require the `ZANALYTICS-ORGID` header.
> - `ZohoAnalytics_Server_URI` depends on the data centre (`analyticsapi.zoho.com`, `.eu`, etc.).
> - **All six APIs are disabled in Client Portal / White Label request contexts** and return `7301`.
> - **Only Account Admins and Organization Admins may call them.** Workspace Admins and custom-role users are refused with `7301` — see [Permission Model](#permission-model).
> - **The organisation's plan must include Backup.** Otherwise every API returns `6025`.
> - API-unit cost per call: [Get Workspace Backups](#1-get-workspace-backups) 1, [Backup Workspace Now](#2-backup-workspace-now) 5, [Download Workspace Backup](#3-download-workspace-backup) 1, [Restore Workspace from Backup](#4-restore-workspace-from-backup) 10, [Get Workspace Backup Status](#5-get-workspace-backup-status) 0.5, [Get Workspace Restore Status](#6-get-workspace-restore-status) 0.5.
> - None of these APIs accepts a `criteria` attribute. There is no search, filter, sort or paging parameter.

---

## Index

| # | API Name | Method | URL | API Units |
|---|----------|--------|-----|----------|
| 1 | [Get Workspace Backups](#1-get-workspace-backups) | GET | `/restapi/v2/workspaces/<workspace-id>/backups` | 1 |
| 2 | [Backup Workspace Now](#2-backup-workspace-now) | POST | `/restapi/v2/workspaces/<workspace-id>/backups` | 5 |
| 3 | [Download Workspace Backup](#3-download-workspace-backup) | GET | `/restapi/v2/workspaces/<workspace-id>/backups/<backup-id>/download` | 1 |
| 4 | [Restore Workspace from Backup](#4-restore-workspace-from-backup) | POST | `/restapi/v2/workspaces/<workspace-id>/backups/<backup-id>/restore` | 10 |
| 5 | [Get Workspace Backup Status](#5-get-workspace-backup-status) | GET | `/restapi/v2/workspaces/<workspace-id>/backups/<backup-id>/status` | 0.5 |
| 6 | [Get Workspace Restore Status](#6-get-workspace-restore-status) | GET | `/restapi/v2/workspaces/<workspace-id>/restores/<restore-id>/status` | 0.5 |

> **Note on method overloading:** the list and start APIs share one path and differ only by method. `GET` never starts anything; `POST` queues a backup immediately. There is no `PUT` or `DELETE` — backups cannot be deleted through the API.

---

## Backup and Restore Lifecycle

The two long-running operations follow the same pattern. Never treat the first response as the outcome.

| Step | Backup | Restore |
|------|--------|---------|
| 1. Start | [Backup Workspace Now](#2-backup-workspace-now) → `backupId`, `status: IN_PROGRESS` | [Restore Workspace from Backup](#4-restore-workspace-from-backup) → `restoreId`, `status: IN_PROGRESS` |
| 2. Poll | [Get Workspace Backup Status](#5-get-workspace-backup-status) with the `backupId` | [Get Workspace Restore Status](#6-get-workspace-restore-status) with the **`restoreId`** |
| 3. Finished when | `status` is `SUCCESS` (or `FAILED`) | `status` is `SUCCESS` (or `FAILURE`) |
| 4. Then | [Download Workspace Backup](#3-download-workspace-backup), or use the backup for a restore | Read the workspace as normal |

**IDs are not interchangeable.** The restore status URL takes the `restoreId` returned by the restore call. Passing a `backupId` there returns `8256`. Passing a `restoreId` to the backup status URL returns `8245`.

**A restore returns the workspace to the state captured in the backup.** The request needs `"confirmRestore": true` for that reason; without it nothing is queued (`8249`). A restore of a `STRUCTURE_AND_DATA` backup restores the workspace data as it was at backup time, so data loaded afterwards is not preserved. Take a fresh backup first if you may need to come back (note that only a small number of backups is kept — see [Limitations](#limitations)).

**Only one backup or restore runs per workspace at a time.** A second request while one is running is refused: `8257` (backup running), `8253` (restore running). Starting a backup is also refused while a connector sync is running (`8255`).

**Reading the backup list can retire old backups.** [Get Workspace Backups](#1-get-workspace-backups) marks backups beyond the newest three as `DELETED` as a side effect of the read. A backup that was restorable before the call can be gone afterwards. See [Limitations](#limitations).

**Restore pre-checks happen before the response.** The server downloads and validates the backup file while handling the restore request, so a `200` also means the file passed validation and the restore has been scheduled. A restore starts shortly afterwards (the scheduler delay defaults to 30 seconds) and the workspace is locked from the moment it is queued.

---

## Limitations

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
| **`CONFIG` length** | **5,000** characters for [Backup Workspace Now](#2-backup-workspace-now); **1,000** for [Restore Workspace from Backup](#4-restore-workspace-from-backup). | — |

> **Request-format limits are enforced before the request reaches the handler.** A malformed `CONFIG`, a non-boolean `confirmRestore`, or an over-long `CONFIG` is rejected at that layer, not by one of the codes in the Error Codes tables below.

---

## Permission Model

| Role | May do | Notes |
|------|--------|-------|
| Account Admin / Organization Admin | All six APIs. | Authorisation is evaluated against the organisation that owns the workspace in the URL. |
| Workspace Admin | Nothing in this document. | Refused with `7301`, even for a workspace they administer. |
| Custom role, any permission | Nothing in this document. | Refused with `7301`. |
| Any user on a Client Portal / White Label domain | Nothing in this document. | Refused with `7301`; the APIs are disabled on those domains. |

> Both write APIs need the `ZohoAnalytics.metadata.create` scope, even though a restore overwrites existing workspace state. A token without it cannot start a backup or a restore.

---

## 1. Get Workspace Backups

Returns the workspace's backup settings and the list of its retained backups. Supplies the `backupId` values used by every other API in this document.

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/backups` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the organisation that owns the workspace. |
| **Permission Required** | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. Workspace Admins and custom-role users are refused (`7301`). |
| **API Units** | 1 unit per request — gateway action `GET_WORKSPACE_BACKUPS` (api-id `3082`), **METADATA** unit category. |
| **Frequency Limit** | 60 requests/minute shared across every **METADATA**-category call of the organisation. |

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

### Sample Requests

**Case 1 — List the backups of a workspace**

```http
GET /restapi/v2/workspaces/137687000271334001/backups HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
GET /restapi/v2/workspaces/137687000271334001/backups HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Sample Responses

**HTTP 200 OK — Two backups, the newest still downloadable, no failed backup**

```json
{
    "status": "success",
    "summary": "Get workspace backups",
    "data": {
        "backupEnabled": true,
        "isInstantBackupInProgress": false,
        "isLastBackupFailed": false,
        "lastBackupFailedTime": "",
        "backups": [
            {
                "backupId": "137687000285490001",
                "createdDate": "14-Jun-2025",
                "createdDateWithTime": "14-Jun-2025 10:42:17 IST",
                "isLatestBackup": true,
                "version": 2,
                "backupMode": "STRUCTURE_AND_DATA",
                "isReadyToDownload": true,
                "isFailed": false
            },
            {
                "backupId": "137687000281450003",
                "createdDate": "07-Jun-2025",
                "createdDateWithTime": "07-Jun-2025 02:00:05 IST",
                "isLatestBackup": false,
                "version": 1,
                "backupMode": "STRUCTURE",
                "isReadyToDownload": true,
                "isFailed": false
            }
        ]
    }
}
```

**HTTP 200 OK — Workspace with no backup information**

```json
{
    "status": "success",
    "summary": "Get workspace backups",
    "data": {
        "backups": []
    }
}
```

**HTTP 403 Forbidden — Request sent through a Client Portal / White Label domain**

```json
{
    "status": "failure",
    "summary": "SECURITY_NOT_PERMITTED",
    "data": {
        "errorCode": 7301,
        "errorMessage": "You (WL_DBAdmin) do not have the permission to do this operation. "
    }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get workspace backups"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.backupEnabled` | Boolean | Whether backups are enabled for the workspace. **Absent** when the workspace has no backup information (see Notes). |
| `data.isInstantBackupInProgress` | Boolean | `true` while a backup started with [Backup Workspace Now](#2-backup-workspace-now) is running. Absent in the same case. |
| `data.isLastBackupFailed` | Boolean | `true` when the most recent backup attempt failed. Absent in the same case. |
| `data.lastBackupFailedTime` | String | Time of the last failed backup, or `""` when there is none. Absent in the same case. |
| `data.scheduleInfo` | JSONObject | The workspace's backup schedule. **Present only when a schedule exists.** Values are returned as stored and are not normalised; treat them as display values, not as an input to other APIs. |
| `data.scheduleInfo.nextScheduleTime` | String | When the next scheduled backup will run. |
| `data.scheduleInfo.periodicUnit` | String | Periodic unit of the schedule, where one is set. |
| `data.scheduleInfo.calendarFreq` | String | Calendar frequency of the schedule, where one is set. Note the key is `calendarFreq`, not `calendarFrequency`. |
| `data.scheduleInfo.calendarTime` | String | Time of day of a calendar schedule. |
| `data.scheduleInfo.calendarDay` | String | Day of the week of a calendar schedule. |
| `data.scheduleInfo.calendarDate` | String | Day of the month of a calendar schedule. |
| `data.backups` | JSONArray | The retained backups. **Always present**; `[]` when there are none. |
| `data.backups[].backupId` | String | Backup ID. Use it in the other `.../backups/<backup-id>/...` URLs. Returned as a string. |
| `data.backups[].createdDate` | String | Creation date, `dd-MMM-yyyy`, for example `14-Jun-2025`. |
| `data.backups[].createdDateWithTime` | String | Creation date and time, `dd-MMM-yyyy HH:mm:ss z`, in the workspace's display time zone. |
| `data.backups[].isLatestBackup` | Boolean | `true` for the most recently created backup. |
| `data.backups[].version` | Integer | Version number of the backup, as recorded when it was taken. |
| `data.backups[].backupMode` | String | `STRUCTURE_AND_DATA` or `STRUCTURE`. See [`backupMode` Values](#backupmode-values). |
| `data.backups[].isReadyToDownload` | Boolean | `true` only for a successfully completed backup that has a stored file. |
| `data.backups[].isFailed` | Boolean | `true` whenever `isReadyToDownload` is `false` — that is, for a failed backup **and** for any backup that has not completed successfully. It is not a precise failure flag; use [Get Workspace Backup Status](#5-get-workspace-backup-status) for the exact state. |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Read-only, with one side effect** | The read does not change settings, but when more than three backups are stored, the ones beyond the newest three are marked `DELETED` and are no longer listed. |
| **No sort, filter or paging** | The list is returned whole. The order of `backups` is not guaranteed — sort on `createdDateWithTime`, or use `isLatestBackup`, rather than relying on position. |
| **`isFailed` is not "failed"** | It is `true` for every entry that is not ready to download. Treat `isReadyToDownload: true` as the only reliable "usable" signal. |
| **No backup information** | A workspace with no backup information returns only `{"backups": []}`. The four workspace-level flags are **missing**, not `false`. Read them defensively. |
| **`scheduleInfo` is optional** | Absent when no schedule is configured. |
| **`backupId` is a string** | Keep it as a string; do not parse it as a 32-bit integer. |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Workspace Operations](WORKSPACE_OPERATIONS.md) → `<workspace-id>` → Get Workspace Backups → `backupId` for [Download Workspace Backup](#3-download-workspace-backup), [Restore Workspace from Backup](#4-restore-workspace-from-backup) and [Get Workspace Backup Status](#5-get-workspace-backup-status). |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 6025 | `BACKUP_NOT_ALLOWED` — The organisation's plan does not include Backup. | Upgrade the plan, or do not call the backup APIs for this organisation. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation that owns the workspace. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| 8084 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

---

## 2. Backup Workspace Now

Queues an immediate backup of the workspace. Returns at once with the new `backupId`; the backup itself runs in the background. Poll [Get Workspace Backup Status](#5-get-workspace-backup-status) until it finishes.

| Attribute | Value |
|-----------|-------|
| **Method** | POST |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/backups` |
| **OAuth Scope** | `ZohoAnalytics.metadata.create` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the organisation that owns the workspace. |
| **Permission Required** | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. Workspace Admins and custom-role users are refused (`7301`). |
| **API Units** | 5 units per request — gateway action `BACKUP_WORKSPACE_NOW` (api-id `3083`), **METADATA** unit category. |
| **Frequency Limit** | 60 requests/minute shared across every **METADATA**-category call of the organisation. |

### CONFIG Parameters

CONFIG is **optional** for this API. Omit it entirely, or send an empty body, to take a full `STRUCTURE_AND_DATA` backup.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `backupMode` | String | No | `STRUCTURE_AND_DATA` | What the backup contains. Up to 100 characters. See [`backupMode` Values](#backupmode-values). A value outside the list is refused with `8251`. |

### Sample Requests

**Case 1 — Full backup, no CONFIG**

```http
POST /restapi/v2/workspaces/137687000271334001/backups HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Structure-only backup**

```http
POST /restapi/v2/workspaces/137687000271334001/backups HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"backupMode":"STRUCTURE"}
```

### Sample Responses

**HTTP 200 OK — Backup queued**

```json
{
    "status": "success",
    "summary": "Backup workspace now",
    "data": {
        "backupId": "137687000285490001",
        "backupMode": "STRUCTURE_AND_DATA",
        "status": "IN_PROGRESS"
    }
}
```

**HTTP 400 Bad Request — A backup is already running**

```json
{
    "status": "failure",
    "summary": "BACKUP_ALREADY_IN_PROGRESS",
    "data": {
        "errorCode": 8257,
        "errorMessage": "A backup is already in progress for this workspace. Wait for it to complete before triggering another."
    }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Backup workspace now"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.backupId` | String | ID of the backup that was queued. Use it with [Get Workspace Backup Status](#5-get-workspace-backup-status). |
| `data.backupMode` | String | The mode of the backup that was queued: the value you sent, or the default. |
| `data.status` | String | Always `IN_PROGRESS` in a success response. It is the state at the time of queuing, not the outcome. |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Asynchronous** | `200` means the backup was queued. It does not mean it succeeded. Poll [Get Workspace Backup Status](#5-get-workspace-backup-status). |
| **Not idempotent** | Each accepted call creates a new backup. Repeating the call after a timeout can create a second one — check [Get Workspace Backups](#1-get-workspace-backups) (`isInstantBackupInProgress`) first. |
| **One backup at a time** | A running backup blocks another (`8257`), and a running restore blocks a backup (`8253`). |
| **Connector sync blocks it** | A running connector, custom connector or import sync on the workspace refuses the request (`8255`). Retry after the sync completes. |
| **Empty CONFIG is allowed** | An absent or empty `CONFIG` takes the defaults. A malformed one fails with `8080`. |
| **Retention** | Only the newest three backups are kept; see [Limitations](#limitations). A new backup can push the oldest out. |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Dependency chain** | [Workspace Operations](WORKSPACE_OPERATIONS.md) → `<workspace-id>` → Backup Workspace Now → `backupId` → [Get Workspace Backup Status](#5-get-workspace-backup-status) → [Download Workspace Backup](#3-download-workspace-backup) or [Restore Workspace from Backup](#4-restore-workspace-from-backup). |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 6025 | `BACKUP_NOT_ALLOWED` — The organisation's plan does not include Backup. | Upgrade the plan, or do not call the backup APIs for this organisation. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation that owns the workspace. |
| 8080 | `INVALID_JSON_CONFIGURATION` — `CONFIG` is present but is not valid JSON. | Send a valid JSON object, or omit `CONFIG`. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| 8084 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| 8251 | `INVALID_BACKUP_MODE` — `backupMode` is not an allowed value. | Use `STRUCTURE` or `STRUCTURE_AND_DATA`. |
| 8253 | `RESTORE_ALREADY_IN_PROGRESS` — A restore is running for this workspace. | Wait for the restore to finish ([Get Workspace Restore Status](#6-get-workspace-restore-status)), then retry. |
| 8255 | `CONNECTOR_SYNC_IN_PROGRESS` — A connector sync is running for this workspace. | Wait for the sync to complete, then retry. |
| 8257 | `BACKUP_ALREADY_IN_PROGRESS` — A backup is already running for this workspace. | Wait for it to complete ([Get Workspace Backup Status](#5-get-workspace-backup-status)), then retry if you still need another. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.create`. |

---

## 3. Download Workspace Backup

Downloads a completed backup as a `.wsbkp` file. The response is the **file itself**, not a JSON envelope.

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/backups/<backup-id>/download` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the organisation that owns the workspace. |
| **Permission Required** | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. Workspace Admins and custom-role users are refused (`7301`). |
| **API Units** | 1 unit per request — gateway action `DOWNLOAD_WORKSPACE_BACKUP` (api-id `3084`), **METADATA** unit category. |
| **Frequency Limit** | 60 requests/minute shared across every **METADATA**-category call of the organisation. |

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

### Sample Requests

**Case 1 — Download a backup**

```http
GET /restapi/v2/workspaces/137687000271334001/backups/137687000285490001/download HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Sample Responses

**HTTP 200 OK — The backup file is streamed as the response body**

```
HTTP/1.1 200 OK
Content-Type: application/x-zip-compressed
Content-Disposition: attachment;filename="Sales_Analysis_14_Jun_2025.wsbkp"
X-Download-Options: noopen

<binary .wsbkp content>
```

**HTTP 400 Bad Request — The backup has not completed**

```json
{
    "status": "failure",
    "summary": "BACKUP_NOT_READY",
    "data": {
        "errorCode": 8246,
        "errorMessage": "The backup is not yet completed and cannot be downloaded."
    }
}
```

### Response Fields

This API does not return a JSON payload on success. The body is the binary backup archive. Failures return the standard JSON failure envelope described in [Appendix D](#appendix-d--general-response-payload-notes).

| Header | Value | Description |
|--------|-------|-------------|
| `Content-Type` | `application/x-zip-compressed` | The archive is a zip-based `.wsbkp` file. |
| `Content-Disposition` | `attachment;filename="<name>.wsbkp"` | The name is `<workspace name>_<creation date, dd MMM yyyy>`, with spaces and special characters replaced by `_`. |
| `X-Download-Options` | `noopen` | Asks browsers to save the file, not open it. |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success has no JSON body** | Read the response as a byte stream, not as JSON. Branch on the HTTP status first; only a non-`200` response carries a JSON error. |
| **Only completed backups** | The backup must have status `SUCCESS` and a stored file. Anything else — in progress, failed, deleted, or of unknown state — returns `8246`. |
| **Backup must belong to the workspace** | A `backupId` that does not exist, or belongs to a different workspace, returns `8245`; the two cases are indistinguishable by design. |
| **No expiry check here** | Unlike restore, this API does not apply the restore window (`8248`). A backup stays downloadable while it is `SUCCESS` and its file is stored. |
| **Download is recorded** | The call is written to the workspace's activity log, and the backup's last-downloaded time is updated. A failure to record that time does not fail the download. |
| **Large files** | The archive can be large for `STRUCTURE_AND_DATA` backups. Stream to disk rather than buffering in memory. |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Dependency chain** | [Get Workspace Backups](#1-get-workspace-backups) or [Backup Workspace Now](#2-backup-workspace-now) → `backupId` → [Get Workspace Backup Status](#5-get-workspace-backup-status) (`SUCCESS`) → Download Workspace Backup. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 6025 | `BACKUP_NOT_ALLOWED` — The organisation's plan does not include Backup. | Upgrade the plan, or do not call the backup APIs for this organisation. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation that owns the workspace. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| 8084 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| 8245 | `BACKUP_NOT_FOUND` — The backup does not exist, or does not belong to this workspace. | Take the `backupId` from [Get Workspace Backups](#1-get-workspace-backups) for the same workspace. |
| 8246 | `BACKUP_NOT_READY` — The backup is not `SUCCESS`, or has no stored file. | Poll [Get Workspace Backup Status](#5-get-workspace-backup-status) until `SUCCESS`; a `FAILED` or `DELETED` backup cannot be downloaded. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

---

## 4. Restore Workspace from Backup

Queues a restore of the workspace from one of its own backups. Returns at once with a `restoreId`; the restore runs in the background. Poll [Get Workspace Restore Status](#6-get-workspace-restore-status) with the `restoreId`.

| Attribute | Value |
|-----------|-------|
| **Method** | POST |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/backups/<backup-id>/restore` |
| **OAuth Scope** | `ZohoAnalytics.metadata.create` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the organisation that owns the workspace. |
| **Permission Required** | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. Workspace Admins and custom-role users are refused (`7301`). |
| **API Units** | 10 units per request — gateway action `RESTORE_WORKSPACE_BACKUP` (api-id `3085`), **METADATA** unit category. |
| **Frequency Limit** | 60 requests/minute shared across every **METADATA**-category call of the organisation. |

### CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `confirmRestore` | Boolean | **Yes** | — | Must be `true`. Any other value, or omitting it, refuses the request with `8249` and queues nothing. |
| `restoreMode` | String | No | The backup's own mode | What to restore. Up to 100 characters. See [`restoreMode` Values](#restoremode-values). `STRUCTURE_AND_DATA` on a `STRUCTURE` backup is refused with `8254`. |

### Sample Requests

**Case 1 — Restore everything the backup holds**

```http
POST /restapi/v2/workspaces/137687000271334001/backups/137687000285490001/restore HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"confirmRestore":true}
```

**Case 2 — Restore only the structure from a full backup**

```http
POST /restapi/v2/workspaces/137687000271334001/backups/137687000285490001/restore HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"confirmRestore":true,"restoreMode":"STRUCTURE"}
```

### Sample Responses

**HTTP 200 OK — Restore queued**

```json
{
    "status": "success",
    "summary": "Restore workspace backup",
    "data": {
        "restoreId": "137687000286120001",
        "backupMode": "STRUCTURE_AND_DATA",
        "status": "IN_PROGRESS"
    }
}
```

**HTTP 400 Bad Request — Confirmation missing**

```json
{
    "status": "failure",
    "summary": "CONFIRM_RESTORE_REQUIRED",
    "data": {
        "errorCode": 8249,
        "errorMessage": "Restore requires explicit confirmation. Pass confirmRestore as true in the CONFIG to proceed."
    }
}
```

**HTTP 400 Bad Request — STRUCTURE_AND_DATA requested from a STRUCTURE-only backup**

```json
{
    "status": "failure",
    "summary": "INVALID_RESTORE_MODE_BACKUP",
    "data": {
        "errorCode": 8254,
        "errorMessage": "Invalid restore mode. STRUCTURE_AND_DATA restore is not allowed for a STRUCTURE-only backup."
    }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Restore workspace backup"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.restoreId` | String | ID of the restore that was queued. Pass it to [Get Workspace Restore Status](#6-get-workspace-restore-status). It is **not** the `backupId`. |
| `data.backupMode` | String | The mode that will be restored: the effective `restoreMode`, after the default is applied. |
| `data.status` | String | Always `IN_PROGRESS` in a success response. It is the state at the time of queuing, not the outcome. |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Asynchronous** | `200` means the restore was validated and scheduled. It does not mean the workspace has been restored. Poll [Get Workspace Restore Status](#6-get-workspace-restore-status). |
| **Replaces workspace state** | The workspace is returned to the state in the backup. Changes made after the backup was taken are not preserved. |
| **Confirmation is mandatory** | `confirmRestore` must be the JSON boolean `true`. There is no dry-run. |
| **Restore mode** | The default is the backup's own mode. `restoreMode: STRUCTURE` on a `STRUCTURE_AND_DATA` backup restores the structure only. `STRUCTURE_AND_DATA` on a `STRUCTURE` backup is refused (`8254`). Naming the backup's own mode explicitly changes nothing. |
| **Checks, in order** | Role (`7301`) → plan (`6025`) → confirmation (`8249`) → backup lookup (`8245`) → backup state (`8247`, `8246`) → restore window (`8248`) → running backup or restore (`8257`, `8253`) → backup file validation. |
| **Backup state** | A `DELETED` or `FAILED` backup returns `8247`. Every other state except `SUCCESS` — including `IN_PROGRESS`, `RETAINED` and `UNDO_BACKUP` — returns `8246`. |
| **Restore window** | A backup older than 30 days (default) returns `8248`. The same code is returned if the stored backup file has expired when the restore is scheduled. |
| **The request does real work** | The backup file is fetched and validated before the response is sent, so this call is slower than the other POST. Validation failures such as a connector or feature mismatch between the backup and the workspace are returned as errors; nothing is queued. |
| **Workspace is locked** | The workspace is locked from the moment the restore is queued. Do not make changes to it, and do not start a backup, until the restore reaches a final state. |
| **No connector-sync check** | Unlike [Backup Workspace Now](#2-backup-workspace-now), a restore is not refused because a connector sync is running. |
| **Not idempotent** | Repeating the call after a timeout can queue a second restore; a running restore blocks it with `8253`. Check [Get Workspace Restore Status](#6-get-workspace-restore-status) or retry only after a final state. |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Dependency chain** | [Get Workspace Backups](#1-get-workspace-backups) → `backupId` (`isReadyToDownload: true`) → Restore Workspace from Backup → `restoreId` → [Get Workspace Restore Status](#6-get-workspace-restore-status). |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 6025 | `BACKUP_NOT_ALLOWED` — The organisation's plan does not include Backup. | Upgrade the plan, or do not call the backup APIs for this organisation. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation that owns the workspace. |
| 8077 | `EMPTY_JSON_CONFIGURATION` — `CONFIG` is present but empty. | Send `CONFIG={"confirmRestore":true}`. |
| 8080 | `INVALID_JSON_CONFIGURATION` — `CONFIG` is present but is not valid JSON. | Send a valid JSON object. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| 8084 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| 8245 | `BACKUP_NOT_FOUND` — The backup does not exist, or does not belong to this workspace. | Take the `backupId` from [Get Workspace Backups](#1-get-workspace-backups) for the same workspace. |
| 8246 | `BACKUP_NOT_READY` — The backup is not in a state that can be restored (for example `IN_PROGRESS`). | Poll [Get Workspace Backup Status](#5-get-workspace-backup-status) until `SUCCESS`, then retry. |
| 8247 | `BACKUP_NOT_RESTORABLE` — The backup is `DELETED` or `FAILED`. | Choose a backup with `isReadyToDownload: true`, or take a new one. |
| 8248 | `BACKUP_EXPIRED` — The backup is older than the restore window, or its stored file has expired. | Take a new backup; an expired one cannot be restored. |
| 8249 | `CONFIRM_RESTORE_REQUIRED` — `confirmRestore` is not `true`. | Send `"confirmRestore": true` in `CONFIG`. |
| 8253 | `RESTORE_ALREADY_IN_PROGRESS` — A restore is running for this workspace. | Wait for it to finish ([Get Workspace Restore Status](#6-get-workspace-restore-status)), then retry if still needed. |
| 8254 | `INVALID_RESTORE_MODE_BACKUP` — `STRUCTURE_AND_DATA` was requested from a `STRUCTURE`-only backup. | Omit `restoreMode`, or send `STRUCTURE`. |
| 8257 | `BACKUP_ALREADY_IN_PROGRESS` — A backup is running for this workspace. | Wait for it to complete ([Get Workspace Backup Status](#5-get-workspace-backup-status)), then retry. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.create`. |
| 160810006 | `RESTORE_CONNECTOR_MISMATCH` — The connectors recorded in the backup do not match the workspace. | Align the workspace's connectors with the backup, or restore a different backup. |
| 160810010 | `RESTORE_SLIDESHOW_NOT_SUPPORTED` — The backup contains slideshow settings that are not supported in the workspace. | Restore a backup without those settings, or enable the feature for the organisation. |
| 160810011 | `RESTORE_PUBLISH_VIEW_NOT_SUPPORTED` — The backup contains published-view settings that are not supported in the workspace. | Restore a backup without those settings, or enable the feature for the organisation. |
| 160810012 | `RESTORE_PUBLISHED_SLIDESHOW_NOT_SUPPORTED` — The backup contains published-slideshow settings that are not supported in the workspace. | Restore a backup without those settings, or enable the feature for the organisation. |

---

## 5. Get Workspace Backup Status

Returns the current status of one backup. Use it to poll a backup started with [Backup Workspace Now](#2-backup-workspace-now), and to check a backup before downloading or restoring it.

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/backups/<backup-id>/status` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the organisation that owns the workspace. |
| **Permission Required** | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. Workspace Admins and custom-role users are refused (`7301`). |
| **API Units** | 0.5 units per request — gateway action `GET_WORKSPACE_BACKUP_STATUS` (api-id `3096`), **METADATA** unit category. |
| **Frequency Limit** | 60 requests/minute shared across every **METADATA**-category call of the organisation. |

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

### Sample Requests

**Case 1 — Poll a backup**

```http
GET /restapi/v2/workspaces/137687000271334001/backups/137687000285490001/status HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Sample Responses

**HTTP 200 OK — Backup completed**

```json
{
    "status": "success",
    "summary": "Get backup status",
    "data": {
        "backupId": "137687000285490001",
        "status": "SUCCESS",
        "backupMode": "STRUCTURE_AND_DATA"
    }
}
```

**HTTP 404 Not Found — Backup does not exist in this workspace**

```json
{
    "status": "failure",
    "summary": "BACKUP_NOT_FOUND",
    "data": {
        "errorCode": 8245,
        "errorMessage": "The specified backup was not found or does not belong to this workspace."
    }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get backup status"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.backupId` | String | The backup ID from the URL. |
| `data.status` | String | The backup's state. See [Backup `status` Values](#backup-status-values). Note this is a field inside `data`, separate from the top-level `status`. |
| `data.backupMode` | String | `STRUCTURE_AND_DATA` or `STRUCTURE`. See [`backupMode` Values](#backupmode-values). |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Read-only and idempotent** | Changes nothing. Cheap to poll (0.5 API unit). |
| **Polling** | Poll every few seconds and stop on any value other than `IN_PROGRESS`. A backup of a large workspace can take a while; there is no completion callback. |
| **Only `SUCCESS` is usable** | Download and restore both need `SUCCESS`. |
| **Wrong workspace or unknown ID** | Returns `8245`. A backup of another workspace is reported as not found. |
| **Unrecognised state** | A backup in a state the API does not recognise also returns `8245`. |
| **Two `status` fields** | The envelope's `status` (`success` / `failure`) and `data.status` are different things. Read `data.status` for progress. |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Dependency chain** | [Backup Workspace Now](#2-backup-workspace-now) or [Get Workspace Backups](#1-get-workspace-backups) → `backupId` → Get Workspace Backup Status → [Download Workspace Backup](#3-download-workspace-backup) or [Restore Workspace from Backup](#4-restore-workspace-from-backup). |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 6025 | `BACKUP_NOT_ALLOWED` — The organisation's plan does not include Backup. | Upgrade the plan, or do not call the backup APIs for this organisation. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation that owns the workspace. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| 8084 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| 8245 | `BACKUP_NOT_FOUND` — The backup does not exist, does not belong to this workspace, or is in an unrecognised state. | Take the `backupId` from [Get Workspace Backups](#1-get-workspace-backups) for the same workspace. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

---

## 6. Get Workspace Restore Status

Returns the current status of one restore. Use it to poll a restore started with [Restore Workspace from Backup](#4-restore-workspace-from-backup).

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/restores/<restore-id>/status` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the organisation that owns the workspace. |
| **Permission Required** | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. Workspace Admins and custom-role users are refused (`7301`). |
| **API Units** | 0.5 units per request — gateway action `GET_WORKSPACE_RESTORE_STATUS` (api-id `3097`), **METADATA** unit category. |
| **Frequency Limit** | 60 requests/minute shared across every **METADATA**-category call of the organisation. |

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

### Sample Requests

**Case 1 — Poll a restore**

```http
GET /restapi/v2/workspaces/137687000271334001/restores/137687000286120001/status HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Sample Responses

**HTTP 200 OK — Restore still running**

```json
{
    "status": "success",
    "summary": "Get restore status",
    "data": {
        "restoreId": "137687000286120001",
        "status": "INIT",
        "backupMode": "STRUCTURE_AND_DATA"
    }
}
```

**HTTP 404 Not Found — Restore does not exist in this workspace**

```json
{
    "status": "failure",
    "summary": "RESTORE_NOT_FOUND",
    "data": {
        "errorCode": 8256,
        "errorMessage": "Restore not found."
    }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get restore status"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.restoreId` | String | The restore ID from the URL. |
| `data.status` | String | The restore's state: `INIT`, `SUCCESS` or `FAILURE`. See [Restore `status` Values](#restore-status-values). |
| `data.backupMode` | String | The mode the restore applies: `STRUCTURE_AND_DATA` or `STRUCTURE`. |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Read-only and idempotent** | Changes nothing. Cheap to poll (0.5 API unit). |
| **`INIT` means running** | There is no `IN_PROGRESS` value here. Poll until `data.status` is `SUCCESS` or `FAILURE`. |
| **No failure detail** | A `FAILURE` is reported as a state only; this API does not return a reason. |
| **Use the `restoreId`** | The ID returned by [Restore Workspace from Backup](#4-restore-workspace-from-backup), not the `backupId`. |
| **Wrong workspace or unknown ID** | Returns `8256`. A restore of another workspace is reported as not found. |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Dependency chain** | [Restore Workspace from Backup](#4-restore-workspace-from-backup) → `restoreId` → Get Workspace Restore Status. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 6025 | `BACKUP_NOT_ALLOWED` — The organisation's plan does not include Backup. | Upgrade the plan, or do not call the backup APIs for this organisation. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation that owns the workspace. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| 8084 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| 8256 | `RESTORE_NOT_FOUND` — The restore does not exist, or does not belong to this workspace. | Use the `restoreId` returned by [Restore Workspace from Backup](#4-restore-workspace-from-backup) for the same workspace. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

---

## Appendix A – Common HTTP Headers

| Header | Value | Required | Description |
|--------|-------|----------|-------------|
| `Authorization` | `Zoho-oauthtoken <oauth-token>` | **Mandatory** | OAuth 2.0 access token of the calling user. Must carry the scope matching the operation (see [Appendix B](#appendix-b--oauth-scope-summary)). |
| `ZANALYTICS-ORGID` | Organization ID string | **Mandatory** | Organization ID of the organisation that owns the workspace. Obtainable from listing API responses as the `orgId` field. Missing → `8083`; unknown → `8084`. |
| `Content-Type` | `application/x-www-form-urlencoded` | Conditional | Required only when a CONFIG body is sent: [Restore Workspace from Backup](#4-restore-workspace-from-backup) always, [Backup Workspace Now](#2-backup-workspace-now) when `backupMode` is set. The GET APIs send no payload. |
| `Host` | `analyticsapi.zoho.com` (or the DC equivalent) | **Mandatory** | Requests sent through a Client Portal / White Label domain are rejected with `7301`. |

> **`ZANALYTICS-DEST-ORGID` is not used by any API in this document.**

Example:

```http
POST /restapi/v2/workspaces/137687000271334001/backups/137687000285490001/restore HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"confirmRestore":true}
```

---

## Appendix B – OAuth Scope Summary

| API | HTTP Method | Scope |
|-----|-------------|-------|
| Get Workspace Backups | GET | `ZohoAnalytics.metadata.read` |
| Backup Workspace Now | POST | `ZohoAnalytics.metadata.create` |
| Download Workspace Backup | GET | `ZohoAnalytics.metadata.read` |
| Restore Workspace from Backup | POST | `ZohoAnalytics.metadata.create` |
| Get Workspace Backup Status | GET | `ZohoAnalytics.metadata.read` |
| Get Workspace Restore Status | GET | `ZohoAnalytics.metadata.read` |

> All six APIs use the `metadata` scope group. The two write APIs need `create`, not `update`. A token that holds only `ZohoAnalytics.metadata.read` can list, poll and download backups but cannot start a backup or a restore; an integration that does both needs both scopes at consent time.

---

## Appendix C – API-Specific Notes and Behaviours

### Get Workspace Backups

- **Use `isReadyToDownload`, not `isFailed`, to choose a usable backup.** `isFailed` is `true` for anything not ready.
- **Read the workspace-level flags defensively.** They are absent when the workspace has no backup information.
- **The read can retire old backups.** Backups beyond the newest three are marked `DELETED`.
- **Dependency chain:** [Workspace Operations](WORKSPACE_OPERATIONS.md) → `<workspace-id>` → Get Workspace Backups.

### Backup Workspace Now

- **Treat `200` as "queued".** Poll [Get Workspace Backup Status](#5-get-workspace-backup-status).
- **Check before retrying.** The call is not idempotent; a retry can create a second backup.
- **Dependency chain:** [Workspace Operations](WORKSPACE_OPERATIONS.md) → `<workspace-id>` → Backup Workspace Now → `backupId` → Get Workspace Backup Status.

### Download Workspace Backup

- **Branch on the HTTP status before parsing.** Success is a file, failure is JSON.
- **Only `SUCCESS` backups download.** Every other state returns `8246`.
- **Dependency chain:** [Get Workspace Backup Status](#5-get-workspace-backup-status) → Download Workspace Backup.

### Restore Workspace from Backup

- **This changes the workspace.** `confirmRestore: true` is required, and the workspace is locked while the restore runs.
- **Keep the `restoreId`.** It, and not the `backupId`, identifies the operation for polling.
- **Choose the backup first.** Check `isReadyToDownload`, creation date (30-day window) and `backupMode` before calling.
- **Dependency chain:** [Get Workspace Backups](#1-get-workspace-backups) → Restore Workspace from Backup → `restoreId` → [Get Workspace Restore Status](#6-get-workspace-restore-status).

### Get Workspace Backup Status

- **Stop polling on any value other than `IN_PROGRESS`.**
- **Dependency chain:** [Backup Workspace Now](#2-backup-workspace-now) → Get Workspace Backup Status.

### Get Workspace Restore Status

- **`INIT` is the running state.** Stop on `SUCCESS` or `FAILURE`.
- **Dependency chain:** [Restore Workspace from Backup](#4-restore-workspace-from-backup) → Get Workspace Restore Status.

---

## Appendix D – General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Which endpoints return which body** | All APIs return `200 OK`. Five return the JSON envelope `{"status", "summary", "data"}`; [Download Workspace Backup](#3-download-workspace-backup) returns the binary file with no envelope. |
| **Failure responses always carry a JSON body** | Including for the download API. `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name, not a localised sentence. |
| **IDs are strings** | `backupId` and `restoreId` are returned as JSON strings. |
| **Two `status` fields** | The envelope's `status` is `success` or `failure`. `data.status` on the polling and start APIs is the progress state. |
| **Start APIs return the initial state only** | `data.status` is `IN_PROGRESS` on the two POST APIs, whatever happens later. |
| **List response can be minimal** | [Get Workspace Backups](#1-get-workspace-backups) returns only `backups: []` for a workspace with no backup information. |
| **Key order is not guaranteed** | Read by name, not position. |
| **Responses are extensible** | Some builds return additional fields. Ignore unrecognised keys rather than validating against a closed schema. |

---

## Appendix E – Enum and Value Reference

#### `backupMode` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `STRUCTURE_AND_DATA` | The backup holds the workspace structure and its data. | Default for [Backup Workspace Now](#2-backup-workspace-now). |
| `STRUCTURE` | The backup holds the structure only; no data. | Cannot be restored with `restoreMode: STRUCTURE_AND_DATA` (`8254`). |

#### `restoreMode` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `STRUCTURE_AND_DATA` | Restore the structure and the data. | Only for a `STRUCTURE_AND_DATA` backup; refused for a `STRUCTURE` backup (`8254`). |
| `STRUCTURE` | Restore the structure only. | Allowed for either kind of backup. |

> Omit `restoreMode` to use the backup's own mode.

#### Backup `status` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `IN_PROGRESS` | The backup is being created. | Cannot be downloaded or restored (`8246`). |
| `SUCCESS` | The backup completed. | The only state that can be downloaded or restored. |
| `DELETED` | The backup was retired, for example by the three-backup retention. | Cannot be downloaded (`8246`) or restored (`8247`). |
| `FAILED` | The backup failed. | Cannot be downloaded (`8246`) or restored (`8247`). |
| `RETAINED` | Internal state. | Cannot be downloaded or restored through this API (`8246`). |
| `UNDO_BACKUP` | Internal state. | Cannot be downloaded or restored through this API (`8246`). |

#### Restore `status` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `INIT` | The restore is queued or running. | Response only. Keep polling. |
| `SUCCESS` | The restore completed. | Response only. Final. |
| `FAILURE` | The restore failed. | Response only. Final. |

---

## Appendix F – CONFIG Attribute Availability by API

| Attribute | Backup Workspace Now | Restore Workspace from Backup |
|-----------|---|---|
| `backupMode` | ✔ | — |
| `confirmRestore` | — | ✔ |
| `restoreMode` | — | ✔ |

> The other four APIs take no CONFIG.

---

## Appendix G – API Units and Frequency Limits

Every call deducts **API units** from the organisation's plan allowance and is counted against a **per-minute request ceiling** shared by all APIs in the same unit category. Both are keyed off the internal gateway action (`api-id`) that the request method and URL resolve to.

| # | API Name | Gateway Action (api-id) | Unit Category | Units | Charged |
|---|----------|-------------------------|---------------|-------|---------|
| 1 | [Get Workspace Backups](#1-get-workspace-backups) | `GET_WORKSPACE_BACKUPS` (3082) | METADATA | 1 | per request |
| 2 | [Backup Workspace Now](#2-backup-workspace-now) | `BACKUP_WORKSPACE_NOW` (3083) | METADATA | 5 | per request |
| 3 | [Download Workspace Backup](#3-download-workspace-backup) | `DOWNLOAD_WORKSPACE_BACKUP` (3084) | METADATA | 1 | per request |
| 4 | [Restore Workspace from Backup](#4-restore-workspace-from-backup) | `RESTORE_WORKSPACE_BACKUP` (3085) | METADATA | 10 | per request |
| 5 | [Get Workspace Backup Status](#5-get-workspace-backup-status) | `GET_WORKSPACE_BACKUP_STATUS` (3096) | METADATA | 0.5 | per request |
| 6 | [Get Workspace Restore Status](#6-get-workspace-restore-status) | `GET_WORKSPACE_RESTORE_STATUS` (3097) | METADATA | 0.5 | per request |

### How the cost is computed

```
units charged = (rows processed / rows basis) * configured units      # row-based APIs
units charged = configured units                                      # everything else
```

Row-based costs are not rounded up to a whole block — processing 250 rows at a rate of 3 units per 1000 rows costs `0.75` units. Units are charged on the rows **actually processed**, after the operation runs, so a partially completed import is still charged for the rows it wrote.

### Frequency limits

| Unit category | Requests per minute | Used by this document |
|---------------|---------------------|-----------------------|
| `DML` | 100 | — |
| `BULK` | 40 | — |
| `METADATA` | 60 | Yes |

The ceiling is per organisation, shared by every API in that category, and is scaled by a plan-specific multiplier — the figures above are the base configuration. Exceeding it fails the request with an API-frequency error, which is independent of running out of units.

The current allocation, usage and remainder of API units for the organisation are returned by the **Get Resource Details** API under `resourceName: "apiUnits"`. Fractional usage is normal. The complete cross-document table is in [API Units and Rate Limits](../API_UNITS_AND_RATE_LIMITS.md).
