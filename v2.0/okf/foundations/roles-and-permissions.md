---
type: Reference
title: Roles and permissions
description: The authorization model of Zoho Analytics REST API v2 - organization roles, workspace roles, view-level share permissions, ownership, and how the "Permission Required" statements in endpoint documents should be read.
tags:
  - zoho-analytics
  - rest-api-v2
  - roles
  - permissions
  - authorization
  - criteria
sources:
  - id: md-org-users
    resource: /domains/users-and-groups/org-users/overview.md
    title: Organization Users - group overview
  - id: md-workspace-users
    resource: /domains/users-and-groups/workspace-users/overview.md
    title: Workspace Users - group overview
  - id: md-sharing
    resource: /domains/share-and-publish/sharing/overview.md
    title: Sharing - group overview
  - id: md-all
    resource: /domains/index.md
    title: Permission Required rows and Permission Model sections of every document
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

Authorization is evaluated in layers, from broad to narrow. An operation succeeds if **any** of the alternatives named in the endpoint's "Permission required" statement holds for the authenticated user. Failing every alternative returns HTTP 403 with [`7301`](error-codes.md#error-7301) (`SECURITY_NOT_PERMITTED`). The OAuth scope on the token is a separate, additional requirement (see [Authentication](authentication.md)).

```text
Account Admin ─ owns the organization; can do everything
   └─ Organization Admin ─ manages users and workspaces org-wide (cannot exceed Account Admin)
        └─ Workspace Admin ─ full control of one workspace
             └─ View Owner ─ created the view
                  └─ Shared user / group member ─ holds specific permissions on specific views
                       └─ Viewer ─ read-only org role
```

# Organization Roles

Managed with the [Organization Users](../domains/users-and-groups/org-users/overview.md) endpoints (`role` values in CONFIG).

| Role (API value) | Display name | What it can do |
|---|---|---|
| Account Admin (implicit; the organization creator) | Account Admin | Everything in the organization: billing, users, every workspace. Exactly one per organization. Some endpoints are Account Admin only (Get Org Admins, Change Workspace Users Status). |
| `ORGADMIN` | Organization Admin | Manage users and all workspaces across the organization. Cannot be assigned inside a portal domain (`6089`). |
| `USER` | User | Standard user. Owns and manages the workspaces they create; accesses what is shared with them. |
| `VIEWER` | Viewer | Read-only. Can open shared reports and dashboards, cannot create or modify data or design. A Viewer can never gain write access through a share. |

The organization role is a **ceiling**: a `USER` can be Workspace Admin of a workspace they own, but a `VIEWER` is read-only everywhere.

# Workspace Roles

Managed with the [Workspace Users](../domains/users-and-groups/workspace-users/overview.md) endpoints.

| Role (API value) | What it can do |
|---|---|
| `WORKSPACEADMIN` (Workspace Admin) | Full access to one workspace: create and delete views, manage users and groups of the workspace, share, schedule, import and export. The workspace owner is a Workspace Admin. |
| `USER` | Accesses the views shared to them, with whatever permissions the share grants. |
| Custom role name | An organization-defined custom role; the name must exist exactly (`7550`). The permissions it carries are configured in the interface, not through the API - see [Custom roles](custom-roles.md). |

Workspace-level user management asymmetry: Workspace Admins may add and remove workspace users, but changing a user's status or role requires Account Admin or Organization Admin.

# View-Level Share Permissions

When a view is shared to a user or a group ([Share Views](../domains/share-and-publish/sharing/share-views.md)), the share carries a permission set. These names are used verbatim in endpoint "Permission required" statements ("any user with Export permission on the view").

| Permission key | Grants |
|---|---|
| `read` | Open the view. **Always required**; a share without `read` fails with `8074`. |
| `export` | Export the view's data (sync and async export, email schedules). |
| `vud` | View Underlying Data of an aggregated report. `vudSelectedColumns` limits it to `vudColumns`. |
| `drillDown` | Drill down by column values; `drillColumns` limits the columns. |
| `addRow`, `updateRow`, `deleteRow`, `deleteAllRows` | Row-level writes on a table. |
| `importAppend`, `importAddOrUpdate`, `importDeleteAllAdd`, `importDeleteUpdateAdd` | Import into the table in the matching `importType` mode. |
| `share` | Re-share the view. Cannot be combined with write permissions for read-only users (`7545`). |
| `discussion`, `insight`, `drillThrough`, `drillActions`, `accessAdminPresets`, `createPreset` | Collaboration, Zia insights, drill-through actions and report presets. |

Row filters (`criteria`) and column lists (`columns`) narrow what the shared user sees; see [Filter criteria syntax](filter-criteria-syntax.md). Public links, private links, embed URLs and slideshows are modeled as shares to reserved pseudo-users and are always read-only.

Workspace-level permissions referenced by endpoint documents include **Create Table**, **Sync Data**, **Create Email Schedule**, **Publish** and **Make Public**; they are granted through the Zoho Analytics interface or through workspace-admin rights.

# Reading a "Permission Required" Statement

A typical statement: *"The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Export permission on the view."*

1. Organization role first: Account Admin or Organization Admin passes.
2. Workspace role next: Workspace Admin of the workspace in the URL passes.
3. Ownership: the user who created the view passes when the statement names the View Owner.
4. Share permission: a user (directly or through a group) holding the named permission on **every** view involved passes. For SQL exports the check runs on every table the query touches.

Additional gates that can apply regardless of role:

| Gate | Signal | Where it applies |
|---|---|---|
| Feature not enabled for the organization or plan | `8023` (Embedded Analytics), `6063` (slideshows), `6054`/`6056` (private links), plan-gated AutoML | Embed, slideshow, publish, AutoML families |
| Organization security control disables the operation | `8088` | Export, private links |
| Caller's primary email not verified | `7565` | Export job creation, mutating publish and slideshow endpoints |
| Job ownership | `8124` | Polling or downloading another user's export job |
| Request arrives through a Client Portal domain where the family is disabled | `7301` | Embed URL family and others; see [White label & Client Portal](white-label-client-portal.md) |

# Related

- [Custom roles](custom-roles.md) - organization-defined roles and their permission catalogue.
- [Permission matrix](permission-matrix.md) - the requirement of every endpoint in one table.
- [OAuth scopes](oauth-scopes.md)
- [Sharing](../domains/share-and-publish/sharing/overview.md)
