---
type: SDK Example
title: SDK examples - Add Column
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns (addColumn)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - data-modeling-and-schema
  - columns
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
  operation_id: addColumn
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns"
  endpoint_doc: "/domains/data-modeling-and-schema/columns/add-column.md"
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
    resource: "/domains/data-modeling-and-schema/columns/add-column.md"
    title: Endpoint reference - Add Column
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Add Column](../../../domains/data-modeling-and-schema/columns/add-column.md) (`POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

Variant 1:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/columns" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"columnName":"Country","dataType":"PLAIN"}'
```

Variant 2:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/columns" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"columns":[{"columnName":"Discount","dataType":"PERCENT"},{"columnName":"Delivery Date","dataType":"DATE_AS_DATE"},{"columnName":"Status","dataType":"PLAIN","isMandatory":true,"default":"Pending"}]}'
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

        public void AddColumn(IAnalyticsClient ac)
        {
            long viewId = 35130000001055717;
            string columnName = "Country";
            string dataType = "PLAIN";
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            var result = view.AddColumn(columnName, dataType, null);
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
                obj.AddColumn(ac);
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

        public void AddColumn(IAnalyticsClient ac)
        {
            long viewId = 35130000001055717;
            string columnName = "Country";
            string dataType = "PLAIN";
            Dictionary<string, object> config = new Dictionary<string, object>();
            List<object> columns1 = new List<object>();
            Dictionary<string, object> columns1Item2 = new Dictionary<string, object>();
            columns1Item2.Add("columnName", "Discount");
            columns1Item2.Add("dataType", "PERCENT");
            columns1.Add(columns1Item2);
            Dictionary<string, object> columns1Item3 = new Dictionary<string, object>();
            columns1Item3.Add("columnName", "Delivery Date");
            columns1Item3.Add("dataType", "DATE_AS_DATE");
            columns1.Add(columns1Item3);
            Dictionary<string, object> columns1Item4 = new Dictionary<string, object>();
            columns1Item4.Add("columnName", "Status");
            columns1Item4.Add("dataType", "PLAIN");
            columns1Item4.Add("isMandatory", true);
            columns1Item4.Add("default", "Pending");
            columns1.Add(columns1Item4);
            config.Add("columns", columns1);
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            var result = view.AddColumn(columnName, dataType, config);
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
                obj.AddColumn(ac);
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

func AddColumn(ac ZAnalytics.Client) {
    viewId := "35130000001055717"
    columnName := "Country"
    dataType := "PLAIN"
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    result, exception := view.AddColumn(columnName, dataType, nil)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    AddColumn(ac)
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

func AddColumn(ac ZAnalytics.Client) {
    viewId := "35130000001055717"
    columnName := "Country"
    dataType := "PLAIN"
    config := map[string]interface{}{
        "columns": []interface{}{map[string]interface{}{
            "columnName": "Discount",
            "dataType": "PERCENT",
        }, map[string]interface{}{
            "columnName": "Delivery Date",
            "dataType": "DATE_AS_DATE",
        }, map[string]interface{}{
            "columnName": "Status",
            "dataType": "PLAIN",
            "isMandatory": true,
            "default": "Pending",
        }},
    }
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    result, exception := view.AddColumn(columnName, dataType, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    AddColumn(ac)
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
            tObj.addColumn(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void addColumn(AnalyticsClient ac) throws Exception {
        long viewId = 35130000001055717l;
        String columnName = "Country";
        String dataType = "PLAIN";
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONObject result = view.addColumn(columnName, dataType, null);
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
            tObj.addColumn(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void addColumn(AnalyticsClient ac) throws Exception {
        long viewId = 35130000001055717l;
        String columnName = "Country";
        String dataType = "PLAIN";
        JSONObject config = new JSONObject();
        JSONArray columns1 = new JSONArray();
        JSONObject columns1Item2 = new JSONObject();
        columns1Item2.put("columnName", "Discount");
        columns1Item2.put("dataType", "PERCENT");
        columns1.put(columns1Item2);
        JSONObject columns1Item3 = new JSONObject();
        columns1Item3.put("columnName", "Delivery Date");
        columns1Item3.put("dataType", "DATE_AS_DATE");
        columns1.put(columns1Item3);
        JSONObject columns1Item4 = new JSONObject();
        columns1Item4.put("columnName", "Status");
        columns1Item4.put("dataType", "PLAIN");
        columns1Item4.put("isMandatory", true);
        columns1Item4.put("default", "Pending");
        columns1.put(columns1Item4);
        config.put("columns", columns1);
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONObject result = view.addColumn(columnName, dataType, config);
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

        function addColumn() {
            $view_id = "35130000001055717";
            $column_name = "Country";
            $data_type = "PLAIN";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $view_id);
            $response = $view->addColumn($column_name, $data_type);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->addColumn();
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

        function addColumn() {
            $view_id = "35130000001055717";
            $column_name = "Country";
            $data_type = "PLAIN";
            $config = array(
                "columns" => array(array(
                    "columnName" => "Discount",
                    "dataType" => "PERCENT"
                ), array(
                    "columnName" => "Delivery Date",
                    "dataType" => "DATE_AS_DATE"
                ), array(
                    "columnName" => "Status",
                    "dataType" => "PLAIN",
                    "isMandatory" => true,
                    "default" => "Pending"
                ))
            );
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $view_id);
            $response = $view->addColumn($column_name, $data_type, $config);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->addColumn();
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

    def add_column(self, ac):
        column_name = "Country"
        data_type = "PLAIN"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, "35130000001055717")
        result = view.add_column(column_name, data_type)
        print(result)

try:
    obj = sample()
    obj.add_column(obj.ac)
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

    def add_column(self, ac):
        column_name = "Country"
        data_type = "PLAIN"
        config = {
            "columns": [{
                "columnName": "Discount",
                "dataType": "PERCENT"
            }, {
                "columnName": "Delivery Date",
                "dataType": "DATE_AS_DATE"
            }, {
                "columnName": "Status",
                "dataType": "PLAIN",
                "isMandatory": True,
                "default": "Pending"
            }]
        }
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, "35130000001055717")
        result = view.add_column(column_name, data_type, config)
        print(result)

try:
    obj = sample()
    obj.add_column(obj.ac)
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
var columnName = 'Country';
var dataType = 'PLAIN';

var view = ac.getViewInstance(orgId, workspaceId, viewId);

view.addColumn(columnName, dataType).then(function (result) {
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
var columnName = 'Country';
var dataType = 'PLAIN';
var config = {
    columns: [{
        columnName: 'Discount',
        dataType: 'PERCENT'
    }, {
        columnName: 'Delivery Date',
        dataType: 'DATE_AS_DATE'
    }, {
        columnName: 'Status',
        dataType: 'PLAIN',
        isMandatory: true,
        default: 'Pending'
    }]
};

var view = ac.getViewInstance(orgId, workspaceId, viewId);

view.addColumn(columnName, dataType, config).then(function (result) {
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

  def add_column
    column_name = "Country"
    data_type = "PLAIN"
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, "35130000001055717")
    result = view.add_column(column_name, data_type)
    puts result
  end
end

begin
  obj = Sample.new
  obj.add_column
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

  def add_column
    column_name = "Country"
    data_type = "PLAIN"
    config = {
        "columns" => [{
            "columnName" => "Discount",
            "dataType" => "PERCENT"
        }, {
            "columnName" => "Delivery Date",
            "dataType" => "DATE_AS_DATE"
        }, {
            "columnName" => "Status",
            "dataType" => "PLAIN",
            "isMandatory" => true,
            "default" => "Pending"
        }]
    }
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, "35130000001055717")
    result = view.add_column(column_name, data_type, config)
    puts result
  end
end

begin
  obj = Sample.new
  obj.add_column
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
config.put("columnName", "Country");
config.put("dataType", "PLAIN");
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/35130000001055717/columns"
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
config_columns = List();
config_columns_item1 = Map();
config_columns_item1.put("columnName", "Discount");
config_columns_item1.put("dataType", "PERCENT");
config_columns.add(config_columns_item1);
config_columns_item2 = Map();
config_columns_item2.put("columnName", "Delivery Date");
config_columns_item2.put("dataType", "DATE_AS_DATE");
config_columns.add(config_columns_item2);
config_columns_item3 = Map();
config_columns_item3.put("columnName", "Status");
config_columns_item3.put("dataType", "PLAIN");
config_columns_item3.put("isMandatory", true);
config_columns_item3.put("default", "Pending");
config_columns.add(config_columns_item3);
config.put("columns", config_columns);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/35130000001055717/columns"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Add Column](../../../domains/data-modeling-and-schema/columns/add-column.md) - full endpoint reference.
- [Columns overview](../../../domains/data-modeling-and-schema/columns/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
