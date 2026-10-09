---
type: API Endpoint
title: Get Import Job Details
description: "Returns the current state of an import job and, once it has finished, the full import summary."
resource: "https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/{workspace-id}/importjobs/{job-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - async-data-import
  - get
  - data
api:
  operation_id: getImportJobDetails
  method: GET
  path: "/restapi/v2/bulk/workspaces/{workspace-id}/importjobs/{job-id}"
  domain: data-operations
  group: async-data-import
  oauth_scopes:
    - ZohoAnalytics.data.create
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "Only the user who created the import job. Any other user — including an Account Admin or Organization Admin — receives 8138."
  error_codes:
    - 7103
    - 8137
    - 8138
    - 8535
  openapi:
    file: "/references/openapi/data-operations-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1bulk~1workspaces~1{workspace-id}~1importjobs~1{job-id}/get"
    config_schema: null
    response_schema: ImportJobDetailsResponse
  sdk_examples: "/sdk-examples/data-operations/async-data-import/get-import-job-details.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-operations-grouped-api.json"
    title: OpenAPI 3 specification - data-operations-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

**GET `/restapi/v2/bulk/workspaces/{workspace-id}/importjobs/{job-id}`** - Get Import Job Details (Asynchronous & Batch Data Import / Data Operations).

Returns the current state of an import job and, once it has finished, the full import summary. This is the monitoring API for **all four** import APIs above.

> This API has no CONFIG parameter.

From the OpenAPI specification:

Returns the current state of an import job and, once it has finished, the full import summary. This is the monitoring API for all four import APIs above.

Job codes returned in the response:
  - 1001 - JOB NOT INITIATED: wait for a few seconds and repeat the status check.
  - 1002 - JOB IN PROGRESS: wait for a few seconds and repeat the status check.
  - 1003 - ERROR OCCURRED: stop the status check and inspect the error message for details.
  - 1004 - JOB COMPLETED: the job is complete and the import summary is returned.
  - 1005 - JOB NOT FOUND: verify the validity of the job ID and terminate the status check.

