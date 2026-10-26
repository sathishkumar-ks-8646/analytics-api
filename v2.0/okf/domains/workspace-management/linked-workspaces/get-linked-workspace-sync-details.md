---
type: API Endpoint
title: Get Linked Workspace Sync Details
description: "Returns, per linked sandbox, what the last sync did entity by entity and what is still waiting to be pushed."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - linked-workspaces
  - get
  - metadata
api:
  operation_id: getLinkedWorkspaceSyncDetails
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync"
  domain: workspace-management
  group: linked-workspaces
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: query
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or an Organization Admin of the organisation in ZANALYTICS-ORGID and of the organisation that owns <workspace-id>."
  error_codes:
    - 7103
    - 7301
    - 8060
    - 8080
    - 8083
    - 8248
    - 8504
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1linkedworkspaces~1sync/get"
    config_schema: GetLinkedWorkspaceSyncDetailsConfig
    response_schema: GetLinkedWorkspaceSyncDetailsResponse
  sdk_examples: "/sdk-examples/workspace-management/linked-workspaces/get-linked-workspace-sync-details.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-20T17:34:40Z
generated:
  by: process:build_okf
  at: 2026-10-23T07:58:54Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync`** - Get Linked Workspace Sync Details (Linked Workspaces / Workspace Management).

Returns, per linked sandbox, what the last sync did entity by entity and what is still waiting to be pushed. This is the only API that reports sync outcomes at entity granularity.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getLinkedWorkspaceSyncDetails` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the master workspace. |
| Permission required | The authenticated user must be an Account Admin or an Organization Admin of the organisation in ZANALYTICS-ORGID and of the organisation that owns <workspace-id>. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - optional |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1linkedworkspaces~1sync/get`; CONFIG schema `GetLinkedWorkspaceSyncDetailsConfig`; response schema `GetLinkedWorkspaceSyncDetailsResponse` |

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

## CONFIG Parameters

CONFIG is **optional** for this API and is sent as a query parameter. Omit it entirely to get every linked sandbox of the master.

| Parameter | Type | Mandatory | Default | Max Length | Description |
|-----------|------|-----------|---------|------------|-------------|
| `sandboxIds` | JSONArray of String | **Yes** when `CONFIG` is sent | All linked sandboxes of the master | 5000 | Restricts the response to these links, as numeric **strings**, **1–100** entries. Every ID must already be mapped to `<workspace-id>` (`8248`). |

> **`CONFIG` is optional, but `sandboxIds` is not optional within it.** The request template marks `sandboxIds` as a required key, so sending `CONFIG={}` is rejected while omitting `CONFIG` altogether is the supported way to ask for everything.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | `"Get linked workspace sync details"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.workspaces` | JSONArray | One entry per requested (or resolved) sandbox. **Always present**; `[]` when the master has no links. Note the key is `workspaces`, not `clients`. |
| `workspaces[].sandboxId` | String | The link's identifier. |
| `workspaces[].workspaceId` | String | The client workspace behind that link. |
| `workspaces[].workspaceName` | String | Client workspace display name. |
| `workspaces[].lastSync` | JSONObject | What the last sync did. **Always present.** |
| `lastSync.syncTime` | String | Time of the last successful sync as **epoch milliseconds in a string**, `"0"` when the link has never synced successfully. Same representation as the listing APIs — not a formatted date. |
| `lastSync.syncStatus` | String | `success`, `failure`, `partialSuccess`, `inProgress` or `unknown`. See [Sync Status Values](overview.md#sync-status-values). |
| `lastSync.syncedBy` | String | E-mail address of the user who ran that sync. |
| `lastSync.syncedByName` | String | Display name of that user. |
| `lastSync.syncedByZuId` | String | ZUID of that user, as a string. |
| `lastSync.entities` | JSONObject | Per-entity outcome of the last sync, read from the stored sync state. **Always present**, with three empty arrays when no state is stored. |
| `entities.dataSources[]` | JSONArray | Data sources touched by the last sync: `datasourceName`, `status`, `message`. **There is no `datasourceId` here** — unlike the same structure in [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md). |
| `entities.tables[]` / `entities.views[]` | JSONArray | Tables and reports touched by the last sync: `viewId`, `viewName`, `viewType`, `viewTypeId`, `status`, `message`. |
| `tables[].viewType` / `views[].viewType` | String | Display name of the entity type — `Table`, `Chart View`, … See [View Type Reference](overview.md#view-type-reference). Falls back to the raw numeric id rendered as a string for an unrecognised type. |
| `tables[].viewTypeId` / `views[].viewTypeId` | Number | Numeric type id companion to `viewType`. Native JSON number. |
| `tables[].status` / `views[].status` / `dataSources[].status` | String | Per-entity outcome — `success`, `warning` or `failure`. See [Entity Status Values](overview.md#entity-status-values). |
| `tables[].message` / `views[].message` / `dataSources[].message` | String | Human-readable reason, normalised to `"Compatible"` when there was no problem. Always **English**, regardless of the caller's locale. |
| `workspaces[].hasPendingEntities` | Boolean | `true` when the master has changes not yet pushed to this client. Native JSON boolean. |
| `workspaces[].pendingEntities` | JSONObject | What the next sync would push. **Always present**, with three empty arrays when nothing is pending. |
| `pendingEntities.dataSources` | JSONArray | **Always empty.** Pending data sources are not reported; only tables and reports are. |
| `pendingEntities.tables[]` / `pendingEntities.views[]` | JSONArray | Pending entities: `viewId`, `viewName`, `viewType`, `viewTypeId`, `modifiedStatus`. |
| `pendingEntities.tables[].modifiedStatus` | String | `created`, `updated` or `deleted` — what the next sync will do to this entity on the client. See [Modified Status Values](overview.md#modified-status-values). |

# Examples

## Sample Requests

**Case 1 — Every linked sandbox of the master**

```http
GET /restapi/v2/workspaces/137687000271334001/linkedworkspaces/sync HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Two named sandboxes**

