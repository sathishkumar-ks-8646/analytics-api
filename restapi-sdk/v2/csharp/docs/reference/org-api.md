# OrgAPI

```csharp
IOrgAPI       org       = ac.GetOrgInstance(orgId);
IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
IViewAPI      view      = ac.GetViewInstance(orgId, workspaceId, viewId);
IBulkAPI      bulk      = ac.GetBulkInstance(orgId, workspaceId);
```

`OrgAPI` exposes **19 methods**. Method names are `PascalCase` and identifiers are `long`.

## Methods

[`ActivateUsers`](#activateusers), [`AddUsers`](#addusers), [`ChangeUserRole`](#changeuserrole), [`CreateCustomRole`](#createcustomrole), [`CreateWorkspace`](#createworkspace), [`DeactivateUsers`](#deactivateusers), [`DeleteCustomRole`](#deletecustomrole), [`GetAdmins`](#getadmins), [`GetAutomlAnalysis`](#getautomlanalysis), [`GetCustomRoles`](#getcustomroles), [`GetLinkedWorkspaces`](#getlinkedworkspaces), [`GetMetaDetails`](#getmetadetails), [`GetOrgAccessRestrictions`](#getorgaccessrestrictions), [`GetResourceDetails`](#getresourcedetails), [`GetSubscriptionDetails`](#getsubscriptiondetails), [`GetUsers`](#getusers), [`RemoveUsers`](#removeusers), [`UpdateCustomRole`](#updatecustomrole), [`UpdateOrgAccessRestrictions`](#updateorgaccessrestrictions)

### ActivateUsers

```csharp
void ActivateUsers(List emailIds, Dictionary config)
```

Activate users in the specified organization.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the users to be activated. |
| `config` | Contains any additional control configurations. Can be null. |

### AddUsers

```csharp
void AddUsers(List emailIds, Dictionary config)
```

Add users to the specified organization.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the users to be added. |
| `config` | Contains any additional control configurations. Can be null. |

### ChangeUserRole

```csharp
void ChangeUserRole(List emailIds, string role, Dictionary config)
```

Change role for the specified users.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the users. |
| `role` | Name of the role to be updated. Can be one of "USER"/"VIEWER"/"ORGADMIN". |
| `config` | Contains any additional control configurations. Can be null. |

### CreateCustomRole

```csharp
long CreateCustomRole(string roleName, string accessType, Dictionary permissions, Dictionary config)
```

Create a new custom role in the organization.

| Parameter | Description |
|---|---|
| `roleName` | Name of the custom role. |
| `accessType` | Access type for the custom role. |
| `permissions` | Permissions configuration for the custom role. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — New custom role id.

### CreateWorkspace

```csharp
long CreateWorkspace(string workspaceName, Dictionary config)
```

Create a blank workspace in the specified organization.

| Parameter | Description |
|---|---|
| `workspaceName` | Name of the workspace. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — New workspace id.

### DeactivateUsers

```csharp
void DeactivateUsers(List emailIds, Dictionary config)
```

Deactivate users in the specified organization.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the users to be deactivated. |
| `config` | Contains any additional control configurations. Can be null. |

### DeleteCustomRole

```csharp
void DeleteCustomRole(long roleId)
```

Delete the specified custom role from the organization.

| Parameter | Description |
|---|---|
| `roleId` | Id of the custom role to be deleted. |

### GetAdmins

```csharp
JsonElement GetAdmins()
```

Returns list of admins for a specified organization.

**Returns** (`JsonElement`) — Organization admins list.

### GetAutomlAnalysis

```csharp
JsonElement GetAutomlAnalysis()
```

Returns all the AutoML analysis available in an organization.

**Returns** (`JsonElement`) — AutoML analysis list.

### GetCustomRoles

```csharp
JsonElement GetCustomRoles()
```

Returns list of all custom roles available in the organization.

**Returns** (`JsonElement`) — Custom roles list.

### GetLinkedWorkspaces

```csharp
JsonElement GetLinkedWorkspaces()
```

Returns list of linked workspaces available in the specified organization.

**Returns** (`JsonElement`) — Linked workspaces list.

### GetMetaDetails

```csharp
JsonElement GetMetaDetails(string workspaceName, string viewName)
```

Returns details of the specified workspace/view.

| Parameter | Description |
|---|---|
| `workspaceName` | The name of the workspace. |
| `viewName` | The name of the view. |

**Returns** (`JsonElement`) — Workspace/view details.

### GetOrgAccessRestrictions

```csharp
JsonElement GetOrgAccessRestrictions()
```

Returns the access restriction settings configured for the organization.

**Returns** (`JsonElement`) — Organization access restriction settings.

### GetResourceDetails

```csharp
JsonElement GetResourceDetails()
```

Returns resource usage details of the specified organization.

**Returns** (`JsonElement`) — Resource details.

### GetSubscriptionDetails

```csharp
JsonElement GetSubscriptionDetails()
```

Returns subscription details of the specified organization.

**Returns** (`JsonElement`) — Subscription details.

### GetUsers

```csharp
JsonElement GetUsers()
```

Returns list of users for the specified organization.

**Returns** (`JsonElement`) — List of users.

### RemoveUsers

```csharp
void RemoveUsers(List emailIds, Dictionary config)
```

Remove users from the specified organization.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the users to be removed. |
| `config` | Contains any additional control configurations. Can be null. |

### UpdateCustomRole

```csharp
void UpdateCustomRole(long roleId, string roleName, string accessType, Dictionary permissions, Dictionary config)
```

Update the existing custom role in the organization.

| Parameter | Description |
|---|---|
| `roleId` | Id of the custom role to be updated. |
| `roleName` | New name for the custom role. |
| `accessType` | New access type for the custom role. |
| `permissions` | New permissions configuration for the custom role. |
| `config` | Contains any additional control configurations. Can be null. |

### UpdateOrgAccessRestrictions

```csharp
void UpdateOrgAccessRestrictions(Dictionary config)
```

Update the access restriction settings of the organization.

| Parameter | Description |
|---|---|
| `config` | Contains the access restriction configurations to be updated. |

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
