---
type: API Group
title: Organization Users
description: "APIs that allow the Account Admin and the Organization Admins of a Zoho Analytics organization to manage its users - listing, adding, removing, activating, deactivating and changing the org-level role of the users, and listing the users who hold the Organization Admin role."
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - org-users
  - api-group
api:
  domain: users-and-groups
  group: org-users
  endpoint_count: 7
  endpoints:
    - operation_id: getUsers
      method: GET
      path: "/restapi/v2/users"
      doc: "/domains/users-and-groups/org-users/get-users.md"
    - operation_id: addUsers
      method: POST
      path: "/restapi/v2/users"
      doc: "/domains/users-and-groups/org-users/add-users.md"
    - operation_id: removeUsers
      method: DELETE
      path: "/restapi/v2/users"
      doc: "/domains/users-and-groups/org-users/remove-users.md"
    - operation_id: activateUsers
      method: PUT
      path: "/restapi/v2/users/active"
      doc: "/domains/users-and-groups/org-users/activate-users.md"
    - operation_id: deActivateUsers
      method: PUT
      path: "/restapi/v2/users/inactive"
      doc: "/domains/users-and-groups/org-users/de-activate-users.md"
    - operation_id: changeUserRole
      method: PUT
      path: "/restapi/v2/users/role"
      doc: "/domains/users-and-groups/org-users/change-user-role.md"
    - operation_id: getOrgAdmins
      method: GET
      path: "/restapi/v2/orgadmins"
      doc: "/domains/users-and-groups/org-users/get-org-admins.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/user-groups-grouped-api.json"
    title: OpenAPI 3 specification - user-groups-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

These APIs allow Account Admins and Organization Admins to manage the users who belong to a Zoho Analytics organisation — including listing, adding, removing, activating, deactivating, and changing the org-level role of users. A separate API returns the list of users holding the Organization Admin role.

> **Note:** All user management APIs operate at the **organisation level** — they govern a user's membership and role within the org, not their access to individual workspaces. Workspace-level sharing is handled separately by workspace share APIs.

> **White Label / Client Portal Note:** Zoho Analytics supports Client Portal (White Label) deployments where an org may have one or more custom-branded portal domains. When the Account Admin of an org is also a Client Portal Admin, user management operations can be scoped to a specific portal domain using the `domainName` field in CONFIG. Users belonging to a portal domain are managed independently of the main org domain. The `domainName` must be a valid portal domain owned by the Account Admin of the org.

---

APIs that allow the Account Admin and the Organization Admins of a Zoho Analytics organization to manage its users - listing, adding, removing, activating, deactivating and changing the org-level role of the users, and listing the users who hold the Organization Admin role.

These APIs operate at the organization level. They govern the membership and role of a user within the organization, and not their access to individual workspaces, which is handled by the workspace sharing APIs.

Zoho Analytics also supports Client Portal (White Label) deployments, where an organization can have one or more custom-branded portal domains. When the Account Admin of the organization is also a Client Portal Admin, the write APIs in this group can be scoped to a specific portal domain using the `domainName` field in CONFIG. Users belonging to a portal domain are managed independently of the main organization domain, and `domainName` must be a valid portal domain owned by the Account Admin of the organization.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Users](get-users.md) | GET | `/restapi/v2/users` | `getUsers` | `ZohoAnalytics.usermanagement.read` | 200 |
| [Add Users](add-users.md) | POST | `/restapi/v2/users` | `addUsers` | `ZohoAnalytics.usermanagement.create` | 204 |
| [Remove Users](remove-users.md) | DELETE | `/restapi/v2/users` | `removeUsers` | `ZohoAnalytics.usermanagement.delete` | 204 |
| [Activate Users](activate-users.md) | PUT | `/restapi/v2/users/active` | `activateUsers` | `ZohoAnalytics.usermanagement.update` | 204 |
| [Deactivate Users](de-activate-users.md) | PUT | `/restapi/v2/users/inactive` | `deActivateUsers` | `ZohoAnalytics.usermanagement.update` | 204 |
| [Change User Role](change-user-role.md) | PUT | `/restapi/v2/users/role` | `changeUserRole` | `ZohoAnalytics.usermanagement.update` | 204 |
| [Get Org Admins](get-org-admins.md) | GET | `/restapi/v2/orgadmins` | `getOrgAdmins` | `ZohoAnalytics.share.read` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# Operational Notes and Failure Cases

