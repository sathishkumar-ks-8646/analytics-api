---
type: API Endpoint
title: Delete Column
description: Permanently deletes a column from the specified table.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - columns
  - delete
  - modeling
api:
  operation_id: deleteColumn
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}"
  domain: data-modeling-and-schema
  group: columns
  oauth_scopes:
    - ZohoAnalytics.modeling.delete
  org_id_header: required
  config_parameter:
    location: form
    required: false
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the workspace."
  error_codes:
    - 7092
    - 7107
    - 7277
    - 7301
    - 7439
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1columns~1{column-id}/delete"
    config_schema: DeleteColumnConfig
    response_schema: null
  sdk_examples: "/sdk-examples/data-modeling-and-schema/columns/delete-column.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}`** - Delete Column (Columns / Data Modeling & Schema).

Permanently deletes a column from the specified table. By default, deletion is blocked if any dependent views (reports, charts, formulas) reference this column. You can override this by setting `deleteDependentViews` to `true`.

From the OpenAPI specification:

Permanently deletes a column from the specified table.

By default the deletion is blocked when any dependent view, report, chart or formula refers to the column. Set `deleteDependentViews` to true to delete those dependents along with the column.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deleteColumn` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingdelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - optional |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1columns~1{column-id}/delete`; CONFIG schema `DeleteColumnConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.delete`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |
| `{column-id}` | string | ID of the column. | [How to obtain](../../../foundations/identifiers.md#column-id) |

## CONFIG Parameters

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `deleteDependentViews` | Boolean | No | `false` | If `true`, all dependent views (reports, charts, pivot tables, formulas) that reference this column are also permanently deleted. If `false`, the deletion is blocked with error 7277 if any dependents exist. |

## Notes from the OpenAPI specification

- This API returns HTTP 204 No Content with no response body on success. There is no status or summary key to parse - treat the HTTP status code as the sole success indicator.
- Call the Get Column Dependents API before deleting. The views, custom formulas and aggregate formulas it lists determine whether a safe deletion or a cascade deletion is appropriate.
- Setting deleteDependentViews to true is irreversible. Every dependent view, report, chart, pivot table, query table and formula column is permanently deleted along with the column.
- The request is rejected with error 7092 when the table is locked by an in-progress import.
- An unknown column ID returns error 7107.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Delete a column with no dependents**

```http
DELETE /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns/7617000000508026 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={}
```

**Case 2 — Delete a column and all its dependent views**

```http
DELETE /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns/7617000000508026 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"deleteDependentViews":true}
```

**Case 3 — White label portal user deleting a column**

```http
DELETE /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns/7617000000508026 HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Delete Column](../../../sdk-examples/data-modeling-and-schema/columns/delete-column.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Delete Column returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Use Get Column Dependents first** | Before deleting, call [Get Column Dependents](get-column-dependents.md) to discover all views and formulas that reference this column. This helps decide whether to proceed with `deleteDependentViews=false` (safe) or `deleteDependentViews=true` (cascade delete). |
| **`deleteDependentViews=true` is permanent** | All dependent views (reports, charts, pivot tables, query tables, formula columns) are permanently deleted along with the column. This cannot be undone. |
| **DDL lock check** | If the table is locked due to an in-progress import, the request is rejected with error 7092. |
| **Column not found** | If the column ID does not exist in the table, error 7107 is returned. |
| **Dependency** | `<view-id>` → Get View List. `<column-id>` → Get Table Metadata. Use Get Column Dependents to assess impact before deletion. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7092](../../../foundations/error-codes.md#error-7092) | 400 | DDL lock is active on the table. | Wait for the in-progress operation to complete. |
| [7107](../../../foundations/error-codes.md#error-7107) | 400 | The specified column does not exist in the table. | Verify `<column-id>` using Get Table Metadata. |
| [7277](../../../foundations/error-codes.md#error-7277) | 400 | The column has dependent views; deletion blocked. | Call Get Column Dependents to identify them, then either delete them manually first or set `deleteDependentViews: true` to cascade delete. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Design Modify permission on the workspace. |
| [7439](../../../foundations/error-codes.md#error-7439) | 400 | The view is not a table. | Provide the view ID of a table. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Columns overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Add Column](add-column.md), [Rename Column](rename-column.md), [Hide Columns](hide-columns.md), [Show Columns](show-columns.md), [Get Column Dependents](get-column-dependents.md), [Sort Data by Columns](sort-data-by-columns.md), [Reorder Columns](reorder-columns.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/columns/delete-column.md).
