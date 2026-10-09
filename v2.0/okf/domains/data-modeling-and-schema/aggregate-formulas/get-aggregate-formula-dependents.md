---
type: API Endpoint
title: Get Aggregate Formula Dependents
description: "Returns all views, dashboards, and other aggregate formulas that depend on the specified aggregate formula, along with the parent table(s) it is built from."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/dependents"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - aggregate-formulas
  - get
  - metadata
api:
  operation_id: getAggregateFormulaDependents
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/dependents"
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
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Read permission on the workspace."
  error_codes:
    - 7301
    - 7428
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1aggregateformulas~1{formula-id}~1dependents/get"
    config_schema: null
    response_schema: GetAggregateFormulaDependentsResponse
  sdk_examples: "/sdk-examples/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-dependents.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/dependents`** - Get Aggregate Formula Dependents (Aggregate Formulas (Unified Metrics) / Data Modeling & Schema).

Returns all views, dashboards, and other aggregate formulas that depend on the specified aggregate formula, along with the parent table(s) it is built from. Use this before deleting or making breaking changes to a formula.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getAggregateFormulaDependents` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/dependents` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Read permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1aggregateformulas~1{formula-id}~1dependents/get`; response schema `GetAggregateFormulaDependentsResponse` |

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
| `childViews` | Array | Reports, charts, and pivot tables (non-dashboard views) that use this aggregate formula. Empty array if none. |
| `childViews[].viewId` | String | ID of the dependent view. |
| `childViews[].viewName` | String | Display name of the dependent view. |
| `childViews[].viewType` | String | Human-readable view type, e.g., `"Chart View"`, `"Pivot View"`. |
| `childViews[].viewTypeId` | Integer | Numeric view type ID (see [Common `viewTypeId` Values](#common-viewtypeid-values) below). |
| `parentTables` | Array | The base table(s) this aggregate formula is computed from (i.e., the table referenced in the `expression`). Typically contains a single entry — the owning table — but may include additional linked tables for cross-table aggregates. |
| `parentTables[].viewId` / `viewName` / `viewType` / `viewTypeId` | String / String / String / Integer | Same structure as `childViews`, but describing the source table rather than a dependent. |
| `aggregateFormulas` | Array | Other aggregate formulas that reference this one in their own expression (formula-on-formula dependencies). Empty array if none. |
| `aggregateFormulas[].formulaId` / `formulaName` | String / String | ID and name of the dependent aggregate formula. |
| `childDashboards` | Array | Dashboards (including tabbed dashboards) that include a widget referencing this formula. Empty array if none. |
| `childDashboards[].viewId` / `viewName` / `viewType` / `viewTypeId` | String / String / String / Integer | Standard view identification fields for the dashboard. |
| `childDashboards[].tabIds` | Array of String | **Only present when `viewType` is `"Tab"`** (a tabbed dashboard container). Lists the IDs of the individual dashboard tabs that use this formula. |

### Common `viewTypeId` Values

| `viewTypeId` | `viewType` |
|--------------|------------|
| `0` | Table |
| `2` | Chart View |
| `3` | Pivot View |
| `7` | Dashboard |
| `9` | Tab (tabbed dashboard container) |

## Notes from the OpenAPI specification

- Always call this API before the Delete Aggregate Formula API. The childViews, childDashboards and aggregateFormulas arrays together represent everything that would be removed by setting deleteDependentViews to true.
- parentTables describes what the formula is built from rather than what depends on it, which makes it useful for understanding the lineage of a metric before its expression is changed. No other dependents API in this suite returns lineage information.
- Several tabs of the same tabbed dashboard that use the metric are consolidated into a single childDashboards entry whose view type is Tab, carrying a tabIds array, rather than one entry per tab.
- Obtain the formula-id from the Get Unified Metrics in Workspace API or from the view-scoped Get Aggregate Formula API.

# Examples

## Sample Requests

**Case 1 — Get dependents of an aggregate formula used in a dashboard**

```http
GET /restapi/v2/workspaces/137687000271334001/aggregateformulas/137687000112449553/dependents HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Get dependents of a formula with no dependents (safe to delete)**

```http
GET /restapi/v2/workspaces/137687000271334001/aggregateformulas/137687000112449600/dependents HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — Formula used in a chart and a tabbed dashboard**

```json
{
  "status": "success",
  "summary": "Get aggregate formula dependents",
  "data": {
    "childViews": [
      {
        "viewName": "Chart_3_1",
        "viewId": "137687000112449496",
        "viewType": "Chart View",
        "viewTypeId": 2
      }
    ],
    "parentTables": [
      {
        "viewId": "137687000112449495",
        "viewName": "Table_3",
        "viewType": "Table",
        "viewTypeId": 0
      }
    ],
    "aggregateFormulas": [],
    "childDashboards": [
      {
        "viewId": "137687000112449498",
        "viewName": "Dashboard_1",
        "viewType": "Dashboard",
        "viewTypeId": 7
      },
      {
        "viewId": "137687000112449499",
        "viewName": "Tab Dashboard 1",
        "viewType": "Tab",
        "viewTypeId": 9,
        "tabIds": ["137687000112449500", "137687000112449501"]
      }
    ]
  }
}
```

**HTTP 200 OK — Formula with no dependents**

```json
{
  "status": "success",
  "summary": "Get aggregate formula dependents",
  "data": {
    "childViews": [],
    "parentTables": [
      {
        "viewId": "137687000112449600",
        "viewName": "Table_5",
        "viewType": "Table",
        "viewTypeId": 0
      }
    ],
    "aggregateFormulas": [],
    "childDashboards": []
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Aggregate Formula Dependents](../../../sdk-examples/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-dependents.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Always call before Delete Aggregate Formula** | The `childViews`, `childDashboards`, and `aggregateFormulas` arrays together represent everything that would be affected by `deleteDependentViews: true` on the Delete Aggregate Formula API. |
| **`parentTables` shows lineage, not dependents** | This is the only field in the response describing what the formula is built *from*, rather than what depends *on* it. Useful for understanding a formula's data lineage before editing its expression. |
| **Tabbed dashboards are consolidated** | Multiple tabs within the same tabbed dashboard that all use the formula are reported as a single `childDashboards` entry with `viewType: "Tab"` and a `tabIds` array, rather than one entry per tab. |
| **Dependency** | `<formula-id>` → Get Unified Metrics in Workspace or the view-scoped Get Aggregate Formula. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Read permission on the workspace. |
| [7428](../../../foundations/error-codes.md#error-7428) | 400 | The specified `<formula-id>` is not a valid aggregate formula, or does not belong to a view in this workspace. | Verify `<formula-id>` using Get Unified Metrics in Workspace. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Aggregate Formulas (Unified Metrics) overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Aggregate Formula](get-aggregate-formula-list.md), [Add Aggregate Formula](add-aggregate-formula.md), [Edit Aggregate Formula](edit-aggregate-formula.md), [Delete Aggregate Formula](delete-aggregate-formula.md), [Get Unified Metrics in Workspace](get-aggregate-formulas-in-workspace.md), [Get Aggregate Formula Value](get-aggregate-formula-value.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-dependents.md).
