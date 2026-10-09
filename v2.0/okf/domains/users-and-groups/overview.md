---
type: API Domain
title: Users & Groups
description: "API for managing users and groups in Zoho Analytics — covering org-level users, workspace-level users, and workspace groups."
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - api-domain
api:
  domain: users-and-groups
  groups:
    - group: org-users
      title: Organization Users
      doc: "/domains/users-and-groups/org-users/overview.md"
      endpoint_count: 7
    - group: custom-roles
      title: Custom Roles
      doc: "/domains/users-and-groups/custom-roles/overview.md"
      endpoint_count: 4
    - group: workspace-users
      title: Workspace Users
      doc: "/domains/users-and-groups/workspace-users/overview.md"
      endpoint_count: 8
    - group: workspace-groups
      title: Workspace Groups
      doc: "/domains/users-and-groups/workspace-groups/overview.md"
      endpoint_count: 7
  endpoint_count: 26
  openapi: "/references/openapi/user-groups-grouped-api.json"
sources:
  - id: openapi-spec
    resource: "/references/openapi/user-groups-grouped-api.json"
    title: OpenAPI 3 specification - user-groups-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

API for managing users and groups in Zoho Analytics — covering org-level users, workspace-level users, and workspace groups.

# API Groups

| Group | Endpoints | Description |
|---|---|---|
| [Organization Users](org-users/overview.md) | 7 | APIs that allow the Account Admin and the Organization Admins of a Zoho Analytics organization to manage its users - listing, adding, removing, activating, deactivating and changing the org-level role of the users, and listing the users who hold the Organization Admin role. |
| [Custom Roles](custom-roles/overview.md) | 4 | APIs that allow the Account Admin and the Organization Admins of a Zoho Analytics organization to define custom roles - named permission bundles that can be granted to users in place of the built-in roles. |
| [Workspace Users](workspace-users/overview.md) | 8 | APIs that manage the users and the administrators of a single Zoho Analytics workspace - controlling who has access to the workspace, the role they hold within it, and whether that access is currently active. |
| [Workspace Groups](workspace-groups/overview.md) | 7 | APIs that manage the groups of a Zoho Analytics workspace. |

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Users](org-users/get-users.md) | GET | `/restapi/v2/users` | `getUsers` | `ZohoAnalytics.usermanagement.read` | 200 |
| [Add Users](org-users/add-users.md) | POST | `/restapi/v2/users` | `addUsers` | `ZohoAnalytics.usermanagement.create` | 204 |
| [Remove Users](org-users/remove-users.md) | DELETE | `/restapi/v2/users` | `removeUsers` | `ZohoAnalytics.usermanagement.delete` | 204 |
| [Activate Users](org-users/activate-users.md) | PUT | `/restapi/v2/users/active` | `activateUsers` | `ZohoAnalytics.usermanagement.update` | 204 |
| [Deactivate Users](org-users/de-activate-users.md) | PUT | `/restapi/v2/users/inactive` | `deActivateUsers` | `ZohoAnalytics.usermanagement.update` | 204 |
| [Change User Role](org-users/change-user-role.md) | PUT | `/restapi/v2/users/role` | `changeUserRole` | `ZohoAnalytics.usermanagement.update` | 204 |
| [Get Org Admins](org-users/get-org-admins.md) | GET | `/restapi/v2/orgadmins` | `getOrgAdmins` | `ZohoAnalytics.share.read` | 200 |
| [Get Custom Roles](custom-roles/get-custom-roles.md) | GET | `/restapi/v2/orgs/roles` | `getCustomRoles` | `ZohoAnalytics.usermanagement.read` | 200 |
| [Create Custom Role](custom-roles/create-custom-role.md) | POST | `/restapi/v2/orgs/roles` | `createCustomRole` | `ZohoAnalytics.usermanagement.create` | 200 |
| [Update Custom Role](custom-roles/update-custom-role.md) | PUT | `/restapi/v2/orgs/roles/{role-id}` | `updateCustomRole` | `ZohoAnalytics.usermanagement.update` | 204 |
| [Delete Custom Role](custom-roles/delete-custom-role.md) | DELETE | `/restapi/v2/orgs/roles/{role-id}` | `deleteCustomRole` | `ZohoAnalytics.usermanagement.delete` | 204 |
| [Get Workspace Users](workspace-users/get-workspace-users.md) | GET | `/restapi/v2/workspaces/{workspace-id}/users` | `getWorkspaceUsers` | `ZohoAnalytics.usermanagement.read` | 200 |
| [Add Workspace Users](workspace-users/add-workspace-users.md) | POST | `/restapi/v2/workspaces/{workspace-id}/users` | `addWorkspaceUsers` | `ZohoAnalytics.usermanagement.create` | 204 |
| [Remove Workspace Users](workspace-users/delete-workspace-users.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/users` | `deleteWorkspaceUsers` | `ZohoAnalytics.usermanagement.delete` | 204 |
| [Change Workspace Users Status](workspace-users/change-workspace-users-status.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/users/status` | `changeWorkspaceUsersStatus` | `ZohoAnalytics.usermanagement.update` | 204 |
| [Change Workspace Users Role](workspace-users/change-workspace-users-role.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/users/role` | `changeWorkspaceUsersRole` | `ZohoAnalytics.usermanagement.update` | 204 |
| [Get Workspace Admins](workspace-users/get-workspace-admins.md) | GET | `/restapi/v2/workspaces/{workspace-id}/admins` | `getWorkspaceAdmins` | `ZohoAnalytics.share.read` | 200 |
| [Add Workspace Admins](workspace-users/add-workspace-admins.md) | POST | `/restapi/v2/workspaces/{workspace-id}/admins` | `addWorkspaceAdmins` | `ZohoAnalytics.share.create` | 204 |
| [Remove Workspace Admins](workspace-users/remove-workspace-admins.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/admins` | `removeWorkspaceAdmins` | `ZohoAnalytics.share.delete` | 204 |
| [Get Group List](workspace-groups/get-groups.md) | GET | `/restapi/v2/workspaces/{workspace-id}/groups` | `getGroups` | `ZohoAnalytics.share.read` | 200 |
| [Create Group](workspace-groups/create-group.md) | POST | `/restapi/v2/workspaces/{workspace-id}/groups` | `createGroup` | `ZohoAnalytics.share.create` | 200 |
| [Rename Group](workspace-groups/rename-group.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}` | `renameGroup` | `ZohoAnalytics.share.update` | 204 |
| [Add Group Members](workspace-groups/add-group-members.md) | POST | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members` | `addGroupMembers` | `ZohoAnalytics.share.create` | 204 |
| [Remove Group Members](workspace-groups/remove-group-members.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members` | `removeGroupMembers` | `ZohoAnalytics.share.delete` | 204 |
| [Delete Group](workspace-groups/delete-group.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}` | `deleteGroup` | `ZohoAnalytics.share.delete` | 204 |
| [Get Group Details](workspace-groups/get-group-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}` | `getGroupDetails` | `ZohoAnalytics.share.read` | 200 |

# Related

- [All domains](../index.md)
- [OpenAPI specification for this domain](../../references/openapi/user-groups-grouped-api.json)
- [Foundations](../../foundations/index.md)
