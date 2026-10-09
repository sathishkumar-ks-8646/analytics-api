---
type: API Group
title: Reports (Analysis Views)
description: "APIs for creating, updating and reading the metadata of analysis views (charts, pivot tables and summary views) inside a workspace."
tags:
  - zoho-analytics
  - rest-api-v2
  - reports-and-dashboards
  - reports
  - api-group
api:
  domain: reports-and-dashboards
  group: reports
  endpoint_count: 3
  endpoints:
    - operation_id: createReport
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/reports"
      doc: "/domains/reports-and-dashboards/reports/create-report.md"
    - operation_id: updateReport
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/reports/{view-id}"
      doc: "/domains/reports-and-dashboards/reports/update-report.md"
    - operation_id: getReportMetadata
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata"
      doc: "/domains/reports-and-dashboards/reports/get-report-metadata.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

This document describes the V2 **Reports (Analysis View)** REST APIs of Zoho Analytics.

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`).
> - The `ZANALYTICS-ORGID` header is **mandatory**.
> - `ZohoAnalytics_Server_URI` depends on the data center (`analyticsapi.zoho.com`, `.eu`, etc.).
> - The `CONFIG` parameter (for POST/PUT) must be sent as a URL-encoded JSON string in the request body.
> - `reportType` must be one of `chart`, `pivot`, or `summary`.

---

APIs for creating, updating and reading the metadata of analysis views (charts, pivot tables and summary views) inside a workspace.

An analysis view is always built on top of a base table in the same workspace. Its whole definition - report type, chart sub-type, axis columns, filters, user filters, drill actions and display settings - travels in a single `CONFIG` JSON parameter that is shared, field for field, by all three APIs in this module.

## Common request conventions

| Header | Value | Required |
|---|---|---|
| `Authorization` | `Zoho-oauthtoken <oauth-token>` | Mandatory |
| `ZANALYTICS-ORGID` | Organization ID owning the workspace | Mandatory |
| `Content-Type` | `application/x-www-form-urlencoded` | POST and PUT only |

For Create and Update, `CONFIG` is a URL encoded JSON string sent as a form field named `CONFIG`. Get Report Metadata takes no `CONFIG` at all - every input is a URL path parameter.

A `workspaceKey` in the format `orgid/workspacename` may be used in place of the numeric workspace ID in the URL path.

`CONFIG` has a maximum serialized size of 10 MB for both Create and Update. The nested arrays `axisColumns`, `mergeAxisInfo`, `filters` and `userFilters` are the ones that realistically approach it.

## OAuth scopes

| API | Method | Scope |
|---|---|---|
| Create Analysis View | POST | `ZohoAnalytics.modeling.create` |
| Update Analysis View | PUT | `ZohoAnalytics.modeling.update` |
| Get Report Metadata | GET | `ZohoAnalytics.modeling.read` |

## Response envelope

Every response follows the standard Zoho Analytics V2 envelope.

**Update Analysis View returns a bare HTTP 204 No Content on success** - there is no JSON body to parse. Create Analysis View and Get Report Metadata return the envelope below; every API returns it on failure.

- **status** - `success` or `failure`. Present in the JSON success responses of Create Analysis View and Get Report Metadata, and in every failure response.
- **summary** - human readable message describing the result. Present only in the JSON success responses of Create Analysis View and Get Report Metadata.
- **data.viewId** - Create only. The ID of the newly created analysis view; use it in the URL of later Update and Get Report Metadata calls.
- **data.reportConfig** - Get Report Metadata only. The full stored configuration of the view.
- **errorCode** and **errorMessage** - failure only.

## Update is a reset, not a patch

Update Analysis View replaces the whole configuration. Every axis column, filter, user filter and settings entry is overwritten with what was sent, fields that are omitted revert to their empty defaults, and `description` is cleared if it is left out. Always fetch, modify, then write back the complete configuration.

**Read-modify-write**

1. `GET /restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata` and take `data.reportConfig`.
2. Change only what needs to change - for example `chartType` from `bar` to `line`, or appending one entry to `axisColumns`. Carry the full `axisColumns`, `filters` and `userFilters` arrays through; anything dropped here is permanently removed from the view.
3. `PUT` the complete modified object back as `CONFIG`.

**Cloning a view**

`data.reportConfig` is structurally identical to the Create `CONFIG`, so it doubles as a clone template. Give the clone a `title` that is unique in the workspace, keep `baseTableName`, and add `folderId` only if the copy belongs somewhere other than the default folder. When cloning across workspaces, every `columnName` and `tableName` in `axisColumns` must exist in the target workspace's base table.

## Fields that behave unexpectedly on Update

| Field | Behaviour | Recommendation |
|---|---|---|
| `title` | Silently ignored; the existing display name is always preserved. There is no V2 field to rename a view through Update. | Send it for clarity if you like, knowing it does nothing. |
| `reportType` | Cannot be changed. A value that does not match the existing view type fails with error 8021. | Carry it unchanged from the Get Report Metadata response. |
| `folderId` | If it differs from the view's current folder the request fails. The same value is a harmless no-op. | Omit it. It is not returned by Get Report Metadata, so it is naturally absent when the response is used as the base. |
| `description` | Read from the CONFIG on every write. If absent it is set to null, clearing it. | Copy it from the Get Report Metadata response. |
| `baseTableName` | Derived from the view's stored parent reference, not from the CONFIG. | Harmless to include; it has no effect. |
| `axisColumns`, `filters`, `userFilters` | Fully replaced. Omitting them removes everything. | Send the full arrays unless the intent is to clear them. |
| `mergeAxisInfo` | Required whenever `isAxisMerge` is true. | Omit both when axis merge is off. |

## Axis type casing

The request samples use camelCase (`xAxis`, `yAxis`, `colorAxis`) while Get Report Metadata returns lowercase (`xaxis`, `yaxis`, `coloraxis`, `sizeaxis`, `textaxis`, `groupby`, `summarize`). The lowercase forms are documented as canonical. When building a `CONFIG` from a metadata response, copy the `type` values verbatim rather than re-casing them.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Create Analysis View](create-report.md) | POST | `/restapi/v2/workspaces/{workspace-id}/reports` | `createReport` | `ZohoAnalytics.modeling.create` | 200 |
| [Update Analysis View](update-report.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}` | `updateReport` | `ZohoAnalytics.modeling.update` | 204 |
| [Get Report Metadata](get-report-metadata.md) | GET | `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata` | `getReportMetadata` | `ZohoAnalytics.modeling.read` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# Response Payload Notes

