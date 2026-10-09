---
type: API Group
title: Custom Roles
description: APIs that allow the Account Admin and the Organization Admins of a Zoho Analytics organization to define custom roles - named permission bundles that can be granted to users in place of the built-in roles.
tags:
  - zoho-analytics
  - rest-api-v2
  - users-and-groups
  - custom-roles
  - api-group
api:
  domain: users-and-groups
  group: custom-roles
  endpoint_count: 4
  endpoints:
    - operation_id: getCustomRoles
      method: GET
      path: "/restapi/v2/orgs/roles"
      doc: "/domains/users-and-groups/custom-roles/get-custom-roles.md"
    - operation_id: createCustomRole
      method: POST
      path: "/restapi/v2/orgs/roles"
      doc: "/domains/users-and-groups/custom-roles/create-custom-role.md"
    - operation_id: updateCustomRole
      method: PUT
      path: "/restapi/v2/orgs/roles/{role-id}"
      doc: "/domains/users-and-groups/custom-roles/update-custom-role.md"
    - operation_id: deleteCustomRole
      method: DELETE
      path: "/restapi/v2/orgs/roles/{role-id}"
      doc: "/domains/users-and-groups/custom-roles/delete-custom-role.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/user-groups-grouped-api.json"
    title: OpenAPI 3 specification - user-groups-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

This document covers the four **Custom Role** REST APIs of Zoho Analytics — the APIs that define the named permission bundles an organization can grant to its users instead of the built-in roles.

APIs that allow the Account Admin and the Organization Admins of a Zoho Analytics organization to define custom roles - named permission bundles that can be granted to users in place of the built-in roles.

A custom role is organization-scoped and is made of three parts: a role name, an access type that decides which kinds of view the role can reach (dashboards only, reports and dashboards, or the underlying data as well), and a set of boolean permissions arranged in seven groups. The access type acts as a ceiling - enabling a permission that lies above the chosen access type is rejected with a specific error rather than being silently ignored.

These APIs define roles only. Attaching a role to a user or to a workspace is done through the user management and workspace sharing APIs. The custom roles feature must be enabled for the organization and included in its subscription plan, and none of these APIs is available through a Client Portal (White Label) custom domain.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Custom Roles](get-custom-roles.md) | GET | `/restapi/v2/orgs/roles` | `getCustomRoles` | `ZohoAnalytics.usermanagement.read` | 200 |
| [Create Custom Role](create-custom-role.md) | POST | `/restapi/v2/orgs/roles` | `createCustomRole` | `ZohoAnalytics.usermanagement.create` | 200 |
| [Update Custom Role](update-custom-role.md) | PUT | `/restapi/v2/orgs/roles/{role-id}` | `updateCustomRole` | `ZohoAnalytics.usermanagement.update` | 204 |
| [Delete Custom Role](delete-custom-role.md) | DELETE | `/restapi/v2/orgs/roles/{role-id}` | `deleteCustomRole` | `ZohoAnalytics.usermanagement.delete` | 204 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What a custom role is

A custom role is an **organization-scoped** definition made of three things:

| Part | What it decides |
|------|-----------------|
| `roleName` | What the role is called. |
| `accessType` | **Which kinds of view** the role can reach — dashboards only, reports and dashboards, or data as well. |
| `permissions` | **What the role can do** with the views it reaches, expressed as seven groups of boolean flags. |

