---
type: API Group
title: Domain & White Label Access
description: APIs that control whether a workspace is reachable through the White Label or Client Portal domain of the organization.
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - domain-and-white-label
  - api-group
api:
  domain: workspace-management
  group: domain-and-white-label
  endpoint_count: 2
  endpoints:
    - operation_id: enableDomainWorkspace
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/wlaccess"
      doc: "/domains/workspace-management/domain-and-white-label/enable-domain-workspace.md"
    - operation_id: disableDomainWorkspace
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/wlaccess"
      doc: "/domains/workspace-management/domain-and-white-label/disable-domain-workspace.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

These APIs control whether a specific workspace is accessible through the organisation's **White Label / Client Portal** domain. When enabled, the workspace (and its shared views) becomes reachable by users who log in via the configured custom portal domain URL (e.g., `https://reports.clientbrand.com`). When disabled, the workspace is hidden from the portal domain — portal users can no longer access it through the custom domain URL.

---

APIs that control whether a workspace is reachable through the White Label or Client Portal domain of the organization. A workspace is disabled for domain access when it is created and has to be enabled explicitly before the portal users can access it.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Enable Workspace for Domain Access](enable-domain-workspace.md) | POST | `/restapi/v2/workspaces/{workspace-id}/wlaccess` | `enableDomainWorkspace` | `ZohoAnalytics.metadata.update` | 204 |
| [Disable Workspace for Domain Access](disable-domain-workspace.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/wlaccess` | `disableDomainWorkspace` | `ZohoAnalytics.metadata.update` | 204 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# Prerequisites and Concepts

## White Label / Client Portal

White Label (also known as Client Portal) is a Zoho Analytics feature that allows organisations to embed analytics under their own branded domain. The Account Admin configures a custom domain (e.g., `reports.clientbrand.com`) through Zoho Analytics settings. Users can then access Zoho Analytics dashboards and reports via that branded domain without seeing Zoho branding.

## Workspace Domain Access

By default, a workspace is **not enabled** for White Label domain access after creation. An admin must explicitly enable it using the **Enable Workspace for Domain Access** API before portal users can access it through the custom domain. This allows fine-grained control over which workspaces are exposed through the portal.

- **Enabled:** The workspace is listed and accessible when users log in through the portal domain URL. Views shared with portal users appear under the custom domain.
- **Disabled:** The workspace is invisible to users accessing via the portal domain. It is still fully accessible via the standard `analyticsapi.zoho.com` URL for non-portal users.

## Permission Requirements for These APIs

These APIs require **two conditions** to be met simultaneously:

1. **The caller** must be an Account Admin or Organization Admin of the workspace's organisation.
2. **The workspace's Account Admin** must have an active White Label / Client Portal domain configured for the organisation.

If the organisation has no White Label domain set up, these APIs will return a permission error even for Account Admins — there is no portal domain to enable or disable the workspace for.

---

# Operational Notes and Failure Cases

## White Label Prerequisites

| Condition | Required For |
|-----------|-------------|
| Organisation has a White Label / Client Portal domain configured | **Mandatory** for both APIs. Without this, even Account Admins get a 7301 error. |
| Caller is Account Admin or Org Admin | **Mandatory**. Regular Workspace Admins and shared users cannot call these APIs. |
| Domain is automatically resolved | The portal domain is resolved from the workspace's Account Admin's White Label configuration — it is not passed as a parameter. An org can have at most one associated portal domain per workspace. |

## Enable Workspace for Domain Access

| Scenario | Behaviour |
|----------|-----------|
| Workspace not yet enabled | Domain ID is written to the workspace's domain configuration. Portal users can now access the workspace via the custom domain URL. |
| Workspace already enabled | **Fails with error 12049.** Unlike similar toggle APIs (e.g., favourites), this is not idempotent. Check current state before calling. |
| Organisation has no White Label domain | **Fails with error 7301.** The API requires a configured portal domain to associate the workspace with. Set up the White Label domain in Zoho Analytics settings first. |
| Multiple workspaces in the same org | Each workspace must be individually enabled. Enabling one workspace does not affect others. |
| New workspace created in an org with existing portal | The workspace starts **disabled** by default. It must be explicitly enabled before portal users can access it. |

## Disable Workspace for Domain Access

| Scenario | Behaviour |
|----------|-----------|
| Workspace currently enabled | Domain ID is cleared from the workspace configuration. Portal users immediately lose access via the custom domain URL. |
| Workspace not enabled (already disabled) | **Fails with error 12050.** Not idempotent. |
| Impact on portal user memberships | Disabling does not remove users from the workspace or revoke view-level sharing. The workspace and its data remain intact. Portal users who are also standard Zoho Analytics users can still access the workspace at `analyticsapi.zoho.com`. Only portal-domain-only users (users who exist exclusively as portal users) lose meaningful access. |
| Impact on shared views | View-level shares are preserved. If the workspace is later re-enabled, portal users will regain access without any re-sharing required. |
| Re-enabling after disable | Call Enable Workspace for Domain Access again. The previous domain association is restored using the Account Admin's current White Label configuration. |

## Enable ↔ Disable State Machine

```
[Created — Disabled by default]
         |
         | POST /wlaccess (Enable)
         ↓
 [Enabled for Domain Access]  ──── POST /wlaccess ──→  Error 12049
         |
         | DELETE /wlaccess (Disable)
         ↓
    [Disabled]  ─────────────── DELETE /wlaccess ──→  Error 12050
         |
         | POST /wlaccess (Re-enable)
         ↓
 [Enabled for Domain Access]
```

## Comparison with Similar APIs

| Aspect | Enable/Disable WL Access | Add/Remove Default Workspace | Add/Remove Favourite |
|--------|--------------------------|------------------------------|----------------------|
| Idempotent enable | **No** — error 12049 on double-enable | Yes (silently replaces) | Yes (silently no-ops) |
| Idempotent disable | **No** — error 12050 on double-disable | No — error 7415 | Yes (silently no-ops) |
| Caller scope | Account Admin / Org Admin only | Any user with workspace access | Any user with workspace access |
| Effect scope | Affects all portal domain users | Per-user preference only | Per-user preference only |
| Prerequisite | Active White Label domain on the org | None | None |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |
| [12049](../../../foundations/error-codes.md#error-12049) | 400 | The workspace is already enabled for White Label domain access. Calling Enable on an already-enabled workspace is not idempotent. |
| [12050](../../../foundations/error-codes.md#error-12050) | 400 | The workspace is not currently enabled for White Label domain access. Calling Disable on an already-disabled workspace is not idempotent. |

# Related

- [Workspace Management](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
