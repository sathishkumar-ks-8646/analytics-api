# BulkAPI

```python
org       = ac.get_org_instance(ORG_ID)
workspace = ac.get_workspace_instance(ORG_ID, WORKSPACE_ID)
view      = ac.get_view_instance(ORG_ID, WORKSPACE_ID, VIEW_ID)
bulk      = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)
```

`BulkAPI` exposes **16 methods**. Method names are `snake_case` and identifiers are `str`.

## Methods

[`export_bulk_data`](#export-bulk-data), [`export_bulk_data_stream`](#export-bulk-data-stream), [`export_data`](#export-data), [`export_data_stream`](#export-data-stream), [`get_export_job_details`](#get-export-job-details), [`get_import_job_details`](#get-import-job-details), [`import_bulk_data`](#import-bulk-data), [`import_bulk_data_in_new_table`](#import-bulk-data-in-new-table), [`import_data`](#import-data), [`import_data_as_batches`](#import-data-as-batches), [`import_data_in_new_table`](#import-data-in-new-table), [`import_data_in_new_table_as_batches`](#import-data-in-new-table-as-batches), [`import_raw_data`](#import-raw-data), [`import_raw_data_in_new_table`](#import-raw-data-in-new-table), [`initiate_bulk_export`](#initiate-bulk-export), [`initiate_bulk_export_using_sql`](#initiate-bulk-export-using-sql)

### export_bulk_data

```python
export_bulk_data(job_id, file_path)
```

Download the exported data for the mentioned job id.

| Parameter | Type | Description |
|---|---|---|
| `job_id` | `string` | Id of the job to be exported. |
| `file_path` | `string` | Path of the file where the data exported to be stored. |

**Raises** — `ServerError`; `ParseError`

### export_bulk_data_stream

```python
export_bulk_data_stream(job_id)
```

Download the exported data for the mentioned job id as stream.

| Parameter | Type | Description |
|---|---|---|
| `job_id` | `string` | Id of the job to be exported. |

**Returns** (`urllib3.response.HTTPResponse`) — A stream object containing the exported data.

**Raises** — `ServerError`; `ParseError`

### export_data

```python
export_data(view_id, response_format, file_path, config = {})
```

Export the mentioned table (or) view data.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view to be exported. |
| `response_format` | `string` | The format in which the data is to be exported. |
| `file_path` | `string` | Path of the file where the data exported to be stored. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Raises** — `ServerError`; `ParseError`

### export_data_stream

```python
export_data_stream(view_id, response_format, config={})
```

Export the mentioned table (or) view data.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view to be exported. |
| `response_format` | `string` | The format in which the data is to be exported. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`urllib3.response.HTTPResponse`) — A stream object containing the exported data.

**Raises** — `ServerError`; `ParseError`

### get_export_job_details

```python
get_export_job_details(job_id)
```

Returns the details of the export job.

| Parameter | Type | Description |
|---|---|---|
| `job_id` | `string` | Id of the export job. |

**Returns** (`dictionary`) — Export job details

**Raises** — `ServerError`; `ParseError`

### get_import_job_details

```python
get_import_job_details(job_id)
```

Returns the details of the import job.

| Parameter | Type | Description |
|---|---|---|
| `job_id` | `string` | Id of the job. |

**Returns** (`dictionary`) — Import job details

**Raises** — `ServerError`; `ParseError`

### import_bulk_data

```python
import_bulk_data(view_id, import_type, file_type, auto_identify, file_path, config = {})
```

Asynchronously import the data contained in the mentioned file into the table.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view where the data to be imported. |
| `import_type` | `string` | The type of import. Can be one of - append, truncateadd, updateadd. |
| `file_type` | `string` | Type of the file to be imported. |
| `auto_identify` | `string` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `file_path` | `string` | Path of the file to be imported. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Import job id

**Raises** — `ServerError`; `ParseError`

### import_bulk_data_in_new_table

```python
import_bulk_data_in_new_table(table_name, file_type, auto_identify, file_path, config = {})
```

Asynchronously create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Type | Description |
|---|---|---|
| `table_name` | `string` | Name of the new table to be created. |
| `file_type` | `string` | Type of the file to be imported. |
| `auto_identify` | `string` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `file_path` | `string` | Path of the file to be imported. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Import job id

