# Troubleshooting — symptom first

Condensed from `../../../../07-troubleshooting.md`, which has the full FAQ.
Every code as data, with fixes: `../../../migration-map.json` → `error_codes`.

## Start from the symptom

| Symptom | Most likely cause |
|---|---|
| `errorCode: 8083` | `ZANALYTICS-ORGID` was not sent |
| `errorCode: 8084` | The Organization ID is wrong, mistyped, or **silently truncated** |
| `errorCode: 7301` on a call that used to work | Not a member of the organization named in the header |
| `errorCode: 7103` on a workspace you know exists | Right workspace, wrong organization |
| `errorCode: 7104` on a view you know exists | Right view, wrong organization |
| `errorCode: 7476` | More than 100 workspaces in scope for the dashboard listing |
| `errorCode: 7387` | A `workspaceIds` entry is not in this organization |
| 404 / "no such endpoint" | Calling a removed path after March 2027 |
| Empty list, no error | **Correct** — nothing is visible to this caller |
| `KeyError: 'ownedWorkspaces'` | Response shape changed — merged into `data.workspaces` |
| `TypeError: list indices must be integers` | `getOrgDashboards` returns an object, not an array |
| Only ever 100 dashboards | Not paging — loop on `pageDetails.hasNextPage` |
| Dashboard list empty for everyone | Access Restrictions, or org-level listing switched off (`7430`/`7431`) |
| `NoMethodError` / `cannot find symbol` after upgrading to SDK 2.10.0 | The method moved off `AnalyticsClient` |

## The failure body

```json
{
  "status": "failure",
  "summary": "ORGID_NOT_PRESENT_IN_THE_HEADER",
  "data": { "errorCode": 8083, "errorMessage": "Organization id is not present in the header." }
}
```

**Branch on `data.errorCode`.** `summary` is the symbolic name; `errorMessage` is
human text and may be localised.

## Header and organization

| Code | Name | Fix |
|---|---|---|
| `8083` | `ORGID_NOT_PRESENT_IN_THE_HEADER` | Add the header. If this appears everywhere at once, the shared request builder was missed |
| `8084` | `ORGID_NOT_EXIST` | Re-read from Settings → Organisation. **Keep the ID a string** |
| `7301` | `SECURITY_NOT_PERMITTED` | The org exists but the user is not an active member. Also returned when Get Org Dashboards is called through a Client Portal / White Label domain |

> **`8084` is usually a type problem, not a typo.** IDs like `700000123456`
> exceed 32-bit range. Carry them as strings everywhere; a truncated ID produces
> `8084` and looks like a mistyped number.

## Not found *in this organization*

| Code | Name | Note |
|---|---|---|
| `7103` | — | Workspace not found in the organization you named |
| `7104` | `META_OBJECT_NOT_PRESENT` | View not found in the organization you named |

Both existed before, but their meaning **narrowed**: they used to mean "does not
exist anywhere", now "does not exist *here*". Check the header before doubting
the ID.

## Dashboard listing only

| Code | Name | Fix |
|---|---|---|
| `7387` | `DBID_NOT_BELONGS_TO_ZSOID` | A `workspaceIds` entry is foreign or missing. The **whole request** fails; bad IDs are not skipped. Build the list from Get Org Workspaces for the same org |
| `7430` | `ORG_LEVEL_VIEWS_NOT_ALLOWED` | Org-level listing switched off; you see this code as Account Admin. Use workspace-level APIs or contact support |
| `7431` | `ORG_LEVEL_VIEWS_NOT_ALLOWED_WL_USERS` | Same setting, reported to everyone else |
| `7476` | `ORG_LEVEL_VIEWS_WS_MORE_THAN_ALLOWED_LIMIT` | Omitted `workspaceIds` with more than 100 visible workspaces. Batch them |

## CONFIG validation

Rejected by the request filter before the handler runs — these describe the
request, not the data.

| Code | Name | Fix |
|---|---|---|
| `8507` | `MORE_THAN_MAX_LENGTH` | `searchKey` > 100 chars, `workspaceIds` > 10,000 chars, CONFIG > 11,000 chars |
| `8516` | `UNABLE_TO_PARSE_DATA_TYPE` | Send `{"pageNo": 2}`, not `{"pageNo": "2"}` |
| `8534` | `JSON_PARSE_ERROR` | Stringify then URL-encode. **Encode once, not twice** |
| `8539` | `INVALID_VALUE_NOT_ALLOWED` | A value is null/empty/blank — leave the key out instead |
| `8542` | `EXTRA_KEY_FOUND_IN_JSON` | Only `workspaceIds`, `pageNo`, `recordsPerPage`, `searchKey`. Check for typos like `pageNum` |
| `8544` | `OUT_OF_RANGE` | `pageNo` 1–1,000, `recordsPerPage` 1–500. `recordsPerPage: 1000` is a common mistake — the cap is 500 |
| `8547` | `ARRAY_SIZE_OUT_OF_RANGE` | Over 1,000 `workspaceIds`. Stay at or under 100 because of `7476` |

## Authentication

`8535` `INVALID_OAUTHTOKEN` — refresh the token. All three new endpoints need
`ZohoAnalytics.metadata.read`, the same scope the old ones used, **so this is not
caused by the migration**. No new OAuth scopes are required.

## Answers people ask for first

- **Can I keep using the old endpoints until 2027?** They answer, but get no
  fixes and no new fields. Anything still calling them is already unsupported.
- **Why no automatic redirect?** The URLs and response shapes differ. A redirect
  would break callers silently instead of loudly.
- **Where do I get the Organization ID?** UI → **Settings → Organisation**. There
  is no API for it.
- **My app serves users across several organizations.** Configure the list of
  organization IDs and fan out explicitly, one `OrgAPI` per organization.
- **Why only 100 dashboards?** That is one page. Loop on `hasNextPage`.
- **How do I tell owned from shared now?** Derive it client-side by comparing
  `createdBy` to the caller — and check whether the split is still wanted.
- **Did `isDefault` change?** On a workspace it means the *caller's* default.
- **Do I need new OAuth scopes?** No.
- **Does this affect import or export?** No.
- **Is `POST /restapi/v2/workspaces` affected?** No. Create Workspace is untouched.
- **Our AI assistant keeps suggesting the old endpoints.** Its index still holds
  the deleted documents. Drop the vector index and rebuild from the 2.0.0 bundle —
  see `zoho-analytics-v2-artifact-migration`.
