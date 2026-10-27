# Limits

Four independent mechanisms limit what an integration can do. They are enforced
separately and signal differently.

| Mechanism | Scope | Signal |
|---|---|---|
| OAuth token throttle | Per refresh token | `access_denied` from Zoho Accounts. See [Authentication](authentication.md#the-access-token-throttle). |
| Per-operation throttles | Per user, per operation | Request rejected for a lockout period. |
| Concurrency guards | One long-running operation per object | A specific error code such as `18072`, `7429`, `8132`. |
| Plan quotas | Per organization | Error when exhausted; visible through Get Resource Details. |

::: danger The token throttle is the one that bites first
Ten access tokens per ten minutes per refresh token. It is the limit most
integrations hit, and it is entirely avoidable — see
[Authentication](authentication.md#the-access-token-throttle).
:::

## Per-operation throttles

Counted per user. Crossing the threshold inside the window locks that user out of
the operation for the lockout period.

| Operation | Limit | Lockout |
|---|---|---|
| Create Query Table | 7 / user / 60s (15/min service-wide) | 5 minutes |
| Edit Query Table | 7 / user / 60s (15/min service-wide) | 5 minutes |
| Get Custom Formulas | 30 / user / 60s | 10 minutes |
| Add Custom Formula | 20 / user / 60s | 10 minutes |
| Edit Custom Formula | 20 / user / 60s | 10 minutes |
| Delete Custom Formula | 30 / user / 60s | 10 minutes |
| Get Aggregate Formula | 30 / user / 60s | 10 minutes |
| Add Aggregate Formula | 20 / user / 60s | 10 minutes |
| Edit Aggregate Formula | 20 / user / 60s | 10 minutes |
| Delete Aggregate Formula | 20 / user / 60s | 10 minutes |
| Create Dashboard | 10 / user / 60s | 10 minutes |
| Update Dashboard | 10 / user / 60s | 10 minutes |
| Read Dashboard Metadata | 20 / user / 60s | — |

## Payload and job limits

| Limit | Value |
|---|---|
| Synchronous import, maximum file size | 20 MB per request |
| Synchronous export, payload ceiling | 100 MB |
| Batch import, maximum batch size | 100 MB per batch |
| Concurrent asynchronous export jobs | 5 per organization (error `8132`) |
| Export job and file retention | 1 hour from job completion |

::: limit When synchronous export is not allowed
Tables over one million rows, dashboards, query tables and live-connect views
cannot be exported synchronously — the call fails with `8133`. Use the
asynchronous job flow described in [Exporting data](guides/exporting-data.md).
:::

## Concurrency guards

| Guard | Error | Behaviour |
|---|---|---|
| One refetch per table | `18072` | A second refetch while one is running is rejected. |
| One copy per organization | `7429` | A second workspace copy is rejected while one runs. |
| Five export jobs per organization | `8132` | A sixth job is rejected. |

Waiting is the fix; backing off blindly without checking whether the blocking
operation finished is not.

## API units

Every call deducts API units from the organization's plan allowance, with the
cost depending on the operation. Current allocation, usage and remainder come
back from Get Resource Details under `resourceName: "apiUnits"`.

::: warning Single-row APIs are expensive at volume
Add Row, Update Row and Delete Row cost one API unit per row. Loading data row
by row will exhaust the quota quickly — use the import APIs instead. See
[Importing data](guides/importing-data.md).
:::

## Plan quotas visible through the API

`users`, `roUsers`, `workspaces`, `rows`, `queryTables`, `archivedrows`,
`scheduledImports`, `scheduledEmails`, `apiUnits`, `scheduledAlerts`,
`scheduledSnapshots`, `archiveschedule`, `financeMultiorgImports`,
`privateLinks`, `actionsByFlow`. A value of `"Unlimited"` means no cap.

## Related

- [Authentication](authentication.md) — the OAuth token throttle.
- [Errors](errors.md) — the codes these limits report through.
