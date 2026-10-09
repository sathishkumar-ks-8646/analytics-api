---
type: SDK Example
title: SDK examples - Update Dashboard
description: "Code samples in 9 languages for PUT /restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id} (updateDashboard)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}"
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - reports-and-dashboards
  - dashboards
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
  operation_id: updateDashboard
  method: PUT
  path: "/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}"
  endpoint_doc: "/domains/reports-and-dashboards/dashboards/update-dashboard.md"
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
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
  - id: endpoint-doc
    resource: "/domains/reports-and-dashboards/dashboards/update-dashboard.md"
    title: Endpoint reference - Update Dashboard
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

Code samples for [Update Dashboard](../../../domains/reports-and-dashboards/dashboards/update-dashboard.md) (`PUT /restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/dashboards/35130000001055801" -X 'PUT' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"layout":"{\"1\":{\"type\":\"USERFILTERS\",\"width\":80,\"height\":3,\"left\":0,\"top\":0},\"2\":{\"type\":\"HTML\",\"width\":80,\"height\":5,\"left\":0,\"top\":3,\"content\":\"<b>Updated Title</b>\"},\"3\":{\"type\":\"VIEW\",\"width\":80,\"height\":20,\"left\":0,\"top\":8,\"viewName\":\"Sales Chart\",\"properties\":{}}}","themes":{"layoutType":2,"type":"solid","solid":{"background":"#1A1B2E"},"card":{"background":"#3E3F4D","title":{"border":{"color":"#6F738E"}},"border":{"color":"#6F738E","width":2}}}}'
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

        public void UpdateDashboard(IAnalyticsClient ac)
        {
            long dashboardId = 35130000001055801;
            string displayName = "Sales Overview - Updated";
            // A supplied layout replaces the existing one in full - partial card sets are not supported. The client library sends layout as the JSON-encoded string the API expects.
            Dictionary<string, object> filterCard = new Dictionary<string, object>{{"type","USERFILTERS"},{"width",80},{"height",3},{"left",0},{"top",0}};
            Dictionary<string, object> htmlCard = new Dictionary<string, object>{{"type","HTML"},{"width",80},{"height",5},{"left",0},{"top",3},{"content","<b>Updated Title</b>"}};
            Dictionary<string, object> viewCard = new Dictionary<string, object>{{"type","VIEW"},{"width",80},{"height",20},{"left",0},{"top",8},{"viewName","Sales Chart"},{"properties",new Dictionary<string, object>()}};
            Dictionary<string, object> layout = new Dictionary<string, object>{{"1",filterCard},{"2",htmlCard},{"3",viewCard}};
            Dictionary<string, object> themes = new Dictionary<string, object>
            {
                {"layoutType", 2},
                {"type", "solid"},
                {"solid", new Dictionary<string, object>{{"background","#1A1B2E"}}},
                {"card", new Dictionary<string, object>
                    {
                        {"background", "#3E3F4D"},
                        {"title", new Dictionary<string, object>{{"border",new Dictionary<string, object>{{"color","#6F738E"}}}}},
                        {"border", new Dictionary<string, object>{{"color","#6F738E"},{"width",2}}}
                    }
                }
            };
            IDashboardAPI dashboard = ac.GetDashboardInstance(orgId, workspaceId, dashboardId);
            dashboard.UpdateDashboard(displayName, layout, null, themes);
            Console.WriteLine("success");
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.UpdateDashboard(ac);
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

var (
    clientId = "1000.xxxxxxx"
    clientSecret = "xxxxxxx"
    refreshToken = "1000.xxxxxxx.xxxxxxx"
    orgId = "55522777"
    workspaceId = "35130000001055707"
)

func UpdateDashboard(ac ZAnalytics.Client) {
    dashboardId := "35130000001055801"
    displayName := "Sales Overview - Updated"
    // A supplied layout replaces the existing one in full - partial card sets are not supported. The client library sends layout as the JSON-encoded string the API expects.
    layout := map[string]interface{}{
        "1": map[string]interface{}{"type": "USERFILTERS", "width": 80, "height": 3, "left": 0, "top": 0},
        "2": map[string]interface{}{"type": "HTML", "width": 80, "height": 5, "left": 0, "top": 3, "content": "<b>Updated Title</b>"},
        "3": map[string]interface{}{"type": "VIEW", "width": 80, "height": 20, "left": 0, "top": 8, "viewName": "Sales Chart", "properties": map[string]interface{}{}},
    }
    themes := map[string]interface{}{
        "layoutType": 2,
        "type": "solid",
        "solid": map[string]interface{}{"background": "#1A1B2E"},
        "card": map[string]interface{}{
            "background": "#3E3F4D",
            "title": map[string]interface{}{"border": map[string]interface{}{"color": "#6F738E"}},
            "border": map[string]interface{}{"color": "#6F738E", "width": 2},
        },
    }
    dashboard := ZAnalytics.GetDashboardInstance(&ac, orgId, workspaceId, dashboardId)
    exception := dashboard.UpdateDashboard(displayName, layout, nil, themes)
    if exception != nil { fmt.Println(exception.ErrorMessage); return }
    fmt.Println("Success")
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    UpdateDashboard(ac)
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
            tObj.updateDashboard(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void updateDashboard(AnalyticsClient ac) throws Exception {
        long dashboardId = 35130000001055801l;
        String displayName = "Sales Overview - Updated";
        // A supplied layout replaces the existing one in full - partial card sets are not supported. The client library sends layout as the JSON-encoded string the API expects.
        JSONObject filterCard = new JSONObject();
        filterCard.put("type", "USERFILTERS");
        filterCard.put("width", 80);
        filterCard.put("height", 3);
        filterCard.put("left", 0);
        filterCard.put("top", 0);
        JSONObject htmlCard = new JSONObject();
        htmlCard.put("type", "HTML");
        htmlCard.put("width", 80);
        htmlCard.put("height", 5);
        htmlCard.put("left", 0);
        htmlCard.put("top", 3);
        htmlCard.put("content", "<b>Updated Title</b>");
        JSONObject viewCard = new JSONObject();
        viewCard.put("type", "VIEW");
        viewCard.put("width", 80);
        viewCard.put("height", 20);
        viewCard.put("left", 0);
        viewCard.put("top", 8);
        viewCard.put("viewName", "Sales Chart");
        viewCard.put("properties", new JSONObject());
        JSONObject layout = new JSONObject();
        layout.put("1", filterCard);
        layout.put("2", htmlCard);
        layout.put("3", viewCard);
        JSONObject cardTheme = new JSONObject();
        cardTheme.put("background", "#3E3F4D");
        cardTheme.put("title", new JSONObject().put("border", new JSONObject().put("color", "#6F738E")));
        cardTheme.put("border", new JSONObject().put("color", "#6F738E").put("width", 2));
        JSONObject themes = new JSONObject();
        themes.put("layoutType", 2);
        themes.put("type", "solid");
        themes.put("solid", new JSONObject().put("background", "#1A1B2E"));
        themes.put("card", cardTheme);
        DashboardAPI dashboard = ac.getDashboardInstance(orgId, workspaceId, dashboardId);
        dashboard.updateDashboard(displayName, layout, null, themes);
        System.out.println("success");
    }
}
```

## PHP

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

    function updateDashboard() {
        $dashboard_id = "35130000001055801";
        $display_name = "Sales Overview - Updated";
        // A supplied layout replaces the existing one in full - partial card sets are not supported. layout travels as a JSON-encoded string.
        $layout = json_encode([
            "1" => ["type" => "USERFILTERS", "width" => 80, "height" => 3, "left" => 0, "top" => 0],
            "2" => ["type" => "HTML", "width" => 80, "height" => 5, "left" => 0, "top" => 3, "content" => "<b>Updated Title</b>"],
            "3" => ["type" => "VIEW", "width" => 80, "height" => 20, "left" => 0, "top" => 8, "viewName" => "Sales Chart", "properties" => (object)[]]
        ]);
        $themes = [
            "layoutType" => 2,
            "type" => "solid",
            "solid" => ["background" => "#1A1B2E"],
            "card" => [
                "background" => "#3E3F4D",
                "title" => ["border" => ["color" => "#6F738E"]],
                "border" => ["color" => "#6F738E", "width" => 2]
            ]
        ];
        $dashboard = $this->ac->getDashboardInstance($this->org_id, $this->workspace_id, $dashboard_id);
        $dashboard->updateDashboard($display_name, $layout, null, $themes);
        echo "success";
    }
}

