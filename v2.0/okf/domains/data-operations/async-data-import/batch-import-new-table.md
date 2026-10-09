---
type: API Endpoint
title: Batch Import Data into New Table
description: Initiate an import job to create a new table and import data in batches into the created table.
resource: "https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/{workspace-id}/data/batch"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - async-data-import
  - post
  - data
api:
  operation_id: batchImportNewTable
  method: POST
  path: "/restapi/v2/bulk/workspaces/{workspace-id}/data/batch"
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
    - 7336
    - 7337
    - 7338
    - 7478
    - 7512
    - 8079
    - 8119
    - 8125
    - 8126
    - 8127
    - 8134
    - 8148
    - 8149
    - 8504
    - 8535
  openapi:
    file: "/references/openapi/data-operations-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1bulk~1workspaces~1{workspace-id}~1data~1batch/post"
    config_schema: BatchImportConfigNewTable
    response_schema: BatchImportSuccessResponse
  sdk_examples: "/sdk-examples/data-operations/async-data-import/batch-import-new-table.md"
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

**POST `/restapi/v2/bulk/workspaces/{workspace-id}/data/batch`** - Batch Import Data into New Table (Asynchronous & Batch Data Import / Data Operations).

Creates a new table and loads it from **several uploads**, all belonging to one import job. Called once per batch.

From the OpenAPI specification:

Initiate an import job to create a new table and import data in batches into the created table.

 The Batch Import API allows you to upload large amounts of data in batches. A large data file is split into small batches, each batch not exceeding 100 MB, and imported using batch import. Alternatively, you can also use Zoho Analytics SDKs to simplify the batching process.

To import large amounts of data using Batch Import, follow the steps below:

- Split the large CSV file into batches (each batch not exceeding 100MB) and upload the first batch using the Batch Import API's {"batchKey":"start"} attribute.
- The server will generate a unique job ID and batch key for the import job and send them to the user in the response.
- Use the received batch key to submit the subsequent batches to the Batch Import API.
- Mark the end of the upload by adding {"isLastBatch":true} to the final batch.

You can check the import job status using the 'Get Import Job Details' API with the jobId received in the response.

Notes:
- After the first batch is imported, scheduled import of the remaining batches begins automatically.
- For 'Append' and 'UpdateAdd' import types, each batch is committed individually.
- For 'TruncateAdd', data is committed only after the final batch is uploaded.
- Batch order is preserved throughout.
- An import summary is stored upon job completion or failure.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `batchImportNewTable` |
| HTTP method | POST |
| URL | `/restapi/v2/bulk/workspaces/{workspace-id}/data/batch` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.data.create`](../../../foundations/oauth-scopes.md#zohoanalyticsdatacreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Table permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` part of a `multipart/form-data` body - **mandatory** |
| Request Content-Type | `multipart/form-data` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1bulk~1workspaces~1{workspace-id}~1data~1batch/post`; CONFIG schema `BatchImportConfigNewTable`; response schema `BatchImportSuccessResponse` |

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

CONFIG is **mandatory on every batch**. Which attributes are read depends on whether this is the first batch.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `batchKey` | String | **Yes** | — | `"start"` on the **first** batch. On every following batch, the `batchKey` returned by the first call. An unrecognised key fails with `7338`. |
| `isLastBatch` | Boolean | No | `false` | Set `true` on the **final** batch to close the job and commit. Once sent, no further batch is accepted (`7337`). |
| `tableName` | String | **Yes on the first batch** | — | Name of the table to create. Must be unused in the workspace (`7111`). Ignored on follow-up batches. |
| `autoIdentify` | Boolean | **Yes on the first batch** | — | When `false`, `delimiter`, `quoted`, and `commentChar` become mandatory. Ignored on follow-up batches. |
| *(shared options)* | — | No | — | Read from the **first batch only** — `onError`, `selectedColumns`, `skipTop`, `delimiter`, `quoted`, `commentChar`, `thousandSeparator`, `decimalSeparator`, `columnSeparators`, `dateFormat`, `columnDateFormat`, `columnTimeFormat`, `columnDurationFormat`, `columnDataTypes`, `matchNulls`, `updateNullForNegativeValues`, `retainColumnNames`, `callbackUrl`. See [Shared CONFIG Attributes](overview.md#shared-config-attributes). |

> There is **no `fileType` attribute** — batch import accepts CSV only.
>
> Repeating the full configuration on every batch is harmless and is the convention in Zoho's own examples, but only `batchKey` and `isLastBatch` are actually read after the first batch.

## Other Body Parts

| Part | Type | Description |
|---|---|---|
| `FILE` | string (binary) | The batch file to be imported. Format should be multipart/form-data. Maximum allowed size per batch is 100 MB. |

## Notes from the OpenAPI specification

The CSV specific attributes - commentChar, delimiter and quoted - are mandatory if autoIdentify is set to false.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Create bulk import job"` — the same string for every batch, including follow-ups. |
| `data` | JSONObject | Response payload wrapper. |
| `data.batchKey` | String | The job's batch key, e.g. `1694703482470_1767024000008426012_SalesTable`. **Generated by the server on the first batch** and echoed unchanged by every subsequent batch. Send it as `batchKey` in every following call. |
| `data.jobId` | String | ID of the import job. Constant across all batches of the job. Pass it to [Get Import Job Details](get-import-job-details.md). |

