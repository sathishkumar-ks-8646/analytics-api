---
type: API Domain
title: Organization Management
description: "APIs that return information about the organisations, resource usage, subscription plan, and workspace or view identity lookups available to the authenticated user."
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
      endpoint_count: 4
  endpoint_count: 4
  openapi: "/references/openapi/org-management-grouped-api.json"
sources:
  - id: openapi-spec
    resource: "/references/openapi/org-management-grouped-api.json"
    title: OpenAPI 3 specification - org-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

APIs that return information about the organisations, resource usage, subscription plan, and workspace or view identity lookups available to the authenticated user. These are read-only metadata APIs and do not modify any data.

# API Groups

| Group | Endpoints | Description |
|---|---|---|
| [Organization Info & Settings](org-info-and-settings/overview.md) | 4 | APIs for retrieving organisation information, resource usage, subscription details, and workspace or view metadata. |

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Org List](org-info-and-settings/get-organizations.md) | GET | `/restapi/v2/orgs` | `getOrganizations` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Resource Details](org-info-and-settings/get-resource-details.md) | GET | `/restapi/v2/resources` | `getResourceDetails` | `ZohoAnalytics.usermanagement.read` | 200 |
| [Get Subscription Details](org-info-and-settings/get-subscription-details.md) | GET | `/restapi/v2/subscription` | `getSubscriptionDetails` | `ZohoAnalytics.usermanagement.read` | 200 |
| [Get Meta Details From Name](org-info-and-settings/get-meta-details.md) | GET | `/restapi/v2/metadetails` | `getMetaDetails` | `ZohoAnalytics.metadata.read` | 200 |

# Related

- [All domains](../index.md)
- [OpenAPI specification for this domain](../../references/openapi/org-management-grouped-api.json)
- [Foundations](../../foundations/index.md)
