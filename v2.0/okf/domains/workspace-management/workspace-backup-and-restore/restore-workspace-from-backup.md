---
type: API Endpoint
title: Restore Workspace from Backup
description: Queues a restore of the workspace from one of its own backups.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/restore"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-backup-and-restore
  - post
  - metadata
api:
  operation_id: restoreWorkspaceFromBackup
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/restore"
  domain: workspace-management
  group: workspace-backup-and-restore
  oauth_scopes:
    - ZohoAnalytics.metadata.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. Workspace Admins and custom-role users are refused (7301).
  error_codes:
    - 6025
    - 7301
    - 8077
    - 8080
    - 8083
    - 8084
    - 8245
    - 8246
    - 8247
    - 8248
    - 8249
    - 8253
    - 8254
    - 8257
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1backups~1{backup-id}~1restore/post"
    config_schema: RestoreWorkspaceFromBackupConfig
    response_schema: RestoreWorkspaceFromBackupResponse
  sdk_examples: "/sdk-examples/workspace-management/workspace-backup-and-restore/restore-workspace-from-backup.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T11:33:37Z
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/restore`** - Restore Workspace from Backup (Workspace Backup & Restore / Workspace Management).

Queues a restore of the workspace from one of its own backups. Returns at once with a `restoreId`; the restore runs in the background. Poll [Get Workspace Restore Status](get-workspace-restore-status.md) with the `restoreId`.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `restoreWorkspaceFromBackup` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/restore` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadatacreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the organisation that owns the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. Workspace Admins and custom-role users are refused (7301). See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1backups~1{backup-id}~1restore/post`; CONFIG schema `RestoreWorkspaceFromBackupConfig`; response schema `RestoreWorkspaceFromBackupResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID, shown in the Zoho Analytics UI under Settings > Organisation. See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | The ID of the workspace. It can be obtained using any of the workspace list APIs. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{backup-id}` | string | ID of the backup. | [How to obtain](../../../foundations/identifiers.md#backup-id) |

## CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `confirmRestore` | Boolean | **Yes** | — | Must be `true`. Any other value, or omitting it, refuses the request with `8249` and queues nothing. |
| `restoreMode` | String | No | The backup's own mode | What to restore. Up to 100 characters. See [`restoreMode` Values](overview.md#restoremode-values). `STRUCTURE_AND_DATA` on a `STRUCTURE` backup is refused with `8254`. |

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Restore workspace backup"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.restoreId` | String | ID of the restore that was queued. Pass it to [Get Workspace Restore Status](get-workspace-restore-status.md). It is **not** the `backupId`. |
| `data.backupMode` | String | The mode that will be restored: the effective `restoreMode`, after the default is applied. |
| `data.status` | String | Always `IN_PROGRESS` in a success response. It is the state at the time of queuing, not the outcome. |

# Examples

## Sample Requests

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

