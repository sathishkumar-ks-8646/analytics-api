# WorkspaceAPI

```python
org       = ac.get_org_instance(ORG_ID)
workspace = ac.get_workspace_instance(ORG_ID, WORKSPACE_ID)
view      = ac.get_view_instance(ORG_ID, WORKSPACE_ID, VIEW_ID)
bulk      = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)
```

`WorkspaceAPI` exposes **117 methods**. Method names are `snake_case` and identifiers are `str`.

## Methods

[`add_admins`](#add-admins), [`add_default`](#add-default), [`add_favorite`](#add-favorite), [`add_group_members`](#add-group-members), [`add_tag_to_views`](#add-tag-to-views), [`add_workspace_users`](#add-workspace-users), [`automl_analysis_prediction`](#automl-analysis-prediction), [`backup_workspace_now`](#backup-workspace-now), [`change_alert_status`](#change-alert-status), [`change_email_schedule_status`](#change-email-schedule-status), [`change_folder_hierarchy`](#change-folder-hierarchy), [`change_folder_position`](#change-folder-position), [`change_workspace_user_role`](#change-workspace-user-role), [`change_workspace_user_status`](#change-workspace-user-status), [`copy`](#copy), [`copy_views`](#copy-views), [`create_automl_analysis`](#create-automl-analysis), [`create_automl_analysis_deployment`](#create-automl-analysis-deployment), [`create_dashboard`](#create-dashboard), [`create_email_schedule`](#create-email-schedule), [`create_folder`](#create-folder), [`create_group`](#create-group), [`create_query_table`](#create-query-table), [`create_report`](#create-report), [`create_slideshow`](#create-slideshow), [`create_table`](#create-table), [`create_tag`](#create-tag), [`create_variable`](#create-variable), [`delete`](#delete), [`delete_alerts`](#delete-alerts), [`delete_automl_analysis`](#delete-automl-analysis), [`delete_automl_analysis_deployment`](#delete-automl-analysis-deployment), [`delete_automl_analysis_model`](#delete-automl-analysis-model), [`delete_email_schedule`](#delete-email-schedule), [`delete_folder`](#delete-folder), [`delete_group`](#delete-group), [`delete_slideshow`](#delete-slideshow), [`delete_tag`](#delete-tag), [`delete_trash_views`](#delete-trash-views), [`delete_variable`](#delete-variable), [`deploy_automl_analysis`](#deploy-automl-analysis), [`disable_domain_access`](#disable-domain-access), [`download_workspace_backup`](#download-workspace-backup), [`edit_query_table`](#edit-query-table), [`enable_domain_access`](#enable-domain-access), [`export_as_template`](#export-as-template), [`get_admins`](#get-admins), [`get_aggregate_formula_dependents`](#get-aggregate-formula-dependents), [`get_aggregate_formula_value`](#get-aggregate-formula-value), [`get_aggregate_formulas`](#get-aggregate-formulas), [`get_alert_configuration`](#get-alert-configuration), [`get_alert_events`](#get-alert-events), [`get_alerts_in_workspace`](#get-alerts-in-workspace), [`get_automl_analysis`](#get-automl-analysis), [`get_automl_analysis_details`](#get-automl-analysis-details), [`get_dashboard_metadata`](#get-dashboard-metadata), [`get_datasources`](#get-datasources), [`get_deployment_details`](#get-deployment-details), [`get_email_schedules`](#get-email-schedules), [`get_folders`](#get-folders), [`get_group_details`](#get-group-details), [`get_groups`](#get-groups), [`get_linkable_workspaces`](#get-linkable-workspaces), [`get_linked_workspace_sync_details`](#get-linked-workspace-sync-details), [`get_linked_workspaces`](#get-linked-workspaces), [`get_query_table_details`](#get-query-table-details), [`get_query_tables`](#get-query-tables), [`get_report_metadata`](#get-report-metadata), [`get_secret_key`](#get-secret-key), [`get_share_info`](#get-share-info), [`get_shared_details_for_views`](#get-shared-details-for-views), [`get_slideshow_details`](#get-slideshow-details), [`get_slideshow_url`](#get-slideshow-url), [`get_slideshows`](#get-slideshows), [`get_tagged_views`](#get-tagged-views), [`get_tags`](#get-tags), [`get_trash_views`](#get-trash-views), [`get_variable_details`](#get-variable-details), [`get_variables`](#get-variables), [`get_views`](#get-views), [`get_workspace_access_restrictions`](#get-workspace-access-restrictions), [`get_workspace_backup_status`](#get-workspace-backup-status), [`get_workspace_backups`](#get-workspace-backups), [`get_workspace_details`](#get-workspace-details), [`get_workspace_linking_compatibility`](#get-workspace-linking-compatibility), [`get_workspace_restore_status`](#get-workspace-restore-status), [`get_workspace_users`](#get-workspace-users), [`link_workspaces`](#link-workspaces), [`make_default_folder`](#make-default-folder), [`move_views_to_folder`](#move-views-to-folder), [`remove_admins`](#remove-admins), [`remove_default`](#remove-default), [`remove_favorite`](#remove-favorite), [`remove_group_members`](#remove-group-members), [`remove_share`](#remove-share), [`remove_tag_from_views`](#remove-tag-from-views), [`remove_workspace_users`](#remove-workspace-users), [`rename`](#rename), [`rename_folder`](#rename-folder), [`rename_group`](#rename-group), [`restore_trash_views`](#restore-trash-views), [`restore_workspace_from_backup`](#restore-workspace-from-backup), [`run_alert`](#run-alert), [`share_views`](#share-views), [`sync_data`](#sync-data), [`sync_linked_workspaces`](#sync-linked-workspaces), [`trigger_email_schedule`](#trigger-email-schedule), [`unlink_workspaces`](#unlink-workspaces), [`update_alert`](#update-alert), [`update_dashboard`](#update-dashboard), [`update_datasource_connection`](#update-datasource-connection), [`update_email_schedule`](#update-email-schedule), [`update_report`](#update-report), [`update_slideshow`](#update-slideshow), [`update_tag`](#update-tag), [`update_variable`](#update-variable), [`update_workspace_access_restrictions`](#update-workspace-access-restrictions)

### add_admins

```python
add_admins(email_ids, config = {})
```

Add admins for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `list` | The email address of the admin users to be added. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### add_default

```python
add_default()
```

Adds a specified workspace as default.

**Raises** — `ServerError`; `ParseError`

### add_favorite

```python
add_favorite()
```

Adds a specified workspace as favorite.

**Raises** — `ServerError`; `ParseError`

### add_group_members

```python
add_group_members(group_id, email_ids, config = {})
```

Add users to the specified group.

| Parameter | Type | Description |
|---|---|---|
| `group_id` | `string` | Id of the group. |
| `email_ids` | `list` | The email address of the users to be added to the group. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### add_tag_to_views

```python
add_tag_to_views(tag_id, view_ids, config = {})
```

Adds the specified tag to multiple views in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `tag_id` | `string` | Id of the tag. |
| `view_ids` | `list` | View ids to be associated with the tag. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### add_workspace_users

```python
add_workspace_users(email_ids, role, config = {})
```

Add users to the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `list` | The email address of the users to be added. |
| `role` | `string` | Role of the user to be added. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### automl_analysis_prediction

```python
automl_analysis_prediction(analysis_id, model_id, features, config = {})
```

Get predictions by providing sample input values for a trained model.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `string` | Id of the Automl Analysis that contains the target model. |
| `model_id` | `string` | Id of the Automl Analysis model to be deployed. |
| `features` | `dictionary` | A dictionary mapping column names to their corresponding values. The prediction will be generated using this data as the input record. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`dictionary`) — Dataset prediction details.

