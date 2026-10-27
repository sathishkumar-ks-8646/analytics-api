# WorkspaceAPI

```csharp
IOrgAPI       org       = ac.GetOrgInstance(orgId);
IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
IViewAPI      view      = ac.GetViewInstance(orgId, workspaceId, viewId);
IBulkAPI      bulk      = ac.GetBulkInstance(orgId, workspaceId);
```

`WorkspaceAPI` exposes **117 methods**. Method names are `PascalCase` and identifiers are `long`.

## Methods

[`AddAdmins`](#addadmins), [`AddDefault`](#adddefault), [`AddFavorite`](#addfavorite), [`AddGroupMembers`](#addgroupmembers), [`AddTagToViews`](#addtagtoviews), [`AddWorkspaceUsers`](#addworkspaceusers), [`AutomlAnalysisPrediction`](#automlanalysisprediction), [`BackupWorkspaceNow`](#backupworkspacenow), [`ChangeAlertStatus`](#changealertstatus), [`ChangeEmailScheduleStatus`](#changeemailschedulestatus), [`ChangeFolderHierarchy`](#changefolderhierarchy), [`ChangeFolderPosition`](#changefolderposition), [`ChangeWorkspaceUserRole`](#changeworkspaceuserrole), [`ChangeWorkspaceUserStatus`](#changeworkspaceuserstatus), [`Copy`](#copy), [`CopyViews`](#copyviews), [`CreateAutomlAnalysis`](#createautomlanalysis), [`CreateAutomlAnalysisDeployment`](#createautomlanalysisdeployment), [`CreateDashboard`](#createdashboard), [`CreateEmailSchedule`](#createemailschedule), [`CreateFolder`](#createfolder), [`CreateGroup`](#creategroup), [`CreateQueryTable`](#createquerytable), [`CreateReport`](#createreport), [`CreateSlideshow`](#createslideshow), [`CreateTable`](#createtable), [`CreateTag`](#createtag), [`CreateVariable`](#createvariable), [`Delete`](#delete), [`DeleteAlerts`](#deletealerts), [`DeleteAutomlAnalysis`](#deleteautomlanalysis), [`DeleteAutomlAnalysisDeployment`](#deleteautomlanalysisdeployment), [`DeleteAutomlAnalysisModel`](#deleteautomlanalysismodel), [`DeleteEmailSchedule`](#deleteemailschedule), [`DeleteFolder`](#deletefolder), [`DeleteGroup`](#deletegroup), [`DeleteSlideshow`](#deleteslideshow), [`DeleteTag`](#deletetag), [`DeleteTrashView`](#deletetrashview), [`DeleteVariable`](#deletevariable), [`DeployAutomlAnalysis`](#deployautomlanalysis), [`DisableDomainAccess`](#disabledomainaccess), [`DownloadWorkspaceBackup`](#downloadworkspacebackup), [`EditQueryTable`](#editquerytable), [`EnableDomainAccess`](#enabledomainaccess), [`ExportAsTemplate`](#exportastemplate), [`GetAdmins`](#getadmins), [`GetAggregateFormulaDependents`](#getaggregateformuladependents), [`GetAggregateFormulas`](#getaggregateformulas), [`GetAggregateFormulaValue`](#getaggregateformulavalue), [`GetAlertConfiguration`](#getalertconfiguration), [`GetAlertEvents`](#getalertevents), [`GetAlertsInWorkspace`](#getalertsinworkspace), [`GetAutomlAnalysis`](#getautomlanalysis), [`GetAutomlAnalysisDetails`](#getautomlanalysisdetails), [`GetDashboardMetadata`](#getdashboardmetadata), [`GetDatasources`](#getdatasources), [`GetDeploymentDetails`](#getdeploymentdetails), [`GetEmailSchedules`](#getemailschedules), [`GetFolders`](#getfolders), [`GetGroupDetails`](#getgroupdetails), [`GetGroups`](#getgroups), [`GetLinkableWorkspaces`](#getlinkableworkspaces), [`GetLinkedWorkspaces`](#getlinkedworkspaces), [`GetLinkedWorkspaceSyncDetails`](#getlinkedworkspacesyncdetails), [`GetQueryTableDetails`](#getquerytabledetails), [`GetQueryTables`](#getquerytables), [`GetReportMetadata`](#getreportmetadata), [`GetSecretKey`](#getsecretkey), [`GetSharedDetailsForViews`](#getshareddetailsforviews), [`GetShareInfo`](#getshareinfo), [`GetSlideshowDetails`](#getslideshowdetails), [`GetSlideshows`](#getslideshows), [`GetSlideshowURL`](#getslideshowurl), [`GetTaggedViews`](#gettaggedviews), [`GetTags`](#gettags), [`GetTrashViews`](#gettrashviews), [`GetVariableDetails`](#getvariabledetails), [`GetVariables`](#getvariables), [`GetViews`](#getviews), [`GetWorkspaceAccessRestrictions`](#getworkspaceaccessrestrictions), [`GetWorkspaceBackups`](#getworkspacebackups), [`GetWorkspaceBackupStatus`](#getworkspacebackupstatus), [`GetWorkspaceDetails`](#getworkspacedetails), [`GetWorkspaceLinkingCompatibility`](#getworkspacelinkingcompatibility), [`GetWorkspaceRestoreStatus`](#getworkspacerestorestatus), [`GetWorkspaceUsers`](#getworkspaceusers), [`LinkWorkspaces`](#linkworkspaces), [`MakeDefaultFolder`](#makedefaultfolder), [`MoveViewsToFolder`](#moveviewstofolder), [`RemoveAdmins`](#removeadmins), [`RemoveDefault`](#removedefault), [`RemoveFavorite`](#removefavorite), [`RemoveGroupMembers`](#removegroupmembers), [`RemoveShare`](#removeshare), [`RemoveTagFromViews`](#removetagfromviews), [`RemoveWorkspaceUsers`](#removeworkspaceusers), [`Rename`](#rename), [`RenameFolder`](#renamefolder), [`RenameGroup`](#renamegroup), [`RestoreTrashView`](#restoretrashview), [`RestoreWorkspaceFromBackup`](#restoreworkspacefrombackup), [`RunAlert`](#runalert), [`ShareViews`](#shareviews), [`SyncData`](#syncdata), [`SyncLinkedWorkspaces`](#synclinkedworkspaces), [`TriggerEmailSchedule`](#triggeremailschedule), [`UnlinkWorkspaces`](#unlinkworkspaces), [`UpdateAlert`](#updatealert), [`UpdateDashboard`](#updatedashboard), [`UpdateDatasourceConnection`](#updatedatasourceconnection), [`UpdateEmailSchedule`](#updateemailschedule), [`UpdateReport`](#updatereport), [`UpdateSlideshow`](#updateslideshow), [`UpdateTag`](#updatetag), [`UpdateVariable`](#updatevariable), [`UpdateWorkspaceAccessRestrictions`](#updateworkspaceaccessrestrictions)

### AddAdmins

```csharp
void AddAdmins(List emailIds, Dictionary config)
```

Add admins for the specified workspace.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the admin users to be added. |
| `config` | Contains any additional control configurations. Can be null. |

### AddDefault

```csharp
void AddDefault()
```

Adds a specified workspace as default.

### AddFavorite

```csharp
void AddFavorite()
```

Adds a specified workspace as favorite.

### AddGroupMembers

```csharp
void AddGroupMembers(long groupId, List emailIds, Dictionary config)
```

Add users to the specified group.

| Parameter | Description |
|---|---|
| `groupId` | The id of the group. |
| `emailIds` | The email address of the users to be added to the group. |
| `config` | Contains any additional control configurations. Can be null. |

### AddTagToViews

```csharp
void AddTagToViews(long tagId, List viewIds, Dictionary config)
```

Adds the specified tag to multiple views in the workspace.

| Parameter | Description |
|---|---|
| `tagId` | Id of the tag. |
| `viewIds` | View ids to be associated with the tag. |
| `config` | Contains any additional control configurations. Can be null. |

### AddWorkspaceUsers

```csharp
void AddWorkspaceUsers(List emailIds, string role, Dictionary config)
```

Add users to the specified workspace.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the users to be added. |
| `role` | Role of the users to be added. |
| `config` | Contains any additional control configurations. Can be null. |

### AutomlAnalysisPrediction

```csharp
JsonElement AutomlAnalysisPrediction(long analysisId, long modelId, Dictionary features, Dictionary config)
```

Get predictions by providing sample input values for a trained model.

**Returns** (`JsonElement`) — Prediction details.

### BackupWorkspaceNow

```csharp
JsonElement BackupWorkspaceNow(Dictionary config)
```

Trigger an instant backup for the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JsonElement`) — Triggered backup details.

### ChangeAlertStatus

```csharp
void ChangeAlertStatus(List alertIds, bool enabled, Dictionary config)
```

Enable or disable the specified data alerts in the workspace.

| Parameter | Description |
|---|---|
| `alertIds` | Ids of the data alerts. |
| `enabled` | Pass true to enable the data alerts and false to disable them. |
| `config` | Contains any additional control configurations. Can be null. |

### ChangeEmailScheduleStatus

```csharp
void ChangeEmailScheduleStatus(long scheduleId, string operation)
```

Update email schedule status.

| Parameter | Description |
|---|---|
| `scheduleId` | Id for the email schedule. |
| `operation` | New status for the schedule ( Values - activate | deactivate ) |

### ChangeFolderHierarchy

```csharp
void ChangeFolderHierarchy(long folderId, int hierarchy, Dictionary config)
```

Swaps the hierarchy of a parent folder and a subfolder.

| Parameter | Description |
|---|---|
| `folderId` | Id of the folder. |
| `hierarchy` | New hierarchy for the folder. (0 - Parent; 1 - Child) |
| `config` | Contains any additional control configurations. Can be null. |

### ChangeFolderPosition

```csharp
void ChangeFolderPosition(long folderId, long referenceFolderId, Dictionary config)
```

Place the folder above the reference folder.

| Parameter | Description |
|---|---|
| `folderId` | Id of the folder. |
| `referenceFolderId` | Id of the reference folder. |
| `config` | Contains any additional control configurations. Can be null. |

### ChangeWorkspaceUserRole

```csharp
void ChangeWorkspaceUserRole(List emailIds, string role, Dictionary config)
```

Change role for the specified users.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the users. |
| `role` | Name of the role. |
| `config` | Contains any additional control configurations. Can be null. |

### ChangeWorkspaceUserStatus

```csharp
void ChangeWorkspaceUserStatus(List emailIds, string operation, Dictionary config)
```

Change users staus in the specified workspace.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the users. |
| `operation` | New status for the users ( Values - activate | deactivate ) |
| `config` | Contains any additional control configurations. Can be null. |

### Copy

```csharp
long Copy(string newWorkspaceName, Dictionary config, long? destOrgId)
```

Copy the specified workspace from one organization to another or within the organization.

| Parameter | Description |
|---|---|
| `newWorkspaceName` | Name of the new workspace. |
| `config` | Contains any additional control configurations. Can be null. |
| `destOrgId` | Id of the organization where the destination workspace is present. Can be null. |

**Returns** (`long`) — New workspace id.

### CopyViews

```csharp
JsonElement CopyViews(List viewIds, long destWorkspaceId, Dictionary config, long? destOrgId)
```

Copy the specified views from one workspace to another workspace.

| Parameter | Description |
|---|---|
| `viewIds` | The id of the views to be copied. |
| `destWorkspaceId` | The destination workspace id. |
| `config` | Contains any additional control configurations. Can be null. |
| `destOrgId` | Id of the organization where the destination workspace is present. Can be null. |

**Returns** (`JsonElement`) — Views list.

### CreateAutomlAnalysis

```csharp
long CreateAutomlAnalysis(string name, long trainingTableId, string predictionType, List features, int serverOption, Dictionary algorithms, Dictionary config)
```

Create a new AutoML analysis within the provided workspace.

**Returns** (`long`) — Created AutoML Analysis Id.

### CreateAutomlAnalysisDeployment

```csharp
JsonElement CreateAutomlAnalysisDeployment(long analysisId, long modelId, long inputTableId, string outputTable, List outputColumns, string predictionColumn, int serverOption, string importType, Dictionary scheduleDetails, Dictionary config)
```

Deploy the AutoML analysis model.

**Returns** (`JsonElement`) — Deployment details.

### CreateDashboard

```csharp
long CreateDashboard(string displayName, string layout, Dictionary config)
```

Create a dashboard in the specified workspace.

| Parameter | Description |
|---|---|
| `displayName` | Name of the dashboard. |
| `layout` | Layout configuration of the dashboard. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — New dashboard id.

### CreateEmailSchedule

```csharp
long CreateEmailSchedule(string scheduleName, List viewIds, string format, List emailIds, Dictionary scheduleDetails, Dictionary config)
```

Create an email schedule in the specified workspace.

| Parameter | Description |
|---|---|
| `scheduleName` | Name of the email schedule. |
| `viewIds` | View ids to be mailed. |
| `format` | The format in which the data has to be mailed. |
| `emailIds` | The recipients' email addresses for sending views. |
| `scheduleDetails` | Contains schedule frequency, date, and time info. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — Email schedule id.

### CreateFolder

```csharp
long CreateFolder(string folderName, Dictionary config)
```

Create a folder in the specified workspace.

| Parameter | Description |
|---|---|
| `folderName` | The name of the folder. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — Folder id.

### CreateGroup

```csharp
long CreateGroup(string groupName, List emailIds, Dictionary config)
```

Create a group in the specified workspace.

| Parameter | Description |
|---|---|
| `groupName` | Name of the group. |
| `emailIds` | The email address of the users to be added to the group. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — Group id.

### CreateQueryTable

```csharp
long CreateQueryTable(string sqlQuery, string queryTableName, Dictionary config)
```

Create a new query table in the workspace.

| Parameter | Description |
|---|---|
| `sqlQuery` | SQL query to construct the query table. |
| `queryTableName` | Name of the query table to be created. |
| `config` | Contains the control configurations. |

**Returns** (`long`) — View id.

### CreateReport

```csharp
long CreateReport(Dictionary config)
```

Create a report in the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains the control configurations. |

**Returns** (`long`) — Created view id.

### CreateSlideshow

```csharp
long CreateSlideshow(string slideName, List viewIds, Dictionary config)
```

Create a slideshow in the specified workspace.

| Parameter | Description |
|---|---|
| `slideName` | Name of the slideshow to be created. |
| `viewIds` | Ids of the view to be included in the slideshow. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — Slideshow id.

### CreateTable

```csharp
long CreateTable(Dictionary tableDesign)
```

Create a table in the specified workspace.

| Parameter | Description |
|---|---|
| `tableDesign` | Table structure. |

**Returns** (`long`) — Table id.

### CreateTag

```csharp
string CreateTag(string tagName, string colorCode, Dictionary config)
```

Create a tag in the specified workspace.

| Parameter | Description |
|---|---|
| `tagName` | Name of the tag to be created. |
| `colorCode` | Color of the tag in HEX color code. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`string`) — Created tag id.

### CreateVariable

```csharp
long CreateVariable(string variableName, int variableDataType, int variableType, Dictionary config)
```

Create a variable in the workspace.

| Parameter | Description |
|---|---|
| `variableName` | Name of the variable to be created. |
| `variableDataType` | Datatype of the variable to be created. |
| `variableType` | Type of the variable to be created. |
| `config` | Contains the control configurations. |

**Returns** (`long`) — Variable id.

### Delete

```csharp
void Delete()
```

Delete a specified workspace in the organization.

### DeleteAlerts

```csharp
void DeleteAlerts(List alertIds, Dictionary config)
```

Delete the specified data alerts from the workspace.

| Parameter | Description |
|---|---|
| `alertIds` | Ids of the data alerts to be deleted. |
| `config` | Contains any additional control configurations. Can be null. |

### DeleteAutomlAnalysis

```csharp
void DeleteAutomlAnalysis(long analysisId, Dictionary config)
```

Delete a specified AutoML analysis from the given workspace.

| Parameter | Description |
|---|---|
| `analysisId` | Id of the AutoML Analysis to be deleted. |
| `config` | Contains any additional control parameters. Can be null. |

### DeleteAutomlAnalysisDeployment

```csharp
void DeleteAutomlAnalysisDeployment(long analysisId, long deploymentId, Dictionary config)
```

Delete the AutoML analysis deployment.

| Parameter | Description |
|---|---|
| `analysisId` | Id of the AutoML Analysis. |
| `deploymentId` | Id of the deployment to be deleted. |
| `config` | Contains any additional control parameters. Can be null. |

### DeleteAutomlAnalysisModel

```csharp
void DeleteAutomlAnalysisModel(long analysisId, long modelId, Dictionary config)
```

Delete a specified model available in the given AutoML analysis.

| Parameter | Description |
|---|---|
| `analysisId` | Id of the AutoML Analysis. |
| `modelId` | Id of the model to be deleted. |
| `config` | Contains any additional control parameters. Can be null. |

### DeleteEmailSchedule

```csharp
void DeleteEmailSchedule(long scheduleId)
```

Delete the specified email schedule in the workspace.

| Parameter | Description |
|---|---|
| `scheduleId` | Id for the email schedule. |

### DeleteFolder

```csharp
void DeleteFolder(long folderId)
```

Delete a specified folder in the workspace.

| Parameter | Description |
|---|---|
| `folderId` | The id of the folder. |

### DeleteGroup

```csharp
void DeleteGroup(long groupId)
```

Delete a specified group.

| Parameter | Description |
|---|---|
| `groupId` | The id of the group. |

### DeleteSlideshow

```csharp
void DeleteSlideshow(long slideId)
```

Delete a specified slideshow in the workspace.

| Parameter | Description |
|---|---|
| `slideId` | The id of the slideshow. |

### DeleteTag

```csharp
void DeleteTag(long tagId)
```

Delete the specified tag from the workspace.

| Parameter | Description |
|---|---|
| `tagId` | Id of the tag. |

### DeleteTrashView

```csharp
void DeleteTrashView(long viewId, Dictionary config)
```

Delete the specified view permanently from trash.

| Parameter | Description |
|---|---|
| `viewId` | Id of the view. |
| `config` | Contains any additional control configurations. Can be null. |

### DeleteVariable

```csharp
void DeleteVariable(long variableId)
```

Delete a specified variable in the workspace.

| Parameter | Description |
|---|---|
| `variableId` | The id of the variable. |

### DeployAutomlAnalysis

```csharp
void DeployAutomlAnalysis(long analysisId, long deploymentId, Dictionary config)
```

Execute the AutoML analysis deployment.

| Parameter | Description |
|---|---|
| `analysisId` | Id of the AutoML Analysis. |
| `deploymentId` | Id of the deployment to execute. |
| `config` | Contains any additional control parameters. Can be null. |

### DisableDomainAccess

```csharp
void DisableDomainAccess()
```

Disable workspace from the specified white label domain.

### DownloadWorkspaceBackup

```csharp
void DownloadWorkspaceBackup(long backupId, string filePath, Dictionary config)
```

Download the specified workspace backup.

| Parameter | Description |
|---|---|
| `backupId` | Id of the backup. |
| `filePath` | Path of the file where the downloaded backup is to be stored. |
| `config` | Contains any additional control configurations. Can be null. |

### EditQueryTable

```csharp
void EditQueryTable(long viewId, string sqlQuery, Dictionary config)
```

Update the mentioned query table in the workspace.

| Parameter | Description |
|---|---|
| `viewId` | Id of the query table to be updated. |
| `sqlQuery` | New SQL query to be updated. |
| `config` | Contains the control configurations. |

### EnableDomainAccess

```csharp
void EnableDomainAccess()
```

Enable workspace to the specified white label domain.

### ExportAsTemplate

```csharp
void ExportAsTemplate(List viewIds, string filePath, Dictionary config)
```

Export the views as templates.

| Parameter | Description |
|---|---|
| `viewId` | Ids of the view to be exported. |
| `filePath` | Path of the file where the data exported to be stored. ( Should be in 'atpt' format ) |
| `config` | Contains any additional control configurations. Can be null. |

### GetAdmins

```csharp
JsonElement GetAdmins()
```

Returns list of admins for the specified workspace.

**Returns** (`JsonElement`) — Workspace admins list.

### GetAggregateFormulaDependents

```csharp
JsonElement GetAggregateFormulaDependents(long formulaId)
```

Returns list of all dependent views and formulas for the specified aggregate formula.

| Parameter | Description |
|---|---|
| `formulaId` | Id of the aggregate formula. |

**Returns** (`JsonElement`) — Dependent details

### GetAggregateFormulas

```csharp
JsonElement GetAggregateFormulas(Dictionary config)
```

Returns list of all aggregate formulas for the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JsonElement`) — Aggregate formula list

