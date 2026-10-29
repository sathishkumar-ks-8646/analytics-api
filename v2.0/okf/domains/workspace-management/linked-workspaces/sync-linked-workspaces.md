---
type: API Endpoint
title: Sync Linked Workspaces
description: "Pushes the master workspace's design to its linked clients."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - linked-workspaces
  - post
  - modeling
api:
  operation_id: syncLinkedWorkspaces
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync"
  domain: workspace-management
  group: linked-workspaces
  api_units:
    api_id: 2082
    action: SYNC_LINKED_WORKSPACES
    category: METADATA
    units: 3
    units_basis: per_request
    units_note: "3 units per request"
    category_frequency_limit: 60 requests/minute
  oauth_scopes:
    - ZohoAnalytics.modeling.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or an Organization Admin of the organisation in ZANALYTICS-ORGID and of the organisation that owns <workspace-id>. When masterViewIds is used, the caller must additionally administer the organisation owning each listed view's workspace."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 8060
    - 8077
    - 8079
    - 8080
    - 8083
    - 8119
    - 8246
    - 8248
    - 8250
    - 8251
    - 8504
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1linkedworkspaces~1sync/post"
    config_schema: SyncLinkedWorkspacesConfig
    response_schema: null
  sdk_examples: "/sdk-examples/workspace-management/linked-workspaces/sync-linked-workspaces.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T11:33:37Z
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync`** - Sync Linked Workspaces (Linked Workspaces / Workspace Management).

Pushes the master workspace's design to its linked clients. The request either syncs every link, or names the sandboxes to sync and — per sandbox — either everything or a specific list of master-workspace views.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `syncLinkedWorkspaces` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the master workspace. |
| Permission required | The authenticated user must be an Account Admin or an Organization Admin of the organisation in ZANALYTICS-ORGID and of the organisation that owns <workspace-id>. When masterViewIds is used, the caller must additionally administer the organisation owning each listed view's workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| API units | 3 units per request - action `SYNC_LINKED_WORKSPACES` (api-id `2082`), **METADATA** category. See [API units](../../../foundations/api-units.md). |
| Frequency limit | 60 requests/minute across all **METADATA**-category calls of the organization. See [API units](../../../foundations/api-units.md#unit-categories-and-frequency-limits). |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1linkedworkspaces~1sync/post`; CONFIG schema `SyncLinkedWorkspacesConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID, shown in the Zoho Analytics UI under Settings > Organisation. See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | The ID of the workspace. It can be obtained using any of the workspace list APIs. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Max Length | Description |
|-----------|------|-----------|---------|------------|-------------|
| `scope` | String (enum) | **Yes** | — | 20 | `ALL` syncs every linked sandbox of this master; `SELECTED` requires `clients`. **Case-sensitive — must be upper case** (`8119` otherwise). See [`scope` Values](overview.md#scope-values) and [The `scope` Attribute](overview.md#the-scope-attribute). |
| `clients` | JSONArray of JSONObject | Conditional | — | 5000000 | Per-sandbox sync instructions, **1–100** entries. **Mandatory when `scope` is `SELECTED`**, and **must be omitted when `scope` is `ALL`** — either mistake is `8250`. See [`clients` Sync Fields](#clients-sync-fields). |

### `clients` Sync Fields

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `sandboxId` | Long | **Yes** | — | 20 | The link to sync, as a JSON **number**. Must already be mapped to `<workspace-id>` (`8248`). A blank or absent value is `8251`. |
| `scope` | String (enum) | **Yes** | — | 20 | `ALL` syncs every eligible entity to this sandbox; `SELECTED` requires `masterViewIds`. **Case-insensitive** — it is upper-cased before comparison, unlike the top-level `scope`. Anything other than `ALL` or `SELECTED` is `8251`. See [`scope` Values](overview.md#scope-values). |
| `masterViewIds` | JSONArray of String | Conditional | — | 50000 | Master-workspace view IDs to push to this sandbox, as numeric **strings**, **1–1000** entries. **Mandatory when this entry's `scope` is `SELECTED`**, and **must be omitted when it is `ALL`** — either mistake is `8251`. |

> **A single request may mix both per-client modes.** Entries with `scope: "ALL"` are collected and scheduled together; entries with `scope: "SELECTED"` push their named views immediately. See the Notes below — the two halves do not behave the same way.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`).

