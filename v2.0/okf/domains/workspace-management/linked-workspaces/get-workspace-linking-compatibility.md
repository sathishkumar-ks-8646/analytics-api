---
type: API Endpoint
title: Get Workspace Linking Compatibility
description: "Runs the full linking validation against a set of candidate client workspaces without linking anything, and returns a per-workspace verdict with the conflicting entities broken out."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/compatibility"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - linked-workspaces
  - get
  - metadata
api:
  operation_id: getWorkspaceLinkingCompatibility
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/compatibility"
  domain: workspace-management
  group: linked-workspaces
  api_units:
    api_id: 3089
    action: GET_WORKSPACE_LINKING_COMPATIBILITY
    category: METADATA
    units: 1
    units_basis: per_request
    units_note: "1 unit per request"
    category_frequency_limit: 60 requests/minute
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: query
    required: true
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or an Organization Admin of the organisation in ZANALYTICS-ORGID, of the organisation that owns <workspace-id>, and of every organisation named in clients[].orgId."
  error_codes:
    - 7103
    - 7301
    - 7387
    - 8060
    - 8077
    - 8080
    - 8083
    - 8246
    - 8504
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1linkedworkspaces~1compatibility/get"
    config_schema: GetWorkspaceLinkingCompatibilityConfig
    response_schema: GetWorkspaceLinkingCompatibilityResponse
  sdk_examples: "/sdk-examples/workspace-management/linked-workspaces/get-workspace-linking-compatibility.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/compatibility`** - Get Workspace Linking Compatibility (Linked Workspaces / Workspace Management).

