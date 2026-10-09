---
type: SDK Example
title: SDK examples - Get AutoML Analysis In Workspace
description: "Code samples in 9 languages for GET /restapi/v2/automl/workspaces/{workspace-id}/analysis (getAutoMLAnalysisInWorkspace)."
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
  operation_id: getAutoMLAnalysisInWorkspace
  method: GET
  path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis"
  endpoint_doc: "/domains/dsml/automl/get-auto-ml-analysis-in-workspace.md"
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
    resource: "/domains/dsml/automl/get-auto-ml-analysis-in-workspace.md"
    title: Endpoint reference - Get AutoML Analysis In Workspace
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Get AutoML Analysis In Workspace](../../../domains/dsml/automl/get-auto-ml-analysis-in-workspace.md) (`GET /restapi/v2/automl/workspaces/{workspace-id}/analysis`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/35130000001055707/analysis" -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
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

        public void GetAutomlAnalysisInWorkspace(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetAutomlAnalysis();
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.GetAutomlAnalysisInWorkspace(ac);
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

func GetAutoMLAnalysisInWorkspace(ac ZAnalytics.Client) {
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, ex := workspace.GetAutoMLAnalysis()
    if ex != nil { fmt.Println(ex.ErrorMessage); return }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetAutoMLAnalysisInWorkspace(ac)
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
            tObj.getAutoMLAnalysisInWorkspace(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void getAutoMLAnalysisInWorkspace(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getAutoMLAnalysis();
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

    function getAutoMLAnalysisInWorkspace() {
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $response = $workspace->getAutoMLAnalysis();
        print_r($response);
    }
}

$obj = new Test();
$obj->getAutoMLAnalysisInWorkspace();
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

    def get_automl_analysis_in_workspace(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_automl_analysis()
        print(result)

obj = sample()
obj.get_automl_analysis_in_workspace(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.getAutomlAnalysis().then((res)=>console.log(res)).catch((err)=>console.log(err));
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

  def get_automl_analysis_in_workspace
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_automl_analysis
    puts result
  end
end

obj = Sample.new
obj.get_automl_analysis_in_workspace
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/" + workspaceId + "/analysis"
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get AutoML Analysis In Workspace](../../../domains/dsml/automl/get-auto-ml-analysis-in-workspace.md) - full endpoint reference.
- [AutoML overview](../../../domains/dsml/automl/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
