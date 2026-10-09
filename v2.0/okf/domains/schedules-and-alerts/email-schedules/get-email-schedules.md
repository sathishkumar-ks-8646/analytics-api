---
type: API Endpoint
title: Get Email Schedules
description: "Returns every email schedule defined in the workspace, with its name, run period, enabled state, creator, and the views it delivers."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/emailschedules"
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - email-schedules
  - get
  - metadata
api:
  operation_id: getEmailSchedules
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/emailschedules"
  domain: schedules-and-alerts
  group: email-schedules
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace."
  error_codes:
    - 7103
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/schedules-alerts-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1emailschedules/get"
    config_schema: null
    response_schema: GetEmailSchedulesResponse
  sdk_examples: "/sdk-examples/schedules-and-alerts/email-schedules/get-email-schedules.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/schedules-alerts-grouped-api.json"
    title: OpenAPI 3 specification - schedules-alerts-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/emailschedules`** - Get Email Schedules (Email Schedules / Schedules & Alerts).

Returns every email schedule defined in the workspace, with its name, run period, enabled state, creator, and the views it delivers. This is the discovery call for `<schedule-id>`, which the other five APIs need.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getEmailSchedules` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/emailschedules` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`schedules-alerts-grouped-api.json`](../../../references/openapi/schedules-alerts-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1emailschedules/get`; response schema `GetEmailSchedulesResponse` |

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

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get email schedules"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.emailSchedules` | JSONArray | One entry per email schedule in the workspace. **Always present**; an empty array `[]` when the workspace has none. |
| `emailSchedules[].scheduleId` | String | ID of the schedule, serialised as a **string**. Use as `<schedule-id>` in the other five APIs. **May change after an update** — see [Schedule ID Lifecycle](overview.md#schedule-id-lifecycle). |
| `emailSchedules[].scheduleName` | String | Display name of the schedule. Unique within the workspace. |
| `emailSchedules[].schedulePeriod` | String | The run frequency and time rendered as **human-readable prose in the schedule's timezone**, e.g. `"weekly on Friday at 14:10 IST"`, `"daily at 12:05 IST"`, `"Every 6 days at 10:50 GMT"`. This is a display string, not a parseable structure — it is **not** the `scheduleDetails` object you sent, and there is no API that returns `scheduleDetails` back. To change the period you must resend a complete `scheduleDetails` object. |
| `emailSchedules[].schedulesConsumed` | Number | How many units of the organization's email-schedule quota this schedule consumes. See [Quota Consumption](overview.md#quota-consumption). |
| `emailSchedules[].isEnabled` | Boolean | `true` when the schedule is active and will run at its next occurrence; `false` when it has been deactivated via [Change Email Schedule Status](change-email-schedule-status.md). A deactivated schedule still exists and can still be triggered manually. |
| `emailSchedules[].createdBy` | String | Email address of the user who created the schedule. Relevant to permissions: a custom-role user without full email-schedule access can only act on schedules where this is their own address. |
| `emailSchedules[].views` | JSONArray of String | IDs of the views the schedule delivers, as strings. Present for ordinary schedules. |
| `emailSchedules[].selectedTabs` | JSONArray of String | **Replaces `views`** when the schedule targets a *tabbed dashboard* — it then lists the delivered tab IDs instead. Exactly one of `views` or `selectedTabs` is present per entry, never both. |

# Examples

## Sample Requests

**Case 1 — Standard workspace**

```http
GET /restapi/v2/workspaces/137687000271334001/emailschedules HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
GET /restapi/v2/workspaces/137687000271334009/emailschedules HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK — Workspace with a multi-view schedule and a single-view schedule**

```json
{
    "status": "success",
    "summary": "Get email schedules",
    "data": {
        "emailSchedules": [
            {
                "scheduleId": "137687000010815003",
                "scheduleName": "Weekly Sales Report",
                "schedulePeriod": "weekly on Friday at 14:10 IST",
                "schedulesConsumed": 1,
                "isEnabled": true,
                "createdBy": "jane.doe@example.com",
                "views": [
                    "137687000006991601",
                    "137687000006991650"
                ]
            },
            {
                "scheduleId": "137687000010815001",
                "scheduleName": "Daily Sales Snapshot",
                "schedulePeriod": "Every 6 days at 10:50 GMT",
                "schedulesConsumed": 1,
                "isEnabled": false,
                "createdBy": "jane.doe@example.com",
                "views": [
                    "137687000006991601"
                ]
            }
        ]
    }
}
```

**HTTP 200 OK — Workspace with no email schedules**

```json
{
    "status": "success",
    "summary": "Get email schedules",
    "data": {
        "emailSchedules": []
    }
}
```

**HTTP 403 Forbidden — Request sent through a Client Portal / White Label domain (Case 2)**

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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Email Schedules](../../../sdk-examples/schedules-and-alerts/email-schedules/get-email-schedules.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Workspace-wide, unfiltered, unpaged** | The response always covers every schedule in the workspace. There is no search, sort, or paging parameter — filter client-side on `scheduleName`, `isEnabled`, or `createdBy`. |
| **Empty array, not an error** | A workspace with no schedules returns HTTP 200 with `"emailSchedules": []`. |
| **`schedulePeriod` is prose, not structure** | It is generated for display and its wording varies by frequency and timezone. Never parse it to reconstruct a `scheduleDetails` object; keep your own copy of what you sent if you need to round-trip. |
| **`views` and `selectedTabs` are mutually exclusive** | Ordinary schedules report `views`; tabbed-dashboard schedules report `selectedTabs`. Code defensively for both keys rather than assuming `views` is always present. |
| **Recipients are not returned** | `emailIds`, `groupIds`, `cc`, `exportType`, `applyShareCriteria`, and `applyDefaultUf` are **not** in this response. There is no read API that returns a schedule's full configuration — an integration that needs it must retain what it sent. |
| **The only way to discover a regenerated ID** | After an update that changed the name or period, this API (or the update response itself) is how you learn the new `scheduleId`. |
| **Newer builds may return additional fields** | Some builds also include `subject`, `message`, and `isBCC` on each entry. Treat the response as extensible and ignore unrecognised keys rather than validating against a closed schema. |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get Workspace List](../../workspace-management/workspace-operations/overview.md) → `<workspace-id>` → Get Email Schedules → `<schedule-id>` for every other API here. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The request came through a Client Portal / White Label domain (where this API is disabled), or the user lacks Create Email Schedule permission on the workspace. | Call from the standard API host as an Account Admin, Organization Admin, Workspace Admin, or a user with Create Email Schedule permission. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Email Schedules overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Schedules & Alerts](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Email Schedule](create-email-schedule.md), [Update Email Schedule](update-email-schedule.md), [Delete Email Schedule](delete-email-schedule.md), [Change Email Schedule Status](change-email-schedule-status.md), [Trigger Email Schedule](trigger-email-schedule.md).
- [SDK examples](../../../sdk-examples/schedules-and-alerts/email-schedules/get-email-schedules.md).
