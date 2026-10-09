---
type: API Endpoint
title: Add Tag To Multiple Views
description: Attaches one tag to a batch of views in the workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - tags
  - post
  - modeling
api:
  operation_id: addTagToViews
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views"
  domain: views-management
  group: tags
  oauth_scopes:
    - ZohoAnalytics.modeling.create
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
    - 8079
    - 8083
    - 8180
    - 8181
    - 8184
    - 8504
    - 8507
    - 8535
    - 8547
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1tags~1{tag-id}~1views/post"
    config_schema: AddTagToViewsConfig
    response_schema: null
  sdk_examples: "/sdk-examples/views-management/tags/add-tag-to-views.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views`** - Add Tag To Multiple Views (Tags / Views Management).

Attaches **one tag** to a batch of views.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace that owns both the tag and the views. |
| `<tag-id>` | Long | ID of the tag to attach. Must exist in `<workspace-id>`, otherwise `8184`. |

From the OpenAPI specification:

Attaches one tag to a batch of views in the workspace.

The batch is validated as a whole - workspace membership, tag existence and the ten-tag ceiling of every view - before anything is written, so one bad view means no view gets tagged. Pairs that already exist are skipped rather than rejected, which makes the call safe to retry. This is the tag-side counterpart of the Add Multiple Tags To View API and, unlike it, requires workspace administration.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `addTagToViews` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. The View Owner alone does not qualify. Read-only users are rejected with 8180. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1tags~1{tag-id}~1views/post`; CONFIG schema `AddTagToViewsConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.create`. See [Authentication](../../../foundations/authentication.md). |
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
| `viewIds` | JSONArray of Long | **Yes** | — | IDs of the views to attach the tag to, 1–1000 entries. Every ID must belong to `<workspace-id>`, otherwise `8184`. Duplicates within the array are collapsed. |

## Notes from the OpenAPI specification

- The calling user must be an Account Admin, Organization Admin or Workspace Admin of the workspace. A View Owner who is not a Workspace Admin cannot use this API - even to tag their own view - and must use the Add Multiple Tags To View API instead.
- Read-only users are blocked from every association API with error code **8180**, regardless of any other permission.
- **viewIds** is mandatory and holds 1 to 1000 view identifiers, each of which must belong to the workspace in the request URI. Duplicate identifiers within the array are collapsed.
- A view can carry at most 10 tags, counted across all its tags rather than per request. A view that would exceed the ceiling fails the whole batch with error code **8181**, and the error message names the offending views.
- The batch is all-or-nothing. Every check runs across the whole batch before anything is written, so one bad view identifier or one view at the ceiling means nothing is written for any view.
- The call is idempotent per pair. A (view, tag) pair that already exists is skipped rather than duplicated or rejected, so re-sending the same request is safe and still returns 204.
- Error code **8184** covers two different mistakes - the tag does not exist in the workspace, or one of the views does not. Verify both with the Get Tags List and Get View List APIs.
- No count is returned. The response does not say how many associations were new versus already present. Confirm with the Get Tagged Views API.
- The API returns HTTP 204 No Content with an empty body on success.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

**None.** This API returns `204 No Content` with an empty body. Confirm with [Get Tagged Views](get-tagged-views.md).

# Examples

## Sample Requests

**Case 1 — attach the tag to one view**

```http
POST /restapi/v2/workspaces/320873000000419001/tags/320873000000425158/views HTTP/1.1
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

**Case 2 — attach it across a mixed batch of view types**

One call can span tables, dashboards, charts, and pivots.

```json
{
  "viewIds": [
    "20867000000038313",
    "20867000000038314",
    "20867000000038319",
    "20867000000038322"
  ]
}
```

## Sample Responses

**HTTP 204 No Content — the tag was attached**

```
HTTP/1.1 204 No Content
```

**HTTP 403 Forbidden — a view would exceed its ten-tag ceiling**

```json
{
  "status": "failure",
  "summary": "TAG_COUNT_EXCEEDS",
  "data": {
    "errorCode": 8181,
    "errorMessage": "Tags on the views [\"20867000000038314\"] exceeds allowed tag limit."
  }
}
```

