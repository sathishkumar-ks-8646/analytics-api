---
type: SDK Example
title: SDK examples - Get Slide URL
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/slides/{slide-id}/publish (getSlideshowUrl)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}/publish"
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
  operation_id: getSlideshowUrl
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}/publish"
  endpoint_doc: "/domains/share-and-publish/slideshow-management/get-slideshow-url.md"
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
    resource: "/domains/share-and-publish/slideshow-management/get-slideshow-url.md"
    title: Endpoint reference - Get Slide URL
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Get Slide URL](../../../domains/share-and-publish/slideshow-management/get-slideshow-url.md) (`GET /restapi/v2/workspaces/{workspace-id}/slides/{slide-id}/publish`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/slides/35130000001056501/publish" -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' -G --data-urlencode 'CONFIG={"autoplay":true,"slideInterval":25}'
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

        public void GetSlideshowUrl(IAnalyticsClient ac)
        {
            long slideId = 35130000001056501L;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("autoplay", true);
            config.Add("slideInterval", 25);
            string result = workspace.GetSlideshowURL(slideId, config);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.GetSlideshowUrl(ac);
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

func GetSlideshowUrl(ac ZAnalytics.Client) {
    slideid := "35130000001056501"
    config := map[string]interface{}{
        "autoplay": true,
        "slideInterval": 25,
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.GetSlideshowUrl(slideid, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetSlideshowUrl(ac)
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
            tObj.getSlideshowUrl(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void getSlideshowUrl(AnalyticsClient ac) throws Exception {
        long slideId = 35130000001056501l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject config = new JSONObject();
        config.put("autoplay", true);
        config.put("slideInterval", 25);
        String result = workspace.getSlideshowURL(slideId, config);
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

    function getSlideshowUrl() {
        $slide_id = "35130000001056501";
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $config = array(
            "autoplay" => true,
            "slideInterval" => 25
        );
        $response = $workspace->getSlideshowUrl($slide_id, $config);
        print_r($response);
    }
}

$obj = new Test();
$obj->getSlideshowUrl();
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

    def get_slideshow_url(self, ac):
        slide_id = "35130000001056501"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        config = {
            "autoplay": True,
            "slideInterval": 25
        }
        result = workspace.get_slideshow_url(slide_id, config)
        print(result)

obj = Sample()
obj.get_slideshow_url(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var slideId = '35130000001056501';
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
var config = { autoplay: true, slideInterval: 25 };
workspace.getSlideshowUrl(slideId, config).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def get_slideshow_url
    slide_id = "35130000001056501"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    config = {
      "autoplay" => true,
      "slideInterval" => 25
    }
    result = workspace.get_slideshow_url(slide_id, config)
    puts result
  end
end

obj = Sample.new
obj.get_slideshow_url
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
slideId = "35130000001056501";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("autoplay", true);
config.put("slideInterval", 25);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/slides/" + slideId + "/publish"
  type :GET
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Slide URL](../../../domains/share-and-publish/slideshow-management/get-slideshow-url.md) - full endpoint reference.
- [Slideshow Management overview](../../../domains/share-and-publish/slideshow-management/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
