---
description: What a Zoho Analytics organization is, what the ZANALYTICS-ORGID header does, and the four concrete problems that cross-organization endpoints caused.
---

# Why organization context is mandatory

If you are new to Zoho Analytics, read this chapter first. It explains the vocabulary, then the four real problems that made the old cross-organization endpoints a bad idea.

## 1. The vocabulary, in plain words

Zoho Analytics nests three things inside each other. Getting these straight makes the rest of the guide easy.

| ^Thing | What it is | Identified by |
|---|---|---|
| **Organization** | A company account. It holds the subscription, the user list, the billing and the security settings. Everything else lives inside one. | `orgId`, a long number like `700000123456` |
| **Workspace** | A container of data inside an organization — roughly a database. A workspace belongs to exactly one organization and never moves. | `workspaceId` |
| **View** | Anything inside a workspace: a table, a chart, a pivot, a summary, a query table or a dashboard. | `viewId` |

So the full address of a chart is *organization → workspace → view*. The organization is the outermost box, and until now the API let you skip it.

### One person, several organizations

Here is the part that causes all the trouble. **A single user can belong to more than one organization.** That is normal and common:

- You are an Account Admin of your own company's organization.
- A client has shared two dashboards with you, from *their* organization.
- A contractor engagement gave you a seat in a third.

Your OAuth token identifies *you*. It does not say which of those three organizations you mean right now. Something has to.

## 2. What the `ZANALYTICS-ORGID` header does

`ZANALYTICS-ORGID` is an HTTP request header. Its value is the `orgId` of the organization you want this one request to act on.

