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
    last_modified: 2026-10-20T17:34:40Z
  - id: endpoint-doc
    resource: "/domains/reports-and-dashboards/reports/create-report.md"
    title: Endpoint reference - Create Report
generated:
  by: process:build_okf
  at: 2026-10-23T07:58:54Z
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
using System.Text.Json;
using ZohoAnalytics;

namespace ZohoAnalyticsTest
{
    class Program
    {
        long orgId = 55522777;
        long workspaceId = 35130000001055707;

        public void CreateReport(IAnalyticsClient ac)
        {
            Dictionary<string, object> config = JsonSerializer.Deserialize<Dictionary<string, object>>("{\"baseTableName\":\"Sales\",\"title\":\"Sales by Region\",\"description\":\"Comprehensive analysis of sales metrics across regions\",\"reportType\":\"chart\",\"chartType\":\"bar\",\"axisColumns\":[{\"type\":\"xAxis\",\"columnName\":\"Region\",\"operation\":\"actual\"},{\"type\":\"yAxis\",\"columnName\":\"Sales\",\"operation\":\"sum\"}]}");
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            long result = workspace.CreateReport(config);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.CreateReport(ac);
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

func CreateReport(ac ZAnalytics.Client) {
    config := map[string]interface{}{
        "baseTableName": "Sales",
        "title": "Sales by Region",
        "description": "Comprehensive analysis of sales metrics across regions",
        "reportType": "chart",
        "chartType": "bar",
        "axisColumns": []interface{}{
            map[string]interface{}{
                "type": "xAxis",
                "columnName": "Region",
                "operation": "actual",
            },
            map[string]interface{}{
                "type": "yAxis",
                "columnName": "Sales",
                "operation": "sum",
            },
        },
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.CreateReport(config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateReport(ac)
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
            tObj.createReport(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void createReport(AnalyticsClient ac) throws Exception {
        JSONObject config = new JSONObject("{\"baseTableName\":\"Sales\",\"title\":\"Sales by Region\",\"description\":\"Comprehensive analysis of sales metrics across regions\",\"reportType\":\"chart\",\"chartType\":\"bar\",\"axisColumns\":[{\"type\":\"xAxis\",\"columnName\":\"Region\",\"operation\":\"actual\"},{\"type\":\"yAxis\",\"columnName\":\"Sales\",\"operation\":\"sum\"}]}");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        long result = workspace.createReport(config);
        System.out.println(result);
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

    function createReport() {
        $config = array(
            "baseTableName" => "Sales",
            "title" => "Sales by Region",
            "description" => "Comprehensive analysis of sales metrics across regions",
            "reportType" => "chart",
            "chartType" => "bar",
            "axisColumns" => array(
                array(
                    "type" => "xAxis",
                    "columnName" => "Region",
                    "operation" => "actual"
                ),
                array(
                    "type" => "yAxis",
                    "columnName" => "Sales",
                    "operation" => "sum"
                )
            )
        );
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $response = $workspace->createReport($config);
        print_r($response);
    }
}

$obj = new Test();
$obj->createReport();
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

    def create_report(self, ac):
        config = {
            "baseTableName": "Sales",
            "title": "Sales by Region",
            "description": "Comprehensive analysis of sales metrics across regions",
            "reportType": "chart",
            "chartType": "bar",
            "axisColumns": [
                {
                    "type": "xAxis",
                    "columnName": "Region",
                    "operation": "actual"
                },
                {
                    "type": "yAxis",
                    "columnName": "Sales",
                    "operation": "sum"
                }
            ]
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_report(config)
        print(result)

obj = Sample()
obj.create_report(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var config = {
    "baseTableName": "Sales",
    "title": "Sales by Region",
    "description": "Comprehensive analysis of sales metrics across regions",
    "reportType": "chart",
    "chartType": "bar",
    "axisColumns": [
        {
            "type": "xAxis",
            "columnName": "Region",
            "operation": "actual"
        },
        {
            "type": "yAxis",
            "columnName": "Sales",
            "operation": "sum"
        }
    ]
};
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.createReport(config).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def create_report
    config = {
      "baseTableName" => "Sales",
      "title" => "Sales by Region",
      "description" => "Comprehensive analysis of sales metrics across regions",
      "reportType" => "chart",
      "chartType" => "bar",
      "axisColumns" => [
        {
          "type" => "xAxis",
          "columnName" => "Region",
          "operation" => "actual"
        },
        {
          "type" => "yAxis",
          "columnName" => "Sales",
          "operation" => "sum"
        }
      ]
    }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.create_report(config)
    puts result
  end
end

obj = Sample.new
obj.create_report
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
