# WorkspaceAPI

```go
org       := ZAnalytics.GetOrgInstance(&ac, orgId)
workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
view      := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
bulk      := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
```

`WorkspaceAPI` exposes **116 methods**. Method names are `PascalCase` (exported) and identifiers are `string`.

## Methods

[`AddAdmins`](#addadmins), [`AddDefault`](#adddefault), [`AddFavorite`](#addfavorite), [`AddGroupMembers`](#addgroupmembers), [`AddTagToViews`](#addtagtoviews), [`AddWorkspaceUsers`](#addworkspaceusers), [`AutoMLAnalysisPrediction`](#automlanalysisprediction), [`BackupWorkspaceNow`](#backupworkspacenow), [`ChangeAlertStatus`](#changealertstatus), [`ChangeEmailScheduleStatus`](#changeemailschedulestatus), [`ChangeFolderHierarchy`](#changefolderhierarchy), [`ChangeFolderPosition`](#changefolderposition), [`ChangeWorkspaceUserRole`](#changeworkspaceuserrole), [`ChangeWorkspaceUserStatus`](#changeworkspaceuserstatus), [`Copy`](#copy), [`CopyViews`](#copyviews), [`CreateAutoMLAnalysis`](#createautomlanalysis), [`CreateAutoMLAnalysisDeployment`](#createautomlanalysisdeployment), [`CreateDashboard`](#createdashboard), [`CreateEmailSchedule`](#createemailschedule), [`CreateFolder`](#createfolder), [`CreateGroup`](#creategroup), [`CreateQueryTable`](#createquerytable), [`CreateReport`](#createreport), [`CreateSlideshow`](#createslideshow), [`CreateTable`](#createtable), [`CreateTag`](#createtag), [`CreateVariable`](#createvariable), [`Delete`](#delete), [`DeleteAlerts`](#deletealerts), [`DeleteAutoMLAnalysis`](#deleteautomlanalysis), [`DeleteAutoMLAnalysisDeployment`](#deleteautomlanalysisdeployment), [`DeleteAutoMLAnalysisModel`](#deleteautomlanalysismodel), [`DeleteEmailSchedule`](#deleteemailschedule), [`DeleteFolder`](#deletefolder), [`DeleteGroup`](#deletegroup), [`DeleteSlideshow`](#deleteslideshow), [`DeleteTag`](#deletetag), [`DeleteTrashView`](#deletetrashview), [`DeleteVariable`](#deletevariable), [`DeployAutoMLAnalysis`](#deployautomlanalysis), [`DisableDomainAccess`](#disabledomainaccess), [`DownloadWorkspaceBackup`](#downloadworkspacebackup), [`EditQueryTable`](#editquerytable), [`EnableDomainAccess`](#enabledomainaccess), [`ExportAsTemplate`](#exportastemplate), [`GetAdmins`](#getadmins), [`GetAggregateFormulaDependents`](#getaggregateformuladependents), [`GetAggregateFormulas`](#getaggregateformulas), [`GetAggregateFormulaValue`](#getaggregateformulavalue), [`GetAlertConfiguration`](#getalertconfiguration), [`GetAlertEvents`](#getalertevents), [`GetAlertsInWorkspace`](#getalertsinworkspace), [`GetAutoMLAnalysis`](#getautomlanalysis), [`GetAutoMLAnalysisDetails`](#getautomlanalysisdetails), [`GetDashboardMetadata`](#getdashboardmetadata), [`GetDatasources`](#getdatasources), [`GetDeploymentDetails`](#getdeploymentdetails), [`GetEmailSchedules`](#getemailschedules), [`GetFolders`](#getfolders), [`GetGroupDetails`](#getgroupdetails), [`GetGroups`](#getgroups), [`GetLinkableWorkspaces`](#getlinkableworkspaces), [`GetLinkedWorkspaces`](#getlinkedworkspaces), [`GetLinkedWorkspaceSyncDetails`](#getlinkedworkspacesyncdetails), [`GetQueryTableDetails`](#getquerytabledetails), [`GetQueryTables`](#getquerytables), [`GetReportMetadata`](#getreportmetadata), [`GetSecretKey`](#getsecretkey), [`GetSharedDetailsForViews`](#getshareddetailsforviews), [`GetShareInfo`](#getshareinfo), [`GetSlideshowDetails`](#getslideshowdetails), [`GetSlideshows`](#getslideshows), [`GetSlideshowUrl`](#getslideshowurl), [`GetTaggedViews`](#gettaggedviews), [`GetTags`](#gettags), [`GetTrashViews`](#gettrashviews), [`GetVariableDetails`](#getvariabledetails), [`GetVariables`](#getvariables), [`GetViews`](#getviews), [`GetWorkspaceAccessRestrictions`](#getworkspaceaccessrestrictions), [`GetWorkspaceBackups`](#getworkspacebackups), [`GetWorkspaceBackupStatus`](#getworkspacebackupstatus), [`GetWorkspaceLinkingCompatibility`](#getworkspacelinkingcompatibility), [`GetWorkspaceRestoreStatus`](#getworkspacerestorestatus), [`GetWorkspaceUsers`](#getworkspaceusers), [`LinkWorkspaces`](#linkworkspaces), [`MakeDefaultFolder`](#makedefaultfolder), [`MoveViewsToFolder`](#moveviewstofolder), [`RemoveAdmins`](#removeadmins), [`RemoveDefault`](#removedefault), [`RemoveFavorite`](#removefavorite), [`RemoveGroupMembers`](#removegroupmembers), [`RemoveShare`](#removeshare), [`RemoveTagFromViews`](#removetagfromviews), [`RemoveWorkspaceUsers`](#removeworkspaceusers), [`Rename`](#rename), [`RenameFolder`](#renamefolder), [`RenameGroup`](#renamegroup), [`RestoreTrashView`](#restoretrashview), [`RestoreWorkspaceFromBackup`](#restoreworkspacefrombackup), [`RunAlert`](#runalert), [`ShareViews`](#shareviews), [`SyncData`](#syncdata), [`SyncLinkedWorkspaces`](#synclinkedworkspaces), [`TriggerEmailSchedule`](#triggeremailschedule), [`UnlinkWorkspaces`](#unlinkworkspaces), [`UpdateAlert`](#updatealert), [`UpdateDashboard`](#updatedashboard), [`UpdateDatasourceConnection`](#updatedatasourceconnection), [`UpdateEmailSchedule`](#updateemailschedule), [`UpdateReport`](#updatereport), [`UpdateSlideshow`](#updateslideshow), [`UpdateTag`](#updatetag), [`UpdateVariable`](#updatevariable), [`UpdateWorkspaceAccessRestrictions`](#updateworkspaceaccessrestrictions)

### AddAdmins

```go
AddAdmins(emailids interface{}, config map[string]interface{}) (serverexception *ServerException)
```

Add admins for the specified workspace.

| Parameter | Description |
|---|---|
| `emailids` | The email address of the admin users to be added. |
| `config` | Contains any additional control configurations. |

### AddDefault

```go
AddDefault() (serverexception *ServerException)
```

Adds a specified workspace as default.

### AddFavorite

```go
AddFavorite() (serverexception *ServerException)
```

Adds a specified workspace as favorite.

### AddGroupMembers

```go
AddGroupMembers(groupid string, emailids interface{}, config map[string]interface{}) (serverexception *ServerException)
```

Add users to the specified group.

| Parameter | Description |
|---|---|
| `groupid` | The id of the group. |
| `emailids` | The email address of the users to be added to the group. |
| `config` | Contains any additional control configurations. |

### AddTagToViews

```go
AddTagToViews(tagid string, viewids interface{}, config map[string]interface{}) (serverexception *ServerException)
```

Adds the specified tag to multiple views in the workspace.

| Parameter | Description |
|---|---|
| `tagid` | Id of the tag. |
| `viewids` | View ids to be associated with the tag. |
| `config` | Contains any additional control configurations. |

### AddWorkspaceUsers

```go
AddWorkspaceUsers(emailids interface{}, role string, config map[string]interface{}) (serverexception *ServerException)
```

Add users to the specified workspace.

| Parameter | Description |
|---|---|
| `emailids` | The email address of the users to be added. |
| `role` | Role of the users to be added. |
| `config` | Contains any additional control configurations. |

### AutoMLAnalysisPrediction

```go
AutoMLAnalysisPrediction(analysisid string, modelid string, features map[string]interface{}, config map[string]interface{},) (prediction interface{}, serverexception *ServerException)
```

Get predictions using a trained AutoML model.

| Parameter | Description |
|---|---|
| `analysisid` | Id of the AutoML Analysis. |
| `modelid` | Id of the AutoML Analysis model. |
| `features` | Feature name to value mapping. |
| `config` | Contains any additional control parameters. |

**Returns** — Returns prediction details as interface.

### BackupWorkspaceNow

```go
BackupWorkspaceNow(config map[string]interface{}) (backupdetails interface{}, serverexception *ServerException)
```

Trigger an instant backup for the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. |

**Returns** — Returns the triggered backup details as interface.

### ChangeAlertStatus

```go
ChangeAlertStatus(alertids interface{}, enabled bool, config map[string]interface{}) (serverexception *ServerException)
```

Enable or disable the specified data alerts in the workspace.

| Parameter | Description |
|---|---|
| `alertids` | Ids of the data alerts. |
| `enabled` | Pass true to enable the data alerts and false to disable them. |
| `config` | Contains any additional control configurations. |

### ChangeEmailScheduleStatus

```go
ChangeEmailScheduleStatus(scheduleid, operation string) (serverexception *ServerException)
```

Trigger configured email schedules instantly.

| Parameter | Description |
|---|---|
| `scheduleid` | Id for the email schedule. |
| `operation` | New status for the schedule ( Values - activate | deactivate ). |

### ChangeFolderHierarchy

```go
ChangeFolderHierarchy(folderid string, hierarchy int, config map[string]interface{}) (serverexception *ServerException)
```

Swaps the hierarchy of a parent folder and a subfolder.

| Parameter | Description |
|---|---|
| `folderid` | The id of the folder. |
| `hierarchy` | New hierarchy for the folder. (0 - Parent; 1 - Child) |
| `config` | Contains any additional control configurations. |

### ChangeFolderPosition

```go
ChangeFolderPosition(folderid, referencefolderid string, config map[string]interface{}) (serverexception *ServerException)
```

Place the folder above the reference folder.

| Parameter | Description |
|---|---|
| `folderid` | Id of the folder to be moved. |
| `referencefolderid` | Id of the reference folder. |
| `config` | Contains any additional control configurations. |

### ChangeWorkspaceUserRole

```go
ChangeWorkspaceUserRole(emailids interface{}, role string, config map[string]interface{}) (serverexception *ServerException)
```

Change users role in the specified workspace.

| Parameter | Description |
|---|---|
| `emailids` | The email address of the users to be modified. |
| `role` | New role of the users. |
| `config` | Contains any additional control configurations. |

### ChangeWorkspaceUserStatus

```go
ChangeWorkspaceUserStatus(emailids interface{}, operation string, config map[string]interface{}) (serverexception *ServerException)
```

Change users staus in the specified workspace.

| Parameter | Description |
|---|---|
| `emailids` | The email address of the users to be modified. |
| `operation` | New status for the users ( Values - activate | deactivate ) |
| `config` | Contains any additional control configurations. |

### Copy

```go
Copy(newworkspacename string, config map[string]interface{}, destorgid string) (newworkspaceid string, serverexception *ServerException)
```

Copy the specified workspace from one organization to another or within the organization.

| Parameter | Description |
|---|---|
| `newworkspacename` | Name of the new workspace. |
| `config` | Contains any additional control configurations. |
| `destorgid` | Id of the organization where the destination workspace is present. |

**Returns** — Returns copied workspace id as string.

### CopyViews

```go
CopyViews(viewids interface{}, destworkspaceid string, config map[string]interface{}, destorgid string) (views interface{}, serverexception *ServerException)
```

Copy the specified views from one workspace to another workspace.

| Parameter | Description |
|---|---|
| `viewids` | The id of the views to be copied. |
| `destworkspaceid` | The destination workspace id. |
| `config` | Contains any additional control configurations. |
| `destorgid` | Id of the organization where the destination workspace is present. |

**Returns** — Returns view list as interface.

### CreateAutoMLAnalysis

```go
CreateAutoMLAnalysis(name string, trainingtableid string, predictiontype string, features []interface{}, serveroption int, algorithms map[string]interface{}, config map[string]interface{},) (analysisid string, serverexception *ServerException)
```

Create a new AutoML analysis within the workspace.

| Parameter | Description |
|---|---|
| `name` | Name of the AutoML analysis. |
| `trainingtableid` | Id of the training table. |
| `predictiontype` | Prediction type (REGRESSION, CLASSIFICATION, CLUSTERING). |
| `features` | List of feature column names. |
| `serveroption` | Compute size option. |
| `algorithms` | Algorithms configuration. |
| `config` | Contains any additional control parameters. |

**Returns** — Returns created AutoML Analysis Id as string.

### CreateAutoMLAnalysisDeployment

```go
CreateAutoMLAnalysisDeployment(analysisid string, modelid string, inputtableid string, outputtable string, outputcolumns []interface{}, predictioncolumn string, serveroption int, importtype string, scheduledetails interface{}, config map[string]interface{},) (deployments interface{}, serverexception *ServerException)
```

Deploy the AutoML analysis model.

| Parameter | Description |
|---|---|
| `analysisid` | Id of the AutoML Analysis. |
| `modelid` | Id of the AutoML Analysis model. |
| `inputtableid` | Id of the input table. |
| `outputtable` | Name of the output table to be created. |
| `outputcolumns` | List of output column names. |
| `predictioncolumn` | Name of the prediction column. |
| `serveroption` | Compute size option. |
| `importtype` | Import type (APPEND, TRUNCATEADD, UPDATEADD). |
| `scheduledetails` | Schedule configuration. |
| `config` | Contains any additional control parameters. |

**Returns** — Returns created AutoML deployment details as interface.

### CreateDashboard

```go
CreateDashboard(displayname string, layout string, config map[string]interface{}) (dashboardid string, serverexception *ServerException)
```

Create a dashboard in the specified workspace.

| Parameter | Description |
|---|---|
| `displayname` | Name of the dashboard. |
| `layout` | Layout configuration of the dashboard. |
| `config` | Contains any additional control configurations. |

**Returns** — Returns the new dashboard id as string.

### CreateEmailSchedule

```go
CreateEmailSchedule(schedulename string, viewids interface{}, format string, emailids interface{}, scheduledetails map[string]interface{}, config map[string]interface{}) (scheduleid string, serverexception *ServerException)
```

Create an email schedule in the specified workspace.

| Parameter | Description |
|---|---|
| `schedulename` | Name of the email schedule. |
| `viewids` | View ids to be mailed. |
| `format` | The format in which the data has to be mailed. |
| `emailids` | The recipients' email addresses for sending views. |
| `scheduledetails` | Contains schedule frequency, date, and time info. |
| `config` | Contains any additional control configurations. |

**Returns** — Returns the created email schedule id.

### CreateFolder

```go
CreateFolder(foldername string, config map[string]interface{}) (folderid string, serverexception *ServerException)
```

Create a folder in the specified workspace.

| Parameter | Description |
|---|---|
| `foldername` | The name of the folder. |
| `config` | Contains any additional control configurations. |

**Returns** — `folderid` (string)

### CreateGroup

```go
CreateGroup(groupname string, emailids interface{}, config map[string]interface{}) (groupid string, serverexception *ServerException)
```

Create a group in the specified workspace.

| Parameter | Description |
|---|---|
| `groupname` | Name of the group. |
| `emailids` | The email address of the users to be added to the group. |
| `config` | Contains any additional control configurations. |

**Returns** — Returns the created group id.

### CreateQueryTable

```go
CreateQueryTable(sqlquery string, querytablename string, config map[string]interface{}) (viewid string, serverexception *ServerException)
```

Create a new query table in the workspace.

| Parameter | Description |
|---|---|
| `sqlquery` | SQL query to construct the query table. |
| `querytablename` | Name of the query table to be created. |
| `config` | Contains the control configurations. |

**Returns** — Returns the newly created view id.

### CreateReport

```go
CreateReport(config map[string]interface{}) (viewid string, serverexception *ServerException)
```

Create a report in the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains the control configurations. |

**Returns** — Created view id.

### CreateSlideshow

```go
CreateSlideshow(slidename string, viewids interface{}, config map[string]interface{}) (slideid string, serverexception *ServerException)
```

Create a slideshow in the specified workspace.

| Parameter | Description |
|---|---|
| `slidename` | Name of the slideshow to be created. |
| `viewids` | Ids of the view to be included in the slideshow. |
| `config` | Contains any additional control configurations. |

**Returns** — Returns the created slideshow id.

### CreateTable

```go
CreateTable(tabledesign map[string]interface{}) (viewid string, serverexception *ServerException)
```

Create a table in the specified workspace.

| Parameter | Description |
|---|---|
| `tabledesign` | Structure of the table to be created. |

**Returns** — Returns created table id.

### CreateTag

```go
CreateTag(tagname, colorcode string, config map[string]interface{}) (tagid string, serverexception *ServerException)
```

Create a tag in the specified workspace.

| Parameter | Description |
|---|---|
| `tagname` | Name of the tag to be created. |
| `colorcode` | Color of the tag in HEX color code. |
| `config` | Contains any additional control configurations. |

**Returns** — Returns the new tag id.

### CreateVariable

```go
CreateVariable(variablename string, variabledatatype int, variabletype int, config map[string]interface{}) (variableid string, serverexception *ServerException)
```

Create a variable in the workspace.

| Parameter | Description |
|---|---|
| `variablename` | Name of the variable to be created. |
| `variabledatatype` | Datatype of the variable to be created. |
| `variabletype` | Type of the variable to be created. |
| `config` | Contains the control configurations. |

**Returns** — Returns the new variable id.

### Delete

```go
Delete() (serverexception *ServerException)
```

Delete a specified workspace in the organization.

### DeleteAlerts

```go
DeleteAlerts(alertids interface{}, config map[string]interface{}) (serverexception *ServerException)
```

Delete the specified data alerts from the workspace.

| Parameter | Description |
|---|---|
| `alertids` | Ids of the data alerts to be deleted. |
| `config` | Contains any additional control configurations. |

### DeleteAutoMLAnalysis

```go
DeleteAutoMLAnalysis(analysisid string, config map[string]interface{}) (serverexception *ServerException)
```

Delete a specified AutoML analysis from the workspace.

| Parameter | Description |
|---|---|
| `analysisid` | Id of the AutoML Analysis. |
| `config` | — |

### DeleteAutoMLAnalysisDeployment

```go
DeleteAutoMLAnalysisDeployment(analysisid string, deploymentid string, config map[string]interface{},) (serverexception *ServerException)
```

Delete an AutoML analysis deployment.

| Parameter | Description |
|---|---|
| `analysisid` | Id of the AutoML Analysis. |
| `deploymentid` | Id of the deployment. |
| `config` | — |

### DeleteAutoMLAnalysisModel

```go
DeleteAutoMLAnalysisModel(analysisid string, modelid string, config map[string]interface{},) (serverexception *ServerException)
```

Delete a specified model from an AutoML analysis.

| Parameter | Description |
|---|---|
| `analysisid` | Id of the AutoML Analysis. |
| `modelid` | Id of the model within the analysis. |
| `config` | — |

### DeleteEmailSchedule

```go
DeleteEmailSchedule(scheduleid string) (serverexception *ServerException)
```

Delete the specified email schedule in the workspace.

| Parameter | Description |
|---|---|
| `scheduleid` | Id for the email schedule. |

### DeleteFolder

```go
DeleteFolder(folderid string) (serverexception *ServerException)
```

Delete a specified folder in the workspace.

| Parameter | Description |
|---|---|
| `folderid` | The id of the folder. |

### DeleteGroup

```go
DeleteGroup(groupid string) (serverexception *ServerException)
```

Delete a specified group.

| Parameter | Description |
|---|---|
| `groupid` | The id of the group. |

### DeleteSlideshow

```go
DeleteSlideshow(slideid string) (serverexception *ServerException)
```

Delete a specified slideshow in the workspace.

| Parameter | Description |
|---|---|
| `slideid` | The id of the slideshow. |

### DeleteTag

```go
DeleteTag(tagid string) (serverexception *ServerException)
```

Delete the specified tag from the workspace.

| Parameter | Description |
|---|---|
| `tagid` | Id of the tag. |

### DeleteTrashView

```go
DeleteTrashView(viewid string, config map[string]interface{}) (serverexception *ServerException)
```

Delete the specified view permanently from trash.

| Parameter | Description |
|---|---|
| `viewid` | Id of the view. |
| `config` | Contains any additional control configurations. |

### DeleteVariable

```go
DeleteVariable(variableid string) (serverexception *ServerException)
```

Delete the specified variable in the workspace.

| Parameter | Description |
|---|---|
| `variableid` | Id of the variable. |

### DeployAutoMLAnalysis

```go
DeployAutoMLAnalysis(analysisid string, deploymentid string, config map[string]interface{},) (serverexception *ServerException)
```

Execute an AutoML analysis deployment.

| Parameter | Description |
|---|---|
| `analysisid` | Id of the AutoML Analysis. |
| `deploymentid` | Id of the deployment. |
| `config` | — |

### DisableDomainAccess

```go
DisableDomainAccess() (serverexception *ServerException)
```

Disable workspace from the specified white label domain.

### DownloadWorkspaceBackup

```go
DownloadWorkspaceBackup(backupid string, filepath string, config map[string]interface{}) (serverexception *ServerException)
```

Download the specified workspace backup.

| Parameter | Description |
|---|---|
| `backupid` | Id of the backup. |
| `filepath` | Path of the file where the downloaded backup is to be stored. |
| `config` | Contains any additional control configurations. |

### EditQueryTable

```go
EditQueryTable(viewid, sqlquery string, config map[string]interface{}) (serverexception *ServerException)
```

Update the mentioned query table in the workspace.

| Parameter | Description |
|---|---|
| `viewid` | Id of the query table to be updated. |
| `sqlquery` | New SQL query to be updated. |
| `config` | Contains any additional control configurations. |

### EnableDomainAccess

```go
EnableDomainAccess() (serverexception *ServerException)
```

Enable workspace to the specified white label domain.

### ExportAsTemplate

```go
ExportAsTemplate(viewids interface{}, filepath string, config map[string]interface{}) (serverexception *ServerException)
```

Export views as templates.

| Parameter | Description |
|---|---|
| `viewids` | View ids to be exported as template. |
| `filepath` | Path of the file where the data exported to be stored. ( Should be in 'atpt' format ) |
| `config` | Contains the control configurations. |

### GetAdmins

```go
GetAdmins() (workspaceadmins interface{}, serverexception *ServerException)
```

Returns list of admins for the specified workspace.

**Returns** — Returns workspace admin list as interface.

### GetAggregateFormulaDependents

```go
GetAggregateFormulaDependents(formulaid string) (dependents interface{}, serverexception *ServerException)
```

Returns list of all dependent views and formulas for the specified aggregate formula.

| Parameter | Description |
|---|---|
| `formulaid` | Id of the aggregate formula. |

**Returns** — Returns dependent list as interface.

### GetAggregateFormulas

```go
GetAggregateFormulas(config map[string]interface{}) (formulas interface{}, serverexception *ServerException)
```

Returns list of all aggregate formulas for the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. |

**Returns** — Aggregate formula list.

### GetAggregateFormulaValue

```go
GetAggregateFormulaValue(formulaid string) (value string, serverexception *ServerException)
```

Returns the value of the aggregate formula.

| Parameter | Description |
|---|---|
| `formulaid` | Id of the aggregate formula. |

**Returns** — Aggregate formula value.

### GetAlertConfiguration

```go
GetAlertConfiguration(alertid string) (alertconfig interface{}, serverexception *ServerException)
```

Returns the configuration of the specified data alert.

| Parameter | Description |
|---|---|
| `alertid` | Id of the data alert. |

**Returns** — Returns the data alert configuration as interface.

### GetAlertEvents

```go
GetAlertEvents(alertid string, config map[string]interface{}) (alertevents interface{}, serverexception *ServerException)
```

Returns the execution events of the specified data alert.

| Parameter | Description |
|---|---|
| `alertid` | Id of the data alert. |
| `config` | Contains any additional control configurations. |

**Returns** — Returns the data alert events along with the page details as interface.

### GetAlertsInWorkspace

```go
GetAlertsInWorkspace() (alerts interface{}, serverexception *ServerException)
```

Returns list of data alerts available in the specified workspace.

**Returns** — Returns the data alerts list as interface.

### GetAutoMLAnalysis

```go
GetAutoMLAnalysis() (analysis interface{}, serverexception *ServerException)
```

Returns list of automl analysis for the specified workspace.

**Returns** — Returns AutoML analysis list as interface.

### GetAutoMLAnalysisDetails

```go
GetAutoMLAnalysisDetails(analysisid string) (details interface{}, serverexception *ServerException)
```

Retrieve detailed information for a specific AutoML analysis.

| Parameter | Description |
|---|---|
| `analysisid` | Id of the AutoML Analysis. |

**Returns** — Returns AutoML analysis details as interface.

### GetDashboardMetadata

```go
GetDashboardMetadata(dashboardid string, config map[string]interface{}) (dashboardconfig interface{}, serverexception *ServerException)
```

Returns the metadata of the specified dashboard.

| Parameter | Description |
|---|---|
| `dashboardid` | Id of the dashboard. |
| `config` | Contains any additional control configurations. |

**Returns** — Returns the dashboard configuration as interface.

### GetDatasources

```go
GetDatasources() (datasourcelist interface{}, serverexception *ServerException)
```

Returns list of datasources for the specified workspace.

**Returns** — Returns Datasource list as interface.

### GetDeploymentDetails

```go
GetDeploymentDetails(analysisid, modelid string) (deployments interface{}, serverexception *ServerException)
```

Returns deployment details available for an AutoML analysis model.

| Parameter | Description |
|---|---|
| `analysisid` | Id of the AutoML Analysis. |
| `modelid` | Id of the AutoML Analysis Model. |

**Returns** — Returns deployment details as interface.

### GetEmailSchedules

```go
GetEmailSchedules() (emailschedules interface{}, serverexception *ServerException)
```

**Returns** — List of email schedules.

### GetFolders

```go
GetFolders() (folders interface{}, serverexception *ServerException)
```

Returns list of all accessible folders for the specified workspace.

**Returns** — Returns folder list as interface.

### GetGroupDetails

```go
GetGroupDetails(groupid string) (groupinfo interface{}, serverexception *ServerException)
```

Returns details of the specified group.

| Parameter | Description |
|---|---|
| `groupid` | The id of the group. |

**Returns** — Returns group detail as interface.

### GetGroups

```go
GetGroups() (groups interface{}, serverexception *ServerException)
```

Returns list of groups for the specified workspace.

**Returns** — Returns the list of groups as interface.

### GetLinkableWorkspaces

```go
GetLinkableWorkspaces() (orgs interface{}, serverexception *ServerException)
```

Returns list of organizations and workspaces that can be linked to the specified master workspace.

**Returns** — Returns the organizations with their linkable workspaces as interface.

### GetLinkedWorkspaces

```go
GetLinkedWorkspaces() (linkedworkspaces interface{}, serverexception *ServerException)
```

Returns list of workspaces linked to the specified master workspace.

**Returns** — Returns the linked workspaces list as interface.

### GetLinkedWorkspaceSyncDetails

```go
GetLinkedWorkspaceSyncDetails(sandboxids interface{}, config map[string]interface{}) (workspaces interface{}, serverexception *ServerException)
```

Returns the sync details of the specified linked workspaces.

| Parameter | Description |
|---|---|
| `sandboxids` | Ids of the linked workspaces for which the sync details are fetched. |
| `config` | Contains any additional control configurations. |

**Returns** — Returns the linked workspace sync details as interface.

### GetQueryTableDetails

```go
GetQueryTableDetails(querytableid string) (details interface{}, serverexception *ServerException)
```

Returns details of the specified query table.

| Parameter | Description |
|---|---|
| `querytableid` | Id of the query table. |

**Returns** — Returns query table details as interface.

### GetQueryTables

```go
GetQueryTables(config map[string]interface{}) (querytables interface{}, serverexception *ServerException)
```

Returns list of all query tables for the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. |

**Returns** — Returns query table list as interface.

### GetReportMetadata

```go
GetReportMetadata(viewid string) (reportconfig interface{}, serverexception *ServerException)
```

Returns the metadata of the specified report.

| Parameter | Description |
|---|---|
| `viewid` | Id of the report. |

**Returns** — Returns the report configuration as interface.

### GetSecretKey

```go
GetSecretKey(config map[string]interface{}) (secretkey string, serverexception *ServerException)
```

Returns the secret key of the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. |

**Returns** — Returns workspace secret key.

### GetSharedDetailsForViews

```go
GetSharedDetailsForViews(viewids interface{}) (shareinfo interface{}, serverexception *ServerException)
```

Returns shared details of the specified views.

| Parameter | Description |
|---|---|
| `viewids` | View ids for which sharing details are required. |

**Returns** — Returns share details as interface.

### GetShareInfo

```go
GetShareInfo() (shareinfo interface{}, serverexception *ServerException)
```

Returns shared details of the specified workspace.

**Returns** — Returns ShareInfo as interface.

### GetSlideshowDetails

```go
GetSlideshowDetails(slideid string) (slideinfo interface{}, serverexception *ServerException)
```

Returns details of the specified slideshow.

| Parameter | Description |
|---|---|
| `slideid` | The id of the slideshow. |

**Returns** — Returns the slideshow details as interface.

### GetSlideshows

```go
GetSlideshows() (slideshows interface{}, serverexception *ServerException)
```

Create a group in the specified workspace.

**Returns** — Returns the list of slideshows as interface.

### GetSlideshowUrl

```go
GetSlideshowUrl(slideid string, config map[string]interface{}) (slideurl string, serverexception *ServerException)
```

Returns slide URL to access the specified slideshow.

| Parameter | Description |
|---|---|
| `slideid` | The id of the slideshow. |
| `config` | Contains the control configurations. |

**Returns** — Returns the slideshow URL.

### GetTaggedViews

```go
GetTaggedViews(tagid string) (views interface{}, serverexception *ServerException)
```

Returns the list of views associated with the specified tag.

| Parameter | Description |
|---|---|
| `tagid` | Id of the tag. |

**Returns** — Returns view list as interface.

### GetTags

```go
GetTags() (tags interface{}, serverexception *ServerException)
```

Returns list of all tags for the specified workspace.

**Returns** — Returns tags list as interface.

### GetTrashViews

```go
GetTrashViews() (views interface{}, serverexception *ServerException)
```

**Returns** — Returns view list as interface.

### GetVariableDetails

```go
GetVariableDetails(variableid string) (variableinfo interface{}, serverexception *ServerException)
```

Returns details of the specified variable.

| Parameter | Description |
|---|---|
| `variableid` | Id of the variable. |

**Returns** — Returns the variable details as interface.

### GetVariables

```go
GetVariables() (variablelist interface{}, serverexception *ServerException)
```

Returns list of variables for the specified workspace.

**Returns** — Returns variable list as interface.

### GetViews

```go
GetViews(config map[string]interface{}) (views interface{}, serverexception *ServerException)
```

Returns list of all accessible views for the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. |

**Returns** — Returns view list as interface.

### GetWorkspaceAccessRestrictions

```go
GetWorkspaceAccessRestrictions() (accessrestrictions interface{}, serverexception *ServerException)
```

Returns the access restriction settings configured for the specified workspace.

**Returns** — Returns the workspace access restriction settings as interface.

### GetWorkspaceBackups

```go
GetWorkspaceBackups() (backups interface{}, serverexception *ServerException)
```

Returns the backup configuration and the list of backups available for the specified workspace.

**Returns** — Returns the workspace backup details as interface.

### GetWorkspaceBackupStatus

```go
GetWorkspaceBackupStatus(backupid string) (backupstatus interface{}, serverexception *ServerException)
```

Returns the status of the specified workspace backup.

| Parameter | Description |
|---|---|
| `backupid` | Id of the backup. |

**Returns** — Returns the backup status details as interface.

### GetWorkspaceLinkingCompatibility

```go
GetWorkspaceLinkingCompatibility(clients interface{}, config map[string]interface{}) (compatibility interface{}, serverexception *ServerException)
```

Returns the linking compatibility details for the specified client workspaces.

| Parameter | Description |
|---|---|
| `clients` | Contains the client workspaces to be verified for linking compatibility. |
| `config` | Contains any additional control configurations. |

**Returns** — Returns the client workspace compatibility details as interface.

### GetWorkspaceRestoreStatus

```go
GetWorkspaceRestoreStatus(restoreid string) (restorestatus interface{}, serverexception *ServerException)
```

Returns the status of the specified workspace restore.

| Parameter | Description |
|---|---|
| `restoreid` | Id of the restore. |

**Returns** — Returns the restore status details as interface.

### GetWorkspaceUsers

```go
GetWorkspaceUsers() (users interface{}, serverexception *ServerException)
```

Returns list of users for the specified workspace.

**Returns** — Returns the list of users as interface.

### LinkWorkspaces

```go
LinkWorkspaces(clients interface{}, config map[string]interface{}) (serverexception *ServerException)
```

Link the specified client workspaces to the master workspace.

| Parameter | Description |
|---|---|
| `clients` | Contains the client workspaces to be linked with the master workspace. |
| `config` | Contains any additional control configurations. |

### MakeDefaultFolder

```go
MakeDefaultFolder(folderid string) (serverexception *ServerException)
```

Make the specified folder as default.

| Parameter | Description |
|---|---|
| `folderid` | Id of the folder. |

### MoveViewsToFolder

```go
MoveViewsToFolder(folderid string, viewids interface{}, config map[string]interface{}) (serverexception *ServerException)
```

Move views to the mentioned folder.

| Parameter | Description |
|---|---|
| `folderid` | Id of the folder. |
| `viewids` | View ids to be moved. |
| `config` | Contains any additional control configurations. |

### RemoveAdmins

```go
RemoveAdmins(emailids interface{}, config map[string]interface{}) (serverexception *ServerException)
```

Remove admins from the specified workspace.

| Parameter | Description |
|---|---|
| `emailids` | The email address of the admin users to be removed. |
| `config` | Contains any additional control configurations. |

### RemoveDefault

```go
RemoveDefault() (serverexception *ServerException)
```

Remove a specified workspace from default.

### RemoveFavorite

```go
RemoveFavorite() (serverexception *ServerException)
```

Remove a specified workspace from favorite.

### RemoveGroupMembers

```go
RemoveGroupMembers(groupid string, emailids interface{}, config map[string]interface{}) (serverexception *ServerException)
```

Remove users from the specified group.

| Parameter | Description |
|---|---|
| `groupid` | The id of the group. |
| `emailids` | The email address of the users to be removed from the group. |
| `config` | Contains any additional control configurations. |

### RemoveShare

```go
RemoveShare(viewids, emailids interface{}, config map[string]interface{}) (serverexception *ServerException)
```

Remove shared views for the specified users.

| Parameter | Description |
|---|---|
| `viewids` | View ids whose sharing needs to be removed. |
| `emailids` | The email address of the users to whom the sharing need to be removed. |
| `config` | Contains any additional control configurations. |

### RemoveTagFromViews

```go
RemoveTagFromViews(tagid string, viewids interface{}, dissociateAll bool, config map[string]interface{}) (serverexception *ServerException)
```

Removes the specified tag from multiple views in the workspace.

| Parameter | Description |
|---|---|
| `tagid` | Id of the tag. |
| `viewids` | View ids to be dissociated. Pass nil when dissociateAll is true. |
| `dissociateAll` | To dissociate the tag from all associated views. |
| `config` | Contains any additional control configurations. |

### RemoveWorkspaceUsers

```go
RemoveWorkspaceUsers(emailids interface{}, config map[string]interface{}) (serverexception *ServerException)
```

Remove users from the specified workspace.

| Parameter | Description |
|---|---|
| `emailids` | The email address of the users to be removed. |
| `config` | Contains any additional control configurations. |

### Rename

```go
Rename(workspacename string, config map[string]interface{}) (serverexception *ServerException)
```

Rename a specified workspace in the organization.

| Parameter | Description |
|---|---|
| `workspacename` | New name of the workspace. |
| `config` | Contains any additional control configurations. |

### RenameFolder

```go
RenameFolder(folderid, folderename string, config map[string]interface{}) (serverexception *ServerException)
```

Rename a specified folder in the workspace.

| Parameter | Description |
|---|---|
| `folderid` | The id of the folder. |
| `folderename` | The new name of the folder. |
| `config` | Contains any additional control configurations. |

### RenameGroup

```go
RenameGroup(groupid, groupname string, config map[string]interface{}) (serverexception *ServerException)
```

Rename a specified group.

| Parameter | Description |
|---|---|
| `groupid` | The id of the group. |
| `groupname` | The new name of the group. |
| `config` | — |

### RestoreTrashView

```go
RestoreTrashView(viewid string, config map[string]interface{}) (serverexception *ServerException)
```

Restore the specified view from trash.

| Parameter | Description |
|---|---|
| `viewid` | Id of the view. |
| `config` | Contains any additional control configurations. |

### RestoreWorkspaceFromBackup

```go
RestoreWorkspaceFromBackup(backupid string, confirmrestore bool, config map[string]interface{}) (restoredetails interface{}, serverexception *ServerException)
```

Restore the specified workspace from the given backup.

| Parameter | Description |
|---|---|
| `backupid` | Id of the backup. |
| `confirmrestore` | Pass true to confirm that the existing workspace data can be overwritten. |
| `config` | Contains any additional control configurations. |

**Returns** — Returns the triggered restore details as interface.

### RunAlert

```go
RunAlert(alertid string, config map[string]interface{}) (serverexception *ServerException)
```

Execute the specified data alert immediately.

| Parameter | Description |
|---|---|
| `alertid` | Id of the data alert. |
| `config` | Contains any additional control configurations. |

### ShareViews

```go
ShareViews(viewids, emailids interface{}, permissions map[string]bool, config map[string]interface{}) (serverexception *ServerException)
```

Share views to the specified users.

| Parameter | Description |
|---|---|
| `viewids` | View ids which to be shared. |
| `emailids` | The email address of the users to whom the views need to be shared. |
| `permissions` | Contains permission details. |
| `config` | Contains any additional control configurations. |

### SyncData

```go
SyncData(datasourceid string, config map[string]interface{}) (serverexception *ServerException)
```

Make the specified folder as default.

| Parameter | Description |
|---|---|
| `datasourceid` | Id of the datasource. |
| `config` | Contains the control configurations. |

### SyncLinkedWorkspaces

```go
SyncLinkedWorkspaces(scope string, config map[string]interface{}) (serverexception *ServerException)
```

Sync the metadata of the master workspace to its linked client workspaces.

| Parameter | Description |
|---|---|
| `scope` | Scope of the sync operation. |
| `config` | Contains any additional control configurations. |

### TriggerEmailSchedule

```go
TriggerEmailSchedule(scheduleid string) (serverexception *ServerException)
```

Trigger configured email schedules instantly.

| Parameter | Description |
|---|---|
| `scheduleid` | Id for the email schedule. |

### UnlinkWorkspaces

```go
UnlinkWorkspaces(scope string, config map[string]interface{}) (serverexception *ServerException)
```

Unlink the client workspaces from the specified master workspace.

| Parameter | Description |
|---|---|
| `scope` | Scope of the unlink operation. |
| `config` | Contains any additional control configurations. |

### UpdateAlert

```go
UpdateAlert(alertid string, alertname string, scheduledetails map[string]interface{}, rules interface{}, config map[string]interface{}) (serverexception *ServerException)
```

Update the specified data alert in the workspace.

| Parameter | Description |
|---|---|
| `alertid` | Id of the data alert. |
| `alertname` | Name of the data alert. |
| `scheduledetails` | Contains the schedule configurations of the data alert. |
| `rules` | Contains the rules to be evaluated by the data alert. |
| `config` | Contains any additional control configurations. |

### UpdateDashboard

```go
UpdateDashboard(dashboardid string, config map[string]interface{}) (serverexception *ServerException)
```

Update the specified dashboard in the workspace.

| Parameter | Description |
|---|---|
| `dashboardid` | Id of the dashboard. |
| `config` | Contains the dashboard configurations to be updated. |

### UpdateDatasourceConnection

```go
UpdateDatasourceConnection(datasourceid string, config map[string]interface{}) (serverexception *ServerException)
```

Update connection details for the specified datasource.

| Parameter | Description |
|---|---|
| `datasourceid` | Id of the datasource. |
| `config` | Contains the control configurations. |

### UpdateEmailSchedule

```go
UpdateEmailSchedule(scheduleid string, config map[string]interface{}) (newscheduleid string, serverexception *ServerException)
```

Update configurations of the specified email schedule in the workspace.

| Parameter | Description |
|---|---|
| `scheduleid` | Id for the email schedule. |
| `config` | Contains the control configurations. |

**Returns** — Returns the updated email schedule id value.

### UpdateReport

```go
UpdateReport(viewid string, config map[string]interface{}) (serverexception *ServerException)
```

Update the design and configuration of the specified report.

| Parameter | Description |
|---|---|
| `viewid` | Id for the view. |
| `config` | Contains the control configurations. |

### UpdateSlideshow

```go
UpdateSlideshow(slideid string, config map[string]interface{}) (serverexception *ServerException)
```

Update details of the specified slideshow.

| Parameter | Description |
|---|---|
| `slideid` | The id of the slideshow. |
| `config` | Contains the control configurations. |

### UpdateTag

```go
UpdateTag(tagid string, config map[string]interface{}) (serverexception *ServerException)
```

Update details of the specified tag in the workspace.

| Parameter | Description |
|---|---|
| `tagid` | Id of the tag. |
| `config` | Contains the control configurations. |

### UpdateVariable

```go
UpdateVariable(variableid string, variablename string, variabledatatype int, variabletype int, config map[string]interface{}) (serverexception *ServerException)
```

Update details of the specified variable in the workspace.

| Parameter | Description |
|---|---|
| `variableid` | Id of the variable. |
| `variablename` | New name for the variable. |
| `variabledatatype` | New datatype for the variable. |
| `variabletype` | New type for the variable. |
| `config` | Contains the control configurations. |

### UpdateWorkspaceAccessRestrictions

```go
UpdateWorkspaceAccessRestrictions(config map[string]interface{}) (serverexception *ServerException)
```

Update the access restriction settings of the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains the access restriction configurations to be updated. |

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
