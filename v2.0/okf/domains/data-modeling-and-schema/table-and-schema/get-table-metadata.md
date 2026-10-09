---
type: API Endpoint
title: Get Table Metadata
description: "Returns the complete column schema of the specified table — including column names, data types, descriptions, lookup relationships, formula expressions, and formatting details."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/metadata"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - table-and-schema
  - get
  - metadata
api:
  operation_id: getTableMetadata
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/metadata"
  domain: data-modeling-and-schema
  group: table-and-schema
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the view."
  error_codes:
    - 7105
    - 7301
    - 7319
    - 7397
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1metadata/get"
    config_schema: null
    response_schema: GetTableMetadataResponse
  sdk_examples: "/sdk-examples/data-modeling-and-schema/table-and-schema/get-table-metadata.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/metadata`** - Get Table Metadata (Table & Schema / Data Modeling & Schema).

Returns the complete column schema of the specified table — including column names, data types, descriptions, lookup relationships, formula expressions, and formatting details. Only columns the calling user has been granted access to are included in the response.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getTableMetadata` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/metadata` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1metadata/get`; response schema `GetTableMetadataResponse` |

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
| `columnId` | String | Unique ID of the column. |
| `columnName` | String | Display name of the column. |
| `dataType` | String | Internal data type code (e.g. `"PLAIN"`, `"CURRENCY"`, `"DATE_AS_DATE"`). |
| `dataTypeId` | Integer | Numeric ID of the data type. |
| `dataTypeName` | String | Human-readable data type name (e.g. `"Plain Text"`, `"Currency"`, `"Date"`). |
| `columnIndex` | Integer | Sort order of the column within the table. Columns are ordered by ascending `columnIndex`. |
| `columnDesc` | String | Column description. Empty string if none set. |
| `columnMaxSize` | Integer | Maximum storage size of the column value (in characters or bytes, depending on type). |
| `isNullable` | Boolean | `true` if the column allows null/empty values. |
| `defaultValue` | String | The configured default value. Empty string if none set. |
| `pkTableName` | String | For lookup columns: the display name of the referenced (parent) table. Empty string for non-lookup columns. |
| `pkColumnName` | String | For lookup columns: the column name in the referenced table. Empty string for non-lookup columns. |
| `formulaDisplayName` | String | For formula columns: the formula expression as a display string. Empty string for non-formula columns. |
| `isHidden` | Boolean | `true` if the column is configured as hidden. |
| `sortedOrder` | Integer | Current sort direction applied to this column: `0` = none, `1` = ascending, `-1` = descending. |
| `sortedIndex` | Integer | Sort priority when multiple columns are sorted. `-1` = not part of any sort order. |
| `dateFormat` *(conditional)* | String | Date or datetime format string. Present only for `DATE` and `DATE_AS_DATE` columns. |
| `durationFormat` *(conditional)* | String | Duration format string. Present only for `DURATION` columns. |
| `timeFormat` *(conditional)* | String | Time format string. Present only for `TIME` columns. |
| `currencyFormat` *(conditional)* | String | Currency locale format string (e.g. `"en;US;"`). Present only for `CURRENCY` columns. |
| `thousandSeparator` *(conditional)* | String | Thousands separator character. Present for numeric types (`CURRENCY`, `NUMBER`, `DECIMAL_NUMBER`, `PERCENT`). |
| `decimalSeparator` *(conditional)* | String | Decimal separator character. Present for numeric types. |
| `decimalPlaces` *(conditional)* | Integer | Number of decimal places configured. Present for numeric types. |

## Notes from the OpenAPI specification

- The columns array reflects only the subset of columns that the caller has access to. A Workspace Admin or a user with full Design Modify permission sees every column, while a user with restricted view-level sharing sees only the shared columns. A short column list therefore does not necessarily mean that the table has few columns.
- This API works only on tables. Calling it with the view ID of a report, chart or dashboard returns error 7397. Use the Get View List API to confirm the view type beforehand.
- pkTableName, pkColumnName, formulaDisplayName, defaultValue and columnDesc are present in every column object and are returned as empty strings when they do not apply. A non-empty pkTableName identifies a lookup column and a non-empty formulaDisplayName identifies a formula column.
- dateFormat, durationFormat, timeFormat, currencyFormat, thousandSeparator, decimalSeparator and decimalPlaces are returned only for the column types to which they apply and are absent otherwise.
- columnId is a numeric identifier internally but is serialized as a quoted string.
- Columns are returned in ascending order of columnIndex, which matches the order shown in the Zoho Analytics interface.

# Examples

## Sample Requests

**Case 1 — Workspace Admin retrieving full table schema**

```http
GET /restapi/v2/workspaces/466206000000071000/views/7617000000508001/metadata HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — User with Design Modify permission retrieving column schema**

