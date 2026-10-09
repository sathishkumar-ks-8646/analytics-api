---
type: Reference
title: Request conventions
description: The rules shared by every Zoho Analytics REST API v2 request - URL structure, path placeholders, mandatory headers, the CONFIG parameter and how to encode it per HTTP method, multipart uploads, and idempotency.
tags:
  - zoho-analytics
  - rest-api-v2
  - request
  - headers
  - config-parameter
  - encoding
sources:
  - id: markdown-docs
    resource: /domains/index.md
    title: API domain and group overviews in this bundle
  - id: openapi
    resource: /references/openapi
    title: OpenAPI 3 specifications (parameters, requestBody encodings)
generated:
  at: {{NOW}}
status: stable
---

# Summary

A Zoho Analytics v2 request is an HTTPS call to `https://<ZohoAnalytics_Server_URI>/restapi/v2/<path>` with two mandatory headers and, for most endpoints, one JSON object named `CONFIG`. The HTTP method decides where `CONFIG` goes. Everything else (data uploads, destination-organization headers) is endpoint specific and stated in the endpoint document.

# URL Structure

| Part | Example | Notes |
|---|---|---|
| Host | `analyticsapi.zoho.com` | Data-center specific, see [Data centers](/foundations/data-centers.md). Requests from a White Label / Client Portal custom domain are allowed for some API families and rejected for others, see [White label & Client Portal](/foundations/white-label-client-portal.md). |
| Prefix | `/restapi/v2` | All endpoints. Asynchronous (bulk) data operations use `/restapi/v2/bulk/...`. |
| Scope segments | `/workspaces/{workspace-id}`, `/views/{view-id}`, ... | Path placeholders are numeric IDs sent as strings. The markdown reference writes them as `<workspace-id>`; the OpenAPI files write `{workspace-id}`. See [Identifiers](/foundations/identifiers.md). |

Endpoints are **organization-scoped** (the `ZANALYTICS-ORGID` header selects the organization), **workspace-scoped** (`/workspaces/{workspace-id}/...`), **view-scoped** (`/workspaces/{workspace-id}/views/{view-id}/...`), or **user-scoped** (no organization header, for example Get Org List, Get All Workspace List).

# Headers

| Header | Value | When | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Always | See [Authentication](/foundations/authentication.md). |
| `ZANALYTICS-ORGID` | Organization ID | Every organization-, workspace- or view-scoped call | Missing header fails with `8083`. Wrong organization for the workspace fails with `7103`. Each endpoint's `api.org_id_header` says `required`, `optional` or `not-required`. |
| `ZANALYTICS-DEST-ORGID` | Destination organization ID | Copy Workspace, Copy Views, Copy Custom Formulas only | Used by an Organization Admin copying into another organization they belong to. Account Admins instead set `ZANALYTICS-ORGID` to the destination. |
| `Content-Type` | `application/x-www-form-urlencoded` | POST, PUT and DELETE requests that carry `CONFIG` in the body | Not needed for GET or for calls without CONFIG. |
| `Content-Type` | `multipart/form-data; boundary=...` | Import endpoints that upload a `FILE` | CONFIG travels as a form part named `CONFIG`. |

# The CONFIG Parameter

`CONFIG` is a **single JSON object** holding every structured input of the call. Its fields are listed per endpoint in the `Request` section (columns: Parameter, Type, Mandatory, Default, Description). The location depends on the HTTP method:

| Method | Where CONFIG goes | Encoding |
|---|---|---|
| GET | Query string parameter `CONFIG` | Serialize the object to a JSON string, then percent-encode it (`{` becomes `%7B`, `"` becomes `%22`, etc.). Some DELETE endpoints also use this form. |
| POST, PUT, DELETE | Body field `CONFIG` with `Content-Type: application/x-www-form-urlencoded` | `CONFIG=<url-encoded JSON string>`. Sample requests in this bundle show the JSON unencoded for readability. |
| POST with file upload | Multipart part named `CONFIG` | Sent alongside the `FILE` (binary) or `DATA` (text) part. |

Rules:

- Nested values keep their JSON types inside CONFIG (`true`, numbers, arrays, objects). Identifiers inside CONFIG (`viewIds`, `columnIds`, ...) are accepted as strings or numbers; responses always return them as strings.
- A malformed or double-encoded CONFIG, an unknown key, or a value of the wrong type fails with [`8080`](/foundations/error-codes.md#error-8080) (`INVALID_JSON_CONFIGURATION`); a missing mandatory CONFIG fails with [`8504`](/foundations/error-codes.md#error-8504).
- Filter expressions inside CONFIG (`criteria`) contain double quotes, which must be escaped as `\"` in the JSON and then percent-encoded. See [Filter criteria syntax](/foundations/filter-criteria-syntax.md).
- When an endpoint says CONFIG is optional and you need no options, omit the parameter entirely rather than sending `{}`.
- Length limits apply (commonly 100,000 characters; 200,000 for the SQL export job) and are stated per endpoint; exceeding them fails with `8507`.

Example of a GET with CONFIG, before and after encoding:

```text
CONFIG={"workspaceName":"Sales Analytics","viewName":"Revenue Trend"}

GET /restapi/v2/metadetails?CONFIG=%7B%22workspaceName%22%3A%22Sales%20Analytics%22%2C%22viewName%22%3A%22Revenue%20Trend%22%7D
```

Example of a POST with CONFIG as a form field:

```http
POST /restapi/v2/workspaces/137687000271334001/share HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG=%7B%22viewIds%22%3A%5B%22137687000006991601%22%5D%2C%22emailIds%22%3A%5B%22jane%40example.com%22%5D%2C%22permissions%22%3A%7B%22read%22%3Atrue%7D%7D
```

# Data Uploads

Import endpoints accept the payload either as a `FILE` multipart part (binary, up to 20 MB for synchronous import and 100 MB per request for asynchronous and batch import) or, for the two synchronous imports only, as a `DATA` form field holding the raw text (up to 10,000,000 characters). Send exactly one of the two. The `fileType` attribute in CONFIG tells the parser how to read the payload; it is not inferred from the file name. See [Import options](/foundations/import-options-and-enums.md).

# HTTP Methods and Idempotency

| Method | Used for | Idempotent |
|---|---|---|
| GET | Reads, ID resolution, synchronous export (returns a file), export-job creation | Yes for reads; export-job creation creates a new job each call. |
| POST | Create, import, share, copy, run | No. Repeating a create makes a duplicate or fails with an "already exists" code (for example `7104`-family name conflicts, `7321` already shared). |
| PUT | Update, rename, enable/disable, reorder | Usually yes; repeating an identical update is harmless. |
| DELETE | Delete, remove, unshare | Yes in effect; a second call fails with a not-found code. |

Many mutating endpoints return **HTTP 204 with no body** on success; check the status code, not the body. See [Response envelope](/foundations/response-envelope.md).

# Values and Types

- All IDs, and all row values in the Row APIs, are exchanged as **strings**.
- Booleans in CONFIG are JSON booleans; some dashboard and report settings are documented as string booleans (`"true"`), follow the endpoint document.
- Dates in row data follow the `dateFormat` you supply (Java date pattern, for example `dd-MMM-yyyy`).
- Names (workspace, view, column) are matched **case-sensitively** by the lookup endpoints and **case-insensitively** by the row-insert endpoint; each endpoint document states which.

# Related

- [Response envelope](/foundations/response-envelope.md)
- [Identifiers](/foundations/identifiers.md)
- [Filter criteria syntax](/foundations/filter-criteria-syntax.md)
- [Rate limits and quotas](/foundations/rate-limits-and-quotas.md)
