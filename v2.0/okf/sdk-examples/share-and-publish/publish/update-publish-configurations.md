---
type: SDK Example
title: SDK examples - Update Publish Configurations
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config (updatePublishConfigurations)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config"
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
  operation_id: updatePublishConfigurations
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config"
  endpoint_doc: "/domains/share-and-publish/publish/update-publish-configurations.md"
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
    resource: "/domains/share-and-publish/publish/update-publish-configurations.md"
    title: Endpoint reference - Update Publish Configurations
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Update Publish Configurations](../../../domains/share-and-publish/publish/update-publish-configurations.md) (`PUT /restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/publish/config" -X 'PUT' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"includeToolBar":true,"includeSearchBox":true}'
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

        public void UpdatePublishConfigurations(IAnalyticsClient ac)
        {
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("includeToolBar", true);
            config.Add("includeSearchBox", true);
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.UpdatePublishConfigurations(config);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.UpdatePublishConfigurations(ac);
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

func UpdatePublishConfigurations(ac ZAnalytics.Client) {
    config := map[string]interface{}{}
    config["includeToolBar"] = true
    config["includeSearchBox"] = true
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    exception := view.UpdatePublishConfigurations(config)
    if exception != nil {
        fmt.Println("Error - " + exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    UpdatePublishConfigurations(ac)
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
            tObj.updatePublishConfigurations(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void updatePublishConfigurations(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONObject config = new JSONObject();
        config.put("includeToolBar", true);
        config.put("includeSearchBox", true);
        view.updatePublishConfigurations(config);
        System.out.println("success");
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

    function updatePublishConfigurations() {
        $config = array("includeToolBar" => true, "includeSearchBox" => true);
        $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
        $view->updatePublishConfigurations($config);
        echo "success\n";
    }
}

$obj = new Test();
$obj->updatePublishConfigurations();
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

    def update_publish_configurations(self, ac):
        config = {"includeToolBar": True, "includeSearchBox": True}
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.update_publish_configurations(config)
        print("success")

obj = Sample()
obj.update_publish_configurations(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';
var viewId = '35130000001055717';

var config = { includeToolBar: true, includeSearchBox: true };
var view = ac.getViewInstance(orgId, workspaceId, viewId);
view.updatePublishConfigurations(config).then(() => { console.log('success'); }).catch((error) => { console.log(error); });
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

  def update_publish_configurations
    config = { "includeToolBar" => true, "includeSearchBox" => true }
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    view.update_publish_configurations(config)
    puts "success"
  end
end

obj = Sample.new
obj.update_publish_configurations
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
viewId = "35130000001055717";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("includeToolBar", true);
config.put("includeSearchBox", true);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/" + viewId + "/publish/config"
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Update Publish Configurations](../../../domains/share-and-publish/publish/update-publish-configurations.md) - full endpoint reference.
- [Publish overview](../../../domains/share-and-publish/publish/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
