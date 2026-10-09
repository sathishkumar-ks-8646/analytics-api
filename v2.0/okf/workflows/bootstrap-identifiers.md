---
type: Playbook
title: "Bootstrap: from access token to workspace and view IDs"
description: The first three calls of every integration - list organizations, pick the org ID for the header, and resolve workspace and view names into the IDs that all other endpoints need.
tags:
  - zoho-analytics
  - rest-api-v2
  - workflow
  - playbook
  - bootstrap
  - identifiers
sources:
  - id: markdown-docs
    resource: /domains/index.md
    title: API domain and group overviews in this bundle
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Goal

Turn human-readable names into the `ZANALYTICS-ORGID` header value, `workspaceId` and `viewId` without hard-coding any identifier.

# Prerequisites

- An access token with `ZohoAnalytics.metadata.read` (see [Authentication](../foundations/authentication.md)).
- The API host of your data center (see [Data centers](../foundations/data-centers.md)).

# Steps

1. **List organizations.** Call [Get Org List](../domains/organization-management/org-info-and-settings/get-organizations.md) (`GET /restapi/v2/orgs`, no organization header). Pick the entry whose `orgName` matches, or the one with `isDefault: true`. Keep `orgId`.
2. **Resolve the workspace.** Call [Get Meta Details From Name](../domains/organization-management/org-info-and-settings/get-meta-details.md) with `ZANALYTICS-ORGID: <orgId>` and `CONFIG={"workspaceName":"Sales Analytics"}`. Names are exact and case-sensitive. Keep `data.workspaces.workspaceId`.
3. **Resolve the view.** Repeat step 2 adding `"viewName":"Revenue Trend"`; keep `data.views.viewId` and `data.views.viewType`. Alternatively list all views with [Get View List](../domains/views-management/view-operations/get-views.md) and pick by name and type.
4. **Resolve deeper IDs as needed.** Columns: [Get Table Metadata](../domains/data-modeling-and-schema/table-and-schema/get-table-metadata.md). Folders: [Get Folder List](../domains/workspace-management/workspace-folders/get-folders.md). Groups: [Get Group List](../domains/users-and-groups/workspace-groups/get-groups.md). See [Identifiers](../foundations/identifiers.md) for the full map.

# Failure Handling

| Code | Meaning | Action |
|---|---|---|
| `8535` | Token invalid or wrong scope | Refresh the token with `ZohoAnalytics.metadata.read`. |
| `7104` | Workspace or view name not found in this organization | Check spelling and case; check the organization header. |
| `7301` | Caller has no view shared in that workspace | Ask for a share or an admin role. |

# Related

- [Identifiers](../foundations/identifiers.md)
- [Request conventions](../foundations/request-conventions.md)
