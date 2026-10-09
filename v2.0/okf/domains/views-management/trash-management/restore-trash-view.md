---
type: API Endpoint
title: Restore Trash View
description: Restores the specified view from the trash back into the workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/trash/{view-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - trash-management
  - post
  - modeling
api:
  operation_id: restoreTrashView
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/trash/{view-id}"
  domain: views-management
  group: trash-management
  oauth_scopes:
    - ZohoAnalytics.modeling.create
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
    - 7941
    - 7943
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1trash~1{view-id}/post"
    config_schema: RestoreTrashViewConfig
    response_schema: null
  sdk_examples: "/sdk-examples/views-management/trash-management/restore-trash-view.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/trash/{view-id}`** - Restore Trash View (Trash Management / Views Management).

From the OpenAPI specification:

Restores the specified view from the trash back into the workspace.

Before restoring, the service checks whether any parent objects the view depends on - the base table, its columns, formulas, relations and data connectors - are also in the trash. If they are, the restore succeeds only when `withDependents` is set to `true`; otherwise it fails with error 7941. When the parents are already active, or the view is standalone, the restore succeeds either way.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `restoreTrashView` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/trash/{view-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner (the user who owned the view before it was trashed). See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - optional |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1trash~1{view-id}/post`; CONFIG schema `RestoreTrashViewConfig` |

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

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `withDependents` | Boolean | No | `false` | When `true`, the view is restored together with all its **parent dependent objects** (tables, columns, formulas, relations, data connectors) that are also in trash and required for the view to function. When `false`, if any required parent objects are also in trash, the restore fails with error `7941`. See **Appendix D** for full details. |

## Notes from the OpenAPI specification

- The CONFIG parameter is optional. When it is omitted, **withDependents** is taken as false.
- Restore fails with error 7941 when the view depends on parent objects that are also in the trash and **withDependents** is false.
- **withDependents** restores only the specified view and the ancestors it requires. Sibling views that depend on the same parent are not restored automatically.
- When restoring several views that were deleted together, restore the parent tables first with **withDependents** as false, then restore the child views. This avoids unintended cascading restores.
- To restore a DashTab, its parent tabbed dashboard must be active. If the parent dashboard is also in the trash, restore the dashboard first or send **withDependents** as true.
- If the folder that originally held the view was deleted as well, the view is restored into the workspace root folder. The folder does not need to be restored first.
- A view listed with **isDisabled** as true cannot be restored under the current plan. Upgrade the plan or delete the view permanently.
- Error 7929 indicates that the view was already restored, possibly by another user or process. Confirm using the Get Trash Views API.
- The API returns HTTP 204 No Content with an empty body on success.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

# Examples

## Sample Requests

**Case 1 — Restore a standalone table (no dependencies)**

```http
POST /restapi/v2/workspaces/7617000032567001/trash/7617000032567618 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Restore an analysis view that depends on a trashed parent table**

If `Sales` table is also in trash, the view `Region_vs_sales` (which is based on `Sales`) cannot be restored alone. Use `withDependents=true`:

```http
POST /restapi/v2/workspaces/7617000032567001/trash/7617000032567466 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"withDependents":true}
```

**Case 3 — Restore with explicit `withDependents=false` (safe for independent views)**

```http
POST /restapi/v2/workspaces/7617000032567001/trash/7617000032567597 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"withDependents":false}
```

## Sample Responses

**HTTP 204 No Content** — Restore operations return no response body on success.

```
HTTP/1.1 204 No Content
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Restore Trash View](../../../sdk-examples/views-management/trash-management/restore-trash-view.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7082](../../../foundations/error-codes.md#error-7082) | 400 | An unexpected error occurred during the trash restore operation. | Retry the request. If the error persists, contact support. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify the `<workspace-id>` in the URL. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission to restore this view from trash. | Ensure the user is a Workspace Admin, Account Admin, Organization Admin, or the original owner of the trashed view. |
| [7929](../../../foundations/error-codes.md#error-7929) | 400 | The view has already been restored from trash. | The view is no longer in trash. No action needed. |
| [7941](../../../foundations/error-codes.md#error-7941) | 400 | The view has parent dependencies that are also in trash and must be restored together. | Retry with `"withDependents": true` in the CONFIG. See **Appendix D** for details. |
| [7943](../../../foundations/error-codes.md#error-7943) | 400 | The requesting user does not have permission to restore this specific trashed view. | Only the view's original owner or an admin can restore it. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid OAuth token. | Provide a valid, non-expired token with scope `ZohoAnalytics.modeling.create`. |

# Related

- [Trash Management overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Trash Views](get-trash-views.md), [Delete Trash View](delete-trash-view.md).
- [SDK examples](../../../sdk-examples/views-management/trash-management/restore-trash-view.md).
