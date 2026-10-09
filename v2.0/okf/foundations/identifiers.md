---
type: Reference
title: Identifiers and how to obtain them
description: "Every identifier used in Zoho Analytics REST API v2 paths and headers (organization, workspace, view, column, job, schedule and more), its format, and the operations that return it."
tags:
  - zoho-analytics
  - rest-api-v2
  - identifiers
  - ids
  - path-parameters
sources:
  - id: openapi-spec
    resource: "/references/openapi/org-management-grouped-api.json"
    title: OpenAPI 3 specification - org-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
  - id: openapi-spec
    resource: "/references/openapi/user-groups-grouped-api.json"
    title: OpenAPI 3 specification - user-groups-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
  - id: openapi-spec
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
  - id: openapi-spec
    resource: "/references/openapi/data-operations-grouped-api.json"
    title: OpenAPI 3 specification - data-operations-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
  - id: openapi-spec
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
  - id: openapi-spec
    resource: "/references/openapi/share-publish-grouped-api.json"
    title: OpenAPI 3 specification - share-publish-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
  - id: openapi-spec
    resource: "/references/openapi/schedules-alerts-grouped-api.json"
    title: OpenAPI 3 specification - schedules-alerts-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
  - id: openapi-spec
    resource: "/references/openapi/dsml-grouped-api.json"
    title: OpenAPI 3 specification - dsml-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

All identifiers are numeric but are transmitted as **strings** (JSON strings in responses, plain text in URL paths and headers). Treat them as opaque strings; never parse them as 32-bit integers, because view and workspace IDs exceed that range. Identifiers are stable for the lifetime of the object but differ across data centers and environments, so resolve them at runtime rather than hard-coding them. The recommended bootstrap sequence is:

1. Call [Get Org List](../domains/organization-management/org-info-and-settings/get-organizations.md) to obtain `orgId` for the `ZANALYTICS-ORGID` header.
2. Call [Get Meta Details From Name](../domains/organization-management/org-info-and-settings/get-meta-details.md) to resolve a workspace name (and optionally a view name) into `workspaceId` and `viewId`.
3. Use listing APIs (views, columns, folders, groups, schedules...) to obtain the remaining IDs.

# Identifiers

## ZANALYTICS-ORGID

- **What it is:** Organization ID
- **Where it is sent:** HTTP header.
- **OpenAPI description:** ID of the organisation on which the operation has to be performed. The organisation ID can be obtained using the Get Organizations API.

- **Obtained from:** [Get Org List](../domains/organization-management/org-info-and-settings/get-organizations.md), [Get Meta Details From Name](../domains/organization-management/org-info-and-settings/get-meta-details.md).

- **Used by:** 175 operations, for example [Get Resource Details](../domains/organization-management/org-info-and-settings/get-resource-details.md), [Get Subscription Details](../domains/organization-management/org-info-and-settings/get-subscription-details.md), [Get Meta Details From Name](../domains/organization-management/org-info-and-settings/get-meta-details.md), [Get Users](../domains/users-and-groups/org-users/get-users.md), [Add Users](../domains/users-and-groups/org-users/add-users.md), [Remove Users](../domains/users-and-groups/org-users/remove-users.md), and others.

## ZANALYTICS-DEST-ORGID

- **What it is:** Destination organization ID for cross-organization copies
- **Where it is sent:** HTTP header.
- **OpenAPI description:** The ID of the destination organization into which the workspace has to be copied. It is used by Organization Admins who have admin access in more than one organization. When this header is present, the system validates that the requesting user is a member of the specified organization and uses it as the target of the copy. When it is absent, the destination organization defaults to the organization resolved from the ZANALYTICS-ORGID header.

- **Obtained from:** [Get Org List](../domains/organization-management/org-info-and-settings/get-organizations.md).

- **Used by:** 3 operations, for example [Copy Workspace](../domains/workspace-management/workspace-operations/copy-workspace.md), [Copy Custom Formulas](../domains/data-modeling-and-schema/formula-columns/copy-formulas.md), [Copy Views](../domains/views-management/view-operations/copy-views.md).