```http
GET /restapi/v2/workspaces/466206000000071000/views/7617000000508001/metadata HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — White label portal user retrieving table schema**

```http
GET /restapi/v2/workspaces/466206000000071000/views/7617000000508001/metadata HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Table with text, date, and currency columns**

```json
{
  "status": "success",
  "summary": "Get table metadata",
  "data": {
    "columns": [
      {
        "columnId": "7617000000508026",
        "columnName": "Region",
        "dataType": "PLAIN",
        "dataTypeId": 1,
        "dataTypeName": "Plain Text",
        "columnIndex": 1,
        "columnDesc": "",
        "columnMaxSize": 253,
        "isNullable": true,
        "defaultValue": "",
        "pkTableName": "",
        "pkColumnName": "",
        "formulaDisplayName": "",
        "isHidden": false,
        "sortedOrder": 0,
        "sortedIndex": -1
      },
      {
        "columnId": "7617000000508025",
        "columnName": "Order Date",
        "dataType": "DATE_AS_DATE",
        "dataTypeId": 22,
        "dataTypeName": "Date",
        "columnIndex": 2,
        "columnDesc": "",
        "columnMaxSize": 19,
        "isNullable": true,
        "defaultValue": "",
        "pkTableName": "",
        "pkColumnName": "",
        "formulaDisplayName": "",
        "dateFormat": "dd MMM, yyyy HH:mm:ss",
        "isHidden": false,
        "sortedOrder": 0,
        "sortedIndex": -1
      },
      {
        "columnId": "7617000000508030",
        "columnName": "Sales Amount",
        "dataType": "CURRENCY",
        "dataTypeId": 7,
        "dataTypeName": "Currency",
        "columnIndex": 3,
        "columnDesc": "",
        "columnMaxSize": 19,
        "isNullable": true,
        "defaultValue": "",
        "pkTableName": "",
        "pkColumnName": "",
        "formulaDisplayName": "",
        "currencyFormat": "en;US;",
        "thousandSeparator": ",",
        "decimalSeparator": ".",
        "decimalPlaces": 2,
        "isHidden": false,
        "sortedOrder": 0,
        "sortedIndex": -1
      }
    ]
  }
}
```

**Case 2 — Table with a lookup column (showing `pkTableName`/`pkColumnName`)**

```json
{
  "status": "success",
  "summary": "Get table metadata",
  "data": {
    "columns": [
      {
        "columnId": "7617000071955021",
        "columnName": "Order ID",
        "dataType": "PLAIN",
        "dataTypeId": 1,
        "dataTypeName": "Plain Text",
        "columnIndex": 1,
        "columnDesc": "",
        "columnMaxSize": 100,
        "isNullable": true,
        "defaultValue": "",
        "pkTableName": "Orders",
        "pkColumnName": "Order ID",
        "formulaDisplayName": "",
        "isHidden": false,
        "sortedOrder": 0,
        "sortedIndex": -1
      },
      {
        "columnId": "7617000071955022",
        "columnName": "Product Name",
        "dataType": "PLAIN",
        "dataTypeId": 1,
        "dataTypeName": "Plain Text",
        "columnIndex": 2,
        "columnDesc": "",
        "columnMaxSize": 100,
        "isNullable": true,
        "defaultValue": "",
        "pkTableName": "",
        "pkColumnName": "",
        "formulaDisplayName": "",
        "isHidden": false,
        "sortedOrder": 0,
        "sortedIndex": -1
      }
    ]
  }
}
```

