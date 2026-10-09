---
type: SDK Example
title: SDK examples - Remove Users
description: Code samples in 9 languages for DELETE /restapi/v2/users (removeUsers).
resource: https://analyticsapi.zoho.com/restapi/v2/users
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - users-and-groups
  - org-users
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
  operation_id: removeUsers
  method: DELETE
  path: "/restapi/v2/users"
  endpoint_doc: "/domains/users-and-groups/org-users/remove-users.md"
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
    resource: "/references/openapi/user-groups-grouped-api.json"
    title: OpenAPI 3 specification - user-groups-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
  - id: endpoint-doc
    resource: "/domains/users-and-groups/org-users/remove-users.md"
    title: Endpoint reference - Remove Users
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Remove Users](../../../domains/users-and-groups/org-users/remove-users.md) (`DELETE /restapi/v2/users`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/users" \
  -X 'DELETE' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"emailIds":["user@example.com"]}'
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

        public void RemoveUsers(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            List<string> emailIds = new List<string>();
            emailIds.Add("user@example.com");
            org.RemoveUsers(emailIds, null);
            Console.WriteLine("success");
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
                obj.RemoveUsers(ac);
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

func RemoveUsers(ac ZAnalytics.Client) {
    org := ZAnalytics.GetOrgInstance(&ac, orgId)
    emailIds := []string{"user@example.com"}
    err := org.RemoveUsers(emailIds, nil)
    if err != nil {
        fmt.Println(err)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    RemoveUsers(ac)
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
            tObj.removeUsers(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void removeUsers(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("user@example.com");
        org.removeUsers(emailIds, null);
        System.out.println("success");
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

        function removeUsers() {
            $email_ids = array("user@example.com");
            $org = $this->ac->getOrgInstance($this->org_id);
            $org->removeUsers($email_ids);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->removeUsers();
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

    def remove_users(self, ac):
        email_ids = ["user@example.com"]
        org = ac.get_org_instance(Config.ORGID)
        org.remove_users(email_ids)
        print("success")

try:
    obj = sample()
    obj.remove_users(obj.ac)
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
var emailIds = ["user@example.com"];

org.removeUsers(emailIds).then(function () {
    console.log('success');
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

  def remove_users
    email_ids = ["user@example.com"]
    org = @ac.get_org_instance(Config::ORGID)
    org.remove_users(email_ids)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.remove_users
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
config = {"emailIds":["user@example.com"]};
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/users"
  type :DELETE
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Remove Users](../../../domains/users-and-groups/org-users/remove-users.md) - full endpoint reference.
- [Organization Users overview](../../../domains/users-and-groups/org-users/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
