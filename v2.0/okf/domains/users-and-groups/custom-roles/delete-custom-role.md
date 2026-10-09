---
type: API Endpoint
title: Delete Custom Role
description: Deletes a custom role definition.
resource: "https://analyticsapi.zoho.com/restapi/v2/orgs/roles/{role-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - custom-roles
  - delete
  - usermanagement
api:
  operation_id: deleteCustomRole
  method: DELETE
  path: "/restapi/v2/orgs/roles/{role-id}"
  domain: users-and-groups
  group: custom-roles
  oauth_scopes:
    - ZohoAnalytics.usermanagement.delete
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin of the organization. No other role qualifies; custom roles must be enabled for the organization and included in its plan."
  error_codes:
    - 6142
    - 7301
    - 7309
    - 7548
    - 8083
    - 8525
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1orgs~1roles~1{role-id}/delete"
    config_schema: null
    response_schema: null
  sdk_examples: "/sdk-examples/users-and-groups/custom-roles/delete-custom-role.md"
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

**DELETE `/restapi/v2/orgs/roles/{role-id}`** - Delete Custom Role (Custom Roles / Users & Groups).

Deletes a custom role definition.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<role-id>` | Long | ID of the role to delete. Must exist in the organization, otherwise `7548`. A non-numeric value does not reach the API and yields `8525`. |

From the OpenAPI specification:

Deletes a custom role definition.

Only the definition is removed. Users who held the role are not deleted, and reassigning them is done through the user management APIs. The operation cannot be undone, and re-creating the same name later produces a new role with a new identifier.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deleteCustomRole` |
| HTTP method | DELETE |
| URL | `/restapi/v2/orgs/roles/{role-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.usermanagement.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsusermanagementdelete) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organization. No other role qualifies; custom roles must be enabled for the organization and included in its plan. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 204 with no body |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1orgs~1roles~1{role-id}/delete` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.usermanagement.delete`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{role-id}` | string | ID of the custom role. | [How to obtain](../../../foundations/identifiers.md#role-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- The calling user must be an Account Admin or Organization Admin of the organization, custom roles must be enabled for the organization, and the request must not arrive through a Client Portal (White Label) custom domain. Any of these failing yields error code **7301**.
- This API removes the role definition only. Users who held the role are not deleted - reassigning them is done through the user management APIs, not here.
- The operation is irreversible. The definition cannot be restored, and re-creating the same name produces a new role with a new **roleId** and no history.
- The API is not idempotent. A second delete of the same role-id fails with error code **7548** rather than returning 204. Treat that as already deleted rather than as a failure to retry.
- The response reports nothing about impact - it does not say how many users held the role. Establish that through the user management APIs before deleting.
- A non-numeric role-id never reaches the API and fails at routing with error code **8525**; a numeric but unknown role-id fails with **7548**.
- One role is deleted per call. There is no bulk-delete variant.
- The API returns HTTP 204 No Content with an empty body on success. Confirm with the Get Custom Roles API.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

**None.** This API returns `204 No Content` with an empty body. Confirm with [Get Custom Roles](get-custom-roles.md).

# Examples

## Sample Requests

```http
DELETE /restapi/v2/orgs/roles/20868000000013096 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

There is nothing else to send.

## Sample Responses

**HTTP 204 No Content — the role was deleted**

```
HTTP/1.1 204 No Content
```

**HTTP 200 OK — reading the role list afterwards**

```json
{
  "status": "success",
  "summary": "Get roles",
  "data": {
    "roles": []
  }
}
```

**HTTP 400 Bad Request — the role does not exist, or was already deleted**

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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Delete Custom Role](../../../sdk-examples/users-and-groups/custom-roles/delete-custom-role.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **It removes the definition only** | Users who held the role are not deleted. Reassigning them is done through the user-management APIs, not here. |
| **There is no undo** | The definition cannot be restored, and re-creating the same name produces a new role with a new `roleId` and no history. |
| **It is not idempotent** | A second delete of the same ID fails with `7548` rather than returning `204`. Treat that as "already gone" rather than as a failure to retry. |
| **The response reports nothing about impact** | It does not say how many users held the role. Establish that before deleting, through the user-management APIs. |
| **A non-numeric `<role-id>` never reaches the API** | It fails at routing with `8525` rather than `7548`. |
| **One role per call** | There is no bulk-delete variant. |
| **Dependency chain:** | [Get Custom Roles](get-custom-roles.md) → `roleId` → Delete Custom Role → [Get Custom Roles](get-custom-roles.md) to verify. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6142](../../../foundations/error-codes.md#error-6142) | 400 | `CUSTOMROLES_NOT_ALLOWED_IN_PLAN` — The plan does not include custom roles. | Upgrade the plan. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an organization administrator, the feature is not enabled, or the request came through a Client Portal / White Label domain. | Call as an organization administrator from the standard API host. |
| [7309](../../../foundations/error-codes.md#error-7309) | 400 | `SECURITY_NEEDS_LOGIN` — No authentication was supplied. | Send an `Authorization` header. |
| [7548](../../../foundations/error-codes.md#error-7548) | 400 | `NO_SUCH_ROLE_EXIST` — No role exists for the given `<role-id>`, or it has already been deleted. | Verify the ID with [Get Custom Roles](get-custom-roles.md). |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing. | Add the header. |
| [8525](../../../foundations/error-codes.md#error-8525) | 400 | `URL_RULE_NOT_CONFIGURED` — `<role-id>` is not numeric, so the request matched no route. | Send a numeric role ID. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token, or the token lacks the `usermanagement` scope. | Provide a valid token carrying `ZohoAnalytics.usermanagement.delete`. |

# Related

- [Custom Roles overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Custom Roles](get-custom-roles.md), [Create Custom Role](create-custom-role.md), [Update Custom Role](update-custom-role.md).
- [SDK examples](../../../sdk-examples/users-and-groups/custom-roles/delete-custom-role.md).
