---
type: API Endpoint
title: Get Custom Roles
description: "Returns every custom role defined in the organization identified by the ZANALYTICS-ORGID header, along with the complete permission definition of each role."
resource: https://analyticsapi.zoho.com/restapi/v2/orgs/roles
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - custom-roles
  - get
  - usermanagement
api:
  operation_id: getCustomRoles
  method: GET
  path: "/restapi/v2/orgs/roles"
  domain: users-and-groups
  group: custom-roles
  oauth_scopes:
    - ZohoAnalytics.usermanagement.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin of the organization. No other role qualifies; custom roles must be enabled for the organization and included in its plan."
  error_codes:
    - 6142
    - 7301
    - 7309
    - 8083
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1orgs~1roles/get"
    config_schema: null
    response_schema: GetCustomRolesResponse
  sdk_examples: "/sdk-examples/users-and-groups/custom-roles/get-custom-roles.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/user-groups-grouped-api.json"
    title: OpenAPI 3 specification - user-groups-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**GET `/restapi/v2/orgs/roles`** - Get Custom Roles (Custom Roles / Users & Groups).

Returns every custom role defined in the organization, with its full permission definition.

This API takes no path parameters. The organization is identified by the `ZANALYTICS-ORGID` header.

From the OpenAPI specification:

Returns every custom role defined in the organization identified by the ZANALYTICS-ORGID header, along with the complete permission definition of each role.

