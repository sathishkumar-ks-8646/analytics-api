---
type: SDK Example
title: SDK examples - Update Email Schedule
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id} (updateEmailSchedule)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - schedules-and-alerts
  - email-schedules
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
  operation_id: updateEmailSchedule
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}"
  endpoint_doc: "/domains/schedules-and-alerts/email-schedules/update-email-schedule.md"
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
    last_modified: 2026-10-09T13:04:25Z
  - id: endpoint-doc
    resource: "/domains/schedules-and-alerts/email-schedules/update-email-schedule.md"
    title: Endpoint reference - Update Email Schedule
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Update Email Schedule](../../../domains/schedules-and-alerts/email-schedules/update-email-schedule.md) (`PUT /restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/emailschedules/35130000001056601" -X 'PUT' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"scheduleName":"Monthly Sales Report","scheduleDetails":{"calendarFrequency":"monthly","hour":8,"minute":30,"monthDay":1},"subject":"Monthly Sales Report"}'
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

        public void UpdateEmailSchedule(IAnalyticsClient ac)
        {
            long scheduleId = 35130000001056601L;
            Dictionary<string, object> scheduleDetails = new Dictionary<string, object>();
            scheduleDetails.Add("calendarFrequency", "monthly");
            scheduleDetails.Add("hour", 8);
            scheduleDetails.Add("minute", 30);
            scheduleDetails.Add("monthDay", 1);
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("scheduleName", "Monthly Sales Report");
            config.Add("scheduleDetails", scheduleDetails);
            config.Add("subject", "Monthly Sales Report");
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            long result = workspace.UpdateEmailSchedule(scheduleId, config);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.UpdateEmailSchedule(ac);
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

func UpdateEmailSchedule(ac ZAnalytics.Client) {
    scheduleid := "35130000001056601"
    scheduledetails := map[string]interface{}{
        "calendarFrequency": "monthly",
        "hour": 8,
        "minute": 30,
        "monthDay": 1,
    }
    config := map[string]interface{}{
        "scheduleName": "Monthly Sales Report",
        "scheduleDetails": scheduledetails,
        "subject": "Monthly Sales Report",
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.UpdateEmailSchedule(scheduleid, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    UpdateEmailSchedule(ac)
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
            tObj.updateEmailSchedule(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void updateEmailSchedule(AnalyticsClient ac) throws Exception {
        long scheduleId = 35130000001056601l;
        JSONObject scheduleDetails = new JSONObject();
        scheduleDetails.put("calendarFrequency", "monthly");
        scheduleDetails.put("hour", 8);
        scheduleDetails.put("minute", 30);
        scheduleDetails.put("monthDay", 1);
        JSONObject config = new JSONObject();
        config.put("scheduleName", "Monthly Sales Report");
        config.put("scheduleDetails", scheduleDetails);
        config.put("subject", "Monthly Sales Report");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        long result = workspace.updateEmailSchedule(scheduleId, config);
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

    function updateEmailSchedule() {
        $schedule_id = "35130000001056601";
        $schedule_details = array(
            "calendarFrequency" => "monthly",
            "hour" => 8,
            "minute" => 30,
            "monthDay" => 1
        );
        $config = array(
            "scheduleName" => "Monthly Sales Report",
            "scheduleDetails" => $schedule_details,
            "subject" => "Monthly Sales Report"
        );
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $result = $workspace->updateEmailSchedule($schedule_id, $config);
        echo $result;
    }
}

$obj = new Test();
$obj->updateEmailSchedule();
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

    def update_email_schedule(self, ac):
        schedule_id = "35130000001056601"
        schedule_details = {
            "calendarFrequency": "monthly",
            "hour": 8,
            "minute": 30,
            "monthDay": 1
        }
        config = {
            "scheduleName": "Monthly Sales Report",
            "scheduleDetails": schedule_details,
            "subject": "Monthly Sales Report"
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.update_email_schedule(schedule_id, config)
        print(result)

obj = sample()
obj.update_email_schedule(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';
var scheduleId = '35130000001056601';

var scheduleDetails = { calendarFrequency: 'monthly', hour: 8, minute: 30, monthDay: 1 };
var config = { scheduleName: 'Monthly Sales Report', scheduleDetails: scheduleDetails, subject: 'Monthly Sales Report' };

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.updateEmailSchedule(scheduleId, config).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def update_email_schedule
    schedule_id = "35130000001056601"
    schedule_details = { "calendarFrequency" => "monthly", "hour" => 8, "minute" => 30, "monthDay" => 1 }
    config = { "scheduleName" => "Monthly Sales Report", "scheduleDetails" => schedule_details, "subject" => "Monthly Sales Report" }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.update_email_schedule(schedule_id, config)
    puts result
  end
end

obj = Sample.new
obj.update_email_schedule
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
scheduleId = "35130000001056601";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
scheduleDetails = Map();
scheduleDetails.put("calendarFrequency", "monthly");
scheduleDetails.put("hour", 8);
scheduleDetails.put("minute", 30);
scheduleDetails.put("monthDay", 1);
config = Map();
config.put("scheduleName", "Monthly Sales Report");
config.put("scheduleDetails", scheduleDetails);
config.put("subject", "Monthly Sales Report");
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/emailschedules/" + scheduleId
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Update Email Schedule](../../../domains/schedules-and-alerts/email-schedules/update-email-schedule.md) - full endpoint reference.
- [Email Schedules overview](../../../domains/schedules-and-alerts/email-schedules/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
