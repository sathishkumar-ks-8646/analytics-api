---
type: API Endpoint
title: Create Import Job for an Existing Table (Asynchronous)
description: Create an import job to import data into a specified existing table asynchronously.
resource: "https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - async-data-import
  - post
  - data
api:
  operation_id: createImportJobExistingTable
  method: POST
  path: "/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data"
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
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user holding the import permission matching the requested importType — see Permission Model."
  error_codes:
    - 7092
    - 7104
    - 7107
    - 7164
    - 7165
    - 7203
    - 7248
    - 7301
    - 7319
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
    pointer: "#/paths/~1restapi~1v2~1bulk~1workspaces~1{workspace-id}~1views~1{view-id}~1data/post"
    config_schema: BulkImportConfigExistingTable
    response_schema: ImportJobCreationResponse
  sdk_examples: "/sdk-examples/data-operations/async-data-import/create-import-job-existing-table.md"
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

**POST `/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data`** - Create Import Job for an Existing Table (Asynchronous) (Asynchronous & Batch Data Import / Data Operations).

Uploads a file and loads it into an existing table in the background, appending, replacing, or merging according to `importType`.

From the OpenAPI specification:

Create an import job to import data into a specified existing table asynchronously. Max allowed file size is 100 MB. 

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
| Operation ID | `createImportJobExistingTable` |
| HTTP method | POST |
| URL | `/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.data.create`](../../../foundations/oauth-scopes.md#zohoanalyticsdatacreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user holding the import permission matching the requested importType — see Permission Model. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` part of a `multipart/form-data` body - **mandatory** |
| Request Content-Type | `multipart/form-data` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1bulk~1workspaces~1{workspace-id}~1views~1{view-id}~1data/post`; CONFIG schema `BulkImportConfigExistingTable`; response schema `ImportJobCreationResponse` |

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
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

CONFIG is **mandatory**.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `importType` | String (enum) | **Yes** | — | How incoming rows combine with existing ones. See [`importType` Values](#importtype-values). Case-insensitive. |
| `fileType` | String (enum) | **Yes** | — | Format of the uploaded file. See [`fileType` Values](overview.md#filetype-values). |
| `autoIdentify` | Boolean | **Yes** | — | As in the new-table import job — when `false`, `delimiter`, `quoted`, and `commentChar` become mandatory for CSV. |
| `matchingColumns` | JSONArray of String | Conditional* | — | Columns used to match an incoming row against an existing one. 1–100 entries; every name must already exist in the table (`7107` otherwise). |
| *(shared options)* | — | No | — | See [Shared CONFIG Attributes](overview.md#shared-config-attributes). |

\* `matchingColumns` is **mandatory** when `importType` is `UPDATEADD`, and ignored for `APPEND` and `TRUNCATEADD`.

### `importType` Values

| Value | Behaviour | Needs `matchingColumns` |
|-------|-----------|-------------------------|
| `APPEND` | Adds every incoming row, keeping all existing rows. | No |
| `TRUNCATEADD` | Deletes **all** existing rows, then adds the incoming ones. | No |
| `UPDATEADD` | Updates rows whose `matchingColumns` values match; adds the rest as new rows. | **Yes** |

> These three modes are the complete supported set. Any other value is rejected with [`8119`](../../../foundations/error-codes.md#error-8119).

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
| `summary` | String | Localised operation summary. `"Create bulk import job"`. |
| `data` | JSONObject | Response payload wrapper. |
| `data.jobId` | String | ID of the newly created import job. Pass it to [Get Import Job Details](get-import-job-details.md). |

> Identical in shape to [Create Import Job for a New Table (Asynchronous)](create-import-job-new-table.md). The distinction between the two appears later, in `jobInfo` — a new-table job reports `viewId` and `importOperation: "created"`, an existing-table job reports neither `viewId` nor a creation.

# Examples

## Sample Requests

**Case 1 — Append a CSV file to an existing table**

```http
POST /restapi/v2/bulk/workspaces/466206000000071000/views/466206000003154002/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: multipart/form-data; boundary=----ZohoBoundary

------ZohoBoundary
Content-Disposition: form-data; name="CONFIG"

{
    "importType": "APPEND",
    "fileType": "CSV",
    "autoIdentify": true
}
------ZohoBoundary
Content-Disposition: form-data; name="FILE"; filename="Sales.csv"
Content-Type: text/csv

<file contents>
------ZohoBoundary--
```

**Case 2 — Merge by key from a JSON file, with a callback**

```http
POST /restapi/v2/bulk/workspaces/466206000000071000/views/466206000003154002/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: multipart/form-data; boundary=----ZohoBoundary

------ZohoBoundary
Content-Disposition: form-data; name="CONFIG"

{
    "importType": "UPDATEADD",
    "fileType": "JSON",
    "autoIdentify": true,
    "matchingColumns": ["Region", "Product"],
    "matchNulls": true,
    "onError": "SETCOLUMNEMPTY",
    "callbackUrl": "https://example.com/zoho/import-callback"
}
------ZohoBoundary
Content-Disposition: form-data; name="FILE"; filename="Sales.json"
Content-Type: application/json

<file contents>
------ZohoBoundary--
```

**Case 3 — Replace the table's contents, with explicit CSV parsing**

```http
POST /restapi/v2/bulk/workspaces/466206000000071000/views/466206000003154002/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: multipart/form-data; boundary=----ZohoBoundary

------ZohoBoundary
Content-Disposition: form-data; name="CONFIG"

{
    "importType": "TRUNCATEADD",
    "fileType": "CSV",
    "autoIdentify": false,
    "delimiter": 0,
    "quoted": 2,
    "commentChar": "#",
    "selectedColumns": ["Region", "Sales"],
    "skipTop": 1
}
------ZohoBoundary
Content-Disposition: form-data; name="FILE"; filename="Sales.csv"
Content-Type: text/csv

<file contents>
------ZohoBoundary--
```

**Case 4 — White Label / Client Portal workspace**

```http
POST /restapi/v2/bulk/workspaces/466206000000071009/views/466206000003154099/data HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: multipart/form-data; boundary=----ZohoBoundary

------ZohoBoundary
Content-Disposition: form-data; name="CONFIG"

{
    "importType": "APPEND",
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
        "jobId": "1767024000003153090"
    }
}
```

**HTTP 400 Bad Request — A `matchingColumns` entry is not a column of the table**

```json
{
    "status": "failure",
    "summary": "META_OBJECT_NOT_PRESENT",
    "data": {
        "errorCode": 7107,
        "errorMessage": "The column Regoin is not present."
    }
}
```

**HTTP 403 Forbidden — The user lacks the import permission for this `importType`**

```json
{
    "status": "failure",
    "summary": "SECURITY_NOT_PERMITTED",
    "data": {
        "errorCode": 7301,
        "errorMessage": "You (RestapiNotPermittedUser V2) do not have the permission to do this operation. "
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Import Job for an Existing Table (Asynchronous)](../../../sdk-examples/data-operations/async-data-import/create-import-job-existing-table.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **200 means "accepted", not "imported"** | Nothing has been written when the response returns. Poll [Get Import Job Details](get-import-job-details.md). |
| **The required permission depends on `importType`** | Append, truncate-and-add, and add-or-update are three separate permissions. A `7301` here means "not allowed to do *this kind* of import". |
| **`TRUNCATEADD` deletes first** | Every existing row is removed before the new rows are written. Because the work happens in the background, a job that then fails can leave the table with fewer rows than it started with — check `jobCode` before assuming the table is intact. |
| **`UPDATEADD` requires `matchingColumns`** | Matching is on the named columns' values, not on any row ID. A name that is not a real column fails with `7107` at job-creation time. |
| **Existing columns keep their types** | `columnDataTypes` entries naming an existing column are discarded. |
| **Validation is split across two phases** | Structural problems (bad `importType`, unknown `matchingColumns`, missing permission) fail synchronously at job creation; data problems (unparseable values, type mismatches) surface later as `jobCode` `1003`. |
| **`callbackUrl` forces asynchronous handling** | As in [Create Import Job for a New Table (Asynchronous)](create-import-job-new-table.md). |
| **Dependency chain** | [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>` → [Get Columns](../../data-modeling-and-schema/columns/overview.md) (to pick `matchingColumns`) → Create Import Job → `data.jobId` → [Get Import Job Details](get-import-job-details.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7092](../../../foundations/error-codes.md#error-7092) | 400 | `DDL_LOCK_SINCE_IMPORT_IN_PROGRESS` — Another import is holding a DDL lock on this table. | Retry once it has finished. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — The view does not exist. | Verify `<view-id>`. |
| [7107](../../../foundations/error-codes.md#error-7107) | 400 | `META_OBJECT_NOT_PRESENT` — A column named in `matchingColumns` is not present in the table. | Verify the names via [Get Columns](../../data-modeling-and-schema/columns/overview.md). |
| [7164](../../../foundations/error-codes.md#error-7164) | 400 | `SYSTEM_TABLE_DATA_MOD` — System table data cannot be modified. | Target a user-created table. |
| [7165](../../../foundations/error-codes.md#error-7165) | 400 | `SNAPSHOT_TABLE_DATAMOD` — Snapshot table data cannot be modified. | Target a non-snapshot table. |
| [7203](../../../foundations/error-codes.md#error-7203) | 400 | `IMPORT_FILE_EMPTY` — No file was uploaded, or it is empty. | Attach a non-empty `FILE` part. |
| [7248](../../../foundations/error-codes.md#error-7248) | 400 | `INVALID_FILE_CONTENT` — The file could not be parsed as the declared `fileType`. | Check that `fileType` matches the content. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user lacks the import permission matching `importType`, or is outside the workspace's permitted IP range. | Grant the specific import permission, or use an `importType` the user is allowed. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The table does not belong to the specified workspace. | Ensure `<workspace-id>` and `<view-id>` are consistent. |
| [7478](../../../foundations/error-codes.md#error-7478) | 400 | `MORE_THAN_MAX_COLUMN` — The source has more columns than the table can hold. | Reduce the columns, or use `selectedColumns`. |
| [7512](../../../foundations/error-codes.md#error-7512) | 400 | `INVALID_DATE_FORMAT` — A date pattern could not be parsed. | Supply a valid pattern. |
| [8046](../../../foundations/error-codes.md#error-8046) | 400 | `INVALID_COLUMNS_SELECTED` — A name in `selectedColumns` is not present in the source. | Match the names to the source's header row. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — A mandatory attribute is missing — commonly `matchingColumns` for `UPDATEADD`, or the CSV attributes when `autoIdentify` is `false`. | The message names the attribute. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE` — `importType`, `fileType`, `onError`, or a parsing attribute is outside its permitted set. | The message names the attribute and allowed values. |
| [8125](../../../foundations/error-codes.md#error-8125) | 400 | `CALLBACKURL_NOT_VALID` / `CALLBACKURL_CONNECTION_ERROR` / `CALLBACKURL_RESTRICTED` — The callback URL is malformed, unreachable, or points at a private address. | See [The `callbackUrl` Attribute](overview.md#the-callbackurl-attribute). |
| [8126](../../../foundations/error-codes.md#error-8126) | 400 | `CALLBACKURL_NOT_VALID` / `CALLBACKURL_CONNECTION_ERROR` / `CALLBACKURL_RESTRICTED` — The callback URL is malformed, unreachable, or points at a private address. | See [The `callbackUrl` Attribute](overview.md#the-callbackurl-attribute). |
| [8127](../../../foundations/error-codes.md#error-8127) | 400 | `CALLBACKURL_NOT_VALID` / `CALLBACKURL_CONNECTION_ERROR` / `CALLBACKURL_RESTRICTED` — The callback URL is malformed, unreachable, or points at a private address. | See [The `callbackUrl` Attribute](overview.md#the-callbackurl-attribute). |
| [8134](../../../foundations/error-codes.md#error-8134) | 400 | `ASYNC_IMPORT_LIMIT_EXCEEDED` — The maximum number of simultaneous import jobs is already in progress. | Wait for a running job to finish. |
| [8148](../../../foundations/error-codes.md#error-8148) | 400 | Separator configuration errors. | See [Number Separator Values](overview.md#number-separator-values). |
| [8149](../../../foundations/error-codes.md#error-8149) | 400 | Separator configuration errors. | See [Number Separator Values](overview.md#number-separator-values). |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` was not sent, or a mandatory key is missing. | Send a complete CONFIG object. |
| [8516](../../../foundations/error-codes.md#error-8516) | 400 | `UNABLE_TO_PARSE_DATA_TYPE` — A CONFIG value has the wrong JSON type. | Check booleans and integers. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.data.create`. |

# Related

- [Asynchronous & Batch Data Import overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Import Job for a New Table (Asynchronous)](create-import-job-new-table.md), [Batch Import Data into New Table](batch-import-new-table.md), [Batch Import Data into Existing Table](batch-import-existing-table.md), [Get Import Job Details](get-import-job-details.md).
- [SDK examples](../../../sdk-examples/data-operations/async-data-import/create-import-job-existing-table.md).
