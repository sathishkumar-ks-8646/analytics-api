---
description: One section per affected Zoho Analytics v2 endpoint - full before-and-after requests and responses, field mapping tables, and the behaviour that genuinely differs.
---

# Endpoint migration

The working chapter. Each endpoint gets its own section with the old call, the new call, a field mapping table and the gotchas. Work down the list and tick them off.

:::sunset
Every endpoint in the **Before** blocks on this page is **deprecated** and will be **switched off in March 2027**. The replacements are available now.
:::

## 1. Endpoint index

Type to filter. Every row links to its own section below.

<div class="filterbar">
  <label class="visually-hidden" for="ep-filter">Filter endpoints</label>
  <input type="search" id="ep-filter" placeholder="Filter&hellip;  e.g. dashboards, recent, header" autocomplete="off" spellcheck="false">
  <span class="filterbar__count" id="ep-count"></span>
</div>

<div class="table-wrap">
<table>
<thead><tr><th>Old call</th><th class="col-narrow">Status</th><th>What to do</th></tr></thead>
<tbody>
<tr data-ep><td class="is-old"><code>GET /restapi/v2/orgs</code></td><td><span class="tag tag--removed">replaced</span></td><td><a href="#get-org-list">Read the Organization ID from the UI</a></td></tr>
<tr data-ep><td class="is-old"><code>GET /restapi/v2/workspaces</code></td><td><span class="tag tag--removed">replaced</span></td><td><a href="#the-three-workspace-listings">Use Get Org Workspaces</a></td></tr>
<tr data-ep><td class="is-old"><code>GET /restapi/v2/workspaces/owned</code></td><td><span class="tag tag--removed">replaced</span></td><td><a href="#the-three-workspace-listings">Use Get Org Workspaces</a></td></tr>
<tr data-ep><td class="is-old"><code>GET /restapi/v2/workspaces/shared</code></td><td><span class="tag tag--removed">replaced</span></td><td><a href="#the-three-workspace-listings">Use Get Org Workspaces</a></td></tr>
<tr data-ep><td class="is-old"><code>GET /restapi/v2/dashboards</code></td><td><span class="tag tag--removed">replaced</span></td><td><a href="#the-three-dashboard-listings">Use Get Org Dashboards</a></td></tr>
<tr data-ep><td class="is-old"><code>GET /restapi/v2/dashboards/owned</code></td><td><span class="tag tag--removed">replaced</span></td><td><a href="#the-three-dashboard-listings">Use Get Org Dashboards</a></td></tr>
<tr data-ep><td class="is-old"><code>GET /restapi/v2/dashboards/shared</code></td><td><span class="tag tag--removed">replaced</span></td><td><a href="#the-three-dashboard-listings">Use Get Org Dashboards</a></td></tr>
<tr data-ep><td class="is-old"><code>GET /restapi/v2/recentviews</code></td><td><span class="tag tag--removed">replaced</span></td><td><a href="#get-recent-views">Use Get Org Recent Items</a></td></tr>
<tr data-ep><td><code>GET /restapi/v2/workspaces/{workspace-id}</code></td><td><span class="tag tag--changed">changed</span></td><td><a href="#get-workspace-info">Add the header</a></td></tr>
<tr data-ep><td><code>GET /restapi/v2/views/{view-id}</code></td><td><span class="tag tag--changed">changed</span></td><td><a href="#get-view-details">Add the header</a></td></tr>
<tr data-ep><td><code>POST /restapi/v2/workspaces</code></td><td><span class="tag tag--info">unchanged</span></td><td>Create Workspace is not affected &mdash; no action</td></tr>
</tbody>
</table>
</div>

<p class="empty-msg" id="ep-empty" hidden>No endpoint matches that filter.</p>

## 2. Get Org List

:::sunset
`GET /restapi/v2/orgs` is **deprecated** and switches off in **March 2027**. There is no API replacement — this is the one change that moves a step out of code and into configuration.
:::

