---
type: API Endpoint
title: Update Tag
description: "Renames a tag, recolours it, or both."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - tags
  - put
  - modeling
api:
  operation_id: updateTag
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}"
  domain: views-management
  group: tags
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace."
  error_codes:
    - 7103
    - 7301
    - 7390
    - 8083
    - 8174
    - 8179
    - 8182
    - 8185
    - 8187
    - 8504
    - 8507
    - 8509
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1tags~1{tag-id}/put"
    config_schema: UpdateTagConfig
    response_schema: null
  sdk_examples: "/sdk-examples/views-management/tags/update-tag.md"
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

**PUT `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}`** - Update Tag (Tags / Views Management).

Renames a tag, recolours it, or both.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace that owns the tag. |
| `<tag-id>` | Long | ID of the tag to update. Must exist in `<workspace-id>`, otherwise `8187`. |

From the OpenAPI specification:

Renames a tag, recolours it, or both.

This is a genuine partial update - the attribute that is omitted keeps its stored value. Associations are never touched: every view tagged before the update is still tagged after it.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `updateTag` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1tags~1{tag-id}/put`; CONFIG schema `UpdateTagConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.update`. See [Authentication](../../../foundations/authentication.md). |
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
| `name` | String | Conditional | unchanged | New display name, 1–100 characters. Must be unique within the workspace, otherwise `8174`. Omit to leave the name unchanged. |
| `colorCode` | String | Conditional | unchanged | New hex colour, `#RRGGBB` or `#RGB`. Omit to leave the colour unchanged. |

