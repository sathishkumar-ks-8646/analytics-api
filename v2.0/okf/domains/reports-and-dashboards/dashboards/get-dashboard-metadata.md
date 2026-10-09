---
type: API Endpoint
title: Get Dashboard Metadata
description: "Retrieves the stored configuration of a dashboard in the specified workspace - its identity attributes, the visual theme, the layout card map and the behaviour settings."
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
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or the View Owner, or any user with Read Only permission on the dashboard."
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
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1dashboards~1{dashboard-id}~1metadata/get"
    config_schema: GetDashboardMetadataConfig
    response_schema: GetDashboardMetadataResponse
  sdk_examples: "/sdk-examples/reports-and-dashboards/dashboards/get-dashboard-metadata.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}/metadata`** - Get Dashboard Metadata (Dashboards / Reports & Dashboards).

From the OpenAPI specification:

Retrieves the stored configuration of a dashboard in the specified workspace - its identity attributes, the visual theme, the layout card map and the behaviour settings. The optional CONFIG parameter narrows the response to specific sections.

This is the first step of any safe update: fetch the section to be changed, merge the change into it, then send the complete section back through Update Dashboard.

The authenticated user must be an Account Admin or an Organization Admin, or the View Owner, or any user with Read Only permission on the dashboard.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getDashboardMetadata` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}/metadata` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingread) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or the View Owner, or any user with Read Only permission on the dashboard. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - optional |
| Success response | HTTP 200 - `application/json` |
| API ID | 2061 |
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
| `{dashboard-id}` | string | ID of the dashboard whose metadata is retrieved. | [How to obtain](../../../foundations/identifiers.md#dashboard-id) |

## CONFIG Parameters

See the CONFIG schema in the OpenAPI specification referenced in the Endpoint table.

## Notes from the OpenAPI specification

This is a workspace-scoped API. The **ZANALYTICS-ORGID** header carrying the organization ID that owns the workspace is mandatory. A workspaceKey in the format **orgid/workspacename** (for example, 700000123456/Sales_Analytics) may be used in place of the numeric workspace ID in the URL path.

The **include** attribute controls which sections are returned.
- **all**, or omitting CONFIG altogether, returns objId, displayName, description, themes, layout and settings.
- A specific section such as themes returns only that section, without the objId, displayName and description identity fields.
- Several sections can be requested as a comma separated list, for example themes,layout.

As this is a GET request, the CONFIG value must be stringified and URL encoded before it is sent.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Notes from the OpenAPI specification

The metadata response serializes theme and settings scalars as strings even where the CONFIG accepts numbers - for example a **layoutType** sent as 6 is returned as "6", and a card **opacity** sent as 0.2 is returned as "0.2". Only the layout card geometry (**width**, **height**, **left**, **top**) is returned as numbers. Sections that were never customized are omitted from the response entirely.

**dashboardConfig.objId** in the metadata response, **data.dashboardId** in the Create Dashboard response and **viewId** in the listing APIs are the same value under three different field names. Any of them can be used as the dashboard ID in the URL path.

Update Dashboard replaces a whole section rather than merging into it. When **layout**, **themes** or **settings** is included, every stored row for that section is deleted and exactly what was sent is stored.
- Sending only some settings keys reverts all other settings to their system defaults.
- A section that is absent from the CONFIG is left unchanged, so it is safe to omit sections that are not being modified.
- Fetch the section with Get Dashboard Metadata, merge the change into it, then send the complete section back.

Tabbed dashboards are not supported by the V2 API. Calling this API on a tabbed dashboard fails with error code 8102.

# Examples

## Sample Requests

**Case 1 — Retrieve full metadata (all sections)**

```http
GET /restapi/v2/workspaces/320873000000001001/dashboards/320873000000597763/metadata HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 320873000000000001
```

**Case 2 — Retrieve only the layout section**

```http
GET /restapi/v2/workspaces/320873000000001001/dashboards/320873000000597763/metadata?CONFIG={"include":"layout"} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 320873000000000001
```

**Case 3 — Retrieve themes and settings only**

```http
GET /restapi/v2/workspaces/320873000000001001/dashboards/320873000000597763/metadata?CONFIG={"include":"themes,settings"} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 320873000000000001
```

## Sample Responses

**Case 1 — Default theme dashboard with VIEW and USERFILTERS cards (HTTP 200 OK)**

```json
{
  "status": "success",
  "summary": "Get dashboard metadata",
  "data": {
    "dashboardConfig": {
      "objId": "320873000000597763",
      "displayName": "Dashboard_Freeform_19",
      "description": "",
      "themes": {
        "default": "true",
        "layoutType": "2"
      },
      "settings": {
        "enableGlobalUF": "false",
        "smartAlignCharts": "true",
        "allowExport": {
          "pdf": "true",
          "excel": "true",
          "zohoSheet": "true",
          "image": "true",
          "csv": "true",
          "html": "true"
        },
        "showContextualOptions": "true",
        "allowEmbedInsights": "true",
        "enableSortMenu": "true",
        "reportAsFilter": "false",
        "hideColumnOptions": "true",
        "layoutWidth": "1279",
        "allowVUD": "true",
        "allowInsights": "true",
        "fitToWidth": "true",
        "layoutType": "web",
        "allowDrillDown": "true",
        "applyImmediateUF": "true",
        "timeSlicer": "false"
      },
      "layout": {
        "1": {
          "type": "USERFILTERS",
          "width": 80,
          "height": 3,
          "left": 0,
          "top": 0
        },
        "2": {
          "type": "VIEW",
          "width": 80,
          "height": 20,
          "left": 0,
          "top": 3,
          "viewName": "Sales_Report"
        }
      }
    }
  }
}
```

**Case 2 — Dashboard with HTML card (HTTP 200 OK)**

```json
{
  "status": "success",
  "summary": "Get dashboard metadata",
  "data": {
    "dashboardConfig": {
      "objId": "320873000000597796",
      "displayName": "Dashboard_HtmlCard_26",
      "description": "",
      "themes": {
        "default": "true",
        "layoutType": "2"
      },
      "settings": {
        "smartAlignCharts": "true",
        "allowExport": { "pdf": "true", "excel": "true", "zohoSheet": "true", "image": "true", "csv": "true", "html": "true" },
        "fitToWidth": "true",
        "allowDrillDown": "true",
        "applyImmediateUF": "true"
      },
      "layout": {
        "1": {
          "type": "HTML",
          "width": 80,
          "height": 5,
          "left": 0,
          "top": 0,
          "content": "<div><h2 style=\"font-family: Arial; color: #2c3e50;\">Dashboard Header</h2><p>This is a <strong>styled HTML</strong> content card.</p></div>"
        },
        "2": {
          "type": "VIEW",
          "width": 80,
          "height": 20,
          "left": 0,
          "top": 5,
          "viewName": "Pivot"
        }
      }
    }
  }
}
```

**Case 3 — Dashboard with IMAGE card**

```json
{
  "status": "success",
  "summary": "Get dashboard metadata",
  "data": {
    "dashboardConfig": {
      "objId": "320873000000597718",
      "displayName": "Dashboard_ImageCard_9",
      "description": "",
      "themes": {
        "layoutType": "2",
        "solid": { "background": "#ffffff" },
        "type": "solid",
        "card": { "background": "#ffffff" }
      },
      "settings": {
        "smartAlignCharts": "true",
        "allowExport": { "pdf": "true", "excel": "true", "zohoSheet": "true", "image": "true", "csv": "true", "html": "true" },
        "fitToWidth": "true",
        "allowDrillDown": "true"
      },
      "layout": {
        "1": {
          "type": "IMAGE",
          "width": 40,
          "height": 15,
          "left": 0,
          "top": 0,
          "content": "https://example.com/banner.jpg"
        },
        "2": {
          "type": "VIEW",
          "width": 40,
          "height": 20,
          "left": 40,
          "top": 0,
          "viewName": "Sales_Table"
        }
      }
    }
  }
}
```

**Case 4 — Dashboard with gradient theme and card styling**

```json
{
  "status": "success",
  "summary": "Get dashboard metadata",
  "data": {
    "dashboardConfig": {
      "objId": "320873000000487179",
      "displayName": "Dashboard_Gradient_Linear_3",
      "description": "",
      "themes": {
        "card": {
          "desc": { "font": { "size": "9", "color": "#bf00ff", "family": "verdana", "style": "italic" } },
          "shadow": "3",
          "paletteType": "2",
          "radius": "5",
          "margin": "10",
          "opacity": "0.2",
          "background": "#00ff00",
          "title": { "font": { "size": "8", "family": "sans-serif", "style": "bold", "color": "#bf00ff" } },
          "blur": "5"
        },
        "palette": { "chart": { "type": "SOLID__BUSINESS" } },
        "gradient": {
          "endColor": "#000000",
          "mode": "linear",
          "linear": { "angle": "270" },
          "startColor": "#bf00ff",
          "background": "#bf00ff"
        },
        "type": "gradient",
        "chartEffect": { "type": "1", "apply": "2" },
        "layoutType": "6",
        "font": { "color": "#bf00ff", "family": "arial" }
      },
      "settings": {
        "enableGlobalUF": "true",
        "smartAlignCharts": "true",
        "allowExport": { "pdf": "false", "excel": "false", "zohoSheet": "false", "image": "false", "csv": "true", "html": "false" },
        "showContextualOptions": "false",
        "allowEmbedInsights": "true",
        "reportAsFilter": "true",
        "allowDrillDown": "true",
        "applyImmediateUF": "true"
      },
      "layout": {
        "1": { "type": "USERFILTERS", "width": 80, "height": 3, "left": 0, "top": 0 },
        "2": { "type": "VIEW", "width": 40, "height": 20, "left": 0, "top": 8, "viewName": "Chart2" }
      }
    }
  }
}
```

**Case 5 — Full card styling with theme overview (solid type, all card borders and palette)**

```json
{
  "status": "success",
  "summary": "Get dashboard metadata",
  "data": {
    "dashboardConfig": {
      "objId": "320873000000487208",
      "displayName": "Dashboard_ThemeOverviewDefault_47",
      "description": "",
      "themes": {
        "chartEffect": { "apply": "1" },
        "card": {
          "border": { "color": "#cccccc", "width": "1" },
          "shadow": "2",
          "paletteType": "1",
          "blur": "0",
          "radius": "5",
          "margin": "10",
          "opacity": "0.5",
          "background": "#ffffff"
        },
        "palette": { "chart": { "type": "SOLID__BUSINESS" } },
        "type": "solid",
        "font": { "color": "#000000", "family": "Arial" },
        "layoutType": "1",
        "solid": { "background": "#ffffff" }
      },
      "settings": {
        "enableGlobalUF": "false",
        "smartAlignCharts": "true",
        "allowExport": { "pdf": "true", "excel": "true", "zohoSheet": "true", "image": "true", "csv": "true", "html": "true" },
        "showContextualOptions": "true",
        "enableSortMenu": "true",
        "allowVUD": "true",
        "allowInsights": "true",
        "fitToWidth": "true",
        "allowDrillDown": "true",
        "applyImmediateUF": "true"
      },
      "layout": {
        "1": { "type": "VIEW", "width": 40, "height": 20, "left": 0, "top": 0, "viewName": "Pivot" }
      }
    }
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Dashboard Metadata](../../../sdk-examples/reports-and-dashboards/dashboards/get-dashboard-metadata.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

## CONFIG Parameter (Optional)

| Field | Type | Mandatory | Description | Default | Allowed Values |
|-------|------|-----------|-------------|---------|----------------|
| `include` | String | No | Controls which sections of the dashboard config to include in the response. | `all` | `all`, `themes`, `layout`, `settings` |

> When `include` is `"all"`, the response includes `objId`, `displayName`, `description`, `themes`, `layout`, and `settings`.  
> When `include` is set to a specific section (e.g., `"themes"`), only that section is returned (without `objId`/`displayName`/`description`).  
> Multiple sections can be requested via comma-separated values (e.g., `"themes,layout"`).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify the `<workspace-id>` in the URL. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | Dashboard not found. | Verify the `<dashboard-id>` exists and belongs to the specified workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission to view this dashboard. | Ensure the user is an Account Admin, Organization Admin, View Owner, or has Read Only permission on the dashboard. |
| [8072](../../../foundations/error-codes.md#error-8072) | 400 | The target object is not a valid dashboard. | Verify the `<dashboard-id>` refers to a dashboard (not a report or other view type). |
| [8102](../../../foundations/error-codes.md#error-8102) | 400 | Dashboard view type not supported for this operation. | The requested dashboard may be a tabbed dashboard, which is not supported via this API. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | Invalid value supplied for the `include` parameter. | Use one or more of: `all`, `themes`, `layout`, `settings`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid OAuth token. | Provide a valid, non-expired OAuth token with the `ZohoAnalytics.modeling.read` scope. |

# Related

- [Dashboards overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Reports & Dashboards](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get All Dashboards](get-dashboards.md), [Get Owned Dashboards](get-owned-dashboards.md), [Get Shared Dashboards](get-shared-dashboards.md), [Create Dashboard](create-dashboard.md), [Update Dashboard](update-dashboard.md).
- [SDK examples](../../../sdk-examples/reports-and-dashboards/dashboards/get-dashboard-metadata.md).
