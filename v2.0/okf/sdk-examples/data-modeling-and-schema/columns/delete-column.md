---
type: SDK Example
title: SDK examples - Delete Column
description: "Code samples in 9 languages for DELETE /restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id} (deleteColumn)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}"
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
  operation_id: deleteColumn
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}"
  endpoint_doc: "/domains/data-modeling-and-schema/columns/delete-column.md"
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
    resource: "/domains/data-modeling-and-schema/columns/delete-column.md"
    title: Endpoint reference - Delete Column
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Delete Column](../../../domains/data-modeling-and-schema/columns/delete-column.md) (`DELETE /restapi/v2/workspaces/{workspace-id}/views/{view-id}/columns/{column-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

Variant 1:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/columns/35130000001055811" -X 'DELETE' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={}'
```

Variant 2:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/columns/35130000001055811" -X 'DELETE' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"deleteDependentViews":true}'
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

        public void DeleteColumn(IAnalyticsClient ac)
        {
            long viewId = 35130000001055717;
            long columnId = 35130000001055811;
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.DeleteColumn(columnId, null);
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
                obj.DeleteColumn(ac);
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

        public void DeleteColumn(IAnalyticsClient ac)
        {
            long viewId = 35130000001055717;
            long columnId = 35130000001055811;
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("deleteDependentViews", true);
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.DeleteColumn(columnId, config);
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
                obj.DeleteColumn(ac);
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

func DeleteColumn(ac ZAnalytics.Client) {
    viewId := "35130000001055717"
    columnId := "35130000001055811"
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    exception := view.DeleteColumn(columnId, nil)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    DeleteColumn(ac)
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

func DeleteColumn(ac ZAnalytics.Client) {
    viewId := "35130000001055717"
    columnId := "35130000001055811"
    config := map[string]interface{}{
        "deleteDependentViews": true,
    }
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    exception := view.DeleteColumn(columnId, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    DeleteColumn(ac)
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
            tObj.deleteColumn(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void deleteColumn(AnalyticsClient ac) throws Exception {
        long viewId = 35130000001055717l;
        long columnId = 35130000001055811l;
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.deleteColumn(columnId, null);
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
            tObj.deleteColumn(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void deleteColumn(AnalyticsClient ac) throws Exception {
        long viewId = 35130000001055717l;
        long columnId = 35130000001055811l;
        JSONObject config = new JSONObject();
        config.put("deleteDependentViews", true);
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.deleteColumn(columnId, config);
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

        function deleteColumn() {
            $view_id = "35130000001055717";
            $column_id = "35130000001055811";
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $view_id);
            $view->deleteColumn($column_id);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->deleteColumn();
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

        function deleteColumn() {
            $view_id = "35130000001055717";
            $column_id = "35130000001055811";
            $config = array(
                "deleteDependentViews" => true
            );
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $view_id);
            $view->deleteColumn($column_id, $config);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->deleteColumn();
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

    def delete_column(self, ac):
        column_id = "35130000001055811"
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, "35130000001055717")
        view.delete_column(column_id)
        print("success")

try:
    obj = sample()
    obj.delete_column(obj.ac)
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

    def delete_column(self, ac):
        column_id = "35130000001055811"
        config = {
            "deleteDependentViews": True
        }
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, "35130000001055717")
        view.delete_column(column_id, config)
        print("success")

try:
    obj = sample()
    obj.delete_column(obj.ac)
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
var columnId = '35130000001055811';

var view = ac.getViewInstance(orgId, workspaceId, viewId);

view.deleteColumn(columnId).then(function () {
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
var columnId = '35130000001055811';
var config = {
    deleteDependentViews: true
};

var view = ac.getViewInstance(orgId, workspaceId, viewId);

view.deleteColumn(columnId, config).then(function () {
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

  def delete_column
    column_id = "35130000001055811"
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, "35130000001055717")
    view.delete_column(column_id)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.delete_column
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

  def delete_column
    column_id = "35130000001055811"
    config = {
        "deleteDependentViews" => true
    }
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, "35130000001055717")
    view.delete_column(column_id, config)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.delete_column
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
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/35130000001055717/columns/35130000001055811"
  type :DELETE
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
config.put("deleteDependentViews", true);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/35130000001055717/columns/35130000001055811"
  type :DELETE
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Delete Column](../../../domains/data-modeling-and-schema/columns/delete-column.md) - full endpoint reference.
- [Columns overview](../../../domains/data-modeling-and-schema/columns/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
