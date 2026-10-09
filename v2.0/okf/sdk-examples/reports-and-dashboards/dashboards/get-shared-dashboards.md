---
type: SDK Example
title: SDK examples - Get Shared Dashboards
description: Code samples in 9 languages for GET /restapi/v2/dashboards/shared (getSharedDashboards).
resource: https://analyticsapi.zoho.com/restapi/v2/dashboards/shared
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
  operation_id: getSharedDashboards
  method: GET
  path: "/restapi/v2/dashboards/shared"
  endpoint_doc: "/domains/reports-and-dashboards/dashboards/get-shared-dashboards.md"
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
    resource: "/domains/reports-and-dashboards/dashboards/get-shared-dashboards.md"
    title: Endpoint reference - Get Shared Dashboards
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Get Shared Dashboards](../../../domains/reports-and-dashboards/dashboards/get-shared-dashboards.md) (`GET /restapi/v2/dashboards/shared`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/dashboards/shared" -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
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

        public void GetSharedDashboards(IAnalyticsClient ac)
        {
            JsonElement result = ac.GetSharedDashboards();
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.GetSharedDashboards(ac);
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

func GetSharedDashboards(ac ZAnalytics.Client) {
    result, exception := ac.GetSharedDashboards()
    if exception != nil { fmt.Println(exception.ErrorMessage); return }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetSharedDashboards(ac)
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
            tObj.getSharedDashboards(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void getSharedDashboards(AnalyticsClient ac) throws Exception {
        JSONArray result = ac.getSharedDashboards();
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

    function getSharedDashboards() {
        $response = $this->ac->getSharedDashboards();
        print_r($response);
    }
}

$obj = new Test();
$obj->getSharedDashboards();
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

    def get_shared_dashboards(self, ac):
        result = ac.get_shared_dashboards()
        print(result)

obj = sample()
obj.get_shared_dashboards(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
ac.getSharedDashboards().then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def get_shared_dashboards
    result = @ac.get_shared_dashboards
    puts result
  end
end

obj = Sample.new
obj.get_shared_dashboards
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/dashboards/shared"
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Shared Dashboards](../../../domains/reports-and-dashboards/dashboards/get-shared-dashboards.md) - full endpoint reference.
- [Dashboards overview](../../../domains/reports-and-dashboards/dashboards/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
