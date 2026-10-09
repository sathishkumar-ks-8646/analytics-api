---
type: API Endpoint
title: Save As View
description: Creates a copy of an existing view (table or analysis view) within the same workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/saveas"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - view-operations
  - post
  - modeling
api:
  operation_id: saveAsView
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/saveas"
  domain: views-management
  group: view-operations
  oauth_scopes:
    - ZohoAnalytics.modeling.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Design & Modify permission on the workspace."
  error_codes:
    - 7103
    - 7104
    - 7111
    - 7144
    - 7301
    - 7319
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1saveas/post"
    config_schema: SaveAsViewConfig
    response_schema: SaveAsViewResponse
  sdk_examples: "/sdk-examples/views-management/view-operations/save-as-view.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/saveas`** - Save As View (View Operations / Views Management).

Creates a copy of an existing view (table or analysis view) within the **same workspace**. The new view is independent of the original after creation — changes to one do not affect the other.

From the OpenAPI specification:

Creates a copy of an existing view (table or analysis view) within the same workspace. The new view is independent of the original after creation — changes to one do not affect the other.

The new view is independent of the original once created; later changes to one do not affect the other. For a table, `copyWithData`, `copyWithLookup` and `copyHugeData` control how much of the source is reproduced. For an analysis view those three attributes are ignored and only the view definition is copied.

The ID of the newly created view is returned in the response and is used to reference the copy in subsequent APIs.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `saveAsView` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/saveas` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - must be the Organization ID of the workspace in which the source view resides. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Design & Modify permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1saveas/post`; CONFIG schema `SaveAsViewConfig`; response schema `SaveAsViewResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameter

The CONFIG parameter is a JSON object sent as a **form parameter** named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `viewName` | String | **Yes** | — | The display name for the newly created view. Must be unique within the workspace. If a view with this name already exists, the request fails with error **7111**. Maximum length follows the workspace/view name validation rules. |
| `viewDesc` | String | No | `""` | A short description for the new view. Maximum 250 characters. If omitted, the new view is created with an empty description. |
| `copyWithData` | Boolean | No | `false` | **Applies to Tables only. Ignored for analysis views (charts, pivots, summaries, etc.).** When `true`: the new table is created as a full copy including all existing row data. When `false`: only the table schema (columns, data types, lookup references, formula definitions) is copied — no row data is duplicated. Use `false` (default) for schema-only copies that will be populated with new data. Combining with `copyHugeData=true` enables asynchronous background copy for large datasets. |
| `copyWithLookup` | Boolean | No | `false` | **Applies to Tables only. Ignored for analysis views.** When `true`: any lookup (join) relationships defined on the source table are also replicated on the new table copy. The copied lookup points to the same referenced table. When `false` (default): lookup definitions are dropped and the new table is standalone. Set to `true` when the new table needs to participate in the same relational model as the source. |
| `copyHugeData` | Boolean | No | `false` | **Applies to Tables only. Ignored for analysis views.** When `true`: data copy is processed asynchronously in the background, allowing the API call to return quickly even for large datasets. The `viewId` is returned immediately but the data population continues in the background. When `false` (default): the API call is synchronous and waits until data copy is complete before returning. Use `true` only when `copyWithData=true` and the source table is large (hundreds of thousands of rows or more) to avoid request timeouts. |
| `folderId` | Long | No | `null` | The ID of the folder within the workspace where the new view should be placed. If omitted (default `null`): the new view is placed in the root-level unorganised area of the workspace. If provided and the folder does not exist in the workspace, the request fails with error **7144**. Use the folder listing API or workspace metadata to get valid folder IDs. |

> **Note on view-type behaviour:**
> - For **Analysis Views** (charts, pivot tables, summary views, query tables, etc.): `copyWithData`, `copyWithLookup`, and `copyHugeData` are all silently ignored. The view definition (axis bindings, filters, settings) is copied. Additional permission checks are applied — the user must also have save permission on the parent table(s) of the analysis view.
> - For **Tables**: all CONFIG fields apply as described.
> - **Dashboards** cannot be duplicated via this API; use Save As on individual views or create a new dashboard manually.

## Notes from the OpenAPI specification

- The new view is independent of the source view once created. Later changes to one do not affect the other.
- **copyWithData**, **copyWithLookup** and **copyHugeData** apply to Tables only. They are silently ignored for analysis views such as charts, pivot tables, summary views and query tables, for which only the view definition - axis bindings, filters and settings - is copied.
- For an analysis view, the user must also hold save permission on the parent table of that view. If the parent table has been deleted or is inaccessible, the request fails with a permission or not-found error.
- **copyHugeData** has an effect only when **copyWithData** is true. Sent on its own it is ignored and the copy stays synchronous and schema-only.
- When **copyWithData** is true and **copyHugeData** is false, the HTTP request may time out on a very large table before the data copy finishes. Use **copyHugeData** as true for such tables.
- When **copyHugeData** is true, the **viewId** is returned immediately while the row data continues to populate in the background.
- When **copyWithLookup** is true and a referenced table no longer exists, that lookup definition is dropped silently and the copy still succeeds.
- **folderId** must belong to the same workspace as the source view. A folder from another workspace fails with error 7144. When it is omitted, the new view is placed in the root-level unorganised area of the workspace.
- Dashboards are not supported by this API. The request may return a new view ID, but card bindings can be broken unless the referenced views are also copied. Use the Copy Views API for full dashboard duplication.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

# Examples

## Sample Requests

**Case 1 — Save As a table (schema only, no data)**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000105001/saveas HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"viewName":"Sales_Archive","viewDesc":"Copy of Sales table for archival","copyWithData":false,"copyWithLookup":true,"folderId":466206000000085001}
```

