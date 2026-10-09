---
type: API Endpoint
title: Get Private URL
description: "Returns the existing Private URL of a view — the open-view URL with the view's secret 32-character private key appended."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - publish
  - get
  - embed
api:
  operation_id: getPrivateUrl
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink"
  domain: share-and-publish
  group: publish
  oauth_scopes:
    - ZohoAnalytics.embed.read
  org_id_header: required
  config_parameter:
    location: query
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission on the view."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 7319
    - 8060
    - 8061
    - 8080
    - 8115
    - 8535
    - 12052
  openapi:
    file: "/references/openapi/share-publish-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1publish~1privatelink/get"
    config_schema: GetPrivateUrlConfig
    response_schema: GetPrivateUrlResponse
  sdk_examples: "/sdk-examples/share-and-publish/publish/get-private-url.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink`** - Get Private URL (Publish / Share & Publish).

Returns the existing **Private URL** of a view — the `open-view` URL with the view's secret 32-character private key appended. Read-only: it neither creates nor regenerates a key.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getPrivateUrl` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.embed.read`](../../../foundations/oauth-scopes.md#zohoanalyticsembedread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - optional |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1publish~1privatelink/get`; CONFIG schema `GetPrivateUrlConfig`; response schema `GetPrivateUrlResponse` |

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

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `domainName` | String | No | — | Client Portal / White Label domain to build the URL on. Only usable by a Client Portal admin of the workspace. Max 200 characters. Preferred over `withCustomDomain`. |
| `withCustomDomain` | Boolean | No | `false` | **Legacy flag.** If `true`, builds the URL on the workspace's configured portal domain without naming it. Requires the caller to be an Organization Admin or Super Admin **and** a Client Portal admin of the workspace. Prefer `domainName`. |

> This API has no `criteria` parameter — a private link's row filter is set when the link is created (see [Create Private URL](create-private-url.md)).

## Notes from the OpenAPI specification

- As this is a GET request, the CONFIG value must be stringified and URL encoded before it is sent.
- `CONFIG` may be omitted entirely, in which case the private URL is returned on the default domain.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get private URL"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.privateUrl` | String | The private URL of the view, in the form `https://<analytics-domain>/open-view/<view-id>/<private-key>`. `<private-key>` is a 32-character lowercase hexadecimal secret. The host is the Zoho Analytics application domain for a standard workspace, or the portal domain in a Client Portal / White Label context. **Treat this value as a secret** — anyone holding it can open the view (subject to the link's password and expiry date, if configured). |

# Examples

## Sample Requests

**Case 1 — Standard workspace (no CONFIG)**

```http
GET /restapi/v2/workspaces/137687000271334001/views/137687000006991601/publish/privatelink HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal: build the URL on a named portal domain**

```http
GET /restapi/v2/workspaces/137687000271334009/views/137687000006991777/publish/privatelink?CONFIG={"domainName":"portal.customdomain.com"} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

**Case 3 — Legacy `withCustomDomain` flag (Organization Admin who is also the portal admin)**

```http
GET /restapi/v2/workspaces/137687000271334009/views/137687000006991777/publish/privatelink?CONFIG={"withCustomDomain":true} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK — Standard workspace (Case 1)**

```json
{
    "status": "success",
    "summary": "Get private URL",
    "data": {
        "privateUrl": "https://analytics.zoho.com/open-view/137687000006991601/a23b4e7affbdcec6c12e5106e9c25f91"
    }
}
```

**HTTP 200 OK — White Label / Client Portal (Cases 2 and 3)**

```json
{
    "status": "success",
    "summary": "Get private URL",
    "data": {
        "privateUrl": "https://portal.customdomain.com/open-view/137687000006991777/062960d2243fe19312ef9d18d0b5a5b7"
    }
}
```

**HTTP 404 Not Found — The view has no private link yet**

```json
{
    "status": "failure",
    "summary": "VIEW_NOT_PUBLISHED_AS_PRIVATE",
    "data": {
        "errorCode": 8115,
        "errorMessage": "This view is not published as a private link."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Private URL](../../../sdk-examples/share-and-publish/publish/get-private-url.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Read-only — never creates a link** | If the view has no private key, this API fails with `8115` instead of generating one. Use [Create Private URL](create-private-url.md) to create the link first. |
| **Stable key** | Repeated calls return the same URL. The key changes only when [Create Private URL](create-private-url.md) is called with `regenerateKey: true`. |
| **Password and expiry are not returned here** | This API returns only the URL. To read whether a password or expiry date is configured, and whether the link has expired, use [Get Publish Configurations](get-publish-configurations.md) (`privateLinkConfig`). |
| **Expired links still return a URL** | An expired private link still has a key, so this API returns HTTP 200 with the URL. Check `privateLinkConfig.isExpired` in [Get Publish Configurations](get-publish-configurations.md) to detect expiry. |
| **No email-verification requirement** | Unlike the mutating publish APIs, this read-only API does not require the caller's primary email to be verified. |
| **`withCustomDomain` is stricter than `domainName`** | The legacy flag additionally requires the caller to be an Organization Admin or Super Admin; `domainName` only requires portal-domain admin rights. Prefer `domainName` in new integrations. |
| **Dependency chain** | [Create Private URL](create-private-url.md) → Get Private URL. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — View not found. | Verify `<view-id>` exists. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user does not have Publish permission on the view. | Ensure the user is an Account Admin, Organization Admin, Workspace Admin, or has Publish permission on the view. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The view does not belong to the specified workspace. | Ensure `<workspace-id>` and `<view-id>` are consistent. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The `domainName` supplied does not exist. | Use a domain returned by the [Domain and White Label APIs](../../workspace-management/domain-and-white-label/overview.md). |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | `DOMAIN_DOES_NOT_BELONGS_TO_USER` — The caller is not an admin of the supplied `domainName`. | Call as an admin of that portal domain, or omit `domainName`. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — CONFIG is not valid JSON or contains an unsupported key. | Send only `domainName` and/or `withCustomDomain`. |
| [8115](../../../foundations/error-codes.md#error-8115) | 404 | `VIEW_NOT_PUBLISHED_AS_PRIVATE` — The view has no private link. | Call [Create Private URL](create-private-url.md) first. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.embed.read`. |
| [12052](../../../foundations/error-codes.md#error-12052) | 400 | `WORKSPACE_NOT_ENABLED_FOR_DOMAIN_ACCESS` — The workspace is not enabled for access through the requested portal domain. | Enable the workspace for that Client Portal domain first. |

# Related

- [Publish overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Make View Public](make-views-public.md), [Remove Public Permission](remove-public-permission.md), [Create Private URL](create-private-url.md), [Remove Private Access](remove-private-access.md), [Get Publish Configurations](get-publish-configurations.md), [Update Publish Configurations](update-publish-configurations.md).
- [SDK examples](../../../sdk-examples/share-and-publish/publish/get-private-url.md).
