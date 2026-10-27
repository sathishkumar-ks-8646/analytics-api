---
type: API Domain
title: Organization Management
description: "APIs that return information about the resource usage, subscription plan, and workspace or view identity lookups available within an organisation, that list the workspaces, dashboards and recently opened views the calling user can reach in that organisation, and that read and update the organisation-wide and per-workspace access restriction settings."
tags:
  - zoho-analytics
  - rest-api-v2
  - organization-management
  - api-domain
api:
  domain: organization-management
  groups:
    - group: org-info-and-settings
      title: Organization Info & Settings
      doc: "/domains/organization-management/org-info-and-settings/overview.md"
      endpoint_count: 3
    - group: org-level-listings
      title: Org-Level Listings
      doc: "/domains/organization-management/org-level-listings/overview.md"
      endpoint_count: 3
    - group: security-controls
      title: Security Controls
      doc: "/domains/organization-management/security-controls/overview.md"
      endpoint_count: 4
  endpoint_count: 10
  openapi: "/references/openapi/org-management-grouped-api.json"
sources:
  - id: openapi-spec
    resource: "/references/openapi/org-management-grouped-api.json"
    title: OpenAPI 3 specification - org-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T10:58:51Z
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

APIs that return information about the resource usage, subscription plan, and workspace or view identity lookups available within an organisation, that list the workspaces, dashboards and recently opened views the calling user can reach in that organisation, and that read and update the organisation-wide and per-workspace access restriction settings.

# API Groups

| Group | Endpoints | Description |
|---|---|---|
| [Organization Info & Settings](org-info-and-settings/overview.md) | 3 | APIs for retrieving organisation information, resource usage, subscription details, and workspace or view metadata. |
| [Org-Level Listings](org-level-listings/overview.md) | 3 | APIs that list, for one organisation, the workspaces the calling user can reach, the dashboards across those workspaces, and the views the user opened most recently. |
| [Security Controls](security-controls/overview.md) | 4 | APIs for reading and updating the access restriction settings of an organisation and of an individual workspace - sharing, private links, public views, export and email. |

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Resource Details](org-info-and-settings/get-resource-details.md) | GET | `/restapi/v2/resources` | `getResourceDetails` | `ZohoAnalytics.usermanagement.read` | 200 |
| [Get Subscription Details](org-info-and-settings/get-subscription-details.md) | GET | `/restapi/v2/subscription` | `getSubscriptionDetails` | `ZohoAnalytics.usermanagement.read` | 200 |
| [Get Meta Details From Name](org-info-and-settings/get-meta-details.md) | GET | `/restapi/v2/metadetails` | `getMetaDetails` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Org Workspaces](org-level-listings/get-org-workspaces.md) | GET | `/restapi/v2/orgs/workspaces` | `getOrgWorkspaces` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Org Dashboards](org-level-listings/get-org-dashboards.md) | GET | `/restapi/v2/orgs/dashboards` | `getOrgDashboards` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Org Recent Items](org-level-listings/get-org-recent-items.md) | GET | `/restapi/v2/orgs/recentitems` | `getOrgRecentItems` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Org Access Restrictions](security-controls/get-org-access-restrictions.md) | GET | `/restapi/v2/security-controls/access-restrictions` | `getOrgAccessRestrictions` | `ZohoAnalytics.metadata.read` | 200 |
| [Update Org Access Restrictions](security-controls/update-org-access-restrictions.md) | PUT | `/restapi/v2/security-controls/access-restrictions` | `updateOrgAccessRestrictions` | `ZohoAnalytics.metadata.update` | 204 |
| [Get Workspace Access Restrictions](security-controls/get-workspace-access-restrictions.md) | GET | `/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions` | `getWorkspaceAccessRestrictions` | `ZohoAnalytics.metadata.read` | 200 |
| [Update Workspace Access Restrictions](security-controls/update-workspace-access-restrictions.md) | PUT | `/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions` | `updateWorkspaceAccessRestrictions` | `ZohoAnalytics.metadata.update` | 204 |

# Related

- [All domains](../index.md)
- [OpenAPI specification for this domain](../../references/openapi/org-management-grouped-api.json)
- [Foundations](../../foundations/index.md)