$obj = new Test();
$obj->updateDashboard();
?>
```

## Python

```python
import json
from AnalyticsClient import AnalyticsClient

class Config:
    CLIENTID = "1000.xxxxxxx"
    CLIENTSECRET = "xxxxxxx"
    REFRESHTOKEN = "1000.xxxxxxx.xxxxxxx"
    ORGID = "55522777"
    WORKSPACEID = "35130000001055707"

class sample:
    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def update_dashboard(self, ac):
        dashboard_id = "35130000001055801"
        display_name = "Sales Overview - Updated"
        # A supplied layout replaces the existing one in full - partial card sets are not supported. layout travels as a JSON-encoded string.
        layout = json.dumps({
            "1": {"type": "USERFILTERS", "width": 80, "height": 3, "left": 0, "top": 0},
            "2": {"type": "HTML", "width": 80, "height": 5, "left": 0, "top": 3, "content": "<b>Updated Title</b>"},
            "3": {"type": "VIEW", "width": 80, "height": 20, "left": 0, "top": 8, "viewName": "Sales Chart", "properties": {}}
        })
        themes = {
            "layoutType": 2,
            "type": "solid",
            "solid": {"background": "#1A1B2E"},
            "card": {
                "background": "#3E3F4D",
                "title": {"border": {"color": "#6F738E"}},
                "border": {"color": "#6F738E", "width": 2}
            }
        }
        dashboard = ac.get_dashboard_instance(Config.ORGID, Config.WORKSPACEID, dashboard_id)
        dashboard.update_dashboard(display_name, layout, None, themes)
        print("success")

