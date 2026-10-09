---
type: API Group
title: Trash Management
description: "APIs to list the views available in the trash of a workspace, restore a trashed view back to the workspace, and permanently delete a view from the trash."
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - trash-management
  - api-group
api:
  domain: views-management
  group: trash-management
  endpoint_count: 3
  endpoints:
    - operation_id: getTrashViews
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/trash"
      doc: "/domains/views-management/trash-management/get-trash-views.md"
    - operation_id: restoreTrashView
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/trash/{view-id}"
      doc: "/domains/views-management/trash-management/restore-trash-view.md"
    - operation_id: deleteTrashView
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/trash/{view-id}"
      doc: "/domains/views-management/trash-management/delete-trash-view.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

This document describes the V2 **Trash View** REST APIs of Zoho Analytics — listing trashed views, restoring them to active state, and permanently deleting them from trash.

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`).
> - All three APIs are **workspace-scoped** and require the `ZANALYTICS-ORGID` header.
> - `ZohoAnalytics_Server_URI` depends on the data center (`analyticsapi.zoho.com`, `.eu`, etc.).

---

APIs to list the views available in the trash of a workspace, restore a trashed view back to the workspace, and permanently delete a view from the trash.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Trash Views](get-trash-views.md) | GET | `/restapi/v2/workspaces/{workspace-id}/trash` | `getTrashViews` | `ZohoAnalytics.metadata.read` | 200 |
| [Restore Trash View](restore-trash-view.md) | POST | `/restapi/v2/workspaces/{workspace-id}/trash/{view-id}` | `restoreTrashView` | `ZohoAnalytics.modeling.create` | 204 |
| [Delete Trash View](delete-trash-view.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/trash/{view-id}` | `deleteTrashView` | `ZohoAnalytics.modeling.delete` | 204 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# Response Payload Notes

| Field | Description |
|-------|-------------|
| `status` | `success` or `failure`. Standard Zoho Analytics V2 response envelope. |
| `summary` | Human-readable description of the operation (`"get trash view list"` for [Get Trash Views](get-trash-views.md)). |
| `data.views` | Array of trashed view objects ([Get Trash Views](get-trash-views.md) only). Empty array `[]` when nothing is in trash. |
| `viewId` | Returned as a **string** despite being a long integer internally. |
| `deletedTime` | Epoch timestamp in **milliseconds** as a string. Divide by 1000 for Unix epoch seconds. |
| `isDisabled` | Only present when `true`. Indicates the view cannot be restored under the current plan (typically Live Connect reports on a plan that no longer supports them). |
| `tabParentId` | Only present for `DashTab` view types. String ID of the parent tabbed dashboard. |
| Restore/Delete responses | [Restore Trash View](restore-trash-view.md) and [Delete Trash View](delete-trash-view.md) return **HTTP 204 No Content** with an empty body on success. |

---

# Understanding Dependent Views in Restore and Delete

## What Are Dependent Views?

In Zoho Analytics, views form **parent–child dependency chains**:

- A **Table** is a parent. Analysis views (charts, pivots, summaries, query tables) built on top of it are its children.
- A **Dashboard** is a parent. Dashboard tabs (`DashTab`) are its children.
- A **Query Table** can itself depend on one or more base tables, and may have child analysis views.

When multiple linked views are all deleted at the same time, they all land in the trash together. The dependency chain is preserved even in trash.

---

## How `withDependents` Affects Restore

When you attempt to restore a view, the system first checks whether any **parent objects** that the view depends on are **also in trash**.

| Scenario | `withDependents=false` (default) | `withDependents=true` |
|----------|----------------------------------|-----------------------|
| View has no parents in trash (standalone) | ✅ Restore succeeds | ✅ Restore succeeds (same result) |
| View depends on a parent table that is also in trash | ❌ Error `7941` — cannot restore without its parent | ✅ Restores the view **and** its parent table (and any related columns, formulas, relations, data connectors) |
| View's parent is already active (not in trash) | ✅ Restore succeeds | ✅ Restore succeeds |

**Example — Restoring a dependent analysis view:**

The `Sales` table and two analysis views (`Region_vs_sales`, `product_Vs_sales`) were all deleted together. The trash list shows all three:

```
Sales          → Table        (parent)
Region_vs_sales → AnalysisView (child of Sales)
product_Vs_sales → AnalysisView (child of Sales)
```

