---
type: SDK Example
title: SDK examples - Delete Alerts
description: "Code samples in 9 languages for DELETE /restapi/v2/workspaces/{workspace-id}/alerts (deleteAlerts)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/alerts"
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
  operation_id: deleteAlerts
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/alerts"
  endpoint_doc: "/domains/schedules-and-alerts/data-alerts/delete-alerts.md"
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
    resource: "/domains/schedules-and-alerts/data-alerts/delete-alerts.md"
    title: Endpoint reference - Delete Alerts
generated:
  by: process:build_okf
  at: 2026-10-23T07:58:54Z
status: stable
---

# Summary

Code samples for [Delete Alerts](../../../domains/schedules-and-alerts/data-alerts/delete-alerts.md) (`DELETE /restapi/v2/workspaces/{workspace-id}/alerts`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/alerts" -X 'DELETE' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"alertIds":["137687000010815003","137687000010815005"]}'
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

        public void DeleteAlerts(IAnalyticsClient ac)
        {
            List<long> alertIds = new List<long>();
            alertIds.Add(137687000010815003L);
            alertIds.Add(137687000010815005L);
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.DeleteAlerts(alertIds, null);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.DeleteAlerts(ac);
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

func DeleteAlerts(ac ZAnalytics.Client) {
    alertids := []string{"137687000010815003", "137687000010815005"}
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    exception := workspace.DeleteAlerts(alertids, nil)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    DeleteAlerts(ac)
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
            tObj.deleteAlerts(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void deleteAlerts(AnalyticsClient ac) throws Exception {
        JSONArray alertIds = new JSONArray();
        alertIds.put("137687000010815003");
        alertIds.put("137687000010815005");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.deleteAlerts(alertIds, null);
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

    function deleteAlerts() {
        $alert_ids = array("137687000010815003", "137687000010815005");
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->deleteAlerts($alert_ids);
        echo "success";
    }
}

$obj = new Test();
$obj->deleteAlerts();
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

    def delete_alerts(self, ac):
        alert_ids = ["137687000010815003", "137687000010815005"]
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.delete_alerts(alert_ids)
        print("success")

obj = Sample()
obj.delete_alerts(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var alertIds = ["137687000010815003", "137687000010815005"];
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.deleteAlerts(alertIds).then(() => { console.log("success"); }).catch((error) => { console.log(error); });
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

  def delete_alerts
    alert_ids = ["137687000010815003", "137687000010815005"]
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.delete_alerts(alert_ids)
    puts "success"
  end
end

obj = Sample.new
obj.delete_alerts
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"alertIds": ["137687000010815003", "137687000010815005"]};
response = invokeurl
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/alerts"
  type :DELETE
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Delete Alerts](../../../domains/schedules-and-alerts/data-alerts/delete-alerts.md) - full endpoint reference.
- [Data Alerts overview](../../../domains/schedules-and-alerts/data-alerts/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
