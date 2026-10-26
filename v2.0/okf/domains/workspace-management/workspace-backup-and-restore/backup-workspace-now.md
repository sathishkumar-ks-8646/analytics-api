---
type: API Endpoint
title: Backup Workspace Now
description: Queues an immediate backup of the workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/backups"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-backup-and-restore
  - post
  - metadata
api:
  operation_id: backupWorkspaceNow
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/backups"
  domain: workspace-management
  group: workspace-backup-and-restore
  oauth_scopes:
    - ZohoAnalytics.metadata.create
  org_id_header: required
  config_parameter:
    location: form
    required: false
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. Workspace Admins and custom-role users are refused (7301).
  error_codes:
    - 6025
    - 7301
    - 8080
    - 8083
    - 8084
    - 8251
    - 8253
    - 8255
    - 8257
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1backups/post"
    config_schema: BackupWorkspaceNowConfig
    response_schema: BackupWorkspaceNowResponse
  sdk_examples: "/sdk-examples/workspace-management/workspace-backup-and-restore/backup-workspace-now.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/backups`** - Backup Workspace Now (Workspace Backup & Restore / Workspace Management).

Queues an immediate backup of the workspace. Returns at once with the new `backupId`; the backup itself runs in the background. Poll [Get Workspace Backup Status](get-workspace-backup-status.md) until it finishes.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `backupWorkspaceNow` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/backups` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadatacreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the organisation that owns the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. Workspace Admins and custom-role users are refused (7301). See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - optional |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1backups/post`; CONFIG schema `BackupWorkspaceNowConfig`; response schema `BackupWorkspaceNowResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | The ID of the workspace. It can be obtained using any of the workspace list APIs. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

CONFIG is **optional** for this API. Omit it entirely, or send an empty body, to take a full `STRUCTURE_AND_DATA` backup.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `backupMode` | String | No | `STRUCTURE_AND_DATA` | What the backup contains. Up to 100 characters. See [`backupMode` Values](overview.md#backupmode-values). A value outside the list is refused with `8251`. |

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Backup workspace now"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.backupId` | String | ID of the backup that was queued. Use it with [Get Workspace Backup Status](get-workspace-backup-status.md). |
| `data.backupMode` | String | The mode of the backup that was queued: the value you sent, or the default. |
| `data.status` | String | Always `IN_PROGRESS` in a success response. It is the state at the time of queuing, not the outcome. |

# Examples

## Sample Requests

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

## Sample Responses

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

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Backup Workspace Now](../../../sdk-examples/workspace-management/workspace-backup-and-restore/backup-workspace-now.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Asynchronous** | `200` means the backup was queued. It does not mean it succeeded. Poll [Get Workspace Backup Status](get-workspace-backup-status.md). |
| **Not idempotent** | Each accepted call creates a new backup. Repeating the call after a timeout can create a second one — check [Get Workspace Backups](get-workspace-backups.md) (`isInstantBackupInProgress`) first. |
| **One backup at a time** | A running backup blocks another (`8257`), and a running restore blocks a backup (`8253`). |
| **Connector sync blocks it** | A running connector, custom connector or import sync on the workspace refuses the request (`8255`). Retry after the sync completes. |
| **Empty CONFIG is allowed** | An absent or empty `CONFIG` takes the defaults. A malformed one fails with `8080`. |
| **Retention** | Only the newest three backups are kept; see [Limitations](overview.md#limitations). A new backup can push the oldest out. |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Dependency chain** | [Workspace Operations](../workspace-operations/overview.md) → `<workspace-id>` → Backup Workspace Now → `backupId` → [Get Workspace Backup Status](get-workspace-backup-status.md) → [Download Workspace Backup](download-workspace-backup.md) or [Restore Workspace from Backup](restore-workspace-from-backup.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6025](../../../foundations/error-codes.md#error-6025) | 400 | `BACKUP_NOT_ALLOWED` — The organisation's plan does not include Backup. | Upgrade the plan, or do not call the backup APIs for this organisation. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation that owns the workspace. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — `CONFIG` is present but is not valid JSON. | Send a valid JSON object, or omit `CONFIG`. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| [8084](../../../foundations/error-codes.md#error-8084) | 400 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| [8251](../../../foundations/error-codes.md#error-8251) | 400 | `INVALID_BACKUP_MODE` — `backupMode` is not an allowed value. | Use `STRUCTURE` or `STRUCTURE_AND_DATA`. |
| [8253](../../../foundations/error-codes.md#error-8253) | 400 | `RESTORE_ALREADY_IN_PROGRESS` — A restore is running for this workspace. | Wait for the restore to finish ([Get Workspace Restore Status](get-workspace-restore-status.md)), then retry. |
| [8255](../../../foundations/error-codes.md#error-8255) | 400 | `CONNECTOR_SYNC_IN_PROGRESS` — A connector sync is running for this workspace. | Wait for the sync to complete, then retry. |
| [8257](../../../foundations/error-codes.md#error-8257) | 400 | `BACKUP_ALREADY_IN_PROGRESS` — A backup is already running for this workspace. | Wait for it to complete ([Get Workspace Backup Status](get-workspace-backup-status.md)), then retry if you still need another. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.create`. |

# Related

- [Workspace Backup & Restore overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Workspace Backups](get-workspace-backups.md), [Download Workspace Backup](download-workspace-backup.md), [Restore Workspace from Backup](restore-workspace-from-backup.md), [Get Workspace Backup Status](get-workspace-backup-status.md), [Get Workspace Restore Status](get-workspace-restore-status.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-backup-and-restore/backup-workspace-now.md).
