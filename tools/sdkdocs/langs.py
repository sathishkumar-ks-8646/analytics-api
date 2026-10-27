"""Per-language profiles: naming, construction, error surface and install notes.

These describe the *language binding* - how C# cases its method names, what Go
returns instead of raising - so they hold for any API version.

The code snippets do not: they call a particular version's endpoints. They live
in `tools/sdkdocs/<version>/snippets.py` and are attached here by
`load_snippets()`, which `build.py` calls once at start-up. Read a profile's
`snippets` before that and you get an empty dict.
"""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass, field
from pathlib import Path


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


def load_snippets(version: str) -> None:
    """Attach `tools/sdkdocs/<version>/snippets.py` to every language profile.

    Call once, before building. Missing file, missing language or a language
    whose key set differs from the others is a hard error: a half-populated
    profile would render pages with silent gaps instead of failing.
    """
    path = Path(__file__).resolve().parent / version / "snippets.py"
    if not path.is_file():
        raise SystemExit(
            "no snippets for %s: %s is missing.\n"
            "A new API version needs its own tools/sdkdocs/<version>/snippets.py."
            % (version, path)
        )

    spec = importlib.util.spec_from_file_location(
        "sdkdocs_snippets_" + version.replace(".", "_"), path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    table = getattr(module, "SNIPPETS", None)
    if not isinstance(table, dict):
        raise SystemExit("%s does not define a SNIPPETS dict" % path)

    missing = [k for k in ORDER if k not in table]
    if missing:
        raise SystemExit(
            "%s has no snippets for: %s" % (path, ", ".join(missing))
        )

    expected = set(table[ORDER[0]])
    for key in ORDER:
        differs = set(table[key]) ^ expected
        if differs:
            raise SystemExit(
                "%s: %s has a different snippet key set (%s)"
                % (path, key, ", ".join(sorted(differs)))
            )
        LANGS[key].snippets = table[key]