**Raises** — `ServerError`; `ParseError`

### backup_workspace_now

```python
backup_workspace_now(config = {})
```

Trigger an instant backup for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`dictionary`) — Triggered backup details.

**Raises** — `ServerError`; `ParseError`

### change_alert_status

```python
change_alert_status(alert_ids, enabled, config = {})
```

Enable or disable the specified data alerts in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `alert_ids` | `list` | Ids of the data alerts. |
| `enabled` | `boolean` | Pass C{True} to enable the data alerts and C{False} to disable them. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### change_email_schedule_status

```python
change_email_schedule_status(schedule_id, operation)
```

Update email schedule status.

| Parameter | Type | Description |
|---|---|---|
| `schedule_id` | `string` | Id for the email schedule. |
| `operation` | `string` | New status for the schedule ( Values - activate | deactivate ) |

**Raises** — `ServerError`; `ParseError`

### change_folder_hierarchy

```python
change_folder_hierarchy(folder_id, hierarchy, config = {})
```

Swaps the hierarchy of a parent folder and a subfolder.

| Parameter | Type | Description |
|---|---|---|
| `folder_id` | `string` | Id of the folder. |
| `hierarchy` | `string` | New hierarchy for the folder. (0 - Parent; 1 - Child). |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### change_folder_position

```python
change_folder_position(folder_id, reference_folder_id, config = {})
```

Place the folder above the reference folder.

| Parameter | Type | Description |
|---|---|---|
| `folder_id` | `string` | Id of the folder. |
| `reference_folder_id` | `string` | Id of the reference folder. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### change_workspace_user_role

```python
change_workspace_user_role(email_ids, role, config = {})
```

Change role for the specified users.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `list` | The email address of the users. |
| `role` | `string` | New role for the users. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### change_workspace_user_status