# Examples

## Sample Requests

**Case 1 — First batch: opens the job**

```http
POST /restapi/v2/bulk/workspaces/466206000000071000/data/batch HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: multipart/form-data; boundary=----ZohoBoundary

------ZohoBoundary
Content-Disposition: form-data; name="CONFIG"

{
    "batchKey": "start",
    "isLastBatch": false,
    "tableName": "SalesTable",
    "autoIdentify": true,
    "onError": "SETCOLUMNEMPTY"
}
------ZohoBoundary
Content-Disposition: form-data; name="FILE"; filename="Sales_batch1.csv"
Content-Type: text/csv

<batch 1 contents>
------ZohoBoundary--
```

**Case 2 — Follow-up batch: uses the returned `batchKey`**

```http
POST /restapi/v2/bulk/workspaces/466206000000071000/data/batch HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: multipart/form-data; boundary=----ZohoBoundary

------ZohoBoundary
Content-Disposition: form-data; name="CONFIG"

{
    "batchKey": "1694703482470_1767024000008426012_SalesTable",
    "isLastBatch": false
}
------ZohoBoundary
Content-Disposition: form-data; name="FILE"; filename="Sales_batch2.csv"
Content-Type: text/csv

<batch 2 contents>
------ZohoBoundary--
```

**Case 3 — Final batch: closes the job**

```http
POST /restapi/v2/bulk/workspaces/466206000000071000/data/batch HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: multipart/form-data; boundary=----ZohoBoundary

------ZohoBoundary
Content-Disposition: form-data; name="CONFIG"

{
    "batchKey": "1694703482470_1767024000008426012_SalesTable",
    "isLastBatch": true
}
------ZohoBoundary
Content-Disposition: form-data; name="FILE"; filename="Sales_batch3.csv"
Content-Type: text/csv

<batch 3 contents>
------ZohoBoundary--
```

**Case 4 — White Label / Client Portal workspace (first batch)**

```http
POST /restapi/v2/bulk/workspaces/466206000000071009/data/batch HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: multipart/form-data; boundary=----ZohoBoundary

------ZohoBoundary
Content-Disposition: form-data; name="CONFIG"

{
    "batchKey": "start",
    "isLastBatch": false,
    "tableName": "PortalSalesTable",
    "autoIdentify": true
}
------ZohoBoundary
Content-Disposition: form-data; name="FILE"; filename="PortalSales_batch1.csv"
Content-Type: text/csv

<batch 1 contents>
------ZohoBoundary--
```

## Sample Responses

**HTTP 200 OK — Batch accepted (identical shape for the first, follow-up, and final batches)**

```json
{
    "status": "success",
    "summary": "Create bulk import job",
    "data": {
        "batchKey": "1694703482470_1767024000008426012_SalesTable",
        "jobId": "1767024000008787011"
    }
}
```

**HTTP 400 Bad Request — A batch was sent after the final one**

```json
{
    "status": "failure",
    "summary": "BATCH_IMPORT_LAST_BATCH_ALREADY_RECEIVED",
    "data": {
        "errorCode": 7337,
        "errorMessage": "The last batch has already been received for the batch key 1694703482470_1767024000008426012_SalesTable."
    }
}
```

**HTTP 400 Bad Request — Too many batches for one job**

