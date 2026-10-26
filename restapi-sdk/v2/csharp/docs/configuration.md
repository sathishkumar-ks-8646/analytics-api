# Configuration

Everything on this page is set on the client and applies to every call made
through it.

## Timeouts

Defaults are generous enough for interactive calls but not for large imports or
exports. Raise the read timeout before moving large files.

```csharp
ac.SetConnectionTimeout(10000);   // milliseconds
ac.SetReadTimeout(60000);

int connect = ac.GetConnectionTimeout();
int read    = ac.GetReadTimeout();
```

::: note Timeouts are not retries
A timeout aborts the HTTP request; it does not cancel work already started on the
server. An import that times out client-side may still land. Check the job status
before retrying — see [Importing data](guides/importing-data.md).
:::

## Proxy

```csharp
ac.SetProxy("proxy.example.com", 8443, "proxyUser", "proxyPassword");
```

## Region

```csharp
ac.SetAnalyticsServerURL("https://analyticsapi.zoho.eu");
ac.SetAccountsServerURL("https://accounts.zoho.eu");
```

See [Authentication](authentication.md#data-centers) for the full host table.

## Request configuration

Most methods take a final `config` value carrying optional parameters for that
endpoint — filter criteria, output format, pagination and so on.

```csharp
// Diagnostic logging is off unless a path is supplied.
AnalyticsClient.SetDebugLogPath(@"C:\logs\zoho-analytics-sdk.log");
```

## Supplying an access token directly

```csharp
// Responses are JsonElement; read them with the System.Text.Json API.
JsonElement views = workspace.GetViews(null);
foreach (JsonElement v in views.EnumerateArray())
{
    Console.WriteLine(v.GetProperty("viewName").GetString());
}
```

## C# notes

- The interfaces (`IAnalyticsClient`, `IOrgAPI`, `IWorkspaceAPI`, `IViewAPI`, `IBulkAPI`) are the supported surface; code against them so the implementation stays swappable in tests.
- `config` accepts `null`.

## Related

- [Authentication](authentication.md) — credentials and the token throttle.
- [Errors](errors.md) — what a failure looks like.
