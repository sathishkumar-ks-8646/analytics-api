# Configuration

Everything on this page is set on the client and applies to every call made
through it.

## Timeouts

Defaults are generous enough for interactive calls but not for large imports or
exports. Raise the read timeout before moving large files.

```go
ac.SetConnectionTimeout(10)   // seconds
ac.SetReadTimeout(60)
```

::: note Timeouts are not retries
A timeout aborts the HTTP request; it does not cancel work already started on the
server. An import that times out client-side may still land. Check the job status
before retrying — see [Importing data](guides/importing-data.md).
:::

## Proxy

```go
ac.SetProxy("proxy.example.com", 8443, "proxyUser", "proxyPassword")
```

## Region

```go
ac.SetAnalyticsServerURL("https://analyticsapi.zoho.eu")
ac.SetAccountsServerURL("https://accounts.zoho.eu")
```

See [Authentication](authentication.md#data-centers) for the full host table.

## Request configuration

Most methods take a final `config` value carrying optional parameters for that
endpoint — filter criteria, output format, pagination and so on.

```go
// Config maps are plain map[string]interface{} values.
config := map[string]interface{}{
    "viewTypes": []string{"0", "1"},
}
views, exception := workspace.GetViews(config)
```

## Supplying an access token directly

```go
ac.SetAccessToken("1000.xxxxxxx.xxxxxxx")
```

## Go notes

- Results come back as `interface{}`; type-assert to `map[string]interface{}` or `[]interface{}` before reading fields.
- `ErrorCode` is a `float64` because it is decoded from JSON; cast with `int(...)` to compare.

## Related

- [Authentication](authentication.md) — credentials and the token throttle.
- [Errors](errors.md) — what a failure looks like.
