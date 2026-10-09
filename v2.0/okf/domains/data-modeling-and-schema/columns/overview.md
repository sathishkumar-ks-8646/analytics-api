---
type: API Group
title: Columns
description: "APIs for adding, renaming, reordering, showing, hiding, deleting, and sorting columns."
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - columns
  - api-group
api:
  domain: data-modeling-and-schema
  group: columns
  endpoint_count: 8
  endpoints:
    - operation_id: addColumn
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns"
      doc: "/domains/data-modeling-and-schema/columns/add-column.md"
    - operation_id: renameColumn
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}"
      doc: "/domains/data-modeling-and-schema/columns/rename-column.md"
    - operation_id: deleteColumn
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}"
      doc: "/domains/data-modeling-and-schema/columns/delete-column.md"
    - operation_id: hideColumns
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/hide"
      doc: "/domains/data-modeling-and-schema/columns/hide-columns.md"
    - operation_id: showColumns
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/show"
      doc: "/domains/data-modeling-and-schema/columns/show-columns.md"
    - operation_id: getColumnDependents
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/dependents"
      doc: "/domains/data-modeling-and-schema/columns/get-column-dependents.md"
    - operation_id: sortDataByColumns
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data/sort"
      doc: "/domains/data-modeling-and-schema/columns/sort-data-by-columns.md"
    - operation_id: reorderColumns
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/reorder"
      doc: "/domains/data-modeling-and-schema/columns/reorder-columns.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

This document covers the APIs for managing columns in a Zoho Analytics table — adding, renaming, deleting, showing/hiding, sorting, and inspecting column dependencies.

> **Tables only:** Add Column, Rename Column, Delete Column, Hide/Show Columns, and Get Column Dependents operate exclusively on *tables*. Calling these APIs with the view ID of a report, chart, or dashboard returns an error.

> **DDL Lock:** Add Column, Rename Column, and Delete Column check for a DDL lock before proceeding. If a data import or schema operation is already in progress on the table, the request is rejected with error 7092 until the lock is released.

> **White Label / Client Portal:** Sort Data by Columns and Reorder Columns are **not available** in custom-domain (portal) contexts. All other column management APIs are available via portal domain URLs when the caller has the required permission.

---

