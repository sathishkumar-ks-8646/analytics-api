---
type: API Endpoint
title: Copy Custom Formulas
description: "Copies one or more custom formula columns, identified by their display names, from a view of the source workspace to the equivalent view of a destination workspace."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/formulas/copy"
tags:
  - zoho-analytics
  - rest-api-v2
  - data-modeling-and-schema
  - formula-columns
  - post
  - modeling
api:
  operation_id: copyFormulas
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/formulas/copy"
  domain: data-modeling-and-schema
  group: formula-columns
  oauth_scopes:
    - ZohoAnalytics.modeling.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin of the destination organisation. This API is not available to Workspace Admins or any custom-permission user — only Account Admin / Org Admin roles are authorized."
  error_codes:
    - 7301
    - 7319
    - 8058
    - 15007
  openapi:
    file: "/references/openapi/data-modeling-schema-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1formulas~1copy/post"
    config_schema: CopyFormulasConfig
    response_schema: null
  sdk_examples: "/sdk-examples/data-modeling-and-schema/formula-columns/copy-formulas.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/formulas/copy`** - Copy Custom Formulas (Custom Formula Columns / Data Modeling & Schema).

Copies one or more custom formula columns (by name) from a view in the source workspace to the equivalent view in a destination workspace. This is typically used to replicate formula logic across workspaces owned by the same organisation (or across organisations the caller administers).

> **Cross-organisation copy header:** Similar to Copy Workspace, when an Org Admin copies formulas into a workspace belonging to a *different* organisation than the one resolved from the OAuth token, the destination organisation must be specified using the `ZANALYTICS-DEST-ORGID` header. See [Request conventions](../../../foundations/request-conventions.md) for details.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `copyFormulas` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/formulas/copy` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the source workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin of the destination organisation. This API is not available to Workspace Admins or any custom-permission user — only Account Admin / Org Admin roles are authorized. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| ZANALYTICS-DEST-ORGID Header | Conditionally required — set this when the destination workspace belongs to a different organisation than the one identified by `ZANALYTICS-ORGID` (Org Admin cross-org scenario). |
| Custom Domain | **Not available** via White Label / Client Portal. |
| OpenAPI | [`data-modeling-schema-grouped-api.json`](../../../references/openapi/data-modeling-schema-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1formulas~1copy/post`; CONFIG schema `CopyFormulasConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `ZANALYTICS-DEST-ORGID` | `<org-id>` | Optional | ID of the destination organisation. Send this when an Organization Admin copies into a workspace that belongs to an organisation other than the one identified by ZANALYTICS-ORGID. |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

| Parameter | Type | Mandatory | Description |
|-----------|------|-----------|-------------|
| `formulaColumnNames` | JSONArray of String | **Yes** | Array of formula column **display names** (not IDs) from the source view to copy. Max 1000 entries. |
| `destWorkspaceId` | Long | **Yes** | ID of the destination workspace where the formulas will be copied to. Must contain a view with the same structure/columns as the source view. |
| `workspaceKey` | String | Conditionally required | The destination workspace's secret key (see [Get Workspace SecretKey](../../workspace-management/workspace-operations/overview.md)). Required when the destination workspace belongs to a different organisation than the source. Not required for same-organisation copies. |

## Notes from the OpenAPI specification

- This API returns HTTP 204 No Content with no response body on success. There is no status or summary key to parse - treat the HTTP status code as the sole success indicator.
- Formulas are matched by their display names, as returned by the Get Custom Formulas API, and not by their formulaId values.
- The destination view is resolved internally from the structure of the views in the destination workspace, because this API takes no destination view ID. Ensure that the destination workspace holds an equivalent view with matching source columns before copying.
- This API is restricted to Account Admins and Organization Admins, unlike most modeling APIs, which also accept a Workspace Admin. This reflects its cross-workspace and cross-organisation nature.
- workspaceKey is needed only when the destination workspace belongs to a different organisation from the source. An Organization Admin identifies that organisation through the ZANALYTICS-DEST-ORGID header, whereas an Account Admin sets ZANALYTICS-ORGID directly to the destination organisation.
- This API is disabled for white label and client portal contexts and can be called only through the standard host.
- Because nothing is returned, call the Get Custom Formulas API on the destination view afterwards to confirm which formulas were copied.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

No response body is returned for this API. Success is indicated solely by the HTTP 204 status code. To verify the copy succeeded, call Get Custom Formulas on the destination view and confirm the formula names now appear there.

# Examples

## Sample Requests

**Case 1 — Copy a single formula within the same organisation**

```http
POST /restapi/v2/workspaces/20868000000040672/views/20868000000040795/formulas/copy HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"formulaColumnNames":["Total Amount"],"destWorkspaceId":20868000000045000}
```

**Case 2 — Copy multiple formulas across organisations (Org Admin, cross-org)**

```http
POST /restapi/v2/workspaces/20868000000040672/views/20868000000040795/formulas/copy HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
ZANALYTICS-DEST-ORGID: 700000987654
Content-Type: application/x-www-form-urlencoded

