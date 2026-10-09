---
type: SDK Example
title: SDK examples - Create Report
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/reports (createReport)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/reports"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - reports-and-dashboards
  - reports
  - bash
  - csharp
  - go
  - java
  - php
  - python
  - javascript
  - ruby
  - deluge
api:
  operation_id: createReport
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/reports"
  endpoint_doc: "/domains/reports-and-dashboards/reports/create-report.md"
  languages:
    - cURL
    - "C#"
    - Go
    - Java
    - PHP
    - Python
    - Node.js
    - Ruby
    - Deluge (Zoho scripting)
sources:
  - id: openapi-spec
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
  - id: endpoint-doc
    resource: "/domains/reports-and-dashboards/reports/create-report.md"
    title: Endpoint reference - Create Report
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Create Report](../../../domains/reports-and-dashboards/reports/create-report.md) (`POST /restapi/v2/workspaces/{workspace-id}/reports`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/reports" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"baseTableName":"Sales","title":"Sales by Region","description":"Comprehensive analysis of sales metrics across regions","reportType":"chart","chartType":"bar","axisColumns":[{"type":"xAxis","columnName":"Region","operation":"actual"},{"type":"yAxis","columnName":"Sales","operation":"sum"}]}'
```

## C#

```csharp
using System;
using System.Collections.Generic;
using ZohoAnalytics;

namespace ZohoAnalyticsTest
{
    class Program
    {
        long orgId = 55522777;
        long workspaceId = 35130000001055707;

        public void CreateVisual(IAnalyticsClient ac)
        {
            string baseTableName = "Sales";
            string title = "Sales by Region";
            string description = "Comprehensive analysis of sales metrics across regions";
            // Allowed values for reportType: "chart", "pivot", "summary"
            string reportType = "chart";
            // Allowed values for chartType: see the supported chart types reference
            string chartType = "bar";
            List<Dictionary<string, object>> axisColumns = new List<Dictionary<string, object>>();
            axisColumns.Add(new Dictionary<string, object>{{"type","xAxis"},{"columnName","Region"},{"operation","actual"}});
            axisColumns.Add(new Dictionary<string, object>{{"type","yAxis"},{"columnName","Sales"},{"operation","sum"}});
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            string viewId = workspace.CreateView(baseTableName, title, description, reportType, chartType, axisColumns, null, null);
            Console.WriteLine(viewId);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.CreateVisual(ac);
        }
    }
}
```

## Go

```go
package main

import (
    "fmt"
    ZAnalytics "zoho/pkg/analyticsclient"
)

var (
    clientId = "1000.xxxxxxx"
    clientSecret = "xxxxxxx"
    refreshToken = "1000.xxxxxxx.xxxxxxx"
    orgId = "55522777"
    workspaceId = "35130000001055707"
)

func CreateVisual(ac ZAnalytics.Client) {
    baseTableName := "Sales"
    title := "Sales by Region"
    description := "Comprehensive analysis of sales metrics across regions"
    // Allowed values for reportType: "chart", "pivot", "summary"
    reportType := "chart"
    // Allowed values for chartType: see the supported chart types reference
    chartType := "bar"
    xAxis := map[string]interface{}{"type": "xAxis", "columnName": "Region", "operation": "actual"}
    yAxis := map[string]interface{}{"type": "yAxis", "columnName": "Sales", "operation": "sum"}
    axisColumns := []map[string]interface{}{xAxis, yAxis}
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    viewId, exception := workspace.CreateView(baseTableName, title, description, reportType, chartType, axisColumns, nil, nil)
    if exception != nil { fmt.Println(exception.ErrorMessage); return }
    fmt.Println(viewId)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateVisual(ac)
}
```

## Java

```java
import com.zoho.analytics.client.*;
import org.json.*;

public class Test {
    private long orgId = 55522777l;
    private long workspaceId = 35130000001055707l;

    public static void main(String args[]) {
        String clientId = "1000.xxxxxxx";
        String clientSecret = "xxxxxxx";
        String refreshToken = "1000.xxxxxxx.xxxxxxx";
        Test tObj = new Test();
        AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
        try {
            tObj.createVisual(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void createVisual(AnalyticsClient ac) throws Exception {
        String baseTableName = "Sales";
        String title = "Sales by Region";
        String description = "Comprehensive analysis of sales metrics across regions";
        // Allowed values for reportType: "chart", "pivot", "summary"
        String reportType = "chart";
        // Allowed values for chartType: see the supported chart types reference
        String chartType = "bar";
        JSONObject xAxis = new JSONObject();
        xAxis.put("type", "xAxis");
        xAxis.put("columnName", "Region");
        xAxis.put("operation", "actual");
        JSONObject yAxis = new JSONObject();
        yAxis.put("type", "yAxis");
        yAxis.put("columnName", "Sales");
        yAxis.put("operation", "sum");
        JSONArray axisColumns = new JSONArray();
        axisColumns.put(xAxis);
        axisColumns.put(yAxis);
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        String viewId = workspace.createView(baseTableName, title, description, reportType, chartType, axisColumns, null, null);
        System.out.println(viewId);
    }
}
```

## PHP

```php
<?php
require 'AnalyticsClient.php';

class Test {
    public $ac;
    public $org_id = "55522777";
    public $workspace_id = "35130000001055707";
    function __construct() {
        $this->ac = new AnalyticsClient("1000.xxxxxxx", "xxxxxxx", "1000.xxxxxxx.xxxxxxx");
    }

    function createVisual() {
        $base_table_name = "Sales";
        $title = "Sales by Region";
        $description = "Comprehensive analysis of sales metrics across regions";
        // Allowed values for $report_type: "chart", "pivot", "summary"
        $report_type = "chart";
        // Allowed values for $chart_type: see the supported chart types reference
        $chart_type = "bar";
        $x_axis = ["type" => "xAxis", "columnName" => "Region", "operation" => "actual"];
        $y_axis = ["type" => "yAxis", "columnName" => "Sales", "operation" => "sum"];
        $axis_columns = [$x_axis, $y_axis];
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $view_id = $workspace->createView($base_table_name, $title, $description, $report_type, $chart_type, $axis_columns);
        print_r($view_id);
    }
}

$obj = new Test();
$obj->createVisual();
?>
```

## Python

```python
from AnalyticsClient import AnalyticsClient

class Config:
    CLIENTID = "1000.xxxxxxx"
    CLIENTSECRET = "xxxxxxx"
    REFRESHTOKEN = "1000.xxxxxxx.xxxxxxx"
    ORGID = "55522777"
    WORKSPACEID = "35130000001055707"

class sample:
    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def create_visual(self, ac):
        base_table_name = "Sales"
        title = "Sales by Region"
        description = "Comprehensive analysis of sales metrics across regions"
        # Allowed values for report_type: "chart", "pivot", "summary"
        report_type = "chart"
        # Allowed values for chart_type: see the supported chart types reference
        chart_type = "bar"
        xAxis = {"type": "xAxis", "columnName": "Region", "operation": "actual"}
        yAxis = {"type": "yAxis", "columnName": "Sales", "operation": "sum"}
        axis_columns = [xAxis, yAxis]
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        view_id = workspace.create_view(base_table_name, title, description, report_type, chart_type, axis_columns)
        print(view_id)

obj = sample()
obj.create_visual(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var baseTableName = 'Sales';
var title = 'Sales by Region';
var description = 'Comprehensive analysis of sales metrics across regions';
// Allowed values for reportType: "chart", "pivot", "summary"
var reportType = 'chart';
// Allowed values for chartType: see the supported chart types reference
var chartType = 'bar';
var xAxis = { type: 'xAxis', columnName: 'Region', operation: 'actual' };
var yAxis = { type: 'yAxis', columnName: 'Sales', operation: 'sum' };
var axisColumns = [xAxis, yAxis];
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.createView(baseTableName, title, description, reportType, chartType, axisColumns).then((viewId) => { console.log(viewId); }).catch((error) => { console.log(error); });
```

## Ruby

```ruby
require 'zoho_analytics_client'

class Config
  ORGID = "55522777"
  WORKSPACEID = "35130000001055707"
end

class Sample
  def initialize
    @ac = AnalyticsClient.new.with_data_center("US").with_oauth({
      "clientId" => "1000.xxxxxxx",
      "clientSecret" => "xxxxxxx",
      "refreshToken" => "1000.xxxxxxx.xxxxxxx"
    }).build
  end

  def create_visual
    base_table_name = "Sales"
    title = "Sales by Region"
    description = "Comprehensive analysis of sales metrics across regions"
    # Allowed values for report_type: "chart", "pivot", "summary"
    report_type = "chart"
    # Allowed values for chart_type: see the supported chart types reference
    chart_type = "bar"
    xAxis = { "type" => "xAxis", "columnName" => "Region", "operation" => "actual" }
    yAxis = { "type" => "yAxis", "columnName" => "Sales", "operation" => "sum" }
    axis_columns = [xAxis, yAxis]
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    view_id = workspace.create_view(base_table_name, title, description, report_type, chart_type, axis_columns)
    puts view_id
  end
end

obj = Sample.new
obj.create_visual
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
xAxisCol = Map();
xAxisCol.put("type", "xAxis");
xAxisCol.put("columnName", "Region");
xAxisCol.put("operation", "actual");
yAxisCol = Map();
yAxisCol.put("type", "yAxis");
yAxisCol.put("columnName", "Sales");
yAxisCol.put("operation", "sum");
axisColumns = List();
axisColumns.add(xAxisCol);
axisColumns.add(yAxisCol);
config = Map();
config.put("baseTableName", "Sales");
config.put("title", "Sales by Region");
config.put("description", "Comprehensive analysis of sales metrics across regions");
// Allowed values for reportType: "chart", "pivot", "summary"
config.put("reportType", "chart");
// Allowed values for chartType: see the supported chart types reference
config.put("chartType", "bar");
config.put("axisColumns", axisColumns);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/reports"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Create Report](../../../domains/reports-and-dashboards/reports/create-report.md) - full endpoint reference.
- [Reports (Analysis Views) overview](../../../domains/reports-and-dashboards/reports/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