### GetAggregateFormulaValue

```csharp
string GetAggregateFormulaValue(long formulaId)
```

Returns the value of the aggregate formula.

| Parameter | Description |
|---|---|
| `formulaId` | Id of the aggregate formula. |

**Returns** (`string`) — Aggregate formula value

### GetAlertConfiguration

```csharp
JsonElement GetAlertConfiguration(long alertId)
```

Returns the configuration of the specified data alert.

| Parameter | Description |
|---|---|
| `alertId` | Id of the data alert. |

**Returns** (`JsonElement`) — Data alert configuration.

### GetAlertEvents

```csharp
JsonElement GetAlertEvents(long alertId, Dictionary config)
```

Returns the execution events of the specified data alert.

| Parameter | Description |
|---|---|
| `alertId` | Id of the data alert. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JsonElement`) — Data alert events along with the page details.

### GetAlertsInWorkspace

```csharp
JsonElement GetAlertsInWorkspace()
```

Returns list of data alerts available in the specified workspace.

**Returns** (`JsonElement`) — Data alerts list.

### GetAutomlAnalysis

```csharp
JsonElement GetAutomlAnalysis()
```

Returns list of AutoML analysis for the specified workspace.

**Returns** (`JsonElement`) — AutoML analysis list.

### GetAutomlAnalysisDetails

```csharp
JsonElement GetAutomlAnalysisDetails(long analysisId)
```

Retrieve detailed information for a specific AutoML analysis.

| Parameter | Description |
|---|---|
| `analysisId` | Id of the AutoML Analysis. |

**Returns** (`JsonElement`) — AutoML analysis details.

### GetDashboardMetadata

```csharp
JsonElement GetDashboardMetadata(long dashboardId, Dictionary config)
```

Returns the metadata of the specified dashboard.

| Parameter | Description |
|---|---|
| `dashboardId` | Id of the dashboard. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JsonElement`) — Dashboard configuration.

