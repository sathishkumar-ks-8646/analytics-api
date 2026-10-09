---
type: API Group
title: Aggregate Formulas (Unified Metrics)
description: APIs for managing aggregate formulas and retrieving values and dependents.
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - aggregate-formulas
  - api-group
api:
  domain: data-modeling-and-schema
  group: aggregate-formulas
  endpoint_count: 7
  endpoints:
    - operation_id: getAggregateFormulaList
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas"
      doc: "/domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-list.md"
    - operation_id: addAggregateFormula
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas"
      doc: "/domains/data-modeling-and-schema/aggregate-formulas/add-aggregate-formula.md"
    - operation_id: editAggregateFormula
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas/{formula-id}"
      doc: "/domains/data-modeling-and-schema/aggregate-formulas/edit-aggregate-formula.md"
    - operation_id: deleteAggregateFormula
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas/{formula-id}"
      doc: "/domains/data-modeling-and-schema/aggregate-formulas/delete-aggregate-formula.md"
    - operation_id: getAggregateFormulasInWorkspace
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/aggregateformulas"
      doc: "/domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formulas-in-workspace.md"
    - operation_id: getAggregateFormulaDependents
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/dependents"
      doc: "/domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-dependents.md"
    - operation_id: getAggregateFormulaValue
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/value"
      doc: "/domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-value.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

This document covers the APIs for creating, editing, deleting, listing, and evaluating **aggregate formulas** — also known as **Unified Metrics** — which are workspace-level, business-metric-style formulas built using aggregate functions (e.g., `sum()`, `max()`, `count_distinct()`) over one or more tables.

APIs for managing aggregate formulas and retrieving values and dependents.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Aggregate Formula](get-aggregate-formula-list.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas` | `getAggregateFormulaList` | `ZohoAnalytics.metadata.read` | 200 |
| [Add Aggregate Formula](add-aggregate-formula.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas` | `addAggregateFormula` | `ZohoAnalytics.modeling.create` | 200 |
| [Edit Aggregate Formula](edit-aggregate-formula.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas/{formula-id}` | `editAggregateFormula` | `ZohoAnalytics.modeling.update` | 204 |
| [Delete Aggregate Formula](delete-aggregate-formula.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas/{formula-id}` | `deleteAggregateFormula` | `ZohoAnalytics.modeling.delete` | 204 |
| [Get Unified Metrics in Workspace](get-aggregate-formulas-in-workspace.md) | GET | `/restapi/v2/workspaces/{workspace-id}/aggregateformulas` | `getAggregateFormulasInWorkspace` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Aggregate Formula Dependents](get-aggregate-formula-dependents.md) | GET | `/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/dependents` | `getAggregateFormulaDependents` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Aggregate Formula Value](get-aggregate-formula-value.md) | GET | `/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/value` | `getAggregateFormulaValue` | `ZohoAnalytics.metadata.read` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is an Aggregate Formula?

Unlike a [custom formula column](../formula-columns/overview.md) (which computes a value per row), an **aggregate formula** produces a single summarized value (e.g., total sales, average order value) by applying an aggregate function across rows of a table. Aggregate formulas:

- Are defined at the level of a specific table/view (the "owning" view), but can reference columns from related tables connected via lookups.
- Can be reused across multiple reports, charts, and dashboards within the workspace as a single source of truth for a business metric — hence the term **Unified Metrics**.
- Support **synonyms** (alternate names) and a **priority** ranking, both of which are used by Zoho Analytics' natural-language search/insight features to better match user queries to the right metric.

> **Expression visibility depends on permission:** For users without edit permission on the aggregate formula (e.g., users with only view/share access), the `expression` field in list responses is returned as an **empty string** — the underlying formula logic is not exposed to non-editors, though the computed name, description, and metadata still are.

---

# API-Specific Notes and Behaviours

## Get Aggregate Formula (view-scoped)

- **Entry point for view-owned formula management.** Use this to enumerate formulas before editing/deleting them via the view-scoped APIs.
- **`subtypeName` key** — remember this differs from the `subtype` key used in the workspace-scoped [Get Unified Metrics in Workspace](get-aggregate-formulas-in-workspace.md). Do not assume identical field names across the two "list" endpoints.
- **Dependency chain:** Get View List → Get Aggregate Formula → Edit/Delete Aggregate Formula.

## Add Aggregate Formula

- **`synonyms` and `columnPriority` power NLP/Ask Zia search**, not the computed value. Populate these fields when you want the metric to be discoverable via natural-language queries in Zoho Analytics' AI-assisted search.
- **Cross-table expressions require an existing lookup.** If your expression spans two tables, ensure a [lookup relationship](../lookups-and-relationships/overview.md) already connects them, or the expression will fail to resolve the referenced column.
- **Dependency chain:** Get Table Metadata (verify columns) → Add Aggregate Formula → `formulaId` returned in response.

## Edit Aggregate Formula

