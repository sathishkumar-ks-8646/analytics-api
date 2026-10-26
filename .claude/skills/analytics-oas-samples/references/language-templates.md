# SDK snippet templates — all nine languages

Copy-ready skeletons, taken verbatim from the shapes already in
`v2.0/zenesis-oas-samples/`. Substitute the operation name, the URL tail, the CONFIG fields and the
path IDs; leave everything else — imports, client construction, error handling, the illustrative
values — exactly as it is.

**House values** (never change these):

```
clientId      1000.xxxxxxx          orgId        55522777
clientSecret  xxxxxxx               workspaceId  35130000001055707
refreshToken  1000.xxxxxxx.xxxxxxx  viewId       35130000001055717
base URL      https://analyticsapi.zoho.com
```

**Two per-file cURL conventions exist. Match the neighbouring snippets in the same file:**

| | Resolved IDs (most files) | Angle placeholders (`user-groups`, `workspace-management`) |
|---|---|---|
| URL | `/workspaces/35130000001055707/querytables` | `/workspaces/<workspace-id>/secretkey` |
| Layout | usually one long line | usually `\` continuations, one header per line |

The SDK snippets are uniform across all files — only cURL varies.

JSON reminder: these go into the file as a **single `code` string** — newlines as `\n`, inner double
quotes escaped as `\"`.

---

# A. GET with no CONFIG — `GET /restapi/v2/workspaces/{workspace-id}/querytables`

## Curl

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/querytables" -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>'
```

One line. `-X 'GET'` is omitted (it is the default); every other method states `-X`.

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

        public void GetQueryTables(IAnalyticsClient ac)
        {
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            var result = workspace.GetQueryTables(null);
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
                obj.GetQueryTables(ac);
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

`using System.Text.Json;` is added only when the snippet serialises a CONFIG.

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
)

func GetQueryTables(ac ZAnalytics.Client) {
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.GetQueryTables(nil)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}

func main() {
    ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)
    GetQueryTables(ac)
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
            tObj.getQueryTables(ac);
        }
        catch (ServerException ex) {
            System.out.println("Server exception - ErrorCode : " + ex.getErrorCode() + ", ErrorMessage : " + ex.getErrorMessage());
        }
        catch (Exception ex) {
            System.out.println("Other exception - ");
            ex.printStackTrace();
        }
    }

    public void getQueryTables(AnalyticsClient ac) throws Exception {
        WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
        JSONObject result = workspace.getQueryTables(null);
        System.out.println(result);
    }
}
```

`long` literals carry the `l` suffix. A list-returning call uses `JSONArray`.

## Php

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

        function getQueryTables() {
            $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
            $response = $workspace->getQueryTables();
            print_r($response);
        }
    }

    $test_obj = new Test();

    try {
        $test_obj->getQueryTables();
    }
    catch(ServerException $se) {
        echo "Server exception : " . $se->getErrorMessage() . "\n";
    }
    catch(Exception $e) {
        echo "Exception : " . $e->getMessage() . "\n";
    }
?>
```

Method names are camelCase; local variables are `$snake_case`.

## Python

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

    def get_query_tables(self, ac):
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.get_query_tables()
        print(result)

try:
    obj = sample()
    obj.get_query_tables(obj.ac)
except Exception as e:
    print(str(e))
```

Add `VIEWID = "35130000001055717"` to `Config` for view-scoped calls. Some snippets call the method
directly (`obj.update_email_schedule(obj.ac)`) without the `try` wrapper — both shapes exist; copy
the neighbour.

## Node

```javascript
var analyticsClient = require('./AnalyticsClient');

var clientId = '1000.xxxxxxx';
var clientSecret = 'xxxxxxx';
var refreshToken = '1000.xxxxxxx.xxxxxxx';
var orgId = '55522777';
var workspaceId = '35130000001055707';

var ac = new analyticsClient(clientId, clientSecret, refreshToken);


var workspace = ac.getWorkspaceInstance(orgId, workspaceId);

workspace.getQueryTables().then(function (result) {
    console.log(result);
}).catch(function (err) {
    console.log(err);
});
```

