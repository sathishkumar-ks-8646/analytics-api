---
type: API Endpoint
title: Create Slide Show
description: "Creates a slideshow in the specified workspace from the given set of views, and returns its ID along with the URL through which it can be accessed."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/slides"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - slideshow-management
  - post
  - embed
api:
  operation_id: createSlideshow
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/slides"
  domain: share-and-publish
  group: slideshow-management
  oauth_scopes:
    - ZohoAnalytics.embed.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Slideshow permission on the workspace."
  error_codes:
    - 6054
    - 6056
    - 6063
    - 7103
    - 7104
    - 7196
    - 7301
    - 7319
    - 7565
    - 8078
    - 8079
    - 8080
    - 8088
    - 8241
    - 8535
  openapi:
    file: "/references/openapi/share-publish-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1slides/post"
    config_schema: CreateSlideshowConfig
    response_schema: CreateSlideshowResponse
  sdk_examples: "/sdk-examples/share-and-publish/slideshow-management/create-slideshow.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/slides`** - Create Slide Show (Slideshow Management / Share & Publish).

Creates a new slideshow in the workspace from an ordered set of views, and returns its new ID together with a ready-to-use presentation URL built with default rendering options.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createSlideshow` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/slides` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.embed.create`](../../../foundations/oauth-scopes.md#zohoanalyticsembedcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Slideshow permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1slides/post`; CONFIG schema `CreateSlideshowConfig`; response schema `CreateSlideshowResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.embed.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `slideName` | String | **Yes** | — | Name of the new slideshow. Must be **unique within the workspace** (`7196` otherwise). Permitted characters are letters, digits, whitespace, and non-Basic-Latin characters — punctuation and symbols are rejected by the template with `8080`. An absent key raises `8079`; an empty/blank value raises `8078`. |
| `viewIds` | JSONArray of String/Long | **Yes** | — | IDs of the views to include, **in the order they should be presented**. 1–100 entries. Every view must belong to `<workspace-id>` (`7319` otherwise). An absent key raises `8079`; an empty array raises `8078`. |
| `accessType` | Integer (`0` \| `1`) | No | `0` | Whether viewers must sign in. See [`accessType` Values](overview.md#accesstype-values). Choosing `1` (access without login) additionally triggers the private-link plan check (`6054`/`6056`) and the private-link security control (`8088`). |
| `validateSystemTags` | Boolean | No | `true` | If `true`, the request is blocked with a confirmation-required error (`8241`) when any view in `viewIds` carries a restricted **DATA_WARNING** system tag — directly, or inherited through lineage from a parent data source or table. Pass `false` to acknowledge the warning and create the slideshow anyway. Only relevant when System Tags are enabled for the organization. |

## Notes from the OpenAPI specification

- The order of the IDs in `viewIds` determines the order in which the views appear in the slideshow.
- `validateSystemTags` is applicable only when System Tags are enabled for your organization.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Create slideshow"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.slideId` | String | ID of the newly created slideshow, serialised as a **string**. Store this — it is the `<slide-id>` for [Get Slide Info](get-slideshow-details.md), [Get Slide URL](get-slideshow-url.md), [Update Slide Show](update-slideshow.md), and [Delete Slide Show](delete-slideshow.md). |
| `data.slideUrl` | String | Presentation URL for the new slideshow, built with **default** rendering options (`AUTOPLAY=true&INTERVAL=25&INCLUDETITLE=true&INCLUDEDESC=true&SOCIALWIDGETS=false`). To obtain a URL with different options, call [Get Slide URL](get-slideshow-url.md) with a CONFIG. **`SLIDEKEY` is a secret** — treat the whole value as a credential. |

> `slideName`, `accessType`, and `viewIds` are **not** echoed back. Read them via [Get Slide Info](get-slideshow-details.md) if you need to confirm what was stored.

# Examples

## Sample Requests

**Case 1 — Minimal: name and views only (defaults to access with login)**

```http
POST /restapi/v2/workspaces/137687000271334001/slides HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "slideName": "Sales Overview",
    "viewIds": ["137687000006991601", "137687000006991650"]
}
```

**Case 2 — Attributes clubbed together: a public slideshow of three views, skipping system-tag validation**

```http
POST /restapi/v2/workspaces/137687000271334001/slides HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "slideName": "Quarterly Highlights",
    "viewIds": [
        "137687000006991601",
        "137687000006991650",
        "137687000006991700"
    ],
    "accessType": 1,
    "validateSystemTags": false
}
```

**Case 3 — White Label / Client Portal: a portal-domain slideshow accessible without login**

```http
POST /restapi/v2/workspaces/137687000271334009/slides HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "slideName": "Portal Summary",
    "viewIds": [
        "137687000006991777",
        "137687000006991778"
    ],
    "accessType": 1
}
```

## Sample Responses

**HTTP 200 OK — Access with login (Case 1)**

```json
{
    "status": "success",
    "summary": "Create slideshow",
    "data": {
        "slideId": "137687000003149001",
        "slideUrl": "https://analytics.zoho.com/ZDBSlideshow.cc?SLIDEID=137687000003149001&SLIDEKEY=3a9aea323f01b0c17012e905a1b10013&AUTOPLAY=true&INTERVAL=25&INCLUDETITLE=true&INCLUDEDESC=true&SOCIALWIDGETS=false"
    }
}
```

**HTTP 200 OK — Access without login (Case 2)**

```json
{
    "status": "success",
    "summary": "Create slideshow",
    "data": {
        "slideId": "137687000003149002",
        "slideUrl": "https://analytics.zoho.com/ZDBSlideshow.cc?SLIDEID=137687000003149002&SLIDEKEY=ab69f2cdb88712190bc4bfae8bb4aef8&AUTOPLAY=true&INTERVAL=25&INCLUDETITLE=true&INCLUDEDESC=true&SOCIALWIDGETS=false"
    }
}
```

