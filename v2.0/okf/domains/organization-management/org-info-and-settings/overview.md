---
type: API Group
title: Organization Info & Settings
description: "APIs for retrieving organisation information, resource usage, subscription details, and workspace or view metadata."
tags:
  - zoho-analytics
  - rest-api-v2
  - organization-management
  - org-info-and-settings
  - api-group
api:
  domain: organization-management
  group: org-info-and-settings
  endpoint_count: 4
  endpoints:
    - operation_id: getOrganizations
      method: GET
      path: "/restapi/v2/orgs"
      doc: "/domains/organization-management/org-info-and-settings/get-organizations.md"
    - operation_id: getResourceDetails
      method: GET
      path: "/restapi/v2/resources"
      doc: "/domains/organization-management/org-info-and-settings/get-resource-details.md"
    - operation_id: getSubscriptionDetails
      method: GET
      path: "/restapi/v2/subscription"
      doc: "/domains/organization-management/org-info-and-settings/get-subscription-details.md"
    - operation_id: getMetaDetails
      method: GET
      path: "/restapi/v2/metadetails"
      doc: "/domains/organization-management/org-info-and-settings/get-meta-details.md"
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

These APIs provide information about the organisations, resource usage, subscription plan, and workspace/view identity lookups available to the authenticated user. They are read-only metadata APIs and do not modify any data.

---

APIs for retrieving organisation information, resource usage, subscription details, and workspace or view metadata.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Org List](get-organizations.md) | GET | `/restapi/v2/orgs` | `getOrganizations` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Resource Details](get-resource-details.md) | GET | `/restapi/v2/resources` | `getResourceDetails` | `ZohoAnalytics.usermanagement.read` | 200 |
| [Get Subscription Details](get-subscription-details.md) | GET | `/restapi/v2/subscription` | `getSubscriptionDetails` | `ZohoAnalytics.usermanagement.read` | 200 |
| [Get Meta Details From Name](get-meta-details.md) | GET | `/restapi/v2/metadetails` | `getMetaDetails` | `ZohoAnalytics.metadata.read` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# Operational Notes and Failure Cases

## Get Org List

| Scenario | Behaviour |
|----------|-----------|
| User belongs to no Zoho Analytics organisation | Returns HTTP 200 with an empty `orgs` array. No error is raised. |
| User is Account Admin in one org and a regular User in another | Both orgs appear in the list. The `role` field differs per entry. `numberOfWorkspaces` reflects all workspaces for the admin org, and only shared workspaces for the User-role org. |
| `isDefault` field | Only one entry in the list will have `isDefault: true`. This corresponds to the user's primary (default) organisation. If the user has a single org, it is always the default. |
| User is a member of an expired or blocked org | Expired/blocked orgs are suppressed from the response. Only active organisations are returned. |

## Get Resource Details

| Scenario | Behaviour |
|----------|-----------|
| `used` value is `"null"` for a resource | Indicates that usage tracking for that resource is asynchronous or not yet computed. The `remaining` value is calculated from the `allocated` limit assuming `0` actual usage. |
| `allocated` is `"Unlimited"` | The plan places no hard cap on this resource. `remaining` is also `"Unlimited"`. |
| `apiUnits` shows fractional values | API unit consumption is tracked at sub-unit precision. The `used` and `remaining` values may contain decimal values (e.g., `"23.3"`). |
| Workspace Admin or regular user calls this API | The request fails with error **7301** — this API is restricted to Account Admin and Organization Admin only. |

## Get Subscription Details

| Scenario | Behaviour |
|----------|-----------|
| Organisation is on a trial | `trialStatus` is `true` and the `trialEndsOn` field is included with the trial expiry date. `billingDate` may be `"-1"` during trial. |
| Organisation has an internal/ultimate plan | `billingDate` is `"-1"` and `trialStatus` is `false`. These plan types do not follow the standard billing cycle. |
| Organisation has no add-ons purchased | `addOns` is an empty string `""`. |
| Trial has expired | `trialStatus` returns `false`. The org may be on a restricted state. Use Get Resource Details to check current limits. |

## Get Meta Details From Name

| Scenario | Behaviour |
|----------|-----------|
| `workspaceName` is provided but the workspace does not exist in the org | Fails with error **7104**. The lookup is scoped to the organisation in `ZANALYTICS-ORGID` — a workspace by that name in a different org will not be found. |
| `viewName` is provided but the workspace exists and the view does not | Fails with error **7104** for the view. The workspace metadata is not returned in failure responses. |
| Name match is case-sensitive | `"Sales Analytics"` and `"sales analytics"` are treated as different names. Verify the exact case as it appears in the Zoho Analytics UI. |
| User has access to the workspace but not the specific view | When `viewName` is in CONFIG, security is checked specifically against the view. If the view is not accessible to the user, the request fails with error **7301** even if the user can see the workspace. |
| User is a shared user with access to only one view in the workspace | Workspace-only lookup (no `viewName`) succeeds only if the user has any view shared with them in that workspace. If the workspace has views but none are shared with the user, the request fails with **7301**. |
| Using this API to bootstrap other API calls | This is the recommended approach for name-based integrations. Call Get Meta Details From Name to resolve `workspaceId` and `viewId`, then pass those IDs to downstream APIs (Get View Details, Export Data, etc.). This avoids hard-coding numeric IDs which can change across environments. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |

# Related

- [Organization Management](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