**Before**

```http
GET /restapi/v2/orgs HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

```json
{
  "status": "success",
  "summary": "Get organizations",
  "data": {
    "orgs": [
      {
        "orgId": "64036181",
        "orgName": "acme-analytics",
        "orgDesc": "",
        "createdBy": "admin@acme.com",
        "createdByZuId": "64035928",
        "planName": "Enterprise",
        "isDefault": true,
        "numberOfWorkspaces": 41,
        "role": "Account Admin"
      }
    ]
  }
}
```

**After** — there is no call. Read the Organization ID once from **Settings → Organisation** in the Zoho Analytics UI and put it in your configuration:

```bash
# .env, a secret manager, a config file — wherever your other connection settings live
ZOHO_ANALYTICS_ORG_ID=700000123456
```

### Why this one has no API replacement

Everything `GET /restapi/v2/orgs` returned was either *discovery* (which organizations exist for me) or *metadata about an organization* (plan, workspace count, my role). Discovery is the part that is going away: the whole point of the change is that your application states its organization rather than discovering one. The metadata is still available, organization-scoped:

| ^Old field | Where to get it now |
|---|---|
| `orgId` | Configuration, read once from **Settings → Organisation** |
| `orgName`, `orgDesc` | Zoho Analytics UI → **Settings → Organisation** |
| `planName` | `GET /restapi/v2/subscription` (needs the header) |
| `numberOfWorkspaces` | Count `data.workspaces` from `GET /restapi/v2/orgs/workspaces`, or `GET /restapi/v2/resources` |
| `role` | `GET /restapi/v2/workspaces/{workspace-id}` with `CONFIG={"withUserRoleInfo":true}` |
| `isDefault` | No equivalent. It described which organization was *your* default; your application now decides. |

### Recipe: I used to list across every organization

Some products legitimately serve users who work in several organizations — a consultancy dashboard, a backup tool, an internal admin console. The pattern changes from *discover then fan out* to *configure then fan out*:

```text
Before:  orgs = GET /restapi/v2/orgs
         for each org: GET /restapi/v2/workspaces   ← actually returned ALL orgs anyway

After:   orgs = <the list of organization IDs your app is configured with>
         for each orgId:
             GET /restapi/v2/orgs/workspaces   with ZANALYTICS-ORGID: orgId
```

```python
# After — explicit fan-out over organizations you have been configured with
ORG_IDS = ["700000123456", "700000999888"]   # from config, not from an API call

all_workspaces = []
for org_id in ORG_IDS:
    org = ac.get_org_instance(org_id)
    for ws in org.get_org_workspaces():
        ws["sourceOrgId"] = org_id       # keep track of where each row came from
        all_workspaces.append(ws)
```

This is more code than before, and that is deliberate: the fan-out is now visible, bounded and auditable instead of implicit.

:::warn Let the user add organizations, do not guess them
If your product needs to cover organizations you cannot know in advance, add an "Add organization" step to your setup flow and ask the user for the Organization ID — the same way you already ask for a client ID and refresh token.
:::

## 3. The three workspace listings

:::sunset
`GET /restapi/v2/workspaces`, `GET /restapi/v2/workspaces/owned` and `GET /restapi/v2/workspaces/shared` are all **deprecated** and switch off in **March 2027**. All three become one call.
:::

| ^Old | New |
|---|---|
| ~~`GET /restapi/v2/workspaces`~~ | ++`GET /restapi/v2/orgs/workspaces`++ |
| ~~`GET /restapi/v2/workspaces/owned`~~ | ++`GET /restapi/v2/orgs/workspaces`++ |
| ~~`GET /restapi/v2/workspaces/shared`~~ | ++`GET /restapi/v2/orgs/workspaces`++ |

### The new call

```http
GET /restapi/v2/orgs/workspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

