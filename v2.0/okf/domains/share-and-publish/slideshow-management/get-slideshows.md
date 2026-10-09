---
type: API Endpoint
title: Get Slide List
description: "Returns every slideshow that exists in the workspace, with its ID, name, and access type."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/slides"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - slideshow-management
  - get
  - embed
api:
  operation_id: getSlideshows
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/slides"
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
    - 8535
  openapi:
    file: "/references/openapi/share-publish-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1slides/get"
    config_schema: null
    response_schema: GetSlideshowsResponse
  sdk_examples: "/sdk-examples/share-and-publish/slideshow-management/get-slideshows.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/slides`** - Get Slide List (Slideshow Management / Share & Publish).

Returns every slideshow that exists in the workspace, with its ID, name, and access type. This is the discovery call for `<slide-id>`, which every other API in this family needs.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getSlideshows` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/slides` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.embed.read`](../../../foundations/oauth-scopes.md#zohoanalyticsembedread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Slideshow permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1slides/get`; response schema `GetSlideshowsResponse` |

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

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get slideshows"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.slideshows` | JSONArray | One entry per slideshow in the workspace, in the workspace's stored order. **Always present**; an empty array `[]` when the workspace has no slideshows. |
| `slideshows[].slideId` | String | Numeric ID of the slideshow, serialised as a **string**. Use this as `<slide-id>` in the other five APIs. |
| `slideshows[].slideName` | String | Display name of the slideshow. Unique within the workspace. |
| `slideshows[].accessType` | Number | Whether a viewer must sign in: `0` = access with login, `1` = access without login. See [`accessType` Values](overview.md#accesstype-values). |

> `slideKey` and `viewIds` are **not** returned by this API — fetch them per slideshow via [Get Slide Info](get-slideshow-details.md).

# Examples

## Sample Requests

**Case 1 — Standard workspace**

```http
GET /restapi/v2/workspaces/137687000271334001/slides HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal workspace**

```http
GET /restapi/v2/workspaces/137687000271334009/slides HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK — Workspace with several slideshows of mixed access type (Case 1)**

```json
{
    "status": "success",
    "summary": "Get slideshows",
    "data": {
        "slideshows": [
            {
                "slideName": "Sales Overview",
                "slideId": "137687000003149001",
                "accessType": 1
            },
            {
                "slideName": "Quarterly Highlights",
                "slideId": "137687000003149002",
                "accessType": 1
            },
            {
                "slideName": "Regional Deep Dive",
                "slideId": "137687000003149003",
                "accessType": 0
            },
            {
                "slideName": "Ops Daily",
                "slideId": "137687000003149004",
                "accessType": 0
            }
        ]
    }
}
```

**HTTP 200 OK — White Label / Client Portal workspace (Case 2)**

```json
{
    "status": "success",
    "summary": "Get slideshows",
    "data": {
        "slideshows": [
            {
                "slideName": "Portal Summary",
                "slideId": "137687000003120001",
                "accessType": 1
            },
            {
                "slideName": "Portal Detail",
                "slideId": "137687000003120002",
                "accessType": 0
            }
        ]
    }
}
```

**HTTP 200 OK — Workspace with no slideshows yet**

```json
{
    "status": "success",
    "summary": "Get slideshows",
    "data": {
        "slideshows": []
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Slide List](../../../sdk-examples/share-and-publish/slideshow-management/get-slideshows.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Workspace-wide, not filtered** | There is no paging, search, or filter parameter — the response always covers every slideshow in the workspace. Filter client-side on `slideName` or `accessType`. |
| **Empty array, not an error** | A workspace with no slideshows returns HTTP 200 with `"slideshows": []`. Absence of slideshows is never an error condition. |
| **Deliberately omits the secret** | `slideKey` is excluded from this listing so that a broad "list everything" call cannot leak presentation URLs. Retrieve it per slideshow through [Get Slide Info](get-slideshow-details.md) or build the URL directly with [Get Slide URL](get-slideshow-url.md). |
| **`accessType` is numeric here** | In the V2 API `accessType` is the integer `0`/`1`. The older (non-V2) client APIs return the strings `"withLogin"`/`"withoutLogin"` for the same concept — do not mix the two shapes. |
| **Plan gate applies even to reading** | The slideshow plan entitlement is checked before the list is built, so this read-only API can itself fail with `6063` on a plan where slideshows are unavailable. |
| **No email-verification requirement** | Unlike the three mutating APIs, this read-only API does not require the caller's primary email to be verified. |
| **Dependency chain** | [Get Workspace List](../../workspace-management/workspace-operations/overview.md) → `<workspace-id>` → Get Slide List → `<slide-id>` for [Get Slide Info](get-slideshow-details.md) / [Get Slide URL](get-slideshow-url.md) / [Update Slide Show](update-slideshow.md) / [Delete Slide Show](delete-slideshow.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6063](../../../foundations/error-codes.md#error-6063) | 400 | `SLIDESHOW_NOT_ALLOWED` — The workspace owner's plan does not include the slideshow feature. | Upgrade the plan to one that supports slideshows. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user is neither a workspace owner nor a custom-role user with Create Slideshow permission. | Ensure the user is an Account Admin, Organization Admin, Workspace Admin, or has Create Slideshow permission on the workspace. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.embed.read`. |

# Related

- [Slideshow Management overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Slide URL](get-slideshow-url.md), [Get Slide Info](get-slideshow-details.md), [Create Slide Show](create-slideshow.md), [Update Slide Show](update-slideshow.md), [Delete Slide Show](delete-slideshow.md).
- [SDK examples](../../../sdk-examples/share-and-publish/slideshow-management/get-slideshows.md).
