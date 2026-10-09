---
type: API Endpoint
title: Create Analysis View
description: "Creates a new analysis view - a chart, a pivot table or a summary view - in the specified workspace, based on a referenced base table."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/reports"
tags:
  - zoho-analytics
  - rest-api-v2
  - reports-and-dashboards
  - reports
  - post
  - modeling
api:
  operation_id: createReport
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/reports"
  domain: reports-and-dashboards
  group: reports
  oauth_scopes:
    - ZohoAnalytics.modeling.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or a Shared User, or a Group Member, or any user with Create Report permission on the workspace."
  error_codes:
    - 7103
    - 7104
    - 7111
    - 7301
    - 8021
    - 8050
    - 8075
    - 8119
    - 8252
    - 8535
  openapi:
    file: "/references/openapi/reports-dashboards-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1reports/post"
    config_schema: CreateReportConfig
    response_schema: CreateReportResponse
  sdk_examples: "/sdk-examples/reports-and-dashboards/reports/create-report.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/reports`** - Create Analysis View (Reports (Analysis Views) / Reports & Dashboards).

From the OpenAPI specification:

Creates a new analysis view - a chart, a pivot table or a summary view - in the specified workspace, based on a referenced base table. The view is configured through the CONFIG JSON parameter, which specifies the report type, the axis columns, the filters and the visualization settings.

