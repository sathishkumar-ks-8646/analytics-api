---
type: SDK Example
title: SDK examples - Save As View
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/saveas (saveAsView)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/saveas"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - views-management
  - view-operations
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
  operation_id: saveAsView
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/saveas"
  endpoint_doc: "/domains/views-management/view-operations/save-as-view.md"
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
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
  - id: endpoint-doc
    resource: "/domains/views-management/view-operations/save-as-view.md"
    title: Endpoint reference - Save As View
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

Code samples for [Save As View](../../../domains/views-management/view-operations/save-as-view.md) (`POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/saveas`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/saveas" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"viewName":"Sales_Copy","viewDesc":"Copy of the Sales table"}'
```

## C#

```csharp
using System;
using System.Collections.Generic;
using System.Text.Json;
using ZohoAnalytics;

namespace ZohoAnalyticsTest
{
    class Program
    {
        long orgId = 55522777;
        long workspaceId = 35130000001055707;
        long viewId = 35130000001055717;

        public void SaveAsView(IAnalyticsClient ac)
        {
            string newViewName = "Sales_Copy";
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("viewDesc", "Copy of the Sales table");
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            long newViewId = view.SaveAs(newViewName, config);
            Console.WriteLine(newViewId);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.SaveAsView(ac);
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

var (
    clientId = "1000.xxxxxxx"
    clientSecret = "xxxxxxx"
    refreshToken = "1000.xxxxxxx.xxxxxxx"
    orgId = "55522777"
    workspaceId = "35130000001055707"
    viewId = "35130000001055717"
)

func SaveAsView(ac ZAnalytics.Client) {
    config := map[string]interface{}{"viewDesc": "Copy of the Sales table"}
    newviewname := "Sales_Copy"
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    result, exception := view.SaveAs(newviewname, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    SaveAsView(ac)
}
```

## Java

```java
import com.zoho.analytics.client.*;
import org.json.*;

public class Test {
    private long orgId = 55522777l;
    private long workspaceId = 35130000001055707l;
    private long viewId = 35130000001055717l;

    public static void main(String args[]) {
        String clientId = "1000.xxxxxxx";
        String clientSecret = "xxxxxxx";
        String refreshToken = "1000.xxxxxxx.xxxxxxx";
        Test tObj = new Test();
        AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
        try {
            tObj.saveAsView(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void saveAsView(AnalyticsClient ac) throws Exception {
        String newViewName = "Sales_Copy";
        JSONObject config = new JSONObject();
        config.put("viewDesc", "Copy of the Sales table");
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        long newViewId = view.saveAs(newViewName, config);
        System.out.println(newViewId);
    }
}
```

## PHP

```php
<?php
require 'AnalyticsClient.php';

class Test {
    public $ac;
    public $org_id = "55522777";
    public $workspace_id = "35130000001055707";
    public $view_id = "35130000001055717";

    function __construct() {
        $this->ac = new AnalyticsClient("1000.xxxxxxx", "xxxxxxx", "1000.xxxxxxx.xxxxxxx");
    }

    function saveAsView() {
        $new_view_name = "Sales_Copy";
        $config = array("viewDesc" => "Copy of the Sales table");
        $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
        $response = $view->saveAs($new_view_name, $config);
        print_r($response);
    }
}

$obj = new Test();
$obj->saveAsView();
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
    VIEWID = "35130000001055717"

class Sample:
    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def save_as_view(self, ac):
        new_view_name = "Sales_Copy"
        config = {"viewDesc": "Copy of the Sales table"}
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.save_as(new_view_name, config)
        print(result)

obj = Sample()
obj.save_as_view(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';
var viewId = '35130000001055717';

var newViewName = 'Sales_Copy';
var config = {viewDesc: 'Copy of the Sales table'};
var view = ac.getViewInstance(orgId, workspaceId, viewId);
view.saveAs(newViewName, config).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
```

## Ruby

```ruby
require 'zoho_analytics_client'

class Config
  ORGID = "55522777"
  WORKSPACEID = "35130000001055707"
  VIEWID = "35130000001055717"
end

class Sample
  def initialize
    @ac = AnalyticsClient.new.with_data_center("US").with_oauth({
      "clientId" => "1000.xxxxxxx",
      "clientSecret" => "xxxxxxx",
      "refreshToken" => "1000.xxxxxxx.xxxxxxx"
    }).build
  end

  def save_as_view
    new_view_name = "Sales_Copy"
    config = {"viewDesc" => "Copy of the Sales table"}
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    result = view.save_as(new_view_name, config)
    puts result
  end
end

obj = Sample.new
obj.save_as_view
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
viewId = "35130000001055717";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("viewName", "Sales_Copy");
config.put("viewDesc", "Copy of the Sales table");
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/" + viewId + "/saveas"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Save As View](../../../domains/views-management/view-operations/save-as-view.md) - full endpoint reference.
- [View Operations overview](../../../domains/views-management/view-operations/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
