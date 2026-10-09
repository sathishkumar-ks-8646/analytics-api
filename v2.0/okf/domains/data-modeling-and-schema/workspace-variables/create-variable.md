---
type: API Endpoint
title: Create Variable
description: Creates a new workspace variable.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/variables"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - workspace-variables
  - post
  - modeling
api:
  operation_id: createVariable
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/variables"
  domain: data-modeling-and-schema
  group: workspace-variables
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
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace."
  error_codes:
    - 7301
    - 70323
    - 70324
    - 70325
    - 70335
    - 70336
    - 70337
    - 70338
    - 70339
    - 70340
    - 70341
    - 70342
    - 70343
    - 70348
    - 70350
    - 70351
    - 70352
    - 70353
    - 70354
    - 70355
    - 70356
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1variables/post"
    config_schema: VariableConfig
    response_schema: CreateVariableResponse
  sdk_examples: "/sdk-examples/data-modeling-and-schema/workspace-variables/create-variable.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/variables`** - Create Variable (Workspace Variables / Data Modeling & Schema).

Creates a new workspace variable.

From the OpenAPI specification:

Creates a new workspace variable.

The variable is defined once with a name, a data type and a type that determines how its value is resolved, and can carry per-user overrides that fall back to a workspace-wide default.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createVariable` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/variables` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1variables/post`; CONFIG schema `VariableConfig`; response schema `CreateVariableResponse` |

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

## CONFIG Parameters

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `variableName` | String | **Yes** | — | Display name of the variable. Must be unique within the workspace (case-insensitive). Cannot start with `system.` or `${`, and cannot end with `}` (these are reserved patterns used internally for system variables). |
| `variableDataType` | Long (enum) | **Yes** | — | The data type that variable values must conform to. See [Variable Data Type Values](#variable-data-type-values) below. |
| `variableType` | Long (enum) | **Yes** | — | Determines how the variable resolves a value: List, Range, or All Values. See [Variable Type Values](#variable-type-values) below. |
| `defaultData` | JSONObject | Conditionally required | — | Workspace-wide fallback values/default used for any user not explicitly listed in `userSpecificData`. **Required for `variableType` = List (`0`) or Range (`1`)**. Not applicable (and ignored) for `variableType` = All Values (`3`). See [defaultData / userSpecificData Fields](#defaultdata--userspecificdata-fields) below. |
| `userSpecificData` | JSONArray | No | `[]` | Array of per-user (or per-portal-domain) override entries. Each entry maps one or more `emailIds` to their own set of values/range/default. See [defaultData / userSpecificData Fields](#defaultdata--userspecificdata-fields) below. |
| `format` | JSONObject | No | `{}` | Display formatting for the variable's value (alignment, decimal places, currency symbol, date format, etc.). See [format Fields](#format-fields) below. |

### Variable Type Values

| `variableType` | Meaning | Requires `defaultData`? | Requires `userSpecificData` fallback entry? |
|--------------------|---------|--------------------------|-----------------------------------------------|
| `0` | **List** — value chosen from a fixed set of allowed `values`, with one `defaultValue`. | Yes | Optional |
| `1` | **Range** — value chosen from a numeric range (`minValue`/`maxValue`/`stepSize`), with one `defaultValue`. | Yes | Optional |
| `3` | **All Values** — represents every possible value; no explicit list/range/default is defined. | No (ignored if supplied) | Not applicable |

> `variableType = 2` ("Any Value") is a reserved/legacy internal type and is **not accepted** through this API (error 70350 `VARIABLE_INVALID_VARTYPE`).

### Variable Data Type Values

| `variableDataType` | Meaning | Range (`variableType=1`) Allowed? |
|--------------------------|---------|---------------------------------------|
| `1` | Text (Plain) | **No** — Range is not supported for Text (error 70335 `VARIABLE_RANGE_NOT_ALLOWED_ON_DT`). |
| `4` | Number | Yes |
| `5` | Positive Number | Yes |
| `6` | Decimal Number | Yes |
| `7` | Currency | Yes |
| `8` | Percentage | Yes |

> Any other `variableDataType` value (e.g., Date, Boolean) returns error 70351 `VARIABLE_INVALID_DATATYPE` — variables only support the six data types listed above.

### `defaultData` / `userSpecificData` Fields

Both `defaultData` (a single JSONObject) and each entry of `userSpecificData` (a JSONArray of JSONObjects) share the same field structure, which varies by `variableType`:

**When `variableType` = List (`0`):**

| Field | Type | Mandatory | Description |
|-------|------|-----------|--------------|
| `values` | JSONArray of String | **Yes** | The list of allowed values for this entry. |
| `defaultValue` | String | **Yes** in `defaultData`; optional in `userSpecificData` entries | The value used when the variable is resolved without further user input. Must be one of the values in `values` (error 70337 `VARIABLE_DEFAULT_VALUE_NOT_PRESENT_IN_LIST` if not). |

**When `variableType` = Range (`1`):**

| Field | Type | Mandatory | Description |
|-------|------|-----------|--------------|
| `minValue` | String (numeric) | **Yes** | Lower bound of the range. |
| `maxValue` | String (numeric) | **Yes** | Upper bound of the range. Must be greater than `minValue` (error 70352 `VARIABLE_RANGE_MIN_LESS_THAN_MAX`). |
| `stepSize` | String (numeric) | **Yes** | Increment step between selectable values. Must be non-zero (error 70354) and must evenly divide the range span (error 70355 `VARIABLE_RANGE_INCR_DIV_EQUALLY_ERR`), and must not exceed the range span itself (error 70353 `VARIABLE_RANGE_INCR_LESSTHAN_RANGESIZE`). |
| `defaultValue` | String (numeric) | **Yes** in `defaultData`; optional in `userSpecificData` entries | Must fall within `[minValue, maxValue]` (error 70356 `VARIABLE_RANGE_DEF_BW_MINMAX_RANGE`). |

**Additional field on `userSpecificData` entries only (not on `defaultData`):**

| Field | Type | Mandatory | Description |
|-------|------|-----------|--------------|
| `emailIds` | JSONArray of String | **Yes** | Email addresses of the users this entry's values/range/default apply to. Each email address may appear in only one `userSpecificData` entry per variable (error 70341 `VARIABLE_DUPLICATE_MAIL_ID_OR_GROUP` on duplicates). Cannot be empty (error 70348 `VARIABLE_EMAIL_NOT_PRESENT`). |
| `domainName` | String | No | Only relevant for White Label/Client Portal workspaces with multiple custom domains. Associates this override entry with a specific portal domain's user base rather than the workspace's default domain. Omit for standard (non-portal) workspaces. |

> **`defaultData` is internally the "everyone else" bucket.** Any user whose email is not present in any `userSpecificData` entry resolves the variable using `defaultData`. There is no separate mechanism to mark a `userSpecificData` entry as the fallback — that role belongs exclusively to the top-level `defaultData` object.

### `format` Fields

| Field | Type | Applies To | Description |
|-------|------|------------|--------------|
| `alignment` | String | All types | Display alignment, e.g. `"Left"`, `"Right"`. |
| `decimalPlaces` | Integer | Number, Positive Number, Decimal Number, Currency, Percentage | Number of decimal places to display. `-1` means "auto" (no fixed precision). |
| `userLocale` | Boolean | Numeric types | If `true`, formats the number according to the viewing user's locale settings rather than a fixed format. |
| `thousandSeparator` | Integer (enum) | Numeric types | Thousands grouping symbol selector (workspace-locale-dependent numeric code; `0` = none/default). |
| `decimalSeparator` | Integer (enum) | Numeric types | Decimal point symbol selector (workspace-locale-dependent numeric code; `0` = default `.`). |
| `units` | String | Numeric types | Custom unit label appended to the value, e.g. `"kg"`. `"None"` if not set. |
| `currencySymbol` | String | Currency (`7`) only | Locale-formatted currency symbol string, e.g. `"en;US;"`. |
| `showNegativeSign` | Boolean | Currency (`7`) only | Whether negative currency values are shown with a minus sign or parentheses-style formatting. |
| `showPercent` | Boolean | Percentage (`8`) only | Whether the `%` symbol is appended to displayed values. |
| `dateFormat` | String | Not applicable to variables (no Date data type supported) | Reserved field inherited from the shared format template; has no effect for variables. |
| `numberingType` | Integer | Numeric types | Numbering system selector (e.g., standard vs. Indian numbering system). |

## Notes from the OpenAPI specification

- defaultData is mandatory for a List or a Range variable and is ignored for an All Values variable. Omitting it for the first two returns error 70343.
- The uniqueness check on variableName is case-insensitive, so Region and region are treated as the same name.
- A name that starts with system. or ${, or ends with }, collides with the syntax of internal system variables and is rejected.
- The Range type cannot be combined with the Text data type, because a range needs a numeric data type.
- Each email address may appear in only one userSpecificData entry, so a user cannot carry two conflicting overrides on the same variable.
- Any user whose email address is not listed in a userSpecificData entry resolves the variable through defaultData. There is no way to mark an override entry as the fallback - that role belongs to defaultData alone.
- On a multi-domain client portal, omitting domainName on an override entry applies it to the default domain, while setting it scopes the entry to the users of a specific branded portal domain.
- The values, bounds and defaults are sent as strings even for the numeric data types, so that precision is preserved.
- Permission is stricter here than for most modeling APIs. Only an Account Admin, an Organization Admin or a Workspace Admin can create a variable - there is no alternative granular permission.
- Once created, the variable is referred to elsewhere by name, wrapped as ${variableName}, inside formula expressions, SQL queries and report filters. The variableId is used only for managing the definition itself.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `variableId` | String | Unique ID assigned to the newly created variable. Use as `<variable-id>` for Edit/Delete Variable and Get Variable Details. |

# Examples

## Sample Requests

**Case 1 — List-type Text variable with a per-user override**

```http
POST /restapi/v2/workspaces/137687000271334001/variables HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"variableName":"Region","variableDataType":1,"variableType":0,"defaultData":{"values":["North","South","East","West"],"defaultValue":"North"},"userSpecificData":[{"values":["East","West"],"defaultValue":"East","emailIds":["sales.east@zylker.com"]}],"format":{"alignment":"Left"}}
```

**Case 2 — Range-type Currency variable ("Target Sales")**

```http
POST /restapi/v2/workspaces/137687000271334001/variables HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"variableName":"Target Sales","variableDataType":7,"variableType":1,"defaultData":{"minValue":"10000","maxValue":"100000","stepSize":"5000","defaultValue":"50000"},"format":{"alignment":"Right","currencySymbol":"en;US;","showNegativeSign":true,"decimalPlaces":2}}
```

**Case 3 — All Values-type variable (no default data needed)**

```http
POST /restapi/v2/workspaces/137687000271334001/variables HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"variableName":"All Regions","variableDataType":1,"variableType":3}
```

## Sample Responses

**HTTP 200 OK**

```json
{
  "status": "success",
  "summary": "Create variable",
  "data": {
    "variableId": "137687000006991651"
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Variable](../../../sdk-examples/data-modeling-and-schema/workspace-variables/create-variable.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`defaultData` is mandatory except for All Values** | Submitting `variableType` 0 (List) or 1 (Range) without `defaultData` returns error 70343 `VARIABLE_NO_VARIABLE_DATA_PRESENT`. |
| **`variableName` uniqueness is case-insensitive** | `"Region"` and `"region"` are treated as the same name and the second create attempt is rejected (error 70323 `DUPLICATE_VARIABLE`). |
| **Reserved name patterns are rejected** | Names starting with `system.` or `${`, or ending with `}`, collide with internal system-variable syntax (e.g., `${Region}`) and are rejected with error 70325 `INVALID_VAR_NAME`. |
| **Range is incompatible with Text** | `variableType: 1` (Range) combined with `variableDataType: 1` (Text) is always rejected — ranges require a numeric data type. |
| **Each email may only appear once across all `userSpecificData` entries** | A given user cannot have two conflicting overrides on the same variable. |
| **White Label domain scoping via `domainName`** | In multi-domain Client Portal setups, omitting `domainName` on a `userSpecificData` entry applies it to the calling/default domain; explicitly setting it scopes the entry to a specific branded portal domain's users. |
| **Dependency** | `<workspace-id>` → Get Workspace List. Once created, `variableId` is referenced by name (as `${variableName}`) inside formula expressions, SQL queries, and report filters — it is not directly embedded by ID in other API payloads. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is an Account Admin, Organization Admin, or Workspace Admin. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |
| [70323](../../../foundations/error-codes.md#error-70323) | 400 | `DUPLICATE_USER_VARIABLE` — A variable with this name already exists in the workspace. | Choose a different `variableName`, or edit the existing variable instead. |
| [70324](../../../foundations/error-codes.md#error-70324) | 400 | `BLANK_VARIABLE_NAME` — `variableName` is empty. | Provide a non-empty variable name. |
| [70325](../../../foundations/error-codes.md#error-70325) | 400 | `INVALID_VAR_NAME` — The name uses a reserved pattern (`system.` prefix, `${` prefix, or `}` suffix). | Choose a name that doesn't collide with system-variable syntax. |
| [70335](../../../foundations/error-codes.md#error-70335) | 400 | `VARIABLE_RANGE_NOT_ALLOWED_ON_DT` — Range type combined with Text data type. | Use a numeric `variableDataType` (4, 5, 6, 7, or 8) when `variableType` is Range. |
| [70336](../../../foundations/error-codes.md#error-70336) | 400 | `VARIABLE_DATA_NOT_PRESENT` — No usable value entries could be derived from the request. | Ensure `defaultData` (and any `userSpecificData` entries) contain the required fields for the chosen `variableType`. |
| [70337](../../../foundations/error-codes.md#error-70337) | 400 | `VARIABLE_DEFAULT_VALUE_NOT_PRESENT_IN_LIST` — The `defaultValue` is not one of the `values` supplied for a List-type entry. | Ensure `defaultValue` matches one of the entries in `values`. |
| [70338](../../../foundations/error-codes.md#error-70338) | 400 | `VARIABLE_RANGE_INSUFFICIENT_DATA` / `VARIABLE_RANGE_EXCESS_DATA` — Range entry is missing a required field or has extra unexpected data. | Ensure exactly `minValue`, `maxValue`, and `stepSize` are provided for Range entries. |
| [70339](../../../foundations/error-codes.md#error-70339) | 400 | `VARIABLE_RANGE_INSUFFICIENT_DATA` / `VARIABLE_RANGE_EXCESS_DATA` — Range entry is missing a required field or has extra unexpected data. | Ensure exactly `minValue`, `maxValue`, and `stepSize` are provided for Range entries. |
| [70340](../../../foundations/error-codes.md#error-70340) | 400 | `VARIABLE_RANGE_DEFAULT_VALUE_OUT_OF_RANGE` / `VARIABLE_RANGE_DEF_BW_MINMAX_RANGE` — The `defaultValue` falls outside `[minValue, maxValue]`. | Ensure `defaultValue` lies within the specified range. |
| [70341](../../../foundations/error-codes.md#error-70341) | 400 | `VARIABLE_DUPLICATE_MAIL_ID_OR_GROUP` — The same email address appears in more than one `userSpecificData` entry. | Ensure each email address is listed in only one override entry. |
| [70342](../../../foundations/error-codes.md#error-70342) | 400 | `VARIABLE_ALL_VALUES_NO_VARIABLE_DATA` — `userSpecificData`/`defaultData` were supplied for an All Values-type variable. | Omit `defaultData` and `userSpecificData` entirely when `variableType` is `3`. |
| [70343](../../../foundations/error-codes.md#error-70343) | 400 | `VARIABLE_NO_VARIABLE_DATA_PRESENT` — `defaultData` is missing for a List or Range-type variable. | Supply `defaultData` with the fields required for the chosen `variableType`. |
| [70348](../../../foundations/error-codes.md#error-70348) | 400 | `VARIABLE_EMAIL_NOT_PRESENT` — A `userSpecificData` entry has an empty `emailIds` array. | Ensure every `userSpecificData` entry lists at least one email address. |
| [70350](../../../foundations/error-codes.md#error-70350) | 400 | `VARIABLE_INVALID_VARTYPE` — `variableType` is not one of `0`, `1`, or `3`. | Use only List (`0`), Range (`1`), or All Values (`3`). |
| [70351](../../../foundations/error-codes.md#error-70351) | 400 | `VARIABLE_INVALID_DATATYPE` — `variableDataType` is not one of the six supported values. | Use only `1`, `4`, `5`, `6`, `7`, or `8`. |
| [70352](../../../foundations/error-codes.md#error-70352) | 400 | `VARIABLE_RANGE_MIN_LESS_THAN_MAX` — `minValue` is not less than `maxValue`. | Ensure `minValue` < `maxValue`. |
| [70353](../../../foundations/error-codes.md#error-70353) | 400 | `VARIABLE_RANGE_INCR_LESSTHAN_RANGESIZE` — `stepSize` is larger than the range span. | Reduce `stepSize` so it fits within `maxValue - minValue`. |
| [70354](../../../foundations/error-codes.md#error-70354) | 400 | `VARIABLE_RANGE_INCR_ZERO_ERR` — `stepSize` is zero. | Provide a non-zero `stepSize`. |
| [70355](../../../foundations/error-codes.md#error-70355) | 400 | `VARIABLE_RANGE_INCR_DIV_EQUALLY_ERR` — `stepSize` does not evenly divide the range span. | Choose a `stepSize` that evenly divides `maxValue - minValue`. |
| [70356](../../../foundations/error-codes.md#error-70356) | 400 | `VARIABLE_RANGE_DEFAULT_VALUE_OUT_OF_RANGE` / `VARIABLE_RANGE_DEF_BW_MINMAX_RANGE` — The `defaultValue` falls outside `[minValue, maxValue]`. | Ensure `defaultValue` lies within the specified range. |

# Related

- [Workspace Variables overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Edit Variable](update-variable.md), [Delete Variable](delete-variable.md), [Get Variables](get-variables.md), [Get Variable Details](get-variable-details.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/workspace-variables/create-variable.md).
