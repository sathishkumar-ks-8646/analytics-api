---
type: SDK Example
title: SDK examples - Update Row
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows (updateRows)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - data-operations
  - row-operations
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
  operation_id: updateRows
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows"
  endpoint_doc: "/domains/data-operations/row-operations/update-rows.md"
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
    resource: "/domains/data-operations/row-operations/update-rows.md"
    title: Endpoint reference - Update Row
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Update Row](../../../domains/data-operations/row-operations/update-rows.md) (`PUT /restapi/v2/workspaces/{workspace-id}/views/{view-id}/rows`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/rows" -X 'PUT' -H 'ZANALYTICS-ORGID: 55522777' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode "CONFIG={\"columns\":{\"Revenue\":\"1500\"},\"criteria\":\"\\\"SalesTable\\\".\\\"Region\\\"='East'\",\"addIfNotExist\":false}"
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

        public void UpdateRow(IAnalyticsClient ac)
        {
            Dictionary<string, string> columnValues = new Dictionary<string, string>();
            columnValues.Add("Revenue", "1500");
            string criteria = "\"SalesTable\".\"Region\"='East'";
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("addIfNotExist", false);
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            JsonElement result = view.UpdateRow(columnValues, criteria, config);
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
                obj.UpdateRow(ac);
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

func UpdateRow(ac ZAnalytics.Client) {
    columnvalues := map[string]interface{}{}
    columnvalues["Revenue"] = "1500"
    criteria := `"SalesTable"."Region"='East'`
    config := map[string]interface{}{}
    config["addIfNotExist"] = false
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    result, err := view.UpdateRow(columnvalues, criteria, config)
    if err != nil {
        fmt.Println("Error - " + err.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    UpdateRow(ac)
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
            tObj.updateRow(ac);
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

    public void updateRow(AnalyticsClient ac) throws Exception {
        JSONObject columnValues = new JSONObject();
        columnValues.put("Revenue", "1500");
        String criteria = "\"SalesTable\".\"Region\"='East'";
        JSONObject config = new JSONObject();
        config.put("addIfNotExist", false);
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONObject result = view.updateRow(columnValues, criteria, config);
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

        function updateRow() {
            $column_values = array();
            $column_values["Revenue"] = "1500";
            $criteria = "\"SalesTable\".\"Region\"='East'";
            $config = array();
            $config["addIfNotExist"] = false;
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
            $response = $view->updateRow($column_values, $criteria, $config);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->updateRow();
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

    def update_row(self, ac):
        column_values = {}
        column_values["Revenue"] = "1500"
        criteria = "\"SalesTable\".\"Region\"='East'"
        config = {}
        config["addIfNotExist"] = False
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.update_row(column_values, criteria, config)
        print(result)

try:
    obj = sample()
    obj.update_row(obj.ac)

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

var columnValues = { "Revenue": "1500" };
var criteria = '"SalesTable"."Region"=\'East\'';
var config = { "addIfNotExist": false };
var view = ac.getViewInstance(orgId, workspaceId, viewId);
view.updateRow(columnValues, criteria, config).then((response) => {
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

  def update_row
    column_values = { "Revenue" => "1500" }
    criteria = "\"SalesTable\".\"Region\"='East'"
    config = { "addIfNotExist" => false }
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    result = view.update_row(column_values, criteria, config)
    puts result
  end
end

begin
  obj = Sample.new
  obj.update_row
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
columns = Map();
columns.put("Revenue", "1500");
config.put("columns", columns);
config.put("criteria", "\"SalesTable\".\"Region\"='East'");
config.put("addIfNotExist", false);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/" + viewId + "/rows"
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Update Row](../../../domains/data-operations/row-operations/update-rows.md) - full endpoint reference.
- [Row Operations overview](../../../domains/data-operations/row-operations/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
