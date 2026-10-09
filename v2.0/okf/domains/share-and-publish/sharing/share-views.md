---
type: API Endpoint
title: Share Views
description: "Shares one or more views with a set of users and/or groups, with a specific permission set, optional column/row restrictions, and optional invite email."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/share"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - sharing
  - post
  - share
api:
  operation_id: shareViews
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/share"
  domain: share-and-publish
  group: sharing
  oauth_scopes:
    - ZohoAnalytics.share.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Share permission on all of the specified viewIds."
  error_codes:
    - 7301
    - 7307
    - 7320
    - 7321
    - 7322
    - 7323
    - 7533
    - 7535
    - 7541
    - 7543
    - 7545
    - 7549
    - 8029
    - 8074
    - 8080
    - 8085
    - 8086
    - 8241
  openapi:
    file: "/references/openapi/share-publish-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1share/post"
    config_schema: ShareViewsConfig
    response_schema: null
  sdk_examples: "/sdk-examples/share-and-publish/sharing/share-views.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/share-publish-grouped-api.json"
    title: OpenAPI 3 specification - share-publish-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/share`** - Share Views (Sharing / Share & Publish).

Shares one or more views with a set of users and/or groups, with a specific permission set, optional column/row restrictions, and optional invite email.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `shareViews` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/share` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.share.create`](../../../foundations/oauth-scopes.md#zohoanalyticssharecreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Share permission on all of the specified viewIds. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1share/post`; CONFIG schema `ShareViewsConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.share.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `viewIds` | JSONArray of String/Long | **Yes** | — | IDs of the views to share (1–1000 entries). All views must belong to the same workspace. |
| `emailIds` | JSONArray of String | No* | — | Email addresses of the users to share to. At least one of `emailIds` or `groupIds` must be supplied. |
| `groupIds` | JSONArray of String/Long | No* | — | IDs of the [workspace groups](../../users-and-groups/workspace-groups/overview.md) to share to. At least one of `emailIds` or `groupIds` must be supplied. |
| `permissions` | JSONObject | No | all `false` except as noted | The permission set to grant. `read` **must be `true`** (error 8074 `READ_PERM_SHOULD_BE_TRUE_FOR_SHARING` otherwise). See [`permissions` Fields](#permissions-fields). |
| `columns` | JSONArray | No | — | Restricts the shared user to specific columns per table/view. See [`columns` / `vudColumns` / `drillColumns` Fields](#columns--vudcolumns--drillcolumns-fields). Only meaningful when sharing a **single** view (error 7543 if combined with multi-view share). |
| `includeAllColsForVUD` | Boolean | No | `false` | If `true`, the shared user can view all columns in "View Underlying Data" mode instead of only the columns in `vudColumns`. |
| `vudColumns` | JSONArray | No | — | Restricts which columns are visible in "View Underlying Data" mode. Same shape as `columns`. |
| `drillColumns` | JSONArray | No | — | Restricts which columns are visible when the shared user drills down. Same shape as `columns`. |
| `criteria` | String | No | — | Row-level filter criteria applied only for this shared user/group (e.g., `"Region"='East'`). Not supported when sharing multiple views at once (error 7541 `FILTER_CRITERIA_NOT_SUPPORTED_FOR_MULTI_VIEW_SHARE`). |
| `inheritParentFilterCriteria` | Boolean | No | `false` | If `true`, the shared user also inherits any filter criteria already applied on the view for the sharer, in addition to `criteria`. |
| `domainName` | String | No | — | Client Portal/White Label domain to scope this share to. Only relevant when the calling user is a domain admin managing a specific portal domain's users; omit for standard sharing. |
| `inviteMail` | Boolean | No | `false` | If `true`, sends an invite/notification email to the newly shared users. |
| `inviteMailCCMe` | Boolean | No | `false` | If `true` (and `inviteMail` is `true`), CCs the sharer on the invite email. |
| `mailSubject` | String | No | Default system subject | Custom subject line for the invite email. Only used if `inviteMail` is `true`. |
| `mailMessage` | String | No | Default system message | Custom body text for the invite email. Only used if `inviteMail` is `true`. |
| `validateSystemTags` | Boolean | No | `true` | If `true`, the share is blocked with a confirmation-required error (`8241`) when any view in `viewIds` carries a restricted **DATA_WARNING** system tag. Pass `false` to acknowledge the warning and share anyway. |

\* At least one of `emailIds` or `groupIds` is required; both may be supplied together to share to users and groups in the same call.

### `permissions` Fields

| Field | Type | Default | Description |
|-------|------|---------|--------------|
| `read` | Boolean | `false` | View/read access. **Must be `true`** — sharing with only write/other permissions and `read=false` is rejected (error 8074). |
| `export` | Boolean | `false` | Allows exporting the view's data. |
| `vud` | Boolean | `false` | Allows "View Underlying Data" (drilling into the raw rows behind an aggregated report). |
| `drillDown` | Boolean | `false` | Allows drilling down into related/child views. |
| `addRow` | Boolean | `false` | Allows adding new rows (tables/imports only). |
| `updateRow` | Boolean | `false` | Allows updating existing rows. |
| `deleteRow` | Boolean | `false` | Allows deleting individual rows. |
| `deleteAllRows` | Boolean | `false` | Allows deleting **all** rows in the table at once. |
| `importAppend` | Boolean | `false` | Allows importing data in "Append" mode. |
| `importAddOrUpdate` | Boolean | `false` | Allows importing data in "Add or Update" mode. |
| `importDeleteAllAdd` | Boolean | `false` | Allows importing data in "Truncate and Add" mode. |
| `importDeleteUpdateAdd` | Boolean | `false` | Allows importing data in "Update and Add" (delta) mode. |
| `share` | Boolean | `false` | Allows the shared user to re-share the view with others. Read-Only (embedded/client-portal) users cannot be granted this together with any write permission (error 7545 `SHARE_AND_WRITE_PERMISSIONS_NOT_ALLOWED_FOR_RO_USERS`). |
| `vudSelectedColumns` | Boolean | `false` | Restricts "View Underlying Data" to only the columns listed in `vudColumns` (paired with `vud`). |
| `discussion` | Boolean | `false` | Allows posting/viewing discussion comments on the view. |
| `insight` | Boolean | `false` | Allows viewing AI-generated insights for the view. |
| `drillThrough` | Boolean | `false` | Allows drill-through actions from this view into linked views. |
| `drillActions` | Boolean | `false` | Allows executing configured drill actions. |
| `accessAdminPresets` | Boolean | `false` | Allows the shared user to view/apply admin-defined report presets. |
| `createPreset` | Boolean | `false` | Allows the shared user to create their own report presets. |

### `columns` / `vudColumns` / `drillColumns` Fields

Each is a JSONArray of objects, one per underlying table referenced by the view:

| Field | Type | Mandatory | Description |
|-------|------|-----------|--------------|
| `tableName` | String | **Yes** | Name of the table whose columns are being restricted. |
| `columnNames` | JSONArray of String | **Yes** | Column names from `tableName` that the shared user is allowed to see. |

## Notes from the OpenAPI specification

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

**Case 1 — Share a single view with one user, read + export only**

```http
POST /restapi/v2/workspaces/137687000271334001/share HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "viewIds": ["137687000006991601"],
    "emailIds": ["jane.doe@example.com"],
    "permissions": {
        "read": true,
        "export": true
    },
    "inviteMail": true
}
```

**Case 2 — Share to a group with a row-level filter and VUD access**

```http
POST /restapi/v2/workspaces/137687000271334001/share HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "viewIds": ["137687000006991601"],
    "groupIds": ["137687000006991700"],
    "permissions": {
        "read": true,
        "export": true,
        "vud": true
    },
    "criteria": "\"Region\"='East'",
    "inheritParentFilterCriteria": false
}
```

**Case 3 — White Label / Client Portal: share to a portal-domain user with write access**

```http
POST /restapi/v2/workspaces/137687000271334009/share HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "viewIds": ["137687000006991777"],
    "emailIds": ["client.user@portalcustomer.com"],
    "permissions": {
        "read": true,
        "export": true,
        "addRow": true,
        "updateRow": true
    },
    "domainName": "portal.customdomain.com"
}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Share Views](../../../sdk-examples/share-and-publish/sharing/share-views.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Share Views returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |
| **`read` is a hard requirement** | Every share must grant at least `read`; there is no "write-only" share. |
| **Single-view restrictions** | `columns`, `vudColumns`, `drillColumns`, and `criteria` only apply when exactly one view is in `viewIds` — combining them with a multi-view share fails (errors 7541/7543). |
| **Re-sharing an already-shared view** | Sharing a view/user (or view/group) combination that is already shared returns error 7321/7322 rather than silently updating it — use [Update Shared Details](update-shared-details-for-view.md) to modify an existing share. |
| **Dependency** | `viewIds` → [Get Views](../../views-management/view-operations/overview.md); `groupIds` → [Get Group List](../../users-and-groups/workspace-groups/get-groups.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — User does not have Share permission on one or more `viewIds`. | Ensure the user is an Account Admin, Organization Admin, or Workspace Admin, or has Share permission on all specified views. |
| [7307](../../../foundations/error-codes.md#error-7307) | 400 | `OWNER_CANNOT_SHARE_HIMSELF` — The sharer attempted to share a view to themselves. | Remove the sharer's own email from `emailIds`. |
| [7320](../../../foundations/error-codes.md#error-7320) | 400 | `CANNOT_SHARETO_SELF` — Same as above (alternate path). | Same as above. |
| [7321](../../../foundations/error-codes.md#error-7321) | 400 | `VIEW_ALREADY_SHARED` — The view is already shared with this user. | Use Update Shared Details to modify the existing share instead. |
| [7322](../../../foundations/error-codes.md#error-7322) | 400 | `VIEW_ALREADY_SHARED` (group form) — The view is already shared with this group. | Use Update Shared Details to modify the existing share instead. |
| [7323](../../../foundations/error-codes.md#error-7323) | 400 | `CANNOT_SHARED_TO_OBJOWNER` — Attempted to share the view with its own owner. | Remove the owner's email/group from the share request. |
| [7533](../../../foundations/error-codes.md#error-7533) | 400 | `CANNOT_SHARE_OBJECT_TO_GROUP` — The view's type does not support group sharing. | Share to individual `emailIds` instead. |
| [7535](../../../foundations/error-codes.md#error-7535) | 400 | `CANNOT_SHARE_TO_MEMBERS_NOT_PART_OF_ORG` — One or more `emailIds` do not belong to the organization. | Verify the recipients are valid organization/portal users. |
| [7541](../../../foundations/error-codes.md#error-7541) | 400 | `FILTER_CRITERIA_NOT_SUPPORTED_FOR_MULTI_VIEW_SHARE` — `criteria` supplied with more than one `viewIds` entry. | Share one view at a time when using row-level `criteria`. |
| [7543](../../../foundations/error-codes.md#error-7543) | 400 | `VUD_OR_DRILL_COLUMNS_EDIT_NOT_SUPPORTED_FOR_MULTI_VIEW_SHARE` — `vudColumns`/`drillColumns` supplied with more than one view. | Share one view at a time when restricting VUD/drill columns. |
| [7545](../../../foundations/error-codes.md#error-7545) | 400 | `SHARE_AND_WRITE_PERMISSIONS_NOT_ALLOWED_FOR_RO_USERS` — A Read-Only/embedded user was granted `share` together with a write permission. | Do not combine `share: true` with write permissions for Read-Only users. |
| [7549](../../../foundations/error-codes.md#error-7549) | 400 | `CANNOT_SHARE_TO_CUSTOMROLE_USER` — Attempted to share directly to a user who only has a custom-role-based org-level permission. | Share via the appropriate group/role mechanism instead. |
| [8029](../../../foundations/error-codes.md#error-8029) | 400 | `SHARE_INVALID_EMAIL_ADDRESS` — One or more `emailIds` entries is not a valid email address. | Correct the malformed email address(es). |
| [8074](../../../foundations/error-codes.md#error-8074) | 400 | `READ_PERM_SHOULD_BE_TRUE_FOR_SHARING` — `permissions.read` was `false` or omitted. | Set `permissions.read` to `true`. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — CONFIG is malformed or missing a required field. | Validate the CONFIG JSON against the parameter table above. |
| [8085](../../../foundations/error-codes.md#error-8085) | 400 | `SHAREDTO_EXTERNAL_DOMAIN_NOT_ALLOWED` — Sharing to an email outside the allowed domain(s) is disabled by org policy. | Share only to users within the permitted domain(s), or contact the Org Admin to adjust the policy. |
| [8086](../../../foundations/error-codes.md#error-8086) | 400 | `SHAREDTO_EXTERNAL_DOMAIN_NOT_ALLOWED` — Sharing to an email outside the allowed domain(s) is disabled by org policy. | Share only to users within the permitted domain(s), or contact the Org Admin to adjust the policy. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | `SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION` (HTTP 409) — A view being shared carries a restricted DATA_WARNING system tag. | Review the warning, then resend with `"validateSystemTags": false` to confirm. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |

# Related

- [Sharing overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Workspace Shared Details](get-workspace-shared-details.md), [Update Shared Details](update-shared-details-for-view.md), [Get Shared Details](get-shared-details-for-views.md), [Remove Shared Views](remove-share.md), [Get My Permissions](get-user-permissions.md).
- [SDK examples](../../../sdk-examples/share-and-publish/sharing/share-views.md).
