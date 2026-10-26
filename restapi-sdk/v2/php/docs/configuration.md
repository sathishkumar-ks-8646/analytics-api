# Configuration

Everything on this page is set on the client and applies to every call made
through it.

## Timeouts

Defaults are generous enough for interactive calls but not for large imports or
exports. Raise the read timeout before moving large files.

```php
$ac->setConnectionTimeout(10);   // seconds
$ac->setReadTimeout(60);

$connect = $ac->getConnectionTimeout();
$read    = $ac->getReadTimeout();
```

::: note Timeouts are not retries
A timeout aborts the HTTP request; it does not cancel work already started on the
server. An import that times out client-side may still land. Check the job status
before retrying — see [Importing data](guides/importing-data.md).
:::

## Proxy

```php
// proxy_type is one of "HTTP", "HTTPS" or "BOTH".
$ac->setProxy("proxy.example.com", 8443, "BOTH", "proxyUser", "proxyPassword");
```

## Region

```php
$ac->setAnalyticsServerURL("https://analyticsapi.zoho.eu");
$ac->setAccountsServerURL("https://accounts.zoho.eu");
```

See [Authentication](authentication.md#data-centers) for the full host table.

## Request configuration

Most methods take a final `config` value carrying optional parameters for that
endpoint — filter criteria, output format, pagination and so on.

```php
$config = array(
    "viewTypes" => array("0", "1")
);
$views = $workspace->getViews($config);
```

## Supplying an access token directly

```php
$ac->setAccessToken("1000.xxxxxxx.xxxxxxx");
```

## PHP notes

- `config` defaults to `array()`; omit it when you have nothing to add.
- Responses are associative arrays, already JSON-decoded.

## Related

- [Authentication](authentication.md) — credentials and the token throttle.
- [Errors](errors.md) — what a failure looks like.