## workspace-id

- **What it is:** Workspace ID
- **Where it is sent:** URL path segment `{workspace-id}`.
- **OpenAPI description:** ID of the workspace.

- **Obtained from:** [Get Meta Details From Name](../domains/organization-management/org-info-and-settings/get-meta-details.md), [Get All Workspace List](../domains/workspace-management/workspace-operations/get-all-workspaces.md), [Get Owned Workspace List](../domains/workspace-management/workspace-operations/get-owned-workspaces.md), [Get Shared Workspace List](../domains/workspace-management/workspace-operations/get-shared-workspaces.md), [Create Workspace](../domains/workspace-management/workspace-operations/create-workspace.md).

- **Used by:** 155 operations, for example [Get Workspace Users](../domains/users-and-groups/workspace-users/get-workspace-users.md), [Add Workspace Users](../domains/users-and-groups/workspace-users/add-workspace-users.md), [Remove Workspace Users](../domains/users-and-groups/workspace-users/delete-workspace-users.md), [Change Workspace Users Status](../domains/users-and-groups/workspace-users/change-workspace-users-status.md), [Change Workspace Users Role](../domains/users-and-groups/workspace-users/change-workspace-users-role.md), [Get Workspace Admins](../domains/users-and-groups/workspace-users/get-workspace-admins.md), and others.

## view-id

- **What it is:** View ID (table, report, dashboard, query table, etc.)
- **Where it is sent:** URL path segment `{view-id}`.
- **OpenAPI description:** ID of the view.

- **Obtained from:** [Get Meta Details From Name](../domains/organization-management/org-info-and-settings/get-meta-details.md), [Get View List](../domains/views-management/view-operations/get-views.md), [Create Table](../domains/data-modeling-and-schema/table-and-schema/create-table.md), [Create Query Table](../domains/data-modeling-and-schema/query-tables/create-query-table.md), [Import Data into a New Table (Synchronous)](../domains/data-operations/sync-data-import/import-data-new-table.md), [Create Report](../domains/reports-and-dashboards/reports/create-report.md), [Create Dashboard](../domains/reports-and-dashboards/dashboards/create-dashboard.md).

- **Used by:** 58 operations, for example [Get Table Metadata](../domains/data-modeling-and-schema/table-and-schema/get-table-metadata.md), [Add Column](../domains/data-modeling-and-schema/columns/add-column.md), [Rename Column](../domains/data-modeling-and-schema/columns/rename-column.md), [Delete Column](../domains/data-modeling-and-schema/columns/delete-column.md), [Hide Columns](../domains/data-modeling-and-schema/columns/hide-columns.md), [Show Columns](../domains/data-modeling-and-schema/columns/show-columns.md), and others.

## column-id

- **What it is:** Column ID within a table
- **Where it is sent:** URL path segment `{column-id}`.
- **OpenAPI description:** ID of the column.

- **Obtained from:** [Get Table Metadata](../domains/data-modeling-and-schema/table-and-schema/get-table-metadata.md), [Add Column](../domains/data-modeling-and-schema/columns/add-column.md).

- **Used by:** 6 operations, for example [Rename Column](../domains/data-modeling-and-schema/columns/rename-column.md), [Delete Column](../domains/data-modeling-and-schema/columns/delete-column.md), [Get Column Dependents](../domains/data-modeling-and-schema/columns/get-column-dependents.md), [Add Lookup](../domains/data-modeling-and-schema/lookups-and-relationships/add-lookup.md), [Remove Lookup](../domains/data-modeling-and-schema/lookups-and-relationships/remove-lookup.md), [Auto Analyse Column](../domains/views-management/auto-analysis/auto-analyse-column.md).

## folder-id

- **What it is:** Folder ID within a workspace
- **Where it is sent:** URL path segment `{folder-id}`.
- **OpenAPI description:** The ID of the folder. It can be obtained using the Get Folder List API.

