---
type: SDK Example
title: SDK examples - Add Group Members
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members (addGroupMembers)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members"
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
  operation_id: addGroupMembers
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members"
  endpoint_doc: "/domains/users-and-groups/workspace-groups/add-group-members.md"
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
    resource: "/domains/users-and-groups/workspace-groups/add-group-members.md"
    title: Endpoint reference - Add Group Members
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Add Group Members](../../../domains/users-and-groups/workspace-groups/add-group-members.md) (`POST /restapi/v2/workspaces/{workspace-id}/groups/{group-id}/members`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

Variant 1:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/groups/<group-id>/members" \
  -X 'POST' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"emailIds":["user@example.com"]}'
```

Variant 2:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/groups/<group-id>/members" \
  -X 'POST' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"emailIds":["grace@acme.com"],"inviteMail":true,"mailSubject":"You've been added to Finance Team","mailMessage":"Hi Grace,<br>You now have group access to Finance Team reports."}'
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

        public void AddGroupMembers(IAnalyticsClient ac)
        {
            long groupId = 35130000001364001;
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            List<string> emailIds = new List<string>();
            emailIds.Add("user@example.com");
            ws.AddGroupMembers(groupId, emailIds, null);
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
                obj.AddGroupMembers(ac);
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

        public void AddGroupMembers(IAnalyticsClient ac)
        {
            long groupId = 35130000001364001;
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            List<string> emailIds = new List<string>();
            emailIds.Add("grace@acme.com");
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("inviteMail", true);
            config.Add("mailSubject", "You've been added to Finance Team");
            config.Add("mailMessage", "Hi Grace,<br>You now have group access to Finance Team reports.");
            ws.AddGroupMembers(groupId, emailIds, config);
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
                obj.AddGroupMembers(ac);
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

func AddGroupMembers(ac ZAnalytics.Client) {
    groupId := "35130000001364001"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    emailIds := []string{"user@example.com"}
    err := workspace.AddGroupMembers(groupId, emailIds, nil)
    if err != nil {
        fmt.Println(err)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    AddGroupMembers(ac)
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

func AddGroupMembers(ac ZAnalytics.Client) {
    groupId := "35130000001364001"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    emailIds := []string{"grace@acme.com"}
    config := map[string]interface{}{"inviteMail": true, "mailSubject": "You've been added to Finance Team", "mailMessage": "Hi Grace,<br>You now have group access to Finance Team reports."}
    err := workspace.AddGroupMembers(groupId, emailIds, config)
    if err != nil {
        fmt.Println(err)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    AddGroupMembers(ac)
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
            tObj.addGroupMembers(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void addGroupMembers(AnalyticsClient ac) throws Exception {
        long groupId = 35130000001364001l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("user@example.com");
        workspace.addGroupMembers(groupId, emailIds, null);
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
            tObj.addGroupMembers(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void addGroupMembers(AnalyticsClient ac) throws Exception {
        long groupId = 35130000001364001l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("grace@acme.com");
        JSONObject config = new JSONObject();
        config.put("inviteMail", true);
        config.put("mailSubject", "You've been added to Finance Team");
        config.put("mailMessage", "Hi Grace,<br>You now have group access to Finance Team reports.");
        workspace.addGroupMembers(groupId, emailIds, config);
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

        function addGroupMembers() {
            $group_id = "35130000001364001";
            $group_members = array("user@example.com");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->addGroupMembers($group_id, $group_members);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->addGroupMembers();
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

        function addGroupMembers() {
            $group_id = "35130000001364001";
            $group_members = array("grace@acme.com");
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $config = array("inviteMail" => true, "mailSubject" => "You've been added to Finance Team", "mailMessage" => "Hi Grace,<br>You now have group access to Finance Team reports.");
            $workspace->addGroupMembers($group_id, $group_members, $config);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->addGroupMembers();
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

    def add_group_members(self, ac):
        group_id = "35130000001364001"
        email_ids = ["user@example.com"]
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.add_group_members(group_id, email_ids)
        print("success")

try:
    obj = sample()
    obj.add_group_members(obj.ac)
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

    def add_group_members(self, ac):
        group_id = "35130000001364001"
        email_ids = ["grace@acme.com"]
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        config = {"inviteMail": True, "mailSubject": "You've been added to Finance Team", "mailMessage": "Hi Grace,<br>You now have group access to Finance Team reports."}
        workspace.add_group_members(group_id, email_ids, config)
        print("success")

try:
    obj = sample()
    obj.add_group_members(obj.ac)
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
var emailIds = ["user@example.com"];
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);

workspace.addGroupMembers(groupId, emailIds).then(function () {
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
var emailIds = ["grace@acme.com"];
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);

var config = {"inviteMail": true, "mailSubject": "You've been added to Finance Team", "mailMessage": "Hi Grace,<br>You now have group access to Finance Team reports."};
workspace.addGroupMembers(groupId, emailIds, config).then(function () {
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

  def add_group_members
    group_id = "35130000001364001"
    email_ids = ["user@example.com"]
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.add_group_members(group_id, email_ids)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.add_group_members
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

  def add_group_members
    group_id = "35130000001364001"
    email_ids = ["grace@acme.com"]
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    config = {"inviteMail" => true, "mailSubject" => "You've been added to Finance Team", "mailMessage" => "Hi Grace,<br>You now have group access to Finance Team reports."}
    workspace.add_group_members(group_id, email_ids, config)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.add_group_members
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
config = {"emailIds":["user@example.com"]};
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/groups/" + groupId + "/members"
  type :POST
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
config = {"emailIds":["grace@acme.com"],"inviteMail":true,"mailSubject":"You've been added to Finance Team","mailMessage":"Hi Grace,<br>You now have group access to Finance Team reports."};
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/groups/" + groupId + "/members"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Add Group Members](../../../domains/users-and-groups/workspace-groups/add-group-members.md) - full endpoint reference.
- [Workspace Groups overview](../../../domains/users-and-groups/workspace-groups/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
