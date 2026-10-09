---
type: API Endpoint
title: Get View Tags
description: Returns the tags attached to a given view.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - tags
  - get
  - metadata
api:
  operation_id: getViewTags
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags"
  domain: views-management
  group: tags
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: Any user with Read permission on the view.
  error_codes:
    - 7104
    - 7301
    - 7390
    - 8083
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1tags/get"
    config_schema: null
    response_schema: GetViewTagsResponse
  sdk_examples: "/sdk-examples/views-management/tags/get-view-tags.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags`** - Get View Tags (Tags / Views Management).

Returns the tags attached to a given view.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace that owns the view. |
| `<view-id>` | Long | ID of the view. Must belong to `<workspace-id>`. |

From the OpenAPI specification:

Returns the tags attached to a given view.

The response has the same shape as the Get Tags List API, limited to the tags on this one view - at most ten. The length of the array is the current tag count of the view, which is the pre-flight check for the ten-tag ceiling before adding more. It is the inverse of the Get Tagged Views API.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getViewTags` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | Any user with Read permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1tags/get`; response schema `GetViewTagsResponse` |

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
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- The calling user needs only Read permission on the view. This is narrower than the workspace-wide check used by the other two read APIs, but still open to any shared user who can open the view.
- The length of the **tags** array is the current tag count of the view. Count it before invoking the Add Multiple Tags To View API to know how many of the ten slots remain, rather than catching error **8181**.
- The response shape is identical to the Get Tags List API - the same **tags** array with **id**, **name** and **colorCode**. Only the summary and the scope of the result differ.
- There is no pagination. The ten-tag ceiling makes it unnecessary.
- The view-id in the request URI must belong to the workspace in the request URI. A view from another workspace is rejected with error code **7301**.
- An empty **tags** array is a success. It is what Remove Multiple Tags From View with **dissociateAll** set to true leaves behind.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | `"success"` on success. |
| `summary` | String | `"Get view tags"`. |
| `data` | Object | Wrapper. |
| `data.tags` | Array | Tags attached to the view — at most 10 entries. Empty when the view is untagged. |
| `data.tags[].id` | String | ID of the tag, **as a string**. |
| `data.tags[].name` | String | Display name of the tag. |
| `data.tags[].colorCode` | String | Hex colour of the tag. |

# Examples

## Sample Requests

```http
GET /restapi/v2/workspaces/320873000000419001/views/20867000000038313/tags HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — a view carrying four tags**

```json
{
  "status": "success",
  "summary": "Get view tags",
  "data": {
    "tags": [
      {
        "id": "320873000000425158",
        "name": "Tag_AccountAdmin_1_Updated",
        "colorCode": "#e72d35"
      },
      {
        "id": "320873000000419779",
        "name": "Tag_AccountAdmin_2",
        "colorCode": "#f5a623"
      },
      {
        "id": "320873000000421641",
        "name": "Tag_OrgAdmin_1_Updated",
        "colorCode": "#55acee"
      },
      {
        "id": "320873000000424199",
        "name": "Tag_WkAdmin_1_Updated",
        "colorCode": "#f5a623"
      }
    ]
  }
}
```

**HTTP 200 OK — an untagged view**

```json
{
  "status": "success",
  "summary": "Get view tags",
  "data": {
    "tags": []
  }
}
```

This is what [Remove Multiple Tags From View](remove-tags-from-view.md) with `dissociateAll: true` leaves behind.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get View Tags](../../../sdk-examples/views-management/tags/get-view-tags.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **The array length is the current tag count** | Count it before calling [Add Multiple Tags To View](add-tags-to-view.md) to know how many of the ten slots remain, rather than catching `8181`. |
| **It needs only Read permission on the view** | Narrower than the workspace-wide check the other two read APIs use, but still open to any shared user who can open the view. |
| **The response shape is identical to [Get Tags List](get-tags.md)** | Same `tags[]` array, same three fields. Only the `summary` and the scope of the result differ. |
| **It is the inverse of [Get Tagged Views](get-tagged-views.md)** | Same association table, read from the other end. |
| **There is no pagination** | The ten-tag ceiling makes it unnecessary. |
| **The view must belong to the workspace in the path** | A view ID from another workspace is rejected. |
| **Dependency chain:** | [Get View List](../view-operations/get-views.md) or [Get Tagged Views](get-tagged-views.md) → `<view-id>` → Get View Tags → `tags[].id`. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — The view does not exist. | Verify `<view-id>` with [Get View List](../view-operations/get-views.md). |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller lacks Read permission on the view, or the view does not belong to `<workspace-id>`. | Ensure the view is shared with the calling user. |
| [7390](../../../foundations/error-codes.md#error-7390) | 400 | `WORKSPACE_NOT_BELONGS_TO_ORG` — The workspace does not belong to the organization in `ZANALYTICS-ORGID`. | Send the organization ID that owns the workspace. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing. | Add the header. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.metadata.read`. |

# Related

- [Tags overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Tags List](get-tags.md), [Get Tagged Views](get-tagged-views.md), [Create Tag](create-tag.md), [Update Tag](update-tag.md), [Delete Tag](delete-tag.md), [Add Tag To Multiple Views](add-tag-to-views.md), [Remove Tag From Multiple Views](remove-tag-from-views.md), [Add Multiple Tags To View](add-tags-to-view.md), [Remove Multiple Tags From View](remove-tags-from-view.md).
- [SDK examples](../../../sdk-examples/views-management/tags/get-view-tags.md).
