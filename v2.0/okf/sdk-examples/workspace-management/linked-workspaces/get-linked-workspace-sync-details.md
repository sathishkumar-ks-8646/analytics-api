---
type: SDK Example
title: SDK examples - Get Linked Workspace Sync Details
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync (getLinkedWorkspaceSyncDetails)."
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
  operation_id: getLinkedWorkspaceSyncDetails
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync"
  endpoint_doc: "/domains/workspace-management/linked-workspaces/get-linked-workspace-sync-details.md"
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
    last_modified: 2026-10-20T17:34:40Z
  - id: endpoint-doc
    resource: "/domains/workspace-management/linked-workspaces/get-linked-workspace-sync-details.md"
    title: Endpoint reference - Get Linked Workspace Sync Details
generated:
  by: process:build_okf
  at: 2026-10-23T07:58:54Z
status: stable
---

# Summary

Code samples for [Get Linked Workspace Sync Details](../../../domains/workspace-management/linked-workspaces/get-linked-workspace-sync-details.md) (`GET /restapi/v2/workspaces/{workspace-id}/linkedworkspaces/sync`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/linkedworkspaces/sync?CONFIG=%7B%22sandboxIds%22%3A%5B%22137687000012345001%22%2C%22137687000012345002%22%5D%7D" \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>'
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

        public void GetLinkedWorkspaceSyncDetails(IAnalyticsClient ac)
        {
            List<long> sandboxIds = new List<long>();
            sandboxIds.Add(137687000012345001L);
            sandboxIds.Add(137687000012345002L);
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetLinkedWorkspaceSyncDetails(sandboxIds, null);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.GetLinkedWorkspaceSyncDetails(ac);
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

func GetLinkedWorkspaceSyncDetails(ac ZAnalytics.Client) {
    sandboxids := []string{"137687000012345001", "137687000012345002"}
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.GetLinkedWorkspaceSyncDetails(sandboxids, nil)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetLinkedWorkspaceSyncDetails(ac)
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
            tObj.getLinkedWorkspaceSyncDetails(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void getLinkedWorkspaceSyncDetails(AnalyticsClient ac) throws Exception {
        JSONArray sandboxIds = new JSONArray();
        sandboxIds.put("137687000012345001");
        sandboxIds.put("137687000012345002");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray result = workspace.getLinkedWorkspaceSyncDetails(sandboxIds, null);
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

    function getLinkedWorkspaceSyncDetails() {
        $sandbox_ids = array("137687000012345001", "137687000012345002");
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $response = $workspace->getLinkedWorkspaceSyncDetails($sandbox_ids);
        print_r($response);
    }
}

$obj = new Test();
$obj->getLinkedWorkspaceSyncDetails();
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

    def get_linked_workspace_sync_details(self, ac):
        sandbox_ids = ["137687000012345001", "137687000012345002"]
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_linked_workspace_sync_details(sandbox_ids)
        print(result)

obj = Sample()
obj.get_linked_workspace_sync_details(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var sandboxIds = ["137687000012345001", "137687000012345002"];
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.getLinkedWorkspaceSyncDetails(sandboxIds).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def get_linked_workspace_sync_details
    sandbox_ids = ["137687000012345001", "137687000012345002"]
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_linked_workspace_sync_details(sandbox_ids)
    puts result
  end
end

obj = Sample.new
obj.get_linked_workspace_sync_details
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"sandboxIds": ["137687000012345001", "137687000012345002"]};
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/linkedworkspaces/sync?CONFIG=" + zoho.encryption.urlEncode(config.toString())
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Linked Workspace Sync Details](../../../domains/workspace-management/linked-workspaces/get-linked-workspace-sync-details.md) - full endpoint reference.
- [Linked Workspaces overview](../../../domains/workspace-management/linked-workspaces/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
