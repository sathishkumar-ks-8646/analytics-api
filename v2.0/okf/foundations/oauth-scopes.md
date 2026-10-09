---
type: Reference
title: OAuth scopes
description: "All Zoho Analytics OAuth 2.0 scopes, what each family covers, and which REST API v2 operations require each scope."
tags:
  - zoho-analytics
  - rest-api-v2
  - oauth
  - scopes
  - authentication
scope_count: 31
scopes:
  - ZohoAnalytics.data.read
  - ZohoAnalytics.data.create
  - ZohoAnalytics.data.update
  - ZohoAnalytics.data.delete
  - ZohoAnalytics.data.all
  - ZohoAnalytics.modeling.read
  - ZohoAnalytics.modeling.create
  - ZohoAnalytics.modeling.update
  - ZohoAnalytics.modeling.delete
  - ZohoAnalytics.modeling.all
  - ZohoAnalytics.metadata.read
  - ZohoAnalytics.metadata.create
  - ZohoAnalytics.metadata.update
  - ZohoAnalytics.metadata.delete
  - ZohoAnalytics.metadata.all
  - ZohoAnalytics.share.read
  - ZohoAnalytics.share.create
  - ZohoAnalytics.share.update
  - ZohoAnalytics.share.delete
  - ZohoAnalytics.share.all
  - ZohoAnalytics.embed.read
  - ZohoAnalytics.embed.create
  - ZohoAnalytics.embed.update
  - ZohoAnalytics.embed.delete
  - ZohoAnalytics.embed.all
  - ZohoAnalytics.usermanagement.read
  - ZohoAnalytics.usermanagement.create
  - ZohoAnalytics.usermanagement.update
  - ZohoAnalytics.usermanagement.delete
  - ZohoAnalytics.usermanagement.all
  - ZohoAnalytics.fullaccess.all