CONFIG={"formulaColumnNames":["Total Amount","Order Status"],"destWorkspaceId":20868000000099000,"workspaceKey":"a1b2c3d4e5f6g7h8"}
```

**Case 3 — Account Admin copying formulas to a workspace in a different org (destination org resolved via ZANALYTICS-ORGID)**

```http
POST /restapi/v2/workspaces/20868000000040672/views/20868000000040795/formulas/copy HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000987654
Content-Type: application/x-www-form-urlencoded

CONFIG={"formulaColumnNames":["Full Name"],"destWorkspaceId":20868000000099000,"workspaceKey":"a1b2c3d4e5f6g7h8"}
```

## Sample Responses

**HTTP 204 No Content**

This API returns no response body on success — only an HTTP 204 status code is returned to external API callers.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Copy Custom Formulas](../../../sdk-examples/data-modeling-and-schema/formula-columns/copy-formulas.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Formulas are matched by name, not ID** | `formulaColumnNames` takes the display names of the source formulas (as seen in Get Custom Formulas), not their `formulaId` values. |
| **Destination view is resolved automatically** | The API does not take a destination view ID — the destination view is matched internally based on the table/view structure in `destWorkspaceId`. Ensure the destination workspace has an equivalent view with matching source columns before copying. |
| **Only Account Admin / Org Admin can call this API** | Unlike most modeling APIs (which accept Workspace Admin), this API is restricted to organisation-level administrators, reflecting its cross-workspace/cross-org nature. |
| **`workspaceKey` required only for cross-organisation copies** | If the destination workspace belongs to the same organisation as the source (as resolved from `ZANALYTICS-ORGID`/`ZANALYTICS-DEST-ORGID`), `workspaceKey` can be omitted. For a different organisation, the destination workspace's secret key must be supplied, or the request fails with error 15007. |
| **No response payload — verify via Get Custom Formulas** | Since this API returns HTTP 204 with no body, always follow up with Get Custom Formulas on the destination view to confirm which formulas were successfully copied. |
| **Not available via White Label/Client Portal** | This API is disabled for custom-domain contexts, matching Copy Workspace and other organisation-level administrative APIs. |
| **Dependency** | `formulaColumnNames` → Get Custom Formulas (on the source view). `destWorkspaceId` → Get Workspace List. `workspaceKey` → Get Workspace SecretKey (destination workspace). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission. | Ensure the user is an Account Admin or Organization Admin of the destination organisation. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The source view does not belong to the specified workspace. | Confirm `<view-id>` belongs to the workspace identified by `<workspace-id>`. |
| [8058](../../../foundations/error-codes.md#error-8058) | 400 | The organisation ID specified in `ZANALYTICS-DEST-ORGID` does not exist. | Verify the destination organisation ID. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. | Regenerate the access token with the required scope (see the endpoint document) and retry. |
| [15007](../../../foundations/error-codes.md#error-15007) | 400 | The copy operation is not allowed — the destination workspace's organisation does not match the caller's organisation, and no valid `workspaceKey` was supplied (or it does not match). | Supply the correct `workspaceKey` for the destination workspace (see Get Workspace SecretKey), or perform the copy within the same organisation. |

# Related

- [Custom Formula Columns overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Modeling & Schema](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Custom Formulas](get-custom-formula-list.md), [Add Custom Formula](add-formula-column.md), [Edit Custom Formula](edit-formula-column.md), [Delete Custom Formula](delete-formula-column.md).
- [SDK examples](../../../sdk-examples/data-modeling-and-schema/formula-columns/copy-formulas.md).
