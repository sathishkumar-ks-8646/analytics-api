---
type: SDK Example
title: SDK examples - Get Workspace Restore Status
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/restores/{restore-id}/status (getWorkspaceRestoreStatus)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/restores/{restore-id}/status"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - workspace-management
  - workspace-backup-and-restore
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
  operation_id: getWorkspaceRestoreStatus
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/restores/{restore-id}/status"
  endpoint_doc: "/domains/workspace-management/workspace-backup-and-restore/get-workspace-restore-status.md"
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
    resource: "/domains/workspace-management/workspace-backup-and-restore/get-workspace-restore-status.md"
    title: Endpoint reference - Get Workspace Restore Status
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

Code samples for [Get Workspace Restore Status](../../../domains/workspace-management/workspace-backup-and-restore/get-workspace-restore-status.md) (`GET /restapi/v2/workspaces/{workspace-id}/restores/{restore-id}/status`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/restores/<restore-id>/status" \
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

        public void GetWorkspaceRestoreStatus(IAnalyticsClient ac)
        {
            long restoreId = 35130000001056801L;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetWorkspaceRestoreStatus(restoreId);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.GetWorkspaceRestoreStatus(ac);
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

func GetWorkspaceRestoreStatus(ac ZAnalytics.Client) {
    restoreid := "35130000001056801"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.GetWorkspaceRestoreStatus(restoreid)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetWorkspaceRestoreStatus(ac)
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
            tObj.getWorkspaceRestoreStatus(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void getWorkspaceRestoreStatus(AnalyticsClient ac) throws Exception {
        long restoreId = 35130000001056801l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getWorkspaceRestoreStatus(restoreId);
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

    function getWorkspaceRestoreStatus() {
        $restore_id = "35130000001056801";
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $response = $workspace->getWorkspaceRestoreStatus($restore_id);
        print_r($response);
    }
}

$obj = new Test();
$obj->getWorkspaceRestoreStatus();
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

    def get_workspace_restore_status(self, ac):
        restore_id = "35130000001056801"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_workspace_restore_status(restore_id)
        print(result)

obj = Sample()
obj.get_workspace_restore_status(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var restoreId = "35130000001056801";
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.getWorkspaceRestoreStatus(restoreId).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def get_workspace_restore_status
    restore_id = "35130000001056801"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_workspace_restore_status(restore_id)
    puts result
  end
end

obj = Sample.new
obj.get_workspace_restore_status
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
restoreId = "35130000001056605";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/restores/" + restoreId + "/status"
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Workspace Restore Status](../../../domains/workspace-management/workspace-backup-and-restore/get-workspace-restore-status.md) - full endpoint reference.
- [Workspace Backup & Restore overview](../../../domains/workspace-management/workspace-backup-and-restore/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
