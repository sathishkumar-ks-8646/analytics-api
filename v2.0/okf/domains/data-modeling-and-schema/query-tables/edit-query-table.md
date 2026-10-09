---
type: API Endpoint
title: Edit Query Table
description: "Updates the SQL definition of an existing query table and, optionally, moves it to another folder."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - query-tables
  - put
  - modeling
api:
  operation_id: editQueryTable
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}"
  domain: data-modeling-and-schema
  group: query-tables
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the query table."
  rate_limit: "7 requests/user/minute (5-minute lockout on breach); 15 requests/minute service-wide."
  error_codes:
    - 7301
    - 7319
    - 7401
    - 7402
    - 7403
    - 7404
    - 7407
    - 7409
    - 7422
    - 7429
    - 7447
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1querytables~1{querytable-id}/put"
    config_schema: EditQueryTableConfig
    response_schema: null
  sdk_examples: "/sdk-examples/data-modeling-and-schema/query-tables/edit-query-table.md"
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

**PUT `/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}`** - Edit Query Table (Query Tables / Data Modeling & Schema).

Updates the SQL definition and/or folder of an existing query table. The query table's data is recomputed based on the new SQL statement.

From the OpenAPI specification:

Updates the SQL definition of an existing query table and, optionally, moves it to another folder. The data of the query table is recomputed from the new SQL statement.

The new statement replaces the existing one entirely - there is no partial update of individual clauses. The display name and the description of a query table cannot be changed through this API.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `editQueryTable` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the query table. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| Rate limit | 7 requests/user/minute (5-minute lockout on breach); 15 requests/minute service-wide. See [Rate limits](../../../foundations/rate-limits-and-quotas.md). |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1querytables~1{querytable-id}/put`; CONFIG schema `EditQueryTableConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{querytable-id}` | string | ID of the query table. Obtained from the Get Query Tables API. | [How to obtain](../../../foundations/identifiers.md#querytable-id) |

## CONFIG Parameters

| Parameter | Type | Mandatory | Max Length | Description |
|-----------|------|-----------|------------|-------------|
| `sqlQuery` | String | **Yes** | 100,000 chars | The new SQL `SELECT` statement. Replaces the existing query definition entirely. |
| `folderId` | Long | No | — | ID of the folder to move the query table into. If omitted, the query table remains in its current folder. |

> **Note:** Unlike Create Query Table, this API has no `queryTableName` or `description` field — the display name and description of the query table cannot be changed via this API. Use Rename View / update description APIs for that purpose (not covered in this document).

## Notes from the OpenAPI specification

- This API returns HTTP 204 No Content with no response body on success. There is no status or summary key to parse - treat the HTTP status code as the sole success indicator.
- sqlQuery is mandatory even when the intent is only to move the query table to another folder. Fetch the current statement using the Get Query Table Details API and resend it unchanged in that case.
- The new statement replaces the previous one completely. There is no partial or incremental update of individual clauses.
- When the new statement selects a different set of columns, whether added, removed, renamed or retyped, the column list of the query table is recomputed and any report or dashboard built on a removed or renamed column breaks. Inspect the current schema through Get Query Table Details before making structural changes.
- The request is rejected with error 7429 when another schema-changing operation is already in progress on the query table.
- This API cannot rename the query table or change its description. Only the SQL statement and the folder can be updated here.
- This API is throttled at 7 requests per user per minute, with a five-minute lockout when the limit is breached, and at 15 requests per minute across the service.
- Call the Get Query Table Details API afterwards to confirm the updated column schema.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Update the SQL query only**

```http
PUT /restapi/v2/workspaces/20868000000040672/querytables/7617000099626164 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"sqlQuery":"SELECT E.FirstName, E.LastName, D.DepartmentName, E.Salary FROM Employee E INNER JOIN Department D ON E.DepartmentID = D.DepartmentID"}
```

**Case 2 — Update SQL and move to a different folder**

```http
PUT /restapi/v2/workspaces/20868000000040672/querytables/7617000099626164 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"sqlQuery":"SELECT Region, SUM(SalesAmount) AS TotalSales FROM Sales WHERE Year = 2026 GROUP BY Region","folderId":20868000000041720}
```

**Case 3 — White label portal user editing a query table**

```http
PUT /restapi/v2/workspaces/20868000000040672/querytables/7617000099626164 HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"sqlQuery":"SELECT OrderID, OrderDate, Amount FROM Orders WHERE Status IN ('Completed','Shipped')"}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Edit Query Table](../../../sdk-examples/data-modeling-and-schema/query-tables/edit-query-table.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Edit QueryTable returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. To confirm the change, call Get QueryTable Details afterward. |
| **`sqlQuery` is mandatory even for a folder-only move** | `sqlQuery` is always required, so it must be resupplied (with its existing value, unchanged) even if the intent is only to change `folderId`. Fetch the current SQL via Get Query Table Details first if you only want to move the query table. |
| **Full replace, not patch** | The new `sqlQuery` completely replaces the old one — there is no partial/incremental update of individual clauses. |
| **Column schema may change** | If the new SQL query selects different columns (added, removed, renamed, or retyped), the query table's column list is recomputed. Reports and dashboards built on removed/renamed columns will break. |
| **Concurrent edit protection** | If the query table is already being edited by another schema-changing operation, the request is rejected with a "design edit in progress" error until the previous operation finishes. |
| **No `queryTableName` or `description` field** | This API cannot rename the query table or change its description — only the SQL and folder can be updated here. |
| **Dependency** | `<querytable-id>` → Get Query Tables or Get Query Table Details. `folderId` → Get Folder List. After editing, call Get Query Table Details to confirm the updated column schema. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Design Modify permission on the query table. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The query table does not belong to the specified workspace. | Confirm `<querytable-id>` belongs to `<workspace-id>`. |
| [7401](../../../foundations/error-codes.md#error-7401) | 400 | The SQL statement is not a valid/allowed SQL construct. | Only `SELECT` queries are permitted. |
| [7402](../../../foundations/error-codes.md#error-7402) | 400 | The SQL statement is invalid. | Verify SQL syntax and referenced object names. |
| [7403](../../../foundations/error-codes.md#error-7403) | 400 | Parsing of the SQL query failed. | Check for typos or unsupported SQL grammar. |
| [7404](../../../foundations/error-codes.md#error-7404) | 400 | Conversion of the SQL query to the internal execution engine failed. | Simplify the query or check for unsupported functions/constructs. |
| [7407](../../../foundations/error-codes.md#error-7407) | 400 | An invalid column was referenced in the `SELECT` clause. | Verify all column names exist in the source table(s). |
| [7409](../../../foundations/error-codes.md#error-7409) | 400 | An invalid/unknown table was referenced in the query. | Verify the table/view name matches an existing view in the workspace. |
| [7422](../../../foundations/error-codes.md#error-7422) | 400 | The query table is referenced as a source by a child view, preventing this type of structural change. | Review dependent views before making incompatible schema changes. |
| [7429](../../../foundations/error-codes.md#error-7429) | 400 | A design edit (schema change) is already in progress for this query table. | Wait for the in-progress operation to complete, then retry. |
| [7447](../../../foundations/error-codes.md#error-7447) | 400 | The query result would exceed the allowed row/column limit. | Add filters or reduce selected columns. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Query Tables overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Query Tables](get-query-tables.md), [Create Query Table](create-query-table.md), [Get Query Table Details](get-query-table-details.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/query-tables/edit-query-table.md).
