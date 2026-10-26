# AnalyticsClient

```php
<?php
require 'AnalyticsClient.php';

$client_id     = "1000.xxxxxxx";
$client_secret = "xxxxxxx";
$refresh_token = "1000.xxxxxxx.xxxxxxx";

$ac = new AnalyticsClient($client_id, $client_secret, $refresh_token);
```

::: danger Construct this once
Creating a client per request exhausts the OAuth token allowance within ten calls. See [Authentication](../authentication.md#the-access-token-throttle).
:::

`AnalyticsClient` exposes **19 methods**. Method names are `camelCase` and identifiers are `string`.

## Methods

[`getBulkInstance`](#getbulkinstance), [`getConnectionTimeout`](#getconnectiontimeout), [`getDashboards`](#getdashboards), [`getOrgInstance`](#getorginstance), [`getOrgs`](#getorgs), [`getOwnedDashboards`](#getowneddashboards), [`getOwnedWorkspaces`](#getownedworkspaces), [`getReadTimeout`](#getreadtimeout), [`getRecentViews`](#getrecentviews), [`getSharedDashboards`](#getshareddashboards), [`getSharedWorkspaces`](#getsharedworkspaces), [`getViewDetails`](#getviewdetails), [`getViewInstance`](#getviewinstance), [`getWorkspaceDetails`](#getworkspacedetails), [`getWorkspaceInstance`](#getworkspaceinstance), [`getWorkspaces`](#getworkspaces), [`setConnectionTimeout`](#setconnectiontimeout), [`setProxy`](#setproxy), [`setReadTimeout`](#setreadtimeout)

### getBulkInstance

```php
getBulkInstance($org_id, $workspace_id)
```

Returns a new BulkAPI instance.

| Parameter | Type | Description |
|---|---|---|
| `org_id` | `string` | The ID of the organization. |
| `workspace_id` | `string` | The ID of the workspace. |

**Returns** — instance.

### getConnectionTimeout

```php
getConnectionTimeout()
```

Returns the timeout until a connection is established.A value of zero means the timeout is not used.

**Returns** — Connection timeout limit.

### getDashboards

```php
getDashboards()
```

Returns list of all accessible dashboards.

**Returns** — Dashboard list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getOrgInstance

```php
getOrgInstance($org_id)
```

Returns a new OrgAPI instance.

| Parameter | Type | Description |
|---|---|---|
| `org_id` | `string` | The ID of the organization. |

**Returns** — instance.

### getOrgs

```php
getOrgs()
```

Returns list of all accessible organizations.

**Returns** — Organization list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getOwnedDashboards

```php
getOwnedDashboards()
```

Returns list of owned dashboards.

**Returns** — Dashboard list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getOwnedWorkspaces

```php
getOwnedWorkspaces()
```

Returns list of owned workspaces.

**Returns** — Workspace list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getReadTimeout

```php
getReadTimeout()
```

Returns the timeout until waiting to read data. A value of zero means the timeout is not used. The default value is 15000.

**Returns** — Read timeout limit.

### getRecentViews

```php
getRecentViews()
```

Returns list of recently accessed views.

**Returns** — View list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getSharedDashboards

```php
getSharedDashboards()
```

Returns list of shared dashboards.

**Returns** — Dashboard list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getSharedWorkspaces

```php
getSharedWorkspaces()
```

Returns list of shared workspaces.

**Returns** — Workspace list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getViewDetails

```php
getViewDetails($view_id, $config = array()
```

Returns details of the specified view.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | The ID of the view. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — View details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getViewInstance

```php
getViewInstance($org_id, $workspace_id, $view_id)
```

Returns a new ViewAPI instance.

| Parameter | Type | Description |
|---|---|---|
| `org_id` | `string` | The ID of the organization. |
| `workspace_id` | `string` | The ID of the workspace. |
| `view_id` | `string` | The ID of the view. |

**Returns** — instance.

### getWorkspaceDetails

```php
getWorkspaceDetails($workspace_id)
```

Returns details of the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `workspace_id` | `string` | The ID of the workspace. |

**Returns** — Workspace details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getWorkspaceInstance

```php
getWorkspaceInstance($org_id, $workspace_id)
```

Returns a new WorkspaceAPI instance.

| Parameter | Type | Description |
|---|---|---|
| `org_id` | `string` | The ID of the organization. |
| `workspace_id` | `string` | The ID of the workspace. |

**Returns** — instance.

### getWorkspaces

```php
getWorkspaces()
```

Returns list of all accessible workspaces.

**Returns** — Workspace list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### setConnectionTimeout

```php
setConnectionTimeout($time_limit)
```

Sets the timeout until a connection is established. A value of zero means the timeout is not used. The default value is 15000.

| Parameter | Type | Description |
|---|---|---|
| `time_limit` | `int` | An integer value. |

### setProxy

```php
setProxy($proxy_host, $proxy_port, $proxy_type, $proxy_user_name, $proxy_password)
```

Used to specify the proxy server details.

| Parameter | Type | Description |
|---|---|---|
| `proxy_host` | `string` | The hostname/ip address of the proxy-server. |
| `proxy_port` | `int` | The proxy server port. |
| `proxy_type` | `string` | Can be any one ( HTTP , HTTPS , BOTH ).Specify "BOTH" if same configuration can be used for both HTTP and HTTPS. |
| `proxy_user_name` | `string` | The user name for proxy-server authentication. |
| `proxy_password` | `string` | The password for proxy-server authentication. |

### setReadTimeout

```php
setReadTimeout($time_limit)
```

Sets the timeout until waiting to read data. A value of zero means the timeout is not used. The default value is 15000.

| Parameter | Type | Description |
|---|---|---|
| `time_limit` | `int` | An integer value. |

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
