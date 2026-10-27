---
description: Migrating the Zoho Analytics SDKs - Java, Python, C#, Go, PHP, Node.js and Ruby. The method moves off AnalyticsClient, and before-and-after code for each language.
---

# SDK migration

All seven official SDKs changed in the same way. If you understand the shape of the change once, the code is mechanical in every language.

:::sunset
The removed client methods call endpoints that are **deprecated** and switch off in **March 2027**. Upgrading the SDK removes them from your build, which is the fastest way to find every call site.
:::

## 1. The shape of the change

Every SDK has the same five objects:

```text
AnalyticsClient          ← configuration + factories
 ├─ OrgAPI               ← needs an organization             getOrgInstance(orgId)
 ├─ WorkspaceAPI         ← needs an organization + workspace getWorkspaceInstance(orgId, workspaceId)
 ├─ ViewAPI              ← org + workspace + view            getViewInstance(orgId, workspaceId, viewId)
 └─ BulkAPI              ← org + workspace                   getBulkInstance(orgId, workspaceId)
```

Each of `OrgAPI`, `WorkspaceAPI`, `ViewAPI` and `BulkAPI` holds the IDs you gave it and sends `ZANALYTICS-ORGID` on every request automatically. **`AnalyticsClient` holds no organization** — which is exactly why the cross-organization methods used to live on it.

Now that every endpoint needs an organization, there is nothing left for `AnalyticsClient` to call directly:

| ^Before | After |
|---|---|
| `AnalyticsClient` had 10 API methods plus 4 factories | `AnalyticsClient` has **only** configuration and the 4 factories |
| You could call `ac.getWorkspaces()` straight away | You must first choose an organization: `ac.getOrgInstance(orgId)` |

:::good This is the whole migration
Get an `OrgAPI` (or `WorkspaceAPI`) first, then call the method on that. The SDK fills in the header for you.
:::

## 2. The method map

Use this table as your find-and-replace list. `ORG` means an `OrgAPI` instance, `WS` a `WorkspaceAPI` instance.

| ^Old &mdash; on `AnalyticsClient` | New | Returns |
|---|---|---|
| ~~`getOrgs()`~~ | *No replacement.* Read the Organization ID from **Settings → Organisation** | — |
| ~~`getWorkspaces()`~~ | ++`ORG.getOrgWorkspaces()`++ | list of workspaces |
| ~~`getOwnedWorkspaces()`~~ | ++`ORG.getOrgWorkspaces()`++ | list of workspaces |
| ~~`getSharedWorkspaces()`~~ | ++`ORG.getOrgWorkspaces()`++ | list of workspaces |
| ~~`getDashboards()`~~ | ++`ORG.getOrgDashboards(config)`++ | object: `views` + `pageDetails` |
| ~~`getOwnedDashboards()`~~ | ++`ORG.getOrgDashboards(config)`++ | object: `views` + `pageDetails` |
| ~~`getSharedDashboards()`~~ | ++`ORG.getOrgDashboards(config)`++ | object: `views` + `pageDetails` |
| ~~`getRecentViews()`~~ | ++`ORG.getOrgRecentItems()`++ | list of recent items |
| ~~`getWorkspaceDetails(workspaceId)`~~ | ++`WS.getWorkspaceDetails(config)`++ | workspace object |
| ~~`getViewDetails(viewId, config)`~~ | ++`ORG.getViewDetails(viewId, config)`++ | view object |

Method names follow each language's convention: `getOrgWorkspaces` in Java, C#, Go, PHP and Node.js; `get_org_workspaces` in Python and Ruby.

### getWorkspaceDetails moves to WorkspaceAPI

Note the dropped argument. A `WorkspaceAPI` instance **already holds the workspace ID**, so passing it again would be redundant:

```text
Before:  ac.getWorkspaceDetails(workspaceId)
After:   ac.getWorkspaceInstance(orgId, workspaceId).getWorkspaceDetails(config)
                                 ^^^^^^^^^^^^^^^^^                      ^^^^^^
                                 IDs go here now            optional, withUserRoleInfo
```

The `config` argument is new on this method and optional. Pass `null` (or `{}` / `None`) if you do not need `withUserRoleInfo`.

