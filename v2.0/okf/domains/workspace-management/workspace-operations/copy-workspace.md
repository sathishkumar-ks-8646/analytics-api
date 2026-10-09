---
type: API Endpoint
title: Copy Workspace
description: "Creates a copy of an existing workspace, either within the same organization or in a different organization."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - workspace-operations
  - post
  - modeling
api:
  operation_id: copyWorkspace
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}"
  domain: workspace-management
  group: workspace-operations
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
  permission_required: The authenticated user must be an Account Admin or Organization Admin of the destination organisation.
  error_codes:
    - 7103
    - 7301
    - 7951
    - 8024
    - 8058
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}/post"
    config_schema: CopyWorkspaceConfig
    response_schema: CopyWorkspaceResponse
  sdk_examples: "/sdk-examples/workspace-management/workspace-operations/copy-workspace.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}`** - Copy Workspace (Workspace Operations / Workspace Management).

Creates a copy of an existing workspace. The copy can be placed in the **same organisation** or a **different organisation**. When copying to a different organisation, the workspace's secret key (`workspaceKey`) must be provided for authorisation. The copy can optionally include all table data and/or preserve import source connections.

> **Rate Limit:** Only one copy operation per organisation is allowed to run at a time. A second request while a copy is in progress will be rejected.

> **Same-organisation copy:** Set `ZANALYTICS-ORGID` to the source workspace's organisation. No `workspaceKey` is required.

> **Cross-organisation copy (Account Admin):** Set `ZANALYTICS-ORGID` to the **destination** organisation's ID. The `workspaceKey` of the source workspace must be provided to authorise the copy — obtain it via the [Get Workspace Secret Key](get-workspace-secret-key.md) API.

> **Cross-organisation copy (Organization Admin):** An Organization Admin who has admin access to multiple organisations can copy to a target org by setting `ZANALYTICS-ORGID` to their own (source) org and providing `ZANALYTICS-DEST-ORGID` as the destination org. The system validates that the caller is a member of the destination org before proceeding. The `workspaceKey` is still required when the destination org differs from the source workspace's org.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `copyWorkspace` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - For same-org copies: the workspace's own organisation ID. For cross-org copies by Account Admin: the **destination** organisation ID. For cross-org copies by Org Admin: the caller's own (source) organisation ID — use `ZANALYTICS-DEST-ORGID` to specify the destination separately. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the destination organisation. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| ZANALYTICS-DEST-ORGID Header | **Optional** — Used by Organization Admins who have admin access in multiple organisations. Set this to the **destination** organisation ID when it differs from the org resolved from `ZANALYTICS-ORGID`. When present, the system validates that the caller is a member of the specified destination org and uses it as the target for the copy. When absent, the destination org defaults to the caller's own resolved organisation. |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}/post`; CONFIG schema `CopyWorkspaceConfig`; response schema `CopyWorkspaceResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `ZANALYTICS-DEST-ORGID` | `<org-id>` | Optional | The ID of the destination organization into which the workspace has to be copied. It is used by Organization Admins who have admin access in more than one organization. When this header is present, the system validates that the requesting user is a member of the specified organization and uses it as the target of the copy. When it is absent, the destination organization defaults to the organization resolved from the ZANALYTICS-ORGID header. |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | The ID of the workspace. It can be obtained using any of the workspace list APIs. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameter

CONFIG is **mandatory**. It must be sent as a form-encoded body parameter named `CONFIG`.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `newWorkspaceName` | String | **Yes** | — | Name for the copied workspace. Must be unique in the destination organisation. Max 50 characters. |
| `newWorkspaceDesc` | String | No | `""` | Description for the copied workspace. Max 250 characters. When omitted, the new workspace has an empty description (the source description is not copied automatically). |
| `workspaceKey` | String | **Yes (cross-org)** | `null` | The secret key of the **source** workspace. Required when the destination organisation (ZANALYTICS-ORGID) differs from the source workspace's organisation. Not required when copying within the same organisation. Obtain this key from the [Get Workspace Secret Key](get-workspace-secret-key.md) API. |
| `copyWithData` | Boolean | No | `false` | When `false` (default): copies only the workspace structure (tables schema, views, formulas, dashboards) — no data rows are copied. When `true`: copies the complete workspace including all table data rows. Copying with data increases both duration and resource usage significantly. |
| `copyWithImportSource` | Boolean | No | `false` | When `false` (default): import source connections are not copied. Tables in the copied workspace will have no active data source — data must be re-imported manually. When `true`: preserves import source configurations (cloud storage connections, database connectors, etc.) — the copied tables will retain their import source links. Only meaningful when there are active data sources in the source workspace. Cannot be `true` when the source workspace has only live/direct database connections (those always require manual reconnection). |

## Notes from the OpenAPI specification

- Only one copy operation is allowed to run at a time per organization. A second request raised while a copy is in progress is rejected.
- For a copy within the same organization, set **ZANALYTICS-ORGID** to the organization of the source workspace. The **workspaceKey** is not validated in this case.
- For a cross-organization copy by an Account Admin, set **ZANALYTICS-ORGID** to the destination organization ID and provide the **workspaceKey** of the source workspace.
- For a cross-organization copy by an Organization Admin, set **ZANALYTICS-ORGID** to the source organization ID and **ZANALYTICS-DEST-ORGID** to the destination organization ID. The system validates that the requesting user is a member of the destination organization before the copy begins.
- A **ZANALYTICS-DEST-ORGID** that does not refer to an existing organization fails with error code 8058. A requesting user who is not a member of that organization fails with error code 7301.
- A cross-organization copy raised without a **workspaceKey**, or with a key that does not match the secret key of the source workspace, fails with error code 8024.
- The description of the source workspace is not copied. Provide **newWorkspaceDesc** explicitly to set a description on the copy.
- When **copyWithImportSource** is set to true, only the import based data sources such as the scheduled syncs, the file imports and the API pushed data are retained. Live and direct database connections cannot be copied and have to be reconnected manually.
- Setting **copyWithData** to true on a large workspace increases both the duration and the resource usage of the operation significantly.
- The copy fails with error code 7951 when the destination organization has reached its workspace limit.
- The response data holds only the **workspaceId** of the copy. Use the Get Workspace Info API to retrieve the complete record.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `data.workspaceId` | String | Unique identifier of the newly created copy. Use this as `<workspace-id>` in subsequent calls. |

