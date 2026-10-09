---
type: API Group
title: Lookups & Relationships
description: APIs for adding and removing lookup relationships.
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - lookups-and-relationships
  - api-group
api:
  domain: data-modeling-and-schema
  group: lookups-and-relationships
  endpoint_count: 2
  endpoints:
    - operation_id: addLookup
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup"
      doc: "/domains/data-modeling-and-schema/lookups-and-relationships/add-lookup.md"
    - operation_id: removeLookup
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup"
      doc: "/domains/data-modeling-and-schema/lookups-and-relationships/remove-lookup.md"
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

This document covers the APIs for creating and removing lookup relationships between tables in a Zoho Analytics workspace.

APIs for adding and removing lookup relationships.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Add Lookup](add-lookup.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup` | `addLookup` | `ZohoAnalytics.modeling.update` | 204 |
| [Remove Lookup](remove-lookup.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup` | `removeLookup` | `ZohoAnalytics.modeling.update` | 204 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is a Lookup?

A **lookup** (also called a **relationship**) links two tables in a workspace through a shared column, analogous to a foreign key constraint in a relational database:

- The **child table** is the table that holds the foreign-key values. Its column is identified by `<column-id>` in the URL.
- The **reference table** (parent table) holds the primary/unique key values. It is identified by `referenceViewId` in CONFIG.
- The **reference column** (`referenceColumnId`) must contain **unique values** in the reference table (acts as the unique key side of the relationship).
- The data type of the child column and the reference column must be **compatible**.

Once a lookup is established, multi-table reports, pivot tables, and query tables can pull data from both the child and reference tables without manual joins. The relationship is visible in the Schema View of the workspace.

> **Tables only:** Lookups can only be created between tables. Reports, charts, pivot tables, query tables, and dashboards cannot be used as the child view or the reference view.

> **Same workspace:** Both the child table and the reference table must belong to the same workspace.

---

# API-Specific Notes and Behaviours

## Add Lookup

- **One child column, one relationship.** A column can hold at most one lookup. To re-point a lookup to a different reference column, the existing one must be removed first.
- **Reference column uniqueness is a prerequisite.** Validate that `referenceColumnId` has unique values before calling. If the reference table contains duplicate values in that column, error 7509 is returned and no lookup is created.
- **Data type must be compatible.** Check the data type of the child column (from Get Table Metadata on `<view-id>`) and the reference column (from Get Table Metadata on `referenceViewId`) before calling.
- **Dependency chain for ID resolution:**
  1. Get Workspace Info → `<workspace-id>`
  2. Get View List → `<view-id>` (child table), `referenceViewId` (reference table)
  3. Get Table Metadata on child table → `<column-id>`
  4. Get Table Metadata on reference table → `referenceColumnId`

## Remove Lookup

- **Not idempotent.** Returns error 7378 if no lookup exists — not a silent success.
- **Always audit dependents first.** Use Get Column Dependents on `<column-id>` to discover which views join across this relationship. Only then decide whether to use `deleteDependentViews: true`.
- **`deleteDependentViews: true` is a cascading permanent delete.** All reports, charts, pivot tables, and query tables that are built across the child and reference tables via this lookup are permanently removed. There is no recovery.
- **Dependency chain for ID resolution:**
  1. Get View List → `<view-id>` (child table)
  2. Get Table Metadata → `<column-id>`
  3. Get Column Dependents → audit impact before proceeding

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **No data payload on success** | Both Add Lookup and Remove Lookup return HTTP `204 No Content` with **no JSON body at all** — not even a `status`/`summary` string. This differs from most other modeling APIs in this documentation suite that return HTTP 200 with a `{"status":"success","summary":"..."}` body. Only failure responses (4xx/5xx) contain a JSON error payload. No relationship IDs or column metadata are returned on success. |
| **Relationship reflection** | After Add Lookup, the Schema View in the Zoho Analytics UI shows a line between the child and reference tables. After Remove Lookup, this line disappears. |
| **`referenceViewId` and `referenceColumnId` in CONFIG are long integers** | Unlike `columnIds` in Hide/Show Columns (which are strings), these values are passed as unquoted numbers in CONFIG: `{"referenceViewId": 7617000000509100, "referenceColumnId": 7617000000509105}`. |
| **Impact on multi-table reports** | Lookups enable cross-table analysis. Adding a lookup makes it possible to drag columns from both tables into a single report. Removing a lookup breaks any report that currently joins the two tables via that column. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7107](../../../foundations/error-codes.md#error-7107) | 400 | The specified column does not exist in the table. |
| [7166](../../../foundations/error-codes.md#error-7166) | 400 | The child column is itself a lookup-derived column (lookup-on-lookup is not allowed). |
| [7183](../../../foundations/error-codes.md#error-7183) | 400 | The lookup column's data type is incompatible with the referenced column's data type. |
| [7184](../../../foundations/error-codes.md#error-7184) | 400 | Adding this lookup would create a circular relationship chain across tables. |
| [7280](../../../foundations/error-codes.md#error-7280) | 400 | A lookup relationship already exists on this child column. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7367](../../../foundations/error-codes.md#error-7367) | 400 | The lookup is used by one or more dependent views; removal blocked. |
| [7377](../../../foundations/error-codes.md#error-7377) | 400 | An identical lookup relationship (same child column → same reference column) is already defined. |
| [7378](../../../foundations/error-codes.md#error-7378) | 400 | No lookup relationship is defined on this column. |
| [7379](../../../foundations/error-codes.md#error-7379) | 400 | A lookup column cannot reference a column within the same table. |
| [7509](../../../foundations/error-codes.md#error-7509) | 400 | The reference column contains duplicate values; it must be unique to serve as the reference side. |

# Related

- [Data Modeling & Schema](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
