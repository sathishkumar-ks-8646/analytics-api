---
type: API Group
title: Linked Workspaces
description: "APIs for listing, linking, syncing and unlinking client workspaces against a master workspace, and for checking which workspaces can be linked."
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - linked-workspaces
  - api-group
api:
  domain: workspace-management
  group: linked-workspaces
  endpoint_count: 8
  endpoints:
    - operation_id: getLinkedWorkspacesForOrganization
      method: GET
      path: "/restapi/v2/linkedworkspaces"
      doc: "/domains/workspace-management/linked-workspaces/get-linked-workspaces-for-organization.md"
    - operation_id: getLinkedWorkspacesForMasterWorkspace
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/linkedworkspaces"
      doc: "/domains/workspace-management/linked-workspaces/get-linked-workspaces-for-master-workspace.md"
    - operation_id: getLinkableWorkspaces
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/linkable"
      doc: "/domains/workspace-management/linked-workspaces/get-linkable-workspaces.md"
    - operation_id: getWorkspaceLinkingCompatibility
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/compatibility"
      doc: "/domains/workspace-management/linked-workspaces/get-workspace-linking-compatibility.md"
    - operation_id: linkWorkspaces
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/linkedworkspaces"
      doc: "/domains/workspace-management/linked-workspaces/link-workspaces.md"
    - operation_id: syncLinkedWorkspaces
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync"
      doc: "/domains/workspace-management/linked-workspaces/sync-linked-workspaces.md"
    - operation_id: getLinkedWorkspaceSyncDetails
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync"
      doc: "/domains/workspace-management/linked-workspaces/get-linked-workspace-sync-details.md"
    - operation_id: unlinkWorkspaces
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/linkedworkspaces"
      doc: "/domains/workspace-management/linked-workspaces/unlink-workspaces.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-20T17:34:40Z
generated:
  by: process:build_okf
  at: 2026-10-23T07:58:54Z
status: stable
---

# Summary

This document covers the V2 **Linked Workspace** REST APIs of Zoho Analytics — the APIs that discover which workspaces can be linked to a master, check them for compatibility, link and unlink them, push the master's design down to them, and report what each push did.

