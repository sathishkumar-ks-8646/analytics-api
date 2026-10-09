---
type: API Endpoint
title: Get Variable Details
description: "Returns the full definition of a specific variable, including its values/range, all per-user overrides, and display format."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - workspace-variables
  - get
  - modeling
api:
  operation_id: getVariableDetails
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}"
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
    - 70320
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1variables~1{variable-id}/get"
    config_schema: null
    response_schema: GetVariableDetailsResponse
  sdk_examples: "/sdk-examples/data-modeling-and-schema/workspace-variables/get-variable-details.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}`** - Get Variable Details (Workspace Variables / Data Modeling & Schema).

Returns the full definition of a specific variable, including its values/range, all per-user overrides, and display format.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getVariableDetails` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1variables~1{variable-id}/get`; response schema `GetVariableDetailsResponse` |

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
| `{variable-id}` | string | ID of the variable. | [How to obtain](../../../foundations/identifiers.md#variable-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `variableName` | String | Display name of the variable. |
| `variableType` | Integer | `0` = List, `1` = Range, `3` = All Values. **Returned as a native integer here**, unlike Get Variables which returns it as a string. |
| `variableDataType` | Integer | `1` = Text, `4` = Number, `5` = Positive Number, `6` = Decimal Number, `7` = Currency, `8` = Percentage. Also a native integer. |
| `userSpecificData` | Array | Per-user override entries. Empty array if no per-user overrides are configured. |
| `userSpecificData[].values` | Array of String | **List type only.** The set of allowed values for the user(s) in this entry. |
| `userSpecificData[].minValue` / `maxValue` / `stepSize` | String | **Range type only.** The numeric bounds and increment for the user(s) in this entry. |
| `userSpecificData[].defaultValue` | String | The default value/range-point applied for the user(s) in this entry. Omitted for **All Values**-type variables, since no default value concept applies. |
| `userSpecificData[].emailIds` | Array of String | Email addresses this override entry applies to. |
| `defaultData` | JSONObject | The workspace-wide fallback definition applied to any user not covered by a `userSpecificData` entry. **Omitted entirely for All Values-type variables** (see the fourth sample above), since there is no fallback value concept for that type. |
| `defaultData.values` / `defaultValue` | Array of String / String | **List type.** Allowed values and the fallback default. |
| `defaultData.minValue` / `maxValue` / `stepSize` / `defaultValue` | String | **Range type.** Numeric bounds, increment, and fallback default. |
| `format` | JSONObject | Display formatting settings. Always present, though its inner keys vary by `variableDataType` (e.g., `currencySymbol`/`showNegativeSign` only appear for Currency; `showPercent` only for Percentage). |

## Notes from the OpenAPI specification

- variableType and variableDataType are returned as native integers by this API but as quoted strings by the Get Variables API. Take care when comparing or switching on these attributes across the two read APIs.
- defaultData may be absent entirely. An All Values variable carries no such key, so check for its presence before reading its sub-attributes.
- The contents of format depend on variableDataType. Read currencySymbol and showNegativeSign only for a Currency variable and showPercent only for a Percentage variable, because those keys are omitted for the other data types.
- The entries of values, along with minValue, maxValue, stepSize and defaultValue, are always strings even for the numeric data types, so that precision is preserved. Parse them into numbers when further calculation is needed.
- Branch the parsing on variableType first and then on variableDataType, because the shape of defaultData, of the userSpecificData entries and of format all depend on those two attributes.
- Obtain the variable-id from the Get Variables API.

# Examples

## Sample Requests

**Case 1 — Get details of a List-type variable with per-user overrides**

```http
GET /restapi/v2/workspaces/137687000271334001/variables/137687000007146340 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Get details of a Range-type variable**

```http
GET /restapi/v2/workspaces/137687000271334001/variables/137687000007146342 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — Get details of a Currency-formatted variable**

```http
GET /restapi/v2/workspaces/137687000271334001/variables/137687000007146350 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — List-type variable with two per-user overrides**

```json
{
  "status": "success",
  "summary": "Get variable details",
  "data": {
    "variableName": "Region",
    "variableType": 0,
    "variableDataType": 1,
    "userSpecificData": [
      {
        "values": ["4", "5", "6"],
        "defaultValue": "4",
        "emailIds": ["sales.east@zylker.com"]
      },
      {
        "values": ["7", "8", "9"],
        "defaultValue": "7",
        "emailIds": ["sales.west@zylker.com"]
      }
    ],
    "defaultData": {
      "values": ["1", "2", "3"],
      "defaultValue": "1"
    },
    "format": {
      "alignment": "Left"
    }
  }
}
```

**HTTP 200 OK — Range-type Number variable, no per-user overrides**

```json
{
  "status": "success",
  "summary": "Get variable details",
  "data": {
    "variableName": "Target Sales",
    "variableType": 1,
    "variableDataType": 4,
    "userSpecificData": [],
    "defaultData": {
      "minValue": "1",
      "maxValue": "3",
      "stepSize": "1",
      "defaultValue": "2"
    },
    "format": {
      "alignment": "Right",
      "units": "None",
      "decimalPlaces": -1,
      "userLocale": false,
      "thousandSeparator": 0,
      "decimalSeparator": 0
    }
  }
}
```

**HTTP 200 OK — Currency-formatted variable**

```json
{
  "status": "success",
  "summary": "Get variable details",
  "data": {
    "variableName": "Unit Cost",
    "variableType": 0,
    "variableDataType": 7,
    "userSpecificData": [],
    "defaultData": {
      "values": ["1", "2", "3"],
      "defaultValue": "1"
    },
    "format": {
      "alignment": "Right",
      "currencySymbol": "en;US;",
      "showNegativeSign": true,
      "units": "None",
      "decimalPlaces": 2,
      "userLocale": false,
      "thousandSeparator": 1,
      "decimalSeparator": 0
    }
  }
}
```

**HTTP 200 OK — All Values-type variable**

```json
{
  "status": "success",
  "summary": "Get variable details",
  "data": {
    "variableName": "All Regions",
    "variableType": 3,
    "variableDataType": 1,
    "userSpecificData": [
      {
        "values": ["1", "2", "3"],
        "emailIds": ["sales.orgadmin@zylker.com"]
      }
    ],
    "format": {
      "alignment": "Left"
    }
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Variable Details](../../../sdk-examples/data-modeling-and-schema/workspace-variables/get-variable-details.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`variableType`/`variableDataType` are integers here, strings in Get Variables** | The reverse of the type note in Get Variables — this API returns native JSON integers for both fields. |
| **`defaultData` may be entirely absent** | For All Values-type variables, the response has no `defaultData` key at all — check for its presence before accessing its sub-fields. |
| **`format` contents depend on `variableDataType`** | Only inspect `currencySymbol`/`showNegativeSign` when `variableDataType` is `7` (Currency), and only inspect `showPercent` when it is `8` (Percentage) — these keys are omitted for other data types. |
| **Values inside `values`/`minValue`/`maxValue`/`stepSize`/`defaultValue` are always strings** | Even for numeric data types (Number, Currency, etc.), these fields are serialized as strings to preserve precision — parse them into numbers in your application if further calculation is required. |
| **Dependency** | `<variable-id>` → Get Variables. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is an Account Admin, Organization Admin, or Workspace Admin. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |
| [70320](../../../foundations/error-codes.md#error-70320) | 400 | `USERVARIABLE_VARIABLE_NOT_FOUND` — `<variable-id>` does not exist in this workspace. | Verify `<variable-id>` using Get Variables. |

# Related

- [Workspace Variables overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Variable](create-variable.md), [Edit Variable](update-variable.md), [Delete Variable](delete-variable.md), [Get Variables](get-variables.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/workspace-variables/get-variable-details.md).
