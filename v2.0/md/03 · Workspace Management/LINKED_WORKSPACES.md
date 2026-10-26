# Zoho Analytics V2 REST API — Linked Workspaces

This document covers the V2 **Linked Workspace** REST APIs of Zoho Analytics — the APIs that discover which workspaces can be linked to a master, check them for compatibility, link and unlink them, push the master's design down to them, and report what each push did.

## What is a "Linked Workspace" in Zoho Analytics?

Workspace linking lets one **master** workspace act as the design source for any number of **client** workspaces, which may live in other organisations. The master holds the canonical tables, reports and dashboards; a **sync** copies that design into every client. Each master↔client pair is tracked by a **sandbox ID**, and that sandbox ID — not the client workspace ID — is the handle every downstream operation uses.

| Part | CONFIG attribute(s) | Notes |
|------|--------------------|-------|
| **What is the source** | `<workspace-id>` in the URL | Always the **master** workspace. It cannot itself be a client of another master (`8246`). There is no CONFIG attribute for it. |
| **What gets linked** | `clients[].orgId`, `clients[].workspaceIds` | Candidate client workspaces, grouped by the organisation that owns them. The caller must be an admin of every organisation named. |
| **What is pushed** | `scope`, `clients[].scope`, `clients[].masterViewIds` | A sync either pushes everything or a named list of master-workspace views, per client. |
| **What identifies a link** | `sandboxId`, `sandboxIds` | The mapping ID minted when a link is created. Unlink and sync-filter operations address links by this value — see [The Master, the Client and the Sandbox ID](#the-master-the-client-and-the-sandbox-id). |

> **The single most important behaviour:** [Link Workspaces](#5-link-workspaces) and [Sync Linked Workspaces](#6-sync-linked-workspaces) return `204` when the work has been **scheduled**, not when it has finished. Nothing in the response tells you what was linked or pushed — read it back with [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details).

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`). The five read APIs use the **`metadata`** scope family; the three write APIs use the **`modeling`** scope family — see [Appendix B](#appendix-b--oauth-scope-summary).
> - All eight APIs require the `ZANALYTICS-ORGID` header, which names the organisation that owns the **master** workspace. A missing header is `8083`.
> - `ZohoAnalytics_Server_URI` depends on the data centre (`analyticsapi.zoho.com`, `.eu`, `.in`, `.com.au`, `.jp`, …).
> - **All eight APIs are disabled in Client Portal / White Label request contexts.** A request that arrives through a custom domain is rejected with `7301` before any business logic runs — see [White Label / Client Portal Behaviour](#white-label--client-portal-behaviour).
> - **All eight APIs are organisation-admin only.** The caller must be an Account Admin or an Organization Admin — of the master's organisation, and of every client organisation the request touches. There is no per-workspace permission that grants access here.
> - Seven of the eight are **master-scoped** (`/workspaces/<workspace-id>/linkedworkspaces...`); only [Get Linked Workspaces For Organization](#1-get-linked-workspaces-for-organization) is organisation-scoped.
> - None of these APIs accepts a `criteria` attribute, and none of them reads or writes table rows — no API here uses the `data` scope family.

---

## Index

| # | API Name | Method | URL |
|---|----------|--------|-----|
| 1 | [Get Linked Workspaces For Organization](#1-get-linked-workspaces-for-organization) | GET | `/restapi/v2/linkedworkspaces` |
| 2 | [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace) | GET | `/restapi/v2/workspaces/<workspace-id>/linkedworkspaces` |
| 3 | [Get Linkable Workspaces](#3-get-linkable-workspaces) | GET | `/restapi/v2/workspaces/<workspace-id>/linkedworkspaces/linkable` |
| 4 | [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility) | GET | `/restapi/v2/workspaces/<workspace-id>/linkedworkspaces/compatibility` |
| 5 | [Link Workspaces](#5-link-workspaces) | POST | `/restapi/v2/workspaces/<workspace-id>/linkedworkspaces` |
| 6 | [Sync Linked Workspaces](#6-sync-linked-workspaces) | POST | `/restapi/v2/workspaces/<workspace-id>/linkedworkspaces/sync` |
| 7 | [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details) | GET | `/restapi/v2/workspaces/<workspace-id>/linkedworkspaces/sync` |
| 8 | [Unlink Workspaces](#8-unlink-workspaces) | DELETE | `/restapi/v2/workspaces/<workspace-id>/linkedworkspaces` |

> **Note on method overloading:** two paths serve two operations each. `/workspaces/<workspace-id>/linkedworkspaces` lists links on `GET`, creates them on `POST` and removes them on `DELETE`; `/workspaces/<workspace-id>/linkedworkspaces/sync` reports sync state on `GET` and triggers a real sync on `POST`. Sending `POST` where you meant `GET` pushes the master's design into live client workspaces.
>
> **Note on `DELETE` with a body:** [Unlink Workspaces](#8-unlink-workspaces) is a `DELETE` that carries a mandatory `CONFIG` form body. Some HTTP clients strip bodies from `DELETE` requests; verify yours does not.
>
> **Note on naming:** these are the operation names the server itself uses in its response summaries. Earlier drafts shortened two of them to "Get Linked Workspaces For Org" and "Get Linked Workspaces For Master"; the full forms above are canonical.

---

## The Master, the Client and the Sandbox ID

Three identifiers circulate through these APIs and they are not interchangeable.

| Identifier | Where it comes from | What addresses it |
|---|---|---|
| **Master workspace ID** | Any workspace you own, via [Get All Workspace List](WORKSPACE_OPERATIONS.md#6-get-all-workspace-list) | The `<workspace-id>` path segment of seven of the eight APIs. |
| **Client workspace ID** | [Get Linkable Workspaces](#3-get-linkable-workspaces) | `clients[].workspaceIds` on [Link Workspaces](#5-link-workspaces) and [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility). **Nothing else accepts it.** |
| **Sandbox ID** | Minted by [Link Workspaces](#5-link-workspaces); read back from `clients[].workspaces[].sandboxId` of [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace) | `sandboxIds` on [Unlink Workspaces](#8-unlink-workspaces) and [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details); `clients[].sandboxId` on [Sync Linked Workspaces](#6-sync-linked-workspaces). |

The rule the server applies is: **you link by client workspace ID, and you operate on the link by sandbox ID.** Practical consequences:

1. **The sandbox ID is not returned by the call that creates it.** [Link Workspaces](#5-link-workspaces) answers `204` with no body. The only way to learn the new sandbox IDs is to call [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace) afterwards — and because linking is scheduled rather than immediate, they may not be there on the first attempt.
2. **Passing a client workspace ID where a sandbox ID is expected fails with `8248`,** not with a type error. The two id spaces look alike.
3. **A master cannot be a client.** If `<workspace-id>` is already linked as somebody's client, [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility), [Link Workspaces](#5-link-workspaces) and [Sync Linked Workspaces](#6-sync-linked-workspaces) all fail with `8246`.
4. **Links whose master or client workspace has been deleted are purged on read.** The two listing APIs delete the stale mapping rows as a side effect, so a sandbox ID that worked yesterday can be gone today with no write having been issued.

---

## The `scope` Attribute

Three APIs take a `scope` attribute, and it means the same thing each time: **`ALL` operates on everything the server can resolve; `SELECTED` requires you to enumerate the targets.** The pairing is strict — supplying the enumeration with `ALL`, or omitting it with `SELECTED`, is rejected rather than ignored.

| API | `scope` | Must be accompanied by | Must omit | Error if wrong |
|---|---|---|---|---|
| [Unlink Workspaces](#8-unlink-workspaces) | `ALL` | — | `sandboxIds` | `8249` |
| [Unlink Workspaces](#8-unlink-workspaces) | `SELECTED` | `sandboxIds` (non-empty) | — | `8249` |
| [Sync Linked Workspaces](#6-sync-linked-workspaces) top level | `ALL` | — | `clients` | `8250` |
| [Sync Linked Workspaces](#6-sync-linked-workspaces) top level | `SELECTED` | `clients` (non-empty) | — | `8250` |
| [Sync Linked Workspaces](#6-sync-linked-workspaces) per client | `ALL` | — | `masterViewIds` | `8251` |
| [Sync Linked Workspaces](#6-sync-linked-workspaces) per client | `SELECTED` | `masterViewIds` (non-empty) | — | `8251` |

> **The top-level `scope` is case-sensitive; the per-client `scope` is not.** `clients[].scope` is upper-cased before it is compared, so `"all"` and `"All"` are accepted there. The top-level `scope` on [Unlink Workspaces](#8-unlink-workspaces) and [Sync Linked Workspaces](#6-sync-linked-workspaces) is compared verbatim — `"all"` fails with `8119`, naming `ALL, SELECTED` as the permitted values. Send upper case everywhere and the inconsistency never bites.

---

## Limitations

These are the limits that apply with **default settings**.

| Limitation | Value | Enforced by |
|------------|-------|-------------|
| **Client organisations per request** | **1–100** entries in `clients`. | Request template |
| **Client workspaces per organisation entry** | **1–100** entries in `clients[].workspaceIds`. | Request template |
| **`sandboxIds` per request** | **1–100** entries. | Request template |
| **`masterViewIds` per client entry** | **1–1000** entries. | Request template |
| **CONFIG size — [Link Workspaces](#5-link-workspaces) / [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility)** | **500,000** characters. | Request template |
| **CONFIG size — [Sync Linked Workspaces](#6-sync-linked-workspaces)** | **5,000,000** characters. | Request template |
| **CONFIG size — [Unlink Workspaces](#8-unlink-workspaces) / [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details)** | **5,000** characters. | Request template |
| **Masters per organisation listing** | Keyed by master workspace **name**, not ID. | — |
| **Pagination, filtering, sorting** | **None on any API here.** Every result set is returned whole. | — |

> **The organisation listing is keyed by master workspace name.** [Get Linked Workspaces For Organization](#1-get-linked-workspaces-for-organization) groups its results by the master's display name, so two masters in the same organisation sharing a name collapse into a single entry whose `clients` array holds both sets. Workspace names are unique within an organisation in normal use, but if you have renamed workspaces across organisations, prefer the per-master listing.

---

## Permission Model

| Role | May do | Notes |
|------|--------|-------|
| Account Admin / Organization Admin of the master's organisation | Every API in this document, for masters in that organisation. | The only role that qualifies. |
| Account Admin / Organization Admin of a **client** organisation as well | Additionally link, validate and list workspaces belonging to that client organisation. | Checked per organisation named in `clients[].orgId`. |
| Workspace Admin, custom-role user, shared user | Nothing. | `7301`. |

Two consequences worth stating plainly:

- **Cross-organisation linking needs admin rights on both sides.** [Link Workspaces](#5-link-workspaces) and [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility) re-check `isOrgAdminOrSuperAdmin` for every `clients[].orgId` in the payload, so an Account Admin of the master organisation alone cannot pull in a workspace from an organisation they do not administer.
- **The listing APIs filter rather than fail.** Links whose master or client organisation the caller does not administer are **silently omitted** from [Get Linked Workspaces For Organization](#1-get-linked-workspaces-for-organization) and [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace). An incomplete list is not an error, so never treat "absent" as "not linked" unless you know the caller administers every organisation involved.

---

## White Label / Client Portal Behaviour

All eight APIs are blocked in Client Portal / White Label request contexts — the same posture as the [Email Schedule APIs](../09%20%C2%B7%20Schedules%20%26%20Alerts/EMAIL_SCHEDULES.md#white-label--client-portal-behaviour).

| Scenario | Result |
|----------|--------|
| The request arrives **through** a Client Portal / White Label custom domain | **Rejected with `7301`** before any business logic runs. |
| The request is sent to the **standard** API host for a workspace that happens to be white-labelled | **Allowed**, and behaves exactly as for any other workspace. |

There is no `domainName` CONFIG attribute on any of these APIs. Manage linked workspaces for a white-labelled organisation by calling the standard `analyticsapi.zoho.*` host.

---

## 1. Get Linked Workspaces For Organization

Returns every master↔client link in the organisation named by `ZANALYTICS-ORGID`, grouped one entry per master workspace. This is the broadest discovery call, and the usual way to find a `sandboxId`.

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/linkedworkspaces` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID whose master workspaces are listed. |
| **Permission Required** | The authenticated user must be an Account Admin or an Organization Admin of the organisation in `ZANALYTICS-ORGID`. Individual links are additionally filtered to those whose master **and** client organisations the caller administers. |

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

### Sample Requests

**Case 1 — List every link in the organisation**

```http
GET /restapi/v2/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
GET /restapi/v2/linkedworkspaces HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

### Sample Responses

**HTTP 200 OK — One master with two clients in a single client organisation**

```json
{
    "status": "success",
    "summary": "Get linked workspaces for organization",
    "data": {
        "linkedWorkspaces": [
            {
                "master": {
                    "workspaceId": "137687000271334001",
                    "workspaceName": "ISV Master Analytics",
                    "orgId": "700000123456",
                    "orgName": "Zylker Analytics"
                },
                "clients": [
                    {
                        "orgId": "700000654321",
                        "orgName": "Northwind Retail",
                        "workspaces": [
                            {
                                "workspaceId": "466206000000071000",
                                "workspaceName": "Northwind Sandbox",
                                "sandboxId": "137687000012345001",
                                "lastSync": {
                                    "syncTime": "1779226560981",
                                    "syncStatus": "success",
                                    "syncedBy": "jane.doe@example.com",
                                    "syncedByName": "Jane Doe",
                                    "syncedByZuId": "60002000000000123"
                                },
                                "hasPendingEntities": false
                            },
                            {
                                "workspaceId": "466206000000071010",
                                "workspaceName": "Northwind EU Sandbox",
                                "sandboxId": "137687000012345002",
                                "lastSync": {
                                    "syncTime": "1779140160981",
                                    "syncStatus": "partialSuccess",
                                    "syncedBy": "john.roe@example.com",
                                    "syncedByName": "John Roe",
                                    "syncedByZuId": "60002000000000456"
                                },
                                "hasPendingEntities": true
                            }
                        ]
                    }
                ]
            }
        ]
    }
}
```

**HTTP 200 OK — Organisation with no linked workspaces**

```json
{
    "status": "success",
    "summary": "Get linked workspaces for organization",
    "data": {
        "linkedWorkspaces": []
    }
}
```

**HTTP 403 Forbidden — Failure paired with Case 2**

```json
{
    "status": "failure",
    "summary": "SECURITY_NOT_PERMITTED",
    "data": {
        "errorCode": 7301,
        "errorMessage": "You (WL_DBAdmin) do not have the permission to do this operation. "
    }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary — `"Get linked workspaces for organization"` for this API. Never branch on it. |
| `data` | JSONObject | Response payload wrapper. |
| `data.linkedWorkspaces` | JSONArray | One entry per master workspace that has at least one live link. **Always present**; `[]` when the organisation has no links, or when every link was filtered out by the permission check. A master with no clients never appears. |
| `linkedWorkspaces[].master` | JSONObject | The master workspace of this group. **Always present.** |
| `master.workspaceId` | String | Master workspace ID, serialised as a **string**. |
| `master.workspaceName` | String | Master workspace display name. This is also the grouping key — see [Limitations](#limitations). |
| `master.orgId` | String | Organisation ID that owns the master. |
| `master.orgName` | String | Organisation display name. On an on-premise build this is the calling user's full name rather than an organisation name. |
| `linkedWorkspaces[].clients` | JSONArray | The master's clients, grouped by client organisation, in the order the links were read. **Always present** and never empty within an entry. |
| `clients[].orgId` | String | Client organisation ID. |
| `clients[].orgName` | String | Client organisation display name. |
| `clients[].workspaces` | JSONArray | The linked client workspaces inside that organisation. |
| `workspaces[].workspaceId` | String | Client workspace ID. |
| `workspaces[].workspaceName` | String | Client workspace display name. |
| `workspaces[].sandboxId` | String | **The link's identifier.** Use it for [Unlink Workspaces](#8-unlink-workspaces), [Sync Linked Workspaces](#6-sync-linked-workspaces) and [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details). |
| `workspaces[].lastSync` | JSONObject | Summary of the most recent successful sync. **Always present**, with empty-ish members when the link has never synced. |
| `lastSync.syncTime` | String | Time of the last successful sync as **epoch milliseconds in a string** (`"1779226560981"`). `"0"` when the link has never synced. Not a formatted date. |
| `lastSync.syncStatus` | String | Outcome of the last sync as a stable enum — `success`, `failure`, `partialSuccess`, `inProgress` or `unknown`. See [Sync Status Values](#sync-status-values). |
| `lastSync.syncedBy` | String | E-mail address of the user who ran that sync. |
| `lastSync.syncedByName` | String | Display name of that user. |
| `lastSync.syncedByZuId` | String | ZUID of that user, serialised as a string. |
| `workspaces[].hasPendingEntities` | Boolean | `true` when the master has entities created, modified or deleted since the last successful sync to this client. Native JSON boolean. The detail behind it is in [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details). |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Scoped to the header organisation** | Only masters owned by the organisation in `ZANALYTICS-ORGID` are listed. To see another organisation's masters, repeat the call with its ID in the header. |
| **Results are filtered, not refused** | A link whose master or client organisation the caller does not administer is silently dropped from the response. An empty array can therefore mean "no links" or "none you may see". |
| **Reading has a housekeeping side effect** | Mappings whose master or client workspace is no longer active are **deleted** while the response is being built. A `GET` here can permanently remove dangling links — benign, but it means the same call can return fewer entries the second time. |
| **Grouped by master workspace name** | The grouping key is the display name, not the ID. See [Limitations](#limitations). |
| **No paging, filtering or sorting** | The whole set comes back in one response; there is no `pageNo`, keyword or status filter anywhere in this family. |
| **Empty result is a success** | An organisation with no links returns `200` with `"linkedWorkspaces": []`, not an error. |
| **Ids are strings** | Parse `workspaceId`, `orgId`, `sandboxId` and `syncedByZuId` as strings or 64-bit longs. A 32-bit integer type loses precision. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get Org List](../01%20%C2%B7%20Organization%20Management/ORG_INFO_AND_SETTINGS.md#1-get-org-list) → `ZANALYTICS-ORGID` → Get Linked Workspaces For Organization → `sandboxId` for the sync and unlink APIs. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin of the organisation in `ZANALYTICS-ORGID`, or the request arrived through a Client Portal / White Label domain. | Authenticate as an organisation administrator and call from the standard API host. |
| 8060 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use the standard API host. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

---

## 2. Get Linked Workspaces For Master Workspace

Returns the links of a single master workspace, in the same shape as one entry of [Get Linked Workspaces For Organization](#1-get-linked-workspaces-for-organization) — but as a **single object**, not an array.

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/linkedworkspaces` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the master workspace. |
| **Permission Required** | The authenticated user must be an Account Admin or an Organization Admin of the organisation in `ZANALYTICS-ORGID` **and** of the organisation that owns `<workspace-id>`. Individual client entries are further filtered to organisations the caller administers. |

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

### Sample Requests

**Case 1 — A master with links**

```http
GET /restapi/v2/workspaces/137687000271334001/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — A workspace that has never been linked**

```http
GET /restapi/v2/workspaces/466206000000071000/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Sample Responses

**HTTP 200 OK — Two client workspaces across two client organisations**

```json
{
    "status": "success",
    "summary": "Get linked workspaces for master workspace",
    "data": {
        "linkedWorkspaces": {
            "master": {
                "workspaceId": "137687000271334001",
                "workspaceName": "ISV Master Analytics",
                "orgId": "700000123456",
                "orgName": "Zylker Analytics"
            },
            "clients": [
                {
                    "orgId": "700000654321",
                    "orgName": "Northwind Retail",
                    "workspaces": [
                        {
                            "workspaceId": "466206000000071000",
                            "workspaceName": "Northwind Sandbox",
                            "sandboxId": "137687000012345001",
                            "lastSync": {
                                "syncTime": "1779226560981",
                                "syncStatus": "partialSuccess",
                                "syncedBy": "jane.doe@example.com",
                                "syncedByName": "Jane Doe",
                                "syncedByZuId": "60002000000000123"
                            },
                            "hasPendingEntities": true
                        }
                    ]
                },
                {
                    "orgId": "700000999999",
                    "orgName": "Contoso Distribution",
                    "workspaces": [
                        {
                            "workspaceId": "466206000000081010",
                            "workspaceName": "Contoso Sandbox",
                            "sandboxId": "137687000012345003",
                            "lastSync": {
                                "syncTime": "0",
                                "syncStatus": "inProgress",
                                "syncedBy": "john.roe@example.com",
                                "syncedByName": "John Roe",
                                "syncedByZuId": "60002000000000456"
                            },
                            "hasPendingEntities": true
                        }
                    ]
                }
            ]
        }
    }
}
```

**HTTP 200 OK — Failure paired with Case 2: the workspace has no links**

```json
{
    "status": "success",
    "summary": "Get linked workspaces for master workspace",
    "data": {
        "linkedWorkspaces": {}
    }
}
```

**HTTP 403 Forbidden — Caller does not administer the master's organisation**

```json
{
    "status": "failure",
    "summary": "SECURITY_NOT_PERMITTED",
    "data": {
        "errorCode": 7301,
        "errorMessage": "You (Jane Doe) do not have the permission to do this operation. "
    }
}
```

### Response Fields

The `master` / `clients` structure is identical to one element of `data.linkedWorkspaces` in [Get Linked Workspaces For Organization](#1-get-linked-workspaces-for-organization) — refer there for every nested field. The differences are:

| Field | Type | Description |
|-------|------|--------------|
| `summary` | String | `"Get linked workspaces for master workspace"` for this API. |
| `data.linkedWorkspaces` | JSONObject | A **single object**, not an array. **Always present**, but an **empty object `{}`** when the master has no links the caller may see. Test for the presence of `master` rather than for an empty array. |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **The container type differs from the organisation listing** | `data.linkedWorkspaces` is a JSON **object** here and a JSON **array** in [Get Linked Workspaces For Organization](#1-get-linked-workspaces-for-organization). A client that shares a parser between the two must branch on the shape. |
| **"No links" is `{}`, not an error** | An unlinked workspace, a workspace whose links were all filtered out by the permission check, and a workspace that is not a master at all are indistinguishable — all three return `{}` with HTTP 200. This API does **not** raise `8246` for a non-master. |
| **Results are filtered, not refused** | Client entries in organisations the caller does not administer are silently dropped, exactly as in the organisation listing. |
| **Reading has a housekeeping side effect** | Mappings pointing at deleted workspaces are purged while the response is built. |
| **`syncTime` is epoch milliseconds** | A string of digits, `"0"` when the link has never synced successfully. |
| **No paging, filtering or sorting** | The whole set comes back in one response. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get All Workspace List](WORKSPACE_OPERATIONS.md#6-get-all-workspace-list) → `<workspace-id>` → Get Linked Workspaces For Master Workspace → `clients[].workspaces[].sandboxId`. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7103 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not an organisation administrator of the header organisation or of the master's organisation, or the request arrived through a Client Portal / White Label domain. | Authenticate as an organisation administrator and call from the standard API host. |
| 8060 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use the standard API host. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

---

## 3. Get Linkable Workspaces

Returns, grouped by organisation, the workspaces the caller may offer as link candidates for a given master. **This is the only source of the `workspaceIds` that [Link Workspaces](#5-link-workspaces) accepts.**

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/linkedworkspaces/linkable` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the master workspace. |
| **Permission Required** | The authenticated user must be an Account Admin or an Organization Admin of the organisation in `ZANALYTICS-ORGID` **and** of the organisation that owns `<workspace-id>`. Candidates are drawn only from organisations the caller administers. |

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

### Sample Requests

**Case 1 — Discover candidates for a master**

```http
GET /restapi/v2/workspaces/137687000271334001/linkedworkspaces/linkable HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Discover candidates for a second master in the same organisation**

```http
GET /restapi/v2/workspaces/137687000271334009/linkedworkspaces/linkable HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Sample Responses

**HTTP 200 OK — Candidates in two organisations**

```json
{
    "status": "success",
    "summary": "Get linkable workspaces",
    "data": {
        "orgs": [
            {
                "orgId": "700000654321",
                "orgName": "Northwind Retail",
                "workspaces": [
                    {
                        "workspaceName": "Northwind Sandbox",
                        "workspaceId": "466206000000071000"
                    },
                    {
                        "workspaceName": "Northwind EU Sandbox",
                        "workspaceId": "466206000000071010"
                    }
                ]
            },
            {
                "orgId": "700000999999",
                "orgName": "Contoso Distribution",
                "workspaces": [
                    {
                        "workspaceName": "Contoso Sandbox",
                        "workspaceId": "466206000000081010"
                    }
                ]
            }
        ]
    }
}
```

**HTTP 200 OK — No candidates available**

```json
{
    "status": "success",
    "summary": "Get linkable workspaces",
    "data": {
        "orgs": []
    }
}
```

**HTTP 403 Forbidden — Caller does not administer the master's organisation**

```json
{
    "status": "failure",
    "summary": "SECURITY_NOT_PERMITTED",
    "data": {
        "errorCode": 7301,
        "errorMessage": "You (Jane Doe) do not have the permission to do this operation. "
    }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | `"Get linkable workspaces"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.orgs` | JSONArray | Candidate workspaces grouped by organisation. **Always present**; `[]` when nothing can be linked. Note the key is `orgs`, not `clients` — the compatibility and linking APIs use `clients`. |
| `orgs[].orgId` | String | Organisation ID. **Empty string** on the rare grouping where the server could not resolve an ID and returned the organisation name as the grouping key instead; `orgName` then carries that key. |
| `orgs[].orgName` | String | Organisation display name. |
| `orgs[].workspaces` | JSONArray | Workspaces inside that organisation that may be offered as link candidates. May be empty for an organisation that has none. |
| `workspaces[].workspaceId` | String | Workspace ID. This is what goes into `clients[].workspaceIds` of [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility) and [Link Workspaces](#5-link-workspaces). |
| `workspaces[].workspaceName` | String | Workspace display name, for a user-facing picker. |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **The only source of link candidates** | `clients[].workspaceIds` is not validated against any other catalogue, so a workspace absent from this list may still be accepted by the write APIs and then fail compatibility. Drive the picker from here. |
| **"Linkable" means eligible, not compatible** | This API applies structural eligibility only: a workspace already acting as a client or a master, or already scheduled to be linked, is excluded. Whether its design actually fits the master is a separate question answered by [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility). |
| **The response key is `orgs`, the request key is `clients`** | You read `data.orgs[].workspaces[].workspaceId` and write `clients[].workspaceIds`. The two shapes do not mirror each other; map the fields explicitly. |
| **Candidates span organisations** | Every organisation the caller administers is searched, not just the master's own. This is what makes cross-organisation linking possible. |
| **`orgId` can be an empty string** | When the underlying grouping key is an organisation name rather than an ID, `orgId` is `""` and `orgName` holds the key. Such an entry cannot be used in `clients[].orgId`; skip it. |
| **Empty result is a success** | `"orgs": []` means nothing is eligible — commonly because every candidate is already linked. |
| **No paging, filtering or sorting** | The whole candidate set comes back in one response. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get All Workspace List](WORKSPACE_OPERATIONS.md#6-get-all-workspace-list) → `<workspace-id>` → Get Linkable Workspaces → `orgs[].orgId` + `workspaces[].workspaceId` → [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility). |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7103 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not an organisation administrator of the header organisation or of the master's organisation, or the request arrived through a Client Portal / White Label domain. | Authenticate as an organisation administrator and call from the standard API host. |
| 8060 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use the standard API host. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

---

## 4. Get Workspace Linking Compatibility

Runs the full linking validation against a set of candidate client workspaces **without linking anything**, and returns a per-workspace verdict with the conflicting entities broken out. [Link Workspaces](#5-link-workspaces) runs exactly this check internally and refuses the whole request if any candidate fails, so calling this first is how you avoid an all-or-nothing rejection.

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/linkedworkspaces/compatibility` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the master workspace. |
| **Permission Required** | The authenticated user must be an Account Admin or an Organization Admin of the organisation in `ZANALYTICS-ORGID`, of the organisation that owns `<workspace-id>`, **and of every organisation named in `clients[].orgId`**. |

### CONFIG Parameters

CONFIG is **mandatory** for this API and is sent as a query parameter.

| Parameter | Type | Mandatory | Default | Max Length | Description |
|-----------|------|-----------|---------|------------|-------------|
| `clients` | JSONArray of JSONObject | **Yes** | — | 500000 | Candidate client workspaces, grouped by the organisation that owns them. **1–100** entries. An absent or non-array `clients` is `8077`. See [`clients` Fields](#clients-fields). |

#### `clients` Fields

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `orgId` | Long | **Yes** | — | 20 | Organisation that owns the listed workspaces, as a JSON **number**. The caller must administer it (`7301`). |
| `workspaceIds` | JSONArray of String | **Yes** | — | 5000 | Client workspace IDs to validate, as numeric **strings**, **1–100** entries. Every ID must belong to `orgId` (`7387`). Duplicates across organisation entries are de-duplicated before validation. |

> **`orgId` is a number, `workspaceIds` entries are strings.** The request template declares `orgId` as a long and each `workspaceIds` entry as text, so the samples below quote the workspace IDs and leave `orgId` unquoted. See [Appendix D](#appendix-d--general-response-payload-notes).

### Sample Requests

**Case 1 — Check one candidate workspace**

```http
GET /restapi/v2/workspaces/137687000271334001/linkedworkspaces/compatibility?CONFIG={"clients":[{"orgId":700000654321,"workspaceIds":["466206000000071000"]}]} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Check several workspaces across two organisations**

```http
GET /restapi/v2/workspaces/137687000271334001/linkedworkspaces/compatibility?CONFIG={"clients":[{"orgId":700000654321,"workspaceIds":["466206000000071000","466206000000071010"]},{"orgId":700000999999,"workspaceIds":["466206000000081010"]}]} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — The master workspace is itself a client of another master (rejected)**

```http
GET /restapi/v2/workspaces/466206000000071000/linkedworkspaces/compatibility?CONFIG={"clients":[{"orgId":700000654321,"workspaceIds":["466206000000071010"]}]} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Sample Responses

**HTTP 200 OK — One compatible workspace and one with entity conflicts**

```json
{
    "status": "success",
    "summary": "Get workspace linking compatibility",
    "data": {
        "clients": [
            {
                "orgId": "700000654321",
                "orgName": "Northwind Retail",
                "workspaces": [
                    {
                        "workspaceId": "466206000000071000",
                        "workspaceName": "Northwind Sandbox",
                        "isCompatible": true,
                        "error": null,
                        "entities": {
                            "dataSources": [],
                            "tables": [],
                            "views": []
                        }
                    },
                    {
                        "workspaceId": "466206000000071010",
                        "workspaceName": "Northwind EU Sandbox",
                        "isCompatible": false,
                        "error": "Some entities have conflicts",
                        "entities": {
                            "dataSources": [
                                {
                                    "datasourceId": "466206000000095001",
                                    "datasourceName": "Books Connection",
                                    "status": "failure",
                                    "message": "Connection configuration differs"
                                }
                            ],
                            "tables": [
                                {
                                    "viewId": "137687000006991601",
                                    "viewName": "Sales_Fact",
                                    "status": "warning",
                                    "message": "Column structure differs"
                                }
                            ],
                            "views": [
                                {
                                    "viewId": "466206000000105001",
                                    "viewName": "Revenue by Region",
                                    "status": "failure",
                                    "message": "Formula column missing in client workspace"
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }
}
```

**HTTP 200 OK — A workspace blocked for a workspace-level reason: `entities` is null**

```json
{
    "status": "success",
    "summary": "Get workspace linking compatibility",
    "data": {
        "clients": [
            {
                "orgId": "700000999999",
                "orgName": "Contoso Distribution",
                "workspaces": [
                    {
                        "workspaceId": "466206000000081010",
                        "workspaceName": "Contoso Sandbox",
                        "isCompatible": false,
                        "error": "This workspace is already linked to another master workspace.",
                        "entities": null
                    }
                ]
            }
        ]
    }
}
```

**HTTP 400 Bad Request — Failure paired with Case 3**

```json
{
    "status": "failure",
    "summary": "INVALID_MASTER_WORKSPACE_MAPPING",
    "data": {
        "errorCode": 8246,
        "errorMessage": "The provided master workspace is already mapped to another workspace."
    }
}
```

**HTTP 400 Bad Request — `clients` missing from CONFIG**

```json
{
    "status": "failure",
    "summary": "EMPTY_JSON_CONFIGURATION",
    "data": {
        "errorCode": 8077,
        "errorMessage": "Empty JSON configuration. Kindly provide a valid JSON configuration."
    }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. A workspace being incompatible is **not** a failure — the envelope is still `success`. |
| `summary` | String | `"Get workspace linking compatibility"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.clients` | JSONArray | One entry per organisation in the request, in request order. **Always present.** |
| `clients[].orgId` | String | Organisation ID, echoed from the request but serialised as a **string**. |
| `clients[].orgName` | String | Organisation display name, resolved server-side. |
| `clients[].workspaces` | JSONArray | One report per workspace in that organisation's `workspaceIds`, in request order. A workspace the validator could not evaluate at all is **omitted**, so this array can be shorter than what you sent. |
| `workspaces[].workspaceId` | String | The candidate workspace. |
| `workspaces[].workspaceName` | String | Its display name. |
| `workspaces[].isCompatible` | Boolean | `true` when the workspace can be linked as-is. **This is the field [Link Workspaces](#5-link-workspaces) gates on.** |
| `workspaces[].error` | String | `null` when compatible. Otherwise either a workspace-level reason (already linked, unsupported configuration, …) or the fixed string `"Some entities have conflicts"` when the detail is in `entities`. |
| `workspaces[].entities` | JSONObject | The per-entity breakdown — **`null`** when the workspace was blocked for a workspace-level reason with no entity detail. Always a populated object otherwise, including for compatible workspaces, where its three arrays are empty. |
| `entities.dataSources` | JSONArray | Conflicting or noteworthy data sources. |
| `dataSources[].datasourceId` | String | Data source ID. **Present here but absent from the same structure in [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details).** |
| `dataSources[].datasourceName` | String | Data source name. |
| `dataSources[].status` | String | Per-entity verdict — `success`, `warning` or `failure`. See [Entity Status Values](#entity-status-values). |
| `dataSources[].message` | String | Human-readable reason. `"Compatible"` when the underlying reason is the no-conflict sentinel. Always rendered in **English**, regardless of the caller's locale. |
| `entities.tables` | JSONArray | Conflicting or noteworthy tables. |
| `entities.views` | JSONArray | Conflicting or noteworthy reports. |
| `tables[].viewId` / `views[].viewId` | String | Entity ID in the **master** workspace. |
| `tables[].viewName` / `views[].viewName` | String | Entity name. |
| `tables[].status` / `views[].status` | String | Per-entity verdict — `success`, `warning` or `failure`. |
| `tables[].message` / `views[].message` | String | Human-readable reason, in English. |

> Unlike the entity lists of [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details), the entries here carry **no** `viewType` or `viewTypeId`.

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **It is a dry run and changes nothing** | No link, no schedule, no state. Safe to call as often as you like. |
| **Incompatibility is a `200`, not an error** | Only request-level problems produce a failure envelope. Branch on `isCompatible`, never on the HTTP status. |
| **`entities` is `null` for workspace-level blocks** | When `error` carries a reason and there is no entity detail, `entities` is JSON `null` rather than an object with empty arrays. Guard before indexing into it. |
| **`error` is `null` when compatible** | The three states are: compatible (`error: null`), blocked at workspace level (`error` = reason, `entities: null`), blocked by entity conflicts (`error` = `"Some entities have conflicts"`, `entities` populated). |
| **Messages are always English** | Per-entity `message` values are resolved through a fixed `en-US` bundle, so they do not follow the caller's language. Do not parse them; use `status`. |
| **A `warning` does not block linking** | `isCompatible` is computed from the workspace-level verdict, so a workspace can be compatible while individual entities report `warning`. |
| **Workspaces may be missing from the response** | A candidate the validator could not evaluate produces no report rather than a failed one. Match the response back to your request by `workspaceId` instead of by position. |
| **It is validated per workspace, not per batch** | Each candidate is evaluated independently against the master, so adding a bad workspace to the list does not change the verdict of the others. |
| **CONFIG travels in the query string** | This is a `GET`; send `CONFIG` as a URL-encoded query parameter, not as a body. No `Content-Type` header is needed. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get Linkable Workspaces](#3-get-linkable-workspaces) → `orgs[].orgId` + `workspaces[].workspaceId` → Get Workspace Linking Compatibility → confirm `isCompatible` → [Link Workspaces](#5-link-workspaces). |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7103 | `META_OBJECT_NOT_PRESENT` — The master workspace or one of the candidate workspaces was not found. | Verify `<workspace-id>` and every `clients[].workspaceIds` entry. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller does not administer the header organisation, the master's organisation, or one of the organisations named in `clients[].orgId`; or the request arrived through a Client Portal / White Label domain. | Authenticate as an administrator of every organisation in the payload, from the standard API host. |
| 7387 | `DBID_NOT_BELONGS_TO_ZSOID` — One or more `workspaceIds` do not belong to the `orgId` they were listed under. | Group each workspace under the organisation that actually owns it, as reported by [Get Linkable Workspaces](#3-get-linkable-workspaces). |
| 8060 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use the standard API host. |
| 8077 | `EMPTY_JSON_CONFIGURATION` — `CONFIG` carries no `clients` array. | Send `{"clients":[{"orgId":…,"workspaceIds":[…]}]}`. |
| 8080 | `INVALID_JSON_CONFIGURATION` — `CONFIG` is not parseable JSON. | Send a valid, URL-encoded JSON object. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| 8246 | `INVALID_MASTER_WORKSPACE_MAPPING` — `<workspace-id>` is itself linked as a client of another master. | Use a workspace that is not already a client; a workspace cannot be both. |
| 8504 | `LESS_THAN_MIN_OCCURANCE` — The `CONFIG` parameter was not sent, or `clients` is outside its 1–100 bound. | Send `CONFIG` with between 1 and 100 organisation entries. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

---

## 5. Link Workspaces

Links one or more client workspaces to a master. The request is validated for compatibility first and, if every candidate passes, the initial design push is **scheduled**. Candidates already linked to this master are skipped silently.

| Attribute | Value |
|-----------|-------|
| **Method** | POST |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/linkedworkspaces` |
| **OAuth Scope** | `ZohoAnalytics.modeling.create` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the master workspace. |
| **Permission Required** | The authenticated user must be an Account Admin or an Organization Admin of the organisation in `ZANALYTICS-ORGID`, of the organisation that owns `<workspace-id>`, **and of every organisation named in `clients[].orgId`**. |

### CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Max Length | Description |
|-----------|------|-----------|---------|------------|-------------|
| `clients` | JSONArray of JSONObject | **Yes** | — | 500000 | Client workspaces to link, grouped by the organisation that owns them. **1–100** entries. Identical in shape to the attribute of [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility) — see [`clients` Fields](#clients-fields). |

> **Already-linked candidates are removed before validation, not rejected.** Any `workspaceIds` entry already linked to this master is filtered out; if that empties the whole payload the call returns `204` having done nothing. A `204` is therefore not proof that anything was linked.

### Sample Requests

**Case 1 — Link one client workspace**

```http
POST /restapi/v2/workspaces/137687000271334001/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "clients": [
        {
            "orgId": 700000654321,
            "workspaceIds": ["466206000000071000"]
        }
    ]
}
```

**Case 2 — Link several workspaces across two client organisations**

```http
POST /restapi/v2/workspaces/137687000271334001/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "clients": [
        {
            "orgId": 700000654321,
            "workspaceIds": ["466206000000071000", "466206000000071010"]
        },
        {
            "orgId": 700000999999,
            "workspaceIds": ["466206000000081010"]
        }
    ]
}
```

**Case 3 — One candidate is incompatible, so the whole request is refused (rejected)**

```http
POST /restapi/v2/workspaces/137687000271334001/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "clients": [
        {
            "orgId": 700000654321,
            "workspaceIds": ["466206000000071000", "466206000000071010"]
        }
    ]
}
```

### Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. It means the link was validated and **scheduled**, not that it has completed.

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — Failure paired with Case 3**

The failure payload carries the full compatibility report for the workspaces that blocked the request, under `data.incompatibleWorkspaces`.

```json
{
    "status": "failure",
    "summary": "LINK_WORKSPACES_INCOMPATIBLE_WORKSPACES",
    "data": {
        "errorCode": 8247,
        "errorMessage": "Workspace linking cannot proceed because the following workspaces are incompatible: Northwind EU Sandbox",
        "incompatibleWorkspaces": [
            {
                "orgId": "700000654321",
                "orgName": "Northwind Retail",
                "workspaces": [
                    {
                        "workspaceId": "466206000000071010",
                        "workspaceName": "Northwind EU Sandbox",
                        "isCompatible": false,
                        "error": "Some entities have conflicts",
                        "entities": {
                            "dataSources": [
                                {
                                    "datasourceId": "466206000000095001",
                                    "datasourceName": "Books Connection",
                                    "status": "failure",
                                    "message": "Connection configuration differs"
                                }
                            ],
                            "tables": [],
                            "views": []
                        }
                    }
                ]
            }
        ]
    }
}
```

**HTTP 400 Bad Request — The master is itself a client of another master**

```json
{
    "status": "failure",
    "summary": "INVALID_MASTER_WORKSPACE_MAPPING",
    "data": {
        "errorCode": 8246,
        "errorMessage": "The provided master workspace is already mapped to another workspace."
    }
}
```

### Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`), plus `data.incompatibleWorkspaces` on `8247`.

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`204` means scheduled, not linked** | The compatibility check runs inline, but the design push is handed to a scheduler. The sandbox IDs do not exist yet when the response arrives — poll [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace) until they appear. |
| **All-or-nothing on compatibility** | If any surviving candidate is incompatible, **nothing** is linked and the response carries every blocking workspace in `data.incompatibleWorkspaces` (`8247`). Run [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility) first to avoid the round trip. |
| **Idempotent in effect** | Re-sending the same payload filters out the now-linked workspaces and returns `204` having done nothing. There is no duplicate-link error. |
| **A `204` can mean "nothing happened"** | Because already-linked candidates are filtered before anything else runs, a payload consisting entirely of existing links short-circuits to `204` — **without** validating the master, the candidate organisations, or the caller's rights over them. Confirm the end state with a listing call. |
| **Duplicate workspace IDs collapse** | IDs repeated within or across `clients[]` entries are de-duplicated before linking. |
| **The link is one-directional** | The master pushes to the client. Nothing flows back, and a client cannot become a master while it is linked (`8246`). |
| **No `sandboxId` is returned** | The identifier every other API needs is only discoverable through [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace). |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get Linkable Workspaces](#3-get-linkable-workspaces) → [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility) → Link Workspaces → [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace) → `sandboxId`. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7103 | `META_OBJECT_NOT_PRESENT` — The master workspace or one of the candidate workspaces was not found. | Verify `<workspace-id>` and every `clients[].workspaceIds` entry. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller does not administer the header organisation, the master's organisation, or one of the organisations named in `clients[].orgId`; or the request arrived through a Client Portal / White Label domain. | Authenticate as an administrator of every organisation in the payload, from the standard API host. |
| 7387 | `DBID_NOT_BELONGS_TO_ZSOID` — One or more `workspaceIds` do not belong to the `orgId` they were listed under. | Group each workspace under the organisation that owns it. |
| 8060 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use the standard API host. |
| 8077 | `EMPTY_JSON_CONFIGURATION` — `CONFIG` carries no `clients` array. | Send `{"clients":[{"orgId":…,"workspaceIds":[…]}]}`. |
| 8080 | `INVALID_JSON_CONFIGURATION` — `CONFIG` is not parseable JSON. | Send a valid, URL-encoded JSON object. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| 8246 | `INVALID_MASTER_WORKSPACE_MAPPING` — `<workspace-id>` is itself linked as a client of another master. | Use a workspace that is not already a client. |
| 8247 | `LINK_WORKSPACES_INCOMPATIBLE_WORKSPACES` — At least one candidate failed the compatibility check. Nothing was linked. | Read `data.incompatibleWorkspaces`, resolve the conflicts or drop those workspaces, and resend. |
| 8504 | `LESS_THAN_MIN_OCCURANCE` — The `CONFIG` parameter was not sent, or `clients` is outside its 1–100 bound. | Send `CONFIG` with between 1 and 100 organisation entries. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |

---

## 6. Sync Linked Workspaces

Pushes the master workspace's design to its linked clients. The request either syncs every link, or names the sandboxes to sync and — per sandbox — either everything or a specific list of master-workspace views.

| Attribute | Value |
|-----------|-------|
| **Method** | POST |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/linkedworkspaces/sync` |
| **OAuth Scope** | `ZohoAnalytics.modeling.create` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the master workspace. |
| **Permission Required** | The authenticated user must be an Account Admin or an Organization Admin of the organisation in `ZANALYTICS-ORGID` and of the organisation that owns `<workspace-id>`. When `masterViewIds` is used, the caller must additionally administer the organisation owning each listed view's workspace. |

### CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Max Length | Description |
|-----------|------|-----------|---------|------------|-------------|
| `scope` | String (enum) | **Yes** | — | 20 | `ALL` syncs every linked sandbox of this master; `SELECTED` requires `clients`. **Case-sensitive — must be upper case** (`8119` otherwise). See [`scope` Values](#scope-values) and [The `scope` Attribute](#the-scope-attribute). |
| `clients` | JSONArray of JSONObject | Conditional | — | 5000000 | Per-sandbox sync instructions, **1–100** entries. **Mandatory when `scope` is `SELECTED`**, and **must be omitted when `scope` is `ALL`** — either mistake is `8250`. See [`clients` Sync Fields](#clients-sync-fields). |

#### `clients` Sync Fields

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `sandboxId` | Long | **Yes** | — | 20 | The link to sync, as a JSON **number**. Must already be mapped to `<workspace-id>` (`8248`). A blank or absent value is `8251`. |
| `scope` | String (enum) | **Yes** | — | 20 | `ALL` syncs every eligible entity to this sandbox; `SELECTED` requires `masterViewIds`. **Case-insensitive** — it is upper-cased before comparison, unlike the top-level `scope`. Anything other than `ALL` or `SELECTED` is `8251`. See [`scope` Values](#scope-values). |
| `masterViewIds` | JSONArray of String | Conditional | — | 50000 | Master-workspace view IDs to push to this sandbox, as numeric **strings**, **1–1000** entries. **Mandatory when this entry's `scope` is `SELECTED`**, and **must be omitted when it is `ALL`** — either mistake is `8251`. |

> **A single request may mix both per-client modes.** Entries with `scope: "ALL"` are collected and scheduled together; entries with `scope: "SELECTED"` push their named views immediately. See the Notes below — the two halves do not behave the same way.

### Sample Requests

**Case 1 — Sync every linked workspace**

```http
POST /restapi/v2/workspaces/137687000271334001/linkedworkspaces/sync HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scope": "ALL"
}
```

**Case 2 — Sync two named sandboxes, one fully and one with selected views**

```http
POST /restapi/v2/workspaces/137687000271334001/linkedworkspaces/sync HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scope": "SELECTED",
    "clients": [
        {
            "sandboxId": 137687000012345001,
            "scope": "ALL"
        },
        {
            "sandboxId": 137687000012345002,
            "scope": "SELECTED",
            "masterViewIds": ["137687000006991601", "466206000000105001"]
        }
    ]
}
```

**Case 3 — `clients` supplied alongside `scope: "ALL"` (rejected)**

```http
POST /restapi/v2/workspaces/137687000271334001/linkedworkspaces/sync HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scope": "ALL",
    "clients": [
        {
            "sandboxId": 137687000012345001,
            "scope": "ALL"
        }
    ]
}
```

**Case 4 — Per-client `SELECTED` without `masterViewIds` (rejected)**

```http
POST /restapi/v2/workspaces/137687000271334001/linkedworkspaces/sync HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scope": "SELECTED",
    "clients": [
        {
            "sandboxId": 137687000012345001,
            "scope": "SELECTED"
        }
    ]
}
```

### Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status.

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — Failure paired with Case 3**

```json
{
    "status": "failure",
    "summary": "INVALID_CONFIGURATION_SYNC_SCOPE_LINKED_WORKSPACES",
    "data": {
        "errorCode": 8250,
        "errorMessage": "Invalid configuration. Kindly provide scope as 'ALL' to sync all linked workspaces or set scope to 'SELECTED' with valid clients array."
    }
}
```

**HTTP 400 Bad Request — Failure paired with Case 4**

```json
{
    "status": "failure",
    "summary": "INVALID_CONFIGURATION_SYNC_CLIENT_SCOPE_LINKED_WORKSPACES",
    "data": {
        "errorCode": 8251,
        "errorMessage": "Invalid configuration. For each client, kindly set scope to 'ALL' to sync all views, or set scope to 'SELECTED' with a valid 'masterViewIds' array."
    }
}
```

**HTTP 400 Bad Request — A `sandboxId` is not linked to this master**

```json
{
    "status": "failure",
    "summary": "SANDBOX_NOT_MAPPED_TO_MASTER_WORKSPACE",
    "data": {
        "errorCode": 8248,
        "errorMessage": "One or more provided sandbox IDs are not mapped to the given master workspace: 137687000012345009"
    }
}
```

### Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`).

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`204` means accepted, not delivered** | Full-sandbox syncs are handed to a scheduler and run afterwards. The only way to learn what a sync did is [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details). |
| **The two per-client modes behave differently** | `scope: "SELECTED"` entries push their `masterViewIds` **inline**, during the request. `scope: "ALL"` entries — and a top-level `scope: "ALL"` — are **scheduled**. A mixed request therefore completes part of its work before responding and defers the rest. |
| **Validation order matters on a mixed request** | All sandbox IDs are validated against the master before anything runs (`8248`), but the inline per-view pushes happen **before** the scheduled full syncs are queued. A failure after the first push leaves the request partially applied. |
| **Top-level `scope` is case-sensitive, per-client `scope` is not** | `{"scope":"all"}` is `8119`; `clients[].scope: "all"` is accepted. Send upper case everywhere. |
| **`ALL` means every link of this master** | Not every link in the organisation. The sandbox list is resolved from `<workspace-id>`. |
| **Not idempotent in effect** | Each call pushes again. Re-syncing an unchanged master is harmless but is not free, and it overwrites client-side drift. |
| **Duplicate sandbox IDs collapse** | A sandbox named twice with `scope: "ALL"` is synced once. |
| **The master must not be a client** | A master that is itself linked as somebody's client is refused with `8246` before any sync work starts. |
| **Views are addressed in the master, not the client** | `masterViewIds` are IDs in `<workspace-id>`. Client-side IDs are never accepted. |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace) → `sandboxId` (+ [Get View List](../06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#6-get-view-list) → `masterViewIds`) → Sync Linked Workspaces → [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details). |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7103 | `META_OBJECT_NOT_PRESENT` — The master workspace was not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| 7104 | `META_OBJECT_NOT_PRESENT` — A `masterViewIds` entry does not exist. | Verify every view ID via [Get View List](../06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#6-get-view-list) against the master workspace. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller does not administer the header organisation, the master's organisation, or the organisation owning a workspace named in `masterViewIds`; or the request arrived through a Client Portal / White Label domain. | Authenticate as an organisation administrator and call from the standard API host. |
| 8060 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use the standard API host. |
| 8077 | `EMPTY_JSON_CONFIGURATION` — `CONFIG` is empty. | Send at least `{"scope":"ALL"}`. |
| 8079 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — `scope` is missing from CONFIG. | Add the top-level `scope`. |
| 8080 | `INVALID_JSON_CONFIGURATION` — `CONFIG` is not parseable JSON. | Send a valid, URL-encoded JSON object. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| 8119 | `INVALID_VALUE_FOR_ATTRIBUTE` — The top-level `scope` is not exactly `ALL` or `SELECTED`. | Send upper-case `ALL` or `SELECTED`. |
| 8246 | `INVALID_MASTER_WORKSPACE_MAPPING` — `<workspace-id>` is itself linked as a client of another master. | Sync from the real master. |
| 8248 | `SANDBOX_NOT_MAPPED_TO_MASTER_WORKSPACE` — One or more `clients[].sandboxId` values are not linked to this master. The message names them. | Use sandbox IDs from [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace). |
| 8250 | `INVALID_CONFIGURATION_SYNC_SCOPE_LINKED_WORKSPACES` — `clients` was supplied with `scope: "ALL"`, omitted with `scope: "SELECTED"`, or resolved to nothing to sync. | Send `{"scope":"ALL"}` or `{"scope":"SELECTED","clients":[…]}`. |
| 8251 | `INVALID_CONFIGURATION_SYNC_CLIENT_SCOPE_LINKED_WORKSPACES` — A `clients[]` entry is missing `sandboxId`, carries a `scope` other than `ALL` / `SELECTED`, supplies `masterViewIds` with `scope: "ALL"`, or omits them with `scope: "SELECTED"`. | Give each entry a `sandboxId` plus either `{"scope":"ALL"}` or `{"scope":"SELECTED","masterViewIds":[…]}`. |
| 8504 | `LESS_THAN_MIN_OCCURANCE` — The `CONFIG` parameter was not sent, or `clients` is outside its 1–100 bound. | Send `CONFIG` with a valid JSON object. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |

---

## 7. Get Linked Workspace Sync Details

Returns, per linked sandbox, what the last sync did entity by entity and what is still waiting to be pushed. This is the only API that reports sync outcomes at entity granularity.

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/linkedworkspaces/sync` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the master workspace. |
| **Permission Required** | The authenticated user must be an Account Admin or an Organization Admin of the organisation in `ZANALYTICS-ORGID` and of the organisation that owns `<workspace-id>`. |

### CONFIG Parameters

CONFIG is **optional** for this API and is sent as a query parameter. Omit it entirely to get every linked sandbox of the master.

| Parameter | Type | Mandatory | Default | Max Length | Description |
|-----------|------|-----------|---------|------------|-------------|
| `sandboxIds` | JSONArray of String | **Yes** when `CONFIG` is sent | All linked sandboxes of the master | 5000 | Restricts the response to these links, as numeric **strings**, **1–100** entries. Every ID must already be mapped to `<workspace-id>` (`8248`). |

> **`CONFIG` is optional, but `sandboxIds` is not optional within it.** The request template marks `sandboxIds` as a required key, so sending `CONFIG={}` is rejected while omitting `CONFIG` altogether is the supported way to ask for everything.

### Sample Requests

**Case 1 — Every linked sandbox of the master**

```http
GET /restapi/v2/workspaces/137687000271334001/linkedworkspaces/sync HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Two named sandboxes**

```http
GET /restapi/v2/workspaces/137687000271334001/linkedworkspaces/sync?CONFIG={"sandboxIds":["137687000012345001","137687000012345002"]} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — A sandbox that is not linked to this master (rejected)**

```http
GET /restapi/v2/workspaces/137687000271334001/linkedworkspaces/sync?CONFIG={"sandboxIds":["137687000012345009"]} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Sample Responses

**HTTP 200 OK — One sandbox with a partially successful last sync and pending work**

```json
{
    "status": "success",
    "summary": "Get linked workspace sync details",
    "data": {
        "workspaces": [
            {
                "sandboxId": "137687000012345001",
                "workspaceId": "466206000000071000",
                "workspaceName": "Northwind Sandbox",
                "lastSync": {
                    "syncTime": "1779226560981",
                    "syncStatus": "partialSuccess",
                    "syncedBy": "jane.doe@example.com",
                    "syncedByName": "Jane Doe",
                    "syncedByZuId": "60002000000000123",
                    "entities": {
                        "dataSources": [
                            {
                                "datasourceName": "Books Connection",
                                "status": "success",
                                "message": "Compatible"
                            }
                        ],
                        "tables": [
                            {
                                "viewId": "137687000006991601",
                                "viewName": "Sales_Fact",
                                "viewType": "Table",
                                "viewTypeId": 0,
                                "status": "success",
                                "message": "Compatible"
                            }
                        ],
                        "views": [
                            {
                                "viewId": "466206000000105001",
                                "viewName": "Revenue by Region",
                                "viewType": "Chart View",
                                "viewTypeId": 2,
                                "status": "failure",
                                "message": "Formula column missing in client workspace"
                            }
                        ]
                    }
                },
                "hasPendingEntities": true,
                "pendingEntities": {
                    "dataSources": [],
                    "tables": [
                        {
                            "viewId": "137687000006991601",
                            "viewName": "Sales_Fact",
                            "viewType": "Table",
                            "viewTypeId": 0,
                            "modifiedStatus": "updated"
                        }
                    ],
                    "views": [
                        {
                            "viewId": "466206000000105001",
                            "viewName": "Revenue by Region",
                            "viewType": "Chart View",
                            "viewTypeId": 2,
                            "modifiedStatus": "created"
                        }
                    ]
                }
            }
        ]
    }
}
```

**HTTP 200 OK — A link that has never synced**

```json
{
    "status": "success",
    "summary": "Get linked workspace sync details",
    "data": {
        "workspaces": [
            {
                "sandboxId": "137687000012345003",
                "workspaceId": "466206000000081010",
                "workspaceName": "Contoso Sandbox",
                "lastSync": {
                    "syncTime": "0",
                    "syncStatus": "inProgress",
                    "syncedBy": "john.roe@example.com",
                    "syncedByName": "John Roe",
                    "syncedByZuId": "60002000000000456",
                    "entities": {
                        "dataSources": [],
                        "tables": [],
                        "views": []
                    }
                },
                "hasPendingEntities": false,
                "pendingEntities": {
                    "dataSources": [],
                    "tables": [],
                    "views": []
                }
            }
        ]
    }
}
```

**HTTP 400 Bad Request — Failure paired with Case 3**

```json
{
    "status": "failure",
    "summary": "SANDBOX_NOT_MAPPED_TO_MASTER_WORKSPACE",
    "data": {
        "errorCode": 8248,
        "errorMessage": "One or more provided sandbox IDs are not mapped to the given master workspace: 137687000012345009"
    }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | `"Get linked workspace sync details"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.workspaces` | JSONArray | One entry per requested (or resolved) sandbox. **Always present**; `[]` when the master has no links. Note the key is `workspaces`, not `clients`. |
| `workspaces[].sandboxId` | String | The link's identifier. |
| `workspaces[].workspaceId` | String | The client workspace behind that link. |
| `workspaces[].workspaceName` | String | Client workspace display name. |
| `workspaces[].lastSync` | JSONObject | What the last sync did. **Always present.** |
| `lastSync.syncTime` | String | Time of the last successful sync as **epoch milliseconds in a string**, `"0"` when the link has never synced successfully. Same representation as the listing APIs — not a formatted date. |
| `lastSync.syncStatus` | String | `success`, `failure`, `partialSuccess`, `inProgress` or `unknown`. See [Sync Status Values](#sync-status-values). |
| `lastSync.syncedBy` | String | E-mail address of the user who ran that sync. |
| `lastSync.syncedByName` | String | Display name of that user. |
| `lastSync.syncedByZuId` | String | ZUID of that user, as a string. |
| `lastSync.entities` | JSONObject | Per-entity outcome of the last sync, read from the stored sync state. **Always present**, with three empty arrays when no state is stored. |
| `entities.dataSources[]` | JSONArray | Data sources touched by the last sync: `datasourceName`, `status`, `message`. **There is no `datasourceId` here** — unlike the same structure in [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility). |
| `entities.tables[]` / `entities.views[]` | JSONArray | Tables and reports touched by the last sync: `viewId`, `viewName`, `viewType`, `viewTypeId`, `status`, `message`. |
| `tables[].viewType` / `views[].viewType` | String | Display name of the entity type — `Table`, `Chart View`, … See [View Type Reference](#view-type-reference). Falls back to the raw numeric id rendered as a string for an unrecognised type. |
| `tables[].viewTypeId` / `views[].viewTypeId` | Number | Numeric type id companion to `viewType`. Native JSON number. |
| `tables[].status` / `views[].status` / `dataSources[].status` | String | Per-entity outcome — `success`, `warning` or `failure`. See [Entity Status Values](#entity-status-values). |
| `tables[].message` / `views[].message` / `dataSources[].message` | String | Human-readable reason, normalised to `"Compatible"` when there was no problem. Always **English**, regardless of the caller's locale. |
| `workspaces[].hasPendingEntities` | Boolean | `true` when the master has changes not yet pushed to this client. Native JSON boolean. |
| `workspaces[].pendingEntities` | JSONObject | What the next sync would push. **Always present**, with three empty arrays when nothing is pending. |
| `pendingEntities.dataSources` | JSONArray | **Always empty.** Pending data sources are not reported; only tables and reports are. |
| `pendingEntities.tables[]` / `pendingEntities.views[]` | JSONArray | Pending entities: `viewId`, `viewName`, `viewType`, `viewTypeId`, `modifiedStatus`. |
| `pendingEntities.tables[].modifiedStatus` | String | `created`, `updated` or `deleted` — what the next sync will do to this entity on the client. See [Modified Status Values](#modified-status-values). |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **The only entity-level view of a sync** | The listing APIs report a single `syncStatus` per link; this is where you find out which table or report failed, and why. |
| **`syncTime` is epoch milliseconds, not a formatted date** | A string of digits; `"0"` when the link has never synced. Format it client-side. |
| **`lastSync.entities` reflects stored state, not a live check** | It is read from the sync state recorded by the last run. A link that has never synced returns three empty arrays, not an error. |
| **`pendingEntities.dataSources` is always empty** | The pending calculation covers tables and reports only. Do not infer "no data source changes" from it. |
| **Pending counts include deletions** | `hasPendingEntities` is driven by created, modified **and** deleted master entities, so it can be `true` purely because something was removed from the master. The `deleted` value of `modifiedStatus` marks those. |
| **The entity shape differs from the compatibility API** | Here, entries carry `viewType` / `viewTypeId` and data sources carry no `datasourceId`. There, it is the other way round. Two structures, two shapes — map them separately. |
| **Omitting `CONFIG` is the way to ask for everything** | Sending `CONFIG={}` fails the template's required-key check; omit the parameter instead. |
| **One remote read per sandbox** | Details are fetched per link, so a master with many clients makes a correspondingly larger request. Filter with `sandboxIds` when you only need a few. |
| **No paging, filtering or sorting** | Beyond `sandboxIds`, there are no query options. |
| **CONFIG travels in the query string** | This is a `GET`; send `CONFIG` as a URL-encoded query parameter, not as a body. No `Content-Type` header is needed. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace) → `sandboxId` → Get Linked Workspace Sync Details; after [Sync Linked Workspaces](#6-sync-linked-workspaces), poll here for the outcome. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7103 | `META_OBJECT_NOT_PRESENT` — The master workspace was not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not an organisation administrator of the header organisation or of the master's organisation, or the request arrived through a Client Portal / White Label domain. | Authenticate as an organisation administrator and call from the standard API host. |
| 8060 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use the standard API host. |
| 8080 | `INVALID_JSON_CONFIGURATION` — `CONFIG` was sent but is not a parseable JSON object. | Send a valid, URL-encoded JSON object, or omit `CONFIG` entirely. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| 8248 | `SANDBOX_NOT_MAPPED_TO_MASTER_WORKSPACE` — One or more `sandboxIds` are not linked to this master. The message names them. | Use sandbox IDs from [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace). |
| 8504 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` was sent without `sandboxIds`, or with more than 100 entries. | Omit `CONFIG` to fetch everything, or send 1–100 sandbox IDs. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

---

## 8. Unlink Workspaces

Removes links between a master workspace and its clients, either all of them or a named set. The client workspaces themselves survive — only the mapping, and the design relationship it carries, is removed.

| Attribute | Value |
|-----------|-------|
| **Method** | DELETE |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/linkedworkspaces` |
| **OAuth Scope** | `ZohoAnalytics.modeling.delete` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the master workspace. |
| **Permission Required** | The authenticated user must be an Account Admin or an Organization Admin of the organisation in `ZANALYTICS-ORGID` and of the organisation that owns `<workspace-id>`. |

### CONFIG Parameters

CONFIG is **mandatory** for this API, and it is sent as a form body on a `DELETE` request.

| Parameter | Type | Mandatory | Default | Max Length | Description |
|-----------|------|-----------|---------|------------|-------------|
| `scope` | String (enum) | **Yes** | — | 20 | `ALL` unlinks every client of this master; `SELECTED` unlinks the listed `sandboxIds`. **Case-sensitive — must be upper case** (`8119` otherwise). See [`scope` Values](#scope-values). |
| `sandboxIds` | JSONArray of String | Conditional | — | 5000 | Links to remove, as numeric **strings**, **1–100** entries. **Mandatory when `scope` is `SELECTED`**, and **must be omitted or empty when `scope` is `ALL`** — either mistake is `8249`. Every ID must already be mapped to `<workspace-id>` (`8248`). |

### Sample Requests

**Case 1 — Unlink every client of the master**

```http
DELETE /restapi/v2/workspaces/137687000271334001/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scope": "ALL"
}
```

**Case 2 — Unlink two named sandboxes**

```http
DELETE /restapi/v2/workspaces/137687000271334001/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scope": "SELECTED",
    "sandboxIds": ["137687000012345001", "137687000012345002"]
}
```

**Case 3 — `scope: "SELECTED"` without `sandboxIds` (rejected)**

```http
DELETE /restapi/v2/workspaces/137687000271334001/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scope": "SELECTED"
}
```

### Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. No per-sandbox result list is returned.

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — Failure paired with Case 3**

```json
{
    "status": "failure",
    "summary": "INVALID_CONFIGURATION_REMOVE_LINKED_WORKSPACES",
    "data": {
        "errorCode": 8249,
        "errorMessage": "Invalid configuration. Kindly provide scope as 'ALL' to remove all linked workspaces from the master workspace or scope as 'SELECTED' with valid sandboxIds."
    }
}
```

**HTTP 400 Bad Request — `scope` sent in lower case**

```json
{
    "status": "failure",
    "summary": "INVALID_VALUE_FOR_ATTRIBUTE",
    "data": {
        "errorCode": 8119,
        "errorMessage": "Invalid value 'all' provided for the attribute 'scope'. Only 'ALL, SELECTED' are allowed."
    }
}
```

### Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`).

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Client workspaces are not deleted** | Only the mapping is removed. The client keeps whatever design was last pushed to it, and it becomes an ordinary, independent workspace. |
| **`scope: "ALL"` on a master with no links is a no-op** | The resolved sandbox list is empty, so the call returns `204` having done nothing. It is not an error. |
| **Idempotent for `ALL`, not for `SELECTED`** | Repeating `{"scope":"ALL"}` is harmless. Repeating a `SELECTED` request with the same IDs fails with `8248`, because they are no longer mapped. |
| **Validated up front** | Every `sandboxIds` entry is checked against the master before anything is removed, so one bad ID fails the whole request and nothing is unlinked. |
| **Nothing is reported per sandbox** | "Unlinked" and "was already gone" are indistinguishable from the response. Confirm with [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace). |
| **`scope` is case-sensitive here** | Unlike the per-client `scope` of [Sync Linked Workspaces](#6-sync-linked-workspaces), this one is compared verbatim. `"all"` is `8119`. |
| **Relinking starts over** | A workspace unlinked and linked again gets a **new** sandbox ID and an empty sync history. Nothing carries over. |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace) → `sandboxId` → Unlink Workspaces. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7103 | `META_OBJECT_NOT_PRESENT` — The master workspace was not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not an organisation administrator of the header organisation or of the master's organisation, or the request arrived through a Client Portal / White Label domain. | Authenticate as an organisation administrator and call from the standard API host. |
| 8060 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use the standard API host. |
| 8078 | `EMPTY_JSON_ATTRIBUTE_FOUND` — `scope` was sent with an empty value. | Send `ALL` or `SELECTED`. |
| 8079 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — `scope` is missing from CONFIG. | Add `scope`. |
| 8080 | `INVALID_JSON_CONFIGURATION` — `CONFIG` is not parseable JSON. | Send a valid, URL-encoded JSON object. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| 8119 | `INVALID_VALUE_FOR_ATTRIBUTE` — `scope` is not exactly `ALL` or `SELECTED`. | Send upper-case `ALL` or `SELECTED`. |
| 8248 | `SANDBOX_NOT_MAPPED_TO_MASTER_WORKSPACE` — One or more `sandboxIds` are not linked to this master. The message names them. | Use sandbox IDs from [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace). |
| 8249 | `INVALID_CONFIGURATION_REMOVE_LINKED_WORKSPACES` — `sandboxIds` was supplied with `scope: "ALL"`, or omitted with `scope: "SELECTED"`. | Send `{"scope":"ALL"}` or `{"scope":"SELECTED","sandboxIds":[…]}`. |
| 8504 | `LESS_THAN_MIN_OCCURANCE` — The `CONFIG` parameter was not sent, or `sandboxIds` is outside its 1–100 bound. | Send `CONFIG` as a URL-encoded form body on the `DELETE` request. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.delete`. |

---

## Appendix A – Common HTTP Headers

| Header | Value | Required | Description |
|--------|-------|----------|-------------|
| `Authorization` | `Zoho-oauthtoken <oauth-token>` | **Mandatory** | OAuth 2.0 access token of the calling user. Must carry the scope matching the operation (see [Appendix B](#appendix-b--oauth-scope-summary)). |
| `ZANALYTICS-ORGID` | Organization ID string | **Mandatory** | Organization ID that owns the **master** workspace — or, for [Get Linked Workspaces For Organization](#1-get-linked-workspaces-for-organization), the organisation whose masters are listed. Missing header is `8083`. Obtainable from the [Get Org List](../01%20%C2%B7%20Organization%20Management/ORG_INFO_AND_SETTINGS.md#1-get-org-list) response. |
| `Content-Type` | `application/x-www-form-urlencoded` | Conditional | Required by the three APIs that send a `CONFIG` **body**: [Link Workspaces](#5-link-workspaces), [Sync Linked Workspaces](#6-sync-linked-workspaces) and [Unlink Workspaces](#8-unlink-workspaces) — note that the last is a `DELETE` **with** a body. [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility) and [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details) pass `CONFIG` in the query string instead and need no `Content-Type`; the other three read APIs send no payload at all. |
| `Host` | `analyticsapi.zoho.com` (or the DC equivalent) | **Mandatory** | Must be the **standard** Zoho Analytics API host. A request whose host is a Client Portal / White Label custom domain is rejected with `7301` for all eight APIs — see [White Label / Client Portal Behaviour](#white-label--client-portal-behaviour). |

> **`ZANALYTICS-DEST-ORGID` is not used by any API in this document.** Cross-organisation targeting here is expressed inside the payload, through `clients[].orgId`, not through a destination header.
>
> **No API in this document accepts a `workspaceKey` either.** [Copy Workspace](WORKSPACE_OPERATIONS.md#2-copy-workspace) requires the source workspace's secret key to authorise a cross-organisation copy; workspace linking is also a cross-organisation operation but authorises differently — the caller must hold **Account Admin or Organization Admin rights in both organisations**, and there is no key to supply or obtain. See [Permission Model](#permission-model).

`CONFIG` is always a **URL-encoded form parameter** (or query parameter for the two `GET` APIs that take one) — never a raw JSON request body.

Example:

```http
POST /restapi/v2/workspaces/137687000271334001/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG=%7B%22clients%22%3A%5B%7B%22orgId%22%3A700000654321%2C%22workspaceIds%22%3A%5B%22466206000000071000%22%5D%7D%5D%7D
```

---

## Appendix B – OAuth Scope Summary

| API | HTTP Method | Scope |
|-----|-------------|-------|
| Get Linked Workspaces For Organization | GET | `ZohoAnalytics.metadata.read` |
| Get Linked Workspaces For Master Workspace | GET | `ZohoAnalytics.metadata.read` |
| Get Linkable Workspaces | GET | `ZohoAnalytics.metadata.read` |
| Get Workspace Linking Compatibility | GET | `ZohoAnalytics.metadata.read` |
| Link Workspaces | POST | `ZohoAnalytics.modeling.create` |
| Sync Linked Workspaces | POST | `ZohoAnalytics.modeling.create` |
| Get Linked Workspace Sync Details | GET | `ZohoAnalytics.metadata.read` |
| Unlink Workspaces | DELETE | `ZohoAnalytics.modeling.delete` |

> This family **spans two scope groups**: the five read APIs use `metadata.read` and the three write APIs use `modeling.*`. An integration that discovers and manages links therefore needs `ZohoAnalytics.metadata.read` **plus** `ZohoAnalytics.modeling.create` and `ZohoAnalytics.modeling.delete` — a token holding only `modeling` cannot discover a `workspaceId` or a `sandboxId`, and a token holding only `metadata` is read-only. Note that **[Sync Linked Workspaces](#6-sync-linked-workspaces) uses `modeling.create`** although it creates nothing: the verb follows the HTTP method, not the effect. A token scoped to `modeling.delete` alone can unlink but cannot sync.
>
> No API in this document uses the `data` scope family — a sync copies workspace **design**, and no endpoint here reads or writes table rows.

---

## Appendix C – API-Specific Notes and Behaviours

### Get Linked Workspaces For Organization

- **The broadest discovery call, and the usual source of `sandboxId`.** Everything except [Get Linkable Workspaces](#3-get-linkable-workspaces) ultimately needs an ID that starts here or in the per-master listing.
- **Scoped to the header organisation.** Only masters owned by `ZANALYTICS-ORGID` are listed; repeat the call per organisation.
- **Filtered, not refused.** Links whose master or client organisation the caller does not administer vanish from the response without comment, so an empty array may mean "none visible" rather than "none exist".
- **Reading deletes stale mappings.** Links pointing at a deleted master or client workspace are purged while the response is built — a `GET` with a persistent side effect.
- **Grouped by master workspace name.** Two masters sharing a display name collapse into one entry; see [Limitations](#limitations).
- **`syncTime` is epoch milliseconds in a string,** `"0"` when the link has never synced.
- **Dependency chain:** [Get Org List](../01%20%C2%B7%20Organization%20Management/ORG_INFO_AND_SETTINGS.md#1-get-org-list) → `ZANALYTICS-ORGID` → Get Linked Workspaces For Organization → `sandboxId`.

### Get Linked Workspaces For Master Workspace

- **Same data, different container.** `data.linkedWorkspaces` is a JSON **object** here and a JSON **array** in the organisation listing. A shared parser must branch.
- **"Not linked" is `{}` and HTTP 200.** An unlinked workspace, a fully filtered result and a workspace that is not a master are indistinguishable. This API never raises `8246`.
- **Same filtering and same housekeeping side effect** as the organisation listing.
- **This is where a freshly created link first becomes visible.** Because [Link Workspaces](#5-link-workspaces) only schedules the work, poll here until the new `sandboxId` appears.
- **Dependency chain:** [Get All Workspace List](WORKSPACE_OPERATIONS.md#6-get-all-workspace-list) → `<workspace-id>` → Get Linked Workspaces For Master Workspace → `sandboxId`.

### Get Linkable Workspaces

- **The only catalogue of link candidates.** `clients[].workspaceIds` is not validated against any other list, so driving the picker from here is what keeps [Link Workspaces](#5-link-workspaces) from failing late.
- **Eligible is not the same as compatible.** This call excludes workspaces that are already a master, already a client, or already scheduled to link. Design-level fitness is [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility)'s job.
- **The response key is `orgs`; the request key is `clients`.** The two shapes deliberately do not mirror each other — map `orgs[].orgId` → `clients[].orgId` and `orgs[].workspaces[].workspaceId` → `clients[].workspaceIds[]`.
- **Candidates span every organisation the caller administers,** which is what makes cross-organisation linking possible at all.
- **`orgId` can be `""`.** When the server could not resolve an organisation ID it returns the organisation name as the grouping key and leaves `orgId` empty; such an entry cannot be used in a write payload.
- **Dependency chain:** [Get All Workspace List](WORKSPACE_OPERATIONS.md#6-get-all-workspace-list) → Get Linkable Workspaces → [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility).

### Get Workspace Linking Compatibility

- **A dry run of exactly what [Link Workspaces](#5-link-workspaces) enforces.** The linking API calls this same routine and refuses the whole request if any candidate fails, so running it first turns an all-or-nothing rejection into a per-workspace report.
- **Incompatibility is a `200`.** Only request-level problems produce a failure envelope. Branch on `isCompatible`.
- **Three result shapes, not two.** Compatible (`error: null`, `entities` populated but empty); blocked at workspace level (`error` = reason, **`entities: null`**); blocked by entity conflicts (`error` = `"Some entities have conflicts"`, `entities` populated). Guard before indexing into `entities`.
- **A `warning` does not block.** `isCompatible` reflects the workspace-level verdict, so individual entities can report `warning` on a compatible workspace.
- **Messages are always English.** They are resolved through a fixed `en-US` bundle and do not follow the caller's language — use `status`, not `message`.
- **Workspaces can be missing from the report.** A candidate the validator could not evaluate produces no entry. Match by `workspaceId`, never by position.
- **Entity entries carry no `viewType`.** Unlike [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details), and unlike it the data sources here **do** carry `datasourceId`.
- **Dependency chain:** [Get Linkable Workspaces](#3-get-linkable-workspaces) → Get Workspace Linking Compatibility → [Link Workspaces](#5-link-workspaces).

### Link Workspaces

- **`204` means scheduled.** Compatibility is checked inline; the design push is queued. No sandbox ID exists yet when the response arrives.
- **All-or-nothing.** One incompatible candidate blocks the entire request, and the failure body carries the full report under `data.incompatibleWorkspaces` (`8247`).
- **Already-linked candidates are filtered out before anything else runs.** If that empties the payload the call short-circuits to `204` **without** validating the master or the client organisations — so a `204` is not evidence that the request was well-formed, only that nothing remained to do.
- **Effectively idempotent.** Re-sending a payload whose workspaces are now linked is a silent no-op; there is no duplicate-link error.
- **A workspace cannot be both master and client.** Linking from a workspace that is already somebody's client fails with `8246`.
- **The relationship is one-directional.** The master pushes; nothing flows back from the client.
- **Dependency chain:** [Get Linkable Workspaces](#3-get-linkable-workspaces) → [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility) → Link Workspaces → [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace).

### Sync Linked Workspaces

- **Half the request may run inline and half may be scheduled.** Per-client `scope: "SELECTED"` entries push their `masterViewIds` during the request; `scope: "ALL"` entries and a top-level `scope: "ALL"` are queued. A mixed request that fails midway can therefore be partially applied.
- **`204` says nothing about the outcome.** Read [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details) afterwards for the entity-level result.
- **The top-level `scope` is case-sensitive, the per-client one is not.** `{"scope":"all"}` is `8119`; `clients[].scope: "all"` is accepted. Send upper case everywhere.
- **`ALL` means every link of this master,** resolved from `<workspace-id>` — not every link in the organisation.
- **Views are addressed in the master.** `masterViewIds` are IDs in `<workspace-id>`; client-side IDs are never accepted, and the caller must administer the organisation owning each listed view's workspace.
- **Not idempotent.** Every call pushes again and overwrites client-side drift.
- **Its scope is `modeling.create`,** matching the HTTP method rather than the effect.
- **Dependency chain:** [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace) → `sandboxId` → Sync Linked Workspaces → [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details).

### Get Linked Workspace Sync Details

- **The only entity-level report in the family.** The listing APIs give one `syncStatus` per link; this tells you which table or report failed and why.
- **`pendingEntities.dataSources` is always empty.** Only tables and reports are counted as pending. Do not read it as "no data source changes".
- **Pending work includes deletions.** `hasPendingEntities` turns `true` for created, modified **and** deleted master entities; the `deleted` value of `modifiedStatus` marks the last case.
- **`syncTime` is epoch milliseconds in a string,** `"0"` when the link has never synced — the same representation as the listing APIs, despite what the field name suggests.
- **The entity shape differs from the compatibility API.** Entries here carry `viewType` / `viewTypeId`; data sources here carry **no** `datasourceId`. There it is the other way round.
- **Omit `CONFIG` to ask for everything.** `CONFIG={}` fails the template's required-key check on `sandboxIds`; leaving the parameter off entirely is the supported form.
- **One remote read per sandbox.** Filter with `sandboxIds` on a master with many clients.
- **Dependency chain:** [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace) → `sandboxId` → Get Linked Workspace Sync Details.

### Unlink Workspaces

- **Client workspaces survive.** Only the mapping is removed; the client keeps the last design pushed to it and becomes an ordinary workspace.
- **Validated up front.** Every `sandboxIds` entry is checked before anything is removed, so one bad ID fails the whole call and nothing is unlinked.
- **`ALL` is idempotent; `SELECTED` is not.** Repeating `{"scope":"ALL"}` on a master with no links returns `204`; repeating a `SELECTED` request with the same IDs fails with `8248`.
- **Nothing is reported per sandbox.** "Unlinked" and "already gone" look identical from the response.
- **`scope` is case-sensitive here,** unlike the per-client `scope` of [Sync Linked Workspaces](#6-sync-linked-workspaces).
- **Relinking starts over.** A new link gets a new sandbox ID and an empty sync history; nothing carries across.
- **Dependency chain:** [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace) → `sandboxId` → Unlink Workspaces.

---

## Appendix D – General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Three of eight APIs return 204 with no body** | [Link Workspaces](#5-link-workspaces), [Sync Linked Workspaces](#6-sync-linked-workspaces) and [Unlink Workspaces](#8-unlink-workspaces) return HTTP **204 No Content** on success — treat the status code as the success indicator and never expect a JSON body. The other five return the standard `{"status", "summary", "data"}` envelope with HTTP 200. |
| **Nothing is echoed by the write APIs** | None of the three returns the sandbox IDs it created, synced or removed. The authoritative post-write state always comes from a follow-up read. |
| **A `204` means "scheduled", not "done"** | Both write APIs that push design hand the work to a scheduler. Confirm with [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace) or [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details). |
| **Failure responses always carry a body** | Even for the 204 APIs, errors return `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. On failure `summary` is the error's **symbolic name** (e.g. `SANDBOX_NOT_MAPPED_TO_MASTER_WORKSPACE`), not a localised sentence. |
| **One error carries extra data** | `8247` `LINK_WORKSPACES_INCOMPATIBLE_WORKSPACES` adds `data.incompatibleWorkspaces` — the full compatibility report for the blocking workspaces, in the shape of `data.clients` from [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility). Read it instead of re-running the check. |
| **`summary` on success is a localised label** | `"Get linked workspaces for organization"`, `"Get linkable workspaces"`, … It changes with the caller's language, so never branch on it. |
| **All IDs come back as strings** | `workspaceId`, `orgId`, `sandboxId`, `viewId`, `datasourceId` and `syncedByZuId` are JSON **strings** even though the values are numeric. Parse them as strings or longs — never as native JSON numbers — to avoid precision loss. |
| **Request-side typing is not uniform** | The scalar IDs `clients[].orgId` and `clients[].sandboxId` are declared as **Long** and are sent unquoted; the array entries `workspaceIds`, `sandboxIds` and `masterViewIds` are declared as text and are sent as **quoted strings**. Follow the samples rather than assuming one convention for the whole payload. |
| **Two fields are genuine JSON types other than String** | `hasPendingEntities` and `isCompatible` are native booleans; `viewTypeId` is a native number. Everything else in these payloads is a string, an array or an object. |
| **`null` is used deliberately in compatibility responses** | `workspaces[].error` is `null` when the workspace is compatible, and `workspaces[].entities` is `null` when it was blocked for a workspace-level reason. Elsewhere in this family absent data is an empty array or an empty string, not `null`. |
| **Timestamps are epoch milliseconds as strings** | `lastSync.syncTime` is `"1779226560981"`-style in **both** the listing APIs and [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details), and `"0"` when the link has never synced. No API here returns a formatted date. |
| **The container type of `linkedWorkspaces` changes between two APIs** | An array in [Get Linked Workspaces For Organization](#1-get-linked-workspaces-for-organization), a single object in [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace), and `{}` when the master has no visible links. |
| **Three different keys hold the same idea** | The candidate catalogue is `data.orgs`, the compatibility report is `data.clients`, and the sync report is `data.workspaces`. They are not interchangeable and their element shapes differ. |
| **Arrays that are always present** | `data.linkedWorkspaces`, `data.orgs`, `data.clients`, `data.workspaces`, and within them `lastSync.entities.{dataSources,tables,views}` and `pendingEntities.{dataSources,tables,views}` — empty when there is nothing to report. |
| **An empty collection is a success** | An empty `linkedWorkspaces`, `orgs` or `workspaces` array comes back with HTTP 200. Never infer failure from emptiness, and never infer "not linked" from an empty listing without knowing the caller administers every organisation involved. |
| **Per-entity `message` values are always English** | They are resolved through a fixed `en-US` bundle regardless of the caller's locale. Switch on `status`, never on `message`. |
| **No pagination anywhere** | None of the eight APIs accepts `pageNo`, a keyword or a sort parameter. Every result set is returned whole. |
| **Responses are extensible** | Some builds return additional fields. Ignore unrecognised keys rather than validating against a closed schema. |
| **`8246`–`8251` are linked-workspace specific** | Every code in that range is raised only by this family. The `7xxx` and other `8xxx` codes are shared across API families, so match on the `summary` symbolic name as well as `errorCode` when handling errors generically. |

---

## Appendix E – Enum and Value Reference

#### `scope` Values

Used by [Sync Linked Workspaces](#6-sync-linked-workspaces) (top level and per client) and [Unlink Workspaces](#8-unlink-workspaces).

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `ALL` | Operate on everything the server resolves for the master: every linked sandbox, or every eligible entity within one sandbox. | The enumeration attribute that pairs with `SELECTED` must be **omitted**. |
| `SELECTED` | Operate only on what the request enumerates. | The paired attribute (`sandboxIds`, `clients` or `masterViewIds`) is **mandatory** and must be non-empty. |

Case handling differs by position: the **top-level** `scope` on both APIs is compared verbatim and must be upper case (`8119` otherwise), while `clients[].scope` on [Sync Linked Workspaces](#6-sync-linked-workspaces) is upper-cased before comparison. See [The `scope` Attribute](#the-scope-attribute).

#### Sync Status Values

`lastSync.syncStatus`, returned by [Get Linked Workspaces For Organization](#1-get-linked-workspaces-for-organization), [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace) and [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details).

| Value | Meaning |
|-------|---------|
| `success` | The last sync completed without errors. |
| `failure` | The last sync failed. |
| `partialSuccess` | Some entities synced and some did not. The per-entity detail is in [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details). |
| `inProgress` | A sync is currently running. Also what a link reports before its first sync has finished. |
| `unknown` | The stored status code was not one of the four above. |

#### Entity Status Values

`status` on every `dataSources[]`, `tables[]` and `views[]` entry, in both the compatibility and the sync-details responses. Distinct from the response-envelope `status` and from `syncStatus`.

| Value | Meaning |
|-------|---------|
| `success` | The entity is compatible, or synced cleanly. |
| `warning` | The entity needs attention — typically it will be overwritten — but does not block the operation. |
| `failure` | The entity conflicts, or did not sync. |

#### Modified Status Values

`modifiedStatus` on `pendingEntities.tables[]` and `pendingEntities.views[]` in [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details).

| Value | Meaning |
|-------|---------|
| `created` | The entity does not exist on the client yet and will be created by the next sync. |
| `updated` | The entity exists on the client and will be overwritten by the next sync. |
| `deleted` | The entity was removed from the master and the mapping on the client will be removed by the next sync. |

#### View Type Reference

`viewType` and `viewTypeId` appear on `lastSync.entities.tables[]`, `lastSync.entities.views[]`, `pendingEntities.tables[]` and `pendingEntities.views[]` of [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details). `viewType` is the display name and `viewTypeId` the numeric id.

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

## Appendix F – CONFIG Attribute Availability by API

Only five APIs accept CONFIG. `✔` means the attribute is accepted; `—` means it is not part of that API's contract.

| Attribute | [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility) | [Link Workspaces](#5-link-workspaces) | [Sync Linked Workspaces](#6-sync-linked-workspaces) | [Get Linked Workspace Sync Details](#7-get-linked-workspace-sync-details) | [Unlink Workspaces](#8-unlink-workspaces) |
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

`clients` carries different members depending on the API: `orgId` + `workspaceIds` for [Get Workspace Linking Compatibility](#4-get-workspace-linking-compatibility) and [Link Workspaces](#5-link-workspaces), `sandboxId` + `scope` + `masterViewIds` for [Sync Linked Workspaces](#6-sync-linked-workspaces). The two shapes are not interchangeable.

[Get Linked Workspaces For Organization](#1-get-linked-workspaces-for-organization), [Get Linked Workspaces For Master Workspace](#2-get-linked-workspaces-for-master-workspace) and [Get Linkable Workspaces](#3-get-linkable-workspaces) take no CONFIG at all.
