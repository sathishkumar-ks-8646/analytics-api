---
type: API Endpoint
title: Delete View
description: Permanently deletes a view from a workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - view-operations
  - delete
  - modeling
api:
  operation_id: deleteView
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}"
  domain: views-management
  group: view-operations
  oauth_scopes:
    - ZohoAnalytics.modeling.delete
  org_id_header: required
  config_parameter:
    location: form
    required: false
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 7319
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}/delete"
    config_schema: DeleteViewConfig
    response_schema: null
  sdk_examples: "/sdk-examples/views-management/view-operations/delete-view.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}/views/{view-id}`** - Delete View (View Operations / Views Management).

Permanently deletes a view from a workspace. The view is moved to the workspace's **Trash** first (soft-delete), from where it can be restored within the retention period. This applies to all view types.

> ⚠️ **Dependent views:** If the view being deleted has other views that depend on it (e.g., analysis views built on a table, or charts embedded in a dashboard), deletion will fail by default unless `deleteDependentViews=true` is set. When set to `true`, all dependent views are also deleted along with the target view.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deleteView` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingdelete) |
| ZANALYTICS-ORGID header | **Required** - Organization ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - optional |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}/delete`; CONFIG schema `DeleteViewConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.delete`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameter

The CONFIG parameter is optional. When provided, it is a JSON object sent as a **form parameter** named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `deleteDependentViews` | Boolean | No | `false` | When `false` (default): if any other view in the workspace depends on `<view-id>` (e.g., an analysis view built on a table being deleted, a dashboard containing views from this table, or a query table referencing this table), the delete operation fails. The error surfaces as a dependency conflict. When `true`: the target view **and all views that depend on it** are deleted in the same operation. This includes direct dependents and transitive dependents (dependents of dependents). Use `true` only when you intend to clean up the entire view graph for this view. This action cannot be undone from the API; all deleted views go to Trash and must be restored individually from there if needed. |

## Notes from the OpenAPI specification

- This is a soft delete. The view is moved to the workspace Trash and can be brought back with the Restore Trash View API within the retention period, after which it is purged permanently.
- The CONFIG parameter is optional. When it is omitted, **deleteDependentViews** is taken as false.
- When **deleteDependentViews** is false and another view depends on this one, the request fails with a dependency error and nothing is deleted. Use the Get View Details API with **withInvolvedMetaInfo** as true to identify the dependents first.
- When **deleteDependentViews** is true, direct and transitive dependents go with the view in the same operation. A table with 50 analysis views loses all 50, and an analysis view embedded in dashboards takes those dashboards with it.
- Deleting an individual dashboard tab removes that tab and every view it holds from the parent tabbed dashboard. If it is the last remaining tab, the parent tabbed dashboard itself may be affected.
- Deleting a tabbed dashboard deletes the parent object, and its constituent tabs count as dependents. Send **deleteDependentViews** as true to remove them in the same call.
- Deleting a table that acts as a lookup source leaves orphaned lookup columns in the tables that reference it. Send **deleteDependentViews** as true, or remove the lookup relationship first.
- Every view removed by this call goes to Trash separately and must be restored individually from there.
- The API returns HTTP 204 No Content with an empty body on success.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

# Examples

## Sample Requests

**Case 1 — Delete a standalone view (no dependents)**

```http
DELETE /restapi/v2/workspaces/466206000000071000/views/466206000000109002 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Delete a table and all its dependent analysis views**

```http
DELETE /restapi/v2/workspaces/466206000000071000/views/466206000000105001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"deleteDependentViews":true}
```

**Case 3 — Delete a dashboard (no dependent views on dashboards)**

```http
DELETE /restapi/v2/workspaces/466206000000071000/views/466206000000106002 HTTP/1.1
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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Delete View](../../../sdk-examples/views-management/view-operations/delete-view.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>` in the URL. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | View not found. | Verify `<view-id>` exists in the workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission to delete this view. Occurs when the user is neither a Workspace Admin, Account Admin, Organization Admin, nor the View Owner. | Ensure the user has the required role. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | View does not belong to the specified workspace. | Verify both `<workspace-id>` and `<view-id>` are correct. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.delete`. |

# Related

- [View Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Save As View](save-as-view.md), [Copy Views](copy-views.md), [Create Similar Views](create-similar-views.md), [Rename View](rename-view.md), [Get View List](get-views.md), [Get View Details](get-view-details.md), [Get View URL](get-view-url.md), [Get View Dependents](get-view-dependents.md), [Get Recent Views](get-recent-views.md).
- [SDK examples](../../../sdk-examples/views-management/view-operations/delete-view.md).
