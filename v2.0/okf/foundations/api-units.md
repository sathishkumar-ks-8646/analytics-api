---
type: Reference
title: "API units and frequency limits"
description: "What one call of each Zoho Analytics REST API v2 endpoint costs in API units, how variable (row-based and format-based) costs are computed, the three unit categories and the per-minute request ceilings they carry."
tags:
  - zoho-analytics
  - rest-api-v2
  - api-units
  - rate-limits
  - throttling
  - quotas
  - pricing
api_unit_categories:
  DML:
    frequency_limit_per_minute: 100
  BULK:
    frequency_limit_per_minute: 40
  METADATA:
    frequency_limit_per_minute: 60
endpoint_count: 205
machine_readable: "/references/endpoint-catalog.json"
sources:
  - id: api-gateway-config
    resource: "webapps/db/WEB-INF/gatewayxmls/zagateway-restapi.xml"
    title: "REST API gateway configuration - unit cost (UNITS), row basis (ROWS), unit category (TYPE) and per-category frequency limit (LIMIT) per api-id"
    author: team:zoho-analytics
  - id: api-security-config
    resource: "webapps/db/WEB-INF/securityxmls/security-restapi.xml"
    title: "REST API URL security configuration - api-id to method/path binding and per-endpoint request throttles (duration, threshold, lock-period)"
    author: team:zoho-analytics
  - id: endpoint-catalog
    resource: "/references/endpoint-catalog.json"
    title: Endpoint catalog - machine-readable copy of the per-endpoint unit costs
generated:
  by: process:build_okf
  at: 2026-10-29T08:27:56Z
status: stable
---

# Summary

Every call to a Zoho Analytics REST API v2 endpoint deducts **API units** from the organization's plan allowance, and is counted against a **per-minute request ceiling**. Both are driven by the same identifier - the internal `api-id` that the gateway resolves from the request method and path.

| Concept | What it is | Where it is enforced |
|---|---|---|
| **API unit cost** | The number of units one call deducts. Fixed for most endpoints; proportional to rows processed for bulk and copy operations. | Gateway, after the call completes - the actual row count is known by then. |
| **Unit category** | `DML`, `BULK` or `METADATA`. Every endpoint belongs to exactly one. | Gateway configuration. |
| **Frequency limit** | Requests per minute allowed for an organization within one unit category. | Gateway, before the call runs. Exceeding it fails the request. |
| **Endpoint throttle** | An additional per-user request threshold with a lockout period, configured on specific write-heavy or expensive endpoints. | URL security layer, before the call runs. |

Current allocation, usage and remainder for units are returned by [Get Resource Details](../domains/organization-management/org-info-and-settings/get-resource-details.md) under `resourceName: "apiUnits"`. Fractional usage is normal - several endpoints cost `0.1` or `0.5` units.

# How a Call Is Costed

1. The gateway resolves the request's method and path to an `api-id`.
2. It looks up the unit cost configured for that `api-id`.
3. If the `api-id` has a **row basis** (`N` rows), the charge is proportional:

   ```
   units charged = (rows processed / rows basis) * configured units
   ```

   For example, [Export Data](../domains/data-operations/sync-data-export/export-data-view.md) in CSV is configured as 3 units per 1000 rows, so exporting 2500 rows costs `2500 / 1000 * 3 = 7.5` units. There is no rounding up to a whole block - a 10-row export of the same report costs `0.03` units.
4. If there is no row basis, the configured number of units is charged once per request, regardless of payload size.
5. Units are charged on the **rows actually processed**, which is known only after the operation runs. A failed import still charges for the rows it managed to write before aborting.

Two consequences worth designing around:

- **Row-level APIs are charged per call, not per row.** [Add Row](../domains/data-operations/row-operations/add-row.md) costs `0.1` units for the single row it inserts - loading 100000 rows that way costs 10000 units, against roughly 1000 units for the same data through [Import Data](../domains/data-operations/sync-data-import/import-data-existing-table.md). Use the import APIs for bulk loads.
- **Job-style endpoints are free to start.** Creating an export or import job, polling its status and downloading its output all cost `0`; the units are charged once, on the job's payload.

# Unit Categories and Frequency Limits

Each endpoint belongs to one unit category. The category determines the per-minute request ceiling that the organization shares across every endpoint in it. The ceiling is scaled by a plan-specific multiplier, so a higher plan raises all three proportionally; the values below are the base configuration.

| Category | Base frequency limit | What it covers |
|---|---|---|
| `DML` | **100 requests/minute** | Row-level writes: [Add Row](../domains/data-operations/row-operations/add-row.md), [Update Row](../domains/data-operations/row-operations/update-rows.md), [Delete Row](../domains/data-operations/row-operations/delete-rows.md). |
| `BULK` | **40 requests/minute** | Import and export of data sets, synchronous and asynchronous, including job creation, status polling and downloads. |
| `METADATA` | **60 requests/minute** | Everything else - workspace, view, column, formula, user, sharing, publishing, schedule, alert and AutoML operations. |

Exceeding a category ceiling fails the request with an API-frequency error rather than a unit-exhaustion error; the two limits are independent, and a request can be rejected for frequency while plenty of units remain.

# Per-endpoint API Units

One row per documented endpoint. `Action` is the gateway action name and its `api-id`. `Units` is the configured cost, `Basis` says whether that cost applies per request or per block of rows.

## Organization Management

| Endpoint | Method | Path | Action (api-id) | Category | Units | Basis |
|---|---|---|---|---|---|---|
| [Get Resource Details](../domains/organization-management/org-info-and-settings/get-resource-details.md) | GET | `/restapi/v2/resources` | `GET_RESOURCE_DETAILS` (6008) | METADATA | 0.1 | per request |
| [Get Subscription Details](../domains/organization-management/org-info-and-settings/get-subscription-details.md) | GET | `/restapi/v2/subscription` | `GET_SUBSCRIPTION_DETAILS` (6006) | METADATA | 0.1 | per request |
| [Get Meta Details From Name](../domains/organization-management/org-info-and-settings/get-meta-details.md) | GET | `/restapi/v2/metadetails` | `GET_META_DETAILS` (3021) | METADATA | 0.1 | per request |
| [Get Org Workspaces](../domains/organization-management/org-level-listings/get-org-workspaces.md) | GET | `/restapi/v2/orgs/workspaces` | `GET_WORKSPACES` (3043) | METADATA | 0.1 | per request |
| [Get Org Dashboards](../domains/organization-management/org-level-listings/get-org-dashboards.md) | GET | `/restapi/v2/orgs/dashboards` | `GET_ORG_DASHBOARDS` (3044) | METADATA | 0.1 | per request |
| [Get Org Recent Items](../domains/organization-management/org-level-listings/get-org-recent-items.md) | GET | `/restapi/v2/orgs/recentitems` | `GET_RECENT_VIEWS` (3007) | METADATA | 0.1 | per request |
| [Get Org Access Restrictions](../domains/organization-management/security-controls/get-org-access-restrictions.md) | GET | `/restapi/v2/security-controls/access-restrictions` | `GET_ORG_ACCESS_RESTRICTIONS` (3067) | METADATA | 1 | per request |
| [Update Org Access Restrictions](../domains/organization-management/security-controls/update-org-access-restrictions.md) | PUT | `/restapi/v2/security-controls/access-restrictions` | `UPDATE_ORG_ACCESS_RESTRICTIONS` (3068) | METADATA | 1 | per request |
| [Get Workspace Access Restrictions](../domains/organization-management/security-controls/get-workspace-access-restrictions.md) | GET | `/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions` | `GET_WORKSPACE_ACCESS_RESTRICTIONS` (3069) | METADATA | 1 | per request |
| [Update Workspace Access Restrictions](../domains/organization-management/security-controls/update-workspace-access-restrictions.md) | PUT | `/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions` | `UPDATE_WORKSPACE_ACCESS_RESTRICTIONS` (3070) | METADATA | 1 | per request |

## Users & Groups

