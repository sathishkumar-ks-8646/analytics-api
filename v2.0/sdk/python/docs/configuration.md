# Configuration

Everything on this page is set on the client and applies to every call made
through it.

## Timeouts

Defaults are generous enough for interactive calls but not for large imports or
exports. Raise the read timeout before moving large files.

```python
# The Python client exposes timeouts through the underlying requests session.
ac.request_timeout = (10, 60)   # (connect, read) in seconds
```

::: note Timeouts are not retries
A timeout aborts the HTTP request; it does not cancel work already started on the
server. An import that times out client-side may still land. Check the job status
before retrying — see [Importing data](guides/importing-data.md).
:::

## Proxy

```python
ac.set_proxy("proxy.example.com", "8443", "proxyUser", "proxyPassword")
```

## Region

```python
ac.analytics_server_url = "https://analyticsapi.zoho.eu"
ac.accounts_server_url = "https://accounts.zoho.eu"
```

See [Authentication](authentication.md#data-centers) for the full host table.

## Request configuration

Most methods take a final `config` value carrying optional parameters for that
endpoint — filter criteria, output format, pagination and so on.

```python
# Any extra headers are merged into every request.
ac.default_headers = {"X-Custom-Source": "nightly-sync"}
```

## Supplying an access token directly

```python
# Supply a token you already hold instead of letting the SDK mint one.
ac.access_token = "1000.xxxxxxx.xxxxxxx"
```

## Python notes

- `config` defaults to `{}`; omit it when you have nothing to add.
- Streaming variants `export_data_stream()` and `export_bulk_data_stream()` return a `urllib3` response so large exports never have to be buffered in memory.

## Related

- [Authentication](authentication.md) — credentials and the token throttle.
- [Errors](errors.md) — what a failure looks like.