**Raises** — `ServerError`; `ParseError`

### import_data

```python
import_data(view_id, import_type, file_type, auto_identify, file_path, config = {})
```

Import the data contained in the mentioned file into the table.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view where the data to be imported. |
| `import_type` | `string` | The type of import. Can be one of - append, truncateadd, updateadd. |
| `file_type` | `string` | Type of the file to be imported. |
| `auto_identify` | `string` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `file_path` | `string` | Path of the file to be imported. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`dictionary`) — Import result

**Raises** — `ServerError`; `ParseError`

### import_data_as_batches

```python
import_data_as_batches(view_id, import_type, auto_identify, file_path, batch_size, config={}, tool_config={})
```

Asynchronously import the data contained in the mentioned file into the table.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view where the data to be imported. |
| `import_type` | `string` | The type of import. Can be one of - append, truncateadd, updateadd. |
| `auto_identify` | `string` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `file_path` | `string` | Path of the file to be imported. |
| `batch_size` | `int` | Number of lines per batch. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |
| `tool_config` | `dictionary` | Contains any additional control parameters for the library. Can be `null`. |

**Returns** (`string`) — Import job id

**Raises** — `ServerError`; `ParseError`

### import_data_in_new_table

```python
import_data_in_new_table(table_name, file_type, auto_identify, file_path, config = {})
```

Create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Type | Description |
|---|---|---|
| `table_name` | `string` | Name of the new table to be created. |
| `file_type` | `string` | Type of the file to be imported. |
| `auto_identify` | `string` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `file_path` | `string` | Path of the file to be imported. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`dictionary`) — Import result

**Raises** — `ServerError`; `ParseError`

### import_data_in_new_table_as_batches

```python
import_data_in_new_table_as_batches(table_name, auto_identify, file_path, batch_size, config={}, tool_config={})
```

Create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Type | Description |
|---|---|---|
| `table_name` | `string` | Name of the new table to be created. |
| `auto_identify` | `string` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `file_path` | `string` | Path of the file to be imported. |
| `batch_size` | `int` | Number of lines per batch. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |
| `tool_config` | `dictionary` | Contains any additional control parameters for the library. Can be `null`. |

**Returns** (`string`) — Import job id

**Raises** — `ServerError`; `ParseError`

### import_raw_data

```python
import_raw_data(view_id, import_type, file_type, auto_identify, data, config = {})
```

Import the raw data provided into the table.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view where the data to be imported. |
| `import_type` | `string` | The type of import. Can be one of - append, truncateadd, updateadd. |
| `file_type` | `string` | Type of the file to be imported. |
| `auto_identify` | `string` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `data` | `string` | Raw data to be imported. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`dictionary`) — Import result

**Raises** — `ServerError`; `ParseError`

### import_raw_data_in_new_table

```python
import_raw_data_in_new_table(table_name, file_type, auto_identify, data, config={})
```

Create a new table and import the raw data provided into the created table.

| Parameter | Type | Description |
|---|---|---|
| `table_name` | `string` | Name of the new table to be created. |
| `file_type` | `string` | Type of the file to be imported. |
| `auto_identify` | `string` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `data` | `string` | Raw data to be imported. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`dictionary`) — Import result

**Raises** — `ServerError`; `ParseError`

### initiate_bulk_export

```python
initiate_bulk_export(view_id, response_format, config = {})
```

Initiate asynchronous export for the mentioned table (or) view data.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `string` | Id of the view to be exported. |
| `response_format` | `string` | The format in which the data is to be exported. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Export job id

**Raises** — `ServerError`; `ParseError`

### initiate_bulk_export_using_sql

```python
initiate_bulk_export_using_sql(sql_query, response_format, config = {})
```

Initiate asynchronous export with the given SQL Query.

| Parameter | Type | Description |
|---|---|---|
| `sql_query` | `string` | SQL Query. |
| `response_format` | `string` | The format in which the data is to be exported. |
| `config` | `dictionary` | Contains any additional control parameters. Can be `null`. |

**Returns** (`string`) — Export job id

**Raises** — `ServerError`; `ParseError`

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
