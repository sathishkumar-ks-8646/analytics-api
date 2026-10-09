---
type: API Endpoint
title: Update Analysis View
description: Resets and updates the configuration of an existing analysis view in the specified workspace.
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
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or the View Owner, or a Shared User, or a Group Member, or any user with Design Modify permission on the view."
  error_codes:
    - 7103
    - 7104
    - 7111
    - 7301
    - 8021
    - 8050
    - 8075
    - 8100
    - 8119
    - 8252
    - 8535
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
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**PUT `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}`** - Update Analysis View (Reports (Analysis Views) / Reports & Dashboards).

From the OpenAPI specification:

Resets and updates the configuration of an existing analysis view in the specified workspace. The whole view configuration - axis columns, filters, user filters, chart type and settings - is replaced with the values provided in the CONFIG parameter, so anything that is omitted reverts to its empty default. Fetch the current configuration with Get Report Metadata, modify it, and send the complete object back.

The authenticated user must be an Account Admin or an Organization Admin, or the View Owner, or a Shared User, or a Group Member, or any user with Design Modify permission on the view.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `updateReport` |
| HTTP method | PUT |
| URL | `/restapi/v2/workspaces/{workspace-id}/reports/{view-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.update`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingupdate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or the View Owner, or a Shared User, or a Group Member, or any user with Design Modify permission on the view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
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
| `{view-id}` | string | ID of the analysis view to update. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## FIELDS FOR CONFIG JSON

> All sub-object schemas (Axis Column Object, Filter Object, User Filter Object, View Settings Object) are identical to those defined in **[Create Analysis View](create-report.md)**. Refer to those sections for field details, enum values, and samples.

| Attribute | Data Type | Mandatory | Default | Allowed Values / Constraints | Description |
|-----------|-----------|-----------|---------|------------------------------|-------------|
| `objId` | long | No | — | Valid view ID | ID of the view to update. If omitted, the view ID from the URL path is used. |
| `reportType` | string | **Yes** | — | `chart`, `pivot`, `summary` | Type of the analysis view. **Must match the existing view type** — cannot be changed via this API. |
| `description` | string | No | `""` | Max 250 characters | Updated description. If omitted, the existing description is **cleared**. Always include the value from Get Report Metadata to preserve it. |
| `chartType` | string | No | `""` | Max 50 characters (alphanumeric, spaces) | Chart sub-type (e.g., `bar`, `line`, `pie`). Required for `chart` views. |
| `axisColumns` | JSONArray | No | `[]` | Max serialized size: 1 MB. See **Axis Column Object** in [Create Analysis View](create-report.md). | Full replacement axis configuration for the view. |
| `isAxisMerge` | boolean | No | `false` | `true` or `false` | When `true`, merges multiple y-axes. Requires `mergeAxisInfo`. |
| `mergeAxisInfo` | JSONArray | No | `[]` | Max serialized size: 10 MB. Each item: `axisIndex` (int array) + `labelName` (string). | Axis merge groupings when `isAxisMerge` is `true`. |
| `filters` | JSONArray | No | `[]` | Max serialized size: 1 MB. See **Filter Object** in [Create Analysis View](create-report.md). | Replacement data filters for the view. |
| `userFilters` | JSONArray | No | `[]` | Max serialized size: 1 MB. See **User Filter Object** in [Create Analysis View](create-report.md). | Replacement interactive filter widgets for the view. |
| `settings` | JSONObject | No | `{}` | Max 10 KB. See **View Settings Object** in [Create Analysis View](create-report.md). | Replacement layout and theme settings. |

> ⚠️ **Read-only fields in Update:** `title` (display name) and `folderId` cannot be changed via this API. `title` in the CONFIG is silently ignored — the existing display name is always preserved. If `folderId` is provided and differs from the view's current folder, the request **fails with an error**. Omit both fields from the Update CONFIG.

## Sample values for CONFIG parameter

**Case 1: Update chart type and axis columns**

```json
{
  "reportType": "chart",
  "chartType": "line",
  "title": "Monthly Sales — Line Chart",
  "axisColumns": [
    {
      "type": "xAxis",
      "columnName": "Date",
      "tableName": "Sales",
      "operation": "monthyear"
    },
    {
      "type": "yAxis",
      "columnName": "Sales",
      "tableName": "Sales",
      "operation": "sum"
    },
    {
      "type": "yAxis",
      "columnName": "Cost",
      "tableName": "Sales",
      "operation": "sum"
    }
  ]
}
```

**Case 2: Move view to a different folder and apply a date filter**

```json
{
  "reportType": "pivot",
  "folderId": 466206000000091005,
  "axisColumns": [
    {
      "type": "row",
      "columnName": "Region",
      "tableName": "Sales"
    },
    {
      "type": "column",
      "columnName": "Date",
      "tableName": "Sales",
      "operation": "year"
    },
    {
      "type": "data",
      "columnName": "Sales",
      "tableName": "Sales",
      "operation": "sum"
    }
  ],
  "filters": [
    {
      "columnName": "Date",
      "tableName": "Sales",
      "operation": "actual",
      "filterType": "year",
      "values": ["2024", "2025"],
      "exclude": false
    }
  ],
  "settings": {
    "layout": { "defaultWidth": 120 },
    "themes": { "themeType": 2, "themeFontSize": 13, "themeRowSpacing": 2 }
  }
}
```

**Case 3: Enable axis merge across two y-axes with theme settings**

