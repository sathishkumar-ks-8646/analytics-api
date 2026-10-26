---
type: API Endpoint
title: Unlink Workspaces
description: "Removes links between a master workspace and its clients, either all of them or a named set."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/linkedworkspaces"
tags:
  - zoho-analytics
  - rest-api-v2
  - workspace-management
  - linked-workspaces
  - delete
  - modeling
api:
  operation_id: unlinkWorkspaces
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/linkedworkspaces"
  domain: workspace-management
  group: linked-workspaces
  oauth_scopes:
    - ZohoAnalytics.modeling.delete
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or an Organization Admin of the organisation in ZANALYTICS-ORGID and of the organisation that owns <workspace-id>."
  error_codes:
    - 7103
    - 7301
    - 8060
    - 8078
    - 8079
    - 8080
    - 8083
    - 8119
    - 8248
    - 8249
    - 8504
    - 8535
  openapi:
    file: "/references/openapi/workspace-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1linkedworkspaces/delete"
    config_schema: UnlinkWorkspacesConfig
    response_schema: null
  sdk_examples: "/sdk-examples/workspace-management/linked-workspaces/unlink-workspaces.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces`** - Unlink Workspaces (Linked Workspaces / Workspace Management).

Removes links between a master workspace and its clients, either all of them or a named set. The client workspaces themselves survive — only the mapping, and the design relationship it carries, is removed.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `unlinkWorkspaces` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/linkedworkspaces` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingdelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the master workspace. |
| Permission required | The authenticated user must be an Account Admin or an Organization Admin of the organisation in ZANALYTICS-ORGID and of the organisation that owns <workspace-id>. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`workspace-management-grouped-api.json`](../../../references/openapi/workspace-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1linkedworkspaces/delete`; CONFIG schema `UnlinkWorkspacesConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.delete`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | The ID of the workspace. It can be obtained using any of the workspace list APIs. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

CONFIG is **mandatory** for this API, and it is sent as a form body on a `DELETE` request.

| Parameter | Type | Mandatory | Default | Max Length | Description |
|-----------|------|-----------|---------|------------|-------------|
| `scope` | String (enum) | **Yes** | — | 20 | `ALL` unlinks every client of this master; `SELECTED` unlinks the listed `sandboxIds`. **Case-sensitive — must be upper case** (`8119` otherwise). See [`scope` Values](overview.md#scope-values). |
| `sandboxIds` | JSONArray of String | Conditional | — | 5000 | Links to remove, as numeric **strings**, **1–100** entries. **Mandatory when `scope` is `SELECTED`**, and **must be omitted or empty when `scope` is `ALL`** — either mistake is `8249`. Every ID must already be mapped to `<workspace-id>` (`8248`). |

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`).

# Examples

## Sample Requests

**Case 1 — Unlink every client of the master**

```http
DELETE /restapi/v2/workspaces/137687000271334001/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scope": "ALL"
}
```

**Case 2 — Unlink two named sandboxes**

```http
DELETE /restapi/v2/workspaces/137687000271334001/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scope": "SELECTED",
    "sandboxIds": ["137687000012345001", "137687000012345002"]
}
```

**Case 3 — `scope: "SELECTED"` without `sandboxIds` (rejected)**

```http
DELETE /restapi/v2/workspaces/137687000271334001/linkedworkspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scope": "SELECTED"
}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. No per-sandbox result list is returned.

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — Failure paired with Case 3**

```json
{
    "status": "failure",
    "summary": "INVALID_CONFIGURATION_REMOVE_LINKED_WORKSPACES",
    "data": {
        "errorCode": 8249,
        "errorMessage": "Invalid configuration. Kindly provide scope as 'ALL' to remove all linked workspaces from the master workspace or scope as 'SELECTED' with valid sandboxIds."
    }
}
```

**HTTP 400 Bad Request — `scope` sent in lower case**

```json
{
    "status": "failure",
    "summary": "INVALID_VALUE_FOR_ATTRIBUTE",
    "data": {
        "errorCode": 8119,
        "errorMessage": "Invalid value 'all' provided for the attribute 'scope'. Only 'ALL, SELECTED' are allowed."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Unlink Workspaces](../../../sdk-examples/workspace-management/linked-workspaces/unlink-workspaces.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Client workspaces are not deleted** | Only the mapping is removed. The client keeps whatever design was last pushed to it, and it becomes an ordinary, independent workspace. |
| **`scope: "ALL"` on a master with no links is a no-op** | The resolved sandbox list is empty, so the call returns `204` having done nothing. It is not an error. |
| **Idempotent for `ALL`, not for `SELECTED`** | Repeating `{"scope":"ALL"}` is harmless. Repeating a `SELECTED` request with the same IDs fails with `8248`, because they are no longer mapped. |
| **Validated up front** | Every `sandboxIds` entry is checked against the master before anything is removed, so one bad ID fails the whole request and nothing is unlinked. |
| **Nothing is reported per sandbox** | "Unlinked" and "was already gone" are indistinguishable from the response. Confirm with [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md). |
| **`scope` is case-sensitive here** | Unlike the per-client `scope` of [Sync Linked Workspaces](sync-linked-workspaces.md), this one is compared verbatim. `"all"` is `8119`. |
| **Relinking starts over** | A workspace unlinked and linked again gets a **new** sandbox ID and an empty sync history. Nothing carries over. |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md) → `sandboxId` → Unlink Workspaces. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — The master workspace was not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an organisation administrator of the header organisation or of the master's organisation, or the request arrived through a Client Portal / White Label domain. | Authenticate as an organisation administrator and call from the standard API host. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use the standard API host. |
| [8078](../../../foundations/error-codes.md#error-8078) | 400 | `EMPTY_JSON_ATTRIBUTE_FOUND` — `scope` was sent with an empty value. | Send `ALL` or `SELECTED`. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — `scope` is missing from CONFIG. | Add `scope`. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — `CONFIG` is not parseable JSON. | Send a valid, URL-encoded JSON object. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE` — `scope` is not exactly `ALL` or `SELECTED`. | Send upper-case `ALL` or `SELECTED`. |
| [8248](../../../foundations/error-codes.md#error-8248) | 400 | `SANDBOX_NOT_MAPPED_TO_MASTER_WORKSPACE` — One or more `sandboxIds` are not linked to this master. The message names them. | Use sandbox IDs from [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md). |
| [8249](../../../foundations/error-codes.md#error-8249) | 400 | `INVALID_CONFIGURATION_REMOVE_LINKED_WORKSPACES` — `sandboxIds` was supplied with `scope: "ALL"`, or omitted with `scope: "SELECTED"`. | Send `{"scope":"ALL"}` or `{"scope":"SELECTED","sandboxIds":[…]}`. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — The `CONFIG` parameter was not sent, or `sandboxIds` is outside its 1–100 bound. | Send `CONFIG` as a URL-encoded form body on the `DELETE` request. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.delete`. |

# Related

- [Linked Workspaces overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Workspace Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Linked Workspaces For Organization](get-linked-workspaces-for-organization.md), [Get Linked Workspaces For Master Workspace](get-linked-workspaces-for-master-workspace.md), [Get Linkable Workspaces](get-linkable-workspaces.md), [Get Workspace Linking Compatibility](get-workspace-linking-compatibility.md), [Link Workspaces](link-workspaces.md), [Sync Linked Workspaces](sync-linked-workspaces.md), [Get Linked Workspace Sync Details](get-linked-workspace-sync-details.md).
- [SDK examples](../../../sdk-examples/workspace-management/linked-workspaces/unlink-workspaces.md).
