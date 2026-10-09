---
type: API Endpoint
title: Create Export Job using View ID (Asynchronous)
description: Create an export job to initiate data export for the mentioned view asynchronously.
resource: "https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - async-data-export
  - get
  - data
api:
  operation_id: createExportJobViewId
  method: GET
  path: "/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data"
  domain: data-operations
  group: async-data-export
  oauth_scopes:
    - ZohoAnalytics.data.read
  org_id_header: required
  config_parameter:
    location: query
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Export permission on the view."
  error_codes:
    - 7104
    - 7301
    - 7327
    - 7330
    - 7331
    - 7332
    - 7333
    - 7543
    - 7565
    - 7801
    - 7803
    - 7824
    - 7827
    - 8001
    - 8014
    - 8015
    - 8017
    - 8088
    - 8119
    - 8125
    - 8126
    - 8127
    - 8128
    - 8132
    - 8188
    - 8241
    - 8507
    - 8535
    - 8547
  openapi:
    file: "/references/openapi/data-operations-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1bulk~1workspaces~1{workspace-id}~1views~1{view-id}~1data/get"
    config_schema: ExportJobConfigViewId
    response_schema: ExportJobCreationResponse
  sdk_examples: "/sdk-examples/data-operations/async-data-export/create-export-job-view-id.md"
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

**GET `/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data`** - Create Export Job using View ID (Asynchronous) (Asynchronous Data Export / Data Operations).

Creates an export job whose source is a saved view — including the view types the synchronous export refuses.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace that owns the view. |
| `<view-id>` | Long | ID of the view to export. Must belong to `<workspace-id>`. |

Unlike the synchronous export, **every** view type is accepted here: tables, tabular views, charts, pivots, summary views, query tables, dashboards, and views of live-connect workspaces, at any row count.

From the OpenAPI specification:

Create an export job to initiate data export for the mentioned view asynchronously. 

Workflow:
1. Create Export Job:
  - Call the Create Export Job API.
  - Receive a unique JOBID to track the export status.

2. Check Export Job Status:
  - Use the JOBID with the Get Export Job Details API.
  - Poll every few seconds to get the current JOBCODE.

   JOBCODEs and Meaning:
   - 1001: JOB NOT INITIATED
     → Export job acknowledged but not started. Retry after a short delay.
   - 1002: JOB IN PROGRESS
     → Export is currently being processed. Continue polling.
   - 1003: ERROR OCCURRED
     → An error occurred. Stop polling and investigate the error.
   - 1004: JOB COMPLETED
     → Export process completed. Proceed to download.
   - 1005: JOB NOT FOUND
     → Provided JOBID is invalid. Stop polling and verify the JOBID.

3. Download Exported Data:
  - Once JOBCODE is 1004, use the Download Exported Data API to download the exported file.

Limitations:
- Exported file will be available only for 1 hour after job completion.
- Maximum 5 concurrent export jobs are allowed per organization.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createExportJobViewId` |
| HTTP method | GET |
| URL | `/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.data.read`](../../../foundations/oauth-scopes.md#zohoanalyticsdataread) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Export permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - optional |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1bulk~1workspaces~1{workspace-id}~1views~1{view-id}~1data/get`; CONFIG schema `ExportJobConfigViewId`; response schema `ExportJobCreationResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.data.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

In addition to the [Shared CONFIG Attributes](overview.md#shared-config-attributes):

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `criteria` | String | No | — | Filter expression selecting the rows to export. Omit to export every row. See [`criteria` syntax](overview.md#criteria-syntax). |
| `applyDefaultUF` | Boolean | No | `false` | Applies the view's saved default user filters before exporting. Meaningful for tabular views. |
| `generateTOC` | Boolean | No | `false` | Generates a table of contents. **Dashboards only**, and only when `responseFormat` is `pdf`. |
| `dashboardLayout` | Integer | No | `1` | Page layout for a dashboard PDF. `0` each report on its own page, `1` the layout as it appears in the dashboard. **Dashboards only.** |
| `zoomFactor` | Integer | No | `100` | Rendering zoom for a dashboard PDF, `1`–`100`. **Dashboards only**; outside the range fails with `8119`. |

## Notes from the OpenAPI specification

This is a GET request, so the CONFIG value is sent as a query parameter. The JSONObject must be stringified and URL encoded before it is appended to the request URL.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | `"success"` on success. |
| `summary` | String | `"Create bulk export job"` — identical to the SQL query export, so the summary does not distinguish the two APIs. |
| `data` | Object | Job identification. |
| `data.jobId` | String | ID of the created job, **as a string**. |

# Examples

## Sample Requests

**Case 1 — `criteria` alone: export only the rows that match a filter**

```http
GET /restapi/v2/bulk/workspaces/466206000000071000/views/466206000000072000/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

