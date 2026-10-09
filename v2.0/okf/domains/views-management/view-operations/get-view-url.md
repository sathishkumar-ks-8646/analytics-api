---
type: API Endpoint
title: Get View URL
description: Generates and returns the publicly accessible URL of a view.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - view-operations
  - get
  - embed
api:
  operation_id: getViewUrl
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish"
  domain: views-management
  group: view-operations
  oauth_scopes:
    - ZohoAnalytics.embed.read
  org_id_header: required
  config_parameter:
    location: query
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission or Make Public permission on the workspace."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 7319
    - 8060
    - 8061
    - 8062
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1publish/get"
    config_schema: GetViewUrlConfig
    response_schema: GetViewUrlResponse
  sdk_examples: "/sdk-examples/views-management/view-operations/get-view-url.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish`** - Get View URL (View Operations / Views Management).

Generates and returns the publicly accessible URL for a view. The URL can be opened directly in a browser without authentication, allowing the view to be shared externally. The URL reflects any visual customisations specified in CONFIG (theme, toolbar, legend position, etc.) and optionally applies a data filter via `criteria`.

> **Two URL forms are returned depending on whether the view has a private key configured:**
> - **Public URL:** `https://analytics.zoho.com/open-view/<view-id>?ZDB_THEME_NAME=<theme>` — accessible by anyone with the link.
> - **Private key URL:** `https://analytics.zoho.com/open-view/<view-id>/<private-key>?ZDB_THEME_NAME=<theme>` — only accessible to users who also possess the private key.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getViewUrl` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.embed.read`](../../../foundations/oauth-scopes.md#zohoanalyticsembedread) |
| ZANALYTICS-ORGID header | **Required** - Organization ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission or Make Public permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - optional |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1publish/get`; CONFIG schema `GetViewUrlConfig`; response schema `GetViewUrlResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.embed.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameter

The CONFIG parameter is optional. When provided, it is a JSON object passed as a **query parameter** named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `theme` | String | No | `"blue"` | The visual theme applied to the view in the URL. The theme name is appended as `?ZDB_THEME_NAME=<theme>` in the generated URL. Common values: `blue` (default), `bluedark`, `grey`, `green`, `violet`, `fire`, `tango`, `contrast`. |
| `includeTitle` | Boolean | No | `true` | When `true` (default): the view title is rendered in the shared page. When `false`: the title bar is hidden, giving more vertical space to the view content. |
| `includeDesc` | Boolean | No | `true` | When `true` (default): the view description is shown below the title. When `false`: the description is hidden. |
| `includeToolBar` | Boolean | No | `false` | When `false` (default): the toolbar (which includes export, share, and other action buttons) is hidden for a cleaner read-only appearance. When `true`: the toolbar is shown, allowing the viewer to interact with export and other toolbar functions. |
| `includeSearchBox` | Boolean | No | `false` | **Applies to Tables and Tabular Views only. Ignored for charts, pivots, dashboards.** When `false` (default): no search box is shown. When `true`: a search/filter box is shown above the table, allowing viewers to perform keyword searches within the displayed data. |
| `includeDatatypeSymbol` | Boolean | No | `false` | **Applies to Tables and Tabular Views only.** When `false` (default): column headers show only the column name. When `true`: a data type symbol (icon) is displayed next to each column name, helping viewers understand the column type (text, number, date, etc.) at a glance. |
| `includeShowHideOption` | Boolean | No | `false` | **Applies to Tables and Tabular Views only.** When `false` (default): viewers cannot toggle column visibility. When `true`: a column visibility toggle button appears, allowing viewers to show or hide specific columns without needing edit access. |
| `legendPosition` | String | No | `null` (view default) | **Applies to Chart (Analysis) Views only. Ignored for tables, dashboards, pivots.** Controls where the chart legend is placed. Allowed values: `top`, `bottom`, `left`, `right`, `hidden` (no legend), `float` (overlay on chart). When omitted, the position configured in the view's saved settings is used. |
| `criteria` | String | No | `null` | A Zoho Analytics filter criteria string applied as a data filter on the URL. Filters the data shown when the URL is opened — the viewer sees only the filtered subset. Example: `"\"Region\"='East'"`. The criteria is encoded and appended as a `CRITERIA` URL parameter. When omitted, all data is shown. The criteria must reference columns that exist in the view. |
| `withCustomDomain` | Boolean | No | `false` | When `false` (default): the URL uses the standard `analytics.zoho.com` domain. When `true`: if the workspace has a custom client portal domain configured, the URL is generated using that custom domain instead. Requires the workspace to have a custom domain set up; if not configured, request fails with error **8062**. Use `domainName` for explicit domain specification instead of this flag when possible. |
| `domainName` | String | No | `null` | Explicitly specifies the custom domain to use in the generated URL. When provided, takes precedence over `withCustomDomain`. Must be a valid custom domain configured for the workspace. If the specified domain does not exist, request fails with error **8060**. If the domain exists but does not belong to the workspace/user, fails with error **8061**. |

## Notes from the OpenAPI specification

- The CONFIG parameter is optional. Without it, the URL is generated with the default theme and the default display settings. As this is a GET request, the value must be stringified and URL encoded before it is sent.
- The generated URL opens directly in a browser without authentication, which is what makes the view shareable outside Zoho Analytics.
- When the view is made public with a private key, the key is embedded in the URL path as **/open-view/<view-id>/<private-key>**. Such a URL is reachable only by someone holding the key, and opening it without the key segment returns an access-denied page.
- **includeSearchBox**, **includeDatatypeSymbol** and **includeShowHideOption** apply to Tables and Tabular Views only. They are silently ignored for charts, pivot tables and dashboards.
- **legendPosition** applies to chart, or analysis, views only and is silently ignored for tables, pivot tables and dashboards. When it is omitted, the legend position saved in the view's own settings is used.
- **criteria** must reference columns that exist in the view. A column that does not exist fails filter criteria validation before the URL is generated.
- **domainName** takes precedence over **withCustomDomain** and is the preferred way to select a custom domain. A domain that does not exist fails with error 8060, and one that exists but does not belong to the workspace or the calling user fails with error 8061.
- **withCustomDomain** as true on a workspace that has no custom domain configured fails with error 8062. Configure the domain first, or omit the attribute to use the standard domain.
- Passing a tabbed dashboard generates a URL for the dashboard as a whole, and the display attributes apply to the dashboard frame. Configuring an individual tab is not exposed through this API.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

# Examples

## Sample Requests

**Case 1 — Get the basic public URL with default theme**

```http
GET /restapi/v2/workspaces/466206000000071000/views/466206000000105001/publish HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — URL with green theme, no toolbar, criteria filter**

```http
GET /restapi/v2/workspaces/466206000000071000/views/466206000000105001/publish?CONFIG={"theme":"green","includeTitle":true,"includeDesc":false,"includeToolBar":false,"criteria":"\"Region\"='East'"} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — Table URL with search box and data type symbols**

```http
GET /restapi/v2/workspaces/466206000000071000/views/466206000000105003/publish?CONFIG={"includeSearchBox":true,"includeDatatypeSymbol":true,"includeShowHideOption":true} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Standard public URL**
```json
{
  "status": "success",
  "summary": "Get view URL",
  "data": {
    "viewUrl": "https://analytics.zoho.com/open-view/466206000000105001?ZDB_THEME_NAME=blue"
  }
}
```

**Case 2 — URL with green theme and region filter**
```json
{
  "status": "success",
  "summary": "Get view URL",
  "data": {
    "viewUrl": "https://analytics.zoho.com/open-view/466206000000105001?ZDB_THEME_NAME=green&INCLUDEDESC=false&CRITERIA=%22Region%22%3D%27East%27"
  }
}
```

**Case 3 — View with private key configured (requires key in URL to access)**
```json
{
  "status": "success",
  "summary": "Get view URL",
  "data": {
    "viewUrl": "https://analytics.zoho.com/open-view/466206000000105001/d7f69c7581b1974af438b42c4aaaed98?ZDB_THEME_NAME=blue"
  }
}
```

> **Difference between Case 1 and Case 3:** When a view's public access is configured with a private key (Make Public with key), the key is embedded in the URL path. This URL is only accessible to users who have the correct key. Without the key segment, the URL returns an access-denied page.

| Response Field | Type | Description |
|----------------|------|-------------|
| `data.viewUrl` | String | The complete, ready-to-use URL. Open this directly in a browser. The URL includes all visual customisations and filter criteria as query parameters. |

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get View URL](../../../sdk-examples/views-management/view-operations/get-view-url.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | View not found. | Verify `<view-id>` exists in the workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have Publish or Make Public permission on the workspace. | Ensure the user is a Workspace Admin, Account Admin, Organization Admin, or has been granted Publish or Make Public permission. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | View does not belong to the specified workspace. | Verify both `<workspace-id>` and `<view-id>` are consistent. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | The specified `domainName` does not exist. | Provide a valid custom domain name configured for the workspace. |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | The specified domain does not belong to the workspace or the calling user. | Use a domain that is associated with the workspace. |
| [8062](../../../foundations/error-codes.md#error-8062) | 400 | `withCustomDomain=true` but no custom domain is configured for this workspace. | Configure a custom domain for the workspace first, or use the standard URL by omitting `withCustomDomain`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.embed.read`. |

# Related

- [View Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Save As View](save-as-view.md), [Copy Views](copy-views.md), [Create Similar Views](create-similar-views.md), [Rename View](rename-view.md), [Delete View](delete-view.md), [Get View List](get-views.md), [Get View Details](get-view-details.md), [Get View Dependents](get-view-dependents.md), [Get Recent Views](get-recent-views.md).
- [SDK examples](../../../sdk-examples/views-management/view-operations/get-view-url.md).
