---
type: SDK Example
title: SDK examples - Run AutoML Analysis
description: "Code samples in 9 languages for POST /restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}/execute (runAutoMLAnalysis)."
resource: "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}/execute"
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
  operation_id: runAutoMLAnalysis
  method: POST
  path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}/execute"
  endpoint_doc: "/domains/dsml/automl/run-auto-ml-analysis.md"
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
    resource: "/domains/dsml/automl/run-auto-ml-analysis.md"
    title: Endpoint reference - Run AutoML Analysis
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Run AutoML Analysis](../../../domains/dsml/automl/run-auto-ml-analysis.md) (`POST /restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}/execute`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/35130000001055707/analysis/35130000001056701/deployments/35130000001056901/execute" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
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

        public void DeployAutomlAnalysis(IAnalyticsClient ac)
        {
            long analysisId = 35130000001056701L;
            long deploymentId = 35130000001056901L;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.DeployAutomlAnalysis(analysisId, deploymentId, null);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.DeployAutomlAnalysis(ac);
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

func DeployAutoMLAnalysis(ac ZAnalytics.Client) {
    analysisID := "35130000001056701"
    deploymentID := "35130000001056901"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    ex := workspace.DeployAutoMLAnalysis(analysisID, deploymentID, nil)
    if ex != nil { fmt.Println(ex.ErrorMessage); return }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    DeployAutoMLAnalysis(ac)
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
            tObj.runAutoMLAnalysis(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void runAutoMLAnalysis(AnalyticsClient ac) throws Exception {
        String analysisId = "35130000001056701";
        String deploymentId = "35130000001056901";
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.deployAutoMLAnalysis(analysisId, deploymentId, null);
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

    function runAutoMLAnalysis() {
        $analysis_id = "35130000001056701";
        $deployment_id = "35130000001056901";
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->deployAutoMLAnalysis($analysis_id, $deployment_id);
        echo "success\n";
    }
}

$obj = new Test();
$obj->runAutoMLAnalysis();
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

    def run_automl_analysis(self, ac):
        analysis_id = "35130000001056701"
        deployment_id = "35130000001056901"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.deploy_automl_analysis(analysis_id, deployment_id)
        print("success")

obj = sample()
obj.run_automl_analysis(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var analysisId = '35130000001056701';
var deploymentId = '35130000001056901';
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.deployAutomlAnalysis(analysisId, deploymentId).then((res)=>console.log(res)).catch((err)=>console.log(err));
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

  def run_automl_analysis
    analysis_id = "35130000001056701"
    deployment_id = "35130000001056901"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.deploy_automl_analysis(analysis_id, deployment_id)
    puts "success"
  end
end

obj = Sample.new
obj.run_automl_analysis
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/" + workspaceId + "/analysis/35130000001056701/deployments/35130000001056901/execute"
  type :POST
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Run AutoML Analysis](../../../domains/dsml/automl/run-auto-ml-analysis.md) - full endpoint reference.
- [AutoML overview](../../../domains/dsml/automl/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
