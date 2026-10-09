---
type: SDK Example
title: SDK examples - Get View Details
description: "Code samples in 9 languages for GET /restapi/v2/views/{view-id} (getViewDetails)."
resource: "https://analyticsapi.zoho.com/restapi/v2/views/{view-id}"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - views-management
  - view-operations
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
  operation_id: getViewDetails
  method: GET
  path: "/restapi/v2/views/{view-id}"
  endpoint_doc: "/domains/views-management/view-operations/get-view-details.md"
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
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
  - id: endpoint-doc
    resource: "/domains/views-management/view-operations/get-view-details.md"
    title: Endpoint reference - Get View Details
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Get View Details](../../../domains/views-management/view-operations/get-view-details.md) (`GET /restapi/v2/views/{view-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/views/35130000001055717?CONFIG=%7B%22withInvolvedMetaInfo%22%3Atrue%7D" -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
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
        long viewId = 35130000001055717;

        public void GetViewDetails(IAnalyticsClient ac)
        {
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("withInvolvedMetaInfo", true);
            JsonElement views = ac.GetViewDetails(viewId, config);
            Console.WriteLine(views);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.GetViewDetails(ac);
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
    viewId = "35130000001055717"
)

func GetViewDetails(ac ZAnalytics.Client) {
    config := map[string]interface{}{}
    result, exception := ac.GetViewDetails(viewId, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetViewDetails(ac)
}
```

## Java

```java
import com.zoho.analytics.client.*;
import org.json.*;

public class Test {
    private long viewId = 35130000001055717l;

    public static void main(String args[]) {
        String clientId = "1000.xxxxxxx";
        String clientSecret = "xxxxxxx";
        String refreshToken = "1000.xxxxxxx.xxxxxxx";
        Test tObj = new Test();
        AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
        try {
            tObj.getViewDetails(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void getViewDetails(AnalyticsClient ac) throws Exception {
        JSONObject config = new JSONObject();
        config.put("withInvolvedMetaInfo", true);
        JSONObject result = ac.getViewDetails(viewId, config);
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
    public $view_id = "35130000001055717";

    function __construct() {
        $this->ac = new AnalyticsClient("1000.xxxxxxx", "xxxxxxx", "1000.xxxxxxx.xxxxxxx");
    }

    function getViewDetails() {
        $config = array("withInvolvedMetaInfo" => true);
        $response = $this->ac->getViewDetails($this->view_id, $config);
        print_r($response);
    }
}

$obj = new Test();
$obj->getViewDetails();
?>
```

## Python

```python
from AnalyticsClient import AnalyticsClient

class Config:
    CLIENTID = "1000.xxxxxxx"
    CLIENTSECRET = "xxxxxxx"
    REFRESHTOKEN = "1000.xxxxxxx.xxxxxxx"
    VIEWID = "35130000001055717"

class Sample:
    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def get_view_details(self, ac):
        config = {"withInvolvedMetaInfo": True}
        result = ac.get_view_details(Config.VIEWID, config)
        print(result)

obj = Sample()
obj.get_view_details(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var viewId = '35130000001055717';
var config = {withInvolvedMetaInfo: true};

ac.getViewDetails(viewId, config).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
```

## Ruby

```ruby
require 'zoho_analytics_client'

class Config
  VIEWID = "35130000001055717"
end

class Sample
  def initialize
    @ac = AnalyticsClient.new.with_data_center("US").with_oauth({
      "clientId" => "1000.xxxxxxx",
      "clientSecret" => "xxxxxxx",
      "refreshToken" => "1000.xxxxxxx.xxxxxxx"
    }).build
  end

  def get_view_details
    config = {"withInvolvedMetaInfo" => true}
    result = @ac.get_view_details(Config::VIEWID, config)
    puts result
  end
end

obj = Sample.new
obj.get_view_details
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
viewId = "35130000001055717";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("withInvolvedMetaInfo", true);
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/views/" + viewId + "?CONFIG=" + zoho.encryption.urlEncode(config.toString())
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get View Details](../../../domains/views-management/view-operations/get-view-details.md) - full endpoint reference.
- [View Operations overview](../../../domains/views-management/view-operations/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