| ^Attribute | Value |
|---|---|
| Method | `GET` |
| URL | `/restapi/v2/orgs/workspaces` |
| OAuth scope | `ZohoAnalytics.metadata.read` |
| `ZANALYTICS-ORGID` | **Mandatory** |
| CONFIG | None — this endpoint takes no parameters |
| Permission | Any active user of the organization |
| API units | 0.1 |

```json
{
  "status": "success",
  "summary": "Get org workspaces",
  "data": {
    "workspaces": [
      {
        "workspaceId": "137687000271334001",
        "workspaceName": "Sales Analysis",
        "workspaceDesc": "Quarterly sales dashboards",
        "orgId": "700000123456",
        "createdTime": "1718361737000",
        "createdBy": "jane.doe@example.com",
        "isDefault": true
      }
    ]
  }
}
```

### Field mapping

| ^Old location | New location | Change |
|---|---|---|
| `data.ownedWorkspaces[]` | `data.workspaces[]` | Merged |
| `data.sharedWorkspaces[]` | `data.workspaces[]` | Merged |
| `data.workspaces[]` *(owned / shared endpoints)* | `data.workspaces[]` | Same key, same shape |
| `…[].workspaceId` | same | — |
| `…[].workspaceName` | same | — |
| `…[].workspaceDesc` | same | — |
| `…[].orgId` | same | Always equals the header you sent |
| `…[].createdTime` | same | Epoch ms as a string |
| `…[].createdBy` | same | Omitted when no address can be resolved |
| `…[].isDefault` | same | **Meaning clarified** — the *caller's* default workspace |

### Rebuilding "owned" and "shared"

If your UI really does need the two buckets, derive them from the data:

```python
me = "jane.doe@example.com"
workspaces = org.get_org_workspaces()

owned  = [w for w in workspaces if w.get("createdBy") == me]
shared = [w for w in workspaces if w.get("createdBy") != me]
```

In most cases you will find you no longer want the split: within one organization an admin sees everything anyway, and for everyone else "shared with me" *is* the whole list.

### Behaviour worth knowing

| ^Aspect | Detail |
|---|---|
| Who sees what | Account Admins and Organization Admins get every active workspace in the organization. Everyone else gets only the workspaces shared with them. |
| Unverified email | An Organization Admin or ordinary user whose primary email address is not verified gets an **empty list**. This does not apply to the Account Admin. |
| Order | Newest created first. No sort parameter. |
| Paging | None. The whole list comes back in one response. |
| Empty list | Valid. HTTP 200 with `"workspaces": []` means "nothing visible to this caller". |
| Client Portal / White Label | Allowed. The list holds only the workspaces enabled for that domain. |

### Errors

| ^Code | Meaning | Fix |
|---|---|---|
| `7301` | The caller is not an active user of that organization | Use an organization the user belongs to, or have an Account Admin add them |
| `8083` | `ZANALYTICS-ORGID` missing or empty | Send the header |
| `8084` | No organization with that ID | Re-read the ID from **Settings → Organisation** |
| `8535` | Invalid or expired OAuth token | Refresh the token; needs `ZohoAnalytics.metadata.read` |

## 4. The three dashboard listings

:::sunset
`GET /restapi/v2/dashboards`, `GET /restapi/v2/dashboards/owned` and `GET /restapi/v2/dashboards/shared` are **deprecated** and switch off in **March 2027**.
:::

This is the biggest behavioural change in the migration, because the replacement is **paged**. Code that assumed one request returned everything must be rewritten, not just re-pointed.

### The new call