| Endpoint | Method | Path | Action (api-id) | Category | Units | Basis |
|---|---|---|---|---|---|---|
| [Get Users](../domains/users-and-groups/org-users/get-users.md) | GET | `/restapi/v2/users` | `GET_ORG_USERS` (6001) | METADATA | 1 | per request |
| [Add Users](../domains/users-and-groups/org-users/add-users.md) | POST | `/restapi/v2/users` | `ADD_ORG_USERS` (6002) | METADATA | 0.1 | per request |
| [Remove Users](../domains/users-and-groups/org-users/remove-users.md) | DELETE | `/restapi/v2/users` | `REMOVE_ORG_USERS` (6003) | METADATA | 0.1 | per request |
| [Activate Users](../domains/users-and-groups/org-users/activate-users.md) | PUT | `/restapi/v2/users/active` | `ACTIVATE_ORG_USERS` (6004) | METADATA | 0.1 | per request |
| [Deactivate Users](../domains/users-and-groups/org-users/de-activate-users.md) | PUT | `/restapi/v2/users/inactive` | `DEACTIVATE_ORG_USERS` (6005) | METADATA | 0.1 | per request |
| [Change User Role](../domains/users-and-groups/org-users/change-user-role.md) | PUT | `/restapi/v2/users/role` | `CHANGE_USER_ROLE` (6007) | METADATA | 0.1 | per request |
| [Get Org Admins](../domains/users-and-groups/org-users/get-org-admins.md) | GET | `/restapi/v2/orgadmins` | `GET_ORG_ADMINS` (4001) | METADATA | 0.1 | per request |
| [Get Custom Roles](../domains/users-and-groups/custom-roles/get-custom-roles.md) | GET | `/restapi/v2/orgs/roles` | `GET_ROLES` (6014) | METADATA | 1 | per request |
| [Create Custom Role](../domains/users-and-groups/custom-roles/create-custom-role.md) | POST | `/restapi/v2/orgs/roles` | `CREATE_ROLE` (6015) | METADATA | 1 | per request |
| [Update Custom Role](../domains/users-and-groups/custom-roles/update-custom-role.md) | PUT | `/restapi/v2/orgs/roles/{role-id}` | `UPDATE_ROLE` (6016) | METADATA | 1 | per request |
| [Delete Custom Role](../domains/users-and-groups/custom-roles/delete-custom-role.md) | DELETE | `/restapi/v2/orgs/roles/{role-id}` | `DELETE_ROLE` (6017) | METADATA | 1 | per request |
| [Get Workspace Users](../domains/users-and-groups/workspace-users/get-workspace-users.md) | GET | `/restapi/v2/workspaces/{workspace-id}/users` | `GET_WORKSPACE_USERS` (6009) | METADATA | 1 | per request |
| [Add Workspace Users](../domains/users-and-groups/workspace-users/add-workspace-users.md) | POST | `/restapi/v2/workspaces/{workspace-id}/users` | `ADD_WORKSPACE_USERS` (6010) | METADATA | 0.5 | per request |
| [Remove Workspace Users](../domains/users-and-groups/workspace-users/delete-workspace-users.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/users` | `REMOVE_WORKSPACE_USERS` (6011) | METADATA | 1 | per request |
| [Change Workspace Users Status](../domains/users-and-groups/workspace-users/change-workspace-users-status.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/users/status` | `CHANGE_WORKSPACE_USERS_STATUS` (6012) | METADATA | 0.5 | per request |
| [Change Workspace Users Role](../domains/users-and-groups/workspace-users/change-workspace-users-role.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/users/role` | `CHANGE_WORKSPACE_USERS_ROLE` (6013) | METADATA | 1 | per request |
| [Get Workspace Admins](../domains/users-and-groups/workspace-users/get-workspace-admins.md) | GET | `/restapi/v2/workspaces/{workspace-id}/admins` | `GET_WORKSPACE_ADMINS` (4004) | METADATA | 0.1 | per request |
| [Add Workspace Admins](../domains/users-and-groups/workspace-users/add-workspace-admins.md) | POST | `/restapi/v2/workspaces/{workspace-id}/admins` | `ADD_WORKSPACE_ADMINS` (4005) | METADATA | 5 | per request |
| [Remove Workspace Admins](../domains/users-and-groups/workspace-users/remove-workspace-admins.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/admins` | `REMOVE_WORKSPACE_ADMINS` (4006) | METADATA | 5 | per request |
| [Get Group List](../domains/users-and-groups/workspace-groups/get-groups.md) | GET | `/restapi/v2/workspaces/{workspace-id}/groups` | `GET_GROUPS` (4012) | METADATA | 0.1 | per request |
| [Create Group](../domains/users-and-groups/workspace-groups/create-group.md) | POST | `/restapi/v2/workspaces/{workspace-id}/groups` | `CREATE_GROUP` (4013) | METADATA | 1 | per request |
| [Rename Group](../domains/users-and-groups/workspace-groups/rename-group.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}` | `RENAME_GROUP` (4014) | METADATA | 0.1 | per request |
| [Add Group Members](../domains/users-and-groups/workspace-groups/add-group-members.md) | POST | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members` | `ADD_GROUP_MEMBERS` (4015) | METADATA | 0.1 | per request |
| [Remove Group Members](../domains/users-and-groups/workspace-groups/remove-group-members.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members` | `REMOVE_GROUP_MEMBERS` (4016) | METADATA | 0.1 | per request |
| [Delete Group](../domains/users-and-groups/workspace-groups/delete-group.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}` | `DELETE_GROUP` (4017) | METADATA | 1 | per request |
| [Get Group Details](../domains/users-and-groups/workspace-groups/get-group-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}` | `GET_GROUP_DETAILS` (4018) | METADATA | 0.1 | per request |

## Workspace Management

| Endpoint | Method | Path | Action (api-id) | Category | Units | Basis |
|---|---|---|---|---|---|---|
| [Create Workspace](../domains/workspace-management/workspace-operations/create-workspace.md) | POST | `/restapi/v2/workspaces` | `CREATE_WORKSPACE` (2001) | METADATA | 1 | per request |
| [Copy Workspace](../domains/workspace-management/workspace-operations/copy-workspace.md) | POST | `/restapi/v2/workspaces/{workspace-id}` | `COPY_WORKSPACE_WO_DATA` (2002) | METADATA | variable | see [Variable-cost operations](#variable-cost-operations) |
| [Rename Workspace](../domains/workspace-management/workspace-operations/rename-workspace.md) | PUT | `/restapi/v2/workspaces/{workspace-id}` | `RENAME_WORKSPACE` (2004) | METADATA | 1 | per request |
| [Delete Workspace](../domains/workspace-management/workspace-operations/delete-workspace.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}` | `DELETE_WORKSPACE` (2005) | METADATA | 1 | per request |
| [Export as Template](../domains/workspace-management/workspace-operations/export-as-template.md) | GET | `/restapi/v2/workspaces/{workspace-id}/template/data` | `EXPORT_AS_TEMPLATE` (3032) | METADATA | 5 | per request |
| [Get Workspace Secret Key](../domains/workspace-management/workspace-operations/get-workspace-secret-key.md) | GET | `/restapi/v2/workspaces/{workspace-id}/secretkey` | `GET_WORKSPACE_SECRETKEY` (3011) | METADATA | 0.5 | per request |
| [Get Workspace Info](../domains/workspace-management/workspace-operations/get-workspace-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}` | `GET_WORKSPACE_DETAILS` (3012) | METADATA | 0.1 | per request |
| [Get Folder List](../domains/workspace-management/workspace-folders/get-folders.md) | GET | `/restapi/v2/workspaces/{workspace-id}/folders` | `GET_FOLDERS` (3006) | METADATA | 0.1 | per request |
| [Create Folder](../domains/workspace-management/workspace-folders/create-folder.md) | POST | `/restapi/v2/workspaces/{workspace-id}/folders` | `CREATE_FOLDER` (2010) | METADATA | 1 | per request |
| [Rename Folder](../domains/workspace-management/workspace-folders/rename-folder.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}` | `RENAME_FOLDER` (2011) | METADATA | 1 | per request |
| [Delete Folder](../domains/workspace-management/workspace-folders/delete-folder.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}` | `DELETE_FOLDER` (2012) | METADATA | 1 | per request |
| [Change Folder Hierarchy](../domains/workspace-management/workspace-folders/change-folder-hierarchy.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/move` | `CHANGE_FOLDER_HIERARCHY` (2047) | METADATA | 1 | per request |
| [Change Folder Position](../domains/workspace-management/workspace-folders/change-folder-position.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/reorder` | `CHANGE_FOLDER_POSITION` (2048) | METADATA | 1 | per request |
| [Move Views To Folder](../domains/workspace-management/workspace-folders/move-views-to-folder.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/movetofolder` | `MOVE_VIEWS_TO_FOLDER` (2049) | METADATA | 1 | per request |
| [Make Default Folder](../domains/workspace-management/workspace-folders/make-default-folder.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/default` | `MAKE_DEFAULT_FOLDER` (2030) | METADATA | 1 | per request |
| [Add Default Workspace](../domains/workspace-management/workspace-preferences/add-default-workspace.md) | POST | `/restapi/v2/workspaces/{workspace-id}/default` | `ADD_DEFAULT_WORKSPACE` (3019) | METADATA | 0.1 | per request |
| [Remove Default Workspace](../domains/workspace-management/workspace-preferences/remove-default-workspace.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/default` | `REMOVE_DEFAULT_WORKSPACE` (3020) | METADATA | 0.1 | per request |
| [Add Favourite Workspace](../domains/workspace-management/workspace-preferences/add-favorite-workspace.md) | POST | `/restapi/v2/workspaces/{workspace-id}/favorite` | `ADD_FAVOURITE_WORKSPACE` (3015) | METADATA | 0.1 | per request |
| [Remove Favourite Workspace](../domains/workspace-management/workspace-preferences/remove-favorite-workspace.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/favorite` | `REMOVE_FAVOURITE_WORKSPACE` (3016) | METADATA | 0.1 | per request |
| [Enable Workspace for Domain Access](../domains/workspace-management/domain-and-white-label/enable-domain-workspace.md) | POST | `/restapi/v2/workspaces/{workspace-id}/wlaccess` | `ENABLE_DOMAIN_WORKSPACE` (3022) | METADATA | 0.1 | per request |
| [Disable Workspace for Domain Access](../domains/workspace-management/domain-and-white-label/disable-domain-workspace.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/wlaccess` | `DISABLE_DOMAIN_WORKSPACE` (3023) | METADATA | 0.1 | per request |
| [Get Linked Workspaces For Organization](../domains/workspace-management/linked-workspaces/get-linked-workspaces-for-organization.md) | GET | `/restapi/v2/linkedworkspaces` | `GET_LINKED_WORKSPACES_FOR_ORGANIZATION` (3086) | METADATA | 1 | per request |
| [Get Linked Workspaces For Master Workspace](../domains/workspace-management/linked-workspaces/get-linked-workspaces-for-master-workspace.md) | GET | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces` | `GET_LINKED_WORKSPACES_FOR_MASTER_WORKSPACE` (3087) | METADATA | 1 | per request |
| [Get Linkable Workspaces](../domains/workspace-management/linked-workspaces/get-linkable-workspaces.md) | GET | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/linkable` | `GET_LINKABLE_WORKSPACES` (3088) | METADATA | 1 | per request |
| [Get Workspace Linking Compatibility](../domains/workspace-management/linked-workspaces/get-workspace-linking-compatibility.md) | GET | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/compatibility` | `GET_WORKSPACE_LINKING_COMPATIBILITY` (3089) | METADATA | 1 | per request |
| [Link Workspaces](../domains/workspace-management/linked-workspaces/link-workspaces.md) | POST | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces` | `LINK_WORKSPACES` (2080) | METADATA | 3 | per request |
| [Sync Linked Workspaces](../domains/workspace-management/linked-workspaces/sync-linked-workspaces.md) | POST | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync` | `SYNC_LINKED_WORKSPACES` (2082) | METADATA | 3 | per request |
| [Get Linked Workspace Sync Details](../domains/workspace-management/linked-workspaces/get-linked-workspace-sync-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync` | `GET_LINKED_WORKSPACE_SYNC_DETAILS` (3090) | METADATA | 1 | per request |
| [Unlink Workspaces](../domains/workspace-management/linked-workspaces/unlink-workspaces.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces` | `UNLINK_WORKSPACES` (2081) | METADATA | 3 | per request |
| [Get Workspace Backups](../domains/workspace-management/workspace-backup-and-restore/get-workspace-backups.md) | GET | `/restapi/v2/workspaces/{workspace-id}/backups` | `GET_WORKSPACE_BACKUPS` (3082) | METADATA | 1 | per request |
| [Backup Workspace Now](../domains/workspace-management/workspace-backup-and-restore/backup-workspace-now.md) | POST | `/restapi/v2/workspaces/{workspace-id}/backups` | `BACKUP_WORKSPACE_NOW` (3083) | METADATA | 5 | per request |
| [Download Workspace Backup](../domains/workspace-management/workspace-backup-and-restore/download-workspace-backup.md) | GET | `/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/download` | `DOWNLOAD_WORKSPACE_BACKUP` (3084) | METADATA | 1 | per request |
| [Restore Workspace from Backup](../domains/workspace-management/workspace-backup-and-restore/restore-workspace-from-backup.md) | POST | `/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/restore` | `RESTORE_WORKSPACE_BACKUP` (3085) | METADATA | 10 | per request |
| [Get Workspace Backup Status](../domains/workspace-management/workspace-backup-and-restore/get-workspace-backup-status.md) | GET | `/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/status` | `GET_WORKSPACE_BACKUP_STATUS` (3096) | METADATA | 0.5 | per request |
| [Get Workspace Restore Status](../domains/workspace-management/workspace-backup-and-restore/get-workspace-restore-status.md) | GET | `/restapi/v2/workspaces/{workspace-id}/restores/{restore-id}/status` | `GET_WORKSPACE_RESTORE_STATUS` (3097) | METADATA | 0.5 | per request |

## Data Modeling & Schema

| Endpoint | Method | Path | Action (api-id) | Category | Units | Basis |
|---|---|---|---|---|---|---|
| [Create Table](../domains/data-modeling-and-schema/table-and-schema/create-table.md) | POST | `/restapi/v2/workspaces/{workspace-id}/tables` | `CREATE_TABLE` (2006) | METADATA | 1 | per request |
| [Get Table Metadata](../domains/data-modeling-and-schema/table-and-schema/get-table-metadata.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/metadata` | `GET_TABLE_METADATA` (3053) | METADATA | 1 | per request |
| [Add Column](../domains/data-modeling-and-schema/columns/add-column.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns` | `ADD_COLUMN` (2013) | METADATA | 15 | per request |
| [Rename Column](../domains/data-modeling-and-schema/columns/rename-column.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}` | `RENAME_COLUMN` (2014) | METADATA | 5 | per request |
| [Delete Column](../domains/data-modeling-and-schema/columns/delete-column.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}` | `DELETE_COLUMN` (2015) | METADATA | 10 | per request |
| [Hide Columns](../domains/data-modeling-and-schema/columns/hide-columns.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/hide` | `HIDE_COLUMNS` (2018) | METADATA | 1 | per request |
| [Show Columns](../domains/data-modeling-and-schema/columns/show-columns.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/show` | `SHOW_COLUMNS` (2019) | METADATA | 1 | per request |
| [Get Column Dependents](../domains/data-modeling-and-schema/columns/get-column-dependents.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/dependents` | `GET_COLUMN_DEPENDENTS` (3030) | METADATA | 0.1 | per request |
| [Sort Data by Columns](../domains/data-modeling-and-schema/columns/sort-data-by-columns.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data/sort` | `SORT_DATA_BY_COLUMNS` (2064) | METADATA | 1 | per request |
| [Reorder Columns](../domains/data-modeling-and-schema/columns/reorder-columns.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/reorder` | `REORDER_COLUMNS` (2063) | METADATA | 1 | per request |
| [Add Lookup](../domains/data-modeling-and-schema/lookups-and-relationships/add-lookup.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup` | `ADD_LOOKUP` (2016) | METADATA | 1 | per request |
| [Remove Lookup](../domains/data-modeling-and-schema/lookups-and-relationships/remove-lookup.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup` | `REMOVE_LOOKUP` (2017) | METADATA | 2 | per request |
| [Get Query Tables](../domains/data-modeling-and-schema/query-tables/get-query-tables.md) | GET | `/restapi/v2/workspaces/{workspace-id}/querytables` | `GET_QUERY_TABLES` (3064) | METADATA | 0.1 | per request |
| [Create Query Table](../domains/data-modeling-and-schema/query-tables/create-query-table.md) | POST | `/restapi/v2/workspaces/{workspace-id}/querytables` | `CREATE_QT` (2037) | METADATA | 15 | per request |
| [Edit Query Table](../domains/data-modeling-and-schema/query-tables/edit-query-table.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}` | `EDIT_QT` (2038) | METADATA | 15 | per request |
| [Get Query Table Details](../domains/data-modeling-and-schema/query-tables/get-query-table-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}` | `GET_QUERYTABLE_DETAILS` (3047) | METADATA | 1 | per request |
| [Get Custom Formulas](../domains/data-modeling-and-schema/formula-columns/get-custom-formula-list.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas` | `GET_FORMULA_COLUMN` (3036) | METADATA | 0.1 | per request |
| [Add Custom Formula](../domains/data-modeling-and-schema/formula-columns/add-formula-column.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas` | `ADD_FORMULA_COLUMN` (2041) | METADATA | 15 | per request |
| [Edit Custom Formula](../domains/data-modeling-and-schema/formula-columns/edit-formula-column.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas/{formula-id}` | `EDIT_FORMULA_COLUMN` (2042) | METADATA | 15 | per request |
| [Delete Custom Formula](../domains/data-modeling-and-schema/formula-columns/delete-formula-column.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas/{formula-id}` | `DELETE_FORMULA_COLUMN` (2043) | METADATA | 2 | per request |
| [Copy Custom Formulas](../domains/data-modeling-and-schema/formula-columns/copy-formulas.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/formulas/copy` | `COPY_FORMULAS` (2021) | METADATA | 1 | per request |
| [Get Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-list.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas` | `GET AGGREGATE FORMULA` (3037) | METADATA | 0.1 | per request |
| [Add Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/add-aggregate-formula.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas` | `ADD_AGG_FORMULA` (2044) | METADATA | 5 | per request |
| [Edit Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/edit-aggregate-formula.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas/{formula-id}` | `EDIT_AGG_FORMULA` (2045) | METADATA | 5 | per request |
| [Delete Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/delete-aggregate-formula.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas/{formula-id}` | `DELETE AGG FORMULA` (2046) | METADATA | 1 | per request |
| [Get Unified Metrics in Workspace](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formulas-in-workspace.md) | GET | `/restapi/v2/workspaces/{workspace-id}/aggregateformulas` | `GET_AGGREGATE_FORMULAS_IN_WORKSPACE` (3039) | METADATA | 1 | per request |
| [Get Aggregate Formula Dependents](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-dependents.md) | GET | `/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/dependents` | `GET_AGGREGATE_FORMULA_DEPENDENTS` (3040) | METADATA | 1 | per request |
| [Get Aggregate Formula Value](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-value.md) | GET | `/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/value` | `GET_AGGREGATE_FORMULA_VALUE` (3041) | METADATA | 1 | per request |
| [Create Variable](../domains/data-modeling-and-schema/workspace-variables/create-variable.md) | POST | `/restapi/v2/workspaces/{workspace-id}/variables` | `CREATE_VARIABLE` (2025) | METADATA | 1 | per request |
| [Edit Variable](../domains/data-modeling-and-schema/workspace-variables/update-variable.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}` | `UPDATE_VARIABLE` (2026) | METADATA | 1 | per request |
| [Delete Variable](../domains/data-modeling-and-schema/workspace-variables/delete-variable.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}` | `DELETE_VARIABLE` (2027) | METADATA | 1 | per request |
| [Get Variables](../domains/data-modeling-and-schema/workspace-variables/get-variables.md) | GET | `/restapi/v2/workspaces/{workspace-id}/variables` | `GET_VARIABLES` (2028) | METADATA | 1 | per request |
| [Get Variable Details](../domains/data-modeling-and-schema/workspace-variables/get-variable-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}` | `GET_VARIABLE_DETAILS` (2029) | METADATA | 1 | per request |

## Data Operations

| Endpoint | Method | Path | Action (api-id) | Category | Units | Basis |
|---|---|---|---|---|---|---|
| [Import Data into a New Table (Synchronous)](../domains/data-operations/sync-data-import/import-data-new-table.md) | POST | `/restapi/v2/workspaces/{workspace-id}/data` | `INITIATE_IMPORT` (8001) | BULK | variable | see [Variable-cost operations](#variable-cost-operations) |
| [Import Data into an Existing Table (Synchronous)](../domains/data-operations/sync-data-import/import-data-existing-table.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data` | `INITIATE_IMPORT` (8001) | BULK | variable | see [Variable-cost operations](#variable-cost-operations) |
| [Create Import Job for a New Table (Asynchronous)](../domains/data-operations/async-data-import/create-import-job-new-table.md) | POST | `/restapi/v2/bulk/workspaces/{workspace-id}/data` | `INITIATE_IMPORT` (8001) | BULK | variable | see [Variable-cost operations](#variable-cost-operations) |
| [Create Import Job for an Existing Table (Asynchronous)](../domains/data-operations/async-data-import/create-import-job-existing-table.md) | POST | `/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data` | `INITIATE_IMPORT` (8001) | BULK | variable | see [Variable-cost operations](#variable-cost-operations) |
| [Batch Import Data into New Table](../domains/data-operations/async-data-import/batch-import-new-table.md) | POST | `/restapi/v2/bulk/workspaces/{workspace-id}/data/batch` | `BATCH_IMPORT_FILE_UPLOAD` (8005) | BULK | variable | see [Variable-cost operations](#variable-cost-operations) |
| [Batch Import Data into Existing Table](../domains/data-operations/async-data-import/batch-import-existing-table.md) | POST | `/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data/batch` | `BATCH_IMPORT_FILE_UPLOAD` (8005) | BULK | variable | see [Variable-cost operations](#variable-cost-operations) |
| [Get Import Job Details](../domains/data-operations/async-data-import/get-import-job-details.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/importjobs/{job-id}` | `IMPORT_JOB_STATUS` (9003) | METADATA | 0 | not charged |
| [Export Data from a View](../domains/data-operations/sync-data-export/export-data-view.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data` | `INITIATE_EXPORT` (7001) | BULK | variable | see [Variable-cost operations](#variable-cost-operations) |
| [Create Export Job using SQL Query (Asynchronous)](../domains/data-operations/async-data-export/create-export-job-sql-query.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/data` | `INITIATE_EXPORT` (7001) | BULK | variable | see [Variable-cost operations](#variable-cost-operations) |
| [Create Export Job using View ID (Asynchronous)](../domains/data-operations/async-data-export/create-export-job-view-id.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data` | `INITIATE_EXPORT` (7001) | BULK | variable | see [Variable-cost operations](#variable-cost-operations) |
| [Get Export Job Details](../domains/data-operations/async-data-export/get-export-job-details.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/exportjobs/{job-id}` | `EXPORT_JOB_STATUS` (9001) | METADATA | 0 | not charged |
| [Download Exported Data](../domains/data-operations/async-data-export/download-exported-data.md) | GET | `/restapi/v2/bulk/workspaces/{workspace-id}/exportjobs/{job-id}/data` | `DOWNLOAD_FILE` (9002) | METADATA | 0 | not charged |
| [Add Row](../domains/data-operations/row-operations/add-row.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows` | `ADD_ROW` (1001) | DML | 0.1 | per request |
| [Update Row](../domains/data-operations/row-operations/update-rows.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows` | `UPDATE_ROW` (1002) | DML | 0.3 | per request |
| [Delete Row](../domains/data-operations/row-operations/delete-rows.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows` | `DELETE_ROW` (1003) | DML | 0.1 | per request |
| [Sync Data](../domains/data-operations/data-sync-and-connectivity/sync-datasource.md) | POST | `/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}/sync` | `SYNC_DATA` (3025) | METADATA | 5 | per request |
| [Refetch Data](../domains/data-operations/data-sync-and-connectivity/refetch-datasource.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/sync` | `REFETCH_DATA` (3026) | METADATA | 2 | per request |
| [Update Datasource Connection](../domains/data-operations/data-sync-and-connectivity/update-datasource-connection.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}` | `UPDATE_DATASOURCE_CONNECTION` (3028) | METADATA | 1 | per request |
| [Get Datasources](../domains/data-operations/data-sync-and-connectivity/get-datasources.md) | GET | `/restapi/v2/workspaces/{workspace-id}/datasources` | `GET_DATASOURCES` (3024) | METADATA | 1 | per request |
| [Get Last Import Details](../domains/data-operations/data-sync-and-connectivity/get-last-import-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/importdetails` | `GET_LAST_IMPORT_DETAILS` (3027) | METADATA | 0.1 | per request |

## Views Management

| Endpoint | Method | Path | Action (api-id) | Category | Units | Basis |
|---|---|---|---|---|---|---|
| [Save As View](../domains/views-management/view-operations/save-as-view.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/saveas` | `SAVEAS_VIEWS` (2007) | METADATA | 1 | per request |
| [Copy Views](../domains/views-management/view-operations/copy-views.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/copy` | `COPY_VIEWS` (2020) | METADATA | 1 | per request |
| [Create Similar Views](../domains/views-management/view-operations/create-similar-views.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/similarviews` | `CREATE_SIMILAR_VIEWS` (2022) | METADATA | 1 | per request |
| [Rename View](../domains/views-management/view-operations/rename-view.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}` | `RENAME_VIEW` (2008) | METADATA | 1 | per request |
| [Delete View](../domains/views-management/view-operations/delete-view.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}` | `DELETE_VIEW` (2009) | METADATA | 2 | per request |
| [Get View List](../domains/views-management/view-operations/get-views.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views` | `GET_VIEWS` (3005) | METADATA | 0.1 | per request |
| [Get View Details](../domains/views-management/view-operations/get-view-details.md) | GET | `/restapi/v2/views/{view-id}` | `GET_VIEW_DETAILS` (3013) | METADATA | 0.1 | per request |
| [Get View URL](../domains/views-management/view-operations/get-view-url.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish` | `GET_VIEW_URL` (5001) | METADATA | 0.1 | per request |
| [Get View Dependents](../domains/views-management/view-operations/get-view-dependents.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/dependents` | `GET_VIEW_DEPENDENTS` (3034) | METADATA | 1 | per request |
| [Add Favourite View](../domains/views-management/view-preferences/add-favorite-view.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/favorite` | `ADD_FAVOURITE_VIEW` (3017) | METADATA | 0.1 | per request |
| [Remove Favourite View](../domains/views-management/view-preferences/remove-favorite-view.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/favorite` | `REMOVE_FAVOURITE_VIEW` (3018) | METADATA | 0.1 | per request |
| [Get Trash Views](../domains/views-management/trash-management/get-trash-views.md) | GET | `/restapi/v2/workspaces/{workspace-id}/trash` | `GET_TRASH_VIEWS` (3035) | METADATA | 1 | per request |
| [Restore Trash View](../domains/views-management/trash-management/restore-trash-view.md) | POST | `/restapi/v2/workspaces/{workspace-id}/trash/{view-id}` | `RESTORE_TRASH_VIEW` (2039) | METADATA | 3 | per request |
| [Delete Trash View](../domains/views-management/trash-management/delete-trash-view.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/trash/{view-id}` | `DELETE_TRASH_VIEW` (2040) | METADATA | 3 | per request |
| [Auto Analyse View](../domains/views-management/auto-analysis/auto-analyse-view.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/autoanalyse` | `AUTO_ANALYSIS_VIEW` (2023) | METADATA | 1 | per request |
| [Auto Analyse Column](../domains/views-management/auto-analysis/auto-analyse-column.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/autoanalyse` | `AUTO_ANALYSIS_COLUMN` (2024) | METADATA | 1 | per request |
| [Get Tags List](../domains/views-management/tags/get-tags.md) | GET | `/restapi/v2/workspaces/{workspace-id}/tags` | `GET_TAGS` (3071) | METADATA | 0.5 | per request |
| [Get Tagged Views](../domains/views-management/tags/get-tagged-views.md) | GET | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views` | `GET_TAGGED_VIEWS` (3072) | METADATA | 0.5 | per request |
| [Get View Tags](../domains/views-management/tags/get-view-tags.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags` | `GET_VIEW_TAGS` (3073) | METADATA | 0.5 | per request |
| [Create Tag](../domains/views-management/tags/create-tag.md) | POST | `/restapi/v2/workspaces/{workspace-id}/tags` | `CREATE_TAG` (2073) | METADATA | 0.5 | per request |
| [Update Tag](../domains/views-management/tags/update-tag.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}` | `UPDATE_TAG` (2074) | METADATA | 0.5 | per request |
| [Delete Tag](../domains/views-management/tags/delete-tag.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}` | `DELETE_TAG` (2075) | METADATA | 0.5 | per request |
| [Add Tag To Multiple Views](../domains/views-management/tags/add-tag-to-views.md) | POST | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views` | `ADD_TAG_TO_VIEWS` (2076) | METADATA | 0.5 | per request |
| [Remove Tag From Multiple Views](../domains/views-management/tags/remove-tag-from-views.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views` | `REMOVE_TAG_FROM_VIEWS` (2077) | METADATA | 0.5 | per request |
| [Add Multiple Tags To View](../domains/views-management/tags/add-tags-to-view.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags` | `ADD_TAGS_TO_VIEW` (2078) | METADATA | 0.5 | per request |
| [Remove Multiple Tags From View](../domains/views-management/tags/remove-tags-from-view.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags` | `REMOVE_TAGS_FROM_VIEW` (2079) | METADATA | 0.5 | per request |

## Reports & Dashboards

| Endpoint | Method | Path | Action (api-id) | Category | Units | Basis |
|---|---|---|---|---|---|---|
| [Create Report](../domains/reports-and-dashboards/reports/create-report.md) | POST | `/restapi/v2/workspaces/{workspace-id}/reports` | `CREATE_ANALYSISVIEW` (2031) | METADATA | 5 | per request |
| [Read Report Metadata](../domains/reports-and-dashboards/reports/get-report-metadata.md) | GET | `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata` | `GET_REPORT_METADATA` (3052) | METADATA | 0.1 | per request |
| [Update Report](../domains/reports-and-dashboards/reports/update-report.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}` | `UPDATE_ANALYSISVIEW` (2032) | METADATA | 5 | per request |
| [Create Dashboard](../domains/reports-and-dashboards/dashboards/create-dashboard.md) | POST | `/restapi/v2/workspaces/{workspace-id}/dashboards` | `CREATE_DASHBOARD` (2060) | METADATA | 5 | per request |
| [Read Dashboard Metadata](../domains/reports-and-dashboards/dashboards/get-dashboard-metadata.md) | GET | `/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}/metadata` | `GET_DASHBOARD_METADATA` (2061) | METADATA | 1 | per request |
| [Update Dashboard](../domains/reports-and-dashboards/dashboards/update-dashboard.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}` | `UPDATE_DASHBOARD` (2062) | METADATA | 5 | per request |

## Share & Publish

| Endpoint | Method | Path | Action (api-id) | Category | Units | Basis |
|---|---|---|---|---|---|---|
| [Get Workspace Shared Details](../domains/share-and-publish/sharing/get-workspace-shared-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/share` | `GET_WORKSPACE_SHARE_INFO` (4007) | METADATA | 3 | per request |
| [Share Views](../domains/share-and-publish/sharing/share-views.md) | POST | `/restapi/v2/workspaces/{workspace-id}/share` | `SHARE_VIEWS` (4008) | METADATA | 5 | per request |
| [Update Shared Details](../domains/share-and-publish/sharing/update-shared-details-for-view.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share` | `UPDATE_SHARED_DETAILS_FOR_VIEW` (4020) | METADATA | 0.1 | per request |
| [Get Shared Details](../domains/share-and-publish/sharing/get-shared-details-for-views.md) | GET | `/restapi/v2/workspaces/{workspace-id}/share/shareddetails` | `GET_SHARED_DETAILS_FOR_VIEW` (4010) | METADATA | 0.1 | per request |
| [Remove Shared Views](../domains/share-and-publish/sharing/remove-share.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/share` | `REMOVE_SHARE` (4009) | METADATA | 5 | per request |
| [Get My Permissions](../domains/share-and-publish/sharing/get-user-permissions.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share/userpermissions` | `GET_MY_PERMISSIONS` (4011) | METADATA | 0.1 | per request |
| [Make View Public](../domains/share-and-publish/publish/make-views-public.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/public` | `MAKE_VIEW_PUBLIC` (5013) | METADATA | 1 | per request |
| [Remove Public Permission](../domains/share-and-publish/publish/remove-public-permission.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/public` | `REMOVE_PUBLIC_VIEW` (5014) | METADATA | 1 | per request |
| [Get Private URL](../domains/share-and-publish/publish/get-private-url.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink` | `GET_PRIVATE_URL` (5003) | METADATA | 0.1 | per request |
| [Create Private URL](../domains/share-and-publish/publish/create-private-url.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink` | `CREATE_PRIVATE_URL` (5004) | METADATA | 1 | per request |
| [Remove Private Access](../domains/share-and-publish/publish/remove-private-access.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink` | `REMOVE_PRIVATE_PERMISSION` (5012) | METADATA | 1 | per request |
| [Get Publish Configurations](../domains/share-and-publish/publish/get-publish-configurations.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config` | `GET_PUBLISH_CONFIGURATIONS` (5015) | METADATA | 0.1 | per request |
| [Update Publish Configurations](../domains/share-and-publish/publish/update-publish-configurations.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config` | `UPDATE_PUBLISH_CONFIGURATIONS` (5016) | METADATA | 0.5 | per request |
| [Get Embed URL](../domains/share-and-publish/embed-url/get-embed-url.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embed` | `GET_EMBED_URL` (5002) | METADATA | 1 | per request |
| [Fetch All Embed URLs](../domains/share-and-publish/embed-url/get-embed-urls.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embedurls` | `FETCH_ALL_EMBED_URLS` (5017) | METADATA | 0.5 | per request |
| [Delete Embed URL](../domains/share-and-publish/embed-url/delete-embed-url.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embed` | `DELETE_EMBED_URL` (5018) | METADATA | 0.5 | per request |
| [Get Slide List](../domains/share-and-publish/slideshow-management/get-slideshows.md) | GET | `/restapi/v2/workspaces/{workspace-id}/slides` | `GET_SLIDE_LIST` (5005) | METADATA | 1 | per request |
| [Get Slide URL](../domains/share-and-publish/slideshow-management/get-slideshow-url.md) | GET | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}/publish` | `GET_SLIDE_URL` (5006) | METADATA | 1 | per request |
| [Get Slide Info](../domains/share-and-publish/slideshow-management/get-slideshow-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}` | `GET_SLIDE_INFO` (5007) | METADATA | 1 | per request |
| [Create Slide Show](../domains/share-and-publish/slideshow-management/create-slideshow.md) | POST | `/restapi/v2/workspaces/{workspace-id}/slides` | `CREATE_SLIDE_SHOW` (5008) | METADATA | 2 | per request |
| [Update Slide Show](../domains/share-and-publish/slideshow-management/update-slideshow.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}` | `UPDATE_SLIDE_SHOW` (5009) | METADATA | 2 | per request |
| [Delete Slide Show](../domains/share-and-publish/slideshow-management/delete-slideshow.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}` | `DELETE_SLIDE_SHOW` (5010) | METADATA | 2 | per request |

## Schedules & Alerts

| Endpoint | Method | Path | Action (api-id) | Category | Units | Basis |
|---|---|---|---|---|---|---|
| [Get Email Schedules](../domains/schedules-and-alerts/email-schedules/get-email-schedules.md) | GET | `/restapi/v2/workspaces/{workspace-id}/emailschedules` | `GET EMAIL SCHEDULES` (3038) | METADATA | 1 | per request |
| [Create Email Schedule](../domains/schedules-and-alerts/email-schedules/create-email-schedule.md) | POST | `/restapi/v2/workspaces/{workspace-id}/emailschedules` | `CREATE_EMAIL_SCHEDULE` (2050) | METADATA | 3 | per request |
| [Update Email Schedule](../domains/schedules-and-alerts/email-schedules/update-email-schedule.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}` | `UPDATE_EMAIL_SCHEDULE` (2051) | METADATA | 3 | per request |
| [Delete Email Schedule](../domains/schedules-and-alerts/email-schedules/delete-email-schedule.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}` | `DELETE_EMAIL_SCHEDULE` (2052) | METADATA | 3 | per request |
| [Change Email Schedule Status](../domains/schedules-and-alerts/email-schedules/change-email-schedule-status.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}/status` | `CHANGE_EMAIL_SCHEDULE_STATUS` (2053) | METADATA | 1 | per request |
| [Trigger Email Schedule](../domains/schedules-and-alerts/email-schedules/trigger-email-schedule.md) | POST | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}` | `TRIGGER_EMAIL_SCHEDULE` (2054) | METADATA | 1 | per request |
| [Get Alerts In Workspace](../domains/schedules-and-alerts/data-alerts/get-alerts-in-workspace.md) | GET | `/restapi/v2/workspaces/{workspace-id}/alerts` | `GET_ALERTS_IN_WORKSPACE` (3091) | METADATA | 2 | per request |
| [Get Alerts In View](../domains/schedules-and-alerts/data-alerts/get-alerts-in-view.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts` | `GET_ALERTS_IN_VIEW` (3092) | METADATA | 0.5 | per request |
| [Get View Metadata For Alert](../domains/schedules-and-alerts/data-alerts/get-view-metadata-for-alert.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts/metadata` | `GET_VIEW_METADATA_FOR_ALERT` (3093) | METADATA | 1 | per request |
| [Get Alert Configuration](../domains/schedules-and-alerts/data-alerts/get-alert-configuration.md) | GET | `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}` | `GET_ALERT_CONFIGURATION` (3094) | METADATA | 1 | per request |
| [Create Alert](../domains/schedules-and-alerts/data-alerts/create-alert.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts` | `CREATE_ALERT` (2083) | METADATA | 3 | per request |
| [Update Alert](../domains/schedules-and-alerts/data-alerts/update-alert.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}` | `UPDATE_ALERT` (2084) | METADATA | 3 | per request |
| [Delete Alerts](../domains/schedules-and-alerts/data-alerts/delete-alerts.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/alerts` | `DELETE_ALERTS` (2085) | METADATA | 2 | per request |
| [Change Alert Status](../domains/schedules-and-alerts/data-alerts/change-alert-status.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/alerts/status` | `CHANGE_ALERT_STATUS` (2086) | METADATA | 1 | per request |
| [Run Alert](../domains/schedules-and-alerts/data-alerts/run-alert.md) | POST | `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/execute` | `RUN_ALERT` (2087) | METADATA | 1 | per request |
| [Get Alert Events](../domains/schedules-and-alerts/data-alerts/get-alert-events.md) | GET | `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/events` | `GET_ALERT_EVENTS` (3095) | METADATA | 1 | per request |

## Data Science & Machine Learning (AutoML)

| Endpoint | Method | Path | Action (api-id) | Category | Units | Basis |
|---|---|---|---|---|---|---|
| [Get AutoML Analysis In Org](../domains/dsml/automl/get-auto-ml-analysis-in-org.md) | GET | `/restapi/v2/automl/analysis` | `GET_AUTOML_ANALYSIS_IN_ORGANIZATION` (3054) | METADATA | 2 | per request |
| [Get AutoML Analysis In Workspace](../domains/dsml/automl/get-auto-ml-analysis-in-workspace.md) | GET | `/restapi/v2/automl/workspaces/{workspace-id}/analysis` | `GET_AUTOML_ANALYSIS_IN_Workspace` (3055) | METADATA | 1 | per request |
| [Get AutoML Analysis Details](../domains/dsml/automl/get-auto-ml-analysis-details.md) | GET | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}` | `GET_AUTOML_ANALYSIS_DETAILS` (3056) | METADATA | 1 | per request |
| [Get Deployments For A Model](../domains/dsml/automl/get-deployments-for-model.md) | GET | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments` | `GET_DEPLOYMENTS_FOR_A_MODEL` (3057) | METADATA | 1 | per request |
| [Create AutoML Analysis](../domains/dsml/automl/create-auto-ml-analysis.md) | POST | `/restapi/v2/automl/workspaces/{workspace-id}/analysis` | `CREATE_AUTOML_ANALYSIS` (2065) | METADATA | 3 | per request |
| [Delete AutoML Analysis](../domains/dsml/automl/delete-auto-ml-analysis.md) | DELETE | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}` | `DELETE_AUTOML_ANALYSIS` (2066) | METADATA | 2 | per request |
| [Delete AutoML Analysis Model](../domains/dsml/automl/delete-auto-ml-analysis-model.md) | DELETE | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}` | `DELETE_AUTOML_ANALYSIS_MODEL` (2067) | METADATA | 2 | per request |
| [Create AutoML Analysis Deployment](../domains/dsml/automl/create-auto-ml-analysis-deployment.md) | POST | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments` | `CREATE_AUTOML_ANALYSIS_DEPLOYMENT` (2068) | METADATA | 3 | per request |
| [Run AutoML Analysis](../domains/dsml/automl/run-auto-ml-analysis.md) | POST | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}/execute` | `RUN_AUTOML_ANALYSIS_DEPLOYMENT` (2069) | METADATA | 2 | per request |
| [Delete AutoML Analysis Model Deployment](../domains/dsml/automl/delete-auto-ml-analysis-model-deployment.md) | DELETE | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}` | `DELETE_AUTOML_ANALYSIS_DEPLOYMENT` (2070) | METADATA | 2 | per request |
| [AutoML What If Analysis](../domains/dsml/automl/auto-ml-what-if-analysis.md) | POST | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/whatif` | `AUTOML_WHAT_IF_ANALYSIS` (2071) | METADATA | 1 | per request |

# Variable-cost Operations

Three operation families do not have a single fixed cost. The endpoint resolves to a gateway action that charges `0`, and the real charge is applied against a second action chosen from the request payload. A fourth family, large-data export, is free throughout.

## Export (synchronous and asynchronous)

[Export Data](../domains/data-operations/sync-data-export/export-data-view.md), [Create Export Job using View ID](../domains/data-operations/async-data-export/create-export-job-view-id.md) and [Create Export Job using SQL Query](../domains/data-operations/async-data-export/create-export-job-sql-query.md) all resolve to `INITIATE_EXPORT` (7001), which costs `0`. The charge is applied when the data is produced, from the requested output format and the view type:

| Condition on the request | Charged action | Cost |
|---|---|---|
| `responseFormat` is `image`, or `pdf` on a chart / analysis view | `EXPORT_CHART` (7004) | **10 units** per request |
| `responseFormat` is `pdf` (any other view type) | `EXPORT_PDF` (7003) | **5 units** per 1000 rows |
| `responseFormat` is `html` | `EXPORT_HTML` (7005) | **15 units** per request |
| The exported view is a dashboard | `EXPORT_DASHBOARD` (7006) | **15 units** per request |
| Anything else - `csv`, `json`, `xml`, `xls` | `EXPORT_DATA` (7002) | **3 units** per 1000 rows |

The conditions are evaluated in that order, so a PDF of a chart is costed as a chart export, not as a PDF export.

[Get Export Job Details](../domains/data-operations/async-data-export/get-export-job-details.md) (`EXPORT_JOB_STATUS`, 9001) and [Download Exported Data](../domains/data-operations/async-data-export/download-exported-data.md) (`DOWNLOAD_FILE`, 9002) cost `0` - polling and downloading are free.

## Import (synchronous, asynchronous and batch)

[Import Data](../domains/data-operations/sync-data-import/import-data-existing-table.md), [Create Import Job](../domains/data-operations/async-data-import/create-import-job-existing-table.md) and the [batch import](../domains/data-operations/async-data-import/batch-import-existing-table.md) endpoints resolve to `INITIATE_IMPORT` (8001) or `BATCH_IMPORT_FILE_UPLOAD` (8005), both `0`. The charge is applied to the rows actually written, from `importType`:

| `importType` | Charged action | Cost |
|---|---|---|
| `append` | `IMPORT` (8002) | **10 units** per 1000 rows |
| `truncateadd` | `IMPORT_TRUNCATE_ADD` (8003) | **10 units** per 1000 rows |
| `updateadd` | `IMPORT_UPDATE_ADD` (8004) | **15 units** per 1000 rows |

For a batch import the charge is applied once, when the final batch is committed - the individual file-upload calls are free. A failed or aborted import is still charged for the rows it wrote before failing.

[Get Import Job Details](../domains/data-operations/async-data-import/get-import-job-details.md) (`IMPORT_JOB_STATUS`, 9003) costs `0`.

## Copy Workspace

[Copy Workspace](../domains/workspace-management/workspace-operations/copy-workspace.md) is costed from whether data is copied:

| Request | Charged action | Cost |
|---|---|---|
| `copyData` false / absent | `COPY_WORKSPACE_WO_DATA` (2002) | **25 units** per request |
| `copyData` true | `COPY_WORKSPACE_WITH_DATA` (2003) plus the base | **25 units** plus **1 unit** per 1000 rows copied |

The 25-unit base is always included - the with-data cost is additive, not a replacement.

## Large-data Export

The large-data export actions (`INITIATE_LARGEDATA_EXPORT` 11001, `DOWNLOAD_LARGEDATA_CHUNK` 11002, `DOWNLOAD_LARGEDATA_FILE` 11003, `GET_LARGEDATA_EXPORT_STATUS` 11004) are all configured at `0` units.

# Endpoint-specific Throttles

These endpoints carry an extra request threshold on top of the category frequency limit. Crossing the threshold inside the window locks the caller out of that endpoint for the lock period - retrying in a tight loop extends nothing and only burns the lockout.

| Endpoint | Action (api-id) | Throttle |
|---|---|---|
| [Add Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/add-aggregate-formula.md) | `ADD_AGG_FORMULA` (2044) | 20 requests per user per minute, 10-minute lockout on breach |
| [Delete Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/delete-aggregate-formula.md) | `DELETE AGG FORMULA` (2046) | 20 requests per user per minute, 10-minute lockout on breach |
| [Edit Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/edit-aggregate-formula.md) | `EDIT_AGG_FORMULA` (2045) | 20 requests per user per minute, 10-minute lockout on breach |
| [Get Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-list.md) | `GET AGGREGATE FORMULA` (3037) | 30 requests per user per minute, 10-minute lockout on breach |
| [Add Custom Formula](../domains/data-modeling-and-schema/formula-columns/add-formula-column.md) | `ADD_FORMULA_COLUMN` (2041) | 20 requests per user per minute, 10-minute lockout on breach |
| [Delete Custom Formula](../domains/data-modeling-and-schema/formula-columns/delete-formula-column.md) | `DELETE_FORMULA_COLUMN` (2043) | 30 requests per user per minute, 10-minute lockout on breach |
| [Edit Custom Formula](../domains/data-modeling-and-schema/formula-columns/edit-formula-column.md) | `EDIT_FORMULA_COLUMN` (2042) | 20 requests per user per minute, 10-minute lockout on breach |
| [Get Custom Formulas](../domains/data-modeling-and-schema/formula-columns/get-custom-formula-list.md) | `GET_FORMULA_COLUMN` (3036) | 30 requests per user per minute, 10-minute lockout on breach |
| [Create Query Table](../domains/data-modeling-and-schema/query-tables/create-query-table.md) | `CREATE_QT` (2037) | 20 requests per user per minute, 10-minute lockout on breach |
| [Edit Query Table](../domains/data-modeling-and-schema/query-tables/edit-query-table.md) | `EDIT_QT` (2038) | 20 requests per user per minute, 10-minute lockout on breach |
| [Refetch Data](../domains/data-operations/data-sync-and-connectivity/refetch-datasource.md) | `REFETCH_DATA` (3026) | 5 requests per minute, 5-minute lockout on breach |
| [Sync Data](../domains/data-operations/data-sync-and-connectivity/sync-datasource.md) | `SYNC_DATA` (3025) | 5 requests per minute, 5-minute lockout on breach |
| [Create Dashboard](../domains/reports-and-dashboards/dashboards/create-dashboard.md) | `CREATE_DASHBOARD` (2060) | 10 requests per user per minute, 10-minute lockout on breach |
| [Read Dashboard Metadata](../domains/reports-and-dashboards/dashboards/get-dashboard-metadata.md) | `GET_DASHBOARD_METADATA` (2061) | 20 requests per user per minute, 10-minute lockout on breach |
| [Update Dashboard](../domains/reports-and-dashboards/dashboards/update-dashboard.md) | `UPDATE_DASHBOARD` (2062) | 10 requests per user per minute, 10-minute lockout on breach |

Documented limits that are enforced outside the URL configuration, and so are not in the table above:

- Create Query Table and Edit Query Table are additionally capped at 15 requests per minute service-wide.
- Copy Workspace allows one copy operation per organization at a time.
- Asynchronous export allows at most 5 simultaneous export jobs per organization.
- Refetch Data allows one refetch per table at a time.

See [Rate limits, throttling and quotas](rate-limits-and-quotas.md) for the concurrency guards and plan quotas that sit alongside these.

# Zero-cost Endpoints

12 endpoints are configured at `0` units in the gateway. They still count against the category frequency limit.

Read the table with one caveat: for the six import/export **initiation** endpoints (`INITIATE_EXPORT`, `INITIATE_IMPORT`, `BATCH_IMPORT_FILE_UPLOAD`) the `0` is only the cost of the request that starts the work - the data itself is charged against a second action once it has been produced, as described in [Variable-cost operations](#variable-cost-operations). The genuinely free endpoints are the four job-status and download calls (`EXPORT_JOB_STATUS`, `DOWNLOAD_FILE`, `IMPORT_JOB_STATUS`).

| Endpoint | Action (api-id) | Category |
|---|---|---|
| [Create Export Job using SQL Query (Asynchronous)](../domains/data-operations/async-data-export/create-export-job-sql-query.md) | `INITIATE_EXPORT` (7001) | BULK |
| [Create Export Job using View ID (Asynchronous)](../domains/data-operations/async-data-export/create-export-job-view-id.md) | `INITIATE_EXPORT` (7001) | BULK |
| [Download Exported Data](../domains/data-operations/async-data-export/download-exported-data.md) | `DOWNLOAD_FILE` (9002) | METADATA |
| [Get Export Job Details](../domains/data-operations/async-data-export/get-export-job-details.md) | `EXPORT_JOB_STATUS` (9001) | METADATA |
| [Batch Import Data into Existing Table](../domains/data-operations/async-data-import/batch-import-existing-table.md) | `BATCH_IMPORT_FILE_UPLOAD` (8005) | BULK |
| [Batch Import Data into New Table](../domains/data-operations/async-data-import/batch-import-new-table.md) | `BATCH_IMPORT_FILE_UPLOAD` (8005) | BULK |
| [Create Import Job for an Existing Table (Asynchronous)](../domains/data-operations/async-data-import/create-import-job-existing-table.md) | `INITIATE_IMPORT` (8001) | BULK |
| [Create Import Job for a New Table (Asynchronous)](../domains/data-operations/async-data-import/create-import-job-new-table.md) | `INITIATE_IMPORT` (8001) | BULK |
| [Get Import Job Details](../domains/data-operations/async-data-import/get-import-job-details.md) | `IMPORT_JOB_STATUS` (9003) | METADATA |
| [Export Data from a View](../domains/data-operations/sync-data-export/export-data-view.md) | `INITIATE_EXPORT` (7001) | BULK |
| [Import Data into an Existing Table (Synchronous)](../domains/data-operations/sync-data-import/import-data-existing-table.md) | `INITIATE_IMPORT` (8001) | BULK |
| [Import Data into a New Table (Synchronous)](../domains/data-operations/sync-data-import/import-data-new-table.md) | `INITIATE_IMPORT` (8001) | BULK |

# Reducing Unit Consumption

- **Load data in bulk.** A 100000-row load costs ~1000 units through [Import Data](../domains/data-operations/sync-data-import/import-data-existing-table.md) and 10000 units through [Add Row](../domains/data-operations/row-operations/add-row.md).
- **Pick the cheapest export format you can use.** CSV/JSON costs 3 units per 1000 rows; the same data as HTML costs a flat 15 units per request and as a chart image 10 units per request. For large row counts the flat-rate formats are cheaper; for small ones they are not.
- **Poll freely, but not pointlessly.** Job status and download endpoints cost `0` units, but they are charged against the `BULK` frequency ceiling of 40 requests/minute - a tight polling loop will hit the frequency limit long before it costs anything.
- **Prefer the listing endpoints over per-object reads.** [Get Views](../domains/views-management/view-operations/get-views.md) at `0.1` units returns in one call what a loop of per-view metadata reads would cost many times over.
- **Watch `apiUnits` in [Get Resource Details](../domains/organization-management/org-info-and-settings/get-resource-details.md).** It costs `0.1` units itself and reports allocated, used and remaining units for the organization.

# Notes on This Reference

- Unit costs, the row basis, unit categories and the per-category frequency limits come from the API gateway configuration; the method/path-to-`api-id` binding and the endpoint throttles come from the URL security configuration.
- Internal-service routes and service-specific unit exemptions exist in those configurations but are deliberately out of scope here - this reference covers only the public, documented v2 endpoints.
- The frequency limits listed are the base configuration. An organization's effective ceiling is the base value scaled by a plan multiplier, so higher plans get proportionally more headroom in every category.
- [Get Org Recent Items](../domains/organization-management/org-level-listings/get-org-recent-items.md) has no URL binding of its own in the security configuration; its cost is taken from `GET_RECENT_VIEWS` (3007), the recent-items action in the gateway.

# Related

- [Rate limits, throttling and quotas](rate-limits-and-quotas.md) - concurrency guards, plan quotas and the wider limit picture.
- [Endpoint catalog](../endpoint-catalog.md) - every endpoint with its unit cost and category in one table.
- [`/references/endpoint-catalog.json`](../references/endpoint-catalog.json) - machine-readable unit costs under `api_units`.
- [Get Resource Details](../domains/organization-management/org-info-and-settings/get-resource-details.md) - live unit allocation, usage and remainder.
- [Asynchronous jobs](asynchronous-jobs.md), [Error code catalog](error-codes.md).
