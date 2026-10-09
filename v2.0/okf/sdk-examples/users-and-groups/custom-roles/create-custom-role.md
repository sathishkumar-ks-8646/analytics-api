---
type: SDK Example
title: SDK examples - Create Custom Role
description: Code samples in 9 languages for POST /restapi/v2/orgs/roles (createCustomRole).
resource: https://analyticsapi.zoho.com/restapi/v2/orgs/roles
tags:
  - zoho-analytics
  - sdk
  - code-sample
  - users-and-groups
  - custom-roles
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
  operation_id: createCustomRole
  method: POST
  path: "/restapi/v2/orgs/roles"
  endpoint_doc: "/domains/users-and-groups/custom-roles/create-custom-role.md"
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
    resource: "/references/openapi/user-groups-grouped-api.json"
    title: OpenAPI 3 specification - user-groups-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
  - id: endpoint-doc
    resource: "/domains/users-and-groups/custom-roles/create-custom-role.md"
    title: Endpoint reference - Create Custom Role
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

Code samples for [Create Custom Role](../../../domains/users-and-groups/custom-roles/create-custom-role.md) (`POST /restapi/v2/orgs/roles`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](../../../foundations/sdk-clients.md).

# Examples

## cURL

Variant 1:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/orgs/roles" \
  -X 'POST' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"roleName":"Dashboard Viewer","accessType":"ALL_DASHBOARDS","permissions":{"interactionPermissions":{"read":true,"vud":true,"drillDown":true,"insight":true},"sharePermissions":{"share":true,"discussion":true},"publishPermissions":{"export":true,"createSlideshow":true},"createPermissions":{"createFolder":true}}}'
```

Variant 2:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/orgs/roles" \
  -X 'POST' \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>' \
  --data-urlencode 'CONFIG={"roleName":"Data Engineer","accessType":"ALL_DATA_REPORTS_AND_DASHBOARDS","permissions":{"createPermissions":{"createTable":true,"createQueryTable":true,"createFolder":true,"createFormula":true},"dataPermissions":{"addRow":true,"modifyRow":true,"deleteRow":true,"importAppend":true,"importAddOrUpdate":true,"importDeleteAllAdd":true,"importDeleteUpdateAdd":true},"designPermissions":{"designModify":true},"interactionPermissions":{"read":true,"vud":true,"drillDown":true,"insight":true,"drillThrough":true,"drillActions":true},"sharePermissions":{"share":true,"discussion":true,"privateLinks":true,"accessAdminPresets":true,"createPreset":true},"publishPermissions":{"export":true,"manageEmailSchedules":true,"allEmailSchedulesAccess":true,"manageDataAlerts":true,"allDataAlertsAccess":true,"createSlideshow":true,"publicViews":true},"datasourcePermissions":{"viewDatasource":true,"editDatasource":true,"syncData":true,"useDatasource":true,"removeDatasource":true}}}'
```

## C#

