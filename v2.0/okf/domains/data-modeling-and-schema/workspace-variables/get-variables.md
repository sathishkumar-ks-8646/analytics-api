---
type: API Endpoint
title: Get Variables
description: Returns a summary list of all variables defined in the workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/variables"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - workspace-variables
  - get
  - modeling
api:
  operation_id: getVariables
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/variables"
  domain: data-modeling-and-schema
  group: workspace-variables
  oauth_scopes:
    - ZohoAnalytics.modeling.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace."
  error_codes:
    - 7301
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1variables/get"
    config_schema: null
    response_schema: GetVariablesResponse
  sdk_examples: "/sdk-examples/data-modeling-and-schema/workspace-variables/get-variables.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/variables`** - Get Variables (Workspace Variables / Data Modeling & Schema).

Returns a summary list of all variables defined in the workspace.

> This API has no CONFIG parameter.

From the OpenAPI specification:

Returns a summary list of all variables defined in the workspace.

The values, the range and the display format of a variable are not included here - use the Get Variable Details API for the full definition of a specific variable.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getVariables` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/variables` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1variables/get`; response schema `GetVariablesResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.read`. See [Authentication](../../../foundations/authentication.md). |
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
| `variables` | Array | List of variables defined in the workspace. Empty array if none exist. |
| `variables[].variableName` | String | Display name of the variable. |
| `variables[].variableId` | String | Unique ID of the variable. Use as `<variable-id>` for Edit/Delete Variable and Get Variable Details. |
| `variables[].variableType` | String (numeric enum) | `"0"` = List, `"1"` = Range, `"3"` = All Values. **Returned as a string here**, unlike Get Variable Details where it is returned as a native integer — account for this type difference when parsing. |
| `variables[].variableDataType` | String (numeric enum) | `"1"` = Text, `"4"` = Number, `"5"` = Positive Number, `"6"` = Decimal Number, `"7"` = Currency, `"8"` = Percentage. Also returned as a string here. |

## Notes from the OpenAPI specification

- This is a summary listing. defaultData, userSpecificData and format are not returned - call the Get Variable Details API for the full definition of a variable.
- variableType and variableDataType are returned as quoted strings by this API but as native integers by the Get Variable Details API. Take care when comparing or switching on these attributes across the two read APIs.
- Obtain the workspace-id from the Get Workspace List API. The variableId values feed into the Edit Variable, Delete Variable and Get Variable Details APIs.

# Examples

## Sample Requests

**Case 1 — Get all variables in the workspace**

```http
GET /restapi/v2/workspaces/137687000271334001/variables HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White label portal admin fetching the variable list**

```http
GET /restapi/v2/workspaces/137687000271334001/variables HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — Multiple variables of different types**

```json
{
  "status": "success",
  "summary": "Get variables",
  "data": {
    "variables": [
      {
        "variableName": "Region",
        "variableId": "137687000007146340",
        "variableType": "0",
        "variableDataType": "1"
      },
      {
        "variableName": "All Regions",
        "variableId": "137687000007146338",
        "variableType": "3",
        "variableDataType": "1"
      },
      {
        "variableName": "Target Sales",
        "variableId": "137687000007146342",
        "variableType": "1",
        "variableDataType": "4"
      },
      {
        "variableName": "Discount Percent",
        "variableId": "137687000007146352",
        "variableType": "0",
        "variableDataType": "8"
      }
    ]
  }
}
```

**HTTP 200 OK — Workspace with no variables**

```json
{
  "status": "success",
  "summary": "Get variables",
  "data": {
    "variables": []
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Variables](../../../sdk-examples/data-modeling-and-schema/workspace-variables/get-variables.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Summary only — no values** | This API does not return `defaultData`, `userSpecificData`, or `format` — use Get Variable Details for the full definition of a specific variable. |
| **`variableType`/`variableDataType` are strings here, integers in Get Variable Details** | Be careful when comparing or switching on these fields across the two "read" APIs in this suite — the JSON type differs. |
| **Dependency** | `<workspace-id>` → Get Workspace List. `variableId` values feed into Edit/Delete Variable and Get Variable Details. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is an Account Admin, Organization Admin, or Workspace Admin. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Workspace Variables overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Variable](create-variable.md), [Edit Variable](update-variable.md), [Delete Variable](delete-variable.md), [Get Variable Details](get-variable-details.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/workspace-variables/get-variables.md).
