---
type: API Domain
title: Reports & Dashboards
description: "API for Reports and Dashboards in Zoho Analytics - covering the creation, update and metadata retrieval of analysis views, and the listing, creation, metadata retrieval and update of dashboards."
tags:
  - zoho-analytics
  - rest-api-v2
  - reports-and-dashboards
  - api-domain
api:
  domain: reports-and-dashboards
  groups:
    - group: reports
      title: Reports (Analysis Views)
      doc: "/domains/reports-and-dashboards/reports/overview.md"
      endpoint_count: 3
    - group: dashboards
      title: Dashboards
      doc: "/domains/reports-and-dashboards/dashboards/overview.md"
      endpoint_count: 6
  endpoint_count: 9
  openapi: "/references/openapi/reports-dashboards-grouped-api.json"
sources:
  - id: openapi-spec
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

API for Reports and Dashboards in Zoho Analytics - covering the creation, update and metadata retrieval of analysis views, and the listing, creation, metadata retrieval and update of dashboards.

# API Groups

| Group | Endpoints | Description |
|---|---|---|
| [Reports (Analysis Views)](reports/overview.md) | 3 | APIs for creating, updating and reading the metadata of analysis views (charts, pivot tables and summary views) inside a workspace. |
| [Dashboards](dashboards/overview.md) | 6 | APIs for listing dashboards accessible to a user, and for creating, reading and updating dashboards inside a workspace. |

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Create Analysis View](reports/create-report.md) | POST | `/restapi/v2/workspaces/{workspace-id}/reports` | `createReport` | `ZohoAnalytics.modeling.create` | 200 |
| [Update Analysis View](reports/update-report.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}` | `updateReport` | `ZohoAnalytics.modeling.update` | 204 |
| [Get Report Metadata](reports/get-report-metadata.md) | GET | `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata` | `getReportMetadata` | `ZohoAnalytics.modeling.read` | 200 |
| [Get All Dashboards](dashboards/get-dashboards.md) | GET | `/restapi/v2/dashboards` | `getDashboards` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Owned Dashboards](dashboards/get-owned-dashboards.md) | GET | `/restapi/v2/dashboards/owned` | `getOwnedDashboards` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Shared Dashboards](dashboards/get-shared-dashboards.md) | GET | `/restapi/v2/dashboards/shared` | `getSharedDashboards` | `ZohoAnalytics.metadata.read` | 200 |
| [Create Dashboard](dashboards/create-dashboard.md) | POST | `/restapi/v2/workspaces/{workspace-id}/dashboards` | `createDashboard` | `ZohoAnalytics.modeling.create` | 200 |
| [Get Dashboard Metadata](dashboards/get-dashboard-metadata.md) | GET | `/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}/metadata` | `getDashboardMetadata` | `ZohoAnalytics.modeling.read` | 200 |
| [Update Dashboard](dashboards/update-dashboard.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}` | `updateDashboard` | `ZohoAnalytics.modeling.update` | 204 |

# Related

- [All domains](../index.md)
- [OpenAPI specification for this domain](../../references/openapi/reports-dashboards-grouped-api.json)
- [Foundations](../../foundations/index.md)
