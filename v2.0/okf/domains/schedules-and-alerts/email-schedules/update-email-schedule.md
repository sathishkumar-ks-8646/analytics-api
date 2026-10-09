---
type: API Endpoint
title: Update Email Schedule
description: "Updates an existing schedule's name, run period, recipients, or email content."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - email-schedules
  - put
  - modeling
api:
  operation_id: updateEmailSchedule
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}"
  domain: schedules-and-alerts
  group: email-schedules
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace. A custom-role user whose role does not grant access to all email schedules may update only schedules they created themselves — otherwise 8002."
  error_codes:
    - 7103
    - 7301
    - 7812
    - 8000
    - 8001
    - 8002
    - 8005
    - 8031
    - 8033
    - 8119
    - 8241
    - 8535
  openapi:
    file: "/references/openapi/schedules-alerts-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1emailschedules~1{schedule-id}/put"
    config_schema: UpdateEmailScheduleConfig
    response_schema: UpdateEmailScheduleResponse
  sdk_examples: "/sdk-examples/schedules-and-alerts/email-schedules/update-email-schedule.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/schedules-alerts-grouped-api.json"
    title: OpenAPI 3 specification - schedules-alerts-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

**PUT `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}`** - Update Email Schedule (Email Schedules / Schedules & Alerts).

