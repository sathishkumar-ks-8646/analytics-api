---
type: API Endpoint
title: Create Private URL
description: Creates a private URL for the specified view and returns it.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - publish
  - post
  - embed
api:
  operation_id: createPrivateUrl
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink"
  domain: share-and-publish
  group: publish
  oauth_scopes:
    - ZohoAnalytics.embed.update
  org_id_header: required
  config_parameter:
    location: form
    required: false
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission on the view."
  error_codes:
    - 6054
    - 6055
    - 6056
    - 6057
    - 6121
    - 6122
    - 7103
    - 7104
    - 7138
    - 7301
    - 7319
    - 7565
    - 8054
    - 8060
    - 8061
    - 8074
    - 8080
    - 8088
    - 8154
    - 8241
    - 8535
    - 12052
  openapi:
    file: "/references/openapi/share-publish-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1publish~1privatelink/post"
    config_schema: CreatePrivateUrlConfig
    response_schema: CreatePrivateUrlResponse
  sdk_examples: "/sdk-examples/share-and-publish/publish/create-private-url.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink`** - Create Private URL (Publish / Share & Publish).

Creates a **Private URL** for a view — generating the secret private key if one does not exist — and, in the same call, sets the link's permission set, row-level filter criteria, column restrictions, password, and expiry date. The freshly built private URL is returned in the response.

From the OpenAPI specification:

