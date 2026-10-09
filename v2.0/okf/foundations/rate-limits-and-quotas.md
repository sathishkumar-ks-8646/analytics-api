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
  - id: group-automl
    resource: "/domains/dsml/automl/overview.md"
    title: AutoML - group overview
  - id: openapi-spec
    resource: "/references/openapi/org-management-grouped-api.json"
    title: OpenAPI 3 specification - org-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
  - id: openapi-spec
    resource: "/references/openapi/user-groups-grouped-api.json"
    title: OpenAPI 3 specification - user-groups-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
  - id: openapi-spec
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
  - id: openapi-spec
    resource: "/references/openapi/data-operations-grouped-api.json"
    title: OpenAPI 3 specification - data-operations-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
  - id: openapi-spec
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
  - id: openapi-spec
    resource: "/references/openapi/share-publish-grouped-api.json"
    title: OpenAPI 3 specification - share-publish-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
  - id: openapi-spec
    resource: "/references/openapi/schedules-alerts-grouped-api.json"
    title: OpenAPI 3 specification - schedules-alerts-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
  - id: openapi-spec
    resource: "/references/openapi/dsml-grouped-api.json"
    title: OpenAPI 3 specification - dsml-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Three different mechanisms limit how much an integration can do. They are enforced independently and produce different signals.

| Mechanism | Scope | Signal | What to do |
|---|---|---|---|
| **Request throttles** | Specific write-heavy operations (query tables, formulas) | Request rejected for the lock period after the threshold is crossed within the window | Space out calls; on rejection wait for the lock period, do not retry in a tight loop. |
| **Concurrency guards** | One long-running operation per object at a time (workspace copy, table refetch, query table design edit, export/import job slots) | A specific error code such as `18072`, `7429`, `8132` | Wait for the running operation to finish, then retry. Backing off blindly does not help. |
| **Plan quotas** | Organization level, governed by the subscription plan (rows, users, scheduled emails, API units, export jobs...) | Error when the quota is exhausted; visible through [Get Resource Details](../domains/organization-management/org-info-and-settings/get-resource-details.md) | Monitor `remaining` values; upgrade the plan or reduce consumption. |

# Per-operation Throttles

Throttles are counted per user. Crossing the threshold inside the window locks the user out of that operation for the lock period.

| Operation | Limit | Lockout | Documented note |
|---|---|---|---|
| [Create Query Table](../domains/data-modeling-and-schema/query-tables/create-query-table.md) | 7 requests / user / 60 s | 5 minutes | 7 requests/user/minute (5-minute lockout on breach); 15 requests/minute service-wide. |
| [Edit Query Table](../domains/data-modeling-and-schema/query-tables/edit-query-table.md) | 7 requests / user / 60 s | 5 minutes | 7 requests/user/minute (5-minute lockout on breach); 15 requests/minute service-wide. |
| [Get Custom Formulas](../domains/data-modeling-and-schema/formula-columns/get-custom-formula-list.md) | 30 requests / user / 60 s | 10 minutes | 30 requests per user per minute (10-minute lockout on breach). |
| [Add Custom Formula](../domains/data-modeling-and-schema/formula-columns/add-formula-column.md) | 20 requests / user / 60 s | 10 minutes | 20 requests per user per minute (10-minute lockout on breach). |
| [Edit Custom Formula](../domains/data-modeling-and-schema/formula-columns/edit-formula-column.md) | 20 requests / user / 60 s | 10 minutes | 20 requests per user per minute (10-minute lockout on breach). |
| [Delete Custom Formula](../domains/data-modeling-and-schema/formula-columns/delete-formula-column.md) | 30 requests / user / 60 s | 10 minutes | 30 requests per user per minute (10-minute lockout on breach). |
| [Get Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-list.md) | 30 requests / user / 60 s | 10 minutes | 30 requests per user per minute (10-minute lockout on breach). |
| [Add Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/add-aggregate-formula.md) | 20 requests / user / 60 s | 10 minutes | 20 requests per user per minute (10-minute lockout on breach). |
| [Edit Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/edit-aggregate-formula.md) | 20 requests / user / 60 s | 10 minutes | 20 requests per user per minute (10-minute lockout on breach). |
| [Delete Aggregate Formula](../domains/data-modeling-and-schema/aggregate-formulas/delete-aggregate-formula.md) | 20 requests / user / 60 s | 10 minutes | 20 requests per user per minute (10-minute lockout on breach). |

Additional documented limits:

- Create Query Table and Edit Query Table are also limited to 15 requests per minute service-wide, in addition to the per-user throttle.
- Copy Workspace allows only one copy operation per organization at a time; a second request while a copy is running is rejected.
- Sync Data and Refetch Data are rate limited per user; a burst of calls is locked out for a short cool-off period. Refetch is additionally guarded by one refetch per table at a time (error [`18072`](error-codes.md#error-18072)).
- Asynchronous export: at most 5 simultaneous export jobs per organization (error [`8132`](error-codes.md#error-8132)); jobs and their files are retained for 72 hours from creation.
- Synchronous export: payload ceiling 100 MB; tables above one million rows, dashboards, query tables and live-connect views must use the asynchronous export (error [`8133`](error-codes.md#error-8133)).
- Synchronous import: maximum file size 20 MB per request.

# API Units

Each API call deducts API units from the organization's plan allowance; the exact cost depends on the operation type. The current allocation, usage and remainder are returned by [Get Resource Details](../domains/organization-management/org-info-and-settings/get-resource-details.md) under `resourceName: "apiUnits"` (fractional usage is possible). Single-row APIs (Add Row, Update Row, Delete Row) cost one unit per row, so bulk loading should use the import APIs instead.

# Plan Quotas Visible Through the API

[Get Resource Details](../domains/organization-management/org-info-and-settings/get-resource-details.md) reports allocated, used and remaining values for: `users`, `roUsers`, `workspaces`, `rows`, `queryTables`, `archivedrows`, `scheduledImports`, `scheduledEmails`, `apiUnits`, `scheduledAlerts`, `scheduledSnapshots`, `archiveschedule`, `financeMultiorgImports`, `privateLinks`, `actionsByFlow`. `"Unlimited"` means no cap.

# Related

- [Error code catalog](error-codes.md)
- [Asynchronous jobs](asynchronous-jobs.md)
