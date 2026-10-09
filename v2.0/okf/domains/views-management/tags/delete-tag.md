---
type: API Endpoint
title: Delete Tag
description: Deletes a tag together with every association it has.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - tags
  - delete
  - modeling
api:
  operation_id: deleteTag
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}"
  domain: views-management
  group: tags
  oauth_scopes:
    - ZohoAnalytics.modeling.delete
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace."
  error_codes:
    - 7103
    - 7301
    - 7390
    - 8083
    - 8179
    - 8184
    - 8185
    - 8535
  openapi:
    file: "/references/openapi/views-management-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1tags~1{tag-id}/delete"
    config_schema: null
    response_schema: null
  sdk_examples: "/sdk-examples/views-management/tags/delete-tag.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}`** - Delete Tag (Tags / Views Management).

Deletes a tag and every association it has.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `<workspace-id>` | Long | ID of the workspace that owns the tag. |
| `<tag-id>` | Long | ID of the tag to delete. Must exist in `<workspace-id>`. |

From the OpenAPI specification:

Deletes a tag together with every association it has.

The views that carried the tag are untouched - only the label disappears from them. There is no undo, and re-creating the same name afterwards produces a different tag with a new identifier and none of the old associations. To clear a tag's links while keeping the tag, use the Remove Tag From Multiple Views API with dissociateAll instead.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deleteTag` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingdelete) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the specified workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 204 with no body |
| OpenAPI | [`views-management-grouped-api.json`](../../../references/openapi/views-management-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1tags~1{tag-id}/delete` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.delete`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{tag-id}` | string | ID of the tag. | [How to obtain](../../../foundations/identifiers.md#tag-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

## Notes from the OpenAPI specification

- The calling user must be an Account Admin, Organization Admin or Workspace Admin of the workspace. Any other user fails with error code **8179**.
- The delete cascades to every association. The tag is silently removed from every view it labelled; the views themselves are untouched.
- The operation is irreversible, and the response does not report how many associations were removed. Call the Get Tagged Views API first to see what will be unlinked.
- Re-creating the same name afterwards produces a different tag with a new **tagId** and none of the old associations.
- To keep the tag but clear its links, use the Remove Tag From Multiple Views API with **dissociateAll** set to true instead.
- The tag-id in the request URI must belong to the workspace in the request URI. Tags are workspace-scoped, and a tag from another workspace fails with error code **8184**.
- One tag is deleted per call. There is no bulk-delete variant.
- The API returns HTTP 204 No Content with an empty body on success. Confirm with the Get Tags List API.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

**None.** This API returns `204 No Content` with an empty body. Confirm with [Get Tags List](get-tags.md).

# Examples

## Sample Requests

```http
DELETE /restapi/v2/workspaces/320873000000419001/tags/320873000000425158 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

There is nothing else to send.

## Sample Responses

**HTTP 204 No Content — the tag was deleted**

```
HTTP/1.1 204 No Content
```

**HTTP 200 OK — reading the tag list afterwards**

```json
{
  "status": "success",
  "summary": "Get tags",
  "data": {
    "tags": []
  }
}
```

**HTTP 403 Forbidden — the tag does not exist**

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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Delete Tag](../../../sdk-examples/views-management/tags/delete-tag.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Behaviour | Detail |
|-----------|--------|
| **It cascades to every association** | Deleting a tag silently removes it from every view it labelled. The views themselves are untouched — only the label disappears. |
| **There is no confirmation and no undo** | The response does not report how many associations were removed, and the tag cannot be restored. Read [Get Tagged Views](get-tagged-views.md) first if you need to know the blast radius. |
| **Re-creating the name afterwards produces a different tag** | The new tag gets a new `tagId` and carries none of the old associations. |
| **To keep the tag but clear its links** | Use [Remove Tag From Multiple Views](remove-tag-from-views.md) with `dissociateAll: true` instead. It removes every association without deleting the tag. |
| **One tag per call** | There is no bulk-delete variant. |
| **Dependency chain:** | [Get Tags List](get-tags.md) → `<tag-id>` → (optionally [Get Tagged Views](get-tagged-views.md) to see what will be unlinked) → Delete Tag. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — The workspace does not exist. | Verify `<workspace-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller cannot access the workspace. | Ensure the workspace is shared with the calling user. |
| [7390](../../../foundations/error-codes.md#error-7390) | 400 | `WORKSPACE_NOT_BELONGS_TO_ORG` — The workspace does not belong to the organization in `ZANALYTICS-ORGID`. | Send the organization ID that owns the workspace. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing. | Add the header. |
| [8179](../../../foundations/error-codes.md#error-8179) | 403 | `DONT_HAVE_PERMISSION_TO_CREATE_TAGS` — The caller is not an Account Admin, Organization Admin, or Workspace Admin. | Call as an administrator of the workspace. |
| [8184](../../../foundations/error-codes.md#error-8184) | 403 | `VIEW_OR_TAG_NOT_PRESENT_IN_DB_TO_TAG` — The tag does not exist in this workspace. | Verify `<tag-id>` with [Get Tags List](get-tags.md). |
| [8185](../../../foundations/error-codes.md#error-8185) | 400 | `CANNOT_DELETE_OR_UPDATE_TAG` — The delete matched no row. | Verify `<tag-id>` with [Get Tags List](get-tags.md). |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token carrying `ZohoAnalytics.modeling.delete`. |

# Related

- [Tags overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Views Management](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Tags List](get-tags.md), [Get Tagged Views](get-tagged-views.md), [Get View Tags](get-view-tags.md), [Create Tag](create-tag.md), [Update Tag](update-tag.md), [Add Tag To Multiple Views](add-tag-to-views.md), [Remove Tag From Multiple Views](remove-tag-from-views.md), [Add Multiple Tags To View](add-tags-to-view.md), [Remove Multiple Tags From View](remove-tags-from-view.md).
- [SDK examples](../../../sdk-examples/views-management/tags/delete-tag.md).
