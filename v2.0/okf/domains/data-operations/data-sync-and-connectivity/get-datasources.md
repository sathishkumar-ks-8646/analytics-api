---
type: API Endpoint
title: Get Datasources
description: "Returns the list of datasources for the specified workspace, the tables each one feeds, and the state of their last sync."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/datasources"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - data-sync-and-connectivity
  - get
  - metadata
api:
  operation_id: getDatasources
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/datasources"
  domain: data-operations
  group: data-sync-and-connectivity
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with View Datasource or Create Table permission on the workspace."
  error_codes:
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/data-operations-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1datasources/get"
    config_schema: null
    response_schema: GetDatasourcesResponse
  sdk_examples: "/sdk-examples/data-operations/data-sync-and-connectivity/get-datasources.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-operations-grouped-api.json"
    title: OpenAPI 3 specification - data-operations-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/datasources`** - Get Datasources (Data Sync & Connectivity / Data Operations).

Lists every datasource in a workspace, the tables each one feeds, and the state of their last sync.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace whose datasources are listed. |

From the OpenAPI specification:

Returns the list of datasources for the specified workspace, the tables each one feeds, and the state of their last sync. This is the only API that returns datasourceId, syncIntervalId and the datasource-to-view mapping. The entry shape varies by source family, so test for the presence of a field rather than assuming a fixed schema. Not available through a Client Portal or White Label domain.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getDatasources` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/datasources` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with View Datasource or Create Table permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1datasources/get`; response schema `GetDatasourcesResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | `"success"` on success. |
| `summary` | String | `"Fetch Datasources"`. |
| `data` | Object | Wrapper. |
| `data.dataSources` | Array | One entry per datasource. Empty when the workspace has none. |
| `dataSources[].datasourceName` | String | Display name of the datasource. For local-drive uploads and snapshots this is the family name (`"Local Drive"`, `"Snapshot"`) rather than an individual connection. |
| `dataSources[].datasourceId` | String | ID of the datasource, as a string. The `<datasource-id>` for [Sync Data](sync-datasource.md) and [Update Datasource Connection](update-datasource-connection.md). **Absent** for local-drive uploads and snapshots. |
| `dataSources[].source` | String | The underlying source identifier — a database name, a URL, or the connected account. |
| `dataSources[].fileType` | String | Format of the source file. Present for file-based datasources only. |
| `dataSources[].authType` | String | Authentication method used to reach the source. Present for sources that authenticate. |
| `dataSources[].databridgeName` | String | Name of the Zoho Databridge agent relaying the connection. Present for local-database sources only. |
| `dataSources[].databridgeStatus` | String | Current state of that agent. Present for local-database sources only. |
| `dataSources[].lastDataSyncStatus` | String | Outcome of the last data sync. Present when the datasource has a single sync interval; otherwise it appears inside each `syncIntervals` entry. Absent for Live Connect. |
| `dataSources[].lastDataSyncTime` | String | When data was last synced, formatted `dd MMMM, yyyy hh:mm:ss a z`. Absent for Live Connect. |
| `dataSources[].schedule` | String | The configured sync schedule, as displayed text (`"Every 15 Minutes"`, `"Daily"`, `"Not Applicable"`). |
| `dataSources[].nextScheduleTime` | String | When the next scheduled sync will run. Absent for Live Connect. |
| `dataSources[].syncUsed` | String | Manual syncs already used today for this connection. |
| `dataSources[].totalSyncAllowed` | String | Manual syncs permitted per day for this connection. |
| `dataSources[].lastDesignSyncStatus` | String | Outcome of the last **schema** sync. Live Connect only — a Live Connect datasource syncs its structure, not its data. |
| `dataSources[].lastDesignSyncTime` | String | When the schema was last synced. Live Connect only; empty string when it has never run. |
| `dataSources[].syncIntervalId` | String | ID of the datasource's single sync interval. Present only when there is exactly one; otherwise use `syncIntervals`. |
| `dataSources[].syncIntervals` | Array | One entry per configured sync interval. Present when the datasource supports multiple schedules. |
| `dataSources[].syncIntervals[].syncIntervalId` | String | ID of this interval. Send it as `syncIntervalId` to [Sync Data](sync-datasource.md). |
| `dataSources[].syncIntervals[].lastDataSyncStatus` | String | Outcome of this interval's last run. |
| `dataSources[].syncIntervals[].lastDataSyncTime` | String | When this interval last ran. |
| `dataSources[].syncIntervals[].schedule` | String | This interval's schedule. |
| `dataSources[].syncIntervals[].nextScheduleTime` | String | When this interval will next run. |
| `dataSources[].syncIntervals[].syncUsed` | String | Manual syncs already used today for this interval. |
| `dataSources[].syncIntervals[].tableDetails` | Array | Tables fed by this interval. Same shape as `dataSources[].tableDetails`. |
| `dataSources[].tableDetails` | Array | Tables fed by this datasource. Present for non-connector sources. |
| `dataSources[].tableDetails[].viewName` | String | Name of the table in Zoho Analytics. |
| `dataSources[].tableDetails[].viewId` | String | ID of the table, as a string. The `<view-id>` for [Refetch Data](refetch-datasource.md) and [Get Last Import Details](get-last-import-details.md). |
| `dataSources[].tableDetails[].sourceName` | String | Name of the corresponding object at the source. |
| `dataSources[].tableDetails[].lastSyncTime` | String | When this table was last synced. |
| `dataSources[].tableDetails[].syncStatus` | String | Outcome of this table's last sync. |
| `dataSources[].tableDetails[].schedule` | String | Snapshot entries only — the snapshot's own schedule. |
| `dataSources[].tableDetails[].nextScheduleTime` | String | Snapshot entries only — when the snapshot next runs. |
| `dataSources[].tableDetails[].status` | String | Snapshot entries only — `"active"` or `"inactive"`. |

# Examples

## Sample Requests

```http
GET /restapi/v2/workspaces/466206000000071000/datasources HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

