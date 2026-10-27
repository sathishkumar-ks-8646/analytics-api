---
type: API Endpoint
title: Get Alerts In Workspace
description: "Returns every alert defined anywhere in the workspace, with its name, the view it watches, its enabled state, audit stamps, and the outcome of its last run."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/alerts"
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - data-alerts
  - get
  - metadata
api:
  operation_id: getAlertsInWorkspace
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/alerts"
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
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or a custom-role user whose role has the Manage Data Alerts permission on this workspace. The check is workspace-wide — see Permission Model."
  error_codes:
    - 7103
    - 7301
    - 7387
    - 8060
    - 8083
    - 8535
  openapi:
    file: "/references/openapi/schedules-alerts-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1alerts/get"
    config_schema: null
    response_schema: GetAlertsInWorkspaceResponse
  sdk_examples: "/sdk-examples/schedules-and-alerts/data-alerts/get-alerts-in-workspace.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/schedules-alerts-grouped-api.json"
    title: OpenAPI 3 specification - schedules-alerts-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T10:54:58Z
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/alerts`** - Get Alerts In Workspace (Data Alerts / Schedules & Alerts).

Returns every alert defined anywhere in the workspace, with its name, the view it watches, its enabled state, audit stamps, and the outcome of its last run. This is the broadest discovery call for `<alert-id>`.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getAlertsInWorkspace` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/alerts` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or a custom-role user whose role has the Manage Data Alerts permission on this workspace. The check is workspace-wide — see Permission Model. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`schedules-alerts-grouped-api.json`](../../../references/openapi/schedules-alerts-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1alerts/get`; response schema `GetAlertsInWorkspaceResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID, shown in the Zoho Analytics UI under Settings > Organisation. See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary — `"Get alerts in workspace"` for this API. Never branch on it. |
| `data` | JSONObject | Response payload wrapper. |
| `data.alerts` | JSONArray | One entry per alert in the workspace. **Always present**; `[]` when the workspace has no alerts. Alerts on every supported view type (Chart / Pivot / Summary) are included. |
| `alerts[].id` | String | Alert id, numeric but serialised as a **string**. This is the `<alert-id>` for the six alert-id-addressed APIs and for the `alertIds` arrays. |
| `alerts[].name` | String | Alert name, as set by `alertName`. |
| `alerts[].viewId` | String | Id of the view the alert watches. Fixed for the life of the alert. |
| `alerts[].viewName` | String | Display name of that view. |
| `alerts[].enabled` | Boolean | `true` when the alert is live, `false` when it is paused. Native JSON boolean. Toggled by [Change Alert Status](change-alert-status.md). |
| `alerts[].createdTime` | String | Creation time as an ISO-8601 offset timestamp (`2026-03-12T10:15:22+05:30`), rendered in the **caller's profile time zone** — not in the alert's `scheduleDetails.timeZone`. |
| `alerts[].createdByName` | String | Display name of the user who created the alert. |
| `alerts[].createdBy` | String | E-mail address of that user, resolved from the owner ZUID. **Empty string** when the lookup fails — enrichment failures never break this response. |
| `alerts[].lastModifiedTime` | String | Last modification time, same format as `createdTime`. |
| `alerts[].lastModifiedByName` | String | Display name of the user who last modified the alert. |
| `alerts[].lastModifiedBy` | String | E-mail address of that user, same fallback as `createdBy`. |
| `alerts[].lastAlertSentTime` | String | When a notification was last **sent**. Empty string when the alert has never notified anyone. |
| `alerts[].lastRunTime` | String | When the alert was last **evaluated**, whether or not it notified. Empty string when it has never run. |
| `alerts[].lastRunStatus` | String | Outcome of that last evaluation as a **localised label** — `"Condition met"` or `"Condition unmet"`. Empty string when the alert has never run. Do not switch on this value; use `status` from [Get Alert Events](get-alert-events.md), which is a stable enum. |
| `alerts[].nextScheduleTime` | String | Next scheduled evaluation, same format as `createdTime`. Empty string when the alert is paused or has no active schedule. |

# Examples

## Sample Requests

**Case 1 — Standard workspace**

```http
GET /restapi/v2/workspaces/137687000271334001/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal: workspace not bound to the calling domain (rejected)**

