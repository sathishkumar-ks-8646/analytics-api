# Zoho Analytics V2 REST API — Data Alerts

This document covers the V2 **Data Alert** REST APIs of Zoho Analytics — the APIs that discover what a report can be alerted on, create and edit alerts, enable/pause and delete them, run one on demand, and read the audit trail of every evaluation.

## What is a "Data Alert" in Zoho Analytics?

A **data alert** is a named, scheduled rule attached to a single report. On every scheduled evaluation the server re-reads the report, tests the alert's rules against it, and — when the boolean combination of those rules is true — delivers a notification through every channel configured on the alert. Alerts exist only on **Chart (analysis view)**, **Pivot Table** and **Summary View** reports; any other view type is refused with `8245`.

| Part | CONFIG attribute(s) | Notes |
|------|--------------------|-------|
| **What is watched** | `rules`, `conditionExpression`, `summaryType`, `rowAxis`, `columnAxis` | Up to 10 rules over the report's columns, combined by a boolean expression. `summaryType` selects the data slice — raw rows, sub totals, or the grand total. |
| **When it is evaluated** | `scheduleDetails` | Frequency, interval, time of day, and the day/week/month selectors that apply to that frequency. The view it watches is fixed at creation and cannot be changed. |
| **Who hears about it** | `email`, `notification`, `slack`, `msteams`, `webhook` | At least one channel must resolve to a real recipient or endpoint (`32000001`). |
| **What else it triggers** | `workflows`, `actionsByFlow` | Zoho Flow mappings. Both are **rejected by Create Alert** (`32000049`) and can only be re-asserted through Update Alert. |
| **How it reads** | `alertName`, `notifyOnChange` | The name is unique within the view (`32000011`); `notifyOnChange` suppresses repeat notifications while the condition stays true. |

