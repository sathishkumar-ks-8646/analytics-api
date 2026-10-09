---
type: SDK Example
title: SDK examples - Create Email Schedule
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/emailschedules (createEmailSchedule)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/emailschedules"
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
  operation_id: createEmailSchedule
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/emailschedules"
  endpoint_doc: "/domains/schedules-and-alerts/email-schedules/create-email-schedule.md"
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
    last_modified: 2026-10-09T14:14:03Z
  - id: endpoint-doc
    resource: "/domains/schedules-and-alerts/email-schedules/create-email-schedule.md"
    title: Endpoint reference - Create Email Schedule
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

Code samples for [Create Email Schedule](../../../domains/schedules-and-alerts/email-schedules/create-email-schedule.md) (`POST /restapi/v2/workspaces/{workspace-id}/emailschedules`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/emailschedules" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"scheduleName":"Weekly Sales Report","viewIds":["35130000001055717"],"exportType":"pdf","scheduleDetails":{"calendarFrequency":"weekly","hour":14,"minute":30,"weekDays":[2,6]},"emailIds":["user@example.com"],"subject":"Weekly Sales Report"}'
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

        public void CreateEmailSchedule(IAnalyticsClient ac)
        {
            string scheduleName = "Weekly Sales Report";
            string format = "pdf";
            List<long> viewIds = new List<long>();
            viewIds.Add(35130000001055717L);
            List<string> emailIds = new List<string>();
            emailIds.Add("user@example.com");
            List<int> weekDays = new List<int>();
            weekDays.Add(2);
            weekDays.Add(6);
            Dictionary<string, object> scheduleDetails = new Dictionary<string, object>();
            scheduleDetails.Add("calendarFrequency", "weekly");
            scheduleDetails.Add("hour", 14);
            scheduleDetails.Add("minute", 30);
            scheduleDetails.Add("weekDays", weekDays);
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("subject", "Weekly Sales Report");
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            long scheduleId = workspace.CreateEmailSchedule(scheduleName, viewIds, format, emailIds, scheduleDetails, config);
            Console.WriteLine(scheduleId);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.CreateEmailSchedule(ac);
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

func CreateEmailSchedule(ac ZAnalytics.Client) {
    schedulename := "Weekly Sales Report"
    format := "pdf"
    viewids := []string{"35130000001055717"}
    emailids := []string{"user@example.com"}
    scheduledetails := map[string]interface{}{
        "calendarFrequency": "weekly",
        "hour": 14,
        "minute": 30,
        "weekDays": []int{2, 6},
    }
    config := map[string]interface{}{
        "subject": "Weekly Sales Report",
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.CreateEmailSchedule(schedulename, viewids, format, emailids, scheduledetails, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateEmailSchedule(ac)
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
            tObj.createEmailSchedule(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void createEmailSchedule(AnalyticsClient ac) throws Exception {
        String scheduleName = "Weekly Sales Report";
        String format = "pdf";
        JSONArray viewIds = new JSONArray();
        viewIds.put("35130000001055717");
        JSONArray emailIds = new JSONArray();
        emailIds.put("user@example.com");
        JSONArray weekDays = new JSONArray();
        weekDays.put(2);
        weekDays.put(6);
        JSONObject scheduleDetails = new JSONObject();
        scheduleDetails.put("calendarFrequency", "weekly");
        scheduleDetails.put("hour", 14);
        scheduleDetails.put("minute", 30);
        scheduleDetails.put("weekDays", weekDays);
        JSONObject config = new JSONObject();
        config.put("subject", "Weekly Sales Report");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        long result = workspace.createEmailSchedule(scheduleName, viewIds, format, emailIds, scheduleDetails, config);
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

    function createEmailSchedule() {
        $schedule_name = "Weekly Sales Report";
        $format = "pdf";
        $view_ids = array("35130000001055717");
        $email_ids = array("user@example.com");
        $schedule_details = array(
            "calendarFrequency" => "weekly",
            "hour" => 14,
            "minute" => 30,
            "weekDays" => array(2, 6)
        );
        $config = array("subject" => "Weekly Sales Report");
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $result = $workspace->createEmailSchedule($schedule_name, $view_ids, $format, $email_ids, $schedule_details, $config);
        echo $result;
    }
}

$obj = new Test();
$obj->createEmailSchedule();
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

class sample:
    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def create_email_schedule(self, ac):
        schedule_name = "Weekly Sales Report"
        format = "pdf"
        view_ids = [Config.VIEWID]
        email_ids = ["user@example.com"]
        schedule_details = {
            "calendarFrequency": "weekly",
            "hour": 14,
            "minute": 30,
            "weekDays": [2, 6]
        }
        config = {"subject": "Weekly Sales Report"}
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_email_schedule(schedule_name, view_ids, format, email_ids, schedule_details, config)
        print(result)

obj = sample()
obj.create_email_schedule(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';
var viewId = '35130000001055717';

var scheduleName = 'Weekly Sales Report';
var format = 'pdf';
var viewIds = [viewId];
var emailIds = ['user@example.com'];
var scheduleDetails = { calendarFrequency: 'weekly', hour: 14, minute: 30, weekDays: [2, 6] };
var config = { subject: 'Weekly Sales Report' };

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.createEmailSchedule(scheduleName, viewIds, format, emailIds, scheduleDetails, config).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def create_email_schedule
    schedule_name = "Weekly Sales Report"
    format = "pdf"
    view_ids = [Config::VIEWID]
    email_ids = ["user@example.com"]
    schedule_details = { "calendarFrequency" => "weekly", "hour" => 14, "minute" => 30, "weekDays" => [2, 6] }
    config = { "subject" => "Weekly Sales Report" }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.create_email_schedule(schedule_name, view_ids, format, email_ids, schedule_details, config)
    puts result
  end
end

obj = Sample.new
obj.create_email_schedule
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
viewId = "35130000001055717";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
viewIds = List();
viewIds.add(viewId);
weekDays = List();
weekDays.add(2);
weekDays.add(6);
scheduleDetails = Map();
scheduleDetails.put("calendarFrequency", "weekly");
scheduleDetails.put("hour", 14);
scheduleDetails.put("minute", 30);
scheduleDetails.put("weekDays", weekDays);
emailIds = List();
emailIds.add("user@example.com");
config = Map();
config.put("scheduleName", "Weekly Sales Report");
config.put("viewIds", viewIds);
config.put("exportType", "pdf");
config.put("scheduleDetails", scheduleDetails);
config.put("emailIds", emailIds);
config.put("subject", "Weekly Sales Report");
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/emailschedules"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Create Email Schedule](../../../domains/schedules-and-alerts/email-schedules/create-email-schedule.md) - full endpoint reference.
- [Email Schedules overview](../../../domains/schedules-and-alerts/email-schedules/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
