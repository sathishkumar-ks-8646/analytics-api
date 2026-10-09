---
type: API Endpoint
title: Create Import Job for a New Table (Asynchronous)
description: "Uploads a file, creates a new table from it, and returns a job ID for tracking."
resource: "https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/{workspace-id}/data"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - async-data-import
  - post
  - data
api:
  operation_id: createImportJobNewTable
  method: POST
  path: "/restapi/v2/bulk/workspaces/{workspace-id}/data"
  domain: data-operations
  group: async-data-import
  oauth_scopes:
    - ZohoAnalytics.data.create
  org_id_header: required
  config_parameter:
    location: multipart
    required: true
  request_content_type: multipart/form-data
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Table permission on the workspace."
  error_codes:
    - 7092
    - 7111
    - 7203
    - 7248
    - 7301
    - 7478
    - 7512
    - 8046
    - 8079
    - 8119
    - 8125
    - 8126
    - 8127
    - 8134
    - 8148
    - 8149
    - 8504
    - 8516
    - 8535
  openapi:
    file: "/references/openapi/data-operations-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1bulk~1workspaces~1{workspace-id}~1data/post"
    config_schema: BulkImportConfigNewTable
    response_schema: ImportJobCreationResponse
  sdk_examples: "/sdk-examples/data-operations/async-data-import/create-import-job-new-table.md"
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

**POST `/restapi/v2/bulk/workspaces/{workspace-id}/data`** - Create Import Job for a New Table (Asynchronous) (Asynchronous & Batch Data Import / Data Operations).

Uploads a file, creates a new table from it, and returns a job ID for tracking. The table is created and populated in the background.

From the OpenAPI specification:

Uploads a file, creates a new table from it, and returns a job ID for tracking. The table is created and populated in the background.

Workflow of Asynchronous Import API:

1. Create Import Job:
   - Initiate the import by calling the Create Import Job API.
   - A unique JOBID will be returned in the response, which serves as the reference for tracking the import job.

2. Check Job Status:
   - Use the Get Import Job Details API to monitor the status of the import job.
   - The JOBID must be used in the request to check the status periodically (e.g., every 10 seconds).
   - The response will include a JOBCODE, which indicates the current state of the job.

Handling Import Job Status Based on JOBCODE:
  - If the JOBCODE is 1001 or 1002, wait for a few seconds and repeat the status check loop.
  - If the JOBCODE is 1003, stop the status check and inspect the error message for details.
  - If the JOBCODE is 1005, verify the validity of the JOBID and terminate the status check.
  - If the JOBCODE is 1004, the job is complete, and the import summary will be returned.

