---
type: API Endpoint
title: Deactivate Users
description: Deactivates one or more users in the specified organization.
resource: https://analyticsapi.zoho.com/restapi/v2/users/inactive
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - org-users
  - put
  - usermanagement
api:
  operation_id: deActivateUsers
  method: PUT
  path: "/restapi/v2/users/inactive"
  domain: users-and-groups
  group: org-users
  oauth_scopes:
    - ZohoAnalytics.usermanagement.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the specified organisation.
  error_codes:
    - 7103
    - 7301
    - 8060
    - 8061
    - 8114
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1users~1inactive/put"
    config_schema: DeactivateUsersConfig
    response_schema: null
  sdk_examples: "/sdk-examples/users-and-groups/org-users/de-activate-users.md"
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

**PUT `/restapi/v2/users/inactive`** - Deactivate Users (Organization Users / Users & Groups).

Deactivates one or more users in the specified organisation. Deactivated users cannot log in or access any workspaces in the org. Their data and permissions are retained and can be restored by reactivating them. This is the recommended approach for temporary suspension (e.g., extended leave) rather than permanent removal.

> **Confirmed account requirement:** The calling user's Zoho account must be confirmed (email-verified) to invoke this API.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deActivateUsers` |
| HTTP method | PUT |
| URL | `/restapi/v2/users/inactive` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.usermanagement.update`](../../../foundations/oauth-scopes.md#zohoanalyticsusermanagementupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID where users should be deactivated. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the specified organisation. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1users~1inactive/put`; CONFIG schema `DeactivateUsersConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.usermanagement.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

This endpoint has no path parameters.

## CONFIG Parameter

CONFIG is **mandatory**. It must be sent as a form-encoded body parameter named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `emailIds` | Array of Strings | **Yes** | — | List of email addresses to deactivate. Maximum 1000 per request. All specified email addresses must already be members of this organisation; non-members cause the request to fail with error **8114**. |
| `domainName` | String | No | `null` | Custom domain name for client portal-based deactivation. When provided, the deactivation is scoped to the custom portal domain context. When omitted, standard org deactivation applies. |

## Notes from the OpenAPI specification

- The Zoho account of the calling user must be confirmed (email verified) to invoke this API.
- A maximum of 1000 email addresses can be sent in a single request.
- The operation is idempotent. Deactivating an already-inactive user succeeds silently and raises no error.
- Every email address in the list must already be a member of the organization. Non-members cause the request to fail with error code **8114**.
- The Account Admin of the organization cannot be deactivated using this API.
- All the workspace shares of the user are preserved while they are deactivated, though the user cannot access them. The shares are restored on reactivation.
- Deactivation is reversible and preserves the user data, shares and role. Removal, performed using the Remove Users API, is permanent - the shares are revoked and the user has to be invited again.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Deactivate a user on leave**

```http
PUT /restapi/v2/users/inactive HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["on.leave@example.com"]}
```

**Case 2 — Deactivate multiple users**

```http
PUT /restapi/v2/users/inactive HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["contractor1@example.com","contractor2@example.com"]}
```

**Case 3 — Deactivate a user in a specific Client Portal domain**

Temporarily suspends a portal user's access. Their portal-specific shares and permissions are preserved and restored upon reactivation.

```http
PUT /restapi/v2/users/inactive HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["suspended.portal.user@client.com"],"domainName":"reports.clientbrand.com"}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Deactivate Users](../../../sdk-examples/users-and-groups/org-users/de-activate-users.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Deactivate Users returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Organisation not found. | Verify the `ZANALYTICS-ORGID` header value. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not an Account Admin or Organization Admin of the organisation. | Ensure the caller has the required role. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | The specified `domainName` does not exist. | Provide a valid client portal domain name configured for the org. |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | The specified `domainName` does not belong to the calling user or the org's Account Admin. | Use a domain name administered by the Account Admin of this organisation. |
| [8114](../../../foundations/error-codes.md#error-8114) | 400 | One or more specified email addresses are not members of this organisation. | Verify all email IDs using Get Users before calling this API. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.usermanagement.update`. |

# Related

- [Organization Users overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Users](get-users.md), [Add Users](add-users.md), [Remove Users](remove-users.md), [Activate Users](activate-users.md), [Change User Role](change-user-role.md), [Get Org Admins](get-org-admins.md).
- [SDK examples](../../../sdk-examples/users-and-groups/org-users/de-activate-users.md).
