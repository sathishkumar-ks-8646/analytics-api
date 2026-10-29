---
type: API Endpoint
title: Get Linked Workspaces For Organization
description: "Returns every master↔client link in the organisation named by ZANALYTICS-ORGID, grouped one entry per master workspace."
resource: https://analyticsapi.zoho.com/restapi/v2/linkedworkspaces
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - linked-workspaces
  - get
  - metadata
api:
  operation_id: getLinkedWorkspacesForOrganization
  method: GET
  path: "/restapi/v2/linkedworkspaces"
  domain: workspace-management
  group: linked-workspaces
  api_units:
    api_id: 3086
    action: GET_LINKED_WORKSPACES_FOR_ORGANIZATION
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
  permission_required: The authenticated user must be an Account Admin or an Organization Admin of the organisation in ZANALYTICS-ORGID. Individual links are additionally filtered to those whose master and client organisations the caller administers.
  error_codes:
    - 7301
    - 8060
    - 8083
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1linkedworkspaces/get"
    config_schema: null
    response_schema: GetLinkedWorkspacesForOrganizationResponse
  sdk_examples: "/sdk-examples/workspace-management/linked-workspaces/get-linked-workspaces-for-organization.md"
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

**GET `/restapi/v2/linkedworkspaces`** - Get Linked Workspaces For Organization (Linked Workspaces / Workspace Management).

Returns every master↔client link in the organisation named by `ZANALYTICS-ORGID`, grouped one entry per master workspace. This is the broadest discovery call, and the usual way to find a `sandboxId`.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getLinkedWorkspacesForOrganization` |
| HTTP method | GET |
| URL | `/restapi/v2/linkedworkspaces` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID whose master workspaces are listed. |
| Permission required | The authenticated user must be an Account Admin or an Organization Admin of the organisation in ZANALYTICS-ORGID. Individual links are additionally filtered to those whose master and client organisations the caller administers. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| API units | 1 unit per request - action `GET_LINKED_WORKSPACES_FOR_ORGANIZATION` (api-id `3086`), **METADATA** category. See [API units](../../../foundations/api-units.md). |
| Frequency limit | 60 requests/minute across all **METADATA**-category calls of the organization. See [API units](../../../foundations/api-units.md#unit-categories-and-frequency-limits). |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1linkedworkspaces/get`; response schema `GetLinkedWorkspacesForOrganizationResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID, shown in the Zoho Analytics UI under Settings > Organisation. See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

This endpoint has no path parameters.

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary — `"Get linked workspaces for organization"` for this API. Never branch on it. |
| `data` | JSONObject | Response payload wrapper. |
| `data.linkedWorkspaces` | JSONArray | One entry per master workspace that has at least one live link. **Always present**; `[]` when the organisation has no links, or when every link was filtered out by the permission check. A master with no clients never appears. |
| `linkedWorkspaces[].master` | JSONObject | The master workspace of this group. **Always present.** |
| `master.workspaceId` | String | Master workspace ID, serialised as a **string**. |
| `master.workspaceName` | String | Master workspace display name. This is also the grouping key — see [Limitations](overview.md#limitations). |
| `master.orgId` | String | Organisation ID that owns the master. |
| `master.orgName` | String | Organisation display name. On an on-premise build this is the calling user's full name rather than an organisation name. |
| `linkedWorkspaces[].clients` | JSONArray | The master's clients, grouped by client organisation, in the order the links were read. **Always present** and never empty within an entry. |
| `clients[].orgId` | String | Client organisation ID. |
| `clients[].orgName` | String | Client organisation display name. |
| `clients[].workspaces` | JSONArray | The linked client workspaces inside that organisation. |
| `workspaces[].workspaceId` | String | Client workspace ID. |
| `workspaces[].workspaceName` | String | Client workspace display name. |
| `workspaces[].sandboxId` | String | **The link's identifier.** Use it for [Unlink Workspaces](unlink-workspaces.md), [Sync Linked Workspaces](sync-linked-workspaces.md) and [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md). |
| `workspaces[].lastSync` | JSONObject | Summary of the most recent successful sync. **Always present**, with empty-ish members when the link has never synced. |
| `lastSync.syncTime` | String | Time of the last successful sync as **epoch milliseconds in a string** (`"1779226560981"`). `"0"` when the link has never synced. Not a formatted date. |
| `lastSync.syncStatus` | String | Outcome of the last sync as a stable enum — `success`, `failure`, `partialSuccess`, `inProgress` or `unknown`. See [Sync Status Values](overview.md#sync-status-values). |
| `lastSync.syncedBy` | String | E-mail address of the user who ran that sync. |
| `lastSync.syncedByName` | String | Display name of that user. |
| `lastSync.syncedByZuId` | String | ZUID of that user, serialised as a string. |
| `workspaces[].hasPendingEntities` | Boolean | `true` when the master has entities created, modified or deleted since the last successful sync to this client. Native JSON boolean. The detail behind it is in [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md). |

# Examples

## Sample Requests

**Case 1 — List every link in the organisation**

```http
GET /restapi/v2/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
GET /restapi/v2/linkedworkspaces HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK — One master with two clients in a single client organisation**

