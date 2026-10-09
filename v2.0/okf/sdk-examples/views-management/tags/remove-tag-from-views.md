---
type: SDK Example
title: SDK examples - Remove Tag From Multiple Views
description: "Code samples in 9 languages for DELETE /restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views (removeTagFromViews)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views"
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
  operation_id: removeTagFromViews
  method: DELETE
  path: "/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views"
  endpoint_doc: "/domains/views-management/tags/remove-tag-from-views.md"
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
    last_modified: 2026-10-09T08:29:02Z
  - id: endpoint-doc
    resource: "/domains/views-management/tags/remove-tag-from-views.md"
    title: Endpoint reference - Remove Tag From Multiple Views
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

Code samples for [Remove Tag From Multiple Views](../../../domains/views-management/tags/remove-tag-from-views.md) (`DELETE /restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

Variant 1:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/tags/35130000001364501/views" -X 'DELETE' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"viewIds":["35130000001055717"]}'
```

Variant 2:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/tags/35130000001364501/views" -X 'DELETE' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"dissociateAll":true}'
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

        public void RemoveTagFromViews(IAnalyticsClient ac)
        {
            long tagId = 35130000001364501L;
            List<long> viewIds = new List<long>();
            viewIds.Add(35130000001055717L);
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.RemoveTagFromViews(tagId, viewIds, null);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.RemoveTagFromViews(ac);
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

        public void RemoveTagFromViews(IAnalyticsClient ac)
        {
            long tagId = 35130000001364501L;
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("dissociateAll", true);
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            ws.RemoveTagFromViews(tagId, null, config);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.RemoveTagFromViews(ac);
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

func RemoveTagFromViews(ac ZAnalytics.Client) {
    tagId := "35130000001364501"
    viewIds := []string{"35130000001055717"}
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    exception := workspace.RemoveTagFromViews(tagId, viewIds, nil)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    RemoveTagFromViews(ac)
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

func RemoveTagFromViews(ac ZAnalytics.Client) {
    tagId := "35130000001364501"
    config := map[string]interface{}{"dissociateAll": true}
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    exception := workspace.RemoveTagFromViews(tagId, nil, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println("success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    RemoveTagFromViews(ac)
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
            tObj.removeTagFromViews(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void removeTagFromViews(AnalyticsClient ac) throws Exception {
        long tagId = 35130000001364501l;
        JSONArray viewIds = new JSONArray();
        viewIds.put("35130000001055717");
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.removeTagFromViews(tagId, viewIds, null);
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
            tObj.removeTagFromViews(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void removeTagFromViews(AnalyticsClient ac) throws Exception {
        long tagId = 35130000001364501l;
        JSONObject config = new JSONObject();
        config.put("dissociateAll", true);
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        workspace.removeTagFromViews(tagId, null, config);
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

    function removeTagFromViews() {
        $tag_id = "35130000001364501";
        $view_ids = array("35130000001055717");
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->removeTagFromViews($tag_id, $view_ids);
        echo "success\n";
    }
}

$obj = new Test();
$obj->removeTagFromViews();
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

    function removeTagFromViews() {
        $tag_id = "35130000001364501";
        $config = array("dissociateAll" => true);
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $workspace->removeTagFromViews($tag_id, null, $config);
        echo "success\n";
    }
}

$obj = new Test();
$obj->removeTagFromViews();
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

    def remove_tag_from_views(self, ac):
        tag_id = "35130000001364501"
        view_ids = ["35130000001055717"]
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.remove_tag_from_views(tag_id, view_ids)
        print("success")

obj = Sample()
obj.remove_tag_from_views(obj.ac)
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

    def remove_tag_from_views(self, ac):
        tag_id = "35130000001364501"
        config = {"dissociateAll": True}
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        workspace.remove_tag_from_views(tag_id, None, config)
        print("success")

obj = Sample()
obj.remove_tag_from_views(obj.ac)
```

## Node.js

Variant 1:

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var tagId = '35130000001364501';
var viewIds = ['35130000001055717'];
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.removeTagFromViews(tagId, viewIds).then(() => { console.log('success'); }).catch((error) => { console.log(error); });
```

Variant 2:

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var tagId = '35130000001364501';
var config = {dissociateAll: true};
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.removeTagFromViews(tagId, null, config).then(() => { console.log('success'); }).catch((error) => { console.log(error); });
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

  def remove_tag_from_views
    tag_id = "35130000001364501"
    view_ids = ["35130000001055717"]
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.remove_tag_from_views(tag_id, view_ids)
    puts "success"
  end
end

obj = Sample.new
obj.remove_tag_from_views
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

  def remove_tag_from_views
    tag_id = "35130000001364501"
    config = {"dissociateAll" => true}
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    workspace.remove_tag_from_views(tag_id, nil, config)
    puts "success"
  end
end

obj = Sample.new
obj.remove_tag_from_views
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
viewIds = List();
viewIds.add("35130000001055717");
config.put("viewIds", viewIds);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/tags/" + tagId + "/views"
  type :DELETE
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
config.put("dissociateAll", true);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/tags/" + tagId + "/views"
  type :DELETE
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info "success";
```

# Related

- [Remove Tag From Multiple Views](../../../domains/views-management/tags/remove-tag-from-views.md) - full endpoint reference.
- [Tags overview](../../../domains/views-management/tags/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
