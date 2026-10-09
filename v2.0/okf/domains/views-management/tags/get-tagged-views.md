---
type: API Endpoint
title: Get Tagged Views
description: Returns the views that carry a given tag.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - tags
  - get
  - metadata
api:
  operation_id: getTaggedViews
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views"
  domain: views-management
  group: tags
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: query
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: Any user with access to the workspace. The returned list is filtered to the views the caller can see.
  error_codes:
    - 7103
    - 7301
    - 7390
    - 8083
    - 8184
    - 8507
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1tags~1{tag-id}~1views/get"
    config_schema: GetTaggedViewsConfig
    response_schema: GetTaggedViewsResponse
  sdk_examples: "/sdk-examples/views-management/tags/get-tagged-views.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views`** - Get Tagged Views (Tags / Views Management).

Returns the views that carry a given tag.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace that owns the tag. |
| `<tag-id>` | Long | ID of the tag. Must exist in `<workspace-id>`, otherwise `8184`. |

From the OpenAPI specification:

Returns the views that carry a given tag.

The result can be paged with limit and offset. It is the inverse of the Get View Tags API - the same association table read from the tag side. A tag that exists but labels nothing returns an empty array, while a tag that does not exist fails with error 8184.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getTaggedViews` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | Any user with access to the workspace. The returned list is filtered to the views the caller can see. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - optional |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1tags~1{tag-id}~1views/get`; CONFIG schema `GetTaggedViewsConfig`; response schema `GetTaggedViewsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{tag-id}` | string | ID of the tag. | [How to obtain](../../../foundations/identifiers.md#tag-id) |

## CONFIG Parameters

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | Integer | No | unlimited | Maximum number of views to return. Omit to return all of them. |
| `offset` | Integer | No | `0` | Number of views to skip before collecting the result. Used with `limit` to page through a large association list. |

## Notes from the OpenAPI specification

- Any user with access to the workspace can invoke this API. The returned list is **filtered to the views the calling user can see** - a shared user sees only the tagged views shared with them, while an administrator sees all of them. Two users can legitimately receive different lists for the same tag.
- The CONFIG parameter is optional. Without it, every view carrying the tag is returned. As this is a GET request, the value must be stringified and URL encoded before it is sent.
- **limit** and **offset** are the only paging controls. No cursor and no total count are returned, so request one more than needed and check for the extra row, or keep paging until a short page comes back.
- A tag that does not exist in the workspace fails with error code **8184**. An empty **views** array means the tag exists and labels nothing - including immediately after Remove Tag From Multiple Views with **dissociateAll** set to true.
- **type** is a view type name such as Table, AnalysisView or Dashboard, never a numeric code.
- The **id** values returned here are the view-id path parameter of the Get View Tags, Add Multiple Tags To View and Remove Multiple Tags From View APIs.
- The order of the result is not guaranteed. Sort client-side if presentation order matters.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | `"success"` on success. |
| `summary` | String | `"Get tagged views"`. |
| `data` | Object | Wrapper. |
| `data.views` | Array | Views carrying the tag that the caller is entitled to see. Empty when there are none. |
| `data.views[].id` | String | ID of the view, **as a string**. The `<view-id>` for [Get View Tags](get-view-tags.md), [Add Multiple Tags To View](add-tags-to-view.md), and [Remove Multiple Tags From View](remove-tags-from-view.md). |
| `data.views[].name` | String | Display name of the view. |
| `data.views[].type` | String | View type. See [View `type` values](#view-type-values). |

### View `type` values

| Value | View type |
|-------|-----------|
| `Table` | A table |
| `Report` | A tabular view |
| `AnalysisView` | A chart view |
| `Pivot` | A pivot view |
| `SummaryView` | A summary view |
| `TableView` | A table view |
| `QueryTable` | A query table |
| `Dashboard` | A dashboard |
| `WIDGET` | A dashboard widget |
| `Tab` | A dashboard tab |
| `PipelineTable` | A pipeline table |
| `DataModelObject` | A data model object |

# Examples

## Sample Requests

**Case 1 — every view carrying the tag**

```http
GET /restapi/v2/workspaces/320873000000419001/tags/320873000000425158/views HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — the second page of ten**

```http
GET /restapi/v2/workspaces/320873000000419001/tags/320873000000425158/views HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

```json
{
  "limit": 10,
  "offset": 10
}
```

As this is a `GET`, the CONFIG travels as a stringified, URL-encoded query parameter — see [Request conventions](../../../foundations/request-conventions.md).

## Sample Responses

**HTTP 200 OK — a tag spanning four view types**

```json
{
  "status": "success",
  "summary": "Get tagged views",
  "data": {
    "views": [
      {
        "id": "20867000000038313",
        "name": "Sales_Table",
        "type": "Table"
      },
      {
        "id": "20867000000038314",
        "name": "Dashboard_1",
        "type": "Dashboard"
      },
      {
        "id": "20867000000038319",
        "name": "Chart1",
        "type": "AnalysisView"
      },
      {
        "id": "20867000000038322",
        "name": "Pivot",
        "type": "Pivot"
      }
    ]
  }
}
```

**HTTP 200 OK — the tag exists but labels nothing**

```json
{
  "status": "success",
  "summary": "Get tagged views",
  "data": {
    "views": []
  }
}
```

This is also what you get immediately after [Remove Tag From Multiple Views](remove-tag-from-views.md) with `dissociateAll: true`.

**HTTP 403 Forbidden — the tag does not exist in this workspace**

```json
{
  "status": "failure",
  "summary": "VIEW_OR_TAG_NOT_PRESENT_IN_DB_TO_TAG",
  "data": {
    "errorCode": 8184,
    "errorMessage": "View/Tag not present or duplicated in db."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Tagged Views](../../../sdk-examples/views-management/tags/get-tagged-views.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **The result is filtered to what the caller can see** | Two users calling this with the same `<tag-id>` can legitimately get different lists. A shared user sees only the tagged views shared with them; an administrator sees all of them. Do not treat the response as the complete association set unless the caller is an administrator. |
| **`limit` and `offset` are the only paging controls** | No cursor and no total count are returned, so you cannot tell from one response whether more pages exist. Request `limit + 1` and check whether you got an extra row, or keep paging until a short page comes back. |
| **A non-existent tag is an error, not an empty list** | `8184`. An empty `views` array means the tag exists and labels nothing. |
| **It is the inverse of [Get View Tags](get-view-tags.md)** | Same association table, read from the other end. |
| **Every value is a string** | Including `id`. `type` is a name, never a numeric code. |
| **Ordering is not guaranteed** | Sort client-side if presentation order matters. |
| **Dependency chain:** | [Get Tags List](get-tags.md) or [Create Tag](create-tag.md) → `<tag-id>` → Get Tagged Views → `views[].id`. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — The workspace does not exist. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller has no access to the workspace. | Ensure the workspace is shared with the calling user. |
| [7390](../../../foundations/error-codes.md#error-7390) | 400 | `WORKSPACE_NOT_BELONGS_TO_ORG` — The workspace does not belong to the organization in `ZANALYTICS-ORGID`. | Send the organization ID that owns the workspace. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing. | Add the header. |
| [8184](../../../foundations/error-codes.md#error-8184) | 403 | `VIEW_OR_TAG_NOT_PRESENT_IN_DB_TO_TAG` — The tag does not exist in this workspace. | Verify `<tag-id>` with [Get Tags List](get-tags.md). |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | `MORE_THAN_MAX_LENGTH` — `CONFIG` exceeds 1,000 characters. | Send only `limit` and `offset`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.metadata.read`. |

# Related

- [Tags overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Tags List](get-tags.md), [Get View Tags](get-view-tags.md), [Create Tag](create-tag.md), [Update Tag](update-tag.md), [Delete Tag](delete-tag.md), [Add Tag To Multiple Views](add-tag-to-views.md), [Remove Tag From Multiple Views](remove-tag-from-views.md), [Add Multiple Tags To View](add-tags-to-view.md), [Remove Multiple Tags From View](remove-tags-from-view.md).
- [SDK examples](../../../sdk-examples/views-management/tags/get-tagged-views.md).
