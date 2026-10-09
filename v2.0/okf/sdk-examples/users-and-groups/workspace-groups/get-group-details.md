---
type: SDK Example
title: SDK examples - Get Group Details
description: "Code samples in 9 languages for GET /restapi/v2/workspaces/{workspace-id}/groups/{group-id} (getGroupDetails)."
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
  operation_id: getGroupDetails
  method: GET
  path: "/restapi/v2/workspaces/{workspace-id}/groups/{group-id}"
  endpoint_doc: "/domains/users-and-groups/workspace-groups/get-group-details.md"
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
    last_modified: 2026-10-09T14:14:03Z
  - id: endpoint-doc
    resource: "/domains/users-and-groups/workspace-groups/get-group-details.md"
    title: Endpoint reference - Get Group Details
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

Code samples for [Get Group Details](../../../domains/users-and-groups/workspace-groups/get-group-details.md) (`GET /restapi/v2/workspaces/{workspace-id}/groups/{group-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/groups/<group-id>" \
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
        long workspaceId = 35130000001055707;

        public void GetGroupDetails(IAnalyticsClient ac)
        {
            long groupId = 35130000001364001;
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            JsonElement result = ws.GetGroupDetails(groupId);
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
                obj.GetGroupDetails(ac);
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

func GetGroupDetails(ac ZAnalytics.Client) {
    groupId := "35130000001364001"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, _ := workspace.GetGroupDetails(groupId)
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetGroupDetails(ac)
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
            tObj.getGroupDetails(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void getGroupDetails(AnalyticsClient ac) throws Exception {
        long groupId = 35130000001364001l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getGroupDetails(groupId);
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
        public $workspace_id = "35130000001055707";

        function __construct() {
            $this->ac = new AnalyticsClient($this->client_id, $this->client_secret, $this->refresh_token);
        }

        function getGroupDetails() {
            $group_id = "35130000001364001";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getGroupDetails($group_id);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->getGroupDetails();
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

    def get_group_details(self, ac):
        group_id = "35130000001364001"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_group_details(group_id)
        print(result)

try:
    obj = sample()
    obj.get_group_details(obj.ac)
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

var groupId = '35130000001364001';
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);

workspace.getGroupDetails(groupId).then(function (result) {
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

  def get_group_details
    group_id = "35130000001364001"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_group_details(group_id)
    puts result
  end
end

begin
  obj = Sample.new
  obj.get_group_details
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
groupId = "35130000001364001";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/groups/" + groupId
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Group Details](../../../domains/users-and-groups/workspace-groups/get-group-details.md) - full endpoint reference.
- [Workspace Groups overview](../../../domains/users-and-groups/workspace-groups/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
