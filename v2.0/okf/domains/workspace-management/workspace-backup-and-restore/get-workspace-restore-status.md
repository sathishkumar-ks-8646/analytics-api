---
type: API Endpoint
title: Get Workspace Restore Status
description: Returns the current status of one restore.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/restores/{restore-id}/status"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-backup-and-restore
  - get
  - metadata
api:
  operation_id: getWorkspaceRestoreStatus
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/restores/{restore-id}/status"
  domain: workspace-management
  group: workspace-backup-and-restore
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
    - 8256
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1restores~1{restore-id}~1status/get"
    config_schema: null
    response_schema: GetWorkspaceRestoreStatusResponse
  sdk_examples: "/sdk-examples/workspace-management/workspace-backup-and-restore/get-workspace-restore-status.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/restores/{restore-id}/status`** - Get Workspace Restore Status (Workspace Backup & Restore / Workspace Management).

Returns the current status of one restore. Use it to poll a restore started with [Restore Workspace from Backup](restore-workspace-from-backup.md).

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getWorkspaceRestoreStatus` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/restores/{restore-id}/status` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the organisation that owns the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. Workspace Admins and custom-role users are refused (7301). See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1restores~1{restore-id}~1status/get`; response schema `GetWorkspaceRestoreStatusResponse` |

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
| `{restore-id}` | string | ID of the restore. | [How to obtain](../../../foundations/identifiers.md#restore-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get restore status"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.restoreId` | String | The restore ID from the URL. |
| `data.status` | String | The restore's state: `INIT`, `SUCCESS` or `FAILURE`. See [Restore `status` Values](overview.md#restore-status-values). |
| `data.backupMode` | String | The mode the restore applies: `STRUCTURE_AND_DATA` or `STRUCTURE`. |

# Examples

## Sample Requests

**Case 1 — Poll a restore**

```http
GET /restapi/v2/workspaces/137687000271334001/restores/137687000286120001/status HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

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

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Workspace Restore Status](../../../sdk-examples/workspace-management/workspace-backup-and-restore/get-workspace-restore-status.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Read-only and idempotent** | Changes nothing. Cheap to poll (0.5 API unit). |
| **`INIT` means running** | There is no `IN_PROGRESS` value here. Poll until `data.status` is `SUCCESS` or `FAILURE`. |
| **No failure detail** | A `FAILURE` is reported as a state only; this API does not return a reason. |
| **Use the `restoreId`** | The ID returned by [Restore Workspace from Backup](restore-workspace-from-backup.md), not the `backupId`. |
| **Wrong workspace or unknown ID** | Returns `8256`. A restore of another workspace is reported as not found. |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Dependency chain** | [Restore Workspace from Backup](restore-workspace-from-backup.md) → `restoreId` → Get Workspace Restore Status. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6025](../../../foundations/error-codes.md#error-6025) | 400 | `BACKUP_NOT_ALLOWED` — The organisation's plan does not include Backup. | Upgrade the plan, or do not call the backup APIs for this organisation. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation that owns the workspace. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| [8084](../../../foundations/error-codes.md#error-8084) | 404 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| [8256](../../../foundations/error-codes.md#error-8256) | 404 | `RESTORE_NOT_FOUND` — The restore does not exist, or does not belong to this workspace. | Use the `restoreId` returned by [Restore Workspace from Backup](restore-workspace-from-backup.md) for the same workspace. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Workspace Backup & Restore overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Workspace Backups](get-workspace-backups.md), [Backup Workspace Now](backup-workspace-now.md), [Download Workspace Backup](download-workspace-backup.md), [Restore Workspace from Backup](restore-workspace-from-backup.md), [Get Workspace Backup Status](get-workspace-backup-status.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-backup-and-restore/get-workspace-restore-status.md).
