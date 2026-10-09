---
type: Playbook
title: Share views with users or groups, with row and column restrictions
description: Grant a permission set on one or more views to users or a group, optionally limiting rows with criteria and columns with column lists, then inspect, update or revoke the share.
tags:
  - zoho-analytics
  - rest-api-v2
  - workflow
  - playbook
  - sharing
  - permissions
  - row-level-security
sources:
  - id: markdown-docs
    resource: /domains/index.md
    title: API domain and group overviews in this bundle
generated:
  at: {{NOW}}
status: stable
---

# Goal

Give specific people access to specific views with exactly the permissions they need, and keep the share auditable.

# Prerequisites

- Token scope `ZohoAnalytics.share.create` (share), `.read` (inspect), `.update`, `.delete`.
- Share permission on every view, or Workspace/Organization/Account Admin.
- `workspaceId`, the `viewIds`, and either recipient `emailIds` (organization members, `7535` otherwise) or `groupIds` from [Get Group List](/domains/users-and-groups/workspace-groups/get-groups.md).

# Steps

1. **(Optional) Create a group** with [Create Group](/domains/users-and-groups/workspace-groups/create-group.md) and add members with [Add Group Members](/domains/users-and-groups/workspace-groups/add-group-members.md) so future changes are one call.
2. **Share.** [Share Views](/domains/share-and-publish/sharing/share-views.md), `POST /restapi/v2/workspaces/{workspace-id}/share`, form field `CONFIG`:

```json
{
  "viewIds": ["137687000006991601"],
  "groupIds": ["137687000006991700"],
  "permissions": { "read": true, "export": true, "vud": true },
  "criteria": "\"Region\"='East'",
  "columns": [ { "tableName": "SalesTable", "columnNames": ["Region", "Sales"] } ],
  "inviteMail": true
}
```

   Rules: `read` must be `true` (`8074`); `criteria`, `columns`, `vudColumns`, `drillColumns` require exactly one view in `viewIds` (`7541`/`7543`); re-sharing an existing combination fails with `7321`/`7322`, use step 4 instead. Success is HTTP 204 with no body.
3. **Inspect.** [Get Shared Details](/domains/share-and-publish/sharing/get-shared-details-for-views.md) for the views, or [Get Workspace Shared Details](/domains/share-and-publish/sharing/get-workspace-shared-details.md) for the whole workspace. The shared user can check their own rights with [Get My Permissions](/domains/share-and-publish/sharing/get-user-permissions.md).
4. **Change.** [Update Shared Details](/domains/share-and-publish/sharing/update-shared-details-for-view.md) replaces the permission set, criteria or columns of an existing share.
5. **Revoke.** [Remove Shared Views](/domains/share-and-publish/sharing/remove-share.md).

# Notes

- A shared user's export or row API calls are automatically ANDed with the share criteria; they cannot widen their slice.
- For Client Portal users add `domainName` and call from the standard API host (see [White label & Client Portal](/foundations/white-label-client-portal.md)).
- System tags may block the share with `8241`; resend with `"validateSystemTags": false` after review.

# Related

- [Sharing](/domains/share-and-publish/sharing/overview.md)
- [Roles & permissions](/foundations/roles-and-permissions.md)
- [Filter criteria syntax](/foundations/filter-criteria-syntax.md)
