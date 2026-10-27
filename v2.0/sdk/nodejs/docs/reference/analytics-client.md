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

`AnalyticsClient` exposes **8 methods**. Method names are `camelCase` and identifiers are `string`.

## Methods

[`getBulkInstance`](#getbulkinstance), [`getOrgInstance`](#getorginstance), [`getViewInstance`](#getviewinstance), [`getWorkspaceInstance`](#getworkspaceinstance), [`parseCSV`](#parsecsv), [`sendBatchImportRequest`](#sendbatchimportrequest), [`sleep`](#sleep), [`stringifyCSV`](#stringifycsv)

### getBulkInstance

```javascript
getBulkInstance(orgId, workspaceId)
```

Returns a new BulkAPI instance.

| Parameter | Type | Description |
|---|---|---|
| `orgId` | `String` | The ID of the organization. |
| `workspaceId` | `String` | The ID of the workspace. |

### getOrgInstance

```javascript
getOrgInstance(orgId)
```

Returns a new OrgAPI instance.

| Parameter | Type | Description |
|---|---|---|
| `orgId` | `String` | The ID of the organization. |

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

### getWorkspaceInstance

```javascript
getWorkspaceInstance(orgId, workspaceId)
```

Returns a new WorkspaceAPI instance.

| Parameter | Type | Description |
|---|---|---|
| `orgId` | `String` | The ID of the organization. |
| `workspaceId` | `String` | The ID of the workspace. |

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
