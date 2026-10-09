---
type: SDK Example
title: SDK examples - Rename Group
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id}/groups/{group-id} (renameGroup)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/groups/{group-id}"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - users-and-groups
  - workspace-groups
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
  operation_id: renameGroup
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/groups/{group-id}"
  endpoint_doc: "/domains/users-and-groups/workspace-groups/rename-group.md"
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
    resource: "/domains/users-and-groups/workspace-groups/rename-group.md"
    title: Endpoint reference - Rename Group
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

Code samples for [Rename Group](../../../domains/users-and-groups/workspace-groups/rename-group.md) (`PUT /restapi/v2/workspaces/{workspace-id}/groups/{group-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

Variant 1:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/groups/<group-id>" \
  -X 'PUT' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"groupName":"Renamed Group"}'
```

Variant 2:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/groups/<group-id>" \
  -X 'PUT' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"groupName":"Finance & Accounts Team","groupDesc":"Finance, accounts payable, and treasury users"}'
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
        long workspaceId = 35130000001055707;

        public void RenameGroup(IAnalyticsClient ac)
        {
            long groupId = 35130000001364001;
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            string groupName = "Renamed Group";
            ws.RenameGroup(groupId, groupName, null);
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
                obj.RenameGroup(ac);
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
        long workspaceId = 35130000001055707;

        public void RenameGroup(IAnalyticsClient ac)
        {
            long groupId = 35130000001364001;
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            string groupName = "Finance & Accounts Team";
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("groupDesc", "Finance, accounts payable, and treasury users");
            ws.RenameGroup(groupId, groupName, config);
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
                obj.RenameGroup(ac);
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
    workspaceId = "35130000001055707"
)

func RenameGroup(ac ZAnalytics.Client) {
    groupId := "35130000001364001"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    groupName := "Renamed Group"
    err := workspace.RenameGroup(groupId, groupName, nil)
    if err != nil {
        fmt.Println(err)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    RenameGroup(ac)
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
    workspaceId = "35130000001055707"
)

func RenameGroup(ac ZAnalytics.Client) {
    groupId := "35130000001364001"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    groupName := "Finance & Accounts Team"
    config := map[string]interface{}{"groupDesc": "Finance, accounts payable, and treasury users"}
    err := workspace.RenameGroup(groupId, groupName, config)
    if err != nil {
        fmt.Println(err)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    RenameGroup(ac)
}
```

## Java

Variant 1:

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
            tObj.renameGroup(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void renameGroup(AnalyticsClient ac) throws Exception {
        long groupId = 35130000001364001l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        String groupName = "Renamed Group";
        workspace.renameGroup(groupId, groupName, null);
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
    private long workspaceId = 35130000001055707l;

    public static void main(String args[]) {
        String clientId = "1000.xxxxxxx";
        String clientSecret = "xxxxxxx";
        String refreshToken = "1000.xxxxxxx.xxxxxxx";

        Test tObj = new Test();
        AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);

        try {
            tObj.renameGroup(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void renameGroup(AnalyticsClient ac) throws Exception {
        long groupId = 35130000001364001l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        String groupName = "Finance & Accounts Team";
        JSONObject config = new JSONObject();
        config.put("groupDesc", "Finance, accounts payable, and treasury users");
        workspace.renameGroup(groupId, groupName, config);
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
        public $workspace_id = "35130000001055707";

        function __construct() {
            $this->ac = new AnalyticsClient($this->client_id, $this->client_secret, $this->refresh_token);
        }

        function renameGroup() {
            $group_id = "35130000001364001";
            $new_group_name = "Renamed Group";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->renameGroup($group_id, $new_group_name);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->renameGroup();
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
        public $workspace_id = "35130000001055707";

        function __construct() {
            $this->ac = new AnalyticsClient($this->client_id, $this->client_secret, $this->refresh_token);
        }

        function renameGroup() {
            $group_id = "35130000001364001";
            $new_group_name = "Finance & Accounts Team";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $config = array("groupDesc" => "Finance, accounts payable, and treasury users");
            $workspace->renameGroup($group_id, $new_group_name, $config);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->renameGroup();
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
    WORKSPACEID = "35130000001055707"

class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def rename_group(self, ac):
        group_id = "35130000001364001"
        group_name = "Renamed Group"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.rename_group(group_id, group_name)
        print("success")

try:
    obj = sample()
    obj.rename_group(obj.ac)
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
    WORKSPACEID = "35130000001055707"

class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def rename_group(self, ac):
        group_id = "35130000001364001"
        group_name = "Finance & Accounts Team"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        config = {"groupDesc": "Finance, accounts payable, and treasury users"}
        workspace.rename_group(group_id, group_name, config)
        print("success")

try:
    obj = sample()
    obj.rename_group(obj.ac)
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
var workspaceId = '35130000001055707';

var ac = new analyticsClient(clientId, clientSecret, refreshToken);

var groupId = '35130000001364001';
var groupName = 'Renamed Group';
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);

workspace.renameGroup(groupId, groupName).then(function () {
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
var workspaceId = '35130000001055707';

var ac = new analyticsClient(clientId, clientSecret, refreshToken);

var groupId = '35130000001364001';
var groupName = 'Finance & Accounts Team';
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);

var config = {"groupDesc": "Finance, accounts payable, and treasury users"};
workspace.renameGroup(groupId, groupName, config).then(function () {
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
  WORKSPACEID = "35130000001055707"
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

  def rename_group
    group_id = "35130000001364001"
    group_name = "Renamed Group"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.rename_group(group_id, group_name)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.rename_group
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
  WORKSPACEID = "35130000001055707"
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

  def rename_group
    group_id = "35130000001364001"
    group_name = "Finance & Accounts Team"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    config = {"groupDesc" => "Finance, accounts payable, and treasury users"}
    workspace.rename_group(group_id, group_name, config)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.rename_group
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
workspaceId = "35130000001055707";
groupId = "35130000001364001";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"groupName":"Renamed Group"};
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/groups/" + groupId
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
workspaceId = "35130000001055707";
groupId = "35130000001364001";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"groupName":"Finance & Accounts Team","groupDesc":"Finance, accounts payable, and treasury users"};
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/groups/" + groupId
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Rename Group](../../../domains/users-and-groups/workspace-groups/rename-group.md) - full endpoint reference.
- [Workspace Groups overview](../../../domains/users-and-groups/workspace-groups/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
