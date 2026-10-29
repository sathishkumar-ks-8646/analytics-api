---
description: The old Zoho Analytics v2 API and the new one side by side - URLs, headers, request shapes, response shapes and the fields that moved.
---

# What changed

Ten endpoints are affected: eight replaced, two changed in place. This chapter shows the old shape and the new shape next to each other so you can see the size of the job before you start editing.

:::sunset
Everything in the **Before** column is **deprecated**. Those endpoints answer today and will **stop answering in March 2027**.
:::

## 1. The complete change list

| ^Status | Title | Old | New |
|---|---|---|---|
| <span class="tag tag--removed">replaced</span> | Get Org List | ~~`GET /restapi/v2/orgs`~~ | Zoho Analytics UI → **Settings → Organisation** |
| <span class="tag tag--removed">replaced</span> | Get All Workspace List | ~~`GET /restapi/v2/workspaces`~~ | ++`GET /restapi/v2/orgs/workspaces`++ |
| <span class="tag tag--removed">replaced</span> | Get Owned Workspace List | ~~`GET /restapi/v2/workspaces/owned`~~ | ++`GET /restapi/v2/orgs/workspaces`++ |
| <span class="tag tag--removed">replaced</span> | Get Shared Workspace List | ~~`GET /restapi/v2/workspaces/shared`~~ | ++`GET /restapi/v2/orgs/workspaces`++ |
| <span class="tag tag--removed">replaced</span> | Get All Dashboards | ~~`GET /restapi/v2/dashboards`~~ | ++`GET /restapi/v2/orgs/dashboards`++ |
| <span class="tag tag--removed">replaced</span> | Get Owned Dashboards | ~~`GET /restapi/v2/dashboards/owned`~~ | ++`GET /restapi/v2/orgs/dashboards`++ |
| <span class="tag tag--removed">replaced</span> | Get Shared Dashboards | ~~`GET /restapi/v2/dashboards/shared`~~ | ++`GET /restapi/v2/orgs/dashboards`++ |
| <span class="tag tag--removed">replaced</span> | Get Recent Views | ~~`GET /restapi/v2/recentviews`~~ | ++`GET /restapi/v2/orgs/recentitems`++ |
| <span class="tag tag--changed">changed</span> | Get Workspace Info | `GET /restapi/v2/workspaces/{workspace-id}` | Same URL, header now **mandatory** |
| <span class="tag tag--changed">changed</span> | Get View Details | `GET /restapi/v2/views/{view-id}` | Same URL, header now **mandatory** |

:::info POST /restapi/v2/workspaces is untouched
Only the **GET** on `/restapi/v2/workspaces` is gone. The **POST** on the same path — *Create Workspace* — is unaffected and still works exactly as before. Check the method before you panic about a grep hit.
:::

## 2. Three endpoints replace eight

The old design split one question three ways:

```text
            ┌─ /restapi/v2/workspaces          "all"
workspaces ─┼─ /restapi/v2/workspaces/owned    "mine"
            └─ /restapi/v2/workspaces/shared   "shared with me"

            ┌─ /restapi/v2/dashboards          "all"
dashboards ─┼─ /restapi/v2/dashboards/owned    "mine"
            └─ /restapi/v2/dashboards/shared   "shared with me"
```

Inside one organization that split stops being useful. "Owned" versus "shared" was mostly a statement about *which organization something came from* — and now you have already said that in the header. So the new design is one endpoint per thing:

```text
workspaces  ──  /restapi/v2/orgs/workspaces
dashboards  ──  /restapi/v2/orgs/dashboards
recent      ──  /restapi/v2/orgs/recentitems
```

Each entry in the response still tells you who owns it (`createdBy`) and who shared it with you (`sharedBy`), so no information is lost — it just moved from the URL into the data, which is where it belonged.

## 3. Workspaces, before and after

<div class="ba">
  <div class="ba__old">
    <div class="ba__label">Before &mdash; deprecated</div>
    <div class="ba__body">
      <p>Three endpoints. No header. Results spanned every organization. Owned and shared arrived in two separate arrays.</p>
    </div>
  </div>
  <div class="ba__new">
    <div class="ba__label">After</div>
    <div class="ba__body">
      <p>One endpoint. Mandatory header. One organization. One flat array.</p>
    </div>
  </div>
