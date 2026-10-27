# Getting started

## Install

Require the client. Every method returns a Promise, so use `await` inside an
`async` function or chain `.then()` / `.catch()`.

```javascript
var analyticsClient = require('./AnalyticsClient');
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

```javascript
var analyticsClient = require('./AnalyticsClient');

var clientId     = '1000.xxxxxxx';
var clientSecret = 'xxxxxxx';
var refreshToken = '1000.xxxxxxx.xxxxxxx';

var ac = new analyticsClient(clientId, clientSecret, refreshToken);
```

## Get a scoped instance

The client hands out four scoped objects. Each one binds the identifiers it
needs, so you do not repeat them on every call.

```javascript
var org       = ac.getOrgInstance(orgId);
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
var view      = ac.getViewInstance(orgId, workspaceId, viewId);
var bulk      = ac.getBulkInstance(orgId, workspaceId);
```

| Instance | Bound to | Use for |
|---|---|---|
| `OrgAPI` | organization | Users, roles, admins, subscription, security controls. |
| `WorkspaceAPI` | organization + workspace | Views, folders, schedules, alerts, backups, sharing. |
| `ViewAPI` | organization + workspace + view | Rows, columns, formulas, publishing. |
| `BulkAPI` | organization + workspace | Importing and exporting data. |

## Make a first call

```javascript
var ac = new analyticsClient(clientId, clientSecret, refreshToken);

async function main() {
    try {
        var org = ac.getOrgInstance(orgId);
        var workspaces = await org.getOrgWorkspaces();
        console.log(workspaces);
    } catch (error) {
        console.log('Server error ' + error.errorCode + ': ' + error.errorMessage);
    }
}

main();
```

A successful call returns the `data` payload of the response envelope, already
decoded. A failure raises or returns A rejected Promise carrying `errorCode` and `errorMessage`..

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
