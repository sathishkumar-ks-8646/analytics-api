---
type: API Endpoint
title: Add Favourite Workspace
description: Adds the specified workspace to the list of favourite workspaces of the requesting user.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/favorite"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-preferences
  - post
  - metadata
api:
  operation_id: addFavoriteWorkspace
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/favorite"
  domain: workspace-management
  group: workspace-preferences
  oauth_scopes:
    - ZohoAnalytics.metadata.update
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be a Workspace Admin, or a Shared User, or a Group Member of the workspace, or any user with at least Read permission on a view within the workspace."
  error_codes:
    - 7103
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1favorite/post"
    config_schema: null
    response_schema: null
  sdk_examples: "/sdk-examples/workspace-management/workspace-preferences/add-favorite-workspace.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/favorite`** - Add Favourite Workspace (Workspace Preferences / Workspace Management).

Adds the specified workspace to the calling user's list of favourite workspaces. Favourited workspaces are typically surfaced at the top of workspace listings for quick navigation.

A user can favourite multiple workspaces simultaneously — there is no exclusivity constraint. If the workspace is already in the user's favourites, this call succeeds silently without error (idempotent).

> This API has no CONFIG parameter and no request body.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `addFavoriteWorkspace` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/favorite` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin, or a Shared User, or a Group Member of the workspace, or any user with at least Read permission on a view within the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 204 with no body |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1favorite/post` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | The ID of the workspace. It can be obtained using any of the workspace list APIs. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- Add Favourite Workspace returns a bare HTTP 204 No Content on success. There is no response body and no **status** or **summary** JSON to parse, so check only the HTTP status code. A JSON payload is returned only on failure.
- This API is idempotent. When the workspace is already present in the favourites of the user, the request succeeds without error and no duplicate entry is created.
- There is no limit on the number of workspaces a user can mark as favourite. Unlike the default workspace, the favourite preference carries no exclusivity constraint.
- The requesting user should have at least one view of the workspace shared with them. Access is checked at the workspace level and no permission beyond basic read access is required. A user with no access fails with error code 7301.
- The favourite preference is not exposed as a distinct field in the response of the standard workspace list APIs.
- The preferences are stored per user and per organization. Adding a workspace to the favourites of one user has no effect on the preferences of any other user.
- Client Portal users and standard Zoho Analytics users maintain separate preference stores, even when they access the same workspace. A Client Portal user should access the workspace through the portal domain in which it is shared with them, failing which the access check fails with error code 7301.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Add a workspace to favourites (Workspace Admin)**

```http
POST /restapi/v2/workspaces/466206000000071000/favorite HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Shared user favouriting a workspace they have view access in**

```http
POST /restapi/v2/workspaces/466206000000071000/favorite HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — Client Portal user favouriting their portal workspace**

```http
POST /restapi/v2/workspaces/38190000004180410/favorite HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 57058019
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Add Favourite Workspace](../../../sdk-examples/workspace-management/workspace-preferences/add-favorite-workspace.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Add Favourite Workspace returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Idempotent** | If the workspace is already in the user's favourites, calling this API again succeeds without error and makes no change. |
| **Multiple favourites allowed** | There is no limit on the number of workspaces a user can mark as favourite. |
| **Access requirement** | The user must have at least one view shared with them in the workspace. Without access, the call fails with error 7301. |
| **No CONFIG or request body** | The workspace is identified solely by `<workspace-id>` in the URL. |
| **Dependency** | `<workspace-id>` → Get All Workspace List or Get Shared Workspace List. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The user has no access to the specified workspace. | Ensure the user is a workspace member or has at least one view shared with them before adding it to favourites. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.update`. |

# Related

- [Workspace Preferences overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Add Default Workspace](add-default-workspace.md), [Remove Default Workspace](remove-default-workspace.md), [Remove Favourite Workspace](remove-favorite-workspace.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-preferences/add-favorite-workspace.md).
