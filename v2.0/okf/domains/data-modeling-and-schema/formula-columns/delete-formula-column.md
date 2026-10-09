---
type: API Endpoint
title: Delete Custom Formula
description: Permanently deletes a custom formula column from the specified view.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas/{formula-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - formula-columns
  - delete
  - modeling
api:
  operation_id: deleteFormulaColumn
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas/{formula-id}"
  domain: data-modeling-and-schema
  group: formula-columns
  oauth_scopes:
    - ZohoAnalytics.modeling.delete
  org_id_header: required
  config_parameter:
    location: form
    required: false
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view."
  rate_limit: 30 requests per user per minute (10-minute lockout on breach).
  error_codes:
    - 7107
    - 7160
    - 7277
    - 7301
    - 7319
    - 7427
    - 7467
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1customformulas~1{formula-id}/delete"
    config_schema: DeleteFormulaColumnConfig
    response_schema: null
  sdk_examples: "/sdk-examples/data-modeling-and-schema/formula-columns/delete-formula-column.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas/{formula-id}`** - Delete Custom Formula (Custom Formula Columns / Data Modeling & Schema).

Permanently deletes a custom formula column from the specified view. By default, deletion is blocked if any dependent views (reports, charts, other formulas) reference this formula column.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deleteFormulaColumn` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas/{formula-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingdelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - optional |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| Rate limit | 30 requests per user per minute (10-minute lockout on breach). See [Rate limits](../../../foundations/rate-limits-and-quotas.md). |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1customformulas~1{formula-id}/delete`; CONFIG schema `DeleteFormulaColumnConfig` |

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
| `{formula-id}` | string | ID of the formula. | [How to obtain](../../../foundations/identifiers.md#formula-id) |

## CONFIG Parameters

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `deleteDependentViews` | Boolean | No | `false` | If `true`, all dependent views (reports, charts, pivot tables, other formula columns) that reference this formula are also permanently deleted. If `false`, deletion is blocked with error 7277 if any dependents exist. |

## Notes from the OpenAPI specification

- This API returns HTTP 204 No Content with no response body on success. There is no status or summary key to parse - treat the HTTP status code as the sole success indicator.
- This API is not idempotent. A formula ID that does not correspond to a formula column of the view, whether because it is a regular column or because it was already deleted, returns an error rather than a silent success.
- Setting deleteDependentViews to true is irreversible. Every dependent report, chart, pivot table and formula column that refers to this formula is permanently deleted.
- The request is rejected when the view is locked by an in-progress schema change. Retry once the lock clears.
- Formula columns are not supported on pipeline tables and such a request returns error 7467.
- This API is throttled at 30 requests per user per minute, with a ten-minute lockout when the limit is breached.
- Obtain the formula-id from the Get Custom Formulas API. The same ID can be passed as a column-id to the Get Column Dependents API to assess the impact before deleting.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Delete a formula column with no dependents**

```http
DELETE /restapi/v2/workspaces/20868000000040672/views/20868000000040795/customformulas/320862000000625897 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={}
```

**Case 2 — Delete a formula column and cascade-delete all dependent views**

```http
DELETE /restapi/v2/workspaces/20868000000040672/views/20868000000040795/customformulas/320862000000625897 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"deleteDependentViews":true}
```

**Case 3 — White label portal user deleting a formula column**

```http
DELETE /restapi/v2/workspaces/20868000000040672/views/20868000000040795/customformulas/320862000000625897 HTTP/1.1
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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Delete Custom Formula](../../../sdk-examples/data-modeling-and-schema/formula-columns/delete-formula-column.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Delete Custom Formula returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Not idempotent** | If `<formula-id>` does not correspond to a formula column on the view (e.g., it's a regular column, or already deleted), error 7107 (column not present) or 7427-equivalent "not a formula column" behaviour is returned rather than a silent success. |
| **`deleteDependentViews: true` is permanent** | All dependent reports, charts, pivot tables, and other formula columns that reference this formula are permanently deleted. This cannot be undone. |
| **DDL lock check** | If the view is locked due to an in-progress schema change, the request is rejected until the lock clears. |
| **Not supported on Pipeline Tables** | Deleting a formula column from a Pipeline Table view returns error 7467. |
| **Dependency** | `<formula-id>` → Get Custom Formulas. Before deleting, consider checking dependent views/formulas via [Get Column Dependents](../columns/get-column-dependents.md), since a formula column's ID can also be passed as a regular `<column-id>` to that API. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7107](../../../foundations/error-codes.md#error-7107) | 400 | The specified column ID does not exist in the view. | Verify `<formula-id>` using Get Custom Formulas. |
| [7160](../../../foundations/error-codes.md#error-7160) | 400 | Formula columns are not allowed for this user/view combination. | Ensure the user is a Workspace Admin or has Create Formula permission on the view. |
| [7277](../../../foundations/error-codes.md#error-7277) | 400 | The formula column has dependent views; deletion blocked. | Use Get Column Dependents to identify dependents, then either delete them manually first or set `deleteDependentViews: true` to cascade delete. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Create Formula permission on the view. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. | Confirm `<view-id>` belongs to `<workspace-id>`. |
| [7427](../../../foundations/error-codes.md#error-7427) | 400 | The specified column is not a custom formula column. | Verify `<formula-id>` refers to a formula column, not a regular column, using Get Custom Formulas. |
| [7467](../../../foundations/error-codes.md#error-7467) | 400 | Formula columns are not supported on Pipeline Tables. | This API only applies to standard tables/views. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Custom Formula Columns overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Custom Formulas](get-custom-formula-list.md), [Add Custom Formula](add-formula-column.md), [Edit Custom Formula](edit-formula-column.md), [Copy Custom Formulas](copy-formulas.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/formula-columns/delete-formula-column.md).
