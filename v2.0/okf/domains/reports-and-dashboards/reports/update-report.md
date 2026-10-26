---
type: API Endpoint
title: Update Report
description: Rebuilds an existing report from a fresh CONFIG and returns no body.
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
  permission_required: "The report's owner, an Account Admin, an Organization Admin, the Workspace Owner or a Workspace Admin. Any other caller — including a shared, group or Custom Role user holding Design Modify — is rejected with 7301. The caller must also be able to read the base table."
  error_codes:
    - 7016
    - 7103
    - 7106
    - 7301
    - 7309
    - 7319
    - 7701
    - 7703
    - 7705
    - 7706
    - 7725
    - 7727
    - 8008
    - 8021
    - 8050
    - 8051
    - 8052
    - 8053
    - 8055
    - 8056
    - 8057
    - 8058
    - 8059
    - 8144
    - 8145
    - 8162
    - 8164
    - 8166
    - 8167
    - 8168
    - 8169
    - 8170
    - 8179
    - 8187
    - 8188
    - 8192
    - 8250
    - 8251
    - 8253
    - 8254
    - 8255
    - 8256
    - 8257
    - 8258
    - 8507
    - 8509
    - 8516
    - 8517
    - 8534
    - 8535
    - 8542
    - 8544
    - 8547
    - 14037
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
    last_modified: 2026-10-20T17:34:40Z
generated:
  by: process:build_okf
  at: 2026-10-23T07:58:54Z
status: stable
---

# Summary

**PUT `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}`** - Update Report (Reports (Analysis Views) / Reports & Dashboards).

Rebuilds an existing report from a fresh CONFIG and returns no body. The `<report-id>` comes from
[Create Report](create-report.md) (`data.viewId`) or from the workspace's view list.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `updateReport` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The report's owner, an Account Admin, an Organization Admin, the Workspace Owner or a Workspace Admin. Any other caller — including a shared, group or Custom Role user holding Design Modify — is rejected with 7301. The caller must also be able to read the base table. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 204 with no body |
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

## CONFIG Parameters

