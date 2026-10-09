---
type: API Endpoint
title: Get Subscription Details
description: "Returns the current subscription plan, add-on details, billing date, and trial status for the specified organisation."
resource: https://analyticsapi.zoho.com/restapi/v2/subscription
tags:
  - zoho-analytics
  - rest-api-v2
  - organization-management
  - org-info-and-settings
  - get
  - usermanagement
api:
  operation_id: getSubscriptionDetails
  method: GET
  path: "/restapi/v2/subscription"
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
    pointer: "#/paths/~1restapi~1v2~1subscription/get"
    config_schema: null
    response_schema: GetSubscriptionDetailsResponse
  sdk_examples: "/sdk-examples/organization-management/org-info-and-settings/get-subscription-details.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/org-management-grouped-api.json"
    title: OpenAPI 3 specification - org-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

**GET `/restapi/v2/subscription`** - Get Subscription Details (Organization Info & Settings / Organization Management).

Returns the current subscription plan, add-on details, billing date, and trial status for the specified organisation.

> This API has no CONFIG parameter.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getSubscriptionDetails` |
| HTTP method | GET |
| URL | `/restapi/v2/subscription` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.usermanagement.read`](../../../foundations/oauth-scopes.md#zohoanalyticsusermanagementread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID to fetch subscription details for. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the specified organisation. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`org-management-grouped-api.json`](../../../references/openapi/org-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1subscription/get`; response schema `GetSubscriptionDetailsResponse` |

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
| `subscription.planName` | String | Name of the active subscription plan (e.g., `"Basic"`, `"Standard"`, `"Premium"`, `"Enterprise"`, `"Ultimate"`). |
| `subscription.addOns` | String | Description of any add-on purchases (e.g., `"25 Viewers"`). Empty string if no add-ons are active. |
| `subscription.billingDate` | String | Next billing/renewal date in human-readable format (e.g., `"22 Jun 2021"`). Returns `"-1"` if the plan is on a trial, is an internal plan with no billing cycle, or the billing date is not applicable. |
| `subscription.trialStatus` | Boolean | `true` if the organisation is currently on an active trial period. `false` otherwise. |
| `subscription.trialEndsOn` | String | *(Present only when `trialStatus` is `true`)* The date and time when the trial period ends. Format: standard Java date string. |

## Notes from the OpenAPI specification

- This API is restricted to Account Admins and Organization Admins. Any other role receives error code 7301.
- When the organisation is on a trial, `trialStatus` returns true and `trialEndsOn` is included in the response. `billingDate` can return `-1` during the trial.
- Internal and ultimate plans do not follow the standard billing cycle. For these plans `billingDate` returns `-1` and `trialStatus` returns false.
- When a trial has expired, `trialStatus` returns false and the organisation can be in a restricted state. Use the Get Resource Details API to check the current limits.
- `addOns` returns an empty string when no add-ons have been purchased.

# Examples

## Sample Requests

**Case 1 — Account Admin checking subscription for their org**

```http
GET /restapi/v2/subscription HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Org Admin checking subscription for the org they manage**

```http
GET /restapi/v2/subscription HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK**

**Case 1 — Premium plan, active subscription with add-ons, not on trial**
```json
{
  "status": "success",
  "summary": "Get subscription details",
  "data": {
    "subscription": {
      "planName": "Premium",
      "addOns": "25 Viewers",
      "billingDate": "22 Jun 2021",
      "trialStatus": false
    }
  }
}
```

**Case 2 — Organisation on a trial period (includes `trialEndsOn`)**
```json
{
  "status": "success",
  "summary": "Get subscription details",
  "data": {
    "subscription": {
      "planName": "Enterprise",
      "addOns": "",
      "billingDate": "-1",
      "trialStatus": true,
      "trialEndsOn": "Sat Jul 15 23:59:59 IST 2026"
    }
  }
}
```

**Case 3 — Internal/Ultimate plan (no billing date)**
```json
{
  "status": "success",
  "summary": "Get subscription details",
  "data": {
    "subscription": {
      "planName": "Ultimate",
      "addOns": "",
      "billingDate": "-1",
      "trialStatus": false
    }
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Subscription Details](../../../sdk-examples/organization-management/org-info-and-settings/get-subscription-details.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Organisation not found. | Verify the `ZANALYTICS-ORGID` header value. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not an Account Admin or Organization Admin of the specified organisation. | Only Account Admins and Organization Admins can view subscription details. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.usermanagement.read`. |

# Related

- [Organization Info & Settings overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Organization Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Org List](get-organizations.md), [Get Resource Details](get-resource-details.md), [Get Meta Details From Name](get-meta-details.md).
- [SDK examples](../../../sdk-examples/organization-management/org-info-and-settings/get-subscription-details.md).
