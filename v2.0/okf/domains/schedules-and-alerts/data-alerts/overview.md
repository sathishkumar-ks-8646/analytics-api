---
type: API Group
title: Data Alerts
description: "APIs for creating, listing, updating, running and deleting data alerts on a view, changing their status and reading their event history."
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - data-alerts
  - api-group
api:
  domain: schedules-and-alerts
  group: data-alerts
  endpoint_count: 10
  endpoints:
    - operation_id: getAlertsInWorkspace
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/alerts"
      doc: "/domains/schedules-and-alerts/data-alerts/get-alerts-in-workspace.md"
    - operation_id: getAlertsInView
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts"
      doc: "/domains/schedules-and-alerts/data-alerts/get-alerts-in-view.md"
    - operation_id: getViewMetadataForAlert
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts/metadata"
      doc: "/domains/schedules-and-alerts/data-alerts/get-view-metadata-for-alert.md"
    - operation_id: getAlertConfiguration
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}"
      doc: "/domains/schedules-and-alerts/data-alerts/get-alert-configuration.md"
    - operation_id: createAlert
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts"
      doc: "/domains/schedules-and-alerts/data-alerts/create-alert.md"
    - operation_id: updateAlert
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}"
      doc: "/domains/schedules-and-alerts/data-alerts/update-alert.md"
    - operation_id: deleteAlerts
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/alerts"
      doc: "/domains/schedules-and-alerts/data-alerts/delete-alerts.md"
    - operation_id: changeAlertStatus
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/alerts/status"
      doc: "/domains/schedules-and-alerts/data-alerts/change-alert-status.md"
    - operation_id: runAlert
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/execute"
      doc: "/domains/schedules-and-alerts/data-alerts/run-alert.md"
    - operation_id: getAlertEvents
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/events"
      doc: "/domains/schedules-and-alerts/data-alerts/get-alert-events.md"
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

This document covers the V2 **Data Alert** REST APIs of Zoho Analytics — the APIs that discover what a report can be alerted on, create and edit alerts, enable/pause and delete them, run one on demand, and read the audit trail of every evaluation.

