---
type: API Endpoint
title: Get Aggregate Formula Value
description: Computes and returns the current value of the specified aggregate formula by executing its expression against the underlying data at request time.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/value"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - aggregate-formulas
  - get
  - metadata
api:
  operation_id: getAggregateFormulaValue
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/value"
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
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Read permission on the workspace and access to the columns/tables involved in the formula."
  error_codes:
    - 7301
    - 7428
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1aggregateformulas~1{formula-id}~1value/get"
    config_schema: null
    response_schema: GetAggregateFormulaValueResponse
  sdk_examples: "/sdk-examples/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-value.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/value`** - Get Aggregate Formula Value (Aggregate Formulas (Unified Metrics) / Data Modeling & Schema).

Computes and returns the current live value of the specified aggregate formula by executing its expression against the underlying data at request time.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getAggregateFormulaValue` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/value` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Read permission on the workspace and access to the columns/tables involved in the formula. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1aggregateformulas~1{formula-id}~1value/get`; response schema `GetAggregateFormulaValueResponse` |

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
| `{formula-id}` | string | ID of the formula. | [How to obtain](../../../foundations/identifiers.md#formula-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `formulaId` | String | ID of the aggregate formula queried. |
| `formulaName` | String | Display name of the aggregate formula. |
| `formulaValue` | String | The computed result of the formula's expression, evaluated live against the current data. Always returned as a string, regardless of whether the underlying result is numeric or decimal — parse according to the formula's `subtypeId`/`subtype` if numeric processing is required. |

## Notes from the OpenAPI specification

- The value is computed live rather than served from a cache. Each call re-executes the underlying aggregate query, so the latency grows with the size of the source tables and the complexity of the expression. Use it sparingly for large or complex metrics.
- Column-level access is needed in addition to workspace access. A caller can pass the workspace read check and still be refused when a column referred to by the expression is restricted from them by column-level sharing.
- formulaValue is always serialized as a string, whatever the result data type of the metric, so that precision is preserved. Parse it into a number when further calculation is needed.
- The owning view of the metric can be a regular table or a query table, and both are supported transparently.
- Obtain the formula-id from the Get Unified Metrics in Workspace API or from the view-scoped Get Aggregate Formula API.

# Examples

## Sample Requests

**Case 1 — Get the value of a total sales metric**

```http
GET /restapi/v2/workspaces/137687000271334001/aggregateformulas/137687000105964059/value HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Get the value of a metric built on a Query Table**

```http
GET /restapi/v2/workspaces/137687000271334001/aggregateformulas/137687000267960449/value HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — Shared user fetching a metric value**

```http
GET /restapi/v2/workspaces/137687000271334001/aggregateformulas/137687000105964061/value HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — Table-based aggregate**

```json
{
  "status": "success",
  "summary": "Get aggregate formula value",
  "data": {
    "formulaId": "137687000105964059",
    "formulaName": "Ag_1",
    "formulaValue": "1299947.06"
  }
}
```

**HTTP 200 OK — Query Table-based aggregate**

```json
{
  "status": "success",
  "summary": "Get aggregate formula value",
  "data": {
    "formulaId": "137687000267960449",
    "formulaName": "qt_agg1",
    "formulaValue": "480774.4600000001"
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Aggregate Formula Value](../../../sdk-examples/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-value.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Value is computed live, not cached** | Each call re-executes the underlying aggregate query against the current data. Expect latency proportional to the size of the source table(s) and complexity of the expression. |
| **Requires column-level access, not just workspace access** | Beyond basic workspace Read permission, the caller must have visibility into the specific columns referenced by the formula's expression. If any referenced column is restricted from the caller via column-level sharing, the request is forbidden. |
| **`formulaValue` is always a string** | Even for numeric/decimal results, the value is serialized as a string (e.g., `"1299947.06"`) to preserve precision — parse it into a number in your application if further calculation is needed. |
| **Works for both table-based and Query Table-based formulas** | The owning view of the formula can be a regular table or a [Query Table](../query-tables/overview.md); this API transparently supports both. |
| **Dependency** | `<formula-id>` → Get Unified Metrics in Workspace or the view-scoped Get Aggregate Formula. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission, or the user lacks access to a column/table involved in the formula. | Ensure the user is a Workspace Admin, or has Read permission on the workspace and visibility into all columns used by the formula. |
| [7428](../../../foundations/error-codes.md#error-7428) | 400 | The specified `<formula-id>` is not a valid aggregate formula. | Verify `<formula-id>` using Get Unified Metrics in Workspace. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Aggregate Formulas (Unified Metrics) overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Aggregate Formula](get-aggregate-formula-list.md), [Add Aggregate Formula](add-aggregate-formula.md), [Edit Aggregate Formula](edit-aggregate-formula.md), [Delete Aggregate Formula](delete-aggregate-formula.md), [Get Unified Metrics in Workspace](get-aggregate-formulas-in-workspace.md), [Get Aggregate Formula Dependents](get-aggregate-formula-dependents.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-value.md).