## Org-Level vs Workspace-Level Role

| Concept | Description |
|---------|-------------|
| **Org-level role** (`role` in Get/Add/Change User APIs) | Determines what the user can do across the entire organisation — create workspaces, manage users, etc. Values: `Account Admin`, `Organization Admin`, `User`, `Viewer`. |
| **Workspace-level role** | Determines what the user can do within a specific workspace — read, design, share, etc. Managed via workspace share APIs, not these user management APIs. |
| **Relationship** | A user's org-level role is a ceiling on their capabilities, but workspace-level permissions can be more granular. A `User` at org level can be a `Workspace Admin` for a specific workspace they own. A `Viewer` at org level can only ever have read access regardless of workspace-level share. |

## Get Users

| Scenario | Behaviour |
|----------|-----------|
| Org has only one user (the Account Admin) | Returns a single entry with `role: "Account Admin"`. |
| User is deactivated | Appears in the list with `status: false`. Deactivated users are included in the result — they are not removed from the list. |
| Organization Admin calls Get Users | Allowed — Org Admins can view the full user list. |

## Add Users

| Scenario | Behaviour |
|----------|-----------|
| Adding a user who already exists in the org | Fails with error **6071** for that email. The entire batch fails — no users from the request are added. |
| `role` omitted | Defaults to `"USER"`. The invited user joins as a standard user. |
| Org Admin adds a user with `role="ORGADMIN"` | Fails — Organization Admins cannot grant the Org Admin role. Only Account Admins can assign `"ORGADMIN"`. |
| Adding more users than the plan's seat limit | Fails with error **6004** before any users are added. The entire batch is rejected. Check current usage with Get Resource Details. |
| Adding a user on a Free plan | Free plans do not support extra users beyond the included allocation. Fails with error **6026**. |
| `domainName` + `role="ORGADMIN"` combination | Always fails with error **6089** regardless of the caller's role. Org Admin role is not assignable via custom domain context. |
| Invited user has not yet accepted | The invitation is pending. The user is not listed in Get Users until they accept and join. |

## Remove Users

| Scenario | Behaviour |
|----------|-----------|
| Attempting to remove the Account Admin | The Account Admin (org owner) cannot be removed by this API. The request will fail. Transfer ownership first if removal is needed. |
| Removing a user who is not in the org | Fails with error **8114** for the entire batch. Use Get Users to validate membership before calling this API. |
| Removing a user who owns workspaces | The user's workspaces are not automatically deleted. The workspaces remain but ownership may need to be transferred separately. Workspace contents remain intact after user removal. |
| Partial batch with mix of valid and invalid emails | The request fails as a whole on the first non-member email. No users are removed if any email in the batch is invalid. |

## Activate Users

| Scenario | Behaviour |
|----------|-----------|
| Activating an already-active user | The request succeeds silently (idempotent). No error is raised for already-active users. |
| User seat limit reached at reactivation time | Fails with error **6004**. A user who was previously deactivated still occupies a seat in terms of plan limits when reactivated. Remove unused users or upgrade the plan first. |
| Activating a user not in the org | Fails with error **8114**. The user must be a member of the org (even if currently deactivated) to be reactivated. |

## Deactivate Users

| Scenario | Behaviour |
|----------|-----------|
| Deactivating an already-inactive user | The request succeeds silently (idempotent). No error is raised for already-deactivated users. |
| Deactivated user's workspace shares | All workspace shares are preserved but the user cannot access them while deactivated. Upon reactivation, all prior shares are restored. |
| Attempting to deactivate the Account Admin | Not permitted. The org owner (Account Admin) cannot be deactivated through this API. |
| Deactivate vs Remove | Deactivate is reversible — user data, shares, and role are preserved. Remove is permanent — shares are revoked and the user must be re-invited. Use Deactivate for temporary suspension. |

## Change User Role

