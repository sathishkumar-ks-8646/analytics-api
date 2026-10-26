# Getting started

## Install

Reference the `ZohoAnalytics` project (`source/ZohoAnalytics.csproj`, `net6.0`) or
build it into a library:

```bash
dotnet build source/ZohoAnalytics.csproj -c Release
```

```csharp
using ZohoAnalytics;
using System.Text.Json;
```

Responses are `System.Text.Json.JsonElement`; request configuration is
`Dictionary<string, object>`.

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

```csharp
using ZohoAnalytics;
using System.Collections.Generic;
using System.Text.Json;

string clientId     = "1000.xxxxxxx";
string clientSecret = "xxxxxxx";
string refreshToken = "1000.xxxxxxx.xxxxxxx";

IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
```

## Get a scoped instance

The client hands out four scoped objects. Each one binds the identifiers it
needs, so you do not repeat them on every call.

```csharp
IOrgAPI       org       = ac.GetOrgInstance(orgId);
IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
IViewAPI      view      = ac.GetViewInstance(orgId, workspaceId, viewId);
IBulkAPI      bulk      = ac.GetBulkInstance(orgId, workspaceId);
```

| Instance | Bound to | Use for |
|---|---|---|
| `OrgAPI` | organization | Users, roles, admins, subscription, security controls. |
| `WorkspaceAPI` | organization + workspace | Views, folders, schedules, alerts, backups, sharing. |
| `ViewAPI` | organization + workspace + view | Rows, columns, formulas, publishing. |
| `BulkAPI` | organization + workspace | Importing and exporting data. |

## Make a first call

```csharp
IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);

try
{
    JsonElement orgs = ac.GetOrgs();
    Console.WriteLine(orgs);
}
catch (ServerException ex)
{
    Console.WriteLine($"HTTP {ex.GetHTTPStatusCode()} / {ex.GetErrorCode()}: {ex.GetErrorMessage()}");
}
```

A successful call returns the `data` payload of the response envelope, already
decoded. A failure raises or returns `ServerException`.

### Sample response

```json
{
  "status": "success",
  "summary": "Get organizations",
  "data": {
    "orgs": [
      {
        "orgId": "55522777",
        "orgName": "Zylker Analytics",
        "orgDesc": "",
        "timeZone": "Asia/Kolkata",
        "role": "ORGADMIN"
      }
    ]
  }
}
```

The SDK unwraps the envelope for you: the value you receive is the contents of
`data.orgs`, not the whole document above.

## Where to go next

- [Authentication](authentication.md) — **read the token throttle section before you ship.**
- [Errors](errors.md) — what to branch on when a call fails.
- [Importing data](guides/importing-data.md) — the three import modes and when to use each.
