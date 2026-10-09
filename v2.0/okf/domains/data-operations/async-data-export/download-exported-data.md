---
type: API Endpoint
title: Download Exported Data
description: Download the file produced by a completed asynchronous export job.
resource: "https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/{workspace-id}/exportjobs/{job-id}/data"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - async-data-export
  - get
  - data
api:
  operation_id: downloadExportedData
  method: GET
  path: "/restapi/v2/bulk/workspaces/{workspace-id}/exportjobs/{job-id}/data"
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
    - text/csv
    - application/json
    - application/xml
    - application/vnd.ms-excel
    - application/pdf
    - text/html
    - image/png
    - image/jpeg
    - application/zip
  permission_required: "Only the user who created the export job. Any other user, including an Account Admin or Organization Admin, receives 8124."
  error_codes:
    - 8120
    - 8121
    - 8122
    - 8123
    - 8124
    - 8535
  openapi:
    file: "/references/openapi/data-operations-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1bulk~1workspaces~1{workspace-id}~1exportjobs~1{job-id}~1data/get"
    config_schema: null
    response_schema: null
  sdk_examples: "/sdk-examples/data-operations/async-data-export/download-exported-data.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-operations-grouped-api.json"
    title: OpenAPI 3 specification - data-operations-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**GET `/restapi/v2/bulk/workspaces/{workspace-id}/exportjobs/{job-id}/data`** - Download Exported Data (Asynchronous Data Export / Data Operations).

Returns the exported file produced by a completed export job.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace the job was created against. |
| `<job-id>` | Long | The `data.jobId` returned by either creation API. |

This endpoint is exactly what `data.downloadUrl` from [Get Export Job Details](get-export-job-details.md) points at.

From the OpenAPI specification:

Download the file produced by a completed asynchronous export job. The job must have reached jobCode 1004; calling earlier fails with 8121 (queued) or 8122 (running), and 8123 if the job failed. Only the user who created the job may download it.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `downloadExportedData` |
| HTTP method | GET |
| URL | `/restapi/v2/bulk/workspaces/{workspace-id}/exportjobs/{job-id}/data` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.data.read`](../../../foundations/oauth-scopes.md#zohoanalyticsdataread) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | Only the user who created the export job. Any other user, including an Account Admin or Organization Admin, receives 8124. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `text/csv`, `application/json`, `application/xml`, `application/vnd.ms-excel`, `application/pdf`, `text/html`, `image/png`, `image/jpeg`, `application/zip` |
| Content-Type | Varies with the job's `responseFormat` — see [Exported File Structure by Format](#exported-file-structure-by-format) |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1bulk~1workspaces~1{workspace-id}~1exportjobs~1{job-id}~1data/get` |

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

## Notes from the OpenAPI specification

The exported file is available only for one hour after the export job completes.

# Response

## Success Response

HTTP `200` with content type `text/csv`, `application/json`, `application/xml`, `application/vnd.ms-excel`, `application/pdf`, `text/html`, `image/png`, `image/jpeg`, `application/zip`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

The success body is a file, not a JSON envelope, so structured fields exist only for the JSON and XML formats. They are identical to the synchronous export's — see [Response Fields](../sync-data-export/export-data-view.md#response-fields) there for the full field tables of all four shapes.

**Response headers**

| Header | Description |
|--------|-------------|
| `Content-Type` | The only header that describes the payload. Derived from the job's `responseFormat`, or `application/zip` when the file was archived — see [Exported File Structure by Format](#exported-file-structure-by-format). |
| `Content-Disposition` | **Not sent.** No filename is suggested, so the client must name the downloaded file itself. |

# Examples

## Sample Requests

**Case 1 — collect the file**

```http
GET /restapi/v2/bulk/workspaces/466206000000071000/exportjobs/466206000000091000/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — a CSV job**

```
Content-Type: text/csv

Region,Product,Sales
East,Laptop,145000
East,Monitor,38200
```

**HTTP 200 OK — a JSON job with the default `keyValueFormat: true`**

```json
{
  "data": [
    {
      "Region": "East",
      "Product": "Laptop",
      "Sales": "145000"
    },
    {
      "Region": "East",
      "Product": "Monitor",
      "Sales": "38200"
    }
  ]
}
```

**HTTP 200 OK — a binary or archived job**

```
Content-Type: application/pdf

%PDF-1.4
… binary …
```

```
Content-Type: application/zip

