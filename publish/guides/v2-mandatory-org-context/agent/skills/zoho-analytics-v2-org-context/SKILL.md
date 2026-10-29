---
name: zoho-analytics-v2-org-context
description: Migrate code, SDKs and API artefacts off the eight removed Zoho Analytics REST API v2 cross-organization endpoints, which stop answering in March 2027. Use when the user mentions Zoho Analytics organization context, ZANALYTICS-ORGID, error 8083 or 8084, or calls any of /restapi/v2/orgs, /restapi/v2/workspaces, /restapi/v2/workspaces/owned, /restapi/v2/workspaces/shared, /restapi/v2/dashboards, /restapi/v2/dashboards/owned, /restapi/v2/dashboards/shared, /restapi/v2/recentviews, or the SDK methods getOrgs, getWorkspaces, getDashboards or getRecentViews.
---

# Zoho Analytics v2 — mandatory organization context

Zoho Analytics REST API v2 now requires every call to name the organization it
applies to. Eight cross-organization endpoints were replaced by three
organization-scoped ones; two more kept their URL but now require a header.

**The eight removed endpoints stop answering in March 2027.** They still respond
today, so nothing is broken yet — this is the migration window.

## The facts every part of this migration depends on

1. **`ZANALYTICS-ORGID` is mandatory on every endpoint**, not just the ones below.
   Add it in your shared HTTP client or request builder once, not per call site.
2. **The Organization ID comes from configuration, not from an API call.** Read it
   once from the Zoho Analytics UI → **Settings → Organisation** and store it next
   to your client ID and refresh token. `GET /restapi/v2/orgs` was the discovery
   call and has no replacement.
3. **`8083` means the header is missing. `8084` means the ID is unknown.** Neither
   is retryable — a retry of the identical request will fail identically.
4. **`GET /restapi/v2/orgs/dashboards` is paged**, where its predecessors were not.
   Loop on `pageDetails.hasNextPage`, never on page length.

## Start here

Ask which situation the user is in, or infer it from the code in front of you,
then read the matching skill. Most migrations need the first two; large
organizations need all three.

| The user is… | Use |
|---|---|
| Calling the REST API directly over HTTP — curl, fetch, requests, a gateway | `zoho-analytics-v2-endpoint-migration` |
| Using an official SDK — Java, Python, C#, Go, PHP, Node.js, Ruby | `zoho-analytics-v2-sdk-migration` |
| Maintaining an OpenAPI spec, Postman collection, RAG index or MCP server | `zoho-analytics-v2-artifact-migration` |
| Looking at a live error right now | `references/troubleshooting.md` first, then the relevant skill above |

If the user has not said, **run the scanner first** — what it finds tells you
which skills apply, and gives the user a number to work down.

## Find the work before changing anything

```bash
python3 agent/scan.py /path/to/their/project
python3 agent/scan.py /path/to/their/project --json   # when you want to parse it
```

It reports every deprecated path, SDK method and response key with file and line,
and exits non-zero if anything is in the `error` class. Severities mean:

- **error** — will fail in March 2027. Must change.
- **warn** — needs a human look. Usually `getWorkspaceDetails` / `getViewDetails`,
  which are fine *if* they are already called on a `WorkspaceAPI` / `OrgAPI`
  instance, and broken if they are still on `AnalyticsClient`.

## The data behind all of this

`agent/migration-map.json` holds every mapping as structured data: old → new
endpoints, old → new SDK methods per language, response field mappings, all 17
error codes, CONFIG parameters and limits. Read it when you need an exact value
rather than prose. Do not restate its contents from memory — the user's build
depends on these being right.

## Reference material

- `references/shared-facts.md` — the four facts above, in full, with the reasoning
- `references/timeline.md` — what happens when, and how to prove you are done
- `references/troubleshooting.md` — every error code, symptom-first

The authored source for all of it is the chapter set two directories up
(`../../../01-why-org-context.md` … `../../../07-troubleshooting.md`). Cite those
to the user when they want the full explanation with examples.

## Working rules

- **Never suggest a deprecated endpoint or method**, even as an interim step.
  There is no fallback and no redirect; the URLs and response shapes differ.
- **Check the HTTP verb before rewriting a `/restapi/v2/workspaces` path.**
  `POST` on that path is Create Workspace and is completely unaffected. A
  path-only search and replace will break it.
- **Re-pointing a dashboard URL is not enough.** The replacement is paged and
  returns an object where the old one returned an array. Both have to change.
- **Do not estimate counts or dates.** The deadline is March 2027; the counts are
  in `migration-map.json`.
