---
type: API Endpoint
title: Get Workspace Access Restrictions
description: Returns the access restriction settings in effect for one workspace and whether they come from the organisation or from the workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions"
tags:
  - zoho-analytics
  - rest-api-v2
  - organization-management
  - security-controls
  - get
  - metadata
api:
  operation_id: getWorkspaceAccessRestrictions
  method: GET
  path: "/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions"
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
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the organisation. Workspace Admins of the workspace and custom-role users are refused (7301).
  error_codes:
    - 7301
    - 7387
    - 8083
    - 8084
    - 8535
  openapi:
    file: "/references/openapi/org-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1security-controls~1workspaces~1{workspace-id}~1access-restrictions/get"
    config_schema: null
    response_schema: GetWorkspaceAccessRestrictionsResponse
  sdk_examples: "/sdk-examples/organization-management/security-controls/get-workspace-access-restrictions.md"
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

**GET `/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions`** - Get Workspace Access Restrictions (Security Controls / Organization Management).

Returns the access restriction settings in effect for one workspace and whether they come from the organisation or from the workspace. Feeds [Update Workspace Access Restrictions](update-workspace-access-restrictions.md).

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getWorkspaceAccessRestrictions` |
| HTTP method | GET |
| URL | `/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the organisation that owns the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the organisation. Workspace Admins of the workspace and custom-role users are refused (7301). See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`org-management-grouped-api.json`](../../../references/openapi/org-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1security-controls~1workspaces~1{workspace-id}~1access-restrictions/get`; response schema `GetWorkspaceAccessRestrictionsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID, shown in the Zoho Analytics UI under Settings > Organisation. See [Identifiers](../../../foundations/identifiers.md). |

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
| `summary` | String | Localised operation summary. `"Get workspace access restrictions"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.accessRestrictionEnabled` | Boolean | The **organisation's** master switch, not a workspace setting. **Always present.** When `false`, nothing below is enforced. |
| `data.configurationSource` | String (enum) | Where the values below come from. **Always present.** See [`configurationSource` Values](#configurationsource-values). |
| `data.shareViews` | JSONObject | Sharing restriction in effect. **Always present.** Fields as in [Get Org Access Restrictions](get-org-access-restrictions.md). |
| `data.privateLinks` | JSONObject | Private link settings in effect. **Always present.** |
| `data.publicViews` | JSONObject | Public view settings in effect. **Always present.** |
| `data.exportViews` | JSONObject | Export settings in effect. **Always present.** |
| `data.emailViews` | JSONObject | Email view settings in effect. **Always present.** |

Every section has the same attributes as in [Get Org Access Restrictions](get-org-access-restrictions.md): `shareViews` carries `domainRestrictionEnabled` and `trustedDomains`; `privateLinks`, `publicViews` and `emailViews` carry `enabled`, `domainRestrictionEnabled` and `trustedDomains`; `exportViews` carries `enabled`. All are **always present**; `trustedDomains` is `[]` when empty.

### `configurationSource` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `ORG` | The workspace follows the organisation. The sections hold the **organisation's** values. | Also returned for a workspace that has never been configured. |
| `WORKSPACE` | The workspace has its own settings. The sections hold the **workspace's** values. | Set only by [Update Workspace Access Restrictions](update-workspace-access-restrictions.md) with `useOrganizationSettings: false`. |

# Examples

## Sample Requests

**Case 1 — Read a workspace's effective settings**

```http
GET /restapi/v2/security-controls/workspaces/137687000271334001/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Workspace that belongs to a different organisation (rejected)**

```http
GET /restapi/v2/security-controls/workspaces/137687000271339999/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — Workspace that follows the organisation (`configurationSource` is `ORG`)**

```json
{
    "status": "success",
    "summary": "Get workspace access restrictions",
    "data": {
        "accessRestrictionEnabled": true,
        "configurationSource": "ORG",
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

**HTTP 200 OK — Workspace with its own settings (`configurationSource` is `WORKSPACE`)**

```json
{
    "status": "success",
    "summary": "Get workspace access restrictions",
    "data": {
        "accessRestrictionEnabled": true,
        "configurationSource": "WORKSPACE",
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
            "enabled": false,
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        },
        "exportViews": {
            "enabled": false
        },
        "emailViews": {
            "enabled": false,
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        }
    }
}
```

**HTTP 400 Bad Request — Failure paired with Case 2**

```json
{
    "status": "failure",
    "summary": "DBID_NOT_BELONGS_TO_ZSOID",
    "data": {
        "errorCode": 7387,
        "errorMessage": "Workspaces(s) does not belongs to current Organization"
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Workspace Access Restrictions](../../../sdk-examples/organization-management/security-controls/get-workspace-access-restrictions.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Read-only and idempotent** | Changes nothing. |
| **Effective values, not stored values** | When `configurationSource` is `ORG`, any values previously stored for the workspace are ignored and **not** shown. They reappear only after the workspace is switched back to `WORKSPACE`. |
| **Available while the master switch is off** | Succeeds when `accessRestrictionEnabled` is `false`; the values it returns are not enforced. |
| **Workspace must belong to the organisation** | A workspace ID from another organisation is rejected with `7387`, not `404`. A non-existent ID gets the same error. |
| **Round-trip warning** | Do not send this response back to [Update Workspace Access Restrictions](update-workspace-access-restrictions.md). See [How Section Updates Are Validated](overview.md#how-section-updates-are-validated). |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Workspace Operations](../../workspace-management/workspace-operations/overview.md) → `<workspace-id>` → Get Workspace Access Restrictions → `configurationSource` and current values for [Update Workspace Access Restrictions](update-workspace-access-restrictions.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation. |
| [7387](../../../foundations/error-codes.md#error-7387) | 400 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not exist in the organisation named in `ZANALYTICS-ORGID`. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches the organisation that owns it. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| [8084](../../../foundations/error-codes.md#error-8084) | 404 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Security Controls overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Organization Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Org Access Restrictions](get-org-access-restrictions.md), [Update Org Access Restrictions](update-org-access-restrictions.md), [Update Workspace Access Restrictions](update-workspace-access-restrictions.md).
- [SDK examples](../../../sdk-examples/organization-management/security-controls/get-workspace-access-restrictions.md).
