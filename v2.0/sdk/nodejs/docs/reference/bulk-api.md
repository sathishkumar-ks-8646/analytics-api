# BulkAPI

```javascript
var org       = ac.getOrgInstance(orgId);
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
var view      = ac.getViewInstance(orgId, workspaceId, viewId);
var bulk      = ac.getBulkInstance(orgId, workspaceId);
```

`BulkAPI` exposes **16 methods**. Method names are `camelCase` and identifiers are `string`.

## Methods

[`exportBulkData`](#exportbulkdata), [`exportBulkDataStream`](#exportbulkdatastream), [`exportData`](#exportdata), [`exportDataStream`](#exportdatastream), [`getExportJobDetails`](#getexportjobdetails), [`getImportJobDetails`](#getimportjobdetails), [`importBulkData`](#importbulkdata), [`importBulkDataAsBatches`](#importbulkdataasbatches), [`importBulkDataInNewTable`](#importbulkdatainnewtable), [`importData`](#importdata), [`importDataInNewTable`](#importdatainnewtable), [`importDataInNewTableAsBatches`](#importdatainnewtableasbatches), [`importRawData`](#importrawdata), [`importRawDataInNewTable`](#importrawdatainnewtable), [`initiateBulkExport`](#initiatebulkexport), [`initiateBulkExportUsingSQL`](#initiatebulkexportusingsql)

### exportBulkData

```javascript
exportBulkData(jobId, filePath)
```

Download the exported data for the mentioned job id.

| Parameter | Type | Description |
|---|---|---|
| `jobId` | `String` | Id of the job to be exported. |
| `filePath` | `String` | Path of the file where the data exported to be stored. |

**Raises** — `Error`

### exportBulkDataStream

```javascript
exportBulkDataStream(jobId)
```

Download the exported bulk data for the given job id as a stream.

| Parameter | Type | Description |
|---|---|---|
| `jobId` | `String` | Export job id |

**Returns** — - Stream containing exported data

### exportData

```javascript
exportData(viewId, responseFormat, filePath, config={})
```

Export the mentioned table (or) view data.

| Parameter | Type | Description |
|---|---|---|
| `viewId` | `String` | Id of the view to be exported. |
| `responseFormat` | `String` | The format in which the data is to be exported. |
| `filePath` | `String` | Path of the file where the data exported to be stored. |
| `config` | `Object` | Contains any additional control attributes. |

**Raises** — `Error`

### exportDataStream

```javascript
exportDataStream(viewId, responseFormat, config = {})
```

Export the mentioned table (or) view data as a stream.

| Parameter | Type | Description |
|---|---|---|
| `viewId` | `String` | Id of the view to be exported |
| `responseFormat` | `String` | Export format (csv, xls, json, etc.) |
| `config` | `Object` | Additional control parameters (optional) |

**Returns** — - Stream containing exported data

### getExportJobDetails

```javascript
getExportJobDetails(jobId)
```

Returns the details of the export job.

| Parameter | Type | Description |
|---|---|---|
| `jobId` | `String` | Id of the export job. |

**Returns** — Export job details.

**Raises** — `Error`

### getImportJobDetails

```javascript
getImportJobDetails(jobId)
```

Returns the details of the import job.

| Parameter | Type | Description |
|---|---|---|
| `jobId` | `String` | Id of the job. |

**Returns** — Import job details.

**Raises** — `Error`

### importBulkData

```javascript
importBulkData(viewId, importType, fileType, autoIdentify, filePath, config={})
```

Asynchronously import the data contained in the mentioned file into the table.

| Parameter | Type | Description |
|---|---|---|
| `viewId` | `String` | Id of the view where the data to be imported. |
| `importType` | `String` | The type of import. Can be one of - append, truncateadd, updateadd. |
| `fileType` | `String` | Type of the file to be imported. |
| `autoIdentify` | `String` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `filePath` | `String` | Path of the file to be imported. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Import job id.

**Raises** — `Error`

### importBulkDataAsBatches

```javascript
importBulkDataAsBatches(viewId, importType, autoIdentify, filePath, batchSize, config={})
```

Asynchronously import the data contained in the mentioned file into the table.

| Parameter | Type | Description |
|---|---|---|
| `viewId` | `String` | Id of the view where the data to be imported. |
| `importType` | `String` | The type of import. Can be one of - append, truncateadd, updateadd. |
| `autoIdentify` | `String` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `filePath` | `String` | Path of the file to be imported. |
| `batchSize` | `Number` | Number of lines per batch. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Import job id.

**Raises** — `Error`

### importBulkDataInNewTable

```javascript
importBulkDataInNewTable(tableName, fileType, autoIdentify, filePath, config={})
```

Asynchronously create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Type | Description |
|---|---|---|
| `tableName` | `String` | Name of the new table to be created. |
| `fileType` | `String` | Type of the file to be imported. |
| `autoIdentify` | `String` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `filePath` | `String` | Path of the file to be imported. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Import job id.

**Raises** — `Error`

### importData

```javascript
importData(viewId, importType, fileType, autoIdentify, filePath, config={})
```

Import the data contained in the mentioned file into the table.

| Parameter | Type | Description |
|---|---|---|
| `viewId` | `String` | Id of the view where the data to be imported. |
| `importType` | `String` | The type of import. Can be one of - append, truncateadd, updateadd. |
| `fileType` | `String` | Type of the file to be imported. |
| `autoIdentify` | `String` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `filePath` | `String` | Path of the file to be imported. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Import result.

**Raises** — `Error`

### importDataInNewTable

```javascript
importDataInNewTable(tableName, fileType, autoIdentify, filePath, config={})
```

Create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Type | Description |
|---|---|---|
| `tableName` | `String` | Name of the new table to be created. |
| `fileType` | `String` | Type of the file to be imported. |
| `autoIdentify` | `String` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `filePath` | `String` | Path of the file to be imported. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Import result.

**Raises** — `Error`

### importDataInNewTableAsBatches

```javascript
importDataInNewTableAsBatches(tableName, autoIdentify, filePath, batchSize, config={})
```

Create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Type | Description |
|---|---|---|
| `tableName` | `String` | Name of the new table to be created. |
| `fileType` | `String` | Type of the file to be imported. |
| `autoIdentify` | `String` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `filePath` | `String` | Path of the file to be imported. |
| `batchSize` | `Number` | Number of lines per batch. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Import result.

**Raises** — `Error`

### importRawData

```javascript
importRawData(viewId, importType, fileType, autoIdentify, data, config={})
```

Import the raw data provided into the table.

| Parameter | Type | Description |
|---|---|---|
| `viewId` | `String` | Id of the view where the data to be imported. |
| `importType` | `String` | The type of import. Can be one of - append, truncateadd, updateadd. |
| `fileType` | `String` | Type of the file to be imported. |
| `autoIdentify` | `String` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `data` | `String` | Raw data to be imported. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Import result.

**Raises** — `Error`

### importRawDataInNewTable

```javascript
importRawDataInNewTable(tableName, fileType, autoIdentify, data, config={})
```

Create a new table and import the raw data provided into the created table.

| Parameter | Type | Description |
|---|---|---|
| `tableName` | `String` | Name of the new table to be created. |
| `fileType` | `String` | Type of the file to be imported. |
| `autoIdentify` | `String` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `data` | `String` | Raw data to be imported. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Import result.

**Raises** — `Error`

### initiateBulkExport

```javascript
initiateBulkExport(viewId, responseFormat, config={})
```

Initiate asynchronous export for the mentioned table (or) view data.

| Parameter | Type | Description |
|---|---|---|
| `viewId` | `String` | Id of the view to be exported. |
| `responseFormat` | `String` | The format in which the data is to be exported. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Export job id.

**Raises** — `Error`

### initiateBulkExportUsingSQL

```javascript
initiateBulkExportUsingSQL(sqlQuery, responseFormat, config={})
```

Initiate asynchronous export with the given SQL Query.

| Parameter | Type | Description |
|---|---|---|
| `sqlQuery` | `String` | The SQL Query whose output is exported. |
| `responseFormat` | `String` | The format in which the data is to be exported. |
| `config` | `Object` | Contains any additional control attributes. |

**Returns** — Export job id.

**Raises** — `Error`

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
