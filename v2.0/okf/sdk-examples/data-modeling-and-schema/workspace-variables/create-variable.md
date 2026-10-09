---
type: SDK Example
title: SDK examples - Create Variable
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/variables (createVariable)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/variables"
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
  operation_id: createVariable
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/variables"
  endpoint_doc: "/domains/data-modeling-and-schema/workspace-variables/create-variable.md"
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
    last_modified: 2026-10-09T08:29:02Z
  - id: endpoint-doc
    resource: "/domains/data-modeling-and-schema/workspace-variables/create-variable.md"
    title: Endpoint reference - Create Variable
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

Code samples for [Create Variable](../../../domains/data-modeling-and-schema/workspace-variables/create-variable.md) (`POST /restapi/v2/workspaces/{workspace-id}/variables`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

Variant 1:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/variables" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"variableName":"Region","variableDataType":1,"variableType":0,"defaultData":{"values":["North","South","East","West"],"defaultValue":"North"}}'
```

Variant 2:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/variables" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"variableName":"Region","variableDataType":1,"variableType":0,"defaultData":{"values":["North","South","East","West"],"defaultValue":"North"},"userSpecificData":[{"values":["East","West"],"defaultValue":"East","emailIds":["sales.east@zylker.com"]}],"format":{"alignment":"Left"}}'
```

## C#

Variant 1:

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

        public void CreateVariable(IAnalyticsClient ac)
        {
            string variableName = "Region";
            int variableDataType = 1;
            int variableType = 0;
            Dictionary<string, object> config = new Dictionary<string, object>();
            Dictionary<string, object> defaultData1 = new Dictionary<string, object>();
            List<object> values2 = new List<object>();
            values2.Add("North");
            values2.Add("South");
            values2.Add("East");
            values2.Add("West");
            defaultData1.Add("values", values2);
            defaultData1.Add("defaultValue", "North");
            config.Add("defaultData", defaultData1);
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            var result = workspace.CreateVariable(variableName, variableDataType, variableType, config);
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
                obj.CreateVariable(ac);
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

namespace ZohoAnalyticsTest
{
    class Program
    {
        long orgId = 55522777;
        long workspaceId = 35130000001055707;

        public void CreateVariable(IAnalyticsClient ac)
        {
            string variableName = "Region";
            int variableDataType = 1;
            int variableType = 0;
            Dictionary<string, object> config = new Dictionary<string, object>();
            Dictionary<string, object> defaultData1 = new Dictionary<string, object>();
            List<object> values2 = new List<object>();
            values2.Add("North");
            values2.Add("South");
            values2.Add("East");
            values2.Add("West");
            defaultData1.Add("values", values2);
            defaultData1.Add("defaultValue", "North");
            config.Add("defaultData", defaultData1);
            List<object> userSpecificData3 = new List<object>();
            Dictionary<string, object> userSpecificData3Item4 = new Dictionary<string, object>();
            List<object> values5 = new List<object>();
            values5.Add("East");
            values5.Add("West");
            userSpecificData3Item4.Add("values", values5);
            userSpecificData3Item4.Add("defaultValue", "East");
            List<object> emailIds6 = new List<object>();
            emailIds6.Add("sales.east@zylker.com");
            userSpecificData3Item4.Add("emailIds", emailIds6);
            userSpecificData3.Add(userSpecificData3Item4);
            config.Add("userSpecificData", userSpecificData3);
            Dictionary<string, object> format7 = new Dictionary<string, object>();
            format7.Add("alignment", "Left");
            config.Add("format", format7);
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            var result = workspace.CreateVariable(variableName, variableDataType, variableType, config);
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
                obj.CreateVariable(ac);
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

func CreateVariable(ac ZAnalytics.Client) {
    variableName := "Region"
    variableDataType := 1
    variableType := 0
    config := map[string]interface{}{
        "defaultData": map[string]interface{}{
            "values": []interface{}{"North", "South", "East", "West"},
            "defaultValue": "North",
        },
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.CreateVariable(variableName, variableDataType, variableType, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateVariable(ac)
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

func CreateVariable(ac ZAnalytics.Client) {
    variableName := "Region"
    variableDataType := 1
    variableType := 0
    config := map[string]interface{}{
        "defaultData": map[string]interface{}{
            "values": []interface{}{"North", "South", "East", "West"},
            "defaultValue": "North",
        },
        "userSpecificData": []interface{}{map[string]interface{}{
            "values": []interface{}{"East", "West"},
            "defaultValue": "East",
            "emailIds": []interface{}{"sales.east@zylker.com"},
        }},
        "format": map[string]interface{}{
            "alignment": "Left",
        },
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.CreateVariable(variableName, variableDataType, variableType, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateVariable(ac)
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
            tObj.createVariable(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void createVariable(AnalyticsClient ac) throws Exception {
        String variableName = "Region";
        int variableDataType = 1;
        int variableType = 0;
        JSONObject config = new JSONObject();
        JSONObject defaultData1 = new JSONObject();
        JSONArray values2 = new JSONArray();
        values2.put("North");
        values2.put("South");
        values2.put("East");
        values2.put("West");
        defaultData1.put("values", values2);
        defaultData1.put("defaultValue", "North");
        config.put("defaultData", defaultData1);
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.createVariable(variableName, variableDataType, variableType, config);
        System.out.println(result);
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
            tObj.createVariable(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void createVariable(AnalyticsClient ac) throws Exception {
        String variableName = "Region";
        int variableDataType = 1;
        int variableType = 0;
        JSONObject config = new JSONObject();
        JSONObject defaultData1 = new JSONObject();
        JSONArray values2 = new JSONArray();
        values2.put("North");
        values2.put("South");
        values2.put("East");
        values2.put("West");
        defaultData1.put("values", values2);
        defaultData1.put("defaultValue", "North");
        config.put("defaultData", defaultData1);
        JSONArray userSpecificData3 = new JSONArray();
        JSONObject userSpecificData3Item4 = new JSONObject();
        JSONArray values5 = new JSONArray();
        values5.put("East");
        values5.put("West");
        userSpecificData3Item4.put("values", values5);
        userSpecificData3Item4.put("defaultValue", "East");
        JSONArray emailIds6 = new JSONArray();
        emailIds6.put("sales.east@zylker.com");
        userSpecificData3Item4.put("emailIds", emailIds6);
        userSpecificData3.put(userSpecificData3Item4);
        config.put("userSpecificData", userSpecificData3);
        JSONObject format7 = new JSONObject();
        format7.put("alignment", "Left");
        config.put("format", format7);
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.createVariable(variableName, variableDataType, variableType, config);
        System.out.println(result);
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

        function createVariable() {
            $variable_name = "Region";
            $variable_data_type = 1;
            $variable_type = 0;
            $config = array(
                "defaultData" => array(
                    "values" => array("North", "South", "East", "West"),
                    "defaultValue" => "North"
                )
            );
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->createVariable($variable_name, $variable_data_type, $variable_type, $config);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->createVariable();
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

        function createVariable() {
            $variable_name = "Region";
            $variable_data_type = 1;
            $variable_type = 0;
            $config = array(
                "defaultData" => array(
                    "values" => array("North", "South", "East", "West"),
                    "defaultValue" => "North"
                ),
                "userSpecificData" => array(array(
                    "values" => array("East", "West"),
                    "defaultValue" => "East",
                    "emailIds" => array("sales.east@zylker.com")
                )),
                "format" => array(
                    "alignment" => "Left"
                )
            );
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->createVariable($variable_name, $variable_data_type, $variable_type, $config);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->createVariable();
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

class Config:
    CLIENTID = "1000.xxxxxxx"
    CLIENTSECRET = "xxxxxxx"
    REFRESHTOKEN = "1000.xxxxxxx.xxxxxxx"
    ORGID = "55522777"
    WORKSPACEID = "35130000001055707"

class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def create_variable(self, ac):
        variable_name = "Region"
        variable_data_type = 1
        variable_type = 0
        config = {
            "defaultData": {
                "values": ["North", "South", "East", "West"],
                "defaultValue": "North"
            }
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_variable(variable_name, variable_data_type, variable_type, config)
        print(result)

try:
    obj = sample()
    obj.create_variable(obj.ac)
except Exception as e:
    print(str(e))
```

Variant 2:

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

    def create_variable(self, ac):
        variable_name = "Region"
        variable_data_type = 1
        variable_type = 0
        config = {
            "defaultData": {
                "values": ["North", "South", "East", "West"],
                "defaultValue": "North"
            },
            "userSpecificData": [{
                "values": ["East", "West"],
                "defaultValue": "East",
                "emailIds": ["sales.east@zylker.com"]
            }],
            "format": {
                "alignment": "Left"
            }
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_variable(variable_name, variable_data_type, variable_type, config)
        print(result)

try:
    obj = sample()
    obj.create_variable(obj.ac)
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

var variableName = 'Region';
var variableDataType = 1;
var variableType = 0;
var config = {
    defaultData: {
        values: ['North', 'South', 'East', 'West'],
        defaultValue: 'North'
    }
};

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);

workspace.createVariable(variableName, variableDataType, variableType, config).then(function (result) {
    console.log(result);
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

var variableName = 'Region';
var variableDataType = 1;
var variableType = 0;
var config = {
    defaultData: {
        values: ['North', 'South', 'East', 'West'],
        defaultValue: 'North'
    },
    userSpecificData: [{
        values: ['East', 'West'],
        defaultValue: 'East',
        emailIds: ['sales.east@zylker.com']
    }],
    format: {
        alignment: 'Left'
    }
};

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);

workspace.createVariable(variableName, variableDataType, variableType, config).then(function (result) {
    console.log(result);
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

  def create_variable
    variable_name = "Region"
    variable_data_type = 1
    variable_type = 0
    config = {
        "defaultData" => {
            "values" => ["North", "South", "East", "West"],
            "defaultValue" => "North"
        }
    }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.create_variable(variable_name, variable_data_type, variable_type, config)
    puts result
  end
end

begin
  obj = Sample.new
  obj.create_variable
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

  def create_variable
    variable_name = "Region"
    variable_data_type = 1
    variable_type = 0
    config = {
        "defaultData" => {
            "values" => ["North", "South", "East", "West"],
            "defaultValue" => "North"
        },
        "userSpecificData" => [{
            "values" => ["East", "West"],
            "defaultValue" => "East",
            "emailIds" => ["sales.east@zylker.com"]
        }],
        "format" => {
            "alignment" => "Left"
        }
    }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.create_variable(variable_name, variable_data_type, variable_type, config)
    puts result
  end
end

begin
  obj = Sample.new
  obj.create_variable
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
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("variableName", "Region");
config.put("variableDataType", 1);
config.put("variableType", 0);
config_defaultData = Map();
config_defaultData_values = List();
config_defaultData_values.add("North");
config_defaultData_values.add("South");
config_defaultData_values.add("East");
config_defaultData_values.add("West");
config_defaultData.put("values", config_defaultData_values);
config_defaultData.put("defaultValue", "North");
config.put("defaultData", config_defaultData);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/variables"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

Variant 2:

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("variableName", "Region");
config.put("variableDataType", 1);
config.put("variableType", 0);
config_defaultData = Map();
config_defaultData_values = List();
config_defaultData_values.add("North");
config_defaultData_values.add("South");
config_defaultData_values.add("East");
config_defaultData_values.add("West");
config_defaultData.put("values", config_defaultData_values);
config_defaultData.put("defaultValue", "North");
config.put("defaultData", config_defaultData);
config_userSpecificData = List();
config_userSpecificData_item1 = Map();
config_userSpecificData_item1_values = List();
config_userSpecificData_item1_values.add("East");
config_userSpecificData_item1_values.add("West");
config_userSpecificData_item1.put("values", config_userSpecificData_item1_values);
config_userSpecificData_item1.put("defaultValue", "East");
config_userSpecificData_item1_emailIds = List();
config_userSpecificData_item1_emailIds.add("sales.east@zylker.com");
config_userSpecificData_item1.put("emailIds", config_userSpecificData_item1_emailIds);
config_userSpecificData.add(config_userSpecificData_item1);
config.put("userSpecificData", config_userSpecificData);
config_format = Map();
config_format.put("alignment", "Left");
config.put("format", config_format);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/variables"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Create Variable](../../../domains/data-modeling-and-schema/workspace-variables/create-variable.md) - full endpoint reference.
- [Workspace Variables overview](../../../domains/data-modeling-and-schema/workspace-variables/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
