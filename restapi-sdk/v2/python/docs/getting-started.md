# Getting started

## Install

Put `AnalyticsClient.py` on the import path and install its one dependency:

```bash
pip install requests
```

```python
from AnalyticsClient import AnalyticsClient
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

```python
from AnalyticsClient import AnalyticsClient

CLIENT_ID     = "1000.xxxxxxx"
CLIENT_SECRET = "xxxxxxx"
REFRESH_TOKEN = "1000.xxxxxxx.xxxxxxx"

ac = AnalyticsClient(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
```

## Get a scoped instance

The client hands out four scoped objects. Each one binds the identifiers it
needs, so you do not repeat them on every call.

```python
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

```python
from AnalyticsClient import AnalyticsClient, ServerError, ParseError

ac = AnalyticsClient(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)

try:
    orgs = ac.get_orgs()
    print(orgs)
except ServerError as err:
    print(f"Server error {err.errorCode}: {err.message}")
except ParseError as err:
    print(f"Could not parse response: {err}")
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
