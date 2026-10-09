---
type: API Group
title: Custom Formula Columns
description: APIs for managing custom formula columns and copying formulas.
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - formula-columns
  - api-group
api:
  domain: data-modeling-and-schema
  group: formula-columns
  endpoint_count: 5
  endpoints:
    - operation_id: getCustomFormulaList
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas"
      doc: "/domains/data-modeling-and-schema/formula-columns/get-custom-formula-list.md"
    - operation_id: addFormulaColumn
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas"
      doc: "/domains/data-modeling-and-schema/formula-columns/add-formula-column.md"
    - operation_id: editFormulaColumn
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas/{formula-id}"
      doc: "/domains/data-modeling-and-schema/formula-columns/edit-formula-column.md"
    - operation_id: deleteFormulaColumn
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas/{formula-id}"
      doc: "/domains/data-modeling-and-schema/formula-columns/delete-formula-column.md"
    - operation_id: copyFormulas
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/formulas/copy"
      doc: "/domains/data-modeling-and-schema/formula-columns/copy-formulas.md"
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

This document covers the APIs for creating, editing, deleting, listing, and copying **custom formula columns** — computed columns whose values are derived from an expression referencing other columns in the same table/view.

> **Naming note:** The URL path for these APIs accepts both `customformulas` and `formulacolumns` as equivalent path segments (an alias for backward compatibility). This document uses **`customformulas`** exclusively, which is the recommended path segment for all new integrations.

> **Tables and single views only:** Custom formula columns can be added to tables and most report/view types. They are **not supported on Pipeline Tables** — attempting to add or edit a formula column on a pipeline table returns error 7467.

---

