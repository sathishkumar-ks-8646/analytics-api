# WorkspaceAPI

```java
OrgAPI       org       = ac.getOrgInstance(orgId);
WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
ViewAPI      view      = ac.getViewInstance(orgId, workspaceId, viewId);
BulkAPI      bulk      = ac.getBulkInstance(orgId, workspaceId);
```

`WorkspaceAPI` exposes **117 methods**. Method names are `camelCase`, matching the endpoint title and identifiers are `long`.

## Methods

[`addAdmins`](#addadmins), [`addDefault`](#adddefault), [`addFavorite`](#addfavorite), [`addGroupMembers`](#addgroupmembers), [`addTagToViews`](#addtagtoviews), [`addWorkspaceUsers`](#addworkspaceusers), [`autoMLAnalysisPrediction`](#automlanalysisprediction), [`backupWorkspaceNow`](#backupworkspacenow), [`changeAlertStatus`](#changealertstatus), [`changeEmailScheduleStatus`](#changeemailschedulestatus), [`changeFolderHierarchy`](#changefolderhierarchy), [`changeFolderPosition`](#changefolderposition), [`changeWorkspaceUserRole`](#changeworkspaceuserrole), [`changeWorkspaceUserStatus`](#changeworkspaceuserstatus), [`copy`](#copy), [`copyViews`](#copyviews), [`createAutoMLAnalysis`](#createautomlanalysis), [`createAutoMLAnalysisDeployment`](#createautomlanalysisdeployment), [`createDashboard`](#createdashboard), [`createEmailSchedule`](#createemailschedule), [`createFolder`](#createfolder), [`createGroup`](#creategroup), [`createQueryTable`](#createquerytable), [`createReport`](#createreport), [`createSlideshow`](#createslideshow), [`createTable`](#createtable), [`createTag`](#createtag), [`createVariable`](#createvariable), [`delete`](#delete), [`deleteAlerts`](#deletealerts), [`deleteAutoMLAnalysis`](#deleteautomlanalysis), [`deleteAutoMLAnalysisDeployment`](#deleteautomlanalysisdeployment), [`deleteAutoMLAnalysisModel`](#deleteautomlanalysismodel), [`deleteEmailSchedule`](#deleteemailschedule), [`deleteFolder`](#deletefolder), [`deleteGroup`](#deletegroup), [`deleteSlideshow`](#deleteslideshow), [`deleteTag`](#deletetag), [`deleteTrashView`](#deletetrashview), [`deleteVariable`](#deletevariable), [`deployAutoMLAnalysis`](#deployautomlanalysis), [`disableDomainAccess`](#disabledomainaccess), [`downloadWorkspaceBackup`](#downloadworkspacebackup), [`enableDomainAccess`](#enabledomainaccess), [`exportAsTemplate`](#exportastemplate), [`getAdmins`](#getadmins), [`getAggregateFormulaDependents`](#getaggregateformuladependents), [`getAggregateFormulas`](#getaggregateformulas), [`getAggregateFormulaValue`](#getaggregateformulavalue), [`getAlertConfiguration`](#getalertconfiguration), [`getAlertEvents`](#getalertevents), [`getAlertsInWorkspace`](#getalertsinworkspace), [`getAutoMLAnalysis`](#getautomlanalysis), [`getAutoMLAnalysisDetails`](#getautomlanalysisdetails), [`getDashboardMetadata`](#getdashboardmetadata), [`getDatasources`](#getdatasources), [`getDeploymentDetails`](#getdeploymentdetails), [`getEmailSchedules`](#getemailschedules), [`getFolders`](#getfolders), [`getGroupDetails`](#getgroupdetails), [`getGroups`](#getgroups), [`getLinkableWorkspaces`](#getlinkableworkspaces), [`getLinkedWorkspaces`](#getlinkedworkspaces), [`getLinkedWorkspaceSyncDetails`](#getlinkedworkspacesyncdetails), [`getQueryTableDetails`](#getquerytabledetails), [`getQueryTables`](#getquerytables), [`getReportMetadata`](#getreportmetadata), [`getSecretKey`](#getsecretkey), [`getSharedDetailsForViews`](#getshareddetailsforviews), [`getShareInfo`](#getshareinfo), [`getSlideshowDetails`](#getslideshowdetails), [`getSlideshows`](#getslideshows), [`getSlideshowURL`](#getslideshowurl), [`getTaggedViews`](#gettaggedviews), [`getTags`](#gettags), [`getTrashViews`](#gettrashviews), [`getVariableDetails`](#getvariabledetails), [`getVariables`](#getvariables), [`getViews`](#getviews), [`getWorkspaceAccessRestrictions`](#getworkspaceaccessrestrictions), [`getWorkspaceBackups`](#getworkspacebackups), [`getWorkspaceBackupStatus`](#getworkspacebackupstatus), [`getWorkspaceDetails`](#getworkspacedetails), [`getWorkspaceLinkingCompatibility`](#getworkspacelinkingcompatibility), [`getWorkspaceRestoreStatus`](#getworkspacerestorestatus), [`getWorkspaceUsers`](#getworkspaceusers), [`linkWorkspaces`](#linkworkspaces), [`makeDefaultFolder`](#makedefaultfolder), [`moveViewsToFolder`](#moveviewstofolder), [`removeAdmins`](#removeadmins), [`removeDefault`](#removedefault), [`removeFavorite`](#removefavorite), [`removeGroupMembers`](#removegroupmembers), [`removeShare`](#removeshare), [`removeTagFromViews`](#removetagfromviews), [`removeWorkspaceUsers`](#removeworkspaceusers), [`rename`](#rename), [`renameFolder`](#renamefolder), [`renameGroup`](#renamegroup), [`restoreTrashView`](#restoretrashview), [`restoreWorkspaceFromBackup`](#restoreworkspacefrombackup), [`runAlert`](#runalert), [`shareViews`](#shareviews), [`syncData`](#syncdata), [`syncLinkedWorkspaces`](#synclinkedworkspaces), [`triggerEmailSchedule`](#triggeremailschedule), [`unlinkWorkspaces`](#unlinkworkspaces), [`updateAlert`](#updatealert), [`updateDashboard`](#updatedashboard), [`updateDatasourceConnection`](#updatedatasourceconnection), [`updateEmailSchedule`](#updateemailschedule), [`updateQueryTable`](#updatequerytable), [`updateReport`](#updatereport), [`updateSlideshow`](#updateslideshow), [`updateTag`](#updatetag), [`updateVariable`](#updatevariable), [`updateWorkspaceAccessRestrictions`](#updateworkspaceaccessrestrictions)

### addAdmins

```java
void addAdmins(JSONArray emailIds, JSONObject config)
```

Add admins for the specified workspace.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the admin users to be added. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### addDefault

```java
void addDefault()
```

Adds a specified workspace as default.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### addFavorite

```java
void addFavorite()
```

Adds a specified workspace as favorite.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### addGroupMembers

```java
void addGroupMembers(long groupId, JSONArray emailIds, JSONObject config)
```

Add users to the specified group.

| Parameter | Description |
|---|---|
| `groupId` | The id of the group. |
| `emailIds` | The email address of the users to be added to the group. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### addTagToViews

```java
void addTagToViews(long tagId, JSONArray viewIds, JSONObject config)
```

Adds the specified tag to multiple views in the workspace.

| Parameter | Description |
|---|---|
| `tagId` | Id of the tag. |
| `viewIds` | List of view ids to be associated with the tag. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### addWorkspaceUsers

```java
void addWorkspaceUsers(JSONArray emailIds, String role, JSONObject config)
```

Add users to the specified workspace.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the users to be added. |
| `role` | Role of the users to be added. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### autoMLAnalysisPrediction

```java
JSONObject autoMLAnalysisPrediction(String analysisId, String modelId, JSONObject features, JSONObject config)
```

Generates predictions using a trained AutoML model with sample input values.

| Parameter | Description |
|---|---|
| `analysisId` | Id of the AutoML analysis. |
| `modelId` | Id of the AutoML model. |
| `features` | Feature values for prediction. |
| `config` | Additional control parameters. Can be null. |

**Returns** (`JSONObject`) — Prediction details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### backupWorkspaceNow

```java
JSONObject backupWorkspaceNow(JSONObject config)
```

Trigger an instant backup for the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JSONObject`) — A `JSONObject` of the triggered backup details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### changeAlertStatus

```java
void changeAlertStatus(JSONArray alertIds, boolean enabled, JSONObject config)
```

Enable or disable the specified data alerts in the workspace.

| Parameter | Description |
|---|---|
| `alertIds` | Ids of the data alerts. |
| `enabled` | Pass `true` to enable the data alerts and `false` to disable them. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### changeEmailScheduleStatus

```java
void changeEmailScheduleStatus(long scheduleId, String operation)
```

Update configurations of the specified email schedule in the workspace.

| Parameter | Description |
|---|---|
| `scheduleId` | Id of the email schedule. |
| `operation` | New status for the email schedule ( Values - activate | deactivate ) |

**Returns** (`void`) — A `long` of updatd email schedule id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### changeFolderHierarchy

```java
void changeFolderHierarchy(long folderId, int hierarchy, JSONObject config)
```

Swaps the hierarchy of a parent folder and a subfolder.

| Parameter | Description |
|---|---|
| `folderId` | Id for the folder. |
| `hierarchy` | New hierarchy for the folder. (0 - Parent; 1 - Child) |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### changeFolderPosition

```java
void changeFolderPosition(long folderId, long referenceFolderId, JSONObject config)
```

Place the folder above the reference folder.

| Parameter | Description |
|---|---|
| `folderId` | Id for the folder. |
| `referenceFolderId` | Id of the reference folder. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### changeWorkspaceUserRole

```java
void changeWorkspaceUserRole(JSONArray emailIds, String role, JSONObject config)
```

Change role of the specified users in the workspace.

| Parameter | Description |
|---|---|
| `emailIds` | Email address of the users. |
| `role` | Name of the role. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### changeWorkspaceUserStatus

```java
void changeWorkspaceUserStatus(JSONArray emailIds, String operation, JSONObject config)
```

Change users staus in the specified workspace.

| Parameter | Description |
|---|---|
| `emailIds` | Email address of the users. |
| `operation` | New status for the users ( Values - activate | deactivate ) |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### copy

```java
long copy(String newWorkspaceName, JSONObject config, Long destOrgId)
```

Copy the specified workspace from one organization to another or within the organization.

| Parameter | Description |
|---|---|
| `newWorkspaceName` | Name of the new workspace. |
| `config` | Contains any additional control configurations. Can be null. |
| `destOrgId` | Id of the organization where the destination workspace is present. Can be null. |

**Returns** (`long`) — A `long` of new workspace id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### copyViews

```java
JSONArray copyViews(JSONArray viewIds, long destWorkspaceId, JSONObject config, Long destOrgId)
```

Copy the specified views from one workspace to another workspace.

| Parameter | Description |
|---|---|
| `viewIds` | The id of the views to be copied. |
| `destWorkspaceId` | The destination workspace id. |
| `config` | Contains any additional control configurations. Can be null. |
| `destOrgId` | Id of the organization where the destination workspace is present. Can be null. |

**Returns** (`JSONArray`) — A `JSONArray` of views list.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### createAutoMLAnalysis

```java
String createAutoMLAnalysis(String name, String trainingTableId, String predictionType, JSONArray features, int serverOption, JSONObject algorithms, JSONObject config)
```

Creates a new AutoML analysis in the workspace.

| Parameter | Description |
|---|---|
| `name` | Name of the AutoML analysis. |
| `trainingTableId` | Id of the training table. |
| `predictionType` | Prediction type (REGRESSION / CLASSIFICATION / CLUSTERING). |
| `features` | Feature column names. |
| `serverOption` | Compute size (1 -> 8GB, 2 -> 16GB, 3 -> 32GB). |
| `algorithms` | Algorithms configuration. |
| `config` | Additional control parameters. Can be null. |

**Returns** (`String`) — Created AutoML analysis Id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### createAutoMLAnalysisDeployment

```java
JSONObject createAutoMLAnalysisDeployment(String analysisId, String modelId, String inputTableId, String outputTable, JSONArray outputColumns, String predictionColumn, int serverOption, String importType, Object scheduleDetails, JSONObject config)
```

Creates a deployment for an AutoML analysis model.

| Parameter | Description |
|---|---|
| `analysisId` | Id of the AutoML analysis. |
| `modelId` | Id of the AutoML model. |
| `inputTableId` | Id of the input table. |
| `outputTable` | Name of the output table. |
| `outputColumns` | Columns to be included in the output table. |
| `predictionColumn` | Prediction column name. |
| `serverOption` | Compute size (1 -> 8GB, 2 -> 16GB, 3 -> 32GB). |
| `importType` | Import type (APPEND, TRUNCATEADD, UPDATEADD). |
| `scheduleDetails` | Schedule details. Can be null. |
| `config` | Additional control parameters. Can be null. |

**Returns** (`JSONObject`) — Deployment details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### createDashboard

```java
long createDashboard(String displayName, String layout, JSONObject config)
```

Create a dashboard in the specified workspace.

| Parameter | Description |
|---|---|
| `displayName` | Name of the dashboard. |
| `layout` | Layout configuration of the dashboard. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — A `long` of new dashboard id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### createEmailSchedule

```java
long createEmailSchedule(String scheduleName, JSONArray viewIds, String format, JSONArray emailIds, JSONObject scheduleDetails, JSONObject config)
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

**Returns** (`long`) — A `long` of email schedule id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### createFolder

```java
long createFolder(String folderName, JSONObject config)
```

Create a folder in the specified workspace.

| Parameter | Description |
|---|---|
| `folderName` | The name of the folder. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — A `long` of folder id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### createGroup

```java
String createGroup(String groupName, JSONArray emailIds, JSONObject config)
```

Create a group in the specified workspace.

| Parameter | Description |
|---|---|
| `groupName` | Name of the group. |
| `emailIds` | The email address of the users to be added to the group. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`String`) — A `long` of group id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### createQueryTable

