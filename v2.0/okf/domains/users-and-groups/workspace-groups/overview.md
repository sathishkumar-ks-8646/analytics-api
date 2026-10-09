---
type: API Group
title: Workspace Groups
description: APIs that manage the groups of a Zoho Analytics workspace.
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - workspace-groups
  - api-group
api:
  domain: users-and-groups
  group: workspace-groups
  endpoint_count: 7
  endpoints:
    - operation_id: getGroups
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/groups"
      doc: "/domains/users-and-groups/workspace-groups/get-groups.md"
    - operation_id: createGroup
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/groups"
      doc: "/domains/users-and-groups/workspace-groups/create-group.md"
    - operation_id: renameGroup
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/groups/{group-id}"
      doc: "/domains/users-and-groups/workspace-groups/rename-group.md"
    - operation_id: addGroupMembers
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members"
      doc: "/domains/users-and-groups/workspace-groups/add-group-members.md"
    - operation_id: removeGroupMembers
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members"
      doc: "/domains/users-and-groups/workspace-groups/remove-group-members.md"
    - operation_id: deleteGroup
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/groups/{group-id}"
      doc: "/domains/users-and-groups/workspace-groups/delete-group.md"
    - operation_id: getGroupDetails
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/groups/{group-id}"
      doc: "/domains/users-and-groups/workspace-groups/get-group-details.md"
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

Workspace Groups are named collections of users within a specific workspace. Groups allow you to manage view-level sharing permissions in bulk — instead of granting access to individual users, you can share views with a group and all members receive that access simultaneously. Managing group membership is the only way to batch-update sharing permissions for multiple users at once.

> **Workspace-Level Scope:** Groups are scoped to a single workspace. A group created in one workspace is not accessible in another workspace. Members must already be users of the workspace (or the specified portal domain) to be added to a group.

> **White Label / Client Portal:** When the Account Admin is a Client Portal Admin, groups can be scoped to a specific portal domain using the `domainName` field during creation. Group list and detail responses include `domainName` per group in portal contexts. Members are automatically matched to their portal domain when `domainName` is set on the group.

---

APIs that manage the groups of a Zoho Analytics workspace. A group is a named collection of users within a single workspace.

Groups are the building block for bulk view-level access management. When a view is shared with a group, every current and future member of that group inherits that sharing - which makes group membership the way to batch-update the sharing permissions of several users at once. Adding a member grants them access to every view currently shared with the group, removing a member revokes that access unless they hold it through another path, and deleting a group revokes it for every member simultaneously.

