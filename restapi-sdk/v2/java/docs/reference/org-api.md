# OrgAPI

```java
OrgAPI       org       = ac.getOrgInstance(orgId);
WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
ViewAPI      view      = ac.getViewInstance(orgId, workspaceId, viewId);
BulkAPI      bulk      = ac.getBulkInstance(orgId, workspaceId);
```

`OrgAPI` exposes **20 methods**. Method names are `camelCase`, matching the endpoint title and identifiers are `long`.

## Methods

[`activateUsers`](#activateusers), [`addUsers`](#addusers), [`changeUserRole`](#changeuserrole), [`createCustomRole`](#createcustomrole), [`createWorkspace`](#createworkspace), [`deactivateUsers`](#deactivateusers), [`deleteCustomRole`](#deletecustomrole), [`getAdmins`](#getadmins), [`getAutoMLAnalysis`](#getautomlanalysis), [`getCustomRoles`](#getcustomroles), [`getLinkedWorkspaces`](#getlinkedworkspaces), [`getMetaDetails`](#getmetadetails), [`getOrgAccessRestrictions`](#getorgaccessrestrictions), [`getOrgWorkspaces`](#getorgworkspaces), [`getResourceDetails`](#getresourcedetails), [`getSubscriptionDetails`](#getsubscriptiondetails), [`getUsers`](#getusers), [`removeUsers`](#removeusers), [`updateCustomRole`](#updatecustomrole), [`updateOrgAccessRestrictions`](#updateorgaccessrestrictions)

### activateUsers

```java
void activateUsers(JSONArray emailIds, JSONObject config)
```

Activate users in the specified organization.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the users to be activated. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### addUsers

```java
void addUsers(JSONArray emailIds, JSONObject config)
```

Add users to the specified organization.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the users to be added. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### changeUserRole

```java
void changeUserRole(JSONArray emailIds, String role, JSONObject config)
```

Change role for the specified users.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the users. |
| `role` | Name of the role to be updated. Can be one of "USER"/"VIEWER"/"ORGADMIN". |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### createCustomRole

```java
String createCustomRole(String roleName, String accessType, JSONObject permissions, JSONObject config)
```

Create a new custom role in the specified organization.

| Parameter | Description |
|---|---|
| `roleName` | Name of the custom role to be created. |
| `accessType` | Access type for the custom role. |
| `permissions` | Contains the permission details for the custom role. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`String`) — A `String` of the created custom role id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### createWorkspace

```java
long createWorkspace(String workspaceName, JSONObject config)
```

Create a blank workspace in the specified organization.

| Parameter | Description |
|---|---|
| `workspaceName` | Name of the workspace. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — A `long` of new workspace id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### deactivateUsers

```java
void deactivateUsers(JSONArray emailIds, JSONObject config)
```

Deactivate users in the specified organization.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the users to be deactivated. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### deleteCustomRole

```java
void deleteCustomRole(String roleId)
```

Delete the specified custom role from the organization.

| Parameter | Description |
|---|---|
| `roleId` | Id of the custom role. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getAdmins

```java
JSONArray getAdmins()
```

Returns list of admins for a specified organization.

**Returns** (`JSONArray`) — A `JSONArray` of organization admins.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getAutoMLAnalysis

```java
JSONArray getAutoMLAnalysis()
```

Returns all AutoML analysis available in the organization.

**Returns** (`JSONArray`) — AutoML analysis list.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getCustomRoles

```java
JSONArray getCustomRoles()
```

Returns list of custom roles for the specified organization.

**Returns** (`JSONArray`) — A `JSONArray` of custom roles.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getLinkedWorkspaces

```java
JSONArray getLinkedWorkspaces()
```

Returns list of linked workspaces available in the specified organization.

**Returns** (`JSONArray`) — A `JSONArray` of linked workspaces.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getMetaDetails

```java
JSONObject getMetaDetails(String workspaceName, String viewName)
```

Returns details of the specified workspace/view.

| Parameter | Description |
|---|---|
| `workspaceName` | The name of the workspace. |
| `viewName` | The name of the view. |

**Returns** (`JSONObject`) — A `JSONObject` of workspace/view details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getOrgAccessRestrictions

```java
JSONObject getOrgAccessRestrictions()
```

Returns the access restriction settings configured for the organization.

**Returns** (`JSONObject`) — A `JSONObject` of organization access restriction settings.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getOrgWorkspaces

```java
JSONArray getOrgWorkspaces()
```

Returns list of all accessible workspaces in the specified organization.

**Returns** (`JSONArray`) — A `JSONArray` of workspace list.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getResourceDetails

```java
JSONArray getResourceDetails()
```

Returns resource usage details of the specified organization.

**Returns** (`JSONArray`) — A `JSONArray` of resource details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getSubscriptionDetails

```java
JSONObject getSubscriptionDetails()
```

Returns subscription details of the specified organization.

**Returns** (`JSONObject`) — A `JSONObject` of subscription details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getUsers

```java
JSONArray getUsers()
```

Returns list of users for the specified organization.

**Returns** (`JSONArray`) — A `JSONArray` of users.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### removeUsers

```java
void removeUsers(JSONArray emailIds, JSONObject config)
```

Remove users from the specified organization.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the users to be removed. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### updateCustomRole

```java
void updateCustomRole(String roleId, String roleName, String accessType, JSONObject permissions, JSONObject config)
```

Update the specified custom role in the organization.

| Parameter | Description |
|---|---|
| `roleId` | Id of the custom role. |
| `roleName` | New name for the custom role. |
| `accessType` | Access type for the custom role. |
| `permissions` | Contains the permission details for the custom role. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### updateOrgAccessRestrictions

```java
void updateOrgAccessRestrictions(JSONObject config)
```

Update the access restriction settings of the organization.

| Parameter | Description |
|---|---|
| `config` | Contains the access restriction configurations to be updated. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