```java
long createQueryTable(String sqlQuery, String queryTableName, JSONObject config)
```

Create a new query table in the workspace.

| Parameter | Description |
|---|---|
| `sqlQuery` | SQL query to construct the query table. |
| `queryTableName` | Name of the query table to be created. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — A `long` of created query table id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### createReport

```java
long createReport(JSONObject config)
```

Create a report in the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains the control configurations. |

**Returns** (`long`) — A `long` of created view id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### createSlideshow

```java
long createSlideshow(String slideName, JSONArray viewIds, JSONObject config)
```

Create a slideshow in the specified workspace.

| Parameter | Description |
|---|---|
| `slideName` | Name of the slideshow to be created. |
| `viewIds` | Ids of the view to be included in the slideshow. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — A `long` of created slideshow id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### createTable

```java
long createTable(JSONObject tableDesign)
```

Create a table in the specified workspace.

| Parameter | Description |
|---|---|
| `tableDesign` | JSON object of table structure. |

**Returns** (`long`) — A `long` of table id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### createTag

```java
long createTag(String tagName, String colorCode, JSONObject config)
```

Create a tag in the specified workspace.

| Parameter | Description |
|---|---|
| `tagName` | Name of the tag to be created. |
| `colorCode` | Color of the tag in HEX color code. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — A `long` of created tag id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### createVariable

