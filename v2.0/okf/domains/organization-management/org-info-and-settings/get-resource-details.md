---
type: API Endpoint
title: Get Resource Details
description: Returns the current resource allocation and usage statistics for the specified organisation.
resource: https://analyticsapi.zoho.com/restapi/v2/resources
tags:
  - zoho-analytics
  - rest-api-v2
  - organization-management
  - org-info-and-settings
  - get
  - usermanagement
api:
  operation_id: getResourceDetails
  method: GET
  path: "/restapi/v2/resources"
  domain: organization-management
  group: org-info-and-settings
  oauth_scopes:
    - ZohoAnalytics.usermanagement.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the specified organisation.
  error_codes:
    - 7103
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/org-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1resources/get"
    config_schema: null
    response_schema: GetResourceDetailsResponse
  sdk_examples: "/sdk-examples/organization-management/org-info-and-settings/get-resource-details.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/org-management-grouped-api.json"
    title: OpenAPI 3 specification - org-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**GET `/restapi/v2/resources`** - Get Resource Details (Organization Info & Settings / Organization Management).

Returns the current resource allocation and usage statistics for the specified organisation. This includes metrics such as user seats, row limits, API units, scheduled imports, and other plan-governed resources. Useful for monitoring usage against plan limits.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getResourceDetails` |
| HTTP method | GET |
| URL | `/restapi/v2/resources` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.usermanagement.read`](../../../foundations/oauth-scopes.md#zohoanalyticsusermanagementread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID to fetch resource details for. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the specified organisation. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`org-management-grouped-api.json`](../../../references/openapi/org-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1resources/get`; response schema `GetResourceDetailsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.usermanagement.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

This endpoint has no path parameters.

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `resourceDetails` | Array | List of resource usage objects, one per resource type. |
| `resourceDetails[].resourceName` | String | Identifier of the resource type. See the Resource Name Reference table below. |
| `resourceDetails[].resourceUsage.allocated` | String | Total allocation for this resource under the current plan. `"Unlimited"` means the plan has no cap on this resource. |
| `resourceDetails[].resourceUsage.used` | String | Amount currently consumed. May be `"null"` for resources where usage tracking is deferred (e.g., `archivedrows`). Fractional values are possible for `apiUnits`. |
| `resourceDetails[].resourceUsage.remaining` | String | Remaining allocation (`allocated - used`). `"Unlimited"` if the resource is uncapped. |
| `resourceDetails[].resourceUsage.remarks` | String | Additional context or notes about the resource limit. Empty string when no remarks apply. |

### Resource Name Reference

| `resourceName` | Description |
|----------------|-------------|
| `users` | Paid user seats (users who can create and edit views). |
| `roUsers` | Read-only/viewer user seats. |
| `workspaces` | Number of workspaces allowed in the organisation. |
| `rows` | Total number of data rows allowed across all tables. |
| `queryTables` | Number of Query Tables allowed. |
| `archivedrows` | Number of rows allowed in archived (cold storage) tables. |
| `scheduledImports` | Number of scheduled data import jobs allowed. |
| `scheduledEmails` | Number of scheduled email reports allowed per month. |
| `apiUnits` | API unit consumption quota (each API call deducts units based on operation type). |
| `scheduledAlerts` | Number of scheduled alert rules allowed. |
| `scheduledSnapshots` | Number of scheduled snapshot jobs allowed. |
| `archiveschedule` | Number of archive schedule jobs allowed. |
| `financeMultiorgImports` | Number of multi-org Finance integration import pipelines allowed. |
| `privateLinks` | Number of private link connections allowed. |
| `actionsByFlow` | Number of automated flow action triggers allowed per month. |

## Notes from the OpenAPI specification

- This API is restricted to Account Admins and Organization Admins. A Workspace Admin or a regular user receives error code 7301.
- `allocated` returns `Unlimited` when the plan places no cap on the resource. `remaining` is then also returned as `Unlimited`.
- `used` returns `null` when usage tracking for the resource is asynchronous or not yet computed, as happens with `archivedrows`. `remaining` is then calculated from `allocated` assuming zero usage.
- API unit consumption is tracked at sub-unit precision, so the `used` and `remaining` values of `apiUnits` can hold decimal values.

# Examples

## Sample Requests

**Case 1 — Account Admin checking resource usage**

```http
GET /restapi/v2/resources HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Org Admin checking usage for their org**

```http
GET /restapi/v2/resources HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Enterprise plan with mix of fixed and unlimited resources**
```json
{
  "status": "success",
  "summary": "Get resource details",
  "data": {
    "resourceDetails": [
      {
        "resourceName": "users",
        "resourceUsage": { "allocated": "15", "used": "4", "remaining": "11", "remarks": "" }
      },
      {
        "resourceName": "roUsers",
        "resourceUsage": { "allocated": "25", "used": "2", "remaining": "23", "remarks": "" }
      },
      {
        "resourceName": "workspaces",
        "resourceUsage": { "allocated": "Unlimited", "used": "1", "remaining": "Unlimited", "remarks": "" }
      },
      {
        "resourceName": "rows",
        "resourceUsage": { "allocated": "5000000", "used": "755", "remaining": "4999245", "remarks": "" }
      },
      {
        "resourceName": "queryTables",
        "resourceUsage": { "allocated": "Unlimited", "used": "0", "remaining": "Unlimited", "remarks": "" }
      },
      {
        "resourceName": "archivedrows",
        "resourceUsage": { "allocated": "500000", "used": "null", "remaining": "500000", "remarks": "" }
      },
      {
        "resourceName": "scheduledImports",
        "resourceUsage": { "allocated": "Unlimited", "used": "0", "remaining": "Unlimited", "remarks": "" }
      },
      {
        "resourceName": "scheduledEmails",
        "resourceUsage": { "allocated": "30", "used": "0", "remaining": "30", "remarks": "" }
      },
      {
        "resourceName": "apiUnits",
        "resourceUsage": { "allocated": "30000", "used": "23.3", "remaining": "29976.7", "remarks": "" }
      },
      {
        "resourceName": "scheduledAlerts",
        "resourceUsage": { "allocated": "30", "used": "0", "remaining": "30", "remarks": "" }
      },
      {
        "resourceName": "scheduledSnapshots",
        "resourceUsage": { "allocated": "Unlimited", "used": "0", "remaining": "Unlimited", "remarks": "" }
      },
      {
        "resourceName": "archiveschedule",
        "resourceUsage": { "allocated": "25", "used": "0", "remaining": "25", "remarks": "" }
      },
      {
        "resourceName": "privateLinks",
        "resourceUsage": { "allocated": "15", "used": "0", "remaining": "15", "remarks": "" }
      },
      {
        "resourceName": "actionsByFlow",
        "resourceUsage": { "allocated": "500", "used": "0", "remaining": "500", "remarks": "" }
      }
    ]
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Resource Details](../../../sdk-examples/organization-management/org-info-and-settings/get-resource-details.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Organisation not found. | Verify the `ZANALYTICS-ORGID` header value. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not an Account Admin or Organization Admin of the specified organisation. | Only Account Admins and Organization Admins can view resource details. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.usermanagement.read`. |

# Related

- [Organization Info & Settings overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Organization Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Org List](get-organizations.md), [Get Subscription Details](get-subscription-details.md), [Get Meta Details From Name](get-meta-details.md).
- [SDK examples](../../../sdk-examples/organization-management/org-info-and-settings/get-resource-details.md).
