"""Page content for the SDK documentation.

Prose is shared across all seven languages; code is pulled from `langs.py` so
every snippet matches the sample program that ships with that SDK. Each builder
returns markdown, which `build.py` writes to disk and also renders to HTML.
"""

from __future__ import annotations

from langs import Lang

DATA_CENTERS = """| Data center | API host | OAuth accounts host | Web application |
|---|---|---|---|
| United States | `analyticsapi.zoho.com` | `accounts.zoho.com` | `analytics.zoho.com` |
| Europe | `analyticsapi.zoho.eu` | `accounts.zoho.eu` | `analytics.zoho.eu` |
| India | `analyticsapi.zoho.in` | `accounts.zoho.in` | `analytics.zoho.in` |
| Australia | `analyticsapi.zoho.com.au` | `accounts.zoho.com.au` | `analytics.zoho.com.au` |
| Japan | `analyticsapi.zoho.jp` | `accounts.zoho.jp` | `analytics.zoho.jp` |
| China | `analyticsapi.zoho.com.cn` | `accounts.zoho.com.cn` | `analytics.zoho.com.cn` |
| Saudi Arabia | `analyticsapi.zoho.sa` | `accounts.zoho.sa` | `analytics.zoho.sa` |
| Canada | `analyticsapi.zohocloud.ca` | `accounts.zohocloud.ca` | `analytics.zohocloud.ca` |"""


# ======================================================================
# index
# ======================================================================

def index(lang: Lang) -> str:
    return f"""# {lang.name} SDK

The Zoho Analytics {lang.name} client wraps REST API v2. It carries your OAuth
credentials, keeps the access token alive, and exposes the API as four scoped
instances hanging off one client object.

::: danger Create the client once, not per request
Constructing a new client on every request will get your integration blocked by
Zoho Accounts within minutes. Read [Authentication](authentication.md#the-access-token-throttle)
before you ship anything.
:::

## Start here

1. [Getting started](getting-started.md) — install, construct a client, make a first call.
2. [Authentication](authentication.md) — OAuth, scopes, data centers, and the token throttle.
3. [Configuration](configuration.md) — timeouts, proxies, custom headers, regions.
4. [Errors](errors.md) — the response envelope, HTTP statuses, and the codes worth branching on.
5. [Limits](limits.md) — throttles, concurrency guards and plan quotas.

## Guides

- [Importing data](guides/importing-data.md) — synchronous, batched and job-based imports.
- [Exporting data](guides/exporting-data.md) — synchronous export and the asynchronous job flow.

## API reference

| Surface | Scope |
|---|---|
| [AnalyticsClient](reference/analytics-client.md) | Credentials, transport settings, instance factories. |
| [OrgAPI](reference/org-api.md) | Users, roles, admins, subscription, security controls. |
| [WorkspaceAPI](reference/workspace-api.md) | Views, folders, tags, schedules, alerts, backups, sharing. |
| [ViewAPI](reference/view-api.md) | Rows, columns, formulas, publishing, per-view metadata. |
| [BulkAPI](reference/bulk-api.md) | Import and export, synchronous and asynchronous. |

## Conventions in this SDK

| | |
|---|---|
| Method naming | {lang.naming} |
| Identifiers | {lang.id_type} |
| Failure surface | {lang.error_type} |
| Source | `{lang.source}` |
| Sample program | `{lang.sample}` |
"""


# ======================================================================
# getting started
# ======================================================================

