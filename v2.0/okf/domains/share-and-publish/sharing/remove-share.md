---
type: API Endpoint
title: Remove Shared Views
description: "Removes an existing share of one or more views from a set of users and/or groups, or removes all of a user's/group's shared views in the workspace at once."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/share"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - sharing
  - delete
  - share
api:
  operation_id: removeShare
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/share"
  domain: share-and-publish
  group: sharing
  oauth_scopes:
    - ZohoAnalytics.share.delete
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "For removing specific viewIds: the authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Share permission on the specified views. For removeAllViews: true: the authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the workspace — this bulk option is restricted to workspace owners."
  error_codes:
    - 7301
    - 7533
    - 8031
    - 8032
    - 8080
    - 8105
    - 8150
  openapi:
    file: "/references/openapi/share-publish-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1share/delete"
    config_schema: RemoveShareConfig
    response_schema: null
  sdk_examples: "/sdk-examples/share-and-publish/sharing/remove-share.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/share-publish-grouped-api.json"
    title: OpenAPI 3 specification - share-publish-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**DELETE `/restapi/v2/workspaces/{workspace-id}/share`** - Remove Shared Views (Sharing / Share & Publish).

Removes an existing share of one or more views from a set of users and/or groups, or removes **all** of a user's/group's shared views in the workspace at once.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `removeShare` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/share` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.share.delete`](../../../foundations/oauth-scopes.md#zohoanalyticssharedelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | For removing specific viewIds: the authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Share permission on the specified views. For removeAllViews: true: the authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin of the workspace — this bulk option is restricted to workspace owners. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1share/delete`; CONFIG schema `RemoveShareConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.share.delete`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `emailIds` | JSONArray of String | No* | — | Email addresses whose share should be removed. |
| `groupIds` | JSONArray of String/Long | No* | — | Group IDs whose share should be removed. |
| `viewIds` | JSONArray of String/Long | Conditionally required | — | IDs of the views to unshare. **Required when `removeAllViews` is `false`/omitted; must be omitted (empty) when `removeAllViews` is `true`** (error 8105 `REMOVESHARE_ALL_VIEWS_PRESENT` if both are supplied together). |
| `removeAllViews` | Boolean | No | `false` | If `true`, removes **every** view shared to the specified `emailIds`/`groupIds` in this workspace, instead of only the views in `viewIds`. |
| `domainName` | String | No | — | Client Portal/White Label domain to scope this removal to. |

\* At least one of `emailIds` or `groupIds` is required, identifying whose share(s) to remove.

## Notes from the OpenAPI specification

- Specify either `viewIds` to remove the sharing of particular views, or set `removeAllViews` to true to remove every view shared with the specified users.
- `domainName` is required only when the shared views have to be removed from a white label domain.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Remove a specific view's share from a user**

```http
DELETE /restapi/v2/workspaces/137687000271334001/share HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "emailIds": ["jane.doe@example.com"],
    "viewIds": ["137687000006991601"]
}
```

**Case 2 — Remove all views shared to a group (Workspace Admin only)**

```http
DELETE /restapi/v2/workspaces/137687000271334001/share HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "groupIds": ["137687000006991700"],
    "removeAllViews": true
}
```

**Case 3 — Client Portal: remove a specific view's share from a portal-domain user**

```http
DELETE /restapi/v2/workspaces/137687000271334009/share HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "emailIds": ["client.user@portalcustomer.com"],
    "viewIds": ["137687000006991777"],
    "domainName": "portal.customdomain.com"
}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Remove Shared Views](../../../sdk-examples/share-and-publish/sharing/remove-share.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Remove Shared Views returns a bare HTTP `204 No Content` on success. |
| **`viewIds` and `removeAllViews` are mutually exclusive** | Supplying `viewIds` together with `removeAllViews: true` is rejected (error 8105); supplying neither `viewIds` nor `removeAllViews: true` is also rejected (`REMOVESHARE_API_PARAMS`, error 8031). |
| **`removeAllViews` requires ownership** | Removing *all* of a user's/group's shares workspace-wide is a bulk administrative action restricted to the Workspace Admin (or Account/Organization Admin) — a regular user with only Share permission on individual views cannot use this flag. |
| **Not shared is not an error for bulk removal** | For `removeAllViews: true`, users/groups with no existing shares are simply skipped; for specific `viewIds`, unsharing a view/user combination that was never shared returns error 8032/8150. |
| **Dependency** | [Get Shared Details](get-shared-details-for-views.md) → confirm the share exists → Remove Shared Views. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — User lacks Share permission on the targeted view(s), or attempted `removeAllViews: true` without Workspace Admin privileges. | Ensure the user is an Account Admin, Organization Admin, or Workspace Admin (required for `removeAllViews`), or has Share permission on the specified views. |
| [7533](../../../foundations/error-codes.md#error-7533) | 400 | `CANNOT_SHARE_OBJECT_TO_GROUP` — The view's type does not support group-based sharing/unsharing. | Only applicable to user-based (`emailIds`) removal for this view type. |
| [8031](../../../foundations/error-codes.md#error-8031) | 400 | `REMOVESHARE_API_PARAMS` — Neither `viewIds` nor `removeAllViews: true` was supplied. | Supply either a `viewIds` array or set `removeAllViews: true`. |
| [8032](../../../foundations/error-codes.md#error-8032) | 400 | `VIEW_NOT_SHARED` — The specified view is not currently shared with this user. | Verify the share exists via Get Shared Details before removing. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — CONFIG is malformed or missing a required field. | Validate the CONFIG JSON against the parameter table above. |
| [8105](../../../foundations/error-codes.md#error-8105) | 400 | `REMOVESHARE_ALL_VIEWS_PRESENT` — Both `viewIds` and `removeAllViews: true` were supplied together. | Supply only one of the two — `viewIds` for a targeted removal, or `removeAllViews: true` alone for a bulk removal. |
| [8150](../../../foundations/error-codes.md#error-8150) | 400 | `VIEW_NOT_SHARED_TO_GROUP` — The specified view is not currently shared with this group. | Verify the share exists via Get Shared Details before removing. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Sharing overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Workspace Shared Details](get-workspace-shared-details.md), [Share Views](share-views.md), [Update Shared Details](update-shared-details-for-view.md), [Get Shared Details](get-shared-details-for-views.md), [Get My Permissions](get-user-permissions.md).
- [SDK examples](../../../sdk-examples/share-and-publish/sharing/remove-share.md).