obj = sample()
obj.update_dashboard(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var dashboardId = '35130000001055801';
var displayName = 'Sales Overview - Updated';
// A supplied layout replaces the existing one in full - partial card sets are not supported. layout travels as a JSON-encoded string.
var layout = JSON.stringify({
    '1': { type: 'USERFILTERS', width: 80, height: 3, left: 0, top: 0 },
    '2': { type: 'HTML', width: 80, height: 5, left: 0, top: 3, content: '<b>Updated Title</b>' },
    '3': { type: 'VIEW', width: 80, height: 20, left: 0, top: 8, viewName: 'Sales Chart', properties: {} }
});
var themes = {
    layoutType: 2,
    type: 'solid',
    solid: { background: '#1A1B2E' },
    card: {
        background: '#3E3F4D',
        title: { border: { color: '#6F738E' } },
        border: { color: '#6F738E', width: 2 }
    }
};
var dashboard = ac.getDashboardInstance(orgId, workspaceId, dashboardId);
dashboard.updateDashboard(displayName, layout, null, themes).then(() => { console.log('success'); }).catch((error) => { console.log(error); });
```

## Ruby

```ruby
require "json"
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

  def update_dashboard
    dashboard_id = "35130000001055801"
    display_name = "Sales Overview - Updated"
    # A supplied layout replaces the existing one in full - partial card sets are not supported. layout travels as a JSON-encoded string.
    layout = JSON.generate({
      "1" => { "type" => "USERFILTERS", "width" => 80, "height" => 3, "left" => 0, "top" => 0 },
      "2" => { "type" => "HTML", "width" => 80, "height" => 5, "left" => 0, "top" => 3, "content" => "<b>Updated Title</b>" },
      "3" => { "type" => "VIEW", "width" => 80, "height" => 20, "left" => 0, "top" => 8, "viewName" => "Sales Chart", "properties" => {} }
    })
    themes = {
      "layoutType" => 2,
      "type" => "solid",
      "solid" => { "background" => "#1A1B2E" },
      "card" => {
        "background" => "#3E3F4D",
        "title" => { "border" => { "color" => "#6F738E" } },
        "border" => { "color" => "#6F738E", "width" => 2 }
      }
    }
    dashboard = @ac.get_dashboard_instance(Config::ORGID, Config::WORKSPACEID, dashboard_id)
    dashboard.update_dashboard(display_name, layout, nil, themes)
    puts "success"
  end
end

obj = Sample.new
obj.update_dashboard
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
dashboardId = "35130000001055801";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
// A supplied layout replaces the existing one in full - partial card sets are not supported
filterCard = Map();
filterCard.put("type", "USERFILTERS");
filterCard.put("width", 80);
filterCard.put("height", 3);
filterCard.put("left", 0);
filterCard.put("top", 0);
htmlCard = Map();
htmlCard.put("type", "HTML");
htmlCard.put("width", 80);
htmlCard.put("height", 5);
htmlCard.put("left", 0);
htmlCard.put("top", 3);
htmlCard.put("content", "<b>Updated Title</b>");
viewCard = Map();
viewCard.put("type", "VIEW");
viewCard.put("width", 80);
viewCard.put("height", 20);
viewCard.put("left", 0);
viewCard.put("top", 8);
viewCard.put("viewName", "Sales Chart");
viewCard.put("properties", Map());
layout = Map();
layout.put("1", filterCard);
layout.put("2", htmlCard);
layout.put("3", viewCard);
titleBorder = Map();
titleBorder.put("color", "#6F738E");
cardTitle = Map();
cardTitle.put("border", titleBorder);
cardBorder = Map();
cardBorder.put("color", "#6F738E");
cardBorder.put("width", 2);
cardTheme = Map();
cardTheme.put("background", "#3E3F4D");
cardTheme.put("title", cardTitle);
cardTheme.put("border", cardBorder);
solidTheme = Map();
solidTheme.put("background", "#1A1B2E");
themes = Map();
themes.put("layoutType", 2);
themes.put("type", "solid");
themes.put("solid", solidTheme);
themes.put("card", cardTheme);
config = Map();
config.put("layout", layout.toString()); // layout travels as a JSON-encoded string
config.put("themes", themes);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/dashboards/" + dashboardId
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Update Dashboard](../../../domains/reports-and-dashboards/dashboards/update-dashboard.md) - full endpoint reference.
- [Dashboards overview](../../../domains/reports-and-dashboards/dashboards/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