```json
{
  "responseFormat": "csv",
  "criteria": "\"SalesTable\".\"Region\"='East'"
}
```

Every other attribute takes its default: comma-separated, DOS line endings, header row present, hidden columns included, personal-data columns excluded.

**Case 2 — a fully configured CSV job with a callback**

```json
{
  "responseFormat": "csv",
  "selectedColumns": ["Region", "Product", "Sales"],
  "delimiter": 1,
  "recordDelimiter": 1,
  "quoted": 1,
  "includeHeader": true,
  "includeRowNums": true,
  "showHiddenCols": false,
  "showPersonalCols": false,
  "applyDefaultUF": true,
  "password": "Zoho@123",
  "callbackUrl": "https://example.com/hooks/za-export"
}
```

**Case 3 — a dashboard as a PDF**

This is the case the synchronous export cannot serve at all.

```json
{
  "responseFormat": "pdf",
  "dashboardLayout": 1,
  "generateTOC": true,
  "zoomFactor": 100,
  "paperSize": 2,
  "paperStyle": "Landscape",
  "showTitle": 0,
  "showDesc": 0,
  "topMargin": 0.25,
  "bottomMargin": 0.25,
  "exportLanguage": 0
}
```

**Case 4 — a chart as an image**

```json
{
  "responseFormat": "image",
  "imageFormat": "png",
  "width": 1200,
  "height": 800,
  "title": true,
  "description": false,
  "legend": true
}
```

## Sample Responses

**HTTP 200 OK — the job was created**

```json
{
  "status": "success",
  "summary": "Create bulk export job",
  "data": {
    "jobId": "466206000000091000"
  }
}
```

**HTTP 400 Bad Request — a dashboard requested in a format it cannot produce**

```json
{
  "status": "failure",
  "summary": "INVALID_VALUE_FOR_ATTRIBUTE",
  "data": {
    "errorCode": 8119,
    "errorMessage": "Invalid value csv given for the attribute responseFormat. Allowed values are PDF and HTML."
  }
}
```

**HTTP 403 Forbidden — the caller lacks Export permission**

```json
{
  "status": "failure",
  "summary": "SECURITY_NOT_PERMITTED",
  "data": {
    "errorCode": 7301,
    "errorMessage": "You do not have the permission to perform this operation."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Export Job using View ID (Asynchronous)](../../../sdk-examples/data-operations/async-data-export/create-export-job-view-id.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **`CONFIG` is optional** | A bare call with no query string queues a CSV export of the whole view with default settings. |
| **No view type is off limits** | Dashboards, query tables, live-connect views, and tables of any size are all accepted. This is the reason to prefer this API over the synchronous export. |
| **A dashboard restricts the format** | Only `pdf` and `html` are valid for a dashboard; anything else fails with `8119`. |
| **A dashboard export may arrive as a ZIP** | An `html` dashboard export, and a `pdf` export of a **multi-tab** dashboard, are delivered as a ZIP archive containing one file per view or tab. Branch on the `Content-Type` returned by [Download Exported Data](download-exported-data.md). |
| **Dashboard PDFs use different paper defaults** | `paperSize` accepts `0`–`4` with default `2` (Tabloid), instead of `0`–`5` with default `4` (A4). |
| **`selectedColumns` is honoured only for tables and tabular views** | For charts, pivots, summary views, and dashboards it is accepted and ignored — the view's own layout decides what is exported. |
| **`selectedColumns` overrides `showHiddenCols` for the columns it names** | A hidden column listed explicitly is exported even when `showHiddenCols` is `false`. It also sets the column order. |
| **Validation happens before the job exists** | A bad `criteria`, an unmatched `selectedColumns` name, an unreachable `callbackUrl`, or a permission failure all produce an error response and **no** `jobId`. |
| **Creation success is not export success** | Failures while producing the file surface as `jobCode` `1003` on [Get Export Job Details](get-export-job-details.md), never on this response. |
| **`criteria` is not accepted by the SQL query variant** | And `sqlQuery` / `tableCriteriaList` are not accepted here. See [Filtering: `criteria` and `tableCriteriaList`](overview.md#filtering-criteria-and-tablecriterialist). |
| **Dependency chain:** | [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>`; [Get Columns](../../data-modeling-and-schema/columns/overview.md) → `selectedColumns` names → Create Export Job using View ID (Asynchronous) → `data.jobId` → [Get Export Job Details](get-export-job-details.md) → [Download Exported Data](download-exported-data.md). |