```http
GET /restapi/v2/workspaces/137687000271334009/alerts HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK — One alert that has run, one that never has**

```json
{
    "status": "success",
    "summary": "Get alerts in workspace",
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
            },
            {
                "id": "137687000010815005",
                "name": "Region sub-total monitor",
                "viewId": "466206000000105001",
                "viewName": "Sales Pivot",
                "enabled": false,
                "createdTime": "2026-03-19T18:42:03+05:30",
                "createdByName": "John Roe",
                "createdBy": "john.roe@example.com",
                "lastModifiedTime": "2026-03-19T18:42:03+05:30",
                "lastModifiedByName": "John Roe",
                "lastModifiedBy": "john.roe@example.com",
                "lastAlertSentTime": "",
                "lastRunTime": "",
                "lastRunStatus": "",
                "nextScheduleTime": ""
            }
        ]
    }
}
```

**HTTP 200 OK — Workspace with no alerts**

```json
{
    "status": "success",
    "summary": "Get alerts in workspace",
    "data": {
        "alerts": []
    }
}
```

**HTTP 403 Forbidden — Failure paired with Case 2**

```json
{
    "status": "failure",
    "summary": "SECURITY_NOT_PERMITTED",
    "data": {
        "errorCode": 7301,
        "errorMessage": "You (WL_DBAdmin) do not have the permission to do this operation. "
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Alerts In Workspace](../../../sdk-examples/schedules-and-alerts/data-alerts/get-alerts-in-workspace.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Permission is workspace-wide, not per view** | One alert-level permission on the workspace lists every alert in it, including alerts on views the caller could not configure. Acting on those alerts is a separate, stricter check — see [Permission Model](overview.md#permission-model). |
| **Timestamps use the caller's time zone** | Every ISO-8601 value is rendered in the caller's profile time zone, not in the alert's own `scheduleDetails.timeZone`. Two users see different wall-clock values for the same `nextScheduleTime`. |
| **Missing timestamps are `""`, never `null`** | A never-run alert reports `lastRunTime`, `lastAlertSentTime` and `lastRunStatus` as empty strings; a paused alert additionally reports an empty `nextScheduleTime`. No field in this response is ever JSON `null`. |
| **`lastRunStatus` is prose, not an enum** | It is translated per caller language. The machine-readable equivalent is `alertEvents[].status` from [Get Alert Events](get-alert-events.md). |
| **Ids are strings** | Parse `id` and `viewId` as strings or 64-bit longs. A 32-bit integer type loses precision. |
| **No paging, no filtering, no sorting** | The whole alert list is returned in one response. There is no `pageNo`, no keyword search and no status filter. [Get Alert Events](get-alert-events.md) is the only paginated API in this family. |
| **Empty result is a success** | A workspace with no alerts returns `200` with `"alerts": []`, not an error. |
| **Owner e-mail resolution is best-effort** | `createdBy` / `lastModifiedBy` are resolved through a remote identity lookup, cached once per distinct ZUID per request. A failed lookup yields `""` rather than failing the call. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get Workspace List](../../workspace-management/workspace-operations/overview.md) → `<workspace-id>` → Get Alerts In Workspace → `alerts[].id`. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is neither a Workspace Admin nor a custom-role user with Manage Data Alerts, or the request arrived through a custom domain the workspace is not bound to. | Authenticate as an admin or a user with Manage Data Alerts, and call from the standard API host unless the workspace is bound to your custom domain. |
| [7387](../../../foundations/error-codes.md#error-7387) | 400 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not belong to the organisation in `ZANALYTICS-ORGID`. | Send the organisation id that owns the workspace. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use a domain you have purchased from Zoho Analytics, or the standard API host. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Data Alerts overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Schedules & Alerts](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Alerts In View](get-alerts-in-view.md), [Get View Metadata For Alert](get-view-metadata-for-alert.md), [Get Alert Configuration](get-alert-configuration.md), [Create Alert](create-alert.md), [Update Alert](update-alert.md), [Delete Alerts](delete-alerts.md), [Change Alert Status](change-alert-status.md), [Run Alert](run-alert.md), [Get Alert Events](get-alert-events.md).
- [SDK examples](../../../sdk-examples/schedules-and-alerts/data-alerts/get-alerts-in-workspace.md).
