# AnalyticsClient

```javascript
var analyticsClient = require('./AnalyticsClient');

var clientId     = '1000.xxxxxxx';
var clientSecret = 'xxxxxxx';
var refreshToken = '1000.xxxxxxx.xxxxxxx';

var ac = new analyticsClient(clientId, clientSecret, refreshToken);
```

::: danger Construct this once
Creating a client per request exhausts the OAuth token allowance within ten calls. See [Authentication](../authentication.md#the-access-token-throttle).
:::

`AnalyticsClient` exposes **18 methods**. Method names are `camelCase` and identifiers are `string`.

## Methods

[`getBulkInstance`](#getbulkinstance), [`getDashboards`](#getdashboards), [`getOrgInstance`](#getorginstance), [`getOrgs`](#getorgs), [`getOwnedDashboards`](#getowneddashboards), [`getOwnedWorkspaces`](#getownedworkspaces), [`getRecentViews`](#getrecentviews), [`getSharedDashboards`](#getshareddashboards), [`getSharedWorkspaces`](#getsharedworkspaces), [`getViewDetails`](#getviewdetails), [`getViewInstance`](#getviewinstance), [`getWorkspaceDetails`](#getworkspacedetails), [`getWorkspaceInstance`](#getworkspaceinstance), [`getWorkspaces`](#getworkspaces), [`parseCSV`](#parsecsv), [`sendBatchImportRequest`](#sendbatchimportrequest), [`sleep`](#sleep), [`stringifyCSV`](#stringifycsv)

### getBulkInstance

```javascript
getBulkInstance(orgId, workspaceId)
```

Returns a new BulkAPI instance.

| Parameter | Type | Description |
|---|---|---|
| `orgId` | `String` | The ID of the organization. |
| `workspaceId` | `String` | The ID of the workspace. |

### getDashboards

```javascript
getDashboards()
```

Returns list of all accessible dashboards.

**Returns** — Dashboard list.

**Raises** — `Error`

### getOrgInstance

```javascript
getOrgInstance(orgId)
```

Returns a new OrgAPI instance.

| Parameter | Type | Description |
|---|---|---|
| `orgId` | `String` | The ID of the organization. |

### getOrgs

```javascript
getOrgs()
```

Returns list of all accessible organizations.

**Returns** — Organization list.

**Raises** — `Error`

### getOwnedDashboards

```javascript
getOwnedDashboards()
```

Returns list of owned dashboards.

**Returns** — Dashboard list.

**Raises** — `Error`

### getOwnedWorkspaces

```javascript
getOwnedWorkspaces()
```

Returns list of owned workspaces.

**Returns** — Workspace list.

**Raises** — `Error`

### getRecentViews

```javascript
getRecentViews()
```

Returns list of recently accessed views.

**Returns** — View list.

**Raises** — `Error`

### getSharedDashboards

```javascript
getSharedDashboards()
```

Returns list of shared dashboards.

**Returns** — Dashboard list.

**Raises** — `Error`

### getSharedWorkspaces

```javascript
getSharedWorkspaces(config={})
```

Returns list of shared workspaces.

**Returns** — Workspace list.

**Raises** — `Error`

### getViewDetails

```javascript
getViewDetails(viewId, config={})
```

Returns details of the specified view.

| Parameter | Type | Description |
|---|---|---|
| `viewId` | `String` | The ID of the view. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — View details.

**Raises** — `Error`

### getViewInstance

```javascript
getViewInstance(orgId, workspaceId, viewId)
```

Returns a new ViewAPI instance.

| Parameter | Type | Description |
|---|---|---|
| `orgId` | `String` | The ID of the organization. |
| `workspaceId` | `String` | The ID of the workspace. |
| `viewId` | `String` | The ID of the view. |

### getWorkspaceDetails

```javascript
getWorkspaceDetails(workspaceId)
```

Returns details of the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `workspaceId` | `String` | The ID of the workspace. |

**Returns** — Workspace details.

**Raises** — `Error`

### getWorkspaceInstance

```javascript
getWorkspaceInstance(orgId, workspaceId)
```

Returns a new WorkspaceAPI instance.

| Parameter | Type | Description |
|---|---|---|
| `orgId` | `String` | The ID of the organization. |
| `workspaceId` | `String` | The ID of the workspace. |

### getWorkspaces

```javascript
getWorkspaces()
```

Returns list of all accessible workspaces.

**Returns** — Workspace list.

**Raises** — `Error`

### parseCSV

```javascript
parseCSV(content, delimiter = ',', quotechar = '"')
```

### sendBatchImportRequest

```javascript
sendBatchImportRequest(url, header, batch)
```

### sleep

```javascript
sleep(ms)
```

### stringifyCSV

```javascript
stringifyCSV(rows, delimiter = ',', quotechar = '"')
```

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
