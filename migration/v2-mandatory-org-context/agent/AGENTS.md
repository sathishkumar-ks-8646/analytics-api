# Zoho Analytics REST API v2 — mandatory organization context

Instructions for AI coding agents working on code that calls the Zoho Analytics
REST API v2. Written for tools that read `AGENTS.md` (Cursor, GitHub Copilot,
Codex, Zed, Jules and others). Agents that support Agent Skills should load
`skills/zoho-analytics-v2-org-context/` instead — it carries the same facts with
task-specific detail.

## What changed

Every call must now name its organization. Eight cross-organization endpoints
were replaced by three organization-scoped ones; two more kept their URL but now
require the `ZANALYTICS-ORGID` header.

**The eight removed endpoints stop answering in March 2027.**

| Old | New |
|---|---|
| `GET /restapi/v2/orgs` | **No endpoint** — the Org ID goes in configuration |
| `GET /restapi/v2/workspaces` | `GET /restapi/v2/orgs/workspaces` |
| `GET /restapi/v2/workspaces/owned` | `GET /restapi/v2/orgs/workspaces` |
| `GET /restapi/v2/workspaces/shared` | `GET /restapi/v2/orgs/workspaces` |
| `GET /restapi/v2/dashboards` | `GET /restapi/v2/orgs/dashboards` |
| `GET /restapi/v2/dashboards/owned` | `GET /restapi/v2/orgs/dashboards` |
| `GET /restapi/v2/dashboards/shared` | `GET /restapi/v2/orgs/dashboards` |
| `GET /restapi/v2/recentviews` | `GET /restapi/v2/orgs/recentitems` |

SDK methods moved off `AnalyticsClient`: `getWorkspaces` → `OrgAPI.getOrgWorkspaces`,
`getDashboards` → `OrgAPI.getOrgDashboards`, `getRecentViews` → `OrgAPI.getOrgRecentItems`,
`getWorkspaceDetails` → `WorkspaceAPI`, `getViewDetails` → `OrgAPI`, `getOrgs` → removed.

## Rules

1. **Never write a deprecated endpoint or SDK method**, even as an interim step.
   There is no fallback and no redirect.
2. **Send `ZANALYTICS-ORGID` on every request.** Add it to the shared HTTP client
   or request builder, not per call site.
3. **The Organization ID comes from configuration** (`ZOHO_ANALYTICS_ORG_ID`),
   read once from the Zoho Analytics UI → Settings → Organisation. There is no
   API that returns it. Never invent, guess or hardcode one.
4. **Carry the Organization ID as a string.** These numbers exceed 32-bit range;
   a truncated ID produces error `8084` and looks like a typo.
5. **Check the HTTP verb before rewriting `/restapi/v2/workspaces`.** `POST` on
   that path is Create Workspace and is unaffected.
6. **`GET /restapi/v2/orgs/dashboards` is paged.** Loop on
   `pageDetails.hasNextPage` — never on page length. It returns an object with
   `views` and `pageDetails`, where the old endpoints returned a plain array.
7. **`8083` and `8084` are terminal.** The header is missing / the ID is unknown.
   Never retry; surface an actionable message.
8. **Merged response keys:** `ownedWorkspaces` + `sharedWorkspaces` →
   `data.workspaces`; `ownedViews` + `sharedViews` → `data.views`.

## Before you change anything

```bash
python3 agent/scan.py /path/to/project          # every call site, with file:line
python3 agent/scan.py /path/to/project --json   # same, machine-readable
```

Exits non-zero when something will break. `warn` findings
(`getWorkspaceDetails`, `getViewDetails`) are correct when already called on a
`WorkspaceAPI` / `OrgAPI` instance — check the receiver before editing.

## Exact values

`agent/migration-map.json` holds every mapping as structured data: endpoints, SDK
methods per language, response fields, all 17 error codes, CONFIG parameters and
limits. **Read values from there rather than recalling them.**

Full prose, with request and response examples:

| Topic | File |
|---|---|
| Why, and the vocabulary | `01-why-org-context.md` |
| What changed, before and after | `02-whats-changed.md` |
| Rewriting HTTP calls | `03-endpoint-migration.md` |
| Java, Python, C#, Go, PHP, Node.js, Ruby | `04-sdk-migration.md` |
| Specs, Postman, RAG indexes, MCP servers | `05-knowledge-bases.md` |
| Timeline and completion checks | `06-timeline.md` |
| Every error code and the FAQ | `07-troubleshooting.md` |
