---
type: API Endpoint
title: Change Alert Status
description: Enables (resumes) or pauses one or more alerts without altering their configuration.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/alerts/status"
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - data-alerts
  - put
  - modeling
api:
  operation_id: changeAlertStatus
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/alerts/status"
  domain: schedules-and-alerts
  group: data-alerts
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the workspace, or a custom-role user with the Manage Data Alerts permission who either has all-alerts access or owns every alert listed. The check runs per id."
  error_codes:
    - 7103
    - 7301
    - 7319
    - 7387
    - 8060
    - 8078
    - 8079
    - 8080
    - 8083
    - 8504
    - 8535
  openapi:
    file: "/references/openapi/schedules-alerts-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1alerts~1status/put"
    config_schema: ChangeAlertStatusConfig
    response_schema: null
  sdk_examples: "/sdk-examples/schedules-and-alerts/data-alerts/change-alert-status.md"
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

**PUT `/restapi/v2/workspaces/{workspace-id}/alerts/status`** - Change Alert Status (Data Alerts / Schedules & Alerts).

Enables (resumes) or pauses one or more alerts without altering their configuration. One request sets **one** state for every id it lists.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `changeAlertStatus` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/alerts/status` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the workspace, or a custom-role user with the Manage Data Alerts permission who either has all-alerts access or owns every alert listed. The check runs per id. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`schedules-alerts-grouped-api.json`](../../../references/openapi/schedules-alerts-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1alerts~1status/put`; CONFIG schema `ChangeAlertStatusConfig` |

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

## CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `alertIds` | JSONArray of String | **Yes** | — | Alert ids whose status changes, as numeric **strings**. **0–1000 entries**; an empty array is accepted and changes nothing. Every id must belong to `<workspace-id>` and must still exist. |
| `enabled` | Boolean | **Yes** | — | The state applied to **every** id in `alertIds`: `true` makes the alert live, `false` pauses it. There is no per-id state — to enable some and pause others, send two requests. |

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`).

# Examples

## Sample Requests

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

## Sample Responses

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

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Change Alert Status](../../../sdk-examples/schedules-and-alerts/data-alerts/change-alert-status.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **One state for the whole list** | `enabled` applies to every id in `alertIds`. There is no per-id payload. |
| **Idempotent** | Setting an alert to the state it is already in is not an error and still answers `204`. |
| **Same up-front validation as Delete Alerts** | Every id is checked for workspace membership and caller permission before any status changes, so one bad id fails the whole request. |
| **Pausing stops the schedule, not the history** | `nextScheduleTime` becomes `""` in the listing APIs, while `lastRunTime`, `lastAlertSentTime` and everything in [Get Alert Events](get-alert-events.md) is retained. |
| **A paused alert can still be run on demand** | [Run Alert](run-alert.md) works on a paused alert — pausing suppresses the *schedule*, not manual evaluation. |
| **Reversible, unlike Delete** | This is the correct way to silence an alert temporarily; [Delete Alerts](delete-alerts.md) is not reversible. |
| **Scope follows the HTTP method, not the effect** | It needs `modeling.update` even though it neither creates nor removes anything. |
| **Success is `204` with an empty body** | Read the resulting state from `alerts[].enabled` in [Get Alerts In Workspace](get-alerts-in-workspace.md). |
| **Dependency chain** | [Get Alerts In Workspace](get-alerts-in-workspace.md) (read `enabled`) → Change Alert Status → verify. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller may not act on at least one of the listed alerts, or the request arrived through a custom domain the workspace is not bound to. | Authenticate as the DB Owner, or list only alerts you own, from the standard API host. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — At least one alert's view does not belong to the workspace in the URL. | Change status from the workspace that owns the alerts. |
| [7387](../../../foundations/error-codes.md#error-7387) | 400 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not belong to the organisation in `ZANALYTICS-ORGID`. | Send the organisation id that owns the workspace. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use a domain you have purchased from Zoho Analytics, or the standard API host. |
| [8078](../../../foundations/error-codes.md#error-8078) | 400 | `EMPTY_JSON_ATTRIBUTE_FOUND` — `alertIds` or `enabled` was sent with an empty value. | Provide a non-empty value for both attributes. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — `alertIds` or `enabled` is missing from CONFIG. | Add the missing attribute. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — `enabled` is not a boolean, or an `alertIds` entry is not a JSON string. | Send `"enabled": true` / `false` and quote every id. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — The `CONFIG` parameter was not sent. | Send `CONFIG` as a URL-encoded form parameter containing a valid JSON object. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.update`. |

# Related

- [Data Alerts overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Schedules & Alerts](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Alerts In Workspace](get-alerts-in-workspace.md), [Get Alerts In View](get-alerts-in-view.md), [Get View Metadata For Alert](get-view-metadata-for-alert.md), [Get Alert Configuration](get-alert-configuration.md), [Create Alert](create-alert.md), [Update Alert](update-alert.md), [Delete Alerts](delete-alerts.md), [Run Alert](run-alert.md), [Get Alert Events](get-alert-events.md).
- [SDK examples](../../../sdk-examples/schedules-and-alerts/data-alerts/change-alert-status.md).