- **Obtained from:** [Get Folder List](../domains/workspace-management/workspace-folders/get-folders.md), [Create Folder](../domains/workspace-management/workspace-folders/create-folder.md).

- **Used by:** 5 operations, for example [Rename Folder](../domains/workspace-management/workspace-folders/rename-folder.md), [Delete Folder](../domains/workspace-management/workspace-folders/delete-folder.md), [Change Folder Hierarchy](../domains/workspace-management/workspace-folders/change-folder-hierarchy.md), [Change Folder Position](../domains/workspace-management/workspace-folders/change-folder-position.md), [Make Default Folder](../domains/workspace-management/workspace-folders/make-default-folder.md).

## group-id

- **What it is:** Workspace group ID
- **Where it is sent:** URL path segment `{group-id}`.
- **OpenAPI description:** ID of the group.

- **Obtained from:** [Get Group List](../domains/users-and-groups/workspace-groups/get-groups.md), [Create Group](../domains/users-and-groups/workspace-groups/create-group.md).

- **Used by:** 5 operations, for example [Rename Group](../domains/users-and-groups/workspace-groups/rename-group.md), [Add Group Members](../domains/users-and-groups/workspace-groups/add-group-members.md), [Remove Group Members](../domains/users-and-groups/workspace-groups/remove-group-members.md), [Delete Group](../domains/users-and-groups/workspace-groups/delete-group.md), [Get Group Details](../domains/users-and-groups/workspace-groups/get-group-details.md).

## job-id

- **What it is:** Import or export job ID
- **Where it is sent:** URL path segment `{job-id}`.
- **OpenAPI description:** The unique identifier of the import/export job.

- **Obtained from:** [Create Export Job using SQL Query (Asynchronous)](../domains/data-operations/async-data-export/create-export-job-sql-query.md), [Create Export Job using View ID (Asynchronous)](../domains/data-operations/async-data-export/create-export-job-view-id.md), [Create Import Job for a New Table (Asynchronous)](../domains/data-operations/async-data-import/create-import-job-new-table.md), [Create Import Job for an Existing Table (Asynchronous)](../domains/data-operations/async-data-import/create-import-job-existing-table.md).

- **Used by:** 3 operations, for example [Get Import Job Details](../domains/data-operations/async-data-import/get-import-job-details.md), [Get Export Job Details](../domains/data-operations/async-data-export/get-export-job-details.md), [Download Exported Data](../domains/data-operations/async-data-export/download-exported-data.md).

## datasource-id

- **What it is:** Datasource ID
- **Where it is sent:** URL path segment `{datasource-id}`.
- **OpenAPI description:** ID of the datasource.

- **Obtained from:** [Get Datasources](../domains/data-operations/data-sync-and-connectivity/get-datasources.md).

- **Used by:** 2 operations, for example [Sync Data](../domains/data-operations/data-sync-and-connectivity/sync-datasource.md), [Update Datasource Connection](../domains/data-operations/data-sync-and-connectivity/update-datasource-connection.md).

## schedule-id

- **What it is:** Email schedule ID
- **Where it is sent:** URL path segment `{schedule-id}`.
- **OpenAPI description:** ID of the email schedule.

- **Obtained from:** [Get Email Schedules](../domains/schedules-and-alerts/email-schedules/get-email-schedules.md), [Create Email Schedule](../domains/schedules-and-alerts/email-schedules/create-email-schedule.md).

- **Used by:** 4 operations, for example [Update Email Schedule](../domains/schedules-and-alerts/email-schedules/update-email-schedule.md), [Delete Email Schedule](../domains/schedules-and-alerts/email-schedules/delete-email-schedule.md), [Change Email Schedule Status](../domains/schedules-and-alerts/email-schedules/change-email-schedule-status.md), [Trigger Email Schedule](../domains/schedules-and-alerts/email-schedules/trigger-email-schedule.md).

