---
type: API Endpoint
title: Copy Views
description: Copies one or more views from a source workspace to a destination workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/copy"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - view-operations
  - post
  - modeling
api:
  operation_id: copyViews
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/copy"
  domain: views-management
  group: view-operations
  oauth_scopes:
    - ZohoAnalytics.modeling.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: The authenticated user must be an Account Admin or Organization Admin (of the destination organisation).
  error_codes:
    - 7103
    - 7104
    - 7301
    - 7319
    - 8058
    - 8535
    - 15007
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1copy/post"
    config_schema: CopyViewsConfig
    response_schema: CopyViewsResponse
  sdk_examples: "/sdk-examples/views-management/view-operations/copy-views.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/views/copy`** - Copy Views (View Operations / Views Management).

Copies one or more views from a **source workspace** to a **destination workspace**. Both workspaces can belong to the same organisation or different organisations. This is a cross-workspace operation, unlike Save As which only works within a single workspace.

> ⚠️ **This API is not available on custom domains.**

> **On ZANALYTICS-ORGID for this API:** By default, the header identifies the **destination org** because the security check validates the user's admin rights in the destination. The source workspace is identified by `<workspace-id>` in the URL. The destination workspace is identified by `destWorkspaceId` in CONFIG. The `destWorkspaceId` must belong to the org that is ultimately resolved as the destination (either `ZANALYTICS-ORGID` directly, or `ZANALYTICS-DEST-ORGID` when supplied).

> **Cross-organisation copy (Account Admin):** Set `ZANALYTICS-ORGID` to the **destination** organisation's ID. The `workspaceKey` of the source workspace must be provided to authorise the copy.

> **Cross-organisation copy (Organization Admin):** An Organization Admin who has admin access to multiple organisations can copy to a target org by setting `ZANALYTICS-ORGID` to their own (source) org and providing `ZANALYTICS-DEST-ORGID` as the destination org. The system validates that the caller is a member of the destination org before proceeding. The `workspaceKey` is still required when the destination org differs from the source workspace's org.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `copyViews` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/copy` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - For Account Admins (or when no `ZANALYTICS-DEST-ORGID` is supplied): must be the **destination Organisation ID** (the org where views will be copied to). For Organization Admins using `ZANALYTICS-DEST-ORGID`: this is the caller's own (current/source) organisation ID instead. This is a key difference from other APIs where ZANALYTICS-ORGID refers to the source workspace's org. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin (of the destination organisation). See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| ZANALYTICS-DEST-ORGID Header | **Optional** — Used by Organization Admins who have admin access to multiple organisations. Set this to the **destination** organisation ID when it differs from the org resolved from `ZANALYTICS-ORGID`. When present, the system validates that the caller is a member of the specified destination org and uses it as the target for the copy. When absent, the destination org defaults to the org resolved from `ZANALYTICS-ORGID`. |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1copy/post`; CONFIG schema `CopyViewsConfig`; response schema `CopyViewsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `ZANALYTICS-DEST-ORGID` | `<org-id>` | Optional | ID of the destination organization. It is meant for an Organization Admin who holds admin access in several organizations and wants to copy into one of them while keeping their own organization in ZANALYTICS-ORGID. When it is sent, it overrides destination resolution and the service validates that the caller is a member of it, failing with error 7301 otherwise and with error 8058 if the organization does not exist. When it is omitted, the destination organization is the one in ZANALYTICS-ORGID. |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the source workspace that holds the views to be copied. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameter

