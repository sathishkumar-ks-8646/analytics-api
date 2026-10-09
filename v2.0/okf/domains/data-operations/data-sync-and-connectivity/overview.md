---
type: API Group
title: Data Sync & Connectivity
description: "APIs for import history, datasource sync/refetch, datasource updates, and listing datasources."
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - data-sync-and-connectivity
  - api-group
api:
  domain: data-operations
  group: data-sync-and-connectivity
  endpoint_count: 5
  endpoints:
    - operation_id: syncDatasource
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}/sync"
      doc: "/domains/data-operations/data-sync-and-connectivity/sync-datasource.md"
    - operation_id: refetchDatasource
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/sync"
      doc: "/domains/data-operations/data-sync-and-connectivity/refetch-datasource.md"
    - operation_id: updateDatasourceConnection
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}"
      doc: "/domains/data-operations/data-sync-and-connectivity/update-datasource-connection.md"
    - operation_id: getDatasources
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/datasources"
      doc: "/domains/data-operations/data-sync-and-connectivity/get-datasources.md"
    - operation_id: getLastImportDetails
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/importdetails"
      doc: "/domains/data-operations/data-sync-and-connectivity/get-last-import-details.md"
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

This document covers the five REST APIs that manage the **datasources** of a workspace — the connections Zoho Analytics uses to pull data in from outside, the schedules that drive them, and the record of what the last pull actually did.

