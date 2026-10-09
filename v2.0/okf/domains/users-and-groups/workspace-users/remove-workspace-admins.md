---
type: API Endpoint
title: Remove Workspace Admins
description: Revokes the Workspace Admin role from one or more users in the specified workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/admins"
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - workspace-users
  - delete
  - share
api:
  operation_id: removeWorkspaceAdmins
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/admins"
  domain: users-and-groups
  group: workspace-users
  oauth_scopes:
    - ZohoAnalytics.share.delete
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace.
  error_codes:
    - 7103
    - 7301
    - 8040
    - 8060
    - 8061
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1admins/delete"
    config_schema: RemoveWorkspaceAdminConfig
    response_schema: null
  sdk_examples: "/sdk-examples/users-and-groups/workspace-users/remove-workspace-admins.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}/admins`** - Remove Workspace Admins (Workspace Users / Users & Groups).

Revokes the Workspace Admin role from one or more users in the specified workspace. All specified email addresses must currently hold Workspace Admin status in the workspace — a user who is not a Workspace Admin causes the entire request to fail with error **8040**.

> **Confirmed account requirement:** The calling user's Zoho account must be confirmed (email-verified) to invoke this API.

From the OpenAPI specification:

Revokes the Workspace Admin role from one or more users in the specified workspace. The users remain in the workspace as regular users and retain their existing view-level access.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `removeWorkspaceAdmins` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/admins` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.share.delete`](../../../foundations/oauth-scopes.md#zohoanalyticssharedelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1admins/delete`; CONFIG schema `RemoveWorkspaceAdminConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.share.delete`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameter

CONFIG is **mandatory**. It must be sent as a form-encoded body parameter named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `emailIds` | Array of Strings | **Yes** | — | Email addresses of Workspace Admins to demote. Max 1000 entries. Every email in the list must currently be a Workspace Admin of this workspace; a non-admin email causes the entire request to fail. |
| `domainName` | String | No | `null` | Client portal domain for portal-scoped demotion. When provided, removes admin status for users in the specified portal domain. When omitted, applies to the standard org domain. |
| `notifyMail` | Boolean | No | `false` | When `false` (default): no email is sent to the removed admins. When `true`: a notification email is sent to each removed admin informing them that their Workspace Admin access has been revoked. |

## Notes from the OpenAPI specification

- The Zoho account of the calling user must be confirmed (email verified) to invoke this API.
- The calling user must be an Account Admin or an Organization Admin of the organization that owns the workspace.
- A maximum of 1000 email addresses can be sent in a single request.
- Every email address in the request must currently hold the Workspace Admin role in this workspace. A non-admin email address causes the entire batch to fail with error code **8040**, and no demotion is applied. Verify the current admin membership using the Get Workspace Admins API before invoking this API.
- This API only demotes. To remove a user from the workspace entirely, use the Remove Workspace Users API instead.
- Removing the last Workspace Admin is allowed. The workspace is then managed only by the Account Admin and the Organization Admins.
- A failure in delivering the notification email does not roll back the demotion. The demotion is committed even when **notifyMail** is set to true and the email cannot be delivered.
- Always specify **domainName** when demoting portal users, so that the operation is scoped to their portal.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Demote a Workspace Admin silently**

```http
DELETE /restapi/v2/workspaces/466206000000071000/admins HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["formeradmin@acme.com"]}
```

**Case 2 — Demote and send a notification email**

```http
DELETE /restapi/v2/workspaces/466206000000071000/admins HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["admin1@acme.com","admin2@acme.com"],"notifyMail":true}
```

**Case 3 — Client Portal: revoke Workspace Admin from a portal user**

```http
DELETE /restapi/v2/workspaces/466206000000071000/admins HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["portal.admin@client.com"],"domainName":"reports.clientbrand.com"}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Remove Workspace Admins](../../../sdk-examples/users-and-groups/workspace-users/remove-workspace-admins.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Remove Workspace Admins returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Demotes only — does not remove from workspace** | This API revokes the Workspace Admin role. The user remains in the workspace as a regular User with their existing view-level access. To completely remove a user from the workspace, use [Remove Workspace Users](delete-workspace-users.md) instead. |
| **Non-admin email causes entire batch to fail** | If any email in `emailIds` is not currently a Workspace Admin, error 8040 is returned and zero demotions are applied. Always verify current admin membership using Get Workspace Admins before calling. |
| **`notifyMail=true` does not block removal** | Email delivery failures do not roll back the demotion. |
| **Removing the last Workspace Admin** | Allowed. The workspace will have no Workspace Admins. Only Account Admin and Org Admin can then manage the workspace. |
| **Dependency** | Admin email addresses → Get Workspace Admins. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not an Account Admin or Organization Admin of the organisation. | Only Account Admins and Organization Admins can manage Workspace Admins. |
| [8040](../../../foundations/error-codes.md#error-8040) | 400 | One or more specified email addresses are not currently Workspace Admins in this workspace. | Verify all email addresses are current Workspace Admins using Get Workspace Admins before calling this API. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | The specified `domainName` does not exist. | Provide a valid client portal domain name. |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | The specified `domainName` does not belong to the org's Account Admin. | Use a domain administered by the Account Admin. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.share.delete`. |

# Related

- [Workspace Users overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Workspace Users](get-workspace-users.md), [Add Workspace Users](add-workspace-users.md), [Remove Workspace Users](delete-workspace-users.md), [Change Workspace Users Status](change-workspace-users-status.md), [Change Workspace Users Role](change-workspace-users-role.md), [Get Workspace Admins](get-workspace-admins.md), [Add Workspace Admins](add-workspace-admins.md).
- [SDK examples](../../../sdk-examples/users-and-groups/workspace-users/remove-workspace-admins.md).
