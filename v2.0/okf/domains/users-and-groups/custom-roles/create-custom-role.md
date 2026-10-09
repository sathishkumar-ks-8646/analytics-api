---
type: API Endpoint
title: Create Custom Role
description: Creates one custom role in the organization.
resource: https://analyticsapi.zoho.com/restapi/v2/orgs/roles
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - custom-roles
  - post
  - usermanagement
api:
  operation_id: createCustomRole
  method: POST
  path: "/restapi/v2/orgs/roles"
  domain: users-and-groups
  group: custom-roles
  oauth_scopes:
    - ZohoAnalytics.usermanagement.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin of the organization. No other role qualifies; custom roles must be enabled for the organization and included in its plan."
  error_codes:
    - 6142
    - 7301
    - 7309
    - 7553
    - 7554
    - 7559
    - 7573
    - 7574
    - 7575
    - 7576
    - 7577
    - 7578
    - 7579
    - 7584
    - 7585
    - 7586
    - 8078
    - 8083
    - 8504
    - 8507
    - 8509
    - 8534
    - 8535
    - 8539
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1orgs~1roles/post"
    config_schema: CreateCustomRoleConfig
    response_schema: CreateCustomRoleResponse
  sdk_examples: "/sdk-examples/users-and-groups/custom-roles/create-custom-role.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/user-groups-grouped-api.json"
    title: OpenAPI 3 specification - user-groups-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

**POST `/restapi/v2/orgs/roles`** - Create Custom Role (Custom Roles / Users & Groups).

Creates one custom role in the organization.

This API takes no path parameters.

From the OpenAPI specification:

Creates one custom role in the organization.

