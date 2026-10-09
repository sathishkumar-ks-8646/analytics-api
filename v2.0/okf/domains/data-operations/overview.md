---
type: API Domain
title: Data Operations
description: "API for Data Operations in Zoho Analytics — covering row operations, import/export workflows, and datasource sync/connectivity."
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - api-domain
api:
  domain: data-operations
  groups:
    - group: sync-data-import
      title: Synchronous Data Import
      doc: "/domains/data-operations/sync-data-import/overview.md"
      endpoint_count: 2
    - group: async-data-import
      title: Asynchronous & Batch Data Import
      doc: "/domains/data-operations/async-data-import/overview.md"
      endpoint_count: 5
    - group: sync-data-export
      title: Synchronous Data Export
      doc: "/domains/data-operations/sync-data-export/overview.md"
      endpoint_count: 1
    - group: async-data-export
      title: Asynchronous Data Export
      doc: "/domains/data-operations/async-data-export/overview.md"
      endpoint_count: 4
    - group: row-operations
      title: Row Operations
      doc: "/domains/data-operations/row-operations/overview.md"
      endpoint_count: 3
    - group: data-sync-and-connectivity
      title: Data Sync & Connectivity
      doc: "/domains/data-operations/data-sync-and-connectivity/overview.md"
      endpoint_count: 5
  endpoint_count: 20
  openapi: "/references/openapi/data-operations-grouped-api.json"
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

API for Data Operations in Zoho Analytics — covering row operations, import/export workflows, and datasource sync/connectivity.

# API Groups

| Group | Endpoints | Description |
|---|---|---|
| [Synchronous Data Import](sync-data-import/overview.md) | 2 | APIs for importing data directly into new or existing tables. |
| [Asynchronous & Batch Data Import](async-data-import/overview.md) | 5 | APIs for creating and monitoring asynchronous import jobs and batch imports. |
| [Synchronous Data Export](sync-data-export/overview.md) | 1 | APIs for exporting view data directly. |
| [Asynchronous Data Export](async-data-export/overview.md) | 4 | APIs for creating export jobs and downloading generated exports. |
| [Row Operations](row-operations/overview.md) | 3 | APIs for adding, updating, and deleting rows in a view. |
| [Data Sync & Connectivity](data-sync-and-connectivity/overview.md) | 5 | APIs for import history, datasource sync/refetch, datasource updates, and listing datasources. |

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Import Data into a New Table (Synchronous)](sync-data-import/import-data-new-table.md) | POST | `/restapi/v2/workspaces/{workspace-id}/data` | `importDataNewTable` | `ZohoAnalytics.data.create` | 200 |
| [Import Data into an Existing Table (Synchronous)](sync-data-import/import-data-existing-table.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data` | `importDataExistingTable` | `ZohoAnalytics.data.create` | 200 |
| [Create Import Job for a New Table (Asynchronous)](async-data-import/create-import-job-new-table.md) | POST | `/restapi/v2/bulk/workspaces/{workspace-id}/data` | `createImportJobNewTable` | `ZohoAnalytics.data.create` | 200 |
| [Create Import Job for an Existing Table (Asynchronous)](async-data-import/create-import-job-existing-table.md) | POST | `/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data` | `createImportJobExistingTable` | `ZohoAnalytics.data.create` | 200 |
| [Batch Import Data into New Table](async-data-import/batch-import-new-table.md) | POST | `/restapi/v2/bulk/workspaces/{workspace-id}/data/batch` | `batchImportNewTable` | `ZohoAnalytics.data.create` | 200 |
| [Batch Import Data into Existing Table](async-data-import/batch-import-existing-table.md) | POST | `/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data/batch` | `batchImportExistingTable` | `ZohoAnalytics.data.create` | 200 |
| [Get Import Job Details](async-data-import/get-import-job-details.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/importjobs/{job-id}` | `getImportJobDetails` | `ZohoAnalytics.data.create` | 200 |
| [Export Data from a View](sync-data-export/export-data-view.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data` | `exportDataView` | `ZohoAnalytics.data.read` | 200 |
| [Create Export Job using SQL Query (Asynchronous)](async-data-export/create-export-job-sql-query.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/data` | `createExportJobSQLQuery` | `ZohoAnalytics.data.read` | 200 |
| [Create Export Job using View ID (Asynchronous)](async-data-export/create-export-job-view-id.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data` | `createExportJobViewId` | `ZohoAnalytics.data.read` | 200 |
| [Get Export Job Details](async-data-export/get-export-job-details.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/exportjobs/{job-id}` | `getExportJobDetails` | `ZohoAnalytics.data.read` | 200 |
| [Download Exported Data](async-data-export/download-exported-data.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/exportjobs/{job-id}/data` | `downloadExportedData` | `ZohoAnalytics.data.read` | 200 |
| [Add Row](row-operations/add-row.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows` | `addRow` | `ZohoAnalytics.data.create` | 200 |
| [Update Row](row-operations/update-rows.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows` | `updateRows` | `ZohoAnalytics.data.update` | 200 |
| [Delete Row](row-operations/delete-rows.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows` | `deleteRows` | `ZohoAnalytics.data.delete` | 200 |
| [Sync Data](data-sync-and-connectivity/sync-datasource.md) | POST | `/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}/sync` | `syncDatasource` | `ZohoAnalytics.metadata.create` | 204 |
| [Refetch Data](data-sync-and-connectivity/refetch-datasource.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/sync` | `refetchDatasource` | `ZohoAnalytics.metadata.create` | 204 |
| [Update Datasource Connection](data-sync-and-connectivity/update-datasource-connection.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}` | `updateDatasourceConnection` | `ZohoAnalytics.metadata.update` | 204 |
| [Get Datasources](data-sync-and-connectivity/get-datasources.md) | GET | `/restapi/v2/workspaces/{workspace-id}/datasources` | `getDatasources` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Last Import Details](data-sync-and-connectivity/get-last-import-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/importdetails` | `getLastImportDetails` | `ZohoAnalytics.metadata.read` | 200 |

# Related

- [All domains](../index.md)
- [OpenAPI specification for this domain](../../references/openapi/data-operations-grouped-api.json)
- [Foundations](../../foundations/index.md)
