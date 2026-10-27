---
description: How each knowledge base and tool adopts the Zoho Analytics organization-context change - OpenAPI specs, the OKF bundle, Postman, SDK docs, MCP servers, AI assistants, wikis and Deluge scripts.
---

# Knowledge bases & tools

Code is only half the job. A stale contract — an OpenAPI file, a Postman collection, an AI assistant's knowledge bundle — will keep telling you and your team that the old endpoints exist, long after they stop answering. This chapter lists every artefact that describes the API and says exactly what to do with each.

:::danger A stale copy is worse than no copy
An out-of-date spec does not fail loudly. It quietly generates a client, autocompletes a request or answers a developer's question with an endpoint that is **deprecated and switches off in March 2027**. Refresh every artefact in this chapter before you consider the migration finished.
:::

## 1. The artefacts, at a glance

| ^Artefact | Where it lives | Who reads it | What to do |
|---|---|---|---|
| OpenAPI 3.1 specifications | `v2.0/oas/` | Swagger UI, Redoc, client generators, MCP servers | Re-pull; regenerate anything generated from it |
| OKF knowledge bundle | `v2.0/okf/` | AI assistants, RAG indexes, `llms.txt` consumers | Re-ingest; **re-index**, do not merge |
| Postman collection | `v2.0/postman/` | Humans, CI smoke tests | Re-import as a new version; delete the old fork |
| SDK reference docs | `v2.0/sdk/<lang>/docs/` | Developers | Re-publish from source |
| Narrative API reference | `v2.0/md/` | Humans, docs site | Already updated in this repo |
| MCP servers | your own / third-party | AI agents | Rebuild tool definitions from the new spec |
| Internal wikis, runbooks | wherever yours live | Everyone | Search and fix by hand — nothing does this for you |
| Deluge scripts, no-code flows | Zoho Creator, Flow, CRM functions | Automations | Search and fix by hand |
| Monitoring and dashboards | your observability stack | On-call | Add alerts on the old paths |

## 2. OpenAPI specifications

**What changed in the spec:**

- A new tag, `Org Level Listings`, inside `org-management-grouped-api.json`, with three operations: `getOrgWorkspaces`, `getOrgDashboards`, `getOrgRecentItems`.
- Eight operations deleted, together with the schemas only they used — `GetOrganizationsResponse`, `OrgList`, `Org`, `GetAllWorkspacesResponse`, `WorkspaceList`, `WorkspaceSummary`, `GetOwnedWorkspacesResponse`, `GetSharedWorkspacesResponse`, `GetDashboardsResponse`, `GetDashboardListResponse`, `DashboardSummary`, `GetRecentViewsResponse`, `RecentView` and friends.
- The `org-id-optional` parameter is gone. Every `ZANALYTICS-ORGID` parameter in every file is now `"required": true`.
- New schemas: `OrgWorkspace`, `OrgWorkspaceList`, `GetOrgWorkspacesResponse`, `GetOrgDashboardsConfig`, `OrgDashboardView`, `OrgDashboardList`, `OrgDashboardPageDetails`, `GetOrgDashboardsResponse`, `OrgRecentItem`, `OrgRecentItemList`, `GetOrgRecentItemsResponse`.

**What to do:**

1. Pull the current specifications. Do not patch your old copy — operations were removed, and a merge will leave them behind.
2. Regenerate anything generated from them: typed clients, request validators, API gateway definitions, mock servers, contract tests.
3. Re-check your generated client compiles. Removed operations become removed methods.

:::warn Generated clients fail silently in dynamic languages
A TypeScript or Java client will not compile against the new spec until you fix the call sites — good. A Python or Ruby client will happily keep an old method in a hand-written wrapper. Grep the wrapper too.
:::

## 3. The OKF knowledge bundle

The OKF bundle in `v2.0/okf/` is the machine-readable knowledge base that AI assistants read: one document per endpoint, plus shared foundations, workflows, an error-code catalog and an `llms.txt` entry point.

**What changed:**

