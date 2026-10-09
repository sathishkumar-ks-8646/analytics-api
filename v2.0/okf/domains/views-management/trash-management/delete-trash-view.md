---
type: API Endpoint
title: Delete Trash View
description: Permanently deletes the specified view from the trash.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/trash/{view-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - trash-management
  - delete
  - modeling
api:
  operation_id: deleteTrashView
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/trash/{view-id}"
  domain: views-management
  group: trash-management
  oauth_scopes:
    - ZohoAnalytics.modeling.delete
  org_id_header: required
  config_parameter:
    location: form
    required: false
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner (the user who owned the view before it was trashed)."
  error_codes:
    - 7082
    - 7103
    - 7301
    - 7929
    - 7942
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1trash~1{view-id}/delete"
    config_schema: DeleteTrashViewConfig
    response_schema: null
  sdk_examples: "/sdk-examples/views-management/trash-management/delete-trash-view.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

**DELETE `/restapi/v2/workspaces/{workspace-id}/trash/{view-id}`** - Delete Trash View (Trash Management / Views Management).

> ⚠️ **This operation is permanent and irreversible.** Once a view is deleted from trash, it cannot be recovered. Ensure you mean to permanently delete the view and not restore it.

From the OpenAPI specification:

Permanently deletes the specified view from the trash. The view, its columns, formulas and relations are removed for good and cannot be recovered.

Before deleting, the service checks whether any child dependent views - reports, pivot tables, summary views or query tables built on this view - are also in the trash. If they are, the delete succeeds only when `withDependents` is set to `true`, in which case the children are permanently deleted along with the view; otherwise it fails with error 7942.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deleteTrashView` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/trash/{view-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingdelete) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner (the user who owned the view before it was trashed). See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - optional |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1trash~1{view-id}/delete`; CONFIG schema `DeleteTrashViewConfig` |

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

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `withDependents` | Boolean | No | `false` | When `true`, the view and all its **child dependent views** that are also in trash are permanently deleted together. When `false`, if any child dependent views exist in trash, the delete fails with error `7942`. See **Appendix D** for full details. |

## Notes from the OpenAPI specification

- This operation is permanent and irreversible. The view and its columns, formulas and relations cannot be recovered once deleted from the trash.
- The CONFIG parameter is optional. When it is omitted, **withDependents** is taken as false.
- Delete fails with error 7942 when child dependent views of this view are also in the trash and **withDependents** is false.
- When deleting several views manually, delete the leaf views such as analysis views and pivot tables before the parent tables. This avoids triggering error 7942.
- Deleting a DashTab from the trash does not affect its parent dashboard when the parent is active.
- Error 7929 indicates that the view was already restored and is no longer in the trash, so it cannot be deleted from there. Confirm using the Get Trash Views API.
- The API returns HTTP 204 No Content with an empty body on success.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

# Examples

## Sample Requests

**Case 1 — Permanently delete a standalone analysis view (no children in trash)**

```http
DELETE /restapi/v2/workspaces/7617000032567001/trash/7617000032567466 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Permanently delete a table and all its dependent child views**

If `Sales` table has dependent analysis views (`Region_vs_sales`, `product_Vs_sales`) also in trash, use `withDependents=true` to delete all of them permanently:

```http
DELETE /restapi/v2/workspaces/7617000032567001/trash/7617000032567465 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"withDependents":true}
```

**Case 3 — Attempt to delete a parent table without `withDependents` (will fail)**

```http
DELETE /restapi/v2/workspaces/7617000032567001/trash/7617000032567465 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

This returns error [`7942`](../../../foundations/error-codes.md#error-7942) because `Region_vs_sales` and `product_Vs_sales` are children of `Sales` and are also in trash. Pass `CONFIG={"withDependents":true}` to force-delete.

## Sample Responses

**HTTP 204 No Content** — Delete operations return no response body on success.

```
HTTP/1.1 204 No Content
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Delete Trash View](../../../sdk-examples/views-management/trash-management/delete-trash-view.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7082](../../../foundations/error-codes.md#error-7082) | 400 | An unexpected error occurred during the permanent delete operation. | Retry the request. If it persists, contact support. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify the `<workspace-id>` in the URL. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission to delete this view from trash. | Ensure the user is a Workspace Admin, Account Admin, Organization Admin, or the original view owner. |
| [7929](../../../foundations/error-codes.md#error-7929) | 400 | The view has already been restored from trash and is no longer in the trash bin. | The view is active again — it cannot be deleted from trash. |
| [7942](../../../foundations/error-codes.md#error-7942) | 400 | The view has child dependent views in trash that must be deleted together. | Retry with `"withDependents": true` in the CONFIG. See **Appendix D** for details. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid OAuth token. | Provide a valid, non-expired token with scope `ZohoAnalytics.modeling.delete`. |

# Related

- [Trash Management overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Trash Views](get-trash-views.md), [Restore Trash View](restore-trash-view.md).
- [SDK examples](../../../sdk-examples/views-management/trash-management/delete-trash-view.md).
