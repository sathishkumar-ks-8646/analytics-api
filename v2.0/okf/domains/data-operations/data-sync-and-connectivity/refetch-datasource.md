---
type: API Endpoint
title: Refetch Data
description: Sync data from the available datasource for the specified view - one table only.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/sync"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - data-sync-and-connectivity
  - post
  - metadata
api:
  operation_id: refetchDatasource
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/sync"
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
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Sync Data permission on the workspace."
  error_codes:
    - 7104
    - 7301
    - 8507
    - 8535
    - 18056
    - 18072
  openapi:
    file: "/references/openapi/data-operations-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1sync/post"
    config_schema: RefetchDataConfig
    response_schema: null
  sdk_examples: "/sdk-examples/data-operations/data-sync-and-connectivity/refetch-datasource.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-operations-grouped-api.json"
    title: OpenAPI 3 specification - data-operations-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/sync`** - Refetch Data (Data Sync & Connectivity / Data Operations).

Triggers an immediate pull for **one table** from whatever datasource sits behind it.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace that owns the view. |
| `<view-id>` | Long | ID of the table to refresh. Must belong to `<workspace-id>` and must have a datasource behind it. |

From the OpenAPI specification:

Sync data from the available datasource for the specified view - one table only. Returns 204 once the refetch has been started; the outcome is read from Get Last Import Details. A table with no datasource behind it fails with 18056. Consumes the daily manual sync quota. Not available through a Client Portal or White Label domain.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `refetchDatasource` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/sync` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadatacreate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Sync Data permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - optional |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1sync/post`; CONFIG schema `RefetchDataConfig` |

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
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `isFullFetch` | Boolean | No | `false` | Selects the fetch mode for database-backed tables — cloud and local databases, OData feeds, local files, Analytics-workspace tables, Elasticsearch, and data-lake tables. `false` fetches only what has changed since the last pull; `true` re-reads the source completely. Ignored by file, web, connector, and snapshot sources, which always fetch in full. |
| `userName` | String | Conditional | — | Username for the source, up to 1,000 characters. Required only for FTP/SFTP and web-hosted files whose credentials are not stored with the source. |
| `password` | String | Conditional | — | Password matching `userName`, up to 1,000 characters. |

> `syncIntervalId` is not read by this API. A table belongs to exactly one interval, so there is nothing to choose.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

**None.** This API returns `204 No Content` with an empty body. Call [Get Last Import Details](get-last-import-details.md) on the same `<view-id>` to see what the refetch did.

# Examples

## Sample Requests

**Case 1 — refresh one table, stored credentials, incremental**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000072000/sync HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — a full re-read of a cloud-database table**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000072000/sync HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"isFullFetch":true}
```

Use this when incremental fetches have drifted from the source — for example after rows were deleted at the source, which an incremental pull will not notice.

**Case 3 — a web-hosted file behind basic authentication**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000072500/sync HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"userName":"zylker_web","password":"Zoho@123"}
```

## Sample Responses

**HTTP 204 No Content — the refetch was initiated**

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — the table has no datasource**

```json
{
  "status": "failure",
  "summary": "NO_SOURCE_AVAILABLE_FOR_TABLE",
  "data": {
    "errorCode": 18056,
    "errorMessage": "No source is available for this table."
  }
}
```

**HTTP 400 Bad Request — a sync for this table is already running**

```json
{
  "status": "failure",
  "summary": "TABLE_SYNC_INPROGRESS",
  "data": {
    "errorCode": 18072,
    "errorMessage": "A sync is already in progress for this table."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Refetch Data](../../../sdk-examples/data-operations/data-sync-and-connectivity/refetch-datasource.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **204 means "started", not "finished"** | The pull runs in the background; the response says nothing about rows loaded. |
| **`isFullFetch` only applies to database-style sources** | For file, web, connector, and snapshot sources every fetch is a full one, and the attribute has no effect. |
| **`isFullFetch` defaults to incremental** | Sending no CONFIG is equivalent to `{"isFullFetch": false}`. |
| **An incremental fetch will not notice deletions at the source** | Rows removed upstream stay in the Zoho Analytics table until a full fetch replaces the data. This is the main reason to send `isFullFetch: true`. |
| **One refetch at a time per table** | A second call while the first is running fails with `18072`, not a queue. |
| **A table without a datasource cannot be refetched** | `18056`. Hand-built tables and tables loaded only by the import APIs have nothing to pull from. |
| **It consumes the daily manual-sync quota** | The same five-per-connection-per-day allowance that [Sync Data](sync-datasource.md) draws on. |
| **A snapshot table is refreshed here** | Snapshot entries carry no `datasourceId`, so [Sync Data](sync-datasource.md) cannot address them; refetching the target table re-runs the snapshot. |
| **The view must belong to the workspace in the path** | A view ID from a different workspace is rejected. |
| **Dependency chain:** | [Get Datasources](get-datasources.md) → `tableDetails[].viewId` → Refetch Data → [Get Last Import Details](get-last-import-details.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — The view does not exist. | Verify `<view-id>` with [Get View List](../../views-management/view-operations/get-views.md). |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The request came through a Client Portal / White Label domain, or the caller is neither an admin nor the View Owner and lacks Sync Data permission. | Call from the standard API host with the required permission. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | `MORE_THAN_MAX_LENGTH` — `CONFIG` exceeds 3,000 characters, or a credential exceeds 1,000. | Shorten the value. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.metadata.create`. |
| [18056](../../../foundations/error-codes.md#error-18056) | 400 | `NO_SOURCE_AVAILABLE_FOR_TABLE` — The table has no datasource behind it. | Refetch only tables fed by a datasource; use the import APIs otherwise. |
| [18072](../../../foundations/error-codes.md#error-18072) | 400 | `TABLE_SYNC_INPROGRESS` — A sync for this table is already running. | Wait for it to finish, then retry. |

# Related

- [Data Sync & Connectivity overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Sync Data](sync-datasource.md), [Update Datasource Connection](update-datasource-connection.md), [Get Datasources](get-datasources.md), [Get Last Import Details](get-last-import-details.md).
- [SDK examples](../../../sdk-examples/data-operations/data-sync-and-connectivity/refetch-datasource.md).
