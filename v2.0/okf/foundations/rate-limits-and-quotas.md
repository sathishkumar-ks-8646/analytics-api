---
type: Reference
title: "Rate limits, throttling and quotas"
description: "Per-operation request throttles, concurrency guards, plan-governed quotas and API unit consumption for the Zoho Analytics REST API v2."
tags:
  - zoho-analytics
  - rest-api-v2
  - rate-limits
  - throttling
  - quotas
  - api-units
sources:
  - id: group-org-info-and-settings
    resource: "/domains/organization-management/org-info-and-settings/overview.md"
    title: Organization Info & Settings - group overview
  - id: group-org-level-listings
    resource: "/domains/organization-management/org-level-listings/overview.md"
    title: Org-Level Listings - group overview
  - id: group-security-controls
    resource: "/domains/organization-management/security-controls/overview.md"
    title: Security Controls - group overview
  - id: group-org-users
    resource: "/domains/users-and-groups/org-users/overview.md"
    title: Organization Users - group overview
  - id: group-custom-roles
    resource: "/domains/users-and-groups/custom-roles/overview.md"
    title: Custom Roles - group overview
  - id: group-workspace-users
    resource: "/domains/users-and-groups/workspace-users/overview.md"
    title: Workspace Users - group overview
  - id: group-workspace-groups
    resource: "/domains/users-and-groups/workspace-groups/overview.md"
    title: Workspace Groups - group overview
  - id: group-workspace-operations
    resource: "/domains/workspace-management/workspace-operations/overview.md"
    title: Workspace Operations - group overview
  - id: group-workspace-folders
    resource: "/domains/workspace-management/workspace-folders/overview.md"
    title: Workspace Folders - group overview
  - id: group-workspace-preferences
    resource: "/domains/workspace-management/workspace-preferences/overview.md"
    title: Workspace Preferences - group overview
  - id: group-domain-and-white-label
    resource: "/domains/workspace-management/domain-and-white-label/overview.md"
    title: Domain & White Label Access - group overview
  - id: group-linked-workspaces
    resource: "/domains/workspace-management/linked-workspaces/overview.md"
    title: Linked Workspaces - group overview
  - id: group-workspace-backup-and-restore
    resource: "/domains/workspace-management/workspace-backup-and-restore/overview.md"
    title: Workspace Backup & Restore - group overview
  - id: group-table-and-schema
    resource: "/domains/data-modeling-and-schema/table-and-schema/overview.md"
    title: Table & Schema - group overview
  - id: group-columns
    resource: "/domains/data-modeling-and-schema/columns/overview.md"
    title: Columns - group overview
  - id: group-lookups-and-relationships
    resource: "/domains/data-modeling-and-schema/lookups-and-relationships/overview.md"
    title: Lookups & Relationships - group overview
  - id: group-query-tables
    resource: "/domains/data-modeling-and-schema/query-tables/overview.md"
    title: Query Tables - group overview
  - id: group-formula-columns
    resource: "/domains/data-modeling-and-schema/formula-columns/overview.md"
    title: Custom Formula Columns - group overview
  - id: group-aggregate-formulas
    resource: "/domains/data-modeling-and-schema/aggregate-formulas/overview.md"
    title: Aggregate Formulas (Unified Metrics) - group overview
  - id: group-workspace-variables
    resource: "/domains/data-modeling-and-schema/workspace-variables/overview.md"
    title: Workspace Variables - group overview
  - id: group-sync-data-import
    resource: "/domains/data-operations/sync-data-import/overview.md"
    title: Synchronous Data Import - group overview
  - id: group-async-data-import
    resource: "/domains/data-operations/async-data-import/overview.md"
    title: Asynchronous & Batch Data Import - group overview
  - id: group-sync-data-export
    resource: "/domains/data-operations/sync-data-export/overview.md"
    title: Synchronous Data Export - group overview
  - id: group-async-data-export
    resource: "/domains/data-operations/async-data-export/overview.md"
    title: Asynchronous Data Export - group overview
  - id: group-row-operations
    resource: "/domains/data-operations/row-operations/overview.md"
    title: Row Operations - group overview
  - id: group-data-sync-and-connectivity
    resource: "/domains/data-operations/data-sync-and-connectivity/overview.md"
    title: Data Sync & Connectivity - group overview
  - id: group-view-operations
    resource: "/domains/views-management/view-operations/overview.md"
    title: View Operations - group overview
  - id: group-view-preferences
    resource: "/domains/views-management/view-preferences/overview.md"
    title: View Preferences - group overview
  - id: group-trash-management
    resource: "/domains/views-management/trash-management/overview.md"
    title: Trash Management - group overview
  - id: group-auto-analysis
    resource: "/domains/views-management/auto-analysis/overview.md"
    title: Auto Analysis - group overview
  - id: group-tags
    resource: "/domains/views-management/tags/overview.md"
    title: Tags - group overview
  - id: group-reports
    resource: "/domains/reports-and-dashboards/reports/overview.md"
    title: Reports (Analysis Views) - group overview
  - id: group-dashboards
    resource: "/domains/reports-and-dashboards/dashboards/overview.md"
    title: Dashboards - group overview
  - id: group-sharing
    resource: "/domains/share-and-publish/sharing/overview.md"
    title: Sharing - group overview
  - id: group-publish
    resource: "/domains/share-and-publish/publish/overview.md"
    title: Publish - group overview
  - id: group-embed-url
    resource: "/domains/share-and-publish/embed-url/overview.md"
    title: Embed URL - group overview
  - id: group-slideshow-management
    resource: "/domains/share-and-publish/slideshow-management/overview.md"
    title: Slideshow Management - group overview
  - id: group-email-schedules
    resource: "/domains/schedules-and-alerts/email-schedules/overview.md"
    title: Email Schedules - group overview
  - id: group-data-alerts
    resource: "/domains/schedules-and-alerts/data-alerts/overview.md"
    title: Data Alerts - group overview
  - id: group-automl
    resource: "/domains/dsml/automl/overview.md"
    title: AutoML - group overview
  - id: openapi-spec
    resource: "/references/openapi/org-management-grouped-api.json"
    title: OpenAPI 3 specification - org-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T10:58:51Z
  - id: openapi-spec
    resource: "/references/openapi/user-groups-grouped-api.json"
    title: OpenAPI 3 specification - user-groups-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T10:54:58Z
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T11:33:37Z
  - id: openapi-spec
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T10:54:58Z
  - id: openapi-spec
    resource: "/references/openapi/data-operations-grouped-api.json"
    title: OpenAPI 3 specification - data-operations-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T10:54:58Z
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T11:33:28Z
  - id: openapi-spec
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T11:33:28Z
  - id: openapi-spec
    resource: "/references/openapi/share-publish-grouped-api.json"
    title: OpenAPI 3 specification - share-publish-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T10:54:58Z
  - id: openapi-spec
    resource: "/references/openapi/schedules-alerts-grouped-api.json"
    title: OpenAPI 3 specification - schedules-alerts-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T10:54:58Z
  - id: openapi-spec
    resource: "/references/openapi/dsml-grouped-api.json"
    title: OpenAPI 3 specification - dsml-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T10:54:58Z
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

