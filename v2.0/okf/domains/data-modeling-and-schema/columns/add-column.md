---
type: API Endpoint
title: Add Column
description: Adds one or more columns to an existing table.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - columns
  - post
  - modeling
api:
  operation_id: addColumn
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns"
  domain: data-modeling-and-schema
  group: columns
  oauth_scopes:
    - ZohoAnalytics.modeling.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the workspace."
  error_codes:
    - 7089
    - 7092
    - 7111
    - 7125
    - 7146
    - 7157
    - 7301
    - 7397
    - 7439
    - 8173
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1columns/post"
    config_schema: AddColumnConfig
    response_schema: AddColumnResponse
  sdk_examples: "/sdk-examples/data-modeling-and-schema/columns/add-column.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns`** - Add Column (Columns / Data Modeling & Schema).

Adds one or more columns to an existing table. Supports two distinct modes in a single API:

- **Single-column mode:** Provide `columnName` and `dataType` at the top level of CONFIG. Returns the new column's ID.
- **Bulk mode:** Provide a `columns` array with multiple column definitions. Adds all columns in one request. Returns a success confirmation (individual column IDs are not returned in bulk mode).

> **Mode selection:** The API detects which mode to use based on whether a `columns` key is present in CONFIG. If `columns` is present, bulk mode is used regardless of whether `columnName` is also present.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `addColumn` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1columns/post`; CONFIG schema `AddColumnConfig`; response schema `AddColumnResponse` |

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

## CONFIG Parameters

See the CONFIG schema in the OpenAPI specification referenced in the Endpoint table.

## Notes from the OpenAPI specification

- The mode is detected from the payload. When CONFIG holds a columns key, bulk mode is used and any top-level columnName and dataType keys are ignored. When no columns key is present, single-column mode is used.
- Single-column mode returns the new columnId. Bulk mode returns only the status and summary - call the Get Table Metadata API afterwards to retrieve the IDs of the newly added columns.
- In bulk mode, a column entry that sets isMandatory to true must also carry a default value. The request fails when default is absent for such an entry.
- The maximum number of columns per bulk request is configurable at the organisation level and defaults to 10. Exceeding it returns error 8173.
- Every columnName must be unique within the table. Adding a column with an existing name returns error 7157.
- The request is rejected with error 7092 when the table is locked by an in-progress import or schema operation. Retry once the import completes.
- This API operates only on tables. The view-id must be that of a table, obtained from the Get View List API.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

# Examples

## Sample Requests

**Case 1 — Single column: add a plain text column**

```http
POST /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"columnName":"Customer Segment","dataType":"PLAIN"}
```

**Case 2 — Single column: add a currency column with PII flag**

```http
POST /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"columnName":"Annual Salary","dataType":"CURRENCY","isPIIColumn":true}
```

**Case 3 — Bulk mode: add multiple columns in one request**

```http
POST /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"columns":[{"columnName":"Discount (%)","dataType":"PERCENT"},{"columnName":"Delivery Date","dataType":"DATE_AS_DATE"},{"columnName":"Notes","dataType":"MULTI_LINE","isMandatory":false}]}
```

**Case 4 — Bulk mode: add a mandatory column (requires `default` field)**

```http
POST /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"columns":[{"columnName":"Status","dataType":"PLAIN","isMandatory":true,"default":"Pending"},{"columnName":"Priority","dataType":"PLAIN","isMandatory":true,"default":"Normal"}]}
```

**Case 5 — White label portal user adding a column**

```http
POST /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"columnName":"Feedback","dataType":"MULTI_LINE"}
```

## Sample Responses

**HTTP 200 OK — Single-column mode**

```json
{
  "status": "success",
  "summary": "Column added successfully.",
  "data": {
    "columnId": "7617000071955030"
  }
}
```

**HTTP 200 OK — Bulk mode**

```json
{
  "status": "success",
  "summary": "Column added successfully."
}
```

> In bulk mode, individual column IDs are not returned. Use Get Table Metadata to retrieve the newly added columns and their IDs.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Add Column](../../../sdk-examples/data-modeling-and-schema/columns/add-column.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Mode is auto-detected** | If the CONFIG contains a `columns` key, bulk mode is used and `columnName`/`dataType` at the top level are ignored. If no `columns` key is present, single mode is used. |
| **Single mode returns `columnId`; bulk mode does not** | Single column add returns the new `columnId`. Bulk mode returns only success/failure status. After a bulk add, call Get Table Metadata to retrieve the new column IDs. |
| **`isMandatory: true` requires `default`** | In bulk mode, if a column has `isMandatory: true`, the `default` field is mandatory. The API will fail if `default` is absent for that column. |
| **DDL lock check** | If the table is locked due to an in-progress import or schema operation, the request is rejected with error 7092. Retry after the import completes. |
| **Bulk mode per-request limit** | A maximum of 10 columns can be sent per bulk request. Exceeding this returns error 8173. |
| **Column name uniqueness** | Each `columnName` must be unique within the table. Attempting to add a column with an existing name returns error 7157. |
| **Dependency** | `<view-id>` → Get View List. The view must be a table. |

## CONFIG Parameters — Single-Column Mode

Use these top-level fields when adding one column at a time:

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `columnName` | String | **Yes** | — | Display name for the new column. Must be unique within the table. |
| `dataType` | String | **Yes** | — | Data type of the column. See the [Supported Data Types](#supported-data-types) table below. |
| `geoRole` | Integer | No | `null` | Geographic role ID for `GEO`-type columns. Specifies the geographic categorization level (e.g., country, state, city). Required when using geo data types. |
| `isPIIColumn` | Boolean | No | `false` | If `true`, marks this column as containing Personally Identifiable Information (PII). |

## CONFIG Parameters — Bulk Mode

Use the `columns` array when adding multiple columns in one request. Each element in `columns` defines one column:

| Parameter | Type | Mandatory | Max Items | Description |
|-----------|------|-----------|-----------|-------------|
| `columns` | JSONArray | **Yes** (for bulk mode) | 300 | Array of column definition objects. |

**Fields within each `columns` entry:**

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `columnName` | String | **Yes** | — | Display name for the column. Must be unique within the table. |
| `dataType` | String | **Yes** | — | Data type. See [Supported Data Types](#supported-data-types) below. |
| `geoRole` | Integer | No | `null` | Geographic role ID. Required for GEO-type columns. |
| `isPIIColumn` | Boolean | No | `false` | Marks the column as PII. |
| `isMandatory` | Boolean | No | `false` | If `true`, marks the column as mandatory for data entry. **When `isMandatory` is `true`, the `default` field becomes required.** |
| `default` | String | **Required when `isMandatory: true`** | `null` | Default value applied when no data is provided. Required if `isMandatory` is `true`. |

> **Bulk mode limit:** A maximum of 10 columns can be sent per bulk request. Exceeding this limit returns error 8173.

## Supported Data Types

The `dataType` field accepts the following values. These apply to both single-column and bulk modes.

| `dataType` Value | Display Name | Notes |
|------------------|--------------|-------|
| `PLAIN` | Plain Text | Short single-line text. |
| `MULTI_LINE` | Multi-line Text | Long-form text with line breaks. |
| `NUMBER` | Number | Integer numbers (positive and negative). |
| `POSITIVE_NUMBER` | Positive Number | Non-negative integers only. |
| `DECIMAL_NUMBER` | Decimal Number | Floating-point numbers. |
| `CURRENCY` | Currency | Monetary values with currency formatting. |
| `PERCENT` | Percentage | Percentage values. |
| `AUTO_NUMBER` | Auto Number | System-generated sequential integer. Cannot be combined with `isMandatory: true`. |
| `BOOLEAN` | True/False | Boolean checkbox (checked/unchecked). |
| `DATE` | Date Time | Date with time component (datetime). |
| `DATE_AS_DATE` | Date | Date only — no time component. |
| `TIME` | Time | Time of day. |
| `DURATION` | Duration | Time duration (hours/minutes/seconds). |
| `EMAIL` | Email Address | Validated email address. |
| `URL` | URL | Validated URL string. |
| `GEO` | Geographic (Text) | Text-based geographic column. Pair with `geoRole` integer ID to specify the geographic level. |
| `GEO_NUM` | Geographic (Number) | Number-based geographic column. Pair with `geoRole`. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7089](../../../foundations/error-codes.md#error-7089) | 400 | (For hide) All columns cannot be hidden simultaneously. | — |
| [7092](../../../foundations/error-codes.md#error-7092) | 400 | DDL lock is active — an import or schema operation is in progress on the table. | Wait for the current import or schema operation to complete before adding a column. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | A view with the same name already exists. | — |
| [7125](../../../foundations/error-codes.md#error-7125) | 400 | The data type is not compatible with the column's configuration. | Verify the `dataType` value. |
| [7146](../../../foundations/error-codes.md#error-7146) | 400 | The `dataType` value is not recognised. | Use one of the values from the Supported Data Types table. |
| [7157](../../../foundations/error-codes.md#error-7157) | 400 | A column with the same name already exists in the table. | Use a unique `columnName` within the table. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Design Modify permission on the workspace. |
| [7397](../../../foundations/error-codes.md#error-7397) | 400 | The view is not a table. | This API only operates on tables. Verify the view type using Get View List. |
| [7439](../../../foundations/error-codes.md#error-7439) | 400 | The view ID provided is not a table. | Provide the view ID of a table, not a report or dashboard. |
| [8173](../../../foundations/error-codes.md#error-8173) | 400 | The number of columns in bulk mode exceeds the allowed limit. | Reduce the number of columns per request or split into multiple calls. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Columns overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Rename Column](rename-column.md), [Delete Column](delete-column.md), [Hide Columns](hide-columns.md), [Show Columns](show-columns.md), [Get Column Dependents](get-column-dependents.md), [Sort Data by Columns](sort-data-by-columns.md), [Reorder Columns](reorder-columns.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/columns/add-column.md).
