---
type: SDK Example
title: SDK examples - Create Folder
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/folders (createFolder)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/folders"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - workspace-management
  - workspace-folders
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
  operation_id: createFolder
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/folders"
  endpoint_doc: "/domains/workspace-management/workspace-folders/create-folder.md"
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
    resource: "/domains/workspace-management/workspace-folders/create-folder.md"
    title: Endpoint reference - Create Folder
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

Code samples for [Create Folder](../../../domains/workspace-management/workspace-folders/create-folder.md) (`POST /restapi/v2/workspaces/{workspace-id}/folders`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/folders" \
  -X 'POST' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"folderName":"My Tables","folderDesc":"Folder for storing new tables","parentFolderId":1767024000000143002}'
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

        public void CreateFolder(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            string folderName = "My Tables";
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("folderDesc", "Folder for storing new tables");
            config.Add("parentFolderId", 1767024000000143002L);
            JsonElement result = workspace.CreateFolder(folderName, config);
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
                obj.CreateFolder(ac);
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

func CreateFolder(ac ZAnalytics.Client) {
    config := map[string]interface{}{
        "folderDesc": "Folder for storing new tables",
        "parentFolderId": "1767024000000143002",
    }
    folderName := "My Tables"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, _ := workspace.CreateFolder(folderName, config)
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateFolder(ac)
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
        try { tObj.createFolder(ac); }
        catch (ServerException ex) { System.out.println("Server exception - " + ex.getErrorCode() + " : " + ex.getErrorMessage()); }
        catch (Exception ex) { ex.printStackTrace(); }
    }

    public void createFolder(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        String folderName = "My Tables";
        JSONObject config = new JSONObject();
        config.put("folderDesc", "Folder for storing new tables");
        config.put("parentFolderId", 1767024000000143002l);
        long result = workspace.createFolder(folderName, config);
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
        function createFolder() {
            $folder_name = "My Tables";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $config = array("folderDesc" => "Folder for storing new tables", "parentFolderId" => "1767024000000143002");
            $response = $workspace->createFolder($folder_name, $config);
            print_r($response);
        }
    }
    $test_obj = new Test();
    try { $test_obj->createFolder(); }
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
    def create_folder(self, ac):
        folder_name = "My Tables"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        config = {"folderDesc": "Folder for storing new tables", "parentFolderId": "1767024000000143002"}
        result = workspace.create_folder(folder_name, config)
        print(result)

try:
    obj = sample()
    obj.create_folder(obj.ac)
except Exception as e:
    print(str(e))
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var workspace = ac.getWorkspaceInstance('55522777', '35130000001055707');
var folderName = 'My Tables';
var config = { 'folderDesc': 'Folder for storing new tables', 'parentFolderId': '1767024000000143002' };
workspace.createFolder(folderName, config).then(function (result) {
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
  def create_folder
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    config = { "folderDesc" => "Folder for storing new tables", "parentFolderId" => "1767024000000143002" }
    result = workspace.create_folder("My Tables", config)
    puts result
  end
end

begin
  obj = Sample.new
  obj.create_folder
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
config = {"folderName":"My Tables","folderDesc":"Folder for storing new tables","parentFolderId":1767024000000143002};
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/folders"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Create Folder](../../../domains/workspace-management/workspace-folders/create-folder.md) - full endpoint reference.
- [Workspace Folders overview](../../../domains/workspace-management/workspace-folders/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
