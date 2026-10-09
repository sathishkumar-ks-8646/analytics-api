---
type: SDK Example
title: SDK examples - Share Views
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/share (shareViews)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/share"
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
  operation_id: shareViews
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/share"
  endpoint_doc: "/domains/share-and-publish/sharing/share-views.md"
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
    resource: "/domains/share-and-publish/sharing/share-views.md"
    title: Endpoint reference - Share Views
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

Code samples for [Share Views](../../../domains/share-and-publish/sharing/share-views.md) (`POST /restapi/v2/workspaces/{workspace-id}/share`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/share" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"viewIds":["35130000001055717"],"emailIds":["user@example.com"],"permissions":{"read":true}}'
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

        public void ShareViews(IAnalyticsClient ac)
        {
            List<long> viewIds = new List<long>();
            viewIds.Add(35130000001055717L);
            List<string> emailIds = new List<string>();
            emailIds.Add("user@example.com");
            Dictionary<string, bool> permissions = new Dictionary<string, bool>();
            permissions.Add("read", true);
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.ShareViews(viewIds, emailIds, permissions, null);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.ShareViews(ac);
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

func ShareViews(ac ZAnalytics.Client) {
    viewids := []int64{35130000001055717}
    emailids := []string{"user@example.com"}
    permissions := map[string]bool{"read": true}
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    err := workspace.ShareViews(viewids, emailids, permissions, nil)
    if err != nil {
        fmt.Println("Error - " + err.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    ShareViews(ac)
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
            tObj.shareViews(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void shareViews(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray viewIds = new JSONArray();
        viewIds.put("35130000001055717");
        JSONArray emailIds = new JSONArray();
        emailIds.put("user@example.com");
        JSONObject permissions = new JSONObject();
        permissions.put("read", true);
        workspace.shareViews(viewIds, emailIds, permissions, null);
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

    function shareViews() {
        $view_ids = array("35130000001055717");
        $email_ids = array("user@example.com");
        $permissions = array("read" => true);
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->shareViews($view_ids, $email_ids, $permissions);
        echo "success\n";
    }
}

$obj = new Test();
$obj->shareViews();
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

    def share_views(self, ac):
        view_ids = ["35130000001055717"]
        email_ids = ["user@example.com"]
        permissions = {"read": True}
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.share_views(view_ids, email_ids, permissions)
        print("success")

obj = Sample()
obj.share_views(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var viewIds = ['35130000001055717'];
var emailIds = ['user@example.com'];
var permissions = { read: true };
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.shareViews(viewIds, emailIds, permissions).then(() => { console.log('success'); }).catch((error) => { console.log(error); });
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

  def share_views
    view_ids = [Config::VIEWID]
    email_ids = ["user@example.com"]
    permissions = { "read" => true }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.share_views(view_ids, email_ids, permissions)
    puts "success"
  end
end

obj = Sample.new
obj.share_views
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
emailIds = List();
emailIds.add("user@example.com");
config.put("emailIds", emailIds);
permissions = Map();
permissions.put("read", true);
config.put("permissions", permissions);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/share"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Share Views](../../../domains/share-and-publish/sharing/share-views.md) - full endpoint reference.
- [Sharing overview](../../../domains/share-and-publish/sharing/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
