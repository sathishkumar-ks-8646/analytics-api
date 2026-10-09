---
type: API Endpoint
title: Edit Custom Formula
description: "Updates the expression of an existing custom formula column, together with its display name and description where needed."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas/{formula-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - formula-columns
  - put
  - modeling
api:
  operation_id: editFormulaColumn
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas/{formula-id}"
  domain: data-modeling-and-schema
  group: formula-columns
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
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
    - 7427
    - 7467
    - 8079
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1customformulas~1{formula-id}/put"
    config_schema: EditFormulaColumnConfig
    response_schema: null
  sdk_examples: "/sdk-examples/data-modeling-and-schema/formula-columns/edit-formula-column.md"
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

**PUT `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas/{formula-id}`** - Edit Custom Formula (Custom Formula Columns / Data Modeling & Schema).

Updates the expression and/or description of an existing custom formula column.

From the OpenAPI specification:

Updates the expression of an existing custom formula column, together with its display name and description where needed.

The new expression replaces the previous one entirely - there is no partial update of individual clauses.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `editFormulaColumn` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas/{formula-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| Rate limit | 20 requests per user per minute (10-minute lockout on breach). See [Rate limits](../../../foundations/rate-limits-and-quotas.md). |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1customformulas~1{formula-id}/put`; CONFIG schema `EditFormulaColumnConfig` |

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
| `{formula-id}` | string | ID of the formula. | [How to obtain](../../../foundations/identifiers.md#formula-id) |

## CONFIG Parameters

| Parameter | Type | Mandatory | Max Length | Description |
|-----------|------|-----------|------------|-------------|
| `expression` | String | **Yes** | 50,000 chars | The new formula expression. Fully replaces the existing expression. |
| `description` | String | No | 250 chars | New description for the formula column. If omitted, the existing description is retained (see Notes below for the current behaviour). |

> **Important — no `formulaName` field:** Unlike Add Custom Formula, this API's CONFIG template does **not** accept a `formulaName` field. The formula column's display name **cannot be renamed** through this API — only the expression and description can be updated.

## Notes from the OpenAPI specification

- This API returns HTTP 204 No Content with no response body on success. There is no status or summary key to parse - treat the HTTP status code as the sole success indicator.
- The display name is carried inside the configuration as formulaName, not as a separate argument, because the SDK method signature is editFormulaColumn(formulaId, expression, config). The published help page states that this API cannot rename a formula column, which contradicts the SDK - confirm the behaviour against a real call before relying on a rename.
- expression is mandatory and fully replaces the previous one. There is no partial update, so the complete expression must be resent even for a minor change.
- Resend description explicitly whenever its value matters. The behaviour of unset optional text fields is not guaranteed to preserve the existing value.
- When the new expression changes the result type, for example from numeric to text, the dependent reports and charts that relied on the previous data type may behave unexpectedly.
- Formula columns are not supported on pipeline tables and such a request returns error 7467.
- This API is throttled at 20 requests per user per minute, with a ten-minute lockout when the limit is breached.
- Obtain the formula-id from the Get Custom Formulas API and confirm the referenced column names through the Get Table Metadata API.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Update the formula expression only**

```http
PUT /restapi/v2/workspaces/20868000000040672/views/20868000000040795/customformulas/320862000000625897 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"expression":"(\"Unit Price\" * \"Quantity\") - \"Discount\""}
```

**Case 2 — Update expression and description together**

```http
PUT /restapi/v2/workspaces/20868000000040672/views/20868000000040795/customformulas/320862000000625897 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"expression":"IF(\"Amount Paid\" >= \"Order Total\", \"Paid\", \"Partially Paid\")","description":"Updated logic to reflect partial payments"}
```

**Case 3 — White label portal user editing a formula**

```http
PUT /restapi/v2/workspaces/20868000000040672/views/20868000000040795/customformulas/320862000000625897 HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"expression":"CONCATENATE(\"First Name\",\" \",\"Middle Name\",\" \",\"Last Name\")"}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Edit Custom Formula](../../../sdk-examples/data-modeling-and-schema/formula-columns/edit-formula-column.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Edit Custom Formula returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Cannot rename via this API** | There is no `formulaName` field in this API's CONFIG. To rename a formula column, use a dedicated column-rename operation if available for the view type, or delete and recreate the formula with the desired name. |
| **`expression` is mandatory and fully replaces the old one** | There is no partial/incremental update — the entire expression must be resupplied even for a minor change. |
| **`description` omission behaviour** | If `description` is not supplied, the internal save logic reuses the column's current display name and does not clear existing metadata; however, always resend `description` explicitly if you want to guarantee its value, since behaviour for unset optional text fields has historically reset to empty in other similar rename/edit APIs in this API suite (see [Workspace Groups](../../users-and-groups/workspace-groups/overview.md) and [Workspace Folders](../../workspace-management/workspace-folders/overview.md) for the equivalent `*Desc` reset pattern in other object types). |
| **Not supported on Pipeline Tables** | Editing a formula column on a Pipeline Table view returns error 7467. |
| **Changing the expression may change the data type** | If the new expression changes the result type (e.g., from numeric to text), any dependent reports/charts relying on the previous data type may behave unexpectedly or show a data type mismatch. |
| **Dependency** | `<formula-id>` → Get Custom Formulas. Column names used in `expression` → Get Table Metadata. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7112](../../../foundations/error-codes.md#error-7112) | 400 | The new formula expression could not be parsed (syntax error). | Review the expression for correct syntax and quoting. |
| [7113](../../../foundations/error-codes.md#error-7113) | 400 | The expression references an unknown/unsupported function. | Verify the function name against the Zoho Analytics formula function reference. |
| [7115](../../../foundations/error-codes.md#error-7115) | 400 | The expression references a column that does not exist, or the formula is otherwise invalid. | Verify all column names referenced in the expression. |
| [7116](../../../foundations/error-codes.md#error-7116) | 400 | The expression references a column that does not exist, or the formula is otherwise invalid. | Verify all column names referenced in the expression. |
| [7160](../../../foundations/error-codes.md#error-7160) | 400 | Formula columns are not allowed for this user/view combination. | Ensure the user is a Workspace Admin or has Create Formula permission on the view. |
| [7180](../../../foundations/error-codes.md#error-7180) | 400 | The updated formula creates a circular dependency. | Remove the circular reference from the expression. |
| [7181](../../../foundations/error-codes.md#error-7181) | 400 | The updated formula creates a circular dependency. | Remove the circular reference from the expression. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Create Formula permission on the view. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. | Confirm `<view-id>` belongs to `<workspace-id>`. |
| [7427](../../../foundations/error-codes.md#error-7427) | 400 | The specified `<formula-id>` is not a valid formula column on this view. | Verify the `<formula-id>` using Get Custom Formulas. |
| [7467](../../../foundations/error-codes.md#error-7467) | 400 | Formula columns are not supported on Pipeline Tables. | This API only applies to standard tables/views. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | The required `expression` attribute is missing from CONFIG. | Ensure `expression` is provided in every Edit Custom Formula request. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Custom Formula Columns overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Custom Formulas](get-custom-formula-list.md), [Add Custom Formula](add-formula-column.md), [Delete Custom Formula](delete-formula-column.md), [Copy Custom Formulas](copy-formulas.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/formula-columns/edit-formula-column.md).