```python
change_workspace_user_status(email_ids, operation, config = {})
```

Change users status in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `list` | The email address of the users. |
| `operation` | `string` | New status for the users ( Values - activate | deactivate ). |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### copy

```python
copy(new_workspace_name, config = {}, dest_org_id = None)
```

Copy the specified workspace from one organization to another or within the organization.

| Parameter | Type | Description |
|---|---|---|
| `new_workspace_name` | `string` | Name of the new workspace. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |
| `dest_org_id` | `string` | Id of the organization where the destination workspace is present. Can be `null`. |

**Returns** (`string`) — Copied workspace id.

**Raises** — `ServerError`; `ParseError`

### copy_views

```python
copy_views(view_ids, dest_workspace_id, config = {}, dest_org_id = None)
```

Copy the specified views from one workspace to another workspace.

| Parameter | Type | Description |
|---|---|---|
| `view_ids` | `list` | The id of the views to be copied. |
| `dest_workspace_id` | `string` | The destination workspace id. |
| `dest_org_id` | `string` | Id of the organization where the destination workspace is present. Can be `null`. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`list`) — View list.

**Raises** — `ServerError`; `ParseError`

### create_automl_analysis

```python
create_automl_analysis(name, training_table_id, prediction_type, features, server_option, algorithms, config = {})
```

Create a new AutoML analysis within the provided workspace.

| Parameter | Type | Description |
|---|---|---|
| `name` | `string` | Name for the automl analysis to be created. |
| `training_table_id` | `string` | Id of the training table. A training table is a structured dataset for training machine learning models, with rows as data points and columns as features. |
| `prediction_type` | `string` | The type of prediction task. Supported values: |
| `features` | `list` | A list of column names representing the features used by the model. Features are the influencing columns in the dataset used by the machine learning model to make predictions. |
| `server_option` | `int` | Specifies the compute size to be used for training. Supported values: |
| `algorithms` | `dictionary` | An algorithm is a particular technique or mathematical model utilized for analyzing data and making predictions. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Created AutoML Analysis Id

**Raises** — `ServerError`; `ParseError`

### create_automl_analysis_deployment

```python
create_automl_analysis_deployment(analysis_id, model_id, input_table_id, output_table, output_columns, prediction_column, server_option, import_type, schedule_details, config = {})
```

Deploy the AutoML analysis model.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `string` | Id of the Automl Analysis that contains the target model. |
| `model_id` | `string` | Id of the Automl Analysis model to be deployed. |
| `input_table_id` | `string` | Id of the input table to be analysed. |
| `output_table` | `string` | Name of the table to be created. New output table will be created while deployment |
| `output_columns` | `list` | A list of column names representing the columns to be included in the output tables. |
| `prediction_column` | `string` | Name of the prediction column to be created in the output table. |
| `server_option` | `int` | Specifies the compute size to be used for training. Supported values: |
| `import_type` | `string` | The type of import. Can be one of - APPEND, TRUNCATEADD, UPDATEADD. |
| `schedule_details` | `dictionary` | Contains schedule frequency, date, and time info. Can be `null`. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`dictionary`) — Created AutoML Deployment Id and the Output Table Id.

**Raises** — `ServerError`; `ParseError`

### create_dashboard

```python
create_dashboard(display_name, layout, config = {})
```

Create a dashboard in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `display_name` | `string` | Name of the dashboard. |
| `layout` | `string` | Layout configuration of the dashboard. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Created dashboard id.

**Raises** — `ServerError`; `ParseError`

### create_email_schedule

```python
create_email_schedule(schedule_name, view_ids, format, email_ids, schedule_details, config={})
```

Create an email schedule in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `schedule_name` | `string` | Name of the email schedule. |
| `view_ids` | `list` | View ids to be mailed. |
| `format` | `string` | The format in which the data has to be mailed. |
| `email_ids` | `list` | The recipients' email addresses for sending views. |
| `schedule_details` | `dictionary` | Contains schedule frequency, date, and time info. |
| `config` | `dictionary` | Contains any additional control parameters. Can be None. |

**Returns** (`string`) — Email schedule id.

**Raises** — `ServerError`; `ParseError`

### create_folder

```python
create_folder(folder_name, config = {})
```

Create a folder in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `folder_name` | `string` | Name of the folder to be created. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Created folder id.

**Raises** — `ServerError`; `ParseError`

### create_group

```python
create_group(group_name, email_ids, config = {})
```

Create a group in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `group_name` | `string` | Name of the group. |
| `email_ids` | `list` | The email address of the users to be added to the group. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Created group id.

**Raises** — `ServerError`; `ParseError`

### create_query_table

```python
create_query_table(sql_query, query_table_name, config = {})
```