PK…
… binary …
```

**HTTP 400 Bad Request — the job has not started yet**

```json
{
  "status": "failure",
  "summary": "EXPORT_JOB_NOT_INITIATED",
  "data": {
    "errorCode": 8121,
    "errorMessage": "Job 466206000000091000 not initiated."
  }
}
```

**HTTP 400 Bad Request — the job is still running**

```json
{
  "status": "failure",
  "summary": "EXPORT_JOB_NOT_COMPLETED",
  "data": {
    "errorCode": 8122,
    "errorMessage": "Job 466206000000091000 not completed."
  }
}
```

**HTTP 400 Bad Request — the job failed**

```json
{
  "status": "failure",
  "summary": "EXPORT_JOB_ERROR_OCCURRED",
  "data": {
    "errorCode": 8123,
    "errorMessage": "An internal error occurred while processing the job 466206000000091000. Kindly contact our support team."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Download Exported Data](../../../sdk-examples/data-operations/async-data-export/download-exported-data.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **The response body is the file, not a wrapper** | A successful call returns no `status` / `summary` / `data` envelope. Only **failures** use the JSON envelope, so branch on the HTTP status before parsing. |
| **It never waits** | Calling before the job has finished is an error, not a blocking read: `8121` while queued, `8122` while running, `8123` if the job failed. Poll [Get Export Job Details](get-export-job-details.md) first. |
| **Each error code names a distinct job state** | `8121` queued, `8122` running, `8123` failed, `8120` absent or expired, `8124` not yours. They map one-to-one onto `jobCode`, so the download error alone is enough to decide whether to retry. |
| **The file can be downloaded more than once** | Within the 72-hour window there is no single-use restriction and no state change on download. |
| **After 72 hours the job is gone** | The record and the file are removed together, and this endpoint then fails with `8120`. |
| **No `Content-Disposition`, no filename** | Derive one from the view or query and the format, and remember that a password-protected `csv` arrives as a ZIP. |
| **Only the creator may download** | Even an Account Admin gets `8124` for another user's job — see [Permission Model](overview.md#permission-model). |
| **`downloadUrl` and this endpoint are the same thing** | Following the URL from [Get Export Job Details](get-export-job-details.md) and constructing the path yourself are equivalent. |
| **Dependency chain:** | [Get Export Job Details](get-export-job-details.md) → `jobCode` `1004` → Download Exported Data → the file. |

## Exported File Structure by Format

The file returned here is byte-for-byte what the [synchronous export](../sync-data-export/export-data-view.md#response-structure-by-format) would have produced for the same CONFIG.

| Job `responseFormat` | `Content-Type` | Body |
|----------------------|----------------|------|
| `csv` | `text/csv` | Delimited text. Optional header row, optional leading `Row Number` field. |
| `json` (`keyValueFormat: true`) | `application/json` | `{"data":[ {…}, … ]}` — one object per row, keyed by column display name. |
| `json` (`keyValueFormat: false`) | `application/json` | `{"response":{"uri":…,"action":"EXPORT","result":{"column_order":[…],"rows":[[…]]}}}` |
| `xml` (`keyValueFormat: false`) | `application/xml` | `<?xml …?><response …><result><rows><row><column name="…">…</column></row></rows></result></response>` |
| `xml` (`keyValueFormat: true`) | `application/xml` | `<result><rows><row><ColumnName>…</ColumnName></row></rows></result>` — no XML declaration and no `<response>` wrapper. |
| `xls` | `application/vnd.ms-excel` | Binary workbook. |
| `pdf` | `application/pdf` | Binary PDF. |
| `html` | `text/html` | An HTML fragment containing the rendered table. |
| `image` | `image/png` or `image/jpeg` | Binary image. |
| **any format with `password`** | `application/zip`, or the native type for `xls` and `pdf` | See [Password Protection](overview.md#password-protection). |
| **a dashboard as `html`** | `application/zip` | One HTML file per view in the dashboard. |
| **a multi-tab dashboard as `pdf`** | `application/zip` | One PDF per tab. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [8120](../../../foundations/error-codes.md#error-8120) | 404 | `EXPORT_JOB_NOT_FOUND` — No export job exists for the given ID, or it has passed its 72-hour retention (HTTP 404). | Verify the `jobId`; if it has expired, create a new job. |
| [8121](../../../foundations/error-codes.md#error-8121) | 400 | `EXPORT_JOB_NOT_INITIATED` — The job is queued but has not started (`jobCode` `1001`). | Poll [Get Export Job Details](get-export-job-details.md) until `jobCode` is `1004`. |
| [8122](../../../foundations/error-codes.md#error-8122) | 400 | `EXPORT_JOB_NOT_COMPLETED` — The job is still running (`jobCode` `1002`). | Poll [Get Export Job Details](get-export-job-details.md) until `jobCode` is `1004`. |
| [8123](../../../foundations/error-codes.md#error-8123) | 400 | `EXPORT_JOB_ERROR_OCCURRED` — The job failed (`jobCode` `1003`). | Nothing to download. Create a new job; if the failure repeats, contact support. |
| [8124](../../../foundations/error-codes.md#error-8124) | 403 | `EXPORT_JOB_ACCESS_DENIED` — The caller did not create this job (HTTP 403). | Download with the same user that created the job. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.data.read`. |

# Related

- [Asynchronous Data Export overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Export Job using SQL Query (Asynchronous)](create-export-job-sql-query.md), [Create Export Job using View ID (Asynchronous)](create-export-job-view-id.md), [Get Export Job Details](get-export-job-details.md).
- [SDK examples](../../../sdk-examples/data-operations/async-data-export/download-exported-data.md).
