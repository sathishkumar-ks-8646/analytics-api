---
type: SDK Example
title: SDK examples - Delete AutoML Analysis Model Deployment
description: "Code samples in 9 languages for DELETE /restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id} (deleteAutoMLAnalysisModelDeployment)."
resource: "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}"
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
  operation_id: deleteAutoMLAnalysisModelDeployment
  method: DELETE
  path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}"
  endpoint_doc: "/domains/dsml/automl/delete-auto-ml-analysis-model-deployment.md"
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
    resource: "/domains/dsml/automl/delete-auto-ml-analysis-model-deployment.md"
    title: Endpoint reference - Delete AutoML Analysis Model Deployment
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

Code samples for [Delete AutoML Analysis Model Deployment](../../../domains/dsml/automl/delete-auto-ml-analysis-model-deployment.md) (`DELETE /restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/deployments/{deployment-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/35130000001055707/analysis/35130000001056701/deployments/35130000001056901" -X 'DELETE' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
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

        public void DeleteAutomlAnalysisDeployment(IAnalyticsClient ac)
        {
            long analysisId = 35130000001056701L;
            long deploymentId = 35130000001056901L;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.DeleteAutomlAnalysisDeployment(analysisId, deploymentId, null);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.DeleteAutomlAnalysisDeployment(ac);
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

func DeleteAutoMLAnalysisDeployment(ac ZAnalytics.Client) {
    analysisID := "35130000001056701"
    deploymentID := "35130000001056901"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    ex := workspace.DeleteAutoMLAnalysisDeployment(analysisID, deploymentID, nil)
    if ex != nil { fmt.Println(ex.ErrorMessage); return }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    DeleteAutoMLAnalysisDeployment(ac)
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
            tObj.deleteAutoMLAnalysisModelDeployment(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void deleteAutoMLAnalysisModelDeployment(AnalyticsClient ac) throws Exception {
        String analysisId = "35130000001056701";
        String deploymentId = "35130000001056901";
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.deleteAutoMLAnalysisDeployment(analysisId, deploymentId, null);
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

    function deleteAutoMLAnalysisModelDeployment() {
        $analysis_id = "35130000001056701";
        $deployment_id = "35130000001056901";
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->deleteAutoMLAnalysisDeployment($analysis_id, $deployment_id);
        echo "success\n";
    }
}

$obj = new Test();
$obj->deleteAutoMLAnalysisModelDeployment();
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

    def delete_automl_analysis_model_deployment(self, ac):
        analysis_id = "35130000001056701"
        deployment_id = "35130000001056901"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.delete_automl_analysis_deployment(analysis_id, deployment_id)
        print("success")

obj = sample()
obj.delete_automl_analysis_model_deployment(obj.ac)
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
workspace.deleteAutomlAnalysisDeployment(analysisId, deploymentId).then((res)=>console.log(res)).catch((err)=>console.log(err));
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

  def delete_automl_analysis_model_deployment
    analysis_id = "35130000001056701"
    deployment_id = "35130000001056901"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.delete_automl_analysis_deployment(analysis_id, deployment_id)
    puts "success"
  end
end

obj = Sample.new
obj.delete_automl_analysis_model_deployment
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/" + workspaceId + "/analysis/35130000001056701/deployments/35130000001056901"
  type :DELETE
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Delete AutoML Analysis Model Deployment](../../../domains/dsml/automl/delete-auto-ml-analysis-model-deployment.md) - full endpoint reference.
- [AutoML overview](../../../domains/dsml/automl/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
