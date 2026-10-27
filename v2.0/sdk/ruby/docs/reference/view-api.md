# ViewAPI

```ruby
org       = ac.get_org_instance(ORG_ID)
workspace = ac.get_workspace_instance(ORG_ID, WORKSPACE_ID)
view      = ac.get_view_instance(ORG_ID, WORKSPACE_ID, VIEW_ID)
bulk      = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)
```

`ViewAPI` exposes **51 methods**. Method names are `snake_case` and identifiers are `string`.

## Methods

[`add_aggregate_formula`](#add-aggregate-formula), [`add_column`](#add-column), [`add_favorite`](#add-favorite), [`add_formula_column`](#add-formula-column), [`add_lookup`](#add-lookup), [`add_row`](#add-row), [`add_tags_to_view`](#add-tags-to-view), [`auto_analyse`](#auto-analyse), [`auto_analyse_column`](#auto-analyse-column), [`copy_formulas`](#copy-formulas), [`create_alert`](#create-alert), [`create_private_url`](#create-private-url), [`create_similar_views`](#create-similar-views), [`delete`](#delete), [`delete_aggregate_formula`](#delete-aggregate-formula), [`delete_column`](#delete-column), [`delete_formula_column`](#delete-formula-column), [`delete_row`](#delete-row), [`edit_aggregate_formula`](#edit-aggregate-formula), [`edit_formula_column`](#edit-formula-column), [`get_aggregate_formulas`](#get-aggregate-formulas), [`get_alerts_in_view`](#get-alerts-in-view), [`get_column_dependents`](#get-column-dependents), [`get_embed_url`](#get-embed-url), [`get_formula_columns`](#get-formula-columns), [`get_last_import_details`](#get-last-import-details), [`get_my_permissions`](#get-my-permissions), [`get_private_url`](#get-private-url), [`get_publish_configurations`](#get-publish-configurations), [`get_table_metadata`](#get-table-metadata), [`get_view_dependents`](#get-view-dependents), [`get_view_metadata_for_alert`](#get-view-metadata-for-alert), [`get_view_tags`](#get-view-tags), [`get_view_url`](#get-view-url), [`hide_columns`](#hide-columns), [`make_view_public`](#make-view-public), [`refetch_data`](#refetch-data), [`remove_favorite`](#remove-favorite), [`remove_lookup`](#remove-lookup), [`remove_private_access`](#remove-private-access), [`remove_public_access`](#remove-public-access), [`remove_tags_from_view`](#remove-tags-from-view), [`rename`](#rename), [`rename_column`](#rename-column), [`reorder_columns`](#reorder-columns), [`save_as`](#save-as), [`show_columns`](#show-columns), [`sort_data_by_columns`](#sort-data-by-columns), [`update_publish_configurations`](#update-publish-configurations), [`update_row`](#update-row), [`update_shared_details`](#update-shared-details)

### add_aggregate_formula

```ruby
add_aggregate_formula(formula_name, expression, config = {})
```

Adds an aggregate formula to the table.

| Parameter | Type | Description |
|---|---|---|
| `formula_name` | `String` | Formula name. |
| `expression` | `String` | Formula expression. |
| `config` | `Hash` | Additional control parameters. |

**Returns** (`String`) — Formula ID.

### add_column

```ruby
add_column(column_name, data_type, config = {})
```

Add a column to the view.

| Parameter | Type | Description |
|---|---|---|
| `column_name` | `String` | — |
| `data_type` | `String` | — |
| `config` | `Hash` | — |

**Returns** (`Integer`) — Integer

### add_favorite

```ruby
add_favorite()
```

Adds a specified view as favorite.

### add_formula_column

```ruby
add_formula_column(formula_name, expression, config = {})
```

Adds a formula column to the table.

| Parameter | Type | Description |
|---|---|---|
| `formula_name` | `String` | Name of the formula column. |
| `expression` | `String` | Formula expression. |
| `config` | `Hash` | Additional control parameters. |

**Returns** (`String`) — Formula ID.

### add_lookup

```ruby
add_lookup(column_id, ref_view_id, ref_column_id, config = {})
```

Adds a lookup in the specified child table.

| Parameter | Type | Description |
|---|---|---|
| `column_id` | `String` | Child column ID. |
| `ref_view_id` | `String` | Parent table ID. |
| `ref_column_id` | `String` | Parent column ID. |
| `config` | `Hash` | Additional control parameters. |

### add_row

```ruby
add_row(column_values, config = {})
```

Adds a single row in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `column_values` | `Hash` | Column name to value mapping. |
| `config` | `Hash` | Additional control parameters. |

**Returns** (`Hash`) — Response containing column names and added row values.

### add_tags_to_view

```ruby
add_tags_to_view(tag_ids, config = {})
```

Adds multiple tags to the specified view.

| Parameter | Type | Description |
|---|---|---|
| `tag_ids` | `Array` | Tag ids to be associated with the view |
| `config` | `Hash` | Additional control parameters |

### auto_analyse

```ruby
auto_analyse(config = {})
```

Auto generate reports.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | — |

### auto_analyse_column

```ruby
auto_analyse_column(column_id, config = {})
```

Auto generates reports for the specified column.

| Parameter | Type | Description |
|---|---|---|
| `column_id` | `String` | Column ID. |
| `config` | `Hash` | Additional control parameters. |

### copy_formulas

```ruby
copy_formulas(formula_names, dest_workspace_id, config = {}, dest_org_id = nil)
```

Copy formulas to another workspace or view.

| Parameter | Type | Description |
|---|---|---|
| `formula_names` | `Array` | Names of formulas |
| `dest_workspace_id` | `String` | Destination workspace ID |
| `config` | `Hash` | Additional control parameters |
| `dest_org_id` | `String, nil` | Optional destination org ID |

### create_alert

```ruby
create_alert(alert_name, schedule_details, rules, config = {})
```

Create a data alert for the specified view.

| Parameter | Type | Description |
|---|---|---|
| `alert_name` | `String` | Name of the data alert |
| `schedule_details` | `Hash` | Contains the schedule configurations of the data alert |
| `rules` | `Array` | Contains the rules to be evaluated by the data alert |
| `config` | `Hash` | Additional control parameters |

**Returns** (`String`) — Created data alert id

### create_private_url

```ruby
create_private_url(config = {})
```

Create private URL for the view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | — |

**Returns** (`String`) — String

### create_similar_views

```ruby
create_similar_views(ref_view_id, folder_id, config = {})
```

Create similar reports based on a reference view.

| Parameter | Type | Description |
|---|---|---|
| `ref_view_id` | `String` | — |
| `folder_id` | `String` | — |
| `config` | `Hash` | — |

### delete

```ruby
delete(config = {})
```

Delete a specified view in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | Additional control parameters |

### delete_aggregate_formula

```ruby
delete_aggregate_formula(formula_id, config = {})
```

Deletes an aggregate formula.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `String` | Formula ID. |
| `config` | `Hash` | Additional control parameters. |

### delete_column

```ruby
delete_column(column_id, config = {})
```

Deletes a specified column in the table.

| Parameter | Type | Description |
|---|---|---|
| `column_id` | `String` | ID of the column. |
| `config` | `Hash` | Additional control parameters. |

### delete_formula_column

```ruby
delete_formula_column(formula_id, config = {})
```

Deletes a formula column.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `String` | Formula column ID. |
| `config` | `Hash` | Additional control parameters. |

### delete_row

```ruby
delete_row(criteria, config = {})
```

Deletes rows in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `criteria` | `String, nil` | Criteria to filter rows for deletion. |
| `config` | `Hash` | Additional control parameters. |

**Returns** (`String`) — Deleted row details.

### edit_aggregate_formula

```ruby
edit_aggregate_formula(formula_id, expression, config = {})
```

Edits an aggregate formula.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `String` | Formula ID. |
| `expression` | `String` | New formula expression. |
| `config` | `Hash` | Additional control parameters. |

### edit_formula_column

```ruby
edit_formula_column(formula_id, expression, config = {})
```

Edits a formula column.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `String` | Formula column ID. |
| `expression` | `String` | New formula expression. |
| `config` | `Hash` | Additional control parameters. |

### get_aggregate_formulas

```ruby
get_aggregate_formulas()
```

Returns list of all aggregate formulas for the table.

**Returns** (`Array`) — Aggregate formulas.

### get_alerts_in_view

```ruby
get_alerts_in_view()
```

Returns list of data alerts configured for the specified view.

**Returns** (`Array`) — Data alerts list

### get_column_dependents

```ruby
get_column_dependents(column_id)
```

Returns list of dependent views and formulas for the specified column.

| Parameter | Type | Description |
|---|---|---|
| `column_id` | `String` | The ID of the column |

**Returns** (`Hash`) — Dependent details

### get_embed_url

```ruby
get_embed_url(config = {})
```

Get embed URL of the view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | — |

**Returns** (`String`) — String

### get_formula_columns

```ruby
get_formula_columns()
```

Returns list of all formula columns for the table.

**Returns** (`Array`) — Formula columns.

### get_last_import_details

```ruby
get_last_import_details()
```

Returns last import details of the view.

**Returns** (`Hash`) — Last import details.

### get_my_permissions

```ruby
get_my_permissions()
```

Get user permissions for the view.

**Returns** (`Hash`) — Hash

### get_private_url

```ruby
get_private_url(config = {})
```

Get private URL of the view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | — |

**Returns** (`String`) — String

### get_publish_configurations

```ruby
get_publish_configurations()
```

Get publish configurations of the view.

**Returns** (`Hash`) — Hash

### get_table_metadata

```ruby
get_table_metadata()
```

Returns metadata details like columns present for the specified table.

**Returns** (`Hash`) — Table metadata details

### get_view_dependents

```ruby
get_view_dependents()
```

Returns the dependent views of this view.

**Returns** (`Array`) — List of dependent views.

### get_view_metadata_for_alert

```ruby
get_view_metadata_for_alert()
```

Returns the view metadata that can be used while configuring a data alert for the specified view.

**Returns** (`Hash`) — View metadata for data alert configuration

### get_view_tags

```ruby
get_view_tags()
```

Returns the list of tags associated with the specified view.

**Returns** (`Array`) — Tags list

### get_view_url

```ruby
get_view_url(config = {})
```

Get the URL to access the view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | — |

**Returns** (`String`) — String

### hide_columns

```ruby
hide_columns(column_ids)
```

Hide columns in the view.

| Parameter | Type | Description |
|---|---|---|
| `column_ids` | `Array` | — |

### make_view_public

```ruby
make_view_public(config = {})
```

Make the view publicly accessible.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | — |

**Returns** (`String`) — String

### refetch_data

```ruby
refetch_data(config = {})
```

Syncs data from the available data source for the view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | Additional control parameters. |

### remove_favorite

```ruby
remove_favorite()
```

Removes a specified view from favorites.

### remove_lookup

```ruby
remove_lookup(column_id, config = {})
```

Removes the lookup for the specified column in the table.

| Parameter | Type | Description |
|---|---|---|
| `column_id` | `String` | Column ID. |
| `config` | `Hash` | Additional control parameters. |

### remove_private_access

```ruby
remove_private_access()
```

Remove private access for the view.

### remove_public_access

```ruby
remove_public_access()
```

Remove public access for the view.

### remove_tags_from_view

```ruby
remove_tags_from_view(tag_ids = nil, dissociate_all = false, config = {})
```

Removes multiple tags from the specified view.

| Parameter | Type | Description |
|---|---|---|
| `tag_ids` | `Array , nil` | Tag ids to be dissociated. Not required when dissociate_all is true. |
| `dissociate_all` | `Boolean` | To dissociate all tags from the view |
| `config` | `Hash` | Additional control parameters |

### rename

```ruby
rename(view_name, config = {})
```

Rename a specified view in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `view_name` | `String` | New name of the view |
| `config` | `Hash` | Additional control parameters |

### rename_column

```ruby
rename_column(column_id, column_name, config = {})
```

Renames a specified column in the table.

| Parameter | Type | Description |
|---|---|---|
| `column_id` | `String` | ID of the column. |
| `column_name` | `String` | New column name. |
| `config` | `Hash` | Additional control parameters. |

### reorder_columns

```ruby
reorder_columns(column_ids, config = {})
```

Updates the column order of the current table.

| Parameter | Type | Description |
|---|---|---|
| `column_ids` | `Array` | List of column IDs in the new order |
| `config` | `Hash` | Additional control parameters |

### save_as

```ruby
save_as(new_view_name, config = {})
```

Copy a specified view within the workspace.

| Parameter | Type | Description |
|---|---|---|
| `new_view_name` | `String` | Name of the new view |
| `config` | `Hash` | Additional control parameters |

**Returns** (`Integer`) — Created view ID

### show_columns

```ruby
show_columns(column_ids)
```

Show hidden columns in the view.

| Parameter | Type | Description |
|---|---|---|
| `column_ids` | `Array` | — |

### sort_data_by_columns

```ruby
sort_data_by_columns(columns = nil, sort_order = nil, reset_sort = false, config = {})
```

Sorts the data in the current table based on the specified columns.

| Parameter | Type | Description |
|---|---|---|
| `columns` | `Array , nil` | Column IDs to sort by |
| `sort_order` | `Integer, nil` | Sort order (1 = Ascending, 2 = Descending) |
| `reset_sort` | `Boolean` | Whether to reset existing sort configuration |
| `config` | `Hash` | Additional control parameters |

### update_publish_configurations

```ruby
update_publish_configurations(config = {})
```

Update publish configurations of the view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | — |

### update_row

```ruby
update_row(column_values, criteria, config = {})
```

Updates rows in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `column_values` | `Hash` | Column name to updated value mapping. |
| `criteria` | `String, nil` | Criteria to filter rows for update. |
| `config` | `Hash` | Additional control parameters. |

**Returns** (`Hash`) — Updated columns list and row count.

### update_shared_details

```ruby
update_shared_details(config = {})
```

Updates the shared details of the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Hash` | Contains the control parameters |

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