- **The only formula-edit API in this API suite that supports renaming without resending the expression.** Compare this to [Edit Custom Formula](../formula-columns/edit-formula-column.md), which has no rename capability at all. This asymmetry is a deliberate design difference between per-row formula columns and workspace-level aggregate formulas — plan integrations accordingly.
- **`synonyms` array is a full replace, not an append.** Always fetch and merge the existing list first if you want to add to it incrementally.
- **Dependency chain:** Get Aggregate Formula / Get Unified Metrics in Workspace (`formulaId`) → Edit Aggregate Formula.

## Delete Aggregate Formula

- **Always run Get Aggregate Formula Dependents first.** The dependents check considers `childViews`, `childDashboards`, and `aggregateFormulas` — all three categories are subject to cascading deletion when `deleteDependentViews: true` is set.
- **Dependency chain:** Get Aggregate Formula Dependents → Delete Aggregate Formula.

## Get Unified Metrics in Workspace

- **The most complete formula inventory in this API set.** Unlike the view-scoped listing, this returns formulas from every table/view in the workspace in one call, along with the owning `tableId`/`tableName` — ideal for building a workspace-wide metrics catalogue or documentation page.
- **Only requires Read permission**, not Create Formula permission — broader audience of callers can use this listing endpoint compared to the view-scoped CRUD APIs.
- **Dependency chain:** Get Unified Metrics in Workspace → Get Aggregate Formula Dependents / Get Aggregate Formula Value (using the returned `formulaId`).

## Get Aggregate Formula Dependents

- **`parentTables` is unique to this API** — none of the other Get Dependents-style APIs in this documentation set (e.g., [Get Column Dependents](../columns/get-column-dependents.md)) return lineage information about what the object is built *from*; only aggregate formula dependents include this.
- **Dependency chain:** Get Unified Metrics in Workspace (`formulaId`) → Get Aggregate Formula Dependents → (optional) Delete Aggregate Formula.

## Get Aggregate Formula Value

- **This is the only API in the entire aggregate formula/custom formula documentation set that returns computed data rather than metadata.** Use it sparingly for large/complex formulas since each call triggers a live query execution.
- **Column-level permission matters, not just workspace-level.** A user could pass the workspace Read check yet still be denied here if they lack visibility into a specific column used by the formula's expression.
- **Dependency chain:** Get Unified Metrics in Workspace (`formulaId`) → Get Aggregate Formula Value.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **`formulaId` is shared across view-scoped and workspace-scoped APIs** | The same `formulaId` value returned by the view-scoped [Get Aggregate Formula](get-aggregate-formula-list.md) is used to call the workspace-scoped [Get Aggregate Formula Dependents](get-aggregate-formula-dependents.md) and [Get Aggregate Formula Value](get-aggregate-formula-value.md) — no separate ID resolution is needed. |
| **`subtypeName` in Get Aggregate Formula vs `subtype` in Get Unified Metrics in Workspace** | Both fields describe the same internal result-data-type code, but use different JSON keys between the view-scoped and workspace-scoped listing APIs. Always check which endpoint you're parsing. |
| **Expression redaction is permission-based, not role-based** | Whether `expression` is visible depends on whether the specific calling user has edit permission on that specific formula (which may vary formula-by-formula for custom-role users), not simply their broad role (Admin/Shared/Group). |
| **Empty response bodies are common for mutating calls** | Edit Aggregate Formula and Delete Aggregate Formula both return HTTP **204 No Content** with no JSON body at all — treat the 2xx status code as the success indicator, not the presence/absence of a `status` field. |
| **`formulaValue` is always serialized as a string** | Regardless of whether the aggregate's `subtypeId` indicates `NUMBER` or `DECIMAL_NUMBER`, the value in Get Aggregate Formula Value is returned as a JSON string, not a native number — parse accordingly. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7107](../../../foundations/error-codes.md#error-7107) | 400 | The specified column does not exist in the table. |
| [7112](../../../foundations/error-codes.md#error-7112) | 400 | The formula expression could not be parsed (syntax error). |
| [7113](../../../foundations/error-codes.md#error-7113) | 400 | The expression references an unknown/unsupported function. |
| [7115](../../../foundations/error-codes.md#error-7115) | 400 | The expression references a column that does not exist, or the formula is otherwise invalid. |
| [7116](../../../foundations/error-codes.md#error-7116) | 400 | The expression references a column that does not exist, or the formula is otherwise invalid. |
| [7160](../../../foundations/error-codes.md#error-7160) | 400 | Formula columns are not allowed for this user/view combination. |
| [7173](../../../foundations/error-codes.md#error-7173) | 400 | The aggregate formula is currently used by one or more dependent views/dashboards/formulas; deletion blocked. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7428](../../../foundations/error-codes.md#error-7428) | 400 | The specified <formula-id> is not a valid aggregate formula on this view. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | A required attribute (expression or formulaName) is missing from CONFIG. |

# Related

- [Data Modeling & Schema](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