Create a new query table in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `sql_query` | `string` | SQL query to construct the query table. |
| `query_table_name` | `string` | Name of the query table to be created. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — created table id.

**Raises** — `ServerError`; `ParseError`

### create_report

```python
create_report(config = {})
```

Create a report in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains the control parameters. |

**Returns** (`string`) — Id of the created view.

**Raises** — `ServerError`; `ParseError`

### create_slideshow

```python
create_slideshow(slide_name, view_ids, config = {})
```

Create a slideshow in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `slide_name` | `string` | Name of the slideshow to be created. |
| `view_ids` | `list` | Ids of the view to be included in the slideshow. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Id of the created slideshow.

**Raises** — `ServerError`; `ParseError`

### create_table

```python
create_table(table_design)
```

Create a table in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `table_design` | `dictionary` | Table structure. |

**Returns** (`string`) — created table id.

**Raises** — `ServerError`; `ParseError`

### create_tag

```python
create_tag(tag_name, color_code, config = {})
```

Create a tag in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `tag_name` | `string` | Name of the tag to be created. |
| `color_code` | `string` | Color of the tag in HEX color code. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Created tag id.

**Raises** — `ServerError`; `ParseError`

### create_variable

```python
create_variable(variable_name, variable_datatype, variable_type, config = {})
```

Create a variable in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `variable_name` | `string` | Name of the variable to be created. |
| `variable_datatype` | `string` | Datatype of the variable to be created. |
| `variable_type` | `string` | Type of the variable to be created. |
| `config` | `dictionary` | Contains the control parameters. |

**Returns** (`string`) — Id of the created variable.

**Raises** — `ServerError`; `ParseError`

### delete

```python
delete()
```

Delete a specified workspace in the organization.

**Raises** — `ServerError`; `ParseError`

### delete_alerts

```python
delete_alerts(alert_ids, config = {})
```

Delete the specified data alerts from the workspace.

| Parameter | Type | Description |
|---|---|---|
| `alert_ids` | `list` | Ids of the data alerts to be deleted. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### delete_automl_analysis

```python
delete_automl_analysis(analysis_id, config = {})
```

Delete a specified automl analysis from the given workspace.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `string` | Id of the Automl Analysis to be deleted. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### delete_automl_analysis_deployment

```python
delete_automl_analysis_deployment(analysis_id, deployment_id, config = {})
```

Delete the AutoML analysis deployment.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `string` | Id of the Automl Analysis.. |
| `deployment_id` | `string` | Id of the Analysis deployment to be deleted. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### delete_automl_analysis_model

```python
delete_automl_analysis_model(analysis_id, model_id, config = {})
```

Delete a specified model avaiable in the given automl analysis.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `string` | Id of the Automl Analysis that contains the target model. |
| `model_id` | `string` | Id of the model within the specified AutoML analysis that should be deleted. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### delete_email_schedule

```python
delete_email_schedule(schedule_id)
```

Delete the specified email schedule in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `schedule_id` | `string` | Id for the email schedule. |

**Raises** — `ServerError`; `ParseError`

### delete_folder

```python
delete_folder(folder_id)
```

Delete a specified folder in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `folder_id` | `string` | Id of the folder to be deleted. |

**Raises** — `ServerError`; `ParseError`

### delete_group

```python
delete_group(group_id)
```

Delete a specified group.

| Parameter | Type | Description |
|---|---|---|
| `group_id` | `string` | The id of the group. |

**Raises** — `ServerError`; `ParseError`

### delete_slideshow

```python
delete_slideshow(slide_id)
```

Delete a specified slideshow in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `slide_id` | `string` | Id of the slideshow. |

**Raises** — `ServerError`; `ParseError`

### delete_tag

```python
delete_tag(tag_id)
```

Delete the specified tag from the workspace.

| Parameter | Type | Description |
|---|---|---|
| `tag_id` | `string` | Id of the tag. |

**Raises** — `ServerError`; `ParseError`

### delete_trash_views

```python
delete_trash_views(view_id, config = {})
```

Delete the specified view permanently from trash.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### delete_variable

```python
delete_variable(variable_id)
```

Delete the specified variable in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `variable_id` | `string` | Id of the variable. |

**Raises** — `ServerError`; `ParseError`

### deploy_automl_analysis

```python
deploy_automl_analysis(analysis_id, deployment_id, config = {})
```

Deploy the AutoML analysis model.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `string` | Id of the Automl Analysis that contains the target model. |
| `deployment_id` | `string` | Id of the Analysis deployment to be executed. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### disable_domain_access

```python
disable_domain_access()
```

Disable workspace from the specified white label domain.

**Raises** — `ServerError`; `ParseError`

### download_workspace_backup

```python
download_workspace_backup(backup_id, file_path, config = {})
```

Download the specified workspace backup.

