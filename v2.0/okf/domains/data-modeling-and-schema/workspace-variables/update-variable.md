---
type: API Endpoint
title: Edit Variable
description: Updates an existing workspace variable.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - workspace-variables
  - put
  - modeling
api:
  operation_id: updateVariable
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}"
  domain: data-modeling-and-schema
  group: workspace-variables
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace."
  error_codes:
    - 7301
    - 70323
    - 70324
    - 70325
    - 70329
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
    - 70358
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1variables~1{variable-id}/put"
    config_schema: VariableConfig
    response_schema: null
  sdk_examples: "/sdk-examples/data-modeling-and-schema/workspace-variables/update-variable.md"
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

**PUT `/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}`** - Edit Variable (Workspace Variables / Data Modeling & Schema).

Updates an existing workspace variable. This API takes the **same CONFIG attributes** as Create Variable and requires the **full variable definition to be resent** — there is no partial/incremental update.

From the OpenAPI specification:

Updates an existing workspace variable. This API uses the same configuration structure as the Create Variable API and requires the full definition to be resent, because it replaces the variable rather than patching it.

Renaming is supported, and the type and the data type of a variable can also be changed, provided that no existing reference conflicts with the new shape.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `updateVariable` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1variables~1{variable-id}/put`; CONFIG schema `VariableConfig` |

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
| `{variable-id}` | string | ID of the variable. | [How to obtain](../../../foundations/identifiers.md#variable-id) |

## CONFIG Parameters

Identical structure to [Create Variable](create-variable.md) — `variableName`, `variableDataType`, `variableType`, `defaultData`, `userSpecificData`, `format` — all resent in full. `variableName` is mandatory even when unchanged, since this API also supports **renaming** the variable.

## Notes from the OpenAPI specification

- This API returns HTTP 204 No Content with no response body on success. There is no status or summary key to parse - treat the HTTP status code as the sole success indicator.
- This is a full replace rather than a patch. Every attribute relevant to the current type and data type of the variable must be resent, so omitting defaultData is treated as removing it rather than leaving it unchanged. Fetch the current definition through the Get Variable Details API first, change only what you intend to, then resend the complete configuration.
- Renaming is supported and preserves the variableId along with every reference to the variable, because formulas and filters resolve the name change automatically.
- The duplicate-name check excludes the variable being edited, so resending its current name unchanged does not trigger error 70323.
- This is the only edit API in the suite that can change the fundamental shape of the object, namely variableType and variableDataType. Doing so is blocked with error 70358 when an existing formula or report depends on the variable in a way incompatible with the new shape.
- All the validation rules of the Create Variable API apply here as well, including the mandatory defaultData for a List or a Range variable and the incompatibility of Range with the Text data type.
- Obtain the variable-id from the Get Variables API or the Get Variable Details API.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Rename the variable (all other fields resent unchanged)**

```http
PUT /restapi/v2/workspaces/137687000271334001/variables/137687000006991651 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"variableName":"Sales Region","variableDataType":1,"variableType":0,"defaultData":{"values":["North","South","East","West"],"defaultValue":"North"}}
```

**Case 2 — Update the default value and add a new per-user override**

```http
PUT /restapi/v2/workspaces/137687000271334001/variables/137687000006991651 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"variableName":"Region","variableDataType":1,"variableType":0,"defaultData":{"values":["North","South","East","West"],"defaultValue":"South"},"userSpecificData":[{"values":["East","West"],"defaultValue":"West","emailIds":["sales.east@zylker.com","sales.west@zylker.com"]}]}
```

**Case 3 — Change the format only (values/default resent unchanged)**

```http
PUT /restapi/v2/workspaces/137687000271334001/variables/137687000006991663 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"variableName":"Target Sales","variableDataType":7,"variableType":1,"defaultData":{"minValue":"10000","maxValue":"100000","stepSize":"5000","defaultValue":"50000"},"format":{"alignment":"Right","currencySymbol":"en;GB;","decimalPlaces":0}}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Edit Variable](../../../sdk-examples/data-modeling-and-schema/workspace-variables/update-variable.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Edit Variable returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Full resend required, not a partial patch** | Since the CONFIG template is identical to Create Variable, all fields relevant to the variable's current `variableType`/`variableDataType` must be resent — omitting `defaultData`, for example, is treated the same as removing it, not "leave unchanged." |
| **Renaming is supported** | Changing `variableName` in the request renames the variable while preserving its `variableId` and all references to it elsewhere (formulas, filters resolve the name change automatically). |
| **`variableName` uniqueness check excludes itself** | The duplicate-name check compares against all other variables in the workspace, so resending the same current name (unchanged) does not trigger error 70323. |
| **Changing `variableType`/`variableDataType` can be blocked by existing references** | If the variable is used in formulas or reports in a way that is incompatible with the new type/data type, the edit is rejected with error 70358 `VARIABLE_CANNOT_BE_UPDATED` rather than silently breaking those dependents. |
| **Dependency** | `<variable-id>` → Get Variables or Get Variable Details. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is an Account Admin, Organization Admin, or Workspace Admin. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |
| [70323](../../../foundations/error-codes.md#error-70323) | 400 | `DUPLICATE_USER_VARIABLE` — The new `variableName` collides with a different existing variable. | Choose a name not already used by another variable in the workspace. |
| [70324](../../../foundations/error-codes.md#error-70324) | 400 | `BLANK_VARIABLE_NAME` — `variableName` is empty. | Provide a non-empty variable name. |
| [70325](../../../foundations/error-codes.md#error-70325) | 400 | `INVALID_VAR_NAME` — The name uses a reserved pattern. | Choose a name that doesn't collide with system-variable syntax. |
| [70329](../../../foundations/error-codes.md#error-70329) | 400 | `CANT_DELETE_VARIABLE` (`UNAUTHORIZED_VAR_ACTION`) — `<variable-id>` does not exist in this workspace. | Verify `<variable-id>` using Get Variables. |
| [70335](../../../foundations/error-codes.md#error-70335) | 400 | `VARIABLE_RANGE_NOT_ALLOWED_ON_DT` — Range type combined with Text data type. | Use a numeric `variableDataType` when `variableType` is Range. |
| [70336](../../../foundations/error-codes.md#error-70336) | 400 | No usable value entry could be derived from the request. | Ensure that defaultData, and any userSpecificData entry, carries the attributes required by the chosen variableType. |
| [70337](../../../foundations/error-codes.md#error-70337) | 400 | The default value is not one of the values supplied for a List entry. | Ensure that defaultValue matches one of the entries of values. |
| [70338](../../../foundations/error-codes.md#error-70338) | 400 | A Range entry is missing a required attribute. | Send exactly minValue, maxValue and stepSize for a Range entry. |
| [70339](../../../foundations/error-codes.md#error-70339) | 400 | A Range entry carries unexpected extra data. | Send exactly minValue, maxValue and stepSize for a Range entry. |
| [70340](../../../foundations/error-codes.md#error-70340) | 400 | The default value falls outside the range. | Ensure that defaultValue lies between minValue and maxValue. |
| [70341](../../../foundations/error-codes.md#error-70341) | 400 | The same email address appears in more than one userSpecificData entry. | Ensure that each email address is listed in only one override entry. |
| [70342](../../../foundations/error-codes.md#error-70342) | 400 | Value data was supplied for an All Values variable. | Omit defaultData and userSpecificData entirely when variableType is 3. |
| [70343](../../../foundations/error-codes.md#error-70343) | 400 | defaultData is missing for a List or a Range variable. | Send defaultData carrying the attributes required by the chosen variableType. |
| [70348](../../../foundations/error-codes.md#error-70348) | 400 | A userSpecificData entry has an empty emailIds array. | Ensure that every override entry lists at least one email address. |
| [70350](../../../foundations/error-codes.md#error-70350) | 400 | variableType is not one of the accepted values. | Use only List, Range or All Values, that is 0, 1 or 3. |
| [70351](../../../foundations/error-codes.md#error-70351) | 400 | variableDataType is not one of the six supported values. | Use only 1, 4, 5, 6, 7 or 8. |
| [70352](../../../foundations/error-codes.md#error-70352) | 400 | minValue is not less than maxValue. | Ensure that minValue is smaller than maxValue. |
| [70353](../../../foundations/error-codes.md#error-70353) | 400 | stepSize is larger than the span of the range. | Reduce stepSize so that it fits within the difference between maxValue and minValue. |
| [70354](../../../foundations/error-codes.md#error-70354) | 400 | stepSize is zero. | Send a non-zero stepSize. |
| [70355](../../../foundations/error-codes.md#error-70355) | 400 | stepSize does not divide the span of the range evenly. | Choose a stepSize that divides the difference between maxValue and minValue evenly. |
| [70356](../../../foundations/error-codes.md#error-70356) | 400 | The default value falls outside the range. | Ensure that defaultValue lies between minValue and maxValue. |
| [70358](../../../foundations/error-codes.md#error-70358) | 400 | `VARIABLE_CANNOT_BE_UPDATED` — The requested type/data type change conflicts with existing formula/report references to this variable. | Remove or update the dependent formulas/reports first, or keep the existing `variableType`/`variableDataType`. |

# Related

- [Workspace Variables overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Variable](create-variable.md), [Delete Variable](delete-variable.md), [Get Variables](get-variables.md), [Get Variable Details](get-variable-details.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/workspace-variables/update-variable.md).
