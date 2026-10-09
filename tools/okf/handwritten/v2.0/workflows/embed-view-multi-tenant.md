---
type: Playbook
title: Embed a view for many tenants with per-tenant row filters
description: Mint one short-lived embed URL per end customer, each carrying its own criteria, permissions and column restrictions, then audit and revoke URLs.
tags:
  - zoho-analytics
  - rest-api-v2
  - workflow
  - playbook
  - embed
  - embedded-analytics
  - multi-tenant
sources:
  - id: markdown-docs
    resource: /domains/index.md
    title: API domain and group overviews in this bundle
generated:
  at: {{NOW}}
status: stable
---

# Goal

Render one Zoho Analytics view inside your application for many customers, each seeing only their rows, without creating Zoho Analytics users.

# Prerequisites

- The organization or workspace is enabled for **Embedded Analytics (OEM)**; otherwise every call fails with `8023`.
- Token scope `ZohoAnalytics.embed.read` (mint, list) and `.delete` (revoke).
- Caller is a Workspace Admin or holds Publish / Make Public permission, and non-owners are in the organization's OEM-enabled users list (`7301` otherwise).
- Call the **standard API host**, never a Client Portal domain (`7301`). Use `domainName` to build URLs on a portal domain.

# Steps

1. **Mint a URL per tenant** with [Get Embed URL](/domains/share-and-publish/embed-url/get-embed-url.md), `GET /restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embed`, URL-encoded CONFIG:

```json
{
  "criteria": "\"Sales_1\".\"Customer ID\"='C-1042'",
  "permissions": { "read": true, "export": true, "vud": true },
  "vudColumns": [ { "tableName": "Sales_1", "columnNames": ["Product", "Region"] } ],
  "validityPeriod": 86400,
  "includeToolBar": false
}
```

   `validityPeriod` is in seconds, default 3600, maximum 86400 (`8177`). Only `read`, `export`, `vud`, `drillDown`, `insight` can be granted. The response `data.embedUrl` is a credential; put it in an `<iframe src>` server-side and never log it.
2. **Re-mint before expiry.** URLs are not renewable; issue a new one when the old one lapses.
3. **Audit** outstanding URLs with [Fetch All Embed URLs](/domains/share-and-publish/embed-url/get-embed-urls.md) (`includeExpiredUrls: true` for history). Each entry returns `rsConfig`, `createdBy`, `expiryTime`, `permissions`, `criteria`.
4. **Revoke** a single URL with [Delete Embed URL](/domains/share-and-publish/embed-url/delete-embed-url.md) using its `rsConfig`.

# Notes

- Criteria are validated against the view (`8054`, `8154`) and stored encrypted.
- Exclude-model lists (`vudColumnsToExclude`, `drillColumnsToExclude`) win over include lists when both are sent.
- Page rendering options for embedded views are shared with published views: [Update Publish Configurations](/domains/share-and-publish/publish/overview.md).

# Related

- [Embed URL](/domains/share-and-publish/embed-url/overview.md)
- [White label & Client Portal](/foundations/white-label-client-portal.md)
- [Filter criteria syntax](/foundations/filter-criteria-syntax.md)
