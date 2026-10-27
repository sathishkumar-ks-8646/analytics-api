# BulkAPI

```ruby
org       = ac.get_org_instance(ORG_ID)
workspace = ac.get_workspace_instance(ORG_ID, WORKSPACE_ID)
view      = ac.get_view_instance(ORG_ID, WORKSPACE_ID, VIEW_ID)
bulk      = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)
```

`BulkAPI` exposes **14 methods**. Method names are `snake_case` and identifiers are `string`.

## Methods

[`export_bulk_data`](#export-bulk-data), [`export_data`](#export-data), [`get_export_job_details`](#get-export-job-details), [`get_import_job_details`](#get-import-job-details), [`import_bulk_data`](#import-bulk-data), [`import_bulk_data_in_new_table`](#import-bulk-data-in-new-table), [`import_data`](#import-data), [`import_data_as_batches`](#import-data-as-batches), [`import_data_in_new_table`](#import-data-in-new-table), [`import_data_in_new_table_as_batches`](#import-data-in-new-table-as-batches), [`import_raw_data`](#import-raw-data), [`import_raw_data_in_new_table`](#import-raw-data-in-new-table), [`initiate_bulk_export`](#initiate-bulk-export), [`initiate_bulk_export_using_sql`](#initiate-bulk-export-using-sql)

### export_bulk_data

```ruby
export_bulk_data(job_id, file_path)
```

Downloads the exported data for a given job ID.

| Parameter | Type | Description |
|---|---|---|
| `job_id` | `String` | ID of the export job to download. |
| `file_path` | `String` | Path to save the exported file. |

**Returns** (`nil`) — nil

### export_data

```ruby
export_data(view_id, response_format, file_path, config = {})
```

Exports the specified view's data to a file.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `String` | ID of the view to export. |
| `response_format` | `String` | Format in which to export the data. |
| `file_path` | `String` | Path to the file where exported data will be stored. |
| `config` | `Hash` | Optional configuration parameters. |

### get_export_job_details

```ruby
get_export_job_details(job_id)
```

Retrieves details of a specific export job.

| Parameter | Type | Description |
|---|---|---|
| `job_id` | `String` | The export job ID. |

**Returns** (`Hash`) — Export job metadata and status.

### get_import_job_details

```ruby
get_import_job_details(job_id)
```

Retrieves the details of an import job by its ID.

| Parameter | Type | Description |
|---|---|---|
| `job_id` | `String` | The job ID to query. |

**Returns** (`Hash`) — Job details and status.

### import_bulk_data

```ruby
import_bulk_data(view_id, import_type, file_type, auto_identify, file_path, config = {})
```

Initiates asynchronous import of data into an existing view.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `String` | Target view ID. |
| `import_type` | `String` | Type of import (APPEND, etc.). |
| `file_type` | `String` | File format. |
| `auto_identify` | `String` | Whether to auto-detect format. |
| `file_path` | `String` | Path to the file. |
| `config` | `Hash` | Additional parameters. |

**Returns** (`String`) — Job ID.

### import_bulk_data_in_new_table

```ruby
import_bulk_data_in_new_table(table_name, file_type, auto_identify, file_path, config = {})
```

Initiates asynchronous import of data into a new table.

| Parameter | Type | Description |
|---|---|---|
| `table_name` | `String` | Target table name. |
| `file_type` | `String` | File format (e.g., "csv"). |
| `auto_identify` | `String` | Whether to auto-detect file format. |
| `file_path` | `String` | Path to the data file. |
| `config` | `Hash` | Additional parameters. |

**Returns** (`String`) — Job ID of the import operation.

### import_data

```ruby
import_data(view_id, import_type, file_type, auto_identify, file_path, config = {})
```

Imports data to an existing view from a file.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `String` | The ID of the target view. |
| `import_type` | `String` | Type of import: "APPEND", "TRUNCATEADD", or "UPDATEADD". |
| `file_type` | `String` | File format (e.g., "csv"). |
| `auto_identify` | `String` | Whether to auto-identify the format. |
| `file_path` | `String` | Path to the input file. |
| `config` | `Hash` | Optional additional parameters. |

**Returns** (`Hash`) — API response data.

### import_data_as_batches

```ruby
import_data_as_batches(view_id, import_type, auto_identify, file_path, batch_size, config = {}, tool_config = {})
```

Asynchronously imports data to an existing view in batches.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `String` | Target view ID. |
| `import_type` | `String` | Type of import. |
| `auto_identify` | `String` | Whether to auto-identify format. |
| `file_path` | `String` | File path for input. |
| `batch_size` | `Integer` | Number of rows per batch. |
| `config` | `Hash` | Additional options. |
| `tool_config` | `Hash` | Internal config for SDK tool. |

**Returns** (`String`) — Job ID of the batch import.

### import_data_in_new_table

```ruby
import_data_in_new_table(table_name, file_type, auto_identify, file_path, config = {})
```

Imports data from a file to a new table.

| Parameter | Type | Description |
|---|---|---|
| `table_name` | `String` | Name of the new table to be created. |
| `file_type` | `String` | Type of the file (e.g., "csv", "json"). |
| `auto_identify` | `String` | Whether to auto-identify the file format ("true" or "false"). |
| `file_path` | `String` | Local path to the import file. |
| `config` | `Hash` | Additional optional parameters. |

**Returns** (`Hash`) — The response data from the API.

### import_data_in_new_table_as_batches

```ruby
import_data_in_new_table_as_batches(table_name, auto_identify, file_path, batch_size, config = {}, tool_config = {})
```

Create a new table and import the data contained in the mentioned file into the created table.

| Parameter | Type | Description |
|---|---|---|
| `table_name` | `String` | Name of the new table to be created. |
| `auto_identify` | `String` | Used to specify whether to auto identify the CSV format. Allowable values - true/false. |
| `file_path` | `String` | Path of the file to be imported. |
| `batch_size` | `Integer` | Number of lines per batch. |
| `config` | `Hash` | Contains any additional control parameters. Can be nil. |
| `tool_config` | `Hash` | Contains any additional control parameters for the library. Can be nil. |

**Returns** (`String`) — Import job id

### import_raw_data

```ruby
import_raw_data(view_id, import_type, file_type, auto_identify, data, config = {})
```

Imports raw data to an existing view.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `String` | ID of the target view. |
| `import_type` | `String` | Type of import (APPEND, etc.). |
| `file_type` | `String` | Format of the raw data. |
| `auto_identify` | `String` | Whether to auto-identify format. |
| `data` | `String` | Raw data content. |
| `config` | `Hash` | Additional parameters. |

**Returns** (`Hash`) — API response data.

### import_raw_data_in_new_table

```ruby
import_raw_data_in_new_table(table_name, file_type, auto_identify, data, config = {})
```

Imports raw data (as a string or byte array) to a new table.

| Parameter | Type | Description |
|---|---|---|
| `table_name` | `String` | Name of the new table to be created. |
| `file_type` | `String` | Type of the raw data (e.g., "csv"). |
| `auto_identify` | `String` | Whether to auto-identify format. |
| `data` | `String` | Raw data content. |
| `config` | `Hash` | Additional parameters. |

**Returns** (`Hash`) — Import result from the API.

### initiate_bulk_export

```ruby
initiate_bulk_export(view_id, response_format, config = {})
```

Initiates an asynchronous export for the given view.

| Parameter | Type | Description |
|---|---|---|
| `view_id` | `String` | ID of the view to be exported. |
| `response_format` | `String` | Format of the exported data (e.g., "csv", "json"). |
| `config` | `Hash` | Additional optional parameters. |

**Returns** (`String`) — Job ID of the export operation.

### initiate_bulk_export_using_sql

```ruby
initiate_bulk_export_using_sql(sql_query, response_format, config = {})
```

Initiates an asynchronous export using a SQL query.

| Parameter | Type | Description |
|---|---|---|
| `sql_query` | `String` | SQL query to run for export. |
| `response_format` | `String` | Format of the exported data. |
| `config` | `Hash` | Additional control parameters. |

**Returns** (`String`) — Job ID of the export task.

## Related

- [Errors](../errors.md) — the failure envelope and codes worth branching on.
- [Limits](../limits.md) — throttles and quotas that apply to these calls.
