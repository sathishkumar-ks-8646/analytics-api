---
type: SDK Example
title: SDK examples - Update Tag
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id}/tags/{tag-id} (updateTag)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - views-management
  - tags
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
  operation_id: updateTag
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}"
  endpoint_doc: "/domains/views-management/tags/update-tag.md"
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
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
  - id: endpoint-doc
    resource: "/domains/views-management/tags/update-tag.md"
    title: Endpoint reference - Update Tag
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Update Tag](../../../domains/views-management/tags/update-tag.md) (`PUT /restapi/v2/workspaces/{workspace-id}/tags/{tag-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

Variant 1:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/tags/35130000001364501" -X 'PUT' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"name":"Finance - Archive","colorCode":"#e72d35"}'
```

Variant 2:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/tags/35130000001364501" -X 'PUT' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"colorCode":"#1da043"}'
```

## C#

Variant 1:

```csharp
using System;
using System.Collections.Generic;
using System.Text.Json;
using ZohoAnalytics;

namespace ZohoAnalyticsTest
{
    class Program
    {
        long orgId = 55522777;
        long workspaceId = 35130000001055707;

        public void UpdateTag(IAnalyticsClient ac)
        {
            long tagId = 35130000001364501L;
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("name", "Finance - Archive");
            config.Add("colorCode", "#e72d35");
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.UpdateTag(tagId, config);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.UpdateTag(ac);
        }
    }
}
```

Variant 2:

```csharp
using System;
using System.Collections.Generic;
using System.Text.Json;
using ZohoAnalytics;

namespace ZohoAnalyticsTest
{
    class Program
    {
        long orgId = 55522777;
        long workspaceId = 35130000001055707;

        public void UpdateTag(IAnalyticsClient ac)
        {
            long tagId = 35130000001364501L;
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("colorCode", "#1da043");
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.UpdateTag(tagId, config);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.UpdateTag(ac);
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

var (
    clientId = "1000.xxxxxxx"
    clientSecret = "xxxxxxx"
    refreshToken = "1000.xxxxxxx.xxxxxxx"
    orgId = "55522777"
    workspaceId = "35130000001055707"
)

func UpdateTag(ac ZAnalytics.Client) {
    tagId := "35130000001364501"
    config := map[string]interface{}{"name": "Finance - Archive", "colorCode": "#e72d35"}
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    exception := workspace.UpdateTag(tagId, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    UpdateTag(ac)
}
```

Variant 2:

```go
package main

import (
    "fmt"
    ZAnalytics "zoho/pkg/analyticsclient"
)

var (
    clientId = "1000.xxxxxxx"
    clientSecret = "xxxxxxx"
    refreshToken = "1000.xxxxxxx.xxxxxxx"
    orgId = "55522777"
    workspaceId = "35130000001055707"
)

func UpdateTag(ac ZAnalytics.Client) {
    tagId := "35130000001364501"
    config := map[string]interface{}{"colorCode": "#1da043"}
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    exception := workspace.UpdateTag(tagId, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    UpdateTag(ac)
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
            tObj.updateTag(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void updateTag(AnalyticsClient ac) throws Exception {
        long tagId = 35130000001364501l;
        JSONObject config = new JSONObject();
        config.put("name", "Finance - Archive");
        config.put("colorCode", "#e72d35");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.updateTag(tagId, config);
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
            tObj.updateTag(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void updateTag(AnalyticsClient ac) throws Exception {
        long tagId = 35130000001364501l;
        JSONObject config = new JSONObject();
        config.put("colorCode", "#1da043");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.updateTag(tagId, config);
        System.out.println("success");
    }
}
```

## PHP

Variant 1:

```php
<?php
require 'AnalyticsClient.php';

class Test {
    public $ac;
    public $org_id = "55522777";
    public $workspace_id = "35130000001055707";

    function __construct() {
        $this->ac = new AnalyticsClient("1000.xxxxxxx", "xxxxxxx", "1000.xxxxxxx.xxxxxxx");
    }

    function updateTag() {
        $tag_id = "35130000001364501";
        $config = array("name" => "Finance - Archive", "colorCode" => "#e72d35");
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->updateTag($tag_id, $config);
        echo "success\n";
    }
}

$obj = new Test();
$obj->updateTag();
?>
```

Variant 2:

```php
<?php
require 'AnalyticsClient.php';

class Test {
    public $ac;
    public $org_id = "55522777";
    public $workspace_id = "35130000001055707";

    function __construct() {
        $this->ac = new AnalyticsClient("1000.xxxxxxx", "xxxxxxx", "1000.xxxxxxx.xxxxxxx");
    }

    function updateTag() {
        $tag_id = "35130000001364501";
        $config = array("colorCode" => "#1da043");
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->updateTag($tag_id, $config);
        echo "success\n";
    }
}

$obj = new Test();
$obj->updateTag();
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

class Sample:
    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def update_tag(self, ac):
        tag_id = "35130000001364501"
        config = {"name": "Finance - Archive", "colorCode": "#e72d35"}
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.update_tag(tag_id, config)
        print("success")

obj = Sample()
obj.update_tag(obj.ac)
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

class Sample:
    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def update_tag(self, ac):
        tag_id = "35130000001364501"
        config = {"colorCode": "#1da043"}
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.update_tag(tag_id, config)
        print("success")

obj = Sample()
obj.update_tag(obj.ac)
```

## Node.js

Variant 1:

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var tagId = '35130000001364501';
var config = {name: 'Finance - Archive', colorCode: '#e72d35'};
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.updateTag(tagId, config).then(() => { console.log('success'); }).catch((error) => { console.log(error); });
```

Variant 2:

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var tagId = '35130000001364501';
var config = {colorCode: '#1da043'};
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.updateTag(tagId, config).then(() => { console.log('success'); }).catch((error) => { console.log(error); });
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
    @ac = AnalyticsClient.new.with_data_center("US").with_oauth({
      "clientId" => "1000.xxxxxxx",
      "clientSecret" => "xxxxxxx",
      "refreshToken" => "1000.xxxxxxx.xxxxxxx"
    }).build
  end

  def update_tag
    tag_id = "35130000001364501"
    config = {"name" => "Finance - Archive", "colorCode" => "#e72d35"}
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.update_tag(tag_id, config)
    puts "success"
  end
end

obj = Sample.new
obj.update_tag
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
    @ac = AnalyticsClient.new.with_data_center("US").with_oauth({
      "clientId" => "1000.xxxxxxx",
      "clientSecret" => "xxxxxxx",
      "refreshToken" => "1000.xxxxxxx.xxxxxxx"
    }).build
  end

  def update_tag
    tag_id = "35130000001364501"
    config = {"colorCode" => "#1da043"}
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.update_tag(tag_id, config)
    puts "success"
  end
end

obj = Sample.new
obj.update_tag
```

## Deluge (Zoho scripting)

Variant 1:

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
tagId = "35130000001364501";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("name", "Finance - Archive");
config.put("colorCode", "#e72d35");
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/tags/" + tagId
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
tagId = "35130000001364501";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("colorCode", "#1da043");
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/tags/" + tagId
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Update Tag](../../../domains/views-management/tags/update-tag.md) - full endpoint reference.
- [Tags overview](../../../domains/views-management/tags/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
