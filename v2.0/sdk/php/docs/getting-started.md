# Getting started

## Install

Require the client and make sure the cURL and JSON extensions are enabled:

```bash
php -m | grep -E 'curl|json'
```

```php
require 'AnalyticsClient.php';
```

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

```php
<?php
require 'AnalyticsClient.php';

$client_id     = "1000.xxxxxxx";
$client_secret = "xxxxxxx";
$refresh_token = "1000.xxxxxxx.xxxxxxx";

$ac = new AnalyticsClient($client_id, $client_secret, $refresh_token);
```

## Get a scoped instance

The client hands out four scoped objects. Each one binds the identifiers it
needs, so you do not repeat them on every call.

```php
$org       = $ac->getOrgInstance($org_id);
$workspace = $ac->getWorkspaceInstance($org_id, $workspace_id);
$view      = $ac->getViewInstance($org_id, $workspace_id, $view_id);
$bulk      = $ac->getBulkInstance($org_id, $workspace_id);
```

| Instance | Bound to | Use for |
|---|---|---|
| `OrgAPI` | organization | Users, roles, admins, subscription, security controls. |
| `WorkspaceAPI` | organization + workspace | Views, folders, schedules, alerts, backups, sharing. |
| `ViewAPI` | organization + workspace + view | Rows, columns, formulas, publishing. |
| `BulkAPI` | organization + workspace | Importing and exporting data. |

## Make a first call

```php
$ac = new AnalyticsClient($client_id, $client_secret, $refresh_token);

try {
    $org = $ac->getOrgInstance($org_id);
    $workspaces = $org->getOrgWorkspaces();
    print_r($workspaces);
}
catch (ServerException $se) {
    echo "Server error " . $se->getErrorCode() . ": " . $se->getErrorMessage() . "\n";
}
catch (ParseException $pe) {
    echo "Could not parse response: " . $pe->getErrorMessage() . "\n";
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