APIs for adding, renaming, reordering, showing, hiding, deleting, and sorting columns.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Add Column](add-column.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns` | `addColumn` | `ZohoAnalytics.modeling.create` | 200 |
| [Rename Column](rename-column.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}` | `renameColumn` | `ZohoAnalytics.modeling.update` | 204 |
| [Delete Column](delete-column.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}` | `deleteColumn` | `ZohoAnalytics.modeling.delete` | 204 |
| [Hide Columns](hide-columns.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/hide` | `hideColumns` | `ZohoAnalytics.modeling.update` | 204 |
| [Show Columns](show-columns.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/show` | `showColumns` | `ZohoAnalytics.modeling.update` | 204 |
| [Get Column Dependents](get-column-dependents.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/dependents` | `getColumnDependents` | `ZohoAnalytics.metadata.read` | 200 |
| [Sort Data by Columns](sort-data-by-columns.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data/sort` | `sortDataByColumns` | `ZohoAnalytics.modeling.update` | 204 |
| [Reorder Columns](reorder-columns.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/reorder` | `reorderColumns` | `ZohoAnalytics.modeling.update` | 204 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# API-Specific Notes and Behaviours

## Add Column

- **Two modes; single mode returns `columnId`, bulk mode does not.** The presence of a `columns` key in CONFIG switches the API to bulk mode automatically. Use Get Table Metadata after a bulk add to find the new column IDs.
- **Mandatory columns in bulk mode:** If `isMandatory: true` is set on a column entry, the `default` field is required for that entry. Omitting `default` when `isMandatory: true` causes the request to fail.
- **DDL lock:** Check for error 7092 if an import is running. Retry after the import completes.
- **Dependency:** `<view-id>` from Get View List. After bulk add, call Get Table Metadata to retrieve new `columnId` values.

## Rename Column

- **Rename propagates automatically.** All views, formulas, and reports referencing the old column name are updated without manual intervention.
- **Pre-check with Get Column Dependents.** If many views depend on the column, a rename is safe (all references are updated), but it is still good practice to audit dependents before bulk renames.
- **Dependency:** `<column-id>` from Get Table Metadata.

## Delete Column

- **Always call Get Column Dependents first.** Understanding what `views`, `customFormulas`, and `aggregateFormulas` depend on this column determines whether a safe deletion (`deleteDependentViews: false`) or a cascade deletion (`deleteDependentViews: true`) is appropriate.
- **`deleteDependentViews: true` is irreversible.** Once confirmed, all listed dependent objects are permanently destroyed.
- **Dependency:** `<column-id>` from Get Table Metadata. Run Get Column Dependents before deciding on `deleteDependentViews`.

## Hide Columns / Show Columns

- **`columnIds` are strings.** Even though column IDs are numeric, they must be passed as quoted strings inside the JSON array.
- **Idempotent for the unchanged direction.** Hiding an already-hidden column or showing an already-visible column is silently no-oped.
- **One-column minimum for Hide.** Ensure at least one column will remain visible after the hide operation. Show Columns has no such constraint.
- **Dependency:** `columnIds` from Get Table Metadata (use the `columnId` field; filter by `isHidden` field to find current visibility state).

## Get Column Dependents

- **Workspace Admin only.** Unlike other column APIs (which accept DESIGNMODIFY permission), this API requires full Workspace Admin access.
- **Call before any destructive column operation.** Both Delete Column and Rename Column can have downstream effects. This API provides the complete impact list.
- **`views` may contain the same view twice** if the column is referenced in multiple ways in that view (e.g., both as a filter and a display column in a query table).
- **Dependency:** `<column-id>` from Get Table Metadata.

## Sort Data by Columns

- **Not available via portal/custom domain URLs.** Only callable through `analyticsapi.zoho.com`.
- **One sort direction for all columns.** The `sortOrder` value applies uniformly to every column in the `columns` array. Mixed-direction sorting must be done through report or query table configuration, not this API.
- **`resetSort: true` is a complete clear.** After reset, all columns will have `sortedOrder: 0` and `sortedIndex: -1` in Get Table Metadata responses.
- **Dependency:** `columns` (column ID strings) from Get Table Metadata.

## Reorder Columns

- **Not available via portal/custom domain URLs.** Only callable through `analyticsapi.zoho.com`.
- **Full column set is mandatory, every call.** Unlike Hide/Show Columns, this API always requires the complete non-system column list — you cannot reorder just two columns without also listing all the others in their existing positions.
- **De-duplication, not rejection.** Repeated IDs in the array are silently collapsed to their first occurrence rather than causing an error.
- **Dependency:** `columns` (column ID strings) from Get Table Metadata, excluding system columns.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **`columnId` type** | Returned as a quoted string in all responses and required as a string in `columnIds` arrays. |
| **Single vs bulk Add Column responses** | Single mode: `data.columnId` is present. Bulk mode: `data` contains internal schema change information; individual `columnId` values are not returned. |
| **`sortOrder` in Sort Data by Columns** | `1` = Ascending (A→Z, smallest to largest). `2` = Descending (Z→A, largest to smallest). Reflected in `sortedOrder` field in Get Table Metadata responses: `0` = no sort, `1` = ascending, `-1` = descending (note the sign difference). |
| **`isHidden` in Get Table Metadata** | `true` when the column was hidden via Hide Columns. Use Show Columns to reverse. |
| **`viewTypeId` in Get Column Dependents** | `1` = Tabular Report, `2` = Chart, `3` = Pivot Table, `4` = Summary View, `6` = Query Table. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7089](../../../foundations/error-codes.md#error-7089) | 400 | All the columns of the table cannot be hidden at the same time. |
| [7092](../../../foundations/error-codes.md#error-7092) | 400 | A DDL lock is active on the table. |
| [7107](../../../foundations/error-codes.md#error-7107) | 400 | The specified column does not exist in the table. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | A view with the given viewName already exists in this workspace. |
| [7125](../../../foundations/error-codes.md#error-7125) | 400 | The specified data type is not compatible with the configuration of the column. |
| [7146](../../../foundations/error-codes.md#error-7146) | 400 | The DATATYPE value is not a recognised data type. |
| [7157](../../../foundations/error-codes.md#error-7157) | 400 | A column with the same name already exists in the table. |
| [7164](../../../foundations/error-codes.md#error-7164) | 400 | The table is a snapshot table and its columns cannot be renamed. |
| [7277](../../../foundations/error-codes.md#error-7277) | 400 | The folder holds tables that have dependent child views, so the deletion is blocked. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7397](../../../foundations/error-codes.md#error-7397) | 400 | The specified view is not a table. |
| [7439](../../../foundations/error-codes.md#error-7439) | 400 | The specified view is not a table. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | Invalid value for attribute. |
| [8173](../../../foundations/error-codes.md#error-8173) | 400 | The number of columns sent in bulk mode exceeds the allowed limit. |
| [8179](../../../foundations/error-codes.md#error-8179) | 403 | The calling user is not an Account Admin, Organization Admin or Workspace Admin of the workspace. |
| [8180](../../../foundations/error-codes.md#error-8180) | 403 | The calling user is a read-only user. Read-only users cannot change tag associations regardless of any other permission. |
| [8182](../../../foundations/error-codes.md#error-8182) | 403 | resetSort and sortOrder cannot be used together. |

# Related

- [Data Modeling & Schema](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
