# Version 2.10.0

**SDK:** C# · Go · JAVA · PHP · PYTHON · NodeJS · Ruby

## Newly added APIs

**Org-Level Listings** — one organization-scoped endpoint for each thing you used to fetch three ways.

- Get Org Workspaces
- Get Org Dashboards
- Get Org Recent Items

**Data Alerts** — create and manage alerts that watch a report or table and notify on a condition.

- Get Alerts In Workspace
- Get Alerts In View
- Get View Metadata For Alert
- Get Alert Configuration
- Create Alert
- Update Alert
- Delete Alerts
- Change Alert Status
- Run Alert
- Get Alert Events

**Linked Workspaces** — push a master workspace's design into client workspaces and track the sync.

- Get Linked Workspaces For Organization
- Get Linked Workspaces For Master Workspace
- Get Linkable Workspaces
- Get Workspace Linking Compatibility
- Link Workspaces
- Sync Linked Workspaces
- Get Linked Workspace Sync Details
- Unlink Workspaces

**Workspace Backup and Restore** — take a backup on demand, download it, and restore from it.

- Get Workspace Backups
- Backup Workspace Now
- Download Workspace Backup
- Restore Workspace from Backup
- Get Workspace Backup Status
- Get Workspace Restore Status

**Security Controls** — read and update IP / access restrictions at organization and workspace level.

- Get Org Access Restrictions
- Update Org Access Restrictions
- Get Workspace Access Restrictions
- Update Workspace Access Restrictions

**Dashboards and Reports** — build and round-trip a dashboard or report definition through the API.

- Create Dashboard
- Read Dashboard Metadata
- Update Dashboard
- Create Report
- Read Report Metadata
- Update Report

## Enhancements

- **Go SDK** reaches parity with the other languages on raw-data import: `ImportRawData` and `ImportRawDataInNewTable` are now available, so a CSV/JSON payload held in memory can be imported without first writing it to a file.
- **Get Org Dashboards** is paged (`pageNo`, `recordsPerPage`), searchable by name (`searchKey`) and can be narrowed to named workspaces (`workspaceIds`). The endpoints it replaces returned everything in one response.