There is nothing else to send.

## Sample Responses

**HTTP 200 OK — a cloud database with two sync intervals**

Multi-interval datasources report their schedules under `syncIntervals`, each with its own tables.

```json
{
  "status": "success",
  "summary": "Fetch Datasources",
  "data": {
    "dataSources": [
      {
        "datasourceName": "Amazon RDS MySQL",
        "datasourceId": "466206000000081000",
        "source": "relmodel",
        "totalSyncAllowed": "5",
        "syncIntervals": [
          {
            "syncIntervalId": "466206000000082000",
            "lastDataSyncStatus": "Success",
            "lastDataSyncTime": "03 August, 2026 03:39:16 PM IST",
            "schedule": "Every 15 Minutes",
            "nextScheduleTime": "03 August, 2026 03:54:16 PM IST",
            "syncUsed": "1",
            "tableDetails": [
              {
                "viewName": "Sales",
                "viewId": "466206000000072000",
                "sourceName": "sales",
                "lastSyncTime": "03 August, 2026 03:39:13 PM IST",
                "syncStatus": "Success"
              }
            ]
          },
          {
            "syncIntervalId": "466206000000082500",
            "lastDataSyncStatus": "Success",
            "lastDataSyncTime": "03 August, 2026 02:00:04 PM IST",
            "schedule": "Daily",
            "nextScheduleTime": "04 August, 2026 02:00:00 PM IST",
            "syncUsed": "0",
            "tableDetails": [
              {
                "viewName": "Targets",
                "viewId": "466206000000072500",
                "sourceName": "targets",
                "lastSyncTime": "03 August, 2026 02:00:01 PM IST",
                "syncStatus": "Success"
              }
            ]
          }
        ]
      }
    ]
  }
}
```

**HTTP 200 OK — a mix of source types in one workspace**

A file source, an integration connector, a Live Connect database, a local-drive upload, and a snapshot. Note how the fields differ between them.

