---
type: API Endpoint
title: Add Favourite View
description: Marks the specified view as a favorite for the authenticated user.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/favorite"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - view-preferences
  - post
  - metadata
api:
  operation_id: addFavoriteView
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/favorite"
  domain: views-management
  group: view-preferences
  oauth_scopes:
    - ZohoAnalytics.metadata.update
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must have at least Read Only permission on the view. This includes Account Admins, Organization Admins, Workspace Admins, View Owners, and any user explicitly granted Read Only or higher access to the view."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 7319
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1favorite/post"
    config_schema: null
    response_schema: null
  sdk_examples: "/sdk-examples/views-management/view-preferences/add-favorite-view.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/favorite`** - Add Favourite View (View Preferences / Views Management).

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

From the OpenAPI specification:

Marks the specified view as a favorite for the authenticated user.

The favorite status is a per-user preference - marking a view as a favorite does not change what any other user sees. Once the view is marked, the `isFavorite` field returned by the listing APIs such as Get All Dashboards and Get Shared Dashboards reads `true` for the same user.

The call is idempotent. Marking a view that the user has already marked as a favorite succeeds silently without raising an error.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `addFavoriteView` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/favorite` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataupdate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must have at least Read Only permission on the view. This includes Account Admins, Organization Admins, Workspace Admins, View Owners, and any user explicitly granted Read Only or higher access to the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 204 with no body |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1favorite/post` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- The favorite status is stored per user. Marking or unmarking a view has no effect on any other user's preferences.
- The authenticated user must have at least Read Only permission on the view. Account Admins, Organization Admins, Workspace Admins and view owners qualify by default.
- Any view type the user can access can be marked as a favorite - Tables, Analysis Views, Pivot Tables, Summary Views, Query Tables and Dashboards.
- This API has no CONFIG parameter. The only inputs are the **workspace-id** and **view-id** path parameters, so no Content-Type header is required.
- The API is idempotent and returns HTTP 204 No Content with an empty body on success.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

# Examples

## Sample Requests

**Case 1 — Mark a chart view as favourite**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000105001/favorite HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Mark a dashboard as favourite**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000106002/favorite HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 204 No Content** — No response body is returned on success.

```
HTTP/1.1 204 No Content
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Add Favourite View](../../../sdk-examples/views-management/view-preferences/add-favorite-view.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

- Adds the specified view to the **favourites list of the authenticated user**.
- Has no effect on other users' favourite preferences.
- If the view is already marked as a favourite by this user, the call succeeds silently (idempotent — no error is raised).
- The resulting `isFavorite: true` value is reflected in listing API responses (e.g., Get All Dashboards, Get Shared Dashboards) for the same user.

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify the `<workspace-id>` in the URL is correct and accessible. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | View not found. | Verify the `<view-id>` exists in the specified workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission to mark this view as a favourite. | Ensure the user has at least Read Only permission on the view. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The specified view does not belong to the specified workspace. | Ensure both `<workspace-id>` and `<view-id>` are consistent and correct. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid OAuth token. | Provide a valid, non-expired token with scope `ZohoAnalytics.metadata.update`. |

# Related

- [View Preferences overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Remove Favourite View](remove-favorite-view.md).
- [SDK examples](../../../sdk-examples/views-management/view-preferences/add-favorite-view.md).
