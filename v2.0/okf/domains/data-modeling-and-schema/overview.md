---
type: API Domain
title: Data Modeling & Schema
description: "API for Data Modeling & Schema in Zoho Analytics — covering tables, schema, columns, lookups, query tables, formulas, and workspace variables."
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - api-domain
api:
  domain: data-modeling-and-schema
  groups:
    - group: table-and-schema
      title: Table & Schema
      doc: "/domains/data-modeling-and-schema/table-and-schema/overview.md"
      endpoint_count: 2
    - group: columns
      title: Columns
      doc: "/domains/data-modeling-and-schema/columns/overview.md"
      endpoint_count: 8
    - group: lookups-and-relationships
      title: Lookups & Relationships
      doc: "/domains/data-modeling-and-schema/lookups-and-relationships/overview.md"
      endpoint_count: 2
    - group: query-tables
      title: Query Tables
      doc: "/domains/data-modeling-and-schema/query-tables/overview.md"
      endpoint_count: 4
    - group: formula-columns
      title: Custom Formula Columns
      doc: "/domains/data-modeling-and-schema/formula-columns/overview.md"
      endpoint_count: 5
    - group: aggregate-formulas
      title: Aggregate Formulas (Unified Metrics)
      doc: "/domains/data-modeling-and-schema/aggregate-formulas/overview.md"
      endpoint_count: 7
    - group: workspace-variables
      title: Workspace Variables
      doc: "/domains/data-modeling-and-schema/workspace-variables/overview.md"
      endpoint_count: 5
  endpoint_count: 33
  openapi: "/references/openapi/data-modeling-schema-grouped-api.json"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

API for Data Modeling & Schema in Zoho Analytics — covering tables, schema, columns, lookups, query tables, formulas, and workspace variables.

# API Groups