The two halves are not independent. `accessType` sets a ceiling, and a permission that lies above that ceiling is rejected rather than ignored — a role limited to dashboards cannot be granted the right to add rows. Most of the validation in this family exists to enforce that relationship, which is why [The `accessType` Hierarchy](overview.md#the-accesstype-hierarchy) and [Permission Dependency Rules](overview.md#permission-dependency-rules) come before the API reference below.

> Custom roles define permissions; they do not assign them. Attaching a role to a user or to a workspace is done through the user- and workspace-management APIs, not here.

---

# How the Four APIs Relate

[Create Custom Role](create-custom-role.md) is the only source of a `roleId`, and [Get Custom Roles](get-custom-roles.md) is the only way to read a role's current definition back — which matters, because [Update Custom Role](update-custom-role.md) replaces permissions wholesale rather than merging them.

```
        2. Create Custom Role  ──►  data.roleId
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        │                               │                               │
        ▼                               ▼                               ▼
  1. Get Custom Roles            3. Update Custom Role          4. Delete Custom Role
  (every role in the org,        (rename, and/or replace        (removes the role
   with full permissions)         accessType + permissions)      definition)
        │                               ▲
        │      read the current         │
        └──────  definition first ──────┘
               before a partial edit
```

| Relationship | Detail |
|--------------|--------|
| **`roleId` has exactly one origin** | [Create Custom Role](create-custom-role.md) returns it as `data.roleId`. [Get Custom Roles](get-custom-roles.md) returns it afterwards as `roles[].roleId`. It is the `<role-id>` path segment for [Update Custom Role](update-custom-role.md) and [Delete Custom Role](delete-custom-role.md). |
| **Get is the mandatory prelude to a permission edit** | [Update Custom Role](update-custom-role.md) does **not** merge: whenever it is given `permissions`, the supplied object replaces the stored one entirely. To change one flag you must read the whole definition from [Get Custom Roles](get-custom-roles.md), modify it, and send it back. |
| **Get returns exactly the shape Update accepts** | `roles[].accessType` and `roles[].permissions` from the read response can be edited and posted straight back as the `accessType` and `permissions` of an update. This round-trip is the intended editing workflow. |
| **A rename needs no read** | Sending only `roleName` to [Update Custom Role](update-custom-role.md) leaves `accessType` and `permissions` untouched. It is the one edit that is safe without a prior read. |
| **`accessType` and `permissions` travel together on update** | Supplying one without the other fails with `7580`. They are validated as a pair because the permissions are only meaningful against an access type. |
| **Every write is validated against the same rule set** | [Create Custom Role](create-custom-role.md) and [Update Custom Role](update-custom-role.md) run identical checks, so the same eleven errors can come from either — see [Permission Dependency Rules](overview.md#permission-dependency-rules). |
| **Deleting a role does not delete its users** | [Delete Custom Role](delete-custom-role.md) removes the definition. Reassigning users who held it is handled by the user-management APIs. |
| **Assignment lives elsewhere** | None of these four attaches a role to a user or a workspace. They manage the definition only. |
| **The feature must be enabled and in plan** | All four fail with `7301` when custom roles are not enabled for the organization, and [Get Custom Roles](get-custom-roles.md) fails with `6142` when the subscription plan does not include them. |

## Typical sequences

**Define a new role and confirm it**

```
Create Custom Role {roleName, accessType, permissions}  →  data.roleId
   → Get Custom Roles                                   →  confirm the stored definition
```

**Change one permission flag safely**

```
Get Custom Roles                    →  roles[] → pick the role → take accessType + permissions
   → flip the one flag in that object
   → Update Custom Role {accessType, permissions}       →  204
   → Get Custom Roles                                   →  verify
```

**Rename only**

```
Update Custom Role {"roleName": "Analysts (EMEA)"}      →  204
```

**Retire a role**

```
Get Custom Roles  →  roleId
   → Delete Custom Role                                 →  204
```

---

# The `accessType` Hierarchy

`accessType` is a single enum with three cumulative levels. Each level includes everything below it.

| Value | Reaches | Adds over the level below |
|-------|---------|---------------------------|
| `ALL_DASHBOARDS` | Dashboards only | — (the most restricted level) |
| `ALL_REPORTS_AND_DASHBOARDS` | Reports **and** dashboards | Reports, and the ability to manage data alerts |
| `ALL_DATA_REPORTS_AND_DASHBOARDS` | Tables, reports **and** dashboards | Underlying data — every data, design, table-creation, and datasource permission becomes available |

The level determines which permission groups may be switched on at all:

| Permission group | `ALL_DASHBOARDS` | `ALL_REPORTS_AND_DASHBOARDS` | `ALL_DATA_REPORTS_AND_DASHBOARDS` |
|------------------|:----------------:|:----------------------------:|:---------------------------------:|
| `interactionPermissions` | ✓ | ✓ | ✓ |
| `sharePermissions` | ✓ | ✓ | ✓ |
| `publishPermissions` — except `manageDataAlerts` | ✓ | ✓ | ✓ |
| `publishPermissions.manageDataAlerts` | – | ✓ | ✓ |
| `createPermissions.createFolder` | ✓ | ✓ | ✓ |
| `createPermissions` — `createTable`, `createQueryTable`, `createFormula` | – | – | ✓ |
| `dataPermissions` | – | – | ✓ |
| `designPermissions` | – | – | ✓ |
| `datasourcePermissions` | – | – | ✓ |

Switching on a permission marked `–` for the chosen level is an error, not a silent no-op. The specific code depends on the group — see [Permission Dependency Rules](overview.md#permission-dependency-rules).

---

# Permission Dependency Rules

Eleven rules are enforced on every [Create Custom Role](create-custom-role.md) and [Update Custom Role](update-custom-role.md) call. They run **before** anything is stored, so a rejected request changes nothing.

| # | Rule | Error |
|---|------|-------|
| 1 | `interactionPermissions.read` must be `true`. Always, at every access level. | `7579` |
| 2 | Any `dataPermissions` flag requires `accessType` = `ALL_DATA_REPORTS_AND_DASHBOARDS`. | `7573` |
| 3 | Any `datasourcePermissions` flag requires `accessType` = `ALL_DATA_REPORTS_AND_DASHBOARDS`. | `7584` |
| 4 | `designPermissions.designModify` requires `accessType` = `ALL_DATA_REPORTS_AND_DASHBOARDS`. | `7574` |
| 5 | `createTable`, `createQueryTable`, and `createFormula` require `accessType` = `ALL_DATA_REPORTS_AND_DASHBOARDS`. | `7575` |
| 6 | `publishPermissions.manageDataAlerts` requires `accessType` = `ALL_REPORTS_AND_DASHBOARDS` or `ALL_DATA_REPORTS_AND_DASHBOARDS`. | `7576` |
| 7 | `designPermissions.designModify` additionally requires **both** `sharePermissions.accessAdminPresets` and `sharePermissions.createPreset` to be `true`. | `7578` |
| 8 | `publishPermissions.manageEmailSchedules` requires `publishPermissions.export` to be `true`. | `7559` |
| 9 | `datasourcePermissions.useDatasource` requires `createPermissions.createTable` to be `true`. | `7585` |
| 10 | `editDatasource`, `syncData`, `useDatasource`, and `removeDatasource` each require `datasourcePermissions.viewDatasource` to be `true`. | `7586` |
| 11 | `dataPermissions.dataArchives` requires `accessType` = `ALL_DATA_REPORTS_AND_DASHBOARDS` **and every data permission to be enabled**. | `7577` |

> **Rule 1 is the one that catches people first.** `read` is not defaulted for you. A `permissions` object that omits `interactionPermissions` entirely — or sets `read` to `false` — is rejected with [`7579`](../../../foundations/error-codes.md#error-7579) even if everything else is valid.

> **Rules 7, 8, 9, and 10 are cross-group dependencies.** They reach across the permission buckets, so a payload assembled group-by-group can look complete and still fail. Check them before sending: design modify pulls in two share permissions, email schedules pull in export, and the datasource group has its own internal prerequisites.

---

# Limitations

These are the limits that apply with **default settings**.

| Limitation | Value | Enforced by |
|------------|-------|-------------|
| **`roleName` length** | **1–30** characters. | `8507` |
| **`roleName` characters** | Letters, digits, spaces, underscore, and hyphen only. | `8509` |
| **`roleName` uniqueness** | Must be unique across the organization, including against built-in role names. | `7553` |
| **`permissions` size** | **5,000** characters serialized. | `8507` |
| **Each permission group's size** | **500** characters serialized. | `8507` |
| **`CONFIG` length** | **1,000,000** characters. | `8507` |
| **`accessType` values** | Exactly three; see [The `accessType` Hierarchy](overview.md#the-accesstype-hierarchy). | `8509` |
| **Bulk operations** | **Not supported.** Create, update, and delete each act on exactly one role per call. | — |
| **Role assignment** | **Not supported by these APIs.** They define roles; attaching them to users or workspaces is done elsewhere. | — |
| **Partial permission edits** | **Not supported.** [Update Custom Role](update-custom-role.md) replaces the whole `permissions` object. | — |
| **Client Portal / White Label** | All four APIs are unavailable through a custom domain. | `7301` |
| **Feature availability** | The organization must have custom roles enabled and included in its plan. | `7301`, `6142` |

> **There is no partial permission update and no permission-level endpoint.** Every change to what a role can do means sending the complete `permissions` object again. Read it with [Get Custom Roles](get-custom-roles.md) first; anything you leave out is switched off.

---

# Permission Model

| API | Who may call it |
|-----|-----------------|
| [Get Custom Roles](get-custom-roles.md) | An Account Admin or Organization Admin. |
| [Create Custom Role](create-custom-role.md) | An Account Admin or Organization Admin. |
| [Update Custom Role](update-custom-role.md) | An Account Admin or Organization Admin. |
| [Delete Custom Role](delete-custom-role.md) | An Account Admin or Organization Admin. |

No other role qualifies. A Workspace Admin, a View Owner, a user holding a custom role, and a shared user are all rejected with [`7301`](../../../foundations/error-codes.md#error-7301).

| Gate | Behaviour |
|------|-----------|
| **Custom roles must be enabled for the organization** | Otherwise every API fails with `7301`, even for an Account Admin. |
| **The plan must include custom roles** | Otherwise `6142`. |
| **Client Portal / White Label** | All four are unavailable through a custom domain and are rejected with `7301` before the role check runs. |
| **Authentication** | An absent or unusable token yields `7309`; an invalid or expired one yields `8535`. |

---

# Permission Groups

`permissions` is an object of seven groups. Every value inside a group is a boolean, and **an omitted flag is treated as `false`** — which is why an update must resend the complete object.

| Group | Governs | Requires `ALL_DATA_REPORTS_AND_DASHBOARDS` |
|-------|---------|:------------------------------------------:|
| `createPermissions` | Creating folders, tables, query tables, and formula columns | Partly — `createFolder` is available at every level |
| `dataPermissions` | Adding, changing, and importing rows | Yes |
| `designPermissions` | Changing a view's design | Yes |
| `interactionPermissions` | Viewing and exploring a view | No |
| `sharePermissions` | Re-sharing, discussions, private links, presets | No |
| `publishPermissions` | Export, email schedules, alerts, slideshows, public views | Partly — `manageDataAlerts` needs reports access |
| `datasourcePermissions` | Viewing and managing the datasource behind a table | Yes |

The complete key list for each group is in [Permission Reference](overview.md#permission-reference).

---

# API-Specific Notes and Behaviours

## Get Custom Roles

- **It is the only read in the family, and there is no get-by-ID.** Every workflow that touches an existing role starts by listing all of them and filtering client-side.
- **Its response is deliberately the update request shape.** `accessType` and `permissions` can be lifted straight out of a role here and posted back to [Update Custom Role](update-custom-role.md). Treat the read as the first half of every permission edit.
- **The response is always complete**, with all seven groups and every flag present including the `false` ones — unlike the request side, where omission means `false`.
- **It reports definitions, not assignments.** Nothing here tells you who holds a role; that lives in the user-management APIs.
- **[`6142`](../../../foundations/error-codes.md#error-6142) and [`7301`](../../../foundations/error-codes.md#error-7301) mean different things.** [`6142`](../../../foundations/error-codes.md#error-6142) is a plan limitation, [`7301`](../../../foundations/error-codes.md#error-7301) covers three separate causes — wrong role, feature disabled, or custom domain. Only [`6142`](../../../foundations/error-codes.md#error-6142) is resolved by a subscription change.
- **Dependency chain:** Get Custom Roles → `roles[].roleId` → [Update Custom Role](update-custom-role.md) / [Delete Custom Role](delete-custom-role.md).

## Create Custom Role

- **`read` is the single most common failure.** It is not defaulted, so a `permissions` object that omits `interactionPermissions` is rejected with [`7579`](../../../foundations/error-codes.md#error-7579) before any other rule is evaluated. Set it explicitly, always.
- **`accessType` is a ceiling, not a hint.** Enabling a permission above the chosen level is an error rather than a silent downgrade, and which error you get depends on the group — five different codes cover the same underlying idea.
- **Four rules cross group boundaries**, which is what makes a hand-assembled payload fail in ways that are hard to read: design modify pulls in two share permissions, email schedules pull in export, `useDatasource` pulls in `createTable`, and every other datasource flag pulls in `viewDatasource`.
- **`roleName` is 30 characters, not 100.** It is also restricted to letters, digits, spaces, underscore, and hyphen.
- **It is not an upsert**, so a re-runnable provisioning script must read [Get Custom Roles](get-custom-roles.md) first and branch, or tolerate [`7553`](../../../foundations/error-codes.md#error-7553).
- **Creating a role changes nobody's access** until it is assigned elsewhere.
- **Dependency chain:** Create Custom Role → `data.roleId` → [Get Custom Roles](get-custom-roles.md) to verify.

## Update Custom Role

- **The replace-not-merge behaviour is the thing to get right.** Supplying `permissions` discards the stored object entirely, so an update built from "just the flags I want to change" silently strips everything else. Always round-trip through [Get Custom Roles](get-custom-roles.md).
- **`permissions` alone is rejected**, which surprises most callers: the natural payload for "change these permissions" fails with [`7580`](../../../foundations/error-codes.md#error-7580). Resend the role's existing `accessType` alongside it.
- **Renaming is the only genuinely partial edit**, and the only one that needs no prior read.
- **Downgrading `accessType` is a two-part change.** The lower level and the cleaned permission set must arrive in the same payload, or the higher-level flags left behind trigger [`7573`](../../../foundations/error-codes.md#error-7573) / [`7574`](../../../foundations/error-codes.md#error-7574) / [`7575`](../../../foundations/error-codes.md#error-7575) / [`7576`](../../../foundations/error-codes.md#error-7576) / [`7584`](../../../foundations/error-codes.md#error-7584).
- **Changes apply immediately to everyone holding the role.** There is no draft, no version, and no staged rollout.
- **[`8525`](../../../foundations/error-codes.md#error-8525) versus [`7548`](../../../foundations/error-codes.md#error-7548).** A non-numeric ID fails at routing and never reaches the API; a numeric but unknown ID reaches it and returns [`7548`](../../../foundations/error-codes.md#error-7548).
- **Dependency chain:** [Get Custom Roles](get-custom-roles.md) → edit `accessType` + `permissions` → Update Custom Role → [Get Custom Roles](get-custom-roles.md).

## Delete Custom Role

- **It deletes a definition, not the people holding it.** Plan the reassignment of affected users through the user-management APIs before calling it; nothing here reports or handles them.
- **It is not idempotent.** The second call returns [`7548`](../../../foundations/error-codes.md#error-7548), so cleanup scripts should treat that code as success rather than retrying.
- **There is no impact report and no undo.** Recreating the name yields a fresh role with a new ID.
- **Dependency chain:** [Get Custom Roles](get-custom-roles.md) → `roleId` → Delete Custom Role.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Two APIs return a body, two return 204** | [Get Custom Roles](get-custom-roles.md) and [Create Custom Role](create-custom-role.md) return `200` with the standard envelope. [Update Custom Role](update-custom-role.md) and [Delete Custom Role](delete-custom-role.md) return `204 No Content` with an empty body. |
| **A 204 carries no confirmation of what changed** | Neither mutating API reports the resulting definition. Verification is a follow-up [Get Custom Roles](get-custom-roles.md). |
| **Failure responses share one shape** | `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name (for example `CR_READ_PERM_MUST_BE_ENABLED`), not a localised sentence. |
| **Success `summary` values are terse** | `"Get roles"` and `"Create role"`. Do not branch on summary text. |
| **IDs are strings** | `roleId` is a JSON string in both the create response and the read response, even though it is numerically a long. |
| **Permission flags are real booleans** | Every leaf inside the seven groups is a JSON `true` / `false`, never a string. |
| **The read response is always complete** | All seven groups and every flag appear, including `false` ones. Request payloads are the opposite — omission means `false`. |
| **An empty role list is a success** | `{"roles": []}` with HTTP 200. |
| **Validation errors leave nothing changed** | Every rule is evaluated before anything is stored, so a rejected create produces no role and a rejected update leaves the role as it was. |
| **One error is reported at a time** | Rules are checked in a fixed order, so a payload with several problems surfaces them one call at a time. |

---

# Permission Reference

Every recognised permission key, by group. All are booleans, and **an omitted key is treated as `false`**.

**`createPermissions`**

| Key | Allows | Minimum `accessType` |
|-----|--------|----------------------|
| `createFolder` | Creating folders | `ALL_DASHBOARDS` |
| `createTable` | Creating tables and importing data into new ones | `ALL_DATA_REPORTS_AND_DASHBOARDS` |
| `createQueryTable` | Creating query tables | `ALL_DATA_REPORTS_AND_DASHBOARDS` |
| `createFormula` | Creating formula columns | `ALL_DATA_REPORTS_AND_DASHBOARDS` |

**`dataPermissions`** — every key requires `ALL_DATA_REPORTS_AND_DASHBOARDS`

| Key | Allows |
|-----|--------|
| `addRow` | Adding rows to a table |
| `modifyRow` | Changing existing rows |
| `deleteRow` | Deleting rows. Also confers the bulk delete-all-rows capability. |
| `importAppend` | Importing in append mode |
| `importAddOrUpdate` | Importing in add-or-update mode |
| `importDeleteAllAdd` | Importing in delete-all-and-add mode |
| `dataArchives` | Managing scheduled data deletion. Requires **every** data permission to be enabled — see rule 11 in [Permission Dependency Rules](overview.md#permission-dependency-rules). |

**`designPermissions`**

| Key | Allows | Requires |
|-----|--------|----------|
| `designModify` | Changing a view's design — formatting, layout, structure | `ALL_DATA_REPORTS_AND_DASHBOARDS`, plus `accessAdminPresets` and `createPreset` |

**`interactionPermissions`** — available at every `accessType`

| Key | Allows |
|-----|--------|
| `read` | Viewing the shared item. **Must always be `true`.** |
| `vud` | Viewing the underlying data of a report |
| `drillDown` | Drilling down within a report |
| `drillThrough` | Drilling through to a linked report |
| `drillActions` | Running drill actions |
| `insight` | Using the AI and insight features on a view |

**`sharePermissions`** — available at every `accessType`

| Key | Allows |
|-----|--------|
| `share` | Re-sharing a view with other users |
| `discussion` | Taking part in view discussions and comments |
| `privateLinks` | Generating private links for a view |
| `accessAdminPresets` | Viewing presets created by the workspace administrator |
| `createPreset` | Creating personal filter and column presets |

**`publishPermissions`**

| Key | Allows | Minimum `accessType` |
|-----|--------|----------------------|
| `export` | Exporting view data | `ALL_DASHBOARDS` |
| `manageEmailSchedules` | Creating and editing email schedules. **Requires `export`.** | `ALL_DASHBOARDS` |
| `allEmailSchedulesAccess` | Also managing email schedules created by other users | `ALL_DASHBOARDS` |
| `manageDataAlerts` | Creating and editing data alerts | `ALL_REPORTS_AND_DASHBOARDS` |
| `allDataAlertsAccess` | Also managing data alerts created by other users | `ALL_REPORTS_AND_DASHBOARDS` |
| `createSlideshow` | Creating slideshows from dashboards | `ALL_DASHBOARDS` |
| `publicViews` | Making a view publicly accessible | `ALL_DASHBOARDS` |

**`datasourcePermissions`** — every key requires `ALL_DATA_REPORTS_AND_DASHBOARDS`

| Key | Allows | Also requires |
|-----|--------|---------------|
| `viewDatasource` | Seeing the datasource behind a table | — |
| `editDatasource` | Changing datasource connection details | `viewDatasource` |
| `syncData` | Triggering a data sync | `viewDatasource` |
| `useDatasource` | Building new tables from an existing datasource | `viewDatasource` **and** `createTable` |
| `removeDatasource` | Removing a datasource | `viewDatasource` |

> `allEmailSchedulesAccess` and `allDataAlertsAccess` are sub-options. Each widens the scope of its parent permission from "schedules I created" to "all schedules", and has no effect unless its parent is `true`.

---

# `accessType` ↔ Permission Availability Matrix

`✓` may be enabled, `–` rejected at that level.

| Permission | `ALL_DASHBOARDS` | `ALL_REPORTS_AND_DASHBOARDS` | `ALL_DATA_REPORTS_AND_DASHBOARDS` | Error if enabled below its level |
|------------|:---:|:---:|:---:|---|
| `read`, `vud`, `drillDown`, `drillThrough`, `drillActions`, `insight` | ✓ | ✓ | ✓ | — |
| `share`, `discussion`, `privateLinks`, `accessAdminPresets`, `createPreset` | ✓ | ✓ | ✓ | — |
| `export`, `manageEmailSchedules`, `allEmailSchedulesAccess`, `createSlideshow`, `publicViews` | ✓ | ✓ | ✓ | — |
| `createFolder` | ✓ | ✓ | ✓ | — |
| `manageDataAlerts`, `allDataAlertsAccess` | – | ✓ | ✓ | `7576` |
| `createTable`, `createQueryTable`, `createFormula` | – | – | ✓ | `7575` |
| `addRow`, `modifyRow`, `deleteRow`, `importAppend`, `importAddOrUpdate`, `importDeleteAllAdd`, `dataArchives` | – | – | ✓ | `7573` |
| `designModify` | – | – | ✓ | `7574` |
| `viewDatasource`, `editDatasource`, `syncData`, `useDatasource`, `removeDatasource` | – | – | ✓ | `7584` |

---

# CONFIG Attribute Availability by API

`✓` accepted, `–` not accepted by that API.

| Attribute | Get Custom Roles | Create Custom Role | Update Custom Role | Delete Custom Role |
|-----------|:---:|:---:|:---:|:---:|
| `roleName` | – | ✓ **mandatory** | ✓ conditional | – |
| `accessType` | – | ✓ **mandatory** | ✓ conditional — with `permissions` | – |
| `permissions` | – | ✓ **mandatory** | ✓ conditional — with `accessType` | – |

[Get Custom Roles](get-custom-roles.md) and [Delete Custom Role](delete-custom-role.md) take no CONFIG at all.

**Valid update combinations**

| `roleName` | `accessType` | `permissions` | Result |
|:---:|:---:|:---:|---|
| ✓ | – | – | Rename only; permissions preserved |
| – | ✓ | ✓ | Access level and permissions replaced; name preserved |
| ✓ | ✓ | ✓ | Everything replaced |
| – | – | – | `7581` |
| – | ✓ | – | `7580` |
| – | – | ✓ | `7580` |
| ✓ | ✓ | – | `7580` |
| ✓ | – | ✓ | `7580` |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [6142](../../../foundations/error-codes.md#error-6142) | 400 | The subscription plan of the organization does not include custom roles. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7309](../../../foundations/error-codes.md#error-7309) | 400 | No authentication was supplied with the request. |
| [7548](../../../foundations/error-codes.md#error-7548) | 400 | No custom role exists for the given role-id in this organization. |
| [7553](../../../foundations/error-codes.md#error-7553) | 400 | A role with the given roleName already exists in the organization. The check covers built-in role names as well as other custom roles. |
| [7554](../../../foundations/error-codes.md#error-7554) | 400 | The accessType value did not resolve to a known access level. |
| [7559](../../../foundations/error-codes.md#error-7559) | 400 | manageEmailSchedules is enabled but export is not. |
| [7573](../../../foundations/error-codes.md#error-7573) | 400 | A dataPermissions flag is enabled while accessType is below ALL_DATA_REPORTS_AND_DASHBOARDS. |
| [7574](../../../foundations/error-codes.md#error-7574) | 400 | designModify is enabled while accessType is below ALL_DATA_REPORTS_AND_DASHBOARDS. |
| [7575](../../../foundations/error-codes.md#error-7575) | 400 | createTable, createQueryTable or createFormula is enabled while accessType is below ALL_DATA_REPORTS_AND_DASHBOARDS. |
| [7576](../../../foundations/error-codes.md#error-7576) | 400 | manageDataAlerts is enabled while accessType is ALL_DASHBOARDS. |
| [7577](../../../foundations/error-codes.md#error-7577) | 400 | dataArchives is enabled but not every other dataPermissions flag is enabled. |
| [7578](../../../foundations/error-codes.md#error-7578) | 400 | designModify is enabled without both accessAdminPresets and createPreset. |
| [7579](../../../foundations/error-codes.md#error-7579) | 400 | interactionPermissions.read is missing or false. Read permission must always be enabled. |
| [7580](../../../foundations/error-codes.md#error-7580) | 400 | One of accessType and permissions was sent without the other. |
| [7581](../../../foundations/error-codes.md#error-7581) | 400 | The CONFIG contained neither roleName nor accessType, so there is nothing to update. |
| [7584](../../../foundations/error-codes.md#error-7584) | 400 | A datasourcePermissions flag is enabled while accessType is below ALL_DATA_REPORTS_AND_DASHBOARDS. |
| [7585](../../../foundations/error-codes.md#error-7585) | 400 | useDatasource is enabled but createTable is not. |
| [7586](../../../foundations/error-codes.md#error-7586) | 400 | editDatasource, syncData, useDatasource or removeDatasource is enabled without viewDatasource. |
| [8078](../../../foundations/error-codes.md#error-8078) | 400 | A mandatory attribute was sent with an empty value. The error message names the attribute. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | The ZANALYTICS-ORGID header is missing from a request that requires it. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | CONFIG was not sent. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | roleName exceeds 30 characters, or the serialized permissions object exceeds its size limit. |
| [8509](../../../foundations/error-codes.md#error-8509) | 400 | roleName contains characters other than letters, digits, spaces, underscore and hyphen, or accessType is not one of the three allowed values. |
| [8525](../../../foundations/error-codes.md#error-8525) | 400 | The role-id in the request URI is not numeric, so the request matched no route. |
| [8534](../../../foundations/error-codes.md#error-8534) | 400 | CONFIG is not valid JSON. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |
| [8539](../../../foundations/error-codes.md#error-8539) | 400 | An attribute carries a value that is structurally valid but not accepted, such as an empty roleName. |

# Related

- [Users & Groups](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
