# BulkAPI

```java
OrgAPI       org       = ac.getOrgInstance(orgId);
WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
ViewAPI      view      = ac.getViewInstance(orgId, workspaceId, viewId);
BulkAPI      bulk      = ac.getBulkInstance(orgId, workspaceId);
```

`BulkAPI` exposes **15 methods**. Method names are `camelCase`, matching the endpoint title and identifiers are `long`.

## Methods

[`exportBulkData`](#exportbulkdata), [`exportData`](#exportdata), [`getExportJobDetails`](#getexportjobdetails), [`getImportJobDetails`](#getimportjobdetails), [`handleCustomBatchImport`](#handlecustombatchimport), [`importBulkData`](#importbulkdata), [`importBulkDataInNewTable`](#importbulkdatainnewtable), [`importData`](#importdata), [`importDataAsBatches`](#importdataasbatches), [`importDataInNewTable`](#importdatainnewtable), [`importDataInNewTableAsBatches`](#importdatainnewtableasbatches), [`importRawData`](#importrawdata), [`importRawDataInNewTable`](#importrawdatainnewtable), [`initiateBulkExport`](#initiatebulkexport), [`initiateBulkExportUsingSQL`](#initiatebulkexportusingsql)

### exportBulkData

```java
void exportBulkData(long jobId, String filePath)
```

Download the exported data for the mentioned job id.

| Parameter | Description |
|---|---|
| `jobId` | Id of the job to be exported. |
| `filePath` | Path of the file where the data exported to be stored. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### exportData

```java
void exportData(long viewId, String responseFormat, String filePath, JSONObject config)
```

Export the mentioned table (or) view data.

| Parameter | Description |
|---|---|
| `viewId` | Id of the view to be exported. |
| `responseFormat` | The format in which the data is to be exported. |
| `filePath` | Path of the file where the data exported to be stored. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getExportJobDetails

```java
JSONObject getExportJobDetails(long jobId)
```

Returns the details of the export job.

| Parameter | Description |
|---|---|
| `jobId` | Id of the export job. |

**Returns** (`JSONObject`) — A `JSONObject` of export job details.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### getImportJobDetails

```java
JSONObject getImportJobDetails(long jobId)
```

Returns the details of the import job.

| Parameter | Description |
|---|---|
| `jobId` | Id of the import job. |

**Returns** (`JSONObject`) — A `JSONObject` of import result.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### handleCustomBatchImport

```java
JSONObject handleCustomBatchImport(long viewId, String filePath, JSONObject config)
```

### importBulkData

```java
long importBulkData(long viewId, String importType, String fileType, boolean autoIdentify, String filePath, JSONObject config)
```

Asynchronously import the data contained in the mentioned file into the table.

| Parameter | Description |
|---|---|
| `viewId` | Id of the view where the data to be imported. |
| `importType` | The type of import. Can be one of APPEND TRUNCATEADD UPDATEADD |
| `fileType` | Type of the file to be imported. |
| `autoIdentify` | Used to specify whether to auto identify the CSV format. |
| `filePath` | Path of the file to be imported. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — A `long` of job id created.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### importBulkDataInNewTable

```java
long importBulkDataInNewTable(String tableName, String fileType, boolean autoIdentify, String filePath, JSONObject config)
```

Asynchronously create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Description |
|---|---|
| `tableName` | Name of the new table to be created. |
| `fileType` | Type of the file to be imported. |
| `autoIdentify` | Used to specify whether to auto identify the CSV format. |
| `filePath` | Path of the file to be imported. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`long`) — A `long` of the job id created.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### importData

```java
JSONObject importData(long viewId, String importType, String fileType, boolean autoIdentify, String filePath, JSONObject config)
```

Import the data contained in the mentioned file into the table.

