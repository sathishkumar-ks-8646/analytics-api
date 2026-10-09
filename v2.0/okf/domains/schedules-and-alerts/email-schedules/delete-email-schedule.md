---
type: API Endpoint
title: Delete Email Schedule
description: Permanently deletes an email schedule.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - email-schedules
  - delete
  - modeling
api:
  operation_id: deleteEmailSchedule
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}"
  domain: schedules-and-alerts
  group: email-schedules
  oauth_scopes:
    - ZohoAnalytics.modeling.delete
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace. A custom-role user whose role does not grant access to all email schedules may delete only schedules they created themselves — otherwise 8002."
  error_codes:
    - 7103
    - 7301
    - 7812
    - 8002
    - 8005
    - 8535
  openapi:
    file: "/references/openapi/schedules-alerts-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1emailschedules~1{schedule-id}/delete"
    config_schema: null
    response_schema: null
  sdk_examples: "/sdk-examples/schedules-and-alerts/email-schedules/delete-email-schedule.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}`** - Delete Email Schedule (Email Schedules / Schedules & Alerts).

Permanently deletes an email schedule. The views it delivered are unaffected; only the schedule and its pending runs are removed.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deleteEmailSchedule` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingdelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace. A custom-role user whose role does not grant access to all email schedules may delete only schedules they created themselves — otherwise 8002. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 204 with no body |
| OpenAPI | [`schedules-alerts-grouped-api.json`](../../../references/openapi/schedules-alerts-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1emailschedules~1{schedule-id}/delete` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.delete`. See [Authentication](../../../foundations/authentication.md). |
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

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`).

# Examples

## Sample Requests

**Case 1 — Standard workspace**

```http
DELETE /restapi/v2/workspaces/137687000271334001/emailschedules/137687000010815003 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
DELETE /restapi/v2/workspaces/137687000271334009/emailschedules/137687000010815009 HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — Schedule already deleted, or an ID left stale by an earlier update**

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

**HTTP 400 Bad Request — Custom-role user deleting a schedule they do not own**

```json
{
    "status": "failure",
    "summary": "SCHMAIL_ACTION_NOTSUPPORTED",
    "data": {
        "errorCode": 8002,
        "errorMessage": "Sorry, you do not have permission to Delete Email Schedule."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Delete Email Schedule](../../../sdk-examples/schedules-and-alerts/email-schedules/delete-email-schedule.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Delete Email Schedule returns a bare HTTP `204 No Content` — no `status`/`summary` JSON to parse. |
| **Views are not affected** | Only the schedule definition and its pending runs are removed. The delivered reports, dashboards, and tables are untouched, as are their sharing and publish state. |
| **Not idempotent** | A second delete of the same `<schedule-id>` fails with `7812` `SCHEDULE_DELETED`. Guard retries with a [Get Email Schedules](get-email-schedules.md) check. |
| **No trash, no restore** | A deleted schedule cannot be recovered. Recreating it produces a new `scheduleId` and resets its run history. |
| **Frees quota** | Deleting a schedule releases the units it consumed, so a create that previously failed on quota may then succeed. |
| **Single schedule per call** | There is no bulk-delete payload; iterate over [Get Email Schedules](get-email-schedules.md) to clear several. |
| **Ownership matters for custom roles** | Same rule as Update — a custom-role user without organization-wide email-schedule access can only delete their own schedules. |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get Email Schedules](get-email-schedules.md) (confirm the schedule exists and check `createdBy`) → Delete Email Schedule. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — Request came through a Client Portal / White Label domain, or the user lacks Create Email Schedule permission on the workspace. | Call from the standard API host with the required permission. |
| [7812](../../../foundations/error-codes.md#error-7812) | 400 | `SCHEDULE_DELETED` — No schedule exists with the given `<schedule-id>`. | Nothing to delete; re-check via [Get Email Schedules](get-email-schedules.md). |
| [8002](../../../foundations/error-codes.md#error-8002) | 400 | `SCHMAIL_ACTION_NOTSUPPORTED` — The schedule is not in this workspace, or a custom-role user attempted to delete a schedule they do not own. | Verify the ID belongs to this workspace; otherwise have the creator or an admin delete it. |
| [8005](../../../foundations/error-codes.md#error-8005) | 400 | `SCH_NOT_IN_WS` — The schedule does not belong to the specified workspace. | Ensure `<workspace-id>` and `<schedule-id>` are consistent. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.delete`. |

# Related

- [Email Schedules overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Schedules & Alerts](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Email Schedules](get-email-schedules.md), [Create Email Schedule](create-email-schedule.md), [Update Email Schedule](update-email-schedule.md), [Change Email Schedule Status](change-email-schedule-status.md), [Trigger Email Schedule](trigger-email-schedule.md).
- [SDK examples](../../../sdk-examples/schedules-and-alerts/email-schedules/delete-email-schedule.md).
