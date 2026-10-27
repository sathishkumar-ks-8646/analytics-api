---
type: API Endpoint
title: Get Alert Events
description: "Returns the audit trail of one alert's evaluations - when each ran, and whether it triggered, did not trigger, or failed."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/events"
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - data-alerts
  - get
  - metadata
api:
  operation_id: getAlertEvents
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/events"
  domain: schedules-and-alerts
  group: data-alerts
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: query
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the workspace, or a custom-role user with the Manage Data Alerts permission who either has all-alerts access or owns this alert."
  error_codes:
    - 7103
    - 7301
    - 7319
    - 7387
    - 8060
    - 8080
    - 8083
    - 8119
    - 8535
  openapi:
    file: "/references/openapi/schedules-alerts-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1alerts~1{alert-id}~1events/get"
    config_schema: GetAlertEventsConfig
    response_schema: GetAlertEventsResponse
  sdk_examples: "/sdk-examples/schedules-and-alerts/data-alerts/get-alert-events.md"
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

**GET `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/events`** - Get Alert Events (Data Alerts / Schedules & Alerts).

Returns the audit trail of one alert's evaluations — when each ran, and whether it triggered, did not trigger, or failed. This is the only machine-readable source of an alert's outcome, and the only paginated API in this family.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getAlertEvents` |
| HTTP method | GET |
| URL | `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/events` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the workspace, or a custom-role user with the Manage Data Alerts permission who either has all-alerts access or owns this alert. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the URL-encoded `CONFIG` query parameter - optional |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`schedules-alerts-grouped-api.json`](../../../references/openapi/schedules-alerts-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1alerts~1{alert-id}~1events/get`; CONFIG schema `GetAlertEventsConfig`; response schema `GetAlertEventsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID, shown in the Zoho Analytics UI under Settings > Organisation. See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{alert-id}` | string | ID of the alert. | [How to obtain](../../../foundations/identifiers.md#alert-id) |

## CONFIG Parameters

CONFIG is **optional** for this API and is sent as a query parameter. Omitting it returns the first 100 events across the full 45-day retention window.

| Parameter | Type | Mandatory | Default | Max Length | Description |
|-----------|------|-----------|---------|------------|-------------|
| `fromDate` | String | No | Start of day, 44 days before today | 50 | Inclusive lower bound, as `yyyy-MM-dd HH:mm:ss` or `yyyy-MM-dd` (the time then defaults to `00:00:00.000`). Interpreted in the **caller's profile time zone**. A malformed value is `32000028`. |
| `toDate` | String | No | End of today | 50 | Inclusive upper bound, same formats. A date-only value defaults the time to `23:59:59.999`. Must be greater than or equal to `fromDate`, otherwise `8119`. |
| `status` | JSONArray of String | No | All outcomes | 200 | Outcome filter, **1–3 distinct entries** drawn from `triggered`, `notTriggered` and `error`. Duplicates collapse silently. An unknown value, or a non-string entry, is `8119`. See [Alert Event Statuses](overview.md#alert-event-statuses). |
| `pageNo` | Integer | No | `1` | — | 1-based page number, **1–100000**. |
| `recordsPerPage` | Integer | No | `100` | — | Page size, **1–100**. A larger value is **silently clamped** to 100 — compare `pageDetails.recordsPerPage` against what you asked for. |

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

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

# Examples

## Sample Requests

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

## Sample Responses

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

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get Alert Events](../../../sdk-examples/schedules-and-alerts/data-alerts/get-alert-events.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **The only machine-readable outcome** | `alertEvents[].status` is a stable enum. `lastRunStatus` in [Get Alerts In Workspace](get-alerts-in-workspace.md) is a translated label and must never be parsed. |
| **Events come back oldest first** | The audit rows are sorted ascending by timestamp, so the newest event is the **last** entry on the **last** page. To read the most recent outcome, walk to the end rather than taking `alertEvents[0]`. |
| **Always paginated** | `pageDetails` is present whether or not you asked for paging, `recordsPerPage` is clamped to 100, and "more data" is signalled by `hasNextPage` rather than by a full page. Loop on `hasNextPage`, not on page length. |
| **History is retained for 45 days, inclusive of today** | Older events are purged, not filtered, so a wider `fromDate` cannot recover them. The implicit lower bound is start-of-day 44 days ago, which together with end-of-today spans exactly 45 calendar days. |
| **Date defaults are asymmetric** | With neither bound supplied the range is the full retention window. With only `fromDate` the upper bound is end-of-today; with only `toDate` the lower bound is the start of the retention window. All four combinations are resolved in the caller's profile time zone. |
| **Date-only values are expanded** | `fromDate: "2026-05-01"` becomes `00:00:00.000` and `toDate: "2026-05-31"` becomes `23:59:59.999`, so a date-only range is inclusive of both whole days. |
| **An empty result is a success** | `[]` means the filters matched nothing, which is also what a brand-new alert returns. |
| **`errorCode` here is a name, not a number** | It is the symbolic name recorded on the audit row, unrelated to the numeric codes in the Error Codes tables. |
| **CONFIG travels in the query string** | This is a `GET`; send `CONFIG` as a URL-encoded query parameter, not as a body. No `Content-Type` header is needed. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get Alerts In Workspace](get-alerts-in-workspace.md) → `alerts[].id` → Get Alert Events; after [Run Alert](run-alert.md), poll here for the outcome. |

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
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — `CONFIG` was sent but is not a parseable JSON object. | Send a valid, URL-encoded JSON object, or omit `CONFIG` entirely. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE` — `fromDate` is later than `toDate`, or a `status` entry is not one of `triggered`, `notTriggered`, `error`, or `pageNo` / `recordsPerPage` is outside its declared range. | Correct the range, the filter values, or the paging numbers. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [Data Alerts overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Schedules & Alerts](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Alerts In Workspace](get-alerts-in-workspace.md), [Get Alerts In View](get-alerts-in-view.md), [Get View Metadata For Alert](get-view-metadata-for-alert.md), [Get Alert Configuration](get-alert-configuration.md), [Create Alert](create-alert.md), [Update Alert](update-alert.md), [Delete Alerts](delete-alerts.md), [Change Alert Status](change-alert-status.md), [Run Alert](run-alert.md).
- [SDK examples](../../../sdk-examples/schedules-and-alerts/data-alerts/get-alert-events.md).