```http
GET /restapi/v2/orgs/dashboards HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

| ^Attribute | Value |
|---|---|
| Method | `GET` |
| URL | `/restapi/v2/orgs/dashboards` |
| OAuth scope | `ZohoAnalytics.metadata.read` |
| `ZANALYTICS-ORGID` | **Mandatory** |
| CONFIG | Optional, as a URL-encoded query parameter |
| Permission | Any member of the organization. Not available on Client Portal / White Label domains |
| API units | 0.1 |

### CONFIG parameters

| ^Name | Type | Default | Notes |
|---|---|---|---|
| `workspaceIds` | array of string | all visible workspaces | 0–1,000 entries, 10,000 characters total. Duplicates ignored. Every ID must belong to the organization in the header or the whole call fails with `7387`. |
| `pageNo` | integer | `1` | Range 1–1,000. Outside that: `8544`. |
| `recordsPerPage` | integer | `100` | Range 1–500. Outside that: `8544`. |
| `searchKey` | string | none | Name contains this text, matched as one phrase, applied before paging. Max 100 characters. Empty or blank: `8539`. |

CONFIG is JSON, stringified and URL-encoded:

```http
GET /restapi/v2/orgs/dashboards?CONFIG=%7B%22searchKey%22%3A%22Sales%22%2C%22recordsPerPage%22%3A50%7D HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Paging correctly

```python
# After — walk every page, the safe way
org = ac.get_org_instance(ORG_ID)

dashboards = []
page = 1
while True:
    result = org.get_org_dashboards({"pageNo": page, "recordsPerPage": 100})
    dashboards.extend(result["views"])
    if not result["pageDetails"]["hasNextPage"]:
        break
    page += 1
```

:::danger Do not stop on a short page
`hasNextPage` is computed after duplicates and role-restricted entries have been removed from the page. A page can legitimately come back with 3 entries when you asked for 100 and still have more pages behind it. **Loop on `hasNextPage`, never on `len(views) < recordsPerPage`.**
:::

### Field mapping

| ^Old location | New location | Change |
|---|---|---|
| `data.ownedViews[]` | `data.views[]` | Merged |
| `data.sharedViews[]` | `data.views[]` | Merged |
| `data.views[]` *(owned / shared endpoints)* | `data.views[]` | Same key |
| — | `data.pageDetails.pageNo` | **New** |
| — | `data.pageDetails.recordsPerPage` | **New** |
| — | `data.pageDetails.hasNextPage` | **New** — drives your loop |
| `…[].viewId`, `viewName`, `viewDesc`, `viewType` | same | — |
| `…[].parentViewId`, `folderId` | same | `folderId` is the string `"null"` when the dashboard is in no folder |
| `…[].createdTime`, `createdBy` | same | `createdBy` is `""` when the caller is not an active user of the owning organization |
| `…[].lastModifiedTime`, `lastModifiedBy` | same | — |
| `…[].isFavorite` | same | Belongs to the **caller**, not the dashboard |
| `…[].sharedBy` | same | Omitted when no address can be resolved |
| `…[].workspaceId`, `orgId` | same | — |

### The 100-workspace cap

If you omit `workspaceIds`, the server first counts the workspaces the caller can see. More than 100 and the call fails:

```json
{
  "status": "failure",
  "summary": "ORG_LEVEL_VIEWS_WS_MORE_THAN_ALLOWED_LIMIT",
  "data": {
    "errorCode": 7476,
    "errorMessage": "Workspace count is more than the allowed limit. Kindly specify the workspace id's to get the views."
  }
}
```

The fix is to name the workspaces yourself, in batches:

```python
# After — list dashboards for a large organization, 100 workspaces at a time
workspaces = org.get_org_workspaces()
ids = [w["workspaceId"] for w in workspaces]

for batch_start in range(0, len(ids), 100):
    batch = ids[batch_start:batch_start + 100]
    page = 1
    while True:
        result = org.get_org_dashboards({"workspaceIds": batch, "pageNo": page})
        handle(result["views"])
        if not result["pageDetails"]["hasNextPage"]:
            break
        page += 1
```

:::warn `workspaceIds` is validated, not filtered
A workspace ID that belongs to another organization, or does not exist, fails the **whole request** with `7387`. It is not silently skipped. Build the batch from `Get Org Workspaces` for the same organization and you will never hit this.
:::

