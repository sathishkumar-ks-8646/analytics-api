---
type: API Endpoint
title: Create Table
description: Creates a new table in the specified workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/tables"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - table-and-schema
  - post
  - modeling
api:
  operation_id: createTable
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/tables"
  domain: data-modeling-and-schema
  group: table-and-schema
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
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Table permission on the workspace."
  error_codes:
    - 7111
    - 7125
    - 7126
    - 7127
    - 7128
    - 7143
    - 7144
    - 7146
    - 7183
    - 7301
    - 7379
    - 7395
    - 7413
    - 7478
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1tables/post"
    config_schema: CreateTableConfig
    response_schema: CreateTableResponse
  sdk_examples: "/sdk-examples/data-modeling-and-schema/table-and-schema/create-table.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/tables`** - Create Table (Table & Schema / Data Modeling & Schema).

Creates a new table in the specified workspace. The table structure — its columns, data types, and optional lookup relationships — is defined entirely through the CONFIG parameter at creation time.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createTable` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/tables` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Table permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1tables/post`; CONFIG schema `CreateTableConfig`; response schema `CreateTableResponse` |

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

## CONFIG Parameters

The top-level CONFIG object wraps a `tableDesign` object:

| Parameter | Type | Mandatory | Default | Max Length | Description |
|-----------|------|-----------|---------|------------|-------------|
| `tableDesign` | JSONObject | Yes | — | — | The complete table design definition. See sub-fields below. |

### `tableDesign` Fields

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `TABLENAME` | String | Yes | — | 1000 | Display name for the new table. Must be unique within the workspace. |
| `TABLEDESCRIPTION` | String | No | `""` | 1000 | Optional description for the table. |
| `FOLDERNAME` | String | No | Default folder | 1000 | Name of an existing folder to place the table in. If omitted, the table is placed in the workspace's default folder. Resolved by folder display name — error 7144 if the folder does not exist. |
| `COLUMNS` | JSONArray | Yes | — | — | Array of column definition objects. Must contain at least one column. See column fields below. |

### `COLUMNS` Array — Column Fields

Each element in the `COLUMNS` array defines one column:

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `COLUMNNAME` | String | Yes | — | 1000 | Display name of the column. Must be unique within the table. |
| `DATATYPE` | String | Yes | — | 1000 | Data type of the column. See the [Supported Data Types](#supported-data-types) table below. |
| `DESCRIPTION` | String | No | `""` | 1000 | Optional description for the column. |
| `MANDATORY` | String | No | `""` | 1000 | Set to `"true"` to mark the column as mandatory for data entry. |
| `DEFAULT` | String | No | `""` | 1000 | Default value to use for the column when no data is provided. Not supported for `AUTO_NUMBER` columns. |
| `ISHIDE` | Boolean | No | `false` | — | If `true`, the column is hidden from view by default. |
| `GEOROLE` | String | No | — | — | Geographic role for geo-type columns. Specifies the geographic entity the column represents (e.g., country, state, city). Required when using geo data types. |
| `LOOKUPCOLUMN` | JSONObject | No | — | 1000 | Defines a lookup relationship for this column. See lookup fields below. |
| `PII` | Boolean | No | `false` | — | If `true`, marks this column as containing Personally Identifiable Information (PII). |

### `LOOKUPCOLUMN` Fields (for lookup columns)

| Field | Type | Mandatory | Description |
|-------|------|-----------|-------------|
| `TABLENAME` | String | Yes (when LOOKUPCOLUMN is present) | Display name of the parent table that this column references. Must be an existing table in the workspace. |
| `COLUMNNAME` | String | Yes (when LOOKUPCOLUMN is present) | Column name in the parent table that this column references. The data types of both columns must be compatible. |

### Supported Data Types

| `DATATYPE` Value | Display Name | Description |
|------------------|--------------|-------------|
| `PLAIN` | Plain Text | Short single-line text. |
| `MULTI_LINE` | Multi-line Text | Long-form text with line breaks. |
| `NUMBER` | Number | Integer numbers. |
| `POSITIVE_NUMBER` | Positive Number | Non-negative integers only. |
| `DECIMAL_NUMBER` | Decimal Number | Floating-point numbers. |
| `CURRENCY` | Currency | Monetary values with currency formatting. |
| `PERCENT` | Percentage | Percentage values. |
| `AUTO_NUMBER` | Auto Number | System-generated sequential integer. Cannot have a DEFAULT value. |
| `BOOLEAN` | True/False | Boolean checkbox. |
| `DATE` | Date Time | Date with time (date + time components). |
| `DATE_AS_DATE` | Date | Date only (no time component). |
| `TIME` | Time | Time of day. |
| `DURATION` | Duration | Time duration (hours/minutes/seconds). |
| `EMAIL` | Email Address | Validated email address string. |
| `URL` | URL | Validated URL string. |
| `GEO` | Geographic (Text) | Text-based geographic column. Pair with `GEOROLE`. |
| `GEO_NUM` | Geographic (Number) | Number-based geographic column. Pair with `GEOROLE`. |

## Notes from the OpenAPI specification

- The COLUMNS array must hold at least one column. An empty array is rejected.
- Column names must be unique within the table. Duplicate names fail with error 7128.
- Columns appear in the table in the order in which they are listed in the COLUMNS array.
- FOLDERNAME accepts the display name of the folder, not its ID. The name is resolved to an internal folder ID at request time and the request fails with error 7144 when the folder does not exist. Use the Get Folder List API to confirm the name.
- An AUTO_NUMBER column cannot carry a DEFAULT value. Including one returns error 7143.
- For a lookup column, the referencing and the referenced columns must have compatible data types, and the referenced table must be a different, existing table in the workspace.
- When several related tables are created in sequence, create the parent table first and then the child tables that refer to it through LOOKUPCOLUMN.
- PII is a data-governance marker only. It does not restrict access to the column or encrypt its data.
- The response returns only viewId. Call the Get Table Metadata API to retrieve the full column schema of the new table.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

# Examples

## Sample Requests

**Case 1 — Create a simple table with basic column types**

```http
POST /restapi/v2/workspaces/466206000000071000/tables HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"tableDesign":{"TABLENAME":"Sales Data","TABLEDESCRIPTION":"Monthly sales records","COLUMNS":[{"COLUMNNAME":"Region","DATATYPE":"PLAIN"},{"COLUMNNAME":"Order Date","DATATYPE":"DATE_AS_DATE"},{"COLUMNNAME":"Product","DATATYPE":"PLAIN"},{"COLUMNNAME":"Sales Amount","DATATYPE":"CURRENCY"},{"COLUMNNAME":"Units Sold","DATATYPE":"NUMBER"}]}}
```

**Case 2 — Create a table with a lookup column referencing another table**

```http
POST /restapi/v2/workspaces/466206000000071000/tables HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"tableDesign":{"TABLENAME":"Order Details","TABLEDESCRIPTION":"Line items for each order","FOLDERNAME":"Sales Analysis","COLUMNS":[{"COLUMNNAME":"Order ID","DATATYPE":"PLAIN","LOOKUPCOLUMN":{"TABLENAME":"Orders","COLUMNNAME":"Order ID"}},{"COLUMNNAME":"Product Name","DATATYPE":"PLAIN"},{"COLUMNNAME":"Quantity","DATATYPE":"POSITIVE_NUMBER"},{"COLUMNNAME":"Unit Price","DATATYPE":"CURRENCY"},{"COLUMNNAME":"Notes","DATATYPE":"MULTI_LINE","ISHIDE":true}]}}
```

**Case 3 — Create a table with mandatory columns, PII flag, and auto-number**

```http
POST /restapi/v2/workspaces/466206000000071000/tables HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"tableDesign":{"TABLENAME":"Customer Registry","TABLEDESCRIPTION":"Customer master records","COLUMNS":[{"COLUMNNAME":"Customer ID","DATATYPE":"AUTO_NUMBER"},{"COLUMNNAME":"Full Name","DATATYPE":"PLAIN","MANDATORY":"true"},{"COLUMNNAME":"Email","DATATYPE":"EMAIL","MANDATORY":"true","PII":true},{"COLUMNNAME":"Phone","DATATYPE":"PLAIN","PII":true},{"COLUMNNAME":"Signup Date","DATATYPE":"DATE_AS_DATE","DEFAULT":"01 Jan, 2024"}]}}
```

**Case 4 — White label portal user creating a table (with Create Table permission)**

```http
POST /restapi/v2/workspaces/466206000000071000/tables HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"tableDesign":{"TABLENAME":"Client Submissions","COLUMNS":[{"COLUMNNAME":"Submission Date","DATATYPE":"DATE_AS_DATE"},{"COLUMNNAME":"Submitted By","DATATYPE":"EMAIL"},{"COLUMNNAME":"Value","DATATYPE":"DECIMAL_NUMBER"}]}}
```

## Sample Responses

**HTTP 200 OK**

```json
{
  "status": "success",
  "summary": "Table has been created successfully.",
  "data": {
    "viewId": "7617000071955020"
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Table](../../../sdk-examples/data-modeling-and-schema/table-and-schema/create-table.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Response returns only `viewId`** | The response contains only the newly created table's view ID. Use Get Table Metadata to retrieve the full column schema, or Get View List to see the table in the workspace. |
| **`FOLDERNAME` is the folder's display name** | This field accepts the folder's display name (not its ID). The name is resolved to an internal folder ID at request time. If the specified folder does not exist, the request fails with error 7144. Use Get Folder List to confirm the folder name before calling. |
| **`COLUMNS` must have at least one entry** | An empty `COLUMNS` array is rejected. |
| **Column names must be unique within the table** | Duplicate column names in the same `COLUMNS` array fail with error 7128. |
| **`AUTO_NUMBER` columns cannot have a `DEFAULT` value** | Including a `DEFAULT` value for an `AUTO_NUMBER` column returns error 7143. |
| **Lookup column compatibility** | Both the referencing column and the referenced column must have compatible data types. Incompatible types fail with error 7183. |
| **Lookup cannot reference the same table** | A column's `LOOKUPCOLUMN` cannot reference a column within the same table being created. This fails with error 7379. |
| **PII flag is metadata only** | Setting `PII: true` marks the column for data governance purposes. It does not restrict access or encrypt data automatically. |
| **Dependency** | If placing the table in a specific folder, obtain the folder display name from Get Folder List. If creating a lookup column, the referenced `TABLENAME` must match an existing table's display name in the workspace. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | A table or view with the same name already exists in the workspace. | Use a unique `TABLENAME` within the workspace. |
| [7125](../../../foundations/error-codes.md#error-7125) | 400 | The specified data type is not compatible with the column's configuration. | Verify the `DATATYPE` value and any associated format settings. |
| [7126](../../../foundations/error-codes.md#error-7126) | 400 | A column name is empty or missing. | Provide a non-empty `COLUMNNAME` for every column in the `COLUMNS` array. |
| [7127](../../../foundations/error-codes.md#error-7127) | 400 | A column name exceeds the maximum allowed length. | Keep `COLUMNNAME` values within 1000 characters. |
| [7128](../../../foundations/error-codes.md#error-7128) | 400 | Duplicate column names found in the `COLUMNS` array. | Ensure all `COLUMNNAME` values are unique within the same table definition. |
| [7143](../../../foundations/error-codes.md#error-7143) | 400 | A `DEFAULT` value was provided for an `AUTO_NUMBER` column. | Remove the `DEFAULT` field from `AUTO_NUMBER` column definitions. |
| [7144](../../../foundations/error-codes.md#error-7144) | 400 | The specified `FOLDERNAME` does not exist in this workspace. | Use Get Folder List to verify the exact folder display name before calling this API. |
| [7146](../../../foundations/error-codes.md#error-7146) | 400 | The `DATATYPE` value is not a recognised data type. | Use one of the supported values from the Supported Data Types table. |
| [7183](../../../foundations/error-codes.md#error-7183) | 400 | The lookup column's data type is incompatible with the referenced column's data type. | Ensure both columns use compatible data types. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Create Table permission on the workspace. |
| [7379](../../../foundations/error-codes.md#error-7379) | 400 | A lookup column cannot reference a column within the same table. | Set `LOOKUPCOLUMN.TABLENAME` to a different existing table, not the table being created. |
| [7395](../../../foundations/error-codes.md#error-7395) | 400 | The column specified in `LOOKUPCOLUMN.COLUMNNAME` does not exist in the referenced table. | Verify the column name using Get Table Metadata on the referenced table. |
| [7413](../../../foundations/error-codes.md#error-7413) | 400 | `TABLENAME` is missing or null. | Ensure the `tableDesign.TABLENAME` field is present and non-empty. |
| [7478](../../../foundations/error-codes.md#error-7478) | 400 | The number of columns exceeds the maximum allowed for a table. | Reduce the number of columns in the `COLUMNS` array. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Table & Schema overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Table Metadata](get-table-metadata.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/table-and-schema/create-table.md).
