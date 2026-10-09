---
type: API Endpoint
title: Update Dashboard
description: Replaces one or more sections of an existing dashboard.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - reports-and-dashboards
  - dashboards
  - put
  - modeling
api:
  operation_id: updateDashboard
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}"
  domain: reports-and-dashboards
  group: dashboards
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "Design Modify on the dashboard — the owner, a Workspace Admin, an Organization Admin, or a shared user granted edit rights."
  rate_limit: "10 requests per user per 60 seconds; lockout 600 seconds on breach"
  error_codes:
    - 7103
    - 7104
    - 7111
    - 7301
    - 7309
    - 7319
    - 7479
    - 7480
    - 7481
    - 7482
    - 7483
    - 7484
    - 7485
    - 7486
    - 7487
    - 7488
    - 7491
    - 7492
    - 7493
    - 7507
    - 7510
    - 7511
    - 7512
    - 7513
    - 7514
    - 8027
    - 8504
    - 8509
    - 8517
    - 8534
    - 8535
    - 8542
    - 9001
  openapi:
    file: "/references/openapi/reports-dashboards-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1dashboards~1{dashboard-id}/put"
    config_schema: UpdateDashboardConfig
    response_schema: null
  sdk_examples: "/sdk-examples/reports-and-dashboards/dashboards/update-dashboard.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**PUT `/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}`** - Update Dashboard (Dashboards / Reports & Dashboards).

Replaces one or more sections of an existing dashboard.

From the OpenAPI specification:

Replaces one or more sections of an existing dashboard.