Creates a private URL for the specified view and returns it. The private URL can be protected with a password and given a validity period, and the permissions granted through it are controlled by the config.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createPrivateUrl` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.embed.update`](../../../foundations/oauth-scopes.md#zohoanalyticsembedupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - optional |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1publish~1privatelink/post`; CONFIG schema `CreatePrivateUrlConfig`; response schema `CreatePrivateUrlResponse` |

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
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `criteria` | String | No | `""` (no filter) | Row-level filter criteria applied to **every private-link visitor**, e.g. `"Sales_1"."Region"='West'`. Only applied when `permissions` is being (re)written — that is, on first creation or when `permissions` is present in the request. |
| `permissions` | JSONObject | No | `read: true`, everything else `false` | Read-only permission set granted to private-link visitors. `read` must not be `false` (`8074`). See [`permissions` Fields](make-views-public.md#permissions-fields) — note that `drillThrough` is always forced to `false` for a private link. |
| `includeAllColsForVUD` | Boolean | No | `false` | Applies only when `permissions.vud` is `true`. If `true`, "View Underlying Data" shows **all** columns of the underlying table instead of only the columns involved in the report. |
| `vudColumns` | JSONArray | No | — | Applies only when `permissions.vud` is `true`. Restricts "View Underlying Data" to exactly the listed columns. 1–100 entries. See [`vudColumns` / `drillColumns` Fields](make-views-public.md#vudcolumns--drillcolumns-fields). |
| `drillColumns` | JSONArray | No | — | Applies only when `permissions.drillDown` is `true`. Restricts drill-down to exactly the listed columns. When omitted, drill-down is limited to the columns involved in the report. 1–100 entries. Same shape as `vudColumns`. |
| `password` | String | No | — (no password) | Password the visitor must enter before the view is rendered. **Minimum 6 characters**, maximum 256. Setting or changing the password invalidates all existing private-link sessions. Mutually exclusive with `removePassword`. |
| `removePassword` | Boolean | No | `false` | If `true` (and `password` is not supplied), removes the existing password so the link opens without a prompt. Ignored when `password` is present. |
| `expiryDate` | String | No | — (never expires) | Date on which the link stops working, in **`dd/MM/yyyy`** format interpreted in **GMT**. The link remains usable until the end of that day. Mutually exclusive with `removeExpiryDate`. |
| `removeExpiryDate` | Boolean | No | `false` | If `true` (and `expiryDate` is not supplied), removes the existing expiry date so the link never expires. Ignored when `expiryDate` is present. |
| `regenerateKey` | Boolean | No | `false` | If `true`, discards the existing private key and generates a new one — instantly invalidating every previously distributed private URL for this view. Has no effect on first creation (a key is generated regardless). |
| `domainName` | String | No | — | Client Portal / White Label domain to build the returned URL on. Only usable by a Client Portal admin of the workspace. Max 200 characters. |
| `withCustomDomain` | Boolean | No | `false` | **Legacy flag.** If `true`, builds the returned URL on the workspace's configured portal domain without naming it. Requires the caller to be an Organization Admin or Super Admin **and** a Client Portal admin of the workspace. Prefer `domainName`. |
| `validateSystemTags` | Boolean | No | `true` | If `true`, the request is blocked with a confirmation-required error (`8241`) when the view carries a restricted **DATA_WARNING** system tag. Pass `false` to acknowledge the warning and create the link anyway. |

## Notes from the OpenAPI specification

- `CONFIG` may be omitted entirely. When it is, a private URL is created with the default settings.
- `password` and `removePassword` are mutually exclusive, as are `expiryDate` and `removeExpiryDate`.
- `vudColumns` is applicable only when the `vud` permission is set to true.
- `drillColumns` is applicable only when the `drillDown` permission is set to true.
- Setting `regenerateKey` to true disables the private link that was issued previously.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Create private URL"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.privateUrl` | String | The private URL of the view, in the form `https://<analytics-domain>/open-view/<view-id>/<private-key>`. When `regenerateKey: true` was sent, this contains the **new** key and every previously distributed URL is dead. **Treat this value as a secret.** The response never echoes back the `password` or `expiryDate` that were set — read those back via [Get Publish Configurations](get-publish-configurations.md). |

# Examples

## Sample Requests

**Case 1 — `criteria` only: create a private link restricted to a single region**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/publish/privatelink HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "criteria": "\"Sales_1\".\"Region\"='West'"
}
```

**Case 2 — Permissions clubbed together: export + VUD on selected columns + drill-down on selected columns + Zia Insights + admin presets**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991650/publish/privatelink HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "permissions": {
        "read": true,
        "export": true,
        "vud": true,
        "drillDown": true,
        "insight": true,
        "accessAdminPresets": true
    },
    "includeAllColsForVUD": false,
    "vudColumns": [
        { "tableName": "Sales_1", "columnNames": ["Product", "Region"] }
    ],
    "drillColumns": [
        { "tableName": "Sales_1", "columnNames": ["Product", "Date"] }
    ]
}
```

**Case 3 — Security options clubbed together: rotate the key, set a password, and set an expiry date**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/publish/privatelink HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "regenerateKey": true,
    "password": "Qwertyui",
    "expiryDate": "20/11/2030"
}
```

**Case 4 — White Label / Client Portal: create the link on a portal domain**

```http
POST /restapi/v2/workspaces/137687000271334009/views/137687000006991777/publish/privatelink HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "domainName": "portal.customdomain.com",
    "permissions": {
        "read": true,
        "export": true
    },
    "password": "Portal@2030",
    "validateSystemTags": false
}
```

## Sample Responses

**HTTP 200 OK — Standard workspace (Cases 1–3)**

```json
{
    "status": "success",
    "summary": "Create private URL",
    "data": {
        "privateUrl": "https://analytics.zoho.com/open-view/137687000006991601/deae5f6151ddf291528b8f11a18d3419"
    }
}
```

**HTTP 200 OK — White Label / Client Portal (Case 4)**

```json
{
    "status": "success",
    "summary": "Create private URL",
    "data": {
        "privateUrl": "https://portal.customdomain.com/open-view/137687000006991777/de59081dec264798a5475c3c2c0b43e1"
    }
}
```

**HTTP 403 Forbidden — Publish disabled for the workspace / user lacks the permission**

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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Private URL](../../../sdk-examples/share-and-publish/publish/create-private-url.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Idempotent creation, incremental update** | On a view with no private link, this API generates a key and applies the full permission set. On a view that already has a link, the key is reused (unless `regenerateKey: true`) and `permissions` / `criteria` / column restrictions are only rewritten when `permissions` is present in the request. Password and expiry are applied whenever their fields are present. |
| **`criteria` needs `permissions`** | Because the row filter is persisted as part of the private-link share record, sending `criteria` **without** `permissions` on an already-existing link leaves the criteria unchanged. Send `permissions` (at minimum `{"read": true}`) alongside `criteria` when updating an existing link. |
| **`drillThrough` is always off** | Unlike a public link, a private link can never be granted `drillThrough` — the value is forced to `false` regardless of what is sent. |
| **`password` wins over `removePassword`; `expiryDate` wins over `removeExpiryDate`** | If both are sent, the setter is applied and the remover is ignored — no error is raised. |
| **Password minimum length is enforced by the template** | A `password` shorter than 6 characters is rejected with `8080` `INVALID_JSON_CONFIGURATION`, not with a password-specific error. |
| **Setting a password kills live sessions** | Changing the password clears all existing private-link sessions, so visitors currently viewing the page must re-authenticate. |
| **`expiryDate` is GMT and end-of-day inclusive** | `"20/11/2030"` is stored as the last usable moment of 20 Nov 2030 GMT, not as midnight at its start. |
| **`regenerateKey` is destructive and immediate** | Every URL handed out earlier stops working the moment the new key is persisted. There is no grace period and no way to recover the old key. |
| **Plan limits apply to private links** | Creating a *new* private link consumes one of the organization's allotted private links (`6121` / `6122` when exhausted). Regenerating an existing key does not consume a new allotment but is itself plan-gated (`6055` / `6057`). |
| **A separate PUT endpoint also exists** | `PUT /publish/privatelink` ("Update Private Link Configurations") updates an existing private link and fails with `8115` if none exists. It is not covered by this document; this POST API covers both creation and update. |
| **Verifying the result** | The resulting private share is visible via [Get Shared Details](../sharing/get-shared-details-for-views.md) as a `shareInfo` entry with `sharedTo: "Private Link"`, `sharedToZuId: "-30"`, and `publicPermLevel: 0`; the password/expiry state is visible via [Get Publish Configurations](get-publish-configurations.md) (`privateLinkConfig`). |
| **Dependency chain** | [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>` → Create Private URL → [Get Private URL](get-private-url.md) / [Get Publish Configurations](get-publish-configurations.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6054](../../../foundations/error-codes.md#error-6054) | 400 | `PUBLISHCNT_VIOLATION` — The current plan does not allow private links. | Upgrade the plan. |
| [6055](../../../foundations/error-codes.md#error-6055) | 400 | `REGENERATE_VIOLATION` — The current plan does not allow regenerating a private-link key. | Upgrade the plan, or omit `regenerateKey`. |
| [6056](../../../foundations/error-codes.md#error-6056) | 400 | `SHAREDUSR_PUBLISHCNT_VIOLATION` — A shared user attempted a plan-restricted private-link creation. | Ask the workspace owner to create the link, or upgrade the plan. |
| [6057](../../../foundations/error-codes.md#error-6057) | 400 | `SHAREDUSR_REGENERATE_VIOLATION` — A shared user attempted a plan-restricted key regeneration. | Ask the workspace owner to regenerate the key, or upgrade the plan. |
| [6121](../../../foundations/error-codes.md#error-6121) | 400 | `EXCEEDING_USR_PLN_PRIVATE_LINKS` — The organization has used all private links allowed by its plan. | Remove an unused private link via [Remove Private Access](remove-private-access.md), or upgrade the plan. |
| [6122](../../../foundations/error-codes.md#error-6122) | 400 | `EXCEEDING_USR_PLN_PRIVATE_LINKS_DM` — Same limit, reported to a non-super-admin caller. | Ask the Organization Admin to free up a private link or upgrade the plan. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — View not found. | Verify `<view-id>` exists. |
| [7138](../../../foundations/error-codes.md#error-7138) | 400 | `META_OBJECT_NOT_PRESENT` — A `tableName` in `vudColumns` / `drillColumns` is not a table involved in this view. | Use only tables that the view actually reads from. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user does not have Publish permission on the view, or publishing is restricted for the workspace. | Ensure the user is an Account Admin, Organization Admin, Workspace Admin, or has Publish permission on the view. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The view does not belong to the specified workspace. | Ensure `<workspace-id>` and `<view-id>` are consistent. |
| [7565](../../../foundations/error-codes.md#error-7565) | 400 | `UNVERIFIED_EMAIL` — The calling user's primary email address is not verified. | Verify the account's primary email address and retry. |
| [8054](../../../foundations/error-codes.md#error-8054) | 400 | `INVALID_FILTER_CRITERIA` — `criteria` could not be parsed. | Correct the criteria syntax (e.g. `"Table"."Column"='Value'`). |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The `domainName` supplied does not exist. | Use a domain returned by the [Domain and White Label APIs](../../workspace-management/domain-and-white-label/overview.md). |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | `DOMAIN_DOES_NOT_BELONGS_TO_USER` — The caller is not an admin of the supplied `domainName`. | Call as an admin of that portal domain, or omit `domainName`. |
| [8074](../../../foundations/error-codes.md#error-8074) | 400 | `READ_PERM_SHOULD_BE_TRUE_FOR_SHARING` — `permissions.read` was sent as `false`. | Omit `read` or set it to `true`. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — CONFIG is not valid JSON, contains an unsupported key, or violates a constraint (e.g. `password` shorter than 6 characters, malformed `expiryDate`). | Send only the documented keys with the documented types and formats. |
| [8088](../../../foundations/error-codes.md#error-8088) | 400 | `SECURITY_CONTROLS_FEATURE_DISABLED` — Private links have been disabled for this organization/workspace by security controls. | Ask the Organization Admin to re-enable private links in Security Controls. |
| [8154](../../../foundations/error-codes.md#error-8154) | 400 | `COLUMN_NOT_PRESENT_IN_TABLE` — A column in `vudColumns` / `drillColumns` (or in `criteria`) does not exist in the given table. | Verify column names via [Get Columns](../../data-modeling-and-schema/columns/overview.md). |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | `SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION` — The view carries a restricted DATA_WARNING system tag. | Review the warning, then resend with `"validateSystemTags": false` to confirm. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.embed.update`. |
| [12052](../../../foundations/error-codes.md#error-12052) | 400 | `WORKSPACE_NOT_ENABLED_FOR_DOMAIN_ACCESS` — The workspace is not enabled for access through the requested portal domain. | Enable the workspace for that Client Portal domain first. |

# Related

- [Publish overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Make View Public](make-views-public.md), [Remove Public Permission](remove-public-permission.md), [Get Private URL](get-private-url.md), [Remove Private Access](remove-private-access.md), [Get Publish Configurations](get-publish-configurations.md), [Update Publish Configurations](update-publish-configurations.md).
- [SDK examples](../../../sdk-examples/share-and-publish/publish/create-private-url.md).
