---
type: API Endpoint
title: Create Similar Views
description: "Replicates, for a target table, every analysis view - chart, pivot table, summary view and so on - that exists on a reference table in the same workspace."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/similarviews"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - view-operations
  - post
  - modeling
api:
  operation_id: createSimilarViews
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/similarviews"
  domain: views-management
  group: view-operations
  oauth_scopes:
    - ZohoAnalytics.modeling.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin, Organization Admin, or Workspace Admin of the workspace."
  error_codes:
    - 7103
    - 7104
    - 7144
    - 7301
    - 7319
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1similarviews/post"
    config_schema: CreateSimilarViewsConfig
    response_schema: null
  sdk_examples: "/sdk-examples/views-management/view-operations/create-similar-views.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/similarviews`** - Create Similar Views (View Operations / Views Management).

Creates copies of all analysis views (charts, pivot tables, summaries, etc.) that exist on a **reference table** and replicates them for a **target table** within the same workspace. The column bindings in the copied views are automatically remapped to the corresponding columns of the target table.

This API is useful when you have two tables with the same (or compatible) column structure and want to replicate an entire set of reports from one table to the other.

> **`<view-id>` in the URL** is the **target table** — the table for which similar views will be created. The newly generated views will be bound to columns from this table.
>
> **`referenceViewId` in CONFIG** is the **reference table** — the table whose existing analysis views are used as the source templates. The structure (axis bindings, filter conditions, settings) of each view on the reference table is cloned and column references are remapped to match the target table's columns by name.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createSimilarViews` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/similarviews` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organization ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin, Organization Admin, or Workspace Admin of the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1similarviews/post`; CONFIG schema `CreateSimilarViewsConfig` |

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
| `referenceViewId` | Long | **Yes** | — | The ID of the **reference table** within the same workspace. All analysis views built on this reference table will be used as templates. Both `<view-id>` (URL path) and `referenceViewId` must belong to the same workspace; if either does not, the request fails with error **7319**. If the reference table has no analysis views, the call succeeds (HTTP 204) but no views are created. |
| `folderId` | Long | **Yes** | — | The ID of the folder (within the workspace) where all newly created similar views will be placed. There is no default — this field is required. All generated views go into this single folder. If the folder does not exist in the workspace, the request fails with error **7144**. |
| `copyCustomFormula` | Boolean | No | `false` | When `true`: custom formula columns defined on the reference table's views are also copied and mapped to the target table. When `false` (default): formula column definitions are excluded from the copied views. Set to `true` only if the target table has compatible column definitions for the formula expressions to remain valid. Using `true` when column structures differ may result in formula errors on the new views. |
| `copyAggFormula` | Boolean | No | `false` | When `true`: aggregate formula columns (summary-level formulas) defined on the reference table's views are copied to the target table views. When `false` (default): aggregate formulas are excluded. Similar caution applies as with `copyCustomFormula` — only set to `true` if the target table supports the same aggregate expressions. |

> **Column remapping behaviour:**
> When columns are remapped from the reference table to the target table, matching is done by **column name**. If the target table has a column with the exact same name as a column used in a reference view, that axis slot is remapped to the target column. If no matching column is found, that axis slot is left empty or the view may be created in an incomplete state. Always ensure the target table has columns with names matching those used in the reference views before calling this API.

> **Combination note for `copyCustomFormula` + `copyAggFormula`:**
> Both can be `true` simultaneously. When both are `true`, all formula types (custom and aggregate) are included. When both are `false`, only the structural axis/filter bindings are copied — no formula columns.

## Notes from the OpenAPI specification

- The **view-id** path parameter is the **target table** - the table the new views will be bound to. **referenceViewId** in the CONFIG is the **reference table** whose existing analysis views act as the templates.
- Both **view-id** and **referenceViewId** must belong to the workspace given in the URL. If either does not, the request fails with error 7319.
- Column bindings are remapped by **column name**. An axis slot is bound to the target column that carries exactly the same name as the reference column. Where no name matches, the slot is left empty and the view is created in an incomplete state, so charts may render without data until the bindings are corrected manually.
- **copyCustomFormula** and **copyAggFormula** are independent and may both be true, in which case custom and aggregate formula columns are both included. When both are false, only the structural axis and filter bindings are copied.
- A formula copied onto a target table that lacks the columns its expression references is created but stays in an error state at render time until the expression is updated manually.
- If the reference table has no analysis views, the call still succeeds with HTTP 204 and no view is created.
- The target table and the reference table may be the same view ID. The API allows it and the result is a duplicate set of views in the specified folder.
- **folderId** may point to a nested sub-folder. Every generated view is placed directly into that single folder regardless of its nesting level.
- The API is designed for table-to-table replication. Passing an analysis view as **referenceViewId** passes workspace validation but may lead to unexpected behaviour.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

# Examples

## Sample Requests

**Case 1 — Create similar views using default settings (no formula copy)**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000105005/similarviews HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"referenceViewId":466206000000105001,"folderId":466206000000085001}
```

**Case 2 — Copy similar views and include all formula column types**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000105005/similarviews HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"referenceViewId":466206000000105001,"folderId":466206000000085001,"copyCustomFormula":true,"copyAggFormula":true}
```

**Case 3 — Copy similar views with only aggregate formulas**

```http
POST /restapi/v2/workspaces/466206000000071000/views/466206000000107003/similarviews HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"referenceViewId":466206000000105001,"folderId":466206000000090002,"copyCustomFormula":false,"copyAggFormula":true}
```

## Sample Responses

**HTTP 204 No Content** — No response body is returned. Success is indicated purely by the HTTP status code.

```
HTTP/1.1 204 No Content
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Similar Views](../../../sdk-examples/views-management/view-operations/create-similar-views.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>` in the URL is valid. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | Target table (`<view-id>`) or reference table (`referenceViewId`) not found. | Verify both view IDs exist in the workspace. |
| [7144](../../../foundations/error-codes.md#error-7144) | 400 | The specified `folderId` does not exist in this workspace. | Provide a valid, existing folder ID within the same workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not authorised to create views in this workspace. | Ensure the user is an Account Admin, Organization Admin, or Workspace Admin. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | One or both view IDs do not belong to the specified workspace. | Ensure both `<view-id>` (URL) and `referenceViewId` (CONFIG) belong to `<workspace-id>`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |

# Related

- [View Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Save As View](save-as-view.md), [Copy Views](copy-views.md), [Rename View](rename-view.md), [Delete View](delete-view.md), [Get View List](get-views.md), [Get View Details](get-view-details.md), [Get View URL](get-view-url.md), [Get View Dependents](get-view-dependents.md), [Get Recent Views](get-recent-views.md).
- [SDK examples](../../../sdk-examples/views-management/view-operations/create-similar-views.md).