APIs for import history, datasource sync/refetch, datasource updates, and listing datasources.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Sync Data](sync-datasource.md) | POST | `/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}/sync` | `syncDatasource` | `ZohoAnalytics.metadata.create` | 204 |
| [Refetch Data](refetch-datasource.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/sync` | `refetchDatasource` | `ZohoAnalytics.metadata.create` | 204 |
| [Update Datasource Connection](update-datasource-connection.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}` | `updateDatasourceConnection` | `ZohoAnalytics.metadata.update` | 204 |
| [Get Datasources](get-datasources.md) | GET | `/restapi/v2/workspaces/{workspace-id}/datasources` | `getDatasources` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Last Import Details](get-last-import-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/importdetails` | `getLastImportDetails` | `ZohoAnalytics.metadata.read` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What these APIs are for

Every table in Zoho Analytics that is not hand-built has a **datasource** behind it: a cloud database, a local database reached through Zoho Databridge, an FTP or web-hosted file, a cloud-storage bucket, a business application connected through an integration connector, a live-connect database, or a snapshot. These five APIs let you inspect those datasources, trigger a pull on demand, repair a connection whose credentials or host have changed, and read the outcome of the last pull.

They do **not** create datasources, and they do not load data supplied in the request. Creating a connection is done in the Zoho Analytics interface; pushing data into a table is [Synchronous Data Import](../sync-data-import/overview.md) or [Asynchronous & Batch Data Import](../async-data-import/overview.md).

| | Data sync (this document) | Data import |
|---|---|---|
| **Where the data comes from** | A datasource Zoho Analytics already knows about | The request payload |
| **Who initiates the transfer** | Zoho Analytics pulls | The caller pushes |
| **What you supply** | A datasource ID or view ID, and optionally credentials | The file or rows themselves |
| **Typical use** | "Refresh this table from its source, now" | "Load this file into a table" |

---

# How the Five APIs Relate

[Get Datasources](get-datasources.md) is the entry point: it is the only API that hands you a `datasourceId`, a `syncIntervalId`, and the `viewId` of every table each datasource feeds. Everything else consumes one of those three.

```
                       4. Get Datasources
                     (GET .../datasources)
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
   datasourceId          syncIntervalId          tableDetails[].viewId
        │                       │                       │
        ├───────────────────────┘                       │
        ▼                                               ▼
  1. Sync Data                                    2. Refetch Data
  (whole datasource,                              (one table only)
   optionally one interval)                             │
        │                                               │
        └───────────────────┬───────────────────────────┘
                            ▼
                 5. Get Last Import Details
              (GET .../views/<view-id>/importdetails)
                     — did the pull work?

  datasourceId ──► 3. Update Datasource Connection
                   (repair host / credentials, then sync again)
```

| Relationship | Detail |
|--------------|--------|
| **`datasourceId` has exactly one source** | It is returned only by [Get Datasources](get-datasources.md), as `dataSources[].datasourceId`. It is the `<datasource-id>` for [Sync Data](sync-datasource.md) and [Update Datasource Connection](update-datasource-connection.md). No other API in the suite returns it. |
| **`syncIntervalId` also has exactly one source** | [Get Datasources](get-datasources.md) returns it as `dataSources[].syncIntervals[].syncIntervalId`. It becomes **mandatory** for [Sync Data](sync-datasource.md) as soon as a datasource has more than one sync interval. |
| **`viewId` comes from the datasource listing too** | `dataSources[].tableDetails[].viewId` (or `dataSources[].syncIntervals[].tableDetails[].viewId`) tells you which tables a datasource feeds. Those are the IDs [Refetch Data](refetch-datasource.md) and [Get Last Import Details](get-last-import-details.md) accept. [Get View List](../../views-management/view-operations/get-views.md) also returns view IDs, but it does not tell you which have a datasource behind them. |
| **Sync Data and Refetch Data work at different levels** | [Sync Data](sync-datasource.md) pulls a **whole datasource** — every table it feeds. [Refetch Data](refetch-datasource.md) pulls **one table**. See [Two Levels of Sync](overview.md#two-levels-of-sync). |
| **Neither sync API reports its outcome** | Both return `204` with no body. The only way to find out whether the pull succeeded is [Get Last Import Details](get-last-import-details.md) for a table, or the `lastDataSyncStatus` fields from [Get Datasources](get-datasources.md) for the datasource. |
| **Update Datasource Connection is the repair path** | When `lastDataSyncStatus` reports a connection failure, [Update Datasource Connection](update-datasource-connection.md) is how you correct the host, port, or credentials — then re-run [Sync Data](sync-datasource.md). It applies only to database-style connections; see its own section. |
| **The sync quota is shared and visible** | `syncUsed` and `totalSyncAllowed` from [Get Datasources](get-datasources.md) report the manual-sync quota that [Sync Data](sync-datasource.md) consumes. Read them before triggering a sync rather than catching `19000048`. |
| **Data arriving through these APIs is read back with the Row and Export APIs** | Once a sync lands, the data is ordinary table data — [Get Rows](../row-operations/overview.md), [Export Data from a View](../sync-data-export/export-data-view.md), and the reporting APIs all apply. |

## Typical sequences

**Refresh everything behind one datasource and confirm it worked**

```
Get Datasources → datasourceId, tableDetails[].viewId
   → Sync Data (204)
   → Get Last Import Details for each viewId → lastImportStatus
```

**Refresh a single table**

```
Get Datasources → tableDetails[].viewId
   → Refetch Data (204)
   → Get Last Import Details → lastImportStatus, rows.success
```

**A connection has started failing**

```
Get Datasources → lastDataSyncStatus reports a failure
   → Update Datasource Connection (new host / credentials, 204)
   → Sync Data (204)
   → Get Last Import Details → confirm recovery
```

**A datasource with several schedules**

```
Get Datasources → syncIntervals[].syncIntervalId
   → Sync Data with {"syncIntervalId": "..."}   ← mandatory here
```

---

# Two Levels of Sync

[Sync Data](sync-datasource.md) and [Refetch Data](refetch-datasource.md) look similar and are not interchangeable.

| | [Sync Data](sync-datasource.md) | [Refetch Data](refetch-datasource.md) |
|---|---|---|
| **Addressed by** | `<datasource-id>` | `<view-id>` |
| **Scope** | The whole datasource — every table it feeds | One table |
| **Multiple schedules** | Can target one via `syncIntervalId`; mandatory when more than one exists | Not applicable |
| **Incremental vs full** | Follows the datasource's own configuration | Selectable with `isFullFetch` |
| **Consumes the manual-sync quota** | Yes | Yes |
| **Permission** | Create Table **or** Sync Data on the workspace | Sync Data on the workspace, or ownership of the view |
| **Typical use** | Scheduled refresh triggered early | One table is stale or failed while others succeeded |

> If a table has no datasource behind it — a hand-built table, or one loaded only by the import APIs — [Refetch Data](refetch-datasource.md) fails with [`18056`](../../../foundations/error-codes.md#error-18056). There is nothing to refetch from.

---

# Source Types

The shape of a datasource entry, and which APIs apply to it, depend on what kind of source it is.

| Source family | Examples | Has `datasourceId` | `syncIntervals` | Updatable by [Update Datasource Connection](update-datasource-connection.md) |
|---------------|----------|:------------------:|:---------------:|:----------------------------:|
| **Cloud / local databases** | Amazon RDS, Redshift, Azure SQL, Snowflake, BigQuery, Athena, MongoDB Atlas, Databricks | ✓ | ✓ | ✓ |
| **Analytics / data-lake tables, OData, Elasticsearch, local files** | Zoho Analytics workspace tables, OData feeds, data-lake tables | ✓ | ✓ | – |
| **Live Connect** | A database queried live rather than imported | ✓ | – | ✓ (credentials only) |
| **File and web sources** | FTP / SFTP, web URL, cloud storage, MS Access, workbooks | ✓ | – | – |
| **Integration connectors** | Zoho CRM, Zoho Desk, Google Analytics, Salesforce and similar | ✓ | – | – |
| **Local drive uploads** | Files uploaded from a desktop | – | – | – |
| **Snapshots** | A point-in-time copy of another table | – | – | – |

Local-drive and snapshot entries appear in [Get Datasources](get-datasources.md) with a name and their table list only — they carry no `datasourceId`, so neither [Sync Data](sync-datasource.md) nor [Update Datasource Connection](update-datasource-connection.md) can address them.

---

# Limitations

These are the limits that apply with **default settings**.

| Limitation | Value | Enforced by |
|------------|-------|-------------|
| **Manual syncs per datasource connection** | **5 per day.** The counter resets daily and is reported as `syncUsed` against `totalSyncAllowed` by [Get Datasources](get-datasources.md). Both [Sync Data](sync-datasource.md) and [Refetch Data](refetch-datasource.md) consume it. | `19000048` |
| **One sync at a time per table** | A table already being synced cannot be synced again until the current run finishes. | `18072` |
| **Repeated rapid calls are throttled** | [Sync Data](sync-datasource.md) and [Refetch Data](refetch-datasource.md) are additionally rate limited per user. A burst of calls in quick succession is locked out for a short cool-off period. | Framework-level rejection |
| **`syncIntervalId` becomes mandatory above one interval** | A datasource with more than one sync interval cannot be synced as a whole. | `8182` |
| **`CONFIG` length — Sync Data / Refetch Data** | **3,000** characters. | `8507` |
| **`CONFIG` length — Update Datasource Connection** | **1,000,000** characters. | `8507` |
| **`userName`, `password` length** | **1,000** characters. | `8507` |
| **`hostName`, `instanceName`, `warehouseName`, `projectId`, `cloudDatabaseName`, `schemaName`, `s3OutputLocation`, SSH tunnel fields** | **10,000** characters each. | `8507` |
| **`connectionString` length** | **20,000** characters. | `8507` |
| **`catalogName`, `workgroupName` length** | **150** characters each. | `8507` |
| **`dataLocation` length** | **30** characters. | `8507` |
| **Datasource creation** | **Not supported by any API in this document.** Connections are created in the Zoho Analytics interface. | — |
| **Client Portal / White Label** | All five APIs are unavailable through a custom domain. | `7301` |

> **Read the quota before spending it.** `syncUsed` and `totalSyncAllowed` are returned by [Get Datasources](get-datasources.md) for every connection. Checking them is cheaper than discovering the limit through `19000048`, and it is the only way to know how many manual syncs remain today.

---

# Permission Model

| API | Who may call it |
|-----|-----------------|
| [Sync Data](sync-datasource.md) | An Account Admin or Organization Admin, or a Workspace Admin, or any user with **Create Table** or **Sync Data** permission on the workspace. |
| [Refetch Data](refetch-datasource.md) | An Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with **Sync Data** permission on the workspace. |
| [Update Datasource Connection](update-datasource-connection.md) | An Account Admin or Organization Admin, or a Workspace Admin, or any user with **Create Table** or **Edit Datasource** permission on the workspace. |
| [Get Datasources](get-datasources.md) | An Account Admin or Organization Admin, or a Workspace Admin, or any user with **View Datasource** or **Create Table** permission on the workspace. |
| [Get Last Import Details](get-last-import-details.md) | An Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with **View Datasource** or an import permission on the view. |

One further gate applies to every API here:

| Gate | Behaviour |
|------|-----------|
| **Client Portal / White Label** | All five are unavailable through a custom domain and are rejected with `7301` before the permission check runs. |

> **View Datasource is narrower than Create Table.** A caller holding only **Create Table** gets the datasource list, but connection details belonging to sources they did not create are filtered out. Grant **View Datasource** for a complete listing.

---

# API-Specific Notes and Behaviours

## Sync Data

- **The whole datasource moves, not one table.** If a datasource feeds twenty tables, this pulls all twenty. When only one is stale, [Refetch Data](refetch-datasource.md) is the cheaper instrument — and both draw on the same daily quota.
- **`syncIntervalId` is mandatory or forbidden depending on data you do not have in hand.** Nothing in the request tells you which case applies; you have to have read `syncIntervals` from [Get Datasources](get-datasources.md) first. An integration that skips the listing call will meet [`8182`](../../../foundations/error-codes.md#error-8182) in production the first time someone adds a second schedule.
- **The quota is per connection and resets daily.** Five manual syncs is not many for an active integration. Read `syncUsed` and `totalSyncAllowed` and decide, rather than catching `19000048` and retrying.
- **`204` is the whole response.** There is no job ID, no queue position, and no polling endpoint. The pull's outcome lives in [Get Last Import Details](get-last-import-details.md), one table at a time.
- **Credentials in CONFIG are for the source system.** They are supplied per call for sources that do not store them, and are excluded from request logging.
- **Dependency chain:** [Get Datasources](get-datasources.md) → `datasourceId` (+ `syncIntervalId`) → Sync Data → [Get Last Import Details](get-last-import-details.md).

## Refetch Data

- **`isFullFetch` is the attribute that matters, and its default is the surprising one.** Incremental is the default, and an incremental fetch will not remove rows that were deleted at the source. A table that has silently drifted needs `isFullFetch: true`.
- **It is the only way to refresh a snapshot.** Snapshot datasources carry no `datasourceId`, so [Sync Data](sync-datasource.md) cannot reach them; refetching the snapshot's target table re-runs it.
- **[`18056`](../../../foundations/error-codes.md#error-18056) means the table has no source, not that the source failed.** Hand-built tables and tables loaded only through the import APIs will always return it — that is a design fact, not a fault to retry.
- **[`18072`](../../../foundations/error-codes.md#error-18072) is a concurrency guard, not a rate limit.** One refetch per table at a time; the fix is to wait for the running one, not to back off and retry blindly.
- **It draws on the same quota as [Sync Data](sync-datasource.md).** Refetching twenty tables individually is not a way around the five-per-connection ceiling.
- **Dependency chain:** [Get Datasources](get-datasources.md) → `tableDetails[].viewId` → Refetch Data → [Get Last Import Details](get-last-import-details.md).

## Update Datasource Connection

- **It replaces the connection rather than patching it.** This is the single most consequential behaviour of this API: omitted attributes are reset, not preserved. Fetch the current definition, change one field, and resend everything.
- **Three attributes are mandatory on every call**, even a password rotation: `serviceName`, `hostName`, `userName`.
- **`databaseType` is required more often than it looks.** Most named services support several engines, so in practice it is mandatory. Omitting it yields [`8079`](../../../foundations/error-codes.md#error-8079) naming `databaseType`, which reads like a missing-field bug rather than a service-capability rule.
- **`hostName` does not always mean a host.** For Amazon Athena it carries the AWS region; for Snowflake, the account name. Sending a URL there is the most common cause of a connection that stores cleanly and then fails to sync.
- **Live Connect connections are half-frozen.** Credentials and endpoint can change; `serviceName` ([`18064`](../../../foundations/error-codes.md#error-18064)) and `databaseType` ([`18063`](../../../foundations/error-codes.md#error-18063)) cannot. To change the engine, rebuild the connection in the interface.
- **`connType`, `authSource`, and `connectionString` only survive for MongoDB variants.** For every other engine the server overwrites them from `databaseType`.
- **A `204` is not a connectivity test.** The details are stored, nothing is dialled. Run [Sync Data](sync-datasource.md) and read the result to know whether they work.
- **It cannot create a connection**, and it cannot touch file, web, cloud-storage, connector, snapshot, or local-drive datasources — [`18061`](../../../foundations/error-codes.md#error-18061) for all of them.
- **Dependency chain:** [Get Datasources](get-datasources.md) → `datasourceId` → Update Datasource Connection → [Sync Data](sync-datasource.md) → [Get Last Import Details](get-last-import-details.md).

## Get Datasources

- **It is the map for this entire document.** `datasourceId`, `syncIntervalId`, and the datasource-to-`viewId` mapping appear in no other response anywhere in the V2 surface. Every integration here starts with this call.
- **The response is polymorphic by design.** Six source families produce six field shapes. Writing a strict deserialiser against one sample will break on the next workspace — key presence is the contract, not a fixed schema.
- **The single-interval / multi-interval split is the sharpest edge.** One interval puts the sync fields on the datasource; two or more move them into `syncIntervals` and remove the top-level `syncIntervalId`. The same datasource changes shape the moment an administrator adds a schedule.
- **Live Connect reports schema syncs, not data syncs.** Looking for `lastDataSyncStatus` on a Live Connect entry finds nothing; the fields are `lastDesignSyncStatus` and `lastDesignSyncTime`.
- **Two entries have no ID at all.** Local-drive uploads and snapshots list their tables but expose no `datasourceId`, which is exactly why neither [Sync Data](sync-datasource.md) nor [Update Datasource Connection](update-datasource-connection.md) can address them.
- **It is also the quota display.** `syncUsed` / `totalSyncAllowed` are the only place the manual-sync allowance is visible.
- **Timestamps are display strings, not machine values.** `03 August, 2026 03:39:16 PM IST` — rendered in a fixed pattern, not epoch or ISO 8601.
- **Dependency chain:** Get Datasources → everything else in this document.

## Get Last Import Details

- **It is the outcome report for two APIs that have none.** [Sync Data](sync-datasource.md) and [Refetch Data](refetch-datasource.md) both return `204`; this is where the result surfaces.
- **An empty `data` object is the "never loaded" signal**, and it arrives with HTTP `200` and `status: "success"`. Code that assumes `data.viewName` exists will fail on a freshly created table.
- **It does not say what performed the load.** A datasource sync and an import API call are indistinguishable here. If you need to attribute a load, record it yourself.
- **`Success` does not imply rows were written.** A sync that found nothing new reports `Success` with counts of `-1`. Compare `rows.success` against `rows.total` before drawing conclusions.
- **`Partial Success` is the one to alert on.** It means data landed but not all of it — the failure mode most likely to go unnoticed, because nothing errored.
- **`importErrors` is HTML.** Display or log it; it is not structured data and its shape is not guaranteed.
- **Dependency chain:** [Get Datasources](get-datasources.md) → `tableDetails[].viewId` → [Sync Data](sync-datasource.md) / [Refetch Data](refetch-datasource.md) → Get Last Import Details.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Three APIs return 204, two return 200** | [Sync Data](sync-datasource.md), [Refetch Data](refetch-datasource.md), and [Update Datasource Connection](update-datasource-connection.md) return `204 No Content` with an empty body. [Get Datasources](get-datasources.md) and [Get Last Import Details](get-last-import-details.md) return `200` with the standard envelope. |
| **A 204 confirms acceptance, not completion** | For the two sync APIs it means the pull was started; for the update API it means the details were stored. Neither implies the operation worked. |
| **Failure responses share one shape** | `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name (for example `NO_SOURCE_AVAILABLE_FOR_TABLE`), not a localised sentence. |
| **Every value in a success `data` object is a string** | IDs, counts, quotas, and statuses alike. Nothing is a JSON number or boolean. |
| **Timestamps use one fixed display format** | `dd MMMM, yyyy hh:mm:ss a z`, for example `03 August, 2026 03:39:16 PM IST`. This applies to `lastDataSyncTime`, `lastSyncTime`, `nextScheduleTime`, `lastDesignSyncTime`, and `lastImportTime`. |
| **Field presence is conditional and meaningful** | Both `200` responses omit fields that do not apply to the source or the situation. Absence carries information; test for keys. |
| **`data` can be legitimately empty** | `{"dataSources": []}` for a workspace with no datasources, and `{}` for a table that has never been loaded. Both are successes. |
| **Status vocabularies differ between the two read APIs** | [Get Datasources](get-datasources.md) reports sync statuses as source-provided display text; [Get Last Import Details](get-last-import-details.md) reports a fixed three-value set. Do not compare them directly. |
| **Credentials never appear in a response** | Usernames, passwords, tokens, and connection strings are write-only. [Get Datasources](get-datasources.md) reports the host and the account, never the secret. |

---

# Enum and Value Reference

**`sshTunnelAuthType`** — [Update Datasource Connection](update-datasource-connection.md), default `0`

| Value | Authentication method |
|-------|-----------------------|
| `0` | Password |
| `1` | Public key |

**`connType`** — [Update Datasource Connection](update-datasource-connection.md), MongoDB variants only

| Value | Connection style |
|-------|------------------|
| `1` | Individual fields — `hostName`, `port`, `userName`, `password` |
| `2` | A single `connectionString` |

**`isFullFetch`** — [Refetch Data](refetch-datasource.md), default `false`

| Value | Fetch mode |
|-------|------------|
| `false` | Incremental — only data changed since the last pull |
| `true` | Full — the source is re-read completely |

**`lastImportStatus`** — [Get Last Import Details](get-last-import-details.md)

| Value | Meaning |
|-------|---------|
| `Success` | Everything loaded, or nothing needed loading |
| `Partial Success` | Some rows loaded, some did not |
| `Failed` | The load did not complete |

**`databridgeStatus`** — [Get Datasources](get-datasources.md), local-database sources only

| Value | Meaning |
|-------|---------|
| `active` | The Zoho Databridge agent is connected |
| `inactive` | The agent is not reachable |

**`status`** (inside `tableDetails`) — [Get Datasources](get-datasources.md), snapshot entries only

| Value | Meaning |
|-------|---------|
| `active` | The snapshot schedule is running |
| `inactive` | The snapshot schedule is paused |

**`serviceName`** — see [`serviceName` values](update-datasource-connection.md#servicename-values) in [Update Datasource Connection](update-datasource-connection.md).

---

# CONFIG Attribute Availability by API

`✓` accepted and acted on, `–` not accepted or has no effect.

| Attribute | Sync Data | Refetch Data | Update Datasource Connection |
|-----------|:---------:|:------------:|:----------------------------:|
| `userName` | ✓ | ✓ | ✓ **mandatory** |
| `password` | ✓ | ✓ | ✓ |
| `syncIntervalId` | ✓ | – | – |
| `isFullFetch` | – | ✓ | – |
| `serviceName` | – | – | ✓ **mandatory** |
| `hostName` | – | – | ✓ **mandatory** |
| `databaseType` | – | – | ✓ conditional |
| `port`, `cloudDatabaseName`, `instanceName`, `schemaName` | – | – | ✓ |
| `warehouseName`, `s3OutputLocation`, `workgroupName`, `dataLocation`, `projectId`, `sId`, `catalogName`, `httpPath` | – | – | ✓ |
| `refreshToken`, `accessToken` | – | – | ✓ |
| `connectionString`, `authSource`, `connType` | – | – | ✓ MongoDB variants only |
| `useSSL`, `useSSLCertificate` | – | – | ✓ |
| `useSSH`, `sshTunnelHost`, `sshTunnelPort`, `sshTunnelUsername`, `sshTunnelPassword`, `sshTunnelAuthType` | – | – | ✓ |

[Get Datasources](get-datasources.md) and [Get Last Import Details](get-last-import-details.md) take no CONFIG attributes at all.

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [8077](../../../foundations/error-codes.md#error-8077) | 400 | EMPTYJSONCONFIGURATION — CONFIG was not sent, or was sent empty. |
| [8078](../../../foundations/error-codes.md#error-8078) | 400 | EMPTYJSONATTRIBUTEFOUND — A mandatory attribute was sent blank. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | A required attribute (expression or formulaName) is missing from CONFIG. |
| [8182](../../../foundations/error-codes.md#error-8182) | 403 | resetSort: true and sortOrder cannot be used together. |
| [8183](../../../foundations/error-codes.md#error-8183) | 400 | SCHEDULEIDNOTASSOCIATEDWITHCONNECTOR — The syncIntervalId does not belong to this datasource. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | LESSTHANMINOCCURANCE — CONFIG was not sent. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | MORETHANMAXLENGTH — roleName exceeds 30 characters, or permissions exceeds its size limit. |
| [8509](../../../foundations/error-codes.md#error-8509) | 400 | PATTERNNOTMATCHED — roleName contains disallowed characters, or accessType is not one of the three values. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |
| [18055](../../../foundations/error-codes.md#error-18055) | 400 | DBTYPESERVICENAMENOTMACHED — The databaseType is not available for the given serviceName. |
| [18056](../../../foundations/error-codes.md#error-18056) | 400 | NOSOURCEAVAILABLEFORTABLE — The table has no datasource behind it. |
| [18057](../../../foundations/error-codes.md#error-18057) | 400 | INVALIDCLOUDSERVICENAME — serviceName is not a recognised service. |
| [18061](../../../foundations/error-codes.md#error-18061) | 400 | CONNECTIONIDNOTASSOSIATEDFORWORKSPACE — The datasource ID does not exist in this workspace, or the source type cannot be synced this way (HTTP 404). |
| [18063](../../../foundations/error-codes.md#error-18063) | 400 | DBTYPECANNOTBEUPDATEDFORLIVECONNECTDB — databaseType differs from the stored one on a Live Connect database. |
| [18064](../../../foundations/error-codes.md#error-18064) | 400 | SERVICENAMECANNOTBEUPDATEDFORLIVECONNECTDB — serviceName differs from the stored one on a Live Connect database. |
| [18072](../../../foundations/error-codes.md#error-18072) | 400 | TABLESYNCINPROGRESS — A sync for this table is already running. |
| [18073](../../../foundations/error-codes.md#error-18073) | 400 | DATASOURCESYNCINPROGRESS — A sync for this datasource is already running. |

# Related

- [Data Operations](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
