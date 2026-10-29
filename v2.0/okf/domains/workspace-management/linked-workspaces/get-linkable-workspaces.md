---
type: API Endpoint
title: Get Linkable Workspaces
description: "Returns, grouped by organisation, the workspaces the caller may offer as link candidates for a given master."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/linkable"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - linked-workspaces
  - get
  - metadata
api:
  operation_id: getLinkableWorkspaces
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/linkable"
  domain: workspace-management
  group: linked-workspaces
  api_units:
    api_id: 3088
    action: GET_LINKABLE_WORKSPACES
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
  permission_required: "The authenticated user must be an Account Admin or an Organization Admin of the organisation in ZANALYTICS-ORGID and of the organisation that owns <workspace-id>. Candidates are drawn only from organisations the caller administers."
  error_codes:
    - 7103
    - 7301
    - 8060
    - 8083
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1linkedworkspaces~1linkable/get"
    config_schema: null
    response_schema: GetLinkableWorkspacesResponse
  sdk_examples: "/sdk-examples/workspace-management/linked-workspaces/get-linkable-workspaces.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/linkable`** - Get Linkable Workspaces (Linked Workspaces / Workspace Management).

Returns, grouped by organisation, the workspaces the caller may offer as link candidates for a given master. **This is the only source of the `workspaceIds` that [Link Workspaces](link-workspaces.md) accepts.**

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getLinkableWorkspaces` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/linkable` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the master workspace. |
| Permission required | The authenticated user must be an Account Admin or an Organization Admin of the organisation in ZANALYTICS-ORGID and of the organisation that owns <workspace-id>. Candidates are drawn only from organisations the caller administers. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| API units | 1 unit per request - action `GET_LINKABLE_WORKSPACES` (api-id `3088`), **METADATA** category. See [API units](../../../foundations/api-units.md). |
| Frequency limit | 60 requests/minute across all **METADATA**-category calls of the organization. See [API units](../../../foundations/api-units.md#unit-categories-and-frequency-limits). |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1linkedworkspaces~1linkable/get`; response schema `GetLinkableWorkspacesResponse` |

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

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | `"Get linkable workspaces"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.orgs` | JSONArray | Candidate workspaces grouped by organisation. **Always present**; `[]` when nothing can be linked. Note the key is `orgs`, not `clients` — the compatibility and linking APIs use `clients`. |
| `orgs[].orgId` | String | Organisation ID. **Empty string** on the rare grouping where the server could not resolve an ID and returned the organisation name as the grouping key instead; `orgName` then carries that key. |
| `orgs[].orgName` | String | Organisation display name. |
| `orgs[].workspaces` | JSONArray | Workspaces inside that organisation that may be offered as link candidates. May be empty for an organisation that has none. |
| `workspaces[].workspaceId` | String | Workspace ID. This is what goes into `clients[].workspaceIds` of [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md) and [Link Workspaces](link-workspaces.md). |
| `workspaces[].workspaceName` | String | Workspace display name, for a user-facing picker. |

# Examples

## Sample Requests

**Case 1 — Discover candidates for a master**

```http
GET /restapi/v2/workspaces/137687000271334001/linkedworkspaces/linkable HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Discover candidates for a second master in the same organisation**

```http
GET /restapi/v2/workspaces/137687000271334009/linkedworkspaces/linkable HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — Candidates in two organisations**

```json
{
    "status": "success",
    "summary": "Get linkable workspaces",
    "data": {
        "orgs": [
            {
                "orgId": "700000654321",
                "orgName": "Northwind Retail",
                "workspaces": [
                    {
                        "workspaceName": "Northwind Sandbox",
                        "workspaceId": "466206000000071000"
                    },
                    {
                        "workspaceName": "Northwind EU Sandbox",
                        "workspaceId": "466206000000071010"
                    }
                ]
            },
            {
                "orgId": "700000999999",
                "orgName": "Contoso Distribution",
                "workspaces": [
                    {
                        "workspaceName": "Contoso Sandbox",
                        "workspaceId": "466206000000081010"
                    }
                ]
            }
        ]
    }
}
```

**HTTP 200 OK — No candidates available**

```json
{
    "status": "success",
    "summary": "Get linkable workspaces",
    "data": {
        "orgs": []
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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Linkable Workspaces](../../../sdk-examples/workspace-management/linked-workspaces/get-linkable-workspaces.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **The only source of link candidates** | `clients[].workspaceIds` is not validated against any other catalogue, so a workspace absent from this list may still be accepted by the write APIs and then fail compatibility. Drive the picker from here. |
| **"Linkable" means eligible, not compatible** | This API applies structural eligibility only: a workspace already acting as a client or a master, or already scheduled to be linked, is excluded. Whether its design actually fits the master is a separate question answered by [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md). |
| **The response key is `orgs`, the request key is `clients`** | You read `data.orgs[].workspaces[].workspaceId` and write `clients[].workspaceIds`. The two shapes do not mirror each other; map the fields explicitly. |
| **Candidates span organisations** | Every organisation the caller administers is searched, not just the master's own. This is what makes cross-organisation linking possible. |
| **`orgId` can be an empty string** | When the underlying grouping key is an organisation name rather than an ID, `orgId` is `""` and `orgName` holds the key. Such an entry cannot be used in `clients[].orgId`; skip it. |
| **Empty result is a success** | `"orgs": []` means nothing is eligible — commonly because every candidate is already linked. |
| **No paging, filtering or sorting** | The whole candidate set comes back in one response. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get Org Workspaces](../../organization-management/org-level-listings/get-org-workspaces.md) → `<workspace-id>` → Get Linkable Workspaces → `orgs[].orgId` + `workspaces[].workspaceId` → [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md). |

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
- Other endpoints in this group: [Get Linked Workspaces For Organization](get-linked-workspaces-for-organization.md), [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md), [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md), [Link Workspaces](link-workspaces.md), [Sync Linked Workspaces](sync-linked-workspaces.md), [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md), [Unlink Workspaces](unlink-workspaces.md).
- [SDK examples](../../../sdk-examples/workspace-management/linked-workspaces/get-linkable-workspaces.md).
- [API units](../../../foundations/api-units.md) - unit cost, unit categories and frequency limits for every endpoint.
