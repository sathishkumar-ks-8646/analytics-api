---
type: Reference
title: Permission matrix
description: "For every Zoho Analytics REST API v2 operation: the OAuth scope, whether the organization header is needed, and the role or view permission the caller must hold."
tags:
  - zoho-analytics
  - rest-api-v2
  - permissions
  - roles
  - authorization
  - criteria
sources:
  - id: group-org-info-and-settings
    resource: "/domains/organization-management/org-info-and-settings/overview.md"
    title: Organization Info & Settings - group overview
  - id: group-org-users
    resource: "/domains/users-and-groups/org-users/overview.md"
    title: Organization Users - group overview
  - id: group-custom-roles
    resource: "/domains/users-and-groups/custom-roles/overview.md"
    title: Custom Roles - group overview
  - id: group-workspace-users
    resource: "/domains/users-and-groups/workspace-users/overview.md"
    title: Workspace Users - group overview
  - id: group-workspace-groups
    resource: "/domains/users-and-groups/workspace-groups/overview.md"
    title: Workspace Groups - group overview
  - id: group-workspace-operations
    resource: "/domains/workspace-management/workspace-operations/overview.md"
    title: Workspace Operations - group overview
  - id: group-workspace-folders
    resource: "/domains/workspace-management/workspace-folders/overview.md"
    title: Workspace Folders - group overview
  - id: group-workspace-preferences
    resource: "/domains/workspace-management/workspace-preferences/overview.md"
    title: Workspace Preferences - group overview
  - id: group-domain-and-white-label
    resource: "/domains/workspace-management/domain-and-white-label/overview.md"
    title: Domain & White Label Access - group overview
  - id: group-table-and-schema
    resource: "/domains/data-modeling-and-schema/table-and-schema/overview.md"
    title: Table & Schema - group overview
  - id: group-columns
    resource: "/domains/data-modeling-and-schema/columns/overview.md"
    title: Columns - group overview
  - id: group-lookups-and-relationships
    resource: "/domains/data-modeling-and-schema/lookups-and-relationships/overview.md"
    title: Lookups & Relationships - group overview
  - id: group-query-tables
    resource: "/domains/data-modeling-and-schema/query-tables/overview.md"
    title: Query Tables - group overview
  - id: group-formula-columns
    resource: "/domains/data-modeling-and-schema/formula-columns/overview.md"
    title: Custom Formula Columns - group overview
  - id: group-aggregate-formulas
    resource: "/domains/data-modeling-and-schema/aggregate-formulas/overview.md"
    title: Aggregate Formulas (Unified Metrics) - group overview
  - id: group-workspace-variables
    resource: "/domains/data-modeling-and-schema/workspace-variables/overview.md"
    title: Workspace Variables - group overview
  - id: group-sync-data-import
    resource: "/domains/data-operations/sync-data-import/overview.md"
    title: Synchronous Data Import - group overview
  - id: group-async-data-import
    resource: "/domains/data-operations/async-data-import/overview.md"
    title: Asynchronous & Batch Data Import - group overview
  - id: group-sync-data-export
    resource: "/domains/data-operations/sync-data-export/overview.md"
    title: Synchronous Data Export - group overview
  - id: group-async-data-export
    resource: "/domains/data-operations/async-data-export/overview.md"
    title: Asynchronous Data Export - group overview
  - id: group-row-operations
    resource: "/domains/data-operations/row-operations/overview.md"
    title: Row Operations - group overview
  - id: group-data-sync-and-connectivity
    resource: "/domains/data-operations/data-sync-and-connectivity/overview.md"
    title: Data Sync & Connectivity - group overview
  - id: group-view-operations
    resource: "/domains/views-management/view-operations/overview.md"
    title: View Operations - group overview
  - id: group-view-preferences
    resource: "/domains/views-management/view-preferences/overview.md"
    title: View Preferences - group overview
  - id: group-trash-management
    resource: "/domains/views-management/trash-management/overview.md"
    title: Trash Management - group overview
  - id: group-auto-analysis
    resource: "/domains/views-management/auto-analysis/overview.md"
    title: Auto Analysis - group overview
  - id: group-tags
    resource: "/domains/views-management/tags/overview.md"
    title: Tags - group overview
  - id: group-reports
    resource: "/domains/reports-and-dashboards/reports/overview.md"
    title: Reports (Analysis Views) - group overview
  - id: group-dashboards
    resource: "/domains/reports-and-dashboards/dashboards/overview.md"
    title: Dashboards - group overview
  - id: group-sharing
    resource: "/domains/share-and-publish/sharing/overview.md"
    title: Sharing - group overview
  - id: group-publish
    resource: "/domains/share-and-publish/publish/overview.md"
    title: Publish - group overview
  - id: group-embed-url
    resource: "/domains/share-and-publish/embed-url/overview.md"
    title: Embed URL - group overview
  - id: group-slideshow-management
    resource: "/domains/share-and-publish/slideshow-management/overview.md"
    title: Slideshow Management - group overview
  - id: group-email-schedules
    resource: "/domains/schedules-and-alerts/email-schedules/overview.md"
    title: Email Schedules - group overview
  - id: group-automl
    resource: "/domains/dsml/automl/overview.md"
    title: AutoML - group overview
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

