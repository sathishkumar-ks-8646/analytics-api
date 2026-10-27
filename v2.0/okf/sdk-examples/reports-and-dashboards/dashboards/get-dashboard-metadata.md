---
type: SDK Example
title: SDK examples - Read Dashboard Metadata
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}/metadata (getDashboardMetadata)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}/metadata"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - reports-and-dashboards
  - dashboards
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
  operation_id: getDashboardMetadata
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}/metadata"
  endpoint_doc: "/domains/reports-and-dashboards/dashboards/get-dashboard-metadata.md"
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
    resource: "/domains/reports-and-dashboards/dashboards/get-dashboard-metadata.md"
    title: Endpoint reference - Read Dashboard Metadata
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

Code samples for [Read Dashboard Metadata](../../../domains/reports-and-dashboards/dashboards/get-dashboard-metadata.md) (`GET /restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}/metadata`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl -G "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/dashboards/35130000001055801/metadata" --data-urlencode 'CONFIG={"include":"layout"}' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
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

        public void GetDashboardMetadata(IAnalyticsClient ac)
        {
            long dashboardId = 35130000001055801L;
            Dictionary<string, object> config = JsonSerializer.Deserialize<Dictionary<string, object>>("{\"include\":\"layout\"}");
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetDashboardMetadata(dashboardId, config);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.GetDashboardMetadata(ac);
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

func GetDashboardMetadata(ac ZAnalytics.Client) {
    dashboardid := "35130000001055801"
    config := map[string]interface{}{
        "include": "layout",
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.GetDashboardMetadata(dashboardid, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetDashboardMetadata(ac)
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
            tObj.getDashboardMetadata(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void getDashboardMetadata(AnalyticsClient ac) throws Exception {
        long dashboardId = 35130000001055801l;
        JSONObject config = new JSONObject("{\"include\":\"layout\"}");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getDashboardMetadata(dashboardId, config);
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

    function getDashboardMetadata() {
        $dashboard_id = "35130000001055801";
        $config = array(
            "include" => "layout"
        );
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $response = $workspace->getDashboardMetadata($dashboard_id, $config);
        print_r($response);
    }
}

$obj = new Test();
$obj->getDashboardMetadata();
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

    def get_dashboard_metadata(self, ac):
        dashboard_id = "35130000001055801"
        config = {
            "include": "layout"
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_dashboard_metadata(dashboard_id, config)
        print(result)

obj = Sample()
obj.get_dashboard_metadata(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var dashboardId = "35130000001055801";
var config = {
    "include": "layout"
};
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.getDashboardMetadata(dashboardId, config).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def get_dashboard_metadata
    dashboard_id = "35130000001055801"
    config = {
      "include" => "layout"
    }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_dashboard_metadata(dashboard_id, config)
    puts result
  end
end

obj = Sample.new
obj.get_dashboard_metadata
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
dashboardId = "35130000001055801";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
// Omit CONFIG to return every section; include names exactly one of all, layout, themes, settings
config = Map();
config.put("include", "layout");
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/dashboards/" + dashboardId + "/metadata?" + parameters
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Read Dashboard Metadata](../../../domains/reports-and-dashboards/dashboards/get-dashboard-metadata.md) - full endpoint reference.
- [Dashboards overview](../../../domains/reports-and-dashboards/dashboards/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
