---
description: The deprecation timeline for the Zoho Analytics v2 cross-organization endpoints - what deprecated means, what happens when, and how to prove nothing in your estate still calls them.
---

# Timeline & deprecation

One date matters: **March 2027**. This chapter says what happens before it, what happens on it, and how to be sure you are ready.

:::danger The headline
The eight replaced endpoints are **deprecated today** and are **removed in March 2027**. After that date they return an error instead of data. There is no extension and no opt-out.
:::

## 1. The timeline

<ul class="timeline">
  <li class="is-now">
    <div class="timeline__when">Now &mdash; the replacements are live</div>
    <h3>Both the old and the new endpoints answer</h3>
    <p>The three organization-scoped listings are available and documented. The eight deprecated endpoints still respond, so nothing of yours has broken. This is the window in which you migrate at your own pace.</p>
  </li>
  <li class="is-now">
    <div class="timeline__when">Now &mdash; documentation</div>
    <h3>The old endpoints are out of the v2 reference</h3>
    <p>They are removed from the API reference, the OpenAPI specifications, the OKF knowledge bundle, the Postman collection and all seven SDKs. A new developer reading the docs today will not find them, and an upgraded SDK will not compile against them.</p>
  </li>
  <li class="is-warn">
    <div class="timeline__when">Throughout the window</div>
    <h3>Deprecated means unsupported, not merely old</h3>
    <p>The deprecated endpoints receive no fixes, no new fields and no behaviour changes. A bug found in one of them will be closed with "migrate to the organization-scoped replacement". Treat anything still calling them as already broken, just not yet failing.</p>
  </li>
  <li class="is-end">
    <div class="timeline__when">March 2027 &mdash; removal</div>
    <h3>The eight endpoints stop answering</h3>
    <p>Requests to the deprecated paths no longer return data. Any integration still calling them fails at that point. There is no silent fallback to the new endpoints &mdash; the URLs and the response shapes are different, so a redirect would break callers just as surely.</p>
  </li>
</ul>

## 2. What exactly goes away in March 2027

| ^Endpoint | Status after March 2027 |
|---|---|
| ~~`GET /restapi/v2/orgs`~~ | Removed |
| ~~`GET /restapi/v2/workspaces`~~ | Removed. **`POST` on the same path keeps working** — Create Workspace is unaffected |
| ~~`GET /restapi/v2/workspaces/owned`~~ | Removed |
| ~~`GET /restapi/v2/workspaces/shared`~~ | Removed |
| ~~`GET /restapi/v2/dashboards`~~ | Removed |
| ~~`GET /restapi/v2/dashboards/owned`~~ | Removed |
| ~~`GET /restapi/v2/dashboards/shared`~~ | Removed |
| ~~`GET /restapi/v2/recentviews`~~ | Removed |

And what does **not** go away:

| ^Endpoint | Status |
|---|---|
| `GET /restapi/v2/orgs/workspaces` | The replacement. Stays. |
| `GET /restapi/v2/orgs/dashboards` | The replacement. Stays. |
| `GET /restapi/v2/orgs/recentitems` | The replacement. Stays. |
| `GET /restapi/v2/workspaces/{workspace-id}` | Stays. Already requires the header. |
| `GET /restapi/v2/views/{view-id}` | Stays. Already requires the header. |
| `POST /restapi/v2/workspaces` | Stays. Never affected. |
| Everything else in v2 | Stays. Around 200 endpoints were already organization-scoped. |

## 3. What "deprecated" means in practice

People read "deprecated" as "still fine for now". It is more specific than that:

