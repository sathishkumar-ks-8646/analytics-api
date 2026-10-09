---
type: API Group
title: Workspace Operations
description: "APIs that manage the lifecycle and the metadata of workspaces, covering the creation, copying, renaming, deletion and inspection of a workspace."
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-operations
  - api-group
api:
  domain: workspace-management
  group: workspace-operations
  endpoint_count: 10
  endpoints:
    - operation_id: createWorkspace
      method: POST
      path: "/restapi/v2/workspaces"
      doc: "/domains/workspace-management/workspace-operations/create-workspace.md"
    - operation_id: copyWorkspace
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}"
      doc: "/domains/workspace-management/workspace-operations/copy-workspace.md"
    - operation_id: renameWorkspace
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}"
      doc: "/domains/workspace-management/workspace-operations/rename-workspace.md"
    - operation_id: deleteWorkspace
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}"
      doc: "/domains/workspace-management/workspace-operations/delete-workspace.md"
    - operation_id: exportAsTemplate
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/template/data"
      doc: "/domains/workspace-management/workspace-operations/export-as-template.md"
    - operation_id: getAllWorkspaces
      method: GET
      path: "/restapi/v2/workspaces"
      doc: "/domains/workspace-management/workspace-operations/get-all-workspaces.md"
    - operation_id: getOwnedWorkspaces
      method: GET
      path: "/restapi/v2/workspaces/owned"
      doc: "/domains/workspace-management/workspace-operations/get-owned-workspaces.md"
    - operation_id: getSharedWorkspaces
      method: GET
      path: "/restapi/v2/workspaces/shared"
      doc: "/domains/workspace-management/workspace-operations/get-shared-workspaces.md"
    - operation_id: getWorkspaceSecretKey
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/secretkey"
      doc: "/domains/workspace-management/workspace-operations/get-workspace-secret-key.md"
    - operation_id: getWorkspaceDetails
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}"
      doc: "/domains/workspace-management/workspace-operations/get-workspace-details.md"
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

These APIs manage the lifecycle and metadata of workspaces — creating, copying, renaming, deleting, and inspecting workspaces. They also provide mechanisms to retrieve workspace access keys for cross-organisation operations, list workspaces accessible to a user, and export a workspace's structure as a reusable template.

> **Workspace:** A workspace is the top-level container in Zoho Analytics that holds tables, reports, dashboards, and sharing configurations. All data and views exist within a workspace.

---

APIs that manage the lifecycle and the metadata of workspaces, covering the creation, copying, renaming, deletion and inspection of a workspace. They also provide the workspace access key used for cross-organization operations, list the workspaces accessible to a user, and export the structure of a workspace as a reusable template.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Create Workspace](create-workspace.md) | POST | `/restapi/v2/workspaces` | `createWorkspace` | `ZohoAnalytics.modeling.create` | 200 |
| [Copy Workspace](copy-workspace.md) | POST | `/restapi/v2/workspaces/{workspace-id}` | `copyWorkspace` | `ZohoAnalytics.modeling.create` | 200 |
| [Rename Workspace](rename-workspace.md) | PUT | `/restapi/v2/workspaces/{workspace-id}` | `renameWorkspace` | `ZohoAnalytics.modeling.update` | 204 |
| [Delete Workspace](delete-workspace.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}` | `deleteWorkspace` | `ZohoAnalytics.modeling.delete` | 204 |
| [Export as Template](export-as-template.md) | GET | `/restapi/v2/workspaces/{workspace-id}/template/data` | `exportAsTemplate` | `ZohoAnalytics.metadata.read` | 200 |
| [Get All Workspace List](get-all-workspaces.md) | GET | `/restapi/v2/workspaces` | `getAllWorkspaces` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Owned Workspace List](get-owned-workspaces.md) | GET | `/restapi/v2/workspaces/owned` | `getOwnedWorkspaces` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Shared Workspace List](get-shared-workspaces.md) | GET | `/restapi/v2/workspaces/shared` | `getSharedWorkspaces` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Workspace Secret Key](get-workspace-secret-key.md) | GET | `/restapi/v2/workspaces/{workspace-id}/secretkey` | `getWorkspaceSecretKey` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Workspace Info](get-workspace-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}` | `getWorkspaceDetails` | `ZohoAnalytics.metadata.read` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# API-Specific Notes and Behaviours

## Workspace Name Constraints

| Rule | Detail |
|------|--------|
| Max length | 50 characters for `workspaceName` / `newWorkspaceName`. Exceeding this is rejected at parameter validation. |
| Uniqueness | Workspace names must be unique within the organisation. Creating or renaming to a duplicate name fails with error **7111**. |
| Description max | 250 characters. Exceeding this is rejected at parameter validation. |
| Description reset | In Rename Workspace, omitting `workspaceDesc` **clears the existing description** to empty string. Always include the current description to preserve it. |

## Create Workspace

| Scenario | Behaviour |
|----------|-----------|
| Plan workspace limit reached | Fails with error **7951**. The limit depends on the organisation's subscription tier. |
| Org Admin calling this API | Allowed — Org Admins can create workspaces within their organisation. |
| Workspace created with no views | The workspace is usable but empty. Tables and views must be added via separate APIs. |

## Copy Workspace

