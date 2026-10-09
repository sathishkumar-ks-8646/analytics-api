---
type: SDK Example
title: SDK examples - Get Org List
description: Code samples in 9 languages for GET /restapi/v2/orgs (getOrganizations).
resource: https://analyticsapi.zoho.com/restapi/v2/orgs
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - organization-management
  - org-info-and-settings
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
  operation_id: getOrganizations
  method: GET
  path: "/restapi/v2/orgs"
  endpoint_doc: "/domains/organization-management/org-info-and-settings/get-organizations.md"
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
    last_modified: 2026-10-09T13:04:25Z
  - id: endpoint-doc
    resource: "/domains/organization-management/org-info-and-settings/get-organizations.md"
    title: Endpoint reference - Get Org List
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Get Org List](../../../domains/organization-management/org-info-and-settings/get-organizations.md) (`GET /restapi/v2/orgs`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/orgs" \
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

        public void GetOrganizations(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            JsonElement result = org.GetOrganizations();
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
                obj.GetOrganizations(ac);
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

func GetOrganizations(ac ZAnalytics.Client) {
    org := ZAnalytics.GetOrgInstance(&ac, orgId)
    result, _ := org.GetOrganizations()
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetOrganizations(ac)
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
            tObj.getOrganizations(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void getOrganizations(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONArray result = org.getOrganizations();
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

        function getOrganizations() {
            $org = $this->ac->getOrgInstance($this->org_id);
            $response = $org->getOrganizations();
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->getOrganizations();
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

    def get_organizations(self, ac):
        org = ac.get_org_instance(Config.ORGID)
        result = org.get_organizations()
        print(result)

try:
    obj = sample()
    obj.get_organizations(obj.ac)
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

org.getOrganizations().then(function (result) {
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

  def get_organizations
    org = @ac.get_org_instance(Config::ORGID)
    result = org.get_organizations
    puts result
  end
end

begin
  obj = Sample.new
  obj.get_organizations
rescue ServerError => e
  puts "Server Error: #{e.response_content}"
rescue StandardError => e
  puts e.message
  puts e.backtrace.join("\n")
end
```

## Deluge (Zoho scripting)

```deluge
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/orgs"
  type :GET
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Org List](../../../domains/organization-management/org-info-and-settings/get-organizations.md) - full endpoint reference.
- [Organization Info & Settings overview](../../../domains/organization-management/org-info-and-settings/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
