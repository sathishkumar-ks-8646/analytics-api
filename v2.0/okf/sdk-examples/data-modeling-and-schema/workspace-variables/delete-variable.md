---
type: SDK Example
title: SDK examples - Delete Variable
description: "Code samples in 9 languages for DELETE /restapi/v2/workspaces/{workspace-id}/variables/{variable-id} (deleteVariable)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - data-modeling-and-schema
  - workspace-variables
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
  operation_id: deleteVariable
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/variables/{variable-id}"
  endpoint_doc: "/domains/data-modeling-and-schema/workspace-variables/delete-variable.md"
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
    resource: "/references/openapi/data-modeling-schema-grouped-api.json"
    title: OpenAPI 3 specification - data-modeling-schema-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
  - id: endpoint-doc
    resource: "/domains/data-modeling-and-schema/workspace-variables/delete-variable.md"
    title: Endpoint reference - Delete Variable
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Delete Variable](../../../domains/data-modeling-and-schema/workspace-variables/delete-variable.md) (`DELETE /restapi/v2/workspaces/{workspace-id}/variables/{variable-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/variables/35130000001056201" -X 'DELETE' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
```

## C#

```csharp
using System;
using System.Collections.Generic;
using ZohoAnalytics;

namespace ZohoAnalyticsTest
{
    class Program
    {
        long orgId = 55522777;
        long workspaceId = 35130000001055707;

        public void DeleteVariable(IAnalyticsClient ac)
        {
            long variableId = 35130000001056201;
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.DeleteVariable(variableId);
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
                obj.DeleteVariable(ac);
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

func DeleteVariable(ac ZAnalytics.Client) {
    variableId := "35130000001056201"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    exception := workspace.DeleteVariable(variableId)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    DeleteVariable(ac)
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
            tObj.deleteVariable(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void deleteVariable(AnalyticsClient ac) throws Exception {
        long variableId = 35130000001056201l;
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.deleteVariable(variableId);
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

        function deleteVariable() {
            $variable_id = "35130000001056201";
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->deleteVariable($variable_id);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->deleteVariable();
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

class Config:
    CLIENTID = "1000.xxxxxxx"
    CLIENTSECRET = "xxxxxxx"
    REFRESHTOKEN = "1000.xxxxxxx.xxxxxxx"
    ORGID = "55522777"
    WORKSPACEID = "35130000001055707"

class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def delete_variable(self, ac):
        variable_id = "35130000001056201"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.delete_variable(variable_id)
        print("success")

try:
    obj = sample()
    obj.delete_variable(obj.ac)
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

var variableId = '35130000001056201';

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);

workspace.deleteVariable(variableId).then(function () {
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

  def delete_variable
    variable_id = "35130000001056201"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.delete_variable(variable_id)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.delete_variable
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
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/variables/35130000001056201"
  type :DELETE
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Delete Variable](../../../domains/data-modeling-and-schema/workspace-variables/delete-variable.md) - full endpoint reference.
- [Workspace Variables overview](../../../domains/data-modeling-and-schema/workspace-variables/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