Permission required: Design Modify on the dashboard — the owner, a Workspace Admin, an Organization Admin, or a shared user granted edit rights.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `updateDashboard` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | Design Modify on the dashboard — the owner, a Workspace Admin, an Organization Admin, or a shared user granted edit rights. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| Rate limit | 10 requests per user per 60 seconds; lockout 600 seconds on breach. See [Rate limits](../../../foundations/rate-limits-and-quotas.md). |
| Content-Type | `application/x-www-form-urlencoded` |
| Custom domain | Permitted when the workspace is mapped to the calling domain. |
| Throttle | 10 requests per minute per user; 10-minute lock-out on breach. |
| OpenAPI | [`reports-dashboards-grouped-api.json`](../../../references/openapi/reports-dashboards-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1dashboards~1{dashboard-id}/put`; CONFIG schema `UpdateDashboardConfig` |

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
| `{workspace-id}` | string | ID of the workspace that contains the dashboard. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{dashboard-id}` | string | ID of the dashboard to update. | [How to obtain](../../../foundations/identifiers.md#dashboard-id) |

## CONFIG Parameter

Maximum encoded size 5,000,000 characters. **Only four keys are accepted** — this is the key difference
from Create.

| Field | Type | Mandatory | Description |
|-------|------|-----------|-------------|
| `layout` | String | No | Replaces the entire layout. Same rules and validation as Create. |
| `themes` | JSONObject | No | Replaces the entire theme. Same required-field rules as Create. |
| `settings` | JSONObject | No | Replaces the entire settings block. |
| `layoutType` | Integer | No | 1–4; triggers auto-layout generation for the supplied `layout`. |

## Notes from the OpenAPI specification

Each supplied section (**layout**, **themes**, **settings**) is deleted and rewritten in full; an omitted section is left untouched. A **settings** object with one key leaves the dashboard with exactly one stored setting. Read the current configuration, merge your change, re-serialise **layout** to a string, then write the whole section back. The whole update runs in one transaction.

This is a workspace-scoped API. The **ZANALYTICS-ORGID** header carrying the organization ID that owns the workspace is mandatory.

Tabbed dashboards are out of scope: Read and Update reject a tabbed dashboard with **7511**.

The CONFIG parameter must be sent as a URL encoded JSON string in a form field named **CONFIG**, with the content type **application/x-www-form-urlencoded**.

The **layout** attribute inside CONFIG is a JSON-encoded **string**, not a nested object: CONFIG={"displayName":"Sales Overview","layout":"{\"1\":{\"type\":\"VIEW\",\"viewName\":\"Sales Chart\",\"width\":80,\"height\":20,\"left\":0,\"top\":0}}"}. **themes** and **settings** are ordinary nested objects. Read Dashboard Metadata returns **layout** as a genuine object, so it must be re-serialised to a string before being written back.

When **layoutType** is 1 to 4 the supplied geometry is discarded and a 1/2/3/4-column layout is generated: a full-width USERFILTERS card, one HTML card per **content** value, then one VIEW card per distinct **viewName**. Omit **layoutType**, or send 0, to keep the layout as submitted. Auto-layout is not recorded in the read response.

The CONFIG parameter has a maximum encoded size of 5,000,000 characters; the encoded **layout** string at most 1,000,000.

The response is not a valid Create or Update payload. Re-serialise **layout** to a string, delete **objId**, **displayName** and **description** before an update (8542), convert the theme numbers that come back as strings (**card.blur**, **card.radius**, **card.margin**, **image.transparency**, **image.flip**) back to numbers/booleans, and expect card IDs renumbered from "1". **layoutType**, card **properties**, **image_properties** and **allowAllExport** are written but never returned.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Notes from the OpenAPI specification

This API returns no response body on success - only HTTP 204 No Content. Only failure responses carry a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Change only the theme**

```http
PUT /restapi/v2/workspaces/466206000000071000/dashboards/466206000000106002 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"themes":{"type":"solid","solid":{"background":"#FFFFFF"},"card":{"background":"#F4F5F7"}}}
```

**Case 2 — Replace the layout**

```http
PUT /restapi/v2/workspaces/466206000000071000/dashboards/466206000000106002 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"layout":"{\"1\":{\"type\":\"USERFILTERS\",\"width\":80,\"height\":3,\"left\":0,\"top\":0},\"2\":{\"type\":\"VIEW\",\"viewName\":\"Sales by Region\",\"width\":80,\"height\":25,\"left\":0,\"top\":3}}"}
```

**Case 3 — Reset to the default theme**

```
CONFIG={"themes":{"default":"true"}}
```

## Sample Responses

**HTTP 204 No Content** — no response body is returned on success.

```
HTTP/1.1 204 No Content
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Update Dashboard](../../../sdk-examples/reports-and-dashboards/dashboards/update-dashboard.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

## What differs from Create

| Aspect | Create | Update |
|--------|--------|--------|
| `displayName` | Required | **Not accepted** — raises **8542**. A dashboard cannot be renamed through this API. |
| `description` | Optional | **Not accepted** — raises **8542**. |
| `layout` | Required | Optional; omit to leave the layout untouched. |
| `themes` | Optional; omission writes the default theme | Optional; omission leaves the existing theme untouched. |
| `settings` | Optional; omission writes the default settings | Optional; omission leaves the existing settings untouched. |
| Response | 200 with `data.dashboardId` | **204 No Content**, empty body. |

> **Each supplied section is deleted and rewritten.** `DashLayoutDeletion`, `DashThemeDeletion` and
> `DashSettingDeletion` run before the new rows are inserted. There is no field-level patching: a
> `settings` object containing one key leaves the dashboard with exactly one setting stored. Read the
> current configuration first, merge your change into it, then write the whole section back — after
> applying the transformations in [Round-tripping a dashboard](overview.md#round-tripping-a-dashboard).

> **Partial layouts fail in confusing ways.** Sending three of a dashboard's six cards does not move
> those three — it replaces the layout with three cards. If the subset happens to violate a rule (for
> example by containing only `USERFILTERS` cards) you will get **9001** or an overlap error rather than
> a clear message.

> The whole update runs inside a single transaction, so a validation failure in any section leaves the
> dashboard untouched.

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Verify <workspace-id>. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The dashboard does not exist in this workspace. | Verify `<dashboard-id>`. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | A dashboard with this displayName already exists in the workspace. | Choose a different name. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The caller lacks Design Modify permission on the dashboard. | Grant edit access. |
| [7309](../../../foundations/error-codes.md#error-7309) | 400 | Authorization header absent. | Send Authorization: Zoho-oauthtoken <token>. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The dashboard belongs to a different workspace. | Make the two path IDs consistent. |
| [7479](../../../foundations/error-codes.md#error-7479) | 400 | A card is missing one or more of type, width, height, left, top. | Add the missing positional fields. |
| [7480](../../../foundations/error-codes.md#error-7480) | 400 | Negative offset, width/height of 1 or less, or left + width > 80. | Keep every card inside the 80-unit grid. |
| [7481](../../../foundations/error-codes.md#error-7481) | 400 | The referenced view exists but the caller cannot read it. | Have the view shared with the caller, or remove the card. |
| [7482](../../../foundations/error-codes.md#error-7482) | 400 | Two cards overlap. | Reposition so no two rectangles intersect. |
| [7483](../../../foundations/error-codes.md#error-7483) | 400 | A HTML, TITLE, PARA, IMAGE or EMBED card has absent, null or empty content. | Supply a non-empty content string. |
| [7484](../../../foundations/error-codes.md#error-7484) | 400 | More than 100 cards in the layout. | Split the dashboard. |
| [7485](../../../foundations/error-codes.md#error-7485) | 400 | Unrecognised card type. | Use one of the eight values in Card types. |
| [7486](../../../foundations/error-codes.md#error-7486) | 400 | A positional field has the wrong JSON type. | width, height, left, top must be integers; type must be a string. |
| [7487](../../../foundations/error-codes.md#error-7487) | 400 | displayName or layout is absent, null or empty. | Supply both. Remember layout is a JSON-encoded string. |
| [7488](../../../foundations/error-codes.md#error-7488) | 400 | A settings or themes key has an empty or null value, or an unrecognised key reached the server. | Remove the key or give it a valid value. |
| [7491](../../../foundations/error-codes.md#error-7491) | 400 | The sub-object required by themes.type is missing, or card is absent. | Add the required sub-object. |
| [7492](../../../foundations/error-codes.md#error-7492) | 400 | A required field inside the type sub-object or inside card is missing. | See the required-fields table in Themes. |
| [7493](../../../foundations/error-codes.md#error-7493) | 400 | A sub-object belonging to a different theme type is present, or a forbidden key accompanies default. | Remove the conflicting key. |
| [7507](../../../foundations/error-codes.md#error-7507) | 400 | displayName exceeds 100 characters, or description exceeds 250. | Shorten the value. |
| [7510](../../../foundations/error-codes.md#error-7510) | 400 | layout is not parseable JSON, or a themes sub-object is null. | Validate the JSON you embed in the layout string; never send null for card, solid, gradient or image. |
| [7511](../../../foundations/error-codes.md#error-7511) | 400 | The target is a tabbed dashboard. | Tabbed dashboards cannot be modified through this API. |
| [7512](../../../foundations/error-codes.md#error-7512) | 400 | A card is smaller than the minimum for its type. | See the min height/width columns in Card types. |
| [7513](../../../foundations/error-codes.md#error-7513) | 400 | chartEffect.type supplied while chartEffect.apply is 1. | Remove type, or set apply to 2. |
| [7514](../../../foundations/error-codes.md#error-7514) | 400 | chartEffect.apply is 2 but chartEffect.type is absent. | Supply chartEffect.type. |
| [8027](../../../foundations/error-codes.md#error-8027) | 400 | One or more VIEW cards name a view that does not exist in this workspace, or viewName is absent / null / non-string. | Check the view display names. Matching is case-insensitive but the view must exist. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | The CONFIG parameter is missing from the request body. | Send CONFIG as a form-encoded parameter. |
| [8509](../../../foundations/error-codes.md#error-8509) | 400 | An enumerated or pattern-constrained value does not match — a malformed colour, an out-of-range number, layoutType outside 1–4, a non-string colour. | Check the ranges in Themes and Settings. |
| [8517](../../../foundations/error-codes.md#error-8517) | 400 | A value has the wrong JSON data type for its schema declaration. | Match the declared types. |
| [8534](../../../foundations/error-codes.md#error-8534) | 400 | A theme sub-object was supplied as an array, or CONFIG is malformed JSON. | Use {} for objects. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Refresh with scope `ZohoAnalytics.modeling.update`. |
| [8542](../../../foundations/error-codes.md#error-8542) | 400 | `displayName`, `description`, or any other key outside `layout` / `themes` / `settings` / `layoutType` is present in `CONFIG`. | Remove the key. Renaming is not supported here. |
| [9001](../../../foundations/error-codes.md#error-9001) | 400 | Every card in the layout is a USERFILTERS card. | Add at least one content-bearing card. |

# Related

- [Dashboards overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Reports & Dashboards](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Dashboard](create-dashboard.md), [Read Dashboard Metadata](get-dashboard-metadata.md), [Get All Dashboards](get-dashboards.md), [Get Owned Dashboards](get-owned-dashboards.md), [Get Shared Dashboards](get-shared-dashboards.md).
- [SDK examples](../../../sdk-examples/reports-and-dashboards/dashboards/update-dashboard.md).