def getting_started(lang: Lang) -> str:
    return f"""# Getting started

## Install

{lang.install}

## Register an OAuth client

1. Open the [Zoho API Console](https://api-console.zoho.com) for your data center.
2. Create a **Self Client** for server-to-server integrations, or a **Server-based
   Application** if users will authorise your app themselves.
3. Note the **Client ID** and **Client Secret**.
4. Generate a **refresh token** with the scopes your integration needs — see
   [Authentication](authentication.md).

::: warning Keep credentials out of source control
The client secret and refresh token are long-lived credentials. Read them from
environment variables or a secret manager; never commit them and never ship them
in client-side code.
:::

## Construct the client

```{lang.fence}
{lang.snippets['construct']}
```

## Get a scoped instance

The client hands out four scoped objects. Each one binds the identifiers it
needs, so you do not repeat them on every call.

```{lang.fence}
{lang.snippets['instances']}
```

| Instance | Bound to | Use for |
|---|---|---|
| `OrgAPI` | organization | Users, roles, admins, subscription, security controls. |
| `WorkspaceAPI` | organization + workspace | Views, folders, schedules, alerts, backups, sharing. |
| `ViewAPI` | organization + workspace + view | Rows, columns, formulas, publishing. |
| `BulkAPI` | organization + workspace | Importing and exporting data. |

## Make a first call

```{lang.fence}
{lang.snippets['first_call']}
```

A successful call returns the `data` payload of the response envelope, already
decoded. A failure raises or returns {lang.error_type.split('(')[0].strip()}.

### Sample response

```json
{{
  "status": "success",
  "summary": "Get organizations",
  "data": {{
    "orgs": [
      {{
        "orgId": "55522777",
        "orgName": "Zylker Analytics",
        "orgDesc": "",
        "timeZone": "Asia/Kolkata",
        "role": "ORGADMIN"
      }}
    ]
  }}
}}
```

The SDK unwraps the envelope for you: the value you receive is the contents of
`data.orgs`, not the whole document above.

## Where to go next

- [Authentication](authentication.md) — **read the token throttle section before you ship.**
- [Errors](errors.md) — what to branch on when a call fails.
- [Importing data](guides/importing-data.md) — the three import modes and when to use each.
"""


# ======================================================================
# authentication  -- the critical page
# ======================================================================

