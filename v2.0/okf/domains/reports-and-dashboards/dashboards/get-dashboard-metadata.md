---
type: API Endpoint
title: Read Dashboard Metadata
description: Returns the stored configuration of a dashboard.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}/metadata"
tags:
  - zoho-analytics
  - rest-api-v2
  - reports-and-dashboards
  - dashboards
  - get
  - modeling
api:
  operation_id: getDashboardMetadata
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}/metadata"
  domain: reports-and-dashboards
  group: dashboards
  oauth_scopes:
    - ZohoAnalytics.modeling.read
  org_id_header: required
  config_parameter:
    location: query
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "Read Only or higher on the dashboard. Owners, Workspace Admins, Organization Admins, shared users and group members with read access all qualify."
  rate_limit: 20 requests per user per 60 seconds
  error_codes:
    - 7018
    - 7103
    - 7104
    - 7301
    - 7309
    - 7319
    - 7511
    - 8509
    - 8535
  openapi:
    file: "/references/openapi/reports-dashboards-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1dashboards~1{dashboard-id}~1metadata/get"
    config_schema: GetDashboardMetadataConfig
    response_schema: GetDashboardMetadataResponse
  sdk_examples: "/sdk-examples/reports-and-dashboards/dashboards/get-dashboard-metadata.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}/metadata`** - Read Dashboard Metadata (Dashboards / Reports & Dashboards).

Returns the stored configuration of a dashboard. This is the read half of the read-modify-write cycle
that [Update Dashboard](update-dashboard.md) requires.

From the OpenAPI specification:

Returns the stored configuration of a dashboard. This is the read half of the read-modify-write cycle that Update Dashboard requires.