| Field | Description |
|-------|-------------|
| `status` | `success` or `failure`. Present in JSON success responses for Create Analysis View and Get Report Metadata, and in JSON failure responses. Update Analysis View success returns no body. |
| `summary` | Human-readable message describing the result of the operation. Present only in JSON success responses for Create Analysis View and Get Report Metadata. |
| `data.viewId` | (Create only) The ID of the newly created analysis view. Use this ID in subsequent API calls (e.g., Update Analysis View, Get Report Metadata). |
| `data.reportConfig` | (Get Report Metadata only) The full configuration object of the retrieved analysis view. |
| `errorCode` | (Failure only) Numeric error code identifying the failure reason. |
| `errorMessage` | (Failure only) Human-readable description of the error. |

> **Note:** The `CONFIG` parameter has a maximum serialized size of **10 MB** for both Create and Update Analysis View APIs. Ensure that nested arrays (`axisColumns`, `mergeAxisInfo`, `filters`, `userFilters`) do not cause the total CONFIG payload to exceed this limit.

---

# Working with Get, Create, and Update Together

## Why Get Report Metadata Before Update

The **Update Analysis View** API performs a **full configuration reset** — not a patch. The method is named `analysisViewResetAndUpdate` internally. When you PUT a CONFIG:

- Every axis column, filter, user filter, and settings entry is **completely replaced** with the new values.
- **`description`** is replaced (or cleared if omitted).
- Fields not provided (e.g., `axisColumns`) revert to their empty defaults.

To avoid losing existing configuration, always **fetch first, modify, then update**.

---

## Workflow 1 — Read-Modify-Write (Safe Update)

Use Get Report Metadata to retrieve the full current state of the view, make targeted changes, then PUT the complete modified config.

**Step 1: Fetch the current full config**

```http
GET /restapi/v2/workspaces/466206000000071000/reports/466206000000105001/metadata HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

Response (`data.reportConfig`):

```json
{
  "title": "Monthly Sales",
  "description": "Rolling 12-month trend",
  "reportType": "chart",
  "chartType": "bar",
  "baseTableName": "Sales",
  "isAxisMerge": false,
  "axisColumns": [
    { "type": "xAxis", "columnName": "Month", "tableName": "Sales", "operation": "actual" },
    { "type": "yAxis", "columnName": "Revenue", "tableName": "Sales", "operation": "sum" }
  ],
  "filters": [],
  "userFilters": []
}
```

**Step 2: Modify only what you need**

For example, change the chart type from `bar` to `line` and add a colour axis:

```json
{
  "reportType": "chart",
  "description": "Rolling 12-month trend",
  "chartType": "line",
  "baseTableName": "Sales",
  "isAxisMerge": false,
  "axisColumns": [
    { "type": "xAxis", "columnName": "Month", "tableName": "Sales", "operation": "actual" },
    { "type": "yAxis", "columnName": "Revenue", "tableName": "Sales", "operation": "sum" },
    { "type": "colorAxis", "columnName": "Region", "tableName": "Sales", "operation": "actual" }
  ],
  "filters": [],
  "userFilters": []
}
```

> Always carry the full `axisColumns` array — only the columns you send are stored. Any column removed here is permanently deleted from the view.

**Step 3: PUT the complete modified config**

```http
PUT /restapi/v2/workspaces/466206000000071000/reports/466206000000105001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"reportType":"chart","description":"Rolling 12-month trend","chartType":"line","baseTableName":"Sales","isAxisMerge":false,"axisColumns":[{"type":"xAxis","columnName":"Month","tableName":"Sales","operation":"actual"},{"type":"yAxis","columnName":"Revenue","tableName":"Sales","operation":"sum"},{"type":"colorAxis","columnName":"Region","tableName":"Sales","operation":"actual"}],"filters":[],"userFilters":[]}
```

---

## Workflow 2 — Cloning a Report (Get → Create)

The `reportConfig` returned by Get Report Metadata is structurally identical to the Create CONFIG. Use it as a template for a new view.

**Step 1: Fetch full metadata of the source view**

```http
GET /restapi/v2/workspaces/466206000000071000/reports/466206000000105001/metadata
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Step 2: Prepare the Create CONFIG from the response**