Note: the import job summary is retained only for one hour after job completion.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getImportJobDetails` |
| HTTP method | GET |
| URL | `/restapi/v2/bulk/workspaces/{workspace-id}/importjobs/{job-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.data.create`](../../../foundations/oauth-scopes.md#zohoanalyticsdatacreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | Only the user who created the import job. Any other user — including an Account Admin or Organization Admin — receives 8138. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1bulk~1workspaces~1{workspace-id}~1importjobs~1{job-id}/get`; response schema `ImportJobDetailsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.data.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{job-id}` | string | The unique identifier of the import/export job. | [How to obtain](../../../foundations/identifiers.md#job-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. **A failed *import job* still returns `"success"`** — the job's own outcome is in `jobCode`, not here. |
| `summary` | String | Localised operation summary. `"Fetch import job info"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.jobId` | String | The job's ID, echoed from the request. |
| `data.jobCode` | String | Current job state as a **string**: `"1001"`, `"1002"`, `"1003"`, `"1004"`, or `"1005"`. See [JOBCODE and status messages](overview.md#jobcode-and-status-messages). |
| `data.jobStatus` | String | Human-readable form of `jobCode` — `JOB NOT INITIATED`, `JOB IN PROGRESS`, `ERROR OCCURRED`, `JOB COMPLETED`, or `JOB NOT FOUND`. |
| `data.batchKey` | String | **Present only for batch-import jobs.** The batch key the job was assembled under. Absent for asynchronous imports. |
| `data.jobInfo` | JSONObject | **Present only when `jobCode` is `1004` or `1003`.** On success it holds the import summary; on failure it holds the error detail. Absent while the job is queued or running. |
| `jobInfo.viewId` | String | ID of the table that was created. Present only for a **new-table** import job. This is where the new table's ID is finally delivered. |
| `jobInfo.importSummary` | JSONObject | Counts describing what was loaded. |
| `importSummary.importType` | String | The import type applied, in upper case. `"APPEND"` for a new-table import. |
| `importSummary.totalColumnCount` | Number | Columns found in the source data. |
| `importSummary.selectedColumnCount` | Number | Columns actually imported. |
| `importSummary.totalRowCount` | Number | Data rows found in the source. |
| `importSummary.successRowCount` | Number | Rows actually written. Lower than `totalRowCount` when `onError: "SKIPROW"` dropped rows. |
| `importSummary.warnings` | Number | Count of values reset or flagged, driven mainly by `onError: "SETCOLUMNEMPTY"`. |
| `importSummary.importOperation` | String | `"created"` for a new-table job, `"updated"` for an existing-table job. |
| `jobInfo.columnDetails` | JSONObject | Column name → assigned data type, as a display label (`"Plain Text"`, `"Number"`, `"Currency"`, `"Date"`, `"E-Mail"`, `"URL"`, `"Geo Column"`, …). |
| `jobInfo.importErrors` | String | Per-line warnings and resets as an **HTML fragment**. Empty string `""` when the import was clean. Not machine-readable — display or log it rather than parsing it. |
| `jobInfo.errorCode` | Number | Present when `jobCode` is `1003`. The error code that caused the job to fail. |
| `jobInfo.errorMessage` | String | Present when `jobCode` is `1003`. The failure detail, often an HTML fragment naming the offending line and field. |
| `data.expiryTime` | String | Epoch timestamp in **milliseconds**, as a string, after which the job summary is discarded. Present only alongside `jobInfo`. |

# Examples

## Sample Requests

**Case 1 — Poll an asynchronous import job**

```http
GET /restapi/v2/bulk/workspaces/466206000000071000/importjobs/1767024000003153087 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Poll a batch import job**

```http
GET /restapi/v2/bulk/workspaces/466206000000071000/importjobs/1767024000008787011 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — White Label / Client Portal workspace**

```http
GET /restapi/v2/bulk/workspaces/466206000000071009/importjobs/1767024000003153099 HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK — Job still running (`jobCode` `1002`)**

```json
{
    "status": "success",
    "summary": "Fetch import job info",
    "data": {
        "jobId": "1767024000003153087",
        "jobCode": "1002",
        "jobStatus": "JOB IN PROGRESS"
    }
}
```

**HTTP 200 OK — Job completed after a new-table import (`jobCode` `1004`)**

```json
{
    "status": "success",
    "summary": "Fetch import job info",
    "data": {
        "jobId": "1767024000003153087",
        "jobCode": "1004",
        "jobStatus": "JOB COMPLETED",
        "jobInfo": {
            "viewId": "1767024000003154002",
            "importSummary": {
                "importType": "APPEND",
                "totalColumnCount": 7,
                "selectedColumnCount": 7,
                "totalRowCount": 755,
                "successRowCount": 755,
                "warnings": 0,
                "importOperation": "created"
            },
            "columnDetails": {
                "Date": "Date",
                "Region": "Plain Text",
                "Product Category": "Plain Text",
                "Product": "Plain Text",
                "Customer Name": "Plain Text",
                "Sales": "Currency",
                "Cost": "Currency"
            },
            "importErrors": ""
        },
        "expiryTime": "1623764592309"
    }
}
```

**HTTP 200 OK — Batch import job completed (carries `batchKey`)**

```json
{
    "status": "success",
    "summary": "Fetch import job info",
    "data": {
        "jobId": "1767024000008787011",
        "jobCode": "1004",
        "jobStatus": "JOB COMPLETED",
        "batchKey": "1694703482470_1767024000008426012_SalesTable",
        "jobInfo": {
            "importSummary": {
                "importType": "APPEND",
                "totalColumnCount": 5,
                "selectedColumnCount": 5,
                "totalRowCount": 250000,
                "successRowCount": 250000,
                "warnings": 0,
                "importOperation": "updated"
            },
            "columnDetails": {
                "Region": "Plain Text",
                "Product": "Plain Text",
                "Sales": "Currency",
                "Cost": "Currency",
                "Date": "Date"
            },
            "importErrors": ""
        },
        "expiryTime": "1623768192309"
    }
}
```

**HTTP 200 OK — Job failed (`jobCode` `1003`)**

```json
{
    "status": "success",
    "summary": "Fetch import job info",
    "data": {
        "jobId": "1767024000003153091",
        "jobCode": "1003",
        "jobStatus": "ERROR OCCURRED",
        "jobInfo": {
            "errorCode": 7232,
            "errorMessage": "<nobr>[Line: 2 Field:  1] (West) -ERROR: Invalid NUMBER value</NOBR><br>"
        },
        "expiryTime": "1623764592309"
    }
}
```

**HTTP 403 Forbidden — Another user's job**

```json
{
    "status": "failure",
    "summary": "IMPORT_JOB_ACCESS_DENIED",
    "data": {
        "errorCode": 8138,
        "errorMessage": "You do not have access to this import job."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Import Job Details](../../../sdk-examples/data-operations/async-data-import/get-import-job-details.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`status` and `jobCode` mean different things** | `status` reports whether the *API call* worked; `jobCode` reports whether the *import* worked. A job that failed outright still returns `"status": "success"` with `jobCode` `1003`. Never infer import success from the HTTP status or `status` field. |
| **`jobInfo` is conditionally present** | It appears only for `1004` and `1003`. Polling code must tolerate its absence while the job is queued or running. |
| **`jobCode` is a string** | Compare against `"1004"`, not `1004`. |
| **`viewId` appears here, not at job creation** | For a new-table job this is the only place the created table's ID is delivered. |
| **`batchKey` marks a batch job** | Its presence distinguishes a batch import from an asynchronous one in the response. |
| **The job is private to its creator** | `8138` for anyone else, regardless of role. An integration that creates jobs under a service account must poll under that same account. |
| **`1005` also means "expired"** | A `jobId` that was valid an hour ago returns `JOB NOT FOUND` once the summary has been discarded — the code does not distinguish "never existed" from "no longer retained". |
| **Poll roughly every 10 seconds** | Frequent enough to be responsive, sparse enough to avoid needless load. Stop on `1003`, `1004`, or `1005`. |
| **Callback delivers this same payload** | If `callbackUrl` was supplied, the body POSTed to it is exactly this `data` structure. |
| **Dependency chain** | Any of the four import APIs above → `data.jobId` → Get Import Job Details → `jobInfo.viewId` → [Row APIs](../row-operations/overview.md), [Get Columns](../../data-modeling-and-schema/columns/overview.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [8137](../../../foundations/error-codes.md#error-8137) | 400 | `IMPORT_JOB_NOT_FOUND` — No import job exists with this ID. | Verify the `jobId`. Note that a job whose summary has expired is also reported as `jobCode` `1005`. |
| [8138](../../../foundations/error-codes.md#error-8138) | 403 | `IMPORT_JOB_ACCESS_DENIED` — The job was created by a different user. | Poll under the same account that created the job. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.data.create`. |

# Related

- [Asynchronous & Batch Data Import overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Import Job for a New Table (Asynchronous)](create-import-job-new-table.md), [Create Import Job for an Existing Table (Asynchronous)](create-import-job-existing-table.md), [Batch Import Data into New Table](batch-import-new-table.md), [Batch Import Data into Existing Table](batch-import-existing-table.md).
- [SDK examples](../../../sdk-examples/data-operations/async-data-import/get-import-job-details.md).
