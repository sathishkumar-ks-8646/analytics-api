---
type: API Endpoint
title: Create Export Job using SQL Query (Asynchronous)
description: Create an export job using an SQL SELECT statement to initiate data export asynchronously.
resource: "https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/{workspace-id}/data"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - async-data-export
  - get
  - data
api:
  operation_id: createExportJobSQLQuery
  method: GET
  path: "/restapi/v2/bulk/workspaces/{workspace-id}/data"
  domain: data-operations
  group: async-data-export
  oauth_scopes:
    - ZohoAnalytics.data.read
  org_id_header: required
  config_parameter:
    location: query
    required: true
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Export permission on every table the SQL query references."
  error_codes:
    - 7301
    - 7401
    - 7565
    - 7571
    - 7801
    - 7824
    - 7827
    - 7835
    - 7836
    - 7837
    - 8001
    - 8014
    - 8015
    - 8077
    - 8078
    - 8079
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
    pointer: "#/paths/~1restapi~1v2~1bulk~1workspaces~1{workspace-id}~1data/get"
    config_schema: ExportJobConfigSQLQuery
    response_schema: ExportJobCreationResponse
  sdk_examples: "/sdk-examples/data-operations/async-data-export/create-export-job-sql-query.md"
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

**GET `/restapi/v2/bulk/workspaces/{workspace-id}/data`** - Create Export Job using SQL Query (Asynchronous) (Asynchronous Data Export / Data Operations).

Creates an export job whose source is an ad-hoc SQL `SELECT` statement rather than a saved view.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace the query runs against. Every table the query references must belong to it. |

From the OpenAPI specification:

Create an export job using an SQL SELECT statement to initiate data export asynchronously.

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
| Operation ID | `createExportJobSQLQuery` |
| HTTP method | GET |
| URL | `/restapi/v2/bulk/workspaces/{workspace-id}/data` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.data.read`](../../../foundations/oauth-scopes.md#zohoanalyticsdataread) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Export permission on every table the SQL query references. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - **mandatory** |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1bulk~1workspaces~1{workspace-id}~1data/get`; CONFIG schema `ExportJobConfigSQLQuery`; response schema `ExportJobCreationResponse` |

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

## CONFIG Parameters

