# ViewAPI

```python
org       = ac.get_org_instance(ORG_ID)
workspace = ac.get_workspace_instance(ORG_ID, WORKSPACE_ID)
view      = ac.get_view_instance(ORG_ID, WORKSPACE_ID, VIEW_ID)
bulk      = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)
```

`ViewAPI` exposes **51 methods**. Method names are `snake_case` and identifiers are `str`.

## Methods

[`add_aggregate_formula`](#add-aggregate-formula), [`add_column`](#add-column), [`add_favorite`](#add-favorite), [`add_formula_column`](#add-formula-column), [`add_lookup`](#add-lookup), [`add_row`](#add-row), [`add_tags_to_view`](#add-tags-to-view), [`auto_analyse`](#auto-analyse), [`auto_analyse_column`](#auto-analyse-column), [`copy_formulas`](#copy-formulas), [`create_alert`](#create-alert), [`create_private_url`](#create-private-url), [`create_similar_views`](#create-similar-views), [`delete`](#delete), [`delete_aggregate_formula`](#delete-aggregate-formula), [`delete_column`](#delete-column), [`delete_formula_column`](#delete-formula-column), [`delete_row`](#delete-row), [`edit_aggregate_formula`](#edit-aggregate-formula), [`edit_formula_column`](#edit-formula-column), [`get_aggregate_formulas`](#get-aggregate-formulas), [`get_alerts_in_view`](#get-alerts-in-view), [`get_column_dependents`](#get-column-dependents), [`get_embed_url`](#get-embed-url), [`get_formula_columns`](#get-formula-columns), [`get_last_import_details`](#get-last-import-details), [`get_my_permissions`](#get-my-permissions), [`get_private_url`](#get-private-url), [`get_publish_configurations`](#get-publish-configurations), [`get_table_metadata`](#get-table-metadata), [`get_view_dependents`](#get-view-dependents), [`get_view_metadata_for_alert`](#get-view-metadata-for-alert), [`get_view_tags`](#get-view-tags), [`get_view_url`](#get-view-url), [`hide_columns`](#hide-columns), [`make_view_public`](#make-view-public), [`refetch_data`](#refetch-data), [`remove_favorite`](#remove-favorite), [`remove_lookup`](#remove-lookup), [`remove_private_access`](#remove-private-access), [`remove_public_access`](#remove-public-access), [`remove_tags_from_view`](#remove-tags-from-view), [`rename`](#rename), [`rename_column`](#rename-column), [`reorder_columns`](#reorder-columns), [`save_as`](#save-as), [`show_columns`](#show-columns), [`sort_data_by_columns`](#sort-data-by-columns), [`update_publish_configurations`](#update-publish-configurations), [`update_row`](#update-row), [`update_shared_details`](#update-shared-details)

### add_aggregate_formula

```python
add_aggregate_formula(formula_name, expression, config = {})
```

Add an aggregate formula in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `formula_name` | `string` | Name of the aggregate formula to be created. |
| `expression` | `string` | Formula expression. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Created formula id.

**Raises** — `ServerError`; `ParseError`

### add_column

```python
add_column(column_name, data_type, config = {})
```

Add a column in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `column_name` | `string` | The name of the column. |
| `data_type` | `string` | The data-type of the column. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Created column id.

**Raises** — `ServerError`; `ParseError`

### add_favorite

```python
add_favorite()
```

Adds a specified view as favorite.

**Raises** — `ServerError`; `ParseError`

### add_formula_column

```python
add_formula_column(formula_name, expression, config = {})
```

Add a formula column in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `formula_name` | `string` | Name of the formula column to be created. |
| `expression` | `string` | Formula expression. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Created formula id.

**Raises** — `ServerError`; `ParseError`

### add_lookup

```python
add_lookup(column_id, ref_view_id, ref_column_id, config = {})
```

Add a lookup in the specified child table.

| Parameter | Type | Description |
|---|---|---|
| `column_id` | `string` | Id of the column. |
| `ref_view_id` | `string` | The id of the table contains the parent column. |
| `ref_column_id` | `string` | The id of the parent column. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### add_row

```python
add_row(column_values, config = {})
```

Add a single row in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `column_values` | `dictionary` | Contains the values for the row. The column names are the key. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`dictionary`) — Column Names and Added Row Values.

**Raises** — `ServerError`; `ParseError`

### add_tags_to_view

```python
add_tags_to_view(tag_ids, config = {})
```

Adds multiple tags to the specified view.

| Parameter | Type | Description |
|---|---|---|
| `tag_ids` | `list` | Tag ids to be associated with the view. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### auto_analyse

```python
auto_analyse(config = {})
```

Auto generate reports for the specified table.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### auto_analyse_column

```python
auto_analyse_column(column_id, config = {})
```

