# WorkspaceAPI

```ruby
org       = ac.get_org_instance(ORG_ID)
workspace = ac.get_workspace_instance(ORG_ID, WORKSPACE_ID)
view      = ac.get_view_instance(ORG_ID, WORKSPACE_ID, VIEW_ID)
bulk      = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)
```

`WorkspaceAPI` exposes **117 methods**. Method names are `snake_case` and identifiers are `string`.

## Methods

[`add_admins`](#add-admins), [`add_default`](#add-default), [`add_favorite`](#add-favorite), [`add_group_members`](#add-group-members), [`add_tag_to_views`](#add-tag-to-views), [`add_workspace_users`](#add-workspace-users), [`automl_analysis_prediction`](#automl-analysis-prediction), [`backup_workspace_now`](#backup-workspace-now), [`change_alert_status`](#change-alert-status), [`change_email_schedule_status`](#change-email-schedule-status), [`change_folder_hierarchy`](#change-folder-hierarchy), [`change_folder_position`](#change-folder-position), [`change_workspace_user_role`](#change-workspace-user-role), [`change_workspace_user_status`](#change-workspace-user-status), [`copy`](#copy), [`copy_views`](#copy-views), [`create_automl_analysis`](#create-automl-analysis), [`create_automl_analysis_deployment`](#create-automl-analysis-deployment), [`create_dashboard`](#create-dashboard), [`create_email_schedule`](#create-email-schedule), [`create_folder`](#create-folder), [`create_group`](#create-group), [`create_query_table`](#create-query-table), [`create_report`](#create-report), [`create_slideshow`](#create-slideshow), [`create_table`](#create-table), [`create_tag`](#create-tag), [`create_variable`](#create-variable), [`delete`](#delete), [`delete_alerts`](#delete-alerts), [`delete_automl_analysis`](#delete-automl-analysis), [`delete_automl_analysis_deployment`](#delete-automl-analysis-deployment), [`delete_automl_analysis_model`](#delete-automl-analysis-model), [`delete_email_schedule`](#delete-email-schedule), [`delete_folder`](#delete-folder), [`delete_group`](#delete-group), [`delete_slideshow`](#delete-slideshow), [`delete_tag`](#delete-tag), [`delete_trash_views`](#delete-trash-views), [`delete_variable`](#delete-variable), [`deploy_automl_analysis`](#deploy-automl-analysis), [`disable_domain_access`](#disable-domain-access), [`download_workspace_backup`](#download-workspace-backup), [`edit_query_table`](#edit-query-table), [`enable_domain_access`](#enable-domain-access), [`export_as_template`](#export-as-template), [`get_admins`](#get-admins), [`get_aggregate_formula_dependents`](#get-aggregate-formula-dependents), [`get_aggregate_formula_value`](#get-aggregate-formula-value), [`get_aggregate_formulas`](#get-aggregate-formulas), [`get_alert_configuration`](#get-alert-configuration), [`get_alert_events`](#get-alert-events), [`get_alerts_in_workspace`](#get-alerts-in-workspace), [`get_automl_analysis`](#get-automl-analysis), [`get_automl_analysis_details`](#get-automl-analysis-details), [`get_dashboard_metadata`](#get-dashboard-metadata), [`get_datasources`](#get-datasources), [`get_deployment_details`](#get-deployment-details), [`get_email_schedules`](#get-email-schedules), [`get_folders`](#get-folders), [`get_group_details`](#get-group-details), [`get_groups`](#get-groups), [`get_linkable_workspaces`](#get-linkable-workspaces), [`get_linked_workspace_sync_details`](#get-linked-workspace-sync-details), [`get_linked_workspaces`](#get-linked-workspaces), [`get_query_table_details`](#get-query-table-details), [`get_query_tables`](#get-query-tables), [`get_report_metadata`](#get-report-metadata), [`get_secret_key`](#get-secret-key), [`get_share_info`](#get-share-info), [`get_shared_details_for_views`](#get-shared-details-for-views), [`get_slideshow_details`](#get-slideshow-details), [`get_slideshow_url`](#get-slideshow-url), [`get_slideshows`](#get-slideshows), [`get_tagged_views`](#get-tagged-views), [`get_tags`](#get-tags), [`get_trash_views`](#get-trash-views), [`get_variable_details`](#get-variable-details), [`get_variables`](#get-variables), [`get_views`](#get-views), [`get_workspace_access_restrictions`](#get-workspace-access-restrictions), [`get_workspace_backup_status`](#get-workspace-backup-status), [`get_workspace_backups`](#get-workspace-backups), [`get_workspace_details`](#get-workspace-details), [`get_workspace_linking_compatibility`](#get-workspace-linking-compatibility), [`get_workspace_restore_status`](#get-workspace-restore-status), [`get_workspace_users`](#get-workspace-users), [`link_workspaces`](#link-workspaces), [`make_default_folder`](#make-default-folder), [`move_views_to_folder`](#move-views-to-folder), [`remove_admins`](#remove-admins), [`remove_default`](#remove-default), [`remove_favorite`](#remove-favorite), [`remove_group_members`](#remove-group-members), [`remove_share`](#remove-share), [`remove_tag_from_views`](#remove-tag-from-views), [`remove_workspace_users`](#remove-workspace-users), [`rename`](#rename), [`rename_folder`](#rename-folder), [`rename_group`](#rename-group), [`restore_trash_views`](#restore-trash-views), [`restore_workspace_from_backup`](#restore-workspace-from-backup), [`run_alert`](#run-alert), [`share_views`](#share-views), [`sync_data`](#sync-data), [`sync_linked_workspaces`](#sync-linked-workspaces), [`trigger_email_schedule`](#trigger-email-schedule), [`unlink_workspaces`](#unlink-workspaces), [`update_alert`](#update-alert), [`update_dashboard`](#update-dashboard), [`update_datasource_connection`](#update-datasource-connection), [`update_email_schedule`](#update-email-schedule), [`update_report`](#update-report), [`update_slideshow`](#update-slideshow), [`update_tag`](#update-tag), [`update_variable`](#update-variable), [`update_workspace_access_restrictions`](#update-workspace-access-restrictions)

### add_admins

```ruby
add_admins(email_ids, config = {})
```

Add admins to the workspace.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `Array` | Email addresses |
| `config` | `Hash` | Optional config |

### add_default

```ruby
add_default()
```

Set the workspace as default.

### add_favorite

```ruby
add_favorite()
```

Mark the workspace as favorite.

### add_group_members

```ruby
add_group_members(group_id, email_ids, config = {})
```

Add users to a group.

| Parameter | Type | Description |
|---|---|---|
| `group_id` | `String` | Group ID |
| `email_ids` | `Array` | Email list |
| `config` | `Hash` | Optional config |

### add_tag_to_views

```ruby
add_tag_to_views(tag_id, view_ids, config = {})
```

Adds the specified tag to multiple views in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `tag_id` | `String` | Id of the tag |
| `view_ids` | `Array` | View ids to be associated with the tag |
| `config` | `Hash` | Additional control parameters |

### add_workspace_users

```ruby
add_workspace_users(email_ids, role, config = {})
```

Add users to the workspace.

### automl_analysis_prediction

```ruby
automl_analysis_prediction(analysis_id, model_id, features, config = {})
```

Gets predictions by providing sample input values for a trained AutoML model.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `String` | AutoML analysis ID |
| `model_id` | `String` | AutoML model ID |
| `features` | `Hash` | Feature values for prediction |
| `config` | `Hash` | Additional control parameters |

**Returns** (`Hash`) — Prediction result

### backup_workspace_now

```ruby
backup_workspace_now(config = {})
```

Trigger an instant backup for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | Additional control parameters |

**Returns** (`Hash`) — Triggered backup details

### change_alert_status

```ruby
change_alert_status(alert_ids, enabled, config = {})
```

Enable or disable the specified data alerts in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `alert_ids` | `Array` | Ids of the data alerts |
| `enabled` | `Boolean` | Pass true to enable the data alerts and false to disable them |
| `config` | `Hash` | Additional control parameters |

### change_email_schedule_status

```ruby
change_email_schedule_status(schedule_id, operation)
```

Update email schedule status (activate or deactivate).

| Parameter | Type | Description |
|---|---|---|
| `schedule_id` | `String` | ID of the email schedule |
| `operation` | `String` | operation to perform ("activate" or "deactivate") |

### change_folder_hierarchy

```ruby
change_folder_hierarchy(folder_id, hierarchy, config = {})
```

Change folder hierarchy (parent/child).

### change_folder_position

```ruby
change_folder_position(folder_id, reference_folder_id, config = {})
```

Reorder folder relative to another folder.

### change_workspace_user_role

```ruby
change_workspace_user_role(email_ids, role, config = {})
```

Change role of workspace users.

### change_workspace_user_status

```ruby
change_workspace_user_status(email_ids, operation, config = {})
```

Change status (activate/deactivate) of workspace users.

### copy

```ruby
copy(new_workspace_name, config = {}, dest_org_id = nil)
```

Copy the specified workspace to a new one.

| Parameter | Type | Description |
|---|---|---|
| `new_workspace_name` | `String` | New workspace name |
| `config` | `Hash` | Optional config |
| `dest_org_id` | `String, nil` | Destination org ID (optional) |

**Returns** (`Integer`) — Copied workspace ID

### copy_views

```ruby
copy_views(view_ids, dest_workspace_id, config = {}, dest_org_id = nil)
```

Copy views to another workspace.

| Parameter | Type | Description |
|---|---|---|
| `view_ids` | `Array` | IDs to copy |
| `dest_workspace_id` | `String` | Destination workspace ID |
| `config` | `Hash` | Optional config |
| `dest_org_id` | `String, nil` | Destination org ID |

**Returns** (`Array`) — Copied views

### create_automl_analysis

```ruby
create_automl_analysis()
```

Creates a new AutoML analysis in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `name` | `String` | AutoML analysis name |
| `training_table_id` | `String` | Training table ID |
| `prediction_type` | `String` | Prediction type (REGRESSION / CLASSIFICATION / CLUSTERING) |
| `features` | `Array` | Feature columns |
| `server_option` | `Integer` | Compute size (1 → 8GB, 2 → 16GB, 3 → 32GB) |
| `algorithms` | `Hash` | Algorithms configuration |
| `config` | `Hash` | Additional parameters |

**Returns** (`String`) — Created AutoML analysis ID

### create_automl_analysis_deployment

```ruby
create_automl_analysis_deployment()
```

Deploys an AutoML analysis model.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `String` | AutoML analysis ID |
| `model_id` | `String` | AutoML model ID |
| `input_table_id` | `String` | Input table ID |
| `output_table` | `String` | Output table name |
| `output_columns` | `Array` | Output column names |
| `prediction_column` | `String` | Prediction column name |
| `server_option` | `Integer` | Compute size (1 → 8GB, 2 → 16GB, 3 → 32GB) |
| `import_type` | `String` | Import type (APPEND, TRUNCATEADD, UPDATEADD) |
| `schedule_details` | `Hash, String` | Schedule details or "none" |
| `config` | `Hash` | Additional control parameters |

**Returns** (`Array`) — Deployment details

### create_dashboard

```ruby
create_dashboard(display_name, layout, config = {})
```

Create a dashboard in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `display_name` | `String` | Name of the dashboard |
| `layout` | `String` | Layout configuration of the dashboard |
| `config` | `Hash` | Additional control parameters |

**Returns** (`String`) — Created dashboard id

### create_email_schedule

```ruby
create_email_schedule(schedule_name, view_ids, format, email_ids, schedule_details, config = {})
```

Create an email schedule in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `schedule_name` | `String` | name of the email schedule |
| `view_ids` | `Array` | list of view IDs to be mailed |
| `format` | `String` | format in which data will be mailed |
| `email_ids` | `Array` | list of recipient email addresses |
| `schedule_details` | `Hash` | frequency, date, and time details |
| `config` | `Hash` | additional optional parameters (default: {}) |

**Returns** (`String`) — created email schedule ID

### create_folder

```ruby
create_folder(folder_name, config = {})
```

Create a new folder in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `folder_name` | `String` | Folder name |
| `config` | `Hash` | Optional config |

**Returns** (`Integer`) — Created folder ID

### create_group

```ruby
create_group(group_name, email_ids, config = {})
```

Create a group.

| Parameter | Type | Description |
|---|---|---|
| `group_name` | `String` | Name of group |
| `email_ids` | `Array` | Emails of members |
| `config` | `Hash` | Optional config |

**Returns** (`Integer`) — Group ID

### create_query_table

```ruby
create_query_table(sql_query, query_table_name, config = {})
```

Create a new query table in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `sql_query` | `String` | SQL definition |
| `query_table_name` | `String` | Name of query table |
| `config` | `Hash` | Optional config |

**Returns** (`Integer`) — Created view ID

### create_report

```ruby
create_report(config = {})
```

Create a report in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | report parameters |

**Returns** (`Integer`) — created view ID

### create_slideshow

```ruby
create_slideshow(slide_name, view_ids, config = {})
```

Create a slideshow in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `slide_name` | `String` | Name of slideshow |
| `view_ids` | `Array` | View IDs |
| `config` | `Hash` | Optional config |

**Returns** (`Integer`) — Slideshow ID

### create_table

```ruby
create_table(table_design)
```

Create a new table in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `table_design` | `Hash` | Table definition |

**Returns** (`Integer`) — Created view ID

### create_tag

```ruby
create_tag(tag_name, color_code, config = {})
```

Create a tag in the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `tag_name` | `String` | Name of the tag to be created |
| `color_code` | `String` | Color of the tag in HEX color code |
| `config` | `Hash` | Additional control parameters |

**Returns** (`String`) — Created tag id

### create_variable

```ruby
create_variable(variable_name, variable_datatype, variable_type, config = {})
```

Create a variable in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `variable_name` | `String` | Name of the variable |
| `variable_datatype` | `String` | Datatype of the variable |
| `variable_type` | `String` | Type of the variable |
| `config` | `Hash` | Additional config |

**Returns** (`Integer`) — Variable ID

### delete

```ruby
delete()
```

Delete the specified workspace.

### delete_alerts

```ruby
delete_alerts(alert_ids, config = {})
```

Delete the specified data alerts from the workspace.

| Parameter | Type | Description |
|---|---|---|
| `alert_ids` | `Array` | Ids of the data alerts to be deleted |
| `config` | `Hash` | Additional control parameters |

### delete_automl_analysis

```ruby
delete_automl_analysis(analysis_id, config = {})
```

Deletes the specified AutoML analysis from the workspace.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `String` | AutoML analysis ID |
| `config` | `Hash` | Additional control parameters |

### delete_automl_analysis_deployment

```ruby
delete_automl_analysis_deployment(analysis_id, deployment_id, config = {})
```

Deletes an AutoML analysis deployment.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `String` | AutoML analysis ID |
| `deployment_id` | `String` | Deployment ID |
| `config` | `Hash` | Additional control parameters |

### delete_automl_analysis_model

```ruby
delete_automl_analysis_model(analysis_id, model_id, config = {})
```

Deletes a specific model from the given AutoML analysis.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `String` | AutoML analysis ID |
| `model_id` | `String` | AutoML model ID |
| `config` | `Hash` | Additional control parameters |

### delete_email_schedule

```ruby
delete_email_schedule(schedule_id)
```

Delete the specified email schedule.

| Parameter | Type | Description |
|---|---|---|
| `schedule_id` | `String` | ID of the email schedule to delete |

### delete_folder

```ruby
delete_folder(folder_id)
```

Delete a folder.

| Parameter | Type | Description |
|---|---|---|
| `folder_id` | `String` | Folder ID |

### delete_group

```ruby
delete_group(group_id)
```

Delete a group.

| Parameter | Type | Description |
|---|---|---|
| `group_id` | `String` | Group ID |

### delete_slideshow

```ruby
delete_slideshow(slide_id)
```

Delete a slideshow.

| Parameter | Type | Description |
|---|---|---|
| `slide_id` | `String` | Slideshow ID |

### delete_tag

```ruby
delete_tag(tag_id)
```

Delete the specified tag from the workspace.

| Parameter | Type | Description |
|---|---|---|
| `tag_id` | `String` | Id of the tag |

### delete_trash_views

```ruby
delete_trash_views(view_id, config = {})
```

Permanently delete a view from trash.

### delete_variable

```ruby
delete_variable(variable_id)
```

Delete a variable from the workspace.

### deploy_automl_analysis

```ruby
deploy_automl_analysis(analysis_id, deployment_id, config = {})
```

Executes an AutoML analysis deployment.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `String` | AutoML analysis ID |
| `deployment_id` | `String` | Deployment ID |
| `config` | `Hash` | Additional control parameters |

### disable_domain_access

```ruby
disable_domain_access()
```

Disable white-label domain access for the workspace.

### download_workspace_backup

```ruby
download_workspace_backup(backup_id, file_path, config = {})
```

Download the specified workspace backup.

| Parameter | Type | Description |
|---|---|---|
| `backup_id` | `String` | Id of the backup |
| `file_path` | `String` | Path of the file where the downloaded backup is to be stored |
| `config` | `Hash` | Additional control parameters |

### edit_query_table

```ruby
edit_query_table(view_id, sql_query, config = {})
```

Update an existing query table.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `String` | View ID |
| `sql_query` | `String` | New SQL query |
| `config` | `Hash` | Optional config |

### enable_domain_access

```ruby
enable_domain_access()
```

Enable the workspace for white-label domain access.

### export_as_template

```ruby
export_as_template(view_ids, file_path, config = {})
```

Export views as a template file.

| Parameter | Type | Description |
|---|---|---|
| `view_ids` | `Array` | View IDs |
| `file_path` | `String` | Path to save the file |
| `config` | `Hash` | Optional config |

### get_admins

```ruby
get_admins()
```

Get list of admins for the workspace.

**Returns** (`Array`) — Admin details

### get_aggregate_formula_dependents

```ruby
get_aggregate_formula_dependents(formula_id)
```

Returns dependents for a specified aggregate formula.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `String` | aggregate formula ID |

**Returns** (`Hash`) — dependent views and formulas

### get_aggregate_formula_value

```ruby
get_aggregate_formula_value(formula_id)
```

Returns the value of the aggregate formula.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `String` | aggregate formula ID |

**Returns** (`String`) — formula value

### get_aggregate_formulas

```ruby
get_aggregate_formulas(config = {})
```

Returns list of all aggregate formulas for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | optional parameters (default: {}) |

**Returns** (`Array`) — list of aggregate formulas

### get_alert_configuration

```ruby
get_alert_configuration(alert_id)
```

Returns the configuration of the specified data alert.

| Parameter | Type | Description |
|---|---|---|
| `alert_id` | `String` | Id of the data alert |

**Returns** (`Hash`) — Data alert configuration

### get_alert_events

```ruby
get_alert_events(alert_id, config = {})
```

Returns the execution events of the specified data alert.

| Parameter | Type | Description |
|---|---|---|
| `alert_id` | `String` | Id of the data alert |
| `config` | `Hash` | Additional control parameters |

**Returns** (`Hash`) — Data alert events along with the page details

### get_alerts_in_workspace

```ruby
get_alerts_in_workspace()
```

Returns list of data alerts available in the specified workspace.

**Returns** (`Array`) — Data alerts list

### get_automl_analysis

```ruby
get_automl_analysis()
```

Returns all AutoML analyses for the workspace.

**Returns** (`Array`) — AutoML analysis list

### get_automl_analysis_details

```ruby
get_automl_analysis_details(analysis_id)
```

Retrieves detailed information for a specific AutoML analysis.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `String` | AutoML analysis ID |

**Returns** (`Hash`) — AutoML analysis details

### get_dashboard_metadata

```ruby
get_dashboard_metadata(dashboard_id, config = {})
```

Returns the metadata of the specified dashboard.

| Parameter | Type | Description |
|---|---|---|
| `dashboard_id` | `String` | Id of the dashboard |
| `config` | `Hash` | Additional control parameters |

**Returns** (`Hash`) — Dashboard configuration

### get_datasources

```ruby
get_datasources()
```

Get list of data sources.

**Returns** (`Array`) — List of data sources

### get_deployment_details

```ruby
get_deployment_details(analysis_id, model_id)
```

Returns deployment details for an AutoML analysis model.

| Parameter | Type | Description |
|---|---|---|
| `analysis_id` | `String` | AutoML analysis ID |
| `model_id` | `String` | AutoML model ID |

**Returns** (`Array`) — Deployment details

### get_email_schedules

```ruby
get_email_schedules()
```

Returns list of email schedules available in the specified workspace.

**Returns** (`Array`) — list of email schedules

### get_folders

```ruby
get_folders()
```

Returns a list of all accessible folders in the workspace.

**Returns** (`Array`) — Folder list

### get_group_details

```ruby
get_group_details(group_id)
```

Get details for a group.

| Parameter | Type | Description |
|---|---|---|
| `group_id` | `String` | Group ID |

**Returns** (`Hash`) — Group details

### get_groups

```ruby
get_groups()
```

Get groups in the workspace.

**Returns** (`Array`) — Group list

### get_linkable_workspaces

```ruby
get_linkable_workspaces()
```

Returns list of organizations and workspaces that can be linked to the specified master workspace.

**Returns** (`Array`) — Organizations with their linkable workspaces

### get_linked_workspace_sync_details

```ruby
get_linked_workspace_sync_details(sandbox_ids, config = {})
```

Returns the sync details of the specified linked workspaces.

| Parameter | Type | Description |
|---|---|---|
| `sandbox_ids` | `Array` | Ids of the linked workspaces for which the sync details are fetched |
| `config` | `Hash` | Additional control parameters |

**Returns** (`Array`) — Linked workspace sync details

### get_linked_workspaces

```ruby
get_linked_workspaces()
```

Returns list of workspaces linked to the specified master workspace.

**Returns** (`Array`) — Linked workspaces list

### get_query_table_details

```ruby
get_query_table_details(query_table_id)
```

Returns details of the specified query table.

| Parameter | Type | Description |
|---|---|---|
| `query_table_id` | `String` | Query table ID |

**Returns** (`Hash`) — Query table details

### get_query_tables

```ruby
get_query_tables(config = {})
```

Returns list of all query tables for the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | Additional control parameters |

**Returns** (`Array`) — Query table list

### get_report_metadata

```ruby
get_report_metadata(view_id)
```

Returns the metadata of the specified report.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `String` | Id of the report |

**Returns** (`Hash`) — Report configuration

### get_secret_key

```ruby
get_secret_key(config = {})
```

Get the secret key for the workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | Optional config |

**Returns** (`String`) — Secret key

### get_share_info

```ruby
get_share_info()
```

Get workspace share info.

**Returns** (`Hash`) — Share information

### get_shared_details_for_views

```ruby
get_shared_details_for_views(view_ids)
```

Get shared details for the given views.

| Parameter | Type | Description |
|---|---|---|
| `view_ids` | `Array` | View IDs |

**Returns** (`Array`) — Shared detail entries

### get_slideshow_details

```ruby
get_slideshow_details(slide_id)
```

Get slideshow details.

| Parameter | Type | Description |
|---|---|---|
| `slide_id` | `String` | Slideshow ID |

**Returns** (`Hash`) — Slideshow details

### get_slideshow_url

```ruby
get_slideshow_url(slide_id, config = {})
```

Get URL to access a slideshow.

| Parameter | Type | Description |
|---|---|---|
| `slide_id` | `String` | Slideshow ID |
| `config` | `Hash` | Optional config |

**Returns** (`String`) — Published URL

### get_slideshows

```ruby
get_slideshows()
```

Get all slideshows in the workspace.

**Returns** (`Array`) — Slideshow list

### get_tagged_views

```ruby
get_tagged_views(tag_id)
```

Returns the list of views associated with the specified tag.

| Parameter | Type | Description |
|---|---|---|
| `tag_id` | `String` | Id of the tag |

**Returns** (`Array`) — Tagged views list

### get_tags

```ruby
get_tags()
```

Returns list of all tags for the specified workspace.

**Returns** (`Array`) — Tags list

### get_trash_views

```ruby
get_trash_views()
```

Get list of trash views.

**Returns** (`Array`) — Trash views

### get_variable_details

```ruby
get_variable_details(variable_id)
```

Get details of a specific variable.

| Parameter | Type | Description |
|---|---|---|
| `variable_id` | `String` | ID of the variable |

**Returns** (`Hash`) — Variable details

### get_variables

```ruby
get_variables()
```

Get list of variables in the workspace.

**Returns** (`Array`) — List of variables

### get_views

```ruby
get_views(config = {})
```

Get list of all views in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | Optional config |

**Returns** (`Array`) — View list

### get_workspace_access_restrictions

```ruby
get_workspace_access_restrictions()
```

Returns the access restriction settings configured for the specified workspace.

**Returns** (`Hash`) — Workspace access restriction settings

### get_workspace_backup_status

```ruby
get_workspace_backup_status(backup_id)
```

Returns the status of the specified workspace backup.

| Parameter | Type | Description |
|---|---|---|
| `backup_id` | `String` | Id of the backup |

**Returns** (`Hash`) — Backup status details

### get_workspace_backups

```ruby
get_workspace_backups()
```

Returns the backup configuration and the list of backups available for the specified workspace.

**Returns** (`Hash`) — Workspace backup details

### get_workspace_details

```ruby
get_workspace_details(config = {})
```

Returns details of the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | Optional config |

**Returns** (`Hash`) — Workspace details

### get_workspace_linking_compatibility

```ruby
get_workspace_linking_compatibility(clients, config = {})
```

Returns the linking compatibility details for the specified client workspaces.

| Parameter | Type | Description |
|---|---|---|
| `clients` | `Array` | Contains the client workspaces to be verified for linking compatibility |
| `config` | `Hash` | Additional control parameters |

**Returns** (`Array`) — Client workspace compatibility details

### get_workspace_restore_status

```ruby
get_workspace_restore_status(restore_id)
```

Returns the status of the specified workspace restore.

| Parameter | Type | Description |
|---|---|---|
| `restore_id` | `String` | Id of the restore |

**Returns** (`Hash`) — Restore status details

### get_workspace_users

```ruby
get_workspace_users()
```

Get users in the workspace.

**Returns** (`Array`) — User list

### link_workspaces

```ruby
link_workspaces(clients, config = {})
```

Link the specified client workspaces to the master workspace.

| Parameter | Type | Description |
|---|---|---|
| `clients` | `Array` | Contains the client workspaces to be linked with the master workspace |
| `config` | `Hash` | Additional control parameters |

### make_default_folder

```ruby
make_default_folder(folder_id)
```

Mark a folder as default.

### move_views_to_folder

```ruby
move_views_to_folder(folder_id, view_ids, config = {})
```

Move views into a folder.

### remove_admins

```ruby
remove_admins(email_ids, config = {})
```

Remove admins from the workspace.

| Parameter | Type | Description |
|---|---|---|
| `email_ids` | `Array` | Email addresses |
| `config` | `Hash` | Optional config |

### remove_default

```ruby
remove_default()
```

Unset the workspace from default.

### remove_favorite

```ruby
remove_favorite()
```

Unmark the workspace as favorite.

### remove_group_members

```ruby
remove_group_members(group_id, email_ids, config = {})
```

Remove users from a group.

| Parameter | Type | Description |
|---|---|---|
| `group_id` | `String` | Group ID |
| `email_ids` | `Array` | Email list |
| `config` | `Hash` | Optional config |

### remove_share

```ruby
remove_share(view_ids, email_ids, config = {})
```

Remove shared views for specific users.

| Parameter | Type | Description |
|---|---|---|
| `view_ids` | `Array , nil` | View IDs |
| `email_ids` | `Array` | User emails |
| `config` | `Hash` | Optional config |

### remove_tag_from_views

```ruby
remove_tag_from_views(tag_id, view_ids = nil, dissociate_all = false, config = {})
```

Removes the specified tag from multiple views in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `tag_id` | `String` | Id of the tag |
| `view_ids` | `Array , nil` | View ids to be dissociated. Not required when dissociate_all is true. |
| `dissociate_all` | `Boolean` | To dissociate the tag from all associated views |
| `config` | `Hash` | Additional control parameters |

### remove_workspace_users

```ruby
remove_workspace_users(email_ids, config = {})
```

Remove users from the workspace.

### rename

```ruby
rename(workspace_name, config = {})
```

Rename the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `workspace_name` | `String` | New name |
| `config` | `Hash` | Optional config |

### rename_folder

```ruby
rename_folder(folder_id, folder_name, config = {})
```

Rename a folder.

| Parameter | Type | Description |
|---|---|---|
| `folder_id` | `String` | Folder ID |
| `folder_name` | `String` | New name |
| `config` | `Hash` | Optional config |

### rename_group

```ruby
rename_group(group_id, group_name, config = {})
```

Rename a group.

| Parameter | Type | Description |
|---|---|---|
| `group_id` | `String` | Group ID |
| `group_name` | `String` | New name |
| `config` | `Hash` | Optional config |

### restore_trash_views

```ruby
restore_trash_views(view_id, config = {})
```

Restore a view from trash.

### restore_workspace_from_backup

```ruby
restore_workspace_from_backup(backup_id, confirm_restore, config = {})
```

Restore the specified workspace from the given backup.

| Parameter | Type | Description |
|---|---|---|
| `backup_id` | `String` | Id of the backup |
| `confirm_restore` | `Boolean` | Pass true to confirm that the existing workspace data can be overwritten |
| `config` | `Hash` | Additional control parameters |

**Returns** (`Hash`) — Triggered restore details

### run_alert

```ruby
run_alert(alert_id, config = {})
```

Execute the specified data alert immediately.

| Parameter | Type | Description |
|---|---|---|
| `alert_id` | `String` | Id of the data alert |
| `config` | `Hash` | Additional control parameters |

### share_views

```ruby
share_views(view_ids, email_ids, permissions, config = {})
```

Share views to users.

| Parameter | Type | Description |
|---|---|---|
| `view_ids` | `Array` | View IDs to share |
| `email_ids` | `Array` | User emails |
| `permissions` | `Hash` | Permission map |
| `config` | `Hash` | Optional config |

### sync_data

```ruby
sync_data(datasource_id, config = {})
```

Trigger data sync for a data source.

### sync_linked_workspaces

```ruby
sync_linked_workspaces(scope, config = {})
```

Sync the metadata of the master workspace to its linked client workspaces.

| Parameter | Type | Description |
|---|---|---|
| `scope` | `String` | Scope of the sync operation |
| `config` | `Hash` | Additional control parameters |

### trigger_email_schedule

```ruby
trigger_email_schedule(schedule_id)
```

Trigger the configured email schedule instantly.

| Parameter | Type | Description |
|---|---|---|
| `schedule_id` | `String` | ID of the email schedule to trigger |

### unlink_workspaces

```ruby
unlink_workspaces(scope, config = {})
```

Unlink the client workspaces from the specified master workspace.

| Parameter | Type | Description |
|---|---|---|
| `scope` | `String` | Scope of the unlink operation |
| `config` | `Hash` | Additional control parameters |

### update_alert

```ruby
update_alert(alert_id, alert_name, schedule_details, rules, config = {})
```

Update the specified data alert in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `alert_id` | `String` | Id of the data alert |
| `alert_name` | `String` | Name of the data alert |
| `schedule_details` | `Hash` | Contains the schedule configurations of the data alert |
| `rules` | `Array` | Contains the rules to be evaluated by the data alert |
| `config` | `Hash` | Additional control parameters |

### update_dashboard

```ruby
update_dashboard(dashboard_id, config = {})
```

Update the specified dashboard in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `dashboard_id` | `String` | Id of the dashboard |
| `config` | `Hash` | Contains the dashboard configurations to be updated |

### update_datasource_connection

```ruby
update_datasource_connection(datasource_id, config = {})
```

Update data source connection.

### update_email_schedule

```ruby
update_email_schedule(schedule_id, config)
```

Update configurations of the specified email schedule.

| Parameter | Type | Description |
|---|---|---|
| `schedule_id` | `String` | ID of the email schedule to update |
| `config` | `Hash` | configuration parameters to update |

**Returns** (`String`) — updated schedule ID

### update_report

```ruby
update_report(view_id, config = {})
```

Update the design and configuration of the specified report.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `String` | ID of the report view |
| `config` | `Hash` | configuration parameters |

### update_slideshow

```ruby
update_slideshow(slide_id, config = {})
```

Update a slideshow.

| Parameter | Type | Description |
|---|---|---|
| `slide_id` | `String` | Slideshow ID |
| `config` | `Hash` | Update data |

### update_tag

```ruby
update_tag(tag_id, config = {})
```

Update details of the specified tag in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `tag_id` | `String` | Id of the tag |
| `config` | `Hash` | Control parameters |

### update_variable

```ruby
update_variable(variable_id, variable_name, variable_datatype, variable_type, config = {})
```

Update a variable in the workspace.

### update_workspace_access_restrictions

```ruby
update_workspace_access_restrictions(config = {})
```

Update the access restriction settings of the specified workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | Contains the access restriction configurations to be updated |

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