</div>

**Before**

```http
GET /restapi/v2/workspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

```json
{
  "status": "success",
  "summary": "Get all workspaces",
  "data": {
    "ownedWorkspaces": [
      {
        "workspaceId": "466206000000071000",
        "workspaceName": "Sales Analytics",
        "workspaceDesc": "Sales reporting workspace",
        "orgId": "700000123456",
        "createdTime": "1619175390377",
        "createdBy": "admin@acme.com",
        "isDefault": false
      }
    ],
    "sharedWorkspaces": [
      {
        "workspaceId": "138022000000002015",
        "workspaceName": "Client Portal Data",
        "workspaceDesc": "",
        "orgId": "700000999888",
        "createdTime": "1606987644675",
        "createdBy": "owner@client.com",
        "isDefault": false
      }
    ]
  }
}
```

**After**

```http
GET /restapi/v2/orgs/workspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

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
      },
      {
        "workspaceId": "466206000000071000",
        "workspaceName": "Support Metrics",
        "workspaceDesc": "",
        "orgId": "700000123456",
        "createdTime": "1707286805000",
        "createdBy": "jane.doe@example.com",
        "isDefault": false
      }
    ]
  }
}
```

### What to change in your parsing code

| ^Old | New | Note |
|---|---|---|
| `data.ownedWorkspaces[]` | `data.workspaces[]` | Both old arrays collapse into this one. |
| `data.sharedWorkspaces[]` | `data.workspaces[]` | Use `createdBy` to tell owned from shared, if you still care. |
| per-entry fields | unchanged | `workspaceId`, `workspaceName`, `workspaceDesc`, `orgId`, `createdTime`, `createdBy`, `isDefault` all keep their names and types. |

:::warn `isDefault` means the caller's default, not the organization's
The old reference described `isDefault` on the workspace list as "the organisation's default workspace". That was wrong, and the new reference states it plainly: **`isDefault` is `true` for the calling user's own default workspace.** Two users see different flags on the same workspace. Do not cache it as a property of the workspace.
:::

## 4. Dashboards, before and after

**Before**

```http
GET /restapi/v2/dashboards HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

```json
{
  "status": "success",
  "summary": "Get all dashboards",
  "data": {
    "ownedViews":  [ { "viewId": "466206000000105001", "viewName": "Executive Sales Dashboard" } ],
    "sharedViews": [ { "viewId": "466206000000200010", "viewName": "Finance Overview" } ]
  }
}
```

**After**

```http
GET /restapi/v2/orgs/dashboards?CONFIG=%7B%22recordsPerPage%22%3A50%7D HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

```json
{
  "status": "success",
  "summary": "Get dashboards",
  "data": {
    "views": [
      {
        "viewId": "466206000000106002",
        "viewName": "Support Overview",
        "viewDesc": "Open tickets by priority",
        "viewType": "Dashboard",
        "parentViewId": "",
        "folderId": "466206000000071005",
        "createdTime": "1718361737000",
        "createdBy": "jane.doe@example.com",
        "lastModifiedTime": "1720000000000",
        "lastModifiedBy": "jane.doe@example.com",
        "isFavorite": true,
        "sharedBy": "jane.doe@example.com",
        "workspaceId": "466206000000071000",
        "orgId": "700000123456"
      }
    ],
    "pageDetails": {
      "pageNo": 1,
      "recordsPerPage": 50,
      "hasNextPage": true
    }
  }
}
```

### What to change in your parsing code

| ^Old | New | Note |
|---|---|---|
| `data.ownedViews[]` | `data.views[]` | Collapsed. |
| `data.sharedViews[]` | `data.views[]` | Use `sharedBy` to tell them apart. |
| — | `data.pageDetails` | **New and always present.** You must now page. |
| per-entry fields | unchanged | Same names and types as before. |

### Genuinely new behaviour

This is the one endpoint that gained capability rather than just moving:

| ^Capability | Detail |
|---|---|
| **Paging** | `pageNo` (1–1,000) and `recordsPerPage` (1–500, default 100). The old endpoint returned everything in one response. |
| **Name search** | `searchKey` returns only dashboards whose name contains that text, matched as one phrase, applied *before* paging. Max 100 characters. |
| **Workspace narrowing** | `workspaceIds` scans only the workspaces you name — 0 to 1,000 IDs, 10,000 characters in total. |
| **A scan cap** | If `workspaceIds` is omitted and the caller can see more than 100 workspaces, the request fails with `7476` and asks you to name the workspaces. |
| **Ordering** | Most recently modified first. There is no sort parameter. |

:::warn A short page is not necessarily the last page
`hasNextPage` is computed *after* duplicates and role-restricted entries have been filtered out of the page. So a page can contain fewer than `recordsPerPage` entries and still have more pages behind it. **Keep requesting while `hasNextPage` is `true`.** Do not stop because a page looked short.
:::

## 5. Recent items, before and after

**Before**

```http
GET /restapi/v2/recentviews HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