```http
GET /restapi/v2/workspaces/137687000271334001/linkedworkspaces/sync?CONFIG={"sandboxIds":["137687000012345001","137687000012345002"]} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — A sandbox that is not linked to this master (rejected)**

```http
GET /restapi/v2/workspaces/137687000271334001/linkedworkspaces/sync?CONFIG={"sandboxIds":["137687000012345009"]} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — One sandbox with a partially successful last sync and pending work**

```json
{
    "status": "success",
    "summary": "Get linked workspace sync details",
    "data": {
        "workspaces": [
            {
                "sandboxId": "137687000012345001",
                "workspaceId": "466206000000071000",
                "workspaceName": "Northwind Sandbox",
                "lastSync": {
                    "syncTime": "1779226560981",
                    "syncStatus": "partialSuccess",
                    "syncedBy": "jane.doe@example.com",
                    "syncedByName": "Jane Doe",
                    "syncedByZuId": "60002000000000123",
                    "entities": {
                        "dataSources": [
                            {
                                "datasourceName": "Books Connection",
                                "status": "success",
                                "message": "Compatible"
                            }
                        ],
                        "tables": [
                            {
                                "viewId": "137687000006991601",
                                "viewName": "Sales_Fact",
                                "viewType": "Table",
                                "viewTypeId": 0,
                                "status": "success",
                                "message": "Compatible"
                            }
                        ],
                        "views": [
                            {
                                "viewId": "466206000000105001",
                                "viewName": "Revenue by Region",
                                "viewType": "Chart View",
                                "viewTypeId": 2,
                                "status": "failure",
                                "message": "Formula column missing in client workspace"
                            }
                        ]
                    }
                },
                "hasPendingEntities": true,
                "pendingEntities": {
                    "dataSources": [],
                    "tables": [
                        {
                            "viewId": "137687000006991601",
                            "viewName": "Sales_Fact",
                            "viewType": "Table",
                            "viewTypeId": 0,
                            "modifiedStatus": "updated"
                        }
                    ],
                    "views": [
                        {
                            "viewId": "466206000000105001",
                            "viewName": "Revenue by Region",
                            "viewType": "Chart View",
                            "viewTypeId": 2,
                            "modifiedStatus": "created"
                        }
                    ]
                }
            }
        ]
    }
}
```

