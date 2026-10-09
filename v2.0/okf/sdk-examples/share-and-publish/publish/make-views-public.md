---
type: SDK Example
title: SDK examples - Make View Public
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/public (makeViewsPublic)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/public"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - share-and-publish
  - publish
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
  operation_id: makeViewsPublic
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/public"
  endpoint_doc: "/domains/share-and-publish/publish/make-views-public.md"
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
    resource: "/references/openapi/share-publish-grouped-api.json"
    title: OpenAPI 3 specification - share-publish-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
  - id: endpoint-doc
    resource: "/domains/share-and-publish/publish/make-views-public.md"
    title: Endpoint reference - Make View Public
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Make View Public](../../../domains/share-and-publish/publish/make-views-public.md) (`POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/public`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/publish/public" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"publicPermLevel":1,"permissions":{"export":true}}'
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

        public void MakeViewPublic(IAnalyticsClient ac)
        {
            Dictionary<string, bool> permissions = new Dictionary<string, bool>();
            permissions.Add("export", true);
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("publicPermLevel", 1);
            config.Add("permissions", permissions);
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            string result = view.MakeViewPublic(config);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.MakeViewPublic(ac);
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

func MakeViewPublic(ac ZAnalytics.Client) {
    permissions := map[string]bool{"export": true}
    config := map[string]interface{}{
        "publicPermLevel": 1,
        "permissions": permissions,
    }
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    result, exception := view.MakeViewPublic(config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    MakeViewPublic(ac)
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
            tObj.makeViewPublic(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void makeViewPublic(AnalyticsClient ac) throws Exception {
        JSONObject permissions = new JSONObject();
        permissions.put("export", true);
        JSONObject config = new JSONObject();
        config.put("publicPermLevel", 1);
        config.put("permissions", permissions);
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        String result = view.makeViewPublic(config);
        System.out.println(result);
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

    function makeViewPublic() {
        $config = array(
            "publicPermLevel" => 1,
            "permissions" => array("export" => true)
        );
        $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
        $response = $view->makeViewPublic($config);
        print_r($response);
    }
}

$obj = new Test();
$obj->makeViewPublic();
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

    def make_view_public(self, ac):
        config = {
            "publicPermLevel": 1,
            "permissions": {"export": True}
        }
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.make_view_public(config)
        print(result)

obj = Sample()
obj.make_view_public(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';
var viewId = '35130000001055717';

var config = { publicPermLevel: 1, permissions: { export: true } };
var view = ac.getViewInstance(orgId, workspaceId, viewId);
view.makeViewPublic(config).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def make_view_public
    config = {
      "publicPermLevel" => 1,
      "permissions" => { "export" => true }
    }
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    result = view.make_view_public(config)
    puts result
  end
end

obj = Sample.new
obj.make_view_public
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
viewId = "35130000001055717";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("publicPermLevel", 1);
permissions = Map();
permissions.put("export", true);
config.put("permissions", permissions);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/" + viewId + "/publish/public"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Make View Public](../../../domains/share-and-publish/publish/make-views-public.md) - full endpoint reference.
- [Publish overview](../../../domains/share-and-publish/publish/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
