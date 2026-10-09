---
type: API Endpoint
title: Update Shared Details
description: "Updates the permission set, column/row restrictions, or filter criteria of an existing share on a single view, for the users/groups specified."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - sharing
  - put
  - share
api:
  operation_id: UpdateSharedDetailsForView
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share"
  domain: share-and-publish
  group: sharing
  oauth_scopes:
    - ZohoAnalytics.share.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Share permission on <view-id>."
  error_codes:
    - 7301
    - 7542
    - 7545
    - 8032
    - 8074
    - 8080
    - 8150
    - 8241
  openapi:
    file: "/references/openapi/share-publish-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1share/put"
    config_schema: UpdateSharedDetailsConfig
    response_schema: null
  sdk_examples: "/sdk-examples/share-and-publish/sharing/update-shared-details-for-view.md"
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

**PUT `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share`** - Update Shared Details (Sharing / Share & Publish).

Updates the permission set, column/row restrictions, or filter criteria of an **existing** share on a single view, for the users/groups specified.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `UpdateSharedDetailsForView` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.share.update`](../../../foundations/oauth-scopes.md#zohoanalyticsshareupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Share permission on <view-id>. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1share/put`; CONFIG schema `UpdateSharedDetailsConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.share.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

Same structure as [Share Views](share-views.md) **except there is no `viewIds` key** — the view is identified by `<view-id>` in the URL, and there are no `inviteMail`/`inviteMailCCMe`/`mailSubject`/`mailMessage` fields (no invite email is sent on an update).

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `emailIds` | JSONArray of String | No* | — | Email addresses whose share on `<view-id>` should be updated. |
| `groupIds` | JSONArray of String/Long | No* | — | Group IDs whose share on `<view-id>` should be updated. |
| `permissions` | JSONObject | No | unchanged if omitted | New permission set to apply. See [`permissions` Fields](share-views.md#permissions-fields). `read` must remain `true`. |
| `columns` | JSONArray | No | unchanged if omitted | See [`columns` Fields](share-views.md#columns--vudcolumns--drillcolumns-fields). |
| `includeAllColsForVUD` | Boolean | No | unchanged if omitted | If `true`, the shared user can view all columns in "View Underlying Data" mode instead of only the columns in `vudColumns`. Same semantics as in [Share Views](share-views.md). |
| `vudColumns` | JSONArray | No | unchanged if omitted | Restricts which columns are visible in "View Underlying Data" mode. Same shape as `columns` — see [Share Views](share-views.md). |
| `drillColumns` | JSONArray | No | unchanged if omitted | Restricts which columns are visible when the shared user drills down. Same shape as `columns` — see [Share Views](share-views.md). |
| `criteria` | String | No | unchanged if omitted | New row-level filter criteria. Pass an empty string to clear an existing criteria. |
| `inheritParentFilterCriteria` | Boolean | No | unchanged if omitted | If `true`, the shared user also inherits any filter criteria already applied on the view for the sharer, in addition to `criteria`. Same semantics as in [Share Views](share-views.md). |
| `domainName` | String | No | — | Client Portal/White Label domain to scope this update to. |
| `validateSystemTags` | Boolean | No | `true` | If `true`, the update is blocked with a confirmation-required error (`8241`) when `<view-id>` carries a restricted **DATA_WARNING** system tag. Pass `false` to acknowledge the warning and update anyway. Same semantics as in [Share Views](share-views.md). |

\* At least one of `emailIds` or `groupIds` is required, identifying which existing share(s) on `<view-id>` to update.

## Notes from the OpenAPI specification

- At least one of `emailIds` or `groupIds` must be specified, to identify the users or the groups whose sharing configuration has to be updated.
- `vudColumns` is applicable only when the `vud` permission is set to true.
- `drillColumns` is applicable only when the `drillDown` permission is set to true.
- `inheritParentFilterCriteria` is applicable only for reports, not for tables.
- `validateSystemTags` is applicable only when System Tags are enabled for your organization.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Grant export access to an already-shared user**

```http
PUT /restapi/v2/workspaces/137687000271334001/views/137687000006991601/share HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "emailIds": ["jane.doe@example.com"],
    "permissions": {
        "read": true,
        "export": true
    }
}
```

**Case 2 — Client Portal: update a group's share to remove write access**

```http
PUT /restapi/v2/workspaces/137687000271334009/views/137687000006991777/share HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "groupIds": ["137687000006991790"],
    "permissions": {
        "read": true,
        "export": true,
        "addRow": false,
        "updateRow": false
    },
    "domainName": "portal.customdomain.com"
}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Update Shared Details](../../../sdk-examples/share-and-publish/sharing/update-shared-details-for-view.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Update Shared Details returns a bare HTTP `204 No Content` on success. |
| **View must already be shared** | This API modifies an existing share; it does not create a new one — if the user/group is not currently shared on `<view-id>`, error 8032 `VIEW_NOT_SHARED` (or 8150 for groups) is returned. Use Share Views to create the share first. |
| **Partial update semantics** | Any field omitted from CONFIG leaves that aspect of the share unchanged; only supplied fields are applied. |
| **Dependency** | [Get Shared Details](get-shared-details-for-views.md) → identify the current share state → Update Shared Details. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — User does not have Share permission on `<view-id>`. | Ensure the user is an Account Admin, Organization Admin, or Workspace Admin, or has Share permission on the view. |
| [7542](../../../foundations/error-codes.md#error-7542) | 400 | `FILTER_CRITERIA_NOT_PERMITTED_FOR_SHARED_USER` — `criteria` update is not permitted for this share type. | Remove or adjust the `criteria` field. |
| [7545](../../../foundations/error-codes.md#error-7545) | 400 | `SHARE_AND_WRITE_PERMISSIONS_NOT_ALLOWED_FOR_RO_USERS` — A Read-Only user was granted `share` together with a write permission. | Do not combine `share: true` with write permissions for Read-Only users. |
| [8032](../../../foundations/error-codes.md#error-8032) | 400 | `VIEW_NOT_SHARED` — The view is not currently shared with the specified user. | Share the view first via Share Views. |
| [8074](../../../foundations/error-codes.md#error-8074) | 400 | `READ_PERM_SHOULD_BE_TRUE_FOR_SHARING` — `permissions.read` was explicitly set to `false`. | Keep `permissions.read` as `true`. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — CONFIG is malformed or missing a required field. | Validate the CONFIG JSON against the parameter table above. |
| [8150](../../../foundations/error-codes.md#error-8150) | 400 | `VIEW_NOT_SHARED_TO_GROUP` — The view is not currently shared with the specified group. | Share the view to this group first via Share Views. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | `SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION` (HTTP 409) — `<view-id>` carries a restricted DATA_WARNING system tag. | Review the warning, then resend with `"validateSystemTags": false` to confirm. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Sharing overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Workspace Shared Details](get-workspace-shared-details.md), [Share Views](share-views.md), [Get Shared Details](get-shared-details-for-views.md), [Remove Shared Views](remove-share.md), [Get My Permissions](get-user-permissions.md).
- [SDK examples](../../../sdk-examples/share-and-publish/sharing/update-shared-details-for-view.md).
