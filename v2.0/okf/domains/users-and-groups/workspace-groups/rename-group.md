---
type: API Endpoint
title: Rename Group
description: Updates the name and/or description of an existing group in the specified workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/groups/{group-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - workspace-groups
  - put
  - share
api:
  operation_id: renameGroup
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/groups/{group-id}"
  domain: users-and-groups
  group: workspace-groups
  oauth_scopes:
    - ZohoAnalytics.share.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access.
  error_codes:
    - 7103
    - 7282
    - 7301
    - 7338
    - 8535
  openapi:
    file: "/references/openapi/user-groups-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1groups~1{group-id}/put"
    config_schema: RenameGroupConfig
    response_schema: null
  sdk_examples: "/sdk-examples/users-and-groups/workspace-groups/rename-group.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/user-groups-grouped-api.json"
    title: OpenAPI 3 specification - user-groups-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**PUT `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}`** - Rename Group (Workspace Groups / Users & Groups).

Updates the name and/or description of an existing group in the specified workspace. Both fields are replaced atomically — if `groupDesc` is omitted, the description is reset to an empty string.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `renameGroup` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.share.update`](../../../foundations/oauth-scopes.md#zohoanalyticsshareupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`user-groups-grouped-api.json`](../../../references/openapi/user-groups-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1groups~1{group-id}/put`; CONFIG schema `RenameGroupConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.share.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{group-id}` | string | ID of the group. | [How to obtain](../../../foundations/identifiers.md#group-id) |

## CONFIG Parameter

CONFIG is **mandatory**. It must be sent as a form-encoded body parameter named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `groupName` | String | **Yes** | — | New display name for the group. Must be unique within the workspace. Cannot be empty or blank. |
| `groupDesc` | String | No | `""` | New description for the group. Max 200 characters. When omitted, the description is reset to an empty string — the previous description is **not** preserved. Always pass the existing description if you only intend to update the name. |

## Notes from the OpenAPI specification

- The calling user must be a Workspace Admin of the workspace. Account Admins and Organization Admins also have access.
- The new group name must be unique within the workspace. A name already used by another group fails with error code **7282**.
- Renaming a group to the name it already holds succeeds silently.
- When **groupDesc** is not provided, the existing description of the group is permanently overwritten with an empty string. It is not preserved. Read the current description using the Get Group Details API and pass it back if only the name has to be changed.
- The group-id in the request URI must belong to the workspace in the request URI. A group from another workspace fails with error code **7338**.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Rename a group (description not provided → reset to empty)**

```http
PUT /restapi/v2/workspaces/466206000000071000/groups/320862000000276835 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"groupName":"Finance & Accounts Team"}
```

**Case 2 — Rename and update description simultaneously**

```http
PUT /restapi/v2/workspaces/466206000000071000/groups/320862000000276835 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"groupName":"Finance & Accounts Team","groupDesc":"Finance, accounts payable, and treasury users"}
```

**Case 3 — Update only description (keep existing name, pass it explicitly)**

```http
PUT /restapi/v2/workspaces/466206000000071000/groups/320862000000276835 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"groupName":"Finance Team","groupDesc":"Updated: Finance and procurement access group"}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Rename Group](../../../sdk-examples/users-and-groups/workspace-groups/rename-group.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Rename Group returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **`groupDesc` is RESET on omission** | If `groupDesc` is not included in the request, the group's existing description is permanently overwritten with an empty string. Always include the current `groupDesc` value (read from Get Group Details) to preserve it. |
| **Renaming to the same name** | Succeeds without error (idempotent for the name). |
| **Dependency** | `<group-id>` in the URL must be obtained from Get Group List. The current `groupDesc` should also be read from Get Group Details before calling this API if you want to preserve the description. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7282](../../../foundations/error-codes.md#error-7282) | 400 | The new group name is already used by another group in this workspace. | Choose a name not already in use. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not a Workspace Admin, Account Admin, or Organization Admin of the workspace. | Ensure the caller has at least Workspace Admin access. |
| [7338](../../../foundations/error-codes.md#error-7338) | 400 | The specified `<group-id>` does not belong to this workspace. | Verify the group ID belongs to the correct workspace using Get Group List. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.share.update`. |

# Related

- [Workspace Groups overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Users & Groups](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Group List](get-groups.md), [Create Group](create-group.md), [Add Group Members](add-group-members.md), [Remove Group Members](remove-group-members.md), [Delete Group](delete-group.md), [Get Group Details](get-group-details.md).
- [SDK examples](../../../sdk-examples/users-and-groups/workspace-groups/rename-group.md).
