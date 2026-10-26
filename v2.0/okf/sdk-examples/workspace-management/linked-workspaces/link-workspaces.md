---
type: SDK Example
title: SDK examples - Link Workspaces
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/linkedworkspaces (linkWorkspaces)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/linkedworkspaces"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - workspace-management
  - linked-workspaces
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
  operation_id: linkWorkspaces
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/linkedworkspaces"
  endpoint_doc: "/domains/workspace-management/linked-workspaces/link-workspaces.md"
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
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-20T17:34:40Z
  - id: endpoint-doc
    resource: "/domains/workspace-management/linked-workspaces/link-workspaces.md"
    title: Endpoint reference - Link Workspaces
generated:
  by: process:build_okf
  at: 2026-10-23T07:58:54Z
status: stable
---

# Summary

Code samples for [Link Workspaces](../../../domains/workspace-management/linked-workspaces/link-workspaces.md) (`POST /restapi/v2/workspaces/{workspace-id}/linkedworkspaces`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/linkedworkspaces" \
  -X 'POST' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"clients":[{"orgId":700000654321,"workspaceIds":["466206000000071000"]}]}'
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

        public void LinkWorkspaces(IAnalyticsClient ac)
        {
            List<Dictionary<string, object>> clients = JsonSerializer.Deserialize<List<Dictionary<string, object>>>("[{\"orgId\":700000654321,\"workspaceIds\":[\"466206000000071000\"]}]");
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.LinkWorkspaces(clients, null);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.LinkWorkspaces(ac);
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

func LinkWorkspaces(ac ZAnalytics.Client) {
    clients := []interface{}{
        map[string]interface{}{
            "orgId": 700000654321,
            "workspaceIds": []string{"466206000000071000"},
        },
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    exception := workspace.LinkWorkspaces(clients, nil)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    LinkWorkspaces(ac)
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
            tObj.linkWorkspaces(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void linkWorkspaces(AnalyticsClient ac) throws Exception {
        JSONArray clients = new JSONArray("[{\"orgId\":700000654321,\"workspaceIds\":[\"466206000000071000\"]}]");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.linkWorkspaces(clients, null);
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

    function linkWorkspaces() {
        $clients = array(
            array(
                "orgId" => 700000654321,
                "workspaceIds" => array("466206000000071000")
            )
        );
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->linkWorkspaces($clients);
        echo "success";
    }
}

$obj = new Test();
$obj->linkWorkspaces();
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

    def link_workspaces(self, ac):
        clients = [
            {
                "orgId": 700000654321,
                "workspaceIds": ["466206000000071000"]
            }
        ]
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.link_workspaces(clients)
        print("success")

obj = Sample()
obj.link_workspaces(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var clients = [
    {
        "orgId": 700000654321,
        "workspaceIds": ["466206000000071000"]
    }
];
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.linkWorkspaces(clients).then(() => { console.log("success"); }).catch((error) => { console.log(error); });
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

  def link_workspaces
    clients = [
      {
        "orgId" => 700000654321,
        "workspaceIds" => ["466206000000071000"]
      }
    ]
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.link_workspaces(clients)
    puts "success"
  end
end

obj = Sample.new
obj.link_workspaces
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"clients": [{"orgId": 700000654321, "workspaceIds": ["466206000000071000"]}]};
response = invokeurl
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/linkedworkspaces"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Link Workspaces](../../../domains/workspace-management/linked-workspaces/link-workspaces.md) - full endpoint reference.
- [Linked Workspaces overview](../../../domains/workspace-management/linked-workspaces/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