**After**

```http
GET /restapi/v2/orgs/recentitems HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

```json
{
  "status": "success",
  "summary": "Get recent views",
  "data": {
    "views": [
      {
        "viewId": "466206000000106002",
        "viewName": "Support Overview",
        "viewType": "Dashboard",
        "workspaceId": "466206000000071000",
        "workspaceName": "Support Metrics",
        "viewLastAccessedTime": "1720100000000"
      }
    ]
  }
}
```

The response shape is the same — `data.views[]` with the same six fields. Three things differ:

- Entries are limited to workspaces visible to the caller **in the named organization**. History from your other organizations no longer appears.
- At most **20** entries are returned. There is no paging, no `limit` and no type filter.
- `summary` still reads `"Get recent views"`. Tell the endpoints apart by URL, not by `summary`.

:::warn Recent items are not access-checked at view level
The list is filtered by *workspace* visibility only. An entry can point at a view you can no longer open. Treat `viewId` as a hint and handle a refusal when you actually open it.
:::

## 6. The two endpoints that changed in place

These are **not** removed. Same URL, same response, same fields. The only difference is that `ZANALYTICS-ORGID` went from optional to mandatory.

| ^Endpoint | Was | Is now |
|---|---|---|
| `GET /restapi/v2/workspaces/{workspace-id}` | Header optional; the workspace resolved across organizations | Header **mandatory**; the workspace is resolved inside the named organization |
| `GET /restapi/v2/views/{view-id}` | Header optional; the view resolved across organizations | Header **mandatory**; the view is resolved inside the named organization |

**Before**

```http
GET /restapi/v2/views/137687000000471835 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

**After**

```http
GET /restapi/v2/views/137687000000471835 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

Both endpoints gained two error codes, because a required header can now be missing or wrong:

| ^Code | Meaning |
|---|---|
| `8083` | `ZANALYTICS-ORGID` is missing or empty. |
| `8084` | No organization exists with that ID. |

And an existing code changed meaning slightly: `7103` (workspace) and `7104` (view) now also fire when the target exists but belongs to a **different** organization than the one in the header.

:::info In the SDKs these two also moved class, from 2.10.0
`getWorkspaceDetails` moved from `AnalyticsClient` to **`WorkspaceAPI`**, and `getViewDetails` moved from `AnalyticsClient` to **`OrgAPI`**. The HTTP call is the same; only the object you call it on changed, and only from **SDK 2.10.0** onwards. See [chapter 04](04-sdk-migration.md#which-sdk-version-do-i-need).
:::

## 7. What did not change

| ^Area | Status |
|---|---|
| OAuth scopes | Unchanged. All three new endpoints use `ZohoAnalytics.metadata.read`, exactly like the ones they replace. |
| Response envelope | Unchanged: `{"status", "summary", "data"}`, and `{"status":"failure","summary":"<ERROR_NAME>","data":{"errorCode","errorMessage"}}` on failure. |
| IDs and times | Still JSON strings. Times are still epoch milliseconds as strings. Do not parse IDs as 32-bit integers. |
| Data centres | Unchanged. |
| Every workspace-scoped and view-scoped endpoint | Unchanged — they already required the header. |
| `POST /restapi/v2/workspaces` (Create Workspace) | Unchanged. |

---

Next: [endpoint-by-endpoint migration](03-endpoint-migration.md), with the full detail for each one.
