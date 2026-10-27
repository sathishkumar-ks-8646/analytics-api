---
type: API Endpoint
title: Link Workspaces
description: Links one or more client workspaces to a master.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/linkedworkspaces"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - linked-workspaces
  - post
  - modeling
api:
  operation_id: linkWorkspaces
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/linkedworkspaces"
  domain: workspace-management
  group: linked-workspaces
  oauth_scopes:
    - ZohoAnalytics.modeling.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
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
    - 8247
    - 8504
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1linkedworkspaces/post"
    config_schema: LinkWorkspacesConfig
    response_schema: null
  sdk_examples: "/sdk-examples/workspace-management/linked-workspaces/link-workspaces.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces`** - Link Workspaces (Linked Workspaces / Workspace Management).

Links one or more client workspaces to a master. The request is validated for compatibility first and, if every candidate passes, the initial design push is **scheduled**. Candidates already linked to this master are skipped silently.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `linkWorkspaces` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the master workspace. |
| Permission required | The authenticated user must be an Account Admin or an Organization Admin of the organisation in ZANALYTICS-ORGID, of the organisation that owns <workspace-id>, and of every organisation named in clients[].orgId. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1linkedworkspaces/post`; CONFIG schema `LinkWorkspacesConfig` |

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
| `clients` | JSONArray of JSONObject | **Yes** | — | 500000 | Client workspaces to link, grouped by the organisation that owns them. **1–100** entries. Identical in shape to the attribute of [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md) — see [`clients` Fields](get-workspace-linking-compatibility.md#clients-fields). |

> **Already-linked candidates are removed before validation, not rejected.** Any `workspaceIds` entry already linked to this master is filtered out; if that empties the whole payload the call returns `204` having done nothing. A `204` is therefore not proof that anything was linked.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`), plus `data.incompatibleWorkspaces` on [`8247`](../../../foundations/error-codes.md#error-8247).

# Examples

## Sample Requests

**Case 1 — Link one client workspace**

```http
POST /restapi/v2/workspaces/137687000271334001/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "clients": [
        {
            "orgId": 700000654321,
            "workspaceIds": ["466206000000071000"]
        }
    ]
}
```

**Case 2 — Link several workspaces across two client organisations**

```http
POST /restapi/v2/workspaces/137687000271334001/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "clients": [
        {
            "orgId": 700000654321,
            "workspaceIds": ["466206000000071000", "466206000000071010"]
        },
        {
            "orgId": 700000999999,
            "workspaceIds": ["466206000000081010"]
        }
    ]
}
```

**Case 3 — One candidate is incompatible, so the whole request is refused (rejected)**

```http
POST /restapi/v2/workspaces/137687000271334001/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "clients": [
        {
            "orgId": 700000654321,
            "workspaceIds": ["466206000000071000", "466206000000071010"]
        }
    ]
}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. It means the link was validated and **scheduled**, not that it has completed.

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — Failure paired with Case 3**

The failure payload carries the full compatibility report for the workspaces that blocked the request, under `data.incompatibleWorkspaces`.

```json
{
    "status": "failure",
    "summary": "LINK_WORKSPACES_INCOMPATIBLE_WORKSPACES",
    "data": {
        "errorCode": 8247,
        "errorMessage": "Workspace linking cannot proceed because the following workspaces are incompatible: Northwind EU Sandbox",
        "incompatibleWorkspaces": [
            {
                "orgId": "700000654321",
                "orgName": "Northwind Retail",
                "workspaces": [
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
                            "tables": [],
                            "views": []
                        }
                    }
                ]
            }
        ]
    }
}
```

**HTTP 400 Bad Request — The master is itself a client of another master**

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

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Link Workspaces](../../../sdk-examples/workspace-management/linked-workspaces/link-workspaces.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`204` means scheduled, not linked** | The compatibility check runs inline, but the design push is handed to a scheduler. The sandbox IDs do not exist yet when the response arrives — poll [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md) until they appear. |
| **All-or-nothing on compatibility** | If any surviving candidate is incompatible, **nothing** is linked and the response carries every blocking workspace in `data.incompatibleWorkspaces` (`8247`). Run [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md) first to avoid the round trip. |
| **Idempotent in effect** | Re-sending the same payload filters out the now-linked workspaces and returns `204` having done nothing. There is no duplicate-link error. |
| **A `204` can mean "nothing happened"** | Because already-linked candidates are filtered before anything else runs, a payload consisting entirely of existing links short-circuits to `204` — **without** validating the master, the candidate organisations, or the caller's rights over them. Confirm the end state with a listing call. |
| **Duplicate workspace IDs collapse** | IDs repeated within or across `clients[]` entries are de-duplicated before linking. |
| **The link is one-directional** | The master pushes to the client. Nothing flows back, and a client cannot become a master while it is linked (`8246`). |
| **No `sandboxId` is returned** | The identifier every other API needs is only discoverable through [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md). |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get Linkable Workspaces](get-linkable-workspaces.md) → [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md) → Link Workspaces → [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md) → `sandboxId`. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — The master workspace or one of the candidate workspaces was not found. | Verify `<workspace-id>` and every `clients[].workspaceIds` entry. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller does not administer the header organisation, the master's organisation, or one of the organisations named in `clients[].orgId`; or the request arrived through a Client Portal / White Label domain. | Authenticate as an administrator of every organisation in the payload, from the standard API host. |
| [7387](../../../foundations/error-codes.md#error-7387) | 400 | `DBID_NOT_BELONGS_TO_ZSOID` — One or more `workspaceIds` do not belong to the `orgId` they were listed under. | Group each workspace under the organisation that owns it. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use the standard API host. |
| [8077](../../../foundations/error-codes.md#error-8077) | 400 | `EMPTY_JSON_CONFIGURATION` — `CONFIG` carries no `clients` array. | Send `{"clients":[{"orgId":…,"workspaceIds":[…]}]}`. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — `CONFIG` is not parseable JSON. | Send a valid, URL-encoded JSON object. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| [8246](../../../foundations/error-codes.md#error-8246) | 400 | `INVALID_MASTER_WORKSPACE_MAPPING` — `<workspace-id>` is itself linked as a client of another master. | Use a workspace that is not already a client. |
| [8247](../../../foundations/error-codes.md#error-8247) | 400 | `LINK_WORKSPACES_INCOMPATIBLE_WORKSPACES` — At least one candidate failed the compatibility check. Nothing was linked. | Read `data.incompatibleWorkspaces`, resolve the conflicts or drop those workspaces, and resend. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — The `CONFIG` parameter was not sent, or `clients` is outside its 1–100 bound. | Send `CONFIG` with between 1 and 100 organisation entries. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |

# Related

- [Linked Workspaces overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Linked Workspaces For Organization](get-linked-workspaces-for-organization.md), [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md), [Get Linkable Workspaces](get-linkable-workspaces.md), [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md), [Sync Linked Workspaces](sync-linked-workspaces.md), [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md), [Unlink Workspaces](unlink-workspaces.md).
- [SDK examples](../../../sdk-examples/workspace-management/linked-workspaces/link-workspaces.md).