| Group | Endpoints | Description |
|---|---|---|
| [Table & Schema](table-and-schema/overview.md) | 2 | APIs for creating tables and fetching table metadata. |
| [Columns](columns/overview.md) | 8 | APIs for adding, renaming, reordering, showing, hiding, deleting, and sorting columns. |
| [Lookups & Relationships](lookups-and-relationships/overview.md) | 2 | APIs for adding and removing lookup relationships. |
| [Query Tables](query-tables/overview.md) | 4 | APIs for creating, editing, and retrieving query table details. |
| [Custom Formula Columns](formula-columns/overview.md) | 5 | APIs for managing custom formula columns and copying formulas. |
| [Aggregate Formulas (Unified Metrics)](aggregate-formulas/overview.md) | 7 | APIs for managing aggregate formulas and retrieving values and dependents. |
| [Workspace Variables](workspace-variables/overview.md) | 5 | APIs for creating, updating, deleting, and retrieving workspace variables. |

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Create Table](table-and-schema/create-table.md) | POST | `/restapi/v2/workspaces/{workspace-id}/tables` | `createTable` | `ZohoAnalytics.modeling.create` | 200 |
| [Get Table Metadata](table-and-schema/get-table-metadata.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/metadata` | `getTableMetadata` | `ZohoAnalytics.metadata.read` | 200 |
| [Add Column](columns/add-column.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns` | `addColumn` | `ZohoAnalytics.modeling.create` | 200 |
| [Rename Column](columns/rename-column.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}` | `renameColumn` | `ZohoAnalytics.modeling.update` | 204 |
| [Delete Column](columns/delete-column.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}` | `deleteColumn` | `ZohoAnalytics.modeling.delete` | 204 |
| [Hide Columns](columns/hide-columns.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/hide` | `hideColumns` | `ZohoAnalytics.modeling.update` | 204 |
| [Show Columns](columns/show-columns.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/show` | `showColumns` | `ZohoAnalytics.modeling.update` | 204 |
| [Get Column Dependents](columns/get-column-dependents.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/dependents` | `getColumnDependents` | `ZohoAnalytics.metadata.read` | 200 |
| [Sort Data by Columns](columns/sort-data-by-columns.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data/sort` | `sortDataByColumns` | `ZohoAnalytics.modeling.update` | 204 |
| [Reorder Columns](columns/reorder-columns.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/reorder` | `reorderColumns` | `ZohoAnalytics.modeling.update` | 204 |
| [Add Lookup](lookups-and-relationships/add-lookup.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup` | `addLookup` | `ZohoAnalytics.modeling.update` | 204 |
| [Remove Lookup](lookups-and-relationships/remove-lookup.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup` | `removeLookup` | `ZohoAnalytics.modeling.update` | 204 |
| [Get Query Tables](query-tables/get-query-tables.md) | GET | `/restapi/v2/workspaces/{workspace-id}/querytables` | `getQueryTables` | `ZohoAnalytics.metadata.read` | 200 |
| [Create Query Table](query-tables/create-query-table.md) | POST | `/restapi/v2/workspaces/{workspace-id}/querytables` | `createQueryTable` | `ZohoAnalytics.modeling.create` | 200 |
| [Edit Query Table](query-tables/edit-query-table.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}` | `editQueryTable` | `ZohoAnalytics.modeling.update` | 204 |
| [Get Query Table Details](query-tables/get-query-table-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}` | `getQueryTableDetails` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Custom Formulas](formula-columns/get-custom-formula-list.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas` | `getCustomFormulaList` | `ZohoAnalytics.metadata.read` | 200 |
| [Add Custom Formula](formula-columns/add-formula-column.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas` | `addFormulaColumn` | `ZohoAnalytics.modeling.create` | 200 |
| [Edit Custom Formula](formula-columns/edit-formula-column.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas/{formula-id}` | `editFormulaColumn` | `ZohoAnalytics.modeling.update` | 204 |
| [Delete Custom Formula](formula-columns/delete-formula-column.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas/{formula-id}` | `deleteFormulaColumn` | `ZohoAnalytics.modeling.delete` | 204 |
| [Copy Custom Formulas](formula-columns/copy-formulas.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/formulas/copy` | `copyFormulas` | `ZohoAnalytics.modeling.create` | 204 |
| [Get Aggregate Formula](aggregate-formulas/get-aggregate-formula-list.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas` | `getAggregateFormulaList` | `ZohoAnalytics.metadata.read` | 200 |
| [Add Aggregate Formula](aggregate-formulas/add-aggregate-formula.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas` | `addAggregateFormula` | `ZohoAnalytics.modeling.create` | 200 |
| [Edit Aggregate Formula](aggregate-formulas/edit-aggregate-formula.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas/{formula-id}` | `editAggregateFormula` | `ZohoAnalytics.modeling.update` | 204 |
| [Delete Aggregate Formula](aggregate-formulas/delete-aggregate-formula.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas/{formula-id}` | `deleteAggregateFormula` | `ZohoAnalytics.modeling.delete` | 204 |
| [Get Unified Metrics in Workspace](aggregate-formulas/get-aggregate-formulas-in-workspace.md) | GET | `/restapi/v2/workspaces/{workspace-id}/aggregateformulas` | `getAggregateFormulasInWorkspace` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Aggregate Formula Dependents](aggregate-formulas/get-aggregate-formula-dependents.md) | GET | `/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/dependents` | `getAggregateFormulaDependents` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Aggregate Formula Value](aggregate-formulas/get-aggregate-formula-value.md) | GET | `/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/value` | `getAggregateFormulaValue` | `ZohoAnalytics.metadata.read` | 200 |
| [Create Variable](workspace-variables/create-variable.md) | POST | `/restapi/v2/workspaces/{workspace-id}/variables` | `createVariable` | `ZohoAnalytics.modeling.create` | 200 |
| [Edit Variable](workspace-variables/update-variable.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}` | `updateVariable` | `ZohoAnalytics.modeling.update` | 204 |
| [Delete Variable](workspace-variables/delete-variable.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}` | `deleteVariable` | `ZohoAnalytics.modeling.delete` | 204 |
| [Get Variables](workspace-variables/get-variables.md) | GET | `/restapi/v2/workspaces/{workspace-id}/variables` | `getVariables` | `ZohoAnalytics.modeling.read` | 200 |
| [Get Variable Details](workspace-variables/get-variable-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}` | `getVariableDetails` | `ZohoAnalytics.modeling.read` | 200 |

# Related

- [All domains](../index.md)
- [OpenAPI specification for this domain](../../references/openapi/data-modeling-schema-grouped-api.json)
- [Foundations](../../foundations/index.md)
