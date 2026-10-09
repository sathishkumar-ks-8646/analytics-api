---
type: API Endpoint
title: Make View Public
description: "Publishes a view as a Public URL and, in the same call, defines the read-only permission set, the row-level filter criteria, and the column restrictions that apply to public visitors."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/public"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - publish
  - post
  - embed
api:
  operation_id: makeViewsPublic
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/public"
  domain: share-and-publish
  group: publish
  oauth_scopes:
    - ZohoAnalytics.embed.create
  org_id_header: required
  config_parameter:
    location: form
    required: false
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Make Public permission on the view."
  error_codes:
    - 6054
    - 7103
    - 7104
    - 7138
    - 7301
    - 7319
    - 7500
    - 7531
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
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1publish~1public/post"
    config_schema: MakeViewsPublicConfig
    response_schema: MakeViewsPublicResponse
  sdk_examples: "/sdk-examples/share-and-publish/publish/make-views-public.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/share-publish-grouped-api.json"
    title: OpenAPI 3 specification - share-publish-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/public`** - Make View Public (Publish / Share & Publish).

Publishes a view as a **Public URL** and, in the same call, defines the read-only permission set, the row-level filter criteria, and the column restrictions that apply to public visitors. Calling it again on an already-public view **updates** the existing public share in place.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `makeViewsPublic` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/public` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.embed.create`](../../../foundations/oauth-scopes.md#zohoanalyticsembedcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Make Public permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - optional |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1publish~1public/post`; CONFIG schema `MakeViewsPublicConfig`; response schema `MakeViewsPublicResponse` |

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
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `criteria` | String | No | — (no filter) | Row-level filter criteria applied to **every public visitor**, e.g. `"Sales_1"."Region"='West'`. Uses the same syntax as the sharing/report filter criteria. Validated against the view's involved columns — an unparseable criteria or an unknown column is rejected (`8054` / `8154`). |
| `inheritParentFilterCriteria` | Boolean | No | `false` | If `true`, the public visitor additionally inherits any filter criteria already applied on the parent view, on top of `criteria`. |
| `publicPermLevel` | String (enum `1` \| `2` \| `3`) | No | `1` | Audience of the public URL. See [`publicPermLevel` Values](#publicpermlevel-values). |
| `permissions` | JSONObject | No | `read: true`, everything else `false` | Read-only permission set granted to public visitors. `read` must not be `false` (`8074`). See [`permissions` Fields](#permissions-fields). |
| `includeAllColsForVUD` | Boolean | No | `false` | Applies only when `permissions.vud` is `true`. If `true`, "View Underlying Data" shows **all** columns of the underlying table instead of only the columns involved in the report. |
| `vudColumns` | JSONArray | No | — | Applies only when `permissions.vud` is `true`. Restricts "View Underlying Data" to exactly the listed columns. 1–100 entries. See [`vudColumns` / `drillColumns` Fields](#vudcolumns--drillcolumns-fields). |
| `drillColumns` | JSONArray | No | — | Applies only when `permissions.drillDown` is `true`. Restricts drill-down to exactly the listed columns. When omitted, drill-down is limited to the columns involved in the report. 1–100 entries. Same shape as `vudColumns`. |
| `domainName` | String | No | — | Client Portal / White Label domain to publish under. Only usable by a Client Portal admin of the workspace; the returned `publicUrl` is then built on that portal domain instead of the Zoho Analytics domain. Max 200 characters. |
| `validateSystemTags` | Boolean | No | `true` | If `true`, the request is blocked with a confirmation-required error (`8241`) when the view carries a restricted **DATA_WARNING** system tag. Pass `false` to acknowledge the warning and publish anyway. |

> `isListed` (whether a public workspace appears in Zoho Analytics' public listing) is **not** accepted here — set it through [Update Publish Configurations](update-publish-configurations.md).

### `publicPermLevel` Values

| Value | Name | Meaning |
|-------|------|---------|
| `1` | Public | Anyone holding the URL, including anonymous visitors who are not signed in to Zoho. This is the default. |
| `2` | Organization Public | Only users signed in to the **same Zoho Analytics organization** as the workspace. Not available on the Free plan (`7531`). |
| `3` | Business Organization Public | Only users belonging to the **same business organization** (the parent Zoho org) as the workspace's Account Admin. Not available on the Free plan (`7531`), and the caller must belong to that same business organization (`7500`). |

> Use [Get Publish Configurations](get-publish-configurations.md) first to learn which levels are permitted for this workspace: `publicViewConfig.isOrgPublicAllowed` gates level `2` and `publicViewConfig.isBussOrgPublicAllowed` gates level `3`.
>
> In a Client Portal / White Label (custom-domain) request context, `publicPermLevel` is **forced to `1`** regardless of what is sent — the organization-scoped levels are not applicable to portal domains.

### `permissions` Fields

Only these seven fields are accepted for a public or private link. Every other permission in the general [sharing `permissions` object](../sharing/share-views.md#permissions-fields) (`addRow`, `updateRow`, `deleteRow`, `deleteAllRows`, the four `import*` modes, `share`, `discussion`, `createPreset`) is forced to `false` server-side and cannot be enabled through this API.

| Field | Type | Default | Description |
|-------|------|---------|--------------|
| `read` | Boolean | `true` | View/read access. Always granted. Explicitly sending `read: false` is rejected with `8074` `READ_PERM_SHOULD_BE_TRUE_FOR_SHARING`. |
| `export` | Boolean | `false` | Allows the visitor to export the view's data (CSV / Excel / PDF / image). |
| `vud` | Boolean | `false` | Allows "View Underlying Data" — drilling from an aggregated report into the raw rows behind it. Pair with `includeAllColsForVUD` / `vudColumns` to control which columns are exposed. |
| `drillDown` | Boolean | `false` | Allows drilling down into the view by column values. Pair with `drillColumns` to control which columns can be drilled. |
| `insight` | Boolean | `false` | Allows the visitor to view Zia Insights generated for the view. |
| `drillThrough` | Boolean | `false` | Allows drill-through actions from this view into linked views. **Public links only** — for a private link this field is always forced to `false`. |
| `accessAdminPresets` | Boolean | `false` | Allows the visitor to view/apply presets defined by the view's admin/owner. |

> For custom-role users the requested permission set is additionally **sanitised against the view type** — for example row-level or VUD permissions that make no sense for a dashboard are dropped silently rather than raising an error.

### `vudColumns` / `drillColumns` Fields

Each is a JSONArray of objects, one per underlying table referenced by the view:

| Field | Type | Mandatory | Description |
|-------|------|-----------|--------------|
| `tableName` | String | **Yes** | Name of the underlying table whose columns are being restricted. Must be a table actually involved in the view (`7138` otherwise). Max 50 characters. |
| `columnNames` | JSONArray of String | **Yes** | Column names from `tableName` to expose. 1–300 entries. Each name must exist in that table (`8154` otherwise). |

## Notes from the OpenAPI specification

- `CONFIG` may be omitted entirely. When it is, the view is published with the default settings.
- `vudColumns` is applicable only when the `vud` permission is set to true.
- `drillColumns` is applicable only when the `drillDown` permission is set to true.
- `inheritParentFilterCriteria` is applicable only for reports, not for tables.
- `validateSystemTags` is applicable only when System Tags are enabled for your organization.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Make view public"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.publicUrl` | String | The public URL of the view, in the form `https://<analytics-domain>/open-view/<view-id>`. The host is the Zoho Analytics application domain for a standard workspace, or the workspace's Client Portal / White Label domain when the call is made in a portal context or with `domainName`. **Note:** this value does not encode `publicPermLevel` — the same URL is returned for all three audience levels; the audience restriction is enforced when the URL is opened. |

# Examples

## Sample Requests

**Case 1 — `criteria` only: publish a view filtered to a single region**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/publish/public HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "criteria": "\"Sales_1\".\"Region\"='West'"
}
```

**Case 2 — Permissions clubbed together: export + VUD on selected columns + drill-down on selected columns + Zia Insights**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991650/publish/public HTTP/1.1
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
        "drillThrough": true,
        "accessAdminPresets": true
    },
    "includeAllColsForVUD": false,
    "vudColumns": [
        { "tableName": "Sales_1", "columnNames": ["Product", "Region"] }
    ],
    "drillColumns": [
        { "tableName": "Sales_1", "columnNames": ["Product", "Date"] }
    ],
    "inheritParentFilterCriteria": true
}
```

**Case 3 — Organization-only audience (`publicPermLevel: "2"`)**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/publish/public HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "publicPermLevel": "2",
    "permissions": {
        "read": true,
        "export": true
    }
}
```

**Case 4 — White Label / Client Portal: publish on a portal domain**

```http
POST /restapi/v2/workspaces/137687000271334009/views/137687000006991777/publish/public HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "domainName": "portal.customdomain.com",
    "permissions": {
        "read": true,
        "export": true,
        "vud": true
    },
    "validateSystemTags": false
}
```

## Sample Responses

**HTTP 200 OK — Standard workspace (Cases 1–3)**

```json
{
    "status": "success",
    "summary": "Make view public",
    "data": {
        "publicUrl": "https://analytics.zoho.com/open-view/137687000006991601"
    }
}
```

**HTTP 200 OK — White Label / Client Portal (Case 4)**

```json
{
    "status": "success",
    "summary": "Make view public",
    "data": {
        "publicUrl": "https://portal.customdomain.com/open-view/137687000006991777"
    }
}
```

**HTTP 403 Forbidden — Workspace not enabled for the portal domain / user lacks the permission**

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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Make View Public](../../../sdk-examples/share-and-publish/publish/make-views-public.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Create *and* update** | Although the operation type is `create`, calling this API on an already-public view **overwrites** the existing public share's permissions, criteria, and column restrictions rather than failing. There is no separate "update public link" API. |
| **Always read-only** | The permission array is sanitised to a read-only set before being persisted. Requesting write permissions has no effect — they are silently dropped, not rejected. |
| **`read` cannot be turned off** | Sending `permissions.read: false` fails with `8074`. Omitting `permissions` entirely grants read-only access. |
| **Column restrictions require the matching permission** | `vudColumns` is ignored unless `permissions.vud` is `true`; `drillColumns` is ignored unless `permissions.drillDown` is `true`. No error is raised for the ignored field. |
| **`publicPermLevel` is forced to `1` on custom domains** | In a Client Portal / White Label request context, the organization-scoped levels (`2`, `3`) are not applicable and the level is overridden to `1`. |
| **`criteria` is validated, `URLCriteria` is not the same thing** | The `criteria` here is a *share-level row filter* stored against the `Public Visitor` pseudo-user. It is unrelated to `URLCriteria` in [Update Publish Configurations](update-publish-configurations.md), which is a *URL parameter* applied when the published page is rendered. |
| **`domainName` ≠ `ZANALYTICS-DEST-ORGID`** | `domainName` scopes the operation to a Client Portal / White Label domain. It is a completely different mechanism from the `ZANALYTICS-DEST-ORGID` header used by cross-org copy operations (see [Copy Views](../../views-management/view-operations/copy-views.md)) — never substitute one for the other. |
| **Verifying the result** | The resulting public share is visible via [Get Shared Details](../sharing/get-shared-details-for-views.md) as a `shareInfo` entry with `sharedTo: "Public Visitor"`, `sharedToZuId: "-20"`, and `publicPermLevel` set to the audience level; and via [Get Publish Configurations](get-publish-configurations.md) as `publicViewConfig.publicPermLevel`. |
| **Dependency chain** | [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>` → (optional) [Get Publish Configurations](get-publish-configurations.md) to check allowed audience levels → Make View Public. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6054](../../../foundations/error-codes.md#error-6054) | 400 | `PUBLISHCNT_VIOLATION` — The current plan does not allow this publish operation. | Upgrade the plan, or publish as a private link instead. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — View not found. | Verify `<view-id>` exists. |
| [7138](../../../foundations/error-codes.md#error-7138) | 400 | `META_OBJECT_NOT_PRESENT` — A `tableName` in `vudColumns` / `drillColumns` is not a table involved in this view. | Use only tables that the view actually reads from. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user cannot make this view public (no Make Public permission, or the workspace/view is restricted). | Ensure the user is an Account Admin, Organization Admin, Workspace Admin, or has Make Public permission on the view. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The view does not belong to the specified workspace. | Ensure `<workspace-id>` and `<view-id>` are consistent. |
| [7500](../../../foundations/error-codes.md#error-7500) | 400 | `UNAUTHORIZED_ORG_CANNOT_MAKEPUBLIC` — `publicPermLevel: "3"` requested but the caller does not belong to the workspace admin's business organization. | Use `publicPermLevel` `1` or `2`, or call as a user of the same business organization. |
| [7531](../../../foundations/error-codes.md#error-7531) | 400 | `PUBLIC_TO_ORG_NOT_SUPPORTED_IN_FREE` — `publicPermLevel` `2` or `3` is not supported on the Free plan. | Upgrade the plan, or use `publicPermLevel: "1"`. |
| [7565](../../../foundations/error-codes.md#error-7565) | 400 | `UNVERIFIED_EMAIL` — The calling user's primary email address is not verified. | Verify the account's primary email address and retry. |
| [8054](../../../foundations/error-codes.md#error-8054) | 400 | `INVALID_FILTER_CRITERIA` — `criteria` could not be parsed. | Correct the criteria syntax (e.g. `"Table"."Column"='Value'`). |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The `domainName` supplied does not exist. | Use a domain returned by the [Domain and White Label APIs](../../workspace-management/domain-and-white-label/overview.md). |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | `DOMAIN_DOES_NOT_BELONGS_TO_USER` — The caller is not an admin of the supplied `domainName`. | Call as an admin of that portal domain, or omit `domainName`. |
| [8074](../../../foundations/error-codes.md#error-8074) | 400 | `READ_PERM_SHOULD_BE_TRUE_FOR_SHARING` — `permissions.read` was sent as `false`. | Omit `read` or set it to `true`. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — CONFIG is not valid JSON, contains an unsupported key, or violates a type/length/allowed-value constraint (e.g. `publicPermLevel` outside `1`/`2`/`3`). | Send only the documented keys with the documented types. |
| [8088](../../../foundations/error-codes.md#error-8088) | 400 | `SECURITY_CONTROLS_FEATURE_DISABLED` — Public sharing has been disabled for this organization/workspace by security controls. | Ask the Organization Admin to re-enable public sharing in Security Controls. |
| [8154](../../../foundations/error-codes.md#error-8154) | 400 | `COLUMN_NOT_PRESENT_IN_TABLE` — A column in `vudColumns` / `drillColumns` (or in `criteria`) does not exist in the given table. | Verify column names via [Get Columns](../../data-modeling-and-schema/columns/overview.md). |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | `SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION` — The view carries a restricted DATA_WARNING system tag. | Review the warning, then resend with `"validateSystemTags": false` to confirm. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.embed.create`. |
| [12052](../../../foundations/error-codes.md#error-12052) | 400 | `WORKSPACE_NOT_ENABLED_FOR_DOMAIN_ACCESS` — The workspace is not enabled for access through the requested portal domain. | Enable the workspace for that Client Portal domain first. |

# Related

- [Publish overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Remove Public Permission](remove-public-permission.md), [Get Private URL](get-private-url.md), [Create Private URL](create-private-url.md), [Remove Private Access](remove-private-access.md), [Get Publish Configurations](get-publish-configurations.md), [Update Publish Configurations](update-publish-configurations.md).
- [SDK examples](../../../sdk-examples/share-and-publish/publish/make-views-public.md).
