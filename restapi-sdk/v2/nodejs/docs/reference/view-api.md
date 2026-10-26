# ViewAPI

```javascript
var org       = ac.getOrgInstance(orgId);
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
var view      = ac.getViewInstance(orgId, workspaceId, viewId);
var bulk      = ac.getBulkInstance(orgId, workspaceId);
```

`ViewAPI` exposes **51 methods**. Method names are `camelCase` and identifiers are `string`.

## Methods

[`addAggregateFormula`](#addaggregateformula), [`addColumn`](#addcolumn), [`addFavorite`](#addfavorite), [`addFormulaColumn`](#addformulacolumn), [`addLookup`](#addlookup), [`addRow`](#addrow), [`addTagsToView`](#addtagstoview), [`autoAnalyse`](#autoanalyse), [`autoAnalyseColumn`](#autoanalysecolumn), [`copyFormulas`](#copyformulas), [`createAlert`](#createalert), [`createPrivateUrl`](#createprivateurl), [`createSimilarViews`](#createsimilarviews), [`delete`](#delete), [`deleteAggregateFormula`](#deleteaggregateformula), [`deleteColumn`](#deletecolumn), [`deleteFormulaColumn`](#deleteformulacolumn), [`deleteRow`](#deleterow), [`editAggregateFormula`](#editaggregateformula), [`editFormulaColumn`](#editformulacolumn), [`getAggregateFormulas`](#getaggregateformulas), [`getAlertsInView`](#getalertsinview), [`getColumnDependents`](#getcolumndependents), [`getEmbedUrl`](#getembedurl), [`getFormulaColumns`](#getformulacolumns), [`getLastImportDetails`](#getlastimportdetails), [`getMyPermissions`](#getmypermissions), [`getPrivateUrl`](#getprivateurl), [`getPublishConfigurations`](#getpublishconfigurations), [`getTableMetadata`](#gettablemetadata), [`getViewDependents`](#getviewdependents), [`getViewMetadataForAlert`](#getviewmetadataforalert), [`getViewTags`](#getviewtags), [`getViewUrl`](#getviewurl), [`hideColumns`](#hidecolumns), [`makeViewPublic`](#makeviewpublic), [`refetchData`](#refetchdata), [`removeFavorite`](#removefavorite), [`removeLookup`](#removelookup), [`removePrivateAccess`](#removeprivateaccess), [`removePublicAccess`](#removepublicaccess), [`removeTagsFromView`](#removetagsfromview), [`rename`](#rename), [`renameColumn`](#renamecolumn), [`reorderColumns`](#reordercolumns), [`saveAs`](#saveas), [`showColumns`](#showcolumns), [`sortDataByColumns`](#sortdatabycolumns), [`updatePublishConfigurations`](#updatepublishconfigurations), [`updateRow`](#updaterow), [`updateSharedDetails`](#updateshareddetails)

### addAggregateFormula

```javascript
addAggregateFormula(formulaName, expression, config={})
```

Add a aggregate formula in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `formulaName` | `String` | Name of the aggregate formula to be created. |
| `expression` | `String` | Formula expression. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Created aggregate formula id.

**Raises** — `Error`

### addColumn

```javascript
addColumn(columnName, dataType, config={})
```

Add a column in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `columnName` | `String` | The name of the column. |
| `dataType` | `String` | The data-type of the column. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Created column id.

**Raises** — `Error`

### addFavorite

```javascript
addFavorite(config={})
```

Adds a specified view as favorite.

**Raises** — `Error`

### addFormulaColumn

```javascript
addFormulaColumn(formulaName, expression, config={})
```

Add a formula column in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `formulaName` | `String` | Name of the formula column to be created. |
| `expression` | `String` | Formula expression. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Created formula column id.

**Raises** — `Error`

### addLookup

```javascript
addLookup(columnId, refViewId, refColumnId, config={})
```

Add a lookup in the specified child table.

| Parameter | Type | Description |
|---|---|---|
| `columnId` | `String` | Id of the column. |
| `refViewId` | `String` | The id of the table contains the parent column. |
| `refColumnId` | `String` | The id of the parent column. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### addRow

```javascript
addRow(columnValues, config={})
```

Add a single row in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `columnValues` | `Object` | Contains the values for the row. The column names are the key. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Column Names and Added Row Values.

**Raises** — `Error`

### addTagsToView

```javascript
addTagsToView(tagIds, config={})
```

Adds multiple tags to the specified view.

| Parameter | Type | Description |
|---|---|---|
| `tagIds` | `JSONArray` | Tag ids to be associated with the view. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### autoAnalyse

```javascript
autoAnalyse(config={})
```

Auto generate reports for the specified table.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### autoAnalyseColumn

```javascript
autoAnalyseColumn(columnId, config={})
```

Auto generate reports for the specified column.

| Parameter | Type | Description |
|---|---|---|
| `columnId` | `String` | Id of the column. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### copyFormulas

```javascript
copyFormulas(formulaNames, destWorkspaceId, config={}, destOrgId=null)
```

Copy the specified formulas from one table to another within the workspace or across workspaces.

| Parameter | Type | Description |
|---|---|---|
| `formulaNames` | `JSONArray` | The name of the formula columns to be copied. |
| `destWorkspaceId` | `String` | The ID of the destination workspace. |
| `config` | `Object` | Contains any additional control attributes. |
| `destOrgId` | `String` | ull - Id of the organization where the destination workspace is present. |

**Raises** — `Error`

### createAlert

```javascript
createAlert(alertName, scheduleDetails, rules, config={})
```

Create a data alert for the specified view.

| Parameter | Type | Description |
|---|---|---|
| `alertName` | `String` | Name of the data alert. |
| `scheduleDetails` | `Object` | Contains the schedule configurations of the data alert. |
| `rules` | `JSONArray` | Contains the rules to be evaluated by the data alert. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Created data alert id.

**Raises** — `Error`

### createPrivateUrl

```javascript
createPrivateUrl(config={})
```

Create a private URL for the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Private URL.

**Raises** — `Error`

### createSimilarViews

```javascript
createSimilarViews(refViewId, folderId, config={})
```

Create reports for the specified table based on the reference table.

| Parameter | Type | Description |
|---|---|---|
| `refViewId` | `String` | The ID of the reference view. |
| `folderId` | `String` | The folder id where the views to be saved. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### delete

```javascript
delete(config={})
```

Delete a specified view in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### deleteAggregateFormula

```javascript
deleteAggregateFormula(formulaId, config={})
```

Delete the specified aggregate formula.

| Parameter | Type | Description |
|---|---|---|
| `formulaId` | `String` | Id of the aggregate formula to be deleted. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### deleteColumn

```javascript
deleteColumn(columnId, config={})
```

Delete a specified column in the table.

| Parameter | Type | Description |
|---|---|---|
| `columnId` | `String` | Id of the column. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### deleteFormulaColumn

```javascript
deleteFormulaColumn(formulaId, config={})
```

Delete the specified formula column.

| Parameter | Type | Description |
|---|---|---|
| `formulaId` | `String` | Id of the formula column to be deleted. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### deleteRow

```javascript
deleteRow(criteria, config={})
```

Delete rows in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `criteria` | `String` | The criteria to be applied for deleting data. Only rows matching the criteria will be deleted. Should be null for delete all rows. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Deleted rows count.

**Raises** — `Error`

### editAggregateFormula

```javascript
editAggregateFormula(formulaId, expression, config={})
```

Edit the specified aggregate formula.

| Parameter | Type | Description |
|---|---|---|
| `formulaId` | `String` | Id of the aggregate formula to be updated. |
| `expression` | `String` | Formula expression. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### editFormulaColumn

```javascript
editFormulaColumn(formulaId, expression, config={})
```

Edit the specified formula column.

| Parameter | Type | Description |
|---|---|---|
| `formulaId` | `String` | Id of the formula column to be updated. |
| `expression` | `String` | Formula expression. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### getAggregateFormulas

```javascript
getAggregateFormulas()
```

Returns list of all aggregate formulas for the specified table.

**Returns** — Aggregate formula list.

**Raises** — `Error`

### getAlertsInView

```javascript
getAlertsInView()
```

Returns list of data alerts configured for the specified view.

**Returns** — Data alerts list.

**Raises** — `Error`

### getColumnDependents

```javascript
getColumnDependents(columnId)
```

Returns list of dependents views and formulas for the specified column.

| Parameter | Type | Description |
|---|---|---|
| `columnId` | `String` | Id of the column. |

**Returns** — Dependent details.

**Raises** — `Error`

### getEmbedUrl

```javascript
getEmbedUrl(config={})
```

Returns embed URL to access the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Embed URL.

**Raises** — `Error`

### getFormulaColumns

```javascript
getFormulaColumns()
```

Returns list of all formula columns for the specified table.

**Returns** — Formula column list.

**Raises** — `Error`

### getLastImportDetails

```javascript
getLastImportDetails()
```

Returns last import details of the specified view.

**Returns** — Last import details.

**Raises** — `Error`

### getMyPermissions

```javascript
getMyPermissions()
```

Returns permissions for the specified view.

**Returns** — Permission details.

**Raises** — `Error`

### getPrivateUrl

```javascript
getPrivateUrl(config={})
```

Returns private URL to access the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Private URL.

**Raises** — `Error`

### getPublishConfigurations

```javascript
getPublishConfigurations()
```

Returns publish configurations for the specified view.

**Returns** — Publish details.

**Raises** — `Error`

### getTableMetadata

```javascript
getTableMetadata()
```

Retrieves metadata information for the current table, including the list of available columns and associated attributes.

**Returns** — Table metadata details.

**Raises** — `Error`

### getViewDependents

```javascript
getViewDependents()
```

Returns list of dependents views for the specified view.

**Returns** — Dependent view list.

**Raises** — `Error`

### getViewMetadataForAlert

```javascript
getViewMetadataForAlert()
```

Returns the view metadata that can be used while configuring a data alert for the specified view.

**Returns** — View metadata for data alert configuration.

**Raises** — `Error`

### getViewTags

```javascript
getViewTags()
```

Returns list of tags associated with the specified view.

**Returns** — Tags list.

**Raises** — `Error`

### getViewUrl

```javascript
getViewUrl(config={})
```

Returns the URL to access the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — View URL.

**Raises** — `Error`

### hideColumns

```javascript
hideColumns(columnIds, config={})
```

Hide the specified columns in the table.

| Parameter | Type | Description |
|---|---|---|
| `columnIds` | `JSONArray` | Ids of the columns to be hidden. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### makeViewPublic

```javascript
makeViewPublic(config={})
```

Make the specified view publically accessible.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Public URL.

**Raises** — `Error`

### refetchData

```javascript
refetchData(config={})
```

Sync data from available datasource for the specified view.

| Parameter | Type | Description |
|---|---|---|
| `viewName` | `String` | New name of the view. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### removeFavorite

```javascript
removeFavorite(config={})
```

Remove a specified view from favorite.

**Raises** — `Error`

### removeLookup

```javascript
removeLookup(columnId, config={})
```

Remove the lookup for the specified column in the table.

| Parameter | Type | Description |
|---|---|---|
| `columnId` | `String` | Id of the column. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### removePrivateAccess

```javascript
removePrivateAccess()
```

Remove private link access for the specified view.

**Raises** — `Error`

### removePublicAccess

```javascript
removePublicAccess()
```

Remove public access for the specified view.

**Raises** — `Error`

### removeTagsFromView

```javascript
removeTagsFromView(tagIds=null, dissociateAll=false, config={})
```

Removes multiple tags from the specified view.

| Parameter | Type | Description |
|---|---|---|
| `tagIds` | `JSONArray` | Tag ids to be dissociated. Not required when dissociateAll is true. |
| `dissociateAll` | `Boolean` | To dissociate all the associated tags from the view. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### rename

```javascript
rename(viewName, config={})
```

Rename a specified view in the workspace.

| Parameter | Type | Description |
|---|---|---|
| `viewName` | `String` | New name of the view. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### renameColumn

```javascript
renameColumn(columnId, newColumnName, config={})
```

Rename a specified column in the table.

| Parameter | Type | Description |
|---|---|---|
| `columnId` | `String` | Id of the column. |
| `newColumnName` | `String` | New name for the column. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### reorderColumns

```javascript
reorderColumns(columnIds, config = {})
```

Updates the column order of the current table.

| Parameter | Type | Description |
|---|---|---|
| `columnIds` | `Array` | Full set of column IDs in the new order. |
| `config` | `Object` | Additional control attributes. |

**Raises** — `Error`

### saveAs

```javascript
saveAs(newViewName, config={})
```

Copy a specified view within the workspace.

| Parameter | Type | Description |
|---|---|---|
| `newViewName` | `String` | The name of the new view. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Newly created view id.

**Raises** — `Error`

### showColumns

```javascript
showColumns(columnIds, config={})
```

Show the specified hidden columns in the table.

| Parameter | Type | Description |
|---|---|---|
| `columnIds` | `JSONArray` | Ids of the columns to be shown. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### sortDataByColumns

```javascript
sortDataByColumns(columns = null, sortOrder = null, resetSort = false, config = {})
```

Sorts the data in the table based on the specified columns.

| Parameter | Type | Description |
|---|---|---|
| `columns` | `Array|null` | List of column IDs to sort by. |
| `sortOrder` | `Number|null` | 1 for ascending, 2 for descending. |
| `resetSort` | `Boolean` | If true, resets existing sort. |
| `config` | `Object` | Additional control attributes. |

**Raises** — `Error`

### updatePublishConfigurations

```javascript
updatePublishConfigurations(config={})
```

Update publish configurations for the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains the required control attributes. |

**Raises** — `Error`

### updateRow

```javascript
updateRow(columnValues, criteria, config={})
```

Update rows in the specified table.

| Parameter | Type | Description |
|---|---|---|
| `columnValues` | `Object` | Contains the values for the row. The column names are the key. |
| `criteria` | `String` | The criteria to be applied for updating data. Only rows matching the criteria will be updated. Should be null for update all rows. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Updated Columns List and Updated Rows Count.

**Raises** — `Error`

### updateSharedDetails

```javascript
updateSharedDetails(config={})
```

Update shared details of the specified view.

| Parameter | Type | Description |
|---|---|---|
| `config` | `Object` | Contains the control attributes. |

**Raises** — `Error`

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