| Scenario | Behaviour |
|----------|-----------|
| Same-org copy without `workspaceKey` | Allowed — `workspaceKey` is only checked for cross-org copies. |
| Account Admin cross-org copy | Set `ZANALYTICS-ORGID` to the destination org ID. Provide `workspaceKey` (source workspace's secret key). The caller must be an Account Admin or Org Admin of the destination org. |
| Org Admin cross-org copy using `ZANALYTICS-DEST-ORGID` | Set `ZANALYTICS-ORGID` to the caller's own (source) org and `ZANALYTICS-DEST-ORGID` to the destination org. The system validates the caller is a member of the destination org. `workspaceKey` is still required because the destination org differs from the source workspace's org. |
| `ZANALYTICS-DEST-ORGID` refers to a non-existent org | Fails with error **8058** before any copy begins. |
| Caller is not a member of the org specified in `ZANALYTICS-DEST-ORGID` | Fails with error **7301** — "not authorised to do this operation." |
| Cross-org copy without `workspaceKey` | Fails with error **8024**. |
| Provided `workspaceKey` does not match source workspace's secret key | Fails with error **8024**. Obtain the correct key from Get Workspace Secret Key. |
| `copyWithData=true` on a large workspace | Operation takes significantly longer. The rate limit (1 concurrent copy per org) means other copy requests will queue or fail while this is in progress. |
| `copyWithImportSource=false` (default) | Tables in the copy will have no import source — data must be re-imported or manually entered. The table schema is preserved. |
| `copyWithImportSource=true` with a live database connection | Live/direct database connections (e.g., Zoho DataPrep live links) cannot be copied by definition — only import-based connections (scheduled syncs, file imports, API-pushed data) are preserved. Live connections require manual reconnection. |
| `newWorkspaceDesc` omitted | The copied workspace has an empty description. The source workspace's description is not automatically copied. |
| Destination org plan limit | Fails with error **7951** if the destination org has reached its workspace limit. |
| Concurrent copy in progress | Only one copy per org runs at a time. A simultaneous request is rejected. |

## Rename Workspace

| Scenario | Behaviour |
|----------|-----------|
| Renaming to the same name | Succeeds (idempotent). |
| Renaming to a name already in use in the org | Fails with error **7111**. |
| `workspaceDesc` omitted from request | Description is permanently cleared to empty string — existing description is lost. Always include `workspaceDesc` if you only intend to change the name. |

## Delete Workspace

| Scenario | Behaviour |
|----------|-----------|
| Workspace has active import jobs | Import jobs are cancelled. The workspace and all its data are deleted. |
| Workspace is shared with users | All sharing configurations are removed. Users who had access to views in this workspace will lose all access immediately. |
| Workspace has Workspace Admins | Their admin role for this workspace is removed when the workspace is deleted. Their org membership is not affected. |
| Deletion is permanent | There is no trash/recycle mechanism for workspaces. Once deleted, the workspace and all its content cannot be recovered. |

## Export as Template

| Scenario | Behaviour |
|----------|-----------|
| `viewIds` is an empty array | Rejected — at least one view ID must be provided. |
| A view ID belongs to a different workspace | Fails with error **7319**. All view IDs must be in the same workspace as specified in the URL. |
| Views with lookup columns | Dependent tables needed to resolve lookups are automatically included in the template. |
| Response format | The response is a binary `.atpt` file, not JSON. Clients must handle the response as a binary stream and save it to disk. |

## Get Workspace Secret Key

| Scenario | Behaviour |
|----------|-----------|
| `regenerateKey=false` (default) | Returns the existing key. If no key has been generated yet, the system generates and returns one. |
| `regenerateKey=true` | Generates a new key. The old key is permanently invalidated. Any cross-org copy that was in progress using the old key is not affected (the key is validated only at copy start), but any future copy attempts using the old key will fail. |
| Who can see the key | Only Account Admins and Org Admins of the workspace's organisation. The key is never returned in workspace listing or info APIs. |

## Get Workspace Info — `withUserRoleInfo`

| Scenario | Behaviour |
|----------|-----------|
| `withUserRoleInfo=false` (default) | Standard metadata only. Fastest response. |
| `withUserRoleInfo=true` — Account Admin caller | `roleName` returns `"Account Admin"`, `roleId` is `0`, `isCustomRoleUser` is `false`. |
| `withUserRoleInfo=true` — Org Admin caller | `roleName` returns `"Organization Admin"`, `roleId` is `0`. |
| `withUserRoleInfo=true` — custom role user | `isCustomRoleUser` is `true`, `roleId` is the custom role's numeric ID, `roleName` is the custom role's display name. |
| `withUserRoleInfo=true` — shared user (no workspace role) | `roleName` may reflect their view-level access role. Behaviour depends on their permission level. |

## Workspace List API Comparison

| API | Returns | Who can call | ZANALYTICS-ORGID |
|-----|---------|--------------|------------------|
| Get All Workspace List | Owned + shared workspaces for the caller | Any user | Not required |
| Get Owned Workspace List | All workspaces in the caller's org | Account Admin only | Not required |
| Get Shared Workspace List | Workspaces from other orgs shared with the caller | Any user | Not required |
| Get Workspace Info | Single workspace details | Workspace Admin, shared user, or any user with view access | Not required |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | A view with the given viewName already exists in this workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7951](../../../foundations/error-codes.md#error-7951) | 400 | The organization has reached its workspace creation limit based on the current subscription plan. |
| [8024](../../../foundations/error-codes.md#error-8024) | 400 | A cross-organization copy was attempted without a valid workspaceKey, or the key provided does not match the secret key of the source workspace. |
| [8058](../../../foundations/error-codes.md#error-8058) | 400 | The organization ID provided in the ZANALYTICS-DEST-ORGID header does not exist. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |

# Related

- [Workspace Management](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