| ^Item | Before | After |
|---|---|---|
| Bundle version | `1.7.0` | **`2.0.0`** — a major bump, because endpoints were removed |
| Endpoint documents | 210 | **205** |
| Groups | 39 | **40** — the new `org-level-listings` group |
| New documents | — | `domains/organization-management/org-level-listings/{get-org-workspaces,get-org-dashboards,get-org-recent-items}.md` |
| Deleted documents | — | `get-organizations.md`, `get-all-workspaces.md`, `get-owned-workspaces.md`, `get-shared-workspaces.md`, `get-dashboards.md`, `get-owned-dashboards.md`, `get-shared-dashboards.md`, `get-recent-views.md` |
| `foundations/identifiers.md` | "Obtain `orgId` from Get Org List" | "Read it from **Settings → Organisation** in the Zoho Analytics UI" |
| `foundations/request-conventions.md` | Described a "user-scoped" category of endpoint | That category no longer exists |
| `workflows/bootstrap-identifiers.md` | Step 1 called Get Org List | Step 1 reads the ID from the UI |

**What to do:**

1. **Re-ingest the whole bundle.** Replace it; do not merge. The major version bump is the signal.
2. **Rebuild your vector index from scratch.** This matters more than it sounds. An incremental re-index adds the three new documents but leaves the eight deleted ones in the index, so a retrieval query for "list workspaces" still surfaces a dead endpoint — with high confidence, because the old document is well written.
3. **Check `okf/manifest.json` reports `"version": "2.0.0"`** after ingestion. That is your proof the swap happened.

```bash
# Prove the old endpoints are really gone from your ingested copy
grep -rl "restapi/v2/recentviews\|dashboards/owned\|workspaces/owned" /path/to/your/okf/copy
# → no output is the correct result
```

:::danger Retrieval-augmented assistants are the worst offenders
A RAG index with both the old and the new documents will confidently recommend `GET /restapi/v2/dashboards` because that document still exists in the index and matches the query well. Users trust the answer, write the code, and ship an integration that breaks in **March 2027**. Drop the index and rebuild it.
:::

## 4. Postman

**What changed:** the collection has 205 requests instead of 210. There is a new folder, **🏢 Organization Management › Org-Level Listings**, with the three new requests. Eight requests are gone. The collection and folder descriptions no longer tell you to run *Get Org List* to populate `organization-id`.

**What to do:**

1. Import the current collection **as a new version**. Do not merge into your existing fork — Postman's merge keeps deleted requests.
2. Re-import the environment file too.
3. Set `organization-id` by hand: Zoho Analytics → **Settings → Organisation**. The old bootstrap step (*run Get Org List, copy `orgId`*) no longer exists.
4. Delete your old fork, or rename it `DEPRECATED — do not use`. Someone on your team has it starred.
5. If you run the collection in CI, re-record expected responses. The dashboard listing now returns `pageDetails`, which your assertions have not seen before.

## 5. SDK reference documentation

Each SDK publishes 13 pages under `v2.0/sdk/<lang>/docs/`, generated from the doc comments in `<lang>/source/`.

**What changed:** `reference/analytics-client.md` lost ten methods. `reference/org-api.md` gained four. `reference/workspace-api.md` gained one. The *first call* example on every "getting started" page now creates an `OrgAPI` first.

**What to do:** if you mirror these docs on an internal developer portal, re-publish them. If you wrote your own wrapper library, update its README with the same before-and-after shown in [chapter 04](04-sdk-migration.md) — your users read your docs, not Zoho's.

## 6. MCP servers and AI agents

If you expose Zoho Analytics to an AI agent through an MCP server, the tool definitions are a contract like any other.

| ^Check | Action |
|---|---|
| Tool list | Remove tools backed by the eight deprecated endpoints. Add three: org workspaces, org dashboards, org recent items. |
| Tool schemas | `ZANALYTICS-ORGID` must be a **required** input on every tool, not optional. |
| Org selection | Decide once: pin the server to a single organization at start-up, or make `orgId` a required argument on every tool. Pinning is simpler and safer. |
| Pagination | The dashboard tool now returns `pageDetails`. Either loop internally and return the full list, or expose `pageNo` and describe `hasNextPage` in the tool description so the model knows to continue. |
| Tool descriptions | Rewrite any description saying "across all organizations". That phrasing will make a model reach for the wrong tool. |
| Error handling | Map `8083` and `8084` to a clear message. An agent that sees a bare `8083` will usually retry the identical request. |

