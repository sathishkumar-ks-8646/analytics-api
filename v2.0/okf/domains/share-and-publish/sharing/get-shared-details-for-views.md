---
type: API Endpoint
title: Get Shared Details
description: Returns the shared details of the specified views.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/share/shareddetails"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - sharing
  - get
  - share
api:
  operation_id: getSharedDetailsForViews
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/share/shareddetails"
  domain: share-and-publish
  group: sharing
  oauth_scopes:
    - ZohoAnalytics.share.read
  org_id_header: required
  config_parameter:
    location: query
    required: true
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Share permission on all of the specified viewIds."
  error_codes:
    - 7301
    - 8080
  openapi:
    file: "/references/openapi/share-publish-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1share~1shareddetails/get"
    config_schema: GetSharedDetailsConfig
    response_schema: GetSharedDetailsResponse
  sdk_examples: "/sdk-examples/share-and-publish/sharing/get-shared-details-for-views.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/share-publish-grouped-api.json"
    title: OpenAPI 3 specification - share-publish-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/share/shareddetails`** - Get Shared Details (Sharing / Share & Publish).

Returns detailed share information — per user and per group, including permission booleans, a human-readable `permissionString`, filter criteria, and restricted columns — for one or more specific views.

From the OpenAPI specification:

Returns the shared details of the specified views. For every view, the response lists each user or group it is shared to, along with the permissions granted, the filter criteria applied, and any column level restrictions in effect.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getSharedDetailsForViews` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/share/shareddetails` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.share.read`](../../../foundations/oauth-scopes.md#zohoanalyticsshareread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Share permission on all of the specified viewIds. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - **mandatory** |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1share~1shareddetails/get`; CONFIG schema `GetSharedDetailsConfig`; response schema `GetSharedDetailsResponse` |

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

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `viewIds` | JSONArray of String/Long | **Yes** | — | IDs of the views whose share details are to be fetched (1–1000 entries). |

## Notes from the OpenAPI specification

- As this is a GET request, the CONFIG value must be stringified and URL encoded before it is sent.
- When `viewIds` is omitted, no view is selected and the shared details are not returned.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `sharedDetails` | JSONArray | One entry per requested `viewId`. |
| `sharedDetails[].viewId` | String | The view ID this entry describes. |
| `sharedDetails[].shareInfo` | JSONArray | One entry per user/group the view is shared with. |
| `shareInfo[].sharedTo` | String | Email address (for a user share) or group name (for a group share). |
| `shareInfo[].sharedBy` | String | Email address of the user who created/last modified this share. |
| `shareInfo[].sharedToZuId` | String | Zoho user ID of the recipient. Present only for user shares (`isGroupShare: false`); a value of `-10` indicates a portal/embedded user account. |
| `shareInfo[].sharedToGroupId` | String | Group ID of the recipient. Present only for group shares (`isGroupShare: true`). |
| `shareInfo[].permissionString` | String | Human-readable, comma-separated summary of the granted permissions — useful for display in UI without re-deriving it from the `permissions` booleans. |
| `shareInfo[].permissions` | JSONObject | Full permission set. See [`permissions` Fields](share-views.md#permissions-fields). |
| `shareInfo[].criteria` | String | Row-level filter criteria applied for this share, if any. Empty string if none. |
| `shareInfo[].inheritParentFilterCriteria` | String (`"true"`/`"false"`) | Whether the shared user also inherits the sharer's own filter on the view. |
| `shareInfo[].isInvalidCriteria` | Boolean | `true` if the stored `criteria` expression is no longer valid (e.g., references a column that was deleted). |
| `shareInfo[].sharedColumns` | JSONArray | Column restrictions applied to this share, if any (empty if the shared user can see all columns). |
| `shareInfo[].vudColumns` | JSONArray | Column restrictions for "View Underlying Data" mode, if any. |
| `shareInfo[].drillColumns` | JSONArray | Column restrictions for drill-down, if any. |
| `shareInfo[].isGroupShare` | Boolean | `true` if this entry represents a share to a group rather than an individual user. |
| `shareInfo[].publicPermLevel` | Integer | Internal public-share permission level indicator; `0` for regular (non-public) shares. |
| `shareInfo[].isROUser` | Boolean | `true` if the recipient is a Read-Only (embedded/Client Portal) user. |

# Examples

## Sample Requests

**Case 1 — Get shared details for a single view**

```http
GET /restapi/v2/workspaces/137687000271334001/share/shareddetails?CONFIG={"viewIds":["320862000001361755"]} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Get shared details for multiple views (Client Portal)**

```http
GET /restapi/v2/workspaces/137687000271334009/share/shareddetails?CONFIG={"viewIds":["320862000001361757","320862000001361759"]} HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK — Single view, shared to a user and a group**

```json
{
    "status": "success",
    "summary": "Get shared details for view",
    "data": {
        "sharedDetails": [
            {
                "viewId": "320862000001361755",
                "shareInfo": [
                    {
                        "sharedTo": "restapi_v2_shareduser@zohotest.com",
                        "sharedBy": "workspaceowner@zohotest.com",
                        "sharedToZuId": "64036387",
                        "permissionString": "Read Access, Export Data, Only Append Rows, Add or Update Rows, Share Views / Child Reports",
                        "permissions": {
                            "read": true,
                            "export": true,
                            "vud": false,
                            "addRow": false,
                            "updateRow": false,
                            "deleteRow": false,
                            "deleteAllRows": false,
                            "importAppend": true,
                            "importAddOrUpdate": true,
                            "importDeleteAllAdd": false,
                            "importDeleteUpdateAdd": false,
                            "share": true,
                            "drillDown": false,
                            "discussion": false,
                            "insight": false,
                            "accessAdminPresets": false,
                            "createPreset": false,
                            "drillThrough": false,
                            "drillActions": false
                        },
                        "criteria": "\"Region\"='East'",
                        "inheritParentFilterCriteria": "false",
                        "isInvalidCriteria": false,
                        "sharedColumns": [],
                        "vudColumns": [],
                        "drillColumns": [],
                        "isGroupShare": false,
                        "publicPermLevel": 0,
                        "isROUser": false
                    },
                    {
                        "sharedTo": "Group-1",
                        "sharedBy": "workspaceowner@zohotest.com",
                        "sharedToGroupId": "320862000001360842",
                        "permissionString": "Read Access, Export Data, Only Append Rows, Add or Update Rows, Share Views / Child Reports",
                        "permissions": {
                            "read": true,
                            "export": true,
                            "vud": false,
                            "addRow": false,
                            "updateRow": false,
                            "deleteRow": false,
                            "deleteAllRows": false,
                            "importAppend": true,
                            "importAddOrUpdate": true,
                            "importDeleteAllAdd": false,
                            "importDeleteUpdateAdd": false,
                            "share": true,
                            "drillDown": false,
                            "discussion": false,
                            "insight": false,
                            "accessAdminPresets": false,
                            "createPreset": false,
                            "drillThrough": false,
                            "drillActions": false
                        },
                        "criteria": "",
                        "inheritParentFilterCriteria": "false",
                        "isInvalidCriteria": false,
                        "sharedColumns": [],
                        "vudColumns": [],
                        "drillColumns": [],
                        "isGroupShare": true,
                        "publicPermLevel": 0,
                        "isROUser": false
                    }
                ]
            }
        ]
    }
}
```

**HTTP 200 OK — Multiple views requested in one call**

```json
{
    "status": "success",
    "summary": "Get shared details for view",
    "data": {
        "sharedDetails": [
            {
                "viewId": "320862000001361757",
                "shareInfo": [
                    {
                        "sharedTo": "restapi_v2_shareduser@zohotest.com",
                        "sharedBy": "workspaceowner@zohotest.com",
                        "sharedToZuId": "64036387",
                        "permissionString": "Read Access, Export Data, Only Append Rows, Add or Update Rows",
                        "permissions": {
                            "read": true,
                            "export": true,
                            "vud": false,
                            "addRow": false,
                            "updateRow": false,
                            "deleteRow": false,
                            "deleteAllRows": false,
                            "importAppend": true,
                            "importAddOrUpdate": true,
                            "importDeleteAllAdd": false,
                            "importDeleteUpdateAdd": false,
                            "share": false,
                            "drillDown": false,
                            "discussion": false,
                            "insight": false,
                            "accessAdminPresets": false,
                            "createPreset": false,
                            "drillThrough": false,
                            "drillActions": false
                        },
                        "criteria": "",
                        "inheritParentFilterCriteria": "false",
                        "isInvalidCriteria": false,
                        "sharedColumns": [],
                        "vudColumns": [],
                        "drillColumns": [],
                        "isGroupShare": false,
                        "publicPermLevel": 0,
                        "isROUser": false
                    }
                ]
            },
            {
                "viewId": "320862000001361759",
                "shareInfo": [
                    {
                        "sharedTo": "restapi_v2_shareduser@zohotest.com",
                        "sharedBy": "workspaceowner@zohotest.com",
                        "sharedToZuId": "64036387",
                        "permissionString": "Read Access, Export Data, Only Append Rows, Add or Update Rows",
                        "permissions": {
                            "read": true,
                            "export": true,
                            "vud": false,
                            "addRow": false,
                            "updateRow": false,
                            "deleteRow": false,
                            "deleteAllRows": false,
                            "importAppend": true,
                            "importAddOrUpdate": true,
                            "importDeleteAllAdd": false,
                            "importDeleteUpdateAdd": false,
                            "share": false,
                            "drillDown": false,
                            "discussion": false,
                            "insight": false,
                            "accessAdminPresets": false,
                            "createPreset": false,
                            "drillThrough": false,
                            "drillActions": false
                        },
                        "criteria": "",
                        "inheritParentFilterCriteria": "false",
                        "isInvalidCriteria": false,
                        "sharedColumns": [],
                        "vudColumns": [],
                        "drillColumns": [],
                        "isGroupShare": false,
                        "publicPermLevel": 0,
                        "isROUser": false
                    }
                ]
            }
        ]
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Shared Details](../../../sdk-examples/share-and-publish/sharing/get-shared-details-for-views.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **View-scoped, batched** | Unlike Get Workspace Shared Details, this API is scoped to the specific `viewIds` requested (not the whole workspace), and can fetch several views' share details in one call. |
| **Includes derived text** | `permissionString` is a ready-to-display summary — do not attempt to reconstruct it manually from the `permissions` booleans; use it directly if you only need to show the recipient a summary. |
| **`sharedToZuId` vs `sharedToGroupId`** | Only one of the two is present per `shareInfo` entry, depending on `isGroupShare`. |
| **Dependency** | [Get Views](../../views-management/view-operations/overview.md) → `viewIds` → Get Shared Details. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — User does not have Share permission on one or more requested `viewIds`. | Ensure the user is an Account Admin, Organization Admin, or Workspace Admin, or has Share permission on all requested views. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — `viewIds` missing or malformed. | Supply a valid, non-empty `viewIds` JSONArray. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Sharing overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Workspace Shared Details](get-workspace-shared-details.md), [Share Views](share-views.md), [Update Shared Details](update-shared-details-for-view.md), [Remove Shared Views](remove-share.md), [Get My Permissions](get-user-permissions.md).
- [SDK examples](../../../sdk-examples/share-and-publish/sharing/get-shared-details-for-views.md).