**Option A — Restore `Sales` first, then restore the views separately:**

```http
POST /trash/7617000032567465   (Sales table)   ← no CONFIG needed, standalone
POST /trash/7617000032567466   (Region_vs_sales) ← withDependents=false now works
POST /trash/7617000032567467   (product_Vs_sales) ← withDependents=false now works
```

**Option B — Restore `Region_vs_sales` directly with dependencies:**

```http
POST /trash/7617000032567466
CONFIG={"withDependents":true}
```

This also restores `Sales` (the parent table) automatically, along with any related formulas and relations. Both analysis views are still in trash and must be restored separately or via a workspace-level bulk operation.

> **Tip:** When restoring multiple views deleted in a batch, always restore the parent tables first (with `withDependents=false`), then restore the child views. This avoids accidental cascading restores.

---

## How `withDependents` Affects Permanent Delete

When you attempt to permanently delete a view from trash, the system checks whether any **child dependent views** are **also in trash** and depend exclusively on this view.

| Scenario | `withDependents=false` (default) | `withDependents=true` |
|----------|----------------------------------|-----------------------|
| View has no children in trash | ✅ Delete succeeds | ✅ Delete succeeds |
| View has child analysis views / reports in trash that depend on it | ❌ Error `7942` — cannot delete parent while children are in trash | ✅ Permanently deletes the view **and all its child dependents** in trash (formulas, relations, dependent reports) |
| View is an analysis view (no children) | ✅ Delete succeeds | ✅ Delete succeeds |

**Example — Permanently deleting a table and its analysis views:**

```
Sales          → Table        (7617000032567465)
Region_vs_sales → AnalysisView (7617000032567466, child of Sales)
product_Vs_sales → AnalysisView (7617000032567467, child of Sales)
```

- `DELETE /trash/7617000032567466` (Region_vs_sales) → ✅ succeeds (leaf node, no children)
- `DELETE /trash/7617000032567465` (Sales) — with dependents still in trash → ❌ error [`7942`](../../../foundations/error-codes.md#error-7942)
- `DELETE /trash/7617000032567465` with `CONFIG={"withDependents":true}` → ✅ permanently deletes Sales AND product_Vs_sales together

> ⚠️ `withDependents=true` on Delete is **irreversible**. All deleted views, their columns, formulas, and relations are permanently removed and cannot be recovered.

---

## Special Cases

| Case | Behaviour |
|------|-----------|
| **`isDisabled: true` in trash list** | The view is a Live Connect report and the current plan does not support Live Connect. It appears in the trash list but restore will fail. Upgrade the plan or permanently delete the view. |
| **DashTab type views** | Dashboard tabs (`DashTab`) are children of a tabbed dashboard. To restore a tab, the parent dashboard must also be active (not in trash). If the parent is in trash, restore the parent dashboard first, or use `withDependents=true` on the tab. |
| **View already restored (error 7929)** | If another user or process restored the same view concurrently, the view is no longer in trash. Verify with Get Trash Views — the view will be absent from the list. |
| **Deleting a `DashTab`** | Deleting a tab from trash does not affect the parent dashboard (if the parent is active). |
| **Restoring a view whose folder was also deleted** | If the original folder containing the view was deleted, the view is restored to the workspace root folder. The folder does not need to be restored first. |
| **Partial restore with `withDependents=true`** | The `withDependents=true` flag on Restore brings back the immediate parent chain (parent table, its columns, formulas, relations, connectors). Sibling views that also depended on the same parent are **not** automatically restored — only the specified view and its required ancestors. |
| **Bulk deletion order** | When deleting multiple views manually (multiple DELETE calls), delete leaf views (analysis views, pivots) before parent tables. This avoids triggering error `7942` unexpectedly. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7082](../../../foundations/error-codes.md#error-7082) | 400 | An unexpected error occurred during the trash restore operation. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7929](../../../foundations/error-codes.md#error-7929) | 400 | The view has already been restored from trash. |
| [7941](../../../foundations/error-codes.md#error-7941) | 400 | The view has parent dependencies that are also in trash and must be restored together. |
| [7942](../../../foundations/error-codes.md#error-7942) | 400 | The view has child dependent views in trash that must be deleted together. |
| [7943](../../../foundations/error-codes.md#error-7943) | 400 | The requesting user does not have permission to restore this specific trashed view. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |

# Related

- [Views Management](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
