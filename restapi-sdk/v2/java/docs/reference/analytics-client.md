# AnalyticsClient

```java
import com.zoho.analytics.client.*;
import org.json.JSONObject;
import org.json.JSONArray;

String clientId     = "1000.xxxxxxx";
String clientSecret = "xxxxxxx";
String refreshToken = "1000.xxxxxxx.xxxxxxx";

AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
```

::: danger Construct this once
Creating a client per request exhausts the OAuth token allowance within ten calls. See [Authentication](../authentication.md#the-access-token-throttle).
:::

`AnalyticsClient` exposes **23 methods**. Method names are `camelCase`, matching the endpoint title and identifiers are `long`.

## Methods

[`getBulkInstance`](#getbulkinstance), [`getConnectionTimeout`](#getconnectiontimeout), [`getDashboards`](#getdashboards), [`getOrgInstance`](#getorginstance), [`getOrgs`](#getorgs), [`getOwnedDashboards`](#getowneddashboards), [`getOwnedWorkspaces`](#getownedworkspaces), [`getReadTimeout`](#getreadtimeout), [`getRecentViews`](#getrecentviews), [`getSharedDashboards`](#getshareddashboards), [`getSharedWorkspaces`](#getsharedworkspaces), [`getViewDetails`](#getviewdetails), [`getViewInstance`](#getviewinstance), [`getWorkspaceDetails`](#getworkspacedetails), [`getWorkspaceInstance`](#getworkspaceinstance), [`getWorkspaces`](#getworkspaces), [`setAccessToken`](#setaccesstoken), [`setAccountsServerURL`](#setaccountsserverurl), [`setAnalyticsServerURL`](#setanalyticsserverurl), [`setConnectionTimeout`](#setconnectiontimeout), [`setHeaders`](#setheaders), [`setProxy`](#setproxy), [`setReadTimeout`](#setreadtimeout)

### getBulkInstance

```java
BulkAPI getBulkInstance(long orgId, long workspaceId)
```

Creates a new `BulkAPI` instance.

| Parameter | Description |
|---|---|
| `orgId` | The ID of the organization. |
| `workspaceId` | The ID of the workspace. |

**Returns** (`BulkAPI`) — BulkAPI instance.

### getConnectionTimeout

```java
int getConnectionTimeout()
```

Returns the timeout until a connection is established. A value of zero means the timeout is not used. The default value is 5000.

**Returns** (`int`) — A `int` value.

### getDashboards

```java
JSONObject getDashboards()
```

Returns list of all accessible dashboards.

**Returns** (`JSONObject`) — A `JSONObject` of dashboards list.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getOrgInstance

```java
OrgAPI getOrgInstance(long orgId)
```

Creates a new `OrgAPI` instance.

| Parameter | Description |
|---|---|
| `orgId` | The ID of the organization. |

**Returns** (`OrgAPI`) — OrgAPI instance.

### getOrgs

```java
JSONArray getOrgs()
```

Returns list of all accessible organizations.

**Returns** (`JSONArray`) — A `JSONArray` of organizations list.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getOwnedDashboards

```java
JSONArray getOwnedDashboards()
```

Returns list of owned dashboards.

**Returns** (`JSONArray`) — A `JSONArray` of owned dashboards list.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getOwnedWorkspaces

```java
JSONArray getOwnedWorkspaces()
```

Returns list of owned workspaces.

**Returns** (`JSONArray`) — A `JSONArray` of owned workspaces list.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getReadTimeout

```java
int getReadTimeout()
```

Returns the read timeout value which will wait for the packet to receive from the server end. The default value is 0.

**Returns** (`int`) — A `int` value.

### getRecentViews

```java
JSONArray getRecentViews()
```

Returns list of recently accessed views.

**Returns** (`JSONArray`) — A `JSONArray` of recent views list.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getSharedDashboards

```java
JSONArray getSharedDashboards()
```

Returns list of shared dashboards.

**Returns** (`JSONArray`) — A `JSONArray` of shared dashboards list.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getSharedWorkspaces

```java
JSONArray getSharedWorkspaces()
```

Returns list of shared workspaces.

**Returns** (`JSONArray`) — A `JSONArray` of shared workspaces list.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getViewDetails

```java
JSONObject getViewDetails(long viewId, JSONObject config)
```

Returns details of the specified view.

| Parameter | Description |
|---|---|
| `viewId` | The ID of the view. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JSONObject`) — A `JSONObject` of view details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getViewInstance

```java
ViewAPI getViewInstance(long orgId, long workspaceId, long viewId)
```

Creates a new `ViewAPI` instance.

| Parameter | Description |
|---|---|
| `orgId` | The ID of the organization. |
| `workspaceId` | The ID of the workspace. |
| `viewId` | The ID of the view. |

**Returns** (`ViewAPI`) — ViewAPI instance.

### getWorkspaceDetails

```java
JSONObject getWorkspaceDetails(long workspaceId)
```

Returns details of the specified workspace.

| Parameter | Description |
|---|---|
| `workspaceId` | The ID of the workspace. |

**Returns** (`JSONObject`) — A `JSONObject` of workspace details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getWorkspaceInstance

```java
WorkspaceAPI getWorkspaceInstance(long orgId, long workspaceId)
```

Creates a new `WorkspaceAPI` instance.

| Parameter | Description |
|---|---|
| `orgId` | The ID of the organization. |
| `workspaceId` | The ID of the workspace. |

**Returns** (`WorkspaceAPI`) — WorkspaceAPI instance.

### getWorkspaces

```java
JSONObject getWorkspaces()
```

Returns list of all accessible workspaces.

**Returns** (`JSONObject`) — A `JSONObject` of workspaces list.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### setAccessToken

```java
void setAccessToken(String accessToken)
```

### setAccountsServerURL

```java
void setAccountsServerURL(String serverURL)
```

Sets the accounts server URL.

| Parameter | Description |
|---|---|
| `serverURL` | The server URL. |

### setAnalyticsServerURL

```java
void setAnalyticsServerURL(String serverURL)
```

Sets the analytics server URL.

| Parameter | Description |
|---|---|
| `serverURL` | The server URL. |

### setConnectionTimeout

```java
void setConnectionTimeout(int timeout)
```

Sets the timeout until a connection is established. A value of zero means the timeout is not used. The default value is 5000.

| Parameter | Description |
|---|---|
| `timeout` | Contains connection timeout value. |

### setHeaders

```java
void setHeaders(String key, String value)
```

### setProxy

```java
void setProxy(String proxyHost, int proxyPort, String proxyUsername, String proxyPassword)
```

To specify the proxy server details. (When configuring the proxy settings, ensure that the 'Basic' authentication scheme is not disabled by the JDK).

| Parameter | Description |
|---|---|
| `proxyHost` | The hostname/IP address of the proxy server. |
| `proxyPort` | The proxy server port. |
| `proxyUsername` | The user name for proxy-server authentication. |
| `proxyPassword` | The password for proxy server authentication. |

### setReadTimeout

```java
void setReadTimeout(int timeout)
```

Sets the read timeout which will wait for data response from the server end. The default value is 0.

| Parameter | Description |
|---|---|
| `timeout` | Contains read timeout value. |

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