In addition to the [Shared CONFIG Attributes](overview.md#shared-config-attributes):

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `sqlQuery` | String | **Yes** | — | The SQL `SELECT` statement to execute, maximum 100,000 characters. Table and column names are the display names shown in Zoho Analytics. A statement that references no table, or that cannot be parsed, fails the create call. |
| `tableCriteriaList` | JSONArray of Object | No | — | Per-table filter expressions, 0–25 entries. See [`tableCriteriaList` structure](overview.md#tablecriterialist-structure). |

> `criteria` and `applyDefaultUF` are **not** accepted by this API. Row selection belongs in the `WHERE` clause of `sqlQuery`, or in `tableCriteriaList`.

> `responseFormat: "image"` can never succeed here — a query result is a flat sheet, not a chart, so the request fails with [`8014`](../../../foundations/error-codes.md#error-8014).

## Notes from the OpenAPI specification

This is a GET request, so the CONFIG value is sent as a query parameter. The JSONObject must be stringified and URL encoded before it is appended to the request URL.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | `"success"` on success. |
| `summary` | String | `"Create bulk export job"`. |
| `data` | Object | Job identification. |
| `data.jobId` | String | ID of the created job, **as a string**. The `<job-id>` for [Get Export Job Details](get-export-job-details.md) and [Download Exported Data](download-exported-data.md). |

# Examples

## Sample Requests

For readability the `CONFIG` values below are shown as plain JSON. On the wire each must be stringified and URL-encoded, as in [Request conventions](../../../foundations/request-conventions.md).

**Case 1 — `tableCriteriaList` alone: filter each participating table**

```http
GET /restapi/v2/bulk/workspaces/466206000000071000/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

```json
{
  "sqlQuery": "SELECT \"Sales\".\"Region\", \"Sales\".\"Amount\", \"Targets\".\"Quota\" FROM \"Sales\" JOIN \"Targets\" ON \"Sales\".\"Region\" = \"Targets\".\"Region\"",
  "responseFormat": "csv",
  "tableCriteriaList": [
    {
      "viewId": 466206000000072000,
      "criteria": "\"Region\"='East'"
    },
    {
      "viewId": 466206000000072500,
      "criteria": "\"Quota\">100000"
    }
  ]
}
```

Each expression is pushed into the generated query for its own table. Both `viewId` values must be tables the statement actually references, otherwise the call fails with [`7836`](../../../foundations/error-codes.md#error-7836).

**Case 2 — a fully configured CSV job with a callback**

Covers column selection, the three CSV delimiter attributes, row numbers, password protection, and callback notification in one call.

```json
{
  "sqlQuery": "SELECT \"Region\", \"Product\", \"Sales\" FROM \"SalesTable\" WHERE \"Sales\" > 1000",
  "responseFormat": "csv",
  "selectedColumns": ["Region", "Product", "Sales"],
  "delimiter": 1,
  "recordDelimiter": 1,
  "quoted": 1,
  "includeHeader": true,
  "includeRowNums": true,
  "showHiddenCols": false,
  "showPersonalCols": false,
  "password": "Zoho@123",
  "callbackUrl": "https://example.com/hooks/za-export"
}
```

Because `password` is present, [Download Exported Data](download-exported-data.md) will return a **ZIP archive** rather than a bare CSV.

**Case 3 — the same query as a print-ready PDF**

```json
{
  "sqlQuery": "SELECT \"Region\", \"Product\", \"Sales\" FROM \"SalesTable\"",
  "responseFormat": "pdf",
  "paperSize": 4,
  "paperStyle": "Landscape",
  "topMargin": 0.5,
  "bottomMargin": 0.5,
  "showTitle": 0,
  "showDesc": 2,
  "columnWidthRatio": 2,
  "exportLanguage": 0,
  "leftHeader": 1,
  "rightHeader": 2,
  "leftFooter": 5,
  "leftFooterText": "Confidential — Internal Use Only",
  "centerFooter": 4,
  "includeHeader": true
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

**HTTP 400 Bad Request — the concurrent job limit is reached**

```json
{
  "status": "failure",
  "summary": "ASYNC_EXPORT_LIMIT_EXCEEDED",
  "data": {
    "errorCode": 8132,
    "errorMessage": "Async export limit reached. Kindly retry once after your previously initiated jobs are completed."
  }
}
```

**HTTP 400 Bad Request — a `tableCriteriaList` entry names a table the query does not use**

```json
{
  "status": "failure",
  "summary": "GIVEN_TABLE_NOT_INVOLVED_IN_SQL_EXPORT",
  "data": {
    "errorCode": 7836,
    "errorMessage": "The given table is not involved in the SQL query."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Export Job using SQL Query (Asynchronous)](../../../sdk-examples/data-operations/async-data-export/create-export-job-sql-query.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **`CONFIG` is mandatory here** | Unlike [Create Export Job using View ID (Asynchronous)](create-export-job-view-id.md), this API has no source without a CONFIG, so an absent or empty CONFIG is rejected with `8077`. |
| **Export permission is checked per involved table** | The statement is parsed, the participating tables are resolved, and Export permission is verified on each. `7301` here means "not allowed to export one of the tables in the query", not "not allowed to export". |
| **A row limit is appended automatically** | The generated query is capped at 800,000 rows. A statement that would return more is silently truncated — the job still completes successfully. |
| **A query that references no table is rejected** | `7835`. Constant-only `SELECT` statements are not a valid export source. |
| **Validation happens before the job exists** | A bad `sqlQuery`, a bad `tableCriteriaList`, an unreachable `callbackUrl`, or a permission failure all produce an error response and **no** `jobId`. |
| **The whole job may still fail later** | Creation success only means the request was accepted. Errors raised while producing the file surface as `jobCode` `1003` on [Get Export Job Details](get-export-job-details.md). |
| **`jobId` is a string** | Even though it is numerically a long. Do not parse it into a fixed-width integer type. |
| **Dependency chain:** | Any SQL `SELECT` over the workspace's tables → Create Export Job using SQL Query (Asynchronous) → `data.jobId` → [Get Export Job Details](get-export-job-details.md) → [Download Exported Data](download-exported-data.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller lacks Export permission on at least one table referenced by the query. | Ensure the caller holds Export permission on every table in the statement. |
| [7401](../../../foundations/error-codes.md#error-7401) | 400 | The SQL statement is not a valid or allowed construct. | Review the syntax; only `SELECT` statements over the workspace's own tables are accepted. |
| [7565](../../../foundations/error-codes.md#error-7565) | 400 | `UNVERIFIED_EMAIL` — The calling user's primary email address is not verified. | Verify the account's primary email address and retry. |
| [7571](../../../foundations/error-codes.md#error-7571) | 400 | `UNKNOWN_VIEWID_PASSED` — A `tableCriteriaList[].viewId` does not exist in this workspace. | Verify the IDs with [Get View List](../../views-management/view-operations/get-views.md). |
| [7801](../../../foundations/error-codes.md#error-7801) | 400 | `MARGIN_VALUE_EXCEEDS` — A PDF margin is outside `0`–`1` inches. | Send a value between `0` and `1`. |
| [7824](../../../foundations/error-codes.md#error-7824) | 400 | `EXPORT_REQ_BLOCKED` — Export has been blocked for this workspace. | Contact Zoho Analytics support using the address in the error message. |
| [7827](../../../foundations/error-codes.md#error-7827) | 400 | `EXP_PDF_RECORD_LIMIT` — The PDF exceeds 1,000,000 cells. | Narrow the statement or use `selectedColumns`. |
| [7835](../../../foundations/error-codes.md#error-7835) | 400 | `NO_TABLES_INVOLVED_IN_SQL_EXPORT` — The statement references no table. | Query at least one table of the workspace. |
| [7836](../../../foundations/error-codes.md#error-7836) | 400 | `GIVEN_TABLE_NOT_INVOLVED_IN_SQL_EXPORT` — A `tableCriteriaList[].viewId` is not used by the statement. | List only tables the query actually references. |
| [7837](../../../foundations/error-codes.md#error-7837) | 400 | `INVOLVED_TABLE_DOES_NOT_HAVE_PERMISSION` — A table used by the query has no matching `tableCriteriaList` entry where one is required. | Supply a criteria entry for every participating table. |
| [8001](../../../foundations/error-codes.md#error-8001) | 400 | `INVALID_RESP_FORMAT` — `responseFormat` is not a supported value. | Send one of `csv`, `json`, `xml`, `xls`, `pdf`, `html`. |
| [8014](../../../foundations/error-codes.md#error-8014) | 400 | `API_IMAGE_RESPONSE_NOT_POSSIBLE` — `image` was requested. | A query result cannot be rendered as an image; choose another format. |
| [8015](../../../foundations/error-codes.md#error-8015) | 400 | `API_EXPORT_COLUMN_NOT_PRESENT` — A name in `selectedColumns` is not in the result set. | Match the names to the columns the statement projects. |
| [8077](../../../foundations/error-codes.md#error-8077) | 400 | `EMPTY_JSON_CONFIGURATION` — `CONFIG` was not sent, or was sent empty. | Send a CONFIG object containing at least `sqlQuery`. |
| [8078](../../../foundations/error-codes.md#error-8078) | 400 | `EMPTY_JSON_ATTRIBUTE_FOUND` — `sqlQuery` was sent but is blank. | Send a non-empty `SELECT` statement. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — A mandatory attribute is missing — `sqlQuery` on the request itself, or `viewId` / `criteria` inside a `tableCriteriaList` entry. | The message names the attribute. |
| [8088](../../../foundations/error-codes.md#error-8088) | 400 | `SECURITY_CONTROLS_FEATURE_DISABLED` — Export is disabled for the organization. | Ask an Organization Admin to re-enable export. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE` — A numeric or enumerated attribute is outside its permitted set. | Correct the value; see [Enum Reference](overview.md#enum-reference). |
| [8125](../../../foundations/error-codes.md#error-8125) | 400 | `CALLBACKURL_NOT_VALID` — `callbackUrl` is malformed. | Send a well-formed absolute `http`/`https` URL. |
| [8126](../../../foundations/error-codes.md#error-8126) | 400 | `CALLBACKURL_CONNECTION_ERROR` — `callbackUrl` could not be reached during validation. | Make the endpoint publicly reachable before creating the job. |
| [8127](../../../foundations/error-codes.md#error-8127) | 400 | `CALLBACKURL_RESTRICTED` — `callbackUrl` resolves to a private or internal address. | Use a publicly routable host. |
| [8128](../../../foundations/error-codes.md#error-8128) | 400 | `INTERNAL_ERROR_ON_INITIATING_EXPORT` — The job could not be queued. | Retry; if it persists, contact support. |
| [8132](../../../foundations/error-codes.md#error-8132) | 400 | `ASYNC_EXPORT_LIMIT_EXCEEDED` — 5 export jobs are already queued or running for the organization. | Wait for an in-flight job to finish, then retry. |
| [8188](../../../foundations/error-codes.md#error-8188) | 400 | `EXPORT_INVALID_PASSWORD` — `password` is blank or shorter than 6 characters. | Send 6–256 characters. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | `SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION` — A source table carries a restricted DATA_WARNING system tag. | Review the warning, then resend with `"validateSystemTags": false`. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | `MORE_THAN_MAX_LENGTH` — `CONFIG` exceeds 200,000 characters, or `sqlQuery` exceeds 100,000. | Shorten the statement. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.data.read`. |
| [8547](../../../foundations/error-codes.md#error-8547) | 400 | `ARRAY_SIZE_OUT_OF_RANGE` — `tableCriteriaList` exceeds 25 entries, or `selectedColumns` is empty or exceeds 300. | Stay within the documented sizes. |

# Related

- [Asynchronous Data Export overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Export Job using View ID (Asynchronous)](create-export-job-view-id.md), [Get Export Job Details](get-export-job-details.md), [Download Exported Data](download-exported-data.md).
- [SDK examples](../../../sdk-examples/data-operations/async-data-export/create-export-job-sql-query.md).