Four different mechanisms limit how much an integration can do. They are enforced independently and produce different signals.

| Mechanism | Scope | Signal | What to do |
|---|---|---|---|
| **Request throttles** | Specific write-heavy operations (query tables, formulas) | Request rejected for the lock period after the threshold is crossed within the window | Space out calls; on rejection wait for the lock period, do not retry in a tight loop. |
| **Concurrency guards** | One long-running operation per object at a time (workspace copy, table refetch, query table design edit, export/import job slots) | A specific error code such as `18072`, `7429`, `8132` | Wait for the running operation to finish, then retry. Backing off blindly does not help. |
| **Plan quotas** | Organization level, governed by the subscription plan (rows, users, scheduled emails, API units, export jobs...) | Error when the quota is exhausted; visible through [Get Resource Details](../domains/organization-management/org-info-and-settings/get-resource-details.md) | Monitor `remaining` values; upgrade the plan or reduce consumption. |
| **Category frequency limits** | Organization level, per unit category (`DML` 100/min, `BULK` 40/min, `METADATA` 60/min) | Request rejected with an API-frequency error | Spread calls across the minute; the ceiling is shared by every endpoint in the category. See [API units](api-units.md#unit-categories-and-frequency-limits). |

# Per-operation Throttles

Throttles are counted per user unless noted. Crossing the threshold inside the window locks the user out of that operation for the lock period. The values below are the ones configured on the endpoint URLs; the per-endpoint pages carry the same figures.

| Operation | Limit | Lockout |
|---|---|---|
| [Create Query Table](../domains/data-modeling-and-schema/query-tables/create-query-table.md) | 20 requests / user / 60 s | 10 minutes |
| [Edit Query Table](../domains/data-modeling-and-schema/query-tables/edit-query-table.md) | 20 requests / user / 60 s | 10 minutes |
| [Get Custom Formulas](../domains/data-modeling-and-schema/formula-columns/get-custom-formula-list.md) | 30 requests / user / 60 s | 10 minutes |
| [Add Custom Formula](../domains/data-modeling-and-schema/formula-columns/add-formula-column.md) | 20 requests / user / 60 s | 10 minutes |
| [Edit Custom Formula](../domains/data-modeling-and-schema/formula-columns/edit-formula-column.md) | 20 requests / user / 60 s | 10 minutes |
| [Delete Custom Formula](../domains/data-modeling-and-schema/formula-columns/delete-formula-column.md) | 30 requests / user / 60 s | 10 minutes |
| [Get Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-list.md) | 30 requests / user / 60 s | 10 minutes |
| [Add Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/add-aggregate-formula.md) | 20 requests / user / 60 s | 10 minutes |
| [Edit Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/edit-aggregate-formula.md) | 20 requests / user / 60 s | 10 minutes |
| [Delete Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/delete-aggregate-formula.md) | 20 requests / user / 60 s | 10 minutes |
| [Create Dashboard](../domains/reports-and-dashboards/dashboards/create-dashboard.md) | 10 requests / user / 60 s | 10 minutes |
| [Read Dashboard Metadata](../domains/reports-and-dashboards/dashboards/get-dashboard-metadata.md) | 20 requests / user / 60 s | 10 minutes |
| [Update Dashboard](../domains/reports-and-dashboards/dashboards/update-dashboard.md) | 10 requests / user / 60 s | 10 minutes |
| [Sync Data](../domains/data-operations/data-sync-and-connectivity/sync-datasource.md) | 5 requests / 60 s | 5 minutes |
| [Refetch Data](../domains/data-operations/data-sync-and-connectivity/refetch-datasource.md) | 5 requests / 60 s | 5 minutes |

On top of these, every endpoint is counted against the per-minute ceiling of its unit category - `DML` 100/min, `BULK` 40/min, `METADATA` 60/min - shared across the whole organization. See [API units](api-units.md#unit-categories-and-frequency-limits).

Additional documented limits:

- Create Query Table and Edit Query Table are also limited to 15 requests per minute service-wide, in addition to the per-user throttle.
- Copy Workspace allows only one copy operation per organization at a time; a second request while a copy is running is rejected.
- Sync Data and Refetch Data are rate limited to 5 requests per minute each, with a 5-minute lockout on breach. Refetch is additionally guarded by one refetch per table at a time (error [`18072`](error-codes.md#error-18072)).
- Asynchronous export: at most 5 simultaneous export jobs per organization (error [`8132`](error-codes.md#error-8132)); jobs and their files are retained for 1 hour from job completion.
- Synchronous export: payload ceiling 100 MB (error [`7830`](error-codes.md#error-7830)). The Export Data API is restricted for certain resources, which must use the asynchronous export (error [`8133`](error-codes.md#error-8133)): tables having more than one million rows; tables and views from live connect workspaces; dashboard and query table view types.
- Synchronous import: maximum file size 20 MB per request.

# API Units

Every call deducts API units from the organization's plan allowance. The cost is fixed per endpoint for most operations and proportional to the rows processed for bulk and copy operations:

```
units charged = (rows processed / rows basis) * configured units      # row-based endpoints
units charged = configured units                                      # everything else
```

Costs range from `0` (job status and download calls) through `0.1` (most reads and user-management writes) to `25` (Copy Workspace). The full per-endpoint table, the row-based and format-based variable costs, and the unit categories are in **[API units](api-units.md)**; the same figures are on every endpoint page and in [`/references/endpoint-catalog.json`](../references/endpoint-catalog.json) under `api_units`.

| Unit category | Frequency limit | Typical cost range |
|---|---|---|
| `DML` | 100 requests/minute | 0.1 - 0.3 units per request |
| `BULK` | 40 requests/minute | 0 to start a job; 3 - 15 units per 1000 rows for the data itself |
| `METADATA` | 60 requests/minute | 0.1 - 25 units per request |

Two practical rules:

- **Load data in bulk.** Add Row costs `0.1` units for one row; [Import Data](../domains/data-operations/sync-data-import/import-data-existing-table.md) costs 10 units per 1000 rows. Loading 100000 rows row-by-row costs 10000 units against roughly 1000 units through import.
- **Poll freely.** Export and import job status and download calls cost `0` units - but they still consume the `BULK` and `METADATA` frequency budget, so a tight polling loop hits the frequency limit rather than the unit allowance.

The current allocation, usage and remainder are returned by [Get Resource Details](../domains/organization-management/org-info-and-settings/get-resource-details.md) under `resourceName: "apiUnits"` (fractional usage is possible).

# Plan Quotas Visible Through the API

[Get Resource Details](../domains/organization-management/org-info-and-settings/get-resource-details.md) reports allocated, used and remaining values for: `users`, `roUsers`, `workspaces`, `rows`, `queryTables`, `archivedrows`, `scheduledImports`, `scheduledEmails`, `apiUnits`, `scheduledAlerts`, `scheduledSnapshots`, `archiveschedule`, `financeMultiorgImports`, `privateLinks`, `actionsByFlow`. `"Unlimited"` means no cap.

# Related

- [API units](api-units.md) - per-endpoint unit cost, unit categories and frequency limits
- [Error code catalog](error-codes.md)
- [Asynchronous jobs](asynchronous-jobs.md)
