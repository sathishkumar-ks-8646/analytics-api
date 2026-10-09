---
type: API Endpoint
title: Remove Tag From Multiple Views
description: "Detaches one tag from a batch of views, or from every view at once."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - tags
  - delete
  - modeling
api:
  operation_id: removeTagFromViews
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views"
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
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. The View Owner alone does not qualify. Read-only users are rejected with 8180."
  error_codes:
    - 7103
    - 7301
    - 7390
    - 8083
    - 8180
    - 8184
    - 8201
    - 8504
    - 8507
    - 8535
    - 8547
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1tags~1{tag-id}~1views/delete"
    config_schema: RemoveTagFromViewsConfig
    response_schema: null
  sdk_examples: "/sdk-examples/views-management/tags/remove-tag-from-views.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views`** - Remove Tag From Multiple Views (Tags / Views Management).

Detaches **one tag** from a batch of views, or from every view at once.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace that owns the tag and the views. |
| `<tag-id>` | Long | ID of the tag to detach. Must exist in `<workspace-id>`. |

From the OpenAPI specification:

Detaches one tag from a batch of views, or from every view at once.

Only the associations are removed - the tag survives and can be re-attached, which is the difference from the Delete Tag API. Either name the views in viewIds, or set dissociateAll to true to strip the tag from every view in the workspace.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `removeTagFromViews` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingdelete) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. The View Owner alone does not qualify. Read-only users are rejected with 8180. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1tags~1{tag-id}~1views/delete`; CONFIG schema `RemoveTagFromViewsConfig` |

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
| `{tag-id}` | string | ID of the tag. | [How to obtain](../../../foundations/identifiers.md#tag-id) |

## CONFIG Parameters

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `viewIds` | JSONArray of Long | Conditional | — | IDs of the views to detach the tag from, 1–1000 entries. **Required unless `dissociateAll` is `true`**; an empty or absent array with `dissociateAll` off fails with `8201`. |
| `dissociateAll` | Boolean | No | `false` | When `true`, the tag is detached from **every** view in the workspace and `viewIds` is ignored. |

> Exactly one of the two mechanisms applies. Either name the views, or set `dissociateAll` to `true`.

## Notes from the OpenAPI specification

- The calling user must be an Account Admin, Organization Admin or Workspace Admin of the workspace. A View Owner who is not a Workspace Admin must use the Remove Multiple Tags From View API instead.
- Read-only users are blocked from every association API with error code **8180**, regardless of any other permission.
- Exactly one of the two mechanisms applies. Either send **viewIds** with 1 to 1000 view identifiers, or set **dissociateAll** to true. An empty or absent **viewIds** with **dissociateAll** off fails with error code **8201**.
- When **dissociateAll** is true, any **viewIds** sent alongside it is ignored and the tag is detached from **every view in the workspace**, including views the caller may not otherwise interact with. No confirmation and no count are returned - check the blast radius with the Get Tagged Views API first.
- The tag survives. Only the links are removed, and the tag can be re-attached later. To remove the tag itself, use the Delete Tag API.
- Detaching a tag from a view that never carried it is not an error. The operation is defined by the end state.
- The error message for **8201** refers to an attribute named removeAll. The attribute this API actually accepts is **dissociateAll**.
- The API returns HTTP 204 No Content with an empty body on success. Confirm with the Get Tagged Views API.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

**None.** This API returns `204 No Content` with an empty body. Confirm with [Get Tagged Views](get-tagged-views.md).

# Examples

## Sample Requests

**Case 1 — detach the tag from named views**

```http
DELETE /restapi/v2/workspaces/320873000000419001/tags/320873000000425158/views HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded
```

```json
{
  "viewIds": ["20867000000038313"]
}
```

**Case 2 — detach the tag from every view, keeping the tag itself**

```json
{
  "dissociateAll": true
}
```

Afterwards [Get Tagged Views](get-tagged-views.md) returns `{"views": []}`, and the tag is still listed by [Get Tags List](get-tags.md).

**Case 3 — `dissociateAll` explicitly off, with named views**

Equivalent to Case 1; useful when the flag is always present in a generated payload.

```json
{
  "viewIds": ["20867000000038313"],
  "dissociateAll": false
}
```

## Sample Responses

**HTTP 204 No Content — the associations were removed**

```
HTTP/1.1 204 No Content
```

**HTTP 200 OK — reading the tagged views afterwards**

```json
{
  "status": "success",
  "summary": "Get tagged views",
  "data": {
    "views": []
  }
}
```

**HTTP 400 Bad Request — neither `viewIds` nor `dissociateAll` was usable**

```json
{
  "status": "failure",
  "summary": "INVALID_CONFIGURATION_REMOVE_VIEWS_LINKED_WITH_TAG",
  "data": {
    "errorCode": 8201,
    "errorMessage": "Invalid configuration. Kindly provide valid viewIds or set 'removeAll' to 'true' to remove all views linked with the tag."
  }
}
```

> The message text names `removeAll`; the attribute this API actually accepts is **`dissociateAll`**.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Remove Tag From Multiple Views](../../../sdk-examples/views-management/tags/remove-tag-from-views.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **The tag survives** | Only the links are removed. This is the difference from [Delete Tag](delete-tag.md), which removes the tag as well. |
| **`dissociateAll` overrides `viewIds`** | When `true`, any `viewIds` sent alongside it is ignored and the tag is stripped from every view. |
| **`dissociateAll: true` has no scope limit** | It reaches every view in the workspace, including views the caller may not otherwise interact with. Confirm the blast radius with [Get Tagged Views](get-tagged-views.md) first. |
| **Detaching a tag that was never attached is not an error** | The operation is defined by the end state, not by how many rows changed. |
| **Administrators only** | Same restriction as [Add Tag To Multiple Views](add-tag-to-views.md); a View Owner must use [Remove Multiple Tags From View](remove-tags-from-view.md). |
| **Read-only users are blocked outright** | `8180`. |
| **No count is returned** | The response does not report how many associations were removed. |
| **Dependency chain:** | [Get Tagged Views](get-tagged-views.md) → `views[].id` → Remove Tag From Multiple Views → [Get Tagged Views](get-tagged-views.md) to verify. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — The workspace does not exist. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin, Organization Admin, or Workspace Admin. | Call as an administrator, or use [Remove Multiple Tags From View](remove-tags-from-view.md) instead. |
| [7390](../../../foundations/error-codes.md#error-7390) | 400 | `WORKSPACE_NOT_BELONGS_TO_ORG` — The workspace does not belong to the organization in `ZANALYTICS-ORGID`. | Send the organization ID that owns the workspace. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing. | Add the header. |
| [8180](../../../foundations/error-codes.md#error-8180) | 403 | `DONT_HAVE_PERMISSION_TO_ASSOCIATE_AND_UNASSOCIATE_TAGS` — The caller is a read-only user. | Associations cannot be changed by read-only users. |
| [8184](../../../foundations/error-codes.md#error-8184) | 403 | `VIEW_OR_TAG_NOT_PRESENT_IN_DB_TO_TAG` — The tag or one of the views does not exist in this workspace. | Verify both sets of IDs. |
| [8201](../../../foundations/error-codes.md#error-8201) | 400 | `INVALID_CONFIGURATION_REMOVE_VIEWS_LINKED_WITH_TAG` — `viewIds` is empty or absent and `dissociateAll` is not `true`. | Send a non-empty `viewIds`, or set `dissociateAll` to `true`. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` was not sent. | Send a CONFIG object. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | `MORE_THAN_MAX_LENGTH` — `viewIds` exceeds 50,000 characters. | Split the batch. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.modeling.delete`. |
| [8547](../../../foundations/error-codes.md#error-8547) | 400 | `ARRAY_SIZE_OUT_OF_RANGE` — `viewIds` exceeds 1000 entries. | Send at most 1000 view IDs, or use `dissociateAll`. |

# Related

- [Tags overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Tags List](get-tags.md), [Get Tagged Views](get-tagged-views.md), [Get View Tags](get-view-tags.md), [Create Tag](create-tag.md), [Update Tag](update-tag.md), [Delete Tag](delete-tag.md), [Add Tag To Multiple Views](add-tag-to-views.md), [Add Multiple Tags To View](add-tags-to-view.md), [Remove Multiple Tags From View](remove-tags-from-view.md).
- [SDK examples](../../../sdk-examples/views-management/tags/remove-tag-from-views.md).
