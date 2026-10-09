---
type: SDK Example
title: SDK examples - Get Tagged Views
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views (getTaggedViews)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - views-management
  - tags
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
  operation_id: getTaggedViews
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views"
  endpoint_doc: "/domains/views-management/tags/get-tagged-views.md"
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
    resource: "/domains/views-management/tags/get-tagged-views.md"
    title: Endpoint reference - Get Tagged Views
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

Code samples for [Get Tagged Views](../../../domains/views-management/tags/get-tagged-views.md) (`GET /restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/tags/35130000001364501/views" -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' -G --data-urlencode 'CONFIG={"limit":10,"offset":10}'
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

        public void GetTaggedViews(IAnalyticsClient ac)
        {
            long tagId = 35130000001364501L;
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("limit", 10);
            config.Add("offset", 10);
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = ws.GetTaggedViews(tagId, config);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.GetTaggedViews(ac);
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
)

func GetTaggedViews(ac ZAnalytics.Client) {
    tagId := "35130000001364501"
    config := map[string]interface{}{"limit": 10, "offset": 10}
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.GetTaggedViews(tagId, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetTaggedViews(ac)
}
```

## Java

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
            tObj.getTaggedViews(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void getTaggedViews(AnalyticsClient ac) throws Exception {
        long tagId = 35130000001364501l;
        JSONObject config = new JSONObject();
        config.put("limit", 10);
        config.put("offset", 10);
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getTaggedViews(tagId, config);
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

    function __construct() {
        $this->ac = new AnalyticsClient("1000.xxxxxxx", "xxxxxxx", "1000.xxxxxxx.xxxxxxx");
    }

    function getTaggedViews() {
        $tag_id = "35130000001364501";
        $config = array("limit" => 10, "offset" => 10);
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $response = $workspace->getTaggedViews($tag_id, $config);
        print_r($response);
    }
}

$obj = new Test();
$obj->getTaggedViews();
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

class Sample:
    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def get_tagged_views(self, ac):
        tag_id = "35130000001364501"
        config = {"limit": 10, "offset": 10}
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_tagged_views(tag_id, config)
        print(result)

obj = Sample()
obj.get_tagged_views(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var tagId = '35130000001364501';
var config = {limit: 10, offset: 10};
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.getTaggedViews(tagId, config).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
```

## Ruby

```ruby
require 'zoho_analytics_client'

class Config
  ORGID = "55522777"
  WORKSPACEID = "35130000001055707"
end

class Sample
  def initialize
    @ac = AnalyticsClient.new.with_data_center("US").with_oauth({
      "clientId" => "1000.xxxxxxx",
      "clientSecret" => "xxxxxxx",
      "refreshToken" => "1000.xxxxxxx.xxxxxxx"
    }).build
  end

  def get_tagged_views
    tag_id = "35130000001364501"
    config = {"limit" => 10, "offset" => 10}
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_tagged_views(tag_id, config)
    puts result
  end
end

obj = Sample.new
obj.get_tagged_views
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
tagId = "35130000001364501";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("limit", 10);
config.put("offset", 10);
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/tags/" + tagId + "/views" + "?CONFIG=" + zoho.encryption.urlEncode(config.toString())
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Tagged Views](../../../domains/views-management/tags/get-tagged-views.md) - full endpoint reference.
- [Tags overview](../../../domains/views-management/tags/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
