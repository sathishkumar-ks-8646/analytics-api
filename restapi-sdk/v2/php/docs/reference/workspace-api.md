# WorkspaceAPI

```php
$org       = $ac->getOrgInstance($org_id);
$workspace = $ac->getWorkspaceInstance($org_id, $workspace_id);
$view      = $ac->getViewInstance($org_id, $workspace_id, $view_id);
$bulk      = $ac->getBulkInstance($org_id, $workspace_id);
```

`WorkspaceAPI` exposes **116 methods**. Method names are `camelCase` and identifiers are `string`.

## Methods

[`addAdmins`](#addadmins), [`addDefault`](#adddefault), [`addFavorite`](#addfavorite), [`addGroupMembers`](#addgroupmembers), [`addTagToViews`](#addtagtoviews), [`addWorkspaceUsers`](#addworkspaceusers), [`autoMLAnalysisPrediction`](#automlanalysisprediction), [`backupWorkspaceNow`](#backupworkspacenow), [`changeAlertStatus`](#changealertstatus), [`changeEmailScheduleStatus`](#changeemailschedulestatus), [`changeFolderHierarchy`](#changefolderhierarchy), [`changeFolderPosition`](#changefolderposition), [`changeWorkspaceUserRole`](#changeworkspaceuserrole), [`changeWorkspaceUserStatus`](#changeworkspaceuserstatus), [`copy`](#copy), [`copyViews`](#copyviews), [`createAutoMLAnalysis`](#createautomlanalysis), [`createAutoMLAnalysisDeployment`](#createautomlanalysisdeployment), [`createDashboard`](#createdashboard), [`createEmailSchedule`](#createemailschedule), [`createFolder`](#createfolder), [`createGroup`](#creategroup), [`createQueryTable`](#createquerytable), [`createReport`](#createreport), [`createSlideshow`](#createslideshow), [`createTable`](#createtable), [`createTag`](#createtag), [`createVariable`](#createvariable), [`delete`](#delete), [`deleteAlerts`](#deletealerts), [`deleteAutoMLAnalysis`](#deleteautomlanalysis), [`deleteAutoMLAnalysisDeployment`](#deleteautomlanalysisdeployment), [`deleteAutoMLAnalysisModel`](#deleteautomlanalysismodel), [`deleteEmailSchedule`](#deleteemailschedule), [`deleteFolder`](#deletefolder), [`deleteGroup`](#deletegroup), [`deleteSlideshow`](#deleteslideshow), [`deleteTag`](#deletetag), [`deleteTrashView`](#deletetrashview), [`deleteVariable`](#deletevariable), [`deployAutoMLAnalysis`](#deployautomlanalysis), [`disableDomainAccess`](#disabledomainaccess), [`downloadWorkspaceBackup`](#downloadworkspacebackup), [`editQueryTable`](#editquerytable), [`enableDomainAccess`](#enabledomainaccess), [`exportAsTemplate`](#exportastemplate), [`getAdmins`](#getadmins), [`getAggregateFormulaDependents`](#getaggregateformuladependents), [`getAggregateFormulas`](#getaggregateformulas), [`getAggregateFormulaValue`](#getaggregateformulavalue), [`getAlertConfiguration`](#getalertconfiguration), [`getAlertEvents`](#getalertevents), [`getAlertsInWorkspace`](#getalertsinworkspace), [`getAutoMLAnalysis`](#getautomlanalysis), [`getAutoMLAnalysisDetails`](#getautomlanalysisdetails), [`getDashboardMetadata`](#getdashboardmetadata), [`getDatasources`](#getdatasources), [`getDeploymentDetails`](#getdeploymentdetails), [`getEmailSchedules`](#getemailschedules), [`getFolders`](#getfolders), [`getGroupDetails`](#getgroupdetails), [`getGroups`](#getgroups), [`getLinkableWorkspaces`](#getlinkableworkspaces), [`getLinkedWorkspaces`](#getlinkedworkspaces), [`getLinkedWorkspaceSyncDetails`](#getlinkedworkspacesyncdetails), [`getQueryTableDetails`](#getquerytabledetails), [`getQueryTables`](#getquerytables), [`getReportMetadata`](#getreportmetadata), [`getSecretKey`](#getsecretkey), [`getSharedDetailsForViews`](#getshareddetailsforviews), [`getShareInfo`](#getshareinfo), [`getSlideshowDetails`](#getslideshowdetails), [`getSlideshows`](#getslideshows), [`getSlideshowUrl`](#getslideshowurl), [`getTaggedViews`](#gettaggedviews), [`getTags`](#gettags), [`getTrashViews`](#gettrashviews), [`getVariableDetails`](#getvariabledetails), [`getVariables`](#getvariables), [`getViews`](#getviews), [`getWorkspaceAccessRestrictions`](#getworkspaceaccessrestrictions), [`getWorkspaceBackups`](#getworkspacebackups), [`getWorkspaceBackupStatus`](#getworkspacebackupstatus), [`getWorkspaceLinkingCompatibility`](#getworkspacelinkingcompatibility), [`getWorkspaceRestoreStatus`](#getworkspacerestorestatus), [`getWorkspaceUsers`](#getworkspaceusers), [`linkWorkspaces`](#linkworkspaces), [`makeDefaultFolder`](#makedefaultfolder), [`moveViewsToFolder`](#moveviewstofolder), [`removeAdmins`](#removeadmins), [`removeDefault`](#removedefault), [`removeFavorite`](#removefavorite), [`removeGroupMembers`](#removegroupmembers), [`removeShare`](#removeshare), [`removeTagFromViews`](#removetagfromviews), [`removeWorkspaceUsers`](#removeworkspaceusers), [`rename`](#rename), [`renameFolder`](#renamefolder), [`renameGroup`](#renamegroup), [`restoreTrashView`](#restoretrashview), [`restoreWorkspaceFromBackup`](#restoreworkspacefrombackup), [`runAlert`](#runalert), [`shareViews`](#shareviews), [`syncData`](#syncdata), [`syncLinkedWorkspaces`](#synclinkedworkspaces), [`triggerEmailSchedule`](#triggeremailschedule), [`unlinkWorkspaces`](#unlinkworkspaces), [`updateAlert`](#updatealert), [`updateDashboard`](#updatedashboard), [`updateDatasourceConnection`](#updatedatasourceconnection), [`updateEmailSchedule`](#updateemailschedule), [`updateReport`](#updatereport), [`updateSlideshow`](#updateslideshow), [`updateTag`](#updatetag), [`updateVariable`](#updatevariable), [`updateWorkspaceAccessRestrictions`](#updateworkspaceaccessrestrictions)

### addAdmins

```php
addAdmins($email_ids, $config = array()
```

Add admins for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `array()` | The email address of the admin users to be added. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### addDefault

```php
addDefault()
```

Adds a specified workspace as default.

**Raises** — `IOException`; `ServerException`; `ParseException`

### addFavorite

```php
addFavorite()
```

Adds a specified workspace as favorite.

**Raises** — `IOException`; `ServerException`; `ParseException`

### addGroupMembers

```php
addGroupMembers($group_id, $email_ids, $config = array()
```

Add users to the specified group.

| Parameter | Type | Description |
|---|---|---|
| `group_id` | `string` | Id of the group. |
| `email_ids` | `array()` | The email address of the users to be added to the group. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### addTagToViews

```php
addTagToViews($tag_id, $view_ids, $config = array()
```

Adds the specified tag to multiple views in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `tag_id` | `string` | Id of the tag. |
| `view_ids` | `array()` | View ids to be associated with the tag. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

### addWorkspaceUsers

```php
addWorkspaceUsers($email_ids, $role, $config = array()
```

Add users to the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `array()` | The email address of the users to be added. |
| `role` | `string` | Role of the user to be added. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### autoMLAnalysisPrediction

```php
autoMLAnalysisPrediction($analysis_id, $model_id, $features, $config = array()
```

Generate predictions using a trained AutoML model.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `string` | Id of the AutoML analysis. |
| `model_id` | `string` | Id of the AutoML model. |
| `features` | `array` | Feature-value mapping. |
| `config` | `array` | Optional control parameters. |

**Returns** — Prediction result.

**Raises** — `IOException`; `ServerException`; `ParseException`

### backupWorkspaceNow

```php
backupWorkspaceNow($config = array()
```

Trigger an instant backup for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Triggered backup details.

### changeAlertStatus

```php
changeAlertStatus($alert_ids, $enabled, $config = array()
```

Enable or disable the specified data alerts in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `alert_ids` | `array()` | Ids of the data alerts. |
| `enabled` | `boolean` | Pass true to enable the data alerts and false to disable them. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

### changeEmailScheduleStatus

```php
changeEmailScheduleStatus($schedule_id, $operation)
```

Update email schedule status.

| Parameter | Type | Description |
|---|---|---|
| `schedule_id` | `string` | Id for the email schedule. |
| `operation` | `string` | New status for the schedule (Values - activate | deactivate). |

**Raises** — `IOException`; `ServerException`; `ParseException`

### changeFolderHierarchy

```php
changeFolderHierarchy($folder_id, $hierarchy, $config = array()
```

Swaps the hierarchy of a parent folder and a subfolder.

| Parameter | Type | Description |
|---|---|---|
| `folder_id` | `string` | Id of the folder. |
| `hierarchy` | `int` | New hierarchy for the folder. (0 - Parent; 1 - Child) |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### changeFolderPosition

```php
changeFolderPosition($folder_id, $reference_folder_id, $config = array()
```

Place the folder above the reference folder.

| Parameter | Type | Description |
|---|---|---|
| `folder_id` | `string` | Id of the folder. |
| `reference_folder_id` | `string` | Id of the reference folder. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### changeWorkspaceUserRole

```php
changeWorkspaceUserRole($email_ids, $role, $config = array()
```

Change role of the specified users in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `array()` | The email address of the users. |
| `role` | `string` | Name of the role. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### changeWorkspaceUserStatus

```php
changeWorkspaceUserStatus($email_ids, $operation, $config = array()
```

Change users staus in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `array()` | The email address of the users. |
| `operation` | `string` | New status for the users ( Values - activate | deactivate ) |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### copy

```php
copy($new_workspace_name, $config = array()
```

Copy the specified workspace from one organization to another or within the organization.

| Parameter | Type | Description |
|---|---|---|
| `new_workspace_name` | `string` | Name of the new workspace. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |
| `dest_org_id` | `string` | Id of the organization where the destination workspace is present. Can be null. |

**Returns** — Copied workspace id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### copyViews

```php
copyViews($view_ids, $dest_workspace_id, $config = array()
```

Copy the specified views from one workspace to another workspace.

| Parameter | Type | Description |
|---|---|---|
| `view_ids` | `array()` | The id of the views to be copied. |
| `dest_workspace_id` | `string` | The destination workspace id. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |
| `dest_org_id` | `string` | Id of the organization where the destination workspace is present. Can be null. |

**Returns** — View list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### createAutoMLAnalysis

```php
createAutoMLAnalysis($name, $training_table_id, $prediction_type, $features, $server_option, $algorithms, $config = array()
```

Creates a new AutoML analysis within the workspace.

| Parameter | Type | Description |
|---|---|---|
| `name` | `string` | Name of the AutoML analysis. |
| `training_table_id` | `string` | Training table ID. |
| `prediction_type` | `string` | Prediction type (REGRESSION | CLASSIFICATION | CLUSTERING). |
| `features` | `array` | Feature column names. |
| `server_option` | `int` | Compute size (1 → 8GB, 2 → 16GB, 3 → 32GB). |
| `algorithms` | `array` | Algorithms configuration. |
| `config` | `array` | Optional configuration parameters. |

**Returns** — Created AutoML analysis ID.

**Raises** — `IOException`; `ServerException`; `ParseException`

### createAutoMLAnalysisDeployment

```php
createAutoMLAnalysisDeployment($analysis_id, $model_id, $input_table_id, $output_table, $output_columns, $prediction_column, $server_option, $import_type, $schedule_details = null, $config = array()
```

Create a deployment for an AutoML analysis model.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `string` | Id of the AutoML analysis. |
| `model_id` | `string` | Id of the AutoML model. |
| `input_table_id` | `string` | Input table ID. |
| `output_table` | `string` | Output table name. |
| `output_columns` | `array` | Columns to include in output table. |
| `prediction_column` | `string` | Prediction column name. |
| `server_option` | `int` | Compute size (1 → 8GB, 2 → 16GB, 3 → 32GB). |
| `import_type` | `string` | Import type (APPEND | TRUNCATEADD | UPDATEADD). |
| `schedule_details` | `array|null` | Schedule configuration. |
| `config` | `array` | Optional control parameters. |

**Returns** — Deployment details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### createDashboard

```php
createDashboard($display_name, $layout, $config = array()
```

Create a dashboard in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `display_name` | `string` | Name of the dashboard. |
| `layout` | `string` | Layout configuration of the dashboard. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Created dashboard id.

### createEmailSchedule

```php
createEmailSchedule($schedule_name, $view_ids, $format, $email_ids, $schedule_details, $config = array()
```

Create an email schedule in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `schedule_name` | `string` | Name of the email schedule. |
| `view_ids` | `array()` | View ids to be mailed. |
| `format` | `string` | The format in which the data has to be mailed. |
| `email_ids` | `array()` | The recipients' email addresses for sending views. |
| `schedule_details` | `array()` | Contains schedule frequency, date, and time info. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Created email schedule id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### createFolder

```php
createFolder($folder_name, $config = array()
```

Create a folder in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `folder_name` | `string` | Name of the folder to be created. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Created folder id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### createGroup

```php
createGroup($group_name, $email_ids, $config = array()
```

Create a group in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `group_name` | `string` | Name of the group. |
| `email_ids` | `array()` | The email address of the users to be added to the group. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Created group id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### createQueryTable

```php
createQueryTable($sql_query, $query_table_name, $config = array()
```

Create a new query table in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `sql_query` | `string` | SQL query to construct the query table. |
| `query_table_name` | `string` | Name of the query table to be created. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Created query table id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### createReport

```php
createReport($config = array()
```

Create a report in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `array()` | Contains the control parameters. |

**Returns** — Created view id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### createSlideshow

```php
createSlideshow($slide_name, $view_ids, $config = array()
```

Create a slideshow in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `slide_name` | `string` | Name of the slideshow. |
| `view_ids` | `array()` | Ids of the view to be included in the slideshow. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Created slideshow id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### createTable

```php
createTable($table_design)
```

Create a table in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `table_design` | `array()` | Table structure. |

**Returns** — Created table id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### createTag

```php
createTag($tag_name, $color_code, $config = array()
```

Create a tag in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `tag_name` | `string` | Name of the tag to be created. |
| `color_code` | `string` | Color of the tag in HEX color code. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Created tag id.

### createVariable

```php
createVariable($variable_name, $variable_datatype, $variable_type, $config = array()
```

Create a variable in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `variable_name` | `string` | Name of the variable to be created. |
| `variable_datatype` | `string` | Datatype of the variable to be created. |
| `variable_type` | `string` | Type of the variable to be created. |
| `config` | `array()` | Contains the control parameters. |

**Returns** — Created variable id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### delete

```php
delete()
```

Delete a specified workspace in the organization.

**Raises** — `IOException`; `ServerException`; `ParseException`

### deleteAlerts

```php
deleteAlerts($alert_ids, $config = array()
```

Delete the specified data alerts from the workspace.

| Parameter | Type | Description |
|---|---|---|
| `alert_ids` | `array()` | Ids of the data alerts to be deleted. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

### deleteAutoMLAnalysis

```php
deleteAutoMLAnalysis($analysis_id, $config = array()
```

Delete a specified AutoML analysis from the workspace.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `string` | Id of the AutoML analysis. |
| `config` | `array` | Optional control parameters. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### deleteAutoMLAnalysisDeployment

```php
deleteAutoMLAnalysisDeployment($analysis_id, $deployment_id, $config = array()
```

Delete an AutoML analysis deployment.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `string` | Id of the AutoML analysis. |
| `deployment_id` | `string` | Id of the deployment. |
| `config` | `array` | Optional control parameters. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### deleteAutoMLAnalysisModel

```php
deleteAutoMLAnalysisModel($analysis_id, $model_id, $config = array()
```

Delete a specific model from an AutoML analysis.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `string` | Id of the AutoML analysis. |
| `model_id` | `string` | Id of the model to delete. |
| `config` | `array` | Optional control parameters. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### deleteEmailSchedule

```php
deleteEmailSchedule($schedule_id)
```

Delete the specified email schedule in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `schedule_id` | `string` | Id for the email schedule. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### deleteFolder

```php
deleteFolder($folder_id)
```

Delete a specified folder in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `folder_id` | `string` | Id of the folder. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### deleteGroup

```php
deleteGroup($group_id)
```

Delete a specified group.

| Parameter | Type | Description |
|---|---|---|
| `group_id` | `string` | Id of the group. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### deleteSlideshow

```php
deleteSlideshow($slide_id)
```

Delete a specified slideshow in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `slide_id` | `string` | Id of the slideshow. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### deleteTag

```php
deleteTag($tag_id)
```

Delete the specified tag from the workspace.

| Parameter | Type | Description |
|---|---|---|
| `tag_id` | `string` | Id of the tag. |

### deleteTrashView

```php
deleteTrashView($view_id, $config=array()
```

Delete the specified view permanently from trash.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### deleteVariable

```php
deleteVariable($variable_id)
```

Delete the specified variable in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `variable_id` | `string` | Id of the variable. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### deployAutoMLAnalysis

```php
deployAutoMLAnalysis($analysis_id, $deployment_id, $config = array()
```

Execute an AutoML analysis deployment.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `string` | Id of the AutoML analysis. |
| `deployment_id` | `string` | Id of the deployment. |
| `config` | `array` | Optional control parameters. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### disableDomainAccess

```php
disableDomainAccess()
```

Disable workspace from the specified white label domain.

**Raises** — `IOException`; `ServerException`; `ParseException`

### downloadWorkspaceBackup

```php
downloadWorkspaceBackup($backup_id, $file_path, $config = array()
```

Download the specified workspace backup.

| Parameter | Type | Description |
|---|---|---|
| `backup_id` | `string` | Id of the backup. |
| `file_path` | `string` | Path of the file where the downloaded backup is to be stored. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

### editQueryTable

```php
editQueryTable($view_id, $sql_query, $config = array()
```

Update the mentioned query table in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the query table to be updated. |
| `sql_query` | `string` | SQL query to construct the query table. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### enableDomainAccess

```php
enableDomainAccess()
```

Enable workspace to the specified white label domain.

**Raises** — `IOException`; `ServerException`; `ParseException`

### exportAsTemplate

```php
exportAsTemplate($view_ids, $file_path, $config = array()
```

Export the mentioned table (or) view data.

| Parameter | Type | Description |
|---|---|---|
| `view_ids` | `array()` | Ids of the view to be exported. |
| `file_path` | `string` | Path of the file where the data exported to be stored. ( Should be in 'atpt' format ) |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### getAdmins

```php
getAdmins()
```

Returns list of admins for the specified workspace.

**Returns** — Workspace admin list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getAggregateFormulaDependents

```php
getAggregateFormulaDependents($formula_id)
```

Returns list of all dependent views and formulas for the specified aggregate formula.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `string` | Id for the aggregate formula. |

**Returns** — Dependent details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getAggregateFormulas

```php
getAggregateFormulas($config = array()
```

Returns list of all aggregate formulas for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Aggregate formula list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getAggregateFormulaValue

```php
getAggregateFormulaValue($formula_id)
```

Returns the value of the aggregate formula.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `string` | Id for the aggregate formula. |

**Returns** — Aggregate formula value.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getAlertConfiguration

```php
getAlertConfiguration($alert_id)
```

Returns the configuration of the specified data alert.

| Parameter | Type | Description |
|---|---|---|
| `alert_id` | `string` | Id of the data alert. |

**Returns** — Data alert configuration.

### getAlertEvents

```php
getAlertEvents($alert_id, $config = array()
```

Returns the execution events of the specified data alert.

| Parameter | Type | Description |
|---|---|---|
| `alert_id` | `string` | Id of the data alert. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Data alert events along with the page details.

### getAlertsInWorkspace

```php
getAlertsInWorkspace()
```

Returns list of data alerts available in the specified workspace.

**Returns** — Data alerts list.

### getAutoMLAnalysis

```php
getAutoMLAnalysis()
```

Returns list of AutoML analysis for the specified workspace.

**Returns** — List of AutoML analysis.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getAutoMLAnalysisDetails

```php
getAutoMLAnalysisDetails($analysis_id)
```

Retrieve detailed information for a specific AutoML analysis.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `string` | Id of the AutoML analysis. |

**Returns** — AutoML analysis details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getDashboardMetadata

```php
getDashboardMetadata($dashboard_id, $config = array()
```

Returns the metadata of the specified dashboard.

| Parameter | Type | Description |
|---|---|---|
| `dashboard_id` | `string` | Id of the dashboard. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Dashboard configuration.

### getDatasources

```php
getDatasources()
```

Returns list of datasources for the specified workspace.

**Returns** — Datasource list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getDeploymentDetails

```php
getDeploymentDetails($analysis_id, $model_id)
```

Returns deployment details available for an AutoML analysis model.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `string` | Id of the AutoML analysis. |
| `model_id` | `string` | Id of the AutoML model. |

**Returns** — Deployment details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getEmailSchedules

```php
getEmailSchedules()
```

Returns list of email schedules available in the specified workspace.

**Returns** — List of email schedules.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getFolders

```php
getFolders()
```

Returns list of all accessible folders for the specified workspace.

**Returns** — Folder list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getGroupDetails

```php
getGroupDetails($group_id)
```

Get the details of the specified group.

| Parameter | Type | Description |
|---|---|---|
| `group_id` | `string` | Id of the group. |

**Returns** — Details of the specified group.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getGroups

```php
getGroups()
```

Returns list of groups for the specified workspace.

**Returns** — Group list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getLinkableWorkspaces

```php
getLinkableWorkspaces()
```

Returns list of organizations and workspaces that can be linked to the specified master workspace.

**Returns** — Organizations with their linkable workspaces.

### getLinkedWorkspaces

```php
getLinkedWorkspaces()
```

Returns list of workspaces linked to the specified master workspace.

**Returns** — Linked workspaces list.

### getLinkedWorkspaceSyncDetails

```php
getLinkedWorkspaceSyncDetails($sandbox_ids, $config = array()
```

Returns the sync details of the specified linked workspaces.

| Parameter | Type | Description |
|---|---|---|
| `sandbox_ids` | `array()` | Ids of the linked workspaces for which the sync details are fetched. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Linked workspace sync details.

### getQueryTableDetails

```php
getQueryTableDetails($query_table_id)
```

Returns details of the specified query table.

| Parameter | Type | Description |
|---|---|---|
| `query_table_id` | `string` | Id of the query table. |

**Returns** — Query table details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getQueryTables

```php
getQueryTables($config = array()
```

Returns list of all query tables for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Query table list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getReportMetadata

```php
getReportMetadata($view_id)
```

Returns the metadata of the specified report.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the report. |

**Returns** — Report configuration.

### getSecretKey

```php
getSecretKey($config = array()
```

Returns the secret key of the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Workspace secret key.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getSharedDetailsForViews

```php
getSharedDetailsForViews($view_ids)
```

Returns shared details of the specified views.

| Parameter | Type | Description |
|---|---|---|
| `view_ids` | `array()` | View ids for which sharing details are required. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### getShareInfo

```php
getShareInfo()
```

Returns shared details of the specified workspace.

**Returns** — Workspace share info.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getSlideshowDetails

```php
getSlideshowDetails($slide_id)
```

Returns details of the specified slideshow.

| Parameter | Type | Description |
|---|---|---|
| `slide_id` | `string` | Id of the slideshow. |

**Returns** — Slideshow details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getSlideshows

```php
getSlideshows()
```

Returns list of slideshows for the specified workspace.

**Returns** — Slideshow list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getSlideshowUrl

```php
getSlideshowUrl($slide_id, $config = array()
```

Returns slide URL to access the specified slideshow.

| Parameter | Type | Description |
|---|---|---|
| `slide_id` | `string` | Id of the slideshow. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Slideshow URL.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getTaggedViews

```php
getTaggedViews($tag_id)
```

Returns the list of views associated with the specified tag.

| Parameter | Type | Description |
|---|---|---|
| `tag_id` | `string` | Id of the tag. |

**Returns** — Tagged views list.

### getTags

```php
getTags()
```

Returns list of all tags for the specified workspace.

**Returns** — Tags list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getTrashViews

```php
getTrashViews()
```

Returns list of all views available in trash for the specified workspace.

**Returns** — Trash view list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getVariableDetails

```php
getVariableDetails($variable_id)
```

Returns details of the specified variable.

| Parameter | Type | Description |
|---|---|---|
| `variable_id` | `string` | Id of the variable. |

**Returns** — Variable details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getVariables

```php
getVariables()
```

Returns list of variables for the specified workspace.

**Returns** — Variables list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getViews

```php
getViews($config = array()
```

Returns list of all accessible views for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — View list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getWorkspaceAccessRestrictions

```php
getWorkspaceAccessRestrictions()
```

Returns the access restriction settings configured for the specified workspace.

**Returns** — Workspace access restriction settings.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getWorkspaceBackups

```php
getWorkspaceBackups()
```

Returns the backup configuration and the list of backups available for the specified workspace.

**Returns** — Workspace backup details.

### getWorkspaceBackupStatus

```php
getWorkspaceBackupStatus($backup_id)
```

Returns the status of the specified workspace backup.

| Parameter | Type | Description |
|---|---|---|
| `backup_id` | `string` | Id of the backup. |

**Returns** — Backup status details.

### getWorkspaceLinkingCompatibility

```php
getWorkspaceLinkingCompatibility($clients, $config = array()
```

Returns the linking compatibility details for the specified client workspaces.

| Parameter | Type | Description |
|---|---|---|
| `clients` | `array()` | Contains the client workspaces to be verified for linking compatibility. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Client workspace compatibility details.

### getWorkspaceRestoreStatus

```php
getWorkspaceRestoreStatus($restore_id)
```

Returns the status of the specified workspace restore.

| Parameter | Type | Description |
|---|---|---|
| `restore_id` | `string` | Id of the restore. |

**Returns** — Restore status details.

### getWorkspaceUsers

```php
getWorkspaceUsers()
```

Returns list of users for the specified workspace.

**Returns** — User list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### linkWorkspaces

```php
linkWorkspaces($clients, $config = array()
```

Link the specified client workspaces to the master workspace.

| Parameter | Type | Description |
|---|---|---|
| `clients` | `array()` | Contains the client workspaces to be linked with the master workspace. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

### makeDefaultFolder

```php
makeDefaultFolder($folder_id)
```

Make the specified folder as default.

| Parameter | Type | Description |
|---|---|---|
| `folder_id` | `string` | Id of the folder. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### moveViewsToFolder

```php
moveViewsToFolder($folder_id, $view_ids, $config = array()
```

Place the folder above the reference folder.

| Parameter | Type | Description |
|---|---|---|
| `folder_id` | `string` | Id of the folder. |
| `referenceFolderId` | `string` | Id of the reference folder. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### removeAdmins

```php
removeAdmins($email_ids, $config = array()
```

Remove admins from the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `array()` | The email address of the admin users to be removed. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### removeDefault

```php
removeDefault()
```

Remove a specified workspace from default.

**Raises** — `IOException`; `ServerException`; `ParseException`

### removeFavorite

```php
removeFavorite()
```

Remove a specified workspace from favorite.

**Raises** — `IOException`; `ServerException`; `ParseException`

### removeGroupMembers

```php
removeGroupMembers($group_id, $email_ids, $config = array()
```

Remove users from the specified group.

| Parameter | Type | Description |
|---|---|---|
| `group_id` | `string` | Id of the group. |
| `email_ids` | `array()` | The email address of the users to be removed from the group. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### removeShare

```php
removeShare($view_ids, $email_ids, $config = array()
```

Remove shared views for the specified users.

| Parameter | Type | Description |
|---|---|---|
| `view_ids` | `array()` | View ids whose sharing needs to be removed. |
| `email_ids` | `array()` | The email address of the users to whom the sharing need to be removed. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### removeTagFromViews

```php
removeTagFromViews($tag_id, $view_ids = NULL, $dissociate_all = false, $config = array()
```

Removes the specified tag from multiple views in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `tag_id` | `string` | Id of the tag. |
| `view_ids` | `array()` | View ids to be dissociated. Not required when dissociate_all is true. |
| `dissociate_all` | `boolean` | To dissociate the tag from all associated views. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

### removeWorkspaceUsers

```php
removeWorkspaceUsers($email_ids, $config = array()
```

Remove users from the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `array()` | The email address of the users to be removed. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### rename

```php
rename($workspace_name, $config = array()
```

Rename a specified workspace in the organization.

| Parameter | Type | Description |
|---|---|---|
| `workspace_name` | `string` | New name for the workspace. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### renameFolder

```php
renameFolder($folder_id, $folder_name, $config = array()
```

Rename a specified folder in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `folder_id` | `string` | Id of the folder. |
| `folder_name` | `string` | New name for the folder. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### renameGroup

```php
renameGroup($group_id, $new_group_name, $config = array()
```

Rename a specified group.

| Parameter | Type | Description |
|---|---|---|
| `group_id` | `string` | Id of the group. |
| `new_group_name` | `string` | New name for the group. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### restoreTrashView

```php
restoreTrashView($view_id, $config=array()
```

Restore the specified view from trash.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### restoreWorkspaceFromBackup

```php
restoreWorkspaceFromBackup($backup_id, $confirm_restore, $config = array()
```

Restore the specified workspace from the given backup.

| Parameter | Type | Description |
|---|---|---|
| `backup_id` | `string` | Id of the backup. |
| `confirm_restore` | `boolean` | Pass true to confirm that the existing workspace data can be overwritten. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Triggered restore details.

### runAlert

```php
runAlert($alert_id, $config = array()
```

Execute the specified data alert immediately.

| Parameter | Type | Description |
|---|---|---|
| `alert_id` | `string` | Id of the data alert. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

### shareViews

```php
shareViews($view_ids, $email_ids, $permissions, $config = array()
```

Share views to the specified users.

| Parameter | Type | Description |
|---|---|---|
| `view_ids` | `array()` | View ids which to be shared. |
| `email_ids` | `array()` | The email address of the users to whom the views need to be shared. |
| `permissions` | `array()` | Contains permission details. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### syncData

```php
syncData($datasource_id, $config=array()
```

Initiate data sync for the specified datasource.

| Parameter | Type | Description |
|---|---|---|
| `datasource_id` | `string` | Id of the datasource. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### syncLinkedWorkspaces

```php
syncLinkedWorkspaces($scope, $config = array()
```

Sync the metadata of the master workspace to its linked client workspaces.

| Parameter | Type | Description |
|---|---|---|
| `scope` | `string` | Scope of the sync operation. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

### triggerEmailSchedule

```php
triggerEmailSchedule($schedule_id)
```

Trigger configured email schedules instantly.

| Parameter | Type | Description |
|---|---|---|
| `schedule_id` | `string` | Id for the email schedule. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### unlinkWorkspaces

```php
unlinkWorkspaces($scope, $config = array()
```

Unlink the client workspaces from the specified master workspace.

| Parameter | Type | Description |
|---|---|---|
| `scope` | `string` | Scope of the unlink operation. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

### updateAlert

```php
updateAlert($alert_id, $alert_name, $schedule_details, $rules, $config = array()
```

Update the specified data alert in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `alert_id` | `string` | Id of the data alert. |
| `alert_name` | `string` | Name of the data alert. |
| `schedule_details` | `array()` | Contains the schedule configurations of the data alert. |
| `rules` | `array()` | Contains the rules to be evaluated by the data alert. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

### updateDashboard

```php
updateDashboard($dashboard_id, $config = array()
```

Update the specified dashboard in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `dashboard_id` | `string` | Id of the dashboard. |
| `config` | `array()` | Contains the dashboard configurations to be updated. |

### updateDatasourceConnection

```php
updateDatasourceConnection($datasource_id, $config=array()
```

Update connection details for the specified datasource.

| Parameter | Type | Description |
|---|---|---|
| `datasource_id` | `string` | Id of the datasource. |
| `config` | `array()` | Contains the control parameters. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### updateEmailSchedule

```php
updateEmailSchedule($schedule_id, $config)
```

Update configurations of the specified email schedule in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `schedule_id` | `string` | Id for the email schedule. |
| `config` | `array()` | Contains the control configurations. |

**Returns** — Updated schedule id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### updateReport

```php
updateReport($view_id, $config = array()
```

Update the design and configuration of the specified report.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view. |
| `config` | `array()` | Contains the control parameters. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### updateSlideshow

```php
updateSlideshow($slide_id, $config = array()
```

Update details of the specified slideshow.

| Parameter | Type | Description |
|---|---|---|
| `slide_id` | `string` | Id of the slideshow. |
| `config` | `array()` | Contains the control configurations |

**Returns** — Created slideshow id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### updateTag

```php
updateTag($tag_id, $config = array()
```

Update details of the specified tag in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `tag_id` | `string` | Id of the tag. |
| `config` | `array()` | Contains the control parameters. |

### updateVariable

```php
updateVariable($variable_id, $variable_name, $variable_datatype, $variable_type, $config = array()
```

Update details of the specified variable in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `variable_id` | `string` | Id of the variable. |
| `variable_name` | `string` | New name for the variable. |
| `variable_datatype` | `string` | New datatype for the variable. |
| `variable_type` | `string` | New type for the variable. |
| `config` | `array()` | Contains the control parameters. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### updateWorkspaceAccessRestrictions

```php
updateWorkspaceAccessRestrictions($config = array()
```

Update the access restriction settings of the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `array()` | Contains the access restriction configurations to be updated. |

**Raises** — `IOException`; `ServerException`; `ParseException`

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
