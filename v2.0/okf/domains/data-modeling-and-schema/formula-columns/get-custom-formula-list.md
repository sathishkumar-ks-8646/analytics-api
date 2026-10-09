---
type: API Endpoint
title: Get Custom Formulas
description: Returns the custom formula columns defined on the specified view.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - formula-columns
  - get
  - metadata
api:
  operation_id: getCustomFormulaList
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas"
  domain: data-modeling-and-schema
  group: formula-columns
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
    - 7160
    - 7301
    - 7319
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1customformulas/get"
    config_schema: null
    response_schema: GetCustomFormulaListResponse
  sdk_examples: "/sdk-examples/data-modeling-and-schema/formula-columns/get-custom-formula-list.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas`** - Get Custom Formulas (Custom Formula Columns / Data Modeling & Schema).

Returns the list of custom formula columns defined on the specified view.

> This API has no CONFIG parameter.

From the OpenAPI specification:

Returns the custom formula columns defined on the specified view. A custom formula column is a computed column whose value is derived, for each row, from an expression referring to other columns of the same view.

The identifiers returned here are the entry point for the Edit Custom Formula and Delete Custom Formula APIs.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getCustomFormulaList` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| Rate limit | 30 requests per user per minute (10-minute lockout on breach). See [Rate limits](../../../foundations/rate-limits-and-quotas.md). |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1customformulas/get`; response schema `GetCustomFormulaListResponse` |

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
| `customFormulas` | Array | List of custom formula columns defined on this view. Empty array if none exist. |
| `customFormulas[].formulaId` | String | Unique column ID of the formula column. Use this as `<formula-id>` for Edit Custom Formula and Delete Custom Formula. |
| `customFormulas[].formulaName` | String | Display name of the formula column, as shown in the Zoho Analytics UI. |

## Notes from the OpenAPI specification

- Only formula-type columns are listed. The regular, non-computed columns of the view are not included, even though they are visible through the Get Table Metadata API.
- The expression of a formula is not returned by this API and there is no dedicated endpoint that exposes it, so keep your own record of the expression text if you need to review it before an edit.
- Workspace-level aggregate formulas are a distinct concept and are not listed here. Use the Get Aggregate Formula API for those.
- The URL path accepts both customformulas and formulacolumns as equivalent segments. Use customformulas for new integrations, because the response key is always customFormulas.
- This API is throttled at 30 requests per user per minute, with a ten-minute lockout when the limit is breached.
- Obtain the view-id from the Get View List API. The formulaId values feed directly into the Edit Custom Formula and Delete Custom Formula APIs.

# Examples

## Sample Requests

**Case 1 — Get all custom formulas on a view**

```http
GET /restapi/v2/workspaces/20868000000040672/views/20868000000040795/customformulas HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White label portal user fetching custom formulas**

```http
GET /restapi/v2/workspaces/20868000000040672/views/20868000000040795/customformulas HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — View with one formula column**

```json
{
  "status": "success",
  "summary": "Get formula columns",
  "data": {
    "customFormulas": [
      {
        "formulaId": "320862000000625897",
        "formulaName": "Length"
      }
    ]
  }
}
```

**HTTP 200 OK — View with no formula columns**

```json
{
  "status": "success",
  "summary": "Get formula columns",
  "data": {
    "customFormulas": []
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Custom Formulas](../../../sdk-examples/data-modeling-and-schema/formula-columns/get-custom-formula-list.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Only formula-type columns are listed** | Regular (non-computed) columns of the view are not included in this response, even though they may be visible in Get Table Metadata. |
| **Response does not include the expression text** | The formula's underlying expression is not returned by this API. There is no dedicated "get formula details" endpoint in this API set — the expression must be tracked externally if you need to re-read it (Edit Custom Formula requires resending the full expression). |
| **Aggregate formulas are excluded** | This endpoint returns only per-row (custom) formula columns. Workspace-level aggregate/metric formulas are a distinct concept and are not listed here. |
| **Dependency** | `<view-id>` → Get View List. `formulaId` values feed directly into Edit Custom Formula and Delete Custom Formula. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7160](../../../foundations/error-codes.md#error-7160) | 400 | The authenticated user is not permitted to view/manage formula columns on this view. | Ensure the user is a Workspace Admin or has Create Formula permission on the view. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Create Formula permission on the view. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. | Confirm `<view-id>` belongs to `<workspace-id>`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Custom Formula Columns overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Add Custom Formula](add-formula-column.md), [Edit Custom Formula](edit-formula-column.md), [Delete Custom Formula](delete-formula-column.md), [Copy Custom Formulas](copy-formulas.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/formula-columns/get-custom-formula-list.md).
