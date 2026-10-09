---
type: SDK Example
title: SDK examples - Get Custom Formulas
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas (getCustomFormulaList)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - data-modeling-and-schema
  - formula-columns
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
  operation_id: getCustomFormulaList
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas"
  endpoint_doc: "/domains/data-modeling-and-schema/formula-columns/get-custom-formula-list.md"
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
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
  - id: endpoint-doc
    resource: "/domains/data-modeling-and-schema/formula-columns/get-custom-formula-list.md"
    title: Endpoint reference - Get Custom Formulas
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Get Custom Formulas](../../../domains/data-modeling-and-schema/formula-columns/get-custom-formula-list.md) (`GET /restapi/v2/workspaces/{workspace-id}/views/{view-id}/customformulas`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/customformulas" -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
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

        public void GetFormulaColumns(IAnalyticsClient ac)
        {
            long viewId = 35130000001055717;
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            var result = view.GetFormulaColumns();
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
                obj.GetFormulaColumns(ac);
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

func GetFormulaColumns(ac ZAnalytics.Client) {
    viewId := "35130000001055717"
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    result, exception := view.GetFormulaColumns()
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetFormulaColumns(ac)
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
            tObj.getCustomFormulaList(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void getCustomFormulaList(AnalyticsClient ac) throws Exception {
        long viewId = 35130000001055717l;
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONObject result = view.getFormulaColumns();
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

        function getFormulaColumns() {
            $view_id = "35130000001055717";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $view_id);
            $response = $view->getFormulaColumns();
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->getFormulaColumns();
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

class Config:
    CLIENTID = "1000.xxxxxxx"
    CLIENTSECRET = "xxxxxxx"
    REFRESHTOKEN = "1000.xxxxxxx.xxxxxxx"
    ORGID = "55522777"
    WORKSPACEID = "35130000001055707"

class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def get_custom_formula_list(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, "35130000001055717")
        result = view.get_formula_columns()
        print(result)

try:
    obj = sample()
    obj.get_custom_formula_list(obj.ac)
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
var workspaceId = '35130000001055707';

var ac = new analyticsClient(clientId, clientSecret, refreshToken);

var viewId = '35130000001055717';

var view = ac.getViewInstance(orgId, workspaceId, viewId);

view.getFormulaColumns().then(function (result) {
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

  def get_custom_formula_list
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, "35130000001055717")
    result = view.get_formula_columns()
    puts result
  end
end

begin
  obj = Sample.new
  obj.get_custom_formula_list
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
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/35130000001055717/customformulas"
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Custom Formulas](../../../domains/data-modeling-and-schema/formula-columns/get-custom-formula-list.md) - full endpoint reference.
- [Custom Formula Columns overview](../../../domains/data-modeling-and-schema/formula-columns/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
