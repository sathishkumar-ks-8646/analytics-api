---
type: SDK Example
title: SDK examples - Get Linked Workspaces For Organization
description: Code samples in 9 languages for GET /restapi/v2/linkedworkspaces (getLinkedWorkspacesForOrganization).
resource: https://analyticsapi.zoho.com/restapi/v2/linkedworkspaces
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
  operation_id: getLinkedWorkspacesForOrganization
  method: GET
  path: "/restapi/v2/linkedworkspaces"
  endpoint_doc: "/domains/workspace-management/linked-workspaces/get-linked-workspaces-for-organization.md"
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
    resource: "/domains/workspace-management/linked-workspaces/get-linked-workspaces-for-organization.md"
    title: Endpoint reference - Get Linked Workspaces For Organization
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

Code samples for [Get Linked Workspaces For Organization](../../../domains/workspace-management/linked-workspaces/get-linked-workspaces-for-organization.md) (`GET /restapi/v2/linkedworkspaces`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/linkedworkspaces" \
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

        public void GetLinkedWorkspaces(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            JsonElement result = org.GetLinkedWorkspaces();
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.GetLinkedWorkspaces(ac);
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

func GetLinkedWorkspaces(ac ZAnalytics.Client) {
    org := ZAnalytics.GetOrgInstance(&ac, orgId)
    result, exception := org.GetLinkedWorkspaces()
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetLinkedWorkspaces(ac)
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
            tObj.getLinkedWorkspaces(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void getLinkedWorkspaces(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONArray result = org.getLinkedWorkspaces();
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

    function getLinkedWorkspaces() {
        $org = $this->ac->getOrgInstance($this->org_id);
        $response = $org->getLinkedWorkspaces();
        print_r($response);
    }
}

$obj = new Test();
$obj->getLinkedWorkspaces();
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

    def get_linked_workspaces(self, ac):
        org = ac.get_org_instance(Config.ORGID)
        result = org.get_linked_workspaces()
        print(result)

obj = Sample()
obj.get_linked_workspaces(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';

var org = ac.getOrgInstance(orgId);
org.getLinkedWorkspaces().then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def get_linked_workspaces
    org = @ac.get_org_instance(Config::ORGID)
    result = org.get_linked_workspaces
    puts result
  end
end

obj = Sample.new
obj.get_linked_workspaces
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/linkedworkspaces"
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Linked Workspaces For Organization](../../../domains/workspace-management/linked-workspaces/get-linked-workspaces-for-organization.md) - full endpoint reference.
- [Linked Workspaces overview](../../../domains/workspace-management/linked-workspaces/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
