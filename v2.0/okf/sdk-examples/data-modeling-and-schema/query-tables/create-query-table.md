---
type: SDK Example
title: SDK examples - Create Query Table
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/querytables (createQueryTable)."
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
  operation_id: createQueryTable
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/querytables"
  endpoint_doc: "/domains/data-modeling-and-schema/query-tables/create-query-table.md"
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
    resource: "/domains/data-modeling-and-schema/query-tables/create-query-table.md"
    title: Endpoint reference - Create Query Table
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Create Query Table](../../../domains/data-modeling-and-schema/query-tables/create-query-table.md) (`POST /restapi/v2/workspaces/{workspace-id}/querytables`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

Variant 1:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/querytables" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"queryTableName":"Regional_Summary","sqlQuery":"SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 GROUP BY Region"}'
```

Variant 2:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/querytables" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"queryTableName":"Regional_Summary","sqlQuery":"SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 GROUP BY Region","description":"Revenue rolled up by region","folderId":35130000001055731}'
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

        public void CreateQueryTable(IAnalyticsClient ac)
        {
            string sqlQuery = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 GROUP BY Region";
            string queryTableName = "Regional_Summary";
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            var result = workspace.CreateQueryTable(sqlQuery, queryTableName, null);
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
                obj.CreateQueryTable(ac);
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

        public void CreateQueryTable(IAnalyticsClient ac)
        {
            string sqlQuery = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 GROUP BY Region";
            string queryTableName = "Regional_Summary";
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("description", "Revenue rolled up by region");
            config.Add("folderId", 35130000001055731);
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            var result = workspace.CreateQueryTable(sqlQuery, queryTableName, config);
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
                obj.CreateQueryTable(ac);
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

func CreateQueryTable(ac ZAnalytics.Client) {
    sqlQuery := "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 GROUP BY Region"
    queryTableName := "Regional_Summary"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.CreateQueryTable(sqlQuery, queryTableName, nil)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateQueryTable(ac)
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

func CreateQueryTable(ac ZAnalytics.Client) {
    sqlQuery := "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 GROUP BY Region"
    queryTableName := "Regional_Summary"
    config := map[string]interface{}{
        "description": "Revenue rolled up by region",
        "folderId": 35130000001055731,
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.CreateQueryTable(sqlQuery, queryTableName, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateQueryTable(ac)
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
            tObj.createQueryTable(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void createQueryTable(AnalyticsClient ac) throws Exception {
        String sqlQuery = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 GROUP BY Region";
        String queryTableName = "Regional_Summary";
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.createQueryTable(sqlQuery, queryTableName, null);
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
            tObj.createQueryTable(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void createQueryTable(AnalyticsClient ac) throws Exception {
        String sqlQuery = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 GROUP BY Region";
        String queryTableName = "Regional_Summary";
        JSONObject config = new JSONObject();
        config.put("description", "Revenue rolled up by region");
        config.put("folderId", 35130000001055731l);
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.createQueryTable(sqlQuery, queryTableName, config);
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

        function createQueryTable() {
            $sql_query = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 GROUP BY Region";
            $query_table_name = "Regional_Summary";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->createQueryTable($sql_query, $query_table_name);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->createQueryTable();
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

        function createQueryTable() {
            $sql_query = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 GROUP BY Region";
            $query_table_name = "Regional_Summary";
            $config = array(
                "description" => "Revenue rolled up by region",
                "folderId" => 35130000001055731
            );
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->createQueryTable($sql_query, $query_table_name, $config);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->createQueryTable();
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

    def create_query_table(self, ac):
        sql_query = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 GROUP BY Region"
        query_table_name = "Regional_Summary"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_query_table(sql_query, query_table_name)
        print(result)

try:
    obj = sample()
    obj.create_query_table(obj.ac)
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

    def create_query_table(self, ac):
        sql_query = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 GROUP BY Region"
        query_table_name = "Regional_Summary"
        config = {
            "description": "Revenue rolled up by region",
            "folderId": 35130000001055731
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_query_table(sql_query, query_table_name, config)
        print(result)

try:
    obj = sample()
    obj.create_query_table(obj.ac)
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

var sqlQuery = 'SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 GROUP BY Region';
var queryTableName = 'Regional_Summary';

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);

workspace.createQueryTable(sqlQuery, queryTableName).then(function (result) {
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

var sqlQuery = 'SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 GROUP BY Region';
var queryTableName = 'Regional_Summary';
var config = {
    description: 'Revenue rolled up by region',
    folderId: 35130000001055731
};

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);

workspace.createQueryTable(sqlQuery, queryTableName, config).then(function (result) {
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

  def create_query_table
    sql_query = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 GROUP BY Region"
    query_table_name = "Regional_Summary"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.create_query_table(sql_query, query_table_name)
    puts result
  end
end

begin
  obj = Sample.new
  obj.create_query_table
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

  def create_query_table
    sql_query = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 GROUP BY Region"
    query_table_name = "Regional_Summary"
    config = {
        "description" => "Revenue rolled up by region",
        "folderId" => 35130000001055731
    }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.create_query_table(sql_query, query_table_name, config)
    puts result
  end
end

begin
  obj = Sample.new
  obj.create_query_table
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
config.put("queryTableName", "Regional_Summary");
config.put("sqlQuery", "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 GROUP BY Region");
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/querytables"
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
config.put("queryTableName", "Regional_Summary");
config.put("sqlQuery", "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 GROUP BY Region");
config.put("description", "Revenue rolled up by region");
config.put("folderId", 35130000001055731);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/querytables"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Create Query Table](../../../domains/data-modeling-and-schema/query-tables/create-query-table.md) - full endpoint reference.
- [Query Tables overview](../../../domains/data-modeling-and-schema/query-tables/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
