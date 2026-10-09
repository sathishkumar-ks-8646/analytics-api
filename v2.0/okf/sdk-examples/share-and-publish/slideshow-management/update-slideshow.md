---
type: SDK Example
title: SDK examples - Update Slide Show
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id}/slides/{slide-id} (updateSlideshow)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}"
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
  operation_id: updateSlideshow
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}"
  endpoint_doc: "/domains/share-and-publish/slideshow-management/update-slideshow.md"
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
    resource: "/domains/share-and-publish/slideshow-management/update-slideshow.md"
    title: Endpoint reference - Update Slide Show
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Update Slide Show](../../../domains/share-and-publish/slideshow-management/update-slideshow.md) (`PUT /restapi/v2/workspaces/{workspace-id}/slides/{slide-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/slides/35130000001056501" -X 'PUT' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"slideName":"Q1 Highlights Updated"}'
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

        public void UpdateSlideshow(IAnalyticsClient ac)
        {
            long slideId = 35130000001056501L;
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("slideName", "Q1 Highlights Updated");
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.UpdateSlideshow(slideId, config);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.UpdateSlideshow(ac);
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

func UpdateSlideshow(ac ZAnalytics.Client) {
    slideid := "35130000001056501"
    config := map[string]interface{}{
        "slideName": "Q1 Highlights Updated",
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    exception := workspace.UpdateSlideshow(slideid, config)
    if exception != nil {
        fmt.Println("Error - " + exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    UpdateSlideshow(ac)
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
            tObj.updateSlideshow(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void updateSlideshow(AnalyticsClient ac) throws Exception {
        long slideId = 35130000001056501l;
        JSONObject config = new JSONObject();
        config.put("slideName", "Q1 Highlights Updated");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.updateSlideshow(slideId, config);
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

    function __construct() {
        $this->ac = new AnalyticsClient("1000.xxxxxxx", "xxxxxxx", "1000.xxxxxxx.xxxxxxx");
    }

    function updateSlideshow() {
        $slide_id = "35130000001056501";
        $config = array("slideName" => "Q1 Highlights Updated");
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->updateSlideshow($slide_id, $config);
        echo "success\n";
    }
}

$obj = new Test();
$obj->updateSlideshow();
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

    def update_slideshow(self, ac):
        slide_id = "35130000001056501"
        config = {"slideName": "Q1 Highlights Updated"}
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.update_slideshow(slide_id, config)
        print("success")

obj = Sample()
obj.update_slideshow(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var slideId = '35130000001056501';
var config = { slideName: 'Q1 Highlights Updated' };
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.updateSlideshow(slideId, config).then(() => { console.log('success'); }).catch((error) => { console.log(error); });
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

  def update_slideshow
    slide_id = "35130000001056501"
    config = { "slideName" => "Q1 Highlights Updated" }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.update_slideshow(slide_id, config)
    puts "success"
  end
end

obj = Sample.new
obj.update_slideshow
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
slideId = "35130000001056501";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("slideName", "Q1 Highlights Updated");
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/slides/" + slideId
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Update Slide Show](../../../domains/share-and-publish/slideshow-management/update-slideshow.md) - full endpoint reference.
- [Slideshow Management overview](../../../domains/share-and-publish/slideshow-management/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
