---
type: API Group
title: Workspace Folders
description: "APIs that manage the folders of a workspace, covering the creation, renaming, deletion, nesting and reordering of folders, the movement of views between folders, and the selection of the default folder."
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-folders
  - api-group
api:
  domain: workspace-management
  group: workspace-folders
  endpoint_count: 8
  endpoints:
    - operation_id: getFolders
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/folders"
      doc: "/domains/workspace-management/workspace-folders/get-folders.md"
    - operation_id: createFolder
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/folders"
      doc: "/domains/workspace-management/workspace-folders/create-folder.md"
    - operation_id: renameFolder
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}"
      doc: "/domains/workspace-management/workspace-folders/rename-folder.md"
    - operation_id: deleteFolder
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}"
      doc: "/domains/workspace-management/workspace-folders/delete-folder.md"
    - operation_id: changeFolderHierarchy
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/move"
      doc: "/domains/workspace-management/workspace-folders/change-folder-hierarchy.md"
    - operation_id: changeFolderPosition
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/reorder"
      doc: "/domains/workspace-management/workspace-folders/change-folder-position.md"
    - operation_id: moveViewsToFolder
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/views/movetofolder"
      doc: "/domains/workspace-management/workspace-folders/move-views-to-folder.md"
    - operation_id: makeDefaultFolder
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/default"
      doc: "/domains/workspace-management/workspace-folders/make-default-folder.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Folders provide a hierarchical organization layer within a workspace. Views (tables, reports, dashboards) can be placed inside folders to help users navigate large workspaces. Folders can be nested up to one level deep — a top-level folder can have sub-folders, but sub-folders cannot have children of their own.

> **Default Folder:** Every workspace has a single default folder. The default folder is where new views are placed when no explicit folder is selected. You can change which folder is the default at any time, but there can only be one default folder per workspace.

> **Folder Visibility for Shared Users:** Workspace Admins see all folders. Shared users and group members see only the folders that contain at least one view they have been granted access to. Parent folders of accessible sub-folders are also included.

> **White Label / Client Portal:** All folder management APIs are available via portal domain URLs. White label portal users can create and manage folders if they have been granted the Create Folder permission on the workspace.

---