### getViewDetails moves to OrgAPI

The signature is unchanged — only the object you call it on:

```text
Before:  ac.getViewDetails(viewId, config)
After:   ac.getOrgInstance(orgId).getViewDetails(viewId, config)
```

It lives on `OrgAPI` rather than `ViewAPI` because the endpoint resolves a view from the organization alone — there is no workspace in its URL, and a `ViewAPI` instance would demand one.

## 3. Java

**Before**

```java
AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);

JSONArray  orgs       = ac.getOrgs();
JSONObject workspaces = ac.getWorkspaces();       // ownedWorkspaces + sharedWorkspaces
JSONArray  owned      = ac.getOwnedWorkspaces();
JSONObject dashboards = ac.getDashboards();       // ownedViews + sharedViews
JSONArray  recent     = ac.getRecentViews();
JSONObject ws         = ac.getWorkspaceDetails(workspaceId);
JSONObject view       = ac.getViewDetails(viewId, null);
```

**After**

```java
AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);

long orgId = 700000123456L;                       // from configuration
OrgAPI org = ac.getOrgInstance(orgId);

JSONArray  workspaces = org.getOrgWorkspaces();   // one flat array

JSONObject config = new JSONObject();
config.put("recordsPerPage", 100);
JSONObject dashboards = org.getOrgDashboards(config);
JSONArray  views      = dashboards.getJSONArray("views");
boolean    more       = dashboards.getJSONObject("pageDetails").getBoolean("hasNextPage");

JSONArray  recent = org.getOrgRecentItems();
JSONObject view   = org.getViewDetails(viewId, null);

WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
JSONObject   ws        = workspace.getWorkspaceDetails(null);
```

Paging:

```java
JSONArray all = new JSONArray();
int page = 1;
while (true) {
    JSONObject cfg = new JSONObject();
    cfg.put("pageNo", page);
    cfg.put("recordsPerPage", 100);

    JSONObject result = org.getOrgDashboards(cfg);
    JSONArray  batch  = result.getJSONArray("views");
    for (int i = 0; i < batch.length(); i++) {
        all.put(batch.get(i));
    }
    if (!result.getJSONObject("pageDetails").getBoolean("hasNextPage")) {
        break;
    }
    page++;
}
```

## 4. Python

**Before**

```python
ac = AnalyticsClient(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)

orgs       = ac.get_orgs()
workspaces = ac.get_workspaces()        # {"ownedWorkspaces": [...], "sharedWorkspaces": [...]}
owned      = ac.get_owned_workspaces()
dashboards = ac.get_dashboards()        # {"ownedViews": [...], "sharedViews": [...]}
recent     = ac.get_recent_views()
ws         = ac.get_workspace_details(WORKSPACE_ID)
view       = ac.get_view_details(VIEW_ID)
```

**After**

```python
ac = AnalyticsClient(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)

ORG_ID = "700000123456"                 # from configuration
org = ac.get_org_instance(ORG_ID)

workspaces = org.get_org_workspaces()   # a flat list

result     = org.get_org_dashboards({"recordsPerPage": 100})
dashboards = result["views"]
has_more   = result["pageDetails"]["hasNextPage"]

recent = org.get_org_recent_items()
view   = org.get_view_details(VIEW_ID)

workspace = ac.get_workspace_instance(ORG_ID, WORKSPACE_ID)
ws        = workspace.get_workspace_details()
```

Paging:

```python
def all_dashboards(org, **config):
    page = 1
    while True:
        result = org.get_org_dashboards({**config, "pageNo": page})
        yield from result["views"]
        if not result["pageDetails"]["hasNextPage"]:
            return
        page += 1

for dashboard in all_dashboards(org, recordsPerPage=100):
    print(dashboard["viewName"], dashboard["workspaceId"])
```

## 5. C#

**Before**

```csharp
IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);

JsonElement orgs       = ac.GetOrgs();
JsonElement workspaces = ac.GetWorkspaces();
JsonElement dashboards = ac.GetDashboards();
JsonElement recent     = ac.GetRecentViews();
JsonElement ws         = ac.GetWorkspaceDetails(workspaceId);
JsonElement view       = ac.GetViewDetails(viewId, null);
```

