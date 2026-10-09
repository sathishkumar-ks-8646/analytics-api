---
type: SDK Example
title: SDK examples - Copy Views
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/views/copy (copyViews)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/copy"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - views-management
  - view-operations
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
  operation_id: copyViews
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/copy"
  endpoint_doc: "/domains/views-management/view-operations/copy-views.md"
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
    resource: "/domains/views-management/view-operations/copy-views.md"
    title: Endpoint reference - Copy Views
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

Code samples for [Copy Views](../../../domains/views-management/view-operations/copy-views.md) (`POST /restapi/v2/workspaces/{workspace-id}/views/copy`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/copy" -X 'POST' -H 'ZANALYTICS-ORGID: <dest-org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"viewIds":["35130000001055717"],"destWorkspaceId":"35130000001055708","copyWithDependentViews":false}'
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

        public void CopyViews(IAnalyticsClient ac)
        {
            List<long> viewIds = new List<long>();
            viewIds.Add(35130000001055717L);
            long destWorkspaceId = 35130000001055708L;
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("copyWithDependentViews", false);
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement views = ws.CopyViews(viewIds, destWorkspaceId, config, null);
            Console.WriteLine(views);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.CopyViews(ac);
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

func CopyViews(ac ZAnalytics.Client) {
    config := map[string]interface{}{"copyWithDependentViews": false}
    destworkspaceid := "35130000001055708"
    viewids := [1]string{}
    viewids[0] = "35130000001055717"
    destorgid := ""
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.CopyViews(viewids, destworkspaceid, config, destorgid)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CopyViews(ac)
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
            tObj.copyViews(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void copyViews(AnalyticsClient ac) throws Exception {
        JSONArray viewIds = new JSONArray();
        viewIds.put("35130000001055717");
        long destWorkspaceId = 35130000001055708l;
        JSONObject config = new JSONObject();
        config.put("copyWithDependentViews", false);
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray views = workspace.copyViews(viewIds, destWorkspaceId, config, null);
        System.out.println(views);
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

    function copyViews() {
        $dest_workspace_id = "35130000001055708";
        $config = array("copyWithDependentViews" => false);
        $view_ids = array("35130000001055717");
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $response = $workspace->copyViews($view_ids, $dest_workspace_id, $config);
        print_r($response);
    }
}

$obj = new Test();
$obj->copyViews();
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

    def copy_views(self, ac):
        view_ids = ["35130000001055717"]
        dest_workspace_id = "35130000001055708"
        config = {"copyWithDependentViews": False}
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.copy_views(view_ids, dest_workspace_id, config)
        print(result)

obj = Sample()
obj.copy_views(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var viewIds = ['35130000001055717'];
var destWorkspaceId = '35130000001055708';
var config = {copyWithDependentViews: false};
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.copyViews(viewIds, destWorkspaceId, config).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def copy_views
    view_ids = [Config::VIEWID]
    dest_workspace_id = "35130000001055708"
    config = {"copyWithDependentViews" => false}
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.copy_views(view_ids, dest_workspace_id, config)
    puts result
  end
end

obj = Sample.new
obj.copy_views
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
config.put("destWorkspaceId", "35130000001055708");
config.put("copyWithDependentViews", false);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/copy"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Copy Views](../../../domains/views-management/view-operations/copy-views.md) - full endpoint reference.
- [View Operations overview](../../../domains/views-management/view-operations/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
