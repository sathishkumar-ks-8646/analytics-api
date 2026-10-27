---
type: SDK Example
title: SDK examples - Update Report
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
    last_modified: 2026-10-26T11:33:28Z
  - id: endpoint-doc
    resource: "/domains/reports-and-dashboards/reports/update-report.md"
    title: Endpoint reference - Update Report
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

Code samples for [Update Report](../../../domains/reports-and-dashboards/reports/update-report.md) (`PUT /restapi/v2/workspaces/{workspace-id}/reports/{view-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/reports/35130000001055901" -X 'PUT' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"title":"Sales Trend by Region","reportType":"chart","chartType":"line","axisColumns":[{"type":"xAxis","columnName":"Date","operation":"year"},{"type":"yAxis","columnName":"Sales","operation":"sum"}]}'
```

## C#

```csharp
using System;
using System.Collections.Generic;
using System.Text.Json;
using ZohoAnalytics;

namespace ZohoAnalyticsTest
{
    class Program
    {
        long orgId = 55522777;
        long workspaceId = 35130000001055707;

        public void UpdateReport(IAnalyticsClient ac)
        {
            long viewId = 35130000001055901L;
            Dictionary<string, object> config = JsonSerializer.Deserialize<Dictionary<string, object>>("{\"title\":\"Sales Trend by Region\",\"reportType\":\"chart\",\"chartType\":\"line\",\"axisColumns\":[{\"type\":\"xAxis\",\"columnName\":\"Date\",\"operation\":\"year\"},{\"type\":\"yAxis\",\"columnName\":\"Sales\",\"operation\":\"sum\"}]}");
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.UpdateReport(viewId, config);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.UpdateReport(ac);
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

func UpdateReport(ac ZAnalytics.Client) {
    viewid := "35130000001055901"
    config := map[string]interface{}{
        "title": "Sales Trend by Region",
        "reportType": "chart",
        "chartType": "line",
        "axisColumns": []interface{}{
            map[string]interface{}{
                "type": "xAxis",
                "columnName": "Date",
                "operation": "year",
            },
            map[string]interface{}{
                "type": "yAxis",
                "columnName": "Sales",
                "operation": "sum",
            },
        },
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    exception := workspace.UpdateReport(viewid, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    UpdateReport(ac)
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
            tObj.updateReport(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void updateReport(AnalyticsClient ac) throws Exception {
        long viewId = 35130000001055901l;
        JSONObject config = new JSONObject("{\"title\":\"Sales Trend by Region\",\"reportType\":\"chart\",\"chartType\":\"line\",\"axisColumns\":[{\"type\":\"xAxis\",\"columnName\":\"Date\",\"operation\":\"year\"},{\"type\":\"yAxis\",\"columnName\":\"Sales\",\"operation\":\"sum\"}]}");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.updateReport(viewId, config);
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

    function updateReport() {
        $view_id = "35130000001055901";
        $config = array(
            "title" => "Sales Trend by Region",
            "reportType" => "chart",
            "chartType" => "line",
            "axisColumns" => array(
                array(
                    "type" => "xAxis",
                    "columnName" => "Date",
                    "operation" => "year"
                ),
                array(
                    "type" => "yAxis",
                    "columnName" => "Sales",
                    "operation" => "sum"
                )
            )
        );
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->updateReport($view_id, $config);
        echo "success";
    }
}

$obj = new Test();
$obj->updateReport();
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

class Sample:
    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def update_report(self, ac):
        view_id = "35130000001055901"
        config = {
            "title": "Sales Trend by Region",
            "reportType": "chart",
            "chartType": "line",
            "axisColumns": [
                {
                    "type": "xAxis",
                    "columnName": "Date",
                    "operation": "year"
                },
                {
                    "type": "yAxis",
                    "columnName": "Sales",
                    "operation": "sum"
                }
            ]
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.update_report(view_id, config)
        print("success")

obj = Sample()
obj.update_report(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var viewId = "35130000001055901";
var config = {
    "title": "Sales Trend by Region",
    "reportType": "chart",
    "chartType": "line",
    "axisColumns": [
        {
            "type": "xAxis",
            "columnName": "Date",
            "operation": "year"
        },
        {
            "type": "yAxis",
            "columnName": "Sales",
            "operation": "sum"
        }
    ]
};
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.updateReport(viewId, config).then(() => { console.log("success"); }).catch((error) => { console.log(error); });
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

  def update_report
    view_id = "35130000001055901"
    config = {
      "title" => "Sales Trend by Region",
      "reportType" => "chart",
      "chartType" => "line",
      "axisColumns" => [
        {
          "type" => "xAxis",
          "columnName" => "Date",
          "operation" => "year"
        },
        {
          "type" => "yAxis",
          "columnName" => "Sales",
          "operation" => "sum"
        }
      ]
    }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.update_report(view_id, config)
    puts "success"
  end
end

obj = Sample.new
obj.update_report
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

- [Update Report](../../../domains/reports-and-dashboards/reports/update-report.md) - full endpoint reference.
- [Reports (Analysis Views) overview](../../../domains/reports-and-dashboards/reports/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