**Case 2 — Save As a table with data (async copy for large table)**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000105001/saveas HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"viewName":"Sales_Backup_Q3","copyWithData":true,"copyHugeData":true}
```

**Case 3 — Save As an analysis view (chart/report)**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000109002/saveas HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"viewName":"Revenue Trend - Copy","viewDesc":"Duplicate of Q3 revenue trend chart"}
```

## Sample Responses

**HTTP 200 OK**

```json
{
  "status": "success",
  "summary": "Saveas view",
  "data": {
    "viewId": "466206000000120001"
  }
}
```

| Response Field | Type | Description |
|----------------|------|-------------|
| `status` | String | `"success"` indicates successful creation. |
| `summary` | String | Human-readable result summary: `"Saveas view"`. |
| `data.viewId` | String | The ID of the **newly created** view. Use this ID in subsequent APIs. |

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Save As View](../../../sdk-examples/views-management/view-operations/save-as-view.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>` in the URL is a valid, accessible workspace. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | Source view not found. | Verify `<view-id>` exists within the specified workspace. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | A view with the given `viewName` already exists in this workspace. | Choose a different, unique name for the new view. |
| [7144](../../../foundations/error-codes.md#error-7144) | 400 | The specified `folderId` does not exist in this workspace. | Provide a valid folder ID from within the same workspace, or omit `folderId` to place the view at the root level. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission to duplicate this view. | Ensure the user is a Workspace Admin, Account Admin, Organization Admin, or has Design & Modify permission on the workspace. For analysis views, the user must also have save permission on the parent table. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The source view does not belong to the specified workspace. | Ensure both `<workspace-id>` and `<view-id>` are correct and consistent. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |

# Related

- [View Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Copy Views](copy-views.md), [Create Similar Views](create-similar-views.md), [Rename View](rename-view.md), [Delete View](delete-view.md), [Get View List](get-views.md), [Get View Details](get-view-details.md), [Get View URL](get-view-url.md), [Get View Dependents](get-view-dependents.md), [Get Recent Views](get-recent-views.md).
- [SDK examples](../../../sdk-examples/views-management/view-operations/save-as-view.md).