# Examples

## Sample Requests

**Case 1 — Copy within the same org (structure only, no data)**

```http
POST /restapi/v2/workspaces/466206000000071000 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"newWorkspaceName":"Sales Analytics – Copy","newWorkspaceDesc":"Backup copy of Sales Analytics"}
```

**Case 2 — Copy within the same org including all data**

```http
POST /restapi/v2/workspaces/466206000000071000 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"newWorkspaceName":"Sales Analytics – Full Backup","copyWithData":true}
```

**Case 3 — Cross-organisation copy by Account Admin (requires `workspaceKey`)**

The `ZANALYTICS-ORGID` is set to the **destination** organisation. The `workspaceKey` authorises access to the source workspace from the destination org's perspective.

```http
POST /restapi/v2/workspaces/466206000000071000 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000999888
Content-Type: application/x-www-form-urlencoded

CONFIG={"newWorkspaceName":"Sales Analytics (Migrated)","workspaceKey":"02aee9b66f299843c961d3712fe09684","copyWithData":true,"copyWithImportSource":true}
```

**Case 4 — Cross-organisation copy by Org Admin using `ZANALYTICS-DEST-ORGID`**

An Organization Admin who has admin access in both the source org and a separate destination org sets `ZANALYTICS-ORGID` to their own (source) org and `ZANALYTICS-DEST-ORGID` to the destination org. The `workspaceKey` is still required since the destination org differs from the source workspace's org.

```http
POST /restapi/v2/workspaces/466206000000071000 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
ZANALYTICS-DEST-ORGID: 700000999888
Content-Type: application/x-www-form-urlencoded

CONFIG={"newWorkspaceName":"Sales Analytics (Org B Copy)","workspaceKey":"02aee9b66f299843c961d3712fe09684"}
```

## Sample Responses

**HTTP 200 OK** — Workspace copied successfully.

```json
{
  "status": "success",
  "summary": "Copy workspace",
  "data": {
    "workspaceId": "466206000000296001"
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Copy Workspace](../../../sdk-examples/workspace-management/workspace-operations/copy-workspace.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`workspaceKey` required for cross-org copies only** | When copying within the same organisation, `workspaceKey` is not validated. When copying to a different organisation (Account Admin or Org Admin cross-org), the key must match the source workspace's secret key from Get Workspace Secret Key. |
| **`ZANALYTICS-ORGID` vs `ZANALYTICS-DEST-ORGID`** | Account Admins doing a cross-org copy set `ZANALYTICS-ORGID` to the destination org. Org Admins who have access to multiple orgs set `ZANALYTICS-ORGID` to their own (source) org and `ZANALYTICS-DEST-ORGID` to the destination org. |
| **Rate limit: 1 concurrent copy per org** | Only one workspace copy can run at a time per organisation. A second request while one is in progress will be rejected. |
| **`newWorkspaceDesc` is not copied from source** | The description of the copy must be provided explicitly in `newWorkspaceDesc`. If omitted, the copied workspace has an empty description. |
| **`copyWithImportSource=true` limitation** | Only import-based data sources (scheduled syncs, file imports, API-pushed data) are preserved in the copy. Live/direct database connections must be manually reconnected. |
| **Response returns only `workspaceId`** | The ID of the newly created copy. Use Get Workspace Info to retrieve full details. |
| **Dependency** | `workspaceKey` → Get Workspace Secret Key (for the source workspace). Source workspace ID from any workspace list API. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Source workspace not found. | Verify `<workspace-id>` of the source workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User is not an Account Admin or Organization Admin of the destination organisation. | The caller must be an admin of the destination org, not just the source org. |
| [7951](../../../foundations/error-codes.md#error-7951) | 400 | The destination organisation has reached its workspace limit. | Upgrade the destination org's plan or remove unused workspaces. |
| [8024](../../../foundations/error-codes.md#error-8024) | 400 | Cross-org copy attempted without a valid `workspaceKey`, or the provided key does not match the source workspace's secret key. | Obtain the correct `workspaceKey` from the source workspace owner using Get Workspace Secret Key, then retry. For same-org copies, omit `workspaceKey`. |
| [8058](../../../foundations/error-codes.md#error-8058) | 400 | The organisation ID provided in `ZANALYTICS-DEST-ORGID` does not exist. | Provide a valid, existing organisation ID in `ZANALYTICS-DEST-ORGID`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |

# Related

- [Workspace Operations overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Workspace](create-workspace.md), [Rename Workspace](rename-workspace.md), [Delete Workspace](delete-workspace.md), [Export as Template](export-as-template.md), [Get All Workspace List](get-all-workspaces.md), [Get Owned Workspace List](get-owned-workspaces.md), [Get Shared Workspace List](get-shared-workspaces.md), [Get Workspace Secret Key](get-workspace-secret-key.md), [Get Workspace Info](get-workspace-details.md).
- [SDK examples](../../../sdk-examples/workspace-management/workspace-operations/copy-workspace.md).