The authenticated user must be an Account Admin or an Organization Admin, or a Workspace Admin, or a Shared User, or a Group Member, or any user with Create Report permission on the workspace.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createReport` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/reports` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or a Shared User, or a Group Member, or any user with Create Report permission on the workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`reports-dashboards-grouped-api.json`](../../../references/openapi/reports-dashboards-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1reports/post`; CONFIG schema `CreateReportConfig`; response schema `CreateReportResponse` |

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
| `{workspace-id}` | string | ID of the workspace in which the analysis view is created. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |

## FIELDS FOR CONFIG JSON

| Attribute | Data Type | Mandatory | Default | Allowed Values / Constraints | Description |
|-----------|-----------|-----------|---------|------------------------------|-------------|
| `baseTableName` | string | **Yes** | — | Max 100 characters | Display name of the base table on which the analysis view is created. |
| `reportType` | string | **Yes** | — | `chart`, `pivot`, `summary` | The type of analysis view to create. |
| `title` | string | No | `""` | Max 100 characters | Display name for the new view. If omitted, the view ID is used as the title. |
| `description` | string | No | `""` | Max 250 characters | Optional description for the view. |
| `folderId` | long | No | Root folder | Valid folder ID; pass `-1` for root | Folder in which to place the new view. |
| `chartType` | string | No | `""` | Max 50 characters (alphanumeric, spaces) | Chart sub-type (e.g., `bar`, `line`, `pie`, `bubble`, `stacked bar`, `heat map`). Required for `chart` views. |
| `axisColumns` | JSONArray | No | `[]` | Max serialized size: 1 MB. See **Axis Column Object** below. | Defines the axis/dimension/measure configuration for the view. |
| `isAxisMerge` | boolean | No | `false` | `true` or `false` | When `true`, merges multiple y-axes onto a single scale. Requires `mergeAxisInfo`. |
| `mergeAxisInfo` | JSONArray | No | `[]` | Max serialized size: 10 MB. Each item: `axisIndex` (int array of 1-based positions) + `labelName` (string). | Groupings for merged axes when `isAxisMerge` is `true`. |
| `filters` | JSONArray | No | `[]` | Max serialized size: 1 MB. See **Filter Object** below. | Data filters applied to the view at render time. |
| `userFilters` | JSONArray | No | `[]` | Max serialized size: 1 MB. See **User Filter Object** below. | Interactive filter widgets shown to the viewer inside the view. |
| `settings` | JSONObject | No | `{}` | Max 10 KB. See **View Settings Object** below. | Layout and theme settings for the view. |
| `modifiedPaths` | JSONObject | No | `{}` | Max 10 KB | Tracks which configuration paths were changed (used for incremental updates). |
| `drillActionConfig` | JSONObject | No | `{}` | Max 100 KB. See **Drill Action Config Object** below. | Configures drill-through actions triggered by clicking data points. |

---

### Axis Column Object

Each element in `axisColumns` is a JSON object describing one dimension or measure on the view.

| Field | Data Type | Mandatory | Description | Allowed Values |
|-------|-----------|-----------|-------------|----------------|
| `type` | string | **Yes** | Axis role of this column. See **Axis Type Enum** below. | See enum below |
| `columnName` | string | Conditional | Name of the column. Required if `columnId` is not provided. | Max 1000 characters |
| `columnId` | long | Conditional | ID of the column (alternative to `columnName`). | Valid column ID |
| `tableName` | string | No | Table the column belongs to. Useful in multi-table workspaces. | Max 100 characters |
| `tableId` | long | No | ID of the table (alternative to `tableName`). | Valid table ID |
| `displayName` | string | No | Custom label shown on the axis in the rendered chart. | Max 250 characters |
| `operation` | string | No | Aggregation or date-grouping operation for the column. See **Operation Enum** below. | See enum below |
| `geoRole` | string | Conditional | Geographic role — required when `operation` is `geo`. See **GeoRole Enum** below. | See enum below |
| `rangeSize` | double | No | Bucket size for numeric range grouping (used with `range` operation). | Any positive double |
| `sort` | string | No | Sort direction for this axis dimension. | `asc` — ascending, `desc` — descending |
| `format` | JSONObject | No | Number/date display formatting. See **Column Format Object** below. | — |
| `windowFunction` | JSONObject | No | Window/table-calculation applied to this measure. See **Window Function Object** below. | — |

#### Axis Type Enum

| Value | Applicable View Types | Description |
|-------|-----------------------|-------------|
| `xAxis` | chart | Horizontal axis (dimension or date) |
| `yAxis` | chart | Vertical axis (measure) |
| `colorAxis` | chart | Groups data into color segments |
| `sizeAxis` | chart (bubble) | Encodes bubble size by measure |
| `textAxis` | chart | Displays a text label on the chart |
| `tooltip` | chart | Extra column shown in hover tooltip |
| `row` | pivot | Row dimension grouping |
| `column` | pivot | Column dimension grouping |
| `data` | pivot | Measure/value cell in pivot |
| `groupBy` | summary | Group-by dimension column |
| `summarize` | summary | Aggregated measure column |
| `custom` | any | Custom-purpose axis column |

#### Operation Enum

| Value | Description |
|-------|-------------|
| `actual` | Raw/actual value |
| `sum` | Sum of values |
| `avg` | Average of values |
| `count` | Count of rows |
| `dc` | Count of unique values |
| `min` | Minimum value |
| `max` | Maximum value |
| `std` | Standard deviation |
| `variance` | Statistical variance |
| `percentile` | Percentile computation |
| `dimension` | Numeric column treated as dimension |
| `range` | Numeric range bucket grouping |
| `geo` | Geographic mapping (use with `geoRole`) |
| `year` | Group by year |
| `quarter` | Group by quarter (Q1–Q4) |
| `month` | Group by month |
| `monthyear` | Group by month-year |
| `absQuarter` | Absolute quarter (e.g., Q1 2024) |
| `datetime` | Full date-time value |
| `seasonal` | Seasonal period grouping |
| `quarteryear` | Group by quarter-year |
| `week` | Group by week |
| `weekyear` | Group by week-year |
| `weekday` | Group by weekday |
| `fulldate` | Group by full date |
| `day` | Group by day |
| `hour` | Group by hour |

#### GeoRole Enum

| Value | Description |
|-------|-------------|
| `latitude` | Numeric latitude coordinate |
| `longitude` | Numeric longitude coordinate |
| `location` | Text-based location (city, region, country) |

#### Samples — Axis Column Configurations

**Sample 1: Bar chart — product dimension on x-axis, sales sum on y-axis**

```json
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
  }
]
```

**Sample 2: Pivot table — rows, column year, and data measures with window functions**

```json
"axisColumns": [
  {
    "type": "row",
    "columnName": "Product",
    "operation": "actual"
  },
  {
    "type": "column",
    "columnName": "Date",
    "operation": "year"
  },
  {
    "type": "data",
    "columnName": "Sales",
    "operation": "avg",
    "windowFunction": { "type": "pctOfTotal" }
  },
  {
    "type": "data",
    "columnName": "Sales",
    "operation": "dc",
    "windowFunction": {
      "type": "pctOfCol",
      "baseField": "Product",
      "baseFieldPosition": "row"
    }
  }
]
```

**Sample 3: Scatter chart — color axis and tooltip for additional context**

```json
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
    "type": "colorAxis",
    "columnName": "Region",
    "tableName": "Sales",
    "operation": "actual"
  },
  {
    "type": "tooltip",
    "columnName": "Customer Name",
    "tableName": "Sales",
    "operation": "actual"
  }
]
```

**Sample 4: Geo map chart — latitude and longitude columns**

```json
"axisColumns": [
  {
    "type": "xAxis",
    "columnName": "Latitude",
    "tableName": "LatLong",
    "operation": "geo",
    "geoRole": "latitude"
  },
  {
    "type": "yAxis",
    "columnName": "Longitude",
    "tableName": "LatLong",
    "operation": "geo",
    "geoRole": "longitude"
  }
]
```

---

### Window Function Object

Attached to a measure entry in `axisColumns` to apply a table calculation on top of the aggregated value.

| Field | Data Type | Description | Allowed Values |
|-------|-----------|-------------|----------------|
| `type` | string | Window function type. | `runTotal` — running total, `pctOfTotal` — % of grand total, `pctOfCol` — % of column total, `pctdifffrom` — % diff from reference, `movingAvg` — moving average |
| `baseField` | string | Reference column name for comparison functions. | Column name string |
| `baseTable` | string | Reference table name. | Table name string |
| `baseFieldPosition` | string | Axis position of the reference field. | `xAxis`, `yAxis`, `row`, `column` |
| `baseFunction` | string | Date-grouping operation on the reference field. | Any value from **Operation Enum** |
| `percentileVal` | int | Percentile target value (only for `percentile` operation). | `0`–`100` |
| `movingCalculation` | JSONObject | Moving window definition: `calculation` (string), `previous` (int), `next` (int), `includeCurrent` (boolean), `includeNull` (boolean). | — |

#### Samples — Window Function

**Sample 1: Percentage of grand total**
```json
"windowFunction": {
  "type": "pctOfTotal"
}
```

**Sample 2: Percentage of column, referencing a pivot row dimension**
```json
"windowFunction": {
  "type": "pctOfCol",
  "baseField": "Product",
  "baseFieldPosition": "row"
}
```

**Sample 3: Running total anchored to date year on x-axis**
```json
"windowFunction": {
  "type": "runTotal",
  "baseField": "Date",
  "baseTable": "Sales",
  "baseFunction": "year",
  "baseFieldPosition": "xAxis"
}
```

---

### Column Format Object

Attached to an `axisColumns` entry to control how values are rendered.

| Field | Data Type | Description | Allowed Values |
|-------|-----------|-------------|----------------|
| `type` | string | Format category. | `number`, `currency`, `percentage`, `date`, `text` |
| `displayName` | string | Override label for this column. | Max 1000 characters |
| `currencyFormat` | string | Currency symbol/code. | e.g., `$`, `€`, `USD` |
| `alignment` | string | Cell text alignment. | `left`, `center`, `right` |
| `thousandSeparator` | int | Enable thousand separator. | `0` — off, `1` — on |
| `decimalPlaces` | int | Number of decimal places to display. | `0`–`9` |
| `decimalSeparator` | int | Decimal separator character. | `0` — period (`.`), `1` — comma (`,`) |
| `showSymbol` | boolean | Show the currency or percentage symbol. | `true` or `false` |
| `showNegativeSign` | boolean | Show explicit minus sign for negatives. | `true` or `false` |
| `numberingType` | int | Scale suffix for large numbers. | `0` — none, `1` — thousands (K), `2` — millions (M), `3` — billions (B) |
| `unitsList` | string | Custom unit suffix appended to value. | e.g., `kg`, `hrs` |
| `displayLabel` | string | Label override displayed in chart legend. | Max 1000 characters |
| `dateFormat` | string | Date display format pattern. | e.g., `yyyy-MM-dd`, `dd MMM yyyy` |
| `userLocale` | boolean | Apply the viewer's locale for formatting. | `true` or `false` |

#### Samples — Column Format

**Sample 1: Currency with two decimal places and thousand separator**
```json
"format": {
  "type": "currency",
  "currencyFormat": "$",
  "decimalPlaces": 2,
  "thousandSeparator": 1,
  "showSymbol": true
}
```

**Sample 2: Percentage value with no decimal places**
```json
"format": {
  "type": "percentage",
  "decimalPlaces": 0,
  "showSymbol": true
}
```

**Sample 3: Large number expressed in millions with custom unit**
```json
"format": {
  "type": "number",
  "numberingType": 2,
  "thousandSeparator": 1,
  "unitsList": "M"
}
```

---

### Filter Object

Each element in `filters` restricts the data rendered in the view based on column values.

| Field | Data Type | Description | Allowed Values |
|-------|-----------|-------------|----------------|
| `columnName` | string | Column to filter on. | Max 1000 characters |
| `columnId` | long | ID of the column (alternative to `columnName`). | Valid column ID |
| `tableName` | string | Table the column belongs to. | Max 1000 characters |
| `tableId` | long | ID of the table. | Valid table ID |
| `operation` | string | How the column value is computed for filtering. | Any value from **Operation Enum** |
| `filterType` | string | Filter category. | `value` — exact match, `ranking` — top/bottom N, `year`, `quarter`, `month`, `week`, `weekday`, `fulldate`, `date`, `datetime`, `quarteryear`, `weekyear`, `common`, `range` |
| `values` | JSONArray | Filter values or ranking spec (e.g., `"Top 5"`). | Array of strings |
| `rankingColumn` | string | Column used to rank results (for `ranking` filterType). | Column name |
| `rankingColumnDateSubType` | string | Date sub-grouping for ranking reference column. | Max 50 characters |
| `exclude` | boolean | When `true`, the listed `values` are excluded instead of included. | `true` or `false` |
| `wildcard` | JSONObject | Wildcard filter. Contains `criteria` (array, max 15 items each with `operation` + `value`) and `expression` (logical expression string). | — |
| `additionalDetails` | JSONObject | Extra filter context. Contains `type`, `label`, `isFromDashboard` (boolean), `fromViewId` (long). | — |

#### Samples — Filter Object

**Sample 1: Year filter — include specific years**
```json
"filters": [
  {
    "columnName": "Date",
    "tableName": "Sales",
    "operation": "actual",
    "filterType": "year",
    "values": ["2023", "2024"],
    "exclude": false
  }
]
```

**Sample 2: Ranking filter — top 5 products by average cost**
```json
"filters": [
  {
    "columnName": "Cost",
    "tableName": "Sales",
    "operation": "avg",
    "filterType": "ranking",
    "values": ["Top 5"],
    "rankingColumn": "Product Category",
    "exclude": false
  }
]
```

**Sample 3: Combined value filter and seasonal week filter**
```json
"filters": [
  {
    "columnName": "Region",
    "tableName": "Sales",
    "operation": "actual",
    "filterType": "value",
    "values": ["North", "East"],
    "exclude": false
  },
  {
    "columnName": "Date",
    "tableName": "Sales",
    "operation": "seasonal",
    "filterType": "week",
    "values": ["Week 2", "Week 3", "Week 4"],
    "exclude": false
  }
]
```

---

### User Filter Object

Each element in `userFilters` defines an interactive filter widget displayed to the viewer inside the view.

| Field | Data Type | Description | Allowed Values |
|-------|-----------|-------------|----------------|
| `tableName` | string | Table the filter column belongs to. | Max 1000 characters |
| `columnName` | string | Column the filter operates on. | Max 1000 characters |
| `operation` | string | Aggregation or grouping for the column. | Any value from **Operation Enum** |
| `compType` | string | UI widget type shown to the viewer. See **compType Enum** below. | See enum below |
| `filterType` | string | Data filter category applied by this widget. | Same values as **Filter Object** `filterType` |
| `isallval` | boolean | When `true`, initially selects all values in the widget. | `true` or `false` |
| `values` | JSONArray | Pre-selected/default values for the widget. | Array of strings |
| `defaultFilterValues` | JSONArray | Default values used when the viewer clears the selection. | Array of strings |
| `exclude` | boolean | When `true`, selected values are excluded. | `true` or `false` |
| `behaviour` | string | Controls which values populate the filter list. | `ListAllValues` — all dataset values, `ListOnlyRelevantValues` — only values relevant to current filters, `ListRelevantValues` — context-aware values |

#### compType Enum

| Value | Description |
|-------|-------------|
| `singleSelect` | Single-value dropdown selector |
| `multiSelect` | Multi-value checklist selector |
| `slider` | Numeric range slider |
| `dateRange` | Date range picker |

#### Samples — User Filter Object

**Sample 1: Single-select dropdown for a dimension, listing all values**
```json
"userFilters": [
  {
    "tableName": "Sales",
    "columnName": "Region",
    "operation": "actual",
    "compType": "singleSelect",
    "isallval": true,
    "exclude": false
  }
]
```

**Sample 2: Multi-select filter with pre-selected product values**
```json
"userFilters": [
  {
    "tableName": "Sales",
    "columnName": "Product",
    "operation": "actual",
    "compType": "multiSelect",
    "filterType": "individualValues",
    "isallval": false,
    "values": ["Bread", "CD"],
    "exclude": false
  }
]
```

**Sample 3: Date range picker with a default date window**
```json
"userFilters": [
  {
    "tableName": "Sales",
    "columnName": "Date",
    "operation": "dateRange",
    "compType": "dateRange",
    "filterType": "range",
    "isallval": false,
    "values": ["01 Jan 2020 to 31 Dec 2025"],
    "defaultFilterValues": ["01 Jan 2024 to 31 Dec 2024"]
  }
]
```

---

### View Settings Object

Controls column layout widths and the visual theme for the view.

#### Layout Sub-fields

| Field | Data Type | Description | Allowed Values |
|-------|-----------|-------------|----------------|
| `defaultWidth` | int | Default column width in pixels for pivot/summary tables. | `1`–`1000` |

#### Theme Sub-fields

| Field | Data Type | Description | Allowed Values |
|-------|-----------|-------------|----------------|
| `themeType` | int | Preset theme style index. | `1`–`7` |
| `themeColor` | string | Primary accent color (hex code). | e.g., `#4A90D9` |
| `themeFontSize` | int | Base font size in points. | `5`–`24` |
| `themeRowSpacing` | int | Row height/spacing level. | `1` — compact, `2` — normal, `3` — relaxed |
| `compactIndent` | int | Row indentation depth in compact mode. | `0`–`3` |
| `fontColor` | string | Override font color (hex code). | e.g., `#333333` |

