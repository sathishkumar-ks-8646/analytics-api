# BulkAPI

```php
$org       = $ac->getOrgInstance($org_id);
$workspace = $ac->getWorkspaceInstance($org_id, $workspace_id);
$view      = $ac->getViewInstance($org_id, $workspace_id, $view_id);
$bulk      = $ac->getBulkInstance($org_id, $workspace_id);
```

`BulkAPI` exposes **16 methods**. Method names are `camelCase` and identifiers are `string`.

## Methods

[`exportBulkData`](#exportbulkdata), [`exportBulkDataStream`](#exportbulkdatastream), [`exportData`](#exportdata), [`exportDataStream`](#exportdatastream), [`getExportJobDetails`](#getexportjobdetails), [`getImportJobDetails`](#getimportjobdetails), [`importBulkData`](#importbulkdata), [`importBulkDataAsBatches`](#importbulkdataasbatches), [`importBulkDataInNewTable`](#importbulkdatainnewtable), [`importBulkDataInNewTableAsBatches`](#importbulkdatainnewtableasbatches), [`importData`](#importdata), [`importDataInNewTable`](#importdatainnewtable), [`importRawData`](#importrawdata), [`importRawDataInNewTable`](#importrawdatainnewtable), [`initiateBulkExport`](#initiatebulkexport), [`initiateBulkExportUsingSQL`](#initiatebulkexportusingsql)

### exportBulkData

```php
exportBulkData($job_id, $file_path)
```

Download the exported data for the mentioned job id.

| Parameter | Type | Description |
|---|---|---|
| `job_id` | `string` | Id of the job. |
| `file_path` | `string` | Path of the file where the data exported to be stored. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### exportBulkDataStream

```php
exportBulkDataStream($job_id)
```

Download exported bulk data for the specified job id as a stream.

| Parameter | Type | Description |
|---|---|---|
| `job_id` | `string` | Id of the export job. |

**Returns** — PHP stream object containing the exported data.

**Raises** — `ServerException`; `ParseException`

### exportData

```php
exportData($view_id, $response_format, $file_path, $config = array()
```

Export the mentioned table (or) view data.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view to be exported. |
| `response_format` | `string` | The format in which the data is to be exported. |
| `file_path` | `string` | Path of the file where the data exported to be stored. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Raises** — `IOException`; `ServerException`; `ParseException`

### exportDataStream

```php
exportDataStream($view_id, $response_format, $config = array()
```

Export the specified view data as a stream.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view to be exported. |
| `response_format` | `string` | Format in which the data is to be exported. |
| `config` | `array` | Optional configuration parameters. |

**Returns** — PHP stream object containing the exported data.

**Raises** — `ServerException`; `ParseException`

### getExportJobDetails

```php
getExportJobDetails($job_id)
```

Returns the details of the export job.

| Parameter | Type | Description |
|---|---|---|
| `job_id` | `string` | Id of the job. |

**Returns** — Export job details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### getImportJobDetails

```php
getImportJobDetails($job_id)
```

Returns the details of the import job.

| Parameter | Type | Description |
|---|---|---|
| `job_id` | `string` | Id of the job. |

**Returns** — Import job details.

**Raises** — `IOException`; `ServerException`; `ParseException`

### importBulkData

```php
importBulkData($view_id, $import_type, $file_type, $auto_identify, $file_path, $config = array()
```

Asynchronously import the data contained in the mentioned file into the table.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view where the data to be imported. |
| `import_type` | `string` | The type of import. Can be one of - append, truncateadd, updateadd. |
| `file_type` | `string` | Type of the file to be imported. |
| `auto_identify` | `string` | Used to specify whether to auto identify the CSV format. |
| `file_path` | `string` | Path of the file to be imported. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Import job id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### importBulkDataAsBatches

```php
importBulkDataAsBatches($view_id, $import_type, $auto_identify, $file_path, $batch_size, $config = array()
```

Asynchronously import the data contained in the mentioned file into the table.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view where the data to be imported. |
| `import_type` | `string` | The type of import. Can be one of - append, truncateadd, updateadd. |
| `auto_identify` | `string` | Used to specify whether to auto identify the CSV format. |
| `file_path` | `string` | Path of the file to be imported. |
| `batch_size` | `int` | Number of lines per batch. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Import job id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### importBulkDataInNewTable

```php
importBulkDataInNewTable($table_name, $file_type, $auto_identify, $file_path, $config = array()
```

Asynchronously create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Type | Description |
|---|---|---|
| `table_name` | `string` | Name of the new table to be created. |
| `file_type` | `string` | Type of the file to be imported. |
| `auto_identify` | `string` | Used to specify whether to auto identify the CSV format. |
| `file_path` | `string` | Path of the file to be imported. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Import job id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### importBulkDataInNewTableAsBatches

```php
importBulkDataInNewTableAsBatches($table_name, $auto_identify, $file_path, $batch_size, $config = array()
```

Asynchronously create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Type | Description |
|---|---|---|
| `table_name` | `string` | Name of the new table to be created. |
| `auto_identify` | `string` | Used to specify whether to auto identify the CSV format. |
| `file_path` | `string` | Path of the file to be imported. |
| `batch_size` | `int` | Number of lines per batch. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Import job id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### importData

```php
importData($view_id, $import_type, $file_type, $auto_identify, $file_path, $config = array()
```

Import the data contained in the mentioned file into the table.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view where the data to be imported. |
| `import_type` | `string` | The type of import. Can be one of - append, truncateadd, updateadd. |
| `file_type` | `string` | Type of the file to be imported. |
| `auto_identify` | `string` | Used to specify whether to auto identify the CSV format. |
| `file_path` | `string` | Path of the file to be imported. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Import result.

**Raises** — `IOException`; `ServerException`; `ParseException`

### importDataInNewTable

```php
importDataInNewTable($table_name, $file_type, $auto_identify, $file_path, $config = array()
```

Create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Type | Description |
|---|---|---|
| `table_name` | `string` | Name of the new table to be created. |
| `file_type` | `string` | Type of the file to be imported. |
| `auto_identify` | `string` | Used to specify whether to auto identify the CSV format. |
| `file_path` | `string` | Path of the file to be imported. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Import result.

**Raises** — `IOException`; `ServerException`; `ParseException`

### importRawData

```php
importRawData($view_id, $import_type, $file_type, $auto_identify, $data, $config = array()
```

Import the data contained in the mentioned file into the table.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view where the data to be imported. |
| `import_type` | `string` | The type of import. Can be one of - append, truncateadd, updateadd. |
| `file_type` | `string` | Type of the file to be imported. |
| `auto_identify` | `string` | Used to specify whether to auto identify the CSV format. |
| `data` | `string` | Raw data to be imported. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Import result.

**Raises** — `IOException`; `ServerException`; `ParseException`

### importRawDataInNewTable

```php
importRawDataInNewTable($table_name, $file_type, $auto_identify, $data, $config = array()
```

Create a new table and import the raw data provided into the created table.

| Parameter | Type | Description |
|---|---|---|
| `table_name` | `string` | Name of the new table to be created. |
| `file_type` | `string` | Type of the file to be imported. |
| `auto_identify` | `string` | Used to specify whether to auto identify the CSV format. |
| `data` | `string` | Raw data to be imported. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Import result.

**Raises** — `IOException`; `ServerException`; `ParseException`

### initiateBulkExport

```php
initiateBulkExport($view_id, $response_format, $config = array()
```

Initiate asynchronous export for the mentioned table (or) view data.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view to be exported. |
| `response_format` | `string` | The format in which the data is to be exported. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Export job id.

**Raises** — `IOException`; `ServerException`; `ParseException`

### initiateBulkExportUsingSQL

```php
initiateBulkExportUsingSQL($sql_query, $response_format, $config = array()
```

Initiate asynchronous export with the given SQL Query.

| Parameter | Type | Description |
|---|---|---|
| `sql_query` | `string` | The SQL Query whose output is exported. |
| `response_format` | `string` | The format in which the data is to be exported. |
| `config` | `array()` | Contains any additional control parameters. Can be null. |

**Returns** — Export job id.

**Raises** — `IOException`; `ServerException`; `ParseException`

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
