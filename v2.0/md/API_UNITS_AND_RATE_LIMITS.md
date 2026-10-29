# Zoho Analytics V2 REST API — API Units and Rate Limits

Every call to a Zoho Analytics V2 REST API deducts **API units** from the organisation's plan allowance, and is counted against a **per-minute request ceiling**. Both are driven by the same thing: the internal gateway action (`api-id`) that the request's HTTP method and URL resolve to.

This document is the single place where the cost of every documented V2 API is listed. The same figures appear on each API's attribute table and in the "API Units and Frequency Limits" appendix of each group document.

## What is an "API unit"?

An API unit is the billing quantum for API usage. Each organisation's plan allocates a number of units; each call deducts some. Costs are fractional — the cheapest reads cost `0.1` units, the most expensive single operation (Copy Workspace) costs `25`.

| Concept | What it is | When it is enforced |
|---------|------------|---------------------|
| **Unit cost** | How many units one call deducts. Fixed per API for most operations, proportional to rows processed for bulk and copy operations. | After the call completes — the row count is only known then. |
| **Unit category** | `DML`, `BULK` or `METADATA`. Every API belongs to exactly one. | — |
| **Frequency limit** | Requests per minute an organisation may make within one unit category. | Before the call runs; the request is rejected with an API-frequency error. |
| **API-specific throttle** | An extra per-user threshold with a lockout period, configured on specific expensive or write-heavy APIs. | Before the call runs; the caller is locked out of that API for the lock period. |

The live allocation, usage and remainder are returned by the **Get Resource Details** API (`GET /restapi/v2/resources`) under `resourceName: "apiUnits"`.

## How the cost is computed

```
units charged = (rows processed / rows basis) * configured units      # row-based APIs
units charged = configured units                                      # everything else
```

