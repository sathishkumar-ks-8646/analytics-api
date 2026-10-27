# ViewAPI

```csharp
IOrgAPI       org       = ac.GetOrgInstance(orgId);
IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
IViewAPI      view      = ac.GetViewInstance(orgId, workspaceId, viewId);
IBulkAPI      bulk      = ac.GetBulkInstance(orgId, workspaceId);
```

`ViewAPI` exposes **51 methods**. Method names are `PascalCase` and identifiers are `long`.

## Methods

[`AddAggregateFormula`](#addaggregateformula), [`AddColumn`](#addcolumn), [`AddFavorite`](#addfavorite), [`AddFormulaColumn`](#addformulacolumn), [`AddLookup`](#addlookup), [`AddRow`](#addrow), [`AddTagsToView`](#addtagstoview), [`AutoAnalyse`](#autoanalyse), [`AutoAnalyseColumn`](#autoanalysecolumn), [`CopyFormulas`](#copyformulas), [`CreateAlert`](#createalert), [`CreatePrivateURL`](#createprivateurl), [`CreateSimilarViews`](#createsimilarviews), [`Delete`](#delete), [`DeleteAggregateFormula`](#deleteaggregateformula), [`DeleteColumn`](#deletecolumn), [`DeleteFormulaColumn`](#deleteformulacolumn), [`DeleteRow`](#deleterow), [`EditAggregateFormula`](#editaggregateformula), [`EditFormulaColumn`](#editformulacolumn), [`GetAggregateFormulas`](#getaggregateformulas), [`GetAlertsInView`](#getalertsinview), [`GetColumnDependents`](#getcolumndependents), [`GetEmbedURL`](#getembedurl), [`GetFormulaColumns`](#getformulacolumns), [`GetLastImportDetails`](#getlastimportdetails), [`GetMyPermissions`](#getmypermissions), [`GetPrivateURL`](#getprivateurl), [`GetPublishConfigurations`](#getpublishconfigurations), [`GetTableMetadata`](#gettablemetadata), [`GetViewDependents`](#getviewdependents), [`GetViewMetadataForAlert`](#getviewmetadataforalert), [`GetViewTags`](#getviewtags), [`GetViewURL`](#getviewurl), [`HideColumns`](#hidecolumns), [`MakeViewPublic`](#makeviewpublic), [`RefetchData`](#refetchdata), [`RemoveFavorite`](#removefavorite), [`RemoveLookup`](#removelookup), [`RemovePrivateAccess`](#removeprivateaccess), [`RemovePublicAccess`](#removepublicaccess), [`RemoveTagsFromView`](#removetagsfromview), [`Rename`](#rename), [`RenameColumn`](#renamecolumn), [`ReorderColumns`](#reordercolumns), [`SaveAs`](#saveas), [`ShowColumns`](#showcolumns), [`SortDataByColumns`](#sortdatabycolumns), [`UpdatePublishConfigurations`](#updatepublishconfigurations), [`UpdateRow`](#updaterow), [`UpdateSharedDetails`](#updateshareddetails)

### AddAggregateFormula

```csharp
long AddAggregateFormula(string formulaName, string expression, Dictionary config)
```

Add a aggregate formula in the specified table.

| Parameter | Description |
|---|---|
| `formulaName` | Name of the formula to be created. |
| `expression` | Formula expression. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — Formula id.

### AddColumn

```csharp
long AddColumn(string columnName, string dataType, Dictionary config)
```

Add a column in the specified table.

| Parameter | Description |
|---|---|
| `columnName` | The name of the column. |
| `dataType` | The data-type of the column. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — Column id.

### AddFavorite

```csharp
void AddFavorite()
```

Adds a specified view as favourite.

### AddFormulaColumn

```csharp
long AddFormulaColumn(string formulaName, string expression, Dictionary config)
```

Add a formula column in the specified table.

| Parameter | Description |
|---|---|
| `formulaName` | Name of the formula column to be created. |
| `expression` | Formula expression. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — Formula id.

### AddLookup

```csharp
void AddLookup(long columnId, long refViewId, long refColumnId, Dictionary config)
```

Add a lookup in the specified child table.

| Parameter | Description |
|---|---|
| `columnId` | The id of the column. |
| `refViewId` | The ID of the table contains the parent column. |
| `refColumnId` | The ID of the parent column. |
| `config` | Contains any additional control configurations. Can be null. |

### AddRow

```csharp
JsonElement AddRow(Dictionary columnValues, Dictionary config)
```

Add a single row in the specified table.

| Parameter | Description |
|---|---|
| `columnValues` | Contains the values for the row. The column names are the key. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JsonElement`) — Added rows details.

### AddTagsToView

```csharp
void AddTagsToView(List tagIds, Dictionary config)
```

Adds multiple tags to the specified view.

| Parameter | Description |
|---|---|
| `tagIds` | Tag ids to be associated with the view. |
| `config` | Contains any additional control configurations. Can be null. |

### AutoAnalyse

```csharp
void AutoAnalyse(Dictionary config)
```

Auto generate reports for the specified table.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

### AutoAnalyseColumn

```csharp
void AutoAnalyseColumn(long columnId, Dictionary config)
```

Auto generate reports for the specified column.

| Parameter | Description |
|---|---|
| `columnId` | The id of the column. |
| `config` | Contains any additional control configurations. Can be null. |

### CopyFormulas

```csharp
void CopyFormulas(List formulaNames, long destWorkspaceId, Dictionary config, long? destOrgId)
```

Copy the specified formulas from one table to another within the workspace or across workspaces.

| Parameter | Description |
|---|---|
| `formulaNames` | The name of the formula columns to be copied. |
| `destWorkspaceId` | The ID of the destination workspace. |
| `config` | Contains any additional control configurations. Can be null. |
| `destOrgId` | Id of the organization where the destination workspace is present. Can be null. |

### CreateAlert

```csharp
long CreateAlert(string alertName, Dictionary scheduleDetails, List > rules, Dictionary config)
```

Create a data alert for the specified view.

| Parameter | Description |
|---|---|
| `alertName` | Name of the data alert. |
| `scheduleDetails` | Contains the schedule configurations of the data alert. |
| `rules` | Contains the rules to be evaluated by the data alert. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — New data alert id.

### CreatePrivateURL

```csharp
string CreatePrivateURL(Dictionary config)
```

Create a private URL for the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`string`) — Private URL.

### CreateSimilarViews

```csharp
void CreateSimilarViews(long refViewId, long folderId, Dictionary config)
```

Create reports for the specified table based on the reference table.

| Parameter | Description |
|---|---|
| `refViewId` | The ID of the reference view. |
| `folderId` | The folder id where the views to be saved. |
| `config` | Contains any additional control configurations. Can be null. |

### Delete

```csharp
void Delete(Dictionary config)
```

Delete a specified view in the workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

### DeleteAggregateFormula

```csharp
void DeleteAggregateFormula(long formulaId, Dictionary config)
```

Delete the specified aggregate formula.

| Parameter | Description |
|---|---|
| `formulaId` | Id of the formula column to be deleted. |
| `config` | Contains any additional control configurations. Can be null. |

### DeleteColumn

```csharp
void DeleteColumn(long columnId, Dictionary config)
```

Delete a specified column in the table.

| Parameter | Description |
|---|---|
| `columnId` | The id of the column. |
| `config` | Contains any additional control configurations. Can be null. |

### DeleteFormulaColumn

```csharp
void DeleteFormulaColumn(long formulaId, Dictionary config)
```

Delete the specified formula column.

| Parameter | Description |
|---|---|
| `formulaId` | Id of the formula column to be deleted. |
| `config` | Contains any additional control configurations. Can be null. |

### DeleteRow

```csharp
int DeleteRow(string criteria, Dictionary config)
```

Delete rows in the specified table.

| Parameter | Description |
|---|---|
| `criteria` | The criteria to be applied for deleting data. Only rows matching the criteria will be deleted. Should be null for delete all rows. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`int`) — Deleted rows count.

### EditAggregateFormula

```csharp
void EditAggregateFormula(long formulaId, string expression, Dictionary config)
```

Edit the specified aggregate formula.

| Parameter | Description |
|---|---|
| `formulaId` | Id of the aggregate formula to be updated. |
| `expression` | Formula expression. |
| `config` | Contains any additional control configurations. Can be null. |

### EditFormulaColumn

```csharp
void EditFormulaColumn(long formulaId, string expression, Dictionary config)
```

Edit the specified formula column.

| Parameter | Description |
|---|---|
| `formulaId` | Id of the formula column to be updated. |
| `expression` | Formula expression. |
| `config` | Contains any additional control configurations. Can be null. |

### GetAggregateFormulas

```csharp
JsonElement GetAggregateFormulas()
```

Returns list of all aggregate formulas for the specified table.

**Returns** (`JsonElement`) — Aggregate formula list

### GetAlertsInView

```csharp
JsonElement GetAlertsInView()
```

Returns list of data alerts configured for the specified view.

**Returns** (`JsonElement`) — Data alerts list.

### GetColumnDependents

```csharp
JsonElement GetColumnDependents(long columnId)
```

Returns list of dependents views and formulas for the specified column.

| Parameter | Description |
|---|---|
| `columnId` | Id of the column. |

**Returns** (`JsonElement`) — Dependent details.

### GetEmbedURL

```csharp
string GetEmbedURL(Dictionary config)
```

Returns embed URL to access the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`string`) — Embed URL.

### GetFormulaColumns

```csharp
JsonElement GetFormulaColumns()
```

Returns list of all formula columns for the specified table.

**Returns** (`JsonElement`) — Formula list

### GetLastImportDetails

```csharp
JsonElement GetLastImportDetails()
```

Returns last import details of the specified view.

**Returns** (`JsonElement`) — Last import details.

### GetMyPermissions

```csharp
JsonElement GetMyPermissions()
```

Returns permissions for the specified view.

**Returns** (`JsonElement`) — Permission details.

### GetPrivateURL

```csharp
string GetPrivateURL(Dictionary config)
```

Returns private URL to access the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`string`) — Private URL.

### GetPublishConfigurations

```csharp
JsonElement GetPublishConfigurations()
```

Returns publish configurations for the specified view.

**Returns** (`JsonElement`) — Publish details.

### GetTableMetadata

```csharp
JsonElement GetTableMetadata()
```

Retrieves metadata information for the current table, including the list of available columns and associated attributes.

**Returns** (`JsonElement`) — Table metadata details.

### GetViewDependents

```csharp
JsonElement GetViewDependents()
```

Returns list of dependents views for the specified view.

**Returns** (`JsonElement`) — Dependent view list.

### GetViewMetadataForAlert

```csharp
JsonElement GetViewMetadataForAlert()
```

Returns the view metadata that can be used while configuring a data alert for the specified view.

**Returns** (`JsonElement`) — View metadata for data alert configuration.

### GetViewTags

```csharp
JsonElement GetViewTags()
```

Returns the list of tags associated with the specified view.

**Returns** (`JsonElement`) — Tags list.

### GetViewURL

```csharp
string GetViewURL(Dictionary config)
```

Returns the URL to access the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`string`) — View URL.

### HideColumns

```csharp
void HideColumns(List columnIds)
```

Hide the specified columns in the table.

| Parameter | Description |
|---|---|
| `columnIds` | The array of column ids to be hidden. |

### MakeViewPublic

```csharp
string MakeViewPublic(Dictionary config)
```

Make the specified view publically accessible.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`string`) — View URL.

### RefetchData

```csharp
void RefetchData(Dictionary config)
```

Sync data from available datasource for the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

### RemoveFavorite

```csharp
void RemoveFavorite()
```

Remove a specified view from favourite.

### RemoveLookup

```csharp
void RemoveLookup(long columnId, Dictionary config)
```

Remove the lookup for the specified column in the table.

| Parameter | Description |
|---|---|
| `columnId` | The id of the column. |
| `config` | Contains any additional control configurations. Can be null. |

### RemovePrivateAccess

```csharp
void RemovePrivateAccess()
```

Remove private link access for the specified view.

### RemovePublicAccess

```csharp
void RemovePublicAccess()
```

Remove public access for the specified view.

### RemoveTagsFromView

```csharp
void RemoveTagsFromView(List tagIds, bool dissociateAll, Dictionary config)
```

Removes multiple tags from the specified view.

| Parameter | Description |
|---|---|
| `tagIds` | Tag ids to be dissociated. Not required when dissociateAll is true. |
| `dissociateAll` | If true, dissociates all tags from the view. |
| `config` | Contains any additional control configurations. Can be null. |

### Rename

```csharp
void Rename(string newViewName, Dictionary config)
```

Rename a specified view in the workspace.

| Parameter | Description |
|---|---|
| `newViewName` | The new name of the view. |
| `config` | Contains any additional control configurations. Can be null. |

### RenameColumn

```csharp
void RenameColumn(long columnId, string columnName)
```

Rename a specified column in the table.

| Parameter | Description |
|---|---|
| `columnId` | The id of the column. |
| `columnName` | The new name of the column. |

### ReorderColumns

```csharp
void ReorderColumns(List columnIds, Dictionary config)
```

Updates the column order of the current table.

| Parameter | Description |
|---|---|
| `columnIds` | A list containing the full set of column IDs in the new order. |
| `config` | Contains any additional control configurations. Can be null. |

### SaveAs

```csharp
long SaveAs(string newViewName, Dictionary config)
```

Copy a specified view within the workspace.

| Parameter | Description |
|---|---|
| `newViewName` | The name of the new view. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — View id.

### ShowColumns

```csharp
void ShowColumns(List columnIds)
```

Show the specified hidden columns in the table.

| Parameter | Description |
|---|---|
| `columnIds` | The array of column ids to be shown. |

### SortDataByColumns

```csharp
void SortDataByColumns(List columns, int? sortOrder, bool resetSort, Dictionary config)
```

Sorts the data in the table based on the specified columns.

| Parameter | Description |
|---|---|
| `columns` | List of column IDs to sort by. |
| `sortOrder` | Sorting order indicator. 1 -> Ascending 2 -> Descending |
| `resetSort` | If true, resets any existing sort configuration. |
| `config` | Contains any additional control configurations. Can be null. |

### UpdatePublishConfigurations

```csharp
void UpdatePublishConfigurations(Dictionary config)
```

Update publish configurations for the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains the control configurations. |

### UpdateRow

```csharp
JsonElement UpdateRow(Dictionary columnValues, string criteria, Dictionary config)
```

Update rows in the specified table.

| Parameter | Description |
|---|---|
| `columnValues` | Contains the values for the row. The column names are the key. |
| `criteria` | The criteria to be applied for updating data. Only rows matching the criteria will be updated. Should be null for update all rows. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JsonElement`) — Updated rows details.

### UpdateSharedDetails

```csharp
void UpdateSharedDetails(Dictionary config)
```

Update the existing sharing configuration for views.

| Parameter | Description |
|---|---|
| `config` | Contains the control configurations. |

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