```java
long createVariable(String variableName, int variableDataType, int variableType, JSONObject config)
```

Create a variable in the workspace.

| Parameter | Description |
|---|---|
| `variableName` | Name of the variable to be created. |
| `variableDataType` | Datatype of the variable to be created. |
| `variableType` | Type of the variable to be created. |
| `config` | Contains the control configurations. |

**Returns** (`long`) — A `long` of created variable id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### delete

```java
void delete()
```

Delete a specified workspace in the organization.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### deleteAlerts

```java
void deleteAlerts(JSONArray alertIds, JSONObject config)
```

Delete the specified data alerts from the workspace.

| Parameter | Description |
|---|---|
| `alertIds` | Ids of the data alerts to be deleted. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### deleteAutoMLAnalysis

```java
void deleteAutoMLAnalysis(String analysisId, JSONObject config)
```

Deletes a specified AutoML analysis from the workspace.

| Parameter | Description |
|---|---|
| `analysisId` | Id of the AutoML analysis to be deleted. |
| `config` | Additional control parameters. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### deleteAutoMLAnalysisDeployment

```java
void deleteAutoMLAnalysisDeployment(String analysisId, String deploymentId, JSONObject config)
```

Deletes a specific AutoML deployment.

| Parameter | Description |
|---|---|
| `analysisId` | Id of the AutoML analysis. |
| `deploymentId` | Id of the deployment to be deleted. |
| `config` | Additional control parameters. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### deleteAutoMLAnalysisModel

