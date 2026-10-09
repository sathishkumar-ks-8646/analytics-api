---
type: SDK Example
title: SDK examples - Get Aggregate Formula Dependents
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/dependents (getAggregateFormulaDependents)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/dependents"
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
  operation_id: getAggregateFormulaDependents
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/dependents"
  endpoint_doc: "/domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-dependents.md"
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
    last_modified: 2026-10-09T14:14:03Z
  - id: endpoint-doc
    resource: "/domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-dependents.md"
    title: Endpoint reference - Get Aggregate Formula Dependents
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

Code samples for [Get Aggregate Formula Dependents](../../../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-dependents.md) (`GET /restapi/v2/workspaces/{workspace-id}/aggregateformulas/{formula-id}/dependents`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/aggregateformulas/35130000001056101/dependents" -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
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

        public void GetAggregateFormulaDependents(IAnalyticsClient ac)
        {
            long formulaId = 35130000001056101;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            var result = workspace.GetAggregateFormulaDependents(formulaId);
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
                obj.GetAggregateFormulaDependents(ac);
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

func GetAggregateFormulaDependents(ac ZAnalytics.Client) {
    formulaId := "35130000001056101"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.GetAggregateFormulaDependents(formulaId)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetAggregateFormulaDependents(ac)
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
            tObj.getAggregateFormulaDependents(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void getAggregateFormulaDependents(AnalyticsClient ac) throws Exception {
        long formulaId = 35130000001056101l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getAggregateFormulaDependents(formulaId);
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

        function getAggregateFormulaDependents() {
            $formula_id = "35130000001056101";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getAggregateFormulaDependents($formula_id);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->getAggregateFormulaDependents();
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

    def get_aggregate_formula_dependents(self, ac):
        formula_id = "35130000001056101"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_aggregate_formula_dependents(formula_id)
        print(result)

try:
    obj = sample()
    obj.get_aggregate_formula_dependents(obj.ac)
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

var formulaId = '35130000001056101';

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);

workspace.getAggregateFormulaDependents(formulaId).then(function (result) {
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

  def get_aggregate_formula_dependents
    formula_id = "35130000001056101"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_aggregate_formula_dependents(formula_id)
    puts result
  end
end

begin
  obj = Sample.new
  obj.get_aggregate_formula_dependents
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
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/aggregateformulas/35130000001056101/dependents"
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Aggregate Formula Dependents](../../../domains/data-modeling-and-schema/aggregate-formulas/get-aggregate-formula-dependents.md) - full endpoint reference.
- [Aggregate Formulas (Unified Metrics) overview](../../../domains/data-modeling-and-schema/aggregate-formulas/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
