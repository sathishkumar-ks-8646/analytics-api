---
type: API Endpoint
title: Get Trash Views
description: "Returns the list of all views available in the trash of the specified workspace, along with the time each view was deleted and the user who deleted it."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/trash"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - trash-management
  - get
  - metadata
api:
  operation_id: getTrashViews
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/trash"
  domain: views-management
  group: trash-management
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or a Shared User, or a Group Member, or any user with Read permission on the workspace."
  error_codes:
    - 7103
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1trash/get"
    config_schema: null
    response_schema: GetTrashViewsResponse
  sdk_examples: "/sdk-examples/views-management/trash-management/get-trash-views.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/trash`** - Get Trash Views (Trash Management / Views Management).

> This API has no `CONFIG` parameter. All inputs are provided via URL path parameters.

From the OpenAPI specification:

Returns the list of all views available in the trash of the specified workspace, along with the time each view was deleted and the user who deleted it.

The scope of the list depends on the caller. Account Admins, Organization Admins and Workspace Admins receive every trashed view in the workspace, while shared users and group members receive only the views they owned before deletion.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getTrashViews` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/trash` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or a Shared User, or a Group Member, or any user with Read permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1trash/get`; response schema `GetTrashViewsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- This API has no CONFIG parameter. The only input is the **workspace-id** path parameter.
- Account Admins, Organization Admins and Workspace Admins see every trashed view in the workspace. Shared users and group members see only the views they owned before deletion.
- An empty **views** array is returned when the trash holds nothing visible to the calling user.
- **deletedTime** is an epoch timestamp in milliseconds returned as a string. Divide it by 1000 to obtain epoch seconds.
- **tabParentId**, **tabParentName** and **tabPosition** are returned only for views whose **viewType** is DashTab.
- **isDisabled** is returned only when it is true. It marks a view that cannot be restored under the current plan, typically a Live Connect report.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Always Present | Description |
|-------|------|----------------|-------------|
| `viewId` | String | Yes | ID of the trashed view, as a string. |
| `viewName` | String | Yes | Display name of the view at the time it was deleted. |
| `viewType` | String | Yes | Type of the view. See **View Type Values** below. |
| `deletedTime` | String | Yes | Epoch timestamp in **milliseconds** when the view was deleted. |
| `deletedBy` | String | Yes | Email address of the user who deleted the view. |
| `isDisabled` | Boolean | Only when `true` | Present and `true` when the view cannot be restored due to plan limitations (e.g., Live Connect views on a non-supporting plan). |
| `tabParentId` | String | Only for `DashTab` | ID of the parent tabbed dashboard this tab belongs to. |
| `tabParentName` | String | Only for `DashTab` | Display name of the parent tabbed dashboard. |
| `tabPosition` | Integer | Only for `DashTab` | Position index of this tab within the parent dashboard. |

**View Type Values:**

| `viewType` | Description |
|------------|-------------|
| `Table` | Data table (base table or imported data). |
| `AnalysisView` | Chart/analysis view (bar, line, pie, etc.). |
| `Pivot` | Pivot table view. |
| `Summary` | Summary view. |
| `QueryTable` | Query table / custom formula table. |
| `Dashboard` | Dashboard view. |
| `DashTab` | A tab within a tabbed dashboard. Includes `tabParentId`, `tabParentName`, `tabPosition`. |

# Examples

## Sample Requests

**Case 1 — List all trashed views in a workspace**

```http
GET /restapi/v2/workspaces/7617000032567001/trash HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Shared user calling the endpoint (returns only views they own)**

```http
GET /restapi/v2/workspaces/7617000032567001/trash HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**Case 1 — Empty trash (no trashed views)**

```json
{
  "status": "success",
  "summary": "get trash view list",
  "data": {
    "views": []
  }
}
```

**Case 2 — Single trashed table (Account Admin view)**

```json
{
  "status": "success",
  "summary": "get trash view list",
  "data": {
    "views": [
      {
        "viewId": "7617000032567618",
        "viewName": "T1_001",
        "viewType": "Table",
        "deletedTime": "1682432425367",
        "deletedBy": "admin@example.com"
      }
    ]
  }
}
```

**Case 3 — Multiple trashed views of different types**

```json
{
  "status": "success",
  "summary": "get trash view list",
  "data": {
    "views": [
      {
        "viewId": "7617000032567465",
        "viewName": "Sales",
        "viewType": "Table",
        "deletedTime": "1682432425829",
        "deletedBy": "admin@example.com"
      },
      {
        "viewId": "7617000032567466",
        "viewName": "Region_vs_sales",
        "viewType": "AnalysisView",
        "deletedTime": "1682432425829",
        "deletedBy": "admin@example.com"
      },
      {
        "viewId": "7617000032567467",
        "viewName": "product_Vs_sales",
        "viewType": "AnalysisView",
        "deletedTime": "1682432425829",
        "deletedBy": "admin@example.com"
      },
      {
        "viewId": "7617000032567597",
        "viewName": "ANV_014",
        "viewType": "Pivot",
        "deletedTime": "1682432426258",
        "deletedBy": "orgadmin@example.com"
      }
    ]
  }
}
```

**Case 4 — Shared user: returns empty (shared users only see views they owned)**

```json
{
  "status": "success",
  "summary": "get trash view list",
  "data": {
    "views": []
  }
}
```

**Case 5 — Trash list including a dashboard tab (`DashTab` type)**

Dashboard tabs have additional fields: `tabParentId`, `tabParentName`, `tabPosition`. These fields are present **only** for views with `viewType: "DashTab"`.

```json
{
  "status": "success",
  "summary": "get trash view list",
  "data": {
    "views": [
      {
        "viewId": "7617000032567701",
        "viewName": "Q1 Summary",
        "viewType": "DashTab",
        "deletedTime": "1682432427100",
        "deletedBy": "admin@example.com",
        "tabParentId": "7617000032567700",
        "tabParentName": "Annual Report Dashboard",
        "tabPosition": 2
      }
    ]
  }
}
```

**Case 6 — List with a `isDisabled` flag (live connect view on unsupported plan)**

When a trashed view is a Live Connect report and the current plan does not support restoring it, the view appears in the list with `isDisabled: true`. Attempting to restore it will fail.

```json
{
  "status": "success",
  "summary": "get trash view list",
  "data": {
    "views": [
      {
        "viewId": "7617000032567800",
        "viewName": "Live_Sales_Report",
        "viewType": "AnalysisView",
        "deletedTime": "1682432428000",
        "deletedBy": "admin@example.com",
        "isDisabled": true
      }
    ]
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Trash Views](../../../sdk-examples/views-management/trash-management/get-trash-views.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify the `<workspace-id>` in the URL. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission to list trash views. | Ensure the user has at least Read permission on the workspace. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid OAuth token. | Provide a valid, non-expired token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Trash Management overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Restore Trash View](restore-trash-view.md), [Delete Trash View](delete-trash-view.md).
- [SDK examples](../../../sdk-examples/views-management/trash-management/get-trash-views.md).
