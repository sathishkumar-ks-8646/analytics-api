---
type: SDK Example
title: SDK examples - Get Workspace Access Restrictions
description: "Code samples in 9 languages for GET /restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions (getWorkspaceAccessRestrictions)."
resource: "https://analyticsapi.zoho.com/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - organization-management
  - security-controls
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
  operation_id: getWorkspaceAccessRestrictions
  method: GET
  path: "/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions"
  endpoint_doc: "/domains/organization-management/security-controls/get-workspace-access-restrictions.md"
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
    resource: "/references/openapi/org-management-grouped-api.json"
    title: OpenAPI 3 specification - org-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-20T17:34:40Z
  - id: endpoint-doc
    resource: "/domains/organization-management/security-controls/get-workspace-access-restrictions.md"
    title: Endpoint reference - Get Workspace Access Restrictions
generated:
  by: process:build_okf
  at: 2026-10-23T07:58:54Z
status: stable
---

# Summary

Code samples for [Get Workspace Access Restrictions](../../../domains/organization-management/security-controls/get-workspace-access-restrictions.md) (`GET /restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/security-controls/workspaces/<workspace-id>/access-restrictions" \
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

        public void GetWorkspaceAccessRestrictions(IAnalyticsClient ac)
        {
            long workspaceId = 35130000001055707L;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = workspace.GetWorkspaceAccessRestrictions();
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.GetWorkspaceAccessRestrictions(ac);
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
)

func GetWorkspaceAccessRestrictions(ac ZAnalytics.Client) {
    workspaceid := "35130000001055707"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceid)
    result, exception := workspace.GetWorkspaceAccessRestrictions()
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetWorkspaceAccessRestrictions(ac)
}
```

## Java

```java
import com.zoho.analytics.client.*;
import org.json.*;

public class Test {
    private long orgId = 55522777l;

    public static void main(String args[]) {
        String clientId = "1000.xxxxxxx";
        String clientSecret = "xxxxxxx";
        String refreshToken = "1000.xxxxxxx.xxxxxxx";
        Test tObj = new Test();
        AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
        try {
            tObj.getWorkspaceAccessRestrictions(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void getWorkspaceAccessRestrictions(AnalyticsClient ac) throws Exception {
        long workspaceId = 35130000001055707l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getWorkspaceAccessRestrictions();
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

    function __construct() {
        $this->ac = new AnalyticsClient("1000.xxxxxxx", "xxxxxxx", "1000.xxxxxxx.xxxxxxx");
    }

    function getWorkspaceAccessRestrictions() {
        $workspace_id = "35130000001055707";
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $workspace_id);
        $response = $workspace->getWorkspaceAccessRestrictions();
        print_r($response);
    }
}

$obj = new Test();
$obj->getWorkspaceAccessRestrictions();
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

class Sample:
    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def get_workspace_access_restrictions(self, ac):
        workspace_id = "35130000001055707"
        workspace = ac.get_workspace_instance(Config.ORGID, workspace_id)
        result = workspace.get_workspace_access_restrictions()
        print(result)

obj = Sample()
obj.get_workspace_access_restrictions(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';

var workspaceId = "35130000001055707";
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.getWorkspaceAccessRestrictions().then((result) => { console.log(result); }).catch((error) => { console.log(error); });
```

## Ruby

```ruby
require 'zoho_analytics_client'

class Config
  ORGID = "55522777"
end

class Sample
  def initialize
    @ac = AnalyticsClient.new.with_data_center("US").with_oauth({
      "clientId" => "1000.xxxxxxx",
      "clientSecret" => "xxxxxxx",
      "refreshToken" => "1000.xxxxxxx.xxxxxxx"
    }).build
  end

  def get_workspace_access_restrictions
    workspace_id = "35130000001055707"
    workspace = @ac.get_workspace_instance(Config::ORGID, workspace_id)
    result = workspace.get_workspace_access_restrictions
    puts result
  end
end

obj = Sample.new
obj.get_workspace_access_restrictions
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/security-controls/workspaces/" + workspaceId + "/access-restrictions"
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Workspace Access Restrictions](../../../domains/organization-management/security-controls/get-workspace-access-restrictions.md) - full endpoint reference.
- [Security Controls overview](../../../domains/organization-management/security-controls/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
