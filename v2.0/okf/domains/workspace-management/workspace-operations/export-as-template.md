---
type: API Endpoint
title: Export as Template
description: Exports the selected views of the specified workspace as a reusable template file in the .atpt (Zoho Analytics Template) format.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/template/data"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-operations
  - get
  - metadata
api:
  operation_id: exportAsTemplate
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/template/data"
  domain: workspace-management
  group: workspace-operations
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: query
    required: true
  success_status: 200
  response_content_types:
    - application/octet-stream
  permission_required: The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access.
  error_codes:
    - 7103
    - 7104
    - 7301
    - 7319
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1template~1data/get"
    config_schema: ExportTemplateConfig
    response_schema: null
  sdk_examples: "/sdk-examples/workspace-management/workspace-operations/export-as-template.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/template/data`** - Export as Template (Workspace Operations / Workspace Management).

Exports selected views from the specified workspace as a reusable template file. The response is a binary file in `.atpt` (Zoho Analytics Template) format — not a JSON payload. This file can be imported into another workspace to recreate the selected views and their structural dependencies.

> **File response:** The API returns the template as a binary file attachment. The response `Content-Type` will be `application/octet-stream` or similar binary content type. Save the response body directly as a `.atpt` file.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `exportAsTemplate` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/template/data` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be a Workspace Admin of the specified workspace. Account Admins and Organization Admins also have access. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - **mandatory** |
| Success response | HTTP 200 - `application/octet-stream` |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1template~1data/get`; CONFIG schema `ExportTemplateConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | The ID of the workspace. It can be obtained using any of the workspace list APIs. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameter

CONFIG is **mandatory**. It must be sent as a query parameter or form-encoded body parameter named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `viewIds` | Array of Longs | **Yes** | — | List of view IDs to include in the template. Min 1 view, max 1000. All specified views must belong to the same workspace. The export automatically includes structural dependencies (lookup columns, formula columns, related tables) required for the selected views to function. |
| `fileName` | String | No | System-generated | Custom name for the exported `.atpt` file (without extension). When omitted, the system generates a file name based on the workspace name. |

## Notes from the OpenAPI specification

- The response of this API is a binary **.atpt** file and not a JSON payload. Handle the response as a binary stream and write it to the disk as a **.atpt** file.
- The template file holds the structure and the design alone. The schema definitions, the formula and lookup columns, the calculated fields and the view design configurations are exported, but the data rows of the source tables are not.
- The **viewIds** array cannot be empty. It should hold a minimum of one view ID and a maximum of 1000 view IDs.
- All the view IDs should belong to the workspace specified in the request URL. A view ID that belongs to a different workspace fails with error code 7319.
- The structural dependencies of the selected views are included automatically. A table referenced by a lookup column is added to the template even when its ID is not listed in **viewIds**.
- When **fileName** is omitted, the name of the exported file is generated from the workspace name.
- As this is a GET request, the CONFIG value should be stringified and URL encoded before it is sent.

# Response

## Success Response

HTTP `200` with content type `application/octet-stream`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

# Examples

## Sample Requests

**Case 1 — Export two specific views as a template**

```http
GET /restapi/v2/workspaces/466206000000071000/template/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"viewIds":[466206000000085001,466206000000085003]}
```

**Case 2 — Export with a custom file name**

```http
GET /restapi/v2/workspaces/466206000000071000/template/data HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"viewIds":[466206000000085001,466206000000085003,466206000000085005],"fileName":"SalesAnalytics_Q3_Template"}
```

## Sample Responses

**HTTP 200 OK** — Binary `.atpt` file is returned as the response body.

```
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="SalesAnalytics_Q3_Template.atpt"

<binary file content>
```

The `.atpt` file contains:
- Schema definitions for all selected tables and views
- Formula columns, lookup columns, and calculated fields
- View design and layout configurations
- Structural dependencies needed for the views to render correctly

> **Data is not included.** The template file contains structure and design only — no data rows from the source tables are exported. To include data, use the workspace export/import data APIs.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Export as Template](../../../sdk-examples/workspace-management/workspace-operations/export-as-template.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Response is a binary `.atpt` file** | Unlike all other APIs in this document, the response is not JSON. It is a binary stream. Clients must handle the response as binary (not parse as JSON) and write it to disk as a `.atpt` file. |
| **`viewIds` cannot be empty** | At least one view ID must be provided. An empty array is rejected. |
| **Dependent tables are auto-included** | If a view has a lookup column referencing another table, that table is automatically included in the template even if its ID was not in `viewIds`. |
| **All view IDs must belong to the workspace** | If any view ID in `viewIds` belongs to a different workspace, the request fails with error 7319. |
| **Dependency** | `viewIds` → Get View List API for the workspace. Workspace ID → Get Workspace Info. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify `<workspace-id>`. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | One or more specified view IDs do not exist. | Verify all `viewIds` are valid using the Get View List API. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not a Workspace Admin, Account Admin, or Organization Admin. | Ensure the caller has at least Workspace Admin access. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | One or more specified view IDs do not belong to the specified workspace. | Ensure all `viewIds` belong to the workspace identified by `<workspace-id>`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Workspace Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Workspace](create-workspace.md), [Copy Workspace](copy-workspace.md), [Rename Workspace](rename-workspace.md), [Delete Workspace](delete-workspace.md), [Get All Workspace List](get-all-workspaces.md), [Get Owned Workspace List](get-owned-workspaces.md), [Get Shared Workspace List](get-shared-workspaces.md), [Get Workspace Secret Key](get-workspace-secret-key.md), [Get Workspace Info](get-workspace-details.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-operations/export-as-template.md).
