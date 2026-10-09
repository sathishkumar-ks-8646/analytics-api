---
type: SDK Example
title: SDK examples - Get Dashboard Metadata
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
    last_modified: 2026-10-09T08:29:02Z
  - id: endpoint-doc
    resource: "/domains/reports-and-dashboards/dashboards/get-dashboard-metadata.md"
    title: Endpoint reference - Get Dashboard Metadata
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

Code samples for [Get Dashboard Metadata](../../../domains/reports-and-dashboards/dashboards/get-dashboard-metadata.md) (`GET /restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}/metadata`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl -G "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/dashboards/35130000001055801/metadata" --data-urlencode 'CONFIG={"include":"themes,settings"}' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
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
            long dashboardId = 35130000001055801;
            // Omit CONFIG to return every section
            Dictionary<string, object> config = new Dictionary<string, object>{{"include","themes,settings"}};
            IDashboardAPI dashboard = ac.GetDashboardInstance(orgId, workspaceId, dashboardId);
            JsonElement dashboardConfig = dashboard.GetMetadata(config);
            Console.WriteLine(dashboardConfig);
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
    dashboardId := "35130000001055801"
    // Omit CONFIG to return every section
    config := map[string]interface{}{"include": "themes,settings"}
    dashboard := ZAnalytics.GetDashboardInstance(&ac, orgId, workspaceId, dashboardId)
    dashboardConfig, exception := dashboard.GetMetadata(config)
    if exception != nil { fmt.Println(exception.ErrorMessage); return }
    fmt.Println(dashboardConfig)
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
        // Omit CONFIG to return every section
        JSONObject config = new JSONObject();
        config.put("include", "themes,settings");
        DashboardAPI dashboard = ac.getDashboardInstance(orgId, workspaceId, dashboardId);
        JSONObject dashboardConfig = dashboard.getMetadata(config);
        System.out.println(dashboardConfig);
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
        // Omit CONFIG to return every section
        $config = ["include" => "themes,settings"];
        $dashboard = $this->ac->getDashboardInstance($this->org_id, $this->workspace_id, $dashboard_id);
        $dashboard_config = $dashboard->getMetadata($config);
        print_r($dashboard_config);
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

class sample:
    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def get_dashboard_metadata(self, ac):
        dashboard_id = "35130000001055801"
        # Omit CONFIG to return every section
        config = {"include": "themes,settings"}
        dashboard = ac.get_dashboard_instance(Config.ORGID, Config.WORKSPACEID, dashboard_id)
        dashboard_config = dashboard.get_metadata(config)
        print(dashboard_config)

obj = sample()
obj.get_dashboard_metadata(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var dashboardId = '35130000001055801';
// Omit CONFIG to return every section
var config = { include: 'themes,settings' };
var dashboard = ac.getDashboardInstance(orgId, workspaceId, dashboardId);
dashboard.getMetadata(config).then((dashboardConfig) => { console.log(dashboardConfig); }).catch((error) => { console.log(error); });
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
    # Omit CONFIG to return every section
    config = { "include" => "themes,settings" }
    dashboard = @ac.get_dashboard_instance(Config::ORGID, Config::WORKSPACEID, dashboard_id)
    dashboard_config = dashboard.get_metadata(config)
    puts dashboard_config
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
// Omit CONFIG to return every section
config = Map();
config.put("include", "themes,settings");
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

- [Get Dashboard Metadata](../../../domains/reports-and-dashboards/dashboards/get-dashboard-metadata.md) - full endpoint reference.
- [Dashboards overview](../../../domains/reports-and-dashboards/dashboards/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
