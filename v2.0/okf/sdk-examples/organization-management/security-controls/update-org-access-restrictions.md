---
type: SDK Example
title: SDK examples - Update Org Access Restrictions
description: Code samples in 9 languages for PUT /restapi/v2/security-controls/access-restrictions (updateOrgAccessRestrictions).
resource: https://analyticsapi.zoho.com/restapi/v2/security-controls/access-restrictions
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
  operation_id: updateOrgAccessRestrictions
  method: PUT
  path: "/restapi/v2/security-controls/access-restrictions"
  endpoint_doc: "/domains/organization-management/security-controls/update-org-access-restrictions.md"
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
    resource: "/domains/organization-management/security-controls/update-org-access-restrictions.md"
    title: Endpoint reference - Update Org Access Restrictions
generated:
  by: process:build_okf
  at: 2026-10-23T07:58:54Z
status: stable
---

# Summary

Code samples for [Update Org Access Restrictions](../../../domains/organization-management/security-controls/update-org-access-restrictions.md) (`PUT /restapi/v2/security-controls/access-restrictions`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/security-controls/access-restrictions" \
  -X 'PUT' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"accessRestrictionEnabled":true}'
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

        public void UpdateOrgAccessRestrictions(IAnalyticsClient ac)
        {
            Dictionary<string, object> config = JsonSerializer.Deserialize<Dictionary<string, object>>("{\"accessRestrictionEnabled\":true}");
            IOrgAPI org = ac.GetOrgInstance(orgId);
            org.UpdateOrgAccessRestrictions(config);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.UpdateOrgAccessRestrictions(ac);
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

func UpdateOrgAccessRestrictions(ac ZAnalytics.Client) {
    config := map[string]interface{}{
        "accessRestrictionEnabled": true,
    }
    org := ZAnalytics.GetOrgInstance(&ac, orgId)
    exception := org.UpdateOrgAccessRestrictions(config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    UpdateOrgAccessRestrictions(ac)
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
            tObj.updateOrgAccessRestrictions(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void updateOrgAccessRestrictions(AnalyticsClient ac) throws Exception {
        JSONObject config = new JSONObject("{\"accessRestrictionEnabled\":true}");
        OrgAPI org = ac.getOrgInstance(orgId);
        org.updateOrgAccessRestrictions(config);
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

    function updateOrgAccessRestrictions() {
        $config = array(
            "accessRestrictionEnabled" => true
        );
        $org = $this->ac->getOrgInstance($this->org_id);
        $org->updateOrgAccessRestrictions($config);
        echo "success";
    }
}

$obj = new Test();
$obj->updateOrgAccessRestrictions();
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

    def update_org_access_restrictions(self, ac):
        config = {
            "accessRestrictionEnabled": True
        }
        org = ac.get_org_instance(Config.ORGID)
        org.update_org_access_restrictions(config)
        print("success")

obj = Sample()
obj.update_org_access_restrictions(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';

var config = {
    "accessRestrictionEnabled": true
};
var org = ac.getOrgInstance(orgId);
org.updateOrgAccessRestrictions(config).then(() => { console.log("success"); }).catch((error) => { console.log(error); });
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

  def update_org_access_restrictions
    config = {
      "accessRestrictionEnabled" => true
    }
    org = @ac.get_org_instance(Config::ORGID)
    org.update_org_access_restrictions(config)
    puts "success"
  end
end

obj = Sample.new
obj.update_org_access_restrictions
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"accessRestrictionEnabled": true};
response = invokeurl
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
[
  url :"https://analyticsapi.zoho.com/restapi/v2/security-controls/access-restrictions"
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Update Org Access Restrictions](../../../domains/organization-management/security-controls/update-org-access-restrictions.md) - full endpoint reference.
- [Security Controls overview](../../../domains/organization-management/security-controls/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
