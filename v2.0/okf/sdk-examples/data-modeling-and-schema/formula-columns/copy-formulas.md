---
type: SDK Example
title: SDK examples - Copy Custom Formulas
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/formulas/copy (copyFormulas)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/formulas/copy"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - data-modeling-and-schema
  - formula-columns
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
  operation_id: copyFormulas
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/formulas/copy"
  endpoint_doc: "/domains/data-modeling-and-schema/formula-columns/copy-formulas.md"
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
    last_modified: 2026-10-09T14:14:03Z
  - id: endpoint-doc
    resource: "/domains/data-modeling-and-schema/formula-columns/copy-formulas.md"
    title: Endpoint reference - Copy Custom Formulas
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

Code samples for [Copy Custom Formulas](../../../domains/data-modeling-and-schema/formula-columns/copy-formulas.md) (`POST /restapi/v2/workspaces/{workspace-id}/views/{view-id}/formulas/copy`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

Variant 1:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/formulas/copy" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"formulaColumnNames":["NetRevenue"],"destWorkspaceId":35130000001055709}'
```

Variant 2:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/views/35130000001055717/formulas/copy" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'ZANALYTICS-DEST-ORGID: <dest-org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"formulaColumnNames":["NetRevenue","GrossMargin"],"destWorkspaceId":35130000001055709,"workspaceKey":"a1b2c3d4e5f6g7h8"}'
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

        public void CopyFormulas(IAnalyticsClient ac)
        {
            long viewId = 35130000001055717;
            List<string> formulaNames = new List<string>() { "NetRevenue" };
            long destWorkspaceId = 35130000001055709;
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.CopyFormulas(formulaNames, destWorkspaceId, null, null);
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
                obj.CopyFormulas(ac);
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

        public void CopyFormulas(IAnalyticsClient ac)
        {
            long viewId = 35130000001055717;
            List<string> formulaNames = new List<string>() { "NetRevenue", "GrossMargin" };
            long destWorkspaceId = 35130000001055709;
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("workspaceKey", "a1b2c3d4e5f6g7h8");
            IViewAPI view = ac.GetViewInstance(orgId, workspaceId, viewId);
            view.CopyFormulas(formulaNames, destWorkspaceId, config, 700000987654);
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
                obj.CopyFormulas(ac);
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

func CopyFormulas(ac ZAnalytics.Client) {
    viewId := "35130000001055717"
    formulaNames := []string{"NetRevenue"}
    destWorkspaceId := "35130000001055709"
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    exception := view.CopyFormulas(formulaNames, destWorkspaceId, nil, nil)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CopyFormulas(ac)
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

func CopyFormulas(ac ZAnalytics.Client) {
    viewId := "35130000001055717"
    formulaNames := []string{"NetRevenue", "GrossMargin"}
    destWorkspaceId := "35130000001055709"
    config := map[string]interface{}{
        "workspaceKey": "a1b2c3d4e5f6g7h8",
    }
    view := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
    exception := view.CopyFormulas(formulaNames, destWorkspaceId, config, "700000987654")
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println("success")
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CopyFormulas(ac)
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
            tObj.copyFormulas(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void copyFormulas(AnalyticsClient ac) throws Exception {
        long viewId = 35130000001055717l;
        JSONArray formulaNames = new JSONArray();
        formulaNames.put("NetRevenue");
        long destWorkspaceId = 35130000001055709l;
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.copyFormulas(formulaNames, destWorkspaceId, null, null);
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
            tObj.copyFormulas(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void copyFormulas(AnalyticsClient ac) throws Exception {
        long viewId = 35130000001055717l;
        JSONArray formulaNames = new JSONArray();
        formulaNames.put("NetRevenue");
        formulaNames.put("GrossMargin");
        long destWorkspaceId = 35130000001055709l;
        JSONObject config = new JSONObject();
        config.put("workspaceKey", "a1b2c3d4e5f6g7h8");
        ViewAPI view = ac.getViewInstance(orgId, workspaceId, viewId);
        view.copyFormulas(formulaNames, destWorkspaceId, config, 700000987654l);
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

        function copyFormulas() {
            $view_id = "35130000001055717";
            $formula_names = array("NetRevenue");
            $dest_workspace_id = 35130000001055709;
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $view_id);
            $view->copyFormulas($formula_names, $dest_workspace_id, NULL, NULL);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->copyFormulas();
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

        function copyFormulas() {
            $view_id = "35130000001055717";
            $formula_names = array("NetRevenue", "GrossMargin");
            $dest_workspace_id = 35130000001055709;
            $config = array(
                "workspaceKey" => "a1b2c3d4e5f6g7h8"
            );
            $view = $this->ac->getViewInstance($this->org_id, $this->workspace_id, $view_id);
            $view->copyFormulas($formula_names, $dest_workspace_id, $config, 700000987654);
            echo "success\n";
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->copyFormulas();
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

    def copy_formulas(self, ac):
        formula_names = ["NetRevenue"]
        dest_workspace_id = 35130000001055709
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, "35130000001055717")
        view.copy_formulas(formula_names, dest_workspace_id, None, None)
        print("success")

try:
    obj = sample()
    obj.copy_formulas(obj.ac)
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

    def copy_formulas(self, ac):
        formula_names = ["NetRevenue", "GrossMargin"]
        dest_workspace_id = 35130000001055709
        config = {
            "workspaceKey": "a1b2c3d4e5f6g7h8"
        }
        view = ac.get_view_instance(Config.ORGID, Config.WORKSPACEID, "35130000001055717")
        view.copy_formulas(formula_names, dest_workspace_id, config, 700000987654)
        print("success")

try:
    obj = sample()
    obj.copy_formulas(obj.ac)
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

var viewId = '35130000001055717';
var formulaNames = ['NetRevenue'];
var destWorkspaceId = 35130000001055709;

var view = ac.getViewInstance(orgId, workspaceId, viewId);

view.copyFormulas(formulaNames, destWorkspaceId, null, null).then(function () {
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

var viewId = '35130000001055717';
var formulaNames = ['NetRevenue', 'GrossMargin'];
var destWorkspaceId = 35130000001055709;
var config = {
    workspaceKey: 'a1b2c3d4e5f6g7h8'
};

var view = ac.getViewInstance(orgId, workspaceId, viewId);

view.copyFormulas(formulaNames, destWorkspaceId, config, 700000987654).then(function () {
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

  def copy_formulas
    formula_names = ["NetRevenue"]
    dest_workspace_id = 35130000001055709
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, "35130000001055717")
    view.copy_formulas(formula_names, dest_workspace_id, nil, nil)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.copy_formulas
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

  def copy_formulas
    formula_names = ["NetRevenue", "GrossMargin"]
    dest_workspace_id = 35130000001055709
    config = {
        "workspaceKey" => "a1b2c3d4e5f6g7h8"
    }
    view = @ac.get_view_instance(Config::ORGID, Config::WORKSPACEID, "35130000001055717")
    view.copy_formulas(formula_names, dest_workspace_id, config, 700000987654)
    puts "success"
  end
end

begin
  obj = Sample.new
  obj.copy_formulas
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
config_formulaColumnNames = List();
config_formulaColumnNames.add("NetRevenue");
config.put("formulaColumnNames", config_formulaColumnNames);
config.put("destWorkspaceId", 35130000001055709);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/35130000001055717/formulas/copy"
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
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
headersMap.put("ZANALYTICS-DEST-ORGID", "<dest-org-id>");
config = Map();
config_formulaColumnNames = List();
config_formulaColumnNames.add("NetRevenue");
config_formulaColumnNames.add("GrossMargin");
config.put("formulaColumnNames", config_formulaColumnNames);
config.put("destWorkspaceId", 35130000001055709);
config.put("workspaceKey", "a1b2c3d4e5f6g7h8");
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/views/35130000001055717/formulas/copy"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Copy Custom Formulas](../../../domains/data-modeling-and-schema/formula-columns/copy-formulas.md) - full endpoint reference.
- [Custom Formula Columns overview](../../../domains/data-modeling-and-schema/formula-columns/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
