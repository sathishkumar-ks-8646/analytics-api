---
type: SDK Example
title: SDK examples - Restore Trash View
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/trash/{view-id} (restoreTrashView)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/trash/{view-id}"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - views-management
  - trash-management
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
  operation_id: restoreTrashView
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/trash/{view-id}"
  endpoint_doc: "/domains/views-management/trash-management/restore-trash-view.md"
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
    last_modified: 2026-10-09T13:04:25Z
  - id: endpoint-doc
    resource: "/domains/views-management/trash-management/restore-trash-view.md"
    title: Endpoint reference - Restore Trash View
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Restore Trash View](../../../domains/views-management/trash-management/restore-trash-view.md) (`POST /restapi/v2/workspaces/{workspace-id}/trash/{view-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/trash/35130000001055717" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"withDependents":false}'
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

        public void RestoreTrashView(IAnalyticsClient ac)
        {
            long restoreViewId = 35130000001055717L;
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("withDependents", false);
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.RestoreTrashView(restoreViewId, config);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.RestoreTrashView(ac);
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

func RestoreTrashView(ac ZAnalytics.Client) {
    config := map[string]interface{}{"withDependents": false}
    viewid := "35130000001055717"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    exception := workspace.RestoreTrashView(viewid, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    RestoreTrashView(ac)
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
            tObj.restoreTrashView(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void restoreTrashView(AnalyticsClient ac) throws Exception {
        JSONObject config = new JSONObject();
        config.put("withDependents", false);
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        long restoreViewId = 35130000001055717l;
        workspace.restoreTrashView(restoreViewId, config);
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

    function restoreTrashView() {
        $view_id = "35130000001055717";
        $config = array("withDependents" => false);
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->restoreTrashView($view_id, $config);
        echo "success\n";
    }
}

$obj = new Test();
$obj->restoreTrashView();
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

    def restore_trash_views(self, ac):
        view_id = "35130000001055717"
        config = {"withDependents": False}
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.restore_trash_views(view_id, config)
        print("success")

obj = Sample()
obj.restore_trash_views(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var restoreViewId = '35130000001055717';
var config = {withDependents: false};
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.restoreTrashView(restoreViewId, config).then(() => { console.log('success'); }).catch((error) => { console.log(error); });
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

  def restore_trash_view
    restore_view_id = "35130000001055717"
    config = {"withDependents" => false}
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.restore_trash_views(restore_view_id, config)
    puts "success"
  end
end

obj = Sample.new
obj.restore_trash_view
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
restoreViewId = "35130000001055717";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("withDependents", false);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/trash/" + restoreViewId
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Restore Trash View](../../../domains/views-management/trash-management/restore-trash-view.md) - full endpoint reference.
- [Trash Management overview](../../../domains/views-management/trash-management/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
