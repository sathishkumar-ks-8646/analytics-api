---
type: SDK Example
title: SDK examples - Edit Query Table
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id} (editQueryTable)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}"
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
  operation_id: editQueryTable
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}"
  endpoint_doc: "/domains/data-modeling-and-schema/query-tables/edit-query-table.md"
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
    resource: "/domains/data-modeling-and-schema/query-tables/edit-query-table.md"
    title: Endpoint reference - Edit Query Table
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Edit Query Table](../../../domains/data-modeling-and-schema/query-tables/edit-query-table.md) (`PUT /restapi/v2/workspaces/{workspace-id}/querytables/{querytable-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

Variant 1:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/querytables/35130000001056001" -X 'PUT' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"sqlQuery":"SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 WHERE Year = 2026 GROUP BY Region"}'
```

Variant 2:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/querytables/35130000001056001" -X 'PUT' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"sqlQuery":"SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 WHERE Year = 2026 GROUP BY Region","folderId":35130000001055731}'
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

        public void EditQueryTable(IAnalyticsClient ac)
        {
            long viewId = 35130000001056001;
            string sqlQuery = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 WHERE Year = 2026 GROUP BY Region";
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.EditQueryTable(viewId, sqlQuery, null);
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
                obj.EditQueryTable(ac);
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

        public void EditQueryTable(IAnalyticsClient ac)
        {
            long viewId = 35130000001056001;
            string sqlQuery = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 WHERE Year = 2026 GROUP BY Region";
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("folderId", 35130000001055731);
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.EditQueryTable(viewId, sqlQuery, config);
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
                obj.EditQueryTable(ac);
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

func EditQueryTable(ac ZAnalytics.Client) {
    viewId := "35130000001056001"
    sqlQuery := "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 WHERE Year = 2026 GROUP BY Region"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    exception := workspace.EditQueryTable(viewId, sqlQuery, nil)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    EditQueryTable(ac)
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

func EditQueryTable(ac ZAnalytics.Client) {
    viewId := "35130000001056001"
    sqlQuery := "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 WHERE Year = 2026 GROUP BY Region"
    config := map[string]interface{}{
        "folderId": 35130000001055731,
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    exception := workspace.EditQueryTable(viewId, sqlQuery, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    EditQueryTable(ac)
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
            tObj.editQueryTable(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void editQueryTable(AnalyticsClient ac) throws Exception {
        long viewId = 35130000001056001l;
        String sqlQuery = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 WHERE Year = 2026 GROUP BY Region";
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.updateQueryTable(viewId, sqlQuery, null);
        System.out.println("success");
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
            tObj.editQueryTable(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void editQueryTable(AnalyticsClient ac) throws Exception {
        long viewId = 35130000001056001l;
        String sqlQuery = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 WHERE Year = 2026 GROUP BY Region";
        JSONObject config = new JSONObject();
        config.put("folderId", 35130000001055731l);
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.updateQueryTable(viewId, sqlQuery, config);
        System.out.println("success");
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

        function editQueryTable() {
            $view_id = "35130000001056001";
            $sql_query = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 WHERE Year = 2026 GROUP BY Region";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->editQueryTable($view_id, $sql_query);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->editQueryTable();
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

        function editQueryTable() {
            $view_id = "35130000001056001";
            $sql_query = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 WHERE Year = 2026 GROUP BY Region";
            $config = array(
                "folderId" => 35130000001055731
            );
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->editQueryTable($view_id, $sql_query, $config);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->editQueryTable();
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

    def edit_query_table(self, ac):
        view_id = "35130000001056001"
        sql_query = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 WHERE Year = 2026 GROUP BY Region"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.edit_query_table(view_id, sql_query)
        print("success")

try:
    obj = sample()
    obj.edit_query_table(obj.ac)
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

    def edit_query_table(self, ac):
        view_id = "35130000001056001"
        sql_query = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 WHERE Year = 2026 GROUP BY Region"
        config = {
            "folderId": 35130000001055731
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.edit_query_table(view_id, sql_query, config)
        print("success")

try:
    obj = sample()
    obj.edit_query_table(obj.ac)
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

var viewId = '35130000001056001';
var sqlQuery = 'SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 WHERE Year = 2026 GROUP BY Region';

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);

workspace.editQueryTable(viewId, sqlQuery).then(function () {
    console.log('success');
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

var viewId = '35130000001056001';
var sqlQuery = 'SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 WHERE Year = 2026 GROUP BY Region';
var config = {
    folderId: 35130000001055731
};

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);

workspace.editQueryTable(viewId, sqlQuery, config).then(function () {
    console.log('success');
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

  def edit_query_table
    view_id = "35130000001056001"
    sql_query = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 WHERE Year = 2026 GROUP BY Region"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.edit_query_table(view_id, sql_query)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.edit_query_table
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

  def edit_query_table
    view_id = "35130000001056001"
    sql_query = "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 WHERE Year = 2026 GROUP BY Region"
    config = {
        "folderId" => 35130000001055731
    }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.edit_query_table(view_id, sql_query, config)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.edit_query_table
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
config.put("sqlQuery", "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 WHERE Year = 2026 GROUP BY Region");
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/querytables/35130000001056001"
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

Variant 2:

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("sqlQuery", "SELECT Region, SUM(Revenue) AS TotalRevenue FROM Sales_2026 WHERE Year = 2026 GROUP BY Region");
config.put("folderId", 35130000001055731);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/querytables/35130000001056001"
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Edit Query Table](../../../domains/data-modeling-and-schema/query-tables/edit-query-table.md) - full endpoint reference.
- [Query Tables overview](../../../domains/data-modeling-and-schema/query-tables/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
