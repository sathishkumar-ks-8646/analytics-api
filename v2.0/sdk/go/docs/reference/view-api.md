# ViewAPI

```go
org       := ZAnalytics.GetOrgInstance(&ac, orgId)
workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
view      := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
bulk      := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
```

`ViewAPI` exposes **51 methods**. Method names are `PascalCase` (exported) and identifiers are `string`.

## Methods

[`AddAggregateFormula`](#addaggregateformula), [`AddColumn`](#addcolumn), [`AddFavorite`](#addfavorite), [`AddFormulaColumn`](#addformulacolumn), [`AddLookup`](#addlookup), [`AddRow`](#addrow), [`AddTagsToView`](#addtagstoview), [`AutoAnalyse`](#autoanalyse), [`AutoAnalyseColumn`](#autoanalysecolumn), [`CopyFormulas`](#copyformulas), [`CreateAlert`](#createalert), [`CreatePrivateUrl`](#createprivateurl), [`CreateSimilarViews`](#createsimilarviews), [`Delete`](#delete), [`DeleteAggregateFormula`](#deleteaggregateformula), [`DeleteColumn`](#deletecolumn), [`DeleteFormulaColumn`](#deleteformulacolumn), [`DeleteRow`](#deleterow), [`EditAggregateFormula`](#editaggregateformula), [`EditFormulaColumn`](#editformulacolumn), [`GetAggregateFormulas`](#getaggregateformulas), [`GetAlertsInView`](#getalertsinview), [`GetColumnDependents`](#getcolumndependents), [`GetEmbedUrl`](#getembedurl), [`GetFormulaColumns`](#getformulacolumns), [`GetLastImportDetails`](#getlastimportdetails), [`GetMyPermissions`](#getmypermissions), [`GetPrivateUrl`](#getprivateurl), [`GetPublishConfigurations`](#getpublishconfigurations), [`GetTableMetadata`](#gettablemetadata), [`GetViewDependents`](#getviewdependents), [`GetViewMetadataForAlert`](#getviewmetadataforalert), [`GetViewTags`](#getviewtags), [`GetViewUrl`](#getviewurl), [`HideColumns`](#hidecolumns), [`MakeViewPublic`](#makeviewpublic), [`RefetchData`](#refetchdata), [`RemoveFavorite`](#removefavorite), [`RemoveLookup`](#removelookup), [`RemovePrivateAccess`](#removeprivateaccess), [`RemovePublicAccess`](#removepublicaccess), [`RemoveTagsFromView`](#removetagsfromview), [`Rename`](#rename), [`RenameColumn`](#renamecolumn), [`ReorderColumns`](#reordercolumns), [`SaveAs`](#saveas), [`ShowColumns`](#showcolumns), [`SortDataByColumns`](#sortdatabycolumns), [`UpdatePublishConfigurations`](#updatepublishconfigurations), [`UpdateRow`](#updaterow), [`UpdateSharedDetails`](#updateshareddetails)

### AddAggregateFormula

```go
AddAggregateFormula(formulaname string, expression string, config map[string]interface{}) (formulaid string, serverexception *ServerException)
```

Add an aggregate formula in the specified table.

| Parameter | Description |
|---|---|
| `formulaname` | Name of the formula to be created. |
| `expression` | Formula expression. |
| `config` | Contains the control configurations. |

**Returns** — Returns id of the created formula.

### AddColumn

```go
AddColumn(columnname, datatype string, config map[string]interface{}) (columnid string, serverexception *ServerException)
```

Add a column in the specified table.

| Parameter | Description |
|---|---|
| `columnname` | The name of the column. |
| `datatype` | The data-type of the column. |
| `config` | Contains the control configurations. |

**Returns** — Returns id of the new column.

### AddFavorite

```go
AddFavorite() (serverexception *ServerException)
```

Adds a specified view as favorite.

### AddFormulaColumn

```go
AddFormulaColumn(formulaname string, expression string, config map[string]interface{}) (formulaid string, serverexception *ServerException)
```

Add a formula column in the specified table.

| Parameter | Description |
|---|---|
| `formulaname` | Name of the formula column to be created. |
| `expression` | Formula expression. |
| `config` | Contains the control configurations. |

**Returns** — Returns id of the formula created.

### AddLookup

```go
AddLookup(columnid, refviewid, refcolumnid string, config map[string]interface{}) (serverexception *ServerException)
```

Add a lookup in the specified child table.

| Parameter | Description |
|---|---|
| `columnid` | The id of the column. |
| `refviewid` | The ID of the table contains the parent column. |
| `refcolumnid` | The ID of the parent column. |
| `config` | Contains the control configurations. |

### AddRow

```go
AddRow(columnvalues, config map[string]interface{}) (data interface{}, serverexception *ServerException)
```

Add a single row in the specified table.

| Parameter | Description |
|---|---|
| `columnvalues` | Contains the values for the row. The column names are the key. |
| `config` | Contains the control configurations. |

**Returns** — Returns details of the added rows as interface.

### AddTagsToView

```go
AddTagsToView(tagids interface{}, config map[string]interface{}) (serverexception *ServerException)
```

Adds multiple tags to the specified view.

| Parameter | Description |
|---|---|
| `tagids` | Tag ids to be associated with the view. |
| `config` | Contains any additional control configurations. |

### AutoAnalyse

```go
AutoAnalyse(config map[string]interface{}) (serverexception *ServerException)
```

Auto generate reports for the specified table.

| Parameter | Description |
|---|---|
| `config` | Contains the control configurations. |

### AutoAnalyseColumn

```go
AutoAnalyseColumn(columnid string, config map[string]interface{}) (serverexception *ServerException)
```

Auto generate reports for the specified column.

| Parameter | Description |
|---|---|
| `columnid` | The id of the column. |
| `config` | Contains the control configurations. |

### CopyFormulas

```go
CopyFormulas(formulanames interface{}, destworkspaceid string, config map[string]interface{}, destorgid string) (serverexception *ServerException)
```

Copy the specified formulas from one table to another within the workspace or across workspaces.

| Parameter | Description |
|---|---|
| `formulanames` | The name of the formula columns to be copied. |
| `destworkspaceid` | The ID of the destination workspace. |
| `config` | Contains the control configurations. |
| `destorgid` | Id of the organization where the destination workspace is present. |

### CreateAlert

```go
CreateAlert(alertname string, scheduledetails map[string]interface{}, rules interface{}, config map[string]interface{}) (alertid string, serverexception *ServerException)
```

Create a data alert for the specified view.

| Parameter | Description |
|---|---|
| `alertname` | Name of the data alert. |
| `scheduledetails` | Contains the schedule configurations of the data alert. |
| `rules` | Contains the rules to be evaluated by the data alert. |
| `config` | Contains any additional control configurations. |

**Returns** — Returns the new data alert id as string.

### CreatePrivateUrl

```go
CreatePrivateUrl(config map[string]interface{}) (privateurl string, serverexception *ServerException)
```

Create a private URL for the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains the control configurations. |

**Returns** — Returns the private URL.

### CreateSimilarViews

```go
CreateSimilarViews(refviewid, folderid string, config map[string]interface{}) (serverexception *ServerException)
```

Create reports for the specified table based on the reference table.

| Parameter | Description |
|---|---|
| `refviewid` | The ID of the reference view. |
| `folderid` | The folder id where the views to be saved. |
| `config` | Contains the control configurations. |

### Delete

```go
Delete(config map[string]interface{}) (serverexception *ServerException)
```

Delete a specified view in the workspace.

| Parameter | Description |
|---|---|
| `config` | Contains the control configurations. |

### DeleteAggregateFormula

```go
DeleteAggregateFormula(formulaid string, config map[string]interface{}) (serverexception *ServerException)
```

Delete the specified aggregate formula.

| Parameter | Description |
|---|---|
| `formulaid` | Id of the aggregate formula to be deleted. |
| `config` | Contains the control configurations. |

### DeleteColumn

```go
DeleteColumn(columnid string, config map[string]interface{}) (serverexception *ServerException)
```

Delete a specified column in the table.

| Parameter | Description |
|---|---|
| `columnid` | The id of the column. |
| `config` | Contains the control configurations. |

### DeleteFormulaColumn

```go
DeleteFormulaColumn(formulaid string, config map[string]interface{}) (serverexception *ServerException)
```

Delete the specified formula column.

| Parameter | Description |
|---|---|
| `formulaid` | Id of the formula column to be deleted. |
| `config` | Contains the control configurations. |

### DeleteRow

```go
DeleteRow(criteria string, config map[string]interface{}) (deletedCount float64, serverexception *ServerException)
```

Delete rows in the specified table.

| Parameter | Description |
|---|---|
| `criteria` | The criteria to be applied for deleting data. Only rows matching the criteria will be deleted. Should be null for delete all rows. |
| `config` | Contains the control configurations. |

**Returns** — Returns deleted rows count.

### EditAggregateFormula

```go
EditAggregateFormula(formulaid string, expression string, config map[string]interface{}) (serverexception *ServerException)
```

Edit the specified aggregate formula.

| Parameter | Description |
|---|---|
| `formulaid` | Id of the aggregate formula to be updated. |
| `expression` | Formula expression. |
| `config` | Contains the control configurations. |

### EditFormulaColumn

```go
EditFormulaColumn(formulaid string, expression string, config map[string]interface{}) (serverexception *ServerException)
```

Edit the specified formula column.

| Parameter | Description |
|---|---|
| `formulaid` | Id of the formula column to be updated. |
| `expression` | Formula expression. |
| `config` | Contains the control configurations. |

### GetAggregateFormulas

```go
GetAggregateFormulas() (formulas interface{}, serverexception *ServerException)
```

Returns list of all aggregate formulas for the specified table.

**Returns** — Returns aggregate formula list as interface.

### GetAlertsInView

```go
GetAlertsInView() (alerts interface{}, serverexception *ServerException)
```

Returns list of data alerts configured for the specified view.

**Returns** — Returns the data alerts list as interface.

### GetColumnDependents

```go
GetColumnDependents(columnid string) (dependents interface{}, serverexception *ServerException)
```

Returns list of dependents views and formulas for the specified column.

| Parameter | Description |
|---|---|
| `columnid` | The id of the column. |

**Returns** — Returns dependent list as interface.

### GetEmbedUrl

```go
GetEmbedUrl(config map[string]interface{}) (embedurl string, serverexception *ServerException)
```

Returns embed URL to access the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains the control configurations. |

**Returns** — Returns the embed URL.

### GetFormulaColumns

```go
GetFormulaColumns() (formulas interface{}, serverexception *ServerException)
```

Returns list of all formula columns for the specified table.

**Returns** — Returns formula column list as interface.

### GetLastImportDetails

```go
GetLastImportDetails() (importDetails interface{}, serverexception *ServerException)
```

Returns last import details of the specified view.

**Returns** — Returns the last import details as interface.

### GetMyPermissions

```go
GetMyPermissions() (permissions interface{}, serverexception *ServerException)
```

Returns permissions for the specified view.

**Returns** — Returns the permission details as interface.

### GetPrivateUrl

```go
GetPrivateUrl(config map[string]interface{}) (privateurl string, serverexception *ServerException)
```

Returns private URL to access the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains the control configurations. |

**Returns** — Returns the private URL.

### GetPublishConfigurations

```go
GetPublishConfigurations() (publishinfo interface{}, serverexception *ServerException)
```

Returns details of the specified slideshow.

**Returns** — Returns publish configurations for the specified view.

### GetTableMetadata

```go
GetTableMetadata() (metadata interface{}, serverexception *ServerException)
```

Retrieves metadata information for the current table.

**Returns** — Returns table metadata details as interface.

### GetViewDependents

```go
GetViewDependents() (dependents interface{}, serverexception *ServerException)
```

Returns list of dependents views for the specified view.

**Returns** — Returns dependent list as interface.

### GetViewMetadataForAlert

```go
GetViewMetadataForAlert() (metadata interface{}, serverexception *ServerException)
```

Returns the view metadata that can be used while configuring a data alert for the specified view.

**Returns** — Returns the view metadata for data alert configuration as interface.

### GetViewTags

```go
GetViewTags() (tags interface{}, serverexception *ServerException)
```

Returns the list of tags associated with the specified view.

**Returns** — Returns tag list as interface.

### GetViewUrl

```go
GetViewUrl(config map[string]interface{}) (viewurl string, serverexception *ServerException)
```

Returns the URL to access the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains the control configurations. |

**Returns** — Returns the view URL.

### HideColumns

```go
HideColumns(columnids interface{}) (serverexception *ServerException)
```

Hide the specified columns in the table.

| Parameter | Description |
|---|---|
| `columnids` | Ids of the column to be hidden. |

### MakeViewPublic

```go
MakeViewPublic(config map[string]interface{}) (privateurl string, serverexception *ServerException)
```

Make the specified view publically accessible.

| Parameter | Description |
|---|---|
| `config` | Contains the control configurations. |

**Returns** — Returns the view URL.

### RefetchData

```go
RefetchData(config map[string]interface{}) (serverexception *ServerException)
```

Sync data from available datasource for the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains any additonal control configurations. |

### RemoveFavorite

```go
RemoveFavorite() (serverexception *ServerException)
```

Remove a specified view from favorite.

### RemoveLookup

```go
RemoveLookup(columnid string, config map[string]interface{}) (serverexception *ServerException)
```

Remove the lookup for the specified column in the table.

| Parameter | Description |
|---|---|
| `columnid` | The id of the column. |
| `config` | Contains the control configurations. |

### RemovePrivateAccess

```go
RemovePrivateAccess() (serverexception *ServerException)
```

Remove private link access for the specified view.

### RemovePublicAccess

```go
RemovePublicAccess() (serverexception *ServerException)
```

Remove public access for the specified view.

### RemoveTagsFromView

```go
RemoveTagsFromView(tagids interface{}, dissociateAll bool, config map[string]interface{}) (serverexception *ServerException)
```

Removes multiple tags from the specified view.

| Parameter | Description |
|---|---|
| `tagids` | Tag ids to be dissociated. Pass nil when dissociateAll is true. |
| `dissociateAll` | To dissociate all tags from the view. |
| `config` | Contains any additional control configurations. |

### Rename

```go
Rename(viewename string, config map[string]interface{}) (serverexception *ServerException)
```

Rename a specified view in the workspace.

| Parameter | Description |
|---|---|
| `viewename` | The new name of the view. |
| `config` | Contains the control configurations. |

### RenameColumn

```go
RenameColumn(columnid, columnname string) (serverexception *ServerException)
```

Rename a specified column in the table.

| Parameter | Description |
|---|---|
| `columnid` | The id of the column. |
| `columnname` | The new name of the column. |

### ReorderColumns

```go
ReorderColumns(columnids []interface{}, config map[string]interface{}) (serverexception *ServerException)
```

Updates the column order of the current table.

| Parameter | Description |
|---|---|
| `columnids` | A list containing the full set of column IDs in the new order in which they should appear. |
| `config` | Contains any additional control parameters. |

### SaveAs

```go
SaveAs(newviewname string, config map[string]interface{}) (viewid string, serverexception *ServerException)
```

Copy a specified view within the workspace.

| Parameter | Description |
|---|---|
| `newviewname` | The name of the new view. |
| `config` | Contains the control configurations. |

**Returns** — Returns id of the new view.

### ShowColumns

```go
ShowColumns(columnids interface{}) (serverexception *ServerException)
```

Show the specified hidden columns in the table.

| Parameter | Description |
|---|---|
| `columnids` | Ids of the column to be shown. |

### SortDataByColumns

```go
SortDataByColumns(columns []interface{}, sortorder int, resetsort bool, config map[string]interface{}) (serverexception *ServerException)
```

Sorts the data in the table based on the specified columns.

| Parameter | Description |
|---|---|
| `columns` | A list of column IDs to sort by. |
| `sortorder` | Sorting order indicator. |
| `resetsort` | If true, resets any existing sort configuration. |
| `config` | Contains any additional control parameters. |

### UpdatePublishConfigurations

```go
UpdatePublishConfigurations(config map[string]interface{}) (serverexception *ServerException)
```

Update publish configurations for the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains the control configurations. |

### UpdateRow

```go
UpdateRow(columnvalues map[string]interface{}, criteria string, config map[string]interface{}) (data interface{}, serverexception *ServerException)
```

Update rows in the specified table.

| Parameter | Description |
|---|---|
| `columnvalues` | Contains the values for the row. The column names are the key. |
| `criteria` | The criteria to be applied for updating data. Only rows matching the criteria will be updated. Should be null for update all rows. |
| `config` | Contains the control configurations. |

**Returns** — Returns details of the updated rows as interface.

### UpdateSharedDetails

```go
UpdateSharedDetails(config map[string]interface{}) (serverexception *ServerException)
```

Update the existing sharing configuration for views.

| Parameter | Description |
|---|---|
| `config` | Contains the control configurations. |

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
