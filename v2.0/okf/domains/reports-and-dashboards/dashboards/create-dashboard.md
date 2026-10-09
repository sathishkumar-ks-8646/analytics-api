---
type: API Endpoint
title: Create Dashboard
description: Creates a dashboard in the given workspace and returns its ID.
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
  permission_required: "Workspace Admin / Organization Admin, or a shared or group user holding Create Report permission on the workspace. A Custom Role user must have the Create Report permission explicitly granted, otherwise the call is rejected before any validation runs."
  rate_limit: "10 requests per user per 60 seconds; lockout 600 seconds on breach"
  error_codes:
    - 7103
    - 7111
    - 7301
    - 7309
    - 7479
    - 7480
    - 7481
    - 7482
    - 7483
    - 7484
    - 7485
    - 7486
    - 7487
    - 7488
    - 7491
    - 7492
    - 7493
    - 7507
    - 7510
    - 7512
    - 7513
    - 7514
    - 8027
    - 8504
    - 8509
    - 8517
    - 8534
    - 8535
    - 8542
    - 9001
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
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/dashboards`** - Create Dashboard (Dashboards / Reports & Dashboards).

Creates a dashboard in the given workspace and returns its ID.

From the OpenAPI specification:

Creates a dashboard in the given workspace and returns its ID.

Permission required: Workspace Admin / Organization Admin, or a shared or group user holding Create Report permission on the workspace. A Custom Role user must have the Create Report permission explicitly granted, otherwise the call is rejected before any validation runs.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createDashboard` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/dashboards` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | Workspace Admin / Organization Admin, or a shared or group user holding Create Report permission on the workspace. A Custom Role user must have the Create Report permission explicitly granted, otherwise the call is rejected before any validation runs. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| Rate limit | 10 requests per user per 60 seconds; lockout 600 seconds on breach. See [Rate limits](../../../foundations/rate-limits-and-quotas.md). |
| Content-Type | `application/x-www-form-urlencoded` |
| Custom domain | Permitted, but only when the target workspace is mapped to the calling white-label domain. A mismatch raises **7301**. |
| Throttle | 10 requests per minute per user; 10-minute lock-out on breach. |
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

`CONFIG` is a JSON object sent as a form-encoded body parameter. Maximum encoded size 5,000,000
characters.

| Field | Type | Mandatory | Constraints | Description |
|-------|------|-----------|-------------|-------------|
| `displayName` | String | **Yes** | 1–100 characters; unique within the workspace | Name of the dashboard. |
| `layout` | String | **Yes** | JSON-encoded string, max 1,000,000 characters | The card layout. See [The layout model](overview.md#the-layout-model). |
| `description` | String | No | Max 250 characters | Free-text description. |
| `themes` | JSONObject | No | Max 10,000 characters | Visual theme. See [Themes](#themes). Omitting it writes the default theme `{"default":"true","type":"2"}`. |
| `settings` | JSONObject | No | Max 10,000 characters | Viewer behaviour flags. See [Settings](#settings). Omitting it writes the full default settings object. |
| `layoutType` | Integer | No | 1–4 | Generate a 1/2/3/4-column layout instead of using the supplied geometry. See [Generated layouts](overview.md#generated-layouts-layouttype). |

## Notes from the OpenAPI specification

This is a workspace-scoped API. The **ZANALYTICS-ORGID** header carrying the organization ID that owns the workspace is mandatory.

Tabbed dashboards are out of scope: Read and Update reject a tabbed dashboard with **7511**.

The CONFIG parameter must be sent as a URL encoded JSON string in a form field named **CONFIG**, with the content type **application/x-www-form-urlencoded**.

The **layout** attribute inside CONFIG is a JSON-encoded **string**, not a nested object: CONFIG={"displayName":"Sales Overview","layout":"{\"1\":{\"type\":\"VIEW\",\"viewName\":\"Sales Chart\",\"width\":80,\"height\":20,\"left\":0,\"top\":0}}"}. **themes** and **settings** are ordinary nested objects. Read Dashboard Metadata returns **layout** as a genuine object, so it must be re-serialised to a string before being written back.

A VIEW card identifies a report by its display name in **viewName**, matched case-insensitively. The view must exist in the workspace (8027) and be readable by the caller (7481). Two cards may reference the same view.

When **layoutType** is 1 to 4 the supplied geometry is discarded and a 1/2/3/4-column layout is generated: a full-width USERFILTERS card, one HTML card per **content** value, then one VIEW card per distinct **viewName**. Omit **layoutType**, or send 0, to keep the layout as submitted. Auto-layout is not recorded in the read response.

The CONFIG parameter has a maximum encoded size of 5,000,000 characters; the encoded **layout** string at most 1,000,000.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Notes from the OpenAPI specification

**dashboardConfig.objId** in the metadata response, **data.dashboardId** in the Create Dashboard response and **viewId** in the listing APIs are the same value under three field names. Any of them can be used as the dashboard ID in the URL path.

# Examples

## Sample Requests

**Case 1 — Minimal dashboard with one report**

```http
POST /restapi/v2/workspaces/466206000000071000/dashboards HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"displayName":"Sales Overview","layout":"{\"1\":{\"type\":\"VIEW\",\"viewName\":\"Sales Chart\",\"width\":80,\"height\":20,\"left\":0,\"top\":0}}"}
```

**Case 2 — Filter panel, a heading and two side-by-side reports**

```http
POST /restapi/v2/workspaces/466206000000071000/dashboards HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
  "displayName": "Regional Performance",
  "description": "Quarterly regional roll-up",
  "layout": "{
     \"1\": {\"type\":\"USERFILTERS\",\"width\":80,\"height\":3,\"left\":0,\"top\":0},
     \"2\": {\"type\":\"TITLE\",\"width\":80,\"height\":3,\"left\":0,\"top\":3,\"content\":\"<b>Q3 Performance</b>\"},
     \"3\": {\"type\":\"VIEW\",\"width\":40,\"height\":20,\"left\":0,\"top\":6,\"viewName\":\"Sales by Region\"},
     \"4\": {\"type\":\"VIEW\",\"width\":40,\"height\":20,\"left\":40,\"top\":6,\"viewName\":\"Margin by Region\"}
  }",
  "settings": {"allowDrillDown":"true","fitToWidth":"true","reportAsFilter":"true","layoutType":"web"},
  "themes": {
    "layoutType": 2,
    "type": "solid",
    "solid": {"background": "#333542"},
    "card": {"background":"#3E3F4D","border":{"color":"#6F738E","width":2},"title":{"border":{"color":"#6F738E"}}}
  }
}
```

**Case 3 — Let the server lay the cards out in two columns**

Only the view names matter here; the geometry is replaced.

```http
POST /restapi/v2/workspaces/466206000000071000/dashboards HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"displayName":"Auto Layout","layoutType":2,"layout":"{\"1\":{\"type\":\"VIEW\",\"viewName\":\"Sales Chart\",\"width\":40,\"height\":20,\"left\":0,\"top\":0},\"2\":{\"type\":\"VIEW\",\"viewName\":\"Margin Chart\",\"width\":40,\"height\":20,\"left\":40,\"top\":0}}"}
```

**Case 4 — Gradient theme**

```
CONFIG={
  "displayName": "Gradient Demo",
  "layout": "{\"1\":{\"type\":\"VIEW\",\"viewName\":\"Sales Chart\",\"width\":80,\"height\":20,\"left\":0,\"top\":0}}",
  "themes": {
    "type": "gradient",
    "gradient": {"background":"#1B1C28","startColor":"#2A2D3E","endColor":"#13141C","mode":"linear","linear":{"angle":135}},
    "card": {"background":"#22242F","opacity":0.9,"blur":4}
  }
}
```

## Sample Responses

**HTTP 200 OK**

```json
{
  "status": "success",
  "summary": "Create dashboard",
  "data": {
    "dashboardId": "466206000000106002",
    "displayName": "Sales Overview"
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Dashboard](../../../sdk-examples/reports-and-dashboards/dashboards/create-dashboard.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

## Settings

Every flag below is optional. Boolean flags are stored as the strings `"true"` / `"false"`; the request
schema declares them as booleans, so JSON `true` / `false` is the form to send and is what the read API
returns as `"true"` / `"false"`.

Supplying a partial `settings` object writes **only** those keys — it does not merge with the defaults,
so unspecified flags fall back to whatever the dashboard renderer treats as unset rather than to the
values in the Default column.

| Field | Values | Default | Description |
|-------|--------|---------|-------------|
| `allowDrillDown` | `"true"` / `"false"` | `"true"` | Allow drill-down on chart data points. |
| `hideColumnOptions` | `"true"` / `"false"` | `"true"` | Hide column-level options from viewers. |
| `smartAlignCharts` | `"true"` / `"false"` | `"true"` | Auto-align chart elements across cards. |
| `enableSortMenu` | `"true"` / `"false"` | `"true"` | Show the sort menu on embedded reports. |
| `reportAsFilter` | `"true"` / `"false"` | `"false"` | Clicking a data point filters the other cards. |
| `showContextualOptions` | `"true"` / `"false"` | `"true"` | Show contextual action menus on cards. |
| `allowVUD` | `"true"` / `"false"` | `"true"` | Enable View Underlying Data on embedded reports. |
| `allowInsights` | `"true"` / `"false"` | `"true"` | Enable Zia Insights on embedded reports. |
| `allowEmbedInsights` | `"true"` / `"false"` | `"true"` | Enable Insights in embedded/published views. |
| `fitToWidth` | `"true"` / `"false"` | `"true"` | Scale embedded reports to the card width. |
| `enableGlobalUF` | `"true"` / `"false"` | `"false"` | Enable the global user filter. |
| `enableGlobalValueUF` | `"true"` / `"false"` | *(unset)* | Enable value-based global user filters. |
| `applyImmediateUF` | `"true"` / `"false"` | `"true"` | Apply user-filter changes without a confirm click. |
| `timeSlicer` | `"true"` / `"false"` | `"false"` | Enable the time-slicer widget. |
| `mapSync` | `"true"` / `"false"` | *(unset)* | Synchronise pan/zoom across map cards. |
| `layoutType` | `web` \| `custom_width` \| `tabloid_1056` \| `letter_816` \| `a4_797` \| `a3_1123` | `"web"` | Target page layout. **`mobile` is not a valid value.** |
| `layoutWidth` | String of 1–4 digits | `"1279"` | Fixed layout width in pixels. |
| `allowExport` | JSONObject | `"true"` (all formats) | Per-format export control. Sub-keys `csv`, `excel`, `html`, `image`, `pdf`, `zohoSheet`, each `"true"` / `"false"`. Any sub-key you omit is stored as `"false"`. |
| `allowAllExport` | `"true"` / `"false"` | — | Alias of `allowExport` used as a single master switch. |

## Themes

`themes` is a nested JSON object. Its shape is driven by `type`.

**Mode A — default theme.** Send `{"default": "true"}` (or `"unset"`). When `default` is present,
`type`, `solid`, `gradient`, `image`, `card`, `chartEffect` and `palette` must all be **absent**
(**7493** otherwise).

**Mode B — explicit theme.** `type` is mandatory and selects which sub-object is required:

| `type` | Required in the type object | Required in `card` | Must be absent |
|--------|-----------------------------|--------------------|----------------|
| `solid` | `background` | `background` | `gradient`, `image` |
| `gradient` | `background`, `startColor`, `endColor`, `mode` | `background`, `opacity`, `blur` | `solid`, `image` |
| `image` | `url`, `background` | `background`, `opacity`, `blur` | `solid`, `gradient` |

For `gradient`, exactly one of `linear` / `radial` must be present and it must match `mode` — supplying
both, neither, or the one that does not match `mode` raises **7492** / **7493**.

Accepted keys and their ranges:

| Key | Type / range |
|-----|--------------|
| `default` | `"true"` \| `"unset"` |
| `layoutType` | `1`–`6` |
| `type` | `solid` \| `gradient` \| `image` |
| `solid.background` | Colour |
| `gradient.background`, `gradient.startColor`, `gradient.endColor` | Colour |
| `gradient.mode` | `linear` \| `radial` |
| `gradient.linear.angle` | `-270`–`270` |
| `gradient.radial.x`, `gradient.radial.y` | `0`–`180` |
| `image.url` | External URL |
| `image.background` | Colour |
| `image.brightness`, `image.contrast` | `-100`–`100` |
| `image.transparency` | `0`–`100` |
| `image.flip` | Boolean |
| `image.fitType` | `1`–`3` |
| `font.color` | Colour |
| `font.family` | Letters, digits, spaces, apostrophes, hyphens; max 50 |
| `font.size` | `7`–`24` |
| `font.style` | `plain` \| `bold` \| `italic` |
| `card.background` | Colour |
| `card.opacity` | `0`–`1` decimal, e.g. `0.85` |
| `card.blur` | `0`–`50` |
| `card.radius` | `0`–`20` |
| `card.margin` | `0`–`10` |
| `card.shadow` | `1`–`3` |
| `card.paletteType` | `1`–`6` |
| `card.border.color` | Colour |
| `card.border.width` | `0`–`5` |
| `card.title.background` | Colour |
| `card.title.border.color` | Colour |
| `card.title.border.width` | `0`–`5` |
| `card.title.font.{color,family,size,style}` | As `font.*` |
| `card.desc.font.{color,family,size,style}` | As `font.*` |
| `chartEffect.apply` | `1` \| `2` — **mandatory** when `chartEffect` is present |
| `chartEffect.type` | `1`–`3` — forbidden when `apply` is `1` (**7513**), required when `apply` is `2` (**7514**) |

> **Colour format.** Only `#RRGGBB` or `#RGB` is accepted (`^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$`).
> 8-digit hex, `rgb()` and named colours are rejected with **8509**. A non-string colour value is
> likewise rejected with **8509**.

> **Border widths are not per-edge.** A single `card.border.width` (or `card.title.border.width`) is
> written to the left, right, top and bottom edges simultaneously.

> **`palette` is accepted but unsupported.** `themes.palette.*` passes schema validation and is written
> to storage, but the conditional validation for it is disabled in the current build. Do not depend on
> it.

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | A dashboard with this `displayName` already exists in the workspace. | Choose a different name. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The caller lacks Create Report permission on the workspace, or is calling from a white-label domain that is not mapped to this workspace. | Grant the permission, or call the standard data-centre domain. |
| [7309](../../../foundations/error-codes.md#error-7309) | 400 | `Authorization` header absent. | Send `Authorization: Zoho-oauthtoken <token>`. |
| [7479](../../../foundations/error-codes.md#error-7479) | 400 | A card is missing one or more of `type`, `width`, `height`, `left`, `top`. | Add the missing positional fields. |
| [7480](../../../foundations/error-codes.md#error-7480) | 400 | Negative offset, `width`/`height` of 1 or less, or `left + width > 80`. | Keep every card inside the 80-unit grid. |
| [7481](../../../foundations/error-codes.md#error-7481) | 400 | The referenced view exists but the caller cannot read it. | Have the view shared with the caller, or remove the card. |
| [7482](../../../foundations/error-codes.md#error-7482) | 400 | Two cards overlap. | Reposition so no two rectangles intersect. |
| [7483](../../../foundations/error-codes.md#error-7483) | 400 | A `HTML`, `TITLE`, `PARA`, `IMAGE` or `EMBED` card has absent, `null` or empty `content`. | Supply a non-empty `content` string. |
| [7484](../../../foundations/error-codes.md#error-7484) | 400 | More than 100 cards in the layout. | Split the dashboard. |
| [7485](../../../foundations/error-codes.md#error-7485) | 400 | Unrecognised card `type`. | Use one of the eight values in [Card types](overview.md#card-types). |
| [7486](../../../foundations/error-codes.md#error-7486) | 400 | A positional field has the wrong JSON type. | `width`, `height`, `left`, `top` must be integers; `type` must be a string. |
| [7487](../../../foundations/error-codes.md#error-7487) | 400 | `displayName` or `layout` is absent, `null` or empty. | Supply both. Remember `layout` is a JSON-encoded **string**. |
| [7488](../../../foundations/error-codes.md#error-7488) | 400 | A `settings` or `themes` key has an empty or `null` value, or an unrecognised key reached the server. | Remove the key or give it a valid value. |
| [7491](../../../foundations/error-codes.md#error-7491) | 400 | The sub-object required by `themes.type` is missing, or `card` is absent. | Add the required sub-object. |
| [7492](../../../foundations/error-codes.md#error-7492) | 400 | A required field inside the type sub-object or inside `card` is missing. | See the required-fields table in [Themes](#themes). |
| [7493](../../../foundations/error-codes.md#error-7493) | 400 | A sub-object belonging to a different theme type is present, or a forbidden key accompanies `default`. | Remove the conflicting key. |
| [7507](../../../foundations/error-codes.md#error-7507) | 400 | `displayName` exceeds 100 characters, or `description` exceeds 250. | Shorten the value. |
| [7510](../../../foundations/error-codes.md#error-7510) | 400 | `layout` is not parseable JSON, or a `themes` sub-object is `null`. | Validate the JSON you embed in the `layout` string; never send `null` for `card`, `solid`, `gradient` or `image`. |
| [7512](../../../foundations/error-codes.md#error-7512) | 400 | A card is smaller than the minimum for its type. | See the min height/width columns in [Card types](overview.md#card-types). |
| [7513](../../../foundations/error-codes.md#error-7513) | 400 | `chartEffect.type` supplied while `chartEffect.apply` is `1`. | Remove `type`, or set `apply` to `2`. |
| [7514](../../../foundations/error-codes.md#error-7514) | 400 | `chartEffect.apply` is `2` but `chartEffect.type` is absent. | Supply `chartEffect.type`. |
| [8027](../../../foundations/error-codes.md#error-8027) | 400 | One or more `VIEW` cards name a view that does not exist in this workspace, or `viewName` is absent / `null` / non-string. | Check the view display names. Matching is case-insensitive but the view must exist. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | The `CONFIG` parameter is missing from the request body. | Send `CONFIG` as a form-encoded parameter. |
| [8509](../../../foundations/error-codes.md#error-8509) | 400 | An enumerated or pattern-constrained value does not match — a malformed colour, an out-of-range number, `layoutType` outside 1–4, a non-string colour. | Check the ranges in [Themes](#themes) and [Settings](#settings). |
| [8517](../../../foundations/error-codes.md#error-8517) | 400 | A value has the wrong JSON data type for its schema declaration. | Match the declared types. |
| [8534](../../../foundations/error-codes.md#error-8534) | 400 | A theme sub-object was supplied as an array, or `CONFIG` is malformed JSON. | Use `{}` for objects. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Refresh the token with scope `ZohoAnalytics.modeling.create`. |
| [8542](../../../foundations/error-codes.md#error-8542) | 400 | An unknown key is present in `CONFIG`. | Only `displayName`, `description`, `layout`, `themes`, `settings`, `layoutType` are accepted. |
| [9001](../../../foundations/error-codes.md#error-9001) | 400 | Every card in the layout is a `USERFILTERS` card. | Add at least one content-bearing card. |

# Related

- [Dashboards overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Reports & Dashboards](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Read Dashboard Metadata](get-dashboard-metadata.md), [Update Dashboard](update-dashboard.md), [Get All Dashboards](get-dashboards.md), [Get Owned Dashboards](get-owned-dashboards.md), [Get Shared Dashboards](get-shared-dashboards.md).
- [SDK examples](../../../sdk-examples/reports-and-dashboards/dashboards/create-dashboard.md).
