---
type: Reference
title: Filter criteria syntax
description: Grammar and rules of the SQL-like criteria expression used by Zoho Analytics REST API v2 to filter rows in exports, row updates and deletes, shares, embed URLs, publish configurations and email schedules.
tags:
  - zoho-analytics
  - rest-api-v2
  - criteria
  - filter
  - sql
  - row-level-security
sources:
  - id: md-row
    resource: /domains/data-operations/row-operations/overview.md
    title: Row Operations - group overview
  - id: md-async-export
    resource: /domains/data-operations/async-data-export/overview.md
    title: Asynchronous Data Export - group overview
  - id: md-sharing
    resource: /domains/share-and-publish/sharing/overview.md
    title: Sharing - group overview
  - id: md-embed
    resource: /domains/share-and-publish/embed-url/overview.md
    title: Embed URL - group overview
generated:
  at: {{NOW}}
status: stable
---

# Summary

`criteria` is a string holding a SQL `WHERE`-clause style expression. Column names are wrapped in **double quotes**, optionally qualified with the table name; string literals use **single quotes**. The same grammar is used wherever a row filter appears in CONFIG.

```text
"Region"='East'
"SalesTable"."Region"='East'
"Sales">1000 and "Region"='West'
"Region" in ('East','West') and "Order Date">='01-Jan-2026'
("Status"='Open' or "Status"='Pending') and "Amount">=500
```

# Grammar

| Element | Form | Notes |
|---|---|---|
| Column reference | `"Column Name"` or `"Table Name"."Column Name"` | Use the display names as shown in Zoho Analytics. Qualify with the table when the view joins several tables. |
| String literal | `'text'` | Escape an embedded single quote by doubling it: `'O''Brien'`. |
| Number literal | `1000`, `12.5` | Unquoted. |
| Date literal | `'01-Jan-2026'` | Quoted, in a format the column's date pattern accepts. |
| Comparison | `=`, `!=`, `<>`, `<`, `<=`, `>`, `>=` | |
| Set membership | `in (...)`, `not in (...)` | |
| Pattern | `like 'A%'`, `not like` | `%` matches any run of characters. |
| Null test | `is null`, `is not null` | |
| Boolean logic | `and`, `or`, `not`, parentheses | Case-insensitive keywords. |

Aggregate functions (`sum`, `avg`, `count`, ...) are **not** permitted; they fail with `7333`.

# Where It Is Used

| Endpoint family | Attribute | Effect |
|---|---|---|
| [Export Data from a View](/domains/data-operations/sync-data-export/export-data-view.md), [Create Export Job using View ID](/domains/data-operations/async-data-export/create-export-job-view-id.md) | `criteria` | Exports only matching rows. |
| [Create Export Job using SQL Query](/domains/data-operations/async-data-export/create-export-job-sql-query.md) | `tableCriteriaList[].criteria` | One filter per table the SQL touches (0 to 25 entries). Row selection otherwise belongs in the SQL `WHERE`. |
| [Update Row](/domains/data-operations/row-operations/update-rows.md), [Delete Row](/domains/data-operations/row-operations/delete-rows.md) | `criteria` | Selects the rows to change. Add Row does not accept it. |
| [Share Views](/domains/share-and-publish/sharing/share-views.md), Update Shared Details | `criteria` | Row-level security: the shared user or group sees only matching rows. Single view per call. |
| [Get Embed URL](/domains/share-and-publish/embed-url/get-embed-url.md) | `criteria` | Bound to that one URL; the multi-tenant primitive for embedded analytics. Stored encrypted. |
| Publish configurations, email schedule report bursts | `criteria`, `criteriaExpression` | Per-URL or per-recipient filtering. |

# Rules That Matter in Practice

- **Validation happens before execution.** A bad criteria fails the call (no export job is created, no rows are changed).
- **Column must exist** in the view or table, otherwise `7330`. A table name that is not part of the view fails with `7332`. A syntactically invalid expression fails with `7331`; one that parses but cannot be converted to SQL fails with `7327`. In the embed and publish APIs the equivalent codes are `8054` (`INVALID_FILTER_CRITERIA`) and `8154` (`COLUMN_NOT_PRESENT_IN_TABLE`).
- **Tabular views** may only reference columns of their own base table (`7543` otherwise).
- **Shared users are always ANDed.** When a user with a share-level filter calls an export or row API with their own `criteria`, the server combines both with `AND`; a shared user can never widen their slice.
- **Omitting `criteria`** means all rows the caller is entitled to see.
- **Encoding.** Inside CONFIG the expression is a JSON string, so every `"` becomes `\"`; the whole CONFIG is then URL-encoded, so `\"` becomes `%5C%22` and `'` may stay or become `%27`. Build the expression as a plain string, let a JSON serializer escape it, then percent-encode the result.

```json
{ "criteria": "\"SalesTable\".\"Region\"='East' and \"Sales\">1000" }
```

- **Length limits** are endpoint specific (for example 250,000 characters for embed URLs; 65,535 for report-burst `criteriaExpression`).
- **Sensitive.** Criteria strings are excluded from server request logging in the Row APIs.

# Related

- [Request conventions](/foundations/request-conventions.md)
- [Roles & permissions](/foundations/roles-and-permissions.md) (share permissions that pair with row filters)
- [Error code catalog](/foundations/error-codes.md)
