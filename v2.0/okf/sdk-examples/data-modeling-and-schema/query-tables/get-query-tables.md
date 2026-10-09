---
type: SDK Example
title: SDK examples - Get Query Tables
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/querytables (getQueryTables)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/querytables"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - data-modeling-and-schema
  - query-tables
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
  operation_id: getQueryTables
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/querytables"
  endpoint_doc: "/domains/data-modeling-and-schema/query-tables/get-query-tables.md"
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
    resource: "/domains/data-modeling-and-schema/query-tables/get-query-tables.md"
    title: Endpoint reference - Get Query Tables
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Get Query Tables](../../../domains/data-modeling-and-schema/query-tables/get-query-tables.md) (`GET /restapi/v2/workspaces/{workspace-id}/querytables`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

Variant 1:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/querytables" -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
```

Variant 2:

```bash
curl -G "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/querytables" -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"keyword":"Sales","sortedColumn":2,"sortedOrder":1}'
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

        public void GetQueryTables(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            var result = workspace.GetQueryTables(null);
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
                obj.GetQueryTables(ac);
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

        public void GetQueryTables(IAnalyticsClient ac)
        {
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("keyword", "Sales");
            config.Add("sortedColumn", 2);
            config.Add("sortedOrder", 1);
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            var result = workspace.GetQueryTables(config);
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
                obj.GetQueryTables(ac);
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

func GetQueryTables(ac ZAnalytics.Client) {
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.GetQueryTables(nil)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetQueryTables(ac)
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

func GetQueryTables(ac ZAnalytics.Client) {
    config := map[string]interface{}{
        "keyword": "Sales",
        "sortedColumn": 2,
        "sortedOrder": 1,
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.GetQueryTables(config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetQueryTables(ac)
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
            tObj.getQueryTables(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void getQueryTables(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getQueryTables(null);
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
            tObj.getQueryTables(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void getQueryTables(AnalyticsClient ac) throws Exception {
        JSONObject config = new JSONObject();
        config.put("keyword", "Sales");
        config.put("sortedColumn", 2);
        config.put("sortedOrder", 1);
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getQueryTables(config);
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

        function getQueryTables() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getQueryTables();
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->getQueryTables();
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

        function getQueryTables() {
            $config = array(
                "keyword" => "Sales",
                "sortedColumn" => 2,
                "sortedOrder" => 1
            );
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getQueryTables($config);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->getQueryTables();
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

    def get_query_tables(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_query_tables()
        print(result)

try:
    obj = sample()
    obj.get_query_tables(obj.ac)
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

    def get_query_tables(self, ac):
        config = {
            "keyword": "Sales",
            "sortedColumn": 2,
            "sortedOrder": 1
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_query_tables(config)
        print(result)

try:
    obj = sample()
    obj.get_query_tables(obj.ac)
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

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);

workspace.getQueryTables().then(function (result) {
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

var config = {
    keyword: 'Sales',
    sortedColumn: 2,
    sortedOrder: 1
};

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);

workspace.getQueryTables(config).then(function (result) {
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

  def get_query_tables
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_query_tables()
    puts result
  end
end

begin
  obj = Sample.new
  obj.get_query_tables
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

  def get_query_tables
    config = {
        "keyword" => "Sales",
        "sortedColumn" => 2,
        "sortedOrder" => 1
    }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_query_tables(config)
    puts result
  end
end

begin
  obj = Sample.new
  obj.get_query_tables
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
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/querytables"
  type :GET
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
config.put("keyword", "Sales");
config.put("sortedColumn", 2);
config.put("sortedOrder", 1);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/querytables" + "?" + parameters
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Query Tables](../../../domains/data-modeling-and-schema/query-tables/get-query-tables.md) - full endpoint reference.
- [Query Tables overview](../../../domains/data-modeling-and-schema/query-tables/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