```http
GET /restapi/v2/orgs/workspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

Read that as two separate statements:

- `Authorization` says **who** is asking.
- `ZANALYTICS-ORGID` says **where** they are asking about.

The server needs both. With only the first it has to guess, and guessing is exactly what the old endpoints did.

:::info This header is not new
Around 200 of the 205 v2 endpoints already required `ZANALYTICS-ORGID` before this change. The ten endpoints in this guide were the exceptions. The change removes the exceptions; it does not introduce a new concept.
:::

## 3. The old model and what went wrong with it

The old endpoints had no organization in the URL and no organization header. `GET /restapi/v2/workspaces` meant *"every workspace this token can reach, in every organization, merged into one list"*. Four problems followed from that.

### Problem 1 — The answer was ambiguous

The same request returned a different list depending on how many organizations you happened to belong to. A workspace named `Sales Analytics` might appear twice, from two different organizations, with different IDs. Code that picked a workspace by name picked the wrong one, intermittently, in production, only for users with multiple memberships.

```json
{
  "data": {
    "ownedWorkspaces": [
      { "workspaceId": "466206000000071000", "workspaceName": "Sales Analytics", "orgId": "700000123456" }
    ],
    "sharedWorkspaces": [
      { "workspaceId": "138022000000002015", "workspaceName": "Sales Analytics", "orgId": "700000999888" }
    ]
  }
}
```

Which one did the caller want? The request did not say, so neither could the server.

### Problem 2 — Data from different organizations was mixed in one response

An organization is a security and billing boundary. Access Restrictions, trusted sharing domains, white-label settings and IP policies are all configured **per organization**. A single response that blended rows from several organizations could not honour all of their policies at once — the strictest organization's rules were effectively diluted by the most permissive one's.

Organization-scoped endpoints apply exactly one organization's policy to exactly one response. That is a property you can reason about and audit.

### Problem 3 — Responses were not safe to cache

Because the result depended on the caller's full membership graph rather than on anything in the request, two callers hitting the identical URL legitimately got different answers. Any cache keyed on the URL served the wrong user's data. Teams discovered this the hard way.

With the organization named in the request, the cache key is honest: *(token identity, organization, path)*.

### Problem 4 — It did not scale, and the cost was invisible

"Every workspace in every organization" has no upper bound. A consultancy user in forty client organizations triggered a scan across all forty, every time. The request had no way to say *"only this one"*, so there was no way to make it cheaper.

The new dashboard listing makes the cost visible and controllable: it is paged, it can be narrowed to specific workspaces with `workspaceIds`, and it refuses outright — with error `7476` — when more than 100 workspaces would have to be scanned.

## 4. The new model

One sentence: **the organization is an input, not a guess.**

| ^ | Old model | New model |
|---|---|---|
| Scope of a request | Every organization the caller belongs to | Exactly one organization |
| How scope is chosen | Inferred from the token's memberships | Stated by `ZANALYTICS-ORGID` |
| Same request, two callers | Different scope | Same scope, different *visibility* within it |
| Result shape | `ownedX` plus `sharedX` | One list, each entry labelled with its owner |
| Cacheable | Not safely | Yes, keyed on identity plus organization |
| Cost | Unbounded | Paged, narrowable, capped |

### What still depends on who is asking

Mandatory organization context does **not** mean everyone sees the same thing. Inside the chosen organization, visibility still follows permissions:

- An **Account Admin** or **Organization Admin** sees every active workspace in that organization.
- **Everyone else** sees only the workspaces shared with them.
- Dashboards additionally apply a view-level check: you see a dashboard if you administer its workspace, hold a custom role in it, or it was shared with you or made public.

So the rule is: *the request fixes the organization; the token still decides what you can see inside it.*

:::warn An empty list is a valid answer
If the caller has nothing shared with them in that organization, you get `"workspaces": []` and HTTP 200 — not an error. Do not treat an empty list as a failure, and do not treat it as "the organization is empty". It means "nothing visible to this caller".
:::

## 5. Where to find your Organization ID

You used to call `GET /restapi/v2/orgs` to discover the IDs of every organization you belong to. That endpoint is gone, so the Organization ID is now something you look up once and keep in configuration.


### From the Zoho Analytics web UI

1. Log in to your Zoho Analytics account.
2. Click the **Organization Settings** (gear/wrench) icon in the top-right corner of the page.
3. The **Organization Details** page opens by default.
4. Copy the **Org ID** listed on the page, directly below the Organization Name.

Store it where you store the rest of your connection settings, next to the client ID and the refresh token. It never changes for a given organization.

### From a response you already have

Nearly every listing response includes an `orgId` field on each entry. If you already hold, say, a workspace record, the organization is right there:

```json
{
  "workspaceId": "466206000000071000",
  "workspaceName": "Sales Analytics",
  "orgId": "700000123456"
}
```

### From a workspace or view name

If you know the *name* of a workspace but not its ID, [Get Meta Details From Name](https://www.zoho.com/analytics/api/v2/) resolves names to IDs — but note that it is itself organization-scoped, so you need the Organization ID first. The UI is the starting point.

:::sunset
`GET /restapi/v2/orgs` is **deprecated** and will be switched off in **March 2027**. If your application currently calls it at start-up to discover organizations, replace that call with a configured Organization ID per connection. If your product genuinely needs to work across several organizations, see the recipe in [chapter 03](03-endpoint-migration.md#recipe-i-used-to-list-across-every-organization).
:::

## 6. What this change does not touch

So you can stop worrying about the rest of your integration:

- **Authentication.** OAuth flow, scopes, token refresh — all unchanged.
- **Workspace-scoped and view-scoped endpoints.** Anything with `/workspaces/{workspace-id}/…` in the path already required the header and is untouched.
- **Data import and export.** Unchanged.
- **The response envelope.** Still `{"status", "summary", "data"}`, still the same error shape.
- **Error semantics you already handle.** `8535` for a bad token, `7301` for permission, and so on. The change adds `8083` and `8084` in places that did not previously return them, because the header is now required there.
- **Data centres.** `analyticsapi.zoho.com`, `.eu`, `.in` and the rest behave exactly as before.

---

Next: [what actually changed](02-whats-changed.md), endpoint by endpoint.
