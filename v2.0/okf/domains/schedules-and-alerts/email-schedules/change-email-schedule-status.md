---
type: API Endpoint
title: Change Email Schedule Status
description: Modify the status of the specified email schedule.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}/status"
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - email-schedules
  - put
  - modeling
api:
  operation_id: changeEmailScheduleStatus
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}/status"
  domain: schedules-and-alerts
  group: email-schedules
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace."
  error_codes:
    - 7103
    - 7301
    - 7812
    - 8002
    - 8003
    - 8004
    - 8005
    - 8119
    - 8535
  openapi:
    file: "/references/openapi/schedules-alerts-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1emailschedules~1{schedule-id}~1status/put"
    config_schema: ChangeEmailScheduleStatusConfig
    response_schema: null
  sdk_examples: "/sdk-examples/schedules-and-alerts/email-schedules/change-email-schedule-status.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/schedules-alerts-grouped-api.json"
    title: OpenAPI 3 specification - schedules-alerts-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**PUT `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}/status`** - Change Email Schedule Status (Email Schedules / Schedules & Alerts).

Activates or deactivates a schedule without deleting it. A deactivated schedule keeps its configuration and ID but stops running automatically.

From the OpenAPI specification:

Modify the status of the specified email schedule. Use this API to activate a schedule that is currently deactivated, or to deactivate one without deleting it.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `changeEmailScheduleStatus` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}/status` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`schedules-alerts-grouped-api.json`](../../../references/openapi/schedules-alerts-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1emailschedules~1{schedule-id}~1status/put`; CONFIG schema `ChangeEmailScheduleStatusConfig` |

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
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{schedule-id}` | string | ID of the email schedule. | [How to obtain](../../../foundations/identifiers.md#schedule-id) |

## CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `operation` | String (enum) | **Yes** | — | `activate` to enable the schedule, `deactivate` to disable it. Any other value is rejected with `8119`, whose message names the two permitted values. |

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload. To read the resulting state, call [Get Email Schedules](get-email-schedules.md) and inspect `isEnabled`.

# Examples

## Sample Requests

**Case 1 — Deactivate a schedule (pause it without losing its configuration)**

```http
PUT /restapi/v2/workspaces/137687000271334001/emailschedules/137687000010815003/status HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "operation": "deactivate"
}
```

**Case 2 — Activate a previously deactivated schedule**

```http
PUT /restapi/v2/workspaces/137687000271334001/emailschedules/137687000010815003/status HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "operation": "activate"
}
```

**Case 3 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
PUT /restapi/v2/workspaces/137687000271334009/emailschedules/137687000010815009/status HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "operation": "activate"
}
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. Confirm the new state with [Get Email Schedules](get-email-schedules.md) (`isEnabled`).

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — Invalid `operation` value**

```json
{
    "status": "failure",
    "summary": "INVALID_VALUE_FOR_ATTRIBUTE",
    "data": {
        "errorCode": 8119,
        "errorMessage": "Invalid value 'pause' for the attribute 'operation'. Allowed values are activate and deactivate."
    }
}
```

**HTTP 403 Forbidden — Request sent through a Client Portal / White Label domain (Case 3)**

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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Change Email Schedule Status](../../../sdk-examples/schedules-and-alerts/email-schedules/change-email-schedule-status.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Change Email Schedule Status returns a bare HTTP `204 No Content` — no `status`/`summary` JSON to parse. |
| **`operation` is a strict two-value enum** | Only the exact lowercase strings `activate` and `deactivate` are accepted. Anything else — including `true`/`false`, `enable`/`disable`, or different casing — fails with `8119`. |
| **Idempotent** | Activating an already-active schedule, or deactivating an already-inactive one, succeeds without error. |
| **The ID never changes** | Unlike [Update Email Schedule](update-email-schedule.md), this call never regenerates `scheduleId` — it only flips the run state. |
| **Deactivation preserves everything** | Recipients, period, views, format, and the ID all survive. Reactivating resumes the schedule at its next natural occurrence; missed occurrences are not backfilled. |
| **Deactivated schedules can still be triggered manually** | [Trigger Email Schedule](trigger-email-schedule.md) works regardless of `isEnabled`. |
| **Quota effects** | A deactivated schedule stops counting toward the active-schedule quota; reactivating it re-checks the quota and can fail if the organization is now at its limit. |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get Email Schedules](get-email-schedules.md) (read current `isEnabled`) → Change Email Schedule Status → [Get Email Schedules](get-email-schedules.md) to verify. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — Request came through a Client Portal / White Label domain, or the user lacks Create Email Schedule permission on the workspace. | Call from the standard API host with the required permission. |
| [7812](../../../foundations/error-codes.md#error-7812) | 400 | `SCHEDULE_DELETED` — No schedule exists with the given `<schedule-id>`. | Re-resolve the current ID via [Get Email Schedules](get-email-schedules.md). |
| [8002](../../../foundations/error-codes.md#error-8002) | 400 | `SCHMAIL_ACTION_NOTSUPPORTED` — The schedule is not in this workspace, or the caller may not act on it. | Verify the ID belongs to this workspace. |
| [8003](../../../foundations/error-codes.md#error-8003) | 400 | `ALL_SCH_RUNERROR` — The schedule could not be activated. | Check that the schedule's views still exist and that the organization is within its schedule quota. |
| [8004](../../../foundations/error-codes.md#error-8004) | 400 | `ALL_SCH_PAUSEERROR` — The schedule could not be deactivated. | Retry; if it persists, verify the schedule still exists. |
| [8005](../../../foundations/error-codes.md#error-8005) | 400 | `SCH_NOT_IN_WS` — The schedule does not belong to the specified workspace. | Ensure `<workspace-id>` and `<schedule-id>` are consistent. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE` — `operation` is neither `activate` nor `deactivate`. | Send exactly `activate` or `deactivate`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.update`. |

# Related

- [Email Schedules overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Schedules & Alerts](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Email Schedules](get-email-schedules.md), [Create Email Schedule](create-email-schedule.md), [Update Email Schedule](update-email-schedule.md), [Delete Email Schedule](delete-email-schedule.md), [Trigger Email Schedule](trigger-email-schedule.md).
- [SDK examples](../../../sdk-examples/schedules-and-alerts/email-schedules/change-email-schedule-status.md).
