---
type: SDK Example
title: SDK examples - Get Datasources
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/datasources (getDatasources)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/datasources"
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
  operation_id: getDatasources
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/datasources"
  endpoint_doc: "/domains/data-operations/data-sync-and-connectivity/get-datasources.md"
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
    resource: "/domains/data-operations/data-sync-and-connectivity/get-datasources.md"
    title: Endpoint reference - Get Datasources
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Get Datasources](../../../domains/data-operations/data-sync-and-connectivity/get-datasources.md) (`GET /restapi/v2/workspaces/{workspace-id}/datasources`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/datasources" -H 'ZANALYTICS-ORGID: 55522777' -H 'Authorization: Zoho-oauthtoken <access_token>'
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

        public void GetDatasources(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetDatasources();
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
                obj.GetDatasources(ac);
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
)

func GetDatasources(ac ZAnalytics.Client) {
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, err := workspace.GetDatasources()
    if err != nil {
        fmt.Println("Error - " + err.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetDatasources(ac)
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
            tObj.getDatasources(ac);
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

    public void getDatasources(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getDatasources();
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
        public $workspace_id = "35130000001055707";

        function __construct() {
            $this->ac = new AnalyticsClient($this->client_id, $this->client_secret, $this->refresh_token);
        }

        function getDatasources() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getDatasources();
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->getDatasources();
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

class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def get_datasources(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_datasources()
        print(result)

try:
    obj = sample()
    obj.get_datasources(obj.ac)

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

var ac = new analyticsClient(clientId, clientSecret, refreshtoken);

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.getDatasources().then((response) => {
    console.log(response);
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

  def get_datasources
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_datasources
    puts result
  end
end

begin
  obj = Sample.new
  obj.get_datasources
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

headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);

response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/datasources"
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Datasources](../../../domains/data-operations/data-sync-and-connectivity/get-datasources.md) - full endpoint reference.
- [Data Sync & Connectivity overview](../../../domains/data-operations/data-sync-and-connectivity/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
