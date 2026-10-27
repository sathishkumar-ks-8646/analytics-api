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

`AnalyticsClient` exposes **4 methods**. Method names are `snake_case` and identifiers are `str`.

## Methods

[`get_bulk_instance`](#get-bulk-instance), [`get_org_instance`](#get-org-instance), [`get_view_instance`](#get-view-instance), [`get_workspace_instance`](#get-workspace-instance)

### get_bulk_instance

```python
get_bulk_instance(org_id, workspace_id)
```

Returns a new C{BulkAPI} instance.

| Parameter | Type | Description |
|---|---|---|
| `org_id` | `string` | The id of the organization. |
| `workspace_id` | `string` | The id of the workspace. |

### get_org_instance

```python
get_org_instance(org_id)
```

Returns a new C{OrgAPI} instance.

| Parameter | Type | Description |
|---|---|---|
| `org_id` | `string` | The id of the organization. |

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

### get_workspace_instance

```python
get_workspace_instance(org_id, workspace_id)
```

Returns a new C{WorkspaceAPI} instance.

| Parameter | Type | Description |
|---|---|---|
| `org_id` | `string` | The id of the organization. |
| `workspace_id` | `string` | The id of the workspace. |

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