Variant 1:

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

        public void CreateCustomRole(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            string roleName = "Dashboard Viewer";
            string accessType = "ALL_DASHBOARDS";
            Dictionary<string, object> permissions = new Dictionary<string, object>();
            Dictionary<string, object> interactionPermissions = new Dictionary<string, object>();
            interactionPermissions.Add("read", true);
            interactionPermissions.Add("vud", true);
            interactionPermissions.Add("drillDown", true);
            interactionPermissions.Add("insight", true);
            permissions.Add("interactionPermissions", interactionPermissions);
            Dictionary<string, object> sharePermissions = new Dictionary<string, object>();
            sharePermissions.Add("share", true);
            sharePermissions.Add("discussion", true);
            permissions.Add("sharePermissions", sharePermissions);
            Dictionary<string, object> publishPermissions = new Dictionary<string, object>();
            publishPermissions.Add("export", true);
            publishPermissions.Add("createSlideshow", true);
            permissions.Add("publishPermissions", publishPermissions);
            Dictionary<string, object> createPermissions = new Dictionary<string, object>();
            createPermissions.Add("createFolder", true);
            permissions.Add("createPermissions", createPermissions);
            string result = org.CreateCustomRole(roleName, accessType, permissions);
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
                obj.CreateCustomRole(ac);
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
using System.Text.Json;

namespace ZohoAnalyticsTest
{
    class Program
    {
        long orgId = 55522777;

        public void CreateCustomRole(IAnalyticsClient ac)
        {
            IOrgAPI org = ac.GetOrgInstance(orgId);
            string roleName = "Data Engineer";
            string accessType = "ALL_DATA_REPORTS_AND_DASHBOARDS";
            Dictionary<string, object> permissions = new Dictionary<string, object>();
            Dictionary<string, object> createPermissions = new Dictionary<string, object>();
            createPermissions.Add("createTable", true);
            createPermissions.Add("createQueryTable", true);
            createPermissions.Add("createFolder", true);
            createPermissions.Add("createFormula", true);
            permissions.Add("createPermissions", createPermissions);
            Dictionary<string, object> dataPermissions = new Dictionary<string, object>();
            dataPermissions.Add("addRow", true);
            dataPermissions.Add("modifyRow", true);
            dataPermissions.Add("deleteRow", true);
            dataPermissions.Add("importAppend", true);
            dataPermissions.Add("importAddOrUpdate", true);
            dataPermissions.Add("importDeleteAllAdd", true);
            dataPermissions.Add("importDeleteUpdateAdd", true);
            permissions.Add("dataPermissions", dataPermissions);
            Dictionary<string, object> designPermissions = new Dictionary<string, object>();
            designPermissions.Add("designModify", true);
            permissions.Add("designPermissions", designPermissions);
            Dictionary<string, object> interactionPermissions = new Dictionary<string, object>();
            interactionPermissions.Add("read", true);
            interactionPermissions.Add("vud", true);
            interactionPermissions.Add("drillDown", true);
            interactionPermissions.Add("insight", true);
            interactionPermissions.Add("drillThrough", true);
            interactionPermissions.Add("drillActions", true);
            permissions.Add("interactionPermissions", interactionPermissions);
            Dictionary<string, object> sharePermissions = new Dictionary<string, object>();
            sharePermissions.Add("share", true);
            sharePermissions.Add("discussion", true);
            sharePermissions.Add("privateLinks", true);
            sharePermissions.Add("accessAdminPresets", true);
            sharePermissions.Add("createPreset", true);
            permissions.Add("sharePermissions", sharePermissions);
            Dictionary<string, object> publishPermissions = new Dictionary<string, object>();
            publishPermissions.Add("export", true);
            publishPermissions.Add("manageEmailSchedules", true);
            publishPermissions.Add("allEmailSchedulesAccess", true);
            publishPermissions.Add("manageDataAlerts", true);
            publishPermissions.Add("allDataAlertsAccess", true);
            publishPermissions.Add("createSlideshow", true);
            publishPermissions.Add("publicViews", true);
            permissions.Add("publishPermissions", publishPermissions);
            Dictionary<string, object> datasourcePermissions = new Dictionary<string, object>();
            datasourcePermissions.Add("viewDatasource", true);
            datasourcePermissions.Add("editDatasource", true);
            datasourcePermissions.Add("syncData", true);
            datasourcePermissions.Add("useDatasource", true);
            datasourcePermissions.Add("removeDatasource", true);
            permissions.Add("datasourcePermissions", datasourcePermissions);
            string result = org.CreateCustomRole(roleName, accessType, permissions);
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
                obj.CreateCustomRole(ac);
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
)

func CreateCustomRole(ac ZAnalytics.Client) {
    org := ZAnalytics.GetOrgInstance(&ac, orgId)
    roleName := "Dashboard Viewer"
    accessType := "ALL_DASHBOARDS"
    permissions := map[string]interface{}{
        "interactionPermissions": map[string]interface{}{"read": true, "vud": true, "drillDown": true, "insight": true},
        "sharePermissions": map[string]interface{}{"share": true, "discussion": true},
        "publishPermissions": map[string]interface{}{"export": true, "createSlideshow": true},
        "createPermissions": map[string]interface{}{"createFolder": true},
    }
    result, _ := org.CreateCustomRole(roleName, accessType, permissions)
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateCustomRole(ac)
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
)

func CreateCustomRole(ac ZAnalytics.Client) {
    org := ZAnalytics.GetOrgInstance(&ac, orgId)
    roleName := "Data Engineer"
    accessType := "ALL_DATA_REPORTS_AND_DASHBOARDS"
    permissions := map[string]interface{}{
        "createPermissions": map[string]interface{}{"createTable": true, "createQueryTable": true, "createFolder": true, "createFormula": true},
        "dataPermissions": map[string]interface{}{"addRow": true, "modifyRow": true, "deleteRow": true, "importAppend": true, "importAddOrUpdate": true, "importDeleteAllAdd": true, "importDeleteUpdateAdd": true},
        "designPermissions": map[string]interface{}{"designModify": true},
        "interactionPermissions": map[string]interface{}{"read": true, "vud": true, "drillDown": true, "insight": true, "drillThrough": true, "drillActions": true},
        "sharePermissions": map[string]interface{}{"share": true, "discussion": true, "privateLinks": true, "accessAdminPresets": true, "createPreset": true},
        "publishPermissions": map[string]interface{}{"export": true, "manageEmailSchedules": true, "allEmailSchedulesAccess": true, "manageDataAlerts": true, "allDataAlertsAccess": true, "createSlideshow": true, "publicViews": true},
        "datasourcePermissions": map[string]interface{}{"viewDatasource": true, "editDatasource": true, "syncData": true, "useDatasource": true, "removeDatasource": true},
    }
    result, _ := org.CreateCustomRole(roleName, accessType, permissions)
    fmt.Println(result)
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    CreateCustomRole(ac)
}
```

## Java

Variant 1:

```java
import com.zoho.analytics.client.*;
import org.json.*;

public class Test {

    private long orgId = 55522777l;

    public static void main(String args[]) {
        String clientId = "1000.xxxxxxx";
        String clientSecret = "xxxxxxx";
        String refreshToken = "1000.xxxxxxx.xxxxxxx";

        Test tObj = new Test();
        AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);

        try {
            tObj.createCustomRole(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void createCustomRole(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        String roleName = "Dashboard Viewer";
        String accessType = "ALL_DASHBOARDS";
        JSONObject permissions = new JSONObject();
        JSONObject interactionPermissions = new JSONObject();
        interactionPermissions.put("read", true);
        interactionPermissions.put("vud", true);
        interactionPermissions.put("drillDown", true);
        interactionPermissions.put("insight", true);
        permissions.put("interactionPermissions", interactionPermissions);
        JSONObject sharePermissions = new JSONObject();
        sharePermissions.put("share", true);
        sharePermissions.put("discussion", true);
        permissions.put("sharePermissions", sharePermissions);
        JSONObject publishPermissions = new JSONObject();
        publishPermissions.put("export", true);
        publishPermissions.put("createSlideshow", true);
        permissions.put("publishPermissions", publishPermissions);
        JSONObject createPermissions = new JSONObject();
        createPermissions.put("createFolder", true);
        permissions.put("createPermissions", createPermissions);
        String result = org.createCustomRole(roleName, accessType, permissions);
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

    public static void main(String args[]) {
        String clientId = "1000.xxxxxxx";
        String clientSecret = "xxxxxxx";
        String refreshToken = "1000.xxxxxxx.xxxxxxx";

        Test tObj = new Test();
        AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);

        try {
            tObj.createCustomRole(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void createCustomRole(AnalyticsClient ac) throws Exception {
        OrgAPI org = ac.getOrgInstance(orgId);
        String roleName = "Data Engineer";
        String accessType = "ALL_DATA_REPORTS_AND_DASHBOARDS";
        JSONObject permissions = new JSONObject();
        JSONObject createPermissions = new JSONObject();
        createPermissions.put("createTable", true);
        createPermissions.put("createQueryTable", true);
        createPermissions.put("createFolder", true);
        createPermissions.put("createFormula", true);
        permissions.put("createPermissions", createPermissions);
        JSONObject dataPermissions = new JSONObject();
        dataPermissions.put("addRow", true);
        dataPermissions.put("modifyRow", true);
        dataPermissions.put("deleteRow", true);
        dataPermissions.put("importAppend", true);
        dataPermissions.put("importAddOrUpdate", true);
        dataPermissions.put("importDeleteAllAdd", true);
        dataPermissions.put("importDeleteUpdateAdd", true);
        permissions.put("dataPermissions", dataPermissions);
        JSONObject designPermissions = new JSONObject();
        designPermissions.put("designModify", true);
        permissions.put("designPermissions", designPermissions);
        JSONObject interactionPermissions = new JSONObject();
        interactionPermissions.put("read", true);
        interactionPermissions.put("vud", true);
        interactionPermissions.put("drillDown", true);
        interactionPermissions.put("insight", true);
        interactionPermissions.put("drillThrough", true);
        interactionPermissions.put("drillActions", true);
        permissions.put("interactionPermissions", interactionPermissions);
        JSONObject sharePermissions = new JSONObject();
        sharePermissions.put("share", true);
        sharePermissions.put("discussion", true);
        sharePermissions.put("privateLinks", true);
        sharePermissions.put("accessAdminPresets", true);
        sharePermissions.put("createPreset", true);
        permissions.put("sharePermissions", sharePermissions);
        JSONObject publishPermissions = new JSONObject();
        publishPermissions.put("export", true);
        publishPermissions.put("manageEmailSchedules", true);
        publishPermissions.put("allEmailSchedulesAccess", true);
        publishPermissions.put("manageDataAlerts", true);
        publishPermissions.put("allDataAlertsAccess", true);
        publishPermissions.put("createSlideshow", true);
        publishPermissions.put("publicViews", true);
        permissions.put("publishPermissions", publishPermissions);
        JSONObject datasourcePermissions = new JSONObject();
        datasourcePermissions.put("viewDatasource", true);
        datasourcePermissions.put("editDatasource", true);
        datasourcePermissions.put("syncData", true);
        datasourcePermissions.put("useDatasource", true);
        datasourcePermissions.put("removeDatasource", true);
        permissions.put("datasourcePermissions", datasourcePermissions);
        String result = org.createCustomRole(roleName, accessType, permissions);
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

        function __construct() {
            $this->ac = new AnalyticsClient($this->client_id, $this->client_secret, $this->refresh_token);
        }

        function createCustomRole() {
            $org = $this->ac->getOrgInstance($this->org_id);
            $role_name = "Dashboard Viewer";
            $access_type = "ALL_DASHBOARDS";
            $permissions = array(
                "interactionPermissions" => array("read" => true, "vud" => true, "drillDown" => true, "insight" => true),
                "sharePermissions" => array("share" => true, "discussion" => true),
                "publishPermissions" => array("export" => true, "createSlideshow" => true),
                "createPermissions" => array("createFolder" => true)
            );
            $response = $org->createCustomRole($role_name, $access_type, $permissions);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->createCustomRole();
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

        function __construct() {
            $this->ac = new AnalyticsClient($this->client_id, $this->client_secret, $this->refresh_token);
        }

        function createCustomRole() {
            $org = $this->ac->getOrgInstance($this->org_id);
            $role_name = "Data Engineer";
            $access_type = "ALL_DATA_REPORTS_AND_DASHBOARDS";
            $permissions = array(
                "createPermissions" => array("createTable" => true, "createQueryTable" => true, "createFolder" => true, "createFormula" => true),
                "dataPermissions" => array("addRow" => true, "modifyRow" => true, "deleteRow" => true, "importAppend" => true, "importAddOrUpdate" => true, "importDeleteAllAdd" => true, "importDeleteUpdateAdd" => true),
                "designPermissions" => array("designModify" => true),
                "interactionPermissions" => array("read" => true, "vud" => true, "drillDown" => true, "insight" => true, "drillThrough" => true, "drillActions" => true),
                "sharePermissions" => array("share" => true, "discussion" => true, "privateLinks" => true, "accessAdminPresets" => true, "createPreset" => true),
                "publishPermissions" => array("export" => true, "manageEmailSchedules" => true, "allEmailSchedulesAccess" => true, "manageDataAlerts" => true, "allDataAlertsAccess" => true, "createSlideshow" => true, "publicViews" => true),
                "datasourcePermissions" => array("viewDatasource" => true, "editDatasource" => true, "syncData" => true, "useDatasource" => true, "removeDatasource" => true)
            );
            $response = $org->createCustomRole($role_name, $access_type, $permissions);
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->createCustomRole();
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
import sys

class Config:
    CLIENTID = "1000.xxxxxxx"
    CLIENTSECRET = "xxxxxxx"
    REFRESHTOKEN = "1000.xxxxxxx.xxxxxxx"
    ORGID = "55522777"

class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def create_custom_role(self, ac):
        org = ac.get_org_instance(Config.ORGID)
        role_name = "Dashboard Viewer"
        access_type = "ALL_DASHBOARDS"
        permissions = {
            "interactionPermissions": {"read": True, "vud": True, "drillDown": True, "insight": True},
            "sharePermissions": {"share": True, "discussion": True},
            "publishPermissions": {"export": True, "createSlideshow": True},
            "createPermissions": {"createFolder": True}
        }
        result = org.create_custom_role(role_name, access_type, permissions)
        print(result)

try:
    obj = sample()
    obj.create_custom_role(obj.ac)
except Exception as e:
    print(str(e))
```

Variant 2:

```python
from AnalyticsClient import AnalyticsClient
import sys

class Config:
    CLIENTID = "1000.xxxxxxx"
    CLIENTSECRET = "xxxxxxx"
    REFRESHTOKEN = "1000.xxxxxxx.xxxxxxx"
    ORGID = "55522777"

class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def create_custom_role(self, ac):
        org = ac.get_org_instance(Config.ORGID)
        role_name = "Data Engineer"
        access_type = "ALL_DATA_REPORTS_AND_DASHBOARDS"
        permissions = {
            "createPermissions": {"createTable": True, "createQueryTable": True, "createFolder": True, "createFormula": True},
            "dataPermissions": {"addRow": True, "modifyRow": True, "deleteRow": True, "importAppend": True, "importAddOrUpdate": True, "importDeleteAllAdd": True, "importDeleteUpdateAdd": True},
            "designPermissions": {"designModify": True},
            "interactionPermissions": {"read": True, "vud": True, "drillDown": True, "insight": True, "drillThrough": True, "drillActions": True},
            "sharePermissions": {"share": True, "discussion": True, "privateLinks": True, "accessAdminPresets": True, "createPreset": True},
            "publishPermissions": {"export": True, "manageEmailSchedules": True, "allEmailSchedulesAccess": True, "manageDataAlerts": True, "allDataAlertsAccess": True, "createSlideshow": True, "publicViews": True},
            "datasourcePermissions": {"viewDatasource": True, "editDatasource": True, "syncData": True, "useDatasource": True, "removeDatasource": True}
        }
        result = org.create_custom_role(role_name, access_type, permissions)
        print(result)

try:
    obj = sample()
    obj.create_custom_role(obj.ac)
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

var ac = new analyticsClient(clientId, clientSecret, refreshToken);

var org = ac.getOrgInstance(orgId);
var roleName = 'Dashboard Viewer';
var accessType = 'ALL_DASHBOARDS';
var permissions = {
    interactionPermissions: {read: true, vud: true, drillDown: true, insight: true},
    sharePermissions: {share: true, discussion: true},
    publishPermissions: {export: true, createSlideshow: true},
    createPermissions: {createFolder: true}
};

org.createCustomRole(roleName, accessType, permissions).then(function (result) {
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

var ac = new analyticsClient(clientId, clientSecret, refreshToken);

var org = ac.getOrgInstance(orgId);
var roleName = 'Data Engineer';
var accessType = 'ALL_DATA_REPORTS_AND_DASHBOARDS';
var permissions = {
    createPermissions: {createTable: true, createQueryTable: true, createFolder: true, createFormula: true},
    dataPermissions: {addRow: true, modifyRow: true, deleteRow: true, importAppend: true, importAddOrUpdate: true, importDeleteAllAdd: true, importDeleteUpdateAdd: true},
    designPermissions: {designModify: true},
    interactionPermissions: {read: true, vud: true, drillDown: true, insight: true, drillThrough: true, drillActions: true},
    sharePermissions: {share: true, discussion: true, privateLinks: true, accessAdminPresets: true, createPreset: true},
    publishPermissions: {export: true, manageEmailSchedules: true, allEmailSchedulesAccess: true, manageDataAlerts: true, allDataAlertsAccess: true, createSlideshow: true, publicViews: true},
    datasourcePermissions: {viewDatasource: true, editDatasource: true, syncData: true, useDatasource: true, removeDatasource: true}
};

org.createCustomRole(roleName, accessType, permissions).then(function (result) {
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

  def create_custom_role
    org = @ac.get_org_instance(Config::ORGID)
    role_name = "Dashboard Viewer"
    access_type = "ALL_DASHBOARDS"
    permissions = {
      "interactionPermissions" => {"read" => true, "vud" => true, "drillDown" => true, "insight" => true},
      "sharePermissions" => {"share" => true, "discussion" => true},
      "publishPermissions" => {"export" => true, "createSlideshow" => true},
      "createPermissions" => {"createFolder" => true}
    }
    result = org.create_custom_role(role_name, access_type, permissions)
    puts result
  end
end

begin
  obj = Sample.new
  obj.create_custom_role
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

  def create_custom_role
    org = @ac.get_org_instance(Config::ORGID)
    role_name = "Data Engineer"
    access_type = "ALL_DATA_REPORTS_AND_DASHBOARDS"
    permissions = {
      "createPermissions" => {"createTable" => true, "createQueryTable" => true, "createFolder" => true, "createFormula" => true},
      "dataPermissions" => {"addRow" => true, "modifyRow" => true, "deleteRow" => true, "importAppend" => true, "importAddOrUpdate" => true, "importDeleteAllAdd" => true, "importDeleteUpdateAdd" => true},
      "designPermissions" => {"designModify" => true},
      "interactionPermissions" => {"read" => true, "vud" => true, "drillDown" => true, "insight" => true, "drillThrough" => true, "drillActions" => true},
      "sharePermissions" => {"share" => true, "discussion" => true, "privateLinks" => true, "accessAdminPresets" => true, "createPreset" => true},
      "publishPermissions" => {"export" => true, "manageEmailSchedules" => true, "allEmailSchedulesAccess" => true, "manageDataAlerts" => true, "allDataAlertsAccess" => true, "createSlideshow" => true, "publicViews" => true},
      "datasourcePermissions" => {"viewDatasource" => true, "editDatasource" => true, "syncData" => true, "useDatasource" => true, "removeDatasource" => true}
    }
    result = org.create_custom_role(role_name, access_type, permissions)
    puts result
  end
end

begin
  obj = Sample.new
  obj.create_custom_role
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
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"roleName":"Dashboard Viewer","accessType":"ALL_DASHBOARDS","permissions":{"interactionPermissions":{"read":true,"vud":true,"drillDown":true,"insight":true},"sharePermissions":{"share":true,"discussion":true},"publishPermissions":{"export":true,"createSlideshow":true},"createPermissions":{"createFolder":true}}};
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/orgs/roles"
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
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = {"roleName":"Data Engineer","accessType":"ALL_DATA_REPORTS_AND_DASHBOARDS","permissions":{"createPermissions":{"createTable":true,"createQueryTable":true,"createFolder":true,"createFormula":true},"dataPermissions":{"addRow":true,"modifyRow":true,"deleteRow":true,"importAppend":true,"importAddOrUpdate":true,"importDeleteAllAdd":true,"importDeleteUpdateAdd":true},"designPermissions":{"designModify":true},"interactionPermissions":{"read":true,"vud":true,"drillDown":true,"insight":true,"drillThrough":true,"drillActions":true},"sharePermissions":{"share":true,"discussion":true,"privateLinks":true,"accessAdminPresets":true,"createPreset":true},"publishPermissions":{"export":true,"manageEmailSchedules":true,"allEmailSchedulesAccess":true,"manageDataAlerts":true,"allDataAlertsAccess":true,"createSlideshow":true,"publicViews":true},"datasourcePermissions":{"viewDatasource":true,"editDatasource":true,"syncData":true,"useDatasource":true,"removeDatasource":true}}};
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/orgs/roles"
  type :POST
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

# Related

- [Create Custom Role](../../../domains/users-and-groups/custom-roles/create-custom-role.md) - full endpoint reference.
- [Custom Roles overview](../../../domains/users-and-groups/custom-roles/overview.md).
- [SDK clients](../../../foundations/sdk-clients.md).
