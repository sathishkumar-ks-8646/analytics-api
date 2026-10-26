---
type: API Endpoint
title: Get Alert Configuration
description: "Returns one alert's complete configuration in exactly the CONFIG shape that Create Alert and Update Alert accept, so the response can be edited and posted straight back."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - data-alerts
  - get
  - metadata
api:
  operation_id: getAlertConfiguration
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}"
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
  permission_required: "The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the workspace, or a custom-role user with the Manage Data Alerts permission who either has all-alerts access or owns this alert. The alert must belong to <workspace-id>."
  error_codes:
    - 7103
    - 7301
    - 7319
    - 7387
    - 8060
    - 8083
    - 8535
  openapi:
    file: "/references/openapi/schedules-alerts-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1alerts~1{alert-id}/get"
    config_schema: null
    response_schema: GetAlertConfigurationResponse
  sdk_examples: "/sdk-examples/schedules-and-alerts/data-alerts/get-alert-configuration.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/schedules-alerts-grouped-api.json"
    title: OpenAPI 3 specification - schedules-alerts-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-20T17:34:40Z
generated:
  by: process:build_okf
  at: 2026-10-23T07:58:54Z
status: stable
---

# Summary

**GET `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}`** - Get Alert Configuration (Data Alerts / Schedules & Alerts).

Returns one alert's complete configuration **in exactly the CONFIG shape that [Create Alert](create-alert.md) and [Update Alert](update-alert.md) accept**, so the response can be edited and posted straight back. This is the intended starting point for any edit.

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getAlertConfiguration` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the workspace, or a custom-role user with the Manage Data Alerts permission who either has all-alerts access or owns this alert. The alert must belong to <workspace-id>. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`schedules-alerts-grouped-api.json`](../../../references/openapi/schedules-alerts-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1alerts~1{alert-id}/get`; response schema `GetAlertConfigurationResponse` |

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
| `{alert-id}` | string | ID of the alert. | [How to obtain](../../../foundations/identifiers.md#alert-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

`data` is the alert's complete configuration in CONFIG shape. For the meaning and constraints of every attribute — including the nested channel objects, `scheduleDetails` and `rules[]` — see [CONFIG Parameters of Create Alert](create-alert.md#config-parameters). This table covers the envelope and states which keys are conditional.

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
| `workflows[].id` | String | Workflow id. This is the only field [Update Alert](update-alert.md) reads back. |
| `workflows[].name` | String | Workflow name; `""` when the workflow has none. **Display only** — it is not validated on write. |
| `workflows[].enabled` | Boolean | `true` when the workflow is active. **Display only.** |
| `data.actionsByFlow` | JSONArray | Zoho Flow actions mapped to this alert. **Conditional** — omitted when none are mapped. |
| `actionsByFlow[].actionConfigId` | Number | Flow action configuration id. A genuine JSON **number**, unlike every other id in this family — and [Update Alert](update-alert.md) requires it back as a **string**, so this one field does not round-trip unedited. |
| `actionsByFlow[].actionConfigName` | String | Flow action name. |
| `actionsByFlow[].connectionId` | Number | Id of the connection the action uses. Also a JSON number, with the same conversion caveat. |
| `data.rules` | JSONArray | The alert's rules in `rules[]` shape. **Always present.** Column references come back as `viewColumnIndex`, threshold references as display names (`"T1"`), and date values re-normalised to `yyyy-MM-dd HH:mm:ss`. Anomaly rules carry an `anomaly` object and **no** `viewColumnIndex`. |

# Examples

## Sample Requests

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

## Sample Responses

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

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Alert Configuration](../../../sdk-examples/schedules-and-alerts/data-alerts/get-alert-configuration.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **The response is a ready-to-post request body, with two exceptions** | It is emitted in exactly the CONFIG shape of [Create Alert](create-alert.md) / [Update Alert](update-alert.md) — including the normalised `scheduleDetails` and round-tripped date literals — which makes read-modify-write the intended editing pattern. The exceptions: `actionsByFlow[].actionConfigId` / `connectionId` come back as JSON numbers but must be re-sent as strings, and `conditionExpression` is not validated on the way out. |
| **Absent means absent, not null** | Unconfigured channels, `workflows`, `actionsByFlow`, `rowAxis` and `columnAxis` are **omitted** rather than returned as `null` or `{}`. Test for key presence, not truthiness. `conditionExpression` is the one attribute that uses `""`. |
| **Orphaned column references are dropped silently** | A `rowAxis`, `columnAxis` or `rules[].viewColumnIndex` whose column was deleted after the alert was created is omitted. A round-trip can therefore quietly lose an axis — compare against fresh [Get View Metadata For Alert](get-view-metadata-for-alert.md) output before posting back. |
| **Anomaly rules deliberately omit `viewColumnIndex`** | The write contract forbids it on anomaly rules (`32000046`), so the read contract does not emit it. The column is recovered from `anomaly.name`. |
| **Legacy schedules are understood and upgraded** | Alerts created before the scheduler rework store the time of day as minutes-from-midnight (`570_daily`). That form is parsed correctly here, and re-saving the alert rewrites it in the current form. `32000034` is raised only when the stored value cannot be parsed at all. |
| **`conditionExpression` is not sanitised on read** | It is returned exactly as stored. A legacy alert can carry `"( 1 AND 2 )"` against a single rule; posting that back fails with `32000020`. Check it against `rules.length` yourself. |
| **Channel secrets are decrypted** | `slack.url`, `msteams.url`, `webhook.url`, webhook `params` / `headers` values and the custom `payload` are stored encrypted and returned in clear text to an authorised caller. Treat the response as sensitive. |
| **The alert id is not repeated in the body** | It is only in the URL you called. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get Alerts In Workspace](get-alerts-in-workspace.md) → `alerts[].id` → Get Alert Configuration → edit → [Update Alert](update-alert.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is neither the DB Owner nor a custom-role user permitted to act on this alert, or the request arrived through a custom domain the workspace is not bound to. | Authenticate as the DB Owner, or as the alert's owner with Manage Data Alerts, from the standard API host. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The alert's view does not belong to the workspace in the URL. | Make `<workspace-id>` and `<alert-id>` consistent. |
| [7387](../../../foundations/error-codes.md#error-7387) | 400 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not belong to the organisation in `ZANALYTICS-ORGID`. | Send the organisation id that owns the workspace. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use a domain you have purchased from Zoho Analytics, or the standard API host. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Data Alerts overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Schedules & Alerts](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Alerts In Workspace](get-alerts-in-workspace.md), [Get Alerts In View](get-alerts-in-view.md), [Get View Metadata For Alert](get-view-metadata-for-alert.md), [Create Alert](create-alert.md), [Update Alert](update-alert.md), [Delete Alerts](delete-alerts.md), [Change Alert Status](change-alert-status.md), [Run Alert](run-alert.md), [Get Alert Events](get-alert-events.md).
- [SDK examples](../../../sdk-examples/schedules-and-alerts/data-alerts/get-alert-configuration.md).
