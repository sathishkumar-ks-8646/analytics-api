---
type: API Endpoint
title: Fetch All Embed URLs
description: "Lists the embed URLs that have been issued for a view, together with the permission set, filter criteria, and column restrictions stored against each one."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embedurls"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - embed-url
  - get
  - embed
api:
  operation_id: getEmbedUrls
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embedurls"
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
  permission_required: "The authenticated user must be an Account Admin or Organization Admin of the organization. The caller must also hold Publish permission or Make Public permission on the view, and the organization or workspace must be enabled for Embedded Analytics, otherwise 8023."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 7319
    - 8023
    - 8080
    - 8535
  openapi:
    file: null
    pointer: null
    note: "This endpoint is documented in the markdown reference only; it is absent from the OpenAPI files."
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embedurls`** - Fetch All Embed URLs (Embed URL / Share & Publish).

Lists the embed URLs that have been issued for a view, together with the permission set, filter criteria, and column restrictions stored against each one. This is the audit and inventory call for the embed channel.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getEmbedUrls` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embedurls` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.embed.read`](../../../foundations/oauth-scopes.md#zohoanalyticsembedread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organization. The caller must also hold Publish permission or Make Public permission on the view, and the organization or workspace must be enabled for Embedded Analytics, otherwise 8023. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - optional |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | Not present in the OpenAPI files (markdown reference only). |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.embed.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | Workspace ID | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | View ID (table, report, dashboard, query table, etc.) | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

CONFIG is **optional**. Because this is a `GET`, it must be passed as a **query parameter** whose value is the stringified, **URL-encoded** JSON object.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `includeExpiredUrls` | Boolean | No | `false` | If `false` (the default), only URLs whose `expiryTime` is still in the future are returned. If `true`, **every** URL ever issued for the view is returned, including expired ones — useful for auditing what was handed out historically. |

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Fetch all embed URLs"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.embedUrls` | JSONArray | One entry per embed URL issued for the view. **Always present**; an empty array `[]` when none are outstanding (or none are unexpired, when `includeExpiredUrls` is `false`). |
| `embedUrls[].rsConfig` | String | The opaque configuration key that identifies this URL — the same value that appears as `RSCONFIG=` in the `embedUrl` returned by [Get Embed URL](get-embed-url.md), and the value to pass to [Delete Embed URL](delete-embed-url.md) to revoke this single URL. **Treat as a credential.** |
| `embedUrls[].createdBy` | String | Email address of the user who minted this URL, resolved from the stored creator ID. |
| `embedUrls[].expiryTime` | String | Epoch timestamp in **milliseconds**, serialised as a string, at which this URL stops working. Compare against the current time to tell active from expired entries — the API itself does not flag expiry, it only filters by it. |
| `embedUrls[].permissions` | JSONObject | The permission set baked into this URL. Contains exactly `read`, `export`, `vud`, `drillDown`, and `insight` (all booleans); `read` is always `true`. `drillThrough` / `accessAdminPresets` never appear, because the embed channel does not store them. |
| `embedUrls[].criteria` | String | The row-level filter bound to this URL, decrypted for this response. Empty string `""` when the URL was minted without a `criteria`. **Sensitive** — it can reveal tenant identifiers. |
| `embedUrls[].vudConfig` | JSONObject | Present **only** when the URL was minted with a VUD column restriction. Absent otherwise. |
| `vudConfig.vudConfigModel` | String | `"include"` — `vudColumns` lists the only columns visible in View Underlying Data; or `"exclude"` — `vudColumns` lists the columns hidden from it. Derived from whether `vudColumns` or `vudColumnsToExclude` was sent at mint time. |
| `vudConfig.vudTables` | JSONArray of String | IDs of the underlying tables involved in the VUD restriction. |
| `vudConfig.vudColumns` | JSONArray of String | Column **IDs** (not names) covered by the restriction, flattened across all tables in `vudTables`. Resolve to names via [Get Columns](../../data-modeling-and-schema/columns/overview.md). |
| `embedUrls[].drillConfig` | JSONObject | Present **only** when the URL was minted with a drill-down column restriction. Absent otherwise. |
| `drillConfig.drillConfigModel` | String | `"include"` — `drillColumns` lists the only drillable columns; or `"exclude"` — `drillColumns` lists the columns excluded from drill-down. |
| `drillConfig.drillColumns` | JSONArray of String | Column **IDs** (not names) covered by the drill restriction, flattened across tables. Note there is no `drillTables` counterpart to `vudConfig.vudTables`. |

# Examples

## Sample Requests

**Case 1 — Active URLs only (no CONFIG)**

```http
GET /restapi/v2/workspaces/137687000271334001/views/137687000006991601/publish/embedurls HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Include expired URLs (full audit trail)**

CONFIG (before encoding):

```json
{
    "includeExpiredUrls": true
}
```

```http
GET /restapi/v2/workspaces/137687000271334001/views/137687000006991601/publish/embedurls?CONFIG=%7B%22includeExpiredUrls%22%3Atrue%7D HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
GET /restapi/v2/workspaces/137687000271334009/views/137687000006991777/publish/embedurls HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK — Several URLs on a table view, one of them filtered (Case 1)**

```json
{
    "status": "success",
    "summary": "Fetch all embed URLs",
    "data": {
        "embedUrls": [
            {
                "rsConfig": "118b3222babc1aa5d7a19284827863e92486f8de9e2ade456527fd5cc61646fe4ab69d0e354c6f84101aa0bd686feb4f",
                "createdBy": "jane.doe@example.com",
                "expiryTime": "1753882235539",
                "permissions": {
                    "read": true,
                    "export": false,
                    "vud": false,
                    "drillDown": false,
                    "insight": false
                },
                "criteria": ""
            },
            {
                "rsConfig": "118b3222babc1aa5d7a19284827863e92486f8de9e2ade456527fd5cc61646fe38300351ec0bccb3c661c0629bab73ae",
                "createdBy": "org.admin@example.com",
                "expiryTime": "1753882235768",
                "permissions": {
                    "read": true,
                    "export": false,
                    "vud": false,
                    "drillDown": false,
                    "insight": false
                },
                "criteria": ""
            },
            {
                "rsConfig": "118b3222babc1aa5d7a19284827863e92486f8de9e2ade456527fd5cc61646fe209e57696f5f6a59c08ef093671adbe5",
                "createdBy": "jane.doe@example.com",
                "expiryTime": "1753882235943",
                "permissions": {
                    "read": true,
                    "export": false,
                    "vud": false,
                    "drillDown": false,
                    "insight": false
                },
                "criteria": "(\"Region\"='West')"
            }
        ]
    }
}
```

**HTTP 200 OK — A chart view with a VUD-restricted URL and an insights-enabled URL**

```json
{
    "status": "success",
    "summary": "Fetch all embed URLs",
    "data": {
        "embedUrls": [
            {
                "rsConfig": "118b3222babc1aa5d7a19284827863e90177da79a369e9644caccd7026a87832eac37794b628a26837ccd0b6cf0db806",
                "createdBy": "jane.doe@example.com",
                "expiryTime": "1749146566512",
                "permissions": {
                    "read": true,
                    "export": false,
                    "vud": true,
                    "drillDown": false,
                    "insight": false
                },
                "criteria": "",
                "vudConfig": {
                    "vudConfigModel": "include",
                    "vudTables": [
                        "137687000006991640",
                        "137687000006991641"
                    ],
                    "vudColumns": [
                        "137687000006991896",
                        "137687000006991897",
                        "137687000006991886",
                        "137687000006991887"
                    ]
                }
            },
            {
                "rsConfig": "118b3222babc1aa5d7a19284827863e90177da79a369e9644caccd7026a87832c980cfd5f64573dc3980b7d95df52faa",
                "createdBy": "jane.doe@example.com",
                "expiryTime": "1749146570295",
                "permissions": {
                    "read": true,
                    "export": false,
                    "vud": false,
                    "drillDown": false,
                    "insight": true
                },
                "criteria": ""
            }
        ]
    }
}
```

**HTTP 200 OK — A drill-down-restricted URL**

```json
{
    "status": "success",
    "summary": "Fetch all embed URLs",
    "data": {
        "embedUrls": [
            {
                "rsConfig": "118b3222babc1aa5d7a19284827863e9dacefb9770cf86e69cef07bcaa9dea10bc63bcbe6e32cdb49616ea6aaad9e15c",
                "createdBy": "jane.doe@example.com",
                "expiryTime": "1749146567231",
                "permissions": {
                    "read": true,
                    "export": false,
                    "vud": false,
                    "drillDown": true,
                    "insight": false
                },
                "criteria": "",
                "drillConfig": {
                    "drillConfigModel": "include",
                    "drillColumns": [
                        "137687000006991891",
                        "137687000006991894",
                        "137687000006991881",
                        "137687000006991884"
                    ]
                }
            }
        ]
    }
}
```

**HTTP 200 OK — No embed URLs outstanding for the view**

```json
{
    "status": "success",
    "summary": "Fetch all embed URLs",
    "data": {
        "embedUrls": []
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
| **Per-view, not per-workspace** | The listing covers one `<view-id>` at a time. There is no workspace-wide embed-URL inventory API — iterate over [Get View List](../../views-management/view-operations/get-views.md) to audit a whole workspace. |
| **Default hides expired URLs** | Without `includeExpiredUrls: true`, entries whose `expiryTime` has passed are filtered out server-side. A view that shows `[]` may still have historical URLs — re-query with the flag to see them. |
| **Expiry is a raw millisecond string** | `expiryTime` is not a formatted date and there is no `isExpired` boolean. Parse it as a long and compare with the current time yourself. |
| **`criteria` is returned decrypted** | The filter is stored encrypted but decrypted for this response, so the payload can expose tenant identifiers or customer names. Restrict who may call this API and avoid logging the response. |
| **`vudConfig` / `drillConfig` are conditional** | They appear only when the corresponding restriction was applied at mint time. Test for key presence rather than assuming a fixed schema. |
| **Model flags are translated for you** | The stored numeric model is converted to the readable strings `"include"` / `"exclude"` in this response — you never see the internal integer. |
| **Columns come back as IDs, not names** | Unlike the request side of [Get Embed URL](get-embed-url.md), which takes `tableName` / `columnNames`, this response returns numeric IDs as strings. Round-tripping requires resolving them via [Get Columns](../../data-modeling-and-schema/columns/overview.md). |
| **`permissions` is narrower than the sharing permission object** | Exactly five keys, always present. Do not expect the row-write, `share`, `discussion`, `drillThrough`, or preset permissions that appear in [Get Shared Details](../sharing/get-shared-details-for-views.md). |
| **The natural verification step after minting or revoking** | Calling this API immediately after [Get Embed URL](get-embed-url.md) shows the new entry; calling it after [Delete Embed URL](delete-embed-url.md) confirms the entry is gone (or that the array is now empty). |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>` → Fetch All Embed URLs → `rsConfig` → [Delete Embed URL](delete-embed-url.md). |

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
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — CONFIG is not valid JSON, was not URL-encoded correctly, or contains an unsupported key. | Send only `includeExpiredUrls`, stringified and URL-encoded. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.embed.read`. |

# Related

- [Embed URL overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Embed URL](get-embed-url.md), [Delete Embed URL](delete-embed-url.md).
