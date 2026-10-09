---
type: SDK Example
title: SDK examples - Create Table
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/tables (createTable)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/tables"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - data-modeling-and-schema
  - table-and-schema
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
  operation_id: createTable
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/tables"
  endpoint_doc: "/domains/data-modeling-and-schema/table-and-schema/create-table.md"
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
    resource: "/domains/data-modeling-and-schema/table-and-schema/create-table.md"
    title: Endpoint reference - Create Table
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Create Table](../../../domains/data-modeling-and-schema/table-and-schema/create-table.md) (`POST /restapi/v2/workspaces/{workspace-id}/tables`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

Variant 1:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/tables" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"tableDesign":{"TABLENAME":"Sales_2026","COLUMNS":[{"COLUMNNAME":"Region","DATATYPE":"PLAIN"},{"COLUMNNAME":"Revenue","DATATYPE":"CURRENCY"}]}}'
```

Variant 2:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/tables" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"tableDesign":{"TABLENAME":"Order_Details","TABLEDESCRIPTION":"Line items for each order","FOLDERNAME":"Sales Analysis","COLUMNS":[{"COLUMNNAME":"Order ID","DATATYPE":"PLAIN","LOOKUPCOLUMN":{"TABLENAME":"Sales_2026","COLUMNNAME":"Region"}},{"COLUMNNAME":"Quantity","DATATYPE":"POSITIVE_NUMBER","DESCRIPTION":"Units ordered","MANDATORY":"true","DEFAULT":"1"},{"COLUMNNAME":"Notes","DATATYPE":"MULTI_LINE","ISHIDE":true},{"COLUMNNAME":"Contact Email","DATATYPE":"EMAIL","PII":true}]}}'
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

        public void CreateTable(IAnalyticsClient ac)
        {
            Dictionary<string, object> tableDesign = new Dictionary<string, object>();
            tableDesign.Add("TABLENAME", "Sales_2026");
            List<object> COLUMNS1 = new List<object>();
            Dictionary<string, object> COLUMNS1Item2 = new Dictionary<string, object>();
            COLUMNS1Item2.Add("COLUMNNAME", "Region");
            COLUMNS1Item2.Add("DATATYPE", "PLAIN");
            COLUMNS1.Add(COLUMNS1Item2);
            Dictionary<string, object> COLUMNS1Item3 = new Dictionary<string, object>();
            COLUMNS1Item3.Add("COLUMNNAME", "Revenue");
            COLUMNS1Item3.Add("DATATYPE", "CURRENCY");
            COLUMNS1.Add(COLUMNS1Item3);
            tableDesign.Add("COLUMNS", COLUMNS1);
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            var result = workspace.CreateTable(tableDesign);
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
                obj.CreateTable(ac);
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

        public void CreateTable(IAnalyticsClient ac)
        {
            Dictionary<string, object> tableDesign = new Dictionary<string, object>();
            tableDesign.Add("TABLENAME", "Order_Details");
            tableDesign.Add("TABLEDESCRIPTION", "Line items for each order");
            tableDesign.Add("FOLDERNAME", "Sales Analysis");
            List<object> COLUMNS1 = new List<object>();
            Dictionary<string, object> COLUMNS1Item2 = new Dictionary<string, object>();
            COLUMNS1Item2.Add("COLUMNNAME", "Order ID");
            COLUMNS1Item2.Add("DATATYPE", "PLAIN");
            Dictionary<string, object> LOOKUPCOLUMN3 = new Dictionary<string, object>();
            LOOKUPCOLUMN3.Add("TABLENAME", "Sales_2026");
            LOOKUPCOLUMN3.Add("COLUMNNAME", "Region");
            COLUMNS1Item2.Add("LOOKUPCOLUMN", LOOKUPCOLUMN3);
            COLUMNS1.Add(COLUMNS1Item2);
            Dictionary<string, object> COLUMNS1Item4 = new Dictionary<string, object>();
            COLUMNS1Item4.Add("COLUMNNAME", "Quantity");
            COLUMNS1Item4.Add("DATATYPE", "POSITIVE_NUMBER");
            COLUMNS1Item4.Add("DESCRIPTION", "Units ordered");
            COLUMNS1Item4.Add("MANDATORY", "true");
            COLUMNS1Item4.Add("DEFAULT", "1");
            COLUMNS1.Add(COLUMNS1Item4);
            Dictionary<string, object> COLUMNS1Item5 = new Dictionary<string, object>();
            COLUMNS1Item5.Add("COLUMNNAME", "Notes");
            COLUMNS1Item5.Add("DATATYPE", "MULTI_LINE");
            COLUMNS1Item5.Add("ISHIDE", true);
            COLUMNS1.Add(COLUMNS1Item5);
            Dictionary<string, object> COLUMNS1Item6 = new Dictionary<string, object>();
            COLUMNS1Item6.Add("COLUMNNAME", "Contact Email");
            COLUMNS1Item6.Add("DATATYPE", "EMAIL");
            COLUMNS1Item6.Add("PII", true);
            COLUMNS1.Add(COLUMNS1Item6);
            tableDesign.Add("COLUMNS", COLUMNS1);
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            var result = workspace.CreateTable(tableDesign);
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
                obj.CreateTable(ac);
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

func CreateTable(ac ZAnalytics.Client) {
    tableDesign := map[string]interface{}{
        "TABLENAME": "Sales_2026",
        "COLUMNS": []interface{}{map[string]interface{}{
            "COLUMNNAME": "Region",
            "DATATYPE": "PLAIN",
        }, map[string]interface{}{
            "COLUMNNAME": "Revenue",
            "DATATYPE": "CURRENCY",
        }},
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.CreateTable(tableDesign)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateTable(ac)
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

func CreateTable(ac ZAnalytics.Client) {
    tableDesign := map[string]interface{}{
        "TABLENAME": "Order_Details",
        "TABLEDESCRIPTION": "Line items for each order",
        "FOLDERNAME": "Sales Analysis",
        "COLUMNS": []interface{}{map[string]interface{}{
            "COLUMNNAME": "Order ID",
            "DATATYPE": "PLAIN",
            "LOOKUPCOLUMN": map[string]interface{}{
                "TABLENAME": "Sales_2026",
                "COLUMNNAME": "Region",
            },
        }, map[string]interface{}{
            "COLUMNNAME": "Quantity",
            "DATATYPE": "POSITIVE_NUMBER",
            "DESCRIPTION": "Units ordered",
            "MANDATORY": "true",
            "DEFAULT": "1",
        }, map[string]interface{}{
            "COLUMNNAME": "Notes",
            "DATATYPE": "MULTI_LINE",
            "ISHIDE": true,
        }, map[string]interface{}{
            "COLUMNNAME": "Contact Email",
            "DATATYPE": "EMAIL",
            "PII": true,
        }},
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.CreateTable(tableDesign)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateTable(ac)
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
            tObj.createTable(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void createTable(AnalyticsClient ac) throws Exception {
        JSONObject tableDesign = new JSONObject();
        tableDesign.put("TABLENAME", "Sales_2026");
        JSONArray COLUMNS1 = new JSONArray();
        JSONObject COLUMNS1Item2 = new JSONObject();
        COLUMNS1Item2.put("COLUMNNAME", "Region");
        COLUMNS1Item2.put("DATATYPE", "PLAIN");
        COLUMNS1.put(COLUMNS1Item2);
        JSONObject COLUMNS1Item3 = new JSONObject();
        COLUMNS1Item3.put("COLUMNNAME", "Revenue");
        COLUMNS1Item3.put("DATATYPE", "CURRENCY");
        COLUMNS1.put(COLUMNS1Item3);
        tableDesign.put("COLUMNS", COLUMNS1);
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.createTable(tableDesign);
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
            tObj.createTable(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void createTable(AnalyticsClient ac) throws Exception {
        JSONObject tableDesign = new JSONObject();
        tableDesign.put("TABLENAME", "Order_Details");
        tableDesign.put("TABLEDESCRIPTION", "Line items for each order");
        tableDesign.put("FOLDERNAME", "Sales Analysis");
        JSONArray COLUMNS1 = new JSONArray();
        JSONObject COLUMNS1Item2 = new JSONObject();
        COLUMNS1Item2.put("COLUMNNAME", "Order ID");
        COLUMNS1Item2.put("DATATYPE", "PLAIN");
        JSONObject LOOKUPCOLUMN3 = new JSONObject();
        LOOKUPCOLUMN3.put("TABLENAME", "Sales_2026");
        LOOKUPCOLUMN3.put("COLUMNNAME", "Region");
        COLUMNS1Item2.put("LOOKUPCOLUMN", LOOKUPCOLUMN3);
        COLUMNS1.put(COLUMNS1Item2);
        JSONObject COLUMNS1Item4 = new JSONObject();
        COLUMNS1Item4.put("COLUMNNAME", "Quantity");
        COLUMNS1Item4.put("DATATYPE", "POSITIVE_NUMBER");
        COLUMNS1Item4.put("DESCRIPTION", "Units ordered");
        COLUMNS1Item4.put("MANDATORY", "true");
        COLUMNS1Item4.put("DEFAULT", "1");
        COLUMNS1.put(COLUMNS1Item4);
        JSONObject COLUMNS1Item5 = new JSONObject();
        COLUMNS1Item5.put("COLUMNNAME", "Notes");
        COLUMNS1Item5.put("DATATYPE", "MULTI_LINE");
        COLUMNS1Item5.put("ISHIDE", true);
        COLUMNS1.put(COLUMNS1Item5);
        JSONObject COLUMNS1Item6 = new JSONObject();
        COLUMNS1Item6.put("COLUMNNAME", "Contact Email");
        COLUMNS1Item6.put("DATATYPE", "EMAIL");
        COLUMNS1Item6.put("PII", true);
        COLUMNS1.put(COLUMNS1Item6);
        tableDesign.put("COLUMNS", COLUMNS1);
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.createTable(tableDesign);
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

        function createTable() {
            $table_design = array(
                "TABLENAME" => "Sales_2026",
                "COLUMNS" => array(array(
                    "COLUMNNAME" => "Region",
                    "DATATYPE" => "PLAIN"
                ), array(
                    "COLUMNNAME" => "Revenue",
                    "DATATYPE" => "CURRENCY"
                ))
            );
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->createTable($table_design);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->createTable();
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

        function createTable() {
            $table_design = array(
                "TABLENAME" => "Order_Details",
                "TABLEDESCRIPTION" => "Line items for each order",
                "FOLDERNAME" => "Sales Analysis",
                "COLUMNS" => array(array(
                    "COLUMNNAME" => "Order ID",
                    "DATATYPE" => "PLAIN",
                    "LOOKUPCOLUMN" => array(
                        "TABLENAME" => "Sales_2026",
                        "COLUMNNAME" => "Region"
                    )
                ), array(
                    "COLUMNNAME" => "Quantity",
                    "DATATYPE" => "POSITIVE_NUMBER",
                    "DESCRIPTION" => "Units ordered",
                    "MANDATORY" => "true",
                    "DEFAULT" => "1"
                ), array(
                    "COLUMNNAME" => "Notes",
                    "DATATYPE" => "MULTI_LINE",
                    "ISHIDE" => true
                ), array(
                    "COLUMNNAME" => "Contact Email",
                    "DATATYPE" => "EMAIL",
                    "PII" => true
                ))
            );
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->createTable($table_design);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->createTable();
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

    def create_table(self, ac):
        table_design = {
            "TABLENAME": "Sales_2026",
            "COLUMNS": [{
                "COLUMNNAME": "Region",
                "DATATYPE": "PLAIN"
            }, {
                "COLUMNNAME": "Revenue",
                "DATATYPE": "CURRENCY"
            }]
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_table(table_design)
        print(result)

try:
    obj = sample()
    obj.create_table(obj.ac)
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

    def create_table(self, ac):
        table_design = {
            "TABLENAME": "Order_Details",
            "TABLEDESCRIPTION": "Line items for each order",
            "FOLDERNAME": "Sales Analysis",
            "COLUMNS": [{
                "COLUMNNAME": "Order ID",
                "DATATYPE": "PLAIN",
                "LOOKUPCOLUMN": {
                    "TABLENAME": "Sales_2026",
                    "COLUMNNAME": "Region"
                }
            }, {
                "COLUMNNAME": "Quantity",
                "DATATYPE": "POSITIVE_NUMBER",
                "DESCRIPTION": "Units ordered",
                "MANDATORY": "true",
                "DEFAULT": "1"
            }, {
                "COLUMNNAME": "Notes",
                "DATATYPE": "MULTI_LINE",
                "ISHIDE": True
            }, {
                "COLUMNNAME": "Contact Email",
                "DATATYPE": "EMAIL",
                "PII": True
            }]
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_table(table_design)
        print(result)

try:
    obj = sample()
    obj.create_table(obj.ac)
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

var tableDesign = {
    TABLENAME: 'Sales_2026',
    COLUMNS: [{
        COLUMNNAME: 'Region',
        DATATYPE: 'PLAIN'
    }, {
        COLUMNNAME: 'Revenue',
        DATATYPE: 'CURRENCY'
    }]
};

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);

workspace.createTable(tableDesign).then(function (result) {
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

var tableDesign = {
    TABLENAME: 'Order_Details',
    TABLEDESCRIPTION: 'Line items for each order',
    FOLDERNAME: 'Sales Analysis',
    COLUMNS: [{
        COLUMNNAME: 'Order ID',
        DATATYPE: 'PLAIN',
        LOOKUPCOLUMN: {
            TABLENAME: 'Sales_2026',
            COLUMNNAME: 'Region'
        }
    }, {
        COLUMNNAME: 'Quantity',
        DATATYPE: 'POSITIVE_NUMBER',
        DESCRIPTION: 'Units ordered',
        MANDATORY: 'true',
        DEFAULT: '1'
    }, {
        COLUMNNAME: 'Notes',
        DATATYPE: 'MULTI_LINE',
        ISHIDE: true
    }, {
        COLUMNNAME: 'Contact Email',
        DATATYPE: 'EMAIL',
        PII: true
    }]
};

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);

workspace.createTable(tableDesign).then(function (result) {
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

  def create_table
    table_design = {
        "TABLENAME" => "Sales_2026",
        "COLUMNS" => [{
            "COLUMNNAME" => "Region",
            "DATATYPE" => "PLAIN"
        }, {
            "COLUMNNAME" => "Revenue",
            "DATATYPE" => "CURRENCY"
        }]
    }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.create_table(table_design)
    puts result
  end
end

begin
  obj = Sample.new
  obj.create_table
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

  def create_table
    table_design = {
        "TABLENAME" => "Order_Details",
        "TABLEDESCRIPTION" => "Line items for each order",
        "FOLDERNAME" => "Sales Analysis",
        "COLUMNS" => [{
            "COLUMNNAME" => "Order ID",
            "DATATYPE" => "PLAIN",
            "LOOKUPCOLUMN" => {
                "TABLENAME" => "Sales_2026",
                "COLUMNNAME" => "Region"
            }
        }, {
            "COLUMNNAME" => "Quantity",
            "DATATYPE" => "POSITIVE_NUMBER",
            "DESCRIPTION" => "Units ordered",
            "MANDATORY" => "true",
            "DEFAULT" => "1"
        }, {
            "COLUMNNAME" => "Notes",
            "DATATYPE" => "MULTI_LINE",
            "ISHIDE" => true
        }, {
            "COLUMNNAME" => "Contact Email",
            "DATATYPE" => "EMAIL",
            "PII" => true
        }]
    }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.create_table(table_design)
    puts result
  end
end

begin
  obj = Sample.new
  obj.create_table
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
config_tableDesign = Map();
config_tableDesign.put("TABLENAME", "Sales_2026");
config_tableDesign_COLUMNS = List();
config_tableDesign_COLUMNS_item1 = Map();
config_tableDesign_COLUMNS_item1.put("COLUMNNAME", "Region");
config_tableDesign_COLUMNS_item1.put("DATATYPE", "PLAIN");
config_tableDesign_COLUMNS.add(config_tableDesign_COLUMNS_item1);
config_tableDesign_COLUMNS_item2 = Map();
config_tableDesign_COLUMNS_item2.put("COLUMNNAME", "Revenue");
config_tableDesign_COLUMNS_item2.put("DATATYPE", "CURRENCY");
config_tableDesign_COLUMNS.add(config_tableDesign_COLUMNS_item2);
config_tableDesign.put("COLUMNS", config_tableDesign_COLUMNS);
config.put("tableDesign", config_tableDesign);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/tables"
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
config_tableDesign = Map();
config_tableDesign.put("TABLENAME", "Order_Details");
config_tableDesign.put("TABLEDESCRIPTION", "Line items for each order");
config_tableDesign.put("FOLDERNAME", "Sales Analysis");
config_tableDesign_COLUMNS = List();
config_tableDesign_COLUMNS_item1 = Map();
config_tableDesign_COLUMNS_item1.put("COLUMNNAME", "Order ID");
config_tableDesign_COLUMNS_item1.put("DATATYPE", "PLAIN");
config_tableDesign_COLUMNS_item1_LOOKUPCOLUMN = Map();
config_tableDesign_COLUMNS_item1_LOOKUPCOLUMN.put("TABLENAME", "Sales_2026");
config_tableDesign_COLUMNS_item1_LOOKUPCOLUMN.put("COLUMNNAME", "Region");
config_tableDesign_COLUMNS_item1.put("LOOKUPCOLUMN", config_tableDesign_COLUMNS_item1_LOOKUPCOLUMN);
config_tableDesign_COLUMNS.add(config_tableDesign_COLUMNS_item1);
config_tableDesign_COLUMNS_item2 = Map();
config_tableDesign_COLUMNS_item2.put("COLUMNNAME", "Quantity");
config_tableDesign_COLUMNS_item2.put("DATATYPE", "POSITIVE_NUMBER");
config_tableDesign_COLUMNS_item2.put("DESCRIPTION", "Units ordered");
config_tableDesign_COLUMNS_item2.put("MANDATORY", "true");
config_tableDesign_COLUMNS_item2.put("DEFAULT", "1");
config_tableDesign_COLUMNS.add(config_tableDesign_COLUMNS_item2);
config_tableDesign_COLUMNS_item3 = Map();
config_tableDesign_COLUMNS_item3.put("COLUMNNAME", "Notes");
config_tableDesign_COLUMNS_item3.put("DATATYPE", "MULTI_LINE");
config_tableDesign_COLUMNS_item3.put("ISHIDE", true);
config_tableDesign_COLUMNS.add(config_tableDesign_COLUMNS_item3);
config_tableDesign_COLUMNS_item4 = Map();
config_tableDesign_COLUMNS_item4.put("COLUMNNAME", "Contact Email");
config_tableDesign_COLUMNS_item4.put("DATATYPE", "EMAIL");
config_tableDesign_COLUMNS_item4.put("PII", true);
config_tableDesign_COLUMNS.add(config_tableDesign_COLUMNS_item4);
config_tableDesign.put("COLUMNS", config_tableDesign_COLUMNS);
config.put("tableDesign", config_tableDesign);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/tables"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Create Table](../../../domains/data-modeling-and-schema/table-and-schema/create-table.md) - full endpoint reference.
- [Table & Schema overview](../../../domains/data-modeling-and-schema/table-and-schema/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
