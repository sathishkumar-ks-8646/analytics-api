# The facts every part of this migration rests on

Condensed from `../../../../01-why-org-context.md` and `../../../../02-whats-changed.md`.
Read those for the full reasoning and worked examples.

## 1. The header is mandatory everywhere

`ZANALYTICS-ORGID` is now required on **every endpoint in the API**, not only the
ones this migration renames. Around 200 endpoints already required it; the change
is that the remaining handful no longer accept its absence.

Add it in the shared HTTP client or request builder, once. If `8083` appears on
every call at the same time, the shared builder is what was missed.

**Carry the ID as a string.** Organization IDs such as `700000123456` exceed
32-bit range, and in JavaScript leave safe-integer territory once concatenated
with other IDs. A silently truncated ID produces `8084` and looks like a typo.

## 2. The Organization ID comes from configuration

`GET /restapi/v2/orgs` was the discovery call. It is removed and **has no API
replacement** — deliberately. The point of the change is that an application
*states* its organization rather than discovering one.

Read it once from the Zoho Analytics UI → **Settings → Organisation**, and store
it next to the client ID and refresh token (`ZOHO_ANALYTICS_ORG_ID`).

Everything else the old endpoint returned is still available, organization-scoped:

| Old field | Where now |
|---|---|
| `orgId` | Configuration |
| `orgName`, `orgDesc` | UI → Settings → Organisation |
| `planName` | `GET /restapi/v2/subscription` (needs the header) |
| `numberOfWorkspaces` | Count `data.workspaces` from `GET /restapi/v2/orgs/workspaces` |
| `role` | `GET /restapi/v2/workspaces/{id}` with `CONFIG={"withUserRoleInfo":true}` |
| `isDefault` | No equivalent — the application decides now |

**Serving several organizations** changes from *discover then fan out* to
*configure then fan out*. Hold the list of organization IDs in configuration. If
the product must cover organizations that cannot be known in advance, add an
"Add organization" step to the setup flow and ask the user for the ID — the same
way you already ask for a client ID. Do not guess.

## 3. `8083` and `8084` are not retryable

| Code | Name | Means |
|---|---|---|
| `8083` | `ORGID_NOT_PRESENT_IN_THE_HEADER` | The header was missing or empty |
| `8084` | `ORGID_NOT_EXIST` | No organization has that ID |

Retrying the identical request fails identically. Anything with a retry policy —
an HTTP client, a job runner, an AI agent — must treat these as terminal and
surface an actionable message rather than looping.

## 4. The dashboard listing is paged

`GET /restapi/v2/orgs/dashboards` returns `data.views` **and** `data.pageDetails`,
where its three predecessors returned everything in one response.

Loop on `pageDetails.hasNextPage`. Never on page length — `hasNextPage` is
computed after duplicates and role-restricted entries have been removed from the
page, so a page can hold 3 entries when 100 were requested and still have more
behind it.

In the SDKs this is also a **return-type change**: an object where the old method
returned an array. In Python, Ruby, PHP, Node.js and Go that is a runtime failure,
not a compile error.

## What did not change

- **Authentication.** Same OAuth flow, same scopes. `ZohoAnalytics.metadata.read`
  covers all three new endpoints — the same scope the old ones used.
- **Data import and export.** Untouched.
- **`POST /restapi/v2/workspaces`** (Create Workspace). Shares a path with a
  removed `GET`; check the verb before rewriting that path.
- **Around 200 other endpoints** that were already organization-scoped.
- **The response envelope**, error-body shape, and CONFIG conventions.

## Why it was done

The old cross-organization endpoints had four problems, all consequences of not
naming an organization: the answer was ambiguous when a user belonged to several
organizations; responses mixed data from different organizations; nothing was
safe to cache; and the cost of the fan-out was invisible and unbounded.

Useful to explain when a user asks why there is no automatic redirect: the new
URLs and response shapes differ, so a redirect would break callers just as surely
as removal does — only silently.