Runs the full linking validation against a set of candidate client workspaces **without linking anything**, and returns a per-workspace verdict with the conflicting entities broken out. [Link Workspaces](link-workspaces.md) runs exactly this check internally and refuses the whole request if any candidate fails, so calling this first is how you avoid an all-or-nothing rejection.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getWorkspaceLinkingCompatibility` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/compatibility` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the master workspace. |
| Permission required | The authenticated user must be an Account Admin or an Organization Admin of the organisation in ZANALYTICS-ORGID, of the organisation that owns <workspace-id>, and of every organisation named in clients[].orgId. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - **mandatory** |
| Success response | HTTP 200 - `application/json` |
| API units | 1 unit per request - action `GET_WORKSPACE_LINKING_COMPATIBILITY` (api-id `3089`), **METADATA** category. See [API units](../../../foundations/api-units.md). |
| Frequency limit | 60 requests/minute across all **METADATA**-category calls of the organization. See [API units](../../../foundations/api-units.md#unit-categories-and-frequency-limits). |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1linkedworkspaces~1compatibility/get`; CONFIG schema `GetWorkspaceLinkingCompatibilityConfig`; response schema `GetWorkspaceLinkingCompatibilityResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID, shown in the Zoho Analytics UI under Settings > Organisation. See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | The ID of the workspace. It can be obtained using any of the workspace list APIs. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

CONFIG is **mandatory** for this API and is sent as a query parameter.

| Parameter | Type | Mandatory | Default | Max Length | Description |
|-----------|------|-----------|---------|------------|-------------|
| `clients` | JSONArray of JSONObject | **Yes** | — | 500000 | Candidate client workspaces, grouped by the organisation that owns them. **1–100** entries. An absent or non-array `clients` is `8077`. See [`clients` Fields](#clients-fields). |

### `clients` Fields

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `orgId` | Long | **Yes** | — | 20 | Organisation that owns the listed workspaces, as a JSON **number**. The caller must administer it (`7301`). |
| `workspaceIds` | JSONArray of String | **Yes** | — | 5000 | Client workspace IDs to validate, as numeric **strings**, **1–100** entries. Every ID must belong to `orgId` (`7387`). Duplicates across organisation entries are de-duplicated before validation. |

> **`orgId` is a number, `workspaceIds` entries are strings.** The request template declares `orgId` as a long and each `workspaceIds` entry as text, so the samples below quote the workspace IDs and leave `orgId` unquoted. See [General Response Payload Notes](overview.md#general-response-payload-notes).

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. A workspace being incompatible is **not** a failure — the envelope is still `success`. |
| `summary` | String | `"Get workspace linking compatibility"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.clients` | JSONArray | One entry per organisation in the request, in request order. **Always present.** |
| `clients[].orgId` | String | Organisation ID, echoed from the request but serialised as a **string**. |
| `clients[].orgName` | String | Organisation display name, resolved server-side. |
| `clients[].workspaces` | JSONArray | One report per workspace in that organisation's `workspaceIds`, in request order. A workspace the validator could not evaluate at all is **omitted**, so this array can be shorter than what you sent. |
| `workspaces[].workspaceId` | String | The candidate workspace. |
| `workspaces[].workspaceName` | String | Its display name. |
| `workspaces[].isCompatible` | Boolean | `true` when the workspace can be linked as-is. **This is the field [Link Workspaces](link-workspaces.md) gates on.** |
| `workspaces[].error` | String | `null` when compatible. Otherwise either a workspace-level reason (already linked, unsupported configuration, …) or the fixed string `"Some entities have conflicts"` when the detail is in `entities`. |
| `workspaces[].entities` | JSONObject | The per-entity breakdown — **`null`** when the workspace was blocked for a workspace-level reason with no entity detail. Always a populated object otherwise, including for compatible workspaces, where its three arrays are empty. |
| `entities.dataSources` | JSONArray | Conflicting or noteworthy data sources. |
| `dataSources[].datasourceId` | String | Data source ID. **Present here but absent from the same structure in [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md).** |
| `dataSources[].datasourceName` | String | Data source name. |
| `dataSources[].status` | String | Per-entity verdict — `success`, `warning` or `failure`. See [Entity Status Values](overview.md#entity-status-values). |
| `dataSources[].message` | String | Human-readable reason. `"Compatible"` when the underlying reason is the no-conflict sentinel. Always rendered in **English**, regardless of the caller's locale. |
| `entities.tables` | JSONArray | Conflicting or noteworthy tables. |
| `entities.views` | JSONArray | Conflicting or noteworthy reports. |
| `tables[].viewId` / `views[].viewId` | String | Entity ID in the **master** workspace. |
| `tables[].viewName` / `views[].viewName` | String | Entity name. |
| `tables[].status` / `views[].status` | String | Per-entity verdict — `success`, `warning` or `failure`. |
| `tables[].message` / `views[].message` | String | Human-readable reason, in English. |

> Unlike the entity lists of [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md), the entries here carry **no** `viewType` or `viewTypeId`.

# Examples

## Sample Requests

**Case 1 — Check one candidate workspace**

```http
GET /restapi/v2/workspaces/137687000271334001/linkedworkspaces/compatibility?CONFIG={"clients":[{"orgId":700000654321,"workspaceIds":["466206000000071000"]}]} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Check several workspaces across two organisations**

```http
GET /restapi/v2/workspaces/137687000271334001/linkedworkspaces/compatibility?CONFIG={"clients":[{"orgId":700000654321,"workspaceIds":["466206000000071000","466206000000071010"]},{"orgId":700000999999,"workspaceIds":["466206000000081010"]}]} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — The master workspace is itself a client of another master (rejected)**

```http
GET /restapi/v2/workspaces/466206000000071000/linkedworkspaces/compatibility?CONFIG={"clients":[{"orgId":700000654321,"workspaceIds":["466206000000071010"]}]} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — One compatible workspace and one with entity conflicts**

```json
{
    "status": "success",
    "summary": "Get workspace linking compatibility",
    "data": {
        "clients": [
            {
                "orgId": "700000654321",
                "orgName": "Northwind Retail",
                "workspaces": [
                    {
                        "workspaceId": "466206000000071000",
                        "workspaceName": "Northwind Sandbox",
                        "isCompatible": true,
                        "error": null,
                        "entities": {
                            "dataSources": [],
                            "tables": [],
                            "views": []
                        }
                    },
                    {
                        "workspaceId": "466206000000071010",
                        "workspaceName": "Northwind EU Sandbox",
                        "isCompatible": false,
                        "error": "Some entities have conflicts",
                        "entities": {
                            "dataSources": [
                                {
                                    "datasourceId": "466206000000095001",
                                    "datasourceName": "Books Connection",
                                    "status": "failure",
                                    "message": "Connection configuration differs"
                                }
                            ],
                            "tables": [
                                {
                                    "viewId": "137687000006991601",
                                    "viewName": "Sales_Fact",
                                    "status": "warning",
                                    "message": "Column structure differs"
                                }
                            ],
                            "views": [
                                {
                                    "viewId": "466206000000105001",
                                    "viewName": "Revenue by Region",
                                    "status": "failure",
                                    "message": "Formula column missing in client workspace"
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }
}
```

**HTTP 200 OK — A workspace blocked for a workspace-level reason: `entities` is null**

```json
{
    "status": "success",
    "summary": "Get workspace linking compatibility",
    "data": {
        "clients": [
            {
                "orgId": "700000999999",
                "orgName": "Contoso Distribution",
                "workspaces": [
                    {
                        "workspaceId": "466206000000081010",
                        "workspaceName": "Contoso Sandbox",
                        "isCompatible": false,
                        "error": "This workspace is already linked to another master workspace.",
                        "entities": null
                    }
                ]
            }
        ]
    }
}
```

**HTTP 400 Bad Request — Failure paired with Case 3**

```json
{
    "status": "failure",
    "summary": "INVALID_MASTER_WORKSPACE_MAPPING",
    "data": {
        "errorCode": 8246,
        "errorMessage": "The provided master workspace is already mapped to another workspace."
    }
}
```

**HTTP 400 Bad Request — `clients` missing from CONFIG**

```json
{
    "status": "failure",
    "summary": "EMPTY_JSON_CONFIGURATION",
    "data": {
        "errorCode": 8077,
        "errorMessage": "Empty JSON configuration. Kindly provide a valid JSON configuration."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Workspace Linking Compatibility](../../../sdk-examples/workspace-management/linked-workspaces/get-workspace-linking-compatibility.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **It is a dry run and changes nothing** | No link, no schedule, no state. Safe to call as often as you like. |
| **Incompatibility is a `200`, not an error** | Only request-level problems produce a failure envelope. Branch on `isCompatible`, never on the HTTP status. |
| **`entities` is `null` for workspace-level blocks** | When `error` carries a reason and there is no entity detail, `entities` is JSON `null` rather than an object with empty arrays. Guard before indexing into it. |
| **`error` is `null` when compatible** | The three states are: compatible (`error: null`), blocked at workspace level (`error` = reason, `entities: null`), blocked by entity conflicts (`error` = `"Some entities have conflicts"`, `entities` populated). |
| **Messages are always English** | Per-entity `message` values are resolved through a fixed `en-US` bundle, so they do not follow the caller's language. Do not parse them; use `status`. |
| **A `warning` does not block linking** | `isCompatible` is computed from the workspace-level verdict, so a workspace can be compatible while individual entities report `warning`. |
| **Workspaces may be missing from the response** | A candidate the validator could not evaluate produces no report rather than a failed one. Match the response back to your request by `workspaceId` instead of by position. |
| **It is validated per workspace, not per batch** | Each candidate is evaluated independently against the master, so adding a bad workspace to the list does not change the verdict of the others. |
| **CONFIG travels in the query string** | This is a `GET`; send `CONFIG` as a URL-encoded query parameter, not as a body. No `Content-Type` header is needed. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get Linkable Workspaces](get-linkable-workspaces.md) → `orgs[].orgId` + `workspaces[].workspaceId` → Get Workspace Linking Compatibility → confirm `isCompatible` → [Link Workspaces](link-workspaces.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — The master workspace or one of the candidate workspaces was not found. | Verify `<workspace-id>` and every `clients[].workspaceIds` entry. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller does not administer the header organisation, the master's organisation, or one of the organisations named in `clients[].orgId`; or the request arrived through a Client Portal / White Label domain. | Authenticate as an administrator of every organisation in the payload, from the standard API host. |
| [7387](../../../foundations/error-codes.md#error-7387) | 400 | `DBID_NOT_BELONGS_TO_ZSOID` — One or more `workspaceIds` do not belong to the `orgId` they were listed under. | Group each workspace under the organisation that actually owns it, as reported by [Get Linkable Workspaces](get-linkable-workspaces.md). |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use the standard API host. |
| [8077](../../../foundations/error-codes.md#error-8077) | 400 | `EMPTY_JSON_CONFIGURATION` — `CONFIG` carries no `clients` array. | Send `{"clients":[{"orgId":…,"workspaceIds":[…]}]}`. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — `CONFIG` is not parseable JSON. | Send a valid, URL-encoded JSON object. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| [8246](../../../foundations/error-codes.md#error-8246) | 400 | `INVALID_MASTER_WORKSPACE_MAPPING` — `<workspace-id>` is itself linked as a client of another master. | Use a workspace that is not already a client; a workspace cannot be both. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — The `CONFIG` parameter was not sent, or `clients` is outside its 1–100 bound. | Send `CONFIG` with between 1 and 100 organisation entries. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Linked Workspaces overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Linked Workspaces For Organization](get-linked-workspaces-for-organization.md), [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md), [Get Linkable Workspaces](get-linkable-workspaces.md), [Link Workspaces](link-workspaces.md), [Sync Linked Workspaces](sync-linked-workspaces.md), [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md), [Unlink Workspaces](unlink-workspaces.md).
- [SDK examples](../../../sdk-examples/workspace-management/linked-workspaces/get-workspace-linking-compatibility.md).
- [API units](../../../foundations/api-units.md) - unit cost, unit categories and frequency limits for every endpoint.
