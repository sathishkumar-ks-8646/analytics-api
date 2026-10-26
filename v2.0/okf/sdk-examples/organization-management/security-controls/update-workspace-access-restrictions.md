---
type: SDK Example
title: SDK examples - Update Workspace Access Restrictions
description: "Code samples in 9 languages for PUT /restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions (updateWorkspaceAccessRestrictions)."
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
  operation_id: updateWorkspaceAccessRestrictions
  method: PUT
  path: "/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions"
  endpoint_doc: "/domains/organization-management/security-controls/update-workspace-access-restrictions.md"
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
    resource: "/domains/organization-management/security-controls/update-workspace-access-restrictions.md"
    title: Endpoint reference - Update Workspace Access Restrictions
generated:
  by: process:build_okf
  at: 2026-10-23T07:58:54Z
status: stable
---

# Summary

Code samples for [Update Workspace Access Restrictions](../../../domains/organization-management/security-controls/update-workspace-access-restrictions.md) (`PUT /restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/security-controls/workspaces/<workspace-id>/access-restrictions" \
  -X 'PUT' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"useOrganizationSettings":false,"shareViews":{"domainRestrictionEnabled":true,"trustedDomains":["example.com","partner.example.org"]},"privateLinks":{"enabled":false},"publicViews":{"enabled":false},"exportViews":{"enabled":true},"emailViews":{"enabled":true,"domainRestrictionEnabled":true,"trustedDomains":["example.com"]}}'
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

        public void UpdateWorkspaceAccessRestrictions(IAnalyticsClient ac)
        {
            long workspaceId = 35130000001055707L;
            Dictionary<string, object> config = JsonSerializer.Deserialize<Dictionary<string, object>>("{\"useOrganizationSettings\":false,\"shareViews\":{\"domainRestrictionEnabled\":true,\"trustedDomains\":[\"example.com\",\"partner.example.org\"]},\"privateLinks\":{\"enabled\":false},\"publicViews\":{\"enabled\":false},\"exportViews\":{\"enabled\":true},\"emailViews\":{\"enabled\":true,\"domainRestrictionEnabled\":true,\"trustedDomains\":[\"example.com\"]}}");
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.UpdateWorkspaceAccessRestrictions(config);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.UpdateWorkspaceAccessRestrictions(ac);
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

func UpdateWorkspaceAccessRestrictions(ac ZAnalytics.Client) {
    workspaceid := "35130000001055707"
    config := map[string]interface{}{
        "useOrganizationSettings": false,
        "shareViews": map[string]interface{}{
            "domainRestrictionEnabled": true,
            "trustedDomains": []string{"example.com", "partner.example.org"},
        },
        "privateLinks": map[string]interface{}{
            "enabled": false,
        },
        "publicViews": map[string]interface{}{
            "enabled": false,
        },
        "exportViews": map[string]interface{}{
            "enabled": true,
        },
        "emailViews": map[string]interface{}{
            "enabled": true,
            "domainRestrictionEnabled": true,
            "trustedDomains": []string{"example.com"},
        },
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceid)
    exception := workspace.UpdateWorkspaceAccessRestrictions(config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    UpdateWorkspaceAccessRestrictions(ac)
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
            tObj.updateWorkspaceAccessRestrictions(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void updateWorkspaceAccessRestrictions(AnalyticsClient ac) throws Exception {
        long workspaceId = 35130000001055707l;
        JSONObject config = new JSONObject("{\"useOrganizationSettings\":false,\"shareViews\":{\"domainRestrictionEnabled\":true,\"trustedDomains\":[\"example.com\",\"partner.example.org\"]},\"privateLinks\":{\"enabled\":false},\"publicViews\":{\"enabled\":false},\"exportViews\":{\"enabled\":true},\"emailViews\":{\"enabled\":true,\"domainRestrictionEnabled\":true,\"trustedDomains\":[\"example.com\"]}}");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.updateWorkspaceAccessRestrictions(config);
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

    function __construct() {
        $this->ac = new AnalyticsClient("1000.xxxxxxx", "xxxxxxx", "1000.xxxxxxx.xxxxxxx");
    }

    function updateWorkspaceAccessRestrictions() {
        $workspace_id = "35130000001055707";
        $config = array(
            "useOrganizationSettings" => false,
            "shareViews" => array(
                "domainRestrictionEnabled" => true,
                "trustedDomains" => array("example.com", "partner.example.org")
            ),
            "privateLinks" => array(
                "enabled" => false
            ),
            "publicViews" => array(
                "enabled" => false
            ),
            "exportViews" => array(
                "enabled" => true
            ),
            "emailViews" => array(
                "enabled" => true,
                "domainRestrictionEnabled" => true,
                "trustedDomains" => array("example.com")
            )
        );
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $workspace_id);
        $workspace->updateWorkspaceAccessRestrictions($config);
        echo "success";
    }
}

$obj = new Test();
$obj->updateWorkspaceAccessRestrictions();
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

    def update_workspace_access_restrictions(self, ac):
        workspace_id = "35130000001055707"
        config = {
            "useOrganizationSettings": False,
            "shareViews": {
                "domainRestrictionEnabled": True,
                "trustedDomains": ["example.com", "partner.example.org"]
            },
            "privateLinks": {
                "enabled": False
            },
            "publicViews": {
                "enabled": False
            },
            "exportViews": {
                "enabled": True
            },
            "emailViews": {
                "enabled": True,
                "domainRestrictionEnabled": True,
                "trustedDomains": ["example.com"]
            }
        }
        workspace = ac.get_workspace_instance(Config.ORGID, workspace_id)
        workspace.update_workspace_access_restrictions(config)
        print("success")

obj = Sample()
obj.update_workspace_access_restrictions(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';

var workspaceId = "35130000001055707";
var config = {
    "useOrganizationSettings": false,
    "shareViews": {
        "domainRestrictionEnabled": true,
        "trustedDomains": ["example.com", "partner.example.org"]
    },
    "privateLinks": {
        "enabled": false
    },
    "publicViews": {
        "enabled": false
    },
    "exportViews": {
        "enabled": true
    },
    "emailViews": {
        "enabled": true,
        "domainRestrictionEnabled": true,
        "trustedDomains": ["example.com"]
    }
};
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.updateWorkspaceAccessRestrictions(config).then(() => { console.log("success"); }).catch((error) => { console.log(error); });
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

  def update_workspace_access_restrictions
    workspace_id = "35130000001055707"
    config = {
      "useOrganizationSettings" => false,
      "shareViews" => {
        "domainRestrictionEnabled" => true,
        "trustedDomains" => ["example.com", "partner.example.org"]
      },
      "privateLinks" => {
        "enabled" => false
      },
      "publicViews" => {
        "enabled" => false
      },
      "exportViews" => {
        "enabled" => true
      },
      "emailViews" => {
        "enabled" => true,
        "domainRestrictionEnabled" => true,
        "trustedDomains" => ["example.com"]
      }
    }
    workspace = @ac.get_workspace_instance(Config::ORGID, workspace_id)
    workspace.update_workspace_access_restrictions(config)
    puts "success"
  end
end

obj = Sample.new
obj.update_workspace_access_restrictions
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"useOrganizationSettings": false, "shareViews": {"domainRestrictionEnabled": true, "trustedDomains": ["example.com", "partner.example.org"]}, "privateLinks": {"enabled": false}, "publicViews": {"enabled": false}, "exportViews": {"enabled": true}, "emailViews": {"enabled": true, "domainRestrictionEnabled": true, "trustedDomains": ["example.com"]}};
response = invokeurl
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
[
  url :"https://analyticsapi.zoho.com/restapi/v2/security-controls/workspaces/" + workspaceId + "/access-restrictions"
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Update Workspace Access Restrictions](../../../domains/organization-management/security-controls/update-workspace-access-restrictions.md) - full endpoint reference.
- [Security Controls overview](../../../domains/organization-management/security-controls/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
