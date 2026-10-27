# Configuration

Everything on this page is set on the client and applies to every call made
through it.

## Timeouts

Defaults are generous enough for interactive calls but not for large imports or
exports. Raise the read timeout before moving large files.

```ruby
# Timeouts are part of the builder configuration.
ac = AnalyticsClient.new
       .with_data_center("US")
       .with_oauth(credentials)
       .build
```

::: note Timeouts are not retries
A timeout aborts the HTTP request; it does not cancel work already started on the
server. An import that times out client-side may still land. Check the job status
before retrying — see [Importing data](guides/importing-data.md).
:::

## Proxy

```ruby
ac = AnalyticsClient.new
       .with_data_center("US")
       .with_oauth(credentials)
       .with_proxy({
         "host"     => "proxy.example.com",
         "port"     => 8443,
         "user"     => "proxyUser",
         "password" => "proxyPassword"
       })
       .build
```

## Region

```ruby
# The data center is set on the builder, not by assembling URLs by hand.
# Accepted values: "US", "EU", "IN", "AU", "JP", "CN", "SA", "CA".
ac = AnalyticsClient.new
       .with_data_center("EU")
       .with_oauth(credentials)
       .build
```

See [Authentication](authentication.md#data-centers) for the full host table.

## Request configuration

Most methods take a final `config` value carrying optional parameters for that
endpoint — filter criteria, output format, pagination and so on.

```ruby
config = { "viewTypes" => ["0", "1"] }
views  = workspace.get_views(config)
```

## Supplying an access token directly

```ruby
# Encrypted on-disk token storage, so a restart does not mint a new token.
ac = AnalyticsClient.new
       .with_data_center("US")
       .with_oauth(credentials)
       .with_token_store_path("/var/lib/myapp/zoho-tokens")
       .build
```

## Ruby notes

- `with_token_store_path` stores the access token encrypted on disk, so a process restart reuses the existing token instead of minting a new one. Strongly recommended for short-lived processes such as cron jobs.
- `config` defaults to `{}`.

## Related

- [Authentication](authentication.md) — credentials and the token throttle.
- [Errors](errors.md) — what a failure looks like.
