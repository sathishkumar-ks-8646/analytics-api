"""Per-language profiles: naming, construction, error surface and code snippets.

Snippets are kept verbatim-close to the verified sample programs under
`<lang>/sample/`, so the documentation and the shipped samples agree.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Lang:
    key: str
    name: str
    fence: str          # markdown code-fence language
    source: str         # path (relative to v2/) of the SDK source
    sample: str         # path of the sample program
    naming: str         # how method names are cased
    id_type: str        # how identifiers are typed
    error_type: str     # the exception/error surface, one line
    install: str        # markdown
    snippets: dict[str, str] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)


# ---------------------------------------------------------------- Java

JAVA = Lang(
    key="java", name="Java", fence="java",
    source="java/source/com/zoho/analytics/client",
    sample="java/sample/test/Test.java",
    naming="`camelCase`, matching the endpoint title.",
    id_type="`long`. Organization, workspace and view ids are numeric literals with an `l` suffix.",
    error_type="`ServerException` (`getErrorCode()`, `getErrorMessage()`) and `ParseException` (`getResponseMessage()`).",
    install="""Add the SDK sources under `com/zoho/analytics/client` to your project and put
these on the classpath:

| Dependency | Why |
|---|---|
| `org.json` (for example `json-20231013.jar`) | Every request config and response is a `JSONObject` / `JSONArray`. |
| Apache Commons CSV (`zr-csv.jar`) | Used by the batched CSV import path. |

```bash
javac -cp json-20231013.jar:zr-csv.jar -sourcepath source -d out sample/test/Test.java
```""",
    snippets={
        "construct": """import com.zoho.analytics.client.*;
import org.json.JSONObject;
import org.json.JSONArray;

String clientId     = "1000.xxxxxxx";
String clientSecret = "xxxxxxx";
String refreshToken = "1000.xxxxxxx.xxxxxxx";

AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);""",
        "singleton": """public final class Analytics {

    // One client for the whole process. The access token it holds is reused
    // across every call and refreshed in place when it expires.
    private static final AnalyticsClient CLIENT =
            new AnalyticsClient(System.getenv("ZOHO_CLIENT_ID"),
                                System.getenv("ZOHO_CLIENT_SECRET"),
                                System.getenv("ZOHO_REFRESH_TOKEN"));

    private Analytics() { }

    public static AnalyticsClient get() {
        return CLIENT;
    }
}

// Everywhere else in the application:
WorkspaceAPI workspace = Analytics.get().getWorkspaceInstance(orgId, workspaceId);""",
        "instances": """OrgAPI       org       = ac.getOrgInstance(orgId);
WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
ViewAPI      view      = ac.getViewInstance(orgId, workspaceId, viewId);
BulkAPI      bulk      = ac.getBulkInstance(orgId, workspaceId);""",
        "first_call": """AnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);

try {
    JSONArray orgs = ac.getOrgs();
    System.out.println(orgs);
}
catch (ServerException ex) {
    System.out.println("Server error " + ex.getErrorCode() + ": " + ex.getErrorMessage());
}
catch (ParseException ex) {
    System.out.println("Could not parse response: " + ex.getResponseMessage());
}""",
        "errors": """try {
    WorkspaceAPI workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    JSONArray views = workspace.getViews(null);
    System.out.println(views);
}
catch (ServerException ex) {
    // ex.getErrorCode() is the stable value to branch on.
    switch ((int) ex.getErrorCode()) {
        case 8535: /* token invalid or under-scoped */ break;
        case 7301: /* caller lacks permission      */ break;
        case 7103: /* workspace does not exist     */ break;
        default:   /* log and surface              */ break;
    }
    System.out.println(ex.getErrorCode() + " " + ex.getErrorMessage());
}
catch (ParseException ex) {
    System.out.println("Malformed response: " + ex.getResponseMessage());
}
catch (java.io.IOException ex) {
    // Network level: time-outs and connection failures. Safe to retry.
    System.out.println("Transport failure: " + ex.getMessage());
}""",
        "timeouts": """ac.setConnectionTimeout(10000);   // milliseconds
ac.setReadTimeout(60000);

int connect = ac.getConnectionTimeout();
int read    = ac.getReadTimeout();""",
        "proxy": """ac.setProxy("proxy.example.com", 8443, "proxyUser", "proxyPassword");""",
        "datacenter": """// Point the client at the data center that hosts your organization.
ac.setAnalyticsServerURL("https://analyticsapi.zoho.eu");
ac.setAccountsServerURL("https://accounts.zoho.eu");""",
        "headers": """// Key accepts alphanumerics and hyphens only; the value may not contain newlines.
ac.setHeaders("X-Custom-Source", "nightly-sync");""",
        "accesstoken": """// Supply a token you already hold instead of letting the SDK mint one.
