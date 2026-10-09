---
type: SDK Example
title: SDK examples - Batch Import Data into New Table
description: "Code samples in 9 languages for POST /restapi/v2/bulk/workspaces/{workspace-id}/data/batch (batchImportNewTable)."
resource: "https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/{workspace-id}/data/batch"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - data-operations
  - async-data-import
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
  operation_id: batchImportNewTable
  method: POST
  path: "/restapi/v2/bulk/workspaces/{workspace-id}/data/batch"
  endpoint_doc: "/domains/data-operations/async-data-import/batch-import-new-table.md"
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
    resource: "/domains/data-operations/async-data-import/batch-import-new-table.md"
    title: Endpoint reference - Batch Import Data into New Table
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Batch Import Data into New Table](../../../domains/data-operations/async-data-import/batch-import-new-table.md) (`POST /restapi/v2/bulk/workspaces/{workspace-id}/data/batch`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/35130000001055707/data/batch" -X 'POST' -H 'ZANALYTICS-ORGID: 55522777' -H 'Authorization: Zoho-oauthtoken <access_token>' -F 'FILE=@/home/local/Sales.csv' -F 'CONFIG={"batchKey":"start","isLastBatch":false,"tableName":"Sales","autoIdentify":true,"onError":"skiprow"}'
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

        public void ImportBulkDataInNewTableAsBatches(IAnalyticsClient ac)
        {
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("onError", "skiprow");
            IBulkAPI bulk = ac.GetBulkInstance(orgId, workspaceId);
            long jobId = bulk.ImportBulkDataInNewTableAsBatches("Sales", true, "/home/local/Sales.csv", 5000, config);
            Console.WriteLine(jobId);
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
                obj.ImportBulkDataInNewTableAsBatches(ac);
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

func ImportBulkDataInNewTableAsBatches(ac ZAnalytics.Client) {
    config := map[string]interface{}{}
    config["onError"] = "skiprow"
    bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
    jobId, err := bulk.ImportBulkDataInNewTableAsBatches("Sales", "true", "/home/local/Sales.csv", 5000, config)
    if err != nil {
        fmt.Println("Error - " + err.ErrorMessage)
    } else {
        fmt.Println(jobId)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    ImportBulkDataInNewTableAsBatches(ac)
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
            tObj.importDataInNewTableAsBatches(ac);
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

    public void importDataInNewTableAsBatches(AnalyticsClient ac) throws Exception {
        JSONObject config = new JSONObject();
        config.put("onError", "skiprow");
        BulkAPI bulk = ac.getBulkInstance(orgId, workspaceId);
        long jobId = bulk.importDataInNewTableAsBatches("Sales", true, "/home/local/Sales.csv", 5000, config, null);
        System.out.println(jobId);
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

        function importBulkDataInNewTableAsBatches() {
            $config = array();
            $config["onError"] = "skiprow";
            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $job_id = $bulk->importBulkDataInNewTableAsBatches("Sales", true, "/home/local/Sales.csv", 5000, $config);
            print_r($job_id);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->importBulkDataInNewTableAsBatches();
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

    def import_data_in_new_table_as_batches(self, ac):
        config = {}
        config["onError"] = "skiprow"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        job_id = bulk.import_data_in_new_table_as_batches("Sales", True, "/home/local/Sales.csv", 5000, config)
        print(job_id)

try:
    obj = sample()
    obj.import_data_in_new_table_as_batches(obj.ac)

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

var config = { "onError": "skiprow" };
var bulk = ac.getBulkInstance(orgId, workspaceId);
bulk.importDataInNewTableAsBatches('Sales', true, '/home/local/Sales.csv', 5000, config).then((jobId) => {
    console.log(jobId);
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

  def import_data_in_new_table_as_batches
    config = { "onError" => "skiprow" }
    bulk = @ac.get_bulk_instance(Config::ORGID, Config::WORKSPACEID)
    job_id = bulk.import_data_in_new_table_as_batches("Sales", true, "/home/local/Sales.csv", 5000, config)
    puts job_id
  end
end

begin
  obj = Sample.new
  obj.import_data_in_new_table_as_batches
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
fileObj = invokeurl
[
  url :"https://www.zylker.com/files/Sales.csv"
  type :GET
];
config = Map();
config.put("batchKey", "start");
config.put("isLastBatch", false);
config.put("tableName", "Sales");
config.put("autoIdentify", true);
config.put("onError", "skiprow");
parametersMap = Map();
parametersMap.put("CONFIG", config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/" + workspaceId + "/data/batch"
  type :POST
  parameters:parametersMap
  files:fileObj
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Batch Import Data into New Table](../../../domains/data-operations/async-data-import/batch-import-new-table.md) - full endpoint reference.
- [Asynchronous & Batch Data Import overview](../../../domains/data-operations/async-data-import/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