| ^Question | Answer |
|---|---|
| Does it still return correct data today? | Yes. |
| Will it get bug fixes? | No. |
| Will it get new fields when the new endpoints do? | No. They will drift apart. |
| Will it appear in the documentation? | No. It is already removed from the reference. |
| Will the SDKs still expose it? | No. The methods are gone from all seven SDKs today. |
| Is there a warning header on the response? | Do not rely on one. Build your own monitoring — see [section 5](#prove-you-are-ready). |
| Will the date move? | Plan as though it will not. |

:::warn The SDKs are ahead of the server
The methods were removed from the SDKs **now**, while the endpoints answer until **March 2027**. So if you upgrade the SDK your code stops compiling before anything stops working. That is deliberate: it makes the migration a build-time problem rather than a 2027 incident.
:::

## 4. A sensible schedule

You have a long window. Use a short slice of it, early, rather than a panicked slice late.

<ol class="steps">
  <li>
    <h3>Week 1 &mdash; find out how exposed you are</h3>
    <p>Grep the code. Add the monitoring alert from <a href="05-knowledge-bases.md#monitoring-prove-you-are-done">chapter 05</a>. You cannot plan until you know how many call sites exist and who owns them.</p>
  </li>
  <li>
    <h3>Week 2 &mdash; configure the Organization ID</h3>
    <p>Read it from <strong>Settings &rarr; Organisation</strong>, add it to configuration, and wire <code>ZANALYTICS-ORGID</code> into the shared request builder. One edit, most of the surface fixed.</p>
  </li>
  <li>
    <h3>Weeks 3&ndash;4 &mdash; migrate the listings</h3>
    <p>Work down <a href="03-endpoint-migration.md">chapter 03</a>. Do the two <em>changed</em> endpoints first &mdash; they need only a header. Then the listings, where response shapes change.</p>
  </li>
  <li>
    <h3>Week 5 &mdash; refresh the contracts</h3>
    <p>OpenAPI, Postman, the OKF bundle, MCP tool definitions, the wiki. See <a href="05-knowledge-bases.md">chapter 05</a>. Skipping this is how the old endpoints creep back in six months later.</p>
  </li>
  <li>
    <h3>Then &mdash; watch the alert</h3>
    <p>Let it stay silent across a full billing cycle, month-end and quarter-end included. Close the ticket when it has.</p>
  </li>
</ol>

:::good Why not wait until 2026?
Because the expensive part is not the code, it is the <em>discovery</em>: the scheduled job nobody owns, the Deluge script in a Creator app, the notebook on an analyst's laptop. Those surface slowly. Start the monitoring now and let them surface while there is still time to fix them calmly.
:::

## 5. Prove you are ready

Three checks. All three must pass.

### Check 1 — the code is clean

```bash
grep -rnE '/restapi/v2/(orgs|workspaces|dashboards)"?$|/restapi/v2/(workspaces|dashboards)/(owned|shared)|/restapi/v2/recentviews' . \
  --include='*.java' --include='*.py' --include='*.cs' --include='*.go' \
  --include='*.php' --include='*.js' --include='*.ts' --include='*.rb' \
  --include='*.dg' --include='*.json' --include='*.yaml' --include='*.yml'
```

No output is a pass. Remember that a hit on `/restapi/v2/workspaces` is only a problem if the method is `GET`.

### Check 2 — the traffic is zero

Your monitoring alert on the eight deprecated paths has not fired for a full billing cycle.

### Check 3 — the contracts are fresh

```bash
# Your ingested OKF bundle should report 2.0.0
grep '"version"' /path/to/okf/manifest.json | head -1

# And none of the removed endpoints should appear anywhere in your copies
grep -rl "recentviews\|dashboards/owned\|dashboards/shared\|workspaces/owned\|workspaces/shared" \
  /path/to/openapi /path/to/postman /path/to/okf
```

No output from the second command is a pass.

## 6. If you are reading this after March 2027

If an integration has already broken, the fastest fix is the smallest one:

1. Find the failing call. The error will be an explicit failure on one of the eight paths listed in [section 2](#what-exactly-goes-away-in-march-2027).
2. Get the Organization ID from **Settings → Organisation**.
3. Add the `ZANALYTICS-ORGID` header.
4. Change the URL per the [endpoint index](03-endpoint-migration.md#endpoint-index).
5. Fix the response parsing — this is the step people miss. `ownedWorkspaces` + `sharedWorkspaces` became `workspaces`; `ownedViews` + `sharedViews` became `views` plus `pageDetails`.
6. For dashboards, add the paging loop. Without it you will silently get only the first 100.

[Chapter 03](03-endpoint-migration.md) has the full before-and-after for each one.

---

Next: [troubleshooting and FAQ](07-troubleshooting.md).
