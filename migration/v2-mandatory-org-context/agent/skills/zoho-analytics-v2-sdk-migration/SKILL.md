---
name: zoho-analytics-v2-sdk-migration
description: Fix Zoho Analytics SDK code after the methods moved off AnalyticsClient onto OrgAPI and WorkspaceAPI, in Java, Python, C#, Go, PHP, Node.js and Ruby. Use for build errors such as cannot find symbol getWorkspaces, AttributeError get_workspaces, NoMethodError get_orgs, ac.GetRecentViews undefined, Call to undefined method getDashboards, or TypeError ac.getRecentViews is not a function, and when getOrgDashboards returns an object where the old method returned an array.
---

# SDK migration — all seven languages

All seven official SDKs changed the same way. Understand the shape once and the
code is mechanical in every language.

Exact per-language before/after code is in `../../../04-sdk-migration.md`.
The method map as data, including snake_case variants, is in
`../../migration-map.json` under `sdk`.

## The shape of the change

`AnalyticsClient` now holds **only configuration and its four factories**. It has
no organization, which is exactly why the cross-organization methods used to live
on it — and why they cannot stay now that every endpoint needs one.

```
AnalyticsClient
 ├─ OrgAPI         getOrgInstance(orgId)
 ├─ WorkspaceAPI   getWorkspaceInstance(orgId, workspaceId)
 ├─ ViewAPI        getViewInstance(orgId, workspaceId, viewId)
 └─ BulkAPI        getBulkInstance(orgId, workspaceId)
```

Each instance holds the IDs you gave it and sends `ZANALYTICS-ORGID` on every
request automatically. **Get an `OrgAPI` first, then call the method on it.**
That is the whole migration.

## The method map

`ORG` = an `OrgAPI` instance, `WS` = a `WorkspaceAPI` instance. All ten were on
`AnalyticsClient` before.

| Old | New | Returns |
|---|---|---|
| `getOrgs()` | **No replacement** — read the ID from Settings → Organisation | — |
| `getWorkspaces()` | `ORG.getOrgWorkspaces()` | list |
| `getOwnedWorkspaces()` | `ORG.getOrgWorkspaces()` | list |
| `getSharedWorkspaces()` | `ORG.getOrgWorkspaces()` | list |
| `getDashboards()` | `ORG.getOrgDashboards(config)` | **object**: `views` + `pageDetails` |
| `getOwnedDashboards()` | `ORG.getOrgDashboards(config)` | **object** |
| `getSharedDashboards()` | `ORG.getOrgDashboards(config)` | **object** |
| `getRecentViews()` | `ORG.getOrgRecentItems()` | list |
| `getWorkspaceDetails(workspaceId)` | `WS.getWorkspaceDetails(config)` | workspace object |
| `getViewDetails(viewId, config)` | `ORG.getViewDetails(viewId, config)` | view object |

Naming follows each language: camelCase in Java, C#, Go, PHP and Node.js;
`snake_case` in Python and Ruby (`get_org_workspaces`, `get_org_recent_items`).

**`getWorkspaceDetails` drops its argument** — the `WorkspaceAPI` instance already
holds the workspace ID. The new `config` argument is optional (`withUserRoleInfo`);
pass `null` / `{}` / `None` if unused.

**`getViewDetails` keeps its signature** — only the object changes. It lives on
`OrgAPI` rather than `ViewAPI` because the endpoint resolves a view from the
organization alone; there is no workspace in its URL.

## Translating a build error

| Language | Message | Fix |
|---|---|---|
| Java | `cannot find symbol: method getWorkspaces()` | `ac.getOrgInstance(orgId).getOrgWorkspaces()` |
| C# | `'IAnalyticsClient' does not contain a definition for 'GetDashboards'` | `ac.GetOrgInstance(orgId).GetOrgDashboards(config)` |
| Go | `ac.GetRecentViews undefined` | `ZAnalytics.GetOrgInstance(&ac, orgId).GetOrgRecentItems()` |
| Python | `AttributeError: 'AnalyticsClient' object has no attribute 'get_workspaces'` | `ac.get_org_instance(org_id).get_org_workspaces()` |
| Ruby | `NoMethodError: undefined method 'get_orgs'` | No replacement — read the ID from the UI |
| PHP | `Call to undefined method AnalyticsClient::getDashboards()` | `$ac->getOrgInstance($org_id)->getOrgDashboards($config)` |
| Node.js | `TypeError: ac.getRecentViews is not a function` | `ac.getOrgInstance(orgId).getOrgRecentItems()` |

Upgrading the SDK and letting the build fail is the fastest way to find every
call site in Java, C# and Go.

## The trap the compiler cannot catch

`getOrgDashboards` returns an **object** with `views` and `pageDetails`. The old
`getDashboards` / `getOwnedDashboards` returned an **array**.

In **Python, Ruby, PHP, Node.js and Go this is a runtime shape change, not a
compile error.** Search for every place the old return value was iterated
directly and add `["views"]`. When migrating one of these languages, do this
pass explicitly — the build will not help you.

The listing is also paged. Always loop on `pageDetails.hasNextPage`:

```python
def all_dashboards(org, **config):
    page = 1
    while True:
        result = org.get_org_dashboards({**config, "pageNo": page})
        yield from result["views"]
        if not result["pageDetails"]["hasNextPage"]:
            return
        page += 1
```

Never loop on `len(views) < recordsPerPage` — `hasNextPage` is computed after
duplicates and role-restricted entries are removed, so short pages are normal.

## C# specific

`IAnalyticsClient` no longer declares the ten removed methods; `IOrgAPI` gained
four and `IWorkspaceAPI` gained one. **If tests mock `IAnalyticsClient`, those
mocks need updating** — the compiler will point at each one.

## Where the Organization ID belongs

Every call needs it, so put it with the other connection settings rather than
threading it through the call stack:

```python
# config.py
ORG_ID = os.environ["ZOHO_ANALYTICS_ORG_ID"]   # Settings → Organisation

# analytics.py
def org():
    return _client.get_org_instance(config.ORG_ID)

def workspace(workspace_id):
    return _client.get_workspace_instance(config.ORG_ID, workspace_id)
```

## Serving several organizations

The pattern changes from *discover then fan out* to *configure then fan out*.
Hold a list of organization IDs in configuration and create one `OrgAPI` per
organization. If the product must cover organizations you cannot know in advance,
add an "Add organization" step to the setup flow and ask the user for the ID —
the same way you already ask for a client ID and refresh token. Do not guess IDs.

## Finding the call sites

```bash
python3 agent/scan.py /path/to/their/project
```

`sdk-get-workspace-details` and `sdk-get-view-details` report as **warn**, not
error: they are correct when already called on a `WorkspaceAPI` / `OrgAPI`
instance. Check what the receiver is before changing either.
