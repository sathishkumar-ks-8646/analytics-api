---
type: SDK Example
title: SDK examples - Get Owned Dashboards
description: Code samples in 9 languages for GET /restapi/v2/dashboards/owned (getOwnedDashboards).
resource: https://analyticsapi.zoho.com/restapi/v2/dashboards/owned
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - reports-and-dashboards
  - dashboards
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
  operation_id: getOwnedDashboards
  method: GET
  path: "/restapi/v2/dashboards/owned"
  endpoint_doc: "/domains/reports-and-dashboards/dashboards/get-owned-dashboards.md"
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
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
  - id: endpoint-doc
    resource: "/domains/reports-and-dashboards/dashboards/get-owned-dashboards.md"
    title: Endpoint reference - Get Owned Dashboards
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Get Owned Dashboards](../../../domains/reports-and-dashboards/dashboards/get-owned-dashboards.md) (`GET /restapi/v2/dashboards/owned`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/dashboards/owned" -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
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

        public void GetOwnedDashboards(IAnalyticsClient ac)
        {
            JsonElement result = ac.GetOwnedDashboards();
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.GetOwnedDashboards(ac);
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

func GetOwnedDashboards(ac ZAnalytics.Client) {
    result, exception := ac.GetOwnedDashboards()
    if exception != nil { fmt.Println(exception.ErrorMessage); return }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetOwnedDashboards(ac)
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
            tObj.getOwnedDashboards(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void getOwnedDashboards(AnalyticsClient ac) throws Exception {
        JSONArray result = ac.getOwnedDashboards();
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

    function getOwnedDashboards() {
        $response = $this->ac->getOwnedDashboards();
        print_r($response);
    }
}

$obj = new Test();
$obj->getOwnedDashboards();
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

class sample:
    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def get_owned_dashboards(self, ac):
        result = ac.get_owned_dashboards()
        print(result)

obj = sample()
obj.get_owned_dashboards(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
ac.getOwnedDashboards().then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def get_owned_dashboards
    result = @ac.get_owned_dashboards
    puts result
  end
end

obj = Sample.new
obj.get_owned_dashboards
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/dashboards/owned"
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Owned Dashboards](../../../domains/reports-and-dashboards/dashboards/get-owned-dashboards.md) - full endpoint reference.
- [Dashboards overview](../../../domains/reports-and-dashboards/dashboards/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
