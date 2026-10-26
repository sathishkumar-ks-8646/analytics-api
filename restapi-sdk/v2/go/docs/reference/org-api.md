# OrgAPI

```go
org       := ZAnalytics.GetOrgInstance(&ac, orgId)
workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
view      := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
bulk      := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
```

`OrgAPI` exposes **19 methods**. Method names are `PascalCase` (exported) and identifiers are `string`.

## Methods

[`ActivateUsers`](#activateusers), [`AddUsers`](#addusers), [`ChangeUserRole`](#changeuserrole), [`CreateCustomRole`](#createcustomrole), [`CreateWorkspace`](#createworkspace), [`DeactivateUsers`](#deactivateusers), [`DeleteCustomRole`](#deletecustomrole), [`GetAdmins`](#getadmins), [`GetAutoMLAnalysis`](#getautomlanalysis), [`GetCustomRoles`](#getcustomroles), [`GetLinkedWorkspaces`](#getlinkedworkspaces), [`GetMetaDetails`](#getmetadetails), [`GetOrgAccessRestrictions`](#getorgaccessrestrictions), [`GetResourceDetails`](#getresourcedetails), [`GetSubscriptionDetails`](#getsubscriptiondetails), [`GetUsers`](#getusers), [`RemoveUsers`](#removeusers), [`UpdateCustomRole`](#updatecustomrole), [`UpdateOrgAccessRestrictions`](#updateorgaccessrestrictions)

### ActivateUsers

```go
ActivateUsers(emailids interface{}, config map[string]interface{}) (serverexception *ServerException)
```

Activate users in the specified organization.

| Parameter | Description |
|---|---|
| `emailids` | The email address of the users to be activated. |
| `config` | Contains any additional control configurations. |

### AddUsers

```go
AddUsers(emailids interface{}, config map[string]interface{}) (serverexception *ServerException)
```

Add users to the specified organization.

| Parameter | Description |
|---|---|
| `emailids` | The email address of the users to be added. |
| `config` | Contains any additional control configurations. |

### ChangeUserRole

```go
ChangeUserRole(emailids interface{}, role string, config map[string]interface{}) (serverexception *ServerException)
```

Change role for the specified users.

| Parameter | Description |
|---|---|
| `emailids` | The email address of the users. |
| `role` | Name of the role to be updated. Can be one of "USER"/"VIEWER"/"ORGADMIN". |
| `config` | Contains any additional control configurations. |

### CreateCustomRole

```go
CreateCustomRole(rolename, accesstype string, permissions map[string]interface{}, config map[string]interface{}) (roleid string, serverexception *ServerException)
```

Create a new custom role in the organization.

| Parameter | Description |
|---|---|
| `rolename` | Name of the custom role. |
| `accesstype` | Access type for the custom role. |
| `permissions` | Permissions configuration for the custom role. |
| `config` | Contains any additional control configurations. |

**Returns** — Returns the new custom role id.

### CreateWorkspace

```go
CreateWorkspace(workspacename string, config map[string]interface{}) (workspaceid string, serverexception *ServerException)
```

Create a blank workspace in the specified organization.

| Parameter | Description |
|---|---|
| `workspacename` | Name of the workspace to be created. |
| `config` | Contains any additional control configurations. |

**Returns** — Returns the new workspace id.

### DeactivateUsers

```go
DeactivateUsers(emailids interface{}, config map[string]interface{}) (serverexception *ServerException)
```

Deactivate users in the specified organization.

| Parameter | Description |
|---|---|
| `emailids` | The email address of the users to be deactivated. |
| `config` | Contains any additional control configurations. |

### DeleteCustomRole

```go
DeleteCustomRole(roleid string) (serverexception *ServerException)
```

Delete the specified custom role from the organization.

| Parameter | Description |
|---|---|
| `roleid` | Id of the custom role to be deleted. |

### GetAdmins

```go
GetAdmins() (orgadmins interface{}, serverexception *ServerException)
```

Returns list of admins for a specified organization.

**Returns** — Returns orgadmin list as interface.

### GetAutoMLAnalysis

```go
GetAutoMLAnalysis() (analysis interface{}, serverexception *ServerException)
```

Returns list of automl analysis for the specified organization.

**Returns** — Returns AutoML analysis list as interface.

### GetCustomRoles

```go
GetCustomRoles() (roles interface{}, serverexception *ServerException)
```

Returns list of all custom roles available in the organization.

**Returns** — Returns custom role list as interface.

### GetLinkedWorkspaces

```go
GetLinkedWorkspaces() (linkedworkspaces interface{}, serverexception *ServerException)
```

Returns list of linked workspaces available in the specified organization.

**Returns** — Returns the linked workspaces list as interface.

### GetMetaDetails

```go
GetMetaDetails(workspacename, viewname string) (metadetails interface{}, serverexception *ServerException)
```

Returns details of the specified workspace/view.

| Parameter | Description |
|---|---|
| `workspacename` | The name of the workspace. |
| `viewname` | The name of the view. |

**Returns** — Returns details as interface.

### GetOrgAccessRestrictions

```go
GetOrgAccessRestrictions() (accessrestrictions interface{}, serverexception *ServerException)
```

Returns the access restriction settings configured for the organization.

**Returns** — Returns the organization access restriction settings as interface.

### GetResourceDetails

```go
GetResourceDetails() (resourceinfo interface{}, serverexception *ServerException)
```

Returns resource usage details of the specified organization.

**Returns** — Returns details as interface.

### GetSubscriptionDetails

```go
GetSubscriptionDetails() (subscriptioninfo interface{}, serverexception *ServerException)
```

Returns subscription details of the specified organization.

**Returns** — Returns details as interface.

### GetUsers

```go
GetUsers() (users interface{}, serverexception *ServerException)
```

Returns list of users for the specified organization.

**Returns** — Returns user list as interface.

### RemoveUsers

```go
RemoveUsers(emailids interface{}, config map[string]interface{}) (serverexception *ServerException)
```

Remove users from the specified organization.

| Parameter | Description |
|---|---|
| `emailids` | The email address of the users to be removed. |
| `config` | Contains any additional control configurations. |

### UpdateCustomRole

```go
UpdateCustomRole(roleid, rolename, accesstype string, permissions map[string]interface{}, config map[string]interface{}) (serverexception *ServerException)
```

Update the existing custom role in the organization.

| Parameter | Description |
|---|---|
| `roleid` | Id of the custom role to be updated. |
| `rolename` | New name for the custom role. |
| `accesstype` | New access type for the custom role. |
| `permissions` | New permissions configuration for the custom role. |
| `config` | Contains any additional control configurations. |

### UpdateOrgAccessRestrictions

```go
UpdateOrgAccessRestrictions(config map[string]interface{}) (serverexception *ServerException)
```

Update the access restriction settings of the organization.

| Parameter | Description |
|---|---|
| `config` | Contains the access restriction configurations to be updated. |

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
