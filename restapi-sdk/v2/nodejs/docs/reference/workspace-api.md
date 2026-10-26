# WorkspaceAPI

```javascript
var org       = ac.getOrgInstance(orgId);
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
var view      = ac.getViewInstance(orgId, workspaceId, viewId);
var bulk      = ac.getBulkInstance(orgId, workspaceId);
```

`WorkspaceAPI` exposes **116 methods**. Method names are `camelCase` and identifiers are `string`.

## Methods

[`addAdmins`](#addadmins), [`addDefault`](#adddefault), [`addFavorite`](#addfavorite), [`addGroupMembers`](#addgroupmembers), [`addTagToViews`](#addtagtoviews), [`addWorkspaceUsers`](#addworkspaceusers), [`automlAnalysisPrediction`](#automlanalysisprediction), [`backupWorkspaceNow`](#backupworkspacenow), [`changeAlertStatus`](#changealertstatus), [`changeEmailScheduleStatus`](#changeemailschedulestatus), [`changeFolderHierarchy`](#changefolderhierarchy), [`changeFolderPosition`](#changefolderposition), [`changeWorkspaceUserRole`](#changeworkspaceuserrole), [`changeWorkspaceUserStatus`](#changeworkspaceuserstatus), [`copy`](#copy), [`copyViews`](#copyviews), [`createAutomlAnalysis`](#createautomlanalysis), [`createAutomlAnalysisDeployment`](#createautomlanalysisdeployment), [`createDashboard`](#createdashboard), [`createEmailSchedule`](#createemailschedule), [`createFolder`](#createfolder), [`createGroup`](#creategroup), [`createQueryTable`](#createquerytable), [`createReport`](#createreport), [`createSlideshow`](#createslideshow), [`createTable`](#createtable), [`createTag`](#createtag), [`createVariable`](#createvariable), [`delete`](#delete), [`deleteAlerts`](#deletealerts), [`deleteAutomlAnalysis`](#deleteautomlanalysis), [`deleteAutomlAnalysisDeployment`](#deleteautomlanalysisdeployment), [`deleteAutomlAnalysisModel`](#deleteautomlanalysismodel), [`deleteEmailSchedule`](#deleteemailschedule), [`deleteFolder`](#deletefolder), [`deleteGroup`](#deletegroup), [`deleteSlideshow`](#deleteslideshow), [`deleteTag`](#deletetag), [`deleteTrashView`](#deletetrashview), [`deleteVariable`](#deletevariable), [`deployAutomlAnalysis`](#deployautomlanalysis), [`disableDomainAccess`](#disabledomainaccess), [`downloadWorkspaceBackup`](#downloadworkspacebackup), [`editQueryTable`](#editquerytable), [`enableDomainAccess`](#enabledomainaccess), [`exportAsTemplate`](#exportastemplate), [`getAdmins`](#getadmins), [`getAggregateFormulaDependents`](#getaggregateformuladependents), [`getAggregateFormulas`](#getaggregateformulas), [`getAggregateFormulaValue`](#getaggregateformulavalue), [`getAlertConfiguration`](#getalertconfiguration), [`getAlertEvents`](#getalertevents), [`getAlertsInWorkspace`](#getalertsinworkspace), [`getAutomlAnalysis`](#getautomlanalysis), [`getAutomlAnalysisDetails`](#getautomlanalysisdetails), [`getDashboardMetadata`](#getdashboardmetadata), [`getDatasources`](#getdatasources), [`getDeploymentDetails`](#getdeploymentdetails), [`getEmailSchedules`](#getemailschedules), [`getFolders`](#getfolders), [`getGroupDetails`](#getgroupdetails), [`getGroups`](#getgroups), [`getLinkableWorkspaces`](#getlinkableworkspaces), [`getLinkedWorkspaces`](#getlinkedworkspaces), [`getLinkedWorkspaceSyncDetails`](#getlinkedworkspacesyncdetails), [`getQueryTableDetails`](#getquerytabledetails), [`getQueryTables`](#getquerytables), [`getReportMetadata`](#getreportmetadata), [`getSecretKey`](#getsecretkey), [`getSharedDetailsForViews`](#getshareddetailsforviews), [`getShareInfo`](#getshareinfo), [`getSlideshowDetails`](#getslideshowdetails), [`getSlideshows`](#getslideshows), [`getSlideshowUrl`](#getslideshowurl), [`getTaggedViews`](#gettaggedviews), [`getTags`](#gettags), [`getTrashViews`](#gettrashviews), [`getVariableDetails`](#getvariabledetails), [`getVariables`](#getvariables), [`getViews`](#getviews), [`getWorkspaceAccessRestrictions`](#getworkspaceaccessrestrictions), [`getWorkspaceBackups`](#getworkspacebackups), [`getWorkspaceBackupStatus`](#getworkspacebackupstatus), [`getWorkspaceLinkingCompatibility`](#getworkspacelinkingcompatibility), [`getWorkspaceRestoreStatus`](#getworkspacerestorestatus), [`getWorkspaceUsers`](#getworkspaceusers), [`linkWorkspaces`](#linkworkspaces), [`makeDefaultFolder`](#makedefaultfolder), [`moveViewsToFolder`](#moveviewstofolder), [`removeAdmins`](#removeadmins), [`removeDefault`](#removedefault), [`removeFavorite`](#removefavorite), [`removeGroupMembers`](#removegroupmembers), [`removeShare`](#removeshare), [`removeTagFromViews`](#removetagfromviews), [`removeWorkspaceUsers`](#removeworkspaceusers), [`rename`](#rename), [`renameFolder`](#renamefolder), [`renameGroup`](#renamegroup), [`restoreTrashView`](#restoretrashview), [`restoreWorkspaceFromBackup`](#restoreworkspacefrombackup), [`runAlert`](#runalert), [`shareViews`](#shareviews), [`syncData`](#syncdata), [`syncLinkedWorkspaces`](#synclinkedworkspaces), [`triggerEmailSchedule`](#triggeremailschedule), [`unlinkWorkspaces`](#unlinkworkspaces), [`updateAlert`](#updatealert), [`updateDashboard`](#updatedashboard), [`updateDatasourceConnection`](#updatedatasourceconnection), [`updateEmailSchedule`](#updateemailschedule), [`updateReport`](#updatereport), [`updateSlideshow`](#updateslideshow), [`updateTag`](#updatetag), [`updateVariable`](#updatevariable), [`updateWorkspaceAccessRestrictions`](#updateworkspaceaccessrestrictions)

### addAdmins

```javascript
addAdmins(emailIds, config={})
```

Add admins for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `emailIds` | `JSONArray` | The email address of the admin users to be added. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### addDefault

```javascript
addDefault(config={})
```

Adds a specified workspace as default.

**Raises** — `Error`

### addFavorite

```javascript
addFavorite(config={})
```

Adds a specified workspace as favorite.

**Raises** — `Error`

### addGroupMembers

```javascript
addGroupMembers(groupId, emailIds, config={})
```

Add users to the specified group.

| Parameter | Type | Description |
|---|---|---|
| `groupId` | `String` | Id of the group. |
| `emailIds` | `JSONArray` | The email address of the users to be added to the group. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### addTagToViews

```javascript
addTagToViews(tagId, viewIds, config={})
```

Adds the specified tag to multiple views in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `tagId` | `String` | Id of the tag. |
| `viewIds` | `JSONArray` | View ids to be associated with the tag. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### addWorkspaceUsers

```javascript
addWorkspaceUsers(emailIds, role, config={})
```

Add users to the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `emailIds` | `JSONArray` | The email address of the users to be added. |
| `role` | `String` | Role for the users to be added. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### automlAnalysisPrediction

```javascript
automlAnalysisPrediction(analysisId, modelId, features, config = {})
```

Get predictions by providing sample input values for a trained model.

| Parameter | Type | Description |
|---|---|---|
| `analysisId` | `String` | Id of the Automl Analysis. |
| `modelId` | `String` | Id of the Automl Analysis model. |
| `features` | `Object` | Column → value map for prediction. |
| `config` | `Object` | Additional control attributes. |

**Returns** — Prediction result.

**Raises** — `Error`

### backupWorkspaceNow

```javascript
backupWorkspaceNow(config={})
```

Trigger an instant backup for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Triggered backup details.

**Raises** — `Error`

### changeAlertStatus

```javascript
changeAlertStatus(alertIds, enabled, config={})
```

Enable or disable the specified data alerts in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `alertIds` | `JSONArray` | Ids of the data alerts. |
| `enabled` | `Boolean` | Pass true to enable the data alerts and false to disable them. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### changeEmailScheduleStatus

```javascript
changeEmailScheduleStatus(scheduleId, operation)
```

Update email schedule status.

| Parameter | Type | Description |
|---|---|---|
| `scheduleId` | `String` | Id for the email schedule. |
| `operation` | `String` | New status for the schedule ( Values - activate | deactivate ) |

**Raises** — `Error`

### changeFolderHierarchy

```javascript
changeFolderHierarchy(folderId, hierarchy, config={})
```

Swaps the hierarchy of a parent folder and a subfolder.

| Parameter | Type | Description |
|---|---|---|
| `folderId` | `String` | Id of the folder. |
| `hierarchy` | `Number` | New hierarchy for the folder. (0 - Parent; 1 - Child). |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### changeFolderPosition

```javascript
changeFolderPosition(folderId, referenceFolderId, config={})
```

Place the folder above the reference folder.

| Parameter | Type | Description |
|---|---|---|
| `folderId` | `String` | Id of the folder. |
| `referenceFolderId` | `String` | Id of the reference folder. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### changeWorkspaceUserRole

```javascript
changeWorkspaceUserRole(emailIds, role, config={})
```

Change role for the specified users.

| Parameter | Type | Description |
|---|---|---|
| `emailIds` | `JSONArray` | The email address of the users. |
| `role` | `String` | New role for the users. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### changeWorkspaceUserStatus

```javascript
changeWorkspaceUserStatus(emailIds, operation, config={})
```

Change users staus in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `emailIds` | `JSONArray` | The email address of the users. |
| `operation` | `String` | New status for the users ( Values - activate | deactivate ) |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### copy

```javascript
copy(workspaceName, config={}, destOrgId=null)
```

Copy the specified workspace from one organization to another or within the organization.

| Parameter | Type | Description |
|---|---|---|
| `workspaceName` | `String` | Name of the new workspace. |
| `config` | `Object` | Contains any additional control attributes. |
| `destOrgId` | `String` | ull - Id of the organization where the destination workspace is present. |

**Returns** — Copied workspace id.

**Raises** — `Error`

### copyViews

```javascript
copyViews(viewIds, destWorkspaceId, config={}, destOrgId=null)
```

Copy the specified views from one workspace to another workspace.

| Parameter | Type | Description |
|---|---|---|
| `viewIds` | `JSONArray` | The id of the views to be copied. |
| `destWorkspaceId` | `String` | The destination workspace id. |
| `config` | `Object` | Contains any additional control attributes. |
| `destOrgId` | `String` | ull - Id of the organization where the destination workspace is present. |

**Returns** — View list.

**Raises** — `Error`

### createAutomlAnalysis

```javascript
createAutomlAnalysis(name, trainingTableId, predictionType, features, serverOption, algorithms, config = {})
```

Create a new AutoML analysis within the provided workspace.

| Parameter | Type | Description |
|---|---|---|
| `name` | `String` | Name for the automl analysis to be created. |
| `trainingTableId` | `String` | Id of the training table. |
| `predictionType` | `String` | REGRESSION / CLASSIFICATION / CLUSTERING. |
| `features` | `Array` | List of column names used as features. |
| `serverOption` | `Number` | 1 → 8GB, 2 → 16GB, 3 → 32GB. |
| `algorithms` | `Object` | Algorithms configuration. |
| `config` | `Object` | Additional control attributes. |

**Returns** — Created AutoML Analysis Id.

**Raises** — `Error`

### createAutomlAnalysisDeployment

```javascript
createAutomlAnalysisDeployment(analysisId, modelId, inputTableId, outputTable, outputColumns, predictionColumn, serverOption, importType, scheduleDetails, config = {})
```

Deploy the AutoML analysis model.

**Returns** — Created AutoML Deployment details.

**Raises** — `Error`

### createDashboard

```javascript
createDashboard(displayName, layout, config={})
```

Create a dashboard in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `displayName` | `String` | Name of the dashboard. |
| `layout` | `String` | Layout configuration of the dashboard. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Created dashboard id.

**Raises** — `Error`

### createEmailSchedule

```javascript
createEmailSchedule(scheduleName, viewIds, format, emailIds, scheduleDetails, config={})
```

Create an email schedule in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `scheduleName` | `String` | Name of the email schedule. |
| `viewIds` | `JSONArray` | View ids to be mailed. |
| `format` | `String` | The format in which the data has to be mailed. |
| `emailIds` | `JSONArray` | The recipients' email addresses for sending views. |
| `scheduleDetails` | `Object` | Contains schedule frequency, date, and time info. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Created email schedule id.

**Raises** — `Error`

### createFolder

```javascript
createFolder(folderName, config={})
```

Create a folder in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `folderName` | `String` | Name of the folder to be created. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Created folder id.

**Raises** — `Error`

### createGroup

```javascript
createGroup(groupName, emailIds, config={})
```

Create a group in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `groupName` | `String` | Name of the group. |
| `emailIds` | `JSONArray` | The email address of the users to be added to the group. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Created group id.

**Raises** — `Error`

### createQueryTable

```javascript
createQueryTable(sqlQuery, queryTableName, config={})
```

Create a new query table in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `sqlQuery` | `String` | SQL query to construct the query table. |
| `queryTableName` | `String` | Name of the query table to be created. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Id of the created query table.

**Raises** — `Error`

### createReport

```javascript
createReport(config={})
```

Create a report in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains the control attributes. |

**Returns** — Id of the created view.

**Raises** — `Error`

### createSlideshow

```javascript
createSlideshow(slideName, viewIds, config={})
```

Create a slideshow in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `slideName` | `String` | Name of the slideshow to be created. |
| `viewIds` | `JSONArray` | Ids of the view to be included in the slideshow. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Id of the created slideshow.

**Raises** — `Error`

### createTable

```javascript
createTable(tableDesign, config={})
```

Create a table in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `tableDesign` | `Object` | Table structure. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — created table id.

**Raises** — `Error`

### createTag

```javascript
createTag(tagName, colorCode, config={})
```

Create a tag in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `tagName` | `String` | Name of the tag to be created. |
| `colorCode` | `String` | Color of the tag in HEX color code. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Created tag id.

**Raises** — `Error`

### createVariable

```javascript
createVariable(variableName, variableDataType, variableType, config={})
```

Create a variable in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `variableName` | `String` | Name of the variable to be created. |
| `variableName` | `Number` | Datatype of the variable to be created. |
| `variableName` | `Number` | Type of the variable to be created. |
| `config` | `Object` | Contains the control attributes. |

**Returns** — Id of the created variable.

**Raises** — `Error`

### delete

```javascript
delete(config={})
```

Delete a specified workspace in the organization.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### deleteAlerts

```javascript
deleteAlerts(alertIds, config={})
```

Delete the specified data alerts from the workspace.

| Parameter | Type | Description |
|---|---|---|
| `alertIds` | `JSONArray` | Ids of the data alerts to be deleted. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### deleteAutomlAnalysis

```javascript
deleteAutomlAnalysis(analysisId, config = {})
```

Delete a specified automl analysis from the given workspace.

| Parameter | Type | Description |
|---|---|---|
| `analysisId` | `String` | Id of the Automl Analysis to be deleted. |
| `config` | `Object` | Additional control attributes. |

**Raises** — `Error`

### deleteAutomlAnalysisDeployment

```javascript
deleteAutomlAnalysisDeployment(analysisId, deploymentId, config = {})
```

Delete the AutoML analysis deployment.

| Parameter | Type | Description |
|---|---|---|
| `analysisId` | `String` | Id of the Automl Analysis. |
| `deploymentId` | `String` | Id of the deployment to be deleted. |
| `config` | `Object` | Additional control attributes. |

**Raises** — `Error`

### deleteAutomlAnalysisModel

```javascript
deleteAutomlAnalysisModel(analysisId, modelId, config = {})
```

Delete a specified model available in the given automl analysis.

| Parameter | Type | Description |
|---|---|---|
| `analysisId` | `String` | Id of the Automl Analysis. |
| `modelId` | `String` | Id of the model to be deleted. |
| `config` | `Object` | Additional control attributes. |

**Raises** — `Error`

### deleteEmailSchedule

```javascript
deleteEmailSchedule(scheduleId)
```

Delete the specified email schedule in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `scheduleId` | `String` | Id for the email schedule. |

**Raises** — `Error`

### deleteFolder

```javascript
deleteFolder(folderId)
```

Delete a specified folder in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `folderId` | `String` | Id of the folder to be deleted. |

**Raises** — `Error`

### deleteGroup

```javascript
deleteGroup(groupId)
```

Delete a specified group.

| Parameter | Type | Description |
|---|---|---|
| `groupId` | `String` | The id of the group. |

**Raises** — `Error`

### deleteSlideshow

```javascript
deleteSlideshow(slideId)
```

Delete a specified slideshow in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `slideId` | `String` | Id of the slideshow. |

**Raises** — `Error`

### deleteTag

```javascript
deleteTag(tagId)
```

Delete the specified tag from the workspace.

| Parameter | Type | Description |
|---|---|---|
| `tagId` | `String` | Id of the tag. |

**Raises** — `Error`

### deleteTrashView

```javascript
deleteTrashView(viewId, config={})
```

Delete the specified view permanently from trash.

| Parameter | Type | Description |
|---|---|---|
| `viewId` | `String` | Id of the view. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### deleteVariable

```javascript
deleteVariable(variableId)
```

Delete a specified variable in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `variableId` | `String` | Id of the variable. |

**Raises** — `Error`

### deployAutomlAnalysis

```javascript
deployAutomlAnalysis(analysisId, deploymentId, config = {})
```

Execute the AutoML analysis deployment.

| Parameter | Type | Description |
|---|---|---|
| `analysisId` | `String` | Id of the Automl Analysis. |
| `deploymentId` | `String` | Id of the deployment to be executed. |
| `config` | `Object` | Additional control attributes. |

**Raises** — `Error`

### disableDomainAccess

```javascript
disableDomainAccess()
```

Disable workspace from the specified white label domain.

**Raises** — `Error`

### downloadWorkspaceBackup

```javascript
downloadWorkspaceBackup(backupId, filePath, config={})
```

Download the specified workspace backup.

| Parameter | Type | Description |
|---|---|---|
| `backupId` | `String` | Id of the backup. |
| `filePath` | `String` | Path of the file where the downloaded backup is to be stored. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### editQueryTable

```javascript
editQueryTable(viewId, sqlQuery, config={})
```

Update the mentioned query table in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `viewId` | `String` | Id of the query table to be updated. |
| `sqlQuery` | `String` | New SQL query to be updated. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### enableDomainAccess

```javascript
enableDomainAccess()
```

Enable workspace to the specified white label domain.

**Raises** — `Error`

### exportAsTemplate

```javascript
exportAsTemplate(viewIds, filePath, config={})
```

Export the mentioned views as templates.

| Parameter | Type | Description |
|---|---|---|
| `viewIds` | `JSONArray` | Ids of the view to be exported. |
| `filePath` | `String` | Path of the file where the data exported to be stored. ( Should be in 'atpt' format ) |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### getAdmins

```javascript
getAdmins(config={})
```

Returns list of admins for the specified workspace.

**Returns** — Workspace admin list.

**Raises** — `Error`

### getAggregateFormulaDependents

```javascript
getAggregateFormulaDependents(formulaId)
```

Returns list of all dependent views and formulas for the specified aggregate formula.

| Parameter | Type | Description |
|---|---|---|
| `formulaId` | `String` | Id of the aggregate formula. |

**Returns** — Dependent details.

**Raises** — `Error`

### getAggregateFormulas

```javascript
getAggregateFormulas(config={})
```

Returns list of all aggregate formulas for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Aggregate formula list.

**Raises** — `Error`

### getAggregateFormulaValue

```javascript
getAggregateFormulaValue(formulaId)
```

Returns the value of the aggregate formula.

| Parameter | Type | Description |
|---|---|---|
| `formulaId` | `String` | Id of the aggregate formula. |

**Returns** — Aggregate formula value.

**Raises** — `Error`

### getAlertConfiguration

```javascript
getAlertConfiguration(alertId)
```

Returns the configuration of the specified data alert.

| Parameter | Type | Description |
|---|---|---|
| `alertId` | `String` | Id of the data alert. |

**Returns** — Data alert configuration.

**Raises** — `Error`

### getAlertEvents

```javascript
getAlertEvents(alertId, config={})
```

Returns the execution events of the specified data alert.

| Parameter | Type | Description |
|---|---|---|
| `alertId` | `String` | Id of the data alert. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Data alert events along with the page details.

**Raises** — `Error`

### getAlertsInWorkspace

```javascript
getAlertsInWorkspace()
```

Returns list of data alerts available in the specified workspace.

**Returns** — Data alerts list.

**Raises** — `Error`

### getAutomlAnalysis

```javascript
getAutomlAnalysis()
```

Returns list of automl analysis for the specified workspace.

**Returns** — AutoML analysis list.

**Raises** — `Error`

### getAutomlAnalysisDetails

```javascript
getAutomlAnalysisDetails(analysisId)
```

Retrieve detailed information for a specific AutoML analysis.

| Parameter | Type | Description |
|---|---|---|
| `analysisId` | `String` | Id of the Automl Analysis. |

**Returns** — AutoML analysis details.

**Raises** — `Error`

### getDashboardMetadata

```javascript
getDashboardMetadata(dashboardId, config={})
```

Returns the metadata of the specified dashboard.

| Parameter | Type | Description |
|---|---|---|
| `dashboardId` | `String` | Id of the dashboard. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Dashboard configuration.

**Raises** — `Error`

### getDatasources

```javascript
getDatasources()
```

Returns list of datasources for the specified workspace.

**Returns** — Datasource list.

**Raises** — `Error`

### getDeploymentDetails

```javascript
getDeploymentDetails(analysisId, modelId)
```

Returns deployment details available for a AutoML analysis model.

| Parameter | Type | Description |
|---|---|---|
| `analysisId` | `String` | Id of the Automl Analysis. |
| `modelId` | `String` | Id of the Automl Analysis Model. |

**Returns** — AutoML analysis deployment details.

**Raises** — `Error`

### getEmailSchedules

```javascript
getEmailSchedules()
```

Returns list of email schedules available in the specified workspace.

**Returns** — List of email schedules.

**Raises** — `Error`

### getFolders

```javascript
getFolders()
```

Returns list of all accessible folders for the specified workspace.

**Returns** — Folder list.

**Raises** — `Error`

### getGroupDetails

```javascript
getGroupDetails(groupId)
```

Get the details of the specified group.

| Parameter | Type | Description |
|---|---|---|
| `groupId` | `String` | Id of the group. |

**Returns** — Details of the specified group.

**Raises** — `Error`

### getGroups

```javascript
getGroups()
```

Returns list of groups for the specified workspace.

**Returns** — Group list.

**Raises** — `Error`

### getLinkableWorkspaces

```javascript
getLinkableWorkspaces()
```

Returns list of organizations and workspaces that can be linked to the specified master workspace.

**Returns** — Organizations with their linkable workspaces.

**Raises** — `Error`

### getLinkedWorkspaces

```javascript
getLinkedWorkspaces()
```

Returns list of workspaces linked to the specified master workspace.

**Returns** — Linked workspaces list.

**Raises** — `Error`

### getLinkedWorkspaceSyncDetails

```javascript
getLinkedWorkspaceSyncDetails(sandboxIds, config={})
```

Returns the sync details of the specified linked workspaces.

| Parameter | Type | Description |
|---|---|---|
| `sandboxIds` | `JSONArray` | Ids of the linked workspaces for which the sync details are fetched. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Linked workspace sync details.

**Raises** — `Error`

### getQueryTableDetails

```javascript
getQueryTableDetails(queryTableId)
```

Returns details of the specified query table.

| Parameter | Type | Description |
|---|---|---|
| `queryTableId` | `String` | Id of the query table. |

**Returns** — View details.

**Raises** — `Error`

### getQueryTables

```javascript
getQueryTables(config={})
```

Returns list of all query tables for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Query table list.

**Raises** — `Error`

### getReportMetadata

```javascript
getReportMetadata(viewId)
```

Returns the metadata of the specified report.

| Parameter | Type | Description |
|---|---|---|
| `viewId` | `String` | Id of the report. |

**Returns** — Report configuration.

**Raises** — `Error`

### getSecretKey

```javascript
getSecretKey(config={})
```

Returns the secret key of the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Workspace secret key.

**Raises** — `Error`

### getSharedDetailsForViews

```javascript
getSharedDetailsForViews(viewIds)
```

Returns shared details of the specified views.

| Parameter | Type | Description |
|---|---|---|
| `viewIds` | `JSONArray` | The id of the views to be copied. |

**Returns** — Folder list.

**Raises** — `Error`

### getShareInfo

```javascript
getShareInfo()
```

Returns shared details of the specified workspace.

**Returns** — Workspace share info.

**Raises** — `Error`

### getSlideshowDetails

```javascript
getSlideshowDetails(slideId)
```

Returns details of the specified slideshow.

| Parameter | Type | Description |
|---|---|---|
| `slideId` | `String` | Id of the slideshow. |

**Returns** — Slideshow details.

**Raises** — `Error`

### getSlideshows

```javascript
getSlideshows()
```

Returns list of slideshows for the specified workspace.

**Returns** — Slideshow list.

**Raises** — `Error`

### getSlideshowUrl

```javascript
getSlideshowUrl(slideId, config={})
```

Returns slide URL to access the specified slideshow.

| Parameter | Type | Description |
|---|---|---|
| `slideId` | `String` | Id of the slideshow. |
| `config` | `Object` | Contains the control configurations |

**Returns** — Slideshow URL.

**Raises** — `Error`

### getTaggedViews

```javascript
getTaggedViews(tagId)
```

Returns list of views associated with the specified tag.

| Parameter | Type | Description |
|---|---|---|
| `tagId` | `String` | Id of the tag. |

**Returns** — Tagged views list.

**Raises** — `Error`

### getTags

```javascript
getTags()
```

Returns list of all tags for the specified workspace.

**Returns** — Tags list.

**Raises** — `Error`

### getTrashViews

```javascript
getTrashViews()
```

Returns list of all views available in trash for the specified workspace.

**Returns** — Trash view list.

**Raises** — `Error`

### getVariableDetails

```javascript
getVariableDetails(variableId)
```

Returns details of the specified variable.

| Parameter | Type | Description |
|---|---|---|
| `variableId` | `String` | Id of the variable. |

**Returns** — Variable details.

**Raises** — `Error`

### getVariables

```javascript
getVariables()
```

Returns list of variables for the specified workspace.

**Returns** — Variable list.

**Raises** — `Error`

### getViews

```javascript
getViews(config={})
```

Returns list of all accessible views for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — View list.

**Raises** — `Error`

### getWorkspaceAccessRestrictions

```javascript
getWorkspaceAccessRestrictions()
```

Returns the access restriction settings configured for the specified workspace.

**Returns** — Workspace access restriction settings.

**Raises** — `Error`

### getWorkspaceBackups

```javascript
getWorkspaceBackups()
```

Returns the backup configuration and the list of backups available for the specified workspace.

**Returns** — Workspace backup details.

**Raises** — `Error`

### getWorkspaceBackupStatus

```javascript
getWorkspaceBackupStatus(backupId)
```

Returns the status of the specified workspace backup.

| Parameter | Type | Description |
|---|---|---|
| `backupId` | `String` | Id of the backup. |

**Returns** — Backup status details.

**Raises** — `Error`

### getWorkspaceLinkingCompatibility

```javascript
getWorkspaceLinkingCompatibility(clients, config={})
```

Returns the linking compatibility details for the specified client workspaces.

| Parameter | Type | Description |
|---|---|---|
| `clients` | `JSONArray` | Contains the client workspaces to be verified for linking compatibility. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Client workspace compatibility details.

**Raises** — `Error`

### getWorkspaceRestoreStatus

```javascript
getWorkspaceRestoreStatus(restoreId)
```

Returns the status of the specified workspace restore.

| Parameter | Type | Description |
|---|---|---|
| `restoreId` | `String` | Id of the restore. |

**Returns** — Restore status details.

**Raises** — `Error`

### getWorkspaceUsers

```javascript
getWorkspaceUsers()
```

Returns list of users for the specified workspace.

**Returns** — User list.

**Raises** — `Error`

### linkWorkspaces

```javascript
linkWorkspaces(clients, config={})
```

Link the specified client workspaces to the master workspace.

| Parameter | Type | Description |
|---|---|---|
| `clients` | `JSONArray` | Contains the client workspaces to be linked with the master workspace. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### makeDefaultFolder

```javascript
makeDefaultFolder(folderId)
```

Make the specified folder as default.

| Parameter | Type | Description |
|---|---|---|
| `folderId` | `String` | Id of the folder. |

**Raises** — `Error`

### moveViewsToFolder

```javascript
moveViewsToFolder(folderId, viewIds, config={})
```

Move views to the mentioned folder.

| Parameter | Type | Description |
|---|---|---|
| `folderId` | `String` | Id of the folder. |
| `viewIds` | `JSONArray` | View ids to be moved. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### removeAdmins

```javascript
removeAdmins(emailIds, config={})
```

Remove admins from the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `emailIds` | `JSONArray` | The email address of the admin users to be removed. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### removeDefault

```javascript
removeDefault(config={})
```

Remove a specified workspace from default.

**Raises** — `Error`

### removeFavorite

```javascript
removeFavorite(config={})
```

Remove a specified workspace from favorite.

**Raises** — `Error`

### removeGroupMembers

```javascript
removeGroupMembers(groupId, emailIds, config={})
```

Remove users from the specified group.

| Parameter | Type | Description |
|---|---|---|
| `groupId` | `String` | Id of the group. |
| `emailIds` | `JSONArray` | The email address of the users to be removed from the group. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### removeShare

```javascript
removeShare(viewIds, emailIds, config={})
```

Remove shared views for the specified users.

| Parameter | Type | Description |
|---|---|---|
| `viewIds` | `JSONArray` | View ids whose sharing needs to be removed. |
| `emailIds` | `JSONArray` | The email address of the users to whom the sharing need to be removed. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### removeTagFromViews

```javascript
removeTagFromViews(tagId, viewIds=null, dissociateAll=false, config={})
```

Removes the specified tag from multiple views in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `tagId` | `String` | Id of the tag. |
| `viewIds` | `JSONArray` | View ids to be dissociated. Not required when dissociateAll is true. |
| `dissociateAll` | `Boolean` | To dissociate the tag from all associated views. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### removeWorkspaceUsers

```javascript
removeWorkspaceUsers(emailIds, config={})
```

Remove users from the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `emailIds` | `JSONArray` | The email address of the users to be removed. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### rename

```javascript
rename(workspaceName, config={})
```

Rename a specified workspace in the organization.

| Parameter | Type | Description |
|---|---|---|
| `workspaceName` | `String` | New name for the workspace. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### renameFolder

```javascript
renameFolder(folderId, newFolderName, config={})
```

Rename a specified folder in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `folderId` | `String` | Id of the folder. |
| `folderName` | `String` | New name for the folder. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### renameGroup

```javascript
renameGroup(groupId, newGroupName, config={})
```

Rename a specified group.

| Parameter | Type | Description |
|---|---|---|
| `groupId` | `String` | Id of the group. |
| `newGroupName` | `String` | New name for the group. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### restoreTrashView

```javascript
restoreTrashView(viewId, config={})
```

Restore the specified view from trash.

| Parameter | Type | Description |
|---|---|---|
| `viewId` | `String` | Id of the view. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### restoreWorkspaceFromBackup

```javascript
restoreWorkspaceFromBackup(backupId, confirmRestore, config={})
```

Restore the specified workspace from the given backup.

| Parameter | Type | Description |
|---|---|---|
| `backupId` | `String` | Id of the backup. |
| `confirmRestore` | `Boolean` | Pass true to confirm that the existing workspace data can be overwritten. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Triggered restore details.

**Raises** — `Error`

### runAlert

```javascript
runAlert(alertId, config={})
```

Execute the specified data alert immediately.

| Parameter | Type | Description |
|---|---|---|
| `alertId` | `String` | Id of the data alert. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### shareViews

```javascript
shareViews(viewIds, emailIds, permissions, config={})
```

Share views to the specified users.

| Parameter | Type | Description |
|---|---|---|
| `viewIds` | `JSONArray` | View ids to be shared. |
| `emailIds` | `JSONArray` | The email address of the users to whom the views need to be shared. |
| `permissions` | `Object` | Contains permission details. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### syncData

```javascript
syncData(datasourceId, config={})
```

Initiate data sync for the specified datasource.

| Parameter | Type | Description |
|---|---|---|
| `datasourceId` | `String` | Id of the datasource. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### syncLinkedWorkspaces

```javascript
syncLinkedWorkspaces(scope, config={})
```

Sync the metadata of the master workspace to its linked client workspaces.

| Parameter | Type | Description |
|---|---|---|
| `scope` | `String` | Scope of the sync operation. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### triggerEmailSchedule

```javascript
triggerEmailSchedule(scheduleId)
```

Trigger configured email schedules instantly.

| Parameter | Type | Description |
|---|---|---|
| `scheduleId` | `String` | Id for the email schedule. |

**Raises** — `Error`

### unlinkWorkspaces

```javascript
unlinkWorkspaces(scope, config={})
```

Unlink the client workspaces from the specified master workspace.

| Parameter | Type | Description |
|---|---|---|
| `scope` | `String` | Scope of the unlink operation. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### updateAlert

```javascript
updateAlert(alertId, alertName, scheduleDetails, rules, config={})
```

Update the specified data alert in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `alertId` | `String` | Id of the data alert. |
| `alertName` | `String` | Name of the data alert. |
| `scheduleDetails` | `Object` | Contains the schedule configurations of the data alert. |
| `rules` | `JSONArray` | Contains the rules to be evaluated by the data alert. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### updateDashboard

```javascript
updateDashboard(dashboardId, config={})
```

Update the specified dashboard in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `dashboardId` | `String` | Id of the dashboard. |
| `config` | `Object` | Contains the dashboard configurations to be updated. |

**Raises** — `Error`

### updateDatasourceConnection

```javascript
updateDatasourceConnection(datasourceId, config={})
```

Update connection details for the specified datasource.

| Parameter | Type | Description |
|---|---|---|
| `datasourceId` | `String` | Id of the datasource. |
| `config` | `Object` | Contains the control attributes. |

**Raises** — `Error`

### updateEmailSchedule

```javascript
updateEmailSchedule(scheduleId, config)
```

Update configurations of the specified email schedule in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `scheduleId` | `String` | Id for the email schedule. |
| `config` | `Object` | Contains the control configurations. |

**Returns** — Updated email schedule id.

**Raises** — `Error`

### updateReport

```javascript
updateReport(viewId, config={})
```

Update the design and configuration of the specified report.

| Parameter | Type | Description |
|---|---|---|
| `viewId` | `String` | Id of the view. |
| `config` | `Object` | Contains the control attributes. |

**Raises** — `Error`

### updateSlideshow

```javascript
updateSlideshow(slideId, config={})
```

Update details of the specified slideshow.

| Parameter | Type | Description |
|---|---|---|
| `slideId` | `String` | The id of the slideshow. |
| `config` | `Object` | Contains the control configurations |

**Raises** — `Error`

### updateTag

```javascript
updateTag(tagId, config={})
```

Update details of the specified tag in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `tagId` | `String` | Id of the tag. |
| `config` | `Object` | Contains the control attributes. |

**Raises** — `Error`

### updateVariable

```javascript
updateVariable(variableId, variableName, variableDataType, variableType, config={})
```

Update details of the specified variable in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `variableId` | `String` | Id of the variable. |
| `variableName` | `String` | New name for the variable. |
| `variableName` | `Number` | New datatype for the variable. |
| `variableName` | `Number` | New type for the variable. |
| `config` | `Object` | Contains the control attributes. |

**Raises** — `Error`

### updateWorkspaceAccessRestrictions

```javascript
updateWorkspaceAccessRestrictions(config={})
```

Update the access restriction settings of the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains the access restriction configurations to be updated. |

**Raises** — `Error`

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
