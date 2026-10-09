---
type: API Endpoint
title: Get Slide Info
description: "Returns the full definition of a single slideshow: its name, its access type, its secret slide key, and the ordered list of view IDs it contains."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - slideshow-management
  - get
  - embed
api:
  operation_id: getSlideshowDetails
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}"
  domain: share-and-publish
  group: slideshow-management
  oauth_scopes:
    - ZohoAnalytics.embed.read
  org_id_header: required
  config_parameter:
    location: none
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
    - 8535
  openapi:
    file: "/references/openapi/share-publish-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1slides~1{slide-id}/get"
    config_schema: null
    response_schema: GetSlideshowDetailsResponse
  sdk_examples: "/sdk-examples/share-and-publish/slideshow-management/get-slideshow-details.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}`** - Get Slide Info (Slideshow Management / Share & Publish).

Returns the full definition of a single slideshow: its name, its access type, its secret slide key, and the ordered list of view IDs it contains.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getSlideshowDetails` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.embed.read`](../../../foundations/oauth-scopes.md#zohoanalyticsembedread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Slideshow permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1slides~1{slide-id}/get`; response schema `GetSlideshowDetailsResponse` |

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

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get slideshow details"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.slideInfo` | JSONObject | The slideshow's full definition. Always present on success. |
| `slideInfo.slideId` | String | Numeric ID of the slideshow, serialised as a **string**. Echoes the `<slide-id>` from the URL. |
| `slideInfo.slideKey` | String | The 32-character lowercase hexadecimal secret embedded in the presentation URL. **Treat as a credential** — combined with `slideId` it reconstructs the viewing URL, which needs no sign-in when `accessType` is `1`. Changes whenever [Update Slide Show](update-slideshow.md) is called with `regenerateSlideKey: true`. |
| `slideInfo.slideName` | String | Display name of the slideshow. Unique within the workspace. |
| `slideInfo.accessType` | Number | Whether a viewer must sign in: `0` = access with login, `1` = access without login. See [`accessType` Values](overview.md#accesstype-values). |
| `slideInfo.viewIds` | JSONArray of String | IDs of the views in the slideshow, **in presentation order**. Each ID is a string. Resolve names/types via [Get View Details](../../views-management/view-operations/get-view-details.md). |

# Examples

## Sample Requests

**Case 1 — Standard workspace**

```http
GET /restapi/v2/workspaces/137687000271334001/slides/137687000003149001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal workspace**

```http
GET /restapi/v2/workspaces/137687000271334009/slides/137687000003120002 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK — Slideshow requiring a login (`accessType: 0`), three views (Case 1)**

```json
{
    "status": "success",
    "summary": "Get slideshow details",
    "data": {
        "slideInfo": {
            "slideId": "137687000003149001",
            "slideKey": "3a9aea323f01b0c17012e905a1b10013",
            "slideName": "Sales Overview",
            "accessType": 0,
            "viewIds": [
                "137687000006991601",
                "137687000006991650",
                "137687000006991700"
            ]
        }
    }
}
```

**HTTP 200 OK — Same slideshow after an update: key rotated, opened up without login, views replaced**

```json
{
    "status": "success",
    "summary": "Get slideshow details",
    "data": {
        "slideInfo": {
            "slideId": "137687000003149001",
            "slideKey": "7ddc2de689a5b7f4efb81ca48245c9be",
            "slideName": "Sales Overview",
            "accessType": 1,
            "viewIds": [
                "137687000006991710",
                "137687000006991711",
                "137687000006991712"
            ]
        }
    }
}
```

**HTTP 200 OK — White Label / Client Portal workspace (Case 2)**

```json
{
    "status": "success",
    "summary": "Get slideshow details",
    "data": {
        "slideInfo": {
            "slideId": "137687000003120002",
            "slideKey": "2f9afc5a38d71d366000dbaac41d9007",
            "slideName": "Portal Detail",
            "accessType": 0,
            "viewIds": [
                "137687000006991777",
                "137687000006991778",
                "137687000006991779"
            ]
        }
    }
}
```

**HTTP 400 Bad Request — Slideshow belongs to a different workspace**

```json
{
    "status": "failure",
    "summary": "SLIDESHOW_NOT_BELONGS_TO_DB",
    "data": {
        "errorCode": 7351,
        "errorMessage": "The given slideshow does not belong to this workspace."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Slide Info](../../../sdk-examples/share-and-publish/slideshow-management/get-slideshow-details.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **The only API that returns `slideKey`** | [Get Slide List](get-slideshows.md) deliberately omits it. If you need to construct a presentation URL yourself, this is where the key comes from — though [Get Slide URL](get-slideshow-url.md) is the supported way to build the URL. |
| **`viewIds` order is the presentation order** | The array is not sorted by ID or name; it is the sequence in which the views are shown. Preserving order matters when round-tripping through [Update Slide Show](update-slideshow.md), which replaces the whole list. |
| **View names are not resolved** | Only IDs are returned. Pair with [Get View List](../../views-management/view-operations/get-views.md) if you need to display names. |
| **Does not re-check per-view access** | The permission check is at workspace level (owner, or Create Slideshow permission). This API does not verify that the caller can read each view in `viewIds`, so a slideshow may list views the caller cannot open individually. |
| **Error precedence: `7351` before `7396`** | A wrong or non-existent `<slide-id>` is caught first by the workspace-membership check and reported as `7351`. `7396` surfaces only in the rarer case where the slideshow record exists but its slide details cannot be read. |
| **No email-verification requirement** | Unlike the three mutating APIs, this read-only API does not require the caller's primary email to be verified. |
| **Dependency chain** | [Get Slide List](get-slideshows.md) → `<slide-id>` → Get Slide Info → (optional) [Get View Details](../../views-management/view-operations/get-view-details.md) for each `viewIds` entry. |

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
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.embed.read`. |

# Related

- [Slideshow Management overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Slide List](get-slideshows.md), [Get Slide URL](get-slideshow-url.md), [Create Slide Show](create-slideshow.md), [Update Slide Show](update-slideshow.md), [Delete Slide Show](delete-slideshow.md).
- [SDK examples](../../../sdk-examples/share-and-publish/slideshow-management/get-slideshow-details.md).