ac.setAccessToken("1000.xxxxxxx.xxxxxxx");""",
        "import_sync": """String importType   = "TRUNCATEADD";
String fileType     = "csv";
boolean autoIdentify = true;
String filePath     = "/home/user/Sales.csv";

BulkAPI bulk = ac.getBulkInstance(orgId, workspaceId);
JSONObject response = bulk.importData(viewId, importType, fileType, autoIdentify, filePath, null);
System.out.println(response);""",
        "import_batch": """String importType    = "APPEND";
boolean autoIdentify = true;
String filePath      = "/home/user/large-sales.csv";
int batchSize        = 100000;          // rows per batch

BulkAPI bulk = ac.getBulkInstance(orgId, workspaceId);
long jobId = bulk.importDataAsBatches(viewId, importType, autoIdentify,
                                      filePath, batchSize, null, null);

JSONObject job = bulk.getImportJobDetails(jobId);
System.out.println(job);""",
        "export_sync": """BulkAPI bulk = ac.getBulkInstance(orgId, workspaceId);
bulk.exportData(viewId, "csv", "/home/user/Sales.csv", null);""",
        "export_async": """BulkAPI bulk = ac.getBulkInstance(orgId, workspaceId);

long jobId = bulk.initiateBulkExport(viewId, "csv", null);

JSONObject job = bulk.getExportJobDetails(jobId);
if ("JOB COMPLETED".equals(job.getString("jobStatus"))) {
    bulk.exportBulkData(jobId, "/home/user/Sales.csv");
}""",
    },
    notes=[
        "Every API method declares `ServerException`, `ParseException`, `IOException` and `JSONException`.",
        "`config` parameters accept `null` when you have nothing to add.",
    ],
)

# ---------------------------------------------------------------- Python

PYTHON = Lang(
    key="python", name="Python", fence="python",
    source="python/source/AnalyticsClient.py",
    sample="python/sample/Test.py",
    naming="`snake_case`.",
    id_type="`str`. Pass identifiers as strings, not integers.",
    error_type="`ServerError` (`.errorCode`, `.message`) and `ParseError`.",
    install="""Put `AnalyticsClient.py` on the import path and install its one dependency:

```bash
pip install requests
```

```python
from AnalyticsClient import AnalyticsClient
```""",
    snippets={
        "construct": """from AnalyticsClient import AnalyticsClient

CLIENT_ID     = "1000.xxxxxxx"
CLIENT_SECRET = "xxxxxxx"
REFRESH_TOKEN = "1000.xxxxxxx.xxxxxxx"

ac = AnalyticsClient(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)""",
        "singleton": '''"""analytics.py -- one client for the whole process."""
import os
from AnalyticsClient import AnalyticsClient

# Module-level: created once on first import, reused by every caller. The
# access token it holds is refreshed in place when it expires.
client = AnalyticsClient(
    os.environ["ZOHO_CLIENT_ID"],
    os.environ["ZOHO_CLIENT_SECRET"],
    os.environ["ZOHO_REFRESH_TOKEN"],
)

# Everywhere else in the application:
#     from analytics import client
#     workspace = client.get_workspace_instance(ORG_ID, WORKSPACE_ID)''',
        "instances": """org       = ac.get_org_instance(ORG_ID)
workspace = ac.get_workspace_instance(ORG_ID, WORKSPACE_ID)
view      = ac.get_view_instance(ORG_ID, WORKSPACE_ID, VIEW_ID)
bulk      = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)""",
        "first_call": """from AnalyticsClient import AnalyticsClient, ServerError, ParseError

ac = AnalyticsClient(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)

try:
    orgs = ac.get_orgs()
    print(orgs)
except ServerError as err:
    print(f"Server error {err.errorCode}: {err.message}")
except ParseError as err:
    print(f"Could not parse response: {err}")""",
        "errors": """from AnalyticsClient import ServerError, ParseError

try:
    workspace = ac.get_workspace_instance(ORG_ID, WORKSPACE_ID)
    print(workspace.get_views())
except ServerError as err:
    # err.errorCode is the stable value to branch on.
    if err.errorCode == 8535:
        pass        # token invalid or under-scoped
    elif err.errorCode == 7301:
        pass        # caller lacks permission
    elif err.errorCode == 7103:
        pass        # workspace does not exist
    print(err.errorCode, err.message)
except ParseError as err:
    print("Malformed response:", err)""",
        "timeouts": """# The Python client exposes timeouts through the underlying requests session.
