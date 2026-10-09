---
type: SDK Example
title: SDK examples - Get Slide List
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/slides (getSlideshows)."
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
  operation_id: getSlideshows
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/slides"
  endpoint_doc: "/domains/share-and-publish/slideshow-management/get-slideshows.md"
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
    resource: "/domains/share-and-publish/slideshow-management/get-slideshows.md"
    title: Endpoint reference - Get Slide List
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Get Slide List](../../../domains/share-and-publish/slideshow-management/get-slideshows.md) (`GET /restapi/v2/workspaces/{workspace-id}/slides`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/slides" -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
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

        public void GetSlideshows(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetSlideshows();
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.GetSlideshows(ac);
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

func GetSlideshows(ac ZAnalytics.Client) {
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.GetSlideshows()
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetSlideshows(ac)
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
            tObj.getSlideshows(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void getSlideshows(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getSlideshows();
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

    function getSlideshows() {
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $response = $workspace->getSlideshows();
        print_r($response);
    }
}

$obj = new Test();
$obj->getSlideshows();
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

    def get_slideshows(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_slideshows()
        print(result)

obj = Sample()
obj.get_slideshows(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.getSlideshows().then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def get_slideshows
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_slideshows
    puts result
  end
end

obj = Sample.new
obj.get_slideshows
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/slides"
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Slide List](../../../domains/share-and-publish/slideshow-management/get-slideshows.md) - full endpoint reference.
- [Slideshow Management overview](../../../domains/share-and-publish/slideshow-management/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