# Examples

## Sample Requests

**Case 1 — Sync every linked workspace**

```http
POST /restapi/v2/workspaces/137687000271334001/linkedworkspaces/sync HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scope": "ALL"
}
```

**Case 2 — Sync two named sandboxes, one fully and one with selected views**

```http
POST /restapi/v2/workspaces/137687000271334001/linkedworkspaces/sync HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scope": "SELECTED",
    "clients": [
        {
            "sandboxId": 137687000012345001,
            "scope": "ALL"
        },
        {
            "sandboxId": 137687000012345002,
            "scope": "SELECTED",
            "masterViewIds": ["137687000006991601", "466206000000105001"]
        }
    ]
}
```

**Case 3 — `clients` supplied alongside `scope: "ALL"` (rejected)**

```http
POST /restapi/v2/workspaces/137687000271334001/linkedworkspaces/sync HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scope": "ALL",
    "clients": [
        {
            "sandboxId": 137687000012345001,
            "scope": "ALL"
        }
    ]
}
```

**Case 4 — Per-client `SELECTED` without `masterViewIds` (rejected)**

```http
POST /restapi/v2/workspaces/137687000271334001/linkedworkspaces/sync HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scope": "SELECTED",
    "clients": [
        {
            "sandboxId": 137687000012345001,
            "scope": "SELECTED"
        }
    ]
}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status.

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — Failure paired with Case 3**

```json
{
    "status": "failure",
    "summary": "INVALID_CONFIGURATION_SYNC_SCOPE_LINKED_WORKSPACES",
    "data": {
        "errorCode": 8250,
        "errorMessage": "Invalid configuration. Kindly provide scope as 'ALL' to sync all linked workspaces or set scope to 'SELECTED' with valid clients array."
    }
}
```

**HTTP 400 Bad Request — Failure paired with Case 4**

```json
{
    "status": "failure",
    "summary": "INVALID_CONFIGURATION_SYNC_CLIENT_SCOPE_LINKED_WORKSPACES",
    "data": {
        "errorCode": 8251,
        "errorMessage": "Invalid configuration. For each client, kindly set scope to 'ALL' to sync all views, or set scope to 'SELECTED' with a valid 'masterViewIds' array."
    }
}
```

**HTTP 400 Bad Request — A `sandboxId` is not linked to this master**

```json
{
    "status": "failure",
    "summary": "SANDBOX_NOT_MAPPED_TO_MASTER_WORKSPACE",
    "data": {
        "errorCode": 8248,
        "errorMessage": "One or more provided sandbox IDs are not mapped to the given master workspace: 137687000012345009"
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Sync Linked Workspaces](../../../sdk-examples/workspace-management/linked-workspaces/sync-linked-workspaces.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`204` means accepted, not delivered** | Full-sandbox syncs are handed to a scheduler and run afterwards. The only way to learn what a sync did is [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md). |
| **The two per-client modes behave differently** | `scope: "SELECTED"` entries push their `masterViewIds` **inline**, during the request. `scope: "ALL"` entries — and a top-level `scope: "ALL"` — are **scheduled**. A mixed request therefore completes part of its work before responding and defers the rest. |
| **Validation order matters on a mixed request** | All sandbox IDs are validated against the master before anything runs (`8248`), but the inline per-view pushes happen **before** the scheduled full syncs are queued. A failure after the first push leaves the request partially applied. |
| **Top-level `scope` is case-sensitive, per-client `scope` is not** | `{"scope":"all"}` is `8119`; `clients[].scope: "all"` is accepted. Send upper case everywhere. |
| **`ALL` means every link of this master** | Not every link in the organisation. The sandbox list is resolved from `<workspace-id>`. |
| **Not idempotent in effect** | Each call pushes again. Re-syncing an unchanged master is harmless but is not free, and it overwrites client-side drift. |
| **Duplicate sandbox IDs collapse** | A sandbox named twice with `scope: "ALL"` is synced once. |
| **The master must not be a client** | A master that is itself linked as somebody's client is refused with `8246` before any sync work starts. |
| **Views are addressed in the master, not the client** | `masterViewIds` are IDs in `<workspace-id>`. Client-side IDs are never accepted. |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md) → `sandboxId` (+ [Get View List](../../views-management/view-operations/get-views.md) → `masterViewIds`) → Sync Linked Workspaces → [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — The master workspace was not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — A `masterViewIds` entry does not exist. | Verify every view ID via [Get View List](../../views-management/view-operations/get-views.md) against the master workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller does not administer the header organisation, the master's organisation, or the organisation owning a workspace named in `masterViewIds`; or the request arrived through a Client Portal / White Label domain. | Authenticate as an organisation administrator and call from the standard API host. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use the standard API host. |
| [8077](../../../foundations/error-codes.md#error-8077) | 400 | `EMPTY_JSON_CONFIGURATION` — `CONFIG` is empty. | Send at least `{"scope":"ALL"}`. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — `scope` is missing from CONFIG. | Add the top-level `scope`. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — `CONFIG` is not parseable JSON. | Send a valid, URL-encoded JSON object. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE` — The top-level `scope` is not exactly `ALL` or `SELECTED`. | Send upper-case `ALL` or `SELECTED`. |
| [8246](../../../foundations/error-codes.md#error-8246) | 400 | `INVALID_MASTER_WORKSPACE_MAPPING` — `<workspace-id>` is itself linked as a client of another master. | Sync from the real master. |
| [8248](../../../foundations/error-codes.md#error-8248) | 400 | `SANDBOX_NOT_MAPPED_TO_MASTER_WORKSPACE` — One or more `clients[].sandboxId` values are not linked to this master. The message names them. | Use sandbox IDs from [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md). |
| [8250](../../../foundations/error-codes.md#error-8250) | 400 | `INVALID_CONFIGURATION_SYNC_SCOPE_LINKED_WORKSPACES` — `clients` was supplied with `scope: "ALL"`, omitted with `scope: "SELECTED"`, or resolved to nothing to sync. | Send `{"scope":"ALL"}` or `{"scope":"SELECTED","clients":[…]}`. |
| [8251](../../../foundations/error-codes.md#error-8251) | 400 | `INVALID_CONFIGURATION_SYNC_CLIENT_SCOPE_LINKED_WORKSPACES` — A `clients[]` entry is missing `sandboxId`, carries a `scope` other than `ALL` / `SELECTED`, supplies `masterViewIds` with `scope: "ALL"`, or omits them with `scope: "SELECTED"`. | Give each entry a `sandboxId` plus either `{"scope":"ALL"}` or `{"scope":"SELECTED","masterViewIds":[…]}`. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — The `CONFIG` parameter was not sent, or `clients` is outside its 1–100 bound. | Send `CONFIG` with a valid JSON object. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |

# Related

- [Linked Workspaces overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Linked Workspaces For Organization](get-linked-workspaces-for-organization.md), [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md), [Get Linkable Workspaces](get-linkable-workspaces.md), [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md), [Link Workspaces](link-workspaces.md), [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md), [Unlink Workspaces](unlink-workspaces.md).
- [SDK examples](../../../sdk-examples/workspace-management/linked-workspaces/sync-linked-workspaces.md).
- [API units](../../../foundations/api-units.md) - unit cost, unit categories and frequency limits for every endpoint.
