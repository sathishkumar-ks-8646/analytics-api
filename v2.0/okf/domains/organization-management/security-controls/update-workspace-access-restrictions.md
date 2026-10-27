---
type: API Endpoint
title: Update Workspace Access Restrictions
description: "Switches one workspace between following the organisation and having its own settings, and updates the workspace's own sections."
resource: "https://analyticsapi.zoho.com/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions"
tags:
  - zoho-analytics
  - rest-api-v2
  - organization-management
  - security-controls
  - put
  - metadata
api:
  operation_id: updateWorkspaceAccessRestrictions
  method: PUT
  path: "/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions"
  domain: organization-management
  group: security-controls
  oauth_scopes:
    - ZohoAnalytics.metadata.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin of the organisation. Workspace Admins of the workspace and custom-role users are refused (7301). The organisation's accessRestrictionEnabled must be true (8197)."
  error_codes:
    - 7301
    - 7387
    - 8077
    - 8080
    - 8083
    - 8084
    - 8192
    - 8193
    - 8194
    - 8195
    - 8197
    - 8198
    - 8199
    - 8535
  openapi:
    file: "/references/openapi/org-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1security-controls~1workspaces~1{workspace-id}~1access-restrictions/put"
    config_schema: UpdateWorkspaceAccessRestrictionsConfig
    response_schema: null
  sdk_examples: "/sdk-examples/organization-management/security-controls/update-workspace-access-restrictions.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/org-management-grouped-api.json"
    title: OpenAPI 3 specification - org-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T10:58:51Z
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

**PUT `/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions`** - Update Workspace Access Restrictions (Security Controls / Organization Management).

