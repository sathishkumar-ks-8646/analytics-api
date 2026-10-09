---
type: SDK Example
title: SDK examples - Create Slide Show
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/slides (createSlideshow)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/slides"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - share-and-publish
  - slideshow-management
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
  operation_id: createSlideshow
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/slides"
  endpoint_doc: "/domains/share-and-publish/slideshow-management/create-slideshow.md"
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
    resource: "/domains/share-and-publish/slideshow-management/create-slideshow.md"
    title: Endpoint reference - Create Slide Show
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Create Slide Show](../../../domains/share-and-publish/slideshow-management/create-slideshow.md) (`POST /restapi/v2/workspaces/{workspace-id}/slides`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/slides" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"slideName":"Q1 Highlights","viewIds":["35130000001055717"]}'
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

        public void CreateSlideshow(IAnalyticsClient ac)
        {
            string slideName = "Q1 Highlights";
            List<long> viewIds = new List<long>();
            viewIds.Add(35130000001055717L);
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            long result = workspace.CreateSlideshow(slideName, viewIds, null);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.CreateSlideshow(ac);
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

func CreateSlideshow(ac ZAnalytics.Client) {
    slidename := "Q1 Highlights"
    viewids := []int64{35130000001055717}
    config := map[string]interface{}{}
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.CreateSlideshow(slidename, viewids, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateSlideshow(ac)
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
            tObj.createSlideshow(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void createSlideshow(AnalyticsClient ac) throws Exception {
        String slideName = "Q1 Highlights";
        JSONArray viewIds = new JSONArray();
        viewIds.put("35130000001055717");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        long result = workspace.createSlideshow(slideName, viewIds, null);
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

    function createSlideshow() {
        $slide_name = "Q1 Highlights";
        $view_ids = array("35130000001055717");
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $response = $workspace->createSlideshow($slide_name, $view_ids);
        print_r($response);
    }
}

$obj = new Test();
$obj->createSlideshow();
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

    def create_slideshow(self, ac):
        slide_name = "Q1 Highlights"
        view_ids = ["35130000001055717"]
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_slideshow(slide_name, view_ids)
        print(result)

obj = Sample()
obj.create_slideshow(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var slideName = 'Q1 Highlights';
var viewIds = ['35130000001055717'];
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.createSlideshow(slideName, viewIds).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def create_slideshow
    slide_name = "Q1 Highlights"
    view_ids = [Config::VIEWID]
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.create_slideshow(slide_name, view_ids)
    puts result
  end
end

obj = Sample.new
obj.create_slideshow
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("slideName", "Q1 Highlights");
viewIds = List();
viewIds.add("35130000001055717");
config.put("viewIds", viewIds);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/slides"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Create Slide Show](../../../domains/share-and-publish/slideshow-management/create-slideshow.md) - full endpoint reference.
- [Slideshow Management overview](../../../domains/share-and-publish/slideshow-management/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