## Sample Responses

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

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Restore Workspace from Backup](../../../sdk-examples/workspace-management/workspace-backup-and-restore/restore-workspace-from-backup.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Asynchronous** | `200` means the restore was validated and scheduled. It does not mean the workspace has been restored. Poll [Get Workspace Restore Status](get-workspace-restore-status.md). |
| **Replaces workspace state** | The workspace is returned to the state in the backup. Changes made after the backup was taken are not preserved. |
| **Confirmation is mandatory** | `confirmRestore` must be the JSON boolean `true`. There is no dry-run. |
| **Restore mode** | The default is the backup's own mode. `restoreMode: STRUCTURE` on a `STRUCTURE_AND_DATA` backup restores the structure only. `STRUCTURE_AND_DATA` on a `STRUCTURE` backup is refused (`8254`). Naming the backup's own mode explicitly changes nothing. |
| **Checks, in order** | Role (`7301`) → plan (`6025`) → confirmation (`8249`) → backup lookup (`8245`) → backup state (`8247`, `8246`) → restore window (`8248`) → running backup or restore (`8257`, `8253`) → backup file validation. |
| **Backup state** | A `DELETED` or `FAILED` backup returns `8247`. Every other state except `SUCCESS` — including `IN_PROGRESS`, `RETAINED` and `UNDO_BACKUP` — returns `8246`. |
| **Restore window** | A backup older than 30 days (default) returns `8248`. The same code is returned if the stored backup file has expired when the restore is scheduled. |
| **The request does real work** | The backup file is fetched and validated before the response is sent, so this call is slower than the other POST. Validation failures such as a connector or feature mismatch between the backup and the workspace are returned as errors; nothing is queued. |
| **Workspace is locked** | The workspace is locked from the moment the restore is queued. Do not make changes to it, and do not start a backup, until the restore reaches a final state. |
| **No connector-sync check** | Unlike [Backup Workspace Now](backup-workspace-now.md), a restore is not refused because a connector sync is running. |
| **Not idempotent** | Repeating the call after a timeout can queue a second restore; a running restore blocks it with `8253`. Check [Get Workspace Restore Status](get-workspace-restore-status.md) or retry only after a final state. |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Dependency chain** | [Get Workspace Backups](get-workspace-backups.md) → `backupId` (`isReadyToDownload: true`) → Restore Workspace from Backup → `restoreId` → [Get Workspace Restore Status](get-workspace-restore-status.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6025](../../../foundations/error-codes.md#error-6025) | 400 | `BACKUP_NOT_ALLOWED` — The organisation's plan does not include Backup. | Upgrade the plan, or do not call the backup APIs for this organisation. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation that owns the workspace. |
| [8077](../../../foundations/error-codes.md#error-8077) | 400 | `EMPTY_JSON_CONFIGURATION` — `CONFIG` is present but empty. | Send `CONFIG={"confirmRestore":true}`. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — `CONFIG` is present but is not valid JSON. | Send a valid JSON object. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| [8084](../../../foundations/error-codes.md#error-8084) | 404 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| [8245](../../../foundations/error-codes.md#error-8245) | 404 | `BACKUP_NOT_FOUND` — The backup does not exist, or does not belong to this workspace. | Take the `backupId` from [Get Workspace Backups](get-workspace-backups.md) for the same workspace. |
| [8246](../../../foundations/error-codes.md#error-8246) | 400 | `BACKUP_NOT_READY` — The backup is not in a state that can be restored (for example `IN_PROGRESS`). | Poll [Get Workspace Backup Status](get-workspace-backup-status.md) until `SUCCESS`, then retry. |
| [8247](../../../foundations/error-codes.md#error-8247) | 400 | `BACKUP_NOT_RESTORABLE` — The backup is `DELETED` or `FAILED`. | Choose a backup with `isReadyToDownload: true`, or take a new one. |
| [8248](../../../foundations/error-codes.md#error-8248) | 400 | `BACKUP_EXPIRED` — The backup is older than the restore window, or its stored file has expired. | Take a new backup; an expired one cannot be restored. |
| [8249](../../../foundations/error-codes.md#error-8249) | 400 | `CONFIRM_RESTORE_REQUIRED` — `confirmRestore` is not `true`. | Send `"confirmRestore": true` in `CONFIG`. |
| [8253](../../../foundations/error-codes.md#error-8253) | 400 | `RESTORE_ALREADY_IN_PROGRESS` — A restore is running for this workspace. | Wait for it to finish ([Get Workspace Restore Status](get-workspace-restore-status.md)), then retry if still needed. |
| [8254](../../../foundations/error-codes.md#error-8254) | 400 | `INVALID_RESTORE_MODE_BACKUP` — `STRUCTURE_AND_DATA` was requested from a `STRUCTURE`-only backup. | Omit `restoreMode`, or send `STRUCTURE`. |
| [8257](../../../foundations/error-codes.md#error-8257) | 400 | `BACKUP_ALREADY_IN_PROGRESS` — A backup is running for this workspace. | Wait for it to complete ([Get Workspace Backup Status](get-workspace-backup-status.md)), then retry. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.create`. |

# Related

- [Workspace Backup & Restore overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Workspace Backups](get-workspace-backups.md), [Backup Workspace Now](backup-workspace-now.md), [Download Workspace Backup](download-workspace-backup.md), [Get Workspace Backup Status](get-workspace-backup-status.md), [Get Workspace Restore Status](get-workspace-restore-status.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-backup-and-restore/restore-workspace-from-backup.md).
