# Configuration

Everything on this page is set on the client and applies to every call made
through it.

## Timeouts

Defaults are generous enough for interactive calls but not for large imports or
exports. Raise the read timeout before moving large files.

```java
ac.setConnectionTimeout(10000);   // milliseconds
ac.setReadTimeout(60000);

int connect = ac.getConnectionTimeout();
int read    = ac.getReadTimeout();
```

::: note Timeouts are not retries
A timeout aborts the HTTP request; it does not cancel work already started on the
server. An import that times out client-side may still land. Check the job status
before retrying — see [Importing data](guides/importing-data.md).
:::

## Proxy

```java
ac.setProxy("proxy.example.com", 8443, "proxyUser", "proxyPassword");
```

## Region

```java
// Point the client at the data center that hosts your organization.
ac.setAnalyticsServerURL("https://analyticsapi.zoho.eu");
ac.setAccountsServerURL("https://accounts.zoho.eu");
```

See [Authentication](authentication.md#data-centers) for the full host table.

## Request configuration

Most methods take a final `config` value carrying optional parameters for that
endpoint — filter criteria, output format, pagination and so on.

```java
// Key accepts alphanumerics and hyphens only; the value may not contain newlines.
ac.setHeaders("X-Custom-Source", "nightly-sync");
```

## Supplying an access token directly

```java
// Supply a token you already hold instead of letting the SDK mint one.
ac.setAccessToken("1000.xxxxxxx.xxxxxxx");
```

## Java notes

- Every API method declares `ServerException`, `ParseException`, `IOException` and `JSONException`.
- `config` parameters accept `null` when you have nothing to add.

## Related

- [Authentication](authentication.md) — credentials and the token throttle.
- [Errors](errors.md) — what a failure looks like.
