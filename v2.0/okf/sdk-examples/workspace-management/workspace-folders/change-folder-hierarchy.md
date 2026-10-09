---
type: SDK Example
title: SDK examples - Change Folder Hierarchy
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/move (changeFolderHierarchy)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/move"
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
  operation_id: changeFolderHierarchy
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/move"
  endpoint_doc: "/domains/workspace-management/workspace-folders/change-folder-hierarchy.md"
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
    resource: "/domains/workspace-management/workspace-folders/change-folder-hierarchy.md"
    title: Endpoint reference - Change Folder Hierarchy
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

Code samples for [Change Folder Hierarchy](../../../domains/workspace-management/workspace-folders/change-folder-hierarchy.md) (`PUT /restapi/v2/workspaces/{workspace-id}/folders/{folder-id}/move`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/folders/<folder-id>/move" \
  -X 'PUT' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"hierarchy":1,"parentFolderId":"1767024000004578021"}'
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
        long folderId = 1767024000000143002;

        public void ChangeFolderHierarchy(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            int hierarchy = 1;
            long parentFolderId = 1767024000004578021L;
            workspace.ChangeFolderHierarchy(folderId, hierarchy, parentFolderId, null);
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
                obj.ChangeFolderHierarchy(ac);
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

func ChangeFolderHierarchy(ac ZAnalytics.Client) {
    config := map[string]interface{}{
        "hierarchy": 1,
        "parentFolderId": "1767024000004578021",
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    err := workspace.ChangeFolderHierarchy(folderId, config)
    if err != nil {
        fmt.Println(err.ErrorMessage)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    ChangeFolderHierarchy(ac)
}
```

## Java

```java
import com.zoho.analytics.client.*;
import org.json.*;

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
        try { tObj.changeFolderHierarchy(ac); }
        catch (ServerException ex) { System.out.println("Server exception - " + ex.getErrorCode() + " : " + ex.getErrorMessage()); }
        catch (Exception ex) { ex.printStackTrace(); }
    }

    public void changeFolderHierarchy(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject config = new JSONObject();
        config.put("hierarchy", 1);
        config.put("parentFolderId", "1767024000004578021");
        workspace.changeFolderHierarchy(folderId, config);
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
        function changeFolderHierarchy() {
            $hierarchy = "1";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->changeFolderHierarchy($this->folder_id, $hierarchy);
            echo "success\n";
        }
    }
    $test_obj = new Test();
    try { $test_obj->changeFolderHierarchy(); }
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
    def change_folder_hierarchy(self, ac):
        config = {"hierarchy": 1, "parentFolderId": "1767024000004578021"}
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.change_folder_hierarchy(Config.FOLDERID, config)
        print("success")

try:
    obj = sample()
    obj.change_folder_hierarchy(obj.ac)
except Exception as e:
    print(str(e))
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var workspace = ac.getWorkspaceInstance('55522777', '35130000001055707');
var folderId = '1767024000000143002';
var hierarchy = 1;
workspace.changeFolderHierarchy(folderId, hierarchy).then(function () {
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
  def change_folder_hierarchy
    config = {"hierarchy" => 1, "parentFolderId" => "1767024000004578021"}
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.change_folder_hierarchy(Config::FOLDERID, config)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.change_folder_hierarchy
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
config = {"hierarchy":1,"parentFolderId":"1767024000004578021"};
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/folders/" + folderId + "/move"
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Change Folder Hierarchy](../../../domains/workspace-management/workspace-folders/change-folder-hierarchy.md) - full endpoint reference.
- [Workspace Folders overview](../../../domains/workspace-management/workspace-folders/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