Take `data.reportConfig` and:
- **Change `title`** — required, must be unique in the workspace.
- **Keep `baseTableName`** — required for Create.
- Keep `reportType`, `chartType`, `axisColumns`, `filters`, `userFilters`, `settings`, `isAxisMerge`, `mergeAxisInfo` as-is.
- **Omit `folderId`** from the response if you want the view in the default folder, or add it to place the clone in a specific folder.

**Step 3: POST to Create**

```http
POST /restapi/v2/workspaces/466206000000071000/reports HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"title":"Monthly Sales - Copy","reportType":"chart","chartType":"bar","baseTableName":"Sales","isAxisMerge":false,"axisColumns":[{"type":"xAxis","columnName":"Month","tableName":"Sales","operation":"actual"},{"type":"yAxis","columnName":"Revenue","tableName":"Sales","operation":"sum"}],"filters":[],"userFilters":[]}
```

---

## Special Cases and Caveats

| Case | Behaviour | Recommendation |
|------|-----------|----------------|
| **`title` is read-only on Update** | Any `title` value in the Update CONFIG is silently ignored — the existing display name is always preserved. There is no V2 API field to rename a view via Update. | Include `title` from the GET response for documentation/clarity, knowing it has no effect. To rename, use a dedicated view rename operation. |
| **`reportType` cannot be changed** | If the `reportType` in Update CONFIG does not match the existing view's type (chart/pivot/summary), the request fails with error `8021`. | Always carry `reportType` unchanged from the GET response when updating an existing view. |
| **`folderId` on Update** | If `folderId` is provided and **differs** from the current folder, the request throws `FOLDERID_CANNOT_BE_UPDATED`. If the same value is provided, it is a harmless no-op. | Omit `folderId` from the Update CONFIG entirely. `folderId` is not returned in the GET response, so it will naturally be absent if you use the GET response as your base. |
| **`description` is cleared if omitted** | `description` is read from the JSON input in both Create and Update paths. If absent from the Update CONFIG, the description is set to `null` (effectively cleared). | Always copy `description` from the GET response into your Update CONFIG to preserve it. |
| **`baseTableName` is ignored on Update** | The base table is derived from the existing view's stored parent reference — not from the CONFIG. Including `baseTableName` from the GET response is harmless but has no effect. | You may include it for consistency, but know it does nothing on Update. |
| **Axis type names are camelCase** | The GET response returns axis types in the same camelCase form the Create and Update CONFIG accept: `xAxis`, `yAxis`, `colorAxis`, `textAxis`, `sizeAxis`, `groupBy`, `summarize`. | Copy axis `type` values verbatim from the GET response when constructing Create or Update CONFIG to avoid mismatch errors. |
| **Full axis reset** | On Update, the entire `axisColumns` array is replaced. Any axis column not in the new array is permanently removed from the view. | Fetch all current axis columns via GET, apply changes, and PUT the full updated array. |
| **Filters and user filters** | Like axis columns, `filters` and `userFilters` are fully replaced. Omitting them from the Update CONFIG removes all filters. | Include the full arrays from the GET response unless intentionally clearing them. |
| **`mergeAxisInfo` with `isAxisMerge`** | If `isAxisMerge` is `true`, `mergeAxisInfo` must also be provided. The GET response includes `mergeAxisInfo` when axis merge is active — use it as-is for Update. | When `isAxisMerge` is `false`, omit `mergeAxisInfo` entirely. |
| **Cross-workspace clone** | When cloning, `columnName` and `tableName` in `axisColumns` must match columns that exist in the **target workspace's** base table. | Verify column availability in the target workspace before POST. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | A view with the given viewName already exists in this workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [8021](../../../foundations/error-codes.md#error-8021) | 400 | Invalid view type specified. |
| [8050](../../../foundations/error-codes.md#error-8050) | 400 | Invalid value provided. |
| [8075](../../../foundations/error-codes.md#error-8075) | 400 | Invalid chart type parameter. |
| [8100](../../../foundations/error-codes.md#error-8100) | 400 | Operation not supported for this analysis view widget. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | Invalid value for attribute. |
| [8252](../../../foundations/error-codes.md#error-8252) | 400 | Invalid report type. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |

# Related

- [Reports & Dashboards](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
