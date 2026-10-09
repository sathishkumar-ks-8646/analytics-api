---
type: API Overview
title: Zoho Analytics REST API v2 - overview
description: What the Zoho Analytics REST API v2 is, how it is organized into 10 domains and 168 endpoints, and the five conventions every call shares.
resource: https://analyticsapi.zoho.com/restapi/v2
tags:
  - zoho-analytics
  - rest-api-v2
  - overview
  - start-here
sources:
  - id: markdown-docs
    resource: /domains/index.md
    title: API domain and group overviews in this bundle
  - id: openapi
    resource: /references/openapi
    title: OpenAPI 3 specifications (10 domain files plus shared components)
generated:
  at: {{NOW}}
status: stable
---

# Summary

Zoho Analytics is a business-intelligence and analytics platform. Its **REST API v2** lets programs do everything a user can do in the product: create workspaces and tables, load and export data, model schema, build reports and dashboards, share and publish views, schedule emails, manage users, and train AutoML models. The API is HTTP plus JSON. Every request is authenticated with an OAuth 2.0 access token, most requests are scoped to one organization through a header, and structured input travels in a single JSON object called `CONFIG`.

This bundle documents **168 endpoints** in **10 domains** and **33 API groups**. Every endpoint has its own document under `/domains/`, every shared rule has its own document under `/foundations/`, and every code sample lives under `/sdk-examples/`.

# The Five Conventions

| Convention | Rule | Detail |
|---|---|---|
| **Base URL** | `https://analyticsapi.zoho.com/restapi/v2` on the US data center; other data centers use their own host. | [Data centers](/foundations/data-centers.md) |
| **Authentication** | `Authorization: Zoho-oauthtoken <access-token>` on every call; the token must carry the scope the endpoint declares. | [Authentication](/foundations/authentication.md), [OAuth scopes](/foundations/oauth-scopes.md) |
| **Organization header** | `ZANALYTICS-ORGID: <org-id>` on every call except the few user-scoped ones. | [Request conventions](/foundations/request-conventions.md), [Identifiers](/foundations/identifiers.md) |
| **CONFIG parameter** | Structured input is one JSON object named `CONFIG`: URL-encoded query parameter on GET, form field on POST/PUT/DELETE, form part on multipart uploads. | [Request conventions](/foundations/request-conventions.md#the-config-parameter) |
| **Response envelope** | Success is HTTP 200 with `{"status":"success","summary":...,"data":{...}}` or HTTP 204 with no body; failure is HTTP 4xx/5xx with `{"status":"failure","summary":"<CONSTANT>","data":{"errorCode":<int>,"errorMessage":"..."}}`. | [Response envelope](/foundations/response-envelope.md), [Error code catalog](/foundations/error-codes.md) |

# Object Model in One Paragraph

An **organization** (identified by `orgId`) owns **workspaces**. A workspace contains **views**: **tables** hold rows of data, **query tables** compute rows from SQL, **reports** (charts, pivots, summary and tabular views) visualize tables, and **dashboards** arrange reports. Tables have **columns**, may be linked by **lookups**, and may carry **custom formula columns** and **aggregate formulas**. Views are organized in **folders**, can be **shared** with users and **groups** under a permission set, **published** as public or private URLs, **embedded** with short-lived URLs, presented as **slideshows**, and delivered by **email schedules**. Data enters through **imports** or **datasource syncs** and leaves through **exports**. See the [Glossary](/foundations/glossary.md).

# Domains

| Domain | Groups | What it covers |
|---|---|---|
| [Organization Management](/domains/organization-management/overview.md) | Organization Info & Settings | List organizations, plan and resource usage, resolve names to IDs. |
| [Users & Groups](/domains/users-and-groups/overview.md) | Organization Users, Workspace Users, Workspace Groups | Membership, roles, activation, admins, groups. |
| [Workspace Management](/domains/workspace-management/overview.md) | Workspace Operations, Folders, Preferences, Domain & White Label Access | Create, copy, rename, delete, list workspaces; folders; favourites; portal access. |
| [Data Modeling & Schema](/domains/data-modeling-and-schema/overview.md) | Table & Schema, Columns, Lookups, Query Tables, Formula Columns, Aggregate Formulas, Variables | Everything about the shape of data. |
| [Data Operations](/domains/data-operations/overview.md) | Sync/Async Import, Sync/Async Export, Row Operations, Data Sync & Connectivity | Everything about moving data in and out. |
| [Views Management](/domains/views-management/overview.md) | View Operations, View Preferences, Trash, Auto Analysis | Copy, rename, delete, list views; favourites; restore; auto-generate views. |
| [Reports & Dashboards](/domains/reports-and-dashboards/overview.md) | Reports, Dashboards | Create, read and update report and dashboard definitions. |
| [Share & Publish](/domains/share-and-publish/overview.md) | Sharing, Publish, Embed URL, Slideshow | Give other people access to views. |
| [Schedules & Alerts](/domains/schedules-and-alerts/overview.md) | Email Schedules | Recurring email delivery of views. |
| [Data Science & ML](/domains/dsml/overview.md) | AutoML | Train, inspect, deploy and run machine-learning models on tables. |

# Typical Call Sequence

1. Obtain an access token ([Authentication](/foundations/authentication.md)).
2. Call [Get Org List](/domains/organization-management/org-info-and-settings/get-organizations.md) and pick the `orgId`.
3. Resolve workspace and view IDs with [Get Meta Details From Name](/domains/organization-management/org-info-and-settings/get-meta-details.md) or the listing endpoints.
4. Call the endpoint you need, sending `CONFIG` as the endpoint document specifies.
5. Read `status`; on `failure`, look up `data.errorCode` in the [Error code catalog](/foundations/error-codes.md).

Multi-step tasks (export a dashboard, load a large file, share with a row filter, embed for many tenants) are written out step by step in [Workflows](/workflows/index.md).

# Related

- [How to use this bundle](/how-to-use-this-bundle.md) - structure, frontmatter keys and navigation rules for tools and agents.
- [Endpoint catalog](/endpoint-catalog.md) - all endpoints in one table.
- [Foundations](/foundations/index.md) - every shared rule.
