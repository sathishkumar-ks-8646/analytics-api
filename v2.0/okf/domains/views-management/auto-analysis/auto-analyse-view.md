---
type: API Endpoint
title: Auto Analyse View
description: Runs auto analysis on an entire table.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/autoanalyse"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - auto-analysis
  - post
  - modeling
api:
  operation_id: autoAnalyseView
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/autoanalyse"
  domain: views-management
  group: auto-analysis
  oauth_scopes:
    - ZohoAnalytics.modeling.create
  org_id_header: required
  config_parameter:
    location: form
    required: false
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Report permission on the workspace."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 7319
    - 7397
    - 8116
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1autoanalyse/post"
    config_schema: AutoAnalyseViewConfig
    response_schema: AutoAnalyseResponse
  sdk_examples: "/sdk-examples/views-management/auto-analysis/auto-analyse-view.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/autoanalyse`** - Auto Analyse View (Auto Analysis / Views Management).

Triggers auto analysis on an entire table. The system scans **all columns** of the table, determines the best ways to visualise the data, and creates a set of views (charts, pivots, summaries) directly in the workspace. This is the full-table equivalent of asking "what can you show me from this data?"

The operation tracks completion state — once auto analysis has been run successfully on a table, a repeat call without `analyseAgain=true` will be rejected. This prevents unintended duplication of auto-generated views.

> **Why `analyseAgain` is necessary here:**
> After a successful run, the table is marked internally as "auto analysis completed." Calling this API again (e.g., after new data or new columns are added) without explicitly confirming intent will fail. Setting `analyseAgain=true` signals that you are intentionally re-running the analysis — all previously auto-generated views for this table are **replaced** by the new set. This guard prevents accidental duplication of views when the API is called multiple times.

From the OpenAPI specification:

Runs auto analysis on an entire table. Every column is scanned, the role of each is inferred - dimension or measure, geographic, temporal - and a curated set of views is created directly in the workspace.

The operation tracks its own completion state. Once a table has been analysed successfully it is marked internally as analysed, and a second call is rejected with error 8116 unless `analyseAgain` is set to `true`. That guard exists to stop auto-generated views being duplicated by an accidental repeat call; setting the flag signals deliberate intent, and the previous set of views is then replaced rather than added to.

The API works on Tables, Query Tables and Pipeline Tables only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `autoAnalyseView` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/autoanalyse` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organization ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Report permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - optional |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1autoanalyse/post`; CONFIG schema `AutoAnalyseViewConfig`; response schema `AutoAnalyseResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameter

The CONFIG parameter is optional. When provided, it is a JSON object sent as a form-encoded body parameter named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `analyseAgain` | Boolean | No | `false` | Controls whether auto analysis can re-run on a table that has already been analysed. When `false` (default): if the table already has auto-generated views from a previous run, the request fails with error **8116** — protecting against accidental duplication. When `true`: the previous auto-generated views are discarded and a fresh analysis is performed, creating a new set of views based on the current state of the table data and schema. Set this to `true` after adding new columns or importing significantly different data. |

## Notes from the OpenAPI specification

- The CONFIG parameter is optional. When it is omitted, **analyseAgain** is taken as false.
- Only Tables, Query Tables and Pipeline Tables can be analysed. Passing a chart, pivot table, summary view, dashboard or any other derived view fails with error 7397.
- The table is marked internally as analysed after a successful run. Calling the API again without **analyseAgain** as true fails with error 8116, and the views already generated are left untouched.
- With **analyseAgain** as true, the previously auto-generated views of the table are discarded and replaced by a fresh set built from the current data and schema. The flag does not add views alongside the old ones.
- Sending **analyseAgain** as true on a table that has never been analysed is permitted. The guard check treats it as a no-op and the call proceeds as a first-time run.
- Re-run with **analyseAgain** as true after adding columns, since the existing views were generated without knowledge of them, and after importing significantly different data, since the distribution those views were built for has changed.
- A table whose columns are all ineligible may still return HTTP 200 while generating few views or none. An empty result is not treated as an error.
- The operation is synchronous - the response is returned only after every view has been created - so a table with many columns can take a while. For a faster targeted result, use the Auto Analyse Column API on the columns that matter most.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

# Examples

## Sample Requests

**Case 1 — First-time analysis on a table (no CONFIG needed)**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000105001/autoanalyse HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded
```

**Case 2 — Re-run analysis after new columns were added to the table**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000105001/autoanalyse HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"analyseAgain":true}
```

**Case 3 — Re-run analysis on a Query Table after its SQL was modified**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000115006/autoanalyse HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"analyseAgain":true}
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — First-time analysis completed successfully**
```json
{
  "status": "success",
  "summary": "Auto Generate Reports",
  "data": {
    "status": "Reports generated successfully"
  }
}
```

**Case 2 — Re-analysis with `analyseAgain=true` completed successfully**
```json
{
  "status": "success",
  "summary": "Auto Generate Reports",
  "data": {
    "status": "Reports generated successfully"
  }
}
```

> **Note:** Both cases return the same response body. The difference is purely in the request: Case 2 replaces the old set of auto-generated views, while Case 1 creates them for the first time.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Auto Analyse View](../../../sdk-examples/views-management/auto-analysis/auto-analyse-view.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | View (table) not found. | Verify `<view-id>` exists in the workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have Create Report permission on the workspace. | Ensure the user is a Workspace Admin, Account Admin, Organization Admin, or has been granted Create Report permission on this workspace. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | View does not belong to the specified workspace. | Verify both `<workspace-id>` and `<view-id>` are consistent. |
| [7397](../../../foundations/error-codes.md#error-7397) | 400 | The view is not a Table, Query Table, or Pipeline Table. | Auto analysis only works on base table types. Pass a valid table view ID. |
| [8116](../../../foundations/error-codes.md#error-8116) | 400 | Auto analysis has already been completed for this table and `analyseAgain` was not set to `true`. | Pass `CONFIG={"analyseAgain":true}` to re-run the analysis and replace previously generated views. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |

# Related

- [Auto Analysis overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Auto Analyse Column](auto-analyse-column.md).
- [SDK examples](../../../sdk-examples/views-management/auto-analysis/auto-analyse-view.md).
