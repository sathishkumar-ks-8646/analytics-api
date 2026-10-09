---
type: API Endpoint
title: Add Workspace Admins
description: Grants the Workspace Admin role to one or more users in the specified workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/admins"
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - workspace-users
  - post
  - share
api:
  operation_id: addWorkspaceAdmins
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/admins"
  domain: users-and-groups
  group: workspace-users
  oauth_scopes:
    - ZohoAnalytics.share.create
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
    - 7390
    - 8060
    - 8061
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1admins/post"
    config_schema: AddWorkspaceAdminConfig
    response_schema: null
  sdk_examples: "/sdk-examples/users-and-groups/workspace-users/add-workspace-admins.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/admins`** - Add Workspace Admins (Workspace Users / Users & Groups).

Grants the Workspace Admin role to one or more users in the specified workspace. Users must already be members of the workspace (or the specified portal domain). Existing Workspace Admins in the `emailIds` list are silently skipped — no error is raised for duplicates.

> **Viewer restriction:** Users who hold the org-level Viewer role cannot be promoted to Workspace Admin. Attempting to add a Viewer as a Workspace Admin fails with error **7390**.

> **Confirmed account requirement:** The calling user's Zoho account must be confirmed (email-verified) to invoke this API.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `addWorkspaceAdmins` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/admins` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.share.create`](../../../foundations/oauth-scopes.md#zohoanalyticssharecreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organisation that owns the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1admins/post`; CONFIG schema `AddWorkspaceAdminConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.share.create`. See [Authentication](../../../foundations/authentication.md). |
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
| `emailIds` | Array of Strings | **Yes** | — | Email addresses to promote to Workspace Admin. Max 1000 entries. Existing admins in the list are silently skipped without error. |
| `domainName` | String | No | `null` | Client portal domain for portal-scoped promotion. When provided, grants Workspace Admin status for users in the specified portal domain. When omitted, applies to the standard org domain. |
| `inviteMail` | Boolean | No | `false` | When `false` (default): no email is sent to the newly added Workspace Admins. When `true`: an invitation/notification email is sent to each newly added admin informing them of their new access. |

## Notes from the OpenAPI specification

- The Zoho account of the calling user must be confirmed (email verified) to invoke this API.
- The calling user must be an Account Admin or an Organization Admin of the organization that owns the workspace.
- A maximum of 1000 email addresses can be sent in a single request.
- The users must already have been added to the workspace using the Add Workspace Users API before they can be promoted to Workspace Admin.
- Email addresses that already hold the Workspace Admin role are skipped silently, and no error is raised for such duplicates. Only genuinely new admins receive a notification email when **inviteMail** is set to true.
- Users who hold the org-level Viewer role cannot be promoted to Workspace Admin. If any email address in the request belongs to a Viewer, the entire batch fails with error code **7390**. Change their org-level role to **USER** using the Change User Role API first.
- A failure in delivering the notification email does not roll back the promotion. The promotion is committed even when **inviteMail** is set to true and the email cannot be delivered.
- Always specify **domainName** when promoting portal users, so that the operation is scoped to their portal.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Promote a user to Workspace Admin without sending an invitation email**

```http
POST /restapi/v2/workspaces/466206000000071000/admins HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["newadmin@acme.com"]}
```

**Case 2 — Promote multiple users and send invitation emails**

```http
POST /restapi/v2/workspaces/466206000000071000/admins HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["admin1@acme.com","admin2@acme.com"],"inviteMail":true}
```

**Case 3 — Client Portal: promote a portal user to Workspace Admin in their portal domain**

```http
POST /restapi/v2/workspaces/466206000000071000/admins HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"emailIds":["portal.admin@client.com"],"domainName":"reports.clientbrand.com","inviteMail":true}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Add Workspace Admins](../../../sdk-examples/users-and-groups/workspace-users/add-workspace-admins.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Add Workspace Admins returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **User must already be in the workspace** | The user must have been added to the workspace (via Add Workspace Users) before they can be promoted to Workspace Admin. |
| **Viewer-role users cannot be promoted** | If any email in the batch belongs to an org-level Viewer, the entire batch fails with error 7390. Change their org role to User first via the org-level role management API. |
| **Adding an existing admin is silently skipped** | Duplicate additions do not raise an error. Only genuinely new admins receive an invitation email when `inviteMail=true`. |
| **`inviteMail=true` does not block the promotion** | Email delivery failures do not roll back the admin promotion. |
| **Dependency** | User email addresses → Get Workspace Users (to confirm users are already in the workspace). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not an Account Admin or Organization Admin of the organisation. | Only Account Admins and Organization Admins can manage Workspace Admins. |
| [7390](../../../foundations/error-codes.md#error-7390) | 400 | One or more of the specified users holds the org-level Viewer role and cannot be promoted to Workspace Admin. | Viewers cannot be Workspace Admins. Change their org-level role to `"USER"` first via the Change User Role API. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | The specified `domainName` does not exist. | Provide a valid client portal domain name. |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | The specified `domainName` does not belong to the org's Account Admin. | Use a domain administered by the Account Admin. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.share.create`. |

# Related

- [Workspace Users overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Workspace Users](get-workspace-users.md), [Add Workspace Users](add-workspace-users.md), [Remove Workspace Users](delete-workspace-users.md), [Change Workspace Users Status](change-workspace-users-status.md), [Change Workspace Users Role](change-workspace-users-role.md), [Get Workspace Admins](get-workspace-admins.md), [Remove Workspace Admins](remove-workspace-admins.md).
- [SDK examples](../../../sdk-examples/users-and-groups/workspace-users/add-workspace-admins.md).
