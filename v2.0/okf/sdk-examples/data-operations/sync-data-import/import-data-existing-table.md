---
type: SDK Example
title: SDK examples - Import Data into an Existing Table (Synchronous)
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/data (importDataExistingTable)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - data-operations
  - sync-data-import
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
  operation_id: importDataExistingTable
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data"
  endpoint_doc: "/domains/data-operations/sync-data-import/import-data-existing-table.md"
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
    last_modified: 2026-10-09T08:29:02Z
  - id: endpoint-doc
    resource: "/domains/data-operations/sync-data-import/import-data-existing-table.md"
    title: Endpoint reference - Import Data into an Existing Table (Synchronous)
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Import Data into an Existing Table (Synchronous)](../../../domains/data-operations/sync-data-import/import-data-existing-table.md) (`POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/data`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/data" -X 'POST' -H 'ZANALYTICS-ORGID: 55522777' -H 'Authorization: Zoho-oauthtoken <access_token>' -F 'FILE=@/home/local/Sales.csv' -F 'CONFIG={"importType":"append","fileType":"csv","autoIdentify":true,"onError":"skiprow"}'
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
        long viewId = 35130000001055717;

        public void ImportData(IAnalyticsClient ac)
        {
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("onError", "skiprow");
            IBulkAPI bulk = ac.GetBulkInstance(orgId, workspaceId);
            JsonElement result = bulk.ImportData(viewId, "append", "csv", true, "/home/local/Sales.csv", config);
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
                obj.ImportData(ac);
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
    viewId = "35130000001055717"
)

func ImportData(ac ZAnalytics.Client) {
    config := map[string]interface{}{}
    config["onError"] = "skiprow"
    bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
    result, err := bulk.ImportData(viewId, "append", "csv", "true", "/home/local/Sales.csv", config)
    if err != nil {
        fmt.Println("Error - " + err.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    ImportData(ac)
}
```

## Java

```java
import com.zoho.analytics.client.*;
import org.json.*;

public class Test {

    private long orgId = 55522777l;
    private long workspaceId = 35130000001055707l;
    private long viewId = 35130000001055717l;

    public static void main(String args[]) {
        String clientId = "1000.xxxxxxx";
        String clientSecret = "xxxxxxx";
        String refreshToken = "1000.xxxxxxx.xxxxxxx";

        Test tObj = new Test();
        AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);

        try {
            tObj.importData(ac);
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

    public void importData(AnalyticsClient ac) throws Exception {
        JSONObject config = new JSONObject();
        config.put("onError", "skiprow");
        BulkAPI bulk = ac.getBulkInstance(orgId, workspaceId);
        JSONObject result = bulk.importData(viewId, "append", "csv", true, "/home/local/Sales.csv", config);
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
        public $view_id = "35130000001055717";

        function __construct() {
            $this->ac = new AnalyticsClient($this->client_id, $this->client_secret, $this->refresh_token);
        }

        function importData() {
            $config = array();
            $config["onError"] = "skiprow";
            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $response = $bulk->importData($this->view_id, "append", "csv", true, "/home/local/Sales.csv", $config);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->importData();
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
    VIEWID = "35130000001055717"

class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def import_data(self, ac):
        config = {}
        config["onError"] = "skiprow"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        result = bulk.import_data(Config.VIEWID, "append", "csv", True, "/home/local/Sales.csv", config)
        print(result)

try:
    obj = sample()
    obj.import_data(obj.ac)

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
var viewId = '35130000001055717';

var ac = new analyticsClient(clientId, clientSecret, refreshtoken);

var config = { "onError": "skiprow" };
var bulk = ac.getBulkInstance(orgId, workspaceId);
bulk.importData(viewId, 'append', 'csv', true, '/home/local/Sales.csv', config).then((response) => {
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
  VIEWID = "35130000001055717"
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

  def import_data
    config = { "onError" => "skiprow" }
    bulk = @ac.get_bulk_instance(Config::ORGID, Config::WORKSPACEID)
    result = bulk.import_data(Config::VIEWID, "append", "csv", true, "/home/local/Sales.csv", config)
    puts result
  end
end

begin
  obj = Sample.new
  obj.import_data
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
viewId = "35130000001055717";

headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
fileObj = invokeurl
[
  url :"https://www.zylker.com/files/Sales.csv"
  type :GET
];
config = Map();
config.put("importType", "append");
config.put("fileType", "csv");
config.put("autoIdentify", true);
config.put("onError", "skiprow");
parametersMap = Map();
parametersMap.put("CONFIG", config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/" + viewId + "/data"
  type :POST
  parameters:parametersMap
  files:fileObj
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Import Data into an Existing Table (Synchronous)](../../../domains/data-operations/sync-data-import/import-data-existing-table.md) - full endpoint reference.
- [Synchronous Data Import overview](../../../domains/data-operations/sync-data-import/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
