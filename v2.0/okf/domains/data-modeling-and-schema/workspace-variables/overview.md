---
type: API Group
title: Workspace Variables
description: "APIs for creating, updating, deleting, and retrieving workspace variables."
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - workspace-variables
  - api-group
api:
  domain: data-modeling-and-schema
  group: workspace-variables
  endpoint_count: 5
  endpoints:
    - operation_id: createVariable
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/variables"
      doc: "/domains/data-modeling-and-schema/workspace-variables/create-variable.md"
    - operation_id: updateVariable
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}"
      doc: "/domains/data-modeling-and-schema/workspace-variables/update-variable.md"
    - operation_id: deleteVariable
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}"
      doc: "/domains/data-modeling-and-schema/workspace-variables/delete-variable.md"
    - operation_id: getVariables
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/variables"
      doc: "/domains/data-modeling-and-schema/workspace-variables/get-variables.md"
    - operation_id: getVariableDetails
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}"
      doc: "/domains/data-modeling-and-schema/workspace-variables/get-variable-details.md"
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

This document covers the APIs for creating, editing, deleting, and retrieving **workspace variables** — reusable placeholders (e.g., `${Region}`, `${Target Sales}`) that can be embedded in formula expressions, SQL queries, filters, and reports. Variables allow the same report/formula definition to resolve to different values per user (or per Client Portal domain), without duplicating the underlying view.

