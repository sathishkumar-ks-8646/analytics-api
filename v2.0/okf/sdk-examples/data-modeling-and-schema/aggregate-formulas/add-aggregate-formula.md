---
type: SDK Example
title: SDK examples - Add Aggregate Formula
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas (addAggregateFormula)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - data-modeling-and-schema
  - aggregate-formulas
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
  operation_id: addAggregateFormula
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas"
  endpoint_doc: "/domains/data-modeling-and-schema/aggregate-formulas/add-aggregate-formula.md"
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
    last_modified: 2026-10-09T08:29:02Z
  - id: endpoint-doc
    resource: "/domains/data-modeling-and-schema/aggregate-formulas/add-aggregate-formula.md"
    title: Endpoint reference - Add Aggregate Formula
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

Code samples for [Add Aggregate Formula](../../../domains/data-modeling-and-schema/aggregate-formulas/add-aggregate-formula.md) (`POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/aggregateformulas`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

Variant 1:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/aggregateformulas" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"formulaName":"TotalRevenue","expression":"sum(\"Sales_2026\".\"Revenue\")"}'
```

Variant 2:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/aggregateformulas" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"formulaName":"TotalRevenue","expression":"sum(\"Sales_2026\".\"Revenue\")","description":"Total revenue across all regions","synonyms":["total sales","revenue total"],"columnPriority":2}'
```

## C#

Variant 1:

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

        public void AddAggregateFormula(IAnalyticsClient ac)
        {
            long viewId = 35130000001055717;
            string formulaName = "TotalRevenue";
            string expression = "sum(\"Sales_2026\".\"Revenue\")";
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            var result = view.AddAggregateFormula(formulaName, expression, null);
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
                obj.AddAggregateFormula(ac);
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

Variant 2:

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

        public void AddAggregateFormula(IAnalyticsClient ac)
        {
            long viewId = 35130000001055717;
            string formulaName = "TotalRevenue";
            string expression = "sum(\"Sales_2026\".\"Revenue\")";
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("description", "Total revenue across all regions");
            List<object> synonyms1 = new List<object>();
            synonyms1.Add("total sales");
            synonyms1.Add("revenue total");
            config.Add("synonyms", synonyms1);
            config.Add("columnPriority", 2);
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            var result = view.AddAggregateFormula(formulaName, expression, config);
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
                obj.AddAggregateFormula(ac);
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

Variant 1:

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

func AddAggregateFormula(ac ZAnalytics.Client) {
    viewId := "35130000001055717"
    formulaName := "TotalRevenue"
    expression := "sum(\"Sales_2026\".\"Revenue\")"
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    result, exception := view.AddAggregateFormula(formulaName, expression, nil)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    AddAggregateFormula(ac)
}
```

Variant 2:

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

func AddAggregateFormula(ac ZAnalytics.Client) {
    viewId := "35130000001055717"
    formulaName := "TotalRevenue"
    expression := "sum(\"Sales_2026\".\"Revenue\")"
    config := map[string]interface{}{
        "description": "Total revenue across all regions",
        "synonyms": []interface{}{"total sales", "revenue total"},
        "columnPriority": 2,
    }
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    result, exception := view.AddAggregateFormula(formulaName, expression, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    AddAggregateFormula(ac)
}
```

## Java

Variant 1:

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
            tObj.addAggregateFormula(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void addAggregateFormula(AnalyticsClient ac) throws Exception {
        long viewId = 35130000001055717l;
        String formulaName = "TotalRevenue";
        String expression = "sum(\"Sales_2026\".\"Revenue\")";
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONObject result = view.addAggregateFormula(formulaName, expression, null);
        System.out.println(result);
    }
}
```

Variant 2:

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
            tObj.addAggregateFormula(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void addAggregateFormula(AnalyticsClient ac) throws Exception {
        long viewId = 35130000001055717l;
        String formulaName = "TotalRevenue";
        String expression = "sum(\"Sales_2026\".\"Revenue\")";
        JSONObject config = new JSONObject();
        config.put("description", "Total revenue across all regions");
        JSONArray synonyms1 = new JSONArray();
        synonyms1.put("total sales");
        synonyms1.put("revenue total");
        config.put("synonyms", synonyms1);
        config.put("columnPriority", 2);
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONObject result = view.addAggregateFormula(formulaName, expression, config);
        System.out.println(result);
    }
}
```

## PHP

Variant 1:

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

        function addAggregateFormula() {
            $view_id = "35130000001055717";
            $formula_name = "TotalRevenue";
            $expression = "sum(\"Sales_2026\".\"Revenue\")";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $view_id);
            $response = $view->addAggregateFormula($formula_name, $expression);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->addAggregateFormula();
    }
    catch(ServerException $se) {
        echo "Server exception : " . $se->getErrorMessage() . "\n";
    }
    catch(Exception $e) {
        echo "Exception : " . $e->getMessage() . "\n";
    }
?>
```

Variant 2:

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

        function addAggregateFormula() {
            $view_id = "35130000001055717";
            $formula_name = "TotalRevenue";
            $expression = "sum(\"Sales_2026\".\"Revenue\")";
            $config = array(
                "description" => "Total revenue across all regions",
                "synonyms" => array("total sales", "revenue total"),
                "columnPriority" => 2
            );
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $view_id);
            $response = $view->addAggregateFormula($formula_name, $expression, $config);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->addAggregateFormula();
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

Variant 1:

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

    def add_aggregate_formula(self, ac):
        formula_name = "TotalRevenue"
        expression = "sum(\"Sales_2026\".\"Revenue\")"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, "35130000001055717")
        result = view.add_aggregate_formula(formula_name, expression)
        print(result)

try:
    obj = sample()
    obj.add_aggregate_formula(obj.ac)
except Exception as e:
    print(str(e))
```

Variant 2:

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

    def add_aggregate_formula(self, ac):
        formula_name = "TotalRevenue"
        expression = "sum(\"Sales_2026\".\"Revenue\")"
        config = {
            "description": "Total revenue across all regions",
            "synonyms": ["total sales", "revenue total"],
            "columnPriority": 2
        }
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, "35130000001055717")
        result = view.add_aggregate_formula(formula_name, expression, config)
        print(result)

try:
    obj = sample()
    obj.add_aggregate_formula(obj.ac)
except Exception as e:
    print(str(e))
```

## Node.js

Variant 1:

```javascript
var analyticsClient = require('./AnalyticsClient');

var clientId = '1000.xxxxxxx';
var clientSecret = 'xxxxxxx';
var refreshToken = '1000.xxxxxxx.xxxxxxx';
var orgId = '55522777';
var workspaceId = '35130000001055707';

var ac = new analyticsClient(clientId, clientSecret, refreshToken);

var viewId = '35130000001055717';
var formulaName = 'TotalRevenue';
var expression = 'sum("Sales_2026"."Revenue")';

var view = ac.getViewInstance(orgId, workspaceId, viewId);

view.addAggregateFormula(formulaName, expression).then(function (result) {
    console.log(result);
}).catch(function (err) {
    console.log(err);
});
```

Variant 2:

```javascript
var analyticsClient = require('./AnalyticsClient');

var clientId = '1000.xxxxxxx';
var clientSecret = 'xxxxxxx';
var refreshToken = '1000.xxxxxxx.xxxxxxx';
var orgId = '55522777';
var workspaceId = '35130000001055707';

var ac = new analyticsClient(clientId, clientSecret, refreshToken);

var viewId = '35130000001055717';
var formulaName = 'TotalRevenue';
var expression = 'sum("Sales_2026"."Revenue")';
var config = {
    description: 'Total revenue across all regions',
    synonyms: ['total sales', 'revenue total'],
    columnPriority: 2
};

var view = ac.getViewInstance(orgId, workspaceId, viewId);

view.addAggregateFormula(formulaName, expression, config).then(function (result) {
    console.log(result);
}).catch(function (err) {
    console.log(err);
});
```

## Ruby

Variant 1:

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

  def add_aggregate_formula
    formula_name = "TotalRevenue"
    expression = "sum(\"Sales_2026\".\"Revenue\")"
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, "35130000001055717")
    result = view.add_aggregate_formula(formula_name, expression)
    puts result
  end
end

begin
  obj = Sample.new
  obj.add_aggregate_formula
rescue ServerError => e
  puts "Server Error: #{e.response_content}"
rescue StandardError => e
  puts e.message
  puts e.backtrace.join("\n")
end
```

Variant 2:

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

  def add_aggregate_formula
    formula_name = "TotalRevenue"
    expression = "sum(\"Sales_2026\".\"Revenue\")"
    config = {
        "description" => "Total revenue across all regions",
        "synonyms" => ["total sales", "revenue total"],
        "columnPriority" => 2
    }
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, "35130000001055717")
    result = view.add_aggregate_formula(formula_name, expression, config)
    puts result
  end
end

begin
  obj = Sample.new
  obj.add_aggregate_formula
rescue ServerError => e
  puts "Server Error: #{e.response_content}"
rescue StandardError => e
  puts e.message
  puts e.backtrace.join("\n")
end
```

## Deluge (Zoho scripting)

Variant 1:

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("formulaName", "TotalRevenue");
config.put("expression", "sum(\"Sales_2026\".\"Revenue\")");
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/35130000001055717/aggregateformulas"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

Variant 2:

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("formulaName", "TotalRevenue");
config.put("expression", "sum(\"Sales_2026\".\"Revenue\")");
config.put("description", "Total revenue across all regions");
config_synonyms = List();
config_synonyms.add("total sales");
config_synonyms.add("revenue total");
config.put("synonyms", config_synonyms);
config.put("columnPriority", 2);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/35130000001055717/aggregateformulas"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Add Aggregate Formula](../../../domains/data-modeling-and-schema/aggregate-formulas/add-aggregate-formula.md) - full endpoint reference.
- [Aggregate Formulas (Unified Metrics) overview](../../../domains/data-modeling-and-schema/aggregate-formulas/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
