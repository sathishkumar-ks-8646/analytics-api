---
description: Every error the Zoho Analytics organization-context migration can produce, what it means in plain words, and the fix - plus the questions people ask first.
---

# Troubleshooting & FAQ

What went wrong, why, and what to type instead.

## 1. Symptom first

Start here if you have a failure in front of you.

| ^Symptom | Most likely cause | Go to |
|---|---|---|
| `errorCode: 8083` | You did not send `ZANALYTICS-ORGID` | [8083](#error-codes) |
| `errorCode: 8084` | The Organization ID is wrong or mistyped | [8084](#error-codes) |
| `errorCode: 7301` on a call that used to work | You are not a member of the organization you named | [7301](#error-codes) |
| `errorCode: 7103` on a workspace you know exists | Right workspace, wrong organization in the header | [7103](#error-codes) |
| `errorCode: 7104` on a view you know exists | Right view, wrong organization in the header | [7104](#error-codes) |
| `errorCode: 7476` | More than 100 workspaces in scope for the dashboard listing | [7476](#error-codes) |
| `errorCode: 7387` | A `workspaceIds` entry is not in this organization | [7387](#error-codes) |
| 404 / "no such endpoint" | You are calling a deprecated path after removal | [Timeline](06-timeline.md) |
| Empty list, no error | Correct behaviour — nothing is visible to this caller | [Why: empty lists](01-why-org-context.md#the-new-model) |
| `KeyError: 'ownedWorkspaces'` | The response shape changed | [Field mapping](03-endpoint-migration.md#the-three-workspace-listings) |
| `TypeError: list indices must be integers` | `getOrgDashboards` returns an object, not an array | [Runtime trap](04-sdk-migration.md#errors-your-build-will-throw-and-what-they-mean) |
| Only ever 100 dashboards come back | You are not paging | [Paging](#q-why-do-i-only-get-100-dashboards) |
| Dashboard list is empty for everyone | Access Restrictions, or org-level listing switched off | [7430 / 7431](#error-codes) |
| `NoMethodError` / `cannot find symbol` after SDK upgrade | The method moved off `AnalyticsClient` | [Method map](04-sdk-migration.md#the-method-map) |

## 2. Error codes

Every code this change can produce. The failure body always looks like this:

```json
{
  "status": "failure",
  "summary": "ORGID_NOT_PRESENT_IN_THE_HEADER",
  "data": {
    "errorCode": 8083,
    "errorMessage": "Organization id is not present in the header."
  }
}
```

Branch on `data.errorCode`. `summary` is the symbolic name; `errorMessage` is human text and may be localised.

### Header and organization

| ^Code | Name | In plain words | Fix |
|---|---|---|---|
| `8083` | `ORGID_NOT_PRESENT_IN_THE_HEADER` | You did not send `ZANALYTICS-ORGID`, or sent it empty. | Add the header. If this appears everywhere at once, you missed the shared request builder. |
| `8084` | `ORGID_NOT_EXIST` | No organization has that ID. Usually a typo, a truncated number, or an ID from a different data centre. | Re-read it from **Settings → Organisation**. Keep it a **string** — these numbers overflow a 32-bit integer. |
| `7301` | `SECURITY_NOT_PERMITTED` | The organization exists, but the authenticated user is not an active member of it. Also returned when Get Org Dashboards is called through a Client Portal / White Label domain. | Check that the token and the organization belong together. For Client Portal, use the standard API host. |

:::warn 8084 is often a type problem, not a typo
Organization IDs such as `700000123456` exceed 32-bit range. In JavaScript they also exceed `Number.MAX_SAFE_INTEGER` territory once concatenated with other IDs. **Carry them as strings everywhere.** A silently truncated ID produces `8084` and looks like a typo.
:::

### Target not found in this organization

| ^Code | Name | In plain words | Fix |
|---|---|---|---|
| `7103` | — | The workspace was not found **in the organization you named**. | The workspace probably lives in a different organization. Check the header before you doubt the ID. |
| `7104` | `META_OBJECT_NOT_PRESENT` | The view was not found **in the organization you named**. | Same — check the header first. |

These two codes existed before, but their meaning narrowed: they used to mean "does not exist anywhere", and now mean "does not exist *here*".

### Dashboard listing only

| ^Code | Name | In plain words | Fix |
|---|---|---|---|
| `7387` | `DBID_NOT_BELONGS_TO_ZSOID` | One of the `workspaceIds` you sent belongs to another organization, or does not exist. The **whole request** fails; bad IDs are not skipped. | Build the list from `Get Org Workspaces` for the same organization. |
| `7430` | `ORG_LEVEL_VIEWS_NOT_ALLOWED` | Org-level view listing is switched off for this organization. You see this code because you are the Account Admin. | Use the workspace-level view APIs, or contact support to enable it. |
| `7431` | `ORG_LEVEL_VIEWS_NOT_ALLOWED_WL_USERS` | Same setting, reported to everyone who is not the Account Admin. | Use the workspace-level APIs, or ask your Account Admin. |
| `7476` | `ORG_LEVEL_VIEWS_WS_MORE_THAN_ALLOWED_LIMIT` | You omitted `workspaceIds` and the caller can see more than 100 workspaces. | Send `workspaceIds` in batches of 100. See the [recipe](03-endpoint-migration.md#the-100-workspace-cap). |

### CONFIG validation

These are rejected by the request filter before the handler runs, so they tell you about the request, not about your data.

| ^Code | Name | In plain words | Fix |
|---|---|---|---|
| `8507` | `MORE_THAN_MAX_LENGTH` | `searchKey` over 100 characters, `workspaceIds` over 10,000 characters, or CONFIG over 11,000 characters. | Shorten it, or send fewer workspace IDs per call. |
| `8516` | `UNABLE_TO_PARSE_DATA_TYPE` | `pageNo` or `recordsPerPage` arrived as a string, not a number. | Send `{"pageNo": 2}`, not `{"pageNo": "2"}`. |
| `8534` | `JSON_PARSE_ERROR` | CONFIG is not valid JSON, or `workspaceIds` is not an array. | Stringify the JSON, then URL-encode it. Encode once, not twice. |
| `8539` | `INVALID_VALUE_NOT_ALLOWED` | A CONFIG value is `null`, empty or blank — including a single blank `workspaceIds` entry. | **Leave the key out** rather than sending an empty value. |
| `8542` | `EXTRA_KEY_FOUND_IN_JSON` | CONFIG has a key other than `workspaceIds`, `pageNo`, `recordsPerPage`, `searchKey`. | Remove it. Check for typos such as `pageNum`. |
| `8544` | `OUT_OF_RANGE` | `pageNo` outside 1–1,000, or `recordsPerPage` outside 1–500. | Clamp before sending. `recordsPerPage: 1000` is a common mistake — the cap is 500. |
| `8547` | `ARRAY_SIZE_OUT_OF_RANGE` | More than 1,000 entries in `workspaceIds`. | Batch. In practice stay at or under 100 because of `7476`. |

### Authentication

| ^Code | Name | Fix |
|---|---|---|
| `8535` | `INVALID_OAUTHTOKEN` | Refresh the token. All three new endpoints need `ZohoAnalytics.metadata.read` — the same scope the old ones used, so this is not caused by the migration. |

## 3. Frequently asked questions

### Q. Can I just keep sending the old endpoints until 2027?

They will answer until then, so technically yes. But they get no fixes, no new fields and no support, and the SDKs no longer expose them. Anything you ship today against a deprecated endpoint is work you have committed to redoing before **March 2027**.

### Q. Why was there no automatic redirect from the old URL to the new one?

Because a redirect would be a lie. `GET /restapi/v2/workspaces` returned `ownedWorkspaces` and `sharedWorkspaces` across every organization; `GET /restapi/v2/orgs/workspaces` returns `workspaces` for one. A client following a redirect would get a 200 with a body it cannot parse — a harder failure to diagnose than a clear error.

### Q. Where do I get the Organization ID now?

Zoho Analytics → **Settings → Organisation**. Copy it once into configuration. See [chapter 01](01-why-org-context.md#where-to-find-your-organization-id).

### Q. My application serves users across several organizations. What now?

Keep a list of Organization IDs in your own configuration or database and loop over it, sending a different `ZANALYTICS-ORGID` per iteration. The [fan-out recipe](03-endpoint-migration.md#recipe-i-used-to-list-across-every-organization) has working code. If you cannot know the organizations in advance, add an "Add organization" step to your setup flow and ask the user for the ID.

### Q. Why do I only get 100 dashboards?

`recordsPerPage` defaults to **100** and the endpoint is paged. Loop while `data.pageDetails.hasNextPage` is `true`. Do not stop because a page came back short — `hasNextPage` is computed after filtering, so a short page can still have more behind it. [Paging code](03-endpoint-migration.md#paging-correctly).

### Q. How do I tell owned dashboards from shared ones now?

`sharedBy` on each entry holds the email address of whoever shared it with you; it is empty or absent for things you own. Same for workspaces, using `createdBy`. The information moved from the URL into the row.

### Q. `isDefault` used to mean the organization's default workspace. Did that change?

The old reference said that, and it was wrong. `isDefault` has always been **per user** — it is `true` for the calling user's own default workspace. The new reference states this explicitly. Do not cache it as a property of the workspace; two users see different values for the same row.

### Q. Can I still get a list of every organization I belong to?

Not from the API. That capability was the thing being removed: the API no longer discovers organizations for you, it acts on the one you name. Read the ID from the UI and configure it.

### Q. Do I need new OAuth scopes?

No. All three replacements use `ZohoAnalytics.metadata.read`, exactly like the endpoints they replace. Existing tokens work unchanged.

### Q. Does this affect data import or export?

No. Import, export, row operations, schema operations and everything else under `/workspaces/{workspace-id}/…` already required the header and are untouched.

### Q. Is `POST /restapi/v2/workspaces` affected?

No. Only the `GET` on that path was removed. Create Workspace is unchanged. Check the method before acting on a grep hit.

### Q. Why did `getViewDetails` move to `OrgAPI` rather than `ViewAPI`?

A `ViewAPI` instance is constructed from an organization **and a workspace and a view**. The Get View Details endpoint has no workspace in its URL — it resolves the view from the organization alone. `OrgAPI` carries exactly an organization, so it is the honest home. Putting it on `ViewAPI` would force you to supply a workspace ID the endpoint never uses.

### Q. Why did `getWorkspaceDetails` lose its `workspaceId` argument?

Because `WorkspaceAPI` already holds it: you passed it to `getWorkspaceInstance(orgId, workspaceId)`. Passing it again would let the two disagree. The method gained an optional `config` argument instead, for `withUserRoleInfo`.

### Q. What happens to recent items I viewed in my other organizations?

They are still there, in those organizations. Call `GET /restapi/v2/orgs/recentitems` once per organization with the matching header. The list is capped at 20 entries **per organization**.

### Q. The new recent-items list points at a view I cannot open. Bug?

No — documented behaviour. Recent items are filtered by *workspace* visibility only, with no view-level check. Treat `viewId` as a hint and handle a refusal when you open it.

### Q. Our AI assistant keeps suggesting the old endpoints.

Its knowledge index still contains the deleted documents. An incremental re-index adds the new ones but does not remove the old. **Drop the index and rebuild it** from OKF bundle `2.0.0`. See [chapter 05](05-knowledge-bases.md#the-okf-knowledge-bundle).

### Q. How do I know when I am finished?

Three things, all true at once: the grep is clean, the monitoring alert on the deprecated paths has been silent for a full billing cycle, and every contract copy (OpenAPI, Postman, OKF, MCP) has been refreshed. [The full check](06-timeline.md#prove-you-are-ready).

## 4. Still stuck

1. Re-read the [endpoint section](03-endpoint-migration.md) for the specific call. The field mapping tables catch most parsing failures.
2. Reproduce the call with `curl`, with the header written out by hand. That separates "my code is wrong" from "my request is wrong".

```bash
curl -s "https://analyticsapi.zoho.com/restapi/v2/orgs/workspaces" \
  -H 'ZANALYTICS-ORGID: 700000123456' \
  -H 'Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy'
```

3. If that works and your code does not, the difference is in your client — usually a missing header, a double-encoded CONFIG, or an Organization ID that became a number somewhere.

:::sunset
A last reminder: the eight endpoints this guide replaces are **deprecated** and stop answering in **March 2027**. If you are reading this page because something broke, check the [timeline](06-timeline.md) first — the fix may simply be that the endpoint no longer exists.
:::

---

Back to [the start](index.md).
