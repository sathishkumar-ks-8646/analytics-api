---
type: API Endpoint
title: Create Query Table
description: Creates a new query table by executing a user-supplied SQL SELECT statement against existing tables/views in the workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/querytables"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - query-tables
  - post
  - modeling
api:
  operation_id: createQueryTable
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/querytables"
  domain: data-modeling-and-schema
  group: query-tables
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
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Query Table permission on the workspace."
  rate_limit: "7 requests/user/minute (5-minute lockout on breach); 15 requests/minute service-wide."
  error_codes:
    - 7301
    - 7399
    - 7400
    - 7401
    - 7402
    - 7403
    - 7404
    - 7407
    - 7408
    - 7409
    - 7413
    - 7421
    - 7433
    - 7447
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1querytables/post"
    config_schema: CreateQueryTableConfig
    response_schema: CreateQueryTableResponse
  sdk_examples: "/sdk-examples/data-modeling-and-schema/query-tables/create-query-table.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/querytables`** - Create Query Table (Query Tables / Data Modeling & Schema).

Creates a new query table by executing a user-supplied SQL `SELECT` statement against existing tables/views in the workspace.

From the OpenAPI specification:

Creates a new query table by executing a user-supplied SQL SELECT statement against existing tables/views in the workspace.

The columns of the query table and their data types are derived from the SELECT clause and cannot be configured separately. The response returns only the view ID of the new query table.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createQueryTable` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/querytables` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Query Table permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| Rate limit | 7 requests/user/minute (5-minute lockout on breach); 15 requests/minute service-wide. See [Rate limits](../../../foundations/rate-limits-and-quotas.md). |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1querytables/post`; CONFIG schema `CreateQueryTableConfig`; response schema `CreateQueryTableResponse` |

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

| Parameter | Type | Mandatory | Max Length | Description |
|-----------|------|-----------|------------|-------------|
| `queryTableName` | String | **Yes** | 80 chars | Display name for the new query table. Must be unique within the workspace. |
| `sqlQuery` | String | **Yes** | 100,000 chars | The SQL `SELECT` statement that defines the query table's data. Must reference existing tables/views in the same workspace. |
| `description` | String | No | 250 chars | Description of the query table. |
| `folderId` | Long | No | — | ID of the folder in which to place the query table. Defaults to the workspace's default folder if omitted. |

## Notes from the OpenAPI specification

- The SQL statement is parsed and validated synchronously at creation time. Syntax errors, unknown tables or columns and unsupported constructs are rejected before the query table is created, and there is no separate draft or asynchronous validation step.
- Every table or view named in the FROM and JOIN clauses must already exist in the same workspace and must be referred to by its display name.
- queryTableName must be unique within the workspace. A duplicate query table or view name is rejected.
- The response returns only viewId. Call the Get Query Table Details API afterwards to retrieve the derived column list and data types, because they are inferred from the SELECT clause rather than specified by the caller.
- A query table whose source is a spatial file type is not supported and returns error 7399.
- When the same SQL query is submitted concurrently, for example because of a network retry, the second request may be delayed or rejected to avoid creating a duplicate query table.
- This API is throttled at 7 requests per user per minute, with a five-minute lockout when the limit is breached, and at 15 requests per minute across the service. Space out bulk creation calls accordingly.
- Obtain folderId from the Get Folder List API and the source table names from the Get View List API.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

# Examples

## Sample Requests

**Case 1 — Simple join query across two tables**

```http
POST /restapi/v2/workspaces/20868000000040672/querytables HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"queryTableName":"Employee_Department","sqlQuery":"SELECT E.FirstName, E.LastName, D.DepartmentName FROM Employee E INNER JOIN Department D ON E.DepartmentID = D.DepartmentID"}
```

**Case 2 — Aggregate query with description and target folder**

```http
POST /restapi/v2/workspaces/20868000000040672/querytables HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"queryTableName":"Monthly_Sales_Summary","sqlQuery":"SELECT Region, SUM(SalesAmount) AS TotalSales FROM Sales GROUP BY Region","description":"Aggregated monthly sales totals by region","folderId":20868000000041715}
```

**Case 3 — White label portal user creating a query table**

```http
POST /restapi/v2/workspaces/20868000000040672/querytables HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"queryTableName":"Client_Order_View","sqlQuery":"SELECT OrderID, OrderDate, Amount FROM Orders WHERE Status = 'Completed'"}
```

## Sample Responses

**HTTP 200 OK**

```json
{
  "status": "success",
  "summary": "Query table has been created successfully.",
  "data": {
    "viewId": "7617000099626164"
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Query Table](../../../sdk-examples/data-modeling-and-schema/query-tables/create-query-table.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **SQL is parsed and validated at creation time** | The system converts the given `sqlQuery` into an internal query plan. Syntax errors, unknown tables/columns, and unsupported SQL constructs are caught and rejected before the query table is created. |
| **Referenced tables must exist in the same workspace** | Table/view names in the `FROM` and `JOIN` clauses must match existing views (by display name) in the same workspace. |
| **`queryTableName` must be unique** | Duplicate query table (or view) names within the workspace are rejected. |
| **Response returns only `viewId`** | Only the new query table's ID is returned. Call Get Query Table Details afterward to retrieve the full schema (auto-derived column list, data types, etc.). |
| **Column names and types are auto-derived** | The resulting query table's columns and their data types are inferred from the `SELECT` clause and the underlying source columns — they are not separately configurable at creation time. |
| **Query table over spatial (GEO) source files is not supported** | Creating a query table whose source is a spatial file type is rejected (error 7399). |
| **Duplicate submission protection** | If the same SQL query is submitted concurrently (e.g., due to network retries), the second request may be delayed or rejected to avoid creating duplicate query tables (error `DUPL_QUERY_TRIGGER`). |
| **Dependency** | `folderId` → Get Folder List. Referenced table/view names in `sqlQuery` → Get View List. After creation, call Get Query Table Details using the returned `viewId` to see resolved columns. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Create Query Table permission on the workspace. |
| [7399](../../../foundations/error-codes.md#error-7399) | 400 | The query references a spatial (GEO) file-based table, which is not supported for query tables. | Remove the spatial table reference from the SQL query. |
| [7400](../../../foundations/error-codes.md#error-7400) | 400 | Query tables are not supported/allowed for this workspace. | Contact your administrator; this is a workspace-level restriction. |
| [7401](../../../foundations/error-codes.md#error-7401) | 400 | The SQL statement is not a valid/allowed SQL construct. | Review the SQL for unsupported syntax (e.g., DDL/DML statements). Only `SELECT` queries are permitted. |
| [7402](../../../foundations/error-codes.md#error-7402) | 400 | The SQL statement is invalid. | Verify the SQL syntax and referenced object names. |
| [7403](../../../foundations/error-codes.md#error-7403) | 400 | Parsing of the SQL query failed. | Check for typos, mismatched parentheses, or unsupported SQL grammar. |
| [7404](../../../foundations/error-codes.md#error-7404) | 400 | Conversion of the SQL query to the internal execution engine failed. | Simplify the query or check for unsupported functions/constructs. |
| [7407](../../../foundations/error-codes.md#error-7407) | 400 | An invalid column was referenced in the `SELECT` clause. | Verify all column names referenced exist in the source table(s). |
| [7408](../../../foundations/error-codes.md#error-7408) | 400 | An invalid column was referenced elsewhere in the query (e.g., `WHERE`, `GROUP BY`). | Verify all column names used in the query. |
| [7409](../../../foundations/error-codes.md#error-7409) | 400 | An invalid/unknown table was referenced in the query. | Verify the table/view name matches an existing view in the workspace (case-sensitive display name). |
| [7413](../../../foundations/error-codes.md#error-7413) | 400 | The number of arguments passed to a SQL function does not match its expected signature. | Check the function's expected argument count. |
| [7421](../../../foundations/error-codes.md#error-7421) | 400 | A general SQL parse error occurred. | Review the query for syntax errors near the reported location. |
| [7433](../../../foundations/error-codes.md#error-7433) | 400 | Duplicate column names detected in the `SELECT` clause (after aliasing). | Use unique aliases (`AS`) for columns with the same name from different tables. |
| [7447](../../../foundations/error-codes.md#error-7447) | 400 | The query result would exceed the allowed row/column limit. | Add filters (`WHERE` clause) or reduce the number of selected columns to bring the result within limits. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Query Tables overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Query Tables](get-query-tables.md), [Edit Query Table](edit-query-table.md), [Get Query Table Details](get-query-table-details.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/query-tables/create-query-table.md).