- Row-based costs are **not** rounded up to a whole block. Exporting 250 rows at 3 units per 1000 rows costs `0.75` units; exporting 2500 rows costs `7.5`.
- Units are charged on the rows **actually processed**. An import that aborts half-way is still charged for the rows it wrote.
- APIs that only *start* work — create export job, create import job, batch file upload — cost `0`. The data itself is charged against a second gateway action once produced. See [Variable costs](#variable-costs).

Two consequences worth designing around:

- **Row APIs are charged per call, not per row.** Add Row costs `0.1` units for the one row it inserts, so loading 100,000 rows that way costs 10,000 units — against roughly 1,000 units for the same data through Import Data. Use the import APIs for bulk loads.
- **Polling is free but not unlimited.** Job status and download APIs cost `0` units, but they still consume the frequency budget of their category, so a tight polling loop hits the frequency limit rather than the unit allowance.

## Frequency limits

Each API belongs to one unit category, and the category sets the per-minute request ceiling that the whole organisation shares across every API in it.

| Unit category | Base frequency limit | What it covers |
|---------------|----------------------|----------------|
| `DML` | **100 requests/minute** | Row-level writes: Add Row, Update Row, Delete Row. |
| `BULK` | **40 requests/minute** | Data import and export, synchronous and asynchronous, including job creation, status polling and downloads. |
| `METADATA` | **60 requests/minute** | Everything else — workspace, view, column, formula, user, sharing, publishing, schedule, alert and AutoML operations. |

The ceiling is scaled by a plan-specific multiplier, so a higher plan raises all three proportionally; the figures above are the base configuration. The frequency limit and the unit allowance are independent — a request can be rejected for frequency while plenty of units remain, and vice versa.

## API units by group

One row per documented API. `Gateway Action` is the internal action name and its `api-id`.

### 01 · Organization Management

**[ORG_INFO_AND_SETTINGS.md](01%20%C2%B7%20Organization%20Management/ORG_INFO_AND_SETTINGS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Resource Details](01%20%C2%B7%20Organization%20Management/ORG_INFO_AND_SETTINGS.md#1-get-resource-details) | GET | `GET_RESOURCE_DETAILS` (6008) | METADATA | 0.1 | per request |
| 2 | [Get Subscription Details](01%20%C2%B7%20Organization%20Management/ORG_INFO_AND_SETTINGS.md#2-get-subscription-details) | GET | `GET_SUBSCRIPTION_DETAILS` (6006) | METADATA | 0.1 | per request |
| 3 | [Get Meta Details From Name](01%20%C2%B7%20Organization%20Management/ORG_INFO_AND_SETTINGS.md#3-get-meta-details-from-name) | GET | `GET_META_DETAILS` (3021) | METADATA | 0.1 | per request |

**[ORG_LEVEL_LISTINGS.md](01%20%C2%B7%20Organization%20Management/ORG_LEVEL_LISTINGS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Org Workspaces](01%20%C2%B7%20Organization%20Management/ORG_LEVEL_LISTINGS.md#1-get-org-workspaces) | GET | `GET_WORKSPACES` (3043) | METADATA | 0.1 | per request |
| 2 | [Get Org Dashboards](01%20%C2%B7%20Organization%20Management/ORG_LEVEL_LISTINGS.md#2-get-org-dashboards) | GET | `GET_ORG_DASHBOARDS` (3044) | METADATA | 0.1 | per request |
| 3 | [Get Org Recent Items](01%20%C2%B7%20Organization%20Management/ORG_LEVEL_LISTINGS.md#3-get-org-recent-items) | GET | `GET_RECENT_VIEWS` (3007) | METADATA | 0.1 | per request |

**[SECURITY_CONTROLS.md](01%20%C2%B7%20Organization%20Management/SECURITY_CONTROLS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Org Access Restrictions](01%20%C2%B7%20Organization%20Management/SECURITY_CONTROLS.md#1-get-org-access-restrictions) | GET | `GET_ORG_ACCESS_RESTRICTIONS` (3067) | METADATA | 1 | per request |
| 2 | [Update Org Access Restrictions](01%20%C2%B7%20Organization%20Management/SECURITY_CONTROLS.md#2-update-org-access-restrictions) | PUT | `UPDATE_ORG_ACCESS_RESTRICTIONS` (3068) | METADATA | 1 | per request |
| 3 | [Get Workspace Access Restrictions](01%20%C2%B7%20Organization%20Management/SECURITY_CONTROLS.md#3-get-workspace-access-restrictions) | GET | `GET_WORKSPACE_ACCESS_RESTRICTIONS` (3069) | METADATA | 1 | per request |
| 4 | [Update Workspace Access Restrictions](01%20%C2%B7%20Organization%20Management/SECURITY_CONTROLS.md#4-update-workspace-access-restrictions) | PUT | `UPDATE_WORKSPACE_ACCESS_RESTRICTIONS` (3070) | METADATA | 1 | per request |

### 02 · User & Groups

**[CUSTOM_ROLES.md](02%20%C2%B7%20User%20%26%20Groups/CUSTOM_ROLES.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Custom Roles](02%20%C2%B7%20User%20%26%20Groups/CUSTOM_ROLES.md#1-get-custom-roles) | GET | `GET_ROLES` (6014) | METADATA | 1 | per request |
| 2 | [Create Custom Role](02%20%C2%B7%20User%20%26%20Groups/CUSTOM_ROLES.md#2-create-custom-role) | POST | `CREATE_ROLE` (6015) | METADATA | 1 | per request |
| 3 | [Update Custom Role](02%20%C2%B7%20User%20%26%20Groups/CUSTOM_ROLES.md#3-update-custom-role) | PUT | `UPDATE_ROLE` (6016) | METADATA | 1 | per request |
| 4 | [Delete Custom Role](02%20%C2%B7%20User%20%26%20Groups/CUSTOM_ROLES.md#4-delete-custom-role) | DELETE | `DELETE_ROLE` (6017) | METADATA | 1 | per request |

**[ORG_USERS.md](02%20%C2%B7%20User%20%26%20Groups/ORG_USERS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Users](02%20%C2%B7%20User%20%26%20Groups/ORG_USERS.md#1-get-users) | GET | `GET_ORG_USERS` (6001) | METADATA | 1 | per request |
| 2 | [Add Users](02%20%C2%B7%20User%20%26%20Groups/ORG_USERS.md#2-add-users) | POST | `ADD_ORG_USERS` (6002) | METADATA | 0.1 | per request |
| 3 | [Remove Users](02%20%C2%B7%20User%20%26%20Groups/ORG_USERS.md#3-remove-users) | DELETE | `REMOVE_ORG_USERS` (6003) | METADATA | 0.1 | per request |
| 4 | [Activate Users](02%20%C2%B7%20User%20%26%20Groups/ORG_USERS.md#4-activate-users) | PUT | `ACTIVATE_ORG_USERS` (6004) | METADATA | 0.1 | per request |
| 5 | [Deactivate Users](02%20%C2%B7%20User%20%26%20Groups/ORG_USERS.md#5-deactivate-users) | PUT | `DEACTIVATE_ORG_USERS` (6005) | METADATA | 0.1 | per request |
| 6 | [Change User Role](02%20%C2%B7%20User%20%26%20Groups/ORG_USERS.md#6-change-user-role) | PUT | `CHANGE_USER_ROLE` (6007) | METADATA | 0.1 | per request |
| 7 | [Get Org Admins](02%20%C2%B7%20User%20%26%20Groups/ORG_USERS.md#7-get-org-admins) | GET | `GET_ORG_ADMINS` (4001) | METADATA | 0.1 | per request |

**[WORKSPACE_GROUPS.md](02%20%C2%B7%20User%20%26%20Groups/WORKSPACE_GROUPS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Group List](02%20%C2%B7%20User%20%26%20Groups/WORKSPACE_GROUPS.md#1-get-group-list) | GET | `GET_GROUPS` (4012) | METADATA | 0.1 | per request |
| 2 | [Create Group](02%20%C2%B7%20User%20%26%20Groups/WORKSPACE_GROUPS.md#2-create-group) | POST | `CREATE_GROUP` (4013) | METADATA | 1 | per request |
| 3 | [Rename Group](02%20%C2%B7%20User%20%26%20Groups/WORKSPACE_GROUPS.md#3-rename-group) | PUT | `RENAME_GROUP` (4014) | METADATA | 0.1 | per request |
| 4 | [Add Group Members](02%20%C2%B7%20User%20%26%20Groups/WORKSPACE_GROUPS.md#4-add-group-members) | POST | `ADD_GROUP_MEMBERS` (4015) | METADATA | 0.1 | per request |
| 5 | [Remove Group Members](02%20%C2%B7%20User%20%26%20Groups/WORKSPACE_GROUPS.md#5-remove-group-members) | DELETE | `REMOVE_GROUP_MEMBERS` (4016) | METADATA | 0.1 | per request |
| 6 | [Delete Group](02%20%C2%B7%20User%20%26%20Groups/WORKSPACE_GROUPS.md#6-delete-group) | DELETE | `DELETE_GROUP` (4017) | METADATA | 1 | per request |
| 7 | [Get Group Details](02%20%C2%B7%20User%20%26%20Groups/WORKSPACE_GROUPS.md#7-get-group-details) | GET | `GET_GROUP_DETAILS` (4018) | METADATA | 0.1 | per request |

**[WORKSPACE_USERS.md](02%20%C2%B7%20User%20%26%20Groups/WORKSPACE_USERS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Workspace Users](02%20%C2%B7%20User%20%26%20Groups/WORKSPACE_USERS.md#1-get-workspace-users) | GET | `GET_WORKSPACE_USERS` (6009) | METADATA | 1 | per request |
| 2 | [Add Workspace Users](02%20%C2%B7%20User%20%26%20Groups/WORKSPACE_USERS.md#2-add-workspace-users) | POST | `ADD_WORKSPACE_USERS` (6010) | METADATA | 0.5 | per request |
| 3 | [Remove Workspace Users](02%20%C2%B7%20User%20%26%20Groups/WORKSPACE_USERS.md#3-remove-workspace-users) | DELETE | `REMOVE_WORKSPACE_USERS` (6011) | METADATA | 1 | per request |
| 4 | [Change Workspace Users Status](02%20%C2%B7%20User%20%26%20Groups/WORKSPACE_USERS.md#4-change-workspace-users-status) | PUT | `CHANGE_WORKSPACE_USERS_STATUS` (6012) | METADATA | 0.5 | per request |
| 5 | [Change Workspace Users Role](02%20%C2%B7%20User%20%26%20Groups/WORKSPACE_USERS.md#5-change-workspace-users-role) | PUT | `CHANGE_WORKSPACE_USERS_ROLE` (6013) | METADATA | 1 | per request |
| 6 | [Get Workspace Admins](02%20%C2%B7%20User%20%26%20Groups/WORKSPACE_USERS.md#6-get-workspace-admins) | GET | `GET_WORKSPACE_ADMINS` (4004) | METADATA | 0.1 | per request |
| 7 | [Add Workspace Admins](02%20%C2%B7%20User%20%26%20Groups/WORKSPACE_USERS.md#7-add-workspace-admins) | POST | `ADD_WORKSPACE_ADMINS` (4005) | METADATA | 5 | per request |
| 8 | [Remove Workspace Admins](02%20%C2%B7%20User%20%26%20Groups/WORKSPACE_USERS.md#8-remove-workspace-admins) | DELETE | `REMOVE_WORKSPACE_ADMINS` (4006) | METADATA | 5 | per request |

### 03 · Workspace Management

**[DOMAIN_AND_WHITE_LABEL.md](03%20%C2%B7%20Workspace%20Management/DOMAIN_AND_WHITE_LABEL.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Enable Workspace for Domain Access](03%20%C2%B7%20Workspace%20Management/DOMAIN_AND_WHITE_LABEL.md#1-enable-workspace-for-domain-access) | POST | `ENABLE_DOMAIN_WORKSPACE` (3022) | METADATA | 0.1 | per request |
| 2 | [Disable Workspace for Domain Access](03%20%C2%B7%20Workspace%20Management/DOMAIN_AND_WHITE_LABEL.md#2-disable-workspace-for-domain-access) | DELETE | `DISABLE_DOMAIN_WORKSPACE` (3023) | METADATA | 0.1 | per request |

**[LINKED_WORKSPACES.md](03%20%C2%B7%20Workspace%20Management/LINKED_WORKSPACES.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Linked Workspaces For Organization](03%20%C2%B7%20Workspace%20Management/LINKED_WORKSPACES.md#1-get-linked-workspaces-for-organization) | GET | `GET_LINKED_WORKSPACES_FOR_ORGANIZATION` (3086) | METADATA | 1 | per request |
| 2 | [Get Linked Workspaces For Master Workspace](03%20%C2%B7%20Workspace%20Management/LINKED_WORKSPACES.md#2-get-linked-workspaces-for-master-workspace) | GET | `GET_LINKED_WORKSPACES_FOR_MASTER_WORKSPACE` (3087) | METADATA | 1 | per request |
| 3 | [Get Linkable Workspaces](03%20%C2%B7%20Workspace%20Management/LINKED_WORKSPACES.md#3-get-linkable-workspaces) | GET | `GET_LINKABLE_WORKSPACES` (3088) | METADATA | 1 | per request |
| 4 | [Get Workspace Linking Compatibility](03%20%C2%B7%20Workspace%20Management/LINKED_WORKSPACES.md#4-get-workspace-linking-compatibility) | GET | `GET_WORKSPACE_LINKING_COMPATIBILITY` (3089) | METADATA | 1 | per request |
| 5 | [Link Workspaces](03%20%C2%B7%20Workspace%20Management/LINKED_WORKSPACES.md#5-link-workspaces) | POST | `LINK_WORKSPACES` (2080) | METADATA | 3 | per request |
| 6 | [Sync Linked Workspaces](03%20%C2%B7%20Workspace%20Management/LINKED_WORKSPACES.md#6-sync-linked-workspaces) | POST | `SYNC_LINKED_WORKSPACES` (2082) | METADATA | 3 | per request |
| 7 | [Get Linked Workspace Sync Details](03%20%C2%B7%20Workspace%20Management/LINKED_WORKSPACES.md#7-get-linked-workspace-sync-details) | GET | `GET_LINKED_WORKSPACE_SYNC_DETAILS` (3090) | METADATA | 1 | per request |
| 8 | [Unlink Workspaces](03%20%C2%B7%20Workspace%20Management/LINKED_WORKSPACES.md#8-unlink-workspaces) | DELETE | `UNLINK_WORKSPACES` (2081) | METADATA | 3 | per request |

**[WORKSPACE_BACKUP_AND_RESTORE.md](03%20%C2%B7%20Workspace%20Management/WORKSPACE_BACKUP_AND_RESTORE.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Workspace Backups](03%20%C2%B7%20Workspace%20Management/WORKSPACE_BACKUP_AND_RESTORE.md#1-get-workspace-backups) | GET | `GET_WORKSPACE_BACKUPS` (3082) | METADATA | 1 | per request |
| 2 | [Backup Workspace Now](03%20%C2%B7%20Workspace%20Management/WORKSPACE_BACKUP_AND_RESTORE.md#2-backup-workspace-now) | POST | `BACKUP_WORKSPACE_NOW` (3083) | METADATA | 5 | per request |
| 3 | [Download Workspace Backup](03%20%C2%B7%20Workspace%20Management/WORKSPACE_BACKUP_AND_RESTORE.md#3-download-workspace-backup) | GET | `DOWNLOAD_WORKSPACE_BACKUP` (3084) | METADATA | 1 | per request |
| 4 | [Restore Workspace from Backup](03%20%C2%B7%20Workspace%20Management/WORKSPACE_BACKUP_AND_RESTORE.md#4-restore-workspace-from-backup) | POST | `RESTORE_WORKSPACE_BACKUP` (3085) | METADATA | 10 | per request |
| 5 | [Get Workspace Backup Status](03%20%C2%B7%20Workspace%20Management/WORKSPACE_BACKUP_AND_RESTORE.md#5-get-workspace-backup-status) | GET | `GET_WORKSPACE_BACKUP_STATUS` (3096) | METADATA | 0.5 | per request |
| 6 | [Get Workspace Restore Status](03%20%C2%B7%20Workspace%20Management/WORKSPACE_BACKUP_AND_RESTORE.md#6-get-workspace-restore-status) | GET | `GET_WORKSPACE_RESTORE_STATUS` (3097) | METADATA | 0.5 | per request |

**[WORKSPACE_FOLDERS.md](03%20%C2%B7%20Workspace%20Management/WORKSPACE_FOLDERS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Folder List](03%20%C2%B7%20Workspace%20Management/WORKSPACE_FOLDERS.md#1-get-folder-list) | GET | `GET_FOLDERS` (3006) | METADATA | 0.1 | per request |
| 2 | [Create Folder](03%20%C2%B7%20Workspace%20Management/WORKSPACE_FOLDERS.md#2-create-folder) | POST | `CREATE_FOLDER` (2010) | METADATA | 1 | per request |
| 3 | [Rename Folder](03%20%C2%B7%20Workspace%20Management/WORKSPACE_FOLDERS.md#3-rename-folder) | PUT | `RENAME_FOLDER` (2011) | METADATA | 1 | per request |
| 4 | [Delete Folder](03%20%C2%B7%20Workspace%20Management/WORKSPACE_FOLDERS.md#4-delete-folder) | DELETE | `DELETE_FOLDER` (2012) | METADATA | 1 | per request |
| 5 | [Change Folder Hierarchy](03%20%C2%B7%20Workspace%20Management/WORKSPACE_FOLDERS.md#5-change-folder-hierarchy) | PUT | `CHANGE_FOLDER_HIERARCHY` (2047) | METADATA | 1 | per request |
| 6 | [Change Folder Position](03%20%C2%B7%20Workspace%20Management/WORKSPACE_FOLDERS.md#6-change-folder-position) | PUT | `CHANGE_FOLDER_POSITION` (2048) | METADATA | 1 | per request |
| 7 | [Move Views To Folder](03%20%C2%B7%20Workspace%20Management/WORKSPACE_FOLDERS.md#7-move-views-to-folder) | PUT | `MOVE_VIEWS_TO_FOLDER` (2049) | METADATA | 1 | per request |
| 8 | [Make Default Folder](03%20%C2%B7%20Workspace%20Management/WORKSPACE_FOLDERS.md#8-make-default-folder) | PUT | `MAKE_DEFAULT_FOLDER` (2030) | METADATA | 1 | per request |

**[WORKSPACE_OPERATIONS.md](03%20%C2%B7%20Workspace%20Management/WORKSPACE_OPERATIONS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Create Workspace](03%20%C2%B7%20Workspace%20Management/WORKSPACE_OPERATIONS.md#1-create-workspace) | POST | `CREATE_WORKSPACE` (2001) | METADATA | 1 | per request |
| 2 | [Copy Workspace](03%20%C2%B7%20Workspace%20Management/WORKSPACE_OPERATIONS.md#2-copy-workspace) | POST | `COPY_WORKSPACE_WO_DATA` (2002) | METADATA | variable | see [Variable costs](#variable-costs) |
| 3 | [Rename Workspace](03%20%C2%B7%20Workspace%20Management/WORKSPACE_OPERATIONS.md#3-rename-workspace) | PUT | `RENAME_WORKSPACE` (2004) | METADATA | 1 | per request |
| 4 | [Delete Workspace](03%20%C2%B7%20Workspace%20Management/WORKSPACE_OPERATIONS.md#4-delete-workspace) | DELETE | `DELETE_WORKSPACE` (2005) | METADATA | 1 | per request |
| 5 | [Export as Template](03%20%C2%B7%20Workspace%20Management/WORKSPACE_OPERATIONS.md#5-export-as-template) | GET | `EXPORT_AS_TEMPLATE` (3032) | METADATA | 5 | per request |
| 6 | [Get Workspace Secret Key](03%20%C2%B7%20Workspace%20Management/WORKSPACE_OPERATIONS.md#6-get-workspace-secret-key) | GET | `GET_WORKSPACE_SECRETKEY` (3011) | METADATA | 0.5 | per request |
| 7 | [Get Workspace Info](03%20%C2%B7%20Workspace%20Management/WORKSPACE_OPERATIONS.md#7-get-workspace-info) | GET | `GET_WORKSPACE_DETAILS` (3012) | METADATA | 0.1 | per request |

**[WORKSPACE_PREFERENCES.md](03%20%C2%B7%20Workspace%20Management/WORKSPACE_PREFERENCES.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Add Default Workspace](03%20%C2%B7%20Workspace%20Management/WORKSPACE_PREFERENCES.md#1-add-default-workspace) | POST | `ADD_DEFAULT_WORKSPACE` (3019) | METADATA | 0.1 | per request |
| 2 | [Remove Default Workspace](03%20%C2%B7%20Workspace%20Management/WORKSPACE_PREFERENCES.md#2-remove-default-workspace) | DELETE | `REMOVE_DEFAULT_WORKSPACE` (3020) | METADATA | 0.1 | per request |
| 3 | [Add Favourite Workspace](03%20%C2%B7%20Workspace%20Management/WORKSPACE_PREFERENCES.md#3-add-favourite-workspace) | POST | `ADD_FAVOURITE_WORKSPACE` (3015) | METADATA | 0.1 | per request |
| 4 | [Remove Favourite Workspace](03%20%C2%B7%20Workspace%20Management/WORKSPACE_PREFERENCES.md#4-remove-favourite-workspace) | DELETE | `REMOVE_FAVOURITE_WORKSPACE` (3016) | METADATA | 0.1 | per request |

### 04 · Data Modeling & Schema

**[AGGREGATE_FORMULAS.md](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/AGGREGATE_FORMULAS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Aggregate Formula](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/AGGREGATE_FORMULAS.md#1-get-aggregate-formula) | GET | `GET AGGREGATE FORMULA` (3037) | METADATA | 0.1 | per request |
| 2 | [Add Aggregate Formula](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/AGGREGATE_FORMULAS.md#2-add-aggregate-formula) | POST | `ADD_AGG_FORMULA` (2044) | METADATA | 5 | per request |
| 3 | [Edit Aggregate Formula](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/AGGREGATE_FORMULAS.md#3-edit-aggregate-formula) | PUT | `EDIT_AGG_FORMULA` (2045) | METADATA | 5 | per request |
| 4 | [Delete Aggregate Formula](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/AGGREGATE_FORMULAS.md#4-delete-aggregate-formula) | DELETE | `DELETE AGG FORMULA` (2046) | METADATA | 1 | per request |
| 5 | [Get Unified Metrics in Workspace](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/AGGREGATE_FORMULAS.md#5-get-unified-metrics-in-workspace) | GET | `GET_AGGREGATE_FORMULAS_IN_WORKSPACE` (3039) | METADATA | 1 | per request |
| 6 | [Get Aggregate Formula Dependents](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/AGGREGATE_FORMULAS.md#6-get-aggregate-formula-dependents) | GET | `GET_AGGREGATE_FORMULA_DEPENDENTS` (3040) | METADATA | 1 | per request |
| 7 | [Get Aggregate Formula Value](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/AGGREGATE_FORMULAS.md#7-get-aggregate-formula-value) | GET | `GET_AGGREGATE_FORMULA_VALUE` (3041) | METADATA | 1 | per request |

**[COLUMNS.md](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/COLUMNS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Add Column](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/COLUMNS.md#1-add-column) | POST | `ADD_COLUMN` (2013) | METADATA | 15 | per request |
| 2 | [Rename Column](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/COLUMNS.md#2-rename-column) | PUT | `RENAME_COLUMN` (2014) | METADATA | 5 | per request |
| 3 | [Delete Column](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/COLUMNS.md#3-delete-column) | DELETE | `DELETE_COLUMN` (2015) | METADATA | 10 | per request |
| 4 | [Hide Columns](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/COLUMNS.md#4-hide-columns) | PUT | `HIDE_COLUMNS` (2018) | METADATA | 1 | per request |
| 5 | [Show Columns](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/COLUMNS.md#5-show-columns) | PUT | `SHOW_COLUMNS` (2019) | METADATA | 1 | per request |
| 6 | [Get Column Dependents](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/COLUMNS.md#6-get-column-dependents) | GET | `GET_COLUMN_DEPENDENTS` (3030) | METADATA | 0.1 | per request |
| 7 | [Sort Data by Columns](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/COLUMNS.md#7-sort-data-by-columns) | PUT | `SORT_DATA_BY_COLUMNS` (2064) | METADATA | 1 | per request |
| 8 | [Reorder Columns](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/COLUMNS.md#8-reorder-columns) | PUT | `REORDER_COLUMNS` (2063) | METADATA | 1 | per request |

**[FORMULA_COLUMNS.md](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/FORMULA_COLUMNS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Custom Formulas](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/FORMULA_COLUMNS.md#1-get-custom-formulas) | GET | `GET_FORMULA_COLUMN` (3036) | METADATA | 0.1 | per request |
| 2 | [Add Custom Formula](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/FORMULA_COLUMNS.md#2-add-custom-formula) | POST | `ADD_FORMULA_COLUMN` (2041) | METADATA | 15 | per request |
| 3 | [Edit Custom Formula](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/FORMULA_COLUMNS.md#3-edit-custom-formula) | PUT | `EDIT_FORMULA_COLUMN` (2042) | METADATA | 15 | per request |
| 4 | [Delete Custom Formula](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/FORMULA_COLUMNS.md#4-delete-custom-formula) | DELETE | `DELETE_FORMULA_COLUMN` (2043) | METADATA | 2 | per request |
| 5 | [Copy Custom Formulas](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/FORMULA_COLUMNS.md#5-copy-custom-formulas) | POST | `COPY_FORMULAS` (2021) | METADATA | 1 | per request |

**[LOOKUPS_AND_RELATIONSHIPS.md](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/LOOKUPS_AND_RELATIONSHIPS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Add Lookup](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/LOOKUPS_AND_RELATIONSHIPS.md#1-add-lookup) | POST | `ADD_LOOKUP` (2016) | METADATA | 1 | per request |
| 2 | [Remove Lookup](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/LOOKUPS_AND_RELATIONSHIPS.md#2-remove-lookup) | DELETE | `REMOVE_LOOKUP` (2017) | METADATA | 2 | per request |

**[QUERY_TABLES.md](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/QUERY_TABLES.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Query Tables](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/QUERY_TABLES.md#1-get-query-tables) | GET | `GET_QUERY_TABLES` (3064) | METADATA | 0.1 | per request |
| 2 | [Create Query Table](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/QUERY_TABLES.md#2-create-query-table) | POST | `CREATE_QT` (2037) | METADATA | 15 | per request |
| 3 | [Edit Query Table](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/QUERY_TABLES.md#3-edit-query-table) | PUT | `EDIT_QT` (2038) | METADATA | 15 | per request |
| 4 | [Get Query Table Details](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/QUERY_TABLES.md#4-get-query-table-details) | GET | `GET_QUERYTABLE_DETAILS` (3047) | METADATA | 1 | per request |

**[TABLE_AND_SCHEMA.md](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/TABLE_AND_SCHEMA.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Create Table](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/TABLE_AND_SCHEMA.md#1-create-table) | POST | `CREATE_TABLE` (2006) | METADATA | 1 | per request |
| 2 | [Get Table Metadata](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/TABLE_AND_SCHEMA.md#2-get-table-metadata) | GET | `GET_TABLE_METADATA` (3053) | METADATA | 1 | per request |

**[WORKSPACE_VARIABLES.md](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/WORKSPACE_VARIABLES.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Create Variable](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/WORKSPACE_VARIABLES.md#1-create-variable) | POST | `CREATE_VARIABLE` (2025) | METADATA | 1 | per request |
| 2 | [Edit Variable](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/WORKSPACE_VARIABLES.md#2-edit-variable) | PUT | `UPDATE_VARIABLE` (2026) | METADATA | 1 | per request |
| 3 | [Delete Variable](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/WORKSPACE_VARIABLES.md#3-delete-variable) | DELETE | `DELETE_VARIABLE` (2027) | METADATA | 1 | per request |
| 4 | [Get Variables](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/WORKSPACE_VARIABLES.md#4-get-variables) | GET | `GET_VARIABLES` (2028) | METADATA | 1 | per request |
| 5 | [Get Variable Details](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/WORKSPACE_VARIABLES.md#5-get-variable-details) | GET | `GET_VARIABLE_DETAILS` (2029) | METADATA | 1 | per request |

### 05 · Data Operations

**[ASYNC_DATA_EXPORT.md](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_EXPORT.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Create Export Job using SQL Query (Asynchronous)](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_EXPORT.md#1-create-export-job-using-sql-query-asynchronous) | GET | `INITIATE_EXPORT` (7001) | BULK | variable | see [Variable costs](#variable-costs) |
| 2 | [Create Export Job using View ID (Asynchronous)](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_EXPORT.md#2-create-export-job-using-view-id-asynchronous) | GET | `INITIATE_EXPORT` (7001) | BULK | variable | see [Variable costs](#variable-costs) |
| 3 | [Get Export Job Details](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_EXPORT.md#3-get-export-job-details) | GET | `EXPORT_JOB_STATUS` (9001) | METADATA | 0 | not charged |
| 4 | [Download Exported Data](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_EXPORT.md#4-download-exported-data) | GET | `DOWNLOAD_FILE` (9002) | METADATA | 0 | not charged |

**[ASYNC_DATA_IMPORT.md](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_IMPORT.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Create Import Job for a New Table (Asynchronous)](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_IMPORT.md#1-create-import-job-for-a-new-table-asynchronous) | POST | `INITIATE_IMPORT` (8001) | BULK | variable | see [Variable costs](#variable-costs) |
| 2 | [Create Import Job for an Existing Table (Asynchronous)](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_IMPORT.md#2-create-import-job-for-an-existing-table-asynchronous) | POST | `INITIATE_IMPORT` (8001) | BULK | variable | see [Variable costs](#variable-costs) |
| 3 | [Batch Import Data into New Table](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_IMPORT.md#3-batch-import-data-into-new-table) | POST | `BATCH_IMPORT_FILE_UPLOAD` (8005) | BULK | variable | see [Variable costs](#variable-costs) |
| 4 | [Batch Import Data into Existing Table](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_IMPORT.md#4-batch-import-data-into-existing-table) | POST | `BATCH_IMPORT_FILE_UPLOAD` (8005) | BULK | variable | see [Variable costs](#variable-costs) |
| 5 | [Get Import Job Details](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_IMPORT.md#5-get-import-job-details) | GET | `IMPORT_JOB_STATUS` (9003) | METADATA | 0 | not charged |

**[DATA_SYNC_AND_CONNECTIVITY.md](05%20%C2%B7%20Data%20Operations/DATA_SYNC_AND_CONNECTIVITY.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Sync Data](05%20%C2%B7%20Data%20Operations/DATA_SYNC_AND_CONNECTIVITY.md#1-sync-data) | POST | `SYNC_DATA` (3025) | METADATA | 5 | per request |
| 2 | [Refetch Data](05%20%C2%B7%20Data%20Operations/DATA_SYNC_AND_CONNECTIVITY.md#2-refetch-data) | POST | `REFETCH_DATA` (3026) | METADATA | 2 | per request |
| 3 | [Update Datasource Connection](05%20%C2%B7%20Data%20Operations/DATA_SYNC_AND_CONNECTIVITY.md#3-update-datasource-connection) | PUT | `UPDATE_DATASOURCE_CONNECTION` (3028) | METADATA | 1 | per request |
| 4 | [Get Datasources](05%20%C2%B7%20Data%20Operations/DATA_SYNC_AND_CONNECTIVITY.md#4-get-datasources) | GET | `GET_DATASOURCES` (3024) | METADATA | 1 | per request |
| 5 | [Get Last Import Details](05%20%C2%B7%20Data%20Operations/DATA_SYNC_AND_CONNECTIVITY.md#5-get-last-import-details) | GET | `GET_LAST_IMPORT_DETAILS` (3027) | METADATA | 0.1 | per request |

**[ROW_OPERATIONS.md](05%20%C2%B7%20Data%20Operations/ROW_OPERATIONS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Add Row](05%20%C2%B7%20Data%20Operations/ROW_OPERATIONS.md#1-add-row) | POST | `ADD_ROW` (1001) | DML | 0.1 | per request |
| 2 | [Update Row](05%20%C2%B7%20Data%20Operations/ROW_OPERATIONS.md#2-update-row) | PUT | `UPDATE_ROW` (1002) | DML | 0.3 | per request |
| 3 | [Delete Row](05%20%C2%B7%20Data%20Operations/ROW_OPERATIONS.md#3-delete-row) | DELETE | `DELETE_ROW` (1003) | DML | 0.1 | per request |

**[SYNC_DATA_EXPORT.md](05%20%C2%B7%20Data%20Operations/SYNC_DATA_EXPORT.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Export Data from a View](05%20%C2%B7%20Data%20Operations/SYNC_DATA_EXPORT.md#1-export-data-from-a-view) | GET | `INITIATE_EXPORT` (7001) | BULK | variable | see [Variable costs](#variable-costs) |

**[SYNC_DATA_IMPORT.md](05%20%C2%B7%20Data%20Operations/SYNC_DATA_IMPORT.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Import Data into a New Table (Synchronous)](05%20%C2%B7%20Data%20Operations/SYNC_DATA_IMPORT.md#1-import-data-into-a-new-table-synchronous) | POST | `INITIATE_IMPORT` (8001) | BULK | variable | see [Variable costs](#variable-costs) |
| 2 | [Import Data into an Existing Table (Synchronous)](05%20%C2%B7%20Data%20Operations/SYNC_DATA_IMPORT.md#2-import-data-into-an-existing-table-synchronous) | POST | `INITIATE_IMPORT` (8001) | BULK | variable | see [Variable costs](#variable-costs) |

### 06 · Views Management

**[AUTO_ANALYSIS.md](06%20%C2%B7%20Views%20Management/AUTO_ANALYSIS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Auto Analyse View](06%20%C2%B7%20Views%20Management/AUTO_ANALYSIS.md#1-auto-analyse-view) | POST | `AUTO_ANALYSIS_VIEW` (2023) | METADATA | 1 | per request |
| 2 | [Auto Analyse Column](06%20%C2%B7%20Views%20Management/AUTO_ANALYSIS.md#2-auto-analyse-column) | POST | `AUTO_ANALYSIS_COLUMN` (2024) | METADATA | 1 | per request |

**[TAGS.md](06%20%C2%B7%20Views%20Management/TAGS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Tags List](06%20%C2%B7%20Views%20Management/TAGS.md#1-get-tags-list) | GET | `GET_TAGS` (3071) | METADATA | 0.5 | per request |
| 2 | [Get Tagged Views](06%20%C2%B7%20Views%20Management/TAGS.md#2-get-tagged-views) | GET | `GET_TAGGED_VIEWS` (3072) | METADATA | 0.5 | per request |
| 3 | [Get View Tags](06%20%C2%B7%20Views%20Management/TAGS.md#3-get-view-tags) | GET | `GET_VIEW_TAGS` (3073) | METADATA | 0.5 | per request |
| 4 | [Create Tag](06%20%C2%B7%20Views%20Management/TAGS.md#4-create-tag) | POST | `CREATE_TAG` (2073) | METADATA | 0.5 | per request |
| 5 | [Update Tag](06%20%C2%B7%20Views%20Management/TAGS.md#5-update-tag) | PUT | `UPDATE_TAG` (2074) | METADATA | 0.5 | per request |
| 6 | [Delete Tag](06%20%C2%B7%20Views%20Management/TAGS.md#6-delete-tag) | DELETE | `DELETE_TAG` (2075) | METADATA | 0.5 | per request |
| 7 | [Add Tag To Multiple Views](06%20%C2%B7%20Views%20Management/TAGS.md#7-add-tag-to-multiple-views) | POST | `ADD_TAG_TO_VIEWS` (2076) | METADATA | 0.5 | per request |
| 8 | [Remove Tag From Multiple Views](06%20%C2%B7%20Views%20Management/TAGS.md#8-remove-tag-from-multiple-views) | DELETE | `REMOVE_TAG_FROM_VIEWS` (2077) | METADATA | 0.5 | per request |
| 9 | [Add Multiple Tags To View](06%20%C2%B7%20Views%20Management/TAGS.md#9-add-multiple-tags-to-view) | POST | `ADD_TAGS_TO_VIEW` (2078) | METADATA | 0.5 | per request |
| 10 | [Remove Multiple Tags From View](06%20%C2%B7%20Views%20Management/TAGS.md#10-remove-multiple-tags-from-view) | DELETE | `REMOVE_TAGS_FROM_VIEW` (2079) | METADATA | 0.5 | per request |

**[TRASH_MANAGEMENT.md](06%20%C2%B7%20Views%20Management/TRASH_MANAGEMENT.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Trash Views](06%20%C2%B7%20Views%20Management/TRASH_MANAGEMENT.md#1-get-trash-views) | GET | `GET_TRASH_VIEWS` (3035) | METADATA | 1 | per request |
| 2 | [Restore Trash View](06%20%C2%B7%20Views%20Management/TRASH_MANAGEMENT.md#2-restore-trash-view) | POST | `RESTORE_TRASH_VIEW` (2039) | METADATA | 3 | per request |
| 3 | [Delete Trash View](06%20%C2%B7%20Views%20Management/TRASH_MANAGEMENT.md#3-delete-trash-view) | DELETE | `DELETE_TRASH_VIEW` (2040) | METADATA | 3 | per request |

**[VIEW_OPERATIONS.md](06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Save As View](06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#1-save-as-view) | POST | `SAVEAS_VIEWS` (2007) | METADATA | 1 | per request |
| 2 | [Copy Views](06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#2-copy-views) | POST | `COPY_VIEWS` (2020) | METADATA | 1 | per request |
| 3 | [Create Similar Views](06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#3-create-similar-views) | POST | `CREATE_SIMILAR_VIEWS` (2022) | METADATA | 1 | per request |
| 4 | [Rename View](06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#4-rename-view) | PUT | `RENAME_VIEW` (2008) | METADATA | 1 | per request |
| 5 | [Delete View](06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#5-delete-view) | DELETE | `DELETE_VIEW` (2009) | METADATA | 2 | per request |
| 6 | [Get View List](06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#6-get-view-list) | GET | `GET_VIEWS` (3005) | METADATA | 0.1 | per request |
| 7 | [Get View Details](06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#7-get-view-details) | GET | `GET_VIEW_DETAILS` (3013) | METADATA | 0.1 | per request |
| 8 | [Get View URL](06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#8-get-view-url) | GET | `GET_VIEW_URL` (5001) | METADATA | 0.1 | per request |
| 9 | [Get View Dependents](06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#9-get-view-dependents) | GET | `GET_VIEW_DEPENDENTS` (3034) | METADATA | 1 | per request |

**[VIEW_PREFERENCES.md](06%20%C2%B7%20Views%20Management/VIEW_PREFERENCES.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Add Favourite View](06%20%C2%B7%20Views%20Management/VIEW_PREFERENCES.md#1-add-favourite-view) | POST | `ADD_FAVOURITE_VIEW` (3017) | METADATA | 0.1 | per request |
| 2 | [Remove Favourite View](06%20%C2%B7%20Views%20Management/VIEW_PREFERENCES.md#2-remove-favourite-view) | DELETE | `REMOVE_FAVOURITE_VIEW` (3018) | METADATA | 0.1 | per request |

### 07 · Reports & Dashboards

**[DASHBOARDS.md](07%20%C2%B7%20Reports%20%26%20Dashboards/DASHBOARDS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Create Dashboard](07%20%C2%B7%20Reports%20%26%20Dashboards/DASHBOARDS.md#1-create-dashboard) | POST | `CREATE_DASHBOARD` (2060) | METADATA | 5 | per request |
| 2 | [Read Dashboard Metadata](07%20%C2%B7%20Reports%20%26%20Dashboards/DASHBOARDS.md#2-read-dashboard-metadata) | GET | `GET_DASHBOARD_METADATA` (2061) | METADATA | 1 | per request |
| 3 | [Update Dashboard](07%20%C2%B7%20Reports%20%26%20Dashboards/DASHBOARDS.md#3-update-dashboard) | PUT | `UPDATE_DASHBOARD` (2062) | METADATA | 5 | per request |

**[REPORTS.md](07%20%C2%B7%20Reports%20%26%20Dashboards/REPORTS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Create Report](07%20%C2%B7%20Reports%20%26%20Dashboards/REPORTS.md#1-create-report) | POST | `CREATE_ANALYSISVIEW` (2031) | METADATA | 5 | per request |
| 2 | [Read Report Metadata](07%20%C2%B7%20Reports%20%26%20Dashboards/REPORTS.md#2-read-report-metadata) | GET | `GET_REPORT_METADATA` (3052) | METADATA | 0.1 | per request |
| 3 | [Update Report](07%20%C2%B7%20Reports%20%26%20Dashboards/REPORTS.md#3-update-report) | PUT | `UPDATE_ANALYSISVIEW` (2032) | METADATA | 5 | per request |

### 08 · Share & Publish

**[EMBED_URL.md](08%20%C2%B7%20Share%20%26%20Publish/EMBED_URL.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Embed URL](08%20%C2%B7%20Share%20%26%20Publish/EMBED_URL.md#1-get-embed-url) | GET | `GET_EMBED_URL` (5002) | METADATA | 1 | per request |
| 2 | [Fetch All Embed URLs](08%20%C2%B7%20Share%20%26%20Publish/EMBED_URL.md#2-fetch-all-embed-urls) | GET | `FETCH_ALL_EMBED_URLS` (5017) | METADATA | 0.5 | per request |
| 3 | [Delete Embed URL](08%20%C2%B7%20Share%20%26%20Publish/EMBED_URL.md#3-delete-embed-url) | DELETE | `DELETE_EMBED_URL` (5018) | METADATA | 0.5 | per request |

**[PUBLISH.md](08%20%C2%B7%20Share%20%26%20Publish/PUBLISH.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Make View Public](08%20%C2%B7%20Share%20%26%20Publish/PUBLISH.md#1-make-view-public) | POST | `MAKE_VIEW_PUBLIC` (5013) | METADATA | 1 | per request |
| 2 | [Remove Public Permission](08%20%C2%B7%20Share%20%26%20Publish/PUBLISH.md#2-remove-public-permission) | DELETE | `REMOVE_PUBLIC_VIEW` (5014) | METADATA | 1 | per request |
| 3 | [Get Private URL](08%20%C2%B7%20Share%20%26%20Publish/PUBLISH.md#3-get-private-url) | GET | `GET_PRIVATE_URL` (5003) | METADATA | 0.1 | per request |
| 4 | [Create Private URL](08%20%C2%B7%20Share%20%26%20Publish/PUBLISH.md#4-create-private-url) | POST | `CREATE_PRIVATE_URL` (5004) | METADATA | 1 | per request |
| 5 | [Remove Private Access](08%20%C2%B7%20Share%20%26%20Publish/PUBLISH.md#5-remove-private-access) | DELETE | `REMOVE_PRIVATE_PERMISSION` (5012) | METADATA | 1 | per request |
| 6 | [Get Publish Configurations](08%20%C2%B7%20Share%20%26%20Publish/PUBLISH.md#6-get-publish-configurations) | GET | `GET_PUBLISH_CONFIGURATIONS` (5015) | METADATA | 0.1 | per request |
| 7 | [Update Publish Configurations](08%20%C2%B7%20Share%20%26%20Publish/PUBLISH.md#7-update-publish-configurations) | PUT | `UPDATE_PUBLISH_CONFIGURATIONS` (5016) | METADATA | 0.5 | per request |

**[SHARING.md](08%20%C2%B7%20Share%20%26%20Publish/SHARING.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Workspace Shared Details](08%20%C2%B7%20Share%20%26%20Publish/SHARING.md#1-get-workspace-shared-details) | GET | `GET_WORKSPACE_SHARE_INFO` (4007) | METADATA | 3 | per request |
| 2 | [Share Views](08%20%C2%B7%20Share%20%26%20Publish/SHARING.md#2-share-views) | POST | `SHARE_VIEWS` (4008) | METADATA | 5 | per request |
| 3 | [Update Shared Details](08%20%C2%B7%20Share%20%26%20Publish/SHARING.md#3-update-shared-details) | PUT | `UPDATE_SHARED_DETAILS_FOR_VIEW` (4020) | METADATA | 0.1 | per request |
| 4 | [Get Shared Details](08%20%C2%B7%20Share%20%26%20Publish/SHARING.md#4-get-shared-details) | GET | `GET_SHARED_DETAILS_FOR_VIEW` (4010) | METADATA | 0.1 | per request |
| 5 | [Remove Shared Views](08%20%C2%B7%20Share%20%26%20Publish/SHARING.md#5-remove-shared-views) | DELETE | `REMOVE_SHARE` (4009) | METADATA | 5 | per request |
| 6 | [Get My Permissions](08%20%C2%B7%20Share%20%26%20Publish/SHARING.md#6-get-my-permissions) | GET | `GET_MY_PERMISSIONS` (4011) | METADATA | 0.1 | per request |

**[SLIDESHOW_MANAGEMENT.md](08%20%C2%B7%20Share%20%26%20Publish/SLIDESHOW_MANAGEMENT.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Slide List](08%20%C2%B7%20Share%20%26%20Publish/SLIDESHOW_MANAGEMENT.md#1-get-slide-list) | GET | `GET_SLIDE_LIST` (5005) | METADATA | 1 | per request |
| 2 | [Get Slide URL](08%20%C2%B7%20Share%20%26%20Publish/SLIDESHOW_MANAGEMENT.md#2-get-slide-url) | GET | `GET_SLIDE_URL` (5006) | METADATA | 1 | per request |
| 3 | [Get Slide Info](08%20%C2%B7%20Share%20%26%20Publish/SLIDESHOW_MANAGEMENT.md#3-get-slide-info) | GET | `GET_SLIDE_INFO` (5007) | METADATA | 1 | per request |
| 4 | [Create Slide Show](08%20%C2%B7%20Share%20%26%20Publish/SLIDESHOW_MANAGEMENT.md#4-create-slide-show) | POST | `CREATE_SLIDE_SHOW` (5008) | METADATA | 2 | per request |
| 5 | [Update Slide Show](08%20%C2%B7%20Share%20%26%20Publish/SLIDESHOW_MANAGEMENT.md#5-update-slide-show) | PUT | `UPDATE_SLIDE_SHOW` (5009) | METADATA | 2 | per request |
| 6 | [Delete Slide Show](08%20%C2%B7%20Share%20%26%20Publish/SLIDESHOW_MANAGEMENT.md#6-delete-slide-show) | DELETE | `DELETE_SLIDE_SHOW` (5010) | METADATA | 2 | per request |

### 09 · Schedules & Alerts

**[DATA_ALERTS.md](09%20%C2%B7%20Schedules%20%26%20Alerts/DATA_ALERTS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Alerts In Workspace](09%20%C2%B7%20Schedules%20%26%20Alerts/DATA_ALERTS.md#1-get-alerts-in-workspace) | GET | `GET_ALERTS_IN_WORKSPACE` (3091) | METADATA | 2 | per request |
| 2 | [Get Alerts In View](09%20%C2%B7%20Schedules%20%26%20Alerts/DATA_ALERTS.md#2-get-alerts-in-view) | GET | `GET_ALERTS_IN_VIEW` (3092) | METADATA | 0.5 | per request |
| 3 | [Get View Metadata For Alert](09%20%C2%B7%20Schedules%20%26%20Alerts/DATA_ALERTS.md#3-get-view-metadata-for-alert) | GET | `GET_VIEW_METADATA_FOR_ALERT` (3093) | METADATA | 1 | per request |
| 4 | [Get Alert Configuration](09%20%C2%B7%20Schedules%20%26%20Alerts/DATA_ALERTS.md#4-get-alert-configuration) | GET | `GET_ALERT_CONFIGURATION` (3094) | METADATA | 1 | per request |
| 5 | [Create Alert](09%20%C2%B7%20Schedules%20%26%20Alerts/DATA_ALERTS.md#5-create-alert) | POST | `CREATE_ALERT` (2083) | METADATA | 3 | per request |
| 6 | [Update Alert](09%20%C2%B7%20Schedules%20%26%20Alerts/DATA_ALERTS.md#6-update-alert) | PUT | `UPDATE_ALERT` (2084) | METADATA | 3 | per request |
| 7 | [Delete Alerts](09%20%C2%B7%20Schedules%20%26%20Alerts/DATA_ALERTS.md#7-delete-alerts) | DELETE | `DELETE_ALERTS` (2085) | METADATA | 2 | per request |
| 8 | [Change Alert Status](09%20%C2%B7%20Schedules%20%26%20Alerts/DATA_ALERTS.md#8-change-alert-status) | PUT | `CHANGE_ALERT_STATUS` (2086) | METADATA | 1 | per request |
| 9 | [Run Alert](09%20%C2%B7%20Schedules%20%26%20Alerts/DATA_ALERTS.md#9-run-alert) | POST | `RUN_ALERT` (2087) | METADATA | 1 | per request |
| 10 | [Get Alert Events](09%20%C2%B7%20Schedules%20%26%20Alerts/DATA_ALERTS.md#10-get-alert-events) | GET | `GET_ALERT_EVENTS` (3095) | METADATA | 1 | per request |

**[EMAIL_SCHEDULES.md](09%20%C2%B7%20Schedules%20%26%20Alerts/EMAIL_SCHEDULES.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get Email Schedules](09%20%C2%B7%20Schedules%20%26%20Alerts/EMAIL_SCHEDULES.md#1-get-email-schedules) | GET | `GET EMAIL SCHEDULES` (3038) | METADATA | 1 | per request |
| 2 | [Create Email Schedule](09%20%C2%B7%20Schedules%20%26%20Alerts/EMAIL_SCHEDULES.md#2-create-email-schedule) | POST | `CREATE_EMAIL_SCHEDULE` (2050) | METADATA | 3 | per request |
| 3 | [Update Email Schedule](09%20%C2%B7%20Schedules%20%26%20Alerts/EMAIL_SCHEDULES.md#3-update-email-schedule) | PUT | `UPDATE_EMAIL_SCHEDULE` (2051) | METADATA | 3 | per request |
| 4 | [Delete Email Schedule](09%20%C2%B7%20Schedules%20%26%20Alerts/EMAIL_SCHEDULES.md#4-delete-email-schedule) | DELETE | `DELETE_EMAIL_SCHEDULE` (2052) | METADATA | 3 | per request |
| 5 | [Change Email Schedule Status](09%20%C2%B7%20Schedules%20%26%20Alerts/EMAIL_SCHEDULES.md#5-change-email-schedule-status) | PUT | `CHANGE_EMAIL_SCHEDULE_STATUS` (2053) | METADATA | 1 | per request |
| 6 | [Trigger Email Schedule](09%20%C2%B7%20Schedules%20%26%20Alerts/EMAIL_SCHEDULES.md#6-trigger-email-schedule) | POST | `TRIGGER_EMAIL_SCHEDULE` (2054) | METADATA | 1 | per request |

### 10 · DSML

**[AUTOML_ANALYSIS.md](10%20%C2%B7%20DSML/AUTOML_ANALYSIS.md)**

| # | API Name | Method | Gateway Action (api-id) | Category | Units | Charged |
|---|----------|--------|-------------------------|----------|-------|---------|
| 1 | [Get AutoML Analysis In Org](10%20%C2%B7%20DSML/AUTOML_ANALYSIS.md#1-get-automl-analysis-in-org) | GET | `GET_AUTOML_ANALYSIS_IN_ORGANIZATION` (3054) | METADATA | 2 | per request |
| 2 | [Get AutoML Analysis In Workspace](10%20%C2%B7%20DSML/AUTOML_ANALYSIS.md#2-get-automl-analysis-in-workspace) | GET | `GET_AUTOML_ANALYSIS_IN_Workspace` (3055) | METADATA | 1 | per request |
| 3 | [Get AutoML Analysis Details](10%20%C2%B7%20DSML/AUTOML_ANALYSIS.md#3-get-automl-analysis-details) | GET | `GET_AUTOML_ANALYSIS_DETAILS` (3056) | METADATA | 1 | per request |
| 4 | [Get Deployments For A Model](10%20%C2%B7%20DSML/AUTOML_ANALYSIS.md#4-get-deployments-for-a-model) | GET | `GET_DEPLOYMENTS_FOR_A_MODEL` (3057) | METADATA | 1 | per request |
| 5 | [Create AutoML Analysis](10%20%C2%B7%20DSML/AUTOML_ANALYSIS.md#5-create-automl-analysis) | POST | `CREATE_AUTOML_ANALYSIS` (2065) | METADATA | 3 | per request |
| 6 | [Delete AutoML Analysis](10%20%C2%B7%20DSML/AUTOML_ANALYSIS.md#6-delete-automl-analysis) | DELETE | `DELETE_AUTOML_ANALYSIS` (2066) | METADATA | 2 | per request |
| 7 | [Delete AutoML Analysis Model](10%20%C2%B7%20DSML/AUTOML_ANALYSIS.md#7-delete-automl-analysis-model) | DELETE | `DELETE_AUTOML_ANALYSIS_MODEL` (2067) | METADATA | 2 | per request |
| 8 | [Create AutoML Analysis Deployment](10%20%C2%B7%20DSML/AUTOML_ANALYSIS.md#8-create-automl-analysis-deployment) | POST | `CREATE_AUTOML_ANALYSIS_DEPLOYMENT` (2068) | METADATA | 3 | per request |
| 9 | [Run AutoML Analysis](10%20%C2%B7%20DSML/AUTOML_ANALYSIS.md#9-run-automl-analysis) | POST | `RUN_AUTOML_ANALYSIS_DEPLOYMENT` (2069) | METADATA | 2 | per request |
| 10 | [Delete AutoML Analysis Model Deployment](10%20%C2%B7%20DSML/AUTOML_ANALYSIS.md#10-delete-automl-analysis-model-deployment) | DELETE | `DELETE_AUTOML_ANALYSIS_DEPLOYMENT` (2070) | METADATA | 2 | per request |
| 11 | [AutoML What If Analysis](10%20%C2%B7%20DSML/AUTOML_ANALYSIS.md#11-automl-what-if-analysis) | POST | `AUTOML_WHAT_IF_ANALYSIS` (2071) | METADATA | 1 | per request |

## Variable costs

Three operation families have no single fixed cost. The API maps to a gateway action charging `0`, and the real charge is applied against a second action chosen from the request payload.

### Export — synchronous and asynchronous

Export Data, Create Export Job using View ID and Create Export Job using SQL Query all map to `INITIATE_EXPORT` (7001), which costs `0`. The charge lands when the data is produced, chosen from the requested output format and the view type:

| Condition on the request | Charged action | Cost |
|--------------------------|----------------|------|
| `responseFormat` is `image`, or `pdf` on a chart / analysis view | `EXPORT_CHART` (7004) | **10 units** per request |
| `responseFormat` is `pdf` on any other view type | `EXPORT_PDF` (7003) | **5 units** per 1000 rows |
| `responseFormat` is `html` | `EXPORT_HTML` (7005) | **15 units** per request |
| The exported view is a dashboard | `EXPORT_DASHBOARD` (7006) | **15 units** per request |
| Anything else — `csv`, `json`, `xml`, `xls` | `EXPORT_DATA` (7002) | **3 units** per 1000 rows |

The conditions are evaluated in that order, so a PDF of a chart is costed as a chart export, not as a PDF export.

Get Export Job Details (`EXPORT_JOB_STATUS`, 9001) and Download Exported Data (`DOWNLOAD_FILE`, 9002) cost `0` — polling and downloading are free.

### Import — synchronous, asynchronous and batch

Import Data, Create Import Job and the batch import APIs map to `INITIATE_IMPORT` (8001) or `BATCH_IMPORT_FILE_UPLOAD` (8005), both `0`. The charge is applied to the rows actually written, chosen from `importType`:

| `importType` | Charged action | Cost |
|--------------|----------------|------|
| `append` | `IMPORT` (8002) | **10 units** per 1000 rows |
| `truncateadd` | `IMPORT_TRUNCATE_ADD` (8003) | **10 units** per 1000 rows |
| `updateadd` | `IMPORT_UPDATE_ADD` (8004) | **15 units** per 1000 rows |

For a batch import the charge is applied once, when the final batch is committed — the individual file-upload calls are free. A failed or aborted import is still charged for the rows it wrote before failing.

Get Import Job Details (`IMPORT_JOB_STATUS`, 9003) costs `0`.

### Copy Workspace

| Request | Charged action | Cost |
|---------|----------------|------|
| `copyData` false or absent | `COPY_WORKSPACE_WO_DATA` (2002) | **25 units** per request |
| `copyData` true | `COPY_WORKSPACE_WITH_DATA` (2003) plus the base | **25 units** plus **1 unit** per 1000 rows copied |

The 25-unit base is always included — the with-data cost is additive, not a replacement.

## API-specific throttles

These APIs carry an extra request threshold on top of the category ceiling. Crossing the threshold inside the window locks the caller out of that API for the lock period — retrying in a tight loop only extends the lockout.

| API Name | Gateway Action (api-id) | Throttle |
|----------|-------------------------|----------|
| [Get Aggregate Formula](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/AGGREGATE_FORMULAS.md#1-get-aggregate-formula) | `GET AGGREGATE FORMULA` (3037) | 30 requests per user per minute, 10-minute lockout on breach |
| [Add Aggregate Formula](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/AGGREGATE_FORMULAS.md#2-add-aggregate-formula) | `ADD_AGG_FORMULA` (2044) | 20 requests per user per minute, 10-minute lockout on breach |
| [Edit Aggregate Formula](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/AGGREGATE_FORMULAS.md#3-edit-aggregate-formula) | `EDIT_AGG_FORMULA` (2045) | 20 requests per user per minute, 10-minute lockout on breach |
| [Delete Aggregate Formula](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/AGGREGATE_FORMULAS.md#4-delete-aggregate-formula) | `DELETE AGG FORMULA` (2046) | 20 requests per user per minute, 10-minute lockout on breach |
| [Get Custom Formulas](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/FORMULA_COLUMNS.md#1-get-custom-formulas) | `GET_FORMULA_COLUMN` (3036) | 30 requests per user per minute, 10-minute lockout on breach |
| [Add Custom Formula](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/FORMULA_COLUMNS.md#2-add-custom-formula) | `ADD_FORMULA_COLUMN` (2041) | 20 requests per user per minute, 10-minute lockout on breach |
| [Edit Custom Formula](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/FORMULA_COLUMNS.md#3-edit-custom-formula) | `EDIT_FORMULA_COLUMN` (2042) | 20 requests per user per minute, 10-minute lockout on breach |
| [Delete Custom Formula](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/FORMULA_COLUMNS.md#4-delete-custom-formula) | `DELETE_FORMULA_COLUMN` (2043) | 30 requests per user per minute, 10-minute lockout on breach |
| [Create Query Table](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/QUERY_TABLES.md#2-create-query-table) | `CREATE_QT` (2037) | 20 requests per user per minute, 10-minute lockout on breach |
| [Edit Query Table](04%20%C2%B7%20Data%20Modeling%20%26%20Schema/QUERY_TABLES.md#3-edit-query-table) | `EDIT_QT` (2038) | 20 requests per user per minute, 10-minute lockout on breach |
| [Sync Data](05%20%C2%B7%20Data%20Operations/DATA_SYNC_AND_CONNECTIVITY.md#1-sync-data) | `SYNC_DATA` (3025) | 5 requests per minute, 5-minute lockout on breach |
| [Refetch Data](05%20%C2%B7%20Data%20Operations/DATA_SYNC_AND_CONNECTIVITY.md#2-refetch-data) | `REFETCH_DATA` (3026) | 5 requests per minute, 5-minute lockout on breach |
| [Create Dashboard](07%20%C2%B7%20Reports%20%26%20Dashboards/DASHBOARDS.md#1-create-dashboard) | `CREATE_DASHBOARD` (2060) | 10 requests per user per minute, 10-minute lockout on breach |
| [Read Dashboard Metadata](07%20%C2%B7%20Reports%20%26%20Dashboards/DASHBOARDS.md#2-read-dashboard-metadata) | `GET_DASHBOARD_METADATA` (2061) | 20 requests per user per minute, 10-minute lockout on breach |
| [Update Dashboard](07%20%C2%B7%20Reports%20%26%20Dashboards/DASHBOARDS.md#3-update-dashboard) | `UPDATE_DASHBOARD` (2062) | 10 requests per user per minute, 10-minute lockout on breach |

Limits enforced outside the URL configuration, and so not in the table above:

- Create Query Table and Edit Query Table are additionally capped at 15 requests per minute service-wide.
- Copy Workspace allows one copy operation per organisation at a time.
- Asynchronous export allows at most 5 simultaneous export jobs per organisation.
- Refetch Data allows one refetch per table at a time.

## Zero-cost APIs

12 APIs are configured at `0` units. They still count against the frequency limit of their category.

Read this with one caveat: for the import/export **initiation** APIs the `0` is only the cost of the request that starts the work — the data itself is charged against a second action once produced, as described in [Variable costs](#variable-costs). The genuinely free APIs are the three job-status and download calls.

| API Name | Gateway Action (api-id) | Category |
|----------|-------------------------|----------|
| [Create Export Job using SQL Query (Asynchronous)](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_EXPORT.md#1-create-export-job-using-sql-query-asynchronous) | `INITIATE_EXPORT` (7001) | BULK |
| [Create Export Job using View ID (Asynchronous)](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_EXPORT.md#2-create-export-job-using-view-id-asynchronous) | `INITIATE_EXPORT` (7001) | BULK |
| [Get Export Job Details](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_EXPORT.md#3-get-export-job-details) | `EXPORT_JOB_STATUS` (9001) | METADATA |
| [Download Exported Data](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_EXPORT.md#4-download-exported-data) | `DOWNLOAD_FILE` (9002) | METADATA |
| [Create Import Job for a New Table (Asynchronous)](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_IMPORT.md#1-create-import-job-for-a-new-table-asynchronous) | `INITIATE_IMPORT` (8001) | BULK |
| [Create Import Job for an Existing Table (Asynchronous)](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_IMPORT.md#2-create-import-job-for-an-existing-table-asynchronous) | `INITIATE_IMPORT` (8001) | BULK |
| [Batch Import Data into New Table](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_IMPORT.md#3-batch-import-data-into-new-table) | `BATCH_IMPORT_FILE_UPLOAD` (8005) | BULK |
| [Batch Import Data into Existing Table](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_IMPORT.md#4-batch-import-data-into-existing-table) | `BATCH_IMPORT_FILE_UPLOAD` (8005) | BULK |
| [Get Import Job Details](05%20%C2%B7%20Data%20Operations/ASYNC_DATA_IMPORT.md#5-get-import-job-details) | `IMPORT_JOB_STATUS` (9003) | METADATA |
| [Export Data from a View](05%20%C2%B7%20Data%20Operations/SYNC_DATA_EXPORT.md#1-export-data-from-a-view) | `INITIATE_EXPORT` (7001) | BULK |
| [Import Data into a New Table (Synchronous)](05%20%C2%B7%20Data%20Operations/SYNC_DATA_IMPORT.md#1-import-data-into-a-new-table-synchronous) | `INITIATE_IMPORT` (8001) | BULK |
| [Import Data into an Existing Table (Synchronous)](05%20%C2%B7%20Data%20Operations/SYNC_DATA_IMPORT.md#2-import-data-into-an-existing-table-synchronous) | `INITIATE_IMPORT` (8001) | BULK |

## Reducing unit consumption

- **Load data in bulk.** 100,000 rows cost ~1,000 units through Import Data and 10,000 units through Add Row.
- **Pick the cheapest export format you can live with.** CSV and JSON cost 3 units per 1000 rows; the same data as HTML costs a flat 15 units per request and as a chart image 10 units per request. For large row counts the flat-rate formats are cheaper; for small ones they are not.
- **Prefer listing APIs over per-object reads.** Get Views at `0.1` units returns in one call what a loop of per-view metadata reads would cost many times over.
- **Poll at a sane interval.** Status and download calls are free in units but are charged against the `BULK` and `METADATA` frequency budgets.
- **Watch `apiUnits` in Get Resource Details.** It costs `0.1` units itself and reports allocated, used and remaining units.

## Notes on this reference

- Unit costs, the row basis, unit categories and per-category frequency limits come from the API gateway configuration (`webapps/db/WEB-INF/gatewayxmls/zagateway-restapi.xml`). The method/URL-to-`api-id` binding and the API-specific throttles come from the URL security configuration (`webapps/db/WEB-INF/securityxmls/security-restapi.xml`).
- Internal-service routes and service-specific unit exemptions exist in those configurations but are out of scope here — this document covers only the public, documented V2 APIs.
- The frequency limits are the base configuration. An organisation's effective ceiling is the base value scaled by a plan multiplier.
- **Get Org Recent Items** has no URL binding of its own in the security configuration; its cost is taken from `GET_RECENT_VIEWS` (3007), the recent-items action in the gateway.
