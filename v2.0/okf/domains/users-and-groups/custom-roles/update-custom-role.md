---
type: API Endpoint
title: Update Custom Role
description: "Renames a custom role, replaces its access type and permissions, or does both in one call."
resource: "https://analyticsapi.zoho.com/restapi/v2/orgs/roles/{role-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - custom-roles
  - put
  - usermanagement
api:
  operation_id: updateCustomRole
  method: PUT
  path: "/restapi/v2/orgs/roles/{role-id}"
  domain: users-and-groups
  group: custom-roles
  oauth_scopes:
    - ZohoAnalytics.usermanagement.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin of the organization. No other role qualifies; custom roles must be enabled for the organization and included in its plan."
  error_codes:
    - 6142
    - 7301
    - 7309
    - 7548
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
    - 7580
    - 7581
    - 7584
    - 7585
    - 7586
    - 8083
    - 8504
    - 8507
    - 8509
    - 8525
    - 8534
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1orgs~1roles~1{role-id}/put"
    config_schema: UpdateCustomRoleConfig
    response_schema: null
  sdk_examples: "/sdk-examples/users-and-groups/custom-roles/update-custom-role.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/user-groups-grouped-api.json"
    title: OpenAPI 3 specification - user-groups-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**PUT `/restapi/v2/orgs/roles/{role-id}`** - Update Custom Role (Custom Roles / Users & Groups).

