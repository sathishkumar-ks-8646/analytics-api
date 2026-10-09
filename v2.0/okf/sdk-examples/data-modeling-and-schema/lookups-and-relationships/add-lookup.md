---
type: SDK Example
title: SDK examples - Add Lookup
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup (addLookup)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - data-modeling-and-schema
  - lookups-and-relationships
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
  operation_id: addLookup
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup"
  endpoint_doc: "/domains/data-modeling-and-schema/lookups-and-relationships/add-lookup.md"
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
    resource: "/domains/data-modeling-and-schema/lookups-and-relationships/add-lookup.md"
    title: Endpoint reference - Add Lookup
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

Code samples for [Add Lookup](../../../domains/data-modeling-and-schema/lookups-and-relationships/add-lookup.md) (`POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}/lookup`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/columns/35130000001055811/lookup" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"referenceViewId":35130000001055719,"referenceColumnId":35130000001055821}'
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

        public void AddLookup(IAnalyticsClient ac)
        {
            long viewId = 35130000001055717;
            long columnId = 35130000001055811;
            long refViewId = 35130000001055719;
            long refColumnId = 35130000001055821;
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("referenceViewId", 35130000001055719);
            config.Add("referenceColumnId", 35130000001055821);
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.AddLookup(columnId, refViewId, refColumnId, config);
            Console.WriteLine("success");
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
                obj.AddLookup(ac);
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

func AddLookup(ac ZAnalytics.Client) {
    viewId := "35130000001055717"
    columnId := "35130000001055811"
    refViewId := "35130000001055719"
    refColumnId := "35130000001055821"
    config := map[string]interface{}{
        "referenceViewId": 35130000001055719,
        "referenceColumnId": 35130000001055821,
    }
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    exception := view.AddLookup(columnId, refViewId, refColumnId, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    AddLookup(ac)
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
            tObj.addLookup(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void addLookup(AnalyticsClient ac) throws Exception {
        long viewId = 35130000001055717l;
        long columnId = 35130000001055811l;
        long refViewId = 35130000001055719l;
        long refColumnId = 35130000001055821l;
        JSONObject config = new JSONObject();
        config.put("referenceViewId", 35130000001055719l);
        config.put("referenceColumnId", 35130000001055821l);
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.addLookup(columnId, refViewId, refColumnId, config);
        System.out.println("success");
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

        function addLookup() {
            $view_id = "35130000001055717";
            $column_id = "35130000001055811";
            $ref_view_id = "35130000001055719";
            $ref_column_id = "35130000001055821";
            $config = array(
                "referenceViewId" => 35130000001055719,
                "referenceColumnId" => 35130000001055821
            );
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $view_id);
            $view->addLookup($column_id, $ref_view_id, $ref_column_id, $config);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->addLookup();
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

    def add_lookup(self, ac):
        column_id = "35130000001055811"
        ref_view_id = "35130000001055719"
        ref_column_id = "35130000001055821"
        config = {
            "referenceViewId": 35130000001055719,
            "referenceColumnId": 35130000001055821
        }
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, "35130000001055717")
        view.add_lookup(column_id, ref_view_id, ref_column_id, config)
        print("success")

try:
    obj = sample()
    obj.add_lookup(obj.ac)
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
var columnId = '35130000001055811';
var refViewId = '35130000001055719';
var refColumnId = '35130000001055821';
var config = {
    referenceViewId: 35130000001055719,
    referenceColumnId: 35130000001055821
};

var view = ac.getViewInstance(orgId, workspaceId, viewId);

view.addLookup(columnId, refViewId, refColumnId, config).then(function () {
    console.log('success');
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

  def add_lookup
    column_id = "35130000001055811"
    ref_view_id = "35130000001055719"
    ref_column_id = "35130000001055821"
    config = {
        "referenceViewId" => 35130000001055719,
        "referenceColumnId" => 35130000001055821
    }
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, "35130000001055717")
    view.add_lookup(column_id, ref_view_id, ref_column_id, config)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.add_lookup
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
config = Map();
config.put("referenceViewId", 35130000001055719);
config.put("referenceColumnId", 35130000001055821);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/35130000001055717/columns/35130000001055811/lookup"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Add Lookup](../../../domains/data-modeling-and-schema/lookups-and-relationships/add-lookup.md) - full endpoint reference.
- [Lookups & Relationships overview](../../../domains/data-modeling-and-schema/lookups-and-relationships/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