ac.request_timeout = (10, 60)   # (connect, read) in seconds""",
        "proxy": """ac.set_proxy("proxy.example.com", "8443", "proxyUser", "proxyPassword")""",
        "datacenter": """ac.analytics_server_url = "https://analyticsapi.zoho.eu"
ac.accounts_server_url = "https://accounts.zoho.eu\"""",
        "headers": """# Any extra headers are merged into every request.
ac.default_headers = {"X-Custom-Source": "nightly-sync"}""",
        "accesstoken": """# Supply a token you already hold instead of letting the SDK mint one.
ac.access_token = "1000.xxxxxxx.xxxxxxx\"""",
        "import_sync": """bulk = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)

response = bulk.import_data(
    VIEW_ID,
    "TRUNCATEADD",      # import_type
    "csv",              # file_type
    True,               # auto_identify
    "/home/user/Sales.csv",
)
print(response)""",
        "import_batch": """bulk = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)

job_id = bulk.import_data_as_batches(
    VIEW_ID,
    "APPEND",
    True,
    "/home/user/large-sales.csv",
    100000,             # rows per batch
)

print(bulk.get_import_job_details(job_id))""",
        "export_sync": """bulk = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)
bulk.export_data(VIEW_ID, "csv", "/home/user/Sales.csv")""",
        "export_async": """bulk = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)

job_id = bulk.initiate_bulk_export(VIEW_ID, "csv")

job = bulk.get_export_job_details(job_id)
if job["jobStatus"] == "JOB COMPLETED":
    bulk.export_bulk_data(job_id, "/home/user/Sales.csv")""",
    },
    notes=[
        "`config` defaults to `{}`; omit it when you have nothing to add.",
        "Streaming variants `export_data_stream()` and `export_bulk_data_stream()` return a "
        "`urllib3` response so large exports never have to be buffered in memory.",
    ],
)

# ---------------------------------------------------------------- C#

CSHARP = Lang(
    key="csharp", name="C#", fence="csharp",
    source="csharp/source/AnalyticsClient.cs",
    sample="csharp/sample/program.cs",
    naming="`PascalCase`.",
    id_type="`long`.",
    error_type="`ServerException` (`GetHTTPStatusCode()`, `GetErrorCode()`, `GetErrorMessage()`).",
    install="""Reference the `ZohoAnalytics` project (`source/ZohoAnalytics.csproj`, `net6.0`) or
build it into a library:

```bash
dotnet build source/ZohoAnalytics.csproj -c Release
```

```csharp
using ZohoAnalytics;
using System.Text.Json;
```

Responses are `System.Text.Json.JsonElement`; request configuration is
`Dictionary<string, object>`.""",
    snippets={
        "construct": """using ZohoAnalytics;
using System.Collections.Generic;
using System.Text.Json;

string clientId     = "1000.xxxxxxx";
string clientSecret = "xxxxxxx";
string refreshToken = "1000.xxxxxxx.xxxxxxx";

IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);""",
        "singleton": """public static class Analytics
{
    // Lazy<T> gives a thread-safe single instance for the whole process. The
    // access token it holds is reused and refreshed in place when it expires.
    private static readonly Lazy<IAnalyticsClient> _client =
        new Lazy<IAnalyticsClient>(() => new AnalyticsClient(
            Environment.GetEnvironmentVariable("ZOHO_CLIENT_ID"),
            Environment.GetEnvironmentVariable("ZOHO_CLIENT_SECRET"),
            Environment.GetEnvironmentVariable("ZOHO_REFRESH_TOKEN")));

    public static IAnalyticsClient Client => _client.Value;
}

// Everywhere else in the application:
IWorkspaceAPI workspace = Analytics.Client.GetWorkspaceInstance(orgId, workspaceId);""",
        "instances": """IOrgAPI       org       = ac.GetOrgInstance(orgId);
IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
IViewAPI      view      = ac.GetViewInstance(orgId, workspaceId, viewId);
IBulkAPI      bulk      = ac.GetBulkInstance(orgId, workspaceId);""",
        "first_call": """IAnalyticsClient ac = new AnalyticsClient(clientId, clientSecret, refreshToken);

try
{
    JsonElement orgs = ac.GetOrgs();
    Console.WriteLine(orgs);
}
catch (ServerException ex)
{
    Console.WriteLine($"HTTP {ex.GetHTTPStatusCode()} / {ex.GetErrorCode()}: {ex.GetErrorMessage()}");
}""",
        "errors": """try
{
    IWorkspaceAPI workspace = ac.GetWorkspaceInstance(orgId, workspaceId);
    Console.WriteLine(workspace.GetViews(null));
}
catch (ServerException ex)
{
    // GetErrorCode() is the stable value to branch on.
    switch (ex.GetErrorCode())
    {
        case 8535: break;   // token invalid or under-scoped
        case 7301: break;   // caller lacks permission
        case 7103: break;   // workspace does not exist
    }
    Console.WriteLine($"HTTP {ex.GetHTTPStatusCode()} / {ex.GetErrorCode()}: {ex.GetErrorMessage()}");
}""",
        "timeouts": """ac.SetConnectionTimeout(10000);   // milliseconds
ac.SetReadTimeout(60000);

int connect = ac.GetConnectionTimeout();
int read    = ac.GetReadTimeout();""",
        "proxy": """ac.SetProxy("proxy.example.com", 8443, "proxyUser", "proxyPassword");""",
        "datacenter": """ac.SetAnalyticsServerURL("https://analyticsapi.zoho.eu");
ac.SetAccountsServerURL("https://accounts.zoho.eu");""",
        "headers": """// Diagnostic logging is off unless a path is supplied.
AnalyticsClient.SetDebugLogPath(@"C:\\logs\\zoho-analytics-sdk.log");""",
        "accesstoken": """// Responses are JsonElement; read them with the System.Text.Json API.
JsonElement views = workspace.GetViews(null);
foreach (JsonElement v in views.EnumerateArray())
{
    Console.WriteLine(v.GetProperty("viewName").GetString());
}""",
        "import_sync": """IBulkAPI bulk = ac.GetBulkInstance(orgId, workspaceId);

JsonElement response = bulk.ImportData(
    viewId,
    "TRUNCATEADD",
    "csv",
    true,
    @"C:\\data\\Sales.csv",
    null);

Console.WriteLine(response);""",
        "import_batch": """IBulkAPI bulk = ac.GetBulkInstance(orgId, workspaceId);

long jobId = bulk.ImportDataAsBatches(
    viewId, "APPEND", true, @"C:\\data\\large-sales.csv", 100000, null, null);

Console.WriteLine(bulk.GetImportJobDetails(jobId));""",
        "export_sync": """IBulkAPI bulk = ac.GetBulkInstance(orgId, workspaceId);
bulk.ExportData(viewId, "csv", @"C:\\data\\Sales.csv", null);""",
        "export_async": """IBulkAPI bulk = ac.GetBulkInstance(orgId, workspaceId);

long jobId = bulk.InitiateBulkExport(viewId, "csv", null);

JsonElement job = bulk.GetExportJobDetails(jobId);
if (job.GetProperty("jobStatus").GetString() == "JOB COMPLETED")
{
    bulk.ExportBulkData(jobId, @"C:\\data\\Sales.csv");
}""",
    },
    notes=[
        "The interfaces (`IAnalyticsClient`, `IOrgAPI`, `IWorkspaceAPI`, `IViewAPI`, `IBulkAPI`) "
        "are the supported surface; code against them so the implementation stays swappable in tests.",
        "`config` accepts `null`.",
    ],
)

