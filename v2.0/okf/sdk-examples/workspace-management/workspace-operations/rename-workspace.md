---
type: SDK Example
title: SDK examples - Rename Workspace
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id} (renameWorkspace)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - workspace-management
  - workspace-operations
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
  operation_id: renameWorkspace
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}"
  endpoint_doc: "/domains/workspace-management/workspace-operations/rename-workspace.md"
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
    last_modified: 2026-10-09T08:29:02Z
  - id: endpoint-doc
    resource: "/domains/workspace-management/workspace-operations/rename-workspace.md"
    title: Endpoint reference - Rename Workspace
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Rename Workspace](../../../domains/workspace-management/workspace-operations/rename-workspace.md) (`PUT /restapi/v2/workspaces/{workspace-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>" \
  -X 'PUT' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"workspaceName":"Q4 Sales Workspace","workspaceDesc":"Consolidated Q4 sales reporting"}'
```

## C#

```csharp
using System;
using System.Collections.Generic;
using ZohoAnalytics;

namespace ZohoAnalyticsTest
{
    class Program
    {
        long orgId = 55522777;
        long workspaceId = 35130000001055707;

        public void RenameWorkspace(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("workspaceDesc", "Consolidated Q4 sales reporting");
            workspace.Rename("Q4 Sales Workspace", config);
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
                obj.RenameWorkspace(ac);
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

func RenameWorkspace(ac ZAnalytics.Client) {
    config := map[string]interface{}{
        "workspaceDesc": "Consolidated Q4 sales reporting",
    }
    workspaceName := "Q4 Sales Workspace"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    err := workspace.Rename(workspaceName, config)
    if err != nil {
        fmt.Println(err.ErrorMessage)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    RenameWorkspace(ac)
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
        try { tObj.renameWorkspace(ac); }
        catch (ServerException ex) { System.out.println("Server exception - " + ex.getErrorCode() + " : " + ex.getErrorMessage()); }
        catch (Exception ex) { ex.printStackTrace(); }
    }

    public void renameWorkspace(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject config = new JSONObject();
        config.put("workspaceDesc", "Consolidated Q4 sales reporting");
        workspace.rename("Q4 Sales Workspace", config);
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
        function renameWorkspace() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $config = array("workspaceDesc" => "Consolidated Q4 sales reporting");
            $workspace->rename("Q4 Sales Workspace", $config);
            echo "success\n";
        }
    }
    $test_obj = new Test();
    try { $test_obj->renameWorkspace(); }
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
    def rename_workspace(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        config = {"workspaceDesc": "Consolidated Q4 sales reporting"}
        workspace.rename("Q4 Sales Workspace", config)
        print("success")

try:
    obj = sample()
    obj.rename_workspace(obj.ac)
except Exception as e:
    print(str(e))
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var workspace = ac.getWorkspaceInstance('55522777', '35130000001055707');
var config = { 'workspaceDesc': 'Consolidated Q4 sales reporting' };
workspace.rename('Q4 Sales Workspace', config).then(function () {
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
  def rename_workspace
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    config = { "workspaceDesc" => "Consolidated Q4 sales reporting" }
    workspace.rename("Q4 Sales Workspace", config)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.rename_workspace
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
config = {"workspaceName":"Q4 Sales Workspace","workspaceDesc":"Consolidated Q4 sales reporting"};
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Rename Workspace](../../../domains/workspace-management/workspace-operations/rename-workspace.md) - full endpoint reference.
- [Workspace Operations overview](../../../domains/workspace-management/workspace-operations/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
