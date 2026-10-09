---
type: SDK Example
title: SDK examples - Create AutoML Analysis
description: "Code samples in 9 languages for POST /restapi/v2/automl/workspaces/{workspace-id}/analysis (createAutoMLAnalysis)."
resource: "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/{workspace-id}/analysis"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - dsml
  - automl
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
  operation_id: createAutoMLAnalysis
  method: POST
  path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis"
  endpoint_doc: "/domains/dsml/automl/create-auto-ml-analysis.md"
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
    resource: "/references/openapi/dsml-grouped-api.json"
    title: OpenAPI 3 specification - dsml-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
  - id: endpoint-doc
    resource: "/domains/dsml/automl/create-auto-ml-analysis.md"
    title: Endpoint reference - Create AutoML Analysis
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Create AutoML Analysis](../../../domains/dsml/automl/create-auto-ml-analysis.md) (`POST /restapi/v2/automl/workspaces/{workspace-id}/analysis`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/35130000001055707/analysis" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"name":"Sales_Forecast","description":"Sales Forecast","trainingTableId":"35130000001055717","targetColumn":"Revenue","predictionType":"CLASSIFICATION","features":["Region","Quarter"],"serverOption":1,"algorithms":{"decisionTreeClassification":{"minimumSampleSplit":"2","maximumDepth":"20"}}}'
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

        public void CreateAutomlAnalysis(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            long trainingTableId = 35130000001055717L;
            List<string> features = new List<string>{"Region","Quarter"};
            Dictionary<string, object> algorithms = new Dictionary<string, object>{
                {"decisionTreeClassification", new Dictionary<string, object>{{"minimumSampleSplit","2"},{"maximumDepth","20"}}}
            };
            Dictionary<string, object> config = new Dictionary<string, object>{{"description","Sales Forecast"},{"targetColumn","Revenue"}};
            long result = workspace.CreateAutomlAnalysis("Sales_Forecast", trainingTableId, "CLASSIFICATION", features, 1, algorithms, config);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.CreateAutomlAnalysis(ac);
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

func CreateAutoMLAnalysis(ac ZAnalytics.Client) {
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    trainingTableID := "35130000001055717"
    features := []interface{}{"Region","Quarter"}
    algorithms := map[string]interface{}{
        "decisionTreeClassification": map[string]interface{}{"minimumSampleSplit":"2","maximumDepth":"20"},
    }
    config := map[string]interface{}{"description":"Sales Forecast","targetColumn":"Revenue"}
    result, ex := workspace.CreateAutoMLAnalysis("Sales_Forecast", trainingTableID, "CLASSIFICATION", features, 1, algorithms, config)
    if ex != nil { fmt.Println(ex.ErrorMessage); return }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateAutoMLAnalysis(ac)
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
            tObj.createAutoMLAnalysis(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void createAutoMLAnalysis(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        String trainingTableId = "35130000001055717";
        JSONArray features = new JSONArray();
        features.put("Region");
        features.put("Quarter");
        JSONObject algorithms = new JSONObject();
        JSONObject dt = new JSONObject();
        dt.put("minimumSampleSplit", "2");
        dt.put("maximumDepth", "20");
        algorithms.put("decisionTreeClassification", dt);
        JSONObject config = new JSONObject();
        config.put("description", "Sales Forecast");
        config.put("targetColumn", "Revenue");
        String result = workspace.createAutoMLAnalysis("Sales_Forecast", trainingTableId, "CLASSIFICATION", features, 1, algorithms, config);
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

    function createAutoMLAnalysis() {
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $training_table_id = "35130000001055717";
        $features = array("Region", "Quarter");
        $algorithms = array("decisionTreeClassification" => array("minimumSampleSplit" => "2", "maximumDepth" => "20"));
        $config = array("description" => "Sales Forecast", "targetColumn" => "Revenue");
        $result = $workspace->createAutoMLAnalysis("Sales_Forecast", $training_table_id, "CLASSIFICATION", $features, 1, $algorithms, $config);
        print_r($result);
    }
}

$obj = new Test();
$obj->createAutoMLAnalysis();
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

    def create_automl_analysis(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        training_table_id = "35130000001055717"
        features = ["Region", "Quarter"]
        algorithms = {"decisionTreeClassification": {"minimumSampleSplit": "2", "maximumDepth": "20"}}
        config = {"description": "Sales Forecast", "targetColumn": "Revenue"}
        result = workspace.create_automl_analysis("Sales_Forecast", training_table_id, "CLASSIFICATION", features, 1, algorithms, config)
        print(result)

obj = sample()
obj.create_automl_analysis(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var trainingTableId = '35130000001055717';
var features = ['Region','Quarter'];
var algorithms = { decisionTreeClassification: { minimumSampleSplit: '2', maximumDepth: '20' } };
var config = { description: 'Sales Forecast', targetColumn: 'Revenue' };
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.createAutomlAnalysis('Sales_Forecast', trainingTableId, 'CLASSIFICATION', features, 1, algorithms, config).then((res)=>{
  console.log(res);
}).catch((err)=>{ console.log(err); });
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

  def create_automl_analysis
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    training_table_id = "35130000001055717"
    features = ["Region", "Quarter"]
    algorithms = { "decisionTreeClassification" => { "minimumSampleSplit" => "2", "maximumDepth" => "20" } }
    config = { "description" => "Sales Forecast", "targetColumn" => "Revenue" }
    result = workspace.create_automl_analysis("Sales_Forecast", training_table_id, "CLASSIFICATION", features, 1, algorithms, config)
    puts result
  end
end

obj = Sample.new
obj.create_automl_analysis
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
features = List();
features.add("Region");
features.add("Quarter");
decisionTree = Map();
decisionTree.put("minimumSampleSplit","2");
decisionTree.put("maximumDepth","20");
algorithms = Map();
algorithms.put("decisionTreeClassification", decisionTree);
config = Map();
config.put("name","Sales_Forecast");
config.put("description","Sales Forecast");
config.put("trainingTableId","35130000001055717");
config.put("targetColumn","Revenue");
config.put("predictionType","CLASSIFICATION");
config.put("features", features);
config.put("serverOption", 1);
config.put("algorithms", algorithms);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/" + workspaceId + "/analysis"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Create AutoML Analysis](../../../domains/dsml/automl/create-auto-ml-analysis.md) - full endpoint reference.
- [AutoML overview](../../../domains/dsml/automl/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
