---
type: SDK Example
title: SDK examples - Create AutoML Analysis Deployment
description: "Code samples in 9 languages for POST /restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments (createAutoMLAnalysisDeployment)."
resource: "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments"
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
  operation_id: createAutoMLAnalysisDeployment
  method: POST
  path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments"
  endpoint_doc: "/domains/dsml/automl/create-auto-ml-analysis-deployment.md"
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
    resource: "/domains/dsml/automl/create-auto-ml-analysis-deployment.md"
    title: Endpoint reference - Create AutoML Analysis Deployment
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

Code samples for [Create AutoML Analysis Deployment](../../../domains/dsml/automl/create-auto-ml-analysis-deployment.md) (`POST /restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/35130000001055707/analysis/35130000001056701/models/35130000001056801/deployments" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"inputTableId":"35130000001055717","outputTable":"SalesDep","outputColumns":["Revenue","Region"],"predictionColumn":"predicted","serverOption":1,"importType":"APPEND","scheduleDetails":{"calendarFrequency":"hourly","interval":3}}'
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

        public void CreateAutomlAnalysisDeployment(IAnalyticsClient ac)
        {
            long analysisId = 35130000001056701L;
            long modelId = 35130000001056801L;
            long inputTableId = 35130000001055717L;
            List<string> outputColumns = new List<string>{"Revenue","Region"};
            Dictionary<string, object> scheduleDetails = new Dictionary<string, object>{{"calendarFrequency","hourly"},{"interval",3}};
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.CreateAutomlAnalysisDeployment(analysisId, modelId, inputTableId, "SalesDep", outputColumns, "predicted", 1, "APPEND", scheduleDetails, null);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.CreateAutomlAnalysisDeployment(ac);
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

func CreateAutoMLAnalysisDeployment(ac ZAnalytics.Client) {
    analysisID := "35130000001056701"
    modelID := "35130000001056801"
    inputTableID := "35130000001055717"
    outputColumns := []interface{}{"Revenue","Region"}
    scheduleDetails := map[string]interface{}{"calendarFrequency":"hourly","interval":3}
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, ex := workspace.CreateAutoMLAnalysisDeployment(analysisID, modelID, inputTableID, "SalesDep", outputColumns, "predicted", 1, "APPEND", scheduleDetails, nil)
    if ex != nil { fmt.Println(ex.ErrorMessage); return }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateAutoMLAnalysisDeployment(ac)
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
            tObj.createAutoMLAnalysisDeployment(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void createAutoMLAnalysisDeployment(AnalyticsClient ac) throws Exception {
        String analysisId = "35130000001056701";
        String modelId = "35130000001056801";
        String inputTableId = "35130000001055717";
        JSONArray outputColumns = new JSONArray(); outputColumns.put("Revenue"); outputColumns.put("Region");
        JSONObject scheduleDetails = new JSONObject(); scheduleDetails.put("calendarFrequency", "hourly"); scheduleDetails.put("interval", 3);
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.createAutoMLAnalysisDeployment(analysisId, modelId, inputTableId, "SalesDep", outputColumns, "predicted", 1, "APPEND", scheduleDetails, null);
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

    function createAutoMLAnalysisDeployment() {
        $analysis_id = "35130000001056701";
        $model_id = "35130000001056801";
        $input_table_id = "35130000001055717";
        $output_columns = array("Revenue", "Region");
        $schedule_details = array("calendarFrequency" => "hourly", "interval" => 3);
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $response = $workspace->createAutoMLAnalysisDeployment($analysis_id, $model_id, $input_table_id, "SalesDep", $output_columns, "predicted", 1, "APPEND", $schedule_details);
        print_r($response);
    }
}

$obj = new Test();
$obj->createAutoMLAnalysisDeployment();
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

    def create_automl_analysis_deployment(self, ac):
        analysis_id = "35130000001056701"
        model_id = "35130000001056801"
        input_table_id = "35130000001055717"
        output_columns = ["Revenue", "Region"]
        schedule_details = {"calendarFrequency": "hourly", "interval": 3}
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_automl_analysis_deployment(analysis_id, model_id, input_table_id, "SalesDep", output_columns, "predicted", 1, "APPEND", schedule_details)
        print(result)

obj = sample()
obj.create_automl_analysis_deployment(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var analysisId = '35130000001056701';
var modelId = '35130000001056801';
var inputTableId = '35130000001055717';
var outputColumns = ['Revenue','Region'];
var scheduleDetails = { calendarFrequency: 'hourly', interval: 3 };
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.createAutomlAnalysisDeployment(analysisId, modelId, inputTableId, 'SalesDep', outputColumns, 'predicted', 1, 'APPEND', scheduleDetails).then((res)=>console.log(res)).catch((err)=>console.log(err));
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

  def create_automl_analysis_deployment
    analysis_id = "35130000001056701"
    model_id = "35130000001056801"
    input_table_id = "35130000001055717"
    output_columns = ["Revenue", "Region"]
    schedule_details = { "calendarFrequency" => "hourly", "interval" => 3 }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.create_automl_analysis_deployment(analysis_id, model_id, input_table_id, "SalesDep", output_columns, "predicted", 1, "APPEND", schedule_details)
    puts result
  end
end

obj = Sample.new
obj.create_automl_analysis_deployment
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
analysisId = "35130000001056701";
modelId = "35130000001056801";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
outputColumns = List();
outputColumns.add("Revenue");
outputColumns.add("Region");
scheduleDetails = Map();
scheduleDetails.put("calendarFrequency","hourly");
scheduleDetails.put("interval", 3);
config = Map();
config.put("inputTableId","35130000001055717");
config.put("outputTable","SalesDep");
config.put("outputColumns", outputColumns);
config.put("predictionColumn","predicted");
config.put("serverOption", 1);
config.put("importType","APPEND");
config.put("scheduleDetails", scheduleDetails);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/" + workspaceId + "/analysis/" + analysisId + "/models/" + modelId + "/deployments"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Create AutoML Analysis Deployment](../../../domains/dsml/automl/create-auto-ml-analysis-deployment.md) - full endpoint reference.
- [AutoML overview](../../../domains/dsml/automl/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
