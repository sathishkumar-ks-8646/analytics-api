---
type: API Endpoint
title: Update Publish Configurations
description: "Updates the presentation configuration of the view's published page — title, description, toolbar, search box, dimensions, auto-refresh interval, legend position, URL-level criteria, Ask Zia — and, when the workspace is public, its public-listing flag."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - publish
  - put
  - embed
api:
  operation_id: updatePublishConfigurations
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config"
  domain: share-and-publish
  group: publish
  oauth_scopes:
    - ZohoAnalytics.embed.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission on the view, or any user with Make Public permission on the view."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 7319
    - 7565
    - 8054
    - 8080
    - 8152
    - 8154
    - 8241
    - 8535
  openapi:
    file: "/references/openapi/share-publish-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1publish~1config/put"
    config_schema: UpdatePublishConfigurationsConfig
    response_schema: null
  sdk_examples: "/sdk-examples/share-and-publish/publish/update-publish-configurations.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/share-publish-grouped-api.json"
    title: OpenAPI 3 specification - share-publish-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

**PUT `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config`** - Update Publish Configurations (Publish / Share & Publish).

Updates the **presentation configuration** of the view's published page — title, description, toolbar, search box, dimensions, auto-refresh interval, legend position, URL-level criteria, Ask Zia — and, when the workspace is public, its public-listing flag.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `updatePublishConfigurations` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.embed.update`](../../../foundations/oauth-scopes.md#zohoanalyticsembedupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission on the view, or any user with Make Public permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1publish~1config/put`; CONFIG schema `UpdatePublishConfigurationsConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.embed.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

> **This API replaces the whole configuration — it is not a patch.** Every field below is rewritten on every call, and any field you omit is reset to the Default listed here. Always read the current state with [Get Publish Configurations](get-publish-configurations.md), merge your change into it, and send the complete object back.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `URLCriteria` | String | No | `""` (cleared) | Row-level filter criteria applied when the published page is rendered, e.g. `"Sales_1"."Region"='West'`. Validated against the view's involved columns (`8054` / `8154`). Omitting it or sending `""` **clears** any previously configured criteria. Distinct from the share-level `criteria` of [Make View Public](make-views-public.md) / [Create Private URL](create-private-url.md). |
| `includeTitle` | Boolean | No | `true` | Render the view's title on the published page. |
| `includeDesc` | Boolean | No | `true` | Render the view's description on the published page. |
| `includeToolBar` | Boolean | No | `false` | Render the toolbar on the published page. |
| `includeSearchBox` | Boolean | No | `true` | Render a search box. Effective for table-type views and tabular reports only. |
| `includeDatatypeSymbol` | Boolean | No | `false` | Show each column's data-type symbol in the header. Table-type views and tabular reports only. |
| `includeShowHideOption` | Boolean | No | `false` | Let the visitor show/hide columns. Table-type views and tabular reports only. |
| `includeSocialWidgets` | Boolean | No | `false` | Render social share widgets. |
| `includeAskZia` | Boolean | No | `false` | Make the Ask Zia conversational-analytics widget available on the published page. |
| `isInteractive` | Boolean | No | `true` | Render a chart interactively (hover, tooltips, zoom). **Only honoured for chart views** — for every other view type the stored value is forced to `true` regardless of what is sent. |
| `legendPosition` | String | No | `"RIGHT"` | Legend placement for chart views, as an uppercase alphabetic keyword (the API validates only that the value is alphabetic; use the legend positions supported by the chart type, e.g. `RIGHT`). Ignored for non-chart views. |
| `width` | Long | No | `800` | Rendering width in pixels. |
| `height` | Long | No | `600` | Rendering height in pixels. |
| `autoRefresh` | Long | No | `-1` | Auto-refresh interval in **seconds**. `-1` disables auto-refresh. Any other value must be **at least 120** — smaller positive values are rejected with `8152`. |
| `isListed` | Boolean | No | — (unchanged) | Whether the workspace's public views appear in Zoho Analytics' public listing. Only applied when the workspace is currently public; otherwise ignored. On the Free plan (excluding CRM Plus Starter) it is **forced to `true`** and cannot be turned off. This is the only field that is left untouched when omitted. |
| `validateSystemTags` | Boolean | No | `true` | If `true`, the request is blocked with a confirmation-required error (`8241`) when the view carries a restricted **DATA_WARNING** system tag. Pass `false` to acknowledge the warning and update anyway. |

## Notes from the OpenAPI specification

- Only the attributes sent in the config are updated; the ones omitted retain their current values.
- `autoRefresh` takes the interval in minutes. Send `-1` to disable the automatic refresh.
- `isListed` applies to the workspace, not to the individual view.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`). To read the resulting configuration, call [Get Publish Configurations](get-publish-configurations.md).

# Examples

## Sample Requests

**Case 1 — `URLCriteria` only: filter the published page to a single region**

```http
PUT /restapi/v2/workspaces/137687000271334001/views/137687000006991601/publish/config HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "URLCriteria": "\"Sales_1\".\"Region\"='West'"
}
```

**Case 2 — Table-view presentation options clubbed together: chrome, search box, data-type symbols, show/hide, dimensions, auto-refresh**

```http
PUT /restapi/v2/workspaces/137687000271334001/views/137687000006991601/publish/config HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "includeTitle": true,
    "includeDesc": false,
    "includeToolBar": true,
    "includeSearchBox": true,
    "includeDatatypeSymbol": true,
    "includeShowHideOption": true,
    "includeSocialWidgets": false,
    "includeAskZia": true,
    "width": 1200,
    "height": 800,
    "autoRefresh": 300
}
```

**Case 3 — Chart-view options clubbed together: interactivity, legend placement, and public listing**

```http
PUT /restapi/v2/workspaces/137687000271334001/views/137687000006991650/publish/config HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "isInteractive": true,
    "legendPosition": "BOTTOM",
    "includeTitle": true,
    "includeDesc": true,
    "width": 1000,
    "height": 700,
    "isListed": false
}
```

**Case 4 — White Label / Client Portal: minimal chrome for embedding in a portal page**

```http
PUT /restapi/v2/workspaces/137687000271334009/views/137687000006991777/publish/config HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "URLCriteria": "\"WL_Table\".\"Region\"='West'",
    "includeTitle": false,
    "includeDesc": false,
    "includeToolBar": false,
    "includeSocialWidgets": false,
    "includeAskZia": false,
    "width": 900,
    "height": 500,
    "validateSystemTags": false
}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code, then read the applied state back with [Get Publish Configurations](get-publish-configurations.md).

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — Auto-refresh interval below the minimum**