```java
void deleteAutoMLAnalysisModel(String analysisId, String modelId, JSONObject config)
```

Deletes a specified model from an AutoML analysis.

| Parameter | Description |
|---|---|
| `analysisId` | Id of the AutoML analysis. |
| `modelId` | Id of the model to be deleted. |
| `config` | Additional control parameters. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### deleteEmailSchedule

```java
void deleteEmailSchedule(long scheduleId)
```

Delete the specified email schedule in the workspace.

| Parameter | Description |
|---|---|
| `scheduleId` | Id of the email schedule to be deleted. |

**Returns** (`void`) — A `long` of updatd email schedule id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### deleteFolder

```java
void deleteFolder(long folderId)
```

Delete a specified folder in the workspace.

| Parameter | Description |
|---|---|
| `folderId` | The id of the folder. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### deleteGroup

```java
void deleteGroup(long groupId)
```

Delete a specified group.

| Parameter | Description |
|---|---|
| `groupId` | The id of the group. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### deleteSlideshow

```java
void deleteSlideshow(long slideId)
```

Delete a specified slideshow in the workspace.

| Parameter | Description |
|---|---|
| `slideId` | The id of the slideshow. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### deleteTag

```java
void deleteTag(long tagId)
```

Delete the specified tag from the workspace.

| Parameter | Description |
|---|---|
| `tagId` | Id of the tag. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### deleteTrashView

```java
void deleteTrashView(long viewId, JSONObject config)
```

Delete the specified view permanently from trash.

| Parameter | Description |
|---|---|
| `viewId` | Id of the view. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### deleteVariable

```java
void deleteVariable(long variableId)
```

Delete a specified variable in the workspace.

| Parameter | Description |
|---|---|
| `variableId` | Id of the variable. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### deployAutoMLAnalysis

```java
void deployAutoMLAnalysis(String analysisId, String deploymentId, JSONObject config)
```

Executes a specific AutoML deployment.

