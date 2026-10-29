---
type: API Endpoint
title: Get Org Dashboards
description: "Returns the dashboards of one organisation that the calling user may read, across all of the workspaces the caller can see or across the workspaces named in workspaceIds."
resource: https://analyticsapi.zoho.com/restapi/v2/orgs/dashboards
tags:
  - zoho-analytics
  - rest-api-v2
  - organization-management
  - org-level-listings
  - get
  - metadata
api:
  operation_id: getOrgDashboards
  method: GET
  path: "/restapi/v2/orgs/dashboards"
  domain: organization-management
  group: org-level-listings
  api_units:
    api_id: 3044
    action: GET_ORG_DASHBOARDS
    category: METADATA
    units: 0.1
    units_basis: per_request
    units_note: "0.1 units per request"
    category_frequency_limit: 60 requests/minute
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: query
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: The authenticated user must be a member of the organisation. Only dashboards the user may read are returned. Not available on Client Portal / White Label domains (7301).
  error_codes:
    - 7301
    - 7387
    - 7430
    - 7431
    - 7476
    - 8083
    - 8084
    - 8507
    - 8516
    - 8534
    - 8535
    - 8539
    - 8542
    - 8544
    - 8547
  openapi:
    file: "/references/openapi/org-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1orgs~1dashboards/get"
    config_schema: GetOrgDashboardsConfig
    response_schema: GetOrgDashboardsResponse
  sdk_examples: "/sdk-examples/organization-management/org-level-listings/get-org-dashboards.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/org-management-grouped-api.json"
    title: OpenAPI 3 specification - org-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T10:58:51Z
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

**GET `/restapi/v2/orgs/dashboards`** - Get Org Dashboards (Org-Level Listings / Organization Management).

Returns the dashboards of one organisation that the caller can read, across all of the caller's workspaces or across the workspaces named in `workspaceIds`. Most recently modified first, in pages.

From the OpenAPI specification:

Returns the dashboards of one organisation that the calling user may read, across all of the workspaces the caller can see or across the workspaces named in `workspaceIds`. The result is paged and is ordered with the most recently modified dashboard first.