#### Samples — View Settings

**Sample 1: Pivot with explicit column width, theme, and font settings**
```json
"settings": {
  "layout": {
    "defaultWidth": 143
  },
  "themes": {
    "themeType": 4,
    "themeFontSize": 14,
    "themeRowSpacing": 2
  }
}
```

**Sample 2: Custom accent color and font color for dark-style presentation**
```json
"settings": {
  "themes": {
    "themeType": 3,
    "themeColor": "#4A90D9",
    "themeFontSize": 12,
    "themeRowSpacing": 1,
    "fontColor": "#FFFFFF"
  }
}
```

**Sample 3: Compact layout with indented rows and narrow default column width**
```json
"settings": {
  "layout": {
    "defaultWidth": 100
  },
  "themes": {
    "themeType": 1,
    "themeFontSize": 11,
    "themeRowSpacing": 1,
    "compactIndent": 2
  }
}
```

---

### Drill Action Config Object

Configures actions triggered when a user clicks a data point in the rendered view.

| Field | Data Type | Description | Allowed Values |
|-------|-----------|-------------|----------------|
| `drillActionsConfig` | JSONArray | Array of drill action items (max 10 items). See sub-fields below. | — |

#### Drill Action Item Sub-fields

| Field | Data Type | Description | Allowed Values |
|-------|-----------|-------------|----------------|
| `id` | string | Unique action identifier. | Long integer or hyphenated long-int format |
| `name` | string | Display name for the action. | Max 50 characters |
| `urlString` | string | Target URL invoked when the action fires. | Valid URL; max 2000 characters |
| `methodType` | string | HTTP method for the URL call. | `GET`, `POST`, `PUT`, `DELETE` |
| `headers` | JSONArray | HTTP headers. Each entry: `key`, `value`, `type`. | Max serialized size: 5 KB |
| `params` | JSONArray | URL query parameters. Each entry: `key`, `value`, `type`. | Max serialized size: 5 KB |
| `formData` | JSONArray | Form body parameters. Each entry: `key`, `value`, `type`. | Max serialized size: 5 KB |
| `body` | string | Raw request body string. | Max 50,000 characters |
| `bodyType` | string | Body content format. | `raw`, `form`, `none` |

