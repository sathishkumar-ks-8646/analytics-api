# Ruby SDK

The Zoho Analytics Ruby client wraps REST API v2. It carries your OAuth
credentials, keeps the access token alive, and exposes the API as four scoped
instances hanging off one client object.

::: danger Create the client once, not per request
Constructing a new client on every request will get your integration blocked by
Zoho Accounts within minutes. Read [Authentication](authentication.md#the-access-token-throttle)
before you ship anything.
:::

## Start here

1. [Getting started](getting-started.md) — install, construct a client, make a first call.
2. [Authentication](authentication.md) — OAuth, scopes, data centers, and the token throttle.
3. [Configuration](configuration.md) — timeouts, proxies, custom headers, regions.
4. [Errors](errors.md) — the response envelope, HTTP statuses, and the codes worth branching on.
5. [Limits](limits.md) — throttles, concurrency guards and plan quotas.

## Guides

- [Importing data](guides/importing-data.md) — synchronous, batched and job-based imports.
- [Exporting data](guides/exporting-data.md) — synchronous export and the asynchronous job flow.

## API reference

| Surface | Scope |
|---|---|
| [AnalyticsClient](reference/analytics-client.md) | Credentials, transport settings, instance factories. |
| [OrgAPI](reference/org-api.md) | Users, roles, admins, subscription, security controls. |
| [WorkspaceAPI](reference/workspace-api.md) | Views, folders, tags, schedules, alerts, backups, sharing. |
| [ViewAPI](reference/view-api.md) | Rows, columns, formulas, publishing, per-view metadata. |
| [BulkAPI](reference/bulk-api.md) | Import and export, synchronous and asynchronous. |

## Conventions in this SDK

| | |
|---|---|
| Method naming | `snake_case`. |
| Identifiers | `String`. |
| Failure surface | `ServerError` (`.error_code`, `.response_content`, `.is_oauth_error`) and `ParseError`. |
| Source | `ruby/source/lib/zoho_analytics_client.rb` |
| Sample program | `ruby/sample/sample.rb` |
