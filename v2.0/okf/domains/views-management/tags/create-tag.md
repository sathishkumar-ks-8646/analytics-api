---
type: API Endpoint
title: Create Tag
description: Creates one tag in the workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/tags"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - tags
  - post
  - modeling
api:
  operation_id: createTag
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/tags"
  domain: views-management
  group: tags
  oauth_scopes:
    - ZohoAnalytics.modeling.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace."
  error_codes:
    - 7103
    - 7301
    - 7390
    - 8079
    - 8083
    - 8174
    - 8179
    - 8504
    - 8507
    - 8509
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1tags/post"
    config_schema: CreateTagConfig
    response_schema: CreateTagResponse
  sdk_examples: "/sdk-examples/views-management/tags/create-tag.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/tags`** - Create Tag (Tags / Views Management).

Creates one tag in the workspace.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace the tag is created in. |

From the OpenAPI specification:

Creates one tag in the workspace.

Both name and colorCode are mandatory. A created tag labels nothing until it is attached to views with the Add Tag To Multiple Views or Add Multiple Tags To View API. The tag name must be unique within the workspace - the same name may exist in another workspace as an unrelated tag.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createTag` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/tags` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1tags/post`; CONFIG schema `CreateTagConfig`; response schema `CreateTagResponse` |

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

## CONFIG Parameters

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | String | **Yes** | — | Display name of the tag, 1–100 characters. Must be unique within the workspace, otherwise `8174`. |
| `colorCode` | String | **Yes** | — | Hex colour, `#RRGGBB` or `#RGB`. See [The `colorCode` Attribute](overview.md#the-colorcode-attribute). |

## Notes from the OpenAPI specification

- The calling user must be an Account Admin, Organization Admin or Workspace Admin of the workspace. Any other user fails with error code **8179**.
- Both **name** and **colorCode** are mandatory, unlike the Update Tag API which accepts either one alone. A missing attribute fails with error code **8079**.
- **name** is limited to 100 characters and must be unique within the workspace. A duplicate fails with error code **8174** - this API is not an upsert and does not return the existing tag. Read the Get Tags List API first if a script must be re-runnable.
- **colorCode** must be a hex colour in the form **#RRGGBB** or **#RGB**, case-insensitive. Colour keywords, rgb() notation, values with an alpha channel and values without the leading # fail with error code **8509**. Colours need not be unique.
- The response key is **tagId**. The read APIs return the same value as **id** - the two names refer to the same identifier.
- A created tag labels nothing. Creation and association are separate steps - follow with the Add Tag To Multiple Views or Add Multiple Tags To View API.
- One tag is created per call. There is no bulk-create variant.
- The success **summary** is "Create Tag" with a capital T, unlike the lower-case summaries of the read APIs. Do not branch on summary text.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | `"success"` on success. |
| `summary` | String | `"Create Tag"` — note the capital `T`, unlike the lower-case summaries of the read APIs. |
| `data` | Object | Wrapper. |
| `data.tagId` | String | ID of the new tag, **as a string**. This is the only place it is returned; capture it. It becomes `<tag-id>` for [Get Tagged Views](get-tagged-views.md), [Update Tag](update-tag.md), [Delete Tag](delete-tag.md), [Add Tag To Multiple Views](add-tag-to-views.md), and [Remove Tag From Multiple Views](remove-tag-from-views.md), and a `tagIds` entry for [Add Multiple Tags To View](add-tags-to-view.md) and [Remove Multiple Tags From View](remove-tags-from-view.md). |

# Examples

## Sample Requests

**Case 1 — a tag with a six-digit colour**

```http
POST /restapi/v2/workspaces/320873000000419001/tags HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded
```

```json
{
  "name": "Tag_AccountAdmin_1",
  "colorCode": "#55acee"
}
```

**Case 2 — a second tag in the same workspace**

Names must differ; colours need not.

```json
{
  "name": "Tag_AccountAdmin_2",
  "colorCode": "#f5a623"
}
```