#### Samples — Drill Action Config

**Sample 1: Simple GET drill-through to an external page**
```json
"drillActionConfig": {
  "drillActionsConfig": [
    {
      "id": "1001",
      "name": "View Order Details",
      "urlString": "https://crm.example.com/orders?id={{OrderID}}",
      "methodType": "GET"
    }
  ]
}
```

**Sample 2: POST action with a JSON body and custom header**
```json
"drillActionConfig": {
  "drillActionsConfig": [
    {
      "id": "1002",
      "name": "Trigger Approval",
      "urlString": "https://api.example.com/approvals",
      "methodType": "POST",
      "headers": [
        { "key": "Content-Type", "value": "application/json", "type": "static" }
      ],
      "body": "{\"orderId\": \"{{OrderID}}\"}",
      "bodyType": "raw"
    }
  ]
}
```

## Sample values for CONFIG parameter

**Case 1: Create a bar chart with ranking filter**

```json
{
  "baseTableName": "Sales",
  "reportType": "chart",
  "chartType": "bar",
  "title": "Top Products by Average Cost",
  "description": "Bar chart filtered to top 5 products by average cost",
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
    }
  ],
  "filters": [
    {
      "columnName": "Cost",
      "tableName": "Sales",
      "operation": "avg",
      "filterType": "ranking",
      "values": ["Top 5"],
      "rankingColumn": "Product Category",
      "exclude": false
    }
  ]
}
```