Single quotes throughout. Arrow callbacks also appear
(`.then((result) => { console.log(result); })`) — copy the neighbour.

## Ruby

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

  def get_query_tables
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.get_query_tables()
    puts result
  end
end

begin
  obj = Sample.new
  obj.get_query_tables
rescue ServerError => e
  puts "Server Error: #{e.response_content}"
rescue StandardError => e
  puts e.message
  puts e.backtrace.join("\n")
end
```

The builder chain (`.with_data_center("US").with_oauth({…}).build`) is mandatory — Ruby is the only
client that takes a data centre.

## Deluge

```javascript
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/querytables"
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

Exact spacing matters to match the neighbours: `url :` and `type :` have a space before the colon;
`headers:`, `parameters:`, `files:`, `connection:` do not. The URL is built by concatenation so the
IDs are visible. `connection:"analytics_oauth_connection"` is always the last entry.

---

# B. GET with a CONFIG query parameter

Only cURL and Deluge change — the SDKs take the CONFIG as an argument.

## Curl

The CONFIG is **percent-encoded inline in the URL query string** — not `-G --data-urlencode`:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/querytables?CONFIG=%7B%22keyword%22%3A%22Sales%22%2C%22startIndex%22%3A11%2C%22noOfResult%22%3A10%7D" \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>'
```

`{` → `%7B`, `}` → `%7D`, `"` → `%22`, `:` → `%3A`, `,` → `%2C`, `[` → `%5B`, `]` → `%5D`,
space → `%20`. A file download adds `-o <name>.<ext>` as the last argument.

The same endpoint in `workspace-management` style, which uses angle placeholders instead of resolved
IDs:

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/<workspace-id>/secretkey?CONFIG=%7B%22regenerateKey%22%3Afalse%7D" \
  -H 'ZANALYTICS-ORGID: <org-id>' \
  -H 'Authorization: Zoho-oauthtoken <access_token>'
```

## Deluge

```javascript
orgId = "55522777";
workspaceId = "35130000001055707";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
config = Map();
config.put("keyword", "Sales");
config.put("startIndex", 11);
config.put("noOfResult", 10);
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/querytables?CONFIG=" + zoho.encryption.urlEncode(config.toString())
  type :GET
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

`zoho.encryption.urlEncode` is required on GET — the server rejects an unencoded CONFIG.

## SDKs

Pass the CONFIG as the trailing argument:

```python
config = { "keyword": "Sales", "startIndex": 11, "noOfResult": 10 }
result = workspace.get_query_tables(config)
```

```java
JSONObject config = new JSONObject();
config.put("keyword", "Sales");
JSONObject result = workspace.getQueryTables(config);
```

```go
config := map[string]interface{}{ "keyword": "Sales" }
result, exception := workspace.GetQueryTables(config)
```

---

# C. POST / PUT / DELETE with a form CONFIG — `PUT …/emailschedules/{schedule-id}`

## Curl

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/emailschedules/35130000001056601" -X 'PUT' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={"scheduleName":"Monthly Sales Report","scheduleDetails":{"calendarFrequency":"monthly","hour":8,"minute":30,"monthDay":1},"subject":"Monthly Sales Report"}'
```

`-X` is explicit. The CONFIG JSON is compact — no spaces after `:` or `,`.

## Python

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

    def update_email_schedule(self, ac):
        schedule_id = "35130000001056601"
        schedule_details = {
            "calendarFrequency": "monthly",
            "hour": 8,
            "minute": 30,
            "monthDay": 1
        }
        config = {
            "scheduleName": "Monthly Sales Report",
            "scheduleDetails": schedule_details,
            "subject": "Monthly Sales Report"
        }
        workspace = ac.get_workspace_instance(Config.ORGID, Config.WORKSPACEID)
        result = workspace.update_email_schedule(schedule_id, config)
        print(result)

obj = sample()
obj.update_email_schedule(obj.ac)
```

