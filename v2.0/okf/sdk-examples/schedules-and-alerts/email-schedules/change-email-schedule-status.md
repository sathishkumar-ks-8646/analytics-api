---
type: SDK Example
title: SDK examples - Change Email Schedule Status
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}/status (changeEmailScheduleStatus)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}/status"
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
  operation_id: changeEmailScheduleStatus
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}/status"
  endpoint_doc: "/domains/schedules-and-alerts/email-schedules/change-email-schedule-status.md"
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
    resource: "/domains/schedules-and-alerts/email-schedules/change-email-schedule-status.md"
    title: Endpoint reference - Change Email Schedule Status
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

Code samples for [Change Email Schedule Status](../../../domains/schedules-and-alerts/email-schedules/change-email-schedule-status.md) (`PUT /restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}/status`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/emailschedules/35130000001056601/status" -X 'PUT' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"operation":"deactivate"}'
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

        public void ChangeEmailScheduleStatus(IAnalyticsClient ac)
        {
            long scheduleId = 35130000001056601L;
            string operation = "deactivate";
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.ChangeEmailScheduleStatus(scheduleId, operation);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.ChangeEmailScheduleStatus(ac);
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

func ChangeEmailScheduleStatus(ac ZAnalytics.Client) {
    scheduleid := "35130000001056601"
    operation := "deactivate"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    exception := workspace.ChangeEmailScheduleStatus(scheduleid, operation)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    ChangeEmailScheduleStatus(ac)
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
            tObj.changeEmailScheduleStatus(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void changeEmailScheduleStatus(AnalyticsClient ac) throws Exception {
        long scheduleId = 35130000001056601l;
        String operation = "deactivate";
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.changeEmailScheduleStatus(scheduleId, operation);
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

    function changeEmailScheduleStatus() {
        $schedule_id = "35130000001056601";
        $operation = "deactivate";
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->changeEmailScheduleStatus($schedule_id, $operation);
        echo "success";
    }
}

$obj = new Test();
$obj->changeEmailScheduleStatus();
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

    def change_email_schedule_status(self, ac):
        schedule_id = "35130000001056601"
        operation = "deactivate"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.change_email_schedule_status(schedule_id, operation)
        print("success")

obj = sample()
obj.change_email_schedule_status(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';
var scheduleId = '35130000001056601';
var operation = 'deactivate';

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.changeEmailScheduleStatus(scheduleId, operation).then(() => { console.log('success'); }).catch((error) => { console.log(error); });
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

  def change_email_schedule_status
    schedule_id = "35130000001056601"
    operation = "deactivate"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.change_email_schedule_status(schedule_id, operation)
    puts "success"
  end
end

obj = Sample.new
obj.change_email_schedule_status
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
scheduleId = "35130000001056601";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("operation", "deactivate");
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/emailschedules/" + scheduleId + "/status"
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Change Email Schedule Status](../../../domains/schedules-and-alerts/email-schedules/change-email-schedule-status.md) - full endpoint reference.
- [Email Schedules overview](../../../domains/schedules-and-alerts/email-schedules/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