This is the only way to read a role definition back - there is no get-by-ID variant. The accessType and permissions returned for a role are in exactly the shape accepted by the Update Custom Role API, so a role can be read, edited and posted back without any transformation.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getCustomRoles` |
| HTTP method | GET |
| URL | `/restapi/v2/orgs/roles` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.usermanagement.read`](../../../foundations/oauth-scopes.md#zohoanalyticsusermanagementread) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organization. No other role qualifies; custom roles must be enabled for the organization and included in its plan. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1orgs~1roles/get`; response schema `GetCustomRolesResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.usermanagement.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

This endpoint has no path parameters.

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- The calling user must be an Account Admin or Organization Admin of the organization. No other role qualifies - Workspace Admins, view owners, users holding a custom role and shared users all fail with error code **7301**.
- The custom roles feature must be enabled for the organization, otherwise the API fails with error code **7301** even for an Account Admin. A subscription plan that does not include custom roles fails with error code **6142**.
- This API is not available through a Client Portal (White Label) custom domain. Such requests are rejected with error code **7301** before any business logic runs.
- There is no path parameter for the organization - the roles returned belong to the organization named in the **ZANALYTICS-ORGID** header.
- This is the only API that reads a role definition. There is no get-by-ID variant, so filter the returned list client-side on **roleId** or **roleName**.
- The response is always complete - all seven permission groups and every flag are returned, including the ones set to false. This differs from the request side of the Create and Update APIs, where an omitted flag is treated as false.
- The **accessType** and **permissions** of a role are returned in exactly the shape accepted by the Update Custom Role API. Read the role here, change the flags needed and send the whole object back - this round-trip is the supported way to make a partial permission edit.
- The **roleId** values returned here are required as the role-id path parameter of the Update Custom Role and Delete Custom Role APIs. They are returned as strings even though they are numeric.
- The response reports role definitions only. It does not indicate which users hold a role.
- The list is not paginated and its order is not guaranteed. Sort client-side if presentation order matters.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | `"success"` on success. |
| `summary` | String | `"Get roles"`. |
| `data` | Object | Wrapper. |
| `data.roles` | Array | Every custom role in the organization. Empty when none are defined. |
| `data.roles[].roleId` | String | ID of the role, **as a string**. The `<role-id>` for [Update Custom Role](update-custom-role.md) and [Delete Custom Role](delete-custom-role.md). |
| `data.roles[].roleName` | String | Display name of the role. |
| `data.roles[].accessType` | String | One of the three levels. See [The `accessType` Hierarchy](overview.md#the-accesstype-hierarchy). |
| `data.roles[].permissions` | Object | The complete permission definition, in seven groups. |
| `data.roles[].permissions.createPermissions` | Object | Creation flags — see [Permission Reference](overview.md#permission-reference). |
| `data.roles[].permissions.dataPermissions` | Object | Row and import flags. |
| `data.roles[].permissions.designPermissions` | Object | Design-modification flag. |
| `data.roles[].permissions.interactionPermissions` | Object | Viewing and exploration flags. |
| `data.roles[].permissions.sharePermissions` | Object | Sharing, discussion, and preset flags. |
| `data.roles[].permissions.publishPermissions` | Object | Export, schedule, alert, and publishing flags. |
| `data.roles[].permissions.datasourcePermissions` | Object | Datasource management flags. |

Every leaf inside the seven groups is a JSON **boolean**.

# Examples

## Sample Requests

```http
GET /restapi/v2/orgs/roles HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

There is nothing else to send.

## Sample Responses

**HTTP 200 OK — one role at the full access level**

```json
{
  "status": "success",
  "summary": "Get roles",
  "data": {
    "roles": [
      {
        "roleId": "320875000000477455",
        "roleName": "cr_tagging",
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
            "importDeleteAllAdd": true,
            "dataArchives": true
          },
          "designPermissions": {
            "designModify": true
          },
          "interactionPermissions": {
            "read": true,
            "insight": true,
            "vud": true,
            "drillDown": false,
            "drillThrough": false,
            "drillActions": false
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
            "viewDatasource": false,
            "editDatasource": false,
            "syncData": false,
            "useDatasource": false,
            "removeDatasource": false
          }
        }
      }
    ]
  }
}
```

Note that **every group and every flag is present**, including the ones set to `false`. The response is a complete definition, not a diff.

**HTTP 200 OK — an organization with no custom roles**

```json
{
  "status": "success",
  "summary": "Get roles",
  "data": {
    "roles": []
  }
}
```

**HTTP 400 Bad Request — the plan does not include custom roles**

```json
{
  "status": "failure",
  "summary": "CUSTOMROLES_NOT_ALLOWED_IN_PLAN",
  "data": {
    "errorCode": 6142,
    "errorMessage": "Custom roles is not allowed in this plan."
  }
}
```

**HTTP 403 Forbidden — the caller is not an organization administrator**

```json
{
  "status": "failure",
  "summary": "SECURITY_NOT_PERMITTED",
  "data": {
    "errorCode": 7301,
    "errorMessage": "You do not have the permission to perform this operation."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Custom Roles](../../../sdk-examples/users-and-groups/custom-roles/get-custom-roles.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **It is the only way to read a role's definition** | There is no get-by-ID endpoint. Fetch the list and filter client-side on `roleId` or `roleName`. |
| **The response is the exact input shape for an update** | Take `accessType` and `permissions` from a role here, change what you need, and send them back to [Update Custom Role](update-custom-role.md). This round-trip is the supported way to make a partial edit. |
| **Every flag is returned, including `false` ones** | Unlike the request side, where omission means `false`, the response is always complete. Do not infer that a returned `false` was explicitly set. |
| **`roleId` is a string** | Even though it is numerically a long. Do not parse it into a fixed-width integer type. |
| **Ordering is not guaranteed** | Sort client-side if presentation order matters. |
| **There is no pagination** | The full list is returned in one response. |
| **An empty list is a success** | `{"roles": []}` with HTTP 200. |
| **It reports definitions, not assignments** | The response says nothing about which users hold a role. |
| **Dependency chain:** | Get Custom Roles → `roles[].roleId` → [Update Custom Role](update-custom-role.md) / [Delete Custom Role](delete-custom-role.md); `roles[].permissions` → the body of an update. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6142](../../../foundations/error-codes.md#error-6142) | 400 | `CUSTOMROLES_NOT_ALLOWED_IN_PLAN` — The organization's subscription plan does not include custom roles. | Upgrade the plan. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, custom roles are not enabled for the organization, or the request came through a Client Portal / White Label domain. | Call as an organization administrator from the standard API host, with the feature enabled. |
| [7309](../../../foundations/error-codes.md#error-7309) | 400 | `SECURITY_NEEDS_LOGIN` — No authentication was supplied. | Send an `Authorization` header. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing. | Add the header. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token, or the token lacks the `usermanagement` scope. | Provide a valid token carrying `ZohoAnalytics.usermanagement.read`. |

# Related

- [Custom Roles overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Custom Role](create-custom-role.md), [Update Custom Role](update-custom-role.md), [Delete Custom Role](delete-custom-role.md).
- [SDK examples](../../../sdk-examples/users-and-groups/custom-roles/get-custom-roles.md).
