---
type: API Group
title: Workspace Users
description: "APIs that manage the users and the administrators of a single Zoho Analytics workspace - controlling who has access to the workspace, the role they hold within it, and whether that access is currently active."
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - workspace-users
  - api-group
api:
  domain: users-and-groups
  group: workspace-users
  endpoint_count: 8
  endpoints:
    - operation_id: getWorkspaceUsers
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/users"
      doc: "/domains/users-and-groups/workspace-users/get-workspace-users.md"
    - operation_id: addWorkspaceUsers
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/users"
      doc: "/domains/users-and-groups/workspace-users/add-workspace-users.md"
    - operation_id: deleteWorkspaceUsers
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/users"
      doc: "/domains/users-and-groups/workspace-users/delete-workspace-users.md"
    - operation_id: changeWorkspaceUsersStatus
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/users/status"
      doc: "/domains/users-and-groups/workspace-users/change-workspace-users-status.md"
    - operation_id: changeWorkspaceUsersRole
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/users/role"
      doc: "/domains/users-and-groups/workspace-users/change-workspace-users-role.md"
    - operation_id: getWorkspaceAdmins
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/admins"
      doc: "/domains/users-and-groups/workspace-users/get-workspace-admins.md"
    - operation_id: addWorkspaceAdmins
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/admins"
      doc: "/domains/users-and-groups/workspace-users/add-workspace-admins.md"
    - operation_id: removeWorkspaceAdmins
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/admins"
      doc: "/domains/users-and-groups/workspace-users/remove-workspace-admins.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/user-groups-grouped-api.json"
    title: OpenAPI 3 specification - user-groups-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

These APIs manage users and administrators at the **workspace level** — controlling who has access to a specific workspace, their role within it, and their active/inactive status. They complement the org-level user management APIs and operate on a single workspace at a time.

> **Workspace-Level vs Org-Level:** Org-level user management controls membership in the organisation (who is a member at all). Workspace-level management controls which of those members can access a specific workspace and in what capacity.

> **White Label / Client Portal:** When the org's Account Admin is also a Client Portal Admin, workspace user operations can be scoped to a specific portal domain using the `domainName` field. Users belonging to a portal domain are listed and managed separately from standard Zoho Analytics users.

---

APIs that manage the users and the administrators of a single Zoho Analytics workspace - controlling who has access to the workspace, the role they hold within it, and whether that access is currently active.

These APIs complement the org-level user management APIs. Org-level management controls who is a member of the organization at all, while workspace-level management controls which of those members can access a specific workspace and in what capacity.

