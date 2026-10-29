---
type: API Endpoint
title: Get Workspace Backups
description: "Returns the workspace's backup settings and the list of its retained backups."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/backups"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-backup-and-restore
  - get
  - metadata
api:
  operation_id: getWorkspaceBackups
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/backups"
  domain: workspace-management
  group: workspace-backup-and-restore
  api_units:
    api_id: 3082
    action: GET_WORKSPACE_BACKUPS
    category: METADATA
    units: 1
    units_basis: per_request
    units_note: "1 unit per request"
    category_frequency_limit: 60 requests/minute
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. Workspace Admins and custom-role users are refused (7301).
  error_codes:
    - 6025
    - 7301
    - 8083
    - 8084
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1backups/get"
    config_schema: null
    response_schema: GetWorkspaceBackupsResponse
  sdk_examples: "/sdk-examples/workspace-management/workspace-backup-and-restore/get-workspace-backups.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/backups`** - Get Workspace Backups (Workspace Backup & Restore / Workspace Management).

Returns the workspace's backup settings and the list of its retained backups. Supplies the `backupId` values used by every other API in this document.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getWorkspaceBackups` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/backups` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the organisation that owns the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. Workspace Admins and custom-role users are refused (7301). See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| API units | 1 unit per request - action `GET_WORKSPACE_BACKUPS` (api-id `3082`), **METADATA** category. See [API units](../../../foundations/api-units.md). |
| Frequency limit | 60 requests/minute across all **METADATA**-category calls of the organization. See [API units](../../../foundations/api-units.md#unit-categories-and-frequency-limits). |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1backups/get`; response schema `GetWorkspaceBackupsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID, shown in the Zoho Analytics UI under Settings > Organisation. See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | The ID of the workspace. It can be obtained using any of the workspace list APIs. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get workspace backups"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.backupEnabled` | Boolean | Whether backups are enabled for the workspace. **Absent** when the workspace has no backup information (see Notes). |
| `data.isInstantBackupInProgress` | Boolean | `true` while a backup started with [Backup Workspace Now](backup-workspace-now.md) is running. Absent in the same case. |
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
| `data.backups[].backupMode` | String | `STRUCTURE_AND_DATA` or `STRUCTURE`. See [`backupMode` Values](overview.md#backupmode-values). |
| `data.backups[].isReadyToDownload` | Boolean | `true` only for a successfully completed backup that has a stored file. |
| `data.backups[].isFailed` | Boolean | `true` whenever `isReadyToDownload` is `false` — that is, for a failed backup **and** for any backup that has not completed successfully. It is not a precise failure flag; use [Get Workspace Backup Status](get-workspace-backup-status.md) for the exact state. |

# Examples

## Sample Requests

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

## Sample Responses

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

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Workspace Backups](../../../sdk-examples/workspace-management/workspace-backup-and-restore/get-workspace-backups.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

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
| **Dependency chain** | [Workspace Operations](../workspace-operations/overview.md) → `<workspace-id>` → Get Workspace Backups → `backupId` for [Download Workspace Backup](download-workspace-backup.md), [Restore Workspace from Backup](restore-workspace-from-backup.md) and [Get Workspace Backup Status](get-workspace-backup-status.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6025](../../../foundations/error-codes.md#error-6025) | 400 | `BACKUP_NOT_ALLOWED` — The organisation's plan does not include Backup. | Upgrade the plan, or do not call the backup APIs for this organisation. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation that owns the workspace. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| [8084](../../../foundations/error-codes.md#error-8084) | 404 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Workspace Backup & Restore overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Backup Workspace Now](backup-workspace-now.md), [Download Workspace Backup](download-workspace-backup.md), [Restore Workspace from Backup](restore-workspace-from-backup.md), [Get Workspace Backup Status](get-workspace-backup-status.md), [Get Workspace Restore Status](get-workspace-restore-status.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-backup-and-restore/get-workspace-backups.md).
- [API units](../../../foundations/api-units.md) - unit cost, unit categories and frequency limits for every endpoint.
