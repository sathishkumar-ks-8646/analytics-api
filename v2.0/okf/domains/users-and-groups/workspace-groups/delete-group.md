---
type: API Endpoint
title: Delete Group
description: Permanently deletes a group from the workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/groups/{group-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - workspace-groups
  - delete
  - share
api:
  operation_id: deleteGroup
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/groups/{group-id}"
  domain: users-and-groups
  group: workspace-groups
  oauth_scopes:
    - ZohoAnalytics.share.delete
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 204
  response_content_types: []
  permission_required: The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access.
  error_codes:
    - 7103
    - 7301
    - 7338
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1groups~1{group-id}/delete"
    config_schema: null
    response_schema: null
  sdk_examples: "/sdk-examples/users-and-groups/workspace-groups/delete-group.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}`** - Delete Group (Workspace Groups / Users & Groups).

Permanently deletes a group from the workspace. This operation is irreversible. All view-level access grants that were based on this group's membership are immediately revoked for all former members (unless those members have access through other means — direct sharing, other groups, or workspace-level roles).

> **Confirmed account requirement:** The calling user's Zoho account must be confirmed (email-verified) to invoke this API.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deleteGroup` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.share.delete`](../../../foundations/oauth-scopes.md#zohoanalyticssharedelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 204 with no body |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1groups~1{group-id}/delete` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.share.delete`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{group-id}` | string | ID of the group. | [How to obtain](../../../foundations/identifiers.md#group-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- The Zoho account of the calling user must be confirmed (email verified) to invoke this API.
- The calling user must be a Workspace Admin of the workspace. Account Admins and Organization Admins also have access.
- This operation is irreversible. There is no soft-delete or trash mechanism for groups - once deleted, the group and its sharing configuration cannot be restored.
- A group holding active members is deleted regardless. Every view share that references the group is also removed, and all the members lose their group-based access simultaneously.
- Users who hold access to the same views through a direct share, through another group, or through a workspace-level role are unaffected.
- The group-id in the request URI must belong to the workspace in the request URI. A group from another workspace fails with error code **7338**.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Delete a group**

```http
DELETE /restapi/v2/workspaces/466206000000071000/groups/320862000000276835 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Client Portal Admin deleting a portal-domain group**

```http
DELETE /restapi/v2/workspaces/466206000000071000/groups/38190000004182920 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Delete Group](../../../sdk-examples/users-and-groups/workspace-groups/delete-group.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Delete Group returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Cascading view access revocation** | When a group is deleted, all view shares granted exclusively via that group are revoked for every affected member simultaneously. Users with direct sharing or membership in other groups sharing the same views are unaffected. |
| **No CONFIG parameter** | The group is identified solely by `<group-id>` in the URL. No request body is needed. |
| **Permanent deletion** | There is no soft-delete or trash mechanism. Once deleted, the group and its sharing configuration cannot be restored. |
| **Dependency** | `<group-id>` → Get Group List. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not a Workspace Admin, Account Admin, or Organization Admin of the workspace. | Ensure the caller has at least Workspace Admin access. |
| [7338](../../../foundations/error-codes.md#error-7338) | 400 | The specified `<group-id>` does not belong to this workspace. | Verify the group ID using Get Group List. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.share.delete`. |

# Related

- [Workspace Groups overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Group List](get-groups.md), [Create Group](create-group.md), [Rename Group](rename-group.md), [Add Group Members](add-group-members.md), [Remove Group Members](remove-group-members.md), [Get Group Details](get-group-details.md).
- [SDK examples](../../../sdk-examples/users-and-groups/workspace-groups/delete-group.md).
