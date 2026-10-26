# AnalyticsClient

```python
from AnalyticsClient import AnalyticsClient

CLIENT_ID     = "1000.xxxxxxx"
CLIENT_SECRET = "xxxxxxx"
REFRESH_TOKEN = "1000.xxxxxxx.xxxxxxx"

ac = AnalyticsClient(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
```

::: danger Construct this once
Creating a client per request exhausts the OAuth token allowance within ten calls. See [Authentication](../authentication.md#the-access-token-throttle).
:::

`AnalyticsClient` exposes **14 methods**. Method names are `snake_case` and identifiers are `str`.

## Methods

[`get_bulk_instance`](#get-bulk-instance), [`get_dashboards`](#get-dashboards), [`get_org_instance`](#get-org-instance), [`get_orgs`](#get-orgs), [`get_owned_dashboards`](#get-owned-dashboards), [`get_owned_workspaces`](#get-owned-workspaces), [`get_recent_views`](#get-recent-views), [`get_shared_dashboards`](#get-shared-dashboards), [`get_shared_workspaces`](#get-shared-workspaces), [`get_view_details`](#get-view-details), [`get_view_instance`](#get-view-instance), [`get_workspace_details`](#get-workspace-details), [`get_workspace_instance`](#get-workspace-instance), [`get_workspaces`](#get-workspaces)

### get_bulk_instance

```python
get_bulk_instance(org_id, workspace_id)
```

Returns a new C{BulkAPI} instance.

| Parameter | Type | Description |
|---|---|---|
| `org_id` | `string` | The id of the organization. |
| `workspace_id` | `string` | The id of the workspace. |

### get_dashboards

```python
get_dashboards()
```

Returns list of all accessible dashboards.

**Returns** (`list`) — Dashboard list.

**Raises** — `ServerError`; `ParseError`

### get_org_instance

```python
get_org_instance(org_id)
```

Returns a new C{OrgAPI} instance.

| Parameter | Type | Description |
|---|---|---|
| `org_id` | `string` | The id of the organization. |

### get_orgs

```python
get_orgs()
```

Returns list of all accessible organizations.

**Returns** (`list`) — Organization list.

**Raises** — `ServerError`; `ParseError`

### get_owned_dashboards

```python
get_owned_dashboards()
```

Returns list of owned dashboards.

**Returns** (`list`) — Dashboard list.

**Raises** — `ServerError`; `ParseError`

### get_owned_workspaces

```python
get_owned_workspaces()
```

Returns list of owned workspaces.

**Returns** (`list`) — Workspace list.

**Raises** — `ServerError`; `ParseError`

### get_recent_views

```python
get_recent_views()
```

Returns list of recently accessed views.

**Returns** (`list`) — View list.

**Raises** — `ServerError`; `ParseError`

### get_shared_dashboards

```python
get_shared_dashboards()
```

Returns list of shared dashboards.

**Returns** (`list`) — Dashboard list.

**Raises** — `ServerError`; `ParseError`

### get_shared_workspaces

```python
get_shared_workspaces()
```

Returns list of shared workspaces.

**Returns** (`list`) — Workspace list.

**Raises** — `ServerError`; `ParseError`

### get_view_details

```python
get_view_details(view_id, config = {})
```

Returns details of the specified view.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`dictionary`) — View details.

**Raises** — `ServerError`; `ParseError`

### get_view_instance

```python
get_view_instance(org_id, workspace_id, view_id)
```

Returns a new C{ViewAPI} instance.

| Parameter | Type | Description |
|---|---|---|
| `org_id` | `string` | The id of the organization. |
| `workspace_id` | `string` | The id of the workspace. |
| `view_id` | `string` | The id of the view. |

### get_workspace_details

```python
get_workspace_details(workspace_id)
```

Returns details of the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `workspace_id` | `string` | Id of the workspace. |

**Returns** (`dictionary`) — Workspace details.

**Raises** — `ServerError`; `ParseError`

### get_workspace_instance

```python
get_workspace_instance(org_id, workspace_id)
```

Returns a new C{WorkspaceAPI} instance.

| Parameter | Type | Description |
|---|---|---|
| `org_id` | `string` | The id of the organization. |
| `workspace_id` | `string` | The id of the workspace. |

### get_workspaces

```python
get_workspaces()
```

Returns list of all accessible workspaces.

**Returns** (`list`) — Workspace list.

**Raises** — `ServerError`; `ParseError`

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
