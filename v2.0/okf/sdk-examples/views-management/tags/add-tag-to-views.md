---
type: SDK Example
title: SDK examples - Add Tag To Multiple Views
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views (addTagToViews)."
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
  operation_id: addTagToViews
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views"
  endpoint_doc: "/domains/views-management/tags/add-tag-to-views.md"
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
    last_modified: 2026-10-09T08:29:02Z
  - id: endpoint-doc
    resource: "/domains/views-management/tags/add-tag-to-views.md"
    title: Endpoint reference - Add Tag To Multiple Views
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Add Tag To Multiple Views](../../../domains/views-management/tags/add-tag-to-views.md) (`POST /restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/tags/35130000001364501/views" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"viewIds":["35130000001055717","35130000001055733"]}'
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

        public void AddTagToViews(IAnalyticsClient ac)
        {
            long tagId = 35130000001364501L;
            List<long> viewIds = new List<long>();
            viewIds.Add(35130000001055717L);
            viewIds.Add(35130000001055733L);
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.AddTagToViews(tagId, viewIds);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.AddTagToViews(ac);
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

func AddTagToViews(ac ZAnalytics.Client) {
    tagId := "35130000001364501"
    viewIds := []string{"35130000001055717", "35130000001055733"}
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    exception := workspace.AddTagToViews(tagId, viewIds)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    AddTagToViews(ac)
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
            tObj.addTagToViews(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void addTagToViews(AnalyticsClient ac) throws Exception {
        long tagId = 35130000001364501l;
        JSONArray viewIds = new JSONArray();
        viewIds.put("35130000001055717");
        viewIds.put("35130000001055733");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.addTagToViews(tagId, viewIds);
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

    function addTagToViews() {
        $tag_id = "35130000001364501";
        $view_ids = array("35130000001055717", "35130000001055733");
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->addTagToViews($tag_id, $view_ids);
        echo "success\n";
    }
}

$obj = new Test();
$obj->addTagToViews();
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

    def add_tag_to_views(self, ac):
        tag_id = "35130000001364501"
        view_ids = ["35130000001055717", "35130000001055733"]
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.add_tag_to_views(tag_id, view_ids)
        print("success")

obj = Sample()
obj.add_tag_to_views(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var tagId = '35130000001364501';
var viewIds = ['35130000001055717', '35130000001055733'];
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.addTagToViews(tagId, viewIds).then(() => { console.log('success'); }).catch((error) => { console.log(error); });
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

  def add_tag_to_views
    tag_id = "35130000001364501"
    view_ids = ["35130000001055717", "35130000001055733"]
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.add_tag_to_views(tag_id, view_ids)
    puts "success"
  end
end

obj = Sample.new
obj.add_tag_to_views
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
tagId = "35130000001364501";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
viewIds = List();
viewIds.add("35130000001055717");
viewIds.add("35130000001055733");
config.put("viewIds", viewIds);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/tags/" + tagId + "/views"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Add Tag To Multiple Views](../../../domains/views-management/tags/add-tag-to-views.md) - full endpoint reference.
- [Tags overview](../../../domains/views-management/tags/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