Switches one workspace between following the organisation and having its own settings, and updates the workspace's own sections. Returns no body. Read the current state first with [Get Workspace Access Restrictions](get-workspace-access-restrictions.md), and read [Organisation and Workspace Settings Lifecycle](overview.md#organisation-and-workspace-settings-lifecycle) before the first override.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `updateWorkspaceAccessRestrictions` |
| HTTP method | PUT |
| URL | `/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the organisation that owns the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organisation. Workspace Admins of the workspace and custom-role users are refused (7301). The organisation's accessRestrictionEnabled must be true (8197). See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`org-management-grouped-api.json`](../../../references/openapi/org-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1security-controls~1workspaces~1{workspace-id}~1access-restrictions/put`; CONFIG schema `UpdateWorkspaceAccessRestrictionsConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID, shown in the Zoho Analytics UI under Settings > Organisation. See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `useOrganizationSettings` | Boolean | No* | Current mode | `false` gives the workspace its own settings; `true` makes it follow the organisation. When omitted, the workspace's current mode is kept — which means omitting it on a workspace that follows the organisation is the same as sending `true` (`8199` if sections are present). `true` cannot be combined with sections (`8198`). Setting `true` keeps the workspace's own values but ignores them. |
| `shareViews` | JSONObject | No* | Unchanged | Sharing restriction. See [`shareViews` Fields](update-org-access-restrictions.md#shareviews-fields). |
| `privateLinks` | JSONObject | No* | Unchanged | Private link settings. See [`privateLinks` Fields](update-org-access-restrictions.md#privatelinks-fields). |
| `publicViews` | JSONObject | No* | Unchanged | Public view settings. See [`publicViews` Fields](update-org-access-restrictions.md#publicviews-fields). |
| `exportViews` | JSONObject | No* | Unchanged | Export settings. Setting `enabled` to `false` also disables email views. See [`exportViews` Fields](update-org-access-restrictions.md#exportviews-fields). |
| `emailViews` | JSONObject | No* | Unchanged | Email view settings. Present at all while export is disabled → `8195`. See [`emailViews` Fields](update-org-access-restrictions.md#emailviews-fields). |

\* At least one of the six attributes must be present, and a section must contain at least one attribute to count; otherwise error [`8080`](../../../foundations/error-codes.md#error-8080). The check applies only to a workspace that follows the organisation; on a workspace that already has its own settings, an empty-but-valid `CONFIG` such as `{}` is accepted and changes nothing. Sections are accepted only when the workspace has, or is being given, its own settings.

> `accessRestrictionEnabled` is the organisation's master switch and is not a CONFIG attribute of this API. `configurationSource` appears in the response of [Get Workspace Access Restrictions](get-workspace-access-restrictions.md) only and is not a CONFIG attribute.

### `shareViews` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `domainRestrictionEnabled` | Boolean | No | Unchanged | `true` allows sharing of views in this workspace only to users from `trustedDomains`. Turning it on requires at least one trusted domain, sent now or already stored for the workspace (`8193`). |
| `trustedDomains` | JSONArray of String | No | Unchanged | Complete list of trusted domains, 0–100 entries, each a domain such as `example.com`. **Replaces** the workspace's stored list; the organisation's list is never copied or merged. See [How Section Updates Are Validated](overview.md#how-section-updates-are-validated) for `8192` and `8193`. |

### `privateLinks` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `enabled` | Boolean | No | Unchanged | `false` stops private links from being generated in this workspace. Domain attributes cannot be changed while private links are disabled (`8194`), except to switch the restriction off and clear the list in the same request. |
| `domainRestrictionEnabled` | Boolean | No | Unchanged | `true` makes private links prompt for login and admit only users from `trustedDomains`. Same list requirements as in `shareViews`. |
| `trustedDomains` | JSONArray of String | No | Unchanged | Complete list of trusted domains, 0–100 entries. **Replaces** the workspace's stored list. |

### `publicViews` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `enabled` | Boolean | No | Unchanged | `false` stops views in this workspace from being made public. Domain attributes cannot be changed while public views are disabled (`8194`), except to switch the restriction off and clear the list in the same request. |
| `domainRestrictionEnabled` | Boolean | No | Unchanged | `true` makes public views prompt for login and admit only users from `trustedDomains`. Same list requirements as in `shareViews`. |
| `trustedDomains` | JSONArray of String | No | Unchanged | Complete list of trusted domains, 0–100 entries. **Replaces** the workspace's stored list. |

### `exportViews` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `enabled` | Boolean | **Yes** | — | `false` disables exporting of views and data in this workspace **and** disables email views. `true` re-enables export but does **not** re-enable email views. `exportViews` has no other attribute, so an empty `exportViews` object is rejected. |

### `emailViews` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `enabled` | Boolean | No | Unchanged | `false` stops views in this workspace from being emailed. Cannot be `true` in the same request that disables export (`8195`). |
| `domainRestrictionEnabled` | Boolean | No | Unchanged | `true` limits email recipients to `trustedDomains`. Same list requirements as in `shareViews`. |
| `trustedDomains` | JSONArray of String | No | Unchanged | Complete list of trusted domains, 0–100 entries. **Replaces** the workspace's stored list. |

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

# Examples

## Sample Requests

**Case 1 — Give the workspace its own settings, naming the sections explicitly**

```http
PUT /restapi/v2/security-controls/workspaces/137687000271334001/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "useOrganizationSettings": false,
    "shareViews": {
        "domainRestrictionEnabled": true,
        "trustedDomains": ["example.com", "partner.example.org"]
    },
    "privateLinks": {
        "enabled": false
    },
    "publicViews": {
        "enabled": false
    },
    "exportViews": {
        "enabled": true
    },
    "emailViews": {
        "enabled": true,
        "domainRestrictionEnabled": true,
        "trustedDomains": ["example.com"]
    }
}
```

**Case 2 — Update one section on a workspace that already has its own settings**

```http
PUT /restapi/v2/security-controls/workspaces/137687000271334001/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "exportViews": {
        "enabled": false
    },
    "emailViews": {
        "enabled": false
    }
}
```

**Case 3 — Return the workspace to the organisation's settings**

```http
PUT /restapi/v2/security-controls/workspaces/137687000271334001/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "useOrganizationSettings": true
}
```

**Case 4 — Sections sent to a workspace that follows the organisation, without `useOrganizationSettings: false` (rejected)**

```http
PUT /restapi/v2/security-controls/workspaces/137687000271334001/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "publicViews": {
        "enabled": false
    }
}
```

## Sample Responses

**HTTP 204 No Content — Cases 1, 2 and 3. No response body is returned on success.**

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — Failure paired with Case 4**

```json
{
    "status": "failure",
    "summary": "WORKSPACE_SETTINGS_NOT_ENABLED",
    "data": {
        "errorCode": 8199,
        "errorMessage": "Workspace-level access restriction is not enabled for the given workspace"
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Update Workspace Access Restrictions](../../../sdk-examples/organization-management/security-controls/update-workspace-access-restrictions.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success is 204 with no body** | The change is committed before the response is sent. Call [Get Workspace Access Restrictions](get-workspace-access-restrictions.md) to read it back. |
| **Idempotent** | Sending the same CONFIG twice leaves the same state. |
| **Check order** | Caller role (`7301`) → workspace ownership (`7387`) → organisation master switch (`8197`) → empty request (`8080`) → sections without an override (`8199`) → `useOrganizationSettings: true` with sections (`8198`) → per-section rules (`8192`–`8195`). |
| **Requires the organisation master switch** | If `accessRestrictionEnabled` is `false` for the organisation, every request fails with `8197`, including `useOrganizationSettings: true`. Enable it with [Update Org Access Restrictions](update-org-access-restrictions.md) first. |
| **First override starts from defaults** | Switching a workspace that follows the organisation to `useOrganizationSettings: false` does not copy the organisation's sections. Unnamed sections start allowed and unrestricted; named sections inherit at most the organisation's flag values, never its `trustedDomains`. See [Organisation and Workspace Settings Lifecycle](overview.md#organisation-and-workspace-settings-lifecycle). |
| **Sections without the switch are rejected** | A workspace that follows the organisation cannot receive sections unless the same request sets `useOrganizationSettings: false` (`8199`). |
| **Reverting keeps workspace values** | `useOrganizationSettings: true` keeps the workspace's own values, ignores them, and cannot be sent with sections (`8198`). |
| **Partial update** | Omitted attributes keep their stored value. **Nothing clears on omission.** |
| **All-or-nothing** | One transaction; a validation failure in any section discards the whole request, including the mode switch. |
| **Domain lists replace, not merge** | See [How Section Updates Are Validated](overview.md#how-section-updates-are-validated). |
| **Organisation changes do not propagate** | A workspace with `configurationSource` `WORKSPACE` ignores later changes to the organisation's sections. |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Responses are extensible** | Ignore unrecognised keys on error bodies rather than validating against a closed schema. |
| **Dependency chain** | [Workspace Operations](../../workspace-management/workspace-operations/overview.md) → `<workspace-id>` → [Get Workspace Access Restrictions](get-workspace-access-restrictions.md) → Update Workspace Access Restrictions. For the first override, also [Get Org Access Restrictions](get-org-access-restrictions.md) for the values to copy. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation. |
| [7387](../../../foundations/error-codes.md#error-7387) | 400 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not exist in the organisation named in `ZANALYTICS-ORGID`. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches the organisation that owns it. |
| [8077](../../../foundations/error-codes.md#error-8077) | 400 | `EMPTY_JSON_CONFIGURATION` — `CONFIG` is present but empty. | Send a JSON object in `CONFIG`. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — `CONFIG` is not valid JSON, or the workspace follows the organisation and the request has neither `useOrganizationSettings` nor a non-empty section. | Send valid JSON with at least one attribute to change. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| [8084](../../../foundations/error-codes.md#error-8084) | 404 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| [8192](../../../foundations/error-codes.md#error-8192) | 400 | `TRUSTED_DOMAINS_WITHOUT_DOMAIN_RESTRICTION` — `trustedDomains` was sent for a section whose domain restriction is off or is being switched off. | Send `domainRestrictionEnabled: true` with the list, or send `domainRestrictionEnabled: false` with `trustedDomains: []` to clear it. |
| [8193](../../../foundations/error-codes.md#error-8193) | 400 | `TRUSTED_DOMAINS_EMPTY` — The domain restriction is on, or being switched on, but the section has no trusted domains. | Send at least one domain in `trustedDomains`, or switch the restriction off. |
| [8194](../../../foundations/error-codes.md#error-8194) | 400 | `DOMAIN_RESTRICTION_NOT_ALLOWED_WHEN_DISABLED` — Domain attributes were sent for `privateLinks`, `publicViews` or `emailViews` while that feature is disabled or is being disabled. | Enable the feature in the same request, or remove the domain attributes. |
| [8195](../../../foundations/error-codes.md#error-8195) | 400 | `EMAIL_NOT_ALLOWED_WHEN_EXPORT_DISABLED` — `emailViews` was sent while export is disabled or is being disabled, and email views would stay enabled. | Enable export in the same request, or send `emailViews: {"enabled": false}` when disabling export. |
| [8197](../../../foundations/error-codes.md#error-8197) | 400 | `ORG_ACCESS_RESTRICTION_NOT_ENABLED` — The organisation's `accessRestrictionEnabled` is `false`. | Enable access restrictions for the organisation with [Update Org Access Restrictions](update-org-access-restrictions.md), then retry. |
| [8198](../../../foundations/error-codes.md#error-8198) | 400 | `SECTIONS_NOT_ALLOWED_WHEN_APPLYING_ORG_SETTINGS` — `useOrganizationSettings: true` was sent together with a non-empty section. | Send `useOrganizationSettings: true` on its own. |
| [8199](../../../foundations/error-codes.md#error-8199) | 400 | `WORKSPACE_SETTINGS_NOT_ENABLED` — The workspace follows the organisation, and the request would update it without `useOrganizationSettings: false`. | Send `useOrganizationSettings: false` in the same request to give the workspace its own settings. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.update`. |

# Related

- [Security Controls overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Organization Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Org Access Restrictions](get-org-access-restrictions.md), [Update Org Access Restrictions](update-org-access-restrictions.md), [Get Workspace Access Restrictions](get-workspace-access-restrictions.md).
- [SDK examples](../../../sdk-examples/organization-management/security-controls/update-workspace-access-restrictions.md).
