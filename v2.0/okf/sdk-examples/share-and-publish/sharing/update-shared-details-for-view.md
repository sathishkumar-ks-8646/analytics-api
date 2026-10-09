---
type: SDK Example
title: SDK examples - Update Shared Details
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id}/views/{view-id}/share (UpdateSharedDetailsForView)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share"
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
  operation_id: UpdateSharedDetailsForView
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share"
  endpoint_doc: "/domains/share-and-publish/sharing/update-shared-details-for-view.md"
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
    resource: "/domains/share-and-publish/sharing/update-shared-details-for-view.md"
    title: Endpoint reference - Update Shared Details
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Update Shared Details](../../../domains/share-and-publish/sharing/update-shared-details-for-view.md) (`PUT /restapi/v2/workspaces/{workspace-id}/views/{view-id}/share`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/share" -X 'PUT' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"emailIds":["user@example.com"],"permissions":{"read":true}}'
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

        public void UpdateSharedDetails(IAnalyticsClient ac)
        {
            List<string> emailIds = new List<string>();
            emailIds.Add("user@example.com");
            Dictionary<string, bool> permissions = new Dictionary<string, bool>();
            permissions.Add("read", true);
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("emailIds", emailIds);
            config.Add("permissions", permissions);
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.UpdateSharedDetails(config);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.UpdateSharedDetails(ac);
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

func UpdateSharedDetails(ac ZAnalytics.Client) {
    emailids := []string{"user@example.com"}
    permissions := map[string]bool{"read": true}
    config := map[string]interface{}{
        "emailIds": emailids,
        "permissions": permissions,
    }
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    err := view.UpdateSharedDetails(config)
    if err != nil {
        fmt.Println("Error - " + err.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    UpdateSharedDetails(ac)
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
            tObj.updateSharedDetails(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void updateSharedDetails(AnalyticsClient ac) throws Exception {
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("user@example.com");
        JSONObject permissions = new JSONObject();
        permissions.put("read", true);
        JSONObject config = new JSONObject();
        config.put("emailIds", emailIds);
        config.put("permissions", permissions);
        view.UpdateSharedDetails(config);
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

    function updateSharedDetails() {
        $email_ids = array("user@example.com");
        $permissions = array("read" => true);
        $config = array(
            "emailIds" => $email_ids,
            "permissions" => $permissions
        );
        $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $this->view_id);
        $view->updateSharedDetails($config);
        echo "success\n";
    }
}

$obj = new Test();
$obj->updateSharedDetails();
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

    def update_shared_details(self, ac):
        config = {
            "emailIds": ["user@example.com"],
            "permissions": {"read": True}
        }
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, Config.VIEWID)
        view.update_shared_details(config)
        print("success")

obj = Sample()
obj.update_shared_details(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';
var viewId = '35130000001055717';

var config = { emailIds: ['user@example.com'], permissions: { read: true } };
var view = ac.getViewInstance(orgId, workspaceId, viewId);
view.updateSharedDetails(config).then(() => { console.log('success'); }).catch((error) => { console.log(error); });
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

  def update_shared_details
    config = {
      "emailIds" => ["user@example.com"],
      "permissions" => { "read" => true }
    }
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, Config::VIEWID)
    view.update_shared_details(config)
    puts "success"
  end
end

obj = Sample.new
obj.update_shared_details
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
viewId = "35130000001055717";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
emailIds = List();
emailIds.add("user@example.com");
config.put("emailIds", emailIds);
permissions = Map();
permissions.put("read", true);
config.put("permissions", permissions);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/" + viewId + "/share"
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Update Shared Details](../../../domains/share-and-publish/sharing/update-shared-details-for-view.md) - full endpoint reference.
- [Sharing overview](../../../domains/share-and-publish/sharing/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
