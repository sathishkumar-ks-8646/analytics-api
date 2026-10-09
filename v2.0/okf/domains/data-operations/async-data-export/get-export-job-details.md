---
type: API Endpoint
title: Get Export Job Details
description: "Reports the progress of an export job, and once it has finished, where to collect the file."
resource: "https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/{workspace-id}/exportjobs/{job-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - async-data-export
  - get
  - data
api:
  operation_id: getExportJobDetails
  method: GET
  path: "/restapi/v2/bulk/workspaces/{workspace-id}/exportjobs/{job-id}"
  domain: data-operations
  group: async-data-export
  oauth_scopes:
    - ZohoAnalytics.data.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "Only the user who created the export job. Any other user, including an Account Admin or Organization Admin, receives 8124."
  error_codes:
    - 8120
    - 8124
    - 8535
  openapi:
    file: "/references/openapi/data-operations-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1bulk~1workspaces~1{workspace-id}~1exportjobs~1{job-id}/get"
    config_schema: null
    response_schema: ExportJobDetailsResponse
  sdk_examples: "/sdk-examples/data-operations/async-data-export/get-export-job-details.md"
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

**GET `/restapi/v2/bulk/workspaces/{workspace-id}/exportjobs/{job-id}`** - Get Export Job Details (Asynchronous Data Export / Data Operations).

Reports the progress of an export job, and once it has finished, where to collect the file.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace the job was created against. |
| `<job-id>` | Long | The `data.jobId` returned by either creation API. |

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getExportJobDetails` |
| HTTP method | GET |
| URL | `/restapi/v2/bulk/workspaces/{workspace-id}/exportjobs/{job-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.data.read`](../../../foundations/oauth-scopes.md#zohoanalyticsdataread) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | Only the user who created the export job. Any other user, including an Account Admin or Organization Admin, receives 8124. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1bulk~1workspaces~1{workspace-id}~1exportjobs~1{job-id}/get`; response schema `ExportJobDetailsResponse` |

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
| `{job-id}` | string | The unique identifier of the import/export job. | [How to obtain](../../../foundations/identifiers.md#job-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | `"success"` whenever the request itself succeeded — including when the job has failed. |
| `summary` | String | `"Fetch export job info"`. |
| `data` | Object | Job state. |
| `data.jobId` | String | Echo of the requested job ID. |
| `data.jobCode` | String | Current state as a numeric code **in a string**: `"1001"`, `"1002"`, `"1003"`, `"1004"`, or `"1005"`. See [Job Codes and Polling](overview.md#job-codes-and-polling). |
| `data.jobStatus` | String | Human-readable form of `jobCode`: `JOB NOT INITIATED`, `JOB IN PROGRESS`, `ERROR OCCURRED`, `JOB COMPLETED`, or `JOB NOT FOUND`. Intended for display; branch on `jobCode`. |
| `data.downloadUrl` | String | Fully-qualified URL of [Download Exported Data](download-exported-data.md) for this job. **Present only when `jobCode` is `"1004"`.** |
| `data.expiryTime` | String | Epoch time in **milliseconds**, as a string, at which the job and its file are removed. Set to 72 hours after the job was **created**. **Present only when `jobCode` is `"1004"`.** |

# Examples

## Sample Requests

**Case 1 — poll a job**

```http
GET /restapi/v2/bulk/workspaces/466206000000071000/exportjobs/466206000000091000 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

There is nothing else to send. The same request is repeated until `jobCode` becomes terminal.

## Sample Responses

**HTTP 200 OK — still queued**

```json
{
  "status": "success",
  "summary": "Fetch export job info",
  "data": {
    "jobId": "466206000000091000",
    "jobCode": "1001",
    "jobStatus": "JOB NOT INITIATED"
  }
}
```

**HTTP 200 OK — running**

```json
{
  "status": "success",
  "summary": "Fetch export job info",
  "data": {
    "jobId": "466206000000091000",
    "jobCode": "1002",
    "jobStatus": "JOB IN PROGRESS"
  }
}
```

**HTTP 200 OK — finished, file ready**

```json
{
  "status": "success",
  "summary": "Fetch export job info",
  "data": {
    "jobId": "466206000000091000",
    "jobCode": "1004",
    "jobStatus": "JOB COMPLETED",
    "downloadUrl": "https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/466206000000071000/exportjobs/466206000000091000/data",
    "expiryTime": "1789171200000"
  }
}
```

**HTTP 200 OK — the job failed**

```json
{
  "status": "success",
  "summary": "Fetch export job info",
  "data": {
    "jobId": "466206000000091000",
    "jobCode": "1003",
    "jobStatus": "ERROR OCCURRED"
  }
}
```

Note the HTTP status is still `200` — the *request* succeeded, the *job* did not.

**HTTP 403 Forbidden — polling someone else's job**

```json
{
  "status": "failure",
  "summary": "EXPORT_JOB_ACCESS_DENIED",
  "data": {
    "errorCode": 8124,
    "errorMessage": "You Jane Doe do not have permission to access the job."
  }
}
```

**HTTP 404 Not Found — no such job**

```json
{
  "status": "failure",
  "summary": "EXPORT_JOB_NOT_FOUND",
  "data": {
    "errorCode": 8120,
    "errorMessage": "Job 466206000000091000 not found."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Export Job Details](../../../sdk-examples/data-operations/async-data-export/get-export-job-details.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **A failed job is still a successful request** | `jobCode` `1003` comes back with HTTP `200` and `status: "success"`. Never infer job health from the HTTP status. |
| **`1005` is returned, not raised** | If a job has expired or its ID was never valid *but the ID is well-formed*, the response is `200` with `jobCode` `1005`. A structurally unresolvable job produces `8120` instead. Handle both. |
| **`downloadUrl` and `expiryTime` are conditional** | They exist only alongside `jobCode` `1004`. Test for the keys. |
| **`expiryTime` is anchored to creation, not completion** | A job created at 09:00 and finishing at 09:40 still expires 72 hours after 09:00. A long-running job therefore leaves a shorter collection window. |
| **This API does not distinguish the two creation APIs** | A view export and a SQL query export produce identical response shapes. Track which is which yourself. |
| **It reveals nothing about the export content** | No row count, no file size, no format. If you need those, record the CONFIG you sent. |
| **Polling is cheap but not free** | Poll every few seconds rather than in a tight loop; use `callbackUrl` when you control an endpoint. |
| **Only the creator may poll** | Job ownership is by user, not by role — see [Permission Model](overview.md#permission-model). |
| **Dependency chain:** | [Create Export Job using SQL Query (Asynchronous)](create-export-job-sql-query.md) or [Create Export Job using View ID (Asynchronous)](create-export-job-view-id.md) → `data.jobId` → Get Export Job Details → `data.downloadUrl` → [Download Exported Data](download-exported-data.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [8120](../../../foundations/error-codes.md#error-8120) | 404 | `EXPORT_JOB_NOT_FOUND` — No export job exists for the given ID (HTTP 404). | Verify the `jobId` returned by the create call, and that the job has not passed its 72-hour retention. |
| [8124](../../../foundations/error-codes.md#error-8124) | 403 | `EXPORT_JOB_ACCESS_DENIED` — The caller did not create this job (HTTP 403). | Poll with the same user that created the job. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.data.read`. |

# Related

- [Asynchronous Data Export overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Export Job using SQL Query (Asynchronous)](create-export-job-sql-query.md), [Create Export Job using View ID (Asynchronous)](create-export-job-view-id.md), [Download Exported Data](download-exported-data.md).
- [SDK examples](../../../sdk-examples/data-operations/async-data-export/get-export-job-details.md).
