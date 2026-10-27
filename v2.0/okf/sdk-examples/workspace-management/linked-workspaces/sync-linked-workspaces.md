---
type: SDK Example
title: SDK examples - Sync Linked Workspaces
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync (syncLinkedWorkspaces)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - workspace-management
  - linked-workspaces
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
  operation_id: syncLinkedWorkspaces
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync"
  endpoint_doc: "/domains/workspace-management/linked-workspaces/sync-linked-workspaces.md"
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
    resource: "/references/openapi/workspace-management-grouped-api.json"
    title: OpenAPI 3 specification - workspace-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T11:33:37Z
  - id: endpoint-doc
    resource: "/domains/workspace-management/linked-workspaces/sync-linked-workspaces.md"
    title: Endpoint reference - Sync Linked Workspaces
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

Code samples for [Sync Linked Workspaces](../../../domains/workspace-management/linked-workspaces/sync-linked-workspaces.md) (`POST /restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/linkedworkspaces/sync" \
  -X 'POST' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"scope":"ALL"}'
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

        public void SyncLinkedWorkspaces(IAnalyticsClient ac)
        {
            string scope = "ALL";
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.SyncLinkedWorkspaces(scope, null);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.SyncLinkedWorkspaces(ac);
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

func SyncLinkedWorkspaces(ac ZAnalytics.Client) {
    scope := "ALL"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    exception := workspace.SyncLinkedWorkspaces(scope, nil)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    SyncLinkedWorkspaces(ac)
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
            tObj.syncLinkedWorkspaces(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void syncLinkedWorkspaces(AnalyticsClient ac) throws Exception {
        String scope = "ALL";
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.syncLinkedWorkspaces(scope, null);
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

    function syncLinkedWorkspaces() {
        $scope = "ALL";
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->syncLinkedWorkspaces($scope);
        echo "success";
    }
}

$obj = new Test();
$obj->syncLinkedWorkspaces();
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

    def sync_linked_workspaces(self, ac):
        scope = "ALL"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.sync_linked_workspaces(scope)
        print("success")

obj = Sample()
obj.sync_linked_workspaces(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var scope = "ALL";
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.syncLinkedWorkspaces(scope).then(() => { console.log("success"); }).catch((error) => { console.log(error); });
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

  def sync_linked_workspaces
    scope = "ALL"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.sync_linked_workspaces(scope)
    puts "success"
  end
end

obj = Sample.new
obj.sync_linked_workspaces
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"scope": "ALL"};
response = invokeurl
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/linkedworkspaces/sync"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Sync Linked Workspaces](../../../domains/workspace-management/linked-workspaces/sync-linked-workspaces.md) - full endpoint reference.
- [Linked Workspaces overview](../../../domains/workspace-management/linked-workspaces/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
