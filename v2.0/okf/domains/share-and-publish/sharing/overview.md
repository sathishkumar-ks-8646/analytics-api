---
type: API Group
title: Sharing
description: "APIs for sharing workspaces and views with users, and retrieving share details and permissions."
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - sharing
  - api-group
api:
  domain: share-and-publish
  group: sharing
  endpoint_count: 6
  endpoints:
    - operation_id: getWorkspaceSharedDetails
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/share"
      doc: "/domains/share-and-publish/sharing/get-workspace-shared-details.md"
    - operation_id: shareViews
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/share"
      doc: "/domains/share-and-publish/sharing/share-views.md"
    - operation_id: UpdateSharedDetailsForView
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share"
      doc: "/domains/share-and-publish/sharing/update-shared-details-for-view.md"
    - operation_id: getSharedDetailsForViews
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/share/shareddetails"
      doc: "/domains/share-and-publish/sharing/get-shared-details-for-views.md"
    - operation_id: removeShare
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/share"
      doc: "/domains/share-and-publish/sharing/remove-share.md"
    - operation_id: getUserPermissions
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share/userpermissions"
      doc: "/domains/share-and-publish/sharing/get-user-permissions.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/share-publish-grouped-api.json"
    title: OpenAPI 3 specification - share-publish-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

This document covers the APIs for sharing views/reports with individual users or groups, updating and inspecting existing share configurations, removing shares, and checking a user's own effective permissions on a view.