Permission required: Read Only or higher on the dashboard. Owners, Workspace Admins, Organization Admins, shared users and group members with read access all qualify.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getDashboardMetadata` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}/metadata` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingread) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | Read Only or higher on the dashboard. Owners, Workspace Admins, Organization Admins, shared users and group members with read access all qualify. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - optional |
| Success response | HTTP 200 - `application/json` |
| Rate limit | 20 requests per user per 60 seconds. See [Rate limits](../../../foundations/rate-limits-and-quotas.md). |
| Custom domain | Permitted when the workspace is mapped to the calling domain. |
| Throttle | 20 requests per minute per user. |
| OpenAPI | [`reports-dashboards-grouped-api.json`](../../../references/openapi/reports-dashboards-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1dashboards~1{dashboard-id}~1metadata/get`; CONFIG schema `GetDashboardMetadataConfig`; response schema `GetDashboardMetadataResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace that contains the dashboard. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{dashboard-id}` | string | ID of the dashboard whose configuration is returned. | [How to obtain](../../../foundations/identifiers.md#dashboard-id) |

## CONFIG Parameter

Optional. Sent as a query parameter.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `include` | String | No | `all` | Which section to return. Exactly one of `all`, `layout`, `themes`, `settings`. Comma-separated lists are **not** accepted. |

When `include` is `all`, the response carries `objId`, `displayName`, `description` and all three
sections. When `include` names a single section, only that section is returned — the identity fields are
omitted.

## Notes from the OpenAPI specification

This is a workspace-scoped API. The **ZANALYTICS-ORGID** header carrying the organization ID that owns the workspace is mandatory.

Tabbed dashboards are out of scope: Read and Update reject a tabbed dashboard with **7511**.

CONFIG is optional and travels as a URL encoded JSON query parameter. **include** names exactly one of all, layout, themes, settings; comma-separated lists are rejected with 8509. With a single section only that section is returned and the identity fields are omitted.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Notes from the OpenAPI specification

The response is not a valid Create or Update payload. Re-serialise **layout** to a string, delete **objId**, **displayName** and **description** before an update (8542), convert the theme numbers that come back as strings (**card.blur**, **card.radius**, **card.margin**, **image.transparency**, **image.flip**) back to numbers/booleans, and expect card IDs renumbered from "1". **layoutType**, card **properties**, **image_properties** and **allowAllExport** are written but never returned.

**dashboardConfig.objId** in the metadata response, **data.dashboardId** in the Create Dashboard response and **viewId** in the listing APIs are the same value under three field names. Any of them can be used as the dashboard ID in the URL path.

# Examples

## Sample Requests

**Case 1 — Full configuration**

```http
GET /restapi/v2/workspaces/466206000000071000/dashboards/466206000000106002/metadata HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Layout only**

```http
GET /restapi/v2/workspaces/466206000000071000/dashboards/466206000000106002/metadata?CONFIG={"include":"layout"} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**Case 1 — `include=all` (default)**

```json
{
  "status": "success",
  "summary": "Get dashboard metadata",
  "data": {
    "dashboardConfig": {
      "objId": "466206000000106002",
      "displayName": "Regional Performance",
      "description": "Quarterly regional roll-up",
      "themes": {
        "default": "true",
        "layoutType": "2"
      },
      "settings": {
        "allowDrillDown": "true",
        "hideColumnOptions": "true",
        "smartAlignCharts": "true",
        "enableSortMenu": "true",
        "reportAsFilter": "false",
        "showContextualOptions": "true",
        "allowVUD": "true",
        "allowInsights": "true",
        "allowEmbedInsights": "true",
        "fitToWidth": "true",
        "enableGlobalUF": "false",
        "applyImmediateUF": "true",
        "timeSlicer": "false",
        "layoutType": "web",
        "layoutWidth": "1279",
        "allowExport": {
          "csv": "true", "excel": "true", "html": "true",
          "image": "true", "pdf": "true", "zohoSheet": "true"
        }
      },
      "layout": {
        "1": { "type": "USERFILTERS", "width": 80, "height": 3, "left": 0, "top": 0 },
        "2": { "type": "TITLE", "width": 80, "height": 3, "left": 0, "top": 3, "content": "<b>Q3 Performance</b>" },
        "3": { "type": "VIEW", "width": 40, "height": 20, "left": 0, "top": 6, "viewName": "Sales by Region" },
        "4": { "type": "VIEW", "width": 40, "height": 20, "left": 40, "top": 6, "viewName": "Margin by Region" }
      }
    }
  }
}
```

**Case 2 — `include=layout`**

```json
{
  "status": "success",
  "summary": "Get dashboard metadata",
  "data": {
    "dashboardConfig": {
      "layout": {
        "1": { "type": "USERFILTERS", "width": 80, "height": 3, "left": 0, "top": 0 },
        "2": { "type": "VIEW", "width": 80, "height": 20, "left": 0, "top": 3, "viewName": "Sales Chart" }
      }
    }
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Read Dashboard Metadata](../../../sdk-examples/reports-and-dashboards/dashboards/get-dashboard-metadata.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

- The returned `layout` is renumbered from `"1"` in storage order; the card IDs you supplied on create
  are not preserved.
- `VIEW` cards are returned with `viewName` resolved to the view's current display name.
- `DELETED` cards carry a `respContent` message explaining whether the underlying view was deleted or
  permanently removed.
- A tabbed dashboard raises **7511** rather than returning a body.
- The response is **not** a valid Update payload. See
  [Round-tripping a dashboard](overview.md#round-tripping-a-dashboard) for the transformations required and the
  list of attributes that are never returned.

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7018](../../../foundations/error-codes.md#error-7018) | 400 | Malformed URL — the ID is not a valid numeric path segment. | Use the numeric dashboard ID only. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The dashboard does not exist, or `<dashboard-id>` is `0`. | Verify `<dashboard-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The caller lacks read permission on the dashboard, or is on an unmapped white-label domain. | Share the dashboard with the caller. |
| [7309](../../../foundations/error-codes.md#error-7309) | 400 | `Authorization` header absent. | Send the OAuth header. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The dashboard exists but belongs to a different workspace. | Make `<workspace-id>` and `<dashboard-id>` consistent. |
| [7511](../../../foundations/error-codes.md#error-7511) | 400 | The target is a tabbed dashboard. | Tabbed dashboards cannot be read through this API. |
| [8509](../../../foundations/error-codes.md#error-8509) | 400 | `include` is not one of `all`, `layout`, `themes`, `settings`. | Use a single valid section name. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Refresh with scope `ZohoAnalytics.modeling.read`. |

# Related

- [Dashboards overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Reports & Dashboards](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Dashboard](create-dashboard.md), [Update Dashboard](update-dashboard.md), [Get All Dashboards](get-dashboards.md), [Get Owned Dashboards](get-owned-dashboards.md), [Get Shared Dashboards](get-shared-dashboards.md).
- [SDK examples](../../../sdk-examples/reports-and-dashboards/dashboards/get-dashboard-metadata.md).
