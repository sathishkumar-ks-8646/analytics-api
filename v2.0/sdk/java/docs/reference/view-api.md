# ViewAPI

```java
OrgAPI       org       = ac.getOrgInstance(orgId);
WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
ViewAPI      view      = ac.getViewInstance(orgId, workspaceId, viewId);
BulkAPI      bulk      = ac.getBulkInstance(orgId, workspaceId);
```

`ViewAPI` exposes **51 methods**. Method names are `camelCase`, matching the endpoint title and identifiers are `long`.

## Methods

[`addAggregateFormula`](#addaggregateformula), [`addColumn`](#addcolumn), [`addFavorite`](#addfavorite), [`addFormulaColumn`](#addformulacolumn), [`addLookup`](#addlookup), [`addRow`](#addrow), [`addTagsToView`](#addtagstoview), [`autoAnalyse`](#autoanalyse), [`autoAnalyseColumn`](#autoanalysecolumn), [`copyFormulas`](#copyformulas), [`createAlert`](#createalert), [`createPrivateURL`](#createprivateurl), [`createSimilarViews`](#createsimilarviews), [`delete`](#delete), [`deleteAggregateFormula`](#deleteaggregateformula), [`deleteColumn`](#deletecolumn), [`deleteFormulaColumn`](#deleteformulacolumn), [`deleteRow`](#deleterow), [`editAggregateFormula`](#editaggregateformula), [`editFormulaColumn`](#editformulacolumn), [`getAggregateFormulas`](#getaggregateformulas), [`getAlertsInView`](#getalertsinview), [`getColumnDependents`](#getcolumndependents), [`getEmbedURL`](#getembedurl), [`getFormulaColumns`](#getformulacolumns), [`getLastImportDetails`](#getlastimportdetails), [`getMyPermissions`](#getmypermissions), [`getPrivateURL`](#getprivateurl), [`getPublishConfigurations`](#getpublishconfigurations), [`getTableMetadata`](#gettablemetadata), [`getViewDependents`](#getviewdependents), [`getViewMetadataForAlert`](#getviewmetadataforalert), [`getViewTags`](#getviewtags), [`getViewURL`](#getviewurl), [`hideColumns`](#hidecolumns), [`makeViewPublic`](#makeviewpublic), [`refetchData`](#refetchdata), [`removeFavorite`](#removefavorite), [`removeLookup`](#removelookup), [`removePrivateAccess`](#removeprivateaccess), [`removePublicAccess`](#removepublicaccess), [`removeTagsFromView`](#removetagsfromview), [`rename`](#rename), [`renameColumn`](#renamecolumn), [`reorderColumns`](#reordercolumns), [`saveAs`](#saveas), [`showColumns`](#showcolumns), [`sortDataByColumns`](#sortdatabycolumns), [`updatePublishConfigurations`](#updatepublishconfigurations), [`updateRow`](#updaterow), [`UpdateSharedDetails`](#updateshareddetails)

### addAggregateFormula

```java
long addAggregateFormula(String formulaName, String expression, JSONObject config)
```

Add a aggregate formula in the specified table.

| Parameter | Description |
|---|---|
| `formulaName` | Name of the aggregate formula to be created. |
| `expression` | Formula expression. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — A `long` of created formula id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### addColumn

```java
long addColumn(String columnName, String dataType, JSONObject config)
```

Add a column in the specified table.

| Parameter | Description |
|---|---|
| `columnName` | The name of the column. |
| `dataType` | The data-type of the column. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — A `long` of column id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### addFavorite

```java
void addFavorite()
```

Adds a specified view as favorite.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### addFormulaColumn

```java
long addFormulaColumn(String formulaName, String expression, JSONObject config)
```

Add a formula column in the specified table.

| Parameter | Description |
|---|---|
| `formulaName` | Name of the formula column to be created. |
| `expression` | Formula expression. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — A `long` of created formula id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### addLookup

```java
void addLookup(long columnId, long refViewId, long refColumnId, JSONObject config)
```

Add a lookup in the specified child table.

| Parameter | Description |
|---|---|
| `columnId` | The id of the column. |
| `refViewId` | The ID of the table contains the parent column. |
| `refColumnId` | The ID of the parent column. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### addRow

```java
JSONObject addRow(JSONObject columnValues, JSONObject config)
```

Add a single row in the specified table.

| Parameter | Description |
|---|---|
| `columnValues` | Contains the values for the row. The column names are the key. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JSONObject`) — A `JSONObject` of values of the added rows.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### addTagsToView

```java
void addTagsToView(JSONArray tagIds, JSONObject config)
```

Adds multiple tags to the specified view.

| Parameter | Description |
|---|---|
| `tagIds` | List of tag ids to be associated with the view. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### autoAnalyse

```java
void autoAnalyse(JSONObject config)
```

Auto generate reports for the specified table.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### autoAnalyseColumn

```java
void autoAnalyseColumn(long columnId, JSONObject config)
```

Auto generate reports for the specified column.

| Parameter | Description |
|---|---|
| `columnId` | The id of the column. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### copyFormulas

```java
void copyFormulas(JSONArray formulaNames, long destWorkspaceId, JSONObject config, Long destOrgId)
```

Copy the specified formulas from one table to another within the workspace or across workspaces.

| Parameter | Description |
|---|---|
| `formulaNames` | The name of the formula columns to be copied. |
| `destWorkspaceId` | The ID of the destination workspace. |
| `config` | Contains any additional control configurations. Can be null. |
| `destOrgId` | Id of the organization where the destination workspace is present. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### createAlert

```java
long createAlert(String alertName, JSONObject scheduleDetails, JSONArray rules, JSONObject config)
```

Create a data alert for the specified view.

| Parameter | Description |
|---|---|
| `alertName` | Name of the data alert. |
| `scheduleDetails` | Contains the schedule configurations of the data alert. |
| `rules` | Contains the rules to be evaluated by the data alert. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — A `long` of new data alert id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### createPrivateURL

```java
String createPrivateURL(JSONObject config)
```

Create a private URL for the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`String`) — A `String` of private URL.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### createSimilarViews

```java
void createSimilarViews(long refViewId, long folderId, JSONObject config)
```

Create reports for the specified table based on the reference table.

| Parameter | Description |
|---|---|
| `refViewId` | The ID of the reference view. |
| `folderId` | The folder id where the views to be saved. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### delete

```java
void delete(JSONObject config)
```

Delete a specified view in the workspace.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### deleteAggregateFormula

```java
void deleteAggregateFormula(long formulaId, JSONObject config)
```

Delete the specified aggregate formula.

| Parameter | Description |
|---|---|
| `formulaId` | Id of the aggregate formula to be deleted. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### deleteColumn

```java
void deleteColumn(long columnId, JSONObject config)
```

Delete a specified column in the table.

| Parameter | Description |
|---|---|
| `columnId` | The id of the column. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### deleteFormulaColumn

```java
void deleteFormulaColumn(long formulaId, JSONObject config)
```

Delete the specified formula column.

| Parameter | Description |
|---|---|
| `formulaId` | Id of the formula column to be deleted. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### deleteRow

```java
int deleteRow(String criteria, JSONObject config)
```

Delete rows in the specified table.

| Parameter | Description |
|---|---|
| `criteria` | The criteria to be applied for deleting data. Only rows matching the criteria will be deleted. Should be null for delete all rows. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`int`) — A `int` of deleted rows count.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### editAggregateFormula

```java
void editAggregateFormula(long formulaId, String expression, JSONObject config)
```

Edit the specified aggregate formula.

| Parameter | Description |
|---|---|
| `formulaId` | Id of the aggregate formula to be updated. |
| `expression` | Formula expression. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### editFormulaColumn

```java
void editFormulaColumn(long formulaId, String expression, JSONObject config)
```

Edit the specified formula column.

| Parameter | Description |
|---|---|
| `formulaId` | Id of the formula column to be updated. |
| `expression` | Formula expression. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getAggregateFormulas

```java
JSONArray getAggregateFormulas()
```

Returns list of all aggregate formulas for the specified table.

**Returns** (`JSONArray`) — A `JSONArray` of aggregate formulas.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getAlertsInView

```java
JSONArray getAlertsInView()
```

Returns list of data alerts configured for the specified view.

**Returns** (`JSONArray`) — A `JSONArray` of data alerts.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getColumnDependents

```java
JSONObject getColumnDependents(long columnId)
```

Returns list of dependents views and formulas for the specified column.

| Parameter | Description |
|---|---|
| `columnId` | Id of the column. |

**Returns** (`JSONObject`) — A `JSONObject` of dependent views and formulas.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getEmbedURL

```java
String getEmbedURL(JSONObject config)
```

Returns embed URL to access the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`String`) — A `String` of Embed URL.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getFormulaColumns

```java
JSONArray getFormulaColumns()
```

Returns list of all formula columns for the specified table.

**Returns** (`JSONArray`) — A `JSONArray` of custom formulas.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getLastImportDetails

```java
JSONObject getLastImportDetails()
```

Returns last import details of the specified view.

**Returns** (`JSONObject`) — A `JSONObject` of last import details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getMyPermissions

```java
JSONObject getMyPermissions()
```

Returns permissions for the specified view.

**Returns** (`JSONObject`) — A `JSONObject` of permission details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getPrivateURL

```java
String getPrivateURL(JSONObject config)
```

Returns private URL to access the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`String`) — A `String` of private URL.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getPublishConfigurations

```java
JSONObject getPublishConfigurations()
```

Returns publish configurations for the specified view.

**Returns** (`JSONObject`) — A `JSONObject` of publish details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getTableMetadata

```java
JSONObject getTableMetadata()
```

Retrieves metadata information for the current table, including the list of available columns and their attributes.

**Returns** (`JSONObject`) — A `JSONObject` containing table metadata.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getViewDependents

```java
JSONArray getViewDependents()
```

Returns list of dependents views for the specified view.

**Returns** (`JSONArray`) — A `JSONArray` of dependent views.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getViewMetadataForAlert

```java
JSONObject getViewMetadataForAlert()
```

Returns the view metadata that can be used while configuring a data alert for the specified view.

**Returns** (`JSONObject`) — A `JSONObject` of view metadata for data alert configuration.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getViewTags

```java
JSONArray getViewTags()
```

Returns the list of tags associated with the specified view.

**Returns** (`JSONArray`) — A `JSONArray` of tags.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getViewURL

```java
String getViewURL(JSONObject config)
```

Returns the URL to access the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`String`) — A `String` of view URL.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### hideColumns

```java
void hideColumns(JSONArray columnIds)
```

Hide the specified columns in the table.

| Parameter | Description |
|---|---|
| `columnIds` | The array of column ids to be hidden. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### makeViewPublic

```java
String makeViewPublic(JSONObject config)
```

Make the specified view publically accessible.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`String`) — A `String` of public URL.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### refetchData

```java
void refetchData(JSONObject config)
```

Sync data from available datasource for the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### removeFavorite

```java
void removeFavorite()
```

Remove a specified view from favorite.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### removeLookup

```java
void removeLookup(long columnId, JSONObject config)
```

Remove the lookup for the specified column in the table.

| Parameter | Description |
|---|---|
| `columnId` | The id of the column. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### removePrivateAccess

```java
void removePrivateAccess()
```

Remove private link access for the specified view.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### removePublicAccess

```java
void removePublicAccess()
```

Remove public access for the specified view.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### removeTagsFromView

```java
void removeTagsFromView(JSONArray tagIds, boolean dissociateAll, JSONObject config)
```

Removes multiple tags from the specified view.

| Parameter | Description |
|---|---|
| `tagIds` | List of tag ids to be dissociated. Can be null when dissociateAll is true. |
| `dissociateAll` | To dissociate all the associated tags from the view. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### rename

```java
void rename(String viewName, JSONObject config)
```

Rename a specified view in the workspace.

| Parameter | Description |
|---|---|
| `viewName` | The new name of the view. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### renameColumn

```java
void renameColumn(long columnId, String columnName)
```

Rename a specified column in the table.

| Parameter | Description |
|---|---|
| `columnId` | The id of the column. |
| `columnName` | The new name of the column. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### reorderColumns

```java
void reorderColumns(JSONArray columnIds, JSONObject config)
```

Updates the column order of the current table.

| Parameter | Description |
|---|---|
| `columnIds` | JSONArray containing the full set of column IDs in the new order in which they should appear. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### saveAs

```java
long saveAs(String newViewName, JSONObject config)
```

Copy a specified view within the workspace.

| Parameter | Description |
|---|---|
| `newViewName` | The name of the new view. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — A `long` of view id.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### showColumns

```java
void showColumns(JSONArray columnIds)
```

Show the specified hidden columns in the table.

| Parameter | Description |
|---|---|
| `columnIds` | The array of column ids to be shown. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### sortDataByColumns

```java
void sortDataByColumns(JSONArray columnIds, Integer sortOrder, boolean resetSort, JSONObject config)
```

Sorts the data in the current table based on specified columns.

| Parameter | Description |
|---|---|
| `columnIds` | JSONArray of column IDs to sort by. |
| `sortOrder` | Sorting order: 1 - Ascending 2 - Descending |
| `resetSort` | If true, resets existing sort configuration. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### updatePublishConfigurations

```java
void updatePublishConfigurations(JSONObject config)
```

Update publish configurations for the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains the control configurations. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### updateRow

```java
JSONObject updateRow(JSONObject columnValues, String criteria, JSONObject config)
```

Update rows in the specified table.

| Parameter | Description |
|---|---|
| `columnValues` | Contains the values for the row. The column names are the key. |
| `criteria` | The criteria to be applied for updating data. Only rows matching the criteria will be updated. Should be null for update all rows. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JSONObject`) — A `JSONObject` of values of the updated rows.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### UpdateSharedDetails

```java
void UpdateSharedDetails(JSONObject config)
```

Update the existing sharing configuration for the specified view.

| Parameter | Description |
|---|---|
| `config` | Contains the required control configurations. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