Visibility follows the permissions of the caller: a dashboard is returned only when the caller administers its workspace, holds a custom role in it, or the dashboard has been shared with them or made public. Account Admins, Organization Admins and workspace admins see every dashboard in their workspaces. The API is not available on a Client Portal or White Label domain.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getOrgDashboards` |
| HTTP method | GET |
| URL | `/restapi/v2/orgs/dashboards` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the organisation whose dashboards are listed. |
| Permission required | The authenticated user must be a member of the organisation. Only dashboards the user may read are returned. Not available on Client Portal / White Label domains (7301). See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - optional |
| Success response | HTTP 200 - `application/json` |
| API units | 0.1 units per request - action `GET_ORG_DASHBOARDS` (api-id `3044`), **METADATA** category. See [API units](../../../foundations/api-units.md). |
| Frequency limit | 60 requests/minute across all **METADATA**-category calls of the organization. See [API units](../../../foundations/api-units.md#unit-categories-and-frequency-limits). |
| OpenAPI | [`org-management-grouped-api.json`](../../../references/openapi/org-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1orgs~1dashboards/get`; CONFIG schema `GetOrgDashboardsConfig`; response schema `GetOrgDashboardsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID, shown in the Zoho Analytics UI under Settings > Organisation. See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

This endpoint has no path parameters.

## CONFIG Parameters

CONFIG is **optional** for this API. Omit it to list the first 100 dashboards across every workspace the caller can see.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `workspaceIds` | JSONArray of String | No | All workspaces visible to the caller | IDs of the workspaces to list dashboards from. 0–1,000 entries, at most 10,000 characters in all. Duplicates are ignored. Every ID must belong to the organisation in the header (`7387`). The IDs are used as given: they are not checked against the workspaces [Get Org Workspaces](get-org-workspaces.md) returns for the caller. An empty array behaves like an omitted one. Supplying IDs does **not** bypass view-level access: dashboards the caller may not read are still left out. |
| `pageNo` | Integer | No | `1` | Page to return, `1–1000`. |
| `recordsPerPage` | Integer | No | `100` | Page size, `1–500`. |
| `searchKey` | String | No | None (no filter) | Returns only dashboards whose **name contains** this text. Up to 100 characters. The text is matched as **one phrase**; it is not split on spaces. Leading and trailing spaces are trimmed. An empty or whitespace-only string, or `null`, is refused with `8539`; omit `searchKey` to apply no filter. |

> A `CONFIG` that is not valid JSON, or a `workspaceIds` that is not a JSON array, is refused with [`8534`](../../../foundations/error-codes.md#error-8534). A key other than the four above is refused with [`8542`](../../../foundations/error-codes.md#error-8542). A key set to `null` or to an empty or blank string, or a `workspaceIds` entry that is, is refused with [`8539`](../../../foundations/error-codes.md#error-8539): leave the key out instead.

## Notes from the OpenAPI specification

- The CONFIG parameter is optional. Without it the first 100 dashboards across every workspace the caller can see are returned. As this is a GET request, the value must be stringified and URL encoded before it is sent.
- When **workspaceIds** is omitted the server first counts the workspaces the caller can see. More than 100 fails with error 7476 - name the workspaces in **workspaceIds** to proceed. The same cap applies to the number of IDs you send. The limit is a server setting and can be changed per organisation.
- **workspaceIds** is validated, not filtered. An ID that belongs to another organisation, or that does not exist, fails the whole request with error 7387 rather than being skipped.
- A CONFIG that is not valid JSON, or a **workspaceIds** that is not a JSON array, fails with error 8534. A key other than the four documented ones fails with error 8542. A key, or a **workspaceIds** entry, set to null or to an empty or blank string fails with error 8539 - leave the key out instead.
- CONFIG accepts at most 11,000 characters in all.

- Any member of the organisation may call this API. A user who is not a member is also admitted when they belong to the same Zoho organisation as the Account Admin, and the usual visibility rules then apply. Everyone else receives error 7301.
- An organisation can have org-level dashboard listing switched off. The Account Admin then receives error 7430 and every other caller receives error 7431.
- When Access Restrictions are active for the organisation, a caller whose email domain is not a trusted domain for sharing receives an empty list, and a caller who is barred from public views no longer receives public dashboards.
- The API is disabled on a Client Portal or White Label domain and is rejected there with error 7301.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get dashboards"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.views` | JSONArray | The dashboards on this page. **Always present**; `[]` when none. The array is named `views` even though every entry is a dashboard. |
| `data.views[].viewId` | String | Dashboard ID. |
| `data.views[].viewName` | String | Dashboard name. |
| `data.views[].viewDesc` | String | Dashboard description; `""` when none. |
| `data.views[].viewType` | String | Always `Dashboard` in this API. See [`viewType` Values](overview.md#viewtype-values). |
| `data.views[].parentViewId` | String | ID of the parent view; `""` when the dashboard has no parent. |
| `data.views[].folderId` | String | ID of the folder that holds the dashboard. A dashboard with no folder entry is reported as the string `"null"`. |
| `data.views[].createdTime` | String | Creation time as epoch milliseconds, returned as a string. |
| `data.views[].createdBy` | String | Email address of the dashboard's owner. `""` when the caller is not an active user of the owning organisation. The key is omitted when no address can be resolved. |
| `data.views[].lastModifiedTime` | String | Last modification time as epoch milliseconds, returned as a string. |
| `data.views[].lastModifiedBy` | String | Email address of the user who last modified the dashboard. Follows the same `""` and omission rules as `createdBy`. |
| `data.views[].isFavorite` | Boolean | `true` when **the caller** has marked the dashboard as a favourite. |
| `data.views[].sharedBy` | String | Email address of the user who shared the dashboard with the caller. Follows the same `""` and omission rules as `createdBy`; the key is omitted whenever no address is available for the sharer. |
| `data.views[].workspaceId` | String | ID of the workspace that holds the dashboard. |
| `data.views[].orgId` | String | ID of the organisation that owns the workspace. |
| `data.pageDetails` | JSONObject | Paging information. **Always present.** |
| `data.pageDetails.pageNo` | Integer | The page returned. |
| `data.pageDetails.recordsPerPage` | Integer | The page size used. |
| `data.pageDetails.hasNextPage` | Boolean | `true` when at least one more dashboard exists after this page. |

## Notes from the OpenAPI specification

- Only dashboards are returned, whatever else the workspace holds. For every other view type use the workspace-level APIs.
- The list is ordered with the most recently modified dashboard first. There is no sort parameter.
- **hasNextPage** is worked out after duplicate entries, and entries a custom role in the workspace does not allow, have been removed from the page. A page can therefore hold fewer than **recordsPerPage** entries, and on such a page **hasNextPage** can be false although later pages still hold dashboards. Keep requesting pages while **hasNextPage** is true, and do not treat a short page as proof that the list has ended.
- **createdBy**, **lastModifiedBy** and **sharedBy** are filled only when the caller is an active user of the owning organisation; otherwise they are empty strings. A key is left out when no address can be resolved for it.
- **isFavorite** belongs to the caller, not to the dashboard. The **isLive** field returned for other view types is never sent for a dashboard.
- Some builds return additional fields. Ignore unrecognised keys rather than validating against a closed schema.

# Examples

## Sample Requests

**Case 1 — First page of every dashboard the caller can read**

```http
GET /restapi/v2/orgs/dashboards HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Two workspaces only, ten per page, page two**

```http
GET /restapi/v2/orgs/dashboards?CONFIG={"workspaceIds":["137687000271334001","466206000000071000"],"pageNo":2,"recordsPerPage":10} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — Search by name**

```http
GET /restapi/v2/orgs/dashboards?CONFIG={"searchKey":"Sales"} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 4 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
GET /restapi/v2/orgs/dashboards HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — Two dashboards, more pages available**

```json
{
    "status": "success",
    "summary": "Get dashboards",
    "data": {
        "views": [
            {
                "viewId": "466206000000106002",
                "viewName": "Support Overview",
                "viewDesc": "Open tickets by priority",
                "viewType": "Dashboard",
                "parentViewId": "",
                "folderId": "466206000000071005",
                "createdTime": "1718361737000",
                "createdBy": "jane.doe@example.com",
                "lastModifiedTime": "1720000000000",
                "lastModifiedBy": "jane.doe@example.com",
                "isFavorite": true,
                "sharedBy": "jane.doe@example.com",
                "workspaceId": "466206000000071000",
                "orgId": "700000123456"
            },
            {
                "viewId": "466206000000106003",
                "viewName": "Support Backlog",
                "viewDesc": "",
                "viewType": "Dashboard",
                "parentViewId": "",
                "folderId": "null",
                "createdTime": "1707286805000",
                "createdBy": "jane.doe@example.com",
                "lastModifiedTime": "1719000000000",
                "lastModifiedBy": "john.roe@example.com",
                "isFavorite": false,
                "sharedBy": "jane.doe@example.com",
                "workspaceId": "466206000000071000",
                "orgId": "700000123456"
            }
        ],
        "pageDetails": {
            "pageNo": 1,
            "recordsPerPage": 2,
            "hasNextPage": true
        }
    }
}
```

**HTTP 200 OK — No dashboards visible to the caller**

```json
{
    "status": "success",
    "summary": "Get dashboards",
    "data": {
        "views": [],
        "pageDetails": {
            "pageNo": 1,
            "recordsPerPage": 100,
            "hasNextPage": false
        }
    }
}
```

**HTTP 400 Bad Request — A workspace ID belongs to a different organisation, or does not exist**

```json
{
    "status": "failure",
    "summary": "DBID_NOT_BELONGS_TO_ZSOID",
    "data": {
        "errorCode": 7387,
        "errorMessage": "Workspaces(s) does not belongs to current Organization"
    }
}
```

**HTTP 400 Bad Request — Too many workspaces to scan**

```json
{
    "status": "failure",
    "summary": "ORG_LEVEL_VIEWS_WS_MORE_THAN_ALLOWED_LIMIT",
    "data": {
        "errorCode": 7476,
        "errorMessage": "Workspace count is more than the allowed limit. Kindly specify the workspace id's to get the views."
    }
}
```

**HTTP 403 Forbidden — Request sent through a Client Portal / White Label domain**

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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Org Dashboards](../../../sdk-examples/organization-management/org-level-listings/get-org-dashboards.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Read-only and idempotent** | Changes nothing. |
| **Dashboards only** | Only dashboards are returned, whatever the workspace holds. For every other view type use the workspace-level APIs. |
| **Per-caller result** | Visibility follows the caller's permissions; see [Visibility and Access Scoping](overview.md#visibility-and-access-scoping). The same request returns different dashboards for different users. |
| **Who may call** | A member of the organisation. A user who is not a member is also admitted when they belong to the same Zoho organisation as the Account Admin; for them the usual visibility rules apply. Everyone else receives `7301`. |
| **Order** | Most recently modified first (the later of the last data change and the last design change). There is no sort parameter. |
| **Paging** | `hasNextPage` is worked out after duplicate entries, and entries a custom role in the workspace does not allow, have been removed from the page. A page can therefore hold fewer than `recordsPerPage` entries, and on such a page `hasNextPage` can be `false` although later pages still hold dashboards. Keep requesting pages while `hasNextPage` is `true`, and do not treat a short page as proof that the list has ended. |
| **Workspace limit** | When `workspaceIds` is omitted, the server first counts the caller's workspaces. More than 100 fails with `7476`; name the workspaces in `workspaceIds` to proceed. The same cap applies to the number of IDs you send. |
| **`workspaceIds` is validated, not filtered** | An ID from another organisation, or one that does not exist, fails the whole request with `7387`. It is not skipped. IDs you send replace the caller's visible-workspace scan: they are not compared with what [Get Org Workspaces](get-org-workspaces.md) returns, and dashboards the caller may not read are still left out. |
| **Switched off for the organisation** | An organisation can have org-level dashboard listing blocked. The Account Admin receives `7430` (contact support); every other caller receives `7431` (contact the account admin). |
| **`searchKey`** | A substring match on the dashboard name, applied before paging, so `pageDetails` reflects the filtered set. |
| **Email fields are conditional** | `createdBy`, `lastModifiedBy` and `sharedBy` are filled only when the caller is an active user of the owning organisation; otherwise they are `""`. A key is left out when no address can be resolved for it. |
| **`isFavorite` belongs to the caller** | It is not a property of the dashboard. |
| **No `isLive` flag** | The `isLive` field returned for other view types is never sent for dashboards. |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get Org Workspaces](get-org-workspaces.md) → `workspaceId` (optional) → Get Org Dashboards → `viewId` and `workspaceId` for the workspace-scoped view APIs. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not a member of the organisation named in the header, or the request came through a Client Portal / White Label domain. | Call from the standard API host as a member of the organisation named in the header. |
| [7387](../../../foundations/error-codes.md#error-7387) | 400 | `DBID_NOT_BELONGS_TO_ZSOID` — A `workspaceIds` entry does not belong to the organisation in the header, or does not exist. | Take workspace IDs from [Get Org Workspaces](get-org-workspaces.md) for the same organisation. |
| [7430](../../../foundations/error-codes.md#error-7430) | 400 | `ORG_LEVEL_VIEWS_NOT_ALLOWED` — Org-level view listing is blocked for the organisation; reported to its Account Admin. | Use the workspace-level APIs, or contact support. |
| [7431](../../../foundations/error-codes.md#error-7431) | 400 | `ORG_LEVEL_VIEWS_NOT_ALLOWED_WL_USERS` — Org-level view listing is blocked for the organisation; reported to every caller other than the Account Admin. | Use the workspace-level APIs, or contact the account admin. |
| [7476](../../../foundations/error-codes.md#error-7476) | 400 | `ORG_LEVEL_VIEWS_WS_MORE_THAN_ALLOWED_LIMIT` — More workspaces are in scope than the limit allows. | Send `workspaceIds` listing the workspaces you want, within the limit. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| [8084](../../../foundations/error-codes.md#error-8084) | 404 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Read the Organization ID from **Settings → Organisation** in the Zoho Analytics UI. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | `MORE_THAN_MAX_LENGTH` — `searchKey` exceeds 100 characters, `workspaceIds` exceeds 10,000 characters, or `CONFIG` exceeds 11,000 characters. | Shorten the value, or send fewer workspace IDs per call. |
| [8516](../../../foundations/error-codes.md#error-8516) | 400 | `UNABLE_TO_PARSE_DATA_TYPE` — `pageNo` or `recordsPerPage` is not a number. | Send a plain number. |
| [8534](../../../foundations/error-codes.md#error-8534) | 400 | `JSON_PARSE_ERROR` — `CONFIG` is not valid JSON, or `workspaceIds` is not an array. | Fix the JSON and URL-encode it correctly; send `workspaceIds` as an array of strings. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |
| [8539](../../../foundations/error-codes.md#error-8539) | 400 | `INVALID_VALUE_NOT_ALLOWED` — `CONFIG` is sent empty, or a `CONFIG` value (`searchKey`, `pageNo`, `recordsPerPage`, `workspaceIds` or one of its entries) is `null` or an empty or blank string. | Leave the key out instead of sending an empty value, and send only non-empty workspace IDs. |
| [8542](../../../foundations/error-codes.md#error-8542) | 400 | `EXTRA_KEY_FOUND_IN_JSON` — `CONFIG` holds a key other than `workspaceIds`, `pageNo`, `recordsPerPage` and `searchKey`. | Remove the key. |
| [8544](../../../foundations/error-codes.md#error-8544) | 400 | `OUT_OF_RANGE` — `pageNo` is outside 1–1,000, or `recordsPerPage` is outside 1–500. | Use a value inside the range. |
| [8547](../../../foundations/error-codes.md#error-8547) | 400 | `ARRAY_SIZE_OUT_OF_RANGE` — `workspaceIds` holds more than 1,000 entries. | Send at most 1,000 IDs — in practice no more than the workspace limit (`7476`). |

# Related

- [Org-Level Listings overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Organization Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Org Workspaces](get-org-workspaces.md), [Get Org Recent Items](get-org-recent-items.md).
- [SDK examples](../../../sdk-examples/organization-management/org-level-listings/get-org-dashboards.md).
- [API units](../../../foundations/api-units.md) - unit cost, unit categories and frequency limits for every endpoint.