Authorization has two independent layers. Both must pass:

1. **OAuth scope** on the access token (see [OAuth scopes](oauth-scopes.md)). A missing scope fails with [`8535`](error-codes.md#error-8535).
2. **Role or permission** of the authenticated user on the organization, workspace or view (see [Roles & permissions](roles-and-permissions.md)). A missing permission fails with [`7301`](error-codes.md#error-7301) (`SECURITY_NOT_PERMITTED`).

The `ZANALYTICS-ORGID` column says whether the organization header is `required`, `optional` or `not-required` for the call.

# Matrix

| Operation | Method | OAuth scope | ZANALYTICS-ORGID | Permission required |
|---|---|---|---|---|
| [Get Org List](../domains/organization-management/org-info-and-settings/get-organizations.md) | GET | `ZohoAnalytics.metadata.read` | not-required | Any authenticated Zoho Analytics user. |
| [Get Resource Details](../domains/organization-management/org-info-and-settings/get-resource-details.md) | GET | `ZohoAnalytics.usermanagement.read` | required | The authenticated user must be an Account Admin or Organization Admin of the specified organisation. |
| [Get Subscription Details](../domains/organization-management/org-info-and-settings/get-subscription-details.md) | GET | `ZohoAnalytics.usermanagement.read` | required | The authenticated user must be an Account Admin or Organization Admin of the specified organisation. |
| [Get Meta Details From Name](../domains/organization-management/org-info-and-settings/get-meta-details.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must have at least Read access on the specified workspace (for workspace-only lookup), or Read access on the specific view (for view lookup). Workspace Admins, Account Admins, Organization Admins, and any user with at least one shared view in the workspace can call this API. |
| [Get Users](../domains/users-and-groups/org-users/get-users.md) | GET | `ZohoAnalytics.usermanagement.read` | required | The authenticated user must be an Account Admin or Organization Admin of the specified organisation. |
| [Add Users](../domains/users-and-groups/org-users/add-users.md) | POST | `ZohoAnalytics.usermanagement.create` | required | The authenticated user must be an Account Admin or Organization Admin of the specified organisation. |
| [Remove Users](../domains/users-and-groups/org-users/remove-users.md) | DELETE | `ZohoAnalytics.usermanagement.delete` | required | The authenticated user must be an Account Admin or Organization Admin of the specified organisation. |
| [Activate Users](../domains/users-and-groups/org-users/activate-users.md) | PUT | `ZohoAnalytics.usermanagement.update` | required | The authenticated user must be an Account Admin or Organization Admin of the specified organisation. |
| [Deactivate Users](../domains/users-and-groups/org-users/de-activate-users.md) | PUT | `ZohoAnalytics.usermanagement.update` | required | The authenticated user must be an Account Admin or Organization Admin of the specified organisation. |
| [Change User Role](../domains/users-and-groups/org-users/change-user-role.md) | PUT | `ZohoAnalytics.usermanagement.update` | required | The authenticated user must be an Account Admin or Organization Admin of the specified organisation. |
| [Get Org Admins](../domains/users-and-groups/org-users/get-org-admins.md) | GET | `ZohoAnalytics.share.read` | required | The authenticated user must be the **Account Admin** of the specified organisation. |
| [Get Custom Roles](../domains/users-and-groups/custom-roles/get-custom-roles.md) | GET | `ZohoAnalytics.usermanagement.read` | required | The authenticated user must be an Account Admin or Organization Admin of the organization. No other role qualifies; custom roles must be enabled for the organization and included in its plan. |
| [Create Custom Role](../domains/users-and-groups/custom-roles/create-custom-role.md) | POST | `ZohoAnalytics.usermanagement.create` | required | The authenticated user must be an Account Admin or Organization Admin of the organization. No other role qualifies; custom roles must be enabled for the organization and included in its plan. |
| [Update Custom Role](../domains/users-and-groups/custom-roles/update-custom-role.md) | PUT | `ZohoAnalytics.usermanagement.update` | required | The authenticated user must be an Account Admin or Organization Admin of the organization. No other role qualifies; custom roles must be enabled for the organization and included in its plan. |
| [Delete Custom Role](../domains/users-and-groups/custom-roles/delete-custom-role.md) | DELETE | `ZohoAnalytics.usermanagement.delete` | required | The authenticated user must be an Account Admin or Organization Admin of the organization. No other role qualifies; custom roles must be enabled for the organization and included in its plan. |
| [Get Workspace Users](../domains/users-and-groups/workspace-users/get-workspace-users.md) | GET | `ZohoAnalytics.usermanagement.read` | required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. |
| [Add Workspace Users](../domains/users-and-groups/workspace-users/add-workspace-users.md) | POST | `ZohoAnalytics.usermanagement.create` | required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. |
| [Remove Workspace Users](../domains/users-and-groups/workspace-users/delete-workspace-users.md) | DELETE | `ZohoAnalytics.usermanagement.delete` | required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. |
| [Change Workspace Users Status](../domains/users-and-groups/workspace-users/change-workspace-users-status.md) | PUT | `ZohoAnalytics.usermanagement.update` | required | The authenticated user must be the **Account Admin** of the organisation that owns the workspace. |
| [Change Workspace Users Role](../domains/users-and-groups/workspace-users/change-workspace-users-role.md) | PUT | `ZohoAnalytics.usermanagement.update` | required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. |
| [Get Workspace Admins](../domains/users-and-groups/workspace-users/get-workspace-admins.md) | GET | `ZohoAnalytics.share.read` | required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. |
| [Add Workspace Admins](../domains/users-and-groups/workspace-users/add-workspace-admins.md) | POST | `ZohoAnalytics.share.create` | required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. |
| [Remove Workspace Admins](../domains/users-and-groups/workspace-users/remove-workspace-admins.md) | DELETE | `ZohoAnalytics.share.delete` | required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. |
| [Get Group List](../domains/users-and-groups/workspace-groups/get-groups.md) | GET | `ZohoAnalytics.share.read` | required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. |
| [Create Group](../domains/users-and-groups/workspace-groups/create-group.md) | POST | `ZohoAnalytics.share.create` | required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. |
| [Rename Group](../domains/users-and-groups/workspace-groups/rename-group.md) | PUT | `ZohoAnalytics.share.update` | required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. |
| [Add Group Members](../domains/users-and-groups/workspace-groups/add-group-members.md) | POST | `ZohoAnalytics.share.create` | required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. |
| [Remove Group Members](../domains/users-and-groups/workspace-groups/remove-group-members.md) | DELETE | `ZohoAnalytics.share.delete` | required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. |
| [Delete Group](../domains/users-and-groups/workspace-groups/delete-group.md) | DELETE | `ZohoAnalytics.share.delete` | required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. |
| [Get Group Details](../domains/users-and-groups/workspace-groups/get-group-details.md) | GET | `ZohoAnalytics.share.read` | required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. |
| [Create Workspace](../domains/workspace-management/workspace-operations/create-workspace.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an Account Admin or Organization Admin of the target organisation. |
| [Copy Workspace](../domains/workspace-management/workspace-operations/copy-workspace.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an Account Admin or Organization Admin of the **destination** organisation. |
| [Rename Workspace](../domains/workspace-management/workspace-operations/rename-workspace.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. |
| [Delete Workspace](../domains/workspace-management/workspace-operations/delete-workspace.md) | DELETE | `ZohoAnalytics.modeling.delete` | required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. |
| [Export as Template](../domains/workspace-management/workspace-operations/export-as-template.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. |
| [Get All Workspace List](../domains/workspace-management/workspace-operations/get-all-workspaces.md) | GET | `ZohoAnalytics.metadata.read` | not-required | Any authenticated Zoho Analytics user. |
| [Get Owned Workspace List](../domains/workspace-management/workspace-operations/get-owned-workspaces.md) | GET | `ZohoAnalytics.metadata.read` | not-required | The authenticated user must be the **Account Admin** of the organisation. |
| [Get Shared Workspace List](../domains/workspace-management/workspace-operations/get-shared-workspaces.md) | GET | `ZohoAnalytics.metadata.read` | not-required | Any authenticated Zoho Analytics user. |
| [Get Workspace Secret Key](../domains/workspace-management/workspace-operations/get-workspace-secret-key.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. |
| [Get Workspace Info](../domains/workspace-management/workspace-operations/get-workspace-details.md) | GET | `ZohoAnalytics.metadata.read` | not-required | The authenticated user must be a Workspace Admin, or a Shared User, or a Group Member of the workspace, or any user with at least Read permission on a view within the workspace. Account Admins and Organization Admins also have access. |
| [Get Folder List](../domains/workspace-management/workspace-folders/get-folders.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be a Workspace Admin of the specified workspace, or a Shared User or Group Member with at least READ permission on one or more views in the workspace. |
| [Create Folder](../domains/workspace-management/workspace-folders/create-folder.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Folder permission on the workspace. |
| [Rename Folder](../domains/workspace-management/workspace-folders/rename-folder.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Folder permission on the workspace. |
| [Delete Folder](../domains/workspace-management/workspace-folders/delete-folder.md) | DELETE | `ZohoAnalytics.modeling.delete` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Folder permission on the workspace. |
| [Change Folder Hierarchy](../domains/workspace-management/workspace-folders/change-folder-hierarchy.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Folder permission on the workspace. |
| [Change Folder Position](../domains/workspace-management/workspace-folders/change-folder-position.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Folder permission on the workspace. |
| [Move Views To Folder](../domains/workspace-management/workspace-folders/move-views-to-folder.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Folder permission on the workspace. |
| [Make Default Folder](../domains/workspace-management/workspace-folders/make-default-folder.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Folder permission on the workspace. |
| [Add Default Workspace](../domains/workspace-management/workspace-preferences/add-default-workspace.md) | POST | `ZohoAnalytics.metadata.update` | required | The authenticated user must be a Workspace Admin, or a Shared User, or a Group Member of the workspace, or any user with at least Read permission on a view within the workspace. |
| [Remove Default Workspace](../domains/workspace-management/workspace-preferences/remove-default-workspace.md) | DELETE | `ZohoAnalytics.metadata.update` | required | The authenticated user must be a Workspace Admin, or a Shared User, or a Group Member of the workspace, or any user with at least Read permission on a view within the workspace. |
| [Add Favourite Workspace](../domains/workspace-management/workspace-preferences/add-favorite-workspace.md) | POST | `ZohoAnalytics.metadata.update` | required | The authenticated user must be a Workspace Admin, or a Shared User, or a Group Member of the workspace, or any user with at least Read permission on a view within the workspace. |
| [Remove Favourite Workspace](../domains/workspace-management/workspace-preferences/remove-favorite-workspace.md) | DELETE | `ZohoAnalytics.metadata.update` | required | The authenticated user must be a Workspace Admin, or a Shared User, or a Group Member of the workspace, or any user with at least Read permission on a view within the workspace. |
| [Enable Workspace for Domain Access](../domains/workspace-management/domain-and-white-label/enable-domain-workspace.md) | POST | `ZohoAnalytics.metadata.update` | required | The authenticated user must be an Account Admin or Organization Admin of the workspace's organisation, **and** the workspace's Account Admin must have a White Label / Client Portal domain configured. |
| [Disable Workspace for Domain Access](../domains/workspace-management/domain-and-white-label/disable-domain-workspace.md) | DELETE | `ZohoAnalytics.metadata.update` | required | The authenticated user must be an Account Admin or Organization Admin of the workspace's organisation, **and** the workspace's Account Admin must have a White Label / Client Portal domain configured. |
| [Create Table](../domains/data-modeling-and-schema/table-and-schema/create-table.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Table permission on the workspace. |
| [Get Table Metadata](../domains/data-modeling-and-schema/table-and-schema/get-table-metadata.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the view. |
| [Add Column](../domains/data-modeling-and-schema/columns/add-column.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the workspace. |
| [Rename Column](../domains/data-modeling-and-schema/columns/rename-column.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the workspace. |
| [Delete Column](../domains/data-modeling-and-schema/columns/delete-column.md) | DELETE | `ZohoAnalytics.modeling.delete` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the workspace. |
| [Hide Columns](../domains/data-modeling-and-schema/columns/hide-columns.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the view. |
| [Show Columns](../domains/data-modeling-and-schema/columns/show-columns.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the view. |
| [Get Column Dependents](../domains/data-modeling-and-schema/columns/get-column-dependents.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be a Workspace Admin of the specified workspace. |
| [Sort Data by Columns](../domains/data-modeling-and-schema/columns/sort-data-by-columns.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the view. |
| [Reorder Columns](../domains/data-modeling-and-schema/columns/reorder-columns.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the view. |
| [Add Lookup](../domains/data-modeling-and-schema/lookups-and-relationships/add-lookup.md) | POST | `ZohoAnalytics.modeling.update` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the workspace. |
| [Remove Lookup](../domains/data-modeling-and-schema/lookups-and-relationships/remove-lookup.md) | DELETE | `ZohoAnalytics.modeling.update` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the workspace. |
| [Get Query Tables](../domains/data-modeling-and-schema/query-tables/get-query-tables.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Query Table permission on the workspace. |
| [Create Query Table](../domains/data-modeling-and-schema/query-tables/create-query-table.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Query Table permission on the workspace. |
| [Edit Query Table](../domains/data-modeling-and-schema/query-tables/edit-query-table.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the query table. |
| [Get Query Table Details](../domains/data-modeling-and-schema/query-tables/get-query-table-details.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the query table. |
| [Get Custom Formulas](../domains/data-modeling-and-schema/formula-columns/get-custom-formula-list.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view. |
| [Add Custom Formula](../domains/data-modeling-and-schema/formula-columns/add-formula-column.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view. |
| [Edit Custom Formula](../domains/data-modeling-and-schema/formula-columns/edit-formula-column.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view. |
| [Delete Custom Formula](../domains/data-modeling-and-schema/formula-columns/delete-formula-column.md) | DELETE | `ZohoAnalytics.modeling.delete` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view. |
| [Copy Custom Formulas](../domains/data-modeling-and-schema/formula-columns/copy-formulas.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an Account Admin or Organization Admin of the destination organisation. This API is **not** available to Workspace Admins or any custom-permission user — only Account Admin / Org Admin roles are authorized. |
| [Get Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-list.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view. |
| [Add Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/add-aggregate-formula.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view. |
| [Edit Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/edit-aggregate-formula.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view. |
| [Delete Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/delete-aggregate-formula.md) | DELETE | `ZohoAnalytics.modeling.delete` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view. |
| [Get Unified Metrics in Workspace](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formulas-in-workspace.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Read permission on the workspace. |
| [Get Aggregate Formula Dependents](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-dependents.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Read permission on the workspace. |
| [Get Aggregate Formula Value](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-value.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Read permission on the workspace **and** access to the columns/tables involved in the formula. |
| [Create Variable](../domains/data-modeling-and-schema/workspace-variables/create-variable.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. |
| [Edit Variable](../domains/data-modeling-and-schema/workspace-variables/update-variable.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. |
| [Delete Variable](../domains/data-modeling-and-schema/workspace-variables/delete-variable.md) | DELETE | `ZohoAnalytics.modeling.delete` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. |
| [Get Variables](../domains/data-modeling-and-schema/workspace-variables/get-variables.md) | GET | `ZohoAnalytics.modeling.read` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. |
| [Get Variable Details](../domains/data-modeling-and-schema/workspace-variables/get-variable-details.md) | GET | `ZohoAnalytics.modeling.read` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. |
| [Import Data into a New Table (Synchronous)](../domains/data-operations/sync-data-import/import-data-new-table.md) | POST | `ZohoAnalytics.data.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Table permission on the workspace. |
| [Import Data into an Existing Table (Synchronous)](../domains/data-operations/sync-data-import/import-data-existing-table.md) | POST | `ZohoAnalytics.data.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user holding the import permission that matches the requested `importType` — see [Permission Model](../domains/data-operations/sync-data-import/overview.md#permission-model). |
| [Create Import Job for a New Table (Asynchronous)](../domains/data-operations/async-data-import/create-import-job-new-table.md) | POST | `ZohoAnalytics.data.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Table permission on the workspace. |
| [Create Import Job for an Existing Table (Asynchronous)](../domains/data-operations/async-data-import/create-import-job-existing-table.md) | POST | `ZohoAnalytics.data.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user holding the import permission matching the requested `importType` — see [Permission Model](../domains/data-operations/async-data-import/overview.md#permission-model). |
| [Batch Import Data into New Table](../domains/data-operations/async-data-import/batch-import-new-table.md) | POST | `ZohoAnalytics.data.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Table permission on the workspace. |
| [Batch Import Data into Existing Table](../domains/data-operations/async-data-import/batch-import-existing-table.md) | POST | `ZohoAnalytics.data.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user holding the import permission matching the requested `importType` — see [Permission Model](../domains/data-operations/async-data-import/overview.md#permission-model). |
| [Get Import Job Details](../domains/data-operations/async-data-import/get-import-job-details.md) | GET | `ZohoAnalytics.data.create` | required | **Only the user who created the import job.** Any other user — including an Account Admin or Organization Admin — receives `8138`. |
| [Export Data from a View](../domains/data-operations/sync-data-export/export-data-view.md) | GET | `ZohoAnalytics.data.read` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Export permission on the view. |
| [Create Export Job using SQL Query (Asynchronous)](../domains/data-operations/async-data-export/create-export-job-sql-query.md) | GET | `ZohoAnalytics.data.read` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Export permission on every table the SQL query references. |
| [Create Export Job using View ID (Asynchronous)](../domains/data-operations/async-data-export/create-export-job-view-id.md) | GET | `ZohoAnalytics.data.read` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Export permission on the view. |
| [Get Export Job Details](../domains/data-operations/async-data-export/get-export-job-details.md) | GET | `ZohoAnalytics.data.read` | required | Only the user who created the export job. Any other user, including an Account Admin or Organization Admin, receives 8124. |
| [Download Exported Data](../domains/data-operations/async-data-export/download-exported-data.md) | GET | `ZohoAnalytics.data.read` | required | Only the user who created the export job. Any other user, including an Account Admin or Organization Admin, receives 8124. |
| [Add Row](../domains/data-operations/row-operations/add-row.md) | POST | `ZohoAnalytics.data.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Add Row permission on the view. |
| [Update Row](../domains/data-operations/row-operations/update-rows.md) | PUT | `ZohoAnalytics.data.update` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Update Row permission on the view. When `addIfNotExist` triggers an insert, **Add Row permission is additionally required**. |
| [Delete Row](../domains/data-operations/row-operations/delete-rows.md) | DELETE | `ZohoAnalytics.data.delete` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with **Delete All Rows** permission on the view. |
| [Sync Data](../domains/data-operations/data-sync-and-connectivity/sync-datasource.md) | POST | `ZohoAnalytics.metadata.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Table or Sync Data permission on the workspace. |
| [Refetch Data](../domains/data-operations/data-sync-and-connectivity/refetch-datasource.md) | POST | `ZohoAnalytics.metadata.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Sync Data permission on the workspace. |
| [Update Datasource Connection](../domains/data-operations/data-sync-and-connectivity/update-datasource-connection.md) | PUT | `ZohoAnalytics.metadata.update` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Table or Edit Datasource permission on the workspace. |
| [Get Datasources](../domains/data-operations/data-sync-and-connectivity/get-datasources.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with View Datasource or Create Table permission on the workspace. |
| [Get Last Import Details](../domains/data-operations/data-sync-and-connectivity/get-last-import-details.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with View Datasource or an import permission on the view. |
| [Save As View](../domains/views-management/view-operations/save-as-view.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Design & Modify permission on the workspace. |
| [Copy Views](../domains/views-management/view-operations/copy-views.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an Account Admin or Organization Admin (of the destination organisation). |
| [Create Similar Views](../domains/views-management/view-operations/create-similar-views.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an Account Admin, Organization Admin, or Workspace Admin of the workspace. |
| [Rename View](../domains/views-management/view-operations/rename-view.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner. |
| [Delete View](../domains/views-management/view-operations/delete-view.md) | DELETE | `ZohoAnalytics.modeling.delete` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner. |
| [Get View List](../domains/views-management/view-operations/get-views.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or a Shared User, or a Group Member, or any user with Read permission on the workspace. |
| [Get View Details](../domains/views-management/view-operations/get-view-details.md) | GET | `ZohoAnalytics.metadata.read` | not-required | The authenticated user must have at least **Read Only** permission on the view. This includes Account Admins, Organization Admins, Workspace Admins, View Owners, and any user with Read Only or higher access to the view. |
| [Get View URL](../domains/views-management/view-operations/get-view-url.md) | GET | `ZohoAnalytics.embed.read` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission or Make Public permission on the workspace. |
| [Get View Dependents](../domains/views-management/view-operations/get-view-dependents.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be an Account Admin, Organization Admin, or Workspace Admin. |
| [Get Recent Views](../domains/views-management/view-operations/get-recent-views.md) | GET | `ZohoAnalytics.metadata.read` | not-required | Any authenticated Zoho Analytics user. |
| [Add Favourite View](../domains/views-management/view-preferences/add-favorite-view.md) | POST | `ZohoAnalytics.metadata.update` | required | The authenticated user must have at least **Read Only** permission on the view. This includes Account Admins, Organization Admins, Workspace Admins, View Owners, and any user explicitly granted Read Only or higher access to the view. |
| [Remove Favourite View](../domains/views-management/view-preferences/remove-favorite-view.md) | DELETE | `ZohoAnalytics.metadata.update` | required | The authenticated user must have at least **Read Only** permission on the view. This includes Account Admins, Organization Admins, Workspace Admins, View Owners, and any user explicitly granted Read Only or higher access to the view. |
| [Get Trash Views](../domains/views-management/trash-management/get-trash-views.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be an **Account Admin** or **Organization Admin**, or a **Workspace Admin**, or a **Shared User**, or a **Group Member**, or any user with **Read** permission on the workspace. |
| [Restore Trash View](../domains/views-management/trash-management/restore-trash-view.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an **Account Admin** or **Organization Admin**, or a **Workspace Admin**, or the **View Owner** (the user who owned the view before it was trashed). |
| [Delete Trash View](../domains/views-management/trash-management/delete-trash-view.md) | DELETE | `ZohoAnalytics.modeling.delete` | required | The authenticated user must be an **Account Admin** or **Organization Admin**, or a **Workspace Admin**, or the **View Owner** (the user who owned the view before it was trashed). |
| [Auto Analyse View](../domains/views-management/auto-analysis/auto-analyse-view.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Report permission on the workspace. |
| [Auto Analyse Column](../domains/views-management/auto-analysis/auto-analyse-column.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Report permission on the workspace. |
| [Get Tags List](../domains/views-management/tags/get-tags.md) | GET | `ZohoAnalytics.metadata.read` | required | Any user with access to the workspace - an Account Admin or Organization Admin, a Workspace Admin, or any shared user, including users holding a custom role. |
| [Get Tagged Views](../domains/views-management/tags/get-tagged-views.md) | GET | `ZohoAnalytics.metadata.read` | required | Any user with access to the workspace. The returned list is filtered to the views the caller can see. |
| [Get View Tags](../domains/views-management/tags/get-view-tags.md) | GET | `ZohoAnalytics.metadata.read` | required | Any user with Read permission on the view. |
| [Create Tag](../domains/views-management/tags/create-tag.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. |
| [Update Tag](../domains/views-management/tags/update-tag.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. |
| [Delete Tag](../domains/views-management/tags/delete-tag.md) | DELETE | `ZohoAnalytics.modeling.delete` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. |
| [Add Tag To Multiple Views](../domains/views-management/tags/add-tag-to-views.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. The View Owner alone does not qualify. Read-only users are rejected with `8180`. |
| [Remove Tag From Multiple Views](../domains/views-management/tags/remove-tag-from-views.md) | DELETE | `ZohoAnalytics.modeling.delete` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. The View Owner alone does not qualify. Read-only users are rejected with `8180`. |
| [Add Multiple Tags To View](../domains/views-management/tags/add-tags-to-view.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Edit Design permission on the view. Read-only users are rejected with `8180`. |
| [Remove Multiple Tags From View](../domains/views-management/tags/remove-tags-from-view.md) | DELETE | `ZohoAnalytics.modeling.delete` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Edit Design permission on the view. Read-only users are rejected with `8180`. |
| [Create Report](../domains/reports-and-dashboards/reports/create-report.md) | POST | `ZohoAnalytics.modeling.create` | required | Workspace Admin / Organization Admin, or a shared or group user holding **Create Report** permission on the base table. |
| [Read Report Metadata](../domains/reports-and-dashboards/reports/get-report-metadata.md) | GET | `ZohoAnalytics.modeling.read` | required | **Design Modify** on the report. A read-only shared user cannot call this endpoint. |
| [Update Report](../domains/reports-and-dashboards/reports/update-report.md) | PUT | `ZohoAnalytics.modeling.update` | required | **Design Modify** on the report — the owner, a Workspace Admin, an Organization Admin, or a shared or group user granted edit rights. |
| [Create Dashboard](../domains/reports-and-dashboards/dashboards/create-dashboard.md) | POST | `ZohoAnalytics.modeling.create` | required | Workspace Admin / Organization Admin, or a shared or group user holding **Create Report** permission on the workspace. A Custom Role user must have the Create Report permission explicitly granted, otherwise the call is rejected before any validation runs. |
| [Read Dashboard Metadata](../domains/reports-and-dashboards/dashboards/get-dashboard-metadata.md) | GET | `ZohoAnalytics.modeling.read` | required | **Read Only** or higher on the dashboard. Owners, Workspace Admins, Organization Admins, shared users and group members with read access all qualify. |
| [Update Dashboard](../domains/reports-and-dashboards/dashboards/update-dashboard.md) | PUT | `ZohoAnalytics.modeling.update` | required | **Design Modify** on the dashboard — the owner, a Workspace Admin, an Organization Admin, or a shared user granted edit rights. |
| [Get All Dashboards](../domains/reports-and-dashboards/dashboards/get-dashboards.md) | GET | `ZohoAnalytics.metadata.read` | not-required | The authenticated user must be any active **Zoho Analytics user**. |
| [Get Owned Dashboards](../domains/reports-and-dashboards/dashboards/get-owned-dashboards.md) | GET | `ZohoAnalytics.metadata.read` | not-required | The authenticated user must be an **Account Admin**. |
| [Get Shared Dashboards](../domains/reports-and-dashboards/dashboards/get-shared-dashboards.md) | GET | `ZohoAnalytics.metadata.read` | not-required | The authenticated user must be any active **Zoho Analytics user**. |
| [Get Workspace Shared Details](../domains/share-and-publish/sharing/get-workspace-shared-details.md) | GET | `ZohoAnalytics.share.read` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. This API is restricted to workspace owners — there is no permission-based alternative. |
| [Share Views](../domains/share-and-publish/sharing/share-views.md) | POST | `ZohoAnalytics.share.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Share permission on all of the specified `viewIds`. |
| [Update Shared Details](../domains/share-and-publish/sharing/update-shared-details-for-view.md) | PUT | `ZohoAnalytics.share.update` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Share permission on `<view-id>`. |
| [Get Shared Details](../domains/share-and-publish/sharing/get-shared-details-for-views.md) | GET | `ZohoAnalytics.share.read` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Share permission on all of the specified `viewIds`. |
| [Remove Shared Views](../domains/share-and-publish/sharing/remove-share.md) | DELETE | `ZohoAnalytics.share.delete` | required | For removing specific `viewIds`: the authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Share permission on the specified views. For `removeAllViews: true`: the authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the workspace — this bulk option is restricted to workspace owners. |
| [Get My Permissions](../domains/share-and-publish/sharing/get-user-permissions.md) | GET | `ZohoAnalytics.share.read` | required | Any authenticated user with at least Read-Only access to `<view-id>` (i.e., any user the view has been shared with, or the view's owner/Workspace Admin). |
| [Make View Public](../domains/share-and-publish/publish/make-views-public.md) | POST | `ZohoAnalytics.embed.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Make Public permission on the view. |
| [Remove Public Permission](../domains/share-and-publish/publish/remove-public-permission.md) | DELETE | `ZohoAnalytics.embed.delete` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Make Public permission on the view, or any user with Share permission on the view. |
| [Get Private URL](../domains/share-and-publish/publish/get-private-url.md) | GET | `ZohoAnalytics.embed.read` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission on the view. |
| [Create Private URL](../domains/share-and-publish/publish/create-private-url.md) | POST | `ZohoAnalytics.embed.update` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission on the view. |
| [Remove Private Access](../domains/share-and-publish/publish/remove-private-access.md) | DELETE | `ZohoAnalytics.embed.delete` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission on the workspace, or any user with Share permission on the view. |
| [Get Publish Configurations](../domains/share-and-publish/publish/get-publish-configurations.md) | GET | `ZohoAnalytics.embed.read` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission on the view, or any user with Make Public permission on the view. |
| [Update Publish Configurations](../domains/share-and-publish/publish/update-publish-configurations.md) | PUT | `ZohoAnalytics.embed.update` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission on the view, or any user with Make Public permission on the view. |
| [Get Embed URL](../domains/share-and-publish/embed-url/get-embed-url.md) | GET | `ZohoAnalytics.embed.read` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission or Make Public permission on the view. A caller who is **not** a workspace owner must additionally be listed in the organization's OEM-enabled users configuration, otherwise `7301`. In every case the organization or the workspace must be enabled for Embedded Analytics, otherwise `8023`. |
| [Fetch All Embed URLs](../domains/share-and-publish/embed-url/get-embed-urls.md) | GET |  | required | The authenticated user must be an Account Admin or Organization Admin of the organization. The caller must also hold Publish permission or Make Public permission on the view, and the organization or workspace must be enabled for Embedded Analytics, otherwise `8023`. |
| [Delete Embed URL](../domains/share-and-publish/embed-url/delete-embed-url.md) | DELETE |  | required | The authenticated user must be an Account Admin or Organization Admin of the organization. The caller must also hold Publish permission or Make Public permission on the view, and the organization or workspace must be enabled for Embedded Analytics, otherwise `8023`. |
| [Get Slide List](../domains/share-and-publish/slideshow-management/get-slideshows.md) | GET | `ZohoAnalytics.embed.read` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Slideshow permission on the workspace. |
| [Get Slide URL](../domains/share-and-publish/slideshow-management/get-slideshow-url.md) | GET | `ZohoAnalytics.embed.read` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Slideshow permission on the workspace. |
| [Get Slide Info](../domains/share-and-publish/slideshow-management/get-slideshow-details.md) | GET | `ZohoAnalytics.embed.read` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Slideshow permission on the workspace. |
| [Create Slide Show](../domains/share-and-publish/slideshow-management/create-slideshow.md) | POST | `ZohoAnalytics.embed.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Slideshow permission on the workspace. |
| [Update Slide Show](../domains/share-and-publish/slideshow-management/update-slideshow.md) | PUT | `ZohoAnalytics.embed.update` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Slideshow permission on the workspace. |
| [Delete Slide Show](../domains/share-and-publish/slideshow-management/delete-slideshow.md) | DELETE | `ZohoAnalytics.embed.delete` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Slideshow permission on the workspace. |
| [Get Email Schedules](../domains/schedules-and-alerts/email-schedules/get-email-schedules.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace. |
| [Create Email Schedule](../domains/schedules-and-alerts/email-schedules/create-email-schedule.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace. The caller must additionally hold **Export** permission on every view listed in `viewIds`. |
| [Update Email Schedule](../domains/schedules-and-alerts/email-schedules/update-email-schedule.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace. A custom-role user whose role does not grant access to all email schedules may update **only schedules they created themselves** — otherwise `8002`. |
| [Delete Email Schedule](../domains/schedules-and-alerts/email-schedules/delete-email-schedule.md) | DELETE | `ZohoAnalytics.modeling.delete` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace. A custom-role user whose role does not grant access to all email schedules may delete **only schedules they created themselves** — otherwise `8002`. |
| [Change Email Schedule Status](../domains/schedules-and-alerts/email-schedules/change-email-schedule-status.md) | PUT | `ZohoAnalytics.modeling.update` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace. |
| [Trigger Email Schedule](../domains/schedules-and-alerts/email-schedules/trigger-email-schedule.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace. Export must also be enabled for the organization and for the workspace. |
| [Get AutoML Analysis In Org](../domains/dsml/automl/get-auto-ml-analysis-in-org.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be an Account Admin or Organization Admin of the organization. A Workspace Admin is **not** sufficient. |
| [Get AutoML Analysis In Workspace](../domains/dsml/automl/get-auto-ml-analysis-in-workspace.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace. |
| [Get AutoML Analysis Details](../domains/dsml/automl/get-auto-ml-analysis-details.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace. |
| [Get Deployments For A Model](../domains/dsml/automl/get-deployments-for-model.md) | GET | `ZohoAnalytics.metadata.read` | required | The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace. |
| [Create AutoML Analysis](../domains/dsml/automl/create-auto-ml-analysis.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace. |
| [Delete AutoML Analysis](../domains/dsml/automl/delete-auto-ml-analysis.md) | DELETE | `ZohoAnalytics.modeling.delete` | required | The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace. |
| [Delete AutoML Analysis Model](../domains/dsml/automl/delete-auto-ml-analysis-model.md) | DELETE | `ZohoAnalytics.modeling.delete` | required | The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace. |
| [Create AutoML Analysis Deployment](../domains/dsml/automl/create-auto-ml-analysis-deployment.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace. |
| [Run AutoML Analysis](../domains/dsml/automl/run-auto-ml-analysis.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace. |
| [Delete AutoML Analysis Model Deployment](../domains/dsml/automl/delete-auto-ml-analysis-model-deployment.md) | DELETE | `ZohoAnalytics.modeling.delete` | required | The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace. |
| [AutoML What If Analysis](../domains/dsml/automl/auto-ml-what-if-analysis.md) | POST | `ZohoAnalytics.modeling.create` | required | The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace. |