**Case 2: Create a pivot table with multiple row/column axes and window functions**

```json
{
  "baseTableName": "Sales",
  "reportType": "pivot",
  "title": "Sales Pivot — Region by Year",
  "description": "Pivot showing sales and cost with percentage-of-total calculations",
  "axisColumns": [
    {
      "type": "row",
      "columnName": "Product",
      "operation": "actual"
    },
    {
      "type": "row",
      "columnName": "Date",
      "operation": "datetime"
    },
    {
      "type": "column",
      "columnName": "Date",
      "operation": "year"
    },
    {
      "type": "data",
      "columnName": "Sales",
      "operation": "avg",
      "windowFunction": { "type": "pctOfTotal" }
    },
    {
      "type": "data",
      "columnName": "Cost",
      "operation": "std"
    },
    {
      "type": "data",
      "columnName": "Sales",
      "operation": "dc",
      "windowFunction": {
        "type": "pctOfCol",
        "baseField": "Product",
        "baseFieldPosition": "row"
      }
    }
  ],
  "settings": {
    "layout": { "defaultWidth": 143 },
    "themes": { "themeType": 4, "themeFontSize": 14, "themeRowSpacing": 2 }
  }
}
```

**Case 3: Create a summary view with multi-select user filter and axis merge**

```json
{
  "baseTableName": "Sales",
  "reportType": "chart",
  "chartType": "combo",
  "title": "Sales vs Cost — Merged Axes",
  "description": "Combo chart with two y-axes merged and a multi-select product filter",
  "axisColumns": [
    {
      "type": "xAxis",
      "columnName": "Product",
      "tableName": "Sales",
      "operation": "actual",
      "displayName": ""
    },
    {
      "type": "yAxis",
      "columnName": "Sales",
      "tableName": "Sales",
      "operation": "min"
    },
    {
      "type": "yAxis",
      "columnName": "Cost",
      "tableName": "Sales",
      "operation": "sum"
    }
  ],
  "isAxisMerge": true,
  "mergeAxisInfo": [
    {
      "axisIndex": [2, 3],
      "labelName": "Sales & Cost"
    }
  ],
  "userFilters": [
    {
      "tableName": "Sales",
      "columnName": "Product",
      "operation": "actual",
      "compType": "multiSelect",
      "filterType": "individualValues",
      "isallval": false,
      "values": ["Bread", "CD"],
      "exclude": false
    }
  ],
  "folderId": 466206000000091001
}
```