| Parameter | Type | Description |
|---|---|---|
| `backup_id` | `string` | Id of the backup. |
| `file_path` | `string` | Path of the file where the downloaded backup is to be stored. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### edit_query_table

```python
edit_query_table(view_id, sql_query, config = {})
```

Update the mentioned query table in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the query table to be updated. |
| `sql_query` | `string` | New SQL query to be updated. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### enable_domain_access

```python
enable_domain_access()
```

Enable workspace to the specified white label domain.

**Raises** — `ServerError`; `ParseError`

### export_as_template

```python
export_as_template(view_ids, file_path, config = {})
```

Export the mentioned views as templates.

| Parameter | Type | Description |
|---|---|---|
| `view_ids` | `list` | Ids of the views to be exported. |
| `file_path` | `string` | Path of the file where the data exported to be stored. ( Should be in 'atpt' format ) |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### get_admins

```python
get_admins()
```

Returns list of admins for the specified workspace.

**Returns** (`list`) — Workspace admin list.

**Raises** — `ServerError`; `ParseError`

### get_aggregate_formula_dependents

```python
get_aggregate_formula_dependents(formula_id)
```

Returns list of all dependent views and formulas for the specified aggregate formula.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `string` | Id of the aggregate formula |

**Returns** (`dictionary`) — Dependent details.

**Raises** — `ServerError`; `ParseError`

### get_aggregate_formula_value

```python
get_aggregate_formula_value(formula_id)
```

Returns the value of the aggregate formula.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `string` | Id of the aggregate formula |

**Returns** (`string`) — Aggregate formula value.

**Raises** — `ServerError`; `ParseError`

### get_aggregate_formulas

```python
get_aggregate_formulas(config = {})
```

Returns list of all aggregate formulas for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`list`) — Aggregate formula list.

**Raises** — `ServerError`; `ParseError`

### get_alert_configuration

```python
get_alert_configuration(alert_id)
```

Returns the configuration of the specified data alert.

| Parameter | Type | Description |
|---|---|---|
| `alert_id` | `string` | Id of the data alert. |

**Returns** (`dictionary`) — Data alert configuration.

**Raises** — `ServerError`; `ParseError`

### get_alert_events

```python
get_alert_events(alert_id, config = {})
```

Returns the execution events of the specified data alert.

| Parameter | Type | Description |
|---|---|---|
| `alert_id` | `string` | Id of the data alert. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`dictionary`) — Data alert events along with the page details.

**Raises** — `ServerError`; `ParseError`

### get_alerts_in_workspace

```python
get_alerts_in_workspace()
```

Returns list of data alerts available in the specified workspace.

**Returns** (`list`) — Data alerts list.

**Raises** — `ServerError`; `ParseError`

### get_automl_analysis

```python
get_automl_analysis()
```

Returns list of automl analysis for the specified workspace.

**Returns** (`list`) — AutoML analysis list.

**Raises** — `ServerError`; `ParseError`

### get_automl_analysis_details

```python
get_automl_analysis_details(analysis_id)
```

Retrieve detailed information for a specific AutoML analysis.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `string` | Id of the Automl Analysis. |

**Returns** (`dictionary`) — AutoML analysis details.

**Raises** — `ServerError`; `ParseError`

### get_dashboard_metadata

```python
get_dashboard_metadata(dashboard_id, config = {})
```

Returns the metadata of the specified dashboard.

| Parameter | Type | Description |
|---|---|---|
| `dashboard_id` | `string` | Id of the dashboard. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`dictionary`) — Dashboard configuration.

**Raises** — `ServerError`; `ParseError`

### get_datasources

```python
get_datasources()
```

Returns list of datasources for the specified workspace.

**Returns** (`list`) — Datasource list.

**Raises** — `ServerError`; `ParseError`

### get_deployment_details

```python
get_deployment_details(analysis_id, model_id)
```

Returns deployment details available for a AutoML analysis model.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `string` | Id of the Automl Analysis. |
| `model_id` | `string` | Id of the Automl Analysis Model. |

**Returns** (`dictionary`) — AutoML analysis deployment details.

**Raises** — `ServerError`; `ParseError`

### get_email_schedules

```python
get_email_schedules()
```

Returns list of email schedules available in the specified workspace.

**Returns** (`list`) — List of email schedules.

**Raises** — `ServerError`; `ParseError`

### get_folders

```python
get_folders()
```

Returns list of all accessible folders for the specified workspace.

**Returns** (`list`) — Folder list.

**Raises** — `ServerError`; `ParseError`

### get_group_details

```python
get_group_details(group_id)
```

Get the details of the specified group.

| Parameter | Type | Description |
|---|---|---|
| `group_id` | `string` | Id of the group. |

**Returns** (`dictionary`) — Details of the specified group.

**Raises** — `ServerError`; `ParseError`

