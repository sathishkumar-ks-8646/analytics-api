---
type: Playbook
title: Add users to an organization and a workspace, and set their roles
description: Invite users to the organization, place them in a workspace with a role, promote or demote admins, deactivate leavers, and understand who may perform each step.
tags:
  - zoho-analytics
  - rest-api-v2
  - workflow
  - playbook
  - users
  - roles
  - administration
sources:
  - id: markdown-docs
    resource: /domains/index.md
    title: API domain and group overviews in this bundle
generated:
  at: {{NOW}}
status: stable
---

# Goal

Provision a new team member end to end: organization membership, organization role, workspace membership, workspace role, and eventually deactivation.

# Prerequisites

- Token scopes from the `usermanagement` family (organization users) and `share` family (workspace users and admins), as listed per endpoint.
- Caller role: Account Admin or Organization Admin for organization-level changes; Workspace Admin suffices to add or remove workspace users, but changing a workspace user's status requires Account Admin and changing their role requires Account Admin or Organization Admin.
- Plan seats available (`users`, `roUsers` in [Get Resource Details](/domains/organization-management/org-info-and-settings/get-resource-details.md)).

# Steps

1. **Add to the organization** with [Add Users](/domains/users-and-groups/org-users/add-users.md) (`emailIds`, optional `role`: `USER`, `VIEWER`, `ORGADMIN`). Verify with [Get Users](/domains/users-and-groups/org-users/get-users.md).
2. **Set the organization role** with [Change User Role](/domains/users-and-groups/org-users/change-user-role.md). `ORGADMIN` cannot be assigned inside a portal domain (`6089`). [Get Org Admins](/domains/users-and-groups/org-users/get-org-admins.md) lists current admins (Account Admin only).
3. **Add to a workspace** with [Add Workspace Users](/domains/users-and-groups/workspace-users/add-workspace-users.md) (`emailIds`, optional role `WORKSPACEADMIN`, `USER` or a custom role name, `7550` if unknown). Alternatively make them a workspace admin with [Add Workspace Admins](/domains/users-and-groups/workspace-users/add-workspace-admins.md).
4. **Give access to views** by sharing directly or through a group: see [Share views](/workflows/share-view-with-row-filter.md).
5. **Change workspace role or status** with [Change Workspace Users Role](/domains/users-and-groups/workspace-users/change-workspace-users-role.md) and [Change Workspace Users Status](/domains/users-and-groups/workspace-users/change-workspace-users-status.md).
6. **Offboard** with [Deactivate Users](/domains/users-and-groups/org-users/de-activate-users.md) (keeps their objects, frees the seat) or [Remove Users](/domains/users-and-groups/org-users/remove-users.md); at workspace level use [Remove Workspace Users](/domains/users-and-groups/workspace-users/delete-workspace-users.md).

Most of these endpoints return HTTP 204 with no body on success.

# Notes

- The organization role is a ceiling: a `VIEWER` stays read-only regardless of workspace shares.
- Email addresses must already be organization members before they can be shared to (`7535`) or added to a workspace (`8114`).

# Related

- [Roles & permissions](/foundations/roles-and-permissions.md)
- [Organization Users](/domains/users-and-groups/org-users/overview.md), [Workspace Users](/domains/users-and-groups/workspace-users/overview.md), [Workspace Groups](/domains/users-and-groups/workspace-groups/overview.md)
