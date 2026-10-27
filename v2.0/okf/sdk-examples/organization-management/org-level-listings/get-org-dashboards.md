---
type: SDK Example
title: SDK examples - Get Org Dashboards
description: Code samples in 9 languages for GET /restapi/v2/orgs/dashboards (getOrgDashboards).
resource: https://analyticsapi.zoho.com/restapi/v2/orgs/dashboards
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - organization-management
  - org-level-listings
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
  operation_id: getOrgDashboards
  method: GET
  path: "/restapi/v2/orgs/dashboards"
  endpoint_doc: "/domains/organization-management/org-level-listings/get-org-dashboards.md"
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
    last_modified: 2026-10-26T10:58:51Z
  - id: endpoint-doc
    resource: "/domains/organization-management/org-level-listings/get-org-dashboards.md"
    title: Endpoint reference - Get Org Dashboards
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

Code samples for [Get Org Dashboards](../../../domains/organization-management/org-level-listings/get-org-dashboards.md) (`GET /restapi/v2/orgs/dashboards`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/orgs/dashboards?CONFIG=%7B%22recordsPerPage%22%3A50%2C%22searchKey%22%3A%22Sales%22%7D" \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>'
```

## C#

```csharp
using System;
using System.Collections.Generic;
using ZohoAnalytics;
using System.Text.Json;

namespace ZohoAnalyticsTest
{
    class Program
    {
        long orgId = 55522777;

        public void GetOrgDashboards(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("recordsPerPage", 50);
            config.Add("searchKey", "Sales");
            JsonElement result = org.GetOrgDashboards(config);
            Console.WriteLine(result);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";

            try
            {
                IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
                Program obj = new Program();
                obj.GetOrgDashboards(ac);
            }
            catch (ServerException ex)
            {
                Console.WriteLine("Server exception - " + ex.GetErrorMessage());
            }
            catch (Exception ex)
            {
                Console.WriteLine("Other exception - " + ex.Message);
            }
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

var(
    clientId = "1000.xxxxxxx"
    clientSecret = "xxxxxxx"
    refreshToken = "1000.xxxxxxx.xxxxxxx"

    orgId = "55522777"
)

func GetOrgDashboards(ac ZAnalytics.Client) {
    org := ZAnalytics.GetOrgInstance(&ac, orgId)
    config := map[string]interface{}{"recordsPerPage": 50, "searchKey": "Sales"}
    result, _ := org.GetOrgDashboards(config)
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetOrgDashboards(ac)
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
            tObj.getOrgDashboards(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void getOrgDashboards(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONObject config = new JSONObject();
        config.put("recordsPerPage", 50);
        config.put("searchKey", "Sales");
        JSONObject result = org.getOrgDashboards(config);
        System.out.println(result);
    }
}
```

## PHP

```php
<?php

    require 'AnalyticsClient.php';

    class Test
    {
        public $ac = NULL;
        public $client_id = "1000.xxxxxxx";
        public $client_secret = "xxxxxxx";
        public $refresh_token = "1000.xxxxxxx.xxxxxxx";

        public $org_id = "55522777";

        function __construct() {
            $this->ac = new AnalyticsClient($this->client_id, $this->client_secret, $this->refresh_token);
        }

        function getOrgDashboards() {
            $org = $this->ac->getOrgInstance($this->org_id);
            $config = array("recordsPerPage" => 50, "searchKey" => "Sales");
            $response = $org->getOrgDashboards($config);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->getOrgDashboards();
    }
    catch(ServerException $se) {
        echo "Server exception : " . $se->getErrorMessage() . "\n";
    }
    catch(Exception $e) {
        echo "Exception : " . $e->getMessage() . "\n";
    }
?>
```

## Python

```python
from AnalyticsClient import AnalyticsClient
import sys

class Config:
    CLIENTID = "1000.xxxxxxx"
    CLIENTSECRET = "xxxxxxx"
    REFRESHTOKEN = "1000.xxxxxxx.xxxxxxx"
    ORGID = "55522777"

class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def get_org_dashboards(self, ac):
        org = ac.get_org_instance(Config.ORGID)
        config = {"recordsPerPage": 50, "searchKey": "Sales"}
        result = org.get_org_dashboards(config)
        print(result)

try:
    obj = sample()
    obj.get_org_dashboards(obj.ac)
except Exception as e:
    print(str(e))
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');

var clientId = '1000.xxxxxxx';
var clientSecret = 'xxxxxxx';
var refreshToken = '1000.xxxxxxx.xxxxxxx';
var orgId = '55522777';

var ac = new analyticsClient(clientId, clientSecret, refreshToken);

var org = ac.getOrgInstance(orgId);
var config = {recordsPerPage: 50, searchKey: 'Sales'};

org.getOrgDashboards(config).then(function (result) {
    console.log(result);
}).catch(function (err) {
    console.log(err);
});
```

## Ruby

```ruby
require 'zoho_analytics_client'

class Config
  ORGID = "55522777"
end

class Sample
  def initialize
    @ac = AnalyticsClient.new
           .with_data_center("US")
           .with_oauth({
             "clientId" => "1000.xxxxxxx",
             "clientSecret" => "xxxxxxx",
             "refreshToken" => "1000.xxxxxxx.xxxxxxx"
           })
           .build
  end

  def get_org_dashboards
    org = @ac.get_org_instance(Config::ORGID)
    config = {"recordsPerPage" => 50, "searchKey" => "Sales"}
    result = org.get_org_dashboards(config)
    puts result
  end
end

begin
  obj = Sample.new
  obj.get_org_dashboards
rescue ServerError => e
  puts "Server Error: #{e.response_content}"
rescue StandardError => e
  puts e.message
  puts e.backtrace.join("\n")
end
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("recordsPerPage", 50);
config.put("searchKey", "Sales");
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/orgs/dashboards?CONFIG=" + zoho.encryption.urlEncode(config.toString())
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Org Dashboards](../../../domains/organization-management/org-level-listings/get-org-dashboards.md) - full endpoint reference.
- [Org-Level Listings overview](../../../domains/organization-management/org-level-listings/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
