---
type: Concept
title: White Label and Client Portal
description: How Zoho Analytics White Label (Client Portal) custom domains interact with the REST API v2 - portal request hosts, the domainName attribute, workspace domain access, and which API families are allowed or blocked in a portal context.
tags:
  - zoho-analytics
  - rest-api-v2
  - white-label
  - client-portal
  - custom-domain
  - embedded-analytics
sources:
  - id: md-domain
    resource: /domains/workspace-management/domain-and-white-label/overview.md
    title: Domain & White Label Access - group overview
  - id: md-embed
    resource: /domains/share-and-publish/embed-url/overview.md
    title: Embed URL - group overview
  - id: md-all
    resource: /domains/index.md
    title: White Label sections and Case samples across the markdown reference
generated:
  at: {{NOW}}
status: stable
---

# Summary

**White Label**, also called **Client Portal**, lets an organization expose Zoho Analytics under its own branded domain (for example `reports.clientbrand.com`). The Account Admin configures the domain in Zoho Analytics settings; portal users then sign in and view reports on that domain without Zoho branding. For the API this creates three concepts: the **portal request host**, the **`domainName` CONFIG attribute**, and **workspace domain access**.

# Three Concepts

| Concept | What it is | Where it appears |
|---|---|---|
| **Portal request host** | Sending the API request to the custom domain (`Host: portal.customdomain.com`) instead of `analyticsapi.zoho.*`. The caller is then treated as a portal-context user. | Sample "White Label / Client Portal" cases throughout the endpoint documents. |
| **`domainName` attribute** | A CONFIG field naming the portal domain, sent from the **standard** API host by a portal admin. Scopes the operation (a share, an embed URL, a user role change) to that portal's users or builds returned URLs on that domain. | Share Views, Get Embed URL, Add/Change Users, Workspace Variables and others. Fails with `8060` if the domain does not exist and `8061` if the caller does not administer it. |
| **Workspace domain access** | A per-workspace switch that makes the workspace visible through the portal domain. Off by default. | [Enable Workspace for Domain Access](/domains/workspace-management/domain-and-white-label/overview.md) and Disable. Requires an Account Admin or Organization Admin **and** an active portal domain for the organization. |

# Which API Families Work in a Portal Context

| Family | Request through portal host | Notes |
|---|---|---|
| Data import, export, rows, sync | Allowed | Standard behaviour; the workspace must be enabled for domain access for portal users to use it. |
| Sharing, publish, slideshows, email schedules | Allowed | Returned URLs (`publicUrl`, `privateUrl`, `slideUrl`) use the portal domain for portal workspaces. Portal users being shared to need `domainName`. |
| Users and roles | Allowed with `domainName` | Role changes inside a portal are scoped to that portal; `ORGADMIN` cannot be assigned inside a portal (`6089`). |
| **Embed URL** (Get, Fetch All, Delete) | **Blocked** with `7301` | Embedded Analytics is called from the standard host; use `domainName` in Get Embed URL to build the URL on the portal domain. |
| **AutoML** | **Blocked** with `7301` | All eleven endpoints must use the standard host. |
| Workspace domain access | Standard host only | Administrative. |

Each group overview states its own portal behaviour under a "White Label / Client Portal Behaviour" heading when it deviates from the default.

# Practical Rules

- The **API host and the returned URL host differ**. Requests go to `analyticsapi.zoho.*`; `embedUrl`, `publicUrl`, `privateUrl` and `slideUrl` point at `analytics.zoho.*` or at the portal domain.
- To embed for a white-labelled customer, call Get Embed URL on the standard host with `domainName`; do not call the portal host.
- A workspace not enabled for domain access is invisible to portal users; embed requests for it fail with `12052` (`WORKSPACE_NOT_ENABLED_FOR_DOMAIN_ACCESS`).
- Portal users count against the same plan quotas as other users; see [Rate limits and quotas](/foundations/rate-limits-and-quotas.md).

# Related

- [Domain & White Label Access](/domains/workspace-management/domain-and-white-label/overview.md)
- [Embed URL](/domains/share-and-publish/embed-url/overview.md)
- [Roles & permissions](/foundations/roles-and-permissions.md)