### GetDatasources

```csharp
JsonElement GetDatasources()
```

Returns list of datasources for the specified workspace.

**Returns** (`JsonElement`) — Datasource list.

### GetDeploymentDetails

```csharp
JsonElement GetDeploymentDetails(long analysisId, long modelId)
```

Returns deployment details available for an AutoML analysis model.

| Parameter | Description |
|---|---|
| `analysisId` | Id of the AutoML analysis. |
| `modelId` | Id of the AutoML model. |

**Returns** (`JsonElement`) — Deployment details.

### GetEmailSchedules

```csharp
JsonElement GetEmailSchedules()
```

Returns list of email schedules available in the specified workspace.

**Returns** (`JsonElement`) — List of email schedules.

### GetFolders

```csharp
JsonElement GetFolders()
```

Returns list of all accessible folders for the specified workspace.

**Returns** (`JsonElement`) — Folders list.

### GetGroupDetails

```csharp
JsonElement GetGroupDetails(long groupId)
```

Returns details of the specified group.

| Parameter | Description |
|---|---|
| `groupId` | The id of the group. |

**Returns** (`JsonElement`) — Group details.

### GetGroups

```csharp
JsonElement GetGroups()
```

Returns list of groups for the specified workspace.

**Returns** (`JsonElement`) — Groups list.