> **The single most important behaviour:** every column in a rule is addressed by `viewColumnIndex`, a **positional** index that is valid only for the report's current shape. See [The viewColumnIndex Contract](#the-viewcolumnindex-contract) before building any rule, and re-read [Get View Metadata For Alert](#3-get-view-metadata-for-alert) after the report is edited.

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`). The five read APIs use the **`metadata`** scope family; the five write APIs use the **`modeling`** scope family — see [Appendix B](#appendix-b--oauth-scope-summary).
> - All ten APIs are **workspace-scoped** (`/restapi/v2/workspaces/<workspace-id>/...`) and require the `ZANALYTICS-ORGID` header. A missing header is `8083`; a header that does not own the workspace is `7387`.
> - `ZohoAnalytics_Server_URI` depends on the data centre (`analyticsapi.zoho.com`, `.eu`, `.in`, `.com.au`, `.jp`, …).
> - These APIs are **not blocked** on a Client Portal / White Label domain — unlike the [Email Schedule APIs](EMAIL_SCHEDULES.md#white-label--client-portal-behaviour). Instead a domain-binding check runs; see [White Label / Client Portal Behaviour](#white-label--client-portal-behaviour).
> - Alerts can only be configured on `AnalysisView` (Chart), `Pivot` and `SummaryView` reports. Any other view type is refused with `8245` before permissions or payload are considered.
> - None of these APIs accepts a `criteria` attribute, and none of them reads or writes table rows — no API here uses the `data` scope family.
> - Every numeric identifier is carried as a JSON **string**, in both directions. Sending `"viewColumnIndex": 2` instead of `"viewColumnIndex": "2"` fails with `8080`.

---

## Index

| # | API Name | Method | URL |
|---|----------|--------|-----|
| 1 | [Get Alerts In Workspace](#1-get-alerts-in-workspace) | GET | `/restapi/v2/workspaces/<workspace-id>/alerts` |
| 2 | [Get Alerts In View](#2-get-alerts-in-view) | GET | `/restapi/v2/workspaces/<workspace-id>/views/<view-id>/alerts` |
| 3 | [Get View Metadata For Alert](#3-get-view-metadata-for-alert) | GET | `/restapi/v2/workspaces/<workspace-id>/views/<view-id>/alerts/metadata` |
| 4 | [Get Alert Configuration](#4-get-alert-configuration) | GET | `/restapi/v2/workspaces/<workspace-id>/alerts/<alert-id>` |
| 5 | [Create Alert](#5-create-alert) | POST | `/restapi/v2/workspaces/<workspace-id>/views/<view-id>/alerts` |
| 6 | [Update Alert](#6-update-alert) | PUT | `/restapi/v2/workspaces/<workspace-id>/alerts/<alert-id>` |
| 7 | [Delete Alerts](#7-delete-alerts) | DELETE | `/restapi/v2/workspaces/<workspace-id>/alerts` |
| 8 | [Change Alert Status](#8-change-alert-status) | PUT | `/restapi/v2/workspaces/<workspace-id>/alerts/status` |
| 9 | [Run Alert](#9-run-alert) | POST | `/restapi/v2/workspaces/<workspace-id>/alerts/<alert-id>/execute` |
| 10 | [Get Alert Events](#10-get-alert-events) | GET | `/restapi/v2/workspaces/<workspace-id>/alerts/<alert-id>/events` |

> **Note on method overloading:** `/workspaces/<workspace-id>/views/<view-id>/alerts` serves [Get Alerts In View](#2-get-alerts-in-view) on `GET` and [Create Alert](#5-create-alert) on `POST`. The same path with the wrong verb silently performs the other operation.
>
> **Note on scoping:** only [Get Alerts In View](#2-get-alerts-in-view), [Get View Metadata For Alert](#3-get-view-metadata-for-alert) and [Create Alert](#5-create-alert) carry a `<view-id>`. Every other API addresses the alert by `<alert-id>` alone, because an alert id is unique within the workspace. There is **no way to move an alert to a different view** — the view is fixed at creation.
>
> **Note on `DELETE` with a body:** [Delete Alerts](#7-delete-alerts) is a `DELETE` that carries a `CONFIG` form body, because it deletes a *list* of alerts. Some HTTP clients strip bodies from `DELETE` requests; verify yours does not.

---

## How the Ten APIs Fit Together

The ten APIs split into **discovery** (what can I alert on, and what alerts exist), **write** (create / change / remove) and **operations** (run it now, inspect what it did). Every write API consumes an id produced by a discovery API.

| Step | What it produces | What consumes it |
|------|------------------|------------------|
| [Get View List](../06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#6-get-view-list) | `<view-id>` of a Chart / Pivot / Summary report | [Get Alerts In View](#2-get-alerts-in-view), [Get View Metadata For Alert](#3-get-view-metadata-for-alert), [Create Alert](#5-create-alert) |
| [Get View Metadata For Alert](#3-get-view-metadata-for-alert) | `viewColumnIndex` values plus the operators, rule types, thresholds and anomalies each column permits | `rules[]`, `rowAxis` and `columnAxis` of [Create Alert](#5-create-alert) / [Update Alert](#6-update-alert) |
| [Create Alert](#5-create-alert) | `data.alertId` | every alert-id-addressed API below |
| [Get Alerts In Workspace](#1-get-alerts-in-workspace) / [Get Alerts In View](#2-get-alerts-in-view) | `alerts[].id` of existing alerts | every alert-id-addressed API below |
| [Get Alert Configuration](#4-get-alert-configuration) | the alert's complete CONFIG, including `workflows` and `actionsByFlow` ids | [Update Alert](#6-update-alert) — edit the returned JSON and post it back |
| [Run Alert](#9-run-alert) | one off-schedule evaluation | [Get Alert Events](#10-get-alert-events) records its outcome |

The read-modify-write loop is the intended editing pattern: [Get Alert Configuration](#4-get-alert-configuration) emits exactly the CONFIG shape [Update Alert](#6-update-alert) accepts, so the response can be edited and posted straight back.

---

## The viewColumnIndex Contract

**The Alert APIs never expose or accept an internal column id. Every column reference is a `viewColumnIndex` — a positional index over the report's current column layout.**

| Where it appears | Meaning |
|---|---|
| `rules[].viewColumnIndex` | The column the rule tests. **Forbidden on anomaly rules** (`32000046`) — the column is derived from `anomaly.name` instead. |
| `rules[].values[0]` when `type` is `column` | The *other* NUMBER column being compared against. |
| `rowAxis` / `columnAxis` | The pivot/summary axis the alert's sub totals are computed over. |
| `viewColumns[].viewColumnIndex` and `anomalies[].viewColumnIndex` (responses) | The values you are allowed to send. |

The rule the server applies is: **the index is resolved against the report's live column layout at the moment of the call.** Practical consequences:

1. **A stale index is not always an error.** If the report has been edited and the index still resolves, it resolves to a *different* column and the alert silently watches the wrong data. If it no longer resolves, the call fails with `32000041` (`RULE_VIEW_COLUMN_INDEX_OUT_OF_BOUNDS`) or `32000029` (`INVALID_AXIS_VIEW_COLUMN`) for an axis.
2. **Re-fetch [Get View Metadata For Alert](#3-get-view-metadata-for-alert) before every write.** Caching the metadata for the duration of one build-a-rule workflow is fine; caching it across report edits is not.
3. **Indexes are JSON strings.** `"viewColumnIndex": "2"`, not `"viewColumnIndex": 2`. The server reads them with a string accessor; a bare numeric literal fails with `8080` `INVALID_JSON_CONFIGURATION`.
4. **[Get Alert Configuration](#4-get-alert-configuration) drops orphaned references silently.** A `rowAxis`, `columnAxis` or `rules[].viewColumnIndex` whose column no longer exists is **omitted** from the response rather than returned as a dangling index — so a naive read-modify-write can quietly lose an axis that had become invalid.

---

## Limitations

These are the limits that apply with **default settings**.

| Limitation | Value | Enforced by |
|------------|-------|-------------|
| **Rules per alert** | **1–10.** Counted across the whole `rules` array, anomaly rules included. | `32000018` (too many), `32000006` (none) |
| **E-mail recipients per alert** | **25** entries in `email.emailIds`. The request template accepts up to 1,000, but the server refuses anything above 25. | `32000007` |
| **Group recipients per alert** | **1–1000** entries in `email.groupIds`. | Request template |
| **Values per rule** | **1–300** entries in `rules[].values`. | Request template |
| **Webhook `params` / `headers`** | **0–10** entries each. | Request template |
| **`alertIds` per request** | **0–1000** entries on [Delete Alerts](#7-delete-alerts) and [Change Alert Status](#8-change-alert-status). An empty array is accepted and is a no-op. | Request template |
| **Alert name length** | **100** characters, unique within the view. | `32000011` |
| **`conditionExpression` length** | **1,000** characters. | Request template |
| **Alert event page size** | **1–100** records. A larger `recordsPerPage` is **silently clamped** to 100. | — |
| **Alert event retention** | **45 days**, inclusive of today. Older events are purged, not filtered. | — |
| **Alert schedules per organisation** | Plan-dependent. An organisation whose plan allows **zero** alert schedules cannot run an alert at all. | `6079` |

> **The e-mail recipient limit is the one that surprises people.** The `alertEmailTemplate_v2API` request template declares `emailIds` as a 1–1000 array, so a 200-address payload passes schema validation and is then rejected by the business layer with `32000007`. Keep explicit recipient lists at or below 25 addresses and use `groupIds` or `notifyAdmins` for wider distribution.

---

## Permission Model

Two different checks apply, and which one you get depends on how the API addresses its target.

| Role | May do | Notes |
|------|--------|-------|
| Account Admin / Organization Admin / Workspace Admin (DB Owner) | Everything in this document, on every alert in the workspace. | The DB Owner check short-circuits every other test. |
| Custom role with **Manage Data Alerts** (`CREATEALERT`) **and** all-alerts access | Everything, on every alert in the workspace. | Equivalent to DB Owner for these APIs. |
| Custom role with **Manage Data Alerts** but **without** all-alerts access | Create alerts on any view they hold `CREATEALERT` on; list every alert of the workspace; but read, edit, run, pause or delete **only alerts they own**. | Acting on somebody else's alert fails with `7301`. |
| Any other user | Nothing. | `7301`. |

| Addressing style | APIs | Check performed |
|---|---|---|
| Workspace | [Get Alerts In Workspace](#1-get-alerts-in-workspace) | The alert permission **on the workspace**. The check is workspace-wide, so the returned list can include alerts on views the caller could not configure individually. |
| View | [Get Alerts In View](#2-get-alerts-in-view), [Get View Metadata For Alert](#3-get-view-metadata-for-alert), [Create Alert](#5-create-alert) | DB Owner of the view's workspace, **or** `CREATEALERT` on that view. The view must also belong to `<workspace-id>` (`7319` otherwise). |
| Alert id | [Get Alert Configuration](#4-get-alert-configuration), [Update Alert](#6-update-alert), [Delete Alerts](#7-delete-alerts), [Change Alert Status](#8-change-alert-status), [Run Alert](#9-run-alert), [Get Alert Events](#10-get-alert-events) | DB Owner, **or** a custom-role user with Manage Data Alerts who either has all-alerts access or owns that specific alert. Evaluated **per id** on the two list-taking APIs. |

Two consequences worth stating plainly:

- **`CREATEALERT` on the view gates creation; alert ownership gates everything afterwards.** Losing view permission does not retract control of an alert already created, and gaining it does not grant control of someone else's.
- **Every alert-id-addressed API also verifies that the alert belongs to the workspace in the URL.** A mismatched pair is `7319`, and a deleted or non-existent alert is `32000009` — so an id from another workspace is never actionable, even for an Account Admin.

---

## White Label / Client Portal Behaviour

Unlike the [Email Schedule APIs](EMAIL_SCHEDULES.md#white-label--client-portal-behaviour), which are disabled outright on custom domains, the Alert APIs run a **domain-binding check**.

| Scenario | Result |
|----------|--------|
| Request sent to the **standard** API host (`analyticsapi.zoho.*`) | **Allowed**, whether or not the workspace is white-labelled. |
| Request sent **through a custom domain**, and the target workspace is bound to that same domain | **Allowed.** |
| Request sent **through a custom domain**, and the target workspace is bound to a different domain or to none | **Rejected with `7301`** before any business logic runs. |

There is no `domainName` CONFIG attribute on any of these APIs. If in doubt, call the standard host.

---

## 1. Get Alerts In Workspace

Returns every alert defined anywhere in the workspace, with its name, the view it watches, its enabled state, audit stamps, and the outcome of its last run. This is the broadest discovery call for `<alert-id>`.

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/alerts` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the workspace. |
| **Permission Required** | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or a custom-role user whose role has the **Manage Data Alerts** permission on this workspace. The check is workspace-wide — see [Permission Model](#permission-model). |

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

### Sample Requests

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

### Sample Responses

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

### Response Fields

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
| `alerts[].enabled` | Boolean | `true` when the alert is live, `false` when it is paused. Native JSON boolean. Toggled by [Change Alert Status](#8-change-alert-status). |
| `alerts[].createdTime` | String | Creation time as an ISO-8601 offset timestamp (`2026-03-12T10:15:22+05:30`), rendered in the **caller's profile time zone** — not in the alert's `scheduleDetails.timeZone`. |
| `alerts[].createdByName` | String | Display name of the user who created the alert. |
| `alerts[].createdBy` | String | E-mail address of that user, resolved from the owner ZUID. **Empty string** when the lookup fails — enrichment failures never break this response. |
| `alerts[].lastModifiedTime` | String | Last modification time, same format as `createdTime`. |
| `alerts[].lastModifiedByName` | String | Display name of the user who last modified the alert. |
| `alerts[].lastModifiedBy` | String | E-mail address of that user, same fallback as `createdBy`. |
| `alerts[].lastAlertSentTime` | String | When a notification was last **sent**. Empty string when the alert has never notified anyone. |
| `alerts[].lastRunTime` | String | When the alert was last **evaluated**, whether or not it notified. Empty string when it has never run. |
| `alerts[].lastRunStatus` | String | Outcome of that last evaluation as a **localised label** — `"Condition met"` or `"Condition unmet"`. Empty string when the alert has never run. Do not switch on this value; use `status` from [Get Alert Events](#10-get-alert-events), which is a stable enum. |
| `alerts[].nextScheduleTime` | String | Next scheduled evaluation, same format as `createdTime`. Empty string when the alert is paused or has no active schedule. |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Permission is workspace-wide, not per view** | One alert-level permission on the workspace lists every alert in it, including alerts on views the caller could not configure. Acting on those alerts is a separate, stricter check — see [Permission Model](#permission-model). |
| **Timestamps use the caller's time zone** | Every ISO-8601 value is rendered in the caller's profile time zone, not in the alert's own `scheduleDetails.timeZone`. Two users see different wall-clock values for the same `nextScheduleTime`. |
| **Missing timestamps are `""`, never `null`** | A never-run alert reports `lastRunTime`, `lastAlertSentTime` and `lastRunStatus` as empty strings; a paused alert additionally reports an empty `nextScheduleTime`. No field in this response is ever JSON `null`. |
| **`lastRunStatus` is prose, not an enum** | It is translated per caller language. The machine-readable equivalent is `alertEvents[].status` from [Get Alert Events](#10-get-alert-events). |
| **Ids are strings** | Parse `id` and `viewId` as strings or 64-bit longs. A 32-bit integer type loses precision. |
| **No paging, no filtering, no sorting** | The whole alert list is returned in one response. There is no `pageNo`, no keyword search and no status filter. [Get Alert Events](#10-get-alert-events) is the only paginated API in this family. |
| **Empty result is a success** | A workspace with no alerts returns `200` with `"alerts": []`, not an error. |
| **Owner e-mail resolution is best-effort** | `createdBy` / `lastModifiedBy` are resolved through a remote identity lookup, cached once per distinct ZUID per request. A failed lookup yields `""` rather than failing the call. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get Workspace List](../03%20%C2%B7%20Workspace%20Management/WORKSPACE_OPERATIONS.md) → `<workspace-id>` → Get Alerts In Workspace → `alerts[].id`. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7103 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is neither a Workspace Admin nor a custom-role user with Manage Data Alerts, or the request arrived through a custom domain the workspace is not bound to. | Authenticate as an admin or a user with Manage Data Alerts, and call from the standard API host unless the workspace is bound to your custom domain. |
| 7387 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not belong to the organisation in `ZANALYTICS-ORGID`. | Send the organisation id that owns the workspace. |
| 8060 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use a domain you have purchased from Zoho Analytics, or the standard API host. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

---

## 2. Get Alerts In View

Returns the alerts configured on one report. The response entries are identical in shape to [Get Alerts In Workspace](#1-get-alerts-in-workspace), narrowed to a single `<view-id>`.

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/views/<view-id>/alerts` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the workspace. |
| **Permission Required** | The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the view's workspace, **or** hold the `CREATEALERT` (Manage Data Alerts) permission on that specific view. Stricter than [Get Alerts In Workspace](#1-get-alerts-in-workspace). |

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

### Sample Requests

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

### Sample Responses

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

### Response Fields

Identical in shape to the Response Fields of [Get Alerts In Workspace](#1-get-alerts-in-workspace) — refer there for every attribute. The differences are:

| Field | Type | Description |
|-------|------|--------------|
| `summary` | String | `"Get alerts in view"` for this API. |
| `data.alerts` | JSONArray | Restricted to the alerts of the requested `<view-id>`, so every entry carries the same `viewId` and `viewName`. **Always present**; `[]` when that view has no alerts. |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Stricter permission than the workspace listing** | This call is view-scoped: DB Owner or `CREATEALERT` on that view. A user who can list the whole workspace may still be refused here for a specific view. |
| **The view/workspace pair is validated** | A `<view-id>` that lives in another workspace fails with `7319` rather than returning an empty list. |
| **`viewName` is filled in by this API** | The underlying lookup does not return a view name for the view-scoped query; the API resolves it from the view's configuration so that entries match the workspace listing byte-for-byte. |
| **Empty does not mean "not alert-capable"** | An empty array is the normal answer for a supported view with no alerts. To find out whether a view can carry an alert at all, call [Get View Metadata For Alert](#3-get-view-metadata-for-alert), which fails with `8245` on unsupported view types. This API does **not** check the view type. |
| **No paging, filtering or sorting** | Same as [Get Alerts In Workspace](#1-get-alerts-in-workspace). |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get View List](../06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#6-get-view-list) → `<view-id>` → Get Alerts In View → `alerts[].id`. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7103 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| 7104 | `META_OBJECT_NOT_PRESENT` — View not found. | Verify `<view-id>` via [Get View List](../06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#6-get-view-list). |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is neither the DB Owner nor a holder of `CREATEALERT` on this view, or the request arrived through a custom domain the workspace is not bound to. | Authenticate as the DB Owner or a user with Manage Data Alerts on that view, from the standard API host. |
| 7319 | `OBJID_NOT_BELONGS_TO_DB` — The view does not belong to the workspace in the URL. | Make `<workspace-id>` and `<view-id>` consistent. |
| 7387 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not belong to the organisation in `ZANALYTICS-ORGID`. | Send the organisation id that owns the workspace. |
| 8060 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use a domain you have purchased from Zoho Analytics, or the standard API host. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

---

## 3. Get View Metadata For Alert

Returns everything needed to construct a rule for a report: its alertable columns with their `viewColumnIndex`, the operator and rule-type catalogues each column permits, the chart thresholds on each column, and the view-level anomaly definitions. **This is the only source of `viewColumnIndex`** — call it before every [Create Alert](#5-create-alert) or [Update Alert](#6-update-alert).

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/views/<view-id>/alerts/metadata` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the workspace. |
| **Permission Required** | The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the view's workspace, **or** hold the `CREATEALERT` (Manage Data Alerts) permission on that specific view. |

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

### Sample Requests

**Case 1 — Chart report with thresholds and an anomaly definition**

```http
GET /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts/metadata HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Tabular report: a view type that cannot carry an alert (rejected)**

```http
GET /restapi/v2/workspaces/137687000271334001/views/137687000006991705/alerts/metadata HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Sample Responses

**HTTP 200 OK — Chart with a dimension column, a measure column carrying two thresholds, and one anomaly**

```json
{
    "status": "success",
    "summary": "Get view metadata for alert",
    "data": {
        "viewType": "AnalysisView",
        "viewColumns": [
            {
                "viewColumnIndex": "1",
                "axis": "X",
                "axisType": "XAXIS",
                "axisDisplayName": "Region",
                "operation": "GROUP",
                "dataType": "PLAIN",
                "viewId": "137687000006991601",
                "formulaId": "",
                "thresholds": [],
                "allowedOperators": ["is", "isnot", "isn", "notisn"],
                "allowedRuleTypes": ["constant"]
            },
            {
                "viewColumnIndex": "2",
                "axis": "Y",
                "axisType": "YAXIS",
                "axisDisplayName": "Sales",
                "operation": "SUM",
                "dataType": "NUMBER",
                "viewId": "137687000006991601",
                "formulaId": "",
                "thresholds": ["T1", "T2"],
                "allowedOperators": ["is", "isnot", "gt", "lt", "gte", "lte", "btw", "notbtw", "isn", "notisn"],
                "allowedRuleTypes": ["constant", "column", "threshold"]
            },
            {
                "viewColumnIndex": "3",
                "axis": "Y",
                "axisType": "YAXIS",
                "axisDisplayName": "Profit",
                "operation": "SUM",
                "dataType": "NUMBER",
                "viewId": "137687000006991601",
                "formulaId": "",
                "thresholds": [],
                "allowedOperators": ["is", "isnot", "gt", "lt", "gte", "lte", "btw", "notbtw", "isn", "notisn"],
                "allowedRuleTypes": ["constant", "column"]
            }
        ],
        "anomalies": [
            {
                "viewColumnIndex": "2",
                "anomalyName": "Sales Spike"
            }
        ],
        "allowedAnomalyOperators": ["sinceLastAlert"]
    }
}
```

**HTTP 200 OK — Chart with no thresholds and no anomalies**

```json
{
    "status": "success",
    "summary": "Get view metadata for alert",
    "data": {
        "viewType": "AnalysisView",
        "viewColumns": [
            {
                "viewColumnIndex": "1",
                "axis": "X",
                "axisType": "XAXIS",
                "axisDisplayName": "Order Date",
                "operation": "ABSMONTH",
                "dataType": "DATE",
                "viewId": "137687000006991601",
                "formulaId": "",
                "thresholds": [],
                "allowedOperators": ["is", "isnot", "curMonth", "prevMonth", "prevNMonths", "lastNMonths", "nextMonth", "nextNMonths"],
                "allowedRuleTypes": ["constant"]
            }
        ],
        "anomalies": [],
        "allowedAnomalyOperators": []
    }
}
```

**HTTP 400 Bad Request — Failure paired with Case 2**

```json
{
    "status": "failure",
    "summary": "INVALID_VIEW_TYPE_FOR_OPERATION",
    "data": {
        "errorCode": 8245,
        "errorMessage": "Invalid view type. This operation can only be performed using the following view(s): Charts, Pivots, Summary Views"
    }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | `"Get view metadata for alert"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.viewType` | String | View type token — `AnalysisView`, `Pivot` or `SummaryView`. These are the internal type names, not the UI labels ("Chart View", "Pivot View", "Summary View"). Any other type is refused with `8245` before this response is built. |
| `data.viewColumns` | JSONArray | One entry per column of the view that can take part in an alert. **Always present.** |
| `viewColumns[].viewColumnIndex` | String | The positional index identifying this column in a write request (`rules[].viewColumnIndex`, `rowAxis`, `columnAxis`, and `values[0]` for `type: "column"`). **The only column identifier the Alert APIs accept** — see [The viewColumnIndex Contract](#the-viewcolumnindex-contract). |
| `viewColumns[].axis` | String | Axis the column occupies in the view — `X`, `Y`, and so on. |
| `viewColumns[].axisType` | String | Axis role — `XAXIS`, `YAXIS`, `COLOR`, `TOOLTIP`, … |
| `viewColumns[].axisDisplayName` | String | Display name of the column as the report shows it. Use this for a user-facing column picker. |
| `viewColumns[].operation` | String | Aggregation or date bucket applied to the column — `SUM`, `GROUP`, `YEAR`, `ABSQUARTER`, `ABSMONTH`, `ABSWEEK`, `DATE`, `TIMESTAMP`, `MEACATEGORY`, `GEO`, … It is what decides the date-bucket operators and, for the view's X axis, the contents of `allowedAnomalyOperators`. |
| `viewColumns[].dataType` | String | The column's **original** data type — `PLAIN`, `NUMBER`, `DATE`, `TIMESTAMP`, … Informative only: the operator catalogue is computed server-side from fields that are not all exposed here, so never derive operators from `dataType` yourself. |
| `viewColumns[].viewId` | String | Id of the view (or of the underlying table, for a base-layer column) the column belongs to. |
| `viewColumns[].formulaId` | String | Id of the backing formula when the column is a formula column; empty string otherwise. |
| `viewColumns[].geoRole` | Number | Geo role of the column. **Conditional** — present only for geo columns. Role `1` (geometry) narrows `allowedOperators` to `isn` / `notisn`. |
| `viewColumns[].thresholds` | JSONArray of String | Chart threshold **display names** configured on this column, sorted by their internal property order (`T1`, `T2`, …). `[]` when the column has none. A value from this array is what a `type: "threshold"` rule puts in `values[0]`. An empty array is also the reason `threshold` is absent from `allowedRuleTypes`. |
| `viewColumns[].allowedOperators` | JSONArray of String | Every `rules[].operator` token legal for this column, already narrowed by its data type, aggregation and geo role. **Treat it as the authoritative allow-list** — an operator outside it fails with `8119`. Token meanings: [Appendix E](#appendix-e--enum-and-value-reference). |
| `viewColumns[].allowedRuleTypes` | JSONArray of String | Which `rules[].type` values this column supports: `constant` always; `column` only when the view has **at least two** NUMBER columns and this column is one of them; `threshold` only when `thresholds` is non-empty. A type outside this list fails with `8119`. |
| `data.anomalies` | JSONArray | Anomaly definitions configured on the view. **Always present**; `[]` when the view has none, in which case anomaly alerts cannot be created on it. |
| `anomalies[].viewColumnIndex` | String | The column the anomaly is defined on. **Conditional** — omitted when the underlying column reference cannot be resolved to an index. |
| `anomalies[].anomalyName` | String | The name to send as `rules[].anomaly.name`. Must match exactly, otherwise `32000042`. |
| `data.allowedAnomalyOperators` | JSONArray of String | Operators legal for an anomaly rule on **this view** — a view-level property, not a per-column one. Derived from the X axis: a `YEAR` bucket yields the yearly tokens, `ABSMONTH` the monthly ones, `DATE` / `TIMESTAMP` the full day-level set. `["sinceLastAlert"]` when the view has anomalies but no date-bucketed X axis; `[]` when `anomalies` is empty. **Always present.** |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **The only source of `viewColumnIndex`** | The Alert APIs never accept or return internal column ids, so a rule cannot be built correctly without this call. Full rules in [The viewColumnIndex Contract](#the-viewcolumnindex-contract). |
| **View type is checked first** | A view that is not `AnalysisView`, `Pivot` or `SummaryView` fails with `8245` before any column metadata is gathered. This is the cheapest way to test whether a report can carry an alert at all. |
| **`allowedOperators` and `allowedRuleTypes` are per column** | They mirror exactly what the alert dialog enables in the product UI. Picking from them is what avoids `8119` on the subsequent write. |
| **`allowedAnomalyOperators` is per view** | It depends only on the X axis's date bucket, so it is emitted once at the top level rather than per column. |
| **`anomalies` is surfaced once** | The underlying payload repeats the anomaly list on every column entry; this API hoists it to the top level. Do not look for it inside `viewColumns[]`. |
| **`thresholds` carries display names, not property names** | You send `"T1"`, not the internal `chart.threshold1`. The translation happens server-side on write and is reversed on [Get Alert Configuration](#4-get-alert-configuration). |
| **It reads structure, not data** | No rows are scanned, so calling it before every write is cheap. |
| **No CONFIG, no paging** | Every alertable column of the view is returned in one response. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get View List](../06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#6-get-view-list) → `<view-id>` → Get View Metadata For Alert → `viewColumnIndex` / `thresholds` / `anomalyName` → [Create Alert](#5-create-alert). |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7103 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| 7104 | `META_OBJECT_NOT_PRESENT` — View not found. | Verify `<view-id>` via [Get View List](../06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#6-get-view-list). |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is neither the DB Owner nor a holder of `CREATEALERT` on this view, or the request arrived through a custom domain the workspace is not bound to. | Authenticate as the DB Owner or a user with Manage Data Alerts on that view, from the standard API host. |
| 7319 | `OBJID_NOT_BELONGS_TO_DB` — The view does not belong to the workspace in the URL. | Make `<workspace-id>` and `<view-id>` consistent. |
| 7387 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not belong to the organisation in `ZANALYTICS-ORGID`. | Send the organisation id that owns the workspace. |
| 8060 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use a domain you have purchased from Zoho Analytics, or the standard API host. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| 8245 | `INVALID_VIEW_TYPE_FOR_OPERATION` — The view is not a Chart, Pivot Table or Summary View. | Alerts are supported only on those three report types; pick a different view. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

---

## 4. Get Alert Configuration

Returns one alert's complete configuration **in exactly the CONFIG shape that [Create Alert](#5-create-alert) and [Update Alert](#6-update-alert) accept**, so the response can be edited and posted straight back. This is the intended starting point for any edit.

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/alerts/<alert-id>` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the workspace. |
| **Permission Required** | The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the workspace, **or** a custom-role user with the **Manage Data Alerts** permission who either has all-alerts access or **owns this alert**. The alert must belong to `<workspace-id>`. |

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

### Sample Requests

**Case 1 — A single-rule alert on a chart**

```http
GET /restapi/v2/workspaces/137687000271334001/alerts/137687000010815003 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — An anomaly alert**

```http
GET /restapi/v2/workspaces/137687000271334001/alerts/137687000010815007 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — Alert id that was deleted (rejected)**

```http
GET /restapi/v2/workspaces/137687000271334001/alerts/137687000010815099 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Sample Responses

**HTTP 200 OK — Daily e-mail alert with one constant rule and two mapped workflows**

```json
{
    "status": "success",
    "summary": "Get alert configuration",
    "data": {
        "alertName": "Sales Drop Alert",
        "summaryType": "data",
        "isAnomaly": false,
        "conditionExpression": "(1)",
        "notifyOnChange": false,
        "scheduleDetails": {
            "timeZone": "Asia/Kolkata",
            "calendarFrequency": "daily",
            "hour": 9,
            "minute": 0,
            "interval": 1,
            "skipWeekends": true
        },
        "email": {
            "notifyAdmins": true,
            "subject": "Sales dropped below threshold",
            "message": "Please review the attached report.",
            "includeReport": true,
            "attachFilteredDataset": false,
            "attachmentType": "attachment",
            "systemMailId": false,
            "emailIds": ["jane.doe@example.com"]
        },
        "workflows": [
            {
                "id": "137687000012564035",
                "name": "Notify sales channel",
                "enabled": true
            },
            {
                "id": "137687000012564054",
                "name": "Create follow-up task",
                "enabled": false
            }
        ],
        "rules": [
            {
                "operator": "lt",
                "viewColumnIndex": "2",
                "type": "constant",
                "values": ["1000"]
            }
        ]
    }
}
```

**HTTP 200 OK — Anomaly alert: note that `viewColumnIndex` is absent from the rule**

```json
{
    "status": "success",
    "summary": "Get alert configuration",
    "data": {
        "alertName": "Sales spike anomaly",
        "summaryType": "data",
        "isAnomaly": true,
        "conditionExpression": "(1)",
        "notifyOnChange": false,
        "scheduleDetails": {
            "timeZone": "Asia/Kolkata",
            "calendarFrequency": "daily",
            "hour": 7,
            "minute": 0,
            "interval": 1,
            "skipWeekends": false
        },
        "notification": {
            "notifyAdmins": true,
            "notifySharedUsers": false,
            "subject": "Sales spike detected",
            "message": "An anomaly was detected on Sales."
        },
        "rules": [
            {
                "operator": "sinceLastAlert",
                "anomaly": {
                    "name": "Sales Spike",
                    "value": "",
                    "comboType": "top",
                    "comboTypeValue": "5"
                }
            }
        ]
    }
}
```

**HTTP 400 Bad Request — Failure paired with Case 3**

```json
{
    "status": "failure",
    "summary": "ALERT_DELETED",
    "data": {
        "errorCode": 32000009,
        "errorMessage": "The alert which your are trying to access was deleted."
    }
}
```

### Response Fields

`data` is the alert's complete configuration in CONFIG shape. For the meaning and constraints of every attribute — including the nested channel objects, `scheduleDetails` and `rules[]` — see [CONFIG Parameters of Create Alert](#config-parameters). This table covers the envelope and states which keys are conditional.

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | `"Get alert configuration"` for this API. |
| `data` | JSONObject | The alert configuration. It does **not** repeat the alert id — you already supplied it in the URL. |
| `data.alertName` | String | Alert name. **Always present.** |
| `data.summaryType` | String | `data`, `subTotal` or `grandTotal`. **Always present.** An anomaly alert reports `data`. |
| `data.isAnomaly` | Boolean | `true` when the alert's rules are anomaly rules. **Always present.** Read-only — it is derived from `rules[]`, and a value sent on write is ignored. |
| `data.rowAxis` | String | `viewColumnIndex` of the row axis of a Pivot / Summary alert. **Conditional** — omitted when the alert has no row axis, **and also omitted when the stored column no longer exists in the view**. |
| `data.columnAxis` | String | `viewColumnIndex` of the column axis, same conditions as `rowAxis`. |
| `data.conditionExpression` | String | The boolean expression combining the rules, e.g. `"(1 AND 2)"`. **Always present**; `""` when the stored value is null. It is emitted verbatim from storage, so an alert created outside the V2 API can carry an expression that references more rules than exist — validate it against `rules.length` before posting back. |
| `data.notifyOnChange` | Boolean | `true` when the alert notifies only on a state change. **Always present.** |
| `data.scheduleDetails` | JSONObject | The schedule, normalised into write shape: array-valued `weekDays` / `monthDays` / `months`, an explicit 1-based `interval`, and `skipWeekends` present **only** for `hourly` and `daily`. **Always present**, but `{}` for an alert with no stored schedule. |
| `data.email` | JSONObject | E-mail channel. **Conditional** — present only when configured. Within it, `emailIds` and `groupIds` are themselves omitted when empty, and `attachmentType` is omitted when no report is attached. |
| `data.notification` | JSONObject | In-app (WMS) channel. **Conditional.** |
| `data.slack` | JSONObject | Slack channel — `url`, `messageType`, plus `subject` / `message` or `payload`. **Conditional.** |
| `data.msteams` | JSONObject | Microsoft Teams channel, same shape as `slack`. **Conditional.** |
| `data.webhook` | JSONObject | Webhook channel — `url`, `method`, `body`, `params`, `headers`. **Conditional.** `params` and `headers` are omitted when empty. |
| `data.workflows` | JSONArray | Zoho Flow workflows mapped to this alert. **Conditional** — omitted when none are mapped. |
| `workflows[].id` | String | Workflow id. This is the only field [Update Alert](#6-update-alert) reads back. |
| `workflows[].name` | String | Workflow name; `""` when the workflow has none. **Display only** — it is not validated on write. |
| `workflows[].enabled` | Boolean | `true` when the workflow is active. **Display only.** |
| `data.actionsByFlow` | JSONArray | Zoho Flow actions mapped to this alert. **Conditional** — omitted when none are mapped. |
| `actionsByFlow[].actionConfigId` | Number | Flow action configuration id. A genuine JSON **number**, unlike every other id in this family — and [Update Alert](#6-update-alert) requires it back as a **string**, so this one field does not round-trip unedited. |
| `actionsByFlow[].actionConfigName` | String | Flow action name. |
| `actionsByFlow[].connectionId` | Number | Id of the connection the action uses. Also a JSON number, with the same conversion caveat. |
| `data.rules` | JSONArray | The alert's rules in `rules[]` shape. **Always present.** Column references come back as `viewColumnIndex`, threshold references as display names (`"T1"`), and date values re-normalised to `yyyy-MM-dd HH:mm:ss`. Anomaly rules carry an `anomaly` object and **no** `viewColumnIndex`. |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **The response is a ready-to-post request body, with two exceptions** | It is emitted in exactly the CONFIG shape of [Create Alert](#5-create-alert) / [Update Alert](#6-update-alert) — including the normalised `scheduleDetails` and round-tripped date literals — which makes read-modify-write the intended editing pattern. The exceptions: `actionsByFlow[].actionConfigId` / `connectionId` come back as JSON numbers but must be re-sent as strings, and `conditionExpression` is not validated on the way out. |
| **Absent means absent, not null** | Unconfigured channels, `workflows`, `actionsByFlow`, `rowAxis` and `columnAxis` are **omitted** rather than returned as `null` or `{}`. Test for key presence, not truthiness. `conditionExpression` is the one attribute that uses `""`. |
| **Orphaned column references are dropped silently** | A `rowAxis`, `columnAxis` or `rules[].viewColumnIndex` whose column was deleted after the alert was created is omitted. A round-trip can therefore quietly lose an axis — compare against fresh [Get View Metadata For Alert](#3-get-view-metadata-for-alert) output before posting back. |
| **Anomaly rules deliberately omit `viewColumnIndex`** | The write contract forbids it on anomaly rules (`32000046`), so the read contract does not emit it. The column is recovered from `anomaly.name`. |
| **Legacy schedules are understood and upgraded** | Alerts created before the scheduler rework store the time of day as minutes-from-midnight (`570_daily`). That form is parsed correctly here, and re-saving the alert rewrites it in the current form. `32000034` is raised only when the stored value cannot be parsed at all. |
| **`conditionExpression` is not sanitised on read** | It is returned exactly as stored. A legacy alert can carry `"( 1 AND 2 )"` against a single rule; posting that back fails with `32000020`. Check it against `rules.length` yourself. |
| **Channel secrets are decrypted** | `slack.url`, `msteams.url`, `webhook.url`, webhook `params` / `headers` values and the custom `payload` are stored encrypted and returned in clear text to an authorised caller. Treat the response as sensitive. |
| **The alert id is not repeated in the body** | It is only in the URL you called. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get Alerts In Workspace](#1-get-alerts-in-workspace) → `alerts[].id` → Get Alert Configuration → edit → [Update Alert](#6-update-alert). |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7103 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is neither the DB Owner nor a custom-role user permitted to act on this alert, or the request arrived through a custom domain the workspace is not bound to. | Authenticate as the DB Owner, or as the alert's owner with Manage Data Alerts, from the standard API host. |
| 7319 | `OBJID_NOT_BELONGS_TO_DB` — The alert's view does not belong to the workspace in the URL. | Make `<workspace-id>` and `<alert-id>` consistent. |
| 7387 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not belong to the organisation in `ZANALYTICS-ORGID`. | Send the organisation id that owns the workspace. |
| 8060 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use a domain you have purchased from Zoho Analytics, or the standard API host. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |
| 32000009 | `ALERT_DELETED` — The alert has been deleted or never existed. | Re-discover the id with [Get Alerts In Workspace](#1-get-alerts-in-workspace). |
| 32000034 | `INVALID_LEGACY_SCHTIME` — The alert's persisted schedule string could not be parsed. | Re-save the alert through [Update Alert](#6-update-alert) with a valid `scheduleDetails`. |

---

## 5. Create Alert

Creates an alert on the specified report and returns its id. The view must be a Chart (`AnalysisView`), `Pivot` or `SummaryView`; the alert is created **live**, with its schedule registered immediately.

| Attribute | Value |
|-----------|-------|
| **Method** | POST |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/views/<view-id>/alerts` |
| **OAuth Scope** | `ZohoAnalytics.modeling.create` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the workspace. |
| **Permission Required** | The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the view's workspace, **or** hold the `CREATEALERT` (Manage Data Alerts) permission on that specific view. |

### CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Max Length | Description |
|-----------|------|-----------|---------|------------|-------------|
| `alertName` | String | **Yes** | — | 100 | Display name of the alert. Must be **unique within the view** (`32000011` otherwise) and non-blank (`32000005`). It can be changed later through [Update Alert](#6-update-alert). |
| `summaryType` | String (enum) | Conditional | `data` | 50 | Which slice of the report the rules are evaluated against. **Mandatory when the view is a Pivot Table** — omitting it there is `8079`. For Chart and Summary views it defaults to `data`. See [`summaryType` Values](#summarytype-values). |
| `rowAxis` | String | Conditional | — | — | `viewColumnIndex` of the row-axis column of a Pivot / Summary report. **Mandatory when `summaryType` is `subTotal`** on a Pivot or Summary view (`32000044` otherwise); meaningless and ignorable elsewhere. Must resolve to a column of this view (`32000041` / `32000029`). Send it as a **string**. |
| `columnAxis` | String | No | — | — | `viewColumnIndex` of the column-axis column of a Pivot / Summary report. Same validation as `rowAxis`, but never mandatory. |
| `conditionExpression` | String | Conditional | `(1)` | 1000 | Boolean expression combining the rules by their 1-based position in `rules[]`. Allowed tokens are rule numbers, `AND`, `OR`, `(` and `)` — e.g. `"(1 AND 2) OR 3"`. **Mandatory when `rules` has more than one entry** (`8079` otherwise); with a single rule it defaults to `(1)`. The grammar is validated strictly: unbalanced parentheses or a dangling operator is `32000024`, a reference outside `1..rules.length` is `32000020`, a blank value is `32000015`. |
| `notifyOnChange` | Boolean | No | `false` | — | When `true`, a notification is sent only when the alert's state **changes** (the condition turning true after having been false) rather than on every matching evaluation. |
| `isAnomaly` | Boolean | No | — | — | **Accepted but ignored.** The server derives it from whether `rules[]` carries `anomaly` objects and overwrites whatever you send. It is returned by [Get Alert Configuration](#4-get-alert-configuration) so that response can be posted back unchanged. |
| `scheduleDetails` | JSONObject | **Yes** | — | 5000 | How often the alert is evaluated. See [`scheduleDetails` Fields](#scheduledetails-fields). |
| `email` | JSONObject | No\* | — | 10000 | E-mail notification channel. See [`email` Fields](#email-fields). |
| `notification` | JSONObject | No\* | — | 10000 | In-product (WMS) notification channel. See [`notification` Fields](#notification-fields). |
| `slack` | JSONObject | No\* | — | 50000 | Slack incoming-webhook channel. See [`slack` and `msteams` Fields](#slack-and-msteams-fields). |
| `msteams` | JSONObject | No\* | — | 50000 | Microsoft Teams incoming-webhook channel. Identical shape to `slack`. |
| `webhook` | JSONObject | No\* | — | 100000 | Generic HTTPS webhook channel. See [`webhook` Fields](#webhook-fields). |
| `workflows` | JSONArray of JSONObject | No | — | 10000 | **Rejected by this API** with `32000049`. Zoho Flow workflow mappings can only be re-asserted through [Update Alert](#6-update-alert), because the mapping cannot exist before the alert does. |
| `actionsByFlow` | JSONArray of JSONObject | No | — | 100000 | **Rejected by this API** with `32000049`, for the same reason as `workflows`. |
| `rules` | JSONArray of JSONObject | **Yes** | — | 100000 | The evaluation rules. **1–10 entries** — more is `32000018`, none is `32000006`. See [`rules` Fields](#rules-fields). |
| `validateSystemTags` | Boolean | No | `true` | — | When `true` (the default) and the alert attaches the report to an e-mail, the view's **Data Warning** system tags are checked and creation is refused with `8241` if a restricted tag is present. Set it to `false` to create the alert anyway. It has no effect when no report is attached. |

\* **At least one notification channel is required.** `email`, `notification`, `slack`, `msteams` and `webhook` are each individually optional, but the request must produce at least one *stored* channel or it fails with `32000001` — and a channel object that resolves to no recipient (an `email` with `notifyAdmins: false` and empty `emailIds` / `groupIds`, or a `notification` with both flags `false`) is discarded with `32000013` rather than stored.

> **`cliq` is not accepted.** The Zoho Cliq channel exists in the product's legacy alert model but is deliberately not exposed by the V2 API; sending it has no effect.

#### `summaryType` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `data` | Evaluate the rules against the report's data rows. | The default for Chart and Summary views. |
| `subTotal` | Evaluate against sub-total rows. | Pivot / Summary views only. Requires `rowAxis` (`32000044`). |
| `grandTotal` | Evaluate against the single grand-total row. | Pivot / Summary views only. |

Any other value is `8119`.

#### `scheduleDetails` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `calendarFrequency` | String (enum) | **Yes** | — | `hourly`, `daily`, `weekly`, `monthly` or `yearly`. Case-insensitive on input, normalised to lower case. Any other value is `8119`. See [`calendarFrequency` Values](#calendarfrequency-values). |
| `interval` | Integer | **Yes** for `hourly` | `1` | "Repeat every N units of `calendarFrequency`". Permitted values depend on the frequency: `hourly` → `1`, `2`, `3`, `4`, `6` or `12`; `daily` → 1–7; `weekly` → 1–4; `monthly` → 1–12; `yearly` → 1–5. Out of range is `8119`. |
| `timeZone` | String | No | Caller's profile time zone, else `GMT` | IANA time zone id used to evaluate the schedule — `Asia/Kolkata`, `America/New_York`, `Europe/London`, `UTC`. An unrecognised id, or an explicit `null` / empty string, is `32000045`. |
| `hour` | Integer | **Yes** except for `hourly` | — | Hour of day, **0–23**. Out of range is `8119`. Not applicable to `hourly` (`32000052`). |
| `minute` | Integer | **Yes** except for `hourly` | — | Minute of hour. Must be a **multiple of 5 in the range 0–55**; `9` is `8119`. Not applicable to `hourly`. |
| `skipWeekends` | Boolean | No | `false` | Skip the evaluations that fall on weekend days. **You do not choose the days** — they are the weekend of the schedule time zone's locale (Sunday for `Asia/Kolkata`; Saturday and Sunday for `America/New_York` and `UTC`; Friday and Saturday for `Asia/Riyadh`). Applicable only to `hourly` and `daily` (`32000052` elsewhere). |
| `weekDays` | JSONArray of Integer | **Yes** for `weekly` | — | Days of the week, **1 = Sunday … 7 = Saturday**. More than one may be selected (`[2, 4]` = Monday and Wednesday); a single day is still a one-entry array (`[6]`). Duplicates are dropped. Applicable only to `weekly`. |
| `monthDays` | JSONArray of Integer | Conditional | — | Dates of the month, **1–31**, or the single-entry list `[99]` meaning "last day of the month" (`99` cannot be combined with other dates). For `monthly` several dates may be selected (`[1, 15]`); for `yearly` the array must carry **exactly one** entry, because a yearly schedule stores one date per selected month. One of `monthDays` or (`weekOfMonth` + `dayOfWeek`) is mandatory for `monthly` and `yearly` — see below. |
| `weekOfMonth` | Integer | Conditional | — | Which occurrence of `dayOfWeek` within the month: **1 = first … 4 = fourth, 5 = last**. Used together with `dayOfWeek`. Applicable only to `monthly` and `yearly`. |
| `dayOfWeek` | Integer | Conditional | — | Day of the week for the "Nth weekday" form, **1 = Sunday … 7 = Saturday**. `weekOfMonth: 2, dayOfWeek: 3` reads "the second Tuesday of the month". Used together with `weekOfMonth`. |
| `months` | JSONArray of Integer | **Yes** for `yearly` | — | Months in which the alert runs, **1 = January … 12 = December**. More than one may be selected (`[1, 7]`). Applicable only to `yearly`. |

**Which field applies to which `calendarFrequency`** — a field sent for a frequency it does not apply to is rejected with `32000052` (`SCHEDULE_ATTRIBUTE_NOT_APPLICABLE`) rather than silently ignored:

| Field | `hourly` | `daily` | `weekly` | `monthly` | `yearly` |
|---|---|---|---|---|---|
| `calendarFrequency` | ✔ | ✔ | ✔ | ✔ | ✔ |
| `interval` | ✔ | ✔ | ✔ | ✔ | ✔ |
| `timeZone` | ✔ | ✔ | ✔ | ✔ | ✔ |
| `hour` | — | ✔ | ✔ | ✔ | ✔ |
| `minute` | — | ✔ | ✔ | ✔ | ✔ |
| `skipWeekends` | ✔ | ✔ | — | — | — |
| `weekDays` | — | — | ✔ | — | — |
| `monthDays` | — | — | — | ✔ | ✔ |
| `weekOfMonth` | — | — | — | ✔ | ✔ |
| `dayOfWeek` | — | — | — | ✔ | ✔ |
| `months` | — | — | — | — | ✔ |

**Monthly and yearly take exactly one of two day forms.** Supplying both, or neither, is `32000051` (`INVALID_SCHEDULE_ATTRIBUTE_COMBINATION`):

| Form | Fields | Reads as |
|---|---|---|
| By date | `monthDays` | "on the 1st and the 15th", or "on the last day" (`[99]`) |
| By weekday | `weekOfMonth` **and** `dayOfWeek` | "on the second Tuesday", or "on the last Friday" (`weekOfMonth: 5`) |

**Complete shapes, one per frequency:**

| Frequency | `scheduleDetails` |
|---|---|
| Hourly | `{"calendarFrequency": "hourly", "interval": 6, "skipWeekends": true}` |
| Daily | `{"calendarFrequency": "daily", "interval": 3, "hour": 9, "minute": 30, "skipWeekends": true}` |
| Weekly | `{"calendarFrequency": "weekly", "interval": 2, "hour": 9, "minute": 30, "weekDays": [2, 4]}` |
| Monthly — by date | `{"calendarFrequency": "monthly", "hour": 9, "minute": 30, "monthDays": [1, 15]}` |
| Monthly — by weekday | `{"calendarFrequency": "monthly", "interval": 3, "hour": 9, "minute": 30, "weekOfMonth": 5, "dayOfWeek": 6}` |
| Yearly — by date | `{"calendarFrequency": "yearly", "hour": 9, "minute": 30, "months": [1, 7], "monthDays": [15]}` |
| Yearly — by weekday | `{"calendarFrequency": "yearly", "interval": 2, "hour": 6, "minute": 0, "months": [4], "weekOfMonth": 1, "dayOfWeek": 2}` |

#### `calendarFrequency` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `hourly` | Every N hours, around the clock. | Carries no `hour` / `minute`. `interval` is **mandatory** and limited to 1, 2, 3, 4, 6 or 12. |
| `daily` | Every N days at a fixed time. | `interval` 1–7. |
| `weekly` | Every N weeks on the selected `weekDays`. | `interval` 1–4. `weekDays` mandatory. |
| `monthly` | Every N months, on a date or an Nth weekday. | `interval` 1–12. Exactly one day form. |
| `yearly` | Every N years, in the selected `months`. | `interval` 1–5. `months` mandatory, exactly one day form, `monthDays` limited to a single entry. |

#### `email` Fields

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `subject` | String | **Yes** | — | 500 | E-mail subject line. A blank value is `32000012`. |
| `message` | String | **Yes** | — | 5000 | E-mail body. HTML is permitted and filtered through AntiSamy. When `systemMailId` is `true` a stricter filter that strips all HTML is applied instead. |
| `notifyAdmins` | Boolean | No | `false` | — | Include the workspace admins / DB Owner in the recipient list. |
| `emailIds` | JSONArray of String | No | `[]` | — | Explicit recipient addresses. **Maximum 25 entries** — the request template permits 1,000, but the server refuses more than 25 with `32000007`. Blank entries are skipped. |
| `groupIds` | JSONArray of String | No | `[]` | — | Workspace group ids whose members receive the e-mail, as numeric **strings**. 1–1000 entries. |
| `includeReport` | Boolean | No | `false` | — | Attach or inline the report itself. When `true`, `attachmentType` becomes mandatory (`8079`). |
| `attachmentType` | String (enum) | **Yes** when `includeReport` is `true` | — | — | `inline` or `attachment`. Any other value is `8119`. Ignored when `includeReport` is `false`. See [`attachmentType` Values](#attachmenttype-values). |
| `attachFilteredDataset` | Boolean | No | `false` | — | Also attach the dataset filtered to the rows that matched the alert criteria. Independent of `includeReport` — it may be set on its own. |
| `systemMailId` | Boolean | No | `false` | — | `true` sends from the Zoho Analytics system mail id; `false` sends from the alert creator's address. Organisation-level display-e-mail settings can override this. |

> **The channel must resolve to a recipient.** If `notifyAdmins` is `false` and both `emailIds` and `groupIds` are empty, the channel is not stored and the request fails with `32000013`.

#### `attachmentType` Values

| Value | Meaning |
|-------|---------|
| `inline` | The report is rendered inside the e-mail body. |
| `attachment` | The report is sent as a file attachment. |

#### `notification` Fields

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `notifyAdmins` | Boolean | **Yes** | — | — | Notify the workspace admins / DB Owner. |
| `notifySharedUsers` | Boolean | **Yes** | — | — | Notify every user the view is shared with. |
| `subject` | String | **Yes** | — | 500 | Notification title. A blank value is `32000012`. |
| `message` | String | **Yes** | — | 5000 | Notification body. HTML is filtered through AntiSamy. |

> **Both flags are mandatory and at least one must be `true`.** `{"notifyAdmins": false, "notifySharedUsers": false}` is not stored and fails with `32000013`.

#### `slack` and `msteams` Fields

Both channels take the same object.

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `url` | String | **Yes** | — | 5000 | Incoming-webhook URL of the channel. **Must start with `https://`** — anything else is `32000025`. |
| `messageType` | String (enum) | **Yes** | — | — | `STANDARD` or `CUSTOM`. Case-insensitive on input, normalised to upper case. See [`messageType` Values](#messagetype-values). |
| `subject` | String | **Yes** when `messageType` is `STANDARD` | — | 500 | Message subject. Blank or absent under `STANDARD` is `32000026`. Stored as `""` under `CUSTOM`. |
| `message` | String | No | `""` | 5000 | Message body, used only under `STANDARD`. |
| `payload` | String | **Yes** when `messageType` is `CUSTOM` | — | 50000 | The raw body POSTed to the webhook, supplied as a **JSON document serialised into a string**. It must parse as a JSON object or array, otherwise `32000027`. Ignored under `STANDARD`. |

#### `messageType` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `STANDARD` | Zoho Analytics composes the message from `subject` and `message`. | `subject` mandatory (`32000026`). `payload` is discarded. |
| `CUSTOM` | Your own `payload` is POSTed verbatim, letting you use Slack Block Kit or a Teams message card. | `payload` mandatory and must be valid JSON (`32000027`). `subject` and `message` are discarded. |

#### `webhook` Fields

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `url` | String | **Yes** | — | 5000 | Target URL. **Must start with `https://`** — anything else is `32000025`. |
| `method` | String (enum) | No | `POST` | 10 | HTTP method used to invoke the webhook. See [`method` Values](#method-values). |
| `body` | String | No | `""` | 50000 | Raw request body sent with the call. Not parsed or validated. |
| `params` | JSONArray of JSONObject | No | — | 50000 | Query / form parameters appended to the request, **0–10** entries. See [`params` and `headers` Fields](#params-and-headers-fields). |
| `headers` | JSONArray of JSONObject | No | — | 10000 | Additional HTTP headers sent with the request, **0–10** entries. Same entry shape as `params`. See [`params` and `headers` Fields](#params-and-headers-fields). |

#### `method` Values

| Value | Meaning |
|-------|---------|
| `GET` | Invoke the webhook with an HTTP `GET`. |
| `POST` | Invoke the webhook with an HTTP `POST`. The default. |
| `PUT` | Invoke the webhook with an HTTP `PUT`. |
| `PATCH` | Invoke the webhook with an HTTP `PATCH`. |
| `DELETE` | Invoke the webhook with an HTTP `DELETE`. |

#### `params` and `headers` Fields

Both arrays carry the same entry shape.

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `name` | String | **Yes** | — | 255 | Parameter or header name. Minimum 1 character. |
| `value` | String | **Yes** | — | 5000 | Parameter or header value. Stored encrypted and returned decrypted by [Get Alert Configuration](#4-get-alert-configuration). |

#### `rules` Fields

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `operator` | String | **Yes** | — | 50 | The comparison. It must appear in the column's `allowedOperators` from [Get View Metadata For Alert](#3-get-view-metadata-for-alert) — anything else is `8119`. Full catalogue in [Appendix E](#appendix-e--enum-and-value-reference). |
| `viewColumnIndex` | String | **Yes** for non-anomaly rules | — | — | The column the rule tests, as a `viewColumnIndex` **string**. **Must be omitted on anomaly rules** (`32000046`); the column is resolved from `anomaly.name` instead. An index that does not resolve is `32000041`. |
| `type` | String (enum) | No | `constant` | — | What the column is compared against: `constant`, `column` or `threshold`. It must appear in the column's `allowedRuleTypes` (`8119` otherwise). See [`type` Values](#type-values). |
| `values` | JSONArray of String | Conditional | — | 5000 | The comparison value(s), always **strings**, **1–300** entries. How many are required depends on the operator and the column — see the value-shape table below. Supplying values for a no-value operator is `32000047`. |
| `anomaly` | JSONObject | No | — | 10000 | Turns the rule into an **anomaly rule**. When any rule carries it, **every** rule must (`32000017`), and the alert must be on a Chart view (`32000019`). See [`anomaly` Fields](#anomaly-fields). |

**The shape of `values` is decided by the column as much as by the operator:**

| Case | `values` | Error if wrong |
|---|---|---|
| `type` is `column` | Exactly one entry: the `viewColumnIndex` of another **NUMBER** column of the same view. | `32000035` (missing), `32000036` (not numeric), `32000041` / `32000037` (not in this view) |
| `type` is `threshold` | Exactly one entry: the threshold **display name** from `viewColumns[].thresholds`, e.g. `"T1"`. | `32000035` (missing), `32000038` (unknown threshold) |
| `btw` / `notbtw` | Exactly two entries — lower bound, then upper bound. | `32000039` |
| `is` / `isnot` on a **categorical or date-bucket** column | One or more entries (multi-select). A comma inside a categorical token is escaped automatically. | `32000040` |
| `is` / `isnot` on a **NUMBER**, `DATE` or `TIMESTAMP` column | Exactly **one** entry — these are scalar comparators here, not multi-select. | `32000053` |
| `isn`, `notisn`, `sinceLastAlert` and the no-value date buckets (`curYear`, `prevMonth`, `today`, …) | **Omit `values` entirely.** | `32000047` if supplied |
| `prevN…` / `lastN…` / `nextN…` date buckets | Exactly one entry: the N, as a numeric string. | `32000040`, `32000053` |
| Every other scalar operator (`gt`, `lt`, `gte`, `lte`) | Exactly one entry. | `32000040` (none), `32000053` (more than one) |

**Date and timestamp columns:** when the rule column's operation is `DATE` or `TIMESTAMP` and the operator is one of `is`, `isnot`, `gt`, `lt`, `gte`, `lte`, `btw`, `notbtw`, every value must be `yyyy-MM-dd HH:mm:ss` or `yyyy-MM-dd` (the time then defaults to `00:00:00`). Any other shape is `32000028`. The server normalises these into its internal form on write and converts them back on [Get Alert Configuration](#4-get-alert-configuration), so the value round-trips.

#### `type` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `constant` | Compare the column against a literal value. | Always available. The default when `type` is absent or blank. |
| `column` | Compare the column against another NUMBER column of the same view. | Only when the view has **at least two** NUMBER columns. Chart views only (`32000019`). |
| `threshold` | Compare the column against a chart threshold (`T1`, `T2`, …). | Only when the column has at least one threshold. Chart views only (`32000019`). |

#### `anomaly` Fields

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `name` | String | **Yes** | — | 100 | Name of an anomaly definition configured on the view, taken verbatim from `anomalies[].anomalyName` of [Get View Metadata For Alert](#3-get-view-metadata-for-alert). An unknown name is `32000042`. This is also what resolves the rule's column, which is why `viewColumnIndex` must be absent. |
| `value` | String | No | `""` | 1000 | The operator's argument, when the chosen anomaly operator takes one (for example the N of `lastNMonths`). |
| `comboType` | String (enum) | No | `""` | 5 | How matched anomalies are aggregated: `top` or `all`. See [`comboType` Values](#combotype-values). |
| `comboTypeValue` | String | **Yes** when `comboType` is `top` | `""` | 10 | The number of top anomalies to consider, as a numeric string. Must parse to a **positive** integer, otherwise `32000021`. |

#### `comboType` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `top` | Consider only the N most significant anomalies. | `comboTypeValue` must be a positive integer (`32000021`). |
| `all` | Consider every detected anomaly. | `comboTypeValue` is ignored. |

### Sample Requests

**Case 1 — Minimal valid alert: one rule, one channel, daily schedule**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Sales Drop Alert",
    "scheduleDetails": {
        "calendarFrequency": "daily",
        "hour": 9,
        "minute": 0
    },
    "email": {
        "notifyAdmins": true,
        "subject": "Sales dropped below threshold",
        "message": "Please review the report."
    },
    "rules": [
        {
            "operator": "lt",
            "viewColumnIndex": "2",
            "type": "constant",
            "values": ["1000"]
        }
    ]
}
```

**Case 2 — Three rules combined by a custom `conditionExpression`, with an inline report attachment**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Sales / Profit / Discount Monitor",
    "summaryType": "data",
    "conditionExpression": "(1 AND 2) OR 3",
    "notifyOnChange": false,
    "scheduleDetails": {
        "calendarFrequency": "daily",
        "interval": 1,
        "hour": 9,
        "minute": 0,
        "timeZone": "Asia/Kolkata",
        "skipWeekends": true
    },
    "email": {
        "notifyAdmins": true,
        "emailIds": ["jane.doe@example.com", "manager@example.com"],
        "subject": "Sales / Profit / Discount alert",
        "message": "One of the configured rules has been breached. Please review.",
        "includeReport": true,
        "attachmentType": "inline",
        "attachFilteredDataset": true,
        "systemMailId": false
    },
    "rules": [
        {
            "operator": "lt",
            "viewColumnIndex": "2",
            "type": "constant",
            "values": ["1000"]
        },
        {
            "operator": "lt",
            "viewColumnIndex": "3",
            "type": "constant",
            "values": ["100"]
        },
        {
            "operator": "gt",
            "viewColumnIndex": "4",
            "type": "constant",
            "values": ["25"]
        }
    ]
}
```

**Case 3 — Threshold rule and column-vs-column rule, hourly schedule, in-app notification**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Sales above T1 or below Profit",
    "conditionExpression": "(1 OR 2)",
    "notifyOnChange": true,
    "scheduleDetails": {
        "calendarFrequency": "hourly",
        "interval": 3,
        "timeZone": "Asia/Kolkata",
        "skipWeekends": true
    },
    "notification": {
        "notifyAdmins": true,
        "notifySharedUsers": true,
        "subject": "Sales crossed T1",
        "message": "Sales has crossed threshold T1 on the Sales By Region chart."
    },
    "rules": [
        {
            "operator": "gt",
            "viewColumnIndex": "2",
            "type": "threshold",
            "values": ["T1"]
        },
        {
            "operator": "lt",
            "viewColumnIndex": "2",
            "type": "column",
            "values": ["3"]
        }
    ]
}
```

**Case 4 — Anomaly alert: no `viewColumnIndex`, every rule carries `anomaly`**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Sales spike anomaly",
    "notifyOnChange": false,
    "scheduleDetails": {
        "calendarFrequency": "daily",
        "hour": 7,
        "minute": 0
    },
    "notification": {
        "notifyAdmins": true,
        "notifySharedUsers": false,
        "subject": "Sales spike detected",
        "message": "An anomaly was detected on Sales."
    },
    "rules": [
        {
            "operator": "sinceLastAlert",
            "anomaly": {
                "name": "Sales Spike",
                "value": "",
                "comboType": "top",
                "comboTypeValue": "5"
            }
        }
    ]
}
```

**Case 5 — Pivot report, sub-total slice: `summaryType` and `rowAxis` are both required**

```http
POST /restapi/v2/workspaces/137687000271334001/views/466206000000105001/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Region sub-total monitor",
    "summaryType": "subTotal",
    "rowAxis": "1",
    "columnAxis": "5",
    "notifyOnChange": true,
    "scheduleDetails": {
        "calendarFrequency": "weekly",
        "interval": 2,
        "hour": 9,
        "minute": 0,
        "weekDays": [2, 4]
    },
    "email": {
        "notifyAdmins": true,
        "groupIds": ["137687000002108009"],
        "subject": "Regional sub-total alert",
        "message": "Regional sub total has crossed the configured limit.",
        "includeReport": true,
        "attachmentType": "attachment"
    },
    "rules": [
        {
            "operator": "btw",
            "viewColumnIndex": "2",
            "type": "constant",
            "values": ["10000", "50000"]
        }
    ]
}
```

**Case 6 — Multi-select dimensional rule, a date rule, and a no-value rule across three channels**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Recent East/West orders",
    "conditionExpression": "(1 AND 2) AND 3",
    "scheduleDetails": {
        "calendarFrequency": "monthly",
        "hour": 7,
        "minute": 15,
        "monthDays": [1, 15],
        "timeZone": "Europe/London"
    },
    "slack": {
        "url": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXX",
        "messageType": "STANDARD",
        "subject": "New East/West orders",
        "message": "Orders from the East and West regions were detected."
    },
    "msteams": {
        "url": "https://example.webhook.office.com/webhookb2/00000000-0000-0000-0000-000000000000",
        "messageType": "CUSTOM",
        "payload": "{\"text\":\"New East/West orders detected\"}"
    },
    "webhook": {
        "url": "https://example.com/zoho-analytics/alert-hook",
        "method": "POST",
        "body": "{\"event\":\"newOrders\",\"severity\":\"info\"}",
        "params": [
            {"name": "source", "value": "analytics"}
        ],
        "headers": [
            {"name": "X-Source", "value": "ZohoAnalytics"}
        ]
    },
    "rules": [
        {
            "operator": "is",
            "viewColumnIndex": "1",
            "type": "constant",
            "values": ["East", "West"]
        },
        {
            "operator": "gte",
            "viewColumnIndex": "6",
            "type": "constant",
            "values": ["2026-01-01 00:00:00"]
        },
        {
            "operator": "notisn",
            "viewColumnIndex": "7",
            "type": "constant"
        }
    ]
}
```

**Case 7 — Yearly "by weekday" schedule, every 2 years, delivered to a webhook**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Biennial audit trigger",
    "summaryType": "grandTotal",
    "scheduleDetails": {
        "calendarFrequency": "yearly",
        "interval": 2,
        "hour": 6,
        "minute": 0,
        "months": [4],
        "weekOfMonth": 1,
        "dayOfWeek": 2
    },
    "webhook": {
        "url": "https://example.com/zoho-analytics/audit-hook",
        "method": "POST",
        "body": "{\"event\":\"biennialAudit\"}"
    },
    "rules": [
        {
            "operator": "gte",
            "viewColumnIndex": "4",
            "type": "constant",
            "values": ["1000000"]
        }
    ]
}
```

**Case 8 — `workflows` supplied on create (rejected)**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Alert with workflow",
    "scheduleDetails": {
        "calendarFrequency": "daily",
        "hour": 9,
        "minute": 0
    },
    "email": {
        "notifyAdmins": true,
        "subject": "Alert",
        "message": "Body."
    },
    "workflows": [
        {"id": "137687000012564035"}
    ],
    "rules": [
        {
            "operator": "lt",
            "viewColumnIndex": "2",
            "type": "constant",
            "values": ["1000"]
        }
    ]
}
```

**Case 9 — `skipWeekends` on a weekly schedule (rejected)**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Weekly with weekend skip",
    "scheduleDetails": {
        "calendarFrequency": "weekly",
        "hour": 9,
        "minute": 0,
        "weekDays": [6],
        "skipWeekends": true
    },
    "email": {
        "notifyAdmins": true,
        "subject": "Alert",
        "message": "Body."
    },
    "rules": [
        {
            "operator": "lt",
            "viewColumnIndex": "2",
            "type": "constant",
            "values": ["1000"]
        }
    ]
}
```

### Sample Responses

**HTTP 200 OK — Alert created**

```json
{
    "status": "success",
    "summary": "Create alert",
    "data": {
        "alertId": "137687000010815003"
    }
}
```

**HTTP 400 Bad Request — Failure paired with Case 8**

```json
{
    "status": "failure",
    "summary": "WORKFLOWS_NOT_ALLOWED_IN_CREATE",
    "data": {
        "errorCode": 32000049,
        "errorMessage": "The attribute 'workflows' is not supported in Create Alert. This attribute is allowed only in Update Alert."
    }
}
```

**HTTP 400 Bad Request — Failure paired with Case 9**

```json
{
    "status": "failure",
    "summary": "SCHEDULE_ATTRIBUTE_NOT_APPLICABLE",
    "data": {
        "errorCode": 32000052,
        "errorMessage": "The attribute 'skipWeekends' is not applicable when calendarFrequency is 'weekly'."
    }
}
```

**HTTP 400 Bad Request — No channel resolved to a recipient**

```json
{
    "status": "failure",
    "summary": "NOCHANNELINPUT",
    "data": {
        "errorCode": 32000001,
        "errorMessage": "Please select any one action to send alert notification."
    }
}
```

**HTTP 409 Conflict — The view carries a restricted Data Warning tag and the alert attaches the report**

```json
{
    "status": "failure",
    "summary": "SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION",
    "data": {
        "errorCode": 8241,
        "errorMessage": "To skip system tag validation, add the validateSystemTags parameter as 'false'."
    }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | `"Create alert"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.alertId` | String | Id of the alert just created, numeric but serialised as a **string**. This is the `<alert-id>` for [Get Alert Configuration](#4-get-alert-configuration), [Update Alert](#6-update-alert), [Change Alert Status](#8-change-alert-status), [Run Alert](#9-run-alert), [Get Alert Events](#10-get-alert-events), and the `alertIds` array of [Delete Alerts](#7-delete-alerts). |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Nothing is echoed back** | The response carries the id only. To see how the server normalised what you sent — resolved column indexes, the canonical `scheduleDetails`, the defaulted `type` and `conditionExpression` — call [Get Alert Configuration](#4-get-alert-configuration) with the returned `alertId`. |
| **The alert is created live** | Its schedule is registered immediately and it starts enabled, so an evaluation can occur before you have read the configuration back. Create it paused by following up with [Change Alert Status](#8-change-alert-status) if that matters. |
| **Not idempotent** | A repeat of the same request fails on the unique-name check with `32000011`. There is no upsert mode. |
| **Every reference is validated against the live view** | Column indexes must resolve (`32000041`), threshold names must exist on that column (`32000038`), anomaly names must exist on the view (`32000042`), and a `type: "column"` rule must point at a NUMBER column of the same view (`32000036` / `32000037`). |
| **`type` defaults to `constant`** | An absent or blank `type` is treated as `constant`, which is also the only type always available. |
| **`isAnomaly` is derived, not accepted** | The server sets it from whether the rules carry `anomaly` objects. Anomaly rules are all-or-nothing (`32000017`), must not carry `viewColumnIndex` (`32000046`), and — like `threshold` rules — are valid only on Chart views (`32000019`). |
| **`workflows` and `actionsByFlow` are rejected here** | Both describe mappings that cannot exist before the alert does (`32000049`). Create the alert first, map the workflow in Zoho Flow, then re-assert it through [Update Alert](#6-update-alert). |
| **`conditionExpression` silently defaults to `(1)`** | With several rules and no expression the request fails with `8079` rather than defaulting — but with exactly one rule the default applies. Always send an explicit expression when `rules` has more than one entry. |
| **`skipWeekends` does not let you choose the days** | They come from the schedule time zone's locale. Two alerts with the same flag but different `timeZone` values skip different days. |
| **Quota is not checked here** | The organisation's alert-schedule plan limit is enforced at **run** time (`6079`), not at creation. An alert can be created on a plan that cannot run it. |
| **System-tag gate** | With `validateSystemTags` left at `true` and an e-mail attachment configured, a restricted Data Warning tag on the view blocks creation with `8241` (HTTP 409). |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get View List](../06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#6-get-view-list) → `<view-id>` → [Get View Metadata For Alert](#3-get-view-metadata-for-alert) → `viewColumnIndex` → Create Alert → `data.alertId`. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7103 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| 7104 | `META_OBJECT_NOT_PRESENT` — View not found. | Verify `<view-id>` via [Get View List](../06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#6-get-view-list). |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is neither the DB Owner nor a holder of `CREATEALERT` on this view, or the request arrived through a custom domain the workspace is not bound to. | Authenticate as the DB Owner or a user with Manage Data Alerts on that view, from the standard API host. |
| 7319 | `OBJID_NOT_BELONGS_TO_DB` — The view does not belong to the workspace in the URL. | Make `<workspace-id>` and `<view-id>` consistent. |
| 7387 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not belong to the organisation in `ZANALYTICS-ORGID`. | Send the organisation id that owns the workspace. |
| 8060 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use a domain you have purchased from Zoho Analytics, or the standard API host. |
| 8078 | `EMPTY_JSON_ATTRIBUTE_FOUND` — A mandatory CONFIG attribute was sent with an empty value. | Give the named attribute a non-empty value. |
| 8079 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — A mandatory attribute is missing: `alertName`, `scheduleDetails`, `rules`, `summaryType` on a Pivot view, `conditionExpression` with more than one rule, or `attachmentType` when `includeReport` is `true`. | Add the named attribute. |
| 8080 | `INVALID_JSON_CONFIGURATION` — An attribute that must be a JSON string was sent as another type, typically `viewColumnIndex`, `rowAxis`, `columnAxis` or a `values` entry sent as a bare number. | Quote numeric identifiers and rule values: `"viewColumnIndex": "2"`, `"values": ["1000"]`. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| 8119 | `INVALID_VALUE_FOR_ATTRIBUTE` — A value is outside its permitted set: an `operator` or `type` not in the column's `allowedOperators` / `allowedRuleTypes`, an unknown `summaryType` or `messageType`, an `attachmentType` other than `inline` / `attachment`, or a `scheduleDetails` number out of range (`hour`, `minute`, `interval`, `weekDays`, `monthDays`, `months`, `weekOfMonth`, `dayOfWeek`). | Take operators and rule types from [Get View Metadata For Alert](#3-get-view-metadata-for-alert) and keep schedule numbers within the ranges in [`scheduleDetails` Fields](#scheduledetails-fields). |
| 8241 | `SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION` — The view carries a restricted Data Warning system tag and the alert attaches the report to an e-mail. HTTP 409. | Resolve the data warning, or resend with `"validateSystemTags": false`. |
| 8245 | `INVALID_VIEW_TYPE_FOR_OPERATION` — The view is not a Chart, Pivot Table or Summary View. | Create the alert on a supported report type. |
| 8504 | `LESS_THAN_MIN_OCCURANCE` — The `CONFIG` parameter was not sent, or a templated attribute is below its minimum occurrence. | Send `CONFIG` as a URL-encoded form parameter containing a valid JSON object. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |
| 32000001 | `NOCHANNELINPUT` — No notification channel was stored. Either none was supplied, or every supplied channel was discarded for having no recipient. | Supply at least one of `email`, `notification`, `slack`, `msteams`, `webhook`, and make sure it resolves to a recipient or endpoint. |
| 32000002 | `INVALID_OPERATOR` — The operator passed the per-column allow-list but is not understood by the evaluation engine for that column's configuration. | Choose a different operator from the column's `allowedOperators`. |
| 32000003 | `INVALID_CRITERIA` — The rule's value is unusable for the column: empty for an operator that needs one, or non-numeric on a NUMBER column. | Supply a value of the right kind for the column's data type. |
| 32000004 | `INVALID_CRITERIA_RANGE` — A year-bucket rule value exceeds 5 digits. | Use a plausible year or N value. |
| 32000005 | `EMPTY_ALERT_NAME` — `alertName` is blank. | Provide a non-empty name of at most 100 characters. |
| 32000006 | `NO_RULES` — `rules` is an empty array. | Provide between 1 and 10 rules. |
| 32000007 | `EMAIL_COUNT_EXCEED` — `email.emailIds` has more than 25 entries. | Keep explicit recipients at 25 or fewer; use `groupIds` or `notifyAdmins` for wider distribution. |
| 32000011 | `DUPLICATE_ALERT_NAME` — Another alert on this view already uses `alertName`. | Choose a name unique within the view. |
| 32000012 | `ALERT_SUBJECT_EMPTY` — The `subject` of the e-mail or in-app channel is blank. | Provide a non-empty `subject` for every channel that requires one. |
| 32000013 | `ALERT_EMPTY_USER_FOR_CHANNEL` — A channel has no recipient: `email` with `notifyAdmins: false` and empty `emailIds` / `groupIds`, or `notification` with both flags `false`. | Enable `notifyAdmins`, or supply `emailIds` / `groupIds`, or set one of the notification flags. |
| 32000015 | `INVALID_CRITERIA_EXPRESSION` — `conditionExpression` is blank or whitespace. | Provide an expression over rule numbers, `AND`, `OR`, `(` and `)`. |
| 32000017 | `INVALID_RULE_CONFIGURATION_FOR_ANOMALY` — Some rules carry `anomaly` and others do not. | Make every rule an anomaly rule, or none of them. |
| 32000018 | `ALERT_RULE_COUNT_EXCEEDED` — More than 10 rules. | Reduce `rules` to 10 entries or fewer. |
| 32000019 | `INVALID_RULE_TYPE_FOR_VIEW` — An anomaly or `threshold` rule was used on a Pivot or Summary view. | Use those rule types only on Chart (`AnalysisView`) reports. |
| 32000020 | `INVALID_CRITERIA_RULE_REFERENCE` — `conditionExpression` references a rule number outside `1..rules.length`. | Renumber the expression against the actual `rules` array. |
| 32000021 | `INVALID_ANOMALY_COMBO_TYPE_VALUE` — `anomaly.comboTypeValue` is not a positive integer while `comboType` is `top`. | Send a positive integer as a string, e.g. `"5"`. |
| 32000024 | `INVALID_CONDITION_EXPRESSION_FORMAT` — `conditionExpression` does not parse: unbalanced parentheses, a dangling `AND` / `OR`, or an unexpected token. | Use forms such as `(1)`, `(1 AND 2)`, `( 1 AND ( 2 OR 3 ) )`. |
| 32000025 | `INVALID_HTTPS_URL` — `slack.url`, `msteams.url` or `webhook.url` does not start with `https://`. | Use an HTTPS endpoint. |
| 32000026 | `EMPTY_MESSAGE_SUBJECT` — `subject` is blank on a `STANDARD` Slack / Teams channel. | Provide a non-empty `subject`, or switch to `messageType: "CUSTOM"`. |
| 32000027 | `INVALID_CUSTOM_PAYLOAD_JSON` — `payload` on a `CUSTOM` channel does not parse as a JSON object or array. | Send a valid JSON document serialised into the `payload` string. |
| 32000028 | `INVALID_DATE_VALUE` — A date / timestamp rule value is not `yyyy-MM-dd HH:mm:ss` or `yyyy-MM-dd`. | Reformat the value; see [`rules` Fields](#rules-fields). |
| 32000029 | `INVALID_AXIS_VIEW_COLUMN` — `rowAxis` or `columnAxis` resolves to a column that is not part of this view. | Use a `viewColumnIndex` from [Get View Metadata For Alert](#3-get-view-metadata-for-alert). |
| 32000035 | `RULE_MISSING_VALUE_FOR_TYPE` — A `column` or `threshold` rule has no `values` entry. | Supply `values[0]` — a `viewColumnIndex` for `column`, a threshold display name for `threshold`. |
| 32000036 | `RULE_VALUE_NOT_NUMERIC_VIEW_COLUMN` — `values[0]` of a `column` rule is not a numeric index. | Send the other column's `viewColumnIndex` as a numeric string. |
| 32000037 | `RULE_VALUE_VIEW_COLUMN_NOT_IN_VIEW` — The column referenced by a `column` rule is not part of this view. | Reference a column from the same view's `viewColumns[]`. |
| 32000038 | `RULE_THRESHOLD_NOT_FOUND` — The threshold display name in `values[0]` does not exist on the view. | Use a value from the column's `thresholds[]` array, e.g. `"T1"`. |
| 32000039 | `RULE_OPERATOR_REQUIRES_TWO_VALUES` — `btw` / `notbtw` did not receive exactly two values. | Send `[lower, upper]`. |
| 32000040 | `RULE_OPERATOR_REQUIRES_VALUE` — The operator needs at least one value and none was supplied. | Add the value, or switch to a no-value operator. |
| 32000041 | `RULE_VIEW_COLUMN_INDEX_OUT_OF_BOUNDS` — A `viewColumnIndex` does not resolve. Applies to `rules[].viewColumnIndex`, `rowAxis`, `columnAxis` and `values[0]` of a `column` rule. | Re-read [Get View Metadata For Alert](#3-get-view-metadata-for-alert); the report's columns have changed. |
| 32000042 | `ANOMALY_NAME_NOT_FOUND` — `anomaly.name` matches no anomaly configured on this view. | Use a name from `anomalies[].anomalyName`. |
| 32000044 | `SUBTOTAL_ROW_AXIS_REQUIRED` — `summaryType: "subTotal"` without `rowAxis` on a Pivot / Summary view. | Supply `rowAxis`. |
| 32000045 | `INVALID_TIME_ZONE_ID` — `scheduleDetails.timeZone` is not a recognised IANA zone id, or was sent as `null` / an empty string. | Send a valid id such as `Asia/Kolkata`, or omit the field to inherit the caller's zone. |
| 32000046 | `RULE_VIEW_COLUMN_NOT_ALLOWED_FOR_ANOMALY` — An anomaly rule also carried `viewColumnIndex`. | Remove `viewColumnIndex`; the column comes from `anomaly.name`. |
| 32000047 | `RULE_OPERATOR_DISALLOWS_VALUE` — `values` was supplied for a no-value operator (`isn`, `notisn`, `sinceLastAlert`, `curYear`, `today`, …). | Omit `values` entirely for those operators. |
| 32000049 | `WORKFLOWS_NOT_ALLOWED_IN_CREATE` — `workflows` or `actionsByFlow` was sent to Create Alert. | Remove it; re-assert the mapping through [Update Alert](#6-update-alert) after the alert exists. |
| 32000051 | `INVALID_SCHEDULE_ATTRIBUTE_COMBINATION` — A monthly / yearly schedule supplied both the by-date and the by-weekday form, or neither. | Supply either `monthDays`, or `weekOfMonth` together with `dayOfWeek`. |
| 32000052 | `SCHEDULE_ATTRIBUTE_NOT_APPLICABLE` — A `scheduleDetails` field was sent for a frequency it does not apply to. | Remove the field, or change `calendarFrequency`. See the applicability table in [`scheduleDetails` Fields](#scheduledetails-fields). |
| 32000053 | `RULE_OPERATOR_REQUIRES_SINGLE_VALUE` — More than one value was supplied for a scalar comparison, typically `is` / `isnot` on a NUMBER, `DATE` or `TIMESTAMP` column. | Send exactly one entry in `values`. |

---

## 6. Update Alert

Replaces an existing alert's configuration. The CONFIG body is the **same shape as [Create Alert](#5-create-alert)** and is treated as a **full replacement** — not a patch. It is also the only API that accepts the Zoho Flow mapping attributes.

| Attribute | Value |
|-----------|-------|
| **Method** | PUT |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/alerts/<alert-id>` |
| **OAuth Scope** | `ZohoAnalytics.modeling.update` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the workspace. |
| **Permission Required** | The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the workspace, **or** a custom-role user with the **Manage Data Alerts** permission who either has all-alerts access or **owns this alert**. |

### CONFIG Parameters

CONFIG is **mandatory** for this API, and it must be complete — attributes you omit are **not** carried over from the stored alert.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `alertName` | String | **Yes** | — | As in [Create Alert](#config-parameters). Uniqueness is still enforced within the view, excluding this alert itself. |
| `summaryType` | String (enum) | Conditional | `data` | As in Create Alert. Still mandatory when the alert's view is a Pivot Table. See [`summaryType` Values](#summarytype-values). |
| `rowAxis` | String | Conditional | — | As in Create Alert. Mandatory when `summaryType` is `subTotal` on a Pivot / Summary view. |
| `columnAxis` | String | No | — | As in Create Alert. |
| `conditionExpression` | String | Conditional | `(1)` | As in Create Alert. Mandatory when `rules` has more than one entry. |
| `notifyOnChange` | Boolean | No | `false` | As in Create Alert. **Omitting it resets the alert to `false`.** |
| `isAnomaly` | Boolean | No | — | Accepted but ignored; derived from `rules`. |
| `scheduleDetails` | JSONObject | **Yes** | — | As in Create Alert, parsed as a complete period definition — never merged field-by-field with the stored one. See [`scheduleDetails` Fields](#scheduledetails-fields). |
| `email` | JSONObject | No\* | — | See [`email` Fields](#email-fields). **Omitting it removes the e-mail channel.** |
| `notification` | JSONObject | No\* | — | See [`notification` Fields](#notification-fields). Omitting it removes the in-app channel. |
| `slack` | JSONObject | No\* | — | See [`slack` and `msteams` Fields](#slack-and-msteams-fields). Omitting it removes the channel. |
| `msteams` | JSONObject | No\* | — | Same shape as `slack`. Omitting it removes the channel. |
| `webhook` | JSONObject | No\* | — | See [`webhook` Fields](#webhook-fields). Omitting it removes the channel. |
| `workflows` | JSONArray of JSONObject | No | — | **Accepted only here.** Re-asserts the Zoho Flow workflow mappings that already exist on this alert. Every `id` must already be mapped to **this** alert, otherwise `32000043` naming all offending ids at once. See [`workflows` Fields](#workflows-fields). |
| `actionsByFlow` | JSONArray of JSONObject | No | — | **Accepted only here.** Re-asserts the Zoho Flow action mappings that already exist on this alert. Every `actionConfigId` must already be mapped to this alert, otherwise `32000050`. See [`actionsByFlow` Fields](#actionsbyflow-fields). |
| `rules` | JSONArray of JSONObject | **Yes** | — | As in Create Alert, 1–10 entries. See [`rules` Fields](#rules-fields). |
| `validateSystemTags` | Boolean | No | `true` | As in Create Alert — the Data Warning gate applies to updates too. |

\* **At least one notification channel is required**, on exactly the same terms as [Create Alert](#5-create-alert): the request must produce at least one stored channel (`32000001`), and a channel with no recipient is discarded (`32000013`).

#### `workflows` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `id` | String | **Yes** | — | Workflow id, exactly as returned by `workflows[].id` of [Get Alert Configuration](#4-get-alert-configuration) for the **same** alert. Digits only, up to 20 characters. An id not already mapped to this alert fails with `32000043`. |

> **`name` and `enabled` are not part of the write contract.** The request template defines no key other than `id`, so those display fields are ignored if present and are **not** validated against the stored mapping. Posting back an unedited [Get Alert Configuration](#4-get-alert-configuration) response is therefore safe.

#### `actionsByFlow` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `actionConfigId` | String | **Yes** | — | Flow action configuration id. Must already be mapped to this alert (`32000050`). **Send it as a JSON string**, even though [Get Alert Configuration](#4-get-alert-configuration) returns it as a number — see the note below. |
| `actionConfigName` | String | No | — | Flow action name, up to 50 characters. Read when the mapping row has to be re-created. |
| `connectionId` | String | No | — | Id of the connection the action uses, also as a JSON **string**. Read when the mapping row has to be re-created. |

> **`actionsByFlow` does not round-trip verbatim.** [Get Alert Configuration](#4-get-alert-configuration) emits `actionConfigId` and `connectionId` as genuine JSON **numbers**, but the write path reads them with a string accessor. Posting the response back unchanged therefore fails with `8080`; convert both values to strings first. Every other id in this family is a string in both directions.

### Sample Requests

**Case 1 — Minimal update: new name, new schedule, same single rule**

```http
PUT /restapi/v2/workspaces/137687000271334001/alerts/137687000010815003 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Sales Drop Alert (weekly)",
    "scheduleDetails": {
        "calendarFrequency": "weekly",
        "hour": 9,
        "minute": 30,
        "weekDays": [6],
        "timeZone": "Asia/Kolkata"
    },
    "email": {
        "notifyAdmins": true,
        "emailIds": ["finance@example.com"],
        "subject": "Weekly sales monitor",
        "message": "Weekly alert summary."
    },
    "rules": [
        {
            "operator": "lt",
            "viewColumnIndex": "2",
            "type": "constant",
            "values": ["1000"]
        }
    ]
}
```

**Case 2 — Re-asserting a mapped workflow and a mapped Flow action**

```http
PUT /restapi/v2/workspaces/137687000271334001/alerts/137687000010815003 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Sales Drop Alert",
    "summaryType": "data",
    "conditionExpression": "(1 OR 2)",
    "notifyOnChange": true,
    "scheduleDetails": {
        "calendarFrequency": "hourly",
        "interval": 2,
        "timeZone": "Asia/Kolkata",
        "skipWeekends": true
    },
    "email": {
        "notifyAdmins": true,
        "emailIds": ["jane.doe@example.com"],
        "subject": "Sales dropped below threshold",
        "message": "Please review the report.",
        "includeReport": true,
        "attachmentType": "attachment"
    },
    "workflows": [
        {"id": "137687000012564035"},
        {"id": "137687000012564054"}
    ],
    "actionsByFlow": [
        {
            "actionConfigName": "Notify sales channel",
            "actionConfigId": "137687000012564035",
            "connectionId": "137687000012564041"
        }
    ],
    "rules": [
        {
            "operator": "lt",
            "viewColumnIndex": "2",
            "type": "constant",
            "values": ["1000"]
        },
        {
            "operator": "gt",
            "viewColumnIndex": "3",
            "type": "constant",
            "values": ["100"]
        }
    ]
}
```

**Case 3 — Monthly schedule moved to "the last Friday of every third month"**

```http
PUT /restapi/v2/workspaces/137687000271334001/alerts/137687000010815005 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Quarter-end margin check",
    "summaryType": "subTotal",
    "rowAxis": "1",
    "scheduleDetails": {
        "calendarFrequency": "monthly",
        "interval": 3,
        "hour": 20,
        "minute": 0,
        "weekOfMonth": 5,
        "dayOfWeek": 6,
        "timeZone": "Europe/London"
    },
    "msteams": {
        "url": "https://example.webhook.office.com/webhookb2/00000000-0000-0000-0000-000000000000",
        "messageType": "CUSTOM",
        "payload": "{\"text\":\"Quarter-end margin is below 18%\"}"
    },
    "rules": [
        {
            "operator": "lt",
            "viewColumnIndex": "2",
            "type": "constant",
            "values": ["18"]
        }
    ]
}
```

**Case 4 — Workflow id that is not mapped to this alert (rejected)**

```http
PUT /restapi/v2/workspaces/137687000271334001/alerts/137687000010815003 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Sales Drop Alert",
    "scheduleDetails": {
        "calendarFrequency": "daily",
        "hour": 9,
        "minute": 0
    },
    "email": {
        "notifyAdmins": true,
        "subject": "Sales dropped below threshold",
        "message": "Please review the report."
    },
    "workflows": [
        {"id": "99999"},
        {"id": "88888"}
    ],
    "rules": [
        {
            "operator": "lt",
            "viewColumnIndex": "2",
            "type": "constant",
            "values": ["1000"]
        }
    ]
}
```

### Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. The alert id is already in the URL, and the stored result is read back with [Get Alert Configuration](#4-get-alert-configuration).

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — Failure paired with Case 4**

```json
{
    "status": "failure",
    "summary": "SUBFLOW_ID_NOT_MAPPED_TO_ALERT",
    "data": {
        "errorCode": 32000043,
        "errorMessage": "Invalid workflow id(s) '99999,88888' for alertId '137687000010815003'. These workflows are not mapped to the alert."
    }
}
```

**HTTP 400 Bad Request — Flow action not mapped to this alert**

```json
{
    "status": "failure",
    "summary": "FLOW_ACTION_NOT_MAPPED_TO_ALERT",
    "data": {
        "errorCode": 32000050,
        "errorMessage": "Invalid Flow action id(s) '77777' for alertId '137687000010815003'. These actions are not mapped to the alert."
    }
}
```

**HTTP 400 Bad Request — The alert was deleted between read and write**

```json
{
    "status": "failure",
    "summary": "ALERT_DELETED",
    "data": {
        "errorCode": 32000009,
        "errorMessage": "The alert which your are trying to access was deleted."
    }
}
```

### Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`).

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Full replace, not a patch** | The CONFIG you send *becomes* the alert. An omitted channel is removed, an omitted `notifyOnChange` resets to `false`, and the whole `rules` array replaces the stored one. Start from [Get Alert Configuration](#4-get-alert-configuration) output rather than composing a partial payload. |
| **The alert id never changes** | Unlike [Update Email Schedule](EMAIL_SCHEDULES.md#3-update-email-schedule), which can mint a new id when the name or period changes, an alert keeps its id across every update. Stored references stay valid. |
| **The view cannot be changed** | The report an alert watches is fixed at creation. The URL carries no `<view-id>`, and there is no CONFIG attribute for it — move an alert by deleting it and creating a new one, which resets its event history. |
| **Everything Create Alert validates is validated again** | Both share one conversion path, so the whole [Create Alert error table](#error-codes-4) applies here as well, on top of the alert-specific codes below. |
| **Idempotent** | Re-sending the same complete CONFIG leaves the alert in the same state and keeps the same id. The unique-name check ignores the alert being updated, so resending its own `alertName` is not `32000011`. |
| **List fields replace, never merge** | `rules`, `emailIds`, `groupIds`, `weekDays`, `monthDays`, `months`, webhook `params` / `headers`, `workflows` and `actionsByFlow` are all wholesale replacements. |
| **`workflows` validates ids only** | Each `workflows[].id` must already be mapped to this alert. `name` and `enabled` are ignored, so an unedited [Get Alert Configuration](#4-get-alert-configuration) response posts back cleanly. All invalid ids are reported in a single `32000043`. |
| **These attributes re-assert, they do not create** | Neither `workflows` nor `actionsByFlow` can introduce a new mapping — mappings are created in Zoho Flow. Omitting them drops the mapping from the alert. |
| **Legacy schedules are rewritten on save** | An alert whose stored schedule used the old minutes-from-midnight form is rewritten in the current form by any successful update. |
| **Permission is ownership-based** | A custom-role user without all-alerts access can update only their own alerts, even on a view they may create alerts on. |
| **Success is `204` with an empty body** | The only way to confirm what was stored is to read it back with [Get Alert Configuration](#4-get-alert-configuration). |
| **Dependency chain** | [Get Alert Configuration](#4-get-alert-configuration) → edit the returned JSON → Update Alert → [Get Alert Configuration](#4-get-alert-configuration) to verify. |

### Error Codes

In addition to the codes below, Update Alert can return **every code listed for [Create Alert](#5-create-alert)**, because the CONFIG payload is validated by the same conversion path.

| Code | Reason | Solution |
|------|--------|----------|
| 7103 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is neither the DB Owner nor a custom-role user permitted to act on this alert, or the request arrived through a custom domain the workspace is not bound to. | Authenticate as the DB Owner, or as the alert's owner with Manage Data Alerts, from the standard API host. |
| 7319 | `OBJID_NOT_BELONGS_TO_DB` — The alert's view does not belong to the workspace in the URL. | Make `<workspace-id>` and `<alert-id>` consistent. |
| 7387 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not belong to the organisation in `ZANALYTICS-ORGID`. | Send the organisation id that owns the workspace. |
| 8060 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use a domain you have purchased from Zoho Analytics, or the standard API host. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| 8245 | `INVALID_VIEW_TYPE_FOR_OPERATION` — The alert's view is no longer a Chart, Pivot Table or Summary View. | The report has been converted to an unsupported type; recreate the alert elsewhere. |
| 8504 | `LESS_THAN_MIN_OCCURANCE` — The `CONFIG` parameter was not sent. | Send `CONFIG` as a URL-encoded form parameter containing a valid JSON object. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.update`. |
| 32000009 | `ALERT_DELETED` — The alert has been deleted or never existed. | Re-discover the id with [Get Alerts In Workspace](#1-get-alerts-in-workspace). |
| 32000043 | `SUBFLOW_ID_NOT_MAPPED_TO_ALERT` — One or more `workflows[].id` values are not mapped to this alert. All offending ids are listed in one message. | Use only the ids returned by [Get Alert Configuration](#4-get-alert-configuration) for this same alert. |
| 32000050 | `FLOW_ACTION_NOT_MAPPED_TO_ALERT` — One or more `actionsByFlow[].actionConfigId` values are not mapped to this alert. | Use only the ids returned by [Get Alert Configuration](#4-get-alert-configuration) for this same alert. |

---

## 7. Delete Alerts

Deletes one or more alerts in a workspace. Every id is validated before anything is removed, so the call is all-or-nothing.

| Attribute | Value |
|-----------|-------|
| **Method** | DELETE |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/alerts` |
| **OAuth Scope** | `ZohoAnalytics.modeling.delete` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the workspace. |
| **Permission Required** | The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the workspace, **or** a custom-role user with the **Manage Data Alerts** permission who either has all-alerts access or **owns every alert listed**. The check runs per id. |

### CONFIG Parameters

CONFIG is **mandatory** for this API, and it is sent as a form body on a `DELETE` request.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `alertIds` | JSONArray of String | **Yes** | — | Alert ids to delete, as numeric **strings** — a bare numeric literal fails. **0–1000 entries**; an empty array is accepted and deletes nothing. Every id must belong to `<workspace-id>` (`7319`) and must still exist (`32000009`), and the caller must be permitted to act on each one (`7301`). |

### Sample Requests

**Case 1 — Delete two alerts**

```http
DELETE /restapi/v2/workspaces/137687000271334001/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertIds": [
        "137687000010815003",
        "137687000010815005"
    ]
}
```

**Case 2 — One id in the list has already been deleted (rejected, nothing is removed)**

```http
DELETE /restapi/v2/workspaces/137687000271334001/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertIds": [
        "137687000010815003",
        "137687000010815099"
    ]
}
```

### Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. No per-id result list is returned.

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — Failure paired with Case 2**

```json
{
    "status": "failure",
    "summary": "ALERT_DELETED",
    "data": {
        "errorCode": 32000009,
        "errorMessage": "The alert which your are trying to access was deleted."
    }
}
```

**HTTP 400 Bad Request — `alertIds` omitted**

```json
{
    "status": "failure",
    "summary": "ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION",
    "data": {
        "errorCode": 8079,
        "errorMessage": "Attribute 'alertIds' not present in the JSON configuration. Kindly provide a valid JSON configuration."
    }
}
```

### Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`).

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **All-or-nothing per request** | Every id is checked for workspace membership and caller permission **before** any deletion happens, so one bad id fails the whole request and nothing is removed. |
| **Ids must be JSON strings** | `["137687000010815003"]`, not `[137687000010815003]`. A numeric literal fails when the server reads the entry as a string. |
| **An empty array is a no-op** | `{"alertIds": []}` returns `204` and deletes nothing. Omitting the key entirely is `8079`. |
| **Nothing is reported per id** | "Deleted" and "was already absent" are indistinguishable from the response. Confirm with [Get Alerts In Workspace](#1-get-alerts-in-workspace) if it matters. |
| **It is a status change, not a purge** | The alert stops evaluating, disappears from the listing APIs and its id stops being actionable (`32000009`). There is no trash and no restore. |
| **Not the way to silence an alert temporarily** | Use [Change Alert Status](#8-change-alert-status), which is reversible and preserves the id and the event history. |
| **Not idempotent** | A second delete of the same ids fails with `32000009`. |
| **Success is `204` with an empty body** | Treat the status code as the success indicator; never expect a JSON body. |
| **Dependency chain** | [Get Alerts In Workspace](#1-get-alerts-in-workspace) → `alerts[].id` → Delete Alerts. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7103 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller may not act on at least one of the listed alerts, or the request arrived through a custom domain the workspace is not bound to. | Authenticate as the DB Owner, or list only alerts you own, from the standard API host. |
| 7319 | `OBJID_NOT_BELONGS_TO_DB` — At least one alert's view does not belong to the workspace in the URL. | Delete alerts from the workspace that owns them. |
| 7387 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not belong to the organisation in `ZANALYTICS-ORGID`. | Send the organisation id that owns the workspace. |
| 8060 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use a domain you have purchased from Zoho Analytics, or the standard API host. |
| 8078 | `EMPTY_JSON_ATTRIBUTE_FOUND` — `alertIds` was sent with an empty value. | Send an array of id strings, or omit the call. |
| 8079 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — `alertIds` is missing from CONFIG. | Add `alertIds`. |
| 8080 | `INVALID_JSON_CONFIGURATION` — An `alertIds` entry is not a JSON string. | Quote every id: `["137687000010815003"]`. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| 8504 | `LESS_THAN_MIN_OCCURANCE` — The `CONFIG` parameter was not sent. | Send `CONFIG` as a URL-encoded form body on the `DELETE` request. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.delete`. |
| 32000009 | `ALERT_DELETED` — At least one listed alert has already been deleted or never existed. | Re-check every entry against [Get Alerts In Workspace](#1-get-alerts-in-workspace). |

---

## 8. Change Alert Status

Enables (resumes) or pauses one or more alerts without altering their configuration. One request sets **one** state for every id it lists.

| Attribute | Value |
|-----------|-------|
| **Method** | PUT |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/alerts/status` |
| **OAuth Scope** | `ZohoAnalytics.modeling.update` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the workspace. |
| **Permission Required** | The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the workspace, **or** a custom-role user with the **Manage Data Alerts** permission who either has all-alerts access or **owns every alert listed**. The check runs per id. |

### CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `alertIds` | JSONArray of String | **Yes** | — | Alert ids whose status changes, as numeric **strings**. **0–1000 entries**; an empty array is accepted and changes nothing. Every id must belong to `<workspace-id>` and must still exist. |
| `enabled` | Boolean | **Yes** | — | The state applied to **every** id in `alertIds`: `true` makes the alert live, `false` pauses it. There is no per-id state — to enable some and pause others, send two requests. |

### Sample Requests

**Case 1 — Pause two alerts**

```http
PUT /restapi/v2/workspaces/137687000271334001/alerts/status HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertIds": [
        "137687000010815003",
        "137687000010815005"
    ],
    "enabled": false
}
```

**Case 2 — Resume a single alert**

```http
PUT /restapi/v2/workspaces/137687000271334001/alerts/status HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertIds": ["137687000010815003"],
    "enabled": true
}
```

**Case 3 — `enabled` omitted (rejected)**

```http
PUT /restapi/v2/workspaces/137687000271334001/alerts/status HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertIds": ["137687000010815003"]
}
```

### Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. The new state is not echoed back.

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — Failure paired with Case 3**

```json
{
    "status": "failure",
    "summary": "ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION",
    "data": {
        "errorCode": 8079,
        "errorMessage": "Attribute 'enabled' not present in the JSON configuration. Kindly provide a valid JSON configuration."
    }
}
```

**HTTP 400 Bad Request — One of the listed alerts no longer exists**

```json
{
    "status": "failure",
    "summary": "ALERT_DELETED",
    "data": {
        "errorCode": 32000009,
        "errorMessage": "The alert which your are trying to access was deleted."
    }
}
```

### Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`).

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **One state for the whole list** | `enabled` applies to every id in `alertIds`. There is no per-id payload. |
| **Idempotent** | Setting an alert to the state it is already in is not an error and still answers `204`. |
| **Same up-front validation as Delete Alerts** | Every id is checked for workspace membership and caller permission before any status changes, so one bad id fails the whole request. |
| **Pausing stops the schedule, not the history** | `nextScheduleTime` becomes `""` in the listing APIs, while `lastRunTime`, `lastAlertSentTime` and everything in [Get Alert Events](#10-get-alert-events) is retained. |
| **A paused alert can still be run on demand** | [Run Alert](#9-run-alert) works on a paused alert — pausing suppresses the *schedule*, not manual evaluation. |
| **Reversible, unlike Delete** | This is the correct way to silence an alert temporarily; [Delete Alerts](#7-delete-alerts) is not reversible. |
| **Scope follows the HTTP method, not the effect** | It needs `modeling.update` even though it neither creates nor removes anything. |
| **Success is `204` with an empty body** | Read the resulting state from `alerts[].enabled` in [Get Alerts In Workspace](#1-get-alerts-in-workspace). |
| **Dependency chain** | [Get Alerts In Workspace](#1-get-alerts-in-workspace) (read `enabled`) → Change Alert Status → verify. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7103 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller may not act on at least one of the listed alerts, or the request arrived through a custom domain the workspace is not bound to. | Authenticate as the DB Owner, or list only alerts you own, from the standard API host. |
| 7319 | `OBJID_NOT_BELONGS_TO_DB` — At least one alert's view does not belong to the workspace in the URL. | Change status from the workspace that owns the alerts. |
| 7387 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not belong to the organisation in `ZANALYTICS-ORGID`. | Send the organisation id that owns the workspace. |
| 8060 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use a domain you have purchased from Zoho Analytics, or the standard API host. |
| 8078 | `EMPTY_JSON_ATTRIBUTE_FOUND` — `alertIds` or `enabled` was sent with an empty value. | Provide a non-empty value for both attributes. |
| 8079 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — `alertIds` or `enabled` is missing from CONFIG. | Add the missing attribute. |
| 8080 | `INVALID_JSON_CONFIGURATION` — `enabled` is not a boolean, or an `alertIds` entry is not a JSON string. | Send `"enabled": true` / `false` and quote every id. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| 8504 | `LESS_THAN_MIN_OCCURANCE` — The `CONFIG` parameter was not sent. | Send `CONFIG` as a URL-encoded form parameter containing a valid JSON object. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.update`. |
| 32000009 | `ALERT_DELETED` — At least one listed alert has been deleted or never existed. | Re-check every entry against [Get Alerts In Workspace](#1-get-alerts-in-workspace). |

---

## 9. Run Alert

Queues an off-schedule evaluation of one alert. The alert is evaluated against live data and, if its condition is met, **every configured channel delivers for real**. There is no dry-run mode.

| Attribute | Value |
|-----------|-------|
| **Method** | POST |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/alerts/<alert-id>/execute` |
| **OAuth Scope** | `ZohoAnalytics.modeling.create` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the workspace. |
| **Permission Required** | The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the workspace, **or** a custom-role user with the **Manage Data Alerts** permission who either has all-alerts access or **owns this alert**. |

### CONFIG Parameters

CONFIG is **optional** for this API. The only attribute it can carry is `validateSystemTags`.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `validateSystemTags` | Boolean | No | `true` | When `true` (the default) **and** the alert has an e-mail attachment configured, the view's **Data Warning** system tags are checked and the run is refused with `8241` (HTTP 409) if a restricted tag is present. Set it to `false` to run anyway. It has no effect on an alert with no e-mail attachment. |

### Sample Requests

**Case 1 — Run with defaults (no body)**

```http
POST /restapi/v2/workspaces/137687000271334001/alerts/137687000010815003/execute HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Run a report-attaching alert past a Data Warning tag**

```http
POST /restapi/v2/workspaces/137687000271334001/alerts/137687000010815003/execute HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "validateSystemTags": false
}
```

### Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. It confirms the run was **accepted and queued**, not that the alert fired.

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — The organisation's plan allows no alert schedules**

```json
{
    "status": "failure",
    "summary": "ALERT_NOTSUPPORTED",
    "data": {
        "errorCode": 6079,
        "errorMessage": "Your current plan does not support \"Data Alert\"."
    }
}
```

**HTTP 409 Conflict — Failure when `validateSystemTags` is left at its default on a flagged view**

```json
{
    "status": "failure",
    "summary": "SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION",
    "data": {
        "errorCode": 8241,
        "errorMessage": "To skip system tag validation, add the validateSystemTags parameter as 'false'."
    }
}
```

**HTTP 400 Bad Request — Alert no longer exists**

```json
{
    "status": "failure",
    "summary": "ALERT_DELETED",
    "data": {
        "errorCode": 32000009,
        "errorMessage": "The alert which your are trying to access was deleted."
    }
}
```

### Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`).

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`204` means queued, not evaluated** | The run is registered as a one-off scheduler task that fires shortly after the call returns — it does **not** execute inline. Poll [Get Alert Events](#10-get-alert-events) for the outcome rather than assuming the run has already happened when the response arrives. |
| **`204` never means "the alert fired"** | Whether the condition was met is recorded as an event. A `204` paired with a `notTriggered` event is the normal outcome when the data does not breach the rules. |
| **Not idempotent** | Each call queues another evaluation, and each evaluation that meets the condition notifies again. Repeating the request does not collapse into one run — guard retries. |
| **Notifications are real** | Every configured channel delivers if the condition is met. There is no preview, no send-to-self, and no undo. Treat it as a production action even in testing. |
| **The run executes as the alert's last modifier** | Not as the caller. A caller permitted to run someone else's alert triggers notifications in that alert's own ownership context. |
| **Works on a paused alert** | Pausing with [Change Alert Status](#8-change-alert-status) suppresses only the recurring schedule. |
| **The recurring schedule is unaffected** | A manual run does not shift or consume the next scheduled occurrence. |
| **The plan is checked at run time, not at create time** | An organisation whose plan allows zero alert schedules can hold alerts it cannot run (`6079`). |
| **`validateSystemTags` only bites on attachments** | The Data Warning check runs only when the alert's e-mail channel attaches or inlines the report. |
| **Scope is `modeling.create`** | The same scope as [Create Alert](#5-create-alert), even though nothing is created. A token scoped only to `modeling.update` can edit and pause an alert but cannot run it. |
| **Dependency chain** | [Get Alerts In Workspace](#1-get-alerts-in-workspace) → `alerts[].id` → Run Alert → [Get Alert Events](#10-get-alert-events) for the outcome. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 6079 | `ALERT_NOTSUPPORTED` — The organisation's plan allows no alert schedules. | Upgrade the plan, or add alert-schedule add-ons. |
| 7103 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is neither the DB Owner nor a custom-role user permitted to act on this alert, or the request arrived through a custom domain the workspace is not bound to. | Authenticate as the DB Owner, or as the alert's owner with Manage Data Alerts, from the standard API host. |
| 7319 | `OBJID_NOT_BELONGS_TO_DB` — The alert's view does not belong to the workspace in the URL. | Make `<workspace-id>` and `<alert-id>` consistent. |
| 7387 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not belong to the organisation in `ZANALYTICS-ORGID`. | Send the organisation id that owns the workspace. |
| 8060 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use a domain you have purchased from Zoho Analytics, or the standard API host. |
| 8080 | `INVALID_JSON_CONFIGURATION` — `CONFIG` was sent but is not a parseable JSON object. | Send a valid, URL-encoded JSON object, or omit `CONFIG` entirely. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| 8241 | `SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION` — The alert attaches a report from a view carrying a restricted Data Warning tag. HTTP 409. | Resolve the data warning, or resend with `"validateSystemTags": false`. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |
| 32000009 | `ALERT_DELETED` — The alert has been deleted or never existed. | Re-discover the id with [Get Alerts In Workspace](#1-get-alerts-in-workspace). |

---

## 10. Get Alert Events

Returns the audit trail of one alert's evaluations — when each ran, and whether it triggered, did not trigger, or failed. This is the only machine-readable source of an alert's outcome, and the only paginated API in this family.

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/alerts/<alert-id>/events` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the workspace. |
| **Permission Required** | The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the workspace, **or** a custom-role user with the **Manage Data Alerts** permission who either has all-alerts access or **owns this alert**. |

### CONFIG Parameters

CONFIG is **optional** for this API and is sent as a query parameter. Omitting it returns the first 100 events across the full 45-day retention window.

| Parameter | Type | Mandatory | Default | Max Length | Description |
|-----------|------|-----------|---------|------------|-------------|
| `fromDate` | String | No | Start of day, 44 days before today | 50 | Inclusive lower bound, as `yyyy-MM-dd HH:mm:ss` or `yyyy-MM-dd` (the time then defaults to `00:00:00.000`). Interpreted in the **caller's profile time zone**. A malformed value is `32000028`. |
| `toDate` | String | No | End of today | 50 | Inclusive upper bound, same formats. A date-only value defaults the time to `23:59:59.999`. Must be greater than or equal to `fromDate`, otherwise `8119`. |
| `status` | JSONArray of String | No | All outcomes | 200 | Outcome filter, **1–3 distinct entries** drawn from `triggered`, `notTriggered` and `error`. Duplicates collapse silently. An unknown value, or a non-string entry, is `8119`. See [Alert Event Statuses](#alert-event-statuses). |
| `pageNo` | Integer | No | `1` | — | 1-based page number, **1–100000**. |
| `recordsPerPage` | Integer | No | `100` | — | Page size, **1–100**. A larger value is **silently clamped** to 100 — compare `pageDetails.recordsPerPage` against what you asked for. |

### Sample Requests

**Case 1 — Defaults: first page of the full retention window**

```http
GET /restapi/v2/workspaces/137687000271334001/alerts/137687000010815003/events HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — A date range, an outcome filter and a smaller page**

```http
GET /restapi/v2/workspaces/137687000271334001/alerts/137687000010815003/events?CONFIG={"fromDate":"2026-05-01 00:00:00","toDate":"2026-05-31 23:59:59","status":["triggered","error"],"pageNo":1,"recordsPerPage":50} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — Unknown value in the `status` filter (rejected)**

```http
GET /restapi/v2/workspaces/137687000271334001/alerts/137687000010815003/events?CONFIG={"status":["failed"]} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Sample Responses

**HTTP 200 OK — Mixed outcomes, more pages available**

```json
{
    "status": "success",
    "summary": "Get alert events",
    "data": {
        "alertEvents": [
            {
                "alertTime": "1779226560981",
                "status": "triggered"
            },
            {
                "alertTime": "1779228341225",
                "status": "error",
                "message": "Given date value 'East 23:59:59' is not compatible with the given date format 'dd MMM yyyy HH:mm:ss'",
                "errorCode": "INCOMPATIBLE_DATE_VALUE"
            },
            {
                "alertTime": "1779228341230",
                "status": "notTriggered"
            }
        ],
        "pageDetails": {
            "pageNo": 1,
            "recordsPerPage": 50,
            "hasNextPage": true
        }
    }
}
```

**HTTP 200 OK — No events matched the filters**

```json
{
    "status": "success",
    "summary": "Get alert events",
    "data": {
        "alertEvents": [],
        "pageDetails": {
            "pageNo": 1,
            "recordsPerPage": 100,
            "hasNextPage": false
        }
    }
}
```

**HTTP 400 Bad Request — Failure paired with Case 3**

```json
{
    "status": "failure",
    "summary": "INVALID_VALUE_FOR_ATTRIBUTE",
    "data": {
        "errorCode": 8119,
        "errorMessage": "Invalid value 'failed' provided for the attribute 'status'. Only 'triggered, error, notTriggered' are allowed."
    }
}
```

**HTTP 400 Bad Request — `fromDate` later than `toDate`**

```json
{
    "status": "failure",
    "summary": "INVALID_VALUE_FOR_ATTRIBUTE",
    "data": {
        "errorCode": 8119,
        "errorMessage": "Invalid value '2026-05-31 > 2026-05-01' provided for the attribute 'fromDate'."
    }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | `"Get alert events"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.alertEvents` | JSONArray | One entry per evaluation inside the requested window, **oldest first** (ascending `alertTime`). **Always present**; `[]` when nothing matched — still HTTP 200. |
| `alertEvents[].alertTime` | String | When the evaluation happened, as **epoch milliseconds in a string** (`"1779226560981"`) — deliberately unformatted so the caller can render it in its own locale and time zone. **Conditional**: omitted on the rare feed row with no stored timestamp. |
| `alertEvents[].status` | String | Outcome as a stable enum: `triggered`, `notTriggered` or `error`. **Always present.** Unlike `lastRunStatus` of the listing APIs this value is **not localised** and is safe to switch on. Any unrecognised stored code is reported as `notTriggered`. |
| `alertEvents[].message` | String | Description of the failure. **Conditional** — present only when a message was recorded, which in practice means `status` is `error`. |
| `alertEvents[].errorCode` | String | **Symbolic error name** of the failure, e.g. `INCOMPATIBLE_DATE_VALUE`. **Conditional** — present only when `status` is `error`. Note it is a *name*, not one of the numeric codes used by the Error Codes tables. |
| `data.pageDetails` | JSONObject | Pagination block. **Always present** — this API always paginates, even when the caller sends no pagination attributes. |
| `pageDetails.pageNo` | Number | The page that was served, 1-based. Native JSON number. |
| `pageDetails.recordsPerPage` | Number | The **effective** page size, already clamped to the 100-record maximum. Compare it against what you requested. |
| `pageDetails.hasNextPage` | Boolean | `true` when more records match the filters. Re-issue with `pageNo + 1`; **do not infer the end of the data from a short page.** |

> `feed` (the snapshot file id) and `contentType` exist on the underlying audit row but are deliberately **not** exposed by this API. Do not build on them appearing.

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **The only machine-readable outcome** | `alertEvents[].status` is a stable enum. `lastRunStatus` in [Get Alerts In Workspace](#1-get-alerts-in-workspace) is a translated label and must never be parsed. |
| **Events come back oldest first** | The audit rows are sorted ascending by timestamp, so the newest event is the **last** entry on the **last** page. To read the most recent outcome, walk to the end rather than taking `alertEvents[0]`. |
| **Always paginated** | `pageDetails` is present whether or not you asked for paging, `recordsPerPage` is clamped to 100, and "more data" is signalled by `hasNextPage` rather than by a full page. Loop on `hasNextPage`, not on page length. |
| **History is retained for 45 days, inclusive of today** | Older events are purged, not filtered, so a wider `fromDate` cannot recover them. The implicit lower bound is start-of-day 44 days ago, which together with end-of-today spans exactly 45 calendar days. |
| **Date defaults are asymmetric** | With neither bound supplied the range is the full retention window. With only `fromDate` the upper bound is end-of-today; with only `toDate` the lower bound is the start of the retention window. All four combinations are resolved in the caller's profile time zone. |
| **Date-only values are expanded** | `fromDate: "2026-05-01"` becomes `00:00:00.000` and `toDate: "2026-05-31"` becomes `23:59:59.999`, so a date-only range is inclusive of both whole days. |
| **An empty result is a success** | `[]` means the filters matched nothing, which is also what a brand-new alert returns. |
| **`errorCode` here is a name, not a number** | It is the symbolic name recorded on the audit row, unrelated to the numeric codes in the Error Codes tables. |
| **CONFIG travels in the query string** | This is a `GET`; send `CONFIG` as a URL-encoded query parameter, not as a body. No `Content-Type` header is needed. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get Alerts In Workspace](#1-get-alerts-in-workspace) → `alerts[].id` → Get Alert Events; after [Run Alert](#9-run-alert), poll here for the outcome. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7103 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is neither the DB Owner nor a custom-role user permitted to act on this alert, or the request arrived through a custom domain the workspace is not bound to. | Authenticate as the DB Owner, or as the alert's owner with Manage Data Alerts, from the standard API host. |
| 7319 | `OBJID_NOT_BELONGS_TO_DB` — The alert's view does not belong to the workspace in the URL. | Make `<workspace-id>` and `<alert-id>` consistent. |
| 7387 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not belong to the organisation in `ZANALYTICS-ORGID`. | Send the organisation id that owns the workspace. |
| 8060 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use a domain you have purchased from Zoho Analytics, or the standard API host. |
| 8080 | `INVALID_JSON_CONFIGURATION` — `CONFIG` was sent but is not a parseable JSON object. | Send a valid, URL-encoded JSON object, or omit `CONFIG` entirely. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| 8119 | `INVALID_VALUE_FOR_ATTRIBUTE` — `fromDate` is later than `toDate`, or a `status` entry is not one of `triggered`, `notTriggered`, `error`, or `pageNo` / `recordsPerPage` is outside its declared range. | Correct the range, the filter values, or the paging numbers. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |
| 32000009 | `ALERT_DELETED` — The alert has been deleted or never existed. | Re-discover the id with [Get Alerts In Workspace](#1-get-alerts-in-workspace). |
| 32000028 | `INVALID_DATE_VALUE` — `fromDate` or `toDate` is not `yyyy-MM-dd HH:mm:ss` or `yyyy-MM-dd`. | Reformat the bound. |

---

## Appendix A – Common HTTP Headers

| Header | Value | Required | Description |
|--------|-------|----------|-------------|
| `Authorization` | `Zoho-oauthtoken <oauth-token>` | **Mandatory** | OAuth 2.0 access token of the calling user. Must carry the scope matching the operation (see [Appendix B](#appendix-b--oauth-scope-summary)). |
| `ZANALYTICS-ORGID` | Organization ID string | **Mandatory** | Organization ID of the workspace that owns the alert. Missing header is `8083`; an id that does not own the workspace is `7387`. Read it from **Settings → Organisation** in the Zoho Analytics UI, or take it from the `orgId` field of any listing API response. |
| `Content-Type` | `application/x-www-form-urlencoded` | Conditional | Required by the five APIs that send a `CONFIG` **body**: [Create Alert](#5-create-alert), [Update Alert](#6-update-alert), [Delete Alerts](#7-delete-alerts), [Change Alert Status](#8-change-alert-status) and [Run Alert](#9-run-alert) when it carries `validateSystemTags`. Note that [Delete Alerts](#7-delete-alerts) is a `DELETE` **with** a body. [Get Alert Events](#10-get-alert-events) passes `CONFIG` in the query string instead and needs no `Content-Type`; the other four read APIs send no payload at all. |
| `Host` | `analyticsapi.zoho.com` (or the DC equivalent) | **Mandatory** | A Client Portal / White Label custom domain is accepted **only** when the target workspace is bound to that same domain; otherwise `7301`. See [White Label / Client Portal Behaviour](#white-label--client-portal-behaviour). |

> **`ZANALYTICS-DEST-ORGID` is not used by any API in this document.** That header applies only to cross-organization copy operations (Copy Workspace, [Copy Views](../06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#2-copy-views), Copy Formulas). The Alert APIs have no cross-organization targeting mechanism.

`CONFIG` is always a **URL-encoded form parameter** (or query parameter for [Get Alert Events](#10-get-alert-events)) — never a raw JSON request body.

Example:

```http
PUT /restapi/v2/workspaces/137687000271334001/alerts/status HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG=%7B%22alertIds%22%3A%5B%22137687000010815003%22%5D%2C%22enabled%22%3Afalse%7D
```

---

## Appendix B – OAuth Scope Summary

| API | HTTP Method | Scope |
|-----|-------------|-------|
| Get Alerts In Workspace | GET | `ZohoAnalytics.metadata.read` |
| Get Alerts In View | GET | `ZohoAnalytics.metadata.read` |
| Get View Metadata For Alert | GET | `ZohoAnalytics.metadata.read` |
| Get Alert Configuration | GET | `ZohoAnalytics.metadata.read` |
| Create Alert | POST | `ZohoAnalytics.modeling.create` |
| Update Alert | PUT | `ZohoAnalytics.modeling.update` |
| Delete Alerts | DELETE | `ZohoAnalytics.modeling.delete` |
| Change Alert Status | PUT | `ZohoAnalytics.modeling.update` |
| Run Alert | POST | `ZohoAnalytics.modeling.create` |
| Get Alert Events | GET | `ZohoAnalytics.metadata.read` |

> This family **spans two scope groups**: all five read APIs use `metadata.read`, and all five write APIs use `modeling.*`. An integration that discovers and manages alerts therefore needs `ZohoAnalytics.metadata.read` **plus** the relevant `ZohoAnalytics.modeling.*` scopes — a token holding only `modeling` cannot discover `<alert-id>` or `viewColumnIndex` values, and a token holding only `metadata` is read-only. Note also that the verb follows the **HTTP method**, not the effect: [Change Alert Status](#8-change-alert-status) needs `modeling.update` although it changes nothing structural, and [Run Alert](#9-run-alert) needs `modeling.create` although it creates nothing. A token scoped to `modeling.update` alone can edit and pause an alert but cannot run it.
>
> No API in this document uses the `data` scope family — none of them reads or writes table rows. [Get Alert Events](#10-get-alert-events) reads audit history, which is metadata.

---

## Appendix C – API-Specific Notes and Behaviours

### Get Alerts In Workspace

- **Workspace-wide permission, not per view.** A single alert permission on the workspace lists every alert in it, including alerts on views the caller could not configure. Acting on those alerts is a separate, stricter check.
- **Timestamps are in the caller's time zone, not the alert's.** Two users see different wall-clock values for the same `nextScheduleTime`; the alert's own `scheduleDetails.timeZone` is not what renders this response.
- **`lastRunStatus` is localised prose.** `"Condition met"` / `"Condition unmet"` change with the caller's language. The stable equivalent is `alertEvents[].status` from [Get Alert Events](#10-get-alert-events).
- **Missing values are `""`, never `null`.** A never-run alert has three empty timestamp fields; a paused alert has four.
- **No paging, no filter, no sort.** The entire alert list comes back in one response — filter client-side.
- **Owner e-mail is best-effort.** `createdBy` and `lastModifiedBy` come from a remote identity lookup; a failure yields `""` rather than failing the call.
- **Dependency chain:** [Get Workspace List](../03%20%C2%B7%20Workspace%20Management/WORKSPACE_OPERATIONS.md) → Get Alerts In Workspace → `alerts[].id` for every alert-id-addressed API here.

### Get Alerts In View

- **Same payload, stricter gate.** Entries are byte-identical in shape to the workspace listing, but the caller must be the DB Owner or hold `CREATEALERT` on that specific view.
- **The view/workspace pair is validated.** A mismatched pair is `7319`, not an empty list.
- **It does not check the view type.** An unsupported report has no alerts and returns `[]` like any other. Use [Get View Metadata For Alert](#3-get-view-metadata-for-alert), which fails with `8245`, to test alert capability.
- **Dependency chain:** [Get View List](../06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#6-get-view-list) → `<view-id>` → Get Alerts In View → `alerts[].id`.

### Get View Metadata For Alert

- **The only source of `viewColumnIndex`.** The Alert APIs neither accept nor return internal column ids, so no rule can be built correctly without this call.
- **`viewColumnIndex` is positional and changes when the report changes.** Cache it for one build-a-rule workflow, never across report edits — a stale index either resolves to a different column or fails with `32000041`.
- **`allowedOperators` and `allowedRuleTypes` are the authoritative allow-lists.** They are computed per column from its add-on type, data type, aggregation and geo role — fields that are not all present in the response, so never derive them yourself. Sending anything outside them is `8119`.
- **`thresholds` doubles as the feature switch for threshold rules.** An empty array is exactly why `threshold` is missing from that column's `allowedRuleTypes`.
- **`allowedAnomalyOperators` is view-level, not column-level.** It is derived from the X axis's date bucket: `YEAR` yields the yearly tokens, `ABSMONTH` the monthly ones, `DATE` / `TIMESTAMP` the full day-level set. With anomalies but no date-bucketed X axis it degrades to `["sinceLastAlert"]`; with no anomalies at all it is `[]`.
- **`anomalies` is hoisted to the top level.** The underlying payload repeats it on every column; do not look for it inside `viewColumns[]`.
- **`viewType` returns internal tokens.** `AnalysisView`, `Pivot`, `SummaryView` — not the UI labels "Chart View", "Pivot View", "Summary View".
- **It reads structure, not data.** No rows are scanned, so calling it before every write costs nothing.
- **Dependency chain:** [Get View List](../06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#6-get-view-list) → Get View Metadata For Alert → `viewColumnIndex` / `thresholds` / `anomalyName` → [Create Alert](#5-create-alert).

### Get Alert Configuration

- **The response is a ready-to-post request body, with two caveats.** It is emitted in exactly the CONFIG shape of [Create Alert](#5-create-alert) / [Update Alert](#6-update-alert), which makes read-modify-write the intended editing pattern — but `actionsByFlow[].actionConfigId` / `connectionId` come back as JSON numbers and must be converted to strings before posting back, and `conditionExpression` is returned unvalidated.
- **`scheduleDetails` is normalised on the way out.** Whatever was stored, the response uses array-valued `weekDays` / `monthDays` / `months`, an explicit 1-based `interval`, and includes `skipWeekends` only for `hourly` and `daily` — so it satisfies the strict applicability check (`32000052`) when posted straight back.
- **Legacy schedules are read and upgraded.** A stored minutes-from-midnight schedule (`570_daily`) is parsed correctly, and re-saving the alert rewrites it in the current form. `32000034` appears only when the stored value cannot be parsed at all.
- **Orphaned references are dropped silently.** `rowAxis`, `columnAxis` and `rules[].viewColumnIndex` are omitted when the referenced column no longer exists, so a round trip can quietly lose an axis.
- **`conditionExpression` is *not* sanitised.** It is returned exactly as stored, so a legacy alert can hand you an expression that references more rules than exist. Validate it against `rules.length` before posting it back, or the write fails with `32000020`.
- **Absent means absent.** Unconfigured channels, `workflows`, `actionsByFlow` and the axes are omitted rather than returned as `null` or `{}`. Test for key presence. `conditionExpression` is the lone attribute that uses `""`.
- **`isAnomaly` is read-only.** It is derived from `rules[]` on write and overwritten whatever you send.
- **Channel secrets are returned in clear text.** Webhook and messaging URLs, header and parameter values, and custom payloads are decrypted for an authorised caller. Treat the response as sensitive.
- **Dependency chain:** [Get Alerts In Workspace](#1-get-alerts-in-workspace) → `alerts[].id` → Get Alert Configuration → edit → [Update Alert](#6-update-alert).

### Create Alert

- **Every reference is validated against the live view, not merely parsed.** Column indexes must resolve (`32000041`), threshold names must exist on that column (`32000038`), anomaly names must exist on the view (`32000042`), and cross-column rules must point at a NUMBER column of the same view (`32000036` / `32000037`).
- **At least one notification channel is mandatory.** An alert with rules but no channel would evaluate and tell nobody, so it is refused (`32000001`) — and a channel that resolves to no recipient is discarded before that check runs (`32000013`), which is how a request carrying an `email` object can still fail with `32000001`.
- **The e-mail recipient ceiling is 25, not 1000.** The request template permits 1,000 entries and the business layer then rejects anything above 25 with `32000007`. Use `groupIds` or `notifyAdmins` for wider distribution.
- **Anomaly rules are all-or-nothing.** Either every entry in `rules[]` carries an `anomaly` object or none does (`32000017`), anomaly rules must not carry `viewColumnIndex` (`32000046`), and anomaly and `threshold` rule types are Chart-only (`32000019`).
- **`workflows` and `actionsByFlow` are rejected here** (`32000049`). Both refer to mappings that cannot exist before the alert does, so they belong to [Update Alert](#6-update-alert).
- **`conditionExpression` defaults only for a single rule.** With more than one rule and no expression the request fails with `8079` rather than defaulting to `(1)`.
- **`isAnomaly` is ignored on input.** It is derived from the rules so that a [Get Alert Configuration](#4-get-alert-configuration) response can be posted back unchanged.
- **The alert is created live.** Its schedule registers immediately, so an evaluation can happen before you have read the configuration back.
- **The response carries only `alertId`.** Nothing is echoed; call [Get Alert Configuration](#4-get-alert-configuration) to see how the input was normalised.
- **Plan limits are not checked here.** An alert can be created on an organisation plan that will refuse to run it (`6079` at [Run Alert](#9-run-alert)).
- **Dependency chain:** [Get View List](../06%20%C2%B7%20Views%20Management/VIEW_OPERATIONS.md#6-get-view-list) → [Get View Metadata For Alert](#3-get-view-metadata-for-alert) → Create Alert → `data.alertId`.

### Update Alert

- **It is a full replace, not a patch.** The CONFIG you send becomes the alert; attributes you leave out are not preserved. Omitting a channel removes it, and omitting `notifyOnChange` resets it to `false`. Start from [Get Alert Configuration](#4-get-alert-configuration) output.
- **The alert id never changes.** Unlike [Update Email Schedule](EMAIL_SCHEDULES.md#3-update-email-schedule), which can mint a new id when the name or period changes, an alert keeps its identity across every update.
- **The view is immutable.** There is no `<view-id>` in the URL and no CONFIG attribute for it. Moving an alert means deleting and recreating it, which resets its event history.
- **It is the only API that accepts `workflows` and `actionsByFlow`,** and both only *re-assert* mappings that already exist — unmapped workflow ids fail with `32000043` and unmapped Flow action ids with `32000050`, each listing every offending id in one message.
- **`workflows` is validated by `id` alone.** `name` and `enabled` are display fields, are not part of the write contract, and are not compared against the stored mapping — so an unedited [Get Alert Configuration](#4-get-alert-configuration) response posts back cleanly.
- **Everything Create Alert validates is validated again**, since both share one conversion path.
- **Permission is ownership-based.** A custom-role user without all-alerts access can update only their own alerts, even on a view they may create alerts on.
- **Success is `204` with an empty body**, so the only way to confirm what was stored is to read it back.
- **Dependency chain:** [Get Alert Configuration](#4-get-alert-configuration) → edit → Update Alert → [Get Alert Configuration](#4-get-alert-configuration) to verify.

### Delete Alerts

- **It takes a list, and the list is validated up front.** Every id is checked for workspace membership and caller permission *before* anything is deleted, so one bad id fails the whole call and nothing is removed.
- **`alertIds` entries must be JSON strings.** Numeric literals are rejected.
- **An empty array is accepted and does nothing**, answering `204`.
- **Nothing is reported per id**, so "deleted" and "already absent" are indistinguishable from the response alone.
- **It is a status change under the hood, not a purge.** The alert stops evaluating, disappears from the listing APIs, and its id stops being actionable (`32000009`). There is no trash and no restore.
- **Not the way to silence an alert temporarily** — [Change Alert Status](#8-change-alert-status) is reversible and keeps the event history.
- **Dependency chain:** [Get Alerts In Workspace](#1-get-alerts-in-workspace) → Delete Alerts.

### Change Alert Status

- **One request sets one state for many alerts.** `enabled` applies to every id; to enable some and pause others, send two requests.
- **Same up-front validation as Delete Alerts.** All ids are checked before any status changes.
- **Idempotent.** Setting an alert to the state it already has is not an error and still answers `204`.
- **Pausing stops the schedule, not the history.** `nextScheduleTime` becomes `""` while `lastRunTime`, `lastAlertSentTime` and everything in [Get Alert Events](#10-get-alert-events) survive.
- **A paused alert can still be run on demand** with [Run Alert](#9-run-alert) — pausing suppresses the schedule, not manual evaluation.
- **Its scope is `modeling.update`,** matching the HTTP method rather than the much narrower effect.
- **Dependency chain:** [Get Alerts In Workspace](#1-get-alerts-in-workspace) (read `enabled`) → Change Alert Status → verify.

### Run Alert

- **`204` means "queued", not "evaluated" and certainly not "fired".** The run is registered as a one-off scheduler task that fires shortly after the response, so do not assume the evaluation has completed when the call returns. Read the newest entry from [Get Alert Events](#10-get-alert-events) for the outcome.
- **Notifications are really sent.** This is not a dry run: if the condition is met, every configured channel delivers. There is no preview mode.
- **The evaluation executes as the alert's last modifier**, not as the caller, so notifications are attributed to that alert's own ownership context.
- **`validateSystemTags` defaults to `true`** and bites only when the alert attaches the report to an e-mail — it then checks the view's Data Warning system tags and refuses with `8241` (HTTP 409) rather than mailing a report flagged as unreliable.
- **The organisation plan is checked at run time.** An organisation whose plan allows zero alert schedules is refused with `6079` even though the alert exists.
- **`CONFIG` is optional here** — the only attribute it can carry is `validateSystemTags`.
- **Its scope is `modeling.create`,** the same as [Create Alert](#5-create-alert).
- **Dependency chain:** [Get Alerts In Workspace](#1-get-alerts-in-workspace) → Run Alert → [Get Alert Events](#10-get-alert-events).

### Get Alert Events

- **The audit trail, and the only machine-readable outcome.** `status` is one of `triggered`, `notTriggered`, `error` and is **not** localised — unlike `lastRunStatus` of the listing APIs.
- **Events are returned oldest first.** The newest evaluation is the last entry on the last page; `alertEvents[0]` is the *oldest* match, not the most recent.
- **The response is always paginated**, whether or not the caller asks: `pageDetails` is always present, `recordsPerPage` is clamped to 100, and more data is signalled by `hasNextPage` rather than by a full page. Loop on `hasNextPage`, not on page length.
- **`alertTime` is epoch milliseconds in a string**, deliberately unformatted so callers can render it in their own locale and time zone.
- **`errorCode` on an event is a symbolic name** (e.g. `INCOMPATIBLE_DATE_VALUE`), not one of the numeric codes in the Error Codes tables, and appears only when `status` is `error`.
- **History is retained for 45 days inclusive of today.** Older events are deleted, not filtered, so a wider `fromDate` cannot recover them.
- **An empty `alertEvents` array is a success.** It means the filters matched nothing, which is also what a brand-new alert returns.
- **`feed` (snapshot file id) and `contentType` exist internally but are intentionally not exposed** — do not build on them appearing later.
- **Dependency chain:** [Get Alerts In Workspace](#1-get-alerts-in-workspace) → `alerts[].id` → Get Alert Events.

---

## Appendix D – General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Four of ten APIs return 204 with no body** | [Update Alert](#6-update-alert), [Delete Alerts](#7-delete-alerts), [Change Alert Status](#8-change-alert-status) and [Run Alert](#9-run-alert) return HTTP **204 No Content** on success — treat the status code as the success indicator and never expect or parse a JSON body. The other six return the standard `{"status", "summary", "data"}` envelope with HTTP 200. |
| **Nothing is echoed by the write APIs** | [Create Alert](#5-create-alert) returns only the new `alertId`; update, delete, status and run return nothing at all. The authoritative post-write state always comes from a follow-up read. |
| **Failure responses always carry a body** | Even for the 204 APIs, errors return `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. On failure `summary` is the error's **symbolic name** (e.g. `ALERT_DELETED`, `SUBFLOW_ID_NOT_MAPPED_TO_ALERT`), not a localised sentence; the sentence is in `data.errorMessage`. |
| **`summary` on success is a localised label** | `"Get alerts in workspace"`, `"Create alert"`, `"Get alert configuration"`, … It changes with the caller's language, so never branch on it. |
| **All IDs are strings — and must be sent back as strings** | `alerts[].id`, `data.alertId`, `viewId`, `viewColumnIndex`, `workflows[].id`, `groupIds[]` and every `alertIds[]` entry are JSON **strings** even though the values are numeric. Parse them as strings or longs, never as native JSON numbers, to avoid precision loss. Sending a bare numeric literal where a string is expected is `8080`. |
| **Two exceptions are genuine JSON numbers** | `actionsByFlow[].actionConfigId` and `actionsByFlow[].connectionId` come back as numbers, as do `pageDetails.pageNo` and `pageDetails.recordsPerPage`. `enabled`, `hasNextPage`, `isAnomaly` and `notifyOnChange` are native booleans. The `actionsByFlow` pair is the one place where the read and write contracts disagree: [Update Alert](#6-update-alert) requires both back as **strings** — see [`actionsByFlow` Fields](#actionsbyflow-fields). |
| **Timestamps come in two flavours** | The listing APIs use **ISO-8601 with offset** in the caller's profile time zone (`2026-03-20T10:00:00+05:30`); [Get Alert Events](#10-get-alert-events) uses **epoch milliseconds as a string** (`"1779226560981"`). No API returns a formatted local date string. |
| **Empty string, not `null`, for absent timestamps** | `lastRunTime`, `lastAlertSentTime`, `lastRunStatus` and `nextScheduleTime` are `""` when they do not apply. No Alert API returns JSON `null`. |
| **Optional objects are omitted, not emptied** | [Get Alert Configuration](#4-get-alert-configuration) leaves out unconfigured channels, `workflows`, `actionsByFlow`, `rowAxis`, `columnAxis`, and empty `emailIds` / `groupIds` / `params` / `headers` entirely. Test for key presence rather than truthiness. `conditionExpression` is the one attribute that uses `""` instead. |
| **Arrays that are always present** | `data.alerts` (both listing APIs), `data.viewColumns` / `data.anomalies` / `data.allowedAnomalyOperators` ([Get View Metadata For Alert](#3-get-view-metadata-for-alert)), `data.rules` ([Get Alert Configuration](#4-get-alert-configuration)), and `data.alertEvents` + `data.pageDetails` ([Get Alert Events](#10-get-alert-events)) are always returned, empty when there is nothing to report. |
| **An empty collection is a success** | An empty `alerts`, `anomalies` or `alertEvents` array comes back with HTTP 200. Never infer failure from emptiness. |
| **Only Get Alert Events paginates** | Every other API returns its full result set in one response; there is no `pageDetails` block anywhere else, and no sort or filter parameters either. |
| **Enums versus labels** | Machine-readable enums: `alertEvents[].status`, `summaryType`, `calendarFrequency`, `rules[].type`, `messageType`, `attachmentType`, `viewType`. Localised labels that must not be parsed: the success `summary`, `alerts[].lastRunStatus`, and `data.errorMessage`. |
| **Responses are extensible** | Some builds return additional fields. Ignore unrecognised keys rather than validating against a closed schema. |
| **`32000xxx` codes are alert-specific** | Every code in the `32000001`–`32000053` range is raised only by the alert subsystem. The `6xxx` / `7xxx` / `8xxx` codes are shared across API families, so match on the `summary` symbolic name as well as `errorCode` when handling errors generically. |

---

## Appendix E – Enum and Value Reference

#### `rules[].operator` Values

Always restrict your choice to the column's `allowedOperators` array from [Get View Metadata For Alert](#3-get-view-metadata-for-alert). The tables below explain what each token means and how many entries `values` must carry.

**Comparison and equality operators** — NUMBER, dimensional (text) and `DATE` / `TIMESTAMP` columns. Date columns require `yyyy-MM-dd HH:mm:ss` or `yyyy-MM-dd` values.

| Operator | Meaning | `values` shape |
|----------|---------|----------------|
| `is` | Equal to, or IN the list on a categorical / date-bucket column. | 1+ entries on a categorical or date-bucket column; **exactly 1** on NUMBER, `DATE` or `TIMESTAMP` (`32000053` otherwise). |
| `isnot` | Not equal to, or NOT IN the list. | Same as `is`. |
| `gt` | Strictly greater than. | Exactly 1. |
| `lt` | Strictly less than. | Exactly 1. |
| `gte` | Greater than or equal. | Exactly 1. |
| `lte` | Less than or equal. | Exactly 1. |
| `btw` | Between, inclusive. | Exactly 2 — `[lower, upper]` (`32000039` otherwise). |
| `notbtw` | Outside the inclusive range. | Exactly 2. |

**Null-check operators** — valid on every column kind.

| Operator | Meaning | `values` shape |
|----------|---------|----------------|
| `isn` | The column value is NULL. | Omit `values` (`32000047` if supplied). |
| `notisn` | The column value is not NULL. | Omit `values`. |

**Relative date-bucket operators, no value** — available on `DATE` / `TIMESTAMP` columns and on the matching `YEAR` / `ABSQUARTER` / `ABSMONTH` / `ABSWEEK` dimensional buckets.

| Operator | Meaning |
|----------|---------|
| `curYear` / `prevYear` / `nextYear` | The current, previous or next calendar year. |
| `curQuarter` / `prevQuarter` / `nextQuarter` | The current, previous or next quarter. |
| `curMonth` / `prevMonth` / `nextMonth` | The current, previous or next month. |
| `curWeek` / `prevWeek` / `nextWeek` | The current, previous or next week. |
| `today` / `yest` / `tom` | Today, yesterday, tomorrow. |

All of these must **omit** `values`.

**N-period date-bucket operators, one value** — same column kinds, but each requires exactly one numeric string: the N.

| Operator | Meaning | Example `values` |
|----------|---------|------------------|
| `prevNYears` / `lastNYears` / `nextNYears` | The previous, trailing or next N years. | `["3"]` |
| `prevNQuarters` / `lastNQuarters` / `nextNQuarters` | The previous, trailing or next N quarters. | `["2"]` |
| `prevNMonths` / `lastNMonths` / `nextNMonths` | The previous, trailing or next N months. | `["6"]` |
| `prevNWeeks` / `lastNWeeks` / `nextNWeeks` | The previous, trailing or next N weeks. | `["4"]` |
| `prevNDays` / `lastNDays` / `nextNDays` | The previous, trailing or next N days. | `["7"]` |

**Anomaly-only operator.**

| Operator | Meaning | `values` shape |
|----------|---------|----------------|
| `sinceLastAlert` | Trigger when an anomaly has been detected since the alert's last successful run. | Omit `values`. The operator's argument, if any, goes in `anomaly.value`. |

On an anomaly rule the operator must come from the view's `allowedAnomalyOperators`, which is `["sinceLastAlert"]` unless the view's X axis is date-bucketed — in which case the matching bucket's date operators are offered instead.

#### Which operators each column kind offers

| Column kind (metadata `dataType` / `operation`) | Operators offered |
|---|---|
| NUMBER measure, `operation` other than `MEACATEGORY` | `is`, `isnot`, `gt`, `lt`, `gte`, `lte`, `btw`, `notbtw`, `isn`, `notisn` |
| NUMBER measure with `operation: "MEACATEGORY"` (pivot measures) | `btw`, `notbtw` |
| Dimensional text column | `is`, `isnot`, `isn`, `notisn` |
| Dimensional with `operation: "YEAR"` | `is`, `isnot` plus the year-bucket operators |
| Dimensional with `operation: "ABSQUARTER"` | `is`, `isnot` plus the quarter-bucket operators |
| Dimensional with `operation: "ABSMONTH"` | `is`, `isnot` plus the month-bucket operators |
| Dimensional with `operation: "ABSWEEK"` | `is`, `isnot` plus the week-bucket operators |
| Dimensional absolute-date categorical column | `is`, `isnot` only |
| Dimensional geo column with geometry role | `isn`, `notisn` only |
| `DATE` / `TIMESTAMP` column | `is`, `isnot`, `gte`, `lt`, `btw`, `notbtw` plus every date-bucket operator |

#### Date and Time Value Format

For `DATE` / `TIMESTAMP` columns the scalar operators (`is`, `isnot`, `gt`, `lt`, `gte`, `lte`, `btw`, `notbtw`) accept:

- `yyyy-MM-dd HH:mm:ss` — e.g. `2026-01-12 10:00:00`
- `yyyy-MM-dd` — e.g. `2026-01-12`, with the time defaulting to `00:00:00`

Anything else is `32000028`. The same two formats apply to `fromDate` / `toDate` of [Get Alert Events](#10-get-alert-events), where a date-only `toDate` is expanded to `23:59:59.999` instead. Date-bucket operators take no value at all.

#### Alert Event Statuses

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `triggered` | The rules matched and the configured channels were notified. | — |
| `notTriggered` | The alert was evaluated and the rules did not match. Also the fallback for any unrecognised stored outcome. | — |
| `error` | The evaluation itself failed. The event carries `errorCode` and `message`. | — |

Accepted in the `status` filter of [Get Alert Events](#10-get-alert-events) as 1–3 distinct entries; anything else is `8119`.

#### Day and Month Numbering

| Field | Numbering |
|-------|-----------|
| `weekDays`, `dayOfWeek` | **1 = Sunday … 7 = Saturday.** |
| `monthDays` | **1–31**, or the single-entry list `[99]` meaning "last day of the month". |
| `weekOfMonth` | **1 = first … 4 = fourth, 5 = last.** |
| `months` | **1 = January … 12 = December.** |

---

## Appendix F – CONFIG Attribute Availability by API

Only five APIs accept CONFIG. `✔` means the attribute is accepted; `—` means it is not part of that API's contract.

| Attribute | [Create Alert](#5-create-alert) | [Update Alert](#6-update-alert) | [Delete Alerts](#7-delete-alerts) | [Change Alert Status](#8-change-alert-status) | [Run Alert](#9-run-alert) | [Get Alert Events](#10-get-alert-events) |
|-----------|---|---|---|---|---|---|
| `alertName` | **Yes** | **Yes** | — | — | — | — |
| `summaryType` | Conditional | Conditional | — | — | — | — |
| `rowAxis` | Conditional | Conditional | — | — | — | — |
| `columnAxis` | No | No | — | — | — | — |
| `conditionExpression` | Conditional | Conditional | — | — | — | — |
| `notifyOnChange` | No | No | — | — | — | — |
| `isAnomaly` | ✔ (ignored) | ✔ (ignored) | — | — | — | — |
| `scheduleDetails` | **Yes** | **Yes** | — | — | — | — |
| `email` | No\* | No\* | — | — | — | — |
| `notification` | No\* | No\* | — | — | — | — |
| `slack` | No\* | No\* | — | — | — | — |
| `msteams` | No\* | No\* | — | — | — | — |
| `webhook` | No\* | No\* | — | — | — | — |
| `workflows` | Rejected (`32000049`) | No | — | — | — | — |
| `actionsByFlow` | Rejected (`32000049`) | No | — | — | — | — |
| `rules` | **Yes** | **Yes** | — | — | — | — |
| `validateSystemTags` | No | No | — | — | No | — |
| `alertIds` | — | — | **Yes** | **Yes** | — | — |
| `enabled` | — | — | — | **Yes** | — | — |
| `fromDate` | — | — | — | — | — | No |
| `toDate` | — | — | — | — | — | No |
| `status` | — | — | — | — | — | No |
| `pageNo` | — | — | — | — | — | No |
| `recordsPerPage` | — | — | — | — | — | No |

\* At least one of `email`, `notification`, `slack`, `msteams` and `webhook` must resolve to a stored channel, otherwise `32000001`.

[Get Alerts In Workspace](#1-get-alerts-in-workspace), [Get Alerts In View](#2-get-alerts-in-view), [Get View Metadata For Alert](#3-get-view-metadata-for-alert) and [Get Alert Configuration](#4-get-alert-configuration) take no CONFIG at all.