When the Account Admin of the organization is also a Client Portal Admin, the operations in this group can be scoped to a specific portal domain using the `domainName` field in CONFIG. Users belonging to a portal domain are listed and managed separately from the standard Zoho Analytics users.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Workspace Users](get-workspace-users.md) | GET | `/restapi/v2/workspaces/{workspace-id}/users` | `getWorkspaceUsers` | `ZohoAnalytics.usermanagement.read` | 200 |
| [Add Workspace Users](add-workspace-users.md) | POST | `/restapi/v2/workspaces/{workspace-id}/users` | `addWorkspaceUsers` | `ZohoAnalytics.usermanagement.create` | 204 |
| [Remove Workspace Users](delete-workspace-users.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/users` | `deleteWorkspaceUsers` | `ZohoAnalytics.usermanagement.delete` | 204 |
| [Change Workspace Users Status](change-workspace-users-status.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/users/status` | `changeWorkspaceUsersStatus` | `ZohoAnalytics.usermanagement.update` | 204 |
| [Change Workspace Users Role](change-workspace-users-role.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/users/role` | `changeWorkspaceUsersRole` | `ZohoAnalytics.usermanagement.update` | 204 |
| [Get Workspace Admins](get-workspace-admins.md) | GET | `/restapi/v2/workspaces/{workspace-id}/admins` | `getWorkspaceAdmins` | `ZohoAnalytics.share.read` | 200 |
| [Add Workspace Admins](add-workspace-admins.md) | POST | `/restapi/v2/workspaces/{workspace-id}/admins` | `addWorkspaceAdmins` | `ZohoAnalytics.share.create` | 204 |
| [Remove Workspace Admins](remove-workspace-admins.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/admins` | `removeWorkspaceAdmins` | `ZohoAnalytics.share.delete` | 204 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# API-Specific Notes and Behaviours

## Permission Summary

| API | Minimum Required Role |
|-----|-----------------------|
| Get Workspace Users | Workspace Admin |
| Add Workspace Users | Workspace Admin |
| Remove Workspace Users | Workspace Admin |
| Change Workspace Users Status | **Account Admin only** |
| Change Workspace Users Role | Account Admin or Organization Admin |
| Get Workspace Admins | Account Admin or Organization Admin |
| Add Workspace Admins | Account Admin or Organization Admin |
| Remove Workspace Admins | Account Admin or Organization Admin |

> **Key asymmetry:** [Add Workspace Users](add-workspace-users.md) and [Remove Workspace Users](delete-workspace-users.md) can be done by Workspace Admins, but [Change Workspace Users Status](change-workspace-users-status.md) and [Change Workspace Users Role](change-workspace-users-role.md) require Account Admin or higher. This prevents Workspace Admins from promoting themselves or blocking other users.

## Workspace Role Values

| `role` Value | Display Name | Description |
|-------------|--------------|-------------|
| `"WORKSPACEADMIN"` | Workspace Admin | Full access to the workspace — can add/remove users, create and delete views, manage shares. |
| `"USER"` | User | Can access views shared with them. Cannot manage workspace settings or users unless specifically shared with Design Modify permission. |
| Custom role name | (as defined) | A role name exactly matching a custom role defined in the org. Must exist — invalid names fail with error **7550**. |

> **Note:** `"VIEWER"` is an org-level role, not a workspace-level role value. At workspace level, Viewers appear as `"User"` in the response. The distinction is enforced at the org level.

## Get Workspace Users

| Scenario | Behaviour |
|----------|-----------|
| Custom role users | Appear in the list with `role` set to the exact custom role name as defined in the org (not a numeric ID). |
| Deactivated users | Appear in the list with `status: false`. They are not removed. |
| `domainName` in response | Only present when the Account Admin is a Client Portal Admin. Standard org users show the default analytics domain; portal users show their portal's domain. |
| Org Admin viewing another admin's workspace | Allowed — Org Admins have visibility into all workspaces in their org. |

## Add Workspace Users

| Scenario | Behaviour |
|----------|-----------|
| `role` omitted | Defaults to `"USER"`. |
| User already has access to the workspace | They are added again with the specified role. If the user already exists with a different role, the role is updated. |
| Bulk mode (`users` array) with 21 or more groups | Rejected at validation — max 20 groups per request. Split into multiple calls. |
| Custom role name not found in the org | Fails with error **7550**. The role name must exactly match an existing custom role. |
| Portal user added without `domainName` | Added to the standard domain context. If the user is a portal-only user without a standard Zoho account, the addition may fail. Always specify `domainName` for portal users. |

## Remove Workspace Users

| Scenario | Behaviour |
|----------|-----------|
| Removing a user who is not in the workspace | The behaviour depends on the portal context. In the standard domain, the user is simply not found and the call may succeed silently or fail depending on the underlying operation. Verify membership using Get Workspace Users first. |
| Removing a Workspace Admin via this API | Allowed. The user is removed from the workspace entirely (loses all access, including admin). To demote without removing, use [Remove Workspace Admins](remove-workspace-admins.md) instead. |
| Portal user removed without `domainName` | Looked up in the standard domain. If the user was added only via a portal domain, they will not be found in the standard context. Always specify `domainName` when managing portal users. |

## Change Workspace Users Status

| Scenario | Behaviour |
|----------|-----------|
| Workspace Admin calls this API | Fails with error **7301** — "Only Account Admin has the permission." |
| `operation` value other than `"activate"` or `"deactivate"` | Fails with error **8119** before any changes are made. The field is case-sensitive — `"Activate"` or `"ACTIVATE"` are invalid. |
| Activating an already-active user | Succeeds silently (idempotent). |
| Deactivating an already-inactive user | Succeeds silently (idempotent). |
| User's workspace-level data after deactivation | All shares, roles, and permissions are preserved. Restored exactly upon reactivation. |

## Change Workspace Users Role

| Scenario | Behaviour |
|----------|-----------|
| Workspace Admin calls this API | Fails with error **7301** — this API requires Account Admin or Organization Admin. |
| Bulk mode `users` array exceeding 20 entries | Rejected at validation. Split into multiple calls. |
| Same role already assigned | Succeeds silently (idempotent). |
| Demoting a Workspace Admin to User | Allowed. The user loses admin capabilities immediately. Their workspace access continues as a User. |
| Portal user role change without `domainName` | Attempted in the standard domain context. If the user is only in a portal domain, they will not be found. Always specify `domainName` for portal users. |

## Add Workspace Admins

| Scenario | Behaviour |
|----------|-----------|
| User already a Workspace Admin | Silently skipped without error. Only users who are not yet admins are processed. |
| Viewer-role user in `emailIds` | Fails with error **7390** before any changes. All emails in the batch are rejected. To promote a Viewer, first change their org-level role to `"USER"` via the Change User Role API, then add them as Workspace Admin. |
| `inviteMail=true` but email delivery fails | The admin promotion is still committed. Email failures are logged but do not roll back the transaction. |
| Portal admin added without `domainName` | Processed in the standard domain. If the user is a portal-only user, use `domainName` to scope the operation to their portal. |

## Remove Workspace Admins

| Scenario | Behaviour |
|----------|-----------|
| Non-admin email in `emailIds` | Fails with error **8040** for that email. The entire batch is rejected — no demotions are applied. Use Get Workspace Admins to verify current admin membership before calling. |
| Removing the last Workspace Admin | Allowed. The workspace will have no Workspace Admins. Only Account Admin and Org Admin can then manage the workspace. |
| `notifyMail=true` but email delivery fails | The admin removal is still committed. Email failures are logged but do not roll back the transaction. |
| Difference from Remove Workspace Users | Remove Workspace Admins only **demotes** (revokes the admin role) — the user retains workspace access as a regular User. [Remove Workspace Users](delete-workspace-users.md) **completely removes** the user from the workspace. |

## White Label / Client Portal Domain Behaviour

| Scenario | Behaviour |
|----------|-----------|
| `domainName` omitted | All operations apply to the standard Zoho Analytics domain. |
| `domainName` provided but does not exist | Fails with error **8060** before any changes. |
| `domainName` provided but not owned by the org's Account Admin | Fails with error **8061**. |
| Get Workspace Users — Client Portal Admin | Every user entry includes `domainName`. Standard users show the default analytics domain URL; portal users show their portal's custom domain URL. |
| Get Workspace Admins — Client Portal Admin | Response contains two groups in `workspaceAdmins`: one for the standard domain and one for the portal domain, each with `domainName`. |
| Bulk Add/Change Role with mixed portal domains | Use the `users` array in bulk mode, setting `domainName` per group. Each group is processed in its own portal context. |
| Portal user operations without specifying `domainName` | Operations are attempted in the standard domain. Portal-only users do not exist in the standard domain and will not be found. Always specify `domainName` when the user was added via a portal. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7390](../../../foundations/error-codes.md#error-7390) | 400 | WORKSPACENOTBELONGSTOORG — The workspace does not belong to the organization in ZANALYTICS-ORGID. |
| [7550](../../../foundations/error-codes.md#error-7550) | 400 | The specified role name does not exist as a custom role in the org. |
| [8040](../../../foundations/error-codes.md#error-8040) | 400 | One or more specified email addresses are not currently Workspace Admins in this workspace. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | The specified domainName does not exist. |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | The specified domainName does not belong to the org's Account Admin. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | INVALIDVALUEFORATTRIBUTE — fileType, onError, delimiter, quoted, thousandSeparator, or decimalSeparator is outside its permitted set. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |

# Related

- [Users & Groups](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