### GetLinkableWorkspaces

```csharp
JsonElement GetLinkableWorkspaces()
```

Returns list of organizations and workspaces that can be linked to the specified master workspace.

**Returns** (`JsonElement`) — Organizations with their linkable workspaces.

### GetLinkedWorkspaces

```csharp
JsonElement GetLinkedWorkspaces()
```

Returns list of workspaces linked to the specified master workspace.

**Returns** (`JsonElement`) — Linked workspaces list.

### GetLinkedWorkspaceSyncDetails

```csharp
JsonElement GetLinkedWorkspaceSyncDetails(List sandboxIds, Dictionary config)
```

Returns the sync details of the specified linked workspaces.

| Parameter | Description |
|---|---|
| `sandboxIds` | Ids of the linked workspaces for which the sync details are fetched. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JsonElement`) — Linked workspace sync details.

### GetQueryTableDetails

```csharp
JsonElement GetQueryTableDetails(long queryTableId)
```

Returns details of the specified query table.

| Parameter | Description |
|---|---|
| `queryTableId` | Id of the query table. |

**Returns** (`JsonElement`) — Query table details.

### GetQueryTables

```csharp
JsonElement GetQueryTables(Dictionary config)
```

Returns list of all query tables for the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JsonElement`) — Query table list.

### GetReportMetadata

