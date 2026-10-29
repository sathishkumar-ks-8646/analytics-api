## Removed APIs

Every Zoho Analytics V2 endpoint now resolves inside a single organization, named by the mandatory `ZANALYTICS-ORGID` header. The eight cross-organization endpoints below have no place in that model and are **deprecated**. They still answer today and **stop answering in March 2027**. There is no extension and no opt-out.

The matching methods have been **removed from all seven SDKs in 2.10.0**, deliberately ahead of the endpoint switch-off: upgrading the SDK turns the migration into a build error today rather than an outage in 2027.

| Removed endpoint | Replacement |
|---|---|
| Get Org List — `GET /restapi/v2/orgs` | *No replacement.* Read the Organization ID from **Settings → Organisation** in the Zoho Analytics UI. |
| Get All Workspace List — `GET /restapi/v2/workspaces` | Get Org Workspaces — `GET /restapi/v2/orgs/workspaces` |
| Get Owned Workspace List — `GET /restapi/v2/workspaces/owned` | Get Org Workspaces |
| Get Shared Workspace List — `GET /restapi/v2/workspaces/shared` | Get Org Workspaces |
| Get All Dashboards — `GET /restapi/v2/dashboards` | Get Org Dashboards — `GET /restapi/v2/orgs/dashboards` |
| Get Owned Dashboards — `GET /restapi/v2/dashboards/owned` | Get Org Dashboards |
| Get Shared Dashboards — `GET /restapi/v2/dashboards/shared` | Get Org Dashboards |
| Get Recent Views — `GET /restapi/v2/recentviews` | Get Org Recent Items — `GET /restapi/v2/orgs/recentitems` |

**Note:** only the `GET` on `/restapi/v2/workspaces` is gone. The `POST` on the same path — *Create Workspace* — is unaffected.

## SDK methods that moved class

These two endpoints are **not** removed. The HTTP call is unchanged; only the SDK object you call it on has changed, because `AnalyticsClient` no longer holds an organization.

- `getWorkspaceDetails` moved from `AnalyticsClient` to **`WorkspaceAPI`**. The workspace ID argument is dropped — the instance already holds it — and an optional `config` argument is added.
- `getViewDetails` moved from `AnalyticsClient` to **`OrgAPI`**. The signature is unchanged.

## Existing APIs that changed in place

Same URL, same response, same fields. `ZANALYTICS-ORGID` has gone from optional to **mandatory**, and each gained two error codes: `8083` (header missing or empty) and `8084` (no organization with that ID).

- Get Workspace Info — `GET /restapi/v2/workspaces/<workspace-id>`
- Get View Details — `GET /restapi/v2/views/<view-id>`

**One runtime trap the compiler cannot catch:** `getOrgDashboards` returns an *object* containing `views` and `pageDetails`, where `getOwnedDashboards` returned an *array*. In Python, Ruby, PHP, Node.js and Go this is a runtime shape change, not a build error. Search for every place you iterated the old return value directly and add `["views"]`.