# ---------------------------------------------------------------- Go

GO = Lang(
    key="go", name="Go", fence="go",
    source="go/source/zoho/pkg/analyticsclient/analyticsclient.go",
    sample="go/sample/test.go",
    naming="`PascalCase` (exported).",
    id_type="`string`.",
    error_type="A returned `*ServerException` with `ErrorCode`, `ErrorMessage`, `HttpStatusCode` and `Action`.",
    install="""Place the package under your module as `zoho/pkg/analyticsclient` and import it:

```go
import ZAnalytics "zoho/pkg/analyticsclient"
```

Go returns errors rather than raising them: every method returns a trailing
`*ServerException` which is `nil` on success.""",
    snippets={
        "construct": """package main

import (
    "fmt"
    ZAnalytics "zoho/pkg/analyticsclient"
)

var (
    clientId     = "1000.xxxxxxx"
    clientSecret = "xxxxxxx"
    refreshToken = "1000.xxxxxxx.xxxxxxx"
)

ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)""",
        "singleton": """package analytics

import (
    "os"
    "sync"

    ZAnalytics "zoho/pkg/analyticsclient"
)

var (
    once   sync.Once
    client ZAnalytics.Client
)

// Client returns the process-wide client. sync.Once guarantees the credentials
// are turned into an access token exactly once; that token is then reused and
// refreshed in place.
func Client() *ZAnalytics.Client {
    once.Do(func() {
        client = ZAnalytics.GetAnalyticsClient(
            os.Getenv("ZOHO_CLIENT_ID"),
            os.Getenv("ZOHO_CLIENT_SECRET"),
            os.Getenv("ZOHO_REFRESH_TOKEN"),
        )
    })
    return &client
}""",
        "instances": """org       := ZAnalytics.GetOrgInstance(&ac, orgId)
workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)
view      := ZAnalytics.GetViewInstance(&ac, orgId, workspaceId, viewId)
bulk      := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)""",
        "first_call": """ac := ZAnalytics.GetAnalyticsClient(clientId, clientSecret, refreshToken)

orgs, exception := ac.GetOrgs()
if exception != nil {
    fmt.Printf("HTTP %d / %v: %s\\n",
        exception.HttpStatusCode, exception.ErrorCode, exception.ErrorMessage)
    return
}
fmt.Println(orgs)""",
        "errors": """workspace := ZAnalytics.GetWorkspaceInstance(&ac, orgId, workspaceId)

views, exception := workspace.GetViews(map[string]interface{}{})
if exception != nil {
    // ErrorCode is a float64; compare numerically.
    switch int(exception.ErrorCode) {
    case 8535: // token invalid or under-scoped
    case 7301: // caller lacks permission
    case 7103: // workspace does not exist
    }
    fmt.Printf("HTTP %d / %v: %s (action: %s)\\n",
        exception.HttpStatusCode, exception.ErrorCode,
        exception.ErrorMessage, exception.Action)
    return
}
fmt.Println(views)""",
        "timeouts": """ac.SetConnectionTimeout(10)   // seconds
ac.SetReadTimeout(60)""",
        "proxy": """ac.SetProxy("proxy.example.com", 8443, "proxyUser", "proxyPassword")""",
        "datacenter": """ac.SetAnalyticsServerURL("https://analyticsapi.zoho.eu")
ac.SetAccountsServerURL("https://accounts.zoho.eu")""",
        "headers": """// Config maps are plain map[string]interface{} values.
config := map[string]interface{}{
    "viewTypes": []string{"0", "1"},
}
views, exception := workspace.GetViews(config)""",
        "accesstoken": """ac.SetAccessToken("1000.xxxxxxx.xxxxxxx")""",
        "import_sync": """bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)

result, exception := bulk.ImportData(
    viewId,
    "TRUNCATEADD",
    "csv",
    true,
    "/home/user/Sales.csv",
    map[string]interface{}{},
)
if exception != nil {
    fmt.Println(exception.ErrorMessage)
    return
}
fmt.Println(result)""",
        "import_batch": """bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)

jobId, exception := bulk.ImportDataAsBatches(
    viewId, "APPEND", true, "/home/user/large-sales.csv", 100000,
    map[string]interface{}{}, map[string]interface{}{},
)
if exception != nil {
    fmt.Println(exception.ErrorMessage)
    return
}

job, exception := bulk.GetImportJobDetails(jobId)
if exception == nil {
    fmt.Println(job)
}""",
        "export_sync": """bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)

exception := bulk.ExportData(viewId, "csv", "/home/user/Sales.csv",
    map[string]interface{}{})
if exception != nil {
    fmt.Println(exception.ErrorMessage)
}""",
        "export_async": """bulk := ZAnalytics.GetBulkInstance(&ac, orgId, workspaceId)

jobId, exception := bulk.InitiateBulkExport(viewId, "csv", map[string]interface{}{})
if exception != nil {
    fmt.Println(exception.ErrorMessage)
    return
}

job, exception := bulk.GetExportJobDetails(jobId)
if exception == nil && job.(map[string]interface{})["jobStatus"] == "JOB COMPLETED" {
    bulk.ExportBulkData(jobId, "/home/user/Sales.csv")
}""",
    },
    notes=[
        "Results come back as `interface{}`; type-assert to `map[string]interface{}` or "
        "`[]interface{}` before reading fields.",
        "`ErrorCode` is a `float64` because it is decoded from JSON; cast with `int(...)` to compare.",
    ],
)

