---
name: zoho-analytics-v2-artifact-migration
description: Refresh the artefacts that describe the Zoho Analytics v2 API after the organization-context change — OpenAPI specs, the OKF knowledge bundle and its vector index, Postman collections, SDK reference docs, MCP server tool definitions, internal wikis, Deluge scripts and monitoring alerts. Use when a spec, collection, RAG index or agent still offers the removed cross-organization endpoints, or when deciding whether to merge or re-import an updated contract.
---

# Artefact migration — specs, collections, indexes, agents

Code is only half the job. A stale contract does not fail loudly: it quietly
generates a client, autocompletes a request, or answers a developer's question
with an endpoint that stops answering in March 2027.

Per-artefact detail: `../../../05-knowledge-bases.md`. The artefact list as data,
including locations and counts: `../../migration-map.json` under `artifacts`.

## The rule that governs almost all of this

**Replace, do not merge.** Operations were *removed*. Every merge-style update —
Postman's collection merge, an incremental vector re-index, patching your old
spec copy — keeps the deleted entries and leaves the old endpoints discoverable.
Re-import or rebuild from scratch in each case.

## OpenAPI specifications

Source: `v2.0/oas/`. Read by Swagger UI, Redoc, client generators, MCP servers.

Eight operations deleted along with their response schemas; a new
`Org Level Listings` tag in `org-management-grouped-api.json` with
`getOrgWorkspaces`, `getOrgDashboards`, `getOrgRecentItems`. The
`org-id-optional` parameter is gone — every `ZANALYTICS-ORGID` is now
`"required": true`.

1. Pull the current specs whole. Do not patch the old copy.
2. Regenerate everything downstream: typed clients, request validators, gateway
   definitions, mock servers, contract tests.
3. Confirm the generated client compiles — removed operations become removed
   methods.

> Typed clients (TypeScript, Java) fail to compile, which is what you want.
> **Dynamic-language clients do not.** A Python or Ruby wrapper will keep a
> hand-written method pointing at a dead path. Grep the wrapper too.

## OKF knowledge bundle

Source: `v2.0/okf/`. Read by AI assistants, RAG indexes, `llms.txt` consumers.
Version `1.7.0` → **`2.0.0`**; 210 → **205** endpoint documents; 39 → **40** groups.

1. Re-ingest the whole bundle. Replace it — the major version bump is the signal.
2. **Drop the vector index and rebuild it from scratch.** This matters more than
   it sounds.
3. Confirm `okf/manifest.json` reports `"version": "2.0.0"` after ingestion.

```bash
# Prove the old endpoints are gone from the ingested copy — no output is correct
grep -rl "restapi/v2/recentviews\|dashboards/owned\|workspaces/owned" /path/to/okf/copy
```

> An incremental re-index adds the three new documents and leaves the eight
> deleted ones in place. A retrieval query for "list workspaces" then surfaces a
> dead endpoint **with high confidence**, because the old document is well
> written and matches well. Users trust it, write the code, and ship an
> integration that breaks in March 2027. RAG indexes are the worst offender in
> this entire migration.

## Postman

Source: `v2.0/postman/`. 210 → **205** requests. New folder
**🏢 Organization Management › Org-Level Listings** with three requests.

1. Import as a **new version**. Postman's merge keeps deleted requests.
2. Re-import the environment file too.
3. Set `organization-id` by hand from **Settings → Organisation** — the old
   bootstrap step (*run Get Org List, copy `orgId`*) no longer exists.
4. Delete the old fork, or rename it `DEPRECATED — do not use`. Someone on the
   team has it starred.
5. If it runs in CI, re-record expected responses — the dashboard listing now
   returns `pageDetails`, which the assertions have never seen.

## SDK reference documentation

Source: `v2.0/sdk/<lang>/docs/`, generated from doc comments in `<lang>/source/`.
`reference/analytics-client.md` lost ten methods, `reference/org-api.md` gained
four, `reference/workspace-api.md` gained one, and the first-call example on
every getting-started page now creates an `OrgAPI` first.

Re-publish from source if you mirror these internally. If you ship a wrapper
library, update its README with the same before-and-after — your users read your
docs, not Zoho's.

## MCP servers and AI agents

Tool definitions are a contract like any other.

| Check | Action |
|---|---|
| Tool list | Remove tools backed by the eight removed endpoints. Add three: org workspaces, org dashboards, org recent items |
| Tool schemas | `ZANALYTICS-ORGID` must be a **required** input on every tool, not optional |
| Org selection | Decide once: pin the server to one organization at start-up, or make `orgId` required on every tool. **Pinning is simpler and safer** |
| Pagination | The dashboard tool returns `pageDetails`. Either loop internally and return the full list, or expose `pageNo` and describe `hasNextPage` so the model knows to continue |
| Tool descriptions | Rewrite anything saying "across all organizations" — that phrasing makes a model reach for the wrong tool |
| Error handling | Map `8083` and `8084` to an actionable message |

> `8083` means the header is missing — a retry will never fix it. An agent that
> sees a bare `8083` retries the identical request forever. Translate it in the
> tool's error path to something like *"This API needs an organization ID. Ask
> the user which organization to use."*

## Internal wikis, runbooks, onboarding guides

Nothing automated finds these. Budget an hour. Search for the eight paths, the
SDK method names in both casings, and the old operation titles ("Get Org List",
"Get All Dashboards", "Get Owned", "Get Shared"). The complete search list is in
`../../../05-knowledge-bases.md`, and `agent/scan.py` will find them in anything
stored as files.

**Onboarding guides are the worst case.** A new developer following "step 1: call
`GET /restapi/v2/orgs` to find your org ID" is stuck on their first morning.

## Deluge and no-code automations

Zoho Creator, Zoho Flow and CRM functions call the API through `invokeurl` with
hand-written headers — no compiler, no type check. Two changes per script: the
**URL**, and a **`headers` line** carrying `ZANALYTICS-ORGID`.

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
```

Scripts already scoped to one workspace probably send the header already — check,
do not assume.

## Monitoring — how you prove it is finished

Add a log-based alert on any outbound request matching the eight deprecated
paths, alerting on count greater than zero. Tag it with the owning team so a hit
routes to someone who can fix it. The regex list is in `migration-map.json` under
`scan_patterns.monitoring_regex`.

> **Done means zero for a full billing cycle** — including month-end and
> quarter-end reporting. Monthly and quarterly jobs are the ones everyone
> forgets. Do not close the migration ticket on a quiet week.

## Checklist

`../../../05-knowledge-bases.md` ends with a sixteen-line per-artefact checklist.
Offer it when the user is coordinating this across teams rather than fixing one
artefact.
