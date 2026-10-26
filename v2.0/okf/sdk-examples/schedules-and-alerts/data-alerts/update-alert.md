---
type: SDK Example
title: SDK examples - Update Alert
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id}/alerts/{alert-id} (updateAlert)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}"
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
  operation_id: updateAlert
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}"
  endpoint_doc: "/domains/schedules-and-alerts/data-alerts/update-alert.md"
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
    resource: "/domains/schedules-and-alerts/data-alerts/update-alert.md"
    title: Endpoint reference - Update Alert
generated:
  by: process:build_okf
  at: 2026-10-23T07:58:54Z
status: stable
---

# Summary

Code samples for [Update Alert](../../../domains/schedules-and-alerts/data-alerts/update-alert.md) (`PUT /restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/alerts/35130000001056611" -X 'PUT' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"alertName":"Sales Drop Alert (weekly)","scheduleDetails":{"calendarFrequency":"weekly","hour":9,"minute":30,"weekDays":[6],"timeZone":"Asia/Kolkata"},"email":{"notifyAdmins":true,"emailIds":["finance@example.com"],"subject":"Weekly sales monitor","message":"Weekly alert summary."},"rules":[{"operator":"lt","viewColumnIndex":"2","type":"constant","values":["1000"]}]}'
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

        public void UpdateAlert(IAnalyticsClient ac)
        {
            long alertId = 35130000001056611L;
            string alertName = "Sales Drop Alert (weekly)";
            Dictionary<string, object> scheduleDetails = JsonSerializer.Deserialize<Dictionary<string, object>>("{\"calendarFrequency\":\"weekly\",\"hour\":9,\"minute\":30,\"weekDays\":[6],\"timeZone\":\"Asia/Kolkata\"}");
            List<Dictionary<string, object>> rules = JsonSerializer.Deserialize<List<Dictionary<string, object>>>("[{\"operator\":\"lt\",\"viewColumnIndex\":\"2\",\"type\":\"constant\",\"values\":[\"1000\"]}]");
            Dictionary<string, object> config = JsonSerializer.Deserialize<Dictionary<string, object>>("{\"email\":{\"notifyAdmins\":true,\"emailIds\":[\"finance@example.com\"],\"subject\":\"Weekly sales monitor\",\"message\":\"Weekly alert summary.\"}}");
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.UpdateAlert(alertId, alertName, scheduleDetails, rules, config);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.UpdateAlert(ac);
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

func UpdateAlert(ac ZAnalytics.Client) {
    alertid := "35130000001056611"
    alertname := "Sales Drop Alert (weekly)"
    scheduledetails := map[string]interface{}{
        "calendarFrequency": "weekly",
        "hour": 9,
        "minute": 30,
        "weekDays": []int{6},
        "timeZone": "Asia/Kolkata",
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
            "emailIds": []string{"finance@example.com"},
            "subject": "Weekly sales monitor",
            "message": "Weekly alert summary.",
        },
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    exception := workspace.UpdateAlert(alertid, alertname, scheduledetails, rules, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    UpdateAlert(ac)
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
            tObj.updateAlert(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void updateAlert(AnalyticsClient ac) throws Exception {
        long alertId = 35130000001056611l;
        String alertName = "Sales Drop Alert (weekly)";
        JSONObject scheduleDetails = new JSONObject("{\"calendarFrequency\":\"weekly\",\"hour\":9,\"minute\":30,\"weekDays\":[6],\"timeZone\":\"Asia/Kolkata\"}");
        JSONArray rules = new JSONArray("[{\"operator\":\"lt\",\"viewColumnIndex\":\"2\",\"type\":\"constant\",\"values\":[\"1000\"]}]");
        JSONObject config = new JSONObject("{\"email\":{\"notifyAdmins\":true,\"emailIds\":[\"finance@example.com\"],\"subject\":\"Weekly sales monitor\",\"message\":\"Weekly alert summary.\"}}");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.updateAlert(alertId, alertName, scheduleDetails, rules, config);
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

    function updateAlert() {
        $alert_id = "35130000001056611";
        $alert_name = "Sales Drop Alert (weekly)";
        $schedule_details = array(
            "calendarFrequency" => "weekly",
            "hour" => 9,
            "minute" => 30,
            "weekDays" => array(6),
            "timeZone" => "Asia/Kolkata"
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
                "emailIds" => array("finance@example.com"),
                "subject" => "Weekly sales monitor",
                "message" => "Weekly alert summary."
            )
        );
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->updateAlert($alert_id, $alert_name, $schedule_details, $rules, $config);
        echo "success";
    }
}

$obj = new Test();
$obj->updateAlert();
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

    def update_alert(self, ac):
        alert_id = "35130000001056611"
        alert_name = "Sales Drop Alert (weekly)"
        schedule_details = {
            "calendarFrequency": "weekly",
            "hour": 9,
            "minute": 30,
            "weekDays": [6],
            "timeZone": "Asia/Kolkata"
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
                "emailIds": ["finance@example.com"],
                "subject": "Weekly sales monitor",
                "message": "Weekly alert summary."
            }
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.update_alert(alert_id, alert_name, schedule_details, rules, config)
        print("success")

obj = Sample()
obj.update_alert(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var alertId = "35130000001056611";
var alertName = "Sales Drop Alert (weekly)";
var scheduleDetails = {
    "calendarFrequency": "weekly",
    "hour": 9,
    "minute": 30,
    "weekDays": [6],
    "timeZone": "Asia/Kolkata"
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
        "emailIds": ["finance@example.com"],
        "subject": "Weekly sales monitor",
        "message": "Weekly alert summary."
    }
};
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.updateAlert(alertId, alertName, scheduleDetails, rules, config).then(() => { console.log("success"); }).catch((error) => { console.log(error); });
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

  def update_alert
    alert_id = "35130000001056611"
    alert_name = "Sales Drop Alert (weekly)"
    schedule_details = {
      "calendarFrequency" => "weekly",
      "hour" => 9,
      "minute" => 30,
      "weekDays" => [6],
      "timeZone" => "Asia/Kolkata"
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
        "emailIds" => ["finance@example.com"],
        "subject" => "Weekly sales monitor",
        "message" => "Weekly alert summary."
      }
    }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.update_alert(alert_id, alert_name, schedule_details, rules, config)
    puts "success"
  end
end

obj = Sample.new
obj.update_alert
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
alertId = "35130000001056611";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"alertName": "Sales Drop Alert (weekly)", "scheduleDetails": {"calendarFrequency": "weekly", "hour": 9, "minute": 30, "weekDays": [6], "timeZone": "Asia/Kolkata"}, "email": {"notifyAdmins": true, "emailIds": ["finance@example.com"], "subject": "Weekly sales monitor", "message": "Weekly alert summary."}, "rules": [{"operator": "lt", "viewColumnIndex": "2", "type": "constant", "values": ["1000"]}]};
response = invokeurl
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/alerts/" + alertId
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Update Alert](../../../domains/schedules-and-alerts/data-alerts/update-alert.md) - full endpoint reference.
- [Data Alerts overview](../../../domains/schedules-and-alerts/data-alerts/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
