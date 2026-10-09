---
type: API Group
title: View Operations
description: "APIs for creating, copying, renaming, deleting, and retrieving views."
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - view-operations
  - api-group
api:
  domain: views-management
  group: view-operations
  endpoint_count: 10
  endpoints:
    - operation_id: saveAsView
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/saveas"
      doc: "/domains/views-management/view-operations/save-as-view.md"
    - operation_id: copyViews
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/views/copy"
      doc: "/domains/views-management/view-operations/copy-views.md"
    - operation_id: createSimilarViews
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/similarviews"
      doc: "/domains/views-management/view-operations/create-similar-views.md"
    - operation_id: renameView
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}"
      doc: "/domains/views-management/view-operations/rename-view.md"
    - operation_id: deleteView
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}"
      doc: "/domains/views-management/view-operations/delete-view.md"
    - operation_id: getViews
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/views"
      doc: "/domains/views-management/view-operations/get-views.md"
    - operation_id: getViewDetails
      method: GET
      path: "/restapi/v2/views/{view-id}"
      doc: "/domains/views-management/view-operations/get-view-details.md"
    - operation_id: getViewUrl
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish"
      doc: "/domains/views-management/view-operations/get-view-url.md"
    - operation_id: getViewDependents
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/dependents"
      doc: "/domains/views-management/view-operations/get-view-dependents.md"
    - operation_id: getRecentViews
      method: GET
      path: "/restapi/v2/recentviews"
      doc: "/domains/views-management/view-operations/get-recent-views.md"
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

This document covers V2 REST APIs for managing views within workspaces in Zoho Analytics: creating copies, renaming, deleting, and listing views.

> **Notes that apply to every API in this document:**
> - All requests require OAuth authentication via `Authorization: Zoho-oauthtoken <token>`.
> - `ZANALYTICS-ORGID` is required where noted. See API-specific notes for which org it represents.
> - `ZohoAnalytics_Server_URI` is data-centre dependent (`analyticsapi.zoho.com`, `.eu`, `.in`, etc.).
> - API IDs are for internal use only and are not exposed here.

---

