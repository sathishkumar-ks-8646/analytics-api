---
type: SDK Example
title: SDK examples - Get Alert Events
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/events (getAlertEvents)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/events"
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
  operation_id: getAlertEvents
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/events"
  endpoint_doc: "/domains/schedules-and-alerts/data-alerts/get-alert-events.md"
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
    last_modified: 2026-10-26T10:54:58Z
  - id: endpoint-doc
    resource: "/domains/schedules-and-alerts/data-alerts/get-alert-events.md"
    title: Endpoint reference - Get Alert Events
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

Code samples for [Get Alert Events](../../../domains/schedules-and-alerts/data-alerts/get-alert-events.md) (`GET /restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/events`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/alerts/35130000001056611/events?CONFIG=%7B%22fromDate%22%3A%222026-05-01%2000%3A00%3A00%22%2C%22toDate%22%3A%222026-05-31%2023%3A59%3A59%22%2C%22status%22%3A%5B%22triggered%22%2C%22error%22%5D%2C%22pageNo%22%3A1%2C%22recordsPerPage%22%3A50%7D" -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
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

        public void GetAlertEvents(IAnalyticsClient ac)
        {
            long alertId = 35130000001056611L;
            Dictionary<string, object> config = JsonSerializer.Deserialize<Dictionary<string, object>>("{\"fromDate\":\"2026-05-01 00:00:00\",\"toDate\":\"2026-05-31 23:59:59\",\"status\":[\"triggered\",\"error\"],\"pageNo\":1,\"recordsPerPage\":50}");
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetAlertEvents(alertId, config);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.GetAlertEvents(ac);
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

func GetAlertEvents(ac ZAnalytics.Client) {
    alertid := "35130000001056611"
    config := map[string]interface{}{
        "fromDate": "2026-05-01 00:00:00",
        "toDate": "2026-05-31 23:59:59",
        "status": []string{"triggered", "error"},
        "pageNo": 1,
        "recordsPerPage": 50,
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.GetAlertEvents(alertid, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetAlertEvents(ac)
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
            tObj.getAlertEvents(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void getAlertEvents(AnalyticsClient ac) throws Exception {
        long alertId = 35130000001056611l;
        JSONObject config = new JSONObject("{\"fromDate\":\"2026-05-01 00:00:00\",\"toDate\":\"2026-05-31 23:59:59\",\"status\":[\"triggered\",\"error\"],\"pageNo\":1,\"recordsPerPage\":50}");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getAlertEvents(alertId, config);
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

    function getAlertEvents() {
        $alert_id = "35130000001056611";
        $config = array(
            "fromDate" => "2026-05-01 00:00:00",
            "toDate" => "2026-05-31 23:59:59",
            "status" => array("triggered", "error"),
            "pageNo" => 1,
            "recordsPerPage" => 50
        );
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $response = $workspace->getAlertEvents($alert_id, $config);
        print_r($response);
    }
}

$obj = new Test();
$obj->getAlertEvents();
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

    def get_alert_events(self, ac):
        alert_id = "35130000001056611"
        config = {
            "fromDate": "2026-05-01 00:00:00",
            "toDate": "2026-05-31 23:59:59",
            "status": ["triggered", "error"],
            "pageNo": 1,
            "recordsPerPage": 50
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_alert_events(alert_id, config)
        print(result)

obj = Sample()
obj.get_alert_events(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var alertId = "35130000001056611";
var config = {
    "fromDate": "2026-05-01 00:00:00",
    "toDate": "2026-05-31 23:59:59",
    "status": ["triggered", "error"],
    "pageNo": 1,
    "recordsPerPage": 50
};
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.getAlertEvents(alertId, config).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def get_alert_events
    alert_id = "35130000001056611"
    config = {
      "fromDate" => "2026-05-01 00:00:00",
      "toDate" => "2026-05-31 23:59:59",
      "status" => ["triggered", "error"],
      "pageNo" => 1,
      "recordsPerPage" => 50
    }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_alert_events(alert_id, config)
    puts result
  end
end

obj = Sample.new
obj.get_alert_events
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
alertId = "35130000001056611";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"fromDate": "2026-05-01 00:00:00", "toDate": "2026-05-31 23:59:59", "status": ["triggered", "error"], "pageNo": 1, "recordsPerPage": 50};
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/alerts/" + alertId + "/events?CONFIG=" + zoho.encryption.urlEncode(config.toString())
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Alert Events](../../../domains/schedules-and-alerts/data-alerts/get-alert-events.md) - full endpoint reference.
- [Data Alerts overview](../../../domains/schedules-and-alerts/data-alerts/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
