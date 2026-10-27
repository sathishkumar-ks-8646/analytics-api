# OrgAPI

```python
org       = ac.get_org_instance(ORG_ID)
workspace = ac.get_workspace_instance(ORG_ID, WORKSPACE_ID)
view      = ac.get_view_instance(ORG_ID, WORKSPACE_ID, VIEW_ID)
bulk      = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)
```

`OrgAPI` exposes **23 methods**. Method names are `snake_case` and identifiers are `str`.

## Methods

[`activate_users`](#activate-users), [`add_users`](#add-users), [`change_user_role`](#change-user-role), [`create_custom_role`](#create-custom-role), [`create_workspace`](#create-workspace), [`deactivate_users`](#deactivate-users), [`delete_custom_role`](#delete-custom-role), [`get_admins`](#get-admins), [`get_automl_analysis`](#get-automl-analysis), [`get_custom_roles`](#get-custom-roles), [`get_linked_workspaces`](#get-linked-workspaces), [`get_meta_details`](#get-meta-details), [`get_org_access_restrictions`](#get-org-access-restrictions), [`get_org_dashboards`](#get-org-dashboards), [`get_org_recent_items`](#get-org-recent-items), [`get_org_workspaces`](#get-org-workspaces), [`get_resource_details`](#get-resource-details), [`get_subscription_details`](#get-subscription-details), [`get_users`](#get-users), [`get_view_details`](#get-view-details), [`remove_users`](#remove-users), [`update_custom_role`](#update-custom-role), [`update_org_access_restrictions`](#update-org-access-restrictions)

### activate_users

```python
activate_users(email_ids, config = {})
```

Activate users in the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `list` | The email address of the users to be activated. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### add_users

```python
add_users(email_ids, config = {})
```

Add users to the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `list` | The email address of the users to be added. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### change_user_role

```python
change_user_role(email_ids, role, config = {})
```

Change role for the specified users.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `list` | The email address of the users to be deactivated. |
| `role` | `string` | New role for the users. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### create_custom_role

```python
create_custom_role(role_name, access_type, permissions, config = {})
```

Create a new custom role in the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `role_name` | `string` | Name of the custom role to be created. |
| `access_type` | `string` | Access type for the custom role. |
| `permissions` | `dictionary` | Contains the permission details for the custom role. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Created custom role id.

**Raises** — `ServerError`; `ParseError`

### create_workspace

```python
create_workspace(workspace_name, config = {})
```

Create a blank workspace in the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `workspace_name` | `string` | The name of the workspace. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Created workspace id.

**Raises** — `ServerError`; `ParseError`

### deactivate_users

```python
deactivate_users(email_ids, config = {})
```

Deactivate users in the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `list` | The email address of the users to be deactivated. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### delete_custom_role

```python
delete_custom_role(role_id)
```

Delete the specified custom role from the organization.

| Parameter | Type | Description |
|---|---|---|
| `role_id` | `string` | Id of the custom role. |

**Raises** — `ServerError`; `ParseError`

### get_admins

```python
get_admins()
```

Returns list of admins for a specified organization.

**Returns** (`list`) — Organization admin list.

**Raises** — `ServerError`; `ParseError`

### get_automl_analysis

```python
get_automl_analysis()
```

Returns all the automl analysis available in an organization.

**Returns** (`list`) — AutoML analysis list.

**Raises** — `ServerError`; `ParseError`

### get_custom_roles

```python
get_custom_roles()
```

Returns list of custom roles for the specified organization.

**Returns** (`list`) — Custom role list.

**Raises** — `ServerError`; `ParseError`

### get_linked_workspaces

```python
get_linked_workspaces()
```

Returns list of linked workspaces available in the specified organization.

**Returns** (`list`) — Linked workspaces list.

**Raises** — `ServerError`; `ParseError`

### get_meta_details

```python
get_meta_details(workspace_name, view_name)
```

Returns details of the specified workspace/view.

| Parameter | Type | Description |
|---|---|---|
| `workspace_name` | `string` | Name of the workspace. |
| `view_name` | `string` | Name of the view. |

**Returns** (`dictionary`) — Workspace (or) View meta details.

**Raises** — `ServerError`; `ParseError`

### get_org_access_restrictions

```python
get_org_access_restrictions()
```

Returns the access restriction settings configured for the organization.

**Returns** (`dictionary`) — Organization access restriction settings.

**Raises** — `ServerError`; `ParseError`

### get_org_dashboards

```python
get_org_dashboards(config = {})
```

Returns the dashboards of the specified organization that the authenticated user may read, across the workspaces the user can reach or across the workspaces named in config["workspaceIds"].

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`dictionary`) — Dashboard list along with the paging details.

**Raises** — `ServerError`; `ParseError`

### get_org_recent_items

```python
get_org_recent_items()
```

Returns the views the authenticated user opened most recently in the specified organization, newest first. At most 20 items are returned.

**Returns** (`list`) — View list.

**Raises** — `ServerError`; `ParseError`

### get_org_workspaces

```python
get_org_workspaces()
```

Returns the workspaces of the specified organization that the authenticated user can reach. An Account Admin and an Organization Admin receive every active workspace of the organization. Every other user receives only the workspaces shared with them.

**Returns** (`list`) — Workspace list.

**Raises** — `ServerError`; `ParseError`

### get_resource_details

```python
get_resource_details()
```

Returns resource usage details of the specified organization.

**Returns** (`dictionary`) — Resource details.

**Raises** — `ServerError`; `ParseError`

### get_subscription_details

```python
get_subscription_details()
```

Returns subscription details of the specified organization.

**Returns** (`dictionary`) — Subscription details.

**Raises** — `ServerError`; `ParseError`

### get_users

```python
get_users()
```

Returns list of users for the specified organization.

**Returns** (`list`) — User list.

**Raises** — `ServerError`; `ParseError`

### get_view_details

```python
get_view_details(view_id, config = {})
```

Returns details of the specified view in the organization.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`dictionary`) — View details.

**Raises** — `ServerError`; `ParseError`

### remove_users

```python
remove_users(email_ids, config = {})
```

Remove users from the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `list` | The email address of the users to be removed. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### update_custom_role

```python
update_custom_role(role_id, role_name, access_type, permissions, config = {})
```

Update the specified custom role in the organization.

| Parameter | Type | Description |
|---|---|---|
| `role_id` | `string` | Id of the custom role. |
| `role_name` | `string` | New name for the custom role. |
| `access_type` | `string` | Access type for the custom role. |
| `permissions` | `dictionary` | Contains the permission details for the custom role. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### update_org_access_restrictions

```python
update_org_access_restrictions(config = {})
```

Update the access restriction settings of the organization.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains the access restriction configurations to be updated. |

**Raises** — `ServerError`; `ParseError`

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
