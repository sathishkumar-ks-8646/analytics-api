# Importing data

Three modes, chosen by file size and whether you need to wait for the result.

| Mode | File size | Blocking | Use when |
|---|---|---|---|
| Synchronous | up to 20 MB | Yes | Small files where you want the row counts immediately. |
| Batched | any | Yes | Large CSV files; the SDK splits and uploads them for you. |
| Asynchronous job | any | No | Large files where you want to poll for completion. |

::: warning Do not load data row by row
Add Row costs one API unit per row. Importing a file costs far less and is
dramatically faster. Use the row APIs for corrections, not for loading.
:::

## Synchronous import

```php
$bulk = $ac->getBulkInstance($org_id, $workspace_id);

$response = $bulk->importData(
    $view_id,
    "TRUNCATEADD",
    "csv",
    true,
    "/home/user/Sales.csv"
);
print_r($response);
```

### Import types

| Value | Behaviour |
|---|---|
| `APPEND` | Add every row. Duplicates are kept. |
| `TRUNCATEADD` | Delete all existing rows, then add. |
| `UPDATEADD` | Update rows matching the configured key, add the rest. |

::: note `UPDATEADD` needs a matching column
Set `matchingColumns` in the config, otherwise the server cannot tell which rows
to update and the call fails validation.
:::

### Sample response

```json
{
  "status": "success",
  "summary": "Import data",
  "data": {
    "importSummary": {
      "totalColumnCount": 8,
      "selectedColumnCount": 8,
      "totalRowCount": 12500,
      "successRowCount": 12498,
      "warnings": 2,
      "importOperation": "updateadd"
    },
    "importErrors": "2 rows were skipped: date value did not match the column format."
  }
}
```

::: warning A successful import can still skip rows
`status` is `success` whenever the request was processed. Compare
`successRowCount` against `totalRowCount` and inspect `importErrors` — rows with
unparseable values are skipped silently otherwise.
:::

## Batched import

For files over 20 MB. The SDK splits the file, uploads each batch, and returns a
job id.

```php
$bulk = $ac->getBulkInstance($org_id, $workspace_id);

$job_id = $bulk->importDataAsBatches(
    $view_id, "APPEND", true, "/home/user/large-sales.csv", 100000
);

print_r($bulk->getImportJobDetails($job_id));
```

Batch size is counted in rows. Keep each resulting batch under 100 MB.

### Sample job response

```json
{
  "status": "success",
  "summary": "Get import job details",
  "data": {
    "jobId": "35130000001343088",
    "jobStatus": "JOB COMPLETED",
    "importSummary": {
      "totalRowCount": 2400000,
      "successRowCount": 2400000,
      "warnings": 0
    }
  }
}
```

`jobStatus` is one of `JOB NOT STARTED`, `JOB IN PROGRESS`, `JOB COMPLETED` or
`JOB FAILED`.

::: note Driving the batches yourself
If you have already split the file, the batch endpoint can be driven directly:
send `batchKey: "start"` with `importType` and `autoIdentify` on the first batch,
reuse the returned `batchKey` on the rest, and set `isLastBatch: true` on the
final one to commit the job.
:::

## Related

- [Exporting data](exporting-data.md)
- [Limits](../limits.md) — file size ceilings and API unit costs.
- [Errors](../errors.md)
