# Configuration

Everything on this page is set on the client and applies to every call made
through it.

## Timeouts

Defaults are generous enough for interactive calls but not for large imports or
exports. Raise the read timeout before moving large files.

```javascript
// Timeouts are supplied when the client is constructed.
var ac = new analyticsClient(clientId, clientSecret, refreshToken);
ac.requestTimeout = 60000;   // milliseconds
```

::: note Timeouts are not retries
A timeout aborts the HTTP request; it does not cancel work already started on the
server. An import that times out client-side may still land. Check the job status
before retrying — see [Importing data](guides/importing-data.md).
:::

## Proxy

```javascript
ac.setProxy('proxy.example.com', 8443, 'proxyUser', 'proxyPassword');
```

## Region

```javascript
ac.setAnalyticsServerURL('https://analyticsapi.zoho.eu');
ac.setAccountsServerURL('https://accounts.zoho.eu');
```

See [Authentication](authentication.md#data-centers) for the full host table.

## Request configuration

Most methods take a final `config` value carrying optional parameters for that
endpoint — filter criteria, output format, pagination and so on.

```javascript
var config = {
    'viewTypes': ['0', '1']
};
var views = await workspace.getViews(config);
```

## Supplying an access token directly

```javascript
ac.setAccessToken('1000.xxxxxxx.xxxxxxx');
```

## Node.js notes

- Unhandled rejections crash the process on modern Node; always attach a `catch` or wrap `await` in `try`.
- `config` defaults to `{}`.

## Related

- [Authentication](authentication.md) — credentials and the token throttle.
- [Errors](errors.md) — what a failure looks like.
