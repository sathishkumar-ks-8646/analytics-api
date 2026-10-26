---
type: SDK Example
title: SDK examples - Download Workspace Backup
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/download (downloadWorkspaceBackup)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/download"
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
  operation_id: downloadWorkspaceBackup
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/download"
  endpoint_doc: "/domains/workspace-management/workspace-backup-and-restore/download-workspace-backup.md"
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
    resource: "/domains/workspace-management/workspace-backup-and-restore/download-workspace-backup.md"
    title: Endpoint reference - Download Workspace Backup
generated:
  by: process:build_okf
  at: 2026-10-23T07:58:54Z
status: stable
---

# Summary

Code samples for [Download Workspace Backup](../../../domains/workspace-management/workspace-backup-and-restore/download-workspace-backup.md) (`GET /restapi/v2/workspaces/{workspace-id}/backups/{backup-id}/download`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/backups/<backup-id>/download" \
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

        public void DownloadWorkspaceBackup(IAnalyticsClient ac)
        {
            long backupId = 35130000001056701L;
            string filePath = "/home/user/workspace-backup.zip";
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.DownloadWorkspaceBackup(backupId, filePath, null);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.DownloadWorkspaceBackup(ac);
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

func DownloadWorkspaceBackup(ac ZAnalytics.Client) {
    backupid := "35130000001056701"
    filepath := "/home/user/workspace-backup.zip"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    exception := workspace.DownloadWorkspaceBackup(backupid, filepath, nil)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    DownloadWorkspaceBackup(ac)
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
            tObj.downloadWorkspaceBackup(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void downloadWorkspaceBackup(AnalyticsClient ac) throws Exception {
        long backupId = 35130000001056701l;
        String filePath = "/home/user/workspace-backup.zip";
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.downloadWorkspaceBackup(backupId, filePath, null);
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

    function downloadWorkspaceBackup() {
        $backup_id = "35130000001056701";
        $file_path = "/home/user/workspace-backup.zip";
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->downloadWorkspaceBackup($backup_id, $file_path);
        echo "success";
    }
}

$obj = new Test();
$obj->downloadWorkspaceBackup();
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

    def download_workspace_backup(self, ac):
        backup_id = "35130000001056701"
        file_path = "/home/user/workspace-backup.zip"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.download_workspace_backup(backup_id, file_path)
        print("success")

obj = Sample()
obj.download_workspace_backup(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var backupId = "35130000001056701";
var filePath = "/home/user/workspace-backup.zip";
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.downloadWorkspaceBackup(backupId, filePath).then(() => { console.log("success"); }).catch((error) => { console.log(error); });
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

  def download_workspace_backup
    backup_id = "35130000001056701"
    file_path = "/home/user/workspace-backup.zip"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.download_workspace_backup(backup_id, file_path)
    puts "success"
  end
end

obj = Sample.new
obj.download_workspace_backup
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
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/backups/" + backupId + "/download"
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Download Workspace Backup](../../../domains/workspace-management/workspace-backup-and-restore/download-workspace-backup.md) - full endpoint reference.
- [Workspace Backup & Restore overview](../../../domains/workspace-management/workspace-backup-and-restore/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