def authentication(lang: Lang) -> str:
    return f"""# Authentication

Every request carries an OAuth 2.0 access token. The SDK obtains and refreshes
that token for you from the client ID, client secret and refresh token you
supply — but *how often you construct the client* determines whether that works
or gets you blocked.

::: danger The single most common way to break this SDK
Constructing a new `AnalyticsClient` for every request — per web request, per
cron tick, per job — discards the access token each time and forces a new one.
Zoho Accounts allows **ten access tokens per ten minutes per refresh token**.
Cross it and token creation is blocked for the next ten minutes, and every call
fails with `access denied`.

**Construct the client once, at application startup, and reuse that instance.**
:::

## The access token throttle

Zoho Accounts throws an `access denied` error when more than **ten access tokens**
are generated within **ten minutes** using the same refresh token. Once that
threshold is reached, Zoho Accounts blocks access token creation for the next ten
minutes.

This matters specifically for SDK users. Whenever you initiate the client
constructor, the existing access token is discarded and a new one is created on
the next API call. A service that builds a client per request therefore mints a
token per request, and crosses the limit after ten requests.

To avoid this, initiate the client object **only once** — during server startup,
as a module-level value, or behind a singleton — and use that same instance
throughout. The same access token is then used for all API calls. When the token
expires after an hour, the SDK handles regeneration itself.

Reference: <https://www.zoho.com/analytics/api/v2/authentication/refresh-token.html>

### What the failure looks like

```json
{{
  "error": "access_denied",
  "error_description": "You have made too many requests continuously. Please try again after some time."
}}
```

This comes from Zoho **Accounts**, not from the Analytics API, so it does not use
the usual Analytics failure envelope and does not carry an Analytics `errorCode`.
That is the signal you have hit the token throttle rather than an API error.

### Do this

```{lang.fence}
{lang.snippets['singleton']}
```

### Not this

```{lang.fence}
{_antipattern(lang)}
```

::: note Why one instance is safe
The token the client holds is valid for one hour. The SDK checks for expiry on
each call and regenerates the token in place when needed — which is one token
per hour, far below the limit. Sharing the instance is what keeps you under it.
:::

## Refresh token limits

| Limit | Value | What happens when you cross it |
|---|---|---|
| Access tokens per refresh token | 10 per 10 minutes | `access_denied` from Zoho Accounts; creation blocked for 10 minutes. |
| Access token lifetime | 1 hour (`expires_in: 3600`) | The SDK regenerates it on the next call. |
| Refresh tokens per client, per user | 20 | Creating a 21st silently deletes the oldest, breaking whatever used it. |

Refresh tokens do not expire on their own and do not change when used. Treat them
as permanent credentials until explicitly revoked.

## Scopes

Request the union of scopes across every endpoint your integration calls. Prefer
the narrowest set that works.

| Scope | Covers |
|---|---|
| `ZohoAnalytics.data.all` | Reading and writing row data. |
| `ZohoAnalytics.metadata.all` | Views, columns, folders, workspace structure. |
| `ZohoAnalytics.modeling.all` | Formulas, query tables, alerts, schedules. |
| `ZohoAnalytics.share.all` | Sharing and permissions. |
| `ZohoAnalytics.usermanagement.all` | Users, roles, admins. |
| `ZohoAnalytics.embed.all` | Embed URLs, private links, publishing. |
| `ZohoAnalytics.fullaccess.all` | Everything. Avoid unless you genuinely need it. |

Each `.all` scope can be narrowed to `.read`, `.create`, `.update` or `.delete`.

::: warning A token missing a scope fails at call time, not at construction
An under-scoped token constructs fine and fails on the first call that needs the
missing scope, with HTTP 401 and error code `8535`. Scope problems therefore look
like authentication problems. Check the scopes on the token before assuming the
credentials are wrong.
:::

## Data centers

An organization lives in exactly one data center. The API host, the OAuth
accounts host and the token must all belong to that same region.

{DATA_CENTERS}

```{lang.fence}
{lang.snippets['datacenter']}
```

::: warning Tokens are bound to their region
A token issued by `accounts.zoho.eu` is rejected by `analyticsapi.zoho.com` with
error `8535`. If authentication fails for no apparent reason, confirm the region
first — find it from the URL you use to sign in to Zoho Analytics in a browser.
:::

## Using a token you already hold

If another part of your system manages tokens, hand the SDK an access token
directly instead of letting it mint one.

```{lang.fence}
{lang.snippets['accesstoken']}
```

You are then responsible for refreshing it before it expires.

## Authorisation is a separate check

A valid token proves *who* is calling. Whether that user may perform the
operation is checked separately against their organization role, workspace role
and view permissions. Those failures return HTTP 403 with error code `7301`, not
a 401 — the token is fine; the user is not allowed.

## Related

- [Errors](errors.md) — the full failure envelope and the codes worth branching on.
- [Limits](limits.md) — API-side throttles, which are separate from this token limit.
- [Configuration](configuration.md) — timeouts, proxies and custom headers.
"""


def _antipattern(lang: Lang) -> str:
    """The per-request construction mistake, in each language's idiom."""
    return {
        "java": """// Every request mints a new access token. After ten requests inside ten
// minutes, Zoho Accounts blocks token creation for the next ten minutes.
public JSONArray handleRequest(long orgId, long workspaceId) throws Exception {
    AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
    return ac.getWorkspaceInstance(orgId, workspaceId).getViews(null);
}""",
        "python": """# Every request mints a new access token. After ten requests inside ten
# minutes, Zoho Accounts blocks token creation for the next ten minutes.
def handle_request(org_id, workspace_id):
    ac = AnalyticsClient(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
    return ac.get_workspace_instance(org_id, workspace_id).get_views()""",
        "csharp": """// Every request mints a new access token. After ten requests inside ten
// minutes, Zoho Accounts blocks token creation for the next ten minutes.
public JsonElement HandleRequest(long orgId, long workspaceId)
{
    IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
    return ac.GetWorkspaceInstance(orgId, workspaceId).GetViews(null);
}""",
        "go": """// Every request mints a new access token. After ten requests inside ten
// minutes, Zoho Accounts blocks token creation for the next ten minutes.
func handleRequest(orgId, workspaceId string) (interface{}, *ZAnalytics.ServerException) {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    return workspace.GetViews(map[string]interface{}{})
}""",
        "php": """// Every request mints a new access token. After ten requests inside ten
// minutes, Zoho Accounts blocks token creation for the next ten minutes.
function handle_request($org_id, $workspace_id) {
    $ac = new AnalyticsClient($client_id, $client_secret, $refresh_token);
    return $ac->getWorkspaceInstance($org_id, $workspace_id)->getViews();
}""",
        "nodejs": """// Every request mints a new access token. After ten requests inside ten
// minutes, Zoho Accounts blocks token creation for the next ten minutes.
app.get('/views', async function (req, res) {
    var ac = new analyticsClient(clientId, clientSecret, refreshToken);
    res.json(await ac.getWorkspaceInstance(orgId, workspaceId).getViews());
});""",
        "ruby": """# Every request mints a new access token. After ten requests inside ten
# minutes, Zoho Accounts blocks token creation for the next ten minutes.
def handle_request(org_id, workspace_id)
  ac = AnalyticsClient.new.with_data_center("US").with_oauth(credentials).build
  ac.get_workspace_instance(org_id, workspace_id).get_views
end""",
    }[lang.key]