:::warn Agents retry blindly on an unexplained error
`8083` means "you forgot the header" — a retry will never fix it. Translate it in your tool's error path to something actionable, such as *"This API needs an organization ID. Ask the user which organization to use."*
:::

## 7. Internal documentation, wikis and runbooks

Nothing automated will find these. Budget an hour.

Search your wiki, onboarding docs, architecture diagrams, Slack canvases, support macros and README files for:

```text
/restapi/v2/orgs
/restapi/v2/workspaces/owned
/restapi/v2/workspaces/shared
/restapi/v2/dashboards/owned
/restapi/v2/dashboards/shared
/restapi/v2/recentviews
getOrgs            get_orgs
getWorkspaces      get_workspaces
getDashboards      get_dashboards
getRecentViews     get_recent_views
"Get Org List"     "Get All Dashboards"     "Get All Workspace List"
"Get Owned"        "Get Shared"
```

Pay particular attention to **onboarding guides**. A new developer following "step 1: call `GET /restapi/v2/orgs` to find your org ID" will be stuck on their first morning.

## 8. Deluge scripts and no-code automations

Deluge code inside Zoho Creator, Zoho Flow and CRM functions calls the API over `invokeurl` with hand-written headers, so there is no compiler to catch anything.

**Before**

```javascript
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces"
  type :GET
  connection:"analytics_oauth_connection"
];
info response;
```

**After**

```javascript
orgId = "700000123456";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/orgs/workspaces"
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

Two changes on every script: the **URL** and the **`headers` line**. Scripts that already act on a specific workspace probably have the header already — check, do not assume.

## 9. Monitoring: prove you are done

The most useful thing you can do today is make the old endpoints visible, so you discover forgotten callers now rather than in 2027.

1. **Add a log-based alert** on any outbound request whose path matches the eight deprecated routes. Alert on count greater than zero.
2. **Tag the alert with the owning team**, so a hit routes to someone who can fix it.
3. **Watch it fall to zero.** That is your completion criterion — not "we think we got them all".

```text
path =~ "^/restapi/v2/orgs$"
   or path =~ "^/restapi/v2/workspaces$"            # GET only — POST is Create Workspace
   or path =~ "^/restapi/v2/workspaces/(owned|shared)$"
   or path =~ "^/restapi/v2/dashboards$"
   or path =~ "^/restapi/v2/dashboards/(owned|shared)$"
   or path =~ "^/restapi/v2/recentviews$"
```

:::good Done means zero for a full billing cycle
Monthly and quarterly jobs are the ones everyone forgets. Let the alert stay quiet across a complete cycle — including month-end and quarter-end reporting — before you close the migration ticket.
:::

## 10. Per-artefact checklist

```text
[ ] OpenAPI specs re-pulled (not merged)
[ ] Generated clients regenerated and compiling
[ ] Contract tests / mock servers rebuilt
[ ] OKF bundle re-ingested at version 2.0.0
[ ] Vector index DROPPED and rebuilt, not incrementally updated
[ ] Postman collection re-imported as a new version
[ ] Postman environment re-imported; organization-id set from the UI
[ ] Old Postman fork deleted or renamed DEPRECATED
[ ] SDK reference docs re-published on the internal portal
[ ] Wrapper-library README updated
[ ] MCP tool list, schemas and descriptions updated
[ ] MCP: ZANALYTICS-ORGID required, 8083/8084 mapped to a clear message
[ ] Internal wiki / onboarding guides searched and fixed
[ ] Deluge scripts and no-code flows updated (URL + headers line)
[ ] Monitoring alert added on the eight deprecated paths
[ ] Alert quiet for one full billing cycle
```

---

Next: [the deprecation timeline](06-timeline.md) — what happens, and when.
