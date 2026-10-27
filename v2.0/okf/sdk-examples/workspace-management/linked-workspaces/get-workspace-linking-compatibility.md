---
type: SDK Example
title: SDK examples - Get Workspace Linking Compatibility
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/linkedworkspaces/compatibility (getWorkspaceLinkingCompatibility)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/compatibility"
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
  operation_id: getWorkspaceLinkingCompatibility
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/compatibility"
  endpoint_doc: "/domains/workspace-management/linked-workspaces/get-workspace-linking-compatibility.md"
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
    last_modified: 2026-10-26T11:33:37Z
  - id: endpoint-doc
    resource: "/domains/workspace-management/linked-workspaces/get-workspace-linking-compatibility.md"
    title: Endpoint reference - Get Workspace Linking Compatibility
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

Code samples for [Get Workspace Linking Compatibility](../../../domains/workspace-management/linked-workspaces/get-workspace-linking-compatibility.md) (`GET /restapi/v2/workspaces/{workspace-id}/linkedworkspaces/compatibility`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/linkedworkspaces/compatibility?CONFIG=%7B%22clients%22%3A%5B%7B%22orgId%22%3A700000654321%2C%22workspaceIds%22%3A%5B%22466206000000071000%22%5D%7D%5D%7D" \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>'
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

        public void GetWorkspaceLinkingCompatibility(IAnalyticsClient ac)
        {
            List<Dictionary<string, object>> clients = JsonSerializer.Deserialize<List<Dictionary<string, object>>>("[{\"orgId\":700000654321,\"workspaceIds\":[\"466206000000071000\"]}]");
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetWorkspaceLinkingCompatibility(clients, null);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.GetWorkspaceLinkingCompatibility(ac);
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

func GetWorkspaceLinkingCompatibility(ac ZAnalytics.Client) {
    clients := []interface{}{
        map[string]interface{}{
            "orgId": 700000654321,
            "workspaceIds": []string{"466206000000071000"},
        },
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.GetWorkspaceLinkingCompatibility(clients, nil)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetWorkspaceLinkingCompatibility(ac)
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
            tObj.getWorkspaceLinkingCompatibility(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void getWorkspaceLinkingCompatibility(AnalyticsClient ac) throws Exception {
        JSONArray clients = new JSONArray("[{\"orgId\":700000654321,\"workspaceIds\":[\"466206000000071000\"]}]");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getWorkspaceLinkingCompatibility(clients, null);
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

    function getWorkspaceLinkingCompatibility() {
        $clients = array(
            array(
                "orgId" => 700000654321,
                "workspaceIds" => array("466206000000071000")
            )
        );
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $response = $workspace->getWorkspaceLinkingCompatibility($clients);
        print_r($response);
    }
}

$obj = new Test();
$obj->getWorkspaceLinkingCompatibility();
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

    def get_workspace_linking_compatibility(self, ac):
        clients = [
            {
                "orgId": 700000654321,
                "workspaceIds": ["466206000000071000"]
            }
        ]
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_workspace_linking_compatibility(clients)
        print(result)

obj = Sample()
obj.get_workspace_linking_compatibility(obj.ac)
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
workspace.getWorkspaceLinkingCompatibility(clients).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def get_workspace_linking_compatibility
    clients = [
      {
        "orgId" => 700000654321,
        "workspaceIds" => ["466206000000071000"]
      }
    ]
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_workspace_linking_compatibility(clients)
    puts result
  end
end

obj = Sample.new
obj.get_workspace_linking_compatibility
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"clients": [{"orgId": 700000654321, "workspaceIds": ["466206000000071000"]}]};
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/linkedworkspaces/compatibility?CONFIG=" + zoho.encryption.urlEncode(config.toString())
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Workspace Linking Compatibility](../../../domains/workspace-management/linked-workspaces/get-workspace-linking-compatibility.md) - full endpoint reference.
- [Linked Workspaces overview](../../../domains/workspace-management/linked-workspaces/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