APIs for listing, linking, syncing and unlinking client workspaces against a master workspace, and for checking which workspaces can be linked.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Linked Workspaces For Organization](get-linked-workspaces-for-organization.md) | GET | `/restapi/v2/linkedworkspaces` | `getLinkedWorkspacesForOrganization` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md) | GET | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces` | `getLinkedWorkspacesForMasterWorkspace` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Linkable Workspaces](get-linkable-workspaces.md) | GET | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/linkable` | `getLinkableWorkspaces` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md) | GET | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/compatibility` | `getWorkspaceLinkingCompatibility` | `ZohoAnalytics.metadata.read` | 200 |
| [Link Workspaces](link-workspaces.md) | POST | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces` | `linkWorkspaces` | `ZohoAnalytics.modeling.create` | 204 |
| [Sync Linked Workspaces](sync-linked-workspaces.md) | POST | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync` | `syncLinkedWorkspaces` | `ZohoAnalytics.modeling.create` | 204 |
| [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync` | `getLinkedWorkspaceSyncDetails` | `ZohoAnalytics.metadata.read` | 200 |
| [Unlink Workspaces](unlink-workspaces.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces` | `unlinkWorkspaces` | `ZohoAnalytics.modeling.delete` | 204 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is a "Linked Workspace" in Zoho Analytics?

Workspace linking lets one **master** workspace act as the design source for any number of **client** workspaces, which may live in other organisations. The master holds the canonical tables, reports and dashboards; a **sync** copies that design into every client. Each master↔client pair is tracked by a **sandbox ID**, and that sandbox ID — not the client workspace ID — is the handle every downstream operation uses.

| Part | CONFIG attribute(s) | Notes |
|------|--------------------|-------|
| **What is the source** | `<workspace-id>` in the URL | Always the **master** workspace. It cannot itself be a client of another master (`8246`). There is no CONFIG attribute for it. |
| **What gets linked** | `clients[].orgId`, `clients[].workspaceIds` | Candidate client workspaces, grouped by the organisation that owns them. The caller must be an admin of every organisation named. |
| **What is pushed** | `scope`, `clients[].scope`, `clients[].masterViewIds` | A sync either pushes everything or a named list of master-workspace views, per client. |
| **What identifies a link** | `sandboxId`, `sandboxIds` | The mapping ID minted when a link is created. Unlink and sync-filter operations address links by this value — see [The Master, the Client and the Sandbox ID](overview.md#the-master-the-client-and-the-sandbox-id). |

> **The single most important behaviour:** [Link Workspaces](link-workspaces.md) and [Sync Linked Workspaces](sync-linked-workspaces.md) return `204` when the work has been **scheduled**, not when it has finished. Nothing in the response tells you what was linked or pushed — read it back with [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md).

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`). The five read APIs use the **`metadata`** scope family; the three write APIs use the **`modeling`** scope family — see [OAuth scopes](../../../foundations/oauth-scopes.md).
> - All eight APIs require the `ZANALYTICS-ORGID` header, which names the organisation that owns the **master** workspace. A missing header is [`8083`](../../../foundations/error-codes.md#error-8083).
> - `ZohoAnalytics_Server_URI` depends on the data centre (`analyticsapi.zoho.com`, `.eu`, `.in`, `.com.au`, `.jp`, …).
> - **All eight APIs are disabled in Client Portal / White Label request contexts.** A request that arrives through a custom domain is rejected with [`7301`](../../../foundations/error-codes.md#error-7301) before any business logic runs — see [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour).
> - **All eight APIs are organisation-admin only.** The caller must be an Account Admin or an Organization Admin — of the master's organisation, and of every client organisation the request touches. There is no per-workspace permission that grants access here.
> - Seven of the eight are **master-scoped** (`/workspaces/<workspace-id>/linkedworkspaces...`); only [Get Linked Workspaces For Organization](get-linked-workspaces-for-organization.md) is organisation-scoped.
> - None of these APIs accepts a `criteria` attribute, and none of them reads or writes table rows — no API here uses the `data` scope family.

---

# The Master, the Client and the Sandbox ID

Three identifiers circulate through these APIs and they are not interchangeable.

| Identifier | Where it comes from | What addresses it |
|---|---|---|
| **Master workspace ID** | Any workspace you own, via [Get All Workspace List](../workspace-operations/get-all-workspaces.md) | The `<workspace-id>` path segment of seven of the eight APIs. |
| **Client workspace ID** | [Get Linkable Workspaces](get-linkable-workspaces.md) | `clients[].workspaceIds` on [Link Workspaces](link-workspaces.md) and [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md). **Nothing else accepts it.** |
| **Sandbox ID** | Minted by [Link Workspaces](link-workspaces.md); read back from `clients[].workspaces[].sandboxId` of [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md) | `sandboxIds` on [Unlink Workspaces](unlink-workspaces.md) and [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md); `clients[].sandboxId` on [Sync Linked Workspaces](sync-linked-workspaces.md). |

The rule the server applies is: **you link by client workspace ID, and you operate on the link by sandbox ID.** Practical consequences:

1. **The sandbox ID is not returned by the call that creates it.** [Link Workspaces](link-workspaces.md) answers `204` with no body. The only way to learn the new sandbox IDs is to call [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md) afterwards — and because linking is scheduled rather than immediate, they may not be there on the first attempt.
2. **Passing a client workspace ID where a sandbox ID is expected fails with [`8248`](../../../foundations/error-codes.md#error-8248),** not with a type error. The two id spaces look alike.
3. **A master cannot be a client.** If `<workspace-id>` is already linked as somebody's client, [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md), [Link Workspaces](link-workspaces.md) and [Sync Linked Workspaces](sync-linked-workspaces.md) all fail with [`8246`](../../../foundations/error-codes.md#error-8246).
4. **Links whose master or client workspace has been deleted are purged on read.** The two listing APIs delete the stale mapping rows as a side effect, so a sandbox ID that worked yesterday can be gone today with no write having been issued.

---

# The `scope` Attribute

Three APIs take a `scope` attribute, and it means the same thing each time: **`ALL` operates on everything the server can resolve; `SELECTED` requires you to enumerate the targets.** The pairing is strict — supplying the enumeration with `ALL`, or omitting it with `SELECTED`, is rejected rather than ignored.

| API | `scope` | Must be accompanied by | Must omit | Error if wrong |
|---|---|---|---|---|
| [Unlink Workspaces](unlink-workspaces.md) | `ALL` | — | `sandboxIds` | `8249` |
| [Unlink Workspaces](unlink-workspaces.md) | `SELECTED` | `sandboxIds` (non-empty) | — | `8249` |
| [Sync Linked Workspaces](sync-linked-workspaces.md) top level | `ALL` | — | `clients` | `8250` |
| [Sync Linked Workspaces](sync-linked-workspaces.md) top level | `SELECTED` | `clients` (non-empty) | — | `8250` |
| [Sync Linked Workspaces](sync-linked-workspaces.md) per client | `ALL` | — | `masterViewIds` | `8251` |
| [Sync Linked Workspaces](sync-linked-workspaces.md) per client | `SELECTED` | `masterViewIds` (non-empty) | — | `8251` |

> **The top-level `scope` is case-sensitive; the per-client `scope` is not.** `clients[].scope` is upper-cased before it is compared, so `"all"` and `"All"` are accepted there. The top-level `scope` on [Unlink Workspaces](unlink-workspaces.md) and [Sync Linked Workspaces](sync-linked-workspaces.md) is compared verbatim — `"all"` fails with [`8119`](../../../foundations/error-codes.md#error-8119), naming `ALL, SELECTED` as the permitted values. Send upper case everywhere and the inconsistency never bites.

---

# Limitations

These are the limits that apply with **default settings**.

| Limitation | Value | Enforced by |
|------------|-------|-------------|
| **Client organisations per request** | **1–100** entries in `clients`. | Request template |
| **Client workspaces per organisation entry** | **1–100** entries in `clients[].workspaceIds`. | Request template |
| **`sandboxIds` per request** | **1–100** entries. | Request template |
| **`masterViewIds` per client entry** | **1–1000** entries. | Request template |
| **CONFIG size — [Link Workspaces](link-workspaces.md) / [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md)** | **500,000** characters. | Request template |
| **CONFIG size — [Sync Linked Workspaces](sync-linked-workspaces.md)** | **5,000,000** characters. | Request template |
| **CONFIG size — [Unlink Workspaces](unlink-workspaces.md) / [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md)** | **5,000** characters. | Request template |
| **Masters per organisation listing** | Keyed by master workspace **name**, not ID. | — |
| **Pagination, filtering, sorting** | **None on any API here.** Every result set is returned whole. | — |

> **The organisation listing is keyed by master workspace name.** [Get Linked Workspaces For Organization](get-linked-workspaces-for-organization.md) groups its results by the master's display name, so two masters in the same organisation sharing a name collapse into a single entry whose `clients` array holds both sets. Workspace names are unique within an organisation in normal use, but if you have renamed workspaces across organisations, prefer the per-master listing.

---

# Permission Model

| Role | May do | Notes |
|------|--------|-------|
| Account Admin / Organization Admin of the master's organisation | Every API in this document, for masters in that organisation. | The only role that qualifies. |
| Account Admin / Organization Admin of a **client** organisation as well | Additionally link, validate and list workspaces belonging to that client organisation. | Checked per organisation named in `clients[].orgId`. |
| Workspace Admin, custom-role user, shared user | Nothing. | `7301`. |

Two consequences worth stating plainly:

- **Cross-organisation linking needs admin rights on both sides.** [Link Workspaces](link-workspaces.md) and [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md) re-check `isOrgAdminOrSuperAdmin` for every `clients[].orgId` in the payload, so an Account Admin of the master organisation alone cannot pull in a workspace from an organisation they do not administer.
- **The listing APIs filter rather than fail.** Links whose master or client organisation the caller does not administer are **silently omitted** from [Get Linked Workspaces For Organization](get-linked-workspaces-for-organization.md) and [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md). An incomplete list is not an error, so never treat "absent" as "not linked" unless you know the caller administers every organisation involved.

---

# White Label / Client Portal Behaviour

All eight APIs are blocked in Client Portal / White Label request contexts — the same posture as the [Email Schedule APIs](../../schedules-and-alerts/email-schedules/overview.md#white-label--client-portal-behaviour).

| Scenario | Result |
|----------|--------|
| The request arrives **through** a Client Portal / White Label custom domain | **Rejected with `7301`** before any business logic runs. |
| The request is sent to the **standard** API host for a workspace that happens to be white-labelled | **Allowed**, and behaves exactly as for any other workspace. |

There is no `domainName` CONFIG attribute on any of these APIs. Manage linked workspaces for a white-labelled organisation by calling the standard `analyticsapi.zoho.*` host.

---

# API-Specific Notes and Behaviours

## Get Linked Workspaces For Organization

- **The broadest discovery call, and the usual source of `sandboxId`.** Everything except [Get Linkable Workspaces](get-linkable-workspaces.md) ultimately needs an ID that starts here or in the per-master listing.
- **Scoped to the header organisation.** Only masters owned by `ZANALYTICS-ORGID` are listed; repeat the call per organisation.
- **Filtered, not refused.** Links whose master or client organisation the caller does not administer vanish from the response without comment, so an empty array may mean "none visible" rather than "none exist".
- **Reading deletes stale mappings.** Links pointing at a deleted master or client workspace are purged while the response is built — a `GET` with a persistent side effect.
- **Grouped by master workspace name.** Two masters sharing a display name collapse into one entry; see [Limitations](overview.md#limitations).
- **`syncTime` is epoch milliseconds in a string,** `"0"` when the link has never synced.
- **Dependency chain:** [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md) → `ZANALYTICS-ORGID` → Get Linked Workspaces For Organization → `sandboxId`.

## Get Linked Workspaces For Master Workspace

- **Same data, different container.** `data.linkedWorkspaces` is a JSON **object** here and a JSON **array** in the organisation listing. A shared parser must branch.
- **"Not linked" is `{}` and HTTP 200.** An unlinked workspace, a fully filtered result and a workspace that is not a master are indistinguishable. This API never raises [`8246`](../../../foundations/error-codes.md#error-8246).
- **Same filtering and same housekeeping side effect** as the organisation listing.
- **This is where a freshly created link first becomes visible.** Because [Link Workspaces](link-workspaces.md) only schedules the work, poll here until the new `sandboxId` appears.
- **Dependency chain:** [Get All Workspace List](../workspace-operations/get-all-workspaces.md) → `<workspace-id>` → Get Linked Workspaces For Master Workspace → `sandboxId`.

## Get Linkable Workspaces

- **The only catalogue of link candidates.** `clients[].workspaceIds` is not validated against any other list, so driving the picker from here is what keeps [Link Workspaces](link-workspaces.md) from failing late.
- **Eligible is not the same as compatible.** This call excludes workspaces that are already a master, already a client, or already scheduled to link. Design-level fitness is [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md)'s job.
- **The response key is `orgs`; the request key is `clients`.** The two shapes deliberately do not mirror each other — map `orgs[].orgId` → `clients[].orgId` and `orgs[].workspaces[].workspaceId` → `clients[].workspaceIds[]`.
- **Candidates span every organisation the caller administers,** which is what makes cross-organisation linking possible at all.
- **`orgId` can be `""`.** When the server could not resolve an organisation ID it returns the organisation name as the grouping key and leaves `orgId` empty; such an entry cannot be used in a write payload.
- **Dependency chain:** [Get All Workspace List](../workspace-operations/get-all-workspaces.md) → Get Linkable Workspaces → [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md).

## Get Workspace Linking Compatibility

- **A dry run of exactly what [Link Workspaces](link-workspaces.md) enforces.** The linking API calls this same routine and refuses the whole request if any candidate fails, so running it first turns an all-or-nothing rejection into a per-workspace report.
- **Incompatibility is a `200`.** Only request-level problems produce a failure envelope. Branch on `isCompatible`.
- **Three result shapes, not two.** Compatible (`error: null`, `entities` populated but empty); blocked at workspace level (`error` = reason, **`entities: null`**); blocked by entity conflicts (`error` = `"Some entities have conflicts"`, `entities` populated). Guard before indexing into `entities`.
- **A `warning` does not block.** `isCompatible` reflects the workspace-level verdict, so individual entities can report `warning` on a compatible workspace.
- **Messages are always English.** They are resolved through a fixed `en-US` bundle and do not follow the caller's language — use `status`, not `message`.
- **Workspaces can be missing from the report.** A candidate the validator could not evaluate produces no entry. Match by `workspaceId`, never by position.
- **Entity entries carry no `viewType`.** Unlike [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md), and unlike it the data sources here **do** carry `datasourceId`.
- **Dependency chain:** [Get Linkable Workspaces](get-linkable-workspaces.md) → Get Workspace Linking Compatibility → [Link Workspaces](link-workspaces.md).

## Link Workspaces

- **`204` means scheduled.** Compatibility is checked inline; the design push is queued. No sandbox ID exists yet when the response arrives.
- **All-or-nothing.** One incompatible candidate blocks the entire request, and the failure body carries the full report under `data.incompatibleWorkspaces` ([`8247`](../../../foundations/error-codes.md#error-8247)).
- **Already-linked candidates are filtered out before anything else runs.** If that empties the payload the call short-circuits to `204` **without** validating the master or the client organisations — so a `204` is not evidence that the request was well-formed, only that nothing remained to do.
- **Effectively idempotent.** Re-sending a payload whose workspaces are now linked is a silent no-op; there is no duplicate-link error.
- **A workspace cannot be both master and client.** Linking from a workspace that is already somebody's client fails with [`8246`](../../../foundations/error-codes.md#error-8246).
- **The relationship is one-directional.** The master pushes; nothing flows back from the client.
- **Dependency chain:** [Get Linkable Workspaces](get-linkable-workspaces.md) → [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md) → Link Workspaces → [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md).

## Sync Linked Workspaces

- **Half the request may run inline and half may be scheduled.** Per-client `scope: "SELECTED"` entries push their `masterViewIds` during the request; `scope: "ALL"` entries and a top-level `scope: "ALL"` are queued. A mixed request that fails midway can therefore be partially applied.
- **`204` says nothing about the outcome.** Read [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md) afterwards for the entity-level result.
- **The top-level `scope` is case-sensitive, the per-client one is not.** `{"scope":"all"}` is [`8119`](../../../foundations/error-codes.md#error-8119); `clients[].scope: "all"` is accepted. Send upper case everywhere.
- **`ALL` means every link of this master,** resolved from `<workspace-id>` — not every link in the organisation.
- **Views are addressed in the master.** `masterViewIds` are IDs in `<workspace-id>`; client-side IDs are never accepted, and the caller must administer the organisation owning each listed view's workspace.
- **Not idempotent.** Every call pushes again and overwrites client-side drift.
- **Its scope is `modeling.create`,** matching the HTTP method rather than the effect.
- **Dependency chain:** [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md) → `sandboxId` → Sync Linked Workspaces → [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md).

## Get Linked Workspace Sync Details

- **The only entity-level report in the family.** The listing APIs give one `syncStatus` per link; this tells you which table or report failed and why.
- **`pendingEntities.dataSources` is always empty.** Only tables and reports are counted as pending. Do not read it as "no data source changes".
- **Pending work includes deletions.** `hasPendingEntities` turns `true` for created, modified **and** deleted master entities; the `deleted` value of `modifiedStatus` marks the last case.
- **`syncTime` is epoch milliseconds in a string,** `"0"` when the link has never synced — the same representation as the listing APIs, despite what the field name suggests.
- **The entity shape differs from the compatibility API.** Entries here carry `viewType` / `viewTypeId`; data sources here carry **no** `datasourceId`. There it is the other way round.
- **Omit `CONFIG` to ask for everything.** `CONFIG={}` fails the template's required-key check on `sandboxIds`; leaving the parameter off entirely is the supported form.
- **One remote read per sandbox.** Filter with `sandboxIds` on a master with many clients.
- **Dependency chain:** [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md) → `sandboxId` → Get Linked Workspace Sync Details.

## Unlink Workspaces

- **Client workspaces survive.** Only the mapping is removed; the client keeps the last design pushed to it and becomes an ordinary workspace.
- **Validated up front.** Every `sandboxIds` entry is checked before anything is removed, so one bad ID fails the whole call and nothing is unlinked.
- **`ALL` is idempotent; `SELECTED` is not.** Repeating `{"scope":"ALL"}` on a master with no links returns `204`; repeating a `SELECTED` request with the same IDs fails with [`8248`](../../../foundations/error-codes.md#error-8248).
- **Nothing is reported per sandbox.** "Unlinked" and "already gone" look identical from the response.
- **`scope` is case-sensitive here,** unlike the per-client `scope` of [Sync Linked Workspaces](sync-linked-workspaces.md).
- **Relinking starts over.** A new link gets a new sandbox ID and an empty sync history; nothing carries across.
- **Dependency chain:** [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md) → `sandboxId` → Unlink Workspaces.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Three of eight APIs return 204 with no body** | [Link Workspaces](link-workspaces.md), [Sync Linked Workspaces](sync-linked-workspaces.md) and [Unlink Workspaces](unlink-workspaces.md) return HTTP **204 No Content** on success — treat the status code as the success indicator and never expect a JSON body. The other five return the standard `{"status", "summary", "data"}` envelope with HTTP 200. |
| **Nothing is echoed by the write APIs** | None of the three returns the sandbox IDs it created, synced or removed. The authoritative post-write state always comes from a follow-up read. |
| **A `204` means "scheduled", not "done"** | Both write APIs that push design hand the work to a scheduler. Confirm with [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md) or [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md). |
| **Failure responses always carry a body** | Even for the 204 APIs, errors return `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. On failure `summary` is the error's **symbolic name** (e.g. `SANDBOX_NOT_MAPPED_TO_MASTER_WORKSPACE`), not a localised sentence. |
| **One error carries extra data** | `8247` `LINK_WORKSPACES_INCOMPATIBLE_WORKSPACES` adds `data.incompatibleWorkspaces` — the full compatibility report for the blocking workspaces, in the shape of `data.clients` from [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md). Read it instead of re-running the check. |
| **`summary` on success is a localised label** | `"Get linked workspaces for organization"`, `"Get linkable workspaces"`, … It changes with the caller's language, so never branch on it. |
| **All IDs come back as strings** | `workspaceId`, `orgId`, `sandboxId`, `viewId`, `datasourceId` and `syncedByZuId` are JSON **strings** even though the values are numeric. Parse them as strings or longs — never as native JSON numbers — to avoid precision loss. |
| **Request-side typing is not uniform** | The scalar IDs `clients[].orgId` and `clients[].sandboxId` are declared as **Long** and are sent unquoted; the array entries `workspaceIds`, `sandboxIds` and `masterViewIds` are declared as text and are sent as **quoted strings**. Follow the samples rather than assuming one convention for the whole payload. |
| **Two fields are genuine JSON types other than String** | `hasPendingEntities` and `isCompatible` are native booleans; `viewTypeId` is a native number. Everything else in these payloads is a string, an array or an object. |
| **`null` is used deliberately in compatibility responses** | `workspaces[].error` is `null` when the workspace is compatible, and `workspaces[].entities` is `null` when it was blocked for a workspace-level reason. Elsewhere in this family absent data is an empty array or an empty string, not `null`. |
| **Timestamps are epoch milliseconds as strings** | `lastSync.syncTime` is `"1779226560981"`-style in **both** the listing APIs and [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md), and `"0"` when the link has never synced. No API here returns a formatted date. |
| **The container type of `linkedWorkspaces` changes between two APIs** | An array in [Get Linked Workspaces For Organization](get-linked-workspaces-for-organization.md), a single object in [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md), and `{}` when the master has no visible links. |
| **Three different keys hold the same idea** | The candidate catalogue is `data.orgs`, the compatibility report is `data.clients`, and the sync report is `data.workspaces`. They are not interchangeable and their element shapes differ. |
| **Arrays that are always present** | `data.linkedWorkspaces`, `data.orgs`, `data.clients`, `data.workspaces`, and within them `lastSync.entities.{dataSources,tables,views}` and `pendingEntities.{dataSources,tables,views}` — empty when there is nothing to report. |
| **An empty collection is a success** | An empty `linkedWorkspaces`, `orgs` or `workspaces` array comes back with HTTP 200. Never infer failure from emptiness, and never infer "not linked" from an empty listing without knowing the caller administers every organisation involved. |
| **Per-entity `message` values are always English** | They are resolved through a fixed `en-US` bundle regardless of the caller's locale. Switch on `status`, never on `message`. |
| **No pagination anywhere** | None of the eight APIs accepts `pageNo`, a keyword or a sort parameter. Every result set is returned whole. |
| **Responses are extensible** | Some builds return additional fields. Ignore unrecognised keys rather than validating against a closed schema. |
| **`8246`–`8251` are linked-workspace specific** | Every code in that range is raised only by this family. The `7xxx` and other `8xxx` codes are shared across API families, so match on the `summary` symbolic name as well as `errorCode` when handling errors generically. |

---

# Enum and Value Reference

### `scope` Values

Used by [Sync Linked Workspaces](sync-linked-workspaces.md) (top level and per client) and [Unlink Workspaces](unlink-workspaces.md).

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `ALL` | Operate on everything the server resolves for the master: every linked sandbox, or every eligible entity within one sandbox. | The enumeration attribute that pairs with `SELECTED` must be **omitted**. |
| `SELECTED` | Operate only on what the request enumerates. | The paired attribute (`sandboxIds`, `clients` or `masterViewIds`) is **mandatory** and must be non-empty. |

Case handling differs by position: the **top-level** `scope` on both APIs is compared verbatim and must be upper case ([`8119`](../../../foundations/error-codes.md#error-8119) otherwise), while `clients[].scope` on [Sync Linked Workspaces](sync-linked-workspaces.md) is upper-cased before comparison. See [The `scope` Attribute](overview.md#the-scope-attribute).

### Sync Status Values

`lastSync.syncStatus`, returned by [Get Linked Workspaces For Organization](get-linked-workspaces-for-organization.md), [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md) and [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md).

| Value | Meaning |
|-------|---------|
| `success` | The last sync completed without errors. |
| `failure` | The last sync failed. |
| `partialSuccess` | Some entities synced and some did not. The per-entity detail is in [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md). |
| `inProgress` | A sync is currently running. Also what a link reports before its first sync has finished. |
| `unknown` | The stored status code was not one of the four above. |

### Entity Status Values

`status` on every `dataSources[]`, `tables[]` and `views[]` entry, in both the compatibility and the sync-details responses. Distinct from the response-envelope `status` and from `syncStatus`.

| Value | Meaning |
|-------|---------|
| `success` | The entity is compatible, or synced cleanly. |
| `warning` | The entity needs attention — typically it will be overwritten — but does not block the operation. |
| `failure` | The entity conflicts, or did not sync. |

### Modified Status Values

`modifiedStatus` on `pendingEntities.tables[]` and `pendingEntities.views[]` in [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md).

| Value | Meaning |
|-------|---------|
| `created` | The entity does not exist on the client yet and will be created by the next sync. |
| `updated` | The entity exists on the client and will be overwritten by the next sync. |
| `deleted` | The entity was removed from the master and the mapping on the client will be removed by the next sync. |

### View Type Reference

`viewType` and `viewTypeId` appear on `lastSync.entities.tables[]`, `lastSync.entities.views[]`, `pendingEntities.tables[]` and `pendingEntities.views[]` of [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md). `viewType` is the display name and `viewTypeId` the numeric id.

| `viewTypeId` | `viewType` |
|---|---|
| `0` | `Table` |
| `1` | `Tabular View` |
| `2` | `Chart View` |
| `3` | `Pivot View` |
| `4` | `Summary View` |
| `5` | `Table View` |
| `6` | `Query Table` |
| `7` | `Dashboard` |
| `8` | `WIDGET` |
| `9` | `Tab` |
| `10` | `Map Chart` |
| `11` | `Slide Show` |
| `12` | `MultiChart` |
| `13` | `Pipeline Table` |
| `14` | `Data Model Object` |

An id outside `0`–`14` is returned in `viewType` as the **raw number rendered as a string**, with `viewTypeId` carrying the same value as a number. Entities are split between the `tables` and `views` arrays by whether `viewTypeId` is `0`; everything else lands in `views`.

---

# CONFIG Attribute Availability by API

Only five APIs accept CONFIG. `✔` means the attribute is accepted; `—` means it is not part of that API's contract.

| Attribute | [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md) | [Link Workspaces](link-workspaces.md) | [Sync Linked Workspaces](sync-linked-workspaces.md) | [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md) | [Unlink Workspaces](unlink-workspaces.md) |
|-----------|---|---|---|---|---|
| `clients` | **Yes** | **Yes** | Conditional | — | — |
| `clients[].orgId` | **Yes** | **Yes** | — | — | — |
| `clients[].workspaceIds` | **Yes** | **Yes** | — | — | — |
| `clients[].sandboxId` | — | — | **Yes** | — | — |
| `clients[].scope` | — | — | **Yes** | — | — |
| `clients[].masterViewIds` | — | — | Conditional | — | — |
| `scope` | — | — | **Yes** | — | **Yes** |
| `sandboxIds` | — | — | — | **Yes**\* | Conditional |
| **CONFIG itself** | Mandatory | Mandatory | Mandatory | Optional | Mandatory |
| **Where CONFIG travels** | Query string | Form body | Form body | Query string | Form body |

\* `sandboxIds` is optional in effect — omit `CONFIG` entirely to fetch every linked sandbox — but it is a required key **within** `CONFIG`, so `CONFIG={}` is rejected.

`clients` carries different members depending on the API: `orgId` + `workspaceIds` for [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md) and [Link Workspaces](link-workspaces.md), `sandboxId` + `scope` + `masterViewIds` for [Sync Linked Workspaces](sync-linked-workspaces.md). The two shapes are not interchangeable.

[Get Linked Workspaces For Organization](get-linked-workspaces-for-organization.md), [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md) and [Get Linkable Workspaces](get-linkable-workspaces.md) take no CONFIG at all.

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7387](../../../foundations/error-codes.md#error-7387) | 400 | DBID_NOT_BELONGS_TO_ZSOID - The workspace does not belong to the organisation in ZANALYTICS-ORGID. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | DOMAIN_NOT_EXIST - The custom domain in the request host is not provisioned. |
| [8077](../../../foundations/error-codes.md#error-8077) | 400 | EMPTY_JSON_CONFIGURATION - CONFIG is present but empty. |
| [8078](../../../foundations/error-codes.md#error-8078) | 400 | EMPTYJSONATTRIBUTEFOUND — A mandatory attribute was sent blank. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION - scope is missing from CONFIG. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | CONFIG is not valid JSON, was not URL-encoded correctly, contains an unsupported key, or violates a type or length constraint. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | The ZANALYTICS-ORGID header is missing from a request that requires it. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | INVALIDVALUEFORATTRIBUTE — fileType, onError, delimiter, quoted, thousandSeparator, or decimalSeparator is outside its permitted set. |
| [8246](../../../foundations/error-codes.md#error-8246) | 400 | INVALID_MASTER_WORKSPACE_MAPPING - <workspace-id> is itself linked as a client of another master. |
| [8247](../../../foundations/error-codes.md#error-8247) | 400 | LINK_WORKSPACES_INCOMPATIBLE_WORKSPACES - At least one candidate failed the compatibility check. Nothing was linked. |
| [8248](../../../foundations/error-codes.md#error-8248) | 400 | SANDBOX_NOT_MAPPED_TO_MASTER_WORKSPACE - One or more sandboxIds are not linked to this master. The message names them. |
| [8249](../../../foundations/error-codes.md#error-8249) | 400 | INVALID_CONFIGURATION_REMOVE_LINKED_WORKSPACES - sandboxIds was supplied with scope: "ALL", or omitted with scope: "SELECTED". |
| [8250](../../../foundations/error-codes.md#error-8250) | 400 | INVALID_UF_COMP_TYPE - compType is not valid for the column category or operation. |
| [8251](../../../foundations/error-codes.md#error-8251) | 400 | INCORRECT_DATE_VALUE - A date in a date-range static filter could not be parsed. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | LESSTHANMINOCCURANCE — CONFIG was not sent. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |

# Related

- [Workspace Management](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
