---
type: API Endpoint
title: Delete Embed URL
description: "Revokes embed URLs for a view — either one specific URL identified by its rsConfig key, or every URL issued for the view."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embed"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - embed-url
  - delete
  - embed
api:
  operation_id: deleteEmbedUrl
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embed"
  domain: share-and-publish
  group: embed-url
  oauth_scopes:
    - ZohoAnalytics.embed.delete
  org_id_header: required
  config_parameter:
    location: form
    required: true
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin of the organization. The caller must also hold Publish permission or Make Public permission on the view, and the organization or workspace must be enabled for Embedded Analytics, otherwise 8023."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 7319
    - 8023
    - 8080
    - 8175
    - 8176
    - 8178
    - 8535
  openapi:
    file: null
    pointer: null
    note: "This endpoint is documented in the markdown reference only; it is absent from the OpenAPI files."
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**DELETE `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embed`** - Delete Embed URL (Embed URL / Share & Publish).

Revokes embed URLs for a view — either one specific URL identified by its `rsConfig` key, or every URL issued for the view. Revocation is immediate; the URL stops rendering on the next request.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deleteEmbedUrl` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embed` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.embed.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsembeddelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organization. The caller must also hold Publish permission or Make Public permission on the view, and the organization or workspace must be enabled for Embedded Analytics, otherwise 8023. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Success response | HTTP 204 with no body |
| OpenAPI | Not present in the OpenAPI files (markdown reference only). |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.embed.delete`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | Workspace ID | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | View ID (table, report, dashboard, query table, etc.) | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

CONFIG is **mandatory** for this API, and exactly one of the two fields below must be supplied.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `rsConfig` | String | Conditional* | — | The configuration key of the single embed URL to revoke, as returned by [Fetch All Embed URLs](get-embed-urls.md) (`embedUrls[].rsConfig`) or taken from the `RSCONFIG=` parameter of an `embedUrl`. Max 1,000 characters. If no URL matches this key for the view, the call fails with `8175`. |
| `deleteAllUrls` | Boolean | Conditional* | `false` | If `true`, revokes **every** embed URL issued for the view, expired ones included. If the view has no embed URLs at all, the call fails with `8176`. |

\* **Exactly one** of `rsConfig` or `deleteAllUrls: true` must be sent. Supplying both, or neither, fails with [`8178`](../../../foundations/error-codes.md#error-8178) `INVALID_DELETE_EMBED_URL_CONFIGURATION`. Note that sending `rsConfig` together with `deleteAllUrls: false` is valid — the flag is only "set" when it is `true`.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`). To confirm what remains, call [Fetch All Embed URLs](get-embed-urls.md).

# Examples

## Sample Requests

**Case 1 — Revoke one specific embed URL by its key**

```http
DELETE /restapi/v2/workspaces/137687000271334001/views/137687000006991601/publish/embed HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "rsConfig": "118b3222babc1aa5d7a19284827863e92486f8de9e2ade456527fd5cc61646fe4ab69d0e354c6f84101aa0bd686feb4f"
}
```

**Case 2 — Revoke every embed URL for the view**

```http
DELETE /restapi/v2/workspaces/137687000271334001/views/137687000006991601/publish/embed HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "deleteAllUrls": true
}
```

**Case 3 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
DELETE /restapi/v2/workspaces/137687000271334009/views/137687000006991777/publish/embed HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "deleteAllUrls": true
}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code, then confirm with [Fetch All Embed URLs](get-embed-urls.md).

```
HTTP/1.1 204 No Content
```

**HTTP 404 Not Found — `deleteAllUrls` on a view that has no embed URLs**

```json
{
    "status": "failure",
    "summary": "OEM_VIEW_HOLD_NO_KEYS",
    "data": {
        "errorCode": 8176,
        "errorMessage": "No embed URLs are associated with the specified view."
    }
}
```

**HTTP 404 Not Found — `rsConfig` does not match any URL on this view**

```json
{
    "status": "failure",
    "summary": "OEM_KEY_NOT_PRESENT",
    "data": {
        "errorCode": 8175,
        "errorMessage": "The specified embed URL key is not present."
    }
}
```

**HTTP 400 Bad Request — Both `rsConfig` and `deleteAllUrls: true` sent (or neither)**