# ---------------------------------------------------------------- PHP

PHP = Lang(
    key="php", name="PHP", fence="php",
    source="php/source/AnalyticsClient.php",
    sample="php/sample/Test.php",
    naming="`camelCase`.",
    id_type="`string`.",
    error_type="`ServerException` (`getErrorCode()`, `getErrorMessage()`), plus `IOException` and `ParseException`.",
    install="""Require the client and make sure the cURL and JSON extensions are enabled:

```bash
php -m | grep -E 'curl|json'
```

```php
require 'AnalyticsClient.php';
```""",
    snippets={
        "construct": """<?php
require 'AnalyticsClient.php';

$client_id     = "1000.xxxxxxx";
$client_secret = "xxxxxxx";
$refresh_token = "1000.xxxxxxx.xxxxxxx";

$ac = new AnalyticsClient($client_id, $client_secret, $refresh_token);""",
        "singleton": """<?php
require_once 'AnalyticsClient.php';

final class Analytics
{
    private static ?AnalyticsClient $client = null;

    // One client per process. The access token it holds is reused across every
    // call and refreshed in place when it expires.
    public static function client(): AnalyticsClient
    {
        if (self::$client === null) {
            self::$client = new AnalyticsClient(
                getenv('ZOHO_CLIENT_ID'),
                getenv('ZOHO_CLIENT_SECRET'),
                getenv('ZOHO_REFRESH_TOKEN')
            );
        }
        return self::$client;
    }
}

// Everywhere else in the application:
$workspace = Analytics::client()->getWorkspaceInstance($org_id, $workspace_id);""",
        "instances": """$org       = $ac->getOrgInstance($org_id);
$workspace = $ac->getWorkspaceInstance($org_id, $workspace_id);
$view      = $ac->getViewInstance($org_id, $workspace_id, $view_id);
$bulk      = $ac->getBulkInstance($org_id, $workspace_id);""",
        "first_call": """$ac = new AnalyticsClient($client_id, $client_secret, $refresh_token);

try {
    $orgs = $ac->getOrgs();
    print_r($orgs);
}
catch (ServerException $se) {
    echo "Server error " . $se->getErrorCode() . ": " . $se->getErrorMessage() . "\\n";
}
catch (ParseException $pe) {
    echo "Could not parse response: " . $pe->getErrorMessage() . "\\n";
}""",
        "errors": """try {
    $workspace = $ac->getWorkspaceInstance($org_id, $workspace_id);
    print_r($workspace->getViews());
}
catch (ServerException $se) {
    // getErrorCode() is the stable value to branch on.
    switch ($se->getErrorCode()) {
        case 8535: break;   // token invalid or under-scoped
        case 7301: break;   // caller lacks permission
        case 7103: break;   // workspace does not exist
    }
    echo $se->getErrorCode() . " " . $se->getErrorMessage() . "\\n";
}
catch (IOException $ioe) {
    // Transport level: time-outs and connection failures. Safe to retry.
    echo "Transport failure: " . $ioe->getErrorMessage() . "\\n";
}
catch (ParseException $pe) {
    echo "Malformed response: " . $pe->getErrorMessage() . "\\n";
}""",
        "timeouts": """$ac->setConnectionTimeout(10);   // seconds
$ac->setReadTimeout(60);

$connect = $ac->getConnectionTimeout();
$read    = $ac->getReadTimeout();""",
        "proxy": """// proxy_type is one of "HTTP", "HTTPS" or "BOTH".
$ac->setProxy("proxy.example.com", 8443, "BOTH", "proxyUser", "proxyPassword");""",
        "datacenter": """$ac->setAnalyticsServerURL("https://analyticsapi.zoho.eu");
$ac->setAccountsServerURL("https://accounts.zoho.eu");""",
        "headers": """$config = array(
    "viewTypes" => array("0", "1")
);
$views = $workspace->getViews($config);""",
        "accesstoken": """$ac->setAccessToken("1000.xxxxxxx.xxxxxxx");""",
        "import_sync": """$bulk = $ac->getBulkInstance($org_id, $workspace_id);

$response = $bulk->importData(
    $view_id,
    "TRUNCATEADD",
    "csv",
    true,
    "/home/user/Sales.csv"
);
print_r($response);""",
        "import_batch": """$bulk = $ac->getBulkInstance($org_id, $workspace_id);

$job_id = $bulk->importDataAsBatches(
    $view_id, "APPEND", true, "/home/user/large-sales.csv", 100000
);

print_r($bulk->getImportJobDetails($job_id));""",
        "export_sync": """$bulk = $ac->getBulkInstance($org_id, $workspace_id);
$bulk->exportData($view_id, "csv", "/home/user/Sales.csv");""",
        "export_async": """$bulk = $ac->getBulkInstance($org_id, $workspace_id);

$job_id = $bulk->initiateBulkExport($view_id, "csv");

$job = $bulk->getExportJobDetails($job_id);
if ($job["jobStatus"] === "JOB COMPLETED") {
    $bulk->exportBulkData($job_id, "/home/user/Sales.csv");
}""",
    },
    notes=[
        "`config` defaults to `array()`; omit it when you have nothing to add.",
        "Responses are associative arrays, already JSON-decoded.",
    ],
)

