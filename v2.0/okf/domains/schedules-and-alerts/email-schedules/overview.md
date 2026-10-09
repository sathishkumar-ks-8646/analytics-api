---
type: API Group
title: Email Schedules
description: "APIs for creating, updating, triggering, and deleting email schedules, and retrieving schedule details."
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - email-schedules
  - api-group
api:
  domain: schedules-and-alerts
  group: email-schedules
  endpoint_count: 6
  endpoints:
    - operation_id: getEmailSchedules
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/emailschedules"
      doc: "/domains/schedules-and-alerts/email-schedules/get-email-schedules.md"
    - operation_id: createEmailSchedule
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/emailschedules"
      doc: "/domains/schedules-and-alerts/email-schedules/create-email-schedule.md"
    - operation_id: updateEmailSchedule
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}"
      doc: "/domains/schedules-and-alerts/email-schedules/update-email-schedule.md"
    - operation_id: deleteEmailSchedule
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}"
      doc: "/domains/schedules-and-alerts/email-schedules/delete-email-schedule.md"
    - operation_id: changeEmailScheduleStatus
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}/status"
      doc: "/domains/schedules-and-alerts/email-schedules/change-email-schedule-status.md"
    - operation_id: triggerEmailSchedule
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}"
      doc: "/domains/schedules-and-alerts/email-schedules/trigger-email-schedule.md"
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

This document covers the V2 **Email Schedule** REST APIs of Zoho Analytics — the APIs that create, list, update, enable/disable, trigger, and delete recurring email deliveries of views (tables, charts, pivots, summaries, dashboards, query tables) to a set of recipients.

APIs for creating, updating, triggering, and deleting email schedules, and retrieving schedule details.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Email Schedules](get-email-schedules.md) | GET | `/restapi/v2/workspaces/{workspace-id}/emailschedules` | `getEmailSchedules` | `ZohoAnalytics.metadata.read` | 200 |
| [Create Email Schedule](create-email-schedule.md) | POST | `/restapi/v2/workspaces/{workspace-id}/emailschedules` | `createEmailSchedule` | `ZohoAnalytics.modeling.create` | 200 |
| [Update Email Schedule](update-email-schedule.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}` | `updateEmailSchedule` | `ZohoAnalytics.modeling.update` | 200 |
| [Delete Email Schedule](delete-email-schedule.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}` | `deleteEmailSchedule` | `ZohoAnalytics.modeling.delete` | 204 |
| [Change Email Schedule Status](change-email-schedule-status.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}/status` | `changeEmailScheduleStatus` | `ZohoAnalytics.modeling.update` | 204 |
| [Trigger Email Schedule](trigger-email-schedule.md) | POST | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}` | `triggerEmailSchedule` | `ZohoAnalytics.modeling.create` | 204 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is an "Email Schedule" in Zoho Analytics?

An **email schedule** is a named, recurring job that exports one or more views in a chosen file format and emails them to a list of recipients — individual email addresses, workspace groups, or both — at a frequency you define. It has four moving parts:

| Part | CONFIG attribute(s) | Notes |
|------|--------------------|-------|
| **What is sent** | `viewIds`, `exportType`, `selectedTabs` | Which views, in which file format. Fixed at creation — `viewIds` and `exportType` cannot be changed later. |
| **When it runs** | `scheduleDetails` | Frequency, time of day, and the day/week/month selectors that apply to that frequency. |
| **Who receives it** | `emailIds`, `groupIds`, `cc`, `isBCC` | Recipients may be raw email addresses or workspace groups; a carbon-copy list is separate. |
| **How it reads** | `scheduleName`, `subject`, `message`, `applyShareCriteria`, `applyDefaultUf` | Naming, email body, and whether each recipient sees data filtered to their own share criteria. |

