---
type: API Endpoint
title: Edit Aggregate Formula
description: Updates an existing aggregate formula.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas/{formula-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - aggregate-formulas
  - put
  - modeling
api:
  operation_id: editAggregateFormula
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas/{formula-id}"
  domain: data-modeling-and-schema
  group: aggregate-formulas
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
    - 7301
    - 7319
    - 7428
    - 8079
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1aggregateformulas~1{formula-id}/put"
    config_schema: EditAggregateFormulaConfig
    response_schema: null
  sdk_examples: "/sdk-examples/data-modeling-and-schema/aggregate-formulas/edit-aggregate-formula.md"
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

**PUT `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas/{formula-id}`** - Edit Aggregate Formula (Aggregate Formulas (Unified Metrics) / Data Modeling & Schema).

Updates an existing aggregate formula. Unlike [Edit Custom Formula](../formula-columns/edit-formula-column.md), this API **does support renaming** the formula.

From the OpenAPI specification:

Updates an existing aggregate formula. Unlike the Edit Custom Formula API, this one supports renaming.

At least one of `formulaName` or `expression` must be sent. When `formulaName` is sent on its own, the current expression is fetched and reapplied unchanged, which performs a pure rename.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `editAggregateFormula` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas/{formula-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Create Formula permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| Rate limit | 20 requests per user per minute (10-minute lockout on breach). See [Rate limits](../../../foundations/rate-limits-and-quotas.md). |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1aggregateformulas~1{formula-id}/put`; CONFIG schema `EditAggregateFormulaConfig` |

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
| `formulaName` | String | No\* | 100 chars | New display name for the aggregate formula. |
| `expression` | String | No\* | 50,000 chars | New aggregate expression. Fully replaces the existing expression. |
| `description` | String | No | 250 chars | New description. |
| `synonyms` | JSONArray of String | No | — | New list of synonyms. Fully replaces the existing list. |
| `columnPriority` | Integer (enum) | No | — | New priority ranking (`0`=Low, `1`=Medium, `2`=High). |

> \* **At least one of `expression` or `formulaName` must be provided.** Submitting neither returns error 8079.

> **Rename-only mode:** If you supply `formulaName` **without** `expression`, the API automatically fetches the formula's current expression internally and reapplies it unchanged — effectively performing a pure rename without requiring you to resend the expression text. This is the opposite behaviour from Edit Custom Formula, which has no `formulaName` field at all.

## Notes from the OpenAPI specification

- This API returns HTTP 204 No Content with no response body on success. There is no status or summary key to parse - treat the HTTP status code as the sole success indicator.
- At least one of formulaName or expression must be sent. A configuration carrying only description, synonyms or columnPriority is rejected with error 8079.
- Sending formulaName without expression performs a pure rename, because the existing expression is preserved automatically. This is the opposite of the Edit Custom Formula API, which has no formulaName attribute at all.
- expression, when sent, fully replaces the previous one. There is no partial update of the formula logic.
- synonyms, when sent, fully replaces the existing list rather than adding to it. Fetch the current list through the Get Unified Metrics in Workspace API and resend the merged array to add a synonym.
- A rename does not change formulaId, so every dependent report and dashboard continues to refer to the metric correctly.
- This API is throttled at 20 requests per user per minute, with a ten-minute lockout when the limit is breached.
- Obtain the formula-id from the view-scoped Get Aggregate Formula API or from the Get Unified Metrics in Workspace API.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Rename only (no expression change)**

```http
PUT /restapi/v2/workspaces/137687000271334001/views/137687000271334499/aggregateformulas/137687000271334553 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"formulaName":"Total Revenue"}
```

**Case 2 — Update the expression only**

```http
PUT /restapi/v2/workspaces/137687000271334001/views/137687000271334499/aggregateformulas/137687000271334553 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"expression":"sum(\"Table_1\".\"Sales\") - sum(\"Table_1\".\"Returns\")"}
```

**Case 3 — Update expression, description, synonyms, and priority together**

```http
PUT /restapi/v2/workspaces/137687000271334001/views/137687000271334499/aggregateformulas/137687000271334553 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"expression":"sum(\"Table_1\".\"Net Sales\")","description":"Total net sales after returns and discounts","synonyms":["net revenue","net sales total"],"columnPriority":2}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Edit Aggregate Formula](../../../sdk-examples/data-modeling-and-schema/aggregate-formulas/edit-aggregate-formula.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Edit Aggregate Formula returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Supports pure rename** | Unlike Edit Custom Formula, providing only `formulaName` (no `expression`) is valid — the existing expression is preserved automatically. |
| **`expression`, when supplied, fully replaces the old one** | There is no partial/incremental update of the formula logic. |
| **`synonyms`, when supplied, fully replaces the existing list** | To add a synonym without losing existing ones, first fetch the current list (via Get Unified Metrics in Workspace) and resend the full merged array. |
| **At least one of `formulaName` or `expression` is required** | Submitting a CONFIG with only `description`, `synonyms`, or `columnPriority` (and no `formulaName`/`expression`) returns error 8079. |
| **Renaming does not change `formulaId`** | The formula's identity is preserved across renames — all dependent reports/dashboards continue to reference it via `formulaId`. |
| **Dependency** | `<formula-id>` → Get Aggregate Formula (view-scoped) or Get Unified Metrics in Workspace. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7112](../../../foundations/error-codes.md#error-7112) | 400 | The new expression could not be parsed (syntax error). | Review the expression for correct syntax. |
| [7113](../../../foundations/error-codes.md#error-7113) | 400 | The expression references an unknown/unsupported function. | Verify the aggregate function name. |
| [7115](../../../foundations/error-codes.md#error-7115) | 400 | The expression references a column that does not exist, or the formula is otherwise invalid. | Verify all table/column names referenced. |
| [7116](../../../foundations/error-codes.md#error-7116) | 400 | The expression references a column that does not exist, or the formula is otherwise invalid. | Verify all table/column names referenced. |
| [7160](../../../foundations/error-codes.md#error-7160) | 400 | Formula operations are not allowed for this user/view combination. | Ensure the user is a Workspace Admin or has Create Formula permission on the view. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Create Formula permission on the view. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. | Confirm `<view-id>` belongs to `<workspace-id>`. |
| [7428](../../../foundations/error-codes.md#error-7428) | 400 | The specified `<formula-id>` is not a valid aggregate formula on this view. | Verify `<formula-id>` using Get Aggregate Formula. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | Neither `formulaName` nor `expression` was provided. | Supply at least one of these two fields. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Aggregate Formulas (Unified Metrics) overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Aggregate Formula](get-aggregate-formula-list.md), [Add Aggregate Formula](add-aggregate-formula.md), [Delete Aggregate Formula](delete-aggregate-formula.md), [Get Unified Metrics in Workspace](get-aggregate-formulas-in-workspace.md), [Get Aggregate Formula Dependents](get-aggregate-formula-dependents.md), [Get Aggregate Formula Value](get-aggregate-formula-value.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/aggregate-formulas/edit-aggregate-formula.md).
