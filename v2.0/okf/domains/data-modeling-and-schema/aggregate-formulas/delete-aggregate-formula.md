---
type: API Endpoint
title: Delete Aggregate Formula
description: Permanently deletes an aggregate formula from the specified view.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas/{formula-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - aggregate-formulas
  - delete
  - modeling
api:
  operation_id: deleteAggregateFormula
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas/{formula-id}"
  domain: data-modeling-and-schema
  group: aggregate-formulas
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
  rate_limit: 20 requests per user per minute (10-minute lockout on breach).
  error_codes:
    - 7107
    - 7160
    - 7173
    - 7301
    - 7319
    - 7428
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1aggregateformulas~1{formula-id}/delete"
    config_schema: DeleteAggregateFormulaConfig
    response_schema: null
  sdk_examples: "/sdk-examples/data-modeling-and-schema/aggregate-formulas/delete-aggregate-formula.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas/{formula-id}`** - Delete Aggregate Formula (Aggregate Formulas (Unified Metrics) / Data Modeling & Schema).

Permanently deletes an aggregate formula from the specified view. By default, deletion is blocked if the formula is currently used by any dependent view (report, chart, dashboard) or referenced by another aggregate formula.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deleteAggregateFormula` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas/{formula-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingdelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - optional |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| Rate limit | 20 requests per user per minute (10-minute lockout on breach). See [Rate limits](../../../foundations/rate-limits-and-quotas.md). |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1aggregateformulas~1{formula-id}/delete`; CONFIG schema `DeleteAggregateFormulaConfig` |

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
| `deleteDependentViews` | Boolean | No | `false` | If `true`, all dependent views/dashboards that reference this aggregate formula are also permanently deleted before the formula itself is removed. If `false`, deletion is blocked with error 7173 if any dependents exist. |

## Notes from the OpenAPI specification

- This API returns HTTP 204 No Content with no response body on success. There is no status or summary key to parse - treat the HTTP status code as the sole success indicator.
- Call the Get Aggregate Formula Dependents API first. Its childViews, childDashboards and aggregateFormulas arrays together represent everything that would be removed by setting deleteDependentViews to true.
- Setting deleteDependentViews to true is irreversible. Every dependent report, chart, pivot table, dashboard and referring aggregate formula is permanently deleted.
- This API is not idempotent. A formula ID that does not exist, or that was already deleted, returns an error rather than a silent success.
- This API is throttled at 20 requests per user per minute, with a ten-minute lockout when the limit is breached.
- Obtain the formula-id from the Get Aggregate Formula API or from the Get Unified Metrics in Workspace API.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Delete an aggregate formula with no dependents**

```http
DELETE /restapi/v2/workspaces/137687000271334001/views/137687000271334499/aggregateformulas/137687000271334553 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={}
```

**Case 2 — Delete an aggregate formula and cascade-delete all dependents**

```http
DELETE /restapi/v2/workspaces/137687000271334001/views/137687000271334499/aggregateformulas/137687000271334553 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"deleteDependentViews":true}
```

**Case 3 — White label portal user deleting an aggregate formula**

```http
DELETE /restapi/v2/workspaces/137687000271334001/views/137687000271334499/aggregateformulas/137687000271334553 HTTP/1.1
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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Delete Aggregate Formula](../../../sdk-examples/data-modeling-and-schema/aggregate-formulas/delete-aggregate-formula.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Delete Aggregate Formula returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Always check dependents first** | Use [Get Aggregate Formula Dependents](get-aggregate-formula-dependents.md) before deleting to see exactly which views, dashboards, and other aggregate formulas depend on this one. |
| **`deleteDependentViews: true` is permanent** | All dependent reports, charts, pivot tables, dashboards, and referencing aggregate formulas are permanently deleted. This cannot be undone. |
| **Not idempotent** | Attempting to delete a formula ID that does not exist (or was already deleted) returns an error, not a silent success. |
| **Dependency** | `<formula-id>` → Get Aggregate Formula or Get Unified Metrics in Workspace. Always call Get Aggregate Formula Dependents beforehand to assess impact. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7107](../../../foundations/error-codes.md#error-7107) | 400 | The specified formula ID does not exist as a column on this view. | Verify `<formula-id>` using Get Aggregate Formula. |
| [7160](../../../foundations/error-codes.md#error-7160) | 400 | Formula operations are not allowed for this user/view combination. | Ensure the user is a Workspace Admin or has Create Formula permission on the view. |
| [7173](../../../foundations/error-codes.md#error-7173) | 400 | The aggregate formula is currently used by one or more dependent views/dashboards/formulas; deletion blocked. | Use Get Aggregate Formula Dependents to identify dependents, then either remove them manually first or set `deleteDependentViews: true` to cascade delete. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Create Formula permission on the view. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. | Confirm `<view-id>` belongs to `<workspace-id>`. |
| [7428](../../../foundations/error-codes.md#error-7428) | 400 | The specified column is not a valid aggregate formula. | Verify `<formula-id>` refers to an aggregate formula, not a regular or custom formula column. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Aggregate Formulas (Unified Metrics) overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Aggregate Formula](get-aggregate-formula-list.md), [Add Aggregate Formula](add-aggregate-formula.md), [Edit Aggregate Formula](edit-aggregate-formula.md), [Get Unified Metrics in Workspace](get-aggregate-formulas-in-workspace.md), [Get Aggregate Formula Dependents](get-aggregate-formula-dependents.md), [Get Aggregate Formula Value](get-aggregate-formula-value.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/aggregate-formulas/delete-aggregate-formula.md).