### get_groups

```python
get_groups()
```

Returns list of groups for the specified workspace.

**Returns** (`list`) — Group list.

**Raises** — `ServerError`; `ParseError`

### get_linkable_workspaces

```python
get_linkable_workspaces()
```

Returns list of organizations and workspaces that can be linked to the specified master workspace.

**Returns** (`list`) — Organizations with their linkable workspaces.

**Raises** — `ServerError`; `ParseError`

### get_linked_workspace_sync_details

```python
get_linked_workspace_sync_details(sandbox_ids, config = {})
```

Returns the sync details of the specified linked workspaces.

| Parameter | Type | Description |
|---|---|---|
| `sandbox_ids` | `list` | Ids of the linked workspaces for which the sync details are fetched. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`list`) — Linked workspace sync details.

**Raises** — `ServerError`; `ParseError`

### get_linked_workspaces

```python
get_linked_workspaces()
```

Returns list of workspaces linked to the specified master workspace.

**Returns** (`list`) — Linked workspaces list.

**Raises** — `ServerError`; `ParseError`

### get_query_table_details

```python
get_query_table_details(query_table_id)
```

Returns details of the specified query table.

| Parameter | Type | Description |
|---|---|---|
| `query_table_id` | `string` | Id of the query table |

**Returns** (`dictionary`) — View details.

**Raises** — `ServerError`; `ParseError`

### get_query_tables

```python
get_query_tables(config = {})
```

Returns list of all query tables for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`list`) — Query table list.

**Raises** — `ServerError`; `ParseError`

### get_report_metadata

```python
get_report_metadata(view_id)
```

Returns the metadata of the specified report.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the report. |

**Returns** (`dictionary`) — Report configuration.

**Raises** — `ServerError`; `ParseError`

### get_secret_key

```python
get_secret_key(config = {})
```

Returns the secret key of the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Workspace secret key.

**Raises** — `ServerError`; `ParseError`

### get_share_info

```python
get_share_info()
```

Returns shared details of the specified workspace.

**Returns** (`dictionary`) — Workspace share info.

**Raises** — `ServerError`; `ParseError`

### get_shared_details_for_views

```python
get_shared_details_for_views(view_ids)
```

Returns shared details of the specified views.

| Parameter | Type | Description |
|---|---|---|
| `view_ids` | `list` | View ids for which sharing details are required. |

**Returns** (`list`) — Shared information.

**Raises** — `ServerError`; `ParseError`

### get_slideshow_details

```python
get_slideshow_details(slide_id)
```

Returns details of the specified slideshow.

| Parameter | Type | Description |
|---|---|---|
| `slide_id` | `string` | Id of the slideshow. |

**Returns** (`dictionary`) — Slideshow details.

**Raises** — `ServerError`; `ParseError`

### get_slideshow_url

```python
get_slideshow_url(slide_id, config = {})
```

Returns slide URL to access the specified slideshow.

| Parameter | Type | Description |
|---|---|---|
| `slide_id` | `string` | Id of the slideshow. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Slideshow URL.

**Raises** — `ServerError`; `ParseError`

### get_slideshows

```python
get_slideshows()
```

Returns list of slideshows for the specified workspace.

**Returns** (`list`) — Slideshow list.

**Raises** — `ServerError`; `ParseError`

### get_tagged_views

```python
get_tagged_views(tag_id)
```

Returns list of views associated with the specified tag.

| Parameter | Type | Description |
|---|---|---|
| `tag_id` | `string` | Id of the tag. |

**Returns** (`list`) — Tagged views list.

**Raises** — `ServerError`; `ParseError`

### get_tags

```python
get_tags()
```

Returns list of all tags for the specified workspace.

**Returns** (`list`) — Tags list.

**Raises** — `ServerError`; `ParseError`

### get_trash_views

```python
get_trash_views()
```

Initiate data sync for the specified datasource.

**Returns** (`list`) — Trash view list.

**Raises** — `ServerError`; `ParseError`

### get_variable_details

```python
get_variable_details(variable_id)
```

Returns list of variables for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `variable_id` | `string` | Id of the variable. |

**Returns** (`dictionary`) — Variable details.

**Raises** — `ServerError`; `ParseError`

### get_variables

```python
get_variables()
```

Returns list of variables for the specified workspace.

**Returns** (`list`) — Variable list.

**Raises** — `ServerError`; `ParseError`

### get_views

```python
get_views(config = {})
```

Returns list of all accessible views for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`list`) — View list.

**Raises** — `ServerError`; `ParseError`

### get_workspace_access_restrictions

```python
get_workspace_access_restrictions()
```

Returns the access restriction settings configured for the specified workspace.

**Returns** (`dictionary`) — Workspace access restriction settings.

**Raises** — `ServerError`; `ParseError`