Updates an existing schedule's name, run period, recipients, or email content. **Read [Schedule ID Lifecycle](overview.md#schedule-id-lifecycle) first** — this call can replace the schedule's ID.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `updateEmailSchedule` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace. A custom-role user whose role does not grant access to all email schedules may update only schedules they created themselves — otherwise 8002. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`schedules-alerts-grouped-api.json`](../../../references/openapi/schedules-alerts-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1emailschedules~1{schedule-id}/put`; CONFIG schema `UpdateEmailScheduleConfig`; response schema `UpdateEmailScheduleResponse` |

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

CONFIG is **mandatory**, but every field inside it is optional: **omitted fields retain their current values**. Note that `viewIds` and `exportType` are absent from this API entirely — they cannot be changed after creation.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `scheduleName` | String | No | unchanged | New name for the schedule. Must remain unique within the workspace. **Changing this regenerates `scheduleId`.** |
| `scheduleDetails` | JSONObject | No | unchanged | New run frequency and time. Must be a **complete** object — it is not merged field-by-field with the existing period. See [`scheduleDetails` Fields](create-email-schedule.md#scheduledetails-fields). **Changing the effective period regenerates `scheduleId`.** |
| `emailIds` | JSONArray of String | No | unchanged | **Replaces** the recipient list, 0–1000 entries. Does not regenerate the ID. |
| `groupIds` | JSONArray of String/Long | No | unchanged | **Replaces** the recipient group list, 0–1000 entries. Does not regenerate the ID. |
| `cc` | JSONObject | No | unchanged | **Replaces** the carbon-copy configuration. See [`cc` Fields](create-email-schedule.md#cc-fields). Supplying `cc` with only `emailIds` leaves `cc.groupIds` unchanged, and vice versa. |
| `isBCC` | Boolean | No | unchanged | Whether recipients are addressed via BCC. |
| `subject` | String | No | unchanged | New subject line. Max 500 characters. |
| `message` | String | No | unchanged | New body text. Max 5,000 characters. HTML is sanitised. |
| `selectedTabs` | JSONArray | No | unchanged | For tabbed dashboards, the tabs to deliver. 0–30 entries. |
| `reportBurstConfig` | JSONObject | No | — | Report-burst configuration. See [`reportBurstConfig` Fields](create-email-schedule.md#reportburstconfig-fields). **Omitting it removes any existing burst configuration**, converting the schedule back to a normal one — this is the one field where omission is not "leave unchanged". |
| `validateSystemTags` | Boolean | No | `true` | If `true`, the request is rejected with `8241` when a view delivered by this schedule carries a restricted DATA_WARNING system tag. Pass `false` to acknowledge and proceed. |

## Notes from the OpenAPI specification

The attributes inside scheduleDetails apply based on the calendarFrequency value.
- weekDay and weekDays - applicable for weekly schedules.
- weekNumber, monthDay and monthDays - applicable for monthly schedules.
- months - applicable for yearly schedules, along with the relevant day attributes.

validateSystemTags is applicable only when System Tags are enabled for your organization. When it is set to true, a view shared by this schedule that carries an Outdated tag - applied directly, or inherited through lineage from a parent Data Source or Table - causes the request to be rejected, and no views are shared.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Update email schedule"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.scheduleId` | String | **The effective schedule ID after the update**, serialised as a string. Equal to the `<schedule-id>` from the request URL when the ID was preserved, and a **different, newly minted ID** when the name or run period changed. Always read this value and replace any stored ID — see [Schedule ID Lifecycle](overview.md#schedule-id-lifecycle). The response gives no separate flag telling you which happened; compare it against the ID you sent. |

# Examples

## Sample Requests

**Case 1 — Recipients and email content only (`scheduleId` is preserved)**

```http
PUT /restapi/v2/workspaces/137687000271334001/emailschedules/137687000010815003 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "emailIds": [
        "jane.doe@example.com",
        "new.recipient@example.com"
    ],
    "cc": {
        "emailIds": ["manager@example.com"]
    },
    "isBCC": true,
    "subject": "Weekly Sales Report (updated)",
    "message": "The recipient list for this report has been updated."
}
```

**Case 2 — Rename and re-schedule to daily (`scheduleId` is regenerated)**

```http
PUT /restapi/v2/workspaces/137687000271334001/emailschedules/137687000010815003 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scheduleName": "Daily Sales Overview",
    "scheduleDetails": {
        "calendarFrequency": "daily",
        "hour": 10,
        "minute": 30
    },
    "subject": "Daily Sales Overview"
}
```

**Case 3 — Switch to a yearly period with new recipients (`scheduleId` is regenerated)**

```http
PUT /restapi/v2/workspaces/137687000271334001/emailschedules/137687000010815001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scheduleName": "Annual Revenue Report",
    "scheduleDetails": {
        "calendarFrequency": "yearly",
        "hour": 7,
        "minute": 0,
        "months": [1, 7],
        "monthDay": 1
    },
    "emailIds": ["finance@example.com"],
    "groupIds": ["137687000006991700"],
    "cc": {
        "emailIds": ["manager@example.com"],
        "groupIds": ["137687000006991701"]
    },
    "subject": "Annual Revenue Report",
    "message": "Here is your updated schedule report."
}
```

**Case 4 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
PUT /restapi/v2/workspaces/137687000271334009/emailschedules/137687000010815009 HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "subject": "Portal report"
}
```

## Sample Responses

**HTTP 200 OK — ID preserved (Case 1): `scheduleId` matches the one in the request URL**

```json
{
    "status": "success",
    "summary": "Update email schedule",
    "data": {
        "scheduleId": "137687000010815003"
    }
}
```

**HTTP 200 OK — ID regenerated (Cases 2 and 3): `scheduleId` differs from the one in the request URL**

```json
{
    "status": "success",
    "summary": "Update email schedule",
    "data": {
        "scheduleId": "137687000010887001"
    }
}
```

**HTTP 400 Bad Request — The schedule no longer exists (e.g. a stale ID after a previous regenerating update)**

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

**HTTP 400 Bad Request — Custom-role user editing a schedule they do not own**

```json
{
    "status": "failure",
    "summary": "SCHMAIL_ACTION_NOTSUPPORTED",
    "data": {
        "errorCode": 8002,
        "errorMessage": "Sorry, you do not have permission to Edit Email Schedule."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Update Email Schedule](../../../sdk-examples/schedules-and-alerts/email-schedules/update-email-schedule.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **The ID may change — compare, don't assume** | Changing `scheduleName` or the effective run period deletes the old scheduler entry and creates a new one. Compare `data.scheduleId` with the `<schedule-id>` you sent to detect it. |
| **True partial update** | Every field falls back to its stored value when omitted, including `scheduleName` and `scheduleDetails`. A CONFIG containing only `subject` is valid and changes only the subject. |
| **`reportBurstConfig` is the exception to "omitted means unchanged"** | Omitting it **clears** any existing burst configuration. To keep a burst schedule bursting, resend the whole `reportBurstConfig` object on every update. |
| **List fields replace, never merge** | `emailIds`, `groupIds`, `cc.emailIds`, `cc.groupIds`, and `selectedTabs` each overwrite the stored list wholesale. To add one recipient, resend the full list. |
| **`scheduleDetails` must be complete** | It is parsed as a whole into a new run period. Sending only `hour` without `calendarFrequency` fails; send the full object. |
| **`viewIds` and `exportType` cannot be changed** | They are not accepted here. Delivering different views or a different format requires deleting and recreating the schedule. |
| **Still needs at least one recipient** | If the update leaves the schedule with no resolvable recipient, it fails with `8033` and nothing is saved. |
| **Ownership matters for custom roles** | A custom-role user without organization-wide email-schedule access can only update schedules whose `createdBy` is their own address (`8002` otherwise). Check `createdBy` via [Get Email Schedules](get-email-schedules.md). |
| **Quota is re-evaluated** | Growing the recipient list, or turning on per-recipient filtering, can push the organization over its schedule quota and fail the update. |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get Email Schedules](get-email-schedules.md) (resolve the current `scheduleId` and `createdBy`) → Update Email Schedule → read `data.scheduleId` → store it. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — Request came through a Client Portal / White Label domain, or the user lacks Create Email Schedule permission on the workspace. | Call from the standard API host with the required permission. |
| [7812](../../../foundations/error-codes.md#error-7812) | 400 | `SCHEDULE_DELETED` — No schedule exists with the given `<schedule-id>`. Commonly a **stale ID after an earlier update regenerated it**. | Re-resolve the current ID via [Get Email Schedules](get-email-schedules.md). |
| [8000](../../../foundations/error-codes.md#error-8000) | 400 | `DUPLICATE_SCHEDULE` — Another schedule in the workspace already uses the requested `scheduleName`. | Choose a different name. |
| [8001](../../../foundations/error-codes.md#error-8001) | 400 | `MAILCOUNT_PER_SCHED_EXCEED` — Too many recipients after the update. | Reduce the recipient list. |
| [8002](../../../foundations/error-codes.md#error-8002) | 400 | `SCHMAIL_ACTION_NOTSUPPORTED` — The schedule is not in this workspace, or a custom-role user attempted to edit a schedule they do not own. | Verify the ID belongs to this workspace; otherwise have the schedule's creator or an admin perform the update. |
| [8005](../../../foundations/error-codes.md#error-8005) | 400 | `SCH_NOT_IN_WS` — The schedule does not belong to the specified workspace. | Ensure `<workspace-id>` and `<schedule-id>` are consistent. |
| [8031](../../../foundations/error-codes.md#error-8031) | 400 | `UNTRUSTED_EMAILIDS` — A recipient address is outside the organization's trusted domains. | Use trusted-domain addresses. |
| [8033](../../../foundations/error-codes.md#error-8033) | 400 | `MAILSCH_SELECT_ATLEASTONE_EMAILID` — The update would leave the schedule with no recipients. | Keep at least one address or non-empty group. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE` — A `scheduleDetails` value is out of range. | The error message names the attribute and its permitted range. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | `SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION` — A delivered view carries a restricted DATA_WARNING system tag. | Review the warning, then resend with `"validateSystemTags": false`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.update`. |

# Related

- [Email Schedules overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Schedules & Alerts](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Email Schedules](get-email-schedules.md), [Create Email Schedule](create-email-schedule.md), [Delete Email Schedule](delete-email-schedule.md), [Change Email Schedule Status](change-email-schedule-status.md), [Trigger Email Schedule](trigger-email-schedule.md).
- [SDK examples](../../../sdk-examples/schedules-and-alerts/email-schedules/update-email-schedule.md).