APIs for sharing workspaces and views with users, and retrieving share details and permissions.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Workspace Shared Details](get-workspace-shared-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/share` | `getWorkspaceSharedDetails` | `ZohoAnalytics.share.read` | 200 |
| [Share Views](share-views.md) | POST | `/restapi/v2/workspaces/{workspace-id}/share` | `shareViews` | `ZohoAnalytics.share.create` | 204 |
| [Update Shared Details](update-shared-details-for-view.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share` | `UpdateSharedDetailsForView` | `ZohoAnalytics.share.update` | 204 |
| [Get Shared Details](get-shared-details-for-views.md) | GET | `/restapi/v2/workspaces/{workspace-id}/share/shareddetails` | `getSharedDetailsForViews` | `ZohoAnalytics.share.read` | 200 |
| [Remove Shared Views](remove-share.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/share` | `removeShare` | `ZohoAnalytics.share.delete` | 204 |
| [Get My Permissions](get-user-permissions.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share/userpermissions` | `getUserPermissions` | `ZohoAnalytics.share.read` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is "Sharing" in Zoho Analytics?

A view (table, report, dashboard, etc.) can be made accessible to other users of the same organization (or, for Client Portal/White Label workspaces, users of a portal domain) without transferring ownership. Sharing is done either:

- **Directly to individual users** — by email address (`emailIds`), or
- **To a group** — a named collection of users (`groupIds`), managed via the [Workspace Groups APIs](../../users-and-groups/workspace-groups/overview.md).

Each share grants a specific **permission set** (read, export, row-level write actions, drill-down, discussion, etc. — see [`permissions` Fields](share-views.md#permissions-fields)), and can optionally restrict the shared user to specific **columns** and/or a row-level **filter criteria**.

---

# API-Specific Notes and Behaviours

## Get Workspace Shared Details

- **Owner-only, workspace-wide snapshot.** This is the only sharing API that requires no `viewIds` at all — it enumerates every share (user, group, public, private-link) across the entire workspace in a single call, restricted to the Workspace Admin/owner.
- **Read-only sibling of Get Shared Details.** Use this API for a workspace-wide audit; use [Get Shared Details](get-shared-details-for-views.md) when you need the fuller per-share fields (`permissionString`, `criteria`, `sharedColumns`, etc.) for a specific set of views.
- **Dependency chain:** Get Workspace List → Get Workspace Shared Details.

## Share Views

- **`read` is non-negotiable.** Every successful share grants at least read access — there is no supported "write-only" share configuration (error 8074 enforces this).
- **Single-view-only restrictions.** `columns`, `vudColumns`, `drillColumns`, and `criteria` are only usable when `viewIds` contains exactly one view — plan multi-view shares to use only the common, unrestricted permission set.
- **Re-sharing fails, does not upsert.** Calling this API again for a view/user (or view/group) pair that is already shared returns an error (7321/7322) instead of updating the share — always route modifications through [Update Shared Details](update-shared-details-for-view.md).
- **Dependency chain:** [Get Views](../../views-management/view-operations/overview.md) + [Get Group List](../../users-and-groups/workspace-groups/get-groups.md) → Share Views → `<view-id>` share created.

## Update Shared Details

- **Modify-only, not upsert.** This API requires the share to already exist (errors 8032/8150 otherwise) — it is the counterpart to Share Views for existing shares, not a replacement for it.
- **No invite email support.** Unlike Share Views, there are no `inviteMail`/`mailSubject`/`mailMessage` fields — updating a share never re-sends an invitation.
- **Dependency chain:** [Get Shared Details](get-shared-details-for-views.md) (fetch current state) → Update Shared Details (apply changes).

## Get Shared Details

- **The richest read API in this family.** Returns `permissionString` (ready for display), `criteria`, `isInvalidCriteria`, and column restrictions in addition to the raw `permissions` booleans — prefer this over Get Workspace Shared Details when you already know which `viewIds` you need details for.
- **Batchable.** Accepts multiple `viewIds` in one call, returning one `sharedDetails` entry per view — avoid looping per-view calls when auditing several views at once.
- **Dependency chain:** [Get Views](../../views-management/view-operations/overview.md) → `viewIds` → Get Shared Details.

## Remove Shared Views

- **Two mutually exclusive modes.** Targeted removal (`viewIds`) is available to any user with Share permission on those views; bulk removal (`removeAllViews: true`) is restricted to the Workspace Admin/owner — mixing the two in one request is rejected (error 8105).
- **Idempotency caveat.** Removing a share that does not exist is an error (8032/8150) for targeted removal, but is silently skipped (no error) for bulk (`removeAllViews: true`) removal of users/groups with no shares.
- **Dependency chain:** [Get Shared Details](get-shared-details-for-views.md) → confirm target share(s) → Remove Shared Views.

## Get My Permissions

- **Self-only, dual path.** Always reflects the caller's own access; `/share/mypermissions` is a deprecated alias retained for backward compatibility alongside the current `/share/userpermissions` path.
- **No admin override parameter.** There is intentionally no way to query another user's permissions through this endpoint — Workspace Admins must use [Get Shared Details](get-shared-details-for-views.md) instead.
- **Dependency chain:** [Get Views](../../views-management/view-operations/overview.md) → `viewId` → Get My Permissions.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Mutating APIs return 204 with no body** | Share Views, Update Shared Details, and Remove Shared Views all return HTTP **204 No Content** on success — treat the 2xx status code as the success indicator, never expect or parse a JSON body for these three APIs. |
| **`permissions` field set differs slightly by endpoint** | Get Workspace Shared Details' nested `views[].permissions` omits `vudSelectedColumns`, `drillThrough`, `drillActions`, `accessAdminPresets`, and `createPreset` (only present in Get Shared Details and Get My Permissions responses). Always code defensively for optional/absent permission keys rather than assuming a fixed schema across all six APIs. |
| **IDs are transmitted as strings** | `viewId`, `groupId`, `sharedToZuId`, `sharedToGroupId`, and all other ID-like fields are JSON strings in every response, even though they are numeric — always parse them as long/string, not as native JSON numbers, to avoid precision loss on large IDs. |
| **`criteria` / `inheritParentFilterCriteria` are always strings in Get Shared Details** | Even though `inheritParentFilterCriteria` is conceptually boolean, Get Shared Details serializes it as the string `"true"`/`"false"` rather than a native boolean — this differs from the CONFIG request format, where it is sent as a native boolean. |
| **Empty containers, not omitted fields** | `userShareInfo`, `groupShareInfo`, `sharedColumns`, `vudColumns`, `drillColumns`, etc. are always present in successful responses but empty (`[]`/`{}`) when there is nothing to report — do not treat their absence as an error condition (they are never absent). |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7307](../../../foundations/error-codes.md#error-7307) | 400 | OWNERCANNOTSHAREHIMSELF — The sharer attempted to share a view to themselves. |
| [7320](../../../foundations/error-codes.md#error-7320) | 400 | CANNOTSHARETOSELF — Same as above (alternate path). |
| [7321](../../../foundations/error-codes.md#error-7321) | 400 | VIEWALREADYSHARED — The view is already shared with this user. |
| [7322](../../../foundations/error-codes.md#error-7322) | 400 | VIEWALREADYSHARED (group form) — The view is already shared with this group. |
| [7323](../../../foundations/error-codes.md#error-7323) | 400 | CANNOTSHAREDTOOBJOWNER — Attempted to share the view with its own owner. |
| [7533](../../../foundations/error-codes.md#error-7533) | 400 | CANNOTSHAREOBJECTTOGROUP — The view's type does not support group sharing. |
| [7535](../../../foundations/error-codes.md#error-7535) | 400 | CANNOTSHARETOMEMBERSNOTPARTOFORG — One or more emailIds do not belong to the organization. |
| [7541](../../../foundations/error-codes.md#error-7541) | 400 | FILTERCRITERIANOTSUPPORTEDFORMULTIVIEWSHARE — criteria supplied with more than one viewIds entry. |
| [7542](../../../foundations/error-codes.md#error-7542) | 400 | FILTERCRITERIANOTPERMITTEDFORSHAREDUSER — criteria update is not permitted for this share type. |
| [7543](../../../foundations/error-codes.md#error-7543) | 400 | ONLYBASETABLECOLINTABULARFILTERCRITERIA — criteria on a tabular view referenced a column outside its base table. |
| [7545](../../../foundations/error-codes.md#error-7545) | 400 | SHAREANDWRITEPERMISSIONSNOTALLOWEDFORROUSERS — A Read-Only/embedded user was granted share together with a write permission. |
| [7549](../../../foundations/error-codes.md#error-7549) | 400 | CANNOTSHARETOCUSTOMROLEUSER — Attempted to share directly to a user who only has a custom-role-based org-level permission. |
| [8029](../../../foundations/error-codes.md#error-8029) | 400 | SHAREINVALIDEMAILADDRESS — One or more emailIds entries is not a valid email address. |
| [8031](../../../foundations/error-codes.md#error-8031) | 400 | UNTRUSTEDEMAILIDS — A recipient address is outside the organization's trusted domains. |
| [8032](../../../foundations/error-codes.md#error-8032) | 400 | VIEWNOTSHARED — The view is not currently shared with the specified user. |
| [8074](../../../foundations/error-codes.md#error-8074) | 400 | READPERMSHOULDBETRUEFORSHARING — permissions.read was sent as false. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | CONFIG is not valid JSON, was not URL-encoded correctly, contains an unsupported key, or violates a type or length constraint. |
| [8085](../../../foundations/error-codes.md#error-8085) | 400 | SHAREDTOEXTERNALDOMAINNOTALLOWED — Sharing to an email outside the allowed domain(s) is disabled by org policy. |
| [8086](../../../foundations/error-codes.md#error-8086) | 400 | SHAREDTOEXTERNALDOMAINNOTALLOWED — Sharing to an email outside the allowed domain(s) is disabled by org policy. |
| [8105](../../../foundations/error-codes.md#error-8105) | 400 | REMOVESHAREALLVIEWSPRESENT — Both viewIds and removeAllViews: true were supplied together. |
| [8150](../../../foundations/error-codes.md#error-8150) | 400 | VIEWNOTSHAREDTOGROUP — The view is not currently shared with the specified group. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | SYSTEMTAGDATAWARNINGV2VALIDATIONCONFIRMATION — The view carries a restricted DATAWARNING system tag. |

# Related

- [Share & Publish](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