| Parameter | Description |
|---|---|
| `viewId` | Id of the view where the data to be imported. |
| `importType` | The type of import. Can be one of append truncateadd updateadd |
| `fileType` | Type of the file to be imported. |
| `autoIdentify` | Used to specify whether to auto identify the CSV format. |
| `filePath` | Path of the file to be imported. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JSONObject`) — A `JSONObject` of import result.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### importDataAsBatches

```java
long importDataAsBatches(long viewId, String importType, boolean autoIdentify, String filePath, int batchSize, JSONObject config, JSONObject toolConfig)
```

Asynchronously import the data contained in the mentioned file into the table.

| Parameter | Description |
|---|---|
| `viewId` | Id of the view where the data to be imported. |
| `importType` | The type of import. Can be one of APPEND TRUNCATEADD UPDATEADD |
| `autoIdentify` | Used to specify whether to auto identify the CSV format. |
| `filePath` | Path of the file to be imported. |
| `batchSize` | Number of lines per batch. |
| `config` | Contains any additional control configurations. Can be null. |
| `toolConfig` | Contains any additional control configurations for the parser tool. Can be null. |

**Returns** (`long`) — A `long` of job id created.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### importDataInNewTable

```java
JSONObject importDataInNewTable(String tableName, String fileType, boolean autoIdentify, String filePath, JSONObject config)
```

Create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Description |
|---|---|
| `tableName` | Name of the new table to be created. |
| `fileType` | Type of the file to be imported. |
| `autoIdentify` | Used to specify whether to auto identify the CSV format. |
| `filePath` | Path of the file to be imported. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JSONObject`) — A `JSONObject` of import result.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### importDataInNewTableAsBatches

```java
long importDataInNewTableAsBatches(String tableName, boolean autoIdentify, String filePath, int batchSize, JSONObject config, JSONObject toolConfig)
```

Create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Description |
|---|---|
| `tableName` | Name of the new table to be created. |
| `autoIdentify` | Used to specify whether to auto identify the CSV format. |
| `filePath` | Path of the file to be imported. |
| `batchSize` | Number of lines per batch. |
| `config` | Contains any additional control configurations. Can be null. |
| `toolConfig` | Contains any additional control configurations for the parser tool. Can be null. |

**Returns** (`long`) — A `long` of the job id created.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### importRawData

```java
JSONObject importRawData(long viewId, String importType, String fileType, boolean autoIdentify, String data, JSONObject config)
```

Import the raw data provided into the table.

| Parameter | Description |
|---|---|
| `viewId` | Id of the view where the data to be imported. |
| `importType` | The type of import. Can be one of APPEND TRUNCATEADD UPDATEADD |
| `fileType` | Type of the file to be imported. |
| `autoIdentify` | Used to specify whether to auto identify the CSV format. |
| `data` | Raw data to be imported. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JSONObject`) — A `JSONObject` of import result.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### importRawDataInNewTable

```java
JSONObject importRawDataInNewTable(String tableName, String fileType, boolean autoIdentify, String data, JSONObject config)
```

Create a new table and import the raw data provided into the created table.

| Parameter | Description |
|---|---|
| `tableName` | Name of the new table to be created. |
| `fileType` | Type of the file to be imported. |
| `autoIdentify` | Used to specify whether to auto identify the CSV format. |
| `data` | Raw data to be imported. |
| `config` | Contains any additional control configurations. Can be null. |

**Returns** (`JSONObject`) — A `JSONObject` of import result.

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### initiateBulkExport

```java
long initiateBulkExport(long viewId, String responseFormat, JSONObject config)
```

Initiate asynchronous export for the mentioned table (or) view data.

| Parameter | Description |
|---|---|
| `viewId` | Id of the view to be exported. |
| `responseFormat` | The format in which the data is to be exported. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

### initiateBulkExportUsingSQL

```java
long initiateBulkExportUsingSQL(String sqlQuery, String responseFormat, JSONObject config)
```

Initiate asynchronous export with the given SQL Query.

| Parameter | Description |
|---|---|
| `sqlQuery` | The SQL Query whose output is exported. |
| `responseFormat` | The format in which the data is to be exported. |
| `config` | Contains any additional control configurations. Can be null. |

**Raises** — `ServerException`; `ParseException`; `IOException`; `JSONException`

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