Limitations:
  - The import job summary is retained only for one hour after job completion.
  - A maximum of 5 simultaneous import jobs is allowed per organization.
  - A maximum file size of 100 MB can be imported.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createImportJobNewTable` |
| HTTP method | POST |
| URL | `/restapi/v2/bulk/workspaces/{workspace-id}/data` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.data.create`](../../../foundations/oauth-scopes.md#zohoanalyticsdatacreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Table permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` part of a `multipart/form-data` body - **mandatory** |
| Request Content-Type | `multipart/form-data` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1bulk~1workspaces~1{workspace-id}~1data/post`; CONFIG schema `BulkImportConfigNewTable`; response schema `ImportJobCreationResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.data.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `multipart/form-data; boundary=...` | Required | CONFIG and the payload (FILE or DATA) are sent as form parts. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

CONFIG is **mandatory** and is sent as a form part alongside the `FILE` part.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `tableName` | String | **Yes** | — | Name of the table to create. Must be **unused in the workspace** (`7111` otherwise). |
| `fileType` | String (enum) | **Yes** | — | Format of the uploaded file. See [`fileType` Values](overview.md#filetype-values). |
| `autoIdentify` | Boolean | **Yes** | — | When `true`, the delimiter, quote character, and column data types are detected automatically. When `false`, `delimiter`, `quoted`, and `commentChar` become **mandatory** for CSV. |
| *(shared options)* | — | No | — | `onError`, `selectedColumns`, `skipTop`, `delimiter`, `quoted`, `commentChar`, `thousandSeparator`, `decimalSeparator`, `columnSeparators`, `dateFormat`, `columnDateFormat`, `columnTimeFormat`, `columnDurationFormat`, `columnDataTypes`, `matchNulls`, `updateNullForNegativeValues`, `retainColumnNames`, `importHiddenRows`, `importHiddenColumns`, `callbackUrl` — see [Shared CONFIG Attributes](overview.md#shared-config-attributes). |

> `matchingColumns` is not used — there are no existing rows to match against.

## Other Body Parts

| Part | Type | Description |
|---|---|---|
| `FILE` | string (binary) | The file to be imported. Format should be multipart/form-data. Maximum allowed file size is 100 MB. |

## Notes from the OpenAPI specification

The CSV specific attributes - commentChar, delimiter and quoted - are mandatory if autoIdentify is set to false.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Create bulk import job"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.jobId` | String | ID of the newly created import job, as a string. Pass it to [Get Import Job Details](get-import-job-details.md) to track progress and, on completion, to read the import summary and the new table's `viewId`. |

> **`viewId` is not returned here.** The table does not exist yet when the job is created — the new table's ID arrives later, inside `jobInfo.viewId` of the [Get Import Job Details](get-import-job-details.md) response.

# Examples

## Sample Requests

**Case 1 — CSV upload with auto-identification**

```http
POST /restapi/v2/bulk/workspaces/466206000000071000/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: multipart/form-data; boundary=----ZohoBoundary

------ZohoBoundary
Content-Disposition: form-data; name="CONFIG"

{
    "tableName": "Sales",
    "fileType": "CSV",
    "autoIdentify": true
}
------ZohoBoundary
Content-Disposition: form-data; name="FILE"; filename="Sales.csv"
Content-Type: text/csv

<file contents>
------ZohoBoundary--
```

**Case 2 — JSON upload with a callback and explicit column types clubbed together**

```http
POST /restapi/v2/bulk/workspaces/466206000000071000/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: multipart/form-data; boundary=----ZohoBoundary

------ZohoBoundary
Content-Disposition: form-data; name="CONFIG"

{
    "tableName": "SalesJSON",
    "fileType": "JSON",
    "autoIdentify": true,
    "retainColumnNames": true,
    "columnDataTypes": [
        { "columnName": "Sales", "dataType": "CURRENCY" }
    ],
    "onError": "SETCOLUMNEMPTY",
    "callbackUrl": "https://example.com/zoho/import-callback"
}
------ZohoBoundary
Content-Disposition: form-data; name="FILE"; filename="Sales.json"
Content-Type: application/json

<file contents>
------ZohoBoundary--
```

**Case 3 — Strict CSV parsing with no auto-identification**

```http
POST /restapi/v2/bulk/workspaces/466206000000071000/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: multipart/form-data; boundary=----ZohoBoundary

------ZohoBoundary
Content-Disposition: form-data; name="CONFIG"

{
    "tableName": "SalesStrict",
    "fileType": "CSV",
    "autoIdentify": false,
    "delimiter": 0,
    "quoted": 2,
    "commentChar": "#",
    "skipTop": 2,
    "thousandSeparator": 0,
    "decimalSeparator": 0,
    "dateFormat": "dd MMM yyyy",
    "onError": "SKIPROW"
}
------ZohoBoundary
Content-Disposition: form-data; name="FILE"; filename="Sales.csv"
Content-Type: text/csv

<file contents>
------ZohoBoundary--
```

**Case 4 — White Label / Client Portal workspace**

```http
POST /restapi/v2/bulk/workspaces/466206000000071009/data HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: multipart/form-data; boundary=----ZohoBoundary

------ZohoBoundary
Content-Disposition: form-data; name="CONFIG"

{
    "tableName": "PortalSales",
    "fileType": "CSV",
    "autoIdentify": true
}
------ZohoBoundary
Content-Disposition: form-data; name="FILE"; filename="PortalSales.csv"
Content-Type: text/csv

<file contents>
------ZohoBoundary--
```

## Sample Responses

**HTTP 200 OK — Job created**

```json
{
    "status": "success",
    "summary": "Create bulk import job",
    "data": {
        "jobId": "1767024000003153087"
    }
}
```

**HTTP 400 Bad Request — Too many jobs already running**

```json
{
    "status": "failure",
    "summary": "ASYNC_IMPORT_LIMIT_EXCEEDED",
    "data": {
        "errorCode": 8134,
        "errorMessage": "The maximum number of simultaneous import jobs has been reached."
    }
}
```

**HTTP 400 Bad Request — A table with this name already exists**

```json
{
    "status": "failure",
    "summary": "META_DBOBJECT_NAME_DUPLICATED",
    "data": {
        "errorCode": 7111,
        "errorMessage": "An object with the name Sales already exists in this workspace."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Import Job for a New Table (Asynchronous)](../../../sdk-examples/data-operations/async-data-import/create-import-job-new-table.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **200 means "accepted", not "imported"** | The response confirms only that the job was queued. Nothing has been written yet, and the table does not exist. Poll [Get Import Job Details](get-import-job-details.md) for the real outcome. |
| **The new table's `viewId` arrives via the job** | Unlike the synchronous [Import Data into a New Table (Synchronous)](../sync-data-import/import-data-new-table.md), which returns `viewId` immediately, here you must wait for `jobCode` `1004` and read `jobInfo.viewId`. |
| **Duplicate names fail at creation time** | `tableName` uniqueness is validated when the job is created, so `7111` comes back synchronously rather than as a failed job. |
| **`callbackUrl` forces asynchronous handling** | Without it, a small upload may be processed inline and complete almost at once. With it, the job always runs through the asynchronous pipeline so the callback can fire. |
| **`autoIdentify: false` makes three attributes mandatory** | `delimiter`, `quoted`, and `commentChar` must all be supplied for CSV. |
| **The 5-job limit is checked up front** | If the organization already has five queued or running import jobs, the call fails immediately with `8134`. |
| **Job summary expires in one hour** | Read and store the result promptly — see [Limitations](overview.md#limitations). |
| **Dependency chain** | [Get Workspace List](../../workspace-management/workspace-operations/overview.md) → `<workspace-id>` → Create Import Job → `data.jobId` → [Get Import Job Details](get-import-job-details.md) → `jobInfo.viewId`. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7092](../../../foundations/error-codes.md#error-7092) | 400 | `DDL_LOCK_SINCE_IMPORT_IN_PROGRESS` — A batch import is holding a lock in this workspace. | Retry once it has finished. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | `META_DBOBJECT_NAME_DUPLICATED` — An object with this `tableName` already exists. | Choose a different name, or import into the existing table with [Create Import Job for an Existing Table (Asynchronous)](create-import-job-existing-table.md). |
| [7203](../../../foundations/error-codes.md#error-7203) | 400 | `IMPORT_FILE_EMPTY` — No file was uploaded, or the uploaded file is empty. | Attach a non-empty `FILE` part. |
| [7248](../../../foundations/error-codes.md#error-7248) | 400 | `INVALID_FILE_CONTENT` — The file could not be parsed as the declared `fileType`. | Check that `fileType` matches the actual content. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user cannot create tables in this workspace. | Ensure the user is an Account Admin, Organization Admin, Workspace Admin, or has Create Table permission. |
| [7478](../../../foundations/error-codes.md#error-7478) | 400 | `MORE_THAN_MAX_COLUMN` — The source has more columns than a table can hold. | Reduce the columns, or use `selectedColumns`. |
| [7512](../../../foundations/error-codes.md#error-7512) | 400 | `INVALID_DATE_FORMAT` — A date pattern could not be parsed. | Supply a valid pattern such as `dd-MMM-yyyy`. |
| [8046](../../../foundations/error-codes.md#error-8046) | 400 | `INVALID_COLUMNS_SELECTED` — A name in `selectedColumns` is not present in the source. | Match the names to the source's header row. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — A mandatory attribute is missing; with `autoIdentify: false` this is usually `delimiter`, `quoted`, or `commentChar`. | The message names the attribute. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE` — `fileType`, `onError`, `delimiter`, `quoted`, `thousandSeparator`, or `decimalSeparator` is outside its permitted set. | The message names the attribute and allowed values. |
| [8125](../../../foundations/error-codes.md#error-8125) | 400 | `CALLBACKURL_NOT_VALID` — `callbackUrl` is not a well-formed URL. | Supply a valid absolute `http`/`https` URL. |
| [8126](../../../foundations/error-codes.md#error-8126) | 400 | `CALLBACKURL_CONNECTION_ERROR` — The callback endpoint could not be reached. | Ensure the endpoint is publicly reachable. |
| [8127](../../../foundations/error-codes.md#error-8127) | 400 | `CALLBACKURL_RESTRICTED` — The callback URL resolves to a private or internal address. | Use a publicly routable endpoint. |
| [8134](../../../foundations/error-codes.md#error-8134) | 400 | `ASYNC_IMPORT_LIMIT_EXCEEDED` — The organization already has the maximum number of import jobs in progress. | Wait for a running job to finish and retry. |
| [8148](../../../foundations/error-codes.md#error-8148) | 400 | `DECIMAL_AND_THOUSAND_SEPARATOR_SAME` — The thousand and decimal separators are the same character. | Choose different separators. |
| [8149](../../../foundations/error-codes.md#error-8149) | 400 | `DECIMAL_AND_THOUSAND_COLUMN_SEPARATOR_LEGNTH_VALIDATION` — A `columnSeparators` entry has fewer than two values. | Send `[thousandSeparator, decimalSeparator]` per column. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` was not sent, or a mandatory key is missing. | Send a complete CONFIG object. |
| [8516](../../../foundations/error-codes.md#error-8516) | 400 | `UNABLE_TO_PARSE_DATA_TYPE` — A CONFIG value has the wrong JSON type. | Check booleans and integers are sent as such. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.data.create`. |

# Related

- [Asynchronous & Batch Data Import overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Import Job for an Existing Table (Asynchronous)](create-import-job-existing-table.md), [Batch Import Data into New Table](batch-import-new-table.md), [Batch Import Data into Existing Table](batch-import-existing-table.md), [Get Import Job Details](get-import-job-details.md).
- [SDK examples](../../../sdk-examples/data-operations/async-data-import/create-import-job-new-table.md).
