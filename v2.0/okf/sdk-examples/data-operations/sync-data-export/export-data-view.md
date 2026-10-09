---
type: SDK Example
title: SDK examples - Export Data from a View
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/views/{view-id}/data (exportDataView)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - data-operations
  - sync-data-export
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
  operation_id: exportDataView
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data"
  endpoint_doc: "/domains/data-operations/sync-data-export/export-data-view.md"
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
    resource: "/domains/data-operations/sync-data-export/export-data-view.md"
    title: Endpoint reference - Export Data from a View
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Export Data from a View](../../../domains/data-operations/sync-data-export/export-data-view.md) (`GET /restapi/v2/workspaces/{workspace-id}/views/{view-id}/data`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/data" -H 'ZANALYTICS-ORGID: 55522777' -H 'Authorization: Zoho-oauthtoken <access_token>' --get --data-urlencode "CONFIG={\"responseFormat\":\"csv\",\"criteria\":\"\\\"SalesTable\\\".\\\"Region\\\"='East'\"}" -o Sales.csv
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

        public void ExportData(IAnalyticsClient ac)
        {
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("criteria", "\"SalesTable\".\"Region\"='East'");
            IBulkAPI bulk = ac.GetBulkInstance(orgId, workspaceId);
            bulk.ExportData(viewId, "csv", "/home/local/Sales.csv", config);
            Console.WriteLine("Exported to /home/local/Sales.csv");
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
                obj.ExportData(ac);
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

func ExportData(ac ZAnalytics.Client) {
    config := map[string]interface{}{}
    config["criteria"] = `"SalesTable"."Region"='East'`
    bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
    err := bulk.ExportData(viewId, "csv", "/home/local/Sales.csv", config)
    if err != nil {
        fmt.Println("Error - " + err.ErrorMessage)
    } else {
        fmt.Println("Exported to /home/local/Sales.csv")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    ExportData(ac)
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
            tObj.exportData(ac);
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

    public void exportData(AnalyticsClient ac) throws Exception {
        JSONObject config = new JSONObject();
        config.put("criteria", "\"SalesTable\".\"Region\"='East'");
        BulkAPI bulk = ac.getBulkInstance(orgId, workspaceId);
        bulk.exportData(viewId, "csv", "/home/local/Sales.csv", config);
        System.out.println("Exported to /home/local/Sales.csv");
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

        function exportData() {
            $config = array();
            $config["criteria"] = "\"SalesTable\".\"Region\"='East'";
            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $bulk->exportData($this->view_id, "csv", "/home/local/Sales.csv", $config);
            echo "Exported to /home/local/Sales.csv";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->exportData();
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

    def export_data(self, ac):
        config = {}
        config["criteria"] = "\"SalesTable\".\"Region\"='East'"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        bulk.export_data(Config.VIEWID, "csv", "/home/local/Sales.csv", config)
        print("Exported to /home/local/Sales.csv")

try:
    obj = sample()
    obj.export_data(obj.ac)

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
bulk.exportData(viewId, 'csv', '/home/local/Sales.csv', config).then(() => {
    console.log('Exported to /home/local/Sales.csv');
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

  def export_data
    config = { "criteria" => "\"SalesTable\".\"Region\"='East'" }
    bulk = @ac.get_bulk_instance(Config::ORGID, Config::WORKSPACEID)
    bulk.export_data(Config::VIEWID, "csv", "/home/local/Sales.csv", config)
    puts "Exported to /home/local/Sales.csv"
  end
end

begin
  obj = Sample.new
  obj.export_data
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
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/" + viewId + "/data?CONFIG=" + zoho.encryption.urlEncode(config.toString())
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Export Data from a View](../../../domains/data-operations/sync-data-export/export-data-view.md) - full endpoint reference.
- [Synchronous Data Export overview](../../../domains/data-operations/sync-data-export/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
