---
type: API Group
title: Auto Analysis
description: "APIs to automatically generate a curated set of views - charts, pivot tables and summary views - from an entire table or from a single column of it."
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - auto-analysis
  - api-group
api:
  domain: views-management
  group: auto-analysis
  endpoint_count: 2
  endpoints:
    - operation_id: autoAnalyseView
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/autoanalyse"
      doc: "/domains/views-management/auto-analysis/auto-analyse-view.md"
    - operation_id: autoAnalyseColumn
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/autoanalyse"
      doc: "/domains/views-management/auto-analysis/auto-analyse-column.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Auto Analysis APIs allow you to automatically generate a set of meaningful views (charts, pivots, summary views) from a table or a specific column within a table. The system examines the data in the source table, infers column roles (dimension vs. measure, geographic, etc.), and creates a curated collection of views — saving the effort of manually designing each view from scratch.

> **Supported source types:** Both APIs work only with **Tables**, **Query Tables**, and **Pipeline Tables**. Passing a chart, dashboard, pivot, or any other derived view type will fail with error **7397**.

---

APIs to automatically generate a curated set of views - charts, pivot tables and summary views - from an entire table or from a single column of it. Both APIs work only on Tables, Query Tables and Pipeline Tables.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Auto Analyse View](auto-analyse-view.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/autoanalyse` | `autoAnalyseView` | `ZohoAnalytics.modeling.create` | 200 |
| [Auto Analyse Column](auto-analyse-column.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/autoanalyse` | `autoAnalyseColumn` | `ZohoAnalytics.modeling.create` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# Operational Notes and Failure Cases

## Auto Analyse View vs Auto Analyse Column — Scope Comparison

| Aspect | Auto Analyse View | Auto Analyse Column |
|--------|-------------------|---------------------|
| **Input scope** | Entire table — all eligible columns are analysed together | Single specific column |
| **Tracks completion state?** | Yes — table is marked "analysed" after a successful run | No — always runs fresh, no state tracking |
| **Re-run guard** | `analyseAgain=true` required to overwrite existing auto-generated views | No guard needed; each call is independent |
| **View output** | A comprehensive set of views covering multiple column combinations | A focused set of views for the selected column only |
| **Best used when** | Getting a broad overview of all insights from a newly imported table | Exploring a specific column after data or schema changes |

## Edge Cases and Failure Scenarios

| Scenario | Behaviour |
|----------|-----------|
| Calling Auto Analyse View a second time without `analyseAgain=true` | Fails immediately with error **8116** — "Analysis already completed." The existing auto-generated views are not modified. |
| Setting `analyseAgain=true` on a table that has never been analysed | Permitted. The flag is treated as a no-op for the guard check and the analysis proceeds normally as a first-time run. |
| Table has only unsupported column types (all Auto-Number, URL, Multi-Line) | Auto Analyse View may complete with HTTP 200 but generate fewer or no views, depending on whether any eligible columns exist. No error is raised for empty results. |
| Passing a chart, pivot, dashboard, or any non-table view ID | Both APIs fail with error **7397** — "Not a valid table." The API is restricted exclusively to Tables, Query Tables, and Pipeline Tables. |
| Calling Auto Analyse Column on the same column multiple times | Each call succeeds independently. New views are created each time. If you want to avoid accumulation of duplicate views, delete the previously generated column views manually before re-running. |
| Query Table column that is disabled | Auto Analyse Column fails with error **14037**. The column must be enabled in the Query Table definition before it can be used for analysis. |
| Latitude column without a corresponding Longitude (or vice versa) | Auto Analyse Column fails. Both latitude and longitude must be present as a visible pair for a Geo Number column to be eligible for analysis. |
| Large table with many columns | Auto Analyse View may take longer than usual. The operation is synchronous — the HTTP response is returned only after all views are created. For very large tables, consider analysing individual high-priority columns using Auto Analyse Column for faster targeted results. |
| Auto analysis after importing new rows (same schema) | Schema has not changed, but data distribution may have changed. Run Auto Analyse View with `analyseAgain=true` to regenerate views that reflect the updated data. |
| Auto analysis after adding new columns to a table | Existing auto-generated views were created without knowledge of the new columns. Run Auto Analyse View with `analyseAgain=true` to include the new columns in the generated view set. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7107](../../../foundations/error-codes.md#error-7107) | 400 | The specified column does not exist in the table. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7397](../../../foundations/error-codes.md#error-7397) | 400 | The view is not a table. |
| [8116](../../../foundations/error-codes.md#error-8116) | 400 | Auto analysis has already been completed for this table and analyseAgain was not set to true. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |
| [14037](../../../foundations/error-codes.md#error-14037) | 400 | The column is disabled in its Query Table definition and cannot be used for analysis. |

# Related

- [Views Management](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
