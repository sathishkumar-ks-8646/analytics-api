---
type: SDK Example
title: SDK examples - Sync Data
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}/sync (syncDatasource)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}/sync"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - data-operations
  - data-sync-and-connectivity
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
  operation_id: syncDatasource
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}/sync"
  endpoint_doc: "/domains/data-operations/data-sync-and-connectivity/sync-datasource.md"
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
    resource: "/references/openapi/data-operations-grouped-api.json"
    title: OpenAPI 3 specification - data-operations-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
  - id: endpoint-doc
    resource: "/domains/data-operations/data-sync-and-connectivity/sync-datasource.md"
    title: Endpoint reference - Sync Data
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Sync Data](../../../domains/data-operations/data-sync-and-connectivity/sync-datasource.md) (`POST /restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}/sync`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/datasources/35130000001056401/sync" -X 'POST' -H 'ZANALYTICS-ORGID: 55522777' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"userName":"john@zylker.com","password":"Zoho@123"}'
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
        long datasourceId = 35130000001056401;

        public void SyncData(IAnalyticsClient ac)
        {
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("userName", "john@zylker.com");
            config.Add("password", "Zoho@123");
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.SyncData(datasourceId, config);
            Console.WriteLine("Sync initiated");
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
                obj.SyncData(ac);
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
    workspaceId = "35130000001055707"
    datasourceId = "35130000001056401"
)

func SyncData(ac ZAnalytics.Client) {
    config := map[string]interface{}{}
    config["userName"] = "john@zylker.com"
    config["password"] = "Zoho@123"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    err := workspace.SyncData(datasourceId, config)
    if err != nil {
        fmt.Println("Error - " + err.ErrorMessage)
    } else {
        fmt.Println("Sync initiated")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    SyncData(ac)
}
```

## Java

```java
import com.zoho.analytics.client.*;
import org.json.*;

public class Test {

    private long orgId = 55522777l;
    private long workspaceId = 35130000001055707l;
    private long datasourceId = 35130000001056401l;

    public static void main(String args[]) {
        String clientId = "1000.xxxxxxx";
        String clientSecret = "xxxxxxx";
        String refreshToken = "1000.xxxxxxx.xxxxxxx";

        Test tObj = new Test();
        AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);

        try {
            tObj.syncData(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (ParseException ex) {
            System.out.println("Parser exception - ErrorMessage : " + ex.getResponseMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void syncData(AnalyticsClient ac) throws Exception {
        JSONObject config = new JSONObject();
        config.put("userName", "john@zylker.com");
        config.put("password", "Zoho@123");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.syncData(datasourceId, config);
        System.out.println("Sync initiated");
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
        public $workspace_id = "35130000001055707";
        public $datasource_id = "35130000001056401";

        function __construct() {
            $this->ac = new AnalyticsClient($this->client_id, $this->client_secret, $this->refresh_token);
        }

        function syncData() {
            $config = array();
            $config["userName"] = "john@zylker.com";
            $config["password"] = "Zoho@123";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->syncData($this->datasource_id, $config);
            echo "Sync initiated";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->syncData();
    }
    catch(ServerException $se) {
        echo "Server exception : " . $se->getErrorMessage() . "\n";
    }
    catch(IOException $ioe) {
        echo "IO exception : " . $ioe->getErrorMessage() . "\n";
    }
    catch(ParseException $pe) {
        echo "Parser exception : " . $pe->getErrorMessage() . "\n";
    }
    catch(Exception $e) {
        echo "Exception : " . $e->getMessage() . "\n";
    }
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
    DATASOURCEID = "35130000001056401"

class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def sync_data(self, ac):
        config = {}
        config["userName"] = "john@zylker.com"
        config["password"] = "Zoho@123"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.sync_data(Config.DATASOURCEID, config)
        print("Sync initiated")

try:
    obj = sample()
    obj.sync_data(obj.ac)

except Exception as e:
    print(str(e))
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');

var clientId = '1000.xxxxxxx';
var clientSecret = 'xxxxxxx';
var refreshtoken = '1000.xxxxxxx.xxxxxxx';
var orgId = '55522777';
var workspaceId = '35130000001055707';
var datasourceId = '35130000001056401';

var ac = new analyticsClient(clientId, clientSecret, refreshtoken);

var config = { "userName": "john@zylker.com", "password": "Zoho@123" };
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.syncData(datasourceId, config).then(() => {
    console.log('Sync initiated');
}).catch((error) => {
    console.log('errorCode : ' + error.errorCode);
    console.log('errorMessage : ' + error.errorMessage);
});
```

## Ruby

```ruby
require 'zoho_analytics_client'

class Config
  ORGID = "55522777"
  WORKSPACEID = "35130000001055707"
  DATASOURCEID = "35130000001056401"
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

  def sync_data
    config = { "userName" => "john@zylker.com", "password" => "Zoho@123" }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.sync_data(Config::DATASOURCEID, config)
    puts "Sync initiated"
  end
end

begin
  obj = Sample.new
  obj.sync_data
rescue ServerError => e
  puts "Server Error: \#{e.response_content}"
rescue StandardError => e
  puts e.message
end
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
datasourceId = "35130000001056401";

headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("userName", "john@zylker.com");
config.put("password", "Zoho@123");
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/datasources/" + datasourceId + "/sync"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Sync Data](../../../domains/data-operations/data-sync-and-connectivity/sync-datasource.md) - full endpoint reference.
- [Data Sync & Connectivity overview](../../../domains/data-operations/data-sync-and-connectivity/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