The CONFIG parameter is a JSON object sent as a **form parameter** named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `viewIds` | JSONArray of Long | **Yes** | — | Array of view IDs (from the source workspace) to copy. All IDs must belong to the workspace specified in the URL path. Maximum 1000 view IDs per request. If any view ID does not exist, the request fails with error **7104**. If a view ID does not belong to the source workspace, the request fails with error **7319**. |
| `destWorkspaceId` | Long | **Yes** | — | The ID of the destination workspace where views will be copied. Must belong to the organisation specified in `ZANALYTICS-ORGID`. If the destination workspace does not belong to the destination org, the request fails. |
| `workspaceKey` | String | Conditional | `""` | The copy key of the **source** workspace. **Required when copying across different organisations** (i.e., source and destination workspaces belong to different orgs). When the source and destination orgs are the same, this field is not required (may be omitted or passed as empty). Obtain the workspace copy key from the source workspace's settings. Alphanumeric characters only. If the cross-org copy is attempted without a matching `workspaceKey`, the request fails with error **15007**. |
| `copyWithDependentViews` | Boolean | No | `false` | When `true`: for each view in `viewIds`, all its dependent views (e.g., analysis views built on a table being copied) are also resolved and included in the copy operation automatically. When `false` (default): only the explicitly listed view IDs are copied. Dependent views that are not listed are excluded. Note that if a dependent view references a table that is not being copied, that dependent view may fail to copy or produce a broken state in the destination. Use `true` for tables to ensure the analysis views built on them are preserved. |
| `continueOnFailure` | Boolean | No | `false` | **Effective only when `copyWithDependentViews=true`.** When `true`: if any individual view in the expanded set fails to copy (e.g., due to a name conflict), the operation continues copying the remaining views and returns a partial result. When `false` (default): the entire operation is rolled back on the first failure. Use `true` for large batch copies where partial success is acceptable and you want to investigate failures after the fact. When `copyWithDependentViews=false`, this flag has no effect because each listed view is attempted independently. |
| `createAsSystemTable` | Boolean | No | `false` | When `true`: marks the copied tables in the destination workspace as system tables (a special internal classification). When `false` (default): copied views are standard user-visible tables. **This option is restricted to specific internal service integrations only.** Attempting to use `createAsSystemTable=true` without the required internal service context results in error **7301** (permission denied). External API consumers should always omit this field or set it to `false`. |

> **Note: `copyWithData` field** — the template definition accepts a `copyWithData` field for future use, but this field is not currently processed by the copy views operation. Table row data is not copied in cross-workspace copy; only the schema and view definitions are transferred.

## Notes from the OpenAPI specification

- This API is not available on custom domains.
- The destination organization is resolved from the headers. An **Account Admin** sends it in **ZANALYTICS-ORGID** and omits the second header. An **Organization Admin** with access to several organizations sends their own organization in **ZANALYTICS-ORGID** and the destination in **ZANALYTICS-DEST-ORGID**, and the service checks that the caller is a member of that destination organization first.
- **ZANALYTICS-ORGID** therefore means something different here than in the rest of this module, where it always names the organization of the workspace in the URL.
- **destWorkspaceId** must belong to the organization that is finally resolved as the destination - **ZANALYTICS-DEST-ORGID** when that header is sent, otherwise **ZANALYTICS-ORGID**. Validation fails when it does not.
- **workspaceKey** is required whenever the destination organization differs from the organization of the source workspace, on both the Account Admin and the Organization Admin route. For a copy within one organization it is ignored even if it is sent. A cross-organization copy without a matching key fails with error 15007 before any view is copied; there is no partial match.
- Source and destination may be the same workspace. Names can then conflict, and error 7111 is raised when a view of the same name already exists in the destination.
- **continueOnFailure** takes effect only when **copyWithDependentViews** is true. When **copyWithDependentViews** is false each listed view is attempted independently and the flag has no effect.
- When **copyWithDependentViews** is false and **continueOnFailure** is false, any failure cancels the whole operation. When **copyWithDependentViews** is true and **continueOnFailure** is false, the whole operation is rolled back on the first failure, including the resolved dependents.
- When **continueOnFailure** is true, only the views that copied successfully appear in the **views** array. There is no failure list in the response, and an empty array is returned with HTTP 200 when every view failed.
- If **viewIds** mixes valid and invalid IDs, validation fails on the first invalid ID with error 7104 or 7319 and no view is copied.
- Row data is not copied across workspaces. Only the schema and the view definitions are transferred.
- If the destination workspace reaches its row or view limit, the copy proceeds up to that limit and the remaining views fail. With **continueOnFailure** as true the partial copy is committed.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

# Examples

## Sample Requests

**Case 1 — Copy two tables to a destination workspace in the same org**

```http
POST /restapi/v2/workspaces/466206000000071000/views/copy HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"viewIds":[466206000000105001,466206000000106002],"destWorkspaceId":466206000000080000}
```

**Case 2 — Copy views with all dependents, continue on failure**

```http
POST /restapi/v2/workspaces/466206000000071000/views/copy HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"viewIds":[466206000000105001],"destWorkspaceId":466206000000080000,"copyWithDependentViews":true,"continueOnFailure":true}
```

**Case 3 — Cross-organisation copy using workspace key**

```http
POST /restapi/v2/workspaces/466206000000071000/views/copy HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000987654
Content-Type: application/x-www-form-urlencoded

CONFIG={"viewIds":[466206000000105001,466206000000107003],"destWorkspaceId":467200000000090000,"workspaceKey":"abc123def456","copyWithDependentViews":true,"continueOnFailure":false}
```

