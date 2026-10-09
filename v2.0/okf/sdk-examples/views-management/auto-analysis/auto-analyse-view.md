---
type: SDK Example
title: SDK examples - Auto Analyse View
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/autoanalyse (autoAnalyseView)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/autoanalyse"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - views-management
  - auto-analysis
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
  operation_id: autoAnalyseView
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/autoanalyse"
  endpoint_doc: "/domains/views-management/auto-analysis/auto-analyse-view.md"
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
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
  - id: endpoint-doc
    resource: "/domains/views-management/auto-analysis/auto-analyse-view.md"
    title: Endpoint reference - Auto Analyse View
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Auto Analyse View](../../../domains/views-management/auto-analysis/auto-analyse-view.md) (`POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/autoanalyse`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/autoanalyse" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"analyseAgain":false}'
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
        long viewId = 35130000001055717;

        public void AutoAnalyseView(IAnalyticsClient ac)
        {
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("analyseAgain", false);
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.AutoAnalyse(config);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.AutoAnalyseView(ac);
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
    viewId = "35130000001055717"
)

func AutoAnalyseView(ac ZAnalytics.Client) {
    config := map[string]interface{}{"analyseAgain": false}
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    exception := view.AutoAnalyse(config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    AutoAnalyseView(ac)
}
```

## Java

```java
import com.zoho.analytics.client.*;
import org.json.*;

public class Test {
    private long orgId = 55522777l;
    private long workspaceId = 35130000001055707l;
    private long viewId = 35130000001055717l;

    public static void main(String args[]) {
        String clientId = "1000.xxxxxxx";
        String clientSecret = "xxxxxxx";
        String refreshToken = "1000.xxxxxxx.xxxxxxx";
        Test tObj = new Test();
        AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
        try {
            tObj.autoAnalyseView(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void autoAnalyseView(AnalyticsClient ac) throws Exception {
        JSONObject config = new JSONObject();
        config.put("analyseAgain", false);
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.autoAnalyse(config);
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
    public $view_id = "35130000001055717";

    function __construct() {
        $this->ac = new AnalyticsClient("1000.xxxxxxx", "xxxxxxx", "1000.xxxxxxx.xxxxxxx");
    }

    function autoAnalyseView() {
        $config = array("analyseAgain" => false);
        $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
        $view->autoAnalyse($config);
        echo "success\n";
    }
}

$obj = new Test();
$obj->autoAnalyseView();
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
    VIEWID = "35130000001055717"

class Sample:
    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def auto_analyse_view(self, ac):
        config = {"analyseAgain": False}
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.auto_analyse(config)
        print("success")

obj = Sample()
obj.auto_analyse_view(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';
var viewId = '35130000001055717';

var config = {analyseAgain: false};
var view = ac.getViewInstance(orgId, workspaceId, viewId);
view.autoAnalyse(config).then(() => { console.log('success'); }).catch((error) => { console.log(error); });
```

## Ruby

```ruby
require 'zoho_analytics_client'

class Config
  ORGID = "55522777"
  WORKSPACEID = "35130000001055707"
  VIEWID = "35130000001055717"
end

class Sample
  def initialize
    @ac = AnalyticsClient.new.with_data_center("US").with_oauth({
      "clientId" => "1000.xxxxxxx",
      "clientSecret" => "xxxxxxx",
      "refreshToken" => "1000.xxxxxxx.xxxxxxx"
    }).build
  end

  def auto_analyse_view
    config = {"analyseAgain" => false}
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    view.auto_analyse(config)
    puts "success"
  end
end

obj = Sample.new
obj.auto_analyse_view
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
viewId = "35130000001055717";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("analyseAgain", false);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/" + viewId + "/autoanalyse"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Auto Analyse View](../../../domains/views-management/auto-analysis/auto-analyse-view.md) - full endpoint reference.
- [Auto Analysis overview](../../../domains/views-management/auto-analysis/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
