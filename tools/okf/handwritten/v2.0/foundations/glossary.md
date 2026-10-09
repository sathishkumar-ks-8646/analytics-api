---
type: Reference
title: Glossary
description: Definitions of every Zoho Analytics object and term used across the REST API v2 documentation - organization, workspace, view, table, query table, report, dashboard, column, lookup, formula, variable, datasource, job, share, publish, embed, slideshow, schedule, AutoML, portal and more.
tags:
  - zoho-analytics
  - rest-api-v2
  - glossary
  - terminology
  - concepts
sources:
  - id: markdown-docs
    resource: /domains/index.md
    title: API domain and group overviews in this bundle
generated:
  at: {{NOW}}
status: stable
---

# Summary

Terms are grouped by area. Each entry names the identifier used in the API and links to the group that manages the object.

# Organization and Users

| Term | Definition | API identifier |
|---|---|---|
| **Organization** | The top-level tenant that owns workspaces, users and the subscription plan. A user can belong to several organizations, one of them marked `isDefault`. | `orgId`, sent as the `ZANALYTICS-ORGID` header. [Organization Info & Settings](/domains/organization-management/org-info-and-settings/overview.md) |
| **Account Admin** | The owner of the organization; the only role that can do everything. | Role display name `Account Admin`. |
| **Organization Admin** | Org-wide administrator below the Account Admin. | `ORGADMIN`. [Organization Users](/domains/users-and-groups/org-users/overview.md) |
| **User / Viewer** | Standard member / read-only member of the organization. | `USER`, `VIEWER`. |
| **Workspace Admin** | Full administrator of one workspace; the owner is one. | `WORKSPACEADMIN`. [Workspace Users](/domains/users-and-groups/workspace-users/overview.md) |
| **Workspace group** | Named set of users inside one workspace used to share views in bulk. | `groupId`. [Workspace Groups](/domains/users-and-groups/workspace-groups/overview.md) |
| **Plan / resources** | Subscription tier (Basic, Standard, Premium, Enterprise, Ultimate) and its quotas (users, rows, API units...). | [Get Subscription Details](/domains/organization-management/org-info-and-settings/get-subscription-details.md), [Get Resource Details](/domains/organization-management/org-info-and-settings/get-resource-details.md) |
| **API units** | Consumption quota deducted per API call according to operation type. | `resourceName: apiUnits`. |

# Workspace

| Term | Definition | API identifier |
|---|---|---|
| **Workspace** | A database-like container of tables, views and settings. Names are unique within an organization. | `workspaceId`. [Workspace Operations](/domains/workspace-management/workspace-operations/overview.md) |
| **Folder** | Hierarchical grouping of views inside a workspace; one folder is the default. | `folderId`. [Workspace Folders](/domains/workspace-management/workspace-folders/overview.md) |
| **Default workspace / Favourite** | Per-user preferences: the workspace opened at login; starred workspaces and views. | [Workspace Preferences](/domains/workspace-management/workspace-preferences/overview.md), [View Preferences](/domains/views-management/view-preferences/overview.md) |
| **Workspace secret key** | Key used by embedding and integration scenarios for a workspace. | [Get Workspace Secret Key](/domains/workspace-management/workspace-operations/overview.md) |
| **Template export** | Exporting a workspace's design (without data) for reuse. | [Export as Template](/domains/workspace-management/workspace-operations/overview.md) |
| **Trash** | Holding area for deleted views that can be restored or permanently deleted. | [Trash Management](/domains/views-management/trash-management/overview.md) |

# Views and Data Model

| Term | Definition | API identifier |
|---|---|---|
| **View** | Any named object in a workspace: table, query table, report (chart, pivot, summary, tabular), dashboard. Names are unique within a workspace. | `viewId`; `viewType` values such as `Table`, `AnalysisView`, `Pivot`, `SummaryView`, `Query Table`, `Dashboard`. [View Operations](/domains/views-management/view-operations/overview.md) |
| **Table** | A view that stores rows and columns; the only view type that accepts row writes and imports. | [Table & Schema](/domains/data-modeling-and-schema/table-and-schema/overview.md) |
| **Column** | A typed field of a table (data types such as `PLAIN`, `NUMBER`, `DECIMAL_NUMBER`, `CURRENCY`, `DATE`, `BOOLEAN`, `EMAIL`, `URL`). | `columnId`. [Columns](/domains/data-modeling-and-schema/columns/overview.md) |
| **Lookup (relationship)** | Foreign-key style link from a child table column to a unique column of a reference (parent) table in the same workspace; enables multi-table reports. | `referenceViewId`, `referenceColumnId`. [Lookups & Relationships](/domains/data-modeling-and-schema/lookups-and-relationships/overview.md) |
| **Query table (QT, SQL view)** | A view computed at query time from a user-written SQL `SELECT` over tables and views of the workspace. | `querytable-id` (a view ID). [Query Tables](/domains/data-modeling-and-schema/query-tables/overview.md) |
| **Custom formula column** | A computed column whose value per row derives from an expression over other columns. | `formulaId`. [Custom Formula Columns](/domains/data-modeling-and-schema/formula-columns/overview.md) |
| **Aggregate formula (Unified Metric)** | A named, reusable aggregate expression (for example total sales) owned by a view, usable across reports and dashboards; supports synonyms and priority for natural-language search. | `formulaId`. [Aggregate Formulas](/domains/data-modeling-and-schema/aggregate-formulas/overview.md) |
| **Workspace variable** | A reusable placeholder such as `${Region}` with a data type and a resolution type (List, Range, All Values), optionally overridden per user. | `variableId`. [Workspace Variables](/domains/data-modeling-and-schema/workspace-variables/overview.md) |
| **Report (Analysis view)** | A chart, pivot, summary or tabular visualization built on tables or query tables. | `viewId`. [Reports](/domains/reports-and-dashboards/reports/overview.md) |
| **Dashboard** | A layout of reports, optionally with tabs, themes and global user filters. | `viewId`. [Dashboards](/domains/reports-and-dashboards/dashboards/overview.md) |
| **Auto analysis** | Server-generated set of meaningful views for a table or a column. | [Auto Analysis](/domains/views-management/auto-analysis/overview.md) |
| **Dependents** | Views, formulas and dashboards that reference an object; inspected before deletes and renames. | Get Column / Aggregate Formula / View Dependents. |
| **System tags** | Organization-level tags (for example `DATA_WARNING`, Outdated) that can block sharing or scheduling until acknowledged with `validateSystemTags: false` (`8241`). | |

