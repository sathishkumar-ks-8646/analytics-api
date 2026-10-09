---
type: API Group
title: Row Operations
description: "APIs for adding, updating, and deleting rows in a view."
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - row-operations
  - api-group
api:
  domain: data-operations
  group: row-operations
  endpoint_count: 3
  endpoints:
    - operation_id: addRow
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows"
      doc: "/domains/data-operations/row-operations/add-row.md"
    - operation_id: updateRows
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows"
      doc: "/domains/data-operations/row-operations/update-rows.md"
    - operation_id: deleteRows
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows"
      doc: "/domains/data-operations/row-operations/delete-rows.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-operations-grouped-api.json"
    title: OpenAPI 3 specification - data-operations-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

This document covers the V2 **Row** REST APIs of Zoho Analytics — the APIs that insert, update, and delete individual rows of data in a table.

APIs for adding, updating, and deleting rows in a view.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Add Row](add-row.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows` | `addRow` | `ZohoAnalytics.data.create` | 200 |
| [Update Row](update-rows.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows` | `updateRows` | `ZohoAnalytics.data.update` | 200 |
| [Delete Row](delete-rows.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows` | `deleteRows` | `ZohoAnalytics.data.delete` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What are the "Row" APIs?

The three Row APIs are the record-level write path into a Zoho Analytics table. They all address the same URL (`/workspaces/<workspace-id>/views/<view-id>/rows`) and differ only by HTTP method:

| Operation | Method | Scope of the change |
|-----------|--------|---------------------|
| [Add Row](add-row.md) | POST | Inserts exactly **one** row per call. |
| [Update Row](update-rows.md) | PUT | Updates **every row matching `criteria`**, or all rows when `updateAllRows` is `true`. Can insert instead when nothing matches. |
| [Delete Row](delete-rows.md) | DELETE | Deletes **every row matching `criteria`**, or all rows when `deleteAllRows` is `true`. |

They operate strictly on **tables**. A report, dashboard, query table, or any other view type is rejected with [`7137`](../../../foundations/error-codes.md#error-7137). For loading many rows at once, use the Data Import APIs rather than looping over Add Row.

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`). All three use the **`data`** scope family — see [OAuth scopes](../../../foundations/oauth-scopes.md).
> - All three are **view-scoped** and require the `ZANALYTICS-ORGID` header.
> - `ZohoAnalytics_Server_URI` depends on the data centre (`analyticsapi.zoho.com`, `analyticsapi.zoho.eu`, etc.).
> - All three are **available in Client Portal / White Label contexts**.
> - `CONFIG` is **mandatory** for all three and is sent as a URL-encoded form parameter.
> - `criteria` and all column names/values are treated as sensitive and are excluded from request logging.
> - **All values are exchanged as strings.** Numeric, boolean, and date column values are sent as JSON strings and are echoed back as strings — see [General Response Payload Notes](overview.md#general-response-payload-notes).

---

# Table Preconditions

Before any row operation runs, the target view is checked. These conditions apply to all three APIs unless noted:

| Condition | Applies to | Error |
|-----------|-----------|-------|
| The view must be a **table**, not a report/dashboard/query table | All three | `7137` |
| The table must **not** be a stream table | Add Row, Update Row | `101021` |
| The table must **not** be a snapshot table | All three | `7165` |
| The table must **not** be a system table | Add Row, Update Row | `7164` |
| DML must be allowed on the table | All three | `7405` |
| No batch import may be holding a DDL lock on the table | All three | `7092` |

---

# `criteria` Syntax

`criteria` is a SQL-like filter expression that selects the rows to update or delete. Column names are quoted with double quotes and string literals with single quotes:

```
"Region"='East'
"SalesTable"."Region"='East'
"Sales">1000 and "Region"='West'
```

Notes that matter in practice:

- A column named in `criteria` must exist in the table, otherwise the request fails with [`7330`](../../../foundations/error-codes.md#error-7330).
- For a **shared user**, the share filter criteria configured for that user is automatically ANDed with whatever `criteria` is sent. A shared user therefore can never update or delete rows outside their own slice of the table, even with a broad criteria.
- `criteria` is not accepted by [Add Row](add-row.md) — a row insert has nothing to filter.

---

# API-Specific Notes and Behaviours

## Add Row

- **Single-row only, and that is its main limitation.** There is no batch variant, so bulk loading through this API means one HTTP call and one API unit per row. Use the Data Import APIs for anything beyond a handful of rows.
- **Unknown column names fail silently by design.** They are collected into `invalidColumns` and the row is still inserted from whatever did match. A caller that ignores `invalidColumns` can write partial rows for a long time without noticing — always assert it is `{}`.
- **The floor is one matching column.** Only when *nothing* matches does the call fail ([`8016`](../../../foundations/error-codes.md#error-8016)).
- **Case-insensitive in, as-sent out.** Matching ignores case, but `addedColumns` echoes the casing you supplied rather than the table's, so it cannot be used to discover canonical column names.
- **Date handling has a three-level precedence**: `columnDateFormat` for that column, then `dateFormat`, then the column's own configured format.
- **It is the only Row API with no `criteria`**, and correspondingly the only one that cannot be constrained by a shared user's share filter.
- **Dependency chain:** [Get View List](../../views-management/view-operations/get-views.md) → [Get Columns](../../data-modeling-and-schema/columns/overview.md) → Add Row.

## Update Row

- **Two mutually exclusive selectors, one of which is mandatory.** `criteria` and `updateAllRows` cannot be combined, and omitting both is an error rather than a default — the API deliberately refuses to guess between "one row" and "every row".
- **`addIfNotExist` changes both the permission requirement and the response shape.** It needs Add Row permission on top of Update Row, and on firing it returns `newRowAdded: true` with the values under `updatedColumns` and `updatedRows: 0`. Code that keys off `addedColumns` will miss the insert entirely.
- **The upsert inserts, it does not merge.** Only the columns present in `columns` are written; there is no partially-matched row to fill in the rest.
- **`updatedRows: 0` is ambiguous on its own.** It means either "criteria matched nothing" or "a row was inserted instead" — distinguish them by the presence of `newRowAdded`.
- **Shared users see silently reduced effects**, because their share filter criteria is ANDed with the criteria they send.
- **Dependency chain:** [Get View List](../../views-management/view-operations/get-views.md) → [Get Columns](../../data-modeling-and-schema/columns/overview.md) → Update Row.

## Delete Row

- **Its permission does not match its name.** The API validates **Delete All Rows**, not Delete Row, regardless of how narrow the `criteria` is. This is the single most surprising behaviour in the family and the most common cause of an unexpected [`7301`](../../../foundations/error-codes.md#error-7301) for a shared user who was granted row-level delete.
- **Two mutually exclusive selectors, one mandatory** — same contract as Update Row, with its own error code ([`8131`](../../../foundations/error-codes.md#error-8131)).
- **Irreversible and potentially total.** `deleteAllRows: true` empties the table in one call with no confirmation step and no row-level trash.
- **It skips the stream-table check** that Add Row and Update Row perform, so [`101021`](../../../foundations/error-codes.md#error-101021) is the one precondition error that cannot occur here.
- **Shared users cannot over-delete.** Even `deleteAllRows: true` is confined to their share filter criteria, so the same request removes different amounts of data depending on who calls it.
- **The narrowest response in the family** — `deletedRows` and nothing else.
- **Dependency chain:** [Get View List](../../views-management/view-operations/get-views.md) → [Get Columns](../../data-modeling-and-schema/columns/overview.md) → Delete Row.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **All three APIs return HTTP 200 with a body** | Unusually for the V2 suite, none of the Row APIs returns 204 — even `DELETE` responds with `{"status", "summary", "data"}` carrying a row count. |
| **Failure responses share one shape** | `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name (e.g. `NOT_A_TABLE`), not a localised sentence. |
| **Column values are strings in both directions** | Send `"Sales": "1000"`, not `1000`; numeric, boolean, and date columns all come back as strings (`"3"`, `"true"`, `"01-Jan-2026"`). Convert on your side. |
| **Row counts are native numbers** | `updatedRows` and `deletedRows` are genuine JSON numbers, in contrast to the string-typed column values around them. |
| **A count of `0` is a success** | Both `updatedRows: 0` and `deletedRows: 0` are returned with HTTP 200 when the criteria matched nothing. Never infer failure from the status code alone. |
| **`invalidColumns` is always present on Add and Update** | Empty `{}` when every supplied name matched. It is never returned by Delete Row, which takes no `columns`. |
| **`newRowAdded` is conditionally present** | It appears only on an [Update Row](update-rows.md) call where `addIfNotExist` triggered an insert, and is then always `true`. Test for the key, not for a `false` value. |
| **Response field names differ per operation** | Insert returns `addedColumns`; update returns `updatedColumns` + `updatedRows`; an `addIfNotExist` insert returns `updatedColumns` + `updatedRows: 0` + `newRowAdded`; delete returns `deletedRows`. There is no single common data shape across the three. |
| **No row identifiers are returned** | None of the three responses includes a row ID, primary key, or row number — only the values applied and the counts affected. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7092](../../../foundations/error-codes.md#error-7092) | 400 | A DDL lock is active on the table. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7137](../../../foundations/error-codes.md#error-7137) | 400 | The target view is not a table. |
| [7164](../../../foundations/error-codes.md#error-7164) | 400 | The table is a snapshot table and its columns cannot be renamed. |
| [7165](../../../foundations/error-codes.md#error-7165) | 400 | Snapshot table data cannot be modified. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7330](../../../foundations/error-codes.md#error-7330) | 400 | A column named in criteria does not exist in the view. |
| [7405](../../../foundations/error-codes.md#error-7405) | 400 | Row modification is not allowed for this table. |
| [7512](../../../foundations/error-codes.md#error-7512) | 400 | A date pattern could not be parsed. |
| [7515](../../../foundations/error-codes.md#error-7515) | 400 | A value for a lookup column does not exist in the parent table. |
| [8016](../../../foundations/error-codes.md#error-8016) | 400 | None of the supplied column names matched a column in the table. |
| [8062](../../../foundations/error-codes.md#error-8062) | 400 | withCustomDomain is true but no custom domain is configured for this workspace. |
| [8130](../../../foundations/error-codes.md#error-8130) | 400 | Both criteria and updateAllRows were sent, or neither was. |
| [8131](../../../foundations/error-codes.md#error-8131) | 400 | Both criteria and deleteAllRows were sent, or neither was. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | CONFIG was not sent. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |
| [101021](../../../foundations/error-codes.md#error-101021) | 400 | Row operations are not supported on a stream table. |

# Related

- [Data Operations](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