APIs for managing custom formula columns and copying formulas.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Custom Formulas](get-custom-formula-list.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas` | `getCustomFormulaList` | `ZohoAnalytics.metadata.read` | 200 |
| [Add Custom Formula](add-formula-column.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas` | `addFormulaColumn` | `ZohoAnalytics.modeling.create` | 200 |
| [Edit Custom Formula](edit-formula-column.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas/{formula-id}` | `editFormulaColumn` | `ZohoAnalytics.modeling.update` | 204 |
| [Delete Custom Formula](delete-formula-column.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas/{formula-id}` | `deleteFormulaColumn` | `ZohoAnalytics.modeling.delete` | 204 |
| [Copy Custom Formulas](copy-formulas.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/formulas/copy` | `copyFormulas` | `ZohoAnalytics.modeling.create` | 204 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# API-Specific Notes and Behaviours

## Get Custom Formulas

- **Entry point for the other three same-view APIs.** The `formulaId` values returned here are required for Edit and Delete.
- **Does not expose the expression.** If you need to review or diff a formula's logic before editing, you must maintain your own record of the expression text externally — this API only returns `formulaId` and `formulaName`.
- **Dependency chain:** Get View List → Get Custom Formulas → Edit/Delete Custom Formula.

## Add Custom Formula

- **Column references must exactly match display names.** Use Get Table Metadata beforehand to confirm the exact spelling/casing of columns referenced in the `expression`.
- **Data type is inferred, not declared.** There is no `dataType` parameter — the formula's result type is determined by the expression itself.
- **Dependency chain:** Get View List → Get Table Metadata (verify column names) → Add Custom Formula → response `formulaId`.

## Edit Custom Formula

- **Cannot rename the formula.** The `formulaName` field is not accepted by this API, unlike Create Formula. This is a deliberate asymmetry between the two APIs — plan integrations accordingly (a rename requires delete + recreate).
- **Full expression replacement only.** There is no way to patch a sub-part of the expression; always resend the complete formula text.
- **Dependency chain:** Get Custom Formulas (`formulaId`) → Edit Custom Formula.

## Delete Custom Formula

- **Not idempotent.** Deleting a non-existent or already-deleted formula ID returns an error, not a silent success.
- **Use `deleteDependentViews` cautiously.** As with [Delete Column](../columns/delete-column.md), cascading deletes of dependent reports/charts/formulas are irreversible.
- **Dependency chain:** Get Custom Formulas (`formulaId`) → (optional) Get Column Dependents → Delete Custom Formula.

## Copy Custom Formulas

- **Restricted to Account Admin / Org Admin only** — the only API in this document (and one of the few in the whole API suite) that excludes Workspace Admins entirely.
- **Matches formulas by name across workspaces.** This implies the destination view must already have a compatible schema (same base columns the formula's expression references) for the copy to succeed.
- **Cross-org copy requires `ZANALYTICS-DEST-ORGID` + `workspaceKey` (Org Admin) or `ZANALYTICS-ORGID` set to the destination org + `workspaceKey` (Account Admin)** — identical pattern to Copy Workspace. See [Workspace Operations](../../workspace-management/workspace-operations/overview.md) for the full explanation of this cross-org header mechanism.
- **No response body.** Always verify success via Get Custom Formulas on the destination view.
- **Dependency chain:** Get Custom Formulas (source view, to get exact `formulaName` values) → Get Workspace SecretKey (destination workspace, if cross-org) → Copy Custom Formulas → Get Custom Formulas (destination view, to verify).

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **`formulaId` vs `columnId`** | A formula column's `formulaId` (as returned by these APIs) is the same underlying value as its `columnId` in Get Table Metadata and Get Column Dependents. Formula columns are a special case of table/view columns. |
| **Empty response bodies are common in this API set** | Edit Custom Formula, Delete Custom Formula, and Copy Custom Formulas all return no JSON payload on success — only an HTTP `204 No Content` status. Always design integrations to treat the HTTP status code as the success indicator rather than parsing a response body. |
| **`customFormulas` naming convention** | Despite the underlying URL path supporting both `customformulas` and `formulacolumns`, the JSON response key is always `customFormulas` (camelCase) when the `customformulas` path is used — use this document's path consistently to avoid ambiguity. |
| **Formula expressions are workspace-local** | An expression valid in one view cannot be blindly reused in another unless the referenced column names exist there too — this is precisely what Copy Custom Formulas automates, provided the destination view has matching columns. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7107](../../../foundations/error-codes.md#error-7107) | 400 | The specified column does not exist in the table. |
| [7112](../../../foundations/error-codes.md#error-7112) | 400 | The formula expression could not be parsed because of a syntax error. |
| [7113](../../../foundations/error-codes.md#error-7113) | 400 | The expression refers to an unknown or unsupported function. |
| [7115](../../../foundations/error-codes.md#error-7115) | 400 | The expression refers to a column that does not exist in the view. |
| [7116](../../../foundations/error-codes.md#error-7116) | 400 | The formula is invalid. |
| [7160](../../../foundations/error-codes.md#error-7160) | 400 | Formula columns are not allowed for this combination of user and view. |
| [7180](../../../foundations/error-codes.md#error-7180) | 400 | The formula creates a circular dependency. |
| [7181](../../../foundations/error-codes.md#error-7181) | 400 | The formula creates a circular dependency. |
| [7277](../../../foundations/error-codes.md#error-7277) | 400 | The folder holds tables that have dependent child views, so the deletion is blocked. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7427](../../../foundations/error-codes.md#error-7427) | 400 | The specified formula ID is not a valid formula column on this view. |
| [7467](../../../foundations/error-codes.md#error-7467) | 400 | Formula columns are not supported on pipeline tables. |
| [8058](../../../foundations/error-codes.md#error-8058) | 400 | The organization ID provided in the ZANALYTICS-DEST-ORGID header does not exist. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | A mandatory attribute is missing from the configuration. |
| [15007](../../../foundations/error-codes.md#error-15007) | 400 | The copy is not allowed because the organisation of the destination workspace does not match that of the caller and no valid workspace key was supplied. |

# Related

- [Data Modeling & Schema](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