# ======================================================================
# configuration
# ======================================================================

def configuration(lang: Lang) -> str:
    notes = "\n".join(f"- {n}" for n in lang.notes) if lang.notes else ""
    notes_block = f"\n## {lang.name} notes\n\n{notes}\n" if notes else ""
    return f"""# Configuration

Everything on this page is set on the client and applies to every call made
through it.

## Timeouts

Defaults are generous enough for interactive calls but not for large imports or
exports. Raise the read timeout before moving large files.

```{lang.fence}
{lang.snippets['timeouts']}
```

::: note Timeouts are not retries
A timeout aborts the HTTP request; it does not cancel work already started on the
server. An import that times out client-side may still land. Check the job status
before retrying — see [Importing data](guides/importing-data.md).
:::

## Proxy

```{lang.fence}
{lang.snippets['proxy']}
```

## Region

```{lang.fence}
{lang.snippets['datacenter']}
```

See [Authentication](authentication.md#data-centers) for the full host table.

## Request configuration

Most methods take a final `config` value carrying optional parameters for that
endpoint — filter criteria, output format, pagination and so on.

```{lang.fence}
{lang.snippets['headers']}
```

## Supplying an access token directly

```{lang.fence}
{lang.snippets['accesstoken']}
```
{notes_block}
## Related

- [Authentication](authentication.md) — credentials and the token throttle.
- [Errors](errors.md) — what a failure looks like.
"""


# ======================================================================
# errors
# ======================================================================

