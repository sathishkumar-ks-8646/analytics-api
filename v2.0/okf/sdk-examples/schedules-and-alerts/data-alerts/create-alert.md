---
type: SDK Example
title: SDK examples - Create Alert
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts (createAlert)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - schedules-and-alerts
  - data-alerts
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
  operation_id: createAlert
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts"
  endpoint_doc: "/domains/schedules-and-alerts/data-alerts/create-alert.md"
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
    resource: "/references/openapi/schedules-alerts-grouped-api.json"
    title: OpenAPI 3 specification - schedules-alerts-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-20T17:34:40Z
  - id: endpoint-doc
    resource: "/domains/schedules-and-alerts/data-alerts/create-alert.md"
    title: Endpoint reference - Create Alert
generated:
  by: process:build_okf
  at: 2026-10-23T07:58:54Z
status: stable
---

# Summary

Code samples for [Create Alert](../../../domains/schedules-and-alerts/data-alerts/create-alert.md) (`POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/alerts" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"alertName":"Sales Drop Alert","scheduleDetails":{"calendarFrequency":"daily","hour":9,"minute":0},"email":{"notifyAdmins":true,"subject":"Sales dropped below threshold","message":"Please review the report."},"rules":[{"operator":"lt","viewColumnIndex":"2","type":"constant","values":["1000"]}]}'
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

        public void CreateAlert(IAnalyticsClient ac)
        {
            string alertName = "Sales Drop Alert";
            Dictionary<string, object> scheduleDetails = JsonSerializer.Deserialize<Dictionary<string, object>>("{\"calendarFrequency\":\"daily\",\"hour\":9,\"minute\":0}");
            List<Dictionary<string, object>> rules = JsonSerializer.Deserialize<List<Dictionary<string, object>>>("[{\"operator\":\"lt\",\"viewColumnIndex\":\"2\",\"type\":\"constant\",\"values\":[\"1000\"]}]");
            Dictionary<string, object> config = JsonSerializer.Deserialize<Dictionary<string, object>>("{\"email\":{\"notifyAdmins\":true,\"subject\":\"Sales dropped below threshold\",\"message\":\"Please review the report.\"}}");
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            long result = view.CreateAlert(alertName, scheduleDetails, rules, config);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.CreateAlert(ac);
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

func CreateAlert(ac ZAnalytics.Client) {
    alertname := "Sales Drop Alert"
    scheduledetails := map[string]interface{}{
        "calendarFrequency": "daily",
        "hour": 9,
        "minute": 0,
    }
    rules := []interface{}{
        map[string]interface{}{
            "operator": "lt",
            "viewColumnIndex": "2",
            "type": "constant",
            "values": []string{"1000"},
        },
    }
    config := map[string]interface{}{
        "email": map[string]interface{}{
            "notifyAdmins": true,
            "subject": "Sales dropped below threshold",
            "message": "Please review the report.",
        },
    }
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    result, exception := view.CreateAlert(alertname, scheduledetails, rules, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateAlert(ac)
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
            tObj.createAlert(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void createAlert(AnalyticsClient ac) throws Exception {
        String alertName = "Sales Drop Alert";
        JSONObject scheduleDetails = new JSONObject("{\"calendarFrequency\":\"daily\",\"hour\":9,\"minute\":0}");
        JSONArray rules = new JSONArray("[{\"operator\":\"lt\",\"viewColumnIndex\":\"2\",\"type\":\"constant\",\"values\":[\"1000\"]}]");
        JSONObject config = new JSONObject("{\"email\":{\"notifyAdmins\":true,\"subject\":\"Sales dropped below threshold\",\"message\":\"Please review the report.\"}}");
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        long result = view.createAlert(alertName, scheduleDetails, rules, config);
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
    public $view_id = "35130000001055717";

    function __construct() {
        $this->ac = new AnalyticsClient("1000.xxxxxxx", "xxxxxxx", "1000.xxxxxxx.xxxxxxx");
    }

    function createAlert() {
        $alert_name = "Sales Drop Alert";
        $schedule_details = array(
            "calendarFrequency" => "daily",
            "hour" => 9,
            "minute" => 0
        );
        $rules = array(
            array(
                "operator" => "lt",
                "viewColumnIndex" => "2",
                "type" => "constant",
                "values" => array("1000")
            )
        );
        $config = array(
            "email" => array(
                "notifyAdmins" => true,
                "subject" => "Sales dropped below threshold",
                "message" => "Please review the report."
            )
        );
        $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
        $response = $view->createAlert($alert_name, $schedule_details, $rules, $config);
        print_r($response);
    }
}

$obj = new Test();
$obj->createAlert();
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

    def create_alert(self, ac):
        alert_name = "Sales Drop Alert"
        schedule_details = {
            "calendarFrequency": "daily",
            "hour": 9,
            "minute": 0
        }
        rules = [
            {
                "operator": "lt",
                "viewColumnIndex": "2",
                "type": "constant",
                "values": ["1000"]
            }
        ]
        config = {
            "email": {
                "notifyAdmins": True,
                "subject": "Sales dropped below threshold",
                "message": "Please review the report."
            }
        }
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.create_alert(alert_name, schedule_details, rules, config)
        print(result)

obj = Sample()
obj.create_alert(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';
var viewId = '35130000001055717';

var alertName = "Sales Drop Alert";
var scheduleDetails = {
    "calendarFrequency": "daily",
    "hour": 9,
    "minute": 0
};
var rules = [
    {
        "operator": "lt",
        "viewColumnIndex": "2",
        "type": "constant",
        "values": ["1000"]
    }
];
var config = {
    "email": {
        "notifyAdmins": true,
        "subject": "Sales dropped below threshold",
        "message": "Please review the report."
    }
};
var view = ac.getViewInstance(orgId, workspaceId, viewId);
view.createAlert(alertName, scheduleDetails, rules, config).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def create_alert
    alert_name = "Sales Drop Alert"
    schedule_details = {
      "calendarFrequency" => "daily",
      "hour" => 9,
      "minute" => 0
    }
    rules = [
      {
        "operator" => "lt",
        "viewColumnIndex" => "2",
        "type" => "constant",
        "values" => ["1000"]
      }
    ]
    config = {
      "email" => {
        "notifyAdmins" => true,
        "subject" => "Sales dropped below threshold",
        "message" => "Please review the report."
      }
    }
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    result = view.create_alert(alert_name, schedule_details, rules, config)
    puts result
  end
end

obj = Sample.new
obj.create_alert
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
viewId = "35130000001055717";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"alertName": "Sales Drop Alert", "scheduleDetails": {"calendarFrequency": "daily", "hour": 9, "minute": 0}, "email": {"notifyAdmins": true, "subject": "Sales dropped below threshold", "message": "Please review the report."}, "rules": [{"operator": "lt", "viewColumnIndex": "2", "type": "constant", "values": ["1000"]}]};
response = invokeurl
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/" + viewId + "/alerts"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Create Alert](../../../domains/schedules-and-alerts/data-alerts/create-alert.md) - full endpoint reference.
- [Data Alerts overview](../../../domains/schedules-and-alerts/data-alerts/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
