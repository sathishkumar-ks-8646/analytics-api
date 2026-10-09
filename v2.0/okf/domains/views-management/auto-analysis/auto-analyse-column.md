---
type: API Endpoint
title: Auto Analyse Column
description: "Runs auto analysis on a single column of a table and creates a focused set of views for it - a category breakdown for a dimension column such as Region, or a trend over time for a date column such as Order Date."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/autoanalyse"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - auto-analysis
  - post
  - modeling
api:
  operation_id: autoAnalyseColumn
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/autoanalyse"
  domain: views-management
  group: auto-analysis
  oauth_scopes:
    - ZohoAnalytics.modeling.create
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Report permission on the workspace."
  error_codes:
    - 7103
    - 7104
    - 7107
    - 7301
    - 7319
    - 7397
    - 8116
    - 8535
    - 14037
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1columns~1{column-id}~1autoanalyse/post"
    config_schema: null
    response_schema: AutoAnalyseResponse
  sdk_examples: "/sdk-examples/views-management/auto-analysis/auto-analyse-column.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/autoanalyse`** - Auto Analyse Column (Auto Analysis / Views Management).

Triggers auto analysis for a **single column** of a table. The system generates targeted views specifically for the selected column — for example, a bar chart of sales by region if the column is "Region", or a trend chart over time if the column is a date. This is useful when you want focused visualisations for a specific column without regenerating the full set.

> **Why `analyseAgain` is NOT present here:**
> Unlike the full-table analysis, column-level analysis does not track whether it has been run before for a given column. Each call generates a new set of views for that column independently — there is no "already completed" guard at the column level. You can call this API multiple times on the same column (for example, after changing column data or for exploratory purposes) and it will always produce a fresh set of views. The `analyseAgain` concept does not apply because column analysis is designed to be repeatable without risk of unintended duplication of full-table views.

> This API has no CONFIG parameter.

From the OpenAPI specification:

Runs auto analysis on a single column of a table and creates a focused set of views for it - a category breakdown for a dimension column such as Region, or a trend over time for a date column such as Order Date.

Unlike the full-table Auto Analyse View API, this operation keeps no record of having been run, so there is no re-run guard and no `analyseAgain` attribute. Each call produces a fresh set of views for the column and may be repeated freely, which makes it suited to exploring one column after a data or schema change.

The API works on Tables, Query Tables and Pipeline Tables only, and not every column type is eligible.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `autoAnalyseColumn` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/autoanalyse` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organization ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Report permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1columns~1{column-id}~1autoanalyse/post`; response schema `AutoAnalyseResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |
| `{column-id}` | string | ID of the column. | [How to obtain](../../../foundations/identifiers.md#column-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- This API has no CONFIG parameter. The only inputs are the **workspace-id**, **view-id** and **column-id** path parameters, so no Content-Type header is required.
- Only Tables, Query Tables and Pipeline Tables can be analysed. Passing any other view type as **view-id** fails with error 7397.
- Column-level analysis keeps no completion state, so there is no equivalent of the **analyseAgain** guard used by the Auto Analyse View API. Every call runs fresh.
- Repeated calls on the same column each succeed and accumulate views. Delete the previously generated column views manually if the duplicates are not wanted.
- Not every column is eligible. Auto-Number, Multi-Line Text, URL and Geometry columns are unsupported, as are hidden columns and system columns such as the row ID. An ineligible column fails with error 8116.
- A column that has been disabled in a Query Table definition cannot be analysed and fails with error 14037. Enable it in the query table configuration first, or choose another column.
- A Geo Number latitude or longitude column is eligible only when both are present and visible as a pair. A lone latitude or longitude column cannot be analysed on its own.
- The views generated are targeted at the selected column - a category breakdown for a dimension column, a time series for a date column - rather than the comprehensive set produced by the Auto Analyse View API.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

# Examples

## Sample Requests

**Case 1 — Analyse a standard dimension column (e.g., "Region")**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000105001/columns/466206000000105020/autoanalyse HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded
```

**Case 2 — Analyse a date column (e.g., "Order Date") to generate time-series views**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000105001/columns/466206000000105025/autoanalyse HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded
```

**Case 3 — Analyse a column in a Query Table**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000115006/columns/466206000000115040/autoanalyse HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Column analysis completed (dimension column)**
```json
{
  "status": "success",
  "summary": "Auto Generate Reports",
  "data": {
    "status": "Reports generated successfully"
  }
}
```

**Case 2 — Column analysis completed (date column generating time-series charts)**
```json
{
  "status": "success",
  "summary": "Auto Generate Reports",
  "data": {
    "status": "Reports generated successfully"
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Auto Analyse Column](../../../sdk-examples/views-management/auto-analysis/auto-analyse-column.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

## Column Eligibility

Not all columns can be analysed. The following column types are **not supported** and will result in an error:

| Column Characteristic | Reason |
|-----------------------|--------|
| **Auto-Number columns** | These are system-generated sequential IDs with no analytical value. |
| **Multi-Line Text columns** | Free-form long text fields cannot be meaningfully aggregated or charted. |
| **URL columns** | URL strings are not suitable for axis-based analysis. |
| **Geometry columns** | Raw geometry fields require special spatial processing and are not handled by auto analysis. |
| **Hidden columns** | Columns marked as not visible in the table are excluded from analysis. |
| **System columns** (e.g., row ID) | Internal system-managed columns are excluded. |
| **Disabled columns in Query Tables** | Columns that have been disabled in a Query Table definition are not available for analysis. |
| **Standalone Geo Number columns (latitude or longitude without its pair)** | Latitude/Longitude columns must both be present and visible as a pair. A lone latitude or longitude column cannot be analysed independently. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | View (table) not found. | Verify `<view-id>` exists in the workspace. |
| [7107](../../../foundations/error-codes.md#error-7107) | 400 | Column not found in the specified table. | Verify `<column-id>` belongs to the table identified by `<view-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have Create Report permission on the workspace. | Ensure the user is a Workspace Admin, Account Admin, Organization Admin, or has been granted Create Report permission on this workspace. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | View does not belong to the specified workspace. | Verify both `<workspace-id>` and `<view-id>` are consistent. |
| [7397](../../../foundations/error-codes.md#error-7397) | 400 | The view is not a Table, Query Table, or Pipeline Table. | Auto analysis only works on base table types. Pass a valid table view ID. |
| [8116](../../../foundations/error-codes.md#error-8116) | 400 | The selected column type is not supported for auto analysis (e.g., Auto-Number, Multi-Line, URL, Geometry, or a system/hidden column). | Choose an eligible column. Refer to the Column Eligibility section for the full list of unsupported column characteristics. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |
| [14037](../../../foundations/error-codes.md#error-14037) | 400 | The column is disabled in its Query Table definition and cannot be used for analysis. | Enable the column in the Query Table configuration or choose a different column. |

# Related

- [Auto Analysis overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Auto Analyse View](auto-analyse-view.md).
- [SDK examples](../../../sdk-examples/views-management/auto-analysis/auto-analyse-column.md).
