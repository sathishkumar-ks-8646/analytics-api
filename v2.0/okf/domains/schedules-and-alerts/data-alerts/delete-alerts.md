---
type: API Endpoint
title: Delete Alerts
description: Deletes one or more alerts in a workspace.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/alerts"
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - data-alerts
  - delete
  - modeling
api:
  operation_id: deleteAlerts
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/alerts"
  domain: schedules-and-alerts
  group: data-alerts
  oauth_scopes:
    - ZohoAnalytics.modeling.delete
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
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1alerts/delete"
    config_schema: DeleteAlertsConfig
    response_schema: null
  sdk_examples: "/sdk-examples/schedules-and-alerts/data-alerts/delete-alerts.md"
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

**DELETE `/restapi/v2/workspaces/{workspace-id}/alerts`** - Delete Alerts (Data Alerts / Schedules & Alerts).

Deletes one or more alerts in a workspace. Every id is validated before anything is removed, so the call is all-or-nothing.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `deleteAlerts` |
| HTTP method | DELETE |
| URL | `/restapi/v2/workspaces/{workspace-id}/alerts` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.delete`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingdelete) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the workspace, or a custom-role user with the Manage Data Alerts permission who either has all-alerts access or owns every alert listed. The check runs per id. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| OpenAPI | [`schedules-alerts-grouped-api.json`](../../../references/openapi/schedules-alerts-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1alerts/delete`; CONFIG schema `DeleteAlertsConfig` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.delete`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## CONFIG Parameters

CONFIG is **mandatory** for this API, and it is sent as a form body on a `DELETE` request.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `alertIds` | JSONArray of String | **Yes** | — | Alert ids to delete, as numeric **strings** — a bare numeric literal fails. **0–1000 entries**; an empty array is accepted and deletes nothing. Every id must belong to `<workspace-id>` (`7319`) and must still exist (`32000009`), and the caller must be permitted to act on each one (`7301`). |

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload (`status`, `summary`, `data.errorCode`, `data.errorMessage`).

# Examples

## Sample Requests

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

## Sample Responses

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

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Delete Alerts](../../../sdk-examples/schedules-and-alerts/data-alerts/delete-alerts.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **All-or-nothing per request** | Every id is checked for workspace membership and caller permission **before** any deletion happens, so one bad id fails the whole request and nothing is removed. |
| **Ids must be JSON strings** | `["137687000010815003"]`, not `[137687000010815003]`. A numeric literal fails when the server reads the entry as a string. |
| **An empty array is a no-op** | `{"alertIds": []}` returns `204` and deletes nothing. Omitting the key entirely is `8079`. |
| **Nothing is reported per id** | "Deleted" and "was already absent" are indistinguishable from the response. Confirm with [Get Alerts In Workspace](get-alerts-in-workspace.md) if it matters. |
| **It is a status change, not a purge** | The alert stops evaluating, disappears from the listing APIs and its id stops being actionable (`32000009`). There is no trash and no restore. |
| **Not the way to silence an alert temporarily** | Use [Change Alert Status](change-alert-status.md), which is reversible and preserves the id and the event history. |
| **Not idempotent** | A second delete of the same ids fails with `32000009`. |
| **Success is `204` with an empty body** | Treat the status code as the success indicator; never expect a JSON body. |
| **Dependency chain** | [Get Alerts In Workspace](get-alerts-in-workspace.md) → `alerts[].id` → Delete Alerts. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller may not act on at least one of the listed alerts, or the request arrived through a custom domain the workspace is not bound to. | Authenticate as the DB Owner, or list only alerts you own, from the standard API host. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — At least one alert's view does not belong to the workspace in the URL. | Delete alerts from the workspace that owns them. |
| [7387](../../../foundations/error-codes.md#error-7387) | 400 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not belong to the organisation in `ZANALYTICS-ORGID`. | Send the organisation id that owns the workspace. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use a domain you have purchased from Zoho Analytics, or the standard API host. |
| [8078](../../../foundations/error-codes.md#error-8078) | 400 | `EMPTY_JSON_ATTRIBUTE_FOUND` — `alertIds` was sent with an empty value. | Send an array of id strings, or omit the call. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — `alertIds` is missing from CONFIG. | Add `alertIds`. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — An `alertIds` entry is not a JSON string. | Quote every id: `["137687000010815003"]`. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — The `CONFIG` parameter was not sent. | Send `CONFIG` as a URL-encoded form body on the `DELETE` request. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.delete`. |

# Related

- [Data Alerts overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Schedules & Alerts](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Alerts In Workspace](get-alerts-in-workspace.md), [Get Alerts In View](get-alerts-in-view.md), [Get View Metadata For Alert](get-view-metadata-for-alert.md), [Get Alert Configuration](get-alert-configuration.md), [Create Alert](create-alert.md), [Update Alert](update-alert.md), [Change Alert Status](change-alert-status.md), [Run Alert](run-alert.md), [Get Alert Events](get-alert-events.md).
- [SDK examples](../../../sdk-examples/schedules-and-alerts/data-alerts/delete-alerts.md).
