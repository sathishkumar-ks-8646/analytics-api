# OrgAPI

```javascript
var org       = ac.getOrgInstance(orgId);
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
var view      = ac.getViewInstance(orgId, workspaceId, viewId);
var bulk      = ac.getBulkInstance(orgId, workspaceId);
```

`OrgAPI` exposes **19 methods**. Method names are `camelCase` and identifiers are `string`.

## Methods

[`activateUsers`](#activateusers), [`addUsers`](#addusers), [`changeUserRole`](#changeuserrole), [`createCustomRole`](#createcustomrole), [`createWorkspace`](#createworkspace), [`deActivateUsers`](#deactivateusers), [`deleteCustomRole`](#deletecustomrole), [`getAdmins`](#getadmins), [`getAutomlAnalysis`](#getautomlanalysis), [`getCustomRoles`](#getcustomroles), [`getLinkedWorkspaces`](#getlinkedworkspaces), [`getMetaDetails`](#getmetadetails), [`getOrgAccessRestrictions`](#getorgaccessrestrictions), [`getResourceDetails`](#getresourcedetails), [`getSubscriptionDetails`](#getsubscriptiondetails), [`getUsers`](#getusers), [`removeUsers`](#removeusers), [`updateCustomRole`](#updatecustomrole), [`updateOrgAccessRestrictions`](#updateorgaccessrestrictions)

### activateUsers

```javascript
activateUsers(emailIds, config={})
```

Activate users in the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `emailIds` | `JSONArray` | The email address of the users to be activated. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### addUsers

```javascript
addUsers(emailIds, config={})
```

Add users to the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `emailIds` | `JSONArray` | The email address of the users to be added. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### changeUserRole

```javascript
changeUserRole(emailIds, role, config={})
```

Change role for the specified users.

| Parameter | Type | Description |
|---|---|---|
| `emailIds` | `JSONArray` | The email address of the users. |
| `role` | `String` | New role for the users. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### createCustomRole

```javascript
createCustomRole(roleName, accessType, permissions, config={})
```

Create a new custom role in the organization.

| Parameter | Type | Description |
|---|---|---|
| `roleName` | `String` | Name of the custom role to be created. |
| `accessType` | `String` | Access type for the custom role. |
| `permissions` | `Object` | Permissions configuration for the custom role. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Created custom role id.

**Raises** — `Error`

### createWorkspace

```javascript
createWorkspace(workspaceName, config={})
```

Create a blank workspace in the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `workspaceName` | `String` | Name of the workspace. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Created workspace id.

**Raises** — `Error`

### deActivateUsers

```javascript
deActivateUsers(emailIds, config={})
```

Deactivate users in the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `emailIds` | `JSONArray` | The email address of the users to be deactivated. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### deleteCustomRole

```javascript
deleteCustomRole(roleId)
```

Delete the specified custom role from the organization.

| Parameter | Type | Description |
|---|---|---|
| `roleId` | `String` | Id of the custom role to be deleted. |

**Raises** — `Error`

### getAdmins

```javascript
getAdmins(config={})
```

Returns list of admins for a specified organization.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Organization admin list.

**Raises** — `Error`

### getAutomlAnalysis

```javascript
getAutomlAnalysis()
```

Returns all the automl analysis available in an organization.

**Returns** — AutoML analysis list.

**Raises** — `Error`

### getCustomRoles

```javascript
getCustomRoles()
```

Returns list of all custom roles available in the organization.

**Returns** — Custom roles list.

**Raises** — `Error`

### getLinkedWorkspaces

```javascript
getLinkedWorkspaces()
```

Returns list of linked workspaces available in the specified organization.

**Returns** — Linked workspaces list.

**Raises** — `Error`

### getMetaDetails

```javascript
getMetaDetails(workspaceName, viewName=null, config={})
```

Returns details of the specified workspace/view.

| Parameter | Type | Description |
|---|---|---|
| `workspaceName` | `String` | Name of the workspace. |
| `viewName` | `String` | Name of the view. Can be null. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Workspace (or) View meta details.

**Raises** — `Error`

### getOrgAccessRestrictions

```javascript
getOrgAccessRestrictions()
```

Returns the access restriction settings configured for the organization.

**Returns** — Organization access restriction settings.

**Raises** — `Error`

### getResourceDetails

```javascript
getResourceDetails()
```

Returns resource usage details of the specified organization.

**Returns** — Resource details.

**Raises** — `Error`

### getSubscriptionDetails

```javascript
getSubscriptionDetails()
```

Returns subscription details of the specified organization.

**Returns** — Subscription details.

**Raises** — `Error`

### getUsers

```javascript
getUsers()
```

Returns list of users for the specified organization.

**Returns** — User list.

**Raises** — `Error`

### removeUsers

```javascript
removeUsers(emailIds, config={})
```

Remove users from the specified organization.

| Parameter | Type | Description |
|---|---|---|
| `emailIds` | `JSONArray` | The email address of the users to be removed. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### updateCustomRole

```javascript
updateCustomRole(roleId, roleName, accessType, permissions, config={})
```

Update the existing custom role in the organization.

| Parameter | Type | Description |
|---|---|---|
| `roleId` | `String` | Id of the custom role to be updated. |
| `roleName` | `String` | New name for the custom role. |
| `accessType` | `String` | New access type for the custom role. |
| `permissions` | `Object` | New permissions configuration for the custom role. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### updateOrgAccessRestrictions

```javascript
updateOrgAccessRestrictions(config={})
```

Update the access restriction settings of the organization.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains the access restriction configurations to be updated. |

**Raises** — `Error`

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
