# BulkAPI

```csharp
IOrgAPI       org       = ac.GetOrgInstance(orgId);
IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
IViewAPI      view      = ac.GetViewInstance(orgId, workspaceId, viewId);
IBulkAPI      bulk      = ac.GetBulkInstance(orgId, workspaceId);
```

`BulkAPI` exposes **14 methods**. Method names are `PascalCase` and identifiers are `long`.

## Methods

[`ExportBulkData`](#exportbulkdata), [`ExportData`](#exportdata), [`GetExportJobDetails`](#getexportjobdetails), [`GetImportJobDetails`](#getimportjobdetails), [`ImportBulkData`](#importbulkdata), [`ImportBulkDataAsBatches`](#importbulkdataasbatches), [`ImportBulkDataInNewTable`](#importbulkdatainnewtable), [`ImportBulkDataInNewTableAsBatches`](#importbulkdatainnewtableasbatches), [`ImportData`](#importdata), [`ImportDataInNewTable`](#importdatainnewtable), [`ImportRawData`](#importrawdata), [`ImportRawDataInNewTable`](#importrawdatainnewtable), [`InitiateBulkExport`](#initiatebulkexport), [`InitiateBulkExportUsingSQL`](#initiatebulkexportusingsql)

### ExportBulkData

```csharp
Stream ExportBulkData(long jobId)
```

Export the mentioned job id and return a live response stream. Caller is responsible for closing the stream.

| Parameter | Description |
|---|---|
| `jobId` | Id of the job to be exported. |

**Returns** (`Stream`) — Stream containing the exported data.

### ExportData

```csharp
Stream ExportData(long viewId, string responseFormat, Dictionary config = null)
```

/// Exports the specified table or view data and returns a stream containing the exported data.

| Parameter | Description |
|---|---|
| `viewId` | Id of the view to be exported. |
| `responseFormat` | The format in which the data has to be exported. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`Stream`) — Stream containing the exported data.

### GetExportJobDetails

```csharp
JsonElement GetExportJobDetails(long jobId)
```

Returns the details of the export job.

| Parameter | Description |
|---|---|
| `jobId` | Id of the export job. |

**Returns** (`JsonElement`) — Export job details.

### GetImportJobDetails

```csharp
JsonElement GetImportJobDetails(long jobId)
```

Returns the details of the import job.

| Parameter | Description |
|---|---|
| `jobId` | Id of the import job. |

**Returns** (`JsonElement`) — Import result.

### ImportBulkData

```csharp
long ImportBulkData(long viewId, string importType, string fileType, bool autoIdentify, string filePath, Dictionary config)
```

Asynchronously import the data contained in the mentioned file into the table.

| Parameter | Description |
|---|---|
| `viewId` | Id of the view where the data to be imported. |
| `importType` | The import type. |
| `fileType` | Type of the file to be imported. |
| `autoIdentify` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `filePath` | Path of the file to be imported. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — The created job id.

### ImportBulkDataAsBatches

```csharp
long ImportBulkDataAsBatches(long viewId, string importType, bool autoIdentify, string filePath, int batchSize, Dictionary config)
```

Import the data contained in the mentioned file into the table.

| Parameter | Description |
|---|---|
| `viewId` | Id of the view where the data to be imported. |
| `importType` | The import type. |
| `fileType` | Type of the file to be imported. |
| `autoIdentify` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `filePath` | Path of the file to be imported. |
| `batchSize` | Number of lines per batch. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — The created job id.

### ImportBulkDataInNewTable

```csharp
long ImportBulkDataInNewTable(string tableName, string fileType, bool autoIdentify, string filePath, Dictionary config)
```

Asynchronously create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Description |
|---|---|
| `tableName` | Name of the new table to be created. |
| `fileType` | Type of the file to be imported. |
| `autoIdentify` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `filePath` | Path of the file to be imported. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — The created job id.

### ImportBulkDataInNewTableAsBatches

```csharp
long ImportBulkDataInNewTableAsBatches(string tableName, bool autoIdentify, string filePath, int batchSize, Dictionary config)
```

Asynchronously create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Description |
|---|---|
| `tableName` | Name of the new table to be created. |
| `fileType` | Type of the file to be imported. |
| `autoIdentify` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `filePath` | Path of the file to be imported. |
| `batchSize` | Number of lines per batch. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — The created job id.

### ImportData

```csharp
JsonElement ImportData(long viewId, string importType, string fileType, bool autoIdentify, string filePath, Dictionary config)
```

Import the data contained in the mentioned file into the table.

| Parameter | Description |
|---|---|
| `viewId` | Id of the view where the data to be imported. |
| `importType` | The import type. |
| `fileType` | Type of the file to be imported. |
| `autoIdentify` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `filePath` | Path of the file to be imported. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JsonElement`) — Import result.

### ImportDataInNewTable

```csharp
JsonElement ImportDataInNewTable(string tableName, string fileType, bool autoIdentify, string filePath, Dictionary config)
```

Create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Description |
|---|---|
| `tableName` | Name of the new table to be created. |
| `fileType` | Type of the file to be imported. |
| `autoIdentify` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `filePath` | Path of the file to be imported. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JsonElement`) — Import result.

### ImportRawData

```csharp
JsonElement ImportRawData(long viewId, string importType, string fileType, bool autoIdentify, string rawData, Dictionary config)
```

Import the raw data provided into the table.

| Parameter | Description |
|---|---|
| `viewId` | Id of the view where the data to be imported. |
| `importType` | The import type. |
| `fileType` | Type of the file to be imported. |
| `autoIdentify` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `rawData` | Raw data to be imported. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JsonElement`) — Import result.

### ImportRawDataInNewTable

```csharp
JsonElement ImportRawDataInNewTable(string tableName, string fileType, bool autoIdentify, string rawData, Dictionary config)
```

Create a new table and import the raw data provided into the created table.

| Parameter | Description |
|---|---|
| `tableName` | Name of the new table to be created. |
| `fileType` | Type of the file to be imported. |
| `autoIdentify` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `rawData` | Raw data to be imported. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JsonElement`) — Import result.

### InitiateBulkExport

```csharp
long InitiateBulkExport(long viewId, string responseFormat, Dictionary config)
```

Initiate asynchronous export for the mentioned table (or) view data.

| Parameter | Description |
|---|---|
| `viewId` | Id of the view to be exported. |
| `responseFormat` | The format in which the data is to be exported. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — Export job id.

### InitiateBulkExportUsingSQL

```csharp
long InitiateBulkExportUsingSQL(string sqlQuery, string responseFormat, Dictionary config)
```

Initiate asynchronous export with the given SQL Query.

| Parameter | Description |
|---|---|
| `sqlQuery` | The SQL Query whose output is exported. |
| `responseFormat` | The format in which the data is to be exported. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — Export job id.

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