## Notes from the OpenAPI specification

This is a workspace-scoped API. The **ZANALYTICS-ORGID** header carrying the organization ID that owns the workspace is mandatory. A workspaceKey in the format **orgid/workspacename** (for example, 700000123456/Sales_Analytics) may be used in place of the numeric workspace ID in the URL path.

The CONFIG parameter must be sent as a URL encoded JSON string in a form field named **CONFIG**, with the content type **application/x-www-form-urlencoded**.

**chartType**, **isAxisMerge** and **mergeAxisInfo** apply only when **reportType** is chart. **chartType** is required for chart views, and **mergeAxisInfo** must be supplied whenever **isAxisMerge** is true.

Axis type values are spelled the same way in every direction. The Create and Update CONFIG accept the camelCase forms (**xAxis**, **yAxis**, **colorAxis**, **sizeAxis**, **textAxis**, **groupBy**, **summarize**) and Get Report Metadata returns them in that same form. When building a Create or Update CONFIG from a Get Report Metadata response, copy the axis type values verbatim.

The CONFIG parameter has a maximum serialized size of 10 MB. Ensure that the nested arrays - **axisColumns**, **mergeAxisInfo**, **filters** and **userFilters** - do not push the total CONFIG payload beyond this limit.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Notes from the OpenAPI specification