APIs that manage the folders of a workspace, covering the creation, renaming, deletion, nesting and reordering of folders, the movement of views between folders, and the selection of the default folder. Folders provide a hierarchical organization layer within a workspace and support exactly one level of nesting.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Folder List](get-folders.md) | GET | `/restapi/v2/workspaces/{workspace-id}/folders` | `getFolders` | `ZohoAnalytics.metadata.read` | 200 |
| [Create Folder](create-folder.md) | POST | `/restapi/v2/workspaces/{workspace-id}/folders` | `createFolder` | `ZohoAnalytics.modeling.create` | 200 |
| [Rename Folder](rename-folder.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}` | `renameFolder` | `ZohoAnalytics.modeling.update` | 204 |
| [Delete Folder](delete-folder.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}` | `deleteFolder` | `ZohoAnalytics.modeling.delete` | 204 |
| [Change Folder Hierarchy](change-folder-hierarchy.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/move` | `changeFolderHierarchy` | `ZohoAnalytics.modeling.update` | 204 |
| [Change Folder Position](change-folder-position.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/reorder` | `changeFolderPosition` | `ZohoAnalytics.modeling.update` | 204 |
| [Move Views To Folder](move-views-to-folder.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/movetofolder` | `moveViewsToFolder` | `ZohoAnalytics.modeling.update` | 204 |
| [Make Default Folder](make-default-folder.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/default` | `makeDefaultFolder` | `ZohoAnalytics.modeling.update` | 204 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# API-Specific Notes and Behaviours

This appendix consolidates key behaviours, edge cases, and inter-API dependency information for each Workspace Folders API.

## Get Folder List

- **Primary source of IDs:** This is the entry point for all other folder APIs. `folderId` values obtained here are used as `<folder-id>` in the URL for every other folder operation, and as `parentFolderId` (Create Folder / Change Folder Hierarchy), `referenceFolderId` (Change Folder Position), and `folderId` (Move Views To Folder).
- **Shared-user filtering:** Shared Users and Group Members receive a filtered list. If a view is inside a sub-folder and that view is accessible to the user, both the sub-folder and its parent are included. An empty `folders` array means the user has access to no views in the workspace.
- **`parentFolderId: "-1"`** indicates a root-level folder (no parent). The value is always returned as a string.

## Create Folder

- **Response gap:** Only `folderId` is returned in the response. To retrieve the full folder record (name, description, index, isDefault), call Get Folder List after creation.
- **`makeDefaultFolder=true`:** Equivalent to calling Make Default Folder immediately after creation. The previous default folder loses its status.
- **Nesting rule:** Only one level of sub-folders is supported. `parentFolderId` must reference a root-level folder.
- **Dependency:** `parentFolderId` (when creating a sub-folder) → Get Folder List.

## Rename Folder

- **`folderDesc` reset behaviour (critical):** Omitting `folderDesc` permanently clears the existing description to an empty string. Always read the current `folderDesc` from Get Folder List before calling this API if you want to preserve it.
- **Dependency:** `<folder-id>` → Get Folder List. Current `folderDesc` value → Get Folder List.

## Delete Folder

- **Views survive by default:** With `deleteDependentViews=false` (the default), views inside the deleted folder are moved to the workspace root — they are not lost.
- **Error 7277 guard:** If any table inside the folder has dependent child views (reports/dashboards built on top of it), deletion is blocked unless `deleteDependentViews=true`.
- **Dependency:** `<folder-id>` → Get Folder List.

## Change Folder Hierarchy

- **`hierarchy` values are strict:** `0` = promote sub-folder to root; `1` = nest under a parent. Any other value immediately returns error 8119.
- **`parentFolderId` must be root-level:** You cannot chain nesting — the target parent must itself be a top-level folder.
- **Dependency:** `<folder-id>` and `parentFolderId` (when `hierarchy=1`) → Get Folder List.

## Change Folder Position

- **Position result:** The target folder is placed immediately above `referenceFolderId`. Use Get Folder List to verify `folderIndex` values after the call.
- **Same-level constraint:** Both folders must be at the same hierarchy level (both root-level, or both sub-folders of the same parent).
- **Dependency:** `<folder-id>` and `referenceFolderId` → Get Folder List.

## Move Views To Folder

- **Atomic operation:** The entire batch succeeds or fails together. A single invalid `viewId` (error 7319) causes zero views to be moved.
- **Dependency:** `folderId` → Get Folder List. `viewIds` → Get View List API for the workspace.

## Make Default Folder

- **Idempotent:** Safe to call even if the folder is already the default — no error is returned.
- **One default at a time:** The workspace always has exactly one default folder; the previous default loses its status immediately upon this call.
- **Dependency:** `<folder-id>` → Get Folder List.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **`parentFolderId` type** | Always returned as a string (e.g. `"-1"`, `"7617000071955001"`), not a numeric. `"-1"` means root level. |
| **`folderIndex` meaning** | Sort order within the folder's hierarchy level. The default folder uses `-1`. Non-default folders are sorted in ascending order of `folderIndex`. |
| **`isDefault` uniqueness** | Exactly one folder per workspace has `isDefault: true` at any given time. |
| **Subfolder nesting limit** | Exactly one level of nesting is supported. A root-level folder can have sub-folders; sub-folders cannot have children. |
| **Create Folder response** | Returns only `folderId`. All other fields (`folderName`, `folderDesc`, `folderIndex`, `isDefault`, `parentFolderId`) are obtained by calling Get Folder List. |
| **Rename Folder `folderDesc` reset** | Omitting `folderDesc` in a Rename request permanently clears the description. This is intentional API behaviour, not a bug. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7140](../../../foundations/error-codes.md#error-7140) | 400 | A folder with the same name already exists in the workspace. |
| [7144](../../../foundations/error-codes.md#error-7144) | 400 | The specified folder does not exist. |
| [7277](../../../foundations/error-codes.md#error-7277) | 400 | The folder holds tables that have dependent child views, so the deletion is blocked. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7414](../../../foundations/error-codes.md#error-7414) | 400 | The folder name cannot be empty. |
| [7496](../../../foundations/error-codes.md#error-7496) | 400 | The maximum sub-folder nesting depth has been exceeded. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | Invalid value for attribute. |

# Related

- [Workspace Management](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
