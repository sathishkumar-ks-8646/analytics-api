---
name: analytics-oas-samples
description: Author or fix the SDK code snippets in <VERSION>/zenesis-oas-samples/ of the analytics-api repository - nine languages (Curl, C#, Go, Java, Php, Python, Node, Ruby, Deluge) per path and method, derived from the markdown reference in <VERSION>/md/ and the matching OpenAPI operation. Use when adding snippets for a new endpoint, updating snippets after a CONFIG attribute changed, or when the validator reports "samples for X, which the spec does not define" or "no SDK samples for X", or when an endpoint has no SDK Example document in the OKF bundle.
---

# Author the SDK samples from the markdown and the operation

`<VERSION>/zenesis-oas-samples/` holds **one JSON file per domain**, named
`<domain-slug>-grouped-api-samples.json` (the same `slug` as the specification). Each file maps
**path template → lower-case method → language → snippets**. No script derives them — you write all
nine snippets per operation, modelled on a neighbouring operation in the same file.

The only consumer is the OKF bundle: each entry becomes one `SDK Example` concept at
`/sdk-examples/<domain>/<group>/<kebab(operationId)>.md`, plus the `api.sdk_examples` frontmatter
pointer and the `## SDK Examples` link on the endpoint document. **An operation with no samples entry
simply gets no SDK Example document** — silently. Nothing errors; the bundle is just poorer.

## 1. The structure

```jsonc
{
  "/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}": {
    "put": {
      "Curl":   { "snippets": [ { "code": "curl …" } ] },
      "C#":     { "snippets": [ { "code": "…" } ] },
      "Go":     { "snippets": [ { "code": "…" } ] },
      "Java":   { "snippets": [ { "code": "…" } ] },
      "Php":    { "snippets": [ { "code": "…" } ] },
      "Python": { "snippets": [ { "code": "…" } ] },
      "Node":   { "snippets": [ { "code": "…" } ] },
      "Ruby":   { "snippets": [ { "code": "…" } ] },
      "Deluge": { "snippets": [ { "code": "…" } ] }
    }
  }
}
```

Non-negotiable:

- **The path key is the OpenAPI path template, character for character** — `{workspace-id}`, not
  `<workspace-id>` and not a resolved ID. A key the spec does not define is a hard error; an
  operation with no key is a warning.
- **The method key is lower-case** (`get`, `post`, `put`, `delete`). `PUT` is an error.
- **Language keys are spelled exactly** `Curl`, `C#`, `Go`, `Java`, `Php`, `Python`, `Node`, `Ruby`,
  `Deluge` — this is `LANG_FENCE` in `tools/okf/build_okf.py`. `cURL`, `PHP`, `NodeJS`, `C-Sharp`
  are all silently ignored.
- All nine, every time. A partial set renders a partial SDK Example document.
- `snippets` is a **list**. More than one entry per language renders as numbered variants — use it
  when the markdown has genuinely different cases (file vs raw data import), not for cosmetic ones.

The OKF bundle renders the languages in a fixed order with fixed display names and fences:

| Key | Heading | Fence |
|---|---|---|
| `Curl` | cURL | `bash` |
| `C#` | C# | `csharp` |
| `Go` | Go | `go` |
| `Java` | Java | `java` |
| `Php` | PHP | `php` |
| `Python` | Python | `python` |
| `Node` | Node.js | `javascript` |
| `Ruby` | Ruby | `ruby` |
| `Deluge` | Deluge | `javascript` |

## 2. House conventions — copy these literally

Every snippet in the repository uses the same illustrative values. **Use these, not the markdown's
sample IDs** (the markdown uses `137687000271334001`-style IDs; the samples use the house set).

| Thing | Value |
|---|---|
| Client ID | `1000.xxxxxxx` |
| Client secret | `xxxxxxx` |
| Refresh token | `1000.xxxxxxx.xxxxxxx` |
| Organisation ID | `55522777` |
| Workspace ID | `35130000001055707` |
| View / table ID | `35130000001055717` |
| Other resource IDs | `35130000001056601`-style, same prefix |
| Base URL | `https://analyticsapi.zoho.com` |
| cURL access token | `<access_token>` placeholder |
| cURL org header | `-H 'ZANALYTICS-ORGID: <org-id>'` *(some files use the literal `55522777`; copy whichever the neighbouring snippets in the same file use)* |
| cURL GET CONFIG | percent-encoded **inline in the URL query string**: `?CONFIG=%7B%22keyword%22%3A%22Sales%22%7D` |
| Email addresses | `user@example.com`, `finance@zylker.com`, `manager@zylker.com` |
| Local file path | `/home/local/Sales.csv` |

Other conventions:

- **URLs in cURL and Deluge never carry the `{braces}` path template** — the path *key* holds the
  template, the snippet shows a real call. Which style of ID is **a per-file convention**: most
  files use resolved numeric IDs (`/workspaces/35130000001055707/…`), while `user-groups` and
  `workspace-management` use angle placeholders (`/workspaces/<workspace-id>/…`). Match the
  neighbouring snippets in the same file.
- cURL line formatting is also per-file: most snippets are one long line, 54 use `\` continuations
  with the headers on their own lines. Match the neighbours.
- **The payload is one representative case**, usually the simplest meaningful one from the markdown's
  `### Sample Requests`. Nine snippets show the same call, so a reader can compare languages.
- Every snippet is **runnable top to bottom**: imports, client construction, the call, printing the
  result. Not a fragment.
- The method name follows each language's convention for the same operation: `update_email_schedule`
  (Python, Ruby), `updateEmailSchedule` (Java, PHP, Node, Deluge), `UpdateEmailSchedule` (C#, Go).
- CONFIG is built as a native map/dict/array and handed to the SDK; only cURL and Deluge serialise it
  by hand.
- Client objects come from the right scope: `get_workspace_instance(org, workspace)` for
  workspace-scoped calls, `get_view_instance(org, workspace, view)` for view-scoped,
  `get_bulk_instance(org, workspace)` for import/export, and the client itself (`ac.…`) for
  org-level calls. Check the neighbouring snippet for which one this endpoint uses.
- `ZANALYTICS-ORGID` is passed to the SDK constructor/instance, not as a header, in every language
  except cURL and Deluge (which build the request by hand).
- Deluge never uses an SDK — it is raw `invokeurl` with `headersMap`,
  `zoho.encryption.urlEncode(config.toString())` for GET, `parametersMap` for a body, and
  `connection:"analytics_oauth_connection"`.
- No real tokens, no real customer data, no internal hostnames.

**Full copy-ready templates for all nine languages, for GET, POST/PUT/DELETE and multipart, are in
[`references/language-templates.md`](references/language-templates.md).** Start there.

## 3. Procedure for one endpoint

1. Confirm the operation exists in `<V>/zenesis-oas/<slug>-grouped-api.json` and copy its **exact**
   path template and method. (If it does not exist yet, write it first — `analytics-zenesis-oas`.)
2. Pick the representative case from the markdown `### Sample Requests`, and the CONFIG fields it
   uses.
3. Find the **nearest neighbouring operation in the same file** — same HTTP method, same CONFIG
   shape, same resource scope — and copy its nine snippets.
4. Rewrite in each: the method name, the URL tail, the CONFIG fields, the path IDs.
5. Keep the house values of §2 untouched.
6. Add the entry under the path key, creating the path key if this is the first method on it.
7. Validate.

## 4. Verify

```bash
python3 tools/validate_api_docs.py --strict --version <V>
python3 tools/okf/build_okf.py --version <V>        # the sdk= count must rise by one per new entry
```

`build_okf.py` prints `endpoints=N groups=N errors=N sdk=N`. **`sdk` is the number of operations
with samples** — if it did not go up, your path key or method key does not match the spec.

| Message | Cause |
|---|---|
| `samples for '<path>', which the spec does not define` | the path key is not an OpenAPI path in that domain — a typo, `<param>` instead of `{param}`, or a resolved ID |
| `samples for PUT <path>, which the spec does not define` | the method key is not on that path, or it is upper-case |
| `samples must be an object keyed by path` | the file's top level is not an object |
| `<path> must map a method to its snippets` | a path key whose value is not an object |
| `no SDK samples for <path>` *(warning)* | the path exists in the spec with no samples entry |
| OKF endpoint document has no `## SDK Examples` section | same cause; the join failed silently |

### Checklist

- [ ] the path key equals the OpenAPI path template exactly, with `{braces}`
- [ ] the method key is lower-case and the spec defines it on that path
- [ ] all nine language keys are present, spelled exactly as in §1
- [ ] each `snippets` is a list of `{ "code": "…" }`
- [ ] every snippet runs top to bottom and shows the **same** call
- [ ] house illustrative IDs, tokens and base URL (§2) are used verbatim
- [ ] the CONFIG fields exist in the operation's CONFIG schema and the markdown's CONFIG table
- [ ] the method name follows each language's convention
- [ ] the client instance scope matches the endpoint's scope
- [ ] `build_okf.py`'s `sdk=` count went up
