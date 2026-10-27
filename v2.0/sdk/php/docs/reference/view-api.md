# ViewAPI

```php
$org       = $ac->getOrgInstance($org_id);
$workspace = $ac->getWorkspaceInstance($org_id, $workspace_id);
$view      = $ac->getViewInstance($org_id, $workspace_id, $view_id);
$bulk      = $ac->getBulkInstance($org_id, $workspace_id);
```

`ViewAPI` exposes **51 methods**. Method names are `camelCase` and identifiers are `string`.

## Methods

[`addAggregateFormula`](#addaggregateformula), [`addColumn`](#addcolumn), [`addFavorite`](#addfavorite), [`addFormulaColumn`](#addformulacolumn), [`addRow`](#addrow), [`addTagsToView`](#addtagstoview), [`autoAnalyse`](#autoanalyse), [`autoAnalyseColumn`](#autoanalysecolumn), [`copyFormulas`](#copyformulas), [`createAlert`](#createalert), [`createLookup`](#createlookup), [`createPrivateURL`](#createprivateurl), [`createSimilarViews`](#createsimilarviews), [`delete`](#delete), [`deleteAggregateFormula`](#deleteaggregateformula), [`deleteColumn`](#deletecolumn), [`deleteFormulaColumn`](#deleteformulacolumn), [`deleteRow`](#deleterow), [`editAggregateFormula`](#editaggregateformula), [`editFormulaColumn`](#editformulacolumn), [`getAggregateFormulas`](#getaggregateformulas), [`getAlertsInView`](#getalertsinview), [`getColumnDependents`](#getcolumndependents), [`getEmbedURL`](#getembedurl), [`getFormulaColumns`](#getformulacolumns), [`getLastImportDetails`](#getlastimportdetails), [`getMyPermissions`](#getmypermissions), [`getPrivateURL`](#getprivateurl), [`getPublishConfigurations`](#getpublishconfigurations), [`getTableMetadata`](#gettablemetadata), [`getViewDependents`](#getviewdependents), [`getViewMetadataForAlert`](#getviewmetadataforalert), [`getViewTags`](#getviewtags), [`getViewURL`](#getviewurl), [`hideColumns`](#hidecolumns), [`makeViewPublic`](#makeviewpublic), [`refetchData`](#refetchdata), [`removeFavorite`](#removefavorite), [`removeLookup`](#removelookup), [`removePrivateAccess`](#removeprivateaccess), [`removePublicAccess`](#removepublicaccess), [`removeTagsFromView`](#removetagsfromview), [`rename`](#rename), [`renameColumn`](#renamecolumn), [`reorderColumns`](#reordercolumns), [`saveAs`](#saveas), [`showColumns`](#showcolumns), [`sortDataByColumns`](#sortdatabycolumns), [`updatePublishConfigurations`](#updatepublishconfigurations), [`updateRow`](#updaterow), [`updateSharedDetails`](#updateshareddetails)

### addAggregateFormula

```php
addAggregateFormula($formula_name, $expression, $config = array()
```

Add an aggregate formula in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `formula_name` | `string` | Name of the aggregate formula to be created. |
| `expression` | `string` | Formula expression. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Created column id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### addColumn

```php
addColumn($column_name, $data_type, $config = array()
```

Add a column in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `column_name` | `string` | The name of the column. |
| `data_type` | `string` | The data-type of the column. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Created column id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### addFavorite

```php
addFavorite()
```

Adds a specified view as favorite.

**Raises** — `IOException`; `ServerException`; `ParseException`

### addFormulaColumn

```php
addFormulaColumn($formula_name, $expression, $config = array()
```

Add a formula column in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `formula_name` | `string` | Name of the formula column to be created. |
| `expression` | `string` | Formula expression. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Created column id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### addRow

```php
addRow($column_values, $config = array()
```

Add a single row in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `column_values` | `array()` | Contains the values for the row. The column names are the key. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Column Names and Added Row Values.

**Raises** — `IOException`; `ServerException`; `ParseException`

### addTagsToView

```php
addTagsToView($tag_ids, $config = array()
```

Adds multiple tags to the specified view.

| Parameter | Type | Description |
|---|---|---|
| `tag_ids` | `array()` | Tag ids to be associated with the view. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

### autoAnalyse

```php
autoAnalyse($config = array()
```

Auto generate reports for the specified table.

| Parameter | Type | Description |
|---|---|---|
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### autoAnalyseColumn

```php
autoAnalyseColumn($column_id, $config = array()
```

Auto generate reports for the specified column.

| Parameter | Type | Description |
|---|---|---|
| `column_id` | `string` | Id of the column. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### copyFormulas

```php
copyFormulas($formulaNames, $dest_workspace_id, $config = array()
```

Copy the specified formulas from one table to another within the workspace or across workspaces.

| Parameter | Type | Description |
|---|---|---|
| `formulaNames` | `string` | The name of the formula columns to be copied. |
| `dest_workspace_id` | `string` | The id of the destination workspace. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |
| `dest_org_id` | `string` | Id of the organization where the destination workspace is present. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### createAlert

```php
createAlert($alert_name, $schedule_details, $rules, $config = array()
```

Create a data alert for the specified view.

| Parameter | Type | Description |
|---|---|---|
| `alert_name` | `string` | Name of the data alert. |
| `schedule_details` | `array()` | Contains the schedule configurations of the data alert. |
| `rules` | `array()` | Contains the rules to be evaluated by the data alert. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Created data alert id.

### createLookup

```php
createLookup($column_id, $ref_view_id, $ref_column_id, $config = array()
```

Add a lookup in the specified child table.

| Parameter | Type | Description |
|---|---|---|
| `column_id` | `string` | Id of the column. |
| `ref_view_id` | `string` | The id of the table contains the parent column. |
| `ref_column_id` | `string` | The id of the parent column. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### createPrivateURL

```php
createPrivateURL($config = array()
```

Create a private URL for the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — private URL.

**Raises** — `IOException`; `ServerException`; `ParseException`

### createSimilarViews

```php
createSimilarViews($ref_view_id, $folder_id, $config = array()
```

Create reports for the specified table based on the reference table.

| Parameter | Type | Description |
|---|---|---|
| `ref_view_id` | `string` | The ID of the reference view. |
| `folder_id` | `string` | The folder id where the views to be saved. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### delete

```php
delete($config = array()
```

Delete a specified view in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### deleteAggregateFormula

```php
deleteAggregateFormula($formula_id, $config = array()
```

Delete the specified aggregate formula.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `string` | Id of the aggregate formula to be deleted. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### deleteColumn

```php
deleteColumn($column_id, $config = array()
```

Delete a specified column in the table.

| Parameter | Type | Description |
|---|---|---|
| `column_id` | `string` | Id of the column. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### deleteFormulaColumn

```php
deleteFormulaColumn($formula_id, $config = array()
```

Delete the specified formula column.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `string` | Id of the formula column to be deleted. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### deleteRow

```php
deleteRow($criteria, $config = array()
```

Delete rows in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `criteria` | `array()` | The criteria to be applied for deleting data. Only rows matching the criteria will be deleted. Should be null for delete all rows. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Deleted rows count.

**Raises** — `IOException`; `ServerException`; `ParseException`

### editAggregateFormula

```php
editAggregateFormula($formula_id, $expression, $config = array()
```

Edit the specified aggregate formula.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `string` | Id of the aggregate formula to be updated. |
| `expression` | `string` | Formula expression. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### editFormulaColumn

```php
editFormulaColumn($formula_id, $expression, $config = array()
```

Edit the specified formula column.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `string` | Id of the formula column to be updated. |
| `expression` | `string` | Formula expression. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### getAggregateFormulas

```php
getAggregateFormulas()
```

Returns list of all aggregate formulas for the specified table.

**Returns** — Aggregate formula list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getAlertsInView

```php
getAlertsInView()
```

Returns list of data alerts configured for the specified view.

**Returns** — Data alerts list.

### getColumnDependents

```php
getColumnDependents($column_id)
```

Returns dependent details for the specified column.

| Parameter | Type | Description |
|---|---|---|
| `formula_id` | `string` | Id of the formula column to be updated. |

**Returns** — Dependent details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getEmbedURL

```php
getEmbedURL($config = array()
```

Returns embed URL to access the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Embed URL.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getFormulaColumns

```php
getFormulaColumns()
```

Returns list of all formula columns for the specified table.

**Returns** — Formula column list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getLastImportDetails

```php
getLastImportDetails()
```

Returns last import details of the specified view.

**Returns** — Last data import details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getMyPermissions

```php
getMyPermissions()
```

Returns permissions for the specified view.

**Returns** — Permission details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getPrivateURL

```php
getPrivateURL($config = array()
```

Returns private URL to access the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Private URL.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getPublishConfigurations

```php
getPublishConfigurations()
```

Returns publish configurations for the specified view.

**Returns** — Publish details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getTableMetadata

```php
getTableMetadata()
```

Retrieves metadata information for the current table. Returns metadata details such as available columns and their attributes.

**Returns** — Table metadata details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getViewDependents

```php
getViewDependents()
```

Returns list of dependents views for the specified view.

**Returns** — Dependent view list.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getViewMetadataForAlert

```php
getViewMetadataForAlert()
```

Returns the view metadata that can be used while configuring a data alert for the specified view.

**Returns** — View metadata for data alert configuration.

### getViewTags

```php
getViewTags()
```

Returns the list of tags associated with the specified view.

**Returns** — Tags list.

### getViewURL

```php
getViewURL($config = array()
```

Returns the URL to access the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — View URL.

**Raises** — `IOException`; `ServerException`; `ParseException`

### hideColumns

```php
hideColumns($column_ids)
```

Hide the specified columns in the table.

| Parameter | Type | Description |
|---|---|---|
| `column_ids` | `array()` | Ids of the columns to be hidden. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### makeViewPublic

```php
makeViewPublic($config = array()
```

Make the specified view publically accessible.

| Parameter | Type | Description |
|---|---|---|
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — public URL.

**Raises** — `IOException`; `ServerException`; `ParseException`

### refetchData

```php
refetchData($config = array()
```

Sync data from available datasource for the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### removeFavorite

```php
removeFavorite()
```

Remove a specified view from favorite.

**Raises** — `IOException`; `ServerException`; `ParseException`

### removeLookup

```php
removeLookup($column_id, $config = array()
```

Remove the lookup for the specified column in the table.

| Parameter | Type | Description |
|---|---|---|
| `column_id` | `string` | Id of the column. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### removePrivateAccess

```php
removePrivateAccess()
```

Remove private link access for the specified view.

**Raises** — `IOException`; `ServerException`; `ParseException`

### removePublicAccess

```php
removePublicAccess()
```

Remove public access for the specified view.

**Raises** — `IOException`; `ServerException`; `ParseException`

### removeTagsFromView

```php
removeTagsFromView($tag_ids = NULL, $dissociate_all = false, $config = array()
```

Removes multiple tags from the specified view.

| Parameter | Type | Description |
|---|---|---|
| `tag_ids` | `array()` | Tag ids to be dissociated. Not required when dissociate_all is true. |
| `dissociate_all` | `boolean` | To dissociate all the associated tags from the view. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

### rename

```php
rename($view_name, $config = array()
```

Rename a specified view in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `view_name` | `string` | New name of the view. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### renameColumn

```php
renameColumn($column_id, $column_name)
```

Rename a specified column in the table.

| Parameter | Type | Description |
|---|---|---|
| `column_id` | `string` | Id of the column. |
| `column_name` | `string` | New name for the column. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### reorderColumns

```php
reorderColumns($column_ids, $config = array()
```

Updates the column order of the current table.

| Parameter | Type | Description |
|---|---|---|
| `column_ids` | `array` | List of column IDs in the desired order. |
| `config` | `array` | Optional configuration parameters. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### saveAs

```php
saveAs($new_view_name, $config = array()
```

Copy a specified view within the workspace.

| Parameter | Type | Description |
|---|---|---|
| `new_view_name` | `string` | The name of the new view. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Created view id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### showColumns

```php
showColumns($column_ids)
```

Show the specified hidden columns in the table.

| Parameter | Type | Description |
|---|---|---|
| `column_ids` | `array()` | Ids of the columns to be hidden. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### sortDataByColumns

```php
sortDataByColumns($columns = NULL, $sort_order = NULL, $reset_sort = false, $config = array()
```

Sorts the data in the table based on specified columns.

| Parameter | Type | Description |
|---|---|---|
| `columns` | `array|null` | List of column IDs to sort by. |
| `sort_order` | `int|null` | Sorting order (1 → Ascending, 2 → Descending). |
| `reset_sort` | `boolean` | If true, resets existing sort configuration. |
| `config` | `array` | Optional configuration parameters. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### updatePublishConfigurations

```php
updatePublishConfigurations($config = array()
```

Update publish configurations for the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `array()` | Contains the control parameters. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### updateRow

```php
updateRow($column_values, $criteria, $config = array()
```

Update rows in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `column_values` | `array()` | Contains the values for the row. The column names are the key. |
| `criteria` | `array()` | The criteria to be applied for updating data. Only rows matching the criteria will be updated. Should be null for update all rows. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Updated Columns List and Updated Rows Count.

**Raises** — `IOException`; `ServerException`; `ParseException`

### updateSharedDetails

```php
updateSharedDetails($config = array()
```

Update the existing sharing configuration for the specified view.

**Raises** — `IOException`; `ServerException`; `ParseException`

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
