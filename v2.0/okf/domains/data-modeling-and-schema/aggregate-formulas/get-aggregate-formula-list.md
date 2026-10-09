---
type: API Endpoint
title: Get Aggregate Formula
description: Returns the aggregate formulas owned by the specified view.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - aggregate-formulas
  - get
  - metadata
api:
  operation_id: getAggregateFormulaList
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas"
  domain: data-modeling-and-schema
  group: aggregate-formulas
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view."
  rate_limit: 30 requests per user per minute (10-minute lockout on breach).
  error_codes:
    - 7301
    - 7319
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1aggregateformulas/get"
    config_schema: null
    response_schema: GetAggregateFormulaListResponse
  sdk_examples: "/sdk-examples/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-list.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas`** - Get Aggregate Formula (Aggregate Formulas (Unified Metrics) / Data Modeling & Schema).

Returns the list of aggregate formulas defined on the specified view.

> This API has no CONFIG parameter.

From the OpenAPI specification:

Returns the aggregate formulas owned by the specified view. An aggregate formula, also called a unified metric, produces a single summarized value by applying an aggregate function across the rows of a table, and can be reused across the reports, charts and dashboards of the workspace as a single source of truth for a business metric.

This listing is scoped to one view. Use the Get Unified Metrics in Workspace API for a workspace-wide catalogue.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getAggregateFormulaList` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| Rate limit | 30 requests per user per minute (10-minute lockout on breach). See [Rate limits](../../../foundations/rate-limits-and-quotas.md). |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1aggregateformulas/get`; response schema `GetAggregateFormulaListResponse` |

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
|-------|------|--------------|
| `aggregateFormulas` | Array | List of aggregate formulas owned by this view. Empty array if none exist. |
| `aggregateFormulas[].formulaId` | String | Unique ID of the aggregate formula. Use as `<formula-id>` for Edit/Delete Aggregate Formula (view-scoped) and for the workspace-scoped Get Dependents / Get Value APIs. |
| `aggregateFormulas[].formulaName` | String | Display name of the aggregate formula. |
| `aggregateFormulas[].expression` | String | The aggregate expression (e.g., `sum("Table_1"."Sales")`). Empty string if the calling user lacks edit permission on the formula. |
| `aggregateFormulas[].description` | String | Description of the formula. Empty string if not set. |
| `aggregateFormulas[].subtypeId` | Integer | Internal numeric code for the result data type of the formula. See [Subtype Values](#subtype-values) below. |
| `aggregateFormulas[].subtypeName` | String | Display-form internal code for the result data type (e.g., `"NUMBER"`, `"DECIMAL_NUMBER"`). Matches the `dataType` values used in [Add Column](../columns/add-column.md). |

### Subtype Values

| `subtypeId` | `subtypeName` | Typical Cause |
|-------------|----------------|----------------|
| `4` | `NUMBER` | Integer-producing aggregates, e.g. `count()`, `count_distinct()`, `count_if()`, or boolean-style conditional expressions. |
| `6` | `DECIMAL_NUMBER` | Decimal-producing aggregates, e.g. `sum()`, `mean()`, `max()`, `min()` on decimal/currency source columns. |

> The exact `subtypeId`/`subtypeName` produced depends on the aggregate function used and the data type of the referenced column(s) — it is inferred automatically and cannot be explicitly set.

## Notes from the OpenAPI specification

- The visibility of the expression is gated by permission. A user with only view or share access sees expression as an empty string, while formulaId, formulaName and the remaining metadata are still returned.
- This listing covers only the formulas owned by the view in the request URL. Use the Get Unified Metrics in Workspace API to see every aggregate formula of the workspace, including those owned by other views.
- The display-form data type is returned here under the key subtypeName, whereas the workspace-scoped listing returns the same information under the key subtype. Account for that difference when parsing both responses.
- The result data type is inferred from the aggregate function and the source columns and cannot be set explicitly.
- This API is throttled at 30 requests per user per minute, with a ten-minute lockout when the limit is breached.
- Obtain the view-id from the Get View List API. The formulaId values feed into the view-scoped Edit and Delete APIs and into the workspace-scoped Get Dependents and Get Value APIs.

# Examples

## Sample Requests

**Case 1 — Get all aggregate formulas on a view**

```http
GET /restapi/v2/workspaces/137687000271334001/views/137687000271334499/aggregateformulas HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White label portal user fetching aggregate formulas**

```http
GET /restapi/v2/workspaces/137687000271334001/views/137687000271334499/aggregateformulas HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — User with edit permission (expression visible)**

```json
{
  "status": "success",
  "summary": "Get aggregate formulas",
  "data": {
    "aggregateFormulas": [
      {
        "formulaId": "137687000271334553",
        "formulaName": "Ag_1",
        "expression": "sum(\"Table_1\".\"Sales\")",
        "description": "",
        "subtypeId": 6,
        "subtypeName": "DECIMAL_NUMBER"
      },
      {
        "formulaId": "137687000271334555",
        "formulaName": "Ag_2",
        "expression": "count_distinct(\"Table_1\".\"Region\")",
        "description": "",
        "subtypeId": 4,
        "subtypeName": "NUMBER"
      }
    ]
  }
}
```

**HTTP 200 OK — View with no aggregate formulas**

```json
{
  "status": "success",
  "summary": "Get aggregate formulas",
  "data": {
    "aggregateFormulas": []
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Aggregate Formula](../../../sdk-examples/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-list.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Expression visibility is permission-gated** | Users with only view/share access (no edit permission) will see `expression: ""` even though `formulaId`, `formulaName`, and other metadata are still returned. |
| **View-scoped, not workspace-wide** | This API only lists formulas owned by `<view-id>`. To see all aggregate formulas across the entire workspace (including those owned by other views), use [Get Unified Metrics in Workspace](get-aggregate-formulas-in-workspace.md). |
| **Dependency** | `<view-id>` → Get View List. `formulaId` values feed into Edit/Delete Aggregate Formula, as well as the workspace-scoped Get Aggregate Formula Dependents and Get Aggregate Formula Value APIs. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Create Formula permission on the view. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. | Confirm `<view-id>` belongs to `<workspace-id>`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Aggregate Formulas (Unified Metrics) overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Add Aggregate Formula](add-aggregate-formula.md), [Edit Aggregate Formula](edit-aggregate-formula.md), [Delete Aggregate Formula](delete-aggregate-formula.md), [Get Unified Metrics in Workspace](get-aggregate-formulas-in-workspace.md), [Get Aggregate Formula Dependents](get-aggregate-formula-dependents.md), [Get Aggregate Formula Value](get-aggregate-formula-value.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-list.md).
