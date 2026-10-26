# AnalyticsClient

```go
package main

import (
    "fmt"
    ZAnalytics "zoho/pkg/analyticsclient"
)

var (
    clientId     = "1000.xxxxxxx"
    clientSecret = "xxxxxxx"
    refreshToken = "1000.xxxxxxx.xxxxxxx"
)

ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
```

::: danger Construct this once
Creating a client per request exhausts the OAuth token allowance within ten calls. See [Authentication](../authentication.md#the-access-token-throttle).
:::

`AnalyticsClient` exposes **10 methods**. Method names are `PascalCase` (exported) and identifiers are `string`.

## Methods

[`GetDashboards`](#getdashboards), [`GetOrgs`](#getorgs), [`GetOwnedDashboards`](#getowneddashboards), [`GetOwnedWorkspaces`](#getownedworkspaces), [`GetRecentViews`](#getrecentviews), [`GetSharedDashboards`](#getshareddashboards), [`GetSharedWorkspaces`](#getsharedworkspaces), [`GetViewDetails`](#getviewdetails), [`GetWorkspaceDetails`](#getworkspacedetails), [`GetWorkspaces`](#getworkspaces)

### GetDashboards

```go
GetDashboards() (dashboards map[string]interface{}, serverexception *ServerException)
```

Returns the list of all accessible dashboards.

**Returns** — Returns the owned and shared dashboards as map.

### GetOrgs

```go
GetOrgs() (orgs interface{}, serverexception *ServerException)
```

Returns list of all accessible organizations.

**Returns** — Returns org list as interface.

### GetOwnedDashboards

```go
GetOwnedDashboards() (views interface{}, serverexception *ServerException)
```

Returns the list of dashboards owned by the user.

**Returns** — Returns the owned dashboards as interface.

### GetOwnedWorkspaces

```go
GetOwnedWorkspaces() (workspaces interface{}, serverexception *ServerException)
```

Returns list of owned workspaces.

**Returns** — Returns workspace list as interface.

### GetRecentViews

```go
GetRecentViews() (views interface{}, serverexception *ServerException)
```

Returns list of recently accessed views.

**Returns** — Returns view list as interface.

### GetSharedDashboards

```go
GetSharedDashboards() (views interface{}, serverexception *ServerException)
```

Returns the list of dashboards shared to the user.

**Returns** — Returns the shared dashboards as interface.

### GetSharedWorkspaces

```go
GetSharedWorkspaces() (workspaces interface{}, serverexception *ServerException)
```

Returns list of shared workspaces.

**Returns** — Returns workspace list as interface.

### GetViewDetails

```go
GetViewDetails(viewid string, config map[string]interface{}) (viewDetails map[string]interface{}, serverexception *ServerException)
```

Returns details of the specified view.

| Parameter | Description |
|---|---|
| `viewid` | The ID of the view. |
| `config` | Contains the control configurations. |

**Returns** — Returns the view details as interface.

### GetWorkspaceDetails

```go
GetWorkspaceDetails(workspaceid string) (workspaceDetails map[string]interface{}, serverexception *ServerException)
```

Returns details of the specified workspace.

| Parameter | Description |
|---|---|
| `workspaceid` | The ID of the workspace. |

**Returns** — Returns workspace details as interface.

### GetWorkspaces

```go
GetWorkspaces() (workspaces map[string]interface{}, serverexception *ServerException)
```

Returns list of all accessible workspaces.

**Returns** — Returns workspace list as interface.

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
