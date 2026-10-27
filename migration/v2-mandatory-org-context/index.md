---
description: Migration guide for the Zoho Analytics REST API v2 move to mandatory organization context. Eight cross-organization endpoints are replaced by three organization-scoped ones; two more now require the ZANALYTICS-ORGID header.
---

# Start here

Zoho Analytics API v2 used to have a handful of endpoints that answered the question *"what can I see **everywhere**?"*. Those are gone. Every endpoint now answers *"what can I see **in this one organization**?"* — and the organization is named by a header you must send.

:::sunset
The replaced endpoints still answer today, but they are **deprecated**. They are removed from the v2 reference now and they will **stop responding in March 2027**. Any integration still calling them after that date will start failing. Plan the move now, not in 2027.
:::

## 1. Am I affected?

Run this one check against your own code. If any of these strings appear in it, you are affected:

```text
/restapi/v2/orgs                 ← and nothing after "orgs"
/restapi/v2/workspaces           ← only the bare GET, not POST and not /workspaces/{id}/...
/restapi/v2/workspaces/owned
/restapi/v2/workspaces/shared
/restapi/v2/dashboards           ← the bare GET
/restapi/v2/dashboards/owned
/restapi/v2/dashboards/shared
/restapi/v2/recentviews
```

A quick grep over a source tree:

```bash
grep -rnE '/restapi/v2/(orgs|workspaces|dashboards)"?$|/restapi/v2/(workspaces|dashboards)/(owned|shared)|/restapi/v2/recentviews' .
```

If you use one of the official SDKs instead of raw HTTP, grep for the method names:

```bash
grep -rniE 'get(Orgs|Workspaces|OwnedWorkspaces|SharedWorkspaces|RecentViews|Dashboards|OwnedDashboards|SharedDashboards|WorkspaceDetails|ViewDetails)|get_(orgs|workspaces|owned_workspaces|shared_workspaces|recent_views|dashboards|owned_dashboards|shared_dashboards|workspace_details|view_details)' .
```

:::good You are not affected if…
…every call you make already sends `ZANALYTICS-ORGID` and already has a workspace ID or view ID in the URL path. That describes the large majority of the v2 surface — around 200 of the 205 endpoints were already organization-scoped and did not change at all.
:::

## 2. The change in sixty seconds

| ^Status | Old endpoint | New endpoint |
|---|---|---|
| Replaced | ~~`GET /restapi/v2/orgs`~~ | Read the Organization ID from the Zoho Analytics UI |
| Replaced | ~~`GET /restapi/v2/workspaces`~~ | ++`GET /restapi/v2/orgs/workspaces`++ |
| Replaced | ~~`GET /restapi/v2/workspaces/owned`~~ | ++`GET /restapi/v2/orgs/workspaces`++ |
| Replaced | ~~`GET /restapi/v2/workspaces/shared`~~ | ++`GET /restapi/v2/orgs/workspaces`++ |
| Replaced | ~~`GET /restapi/v2/dashboards`~~ | ++`GET /restapi/v2/orgs/dashboards`++ |
| Replaced | ~~`GET /restapi/v2/dashboards/owned`~~ | ++`GET /restapi/v2/orgs/dashboards`++ |
| Replaced | ~~`GET /restapi/v2/dashboards/shared`~~ | ++`GET /restapi/v2/orgs/dashboards`++ |
| Replaced | ~~`GET /restapi/v2/recentviews`~~ | ++`GET /restapi/v2/orgs/recentitems`++ |
| Changed | `GET /restapi/v2/workspaces/{workspace-id}` | Same URL — `ZANALYTICS-ORGID` is now **mandatory** |
| Changed | `GET /restapi/v2/views/{view-id}` | Same URL — `ZANALYTICS-ORGID` is now **mandatory** |

Eight endpoints became three, because the old set split one idea three ways — *all*, *owned* and *shared*. Inside a single organization that split carries no information: the new listing simply returns everything the caller can reach, and each entry already tells you who owns it and who shared it.

## 3. The one rule to remember

:::info The rule
**Every request carries `ZANALYTICS-ORGID`.** No exceptions. If you do not send it you get error `8083`; if you send an ID that does not exist you get `8084`; if you send an organization you are not a member of you get `7301`.
:::