| Parameter | Description |
|---|---|
| `analysisId` | Id of the AutoML analysis. |
| `deploymentId` | Id of the deployment to be executed. |
| `config` | Additional control parameters. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### disableDomainAccess

```java
void disableDomainAccess()
```

Disable workspace from the specified white label domain.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### downloadWorkspaceBackup

```java
void downloadWorkspaceBackup(long backupId, String filePath, JSONObject config)
```

Download the specified workspace backup.

| Parameter | Description |
|---|---|
| `backupId` | Id of the backup. |
| `filePath` | Path of the file where the downloaded backup is to be stored. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### enableDomainAccess

```java
void enableDomainAccess()
```

Enable workspace to the specified white label domain.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### exportAsTemplate

```java
void exportAsTemplate(JSONArray viewIds, String filePath, JSONObject config)
```

Export the mentioned views as templates.

| Parameter | Description |
|---|---|
| `viewIds` | Ids of the view to be exported. |
| `filePath` | Path of the file where the data exported to be stored. ( Should be in 'atpt' format ) |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getAdmins

```java
JSONArray getAdmins()
```

Returns list of admins for the specified workspace.

**Returns** (`JSONArray`) — A `JSONArray` of workspace admins.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getAggregateFormulaDependents

```java
JSONObject getAggregateFormulaDependents(long formulaId)
```

Returns list of all dependent views and formulas for the specified aggregate formula.

| Parameter | Description |
|---|---|
| `formulaId` | Id of the aggregate formula. |

**Returns** (`JSONObject`) — A `JSONObject` of dependent views and formulas.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getAggregateFormulas

```java
JSONArray getAggregateFormulas(JSONObject config)
```

Returns list of all aggregate formulas for the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JSONArray`) — A `JSONArray` of aggregate formulas.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getAggregateFormulaValue

```java
String getAggregateFormulaValue(long formulaId)
```

Returns the value of the aggregate formula.

| Parameter | Description |
|---|---|
| `formulaId` | Id of the aggregate formula. |

**Returns** (`String`) — A `String` contains aggregate formula value.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getAlertConfiguration

```java
JSONObject getAlertConfiguration(long alertId)
```

Returns the configuration of the specified data alert.

| Parameter | Description |
|---|---|
| `alertId` | Id of the data alert. |

**Returns** (`JSONObject`) — A `JSONObject` of data alert configuration.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getAlertEvents

```java
JSONObject getAlertEvents(long alertId, JSONObject config)
```

Returns the execution events of the specified data alert.

| Parameter | Description |
|---|---|
| `alertId` | Id of the data alert. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JSONObject`) — A `JSONObject` of data alert events along with the page details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getAlertsInWorkspace

```java
JSONArray getAlertsInWorkspace()
```

Returns list of data alerts available in the specified workspace.

**Returns** (`JSONArray`) — A `JSONArray` of data alerts.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getAutoMLAnalysis

```java
JSONArray getAutoMLAnalysis()
```

Returns list of AutoML analysis for the specified workspace.

**Returns** (`JSONArray`) — AutoML analysis list.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getAutoMLAnalysisDetails

```java
JSONObject getAutoMLAnalysisDetails(String analysisId)
```

Retrieves detailed information for a specific AutoML analysis.

| Parameter | Description |
|---|---|
| `analysisId` | Id of the AutoML analysis. |

**Returns** (`JSONObject`) — AutoML analysis details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getDashboardMetadata

```java
JSONObject getDashboardMetadata(long dashboardId, JSONObject config)
```

Returns the metadata of the specified dashboard.

| Parameter | Description |
|---|---|
| `dashboardId` | Id of the dashboard. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JSONObject`) — A `JSONObject` of dashboard configuration.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getDatasources

```java
JSONArray getDatasources()
```

Returns list of all datasource for the specified workspace.

**Returns** (`JSONArray`) — A `JSONArray` of datasource list.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getDeploymentDetails

```java
JSONObject getDeploymentDetails(String analysisId, String modelId)
```

Returns deployment details for a specific AutoML analysis model.

| Parameter | Description |
|---|---|
| `analysisId` | Id of the AutoML analysis. |
| `modelId` | Id of the AutoML analysis model. |

**Returns** (`JSONObject`) — Deployment details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getEmailSchedules

```java
JSONArray getEmailSchedules()
```

Returns list of email schedules available in the specified workspace.

**Returns** (`JSONArray`) — A `JSONArray` of emailschedules.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getFolders

```java
JSONArray getFolders()
```

Returns list of all accessible folders for the specified workspace.

**Returns** (`JSONArray`) — A `JSONArray` of folders list.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getGroupDetails

```java
JSONObject getGroupDetails(long groupId)
```

Returns details of the specified group.

| Parameter | Description |
|---|---|
| `groupId` | The id of the group. |

**Returns** (`JSONObject`) — A `JSONObject` of group details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getGroups

```java
JSONArray getGroups()
```

Returns list of groups for the specified workspace.

**Returns** (`JSONArray`) — A `JSONArray` of groups list.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getLinkableWorkspaces

```java
JSONArray getLinkableWorkspaces()
```

Returns list of organizations and workspaces that can be linked to the specified master workspace.

**Returns** (`JSONArray`) — A `JSONArray` of organizations with their linkable workspaces.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getLinkedWorkspaces

```java
JSONArray getLinkedWorkspaces()
```

Returns list of workspaces linked to the specified master workspace.

**Returns** (`JSONArray`) — A `JSONArray` of linked workspaces.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getLinkedWorkspaceSyncDetails

```java
JSONArray getLinkedWorkspaceSyncDetails(JSONArray sandboxIds, JSONObject config)
```

Returns the sync details of the specified linked workspaces.

| Parameter | Description |
|---|---|
| `sandboxIds` | Ids of the linked workspaces for which the sync details are fetched. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JSONArray`) — A `JSONArray` of linked workspace sync details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getQueryTableDetails

