# OrgAPI

```php
$org       = $ac->getOrgInstance($org_id);
$workspace = $ac->getWorkspaceInstance($org_id, $workspace_id);
$view      = $ac->getViewInstance($org_id, $workspace_id, $view_id);
$bulk      = $ac->getBulkInstance($org_id, $workspace_id);
```

`OrgAPI` exposes **19 methods**. Method names are `camelCase` and identifiers are `string`.

## Methods

[`activateUsers`](#activateusers), [`addUsers`](#addusers), [`changeUserRole`](#changeuserrole), [`createCustomRole`](#createcustomrole), [`createWorkspace`](#createworkspace), [`deactivateUsers`](#deactivateusers), [`deleteCustomRole`](#deletecustomrole), [`getAdmins`](#getadmins), [`getAutoMLAnalysis`](#getautomlanalysis), [`getCustomRoles`](#getcustomroles), [`getLinkedWorkspaces`](#getlinkedworkspaces), [`getMetaDetails`](#getmetadetails), [`getOrgAccessRestrictions`](#getorgaccessrestrictions), [`getResourceDetails`](#getresourcedetails), [`getSubscriptionDetails`](#getsubscriptiondetails), [`getUsers`](#getusers), [`removeUsers`](#removeusers), [`updateCustomRole`](#updatecustomrole), [`updateOrgAccessRestrictions`](#updateorgaccessrestrictions)

### activateUsers

```php
activateUsers($email_ids, $config = array()
```

Activate users in the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `array()` | The email address of the users to be activated. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### addUsers

```php
addUsers($email_ids, $config = array()
```

Add users to the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `array()` | The email address of the users to be added. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### changeUserRole

```php
changeUserRole($email_ids, $role, $config = array()
```

Change role for the specified users.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `array()` | The email address of the users. |
| `role` | `string` | New role for the users. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### createCustomRole

```php
createCustomRole($role_name, $access_type, $permissions, $config = array()
```

Create a new custom role in the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `role_name` | `string` | Name of the custom role to be created. |
| `access_type` | `string` | Access type for the custom role. |
| `permissions` | `array` | Contains the permission details for the custom role. |
| `config` | `array` | Optional control parameters. |

**Returns** — Created custom role id.

### createWorkspace

```php
createWorkspace($workspace_name, $config = array()
```

Returns a new BulkAPI instance.

| Parameter | Type | Description |
|---|---|---|
| `workspace_name` | `string` | Name of the workspace. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Created workspace id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### deactivateUsers

```php
deactivateUsers($email_ids, $config = array()
```

Deactivate users in the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `array()` | The email address of the users to be deactivated. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### deleteCustomRole

```php
deleteCustomRole($role_id)
```

Delete the specified custom role from the organization.

| Parameter | Type | Description |
|---|---|---|
| `role_id` | `string` | Id of the custom role. |

### getAdmins

```php
getAdmins()
```

Returns list of admins for a specified organization.

**Returns** — Organization admin list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getAutoMLAnalysis

```php
getAutoMLAnalysis()
```

Returns all AutoML analysis available in an organization.

**Returns** — List of AutoML analysis.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getCustomRoles

```php
getCustomRoles()
```

Returns list of custom roles for the specified organization.

**Returns** — Custom role list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getLinkedWorkspaces

```php
getLinkedWorkspaces()
```

Returns list of linked workspaces available in the specified organization.

**Returns** — Linked workspaces list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getMetaDetails

```php
getMetaDetails($workspace_name, $view_name)
```

Returns details of the specified workspace/view.

| Parameter | Type | Description |
|---|---|---|
| `workspace_name` | `string` | Name of the workspace. |
| `view_name` | `string` | Name of the view. |

**Returns** — Workspace (or) View meta details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getOrgAccessRestrictions

```php
getOrgAccessRestrictions()
```

Returns the access restriction settings configured for the organization.

**Returns** — Organization access restriction settings.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getResourceDetails

```php
getResourceDetails()
```

Returns resource usage details of the specified organization.

**Returns** — Resource details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getSubscriptionDetails

```php
getSubscriptionDetails()
```

Returns subscription details of the specified organization.

**Returns** — Subscription details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getUsers

```php
getUsers()
```

Returns list of users for the specified organization.

**Returns** — User list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### removeUsers

```php
removeUsers($email_ids, $config = array()
```

Remove users from the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `array()` | The email address of the users to be removed. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### updateCustomRole

```php
updateCustomRole($role_id, $role_name, $access_type, $permissions, $config = array()
```

Update the specified custom role in the organization.

| Parameter | Type | Description |
|---|---|---|
| `role_id` | `string` | Id of the custom role. |
| `role_name` | `string` | New name for the custom role. |
| `access_type` | `string` | Access type for the custom role. |
| `permissions` | `array` | Contains the permission details for the custom role. |
| `config` | `array` | Optional control parameters. |

### updateOrgAccessRestrictions

```php
updateOrgAccessRestrictions($config = array()
```

Update the access restriction settings of the organization.

| Parameter | Type | Description |
|---|---|---|
| `config` | `array()` | Contains the access restriction configurations to be updated. |

**Raises** — `IOException`; `ServerException`; `ParseException`

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
