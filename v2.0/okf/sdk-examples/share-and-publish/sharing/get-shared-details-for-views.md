---
type: SDK Example
title: SDK examples - Get Shared Details
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/share/shareddetails (getSharedDetailsForViews)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/share/shareddetails"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - share-and-publish
  - sharing
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
  operation_id: getSharedDetailsForViews
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/share/shareddetails"
  endpoint_doc: "/domains/share-and-publish/sharing/get-shared-details-for-views.md"
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
    last_modified: 2026-10-09T08:29:02Z
  - id: endpoint-doc
    resource: "/domains/share-and-publish/sharing/get-shared-details-for-views.md"
    title: Endpoint reference - Get Shared Details
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

Code samples for [Get Shared Details](../../../domains/share-and-publish/sharing/get-shared-details-for-views.md) (`GET /restapi/v2/workspaces/{workspace-id}/share/shareddetails`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/share/shareddetails?CONFIG=%7B%22viewIds%22%3A%5B%2235130000001055717%22%5D%7D" -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
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

        public void GetSharedDetailsForViews(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            List<long> viewIds = new List<long>();
            viewIds.Add(35130000001055717L);
            JsonElement result = ws.GetSharedDetailsForViews(viewIds);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.GetSharedDetailsForViews(ac);
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

func GetSharedDetailsForViews(ac ZAnalytics.Client) {
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    viewids := []int64{35130000001055717}
    result, exception := workspace.GetSharedDetailsForViews(viewids)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetSharedDetailsForViews(ac)
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
            tObj.getSharedDetailsForViews(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void getSharedDetailsForViews(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray viewIds = new JSONArray();
        viewIds.put("35130000001055717");
        JSONArray result = workspace.getSharedDetailsForViews(viewIds);
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

    function getSharedDetailsForViews() {
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $view_ids = array("35130000001055717");
        $response = $workspace->getSharedDetailsForViews($view_ids);
        print_r($response);
    }
}

$obj = new Test();
$obj->getSharedDetailsForViews();
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

    def get_shared_details_for_views(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        view_ids = ["35130000001055717"]
        result = workspace.get_shared_details_for_views(view_ids)
        print(result)

obj = Sample()
obj.get_shared_details_for_views(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
var viewIds = ['35130000001055717'];
workspace.getSharedDetailsForViews(viewIds).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def get_shared_details_for_views
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    view_ids = [Config::VIEWID]
    result = workspace.get_shared_details_for_views(view_ids)
    puts result
  end
end

obj = Sample.new
obj.get_shared_details_for_views
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
viewIds = List();
viewIds.add("35130000001055717");
config.put("viewIds", viewIds);
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/share/shareddetails?CONFIG=" + zoho.encryption.urlEncode(config.toString())
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Shared Details](../../../domains/share-and-publish/sharing/get-shared-details-for-views.md) - full endpoint reference.
- [Sharing overview](../../../domains/share-and-publish/sharing/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
