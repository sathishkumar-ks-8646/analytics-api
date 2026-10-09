---
type: SDK Example
title: SDK examples - Add Favourite Workspace
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/favorite (addFavoriteWorkspace)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/favorite"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - workspace-management
  - workspace-preferences
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
  operation_id: addFavoriteWorkspace
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/favorite"
  endpoint_doc: "/domains/workspace-management/workspace-preferences/add-favorite-workspace.md"
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
    last_modified: 2026-10-09T13:04:25Z
  - id: endpoint-doc
    resource: "/domains/workspace-management/workspace-preferences/add-favorite-workspace.md"
    title: Endpoint reference - Add Favourite Workspace
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Add Favourite Workspace](../../../domains/workspace-management/workspace-preferences/add-favorite-workspace.md) (`POST /restapi/v2/workspaces/{workspace-id}/favorite`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/favorite" \
  -X 'POST' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>'
```

## C#

```csharp
using System;
using ZohoAnalytics;

namespace ZohoAnalyticsTest
{
    class Program
    {
        long orgId = 55522777;
        long workspaceId = 35130000001055707;

        public void AddFavoriteWorkspace(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.AddFavorite();
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            try
            {
                IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
                Program obj = new Program();
                obj.AddFavoriteWorkspace(ac);
            }
            catch (ServerException ex) { Console.WriteLine("Server exception - " + ex.GetErrorMessage()); }
            catch (Exception ex) { Console.WriteLine("Other exception - " + ex.Message); }
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

var(
    clientId = "1000.xxxxxxx"
    clientSecret = "xxxxxxx"
    refreshToken = "1000.xxxxxxx.xxxxxxx"
    orgId = "55522777"
    workspaceId = "35130000001055707"
)

func AddFavoriteWorkspace(ac ZAnalytics.Client) {
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    err := workspace.AddFavorite()
    if err != nil {
        fmt.Println(err.ErrorMessage)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    AddFavoriteWorkspace(ac)
}
```

## Java

```java
import com.zoho.analytics.client.*;

public class Test {
    private long orgId = 55522777l;
    private long workspaceId = 35130000001055707l;

    public static void main(String args[]) {
        String clientId = "1000.xxxxxxx";
        String clientSecret = "xxxxxxx";
        String refreshToken = "1000.xxxxxxx.xxxxxxx";
        Test tObj = new Test();
        AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
        try { tObj.addFavoriteWorkspace(ac); }
        catch (ServerException ex) { System.out.println("Server exception - " + ex.getErrorCode() + " : " + ex.getErrorMessage()); }
        catch (Exception ex) { ex.printStackTrace(); }
    }

    public void addFavoriteWorkspace(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.addFavorite();
        System.out.println("success");
    }
}
```

## PHP

```php
<?php
    require 'AnalyticsClient.php';
    class Test {
        public $ac = NULL;
        public $client_id = "1000.xxxxxxx";
        public $client_secret = "xxxxxxx";
        public $refresh_token = "1000.xxxxxxx.xxxxxxx";
        public $org_id = "55522777";
        public $workspace_id = "35130000001055707";
        function __construct() { $this->ac = new AnalyticsClient($this->client_id, $this->client_secret, $this->refresh_token); }
        function addFavoriteWorkspace() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->addFavorite();
            echo "success\n";
        }
    }
    $test_obj = new Test();
    try { $test_obj->addFavoriteWorkspace(); }
    catch(ServerException $se) { echo "Server exception : " . $se->getErrorMessage() . "\n"; }
    catch(Exception $e) { echo "Exception : " . $e->getMessage() . "\n"; }
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
    def add_favorite_workspace(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.add_favorite()
        print("success")

try:
    obj = sample()
    obj.add_favorite_workspace(obj.ac)
except Exception as e:
    print(str(e))
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var workspace = ac.getWorkspaceInstance('55522777', '35130000001055707');
workspace.addFavorite().then(function () {
    console.log('success');
}).catch(function (err) { console.log(err); });
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
    @ac = AnalyticsClient.new
           .with_data_center("US")
           .with_oauth({"clientId" => "1000.xxxxxxx", "clientSecret" => "xxxxxxx", "refreshToken" => "1000.xxxxxxx.xxxxxxx"})
           .build
  end
  def add_favorite_workspace
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.add_favorite
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.add_favorite_workspace
rescue ServerError => e
  puts "Server Error: #{e.response_content}"
rescue StandardError => e
  puts e.message
end
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/favorite"
  type :POST
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Add Favourite Workspace](../../../domains/workspace-management/workspace-preferences/add-favorite-workspace.md) - full endpoint reference.
- [Workspace Preferences overview](../../../domains/workspace-management/workspace-preferences/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