```csharp
JsonElement GetReportMetadata(long viewId)
```

Returns the metadata of the specified report.

| Parameter | Description |
|---|---|
| `viewId` | Id of the report. |

**Returns** (`JsonElement`) — Report configuration.

### GetSecretKey

```csharp
string GetSecretKey(Dictionary config)
```

Returns the secret key of the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`string`) — Workspace secret key.

### GetSharedDetailsForViews

```csharp
JsonElement GetSharedDetailsForViews(List viewIds)
```

Returns shared details of the specified views.

| Parameter | Description |
|---|---|
| `viewIds` | View ids for which sharing details are required. |

**Returns** (`JsonElement`) — Shared details.

### GetShareInfo

```csharp
JsonElement GetShareInfo()
```

Returns shared details of the specified workspace.

**Returns** (`JsonElement`) — Shared details.

### GetSlideshowDetails

```csharp
JsonElement GetSlideshowDetails(long slideId)
```

Returns details of the specified slideshow.

| Parameter | Description |
|---|---|
| `slideId` | The id of the slideshow. |

**Returns** (`JsonElement`) — Slideshow details.

### GetSlideshows

```csharp
JsonElement GetSlideshows()
```

Returns list of slideshows for the specified workspace.

**Returns** (`JsonElement`) — Slideshow list.

