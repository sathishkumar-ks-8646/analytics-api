---
type: API Endpoint
title: Get Org Access Restrictions
description: "Returns the organisation's access restriction settings: the master switch and the five sections."
resource: https://analyticsapi.zoho.com/restapi/v2/security-controls/access-restrictions
tags:
  - zoho-analytics
  - rest-api-v2
  - organization-management
  - security-controls
  - get
  - metadata
api:
  operation_id: getOrgAccessRestrictions
  method: GET
  path: "/restapi/v2/security-controls/access-restrictions"
  domain: organization-management
  group: security-controls
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the organisation. Workspace Admins and custom-role users are refused (7301).
  error_codes:
    - 7301
    - 8083
    - 8084
    - 8535
  openapi:
    file: "/references/openapi/org-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1security-controls~1access-restrictions/get"
    config_schema: null
    response_schema: GetOrgAccessRestrictionsResponse
  sdk_examples: "/sdk-examples/organization-management/security-controls/get-org-access-restrictions.md"
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

**GET `/restapi/v2/security-controls/access-restrictions`** - Get Org Access Restrictions (Security Controls / Organization Management).

Returns the organisation's access restriction settings: the master switch and the five sections. Feeds [Update Org Access Restrictions](update-org-access-restrictions.md) and supplies the values to copy when overriding a workspace.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getOrgAccessRestrictions` |
| HTTP method | GET |
| URL | `/restapi/v2/security-controls/access-restrictions` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the organisation to read. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organisation. Workspace Admins and custom-role users are refused (7301). See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`org-management-grouped-api.json`](../../../references/openapi/org-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1security-controls~1access-restrictions/get`; response schema `GetOrgAccessRestrictionsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID, shown in the Zoho Analytics UI under Settings > Organisation. See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

This endpoint has no path parameters.

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get org access restrictions"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.accessRestrictionEnabled` | Boolean | The master switch. **Always present.** `false` for an organisation that has never configured access restrictions. When `false`, none of the settings below are enforced. |
| `data.shareViews` | JSONObject | Sharing restriction. **Always present.** |
| `data.shareViews.domainRestrictionEnabled` | Boolean | `true` when views can be shared only to users from `trustedDomains`. **Always present.** |
| `data.shareViews.trustedDomains` | JSONArray of String | Trusted domains for sharing. **Always present**; `[]` when none. Returned even when `domainRestrictionEnabled` is `false`. |
| `data.privateLinks` | JSONObject | Private link settings. **Always present.** |
| `data.privateLinks.enabled` | Boolean | `true` when private links can be generated. **Always present.** |
| `data.privateLinks.domainRestrictionEnabled` | Boolean | `true` when private links admit only users from `trustedDomains`. **Always present.** |
| `data.privateLinks.trustedDomains` | JSONArray of String | Trusted domains for private links. **Always present**; `[]` when none. |
| `data.publicViews` | JSONObject | Public view settings. **Always present.** |
| `data.publicViews.enabled` | Boolean | `true` when views can be made public. **Always present.** |
| `data.publicViews.domainRestrictionEnabled` | Boolean | `true` when public views admit only users from `trustedDomains`. **Always present.** |
| `data.publicViews.trustedDomains` | JSONArray of String | Trusted domains for public views. **Always present**; `[]` when none. |
| `data.exportViews` | JSONObject | Export settings. **Always present.** |
| `data.exportViews.enabled` | Boolean | `true` when views and data can be exported. **Always present.** |
| `data.emailViews` | JSONObject | Email view settings. **Always present.** |
| `data.emailViews.enabled` | Boolean | `true` when views can be emailed. **Always present.** Reports `false` after export has been disabled. |
| `data.emailViews.domainRestrictionEnabled` | Boolean | `true` when emails can go only to `trustedDomains`. **Always present.** |
| `data.emailViews.trustedDomains` | JSONArray of String | Trusted domains for email. **Always present**; `[]` when none. |

# Examples

## Sample Requests

**Case 1 — Read the organisation's settings**

```http
GET /restapi/v2/security-controls/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
GET /restapi/v2/security-controls/access-restrictions HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — Restrictions enabled, private links disabled, domain restrictions on sharing and email**

```json
{
    "status": "success",
    "summary": "Get org access restrictions",
    "data": {
        "accessRestrictionEnabled": true,
        "shareViews": {
            "domainRestrictionEnabled": true,
            "trustedDomains": [
                "example.com",
                "partner.example.org"
            ]
        },
        "privateLinks": {
            "enabled": false,
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        },
        "publicViews": {
            "enabled": true,
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        },
        "exportViews": {
            "enabled": true
        },
        "emailViews": {
            "enabled": true,
            "domainRestrictionEnabled": true,
            "trustedDomains": [
                "example.com"
            ]
        }
    }
}
```

**HTTP 200 OK — Organisation that has never configured access restrictions**

```json
{
    "status": "success",
    "summary": "Get org access restrictions",
    "data": {
        "accessRestrictionEnabled": false,
        "shareViews": {
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        },
        "privateLinks": {
            "enabled": true,
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        },
        "publicViews": {
            "enabled": true,
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        },
        "exportViews": {
            "enabled": true
        },
        "emailViews": {
            "enabled": true,
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        }
    }
}
```

**HTTP 403 Forbidden — Failure paired with Case 2**

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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Org Access Restrictions](../../../sdk-examples/organization-management/security-controls/get-org-access-restrictions.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Read-only and idempotent** | Changes nothing. Repeating the call returns the current state. |
| **All sections, always** | Every section and every attribute is returned on every call, including attributes of disabled features. There is no way to request a subset. |
| **Stored values are returned even when not enforced** | With `accessRestrictionEnabled: false`, the sections still show their stored values. Read the master switch first. |
| **Domain order is not guaranteed** | Compare `trustedDomains` as sets. |
| **Never-configured organisation** | Returns the second sample above — not an error. |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Organization Info and Settings](../org-info-and-settings/overview.md) → `ZANALYTICS-ORGID` → Get Org Access Restrictions → current values for [Update Org Access Restrictions](update-org-access-restrictions.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| [8084](../../../foundations/error-codes.md#error-8084) | 404 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Security Controls overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Organization Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Update Org Access Restrictions](update-org-access-restrictions.md), [Get Workspace Access Restrictions](get-workspace-access-restrictions.md), [Update Workspace Access Restrictions](update-workspace-access-restrictions.md).
- [SDK examples](../../../sdk-examples/organization-management/security-controls/get-org-access-restrictions.md).