APIs for creating, copying, renaming, deleting, and retrieving views.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Save As View](save-as-view.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/saveas` | `saveAsView` | `ZohoAnalytics.modeling.create` | 200 |
| [Copy Views](copy-views.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/copy` | `copyViews` | `ZohoAnalytics.modeling.create` | 200 |
| [Create Similar Views](create-similar-views.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/similarviews` | `createSimilarViews` | `ZohoAnalytics.modeling.create` | 204 |
| [Rename View](rename-view.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}` | `renameView` | `ZohoAnalytics.modeling.update` | 204 |
| [Delete View](delete-view.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}` | `deleteView` | `ZohoAnalytics.modeling.delete` | 204 |
| [Get View List](get-views.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views` | `getViews` | `ZohoAnalytics.metadata.read` | 200 |
| [Get View Details](get-view-details.md) | GET | `/restapi/v2/views/{view-id}` | `getViewDetails` | `ZohoAnalytics.metadata.read` | 200 |
| [Get View URL](get-view-url.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish` | `getViewUrl` | `ZohoAnalytics.embed.read` | 200 |
| [Get View Dependents](get-view-dependents.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/dependents` | `getViewDependents` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Recent Views](get-recent-views.md) | GET | `/restapi/v2/recentviews` | `getRecentViews` | `ZohoAnalytics.metadata.read` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# Operational Notes and Failure Cases

## Save As View

| Scenario | Behaviour |
|----------|-----------|
| `viewName` conflicts with an existing view name in the workspace | Request fails immediately with error **7111** before any copy is started. |
| `folderId` refers to a folder in a different workspace | Request fails with error **7144** — folder must be in the same workspace as the view being copied. |
| `copyWithLookup=true` and the referenced table no longer exists | Lookup definitions are silently dropped for missing references. The copy still succeeds. |
| `copyHugeData=true` without `copyWithData=true` | `copyHugeData` has no effect. The copy is synchronous with schema only. |
| `copyWithData=true`, `copyHugeData=false` on a very large table | The HTTP request may time out before the data copy completes. Use `copyHugeData=true` for large datasets. |
| Analysis view whose parent table is deleted or inaccessible | Request fails with a permission/not-found error — the parent table must be accessible for the user to save a copy. |
| Dashboard view ID passed as `<view-id>` | Dashboards are not supported by Save As Views. The request may succeed (returning a new view ID) but the result is a copy of the dashboard definition only; card bindings may be broken if referenced views are not also copied. Consider using Copy Views for full dashboard duplication. |

## Copy Views

| Scenario | Behaviour |
|----------|-----------|
| Source and destination workspaces are the same | Allowed. View names may conflict; error **7111** will occur if a view with the same name already exists in the destination. |
| `viewIds` contains a mix of valid and invalid IDs | The security validation phase fails on the first invalid ID (error **7104** or **7319**); no views are copied. |
| `copyWithDependentViews=true` resolves a very large dependency tree | All resolved views are included in the transaction. For very deep dependency chains, the operation may take time. |
| `continueOnFailure=true` and all views fail | HTTP 200 is returned but `data.views` is an empty array. No error is raised. |
| Cross-org copy with incorrect `workspaceKey` | Fails with error **15007**. The workspace key must exactly match the source workspace's copy key; there is no partial match. |
| `destWorkspaceId` belongs to a different org than the resolved destination org | Validation fails; the destination workspace must belong to the destination org resolved from `ZANALYTICS-ORGID` (or `ZANALYTICS-DEST-ORGID` when supplied). |
| Org Admin cross-org copy using `ZANALYTICS-DEST-ORGID` | Set `ZANALYTICS-ORGID` to the caller's own (source) org and `ZANALYTICS-DEST-ORGID` to the destination org. The system validates the caller is a member of the destination org. `workspaceKey` is still required because the destination org differs from the source workspace's org. |
| `ZANALYTICS-DEST-ORGID` refers to a non-existent org | Fails with error **8058** before any copy begins. |
| Caller is not a member of the org specified in `ZANALYTICS-DEST-ORGID` | Fails with error **7301** — "not authorised to do this operation." |
| Destination workspace is full (row/view limits reached) | Copy proceeds up to the limit; remaining views fail. With `continueOnFailure=true`, partial copies are committed. |

## Create Similar Views

| Scenario | Behaviour |
|----------|-----------|
| Reference table has no analysis views | Operation succeeds (HTTP 204) with no views created. |
| Target and reference table are the same view ID | Allowed by the API. Results in duplicate views in the specified folder, since views from the reference are cloned for the same table. |
| Target table column names do not match reference table columns | Column remapping fails for unmatched axes. The similar views are still created but affected axis slots will be empty. Charts may render without data or with errors until the axis bindings are manually corrected. |
| `copyCustomFormula=true` but formula expressions reference columns absent on the target table | Formula columns are created on the target views, but they will be in an error state at render time until the expressions are manually updated to reference valid target columns. |
| `folderId` is a folder that belongs to a nested sub-folder | Supported. All similar views are placed directly into the specified folder regardless of its nesting level. |
| `referenceViewId` is an analysis view (not a table) | The intent is for both `<view-id>` and `referenceViewId` to be base tables. Passing a non-table view as `referenceViewId` may result in unexpected behaviour, as the operation is designed for table-to-table view replication. |

## Rename View

| Scenario | Behaviour |
|----------|-----------|
| `viewDesc` is omitted | The view's existing description is **cleared to empty string** — it is not preserved. Always pass the current description if you do not intend to change it. |
| `viewName` is an empty string | Request fails with error **7413** (view name cannot be empty). |
| Renaming to the same name the view already has | Request succeeds if the name uniqueness check passes (the view itself is excluded from the duplicate check). |
| Renaming a view that is embedded in a dashboard | The rename propagates to all dashboard card references. Dashboard cards reflect the new name immediately without requiring a dashboard update. |
| Renaming a QueryTable | The rename applies to the virtual table. Any analysis views built on the query table are not automatically renamed. |

## Delete View

| Scenario | Behaviour |
|----------|-----------|
| `deleteDependentViews=false` (default) and view has dependents | Request fails with a dependency error. The view is not deleted. Use **[Get View Dependents](get-view-dependents.md)** to enumerate all dependents before attempting deletion. |
| `deleteDependentViews=true` | All direct and transitive dependents are deleted along with the target view. For a table with 50 analysis views, all 50 are deleted. For an analysis view embedded in dashboards, those dashboards are also deleted. Review all dependents via **Get View Dependents** before proceeding. |
| Deleting a Dashboard Tab | Deleting an individual tab (`viewType: "Tab"`) removes that tab and all views it contains from the parent tabbed dashboard. If it is the last remaining tab, the parent tabbed dashboard itself may be affected. |
| Deleting a Tabbed Dashboard | Deletes the parent tabbed dashboard object. All constituent tabs are deleted as dependents. Set `deleteDependentViews=true` to include tabs in the same operation. |
| Soft-delete behaviour | Deleted views are moved to Trash. They can be restored using the Restore Trash View API within the retention period. After the retention period, they are permanently purged. |
| Deleting a table that is a lookup source for another table | If the source table is deleted, lookup columns in tables that reference it will be orphaned. Set `deleteDependentViews=true` to handle this, or remove the lookup relationship first. |

## Get View List

| Scenario | Behaviour |
|----------|-----------|
| `viewTypes` filter excludes all view types the user has access to | Returns an empty `views` array with HTTP 200. No error is raised. |
| `keyword` matches no view names | Returns an empty `views` array with HTTP 200. |
| `startIndex` is beyond the total result count | Returns an empty `views` array with HTTP 200. |
| Shared User requests the list | Only views explicitly shared with that user are returned. The `sharedBy` field indicates who shared each view. Views not shared with the user are not listed. |
| Group Member requests the list | Views shared with the group the user belongs to are included. `sharedBy` shows the sharing user. |
| `criteriaZuid` is the ZUID of a user who has no views in the workspace | Returns an empty `views` array with HTTP 200. |
| `sortedColumn=1` (created time) with `sortedOrder=1` | Returns views from newest created to oldest created. |
| Workspace contains Dashboard Tabs (`viewType=9`) | Tabs are returned separately from their parent Tabbed Dashboard when `viewTypes` includes `9`. Each tab has `parentViewId` set to the parent dashboard's ID. To get only the dashboard entries (not individual tabs), use `viewTypes=[7]`. |

## Get View Details

| Scenario | Behaviour |
|----------|-----------|
| `withInvolvedMetaInfo=false` (default) on a Tabbed Dashboard | Only the base fields are returned — `isTabbedDashboard: true` is present but `tabs` is absent. To get tab structure, request with `withInvolvedMetaInfo=true`. |
| `withInvolvedMetaInfo=true` called by a non-admin (Shared User / Group Member) | Workspace Admin-restricted fields (`rowCount`, `involvedViews`, `tabs`) are returned as `null`. `columns` is still returned for views the user has access to. |
| Getting details of a Dashboard Tab via its `viewId` | Returns the tab's basic info including `parentViewId` pointing to the parent Tabbed Dashboard. Does not return the tab's contained views unless `withInvolvedMetaInfo=true` and the user is a Workspace Admin. |
| View is a Live Connect table | `isLive: true` is included in the response. `rowCount` returns `0` for live tables regardless of actual remote data volume. |
| View is a Tabbed Dashboard but user is non-admin with `withInvolvedMetaInfo=true` | `isTabbedDashboard: true` is present, but `tabs` is `null` (admin-only). |

## Get View URL

| Scenario | Behaviour |
|----------|-----------|
| `criteria` contains a column name that does not exist in the view | Request fails with a filter criteria validation error before generating the URL. Always validate column names against the view's current schema. |
| `domainName` specified but custom domain not yet configured | Request fails with error **8060** (domain does not exist). Configure the custom domain in workspace settings first. |
| `withCustomDomain=true` but no custom domain is configured | Request fails with error **8062**. Remove `withCustomDomain` or use the standard domain. |
| `legendPosition` applied to a table or dashboard | The parameter is silently ignored for non-chart view types. Only Analysis Views (charts) honour `legendPosition`. |
| `includeSearchBox`, `includeDatatypeSymbol`, or `includeShowHideOption` applied to a chart view | These parameters are silently ignored for non-table view types. They only apply to Tables and Tabular Views (Reports). |
| View has a private key configured | The generated URL includes the private key in the path: `.../open-view/<viewId>/<privateKey>?...`. Accessing the URL without the key will fail. This is the intended secure sharing behaviour. |
| Tabbed Dashboard view ID passed as `<view-id>` | A URL is generated for the tabbed dashboard as a whole. All CONFIG display parameters (toolbar, title, theme) apply to the dashboard frame. Individual tab configuration is not exposed through this API. |

## Get View Dependents

| Scenario | Behaviour |
|----------|-----------|
| View has no dependents (standalone table, dashboard, standalone chart) | Returns HTTP 200 with an empty `views` array. No error is raised. |
| Dashboard is passed as `<view-id>` | Dashboards are leaf nodes in the dependency graph — they have no downstream dependents. Returns an empty `views` array. |
| Analysis view (chart) is passed as `<view-id>` | Returns any dashboards that embed this chart. Analysis views themselves cannot be the parent of other views. |
| Table with deeply nested dependent chain (table → QT → chart → dashboard) | All views in the full transitive chain are returned, not just direct dependents. The result is the complete set of views that would break if the source view were deleted. |
| Dashboard Tabs in a Tabbed Dashboard | Dashboard Tabs are **excluded** from the dependent list. The parent Tabbed Dashboard object is included instead. Use **Get View Details** (`withInvolvedMetaInfo=true`) to inspect the contents of individual tabs. |
| Query table that is both a parent (references other tables) and a child (referenced by analysis views) | Get View Dependents returns **downstream** views only — those that depend on the QT. It does not list the tables the QT itself depends on (use Get View Details for that). |
| `<view-id>` belongs to the Trash | Only active (non-trashed) views are returned as dependents. Views that have been moved to Trash are not included. |

## Get Recent Views

| Scenario | Behaviour |
|----------|-----------|
| User has never accessed any views | Returns HTTP 200 with an empty `views` array. |
| Views from multiple workspaces and organisations | All recent views across all the user's accessible workspaces are returned together in a single list, ordered by access time. The `workspaceId` and `workspaceName` fields distinguish the workspace for each view. |
| A recently accessed view was subsequently deleted | Deleted views are not included in recent views. Only currently active views are returned. |
| Shared User or Group Member | Only views the user currently has access to appear in the result. If a view was later unshared, it is removed from the recent list. |
| Calling with different OAuth tokens (different users) | Returns each user's own individual recent view history. The API is strictly per-user. |

---

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | METADBOBJECTNAMEDUPLICATED — An object with this tableName already exists. |
| [7144](../../../foundations/error-codes.md#error-7144) | 400 | The specified folder does not exist. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7413](../../../foundations/error-codes.md#error-7413) | 400 | TABLENAME is missing or null. |
| [8058](../../../foundations/error-codes.md#error-8058) | 400 | The organisation ID provided in ZANALYTICS-DEST-ORGID does not exist. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | The specified domainName does not exist. |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | The specified domainName does not belong to the org's Account Admin. |
| [8062](../../../foundations/error-codes.md#error-8062) | 400 | ADDROWREQUESTSTILLINPROGRESS — Another row-write request for this table is still being processed. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | INVALIDVALUEFORATTRIBUTE — fileType, onError, delimiter, quoted, thousandSeparator, or decimalSeparator is outside its permitted set. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |
| [15007](../../../foundations/error-codes.md#error-15007) | 400 | The copy operation is not allowed — the destination workspace's organisation does not match the caller's organisation, and no valid workspaceKey was supplied (or it does not match). |

# Related

- [Views Management](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
