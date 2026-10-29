---
type: API Endpoint
title: Get Linked Workspaces For Master Workspace
description: "Returns the links of a single master workspace, in the same shape as one entry of Get Linked Workspaces For Organization - but as a single object, not an array."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/linkedworkspaces"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - linked-workspaces
  - get
  - metadata
api:
  operation_id: getLinkedWorkspacesForMasterWorkspace
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/linkedworkspaces"
  domain: workspace-management
  group: linked-workspaces
  api_units:
    api_id: 3087
    action: GET_LINKED_WORKSPACES_FOR_MASTER_WORKSPACE
    category: METADATA
    units: 1
    units_basis: per_request
    units_note: "1 unit per request"
    category_frequency_limit: 60 requests/minute
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or an Organization Admin of the organisation in ZANALYTICS-ORGID and of the organisation that owns <workspace-id>. Individual client entries are further filtered to organisations the caller administers."
  error_codes:
    - 7103
    - 7301
    - 8060
    - 8083
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1linkedworkspaces/get"
    config_schema: null
    response_schema: GetLinkedWorkspacesForMasterWorkspaceResponse
  sdk_examples: "/sdk-examples/workspace-management/linked-workspaces/get-linked-workspaces-for-master-workspace.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces`** - Get Linked Workspaces For Master Workspace (Linked Workspaces / Workspace Management).

Returns the links of a single master workspace, in the same shape as one entry of [Get Linked Workspaces For Organization](get-linked-workspaces-for-organization.md) — but as a **single object**, not an array.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getLinkedWorkspacesForMasterWorkspace` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the master workspace. |
| Permission required | The authenticated user must be an Account Admin or an Organization Admin of the organisation in ZANALYTICS-ORGID and of the organisation that owns <workspace-id>. Individual client entries are further filtered to organisations the caller administers. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| API units | 1 unit per request - action `GET_LINKED_WORKSPACES_FOR_MASTER_WORKSPACE` (api-id `3087`), **METADATA** category. See [API units](../../../foundations/api-units.md). |
| Frequency limit | 60 requests/minute across all **METADATA**-category calls of the organization. See [API units](../../../foundations/api-units.md#unit-categories-and-frequency-limits). |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1linkedworkspaces/get`; response schema `GetLinkedWorkspacesForMasterWorkspaceResponse` |

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

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

The `master` / `clients` structure is identical to one element of `data.linkedWorkspaces` in [Get Linked Workspaces For Organization](get-linked-workspaces-for-organization.md) — refer there for every nested field. The differences are:

| Field | Type | Description |
|-------|------|--------------|
| `summary` | String | `"Get linked workspaces for master workspace"` for this API. |
| `data.linkedWorkspaces` | JSONObject | A **single object**, not an array. **Always present**, but an **empty object `{}`** when the master has no links the caller may see. Test for the presence of `master` rather than for an empty array. |

# Examples

## Sample Requests

**Case 1 — A master with links**

```http
GET /restapi/v2/workspaces/137687000271334001/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — A workspace that has never been linked**

```http
GET /restapi/v2/workspaces/466206000000071000/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — Two client workspaces across two client organisations**

```json
{
    "status": "success",
    "summary": "Get linked workspaces for master workspace",
    "data": {
        "linkedWorkspaces": {
            "master": {
                "workspaceId": "137687000271334001",
                "workspaceName": "ISV Master Analytics",
                "orgId": "700000123456",
                "orgName": "Zylker Analytics"
            },
            "clients": [
                {
                    "orgId": "700000654321",
                    "orgName": "Northwind Retail",
                    "workspaces": [
                        {
                            "workspaceId": "466206000000071000",
                            "workspaceName": "Northwind Sandbox",
                            "sandboxId": "137687000012345001",
                            "lastSync": {
                                "syncTime": "1779226560981",
                                "syncStatus": "partialSuccess",
                                "syncedBy": "jane.doe@example.com",
                                "syncedByName": "Jane Doe",
                                "syncedByZuId": "60002000000000123"
                            },
                            "hasPendingEntities": true
                        }
                    ]
                },
                {
                    "orgId": "700000999999",
                    "orgName": "Contoso Distribution",
                    "workspaces": [
                        {
                            "workspaceId": "466206000000081010",
                            "workspaceName": "Contoso Sandbox",
                            "sandboxId": "137687000012345003",
                            "lastSync": {
                                "syncTime": "0",
                                "syncStatus": "inProgress",
                                "syncedBy": "john.roe@example.com",
                                "syncedByName": "John Roe",
                                "syncedByZuId": "60002000000000456"
                            },
                            "hasPendingEntities": true
                        }
                    ]
                }
            ]
        }
    }
}
```

**HTTP 200 OK — Failure paired with Case 2: the workspace has no links**

```json
{
    "status": "success",
    "summary": "Get linked workspaces for master workspace",
    "data": {
        "linkedWorkspaces": {}
    }
}
```

**HTTP 403 Forbidden — Caller does not administer the master's organisation**

```json
{
    "status": "failure",
    "summary": "SECURITY_NOT_PERMITTED",
    "data": {
        "errorCode": 7301,
        "errorMessage": "You (Jane Doe) do not have the permission to do this operation. "
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Linked Workspaces For Master Workspace](../../../sdk-examples/workspace-management/linked-workspaces/get-linked-workspaces-for-master-workspace.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **The container type differs from the organisation listing** | `data.linkedWorkspaces` is a JSON **object** here and a JSON **array** in [Get Linked Workspaces For Organization](get-linked-workspaces-for-organization.md). A client that shares a parser between the two must branch on the shape. |
| **"No links" is `{}`, not an error** | An unlinked workspace, a workspace whose links were all filtered out by the permission check, and a workspace that is not a master at all are indistinguishable — all three return `{}` with HTTP 200. This API does **not** raise `8246` for a non-master. |
| **Results are filtered, not refused** | Client entries in organisations the caller does not administer are silently dropped, exactly as in the organisation listing. |
| **Reading has a housekeeping side effect** | Mappings pointing at deleted workspaces are purged while the response is built. |
| **`syncTime` is epoch milliseconds** | A string of digits, `"0"` when the link has never synced successfully. |
| **No paging, filtering or sorting** | The whole set comes back in one response. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get Org Workspaces](../../organization-management/org-level-listings/get-org-workspaces.md) → `<workspace-id>` → Get Linked Workspaces For Master Workspace → `clients[].workspaces[].sandboxId`. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an organisation administrator of the header organisation or of the master's organisation, or the request arrived through a Client Portal / White Label domain. | Authenticate as an organisation administrator and call from the standard API host. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use the standard API host. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Linked Workspaces overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Linked Workspaces For Organization](get-linked-workspaces-for-organization.md), [Get Linkable Workspaces](get-linkable-workspaces.md), [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md), [Link Workspaces](link-workspaces.md), [Sync Linked Workspaces](sync-linked-workspaces.md), [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md), [Unlink Workspaces](unlink-workspaces.md).
- [SDK examples](../../../sdk-examples/workspace-management/linked-workspaces/get-linked-workspaces-for-master-workspace.md).
- [API units](../../../foundations/api-units.md) - unit cost, unit categories and frequency limits for every endpoint.
