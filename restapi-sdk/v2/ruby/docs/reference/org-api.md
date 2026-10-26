# OrgAPI

```ruby
org       = ac.get_org_instance(ORG_ID)
workspace = ac.get_workspace_instance(ORG_ID, WORKSPACE_ID)
view      = ac.get_view_instance(ORG_ID, WORKSPACE_ID, VIEW_ID)
bulk      = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)
```

`OrgAPI` exposes **19 methods**. Method names are `snake_case` and identifiers are `string`.

## Methods

[`activate_users`](#activate-users), [`add_users`](#add-users), [`change_user_role`](#change-user-role), [`create_custom_role`](#create-custom-role), [`create_workspace`](#create-workspace), [`deactivate_users`](#deactivate-users), [`delete_custom_role`](#delete-custom-role), [`get_admins`](#get-admins), [`get_automl_analysis`](#get-automl-analysis), [`get_custom_roles`](#get-custom-roles), [`get_linked_workspaces`](#get-linked-workspaces), [`get_meta_details`](#get-meta-details), [`get_org_access_restrictions`](#get-org-access-restrictions), [`get_resource_details`](#get-resource-details), [`get_subscription_details`](#get-subscription-details), [`get_users`](#get-users), [`remove_users`](#remove-users), [`update_custom_role`](#update-custom-role), [`update_org_access_restrictions`](#update-org-access-restrictions)

### activate_users

```ruby
activate_users(email_ids, config = {})
```

Activate users in the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `Array` | Email addresses to activate |
| `config` | `Hash` | Optional config |

### add_users

```ruby
add_users(email_ids, config = {})
```

Add users to the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `Array` | Email addresses to add |
| `config` | `Hash` | Optional config |

### change_user_role

```ruby
change_user_role(email_ids, role, config = {})
```

Change role for the specified users.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `Array` | Email addresses to modify |
| `role` | `String` | New role to assign |
| `config` | `Hash` | Optional config |

### create_custom_role

```ruby
create_custom_role(role_name, access_type, permissions, config = {})
```

Create a new custom role in the organization.

| Parameter | Type | Description |
|---|---|---|
| `role_name` | `String` | Name of the custom role to be created |
| `access_type` | `String` | Access type for the custom role |
| `permissions` | `Hash` | Permissions configuration |
| `config` | `Hash` | Additional control parameters |

**Returns** (`String`) — Created custom role id

### create_workspace

```ruby
create_workspace(workspace_name, config = {})
```

Create a blank workspace in the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `workspace_name` | `String` | The name of the workspace |
| `config` | `Hash` | Optional configuration parameters |

**Returns** (`Integer`) — Created workspace ID

### deactivate_users

```ruby
deactivate_users(email_ids, config = {})
```

Deactivate users in the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `Array` | Email addresses to deactivate |
| `config` | `Hash` | Optional config |

### delete_custom_role

```ruby
delete_custom_role(role_id)
```

Delete the specified custom role from the organization.

| Parameter | Type | Description |
|---|---|---|
| `role_id` | `String` | Id of the custom role to be deleted |

### get_admins

```ruby
get_admins()
```

Returns list of admins for a specified organization.

**Returns** (`Array`) — List of organization admins

### get_automl_analysis

```ruby
get_automl_analysis()
```

Returns all AutoML analyses available in the organization.

**Returns** (`Array`) — AutoML analysis list

### get_custom_roles

```ruby
get_custom_roles()
```

Returns list of all custom roles available in the organization.

**Returns** (`Array`) — Custom roles list

### get_linked_workspaces

```ruby
get_linked_workspaces()
```

Returns list of linked workspaces available in the specified organization.

**Returns** (`Array`) — Linked workspaces list

### get_meta_details

```ruby
get_meta_details(workspace_name, view_name = nil)
```

Returns metadata details of a workspace or a specific view.

| Parameter | Type | Description |
|---|---|---|
| `workspace_name` | `String` | Name of the workspace |
| `view_name` | `String, nil` | Name of the view (optional) |

**Returns** (`Hash`) — Metadata details

### get_org_access_restrictions

```ruby
get_org_access_restrictions()
```

Returns the access restriction settings configured for the organization.

**Returns** (`Hash`) — Organization access restriction settings

### get_resource_details

```ruby
get_resource_details()
```

Returns resource usage details of the specified organization.

**Returns** (`Hash`) — Resource usage details

### get_subscription_details

```ruby
get_subscription_details()
```

Returns subscription details of the specified organization.

**Returns** (`Hash`) — Subscription details

### get_users

```ruby
get_users()
```

Returns list of users for the specified organization.

**Returns** (`Array`) — List of users

### remove_users

```ruby
remove_users(email_ids, config = {})
```

Remove users from the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `Array` | Email addresses to remove |
| `config` | `Hash` | Optional config |

### update_custom_role

```ruby
update_custom_role(role_id, role_name, access_type, permissions, config = {})
```

Update the existing custom role in the organization.

| Parameter | Type | Description |
|---|---|---|
| `role_id` | `String` | Id of the custom role to be updated |
| `role_name` | `String` | New name for the custom role |
| `access_type` | `String` | New access type for the custom role |
| `permissions` | `Hash` | New permissions configuration |
| `config` | `Hash` | Additional control parameters |

### update_org_access_restrictions

```ruby
update_org_access_restrictions(config = {})
```

Update the access restriction settings of the organization.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | Contains the access restriction configurations to be updated |

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