Auto generate reports for the specified column.

| Parameter | Type | Description |
|---|---|---|
| `column_id` | `string` | Id of the column. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### copy_formulas

```python
copy_formulas(formula_names, dest_workspace_id, config = {}, dest_org_id = None)
```

Copy the specified formulas from one table to another within the workspace or across workspaces.

| Parameter | Type | Description |
|---|---|---|
| `formula_names` | `list` | The name of the formula columns to be copied. |
| `dest_workspace_id` | `string` | The ID of the destination workspace. |
| `dest_org_id` | `string` | Id of the organization where the destination workspace is present. Can be `null`. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### create_alert

```python
create_alert(alert_name, schedule_details, rules, config = {})
```

Create a data alert for the specified view.

| Parameter | Type | Description |
|---|---|---|
| `alert_name` | `string` | Name of the data alert. |
| `schedule_details` | `dictionary` | Contains the schedule configurations of the data alert. |
| `rules` | `list` | Contains the rules to be evaluated by the data alert. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Created data alert id.

**Raises** — `ServerError`; `ParseError`

### create_private_url

```python
create_private_url(config = {})
```

Create a private URL for the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Private URL.

**Raises** — `ServerError`; `ParseError`

### create_similar_views

```python
create_similar_views(ref_view_id, folder_id, config = {})
```

Create reports for the specified table based on the reference table.

| Parameter | Type | Description |
|---|---|---|
| `ref_view_id` | `string` | The ID of the reference view. |
| `folder_id` | `string` | The folder id where the views to be saved. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### delete

```python
delete(config = {})
```

Delete a specified view in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### delete_aggregate_formula

```python
delete_aggregate_formula(formula_id, config = {})
```

Delete the specified aggregate formula.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `string` | Id of the aggregate formula to be deleted. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### delete_column

```python
delete_column(column_id, config = {})
```

Delete a specified column in the table.

| Parameter | Type | Description |
|---|---|---|
| `column_id` | `string` | Id of the column. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### delete_formula_column

```python
delete_formula_column(formula_id, config = {})
```

Delete the specified formula column.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `string` | Id of the formula column to be deleted. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### delete_row

```python
delete_row(criteria, config = {})
```

Delete rows in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `criteria` | `string` | The criteria to be applied for deleting data. Only rows matching the criteria will be deleted. Should be null for delete all rows. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Deleted rows details.

**Raises** — `ServerError`; `ParseError`

### edit_aggregate_formula

```python
edit_aggregate_formula(formula_id, expression, config = {})
```

Edit the specified aggregate formula.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `string` | Id of the aggregate formula to be updated. |
| `expression` | `string` | Formula expression. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### edit_formula_column

```python
edit_formula_column(formula_id, expression, config = {})
```

Edit the specified formula column.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `string` | Id of the formula column to be updated. |
| `expression` | `string` | Formula expression. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### get_aggregate_formulas

```python
get_aggregate_formulas()
```

Returns list of all aggregate formulas for the specified table.

**Returns** (`list`) — Aggregate Formula list.

**Raises** — `ServerError`; `ParseError`

### get_alerts_in_view

```python
get_alerts_in_view()
```

Returns list of data alerts configured for the specified view.

**Returns** (`list`) — Data alerts list.

**Raises** — `ServerError`; `ParseError`

### get_column_dependents

```python
get_column_dependents(column_id)
```

Returns list of dependents views and formulas for the specified column.

**Returns** (`dictionary`) — Dependent details.

**Raises** — `ServerError`; `ParseError`

### get_embed_url

```python
get_embed_url(config = {})
```

Returns embed URL to access the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Embed URL.

**Raises** — `ServerError`; `ParseError`

### get_formula_columns

```python
get_formula_columns()
```

Returns list of all formula columns for the specified table.

**Returns** (`list`) — Formula column list.

**Raises** — `ServerError`; `ParseError`

### get_last_import_details

```python
get_last_import_details()
```

Returns last import details of the specified view.

**Returns** (`dictionary`) — Last import details.

**Raises** — `ServerError`; `ParseError`

### get_my_permissions

```python
get_my_permissions()
```

Returns permissions for the specified view.

**Returns** (`dictionary`) — Permission details.

**Raises** — `ServerError`; `ParseError`

### get_private_url

```python
get_private_url(config = {})
```

Returns private URL to access the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Private URL.

**Raises** — `ServerError`; `ParseError`

### get_publish_configurations

```python
get_publish_configurations()
```

Returns publish configurations for the specified view.

**Returns** (`dictionary`) — Publish details.

**Raises** — `ServerError`; `ParseError`

### get_table_metadata

```python
get_table_metadata()
```

Retrieves metadata information for the current table, including the list of available columns and associated attributes. Returns metadata information like columns present for the specified table.

