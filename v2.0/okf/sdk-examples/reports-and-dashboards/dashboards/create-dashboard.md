---
type: SDK Example
title: SDK examples - Create Dashboard
description: "Code samples in 9 languages for POST /restapi/v2/workspaces/{workspace-id}/dashboards (createDashboard)."
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/dashboards"
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
  operation_id: createDashboard
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/dashboards"
  endpoint_doc: "/domains/reports-and-dashboards/dashboards/create-dashboard.md"
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
    last_modified: 2026-10-09T14:14:03Z
  - id: endpoint-doc
    resource: "/domains/reports-and-dashboards/dashboards/create-dashboard.md"
    title: Endpoint reference - Create Dashboard
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

Code samples for [Create Dashboard](../../../domains/reports-and-dashboards/dashboards/create-dashboard.md) (`POST /restapi/v2/workspaces/{workspace-id}/dashboards`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/dashboards" -X 'POST' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"displayName":"Sales Overview","layout":"{\"1\":{\"type\":\"USERFILTERS\",\"width\":80,\"height\":3,\"left\":0,\"top\":0},\"2\":{\"type\":\"HTML\",\"width\":80,\"height\":5,\"left\":0,\"top\":3,\"content\":\"<b>Sales Dashboard</b>\"},\"3\":{\"type\":\"VIEW\",\"width\":80,\"height\":20,\"left\":0,\"top\":8,\"viewName\":\"Sales Chart\",\"properties\":{}}}","settings":{"allowDrillDown":"true","fitToWidth":"true","allowExport":{"csv":"true","pdf":"true"}},"themes":{"layoutType":2,"type":"solid","solid":{"background":"#333542"},"card":{"background":"#3E3F4D","title":{"border":{"color":"#6F738E"}},"border":{"color":"#6F738E","width":2}}}}'
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

        public void CreateDashboard(IAnalyticsClient ac)
        {
            string displayName = "Sales Overview";
            // Each layout key is a card ID; the value is that card's configuration. The client library sends layout as the JSON-encoded string the API expects.
            Dictionary<string, object> filterCard = new Dictionary<string, object>{{"type","USERFILTERS"},{"width",80},{"height",3},{"left",0},{"top",0}};
            Dictionary<string, object> htmlCard = new Dictionary<string, object>{{"type","HTML"},{"width",80},{"height",5},{"left",0},{"top",3},{"content","<b>Sales Dashboard</b>"}};
            Dictionary<string, object> viewCard = new Dictionary<string, object>{{"type","VIEW"},{"width",80},{"height",20},{"left",0},{"top",8},{"viewName","Sales Chart"},{"properties",new Dictionary<string, object>()}};
            Dictionary<string, object> layout = new Dictionary<string, object>{{"1",filterCard},{"2",htmlCard},{"3",viewCard}};
            Dictionary<string, object> settings = new Dictionary<string, object>{{"allowDrillDown","true"},{"fitToWidth","true"},{"allowExport",new Dictionary<string, object>{{"csv","true"},{"pdf","true"}}}};
            Dictionary<string, object> themes = new Dictionary<string, object>
            {
                {"layoutType", 2},
                {"type", "solid"},
                {"solid", new Dictionary<string, object>{{"background","#333542"}}},
                {"card", new Dictionary<string, object>
                    {
                        {"background", "#3E3F4D"},
                        {"title", new Dictionary<string, object>{{"border",new Dictionary<string, object>{{"color","#6F738E"}}}}},
                        {"border", new Dictionary<string, object>{{"color","#6F738E"},{"width",2}}}
                    }
                }
            };
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            string dashboardId = workspace.CreateDashboard(displayName, layout, settings, themes);
            Console.WriteLine(dashboardId);
        }

        static void Main(string[] args)
        {
            string clientId = "1000.xxxxxxx";
            string clientSecret = "xxxxxxx";
            string refreshToken = "1000.xxxxxxx.xxxxxxx";
            IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);
            Program obj = new Program();
            obj.CreateDashboard(ac);
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

func CreateDashboard(ac ZAnalytics.Client) {
    displayName := "Sales Overview"
    // Each layout key is a card ID; the value is that card's configuration. The client library sends layout as the JSON-encoded string the API expects.
    layout := map[string]interface{}{
        "1": map[string]interface{}{"type": "USERFILTERS", "width": 80, "height": 3, "left": 0, "top": 0},
        "2": map[string]interface{}{"type": "HTML", "width": 80, "height": 5, "left": 0, "top": 3, "content": "<b>Sales Dashboard</b>"},
        "3": map[string]interface{}{"type": "VIEW", "width": 80, "height": 20, "left": 0, "top": 8, "viewName": "Sales Chart", "properties": map[string]interface{}{}},
    }
    settings := map[string]interface{}{"allowDrillDown": "true", "fitToWidth": "true", "allowExport": map[string]interface{}{"csv": "true", "pdf": "true"}}
    themes := map[string]interface{}{
        "layoutType": 2,
        "type": "solid",
        "solid": map[string]interface{}{"background": "#333542"},
        "card": map[string]interface{}{
            "background": "#3E3F4D",
            "title": map[string]interface{}{"border": map[string]interface{}{"color": "#6F738E"}},
            "border": map[string]interface{}{"color": "#6F738E", "width": 2},
        },
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    dashboardId, exception := workspace.CreateDashboard(displayName, layout, settings, themes)
    if exception != nil { fmt.Println(exception.ErrorMessage); return }
    fmt.Println(dashboardId)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateDashboard(ac)
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
            tObj.createDashboard(ac);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void createDashboard(AnalyticsClient ac) throws Exception {
        String displayName = "Sales Overview";
        // Each layout key is a card ID; the value is that card's configuration. The client library sends layout as the JSON-encoded string the API expects.
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
        htmlCard.put("content", "<b>Sales Dashboard</b>");
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
        JSONObject allowExport = new JSONObject();
        allowExport.put("csv", "true");
        allowExport.put("pdf", "true");
        JSONObject settings = new JSONObject();
        settings.put("allowDrillDown", "true");
        settings.put("fitToWidth", "true");
        settings.put("allowExport", allowExport);
        JSONObject cardTheme = new JSONObject();
        cardTheme.put("background", "#3E3F4D");
        cardTheme.put("title", new JSONObject().put("border", new JSONObject().put("color", "#6F738E")));
        cardTheme.put("border", new JSONObject().put("color", "#6F738E").put("width", 2));
        JSONObject themes = new JSONObject();
        themes.put("layoutType", 2);
        themes.put("type", "solid");
        themes.put("solid", new JSONObject().put("background", "#333542"));
        themes.put("card", cardTheme);
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        String dashboardId = workspace.createDashboard(displayName, layout, settings, themes);
        System.out.println(dashboardId);
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

    function createDashboard() {
        $display_name = "Sales Overview";
        // Each layout key is a card ID; the value is that card's configuration. layout travels as a JSON-encoded string.
        $layout = json_encode([
            "1" => ["type" => "USERFILTERS", "width" => 80, "height" => 3, "left" => 0, "top" => 0],
            "2" => ["type" => "HTML", "width" => 80, "height" => 5, "left" => 0, "top" => 3, "content" => "<b>Sales Dashboard</b>"],
            "3" => ["type" => "VIEW", "width" => 80, "height" => 20, "left" => 0, "top" => 8, "viewName" => "Sales Chart", "properties" => (object)[]]
        ]);
        $settings = ["allowDrillDown" => "true", "fitToWidth" => "true", "allowExport" => ["csv" => "true", "pdf" => "true"]];
        $themes = [
            "layoutType" => 2,
            "type" => "solid",
            "solid" => ["background" => "#333542"],
            "card" => [
                "background" => "#3E3F4D",
                "title" => ["border" => ["color" => "#6F738E"]],
                "border" => ["color" => "#6F738E", "width" => 2]
            ]
        ];
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $dashboard_id = $workspace->createDashboard($display_name, $layout, $settings, $themes);
        print_r($dashboard_id);
    }
}

$obj = new Test();
$obj->createDashboard();
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

    def create_dashboard(self, ac):
        display_name = "Sales Overview"
        # Each layout key is a card ID; the value is that card's configuration. layout travels as a JSON-encoded string.
        layout = json.dumps({
            "1": {"type": "USERFILTERS", "width": 80, "height": 3, "left": 0, "top": 0},
            "2": {"type": "HTML", "width": 80, "height": 5, "left": 0, "top": 3, "content": "<b>Sales Dashboard</b>"},
            "3": {"type": "VIEW", "width": 80, "height": 20, "left": 0, "top": 8, "viewName": "Sales Chart", "properties": {}}
        })
        settings = {"allowDrillDown": "true", "fitToWidth": "true", "allowExport": {"csv": "true", "pdf": "true"}}
        themes = {
            "layoutType": 2,
            "type": "solid",
            "solid": {"background": "#333542"},
            "card": {
                "background": "#3E3F4D",
                "title": {"border": {"color": "#6F738E"}},
                "border": {"color": "#6F738E", "width": 2}
            }
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        dashboard_id = workspace.create_dashboard(display_name, layout, settings, themes)
        print(dashboard_id)

obj = sample()
obj.create_dashboard(obj.ac)
```

## Node.js

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';

var displayName = 'Sales Overview';
// Each layout key is a card ID; the value is that card's configuration. layout travels as a JSON-encoded string.
var layout = JSON.stringify({
    '1': { type: 'USERFILTERS', width: 80, height: 3, left: 0, top: 0 },
    '2': { type: 'HTML', width: 80, height: 5, left: 0, top: 3, content: '<b>Sales Dashboard</b>' },
    '3': { type: 'VIEW', width: 80, height: 20, left: 0, top: 8, viewName: 'Sales Chart', properties: {} }
});
var settings = { allowDrillDown: 'true', fitToWidth: 'true', allowExport: { csv: 'true', pdf: 'true' } };
var themes = {
    layoutType: 2,
    type: 'solid',
    solid: { background: '#333542' },
    card: {
        background: '#3E3F4D',
        title: { border: { color: '#6F738E' } },
        border: { color: '#6F738E', width: 2 }
    }
};
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.createDashboard(displayName, layout, settings, themes).then((dashboardId) => { console.log(dashboardId); }).catch((error) => { console.log(error); });
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

  def create_dashboard
    display_name = "Sales Overview"
    # Each layout key is a card ID; the value is that card's configuration. layout travels as a JSON-encoded string.
    layout = JSON.generate({
      "1" => { "type" => "USERFILTERS", "width" => 80, "height" => 3, "left" => 0, "top" => 0 },
      "2" => { "type" => "HTML", "width" => 80, "height" => 5, "left" => 0, "top" => 3, "content" => "<b>Sales Dashboard</b>" },
      "3" => { "type" => "VIEW", "width" => 80, "height" => 20, "left" => 0, "top" => 8, "viewName" => "Sales Chart", "properties" => {} }
    })
    settings = { "allowDrillDown" => "true", "fitToWidth" => "true", "allowExport" => { "csv" => "true", "pdf" => "true" } }
    themes = {
      "layoutType" => 2,
      "type" => "solid",
      "solid" => { "background" => "#333542" },
      "card" => {
        "background" => "#3E3F4D",
        "title" => { "border" => { "color" => "#6F738E" } },
        "border" => { "color" => "#6F738E", "width" => 2 }
      }
    }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    dashboard_id = workspace.create_dashboard(display_name, layout, settings, themes)
    puts dashboard_id
  end
end

obj = Sample.new
obj.create_dashboard
```

## Deluge (Zoho scripting)

```deluge
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
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
htmlCard.put("content", "<b>Sales Dashboard</b>");
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
allowExport = Map();
allowExport.put("csv", "true");
allowExport.put("pdf", "true");
settings = Map();
settings.put("allowDrillDown", "true");
settings.put("fitToWidth", "true");
settings.put("allowExport", allowExport);
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
solidTheme.put("background", "#333542");
themes = Map();
themes.put("layoutType", 2);
themes.put("type", "solid");
themes.put("solid", solidTheme);
themes.put("card", cardTheme);
config = Map();
config.put("displayName", "Sales Overview");
config.put("layout", layout.toString()); // layout travels as a JSON-encoded string
config.put("settings", settings);
config.put("themes", themes);
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/dashboards"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Create Dashboard](../../../domains/reports-and-dashboards/dashboards/create-dashboard.md) - full endpoint reference.
- [Dashboards overview](../../../domains/reports-and-dashboards/dashboards/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
