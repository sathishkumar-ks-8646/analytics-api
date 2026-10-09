---
type: API Endpoint
title: Rename View
description: Renames an existing view and optionally updates its description.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - view-operations
  - put
  - modeling
api:
  operation_id: renameView
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}"
  domain: views-management
  group: view-operations
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner."
  error_codes:
    - 7103
    - 7104
    - 7111
    - 7301
    - 7319
    - 7413
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}/put"
    config_schema: RenameViewConfig
    response_schema: null
  sdk_examples: "/sdk-examples/views-management/view-operations/rename-view.md"
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

**PUT `/restapi/v2/workspaces/{workspace-id}/views/{view-id}`** - Rename View (View Operations / Views Management).

Renames an existing view and optionally updates its description. This applies to all view types — tables, analysis views, dashboards, query tables, and others.

> ⚠️ **Description is always overwritten:** If `viewDesc` is omitted, the description is set to an empty string and the existing description is cleared. Always include the current description if you do not intend to change it.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `renameView` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organization ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}/put`; CONFIG schema `RenameViewConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.update`. See [Authentication](../../../foundations/authentication.md). |
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
| `viewName` | String | **Yes** | — | The new display name for the view. Must be non-empty and unique within the workspace. If a view with the same name already exists, the request fails with error **7111**. If an empty string is provided, the request fails with error **7413**. The name follows the workspace/view name validation rules for length and allowed characters. |
| `viewDesc` | String | No | `""` | The new description for the view. Maximum 250 characters. **If omitted, the description is cleared to an empty string** — the previous description is not preserved. To retain the existing description, you must explicitly pass its current value. |

## Notes from the OpenAPI specification

- **viewDesc** is always overwritten. When it is omitted, the existing description is cleared to an empty string rather than preserved, so the current description must be passed explicitly to retain it.
- **viewName** must be non-empty. An empty string fails with error 7413.
- **viewName** must be unique within the workspace and a clash fails with error 7111. Renaming a view to the name it already carries succeeds, because the view itself is excluded from the uniqueness check.
- The API applies to every view type - tables, analysis views, dashboards, query tables and others.
- Renaming a view that is embedded in a dashboard propagates to every dashboard card reference immediately. No dashboard update is needed.
- Renaming a query table renames the virtual table alone. The analysis views built on it are not renamed.
- The API returns HTTP 204 No Content with an empty body on success.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

# Examples

## Sample Requests

**Case 1 — Rename a view (update name only, clears description)**

```http
PUT /restapi/v2/workspaces/466206000000071000/views/466206000000105001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"viewName":"Sales_Q3_2024"}
```

**Case 2 — Rename a view and update its description**

```http
PUT /restapi/v2/workspaces/466206000000071000/views/466206000000105001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"viewName":"Revenue Chart - Q3","viewDesc":"Monthly revenue breakdown for Q3 2024"}
```

**Case 3 — Rename a dashboard**

```http
PUT /restapi/v2/workspaces/466206000000071000/views/466206000000109002 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"viewName":"Executive Dashboard v2","viewDesc":"Consolidated KPIs for Q3 review"}
```

## Sample Responses

**HTTP 204 No Content** — No response body is returned on success.

```
HTTP/1.1 204 No Content
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Rename View](../../../sdk-examples/views-management/view-operations/rename-view.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>` in the URL. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | View not found. | Verify `<view-id>` exists in the workspace. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | A view with the given `viewName` already exists in this workspace. | Choose a unique name for the view. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission to rename this view. | Ensure the user is a Workspace Admin, Account Admin, Organization Admin, or the View Owner. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | View does not belong to the specified workspace. | Verify both `<workspace-id>` and `<view-id>` are correct and consistent. |
| [7413](../../../foundations/error-codes.md#error-7413) | 400 | `viewName` is empty. | Provide a non-empty, valid view name. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.update`. |

# Related

- [View Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Save As View](save-as-view.md), [Copy Views](copy-views.md), [Create Similar Views](create-similar-views.md), [Delete View](delete-view.md), [Get View List](get-views.md), [Get View Details](get-view-details.md), [Get View URL](get-view-url.md), [Get View Dependents](get-view-dependents.md), [Get Recent Views](get-recent-views.md).
- [SDK examples](../../../sdk-examples/views-management/view-operations/rename-view.md).