**Case 3 — the three-digit colour form**

```json
{
  "name": "Finance",
  "colorCode": "#1da"
}
```

## Sample Responses

**HTTP 200 OK — the tag was created**

```json
{
  "status": "success",
  "summary": "Create Tag",
  "data": {
    "tagId": "20867000000038794"
  }
}
```

**HTTP 403 Forbidden — the name is already taken in this workspace**

```json
{
  "status": "failure",
  "summary": "DUPLICATE_TAG_NAME_FOUND",
  "data": {
    "errorCode": 8174,
    "errorMessage": "Duplicate tag found. Kindly Check the tags given."
  }
}
```

**HTTP 403 Forbidden — the caller is not an administrator**

```json
{
  "status": "failure",
  "summary": "DONT_HAVE_PERMISSION_TO_CREATE_TAGS",
  "data": {
    "errorCode": 8179,
    "errorMessage": "You don't have permission to create new tag."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Tag](../../../sdk-examples/views-management/tags/create-tag.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **The response key is `tagId`, not `id`** | The read APIs return the same value as `tags[].id`. The two names refer to the same thing. |
| **One tag per call** | There is no bulk-create variant. Creating twenty tags takes twenty calls. |
| **A created tag labels nothing** | Creation and association are separate steps. Follow with [Add Tag To Multiple Views](add-tag-to-views.md) or [Add Multiple Tags To View](add-tags-to-view.md). |
| **Name uniqueness is per workspace** | The same name may exist in two different workspaces as two unrelated tags. |
| **It is not an upsert** | Re-creating an existing name fails with `8174` rather than returning the existing tag. To find out whether a name is taken, read [Get Tags List](get-tags.md) first. |
| **Both attributes are mandatory** | Unlike [Update Tag](update-tag.md), which accepts either one alone. |
| **Dependency chain:** | Create Tag → `data.tagId` → [Add Tag To Multiple Views](add-tag-to-views.md) → [Get Tagged Views](get-tagged-views.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — The workspace does not exist. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller cannot access the workspace. | Ensure the workspace is shared with the calling user. |
| [7390](../../../foundations/error-codes.md#error-7390) | 400 | `WORKSPACE_NOT_BELONGS_TO_ORG` — The workspace does not belong to the organization in `ZANALYTICS-ORGID`. | Send the organization ID that owns the workspace. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — `name` or `colorCode` is missing. | The message names the attribute; both are mandatory. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing. | Add the header. |
| [8174](../../../foundations/error-codes.md#error-8174) | 403 | `DUPLICATE_TAG_NAME_FOUND` — A tag with this name already exists in the workspace. | Choose a different name, or reuse the existing tag's ID. |
| [8179](../../../foundations/error-codes.md#error-8179) | 403 | `DONT_HAVE_PERMISSION_TO_CREATE_TAGS` — The caller is not an Account Admin, Organization Admin, or Workspace Admin. | Call as an administrator of the workspace. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` was not sent. | Send a CONFIG object containing `name` and `colorCode`. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | `MORE_THAN_MAX_LENGTH` — `name` exceeds 100 characters. | Shorten the name. |
| [8509](../../../foundations/error-codes.md#error-8509) | 400 | `PATTERN_NOT_MATCHED` — `colorCode` is not a valid hex colour. | Send `#RRGGBB` or `#RGB`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.modeling.create`. |

# Related

- [Tags overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Tags List](get-tags.md), [Get Tagged Views](get-tagged-views.md), [Get View Tags](get-view-tags.md), [Update Tag](update-tag.md), [Delete Tag](delete-tag.md), [Add Tag To Multiple Views](add-tag-to-views.md), [Remove Tag From Multiple Views](remove-tag-from-views.md), [Add Multiple Tags To View](add-tags-to-view.md), [Remove Multiple Tags From View](remove-tags-from-view.md).
- [SDK examples](../../../sdk-examples/views-management/tags/create-tag.md).