| Scenario | Behaviour |
|----------|-----------|
| Promoting a `"USER"` to `"ORGADMIN"` by an Org Admin | Not allowed — Org Admins cannot grant the Org Admin role. Fails with a permission error (7301). Only Account Admins can do this. |
| Demoting an `"ORGADMIN"` back to `"USER"` | Allowed by Account Admin. The former Org Admin immediately loses org-wide management capabilities. Their workspace-level permissions (if any) are unaffected. |
| Changing role of a deactivated user | Allowed. The role change takes effect. When the user is reactivated, they will have the new role. |
| Changing role of a user not in the org | Fails with error **8114**. Verify membership with Get Users first. |
| Setting `role="VIEWER"` for a user who owns workspaces | The user becomes read-only at the org level. However, workspaces they own are not automatically transferred. They may still have Workspace Admin access on those specific workspaces. |
| Applying the same role the user already has | The request succeeds silently (idempotent). No error is raised. |

## Get Org Admins

| Scenario | Behaviour |
|----------|-----------|
| No Organization Admins have been assigned | Returns HTTP 200 with an empty `orgAdmins` array. All admin operations are handled by the Account Admin only. |
| Org Admin calls Get Org Admins | Fails with error **7301** — this endpoint is restricted to the Account Admin only. Unlike the other user management APIs that allow Org Admins, this one requires the Account Admin. |
| Relationship to Add/Change User Role APIs | Org Admins are users whose `role` in the Change User Role API was set to `"ORGADMIN"`. This API is a convenience endpoint that filters for only that role — equivalent to filtering Get Users results where `role = "Organization Admin"`. |

## White Label / Client Portal Domain Behaviour

| Scenario | Behaviour |
|----------|-----------|
| `domainName` omitted in all write APIs | Operation applies to the standard Zoho Analytics domain (default org context). Users are managed as regular org members. |
| `domainName` provided but the domain does not exist | All write APIs (Add, Remove, Activate, Deactivate, Change Role) fail with error **8060** before any change is made. |
| `domainName` provided but belongs to a different Account Admin | Fails with error **8061**. Only domains owned by the Account Admin of the specified org are valid. An Org Admin providing a `domainName` that they do not administer also triggers 8061. |
| Caller is not a Client Portal Admin and provides `domainName` | Fails with error **8061**. The `domainName` parameter is only meaningful when the Account Admin of the org has Client Portal Admin status. |
| `role="ORGADMIN"` + `domainName` in Add Users or Change User Role | Always fails with error **6089**. Organization Admin is an org-level concept and cannot be assigned to a portal-scoped user. Use `role="USER"` or `role="VIEWER"` for portal domain operations. |
| Get Users when Account Admin is a Client Portal Admin | Every user entry in the response includes a `domainName` field. Users added via the standard Zoho Analytics org show the default analytics domain URL. Users added via a specific client portal show that portal's custom domain URL. This allows the admin to distinguish portal membership at a glance. |
| Get Users when Account Admin is NOT a Client Portal Admin | The `domainName` field is absent from all user entries in the response. Only `emailId`, `status`, and `role` are returned. |
| A user added via a portal domain — can they access the main org? | No. Portal-domain users are scoped to their portal. They access analytics only through the portal's branded URL. They do not appear as standard org members on `analytics.zoho.com`. |
| Remove a portal user without specifying `domainName` | The user is looked up in the default (standard) org context. If they were added via a portal domain only and do not exist in the standard org, the request fails with error **8114**. Always specify `domainName` when managing portal-scoped users. |
| Multiple client portals under the same org | Each portal domain is managed independently. Specify the target `domainName` in each API call. A user can be a member of multiple portals simultaneously — their membership in one portal is unaffected by operations on another. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [6004](../../../foundations/error-codes.md#error-6004) | 400 | Adding these users would exceed the organisation's user seat limit under the current plan. |
| [6026](../../../foundations/error-codes.md#error-6026) | 400 | The current plan does not support adding extra users (free plan restriction). |
| [6071](../../../foundations/error-codes.md#error-6071) | 400 | One or more of the specified email addresses is already a member of this organisation. |
| [6089](../../../foundations/error-codes.md#error-6089) | 400 | Attempted to assign "ORGADMIN" role via a custom domain (domainName). Organization Admin role cannot be assigned through a custom portal domain. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | The specified domainName does not exist. |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | The specified domainName does not belong to the org's Account Admin. |
| [8114](../../../foundations/error-codes.md#error-8114) | 400 | One or more specified email addresses are not members of this organisation. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |

# Related

- [Users & Groups](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