**HTTP 200 OK — A link that has never synced**

```json
{
    "status": "success",
    "summary": "Get linked workspace sync details",
    "data": {
        "workspaces": [
            {
                "sandboxId": "137687000012345003",
                "workspaceId": "466206000000081010",
                "workspaceName": "Contoso Sandbox",
                "lastSync": {
                    "syncTime": "0",
                    "syncStatus": "inProgress",
                    "syncedBy": "john.roe@example.com",
                    "syncedByName": "John Roe",
                    "syncedByZuId": "60002000000000456",
                    "entities": {
                        "dataSources": [],
                        "tables": [],
                        "views": []
                    }
                },
                "hasPendingEntities": false,
                "pendingEntities": {
                    "dataSources": [],
                    "tables": [],
                    "views": []
                }
            }
        ]
    }
}
```

**HTTP 400 Bad Request — Failure paired with Case 3**

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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Linked Workspace Sync Details](../../../sdk-examples/workspace-management/linked-workspaces/get-linked-workspace-sync-details.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **The only entity-level view of a sync** | The listing APIs report a single `syncStatus` per link; this is where you find out which table or report failed, and why. |
| **`syncTime` is epoch milliseconds, not a formatted date** | A string of digits; `"0"` when the link has never synced. Format it client-side. |
| **`lastSync.entities` reflects stored state, not a live check** | It is read from the sync state recorded by the last run. A link that has never synced returns three empty arrays, not an error. |
| **`pendingEntities.dataSources` is always empty** | The pending calculation covers tables and reports only. Do not infer "no data source changes" from it. |
| **Pending counts include deletions** | `hasPendingEntities` is driven by created, modified **and** deleted master entities, so it can be `true` purely because something was removed from the master. The `deleted` value of `modifiedStatus` marks those. |
| **The entity shape differs from the compatibility API** | Here, entries carry `viewType` / `viewTypeId` and data sources carry no `datasourceId`. There, it is the other way round. Two structures, two shapes — map them separately. |
| **Omitting `CONFIG` is the way to ask for everything** | Sending `CONFIG={}` fails the template's required-key check; omit the parameter instead. |
| **One remote read per sandbox** | Details are fetched per link, so a master with many clients makes a correspondingly larger request. Filter with `sandboxIds` when you only need a few. |
| **No paging, filtering or sorting** | Beyond `sandboxIds`, there are no query options. |
| **CONFIG travels in the query string** | This is a `GET`; send `CONFIG` as a URL-encoded query parameter, not as a body. No `Content-Type` header is needed. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md) → `sandboxId` → Get Linked Workspace Sync Details; after [Sync Linked Workspaces](sync-linked-workspaces.md), poll here for the outcome. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — The master workspace was not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an organisation administrator of the header organisation or of the master's organisation, or the request arrived through a Client Portal / White Label domain. | Authenticate as an organisation administrator and call from the standard API host. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use the standard API host. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — `CONFIG` was sent but is not a parseable JSON object. | Send a valid, URL-encoded JSON object, or omit `CONFIG` entirely. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| [8248](../../../foundations/error-codes.md#error-8248) | 400 | `SANDBOX_NOT_MAPPED_TO_MASTER_WORKSPACE` — One or more `sandboxIds` are not linked to this master. The message names them. | Use sandbox IDs from [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md). |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` was sent without `sandboxIds`, or with more than 100 entries. | Omit `CONFIG` to fetch everything, or send 1–100 sandbox IDs. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Linked Workspaces overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Linked Workspaces For Organization](get-linked-workspaces-for-organization.md), [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md), [Get Linkable Workspaces](get-linkable-workspaces.md), [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md), [Link Workspaces](link-workspaces.md), [Sync Linked Workspaces](sync-linked-workspaces.md), [Unlink Workspaces](unlink-workspaces.md).
- [SDK examples](../../../sdk-examples/workspace-management/linked-workspaces/get-linked-workspace-sync-details.md).
