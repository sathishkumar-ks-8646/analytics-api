---
type: API Endpoint
title: Add Aggregate Formula
description: Creates a new aggregate formula owned by the specified view.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - aggregate-formulas
  - post
  - modeling
api:
  operation_id: addAggregateFormula
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas"
  domain: data-modeling-and-schema
  group: aggregate-formulas
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
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view."
  rate_limit: 20 requests per user per minute (10-minute lockout on breach).
  error_codes:
    - 7112
    - 7113
    - 7115
    - 7116
    - 7160
    - 7301
    - 7319
    - 8079
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1aggregateformulas/post"
    config_schema: AddAggregateFormulaConfig
    response_schema: AddAggregateFormulaResponse
  sdk_examples: "/sdk-examples/data-modeling-and-schema/aggregate-formulas/add-aggregate-formula.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas`** - Add Aggregate Formula (Aggregate Formulas (Unified Metrics) / Data Modeling & Schema).

Creates a new aggregate formula owned by the specified view.

From the OpenAPI specification:

Creates a new aggregate formula owned by the specified view.

Synonyms and a priority ranking can be supplied so that the metric is matched to natural-language queries by the search and insight features.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `addAggregateFormula` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| Rate limit | 20 requests per user per minute (10-minute lockout on breach). See [Rate limits](../../../foundations/rate-limits-and-quotas.md). |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1aggregateformulas/post`; CONFIG schema `AddAggregateFormulaConfig`; response schema `AddAggregateFormulaResponse` |

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
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

| Parameter | Type | Mandatory | Max Length | Default | Description |
|-----------|------|-----------|------------|---------|-------------|
| `formulaName` | String | **Yes** | 100 chars | — | Display name for the new aggregate formula. Must be unique within the workspace. |
| `expression` | String | **Yes** | 50,000 chars | — | The aggregate formula expression, using an aggregate function (e.g., `sum()`, `max()`, `min()`, `mean()`, `count()`, `count_distinct()`, `count_if()`) applied to one or more columns, referenced as `"TableName"."ColumnName"`. |
| `description` | String | No | 250 chars | `""` | Description of the aggregate formula. |
| `synonyms` | JSONArray of String | No | — | `[]` | Alternate names/keywords for this metric, used by natural-language search and insight suggestion features to match user queries to this formula. |
| `columnPriority` | Integer (enum) | No | — | `0` (Low) | Ranking priority of this formula when multiple metrics could match a natural-language query. See [Column Priority Values](#column-priority-values) below. |

### Column Priority Values

| `columnPriority` Value | Priority Level |
|---------------------------|-----------------|
| `0` (default) | Low |
| `1` | Medium |
| `2` | High |

## Notes from the OpenAPI specification

- The expression is validated at creation time. The aggregate function names and the referenced column names are checked before the formula is created.
- formulaName must be unique within the workspace, not merely within the view. A duplicate name is rejected.
- The result data type is inferred from the aggregate function and the source columns and cannot be declared.
- synonyms and columnPriority are metadata for natural-language search and generated insights only. They have no effect on the computed value of the formula.
- When the expression refers to columns of a table other than the one owning the view, that table must already be connected through a lookup relationship, otherwise the reference cannot be resolved.
- This API is throttled at 20 requests per user per minute, with a ten-minute lockout when the limit is breached.
- Confirm the table and column names through the Get Table Metadata API before calling. The returned formulaId can afterwards be passed to the Get Aggregate Formula Value API.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `formulaId` | String | Unique ID assigned to the newly created aggregate formula. Use as `<formula-id>` for subsequent Edit/Delete calls, and for the workspace-scoped Get Dependents / Get Value APIs. |
| `formulaName` | String | The display name of the aggregate formula, echoing the `formulaName` value from the request. |

# Examples

## Sample Requests

**Case 1 — Simple sum aggregate**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000271334499/aggregateformulas HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"formulaName":"Total Sales","expression":"sum(\"Table_1\".\"Sales\")"}
```

**Case 2 — Aggregate with synonyms and high priority for NLP search**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000271334499/aggregateformulas HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"formulaName":"Average Order Value","expression":"mean(\"Table_1\".\"Order Amount\")","description":"Average value of a single order","synonyms":["AOV","avg order value","mean order amount"],"columnPriority":2}
```

**Case 3 — White label portal user adding a count_distinct aggregate**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000271334499/aggregateformulas HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"formulaName":"Unique Regions","expression":"count_distinct(\"Table_1\".\"Region\")"}
```

## Sample Responses

**HTTP 200 OK**

```json
{
  "status": "success",
  "summary": "Aggregate formula has been added successfully.",
  "data": {
    "formulaId": "137687000271334553",
    "formulaName": "Total Sales"
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Add Aggregate Formula](../../../sdk-examples/data-modeling-and-schema/aggregate-formulas/add-aggregate-formula.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Expression is validated at creation time** | Aggregate function names and referenced column names are checked before the formula is created. |
| **`formulaName` must be unique** | Duplicate aggregate formula names within the same workspace are rejected. |
| **Result data type (`subtypeId`) is inferred, not declared** | There is no data-type parameter; the type is derived from the aggregate function and the source column(s). |
| **`synonyms` and `columnPriority` are NLP/insights metadata only** | These fields do not affect the computed value of the formula — they only influence how the formula surfaces in natural-language search and auto-generated insights. |
| **Cross-table aggregates require a lookup relationship** | If the expression references columns from a table other than the owning view's table, that table must already be linked via a [lookup relationship](../lookups-and-relationships/overview.md). |
| **Dependency** | `<view-id>` → Get View List. Column/table names used in `expression` → Get Table Metadata. After creation, the returned `formulaId` can be queried via [Get Aggregate Formula Value](get-aggregate-formula-value.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7112](../../../foundations/error-codes.md#error-7112) | 400 | The formula expression could not be parsed (syntax error). | Review the expression for correct aggregate function syntax and column quoting. |
| [7113](../../../foundations/error-codes.md#error-7113) | 400 | The expression references an unknown/unsupported function. | Verify the aggregate function name (e.g., `sum`, `mean`, `max`, `min`, `count`, `count_distinct`, `count_if`). |
| [7115](../../../foundations/error-codes.md#error-7115) | 400 | The expression references a column that does not exist, or the formula is otherwise invalid. | Verify all table/column names referenced in the expression. |
| [7116](../../../foundations/error-codes.md#error-7116) | 400 | The expression references a column that does not exist, or the formula is otherwise invalid. | Verify all table/column names referenced in the expression. |
| [7160](../../../foundations/error-codes.md#error-7160) | 400 | Formula columns/aggregate formulas are not allowed for this user/view combination. | Ensure the user is a Workspace Admin or has Create Formula permission on the view. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Create Formula permission on the view. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. | Confirm `<view-id>` belongs to `<workspace-id>`. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | A required attribute (`expression` or `formulaName`) is missing from CONFIG. | Ensure both `formulaName` and `expression` are provided. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Aggregate Formulas (Unified Metrics) overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Aggregate Formula](get-aggregate-formula-list.md), [Edit Aggregate Formula](edit-aggregate-formula.md), [Delete Aggregate Formula](delete-aggregate-formula.md), [Get Unified Metrics in Workspace](get-aggregate-formulas-in-workspace.md), [Get Aggregate Formula Dependents](get-aggregate-formula-dependents.md), [Get Aggregate Formula Value](get-aggregate-formula-value.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/aggregate-formulas/add-aggregate-formula.md).
