---
type: SDK Example
title: SDK examples - Change Alert Status
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id}/alerts/status (changeAlertStatus)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/alerts/status"
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
  operation_id: changeAlertStatus
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/alerts/status"
  endpoint_doc: "/domains/schedules-and-alerts/data-alerts/change-alert-status.md"
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
    resource: "/domains/schedules-and-alerts/data-alerts/change-alert-status.md"
    title: Endpoint reference - Change Alert Status
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

Code samples for [Change Alert Status](../../../domains/schedules-and-alerts/data-alerts/change-alert-status.md) (`PUT /restapi/v2/workspaces/{workspace-id}/alerts/status`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/alerts/status" -X 'PUT' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"alertIds":["137687000010815003","137687000010815005"],"enabled":false}'
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

        public void ChangeAlertStatus(IAnalyticsClient ac)
        {
            List<long> alertIds = new List<long>();
            alertIds.Add(137687000010815003L);
            alertIds.Add(137687000010815005L);
            bool enabled = false;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.ChangeAlertStatus(alertIds, enabled, null);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.ChangeAlertStatus(ac);
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

func ChangeAlertStatus(ac ZAnalytics.Client) {
    alertids := []string{"137687000010815003", "137687000010815005"}
    enabled := false
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    exception := workspace.ChangeAlertStatus(alertids, enabled, nil)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    ChangeAlertStatus(ac)
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
            tObj.changeAlertStatus(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void changeAlertStatus(AnalyticsClient ac) throws Exception {
        JSONArray alertIds = new JSONArray();
        alertIds.put("137687000010815003");
        alertIds.put("137687000010815005");
        boolean enabled = false;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.changeAlertStatus(alertIds, enabled, null);
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

    function changeAlertStatus() {
        $alert_ids = array("137687000010815003", "137687000010815005");
        $enabled = false;
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->changeAlertStatus($alert_ids, $enabled);
        echo "success";
    }
}

$obj = new Test();
$obj->changeAlertStatus();
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

    def change_alert_status(self, ac):
        alert_ids = ["137687000010815003", "137687000010815005"]
        enabled = False
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.change_alert_status(alert_ids, enabled)
        print("success")

obj = Sample()
obj.change_alert_status(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var alertIds = ["137687000010815003", "137687000010815005"];
var enabled = false;
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.changeAlertStatus(alertIds, enabled).then(() => { console.log("success"); }).catch((error) => { console.log(error); });
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

  def change_alert_status
    alert_ids = ["137687000010815003", "137687000010815005"]
    enabled = false
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.change_alert_status(alert_ids, enabled)
    puts "success"
  end
end

obj = Sample.new
obj.change_alert_status
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"alertIds": ["137687000010815003", "137687000010815005"], "enabled": false};
response = invokeurl
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/alerts/status"
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Change Alert Status](../../../domains/schedules-and-alerts/data-alerts/change-alert-status.md) - full endpoint reference.
- [Data Alerts overview](../../../domains/schedules-and-alerts/data-alerts/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
