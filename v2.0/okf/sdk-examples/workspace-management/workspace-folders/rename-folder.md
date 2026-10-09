---
type: SDK Example
title: SDK examples - Rename Folder
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id}/folders/{folder-id} (renameFolder)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}"
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
  operation_id: renameFolder
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}"
  endpoint_doc: "/domains/workspace-management/workspace-folders/rename-folder.md"
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
    resource: "/domains/workspace-management/workspace-folders/rename-folder.md"
    title: Endpoint reference - Rename Folder
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Rename Folder](../../../domains/workspace-management/workspace-folders/rename-folder.md) (`PUT /restapi/v2/workspaces/{workspace-id}/folders/{folder-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/folders/<folder-id>" \
  -X 'PUT' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"folderName":"Archived Reports","folderDesc":"Reports retained for audit"}'
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
        long folderId = 1767024000000143002;

        public void RenameFolder(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("folderDesc", "Reports retained for audit");
            workspace.RenameFolder(folderId, "Archived Reports", config);
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
                obj.RenameFolder(ac);
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
    folderId = "1767024000000143002"
)

func RenameFolder(ac ZAnalytics.Client) {
    config := map[string]interface{}{
        "folderDesc": "Reports retained for audit",
    }
    folderName := "Archived Reports"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    err := workspace.RenameFolder(folderId, folderName, config)
    if err != nil {
        fmt.Println(err.ErrorMessage)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    RenameFolder(ac)
}
```

## Java

```java
import com.zoho.analytics.client.*;

public class Test {
    private long orgId = 55522777l;
    private long workspaceId = 35130000001055707l;
    private long folderId = 1767024000000143002l;

    public static void main(String args[]) {
        String clientId = "1000.xxxxxxx";
        String clientSecret = "xxxxxxx";
        String refreshToken = "1000.xxxxxxx.xxxxxxx";
        Test tObj = new Test();
        AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
        try { tObj.renameFolder(ac); }
        catch (ServerException ex) { System.out.println("Server exception - " + ex.getErrorCode() + " : " + ex.getErrorMessage()); }
        catch (Exception ex) { ex.printStackTrace(); }
    }

    public void renameFolder(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject config = new JSONObject();
        config.put("folderDesc", "Reports retained for audit");
        workspace.renameFolder(folderId, "Archived Reports", config);
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
        public $folder_id = "1767024000000143002";
        function __construct() { $this->ac = new AnalyticsClient($this->client_id, $this->client_secret, $this->refresh_token); }
        function renameFolder() {
            $folder_name = "Archived Reports";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $config = array("folderDesc" => "Reports retained for audit");
            $workspace->renameFolder($this->folder_id, $folder_name, $config);
            echo "success\n";
        }
    }
    $test_obj = new Test();
    try { $test_obj->renameFolder(); }
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
    FOLDERID = "1767024000000143002"

class sample:
    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)
    def rename_folder(self, ac):
        folder_name = "Archived Reports"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        config = {"folderDesc": "Reports retained for audit"}
        workspace.rename_folder(Config.FOLDERID, folder_name, config)
        print("success")

try:
    obj = sample()
    obj.rename_folder(obj.ac)
except Exception as e:
    print(str(e))
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var workspace = ac.getWorkspaceInstance('55522777', '35130000001055707');
var folderId = '1767024000000143002';
var config = { 'folderDesc': 'Reports retained for audit' };
workspace.renameFolder(folderId, 'Archived Reports', config).then(function () {
    console.log('success');
}).catch(function (err) { console.log(err); });
```

## Ruby

```ruby
require 'zoho_analytics_client'

class Config
  ORGID = "55522777"
  WORKSPACEID = "35130000001055707"
  FOLDERID = "1767024000000143002"
end

class Sample
  def initialize
    @ac = AnalyticsClient.new
           .with_data_center("US")
           .with_oauth({"clientId" => "1000.xxxxxxx", "clientSecret" => "xxxxxxx", "refreshToken" => "1000.xxxxxxx.xxxxxxx"})
           .build
  end
  def rename_folder
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    config = { "folderDesc" => "Reports retained for audit" }
    workspace.rename_folder(Config::FOLDERID, "Archived Reports", config)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.rename_folder
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
folderId = "1767024000000143002";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"folderName":"Archived Reports","folderDesc":"Reports retained for audit"};
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/folders/" + folderId
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Rename Folder](../../../domains/workspace-management/workspace-folders/rename-folder.md) - full endpoint reference.
- [Workspace Folders overview](../../../domains/workspace-management/workspace-folders/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
