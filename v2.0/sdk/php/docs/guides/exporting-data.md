# Exporting data

Two modes. Synchronous returns the file on the same call; asynchronous creates a
job you poll and then download.

| Mode | Ceiling | Use when |
|---|---|---|
| Synchronous | 100 MB | The resource is not one of the restricted ones below. |
| Asynchronous job | No practical ceiling | **Required** for any restricted resource, and for anything over the synchronous ceiling. |

The choice is not about convenience. Export Data API is restricted for the
resources below; for these you must use the asynchronous export, and the
synchronous call rejects them with `8133`:

- Tables having more than one million rows.
- Tables and Views from live connect workspaces.
- Dashboard and Query Table view types.

## Synchronous export

```php
$bulk = $ac->getBulkInstance($org_id, $workspace_id);
$bulk->exportData($view_id, "csv", "/home/user/Sales.csv");
```

### Formats

| Format | Applies to |
|---|---|
| `csv`, `json`, `xml` | Tables, query tables, reports. |
| `xls` | Tables and reports. |
| `pdf`, `html` | Reports and dashboards. |
| `image` | Charts. |

::: limit Synchronous export is not always allowed
Tables over one million rows, dashboards, query tables and live-connect views
reject synchronous export with error `8133`. Use the asynchronous flow below.
:::

## Asynchronous export

Create the job, poll it, then download when it reports complete.

```php
$bulk = $ac->getBulkInstance($org_id, $workspace_id);

$job_id = $bulk->initiateBulkExport($view_id, "csv");

$job = $bulk->getExportJobDetails($job_id);
if ($job["jobStatus"] === "JOB COMPLETED") {
    $bulk->exportBulkData($job_id, "/home/user/Sales.csv");
}
```

### Sample job response

```json
{
  "status": "success",
  "summary": "Get export job details",
  "data": {
    "jobId": "35130000001343084",
    "jobStatus": "JOB COMPLETED",
    "downloadUrl": "https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/35130000001055707/exportjobs/35130000001343084/data",
    "expiryTime": "1735689600000"
  }
}
```

::: note Use the returned `downloadUrl`
It is fully qualified and already points at the correct data center. Do not
assemble download URLs by hand — they differ by region.
:::

::: warning Jobs and files expire one hour after the job completes
Both the job record and the generated file are retained for one hour from the
moment the job reports complete — not from when it was created. `expiryTime`
carries the exact deadline. Download as soon as the job completes, or create a
new job; nothing is recoverable afterwards.
:::

::: limit Five concurrent export jobs per organization
A sixth is rejected with error `8132`. Poll and drain the queue rather than
creating jobs in a loop.
:::

### Polling

Poll at a sensible interval — a few seconds for small exports, tens of seconds
for large ones. `jobStatus` moves through `JOB NOT STARTED`, `JOB IN PROGRESS`,
then `JOB COMPLETED` or `JOB FAILED`. Treat `JOB FAILED` as terminal; the
response carries the reason.

## Related

- [Importing data](importing-data.md)
- [Limits](../limits.md)
- [Errors](../errors.md)
