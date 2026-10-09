---
type: API Endpoint
title: Update Dashboard
description: Updates an existing dashboard in the specified workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - reports-and-dashboards
  - dashboards
  - put
  - modeling
api:
  operation_id: updateDashboard
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}"
  domain: reports-and-dashboards
  group: dashboards
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or the View Owner, or any user with Design Modify permission on the dashboard."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 8072
    - 8102
    - 8119
    - 8535
  openapi:
    file: "/references/openapi/reports-dashboards-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1dashboards~1{dashboard-id}/put"
    config_schema: UpdateDashboardConfig
    response_schema: null
  sdk_examples: "/sdk-examples/reports-and-dashboards/dashboards/update-dashboard.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**PUT `/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}`** - Update Dashboard (Dashboards / Reports & Dashboards).

From the OpenAPI specification:

Updates an existing dashboard in the specified workspace. Every attribute of the CONFIG is optional and a section that is left out is not touched, but a section that is sent replaces the stored one wholesale rather than merging into it. Fetch the section with Get Dashboard Metadata, merge the change into it, then send the complete section back.

`displayName` and `description` are not part of this CONFIG - a dedicated rename API is needed to change the dashboard name.

The authenticated user must be an Account Admin or an Organization Admin, or the View Owner, or any user with Design Modify permission on the dashboard.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `updateDashboard` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or the View Owner, or any user with Design Modify permission on the dashboard. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| API ID | 2062 |
| OpenAPI | [`reports-dashboards-grouped-api.json`](../../../references/openapi/reports-dashboards-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1dashboards~1{dashboard-id}/put`; CONFIG schema `UpdateDashboardConfig` |

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
| `{workspace-id}` | string | ID of the workspace that contains the dashboard. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{dashboard-id}` | string | ID of the dashboard to update. | [How to obtain](../../../foundations/identifiers.md#dashboard-id) |

## CONFIG Parameter

The `CONFIG` parameter is a JSON object. All fields are optional — only the fields provided are updated. To clear the theme back to defaults, use `"default": "true"` inside `themes`.

> **Note:** The `displayName` and `description` fields are **not** part of the Update Dashboard CONFIG. Use a dedicated rename API to change the dashboard name.

| Field | Type | Mandatory | Description | Default |
|-------|------|-----------|-------------|---------|
| `layoutType` | Integer | No | Grid column preset: `1`–`4` (see Create Dashboard for values). | Unchanged |
| `layout` | JSON Object | No | Replacement layout card map. Replaces the entire layout when provided. Card structure is identical to Create Dashboard. | Unchanged |
| `themes` | JSON Object | No | Updated theme settings. Set `"default": "true"` inside to reset to system defaults. Same structure as Create Dashboard `themes`. | Unchanged |
| `settings` | JSON Object | No | Updated settings. Only the settings keys provided are updated (partial update). Same structure as Create Dashboard `settings`. | Unchanged |

## Notes from the OpenAPI specification

Update Dashboard replaces a whole section rather than merging into it. When **layout**, **themes** or **settings** is included, every stored row for that section is deleted and exactly what was sent is stored.
- Sending only some settings keys reverts all other settings to their system defaults.
- A section that is absent from the CONFIG is left unchanged, so it is safe to omit sections that are not being modified.
- Fetch the section with Get Dashboard Metadata, merge the change into it, then send the complete section back.

This is a workspace-scoped API. The **ZANALYTICS-ORGID** header carrying the organization ID that owns the workspace is mandatory. A workspaceKey in the format **orgid/workspacename** (for example, 700000123456/Sales_Analytics) may be used in place of the numeric workspace ID in the URL path.

The CONFIG parameter must be sent as a URL encoded JSON string in a form field named **CONFIG**, with the content type **application/x-www-form-urlencoded**.

A VIEW card identifies an analysis view by its display name in **viewName**, not by its ID. If the referenced view is renamed or deleted the card renders as broken, and when cloning across workspaces the **viewName** values must be updated to match views that exist in the target workspace.

When **layoutType** is set to a grid preset (1 to 4), the server auto-injects a USERFILTERS card at position "1" and rearranges the view cards into columns, so the card indices that were sent may be renumbered. Omit **layoutType**, or set it to 0, for a free form layout, and call Get Dashboard Metadata afterwards to confirm the layout that was actually stored.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Notes from the OpenAPI specification

This API returns no response body on success - only an HTTP 204 No Content status. There is no JSON payload to parse; check the HTTP status code alone. Only failure responses carry a JSON error payload.

Tabbed dashboards are not supported by the V2 API. Calling this API on a tabbed dashboard fails with error code 8102.

# Examples

## Sample Requests

**Case 1 — Update layout to add a new chart card**

```http
PUT /restapi/v2/workspaces/320873000000001001/dashboards/320873000000597763 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 320873000000000001
Content-Type: application/x-www-form-urlencoded

CONFIG={"layout":{"1":{"type":"VIEW","width":40,"height":20,"left":0,"top":0,"viewName":"Sales_Chart","properties":{}},"2":{"type":"VIEW","width":40,"height":20,"left":40,"top":0,"viewName":"Revenue_Pivot","properties":{}},"3":{"type":"USERFILTERS","width":80,"height":3,"left":0,"top":20}}}
```

**Case 2 — Update to solid theme with custom card styling**

```http
PUT /restapi/v2/workspaces/320873000000001001/dashboards/320873000000597763 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 320873000000000001
Content-Type: application/x-www-form-urlencoded

CONFIG={"themes":{"layoutType":1,"type":"solid","solid":{"background":"#333542"},"card":{"background":"#3E3F4D","border":{"color":"#6F738E","width":"2"},"title":{"border":{"color":"#6F738E"}}},"font":{"color":"#ffffff","family":"Arial"},"chartEffect":{"apply":1}}}
```

**Case 3 — Update settings only (restrict exports, enable global filter)**

```http
PUT /restapi/v2/workspaces/320873000000001001/dashboards/320873000000597763 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 320873000000000001
Content-Type: application/x-www-form-urlencoded

CONFIG={"settings":{"enableGlobalUF":"true","allowExport":{"pdf":"false","excel":"true","zohoSheet":"false","csv":"true","html":"false"},"reportAsFilter":"true","fitToWidth":"false"}}
```

## Sample Responses

**HTTP 204 No Content** — The Update Dashboard API returns no response body on success. A 204 status confirms the dashboard was updated.

```
HTTP/1.1 204 No Content
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Update Dashboard](../../../sdk-examples/reports-and-dashboards/dashboards/update-dashboard.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify the `<workspace-id>` in the URL. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | Dashboard not found. | Verify the `<dashboard-id>` exists and belongs to the specified workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission to update this dashboard. | Ensure the user is an Account Admin, Organization Admin, View Owner, or has Design Modify permission on the dashboard. |
| [8072](../../../foundations/error-codes.md#error-8072) | 400 | The target object is not a valid dashboard. | Verify the `<dashboard-id>` refers to a dashboard. |
| [8102](../../../foundations/error-codes.md#error-8102) | 400 | Dashboard view type not supported for this operation. | Tabbed dashboards cannot be updated via this API. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | One or more CONFIG field values are invalid (e.g., out-of-range numbers, invalid colors). | Review the CONFIG JSON and correct the invalid values. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid OAuth token. | Provide a valid, non-expired OAuth token with the `ZohoAnalytics.modeling.update` scope. |

# Related

- [Dashboards overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Reports & Dashboards](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get All Dashboards](get-dashboards.md), [Get Owned Dashboards](get-owned-dashboards.md), [Get Shared Dashboards](get-shared-dashboards.md), [Create Dashboard](create-dashboard.md), [Get Dashboard Metadata](get-dashboard-metadata.md).
- [SDK examples](../../../sdk-examples/reports-and-dashboards/dashboards/update-dashboard.md).
