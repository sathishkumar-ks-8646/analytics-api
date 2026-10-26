# AnalyticsClient

```csharp
using ZohoAnalytics;
using System.Collections.Generic;
using System.Text.Json;

string clientId     = "1000.xxxxxxx";
string clientSecret = "xxxxxxx";
string refreshToken = "1000.xxxxxxx.xxxxxxx";

IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
```

::: danger Construct this once
Creating a client per request exhausts the OAuth token allowance within ten calls. See [Authentication](../authentication.md#the-access-token-throttle).
:::

`AnalyticsClient` exposes **22 methods**. Method names are `PascalCase` and identifiers are `long`.

## Methods

[`GetBulkInstance`](#getbulkinstance), [`GetConnectionTimeout`](#getconnectiontimeout), [`GetDashboards`](#getdashboards), [`GetOrgInstance`](#getorginstance), [`GetOrgs`](#getorgs), [`GetOwnedDashboards`](#getowneddashboards), [`GetOwnedWorkspaces`](#getownedworkspaces), [`GetReadTimeout`](#getreadtimeout), [`GetRecentViews`](#getrecentviews), [`GetSharedDashboards`](#getshareddashboards), [`GetSharedWorkspaces`](#getsharedworkspaces), [`GetViewDetails`](#getviewdetails), [`GetViewInstance`](#getviewinstance), [`GetWorkspaceDetails`](#getworkspacedetails), [`GetWorkspaceInstance`](#getworkspaceinstance), [`GetWorkspaces`](#getworkspaces), [`SetAccountsServerURL`](#setaccountsserverurl), [`SetAnalyticsServerURL`](#setanalyticsserverurl), [`SetConnectionTimeout`](#setconnectiontimeout), [`SetDebugLogPath`](#setdebuglogpath), [`SetProxy`](#setproxy), [`SetReadTimeout`](#setreadtimeout)

### GetBulkInstance

```csharp
IBulkAPI GetBulkInstance(long orgId, long workspaceId)
```

Creates a new BulkAPI instance.

| Parameter | Description |
|---|---|
| `orgId` | The ID of the organization. |
| `workspaceId` | The ID of the workspace. |

**Returns** (`IBulkAPI`) — BulkAPI instance.

### GetConnectionTimeout

```csharp
int GetConnectionTimeout()
```

Returns the timeout until a connection is established.

**Returns** (`int`) — The timeout value.

### GetDashboards

```csharp
JsonElement GetDashboards()
```

Returns list of all accessible dashboards.

**Returns** (`JsonElement`) — All dashboards list.

### GetOrgInstance

```csharp
IOrgAPI GetOrgInstance(long orgId)
```

Creates a new OrgAPI instance.

| Parameter | Description |
|---|---|
| `orgId` | The ID of the organization. |

**Returns** (`IOrgAPI`) — OrgAPI instance.

### GetOrgs

```csharp
JsonElement GetOrgs()
```

Returns list of all accessible organizations.

**Returns** (`JsonElement`) — Organizations list.

### GetOwnedDashboards

```csharp
JsonElement GetOwnedDashboards()
```

Returns list of owned dashboards.

**Returns** (`JsonElement`) — Owned dashboards list.

### GetOwnedWorkspaces

```csharp
JsonElement GetOwnedWorkspaces()
```

Returns list of owned workspaces.

**Returns** (`JsonElement`) — Owned workspaces list.

### GetReadTimeout

```csharp
int GetReadTimeout()
```

Returns the read timeout value which will wait for the packet to receive from the server end.

**Returns** (`int`) — The timeout value.

### GetRecentViews

```csharp
JsonElement GetRecentViews()
```

Returns list of recently accessed views.

**Returns** (`JsonElement`) — Recent views list.

### GetSharedDashboards

```csharp
JsonElement GetSharedDashboards()
```

Returns list of shared dashboards.

**Returns** (`JsonElement`) — Shared dashboards list.

### GetSharedWorkspaces

```csharp
JsonElement GetSharedWorkspaces()
```

Returns list of shared workspaces.

**Returns** (`JsonElement`) — Shared workspaces list.

### GetViewDetails

```csharp
JsonElement GetViewDetails(long viewId, Dictionary config)
```

Returns details of the specified view.

| Parameter | Description |
|---|---|
| `viewId` | Id of the view. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JsonElement`) — View details.

### GetViewInstance

```csharp
IViewAPI GetViewInstance(long orgId, long workspaceId, long viewId)
```

Creates a new ViewAPI instance.

| Parameter | Description |
|---|---|
| `orgId` | The ID of the organization. |
| `workspaceId` | The ID of the workspace. |
| `viewId` | The ID of the view. |

**Returns** (`IViewAPI`) — ViewAPI instance.

### GetWorkspaceDetails

```csharp
JsonElement GetWorkspaceDetails(long workspaceId)
```

Returns details of the specified workspace.

| Parameter | Description |
|---|---|
| `workspaceId` | Id of the workspace. |

**Returns** (`JsonElement`) — Workspace details.

### GetWorkspaceInstance

```csharp
IWorkspaceAPI GetWorkspaceInstance(long orgId, long workspaceId)
```

Creates a new WorkspaceAPI instance.

| Parameter | Description |
|---|---|
| `orgId` | The ID of the organization. |
| `workspaceId` | The ID of the workspace. |

**Returns** (`IWorkspaceAPI`) — WorkspaceAPI instance.

### GetWorkspaces

```csharp
JsonElement GetWorkspaces()
```

Returns list of all accessible workspaces.

**Returns** (`JsonElement`) — All workspaces list.

### SetAccountsServerURL

```csharp
void SetAccountsServerURL(string serverUrl)
```

Sets the accounts server URL.

| Parameter | Description |
|---|---|
| `serverUrl` | ZohoAccounts server URL |

### SetAnalyticsServerURL

```csharp
void SetAnalyticsServerURL(string serverUrl)
```

Sets the analytics server URL.

| Parameter | Description |
|---|---|
| `serverUrl` | ZohoAnalytics server URL |

### SetConnectionTimeout

```csharp
void SetConnectionTimeout(int timeout)
```

Sets the timeout until a connection is established.

| Parameter | Description |
|---|---|
| `timeout` | The timeout value. |

### SetDebugLogPath

```csharp
void SetDebugLogPath(string logFilePath)
```

Sets the file path for the debug log. Call this before making any API calls.

| Parameter | Description |
|---|---|
| `logFilePath` | Full path to the log file. E.g. "C:\Logs\ZohoAnalytics.log" |

### SetProxy

```csharp
void SetProxy(string proxyHost, int proxyPort, string proxyUsername, string proxyPassword)
```

To specify the proxy server details.

| Parameter | Description |
|---|---|
| `proxyHost` | The hostname/IP address of the proxy server. |
| `proxyPort` | The proxy server port. |
| `proxyUsername` | The user name for proxy-server authentication. |
| `proxyPassword` | The password for proxy server authentication. |

### SetReadTimeout

```csharp
void SetReadTimeout(int timeout)
```

Sets the read timeout which will wait for data response from the server end.

| Parameter | Description |
|---|---|
| `timeout` | The timeout value. |

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
