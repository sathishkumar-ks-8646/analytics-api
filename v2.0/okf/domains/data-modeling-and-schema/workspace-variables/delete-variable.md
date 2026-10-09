---
type: API Endpoint
title: Delete Variable
description: Permanently deletes a workspace variable.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - workspace-variables
  - delete
  - modeling
api:
  operation_id: deleteVariable
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}"
  domain: data-modeling-and-schema
  group: workspace-variables
  oauth_scopes:
    - ZohoAnalytics.modeling.delete
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace."
  error_codes:
    - 7301
    - 70321
    - 70322
    - 70326
    - 70329
    - 70357
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1variables~1{variable-id}/delete"
    config_schema: null
    response_schema: null
  sdk_examples: "/sdk-examples/data-modeling-and-schema/workspace-variables/delete-variable.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}`** - Delete Variable (Workspace Variables / Data Modeling & Schema).

Permanently deletes a workspace variable.

> This API has no CONFIG parameter.

From the OpenAPI specification:

Permanently deletes a workspace variable.

The deletion is blocked when the variable is still referred to by a formula, a report filter or a SQL query. There is no cascade option, so the dependent references must be removed first.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deleteVariable` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingdelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 204 with no body |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1variables~1{variable-id}/delete` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.delete`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{variable-id}` | string | ID of the variable. | [How to obtain](../../../foundations/identifiers.md#variable-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- This API returns HTTP 204 No Content with no response body on success. There is no status or summary key to parse - treat the HTTP status code as the sole success indicator.
- This API is not idempotent. A variable ID that does not exist, or that was already deleted, returns an error rather than a silent success.
- The deletion is blocked whenever the variable is used in a formula, a report filter or a SQL query of the workspace, so that those dependents are not broken.
- There is no cascade option here, unlike the Delete Column and Delete Aggregate Formula APIs. The dependent references must always be removed manually first.
- There is no dedicated dependents API for variables. Review the formula expressions, through the Get Custom Formulas and Get Aggregate Formula APIs, along with the report and query definitions, looking for ${variableName} references before deleting.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Delete an unused variable**

```http
DELETE /restapi/v2/workspaces/137687000271334001/variables/137687000006991651 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Attempt to delete a variable still referenced by a formula (fails)**

```http
DELETE /restapi/v2/workspaces/137687000271334001/variables/137687000006991655 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Delete Variable](../../../sdk-examples/data-modeling-and-schema/workspace-variables/delete-variable.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Delete Variable returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Not idempotent** | Deleting a `<variable-id>` that does not exist (or was already deleted) returns an error, not a silent success. |
| **Blocked if referenced elsewhere** | If the variable is used in any formula, report filter, or SQL query in the workspace, deletion is blocked to avoid breaking those dependents. |
| **No cascade-delete option** | Unlike Delete Column/Delete Aggregate Formula, this API has no `deleteDependentViews`-style flag — dependent references must be manually removed before the variable can be deleted. |
| **Dependency** | `<variable-id>` → Get Variables or Get Variable Details. There is no dedicated "Get Variable Dependents" API in this suite — use Get Table Metadata / formula expressions review to locate references before deleting. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is an Account Admin, Organization Admin, or Workspace Admin. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |
| [70321](../../../foundations/error-codes.md#error-70321) | 400 | `USERVARIABLE_VARIABLE_IN_USE` — The variable is currently referenced elsewhere and cannot be deleted. | Remove all references to this variable (in formulas, filters, SQL queries) before deleting. |
| [70322](../../../foundations/error-codes.md#error-70322) | 400 | `USERVARIABLE_VARIABLE_IN_USE` (multi-variable form) — One or more of the requested variables are in use. | Same as above; applies when multiple variables are targeted in a single internal delete operation. |
| [70326](../../../foundations/error-codes.md#error-70326) | 400 | `CANT_DELETE_VARIABLE` — The variable cannot be deleted by this user (ownership restriction). | Ensure the user is an Account Admin, Organization Admin, or Workspace Admin. |
| [70329](../../../foundations/error-codes.md#error-70329) | 400 | `CANT_DELETE_VARIABLE` (`UNAUTHORIZED_VAR_ACTION`) — `<variable-id>` does not exist in this workspace. | Verify `<variable-id>` using Get Variables. |
| [70357](../../../foundations/error-codes.md#error-70357) | 400 | `USERVARIABLE_VARIABLE_CANNOT_BE_DELETED` — Deletion blocked due to unresolved references. | Identify and remove dependent formulas/reports, then retry. |

# Related

- [Workspace Variables overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Variable](create-variable.md), [Edit Variable](update-variable.md), [Get Variables](get-variables.md), [Get Variable Details](get-variable-details.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/workspace-variables/delete-variable.md).
