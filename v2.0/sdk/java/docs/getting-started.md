# Getting started

## Install

Add the SDK sources under `com/zoho/analytics/client` to your project and put
these on the classpath:

| Dependency | Why |
|---|---|
| `org.json` (for example `json-20231013.jar`) | Every request config and response is a `JSONObject` / `JSONArray`. |
| Apache Commons CSV (`zr-csv.jar`) | Used by the batched CSV import path. |

```bash
javac -cp json-20231013.jar:zr-csv.jar -sourcepath source -d out sample/test/Test.java
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

```java
import com.zoho.analytics.client.*;
import org.json.JSONObject;
import org.json.JSONArray;

String clientId     = "1000.xxxxxxx";
String clientSecret = "xxxxxxx";
String refreshToken = "1000.xxxxxxx.xxxxxxx";

AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
```

## Get a scoped instance

The client hands out four scoped objects. Each one binds the identifiers it
needs, so you do not repeat them on every call.

```java
OrgAPI       org       = ac.getOrgInstance(orgId);
WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
ViewAPI      view      = ac.getViewInstance(orgId, workspaceId, viewId);
BulkAPI      bulk      = ac.getBulkInstance(orgId, workspaceId);
```

| Instance | Bound to | Use for |
|---|---|---|
| `OrgAPI` | organization | Users, roles, admins, subscription, security controls. |
| `WorkspaceAPI` | organization + workspace | Views, folders, schedules, alerts, backups, sharing. |
| `ViewAPI` | organization + workspace + view | Rows, columns, formulas, publishing. |
| `BulkAPI` | organization + workspace | Importing and exporting data. |

## Make a first call

```java
AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);

try {
    OrgAPI org = ac.getOrgInstance(orgId);
    JSONArray workspaces = org.getOrgWorkspaces();
    System.out.println(workspaces);
}
catch (ServerException ex) {
    System.out.println("Server error " + ex.getErrorCode() + ": " + ex.getErrorMessage());
}
catch (ParseException ex) {
    System.out.println("Could not parse response: " + ex.getResponseMessage());
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