## querytable-id

- **What it is:** Query table ID (a view ID)
- **Where it is sent:** URL path segment `{querytable-id}`.
- **OpenAPI description:** ID of the query table. Obtained from the Get Query Tables API.

- **Obtained from:** [Get Query Tables](../domains/data-modeling-and-schema/query-tables/get-query-tables.md), [Create Query Table](../domains/data-modeling-and-schema/query-tables/create-query-table.md).

- **Used by:** 2 operations, for example [Edit Query Table](../domains/data-modeling-and-schema/query-tables/edit-query-table.md), [Get Query Table Details](../domains/data-modeling-and-schema/query-tables/get-query-table-details.md).

## formula-id

- **What it is:** Custom formula column ID or aggregate formula ID
- **Where it is sent:** URL path segment `{formula-id}`.
- **OpenAPI description:** ID of the formula.

- **Obtained from:** [Get Custom Formulas](../domains/data-modeling-and-schema/formula-columns/get-custom-formula-list.md), [Add Custom Formula](../domains/data-modeling-and-schema/formula-columns/add-formula-column.md), [Get Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-list.md), [Add Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/add-aggregate-formula.md), [Get Unified Metrics in Workspace](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formulas-in-workspace.md).

- **Used by:** 6 operations, for example [Edit Custom Formula](../domains/data-modeling-and-schema/formula-columns/edit-formula-column.md), [Delete Custom Formula](../domains/data-modeling-and-schema/formula-columns/delete-formula-column.md), [Edit Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/edit-aggregate-formula.md), [Delete Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/delete-aggregate-formula.md), [Get Aggregate Formula Dependents](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-dependents.md), [Get Aggregate Formula Value](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-value.md).

## variable-id

- **What it is:** Workspace variable ID
- **Where it is sent:** URL path segment `{variable-id}`.
- **OpenAPI description:** ID of the variable.

- **Obtained from:** [Get Variables](../domains/data-modeling-and-schema/workspace-variables/get-variables.md), [Create Variable](../domains/data-modeling-and-schema/workspace-variables/create-variable.md).

- **Used by:** 3 operations, for example [Edit Variable](../domains/data-modeling-and-schema/workspace-variables/update-variable.md), [Delete Variable](../domains/data-modeling-and-schema/workspace-variables/delete-variable.md), [Get Variable Details](../domains/data-modeling-and-schema/workspace-variables/get-variable-details.md).

## slide-id

- **What it is:** Slideshow ID
- **Where it is sent:** URL path segment `{slide-id}`.
- **OpenAPI description:** ID of the slide.

- **Obtained from:** [Get Slide List](../domains/share-and-publish/slideshow-management/get-slideshows.md), [Create Slide Show](../domains/share-and-publish/slideshow-management/create-slideshow.md).

- **Used by:** 4 operations, for example [Get Slide URL](../domains/share-and-publish/slideshow-management/get-slideshow-url.md), [Get Slide Info](../domains/share-and-publish/slideshow-management/get-slideshow-details.md), [Update Slide Show](../domains/share-and-publish/slideshow-management/update-slideshow.md), [Delete Slide Show](../domains/share-and-publish/slideshow-management/delete-slideshow.md).

## analysis-id

- **What it is:** AutoML analysis ID
- **Where it is sent:** URL path segment `{analysis-id}`.
- **OpenAPI description:** ID of the AutoML analysis.

- **Obtained from:** [Get AutoML Analysis In Org](../domains/dsml/automl/get-auto-ml-analysis-in-org.md), [Get AutoML Analysis In Workspace](../domains/dsml/automl/get-auto-ml-analysis-in-workspace.md), [Create AutoML Analysis](../domains/dsml/automl/create-auto-ml-analysis.md).

