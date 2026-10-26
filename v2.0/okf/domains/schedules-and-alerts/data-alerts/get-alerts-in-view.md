---
type: API Endpoint
title: Get Alerts In View
description: Returns the alerts configured on one report.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts"
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - data-alerts
  - get
  - metadata
api:
  operation_id: getAlertsInView
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts"
  domain: schedules-and-alerts
  group: data-alerts
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the view's workspace, or hold the CREATEALERT (Manage Data Alerts) permission on that specific view. Stricter than Get Alerts In Workspace."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 7319
    - 7387
    - 8060
    - 8083
    - 8535
  openapi:
    file: "/references/openapi/schedules-alerts-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1alerts/get"
    config_schema: null
    response_schema: GetAlertsInViewResponse
  sdk_examples: "/sdk-examples/schedules-and-alerts/data-alerts/get-alerts-in-view.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/schedules-alerts-grouped-api.json"
    title: OpenAPI 3 specification - schedules-alerts-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-20T17:34:40Z
generated:
  by: process:build_okf
  at: 2026-10-23T07:58:54Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts`** - Get Alerts In View (Data Alerts / Schedules & Alerts).

Returns the alerts configured on one report. The response entries are identical in shape to [Get Alerts In Workspace](get-alerts-in-workspace.md), narrowed to a single `<view-id>`.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getAlertsInView` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the view's workspace, or hold the CREATEALERT (Manage Data Alerts) permission on that specific view. Stricter than Get Alerts In Workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`schedules-alerts-grouped-api.json`](../../../references/openapi/schedules-alerts-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1alerts/get`; response schema `GetAlertsInViewResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
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

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Identical in shape to the Response Fields of [Get Alerts In Workspace](get-alerts-in-workspace.md) — refer there for every attribute. The differences are:

| Field | Type | Description |
|-------|------|--------------|
| `summary` | String | `"Get alerts in view"` for this API. |
| `data.alerts` | JSONArray | Restricted to the alerts of the requested `<view-id>`, so every entry carries the same `viewId` and `viewName`. **Always present**; `[]` when that view has no alerts. |

# Examples

## Sample Requests

**Case 1 — Chart report with one alert**

```http
GET /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — View that belongs to a different workspace (rejected)**

```http
GET /restapi/v2/workspaces/137687000271334001/views/466206000000105001/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

## Sample Responses

**HTTP 200 OK — One alert on the requested view**

```json
{
    "status": "success",
    "summary": "Get alerts in view",
    "data": {
        "alerts": [
            {
                "id": "137687000010815003",
                "name": "Sales Drop Alert",
                "viewId": "137687000006991601",
                "viewName": "Sales By Region",
                "enabled": true,
                "createdTime": "2026-03-12T10:15:22+05:30",
                "createdByName": "Jane Doe",
                "createdBy": "jane.doe@example.com",
                "lastModifiedTime": "2026-03-20T09:00:00+05:30",
                "lastModifiedByName": "Jane Doe",
                "lastModifiedBy": "jane.doe@example.com",
                "lastAlertSentTime": "2026-03-20T09:05:00+05:30",
                "lastRunTime": "2026-03-20T09:05:00+05:30",
                "lastRunStatus": "Condition met",
                "nextScheduleTime": "2026-03-21T09:00:00+05:30"
            }
        ]
    }
}
```

**HTTP 200 OK — View with no alerts**

```json
{
    "status": "success",
    "summary": "Get alerts in view",
    "data": {
        "alerts": []
    }
}
```

**HTTP 400 Bad Request — Failure paired with Case 2**

```json
{
    "status": "failure",
    "summary": "OBJID_NOT_BELONGS_TO_DB",
    "data": {
        "errorCode": 7319,
        "errorMessage": "Objects not belongs to current workspace"
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Alerts In View](../../../sdk-examples/schedules-and-alerts/data-alerts/get-alerts-in-view.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Stricter permission than the workspace listing** | This call is view-scoped: DB Owner or `CREATEALERT` on that view. A user who can list the whole workspace may still be refused here for a specific view. |
| **The view/workspace pair is validated** | A `<view-id>` that lives in another workspace fails with `7319` rather than returning an empty list. |
| **`viewName` is filled in by this API** | The underlying lookup does not return a view name for the view-scoped query; the API resolves it from the view's configuration so that entries match the workspace listing byte-for-byte. |
| **Empty does not mean "not alert-capable"** | An empty array is the normal answer for a supported view with no alerts. To find out whether a view can carry an alert at all, call [Get View Metadata For Alert](get-view-metadata-for-alert.md), which fails with `8245` on unsupported view types. This API does **not** check the view type. |
| **No paging, filtering or sorting** | Same as [Get Alerts In Workspace](get-alerts-in-workspace.md). |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>` → Get Alerts In View → `alerts[].id`. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — View not found. | Verify `<view-id>` via [Get View List](../../views-management/view-operations/get-views.md). |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is neither the DB Owner nor a holder of `CREATEALERT` on this view, or the request arrived through a custom domain the workspace is not bound to. | Authenticate as the DB Owner or a user with Manage Data Alerts on that view, from the standard API host. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The view does not belong to the workspace in the URL. | Make `<workspace-id>` and `<view-id>` consistent. |
| [7387](../../../foundations/error-codes.md#error-7387) | 400 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not belong to the organisation in `ZANALYTICS-ORGID`. | Send the organisation id that owns the workspace. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use a domain you have purchased from Zoho Analytics, or the standard API host. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Data Alerts overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Schedules & Alerts](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Alerts In Workspace](get-alerts-in-workspace.md), [Get View Metadata For Alert](get-view-metadata-for-alert.md), [Get Alert Configuration](get-alert-configuration.md), [Create Alert](create-alert.md), [Update Alert](update-alert.md), [Delete Alerts](delete-alerts.md), [Change Alert Status](change-alert-status.md), [Run Alert](run-alert.md), [Get Alert Events](get-alert-events.md).
- [SDK examples](../../../sdk-examples/schedules-and-alerts/data-alerts/get-alerts-in-view.md).