```http
GET /restapi/v2/orgs/workspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

That third header line is the whole migration, repeated across every call you make.

## 4. Read the guide in order

<div class="grid grid--2">
  <a class="panel panel--blue" href="01-why-org-context.html">
    <div class="panel__num">01</div>
    <h3>Why organization context is mandatory</h3>
    <p>What an organization is, what the header does, and the four concrete problems the old cross-organization endpoints caused. Start here if the change feels arbitrary.</p>
    <span class="panel__link">Read chapter 01</span>
  </a>
  <a class="panel panel--red" href="02-whats-changed.html">
    <div class="panel__num">02</div>
    <h3>What changed</h3>
    <p>The old API and the new API side by side: URLs, headers, request shapes, response shapes and the fields that moved or disappeared.</p>
    <span class="panel__link">Read chapter 02</span>
  </a>
  <a class="panel panel--green" href="03-endpoint-migration.html">
    <div class="panel__num">03</div>
    <h3>Endpoint migration</h3>
    <p>One section per endpoint. Full before-and-after requests and responses, a field-by-field mapping table, and the behaviour that is genuinely different.</p>
    <span class="panel__link">Read chapter 03</span>
  </a>
  <a class="panel panel--green" href="04-sdk-migration.html">
    <div class="panel__num">04</div>
    <h3>SDK migration</h3>
    <p>Java, Python, C#, Go, PHP, Node.js and Ruby. The method moves, the new classes to call, and copy-paste before-and-after code for each language.</p>
    <span class="panel__link">Read chapter 04</span>
  </a>
  <a class="panel panel--blue" href="05-knowledge-bases.html">
    <div class="panel__num">05</div>
    <h3>Knowledge bases &amp; tools</h3>
    <p>How the OpenAPI specs, the OKF bundle, Postman, the SDK docs, MCP servers, AI assistants, internal wikis and Deluge scripts each have to adopt the change.</p>
    <span class="panel__link">Read chapter 05</span>
  </a>
  <a class="panel panel--yellow" href="06-timeline.html">
    <div class="panel__num">06</div>
    <h3>Timeline &amp; deprecation</h3>
    <p>What "deprecated" means here, what happens on each date, and how to prove to yourself that nothing in your estate still calls an old endpoint.</p>
    <span class="panel__link">Read chapter 06</span>
  </a>
  <a class="panel panel--red" href="07-troubleshooting.html">
    <div class="panel__num">07</div>
    <h3>Troubleshooting &amp; FAQ</h3>
    <p>Every error code the change can produce, what it means in plain words, and the fix. Plus the questions people ask first.</p>
    <span class="panel__link">Read chapter 07</span>
  </a>
</div>

## 5. What to do this week

1. **Find your Organization ID.**
   Open Zoho Analytics, go to **Settings → Organisation**, and copy the Organization ID. You used to fetch it from `GET /restapi/v2/orgs`; now you read it once and store it in your configuration. See [where to find your Organization ID](01-why-org-context.md#where-to-find-your-organization-id).

2. **Grep for the eight old paths.**
   Use the commands in [section 1](#am-i-affected). Include scheduled jobs, Deluge scripts, notebooks, Postman collections and anything a colleague wrote two years ago.

3. **Add the header everywhere.**
   If you have a shared HTTP client, add `ZANALYTICS-ORGID` once in the place that builds requests. That single edit fixes most of the surface.

4. **Swap the eight endpoints for the three.**
   Follow [chapter 03](03-endpoint-migration.md) one endpoint at a time. The response shapes change, so read the field mapping tables rather than guessing.

5. **Upgrade the SDK, if you use one.**
   Methods moved off `AnalyticsClient` onto `OrgAPI` and `WorkspaceAPI`. Your compiler or interpreter will point at every call site. See [chapter 04](04-sdk-migration.md).

6. **Re-import the contracts your tools depend on.**
   OpenAPI specs, the Postman collection, the OKF bundle your AI assistant reads. A stale copy will keep telling you the old endpoints exist. See [chapter 05](05-knowledge-bases.md).

:::warn Do not wait for the deadline
The old endpoints are deprecated **now**. Treat *"it still works"* as a grace period, not as support. Everything shipped after today should use the new endpoints, and the old ones go dark in **March 2027**.
:::

## 6. Conventions used in this guide

| ^Signal | Meaning |
|---|---|
| <span class="tag tag--removed">removed</span> | The endpoint, field or method is deprecated and will be switched off in March 2027. |
| <span class="tag tag--new">new</span> | The replacement. Use this. |
| <span class="tag tag--changed">changed</span> | Still exists, still at the same URL, but behaves differently. |
| <span class="tag tag--info">unchanged</span> | Shown only so you can confirm you do not need to touch it. |

Code blocks labelled **Before** show the old call. Blocks labelled **After** show the replacement. Where a response shape changes, both are shown in full — the fields are not always where you expect.

Every chapter is also available as plain Markdown: the link is in the left-hand rail under **Source**, or just change `.html` to `.md` in the address bar.
