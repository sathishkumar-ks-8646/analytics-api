---
type: API Group
title: Query Tables
description: "APIs for creating, editing, and retrieving query table details."
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - query-tables
  - api-group
api:
  domain: data-modeling-and-schema
  group: query-tables
  endpoint_count: 4
  endpoints:
    - operation_id: getQueryTables
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/querytables"
      doc: "/domains/data-modeling-and-schema/query-tables/get-query-tables.md"
    - operation_id: createQueryTable
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/querytables"
      doc: "/domains/data-modeling-and-schema/query-tables/create-query-table.md"
    - operation_id: editQueryTable
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}"
      doc: "/domains/data-modeling-and-schema/query-tables/edit-query-table.md"
    - operation_id: getQueryTableDetails
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}"
      doc: "/domains/data-modeling-and-schema/query-tables/get-query-table-details.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

This document covers the APIs for creating, editing, listing, and inspecting **Query Tables** — virtual tables defined by a user-written SQL `SELECT` query that runs against one or more existing tables/views in the workspace.

APIs for creating, editing, and retrieving query table details.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Query Tables](get-query-tables.md) | GET | `/restapi/v2/workspaces/{workspace-id}/querytables` | `getQueryTables` | `ZohoAnalytics.metadata.read` | 200 |
| [Create Query Table](create-query-table.md) | POST | `/restapi/v2/workspaces/{workspace-id}/querytables` | `createQueryTable` | `ZohoAnalytics.modeling.create` | 200 |
| [Edit Query Table](edit-query-table.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}` | `editQueryTable` | `ZohoAnalytics.modeling.update` | 204 |
| [Get Query Table Details](get-query-table-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}` | `getQueryTableDetails` | `ZohoAnalytics.metadata.read` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is a Query Table?

A **Query Table** (also called a **SQL View** or **QT**) is a view whose data is computed by executing a custom SQL query at query time rather than storing raw imported data. It allows joining, aggregating, and transforming data from one or more existing tables in the workspace using standard SQL syntax.

> **Rate Limited:** Create Query Table and Edit Query Table are throttled — a maximum of 7 requests per user per minute (5-minute lockout on breach) and 15 requests per minute service-wide. Design your integration to batch or space out query table creation/edit calls accordingly.

---

# API-Specific Notes and Behaviours

## Get Query Tables

- **CONFIG is fully optional.** All fields default sensibly — omit CONFIG for a simple, unfiltered listing.
- **Pagination requires both `startIndex` and `noOfResult`.** Supplying only one has no effect.
- **`viewId` values feed directly into Edit and Get Details.** No separate ID resolution API call is required — this listing API is the entry point for the other three.

## Create Query Table

- **SQL is validated synchronously at creation time.** All syntax, table-reference, and column-reference checks happen before the API returns; there is no separate "draft" or "async validation" step exposed via this API.
- **Response is minimal — only `viewId`.** Always follow up with Get Query Table Details to retrieve the resolved column schema, since column names/types are derived from the query, not specified explicitly by the caller.
- **`folderId` defaults to the workspace's default folder.** Use Get Folder List and Make Default Folder (see [Workspace Folders](../../workspace-management/workspace-folders/overview.md)) to control the target folder explicitly.
- **Dependency chain:** Get View List (to identify valid source table names for the SQL) → Create Query Table → Get Query Table Details (to retrieve `viewId`'s resolved schema).

## Edit Query Table

- **`sqlQuery` must always be resent in full**, even for a folder-only move, because it is a mandatory attribute. There is no partial-update semantics.
- **No rename/description support.** This API cannot change `queryTableName` or `description` — only `sqlQuery` and `folderId`.
- **Changing the `SELECT` clause changes the column schema.** Any report, chart, or pivot built on a column that is renamed or removed from the new query will break. Always call Get Column Dependents-equivalent checks (via Get Query Table Details → `columns`) before making structural changes.
- **Dependency chain:** Get Query Table Details (fetch current `sqlQuery`) → modify → Edit Query Table → Get Query Table Details (confirm new schema).

## Get Query Table Details

- **Primary source of truth for the SQL definition.** Since the SQL is not exposed anywhere else (not in Get Query Tables list), always use this API to retrieve/audit the query text.
- **`involvedViews` is not recursive.** For query tables built on top of other query tables, only the immediate source is listed — trace nested dependencies manually if needed.
- **Dependency chain:** Get Query Tables (`viewId`) → Get Query Table Details → `involvedViews` cross-referenced against Get View List / Get Table Metadata for full lineage.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Rate limiting is per-user AND service-wide** | Both Create Query Table and Edit Query Table enforce a 7-per-minute-per-user limit (5-minute lockout) as well as a 15-per-minute service-wide limit. Exceeding either results in throttling — plan bulk operations with delays between calls. |
| **Query table columns follow the same schema shape as regular table columns** | The `columns` array in Get Query Table Details uses the same field structure (`columnId`, `dataType`, `dataTypeName`, `isHidden`, `sortedOrder`, etc.) documented in [Table & Schema](../table-and-schema/overview.md) and [Columns](../columns/overview.md). |
| **Edit Query Table has no data payload on success** | Unlike Create (`viewId`) and Get Details (full metadata), a successful Edit call returns HTTP `204 No Content` with no response body. |
| **`orgId` in responses is the organisation ID, not the workspace ID** | Do not confuse `orgId` with `workspaceId` when parsing responses. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7399](../../../foundations/error-codes.md#error-7399) | 400 | The query references a spatial (GEO) file-based table, which is not supported for query tables. |
| [7400](../../../foundations/error-codes.md#error-7400) | 400 | Query tables are not supported/allowed for this workspace. |
| [7401](../../../foundations/error-codes.md#error-7401) | 400 | The SQL statement is not a valid/allowed SQL construct. |
| [7402](../../../foundations/error-codes.md#error-7402) | 400 | The SQL statement is invalid. |
| [7403](../../../foundations/error-codes.md#error-7403) | 400 | Parsing of the SQL query failed. |
| [7404](../../../foundations/error-codes.md#error-7404) | 400 | Conversion of the SQL query to the internal execution engine failed. |
| [7407](../../../foundations/error-codes.md#error-7407) | 400 | An invalid column was referenced in the SELECT clause. |
| [7408](../../../foundations/error-codes.md#error-7408) | 400 | An invalid column was referenced elsewhere in the query (e.g., WHERE, GROUP BY). |
| [7409](../../../foundations/error-codes.md#error-7409) | 400 | An invalid/unknown table was referenced in the query. |
| [7413](../../../foundations/error-codes.md#error-7413) | 400 | TABLENAME is missing or null. |
| [7421](../../../foundations/error-codes.md#error-7421) | 400 | A general SQL parse error occurred. |
| [7422](../../../foundations/error-codes.md#error-7422) | 400 | The query table is referenced as a source by a child view, preventing this type of structural change. |
| [7429](../../../foundations/error-codes.md#error-7429) | 400 | A design edit (schema change) is already in progress for this query table. |
| [7433](../../../foundations/error-codes.md#error-7433) | 400 | Duplicate column names detected in the SELECT clause (after aliasing). |
| [7447](../../../foundations/error-codes.md#error-7447) | 400 | The query result would exceed the allowed row/column limit. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | INVALIDVALUEFORATTRIBUTE — fileType, onError, delimiter, quoted, thousandSeparator, or decimalSeparator is outside its permitted set. |

# Related

- [Data Modeling & Schema](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
