---
type: API Group
title: Table & Schema
description: APIs for creating tables and fetching table metadata.
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - table-and-schema
  - api-group
api:
  domain: data-modeling-and-schema
  group: table-and-schema
  endpoint_count: 2
  endpoints:
    - operation_id: createTable
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/tables"
      doc: "/domains/data-modeling-and-schema/table-and-schema/create-table.md"
    - operation_id: getTableMetadata
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/metadata"
      doc: "/domains/data-modeling-and-schema/table-and-schema/get-table-metadata.md"
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

This document covers the APIs for creating tables and inspecting table schema (column metadata) in a Zoho Analytics workspace. A table in Zoho Analytics is the primary data container — columns define its structure, and data is pushed or imported into rows.

> **Table vs. View:** In Zoho Analytics, the term *view* encompasses all objects inside a workspace — tables, reports, charts, and dashboards. Every table is a view with a specific type. The Get Table Metadata API accepts the view ID of a table and returns its column definitions.

> **Column-level Permissions:** Get Table Metadata returns only the columns that the calling user has been granted access to. Users with workspace-level DESIGNMODIFY permission see all columns; users with restricted view sharing may see a subset.

> **White Label / Client Portal:** Both APIs are available via portal domain URLs. Portal users with the appropriate workspace permissions can create tables and retrieve schema information.

---

APIs for creating tables and fetching table metadata.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Create Table](create-table.md) | POST | `/restapi/v2/workspaces/{workspace-id}/tables` | `createTable` | `ZohoAnalytics.modeling.create` | 200 |
| [Get Table Metadata](get-table-metadata.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/metadata` | `getTableMetadata` | `ZohoAnalytics.metadata.read` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# API-Specific Notes and Behaviours

## Create Table

- **Response gap:** Only `viewId` is returned. To inspect the created table's column schema, call Get Table Metadata immediately after creation.
- **`FOLDERNAME` resolves by display name:** Unlike most APIs that accept folder IDs, this field accepts the folder's display name. If the name doesn't exactly match an existing folder, the request fails with error 7144. Obtain the exact name from Get Folder List.
- **Lookup column chaining:** If you are creating multiple related tables in sequence, create the parent table first, then create child tables with `LOOKUPCOLUMN` references pointing to the parent.
- **Column ordering:** Columns appear in the table in the order they are listed in the `COLUMNS` array.
- **Dependency:** `FOLDERNAME` → Get Folder List (for the display name). For lookup columns, the referenced `TABLENAME` must match an existing table's display name in the workspace (obtained from Get View List).

## Get Table Metadata

- **Column visibility is caller-scoped:** The `columns` array in the response reflects the subset of columns the caller has access to. Do not assume that an empty or short column list means the table has few columns — the caller may simply have restricted sharing.
- **`pkTableName` identifies lookup source:** When `pkTableName` is a non-empty string, the column is a lookup column. The value is the display name of the parent table, which matches the `TABLENAME` used when the lookup was created.
- **`formulaDisplayName` reveals formula logic:** Non-empty `formulaDisplayName` means the column is a computed formula column. The formula is shown as a human-readable expression.
- **Type-specific formatting fields:** Use `dateFormat`, `currencyFormat`, `decimalPlaces`, etc. to correctly format values when displaying or importing data for those column types.
- **`columnIndex` is the display order:** Columns are returned in the order they appear in the table, sorted by `columnIndex`. This matches what users see in the Zoho Analytics UI.
- **Dependency:** `<view-id>` → Get View List API for the workspace. Verify that the view's type is a table before calling.

## Cross-API Dependency Chain

```
Get Workspace List
  └─ Get View List (for workspace)
       ├─ Get Table Metadata   [requires view-id of a table]
       └─ Create Table
            └─ Get Folder List [for FOLDERNAME value]
```

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **`viewId` in Create Table response** | Returned as a quoted string, not a numeric. Consistent with how all view/column/folder IDs are returned across the API. |
| **`columnId` in Get Table Metadata** | Returned as a quoted string. |
| **`dataType` vs `dataTypeName`** | `dataType` is the internal code used in Create Table requests (e.g., `"PLAIN"`). `dataTypeName` is the human-readable display name (e.g., `"Plain Text"`). Use `dataType` when creating or modifying columns via the API. |
| **Empty string vs absent fields** | `pkTableName`, `pkColumnName`, `formulaDisplayName`, `defaultValue`, `columnDesc` are always present in every column object and default to `""` when not applicable. Type-specific fields (`dateFormat`, `currencyFormat`, etc.) are absent entirely when not applicable to the column's data type. |
| **`columnMaxSize`** | Represents the configured or default maximum storage size for the column. For text columns this is a character limit; for numeric columns it reflects internal precision. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7105](../../../foundations/error-codes.md#error-7105) | 400 | The specified view does not exist. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | A view with the given viewName already exists in this workspace. |
| [7125](../../../foundations/error-codes.md#error-7125) | 400 | The specified data type is not compatible with the configuration of the column. |
| [7126](../../../foundations/error-codes.md#error-7126) | 400 | A column name is empty or missing. |
| [7127](../../../foundations/error-codes.md#error-7127) | 400 | A column name exceeds the maximum allowed length. |
| [7128](../../../foundations/error-codes.md#error-7128) | 400 | Duplicate column names were found in the COLUMNS array. |
| [7143](../../../foundations/error-codes.md#error-7143) | 400 | A DEFAULT value was provided for an AUTO_NUMBER column. |
| [7144](../../../foundations/error-codes.md#error-7144) | 400 | The specified folder does not exist. |
| [7146](../../../foundations/error-codes.md#error-7146) | 400 | The DATATYPE value is not a recognised data type. |
| [7183](../../../foundations/error-codes.md#error-7183) | 400 | The data type of the lookup column is incompatible with the data type of the referenced column. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7379](../../../foundations/error-codes.md#error-7379) | 400 | A lookup column cannot refer to a column within the same table. |
| [7395](../../../foundations/error-codes.md#error-7395) | 400 | The column specified in LOOKUPCOLUMN.COLUMNNAME does not exist in the referenced table. |
| [7397](../../../foundations/error-codes.md#error-7397) | 400 | The specified view is not a table. |
| [7413](../../../foundations/error-codes.md#error-7413) | 400 | TABLENAME is missing or null. |
| [7478](../../../foundations/error-codes.md#error-7478) | 400 | The number of columns exceeds the maximum allowed for a table. |

# Related

- [Data Modeling & Schema](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
