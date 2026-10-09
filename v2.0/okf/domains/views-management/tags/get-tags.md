---
type: API Endpoint
title: Get Tags List
description: Returns every tag that exists in the workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/tags"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - tags
  - get
  - metadata
api:
  operation_id: getTags
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/tags"
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
  permission_required: "Any user with access to the workspace - an Account Admin or Organization Admin, a Workspace Admin, or any shared user, including users holding a custom role."
  error_codes:
    - 7103
    - 7301
    - 7390
    - 8083
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1tags/get"
    config_schema: null
    response_schema: GetTagsResponse
  sdk_examples: "/sdk-examples/views-management/tags/get-tags.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/tags`** - Get Tags List (Tags / Views Management).

Returns every tag that exists in the workspace.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace whose tags are listed. |

From the OpenAPI specification:

Returns every tag that exists in the workspace.

A tag is listed whether or not it is attached to any view. To find out which views a tag labels, use the Get Tagged Views API. Every user who can open the workspace can read the list, including shared users on custom roles.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getTags` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/tags` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | Any user with access to the workspace - an Account Admin or Organization Admin, a Workspace Admin, or any shared user, including users holding a custom role. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1tags/get`; response schema `GetTagsResponse` |

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

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- Any user with access to the workspace can invoke this API - Account Admins, Organization Admins, Workspace Admins and every shared user, including users holding a custom role.
- This API lists tags, not associations. A tag appears here whether or not it is attached to a view. Use the Get Tagged Views API to find out what a tag labels.
- The **id** values returned here are the tag-id path parameter of the Update Tag, Delete Tag, Get Tagged Views, Add Tag To Multiple Views and Remove Tag From Multiple Views APIs, and the **tagIds** entries of the Add Multiple Tags To View and Remove Multiple Tags From View APIs.
- There is no lookup-by-name API. To resolve a tag name to an identifier, list the tags and match client-side.
- The list is not paginated and its order is not guaranteed. Sort client-side if presentation order matters.
- An empty **tags** array is a success, not an error. It means the workspace has no tags yet.
- This API is available in Client Portal (White Label) contexts, subject to the same permissions.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | `"success"` on success. |
| `summary` | String | `"Get tags"`. |
| `data` | Object | Wrapper. |
| `data.tags` | Array | Every tag in the workspace. Empty when there are none. |
| `data.tags[].id` | String | ID of the tag, **as a string**. This is the `<tag-id>` for [Update Tag](update-tag.md), [Delete Tag](delete-tag.md), [Get Tagged Views](get-tagged-views.md), [Add Tag To Multiple Views](add-tag-to-views.md), and [Remove Tag From Multiple Views](remove-tag-from-views.md), and the `tagIds` value for [Add Multiple Tags To View](add-tags-to-view.md) and [Remove Multiple Tags From View](remove-tags-from-view.md). |
| `data.tags[].name` | String | Display name of the tag, unique within the workspace. |
| `data.tags[].colorCode` | String | Hex colour, returned exactly as it was stored. |

# Examples

## Sample Requests

```http
GET /restapi/v2/workspaces/320873000000419001/tags HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

There is nothing else to send.

## Sample Responses

**HTTP 200 OK — a workspace with four tags**

```json
{
  "status": "success",
  "summary": "Get tags",
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

Note that two different tags share `#f5a623` — colours are not unique.

**HTTP 200 OK — a workspace with no tags**

```json
{
  "status": "success",
  "summary": "Get tags",
  "data": {
    "tags": []
  }
}
```

An empty array is a success, not an error.

**HTTP 403 Forbidden — the caller cannot reach the workspace**

```json
{
  "status": "failure",
  "summary": "SECURITY_NOT_PERMITTED",
  "data": {
    "errorCode": 7301,
    "errorMessage": "You do not have the permission to perform this operation."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Tags List](../../../sdk-examples/views-management/tags/get-tags.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **It lists tags, not associations** | A tag appears here whether or not it is attached to anything. To find out what a tag labels, call [Get Tagged Views](get-tagged-views.md). |
| **Every user who can open the workspace can read it** | Including shared users on custom roles. Tags are a shared vocabulary, so the read is deliberately unrestricted. |
| **Ordering is not guaranteed** | Do not depend on the array order. Sort client-side if you need a stable presentation. |
| **`id` is a string** | Even though it is numerically a long. Do not parse it into a fixed-width integer type. |
| **There is no pagination** | The full tag list is returned in one response. The per-view ceiling keeps workspaces from accumulating unbounded tags in practice. |
| **An empty list is a success** | `{"tags": []}` with HTTP 200. |
| **Dependency chain:** | Get Tags List → `tags[].id` → [Add Multiple Tags To View](add-tags-to-view.md) / [Get Tagged Views](get-tagged-views.md) / [Update Tag](update-tag.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — The workspace does not exist. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller has no access to the workspace. | Ensure the workspace is shared with the calling user. |
| [7390](../../../foundations/error-codes.md#error-7390) | 400 | `WORKSPACE_NOT_BELONGS_TO_ORG` — The workspace does not belong to the organization in `ZANALYTICS-ORGID`. | Send the organization ID that owns the workspace. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing. | Add the header. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.metadata.read`. |

# Related

- [Tags overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Tagged Views](get-tagged-views.md), [Get View Tags](get-view-tags.md), [Create Tag](create-tag.md), [Update Tag](update-tag.md), [Delete Tag](delete-tag.md), [Add Tag To Multiple Views](add-tag-to-views.md), [Remove Tag From Multiple Views](remove-tag-from-views.md), [Add Multiple Tags To View](add-tags-to-view.md), [Remove Multiple Tags From View](remove-tags-from-view.md).
- [SDK examples](../../../sdk-examples/views-management/tags/get-tags.md).
