---
type: SDK Example
title: SDK examples - Create Export Job using View ID (Asynchronous)
description: "Code samples in 9 languages for GET /restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data (createExportJobViewId)."
resource: "https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - data-operations
  - async-data-export
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
  operation_id: createExportJobViewId
  method: GET
  path: "/restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data"
  endpoint_doc: "/domains/data-operations/async-data-export/create-export-job-view-id.md"
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
    resource: "/domains/data-operations/async-data-export/create-export-job-view-id.md"
    title: Endpoint reference - Create Export Job using View ID (Asynchronous)
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Create Export Job using View ID (Asynchronous)](../../../domains/data-operations/async-data-export/create-export-job-view-id.md) (`GET /restapi/v2/bulk/workspaces/{workspace-id}/views/{view-id}/data`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/35130000001055707/views/35130000001055717/data" -H 'ZANALYTICS-ORGID: 55522777' -H 'Authorization: Zoho-oauthtoken <access_token>' --get --data-urlencode "CONFIG={\"responseFormat\":\"csv\",\"criteria\":\"\\\"SalesTable\\\".\\\"Region\\\"='East'\"}"
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

        public void InitiateBulkExport(IAnalyticsClient ac)
        {
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("criteria", "\"SalesTable\".\"Region\"='East'");
            IBulkAPI bulk = ac.GetBulkInstance(orgId, workspaceId);
            long jobId = bulk.InitiateBulkExport(viewId, "csv", config);
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
                obj.InitiateBulkExport(ac);
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

func InitiateBulkExport(ac ZAnalytics.Client) {
    config := map[string]interface{}{}
    config["criteria"] = `"SalesTable"."Region"='East'`
    bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
    jobId, err := bulk.InitiateBulkExport(viewId, "csv", config)
    if err != nil {
        fmt.Println("Error - " + err.ErrorMessage)
    } else {
        fmt.Println(jobId)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    InitiateBulkExport(ac)
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
            tObj.initiateBulkExport(ac);
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

    public void initiateBulkExport(AnalyticsClient ac) throws Exception {
        JSONObject config = new JSONObject();
        config.put("criteria", "\"SalesTable\".\"Region\"='East'");
        BulkAPI bulk = ac.getBulkInstance(orgId, workspaceId);
        long jobId = bulk.initiateBulkExport(viewId, "csv", config);
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
        public $view_id = "35130000001055717";

        function __construct() {
            $this->ac = new AnalyticsClient($this->client_id, $this->client_secret, $this->refresh_token);
        }

        function initiateBulkExport() {
            $config = array();
            $config["criteria"] = "\"SalesTable\".\"Region\"='East'";
            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $job_id = $bulk->initiateBulkExport($this->view_id, "csv", $config);
            print_r($job_id);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->initiateBulkExport();
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

    def initiate_bulk_export(self, ac):
        config = {}
        config["criteria"] = "\"SalesTable\".\"Region\"='East'"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        job_id = bulk.initiate_bulk_export(Config.VIEWID, "csv", config)
        print(job_id)

try:
    obj = sample()
    obj.initiate_bulk_export(obj.ac)

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

var config = { "criteria": '"SalesTable"."Region"=\'East\'' };
var bulk = ac.getBulkInstance(orgId, workspaceId);
bulk.initiateBulkExport(viewId, 'csv', config).then((jobId) => {
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

  def initiate_bulk_export
    config = { "criteria" => "\"SalesTable\".\"Region\"='East'" }
    bulk = @ac.get_bulk_instance(Config::ORGID, Config::WORKSPACEID)
    job_id = bulk.initiate_bulk_export(Config::VIEWID, "csv", config)
    puts job_id
  end
end

begin
  obj = Sample.new
  obj.initiate_bulk_export
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
config = Map();
config.put("responseFormat", "csv");
config.put("criteria", "\"SalesTable\".\"Region\"='East'");
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/" + workspaceId + "/views/" + viewId + "/data?CONFIG=" + zoho.encryption.urlEncode(config.toString())
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Create Export Job using View ID (Asynchronous)](../../../domains/data-operations/async-data-export/create-export-job-view-id.md) - full endpoint reference.
- [Asynchronous Data Export overview](../../../domains/data-operations/async-data-export/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
