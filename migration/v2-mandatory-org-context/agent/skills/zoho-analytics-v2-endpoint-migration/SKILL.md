---
name: zoho-analytics-v2-endpoint-migration
description: Rewrite direct HTTP calls to the removed Zoho Analytics REST API v2 cross-organization endpoints. Use when code calls /restapi/v2/orgs, /restapi/v2/workspaces, /restapi/v2/workspaces/owned, /restapi/v2/workspaces/shared, /restapi/v2/dashboards, /restapi/v2/dashboards/owned, /restapi/v2/dashboards/shared or /restapi/v2/recentviews over raw HTTP, when a response parses ownedWorkspaces, sharedWorkspaces, ownedViews or sharedViews, or when adding the ZANALYTICS-ORGID header to existing requests.
---

# Endpoint migration — direct HTTP calls

For code that builds Zoho Analytics requests itself: curl, fetch, `requests`,
an API gateway, a Deluge `invokeurl`. If the user calls through an official SDK,
use `zoho-analytics-v2-sdk-migration` instead.

Exact paths, CONFIG parameters, field mappings and error codes are in
`../../migration-map.json`. Read values from there rather than recalling them.
Full prose with request/response examples: `../../../03-endpoint-migration.md`.

## The mapping

| Old | New |
|---|---|
| `GET /restapi/v2/orgs` | **No endpoint.** Org ID comes from configuration |
| `GET /restapi/v2/workspaces` | `GET /restapi/v2/orgs/workspaces` |
| `GET /restapi/v2/workspaces/owned` | `GET /restapi/v2/orgs/workspaces` |
| `GET /restapi/v2/workspaces/shared` | `GET /restapi/v2/orgs/workspaces` |
| `GET /restapi/v2/dashboards` | `GET /restapi/v2/orgs/dashboards` |
| `GET /restapi/v2/dashboards/owned` | `GET /restapi/v2/orgs/dashboards` |
| `GET /restapi/v2/dashboards/shared` | `GET /restapi/v2/orgs/dashboards` |
| `GET /restapi/v2/recentviews` | `GET /restapi/v2/orgs/recentitems` |

Unchanged URL, header now mandatory: `GET /restapi/v2/workspaces/{workspace-id}`
and `GET /restapi/v2/views/{view-id}`.

**Unaffected: `POST /restapi/v2/workspaces`** (Create Workspace). It shares a path
with a removed `GET`. Always check the verb before you rewrite that path.

## Order of work

1. **Put the Organization ID in configuration.** `ZOHO_ANALYTICS_ORG_ID`, next to
   the client ID and refresh token. Source: UI → **Settings → Organisation**.
2. **Add `ZANALYTICS-ORGID` in the shared request builder**, once. Every endpoint
   needs it now, so a per-call-site change is the wrong shape.
3. **Rewrite the paths** from the table above.
4. **Fix the response parsing** — this is where the real work is, below.
5. **Handle `8083` and `8084`** wherever the header is now required.

## Response parsing — the part that is not a URL change

**Workspaces.** `data.ownedWorkspaces[]` and `data.sharedWorkspaces[]` merge into a
single `data.workspaces[]`. Per-item fields are unchanged. If the UI genuinely
needs the two buckets, derive them client-side by comparing `createdBy` to the
caller — but check whether the split is still wanted: within one organization an
admin sees everything, and for everyone else "shared with me" *is* the whole list.

**Dashboards.** `data.ownedViews[]` and `data.sharedViews[]` merge into
`data.views[]`, and a new `data.pageDetails` appears. This endpoint is **paged**:

```python
dashboards, page = [], 1
while True:
    r = get("/restapi/v2/orgs/dashboards", config={"pageNo": page, "recordsPerPage": 100})
    dashboards.extend(r["data"]["views"])
    if not r["data"]["pageDetails"]["hasNextPage"]:
        break
    page += 1
```

> **Loop on `hasNextPage`, never on page length.** It is computed after duplicates
> and role-restricted entries are removed, so a page can hold 3 entries when you
> asked for 100 and still have more pages behind it.

**Recent items.** Response shape is unchanged — but the list is capped at 20,
scoped to the named organization, and access is checked at workspace level only,
so an entry can point at a view the caller cannot open. Names come from the
stored history record and may be stale. It costs **1 API unit**, ten times the
other two org-level listings; budget for it if you poll.

## The 100-workspace cap

Omitting `workspaceIds` fails with `7476` when the caller can see more than 100
workspaces. Fix by naming the workspaces in batches of at most 100, taken from
`GET /restapi/v2/orgs/workspaces` for the same organization, and paging within
each batch.

`workspaceIds` is **validated, not filtered** — one ID from another organization
fails the whole request with `7387`, it is not silently skipped.

## CONFIG on the dashboard listing

Stringified JSON, URL-encoded, in the `CONFIG` query parameter. Four keys only;
anything else is `8542`. `workspaceIds` (≤1,000 entries, ≤10,000 chars),
`pageNo` (1–1,000), `recordsPerPage` (1–500), `searchKey` (≤100 chars). Limits and
the error code for each are in `migration-map.json` under `config_parameters`.

## Errors to handle

| Code | Means | Do |
|---|---|---|
| `8083` | Header missing or empty | Send it. Never retry unchanged |
| `8084` | No organization with that ID | Re-read from Settings → Organisation |
| `7301` | Caller is not an active user of that organization | Use an org they belong to |
| `7103` / `7104` | Workspace / view not found **in this organization** | Check the header before the ID |
| `7476` | More than 100 workspaces in scope | Batch `workspaceIds` |
| `7387` | A `workspaceIds` entry is not in this organization | Build batches from Get Org Workspaces |
| `7430` / `7431` | Org-level listing switched off for the organization | Use workspace-level APIs, or contact support |

Full table including the eight CONFIG validation codes: `migration-map.json`
under `error_codes`, or `../../../07-troubleshooting.md`.

## Behaviour that is correct but looks like a bug

- **Empty list, HTTP 200.** Valid — nothing is visible to this caller. An
  Organization Admin or ordinary user whose primary email is unverified gets an
  empty list; the Account Admin does not.
- **`isDefault` on a workspace** means the *caller's* default, not the
  organization's.
- **`folderId` is the string `"null"`** when a dashboard is in no folder.
- **`createdBy` is `""`** when the caller is not an active user of the owning org.

## Checklist

`../../../03-endpoint-migration.md` ends with a checklist written to paste into a
ticket. Offer it when the user is tracking this as a work item rather than fixing
one call.
