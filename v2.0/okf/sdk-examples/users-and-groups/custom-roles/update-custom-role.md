---
type: SDK Example
title: SDK examples - Update Custom Role
description: "Code samples in 9 languages for PUT /restapi/v2/orgs/roles/{role-id} (updateCustomRole)."
resource: "https://analyticsapi.zoho.com/restapi/v2/orgs/roles/{role-id}"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - users-and-groups
  - custom-roles
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
  operation_id: updateCustomRole
  method: PUT
  path: "/restapi/v2/orgs/roles/{role-id}"
  endpoint_doc: "/domains/users-and-groups/custom-roles/update-custom-role.md"
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
    resource: "/domains/users-and-groups/custom-roles/update-custom-role.md"
    title: Endpoint reference - Update Custom Role
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

Code samples for [Update Custom Role](../../../domains/users-and-groups/custom-roles/update-custom-role.md) (`PUT /restapi/v2/orgs/roles/{role-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

Variant 1:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/orgs/roles/<role-id>" \
  -X 'PUT' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"roleName":"Report Analyst EMEA"}'
```

Variant 2:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/orgs/roles/<role-id>" \
  -X 'PUT' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"accessType":"ALL_REPORTS_AND_DASHBOARDS","permissions":{"interactionPermissions":{"read":true,"vud":true,"drillDown":true,"insight":true},"sharePermissions":{"share":true,"discussion":true},"publishPermissions":{"export":true,"manageDataAlerts":true},"createPermissions":{"createFolder":true}}}'
```

## C#

Variant 1:

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

        public void UpdateCustomRole(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            long roleId = 35130000012043001;
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("roleName", "Report Analyst EMEA");
            org.UpdateCustomRole(roleId, config);
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
                obj.UpdateCustomRole(ac);
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

Variant 2:

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

        public void UpdateCustomRole(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            long roleId = 35130000012043001;
            Dictionary<string, object> permissions = new Dictionary<string, object>();
            Dictionary<string, object> interactionPermissions = new Dictionary<string, object>();
            interactionPermissions.Add("read", true);
            interactionPermissions.Add("vud", true);
            interactionPermissions.Add("drillDown", true);
            interactionPermissions.Add("insight", true);
            permissions.Add("interactionPermissions", interactionPermissions);
            Dictionary<string, object> sharePermissions = new Dictionary<string, object>();
            sharePermissions.Add("share", true);
            sharePermissions.Add("discussion", true);
            permissions.Add("sharePermissions", sharePermissions);
            Dictionary<string, object> publishPermissions = new Dictionary<string, object>();
            publishPermissions.Add("export", true);
            publishPermissions.Add("manageDataAlerts", true);
            permissions.Add("publishPermissions", publishPermissions);
            Dictionary<string, object> createPermissions = new Dictionary<string, object>();
            createPermissions.Add("createFolder", true);
            permissions.Add("createPermissions", createPermissions);
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("accessType", "ALL_REPORTS_AND_DASHBOARDS");
            config.Add("permissions", permissions);
            org.UpdateCustomRole(roleId, config);
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
                obj.UpdateCustomRole(ac);
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

Variant 1:

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

func UpdateCustomRole(ac ZAnalytics.Client) {
    org := ZAnalytics.GetOrgInstance(&ac, orgId)
    roleId := "35130000012043001"
    config := map[string]interface{}{"roleName": "Report Analyst EMEA"}
    err := org.UpdateCustomRole(roleId, config)
    if err != nil {
        fmt.Println(err)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    UpdateCustomRole(ac)
}
```

Variant 2:

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

func UpdateCustomRole(ac ZAnalytics.Client) {
    org := ZAnalytics.GetOrgInstance(&ac, orgId)
    roleId := "35130000012043001"
    permissions := map[string]interface{}{
        "interactionPermissions": map[string]interface{}{"read": true, "vud": true, "drillDown": true, "insight": true},
        "sharePermissions": map[string]interface{}{"share": true, "discussion": true},
        "publishPermissions": map[string]interface{}{"export": true, "manageDataAlerts": true},
        "createPermissions": map[string]interface{}{"createFolder": true},
    }
    config := map[string]interface{}{"accessType": "ALL_REPORTS_AND_DASHBOARDS", "permissions": permissions}
    err := org.UpdateCustomRole(roleId, config)
    if err != nil {
        fmt.Println(err)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    UpdateCustomRole(ac)
}
```

## Java

Variant 1:

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
            tObj.updateCustomRole(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void updateCustomRole(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        long roleId = 35130000012043001l;
        JSONObject config = new JSONObject();
        config.put("roleName", "Report Analyst EMEA");
        org.updateCustomRole(roleId, config);
        System.out.println("success");
    }
}
```

Variant 2:

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
            tObj.updateCustomRole(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void updateCustomRole(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        long roleId = 35130000012043001l;
        JSONObject permissions = new JSONObject();
        JSONObject interactionPermissions = new JSONObject();
        interactionPermissions.put("read", true);
        interactionPermissions.put("vud", true);
        interactionPermissions.put("drillDown", true);
        interactionPermissions.put("insight", true);
        permissions.put("interactionPermissions", interactionPermissions);
        JSONObject sharePermissions = new JSONObject();
        sharePermissions.put("share", true);
        sharePermissions.put("discussion", true);
        permissions.put("sharePermissions", sharePermissions);
        JSONObject publishPermissions = new JSONObject();
        publishPermissions.put("export", true);
        publishPermissions.put("manageDataAlerts", true);
        permissions.put("publishPermissions", publishPermissions);
        JSONObject createPermissions = new JSONObject();
        createPermissions.put("createFolder", true);
        permissions.put("createPermissions", createPermissions);
        JSONObject config = new JSONObject();
        config.put("accessType", "ALL_REPORTS_AND_DASHBOARDS");
        config.put("permissions", permissions);
        org.updateCustomRole(roleId, config);
        System.out.println("success");
    }
}
```

## PHP

Variant 1:

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

        function updateCustomRole() {
            $org = $this->ac->getOrgInstance($this->org_id);
            $role_id = "35130000012043001";
            $config = array("roleName" => "Report Analyst EMEA");
            $org->updateCustomRole($role_id, $config);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->updateCustomRole();
    }
    catch(ServerException $se) {
        echo "Server exception : " . $se->getErrorMessage() . "\n";
    }
    catch(Exception $e) {
        echo "Exception : " . $e->getMessage() . "\n";
    }
?>
```

Variant 2:

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

        function updateCustomRole() {
            $org = $this->ac->getOrgInstance($this->org_id);
            $role_id = "35130000012043001";
            $permissions = array(
                "interactionPermissions" => array("read" => true, "vud" => true, "drillDown" => true, "insight" => true),
                "sharePermissions" => array("share" => true, "discussion" => true),
                "publishPermissions" => array("export" => true, "manageDataAlerts" => true),
                "createPermissions" => array("createFolder" => true)
            );
            $config = array("accessType" => "ALL_REPORTS_AND_DASHBOARDS", "permissions" => $permissions);
            $org->updateCustomRole($role_id, $config);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->updateCustomRole();
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

Variant 1:

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

    def update_custom_role(self, ac):
        org = ac.get_org_instance(Config.ORGID)
        role_id = "35130000012043001"
        config = {"roleName": "Report Analyst EMEA"}
        org.update_custom_role(role_id, config)
        print("success")

try:
    obj = sample()
    obj.update_custom_role(obj.ac)
except Exception as e:
    print(str(e))
```

Variant 2:

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

    def update_custom_role(self, ac):
        org = ac.get_org_instance(Config.ORGID)
        role_id = "35130000012043001"
        permissions = {
            "interactionPermissions": {"read": True, "vud": True, "drillDown": True, "insight": True},
            "sharePermissions": {"share": True, "discussion": True},
            "publishPermissions": {"export": True, "manageDataAlerts": True},
            "createPermissions": {"createFolder": True}
        }
        config = {"accessType": "ALL_REPORTS_AND_DASHBOARDS", "permissions": permissions}
        org.update_custom_role(role_id, config)
        print("success")

try:
    obj = sample()
    obj.update_custom_role(obj.ac)
except Exception as e:
    print(str(e))
```

## Node.js

Variant 1:

```javascript
var analyticsClient = require('./AnalyticsClient');

var clientId = '1000.xxxxxxx';
var clientSecret = 'xxxxxxx';
var refreshToken = '1000.xxxxxxx.xxxxxxx';
var orgId = '55522777';

var ac = new analyticsClient(clientId, clientSecret, refreshToken);

var org = ac.getOrgInstance(orgId);
var roleId = '35130000012043001';
var config = {"roleName": "Report Analyst EMEA"};

org.updateCustomRole(roleId, config).then(function () {
    console.log('success');
}).catch(function (err) {
    console.log(err);
});
```

Variant 2:

```javascript
var analyticsClient = require('./AnalyticsClient');

var clientId = '1000.xxxxxxx';
var clientSecret = 'xxxxxxx';
var refreshToken = '1000.xxxxxxx.xxxxxxx';
var orgId = '55522777';

var ac = new analyticsClient(clientId, clientSecret, refreshToken);

var org = ac.getOrgInstance(orgId);
var roleId = '35130000012043001';
var permissions = {
    interactionPermissions: {read: true, vud: true, drillDown: true, insight: true},
    sharePermissions: {share: true, discussion: true},
    publishPermissions: {export: true, manageDataAlerts: true},
    createPermissions: {createFolder: true}
};
var config = {accessType: 'ALL_REPORTS_AND_DASHBOARDS', permissions: permissions};

org.updateCustomRole(roleId, config).then(function () {
    console.log('success');
}).catch(function (err) {
    console.log(err);
});
```

## Ruby

Variant 1:

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

  def update_custom_role
    org = @ac.get_org_instance(Config::ORGID)
    role_id = "35130000012043001"
    config = {"roleName" => "Report Analyst EMEA"}
    org.update_custom_role(role_id, config)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.update_custom_role
rescue ServerError => e
  puts "Server Error: #{e.response_content}"
rescue StandardError => e
  puts e.message
  puts e.backtrace.join("\n")
end
```

Variant 2:

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

  def update_custom_role
    org = @ac.get_org_instance(Config::ORGID)
    role_id = "35130000012043001"
    permissions = {
      "interactionPermissions" => {"read" => true, "vud" => true, "drillDown" => true, "insight" => true},
      "sharePermissions" => {"share" => true, "discussion" => true},
      "publishPermissions" => {"export" => true, "manageDataAlerts" => true},
      "createPermissions" => {"createFolder" => true}
    }
    config = {"accessType" => "ALL_REPORTS_AND_DASHBOARDS", "permissions" => permissions}
    org.update_custom_role(role_id, config)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.update_custom_role
rescue ServerError => e
  puts "Server Error: #{e.response_content}"
rescue StandardError => e
  puts e.message
  puts e.backtrace.join("\n")
end
```

## Deluge (Zoho scripting)

Variant 1:

```deluge
orgId = "55522777";
roleId = "35130000012043001";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"roleName":"Report Analyst EMEA"};
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/orgs/roles/" + roleId
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

Variant 2:

```deluge
orgId = "55522777";
roleId = "35130000012043001";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"accessType":"ALL_REPORTS_AND_DASHBOARDS","permissions":{"interactionPermissions":{"read":true,"vud":true,"drillDown":true,"insight":true},"sharePermissions":{"share":true,"discussion":true},"publishPermissions":{"export":true,"manageDataAlerts":true},"createPermissions":{"createFolder":true}}};
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/orgs/roles/" + roleId
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Update Custom Role](../../../domains/users-and-groups/custom-roles/update-custom-role.md) - full endpoint reference.
- [Custom Roles overview](../../../domains/users-and-groups/custom-roles/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