```java
JSONObject getQueryTableDetails(String queryTableId)
```

Returns details of the specified query table.

| Parameter | Description |
|---|---|
| `queryTableId` | Id of the query table. |

**Returns** (`JSONObject`) — Query table details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getQueryTables

```java
JSONArray getQueryTables(JSONObject config)
```

Returns list of all query tables for the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JSONArray`) — A `JSONArray` of query tables.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getReportMetadata

```java
JSONObject getReportMetadata(long viewId)
```

Returns the metadata of the specified report.

| Parameter | Description |
|---|---|
| `viewId` | Id of the report. |

**Returns** (`JSONObject`) — A `JSONObject` of report configuration.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getSecretKey

```java
String getSecretKey(JSONObject config)
```

Returns the secret key of the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`String`) — A `String` of workspace secret key.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getSharedDetailsForViews

```java
JSONArray getSharedDetailsForViews(JSONArray viewIds)
```

Returns shared details of the specified views.

| Parameter | Description |
|---|---|
| `viewIds` | Ids of the view to be included in the slideshow. |

**Returns** (`JSONArray`) — A `JSONArray` of shared info of views.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getShareInfo

```java
ShareInfo getShareInfo()
```

Returns shared details of the specified workspace.

**Returns** (`ShareInfo`) — A `ShareInfo` object.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getSlideshowDetails

```java
JSONObject getSlideshowDetails(long slideId)
```

Returns details of the specified slideshow.

| Parameter | Description |
|---|---|
| `slideId` | The id of the slideshow. |

**Returns** (`JSONObject`) — A `JSONObject` of slideshow details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getSlideshows

```java
JSONArray getSlideshows()
```

Returns list of slideshows for the specified workspace.

**Returns** (`JSONArray`) — A `JSONArray` of slideshows.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getSlideshowURL

```java
String getSlideshowURL(long slideId, JSONObject config)
```

Returns slide URL to access the specified slideshow.

| Parameter | Description |
|---|---|
| `slideId` | The id of the slideshow. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`String`) — A `String` of slideshow URL.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getTaggedViews

```java
JSONArray getTaggedViews(long tagId)
```

Returns the list of views associated with the specified tag.

| Parameter | Description |
|---|---|
| `tagId` | Id of the tag. |

**Returns** (`JSONArray`) — A `JSONArray` of tagged views.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getTags

```java
JSONArray getTags()
```

Returns list of all tags for the specified workspace.

**Returns** (`JSONArray`) — A `JSONArray` of tags list.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getTrashViews

```java
JSONArray getTrashViews()
```

Returns list of all views available in trash for the specified workspace.

**Returns** (`JSONArray`) — A `JSONArray` of trash views.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getVariableDetails

```java
JSONObject getVariableDetails(long variableId)
```

Returns details of the specified variable.

| Parameter | Description |
|---|---|
| `variableId` | The id of the variable. |

**Returns** (`JSONObject`) — A `JSONObject` of variable details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getVariables

```java
JSONArray getVariables()
```

Returns list of all variables for the specified workspace.

**Returns** (`JSONArray`) — A `JSONArray` of variables list.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getViews

```java
JSONArray getViews(JSONObject config)
```

Returns list of all accessible views for the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JSONArray`) — A `JSONArray` of views list.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getWorkspaceAccessRestrictions

```java
JSONObject getWorkspaceAccessRestrictions()
```

Returns the access restriction settings configured for the specified workspace.

**Returns** (`JSONObject`) — A `JSONObject` of workspace access restriction settings.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getWorkspaceBackups

```java
JSONObject getWorkspaceBackups()
```

Returns the backup configuration and the list of backups available for the specified workspace.

**Returns** (`JSONObject`) — A `JSONObject` of workspace backup details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getWorkspaceBackupStatus

