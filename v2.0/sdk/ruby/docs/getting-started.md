# Getting started

## Install

Install the gem and require it:

```bash
gem build zoho_analytics_client.gemspec
gem install zoho_analytics_client-*.gem
```

```ruby
require 'zoho_analytics_client'
```

Ruby is the one client built with a **builder**: set the data center and the
credentials, then call `build`.

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

```ruby
require 'zoho_analytics_client'

ac = AnalyticsClient.new
       .with_data_center("US")
       .with_oauth({
         "clientId"     => "1000.xxxxxxx",
         "clientSecret" => "xxxxxxx",
         "refreshToken" => "1000.xxxxxxx.xxxxxxx"
       })
       .build
```

## Get a scoped instance

The client hands out four scoped objects. Each one binds the identifiers it
needs, so you do not repeat them on every call.

```ruby
org       = ac.get_org_instance(ORG_ID)
workspace = ac.get_workspace_instance(ORG_ID, WORKSPACE_ID)
view      = ac.get_view_instance(ORG_ID, WORKSPACE_ID, VIEW_ID)
bulk      = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)
```

| Instance | Bound to | Use for |
|---|---|---|
| `OrgAPI` | organization | Users, roles, admins, subscription, security controls. |
| `WorkspaceAPI` | organization + workspace | Views, folders, schedules, alerts, backups, sharing. |
| `ViewAPI` | organization + workspace + view | Rows, columns, formulas, publishing. |
| `BulkAPI` | organization + workspace | Importing and exporting data. |

## Make a first call

```ruby
begin
  org = ac.get_org_instance(ORG_ID)
  puts org.get_org_workspaces
rescue ServerError => e
  puts "Server error #{e.error_code}: #{e.response_content}"
rescue StandardError => e
  puts e.message
end
```

A successful call returns the `data` payload of the response envelope, already
decoded. A failure raises or returns `ServerError`.

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
