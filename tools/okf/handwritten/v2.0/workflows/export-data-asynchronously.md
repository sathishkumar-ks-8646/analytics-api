---
type: Playbook
title: Export a view, dashboard or SQL result asynchronously
description: Create an export job, poll or receive a callback, and download the file - the path for dashboards, query tables, large tables and ad-hoc SQL that the synchronous export rejects.
tags:
  - zoho-analytics
  - rest-api-v2
  - workflow
  - playbook
  - export
  - asynchronous
  - jobs
sources:
  - id: markdown-docs
    resource: /domains/index.md
    title: API domain and group overviews in this bundle
generated:
  at: {{NOW}}
status: stable
---

# Goal

Obtain a CSV, JSON, XML, XLS, PDF, HTML or image file for any view, including dashboards and tables above one million rows, or for an ad-hoc SQL query.

# When to Use the Synchronous Export Instead

[Export Data from a View](/domains/data-operations/sync-data-export/export-data-view.md) returns the file in one call and is simpler for tables and reports under one million rows and under 100 MB. It rejects dashboards, query tables, live-connect views and very large tables with `8133`.

# Prerequisites

- Token scope `ZohoAnalytics.data.read`.
- Export permission on the view (or on every table a SQL query touches), or an admin role. Verified primary email (`7565` otherwise). Organization export control enabled (`8088` otherwise).
- `workspaceId` and `viewId` (see [Bootstrap](/workflows/bootstrap-identifiers.md)).

# Steps

1. **Create the job.**
   - From a saved view: [Create Export Job using View ID](/domains/data-operations/async-data-export/create-export-job-view-id.md), `GET /restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data` with `CONFIG={"responseFormat":"pdf","dashboardLayout":1}` (options in [Export formats](/foundations/export-formats-and-enums.md); row filter via `criteria`).
   - From SQL: [Create Export Job using SQL Query](/domains/data-operations/async-data-export/create-export-job-sql-query.md), `GET /restapi/v2/bulk/workspaces/{workspace-id}/data` with `CONFIG={"sqlQuery":"SELECT ...","responseFormat":"csv"}` (up to 100,000 characters, 800,000 result rows; per-table filters in `tableCriteriaList`).
   - Optionally add `"callbackUrl":"https://your-host/notify"` to be notified instead of polling.
   - Keep `data.jobId`.
2. **Wait for completion.** Poll [Get Export Job Details](/domains/data-operations/async-data-export/get-export-job-details.md) every few seconds until `jobCode` is `1004` (done) or `1003` (failed). `1001`/`1002` mean keep waiting. With a callback, the same fields arrive as an HTTP POST.
3. **Download.** Follow `data.downloadUrl` or call [Download Exported Data](/domains/data-operations/async-data-export/download-exported-data.md). The response body is the file. Do this before `expiryTime` and within 72 hours of job creation.

# Limits

Five concurrent jobs per organization (`8132`); only the creator can poll or download (`8124`); downloading early fails with `8121`/`8122`. See [Asynchronous jobs](/foundations/asynchronous-jobs.md).

# Related

- [Asynchronous Data Export](/domains/data-operations/async-data-export/overview.md)
- [Export formats and enumerations](/foundations/export-formats-and-enums.md)
- [Filter criteria syntax](/foundations/filter-criteria-syntax.md)
