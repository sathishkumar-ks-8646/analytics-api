# BulkAPI

```go
org       := ZAnalytics.GetOrgInstance(&ac, orgId)
workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
view      := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
bulk      := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
```

`BulkAPI` exposes **14 methods**. Method names are `PascalCase` (exported) and identifiers are `string`.

## Methods

[`ExportBulkData`](#exportbulkdata), [`ExportData`](#exportdata), [`GetExportJobDetails`](#getexportjobdetails), [`GetImportJobDetails`](#getimportjobdetails), [`ImportBulkData`](#importbulkdata), [`ImportBulkDataAsBatches`](#importbulkdataasbatches), [`ImportBulkDataInNewTable`](#importbulkdatainnewtable), [`ImportBulkDataInNewTableAsBatches`](#importbulkdatainnewtableasbatches), [`ImportData`](#importdata), [`ImportDataInNewTable`](#importdatainnewtable), [`ImportRawData`](#importrawdata), [`ImportRawDataInNewTable`](#importrawdatainnewtable), [`InitiateBulkExport`](#initiatebulkexport), [`InitiateBulkExportUsingSQL`](#initiatebulkexportusingsql)

### ExportBulkData

```go
ExportBulkData(jobid, filepath string) (serverexception *ServerException)
```

Download the exported data for the mentioned job id.

| Parameter | Description |
|---|---|
| `jobid` | Returns the export job id. |
| `filepath` | Path of the file where the data exported to be stored. |

### ExportData

```go
ExportData(viewid, responseformat, filepath string, config map[string]interface{}) (serverexception *ServerException)
```

Export the mentioned table (or) view data.

| Parameter | Description |
|---|---|
| `viewid` | Id of the view to be exported. |
| `responseformat` | The format in which the data is to be exported. |
| `filepath` | Path of the file where the data exported to be stored. |
| `config` | Contains the control configurations. |

### GetExportJobDetails

```go
GetExportJobDetails(jobid string) (result interface{}, serverexception *ServerException)
```

| Parameter | Description |
|---|---|
| `jobid` | Id of the export job. |

**Returns** — Returns the export job details as interface.

### GetImportJobDetails

```go
GetImportJobDetails(jobid string) (result interface{}, serverexception *ServerException)
```

Returns the details of the import job.

| Parameter | Description |
|---|---|
| `jobid` | Id of the import job. |

**Returns** — Returns the import job details as interface.

### ImportBulkData

```go
ImportBulkData(viewid, importtype, filetype, autoidentify, filepath string, config map[string]interface{}) (jobid string, serverexception *ServerException)
```

Asynchronously import the data contained in the mentioned file into the table.

| Parameter | Description |
|---|---|
| `viewid` | Id of the view where the data to be imported. |
| `importtype` | The type of import. Can be one of - append, truncateadd, updateadd. |
| `filetype` | Type of the file to be imported. |
| `autoidentify` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `filepath` | Path of the file to be imported. |
| `config` | Contains the control configurations. |

**Returns** — Returns the import job id.

### ImportBulkDataAsBatches

```go
ImportBulkDataAsBatches(viewid, importtype, autoidentify, filepath string, batchSize int, config map[string]interface{}) (jobid string, serverexception *ServerException)
```

| Parameter | Description |
|---|---|
| `viewid` | Id of the view where the data to be imported. |
| `importtype` | The type of import. Can be one of - append, truncateadd, updateadd. |
| `autoidentify` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `filepath` | Path of the file to be imported. |
| `batchSize` | Number of lines per batch. |
| `config` | Contains the control configurations. |

**Returns** — Returns the import job id.

### ImportBulkDataInNewTable

```go
ImportBulkDataInNewTable(tablename, filetype, autoidentify, filepath string, config map[string]interface{}) (jobid string, serverexception *ServerException)
```

Asynchronously create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Description |
|---|---|
| `tablename` | Name of the new table to be created. |
| `filetype` | Type of the file to be imported. |
| `autoidentify` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `filepath` | Path of the file to be imported. |
| `config` | Contains the control configurations. |

**Returns** — Returns the import job id.

### ImportBulkDataInNewTableAsBatches

```go
ImportBulkDataInNewTableAsBatches(tablename, autoidentify, filepath string, batchSize int, config map[string]interface{}) (jobid string, serverexception *ServerException)
```

| Parameter | Description |
|---|---|
| `tablename` | Name of the new table to be created. |
| `autoidentify` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `filepath` | Path of the file to be imported. |
| `batchSize` | Number of lines per batch |
| `config` | Contains the control configurations. |

**Returns** — Returns the import job id.

### ImportData

```go
ImportData(viewid, importtype, filetype, autoidentify, filepath string, config map[string]interface{}) (result interface{}, serverexception *ServerException)
```

Create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Description |
|---|---|
| `viewid` | Id of the view where the data to be imported. |
| `importtype` | The type of import. Can be one of - append, truncateadd, updateadd. |
| `filetype` | Type of the file to be imported. |
| `autoidentify` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `filepath` | Path of the file to be imported. |
| `config` | Contains the control configurations. |

**Returns** — Returns the import result as interface.

### ImportDataInNewTable

```go
ImportDataInNewTable(tablename, filetype, autoidentify, filepath string, config map[string]interface{}) (result interface{}, serverexception *ServerException)
```

Create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Description |
|---|---|
| `tablename` | Name of the new table to be created. |
| `filetype` | Type of the file to be imported. |
| `autoidentify` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `filepath` | Path of the file to be imported. |
| `config` | Contains the control configurations. |

**Returns** — Returns the import result as interface.

### ImportRawData

```go
ImportRawData(viewid, importtype, filetype, autoidentify, data string, config map[string]interface{}) (result interface{}, serverexception *ServerException)
```

Import the raw data provided into the table.

| Parameter | Description |
|---|---|
| `viewid` | Id of the view where the data to be imported. |
| `importtype` | The type of import. Can be one of - append, truncateadd, updateadd. |
| `filetype` | Type of the file to be imported. |
| `autoidentify` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `data` | Raw data to be imported. |
| `config` | Contains the control configurations. |

**Returns** — Returns the import result as interface.

### ImportRawDataInNewTable

```go
ImportRawDataInNewTable(tablename, filetype, autoidentify, data string, config map[string]interface{}) (result interface{}, serverexception *ServerException)
```

Create a new table and import the raw data provided into the created table.

| Parameter | Description |
|---|---|
| `tablename` | Name of the new table to be created. |
| `filetype` | Type of the file to be imported. |
| `autoidentify` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `data` | Raw data to be imported. |
| `config` | Contains the control configurations. |

**Returns** — Returns the import result as interface.

### InitiateBulkExport

```go
InitiateBulkExport(viewid, responseformat string, config map[string]interface{}) (jobid string, serverexception *ServerException)
```

Initiate asynchronous export for the mentioned table (or) view data.

| Parameter | Description |
|---|---|
| `viewid` | Id of the view to be exported. |
| `responseformat` | The format in which the data is to be exported. |
| `config` | Contains the control configurations. |

**Returns** — Returns the export job id.

### InitiateBulkExportUsingSQL

```go
InitiateBulkExportUsingSQL(sqlquery, responseformat string, config map[string]interface{}) (jobid string, serverexception *ServerException)
```

Initiate asynchronous export with the given SQL Query.

| Parameter | Description |
|---|---|
| `sqlquery` | The SQL Query whose output is exported. |
| `responseformat` | The format in which the data is to be exported. |
| `config` | Contains the control configurations. |

**Returns** — Returns the export job id.

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