def errors(lang: Lang) -> str:
    return f"""# Errors

## The failure surface

{lang.error_type}

```{lang.fence}
{lang.snippets['errors']}
```

## The response envelope

The API has exactly three response shapes.

| Shape | HTTP | Body |
|---|---|---|
| Success with data | 200 | `{{"status":"success","summary":"...","data":{{...}}}}` |
| Success, nothing to return | 204 | Empty. |
| Failure | 4xx, 5xx | `{{"status":"failure","summary":"<CONSTANT>","data":{{"errorCode":<int>,"errorMessage":"..."}}}}` |

Synchronous export endpoints are the exception: on success they return the file
itself with a matching `Content-Type`, and only use the JSON envelope on failure.

### A failure response

```json
{{
  "status": "failure",
  "summary": "SECURITY_NOT_PERMITTED",
  "data": {{
    "errorCode": 7301,
    "errorMessage": "You (user@zylker.com) do not have the permission to do this operation."
  }}
}}
```

Branch on `errorCode`. `summary` is a stable constant you can log, and
`errorMessage` is localised prose — log it, do not parse it.

## HTTP status codes

| Status | Meaning | Retry? |
|---|---|---|
| **200** | Success with a payload. | — |
| **204** | Success, nothing to return. | — |
| **400** | The request is wrong: bad config, validation failure, business-rule violation, limit exceeded. | No. Fix the request. |
| **401** | Authentication failed — token missing, expired, revoked, under-scoped or from the wrong region. | Only after refreshing. |
| **403** | Authenticated but not allowed: missing role or permission, or a feature not on your plan. | No. |
| **404** | The organization, workspace or view in the path does not exist. | No. Fix the identifier. |
| **409** | Needs explicit confirmation, or conflicts with current state. | Yes, after acknowledging. |
| **500** | Unexpected server-side failure. | Yes, after a short delay. |

## Codes worth branching on

| Code | Constant | Meaning | What to do |
|---|---|---|---|
| `8535` | `INVALID_OAUTHTOKEN` | Token missing, expired, revoked, under-scoped, or issued in another region. | Check scopes and region. See [Authentication](authentication.md). |
| `8083` | `ORGID_NOT_PRESENT_IN_THE_HEADER` | Organization id missing. | The SDK sets this; it usually means the instance was built without an org id. |
| `7301` | `SECURITY_NOT_PERMITTED` | Authenticated user lacks the role or permission. | Change the caller or grant permission. Not retryable. |
| `7103` | — | Workspace does not exist, or is not visible to this user. | Check the workspace id and the user's access. |
| `7104` | — | View does not exist, or is not visible to this user. | Check the view id. |
| `8241` | — | Operation would touch system-tagged data. | Resend with `validateSystemTags: false` once you have confirmed. |
| `8132` | — | Too many concurrent export jobs (limit is 5 per organization). | Wait for a running job to finish. |
| `8133` | — | Resource is restricted for synchronous export: over one million rows, from a live connect workspace, or a dashboard or query table. | Use the asynchronous job flow. |
| `18072` | — | A refetch is already running for this table. | Wait; do not retry in a loop. |
| `7429` | — | A copy is already running for this workspace. | Wait for it to finish. |
| `7005` | — | Unexpected server error. | Retry after a short delay; escalate if persistent. |

::: warning Not every 400 is permanent
Concurrency guards (`18072`, `7429`, `8132`) come back as HTTP 400 but *are*
retryable once the operation they are guarding finishes. Retrying them
immediately in a tight loop will not help; waiting will.
:::

## A retry policy that works

- **Retry** 500s and the concurrency guards above, with exponential backoff.
- **Retry once** after a 401, having refreshed the token — but if you are
  constructing one client and reusing it, the SDK has already done this.
- **Never retry** 400 (other than the guards), 403 or 404. The request or the
  caller is wrong; repeating it just burns API units.
- **Back off for the full lockout** when throttled. See [Limits](limits.md).

## Related

- [Limits](limits.md) — throttles, quotas and concurrency guards.
- [Authentication](authentication.md) — the token throttle, which reports through
  Zoho Accounts rather than this envelope.
"""


# ======================================================================
# limits
# ======================================================================

