---
type: SDK Example
title: SDK examples - Create Private URL
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink (createPrivateUrl)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink"
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
  operation_id: createPrivateUrl
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink"
  endpoint_doc: "/domains/share-and-publish/publish/create-private-url.md"
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
    resource: "/domains/share-and-publish/publish/create-private-url.md"
    title: Endpoint reference - Create Private URL
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Create Private URL](../../../domains/share-and-publish/publish/create-private-url.md) (`POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/publish/privatelink" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"permissions":{"export":true},"regenerateKey":false}'
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

        public void CreatePrivateUrl(IAnalyticsClient ac)
        {
            Dictionary<string, bool> permissions = new Dictionary<string, bool>();
            permissions.Add("export", true);
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("permissions", permissions);
            config.Add("regenerateKey", false);
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            string result = view.CreatePrivateURL(config);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.CreatePrivateUrl(ac);
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

func CreatePrivateUrl(ac ZAnalytics.Client) {
    permissions := map[string]bool{"export": true}
    config := map[string]interface{}{
        "permissions": permissions,
        "regenerateKey": false,
    }
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    result, exception := view.CreatePrivateUrl(config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreatePrivateUrl(ac)
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
            tObj.createPrivateURL(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void createPrivateURL(AnalyticsClient ac) throws Exception {
        JSONObject permissions = new JSONObject();
        permissions.put("export", true);
        JSONObject config = new JSONObject();
        config.put("permissions", permissions);
        config.put("regenerateKey", false);
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        String result = view.createPrivateURL(config);
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

    function createPrivateURL() {
        $config = array(
            "permissions" => array("export" => true),
            "regenerateKey" => false
        );
        $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
        $response = $view->createPrivateURL($config);
        print_r($response);
    }
}

$obj = new Test();
$obj->createPrivateURL();
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

    def create_private_url(self, ac):
        config = {
            "permissions": {"export": True},
            "regenerateKey": False
        }
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        result = view.create_private_url(config)
        print(result)

obj = Sample()
obj.create_private_url(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';
var viewId = '35130000001055717';

var config = { permissions: { export: true }, regenerateKey: false };
var view = ac.getViewInstance(orgId, workspaceId, viewId);
view.createPrivateUrl(config).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def create_private_url
    config = {
      "permissions" => { "export" => true },
      "regenerateKey" => false
    }
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    result = view.create_private_url(config)
    puts result
  end
end

obj = Sample.new
obj.create_private_url
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
viewId = "35130000001055717";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
permissions = Map();
permissions.put("export", true);
config.put("permissions", permissions);
config.put("regenerateKey", false);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/" + viewId + "/publish/privatelink"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Create Private URL](../../../domains/share-and-publish/publish/create-private-url.md) - full endpoint reference.
- [Publish overview](../../../domains/share-and-publish/publish/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
