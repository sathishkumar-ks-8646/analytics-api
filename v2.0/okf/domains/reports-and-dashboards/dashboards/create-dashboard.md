---
type: API Endpoint
title: Create Dashboard
description: Creates a new dashboard in the specified workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/dashboards"
tags:
  - zoho-analytics
  - rest-api-v2
  - reports-and-dashboards
  - dashboards
  - post
  - modeling
api:
  operation_id: createDashboard
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/dashboards"
  domain: reports-and-dashboards
  group: dashboards
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
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or a Shared User, or a Group Member, or any user with Create Report permission on the workspace."
  error_codes:
    - 7103
    - 7111
    - 7301
    - 8072
    - 8119
    - 8535
  openapi:
    file: "/references/openapi/reports-dashboards-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1dashboards/post"
    config_schema: CreateDashboardConfig
    response_schema: CreateDashboardResponse
  sdk_examples: "/sdk-examples/reports-and-dashboards/dashboards/create-dashboard.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/dashboards`** - Create Dashboard (Dashboards / Reports & Dashboards).

From the OpenAPI specification:

Creates a new dashboard in the specified workspace. The dashboard is defined through the CONFIG JSON parameter, which carries the display name, the layout card map and, optionally, the visual theme and the behaviour settings.

The authenticated user must be an Account Admin or an Organization Admin, or a Workspace Admin, or a Shared User, or a Group Member, or any user with Create Report permission on the workspace.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createDashboard` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/dashboards` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or a Shared User, or a Group Member, or any user with Create Report permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| API ID | 2060 |
| OpenAPI | [`reports-dashboards-grouped-api.json`](../../../references/openapi/reports-dashboards-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1dashboards/post`; CONFIG schema `CreateDashboardConfig`; response schema `CreateDashboardResponse` |

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
| `{workspace-id}` | string | ID of the workspace in which the dashboard is created. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameter

The `CONFIG` parameter is a JSON object sent as a form field. `displayName` and `layout` are required.

| Field | Type | Mandatory | Description | Default |
|-------|------|-----------|-------------|---------|
| `displayName` | String | **Yes** | Display name of the new dashboard. Must be unique within the workspace. Max 100 characters. | — |
| `description` | String | No | Optional text description for the dashboard. Max 250 characters. | `""` |
| `layout` | JSON Object | **Yes** | Layout card map. Keys are sequential card index strings (`"1"`, `"2"`, …). Each value is a layout card object (see sub-table below). | — |
| `layoutType` | Integer | No | Grid column preset applied at creation time: `1` = single column, `2` = two columns, `3` = three columns, `4` = four columns. Only meaningful when combined with a `layout` that uses the grid. | `0` (free form) |
| `themes` | JSON Object | No | Visual theme configuration (see Themes Object below). | Default theme |
| `settings` | JSON Object | No | Dashboard behaviour settings (see Settings Object below). | System defaults |

### Layout Card Object

Each entry in `layout` is keyed by its card index (e.g., `"1"`, `"2"`) and contains the following fields:

| Field | Type | Mandatory | Description |
|-------|------|-----------|-------------|
| `type` | String | **Yes** | Card type. Allowed values: `VIEW`, `HTML`, `TITLE`, `PARA`, `IMAGE`, `EMBED`, `USERFILTERS`, `DELETED`. |
| `width` | Integer | **Yes** | Card width in grid units. Combined with `left`, must not exceed `80`. |
| `height` | Integer | **Yes** | Card height in grid units. Minimum varies by type (USERFILTERS: 3, HTML: 5, others: depends). |
| `left` | Integer | **Yes** | Left offset in grid units (0–79). |
| `top` | Integer | **Yes** | Top offset in grid units (0+). |
| `viewName` | String | Yes (for `VIEW`) | Display name of the existing analysis view to embed. Required when `type` is `VIEW`. |
| `content` | String | Yes (for HTML/IMAGE/EMBED/TITLE/PARA) | HTML markup, image URL, or embed URL depending on card type. |
| `properties` | JSON Object | No | Additional card-level properties (e.g., interaction overrides). Optional for `VIEW` cards. |

### Themes Object

| Field | Type | Description | Allowed Values / Constraints |
|-------|------|-------------|------------------------------|
| `default` | String | Reset theme to built-in defaults. If set to `"true"`, all other theme fields are ignored. | `"true"`, `"unset"` |
| `type` | String | Background fill style. | `solid`, `gradient`, `image` |
| `layoutType` | Integer | Preset layout theme number (1–6). | `1`–`6` |
| `solid` | Object | Solid background config. Contains `background` (hex color). | — |
| `gradient` | Object | Gradient background (see Gradient Sub-Object below). | — |
| `image` | Object | Image background (see Image Sub-Object below). | — |
| `font` | Object | Global font settings. Contains `color` (hex), `family` (font name), `size` (7–24), `style` (`plain`, `bold`, `italic`). | — |
| `card` | Object | Card-level styling (see Card Sub-Object below). | — |
| `chartEffect` | Object | Chart animation effect. Contains `apply` (**mandatory**, `1`=none / `2`=apply) and `type` (`1`–`3`). | — |
| `palette` | Object | Color palette for charts. Contains `chart.type` (palette name string). | — |

**Gradient Sub-Object:**

| Field | Type | Description | Allowed Values |
|-------|------|-------------|----------------|
| `background` | String | Fallback background color (hex). | Hex color |
| `startColor` | String | Gradient start color (hex). | Hex color |
| `endColor` | String | Gradient end color (hex). | Hex color |
| `mode` | String | Gradient direction mode. | `linear`, `radial` |
| `linear.angle` | Integer | Angle of the linear gradient in degrees (-270 to 270). | `-270`–`270` |
| `radial.x` | Integer | Horizontal focal point of radial gradient (0–180). | `0`–`180` |
| `radial.y` | Integer | Vertical focal point of radial gradient (0–180). | `0`–`180` |

**Image Sub-Object:**

| Field | Type | Description | Allowed Values |
|-------|------|-------------|----------------|
| `url` | String | URL of the background image. | Valid URL |
| `background` | String | Fallback color behind the image (hex). | Hex color |
| `brightness` | Integer | Brightness adjustment (-100 to 100). | `-100`–`100` |
| `contrast` | Integer | Contrast adjustment (-100 to 100). | `-100`–`100` |
| `transparency` | String | Transparency percentage as a string (`"0"`–`"100"`). | `"0"`–`"100"` |
| `flip` | String | Whether to flip the image (`"true"` / `"false"`). | `"true"`, `"false"` |
| `fitType` | String | Image fit strategy (`"1"` = cover, `"2"` = contain, `"3"` = stretch). | `"1"`, `"2"`, `"3"` |

**Card Sub-Object:**

| Field | Type | Description | Allowed Values |
|-------|------|-------------|----------------|
| `background` | String | Card background color (hex). | Hex color |
| `opacity` | Float | Card background opacity (0.0–1.0). | `0.0`–`1.0` |
| `blur` | Integer | Background blur radius (0–50). | `0`–`50` |
| `radius` | Integer | Card corner radius (0–20). | `0`–`20` |
| `margin` | Integer | Card outer margin (0–10). | `0`–`10` |
| `shadow` | Integer | Card shadow style (1–3). | `1`–`3` |
| `paletteType` | Integer | Card palette variant (`1` = themed, `2` = custom). | `1`, `2` |
| `border` | Object | Card border. Contains `color` (hex) and `width` (string, `"0"`–`"5"`). | — |
| `title` | Object | Card title font. Contains nested `font` object (`color`, `family`, `size`, `style`). | — |
| `desc` | Object | Card description font. Contains nested `font` object (`color`, `family`, `size`, `style`). | — |

### Settings Object

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `enableGlobalUF` | String | Enable global user filter for all cards. | `"false"` |
| `enableGlobalValueUF` | String | Enable global value-based user filter. | `"false"` |
| `smartAlignCharts` | String | Auto-align charts to the grid. | `"true"` |
| `allowExport` | Object | Controls which export formats are enabled. Contains boolean string fields: `csv`, `excel`, `html`, `image`, `pdf`, `zohoSheet`. | All `"true"` |
| `showContextualOptions` | String | Show contextual chart options to viewers. | `"true"` |
| `allowEmbedInsights` | String | Allow embedding AI insights in dashboards. | `"true"` |
| `enableSortMenu` | String | Show sort options in viewer mode. | `"true"` |
| `reportAsFilter` | String | Allow charts to act as filters for other charts. | `"false"` |
| `hideColumnOptions` | String | Hide column-level options in viewer mode. | `"true"` |
| `allowVUD` | String | Allow view/update/delete interactions. | `"true"` |
| `allowInsights` | String | Enable AI-powered insights. | `"true"` |
| `fitToWidth` | String | Stretch dashboard to fill browser width. | `"true"` |
| `layoutType` | String | Layout width mode. | `"web"` |
| `layoutWidth` | String | Custom layout width in pixels (only when `layoutType` is `custom_width`). | `"1279"` |
| `allowDrillDown` | String | Enable drill-down on chart data points. | `"true"` |
| `applyImmediateUF` | String | Apply user filter values immediately (without a submit button). | `"true"` |
| `timeSlicer` | String | Enable time-slicer user filter component. | `"false"` |
| `mapSync` | String | Sync map view across dashboard cards. | `"false"` |

> **layoutType allowed values:** `web`, `custom_width`, `tabloid_1056`, `letter_816`, `a4_797`, `a3_1123`

## Notes from the OpenAPI specification

This is a workspace-scoped API. The **ZANALYTICS-ORGID** header carrying the organization ID that owns the workspace is mandatory. A workspaceKey in the format **orgid/workspacename** (for example, 700000123456/Sales_Analytics) may be used in place of the numeric workspace ID in the URL path.

The CONFIG parameter must be sent as a URL encoded JSON string in a form field named **CONFIG**, with the content type **application/x-www-form-urlencoded**.

A VIEW card identifies an analysis view by its display name in **viewName**, not by its ID. If the referenced view is renamed or deleted the card renders as broken, and when cloning across workspaces the **viewName** values must be updated to match views that exist in the target workspace.

When **layoutType** is set to a grid preset (1 to 4), the server auto-injects a USERFILTERS card at position "1" and rearranges the view cards into columns, so the card indices that were sent may be renumbered. Omit **layoutType**, or set it to 0, for a free form layout, and call Get Dashboard Metadata afterwards to confirm the layout that was actually stored.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Notes from the OpenAPI specification

**dashboardConfig.objId** in the metadata response, **data.dashboardId** in the Create Dashboard response and **viewId** in the listing APIs are the same value under three different field names. Any of them can be used as the dashboard ID in the URL path.

# Examples

## Sample Requests

**Case 1 — Minimal dashboard with a single chart and default theme**

```http
POST /restapi/v2/workspaces/320873000000001001/dashboards HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 320873000000000001
Content-Type: application/x-www-form-urlencoded

CONFIG={"displayName":"Sales Overview","description":"Monthly sales KPIs","layout":{"1":{"type":"VIEW","width":40,"height":20,"left":0,"top":0,"viewName":"Monthly_Sales_Chart","properties":{}},"2":{"type":"VIEW","width":40,"height":20,"left":40,"top":0,"viewName":"Sales_Pivot","properties":{}}}}
```

**Case 2 — Dashboard with gradient theme, card styling, and restricted export**

```http
POST /restapi/v2/workspaces/320873000000001001/dashboards HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 320873000000000001
Content-Type: application/x-www-form-urlencoded

CONFIG={"displayName":"Dashboard_Gradient_Linear_3","themes":{"layoutType":6,"type":"gradient","gradient":{"background":"#bf00ff","startColor":"#bf00ff","endColor":"#000000","mode":"linear","linear":{"angle":270}},"font":{"color":"#bf00ff","family":"arial"},"card":{"background":"#00ff00","opacity":0.2,"blur":5,"margin":10,"radius":5,"shadow":3,"paletteType":2},"chartEffect":{"apply":2,"type":1},"palette":{"chart":{"type":"SOLID__BUSINESS"}}},"settings":{"allowDrillDown":"true","smartAlignCharts":"true","reportAsFilter":"true","showContextualOptions":"false","allowExport":{"csv":"true"},"fitToWidth":"false","enableGlobalUF":"true","applyImmediateUF":"true"},"layout":{"1":{"type":"VIEW","width":40,"height":20,"left":0,"top":8,"viewName":"Chart2","properties":{}},"2":{"type":"USERFILTERS","width":80,"height":3,"left":0,"top":0}}}
```

**Case 3 — Dashboard with image background, HTML card, and image card**

```http
POST /restapi/v2/workspaces/320873000000001001/dashboards HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 320873000000000001
Content-Type: application/x-www-form-urlencoded

CONFIG={"displayName":"Dashboard_Image_Theme_6","themes":{"layoutType":6,"type":"image","image":{"url":"https://example.com/bg.jpg","brightness":2,"flip":"true","transparency":"40","fitType":"2","contrast":5,"background":"#bf00ff"},"font":{"color":"#bf00ff","family":"arial"},"card":{"background":"#00ff00","opacity":0.2,"blur":5,"margin":10,"radius":5,"shadow":3,"paletteType":2},"chartEffect":{"apply":1},"palette":{"chart":{"type":"SOLID__BUSINESS"}}},"layout":{"1":{"type":"HTML","width":80,"height":5,"left":0,"top":0,"content":"<div><h2 style=\"font-family: Arial\">Dashboard Header</h2></div>"},"2":{"type":"IMAGE","width":40,"height":15,"left":0,"top":5,"content":"https://example.com/logo.png"},"3":{"type":"VIEW","width":40,"height":20,"left":40,"top":5,"viewName":"Pivot","properties":{}}}}
```

## Sample Responses

**HTTP 200 OK**

```json
{
  "status": "success",
  "summary": "Create dashboard",
  "data": {
    "dashboardId": "320873000000597763",
    "displayName": "Sales Overview"
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Dashboard](../../../sdk-examples/reports-and-dashboards/dashboards/create-dashboard.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify the `<workspace-id>` in the URL is correct and accessible to the user. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | A dashboard with the same name already exists in the workspace. | Use a different `displayName` value. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission to create a dashboard. | Ensure the user is an Account Admin, Organization Admin, Workspace Admin, Shared User, Group Member, or has Create Report permission. |
| [8072](../../../foundations/error-codes.md#error-8072) | 400 | The target object is not a valid dashboard. | Verify the request parameters and ensure the workspace supports dashboard creation. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | One or more CONFIG field values are invalid (e.g., invalid color, out-of-range number). | Review the CONFIG JSON and correct the invalid values. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid OAuth token. | Provide a valid, non-expired OAuth token with the `ZohoAnalytics.modeling.create` scope. |

# Related

- [Dashboards overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Reports & Dashboards](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get All Dashboards](get-dashboards.md), [Get Owned Dashboards](get-owned-dashboards.md), [Get Shared Dashboards](get-shared-dashboards.md), [Get Dashboard Metadata](get-dashboard-metadata.md), [Update Dashboard](update-dashboard.md).
- [SDK examples](../../../sdk-examples/reports-and-dashboards/dashboards/create-dashboard.md).