```json
{
  "reportType": "chart",
  "chartType": "combo",
  "axisColumns": [
    {
      "type": "xAxis",
      "columnName": "Product",
      "tableName": "Sales",
      "operation": "actual"
    },
    {
      "type": "yAxis",
      "columnName": "Sales",
      "tableName": "Sales",
      "operation": "sum"
    },
    {
      "type": "yAxis",
      "columnName": "Date",
      "tableName": "Sales",
      "operation": "count"
    },
    {
      "type": "yAxis",
      "columnName": "Cost",
      "tableName": "Sales",
      "operation": "count"
    }
  ],
  "isAxisMerge": true,
  "mergeAxisInfo": [
    {
      "axisIndex": [2, 5],
      "labelName": "Sales & Cost Metrics"
    }
  ],
  "settings": {
    "themes": {
      "themeType": 3,
      "themeColor": "#4A90D9",
      "themeFontSize": 12,
      "themeRowSpacing": 1
    }
  }
}
```

## Notes from the OpenAPI specification

Update Analysis View performs a full configuration reset, not a patch.
- Every axis column, filter, user filter and settings entry is replaced with the values sent in the CONFIG.
- Fields that are not provided revert to their empty defaults - omitting **axisColumns**, **filters** or **userFilters** clears them.
- **description** is cleared if it is omitted.
- Always fetch the current state with Get Report Metadata, modify it, then send the complete configuration back.

This is a workspace-scoped API. The **ZANALYTICS-ORGID** header carrying the organization ID that owns the workspace is mandatory. A workspaceKey in the format **orgid/workspacename** (for example, 700000123456/Sales_Analytics) may be used in place of the numeric workspace ID in the URL path.

The CONFIG parameter must be sent as a URL encoded JSON string in a form field named **CONFIG**, with the content type **application/x-www-form-urlencoded**.

The following fields cannot be changed through Update Analysis View:
- **title** - silently ignored; the existing display name is always preserved.
- **folderId** - the request fails if the value differs from the view's current folder. Omit it entirely.
- **reportType** - must match the existing view type. A mismatch fails with error code 8021.
- **baseTableName** - derived from the view's stored parent reference. Sending it is harmless but has no effect.

**chartType**, **isAxisMerge** and **mergeAxisInfo** apply only when **reportType** is chart. **chartType** is required for chart views, and **mergeAxisInfo** must be supplied whenever **isAxisMerge** is true.

Axis type values are spelled the same way in every direction. The Create and Update CONFIG accept the camelCase forms (**xAxis**, **yAxis**, **colorAxis**, **sizeAxis**, **textAxis**, **groupBy**, **summarize**) and Get Report Metadata returns them in that same form. When building a Create or Update CONFIG from a Get Report Metadata response, copy the axis type values verbatim.

The CONFIG parameter has a maximum serialized size of 10 MB. Ensure that the nested arrays - **axisColumns**, **mergeAxisInfo**, **filters** and **userFilters** - do not push the total CONFIG payload beyond this limit.

# Response

## Success Response

HTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

Not applicable — this API never returns a JSON body on success (HTTP 204 No Content). Only failure responses contain a JSON error payload.

## Notes from the OpenAPI specification

This API returns no response body on success - only an HTTP 204 No Content status. There is no JSON payload to parse; check the HTTP status code alone. Only failure responses carry a JSON error payload.

# Examples

## Sample Responses

**HTTP 204 No Content**

This API returns **no response body** on success — only an HTTP `204 No Content` status. There is no JSON payload to parse on success; check only the HTTP status code.

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Update Analysis View](../../../sdk-examples/reports-and-dashboards/reports/update-report.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success response has no body** | Update Analysis View returns a bare HTTP `204 No Content` on success — no `status`/`summary` JSON to parse. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Provide a valid `workspace-id` in the URL. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The specified view does not exist. | Ensure the `view-id` in the URL corresponds to an existing analysis view. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | A view with the given title already exists in the workspace. | Choose a unique `title` for the view. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission to update this view. | Ensure the user is an **Account Admin**, **Organization Admin**, **View Owner**, **Shared User**, **Group Member**, or has **Design Modify** permission on the view. |
| [8021](../../../foundations/error-codes.md#error-8021) | 400 | Invalid view type specified. | Set `reportType` to one of `chart`, `pivot`, or `summary`. |
| [8050](../../../foundations/error-codes.md#error-8050) | 400 | Invalid value provided. | Check that all CONFIG field values are within the allowed ranges and types. |
| [8075](../../../foundations/error-codes.md#error-8075) | 400 | Invalid chart type parameter. | Provide a valid `chartType` value (e.g., `Bar`, `Line`, `Pie`). |
| [8100](../../../foundations/error-codes.md#error-8100) | 400 | Operation not supported for this analysis view widget. | Ensure the update operation is valid for the current view type. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | Invalid value for attribute. | Verify all attribute values in `axisColumns`, `filters`, and `settings` conform to the allowed constraints. |
| [8252](../../../foundations/error-codes.md#error-8252) | 400 | Invalid report type. | Ensure `reportType` is `chart`, `pivot`, or `summary`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid OAuth token. | Provide a valid, non-expired OAuth token in the `Authorization` header. |

# Related

- [Reports (Analysis Views) overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Reports & Dashboards](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Create Analysis View](create-report.md), [Get Report Metadata](get-report-metadata.md).
- [SDK examples](../../../sdk-examples/reports-and-dashboards/reports/update-report.md).
