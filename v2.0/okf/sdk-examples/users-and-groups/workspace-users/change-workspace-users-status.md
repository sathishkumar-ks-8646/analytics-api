---
type: SDK Example
title: SDK examples - Change Workspace Users Status
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id}/users/status (changeWorkspaceUsersStatus)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/users/status"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - users-and-groups
  - workspace-users
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
  operation_id: changeWorkspaceUsersStatus
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/users/status"
  endpoint_doc: "/domains/users-and-groups/workspace-users/change-workspace-users-status.md"
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
    last_modified: 2026-10-09T13:04:25Z
  - id: endpoint-doc
    resource: "/domains/users-and-groups/workspace-users/change-workspace-users-status.md"
    title: Endpoint reference - Change Workspace Users Status
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Change Workspace Users Status](../../../domains/users-and-groups/workspace-users/change-workspace-users-status.md) (`PUT /restapi/v2/workspaces/{workspace-id}/users/status`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/users/status" \
  -X 'PUT' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"emailIds":["user@example.com"],"operation":"activate"}'
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
        long workspaceId = 35130000001055707;

        public void ChangeWorkspaceUserStatus(IAnalyticsClient ac)
        {
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            List<string> emailIds = new List<string>();
            emailIds.Add("user@example.com");
            string operation = "activate";
            ws.ChangeWorkspaceUserStatus(emailIds, operation, null);
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
                obj.ChangeWorkspaceUserStatus(ac);
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
    workspaceId = "35130000001055707"
)

func ChangeWorkspaceUserStatus(ac ZAnalytics.Client) {
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    emailIds := []string{"user@example.com"}
    operation := "activate"
    err := workspace.ChangeWorkspaceUserStatus(emailIds, operation, nil)
    if err != nil {
        fmt.Println(err)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    ChangeWorkspaceUserStatus(ac)
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
            tObj.changeWorkspaceUserStatus(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void changeWorkspaceUserStatus(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONArray emailIds = new JSONArray();
        emailIds.put("user@example.com");
        String operation = "activate";
        workspace.changeWorkspaceUserStatus(emailIds, operation, null);
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
        public $workspace_id = "35130000001055707";

        function __construct() {
            $this->ac = new AnalyticsClient($this->client_id, $this->client_secret, $this->refresh_token);
        }

        function changeWorkspaceUserStatus() {
            $email_ids = array("user@example.com");
            $operation = "activate";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->changeWorkspaceUserStatus($email_ids, $operation);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->changeWorkspaceUserStatus();
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
    WORKSPACEID = "35130000001055707"

class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def change_workspace_user_status(self, ac):
        email_ids = ["user@example.com"]
        operation = "activate"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.change_workspace_user_status(email_ids, operation)
        print("success")

try:
    obj = sample()
    obj.change_workspace_user_status(obj.ac)
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
var workspaceId = '35130000001055707';

var ac = new analyticsClient(clientId, clientSecret, refreshToken);

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
var emailIds = ["user@example.com"];
var operation = 'activate';

workspace.changeWorkspaceUserStatus(emailIds, operation).then(function () {
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

  def change_workspace_user_status
    email_ids = ["user@example.com"]
    operation = "activate"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.change_workspace_user_status(email_ids, operation)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.change_workspace_user_status
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
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"emailIds":["user@example.com"],"operation":"activate"};
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/users/status"
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Change Workspace Users Status](../../../domains/users-and-groups/workspace-users/change-workspace-users-status.md) - full endpoint reference.
- [Workspace Users overview](../../../domains/users-and-groups/workspace-users/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
