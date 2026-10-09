---
type: API Endpoint
title: Get Last Import Details
description: "Returns the details of the most recent load into the specified view, whatever performed it - a datasource sync, a refetch, or an import API call."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/importdetails"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-operations
  - data-sync-and-connectivity
  - get
  - metadata
api:
  operation_id: getLastImportDetails
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/importdetails"
  domain: data-operations
  group: data-sync-and-connectivity
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with View Datasource or an import permission on the view."
  error_codes:
    - 7104
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/data-operations-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1importdetails/get"
    config_schema: null
    response_schema: GetLastImportDetailsResponse
  sdk_examples: "/sdk-examples/data-operations/data-sync-and-connectivity/get-last-import-details.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/importdetails`** - Get Last Import Details (Data Sync & Connectivity / Data Operations).

Reports what the most recent load into a table actually did — when it ran, whether it succeeded, and how many rows and columns landed.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace that owns the view. |
| `<view-id>` | Long | ID of the table to report on. Must belong to `<workspace-id>`. |

This API covers **every** kind of load, not only datasource syncs. A table last written by [Import Data into an Existing Table (Synchronous)](../sync-data-import/import-data-existing-table.md) reports that import here too.

From the OpenAPI specification:

Returns the details of the most recent load into the specified view, whatever performed it - a datasource sync, a refetch, or an import API call. Returns 200 with an empty data object when the view has never been loaded. Not available through a Client Portal or White Label domain.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getLastImportDetails` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/importdetails` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with View Datasource or an import permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-operations-grouped-api.json`](../../../references/openapi/data-operations-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1importdetails/get`; response schema `GetLastImportDetailsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | `"success"` on success. |
| `summary` | String | `"Fetch last import details"`. |
| `data` | Object | Details of the last load. **Empty (`{}`) when the table has never been loaded.** |
| `data.viewName` | String | Display name of the table. |
| `data.lastImportTime` | String | When the load ran, formatted `dd MMMM, yyyy hh:mm:ss a z`. |
| `data.lastImportStatus` | String | `"Success"`, `"Partial Success"`, or `"Failed"`. See [`lastImportStatus` values](#lastimportstatus-values). |
| `data.importSentFromEmail` | String | For tables loaded from an emailed attachment, the sender's address. Absent for every other source. |
| `data.columns` | Object | Column counts. |
| `data.columns.total` | String | Columns present in the incoming data. |
| `data.columns.success` | String | Columns loaded successfully. |
| `data.rows` | Object | Row counts. |
| `data.rows.total` | String | Rows present in the incoming data. |
| `data.rows.success` | String | Rows loaded successfully. |
| `data.rows.warning` | String | Rows loaded with a value reset or truncated. |
| `data.rows.failed` | String | Rows rejected outright. |
| `data.importErrors` | String | An HTML fragment describing each offending line, field, and value. Empty (`""`) when the load was clean. Display or log it — do not parse it. |

### `lastImportStatus` values

| Value | Meaning |
|-------|---------|
| `Success` | Every row loaded, and no errors were reported. Also returned when the source had nothing new, so no rows changed. |
| `Partial Success` | Some rows loaded and some did not — `rows.success` is below `rows.total`, or `warning` or `failed` is above zero. |
| `Failed` | The load did not complete. |

# Examples

## Sample Requests

```http
GET /restapi/v2/workspaces/466206000000071000/views/466206000000072000/importdetails HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — a clean load**

```json
{
  "status": "success",
  "summary": "Fetch last import details",
  "data": {
    "viewName": "Sales",
    "lastImportTime": "03 August, 2026 03:39:16 PM IST",
    "lastImportStatus": "Success",
    "columns": {
      "total": "7",
      "success": "7"
    },
    "rows": {
      "total": "755",
      "success": "755",
      "warning": "0",
      "failed": "0"
    },
    "importErrors": ""
  }
}
```

**HTTP 200 OK — some rows did not land**

```json
{
  "status": "success",
  "summary": "Fetch last import details",
  "data": {
    "viewName": "Sales",
    "lastImportTime": "03 August, 2026 03:39:16 PM IST",
    "lastImportStatus": "Partial Success",
    "columns": {
      "total": "7",
      "success": "7"
    },
    "rows": {
      "total": "755",
      "success": "740",
      "warning": "9",
      "failed": "6"
    },
    "importErrors": "<nobr>Line 42 : Invalid value for the column Order Date</NOBR><br><nobr>Line 88 : Invalid value for the column Sales</NOBR><br>"
  }
}
```

**HTTP 200 OK — a table loaded from an email attachment**

```json
{
  "status": "success",
  "summary": "Fetch last import details",
  "data": {
    "viewName": "InboundLeads",
    "lastImportTime": "02 August, 2026 09:14:02 AM IST",
    "lastImportStatus": "Success",
    "importSentFromEmail": "leads@zylker.com",
    "columns": {
      "total": "5",
      "success": "5"
    },
    "rows": {
      "total": "120",
      "success": "120",
      "warning": "0",
      "failed": "0"
    },
    "importErrors": ""
  }
}
```

**HTTP 200 OK — the table has never been loaded**

```json
{
  "status": "success",
  "summary": "Fetch last import details",
  "data": {}
}
```

An empty `data` object is a valid success. It means no import has ever run against this table.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Last Import Details](../../../sdk-examples/data-operations/data-sync-and-connectivity/get-last-import-details.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **An empty `data` object is a success, not an error** | It simply means the table has never been loaded. Test for the absence of `viewName` before reading any other field. |
| **It reports the last load from any path** | A datasource sync, a refetch, or an import API call — whichever ran most recently. The response does not say which. |
| **`Success` covers "nothing changed"** | When a sync finds no new data, the counts come back as `-1` and the status is still `Success`. Do not read `rows.success` as "rows written" without checking `rows.total`. |
| **All counts are strings** | `"755"`, not `755`. Convert before arithmetic. |
| **`importErrors` is markup, not data** | It is a fragment of `<nobr>…</NOBR><br>` HTML. Render or log it; do not attempt to parse fields out of it. |
| **`lastImportTime` is a pre-formatted display string** | `dd MMMM, yyyy hh:mm:ss a z`. Not epoch, not ISO 8601. |
| **It is the only outcome report for the two sync APIs** | Both return `204`, so this is where you find out whether a sync worked. |
| **`importSentFromEmail` is conditional** | Present only for tables fed by emailed attachments. |
| **Dependency chain:** | [Get Datasources](get-datasources.md) → `tableDetails[].viewId`, or [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>` → [Sync Data](sync-datasource.md) / [Refetch Data](refetch-datasource.md) → Get Last Import Details. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — The view does not exist. | Verify `<view-id>` with [Get View List](../../views-management/view-operations/get-views.md). |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The request came through a Client Portal / White Label domain, or the caller is neither an admin nor the View Owner and lacks View Datasource or an import permission on the view. | Call from the standard API host with the required permission. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.metadata.read`. |

# Related

- [Data Sync & Connectivity overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Operations](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Sync Data](sync-datasource.md), [Refetch Data](refetch-datasource.md), [Update Datasource Connection](update-datasource-connection.md), [Get Datasources](get-datasources.md).
- [SDK examples](../../../sdk-examples/data-operations/data-sync-and-connectivity/get-last-import-details.md).
