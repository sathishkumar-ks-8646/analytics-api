---
type: API Endpoint
title: Add Custom Formula
description: Creates a new custom formula column on the specified view.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - formula-columns
  - post
  - modeling
api:
  operation_id: addFormulaColumn
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas"
  domain: data-modeling-and-schema
  group: formula-columns
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
    - 7180
    - 7181
    - 7301
    - 7319
    - 7467
    - 8079
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1customformulas/post"
    config_schema: AddFormulaColumnConfig
    response_schema: AddFormulaColumnResponse
  sdk_examples: "/sdk-examples/data-modeling-and-schema/formula-columns/add-formula-column.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas`** - Add Custom Formula (Custom Formula Columns / Data Modeling & Schema).

Creates a new custom formula column on the specified view. The formula's value is computed for each row using the supplied expression.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `addFormulaColumn` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| Rate limit | 20 requests per user per minute (10-minute lockout on breach). See [Rate limits](../../../foundations/rate-limits-and-quotas.md). |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1customformulas/post`; CONFIG schema `AddFormulaColumnConfig`; response schema `AddFormulaColumnResponse` |

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

| Parameter | Type | Mandatory | Max Length | Description |
|-----------|------|-----------|------------|-------------|
| `formulaName` | String | **Yes** | 100 chars | Display name for the new formula column. Must be unique within the view. |
| `expression` | String | **Yes** | 50,000 chars | The formula expression, using Zoho Analytics formula syntax (e.g., `IF()`, `CONCATENATE()`, arithmetic operators, references to other column names in double quotes). |
| `description` | String | No | 250 chars | Description of the formula column. |

> **Formula expression syntax:** Column references within the expression must use the exact display name of the column, enclosed in double quotes, e.g. `"Unit Price" * "Quantity"`. Refer to the Zoho Analytics formula function reference for the full list of supported functions.

## Notes from the OpenAPI specification

- The expression is validated and parsed at creation time. Column references, function names and syntax are checked before the column is created, so an invalid expression is rejected before any schema change occurs.
- Column references inside the expression must use the exact display name of the column, enclosed in double quotes, such as "Unit Price" * "Quantity". A misspelled or missing column name returns an unknown-column error.
- formulaName must be unique within the view. A duplicate formula or column name is rejected.
- The data type of the resulting column is derived automatically from the expression - an arithmetic expression over numeric columns yields a numeric formula column, for instance - and cannot be set explicitly.
- Formula columns are not supported on pipeline tables and such a request returns error 7467.
- This API is throttled at 20 requests per user per minute, with a ten-minute lockout when the limit is breached.
- Confirm the exact display names of the referenced columns through the Get Table Metadata API before calling. The returned formulaId can afterwards be passed to the Get Column Dependents API to trace where the formula is used.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `formulaId` | String | Unique column ID assigned to the newly created formula column. Use this as `<formula-id>` for subsequent Edit or Delete calls. |
| `formulaName` | String | The display name of the formula column, echoing the `formulaName` value from the request. |

# Examples

## Sample Requests

**Case 1 — Simple arithmetic formula**

```http
POST /restapi/v2/workspaces/20868000000040672/views/20868000000040795/customformulas HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"formulaName":"Total Amount","expression":"\"Unit Price\" * \"Quantity\""}
```

**Case 2 — Conditional (IF) formula with a description**

```http
POST /restapi/v2/workspaces/20868000000040672/views/20868000000040795/customformulas HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"formulaName":"Order Status","expression":"IF(\"Amount Paid\" >= \"Order Total\", \"Paid\", \"Pending\")","description":"Flags each order as Paid or Pending based on payment amount"}
```

**Case 3 — White label portal user adding a text concatenation formula**

```http
POST /restapi/v2/workspaces/20868000000040672/views/20868000000040795/customformulas HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"formulaName":"Full Name","expression":"CONCATENATE(\"First Name\",\" \",\"Last Name\")"}
```

## Sample Responses

**HTTP 200 OK**

```json
{
  "status": "success",
  "summary": "Custom formula has been added successfully.",
  "data": {
    "formulaId": "320862000000625897",
    "formulaName": "Total Amount"
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Add Custom Formula](../../../sdk-examples/data-modeling-and-schema/formula-columns/add-formula-column.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Expression is validated and parsed at creation time** | Column references, function names, and syntax are checked before the formula column is created. Invalid expressions are rejected with a parse or validation error before any schema change occurs. |
| **`formulaName` must be unique** | Duplicate formula/column names within the same view are rejected. |
| **Column references use exact display names in double quotes** | If a referenced column name is misspelled or does not exist in the view, an "unknown column" error is returned. |
| **Not supported on Pipeline Tables** | Attempting to add a formula column to a Pipeline Table view returns error 7467. |
| **Data type of the formula column is inferred** | The resulting column's data type is derived automatically from the expression (e.g., an arithmetic expression on numeric columns yields a numeric formula column). It cannot be explicitly set. |
| **Dependency** | `<view-id>` → Get View List. Column names used in `expression` → Get Table Metadata (to confirm exact display names). After creation, the returned `formulaId` can be used with Get Column Dependents (see [Columns](../columns/overview.md)) to trace where the formula is later used. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7112](../../../foundations/error-codes.md#error-7112) | 400 | The formula expression could not be parsed (syntax error). | Review the expression for unbalanced parentheses, missing operators, or incorrect quoting of column names. |
| [7113](../../../foundations/error-codes.md#error-7113) | 400 | The expression references an unknown/unsupported function. | Verify the function name against the Zoho Analytics formula function reference. |
| [7115](../../../foundations/error-codes.md#error-7115) | 400 | The expression references a column that does not exist in the view, or the formula is otherwise invalid. | Verify all column names referenced in the expression exist and are spelled exactly as shown in Get Table Metadata. |
| [7116](../../../foundations/error-codes.md#error-7116) | 400 | The expression references a column that does not exist in the view, or the formula is otherwise invalid. | Verify all column names referenced in the expression exist and are spelled exactly as shown in Get Table Metadata. |
| [7160](../../../foundations/error-codes.md#error-7160) | 400 | Formula columns are not allowed for this user/view combination. | Ensure the user is a Workspace Admin or has Create Formula permission on the view. |
| [7180](../../../foundations/error-codes.md#error-7180) | 400 | The formula creates a circular dependency (it references a formula that, directly or indirectly, references this one). | Remove the circular reference from the expression. |
| [7181](../../../foundations/error-codes.md#error-7181) | 400 | The formula creates a circular dependency (it references a formula that, directly or indirectly, references this one). | Remove the circular reference from the expression. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Create Formula permission on the view. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. | Confirm `<view-id>` belongs to `<workspace-id>`. |
| [7467](../../../foundations/error-codes.md#error-7467) | 400 | Formula columns are not supported on Pipeline Tables. | Formula columns can only be added to regular tables and standard views. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | A required attribute (`expression` or `formulaName`) is missing from CONFIG. | Ensure both `formulaName` and `expression` are provided. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Custom Formula Columns overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Custom Formulas](get-custom-formula-list.md), [Edit Custom Formula](edit-formula-column.md), [Delete Custom Formula](delete-formula-column.md), [Copy Custom Formulas](copy-formulas.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/formula-columns/add-formula-column.md).