sources:
  - id: openapi-common
    resource: "/references/openapi/zoho-analytics-api-common.json"
    title: "Shared OpenAPI components (scopes, error envelope)"
    author: team:zoho-analytics-api-docs
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Zoho Analytics scopes follow the pattern `ZohoAnalytics.<family>.<operation>`. The `<operation>` is one of `read`, `create`, `update`, `delete`, or `all` (every operation of that family). `ZohoAnalytics.fullaccess.all` grants every family. Request only the scopes your integration needs; an access token missing the required scope fails with error [`8535`](error-codes.md#error-8535) (`INVALID_OAUTHTOKEN`).

Scopes are requested during the OAuth authorization step (see [Authentication](authentication.md)) as a comma-separated `scope` parameter, for example `ZohoAnalytics.data.read,ZohoAnalytics.metadata.read`.

# Scope Families

| Family | Covers |
|---|---|
| `data` | Row data: import, export, add/update/delete rows, sync and refetch. |
| `modeling` | Schema objects: tables, columns, lookups, query tables, formulas, variables. |
| `metadata` | Read-only metadata: organizations, workspaces, views, folders, trash, dependents. |
| `share` | Sharing, publishing, private/public URLs, slideshows, groups, workspace users. |
| `embed` | Embed URLs for Embedded Analytics (OEM) customers. |
| `usermanagement` | Organization users, roles, subscription and resource usage. |
| `fullaccess` | Everything above. |

# Scopes

| Scope | Description | Operations |
|---|---|---|
| [`ZohoAnalytics.data.read`](#zohoanalyticsdataread) | Read data from Zoho Analytics. | 5 |
| [`ZohoAnalytics.data.create`](#zohoanalyticsdatacreate) | Create data in Zoho Analytics. | 8 |
| [`ZohoAnalytics.data.update`](#zohoanalyticsdataupdate) | Update data in Zoho Analytics. | 1 |
| [`ZohoAnalytics.data.delete`](#zohoanalyticsdatadelete) | Delete data from Zoho Analytics. | 1 |
| [`ZohoAnalytics.data.all`](#zohoanalyticsdataall) | Full access to data in Zoho Analytics. | 0 |
| [`ZohoAnalytics.modeling.read`](#zohoanalyticsmodelingread) | Read modeling objects in Zoho Analytics. | 4 |
| [`ZohoAnalytics.modeling.create`](#zohoanalyticsmodelingcreate) | Create modeling objects in Zoho Analytics. | 27 |
| [`ZohoAnalytics.modeling.update`](#zohoanalyticsmodelingupdate) | Update modeling objects in Zoho Analytics. | 23 |
| [`ZohoAnalytics.modeling.delete`](#zohoanalyticsmodelingdelete) | Delete modeling objects in Zoho Analytics. | 15 |
| [`ZohoAnalytics.modeling.all`](#zohoanalyticsmodelingall) | Full access to modeling objects in Zoho Analytics. | 0 |
| [`ZohoAnalytics.metadata.read`](#zohoanalyticsmetadataread) | Read metadata from Zoho Analytics. | 36 |
| [`ZohoAnalytics.metadata.create`](#zohoanalyticsmetadatacreate) | Create metadata in Zoho Analytics. | 2 |
| [`ZohoAnalytics.metadata.update`](#zohoanalyticsmetadataupdate) | Update metadata in Zoho Analytics. | 9 |
| [`ZohoAnalytics.metadata.delete`](#zohoanalyticsmetadatadelete) | Delete metadata from Zoho Analytics. | 0 |
| [`ZohoAnalytics.metadata.all`](#zohoanalyticsmetadataall) | Full access to metadata in Zoho Analytics. | 0 |
| [`ZohoAnalytics.share.read`](#zohoanalyticsshareread) | Read shared items in Zoho Analytics. | 7 |
| [`ZohoAnalytics.share.create`](#zohoanalyticssharecreate) | Create shared items in Zoho Analytics. | 4 |
| [`ZohoAnalytics.share.update`](#zohoanalyticsshareupdate) | Update shared items in Zoho Analytics. | 2 |
| [`ZohoAnalytics.share.delete`](#zohoanalyticssharedelete) | Delete shared items in Zoho Analytics. | 4 |
| [`ZohoAnalytics.share.all`](#zohoanalyticsshareall) | Full access to shared items in Zoho Analytics. | 0 |
| [`ZohoAnalytics.embed.read`](#zohoanalyticsembedread) | Read embedded content from Zoho Analytics. | 7 |
| [`ZohoAnalytics.embed.create`](#zohoanalyticsembedcreate) | Create embedded content in Zoho Analytics. | 2 |
| [`ZohoAnalytics.embed.update`](#zohoanalyticsembedupdate) | Update embedded content in Zoho Analytics. | 3 |
| [`ZohoAnalytics.embed.delete`](#zohoanalyticsembeddelete) | Delete embedded content in Zoho Analytics. | 3 |
| [`ZohoAnalytics.embed.all`](#zohoanalyticsembedall) | Full access to embedded content in Zoho Analytics. | 0 |
| [`ZohoAnalytics.usermanagement.read`](#zohoanalyticsusermanagementread) | Read user management data in Zoho Analytics. | 5 |
| [`ZohoAnalytics.usermanagement.create`](#zohoanalyticsusermanagementcreate) | Create user management data in Zoho Analytics. | 3 |
| [`ZohoAnalytics.usermanagement.update`](#zohoanalyticsusermanagementupdate) | Update user management data in Zoho Analytics. | 6 |
| [`ZohoAnalytics.usermanagement.delete`](#zohoanalyticsusermanagementdelete) | Delete user management data in Zoho Analytics. | 3 |
| [`ZohoAnalytics.usermanagement.all`](#zohoanalyticsusermanagementall) | Full access to user management in Zoho Analytics. | 0 |
| [`ZohoAnalytics.fullaccess.all`](#zohoanalyticsfullaccessall) | Full access to all Zoho Analytics features. | 0 |

# Operations per Scope

## ZohoAnalytics.data.read

Read data from Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Export Data from a View](../domains/data-operations/sync-data-export/export-data-view.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data` |
| [Create Export Job using SQL Query (Asynchronous)](../domains/data-operations/async-data-export/create-export-job-sql-query.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/data` |
| [Create Export Job using View ID (Asynchronous)](../domains/data-operations/async-data-export/create-export-job-view-id.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data` |
| [Get Export Job Details](../domains/data-operations/async-data-export/get-export-job-details.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/exportjobs/{job-id}` |
| [Download Exported Data](../domains/data-operations/async-data-export/download-exported-data.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/exportjobs/{job-id}/data` |

## ZohoAnalytics.data.create

Create data in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Import Data into a New Table (Synchronous)](../domains/data-operations/sync-data-import/import-data-new-table.md) | POST | `/restapi/v2/workspaces/{workspace-id}/data` |
| [Import Data into an Existing Table (Synchronous)](../domains/data-operations/sync-data-import/import-data-existing-table.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data` |
| [Create Import Job for a New Table (Asynchronous)](../domains/data-operations/async-data-import/create-import-job-new-table.md) | POST | `/restapi/v2/bulk/workspaces/{workspace-id}/data` |
| [Create Import Job for an Existing Table (Asynchronous)](../domains/data-operations/async-data-import/create-import-job-existing-table.md) | POST | `/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data` |
| [Batch Import Data into New Table](../domains/data-operations/async-data-import/batch-import-new-table.md) | POST | `/restapi/v2/bulk/workspaces/{workspace-id}/data/batch` |
| [Batch Import Data into Existing Table](../domains/data-operations/async-data-import/batch-import-existing-table.md) | POST | `/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data/batch` |
| [Get Import Job Details](../domains/data-operations/async-data-import/get-import-job-details.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/importjobs/{job-id}` |
| [Add Row](../domains/data-operations/row-operations/add-row.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows` |

## ZohoAnalytics.data.update

Update data in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Update Row](../domains/data-operations/row-operations/update-rows.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows` |

## ZohoAnalytics.data.delete

Delete data from Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Delete Row](../domains/data-operations/row-operations/delete-rows.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows` |

## ZohoAnalytics.data.all

Full access to data in Zoho Analytics.

No documented v2 operation declares this scope directly. `.all` scopes satisfy any operation of the same family; `fullaccess.all` satisfies every operation.

## ZohoAnalytics.modeling.read

Read modeling objects in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Get Variables](../domains/data-modeling-and-schema/workspace-variables/get-variables.md) | GET | `/restapi/v2/workspaces/{workspace-id}/variables` |
| [Get Variable Details](../domains/data-modeling-and-schema/workspace-variables/get-variable-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}` |
| [Get Report Metadata](../domains/reports-and-dashboards/reports/get-report-metadata.md) | GET | `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata` |
| [Get Dashboard Metadata](../domains/reports-and-dashboards/dashboards/get-dashboard-metadata.md) | GET | `/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}/metadata` |

## ZohoAnalytics.modeling.create

Create modeling objects in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Create Workspace](../domains/workspace-management/workspace-operations/create-workspace.md) | POST | `/restapi/v2/workspaces` |
| [Copy Workspace](../domains/workspace-management/workspace-operations/copy-workspace.md) | POST | `/restapi/v2/workspaces/{workspace-id}` |
| [Create Folder](../domains/workspace-management/workspace-folders/create-folder.md) | POST | `/restapi/v2/workspaces/{workspace-id}/folders` |
| [Create Table](../domains/data-modeling-and-schema/table-and-schema/create-table.md) | POST | `/restapi/v2/workspaces/{workspace-id}/tables` |
| [Add Column](../domains/data-modeling-and-schema/columns/add-column.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns` |
| [Create Query Table](../domains/data-modeling-and-schema/query-tables/create-query-table.md) | POST | `/restapi/v2/workspaces/{workspace-id}/querytables` |
| [Add Custom Formula](../domains/data-modeling-and-schema/formula-columns/add-formula-column.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas` |
| [Copy Custom Formulas](../domains/data-modeling-and-schema/formula-columns/copy-formulas.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/formulas/copy` |
| [Add Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/add-aggregate-formula.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas` |
| [Create Variable](../domains/data-modeling-and-schema/workspace-variables/create-variable.md) | POST | `/restapi/v2/workspaces/{workspace-id}/variables` |
| [Save As View](../domains/views-management/view-operations/save-as-view.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/saveas` |
| [Copy Views](../domains/views-management/view-operations/copy-views.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/copy` |
| [Create Similar Views](../domains/views-management/view-operations/create-similar-views.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/similarviews` |
| [Restore Trash View](../domains/views-management/trash-management/restore-trash-view.md) | POST | `/restapi/v2/workspaces/{workspace-id}/trash/{view-id}` |
| [Auto Analyse View](../domains/views-management/auto-analysis/auto-analyse-view.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/autoanalyse` |
| [Auto Analyse Column](../domains/views-management/auto-analysis/auto-analyse-column.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/autoanalyse` |
| [Create Tag](../domains/views-management/tags/create-tag.md) | POST | `/restapi/v2/workspaces/{workspace-id}/tags` |
| [Add Tag To Multiple Views](../domains/views-management/tags/add-tag-to-views.md) | POST | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views` |
| [Add Multiple Tags To View](../domains/views-management/tags/add-tags-to-view.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags` |
| [Create Analysis View](../domains/reports-and-dashboards/reports/create-report.md) | POST | `/restapi/v2/workspaces/{workspace-id}/reports` |
| [Create Dashboard](../domains/reports-and-dashboards/dashboards/create-dashboard.md) | POST | `/restapi/v2/workspaces/{workspace-id}/dashboards` |
| [Create Email Schedule](../domains/schedules-and-alerts/email-schedules/create-email-schedule.md) | POST | `/restapi/v2/workspaces/{workspace-id}/emailschedules` |
| [Trigger Email Schedule](../domains/schedules-and-alerts/email-schedules/trigger-email-schedule.md) | POST | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}` |
| [Create AutoML Analysis](../domains/dsml/automl/create-auto-ml-analysis.md) | POST | `/restapi/v2/automl/workspaces/{workspace-id}/analysis` |
| [Create AutoML Analysis Deployment](../domains/dsml/automl/create-auto-ml-analysis-deployment.md) | POST | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments` |
| [Run AutoML Analysis](../domains/dsml/automl/run-auto-ml-analysis.md) | POST | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}/execute` |
| [AutoML What If Analysis](../domains/dsml/automl/auto-ml-what-if-analysis.md) | POST | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/whatif` |

## ZohoAnalytics.modeling.update

Update modeling objects in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Rename Workspace](../domains/workspace-management/workspace-operations/rename-workspace.md) | PUT | `/restapi/v2/workspaces/{workspace-id}` |
| [Rename Folder](../domains/workspace-management/workspace-folders/rename-folder.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}` |
| [Change Folder Hierarchy](../domains/workspace-management/workspace-folders/change-folder-hierarchy.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/move` |
| [Change Folder Position](../domains/workspace-management/workspace-folders/change-folder-position.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/reorder` |
| [Move Views To Folder](../domains/workspace-management/workspace-folders/move-views-to-folder.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/movetofolder` |
| [Make Default Folder](../domains/workspace-management/workspace-folders/make-default-folder.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/default` |
| [Rename Column](../domains/data-modeling-and-schema/columns/rename-column.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}` |
| [Hide Columns](../domains/data-modeling-and-schema/columns/hide-columns.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/hide` |
| [Show Columns](../domains/data-modeling-and-schema/columns/show-columns.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/show` |
| [Sort Data by Columns](../domains/data-modeling-and-schema/columns/sort-data-by-columns.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data/sort` |
| [Reorder Columns](../domains/data-modeling-and-schema/columns/reorder-columns.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/reorder` |
| [Add Lookup](../domains/data-modeling-and-schema/lookups-and-relationships/add-lookup.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup` |
| [Remove Lookup](../domains/data-modeling-and-schema/lookups-and-relationships/remove-lookup.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup` |
| [Edit Query Table](../domains/data-modeling-and-schema/query-tables/edit-query-table.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}` |
| [Edit Custom Formula](../domains/data-modeling-and-schema/formula-columns/edit-formula-column.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas/{formula-id}` |
| [Edit Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/edit-aggregate-formula.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas/{formula-id}` |
| [Edit Variable](../domains/data-modeling-and-schema/workspace-variables/update-variable.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}` |
| [Rename View](../domains/views-management/view-operations/rename-view.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}` |
| [Update Tag](../domains/views-management/tags/update-tag.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}` |
| [Update Analysis View](../domains/reports-and-dashboards/reports/update-report.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}` |
| [Update Dashboard](../domains/reports-and-dashboards/dashboards/update-dashboard.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}` |
| [Update Email Schedule](../domains/schedules-and-alerts/email-schedules/update-email-schedule.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}` |
| [Change Email Schedule Status](../domains/schedules-and-alerts/email-schedules/change-email-schedule-status.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}/status` |

## ZohoAnalytics.modeling.delete

Delete modeling objects in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Delete Workspace](../domains/workspace-management/workspace-operations/delete-workspace.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}` |
| [Delete Folder](../domains/workspace-management/workspace-folders/delete-folder.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}` |
| [Delete Column](../domains/data-modeling-and-schema/columns/delete-column.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}` |
| [Delete Custom Formula](../domains/data-modeling-and-schema/formula-columns/delete-formula-column.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas/{formula-id}` |
| [Delete Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/delete-aggregate-formula.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas/{formula-id}` |
| [Delete Variable](../domains/data-modeling-and-schema/workspace-variables/delete-variable.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}` |
| [Delete View](../domains/views-management/view-operations/delete-view.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}` |
| [Delete Trash View](../domains/views-management/trash-management/delete-trash-view.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/trash/{view-id}` |
| [Delete Tag](../domains/views-management/tags/delete-tag.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}` |
| [Remove Tag From Multiple Views](../domains/views-management/tags/remove-tag-from-views.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views` |
| [Remove Multiple Tags From View](../domains/views-management/tags/remove-tags-from-view.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags` |
| [Delete Email Schedule](../domains/schedules-and-alerts/email-schedules/delete-email-schedule.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}` |
| [Delete AutoML Analysis](../domains/dsml/automl/delete-auto-ml-analysis.md) | DELETE | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}` |
| [Delete AutoML Analysis Model](../domains/dsml/automl/delete-auto-ml-analysis-model.md) | DELETE | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}` |
| [Delete AutoML Analysis Model Deployment](../domains/dsml/automl/delete-auto-ml-analysis-model-deployment.md) | DELETE | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}` |

## ZohoAnalytics.modeling.all

Full access to modeling objects in Zoho Analytics.

No documented v2 operation declares this scope directly. `.all` scopes satisfy any operation of the same family; `fullaccess.all` satisfies every operation.

## ZohoAnalytics.metadata.read

Read metadata from Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Get Org List](../domains/organization-management/org-info-and-settings/get-organizations.md) | GET | `/restapi/v2/orgs` |
| [Get Meta Details From Name](../domains/organization-management/org-info-and-settings/get-meta-details.md) | GET | `/restapi/v2/metadetails` |
| [Export as Template](../domains/workspace-management/workspace-operations/export-as-template.md) | GET | `/restapi/v2/workspaces/{workspace-id}/template/data` |
| [Get All Workspace List](../domains/workspace-management/workspace-operations/get-all-workspaces.md) | GET | `/restapi/v2/workspaces` |
| [Get Owned Workspace List](../domains/workspace-management/workspace-operations/get-owned-workspaces.md) | GET | `/restapi/v2/workspaces/owned` |
| [Get Shared Workspace List](../domains/workspace-management/workspace-operations/get-shared-workspaces.md) | GET | `/restapi/v2/workspaces/shared` |
| [Get Workspace Secret Key](../domains/workspace-management/workspace-operations/get-workspace-secret-key.md) | GET | `/restapi/v2/workspaces/{workspace-id}/secretkey` |
| [Get Workspace Info](../domains/workspace-management/workspace-operations/get-workspace-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}` |
| [Get Folder List](../domains/workspace-management/workspace-folders/get-folders.md) | GET | `/restapi/v2/workspaces/{workspace-id}/folders` |
| [Get Table Metadata](../domains/data-modeling-and-schema/table-and-schema/get-table-metadata.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/metadata` |
| [Get Column Dependents](../domains/data-modeling-and-schema/columns/get-column-dependents.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/dependents` |
| [Get Query Tables](../domains/data-modeling-and-schema/query-tables/get-query-tables.md) | GET | `/restapi/v2/workspaces/{workspace-id}/querytables` |
| [Get Query Table Details](../domains/data-modeling-and-schema/query-tables/get-query-table-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}` |
| [Get Custom Formulas](../domains/data-modeling-and-schema/formula-columns/get-custom-formula-list.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas` |
| [Get Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-list.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas` |
| [Get Unified Metrics in Workspace](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formulas-in-workspace.md) | GET | `/restapi/v2/workspaces/{workspace-id}/aggregateformulas` |
| [Get Aggregate Formula Dependents](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-dependents.md) | GET | `/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/dependents` |
| [Get Aggregate Formula Value](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-value.md) | GET | `/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/value` |
| [Get Datasources](../domains/data-operations/data-sync-and-connectivity/get-datasources.md) | GET | `/restapi/v2/workspaces/{workspace-id}/datasources` |
| [Get Last Import Details](../domains/data-operations/data-sync-and-connectivity/get-last-import-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/importdetails` |
| [Get View List](../domains/views-management/view-operations/get-views.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views` |
| [Get View Details](../domains/views-management/view-operations/get-view-details.md) | GET | `/restapi/v2/views/{view-id}` |
| [Get View Dependents](../domains/views-management/view-operations/get-view-dependents.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/dependents` |
| [Get Recent Views](../domains/views-management/view-operations/get-recent-views.md) | GET | `/restapi/v2/recentviews` |
| [Get Trash Views](../domains/views-management/trash-management/get-trash-views.md) | GET | `/restapi/v2/workspaces/{workspace-id}/trash` |
| [Get Tags List](../domains/views-management/tags/get-tags.md) | GET | `/restapi/v2/workspaces/{workspace-id}/tags` |
| [Get Tagged Views](../domains/views-management/tags/get-tagged-views.md) | GET | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views` |
| [Get View Tags](../domains/views-management/tags/get-view-tags.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags` |
| [Get All Dashboards](../domains/reports-and-dashboards/dashboards/get-dashboards.md) | GET | `/restapi/v2/dashboards` |
| [Get Owned Dashboards](../domains/reports-and-dashboards/dashboards/get-owned-dashboards.md) | GET | `/restapi/v2/dashboards/owned` |
| [Get Shared Dashboards](../domains/reports-and-dashboards/dashboards/get-shared-dashboards.md) | GET | `/restapi/v2/dashboards/shared` |
| [Get Email Schedules](../domains/schedules-and-alerts/email-schedules/get-email-schedules.md) | GET | `/restapi/v2/workspaces/{workspace-id}/emailschedules` |
| [Get AutoML Analysis In Org](../domains/dsml/automl/get-auto-ml-analysis-in-org.md) | GET | `/restapi/v2/automl/analysis` |
| [Get AutoML Analysis In Workspace](../domains/dsml/automl/get-auto-ml-analysis-in-workspace.md) | GET | `/restapi/v2/automl/workspaces/{workspace-id}/analysis` |
| [Get AutoML Analysis Details](../domains/dsml/automl/get-auto-ml-analysis-details.md) | GET | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}` |
| [Get Deployments For A Model](../domains/dsml/automl/get-deployments-for-model.md) | GET | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments` |

## ZohoAnalytics.metadata.create

Create metadata in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Sync Data](../domains/data-operations/data-sync-and-connectivity/sync-datasource.md) | POST | `/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}/sync` |
| [Refetch Data](../domains/data-operations/data-sync-and-connectivity/refetch-datasource.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/sync` |

## ZohoAnalytics.metadata.update

Update metadata in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Add Default Workspace](../domains/workspace-management/workspace-preferences/add-default-workspace.md) | POST | `/restapi/v2/workspaces/{workspace-id}/default` |
| [Remove Default Workspace](../domains/workspace-management/workspace-preferences/remove-default-workspace.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/default` |
| [Add Favourite Workspace](../domains/workspace-management/workspace-preferences/add-favorite-workspace.md) | POST | `/restapi/v2/workspaces/{workspace-id}/favorite` |
| [Remove Favourite Workspace](../domains/workspace-management/workspace-preferences/remove-favorite-workspace.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/favorite` |
| [Enable Workspace for Domain Access](../domains/workspace-management/domain-and-white-label/enable-domain-workspace.md) | POST | `/restapi/v2/workspaces/{workspace-id}/wlaccess` |
| [Disable Workspace for Domain Access](../domains/workspace-management/domain-and-white-label/disable-domain-workspace.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/wlaccess` |
| [Update Datasource Connection](../domains/data-operations/data-sync-and-connectivity/update-datasource-connection.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}` |
| [Add Favourite View](../domains/views-management/view-preferences/add-favorite-view.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/favorite` |
| [Remove Favourite View](../domains/views-management/view-preferences/remove-favorite-view.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/favorite` |

## ZohoAnalytics.metadata.delete

Delete metadata from Zoho Analytics.

No documented v2 operation declares this scope directly. `.all` scopes satisfy any operation of the same family; `fullaccess.all` satisfies every operation.

## ZohoAnalytics.metadata.all

Full access to metadata in Zoho Analytics.

No documented v2 operation declares this scope directly. `.all` scopes satisfy any operation of the same family; `fullaccess.all` satisfies every operation.

## ZohoAnalytics.share.read

Read shared items in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Get Org Admins](../domains/users-and-groups/org-users/get-org-admins.md) | GET | `/restapi/v2/orgadmins` |
| [Get Workspace Admins](../domains/users-and-groups/workspace-users/get-workspace-admins.md) | GET | `/restapi/v2/workspaces/{workspace-id}/admins` |
| [Get Group List](../domains/users-and-groups/workspace-groups/get-groups.md) | GET | `/restapi/v2/workspaces/{workspace-id}/groups` |
| [Get Group Details](../domains/users-and-groups/workspace-groups/get-group-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}` |
| [Get Workspace Shared Details](../domains/share-and-publish/sharing/get-workspace-shared-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/share` |
| [Get Shared Details](../domains/share-and-publish/sharing/get-shared-details-for-views.md) | GET | `/restapi/v2/workspaces/{workspace-id}/share/shareddetails` |
| [Get My Permissions](../domains/share-and-publish/sharing/get-user-permissions.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share/mypermissions` |

## ZohoAnalytics.share.create

Create shared items in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Add Workspace Admins](../domains/users-and-groups/workspace-users/add-workspace-admins.md) | POST | `/restapi/v2/workspaces/{workspace-id}/admins` |
| [Create Group](../domains/users-and-groups/workspace-groups/create-group.md) | POST | `/restapi/v2/workspaces/{workspace-id}/groups` |
| [Add Group Members](../domains/users-and-groups/workspace-groups/add-group-members.md) | POST | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members` |
| [Share Views](../domains/share-and-publish/sharing/share-views.md) | POST | `/restapi/v2/workspaces/{workspace-id}/share` |

## ZohoAnalytics.share.update

Update shared items in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Rename Group](../domains/users-and-groups/workspace-groups/rename-group.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}` |
| [Update Shared Details](../domains/share-and-publish/sharing/update-shared-details-for-view.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share` |

## ZohoAnalytics.share.delete

Delete shared items in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Remove Workspace Admins](../domains/users-and-groups/workspace-users/remove-workspace-admins.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/admins` |
| [Remove Group Members](../domains/users-and-groups/workspace-groups/remove-group-members.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members` |
| [Delete Group](../domains/users-and-groups/workspace-groups/delete-group.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}` |
| [Remove Shared Views](../domains/share-and-publish/sharing/remove-share.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/share` |

## ZohoAnalytics.share.all

Full access to shared items in Zoho Analytics.

No documented v2 operation declares this scope directly. `.all` scopes satisfy any operation of the same family; `fullaccess.all` satisfies every operation.

## ZohoAnalytics.embed.read

Read embedded content from Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Get View URL](../domains/views-management/view-operations/get-view-url.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish` |
| [Get Private URL](../domains/share-and-publish/publish/get-private-url.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink` |
| [Get Publish Configurations](../domains/share-and-publish/publish/get-publish-configurations.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config` |
| [Get Embed URL](../domains/share-and-publish/embed-url/get-embed-url.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embed` |
| [Get Slide List](../domains/share-and-publish/slideshow-management/get-slideshows.md) | GET | `/restapi/v2/workspaces/{workspace-id}/slides` |
| [Get Slide URL](../domains/share-and-publish/slideshow-management/get-slideshow-url.md) | GET | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}/publish` |
| [Get Slide Info](../domains/share-and-publish/slideshow-management/get-slideshow-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}` |

## ZohoAnalytics.embed.create

Create embedded content in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Make View Public](../domains/share-and-publish/publish/make-views-public.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/public` |
| [Create Slide Show](../domains/share-and-publish/slideshow-management/create-slideshow.md) | POST | `/restapi/v2/workspaces/{workspace-id}/slides` |

## ZohoAnalytics.embed.update

Update embedded content in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Create Private URL](../domains/share-and-publish/publish/create-private-url.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink` |
| [Update Publish Configurations](../domains/share-and-publish/publish/update-publish-configurations.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config` |
| [Update Slide Show](../domains/share-and-publish/slideshow-management/update-slideshow.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}` |

## ZohoAnalytics.embed.delete

Delete embedded content in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Remove Public Permission](../domains/share-and-publish/publish/remove-public-permission.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/public` |
| [Remove Private Access](../domains/share-and-publish/publish/remove-private-access.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink` |
| [Delete Slide Show](../domains/share-and-publish/slideshow-management/delete-slideshow.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}` |

## ZohoAnalytics.embed.all

Full access to embedded content in Zoho Analytics.

No documented v2 operation declares this scope directly. `.all` scopes satisfy any operation of the same family; `fullaccess.all` satisfies every operation.

## ZohoAnalytics.usermanagement.read

Read user management data in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Get Resource Details](../domains/organization-management/org-info-and-settings/get-resource-details.md) | GET | `/restapi/v2/resources` |
| [Get Subscription Details](../domains/organization-management/org-info-and-settings/get-subscription-details.md) | GET | `/restapi/v2/subscription` |
| [Get Users](../domains/users-and-groups/org-users/get-users.md) | GET | `/restapi/v2/users` |
| [Get Custom Roles](../domains/users-and-groups/custom-roles/get-custom-roles.md) | GET | `/restapi/v2/orgs/roles` |
| [Get Workspace Users](../domains/users-and-groups/workspace-users/get-workspace-users.md) | GET | `/restapi/v2/workspaces/{workspace-id}/users` |

## ZohoAnalytics.usermanagement.create

Create user management data in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Add Users](../domains/users-and-groups/org-users/add-users.md) | POST | `/restapi/v2/users` |
| [Create Custom Role](../domains/users-and-groups/custom-roles/create-custom-role.md) | POST | `/restapi/v2/orgs/roles` |
| [Add Workspace Users](../domains/users-and-groups/workspace-users/add-workspace-users.md) | POST | `/restapi/v2/workspaces/{workspace-id}/users` |

## ZohoAnalytics.usermanagement.update

Update user management data in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Activate Users](../domains/users-and-groups/org-users/activate-users.md) | PUT | `/restapi/v2/users/active` |
| [Deactivate Users](../domains/users-and-groups/org-users/de-activate-users.md) | PUT | `/restapi/v2/users/inactive` |
| [Change User Role](../domains/users-and-groups/org-users/change-user-role.md) | PUT | `/restapi/v2/users/role` |
| [Update Custom Role](../domains/users-and-groups/custom-roles/update-custom-role.md) | PUT | `/restapi/v2/orgs/roles/{role-id}` |
| [Change Workspace Users Status](../domains/users-and-groups/workspace-users/change-workspace-users-status.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/users/status` |
| [Change Workspace Users Role](../domains/users-and-groups/workspace-users/change-workspace-users-role.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/users/role` |

## ZohoAnalytics.usermanagement.delete

Delete user management data in Zoho Analytics.

| Operation | Method | Path |
|---|---|---|
| [Remove Users](../domains/users-and-groups/org-users/remove-users.md) | DELETE | `/restapi/v2/users` |
| [Delete Custom Role](../domains/users-and-groups/custom-roles/delete-custom-role.md) | DELETE | `/restapi/v2/orgs/roles/{role-id}` |
| [Remove Workspace Users](../domains/users-and-groups/workspace-users/delete-workspace-users.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/users` |

## ZohoAnalytics.usermanagement.all

Full access to user management in Zoho Analytics.

No documented v2 operation declares this scope directly. `.all` scopes satisfy any operation of the same family; `fullaccess.all` satisfies every operation.

## ZohoAnalytics.fullaccess.all

Full access to all Zoho Analytics features.

No documented v2 operation declares this scope directly. `.all` scopes satisfy any operation of the same family; `fullaccess.all` satisfies every operation.

# Related

- [Authentication](authentication.md)
- [Permission matrix](permission-matrix.md)
