---
type: SDK Example
title: SDK examples - Create Tag
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/tags (createTag)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/tags"
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
  operation_id: createTag
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/tags"
  endpoint_doc: "/domains/views-management/tags/create-tag.md"
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
    resource: "/domains/views-management/tags/create-tag.md"
    title: Endpoint reference - Create Tag
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

Code samples for [Create Tag](../../../domains/views-management/tags/create-tag.md) (`POST /restapi/v2/workspaces/{workspace-id}/tags`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

Variant 1:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/tags" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"name":"Finance","colorCode":"#1da043"}'
```

Variant 2:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/tags" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"name":"Deprecated","colorCode":"#f90"}'
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

        public void CreateTag(IAnalyticsClient ac)
        {
            string tagName = "Finance";
            string colorCode = "#1da043";
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            string tagId = ws.CreateTag(tagName, colorCode);
            Console.WriteLine(tagId);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.CreateTag(ac);
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

        public void CreateTag(IAnalyticsClient ac)
        {
            string tagName = "Deprecated";
            string colorCode = "#f90";
            IWorkspaceAPI ws = ac.GetWorkspaceInstance(orgId, workspaceId);
            string tagId = ws.CreateTag(tagName, colorCode);
            Console.WriteLine(tagId);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.CreateTag(ac);
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

func CreateTag(ac ZAnalytics.Client) {
    tagName := "Finance"
    colorCode := "#1da043"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.CreateTag(tagName, colorCode)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateTag(ac)
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

func CreateTag(ac ZAnalytics.Client) {
    tagName := "Deprecated"
    colorCode := "#f90"
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.CreateTag(tagName, colorCode)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
        return
    }
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateTag(ac)
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
            tObj.createTag(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void createTag(AnalyticsClient ac) throws Exception {
        String tagName = "Finance";
        String colorCode = "#1da043";
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        long tagId = workspace.createTag(tagName, colorCode);
        System.out.println(tagId);
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
            tObj.createTag(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void createTag(AnalyticsClient ac) throws Exception {
        String tagName = "Deprecated";
        String colorCode = "#f90";
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        long tagId = workspace.createTag(tagName, colorCode);
        System.out.println(tagId);
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

    function createTag() {
        $tag_name = "Finance";
        $color_code = "#1da043";
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $response = $workspace->createTag($tag_name, $color_code);
        print_r($response);
    }
}

$obj = new Test();
$obj->createTag();
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

    function createTag() {
        $tag_name = "Deprecated";
        $color_code = "#f90";
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $response = $workspace->createTag($tag_name, $color_code);
        print_r($response);
    }
}

$obj = new Test();
$obj->createTag();
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

    def create_tag(self, ac):
        tag_name = "Finance"
        color_code = "#1da043"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_tag(tag_name, color_code)
        print(result)

obj = Sample()
obj.create_tag(obj.ac)
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

    def create_tag(self, ac):
        tag_name = "Deprecated"
        color_code = "#f90"
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.create_tag(tag_name, color_code)
        print(result)

obj = Sample()
obj.create_tag(obj.ac)
```

## Node.js

Variant 1:

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var tagName = 'Finance';
var colorCode = '#1da043';
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.createTag(tagName, colorCode).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
```

Variant 2:

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var tagName = 'Deprecated';
var colorCode = '#f90';
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.createTag(tagName, colorCode).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
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

  def create_tag
    tag_name = "Finance"
    color_code = "#1da043"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.create_tag(tag_name, color_code)
    puts result
  end
end

obj = Sample.new
obj.create_tag
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

  def create_tag
    tag_name = "Deprecated"
    color_code = "#f90"
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.create_tag(tag_name, color_code)
    puts result
  end
end

obj = Sample.new
obj.create_tag
```

## Deluge (Zoho scripting)

Variant 1:

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("name", "Finance");
config.put("colorCode", "#1da043");
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/tags"
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
config.put("name", "Deprecated");
config.put("colorCode", "#f90");
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/tags"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Create Tag](../../../domains/views-management/tags/create-tag.md) - full endpoint reference.
- [Tags overview](../../../domains/views-management/tags/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
