---
type: API Endpoint
title: Run Alert
description: Queues an off-schedule evaluation of one alert.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/execute"
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - data-alerts
  - post
  - modeling
api:
  operation_id: runAlert
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/execute"
  domain: schedules-and-alerts
  group: data-alerts
  oauth_scopes:
    - ZohoAnalytics.modeling.create
  org_id_header: required
  config_parameter:
    location: form
    required: false
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the workspace, or a custom-role user with the Manage Data Alerts permission who either has all-alerts access or owns this alert."
  error_codes:
    - 6079
    - 7103
    - 7301
    - 7319
    - 7387
    - 8060
    - 8080
    - 8083
    - 8241
    - 8535
  openapi:
    file: "/references/openapi/schedules-alerts-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1alerts~1{alert-id}~1execute/post"
    config_schema: RunAlertConfig
    response_schema: null
  sdk_examples: "/sdk-examples/schedules-and-alerts/data-alerts/run-alert.md"
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

**POST `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/execute`** - Run Alert (Data Alerts / Schedules & Alerts).

Queues an off-schedule evaluation of one alert. The alert is evaluated against live data and, if its condition is met, **every configured channel delivers for real**. There is no dry-run mode.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `runAlert` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/execute` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the workspace, or a custom-role user with the Manage Data Alerts permission who either has all-alerts access or owns this alert. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - optional |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`schedules-alerts-grouped-api.json`](../../../references/openapi/schedules-alerts-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1alerts~1{alert-id}~1execute/post`; CONFIG schema `RunAlertConfig` |

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
| `{alert-id}` | string | ID of the alert. | [How to obtain](../../../foundations/identifiers.md#alert-id) |

## CONFIG Parameters

CONFIG is **optional** for this API. The only attribute it can carry is `validateSystemTags`.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `validateSystemTags` | Boolean | No | `true` | When `true` (the default) **and** the alert has an e-mail attachment configured, the view's **Data Warning** system tags are checked and the run is refused with `8241` (HTTP 409) if a restricted tag is present. Set it to `false` to run anyway. It has no effect on an alert with no e-mail attachment. |

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`).

# Examples

## Sample Requests

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

## Sample Responses

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

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Run Alert](../../../sdk-examples/schedules-and-alerts/data-alerts/run-alert.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **`204` means queued, not evaluated** | The run is registered as a one-off scheduler task that fires shortly after the call returns — it does **not** execute inline. Poll [Get Alert Events](get-alert-events.md) for the outcome rather than assuming the run has already happened when the response arrives. |
| **`204` never means "the alert fired"** | Whether the condition was met is recorded as an event. A `204` paired with a `notTriggered` event is the normal outcome when the data does not breach the rules. |
| **Not idempotent** | Each call queues another evaluation, and each evaluation that meets the condition notifies again. Repeating the request does not collapse into one run — guard retries. |
| **Notifications are real** | Every configured channel delivers if the condition is met. There is no preview, no send-to-self, and no undo. Treat it as a production action even in testing. |
| **The run executes as the alert's last modifier** | Not as the caller. A caller permitted to run someone else's alert triggers notifications in that alert's own ownership context. |
| **Works on a paused alert** | Pausing with [Change Alert Status](change-alert-status.md) suppresses only the recurring schedule. |
| **The recurring schedule is unaffected** | A manual run does not shift or consume the next scheduled occurrence. |
| **The plan is checked at run time, not at create time** | An organisation whose plan allows zero alert schedules can hold alerts it cannot run (`6079`). |
| **`validateSystemTags` only bites on attachments** | The Data Warning check runs only when the alert's e-mail channel attaches or inlines the report. |
| **Scope is `modeling.create`** | The same scope as [Create Alert](create-alert.md), even though nothing is created. A token scoped only to `modeling.update` can edit and pause an alert but cannot run it. |
| **Dependency chain** | [Get Alerts In Workspace](get-alerts-in-workspace.md) → `alerts[].id` → Run Alert → [Get Alert Events](get-alert-events.md) for the outcome. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [6079](../../../foundations/error-codes.md#error-6079) | 400 | `ALERT_NOTSUPPORTED` — The organisation's plan allows no alert schedules. | Upgrade the plan, or add alert-schedule add-ons. |
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is neither the DB Owner nor a custom-role user permitted to act on this alert, or the request arrived through a custom domain the workspace is not bound to. | Authenticate as the DB Owner, or as the alert's owner with Manage Data Alerts, from the standard API host. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The alert's view does not belong to the workspace in the URL. | Make `<workspace-id>` and `<alert-id>` consistent. |
| [7387](../../../foundations/error-codes.md#error-7387) | 400 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not belong to the organisation in `ZANALYTICS-ORGID`. | Send the organisation id that owns the workspace. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use a domain you have purchased from Zoho Analytics, or the standard API host. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — `CONFIG` was sent but is not a parseable JSON object. | Send a valid, URL-encoded JSON object, or omit `CONFIG` entirely. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | `SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION` — The alert attaches a report from a view carrying a restricted Data Warning tag. HTTP 409. | Resolve the data warning, or resend with `"validateSystemTags": false`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |

# Related

- [Data Alerts overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Schedules & Alerts](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Alerts In Workspace](get-alerts-in-workspace.md), [Get Alerts In View](get-alerts-in-view.md), [Get View Metadata For Alert](get-view-metadata-for-alert.md), [Get Alert Configuration](get-alert-configuration.md), [Create Alert](create-alert.md), [Update Alert](update-alert.md), [Delete Alerts](delete-alerts.md), [Change Alert Status](change-alert-status.md), [Get Alert Events](get-alert-events.md).
- [SDK examples](../../../sdk-examples/schedules-and-alerts/data-alerts/run-alert.md).