# ---------------------------------------------------------------- Node.js

NODEJS = Lang(
    key="nodejs", name="Node.js", fence="javascript",
    source="nodejs/source/AnalyticsClient.js",
    sample="nodejs/sample/dummytest.js",
    naming="`camelCase`.",
    id_type="`string`.",
    error_type="A rejected Promise carrying `errorCode` and `errorMessage`.",
    install="""Require the client. Every method returns a Promise, so use `await` inside an
`async` function or chain `.then()` / `.catch()`.

```javascript
var analyticsClient = require('./AnalyticsClient');
```""",
    snippets={
        "construct": """var analyticsClient = require('./AnalyticsClient');

var clientId     = '1000.xxxxxxx';
var clientSecret = 'xxxxxxx';
var refreshToken = '1000.xxxxxxx.xxxxxxx';

var ac = new analyticsClient(clientId, clientSecret, refreshToken);""",
        "singleton": """// analytics.js -- one client for the whole process.
var analyticsClient = require('./AnalyticsClient');

// Node caches modules, so this constructor runs once no matter how many files
// require it. The access token is reused and refreshed in place when it expires.
var ac = new analyticsClient(
    process.env.ZOHO_CLIENT_ID,
    process.env.ZOHO_CLIENT_SECRET,
    process.env.ZOHO_REFRESH_TOKEN
);

module.exports = ac;

// Everywhere else in the application:
//     var ac = require('./analytics');
//     var workspace = ac.getWorkspaceInstance(orgId, workspaceId);""",
        "instances": """var org       = ac.getOrgInstance(orgId);
var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
var view      = ac.getViewInstance(orgId, workspaceId, viewId);
var bulk      = ac.getBulkInstance(orgId, workspaceId);""",
        "first_call": """var ac = new analyticsClient(clientId, clientSecret, refreshToken);

async function main() {
    try {
        var orgs = await ac.getOrgs();
        console.log(orgs);
    } catch (error) {
        console.log('Server error ' + error.errorCode + ': ' + error.errorMessage);
    }
}

main();""",
        "errors": """async function listViews() {
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    try {
        var views = await workspace.getViews();
        console.log(views);
    } catch (error) {
        // error.errorCode is the stable value to branch on.
        switch (error.errorCode) {
            case 8535: break;   // token invalid or under-scoped
            case 7301: break;   // caller lacks permission
            case 7103: break;   // workspace does not exist
        }
        console.log(error.errorCode, error.errorMessage);
    }
}""",
        "timeouts": """// Timeouts are supplied when the client is constructed.
var ac = new analyticsClient(clientId, clientSecret, refreshToken);
ac.requestTimeout = 60000;   // milliseconds""",
        "proxy": """ac.setProxy('proxy.example.com', 8443, 'proxyUser', 'proxyPassword');""",
        "datacenter": """ac.setAnalyticsServerURL('https://analyticsapi.zoho.eu');
ac.setAccountsServerURL('https://accounts.zoho.eu');""",
        "headers": """var config = {
    'viewTypes': ['0', '1']
};
var views = await workspace.getViews(config);""",
        "accesstoken": """ac.setAccessToken('1000.xxxxxxx.xxxxxxx');""",
        "import_sync": """var bulk = ac.getBulkInstance(orgId, workspaceId);

var response = await bulk.importData(
    viewId,
    'TRUNCATEADD',
    'csv',
    true,
    '/home/user/Sales.csv'
);
console.log(response);""",
        "import_batch": """var bulk = ac.getBulkInstance(orgId, workspaceId);

var jobId = await bulk.importDataAsBatches(
    viewId, 'APPEND', true, '/home/user/large-sales.csv', 100000
);

console.log(await bulk.getImportJobDetails(jobId));""",
        "export_sync": """var bulk = ac.getBulkInstance(orgId, workspaceId);
await bulk.exportData(viewId, 'csv', '/home/user/Sales.csv');""",
        "export_async": """var bulk = ac.getBulkInstance(orgId, workspaceId);

var jobId = await bulk.initiateBulkExport(viewId, 'csv');

var job = await bulk.getExportJobDetails(jobId);
if (job.jobStatus === 'JOB COMPLETED') {
    await bulk.exportBulkData(jobId, '/home/user/Sales.csv');
}""",
    },
    notes=[
        "Unhandled rejections crash the process on modern Node; always attach a "
        "`catch` or wrap `await` in `try`.",
        "`config` defaults to `{}`.",
    ],
)

