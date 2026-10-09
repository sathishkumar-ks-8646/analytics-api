---
type: SDK Example
title: SDK examples - Create Workspace
description: Code samples in 9 languages for POST /restapi/v2/workspaces (createWorkspace).
resource: https://analyticsapi.zoho.com/restapi/v2/workspaces
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
  operation_id: createWorkspace
  method: POST
  path: "/restapi/v2/workspaces"
  endpoint_doc: "/domains/workspace-management/workspace-operations/create-workspace.md"
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
    last_modified: 2026-10-09T14:14:03Z
  - id: endpoint-doc
    resource: "/domains/workspace-management/workspace-operations/create-workspace.md"
    title: Endpoint reference - Create Workspace
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

Code samples for [Create Workspace](../../../domains/workspace-management/workspace-operations/create-workspace.md) (`POST /restapi/v2/workspaces`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces" \
  -X 'POST' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"workspaceName":"Sales Analytics","workspaceDesc":"Workspace for quarterly sales"}'
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

        public void CreateWorkspace(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            string workspaceName = "Sales Analytics";
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("workspaceDesc", "Workspace for quarterly sales");
            JsonElement result = org.CreateWorkspace(workspaceName, config);
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
                obj.CreateWorkspace(ac);
            }
            catch (ServerException ex)
            {
                Console.WriteLine("Server exception - " + ex.GetErrorMessage());
            }
            catch (Exception ex)
            {
                Console.WriteLine("Other exception - " + ex.Message);
            }
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
)

func CreateWorkspace(ac ZAnalytics.Client) {
    config := map[string]interface{}{
        "workspaceDesc": "Workspace for quarterly sales",
    }
    workspaceName := "Sales Analytics"
    org := ZAnalytics.GetOrgInstance(&ac, orgId)
    result, _ := org.CreateWorkspace(workspaceName, config)
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateWorkspace(ac)
}
```

## Java

```java
import com.zoho.analytics.client.*;
import org.json.*;

public class Test {
    private long orgId = 55522777l;

    public static void main(String args[]) {
        String clientId = "1000.xxxxxxx";
        String clientSecret = "xxxxxxx";
        String refreshToken = "1000.xxxxxxx.xxxxxxx";

        Test tObj = new Test();
        AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);

        try {
            tObj.createWorkspace(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void createWorkspace(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        String workspaceName = "Sales Analytics";
        JSONObject config = new JSONObject();
        config.put("workspaceDesc", "Workspace for quarterly sales");
        long result = org.createWorkspace(workspaceName, config);
        System.out.println(result);
    }
}
```

## PHP

```php
<?php

    require 'AnalyticsClient.php';

    class Test
    {
        public $ac = NULL;
        public $client_id = "1000.xxxxxxx";
        public $client_secret = "xxxxxxx";
        public $refresh_token = "1000.xxxxxxx.xxxxxxx";

        public $org_id = "55522777";

        function __construct() {
            $this->ac = new AnalyticsClient($this->client_id, $this->client_secret, $this->refresh_token);
        }

        function createWorkspace() {
            $workspace_name = "Sales Analytics";
            $org = $this->ac->getOrgInstance($this->org_id);
            $config = array("workspaceDesc" => "Workspace for quarterly sales");
            $response = $org->createWorkspace($workspace_name, $config);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->createWorkspace();
    }
    catch(ServerException $se) {
        echo "Server exception : " . $se->getErrorMessage() . "\n";
    }
    catch(Exception $e) {
        echo "Exception : " . $e->getMessage() . "\n";
    }
?>
```

## Python

```python
from AnalyticsClient import AnalyticsClient
import sys

class Config:
    CLIENTID = "1000.xxxxxxx"
    CLIENTSECRET = "xxxxxxx"
    REFRESHTOKEN = "1000.xxxxxxx.xxxxxxx"
    ORGID = "55522777"

class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def create_workspace(self, ac):
        workspace_name = "Sales Analytics"
        org = ac.get_org_instance(Config.ORGID)
        config = {"workspaceDesc": "Workspace for quarterly sales"}
        result = org.create_workspace(workspace_name, config)
        print(result)

try:
    obj = sample()
    obj.create_workspace(obj.ac)
except Exception as e:
    print(str(e))
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');

var clientId = '1000.xxxxxxx';
var clientSecret = 'xxxxxxx';
var refreshToken = '1000.xxxxxxx.xxxxxxx';
var orgId = '55522777';

var ac = new analyticsClient(clientId, clientSecret, refreshToken);

var org = ac.getOrgInstance(orgId);
var workspaceName = 'Sales Analytics';

var config = { 'workspaceDesc': 'Workspace for quarterly sales' };
org.createWorkspace(workspaceName, config).then(function (result) {
    console.log(result);
}).catch(function (err) {
    console.log(err);
});
```

## Ruby

```ruby
require 'zoho_analytics_client'

class Config
  ORGID = "55522777"
end

class Sample
  def initialize
    @ac = AnalyticsClient.new
           .with_data_center("US")
           .with_oauth({
             "clientId" => "1000.xxxxxxx",
             "clientSecret" => "xxxxxxx",
             "refreshToken" => "1000.xxxxxxx.xxxxxxx"
           })
           .build
  end

  def create_workspace
    workspace_name = "Sales Analytics"
    org = @ac.get_org_instance(Config::ORGID)
    config = { "workspaceDesc" => "Workspace for quarterly sales" }
    result = org.create_workspace(workspace_name, config)
    puts result
  end
end

begin
  obj = Sample.new
  obj.create_workspace
rescue ServerError => e
  puts "Server Error: #{e.response_content}"
rescue StandardError => e
  puts e.message
  puts e.backtrace.join("\n")
end
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"workspaceName":"Sales Analytics","workspaceDesc":"Workspace for quarterly sales"};
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Create Workspace](../../../domains/workspace-management/workspace-operations/create-workspace.md) - full endpoint reference.
- [Workspace Operations overview](../../../domains/workspace-management/workspace-operations/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