```json
{
    "status": "success",
    "summary": "Get linked workspaces for organization",
    "data": {
        "linkedWorkspaces": [
            {
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
                                    "syncStatus": "success",
                                    "syncedBy": "jane.doe@example.com",
                                    "syncedByName": "Jane Doe",
                                    "syncedByZuId": "60002000000000123"
                                },
                                "hasPendingEntities": false
                            },
                            {
                                "workspaceId": "466206000000071010",
                                "workspaceName": "Northwind EU Sandbox",
                                "sandboxId": "137687000012345002",
                                "lastSync": {
                                    "syncTime": "1779140160981",
                                    "syncStatus": "partialSuccess",
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
        ]
    }
}
```

**HTTP 200 OK — Organisation with no linked workspaces**

```json
{
    "status": "success",
    "summary": "Get linked workspaces for organization",
    "data": {
        "linkedWorkspaces": []
    }
}
```

**HTTP 403 Forbidden — Failure paired with Case 2**

```json
{
    "status": "failure",
    "summary": "SECURITY_NOT_PERMITTED",
    "data": {
        "errorCode": 7301,
        "errorMessage": "You (WL_DBAdmin) do not have the permission to do this operation. "
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Linked Workspaces For Organization](../../../sdk-examples/workspace-management/linked-workspaces/get-linked-workspaces-for-organization.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Scoped to the header organisation** | Only masters owned by the organisation in `ZANALYTICS-ORGID` are listed. To see another organisation's masters, repeat the call with its ID in the header. |
| **Results are filtered, not refused** | A link whose master or client organisation the caller does not administer is silently dropped from the response. An empty array can therefore mean "no links" or "none you may see". |
| **Reading has a housekeeping side effect** | Mappings whose master or client workspace is no longer active are **deleted** while the response is being built. A `GET` here can permanently remove dangling links — benign, but it means the same call can return fewer entries the second time. |
| **Grouped by master workspace name** | The grouping key is the display name, not the ID. See [Limitations](overview.md#limitations). |
| **No paging, filtering or sorting** | The whole set comes back in one response; there is no `pageNo`, keyword or status filter anywhere in this family. |
| **Empty result is a success** | An organisation with no links returns `200` with `"linkedWorkspaces": []`, not an error. |
| **Ids are strings** | Parse `workspaceId`, `orgId`, `sandboxId` and `syncedByZuId` as strings or 64-bit longs. A 32-bit integer type loses precision. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | Organization ID (Zoho Analytics UI → **Settings → Organisation**) → `ZANALYTICS-ORGID` → Get Linked Workspaces For Organization → `sandboxId` for the sync and unlink APIs. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin of the organisation in `ZANALYTICS-ORGID`, or the request arrived through a Client Portal / White Label domain. | Authenticate as an organisation administrator and call from the standard API host. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use the standard API host. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Linked Workspaces overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md), [Get Linkable Workspaces](get-linkable-workspaces.md), [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md), [Link Workspaces](link-workspaces.md), [Sync Linked Workspaces](sync-linked-workspaces.md), [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md), [Unlink Workspaces](unlink-workspaces.md).
- [SDK examples](../../../sdk-examples/workspace-management/linked-workspaces/get-linked-workspaces-for-organization.md).
- [API units](../../../foundations/api-units.md) - unit cost, unit categories and frequency limits for every endpoint.
