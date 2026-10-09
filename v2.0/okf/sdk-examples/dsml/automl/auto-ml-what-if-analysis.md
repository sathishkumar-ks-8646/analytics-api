---
type: SDK Example
title: SDK examples - AutoML What If Analysis
description: "Code samples in 9 languages for POST /restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/whatif (autoMLWhatIfAnalysis)."
resource: "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/whatif"
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
  operation_id: autoMLWhatIfAnalysis
  method: POST
  path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/whatif"
  endpoint_doc: "/domains/dsml/automl/auto-ml-what-if-analysis.md"
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
    last_modified: 2026-10-09T14:14:03Z
  - id: endpoint-doc
    resource: "/domains/dsml/automl/auto-ml-what-if-analysis.md"
    title: Endpoint reference - AutoML What If Analysis
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

Code samples for [AutoML What If Analysis](../../../domains/dsml/automl/auto-ml-what-if-analysis.md) (`POST /restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/whatif`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/35130000001055707/analysis/35130000001056701/models/35130000001056801/whatif" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"features":{"Region":"East","Quarter":"Q2"}}'
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

        public void AutomlAnalysisPrediction(IAnalyticsClient ac)
        {
            long analysisId = 35130000001056701L;
            long modelId = 35130000001056801L;
            Dictionary<string, object> features = new Dictionary<string, object>{{"Region","East"},{"Quarter","Q2"}};
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.AutomlAnalysisPrediction(analysisId, modelId, features, null);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.AutomlAnalysisPrediction(ac);
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

func AutoMLWhatIfAnalysis(ac ZAnalytics.Client) {
    analysisID := "35130000001056701"
    modelID := "35130000001056801"
    features := map[string]interface{}{"Region":"East","Quarter":"Q2"}
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, ex := workspace.AutoMLAnalysisPrediction(analysisID, modelID, features, nil)
    if ex != nil { fmt.Println(ex.ErrorMessage); return }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    AutoMLWhatIfAnalysis(ac)
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
            tObj.autoMLWhatIfAnalysis(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void autoMLWhatIfAnalysis(AnalyticsClient ac) throws Exception {
        String analysisId = "35130000001056701";
        String modelId = "35130000001056801";
        JSONObject features = new JSONObject();
        features.put("Region", "East");
        features.put("Quarter", "Q2");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.autoMLAnalysisPrediction(analysisId, modelId, features, null);
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

    function autoMLWhatIfAnalysis() {
        $analysis_id = "35130000001056701";
        $model_id = "35130000001056801";
        $features = array("Region" => "East", "Quarter" => "Q2");
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $response = $workspace->autoMLAnalysisPrediction($analysis_id, $model_id, $features);
        print_r($response);
    }
}

$obj = new Test();
$obj->autoMLWhatIfAnalysis();
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

    def automl_what_if_analysis(self, ac):
        analysis_id = "35130000001056701"
        model_id = "35130000001056801"
        features = {"Region": "East", "Quarter": "Q2"}
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.automl_analysis_prediction(analysis_id, model_id, features)
        print(result)

obj = sample()
obj.automl_what_if_analysis(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var analysisId = '35130000001056701';
var modelId = '35130000001056801';
var features = { Region: 'East', Quarter: 'Q2' };
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.automlAnalysisPrediction(analysisId, modelId, features).then((res)=>console.log(res)).catch((err)=>console.log(err));
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

  def automl_what_if_analysis
    analysis_id = "35130000001056701"
    model_id = "35130000001056801"
    features = { "Region" => "East", "Quarter" => "Q2" }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.automl_analysis_prediction(analysis_id, model_id, features)
    puts result
  end
end

obj = Sample.new
obj.automl_what_if_analysis
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
analysisId = "35130000001056701";
modelId = "35130000001056801";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
features = Map();
features.put("Region","East");
features.put("Quarter","Q2");
config = Map();
config.put("features", features);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/" + workspaceId + "/analysis/" + analysisId + "/models/" + modelId + "/whatif"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [AutoML What If Analysis](../../../domains/dsml/automl/auto-ml-what-if-analysis.md) - full endpoint reference.
- [AutoML overview](../../../domains/dsml/automl/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