### Errors

| ^Code | Meaning | Fix |
|---|---|---|
| `7301` | Not a member of that organization, or the request came through a Client Portal / White Label domain | Call from the standard API host as a member |
| `7387` | A `workspaceIds` entry is not in this organization, or does not exist | Take IDs from Get Org Workspaces for the same organization |
| `7430` | Org-level view listing is switched off for the organization (reported to the Account Admin) | Use the workspace-level APIs, or contact support |
| `7431` | Same, reported to every other caller | Use the workspace-level APIs, or contact your account admin |
| `7476` | More than 100 workspaces in scope | Send `workspaceIds` in batches |
| `8083` / `8084` | Header missing / organization unknown | Send a valid `ZANALYTICS-ORGID` |
| `8507` | `searchKey` > 100 chars, `workspaceIds` > 10,000 chars, or CONFIG > 11,000 chars | Shorten, or send fewer IDs per call |
| `8516` | `pageNo` or `recordsPerPage` is not a number | Send a plain number, not a string |
| `8534` | CONFIG is not valid JSON, or `workspaceIds` is not an array | Fix the JSON and URL-encode it |
| `8539` | A CONFIG value is `null`, empty or blank | Leave the key out instead of sending an empty value |
| `8542` | CONFIG holds a key other than the four documented ones | Remove it |
| `8544` | `pageNo` outside 1–1,000, or `recordsPerPage` outside 1–500 | Use a value in range |
| `8547` | More than 1,000 entries in `workspaceIds` | Send at most 1,000 — in practice no more than 100 |

## 5. Get Recent Views

:::sunset
`GET /restapi/v2/recentviews` is **deprecated** and switches off in **March 2027**.
:::

| ^Old | New |
|---|---|
| ~~`GET /restapi/v2/recentviews`~~ | ++`GET /restapi/v2/orgs/recentitems`++ |

```http
GET /restapi/v2/orgs/recentitems HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

| ^Attribute | Value |
|---|---|
| Method | `GET` |
| URL | `/restapi/v2/orgs/recentitems` |
| OAuth scope | `ZohoAnalytics.metadata.read` |
| `ZANALYTICS-ORGID` | **Mandatory** |
| CONFIG | None |
| Permission | Any active user of the organization. Only the caller's own history |
| API units | **1** — ten times the other two org-level listings |

The response shape is unchanged — `data.views[]` with `viewId`, `viewName`, `viewType`, `workspaceId`, `workspaceName` and `viewLastAccessedTime`. What differs:

| ^Aspect | Detail |
|---|---|
| Scope | Only entries whose workspace is visible to the caller **in the named organization**. |
| Size | At most **20** entries, newest first. No paging, no `limit`, no type filter. |
| Access check | Workspace-level only. An entry can point at a view the caller can no longer open. |
| Names | `viewName` and `workspaceName` come from the stored history record, not a live lookup. They can be stale if something was renamed. |
| `summary` | Still `"Get recent views"`. Tell the endpoints apart by URL. |
| Cost | 1 API unit. If you poll this, budget for it. |

### Errors

| ^Code | Meaning |
|---|---|
| `7301` | The caller is not an active user of that organization |
| `8083` / `8084` | Header missing / organization unknown |
| `8535` | Invalid or expired OAuth token |

## 6. Get Workspace Info

Status: <span class="tag tag--changed">changed</span> — **not removed**. Same URL, same response. The header became mandatory.

**Before**

```http
GET /restapi/v2/workspaces/466206000000071000 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

**After**

