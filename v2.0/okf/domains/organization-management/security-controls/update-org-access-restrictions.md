---
type: API Endpoint
title: Update Org Access Restrictions
description: "Switches the organisation's access restrictions on or off and updates any of the five sections."
resource: https://analyticsapi.zoho.com/restapi/v2/security-controls/access-restrictions
tags:
  - zoho-analytics
  - rest-api-v2
  - organization-management
  - security-controls
  - put
  - metadata
api:
  operation_id: updateOrgAccessRestrictions
  method: PUT
  path: "/restapi/v2/security-controls/access-restrictions"
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
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the organisation. Workspace Admins and custom-role users are refused (7301).
  error_codes:
    - 7301
    - 8077
    - 8080
    - 8083
    - 8084
    - 8192
    - 8193
    - 8194
    - 8195
    - 8196
    - 8200
    - 8535
  openapi:
    file: "/references/openapi/org-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1security-controls~1access-restrictions/put"
    config_schema: UpdateOrgAccessRestrictionsConfig
    response_schema: null
  sdk_examples: "/sdk-examples/organization-management/security-controls/update-org-access-restrictions.md"
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

**PUT `/restapi/v2/security-controls/access-restrictions`** - Update Org Access Restrictions (Security Controls / Organization Management).

Switches the organisation's access restrictions on or off and updates any of the five sections. Returns no body. Read the current state first with [Get Org Access Restrictions](get-org-access-restrictions.md).

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `updateOrgAccessRestrictions` |
| HTTP method | PUT |
| URL | `/restapi/v2/security-controls/access-restrictions` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the organisation to update. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organisation. Workspace Admins and custom-role users are refused (7301). See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`org-management-grouped-api.json`](../../../references/openapi/org-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1security-controls~1access-restrictions/put`; CONFIG schema `UpdateOrgAccessRestrictionsConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID, shown in the Zoho Analytics UI under Settings > Organisation. See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

This endpoint has no path parameters.

## CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `accessRestrictionEnabled` | Boolean | No* | Unchanged | Master switch for the organisation. `false` stops enforcement everywhere, for the organisation and every workspace, without deleting any setting. Cannot be combined with sections when set to `false` (`8200`). While the switch is off, sections are accepted only if this attribute is `true` in the same request (`8196`). |
| `shareViews` | JSONObject | No* | Unchanged | Sharing restriction. See [`shareViews` Fields](#shareviews-fields). |
| `privateLinks` | JSONObject | No* | Unchanged | Private link settings. See [`privateLinks` Fields](#privatelinks-fields). |
| `publicViews` | JSONObject | No* | Unchanged | Public view settings. See [`publicViews` Fields](#publicviews-fields). |
| `exportViews` | JSONObject | No* | Unchanged | Export settings. Setting `enabled` to `false` also disables email views. See [`exportViews` Fields](#exportviews-fields). |
| `emailViews` | JSONObject | No* | Unchanged | Email view settings. Present at all while export is disabled → `8195`. See [`emailViews` Fields](#emailviews-fields). |

\* At least one of the six attributes must be present, and a section must contain at least one attribute to count; otherwise error [`8080`](../../../foundations/error-codes.md#error-8080). Cross-attribute rules are in [How Section Updates Are Validated](overview.md#how-section-updates-are-validated).

> `useOrganizationSettings` and `configurationSource` are workspace-level concepts and are not CONFIG attributes of this API.

### `shareViews` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `domainRestrictionEnabled` | Boolean | No | Unchanged | `true` allows sharing of views only to users from `trustedDomains`. Turning it on requires at least one trusted domain, sent now or already stored (`8193`). |
| `trustedDomains` | JSONArray of String | No | Unchanged | Complete list of trusted domains, 0–100 entries, each a domain such as `example.com`. **Replaces** the stored list. See [How Section Updates Are Validated](overview.md#how-section-updates-are-validated) for `8192` and `8193`. |

### `privateLinks` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `enabled` | Boolean | No | Unchanged | `false` stops private links from being generated. Domain attributes cannot be changed while private links are disabled (`8194`), except to switch the restriction off and clear the list in the same request. |
| `domainRestrictionEnabled` | Boolean | No | Unchanged | `true` makes private links prompt for login and admit only users from `trustedDomains`. Same list requirements as in `shareViews`. |
| `trustedDomains` | JSONArray of String | No | Unchanged | Complete list of trusted domains, 0–100 entries. **Replaces** the stored list. |

### `publicViews` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `enabled` | Boolean | No | Unchanged | `false` stops views from being made public. Domain attributes cannot be changed while public views are disabled (`8194`), except to switch the restriction off and clear the list in the same request. |
| `domainRestrictionEnabled` | Boolean | No | Unchanged | `true` makes public views prompt for login and admit only users from `trustedDomains`. Same list requirements as in `shareViews`. |
| `trustedDomains` | JSONArray of String | No | Unchanged | Complete list of trusted domains, 0–100 entries. **Replaces** the stored list. |

### `exportViews` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `enabled` | Boolean | **Yes** | — | `false` disables exporting of views and data **and** disables email views. `true` re-enables export but does **not** re-enable email views. `exportViews` has no other attribute, so an empty `exportViews` object is rejected. |

### `emailViews` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `enabled` | Boolean | No | Unchanged | `false` stops views from being emailed. Cannot be `true` in the same request that disables export (`8195`). |
| `domainRestrictionEnabled` | Boolean | No | Unchanged | `true` limits email recipients to `trustedDomains`. Same list requirements as in `shareViews`. |
| `trustedDomains` | JSONArray of String | No | Unchanged | Complete list of trusted domains, 0–100 entries. **Replaces** the stored list. |

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

# Examples

## Sample Requests

**Case 1 — Switch access restrictions on, change nothing else**

```http
PUT /restapi/v2/security-controls/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "accessRestrictionEnabled": true
}
```

**Case 2 — Configure several sections at once**

```http
PUT /restapi/v2/security-controls/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "shareViews": {
        "domainRestrictionEnabled": true,
        "trustedDomains": ["example.com", "partner.example.org"]
    },
    "privateLinks": {
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

**Case 3 — Disable access restrictions and change a section in the same request (rejected)**

```http
PUT /restapi/v2/security-controls/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "accessRestrictionEnabled": false,
    "publicViews": {
        "enabled": false
    }
}
```

## Sample Responses

**HTTP 204 No Content — Cases 1 and 2. No response body is returned on success.**

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — Failure paired with Case 3**

```json
{
    "status": "failure",
    "summary": "SECTIONS_NOT_ALLOWED_WHEN_DISABLING_ACCESS_RESTRICTION",
    "data": {
        "errorCode": 8200,
        "errorMessage": "Other settings updates are not allowed while disabling access restriction"
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Update Org Access Restrictions](../../../sdk-examples/organization-management/security-controls/update-org-access-restrictions.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success is 204 with no body** | The change is committed before the response is sent. Call [Get Org Access Restrictions](get-org-access-restrictions.md) to read it back. |
| **Idempotent** | Sending the same CONFIG twice leaves the same state and returns `204` both times. |
| **Partial update** | Omitted attributes keep their stored value. **Nothing clears on omission.** |
| **All-or-nothing** | The request runs in one transaction. A validation failure in any section, including the last, discards the whole request. |
| **Domain lists replace, not merge** | See [How Section Updates Are Validated](overview.md#how-section-updates-are-validated). Resend every domain you want to keep. |
| **Master switch off blocks section edits** | While `accessRestrictionEnabled` is `false`, a request with sections but without `accessRestrictionEnabled: true` is rejected (`8196`). Enable and configure in a single request, or enable first. |
| **Disabling the master switch is exclusive** | `accessRestrictionEnabled: false` cannot share a request with any non-empty section (`8200`). |
| **Empty section objects** | `"privateLinks": {}` changes nothing and does not count as a change for the `8080` check, but still passes through validation. |
| **Stored settings survive the master switch** | Turning the switch off retains every section value; turning it on again re-applies them. |
| **Workspace overrides are unaffected** | Changes here do not alter workspaces whose `configurationSource` is `WORKSPACE`. |
| **No dry run** | There is no validate-only mode. Settings take effect on commit. |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Responses are extensible** | Ignore unrecognised keys on error bodies rather than validating against a closed schema. |
| **Dependency chain** | [Organization Info and Settings](../org-info-and-settings/overview.md) → `ZANALYTICS-ORGID` → [Get Org Access Restrictions](get-org-access-restrictions.md) → Update Org Access Restrictions. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation. |
| [8077](../../../foundations/error-codes.md#error-8077) | 400 | `EMPTY_JSON_CONFIGURATION` — `CONFIG` is present but empty. | Send a JSON object in `CONFIG`. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — `CONFIG` is not valid JSON, or it contains neither `accessRestrictionEnabled` nor a non-empty section. | Send valid JSON with at least one attribute to change. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| [8084](../../../foundations/error-codes.md#error-8084) | 404 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| [8192](../../../foundations/error-codes.md#error-8192) | 400 | `TRUSTED_DOMAINS_WITHOUT_DOMAIN_RESTRICTION` — `trustedDomains` was sent for a section whose domain restriction is off or is being switched off. | Send `domainRestrictionEnabled: true` with the list, or send `domainRestrictionEnabled: false` with `trustedDomains: []` to clear it. |
| [8193](../../../foundations/error-codes.md#error-8193) | 400 | `TRUSTED_DOMAINS_EMPTY` — The domain restriction is on, or being switched on, but the section has no trusted domains. | Send at least one domain in `trustedDomains`, or switch the restriction off. |
| [8194](../../../foundations/error-codes.md#error-8194) | 400 | `DOMAIN_RESTRICTION_NOT_ALLOWED_WHEN_DISABLED` — Domain attributes were sent for `privateLinks`, `publicViews` or `emailViews` while that feature is disabled or is being disabled. | Enable the feature in the same request, or remove the domain attributes. |
| [8195](../../../foundations/error-codes.md#error-8195) | 400 | `EMAIL_NOT_ALLOWED_WHEN_EXPORT_DISABLED` — `emailViews` was sent while export is disabled or is being disabled, and email views would stay enabled. | Enable export in the same request, or send `emailViews: {"enabled": false}` when disabling export. |
| [8196](../../../foundations/error-codes.md#error-8196) | 400 | `ACCESS_RESTRICTION_DISABLED` — Access restriction is off for the organisation and the request carries sections without turning it on, including `accessRestrictionEnabled: false` sent with sections while it is already off. | Include `accessRestrictionEnabled: true` in the same request. |
| [8200](../../../foundations/error-codes.md#error-8200) | 400 | `SECTIONS_NOT_ALLOWED_WHEN_DISABLING_ACCESS_RESTRICTION` — `accessRestrictionEnabled: false` was sent together with a non-empty section. | Send `accessRestrictionEnabled: false` on its own. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.update`. |

# Related

- [Security Controls overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Organization Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Org Access Restrictions](get-org-access-restrictions.md), [Get Workspace Access Restrictions](get-workspace-access-restrictions.md), [Update Workspace Access Restrictions](update-workspace-access-restrictions.md).
- [SDK examples](../../../sdk-examples/organization-management/security-controls/update-org-access-restrictions.md).