```json
{
    "status": "failure",
    "summary": "BATCH_IMPORT_LIMIT_EXCEEDED",
    "data": {
        "errorCode": 7336,
        "errorMessage": "The allowed number of batches (100) has been exceeded."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Batch Import Data into New Table](../../../sdk-examples/data-operations/async-data-import/batch-import-new-table.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`batchKey: "start"` is a literal** | The first batch must send exactly the string `"start"`. It is not a placeholder for a value you generate — the server mints the real key and returns it. |
| **Configuration is read once** | `tableName`, `autoIdentify`, and every parsing option are consumed from the **first** batch. Changing them on a later batch has no effect; the job keeps the first batch's configuration. |
| **The job is not closed until you say so** | Without `isLastBatch: true` the job stays open and never commits. An abandoned batch job holds one of the five concurrent-job slots. |
| **The final batch is final** | After `isLastBatch: true`, any further batch on that key fails with `7337`. |
| **CSV only** | There is no `fileType`; every batch is parsed as CSV. |
| **Per-batch size limit** | Each uploaded batch may be up to 100 MB. The job's total size is unbounded, subject to the 100-batch ceiling. |
| **Ordering is preserved** | Batches are committed in the order the server receives them. There is no way to re-send or reorder a batch once accepted. |
| **Data appears progressively** | Scheduled processing of the remaining batches starts automatically after the first batch is imported. |
| **Errors can be synchronous or deferred** | An invalid key, a closed job, or an exceeded batch limit fails on the batch call itself. Data errors surface later as `jobCode` `1003`. |
| **Dependency chain** | [Get Workspace List](../../workspace-management/workspace-operations/overview.md) → first batch (`batchKey: "start"`) → `data.batchKey` + `data.jobId` → follow-up batches → final batch → [Get Import Job Details](get-import-job-details.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7092](../../../foundations/error-codes.md#error-7092) | 400 | `DDL_LOCK_SINCE_IMPORT_IN_PROGRESS` — A batch import is holding a lock in this workspace. | Retry once it has finished. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | `META_DBOBJECT_NAME_DUPLICATED` — An object with this `tableName` already exists. | Choose a different name, or use [Batch Import Data into Existing Table](batch-import-existing-table.md). |
| [7203](../../../foundations/error-codes.md#error-7203) | 400 | `IMPORT_FILE_EMPTY` — No file was uploaded for this batch, or it is empty. | Attach a non-empty `FILE` part to every batch. |
| [7248](../../../foundations/error-codes.md#error-7248) | 400 | `INVALID_FILE_CONTENT` — The batch could not be parsed as CSV. | Batch import accepts CSV only. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user cannot create tables in this workspace. | Ensure the user has Create Table permission. |
| [7336](../../../foundations/error-codes.md#error-7336) | 400 | `BATCH_IMPORT_LIMIT_EXCEEDED` — More than 100 batches were sent for one job. | Use larger batches so the job fits within the limit. |
| [7337](../../../foundations/error-codes.md#error-7337) | 400 | `BATCH_IMPORT_LAST_BATCH_ALREADY_RECEIVED` — A batch was sent after `isLastBatch: true`. | Start a new job for additional data. |
| [7338](../../../foundations/error-codes.md#error-7338) | 400 | `BATCH_IMPORT_INVALID_KEY` — The `batchKey` is not recognised, or its job is no longer active. | Use the `batchKey` returned by the first batch, and start a new job if it has expired. |
| [7478](../../../foundations/error-codes.md#error-7478) | 400 | `MORE_THAN_MAX_COLUMN` — The source has more columns than a table can hold. | Reduce the columns, or use `selectedColumns` on the first batch. |
| [7512](../../../foundations/error-codes.md#error-7512) | 400 | `INVALID_DATE_FORMAT` — A date pattern could not be parsed. | Supply a valid pattern on the first batch. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — A mandatory attribute is missing; on the first batch this is usually `tableName` or `autoIdentify`. | The message names the attribute. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE` — `onError` or a parsing attribute is outside its permitted set. | The message names the attribute and allowed values. |
| [8125](../../../foundations/error-codes.md#error-8125) | 400 | Callback URL is malformed, unreachable, or private. | See [The `callbackUrl` Attribute](overview.md#the-callbackurl-attribute). |
| [8126](../../../foundations/error-codes.md#error-8126) | 400 | Callback URL is malformed, unreachable, or private. | See [The `callbackUrl` Attribute](overview.md#the-callbackurl-attribute). |
| [8127](../../../foundations/error-codes.md#error-8127) | 400 | Callback URL is malformed, unreachable, or private. | See [The `callbackUrl` Attribute](overview.md#the-callbackurl-attribute). |
| [8134](../../../foundations/error-codes.md#error-8134) | 400 | `ASYNC_IMPORT_LIMIT_EXCEEDED` — The maximum number of simultaneous import jobs is in progress. | Wait for a running job to finish, or close an abandoned batch job. |
| [8148](../../../foundations/error-codes.md#error-8148) | 400 | Separator configuration errors. | See [Number Separator Values](overview.md#number-separator-values). |
| [8149](../../../foundations/error-codes.md#error-8149) | 400 | Separator configuration errors. | See [Number Separator Values](overview.md#number-separator-values). |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` was not sent, or `batchKey` is missing. | Every batch must carry a CONFIG containing `batchKey`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.data.create`. |

# Related

- [Asynchronous & Batch Data Import overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Import Job for a New Table (Asynchronous)](create-import-job-new-table.md), [Create Import Job for an Existing Table (Asynchronous)](create-import-job-existing-table.md), [Batch Import Data into Existing Table](batch-import-existing-table.md), [Get Import Job Details](get-import-job-details.md).
- [SDK examples](../../../sdk-examples/data-operations/async-data-import/batch-import-new-table.md).
