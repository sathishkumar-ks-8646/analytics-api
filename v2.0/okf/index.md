---
okf_version: "0.2"
---

# Zoho Analytics REST API v2 - Open Knowledge Format bundle

Knowledge bundle covering every public Zoho Analytics REST API v2 endpoint, the conventions shared by all of them, and their error codes, scopes and permissions. Start with the overview, then the foundations, then the domain you need.

# Start Here

* [Zoho Analytics REST API v2 - overview](overview.md) - What the Zoho Analytics REST API v2 is, how it is organized into 10 domains and 168 endpoints, and the five conventions every call shares.
* [Endpoint catalog](endpoint-catalog.md) - All 182 Zoho Analytics REST API v2 endpoints in one table: method, path, operation ID, group, OAuth scope, success status and organization-header requirement.
* [How to use this bundle](how-to-use-this-bundle.md) - Structure of the Zoho Analytics REST API v2 OKF bundle, the frontmatter contract of each concept type, and navigation rules for AI assistants, SDK generators, Postman runners and MCP servers.

# Foundations (shared by every endpoint)

* [Asynchronous jobs (export and import)](foundations/asynchronous-jobs.md) - How background jobs work in Zoho Analytics REST API v2 - job creation, jobCode states, polling, callbackUrl notifications, batch import keys, retention and ownership rules.
* [Authentication (OAuth 2.0)](foundations/authentication.md) - How to authenticate Zoho Analytics REST API v2 calls with OAuth 2.0 access tokens, the Authorization header format, token lifetime and refresh, and the errors returned when authentication fails.
* [Custom roles](foundations/custom-roles.md) - Organization-defined custom roles in Zoho Analytics - the three access permission levels, the full permission catalogue by category, how a custom role name is used by the REST API v2 user-management endpoints, and how its permissions map onto the API's authorization vocabulary.
* [Data centers and base URLs](foundations/data-centers.md) - The Zoho Analytics API host (ZohoAnalytics_Server_URI) and OAuth accounts host for each data center, and the rules for choosing them.
* [Error codes - quick reference](foundations/error-codes-quick-reference.md) - Compact one-line-per-code table of all 352 Zoho Analytics REST API v2 error codes (code, summary constant, HTTP status, meaning); use the full catalog for per-operation reasons and solutions.
* [Error code catalog](foundations/error-codes.md) - Every documented Zoho Analytics REST API v2 error code (352 codes) with its meaning, typical HTTP status, resolution and the operations that raise it.
* [Export formats and enumerations](foundations/export-formats-and-enums.md) - Every enumerated CONFIG attribute shared by the Zoho Analytics REST API v2 export endpoints and email schedules - responseFormat, CSV delimiters, PDF page setup, header and footer slots, image options, email exportType - with default values and error codes.
* [Filter criteria syntax](foundations/filter-criteria-syntax.md) - Grammar and rules of the SQL-like criteria expression used by Zoho Analytics REST API v2 to filter rows in exports, row updates and deletes, shares, embed URLs, publish configurations and email schedules.
* [Glossary](foundations/glossary.md) - Definitions of every Zoho Analytics object and term used across the REST API v2 documentation - organization, workspace, view, table, query table, report, dashboard, column, lookup, formula, variable, datasource, job, share, publish, embed, slideshow, schedule, AutoML, portal and more.
* [HTTP status codes](foundations/http-status-codes.md) - Which HTTP status codes Zoho Analytics REST API v2 returns, what each one means, and how it maps to the application error codes in the failure envelope.
* [Identifiers and how to obtain them](foundations/identifiers.md) - Every identifier used in Zoho Analytics REST API v2 paths and headers (organization, workspace, view, column, job, schedule and more), its format, and the operations that return it.
* [Import options and enumerations](foundations/import-options-and-enums.md) - The CONFIG vocabulary shared by the Zoho Analytics REST API v2 import endpoints - importType modes, fileType, autoIdentify, onError, number separators, columnDataTypes, matchingColumns, payload limits, and the permission each mode needs.
* [OAuth scopes](foundations/oauth-scopes.md) - All Zoho Analytics OAuth 2.0 scopes, what each family covers, and which REST API v2 operations require each scope.
* [Permission matrix](foundations/permission-matrix.md) - For every Zoho Analytics REST API v2 operation: the OAuth scope, whether the organization header is needed, and the role or view permission the caller must hold.
* [Rate limits, throttling and quotas](foundations/rate-limits-and-quotas.md) - Per-operation request throttles, concurrency guards, plan-governed quotas and API unit consumption for the Zoho Analytics REST API v2.
* [Report and dashboard enumerations](foundations/report-and-dashboard-enums.md) - Every enumerated CONFIG value shared by the Zoho Analytics REST API v2 report and dashboard endpoints - chart types, axis types and which report type accepts them, operations and the column data types they apply to, filter operations and types, user-filter widgets, dashboard card types and the layout grid rules.
* [Request conventions](foundations/request-conventions.md) - The rules shared by every Zoho Analytics REST API v2 request - URL structure, path placeholders, mandatory headers, the CONFIG parameter and how to encode it per HTTP method, multipart uploads, and idempotency.
* [Response envelope](foundations/response-envelope.md) - The JSON envelope returned by Zoho Analytics REST API v2 on success and failure, the 204 no-body pattern, file responses from export endpoints, and the value conventions inside data.
* [Roles and permissions](foundations/roles-and-permissions.md) - The authorization model of Zoho Analytics REST API v2 - organization roles, workspace roles, view-level share permissions, ownership, and how the "Permission Required" statements in endpoint documents should be read.
* [SDK clients and code samples](foundations/sdk-clients.md) - The official Zoho Analytics client libraries (Java, C#, Go, PHP, Python, Node.js, Ruby), the Deluge scripting pattern, how each client is constructed from OAuth credentials, and how to read the per-endpoint SDK example documents.
* [White Label and Client Portal](foundations/white-label-client-portal.md) - How Zoho Analytics White Label (Client Portal) custom domains interact with the REST API v2 - portal request hosts, the domainName attribute, workspace domain access, and which API families are allowed or blocked in a portal context.

# API Domains

* [Organization Management](domains/organization-management/index.md) - 4 endpoints in 1 groups: Organization Info & Settings.
* [Users & Groups](domains/users-and-groups/index.md) - 26 endpoints in 4 groups: Organization Users, Custom Roles, Workspace Users, Workspace Groups.
* [Workspace Management](domains/workspace-management/index.md) - 24 endpoints in 4 groups: Workspace Operations, Workspace Folders, Workspace Preferences, Domain & White Label Access.
* [Data Modeling & Schema](domains/data-modeling-and-schema/index.md) - 33 endpoints in 7 groups: Table & Schema, Columns, Lookups & Relationships, Query Tables, Custom Formula Columns, Aggregate Formulas (Unified Metrics), Workspace Variables.
* [Data Operations](domains/data-operations/index.md) - 20 endpoints in 6 groups: Synchronous Data Import, Asynchronous & Batch Data Import, Synchronous Data Export, Asynchronous Data Export, Row Operations, Data Sync & Connectivity.
* [Views Management](domains/views-management/index.md) - 27 endpoints in 5 groups: View Operations, View Preferences, Trash Management, Auto Analysis, Tags.
* [Reports & Dashboards](domains/reports-and-dashboards/index.md) - 9 endpoints in 2 groups: Reports (Analysis Views), Dashboards.
* [Share & Publish](domains/share-and-publish/index.md) - 22 endpoints in 4 groups: Sharing, Publish, Embed URL, Slideshow Management.
* [Schedules & Alerts](domains/schedules-and-alerts/index.md) - 6 endpoints in 1 groups: Email Schedules.
* [Data Science & Machine Learning (AutoML)](domains/dsml/index.md) - 11 endpoints in 1 groups: AutoML.

# Workflows

* [Bootstrap: from access token to workspace and view IDs](workflows/bootstrap-identifiers.md) - The first three calls of every integration - list organizations, pick the org ID for the header, and resolve workspace and view names into the IDs that all other endpoints need.
* [Embed a view for many tenants with per-tenant row filters](workflows/embed-view-multi-tenant.md) - Mint one short-lived embed URL per end customer, each carrying its own criteria, permissions and column restrictions, then audit and revoke URLs.
* [Export a view, dashboard or SQL result asynchronously](workflows/export-data-asynchronously.md) - Create an export job, poll or receive a callback, and download the file - the path for dashboards, query tables, large tables and ad-hoc SQL that the synchronous export rejects.
* [Load data into a table (small, large and very large files)](workflows/import-large-dataset.md) - Choose between synchronous import, asynchronous import job and batch import, then create or fill a table and verify the result.
* [Add users to an organization and a workspace, and set their roles](workflows/manage-users-and-roles.md) - Invite users to the organization, place them in a workspace with a role, promote or demote admins, deactivate leavers, and understand who may perform each step.
* [Schedule a recurring email delivery of a report or dashboard](workflows/schedule-email-report.md) - Create an email schedule with recipients and calendar frequency, trigger it once to test, enable or disable it, and update it safely.
* [Share views with users or groups, with row and column restrictions](workflows/share-view-with-row-filter.md) - Grant a permission set on one or more views to users or a group, optionally limiting rows with criteria and columns with column lists, then inspect, update or revoke the share.
* [Train an AutoML model, deploy it and score a table](workflows/train-and-run-automl-model.md) - The end-to-end AutoML sequence - create an analysis on a training table, wait for models to train, deploy the best model, run predictions into an output table, and clean up.

# SDK Examples

* [SDK examples](sdk-examples/index.md) - code samples in 9 languages for every OpenAPI-documented endpoint, one document per endpoint.

# References

* [OpenAPI specifications](references/openapi/index.md) - the OpenAPI 3 files this bundle was generated from, one per domain plus the shared components file.
* [endpoint-catalog.json](references/endpoint-catalog.json) - machine-readable endpoint catalog for tooling (Postman collections, MCP servers, SDK generators).
* [manifest.json](manifest.json) - bundle name, version, OKF version, counts and entry points.

* [llms.txt](llms.txt) - curated entry point for AI agents, with absolute links to every document.

# History

* [log.md](log.md) - update log for this bundle.