- **Used by:** 8 operations, for example [Get AutoML Analysis Details](../domains/dsml/automl/get-auto-ml-analysis-details.md), [Get Deployments For A Model](../domains/dsml/automl/get-deployments-for-model.md), [Delete AutoML Analysis](../domains/dsml/automl/delete-auto-ml-analysis.md), [Delete AutoML Analysis Model](../domains/dsml/automl/delete-auto-ml-analysis-model.md), [Create AutoML Analysis Deployment](../domains/dsml/automl/create-auto-ml-analysis-deployment.md), [Run AutoML Analysis](../domains/dsml/automl/run-auto-ml-analysis.md), and others.

## model-id

- **What it is:** AutoML model ID
- **Where it is sent:** URL path segment `{model-id}`.
- **OpenAPI description:** ID of the AutoML analysis model.

- **Obtained from:** [Get AutoML Analysis Details](../domains/dsml/automl/get-auto-ml-analysis-details.md).

- **Used by:** 4 operations, for example [Get Deployments For A Model](../domains/dsml/automl/get-deployments-for-model.md), [Delete AutoML Analysis Model](../domains/dsml/automl/delete-auto-ml-analysis-model.md), [Create AutoML Analysis Deployment](../domains/dsml/automl/create-auto-ml-analysis-deployment.md), [AutoML What If Analysis](../domains/dsml/automl/auto-ml-what-if-analysis.md).

## deployment-id

- **What it is:** AutoML model deployment ID
- **Where it is sent:** URL path segment `{deployment-id}`.
- **OpenAPI description:** ID of the AutoML analysis deployment.

- **Obtained from:** [Get Deployments For A Model](../domains/dsml/automl/get-deployments-for-model.md), [Create AutoML Analysis Deployment](../domains/dsml/automl/create-auto-ml-analysis-deployment.md).

- **Used by:** 2 operations, for example [Run AutoML Analysis](../domains/dsml/automl/run-auto-ml-analysis.md), [Delete AutoML Analysis Model Deployment](../domains/dsml/automl/delete-auto-ml-analysis-model-deployment.md).

## role-id

- **What it is:** Custom role ID
- **Where it is sent:** URL path segment `{role-id}`.
- **OpenAPI description:** ID of the custom role.

- **Used by:** 2 operations, for example [Update Custom Role](../domains/users-and-groups/custom-roles/update-custom-role.md), [Delete Custom Role](../domains/users-and-groups/custom-roles/delete-custom-role.md).

## tag-id

- **What it is:** ID of the tag.
- **Where it is sent:** URL path segment `{tag-id}`.
- **OpenAPI description:** ID of the tag.

- **Used by:** 5 operations, for example [Get Tagged Views](../domains/views-management/tags/get-tagged-views.md), [Update Tag](../domains/views-management/tags/update-tag.md), [Delete Tag](../domains/views-management/tags/delete-tag.md), [Add Tag To Multiple Views](../domains/views-management/tags/add-tag-to-views.md), [Remove Tag From Multiple Views](../domains/views-management/tags/remove-tag-from-views.md).

## dashboard-id

- **What it is:** Dashboard ID (a view ID whose type is Dashboard)
- **Where it is sent:** URL path segment `{dashboard-id}`.
- **OpenAPI description:** ID of the dashboard whose configuration is returned.

- **Obtained from:** [Get All Dashboards](../domains/reports-and-dashboards/dashboards/get-dashboards.md), [Get Owned Dashboards](../domains/reports-and-dashboards/dashboards/get-owned-dashboards.md), [Get Shared Dashboards](../domains/reports-and-dashboards/dashboards/get-shared-dashboards.md), [Create Dashboard](../domains/reports-and-dashboards/dashboards/create-dashboard.md), [Get View List](../domains/views-management/view-operations/get-views.md).

- **Used by:** 2 operations, for example [Read Dashboard Metadata](../domains/reports-and-dashboards/dashboards/get-dashboard-metadata.md), [Update Dashboard](../domains/reports-and-dashboards/dashboards/update-dashboard.md).

# Related

- [Request conventions](request-conventions.md)
- [Glossary](glossary.md)
