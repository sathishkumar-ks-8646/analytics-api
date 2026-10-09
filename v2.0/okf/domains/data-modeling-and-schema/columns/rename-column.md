---
type: API Endpoint
title: Rename Column
description: Renames the specified column of a table.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - columns
  - put
  - modeling
api:
  operation_id: renameColumn
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}"
  domain: data-modeling-and-schema
  group: columns
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the workspace."
  error_codes:
    - 7092
    - 7107
    - 7111
    - 7157
    - 7164
    - 7301
    - 7439
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1columns~1{column-id}/put"
    config_schema: RenameColumnConfig
    response_schema: null
  sdk_examples: "/sdk-examples/data-modeling-and-schema/columns/rename-column.md"
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

**PUT `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}`** - Rename Column (Columns / Data Modeling & Schema).

Renames the specified column in the given table. The column is identified by its numeric column ID in the URL.

From the OpenAPI specification:

Renames the specified column of a table. The column is identified by its column ID in the request URL.

Every view, formula and report that refers to the column is updated automatically to use the new name.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `renameColumn` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1columns~1{column-id}/put`; CONFIG schema `RenameColumnConfig` |

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
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |
| `{column-id}` | string | ID of the column. | [How to obtain](../../../foundations/identifiers.md#column-id) |

## CONFIG Parameters

| Parameter | Type | Mandatory | Description |
|-----------|------|-----------|-------------|
| `columnName` | String | **Yes** | New display name for the column. Must be unique within the table. |

## Notes from the OpenAPI specification

- This API returns HTTP 204 No Content with no response body on success. There is no status or summary key to parse - treat the HTTP status code as the sole success indicator.
- The rename propagates automatically. Reports, charts, pivot tables and formula columns that refer to this column are updated to use the new name, so no manual update of the dependent views is needed.
- Renaming a column to its existing name succeeds without an error.
- The request is rejected with error 7092 when the table is locked by an in-progress import.
- Columns of a snapshot table cannot be renamed and return error 7164.
- An unknown column ID returns error 7107. Verify the column-id using the Get Table Metadata API.
- Although a rename is safe because every reference is updated, calling the Get Column Dependents API first is good practice before a bulk rename.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Rename a column**

```http
PUT /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns/7617000000508026 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"columnName":"Geographic Region"}
```

**Case 2 — White label portal user renaming a column**

```http
PUT /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns/7617000000508026 HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"columnName":"Client Region"}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Rename Column](../../../sdk-examples/data-modeling-and-schema/columns/rename-column.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Unlike Add Column (which returns an HTTP 200 with a JSON body containing `columnId`), Rename Column returns a bare HTTP `204 No Content` — do not expect a `status`/`summary` field on success. |
| **Rename propagates to dependent views** | Reports, charts, pivot tables, and formula columns that reference this column are automatically updated to use the new column name. No manual update of dependent views is needed. |
| **Renaming to the same name** | Succeeds without error (idempotent for the name). |
| **DDL lock check** | If the table is locked due to an in-progress import, the request is rejected with error 7092. |
| **Snapshot tables** | Columns in snapshot tables cannot be renamed (error 7164). |
| **Column not found** | If the column ID does not exist in the table, error 7107 is returned. Use Get Table Metadata to verify the `columnId`. |
| **Dependency** | `<view-id>` → Get View List. `<column-id>` → Get Table Metadata (to find the column's numeric ID). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7092](../../../foundations/error-codes.md#error-7092) | 400 | DDL lock is active on the table. | Wait for the in-progress operation to complete. |
| [7107](../../../foundations/error-codes.md#error-7107) | 400 | The specified column does not exist in the table. | Verify the `<column-id>` using Get Table Metadata. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | A column with the new name already exists in the table. | Use a unique column name within the table. |
| [7157](../../../foundations/error-codes.md#error-7157) | 400 | Column name already exists. | Use a unique `columnName` within the table. |
| [7164](../../../foundations/error-codes.md#error-7164) | 400 | The table is a snapshot table; columns cannot be renamed. | Snapshot tables are read-only schema-wise. Create a new table if schema changes are needed. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Design Modify permission on the workspace. |
| [7439](../../../foundations/error-codes.md#error-7439) | 400 | The view is not a table. | Provide the view ID of a table. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Columns overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Add Column](add-column.md), [Delete Column](delete-column.md), [Hide Columns](hide-columns.md), [Show Columns](show-columns.md), [Get Column Dependents](get-column-dependents.md), [Sort Data by Columns](sort-data-by-columns.md), [Reorder Columns](reorder-columns.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/columns/rename-column.md).
