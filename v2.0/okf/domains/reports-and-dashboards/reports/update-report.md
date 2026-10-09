---
type: API Endpoint
title: Update Report
description: Rebuilds an existing report from a fresh CONFIG.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/reports/{view-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - reports-and-dashboards
  - reports
  - put
  - modeling
api:
  operation_id: updateReport
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/reports/{view-id}"
  domain: reports-and-dashboards
  group: reports
  oauth_scopes:
    - ZohoAnalytics.modeling.update
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 204
  response_content_types: []
  permission_required: "Design Modify on the report — the owner, a Workspace Admin, an Organization Admin, or a shared or group user granted edit rights."
  error_codes:
    - 7005
    - 7016
    - 7104
    - 7106
    - 7111
    - 7138
    - 7301
    - 7362
    - 7701
    - 7703
    - 7727
    - 8008
    - 8021
    - 8050
    - 8051
    - 8052
    - 8057
    - 8059
    - 8092
    - 8144
    - 8145
    - 8147
    - 8162
    - 8166
    - 8167
    - 8168
    - 8170
    - 8191
    - 8250
    - 8252
    - 8253
    - 8254
    - 8255
    - 8256
    - 8257
    - 8258
    - 8504
    - 8507
    - 8509
    - 8516
    - 8517
    - 8534
    - 8535
    - 8542
  openapi:
    file: "/references/openapi/reports-dashboards-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1reports~1{view-id}/put"
    config_schema: UpdateReportConfig
    response_schema: null
  sdk_examples: "/sdk-examples/reports-and-dashboards/reports/update-report.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**PUT `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}`** - Update Report (Reports (Analysis Views) / Reports & Dashboards).

Rebuilds an existing report from a fresh CONFIG.

From the OpenAPI specification:

Rebuilds an existing report from a fresh CONFIG.

Permission required: Design Modify on the report — the owner, a Workspace Admin, an Organization Admin, or a shared or group user granted edit rights.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `updateReport` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | Design Modify on the report — the owner, a Workspace Admin, an Organization Admin, or a shared or group user granted edit rights. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
| Content-Type | `application/x-www-form-urlencoded` |
| Custom domain | Not permitted. |
| OpenAPI | [`reports-dashboards-grouped-api.json`](../../../references/openapi/reports-dashboards-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1reports~1{view-id}/put`; CONFIG schema `UpdateReportConfig` |

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
| `{workspace-id}` | string | ID of the workspace that contains the analysis view. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the report (view) to update. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameter

| Field | Mandatory | How it differs from Create |
|-------|-----------|----------------------------|
| `reportType` | **Yes** | Must match the stored view's type. A mismatch raises **8021**. |
| `axisColumns` | **Yes** | Identical structure to Create. |
| `title` | No | **Accepted but ignored.** The server overwrites it with the stored display name. A report cannot be renamed through this endpoint. |
| `description` | No | Accepted. Omitting it clears the existing description. |
| `chartType`, `isAxisMerge`, `mergeAxisInfo`, `filters`, `userFilters`, `settings` | No | Identical to Create. |
| `folderId` | No | Accepted by the schema, but the report cannot be moved. Supplying it raises **8145**. Omit it. |
| `baseTableName` | **Not accepted** | Rejected with **8542**. The base table cannot be changed. |
| `drillActionConfig`, `modifiedPaths` | **Not accepted** | Rejected with **8542**. |
| `objId` | No | Accepted by the schema but inert — the server always uses `<report-id>` from the URL. |

## Notes from the OpenAPI specification

Update Report rebuilds the report from scratch on every call; there is no field-level patching.
- Omitting **filters** or **userFilters** removes them all.
- Omitting **description** clears it.
- Omitting **chartType** falls back to the server's BEST selection.
- **axisColumns** is mandatory.

This is a workspace-scoped API. The **ZANALYTICS-ORGID** header carrying the organization ID that owns the workspace is mandatory.

This API is not available on white-label / custom domains. Call the standard REST host for your data centre (**analyticsapi.zoho.com**, **analyticsapi.zoho.eu**, ...).

The CONFIG parameter must be sent as a URL encoded JSON string in a form field named **CONFIG**, with the content type **application/x-www-form-urlencoded**.

**chartType**, **isAxisMerge** and **mergeAxisInfo** apply only when **reportType** is chart. **mergeAxisInfo** is required when merging and **isAxisMerge** must be true whenever it is non-empty.

The CONFIG parameter has a maximum encoded size of 10,000,000 characters. Each of **axisColumns**, **filters** and **userFilters** holds at most 1000 entries (8052).

The **reportConfig** returned by Read Report Metadata is a summary of the stored definition, not a Create or Update payload. It omits **folderId**, **settings**, **drillActionConfig**, **modifiedPaths**, every per-column **displayName**, **sort**, **rangeSize**, **windowFunction**, **format** and **geoRole**, the **wildcard**, **rankingColumn** and **additionalDetails** of filters, and every user-filter key except **tableName**, **columnName** and **operation**. Remove **baseTableName** and add **reportType** before using it as an update payload; for anything beyond trivial edits keep the CONFIG you submitted at create time and modify that.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Notes from the OpenAPI specification

This API returns no response body on success - only HTTP 204 No Content. Only failure responses carry a JSON error payload.

# Examples

## Sample Requests

**Case 1 — Change the chart type and re-sort**

```http
PUT /restapi/v2/workspaces/466206000000071000/reports/466206000000105001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
  "reportType": "chart",
  "chartType": "stacked bar",
  "description": "Monthly trend, excluding returns",
  "axisColumns": [
    { "type": "xAxis", "columnName": "Order Date", "operation": "monthyear" },
    { "type": "yAxis", "columnName": "Sales", "operation": "sum", "sort": "asc" }
  ]
}
```

**Case 2 — Widen a filter, keeping everything else**

Note that `userFilters` has to be re-sent in full even though it is unchanged; omitting it would delete it.

```
CONFIG={
  "reportType": "chart",
  "chartType": "line",
  "description": "Monthly trend, excluding returns",
  "axisColumns": [
    { "type": "xAxis", "columnName": "Order Date", "operation": "monthyear" },
    { "type": "yAxis", "columnName": "Sales", "operation": "sum" }
  ],
  "filters": [
    { "columnName": "Status", "operation": "actual", "filterType": "individualvalues",
      "values": ["Returned", "Cancelled"], "exclude": true }
  ],
  "userFilters": [
    { "columnName": "Product Category", "operation": "actual",
      "compType": "multiSelect", "filterType": "individualvalues", "isallval": true }
  ]
}
```

**Case 3 — Strip all filters off a report**

```
CONFIG={
  "reportType": "pivot",
  "axisColumns": [
    { "type": "row",  "columnName": "Region", "operation": "actual" },
    { "type": "data", "columnName": "Sales",  "operation": "sum"    }
  ]
}
```

## Sample Responses

**HTTP 204 No Content** — no response body is returned on success.

```
HTTP/1.1 204 No Content
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Update Report](../../../sdk-examples/reports-and-dashboards/reports/update-report.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

## Update is destructive

The report is rebuilt from scratch on every call. There is no field-level patching.

| Omit this | And this happens |
|---|---|
| `filters` | All static filters are removed. |
| `userFilters` | All user filters are removed. |
| `description` | The description is **cleared** — `description` is written unconditionally, so an absent key stores `null`. |
| `chartType` | The chart type falls back to the server's `BEST` selection. |
| `axisColumns` | The call fails — `axisColumns` is mandatory. |

Always [read the current definition](get-report-metadata.md) first — while remembering that the read
response is lossy. For anything beyond trivial edits, keep your own copy of the CONFIG you used at
create time and modify that instead — see [Round-tripping a report](overview.md#round-tripping-a-report).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | A null element inside axisColumns or filters. | Ensure every array element is a JSON object. |
| [7016](../../../foundations/error-codes.md#error-7016) | 400 | title is empty or whitespace-only. | Supply a non-empty title. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The report does not exist, has been deleted, or the caller cannot edit it. | Verify `<report-id>` and the caller's permission. |
| [7106](../../../foundations/error-codes.md#error-7106) | 404 | The report does not exist, has been deleted, or the caller cannot edit it. | Verify `<report-id>` and the caller's permission. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | A view with this title already exists in the workspace. | Choose a unique title. |
| [7138](../../../foundations/error-codes.md#error-7138) | 400 | baseTableName does not resolve to a table in this workspace. | Use the exact table display name. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The caller lacks Design Modify permission on the report. | Grant edit access. |
| [7362](../../../foundations/error-codes.md#error-7362) | 400 | folderId does not exist in the workspace. | Supply a valid folder ID or omit the key. |
| [7701](../../../foundations/error-codes.md#error-7701) | 400 | A chart report has no X-axis or no Y-axis column. | Add at least one of each. |
| [7703](../../../foundations/error-codes.md#error-7703) | 400 | A colorAxis column is present alongside more than one Y-axis column. | Drop the colour axis, or reduce to one Y axis. |
| [7727](../../../foundations/error-codes.md#error-7727) | 400 | More than 15 Y-axis columns on a chart. | Reduce to 15 or fewer. |
| [8008](../../../foundations/error-codes.md#error-8008) | 400 | behaviour was supplied on a daterange or relative user filter. | Remove behaviour. |
| [8021](../../../foundations/error-codes.md#error-8021) | 400 | `reportType` does not match the stored view's type, or the target is not an analysis view at all. | Send the report's actual type. |
| [8050](../../../foundations/error-codes.md#error-8050) | 400 | A value is invalid — unknown columnName, an operation incompatible with the column, a null axisColumns. | Check column names and operations. |
| [8051](../../../foundations/error-codes.md#error-8051) | 400 | A required field is missing — title, reportType, axisColumns, or a mandatory key inside an axis/filter object. | Add the missing field. |
| [8052](../../../foundations/error-codes.md#error-8052) | 400 | More than 1000 entries in axisColumns, filters or userFilters. | Reduce the array size. |
| [8057](../../../foundations/error-codes.md#error-8057) | 400 | The column named in windowFunction.baseField cannot be used as a base field here. | Choose a different reference column. |
| [8059](../../../foundations/error-codes.md#error-8059) | 400 | The tableName is not part of the workspace or is not joined to the base table. | Use a table reachable through the join graph. |
| [8092](../../../foundations/error-codes.md#error-8092) | 400 | reportType resolves to a view kind that cannot be saved standalone. | Use chart, pivot or summary. |
| [8144](../../../foundations/error-codes.md#error-8144) | 400 | chartType is not a recognised chart name. | See Appendix A. |
| [8145](../../../foundations/error-codes.md#error-8145) | 400 | `folderId` was supplied. | Remove `folderId` — reports cannot be moved through this endpoint. |
| [8147](../../../foundations/error-codes.md#error-8147) | 400 | settings was supplied for a non-pivot report. | Remove settings, or change reportType to pivot. |
| [8162](../../../foundations/error-codes.md#error-8162) | 400 | rangeSize was supplied as a string, or on an operation that does not support ranges. | Send a JSON number, and only with range grouping. |
| [8166](../../../foundations/error-codes.md#error-8166) | 400 | The operation is incompatible with the column's data type. | See Appendix C. |
| [8167](../../../foundations/error-codes.md#error-8167) | 400 | The filterType is not valid for the column type + operation combination. | See Appendix D. |
| [8168](../../../foundations/error-codes.md#error-8168) | 400 | A values entry does not match the expected format for the filterType. | See Appendix E. |
| [8170](../../../foundations/error-codes.md#error-8170) | 400 | An axis type is not valid for the chosen reportType. | See Appendix B. |
| [8191](../../../foundations/error-codes.md#error-8191) | 400 | An invalid date value was supplied to a date filter. | Use the documented date formats. |
| [8250](../../../foundations/error-codes.md#error-8250) | 400 | compType is not applicable to the column category — e.g. slider on a dimension, singleSelect on a measure. | Match the widget to the column type. |
| [8252](../../../foundations/error-codes.md#error-8252) | 400 | reportType is absent or null. | Supply chart, pivot or summary. |
| [8253](../../../foundations/error-codes.md#error-8253) | 400 | A mandatory userFilters key is missing, typically compType or filterType. | Add the missing key. |
| [8254](../../../foundations/error-codes.md#error-8254) | 400 | A geoRole value is wrong for the column type. | latitude/longitude for numeric columns; place roles for text columns. |
| [8255](../../../foundations/error-codes.md#error-8255) | 400 | geoRole was supplied on a column that cannot be geocoded. | Remove geoRole, or use a geocodable column. |
| [8256](../../../foundations/error-codes.md#error-8256) | 400 | More than one geo operation on the same axis. | Keep one geo column per axis. |
| [8257](../../../foundations/error-codes.md#error-8257) | 400 | A numeric geo column coexists with a categorical geo column. | Use one or the other. |
| [8258](../../../foundations/error-codes.md#error-8258) | 400 | A categorical geo column was placed on an axis other than X. | Move it to xAxis. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | baseTableName is absent, or the CONFIG parameter itself is missing. | Send CONFIG with baseTableName. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | title exceeds 100 characters, description exceeds 250, or an axis displayName exceeds 250. | Shorten the value. |
| [8509](../../../foundations/error-codes.md#error-8509) | 400 | An enumerated or pattern-constrained value does not match — reportType: "Chart" (must be lowercase), type: "sizeAxis" (must be sizeaxis), sort: "descending", a wildcard expression without parentheses. | Use the exact accepted values. |
| [8516](../../../foundations/error-codes.md#error-8516) | 400 | rangeSize was supplied as an array. | Send a plain number. |
| [8517](../../../foundations/error-codes.md#error-8517) | 400 | A field has the wrong JSON data type — exclude: "yes", isAxisMerge: "maybe", compType: 123. | Use real JSON booleans and strings. |
| [8534](../../../foundations/error-codes.md#error-8534) | 400 | CONFIG is malformed, or a key has the wrong structural type — axisColumns as {}, mergeAxisInfo as an object, values as a bare string. | Arrays must be [], objects {}. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid or expired OAuth token. | Refresh with scope `ZohoAnalytics.modeling.update`. |
| [8542](../../../foundations/error-codes.md#error-8542) | 400 | `baseTableName`, `drillActionConfig`, `modifiedPaths` or any other key outside the Update schema is present. | Remove the key. |

# Related

- [Reports (Analysis Views) overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Reports & Dashboards](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Report](create-report.md), [Read Report Metadata](get-report-metadata.md).
- [SDK examples](../../../sdk-examples/reports-and-dashboards/reports/update-report.md).
