---
type: API Endpoint
title: Update Slide Show
description: Updates the details of the specified slideshow.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - slideshow-management
  - put
  - embed
api:
  operation_id: updateSlideshow
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}"
  domain: share-and-publish
  group: slideshow-management
  oauth_scopes:
    - ZohoAnalytics.embed.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
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
    - 7351
    - 7565
    - 8080
    - 8088
    - 8241
    - 8535
  openapi:
    file: "/references/openapi/share-publish-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1slides~1{slide-id}/put"
    config_schema: UpdateSlideshowConfig
    response_schema: null
  sdk_examples: "/sdk-examples/share-and-publish/slideshow-management/update-slideshow.md"
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

**PUT `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}`** - Update Slide Show (Slideshow Management / Share & Publish).

Updates an existing slideshow: renames it, replaces its set of views, changes its access type, and/or rotates its slide key. Unlike the publish configuration APIs, this one is a genuine **partial update** — only the attributes present in CONFIG are touched.

From the OpenAPI specification:

Updates the details of the specified slideshow. The name, the views it contains, and its access type can all be changed, and the slide key can be regenerated to invalidate the URL issued previously.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `updateSlideshow` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.embed.update`](../../../foundations/oauth-scopes.md#zohoanalyticsembedupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Slideshow permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1slides~1{slide-id}/put`; CONFIG schema `UpdateSlideshowConfig` |

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
| `{slide-id}` | string | ID of the slide. | [How to obtain](../../../foundations/identifiers.md#slide-id) |

## CONFIG Parameters

CONFIG is **mandatory** for this API, but every field inside it is optional. Fields you omit keep their current values.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `slideName` | String | No | — (unchanged) | New name for the slideshow. Must be unique within the workspace, ignoring the slideshow being updated (`7196` otherwise) — re-sending the slideshow's own current name is therefore accepted. Same character-set restriction as on create: letters, digits, whitespace, and non-Basic-Latin characters only. |
| `viewIds` | JSONArray of String/Long | No | — (unchanged) | **Replaces** the entire set of views, in the order given. 1–100 entries. Every view must belong to `<workspace-id>` (`7319` otherwise). This is not an append — to add one view, send the existing list from [Get Slide Info](get-slideshow-details.md) plus the new ID. |
| `accessType` | Integer (`0` \| `1`) | No | — (unchanged) | New access type. See [`accessType` Values](overview.md#accesstype-values). Switching **to** `1` triggers the private-link plan check (`6054`/`6056`) and the private-link security control (`8088`); switching to `0` does not. |
| `regenerateSlideKey` | Boolean | No | `false` | If `true`, generates a new slide key, immediately invalidating every presentation URL issued earlier. Also gated by the private-link plan check and security control. Sending `false` explicitly is a no-op. |
| `validateSystemTags` | Boolean | No | `true` | If `true`, the request is blocked with a confirmation-required error (`8241`) when any view in `viewIds` carries a restricted **DATA_WARNING** system tag. Pass `false` to acknowledge and proceed. Only evaluated when `viewIds` is present. |

## Notes from the OpenAPI specification

- Only the attributes sent in the config are updated; the ones omitted retain their current values.
- Sending `viewIds` replaces the entire set of views in the slideshow rather than adding to it.
- Setting `regenerateSlideKey` to true disables the slideshow URL that was issued previously.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`). To read the resulting state, call [Get Slide Info](get-slideshow-details.md).

# Examples

## Sample Requests

**Case 1 — Rename only (views and access type untouched)**

```http
PUT /restapi/v2/workspaces/137687000271334001/slides/137687000003149001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "slideName": "Sales Overview 2026"
}
```

**Case 2 — Attributes clubbed together: replace the views, rename, and open it up without login**

```http
PUT /restapi/v2/workspaces/137687000271334001/slides/137687000003149001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "slideName": "Sales Overview 2026",
    "viewIds": [
        "137687000006991710",
        "137687000006991711",
        "137687000006991712"
    ],
    "accessType": 1,
    "validateSystemTags": false
}
```

**Case 3 — Rotate the slide key to revoke previously shared URLs**

```http
PUT /restapi/v2/workspaces/137687000271334001/slides/137687000003149001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "regenerateSlideKey": true
}
```

**Case 4 — White Label / Client Portal: add a view to a portal slideshow (full list resent)**

```http
PUT /restapi/v2/workspaces/137687000271334009/slides/137687000003120002 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "viewIds": [
        "137687000006991777",
        "137687000006991778",
        "137687000006991779"
    ]
}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code, then read the applied state back with [Get Slide Info](get-slideshow-details.md).

```
HTTP/1.1 204 No Content
```

**HTTP 404 Not Found — Name collides with another slideshow in the workspace**