## Image specific

Applicable when `responseFormat` is `image`. Valid **only for chart views**; any other view type fails with [`8014`](../../../foundations/error-codes.md#error-8014).

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `imageFormat` | String | No | `"png"` | `"png"`, `"jpg"`, or `"jpeg"` (case-insensitive). Anything else fails with `8017`. |
| `width` | Integer | No | `500` | Image width in pixels, `250`–`2000`. Outside fails with `7803`. |
| `height` | Integer | No | `400` | Image height in pixels, `200`–`2000`. Outside fails with `7803`. |
| `title` | Boolean | No | `false` | Whether the chart title is drawn on the image. |
| `description` | Boolean | No | `false` | Whether the chart description is drawn on the image. |
| `legend` | Boolean | No | `true` | Whether the chart legend is drawn on the image. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — The view does not exist. | Verify `<view-id>` with [Get View List](../../views-management/view-operations/get-views.md). |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller lacks Export permission on the view, or the view does not belong to `<workspace-id>`. | Ensure the caller is an Account Admin, Organization Admin, Workspace Admin, or View Owner, or holds Export permission on the view. |
| [7327](../../../foundations/error-codes.md#error-7327) | 400 | `FILTER_CRITERIA_INVALID` — `criteria` parsed but could not be converted into a query. | Simplify the expression and check operator and value types. |
| [7330](../../../foundations/error-codes.md#error-7330) | 400 | `UNKNOWN_COLUMN_IN_FILTERCRITERIA` — A column named in `criteria` does not exist in the view. | Check the name against [Get Columns](../../data-modeling-and-schema/columns/overview.md). |
| [7331](../../../foundations/error-codes.md#error-7331) | 400 | `FILTERCRITERIA_PARSE_ERROR` — `criteria` is syntactically malformed. | Check quoting: double quotes around column names, single quotes around string literals. |
| [7332](../../../foundations/error-codes.md#error-7332) | 400 | `UNKNOWN_TABLE_IN_FILTERCRITERIA` — A table qualifier in `criteria` is not part of the view. | Qualify columns only with tables the view uses. |
| [7333](../../../foundations/error-codes.md#error-7333) | 400 | `INVALID_GROUP_FUNC_USE_IN_FILTERCRITERIA` — An aggregate function was used in `criteria`. | Filter on raw column values instead. |
| [7543](../../../foundations/error-codes.md#error-7543) | 400 | `ONLY_BASETABLE_COL_IN_TABULAR_FILTERCRITERIA` — `criteria` on a tabular view referenced a column outside its base table. | Filter using only the base table's own columns. |
| [7565](../../../foundations/error-codes.md#error-7565) | 400 | `UNVERIFIED_EMAIL` — The calling user's primary email address is not verified. | Verify the account's primary email address and retry. |
| [7801](../../../foundations/error-codes.md#error-7801) | 400 | `MARGIN_VALUE_EXCEEDS` — A PDF margin is outside `0`–`1` inches. | Send a value between `0` and `1`. |
| [7803](../../../foundations/error-codes.md#error-7803) | 400 | `INVALID_DIMENSION` — `width` or `height` is outside the permitted image range. | Use `width` 250–2000 and `height` 200–2000. |
| [7824](../../../foundations/error-codes.md#error-7824) | 400 | `EXPORT_REQ_BLOCKED` — Export has been blocked for this workspace. | Contact Zoho Analytics support using the address in the error message. |
| [7827](../../../foundations/error-codes.md#error-7827) | 400 | `EXP_PDF_RECORD_LIMIT` — The PDF exceeds 1,000,000 cells. | Narrow the export with `criteria` or `selectedColumns`. |
| [8001](../../../foundations/error-codes.md#error-8001) | 400 | `INVALID_RESP_FORMAT` — `responseFormat` is not a supported value. | Send one of `csv`, `json`, `xml`, `xls`, `pdf`, `html`, `image`. |
| [8014](../../../foundations/error-codes.md#error-8014) | 400 | `API_IMAGE_RESPONSE_NOT_POSSIBLE` — `image` was requested for a view that is not a chart. | Export charts as images; use `pdf` or `html` otherwise. |
| [8015](../../../foundations/error-codes.md#error-8015) | 400 | `API_EXPORT_COLUMN_NOT_PRESENT` — A name in `selectedColumns` does not match any column in the view. | Check the display names with [Get Columns](../../data-modeling-and-schema/columns/overview.md). |
| [8017](../../../foundations/error-codes.md#error-8017) | 400 | `INVALID_IMAGE_FORMAT` — `imageFormat` is not `png`, `jpg`, or `jpeg`. | Send one of the three supported values. |
| [8088](../../../foundations/error-codes.md#error-8088) | 400 | `SECURITY_CONTROLS_FEATURE_DISABLED` — Export is disabled for the organization. | Ask an Organization Admin to re-enable export. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE` — A numeric or enumerated attribute is outside its permitted set, or a dashboard was requested in a format other than PDF or HTML. | Correct the value; see [Enum Reference](overview.md#enum-reference). |
| [8125](../../../foundations/error-codes.md#error-8125) | 400 | `CALLBACKURL_NOT_VALID` — `callbackUrl` is malformed. | Send a well-formed absolute `http`/`https` URL. |
| [8126](../../../foundations/error-codes.md#error-8126) | 400 | `CALLBACKURL_CONNECTION_ERROR` — `callbackUrl` could not be reached during validation. | Make the endpoint publicly reachable before creating the job. |
| [8127](../../../foundations/error-codes.md#error-8127) | 400 | `CALLBACKURL_RESTRICTED` — `callbackUrl` resolves to a private or internal address. | Use a publicly routable host. |
| [8128](../../../foundations/error-codes.md#error-8128) | 400 | `INTERNAL_ERROR_ON_INITIATING_EXPORT` — The job could not be queued. | Retry; if it persists, contact support. |
| [8132](../../../foundations/error-codes.md#error-8132) | 400 | `ASYNC_EXPORT_LIMIT_EXCEEDED` — 5 export jobs are already queued or running for the organization. | Wait for an in-flight job to finish, then retry. |
| [8188](../../../foundations/error-codes.md#error-8188) | 400 | `EXPORT_INVALID_PASSWORD` — `password` is blank or shorter than 6 characters. | Send 6–256 characters. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | `SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION` — The view carries a restricted DATA_WARNING system tag. | Review the warning, then resend with `"validateSystemTags": false`. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | `MORE_THAN_MAX_LENGTH` — `CONFIG` exceeds 100,000 characters. | Shorten `criteria` or `selectedColumns`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.data.read`. |
| [8547](../../../foundations/error-codes.md#error-8547) | 400 | `ARRAY_SIZE_OUT_OF_RANGE` — `selectedColumns` is empty or holds more than 300 entries. | Send between 1 and 300 column names, or omit the attribute. |

# Related

- [Asynchronous Data Export overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Export Job using SQL Query (Asynchronous)](create-export-job-sql-query.md), [Get Export Job Details](get-export-job-details.md), [Download Exported Data](download-exported-data.md).
- [SDK examples](../../../sdk-examples/data-operations/async-data-export/create-export-job-view-id.md).