APIs for creating, updating, deleting, and retrieving workspace variables.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Create Variable](create-variable.md) | POST | `/restapi/v2/workspaces/{workspace-id}/variables` | `createVariable` | `ZohoAnalytics.modeling.create` | 200 |
| [Edit Variable](update-variable.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}` | `updateVariable` | `ZohoAnalytics.modeling.update` | 204 |
| [Delete Variable](delete-variable.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}` | `deleteVariable` | `ZohoAnalytics.modeling.delete` | 204 |
| [Get Variables](get-variables.md) | GET | `/restapi/v2/workspaces/{workspace-id}/variables` | `getVariables` | `ZohoAnalytics.modeling.read` | 200 |
| [Get Variable Details](get-variable-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}` | `getVariableDetails` | `ZohoAnalytics.modeling.read` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is a Workspace Variable?

A variable is defined once at the workspace level with a name, a data type, and a **type** that determines how its value is resolved:

- **List** — the variable resolves to one value picked from a fixed list of allowed values, with a default value.
- **Range** — the variable resolves to a numeric value within a min/max bound, incremented by a step size, with a default value.
- **All Values** — a special type with no explicit values; it always represents "every possible value" (used chiefly as a placeholder default with no per-user override).

Each variable can additionally carry **per-user (or per-portal-domain) overrides** — different sets of allowed values, ranges, and defaults for specific email addresses — falling back to a workspace-wide `defaultData` definition for any user not explicitly listed.

---

# API-Specific Notes and Behaviours

## Create Variable

- **Permission is stricter than most modeling APIs in this documentation suite.** There is no permission-based alternative here (e.g., no "Create Formula"/"Design Modify" option) — only Account Admin, Organization Admin, or Workspace Admin roles can create variables. Regular users with granular permissions cannot.
- **`variableType` and `variableDataType` together gate what fields are valid.** Always cross-check the [Variable Type Values](create-variable.md#variable-type-values) and [Variable Data Type Values](create-variable.md#variable-data-type-values) tables before constructing a request — an otherwise well-formed request fails outright if the combination is invalid (e.g., Range + Text).
- **Dependency chain:** Get Workspace List → Create Variable → `variableId` returned in response → reference the variable by name (`${variableName}`) in formulas/filters/SQL.

## Edit Variable

- **This is a full-replace API, not a patch API** — the exact same behavior pattern as [Edit Query Table](../query-tables/edit-query-table.md), which also requires resending the complete definition. Always fetch the current definition via Get Variable Details first, modify only the fields you intend to change, then resend the full CONFIG.
- **Uniquely among the Edit APIs in this documentation suite, this one supports changing the fundamental "shape" of the object** (`variableType` and `variableDataType`) rather than just its name/values — but doing so is blocked (error 70358) if existing formulas/reports depend on the variable in a way incompatible with the new shape.
- **Dependency chain:** Get Variable Details (fetch current state) → Edit Variable (resend full, modified CONFIG).

## Delete Variable

- **No dedicated "Get Variable Dependents" API exists in this suite**, unlike columns and aggregate formulas which both have their own dependents-lookup endpoints. To determine what references a variable before deleting it, review formula expressions (via [Get Custom Formulas](../formula-columns/get-custom-formula-list.md) / [Get Aggregate Formula](../aggregate-formulas/get-aggregate-formula-list.md)) and report/query definitions for `${variableName}` references manually.
- **No cascade-delete flag** — this is a deliberate difference from Delete Column/Delete Aggregate Formula's `deleteDependentViews` option; dependent objects must always be updated or removed manually first.
- **Dependency chain:** Get Variables → (manually verify no formula/report references exist) → Delete Variable.

## Get Variables

- **Lightweight listing, integer-as-string fields.** Use this for building selection UIs or inventories; switch to Get Variable Details only when the full value set is needed, since `variableType`/`variableDataType` here are strings rather than integers.
- **Dependency chain:** Get Workspace List → Get Variables → `variableId` feeds into Get Variable Details / Edit / Delete Variable.

## Get Variable Details

- **The most detailed "read" response in this API family** — includes conditional per-type fields (`values` vs. `minValue`/`maxValue`/`stepSize`) and an optional top-level `defaultData` object that may be entirely absent for All Values-type variables.
- **Always branch your parsing logic on `variableType` first**, then on `variableDataType` for format-specific fields, since the shape of `defaultData`/`userSpecificData` entries and `format` both depend on these two enums.
- **Dependency chain:** Get Variables (`variableId`) → Get Variable Details.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **`variableType`/`variableDataType` type inconsistency across read APIs** | Get Variables returns these as strings (`"0"`, `"1"`); Get Variable Details returns them as native integers (`0`, `1`). This is the most important cross-API parsing note in this document — do not assume consistent JSON types for the same logical field across different endpoints. |
| **All numeric variable values are transmitted as strings** | `values`, `minValue`, `maxValue`, `stepSize`, and `defaultValue` are always JSON strings in both requests and responses, regardless of the variable's numeric `variableDataType` — this preserves precision for large/decimal numbers. |
| **`defaultData` presence is conditional on `variableType`** | Only List (`0`) and Range (`1`) type variables have a `defaultData` object; All Values (`3`) type variables omit it entirely, both in requests (it is ignored/rejected if sent) and in Get Variable Details responses. |
| **Empty response bodies are common for mutating calls** | Edit Variable and Delete Variable both return HTTP **204 No Content** with no JSON body at all — treat the 2xx status code as the success indicator, not the presence/absence of a `status` field. |
| **Variables are referenced by name, not ID, in downstream APIs** | Unlike columns or formulas (referenced by ID in dependents/value APIs), workspace variables are referenced inside formula expressions and SQL queries using their `variableName` wrapped in `${...}` syntax — the `variableId` returned by these APIs is only used for managing the variable definition itself (Edit/Delete/Get Details), not for embedding it elsewhere. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [70320](../../../foundations/error-codes.md#error-70320) | 400 | USERVARIABLEVARIABLENOTFOUND — <variable-id> does not exist in this workspace. |
| [70321](../../../foundations/error-codes.md#error-70321) | 400 | USERVARIABLEVARIABLEINUSE — The variable is currently referenced elsewhere and cannot be deleted. |
| [70322](../../../foundations/error-codes.md#error-70322) | 400 | USERVARIABLEVARIABLEINUSE (multi-variable form) — One or more of the requested variables are in use. |
| [70323](../../../foundations/error-codes.md#error-70323) | 400 | DUPLICATEUSERVARIABLE — A variable with this name already exists in the workspace. |
| [70324](../../../foundations/error-codes.md#error-70324) | 400 | BLANKVARIABLENAME — variableName is empty. |
| [70325](../../../foundations/error-codes.md#error-70325) | 400 | INVALIDVARNAME — The name uses a reserved pattern (system. prefix, ${ prefix, or } suffix). |
| [70326](../../../foundations/error-codes.md#error-70326) | 400 | CANTDELETEVARIABLE — The variable cannot be deleted by this user (ownership restriction). |
| [70329](../../../foundations/error-codes.md#error-70329) | 400 | CANTDELETEVARIABLE (UNAUTHORIZEDVARACTION) — <variable-id> does not exist in this workspace. |
| [70335](../../../foundations/error-codes.md#error-70335) | 400 | VARIABLERANGENOTALLOWEDONDT — Range type combined with Text data type. |
| [70336](../../../foundations/error-codes.md#error-70336) | 400 | VARIABLEDATANOTPRESENT — No usable value entries could be derived from the request. |
| [70337](../../../foundations/error-codes.md#error-70337) | 400 | VARIABLEDEFAULTVALUENOTPRESENTINLIST — The defaultValue is not one of the values supplied for a List-type entry. |
| [70338](../../../foundations/error-codes.md#error-70338) | 400 | VARIABLERANGEINSUFFICIENTDATA / VARIABLERANGEEXCESSDATA — Range entry is missing a required field or has extra unexpected data. |
| [70339](../../../foundations/error-codes.md#error-70339) | 400 | VARIABLERANGEINSUFFICIENTDATA / VARIABLERANGEEXCESSDATA — Range entry is missing a required field or has extra unexpected data. |
| [70340](../../../foundations/error-codes.md#error-70340) | 400 | VARIABLERANGEDEFAULTVALUEOUTOFRANGE / VARIABLERANGEDEFBWMINMAXRANGE — The defaultValue falls outside [minValue, maxValue]. |
| [70341](../../../foundations/error-codes.md#error-70341) | 400 | VARIABLEDUPLICATEMAILIDORGROUP — The same email address appears in more than one userSpecificData entry. |
| [70342](../../../foundations/error-codes.md#error-70342) | 400 | VARIABLEALLVALUESNOVARIABLEDATA — userSpecificData/defaultData were supplied for an All Values-type variable. |
| [70343](../../../foundations/error-codes.md#error-70343) | 400 | VARIABLENOVARIABLEDATAPRESENT — defaultData is missing for a List or Range-type variable. |
| [70348](../../../foundations/error-codes.md#error-70348) | 400 | VARIABLEEMAILNOTPRESENT — A userSpecificData entry has an empty emailIds array. |
| [70350](../../../foundations/error-codes.md#error-70350) | 400 | VARIABLEINVALIDVARTYPE — variableType is not one of 0, 1, or 3. |
| [70351](../../../foundations/error-codes.md#error-70351) | 400 | VARIABLEINVALIDDATATYPE — variableDataType is not one of the six supported values. |
| [70352](../../../foundations/error-codes.md#error-70352) | 400 | VARIABLERANGEMINLESSTHANMAX — minValue is not less than maxValue. |
| [70353](../../../foundations/error-codes.md#error-70353) | 400 | VARIABLERANGEINCRLESSTHANRANGESIZE — stepSize is larger than the range span. |
| [70354](../../../foundations/error-codes.md#error-70354) | 400 | VARIABLERANGEINCRZEROERR — stepSize is zero. |
| [70355](../../../foundations/error-codes.md#error-70355) | 400 | VARIABLERANGEINCRDIVEQUALLYERR — stepSize does not evenly divide the range span. |
| [70356](../../../foundations/error-codes.md#error-70356) | 400 | VARIABLERANGEDEFAULTVALUEOUTOFRANGE / VARIABLERANGEDEFBWMINMAXRANGE — The defaultValue falls outside [minValue, maxValue]. |
| [70357](../../../foundations/error-codes.md#error-70357) | 400 | USERVARIABLEVARIABLECANNOTBEDELETED — Deletion blocked due to unresolved references. |
| [70358](../../../foundations/error-codes.md#error-70358) | 400 | VARIABLECANNOTBEUPDATED — The requested type/data type change conflicts with existing formula/report references to this variable. |

# Related

- [Data Modeling & Schema](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
