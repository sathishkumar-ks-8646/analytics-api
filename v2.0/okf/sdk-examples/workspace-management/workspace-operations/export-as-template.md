---
type: SDK Example
title: SDK examples - Export as Template
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/template/data (exportAsTemplate)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/template/data"
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
  operation_id: exportAsTemplate
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/template/data"
  endpoint_doc: "/domains/workspace-management/workspace-operations/export-as-template.md"
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
    resource: "/domains/workspace-management/workspace-operations/export-as-template.md"
    title: Endpoint reference - Export as Template
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Export as Template](../../../domains/workspace-management/workspace-operations/export-as-template.md) (`GET /restapi/v2/workspaces/{workspace-id}/template/data`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/template/data?CONFIG=%7B%22viewIds%22%3A%5B%22176702000008549302%22%2C%22176702000008549300%22%5D%2C%22fileName%22%3A%22SalesAnalytics_Template%22%7D" \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  -o template_export.atpt
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

        public void ExportAsTemplate(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            List<long> viewIds = new List<long> { 35130000001080001L, 35130000001080082L };
            string filePath = "C:\\Users\\Administrator\\Downloads\\template.atpt";
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("fileName", "SalesAnalytics_Template");
            workspace.ExportAsTemplate(viewIds, filePath, config);
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
                obj.ExportAsTemplate(ac);
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

func ExportAsTemplate(ac ZAnalytics.Client) {
    viewIds := []string{"35130000001080001", "35130000001080082"}
    filePath := "/home/local/admin/Files/template.atpt"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    config := map[string]interface{}{
        "fileName": "SalesAnalytics_Template",
    }
    err := workspace.ExportAsTemplate(viewIds, filePath, config)
    if err != nil {
        fmt.Println(err.ErrorMessage)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    ExportAsTemplate(ac)
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
        try { tObj.exportAsTemplate(ac); }
        catch (ServerException ex) { System.out.println("Server exception - " + ex.getErrorCode() + " : " + ex.getErrorMessage()); }
        catch (Exception ex) { ex.printStackTrace(); }
    }

    public void exportAsTemplate(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray viewIds = new JSONArray();
        viewIds.put(35130000001080001L);
        viewIds.put(35130000001080082L);
        String filePath = "/home/local/admin/Files/template.atpt";
        JSONObject config = new JSONObject();
        config.put("fileName", "SalesAnalytics_Template");
        workspace.exportAsTemplate(viewIds, filePath, config);
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
        function exportAsTemplate() {
            $file_path = "/home/local/admin/Files/template.atpt";
            $view_ids = array("35130000001080001", "35130000001080082");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $config = array("fileName" => "SalesAnalytics_Template");
            $workspace->exportAsTemplate($view_ids, $file_path, $config);
            echo "success\n";
        }
    }
    $test_obj = new Test();
    try { $test_obj->exportAsTemplate(); }
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
    def export_as_template(self, ac):
        view_ids = ["35130000001080001", "35130000001080082"]
        file_path = "/home/local/admin/Files/template.atpt"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        config = {"fileName": "SalesAnalytics_Template"}
        workspace.export_as_template(view_ids, file_path, config)
        print("success")

try:
    obj = sample()
    obj.export_as_template(obj.ac)
except Exception as e:
    print(str(e))
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var workspace = ac.getWorkspaceInstance('55522777', '35130000001055707');
var viewIds = ['35130000001080001', '35130000001080082'];
var filePath = '/home/local/admin/Files/template.atpt';
var config = { 'fileName': 'SalesAnalytics_Template' };
workspace.exportAsTemplate(viewIds, filePath, config).then(function () {
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
  def export_as_template
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    view_ids = ["35130000001080001", "35130000001080082"]
    file_path = "/home/local/admin/Files/template.atpt"
    config = { "fileName" => "SalesAnalytics_Template" }
    workspace.export_as_template(view_ids, file_path, config)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.export_as_template
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
config = {"viewIds":["35130000001080001","35130000001080082"],"fileName":"SalesAnalytics_Template"};
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/template/data?CONFIG=" + zoho.encryption.urlEncode(config.toString())
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Export as Template](../../../domains/workspace-management/workspace-operations/export-as-template.md) - full endpoint reference.
- [Workspace Operations overview](../../../domains/workspace-management/workspace-operations/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