```http
GET /restapi/v2/workspaces/466206000000071000 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

| ^What | Before | After |
|---|---|---|
| `ZANALYTICS-ORGID` | Optional | **Mandatory** |
| Resolution | The workspace was found wherever it lived | The workspace is found **inside the named organization** |
| `CONFIG={"withUserRoleInfo":true}` | Supported | Supported, unchanged |
| Response | `data.workspaces` — a single object, not an array | Unchanged |
| New errors | — | `8083` header missing, `8084` organization unknown |
| Changed error | `7103` = workspace not found | `7103` = not found **in this organization** |

:::warn 7103 can now mean "right workspace, wrong organization"
If you get `7103` on a workspace ID that you are certain exists, check the header before you check the ID. The workspace is probably in a different organization than the one you named.
:::

In the SDKs this method moved from `AnalyticsClient` to `WorkspaceAPI` — see [chapter 04](04-sdk-migration.md#getworkspacedetails-moves-to-workspaceapi).

## 7. Get View Details

Status: <span class="tag tag--changed">changed</span> — **not removed**. Same URL, same response. The header became mandatory.

**Before**

```http
GET /restapi/v2/views/137687000000471835 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

**After**

```http
GET /restapi/v2/views/137687000000471835?CONFIG=%7B%22withInvolvedMetaInfo%22%3Atrue%7D HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

| ^What | Before | After |
|---|---|---|
| `ZANALYTICS-ORGID` | Optional ("harmless, recommended for consistency") | **Mandatory** |
| Resolution | The view was resolved globally by ID | The view is resolved **inside the named organization** |
| `CONFIG={"withInvolvedMetaInfo":true}` | Supported | Supported, unchanged |
| Response | `data.views` — a single object | Unchanged |
| New errors | — | `8083` header missing, `8084` organization unknown |
| Changed error | `7104` = view not found | `7104` = not found **in this organization** |

In the SDKs this method moved from `AnalyticsClient` to `OrgAPI` — see [chapter 04](04-sdk-migration.md#getviewdetails-moves-to-orgapi).

:::info Why OrgAPI and not ViewAPI?
`ViewAPI` instances are built from an organization **and a workspace and a view**. This endpoint has no workspace in its URL — it finds the view from the organization alone. `OrgAPI`, which carries exactly an organization, is the honest home for it.
:::

## 8. A migration checklist you can paste into a ticket

```text
[ ] Organization ID read from Settings → Organisation and stored in config
[ ] ZANALYTICS-ORGID added in the shared HTTP client / request builder
[ ] GET /restapi/v2/orgs              → removed, ID now comes from config
[ ] GET /restapi/v2/workspaces        → GET /restapi/v2/orgs/workspaces
[ ] GET /restapi/v2/workspaces/owned  → GET /restapi/v2/orgs/workspaces
[ ] GET /restapi/v2/workspaces/shared → GET /restapi/v2/orgs/workspaces
[ ] ownedWorkspaces + sharedWorkspaces parsing replaced by data.workspaces
[ ] GET /restapi/v2/dashboards        → GET /restapi/v2/orgs/dashboards
[ ] GET /restapi/v2/dashboards/owned  → GET /restapi/v2/orgs/dashboards
[ ] GET /restapi/v2/dashboards/shared → GET /restapi/v2/orgs/dashboards
[ ] ownedViews + sharedViews parsing replaced by data.views
[ ] Dashboard paging loop added, driven by pageDetails.hasNextPage
[ ] 7476 handled — fall back to batched workspaceIds for large organizations
[ ] GET /restapi/v2/recentviews       → GET /restapi/v2/orgs/recentitems
[ ] Recent-items callers tolerate a viewId they can no longer open
[ ] GET /restapi/v2/workspaces/{id}   → header added
[ ] GET /restapi/v2/views/{id}        → header added
[ ] 8083 and 8084 handled wherever the header is now required
[ ] SDK upgraded; getWorkspaceDetails and getViewDetails moved class
[ ] OpenAPI / Postman / OKF / MCP copies re-imported (chapter 05)
```

---

Next: [the same migration, in the SDKs](04-sdk-migration.md).
