---
type: SDK Example
title: SDK examples - Delete AutoML Analysis Model
description: "Code samples in 9 languages for DELETE /restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id} (deleteAutoMLAnalysisModel)."
resource: "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}"
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
  operation_id: deleteAutoMLAnalysisModel
  method: DELETE
  path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}"
  endpoint_doc: "/domains/dsml/automl/delete-auto-ml-analysis-model.md"
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
    resource: "/domains/dsml/automl/delete-auto-ml-analysis-model.md"
    title: Endpoint reference - Delete AutoML Analysis Model
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

Code samples for [Delete AutoML Analysis Model](../../../domains/dsml/automl/delete-auto-ml-analysis-model.md) (`DELETE /restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/35130000001055707/analysis/35130000001056701/models/35130000001056801" -X 'DELETE' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
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

        public void DeleteAutomlAnalysisModel(IAnalyticsClient ac)
        {
            long analysisId = 35130000001056701L;
            long modelId = 35130000001056801L;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.DeleteAutomlAnalysisModel(analysisId, modelId, null);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.DeleteAutomlAnalysisModel(ac);
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

func DeleteAutoMLAnalysisModel(ac ZAnalytics.Client) {
    analysisID := "35130000001056701"
    modelID := "35130000001056801"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    ex := workspace.DeleteAutoMLAnalysisModel(analysisID, modelID, nil)
    if ex != nil { fmt.Println(ex.ErrorMessage); return }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    DeleteAutoMLAnalysisModel(ac)
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
            tObj.deleteAutoMLAnalysisModel(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void deleteAutoMLAnalysisModel(AnalyticsClient ac) throws Exception {
        String analysisId = "35130000001056701";
        String modelId = "35130000001056801";
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.deleteAutoMLAnalysisModel(analysisId, modelId, null);
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

    function deleteAutoMLAnalysisModel() {
        $analysis_id = "35130000001056701";
        $model_id = "35130000001056801";
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->deleteAutoMLAnalysisModel($analysis_id, $model_id);
        echo "success\n";
    }
}

$obj = new Test();
$obj->deleteAutoMLAnalysisModel();
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

    def delete_automl_analysis_model(self, ac):
        analysis_id = "35130000001056701"
        model_id = "35130000001056801"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.delete_automl_analysis_model(analysis_id, model_id)
        print("success")

obj = sample()
obj.delete_automl_analysis_model(obj.ac)
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
workspace.deleteAutomlAnalysisModel(analysisId, modelId).then((res)=>console.log(res)).catch((err)=>console.log(err));
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

  def delete_automl_analysis_model
    analysis_id = "35130000001056701"
    model_id = "35130000001056801"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.delete_automl_analysis_model(analysis_id, model_id)
    puts "success"
  end
end

obj = Sample.new
obj.delete_automl_analysis_model
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/" + workspaceId + "/analysis/35130000001056701/models/35130000001056801"
  type :DELETE
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Delete AutoML Analysis Model](../../../domains/dsml/automl/delete-auto-ml-analysis-model.md) - full endpoint reference.
- [AutoML overview](../../../domains/dsml/automl/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