The role name, the access type and the permissions are all mandatory. The permissions are validated as a whole against the access type and against the cross-group dependency rules before anything is stored, so a rejected request creates nothing and can be corrected and retried safely.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createCustomRole` |
| HTTP method | POST |
| URL | `/restapi/v2/orgs/roles` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.usermanagement.create`](../../../foundations/oauth-scopes.md#zohoanalyticsusermanagementcreate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organization. No other role qualifies; custom roles must be enabled for the organization and included in its plan. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1orgs~1roles/post`; CONFIG schema `CreateCustomRoleConfig`; response schema `CreateCustomRoleResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.usermanagement.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

This endpoint has no path parameters.

## CONFIG Parameters

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `roleName` | String | **Yes** | — | Display name of the role, 1–30 characters. Letters, digits, spaces, underscore, and hyphen only. Must be unique across the organization, otherwise `7553`. |
| `accessType` | String | **Yes** | — | One of `ALL_DASHBOARDS`, `ALL_REPORTS_AND_DASHBOARDS`, `ALL_DATA_REPORTS_AND_DASHBOARDS`. See [The `accessType` Hierarchy](overview.md#the-accesstype-hierarchy). |
| `permissions` | JSONObject | **Yes** | — | The permission definition, in up to seven groups, serialized to at most 5,000 characters. Groups you omit are treated as all-`false`. Must satisfy every rule in [Permission Dependency Rules](overview.md#permission-dependency-rules). |

All three are mandatory. Omitting any of them fails with [`8504`](../../../foundations/error-codes.md#error-8504); sending one empty fails with [`8539`](../../../foundations/error-codes.md#error-8539) or [`8078`](../../../foundations/error-codes.md#error-8078).

## Notes from the OpenAPI specification

- The calling user must be an Account Admin or Organization Admin of the organization, custom roles must be enabled for the organization, and the request must not arrive through a Client Portal (White Label) custom domain. Any of these failing yields error code **7301**.
- **roleName**, **accessType** and **permissions** are all mandatory. Omitting any of them fails with error code **8504**; sending one with an empty value fails with error code **8539** or **8078**.
- **roleName** is limited to 1 to 30 characters made of letters, digits, spaces, underscore and hyphen, and must be unique across the organization - the uniqueness check covers built-in role names too. A longer name fails with error code **8507**, disallowed characters fail with **8509**, and a clash fails with **7553**.
- **accessType** is a ceiling. Every permission group is only available at or above a given level - see the CustomRolePermissions schema. Enabling a permission above the chosen level is an error (**7573**, **7574**, **7575**, **7576** or **7584** depending on the group), not a silent no-op.
- **interactionPermissions.read** must be explicitly true. It is not defaulted - a **permissions** object that omits **interactionPermissions** entirely, or sets **read** to false, fails with error code **7579** before any other rule is evaluated.
- Every flag that is omitted from **permissions** is treated as false. A group that is left out is entirely disabled.
- Four rules reach across permission groups: **designModify** requires both **accessAdminPresets** and **createPreset** (**7578**); **manageEmailSchedules** requires **export** (**7559**); **useDatasource** requires **createTable** (**7585**); and **editDatasource**, **syncData**, **useDatasource** and **removeDatasource** each require **viewDatasource** (**7586**). **dataArchives** additionally requires every other data permission to be enabled (**7577**).
- All validation runs before anything is stored, and the rules fire in a fixed order, so a payload with several problems reports one error at a time. A rejected request creates no role and is safe to correct and retry.
- This API is not an upsert. Re-creating an existing name fails with error code **7553** rather than returning or updating the existing role.
- One role is created per call. There is no bulk-create variant.
- Creating a role grants nothing by itself. Until the role is assigned to a user or a workspace through the user management and sharing APIs, it has no effect.
- Only the new **roleId** is returned. Use the Get Custom Roles API to read the stored definition back.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | `"success"` on success. |
| `summary` | String | `"Create role"`. |
| `data` | Object | Wrapper. |
| `data.roleId` | String | ID of the new role, **as a string**. This is the only place it is returned on creation; capture it. It becomes `<role-id>` for [Update Custom Role](update-custom-role.md) and [Delete Custom Role](delete-custom-role.md). |

# Examples

## Sample Requests

**Case 1 — a dashboard-only role**

The most restricted level. No data, design, or datasource permissions may appear, and `createFolder` is the only creation flag available.

```http
POST /restapi/v2/orgs/roles HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded
```

```json
{
  "roleName": "Dashboard Viewer",
  "accessType": "ALL_DASHBOARDS",
  "permissions": {
    "interactionPermissions": {
      "read": true,
      "vud": true,
      "drillDown": true,
      "insight": true,
      "drillThrough": true,
      "drillActions": true
    },
    "publishPermissions": {
      "export": true,
      "publicViews": true,
      "createSlideshow": true,
      "manageEmailSchedules": true,
      "allEmailSchedulesAccess": true
    },
    "sharePermissions": {
      "share": true,
      "discussion": true,
      "accessAdminPresets": true,
      "createPreset": true,
      "privateLinks": true
    },
    "createPermissions": {
      "createFolder": true
    }
  }
}
```

Note `export: true` alongside `manageEmailSchedules: true` — rule 8 requires it.

**Case 2 — reports and dashboards, with alerts**

Raising the access level unlocks `manageDataAlerts`, which `ALL_DASHBOARDS` would reject with [`7576`](../../../foundations/error-codes.md#error-7576).

```json
{
  "roleName": "Report Analyst",
  "accessType": "ALL_REPORTS_AND_DASHBOARDS",
  "permissions": {
    "interactionPermissions": {
      "read": true,
      "vud": true,
      "drillDown": true,
      "insight": true,
      "drillThrough": true,
      "drillActions": true
    },
    "publishPermissions": {
      "export": true,
      "publicViews": true,
      "manageDataAlerts": true,
      "allDataAlertsAccess": true,
      "createSlideshow": true,
      "manageEmailSchedules": true,
      "allEmailSchedulesAccess": true
    },
    "sharePermissions": {
      "share": true,
      "discussion": true,
      "accessAdminPresets": true,
      "createPreset": true,
      "privateLinks": true
    },
    "createPermissions": {
      "createFolder": true
    }
  }
}
```

**Case 3 — full access, covering every group**

The only level at which `dataPermissions`, `designPermissions`, `datasourcePermissions`, and the table-creation flags are legal. This payload satisfies rules 7 (design modify pulls in both preset permissions), 9 (`useDatasource` pulls in `createTable`), and 10 (every other datasource flag pulls in `viewDatasource`).

```json
{
  "roleName": "Data Engineer",
  "accessType": "ALL_DATA_REPORTS_AND_DASHBOARDS",
  "permissions": {
    "createPermissions": {
      "createTable": true,
      "createQueryTable": true,
      "createFolder": true,
      "createFormula": true
    },
    "dataPermissions": {
      "addRow": true,
      "modifyRow": true,
      "deleteRow": true,
      "importAppend": true,
      "importAddOrUpdate": true,
      "importDeleteAllAdd": true
    },
    "designPermissions": {
      "designModify": true
    },
    "interactionPermissions": {
      "read": true,
      "vud": true,
      "drillDown": true,
      "insight": true,
      "drillThrough": true,
      "drillActions": true
    },
    "sharePermissions": {
      "share": true,
      "discussion": true,
      "privateLinks": true,
      "accessAdminPresets": true,
      "createPreset": true
    },
    "publishPermissions": {
      "export": true,
      "manageEmailSchedules": true,
      "allEmailSchedulesAccess": true,
      "manageDataAlerts": true,
      "allDataAlertsAccess": true,
      "createSlideshow": true,
      "publicViews": true
    },
    "datasourcePermissions": {
      "viewDatasource": true,
      "editDatasource": true,
      "syncData": true,
      "useDatasource": true,
      "removeDatasource": true
    }
  }
}
```

## Sample Responses

**HTTP 200 OK — the role was created**

```json
{
  "status": "success",
  "summary": "Create role",
  "data": {
    "roleId": "20868000000013096"
  }
}
```

**HTTP 400 Bad Request — `read` was not enabled**

```json
{
  "status": "failure",
  "summary": "CR_READ_PERM_MUST_BE_ENABLED",
  "data": {
    "errorCode": 7579,
    "errorMessage": "Read permission must always be enabled."
  }
}
```

**HTTP 400 Bad Request — a data permission at a level that does not allow it**

```json
{
  "status": "failure",
  "summary": "CR_DATA_PERM_NOT_ALLOWED_FOR_ACCESS_TYPE",
  "data": {
    "errorCode": 7573,
    "errorMessage": "Data permissions (Add Row, Modify Row, Delete Row, Import Data, etc.) are only allowed when the access type includes All Data, Reports And Dashboards."
  }
}
```

**HTTP 400 Bad Request — email schedules without export**

```json
{
  "status": "failure",
  "summary": "EXPORT_PERM_NEEDED_FOR_EMAILSCH",
  "data": {
    "errorCode": 7559,
    "errorMessage": "Export permission is necessary for Managing Email Schedules."
  }
}
```

**HTTP 400 Bad Request — the name is already in use**

```json
{
  "status": "failure",
  "summary": "ROLENAME_EXISTS",
  "data": {
    "errorCode": 7553,
    "errorMessage": "A role with the same name already exists. Please provide a different name"
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Custom Role](../../../sdk-examples/users-and-groups/custom-roles/create-custom-role.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **All three CONFIG attributes are mandatory** | Unlike [Update Custom Role](update-custom-role.md), which accepts `roleName` alone. |
| **Omitted permission flags are `false`** | There is no "inherit" or "default on". A group you leave out is entirely disabled — except `read`, which must be explicitly `true`. |
| **Validation is complete before anything is stored** | A rejected request creates no role, so a failed call is safe to correct and retry. |
| **Rules fire in a fixed order** | `read` is checked first, so a payload with several problems reports `7579` before anything else. Fix and resend to surface the next one. |
| **Names compete with built-in roles too** | `7553` covers a clash with any existing role name in the organization, not only with other custom roles. |
| **`roleName` is limited to 30 characters** | Longer names fail with `8507`, and characters outside letters, digits, space, underscore, and hyphen fail with `8509`. |
| **It is not an upsert** | Re-creating an existing name fails rather than returning or updating the existing role. |
| **One role per call** | There is no bulk-create variant. |
| **Creating a role grants nothing by itself** | Until the role is assigned to a user or workspace elsewhere, it has no effect. |
| **Dependency chain:** | Create Custom Role → `data.roleId` → [Get Custom Roles](get-custom-roles.md) to verify → [Update Custom Role](update-custom-role.md) / [Delete Custom Role](delete-custom-role.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6142](../../../foundations/error-codes.md#error-6142) | 400 | `CUSTOMROLES_NOT_ALLOWED_IN_PLAN` — The plan does not include custom roles. | Upgrade the plan. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an organization administrator, the feature is not enabled, or the request came through a Client Portal / White Label domain. | Call as an organization administrator from the standard API host. |
| [7309](../../../foundations/error-codes.md#error-7309) | 400 | `SECURITY_NEEDS_LOGIN` — No authentication was supplied. | Send an `Authorization` header. |
| [7553](../../../foundations/error-codes.md#error-7553) | 400 | `ROLENAME_EXISTS` — A role with this name already exists in the organization. | Choose a different name. |
| [7554](../../../foundations/error-codes.md#error-7554) | 400 | `INVALID_VIEWTYPE_GROUP` — `accessType` did not resolve to a known level. | Send one of the three documented values. |
| [7559](../../../foundations/error-codes.md#error-7559) | 400 | `EXPORT_PERM_NEEDED_FOR_EMAILSCH` — `manageEmailSchedules` is `true` but `export` is not. | Set `publishPermissions.export` to `true`. |
| [7573](../../../foundations/error-codes.md#error-7573) | 400 | `CR_DATA_PERM_NOT_ALLOWED_FOR_ACCESS_TYPE` — A data permission was enabled below the full access level. | Raise `accessType`, or set every `dataPermissions` flag to `false`. |
| [7574](../../../foundations/error-codes.md#error-7574) | 400 | `CR_DESIGN_PERM_NOT_ALLOWED_FOR_ACCESS_TYPE` — `designModify` was enabled below the full access level. | Raise `accessType`, or disable `designModify`. |
| [7575](../../../foundations/error-codes.md#error-7575) | 400 | `CR_CREATE_PERM_NOT_ALLOWED_FOR_ACCESS_TYPE` — `createTable`, `createQueryTable`, or `createFormula` was enabled below the full access level. | Raise `accessType`, or disable those flags. `createFolder` is allowed at every level. |
| [7576](../../../foundations/error-codes.md#error-7576) | 400 | `CR_ALERT_PERM_NOT_ALLOWED_FOR_ACCESS_TYPE` — `manageDataAlerts` was enabled with `ALL_DASHBOARDS`. | Use `ALL_REPORTS_AND_DASHBOARDS` or higher, or disable the flag. |
| [7577](../../../foundations/error-codes.md#error-7577) | 400 | `CR_SCHEDULED_DATA_DELETION_PERM_NOT_ALLOWED` — `dataArchives` is `true` but not every data permission is enabled. | Enable all data permissions, or disable `dataArchives`. |
| [7578](../../../foundations/error-codes.md#error-7578) | 400 | `CR_DESIGN_MODIFY_REQUIRES_PRESET_PERMS` — `designModify` is `true` without both preset permissions. | Set `accessAdminPresets` and `createPreset` to `true`. |
| [7579](../../../foundations/error-codes.md#error-7579) | 400 | `CR_READ_PERM_MUST_BE_ENABLED` — `interactionPermissions.read` is missing or `false`. | Set `read` to `true`. |
| [7584](../../../foundations/error-codes.md#error-7584) | 400 | `CR_DATASOURCE_PERM_NOT_ALLOWED_FOR_ACCESS_TYPE` — A datasource permission was enabled below the full access level. | Raise `accessType`, or disable the datasource group. |
| [7585](../../../foundations/error-codes.md#error-7585) | 400 | `CR_USE_DATASOURCE_REQUIRES_CREATETABLE` — `useDatasource` is `true` but `createTable` is not. | Enable `createPermissions.createTable`. |
| [7586](../../../foundations/error-codes.md#error-7586) | 400 | `CR_VIEW_DATASOURCE_REQUIRED_FOR_DATASOURCE_PERMS` — Another datasource permission is enabled without `viewDatasource`. | Set `datasourcePermissions.viewDatasource` to `true`. |
| [8078](../../../foundations/error-codes.md#error-8078) | 400 | `EMPTY_JSON_ATTRIBUTE_FOUND` — A mandatory attribute was sent blank. | The message names the attribute. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing. | Add the header. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` was not sent, or a mandatory attribute is missing. | Send `roleName`, `accessType`, and `permissions`. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | `MORE_THAN_MAX_LENGTH` — `roleName` exceeds 30 characters, or `permissions` exceeds its size limit. | Shorten the value. |
| [8509](../../../foundations/error-codes.md#error-8509) | 400 | `PATTERN_NOT_MATCHED` — `roleName` contains disallowed characters, or `accessType` is not one of the three values. | Correct the value. |
| [8534](../../../foundations/error-codes.md#error-8534) | 400 | `JSON_PARSE_ERROR` — `CONFIG` is not valid JSON. | Fix the JSON and URL-encode it correctly. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token, or the token lacks the `usermanagement` scope. | Provide a valid token carrying `ZohoAnalytics.usermanagement.create`. |
| [8539](../../../foundations/error-codes.md#error-8539) | 400 | `INVALID_VALUE_NOT_ALLOWED` — An attribute carries a value that is structurally valid but not accepted, such as an empty `roleName`. | Send a non-empty value. |

# Related

- [Custom Roles overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Custom Roles](get-custom-roles.md), [Update Custom Role](update-custom-role.md), [Delete Custom Role](delete-custom-role.md).
- [SDK examples](../../../sdk-examples/users-and-groups/custom-roles/create-custom-role.md).