> **The single most important behaviour:** updating a schedule can **replace its ID**. See [Schedule ID Lifecycle](overview.md#schedule-id-lifecycle) before writing any integration that stores schedule IDs.

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`). The read API uses the **`metadata`** scope family; the five write APIs use the **`modeling`** scope family — see [OAuth scopes](../../../foundations/oauth-scopes.md).
> - All six APIs are **workspace-scoped** (`/workspaces/<workspace-id>/emailschedules...`) and require the `ZANALYTICS-ORGID` header.
> - **All six APIs are disabled in Client Portal / White Label request contexts.** A request that arrives through a custom domain is rejected with [`7301`](../../../foundations/error-codes.md#error-7301) before any business logic runs — see [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour).
> - Email schedules consume a per-organization **schedule quota**. See [Quota Consumption](overview.md#quota-consumption).
> - None of these APIs accepts a `criteria` attribute. Row-level filtering for a schedule is driven by `applyShareCriteria` (each recipient receives data filtered by the share criteria already configured for them), not by a per-request filter expression.

---

# Schedule ID Lifecycle

This is the behaviour that most often surprises integrators, so it is documented up front.

**[Update Email Schedule](update-email-schedule.md) does not always update in place.** Depending on what changed, the server either edits the existing scheduler entry or **deletes it and inserts a brand-new one with a new `scheduleId`**.

| What you change in the update CONFIG | Result |
|---|---|
| `scheduleName` | **New `scheduleId` is minted.** The old scheduler entry is deleted. |
| Anything inside `scheduleDetails` that alters the effective run period (`calendarFrequency`, `hour`, `minute`, `skipFrequency`, `weekDays`, `weekDay`, `weekNumber`, `monthDay`, `monthDays`, `months`) | **New `scheduleId` is minted.** The old scheduler entry is deleted. |
| `emailIds`, `groupIds`, `cc`, `subject`, `message`, `isBCC`, `selectedTabs`, `reportBurstConfig` — with `scheduleName` and `scheduleDetails` unchanged or omitted | **`scheduleId` is preserved.** The existing entry is edited in place. |

The rule the server applies is: **keep the ID only if the schedule name and the computed run period are both byte-for-byte identical to the stored values.** Any difference in either one causes regeneration. (A third input, the schedule's timezone, also participates in this comparison, but the V2 update path always carries the stored timezone forward, so it can never be the cause.)

Practical consequences:

1. **The response is authoritative.** `data.scheduleId` in the [Update Email Schedule](update-email-schedule.md) response is always the *effective* ID after the call — the new one if it was regenerated, the same one otherwise. Read it and replace whatever you had stored.
2. **The `<schedule-id>` in your request URL may be dead the moment the call returns.** A second update using the old path ID will fail with [`7812`](../../../foundations/error-codes.md#error-7812) `SCHEDULE_DELETED`.
3. **Re-sending the current name and period is safe.** Because the comparison is on values, not on presence, a "write the whole object back" update that happens to send identical `scheduleName` and `scheduleDetails` keeps the ID.
4. **Renaming and re-scheduling are not free.** Both are structural changes that destroy and recreate the underlying scheduler task. Anything keyed off the old ID externally (dashboards, logs, your own database) needs remapping.
5. **The last-run history does not follow the new ID.** Because the old entry is deleted, run history and audit rows associated with the previous ID do not carry over to the new one.

If your integration needs stable identifiers, key your own records on `scheduleName` (unique within a workspace) rather than on `scheduleId`, and resolve the current ID through [Get Email Schedules](get-email-schedules.md) before each write.

---

# White Label / Client Portal Behaviour

All six APIs are blocked in Client Portal / White Label request contexts — the same posture as the [Embed URL APIs](../../share-and-publish/embed-url/overview.md#white-label--client-portal-behaviour), and the opposite of the [Publish](../../share-and-publish/publish/overview.md) and [Slideshow](../../share-and-publish/slideshow-management/overview.md) families.

| Scenario | Result |
|----------|--------|
| The API request arrives **through** a Client Portal / White Label custom domain | **Rejected with `7301`** before any business logic runs. Email schedules cannot be managed from a portal-domain context at all. |
| The API request is sent to the **standard API host** for a workspace that happens to be white-labelled | **Allowed**, and behaves exactly as for any other workspace. |

There is no `domainName` CONFIG attribute on any of these APIs — the commented-out entries in the request templates are not active. Manage schedules for a white-labelled workspace by calling the standard `analyticsapi.zoho.*` host.

---

# Quota Consumption

Each schedule consumes one or more units from the organization's email-schedule quota, reported per schedule as `schedulesConsumed` in the [Get Email Schedules](get-email-schedules.md) response:

| Configuration | Units consumed |
|---|---|
| Default (no share criteria) | `ceil((recipients + cc recipients) / 25)` — one unit per 25 addresses. |
| `applyShareCriteria: true` | **One unit per recipient**, because each recipient receives an individually filtered export. |

A create or update that would push the organization past its quota is rejected before anything is saved.

---

# API-Specific Notes and Behaviours

## Get Email Schedules

- **The entry point, and the only recovery path for a regenerated ID.** Every other API needs a `<schedule-id>`, and after an update that changed the name or period this is how you rediscover the new one. Treat it as the first call in any schedule workflow.
- **It is a summary, not the full configuration.** Recipients, CC list, `exportType`, `applyShareCriteria`, and `applyDefaultUf` are not returned, and no other API returns them either. An integration that needs to round-trip a schedule must retain its own copy of what it sent.
- **`schedulePeriod` is display prose, not data.** It is generated in the schedule's timezone with wording that varies by frequency (`"weekly on Friday at 14:10 IST"`, `"Every 6 days at 10:50 GMT"`). It is not the `scheduleDetails` you sent and must never be parsed to rebuild one.
- **`views` and `selectedTabs` are alternatives.** Tabbed-dashboard schedules report `selectedTabs` in place of `views`. Handle both keys.
- **`createdBy` is a permission signal.** For custom-role users without organization-wide email-schedule access, only entries whose `createdBy` matches their own address can be updated, deleted, or triggered — check it before offering those actions in a UI.
- **Different scope group from the write APIs.** This is the one API in the family on `metadata.read`; the other five are on `modeling.*`.
- **Dependency chain:** [Get Workspace List](../../workspace-management/workspace-operations/overview.md) → Get Email Schedules → `<schedule-id>` for every other API here.

## Create Email Schedule

- **`viewIds` and `exportType` are set for life.** Neither can be changed by [Update Email Schedule](update-email-schedule.md). Getting them wrong means deleting the schedule and starting over, which also loses its run history — so validate view IDs and format compatibility before the first call.
- **Format rules are view-type dependent and enforced hard.** `XLS` accepts exactly one view; `IMG` accepts only charts; a dashboard must be scheduled alone and only as `PDF` or `HTML`. These are four distinct error codes ([`8037`](../../../foundations/error-codes.md#error-8037), [`8036`](../../../foundations/error-codes.md#error-8036), [`8034`](../../../foundations/error-codes.md#error-8034), [`8035`](../../../foundations/error-codes.md#error-8035)) rather than one generic failure.
- **Recipients default to BCC.** `isBCC` defaults to `true`, so unless you set it to `false` recipients will not see one another — a deliberate privacy default that surprises people expecting a visible To line.
- **`applyShareCriteria` is the per-recipient personalisation switch, and it is expensive.** It changes quota consumption from one unit per 25 addresses to **one unit per recipient**. On a 200-person list that is the difference between 8 units and 200.
- **Uniqueness is on the name, and the name is also an ID-stability input.** A `scheduleName` must be unique in the workspace, and — because renaming regenerates the ID — it is the most stable key an integration can hold. Choose names deliberately.
- **No per-request row filter.** There is no `criteria` attribute. Row-level personalisation comes from `applyShareCriteria`, `applyDefaultUf`, or `reportBurstConfig`.
- **Dependency chain:** [Get View List](../../views-management/view-operations/get-views.md) + [Get Group List](../../users-and-groups/workspace-groups/get-groups.md) → Create Email Schedule → [Get Email Schedules](get-email-schedules.md).

## Update Email Schedule

- **It can replace the schedule's identity — the defining behaviour of this API.** Changing `scheduleName` or the effective run period deletes the underlying scheduler entry and inserts a new one with a new `scheduleId`; the old ID is then dead and returns [`7812`](../../../foundations/error-codes.md#error-7812) on the next call. Changing only recipients or email content edits in place. Always read `data.scheduleId` from the response and compare it against what you sent. Full rules in [Schedule ID Lifecycle](overview.md#schedule-id-lifecycle).
- **It returns 200 with a body, unlike most V2 PUTs.** The body exists precisely to carry the possibly-new ID back, so this is one PUT whose response must never be ignored.
- **Genuinely partial — but with one trap.** Every omitted field keeps its stored value, *except* `reportBurstConfig`, whose omission **clears** the burst configuration. Burst schedules must resend it on every update.
- **List fields replace rather than merge.** Adding one recipient means resending the entire `emailIds` array; the same applies to `groupIds`, `cc.*`, and `selectedTabs`.
- **`scheduleDetails` is all-or-nothing.** It is parsed as a complete period definition, not merged field-by-field with the stored one.
- **Ownership gate for custom roles.** A custom-role user without organization-wide email-schedule access can only update schedules they created ([`8002`](../../../foundations/error-codes.md#error-8002)), so check `createdBy` from [Get Email Schedules](get-email-schedules.md) first.
- **Dependency chain:** [Get Email Schedules](get-email-schedules.md) → Update Email Schedule → read `data.scheduleId` → store the effective ID.

## Delete Email Schedule

- **204 No Content, no body.** Verified against the implementation.
- **Views survive; the schedule does not.** Only the schedule definition, its pending runs, and its history are removed — nothing about the delivered reports, dashboards, or tables changes.
- **No trash and no restore.** Unlike views, which go through the [Trash APIs](../../views-management/trash-management/overview.md), a deleted schedule is gone. Recreating it yields a new `scheduleId` and an empty run history.
- **Not idempotent.** A repeat delete fails with [`7812`](../../../foundations/error-codes.md#error-7812). The same code also appears when the ID went stale because an earlier update regenerated it — so a [`7812`](../../../foundations/error-codes.md#error-7812) is not always "already deleted".
- **Frees quota immediately.** A create that previously failed on the organization's schedule limit may succeed right after a delete.
- **Same ownership gate as Update.** Custom-role users without full access can only delete their own schedules.
- **Dependency chain:** [Get Email Schedules](get-email-schedules.md) → Delete Email Schedule.

## Change Email Schedule Status

- **204 No Content, no body.** Verified against the implementation.
- **The safe alternative to deleting.** Deactivation preserves the configuration, the recipients, and — importantly — the `scheduleId`. Use it for temporary pauses instead of delete-and-recreate, which would change the ID and lose history.
- **A strict two-value enum with an unusual shape.** `operation` accepts only the exact lowercase strings `activate` and `deactivate` — not booleans, not `enable`/`disable`. This is the only status-style API in the suite that uses a verb string rather than a `status` boolean, so it is easy to get wrong; the [`8119`](../../../foundations/error-codes.md#error-8119) message names both valid values.
- **Idempotent, unlike most write APIs here.** Re-activating an active schedule or re-deactivating an inactive one is a no-op rather than an error.
- **Deactivation does not block manual sends.** [Trigger Email Schedule](trigger-email-schedule.md) still works on an inactive schedule.
- **Reactivation re-checks quota.** A schedule paused while the organization had headroom can fail to reactivate ([`8003`](../../../foundations/error-codes.md#error-8003)) if the quota has since been consumed.
- **Dependency chain:** [Get Email Schedules](get-email-schedules.md) (read `isEnabled`) → Change Email Schedule Status → verify.

## Trigger Email Schedule

- **204 No Content, no body.** Verified against the implementation.
- **It is a live send with no dry-run.** Every recipient and CC address receives the export immediately. There is no preview, no send-to-self mode, and no way to undo it — treat it as a production action even in testing.
- **The most dangerous verb collision in the suite.** `POST /emailschedules/<schedule-id>` triggers a send while `PUT` on the exact same path updates the schedule. A client that gets the method wrong emails the entire recipient list instead of editing a subject line.
- **Works on deactivated schedules.** `isEnabled: false` suppresses only automatic runs.
- **Does not disturb the recurring timetable.** The next scheduled occurrence is unaffected and the manual run does not consume one.
- **Export gates are re-evaluated at send time.** Organization-level and workspace-level export restrictions are checked on every trigger, so a long-standing schedule can begin failing with [`8030`](../../../foundations/error-codes.md#error-8030) after an admin disables export.
- **204 means accepted, not delivered.** Generation and delivery proceed asynchronously and per-recipient failures are not surfaced by this API.
- **Dependency chain:** [Get Email Schedules](get-email-schedules.md) → Trigger Email Schedule.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Three of six APIs return 204 with no body** | [Delete Email Schedule](delete-email-schedule.md), [Change Email Schedule Status](change-email-schedule-status.md), and [Trigger Email Schedule](trigger-email-schedule.md) return HTTP **204 No Content** on success — treat the 2xx status code as the success indicator and never expect or parse a JSON body. The other three return the standard `{"status", "summary", "data"}` envelope with HTTP 200. |
| **Update returns 200 with a body, and that body matters** | [Update Email Schedule](update-email-schedule.md) is the exception among the write APIs: it returns `data.scheduleId`, which may be a **different ID** from the one in the request URL. Ignoring this response body is the most common way to end up with a stale ID and subsequent `7812` errors. |
| **Failure responses always carry a body** | Even for the 204 APIs, errors return `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name (e.g. `SCHEDULE_DELETED`, `SCHMAIL_ACTION_NOTSUPPORTED`), not a localised sentence. |
| **All IDs are strings** | `scheduleId` and every entry of `views` / `selectedTabs` are JSON **strings** even though the values are numeric. Parse them as strings or longs — never as native JSON numbers — to avoid precision loss on large IDs. |
| **`schedulesConsumed` and `isEnabled` are native types** | `schedulesConsumed` is a native JSON number and `isEnabled` a native boolean; everything else in the list response is a string or an array of strings. |
| **Empty array, never a missing key** | `data.emailSchedules` is always present in a successful [Get Email Schedules](get-email-schedules.md) response, empty (`[]`) when the workspace has no schedules. |
| **Conditional keys within a schedule entry** | `views` and `selectedTabs` are mutually exclusive — exactly one appears per entry depending on whether the schedule targets a tabbed dashboard. Test for key presence rather than assuming `views`. |
| **The list response is a summary, not the full record** | Recipients, CC, `exportType`, `applyShareCriteria`, `applyDefaultUf`, and `reportBurstConfig` are never returned by any API in this family. Retain your own copy of a schedule's configuration if you need to reconstruct or clone it. |
| **Responses are extensible** | Some builds return additional per-schedule fields such as `subject`, `message`, and `isBCC`. Ignore unrecognised keys rather than validating against a closed schema. |
| **`schedulePeriod` is localised prose** | Its wording and timezone abbreviation depend on the schedule and the organization, so it is unsuitable for equality checks, sorting, or parsing. Compare schedules on `scheduleId` or `scheduleName` instead. |
| **Error codes 8000–8053 in this family are email-schedule specific** | They are defined in the mail-schedule error set and are numerically distinct from the identically numbered codes used by other API families. Always match on the `summary` symbolic name in addition to `errorCode` when handling errors across families. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7106](../../../foundations/error-codes.md#error-7106) | 404 | The report does not exist or has been deleted. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7812](../../../foundations/error-codes.md#error-7812) | 400 | SCHEDULEDELETED — No schedule exists with the given <schedule-id>. |
| [7832](../../../foundations/error-codes.md#error-7832) | 400 | INVALIDEXPORTTYPE — exportType is not one of the supported formats. |
| [8000](../../../foundations/error-codes.md#error-8000) | 400 | DUPLICATESCHEDULE — A schedule with this scheduleName already exists in the workspace. |
| [8001](../../../foundations/error-codes.md#error-8001) | 400 | INVALIDRESPFORMAT — responseFormat is not a supported value. |
| [8002](../../../foundations/error-codes.md#error-8002) | 400 | SCHMAILACTIONNOTSUPPORTED — The schedule is not in this workspace, or the caller may not act on it. |
| [8003](../../../foundations/error-codes.md#error-8003) | 400 | ALLSCHRUNERROR — The schedule could not be activated. |
| [8004](../../../foundations/error-codes.md#error-8004) | 400 | ALLSCHPAUSEERROR — The schedule could not be deactivated. |
| [8005](../../../foundations/error-codes.md#error-8005) | 400 | SCHNOTINWS — The schedule does not belong to the specified workspace. |
| [8009](../../../foundations/error-codes.md#error-8009) | 400 | MAILMULTIVIEWMAXCOUNTEXCEEEDED — Too many views in one schedule. |
| [8030](../../../foundations/error-codes.md#error-8030) | 400 | EMAILEXPORTDISABLEDINORG — Email export is disabled for this organization. |
| [8031](../../../foundations/error-codes.md#error-8031) | 400 | UNTRUSTEDEMAILIDS — A recipient address is outside the organization's trusted domains. |
| [8032](../../../foundations/error-codes.md#error-8032) | 400 | VIEWNOTSHARED — The view is not currently shared with the specified user. |
| [8033](../../../foundations/error-codes.md#error-8033) | 400 | MAILSCHSELECTATLEASTONEEMAILID — No recipient could be resolved from emailIds, groupIds, and cc. |
| [8034](../../../foundations/error-codes.md#error-8034) | 400 | ONLYONEDASHBOARDISALLOWEDPERSCH — More than one view scheduled where the first is a dashboard. |
| [8035](../../../foundations/error-codes.md#error-8035) | 400 | EXPORTFORMATSALLOWEDFORDASHBOARD — Dashboard scheduled with a format other than PDF/HTML. |
| [8036](../../../foundations/error-codes.md#error-8036) | 400 | EXPORTFORMATSALLOWEDFORCHART — IMG requested for a view that is not a chart. |
| [8037](../../../foundations/error-codes.md#error-8037) | 400 | ONLYONEVIEWISALLOWEDFORXLS — XLS requested with more than one view. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | INVALIDVALUEFORATTRIBUTE — fileType, onError, delimiter, quoted, thousandSeparator, or decimalSeparator is outside its permitted set. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | SYSTEMTAGDATAWARNINGV2VALIDATIONCONFIRMATION — The view carries a restricted DATAWARNING system tag. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |

# Related

- [Schedules & Alerts](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
