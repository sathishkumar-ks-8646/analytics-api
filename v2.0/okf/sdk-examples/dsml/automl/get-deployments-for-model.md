---
type: SDK Example
title: SDK examples - Get Deployments For A Model
description: "Code samples in 9 languages for GET /restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments (getDeploymentsForModel)."
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
  operation_id: getDeploymentsForModel
  method: GET
  path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments"
  endpoint_doc: "/domains/dsml/automl/get-deployments-for-model.md"
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
    resource: "/domains/dsml/automl/get-deployments-for-model.md"
    title: Endpoint reference - Get Deployments For A Model
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Get Deployments For A Model](../../../domains/dsml/automl/get-deployments-for-model.md) (`GET /restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/35130000001055707/analysis/35130000001056701/models/35130000001056801/deployments" -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
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

        public void GetDeploymentDetails(IAnalyticsClient ac)
        {
            long analysisId = 35130000001056701L;
            long modelId = 35130000001056801L;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetDeploymentDetails(analysisId, modelId);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.GetDeploymentDetails(ac);
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

func GetDeploymentDetails(ac ZAnalytics.Client) {
    analysisID := "35130000001056701"
    modelID := "35130000001056801"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, ex := workspace.GetDeploymentDetails(analysisID, modelID)
    if ex != nil { fmt.Println(ex.ErrorMessage); return }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetDeploymentDetails(ac)
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
            tObj.getDeploymentsForModel(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void getDeploymentsForModel(AnalyticsClient ac) throws Exception {
        String analysisId = "35130000001056701";
        String modelId = "35130000001056801";
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getDeploymentDetails(analysisId, modelId);
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

    function getDeploymentsForModel() {
        $analysis_id = "35130000001056701";
        $model_id = "35130000001056801";
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $response = $workspace->getDeploymentDetails($analysis_id, $model_id);
        print_r($response);
    }
}

$obj = new Test();
$obj->getDeploymentsForModel();
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

    def get_deployments_for_model(self, ac):
        analysis_id = "35130000001056701"
        model_id = "35130000001056801"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_deployment_details(analysis_id, model_id)
        print(result)

obj = sample()
obj.get_deployments_for_model(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var analysisId = '35130000001056701';
var modelId = '35130000001056801';
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.getDeploymentDetails(analysisId, modelId).then((res)=>console.log(res)).catch((err)=>console.log(err));
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

  def get_deployments_for_model
    analysis_id = "35130000001056701"
    model_id = "35130000001056801"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_deployment_details(analysis_id, model_id)
    puts result
  end
end

obj = Sample.new
obj.get_deployments_for_model
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/" + workspaceId + "/analysis/35130000001056701/models/35130000001056801/deployments"
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Deployments For A Model](../../../domains/dsml/automl/get-deployments-for-model.md) - full endpoint reference.
- [AutoML overview](../../../domains/dsml/automl/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