CONFIG is **mandatory** for this API. Maximum encoded size 10,000,000 characters. **Every call replaces
the whole definition** — omitted attributes are cleared, not kept.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `reportType` | String (enum) | **Yes** | — | Must equal the stored report's type (`8021` otherwise). See [`reportType` Values](create-report.md#reporttype-values). |
| `axisColumns` | JSONArray | **Yes** | — | The complete new drop-field configuration, as in [`axisColumns` Fields](create-report.md#axiscolumns-fields). Every axis-column key not re-sent is removed. |
| `description` | String | No | Cleared | Max 250 characters. **Omitting it clears the stored description** (stored as an empty string). |
| `chartType` | String (enum) | No | Chosen automatically | As in Create. Omitting it lets the server choose the chart type. |
| `isAxisMerge` | Boolean | No | `false` | As in Create. Omitting it turns axis merging off. |
| `mergeAxisInfo` | JSONArray | No | — | As in Create — see [`mergeAxisInfo` Fields](create-report.md#mergeaxisinfo-fields). |
| `filters` | JSONArray | No | Cleared | As in Create — see [`filters` Fields](create-report.md#filters-fields) — except that `filterType: "wildcard"` is rejected with `8192`. **Omitting it removes every static filter.** |
| `userFilters` | JSONArray | No | Cleared | As in Create — see [`userFilters` Fields](create-report.md#userfilters-fields). **Omitting it removes every user filter.** |
| `title` | String | No | Stored name | New report name, 1–100 characters (`8507` above 100); empty or whitespace-only raises `7016`. Omitted → the stored name is kept. Sent → **the report is renamed.** Unlike Create, Update neither trims the name nor checks it for uniqueness: make sure no other object in the workspace has this name, otherwise two objects share it. |

> **Not accepted on Update:** `folderId` raises [`8145`](../../../foundations/error-codes.md#error-8145) — even when it equals the report's current folder
> — and `baseTableName` raises [`8542`](../../../foundations/error-codes.md#error-8542). A report cannot be moved or re-based through this API.

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

**Case 1 — Change the chart type and re-sort (minimal)**

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
        {"type": "xAxis", "columnName": "Order Date", "operation": "monthyear"},
        {"type": "yAxis", "columnName": "Sales", "operation": "sum", "sort": "asc"}
    ]
}
```

**Case 2 — Widen a filter, keeping everything else**

`userFilters` has to be re-sent in full even though it is unchanged; omitting it would delete it.

```http
PUT /restapi/v2/workspaces/466206000000071000/reports/466206000000105001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "reportType": "chart",
    "chartType": "line",
    "description": "Monthly trend, excluding returns",
    "axisColumns": [
        {"type": "xAxis", "columnName": "Order Date", "operation": "monthyear"},
        {"type": "yAxis", "columnName": "Sales", "operation": "sum"}
    ],
    "filters": [
        {
            "columnName": "Status",
            "operation": "actual",
            "filterType": "individualvalues",
            "values": ["Returned", "Cancelled"],
            "exclude": true
        }
    ],
    "userFilters": [
        {
            "columnName": "Product Category",
            "operation": "actual",
            "compType": "multiSelect",
            "filterType": "individualvalues",
            "isallval": true
        }
    ]
}
```

**Case 3 — Strip all filters off a pivot**

```http
PUT /restapi/v2/workspaces/466206000000071000/reports/466206000000105002 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "reportType": "pivot",
    "axisColumns": [
        {"type": "row", "columnName": "Region", "operation": "actual"},
        {"type": "data", "columnName": "Sales", "operation": "sum"}
    ]
}
```

**Case 4 — Attempt to move the report to another folder (rejected)**

```http
PUT /restapi/v2/workspaces/466206000000071000/reports/466206000000105001 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "reportType": "chart",
    "folderId": 466206000000094005,
    "axisColumns": [
        {"type": "xAxis", "columnName": "Order Date", "operation": "monthyear"},
        {"type": "yAxis", "columnName": "Sales", "operation": "sum"}
    ]
}
```

## Sample Responses

**HTTP 204 No Content — Report rebuilt (Cases 1–3)** — No response body is returned on success.

```
HTTP/1.1 204 No Content
```

**HTTP 406 Not Acceptable — `folderId` supplied (Case 4)**

```json
{
    "status": "failure",
    "summary": "FOLDERID_CANNOT_BE_UPDATED",
    "data": {
        "errorCode": 8145,
        "errorMessage": "Folder ID cannot be updated with analysisview API."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Update Report](../../../sdk-examples/reports-and-dashboards/reports/update-report.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Full replacement** | The report is rebuilt from exactly what you send. There is no field-level patching. |
| **What omission clears** | `filters` → all static filters removed. `userFilters` → all user filters removed. `description` → cleared. `chartType` → chosen automatically. `isAxisMerge` → off. Every axis-column key not re-sent (`displayName`, `sort`, `rangeSize`, `geoRole`, `windowFunction`) → removed. The chart legend is reset to its default position and title. |
| **What is kept** | The report's ID, owner, folder, creation time and sharing — and its name when `title` is omitted. |
| **Arrays replace, never merge** | `axisColumns`, `filters`, `userFilters` and `mergeAxisInfo` replace the stored arrays wholesale. |
| **Idempotent** | Sending the same CONFIG twice produces the same report. |
| **All-or-nothing** | The update is transactional: when any error is returned, the report is unchanged. |
| **Renaming** | Sending `title` renames the report. Update performs no name-uniqueness check and no trimming, so `7111`, `8201` and `7362` never occur — check uniqueness yourself before renaming. |
| **Do not build the CONFIG from a read** | See [Round-tripping a Report](overview.md#round-tripping-a-report). |
| **Client Portal / White Label** | Not available on Client Portal / White Label domains. Call the standard API host. |
| **Dependency chain** | [Create Report](create-report.md) → `data.viewId` → `<report-id>` → Update Report; keep the Create CONFIG as the base for the new CONFIG. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7016](../../../foundations/error-codes.md#error-7016) | 400 | OBJECT_NAME_EMPTY - title is empty or whitespace-only. | Supply a non-empty title. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7106](../../../foundations/error-codes.md#error-7106) | 404 | `META_OBJECT_NOT_PRESENT` — The report does not exist or has been deleted. | Verify `<report-id>`. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is not the report's owner, an Account Admin, an Organization Admin, the Workspace Owner or a Workspace Admin. | Call as one of those users. |
| [7309](../../../foundations/error-codes.md#error-7309) | 400 | SECURITY_NEEDS_LOGIN - Authorization header absent. | Send Authorization: Zoho-oauthtoken <token>. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The report belongs to a different workspace. | Make `<workspace-id>` and `<report-id>` consistent. |
| [7701](../../../foundations/error-codes.md#error-7701) | 400 | DROP_X_Y - The chart's shelves do not form a drawable chart; typically no X-axis or no Y-axis column. | Add the missing shelf. |
| [7703](../../../foundations/error-codes.md#error-7703) | 400 | REMOVE_CLR_FIELD - Multiple Y-axis columns in a shelf combination that does not support them, typically with a colorAxis column or with no X-axis column. | Drop the colour axis, add an X axis, or reduce to one Y axis. |
| [7705](../../../foundations/error-codes.md#error-7705) | 400 | DROP_SUMMARY - A summary report has no groupBy and no summarize column. | Add at least one. |
| [7706](../../../foundations/error-codes.md#error-7706) | 400 | DROP_PIVOT - A pivot report has no row, column or data column. | Add at least one. |
| [7725](../../../foundations/error-codes.md#error-7725) | 400 | ILLEGAL_COLUMN - The caller is not permitted to access a column used in the report. | Share the column with the caller, or remove it. |
| [7727](../../../foundations/error-codes.md#error-7727) | 400 | Y_EXCEED_LIMIT - More than 15 Y-axis columns on a chart. | Reduce to 15 or fewer. |
| [8008](../../../foundations/error-codes.md#error-8008) | 400 | UNKNOWN_PARAMETER - behaviour was supplied on a slider, dateRange or relative user filter. | Remove behaviour from that user filter. |
| [8021](../../../foundations/error-codes.md#error-8021) | 400 | `INVALID_VIEW_TYPE_IN_REQUEST` — `reportType` does not match the stored report's type, or the target is not a report. | Send the report's actual `reportType`. |
| [8050](../../../foundations/error-codes.md#error-8050) | 400 | INVALID_VALUE - A value is invalid: an unknown column name; an explicit null for any key; an empty columnName; a mergeAxisInfo rule violation; mergeAxisInfo without isAxisMerge: true; isallval: false with no values; an invalid user-filter operation or filterType; exclude: true on a range-picker user filter. | Check names and values against this document. |
| [8051](../../../foundations/error-codes.md#error-8051) | 400 | VALUE_NOT_PRESENT - A mandatory key is missing: title, reportType, axisColumns, an axis type or operation, a filter's filterType, values, exclude or operation, windowFunction.type, baseFieldPosition, movingCalculation or one of its keys, a wildcard object, mergeAxisInfo[].axisIndex; or the four-key base-field lookup found no matching entry. | Add the missing key. |
| [8052](../../../foundations/error-codes.md#error-8052) | 400 | COLUMN_COUNT_EXCEEDED - More than 1000 entries in axisColumns, filters or userFilters. | Reduce the array size. |
| [8053](../../../foundations/error-codes.md#error-8053) | 400 | AGGREGATE_COLUMN_INVALID_FIELD - In a pivot or summary report, an aggregate formula column is placed on row, column or groupBy. | Place it on data or summarize. |
| [8055](../../../foundations/error-codes.md#error-8055) | 400 | NUMERIC_RANKING_COLUMN - rankingColumn names a Numeric column. | Use a Text or Date column. |
| [8056](../../../foundations/error-codes.md#error-8056) | 400 | NOT_ALLOWED - pctoftotal on an average, stddev, variance, dc or distinctcount column, or on an aggregate formula. | Choose another window function type. |
| [8057](../../../foundations/error-codes.md#error-8057) | 400 | NOT_ALLOWED_BASEFIELD - windowFunction.baseField is not a dimension entry of axisColumns. | Add the base field to axisColumns as a dimension. |
| [8058](../../../foundations/error-codes.md#error-8058) | 400 | BASEFIELD_INVALID_AXIS - windowFunction.baseField sits on a different shelf from baseFieldPosition. | Correct baseFieldPosition. |
| [8059](../../../foundations/error-codes.md#error-8059) | 400 | UNRELATED_TABLE - A tableName is not a table joined to the base table. | Use a table reachable from the base table. |
| [8144](../../../foundations/error-codes.md#error-8144) | 406 | INVALID_GRAPH_TYPE - chartType is not a value from chartType Values. | Use an accepted chart type, or omit chartType. |
| [8145](../../../foundations/error-codes.md#error-8145) | 406 | `FOLDERID_CANNOT_BE_UPDATED` — `folderId` was supplied. | Remove `folderId`. |
| [8162](../../../foundations/error-codes.md#error-8162) | 400 | RANGE_SIZE_NOT_SUPPORTED_FOR_THIS_OPERATION - rangeSize was supplied on an operation other than range. | Use rangeSize only with operation: "range". |
| [8164](../../../foundations/error-codes.md#error-8164) | 400 | FILTER_COLUMN_DATATYPE_MISMATCH - A numeric individualvalues filter value is not a valid number for the column. | Send the exact stored numeric value. |
| [8166](../../../foundations/error-codes.md#error-8166) | 400 | INVALID OPERATION FOR THE COLUMN - The operation is not valid for the column's category and shelf; or a defaultFilterValues entry is invalid. | See Axis Operation Values and Static Filter Operation and Type Values. |
| [8167](../../../foundations/error-codes.md#error-8167) | 400 | INVALID FILTER TYPE FOR THE GIVEN OPERATION - The filterType is not valid for the column category and operation. | See Static Filter Operation and Type Values. |
| [8168](../../../foundations/error-codes.md#error-8168) | 400 | INVALID CRITERIA FORMAT FOR THE COLUMN - A values entry does not match the format for its filterType. | See Filter Value Formats. |
| [8169](../../../foundations/error-codes.md#error-8169) | 400 | INVALID WINDOW TYPE FOR THE COLUMN - windowFunction.type or movingCalculation.calculation is not a valid value. | See Window Function Type Values. |
| [8170](../../../foundations/error-codes.md#error-8170) | 400 | INVALID AXIS TYPE FOR THE REPORT - An axis type is not valid for the chosen reportType. | See Axis Type Values. |
| [8179](../../../foundations/error-codes.md#error-8179) | 403 | ADVFILTER_EXPRESSION_NO_CRITERIAS - wildcard.criteria is empty. | Supply 1-15 criteria. |
| [8187](../../../foundations/error-codes.md#error-8187) | 400 | ADVFILTER_EXPRESSION_ORDER_CHANGE - Criteria indexes in wildcard.expression are out of order. | Reference criteria as 1, 2, 3 … in order. |
| [8188](../../../foundations/error-codes.md#error-8188) | 400 | ADVFILTER_EXPRESSION_LENGTH_MISMATCH - The number of indexes in wildcard.expression differs from the number of criteria. | Reference every criterion exactly once. |
| [8192](../../../foundations/error-codes.md#error-8192) | 400 | `ADVFILTER_UPDATE_HANDLING` — A `filters` entry uses `filterType: "wildcard"`. | Wildcard filters can only be set at create time. |
| [8250](../../../foundations/error-codes.md#error-8250) | 400 | INVALID_UF_COMP_TYPE - compType is not valid for the column category or operation. | See User Filter Rules by Column. |
| [8251](../../../foundations/error-codes.md#error-8251) | 400 | INCORRECT_DATE_VALUE - A date in a date-range static filter could not be parsed. | Use the date formats in Filter Value Formats. |
| [8253](../../../foundations/error-codes.md#error-8253) | 400 | REQUIRED PARAM IS MISSING - A required key is missing: windowFunction.baseField, user-filter compType, or user-filter filterType where User Filter Rules by Column marks it required. | Add the key. |
| [8254](../../../foundations/error-codes.md#error-8254) | 400 | INVALID_VALUE_FOR_ATTRIBUTE_FOR_COLUMN - latitude / longitude on a text column, or a place role on a numeric column. | See Geo Role Values. |
| [8255](../../../foundations/error-codes.md#error-8255) | 400 | INVALID_KEY_GIVEN - operation: "geo" on a column type that cannot be geocoded. | Use a Plain Text, Number, Positive Number, Decimal Number or Geo column. |
| [8256](../../../foundations/error-codes.md#error-8256) | 404 | GEO_COL_COUNT_EXCEEDED - More than one text geo column on X, or more than one numeric geo column on one axis. | Keep one geo column per axis. |
| [8257](../../../foundations/error-codes.md#error-8257) | 400 | GEO_COL_COUNT_EXCEEDED_CATEGORICAL - A text geo column on X coexists with a numeric geo column on Y. | Use one or the other. |
| [8258](../../../foundations/error-codes.md#error-8258) | 400 | GEO_COL_CATEGORY_ONLY_X - A text geo column was placed on a shelf other than X. | Move it to xAxis. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | MORE_THAN_MAX_LENGTH - A string exceeds its limit: title 100, description 250, chartType 50, axis displayName 250, columnName 1000, axis tableName 100, windowFunction object 1000, serialised values / defaultFilterValues array 1000. | Shorten the value. |
| [8509](../../../foundations/error-codes.md#error-8509) | 400 | PATTERN_NOT_MATCHED - A value does not match its pattern: reportType: "Chart", type: "sizeAxis", sort: "descending", a chartType with a hyphen, compType: "multiselect", a wildcard expression without parentheses, a wildcard operation in lowercase. | Use the exact accepted values. |
| [8516](../../../foundations/error-codes.md#error-8516) | 400 | UNABLE_TO_PARSE_DATA_TYPE - A numeric value could not be parsed, for example rangeSize sent as an array. | Send a plain number. |
| [8517](../../../foundations/error-codes.md#error-8517) | 400 | DATATYPE_NOT_MATCHED - A value has the wrong JSON type: exclude: "yes", isAxisMerge: 1, folderId: "abc". | Use JSON booleans, numbers and strings as documented. |
| [8534](../../../foundations/error-codes.md#error-8534) | 400 | JSON_PARSE_ERROR - CONFIG is not valid JSON, or a key has the wrong structure (axisColumns as {}, values as a string, mergeAxisInfo as an object). | Arrays must be [], objects {}. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.update`. |
| [8542](../../../foundations/error-codes.md#error-8542) | 400 | `EXTRA_KEY_FOUND_IN_JSON` — `baseTableName` or any other key outside the Update schema is present. | Remove the key. |
| [8544](../../../foundations/error-codes.md#error-8544) | 400 | OUT_OF_RANGE - An integer is outside its range: percentileVal outside 0-100, a mergeAxisInfo index outside 0-100. | Use a value inside the range. |
| [8547](../../../foundations/error-codes.md#error-8547) | 400 | ARRAY_SIZE_OUT_OF_RANGE - More than 15 entries in wildcard.criteria. | Reduce the array size. |
| [14037](../../../foundations/error-codes.md#error-14037) | 400 | DISABLED_COLUMNS_USED - A disabled column is used in the report. | Enable the column, or remove it. |

# Related

- [Reports (Analysis Views) overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Reports & Dashboards](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Report](create-report.md), [Read Report Metadata](get-report-metadata.md).
- [SDK examples](../../../sdk-examples/reports-and-dashboards/reports/update-report.md).
