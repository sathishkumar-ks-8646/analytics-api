---
type: API Endpoint
title: Show Columns
description: Makes one or more previously hidden columns visible again in the specified table.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/show"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - columns
  - put
  - modeling
api:
  operation_id: showColumns
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/show"
  domain: data-modeling-and-schema
  group: columns
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the view."
  error_codes:
    - 7107
    - 7301
    - 7397
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1columns~1show/put"
    config_schema: HideShowColumnConfig
    response_schema: null
  sdk_examples: "/sdk-examples/data-modeling-and-schema/columns/show-columns.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**PUT `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/show`** - Show Columns (Columns / Data Modeling & Schema).

Makes one or more previously hidden columns visible again in the specified table.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `showColumns` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/show` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1columns~1show/put`; CONFIG schema `HideShowColumnConfig` |

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

## CONFIG Parameters

| Parameter | Type | Mandatory | Max Items | Description |
|-----------|------|-----------|-----------|-------------|
| `columnIds` | JSONArray of String | **Yes** | 1000 | Array of column IDs (as strings) to make visible. All IDs must belong to the specified view. |

## Notes from the OpenAPI specification

- This API returns HTTP 204 No Content with no response body on success. There is no status or summary key to parse - treat the HTTP status code as the sole success indicator.
- Showing a column that is already visible is silently ignored. Only the columns that change from hidden to visible are updated.
- Column IDs must be sent as quoted strings inside the JSON array, not as integers.
- There is no minimum or maximum visible column count for this API. The one-visible-column constraint applies only to the Hide Columns API.
- Obtain the column IDs from the Get Table Metadata API, using the isHidden key to identify the columns that are currently hidden.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Show a previously hidden column**

```http
PUT /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns/show HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"columnIds":["7617000000508026"]}
```

**Case 2 — Show multiple hidden columns**

```http
PUT /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns/show HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"columnIds":["7617000000508026","7617000000508027"]}
```

**Case 3 — White label portal user showing columns**

```http
PUT /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns/show HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"columnIds":["7617000000508026"]}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Show Columns](../../../sdk-examples/data-modeling-and-schema/columns/show-columns.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Show Columns returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **Showing an already-visible column** | Silently no-ops — no error is raised. Only columns that change state (hidden → visible) are updated. |
| **`columnIds` values are strings** | Column IDs must be passed as quoted strings in the JSON array, not as integers. |
| **No constraint on showing columns** | There is no minimum or maximum visible column count enforced for Show Columns (only Hide Columns has the one-visible-column minimum constraint). |
| **Dependency** | `<view-id>` → Get View List. `columnIds` → Get Table Metadata (use `columnId` values from columns where `isHidden: true`). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7107](../../../foundations/error-codes.md#error-7107) | 400 | One or more column IDs do not exist in the table. | Verify all IDs using Get Table Metadata. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Design Modify permission on the view. |
| [7397](../../../foundations/error-codes.md#error-7397) | 400 | The view is not a table. | This API only works on tables. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Columns overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Add Column](add-column.md), [Rename Column](rename-column.md), [Delete Column](delete-column.md), [Hide Columns](hide-columns.md), [Get Column Dependents](get-column-dependents.md), [Sort Data by Columns](sort-data-by-columns.md), [Reorder Columns](reorder-columns.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/columns/show-columns.md).
