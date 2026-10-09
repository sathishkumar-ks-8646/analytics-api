---
type: API Endpoint
title: Remove Private Access
description: "Removes the view's Private URL entirely — the private key, the associated permission set, the password, and the expiry date."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink"
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - publish
  - delete
  - embed
api:
  operation_id: removePrivateAccess
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink"
  domain: share-and-publish
  group: publish
  oauth_scopes:
    - ZohoAnalytics.embed.delete
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission on the workspace, or any user with Share permission on the view."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 7319
    - 7565
    - 8115
    - 8535
  openapi:
    file: "/references/openapi/share-publish-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1publish~1privatelink/delete"
    config_schema: null
    response_schema: null
  sdk_examples: "/sdk-examples/share-and-publish/publish/remove-private-access.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink`** - Remove Private Access (Publish / Share & Publish).

Removes the view's **Private URL** entirely — the private key, the associated permission set, the password, and the expiry date. Every previously distributed private URL for the view stops working. The public URL (if any) and the publish configuration are left untouched.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `removePrivateAccess` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.embed.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsembeddelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Publish permission on the workspace, or any user with Share permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 204 with no body |
| OpenAPI | [`share-publish-grouped-api.json`](../../../references/openapi/share-publish-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1publish~1privatelink/delete` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.embed.delete`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`).

# Examples

## Sample Requests

**Case 1 — Standard workspace**

```http
DELETE /restapi/v2/workspaces/137687000271334001/views/137687000006991601/publish/privatelink HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal workspace**

```http
DELETE /restapi/v2/workspaces/137687000271334009/views/137687000006991777/publish/privatelink HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

```
HTTP/1.1 204 No Content
```

**HTTP 404 Not Found — The view has no private link**

```json
{
    "status": "failure",
    "summary": "VIEW_NOT_PUBLISHED_AS_PRIVATE",
    "data": {
        "errorCode": 8115,
        "errorMessage": "This view is not published as a private link."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Remove Private Access](../../../sdk-examples/share-and-publish/publish/remove-private-access.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Remove Private Access returns a bare HTTP `204 No Content` — no `status`/`summary` JSON to parse. |
| **Not idempotent** | Calling it on a view that has no private link fails with `8115` `VIEW_NOT_PUBLISHED_AS_PRIVATE`. Check `privateLinkConfig.isPrivate` via [Get Publish Configurations](get-publish-configurations.md) first if you need a safe repeat. |
| **Password and expiry go with the link** | There is no separate "remove password" or "remove expiry" call needed — both are discarded along with the link. (To clear them while keeping the link alive, use `removePassword` / `removeExpiryDate` on [Create Private URL](create-private-url.md).) |
| **Frees a plan allotment** | Removing a private link releases one of the organization's allotted private links, so a subsequent [Create Private URL](create-private-url.md) that previously failed with `6121`/`6122` may then succeed. |
| **Permission check is workspace-level for Publish** | The Publish permission is evaluated at the **workspace** level for this API (unlike [Get Private URL](get-private-url.md) and [Create Private URL](create-private-url.md), which evaluate it per view). A custom-role user with Publish or Make Public permission on the specific view is also accepted. |
| **Only the private channel is removed** | An active public URL on the same view survives this call — remove it with [Remove Public Permission](remove-public-permission.md). |
| **Dependency chain** | [Get Publish Configurations](get-publish-configurations.md) (confirm `privateLinkConfig.isPrivate` is `true`) → Remove Private Access. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — View not found. | Verify `<view-id>` exists. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The user does not have Publish permission on the workspace or Share permission on the view. | Ensure the user is an Account Admin, Organization Admin, Workspace Admin, or has Publish / Share permission. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The view does not belong to the specified workspace. | Ensure `<workspace-id>` and `<view-id>` are consistent. |
| [7565](../../../foundations/error-codes.md#error-7565) | 400 | `UNVERIFIED_EMAIL` — The calling user's primary email address is not verified. | Verify the account's primary email address and retry. |
| [8115](../../../foundations/error-codes.md#error-8115) | 404 | `VIEW_NOT_PUBLISHED_AS_PRIVATE` — The view has no private link. | Nothing to remove; the link is already absent. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.embed.delete`. |

# Related

- [Publish overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Share & Publish](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Make View Public](make-views-public.md), [Remove Public Permission](remove-public-permission.md), [Get Private URL](get-private-url.md), [Create Private URL](create-private-url.md), [Get Publish Configurations](get-publish-configurations.md), [Update Publish Configurations](update-publish-configurations.md).
- [SDK examples](../../../sdk-examples/share-and-publish/publish/remove-private-access.md).