### GetSlideshowURL

```csharp
string GetSlideshowURL(long slideId, Dictionary config)
```

Returns slide URL to access the specified slideshow.

| Parameter | Description |
|---|---|
| `slideId` | The id of the slideshow. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`string`) — Slideshow URL.

### GetTaggedViews

```csharp
JsonElement GetTaggedViews(long tagId)
```

Returns the list of views associated with the specified tag.

| Parameter | Description |
|---|---|
| `tagId` | Id of the tag. |

**Returns** (`JsonElement`) — Tagged views list.

### GetTags

```csharp
JsonElement GetTags()
```

Returns list of all tags for the specified workspace.

**Returns** (`JsonElement`) — Tags list.

### GetTrashViews

```csharp
JsonElement GetTrashViews()
```

Returns list of all views available in trash for the specified workspace.

**Returns** (`JsonElement`) — Views list.

### GetVariableDetails

```csharp
JsonElement GetVariableDetails(long variableId)
```

Returns details of the specified variable.

| Parameter | Description |
|---|---|
| `variableId` | The id of the variable. |

**Returns** (`JsonElement`) — Variable details.

### GetVariables

```csharp
JsonElement GetVariables()
```

Returns list of variables for the specified workspace.

**Returns** (`JsonElement`) — Variables list.

### GetViews

```csharp
JsonElement GetViews(Dictionary config)
```

Returns list of all accessible views for the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JsonElement`) — Views list.

### GetWorkspaceAccessRestrictions

```csharp
JsonElement GetWorkspaceAccessRestrictions()
```

Returns the access restriction settings configured for the specified workspace.

**Returns** (`JsonElement`) — Workspace access restriction settings.

### GetWorkspaceBackups

```csharp
JsonElement GetWorkspaceBackups()
```

Returns the backup configuration and the list of backups available for the specified workspace.

**Returns** (`JsonElement`) — Workspace backup details.

### GetWorkspaceBackupStatus

```csharp
JsonElement GetWorkspaceBackupStatus(long backupId)
```

Returns the status of the specified workspace backup.

| Parameter | Description |
|---|---|
| `backupId` | Id of the backup. |

**Returns** (`JsonElement`) — Backup status details.

### GetWorkspaceDetails

```csharp
JsonElement GetWorkspaceDetails(Dictionary config)
```

Returns details of the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JsonElement`) — Workspace details.