**Case 3 — Table with a formula column (showing `formulaDisplayName`)**

```json
{
  "status": "success",
  "summary": "Get table metadata",
  "data": {
    "columns": [
      {
        "columnId": "7617000000508030",
        "columnName": "Sales",
        "dataType": "CURRENCY",
        "dataTypeId": 7,
        "dataTypeName": "Currency",
        "columnIndex": 1,
        "columnDesc": "",
        "columnMaxSize": 19,
        "isNullable": true,
        "defaultValue": "",
        "pkTableName": "",
        "pkColumnName": "",
        "formulaDisplayName": "",
        "currencyFormat": "en;US;",
        "thousandSeparator": ",",
        "decimalSeparator": ".",
        "decimalPlaces": 2,
        "isHidden": false,
        "sortedOrder": 0,
        "sortedIndex": -1
      },
      {
        "columnId": "7617000000508031",
        "columnName": "Cost",
        "dataType": "CURRENCY",
        "dataTypeId": 7,
        "dataTypeName": "Currency",
        "columnIndex": 2,
        "columnDesc": "",
        "columnMaxSize": 19,
        "isNullable": true,
        "defaultValue": "",
        "pkTableName": "",
        "pkColumnName": "",
        "formulaDisplayName": "",
        "currencyFormat": "en;US;",
        "thousandSeparator": ",",
        "decimalSeparator": ".",
        "decimalPlaces": 2,
        "isHidden": false,
        "sortedOrder": 0,
        "sortedIndex": -1
      },
      {
        "columnId": "7617000000508032",
        "columnName": "Profit",
        "dataType": "CURRENCY",
        "dataTypeId": 7,
        "dataTypeName": "Currency",
        "columnIndex": 3,
        "columnDesc": "",
        "columnMaxSize": 19,
        "isNullable": true,
        "defaultValue": "",
        "pkTableName": "",
        "pkColumnName": "",
        "formulaDisplayName": "\"Sales\" - \"Cost\"",
        "currencyFormat": "en;US;",
        "thousandSeparator": ",",
        "decimalSeparator": ".",
        "decimalPlaces": 2,
        "isHidden": false,
        "sortedOrder": 0,
        "sortedIndex": -1
      }
    ]
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Table Metadata](../../../sdk-examples/data-modeling-and-schema/table-and-schema/get-table-metadata.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Filtered column list** | The response includes only the columns that the calling user has been granted access to. A Workspace Admin or user with full DESIGNMODIFY permission sees all columns. Users with restricted view-level sharing see only their shared columns. |
| **Non-table views are rejected** | This API only works on tables. Calling it with the view ID of a report, chart, or dashboard returns error 7397. Use the Get View List API to confirm the view type before calling. |
| **`pkTableName` / `pkColumnName` for non-lookup columns** | These fields are always present in every column object but are empty strings (`""`) for columns that are not lookup columns. |
| **`formulaDisplayName` for non-formula columns** | Always present in every column object but is an empty string for non-formula columns. |
| **Conditional type-specific fields** | `dateFormat`, `durationFormat`, `timeFormat`, `currencyFormat`, `thousandSeparator`, `decimalSeparator`, and `decimalPlaces` appear only in the response for column types where they apply. They are absent for unrelated column types. |
| **`columnId` is returned as a string** | Despite being a numeric identifier internally, `columnId` is serialized as a quoted string. |
| **Dependency** | `<view-id>` in the URL must be a table's view ID, obtained from the Get View List API for the workspace. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7105](../../../foundations/error-codes.md#error-7105) | 400 | The specified view does not exist. | Verify the `<view-id>` using the Get View List API. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Design Modify permission on the specified view. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The specified view ID does not belong to the given workspace. | Confirm the `<view-id>` belongs to the workspace identified by `<workspace-id>`. |
| [7397](../../../foundations/error-codes.md#error-7397) | 400 | The specified view is not a table. | This API only returns metadata for tables. Use Get View List to confirm the view type is a table before calling. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Table & Schema overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Table](create-table.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/table-and-schema/get-table-metadata.md).