# ---------------------------------------------------------------- Ruby

RUBY = Lang(
    key="ruby", name="Ruby", fence="ruby",
    source="ruby/source/lib/zoho_analytics_client.rb",
    sample="ruby/sample/sample.rb",
    naming="`snake_case`.",
    id_type="`String`.",
    error_type="`ServerError` (`.error_code`, `.response_content`, `.is_oauth_error`) and `ParseError`.",
    install="""Install the gem and require it:

```bash
gem build zoho_analytics_client.gemspec
gem install zoho_analytics_client-*.gem
```

```ruby
require 'zoho_analytics_client'
```

Ruby is the one client built with a **builder**: set the data center and the
credentials, then call `build`.""",
    snippets={
        "construct": """require 'zoho_analytics_client'

ac = AnalyticsClient.new
       .with_data_center("US")
       .with_oauth({
         "clientId"     => "1000.xxxxxxx",
         "clientSecret" => "xxxxxxx",
         "refreshToken" => "1000.xxxxxxx.xxxxxxx"
       })
       .build""",
        "singleton": """# analytics.rb -- one client for the whole process.
require 'singleton'
require 'zoho_analytics_client'

class Analytics
  include Singleton

  attr_reader :client

  # Runs once. The access token the client holds is reused across every call
  # and refreshed in place when it expires.
  def initialize
    @client = AnalyticsClient.new
                .with_data_center(ENV.fetch("ZOHO_DC", "US"))
                .with_oauth({
                  "clientId"     => ENV.fetch("ZOHO_CLIENT_ID"),
                  "clientSecret" => ENV.fetch("ZOHO_CLIENT_SECRET"),
                  "refreshToken" => ENV.fetch("ZOHO_REFRESH_TOKEN")
                })
                .build
  end
end

# Everywhere else in the application:
workspace = Analytics.instance.client.get_workspace_instance(ORG_ID, WORKSPACE_ID)""",
        "instances": """org       = ac.get_org_instance(ORG_ID)
workspace = ac.get_workspace_instance(ORG_ID, WORKSPACE_ID)
view      = ac.get_view_instance(ORG_ID, WORKSPACE_ID, VIEW_ID)
bulk      = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)""",
        "first_call": """begin
  orgs = ac.get_orgs
  puts orgs
rescue ServerError => e
  puts "Server error #{e.error_code}: #{e.response_content}"
rescue StandardError => e
  puts e.message
end""",
        "errors": """begin
  workspace = ac.get_workspace_instance(ORG_ID, WORKSPACE_ID)
  puts workspace.get_views
rescue ServerError => e
  # e.error_code is the stable value to branch on.
  case e.error_code
  when 8535 then nil   # token invalid or under-scoped
  when 7301 then nil   # caller lacks permission
  when 7103 then nil   # workspace does not exist
  end
  puts "#{e.error_code} #{e.response_content}"
  puts "OAuth problem" if e.is_oauth_error
rescue ParseError => e
  puts "Malformed response: #{e.message}"
end""",
        "timeouts": """# Timeouts are part of the builder configuration.
ac = AnalyticsClient.new
       .with_data_center("US")
       .with_oauth(credentials)
       .build""",
        "proxy": """ac = AnalyticsClient.new
       .with_data_center("US")
       .with_oauth(credentials)
       .with_proxy({
         "host"     => "proxy.example.com",
         "port"     => 8443,
         "user"     => "proxyUser",
         "password" => "proxyPassword"
       })
       .build""",
        "datacenter": """# The data center is set on the builder, not by assembling URLs by hand.
# Accepted values: "US", "EU", "IN", "AU", "JP", "CN", "SA", "CA".
ac = AnalyticsClient.new
       .with_data_center("EU")
       .with_oauth(credentials)
       .build""",
        "headers": """config = { "viewTypes" => ["0", "1"] }
views  = workspace.get_views(config)""",
        "accesstoken": """# Encrypted on-disk token storage, so a restart does not mint a new token.
ac = AnalyticsClient.new
       .with_data_center("US")
       .with_oauth(credentials)
       .with_token_store_path("/var/lib/myapp/zoho-tokens")
       .build""",
        "import_sync": """bulk = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)

result = bulk.import_data(
  VIEW_ID,
  "TRUNCATEADD",
  "csv",
  "true",
  "/home/user/Sales.csv"
)
puts result""",
        "import_batch": """bulk = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)

job_id = bulk.import_data_as_batches(
  VIEW_ID, "APPEND", "true", "/home/user/large-sales.csv", 100000
)

puts bulk.get_import_job_details(job_id)""",
        "export_sync": """bulk = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)
bulk.export_data(VIEW_ID, "csv", "/home/user/Sales.csv")""",
        "export_async": """bulk = ac.get_bulk_instance(ORG_ID, WORKSPACE_ID)

job_id = bulk.initiate_bulk_export(VIEW_ID, "csv")

job = bulk.get_export_job_details(job_id)
if job["jobStatus"] == "JOB COMPLETED"
  bulk.export_bulk_data(job_id, "/home/user/Sales.csv")
end""",
    },
    notes=[
        "`with_token_store_path` stores the access token encrypted on disk, so a process "
        "restart reuses the existing token instead of minting a new one. Strongly recommended "
        "for short-lived processes such as cron jobs.",
        "`config` defaults to `{}`.",
    ],
)

LANGS: dict[str, Lang] = {
    l.key: l for l in (JAVA, PYTHON, CSHARP, GO, PHP, NODEJS, RUBY)
}

ORDER = ["java", "python", "csharp", "go", "php", "nodejs", "ruby"]