### GetWorkspaceLinkingCompatibility

```csharp
JsonElement GetWorkspaceLinkingCompatibility(List > clients, Dictionary config)
```

Returns the linking compatibility details for the specified client workspaces.

| Parameter | Description |
|---|---|
| `clients` | Contains the client workspaces to be verified for linking compatibility. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JsonElement`) — Client workspace compatibility details.

### GetWorkspaceRestoreStatus

```csharp
JsonElement GetWorkspaceRestoreStatus(long restoreId)
```

Returns the status of the specified workspace restore.

| Parameter | Description |
|---|---|
| `restoreId` | Id of the restore. |

**Returns** (`JsonElement`) — Restore status details.

### GetWorkspaceUsers

```csharp
JsonElement GetWorkspaceUsers()
```

Returns list of users for the specified workspace.

**Returns** (`JsonElement`) — List of users.

### LinkWorkspaces

```csharp
void LinkWorkspaces(List > clients, Dictionary config)
```

Link the specified client workspaces to the master workspace.

| Parameter | Description |
|---|---|
| `clients` | Contains the client workspaces to be linked with the master workspace. |
| `config` | Contains any additional control configurations. Can be null. |

### MakeDefaultFolder

```csharp
void MakeDefaultFolder(long folderId)
```

Make the specified folder as default.

| Parameter | Description |
|---|---|
| `folderId` | The id of the folder. |

### MoveViewsToFolder

```csharp
void MoveViewsToFolder(long folderId, List viewIds, Dictionary config)
```

Move views to the mentioned folder.

| Parameter | Description |
|---|---|
| `folderId` | Id of the folder. |
| `viewIds` | View ids to be moved. |
| `config` | Contains any additional control configurations. Can be null. |

### RemoveAdmins

```csharp
void RemoveAdmins(List emailIds, Dictionary config)
```

Remove admins from the specified workspace.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the admin users to be removed. |
| `config` | Contains any additional control configurations. Can be null. |

### RemoveDefault

```csharp
void RemoveDefault()
```

Remove a specified workspace from default.

### RemoveFavorite

```csharp
void RemoveFavorite()
```

Remove a specified workspace from favorite.

### RemoveGroupMembers

```csharp
void RemoveGroupMembers(long groupId, List emailIds, Dictionary config)
```

Remove users from the specified group.

| Parameter | Description |
|---|---|
| `groupId` | The id of the group. |
| `emailIds` | The email address of the users to be removed from the group. |
| `config` | Contains any additional control configurations. Can be null. |

### RemoveShare

```csharp
void RemoveShare(List viewIds, List emailIds, Dictionary config)
```

Remove shared views for the specified users.

| Parameter | Description |
|---|---|
| `viewIds` | View ids whose sharing needs to be removed. |
| `emailIds` | The email address of the users to whom the sharing need to be removed. |
| `config` | Contains any additional control configurations. Can be null. |

### RemoveTagFromViews

```csharp
void RemoveTagFromViews(long tagId, List viewIds, bool dissociateAll, Dictionary config)
```

Removes the specified tag from multiple views in the workspace.

| Parameter | Description |
|---|---|
| `tagId` | Id of the tag. |
| `viewIds` | View ids to be dissociated. Not required when dissociateAll is true. |
| `dissociateAll` | If true, dissociates the tag from all associated views. |
| `config` | Contains any additional control configurations. Can be null. |

### RemoveWorkspaceUsers

```csharp
void RemoveWorkspaceUsers(List emailIds, Dictionary config)
```

Remove users from the specified workspace.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the users to be removed. |
| `config` | Contains any additional control configurations. Can be null. |

### Rename

```csharp
void Rename(string workspaceName, Dictionary config)
```

Rename a specified workspace in the organization.

| Parameter | Description |
|---|---|
| `workspaceName` | New name of the workspace. |
| `config` | Contains any additional control configurations. Can be null. |

### RenameFolder

```csharp
void RenameFolder(long folderId, string folderName, Dictionary config)
```

Rename a specified folder in the workspace.

| Parameter | Description |
|---|---|
| `folderId` | The id of the folder. |
| `folderName` | The new name of the folder. |
| `config` | Contains any additional control configurations. Can be null. |

### RenameGroup

```csharp
void RenameGroup(long groupId, string groupName, Dictionary config)
```

Rename a specified group.

| Parameter | Description |
|---|---|
| `groupId` | The id of the group. |
| `groupName` | The new name of the group. |
| `config` | Contains any additional control configurations. Can be null. |

### RestoreTrashView

```csharp
void RestoreTrashView(long viewId, Dictionary config)
```

Restore the specified view from trash.

| Parameter | Description |
|---|---|
| `viewId` | Id of the view. |
| `config` | Contains any additional control configurations. Can be null. |

### RestoreWorkspaceFromBackup

```csharp
JsonElement RestoreWorkspaceFromBackup(long backupId, bool confirmRestore, Dictionary config)
```

Restore the specified workspace from the given backup.

| Parameter | Description |
|---|---|
| `backupId` | Id of the backup. |
| `confirmRestore` | Pass true to confirm that the existing workspace data can be overwritten. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JsonElement`) — Triggered restore details.

