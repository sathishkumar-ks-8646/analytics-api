# Authentication

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
{
  "error": "access_denied",
  "error_description": "You have made too many requests continuously. Please try again after some time."
}
```

This comes from Zoho **Accounts**, not from the Analytics API, so it does not use
the usual Analytics failure envelope and does not carry an Analytics `errorCode`.
That is the signal you have hit the token throttle rather than an API error.

### Do this

```javascript
// analytics.js -- one client for the whole process.
var analyticsClient = require('./AnalyticsClient');

// Node caches modules, so this constructor runs once no matter how many files
// require it. The access token is reused and refreshed in place when it expires.
var ac = new analyticsClient(
    process.env.ZOHO_CLIENT_ID,
    process.env.ZOHO_CLIENT_SECRET,
    process.env.ZOHO_REFRESH_TOKEN
);

module.exports = ac;

// Everywhere else in the application:
//     var ac = require('./analytics');
//     var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
```

### Not this

```javascript
// Every request mints a new access token. After ten requests inside ten
// minutes, Zoho Accounts blocks token creation for the next ten minutes.
app.get('/views', async function (req, res) {
    var ac = new analyticsClient(clientId, clientSecret, refreshToken);
    res.json(await ac.getWorkspaceInstance(orgId, workspaceId).getViews());
});
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

| Data center | API host | OAuth accounts host | Web application |
|---|---|---|---|
| United States | `analyticsapi.zoho.com` | `accounts.zoho.com` | `analytics.zoho.com` |
| Europe | `analyticsapi.zoho.eu` | `accounts.zoho.eu` | `analytics.zoho.eu` |
| India | `analyticsapi.zoho.in` | `accounts.zoho.in` | `analytics.zoho.in` |
| Australia | `analyticsapi.zoho.com.au` | `accounts.zoho.com.au` | `analytics.zoho.com.au` |
| Japan | `analyticsapi.zoho.jp` | `accounts.zoho.jp` | `analytics.zoho.jp` |
| China | `analyticsapi.zoho.com.cn` | `accounts.zoho.com.cn` | `analytics.zoho.com.cn` |
| Saudi Arabia | `analyticsapi.zoho.sa` | `accounts.zoho.sa` | `analytics.zoho.sa` |
| Canada | `analyticsapi.zohocloud.ca` | `accounts.zohocloud.ca` | `analytics.zohocloud.ca` |

```javascript
ac.setAnalyticsServerURL('https://analyticsapi.zoho.eu');
ac.setAccountsServerURL('https://accounts.zoho.eu');
```

::: warning Tokens are bound to their region
A token issued by `accounts.zoho.eu` is rejected by `analyticsapi.zoho.com` with
error `8535`. If authentication fails for no apparent reason, confirm the region
first — find it from the URL you use to sign in to Zoho Analytics in a browser.
:::

## Using a token you already hold

If another part of your system manages tokens, hand the SDK an access token
directly instead of letting it mint one.

```javascript
ac.setAccessToken('1000.xxxxxxx.xxxxxxx');
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