def limits(lang: Lang) -> str:
    return f"""# Limits

Four independent mechanisms limit what an integration can do. They are enforced
separately and signal differently.

| Mechanism | Scope | Signal |
|---|---|---|
| OAuth token throttle | Per refresh token | `access_denied` from Zoho Accounts. See [Authentication](authentication.md#the-access-token-throttle). |
| Per-operation throttles | Per user, per operation | Request rejected for a lockout period. |
| Concurrency guards | One long-running operation per object | A specific error code such as `18072`, `7429`, `8132`. |
| Plan quotas | Per organization | Error when exhausted; visible through Get Resource Details. |

::: danger The token throttle is the one that bites first
Ten access tokens per ten minutes per refresh token. It is the limit most
integrations hit, and it is entirely avoidable — see
[Authentication](authentication.md#the-access-token-throttle).
:::

## Per-operation throttles

Counted per user. Crossing the threshold inside the window locks that user out of
the operation for the lockout period.

| Operation | Limit | Lockout |
|---|---|---|
| Create Query Table | 7 / user / 60s (15/min service-wide) | 5 minutes |
| Edit Query Table | 7 / user / 60s (15/min service-wide) | 5 minutes |
| Get Custom Formulas | 30 / user / 60s | 10 minutes |
| Add Custom Formula | 20 / user / 60s | 10 minutes |
| Edit Custom Formula | 20 / user / 60s | 10 minutes |
| Delete Custom Formula | 30 / user / 60s | 10 minutes |
| Get Aggregate Formula | 30 / user / 60s | 10 minutes |
| Add Aggregate Formula | 20 / user / 60s | 10 minutes |
| Edit Aggregate Formula | 20 / user / 60s | 10 minutes |
| Delete Aggregate Formula | 20 / user / 60s | 10 minutes |
| Create Dashboard | 10 / user / 60s | 10 minutes |
| Update Dashboard | 10 / user / 60s | 10 minutes |
| Read Dashboard Metadata | 20 / user / 60s | — |

## Payload and job limits

| Limit | Value |
|---|---|
| Synchronous import, maximum file size | 20 MB per request |
| Synchronous export, payload ceiling | 100 MB |
| Batch import, maximum batch size | 100 MB per batch |
| Concurrent asynchronous export jobs | 5 per organization (error `8132`) |
| Export job and file retention | 1 hour from job completion |

::: limit When synchronous export is not allowed
Tables over one million rows, dashboards, query tables and live-connect views
cannot be exported synchronously — the call fails with `8133`. Use the
asynchronous job flow described in [Exporting data](guides/exporting-data.md).
:::

## Concurrency guards

| Guard | Error | Behaviour |
|---|---|---|
| One refetch per table | `18072` | A second refetch while one is running is rejected. |
| One copy per organization | `7429` | A second workspace copy is rejected while one runs. |
| Five export jobs per organization | `8132` | A sixth job is rejected. |

Waiting is the fix; backing off blindly without checking whether the blocking
operation finished is not.

## API units

Every call deducts API units from the organization's plan allowance, with the
cost depending on the operation. Current allocation, usage and remainder come
back from Get Resource Details under `resourceName: "apiUnits"`.

::: warning Single-row APIs are expensive at volume
Add Row, Update Row and Delete Row cost one API unit per row. Loading data row
by row will exhaust the quota quickly — use the import APIs instead. See
[Importing data](guides/importing-data.md).
:::

## Plan quotas visible through the API

`users`, `roUsers`, `workspaces`, `rows`, `queryTables`, `archivedrows`,
`scheduledImports`, `scheduledEmails`, `apiUnits`, `scheduledAlerts`,
`scheduledSnapshots`, `archiveschedule`, `financeMultiorgImports`,
`privateLinks`, `actionsByFlow`. A value of `"Unlimited"` means no cap.

## Related

- [Authentication](authentication.md) — the OAuth token throttle.
- [Errors](errors.md) — the codes these limits report through.
"""


# ======================================================================
# guides
# ======================================================================

def importing(lang: Lang) -> str:
    return f"""# Importing data

Three modes, chosen by file size and whether you need to wait for the result.

| Mode | File size | Blocking | Use when |
|---|---|---|---|
| Synchronous | up to 20 MB | Yes | Small files where you want the row counts immediately. |
| Batched | any | Yes | Large CSV files; the SDK splits and uploads them for you. |
| Asynchronous job | any | No | Large files where you want to poll for completion. |

::: warning Do not load data row by row
Add Row costs one API unit per row. Importing a file costs far less and is
dramatically faster. Use the row APIs for corrections, not for loading.
:::

## Synchronous import

```{lang.fence}
{lang.snippets['import_sync']}
```

### Import types

| Value | Behaviour |
|---|---|
| `APPEND` | Add every row. Duplicates are kept. |
| `TRUNCATEADD` | Delete all existing rows, then add. |
| `UPDATEADD` | Update rows matching the configured key, add the rest. |

::: note `UPDATEADD` needs a matching column
Set `matchingColumns` in the config, otherwise the server cannot tell which rows
to update and the call fails validation.
:::

### Sample response

```json
{{
  "status": "success",
  "summary": "Import data",
  "data": {{
    "importSummary": {{
      "totalColumnCount": 8,
      "selectedColumnCount": 8,
      "totalRowCount": 12500,
      "successRowCount": 12498,
      "warnings": 2,
      "importOperation": "updateadd"
    }},
    "importErrors": "2 rows were skipped: date value did not match the column format."
  }}
}}
```

::: warning A successful import can still skip rows
`status` is `success` whenever the request was processed. Compare
`successRowCount` against `totalRowCount` and inspect `importErrors` — rows with
unparseable values are skipped silently otherwise.
:::

## Batched import

For files over 20 MB. The SDK splits the file, uploads each batch, and returns a
job id.

```{lang.fence}
{lang.snippets['import_batch']}
```

Batch size is counted in rows. Keep each resulting batch under 100 MB.

### Sample job response

```json
{{
  "status": "success",
  "summary": "Get import job details",
  "data": {{
    "jobId": "35130000001343088",
    "jobStatus": "JOB COMPLETED",
    "importSummary": {{
      "totalRowCount": 2400000,
      "successRowCount": 2400000,
      "warnings": 0
    }}
  }}
}}
```

`jobStatus` is one of `JOB NOT STARTED`, `JOB IN PROGRESS`, `JOB COMPLETED` or
`JOB FAILED`.

::: note Driving the batches yourself
If you have already split the file, the batch endpoint can be driven directly:
send `batchKey: "start"` with `importType` and `autoIdentify` on the first batch,
reuse the returned `batchKey` on the rest, and set `isLastBatch: true` on the
final one to commit the job.
:::

## Related

- [Exporting data](exporting-data.md)
- [Limits](../limits.md) — file size ceilings and API unit costs.
- [Errors](../errors.md)
"""