### get_workspace_backup_status

```python
get_workspace_backup_status(backup_id)
```

Returns the status of the specified workspace backup.

| Parameter | Type | Description |
|---|---|---|
| `backup_id` | `string` | Id of the backup. |

**Returns** (`dictionary`) — Backup status details.

**Raises** — `ServerError`; `ParseError`

### get_workspace_backups

```python
get_workspace_backups()
```

Returns the backup configuration and the list of backups available for the specified workspace.

**Returns** (`dictionary`) — Workspace backup details.

**Raises** — `ServerError`; `ParseError`

### get_workspace_details

```python
get_workspace_details(config = {})
```

Returns details of the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`dictionary`) — Workspace details.

**Raises** — `ServerError`; `ParseError`

### get_workspace_linking_compatibility

```python
get_workspace_linking_compatibility(clients, config = {})
```

Returns the linking compatibility details for the specified client workspaces.

| Parameter | Type | Description |
|---|---|---|
| `clients` | `list` | Contains the client workspaces to be verified for linking compatibility. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`list`) — Client workspace compatibility details.

**Raises** — `ServerError`; `ParseError`

### get_workspace_restore_status

```python
get_workspace_restore_status(restore_id)
```

Returns the status of the specified workspace restore.

| Parameter | Type | Description |
|---|---|---|
| `restore_id` | `string` | Id of the restore. |

**Returns** (`dictionary`) — Restore status details.

**Raises** — `ServerError`; `ParseError`

### get_workspace_users

```python
get_workspace_users()
```

Returns list of users for the specified workspace.

**Returns** (`list`) — User list.

**Raises** — `ServerError`; `ParseError`

### link_workspaces

```python
link_workspaces(clients, config = {})
```

Link the specified client workspaces to the master workspace.

| Parameter | Type | Description |
|---|---|---|
| `clients` | `list` | Contains the client workspaces to be linked with the master workspace. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### make_default_folder

```python
make_default_folder(folder_id)
```

Make the specified folder as default.

| Parameter | Type | Description |
|---|---|---|
| `folder_id` | `string` | Id of the folder. |

**Raises** — `ServerError`; `ParseError`

### move_views_to_folder

```python
move_views_to_folder(folder_id, view_ids, config = {})
```

Move views to the mentioned folder.

| Parameter | Type | Description |
|---|---|---|
| `folder_id` | `string` | Id of the folder. |
| `view_ids` | `list` | View ids to be moved. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### remove_admins

```python
remove_admins(email_ids, config = {})
```

Remove admins from the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `list` | The email address of the admin users to be removed. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### remove_default

```python
remove_default()
```

Remove a specified workspace from default.

**Raises** — `ServerError`; `ParseError`

### remove_favorite

```python
remove_favorite()
```

Remove a specified workspace from favorite.

**Raises** — `ServerError`; `ParseError`

### remove_group_members

```python
remove_group_members(group_id, email_ids, config = {})
```

Remove users from the specified group.

| Parameter | Type | Description |
|---|---|---|
| `group_id` | `string` | Id of the group. |
| `email_ids` | `list` | The email address of the users to be removed from the group. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### remove_share

```python
remove_share(view_ids, email_ids, config = {})
```

Remove shared views for the specified users.

| Parameter | Type | Description |
|---|---|---|
| `view_ids` | `list` | View ids whose sharing needs to be removed. |
| `email_ids` | `list` | The email address of the users to whom the sharing need to be removed. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### remove_tag_from_views

```python
remove_tag_from_views(tag_id, view_ids = None, dissociate_all = False, config = {})
```

Removes the specified tag from multiple views in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `tag_id` | `string` | Id of the tag. |
| `view_ids` | `list` | View ids to be dissociated. Not required when dissociate_all is True. |
| `dissociate_all` | `boolean` | To dissociate the tag from all associated views. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### remove_workspace_users

```python
remove_workspace_users(email_ids, config = {})
```

Remove users from the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `list` | The email address of the users to be removed. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### rename

```python
rename(workspace_name, config = {})
```

Rename a specified workspace in the organization.

| Parameter | Type | Description |
|---|---|---|
| `workspace_name` | `string` | New name for the workspace. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### rename_folder

```python
rename_folder(folder_id, folder_name, config = {})
```

Rename a specified folder in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `folder_id` | `string` | Id of the folder. |
| `folder_name` | `string` | New name for the folder. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### rename_group

```python
rename_group(group_id, group_name, config = {})
```

Rename a specified group.

| Parameter | Type | Description |
|---|---|---|
| `group_id` | `string` | Id of the group. |
| `group_name` | `string` | New name for the group. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### restore_trash_views

```python
restore_trash_views(view_id, config = {})
```

Restore the specified view from trash.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### restore_workspace_from_backup