```json
{
  "status": "success",
  "summary": "Fetch Datasources",
  "data": {
    "dataSources": [
      {
        "datasourceName": "Monthly Sales CSV",
        "datasourceId": "466206000000083000",
        "source": "https://files.zylker.com/monthly-sales.csv",
        "fileType": "csv",
        "authType": "basic",
        "lastDataSyncStatus": "Success",
        "lastDataSyncTime": "03 August, 2026 06:00:12 AM IST",
        "schedule": "Daily",
        "nextScheduleTime": "04 August, 2026 06:00:00 AM IST",
        "syncUsed": "0",
        "totalSyncAllowed": "5",
        "tableDetails": [
          {
            "viewName": "MonthlySales",
            "viewId": "466206000000073000",
            "sourceName": "monthly-sales.csv",
            "lastSyncTime": "03 August, 2026 06:00:10 AM IST",
            "syncStatus": "Success"
          }
        ]
      },
      {
        "datasourceName": "Zoho CRM",
        "datasourceId": "466206000000084000",
        "source": "zylker_crm",
        "lastDataSyncStatus": "Failed",
        "lastDataSyncTime": "03 August, 2026 05:00:41 AM IST",
        "schedule": "Every 3 Hours",
        "nextScheduleTime": "03 August, 2026 08:00:00 AM IST",
        "syncUsed": "2",
        "totalSyncAllowed": "5"
      },
      {
        "datasourceName": "Warehouse PostgreSQL",
        "datasourceId": "466206000000085000",
        "source": "warehouse",
        "databridgeName": "zylker-bridge-01",
        "databridgeStatus": "active",
        "lastDesignSyncStatus": "Success",
        "lastDesignSyncTime": "01 August, 2026 11:20:05 AM IST",
        "schedule": "Not Applicable",
        "syncUsed": "0",
        "totalSyncAllowed": "5",
        "tableDetails": [
          {
            "viewName": "Orders",
            "viewId": "466206000000074000",
            "sourceName": "public.orders"
          }
        ]
      },
      {
        "datasourceName": "Local Drive",
        "tableDetails": [
          {
            "viewName": "RegionLookup",
            "viewId": "466206000000075000",
            "sourceName": "region-lookup.xlsx",
            "lastSyncTime": "28 July, 2026 04:12:33 PM IST",
            "syncStatus": "Success"
          }
        ]
      },
      {
        "datasourceName": "Snapshot",
        "tableDetails": [
          {
            "viewName": "Sales_Snapshot_July",
            "viewId": "466206000000076000",
            "sourceName": "Sales",
            "lastSyncTime": "31 July, 2026 11:59:00 PM IST",
            "syncStatus": "Success",
            "schedule": "Monthly",
            "nextScheduleTime": "31 August, 2026 11:59:00 PM IST",
            "status": "active"
          }
        ]
      }
    ]
  }
}
```

**HTTP 200 OK — a workspace with no datasources**

```json
{
  "status": "success",
  "summary": "Fetch Datasources",
  "data": {
    "dataSources": []
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Datasources](../../../sdk-examples/data-operations/data-sync-and-connectivity/get-datasources.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **This is the only source of `datasourceId`, `syncIntervalId`, and the datasource-to-table mapping** | Three of the other four APIs depend on IDs that appear nowhere else. |
| **The entry shape varies by source type** | A field's absence is meaningful, not an error. Test for keys rather than assuming a fixed schema — see [Source Types](overview.md#source-types). |
| **Single-interval and multi-interval datasources report differently** | With one interval the sync fields sit directly on the datasource; with several they move into `syncIntervals`, and the top-level `syncIntervalId` disappears. Handle both. |
| **Live Connect reports a design sync, not a data sync** | `lastDesignSyncStatus` and `lastDesignSyncTime` replace the data-sync fields, because a Live Connect datasource keeps its structure in step rather than copying rows. |
| **Integration connectors report no tables** | Connector entries omit `tableDetails` entirely; the tables they populate are visible through [Get View List](../../views-management/view-operations/get-views.md). |
| **Local-drive and snapshot entries have no `datasourceId`** | They cannot be synced or updated through this suite. A snapshot's target table can still be refreshed with [Refetch Data](refetch-datasource.md). |
| **Every value is a string** | Including IDs, counts, and `syncUsed` / `totalSyncAllowed`. Nothing in the response is a JSON number. |
| **Times are pre-formatted display strings** | `dd MMMM, yyyy hh:mm:ss a z` — not epoch values and not ISO 8601. Parse against that pattern or treat them as opaque. |
| **A caller with only Create Table sees a reduced list** | Connection details for sources they did not create are filtered out. Grant **View Datasource** for the full picture. |
| **Dependency chain:** | Get Datasources → `datasourceId` → [Sync Data](sync-datasource.md) / [Update Datasource Connection](update-datasource-connection.md); → `tableDetails[].viewId` → [Refetch Data](refetch-datasource.md) / [Get Last Import Details](get-last-import-details.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The request came through a Client Portal / White Label domain, or the caller lacks View Datasource and Create Table permission on the workspace. | Call from the standard API host with one of the two permissions. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.metadata.read`. |

# Related

- [Data Sync & Connectivity overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Sync Data](sync-datasource.md), [Refetch Data](refetch-datasource.md), [Update Datasource Connection](update-datasource-connection.md), [Get Last Import Details](get-last-import-details.md).
- [SDK examples](../../../sdk-examples/data-operations/data-sync-and-connectivity/get-datasources.md).
