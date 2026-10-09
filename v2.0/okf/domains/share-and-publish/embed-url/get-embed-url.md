---
type: API Endpoint
title: Get Embed URL
description: Returns an embed URL through which the specified view can be accessed.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embed"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - embed-url
  - get
  - embed
api:
  operation_id: getEmbedUrl
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embed"
  domain: share-and-publish
  group: embed-url
  oauth_scopes:
    - ZohoAnalytics.embed.read
  org_id_header: required
  config_parameter:
    location: query
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission or Make Public permission on the view. A caller who is not a workspace owner must additionally be listed in the organization's OEM-enabled users configuration, otherwise 7301. In every case the organization or the workspace must be enabled for Embedded Analytics, otherwise 8023."
  error_codes:
    - 7103
    - 7104
    - 7138
    - 7301
    - 7319
    - 8023
    - 8054
    - 8060
    - 8061
    - 8080
    - 8154
    - 8177
    - 8241
    - 8535
    - 9102
    - 12052
  openapi:
    file: "/references/openapi/share-publish-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1publish~1embed/get"
    config_schema: GetEmbedUrlConfig
    response_schema: GetEmbedUrlResponse
  sdk_examples: "/sdk-examples/share-and-publish/embed-url/get-embed-url.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/share-publish-grouped-api.json"
    title: OpenAPI 3 specification - share-publish-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embed`** - Get Embed URL (Embed URL / Share & Publish).

Mints a new, short-lived embed URL for a view. Everything the eventual viewer can see and do — which rows, which columns, whether they can export or drill — is fixed at the moment of this call and baked into the URL's stored configuration. The URL requires no sign-in.

From the OpenAPI specification:

Returns an embed URL through which the specified view can be accessed. The generated URL is short-lived, which adds more security to it. It does not require a login, and what the viewer can see and do is governed entirely by the permissions, filter criteria, and column restrictions sent in the config.

> **Note:** This API is available only to Embedded Analytics customers.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getEmbedUrl` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embed` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.embed.read`](../../../foundations/oauth-scopes.md#zohoanalyticsembedread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission or Make Public permission on the view. A caller who is not a workspace owner must additionally be listed in the organization's OEM-enabled users configuration, otherwise 7301. In every case the organization or the workspace must be enabled for Embedded Analytics, otherwise 8023. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - optional |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1publish~1embed/get`; CONFIG schema `GetEmbedUrlConfig`; response schema `GetEmbedUrlResponse` |

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

CONFIG is **optional**. Because this is a `GET`, it must be passed as a **query parameter** whose value is the stringified, **URL-encoded** JSON object. Omitting CONFIG returns a read-only embed URL with a one-hour validity.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `criteria` | String | No | — (no filter) | Row-level filter criteria applied to **this URL only**, e.g. `"Sales_1"."Region"='West'`. This is the primary multi-tenant mechanism: issue one embed URL per customer, each with a `criteria` that scopes it to that customer's rows. Validated against the view's involved columns (`8054` / `8154`) and stored **encrypted**. Max 250,000 characters. |
| `permissions` | JSONObject | No | `read: true`, everything else `false` | Read-only permission set carried by the URL. See [`permissions` Fields](#permissions-fields). |
| `vudColumns` | JSONArray | No | — | **Include model.** Applies only when `permissions.vud` is `true`. Restricts "View Underlying Data" to exactly the listed columns. 1–100 entries. See [`vudColumns` / `drillColumns` Fields](#vudcolumns--drillcolumns-fields). |
| `vudColumnsToExclude` | JSONArray | No | — | **Exclude model.** Applies only when `permissions.vud` is `true`. Hides exactly the listed columns from "View Underlying Data" and shows the rest. Same shape as `vudColumns`. When both are sent, the **exclude** model wins. |
| `drillColumns` | JSONArray | No | — | **Include model.** Applies only when `permissions.drillDown` is `true`. Restricts drill-down to exactly the listed columns. 1–100 entries. Same shape as `vudColumns`. |
| `drillColumnsToExclude` | JSONArray | No | — | **Exclude model.** Applies only when `permissions.drillDown` is `true`. Excludes exactly the listed columns from drill-down. When both are sent, the **exclude** model wins. |
| `validityPeriod` | Long | No | `3600` | How long the URL stays usable, in **seconds**, counted from the moment of this call. The default is one hour (`3600`) and the maximum is **86400 seconds (1 day)**. A larger value fails with `8177`. |
| `domainName` | String | No | — | Client Portal / White Label domain on which to build the returned URL. Only usable by a Client Portal admin of the workspace, calling from the standard API host — see [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). Max 200 characters. |
| `withCustomDomain` | Boolean | No | `false` | **Legacy flag.** Builds the URL on the workspace's configured portal domain without naming it. Requires the caller to be an Organization Admin or Super Admin **and** a Client Portal admin of the workspace. Prefer `domainName`. |
| `includeTitle` | Boolean | No | `true` | Whether the view's title is rendered inside the iframe. |
| `includeDesc` | Boolean | No | `true` | Whether the view's description is rendered inside the iframe. |
| `includeToolBar` | Boolean | No | `false` | Whether the toolbar is rendered inside the iframe. |
| `includeSearchBox` | Boolean | No | `false` | Whether a search box is rendered. Honoured **only for table-type views and tabular reports**; silently ignored for charts and dashboards. |
| `includeDatatypeSymbol` | Boolean | No | `false` | Whether column headers show their data-type symbol. Table-type views and tabular reports only. |
| `includeShowHideOption` | Boolean | No | `false` | Whether the viewer can show/hide columns. Table-type views and tabular reports only. |
| `legendPosition` | String | No | — (view's own setting) | Legend placement, honoured **only for chart views**. Accepts a single word (letters, digits, underscore), e.g. `BOTTOMCENTER`. Silently ignored for non-chart views. |
| `language` | String | No | — (viewer's default) | Renders the embedded view in this language. Must be one of the supported language names — see [`language` Values](#language-values). An unsupported name fails with `9102`. |
| `validateSystemTags` | Boolean | No | `true` | If `true`, the request is blocked with a confirmation-required error (`8241`) when the view carries a restricted **DATA_WARNING** system tag. Pass `false` to acknowledge the warning and mint the URL anyway. |

### `permissions` Fields

An embed URL carries only the five read-oriented permissions below. `read` is always granted; the row-write permissions, `share`, and `discussion` can never be attached to an embed URL.

| Field | Type | Default | Description |
|-------|------|---------|--------------|
| `read` | Boolean | `true` | View/read access. Always granted and always present in the stored configuration — it cannot be switched off. |
| `export` | Boolean | `false` | Allows the viewer to export the embedded view's data. |
| `vud` | Boolean | `false` | Allows "View Underlying Data" — drilling from an aggregated report into the raw rows behind it. Pair with `vudColumns` / `vudColumnsToExclude` to control which columns are exposed. |
| `drillDown` | Boolean | `false` | Allows drilling down into the view by column values. Pair with `drillColumns` / `drillColumnsToExclude`. |
| `insight` | Boolean | `false` | Allows the viewer to see Zia Insights generated for the view. |

### `vudColumns` / `drillColumns` Fields

`vudColumns`, `vudColumnsToExclude`, `drillColumns`, and `drillColumnsToExclude` all take the same shape — a JSONArray of objects, one per underlying table referenced by the view:

| Field | Type | Mandatory | Description |
|-------|------|-----------|--------------|
| `tableName` | String | **Yes** | Name of the underlying table whose columns are being restricted. Must be a table actually involved in the view (`7138` otherwise). Max 50 characters. |
| `columnNames` | JSONArray of String | **Yes** | Column names from `tableName`. 1–300 entries. Each name must exist in that table (`8154` otherwise). |

### `language` Values

`english`, `chinese`, `chinese_td`, `japanese`, `korean`, `french`, `italian`, `spanish`, `portuguese`, `portuguese_td`, `german`, `dutch`, `russian`, `polish`, `arabic`, `hebrew`, `turkish`, `hungarian`, `swedish`, `danish`, `ukranian`, `vietnamies`, `bulgarian`, `croatian`, `czech`, `hindi`, `thai`, `indonesian`, `malay`, `khmer`.

## Notes from the OpenAPI specification

- This API is available only to Embedded Analytics customers.
- The generated URL is short-lived and does not require a login. Anyone holding it has the access granted by the config until the validity period elapses.

- As this is a GET request, the CONFIG value must be stringified and URL encoded before it is sent.
- `CONFIG` may be omitted entirely, in which case the embed URL is returned with the default rendering options and a one hour validity period.
- `vudColumns` is applicable only when the `vud` permission is set to true.
- `drillColumns` is applicable only when the `drillDown` permission is set to true.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get embed URL"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.embedUrl` | String | The newly minted embed URL, of the form `https://<domain>/open-view/<view-id>?RSCONFIG=<config-key>&FS=OS`. `<config-key>` is the opaque encrypted key under which this URL's configuration is stored — it is the same value returned as `rsConfig` by [Fetch All Embed URLs](get-embed-urls.md) and accepted by [Delete Embed URL](delete-embed-url.md). `FS` is always `OS`. **Treat the whole value as a credential** — it grants sign-in-free access to the view, with the permissions and filter baked in, until it expires. |

> The response does **not** echo back the permissions, criteria, validity period, or column restrictions that were applied. Read them back through [Fetch All Embed URLs](get-embed-urls.md).

# Examples

## Sample Requests

**Case 1 — `criteria` only: one tenant's rows (the canonical multi-tenant call)**

CONFIG (before encoding):

```json
{
    "criteria": "\"Sales_1\".\"Region\"='West'"
}
```

```http
GET /restapi/v2/workspaces/137687000271334001/views/137687000006991601/publish/embed?CONFIG=%7B%22criteria%22%3A%22%5C%22Sales_1%5C%22.%5C%22Region%5C%22%3D'West'%22%7D HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Permissions and column restrictions clubbed together (include model)**

CONFIG (before encoding):

```json
{
    "permissions": {
        "read": true,
        "export": true,
        "vud": true,
        "drillDown": true,
        "insight": true
    },
    "vudColumns": [
        { "tableName": "Sales_1", "columnNames": ["Product", "Region"] }
    ],
    "drillColumns": [
        { "tableName": "Sales_1", "columnNames": ["Product", "Date"] }
    ],
    "includeToolBar": true
}
```

```http
GET /restapi/v2/workspaces/137687000271334001/views/137687000006991650/publish/embed?CONFIG=%7B%22permissions%22%3A%7B%22read%22%3Atrue%2C%22export%22%3Atrue%2C%22vud%22%3Atrue%2C%22drillDown%22%3Atrue%2C%22insight%22%3Atrue%7D%2C%22vudColumns%22%3A%5B%7B%22tableName%22%3A%22Sales_1%22%2C%22columnNames%22%3A%5B%22Product%22%2C%22Region%22%5D%7D%5D%2C%22drillColumns%22%3A%5B%7B%22tableName%22%3A%22Sales_1%22%2C%22columnNames%22%3A%5B%22Product%22%2C%22Date%22%5D%7D%5D%2C%22includeToolBar%22%3Atrue%7D HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — Exclude model, longer validity, localisation, and minimal chrome clubbed together**

CONFIG (before encoding):

```json
{
    "permissions": {
        "read": true,
        "vud": true
    },
    "vudColumnsToExclude": [
        { "tableName": "Sales_1", "columnNames": ["Cost", "Margin"] }
    ],
    "validityPeriod": 86400,
    "language": "french",
    "includeTitle": false,
    "includeDesc": false,
    "includeSearchBox": true,
    "includeDatatypeSymbol": true,
    "includeShowHideOption": true
}
```

```http
GET /restapi/v2/workspaces/137687000271334001/views/137687000006991601/publish/embed?CONFIG=%7B%22permissions%22%3A%7B%22read%22%3Atrue%2C%22vud%22%3Atrue%7D%2C%22vudColumnsToExclude%22%3A%5B%7B%22tableName%22%3A%22Sales_1%22%2C%22columnNames%22%3A%5B%22Cost%22%2C%22Margin%22%5D%7D%5D%2C%22validityPeriod%22%3A86400%2C%22language%22%3A%22french%22%2C%22includeTitle%22%3Afalse%2C%22includeDesc%22%3Afalse%2C%22includeSearchBox%22%3Atrue%2C%22includeDatatypeSymbol%22%3Atrue%2C%22includeShowHideOption%22%3Atrue%7D HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 4 — White Label / Client Portal: portal-domain embed URL, requested from the standard API host**

CONFIG (before encoding):

```json
{
    "domainName": "portal.customdomain.com",
    "criteria": "\"WL_Table\".\"Region\"='West'",
    "permissions": {
        "read": true,
        "export": true
    },
    "validityPeriod": 7200
}
```

```http
GET /restapi/v2/workspaces/137687000271334009/views/137687000006991777/publish/embed?CONFIG=%7B%22domainName%22%3A%22portal.customdomain.com%22%2C%22criteria%22%3A%22%5C%22WL_Table%5C%22.%5C%22Region%5C%22%3D'West'%22%2C%22permissions%22%3A%7B%22read%22%3Atrue%2C%22export%22%3Atrue%7D%2C%22validityPeriod%22%3A7200%7D HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK — Filtered embed URL (Case 1)**

```json
{
    "status": "success",
    "summary": "Get embed URL",
    "data": {
        "embedUrl": "https://analytics.zoho.com/open-view/137687000006991601?RSCONFIG=118b3222babc1aa5d7a19284827863e9428b334f8abc65ee92e648794bf501bcc77fe1ed97d0b48d9681a00aeb9545d6&FS=OS"
    }
}
```

**HTTP 200 OK — VUD and drill-down restricted to selected columns (Case 2)**

```json
{
    "status": "success",
    "summary": "Get embed URL",
    "data": {
        "embedUrl": "https://analytics.zoho.com/open-view/137687000006991650?RSCONFIG=118b3222babc1aa5d7a19284827863e90177da79a369e9644caccd7026a87832eac37794b628a26837ccd0b6cf0db806&FS=OS"
    }
}
```

**HTTP 200 OK — White Label / Client Portal, portal-domain host (Case 4)**

```json
{
    "status": "success",
    "summary": "Get embed URL",
    "data": {
        "embedUrl": "https://portal.customdomain.com/open-view/137687000006991777?RSCONFIG=118b3222babc1aa5d7a19284827863e9fb29464e6e58fe88322963307a65fbaaf3a483a26d6adbf3a6c7906d213dc946&FS=OS"
    }
}
```

**HTTP 403 Forbidden — Request sent through a Client Portal / White Label domain (API disabled there)**

```json
{
    "status": "failure",
    "summary": "SECURITY_NOT_PERMITTED",
    "data": {
        "errorCode": 7301,
        "errorMessage": "You (WL_DBAdmin) do not have the permission to do this operation. "
    }
}
```

**HTTP 403 Forbidden — Organization not enabled for Embedded Analytics**

```json
{
    "status": "failure",
    "summary": "OEM_OPERATION_NOT_ALLOWED",
    "data": {
        "errorCode": 8023,
        "errorMessage": "This operation is not allowed."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Embed URL](../../../sdk-examples/share-and-publish/embed-url/get-embed-url.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Every call mints a new URL** | This API is a factory, not an accessor. Ten calls produce ten independent, simultaneously valid URLs, each with its own configuration and its own expiry. Nothing about the view itself is modified. Use [Fetch All Embed URLs](get-embed-urls.md) to see how many are outstanding. |
| **`criteria` is the multi-tenancy primitive** | Because the filter is bound to the URL rather than to the view or to a user, one view can serve many customers: issue one URL per customer with a `criteria` that scopes it to their rows. The criteria is stored encrypted and is not visible to the viewer. |
| **Short-lived by default** | With no `validityPeriod`, the URL dies after **3600 seconds**. Hosts that render long-lived dashboards must either raise `validityPeriod` (up to the maximum of 86400 seconds) or re-mint the URL server-side before it lapses. |
| **`validityPeriod` is validated, not clamped** | A value above the 86400-second maximum fails with `8177` `MAX_ALLOWED_VALUE_EXCEEDED` rather than being reduced to the limit. |
| **Exclude model beats include model** | If both `vudColumns` and `vudColumnsToExclude` are sent, the exclude list is used and the include list is ignored — no error is raised. The same applies to `drillColumns` versus `drillColumnsToExclude`. |
| **Column restrictions need the matching permission** | `vudColumns` / `vudColumnsToExclude` are ignored unless `permissions.vud` is `true`; `drillColumns` / `drillColumnsToExclude` are ignored unless `permissions.drillDown` is `true`. No error is raised for the ignored field. |
| **Only five permissions apply** | `read`, `export`, `vud`, `drillDown`, and `insight` are the whole permission surface of an embed URL. Anything else in the wider [sharing permission set](../sharing/share-views.md#permissions-fields) cannot be granted through this channel. |
| **The URL carries no options in its query string** | Everything requested in CONFIG — permissions, criteria, column restrictions, validity — is stored server-side against the `RSCONFIG` key; the URL itself is only `?RSCONFIG=<key>&FS=OS`. Treat `embedUrl` as opaque and do not attempt to alter behaviour by editing its query string. |
| **View-type-scoped options fail silently** | `includeSearchBox`, `includeDatatypeSymbol`, and `includeShowHideOption` apply only to table-type views and tabular reports; `legendPosition` applies only to charts. Sending them for the wrong view type is accepted and ignored. |
| **URL-encode the CONFIG** | The value contains `{`, `"`, and `=` characters that are illegal in a raw query string. Stringify and percent-encode it; sending it raw produces a client-side URI parse failure before the request ever reaches the server. |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour) — use `domainName` from the standard API host instead. |
| **Dependency chain** | [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>` → Get Embed URL → (audit) [Fetch All Embed URLs](get-embed-urls.md) → (revoke) [Delete Embed URL](delete-embed-url.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — View not found. | Verify `<view-id>` exists in the workspace. |
| [7138](../../../foundations/error-codes.md#error-7138) | 400 | `META_OBJECT_NOT_PRESENT` — A `tableName` in a `vudColumns`/`drillColumns` array is not a table involved in this view. | Use only tables that the view actually reads from. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The request came through a Client Portal / White Label domain (where this API is disabled), or a non-owner caller is not in the organization's OEM-enabled users list, or the user lacks Publish / Make Public permission on the view. | Call from the standard API host; ensure the user is an Account Admin, Organization Admin, Workspace Admin, or has Publish / Make Public permission, and is OEM-enabled if not a workspace owner. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The view does not belong to the specified workspace. | Ensure `<workspace-id>` and `<view-id>` are consistent. |
| [8023](../../../foundations/error-codes.md#error-8023) | 403 | `OEM_OPERATION_NOT_ALLOWED` — The organization/workspace is not enabled for Embedded Analytics. | Embedded Analytics must be enabled for the account; contact Zoho Analytics support/sales. |
| [8054](../../../foundations/error-codes.md#error-8054) | 400 | `INVALID_FILTER_CRITERIA` — `criteria` could not be parsed. | Correct the criteria syntax (e.g. `"Table"."Column"='Value'`). |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The `domainName` supplied does not exist. | Use a domain returned by the [Domain and White Label APIs](../../workspace-management/domain-and-white-label/overview.md). |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | `DOMAIN_DOES_NOT_BELONGS_TO_USER` — The caller is not an admin of the supplied `domainName`. | Call as an admin of that portal domain, or omit `domainName`. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — CONFIG is not valid JSON, was not URL-encoded correctly, contains an unsupported key, or violates a type/length constraint. | Stringify and URL-encode the CONFIG object, and send only the documented keys. |
| [8154](../../../foundations/error-codes.md#error-8154) | 400 | `COLUMN_NOT_PRESENT_IN_TABLE` — A column in a `vudColumns`/`drillColumns` array (or in `criteria`) does not exist in the given table. | Verify column names via [Get Columns](../../data-modeling-and-schema/columns/overview.md). |
| [8177](../../../foundations/error-codes.md#error-8177) | 400 | `MAX_ALLOWED_VALUE_EXCEEDED` — `validityPeriod` exceeds the maximum of 86400 seconds (1 day). | Send a value of 86400 seconds or less. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | `SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION` — The view carries a restricted DATA_WARNING system tag. | Review the warning, then resend with `"validateSystemTags": false` to confirm. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.embed.read`. |
| [9102](../../../foundations/error-codes.md#error-9102) | 400 | `LANGUAGE_NOT_SUPPORTED` — `language` is not one of the supported language names. | Use a value from [`language` Values](#language-values). |
| [12052](../../../foundations/error-codes.md#error-12052) | 400 | `WORKSPACE_NOT_ENABLED_FOR_DOMAIN_ACCESS` — The workspace is not enabled for access through the requested portal domain. | Enable the workspace for that Client Portal domain first. |

# Related

- [Embed URL overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Fetch All Embed URLs](get-embed-urls.md), [Delete Embed URL](delete-embed-url.md).
- [SDK examples](../../../sdk-examples/share-and-publish/embed-url/get-embed-url.md).
