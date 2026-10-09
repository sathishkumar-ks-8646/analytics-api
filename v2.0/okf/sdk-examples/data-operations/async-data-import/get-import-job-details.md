---
type: SDK Example
title: SDK examples - Get Import Job Details
description: "Code samples in 9 languages for GET /restapi/v2/bulk/workspaces/{workspace-id}/importjobs/{job-id} (getImportJobDetails)."
resource: "https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/{workspace-id}/importjobs/{job-id}"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - data-operations
  - async-data-import
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
  operation_id: getImportJobDetails
  method: GET
  path: "/restapi/v2/bulk/workspaces/{workspace-id}/importjobs/{job-id}"
  endpoint_doc: "/domains/data-operations/async-data-import/get-import-job-details.md"
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
    last_modified: 2026-10-09T08:29:02Z
  - id: endpoint-doc
    resource: "/domains/data-operations/async-data-import/get-import-job-details.md"
    title: Endpoint reference - Get Import Job Details
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Get Import Job Details](../../../domains/data-operations/async-data-import/get-import-job-details.md) (`GET /restapi/v2/bulk/workspaces/{workspace-id}/importjobs/{job-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/35130000001055707/importjobs/35130000001056301" -H 'ZANALYTICS-ORGID: 55522777' -H 'Authorization: Zoho-oauthtoken <access_token>'
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
        long jobId = 35130000001056301;

        public void GetImportJobDetails(IAnalyticsClient ac)
        {
            IBulkAPI bulk = ac.GetBulkInstance(orgId, workspaceId);
            JsonElement result = bulk.GetImportJobDetails(jobId);
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
                obj.GetImportJobDetails(ac);
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
    jobId = "35130000001056301"
)

func GetImportJobDetails(ac ZAnalytics.Client) {
    bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)
    result, err := bulk.GetImportJobDetails(jobId)
    if err != nil {
        fmt.Println("Error - " + err.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetImportJobDetails(ac)
}
```

## Java

```java
import com.zoho.analytics.client.*;
import org.json.*;

public class Test {

    private long orgId = 55522777l;
    private long workspaceId = 35130000001055707l;
    private long jobId = 35130000001056301l;

    public static void main(String args[]) {
        String clientId = "1000.xxxxxxx";
        String clientSecret = "xxxxxxx";
        String refreshToken = "1000.xxxxxxx.xxxxxxx";

        Test tObj = new Test();
        AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);

        try {
            tObj.getImportJobDetails(ac);
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

    public void getImportJobDetails(AnalyticsClient ac) throws Exception {
        BulkAPI bulk = ac.getBulkInstance(orgId, workspaceId);
        JSONObject result = bulk.getImportJobDetails(jobId);
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
        public $job_id = "35130000001056301";

        function __construct() {
            $this->ac = new AnalyticsClient($this->client_id, $this->client_secret, $this->refresh_token);
        }

        function getImportJobDetails() {
            $bulk = $this->ac->getBulkInstance($this->org_id, $this->workspace_id);
            $response = $bulk->getImportJobDetails($this->job_id);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->getImportJobDetails();
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
    JOBID = "35130000001056301"

class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def get_import_job_details(self, ac):
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        result = bulk.get_import_job_details(Config.JOBID)
        print(result)

try:
    obj = sample()
    obj.get_import_job_details(obj.ac)

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
var jobId = '35130000001056301';

var ac = new analyticsClient(clientId, clientSecret, refreshtoken);

var bulk = ac.getBulkInstance(orgId, workspaceId);
bulk.getImportJobDetails(jobId).then((response) => {
    console.log(response);
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
  JOBID = "35130000001056301"
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

  def get_import_job_details
    bulk = @ac.get_bulk_instance(Config::ORGID, Config::WORKSPACEID)
    result = bulk.get_import_job_details(Config::JOBID)
    puts result
  end
end

begin
  obj = Sample.new
  obj.get_import_job_details
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
jobId = "35130000001056301";

headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);

response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/bulk/workspaces/" + workspaceId + "/importjobs/" + jobId
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Get Import Job Details](../../../domains/data-operations/async-data-import/get-import-job-details.md) - full endpoint reference.
- [Asynchronous & Batch Data Import overview](../../../domains/data-operations/async-data-import/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