APIs for creating, listing, updating, running and deleting data alerts on a view, changing their status and reading their event history.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Alerts In Workspace](get-alerts-in-workspace.md) | GET | `/restapi/v2/workspaces/{workspace-id}/alerts` | `getAlertsInWorkspace` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Alerts In View](get-alerts-in-view.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts` | `getAlertsInView` | `ZohoAnalytics.metadata.read` | 200 |
| [Get View Metadata For Alert](get-view-metadata-for-alert.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts/metadata` | `getViewMetadataForAlert` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Alert Configuration](get-alert-configuration.md) | GET | `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}` | `getAlertConfiguration` | `ZohoAnalytics.metadata.read` | 200 |
| [Create Alert](create-alert.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts` | `createAlert` | `ZohoAnalytics.modeling.create` | 200 |
| [Update Alert](update-alert.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}` | `updateAlert` | `ZohoAnalytics.modeling.update` | 204 |
| [Delete Alerts](delete-alerts.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/alerts` | `deleteAlerts` | `ZohoAnalytics.modeling.delete` | 204 |
| [Change Alert Status](change-alert-status.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/alerts/status` | `changeAlertStatus` | `ZohoAnalytics.modeling.update` | 204 |
| [Run Alert](run-alert.md) | POST | `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/execute` | `runAlert` | `ZohoAnalytics.modeling.create` | 204 |
| [Get Alert Events](get-alert-events.md) | GET | `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/events` | `getAlertEvents` | `ZohoAnalytics.metadata.read` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is a "Data Alert" in Zoho Analytics?

A **data alert** is a named, scheduled rule attached to a single report. On every scheduled evaluation the server re-reads the report, tests the alert's rules against it, and — when the boolean combination of those rules is true — delivers a notification through every channel configured on the alert. Alerts exist only on **Chart (analysis view)**, **Pivot Table** and **Summary View** reports; any other view type is refused with [`8245`](../../../foundations/error-codes.md#error-8245).

| Part | CONFIG attribute(s) | Notes |
|------|--------------------|-------|
| **What is watched** | `rules`, `conditionExpression`, `summaryType`, `rowAxis`, `columnAxis` | Up to 10 rules over the report's columns, combined by a boolean expression. `summaryType` selects the data slice — raw rows, sub totals, or the grand total. |
| **When it is evaluated** | `scheduleDetails` | Frequency, interval, time of day, and the day/week/month selectors that apply to that frequency. The view it watches is fixed at creation and cannot be changed. |
| **Who hears about it** | `email`, `notification`, `slack`, `msteams`, `webhook` | At least one channel must resolve to a real recipient or endpoint (`32000001`). |
| **What else it triggers** | `workflows`, `actionsByFlow` | Zoho Flow mappings. Both are **rejected by Create Alert** (`32000049`) and can only be re-asserted through Update Alert. |
| **How it reads** | `alertName`, `notifyOnChange` | The name is unique within the view (`32000011`); `notifyOnChange` suppresses repeat notifications while the condition stays true. |

> **The single most important behaviour:** every column in a rule is addressed by `viewColumnIndex`, a **positional** index that is valid only for the report's current shape. See [The viewColumnIndex Contract](overview.md#the-viewcolumnindex-contract) before building any rule, and re-read [Get View Metadata For Alert](get-view-metadata-for-alert.md) after the report is edited.

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`). The five read APIs use the **`metadata`** scope family; the five write APIs use the **`modeling`** scope family — see [OAuth scopes](../../../foundations/oauth-scopes.md).
> - All ten APIs are **workspace-scoped** (`/restapi/v2/workspaces/<workspace-id>/...`) and require the `ZANALYTICS-ORGID` header. A missing header is [`8083`](../../../foundations/error-codes.md#error-8083); a header that does not own the workspace is [`7387`](../../../foundations/error-codes.md#error-7387).
> - `ZohoAnalytics_Server_URI` depends on the data centre (`analyticsapi.zoho.com`, `.eu`, `.in`, `.com.au`, `.jp`, …).
> - These APIs are **not blocked** on a Client Portal / White Label domain — unlike the [Email Schedule APIs](../email-schedules/overview.md#white-label--client-portal-behaviour). Instead a domain-binding check runs; see [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour).
> - Alerts can only be configured on `AnalysisView` (Chart), `Pivot` and `SummaryView` reports. Any other view type is refused with [`8245`](../../../foundations/error-codes.md#error-8245) before permissions or payload are considered.
> - None of these APIs accepts a `criteria` attribute, and none of them reads or writes table rows — no API here uses the `data` scope family.
> - Every numeric identifier is carried as a JSON **string**, in both directions. Sending `"viewColumnIndex": 2` instead of `"viewColumnIndex": "2"` fails with [`8080`](../../../foundations/error-codes.md#error-8080).

---

# How the Ten APIs Fit Together

The ten APIs split into **discovery** (what can I alert on, and what alerts exist), **write** (create / change / remove) and **operations** (run it now, inspect what it did). Every write API consumes an id produced by a discovery API.

| Step | What it produces | What consumes it |
|------|------------------|------------------|
| [Get View List](../../views-management/view-operations/get-views.md) | `<view-id>` of a Chart / Pivot / Summary report | [Get Alerts In View](get-alerts-in-view.md), [Get View Metadata For Alert](get-view-metadata-for-alert.md), [Create Alert](create-alert.md) |
| [Get View Metadata For Alert](get-view-metadata-for-alert.md) | `viewColumnIndex` values plus the operators, rule types, thresholds and anomalies each column permits | `rules[]`, `rowAxis` and `columnAxis` of [Create Alert](create-alert.md) / [Update Alert](update-alert.md) |
| [Create Alert](create-alert.md) | `data.alertId` | every alert-id-addressed API below |
| [Get Alerts In Workspace](get-alerts-in-workspace.md) / [Get Alerts In View](get-alerts-in-view.md) | `alerts[].id` of existing alerts | every alert-id-addressed API below |
| [Get Alert Configuration](get-alert-configuration.md) | the alert's complete CONFIG, including `workflows` and `actionsByFlow` ids | [Update Alert](update-alert.md) — edit the returned JSON and post it back |
| [Run Alert](run-alert.md) | one off-schedule evaluation | [Get Alert Events](get-alert-events.md) records its outcome |

The read-modify-write loop is the intended editing pattern: [Get Alert Configuration](get-alert-configuration.md) emits exactly the CONFIG shape [Update Alert](update-alert.md) accepts, so the response can be edited and posted straight back.

---

# The viewColumnIndex Contract

**The Alert APIs never expose or accept an internal column id. Every column reference is a `viewColumnIndex` — a positional index over the report's current column layout.**

| Where it appears | Meaning |
|---|---|
| `rules[].viewColumnIndex` | The column the rule tests. **Forbidden on anomaly rules** (`32000046`) — the column is derived from `anomaly.name` instead. |
| `rules[].values[0]` when `type` is `column` | The *other* NUMBER column being compared against. |
| `rowAxis` / `columnAxis` | The pivot/summary axis the alert's sub totals are computed over. |
| `viewColumns[].viewColumnIndex` and `anomalies[].viewColumnIndex` (responses) | The values you are allowed to send. |

The rule the server applies is: **the index is resolved against the report's live column layout at the moment of the call.** Practical consequences:

1. **A stale index is not always an error.** If the report has been edited and the index still resolves, it resolves to a *different* column and the alert silently watches the wrong data. If it no longer resolves, the call fails with `32000041` (`RULE_VIEW_COLUMN_INDEX_OUT_OF_BOUNDS`) or `32000029` (`INVALID_AXIS_VIEW_COLUMN`) for an axis.
2. **Re-fetch [Get View Metadata For Alert](get-view-metadata-for-alert.md) before every write.** Caching the metadata for the duration of one build-a-rule workflow is fine; caching it across report edits is not.
3. **Indexes are JSON strings.** `"viewColumnIndex": "2"`, not `"viewColumnIndex": 2`. The server reads them with a string accessor; a bare numeric literal fails with [`8080`](../../../foundations/error-codes.md#error-8080) `INVALID_JSON_CONFIGURATION`.
4. **[Get Alert Configuration](get-alert-configuration.md) drops orphaned references silently.** A `rowAxis`, `columnAxis` or `rules[].viewColumnIndex` whose column no longer exists is **omitted** from the response rather than returned as a dangling index — so a naive read-modify-write can quietly lose an axis that had become invalid.

---

# Limitations

These are the limits that apply with **default settings**.

| Limitation | Value | Enforced by |
|------------|-------|-------------|
| **Rules per alert** | **1–10.** Counted across the whole `rules` array, anomaly rules included. | `32000018` (too many), `32000006` (none) |
| **E-mail recipients per alert** | **25** entries in `email.emailIds`. The request template accepts up to 1,000, but the server refuses anything above 25. | `32000007` |
| **Group recipients per alert** | **1–1000** entries in `email.groupIds`. | Request template |
| **Values per rule** | **1–300** entries in `rules[].values`. | Request template |
| **Webhook `params` / `headers`** | **0–10** entries each. | Request template |
| **`alertIds` per request** | **0–1000** entries on [Delete Alerts](delete-alerts.md) and [Change Alert Status](change-alert-status.md). An empty array is accepted and is a no-op. | Request template |
| **Alert name length** | **100** characters, unique within the view. | `32000011` |
| **`conditionExpression` length** | **1,000** characters. | Request template |
| **Alert event page size** | **1–100** records. A larger `recordsPerPage` is **silently clamped** to 100. | — |
| **Alert event retention** | **45 days**, inclusive of today. Older events are purged, not filtered. | — |
| **Alert schedules per organisation** | Plan-dependent. An organisation whose plan allows **zero** alert schedules cannot run an alert at all. | `6079` |

> **The e-mail recipient limit is the one that surprises people.** The `alertEmailTemplate_v2API` request template declares `emailIds` as a 1–1000 array, so a 200-address payload passes schema validation and is then rejected by the business layer with `32000007`. Keep explicit recipient lists at or below 25 addresses and use `groupIds` or `notifyAdmins` for wider distribution.

---

# Permission Model

Two different checks apply, and which one you get depends on how the API addresses its target.

| Role | May do | Notes |
|------|--------|-------|
| Account Admin / Organization Admin / Workspace Admin (DB Owner) | Everything in this document, on every alert in the workspace. | The DB Owner check short-circuits every other test. |
| Custom role with **Manage Data Alerts** (`CREATEALERT`) **and** all-alerts access | Everything, on every alert in the workspace. | Equivalent to DB Owner for these APIs. |
| Custom role with **Manage Data Alerts** but **without** all-alerts access | Create alerts on any view they hold `CREATEALERT` on; list every alert of the workspace; but read, edit, run, pause or delete **only alerts they own**. | Acting on somebody else's alert fails with `7301`. |
| Any other user | Nothing. | `7301`. |

| Addressing style | APIs | Check performed |
|---|---|---|
| Workspace | [Get Alerts In Workspace](get-alerts-in-workspace.md) | The alert permission **on the workspace**. The check is workspace-wide, so the returned list can include alerts on views the caller could not configure individually. |
| View | [Get Alerts In View](get-alerts-in-view.md), [Get View Metadata For Alert](get-view-metadata-for-alert.md), [Create Alert](create-alert.md) | DB Owner of the view's workspace, **or** `CREATEALERT` on that view. The view must also belong to `<workspace-id>` (`7319` otherwise). |
| Alert id | [Get Alert Configuration](get-alert-configuration.md), [Update Alert](update-alert.md), [Delete Alerts](delete-alerts.md), [Change Alert Status](change-alert-status.md), [Run Alert](run-alert.md), [Get Alert Events](get-alert-events.md) | DB Owner, **or** a custom-role user with Manage Data Alerts who either has all-alerts access or owns that specific alert. Evaluated **per id** on the two list-taking APIs. |

Two consequences worth stating plainly:

- **`CREATEALERT` on the view gates creation; alert ownership gates everything afterwards.** Losing view permission does not retract control of an alert already created, and gaining it does not grant control of someone else's.
- **Every alert-id-addressed API also verifies that the alert belongs to the workspace in the URL.** A mismatched pair is [`7319`](../../../foundations/error-codes.md#error-7319), and a deleted or non-existent alert is `32000009` — so an id from another workspace is never actionable, even for an Account Admin.

---

# White Label / Client Portal Behaviour

Unlike the [Email Schedule APIs](../email-schedules/overview.md#white-label--client-portal-behaviour), which are disabled outright on custom domains, the Alert APIs run a **domain-binding check**.

| Scenario | Result |
|----------|--------|
| Request sent to the **standard** API host (`analyticsapi.zoho.*`) | **Allowed**, whether or not the workspace is white-labelled. |
| Request sent **through a custom domain**, and the target workspace is bound to that same domain | **Allowed.** |
| Request sent **through a custom domain**, and the target workspace is bound to a different domain or to none | **Rejected with `7301`** before any business logic runs. |

There is no `domainName` CONFIG attribute on any of these APIs. If in doubt, call the standard host.

---

# API-Specific Notes and Behaviours

## Get Alerts In Workspace

- **Workspace-wide permission, not per view.** A single alert permission on the workspace lists every alert in it, including alerts on views the caller could not configure. Acting on those alerts is a separate, stricter check.
- **Timestamps are in the caller's time zone, not the alert's.** Two users see different wall-clock values for the same `nextScheduleTime`; the alert's own `scheduleDetails.timeZone` is not what renders this response.
- **`lastRunStatus` is localised prose.** `"Condition met"` / `"Condition unmet"` change with the caller's language. The stable equivalent is `alertEvents[].status` from [Get Alert Events](get-alert-events.md).
- **Missing values are `""`, never `null`.** A never-run alert has three empty timestamp fields; a paused alert has four.
- **No paging, no filter, no sort.** The entire alert list comes back in one response — filter client-side.
- **Owner e-mail is best-effort.** `createdBy` and `lastModifiedBy` come from a remote identity lookup; a failure yields `""` rather than failing the call.
- **Dependency chain:** [Get Workspace List](../../workspace-management/workspace-operations/overview.md) → Get Alerts In Workspace → `alerts[].id` for every alert-id-addressed API here.

## Get Alerts In View

- **Same payload, stricter gate.** Entries are byte-identical in shape to the workspace listing, but the caller must be the DB Owner or hold `CREATEALERT` on that specific view.
- **The view/workspace pair is validated.** A mismatched pair is [`7319`](../../../foundations/error-codes.md#error-7319), not an empty list.
- **It does not check the view type.** An unsupported report has no alerts and returns `[]` like any other. Use [Get View Metadata For Alert](get-view-metadata-for-alert.md), which fails with [`8245`](../../../foundations/error-codes.md#error-8245), to test alert capability.
- **Dependency chain:** [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>` → Get Alerts In View → `alerts[].id`.

## Get View Metadata For Alert

- **The only source of `viewColumnIndex`.** The Alert APIs neither accept nor return internal column ids, so no rule can be built correctly without this call.
- **`viewColumnIndex` is positional and changes when the report changes.** Cache it for one build-a-rule workflow, never across report edits — a stale index either resolves to a different column or fails with `32000041`.
- **`allowedOperators` and `allowedRuleTypes` are the authoritative allow-lists.** They are computed per column from its add-on type, data type, aggregation and geo role — fields that are not all present in the response, so never derive them yourself. Sending anything outside them is [`8119`](../../../foundations/error-codes.md#error-8119).
- **`thresholds` doubles as the feature switch for threshold rules.** An empty array is exactly why `threshold` is missing from that column's `allowedRuleTypes`.
- **`allowedAnomalyOperators` is view-level, not column-level.** It is derived from the X axis's date bucket: `YEAR` yields the yearly tokens, `ABSMONTH` the monthly ones, `DATE` / `TIMESTAMP` the full day-level set. With anomalies but no date-bucketed X axis it degrades to `["sinceLastAlert"]`; with no anomalies at all it is `[]`.
- **`anomalies` is hoisted to the top level.** The underlying payload repeats it on every column; do not look for it inside `viewColumns[]`.
- **`viewType` returns internal tokens.** `AnalysisView`, `Pivot`, `SummaryView` — not the UI labels "Chart View", "Pivot View", "Summary View".
- **It reads structure, not data.** No rows are scanned, so calling it before every write costs nothing.
- **Dependency chain:** [Get View List](../../views-management/view-operations/get-views.md) → Get View Metadata For Alert → `viewColumnIndex` / `thresholds` / `anomalyName` → [Create Alert](create-alert.md).

## Get Alert Configuration

- **The response is a ready-to-post request body, with two caveats.** It is emitted in exactly the CONFIG shape of [Create Alert](create-alert.md) / [Update Alert](update-alert.md), which makes read-modify-write the intended editing pattern — but `actionsByFlow[].actionConfigId` / `connectionId` come back as JSON numbers and must be converted to strings before posting back, and `conditionExpression` is returned unvalidated.
- **`scheduleDetails` is normalised on the way out.** Whatever was stored, the response uses array-valued `weekDays` / `monthDays` / `months`, an explicit 1-based `interval`, and includes `skipWeekends` only for `hourly` and `daily` — so it satisfies the strict applicability check (`32000052`) when posted straight back.
- **Legacy schedules are read and upgraded.** A stored minutes-from-midnight schedule (`570_daily`) is parsed correctly, and re-saving the alert rewrites it in the current form. `32000034` appears only when the stored value cannot be parsed at all.
- **Orphaned references are dropped silently.** `rowAxis`, `columnAxis` and `rules[].viewColumnIndex` are omitted when the referenced column no longer exists, so a round trip can quietly lose an axis.
- **`conditionExpression` is *not* sanitised.** It is returned exactly as stored, so a legacy alert can hand you an expression that references more rules than exist. Validate it against `rules.length` before posting it back, or the write fails with `32000020`.
- **Absent means absent.** Unconfigured channels, `workflows`, `actionsByFlow` and the axes are omitted rather than returned as `null` or `{}`. Test for key presence. `conditionExpression` is the lone attribute that uses `""`.
- **`isAnomaly` is read-only.** It is derived from `rules[]` on write and overwritten whatever you send.
- **Channel secrets are returned in clear text.** Webhook and messaging URLs, header and parameter values, and custom payloads are decrypted for an authorised caller. Treat the response as sensitive.
- **Dependency chain:** [Get Alerts In Workspace](get-alerts-in-workspace.md) → `alerts[].id` → Get Alert Configuration → edit → [Update Alert](update-alert.md).

## Create Alert

- **Every reference is validated against the live view, not merely parsed.** Column indexes must resolve (`32000041`), threshold names must exist on that column (`32000038`), anomaly names must exist on the view (`32000042`), and cross-column rules must point at a NUMBER column of the same view (`32000036` / `32000037`).
- **At least one notification channel is mandatory.** An alert with rules but no channel would evaluate and tell nobody, so it is refused (`32000001`) — and a channel that resolves to no recipient is discarded before that check runs (`32000013`), which is how a request carrying an `email` object can still fail with `32000001`.
- **The e-mail recipient ceiling is 25, not 1000.** The request template permits 1,000 entries and the business layer then rejects anything above 25 with `32000007`. Use `groupIds` or `notifyAdmins` for wider distribution.
- **Anomaly rules are all-or-nothing.** Either every entry in `rules[]` carries an `anomaly` object or none does (`32000017`), anomaly rules must not carry `viewColumnIndex` (`32000046`), and anomaly and `threshold` rule types are Chart-only (`32000019`).
- **`workflows` and `actionsByFlow` are rejected here** (`32000049`). Both refer to mappings that cannot exist before the alert does, so they belong to [Update Alert](update-alert.md).
- **`conditionExpression` defaults only for a single rule.** With more than one rule and no expression the request fails with [`8079`](../../../foundations/error-codes.md#error-8079) rather than defaulting to `(1)`.
- **`isAnomaly` is ignored on input.** It is derived from the rules so that a [Get Alert Configuration](get-alert-configuration.md) response can be posted back unchanged.
- **The alert is created live.** Its schedule registers immediately, so an evaluation can happen before you have read the configuration back.
- **The response carries only `alertId`.** Nothing is echoed; call [Get Alert Configuration](get-alert-configuration.md) to see how the input was normalised.
- **Plan limits are not checked here.** An alert can be created on an organisation plan that will refuse to run it ([`6079`](../../../foundations/error-codes.md#error-6079) at [Run Alert](run-alert.md)).
- **Dependency chain:** [Get View List](../../views-management/view-operations/get-views.md) → [Get View Metadata For Alert](get-view-metadata-for-alert.md) → Create Alert → `data.alertId`.

## Update Alert

- **It is a full replace, not a patch.** The CONFIG you send becomes the alert; attributes you leave out are not preserved. Omitting a channel removes it, and omitting `notifyOnChange` resets it to `false`. Start from [Get Alert Configuration](get-alert-configuration.md) output.
- **The alert id never changes.** Unlike [Update Email Schedule](../email-schedules/update-email-schedule.md), which can mint a new id when the name or period changes, an alert keeps its identity across every update.
- **The view is immutable.** There is no `<view-id>` in the URL and no CONFIG attribute for it. Moving an alert means deleting and recreating it, which resets its event history.
- **It is the only API that accepts `workflows` and `actionsByFlow`,** and both only *re-assert* mappings that already exist — unmapped workflow ids fail with `32000043` and unmapped Flow action ids with `32000050`, each listing every offending id in one message.
- **`workflows` is validated by `id` alone.** `name` and `enabled` are display fields, are not part of the write contract, and are not compared against the stored mapping — so an unedited [Get Alert Configuration](get-alert-configuration.md) response posts back cleanly.
- **Everything Create Alert validates is validated again**, since both share one conversion path.
- **Permission is ownership-based.** A custom-role user without all-alerts access can update only their own alerts, even on a view they may create alerts on.
- **Success is `204` with an empty body**, so the only way to confirm what was stored is to read it back.
- **Dependency chain:** [Get Alert Configuration](get-alert-configuration.md) → edit → Update Alert → [Get Alert Configuration](get-alert-configuration.md) to verify.

## Delete Alerts

- **It takes a list, and the list is validated up front.** Every id is checked for workspace membership and caller permission *before* anything is deleted, so one bad id fails the whole call and nothing is removed.
- **`alertIds` entries must be JSON strings.** Numeric literals are rejected.
- **An empty array is accepted and does nothing**, answering `204`.
- **Nothing is reported per id**, so "deleted" and "already absent" are indistinguishable from the response alone.
- **It is a status change under the hood, not a purge.** The alert stops evaluating, disappears from the listing APIs, and its id stops being actionable (`32000009`). There is no trash and no restore.
- **Not the way to silence an alert temporarily** — [Change Alert Status](change-alert-status.md) is reversible and keeps the event history.
- **Dependency chain:** [Get Alerts In Workspace](get-alerts-in-workspace.md) → Delete Alerts.

## Change Alert Status

- **One request sets one state for many alerts.** `enabled` applies to every id; to enable some and pause others, send two requests.
- **Same up-front validation as Delete Alerts.** All ids are checked before any status changes.
- **Idempotent.** Setting an alert to the state it already has is not an error and still answers `204`.
- **Pausing stops the schedule, not the history.** `nextScheduleTime` becomes `""` while `lastRunTime`, `lastAlertSentTime` and everything in [Get Alert Events](get-alert-events.md) survive.
- **A paused alert can still be run on demand** with [Run Alert](run-alert.md) — pausing suppresses the schedule, not manual evaluation.
- **Its scope is `modeling.update`,** matching the HTTP method rather than the much narrower effect.
- **Dependency chain:** [Get Alerts In Workspace](get-alerts-in-workspace.md) (read `enabled`) → Change Alert Status → verify.

## Run Alert

- **`204` means "queued", not "evaluated" and certainly not "fired".** The run is registered as a one-off scheduler task that fires shortly after the response, so do not assume the evaluation has completed when the call returns. Read the newest entry from [Get Alert Events](get-alert-events.md) for the outcome.
- **Notifications are really sent.** This is not a dry run: if the condition is met, every configured channel delivers. There is no preview mode.
- **The evaluation executes as the alert's last modifier**, not as the caller, so notifications are attributed to that alert's own ownership context.
- **`validateSystemTags` defaults to `true`** and bites only when the alert attaches the report to an e-mail — it then checks the view's Data Warning system tags and refuses with [`8241`](../../../foundations/error-codes.md#error-8241) (HTTP 409) rather than mailing a report flagged as unreliable.
- **The organisation plan is checked at run time.** An organisation whose plan allows zero alert schedules is refused with [`6079`](../../../foundations/error-codes.md#error-6079) even though the alert exists.
- **`CONFIG` is optional here** — the only attribute it can carry is `validateSystemTags`.
- **Its scope is `modeling.create`,** the same as [Create Alert](create-alert.md).
- **Dependency chain:** [Get Alerts In Workspace](get-alerts-in-workspace.md) → Run Alert → [Get Alert Events](get-alert-events.md).

## Get Alert Events

- **The audit trail, and the only machine-readable outcome.** `status` is one of `triggered`, `notTriggered`, `error` and is **not** localised — unlike `lastRunStatus` of the listing APIs.
- **Events are returned oldest first.** The newest evaluation is the last entry on the last page; `alertEvents[0]` is the *oldest* match, not the most recent.
- **The response is always paginated**, whether or not the caller asks: `pageDetails` is always present, `recordsPerPage` is clamped to 100, and more data is signalled by `hasNextPage` rather than by a full page. Loop on `hasNextPage`, not on page length.
- **`alertTime` is epoch milliseconds in a string**, deliberately unformatted so callers can render it in their own locale and time zone.
- **`errorCode` on an event is a symbolic name** (e.g. `INCOMPATIBLE_DATE_VALUE`), not one of the numeric codes in the Error Codes tables, and appears only when `status` is `error`.
- **History is retained for 45 days inclusive of today.** Older events are deleted, not filtered, so a wider `fromDate` cannot recover them.
- **An empty `alertEvents` array is a success.** It means the filters matched nothing, which is also what a brand-new alert returns.
- **`feed` (snapshot file id) and `contentType` exist internally but are intentionally not exposed** — do not build on them appearing later.
- **Dependency chain:** [Get Alerts In Workspace](get-alerts-in-workspace.md) → `alerts[].id` → Get Alert Events.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Four of ten APIs return 204 with no body** | [Update Alert](update-alert.md), [Delete Alerts](delete-alerts.md), [Change Alert Status](change-alert-status.md) and [Run Alert](run-alert.md) return HTTP **204 No Content** on success — treat the status code as the success indicator and never expect or parse a JSON body. The other six return the standard `{"status", "summary", "data"}` envelope with HTTP 200. |
| **Nothing is echoed by the write APIs** | [Create Alert](create-alert.md) returns only the new `alertId`; update, delete, status and run return nothing at all. The authoritative post-write state always comes from a follow-up read. |
| **Failure responses always carry a body** | Even for the 204 APIs, errors return `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. On failure `summary` is the error's **symbolic name** (e.g. `ALERT_DELETED`, `SUBFLOW_ID_NOT_MAPPED_TO_ALERT`), not a localised sentence; the sentence is in `data.errorMessage`. |
| **`summary` on success is a localised label** | `"Get alerts in workspace"`, `"Create alert"`, `"Get alert configuration"`, … It changes with the caller's language, so never branch on it. |
| **All IDs are strings — and must be sent back as strings** | `alerts[].id`, `data.alertId`, `viewId`, `viewColumnIndex`, `workflows[].id`, `groupIds[]` and every `alertIds[]` entry are JSON **strings** even though the values are numeric. Parse them as strings or longs, never as native JSON numbers, to avoid precision loss. Sending a bare numeric literal where a string is expected is `8080`. |
| **Two exceptions are genuine JSON numbers** | `actionsByFlow[].actionConfigId` and `actionsByFlow[].connectionId` come back as numbers, as do `pageDetails.pageNo` and `pageDetails.recordsPerPage`. `enabled`, `hasNextPage`, `isAnomaly` and `notifyOnChange` are native booleans. The `actionsByFlow` pair is the one place where the read and write contracts disagree: [Update Alert](update-alert.md) requires both back as **strings** — see [`actionsByFlow` Fields](update-alert.md#actionsbyflow-fields). |
| **Timestamps come in two flavours** | The listing APIs use **ISO-8601 with offset** in the caller's profile time zone (`2026-03-20T10:00:00+05:30`); [Get Alert Events](get-alert-events.md) uses **epoch milliseconds as a string** (`"1779226560981"`). No API returns a formatted local date string. |
| **Empty string, not `null`, for absent timestamps** | `lastRunTime`, `lastAlertSentTime`, `lastRunStatus` and `nextScheduleTime` are `""` when they do not apply. No Alert API returns JSON `null`. |
| **Optional objects are omitted, not emptied** | [Get Alert Configuration](get-alert-configuration.md) leaves out unconfigured channels, `workflows`, `actionsByFlow`, `rowAxis`, `columnAxis`, and empty `emailIds` / `groupIds` / `params` / `headers` entirely. Test for key presence rather than truthiness. `conditionExpression` is the one attribute that uses `""` instead. |
| **Arrays that are always present** | `data.alerts` (both listing APIs), `data.viewColumns` / `data.anomalies` / `data.allowedAnomalyOperators` ([Get View Metadata For Alert](get-view-metadata-for-alert.md)), `data.rules` ([Get Alert Configuration](get-alert-configuration.md)), and `data.alertEvents` + `data.pageDetails` ([Get Alert Events](get-alert-events.md)) are always returned, empty when there is nothing to report. |
| **An empty collection is a success** | An empty `alerts`, `anomalies` or `alertEvents` array comes back with HTTP 200. Never infer failure from emptiness. |
| **Only Get Alert Events paginates** | Every other API returns its full result set in one response; there is no `pageDetails` block anywhere else, and no sort or filter parameters either. |
| **Enums versus labels** | Machine-readable enums: `alertEvents[].status`, `summaryType`, `calendarFrequency`, `rules[].type`, `messageType`, `attachmentType`, `viewType`. Localised labels that must not be parsed: the success `summary`, `alerts[].lastRunStatus`, and `data.errorMessage`. |
| **Responses are extensible** | Some builds return additional fields. Ignore unrecognised keys rather than validating against a closed schema. |
| **`32000xxx` codes are alert-specific** | Every code in the `32000001`–`32000053` range is raised only by the alert subsystem. The `6xxx` / `7xxx` / `8xxx` codes are shared across API families, so match on the `summary` symbolic name as well as `errorCode` when handling errors generically. |

---

# Enum and Value Reference

### `rules[].operator` Values

Always restrict your choice to the column's `allowedOperators` array from [Get View Metadata For Alert](get-view-metadata-for-alert.md). The tables below explain what each token means and how many entries `values` must carry.

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

### Which operators each column kind offers

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

### Date and Time Value Format

For `DATE` / `TIMESTAMP` columns the scalar operators (`is`, `isnot`, `gt`, `lt`, `gte`, `lte`, `btw`, `notbtw`) accept:

- `yyyy-MM-dd HH:mm:ss` — e.g. `2026-01-12 10:00:00`
- `yyyy-MM-dd` — e.g. `2026-01-12`, with the time defaulting to `00:00:00`

Anything else is `32000028`. The same two formats apply to `fromDate` / `toDate` of [Get Alert Events](get-alert-events.md), where a date-only `toDate` is expanded to `23:59:59.999` instead. Date-bucket operators take no value at all.

### Alert Event Statuses

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `triggered` | The rules matched and the configured channels were notified. | — |
| `notTriggered` | The alert was evaluated and the rules did not match. Also the fallback for any unrecognised stored outcome. | — |
| `error` | The evaluation itself failed. The event carries `errorCode` and `message`. | — |

Accepted in the `status` filter of [Get Alert Events](get-alert-events.md) as 1–3 distinct entries; anything else is [`8119`](../../../foundations/error-codes.md#error-8119).

### Day and Month Numbering

| Field | Numbering |
|-------|-----------|
| `weekDays`, `dayOfWeek` | **1 = Sunday … 7 = Saturday.** |
| `monthDays` | **1–31**, or the single-entry list `[99]` meaning "last day of the month". |
| `weekOfMonth` | **1 = first … 4 = fourth, 5 = last.** |
| `months` | **1 = January … 12 = December.** |

---

# CONFIG Attribute Availability by API

Only five APIs accept CONFIG. `✔` means the attribute is accepted; `—` means it is not part of that API's contract.

| Attribute | [Create Alert](create-alert.md) | [Update Alert](update-alert.md) | [Delete Alerts](delete-alerts.md) | [Change Alert Status](change-alert-status.md) | [Run Alert](run-alert.md) | [Get Alert Events](get-alert-events.md) |
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

[Get Alerts In Workspace](get-alerts-in-workspace.md), [Get Alerts In View](get-alerts-in-view.md), [Get View Metadata For Alert](get-view-metadata-for-alert.md) and [Get Alert Configuration](get-alert-configuration.md) take no CONFIG at all.

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [6079](../../../foundations/error-codes.md#error-6079) | 400 | ALERT_NOTSUPPORTED - The organisation's plan allows no alert schedules. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7387](../../../foundations/error-codes.md#error-7387) | 400 | DBID_NOT_BELONGS_TO_ZSOID - The workspace does not belong to the organisation in ZANALYTICS-ORGID. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | DOMAIN_NOT_EXIST - The custom domain in the request host is not provisioned. |
| [8078](../../../foundations/error-codes.md#error-8078) | 400 | EMPTYJSONATTRIBUTEFOUND — A mandatory attribute was sent blank. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION - scope is missing from CONFIG. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | CONFIG is not valid JSON, was not URL-encoded correctly, contains an unsupported key, or violates a type or length constraint. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | The ZANALYTICS-ORGID header is missing from a request that requires it. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | INVALIDVALUEFORATTRIBUTE — fileType, onError, delimiter, quoted, thousandSeparator, or decimalSeparator is outside its permitted set. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | SYSTEMTAGDATAWARNINGV2VALIDATIONCONFIRMATION — The view carries a restricted DATAWARNING system tag. |
| [8245](../../../foundations/error-codes.md#error-8245) | 404 | BACKUP_NOT_FOUND - The backup does not exist, or does not belong to this workspace. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | LESSTHANMINOCCURANCE — CONFIG was not sent. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |

# Related

- [Schedules & Alerts](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