Renames a custom role, replaces its access type and permissions, or both.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<role-id>` | Long | ID of the role to update. Must exist in the organization, otherwise `7548`. A non-numeric value does not reach the API and yields `8525`. |

From the OpenAPI specification:

Renames a custom role, replaces its access type and permissions, or does both in one call.

This is a replace, not a merge. Whenever permissions is supplied, the stored definition is discarded and rebuilt from the object sent - every flag left out becomes false. Read the current definition with the Get Custom Roles API, edit it, and send the whole object back. Sending roleName alone is the one edit that leaves the permission definition untouched.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `updateCustomRole` |
| HTTP method | PUT |
| URL | `/restapi/v2/orgs/roles/{role-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.usermanagement.update`](../../../foundations/oauth-scopes.md#zohoanalyticsusermanagementupdate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organization. No other role qualifies; custom roles must be enabled for the organization and included in its plan. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1orgs~1roles~1{role-id}/put`; CONFIG schema `UpdateCustomRoleConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.usermanagement.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{role-id}` | string | ID of the custom role. | [How to obtain](../../../foundations/identifiers.md#role-id) |

## CONFIG Parameters

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `roleName` | String | Conditional | unchanged | New display name, 1–30 characters. Must be unique across the organization, otherwise `7553`. Omit to keep the current name. |
| `accessType` | String | Conditional | unchanged | New access level. **Must be sent together with `permissions`**, otherwise `7580`. |
| `permissions` | JSONObject | Conditional | unchanged | Complete replacement permission definition. **Must be sent together with `accessType`**, otherwise `7580`. |

Two rules govern which combinations are legal:

- **At least one of `roleName` or `accessType` must be present.** A CONFIG carrying neither fails with [`7581`](../../../foundations/error-codes.md#error-7581).
- **`accessType` and `permissions` are all-or-nothing.** Sending one without the other fails with [`7580`](../../../foundations/error-codes.md#error-7580) — including sending `permissions` alone.

That leaves exactly three valid shapes:

| Shape | Effect |
|-------|--------|
| `roleName` only | Renames the role. `accessType` and `permissions` are preserved untouched. |
| `accessType` + `permissions` | Replaces the access level and the entire permission set. The name is preserved. |
| `roleName` + `accessType` + `permissions` | Replaces everything. |

> **This is a replace, not a merge.** When `permissions` is supplied, the stored definition is discarded and rebuilt from what you sent. Any flag you omit becomes `false`. Read the current definition from [Get Custom Roles](get-custom-roles.md) and edit it, rather than sending only the flags you want to change.

## Notes from the OpenAPI specification

- The calling user must be an Account Admin or Organization Admin of the organization, custom roles must be enabled for the organization, and the request must not arrive through a Client Portal (White Label) custom domain. Any of these failing yields error code **7301**.
- At least one of **roleName** or **accessType** must be present. A CONFIG carrying neither fails with error code **7581**.
- **accessType** and **permissions** are all-or-nothing. Sending one without the other - including sending **permissions** alone - fails with error code **7580**. To change permissions without changing the level, resend the role's current **accessType** alongside them.
- Exactly three CONFIG shapes are valid: **roleName** alone (rename, permissions preserved); **accessType** with **permissions** (level and permission set replaced, name preserved); and all three together (everything replaced).
- **permissions** is replaced, never merged. A payload containing one group wipes the other six, and any flag left out becomes false. Always start from the definition returned by the Get Custom Roles API.
- Whenever **permissions** is supplied it is validated in full with the same rules as the Create Custom Role API, so an update can fail with any of the create-time permission errors.
- Lowering **accessType** is a two-part change. The lower level and the cleaned permission set must arrive in the same payload - a higher-level flag left enabled fails with **7573**, **7574**, **7575**, **7576** or **7584** depending on the group.
- The new **roleName** follows the same rules as on creation - 1 to 30 characters, letters, digits, spaces, underscore and hyphen only, and unique across the organization (**7553**).
- Validation happens before anything is stored. A rejected update leaves the role exactly as it was.
- Changes apply immediately to every user who holds the role. There is no versioning, draft or staged rollout.
- A non-numeric role-id never reaches the API and fails at routing with error code **8525**; a numeric but unknown role-id fails with **7548**.
- The API returns HTTP 204 No Content with an empty body on success. Read the new definition back with the Get Custom Roles API.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

**None.** This API returns `204 No Content` with an empty body. Confirm the change with [Get Custom Roles](get-custom-roles.md).

# Examples

## Sample Requests

**Case 1 — rename only**

The one edit that needs no prior read, and the only shape that leaves permissions alone.

```http
PUT /restapi/v2/orgs/roles/20868000000013096 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded
```

```json
{
  "roleName": "Report Analyst EMEA"
}
```

**Case 2 — replace access level and permissions**

Sent after reading the current definition and editing it. The name is untouched.

```json
{
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
    }
  }
}
```

**Case 3 — rename and redefine in one call**

Downgrading to a lower access level. Every permission above the new ceiling must be absent or `false`, or the call is rejected.

```json
{
  "roleName": "Dashboard Only",
  "accessType": "ALL_DASHBOARDS",
  "permissions": {
    "interactionPermissions": {
      "read": true,
      "vud": true,
      "drillDown": true,
      "insight": true
    },
    "sharePermissions": {
      "share": true,
      "discussion": true
    },
    "publishPermissions": {
      "export": true
    },
    "createPermissions": {
      "createFolder": true
    }
  }
}
```

## Sample Responses

**HTTP 204 No Content — the role was updated**

```
HTTP/1.1 204 No Content
```

There is no response body. Read the new definition back with [Get Custom Roles](get-custom-roles.md).

**HTTP 400 Bad Request — nothing to update**

```json
{
  "status": "failure",
  "summary": "CR_NO_FIELDS_TO_UPDATE",
  "data": {
    "errorCode": 7581,
    "errorMessage": "At least one of roleName, accessType with permissions must be provided for update."
  }
}
```

**HTTP 400 Bad Request — `accessType` sent without `permissions`**

```json
{
  "status": "failure",
  "summary": "CR_ACCESS_TYPE_AND_PERMS_REQUIRED_TOGETHER",
  "data": {
    "errorCode": 7580,
    "errorMessage": "Both accessType and permissions must be provided together."
  }
}
```

**HTTP 400 Bad Request — the role does not exist**

```json
{
  "status": "failure",
  "summary": "NO_SUCH_ROLE_EXIST",
  "data": {
    "errorCode": 7548,
    "errorMessage": "The given role does not exist."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Update Custom Role](../../../sdk-examples/users-and-groups/custom-roles/update-custom-role.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **`permissions` is replaced, never merged** | This is the most consequential behaviour of the API. A payload containing one group wipes the other six. Always start from a [Get Custom Roles](get-custom-roles.md) response. |
| **`permissions` alone is rejected** | Even though it looks like the natural way to edit permissions, it fails with `7580`. `accessType` must accompany it — resend the role's current level if you are not changing it. |
| **A rename is the only safe standalone edit** | `roleName` on its own preserves the entire permission definition. |
| **The same eleven rules apply as on create** | Whenever `permissions` is supplied it is validated in full, so an update can fail with any of the create-time permission errors. |
| **Downgrading `accessType` requires cleaning the permissions first** | Lowering the level while leaving a higher-level flag `true` fails with `7573`, `7574`, `7575`, `7576`, or `7584` depending on which flag. Strip them in the same payload. |
| **Validation happens before anything is stored** | A rejected update leaves the role exactly as it was. |
| **Existing holders are affected immediately** | Users already assigned the role take on the new definition; there is no versioning and no migration step. |
| **A non-numeric `<role-id>` never reaches the API** | It fails at routing with `8525` rather than `7548`. |
| **One role per call** | There is no bulk-update variant. |
| **Dependency chain:** | [Get Custom Roles](get-custom-roles.md) → `roleId` + `accessType` + `permissions` → edit → Update Custom Role → [Get Custom Roles](get-custom-roles.md) to verify. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6142](../../../foundations/error-codes.md#error-6142) | 400 | `CUSTOMROLES_NOT_ALLOWED_IN_PLAN` — The plan does not include custom roles. | Upgrade the plan. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an organization administrator, the feature is not enabled, or the request came through a Client Portal / White Label domain. | Call as an organization administrator from the standard API host. |
| [7309](../../../foundations/error-codes.md#error-7309) | 400 | `SECURITY_NEEDS_LOGIN` — No authentication was supplied. | Send an `Authorization` header. |
| [7548](../../../foundations/error-codes.md#error-7548) | 400 | `NO_SUCH_ROLE_EXIST` — No role exists for the given `<role-id>`. | Verify the ID with [Get Custom Roles](get-custom-roles.md). |
| [7553](../../../foundations/error-codes.md#error-7553) | 400 | `ROLENAME_EXISTS` — Another role already uses the new name. | Choose a different name. |
| [7554](../../../foundations/error-codes.md#error-7554) | 400 | `INVALID_VIEWTYPE_GROUP` — `accessType` did not resolve to a known level. | Send one of the three documented values. |
| [7559](../../../foundations/error-codes.md#error-7559) | 400 | `EXPORT_PERM_NEEDED_FOR_EMAILSCH` — `manageEmailSchedules` is `true` but `export` is not. | Set `publishPermissions.export` to `true`. |
| [7573](../../../foundations/error-codes.md#error-7573) | 400 | `CR_DATA_PERM_NOT_ALLOWED_FOR_ACCESS_TYPE` — A data permission is enabled below the full access level. | Raise `accessType`, or disable those flags. |
| [7574](../../../foundations/error-codes.md#error-7574) | 400 | `CR_DESIGN_PERM_NOT_ALLOWED_FOR_ACCESS_TYPE` — `designModify` is enabled below the full access level. | Raise `accessType`, or disable it. |
| [7575](../../../foundations/error-codes.md#error-7575) | 400 | `CR_CREATE_PERM_NOT_ALLOWED_FOR_ACCESS_TYPE` — A data-level creation flag is enabled below the full access level. | Raise `accessType`, or disable those flags. |
| [7576](../../../foundations/error-codes.md#error-7576) | 400 | `CR_ALERT_PERM_NOT_ALLOWED_FOR_ACCESS_TYPE` — `manageDataAlerts` is enabled with `ALL_DASHBOARDS`. | Use a higher `accessType`, or disable the flag. |
| [7577](../../../foundations/error-codes.md#error-7577) | 400 | `CR_SCHEDULED_DATA_DELETION_PERM_NOT_ALLOWED` — `dataArchives` is `true` but not every data permission is enabled. | Enable all data permissions, or disable `dataArchives`. |
| [7578](../../../foundations/error-codes.md#error-7578) | 400 | `CR_DESIGN_MODIFY_REQUIRES_PRESET_PERMS` — `designModify` is `true` without both preset permissions. | Set `accessAdminPresets` and `createPreset` to `true`. |
| [7579](../../../foundations/error-codes.md#error-7579) | 400 | `CR_READ_PERM_MUST_BE_ENABLED` — `interactionPermissions.read` is missing or `false`. | Set `read` to `true`. |
| [7580](../../../foundations/error-codes.md#error-7580) | 400 | `CR_ACCESS_TYPE_AND_PERMS_REQUIRED_TOGETHER` — One of `accessType` / `permissions` was sent without the other. | Send both, or neither. |
| [7581](../../../foundations/error-codes.md#error-7581) | 400 | `CR_NO_FIELDS_TO_UPDATE` — Neither `roleName` nor `accessType` was supplied. | Send at least one. |
| [7584](../../../foundations/error-codes.md#error-7584) | 400 | `CR_DATASOURCE_PERM_NOT_ALLOWED_FOR_ACCESS_TYPE` — A datasource permission is enabled below the full access level. | Raise `accessType`, or disable the group. |
| [7585](../../../foundations/error-codes.md#error-7585) | 400 | `CR_USE_DATASOURCE_REQUIRES_CREATETABLE` — `useDatasource` is `true` but `createTable` is not. | Enable `createPermissions.createTable`. |
| [7586](../../../foundations/error-codes.md#error-7586) | 400 | `CR_VIEW_DATASOURCE_REQUIRED_FOR_DATASOURCE_PERMS` — Another datasource permission is enabled without `viewDatasource`. | Set `datasourcePermissions.viewDatasource` to `true`. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing. | Add the header. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` was not sent. | Send a CONFIG object. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | `MORE_THAN_MAX_LENGTH` — `roleName` exceeds 30 characters, or `permissions` exceeds its size limit. | Shorten the value. |
| [8509](../../../foundations/error-codes.md#error-8509) | 400 | `PATTERN_NOT_MATCHED` — `roleName` contains disallowed characters, or `accessType` is not one of the three values. | Correct the value. |
| [8525](../../../foundations/error-codes.md#error-8525) | 400 | `URL_RULE_NOT_CONFIGURED` — `<role-id>` is not numeric, so the request matched no route. | Send a numeric role ID. |
| [8534](../../../foundations/error-codes.md#error-8534) | 400 | `JSON_PARSE_ERROR` — `CONFIG` is not valid JSON. | Fix the JSON and URL-encode it correctly. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token, or the token lacks the `usermanagement` scope. | Provide a valid token carrying `ZohoAnalytics.usermanagement.update`. |

# Related

- [Custom Roles overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Custom Roles](get-custom-roles.md), [Create Custom Role](create-custom-role.md), [Delete Custom Role](delete-custom-role.md).
- [SDK examples](../../../sdk-examples/users-and-groups/custom-roles/update-custom-role.md).
