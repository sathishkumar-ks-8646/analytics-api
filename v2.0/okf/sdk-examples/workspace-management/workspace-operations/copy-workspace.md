---
type: SDK Example
title: SDK examples - Copy Workspace
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id} (copyWorkspace)."
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
  operation_id: copyWorkspace
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}"
  endpoint_doc: "/domains/workspace-management/workspace-operations/copy-workspace.md"
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
    resource: "/domains/workspace-management/workspace-operations/copy-workspace.md"
    title: Endpoint reference - Copy Workspace
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Copy Workspace](../../../domains/workspace-management/workspace-operations/copy-workspace.md) (`POST /restapi/v2/workspaces/{workspace-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>" \
  -X 'POST' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"newWorkspaceName":"Cloned Workspace","newWorkspaceDesc":"Backup copy of the sales workspace","copyWithData":true}'
```

## C#

```csharp
using System;
using System.Collections.Generic;
using ZohoAnalytics;
using System.Text.Json;

namespace ZohoAnalyticsTest
{
    class Program
    {
        long orgId = 55522777;
        long workspaceId = 35130000001055707;

        public void CopyWorkspace(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            string newWorkspaceName = "Cloned Workspace";
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("newWorkspaceDesc", "Backup copy of the sales workspace");
            config.Add("copyWithData", true);
            JsonElement result = workspace.Copy(newWorkspaceName, config);
            Console.WriteLine(result);
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
                obj.CopyWorkspace(ac);
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

func CopyWorkspace(ac ZAnalytics.Client) {
    config := map[string]interface{}{
        "newWorkspaceDesc": "Backup copy of the sales workspace",
        "copyWithData": true,
    }
    newWorkspaceName := "Cloned Workspace"
    destOrgId := ""
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, _ := workspace.Copy(newWorkspaceName, config, destOrgId)
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CopyWorkspace(ac)
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
        try { tObj.copyWorkspace(ac); }
        catch (ServerException ex) { System.out.println("Server exception - " + ex.getErrorCode() + " : " + ex.getErrorMessage()); }
        catch (Exception ex) { ex.printStackTrace(); }
    }

    public void copyWorkspace(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        String newWorkspaceName = "Cloned Workspace";
        Long destOrgId = null;
        JSONObject config = new JSONObject();
        config.put("newWorkspaceDesc", "Backup copy of the sales workspace");
        config.put("copyWithData", true);
        long result = workspace.copy(newWorkspaceName, config, destOrgId);
        System.out.println(result);
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
        function copyWorkspace() {
            $new_workspace_name = "Cloned Workspace";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $config = array("newWorkspaceDesc" => "Backup copy of the sales workspace", "copyWithData" => true);
            $response = $workspace->copy($new_workspace_name, $config);
            print_r($response);
        }
    }
    $test_obj = new Test();
    try { $test_obj->copyWorkspace(); }
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
    def copy_workspace(self, ac):
        new_workspace_name = "Cloned Workspace"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        config = {"newWorkspaceDesc": "Backup copy of the sales workspace", "copyWithData": True}
        result = workspace.copy(new_workspace_name, config)
        print(result)

try:
    obj = sample()
    obj.copy_workspace(obj.ac)
except Exception as e:
    print(str(e))
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
var newWorkspaceName = 'Cloned Workspace';
var config = { 'newWorkspaceDesc': 'Backup copy of the sales workspace', 'copyWithData': true };
workspace.copy(newWorkspaceName, config).then(function (result) {
    console.log(result);
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
  def copy_workspace
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    config = { "newWorkspaceDesc" => "Backup copy of the sales workspace", "copyWithData" => true }
    result = workspace.copy("Cloned Workspace", config)
    puts result
  end
end

begin
  obj = Sample.new
  obj.copy_workspace
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
config = {"newWorkspaceName":"Cloned Workspace","newWorkspaceDesc":"Backup copy of the sales workspace","copyWithData":true};
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Copy Workspace](../../../domains/workspace-management/workspace-operations/copy-workspace.md) - full endpoint reference.
- [Workspace Operations overview](../../../domains/workspace-management/workspace-operations/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
