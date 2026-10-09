---
type: SDK Example
title: SDK examples - Update Datasource Connection
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id} (updateDatasourceConnection)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - data-operations
  - data-sync-and-connectivity
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
  operation_id: updateDatasourceConnection
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}"
  endpoint_doc: "/domains/data-operations/data-sync-and-connectivity/update-datasource-connection.md"
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
    resource: "/references/openapi/data-operations-grouped-api.json"
    title: OpenAPI 3 specification - data-operations-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
  - id: endpoint-doc
    resource: "/domains/data-operations/data-sync-and-connectivity/update-datasource-connection.md"
    title: Endpoint reference - Update Datasource Connection
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

Code samples for [Update Datasource Connection](../../../domains/data-operations/data-sync-and-connectivity/update-datasource-connection.md) (`PUT /restapi/v2/workspaces/{workspace-id}/datasources/{datasource-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/datasources/35130000001056401" -X 'PUT' -H 'ZANALYTICS-ORGID: 55522777' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"serviceName":"AMAZON RDS","databaseType":"MYSQL","hostName":"zylker.abcdef.us-east-1.rds.amazonaws.com","port":3306,"userName":"zylkeradmin","password":"Zoho@123","cloudDatabaseName":"sales_db","useSSL":true}'
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
        long datasourceId = 35130000001056401;

        public void UpdateDatasourceConnection(IAnalyticsClient ac)
        {
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("serviceName", "AMAZON RDS");
            config.Add("databaseType", "MYSQL");
            config.Add("hostName", "zylker.abcdef.us-east-1.rds.amazonaws.com");
            config.Add("port", 3306);
            config.Add("userName", "zylkeradmin");
            config.Add("password", "Zoho@123");
            config.Add("cloudDatabaseName", "sales_db");
            config.Add("useSSL", true);
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            workspace.UpdateDatasourceConnection(datasourceId, config);
            Console.WriteLine("Connection updated");
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
                obj.UpdateDatasourceConnection(ac);
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
    datasourceId = "35130000001056401"
)

func UpdateDatasourceConnection(ac ZAnalytics.Client) {
    config := map[string]interface{}{}
    config["serviceName"] = "AMAZON RDS"
    config["databaseType"] = "MYSQL"
    config["hostName"] = "zylker.abcdef.us-east-1.rds.amazonaws.com"
    config["port"] = 3306
    config["userName"] = "zylkeradmin"
    config["password"] = "Zoho@123"
    config["cloudDatabaseName"] = "sales_db"
    config["useSSL"] = true
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    err := workspace.UpdateDatasourceConnection(datasourceId, config)
    if err != nil {
        fmt.Println("Error - " + err.ErrorMessage)
    } else {
        fmt.Println("Connection updated")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    UpdateDatasourceConnection(ac)
}
```

## Java

```java
import com.zoho.analytics.client.*;
import org.json.*;

public class Test {

    private long orgId = 55522777l;
    private long workspaceId = 35130000001055707l;
    private long datasourceId = 35130000001056401l;

    public static void main(String args[]) {
        String clientId = "1000.xxxxxxx";
        String clientSecret = "xxxxxxx";
        String refreshToken = "1000.xxxxxxx.xxxxxxx";

        Test tObj = new Test();
        AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);

        try {
            tObj.updateDatasourceConnection(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (ParseException ex) {
            System.out.println("Parser exception - ErrorMessage : " + ex.getResponseMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void updateDatasourceConnection(AnalyticsClient ac) throws Exception {
        JSONObject config = new JSONObject();
        config.put("serviceName", "AMAZON RDS");
        config.put("databaseType", "MYSQL");
        config.put("hostName", "zylker.abcdef.us-east-1.rds.amazonaws.com");
        config.put("port", 3306);
        config.put("userName", "zylkeradmin");
        config.put("password", "Zoho@123");
        config.put("cloudDatabaseName", "sales_db");
        config.put("useSSL", true);
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.updateDatasourceConnection(datasourceId, config);
        System.out.println("Connection updated");
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
        public $datasource_id = "35130000001056401";

        function __construct() {
            $this->ac = new AnalyticsClient($this->client_id, $this->client_secret, $this->refresh_token);
        }

        function updateDatasourceConnection() {
            $config = array();
            $config["serviceName"] = "AMAZON RDS";
            $config["databaseType"] = "MYSQL";
            $config["hostName"] = "zylker.abcdef.us-east-1.rds.amazonaws.com";
            $config["port"] = 3306;
            $config["userName"] = "zylkeradmin";
            $config["password"] = "Zoho@123";
            $config["cloudDatabaseName"] = "sales_db";
            $config["useSSL"] = true;
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $workspace->updateDatasourceConnection($this->datasource_id, $config);
            echo "Connection updated";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->updateDatasourceConnection();
    }
    catch(ServerException $se) {
        echo "Server exception : " . $se->getErrorMessage() . "\n";
    }
    catch(IOException $ioe) {
        echo "IO exception : " . $ioe->getErrorMessage() . "\n";
    }
    catch(ParseException $pe) {
        echo "Parser exception : " . $pe->getErrorMessage() . "\n";
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
    DATASOURCEID = "35130000001056401"

class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def update_datasource_connection(self, ac):
        config = {}
        config["serviceName"] = "AMAZON RDS"
        config["databaseType"] = "MYSQL"
        config["hostName"] = "zylker.abcdef.us-east-1.rds.amazonaws.com"
        config["port"] = 3306
        config["userName"] = "zylkeradmin"
        config["password"] = "Zoho@123"
        config["cloudDatabaseName"] = "sales_db"
        config["useSSL"] = True
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.update_datasource_connection(Config.DATASOURCEID, config)
        print("Connection updated")

try:
    obj = sample()
    obj.update_datasource_connection(obj.ac)

except Exception as e:
    print(str(e))
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');

var clientId = '1000.xxxxxxx';
var clientSecret = 'xxxxxxx';
var refreshtoken = '1000.xxxxxxx.xxxxxxx';
var orgId = '55522777';
var workspaceId = '35130000001055707';
var datasourceId = '35130000001056401';

var ac = new analyticsClient(clientId, clientSecret, refreshtoken);

var config = {
    "serviceName": "AMAZON RDS",
    "databaseType": "MYSQL",
    "hostName": "zylker.abcdef.us-east-1.rds.amazonaws.com",
    "port": 3306,
    "userName": "zylkeradmin",
    "password": "Zoho@123",
    "cloudDatabaseName": "sales_db",
    "useSSL": true
};
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.updateDatasourceConnection(datasourceId, config).then(() => {
    console.log('Connection updated');
}).catch((error) => {
    console.log('errorCode : ' + error.errorCode);
    console.log('errorMessage : ' + error.errorMessage);
});
```

## Ruby

```ruby
require 'zoho_analytics_client'

class Config
  ORGID = "55522777"
  WORKSPACEID = "35130000001055707"
  DATASOURCEID = "35130000001056401"
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

  def update_datasource_connection
    config = {
      "serviceName" => "AMAZON RDS",
      "databaseType" => "MYSQL",
      "hostName" => "zylker.abcdef.us-east-1.rds.amazonaws.com",
      "port" => 3306,
      "userName" => "zylkeradmin",
      "password" => "Zoho@123",
      "cloudDatabaseName" => "sales_db",
      "useSSL" => true
    }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.update_datasource_connection(Config::DATASOURCEID, config)
    puts "Connection updated"
  end
end

begin
  obj = Sample.new
  obj.update_datasource_connection
rescue ServerError => e
  puts "Server Error: \#{e.response_content}"
rescue StandardError => e
  puts e.message
end
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
datasourceId = "35130000001056401";

headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("serviceName", "AMAZON RDS");
config.put("databaseType", "MYSQL");
config.put("hostName", "zylker.abcdef.us-east-1.rds.amazonaws.com");
config.put("port", 3306);
config.put("userName", "zylkeradmin");
config.put("password", "Zoho@123");
config.put("cloudDatabaseName", "sales_db");
config.put("useSSL", true);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/datasources/" + datasourceId
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Update Datasource Connection](../../../domains/data-operations/data-sync-and-connectivity/update-datasource-connection.md) - full endpoint reference.
- [Data Sync & Connectivity overview](../../../domains/data-operations/data-sync-and-connectivity/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
