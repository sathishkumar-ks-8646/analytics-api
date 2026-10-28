# Timeline, and how to prove the migration is finished

Condensed from `../../../../06-timeline.md`.

## One date

**March 2027.** The eight replaced endpoints stop answering. No extension, no
opt-out, and no silent fallback — the new URLs and response shapes differ, so a
redirect would break callers just as surely as removal.

## Where things stand now

- **Both old and new endpoints answer.** Nothing is broken yet. This is the
  migration window.
- **The old endpoints are already out of the documentation** — the API reference,
  the OpenAPI specs, the OKF bundle, the Postman collection and all seven SDKs. A
  developer reading the docs today will not find them.
- **The SDKs are ahead of the server.** The methods are gone from all seven SDKs
  *now*, while the endpoints answer until 2027. Upgrading the SDK breaks the build
  before anything breaks in production. That is deliberate: it turns a 2027
  incident into a build-time problem.

## What "deprecated" actually means here

| Question | Answer |
|---|---|
| Returns correct data today? | Yes |
| Will get bug fixes? | No |
| Will get new fields when the new endpoints do? | No — they will drift apart |
| Appears in the documentation? | No, already removed |
| Still exposed by the SDKs? | No, removed from all seven today |
| Warning header on the response? | Do not rely on one — build your own monitoring |
| Will the date move? | Plan as though it will not |

Treat anything still calling them as already broken, just not yet failing.

## A sensible schedule

The window is long. Use a short slice of it early rather than a panicked slice
late — because the expensive part is not the code, it is the **discovery**: the
scheduled job nobody owns, the Deluge script in a Creator app, the notebook on an
analyst's laptop. Those surface slowly.

1. **Week 1 — measure exposure.** Run `agent/scan.py`, and add the monitoring
   alert. You cannot plan until you know how many call sites exist and who owns them.
2. **Week 2 — configure the Organization ID** and wire `ZANALYTICS-ORGID` into
   the shared request builder. One edit, most of the surface fixed.
3. **Weeks 3–4 — migrate the listings.** Do the two *changed* endpoints first
   (header only), then the listings, where response shapes change.
4. **Week 5 — refresh the contracts.** OpenAPI, Postman, OKF, MCP tool
   definitions, the wiki. Skipping this is how the old endpoints creep back in
   six months later.
5. **Then — watch the alert** until it is silent across a full billing cycle.

## The three completion checks

All three must pass. "We think we got them all" is not one of them.

**1. The code is clean.**

```bash
python3 agent/scan.py /path/to/project    # exits 0, no errors reported
```

A hit on `/restapi/v2/workspaces` is only a problem when the method is `GET`.

**2. The traffic is zero.** The monitoring alert on the eight deprecated paths
has not fired for a **full billing cycle** — month-end and quarter-end included.
Monthly and quarterly jobs are the ones everyone forgets. Do not close the ticket
on a quiet week.

**3. The contracts are fresh.**

```bash
grep '"version"' /path/to/okf/manifest.json | head -1       # expect 2.0.0

grep -rl "recentviews\|dashboards/owned\|dashboards/shared\|workspaces/owned\|workspaces/shared" \
  /path/to/openapi /path/to/postman /path/to/okf             # expect no output
```

## If you are reading this after March 2027

An integration has probably already broken. Smallest fix first:

1. Find the failing call — an explicit failure on one of the eight removed paths.
2. Get the Organization ID from **Settings → Organisation**.
3. Add the `ZANALYTICS-ORGID` header, re-point the path, and fix the response
   parsing. Use `zoho-analytics-v2-endpoint-migration`.

Dashboard listings need the most work: the replacement is paged and returns an
object rather than an array.