```json
{
    "status": "failure",
    "summary": "INVALID_DELETE_EMBED_URL_CONFIGURATION",
    "data": {
        "errorCode": 8178,
        "errorMessage": "Invalid configuration for deleting the embed URL."
    }
}
```

**HTTP 403 Forbidden — Request sent through a Client Portal / White Label domain (Case 3)**

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

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Delete Embed URL returns a bare HTTP `204 No Content` — no `status`/`summary` JSON, and no count of how many URLs were removed. |
| **Two mutually exclusive modes** | Targeted (`rsConfig`) and bulk (`deleteAllUrls: true`). Supplying both or neither is rejected with `8178`, so the caller must decide explicitly — there is no default mode. |
| **Not idempotent in either mode** | A repeat targeted delete fails with `8175` (`OEM_KEY_NOT_PRESENT`); a repeat bulk delete fails with `8176` (`OEM_VIEW_HOLD_NO_KEYS`). Both are "nothing to delete" conditions reported as errors, not silent successes. Guard retries with [Fetch All Embed URLs](get-embed-urls.md). |
| **Bulk mode also clears expired URLs** | `deleteAllUrls: true` removes every stored configuration for the view regardless of `expiryTime`, so it also wipes the historical audit trail that `includeExpiredUrls: true` would otherwise show. |
| **Revocation is immediate and irreversible** | The stored configuration is deleted, so the URL can no longer be resolved. There is no restore path — a replacement must be minted with [Get Embed URL](get-embed-url.md), which produces a different `RSCONFIG` key. |
| **Only the embed channel is affected** | Public URLs, private URLs, slideshows, and ordinary user/group shares on the same view are untouched. Use [Remove Public Permission](../publish/remove-public-permission.md) / [Remove Private Access](../publish/remove-private-access.md) for those. |
| **Deleting a URL does not delete the view** | Only the issued access URLs are removed; the view, its data, and its definition are unchanged. |
| **CONFIG travels in the body, not the query string** | Unlike the two GET APIs in this family, this DELETE takes CONFIG as a form-encoded body parameter, so no URL encoding of the JSON is needed. |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | [Fetch All Embed URLs](get-embed-urls.md) → `rsConfig` → Delete Embed URL → [Fetch All Embed URLs](get-embed-urls.md) to verify. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — View not found. | Verify `<view-id>` exists in the workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The request came through a Client Portal / White Label domain (where this API is disabled), or the caller is not an Account Admin / Organization Admin, or lacks Publish / Make Public permission on the view. | Call from the standard API host as an Account Admin or Organization Admin. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The view does not belong to the specified workspace. | Ensure `<workspace-id>` and `<view-id>` are consistent. |
| [8023](../../../foundations/error-codes.md#error-8023) | 403 | `OEM_OPERATION_NOT_ALLOWED` — The organization/workspace is not enabled for Embedded Analytics. | Embedded Analytics must be enabled for the account; contact Zoho Analytics support/sales. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — CONFIG is missing, is not valid JSON, contains an unsupported key, or `rsConfig` exceeds 1,000 characters. | Send a valid CONFIG containing only `rsConfig` or `deleteAllUrls`. |
| [8175](../../../foundations/error-codes.md#error-8175) | 404 | `OEM_KEY_NOT_PRESENT` — No embed URL on this view matches the supplied `rsConfig`. | Re-read the current keys via [Fetch All Embed URLs](get-embed-urls.md). |
| [8176](../../../foundations/error-codes.md#error-8176) | 404 | `OEM_VIEW_HOLD_NO_KEYS` — `deleteAllUrls` was requested but the view has no embed URLs. | Confirm the view has outstanding URLs via [Fetch All Embed URLs](get-embed-urls.md) with `includeExpiredUrls: true`. |
| [8178](../../../foundations/error-codes.md#error-8178) | 400 | `INVALID_DELETE_EMBED_URL_CONFIGURATION` — Both `rsConfig` and `deleteAllUrls: true` were sent, or neither was. | Send exactly one of the two. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.embed.delete`. |

# Related

- [Embed URL overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Embed URL](get-embed-url.md), [Fetch All Embed URLs](get-embed-urls.md).
