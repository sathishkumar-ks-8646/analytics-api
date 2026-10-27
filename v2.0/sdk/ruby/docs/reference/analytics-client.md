# AnalyticsClient

```ruby
require 'zoho_analytics_client'

ac = AnalyticsClient.new
       .with_data_center("US")
       .with_oauth({
         "clientId"     => "1000.xxxxxxx",
         "clientSecret" => "xxxxxxx",
         "refreshToken" => "1000.xxxxxxx.xxxxxxx"
       })
       .build
```

::: danger Construct this once
Creating a client per request exhausts the OAuth token allowance within ten calls. See [Authentication](../authentication.md#the-access-token-throttle).
:::

`AnalyticsClient` exposes **15 methods**. Method names are `snake_case` and identifiers are `string`.

## Methods

[`get_accounts_server_url`](#get-accounts-server-url), [`get_analytics_server_url`](#get-analytics-server-url), [`get_bulk_instance`](#get-bulk-instance), [`get_org_instance`](#get-org-instance), [`get_view_instance`](#get-view-instance), [`get_workspace_instance`](#get-workspace-instance), [`new`](#new), [`set_access_token`](#set-access-token), [`set_accounts_server_url`](#set-accounts-server-url), [`set_analytics_server_url`](#set-analytics-server-url), [`with_access_token`](#with-access-token), [`with_data_center`](#with-data-center), [`with_oauth`](#with-oauth), [`with_proxy`](#with-proxy), [`with_token_store_path`](#with-token-store-path)

### get_accounts_server_url

```ruby
get_accounts_server_url()
```

Gets the current accounts server URL

**Returns** (`String`) — The current accounts server URL

### get_analytics_server_url

```ruby
get_analytics_server_url()
```

Gets the current analytics server URL

**Returns** (`String`) — The current analytics server URL

### get_bulk_instance

```ruby
get_bulk_instance(org_id, workspace_id)
```

Returns a new BulkAPI instance.

| Parameter | Type | Description |
|---|---|---|
| `org_id` | `String` | The id of the organization. |
| `workspace_id` | `String` | The id of the workspace. |

**Returns** (`BulkAPI`) — Bulk API instance

### get_org_instance

```ruby
get_org_instance(org_id)
```

Returns a new OrgAPI instance.

| Parameter | Type | Description |
|---|---|---|
| `org_id` | `String` | The id of the organization. |

**Returns** (`OrgAPI`) — Organization API instance

### get_view_instance

```ruby
get_view_instance(org_id, workspace_id, view_id)
```

Returns a new ViewAPI instance.

| Parameter | Type | Description |
|---|---|---|
| `org_id` | `String` | The id of the organization. |
| `workspace_id` | `String` | The id of the workspace. |
| `view_id` | `String` | The id of the view. |

**Returns** (`ViewAPI`) — View API instance

### get_workspace_instance

```ruby
get_workspace_instance(org_id, workspace_id)
```

Returns a new WorkspaceAPI instance.

| Parameter | Type | Description |
|---|---|---|
| `org_id` | `String` | The id of the organization. |
| `workspace_id` | `String` | The id of the workspace. |

**Returns** (`WorkspaceAPI`) — Workspace API instance

### new

```ruby
new()
```

### set_access_token

```ruby
set_access_token(token)
```

========== TOKEN HANDLING LOGIC ========== Sets the access token directly on the AnalyticsClient instance, bypassing the need for OAuth token refresh or regeneration.

### set_accounts_server_url

```ruby
set_accounts_server_url(url)
```

Sets the accounts server URL

| Parameter | Type | Description |
|---|---|---|
| `url` | `String` | The accounts server URL |

**Returns** (`String`) — The updated accounts server URL

### set_analytics_server_url

```ruby
set_analytics_server_url(url)
```

Sets the analytics server URL

| Parameter | Type | Description |
|---|---|---|
| `url` | `String` | The analytics server URL |

**Returns** (`String`) — The updated analytics server URL

### with_access_token

```ruby
with_access_token(token)
```

Sets a direct access token on the client, bypassing OAuth. Using this token disables automatic token refresh logic.

| Parameter | Type | Description |
|---|---|---|
| `token` | `String` | The direct access token string |

**Returns** (`Builder`) — Returns self for method chaining

### with_data_center

```ruby
with_data_center(dc)
```

Sets the Zoho Analytics data center for this client.

| Parameter | Type | Description |
|---|---|---|
| `dc` | `String` | Data center code, mandatory (e.g., "US", "EU") |

**Returns** (`Builder`) — Returns self for method chaining

### with_oauth

```ruby
with_oauth(oauth_hash)
```

Sets the OAuth credentials hash for authentication.

| Parameter | Type | Description |
|---|---|---|
| `oauth_hash` | `Hash` | OAuth credentials with keys: |

**Returns** (`Builder`) — Returns self for method chaining

### with_proxy

```ruby
with_proxy(proxy_details)
```

Sets the proxy configuration details.

| Parameter | Type | Description |
|---|---|---|
| `proxy_details` | `Hash` | Proxy settings with keys: |

**Returns** (`Builder`) — Returns self for method chaining

### with_token_store_path

```ruby
with_token_store_path(path)
```

Sets the path for encrypted token storage. Raises an error if the directory does not exist.

| Parameter | Type | Description |
|---|---|---|
| `path` | `String` | Filesystem directory to store encrypted tokens |

**Returns** (`Builder`) — Returns self for method chaining

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
