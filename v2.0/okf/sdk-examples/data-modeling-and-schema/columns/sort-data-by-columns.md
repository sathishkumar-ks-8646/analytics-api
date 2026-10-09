---
type: SDK Example
title: SDK examples - Sort Data by Columns
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id}/views/{view-id}/data/sort (sortDataByColumns)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data/sort"
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
  operation_id: sortDataByColumns
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/data/sort"
  endpoint_doc: "/domains/data-modeling-and-schema/columns/sort-data-by-columns.md"
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
    resource: "/domains/data-modeling-and-schema/columns/sort-data-by-columns.md"
    title: Endpoint reference - Sort Data by Columns
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Sort Data by Columns](../../../domains/data-modeling-and-schema/columns/sort-data-by-columns.md) (`PUT /restapi/v2/workspaces/{workspace-id}/views/{view-id}/data/sort`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

Variant 1:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/data/sort" -X 'PUT' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"columns":["35130000001055811"],"sortOrder":1}'
```

Variant 2:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/data/sort" -X 'PUT' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"resetSort":true}'
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

        public void SortDataByColumns(IAnalyticsClient ac)
        {
            long viewId = 35130000001055717;
            List<long> columns = new List<long>() { 35130000001055811 };
            int? sortOrder = 1;
            bool resetSort = false;
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.SortDataByColumns(columns, sortOrder, resetSort, null);
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
                obj.SortDataByColumns(ac);
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

        public void SortDataByColumns(IAnalyticsClient ac)
        {
            long viewId = 35130000001055717;
            List<long> columns = new List<long>() {  };
            int? sortOrder = null;
            bool resetSort = true;
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.SortDataByColumns(columns, sortOrder, resetSort, null);
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
                obj.SortDataByColumns(ac);
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

func SortDataByColumns(ac ZAnalytics.Client) {
    viewId := "35130000001055717"
    columns := []string{"35130000001055811"}
    sortOrder := 1
    resetSort := false
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    exception := view.SortDataByColumns(columns, sortOrder, resetSort, nil)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    SortDataByColumns(ac)
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

func SortDataByColumns(ac ZAnalytics.Client) {
    viewId := "35130000001055717"
    columns := []string{}
    sortOrder := nil
    resetSort := true
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    exception := view.SortDataByColumns(columns, sortOrder, resetSort, nil)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    SortDataByColumns(ac)
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
            tObj.sortDataByColumns(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void sortDataByColumns(AnalyticsClient ac) throws Exception {
        long viewId = 35130000001055717l;
        JSONArray columns = new JSONArray();
        columns.put("35130000001055811");
        Integer sortOrder = 1;
        boolean resetSort = false;
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.sortDataByColumns(columns, sortOrder, resetSort, null);
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
            tObj.sortDataByColumns(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void sortDataByColumns(AnalyticsClient ac) throws Exception {
        long viewId = 35130000001055717l;
        JSONArray columns = new JSONArray();
        Integer sortOrder = null;
        boolean resetSort = true;
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.sortDataByColumns(columns, sortOrder, resetSort, null);
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

        function sortDataByColumns() {
            $view_id = "35130000001055717";
            $columns = array("35130000001055811");
            $sort_order = 1;
            $reset_sort = false;
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $view_id);
            $view->sortDataByColumns($columns, $sort_order, $reset_sort);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->sortDataByColumns();
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

        function sortDataByColumns() {
            $view_id = "35130000001055717";
            $columns = array();
            $sort_order = NULL;
            $reset_sort = true;
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $view_id);
            $view->sortDataByColumns($columns, $sort_order, $reset_sort);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->sortDataByColumns();
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

    def sort_data_by_columns(self, ac):
        columns = ["35130000001055811"]
        sort_order = 1
        reset_sort = False
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, "35130000001055717")
        view.sort_data_by_columns(columns, sort_order, reset_sort)
        print("success")

try:
    obj = sample()
    obj.sort_data_by_columns(obj.ac)
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

    def sort_data_by_columns(self, ac):
        columns = []
        sort_order = None
        reset_sort = True
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, "35130000001055717")
        view.sort_data_by_columns(columns, sort_order, reset_sort)
        print("success")

try:
    obj = sample()
    obj.sort_data_by_columns(obj.ac)
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
var columns = ['35130000001055811'];
var sortOrder = 1;
var resetSort = false;

var view = ac.getViewInstance(orgId, workspaceId, viewId);

view.sortDataByColumns(columns, sortOrder, resetSort).then(function () {
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

var viewId = '35130000001055717';
var columns = [];
var sortOrder = null;
var resetSort = true;

var view = ac.getViewInstance(orgId, workspaceId, viewId);

view.sortDataByColumns(columns, sortOrder, resetSort).then(function () {
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

  def sort_data_by_columns
    columns = ["35130000001055811"]
    sort_order = 1
    reset_sort = false
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, "35130000001055717")
    view.sort_data_by_columns(columns, sort_order, reset_sort)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.sort_data_by_columns
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

  def sort_data_by_columns
    columns = []
    sort_order = nil
    reset_sort = true
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, "35130000001055717")
    view.sort_data_by_columns(columns, sort_order, reset_sort)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.sort_data_by_columns
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
config_columns = List();
config_columns.add("35130000001055811");
config.put("columns", config_columns);
config.put("sortOrder", 1);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/35130000001055717/data/sort"
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
config.put("resetSort", true);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/35130000001055717/data/sort"
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Sort Data by Columns](../../../domains/data-modeling-and-schema/columns/sort-data-by-columns.md) - full endpoint reference.
- [Columns overview](../../../domains/data-modeling-and-schema/columns/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