```json
{
    "status": "failure",
    "summary": "INTERVAL_SHOULD_BE_120_OR_ABOVE",
    "data": {
        "errorCode": 8152,
        "errorMessage": "Refresh interval should be 120 seconds or above."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Update Publish Configurations](../../../sdk-examples/share-and-publish/publish/update-publish-configurations.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Update Publish Configurations returns a bare HTTP `204 No Content` — no `status`/`summary` JSON to parse. |
| **Full replace, not a patch** | The stored configuration is rebuilt from scratch on every call. Omitted fields fall back to the defaults in the CONFIG table above and **overwrite** whatever was stored before. Sending `{"includeTitle": true}` alone therefore also resets `width`, `height`, `autoRefresh`, `legendPosition`, `URLCriteria`, and every `include*` flag. `isListed` is the sole exception — it is only touched when present. |
| **Read-default vs. write-default asymmetry** | `includeSearchBox` defaults to `false` when read from a never-updated view but to `true` here; `includeAskZia` defaults to `true` when read but to `false` here. A bare update call visibly flips both. Always send them explicitly. |
| **`isInteractive` is forced for non-chart views** | For anything other than a chart view, the stored value is `true` no matter what is sent — tables, pivots, summaries, and dashboards are always interactive. |
| **`autoRefresh` has a hard floor** | Only `-1` (off) or values ≥ `120` seconds are accepted; anything in between fails with `8152`. |
| **`URLCriteria` is cleared by omission** | Because the configuration is rebuilt, omitting `URLCriteria` (or sending `""`) removes any criteria previously attached to the published URL. To keep it, resend it. |
| **`URLCriteria` ≠ share-level `criteria`** | `URLCriteria` is a URL parameter evaluated when the page renders and applies to *both* the public and private channels. The `criteria` field of [Make View Public](make-views-public.md) / [Create Private URL](create-private-url.md) is a per-channel share filter stored against the `Public Visitor` / `Private Link` pseudo-user. Both can be active at once and both then apply. |
| **`isListed` only bites on public workspaces** | The flag is applied only when the workspace itself is currently public; on a non-public workspace it is accepted and ignored. On the Free plan it is coerced to `true`. |
| **Applies to every publish channel** | The same configuration drives the public URL, the private URL, and the embed URL for this view — there is no per-channel presentation configuration. |
| **Dependency chain** | [Get Publish Configurations](get-publish-configurations.md) (read current state) → merge → Update Publish Configurations → [Get Publish Configurations](get-publish-configurations.md) (verify). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — View not found. | Verify `<view-id>` exists. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user has neither Publish nor Make Public permission on the view. | Ensure the user is an Account Admin, Organization Admin, Workspace Admin, or has Publish / Make Public permission on the view. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The view does not belong to the specified workspace. | Ensure `<workspace-id>` and `<view-id>` are consistent. |
| [7565](../../../foundations/error-codes.md#error-7565) | 400 | `UNVERIFIED_EMAIL` — The calling user's primary email address is not verified. | Verify the account's primary email address and retry. |
| [8054](../../../foundations/error-codes.md#error-8054) | 400 | `INVALID_FILTER_CRITERIA` — `URLCriteria` could not be parsed. | Correct the criteria syntax (e.g. `"Table"."Column"='Value'`). |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — CONFIG is not valid JSON, contains an unsupported key, or violates a type constraint (e.g. a non-alphabetic `legendPosition`). | Send only the documented keys with the documented types. |
| [8152](../../../foundations/error-codes.md#error-8152) | 400 | `INTERVAL_SHOULD_BE_120_OR_ABOVE` — `autoRefresh` is a positive value below 120 seconds. | Use `-1` to disable auto-refresh, or a value of at least `120`. |
| [8154](../../../foundations/error-codes.md#error-8154) | 400 | `COLUMN_NOT_PRESENT_IN_TABLE` — A column referenced in `URLCriteria` does not exist. | Verify column names via [Get Columns](../../data-modeling-and-schema/columns/overview.md). |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | `SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION` — The view carries a restricted DATA_WARNING system tag. | Review the warning, then resend with `"validateSystemTags": false` to confirm. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.embed.update`. |

# Related

- [Publish overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Make View Public](make-views-public.md), [Remove Public Permission](remove-public-permission.md), [Get Private URL](get-private-url.md), [Create Private URL](create-private-url.md), [Remove Private Access](remove-private-access.md), [Get Publish Configurations](get-publish-configurations.md).
- [SDK examples](../../../sdk-examples/share-and-publish/publish/update-publish-configurations.md).
