---
type: API Endpoint
title: Remove Lookup
description: Removes the existing lookup relationship from the specified child column.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - lookups-and-relationships
  - delete
  - modeling
api:
  operation_id: removeLookup
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup"
  domain: data-modeling-and-schema
  group: lookups-and-relationships
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: false
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the workspace."
  error_codes:
    - 7107
    - 7301
    - 7319
    - 7367
    - 7378
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1columns~1{column-id}~1lookup/delete"
    config_schema: RemoveLookupConfig
    response_schema: null
  sdk_examples: "/sdk-examples/data-modeling-and-schema/lookups-and-relationships/remove-lookup.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup`** - Remove Lookup (Lookups & Relationships / Data Modeling & Schema).

Removes the existing lookup relationship from the specified child column. Once removed, the child column no longer references the parent table, and multi-table views spanning these two tables may break.

By default, if any reports, charts, pivot tables, or query tables depend on this lookup relationship (i.e., they join the child and parent tables), the removal is blocked. Set `deleteDependentViews` to `true` to cascade-delete those dependent views along with the lookup.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `removeLookup` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - optional |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1columns~1{column-id}~1lookup/delete`; CONFIG schema `RemoveLookupConfig` |

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

## URL Parameters

| Parameter | Description |
|-----------|-------------|
| `<workspace-id>` | Numeric ID of the workspace. |
| `<view-id>` | Numeric ID of the **child table** that owns the lookup column. |
| `<column-id>` | Numeric ID of the **child column** whose lookup relationship is to be removed. |

## CONFIG Parameters

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `deleteDependentViews` | Boolean | No | `false` | If `false`, the removal is blocked with error 7367 if any views (reports, charts, pivot tables, query tables) depend on this lookup. If `true`, all dependent views are permanently deleted along with the lookup. |

## Notes from the OpenAPI specification

- This API returns HTTP 204 No Content with no response body on success. There is no status or summary key to parse - treat the HTTP status code as the sole success indicator.
- Call the Get Column Dependents API on the child column before removing the relationship, to discover which views join across it. That list determines whether a safe removal or a cascading removal is appropriate.
- Setting deleteDependentViews to true is irreversible. Every multi-table report, chart, pivot table and query table built across the two tables through this lookup is permanently deleted and cannot be recovered.
- This API is not idempotent. When no lookup is defined on the column at the time of the call, error 7378 is returned rather than a silent success.
- A column holds at most one lookup, but when the internal model has recorded several relation IDs for the same column, for example after a migration, all of them are removed in a single atomic transaction.
- After a successful removal, the relationship line between the two tables disappears from the Schema View of the workspace.
- Resolve the IDs in this order: Get View List for the view-id, Get Table Metadata for the column-id, then Get Column Dependents to assess the impact.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON body (see [Error Codes](add-lookup.md#error-codes) below).

# Examples

## Sample Requests

**Case 1 — Remove a lookup (safe mode — fails if dependents exist)**

```http
DELETE /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns/7617000000508026/lookup HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={}
```

**Case 2 — Remove a lookup and cascade-delete all dependent views**

```http
DELETE /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns/7617000000508026/lookup HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"deleteDependentViews":true}
```

**Case 3 — White label portal user removing a lookup**

```http
DELETE /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns/7617000000508026/lookup HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse; the absence of an error response (4xx/5xx with a `status: "failure"` body) is the sole success indicator.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Remove Lookup](../../../sdk-examples/data-modeling-and-schema/lookups-and-relationships/remove-lookup.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Like Add Lookup, Remove Lookup returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. Check only the HTTP status code. |
| **Always check dependents before removing** | Use the [Get Column Dependents](../columns/get-column-dependents.md) API on `<column-id>` to discover which views join on this lookup relationship. This helps decide between `deleteDependentViews: false` (safe check) and `deleteDependentViews: true` (cascade). |
| **`deleteDependentViews: true` is permanent** | All dependent multi-table reports, charts, pivot tables, and query tables that span the child and reference tables via this lookup are permanently deleted. This cannot be undone. |
| **Not idempotent — no lookup means error** | If no lookup is defined on the child column at the time of the call, error 7378 is returned. This API does not silently succeed when there is nothing to remove. |
| **All lookup relationships on the column are removed** | A column can have at most one lookup, but if the internal model has recorded multiple relation IDs for the same column (e.g., due to migrations), all of them are removed in a single atomic transaction. |
| **Schema View update** | After a successful removal, the relationship line between the tables disappears from the workspace's Schema View. |
| **Dependency chain** | `<workspace-id>` → Get Workspace Info. `<view-id>` → Get View List. `<column-id>` → Get Table Metadata. Before removing, call Get Column Dependents to assess impact. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7107](../../../foundations/error-codes.md#error-7107) | 400 | The specified child column (`<column-id>`) does not exist in the child table. | Verify `<column-id>` using Get Table Metadata. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Design Modify permission on the workspace. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The child table (`<view-id>`) does not belong to the specified workspace. | Confirm `<view-id>` is a table within `<workspace-id>`. |
| [7367](../../../foundations/error-codes.md#error-7367) | 400 | The lookup is used by one or more dependent views; removal blocked. | Call Get Column Dependents to identify dependent views. Either delete them manually first, or set `deleteDependentViews: true` to cascade-delete them automatically. |
| [7378](../../../foundations/error-codes.md#error-7378) | 400 | No lookup relationship is defined on this column. | Verify the correct `<column-id>` and `<view-id>`. The lookup may have already been removed. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Lookups & Relationships overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Add Lookup](add-lookup.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/lookups-and-relationships/remove-lookup.md).