def exporting(lang: Lang) -> str:
    return f"""# Exporting data

Two modes. Synchronous returns the file on the same call; asynchronous creates a
job you poll and then download.

| Mode | Ceiling | Use when |
|---|---|---|
| Synchronous | 100 MB | The resource is not one of the restricted ones below. |
| Asynchronous job | No practical ceiling | **Required** for any restricted resource, and for anything over the synchronous ceiling. |

The choice is not about convenience. Export Data API is restricted for the
resources below; for these you must use the asynchronous export, and the
synchronous call rejects them with `8133`:

- Tables having more than one million rows.
- Tables and Views from live connect workspaces.
- Dashboard and Query Table view types.

## Synchronous export

```{lang.fence}
{lang.snippets['export_sync']}
```

### Formats

| Format | Applies to |
|---|---|
| `csv`, `json`, `xml` | Tables, query tables, reports. |
| `xls` | Tables and reports. |
| `pdf`, `html` | Reports and dashboards. |
| `image` | Charts. |

::: limit Synchronous export is not always allowed
Tables over one million rows, dashboards, query tables and live-connect views
reject synchronous export with error `8133`. Use the asynchronous flow below.
:::

## Asynchronous export

Create the job, poll it, then download when it reports complete.

```{lang.fence}
{lang.snippets['export_async']}
```

### Sample job response

```json
{{
  "status": "success",
  "summary": "Get export job details",
  "data": {{
    "jobId": "35130000001343084",
    "jobStatus": "JOB COMPLETED",
    "downloadUrl": "https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/35130000001055707/exportjobs/35130000001343084/data",
    "expiryTime": "1735689600000"
  }}
}}
```

::: note Use the returned `downloadUrl`
It is fully qualified and already points at the correct data center. Do not
assemble download URLs by hand — they differ by region.
:::

::: warning Jobs and files expire one hour after the job completes
Both the job record and the generated file are retained for one hour from the
moment the job reports complete — not from when it was created. `expiryTime`
carries the exact deadline. Download as soon as the job completes, or create a
new job; nothing is recoverable afterwards.
:::

::: limit Five concurrent export jobs per organization
A sixth is rejected with error `8132`. Poll and drain the queue rather than
creating jobs in a loop.
:::

### Polling

Poll at a sensible interval — a few seconds for small exports, tens of seconds
for large ones. `jobStatus` moves through `JOB NOT STARTED`, `JOB IN PROGRESS`,
then `JOB COMPLETED` or `JOB FAILED`. Treat `JOB FAILED` as terminal; the
response carries the reason.

## Related

- [Importing data](importing-data.md)
- [Limits](../limits.md)
- [Errors](../errors.md)
"""