**Case 4 — Cross-organisation copy by Org Admin using `ZANALYTICS-DEST-ORGID`**

An Organization Admin who has admin access in both the source org and a separate destination org sets `ZANALYTICS-ORGID` to their own (source/current) org and `ZANALYTICS-DEST-ORGID` to the destination org. The `workspaceKey` is still required since the destination org differs from the source workspace's org.

```http
POST /restapi/v2/workspaces/466206000000071000/views/copy HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
ZANALYTICS-DEST-ORGID: 700000999888
Content-Type: application/x-www-form-urlencoded

CONFIG={"viewIds":[466206000000105001],"destWorkspaceId":467200000000090000,"workspaceKey":"abc123def456"}
```

## Sample Responses

**HTTP 200 OK** — Returns a mapping of source view IDs to newly created destination view IDs.

```json
{
  "status": "success",
  "summary": "Copy views",
  "data": {
    "views": [
      {
        "sourceViewId": "466206000000105001",
        "destViewId": "467200000000112001"
      },
      {
        "sourceViewId": "466206000000107003",
        "destViewId": "467200000000112002"
      }
    ]
  }
}
```

| Response Field | Type | Description |
|----------------|------|-------------|
| `status` | String | `"success"` on success. |
| `summary` | String | `"Copy views"` |
| `data.views` | Array | One entry per successfully copied view. |
| `data.views[].sourceViewId` | String | View ID in the source workspace. |
| `data.views[].destViewId` | String | Newly created view ID in the destination workspace. Use this to reference the copied view going forward. |

> When `continueOnFailure=true` and some views fail, only successfully copied views appear in the `views` array. There is no explicit failure list in the current response format.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Copy Views](../../../sdk-examples/views-management/view-operations/copy-views.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

## Combination Behaviour

| Combination | Behaviour |
|-------------|-----------|
| `copyWithDependentViews=false`, `continueOnFailure=false` | Only listed view IDs are copied. Any failure cancels the entire operation. |
| `copyWithDependentViews=false`, `continueOnFailure=true` | `continueOnFailure` has no effect. Only listed views are copied, each independently. |
| `copyWithDependentViews=true`, `continueOnFailure=false` | All dependent views are resolved and added. If any view (listed or resolved dependent) fails to copy, the entire operation is rolled back. |
| `copyWithDependentViews=true`, `continueOnFailure=true` | All dependent views are resolved. Failures on individual views are skipped; the operation proceeds and returns a combined result of successes. Failures are not in the `views` array of the response. |
| Cross-org copy (different source/dest org) without `workspaceKey` | Request fails immediately with error **15007** before any copy is attempted. |
| Cross-org copy with correct `workspaceKey` | Copy proceeds normally, subject to permission checks. |
| Same-org copy (source and dest in same org) | `workspaceKey` is ignored even if provided. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Source or destination workspace not found. | Verify `<workspace-id>` (URL) and `destWorkspaceId` (CONFIG) are valid. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | One or more view IDs in `viewIds` do not exist. | Verify each view ID in the array exists and is accessible. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. Occurs when the user is not an Account Admin / Org Admin of the destination org, or when `createAsSystemTable=true` is used outside of an authorised internal service. | Ensure the user is an Account Admin or Organization Admin of the destination organisation. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | One or more view IDs do not belong to the source workspace specified in the URL. | Ensure all view IDs in `viewIds` are from the workspace specified in `<workspace-id>`. |
| [8058](../../../foundations/error-codes.md#error-8058) | 400 | The organisation ID provided in `ZANALYTICS-DEST-ORGID` does not exist. | Provide a valid, existing organisation ID in `ZANALYTICS-DEST-ORGID`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |
| [15007](../../../foundations/error-codes.md#error-15007) | 400 | Cross-organisation copy not authorised. Occurs when the destination org differs from the source workspace's org and the `workspaceKey` is missing or incorrect. | Provide the correct `workspaceKey` of the source workspace for cross-org copy operations. |

# Related

- [View Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Save As View](save-as-view.md), [Create Similar Views](create-similar-views.md), [Rename View](rename-view.md), [Delete View](delete-view.md), [Get View List](get-views.md), [Get View Details](get-view-details.md), [Get View URL](get-view-url.md), [Get View Dependents](get-view-dependents.md), [Get Recent Views](get-recent-views.md).
- [SDK examples](../../../sdk-examples/views-management/view-operations/copy-views.md).