```java
JSONObject getWorkspaceBackupStatus(long backupId)
```

Returns the status of the specified workspace backup.

| Parameter | Description |
|---|---|
| `backupId` | Id of the backup. |

**Returns** (`JSONObject`) — A `JSONObject` of backup status details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getWorkspaceDetails

```java
JSONObject getWorkspaceDetails(JSONObject config)
```

Returns details of the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JSONObject`) — A `JSONObject` of workspace details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getWorkspaceLinkingCompatibility

```java
JSONArray getWorkspaceLinkingCompatibility(JSONArray clients, JSONObject config)
```

Returns the linking compatibility details for the specified client workspaces.

| Parameter | Description |
|---|---|
| `clients` | Contains the client workspaces to be verified for linking compatibility. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JSONArray`) — A `JSONArray` of client workspace compatibility details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getWorkspaceRestoreStatus

```java
JSONObject getWorkspaceRestoreStatus(long restoreId)
```

Returns the status of the specified workspace restore.

| Parameter | Description |
|---|---|
| `restoreId` | Id of the restore. |

**Returns** (`JSONObject`) — A `JSONObject` of restore status details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getWorkspaceUsers

```java
JSONArray getWorkspaceUsers()
```

Returns list of users for the specified workspace.

**Returns** (`JSONArray`) — A `JSONArray` of users.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### linkWorkspaces

```java
void linkWorkspaces(JSONArray clients, JSONObject config)
```

Link the specified client workspaces to the master workspace.

| Parameter | Description |
|---|---|
| `clients` | Contains the client workspaces to be linked with the master workspace. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### makeDefaultFolder

```java
void makeDefaultFolder(long folderId)
```

Make the specified folder as default.

| Parameter | Description |
|---|---|
| `folderId` | Id of the variable. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### moveViewsToFolder

```java
void moveViewsToFolder(long folderId, JSONArray viewIds, JSONObject config)
```

Move views to the mentioned folder.

| Parameter | Description |
|---|---|
| `folderId` | Id for the folder. |
| `viewIds` | Ids of the views to be moved. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### removeAdmins

```java
void removeAdmins(JSONArray emailIds, JSONObject config)
```

Remove admins from the specified workspace.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the admin users to be removed. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### removeDefault

```java
void removeDefault()
```

Remove a specified workspace from default.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### removeFavorite

```java
void removeFavorite()
```

Remove a specified workspace from favorite.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### removeGroupMembers

```java
void removeGroupMembers(long groupId, JSONArray emailIds, JSONObject config)
```

Remove users from the specified group.

| Parameter | Description |
|---|---|
| `groupId` | The id of the group. |
| `emailIds` | The email address of the users to be removed from the group. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### removeShare

```java
void removeShare(JSONArray viewIds, JSONArray emailIds, JSONObject config)
```

Remove shared views for the specified users.

| Parameter | Description |
|---|---|
| `viewIds` | View ids whose sharing needs to be removed. |
| `emailIds` | The email address of the users to whom the sharing need to be removed. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### removeTagFromViews

```java
void removeTagFromViews(long tagId, JSONArray viewIds, boolean dissociateAll, JSONObject config)
```

Removes the specified tag from multiple views in the workspace.

| Parameter | Description |
|---|---|
| `tagId` | Id of the tag. |
| `viewIds` | List of view ids to be dissociated. Can be null when dissociateAll is true. |
| `dissociateAll` | To dissociate the tag from all associated views. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### removeWorkspaceUsers

```java
void removeWorkspaceUsers(JSONArray emailIds, JSONObject config)
```

Remove users from the specified workspace.

| Parameter | Description |
|---|---|
| `emailIds` | The email address of the users to be removed. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### rename

```java
void rename(String workspaceName, JSONObject config)
```

Rename a specified workspace in the organization.

| Parameter | Description |
|---|---|
| `workspaceName` | New name of the workspace. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### renameFolder

```java
void renameFolder(long folderId, String folderName, JSONObject config)
```

Rename a specified folder in the workspace.

| Parameter | Description |
|---|---|
| `folderId` | The id of the folder. |
| `folderName` | The new name of the folder. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### renameGroup

```java
void renameGroup(long groupId, String groupName, JSONObject config)
```

Rename a specified group.

| Parameter | Description |
|---|---|
| `groupId` | The id of the group. |
| `groupName` | The new name of the group. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### restoreTrashView

```java
void restoreTrashView(long viewId, JSONObject config)
```

Restore the specified view from trash.

| Parameter | Description |
|---|---|
| `viewId` | Id of the view. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### restoreWorkspaceFromBackup

```java
JSONObject restoreWorkspaceFromBackup(long backupId, boolean confirmRestore, JSONObject config)
```

Restore the specified workspace from the given backup.

