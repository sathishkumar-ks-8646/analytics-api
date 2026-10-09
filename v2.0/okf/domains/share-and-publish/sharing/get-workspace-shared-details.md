---
type: API Endpoint
title: Get Workspace Shared Details
description: Returns the shared details of the specified workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/share"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - sharing
  - get
  - share
api:
  operation_id: getWorkspaceSharedDetails
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/share"
  domain: share-and-publish
  group: sharing
  oauth_scopes:
    - ZohoAnalytics.share.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. This API is restricted to workspace owners — there is no permission-based alternative."
  error_codes:
    - 7301
  openapi:
    file: "/references/openapi/share-publish-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1share/get"
    config_schema: null
    response_schema: GetWorkspaceSharedDetailsResponse
  sdk_examples: "/sdk-examples/share-and-publish/sharing/get-workspace-shared-details.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/share-publish-grouped-api.json"
    title: OpenAPI 3 specification - share-publish-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/share`** - Get Workspace Shared Details (Sharing / Share & Publish).

Returns a consolidated view of every share that exists in the workspace — grouped by user, by group, plus any public/private-link shares — in a single call. Intended for workspace-level share auditing/administration.

> This API has no CONFIG parameter.

From the OpenAPI specification:

Returns the shared details of the specified workspace. The response groups the sharing into four blocks - views shared directly with individual users, views shared with groups, views published publicly, and views shared through a private link.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getWorkspaceSharedDetails` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/share` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.share.read`](../../../foundations/oauth-scopes.md#zohoanalyticsshareread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. This API is restricted to workspace owners — there is no permission-based alternative. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1share/get`; response schema `GetWorkspaceSharedDetailsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.share.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `userShareInfo` | JSONArray | One entry per user the workspace's views are shared with. Each entry has `emailId`, `views[]` (each with `viewId`, `viewName`, `sharedBy`, `permissions`). Empty if no views are shared to individual users. |
| `groupShareInfo` | JSONArray | One entry per group the workspace's views are shared with. Each entry has `groupId`, `groupName`, `groupDesc`, `groupMembers[]` (member email addresses), and `views[]` (same shape as in `userShareInfo`). Empty if no views are shared to groups. |
| `publicShareInfo` | JSONObject | Public/anyone-with-link share configuration for the workspace's views, if any. Empty object `{}` if no view is publicly shared. |
| `privateLinkShareInfo` | JSONObject | Private-link ("share via secret URL") share configuration, if any. Empty object `{}` if none configured. |
| `views[].permissions` | JSONObject | The permission set granted for that specific view. See [`permissions` Fields](share-views.md#permissions-fields) — note that `vudSelectedColumns`, `drillThrough`, `drillActions`, `accessAdminPresets`, and `createPreset` are omitted from this particular response and only appear in Get Shared Details / Get My Permissions responses. |

## Notes from the OpenAPI specification

- `publicShareInfo` and `privateLinkShareInfo` are always returned, with an empty `views` array when nothing is published publicly or through a private link.
- The `emailId` returned inside `publicShareInfo` and `privateLinkShareInfo` is a fixed placeholder, not a real user.

# Examples

## Sample Requests

**Case 1 — Standard workspace**

```http
GET /restapi/v2/workspaces/137687000271334001/share HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Client Portal / White Label workspace**

```http
GET /restapi/v2/workspaces/137687000271334009/share HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK — No shares exist yet**

```json
{
    "status": "success",
    "summary": "Get share info",
    "data": {
        "userShareInfo": [],
        "groupShareInfo": [],
        "publicShareInfo": {},
        "privateLinkShareInfo": {}
    }
}
```

**HTTP 200 OK — Workspace with a group share (Client Portal / White Label)**

```json
{
    "status": "success",
    "summary": "Get share info",
    "data": {
        "userShareInfo": [],
        "groupShareInfo": [
            {
                "groupId": "38190000004189049",
                "groupName": "Group",
                "groupDesc": "",
                "groupMembers": ["melba.s+wl_groupuser1t0@zohotest.com"],
                "views": [
                    {
                        "viewId": "38190000004178369",
                        "viewName": "ChartWL1",
                        "sharedBy": "melba.s+wldbadmint0@zohotest.com",
                        "permissions": {
                            "read": true,
                            "export": true,
                            "vud": true,
                            "addRow": false,
                            "updateRow": false,
                            "deleteRow": false,
                            "deleteAllRows": false,
                            "importAppend": false,
                            "importAddOrUpdate": false,
                            "importDeleteAllAdd": false,
                            "importDeleteUpdateAdd": false,
                            "drillDown": true,
                            "share": false,
                            "discussion": false,
                            "insight": false
                        }
                    },
                    {
                        "viewId": "38190000004178370",
                        "viewName": "PivotWL1",
                        "sharedBy": "melba.s+wldbadmint0@zohotest.com",
                        "permissions": {
                            "read": true,
                            "export": true,
                            "vud": false,
                            "addRow": true,
                            "updateRow": true,
                            "deleteRow": true,
                            "deleteAllRows": true,
                            "importAppend": true,
                            "importAddOrUpdate": true,
                            "importDeleteAllAdd": true,
                            "importDeleteUpdateAdd": true,
                            "drillDown": false,
                            "share": true,
                            "discussion": true,
                            "insight": false
                        }
                    }
                ]
            }
        ],
        "publicShareInfo": {},
        "privateLinkShareInfo": {}
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Workspace Shared Details](../../../sdk-examples/share-and-publish/sharing/get-workspace-shared-details.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Workspace-level, not view-level** | Unlike [Get Shared Details](get-shared-details-for-views.md), this API requires no `viewIds` — it returns share data for **every** shared view in the workspace in one response. |
| **Owner-only visibility** | Only the Workspace Admin (or Account/Organization Admin) can call this — a regular shared user cannot use it to see who else a view is shared with. |
| **Empty arrays/objects on no data** | Fields are always present in the response but are empty (`[]` or `{}`) rather than omitted when nothing of that share type exists. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — User does not have permission to view workspace share info. | Ensure the user is an Account Admin, Organization Admin, or Workspace Admin. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Sharing overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Share Views](share-views.md), [Update Shared Details](update-shared-details-for-view.md), [Get Shared Details](get-shared-details-for-views.md), [Remove Shared Views](remove-share.md), [Get My Permissions](get-user-permissions.md).
- [SDK examples](../../../sdk-examples/share-and-publish/sharing/get-workspace-shared-details.md).
