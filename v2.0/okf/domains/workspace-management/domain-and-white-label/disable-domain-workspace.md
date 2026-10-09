---
type: API Endpoint
title: Disable Workspace for Domain Access
description: "Removes the specified workspace from the organisation's White Label / Client Portal domain."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/wlaccess"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - domain-and-white-label
  - delete
  - metadata
api:
  operation_id: disableDomainWorkspace
  method: DELETE
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
    - 12050
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1wlaccess/delete"
    config_schema: null
    response_schema: null
  sdk_examples: "/sdk-examples/workspace-management/domain-and-white-label/disable-domain-workspace.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

**DELETE `/restapi/v2/workspaces/{workspace-id}/wlaccess`** - Disable Workspace for Domain Access (Domain & White Label Access / Workspace Management).

Removes the specified workspace from the organisation's White Label / Client Portal domain. Once disabled, the workspace is no longer accessible to users who log in via the custom portal domain URL. Users who had access via the portal immediately lose that access.

> **Impact on portal users:** Disabling a workspace does not remove any view-level sharing or user memberships. It only gates access via the portal domain URL. The workspace and its data remain intact and accessible via the standard Zoho Analytics URL for non-portal users.

Calling this API on a workspace that is not currently enabled for domain access fails with error **12050**.

> This API has no CONFIG parameter and no request body.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `disableDomainWorkspace` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/wlaccess` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the workspace's organisation, and the workspace's Account Admin must have a White Label / Client Portal domain configured. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 204 with no body |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1wlaccess/delete` |

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

- Disable Workspace for Domain Access returns a bare HTTP 204 No Content on success. There is no response body and no **status** or **summary** JSON to parse, so check only the HTTP status code. A JSON payload is returned only on failure.
- This API requires two conditions to be met at the same time. The requesting user should be an Account Admin or an Organization Admin of the organization that owns the workspace, and the organization should hold an active White Label or Client Portal domain.
- This API is not idempotent. Invoking it on a workspace that is not currently enabled for domain access fails with error code 12050. Verify the current state before invoking this API.
- Disabling the workspace gates only the access through the portal domain URL. It does not remove any user from the workspace and does not revoke any view level sharing, and the workspace along with its data remains intact.
- Portal users who are also standard Zoho Analytics users can continue to access the workspace through the standard Zoho Analytics URL. Only the users who exist exclusively as portal users lose meaningful access.
- The view level shares are preserved. When the workspace is enabled again using the Enable Workspace for Domain Access API, the portal users regain access without any re-sharing, and the domain association is restored from the current White Label configuration of the Account Admin.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Account Admin disabling a workspace from the portal domain**

```http
DELETE /restapi/v2/workspaces/466206000000071000/wlaccess HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Organization Admin disabling a workspace from the portal**

```http
DELETE /restapi/v2/workspaces/466206000000071000/wlaccess HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

**Workspace not currently enabled for domain access (error)**

```json
{
  "status": "failure",
  "summary": "WORKSPACE_ALREADY_DISABLED_FOR_DOMAIN_ACCESS",
  "data": {
    "errorCode": 12050,
    "errorMessage": "The workspace is already disabled for domain access."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Disable Workspace for Domain Access](../../../sdk-examples/workspace-management/domain-and-white-label/disable-domain-workspace.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Disable Workspace for Domain Access returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The caller is not an Account Admin or Organization Admin of the workspace's organisation, or the organisation has no White Label domain. | Ensure the caller has admin access and the org has a configured White Label domain. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.update`. |
| [12050](../../../foundations/error-codes.md#error-12050) | 400 | The workspace is not currently enabled for White Label domain access. Calling Disable on an already-disabled workspace is not idempotent. | Verify the current state before calling. Only call Disable on workspaces previously enabled via Enable Workspace for Domain Access. |

# Related

- [Domain & White Label Access overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Enable Workspace for Domain Access](enable-domain-workspace.md).
- [SDK examples](../../../sdk-examples/workspace-management/domain-and-white-label/disable-domain-workspace.md).