```python
restore_workspace_from_backup(backup_id, confirm_restore, config = {})
```

Restore the specified workspace from the given backup.

| Parameter | Type | Description |
|---|---|---|
| `backup_id` | `string` | Id of the backup. |
| `confirm_restore` | `boolean` | Pass C{True} to confirm that the existing workspace data can be overwritten. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`dictionary`) — Triggered restore details.

**Raises** — `ServerError`; `ParseError`

### run_alert

```python
run_alert(alert_id, config = {})
```

Execute the specified data alert immediately.

| Parameter | Type | Description |
|---|---|---|
| `alert_id` | `string` | Id of the data alert. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### share_views

```python
share_views(view_ids, email_ids, permissions, config = {})
```

Share views to the specified users.

| Parameter | Type | Description |
|---|---|---|
| `view_ids` | `list` | View ids which to be shared. |
| `email_ids` | `list` | The email address of the users to whom the views need to be shared. |
| `permissions` | `dictionary` | Contains permission details. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### sync_data

```python
sync_data(datasource_id, config = {})
```

Initiate data sync for the specified datasource.

| Parameter | Type | Description |
|---|---|---|
| `datasource_id` | `string` | Id of the datasource. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### sync_linked_workspaces

```python
sync_linked_workspaces(scope, config = {})
```

Sync the metadata of the master workspace to its linked client workspaces.

| Parameter | Type | Description |
|---|---|---|
| `scope` | `string` | Scope of the sync operation. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### trigger_email_schedule

```python
trigger_email_schedule(schedule_id)
```

Trigger configured email schedules instantly.

| Parameter | Type | Description |
|---|---|---|
| `schedule_id` | `string` | Id for the email schedule. |

**Raises** — `ServerError`; `ParseError`

### unlink_workspaces

```python
unlink_workspaces(scope, config = {})
```

Unlink the client workspaces from the specified master workspace.

| Parameter | Type | Description |
|---|---|---|
| `scope` | `string` | Scope of the unlink operation. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### update_alert

```python
update_alert(alert_id, alert_name, schedule_details, rules, config = {})
```

Update the specified data alert in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `alert_id` | `string` | Id of the data alert. |
| `alert_name` | `string` | Name of the data alert. |
| `schedule_details` | `dictionary` | Contains the schedule configurations of the data alert. |
| `rules` | `list` | Contains the rules to be evaluated by the data alert. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### update_dashboard

```python
update_dashboard(dashboard_id, config = {})
```

Update the specified dashboard in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `dashboard_id` | `string` | Id of the dashboard. |
| `config` | `dictionary` | Contains the dashboard configurations to be updated. |

**Raises** — `ServerError`; `ParseError`

### update_datasource_connection

```python
update_datasource_connection(datasource_id, config = {})
```

Update connection details for the specified datasource.

| Parameter | Type | Description |
|---|---|---|
| `datasource_id` | `string` | Id of the datasource. |
| `config` | `dictionary` | Contains the control parameters. |

**Raises** — `ServerError`; `ParseError`

### update_email_schedule

```python
update_email_schedule(schedule_id, config)
```

Update configurations of the specified email schedule in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `schedule_id` | `string` | Id for the email schedule. |
| `config` | `dictionary` | Contains the control configurations. |

**Returns** (`string`) — Updated schedule id.

**Raises** — `ServerError`; `ParseError`

### update_report

```python
update_report(view_id, config = {})
```

Update the design and configuration of the specified report.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view. |
| `config` | `dictionary` | Contains the control parameters. |

**Raises** — `ServerError`; `ParseError`

### update_slideshow

```python
update_slideshow(slide_id, config = {})
```

Update details of the specified slideshow.

| Parameter | Type | Description |
|---|---|---|
| `slide_id` | `string` | The id of the slideshow. |
| `config` | `dictionary` | — |

**Raises** — `ServerError`; `ParseError`

### update_tag

```python
update_tag(tag_id, config = {})
```

Update details of the specified tag in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `tag_id` | `string` | Id of the tag. |
| `config` | `dictionary` | Contains the control parameters. |

**Raises** — `ServerError`; `ParseError`

### update_variable

```python
update_variable(variable_id, variable_name, variable_datatype, variable_type, config = {})
```

Update details of the specified variable in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `variable_id` | `string` | Id of the variable. |
| `variable_name` | `string` | New name for the variable. |
| `variable_datatype` | `string` | New datatype for the variable. |
| `variable_type` | `string` | New type for the variable. |
| `config` | `dictionary` | Contains the control parameters. |

**Raises** — `ServerError`; `ParseError`

### update_workspace_access_restrictions

```python
update_workspace_access_restrictions(config = {})
```

Update the access restriction settings of the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains the access restriction configurations to be updated. |

**Raises** — `ServerError`; `ParseError`

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
