---
type: Reference
title: Custom roles
description: Organization-defined custom roles in Zoho Analytics - the three access permission levels, the full permission catalogue by category, how a custom role name is used by the REST API v2 user-management endpoints, and how its permissions map onto the API's authorization vocabulary.
tags:
  - zoho-analytics
  - rest-api-v2
  - roles
  - custom-roles
  - permissions
  - authorization
sources:
  - id: help-manage-role
    resource: "https://www.zoho.com/analytics/help/manage-role.html"
    title: "Manage Roles - Zoho Analytics help"
    author: "team:zoho-analytics-docs"
  - id: help-user-role-management
    resource: "https://www.zoho.com/analytics/help/user-role-management.html"
    title: "User Role Management - Zoho Analytics help"
    author: "team:zoho-analytics-docs"
  - id: md-workspace-users
    resource: "/domains/users-and-groups/workspace-users/overview.md"
    title: Workspace Users - group overview
  - id: md-org-users
    resource: "/domains/users-and-groups/org-users/overview.md"
    title: Organization Users - group overview
  - id: md-sharing
    resource: "/domains/share-and-publish/sharing/overview.md"
    title: Sharing - group overview
generated:
  by: claude-opus-5/claude-code
  at: 2026-09-30T00:00:00Z
status: stable
---

# Summary

A **custom role** is an organization-defined set of permissions that an administrator assembles once and then assigns to users, instead of accepting the broader bundle that a predefined role carries. Custom roles apply **over the workspaces shared with the user**: a user holding one gets the configured permissions on every view of the selected entity in those workspaces, including views created later.

> Unlike the rest of this bundle, this document is derived from the Zoho Analytics **help documentation** rather than from the REST API reference or the OpenAPI specifications, because custom roles are configured in the product interface and the API only consumes their names. Sources are listed in the frontmatter. Treat the permission labels as the product's own wording.

The single most important fact for an API caller:

> **The REST API v2 can assign a custom role, but cannot create, list, modify or delete one.** There is no roles endpoint. A custom role is created in the interface and reaches the API only as a **name string** in the `role` attribute of the workspace-user endpoints. The permissions behind that name are invisible to the API; the API sees only whether the name exists.

# Availability and Who Manages Them

