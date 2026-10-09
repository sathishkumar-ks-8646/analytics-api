---
type: API Endpoint
title: Add Lookup
description: Creates a lookup relationship from the specified child column to a column in a reference table.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - lookups-and-relationships
  - post
  - modeling
api:
  operation_id: addLookup
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup"
  domain: data-modeling-and-schema
  group: lookups-and-relationships
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the workspace."
  error_codes:
    - 7107
    - 7166
    - 7183
    - 7184
    - 7280
    - 7301
    - 7319
    - 7377
    - 7379
    - 7509
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1columns~1{column-id}~1lookup/post"
    config_schema: AddLookupConfig
    response_schema: null
  sdk_examples: "/sdk-examples/data-modeling-and-schema/lookups-and-relationships/add-lookup.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup`** - Add Lookup (Lookups & Relationships / Data Modeling & Schema).

Creates a lookup relationship from the specified child column to a column in a reference (parent) table. The child column in the URL is the "many" side of the relationship; the `referenceColumnId` in the reference table is the "one" (unique key) side.

From the OpenAPI specification:

Creates a lookup relationship from the specified child column to a column in a reference table. A lookup links two tables of a workspace through a shared column, in the same way that a foreign key constraint links two relational tables.

The child column identified by `column-id` in the request URL is the many side of the relationship, and `referenceColumnId` in the reference table is the one, or unique key, side. Once the relationship exists, multi-table reports, pivot tables and query tables can pull data from both tables without a manual join, and the relationship becomes visible in the Schema View of the workspace.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `addLookup` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace, or any user with Design Modify permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1columns~1{column-id}~1lookup/post`; CONFIG schema `AddLookupConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |
| `{column-id}` | string | ID of the column. | [How to obtain](../../../foundations/identifiers.md#column-id) |

## URL Parameters

| Parameter | Description |
|-----------|-------------|
| `<workspace-id>` | Numeric ID of the workspace that owns both tables. Obtained from Get Workspace Info or Get Workspace List. |
| `<view-id>` | Numeric ID of the **child table** — the table whose column will hold the foreign-key values. Obtained from Get View List. |
| `<column-id>` | Numeric ID of the **child column** in the child table — the column that will store foreign-key values matching the reference column. Obtained from Get Table Metadata. |

## CONFIG Parameters

| Parameter | Type | Mandatory | Description |
|-----------|------|-----------|-------------|
| `referenceViewId` | Long (Integer) | **Yes** | Numeric ID of the **reference (parent) table** — the table that holds the unique key values. This view must be a table in the same workspace. Obtained from Get View List. |
| `referenceColumnId` | Long (Integer) | **Yes** | Numeric ID of the **reference (parent) column** in the reference table — the column with unique values that the child column maps to. Obtained from Get Table Metadata on the reference table. |

## Notes from the OpenAPI specification

- This API returns HTTP 204 No Content with no response body on success. There is no status or summary key to parse - treat the HTTP status code as the sole success indicator.
- Lookups can be created only between tables. A report, chart, pivot table, query table or dashboard cannot be used as the child view or as the reference view, and both tables must belong to the same workspace.
- A child column can take part in exactly one lookup relationship. To point the lookup at a different target, call the Remove Lookup API on the column first and then add the new relationship.
- The uniqueness of the reference column is validated before the relationship is created, and duplicate values return error 7509. Uniqueness is checked only at creation time - it is not enforced for rows inserted into the reference table afterwards.
- For GEO and GEO_NUM columns, the geo role level must match between the child and the reference column, such as country to country or city to city. A mismatch returns error 7183.
- An AUTO_NUMBER column cannot be used as the reference column.
- referenceViewId and referenceColumnId are sent as unquoted numbers, unlike the column ID arrays of the Hide Columns and Show Columns APIs, which are sent as strings.
- Adding a lookup has no effect on existing reports. It is the removal of a lookup that can break reports spanning the two tables.
- Resolve the IDs in this order: Get View List for the child view-id and for referenceViewId, then Get Table Metadata on each table for column-id and referenceColumnId.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON body (see [Error Codes](#error-codes) below).

# Examples

## Sample Requests

**Case 1 — Link `Order Details.Customer ID` to `Customers.ID`**

In this example, `Order Details` is the child table (many side), and `Customers` is the reference table (one side). The lookup means "each order's Customer ID references a unique Customer ID in the Customers table."

```http
POST /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns/7617000000508026/lookup HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"referenceViewId":7617000000509100,"referenceColumnId":7617000000509105}
```

**Case 2 — Link `Sales.Product Code` to `Products.Product Code`**

```http
POST /restapi/v2/workspaces/466206000000071000/views/7617000000511002/columns/7617000000511020/lookup HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"referenceViewId":7617000000512000,"referenceColumnId":7617000000512005}
```

**Case 3 — White label portal user creating a lookup**

```http
POST /restapi/v2/workspaces/466206000000071000/views/7617000000508001/columns/7617000000508026/lookup HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"referenceViewId":7617000000509100,"referenceColumnId":7617000000509105}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse; the absence of an error response (4xx/5xx with a `status: "failure"` body) is the sole success indicator.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Add Lookup](../../../sdk-examples/data-modeling-and-schema/lookups-and-relationships/add-lookup.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Unlike most other modeling APIs in this suite (which return `{"status":"success","summary":"..."}` on HTTP 200), Add Lookup returns a bare HTTP `204 No Content`. Do not attempt to parse a JSON body from a successful response — check only the HTTP status code. |
| **One lookup per child column** | A child column can participate in exactly one lookup relationship. To change the reference target, first call Remove Lookup on the column, then call Add Lookup with the new `referenceViewId` and `referenceColumnId`. |
| **Reference column uniqueness is validated** | Before creating the lookup, the system checks that all current values in `referenceColumnId` are unique. If not, error 7509 is returned. Note: uniqueness is checked at creation time only — the system does not enforce uniqueness for future inserts into the reference table. |
| **Data type compatibility is strict for geo columns** | For `GEO`/`GEO_NUM` typed columns, the geo role level must also match between child and reference column (e.g., both must be the same geographic level: country-to-country, city-to-city). Mismatched geo roles return error 7183. |
| **Auto-number columns cannot be reference columns** | Using an `AUTO_NUMBER` column as the reference side (`referenceColumnId`) is rejected. |
| **Lookup affects dependent views at remove time, not create time** | Adding a lookup has no impact on existing reports. Removing a lookup may break reports that span the two tables. |
| **Schema View reflects the relationship** | After a successful add, the relationship line between the two tables becomes visible in the workspace's Schema View (Relationship View). |
| **Dependency chain** | `<workspace-id>` → Get Workspace Info. `<view-id>` → Get View List (child table). `<column-id>` → Get Table Metadata on the child table. `referenceViewId` → Get View List (reference table). `referenceColumnId` → Get Table Metadata on the reference table. |

## Constraints on the Relationship

The following conditions must be satisfied for a lookup to be created successfully:

| Constraint | Detail |
|------------|--------|
| **Compatible data types** | The child column's data type and the reference column's data type must be compatible. For example, a `PLAIN` (text) child column can reference a `PLAIN` reference column; a `NUMBER` child can reference a `NUMBER` reference. Mixed type lookups (e.g., text → number) are rejected with error 7183. |
| **Reference column must be unique** | The reference column (`referenceColumnId`) must contain only unique values. If duplicate values are detected, error 7509 is returned. Use a primary key column or a column with a uniqueness constraint on the reference table. |
| **Child column must not already be a lookup** | Each child column can only have one lookup relationship. If the child column already has a lookup defined, error 7280 is returned. |
| **No self-referential lookup** | The reference table (`referenceViewId`) cannot be the same as the child table (`<view-id>`). Error 7379 is returned. |
| **No chained (lookup-on-lookup) columns** | The child column cannot itself be a column pulled in via an existing lookup relationship (i.e., it cannot be a derived lookup column). Error 7166 is returned. |
| **No circular relationships** | The relationship must not form a cycle across multiple tables (e.g., A → B → C → A). Error 7184 is returned. |
| **Both views in same workspace** | If `referenceViewId` does not belong to the same workspace as `<view-id>`, error 7319 is returned. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7107](../../../foundations/error-codes.md#error-7107) | 400 | The specified child column (`<column-id>`) does not exist in the child table. | Verify `<column-id>` using Get Table Metadata on the child view. |
| [7166](../../../foundations/error-codes.md#error-7166) | 400 | The child column is itself a lookup-derived column (lookup-on-lookup is not allowed). | Use a regular (base) column of the child table, not a column pulled in from a parent via an existing lookup. |
| [7183](../../../foundations/error-codes.md#error-7183) | 400 | The child column and the reference column have incompatible data types. | Ensure both columns share a compatible data type (e.g., both `PLAIN`, both `NUMBER`). For GEO columns, the geo role level must also match. |
| [7184](../../../foundations/error-codes.md#error-7184) | 400 | Adding this lookup would create a circular relationship chain across tables. | Review existing relationships and choose a reference table that does not already reference the child table (directly or transitively). |
| [7280](../../../foundations/error-codes.md#error-7280) | 400 | A lookup relationship already exists on this child column. | Remove the existing lookup first (using Remove Lookup), then add the new one. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is a Workspace Admin or has Design Modify permission on the workspace. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The reference table (`referenceViewId`) does not belong to the same workspace as the child table. | Both tables must be in the workspace identified by `<workspace-id>`. |
| [7377](../../../foundations/error-codes.md#error-7377) | 400 | An identical lookup relationship (same child column → same reference column) is already defined. | No action needed — the relationship already exists. |
| [7379](../../../foundations/error-codes.md#error-7379) | 400 | The reference table is the same as the child table (self-referential lookup not allowed). | Provide a `referenceViewId` that is different from `<view-id>`. |
| [7509](../../../foundations/error-codes.md#error-7509) | 400 | The reference column contains duplicate values; it must be unique to serve as the reference side. | Choose a column in the reference table that has unique values, or de-duplicate the reference column's data first. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Lookups & Relationships overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Remove Lookup](remove-lookup.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/lookups-and-relationships/add-lookup.md).
