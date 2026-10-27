---
type: API Endpoint
title: Download Workspace Backup
description: Downloads a completed backup as a .wsbkp file.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/download"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-backup-and-restore
  - get
  - metadata
api:
  operation_id: downloadWorkspaceBackup
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/download"
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
    - application/x-zip-compressed
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. Workspace Admins and custom-role users are refused (7301).
  error_codes:
    - 6025
    - 7301
    - 8083
    - 8084
    - 8245
    - 8246
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1backups~1{backup-id}~1download/get"
    config_schema: null
    response_schema: null
  sdk_examples: "/sdk-examples/workspace-management/workspace-backup-and-restore/download-workspace-backup.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/download`** - Download Workspace Backup (Workspace Backup & Restore / Workspace Management).

Downloads a completed backup as a `.wsbkp` file. The response is the **file itself**, not a JSON envelope.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `downloadWorkspaceBackup` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/download` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the organisation that owns the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. Workspace Admins and custom-role users are refused (7301). See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/x-zip-compressed` |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1backups~1{backup-id}~1download/get` |

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
| `{backup-id}` | string | ID of the backup. | [How to obtain](../../../foundations/identifiers.md#backup-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/x-zip-compressed`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

This API does not return a JSON payload on success. The body is the binary backup archive. Failures return the standard JSON failure envelope described in [General Response Payload Notes](overview.md#general-response-payload-notes).

| Header | Value | Description |
|--------|-------|-------------|
| `Content-Type` | `application/x-zip-compressed` | The archive is a zip-based `.wsbkp` file. |
| `Content-Disposition` | `attachment;filename="<name>.wsbkp"` | The name is `<workspace name>_<creation date, dd MMM yyyy>`, with spaces and special characters replaced by `_`. |
| `X-Download-Options` | `noopen` | Asks browsers to save the file, not open it. |

# Examples

## Sample Requests

**Case 1 — Download a backup**

```http
GET /restapi/v2/workspaces/137687000271334001/backups/137687000285490001/download HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

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

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Download Workspace Backup](../../../sdk-examples/workspace-management/workspace-backup-and-restore/download-workspace-backup.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success has no JSON body** | Read the response as a byte stream, not as JSON. Branch on the HTTP status first; only a non-`200` response carries a JSON error. |
| **Only completed backups** | The backup must have status `SUCCESS` and a stored file. Anything else — in progress, failed, deleted, or of unknown state — returns `8246`. |
| **Backup must belong to the workspace** | A `backupId` that does not exist, or belongs to a different workspace, returns `8245`; the two cases are indistinguishable by design. |
| **No expiry check here** | Unlike restore, this API does not apply the restore window (`8248`). A backup stays downloadable while it is `SUCCESS` and its file is stored. |
| **Download is recorded** | The call is written to the workspace's activity log, and the backup's last-downloaded time is updated. A failure to record that time does not fail the download. |
| **Large files** | The archive can be large for `STRUCTURE_AND_DATA` backups. Stream to disk rather than buffering in memory. |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Dependency chain** | [Get Workspace Backups](get-workspace-backups.md) or [Backup Workspace Now](backup-workspace-now.md) → `backupId` → [Get Workspace Backup Status](get-workspace-backup-status.md) (`SUCCESS`) → Download Workspace Backup. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6025](../../../foundations/error-codes.md#error-6025) | 400 | `BACKUP_NOT_ALLOWED` — The organisation's plan does not include Backup. | Upgrade the plan, or do not call the backup APIs for this organisation. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation that owns the workspace. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| [8084](../../../foundations/error-codes.md#error-8084) | 404 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| [8245](../../../foundations/error-codes.md#error-8245) | 404 | `BACKUP_NOT_FOUND` — The backup does not exist, or does not belong to this workspace. | Take the `backupId` from [Get Workspace Backups](get-workspace-backups.md) for the same workspace. |
| [8246](../../../foundations/error-codes.md#error-8246) | 400 | `BACKUP_NOT_READY` — The backup is not `SUCCESS`, or has no stored file. | Poll [Get Workspace Backup Status](get-workspace-backup-status.md) until `SUCCESS`; a `FAILED` or `DELETED` backup cannot be downloaded. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Workspace Backup & Restore overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Workspace Backups](get-workspace-backups.md), [Backup Workspace Now](backup-workspace-now.md), [Restore Workspace from Backup](restore-workspace-from-backup.md), [Get Workspace Backup Status](get-workspace-backup-status.md), [Get Workspace Restore Status](get-workspace-restore-status.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-backup-and-restore/download-workspace-backup.md).