Nested JSONObjects are built as named locals first (`schedule_details`), then referenced — never
inlined. The path ID is a local, not in `Config`.

## C#

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

        public void UpdateEmailSchedule(IAnalyticsClient ac)
        {
            long scheduleId = 35130000001056601L;
            Dictionary<string, object> scheduleDetails = new Dictionary<string, object>();
            scheduleDetails.Add("calendarFrequency", "monthly");
            scheduleDetails.Add("hour", 8);
            scheduleDetails.Add("minute", 30);
            scheduleDetails.Add("monthDay", 1);
            Dictionary<string, object> config = new Dictionary<string, object>();
            config.Add("scheduleName", "Monthly Sales Report");
            config.Add("scheduleDetails", scheduleDetails);
            config.Add("subject", "Monthly Sales Report");
            IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
            var result = workspace.UpdateEmailSchedule(scheduleId, config);
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
                obj.UpdateEmailSchedule(ac);
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

`Dictionary<string, object>` with `.Add(...)` per key — never a collection initialiser.

## Go

```go
func UpdateEmailSchedule(ac ZAnalytics.Client) {
    scheduleid := "35130000001056601"
    scheduledetails := map[string]interface{}{
        "calendarFrequency": "monthly",
        "hour": 8,
        "minute": 30,
        "monthDay": 1,
    }
    config := map[string]interface{}{
        "scheduleName": "Monthly Sales Report",
        "scheduleDetails": scheduledetails,
        "subject": "Monthly Sales Report",
    }
    workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
    result, exception := workspace.UpdateEmailSchedule(scheduleid, config)
    if exception != nil {
        fmt.Println(exception.ErrorMessage)
    } else {
        fmt.Println(result)
    }
}
```

Go locals are all-lower-case (`scheduleid`, `scheduledetails`), unlike the exported function name.

## Java

```java
public void updateEmailSchedule(AnalyticsClient ac) throws Exception {
    long scheduleId = 35130000001056601l;
    JSONObject scheduleDetails = new JSONObject();
    scheduleDetails.put("calendarFrequency", "monthly");
    scheduleDetails.put("hour", 8);
    scheduleDetails.put("minute", 30);
    scheduleDetails.put("monthDay", 1);
    JSONObject config = new JSONObject();
    config.put("scheduleName", "Monthly Sales Report");
    config.put("scheduleDetails", scheduleDetails);
    config.put("subject", "Monthly Sales Report");
    WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    JSONObject result = workspace.updateEmailSchedule(scheduleId, config);
    System.out.println(result);
}
```

## Php

```php
    function updateEmailSchedule() {
        $schedule_id = "35130000001056601";
        $schedule_details = array(
            "calendarFrequency" => "monthly",
            "hour" => 8,
            "minute" => 30,
            "monthDay" => 1
        );
        $config = array(
            "scheduleName" => "Monthly Sales Report",
            "scheduleDetails" => $schedule_details,
            "subject" => "Monthly Sales Report"
        );
        $workspace = $this->ac->getWorkspaceInstance($this->org_id, $this->workspace_id);
        $response = $workspace->updateEmailSchedule($schedule_id, $config);
        print_r($response);
    }
```

`array(...)` with `=>`, never `[...]`.

## Node

```javascript
var analyticsClient = require('./AnalyticsClient');
var ac = new analyticsClient('1000.xxxxxxx', 'xxxxxxx', '1000.xxxxxxx.xxxxxxx');
var orgId = '55522777';
var workspaceId = '35130000001055707';
var scheduleId = '35130000001056601';

var scheduleDetails = { calendarFrequency: 'monthly', hour: 8, minute: 30, monthDay: 1 };
var config = { scheduleName: 'Monthly Sales Report', scheduleDetails: scheduleDetails, subject: 'Monthly Sales Report' };

var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
workspace.updateEmailSchedule(scheduleId, config).then((result) => { console.log(result); }).catch((error) => { console.log(error); });
```

Object literals are single-line; keys unquoted.

## Ruby

```ruby
  def update_email_schedule
    schedule_id = "35130000001056601"
    schedule_details = { "calendarFrequency" => "monthly", "hour" => 8, "minute" => 30, "monthDay" => 1 }
    config = { "scheduleName" => "Monthly Sales Report", "scheduleDetails" => schedule_details, "subject" => "Monthly Sales Report" }
    workspace = @ac.get_workspace_instance(Config::ORGID, Config::WORKSPACEID)
    result = workspace.update_email_schedule(schedule_id, config)
    puts result
  end
```

Hash keys are **strings** with `=>`, never symbols.

## Deluge

```javascript
orgId = "55522777";
workspaceId = "35130000001055707";
scheduleId = "35130000001056601";
headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
scheduleDetails = Map();
scheduleDetails.put("calendarFrequency", "monthly");
scheduleDetails.put("hour", 8);
scheduleDetails.put("minute", 30);
scheduleDetails.put("monthDay", 1);
config = Map();
config.put("scheduleName", "Monthly Sales Report");
config.put("scheduleDetails", scheduleDetails);
config.put("subject", "Monthly Sales Report");
parameters = "CONFIG=" + zoho.encryption.urlEncode(config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/emailschedules/" + scheduleId
  type :PUT
  parameters:parameters
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

A body CONFIG goes into `parameters` as an encoded **string**. Arrays are `List()` with `.add(...)`.

---

# D. Multipart import — `POST /restapi/v2/workspaces/{workspace-id}/data`

## Curl

```bash
curl "https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/data" -X 'POST' -H 'ZANALYTICS-ORGID: 55522777' -H 'Authorization: Zoho-oauthtoken <access_token>' -F 'FILE=@/home/local/Sales.csv' -F 'CONFIG={"tableName":"Sales","fileType":"csv","autoIdentify":true,"onError":"skiprow"}'
```

`-F` per part, `@` for the file.

## Python

```python
    def import_data_in_new_table(self, ac):
        config = {}
        config["onError"] = "skiprow"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        result = bulk.import_data_in_new_table("Sales", "csv", True, "/home/local/Sales.csv", config)
        print(result)
```

Imports and exports use `get_bulk_instance`, not `get_workspace_instance`, and the SDK takes the
well-known CONFIG fields as positional arguments with the remainder in `config`.

## Deluge

```javascript
orgId = "55522777";
workspaceId = "35130000001055707";

headersMap = Map();
headersMap.put("ZANALYTICS-ORGID", orgId);
fileObj = invokeurl
[
  url :"https://www.zylker.com/files/Sales.csv"
  type :GET
];
config = Map();
config.put("tableName", "Sales");
config.put("fileType", "csv");
config.put("autoIdentify", true);
config.put("onError", "skiprow");
parametersMap = Map();
parametersMap.put("CONFIG", config.toString());
response = invokeurl
[
  url :"https://analyticsapi.zoho.com/restapi/v2/workspaces/" + workspaceId + "/data"
  type :POST
  parameters:parametersMap
  files:fileObj
  headers:headersMap
  connection:"analytics_oauth_connection"
];
info response;
```

Deluge has no local filesystem: the file is fetched with a first `invokeurl` and passed as `files:`.
Here `parameters` is a **Map**, not an encoded string, because the request is multipart.

## Two variants

When the markdown documents both `FILE` and `DATA`, give the language two snippets:

```jsonc
"Curl": { "snippets": [
  { "code": "curl … -F 'FILE=@/home/local/Sales.csv' -F 'CONFIG={…}'" },
  { "code": "curl … -F 'DATA=Region,Sales\\nEast,100' -F 'CONFIG={…}'" }
] }
```

They render as numbered variants under the language heading. Keep the variants parallel across all
nine languages, or none.
