---
type: API Endpoint
title: Enable Workspace for Domain Access
description: Enables the specified workspace for access through the White Label or Client Portal domain of the organization.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/wlaccess"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - domain-and-white-label
  - post
  - metadata
api:
  operation_id: enableDomainWorkspace
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/wlaccess"
  domain: workspace-management
  group: domain-and-white-label
  oauth_scopes:
    - ZohoAnalytics.metadata.update
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin of the workspace's organisation, and the workspace's Account Admin must have a White Label / Client Portal domain configured."
  error_codes:
    - 7103
    - 7301
    - 8535
    - 12049
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1wlaccess/post"
    config_schema: null
    response_schema: null
  sdk_examples: "/sdk-examples/workspace-management/domain-and-white-label/enable-domain-workspace.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/wlaccess`** - Enable Workspace for Domain Access (Domain & White Label Access / Workspace Management).

Enables the specified workspace for access through the organisation's White Label / Client Portal domain. Once enabled, the workspace becomes visible and accessible to users who log in via the configured custom domain URL.

The portal domain is automatically resolved from the workspace's Account Admin's White Label configuration — no domain name parameter is required. Each workspace can only be associated with one portal domain (the Account Admin's configured domain).

Calling this API on a workspace that is already enabled for domain access fails with error **12049**.

> This API has no CONFIG parameter and no request body.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `enableDomainWorkspace` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/wlaccess` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the workspace's organisation, and the workspace's Account Admin must have a White Label / Client Portal domain configured. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 204 with no body |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1wlaccess/post` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | The ID of the workspace. It can be obtained using any of the workspace list APIs. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- Enable Workspace for Domain Access returns a bare HTTP 204 No Content on success. There is no response body and no **status** or **summary** JSON to parse, so check only the HTTP status code. A JSON payload is returned only on failure.
- This API requires two conditions to be met at the same time. The requesting user should be an Account Admin or an Organization Admin of the organization that owns the workspace, and the Account Admin of the workspace should have an active White Label or Client Portal domain configured for the organization. When the organization holds no White Label domain, the request fails with error code 7301 even for an Account Admin.
- The portal domain is resolved automatically from the White Label configuration of the Account Admin of the workspace. No domain name has to be passed as a parameter, and a workspace can be associated with only one portal domain.
- This API is not idempotent. Invoking it on a workspace that is already enabled for domain access fails with error code 12049. Verify the current state before invoking this API.
- A workspace is disabled for domain access by default when it is created, even in an organization that already holds a configured portal. It has to be enabled explicitly before portal users can access it.
- Each workspace has to be enabled individually. Enabling one workspace has no effect on the other workspaces of the organization.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Account Admin enabling a workspace for their portal domain**

The caller is the Account Admin who has a White Label domain (`reports.clientbrand.com`) configured. This enables the workspace so users on that portal can access it.

```http
POST /restapi/v2/workspaces/466206000000071000/wlaccess HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Organization Admin enabling a workspace on behalf of the org's portal**

An Org Admin in an organisation with an active White Label setup enabling a workspace for portal access.

```http
POST /restapi/v2/workspaces/466206000000071000/wlaccess HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

**Workspace already enabled (error)**

```json
{
  "status": "failure",
  "summary": "WORKSPACE_ALREADY_ENABLED_FOR_DOMAIN_ACCESS",
  "data": {
    "errorCode": 12049,
    "errorMessage": "The workspace is already enabled for domain access."
  }
}
```

**Caller's org has no White Label domain configured (permission error)**

```json
{
  "status": "failure",
  "summary": "SECURITY_NOT_PERMITTED",
  "data": {
    "errorCode": 7301,
    "errorMessage": "You do not have the permission to do this operation."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Enable Workspace for Domain Access](../../../sdk-examples/workspace-management/domain-and-white-label/enable-domain-workspace.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Enable Workspace for Domain Access returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The caller is not an Account Admin or Organization Admin of the workspace's organisation, **or** the workspace's Account Admin does not have a White Label / Client Portal domain configured. | Ensure the caller is an org admin and that the organisation has an active White Label domain setup. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.update`. |
| [12049](../../../foundations/error-codes.md#error-12049) | 400 | The workspace is already enabled for White Label domain access. Calling Enable on an already-enabled workspace is not idempotent. | Check the current domain access state before calling. Use Disable first if you need to re-enable (e.g., after domain reconfiguration). |

# Related

- [Domain & White Label Access overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Disable Workspace for Domain Access](disable-domain-workspace.md).
- [SDK examples](../../../sdk-examples/workspace-management/domain-and-white-label/enable-domain-workspace.md).