**HTTP 200 OK — White Label / Client Portal (Case 3)**

```json
{
    "status": "success",
    "summary": "Create slideshow",
    "data": {
        "slideId": "137687000003120001",
        "slideUrl": "https://portal.customdomain.com/ZDBSlideshow.cc?SLIDEID=137687000003120001&SLIDEKEY=456090ad1e6afdbccf3ee53a89a1d9dd&AUTOPLAY=true&INTERVAL=25&INCLUDETITLE=true&INCLUDEDESC=true&SOCIALWIDGETS=false"
    }
}
```

**HTTP 403 Forbidden — Slideshows disabled for this portal workspace / user lacks the permission**

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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Slide Show](../../../sdk-examples/share-and-publish/slideshow-management/create-slideshow.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`viewIds` order is the presentation order** | The array is stored as given — the first ID is the first slide. This is the only place the order is set on creation; changing it later means resending the whole array through [Update Slide Show](update-slideshow.md). |
| **Names must be unique per workspace** | A duplicate `slideName` fails with `7196` `SLIDENAME_ALREADY_EXISTS`; the call is not turned into an update. Check [Get Slide List](get-slideshows.md) first, or catch `7196` and retry with a different name. |
| **`slideName` character set is restrictive** | Only letters, digits, whitespace, and non-Basic-Latin characters pass template validation. Common punctuation (`-`, `_`, `:`, `/`, `&`, `.`) is rejected with `8080`, not silently stripped. |
| **Views are checked for workspace membership, not for readability** | Every ID in `viewIds` must belong to `<workspace-id>` (`7319`), but the caller's read permission on each individual view is **not** re-verified on this path — the workspace-level Create Slideshow permission governs the whole operation. |
| **`accessType: 1` is the private-link equivalent** | It brings in the private-link plan entitlement (`6054`/`6056`) and the organization's private-link security control (`8088`). `accessType: 0` skips both checks. |
| **The returned URL uses defaults only** | There is no way to pass rendering options to this API — `slideURL` options belong to [Get Slide URL](get-slideshow-url.md). The URL returned here is a convenience, not a configured artefact. |
| **Portal domain is automatic in a portal context** | When called through a Client Portal / White Label domain, the returned `slideUrl` is already on that domain; no CONFIG flag is involved. |
| **No `criteria` support** | Slideshows present each view as defined; there is no row-filter attribute on this API. |
| **Dependency chain** | [Get View List](../../views-management/view-operations/get-views.md) → `viewIds` → Create Slide Show → `slideId` → [Get Slide URL](get-slideshow-url.md) / [Get Slide Info](get-slideshow-details.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6054](../../../foundations/error-codes.md#error-6054) | 400 | `PUBLISHCNT_VIOLATION` — `accessType: 1` requested but the plan does not allow login-free (private-link style) access. | Use `accessType: 0`, or upgrade the plan. |
| [6056](../../../foundations/error-codes.md#error-6056) | 400 | `SHAREDUSR_PUBLISHCNT_VIOLATION` — A shared user requested `accessType: 1` on a plan that restricts it. | Ask the workspace owner to create the slideshow, use `accessType: 0`, or upgrade the plan. |
| [6063](../../../foundations/error-codes.md#error-6063) | 400 | `SLIDESHOW_NOT_ALLOWED` — The workspace owner's plan does not include the slideshow feature. | Upgrade the plan to one that supports slideshows. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — A view in `viewIds` does not exist. | Verify the IDs via [Get View List](../../views-management/view-operations/get-views.md). |
| [7196](../../../foundations/error-codes.md#error-7196) | 404 | `SLIDENAME_ALREADY_EXISTS` — Another slideshow in this workspace already uses `slideName`. | Choose a different name, or update the existing slideshow via [Update Slide Show](update-slideshow.md). |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user is neither a workspace owner nor a custom-role user with Create Slideshow permission. | Ensure the user is an Account Admin, Organization Admin, Workspace Admin, or has Create Slideshow permission on the workspace. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — A view in `viewIds` belongs to a different workspace. | Include only views from `<workspace-id>`. |
| [7565](../../../foundations/error-codes.md#error-7565) | 400 | `UNVERIFIED_EMAIL` — The calling user's primary email address is not verified. | Verify the account's primary email address and retry. |
| [8078](../../../foundations/error-codes.md#error-8078) | 400 | `EMPTY_JSON_ATTRIBUTE_FOUND` — `slideName` is blank, or `viewIds` is an empty array. | Supply a non-empty name and at least one view ID. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — `slideName` or `viewIds` is missing from CONFIG. | Both are mandatory; include them. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — CONFIG is not valid JSON, contains an unsupported key, or violates a constraint (e.g. punctuation in `slideName`, more than 100 entries in `viewIds`). | Send only the documented keys with the documented types and value constraints. |
| [8088](../../../foundations/error-codes.md#error-8088) | 400 | `SECURITY_CONTROLS_FEATURE_DISABLED` — `accessType: 1` requested but login-free links are disabled for this organization/workspace by security controls. | Use `accessType: 0`, or ask the Organization Admin to re-enable private links in Security Controls. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | `SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION` — A view in `viewIds` carries a restricted DATA_WARNING system tag. | Review the warning, then resend with `"validateSystemTags": false` to confirm. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.embed.create`. |

# Related

- [Slideshow Management overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Slide List](get-slideshows.md), [Get Slide URL](get-slideshow-url.md), [Get Slide Info](get-slideshow-details.md), [Update Slide Show](update-slideshow.md), [Delete Slide Show](delete-slideshow.md).
- [SDK examples](../../../sdk-examples/share-and-publish/slideshow-management/create-slideshow.md).
