---
type: Reference
title: Data centers and base URLs
description: The Zoho Analytics API host (ZohoAnalytics_Server_URI) and OAuth accounts host for each data center, and the rules for choosing them.
tags:
  - zoho-analytics
  - rest-api-v2
  - data-centers
  - base-url
  - regions
sources:
  - id: zoho-api-spec
    resource: https://www.zoho.com/analytics/api/v2/api-specification.html
    title: Zoho Analytics API v2 - API specification, Server URI section (public documentation)
    author: team:zoho-analytics-public-docs
  - id: markdown-docs
    resource: /domains/index.md
    title: API domain and group overviews in this bundle
generated:
  at: {{NOW}}
status: stable
---

# Summary

Zoho hosts Analytics in several regional data centers. An organization lives in exactly one of them, and every API call for that organization must go to that data center's API host. The OAuth token must also be issued by the same region's `accounts` host. Every path in this bundle is written against the US host `https://analyticsapi.zoho.com`; substitute the host for your region.

# Hosts per Data Center

| Data center | API host (`ZohoAnalytics_Server_URI`) | OAuth accounts host | Web application host |
|---|---|---|---|
| United States (US) | `analyticsapi.zoho.com` | `accounts.zoho.com` | `analytics.zoho.com` |
| Europe (EU) | `analyticsapi.zoho.eu` | `accounts.zoho.eu` | `analytics.zoho.eu` |
| India (IN) | `analyticsapi.zoho.in` | `accounts.zoho.in` | `analytics.zoho.in` |
| Australia (AU) | `analyticsapi.zoho.com.au` | `accounts.zoho.com.au` | `analytics.zoho.com.au` |
| Japan (JP) | `analyticsapi.zoho.jp` | `accounts.zoho.jp` | `analytics.zoho.jp` |
| China (CN) | `analyticsapi.zoho.com.cn` | `accounts.zoho.com.cn` | `analytics.zoho.com.cn` |
| Saudi Arabia (SA) | `analyticsapi.zoho.sa` | `accounts.zoho.sa` | `analytics.zoho.sa` |
| Canada (CA) | `analyticsapi.zohocloud.ca` | `accounts.zohocloud.ca` | `analytics.zohocloud.ca` |

The API host column is taken from Zoho's public API specification page. The `accounts` and web application hosts follow Zoho's standard per-region domain pattern; the source markdown documents only mention the US, EU and IN API hosts explicitly. Verify the accounts host for your region in the Zoho API Console if in doubt.

# Rules

- **Find your region** from the URL you use to sign in to Zoho Analytics in a browser (`analytics.zoho.eu` means the EU data center), or from the `api_domain`/location information returned during OAuth.
- **Tokens are region-bound.** An access token from `accounts.zoho.eu` is rejected with `8535` by `analyticsapi.zoho.com`.
- **Returned URLs are region-aware.** `downloadUrl` from export jobs, `embedUrl`, `publicUrl`, `privateUrl` and `slideUrl` are fully qualified and already point at the correct region; prefer them over hand-assembled URLs. Published and embed URLs point at the **web application host** (or a Client Portal custom domain), never at the API host.
- **White Label / Client Portal domains** (for example `portal.customdomain.com`) can be used as the request host for some API families; see [White label & Client Portal](/foundations/white-label-client-portal.md).
- **SDKs** take the data center as a configuration value (for example the Ruby client's `with_data_center("US")`); see [SDK clients](/foundations/sdk-clients.md).

# Related

- [Authentication](/foundations/authentication.md)
- [Request conventions](/foundations/request-conventions.md)
