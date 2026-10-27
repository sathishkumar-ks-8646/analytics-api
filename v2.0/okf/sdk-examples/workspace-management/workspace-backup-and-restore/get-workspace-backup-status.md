---
type: SDK Example
title: SDK examples - Get Workspace Backup Status
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/status (getWorkspaceBackupStatus)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/status"
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
  operation_id: getWorkspaceBackupStatus
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/status"
  endpoint_doc: "/domains/workspace-management/workspace-backup-and-restore/get-workspace-backup-status.md"
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
    resource: "/domains/workspace-management/workspace-backup-and-restore/get-workspace-backup-status.md"
    title: Endpoint reference - Get Workspace Backup Status
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

Code samples for [Get Workspace Backup Status](../../../domains/workspace-management/workspace-backup-and-restore/get-workspace-backup-status.md) (`GET /restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/status`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/backups/<backup-id>/status" \
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

        public void GetWorkspaceBackupStatus(IAnalyticsClient ac)
        {
            long backupId = 35130000001056701L;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetWorkspaceBackupStatus(backupId);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.GetWorkspaceBackupStatus(ac);
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

func GetWorkspaceBackupStatus(ac ZAnalytics.Client) {
    backupid := "35130000001056701"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.GetWorkspaceBackupStatus(backupid)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetWorkspaceBackupStatus(ac)
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
            tObj.getWorkspaceBackupStatus(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void getWorkspaceBackupStatus(AnalyticsClient ac) throws Exception {
        long backupId = 35130000001056701l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getWorkspaceBackupStatus(backupId);
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

    function getWorkspaceBackupStatus() {
        $backup_id = "35130000001056701";
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $response = $workspace->getWorkspaceBackupStatus($backup_id);
        print_r($response);
    }
}

$obj = new Test();
$obj->getWorkspaceBackupStatus();
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

    def get_workspace_backup_status(self, ac):
        backup_id = "35130000001056701"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_workspace_backup_status(backup_id)
        print(result)

obj = Sample()
obj.get_workspace_backup_status(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var backupId = "35130000001056701";
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.getWorkspaceBackupStatus(backupId).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def get_workspace_backup_status
    backup_id = "35130000001056701"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_workspace_backup_status(backup_id)
    puts result
  end
end

obj = Sample.new
obj.get_workspace_backup_status
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
backupId = "35130000001056601";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/backups/" + backupId + "/status"
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Workspace Backup Status](../../../domains/workspace-management/workspace-backup-and-restore/get-workspace-backup-status.md) - full endpoint reference.
- [Workspace Backup & Restore overview](../../../domains/workspace-management/workspace-backup-and-restore/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