```json
{
    "status": "failure",
    "summary": "SLIDENAME_ALREADY_EXISTS",
    "data": {
        "errorCode": 7196,
        "errorMessage": "A slideshow with this name already exists."
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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Update Slide Show](../../../sdk-examples/share-and-publish/slideshow-management/update-slideshow.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Update Slide Show returns a bare HTTP `204 No Content` — no `status`/`summary` JSON to parse, and no updated `slideUrl`. Fetch the new URL from [Get Slide URL](get-slideshow-url.md) after rotating the key. |
| **True partial update** | Only keys present in CONFIG are applied; omitted attributes keep their values. This is the opposite of [Update Publish Configurations](../publish/update-publish-configurations.md), which rebuilds its whole configuration on every call. |
| **`viewIds` replaces, never appends** | Sending two IDs on a slideshow that had five leaves it with exactly those two, in that order. To add or reorder, read the current list from [Get Slide Info](get-slideshow-details.md), modify it, and resend it in full. |
| **Applied in a fixed order** | The server processes `slideName`, then `accessType`, then `viewIds`, then `regenerateSlideKey`. Each step can fail independently — a request that renames and replaces views may therefore have renamed successfully before failing on a bad view ID. Verify with [Get Slide Info](get-slideshow-details.md) after a partial failure. |
| **Re-sending the current name is safe** | The uniqueness check excludes the slideshow being updated, so an idempotent "write the whole object back" pattern does not trip `7196`. |
| **`regenerateSlideKey` is an irreversible revocation** | Every URL previously handed out stops working the moment the new key is stored. There is no grace period and no way to recover the old key. |
| **Two operations share the private-link gating** | Both `accessType: 1` and `regenerateSlideKey: true` run the private-link plan check (`6054`/`6056`) and security-control check (`8088`). A rename-only or `accessType: 0` update skips them. |
| **`validateSystemTags` only matters with `viewIds`** | System-tag validation runs against the views being added; a request without `viewIds` never triggers `8241`. |
| **No `criteria` support** | There is no row-filter attribute on this API. |
| **Dependency chain** | [Get Slide Info](get-slideshow-details.md) (read current name/views/access type) → merge → Update Slide Show → [Get Slide Info](get-slideshow-details.md) / [Get Slide URL](get-slideshow-url.md) to verify. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6054](../../../foundations/error-codes.md#error-6054) | 400 | `PUBLISHCNT_VIOLATION` — `accessType: 1` or `regenerateSlideKey: true` requested but the plan does not allow login-free (private-link style) access. | Use `accessType: 0` and omit `regenerateSlideKey`, or upgrade the plan. |
| [6056](../../../foundations/error-codes.md#error-6056) | 400 | `SHAREDUSR_PUBLISHCNT_VIOLATION` — A shared user requested a plan-restricted `accessType: 1` or key rotation. | Ask the workspace owner to perform the update, or upgrade the plan. |
| [6063](../../../foundations/error-codes.md#error-6063) | 400 | `SLIDESHOW_NOT_ALLOWED` — The workspace owner's plan does not include the slideshow feature. | Upgrade the plan to one that supports slideshows. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — A view in `viewIds` does not exist. | Verify the IDs via [Get View List](../../views-management/view-operations/get-views.md). |
| [7196](../../../foundations/error-codes.md#error-7196) | 404 | `SLIDENAME_ALREADY_EXISTS` — Another slideshow in this workspace already uses the requested `slideName`. | Choose a different name. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user is neither a workspace owner nor a custom-role user with Create Slideshow permission. | Ensure the user is an Account Admin, Organization Admin, Workspace Admin, or has Create Slideshow permission on the workspace. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — A view in `viewIds` belongs to a different workspace. | Include only views from `<workspace-id>`. |
| [7351](../../../foundations/error-codes.md#error-7351) | 400 | `SLIDESHOW_NOT_BELONGS_TO_DB` — The slideshow does not exist, or belongs to a different workspace. | Verify `<slide-id>` against [Get Slide List](get-slideshows.md) for this workspace. |
| [7565](../../../foundations/error-codes.md#error-7565) | 400 | `UNVERIFIED_EMAIL` — The calling user's primary email address is not verified. | Verify the account's primary email address and retry. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — CONFIG is not valid JSON, contains an unsupported key, or violates a constraint (e.g. punctuation in `slideName`, more than 100 entries in `viewIds`). | Send only the documented keys with the documented types and value constraints. |
| [8088](../../../foundations/error-codes.md#error-8088) | 400 | `SECURITY_CONTROLS_FEATURE_DISABLED` — `accessType: 1` or key rotation requested but login-free links are disabled for this organization/workspace by security controls. | Ask the Organization Admin to re-enable private links in Security Controls. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | `SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION` — A view in `viewIds` carries a restricted DATA_WARNING system tag. | Review the warning, then resend with `"validateSystemTags": false` to confirm. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.embed.update`. |

# Related

- [Slideshow Management overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Slide List](get-slideshows.md), [Get Slide URL](get-slideshow-url.md), [Get Slide Info](get-slideshow-details.md), [Create Slide Show](create-slideshow.md), [Delete Slide Show](delete-slideshow.md).
- [SDK examples](../../../sdk-examples/share-and-publish/slideshow-management/update-slideshow.md).
