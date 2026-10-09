---
type: API Group
title: Workspace Preferences
description: "APIs that manage the workspace preferences of a user, covering the default workspace that opens on login and the favourite workspaces starred for quick access."
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-preferences
  - api-group
api:
  domain: workspace-management
  group: workspace-preferences
  endpoint_count: 4
  endpoints:
    - operation_id: addDefaultWorkspace
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/default"
      doc: "/domains/workspace-management/workspace-preferences/add-default-workspace.md"
    - operation_id: removeDefaultWorkspace
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/default"
      doc: "/domains/workspace-management/workspace-preferences/remove-default-workspace.md"
    - operation_id: addFavoriteWorkspace
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/favorite"
      doc: "/domains/workspace-management/workspace-preferences/add-favorite-workspace.md"
    - operation_id: removeFavoriteWorkspace
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/favorite"
      doc: "/domains/workspace-management/workspace-preferences/remove-favorite-workspace.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

These APIs manage per-user workspace preferences — marking a workspace as the **default** (the workspace that opens on login) and managing **favourites** (starred workspaces for quick access).

> **Per-user scope:** Both default and favourite preferences are stored individually per user. Marking a workspace as default or favourite for one user has no effect on any other user's preferences.

> **Default vs Favourite:**
> - **Default workspace** — each user can have at most **one** default workspace at a time. Setting a new default automatically replaces the previous one. The default workspace is indicated by `isDefault: true` in workspace listing responses.
> - **Favourite workspaces** — a user can mark **multiple** workspaces as favourite simultaneously. Favouriting is an additive preference with no exclusivity constraint.

---

APIs that manage the workspace preferences of a user, covering the default workspace that opens on login and the favourite workspaces starred for quick access. Both the preferences are stored per user and per organization, and have no effect on the preferences of any other user.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Add Default Workspace](add-default-workspace.md) | POST | `/restapi/v2/workspaces/{workspace-id}/default` | `addDefaultWorkspace` | `ZohoAnalytics.metadata.update` | 204 |
| [Remove Default Workspace](remove-default-workspace.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/default` | `removeDefaultWorkspace` | `ZohoAnalytics.metadata.update` | 204 |
| [Add Favourite Workspace](add-favorite-workspace.md) | POST | `/restapi/v2/workspaces/{workspace-id}/favorite` | `addFavoriteWorkspace` | `ZohoAnalytics.metadata.update` | 204 |
| [Remove Favourite Workspace](remove-favorite-workspace.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/favorite` | `removeFavoriteWorkspace` | `ZohoAnalytics.metadata.update` | 204 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# API-Specific Notes and Behaviours

## Default vs Favourite — Behavioural Comparison

| Aspect | Default Workspace | Favourite Workspace |
|--------|-------------------|---------------------|
| How many per user | **Exactly one** (or none) | **Multiple** — no limit |
| Adding when already set/added | Replaces existing default silently | Silently no-ops (idempotent) |
| Removing when not set/added | **Fails with error 7415** | Silently no-ops (idempotent) |
| Visibility in workspace lists | `isDefault: true` in Get All / Owned / Shared response | Not exposed as a distinct field in standard list responses |
| Purpose | Opens on login | Quick navigation / starred workspaces |
| User scope | Per user, per org | Per user, per org |

## Add Default Workspace

| Scenario | Behaviour |
|----------|-----------|
| User has no existing default | The specified workspace is set as the user's default. |
| User already has a different workspace as default | The previous default is silently replaced. No error is raised for the switch. |
| Calling with the same workspace already set as default | Succeeds silently — idempotent. |
| User loses workspace access after setting default | The default preference is still stored. However, the workspace will not be presented as accessible until access is restored. |

## Remove Default Workspace

| Scenario | Behaviour |
|----------|-----------|
| Workspace is currently the user's default | Default is removed. The user has no default workspace until they set a new one. |
| Workspace is **not** the user's current default | **Fails with error 7415.** This is the primary failure case — use Get All Workspace List to confirm `isDefault: true` before calling this API. |
| Workspace ID is valid but user has no access | Fails with error 7301. |
| Calling immediately after Add Default | Succeeds — the workspace was just set and can be unset in sequence. |

## Add Favourite Workspace

| Scenario | Behaviour |
|----------|-----------|
| Workspace not yet in favourites | Added to the user's favourites list. |
| Workspace already in favourites | Succeeds silently — idempotent. No duplicate entry is created. |
| User can mark any workspace they have access to | Access is checked at the workspace level (any shared view). There is no additional permission required beyond basic read access. |

## Remove Favourite Workspace

| Scenario | Behaviour |
|----------|-----------|
| Workspace is in the user's favourites | Removed from the favourites list. |
| Workspace is **not** in the user's favourites | Succeeds silently — idempotent. Unlike Remove Default, this does not error. |

## White Label / Client Portal Behaviour

| Scenario | Behaviour |
|----------|-----------|
| Portal user adding a default/favourite workspace | Preferences are stored scoped to the portal user's organisation namespace. Portal users and standard Zoho Analytics users maintain separate preference stores even if they access the same workspace. |
| Portal user accessing via custom domain URL | The workspace must be accessible via that portal domain (shared with the portal user). If the workspace is not accessible in the portal domain context, the access check fails with 7301. |
| Account Admin (Client Portal Admin) managing preferences | Uses the standard Zoho Analytics namespace. The admin's preferences are independent of portal user preferences. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7415](../../../foundations/error-codes.md#error-7415) | 400 | The specified workspace is not the current default workspace of the requesting user. This API does not succeed silently for a workspace that is not the default. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |

# Related

- [Workspace Management](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
