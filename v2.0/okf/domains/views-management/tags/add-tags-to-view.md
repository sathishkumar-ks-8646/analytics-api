---
type: API Endpoint
title: Add Multiple Tags To View
description: Attaches a batch of existing tags to one view.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - tags
  - post
  - modeling
api:
  operation_id: addTagsToView
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags"
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
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Edit Design permission on the view. Read-only users are rejected with 8180."
  error_codes:
    - 7104
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
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1tags/post"
    config_schema: AddTagsToViewConfig
    response_schema: null
  sdk_examples: "/sdk-examples/views-management/tags/add-tags-to-view.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags`** - Add Multiple Tags To View (Tags / Views Management).

Attaches a batch of **tags** to one view.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace that owns the view and the tags. |
| `<view-id>` | Long | ID of the view to tag. Must belong to `<workspace-id>`. |

From the OpenAPI specification:

Attaches a batch of existing tags to one view.

This is the view-side counterpart of the Add Tag To Multiple Views API, and the one a non-administrator should use - the View Owner and any user with Edit Design permission on the view can call it. Every tag must already exist in the workspace; this API cannot create tags. Tags already on the view are skipped and do not count against the ten-tag ceiling.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `addTagsToView` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with Edit Design permission on the view. Read-only users are rejected with 8180. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1tags/post`; CONFIG schema `AddTagsToViewConfig` |

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
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `tagIds` | JSONArray of Long | **Yes** | — | IDs of the tags to attach, 1–1000 entries. Every tag must already exist in `<workspace-id>`, otherwise `8184`. Duplicates within the array are collapsed. |

> This API **cannot create tags**. It only links existing ones — create them first with [Create Tag](create-tag.md).

## Notes from the OpenAPI specification

- The calling user must be an Account Admin, Organization Admin or Workspace Admin of the workspace, or the View Owner, or any user with Edit Design permission on the view. This is the API to use when the caller is not a workspace administrator.
- Read-only users are blocked from every association API with error code **8180**, even on views they own.
- **tagIds** is mandatory and holds 1 to 1000 tag identifiers, each of which must already exist in the workspace in the request URI. A missing tag fails with error code **8184** - this API cannot create tags, so create them first with the Create Tag API. Duplicate identifiers within the array are collapsed.
- A view can carry at most 10 tags. Tags already attached to the view are skipped and do not count towards the check, so sending a superset of the current tags is safe. A request that would push the view past the ceiling fails with error code **8181** and nothing is written.
- The batch is all-or-nothing. The ten-tag check and the existence checks run before anything is written.
- The call is idempotent per pair. Re-sending the same request returns 204.
- Use the Get View Tags API beforehand to know how many of the ten slots remain.
- The view-id in the request URI must belong to the workspace in the request URI.
- No count is returned. The response does not say how many tags were newly attached. Confirm with the Get View Tags API.
- The API returns HTTP 204 No Content with an empty body on success.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

**None.** This API returns `204 No Content` with an empty body. Confirm with [Get View Tags](get-view-tags.md).

# Examples

## Sample Requests

**Case 1 — attach two existing tags to a view**

```http
POST /restapi/v2/workspaces/320873000000419001/views/20867000000038313/tags HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded
```

```json
{
  "tagIds": [
    "320873000000425158",
    "320873000000419779"
  ]
}
```

**Case 2 — attach a single tag**

```json
{
  "tagIds": ["320873000000421641"]
}
```

## Sample Responses

**HTTP 204 No Content — the tags were attached**

```
HTTP/1.1 204 No Content
```

**HTTP 403 Forbidden — the view would end up with more than ten tags**

```json
{
  "status": "failure",
  "summary": "TAG_COUNT_EXCEEDS",
  "data": {
    "errorCode": 8181,
    "errorMessage": "Tags on the views [\"20867000000038313\"] exceeds allowed tag limit."
  }
}
```

**HTTP 403 Forbidden — one of the tag IDs does not exist**

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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Add Multiple Tags To View](../../../sdk-examples/views-management/tags/add-tags-to-view.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **It is idempotent per pair** | Tags already on the view are skipped, not duplicated or rejected. Re-sending the same request returns `204`. |
| **Already-attached tags do not count against the ceiling** | Sending ten tags to a view that already carries five of them adds only the five new ones, and passes the limit check. |
| **The batch is all-or-nothing** | The ten-tag check and the existence checks run before anything is written. |
| **This is the API a non-admin should use** | The View Owner and anyone with Edit Design permission on the view can call it, which is not true of [Add Tag To Multiple Views](add-tag-to-views.md). |
| **Read-only users are blocked outright** | `8180`, even if they own the view. |
| **Duplicate IDs in `tagIds` are collapsed** | Sending the same tag twice counts once. |
| **No count is returned** | The response does not say how many tags were newly attached. |
| **Dependency chain:** | [Get Tags List](get-tags.md) → `tagIds`; [Get View List](../view-operations/get-views.md) → `<view-id>` → Add Multiple Tags To View → [Get View Tags](get-view-tags.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — The view does not exist. | Verify `<view-id>` with [Get View List](../view-operations/get-views.md). |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller lacks Edit Design permission on the view, or the view does not belong to `<workspace-id>`. | Call as an administrator, the View Owner, or a user with Edit Design permission. |
| [7390](../../../foundations/error-codes.md#error-7390) | 400 | `WORKSPACE_NOT_BELONGS_TO_ORG` — The workspace does not belong to the organization in `ZANALYTICS-ORGID`. | Send the organization ID that owns the workspace. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — `tagIds` is missing. | Send a `tagIds` array. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing. | Add the header. |
| [8180](../../../foundations/error-codes.md#error-8180) | 403 | `DONT_HAVE_PERMISSION_TO_ASSOCIATE_AND_UNASSOCIATE_TAGS` — The caller is a read-only user. | Associations cannot be changed by read-only users. |
| [8181](../../../foundations/error-codes.md#error-8181) | 403 | `TAG_COUNT_EXCEEDS` — The view would exceed 10 tags. | Remove some tags first, or send fewer. |
| [8184](../../../foundations/error-codes.md#error-8184) | 403 | `VIEW_OR_TAG_NOT_PRESENT_IN_DB_TO_TAG` — One of the tags does not exist in this workspace. | Verify the IDs with [Get Tags List](get-tags.md). Create missing tags with [Create Tag](create-tag.md). |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` was not sent, or `tagIds` is missing. | Send a CONFIG object containing `tagIds`. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | `MORE_THAN_MAX_LENGTH` — `tagIds` exceeds 50,000 characters. | Split the batch. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.modeling.create`. |
| [8547](../../../foundations/error-codes.md#error-8547) | 400 | `ARRAY_SIZE_OUT_OF_RANGE` — `tagIds` is empty or exceeds 1000 entries. | Send between 1 and 1000 tag IDs. |

# Related

- [Tags overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Tags List](get-tags.md), [Get Tagged Views](get-tagged-views.md), [Get View Tags](get-view-tags.md), [Create Tag](create-tag.md), [Update Tag](update-tag.md), [Delete Tag](delete-tag.md), [Add Tag To Multiple Views](add-tag-to-views.md), [Remove Tag From Multiple Views](remove-tag-from-views.md), [Remove Multiple Tags From View](remove-tags-from-view.md).
- [SDK examples](../../../sdk-examples/views-management/tags/add-tags-to-view.md).