The **reportConfig** object returned by Get Report Metadata is structurally identical to the Create CONFIG, so it can be used directly as a clone template. Change **title** to a value that is unique in the workspace, keep **baseTableName**, and verify that every **columnName** and **tableName** exists in the target workspace's base table before posting.

# Examples

## Sample Responses

**Case 1 – Success (chart created)**

```http
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8

{
  "status": "success",
  "summary": "Chart view created successfully.",
  "data": {
    "viewId": "466206000000105001"
  }
}
```

**Case 2 – Success (pivot created)**

```json
{
  "status": "success",
  "summary": "Pivot view created successfully.",
  "data": {
    "viewId": "466206000000106002"
  }
}
```

**Case 3 – Success (summary created)**

```json
{
  "status": "success",
  "summary": "Summary view created successfully.",
  "data": {
    "viewId": "466206000000107003"
  }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Analysis View](../../../sdk-examples/reports-and-dashboards/reports/create-report.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | Workspace not found. | Provide a valid `workspace-id` in the URL. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The specified base table does not exist in the workspace. | Ensure `baseTableName` matches an existing table in the workspace. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | A view with the given title already exists in the workspace. | Choose a unique `title` for the new view. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | User does not have permission to create a report. | Ensure the user is an **Account Admin**, **Organization Admin**, **Workspace Admin**, **Shared User**, **Group Member**, or has **Create Report** permission on the workspace. |
| [8021](../../../foundations/error-codes.md#error-8021) | 400 | Invalid view type specified. | Set `reportType` to one of `chart`, `pivot`, or `summary`. |
| [8050](../../../foundations/error-codes.md#error-8050) | 400 | Invalid value provided. | Check that all CONFIG field values are within the allowed ranges and types. |
| [8075](../../../foundations/error-codes.md#error-8075) | 400 | Invalid chart type parameter. | Provide a valid `chartType` value (e.g., `Bar`, `Line`, `Pie`). |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | Invalid value for attribute. | Verify all attribute values in `axisColumns`, `filters`, and `settings` conform to the allowed constraints. |
| [8252](../../../foundations/error-codes.md#error-8252) | 400 | Invalid report type. | Ensure `reportType` is `chart`, `pivot`, or `summary`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | Invalid OAuth token. | Provide a valid, non-expired OAuth token in the `Authorization` header. |

# Related

- [Reports (Analysis Views) overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Reports & Dashboards](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Update Analysis View](update-report.md), [Get Report Metadata](get-report-metadata.md).
- [SDK examples](../../../sdk-examples/reports-and-dashboards/reports/create-report.md).