The message names the offending views. Nothing was written for any view in the batch.

**HTTP 403 Forbidden — a read-only user attempted the call**

```json
{
  "status": "failure",
  "summary": "DONT_HAVE_PERMISSION_TO_ASSOCIATE_AND_UNASSOCIATE_TAGS",
  "data": {
    "errorCode": 8180,
    "errorMessage": "You don't have permission to associate/unassociate a tag."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Add Tag To Multiple Views](../../../sdk-examples/views-management/tags/add-tag-to-views.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **It is idempotent per pair** | A `(view, tag)` pair that already exists is skipped rather than duplicated or rejected. Re-sending the same request is safe and still returns `204`. |
| **Duplicate IDs in `viewIds` are collapsed** | Sending the same view twice in one array counts once. |
| **The batch is all-or-nothing** | Validation — workspace membership, tag existence, and the ten-tag ceiling — runs across the whole batch before anything is written. One bad view ID means no view gets tagged. |
| **Administrators only** | Unlike its view-side counterpart [Add Multiple Tags To View](add-tags-to-view.md), a View Owner cannot call this. See [The Two Sides of an Association](overview.md#the-two-sides-of-an-association). |
| **Read-only users are blocked outright** | `8180`, regardless of any other permission. |
| **`8184` covers two different mistakes** | Either the tag does not exist in the workspace, or one of the `viewIds` does not. The message does not distinguish them — verify both with [Get Tags List](get-tags.md) and [Get View List](../view-operations/get-views.md). |
| **No count is returned** | The response does not say how many associations were new versus already present. |
| **Dependency chain:** | [Create Tag](create-tag.md) → `<tag-id>`; [Get View List](../view-operations/get-views.md) → `viewIds` → Add Tag To Multiple Views → [Get Tagged Views](get-tagged-views.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — The workspace does not exist. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin, Organization Admin, or Workspace Admin. | Call as an administrator, or use [Add Multiple Tags To View](add-tags-to-view.md) instead. |
| [7390](../../../foundations/error-codes.md#error-7390) | 400 | `WORKSPACE_NOT_BELONGS_TO_ORG` — The workspace does not belong to the organization in `ZANALYTICS-ORGID`. | Send the organization ID that owns the workspace. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — `viewIds` is missing. | Send a `viewIds` array. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing. | Add the header. |
| [8180](../../../foundations/error-codes.md#error-8180) | 403 | `DONT_HAVE_PERMISSION_TO_ASSOCIATE_AND_UNASSOCIATE_TAGS` — The caller is a read-only user. | Associations cannot be changed by read-only users. |
| [8181](../../../foundations/error-codes.md#error-8181) | 403 | `TAG_COUNT_EXCEEDS` — One or more views would exceed 10 tags. The message lists them. | Remove tags from those views first, or drop them from the batch. |
| [8184](../../../foundations/error-codes.md#error-8184) | 403 | `VIEW_OR_TAG_NOT_PRESENT_IN_DB_TO_TAG` — The tag or one of the views does not exist in this workspace. | Verify both sets of IDs. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` was not sent, or `viewIds` is missing. | Send a CONFIG object containing `viewIds`. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | `MORE_THAN_MAX_LENGTH` — `viewIds` exceeds 50,000 characters. | Split the batch. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.modeling.create`. |
| [8547](../../../foundations/error-codes.md#error-8547) | 400 | `ARRAY_SIZE_OUT_OF_RANGE` — `viewIds` is empty or exceeds 1000 entries. | Send between 1 and 1000 view IDs. |

# Related

- [Tags overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Tags List](get-tags.md), [Get Tagged Views](get-tagged-views.md), [Get View Tags](get-view-tags.md), [Create Tag](create-tag.md), [Update Tag](update-tag.md), [Delete Tag](delete-tag.md), [Remove Tag From Multiple Views](remove-tag-from-views.md), [Add Multiple Tags To View](add-tags-to-view.md), [Remove Multiple Tags From View](remove-tags-from-view.md).
- [SDK examples](../../../sdk-examples/views-management/tags/add-tag-to-views.md).
