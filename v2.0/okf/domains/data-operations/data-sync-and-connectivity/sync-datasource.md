---
type: API Endpoint
title: Sync Data
description: "Triggers an immediate pull for a whole datasource — every table it feeds."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}/sync"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - data-sync-and-connectivity
  - post
  - metadata
api:
  operation_id: syncDatasource
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}/sync"
  domain: data-operations
  group: data-sync-and-connectivity
  oauth_scopes:
    - ZohoAnalytics.metadata.create
  org_id_header: required
  config_parameter:
    location: form
    required: false
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Table or Sync Data permission on the workspace."
  error_codes:
    - 7301
    - 8079
    - 8182
    - 8183
    - 8507
    - 8535
    - 18061
    - 18073
  openapi:
    file: "/references/openapi/data-operations-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1datasources~1{datasource-id}~1sync/post"
    config_schema: SyncDataConfig
    response_schema: null
  sdk_examples: "/sdk-examples/data-operations/data-sync-and-connectivity/sync-datasource.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-operations-grouped-api.json"
    title: OpenAPI 3 specification - data-operations-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}/sync`** - Sync Data (Data Sync & Connectivity / Data Operations).

Triggers an immediate pull for a whole datasource — every table it feeds.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace that owns the datasource. |
| `<datasource-id>` | Long | `dataSources[].datasourceId` from [Get Datasources](get-datasources.md). |

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `syncDatasource` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}/sync` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadatacreate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Table or Sync Data permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - optional |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1datasources~1{datasource-id}~1sync/post`; CONFIG schema `SyncDataConfig` |

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
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{datasource-id}` | string | ID of the datasource. | [How to obtain](../../../foundations/identifiers.md#datasource-id) |

## CONFIG Parameters

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `syncIntervalId` | Long | Conditional | — | Targets one sync interval of the datasource. **Mandatory when the datasource has more than one sync interval**, otherwise the call fails with `8182`. Omit for a single-interval datasource. An ID that belongs to a different datasource fails with `8183`. Obtain it from `dataSources[].syncIntervals[].syncIntervalId`. |
| `userName` | String | Conditional | — | Username for the source, up to 1,000 characters. Required only for sources that ask for credentials at fetch time — FTP/SFTP-hosted workbooks and MS Access sources. Ignored by every other source type. |
| `password` | String | Conditional | — | Password matching `userName`, up to 1,000 characters. |

> `isFullFetch` is not read by this API. Whether a pull is incremental or complete follows the datasource's own configuration. To choose explicitly, use [Refetch Data](refetch-datasource.md) on the individual table.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

**None.** This API returns `204 No Content` with an empty body. To learn what the sync did, call [Get Last Import Details](get-last-import-details.md) for a table it feeds, or re-read `lastDataSyncStatus` from [Get Datasources](get-datasources.md).

# Examples

## Sample Requests

**Case 1 — a single-interval datasource, no CONFIG at all**

```http
POST /restapi/v2/workspaces/466206000000071000/datasources/466206000000081000/sync HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

Most datasources need nothing beyond the path.

**Case 2 — a datasource with several sync intervals**

```http
POST /restapi/v2/workspaces/466206000000071000/datasources/466206000000081000/sync HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"syncIntervalId":"466206000000082000"}
```

Without `syncIntervalId` this same call fails with [`8182`](../../../foundations/error-codes.md#error-8182).

**Case 3 — an FTP-hosted workbook that asks for credentials**

```http
POST /restapi/v2/workspaces/466206000000071000/datasources/466206000000081500/sync HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"userName":"zylker_ftp","password":"Zoho@123"}
```

## Sample Responses

**HTTP 204 No Content — the sync was initiated**

```
HTTP/1.1 204 No Content
```

There is no response body. A `204` means the pull has been **started**, not that it has finished or succeeded.

**HTTP 403 Forbidden — the datasource has several intervals and none was named**

```json
{
  "status": "failure",
  "summary": "SYNC_CANNOT_BE_INITIATED_FOR_CONNECTOR_WITH_MULTIPLE_SCHEDULES",
  "data": {
    "errorCode": 8182,
    "errorMessage": "Sync cannot be initiated for a datasource with multiple schedules. Provide a syncIntervalId."
  }
}
```

**HTTP 400 Bad Request — the daily manual-sync quota is exhausted**

```json
{
  "status": "failure",
  "summary": "CONN_SYNCNOW_CNT_EXCEEDED",
  "data": {
    "errorCode": 19000048,
    "errorMessage": "You have exceeded the maximum number of manual syncs allowed for this connection."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Sync Data](../../../sdk-examples/data-operations/data-sync-and-connectivity/sync-datasource.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **204 means "started", not "finished"** | The pull runs in the background. A datasource with many tables may still be loading long after the response has been returned. |
| **There is no job ID and no polling endpoint** | Unlike the import and export job APIs, the sync APIs expose no handle on the run. Progress is observed through the table's import details. |
| **It consumes the daily manual-sync quota** | Five per connection per day; the counter resets daily. Check `syncUsed` against `totalSyncAllowed` first. |
| **`syncIntervalId` is conditionally mandatory** | Its necessity depends on the datasource's configuration, not on anything in the request. Read `syncIntervals` from [Get Datasources](get-datasources.md) to know which case you are in. |
| **`CONFIG` is optional** | For a single-interval datasource that stores its own credentials — the common case — the path alone is enough. |
| **`userName` and `password` are for the source, not for Zoho Analytics** | They are the credentials of the FTP server or MS Access file being fetched. They are treated as sensitive and excluded from request logging. |
| **It cannot address local-drive uploads or snapshots** | Those entries carry no `datasourceId`. A snapshot is refreshed with [Refetch Data](refetch-datasource.md) on its target table. |
| **A datasource ID from another workspace fails** | `18061`. IDs are not portable between workspaces. |
| **Dependency chain:** | [Get Datasources](get-datasources.md) → `datasourceId` (+ `syncIntervalId` when present) → Sync Data → [Get Last Import Details](get-last-import-details.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The request came through a Client Portal / White Label domain, or the caller lacks Create Table and Sync Data permission on the workspace. | Call from the standard API host with one of the two permissions. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — A mandatory attribute is missing. | The message names the attribute. |
| [8182](../../../foundations/error-codes.md#error-8182) | 403 | `SYNC_CANNOT_BE_INITIATED_FOR_CONNECTOR_WITH_MULTIPLE_SCHEDULES` — The datasource has more than one sync interval and none was named. | Send `syncIntervalId`; read the options from [Get Datasources](get-datasources.md). |
| [8183](../../../foundations/error-codes.md#error-8183) | 400 | `SCHEDULE_ID_NOT_ASSOCIATED_WITH_CONNECTOR` — The `syncIntervalId` does not belong to this datasource. | Use a `syncIntervalId` listed under this datasource's `syncIntervals`. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | `MORE_THAN_MAX_LENGTH` — `CONFIG` exceeds 3,000 characters, or a credential exceeds 1,000. | Shorten the value. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.metadata.create`. |
| [18061](../../../foundations/error-codes.md#error-18061) | 400 | `CONNECTION_ID_NOT_ASSOSIATED_FOR_WORKSPACE` — The datasource ID does not exist in this workspace, or the source type cannot be synced this way (HTTP 404). | Verify `<datasource-id>` with [Get Datasources](get-datasources.md). |
| [18073](../../../foundations/error-codes.md#error-18073) | 400 | `DATASOURCE_SYNC_INPROGRESS` — A sync for this datasource is already running. | Wait for the running sync to finish. |

# Related

- [Data Sync & Connectivity overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Refetch Data](refetch-datasource.md), [Update Datasource Connection](update-datasource-connection.md), [Get Datasources](get-datasources.md), [Get Last Import Details](get-last-import-details.md).
- [SDK examples](../../../sdk-examples/data-operations/data-sync-and-connectivity/sync-datasource.md).
