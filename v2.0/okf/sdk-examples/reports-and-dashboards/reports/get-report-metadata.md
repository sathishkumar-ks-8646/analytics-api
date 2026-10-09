---
type: SDK Example
title: SDK examples - Read Report Metadata
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata (getReportMetadata)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - reports-and-dashboards
  - reports
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
  operation_id: getReportMetadata
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata"
  endpoint_doc: "/domains/reports-and-dashboards/reports/get-report-metadata.md"
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
    last_modified: 2026-10-09T13:04:25Z
  - id: endpoint-doc
    resource: "/domains/reports-and-dashboards/reports/get-report-metadata.md"
    title: Endpoint reference - Read Report Metadata
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Read Report Metadata](../../../domains/reports-and-dashboards/reports/get-report-metadata.md) (`GET /restapi/v2/workspaces/{workspace-id}/reports/{view-id}/metadata`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/reports/35130000001055901/metadata" -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
```

## C#

```csharp
using System;
using System.Text.Json;
using ZohoAnalytics;

namespace ZohoAnalyticsTest
{
    class Program
    {
        long orgId = 55522777;
        long workspaceId = 35130000001055707;

        public void GetVisualMetadata(IAnalyticsClient ac)
        {
            long viewId = 35130000001055901;
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            JsonElement reportConfig = view.GetMetadata();
            Console.WriteLine(reportConfig);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.GetVisualMetadata(ac);
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

func GetVisualMetadata(ac ZAnalytics.Client) {
    viewId := "35130000001055901"
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    reportConfig, exception := view.GetMetadata()
    if exception != nil { fmt.Println(exception.ErrorMessage); return }
    fmt.Println(reportConfig)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetVisualMetadata(ac)
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
            tObj.getVisualMetadata(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void getVisualMetadata(AnalyticsClient ac) throws Exception {
        long viewId = 35130000001055901l;
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONObject reportConfig = view.getMetadata();
        System.out.println(reportConfig);
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

    function getVisualMetadata() {
        $view_id = "35130000001055901";
        $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $view_id);
        $report_config = $view->getMetadata();
        print_r($report_config);
    }
}

$obj = new Test();
$obj->getVisualMetadata();
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

    def get_visual_metadata(self, ac):
        view_id = "35130000001055901"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, view_id)
        report_config = view.get_metadata()
        print(report_config)

obj = sample()
obj.get_visual_metadata(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var viewId = '35130000001055901';
var view = ac.getViewInstance(orgId, workspaceId, viewId);
view.getMetadata().then((reportConfig) => { console.log(reportConfig); }).catch((error) => { console.log(error); });
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

  def get_visual_metadata
    view_id = "35130000001055901"
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, view_id)
    report_config = view.get_metadata
    puts report_config
  end
end

obj = Sample.new
obj.get_visual_metadata
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
viewId = "35130000001055901";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/reports/" + viewId + "/metadata"
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Read Report Metadata](../../../domains/reports-and-dashboards/reports/get-report-metadata.md) - full endpoint reference.
- [Reports (Analysis Views) overview](../../../domains/reports-and-dashboards/reports/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
