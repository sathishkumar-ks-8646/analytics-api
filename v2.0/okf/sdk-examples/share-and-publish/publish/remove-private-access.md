---
type: SDK Example
title: SDK examples - Remove Private Access
description: "Code samples in 9 languages for DELETE /restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink (removePrivateAccess)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - share-and-publish
  - publish
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
  operation_id: removePrivateAccess
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink"
  endpoint_doc: "/domains/share-and-publish/publish/remove-private-access.md"
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
    resource: "/domains/share-and-publish/publish/remove-private-access.md"
    title: Endpoint reference - Remove Private Access
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Remove Private Access](../../../domains/share-and-publish/publish/remove-private-access.md) (`DELETE /restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/publish/privatelink" -X 'DELETE' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
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
        long viewId = 35130000001055717;

        public void RemovePrivateAccess(IAnalyticsClient ac)
        {
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.RemovePrivateAccess();
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.RemovePrivateAccess(ac);
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
    viewId = "35130000001055717"
)

func RemovePrivateAccess(ac ZAnalytics.Client) {
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    exception := view.RemovePrivateAccess()
    if exception != nil {
        fmt.Println("Error - " + exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    RemovePrivateAccess(ac)
}
```

## Java

```java
import com.zoho.analytics.client.*;
import org.json.*;

public class Test {
    private long orgId = 55522777l;
    private long workspaceId = 35130000001055707l;
    private long viewId = 35130000001055717l;

    public static void main(String args[]) {
        String clientId = "1000.xxxxxxx";
        String clientSecret = "xxxxxxx";
        String refreshToken = "1000.xxxxxxx.xxxxxxx";
        Test tObj = new Test();
        AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
        try {
            tObj.removePrivateAccess(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void removePrivateAccess(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.removePrivateAccess();
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

    function removePrivateAccess() {
        $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
        $view->removePrivateAccess();
        echo "success\n";
    }
}

$obj = new Test();
$obj->removePrivateAccess();
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
    VIEWID = "35130000001055717"

class Sample:
    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def remove_private_access(self, ac):
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.remove_private_access()
        print("success")

obj = Sample()
obj.remove_private_access(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';
var viewId = '35130000001055717';

var view = ac.getViewInstance(orgId, workspaceId, viewId);
view.removePrivateAccess().then(() => { console.log('success'); }).catch((error) => { console.log(error); });
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

  def remove_private_access
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    view.remove_private_access
    puts "success"
  end
end

obj = Sample.new
obj.remove_private_access
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
viewId = "35130000001055717";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/" + viewId + "/publish/privatelink"
  type :DELETE
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Remove Private Access](../../../domains/share-and-publish/publish/remove-private-access.md) - full endpoint reference.
- [Publish overview](../../../domains/share-and-publish/publish/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
