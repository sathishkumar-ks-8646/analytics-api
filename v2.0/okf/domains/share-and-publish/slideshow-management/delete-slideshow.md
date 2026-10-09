---
type: API Endpoint
title: Delete Slide Show
description: Deletes the specified slideshow from the workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - slideshow-management
  - delete
  - embed
api:
  operation_id: deleteSlideshow
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}"
  domain: share-and-publish
  group: slideshow-management
  oauth_scopes:
    - ZohoAnalytics.embed.delete
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Slideshow permission on the workspace."
  error_codes:
    - 6063
    - 7103
    - 7301
    - 7351
    - 7565
    - 8535
  openapi:
    file: "/references/openapi/share-publish-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1slides~1{slide-id}/delete"
    config_schema: null
    response_schema: null
  sdk_examples: "/sdk-examples/share-and-publish/slideshow-management/delete-slideshow.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}`** - Delete Slide Show (Slideshow Management / Share & Publish).

Deletes a slideshow from the workspace. The views that were part of it are untouched — only the slideshow definition, its slide key, and therefore its presentation URL are removed.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deleteSlideshow` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.embed.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsembeddelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Slideshow permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 204 with no body |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1slides~1{slide-id}/delete` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.embed.delete`. See [Authentication](../../../foundations/authentication.md). |
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

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`).

# Examples

## Sample Requests

**Case 1 — Standard workspace**

```http
DELETE /restapi/v2/workspaces/137687000271334001/slides/137687000003149001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal workspace**

```http
DELETE /restapi/v2/workspaces/137687000271334009/slides/137687000003120002 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — Slideshow already deleted, or belongs to a different workspace**

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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Delete Slide Show](../../../sdk-examples/share-and-publish/slideshow-management/delete-slideshow.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Delete Slide Show returns a bare HTTP `204 No Content` — no `status`/`summary` JSON to parse. |
| **Views are not affected** | Deleting a slideshow removes only the grouping and its key. The underlying reports, dashboards, and tables remain exactly as they were, with their own sharing and publish state intact. |
| **Not idempotent** | A second delete of the same `<slide-id>` fails with `7351` `SLIDESHOW_NOT_BELONGS_TO_DB`, because the slideshow can no longer be found in the workspace. Guard repeats with a [Get Slide List](get-slideshows.md) check rather than relying on a silent success. |
| **Revokes the URL immediately** | Any presentation URL for this slideshow stops working as soon as the delete completes. There is no trash or restore path for slideshows — unlike views, which go through the [Trash APIs](../../views-management/trash-management/overview.md). |
| **Single slideshow per call** | The V2 API deletes one `<slide-id>` at a time; there is no bulk-delete payload. Loop over [Get Slide List](get-slideshows.md) to clear several. |
| **Plan gate still applies** | The slideshow plan entitlement is checked before the delete, so the call can fail with `6063` on a plan where slideshows are unavailable even though the operation is destructive rather than creative. |
| **Dependency chain** | [Get Slide List](get-slideshows.md) (confirm the slideshow exists) → Delete Slide Show. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6063](../../../foundations/error-codes.md#error-6063) | 400 | `SLIDESHOW_NOT_ALLOWED` — The workspace owner's plan does not include the slideshow feature. | Upgrade the plan to one that supports slideshows. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user is neither a workspace owner nor a custom-role user with Create Slideshow permission. | Ensure the user is an Account Admin, Organization Admin, Workspace Admin, or has Create Slideshow permission on the workspace. |
| [7351](../../../foundations/error-codes.md#error-7351) | 400 | `SLIDESHOW_NOT_BELONGS_TO_DB` — The slideshow does not exist, was already deleted, or belongs to a different workspace. | Verify `<slide-id>` against [Get Slide List](get-slideshows.md) for this workspace. |
| [7565](../../../foundations/error-codes.md#error-7565) | 400 | `UNVERIFIED_EMAIL` — The calling user's primary email address is not verified. | Verify the account's primary email address and retry. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.embed.delete`. |

# Related

- [Slideshow Management overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Slide List](get-slideshows.md), [Get Slide URL](get-slideshow-url.md), [Get Slide Info](get-slideshow-details.md), [Create Slide Show](create-slideshow.md), [Update Slide Show](update-slideshow.md).
- [SDK examples](../../../sdk-examples/share-and-publish/slideshow-management/delete-slideshow.md).