**After**

```csharp
IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);

long orgId  = 700000123456;                       // from configuration
IOrgAPI org = ac.GetOrgInstance(orgId);

JsonElement workspaces = org.GetOrgWorkspaces();

var config = new Dictionary<string, object> { { "recordsPerPage", 100 } };
JsonElement result     = org.GetOrgDashboards(config);
JsonElement views      = result.GetProperty("views");
bool        hasNext    = result.GetProperty("pageDetails").GetProperty("hasNextPage").GetBoolean();

JsonElement recent = org.GetOrgRecentItems();
JsonElement view   = org.GetViewDetails(viewId, null);

IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
JsonElement   ws        = workspace.GetWorkspaceDetails(null);
```

:::info The interface changed too
`IAnalyticsClient` no longer declares the ten removed methods; `IOrgAPI` gained four and `IWorkspaceAPI` gained one. If you mock `IAnalyticsClient` in tests, your mocks will need updating — the compiler will tell you where.
:::

## 6. Go

**Before**

```go
ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)

orgs, _       := ac.GetOrgs()
workspaces, _ := ac.GetWorkspaces()
dashboards, _ := ac.GetDashboards()
recent, _     := ac.GetRecentViews()
ws, _         := ac.GetWorkspaceDetails(workspaceId)
view, _       := ac.GetViewDetails(viewId, config)
```

**After**

```go
ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)

orgId := "700000123456"                            // from configuration
org   := ZAnalytics.GetOrgInstance(&ac, orgId)

workspaces, exception := org.GetOrgWorkspaces()
if exception != nil {
    fmt.Println(exception.ErrorMessage)
    return
}

config := map[string]interface{}{"recordsPerPage": 100}
result, exception := org.GetOrgDashboards(config)
if exception != nil {
    fmt.Println(exception.ErrorMessage)
    return
}
views       := result["views"]
pageDetails := result["pageDetails"].(map[string]interface{})
hasNext     := pageDetails["hasNextPage"].(bool)

recent, _ := org.GetOrgRecentItems()
view, _   := org.GetViewDetails(viewId, config)

workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
ws, _     := workspace.GetWorkspaceDetails(map[string]interface{}{})
```

## 7. PHP

**Before**

```php
$ac = new AnalyticsClient($client_id, $client_secret, $refresh_token);

$orgs       = $ac->getOrgs();
$workspaces = $ac->getWorkspaces();
$dashboards = $ac->getDashboards();
$recent     = $ac->getRecentViews();
$ws         = $ac->getWorkspaceDetails($workspace_id);
$view       = $ac->getViewDetails($view_id, NULL);
```

**After**

```php
$ac = new AnalyticsClient($client_id, $client_secret, $refresh_token);

$org_id = "700000123456";                          // from configuration
$org    = $ac->getOrgInstance($org_id);

$workspaces = $org->getOrgWorkspaces();

$result     = $org->getOrgDashboards(array("recordsPerPage" => 100));
$dashboards = $result["views"];
$has_next   = $result["pageDetails"]["hasNextPage"];

$recent = $org->getOrgRecentItems();
$view   = $org->getViewDetails($view_id, NULL);

$workspace = $ac->getWorkspaceInstance($org_id, $workspace_id);
$ws        = $workspace->getWorkspaceDetails();
```

## 8. Node.js

**Before**

```javascript
var ac = new analyticsClient(clientId, clientSecret, refreshToken);

var orgs       = await ac.getOrgs();
var workspaces = await ac.getWorkspaces();
var dashboards = await ac.getDashboards();
var recent     = await ac.getRecentViews();
var ws         = await ac.getWorkspaceDetails(workspaceId);
var view       = await ac.getViewDetails(viewId, {});
```

**After**

```javascript
var ac = new analyticsClient(clientId, clientSecret, refreshToken);

var orgId = '700000123456';                        // from configuration
var org   = ac.getOrgInstance(orgId);

var workspaces = await org.getOrgWorkspaces();

var result     = await org.getOrgDashboards({ recordsPerPage: 100 });
var dashboards = result.views;
var hasNext    = result.pageDetails.hasNextPage;

var recent = await org.getOrgRecentItems();
var view   = await org.getViewDetails(viewId, {});

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
var ws        = await workspace.getWorkspaceDetails({});
```

