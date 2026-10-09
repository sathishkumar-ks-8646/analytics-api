---
type: API Endpoint
title: Create Email Schedule
description: Creates a new recurring email schedule in the workspace and returns its ID.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/emailschedules"
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - email-schedules
  - post
  - modeling
api:
  operation_id: createEmailSchedule
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/emailschedules"
  domain: schedules-and-alerts
  group: email-schedules
  oauth_scopes:
    - ZohoAnalytics.modeling.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace. The caller must additionally hold Export permission on every view listed in viewIds."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 7319
    - 7832
    - 8000
    - 8001
    - 8009
    - 8030
    - 8031
    - 8032
    - 8033
    - 8034
    - 8035
    - 8036
    - 8037
    - 8119
    - 8241
    - 8535
  openapi:
    file: "/references/openapi/schedules-alerts-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1emailschedules/post"
    config_schema: CreateEmailScheduleConfig
    response_schema: CreateEmailScheduleResponse
  sdk_examples: "/sdk-examples/schedules-and-alerts/email-schedules/create-email-schedule.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/emailschedules`** - Create Email Schedule (Email Schedules / Schedules & Alerts).

Creates a new recurring email schedule in the workspace and returns its ID.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createEmailSchedule` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/emailschedules` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace. The caller must additionally hold Export permission on every view listed in viewIds. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`schedules-alerts-grouped-api.json`](../../../references/openapi/schedules-alerts-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1emailschedules/post`; CONFIG schema `CreateEmailScheduleConfig`; response schema `CreateEmailScheduleResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `scheduleName` | String | **Yes** | — | Name of the schedule. Must be **unique within the workspace** (`8000` otherwise). Also one of the two inputs that decide whether a later update regenerates the ID — see [Schedule ID Lifecycle](overview.md#schedule-id-lifecycle). |
| `viewIds` | JSONArray of String/Long | **Yes** | — | IDs of the views to deliver, 1–1000 entries. All must belong to `<workspace-id>`, and the caller must have Export permission on each. Duplicates are removed. **Cannot be changed after creation** — there is no `viewIds` attribute on the update API. |
| `exportType` | String (enum) | **Yes** | — | File format of the attachment. See [`exportType` Values](#exporttype-values). Case-insensitive on input, normalised to upper case. **Cannot be changed after creation.** |
| `scheduleDetails` | JSONObject | **Yes** | — | When the schedule runs. See [`scheduleDetails` Fields](#scheduledetails-fields). |
| `emailIds` | JSONArray of String | No* | — | Recipient email addresses, 0–1000 entries. Lower-cased and de-duplicated. Addresses outside a trusted domain may be rejected (`8031`). |
| `groupIds` | JSONArray of String/Long | No* | — | IDs of [workspace groups](../../users-and-groups/workspace-groups/overview.md) whose members receive the email, 0–1000 entries. Must belong to `<workspace-id>`. |
| `cc` | JSONObject | No | — | Carbon-copy recipients. See [`cc` Fields](#cc-fields). |
| `isBCC` | Boolean | No | `true` | When `true` (the default), the addresses in `emailIds` are placed in **BCC** so recipients cannot see one another. Set `false` to address them in the **To** line. |
| `subject` | String | No | System default | Subject line of the email. Max 500 characters. |
| `message` | String | No | System default | Body text of the email. Max 5,000 characters. HTML is sanitised. |
| `applyShareCriteria` | Boolean | No | `false` | When `true`, each recipient receives an export filtered by the **share criteria already configured for that user** on the view — so different recipients see different rows from one schedule. Increases quota consumption to one unit per recipient (see [Quota Consumption](overview.md#quota-consumption)). |
| `applyDefaultUf` | Boolean | No | `false` | When `true`, the view's **default user filter** values are applied to the export instead of the unfiltered view. |
| `emailAsInline` | Boolean | No | `false` | When `true`, the exported content is rendered **inline in the email body** instead of being attached as a file. Meaningful for `HTML` exports. |
| `isNormalDbExp` | Boolean | No | `false` | Dashboard export layout switch. When `true`, the dashboard is exported in the standard document layout rather than the widget-by-widget layout. Applies to dashboard schedules only. |
| `selectedTabs` | JSONArray | No | All tabs | For a **tabbed dashboard**, restricts delivery to the listed tabs. 0–30 entries. Ignored for other view types. |
| `reportBurstConfig` | JSONObject | No | — | Turns the schedule into a **report burst** — one personalised email per row of a distribution-list table. See [`reportBurstConfig` Fields](#reportburstconfig-fields). |
| `validateSystemTags` | Boolean | No | `true` | If `true`, the request is rejected with a confirmation-required error (`8241`) when any view in `viewIds` carries a restricted **DATA_WARNING** system tag — directly, or inherited through lineage from a parent data source or table. Pass `false` to acknowledge and proceed. Only relevant when System Tags are enabled for the organization. |

\* At least one delivery target is required: the combination of `emailIds`, `groupIds`, and `cc` must resolve to at least one address, otherwise error [`8033`](../../../foundations/error-codes.md#error-8033).

> The `timeZone` of a schedule is **not settable through this API**. Every schedule is created in the timezone of the workspace's Account Admin, and that timezone is preserved for the life of the schedule.

### `exportType` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `CSV` | Comma-separated values file. | Not permitted for dashboards. |
| `XLS` | Excel workbook. | **Only one view** may be scheduled (`8037` if `viewIds` has more than one). Not permitted for dashboards. |
| `PDF` | PDF document. | Permitted for all view types, including dashboards. |
| `HTML` | HTML document, attachable or inline (see `emailAsInline`). | Permitted for all view types, including dashboards. |
| `IMG` | Image file. | **Chart views only** — every view in `viewIds` must be a chart (`8036` otherwise). Not permitted for dashboards. |

> **Dashboard rules:** a schedule whose first view is a dashboard may contain **only that one view** ([`8034`](../../../foundations/error-codes.md#error-8034) otherwise) and may use only `PDF` or `HTML` ([`8035`](../../../foundations/error-codes.md#error-8035) otherwise).

### `scheduleDetails` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `calendarFrequency` | String (enum) | **Yes** | — | `daily`, `weekly`, `monthly`, or `yearly`. Determines which of the remaining fields apply. |
| `hour` | Integer | **Yes** | — | Hour of the day, **0–23**. |
| `minute` | Integer | **Yes** | — | Minute within the hour. Must be a **multiple of 5 in the range 0–55** (`0, 5, 10, … 55`). |
| `skipFrequency` | Integer | No | `0` | How many periods to skip between runs — `0` means every period, `1` means every other, and so on. The permitted maximum depends on `calendarFrequency`: **0–6** for `daily`, **0–3** for `weekly`, **0–11** for `monthly`, **0–4** for `yearly`. |
| `weekDays` | JSONArray of Integer | **Yes** for `weekly` | — | Days of the week to run on. `1` = Sunday … `7` = Saturday. |
| `weekNumber` | Integer | Conditional | — | Week of the month, **1–5**. Required for `monthly`/`yearly` when `monthDays`/`monthDay` is not supplied. |
| `weekDay` | Integer | Conditional | — | A single day of the week, `1` = Sunday … `7` = Saturday. Used together with `weekNumber`. |
| `monthDays` | JSONArray of Integer | Conditional | — | Days of the month for `monthly`. Values **1–31**, or **`99` to mean "last day of the month"**. Supply either `monthDays` **or** the `weekNumber` + `weekDay` pair. |
| `months` | JSONArray of Integer | **Yes** for `yearly` | — | Months to run in, `1` = January … `12` = December. |
| `monthDay` | Integer | Conditional | — | A single day of the month for `yearly`. Values **1–31**, or **`99` for the last day**. Supply either `monthDay` **or** the `weekNumber` + `weekDay` pair. |

**Which fields apply to which frequency:**

| `calendarFrequency` | Required alongside `hour`/`minute` | Optional |
|---|---|---|
| `daily` | — | `skipFrequency` (0–6) |
| `weekly` | `weekDays` | `skipFrequency` (0–3) |
| `monthly` | `monthDays` **or** (`weekNumber` + `weekDay`) | `skipFrequency` (0–11) |
| `yearly` | `months`, **and** `monthDay` **or** (`weekNumber` + `weekDay`) | `skipFrequency` (0–4) |

### `cc` Fields

| Field | Type | Mandatory | Description |
|-------|------|-----------|--------------|
| `emailIds` | JSONArray of String | No | Carbon-copy email addresses. Lower-cased and de-duplicated. |
| `groupIds` | JSONArray of String/Long | No | IDs of workspace groups to carbon-copy. Must belong to `<workspace-id>`. |

### `reportBurstConfig` Fields

A report burst reads a **distribution-list table** and sends one personalised email per row, filtering each report by values taken from that row.

| Field | Type | Mandatory | Description |
|-------|------|-----------|--------------|
| `zaTableId` | Long | **Yes** | ID of the table holding the distribution list (`8040` if not found). |
| `emailColumnId` | Long | **Yes** | ID of the column in that table containing the recipient email address (`8041` if not found). |
| `reports` | JSONArray | **Yes** | 1–15 report entries, each shaped as below. |
| `reports[].objId` | Long | **Yes** | ID of the view to include in the burst (`8046` if not found). |
| `reports[].exportFormat` | String | **Yes** | Export format for this report entry. |
| `reports[].deliveryMode` | Integer | No | `0` or `1` — how the report is delivered for this entry (`8047` if out of range). |
| `reports[].criteriaExpression` | String | No | Filter expression applied to this report per recipient. Max 65,535 characters. |
| `reports[].sortOrder` | Integer | No | Position of this report within the email. |
| `reports[].filterColumns` | JSONArray | No | 0–10 entries mapping distribution-list columns to report columns. |
| `reports[].filterColumns[].criteriaColumnId` | Long | **Yes** | Column in the distribution-list table supplying the filter value. |
| `reports[].filterColumns[].targetColumnId` | Long | **Yes** | Column in the report that the value filters (`8045` if not found). |

## Notes from the OpenAPI specification

The attributes inside scheduleDetails apply based on the calendarFrequency value.
- weekDay and weekDays - applicable for weekly schedules.
- weekNumber, monthDay and monthDays - applicable for monthly schedules.
- months - applicable for yearly schedules, along with the relevant day attributes.

validateSystemTags is applicable only when System Tags are enabled for your organization. When it is set to true, a view listed in viewIds that carries an Outdated tag - applied directly, or inherited through lineage from a parent Data Source or Table - causes the request to be rejected, and no views are shared.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Create Email Schedule"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.scheduleId` | String | ID of the newly created schedule, serialised as a **string**. Store it — but note it is **not permanently stable**: a later update that changes the name or the run period replaces it. See [Schedule ID Lifecycle](overview.md#schedule-id-lifecycle). |

> The response does not echo back the schedule's configuration. Confirm what was stored with [Get Email Schedules](get-email-schedules.md).

# Examples

## Sample Requests

**Case 1 — Daily CSV schedule, minimal**

```http
POST /restapi/v2/workspaces/137687000271334001/emailschedules HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scheduleName": "Daily Sales Snapshot",
    "viewIds": ["137687000006991601"],
    "exportType": "CSV",
    "scheduleDetails": {
        "calendarFrequency": "daily",
        "hour": 9,
        "minute": 0
    },
    "emailIds": ["jane.doe@example.com"],
    "subject": "Daily Sales Snapshot",
    "message": "Please find today's sales snapshot attached."
}
```

**Case 2 — Weekly PDF to users and groups, with CC, share criteria and default user filter clubbed together**

```http
POST /restapi/v2/workspaces/137687000271334001/emailschedules HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scheduleName": "Weekly Sales Report",
    "viewIds": [
        "137687000006991601",
        "137687000006991650"
    ],
    "exportType": "PDF",
    "scheduleDetails": {
        "calendarFrequency": "weekly",
        "hour": 14,
        "minute": 30,
        "weekDays": [2, 6],
        "skipFrequency": 1
    },
    "emailIds": [
        "jane.doe@example.com",
        "john.roe@example.com"
    ],
    "groupIds": ["137687000006991700"],
    "cc": {
        "emailIds": ["manager@example.com"],
        "groupIds": ["137687000006991701"]
    },
    "isBCC": false,
    "applyShareCriteria": true,
    "applyDefaultUf": true,
    "subject": "Weekly Sales Report",
    "message": "Your weekly report is attached."
}
```

**Case 3 — Monthly dashboard as inline HTML on the last day of the month, restricted to selected tabs**

```http
POST /restapi/v2/workspaces/137687000271334001/emailschedules HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scheduleName": "Monthly Revenue Board",
    "viewIds": ["137687000006991700"],
    "exportType": "HTML",
    "scheduleDetails": {
        "calendarFrequency": "monthly",
        "hour": 8,
        "minute": 15,
        "monthDays": [1, 99]
    },
    "emailIds": ["finance@example.com"],
    "emailAsInline": true,
    "isNormalDbExp": true,
    "selectedTabs": ["137687000006991710", "137687000006991711"],
    "subject": "Monthly Revenue Board",
    "validateSystemTags": false
}
```

**Case 4 — Yearly image schedule for a chart, on the second Monday of January and July**

```http
POST /restapi/v2/workspaces/137687000271334001/emailschedules HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "scheduleName": "Half-Yearly Trend Chart",
    "viewIds": ["137687000006991650"],
    "exportType": "IMG",
    "scheduleDetails": {
        "calendarFrequency": "yearly",
        "hour": 7,
        "minute": 0,
        "months": [1, 7],
        "weekNumber": 2,
        "weekDay": 2
    },
    "emailIds": ["leadership@example.com"]
}
```

## Sample Responses

**HTTP 200 OK — Schedule created**

```json
{
    "status": "success",
    "summary": "Create Email Schedule",
    "data": {
        "scheduleId": "137687000010886001"
    }
}
```

**HTTP 400 Bad Request — Duplicate schedule name**

```json
{
    "status": "failure",
    "summary": "DUPLICATE_SCHEDULE",
    "data": {
        "errorCode": 8000,
        "errorMessage": "A schedule with this name already exists in the workspace."
    }
}
```

**HTTP 403 Forbidden — Request sent through a Client Portal / White Label domain**

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

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Email Schedule](../../../sdk-examples/schedules-and-alerts/email-schedules/create-email-schedule.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`viewIds` and `exportType` are permanent** | Neither appears in the update CONFIG. To deliver different views or a different file format, delete the schedule and create a new one. |
| **Names must be unique per workspace** | A duplicate `scheduleName` fails with `8000`; the call is never turned into an update. |
| **Export permission is checked per view** | The caller must hold Export permission on **every** view in `viewIds`, in addition to the workspace-level Create Email Schedule permission. |
| **At least one resolved recipient is required** | `emailIds`, `groupIds`, and `cc` may each be omitted, but between them they must resolve to at least one address — otherwise `8033`. An empty group counts for nothing. |
| **Recipients are BCC by default** | `isBCC` defaults to **`true`**, so recipients cannot see one another unless you explicitly send `isBCC: false`. |
| **`applyShareCriteria` multiplies quota** | It changes consumption from one unit per 25 addresses to **one unit per recipient**, because each recipient gets an individually filtered export. Budget accordingly on large lists. |
| **Format restrictions are view-type dependent** | `XLS` is single-view only; `IMG` is chart-only; dashboards are single-view and `PDF`/`HTML` only. See [`exportType` Values](#exporttype-values). |
| **Timezone is inherited, not chosen** | The schedule runs in the workspace Account Admin's timezone. `scheduleDetails.hour` / `minute` are interpreted in that timezone, and `schedulePeriod` in the list response is rendered with it. |
| **Untrusted recipient domains are rejected** | If the organization restricts sharing to trusted domains, addresses outside them fail with `8031`. |
| **No `criteria` attribute** | Per-request row filtering is not supported; use `applyShareCriteria` (per-recipient share filters) or `reportBurstConfig` (per-row bursting). |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get View List](../../views-management/view-operations/get-views.md) → `viewIds`; [Get Group List](../../users-and-groups/workspace-groups/get-groups.md) → `groupIds` → Create Email Schedule → `scheduleId`. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — A view in `viewIds` does not exist. | Verify the IDs via [Get View List](../../views-management/view-operations/get-views.md). |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — Request came through a Client Portal / White Label domain, the user lacks Create Email Schedule permission, or lacks Export permission on a view in `viewIds`. | Call from the standard API host with the required permissions. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — A view in `viewIds` belongs to a different workspace. | Include only views from `<workspace-id>`. |
| [7832](../../../foundations/error-codes.md#error-7832) | 400 | `INVALID_EXPORT_TYPE` — `exportType` is not one of the supported formats. | Use `CSV`, `XLS`, `PDF`, `HTML`, or `IMG`. |
| [8000](../../../foundations/error-codes.md#error-8000) | 400 | `DUPLICATE_SCHEDULE` — A schedule with this `scheduleName` already exists in the workspace. | Choose a different name. |
| [8001](../../../foundations/error-codes.md#error-8001) | 400 | `MAILCOUNT_PER_SCHED_EXCEED` — Too many recipients for a single schedule. | Reduce the recipient list, or split it across schedules. |
| [8009](../../../foundations/error-codes.md#error-8009) | 400 | `MAIL_MULTIVIEW_MAXCOUNT_EXCEEEDED` — Too many views in one schedule. | Reduce `viewIds`, or split across schedules. |
| [8030](../../../foundations/error-codes.md#error-8030) | 400 | `EMAILEXPORT_DISABLED_IN_ORG` — Email export is disabled for this organization. | Ask the Organization Admin to enable export in Security Controls. |
| [8031](../../../foundations/error-codes.md#error-8031) | 400 | `UNTRUSTED_EMAILIDS` — A recipient address is outside the organization's trusted domains. | Use trusted-domain addresses, or ask the Organization Admin to add the domain. |
| [8032](../../../foundations/error-codes.md#error-8032) | 400 | `EMAILINGVIEW_DISABLED` — Emailing this view is disabled. | Check the view's and workspace's export settings. |
| [8033](../../../foundations/error-codes.md#error-8033) | 400 | `MAILSCH_SELECT_ATLEASTONE_EMAILID` — No recipient could be resolved from `emailIds`, `groupIds`, and `cc`. | Supply at least one address or a non-empty group. |
| [8034](../../../foundations/error-codes.md#error-8034) | 400 | `ONLY_ONE_DASHBOARD_IS_ALLOWED_PER_SCH` — More than one view scheduled where the first is a dashboard. | Schedule the dashboard on its own. |
| [8035](../../../foundations/error-codes.md#error-8035) | 400 | `EXPORT_FORMATS_ALLOWED_FOR_DASHBOARD` — Dashboard scheduled with a format other than `PDF`/`HTML`. | Use `PDF` or `HTML`. |
| [8036](../../../foundations/error-codes.md#error-8036) | 400 | `EXPORT_FORMATS_ALLOWED_FOR_CHART` — `IMG` requested for a view that is not a chart. | Use `IMG` only for chart views. |
| [8037](../../../foundations/error-codes.md#error-8037) | 400 | `ONLY_ONE_VIEW_IS_ALLOWED_FOR_XLS` — `XLS` requested with more than one view. | Send exactly one view, or choose another format. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE` — A `scheduleDetails` value is out of range (e.g. `hour` outside 0–23, `minute` not a multiple of 5, `weekDays` outside 1–7, `months` outside 1–12, `skipFrequency` beyond the limit for the chosen frequency). | The error message names the attribute and its permitted range; correct the value. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | `SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION` — A view carries a restricted DATA_WARNING system tag. | Review the warning, then resend with `"validateSystemTags": false`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |

# Related

- [Email Schedules overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Schedules & Alerts](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Email Schedules](get-email-schedules.md), [Update Email Schedule](update-email-schedule.md), [Delete Email Schedule](delete-email-schedule.md), [Change Email Schedule Status](change-email-schedule-status.md), [Trigger Email Schedule](trigger-email-schedule.md).
- [SDK examples](../../../sdk-examples/schedules-and-alerts/email-schedules/create-email-schedule.md).