> **At least one of the two must be present.** Sending a CONFIG with neither — or with both empty — fails with [`8182`](../../../foundations/error-codes.md#error-8182). This is a genuine partial update: the attribute you omit is preserved, not reset.

## Notes from the OpenAPI specification

- The calling user must be an Account Admin, Organization Admin or Workspace Admin of the workspace. Any other user fails with error code **8179**.
- At least one of **name** or **colorCode** must be present. A CONFIG carrying neither, or both empty, fails with error code **8182**. Despite the wording of its message, **8182** means there is nothing to update - a real permission failure surfaces as **8179**.
- This is a genuine partial update. The attribute that is omitted is preserved, not reset - unlike most other V2 update APIs, which replace the whole definition.
- The new **name** is limited to 100 characters and must be unique within the workspace - renaming onto an existing name fails with error code **8174**. Renaming a tag to the name it already holds succeeds.
- **colorCode** must be a hex colour in the form **#RRGGBB** or **#RGB**, otherwise error code **8509**.
- Associations are untouched. Every view tagged before the update is still tagged after it, because the link is by identifier.
- The tag-id in the request URI must belong to the workspace in the request URI. Tags are workspace-scoped, and a tag from another workspace fails with error code **8187**.
- The API returns HTTP 204 No Content with an empty body on success. Read the new values back with the Get Tags List API.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

**None.** This API returns `204 No Content` with an empty body. Confirm the change with [Get Tags List](get-tags.md).

# Examples

## Sample Requests

**Case 1 — rename and recolour together**

```http
PUT /restapi/v2/workspaces/320873000000419001/tags/320873000000425158 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded
```

```json
{
  "name": "Tag_AccountAdmin_1_Updated",
  "colorCode": "#e72d35"
}
```

**Case 2 — recolour only, keeping the name**

```json
{
  "colorCode": "#1da043"
}
```

**Case 3 — rename only, keeping the colour**

```json
{
  "name": "Finance_Archive"
}
```

## Sample Responses

**HTTP 204 No Content — the tag was updated**

```
HTTP/1.1 204 No Content
```

There is no response body. Read the new values back with [Get Tags List](get-tags.md).

**HTTP 400 Bad Request — neither attribute was supplied**

```json
{
  "status": "failure",
  "summary": "CANNOT_UPDATE_THE_TAG",
  "data": {
    "errorCode": 8182,
    "errorMessage": "You don't have permission to update a tag."
  }
}
```

Despite the wording of the message, this code is raised when the CONFIG carries nothing to change.

**HTTP 400 Bad Request — the tag does not exist**

```json
{
  "status": "failure",
  "summary": "TAG_NOT_PRESENT_IN_DB",
  "data": {
    "errorCode": 8187,
    "errorMessage": "Tag is not present in db to delete/update."
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Update Tag](../../../sdk-examples/views-management/tags/update-tag.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **It is a genuine partial update** | Omitted attributes keep their stored values. This is the opposite of most V2 update APIs, which replace the whole definition. |
| **Associations are untouched** | Every view tagged before the update is still tagged after it. Renaming is safe for existing links. |
| **The name uniqueness check still applies** | Renaming onto an existing name fails with `8174`. |
| **`8182` means "nothing to update", not a permission problem** | Its message text reads like a permission error, but a permission failure surfaces as `8179`. Check whether your CONFIG actually contained `name` or `colorCode`. |
| **Renaming to the current name is accepted** | It is not treated as a duplicate of itself. |
| **There is no bulk update** | One tag per call. |
| **Dependency chain:** | [Get Tags List](get-tags.md) or [Create Tag](create-tag.md) → `<tag-id>` → Update Tag → [Get Tags List](get-tags.md) to verify. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — The workspace does not exist. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller cannot access the workspace. | Ensure the workspace is shared with the calling user. |
| [7390](../../../foundations/error-codes.md#error-7390) | 400 | `WORKSPACE_NOT_BELONGS_TO_ORG` — The workspace does not belong to the organization in `ZANALYTICS-ORGID`. | Send the organization ID that owns the workspace. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing. | Add the header. |
| [8174](../../../foundations/error-codes.md#error-8174) | 403 | `DUPLICATE_TAG_NAME_FOUND` — Another tag in the workspace already uses this name. | Choose a different name. |
| [8179](../../../foundations/error-codes.md#error-8179) | 403 | `DONT_HAVE_PERMISSION_TO_CREATE_TAGS` — The caller is not an Account Admin, Organization Admin, or Workspace Admin. | Call as an administrator of the workspace. |
| [8182](../../../foundations/error-codes.md#error-8182) | 403 | `CANNOT_UPDATE_THE_TAG` — The CONFIG contained neither `name` nor `colorCode`. | Send at least one of the two. |
| [8185](../../../foundations/error-codes.md#error-8185) | 400 | `CANNOT_DELETE_OR_UPDATE_TAG` — The update matched no row. | Verify `<tag-id>` with [Get Tags List](get-tags.md). |
| [8187](../../../foundations/error-codes.md#error-8187) | 400 | `TAG_NOT_PRESENT_IN_DB` — The tag does not exist in this workspace. | Verify `<tag-id>` with [Get Tags List](get-tags.md). |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — `CONFIG` was not sent. | Send a CONFIG object. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | `MORE_THAN_MAX_LENGTH` — `name` exceeds 100 characters. | Shorten the name. |
| [8509](../../../foundations/error-codes.md#error-8509) | 400 | `PATTERN_NOT_MATCHED` — `colorCode` is not a valid hex colour. | Send `#RRGGBB` or `#RGB`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.modeling.update`. |

# Related

- [Tags overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Tags List](get-tags.md), [Get Tagged Views](get-tagged-views.md), [Get View Tags](get-view-tags.md), [Create Tag](create-tag.md), [Delete Tag](delete-tag.md), [Add Tag To Multiple Views](add-tag-to-views.md), [Remove Tag From Multiple Views](remove-tag-from-views.md), [Add Multiple Tags To View](add-tags-to-view.md), [Remove Multiple Tags From View](remove-tags-from-view.md).
- [SDK examples](../../../sdk-examples/views-management/tags/update-tag.md).