# Data Movement

| Term | Definition | API identifier |
|---|---|---|
| **Import** | Pushing a file or text payload into a new or existing table. Synchronous (inline result) or asynchronous (job). | [Import options](/foundations/import-options-and-enums.md) |
| **Export** | Pulling a view's data as CSV, JSON, XML, XLS, PDF, HTML or image. Synchronous (file in the response) or asynchronous (job, then download). | [Export formats](/foundations/export-formats-and-enums.md) |
| **Job** | A background import or export identified by `jobId` with `jobCode` states 1001 to 1005. | [Asynchronous jobs](/foundations/asynchronous-jobs.md) |
| **Batch import** | A single job fed by many CSV requests sharing a `batchKey`. | [Asynchronous & Batch Data Import](/domains/data-operations/async-data-import/overview.md) |
| **Row operations** | Single-row insert, criteria-based update and delete on a table. | [Row Operations](/domains/data-operations/row-operations/overview.md) |
| **Datasource** | The external connection (cloud or local database, file, web feed, cloud storage, integration connector, live connect, snapshot) behind a table. | `datasourceId`. [Data Sync & Connectivity](/domains/data-operations/data-sync-and-connectivity/overview.md) |
| **Sync / Refetch** | Sync pulls a whole datasource; refetch pulls one table, optionally as a full fetch. Both consume the manual-sync quota. | |
| **Criteria** | SQL-like row filter expression. | [Filter criteria syntax](/foundations/filter-criteria-syntax.md) |

# Access and Distribution

| Term | Definition | API identifier |
|---|---|---|
| **Share** | Granting users or groups a permission set (read, export, vud, drill, row writes, imports, share...) on views, optionally limited by columns and criteria. | [Sharing](/domains/share-and-publish/sharing/overview.md) |
| **Publish: public URL** | A stand-alone read-only URL open to anyone with the link (or to the organization, per `publicPermLevel`). Modeled as a share to the `Public Visitor` pseudo-user (`sharedToZuId: -20`). | [Publish](/domains/share-and-publish/publish/overview.md) |
| **Publish: private URL** | A read-only URL with a 32-character secret key, optional password and expiry. Pseudo-user `Private Link` (`-30`). | |
| **Publish configuration** | How a published or embedded page renders (title, toolbar, size, auto-refresh, legend, Ask Zia...). | |
| **Embed URL** | Short-lived (default 1 hour, max 1 day), login-free URL for one view with its own permissions, criteria and column restrictions; one per call; Embedded Analytics (OEM) customers only. | `rsConfig`. [Embed URL](/domains/share-and-publish/embed-url/overview.md) |
| **Slideshow** | Ordered set of views presented on a stand-alone page identified by `slideId` and a secret `slideKey`; `accessType` 0 requires login, 1 does not. | `slideId`. [Slideshow Management](/domains/share-and-publish/slideshow-management/overview.md) |
| **Email schedule** | Recurring email delivery of views as CSV, XLS, PDF, HTML or image, with calendar frequency, recipients, groups, report bursts. | `scheduleId`. [Email Schedules](/domains/schedules-and-alerts/email-schedules/overview.md) |
| **Report burst** | Email schedule variant sending one personalized email per row of a distribution-list table. | `reportBurstConfig`. |
| **White Label / Client Portal** | Branded custom domain through which portal users access analytics. | `domainName`. [White label & Client Portal](/foundations/white-label-client-portal.md) |
| **Embedded Analytics (OEM)** | Licensing mode that enables embed URLs. | Error `8023` when not enabled. |

# Machine Learning

| Term | Definition | API identifier |
|---|---|---|
| **AutoML analysis** | A training run on a table (`trainingTableId`) that produces one model per algorithm. | `analysisId`. [AutoML](/domains/dsml/automl/overview.md) |
| **Model** | A trained algorithm inside an analysis with a `trainingStatus`; the only source of `modelId` is Get AutoML Analysis Details. | `modelId`. |
| **Deployment** | Binding of one model to an input table and an output table so it can be run; one deployment per model. | `deploymentId`, `outputTableId`. |
| **What-If analysis** | One-off prediction against a model without storing anything. | |

# Related

- [Overview](/overview.md)
- [Identifiers](/foundations/identifiers.md)