**Returns** (`dictionary`) — Table metadata details.

**Raises** — `ServerError`; `ParseError`

### get_view_dependents

```python
get_view_dependents()
```

Returns list of dependents views for the specified view.

**Returns** (`list`) — Dependent view list.

**Raises** — `ServerError`; `ParseError`

### get_view_metadata_for_alert

```python
get_view_metadata_for_alert()
```

Returns the view metadata that can be used while configuring a data alert for the specified view.

**Returns** (`dictionary`) — View metadata for data alert configuration.

**Raises** — `ServerError`; `ParseError`

### get_view_tags

```python
get_view_tags()
```

Returns list of tags associated with the specified view.

**Returns** (`list`) — Tags list.

**Raises** — `ServerError`; `ParseError`

### get_view_url

```python
get_view_url(config = {})
```

Returns the URL to access the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — View URL.

**Raises** — `ServerError`; `ParseError`

### hide_columns

```python
hide_columns(column_ids)
```

Hide the specified columns in the table.

| Parameter | Type | Description |
|---|---|---|
| `column_ids` | `list` | Ids of the columns to be hidden. |

**Raises** — `ServerError`; `ParseError`

### make_view_public

```python
make_view_public(config = {})
```

Make the specified view publically accessible.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Public URL.

**Raises** — `ServerError`; `ParseError`

### refetch_data

```python
refetch_data(config = {})
```

Sync data from available datasource for the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### remove_favorite

```python
remove_favorite()
```

Remove a specified view from favorite.

**Raises** — `ServerError`; `ParseError`

### remove_lookup

```python
remove_lookup(column_id, config = {})
```

Remove the lookup for the specified column in the table.

| Parameter | Type | Description |
|---|---|---|
| `column_id` | `string` | Id of the column. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### remove_private_access

```python
remove_private_access()
```

Remove private link access for the specified view.

**Raises** — `ServerError`; `ParseError`

### remove_public_access

```python
remove_public_access()
```

Remove public access for the specified view.

**Raises** — `ServerError`; `ParseError`

### remove_tags_from_view

```python
remove_tags_from_view(tag_ids = None, dissociate_all = False, config = {})
```

Removes multiple tags from the specified view.

| Parameter | Type | Description |
|---|---|---|
| `tag_ids` | `list` | Tag ids to be dissociated. Not required when dissociate_all is True. |
| `dissociate_all` | `boolean` | To dissociate all the associated tags from the view. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### rename

```python
rename(view_name, config = {})
```

Rename a specified view in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `view_name` | `string` | New name of the view. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### rename_column

```python
rename_column(column_id, column_name, config = {})
```

Rename a specified column in the table.

| Parameter | Type | Description |
|---|---|---|
| `column_id` | `string` | Id of the column. |
| `column_name` | `string` | New name for the column. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### reorder_columns

```python
reorder_columns(column_ids, config = {})
```

Updates the column order of the current table.

| Parameter | Type | Description |
|---|---|---|
| `column_ids` | `list` | A list containing the full set of column IDs in the new order in which they should appear. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### save_as

```python
save_as(new_view_name, config = {})
```

Copy a specified view within the workspace.

| Parameter | Type | Description |
|---|---|---|
| `new_view_name` | `string` | The name of the new view. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Created view id.

**Raises** — `ServerError`; `ParseError`

### show_columns

```python
show_columns(column_ids)
```

Show the specified hidden columns in the table.

| Parameter | Type | Description |
|---|---|---|
| `column_ids` | `list` | Ids of the columns to be shown. |

**Raises** — `ServerError`; `ParseError`

### sort_data_by_columns

```python
sort_data_by_columns(columns=None, sort_order=None, reset_sort=False, config={})
```

Sorts the data in the provided table based on the specified columns.

| Parameter | Type | Description |
|---|---|---|
| `columns` | `list` | A list of column IDs to sort by. |
| `sort_order` | `int` | Sorting order indicator. |
| `reset_sort` | `boolean` | If True, resets any existing sort configuration before applying new sort. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### update_publish_configurations

```python
update_publish_configurations(config = {})
```

Update publish configurations for the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains the control parameters. |

**Raises** — `ServerError`; `ParseError`

### update_row

```python
update_row(column_values, criteria, config = {})
```

Update rows in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `column_values` | `dictionary` | Contains the values for the row. The column names are the key. |
| `criteria` | `string` | The criteria to be applied for updating data. Only rows matching the criteria will be updated. Should be null for update all rows. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`dictionary`) — Updated Columns List and Updated Rows Count.

**Raises** — `ServerError`; `ParseError`

### update_shared_details

```python
update_shared_details(config = {})
```

Update shared details of the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `dictionary` | Contains the control parameters. |

**Raises** — `ServerError`; `ParseError`

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
