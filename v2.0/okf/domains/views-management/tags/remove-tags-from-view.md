---
type: API Endpoint
title: Remove Multiple Tags From View
description: "Detaches a batch of tags from one view, or clears the view of every tag."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - tags
  - delete
  - modeling
api:
  operation_id: removeTagsFromView
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags"
  domain: views-management
  group: tags
  oauth_scopes:
    - ZohoAnalytics.modeling.delete
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Edit Design permission on the view. Read-only users are rejected with 8180."
  error_codes:
    - 7104
    - 7301
    - 7390
    - 8083
    - 8180
    - 8184
    - 8202
    - 8504
    - 8507
    - 8535
    - 8547
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1tags/delete"
    config_schema: RemoveTagsFromViewConfig
    response_schema: null
  sdk_examples: "/sdk-examples/views-management/tags/remove-tags-from-view.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**DELETE `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags`** - Remove Multiple Tags From View (Tags / Views Management).

Detaches a batch of **tags** from one view, or clears the view entirely.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace that owns the view and the tags. |
| `<view-id>` | Long | ID of the view. Must belong to `<workspace-id>`. |

From the OpenAPI specification:

Detaches a batch of tags from one view, or clears the view of every tag.

The tags survive and stay attached to every other view - only this view's links are removed. Setting dissociateAll to true is scoped to this single view, which makes it the safe way to reset a view's labels and to free slots against the ten-tag ceiling.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `removeTagsFromView` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingdelete) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Edit Design permission on the view. Read-only users are rejected with 8180. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1tags/delete`; CONFIG schema `RemoveTagsFromViewConfig` |

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
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `tagIds` | JSONArray of Long | Conditional | — | IDs of the tags to detach, 1–1000 entries. **Required unless `dissociateAll` is `true`**; an empty or absent array with `dissociateAll` off fails with `8202`. |
| `dissociateAll` | Boolean | No | `false` | When `true`, **every** tag is detached from the view and `tagIds` is ignored. |

## Notes from the OpenAPI specification

- The calling user must be an Account Admin, Organization Admin or Workspace Admin of the workspace, or the View Owner, or any user with Edit Design permission on the view.
- Read-only users are blocked from every association API with error code **8180**, even on views they own.
- Exactly one of the two mechanisms applies. Either send **tagIds** with 1 to 1000 tag identifiers, or set **dissociateAll** to true. An empty or absent **tagIds** with **dissociateAll** off fails with error code **8202**.
- When **dissociateAll** is true, any **tagIds** sent alongside it is ignored and every tag is detached from this one view. Unlike the same flag on the Remove Tag From Multiple Views API, the blast radius is a single view.
- The tags survive. They remain in the workspace and stay attached to every other view.
- Detaching a tag that was not attached is not an error. The operation is defined by the end state.
- Use this API to make room at the ten-tag ceiling before invoking the Add Multiple Tags To View API.
- The error message for **8202** refers to an attribute named removeAll. The attribute this API actually accepts is **dissociateAll**.
- The view-id in the request URI must belong to the workspace in the request URI.
- The API returns HTTP 204 No Content with an empty body on success. Confirm with the Get View Tags API.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

**None.** This API returns `204 No Content` with an empty body. Confirm with [Get View Tags](get-view-tags.md).

# Examples

## Sample Requests

**Case 1 — detach one named tag**

```http
DELETE /restapi/v2/workspaces/320873000000419001/views/20867000000038313/tags HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded
```

```json
{
  "tagIds": ["320873000000419779"]
}
```

**Case 2 — clear every tag from the view**

```json
{
  "dissociateAll": true
}
```

**Case 3 — `dissociateAll` explicitly off, with named tags**

```json
{
  "tagIds": ["320873000000425158"],
  "dissociateAll": false
}
```

## Sample Responses

**HTTP 204 No Content — the tags were detached**

```
HTTP/1.1 204 No Content
```

**HTTP 200 OK — reading the view's tags afterwards**

```json
{
  "status": "success",
  "summary": "Get view tags",
  "data": {
    "tags": []
  }
}
```

**HTTP 400 Bad Request — neither `tagIds` nor `dissociateAll` was usable**

```json
{
  "status": "failure",
  "summary": "INVALID_CONFIGURATION_REMOVE_TAGS_FOR_VIEW",
  "data": {
    "errorCode": 8202,
    "errorMessage": "Invalid configuration. Kindly provide valid tagIds or set 'removeAll' to 'true' to remove all tags from the view."
  }
}
```

> The message text names `removeAll`; the attribute this API actually accepts is **`dissociateAll`**.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Remove Multiple Tags From View](../../../sdk-examples/views-management/tags/remove-tags-from-view.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **The tags survive** | Only this view's links are removed. The tags remain in the workspace and stay attached to every other view. |
| **`dissociateAll` overrides `tagIds`** | When `true`, any `tagIds` sent alongside it is ignored. |
| **`dissociateAll: true` is scoped to this one view** | Unlike its tag-side counterpart, the blast radius is a single view — which makes it the safe way to reset a view's labels. |
| **Detaching a tag that was not attached is not an error** | The operation is defined by the end state. |
| **It frees slots against the ten-tag ceiling** | Use it before [Add Multiple Tags To View](add-tags-to-view.md) when a view is at the limit. |
| **The View Owner can call it** | Same permission rule as [Add Multiple Tags To View](add-tags-to-view.md). |
| **Read-only users are blocked outright** | `8180`. |
| **Dependency chain:** | [Get View Tags](get-view-tags.md) → `tags[].id` → Remove Multiple Tags From View → [Get View Tags](get-view-tags.md) to verify. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — The view does not exist. | Verify `<view-id>` with [Get View List](../view-operations/get-views.md). |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller lacks Edit Design permission on the view, or the view does not belong to `<workspace-id>`. | Call as an administrator, the View Owner, or a user with Edit Design permission. |
| [7390](../../../foundations/error-codes.md#error-7390) | 400 | `WORKSPACE_NOT_BELONGS_TO_ORG` — The workspace does not belong to the organization in `ZANALYTICS-ORGID`. | Send the organization ID that owns the workspace. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing. | Add the header. |
| [8180](../../../foundations/error-codes.md#error-8180) | 403 | `DONT_HAVE_PERMISSION_TO_ASSOCIATE_AND_UNASSOCIATE_TAGS` — The caller is a read-only user. | Associations cannot be changed by read-only users. |
| [8184](../../../foundations/error-codes.md#error-8184) | 403 | `VIEW_OR_TAG_NOT_PRESENT_IN_DB_TO_TAG` — One of the tags does not exist in this workspace. | Verify the IDs with [Get View Tags](get-view-tags.md). |
| [8202](../../../foundations/error-codes.md#error-8202) | 400 | `INVALID_CONFIGURATION_REMOVE_TAGS_FOR_VIEW` — `tagIds` is empty or absent and `dissociateAll` is not `true`. | Send a non-empty `tagIds`, or set `dissociateAll` to `true`. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` was not sent. | Send a CONFIG object. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | `MORE_THAN_MAX_LENGTH` — `tagIds` exceeds 50,000 characters. | Split the batch. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.modeling.delete`. |
| [8547](../../../foundations/error-codes.md#error-8547) | 400 | `ARRAY_SIZE_OUT_OF_RANGE` — `tagIds` exceeds 1000 entries. | Send at most 1000 tag IDs, or use `dissociateAll`. |

# Related

- [Tags overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Tags List](get-tags.md), [Get Tagged Views](get-tagged-views.md), [Get View Tags](get-view-tags.md), [Create Tag](create-tag.md), [Update Tag](update-tag.md), [Delete Tag](delete-tag.md), [Add Tag To Multiple Views](add-tag-to-views.md), [Remove Tag From Multiple Views](remove-tag-from-views.md), [Add Multiple Tags To View](add-tags-to-view.md).
- [SDK examples](../../../sdk-examples/views-management/tags/remove-tags-from-view.md).