Groups are scoped to a single workspace, and their members must already be users of that workspace. When the Account Admin of the organization is also a Client Portal Admin, a group can be scoped to a specific portal domain using the `domainName` field at creation. That association is fixed for the life of the group, and the member management APIs resolve the domain context from the group rather than taking it as an attribute.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Group List](get-groups.md) | GET | `/restapi/v2/workspaces/{workspace-id}/groups` | `getGroups` | `ZohoAnalytics.share.read` | 200 |
| [Create Group](create-group.md) | POST | `/restapi/v2/workspaces/{workspace-id}/groups` | `createGroup` | `ZohoAnalytics.share.create` | 200 |
| [Rename Group](rename-group.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}` | `renameGroup` | `ZohoAnalytics.share.update` | 204 |
| [Add Group Members](add-group-members.md) | POST | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members` | `addGroupMembers` | `ZohoAnalytics.share.create` | 204 |
| [Remove Group Members](remove-group-members.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members` | `removeGroupMembers` | `ZohoAnalytics.share.delete` | 204 |
| [Delete Group](delete-group.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}` | `deleteGroup` | `ZohoAnalytics.share.delete` | 204 |
| [Get Group Details](get-group-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/groups/{group-id}` | `getGroupDetails` | `ZohoAnalytics.share.read` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# API-Specific Notes and Behaviours

## Groups and View Sharing

Groups are the building block for bulk view-level access management. When a view is shared with a group, every current and future member of that group inherits that sharing. This means:

- **Adding a member to a group** immediately grants them access to all views currently shared with that group.
- **Removing a member from a group** immediately revokes the group-based access for that view — but only if the user has no other path to the view (direct sharing or membership in another group with the same share).
- **Deleting a group** revokes all group-based view access for every member simultaneously.

## Create Group

| Scenario | Behaviour |
|----------|-----------|
| `groupName` is empty or whitespace | Rejected immediately. Group names must be non-empty. |
| Duplicate `groupName` in same workspace | Fails with error **7282**. Group names are unique per workspace — the same name can exist in different workspaces. |
| `emailIds` contains a user not in the workspace | The request may partially succeed or fail depending on the portal domain context. Ensure all listed users are already workspace members. |
| `emailIds` contains a user already added to the group | For creation, all `emailIds` become members of the new group. No duplicate check is performed. |
| `inviteMail=true` with no `mailSubject` or `mailMessage` | The invitation is sent with default system-generated subject and message text. |
| `inviteMail=true` but email delivery fails | The group and its members are still created successfully. Email delivery failures do not roll back the operation. |
| `domainName` provided | The group is scoped to that portal domain. All `emailIds` must be users within that portal domain. Standard Zoho Analytics domain users cannot be added to a portal-domain group. |

## Rename Group

| Scenario | Behaviour |
|----------|-----------|
| `groupDesc` omitted | The description is **reset to an empty string**. It is not preserved from the previous value. Always include the existing description if you only intend to rename. |
| Renaming to the current name | Succeeds (idempotent for the name itself). |
| Renaming to a name used by another group in the same workspace | Fails with error **7282**. |
| Group ID from a different workspace | Fails with error **7338**. |

## Add Group Members

| Scenario | Behaviour |
|----------|-----------|
| Adding a user already in the group | Silently skipped. No error is raised. Only users genuinely new to the group receive an invitation email when `inviteMail=true`. |
| Adding a user not in the workspace | The behaviour depends on the portal context. In standard orgs, only workspace users can be group members. Add the user to the workspace first. |
| No `domainName` field | The domain context is resolved automatically from the group's existing domain association. The group was scoped to a domain at creation, and that scoping is preserved. |
| `inviteMail=true` but email delivery fails | Members are still added. Email failures do not roll back the operation. |

## Remove Group Members

| Scenario | Behaviour |
|----------|-----------|
| Removing a user not in the group | Silently processed. No error is raised. |
| Removing all members from a group | Allowed. The group continues to exist with zero members. It can be repopulated or deleted later. |
| `notifyUser=true` but email delivery fails | Members are still removed. Email failures do not roll back the operation. |
| Impact on shared views | If the user's only path to a shared view was through this group membership, they immediately lose access. If they also have direct sharing or membership in another group sharing the same view, access is retained. |

## Delete Group

| Scenario | Behaviour |
|----------|-----------|
| Group has active members | The group is deleted regardless. All members' group-based view access is revoked immediately. |
| Group is used in active view shares | All view shares that reference this group are also removed. Users who accessed views exclusively via this group will lose that access immediately. Users with direct sharing or other group access on the same views are unaffected. |
| Group ID from a different workspace | Fails with error **7338**. The group must belong to the same workspace specified in the URL. |
| Deletion is permanent | There is no soft-delete or trash mechanism for groups. Once deleted, the group and its sharing configuration cannot be restored. |

## Get Group Details vs. Get Group List

| Aspect | Get Group List | Get Group Details |
|--------|----------------|-------------------|
| URL | `.../groups` | `.../groups/<group-id>` |
| `data.groups` type | **Array** of group objects | **Single** group object |
| `domainName` in response | Only when Account Admin is a Client Portal Admin | When Account Admin is a Client Portal Admin **or** when accessed via a custom portal domain URL |
| Use case | Enumerate all groups; discover `groupId` values | Inspect a known group's current member list |

## White Label / Client Portal Domain Behaviour

| Scenario | Behaviour |
|----------|-----------|
| `domainName` provided in Create Group but does not exist | Fails with error **8060** before the group is created. |
| `domainName` belongs to a different org's Account Admin | Fails with error **8061**. |
| Standard domain user calling Get Group List via a portal URL | Returns only groups belonging to the portal's domain (not all workspace groups). |
| Client Portal Admin calling Get Group List | Returns all groups across all domain contexts. Each group entry includes `domainName`. |
| Client Portal Admin calling Get Group Details | Response includes `domainName` regardless of which domain the group belongs to. |
| Standard domain user calling Get Group Details via a portal URL | Response includes `domainName` showing the group's portal domain. |
| Adding members to a portal-domain group | Members must belong to the group's portal domain. Standard org users cannot be added to a portal-domain group. Do not include `domainName` in Add/Remove Group Members calls — the domain is determined by the group. |
| WL Workspace Admin (portal domain with restricted workspace access) | Cannot call any group APIs. Returns error **7301** — WL Workspace Admins do not have access in disabled-workspace portal contexts. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7282](../../../foundations/error-codes.md#error-7282) | 400 | A group with the same name already exists in this workspace. Group names must be unique per workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7338](../../../foundations/error-codes.md#error-7338) | 400 | The specified <group-id> does not belong to this workspace. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | The specified domainName does not exist. |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | The specified domainName does not belong to the org's Account Admin. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |

# Related

- [Users & Groups](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
