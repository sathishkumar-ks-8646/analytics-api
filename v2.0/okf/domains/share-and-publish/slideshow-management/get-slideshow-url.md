---
type: API Endpoint
title: Get Slide URL
description: Returns the URL through which the specified slideshow can be accessed.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}/publish"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - slideshow-management
  - get
  - embed
api:
  operation_id: getSlideshowUrl
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}/publish"
  domain: share-and-publish
  group: slideshow-management
  oauth_scopes:
    - ZohoAnalytics.embed.read
  org_id_header: required
  config_parameter:
    location: query
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Slideshow permission on the workspace."
  error_codes:
    - 6063
    - 7103
    - 7301
    - 7351
    - 7396
    - 8080
    - 8119
    - 8535
  openapi:
    file: "/references/openapi/share-publish-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1slides~1{slide-id}~1publish/get"
    config_schema: GetSlideshowUrlConfig
    response_schema: GetSlideshowUrlResponse
  sdk_examples: "/sdk-examples/share-and-publish/slideshow-management/get-slideshow-url.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/share-publish-grouped-api.json"
    title: OpenAPI 3 specification - share-publish-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}/publish`** - Get Slide URL (Slideshow Management / Share & Publish).

Builds and returns the presentation URL for an existing slideshow. The rendering options sent in CONFIG are not stored — they are baked into the query string of the URL that comes back, so different callers can obtain differently configured URLs for the same slideshow.

From the OpenAPI specification:

Returns the URL through which the specified slideshow can be accessed. The rendering options sent in the config - the title, description, social widgets, autoplay, and the switching interval - are carried in the query string of the returned URL.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getSlideshowUrl` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}/publish` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.embed.read`](../../../foundations/oauth-scopes.md#zohoanalyticsembedread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Slideshow permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - optional |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1slides~1{slide-id}~1publish/get`; CONFIG schema `GetSlideshowUrlConfig`; response schema `GetSlideshowUrlResponse` |

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
| `{slide-id}` | string | ID of the slide. | [How to obtain](../../../foundations/identifiers.md#slide-id) |

## CONFIG Parameters

CONFIG is **optional** for this API. Because this is a `GET`, it must be passed as a **query parameter** whose value is the stringified, URL-encoded JSON object. Omitting CONFIG entirely returns the URL with all defaults applied.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `autoplay` | Boolean | No | `true` | Whether the slideshow advances from one view to the next on its own. Emitted as `AUTOPLAY=<value>` in the returned URL. Set to `false` for a manually driven presentation. |
| `slideInterval` | Integer | No | `25` | Seconds each view is displayed before the slideshow advances. **Must be between 10 and 300 inclusive** — any other value is rejected with `8119`. Emitted as `INTERVAL=<value>`. Only meaningful when `autoplay` is `true`. |
| `includeTitle` | Boolean | No | `true` | Whether each view's name is shown on its slide. Emitted as `INCLUDETITLE=<value>`. |
| `includeDesc` | Boolean | No | `true` | Whether each view's description is shown on its slide. Emitted as `INCLUDEDESC=<value>`. |
| `includeSocialWidgets` | Boolean | No | `false` | Whether social share widgets are rendered on the slides. Emitted as `SOCIALWIDGETS=<value>`. |
| `withCustomDomain` | Boolean | No | `false` | If `true`, returns the URL on the workspace's configured Client Portal / White Label domain instead of the Zoho Analytics domain. Requires the caller to be an **Organization Admin or Super Admin**, and the workspace must have a portal domain configured — if either condition fails, the flag is silently ignored and the normal domain is used. Unnecessary when the request is already made in a portal context (see Notes). |
| `domainName` | String | No | — | Accepted by the request template (max 200 characters) but **not used** by the slideshow URL builder. It has no effect on the returned URL; use `withCustomDomain` instead. |

## Notes from the OpenAPI specification

- As this is a GET request, the CONFIG value must be stringified and URL encoded before it is sent.
- `CONFIG` may be omitted entirely, in which case the slideshow URL is returned with the default rendering options.
- `slideInterval` must be between 10 and 300 seconds.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get slideshow URL"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.slideUrl` | String | The full presentation URL, always of the form `https://<domain>/ZDBSlideshow.cc?SLIDEID=<slide-id>&SLIDEKEY=<slide-key>&AUTOPLAY=<bool>&INTERVAL=<seconds>&INCLUDETITLE=<bool>&INCLUDEDESC=<bool>&SOCIALWIDGETS=<bool>`. The seven query parameters are always present, in that order, whether or not they were supplied in CONFIG. **`SLIDEKEY` is a secret** — for an `accessType: 1` slideshow this URL is sufficient to view the content with no sign-in, so treat the whole value as a credential. |

# Examples

## Sample Requests

**Case 1 — No CONFIG: default presentation URL**

```http
GET /restapi/v2/workspaces/137687000271334001/slides/137687000003149001/publish HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Playback options clubbed together: autoplay with a longer interval, no social widgets**

CONFIG (before encoding):

```json
{
    "autoplay": true,
    "slideInterval": 100,
    "includeTitle": true,
    "includeDesc": true,
    "includeSocialWidgets": false
}
```

```http
GET /restapi/v2/workspaces/137687000271334001/slides/137687000003149001/publish?CONFIG=%7B%22autoplay%22%3Atrue%2C%22slideInterval%22%3A100%2C%22includeTitle%22%3Atrue%2C%22includeDesc%22%3Atrue%2C%22includeSocialWidgets%22%3Afalse%7D HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — Chrome options clubbed together: manual advance, no title or description, social widgets on**

CONFIG (before encoding):

```json
{
    "autoplay": false,
    "includeTitle": false,
    "includeDesc": false,
    "includeSocialWidgets": true
}
```

```http
GET /restapi/v2/workspaces/137687000271334001/slides/137687000003149001/publish?CONFIG=%7B%22autoplay%22%3Afalse%2C%22includeTitle%22%3Afalse%2C%22includeDesc%22%3Afalse%2C%22includeSocialWidgets%22%3Atrue%7D HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 4 — White Label / Client Portal: return the URL on the portal domain**

CONFIG (before encoding):

```json
{
    "withCustomDomain": true,
    "autoplay": true,
    "slideInterval": 60
}
```

```http
GET /restapi/v2/workspaces/137687000271334009/slides/137687000003120002/publish?CONFIG=%7B%22withCustomDomain%22%3Atrue%2C%22autoplay%22%3Atrue%2C%22slideInterval%22%3A60%7D HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK — Defaults (Case 1)**

```json
{
    "status": "success",
    "summary": "Get slideshow URL",
    "data": {
        "slideUrl": "https://analytics.zoho.com/ZDBSlideshow.cc?SLIDEID=137687000003149001&SLIDEKEY=7ddc2de689a5b7f4efb81ca48245c9be&AUTOPLAY=true&INTERVAL=25&INCLUDETITLE=true&INCLUDEDESC=true&SOCIALWIDGETS=false"
    }
}
```

**HTTP 200 OK — Longer interval (Case 2)**

```json
{
    "status": "success",
    "summary": "Get slideshow URL",
    "data": {
        "slideUrl": "https://analytics.zoho.com/ZDBSlideshow.cc?SLIDEID=137687000003149001&SLIDEKEY=7ddc2de689a5b7f4efb81ca48245c9be&AUTOPLAY=true&INTERVAL=100&INCLUDETITLE=true&INCLUDEDESC=true&SOCIALWIDGETS=false"
    }
}
```

**HTTP 200 OK — Manual advance, no title/description, social widgets on (Case 3)**

```json
{
    "status": "success",
    "summary": "Get slideshow URL",
    "data": {
        "slideUrl": "https://analytics.zoho.com/ZDBSlideshow.cc?SLIDEID=137687000003149001&SLIDEKEY=7ddc2de689a5b7f4efb81ca48245c9be&AUTOPLAY=false&INTERVAL=25&INCLUDETITLE=false&INCLUDEDESC=false&SOCIALWIDGETS=true"
    }
}
```

**HTTP 200 OK — White Label / Client Portal (Case 4)**

```json
{
    "status": "success",
    "summary": "Get slideshow URL",
    "data": {
        "slideUrl": "https://portal.customdomain.com/ZDBSlideshow.cc?SLIDEID=137687000003120002&SLIDEKEY=2f9afc5a38d71d366000dbaac41d9007&AUTOPLAY=true&INTERVAL=60&INCLUDETITLE=true&INCLUDEDESC=true&SOCIALWIDGETS=false"
    }
}
```

**HTTP 403 Forbidden — User lacks the slideshow permission on the workspace**

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

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Slide URL](../../../sdk-examples/share-and-publish/slideshow-management/get-slideshow-url.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Nothing is persisted** | The rendering options are query-string decoration on the returned URL only. Calling this API does not change the slideshow, and two callers can hold two differently configured URLs for the same `slideId` simultaneously. Contrast with [Update Publish Configurations](../publish/update-publish-configurations.md), which does store per-view presentation settings. |
| **The full query string is always emitted** | Even a bare call with no CONFIG returns all seven parameters with their defaults, so the URL shape is stable and parseable. |
| **`autoplay` defaults to `true`** | A call with no CONFIG produces `AUTOPLAY=true&INTERVAL=25`. Send `"autoplay": false` explicitly for a manually advanced presentation. |
| **`slideInterval` is validated, not clamped** | Values below 10 or above 300 raise `8119` `INVALID_VALUE_FOR_ATTRIBUTE` rather than being rounded into range. The error message names the offending value and the permitted `10-300` range. |
| **Portal domain is automatic in a portal context** | When the request itself arrives through a Client Portal / White Label domain, the returned URL is already built on that domain — `withCustomDomain` is unnecessary. The flag exists for the case where an Organization Admin calls from the standard Zoho Analytics context and wants the portal-domain form of the URL. |
| **`withCustomDomain` fails silently** | If the caller is not an Organization Admin or Super Admin, or the workspace has no portal domain configured, the flag is ignored and the standard domain is returned with HTTP 200. There is no error to distinguish "ignored" from "applied" — compare the host in `slideUrl` to confirm. |
| **`domainName` has no effect** | The key is accepted by the request template but is never read by the slideshow URL builder. Sending it does not error and does not change the host. |
| **Reflects the current `slideKey`** | The URL always embeds the slideshow's live key, so a URL fetched after a `regenerateSlideKey` update differs from one fetched before, and the earlier one no longer works. |
| **No email-verification requirement** | Unlike the three mutating APIs, this read-only API does not require the caller's primary email to be verified. |
| **Dependency chain** | [Get Slide List](get-slideshows.md) → `<slide-id>` → Get Slide URL. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6063](../../../foundations/error-codes.md#error-6063) | 400 | `SLIDESHOW_NOT_ALLOWED` — The workspace owner's plan does not include the slideshow feature. | Upgrade the plan to one that supports slideshows. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user is neither a workspace owner nor a custom-role user with Create Slideshow permission. | Ensure the user is an Account Admin, Organization Admin, Workspace Admin, or has Create Slideshow permission on the workspace. |
| [7351](../../../foundations/error-codes.md#error-7351) | 400 | `SLIDESHOW_NOT_BELONGS_TO_DB` — The slideshow does not exist, or belongs to a different workspace. | Verify `<slide-id>` against [Get Slide List](get-slideshows.md) for this workspace. |
| [7396](../../../foundations/error-codes.md#error-7396) | 400 | `SLIDE_NOT_PRESENT_IN_DB` — The slideshow record exists but no slide details could be read for it. | Re-check the slideshow via [Get Slide List](get-slideshows.md); recreate it if it is in an inconsistent state. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — CONFIG is not valid JSON, was not URL-encoded correctly, or contains an unsupported key. | Stringify and URL-encode the CONFIG object, and send only the documented keys. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE` — `slideInterval` is outside the permitted `10-300` range. | Send a value between 10 and 300 seconds, or omit it to use the default of 25. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.embed.read`. |

# Related

- [Slideshow Management overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Slide List](get-slideshows.md), [Get Slide Info](get-slideshow-details.md), [Create Slide Show](create-slideshow.md), [Update Slide Show](update-slideshow.md), [Delete Slide Show](delete-slideshow.md).
- [SDK examples](../../../sdk-examples/share-and-publish/slideshow-management/get-slideshow-url.md).