Paging:

```javascript
async function allDashboards(org, config) {
    var out = [];
    var page = 1;
    for (;;) {
        var result = await org.getOrgDashboards(Object.assign({}, config, { pageNo: page }));
        out = out.concat(result.views);
        if (!result.pageDetails.hasNextPage) { return out; }
        page++;
    }
}
```

## 9. Ruby

**Before**

```ruby
ac = AnalyticsClient.new.with_data_center("US").with_oauth(creds).build

orgs       = ac.get_orgs
workspaces = ac.get_workspaces
dashboards = ac.get_dashboards
recent     = ac.get_recent_views
ws         = ac.get_workspace_details(WORKSPACE_ID)
view       = ac.get_view_details(VIEW_ID)
```

**After**

```ruby
ac = AnalyticsClient.new.with_data_center("US").with_oauth(creds).build

ORG_ID = "700000123456"                            # from configuration
org    = ac.get_org_instance(ORG_ID)

workspaces = org.get_org_workspaces

result     = org.get_org_dashboards({ "recordsPerPage" => 100 })
dashboards = result["views"]
has_next   = result["pageDetails"]["hasNextPage"]

recent = org.get_org_recent_items
view   = org.get_view_details(VIEW_ID)

workspace = ac.get_workspace_instance(ORG_ID, WORKSPACE_ID)
ws        = workspace.get_workspace_details
```

## 10. Errors your build will throw, and what they mean

| ^Language | Message you will see | Fix |
|---|---|---|
| Java | `cannot find symbol: method getWorkspaces()` | `ac.getOrgInstance(orgId).getOrgWorkspaces()` |
| C# | `'IAnalyticsClient' does not contain a definition for 'GetDashboards'` | `ac.GetOrgInstance(orgId).GetOrgDashboards(config)` |
| Go | `ac.GetRecentViews undefined (type Client has no field or method GetRecentViews)` | `ZAnalytics.GetOrgInstance(&ac, orgId).GetOrgRecentItems()` |
| Python | `AttributeError: 'AnalyticsClient' object has no attribute 'get_workspaces'` | `ac.get_org_instance(org_id).get_org_workspaces()` |
| Ruby | `NoMethodError: undefined method 'get_orgs'` | No replacement — read the ID from the UI |
| PHP | `Call to undefined method AnalyticsClient::getDashboards()` | `$ac->getOrgInstance($org_id)->getOrgDashboards($config)` |
| Node.js | `TypeError: ac.getRecentViews is not a function` | `ac.getOrgInstance(orgId).getOrgRecentItems()` |

:::warn One runtime trap the compiler cannot catch
`getOrgDashboards` returns an **object** containing `views` and `pageDetails`, where `getOwnedDashboards` returned an **array**. In Python, Ruby, PHP, Node.js and Go this is a runtime shape change, not a compile error. Search for every place you iterated the old return value directly and add `["views"]`.
:::

## 11. Keeping a single organization ID in one place

Since every call now needs it, put it next to your other connection settings rather than threading it through the call stack:

```python
# config.py
import os

CLIENT_ID     = os.environ["ZOHO_CLIENT_ID"]
CLIENT_SECRET = os.environ["ZOHO_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["ZOHO_REFRESH_TOKEN"]
ORG_ID        = os.environ["ZOHO_ANALYTICS_ORG_ID"]   # Settings → Organisation

# analytics.py
from AnalyticsClient import AnalyticsClient
import config

_client = AnalyticsClient(config.CLIENT_ID, config.CLIENT_SECRET, config.REFRESH_TOKEN)

def org():
    return _client.get_org_instance(config.ORG_ID)

def workspace(workspace_id):
    return _client.get_workspace_instance(config.ORG_ID, workspace_id)
```

Call sites then never mention the organization at all:

```python
import analytics

for ws in analytics.org().get_org_workspaces():
    print(ws["workspaceName"])
```

---

Next: [how your knowledge bases and tools adopt the change](05-knowledge-bases.md).
