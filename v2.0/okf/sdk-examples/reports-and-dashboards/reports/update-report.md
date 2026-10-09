---
type: SDK Example
title: SDK examples - Update Analysis View
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id}/reports/{view-id} (updateReport)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/reports/{view-id}"
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
  operation_id: updateReport
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/reports/{view-id}"
  endpoint_doc: "/domains/reports-and-dashboards/reports/update-report.md"
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
    last_modified: 2026-10-09T08:29:02Z
  - id: endpoint-doc
    resource: "/domains/reports-and-dashboards/reports/update-report.md"
    title: Endpoint reference - Update Analysis View
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Update Analysis View](../../../domains/reports-and-dashboards/reports/update-report.md) (`PUT /restapi/v2/workspaces/{workspace-id}/reports/{view-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/reports/35130000001055901" -X 'PUT' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"title":"Sales Trend by Region","reportType":"chart","chartType":"line","axisColumns":[{"type":"xAxis","columnName":"Date","operation":"year"},{"type":"yAxis","columnName":"Sales","operation":"sum"}]}'
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

        public void UpdateVisual(IAnalyticsClient ac)
        {
            long viewId = 35130000001055901;
            string title = "Sales Trend by Region";
            // Allowed values for reportType: "chart", "pivot", "summary"
            string reportType = "chart";
            // Allowed values for chartType: see the supported chart types reference
            string chartType = "line";
            List<Dictionary<string, object>> axisColumns = new List<Dictionary<string, object>>();
            axisColumns.Add(new Dictionary<string, object>{{"type","xAxis"},{"columnName","Date"},{"operation","year"}});
            axisColumns.Add(new Dictionary<string, object>{{"type","yAxis"},{"columnName","Sales"},{"operation","sum"}});
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.UpdateView(title, reportType, chartType, axisColumns, null, null);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.UpdateVisual(ac);
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

func UpdateVisual(ac ZAnalytics.Client) {
    viewId := "35130000001055901"
    title := "Sales Trend by Region"
    // Allowed values for reportType: "chart", "pivot", "summary"
    reportType := "chart"
    // Allowed values for chartType: see the supported chart types reference
    chartType := "line"
    xAxis := map[string]interface{}{"type": "xAxis", "columnName": "Date", "operation": "year"}
    yAxis := map[string]interface{}{"type": "yAxis", "columnName": "Sales", "operation": "sum"}
    axisColumns := []map[string]interface{}{xAxis, yAxis}
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    exception := view.UpdateView(title, reportType, chartType, axisColumns, nil, nil)
    if exception != nil { fmt.Println(exception.ErrorMessage); return }
    fmt.Println("Success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    UpdateVisual(ac)
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
            tObj.updateVisual(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void updateVisual(AnalyticsClient ac) throws Exception {
        long viewId = 35130000001055901l;
        String title = "Sales Trend by Region";
        // Allowed values for reportType: "chart", "pivot", "summary"
        String reportType = "chart";
        // Allowed values for chartType: see the supported chart types reference
        String chartType = "line";
        JSONObject xAxis = new JSONObject();
        xAxis.put("type", "xAxis");
        xAxis.put("columnName", "Date");
        xAxis.put("operation", "year");
        JSONObject yAxis = new JSONObject();
        yAxis.put("type", "yAxis");
        yAxis.put("columnName", "Sales");
        yAxis.put("operation", "sum");
        JSONArray axisColumns = new JSONArray();
        axisColumns.put(xAxis);
        axisColumns.put(yAxis);
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.updateView(title, reportType, chartType, axisColumns, null, null);
        System.out.println("success");
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

    function updateVisual() {
        $view_id = "35130000001055901";
        $title = "Sales Trend by Region";
        // Allowed values for $report_type: "chart", "pivot", "summary"
        $report_type = "chart";
        // Allowed values for $chart_type: see the supported chart types reference
        $chart_type = "line";
        $x_axis = ["type" => "xAxis", "columnName" => "Date", "operation" => "year"];
        $y_axis = ["type" => "yAxis", "columnName" => "Sales", "operation" => "sum"];
        $axis_columns = [$x_axis, $y_axis];
        $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $view_id);
        $view->updateView($title, $report_type, $chart_type, $axis_columns);
        echo "success";
    }
}

$obj = new Test();
$obj->updateVisual();
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

    def update_visual(self, ac):
        view_id = "35130000001055901"
        title = "Sales Trend by Region"
        # Allowed values for report_type: "chart", "pivot", "summary"
        report_type = "chart"
        # Allowed values for chart_type: see the supported chart types reference
        chart_type = "line"
        xAxis = {"type": "xAxis", "columnName": "Date", "operation": "year"}
        yAxis = {"type": "yAxis", "columnName": "Sales", "operation": "sum"}
        axis_columns = [xAxis, yAxis]
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, view_id)
        view.update_view(title, report_type, chart_type, axis_columns)
        print("success")

obj = sample()
obj.update_visual(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var viewId = '35130000001055901';
var title = 'Sales Trend by Region';
// Allowed values for reportType: "chart", "pivot", "summary"
var reportType = 'chart';
// Allowed values for chartType: see the supported chart types reference
var chartType = 'line';
var xAxis = { type: 'xAxis', columnName: 'Date', operation: 'year' };
var yAxis = { type: 'yAxis', columnName: 'Sales', operation: 'sum' };
var axisColumns = [xAxis, yAxis];
var view = ac.getViewInstance(orgId, workspaceId, viewId);
view.updateView(title, reportType, chartType, axisColumns).then(() => { console.log('success'); }).catch((error) => { console.log(error); });
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

  def update_visual
    view_id = "35130000001055901"
    title = "Sales Trend by Region"
    # Allowed values for report_type: "chart", "pivot", "summary"
    report_type = "chart"
    # Allowed values for chart_type: see the supported chart types reference
    chart_type = "line"
    xAxis = { "type" => "xAxis", "columnName" => "Date", "operation" => "year" }
    yAxis = { "type" => "yAxis", "columnName" => "Sales", "operation" => "sum" }
    axis_columns = [xAxis, yAxis]
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, view_id)
    view.update_view(title, report_type, chart_type, axis_columns)
    puts "success"
  end
end

obj = Sample.new
obj.update_visual
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
viewId = "35130000001055901";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
xAxisCol = Map();
xAxisCol.put("type", "xAxis");
xAxisCol.put("columnName", "Date");
xAxisCol.put("operation", "year");
yAxisCol = Map();
yAxisCol.put("type", "yAxis");
yAxisCol.put("columnName", "Sales");
yAxisCol.put("operation", "sum");
axisColumns = List();
axisColumns.add(xAxisCol);
axisColumns.add(yAxisCol);
config = Map();
config.put("title", "Sales Trend by Region");
// Allowed values for reportType: "chart", "pivot", "summary"
config.put("reportType", "chart");
// Allowed values for chartType: see the supported chart types reference
config.put("chartType", "line");
config.put("axisColumns", axisColumns);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/reports/" + viewId
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Update Analysis View](../../../domains/reports-and-dashboards/reports/update-report.md) - full endpoint reference.
- [Reports (Analysis Views) overview](../../../domains/reports-and-dashboards/reports/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