| Question | Answer |
|---|---|
| Which plans? | Premium plan and above. |
| Who can create and manage them? | The **Account Admin** and **Organization Admins**. A Workspace Admin cannot. |
| Where? | **Organization Settings → Manage Roles → Add New Role** in the Zoho Analytics interface. |
| Is there an API? | No. See [Using a Custom Role from the API](#using-a-custom-role-from-the-api). |
| Licensing impact | Licensing counts **users in the organization**, not roles assigned. Creating more roles does not change the bill. |

# Access Permission Levels

Every custom role starts by choosing one of three access levels. The level decides which permission categories are even offered - the Data and Data Source categories appear only at the widest level.

| Level | The role's users can reach | Data and Data Source permissions available? |
|---|---|---|
| **All Dashboards** | Dashboards only. | No |
| **All Reports And Dashboards** | Reports and dashboards; report creation can be granted. | No |
| **All Data, Reports And Dashboards** | Tables and underlying data as well as reports and dashboards. | Yes |

Because the level is defined in terms of *all* views of the selected entity, a user with a custom role picks up **new views automatically** as they are created in a shared workspace. This is the main behavioural difference from a `USER`, who sees nothing until a view is explicitly shared.

# Permission Catalogue

The permissions an administrator can switch on, grouped as the interface groups them.

## Create

| Permission | Effect |
|---|---|
| Create Dashboards | Create new dashboards. |
| Create Reports | Create new reports. |
| Create Table / Import Data | Create tables and import data into the workspace. |
| Create Query Table | Create SQL query tables. |
| Formula Column / Aggregate Formula / Bucket Column | Create the three derived-column kinds. |
| Create Folder | Create folders to organise views. |

## Data

*Offered only at the **All Data, Reports And Dashboards** level.*

| Permission | Effect |
|---|---|
| Add Row | Insert rows. |
| Delete Row | Delete rows. |
| Modify Row | Update existing rows. |
| Only Append Rows | Import that appends and never modifies existing rows. |
| Delete All Rows And Add New Rows | Import that truncates the table first. |
| Add Or Update Rows | Upsert-style import matched on key columns. |
| Add New, Replace Existing And Delete Missing Rows | Full-sync import. |
| Create, Modify And Delete Data Archives | Manage data archives. |

## Design

| Permission | Effect |
|---|---|
| Design | Edit the structure of tables, reports and dashboards - adding and deleting columns, lookup columns, and access to report settings. |

## Interaction

| Permission | Effect |
|---|---|
| Read Access | Open the view. Everything else is meaningless without it. |
| View Underlying Data | See the rows behind an aggregated report. |
| Drill Down | Drill down by column values. |
| Drill Through | Drill through to a linked report. |
| Drill Actions | Use configured drill actions. |
| Zia Insights | Use Zia-generated insights. |
| GenAI Skills | Use the generative-AI skills. |

## Share and Collaborate

| Permission | Effect |
|---|---|
| Share Views / Child Reports | Re-share views, and the reports derived from them. |
| Commenting Actions | Post and manage comments. |
| Private Links | Create and manage private links. |
| Access Admin/Owner Presets | Use presets created by an administrator or the view owner. |
| Allow Preset Creation | Create their own presets. |

## Publish

| Permission | Effect |
|---|---|
| Export | Export view data. |
| Manage Email Schedules | Create and manage scheduled email delivery. |
| Manage Data Alerts | Create and manage data alerts. |
| Create Slideshow | Create slideshows. |
| Public Views | Publish views publicly. |

## Data Source

*Offered only at the **All Data, Reports And Dashboards** level.*

| Permission | Effect |
|---|---|
| View Data Source | See datasource connections and their details. |
| Use Data Source | Use an existing connection when importing. |
| Sync Data | Trigger a sync or refetch. |
| Edit Data Source | Change connection settings. |
| Remove Data Source | Delete a connection. |

# How These Map onto API Permission Checks

Endpoint documents in this bundle phrase their requirement as *"any user with **Export** permission on the view"* or *"any user with **Sync Data** permission on the workspace"*. Those names are the same vocabulary the custom-role interface uses, so a custom role is one of the ways a caller comes to hold them - alongside a direct share ([Share Views](../domains/share-and-publish/sharing/share-views.md)) and a workspace role.

| Custom-role permission | Vocabulary used in this bundle | Where it appears |
|---|---|---|
| Read Access | `read` share key | Every read endpoint |
| Export | `export` share key, "Export permission" | [Synchronous](../domains/data-operations/sync-data-export/overview.md) and [asynchronous](../domains/data-operations/async-data-export/overview.md) export, email schedules |
| View Underlying Data | `vud` share key | Export, row reads |
| Drill Down / Drill Through / Drill Actions | `drillDown`, `drillThrough`, `drillActions` share keys | [Sharing](../domains/share-and-publish/sharing/overview.md) |
| Zia Insights | `insight` share key | [Sharing](../domains/share-and-publish/sharing/overview.md) |
| Add Row / Modify Row / Delete Row | `addRow`, `updateRow`, `deleteRow` share keys | [Row operations](../domains/data-operations/row-operations/overview.md) |
| Only Append Rows | `importAppend`, `importType: APPEND` | [Synchronous import](../domains/data-operations/sync-data-import/overview.md) |
| Add Or Update Rows | `importAddOrUpdate`, `importType: UPDATEADD` | [Synchronous import](../domains/data-operations/sync-data-import/overview.md) |
| Delete All Rows And Add New Rows | `importDeleteAllAdd`, `importType: TRUNCATEADD` | [Synchronous import](../domains/data-operations/sync-data-import/overview.md) |
| Add New, Replace Existing And Delete Missing Rows | `importDeleteUpdateAdd` | [Synchronous import](../domains/data-operations/sync-data-import/overview.md) |
| Share Views / Child Reports | `share` share key, "Share permission" | [Share Views](../domains/share-and-publish/sharing/share-views.md) |
| Commenting Actions | `discussion` share key | [Sharing](../domains/share-and-publish/sharing/overview.md) |
| Access Admin/Owner Presets, Allow Preset Creation | `accessAdminPresets`, `createPreset` share keys | [Sharing](../domains/share-and-publish/sharing/overview.md) |
| Create Table / Import Data | "Create Table permission" | [Import](../domains/data-operations/sync-data-import/overview.md), [Data sync](../domains/data-operations/data-sync-and-connectivity/overview.md) |
| Design | "Design & Modify permission" | [Views management](../domains/views-management/view-operations/overview.md), [Columns](../domains/data-modeling-and-schema/columns/overview.md) |
| Sync Data | "Sync Data permission" | [Data sync and connectivity](../domains/data-operations/data-sync-and-connectivity/overview.md) |
| View Data Source | "View Datasource permission" | [Get Datasources](../domains/data-operations/data-sync-and-connectivity/get-datasources.md) |
| Edit Data Source | "Edit Datasource permission" | [Update Datasource Connection](../domains/data-operations/data-sync-and-connectivity/update-datasource-connection.md) |
| Manage Email Schedules | "Create Email Schedule permission" | [Email schedules](../domains/schedules-and-alerts/email-schedules/overview.md) |
| Public Views | "Make Public permission" | [Publish](../domains/share-and-publish/publish/overview.md) |

> **This mapping is by name and observed behaviour, not a published identity.** Zoho does not document a formal one-to-one correspondence between custom-role checkboxes and share-permission keys, and a few custom-role permissions (GenAI Skills, Create, Modify And Delete Data Archives, Use Data Source, Remove Data Source, Private Links, Manage Data Alerts, Create Slideshow, Create Folder) have no share key of their own - they gate interface features or whole endpoint families rather than a per-view flag. When an authorization outcome matters, verify it against the live service rather than inferring it from this table.

# Using a Custom Role from the API

A custom role reaches the REST API in exactly one way: as the **`role`** string in the workspace-user endpoints.

| Endpoint | How the custom role is used |
|---|---|
| [Add Workspace Users](../domains/users-and-groups/workspace-users/add-workspace-users.md) | `role` accepts `"WORKSPACEADMIN"`, `"USER"`, or the exact name of a custom role. Omitted, it defaults to `"USER"`. |
| [Change Workspace Users Role](../domains/users-and-groups/workspace-users/change-workspace-users-role.md) | `role` is mandatory and accepts the same three forms. Requires Account Admin or Organization Admin. |
| [Get Workspace Users](../domains/users-and-groups/workspace-users/get-workspace-users.md) | Returns `users[].role` as the **exact custom role name**, not a numeric identifier. This is the only way to discover which custom roles are in use. |

Rules that follow from that:

1. **The name must match exactly**, including case and spacing. An unknown name fails with [`7550`](error-codes.md#error-7550) (HTTP 400).
2. **There is no way to enumerate the available role names from the API.** [Get Workspace Users](../domains/users-and-groups/workspace-users/get-workspace-users.md) shows only the roles already assigned in that workspace. To validate a name before assigning it, read it from the interface or keep a configured list.
3. **A custom role is a workspace-level assignment.** The organization-level role (`ORGADMIN`, `USER`, `VIEWER` - see [Roles and permissions](roles-and-permissions.md)) remains a ceiling: a `VIEWER` stays read-only whatever custom role is applied.
4. **Renaming a role in the interface breaks stored automation.** Any script holding the old string starts failing with `7550`.

# Custom Role Compared with the Predefined Roles

| | Custom Role | Viewer | User | Workspace Administrator |
|---|---|---|---|---|
| **Access scope** | All views of the selected entity in a shared workspace | Only views explicitly shared to them | Only views explicitly shared to them | All views in the workspace |
| **Access to new views** | Automatic, for the selected entity | No, until shared | No, until shared | Automatic |
| **Create or modify reports** | Yes, if granted | No | No | Yes |
| **Add or modify data** | Yes, if granted | No | Yes, in shared tables | Yes |
| **Administrative privileges** | None unless granted | None | None | All, except renaming, deleting or backing up the workspace |

# Related

- [Roles and permissions](roles-and-permissions.md) - the full authorization model: organization roles, workspace roles and share permissions.
- [Permission matrix](permission-matrix.md) - the scope and permission requirement of every endpoint.
- [Workspace Users](../domains/users-and-groups/workspace-users/overview.md) - the endpoints that assign a role.
- [Organization Users](../domains/users-and-groups/org-users/overview.md) - organization-level role assignment.
- [Manage users and roles](../workflows/manage-users-and-roles.md) - the end-to-end playbook.
- [Sharing](../domains/share-and-publish/sharing/overview.md) - the per-view permission keys.
