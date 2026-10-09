---
type: API Endpoint
title: Trigger Email Schedule
description: "Trigger the specified email schedule instantly, without waiting for its configured run time."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - email-schedules
  - post
  - modeling
api:
  operation_id: triggerEmailSchedule
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}"
  domain: schedules-and-alerts
  group: email-schedules
  oauth_scopes:
    - ZohoAnalytics.modeling.create
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace. Export must also be enabled for the organization and for the workspace."
  error_codes:
    - 7103
    - 7106
    - 7301
    - 7812
    - 8002
    - 8005
    - 8030
    - 8032
    - 8535
  openapi:
    file: "/references/openapi/schedules-alerts-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1emailschedules~1{schedule-id}/post"
    config_schema: null
    response_schema: null
  sdk_examples: "/sdk-examples/schedules-and-alerts/email-schedules/trigger-email-schedule.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/schedules-alerts-grouped-api.json"
    title: OpenAPI 3 specification - schedules-alerts-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}`** - Trigger Email Schedule (Email Schedules / Schedules & Alerts).

Runs a schedule immediately — the "send now" action. **This sends real email to every configured recipient**, using the schedule's stored configuration.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

From the OpenAPI specification:

Trigger the specified email schedule instantly, without waiting for its configured run time.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `triggerEmailSchedule` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace. Export must also be enabled for the organization and for the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 204 with no body |
| OpenAPI | [`schedules-alerts-grouped-api.json`](../../../references/openapi/schedules-alerts-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1emailschedules~1{schedule-id}/post` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{schedule-id}` | string | ID of the email schedule. | [How to obtain](../../../foundations/identifiers.md#schedule-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload. There is no send-report, message ID, or per-recipient delivery status in the response.

# Examples

## Sample Requests

**Case 1 — Send an active schedule immediately**

```http
POST /restapi/v2/workspaces/137687000271334001/emailschedules/137687000010815003 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Send a deactivated schedule on demand (allowed)**

```http
POST /restapi/v2/workspaces/137687000271334001/emailschedules/137687000010815001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
POST /restapi/v2/workspaces/137687000271334009/emailschedules/137687000010815009 HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. The 204 confirms the send was *accepted and initiated*, not that every recipient's message was delivered.

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — The schedule no longer exists**

```json
{
    "status": "failure",
    "summary": "SCHEDULE_DELETED",
    "data": {
        "errorCode": 7812,
        "errorMessage": "This schedule has been deleted."
    }
}
```

**HTTP 404 Not Found — Every view the schedule delivered has been deleted**

```json
{
    "status": "failure",
    "summary": "META_OBJECT_NOT_PRESENT",
    "data": {
        "errorCode": 7106,
        "errorMessage": "The view is not present."
    }
}
```

**HTTP 400 Bad Request — Export disabled for the organization**

```json
{
    "status": "failure",
    "summary": "EMAILEXPORT_DISABLED_IN_ORG",
    "data": {
        "errorCode": 8030,
        "errorMessage": "Email export is disabled for this organization."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Trigger Email Schedule](../../../sdk-examples/schedules-and-alerts/email-schedules/trigger-email-schedule.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Trigger Email Schedule returns a bare HTTP `204 No Content` — no `status`/`summary` JSON to parse, and no delivery report. |
| **It sends real email** | There is no dry-run or preview mode. Every configured recipient and CC address receives the export. Be careful when testing against a production schedule. |
| **Beware the verb** | `POST /emailschedules/<schedule-id>` triggers a send, while `PUT` on the same path updates the schedule. Sending POST where PUT was intended emails everyone. |
| **Works on deactivated schedules** | `isEnabled: false` only stops *automatic* runs; a manual trigger still sends. |
| **Does not shift the recurring timetable** | A manual send is a one-off. The schedule's next automatic occurrence is unchanged, and the manual run does not consume one. |
| **All views must still exist** | If every view the schedule delivered has been deleted, the trigger fails with `7106`. |
| **Export gates apply at send time** | Organization-level and workspace-level export restrictions are re-checked on every trigger, so a schedule created while export was enabled can start failing with `8030` later. |
| **204 means accepted, not delivered** | Mail generation and delivery continue asynchronously; per-recipient failures are not reported through this API. |
| **The ID never changes** | Triggering never regenerates `scheduleId`. |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get Email Schedules](get-email-schedules.md) → `<schedule-id>` → Trigger Email Schedule. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7106](../../../foundations/error-codes.md#error-7106) | 404 | `META_OBJECT_NOT_PRESENT` — The schedule has no surviving views to send. | Recreate the schedule against existing views. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — Request came through a Client Portal / White Label domain, or the user lacks Create Email Schedule permission on the workspace. | Call from the standard API host with the required permission. |
| [7812](../../../foundations/error-codes.md#error-7812) | 400 | `SCHEDULE_DELETED` — No schedule exists with the given `<schedule-id>`. | Re-resolve the current ID via [Get Email Schedules](get-email-schedules.md). |
| [8002](../../../foundations/error-codes.md#error-8002) | 400 | `SCHMAIL_ACTION_NOTSUPPORTED` — The schedule is not in this workspace, or the caller may not act on it. | Verify the ID belongs to this workspace. |
| [8005](../../../foundations/error-codes.md#error-8005) | 400 | `SCH_NOT_IN_WS` — The schedule does not belong to the specified workspace. | Ensure `<workspace-id>` and `<schedule-id>` are consistent. |
| [8030](../../../foundations/error-codes.md#error-8030) | 400 | `EMAILEXPORT_DISABLED_IN_ORG` — Email export is disabled for this organization. | Ask the Organization Admin to enable export in Security Controls. |
| [8032](../../../foundations/error-codes.md#error-8032) | 400 | `EMAILINGVIEW_DISABLED` — Emailing is disabled for a view in this schedule. | Check the view's and workspace's export settings. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |

# Related

- [Email Schedules overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Schedules & Alerts](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Email Schedules](get-email-schedules.md), [Create Email Schedule](create-email-schedule.md), [Update Email Schedule](update-email-schedule.md), [Delete Email Schedule](delete-email-schedule.md), [Change Email Schedule Status](change-email-schedule-status.md).
- [SDK examples](../../../sdk-examples/schedules-and-alerts/email-schedules/trigger-email-schedule.md).
