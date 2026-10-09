---
type: API Endpoint
title: Get Query Table Details
description: "Returns the full metadata of the specified query table, including its SQL definition, the source views that the statement refers to, and the derived column schema."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - query-tables
  - get
  - metadata
api:
  operation_id: getQueryTableDetails
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}"
  domain: data-modeling-and-schema
  group: query-tables
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the query table."
  error_codes:
    - 7301
    - 7319
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1querytables~1{querytable-id}/get"
    config_schema: null
    response_schema: GetQueryTableDetailsResponse
  sdk_examples: "/sdk-examples/data-modeling-and-schema/query-tables/get-query-table-details.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}`** - Get Query Table Details (Query Tables / Data Modeling & Schema).

Returns the full metadata of a query table, including its SQL definition, the tables involved, and its column schema.

> This API has no CONFIG parameter.

From the OpenAPI specification:

Returns the full metadata of the specified query table, including its SQL definition, the source views that the statement refers to, and the derived column schema.

This is the only API that exposes the SQL text of a query table, so use it to audit the definition and to fetch the current statement before calling the Edit Query Table API.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getQueryTableDetails` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the query table. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1querytables~1{querytable-id}/get`; response schema `GetQueryTableDetailsResponse` |

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
| `{querytable-id}` | string | ID of the query table. Obtained from the Get Query Tables API. | [How to obtain](../../../foundations/identifiers.md#querytable-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `viewId` | String | Unique ID of the query table. |
| `viewName` | String | Display name of the query table. |
| `viewDesc` | String | Description of the query table. |
| `sqlQuery` | String | The exact SQL statement currently defining this query table. |
| `workspaceId` | String | Workspace ID. |
| `orgId` | String | Organisation ID. |
| `createdTime` | String | Epoch milliseconds of creation. |
| `createdBy` | String | Email of the creator. |
| `createdByName` | String | Display name of the creator. |
| `lastDesignModifiedTime` | String | Epoch milliseconds of the last schema/SQL change. |
| `lastDesignModifiedBy` | String | Email of the last user who modified the SQL/schema. |
| `lastDesignModifiedByName` | String | Display name of the last modifier. |
| `involvedViews` | Array | List of source tables/views referenced by the SQL query. |
| `involvedViews[].viewId` | String | ID of the source view. |
| `involvedViews[].viewName` | String | Display name of the source view. |
| `involvedViews[].viewType` | String | Type of the source view, e.g., `"Table"`. |
| `columns` | Array | Auto-derived column schema of the query table (same structure as [Get Table Metadata](../table-and-schema/overview.md)). |
| `columns[].columnName` | String | Derived column name — typically `<table-alias>.<source-column-name>` unless aliased in the SQL with `AS`. |
| `columns[].dataType` / `dataTypeName` | String | Internal code / display name of the data type, inherited from the source column. |
| `columns[].pkTableName` / `pkColumnName` | String | Present only if the column is a lookup/foreign-key column resolved through a join; empty otherwise. |

## Notes from the OpenAPI specification

- sqlQuery holds the exact stored statement. The formatting, including line breaks and whitespace, is preserved as it was submitted in the most recent create or edit call.
- Unless the SQL statement aliases each selected column with AS, the derived column name carries the source table alias, such as E.FirstName, matching the SELECT clause exactly.
- involvedViews lists only the direct sources. When a query table is built on another query table, the nested query table appears in the list but its own upstream sources are not expanded recursively.
- The columns array uses the same structure as the response of the Get Table Metadata API. pkTableName and pkColumnName are populated only for a column resolved through a join and are empty otherwise.
- Call this API before editing, because the Edit Query Table API requires the full SQL statement to be resent even for a folder-only move.
- Cross-reference the involvedViews entries against the Get View List and Get Table Metadata APIs to trace the schema of the underlying sources.

# Examples

## Sample Requests

**Case 1 — Get details of a query table**

```http
GET /restapi/v2/workspaces/7617000099626011/querytables/7617000099626164 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White label portal user fetching query table details**

```http
GET /restapi/v2/workspaces/7617000099626011/querytables/7617000099626164 HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK**

```json
{
  "status": "success",
  "summary": "Get querytable details",
  "data": {
    "viewId": "7617000099626164",
    "viewName": "QT_1",
    "viewDesc": "",
    "sqlQuery": "SELECT\n\t\t E.FirstName,\n\t\t E.LastName,\n\t\t D.DepartmentName\nFROM  Employee E\nINNER JOIN Department D ON E.DepartmentID  = D.DepartmentID  \n",
    "workspaceId": "7617000099626011",
    "orgId": "700000123456",
    "createdTime": "1743431919984",
    "createdBy": "sales.admin@zylker.com",
    "createdByName": "Sales Admin",
    "lastDesignModifiedTime": "1743431920619",
    "lastDesignModifiedBy": "sales.admin@zylker.com",
    "lastDesignModifiedByName": "Sales Admin",
    "involvedViews": [
      {
        "viewId": "7617000099626002",
        "viewName": "Employee",
        "viewType": "Table"
      },
      {
        "viewId": "7617000099626105",
        "viewName": "Department",
        "viewType": "Table"
      }
    ],
    "columns": [
      {
        "columnId": "7617000099626167",
        "columnName": "E.FirstName",
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
        "columnId": "7617000099626168",
        "columnName": "E.LastName",
        "dataType": "PLAIN",
        "dataTypeId": 1,
        "dataTypeName": "Plain Text",
        "columnIndex": 2,
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
        "columnId": "7617000099626169",
        "columnName": "D.DepartmentName",
        "dataType": "PLAIN",
        "dataTypeId": 1,
        "dataTypeName": "Plain Text",
        "columnIndex": 3,
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
      }
    ]
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Query Table Details](../../../sdk-examples/data-modeling-and-schema/query-tables/get-query-table-details.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`sqlQuery` reflects the exact stored SQL** | Formatting (line breaks, whitespace) is preserved as submitted in the most recent Create/Edit call. |
| **`columns[].columnName` often includes the source alias** | Unless the SQL query explicitly aliases each selected column with `AS`, the column name in the response is prefixed with the source table alias (e.g., `E.FirstName`), matching the `SELECT` clause exactly. |
| **`involvedViews` reflects only direct source tables** | If the query table's SQL references another query table (nested query tables), that nested query table itself appears in `involvedViews`, but its own upstream sources are not expanded recursively. |
| **Use before editing** | Since Edit Query Table requires resending the full `sqlQuery`, call this API first to retrieve the current query text, modify it, and then submit the edit. |
| **Dependency** | `<querytable-id>` → Get Query Tables. `involvedViews[].viewId` → cross-reference with Get View List / Get Table Metadata for the underlying source schema. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Design Modify permission on the query table. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The query table does not belong to the specified workspace. | Confirm `<querytable-id>` belongs to `<workspace-id>`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Query Tables overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Query Tables](get-query-tables.md), [Create Query Table](create-query-table.md), [Edit Query Table](edit-query-table.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/query-tables/get-query-table-details.md).
