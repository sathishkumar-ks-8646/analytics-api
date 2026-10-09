---
type: API Endpoint
title: Get Publish Configurations
description: "Returns the complete publish state of a view in one call: the public channel's audience and listing state, the private channel's password/expiry state, and the presentation configuration used to render the published page."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - publish
  - get
  - embed
api:
  operation_id: getPublishConfigurations
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config"
  domain: share-and-publish
  group: publish
  oauth_scopes:
    - ZohoAnalytics.embed.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission on the view, or any user with Make Public permission on the view."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 7319
    - 8535
  openapi:
    file: "/references/openapi/share-publish-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1publish~1config/get"
    config_schema: null
    response_schema: GetPublishConfigurationsResponse
  sdk_examples: "/sdk-examples/share-and-publish/publish/get-publish-configurations.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/share-publish-grouped-api.json"
    title: OpenAPI 3 specification - share-publish-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config`** - Get Publish Configurations (Publish / Share & Publish).

Returns the complete publish state of a view in one call: the **public** channel's audience and listing state, the **private** channel's password/expiry state, and the **presentation configuration** used to render the published page.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getPublishConfigurations` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.embed.read`](../../../foundations/oauth-scopes.md#zohoanalyticsembedread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission on the view, or any user with Make Public permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1publish~1config/get`; response schema `GetPublishConfigurationsResponse` |

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

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get publish configurations"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.publicViewConfig` | JSONObject | Public-channel state. **Present only if the caller has Make Public permission on the workspace** — absent otherwise. |
| `publicViewConfig.publicPermLevel` | Number | Current public audience of the view: `0` = not public, `1` = Public (anyone with the link), `2` = Organization Public, `3` = Business Organization Public. See [`publicPermLevel` Values](make-views-public.md#publicpermlevel-values). |
| `publicViewConfig.isListed` | Boolean | `true` when the workspace's public views are discoverable in Zoho Analytics' public listing. Forced to `true` and not editable on the Free plan (and non-CRM-Plus-Starter free tiers). Settable via [Update Publish Configurations](update-publish-configurations.md) only while the workspace is public. |
| `publicViewConfig.isOrgPublicAllowed` | Boolean | `true` when `publicPermLevel: "2"` (Organization Public) may be requested. `false` on the Free plan and in Client Portal / White Label (custom-domain) contexts. |
| `publicViewConfig.orgName` | String | Display name of the Zoho Analytics organization that owns the workspace — used to label the "Organization Public" audience in a UI. |
| `publicViewConfig.isBussOrgPublicAllowed` | Boolean | `true` when `publicPermLevel: "3"` (Business Organization Public) may be requested. Requires a paid plan, a non-custom-domain context, and the caller to belong to the same business organization as the workspace's Account Admin. |
| `publicViewConfig.businessOrgName` | String | Display name of the parent business organization. Empty string `""` when `isBussOrgPublicAllowed` is `false`. |
| `data.privateLinkConfig` | JSONObject | Private-channel state. **Present only if private links are permitted for this organization/workspace *and* the caller has Publish permission on the workspace** — absent otherwise (see the Free-plan sample above). |
| `privateLinkConfig.isPrivate` | Boolean | `true` when the view currently has a private link (a private key exists). |
| `privateLinkConfig.isExpired` | Boolean | `true` when an expiry date is set and has already passed. Always `false` when no expiry date is configured. |
| `privateLinkConfig.password` | String | The private link's password **in clear text**, or the sentinel `"-1"` when no password is set. Treat this field as sensitive and never log or surface it to unauthorised users. |
| `privateLinkConfig.expiryDate` | String | The expiry date in `dd/MM/yyyy` format (GMT), or the sentinel `"-1"` when the link never expires. |
| `data.publishConfig` | JSONObject | Presentation configuration of the published page. **Always present**, for every caller. Shared by the public URL, the private URL, and the embed URL. |
| `publishConfig.includeTitle` | Boolean | Whether the view's title is rendered on the published page. |
| `publishConfig.includeDesc` | Boolean | Whether the view's description is rendered on the published page. |
| `publishConfig.includeToolBar` | Boolean | Whether the toolbar is rendered. Stored internally as its inverse (`REMTOOLBAR`); the API always presents the positive `includeToolBar` form. |
| `publishConfig.includeSocialWidgets` | Boolean | Whether social share widgets are rendered. |
| `publishConfig.includeSearchBox` | Boolean | Whether a search box is rendered. Applies to table-type views and tabular reports only; ignored for charts and dashboards. |
| `publishConfig.includeDatatypeSymbol` | Boolean | Whether each column header shows its data-type symbol. Table-type views and tabular reports only. |
| `publishConfig.includeShowHideOption` | Boolean | Whether the visitor can show/hide columns. Table-type views and tabular reports only. |
| `publishConfig.isInteractive` | Boolean | Whether the published chart is interactive (hover, tooltips, zoom) rather than a static rendering. Meaningful for chart views only — **always `true` for every other view type**. |
| `publishConfig.legendPosition` | String | Legend placement for chart views, as an uppercase alphabetic keyword. `"RIGHT"` is the default returned when nothing has been configured. Ignored for non-chart views. |
| `publishConfig.width` | Number | Rendering width in pixels. Default `800`. |
| `publishConfig.height` | Number | Rendering height in pixels. Default `600`. |
| `publishConfig.autoRefresh` | Number | Auto-refresh interval in **seconds**. `-1` means no auto-refresh (the default). Any other value is at least `120`. |
| `publishConfig.URLCriteria` | String | Row-level filter criteria applied as a URL parameter when the published page is rendered. Empty string `""` when none is configured. **Distinct from** the share-level `criteria` set by [Make View Public](make-views-public.md) / [Create Private URL](create-private-url.md). |
| `publishConfig.includeAskZia` | Boolean | Whether the Ask Zia conversational-analytics widget is available on the published page. |

## Notes from the OpenAPI specification

- In `privateLinkConfig`, a `password` or `expiryDate` of `-1` means that no password or validity period is set.
- `legendPosition` and `includeShowHideOption` are returned by this API but cannot be set through Update Publish Configurations.

# Examples

## Sample Requests

**Case 1 — Standard workspace**

```http
GET /restapi/v2/workspaces/137687000271334001/views/137687000006991601/publish/config HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal workspace**

```http
GET /restapi/v2/workspaces/137687000271334009/views/137687000006991777/publish/config HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK — Paid organization, view not yet published (Case 1)**

```json
{
    "status": "success",
    "summary": "Get publish configurations",
    "data": {
        "publicViewConfig": {
            "publicPermLevel": 0,
            "isListed": false,
            "isOrgPublicAllowed": true,
            "orgName": "AcmeAnalytics",
            "isBussOrgPublicAllowed": false,
            "businessOrgName": ""
        },
        "privateLinkConfig": {
            "isPrivate": false,
            "isExpired": false,
            "password": "-1",
            "expiryDate": "-1"
        },
        "publishConfig": {
            "includeTitle": true,
            "includeDesc": true,
            "includeToolBar": false,
            "includeSocialWidgets": false,
            "includeSearchBox": false,
            "includeDatatypeSymbol": false,
            "includeShowHideOption": false,
            "isInteractive": true,
            "legendPosition": "RIGHT",
            "width": 800,
            "height": 600,
            "autoRefresh": -1,
            "URLCriteria": "",
            "includeAskZia": true
        }
    }
}
```

**HTTP 200 OK — Private link active with a password (after [Create Private URL](create-private-url.md) Case 3)**

```json
{
    "status": "success",
    "summary": "Get publish configurations",
    "data": {
        "publicViewConfig": {
            "publicPermLevel": 0,
            "isListed": false,
            "isOrgPublicAllowed": true,
            "orgName": "AcmeAnalytics",
            "isBussOrgPublicAllowed": false,
            "businessOrgName": ""
        },
        "privateLinkConfig": {
            "isPrivate": true,
            "isExpired": false,
            "password": "Qwertyui",
            "expiryDate": "20/11/2030"
        },
        "publishConfig": {
            "includeTitle": true,
            "includeDesc": true,
            "includeToolBar": false,
            "includeSocialWidgets": false,
            "includeSearchBox": false,
            "includeDatatypeSymbol": false,
            "includeShowHideOption": false,
            "isInteractive": true,
            "legendPosition": "RIGHT",
            "width": 800,
            "height": 600,
            "autoRefresh": -1,
            "URLCriteria": "",
            "includeAskZia": true
        }
    }
}
```

**HTTP 200 OK — Free plan: `privateLinkConfig` is omitted and `isListed` is forced to `true`**

```json
{
    "status": "success",
    "summary": "Get publish configurations",
    "data": {
        "publicViewConfig": {
            "publicPermLevel": 0,
            "isListed": true,
            "isOrgPublicAllowed": false,
            "orgName": "AcmeFreeOrg",
            "isBussOrgPublicAllowed": false,
            "businessOrgName": ""
        },
        "publishConfig": {
            "includeTitle": true,
            "includeDesc": true,
            "includeToolBar": false,
            "includeSocialWidgets": false,
            "includeSearchBox": false,
            "includeDatatypeSymbol": false,
            "includeShowHideOption": false,
            "isInteractive": true,
            "legendPosition": "RIGHT",
            "width": 800,
            "height": 600,
            "autoRefresh": -1,
            "URLCriteria": "",
            "includeAskZia": true
        }
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Publish Configurations](../../../sdk-examples/share-and-publish/publish/get-publish-configurations.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Two of the three blocks are conditional** | `publicViewConfig` appears only when the caller has Make Public permission on the workspace; `privateLinkConfig` appears only when private links are permitted **and** the caller has Publish permission on the workspace. `publishConfig` is always present. Code defensively — do not assume all three keys exist. |
| **`publicPermLevel: 0` is a read-only sentinel** | `0` (not public) is returned by this API but is **not** a valid input to [Make View Public](make-views-public.md), whose `publicPermLevel` accepts only `1`, `2`, or `3`. To move a view to "not public", call [Remove Public Permission](remove-public-permission.md). |
| **`password` is returned in clear text** | The private-link password is decrypted for this response. This is by design (so an admin UI can display it), but it makes the response sensitive — avoid logging it and restrict who may call this API. |
| **`"-1"` sentinels, not `null`** | `privateLinkConfig.password` and `privateLinkConfig.expiryDate` are the string `"-1"` when unset — never `null` and never absent while `privateLinkConfig` itself is present. |
| **Defaults reported before the first update differ from update-time defaults** | Until [Update Publish Configurations](update-publish-configurations.md) has been called for the view, no publish data is stored and this API reports its own read-time defaults — notably `includeSearchBox: false` and `includeAskZia: true`. The update API's own defaults for those two fields are the opposite (`true` and `false` respectively), so a bare update call visibly flips them. See the [Update Publish Configurations notes](make-views-public.md#notes--behaviour). |
| **Reflects both channels at once** | A view can be simultaneously public and private-linked; `publicViewConfig.publicPermLevel > 0` and `privateLinkConfig.isPrivate: true` can both hold in the same response. |
| **Custom-domain handling of `URLCriteria` is transparent** | Internally the criteria is stored under a different key for portal domains than for the Zoho Analytics domain, but this API normalises both to `URLCriteria` — callers see one field regardless of context. |
| **No email-verification requirement** | Unlike the mutating publish APIs, this read-only API does not require the caller's primary email to be verified. |
| **Dependency chain** | [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>` → Get Publish Configurations (then decide which publish API to call). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — View not found. | Verify `<view-id>` exists. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user has neither Publish nor Make Public permission on the view. | Ensure the user is an Account Admin, Organization Admin, Workspace Admin, or has Publish / Make Public permission on the view. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The view does not belong to the specified workspace. | Ensure `<workspace-id>` and `<view-id>` are consistent. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.embed.read`. |

# Related

- [Publish overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Make View Public](make-views-public.md), [Remove Public Permission](remove-public-permission.md), [Get Private URL](get-private-url.md), [Create Private URL](create-private-url.md), [Remove Private Access](remove-private-access.md), [Update Publish Configurations](update-publish-configurations.md).
- [SDK examples](../../../sdk-examples/share-and-publish/publish/get-publish-configurations.md).
