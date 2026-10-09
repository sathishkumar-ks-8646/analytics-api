---
type: API Endpoint
title: Get Unified Metrics in Workspace
description: "Returns every aggregate formula across all the views and tables of the workspace, together with the table that owns each one."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/aggregateformulas"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - aggregate-formulas
  - get
  - metadata
api:
  operation_id: getAggregateFormulasInWorkspace
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/aggregateformulas"
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
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1aggregateformulas/get"
    config_schema: null
    response_schema: GetAggregateFormulasInWorkspaceResponse
  sdk_examples: "/sdk-examples/data-modeling-and-schema/aggregate-formulas/get-aggregate-formulas-in-workspace.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/aggregateformulas`** - Get Unified Metrics in Workspace (Aggregate Formulas (Unified Metrics) / Data Modeling & Schema).

Returns the full list of aggregate formulas (Unified Metrics) across **every** view/table in the workspace, along with the table that owns each formula. Use this API when you need a workspace-wide inventory of all metrics rather than the formulas owned by a single view.

> **Renamed for clarity:** This API corresponds to the underlying `/aggregateformulas` workspace-level endpoint. It has been documented here as **"Get Unified Metrics in Workspace"** to better reflect its purpose as a workspace-wide metrics catalogue, distinct from the view-scoped [Get Aggregate Formula](get-aggregate-formula-list.md) API.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getAggregateFormulasInWorkspace` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/aggregateformulas` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Read permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1aggregateformulas/get`; response schema `GetAggregateFormulasInWorkspaceResponse` |

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

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `aggregateFormulas` | Array | List of every aggregate formula in the workspace, regardless of which view owns it. |
| `aggregateFormulas[].formulaId` | String | Unique ID of the aggregate formula. Use as `<formula-id>` for Get Aggregate Formula Dependents and Get Aggregate Formula Value. |
| `aggregateFormulas[].formulaName` | String | Display name of the formula. |
| `aggregateFormulas[].expression` | String | The aggregate expression. Returned as an **empty string** if the calling user does not have edit permission on the formula. |
| `aggregateFormulas[].description` | String | Description of the formula. Empty string if not set. |
| `aggregateFormulas[].subtypeId` | Integer | Internal numeric code for the formula's result data type. See [Subtype Values](get-aggregate-formula-list.md#subtype-values). |
| `aggregateFormulas[].subtype` | String | Display-form internal code for the result data type (e.g., `"NUMBER"`, `"DECIMAL_NUMBER"`). **Note:** this field is named `subtype` here, not `subtypeName` as in the view-scoped Get Aggregate Formula API — the underlying data is identical, only the JSON key differs between the two APIs. |
| `aggregateFormulas[].tableId` | String | ID of the table/view that owns this aggregate formula. Cross-reference with Get View List. |
| `aggregateFormulas[].tableName` | String | Display name of the owning table/view. |
| `aggregateFormulas[].createdBy` | String | Email address of the user who created the formula. |
| `aggregateFormulas[].modifiedTime` | String | Epoch milliseconds of the last modification to the formula. |

## Notes from the OpenAPI specification

- The display-form data type is returned here under the key subtype, whereas the view-scoped Get Aggregate Formula API returns the same information under the key subtypeName. Always check which endpoint you are parsing.
- The visibility of the expression is gated per formula. A user without edit permission on a given metric sees expression as an empty string for that entry, even when the other metadata is visible.
- The listing includes the metrics owned by query tables as well as those owned by regular tables, so tableName may name a query table.
- Read permission on the workspace is sufficient for this API, unlike the view-scoped create, edit and delete APIs, which need Create Formula permission.
- Cross-reference tableId against the Get View List and Get Table Metadata APIs to inspect the schema of the owning table. The formulaId values feed into the Get Aggregate Formula Dependents and Get Aggregate Formula Value APIs.

# Examples

## Sample Requests

**Case 1 — Get all Unified Metrics in the workspace**

```http
GET /restapi/v2/workspaces/137687000271334001/aggregateformulas HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White label portal Shared User with restricted view of expressions**

```http
GET /restapi/v2/workspaces/137687000271334001/aggregateformulas HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — Workspace Admin (full expression visibility)**

```json
{
  "status": "success",
  "summary": "Get aggregate formulas in workspace",
  "data": {
    "aggregateFormulas": [
      {
        "formulaId": "137687000271334557",
        "formulaName": "Ag_3",
        "expression": "max(\"Table_1\".\"Cost\")",
        "description": "",
        "subtypeId": 6,
        "subtype": "DECIMAL_NUMBER",
        "tableId": "137687000271334499",
        "tableName": "Table_1",
        "createdBy": "sales.admin@zylker.com",
        "modifiedTime": "1783507397220"
      },
      {
        "formulaId": "137687000271334569",
        "formulaName": "qt_agg1",
        "expression": "sum(\"QT1\".\"Cost\")",
        "description": "",
        "subtypeId": 6,
        "subtype": "DECIMAL_NUMBER",
        "tableId": "137687000271334508",
        "tableName": "QT1",
        "createdBy": "sales.admin@zylker.com",
        "modifiedTime": "1783507397220"
      }
    ]
  }
}
```

**HTTP 200 OK — Shared User (expression hidden — empty string)**

```json
{
  "status": "success",
  "summary": "Get aggregate formulas in workspace",
  "data": {
    "aggregateFormulas": [
      {
        "formulaId": "137687000271334207",
        "formulaName": "Ag_3",
        "expression": "",
        "description": "",
        "subtypeId": 6,
        "subtype": "DECIMAL_NUMBER",
        "tableId": "137687000271334149",
        "tableName": "Table_1",
        "createdBy": "sales.admin@zylker.com",
        "modifiedTime": "1783507040473"
      }
    ]
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Unified Metrics in Workspace](../../../sdk-examples/data-modeling-and-schema/aggregate-formulas/get-aggregate-formulas-in-workspace.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Field name discrepancy: `subtype` vs `subtypeName`** | This workspace-scoped API returns the display-form data type under the key `subtype`, while the view-scoped [Get Aggregate Formula](get-aggregate-formula-list.md) API returns the same information under the key `subtypeName`. Both represent identical data — account for this naming difference when parsing responses from both APIs. |
| **Expression visibility is permission-gated per formula** | As with the view-scoped listing, users without edit permission on a given formula see `expression: ""` for that entry, even if they can see other metadata fields. |
| **Includes formulas owned by Query Tables** | `tableName` may refer to a Query Table (e.g., `"QT1"`) as well as a regular table, since aggregate formulas can be defined on Query Table views too. |
| **Read-only permission is sufficient** | Unlike the view-scoped Create/Edit/Delete APIs (which require Create Formula permission), this workspace-scoped listing only requires standard Read permission on the workspace. |
| **Dependency** | `tableId` → Get View List / Get Table Metadata (to see the owning table's schema). `formulaId` → Get Aggregate Formula Dependents, Get Aggregate Formula Value. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Read permission on the workspace. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Aggregate Formulas (Unified Metrics) overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Aggregate Formula](get-aggregate-formula-list.md), [Add Aggregate Formula](add-aggregate-formula.md), [Edit Aggregate Formula](edit-aggregate-formula.md), [Delete Aggregate Formula](delete-aggregate-formula.md), [Get Aggregate Formula Dependents](get-aggregate-formula-dependents.md), [Get Aggregate Formula Value](get-aggregate-formula-value.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/aggregate-formulas/get-aggregate-formulas-in-workspace.md).
