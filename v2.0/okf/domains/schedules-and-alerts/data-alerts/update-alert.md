---
type: API Endpoint
title: Update Alert
description: "Replaces an existing alert's configuration."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - data-alerts
  - put
  - modeling
api:
  operation_id: updateAlert
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}"
  domain: schedules-and-alerts
  group: data-alerts
  api_units:
    api_id: 2084
    action: UPDATE_ALERT
    category: METADATA
    units: 3
    units_basis: per_request
    units_note: "3 units per request"
    category_frequency_limit: 60 requests/minute
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the workspace, or a custom-role user with the Manage Data Alerts permission who either has all-alerts access or owns this alert."
  error_codes:
    - 7103
    - 7301
    - 7319
    - 7387
    - 8060
    - 8083
    - 8245
    - 8504
    - 8535
  openapi:
    file: "/references/openapi/schedules-alerts-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1alerts~1{alert-id}/put"
    config_schema: UpdateAlertConfig
    response_schema: null
  sdk_examples: "/sdk-examples/schedules-and-alerts/data-alerts/update-alert.md"
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

**PUT `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}`** - Update Alert (Data Alerts / Schedules & Alerts).

Replaces an existing alert's configuration. The CONFIG body is the **same shape as [Create Alert](create-alert.md)** and is treated as a **full replacement** — not a patch. It is also the only API that accepts the Zoho Flow mapping attributes.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `updateAlert` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the workspace, or a custom-role user with the Manage Data Alerts permission who either has all-alerts access or owns this alert. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| API units | 3 units per request - action `UPDATE_ALERT` (api-id `2084`), **METADATA** category. See [API units](../../../foundations/api-units.md). |
| Frequency limit | 60 requests/minute across all **METADATA**-category calls of the organization. See [API units](../../../foundations/api-units.md#unit-categories-and-frequency-limits). |
| OpenAPI | [`schedules-alerts-grouped-api.json`](../../../references/openapi/schedules-alerts-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1alerts~1{alert-id}/put`; CONFIG schema `UpdateAlertConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.update`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID, shown in the Zoho Analytics UI under Settings > Organisation. See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{alert-id}` | string | ID of the alert. | [How to obtain](../../../foundations/identifiers.md#alert-id) |

## CONFIG Parameters

CONFIG is **mandatory** for this API, and it must be complete — attributes you omit are **not** carried over from the stored alert.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `alertName` | String | **Yes** | — | As in [Create Alert](create-alert.md#config-parameters). Uniqueness is still enforced within the view, excluding this alert itself. |
| `summaryType` | String (enum) | Conditional | `data` | As in Create Alert. Still mandatory when the alert's view is a Pivot Table. See [`summaryType` Values](create-alert.md#summarytype-values). |
| `rowAxis` | String | Conditional | — | As in Create Alert. Mandatory when `summaryType` is `subTotal` on a Pivot / Summary view. |
| `columnAxis` | String | No | — | As in Create Alert. |
| `conditionExpression` | String | Conditional | `(1)` | As in Create Alert. Mandatory when `rules` has more than one entry. |
| `notifyOnChange` | Boolean | No | `false` | As in Create Alert. **Omitting it resets the alert to `false`.** |
| `isAnomaly` | Boolean | No | — | Accepted but ignored; derived from `rules`. |
| `scheduleDetails` | JSONObject | **Yes** | — | As in Create Alert, parsed as a complete period definition — never merged field-by-field with the stored one. See [`scheduleDetails` Fields](create-alert.md#scheduledetails-fields). |
| `email` | JSONObject | No\* | — | See [`email` Fields](create-alert.md#email-fields). **Omitting it removes the e-mail channel.** |
| `notification` | JSONObject | No\* | — | See [`notification` Fields](create-alert.md#notification-fields). Omitting it removes the in-app channel. |
| `slack` | JSONObject | No\* | — | See [`slack` and `msteams` Fields](create-alert.md#slack-and-msteams-fields). Omitting it removes the channel. |
| `msteams` | JSONObject | No\* | — | Same shape as `slack`. Omitting it removes the channel. |
| `webhook` | JSONObject | No\* | — | See [`webhook` Fields](create-alert.md#webhook-fields). Omitting it removes the channel. |
| `workflows` | JSONArray of JSONObject | No | — | **Accepted only here.** Re-asserts the Zoho Flow workflow mappings that already exist on this alert. Every `id` must already be mapped to **this** alert, otherwise `32000043` naming all offending ids at once. See [`workflows` Fields](#workflows-fields). |
| `actionsByFlow` | JSONArray of JSONObject | No | — | **Accepted only here.** Re-asserts the Zoho Flow action mappings that already exist on this alert. Every `actionConfigId` must already be mapped to this alert, otherwise `32000050`. See [`actionsByFlow` Fields](#actionsbyflow-fields). |
| `rules` | JSONArray of JSONObject | **Yes** | — | As in Create Alert, 1–10 entries. See [`rules` Fields](create-alert.md#rules-fields). |
| `validateSystemTags` | Boolean | No | `true` | As in Create Alert — the Data Warning gate applies to updates too. |

\* **At least one notification channel is required**, on exactly the same terms as [Create Alert](create-alert.md): the request must produce at least one stored channel (`32000001`), and a channel with no recipient is discarded (`32000013`).

### `workflows` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `id` | String | **Yes** | — | Workflow id, exactly as returned by `workflows[].id` of [Get Alert Configuration](get-alert-configuration.md) for the **same** alert. Digits only, up to 20 characters. An id not already mapped to this alert fails with `32000043`. |

> **`name` and `enabled` are not part of the write contract.** The request template defines no key other than `id`, so those display fields are ignored if present and are **not** validated against the stored mapping. Posting back an unedited [Get Alert Configuration](get-alert-configuration.md) response is therefore safe.

### `actionsByFlow` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `actionConfigId` | String | **Yes** | — | Flow action configuration id. Must already be mapped to this alert (`32000050`). **Send it as a JSON string**, even though [Get Alert Configuration](get-alert-configuration.md) returns it as a number — see the note below. |
| `actionConfigName` | String | No | — | Flow action name, up to 50 characters. Read when the mapping row has to be re-created. |
| `connectionId` | String | No | — | Id of the connection the action uses, also as a JSON **string**. Read when the mapping row has to be re-created. |

> **`actionsByFlow` does not round-trip verbatim.** [Get Alert Configuration](get-alert-configuration.md) emits `actionConfigId` and `connectionId` as genuine JSON **numbers**, but the write path reads them with a string accessor. Posting the response back unchanged therefore fails with [`8080`](../../../foundations/error-codes.md#error-8080); convert both values to strings first. Every other id in this family is a string in both directions.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`).

# Examples

## Sample Requests

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

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. The alert id is already in the URL, and the stored result is read back with [Get Alert Configuration](get-alert-configuration.md).

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

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Update Alert](../../../sdk-examples/schedules-and-alerts/data-alerts/update-alert.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Full replace, not a patch** | The CONFIG you send *becomes* the alert. An omitted channel is removed, an omitted `notifyOnChange` resets to `false`, and the whole `rules` array replaces the stored one. Start from [Get Alert Configuration](get-alert-configuration.md) output rather than composing a partial payload. |
| **The alert id never changes** | Unlike [Update Email Schedule](../email-schedules/update-email-schedule.md), which can mint a new id when the name or period changes, an alert keeps its id across every update. Stored references stay valid. |
| **The view cannot be changed** | The report an alert watches is fixed at creation. The URL carries no `<view-id>`, and there is no CONFIG attribute for it — move an alert by deleting it and creating a new one, which resets its event history. |
| **Everything Create Alert validates is validated again** | Both share one conversion path, so the whole [Create Alert error table](get-alerts-in-workspace.md#error-codes) applies here as well, on top of the alert-specific codes below. |
| **Idempotent** | Re-sending the same complete CONFIG leaves the alert in the same state and keeps the same id. The unique-name check ignores the alert being updated, so resending its own `alertName` is not `32000011`. |
| **List fields replace, never merge** | `rules`, `emailIds`, `groupIds`, `weekDays`, `monthDays`, `months`, webhook `params` / `headers`, `workflows` and `actionsByFlow` are all wholesale replacements. |
| **`workflows` validates ids only** | Each `workflows[].id` must already be mapped to this alert. `name` and `enabled` are ignored, so an unedited [Get Alert Configuration](get-alert-configuration.md) response posts back cleanly. All invalid ids are reported in a single `32000043`. |
| **These attributes re-assert, they do not create** | Neither `workflows` nor `actionsByFlow` can introduce a new mapping — mappings are created in Zoho Flow. Omitting them drops the mapping from the alert. |
| **Legacy schedules are rewritten on save** | An alert whose stored schedule used the old minutes-from-midnight form is rewritten in the current form by any successful update. |
| **Permission is ownership-based** | A custom-role user without all-alerts access can update only their own alerts, even on a view they may create alerts on. |
| **Success is `204` with an empty body** | The only way to confirm what was stored is to read it back with [Get Alert Configuration](get-alert-configuration.md). |
| **Dependency chain** | [Get Alert Configuration](get-alert-configuration.md) → edit the returned JSON → Update Alert → [Get Alert Configuration](get-alert-configuration.md) to verify. |

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
| [8245](../../../foundations/error-codes.md#error-8245) | 404 | `INVALID_VIEW_TYPE_FOR_OPERATION` — The alert's view is no longer a Chart, Pivot Table or Summary View. | The report has been converted to an unsupported type; recreate the alert elsewhere. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — The `CONFIG` parameter was not sent. | Send `CONFIG` as a URL-encoded form parameter containing a valid JSON object. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.update`. |

# Related

- [Data Alerts overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Schedules & Alerts](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Alerts In Workspace](get-alerts-in-workspace.md), [Get Alerts In View](get-alerts-in-view.md), [Get View Metadata For Alert](get-view-metadata-for-alert.md), [Get Alert Configuration](get-alert-configuration.md), [Create Alert](create-alert.md), [Delete Alerts](delete-alerts.md), [Change Alert Status](change-alert-status.md), [Run Alert](run-alert.md), [Get Alert Events](get-alert-events.md).
- [SDK examples](../../../sdk-examples/schedules-and-alerts/data-alerts/update-alert.md).
- [API units](../../../foundations/api-units.md) - unit cost, unit categories and frequency limits for every endpoint.