### RunAlert

```csharp
void RunAlert(long alertId, Dictionary config)
```

Execute the specified data alert immediately.

| Parameter | Description |
|---|---|
| `alertId` | Id of the data alert. |
| `config` | Contains any additional control configurations. Can be null. |

### ShareViews

```csharp
void ShareViews(List viewIds, List emailIds, Dictionary permissions, Dictionary config)
```

Share views to the specified users.

| Parameter | Description |
|---|---|
| `viewIds` | View ids which to be shared. |
| `emailIds` | The email address of the users to whom the views need to be shared. |
| `permissions` | Contains permission details. |
| `config` | Contains any additional control configurations. Can be null. |

### SyncData

```csharp
void SyncData(long datasourceId, Dictionary config)
```

Initiate data sync for the specified datasource.

| Parameter | Description |
|---|---|
| `datasourceId` | Id of the datasource. |
| `config` | Contains any additional control configurations. Can be null. |

### SyncLinkedWorkspaces

```csharp
void SyncLinkedWorkspaces(string scope, Dictionary config)
```

Sync the metadata of the master workspace to its linked client workspaces.

| Parameter | Description |
|---|---|
| `scope` | Scope of the sync operation. |
| `config` | Contains any additional control configurations. Can be null. |

### TriggerEmailSchedule

```csharp
void TriggerEmailSchedule(long scheduleId)
```

Trigger configured email schedules instantly.

| Parameter | Description |
|---|---|
| `scheduleId` | Id for the email schedule. |

### UnlinkWorkspaces

```csharp
void UnlinkWorkspaces(string scope, Dictionary config)
```

Unlink the client workspaces from the specified master workspace.

| Parameter | Description |
|---|---|
| `scope` | Scope of the unlink operation. |
| `config` | Contains any additional control configurations. Can be null. |

### UpdateAlert

```csharp
void UpdateAlert(long alertId, string alertName, Dictionary scheduleDetails, List > rules, Dictionary config)
```

Update the specified data alert in the workspace.

| Parameter | Description |
|---|---|
| `alertId` | Id of the data alert. |
| `alertName` | Name of the data alert. |
| `scheduleDetails` | Contains the schedule configurations of the data alert. |
| `rules` | Contains the rules to be evaluated by the data alert. |
| `config` | Contains any additional control configurations. Can be null. |

### UpdateDashboard

```csharp
void UpdateDashboard(long dashboardId, Dictionary config)
```

Update the specified dashboard in the workspace.

| Parameter | Description |
|---|---|
| `dashboardId` | Id of the dashboard. |
| `config` | Contains the dashboard configurations to be updated. |

### UpdateDatasourceConnection

```csharp
void UpdateDatasourceConnection(long datasourceId, Dictionary config)
```

Update connection details for the specified datasource.

| Parameter | Description |
|---|---|
| `datasourceId` | Id of the datasource. |
| `config` | Contains the control configurations. |

### UpdateEmailSchedule

```csharp
long UpdateEmailSchedule(long scheduleId, Dictionary config)
```

Update configurations of the specified email schedule in the workspace.

| Parameter | Description |
|---|---|
| `scheduleId` | Id for the email schedule. |
| `config` | Contains the control configurations. |

**Returns** (`long`) — Updated schedule id.

### UpdateReport

```csharp
void UpdateReport(long viewId, Dictionary config)
```

Update the design and configuration of the specified report.

| Parameter | Description |
|---|---|
| `viewId` | Id for the view. |
| `config` | Contains the control configurations. |

### UpdateSlideshow

```csharp
void UpdateSlideshow(long slideId, Dictionary config)
```

Update details of the specified slideshow.

| Parameter | Description |
|---|---|
| `slideId` | The id of the slideshow. |
| `config` | Contains any additional control configurations. Can be null. |

### UpdateTag

```csharp
void UpdateTag(long tagId, Dictionary config)
```

Update details of the specified tag in the workspace.

| Parameter | Description |
|---|---|
| `tagId` | Id of the tag. |
| `config` | Contains the control configurations. |

### UpdateVariable

```csharp
void UpdateVariable(long variableId, string variableName, int variableDataType, int variableType, Dictionary config)
```

Update details of the specified variable in the workspace.

| Parameter | Description |
|---|---|
| `variableId` | Id for the variable. |
| `variableName` | New name for the variable. |
| `variableDataType` | New datatype for the variable. |
| `variableType` | New type for the variable. |
| `config` | Contains the control configurations. |

### UpdateWorkspaceAccessRestrictions

```csharp
void UpdateWorkspaceAccessRestrictions(Dictionary config)
```

Update the access restriction settings of the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains the access restriction configurations to be updated. |

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