| Parameter | Description |
|---|---|
| `backupId` | Id of the backup. |
| `confirmRestore` | Pass `true` to confirm that the existing workspace data can be overwritten. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JSONObject`) — A `JSONObject` of the triggered restore details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### runAlert

```java
void runAlert(long alertId, JSONObject config)
```

Execute the specified data alert immediately.

| Parameter | Description |
|---|---|
| `alertId` | Id of the data alert. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### shareViews

```java
void shareViews(JSONArray viewIds, JSONArray emailIds, JSONObject permissions, JSONObject config)
```

Share views to the specified users.

| Parameter | Description |
|---|---|
| `viewIds` | View ids which to be shared. |
| `emailIds` | The email address of the users to whom the views need to be shared. |
| `permissions` | Contains permission details. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### syncData

```java
void syncData(long datasourceId, JSONObject config)
```

Initiate data sync for the specified datasource.

| Parameter | Description |
|---|---|
| `datasourceId` | Id for the datasource. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### syncLinkedWorkspaces

```java
void syncLinkedWorkspaces(String scope, JSONObject config)
```

Sync the metadata of the master workspace to its linked client workspaces.

| Parameter | Description |
|---|---|
| `scope` | Scope of the sync operation. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### triggerEmailSchedule

```java
void triggerEmailSchedule(long scheduleId)
```

Trigger configured email schedules instantly.

| Parameter | Description |
|---|---|
| `scheduleId` | Id of the email schedule. |

**Returns** (`void`) — A `long` of updatd email schedule id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### unlinkWorkspaces

```java
void unlinkWorkspaces(String scope, JSONObject config)
```

Unlink the client workspaces from the specified master workspace.

| Parameter | Description |
|---|---|
| `scope` | Scope of the unlink operation. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### updateAlert

```java
void updateAlert(long alertId, String alertName, JSONObject scheduleDetails, JSONArray rules, JSONObject config)
```

Update the specified data alert in the workspace.

| Parameter | Description |
|---|---|
| `alertId` | Id of the data alert. |
| `alertName` | Name of the data alert. |
| `scheduleDetails` | Contains the schedule configurations of the data alert. |
| `rules` | Contains the rules to be evaluated by the data alert. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### updateDashboard

```java
void updateDashboard(long dashboardId, JSONObject config)
```

Update the specified dashboard in the workspace.

| Parameter | Description |
|---|---|
| `dashboardId` | Id of the dashboard. |
| `config` | Contains the dashboard configurations to be updated. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### updateDatasourceConnection

```java
void updateDatasourceConnection(long datasourceId, JSONObject config)
```

Update connection details for the specified datasource.

| Parameter | Description |
|---|---|
| `datasourceId` | Id of the datasource. |
| `config` | Contains the control configurations. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### updateEmailSchedule

```java
long updateEmailSchedule(long scheduleId, JSONObject config)
```

Update configurations of the specified email schedule in the workspace.

| Parameter | Description |
|---|---|
| `scheduleId` | Id of the email schedule. |
| `config` | Contains the control configurations. |

**Returns** (`long`) — A `long` of updatd email schedule id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### updateQueryTable

```java
void updateQueryTable(long viewId, String sqlQuery, JSONObject config)
```

Update the mentioned query table in the workspace.

| Parameter | Description |
|---|---|
| `viewId` | Id of the query table to be updated. |
| `sqlQuery` | New SQL query to be updated. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### updateReport

```java
void updateReport(long viewId, JSONObject config)
```

Update the design and configuration of the specified report.

| Parameter | Description |
|---|---|
| `viewId` | Id of the view. |
| `config` | Contains the control configurations. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### updateSlideshow

```java
void updateSlideshow(long slideId, JSONObject config)
```

Update details of the specified slideshow.

| Parameter | Description |
|---|---|
| `slideId` | The id of the slideshow. |
| `config` | Contains the control configurations. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### updateTag

```java
void updateTag(long tagId, JSONObject config)
```

Update details of the specified tag in the workspace.

| Parameter | Description |
|---|---|
| `tagId` | Id of the tag. |
| `config` | Contains the control configurations. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### updateVariable

```java
void updateVariable(long variableId, String variableName, int variableDataType, int variableType, JSONObject config)
```

Update details of the specified variable in the workspace.

| Parameter | Description |
|---|---|
| `variableId` | Id for the variable. |
| `variableName` | Name of the variable to be created. |
| `variableDataType` | Datatype of the variable to be created. |
| `variableType` | Type of the variable to be created. |
| `config` | Contains the control configurations. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### updateWorkspaceAccessRestrictions

```java
void updateWorkspaceAccessRestrictions(JSONObject config)
```

Update the access restriction settings of the specified workspace.

| Parameter | Description |
|---|---|
| `config` | Contains the access restriction configurations to be updated. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
