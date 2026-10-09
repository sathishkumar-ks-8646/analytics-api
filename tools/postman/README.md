# postman - Postman collection generator

Generates the **Zoho Analytics REST APIs** Postman collection and the **Zoho Analytics REST
Variables** environment for one API version, from the artefacts already built for that version. Both
files are written to `<repo>/<VERSION>/postman/` and committed; nothing there is edited by hand.

```bash
python3 tools/postman/build_postman.py --version v2.0          # writes <VERSION>/postman/
python3 tools/postman/build_postman.py --version v2.0 --check  # exit 1 if the committed files are stale
```

## What it reads

| Input | Used for |
|---|---|
| `<VERSION>/okf/references/endpoint-catalog.json` | the request list: title, method, path, scopes, organization header, CONFIG location, success status, permission, document paths |
| `<VERSION>/okf/domains/**/*.md` | endpoint one-line descriptions and group descriptions (frontmatter) |
| `<VERSION>/okf/workflows/*.md` | playbook tables on the domain and section folders: title, description, step labels, the endpoints each one uses |
| `<VERSION>/oas/*.json` | the ready-to-send CONFIG example on each request (first example), the other example names, header parameters such as `ZANALYTICS-DEST-ORGID`, multipart parts |
| `<VERSION>/md/<domain>/<GROUP>.md` | the opening paragraph of each section folder |
| `<VERSION>/manifest.json` | domain order, and each domain's `postman` block: `emoji`, `title`, `covers` |
| `templates/authentication-folder.json` | the 🔐 Authentication folder (token generation, refresh, revoke), carried verbatim |
| `templates/collection-skeleton.json` | collection-level auth (`Bearer {{access-token}}`) and the pre-request script that URL-encodes `CONFIG` on GET requests |
| `templates/collection-description.md`, `templates/version-folder-description.md` | the long descriptions; the counts and the per-domain table are regenerated |
| `api-reference-links.json` | endpoint title → page in the public API reference. **Curated**: add a line when a new endpoint gets a page; requests without one say "newly added" and link the OpenAPI file |

So the OKF bundle must be built first (`tools/okf/build_okf.py`); `tools/api-agent/pipeline.py`
runs the stages in the right order.

## Conventions in the output

- Request names are the endpoint titles of the API reference (the markdown `## N. Title`), folders
  are domains (`emoji title`) and groups (the OKF group title).
- URLs are `https://{{analytics-domain}}/restapi/v2/...` with every path parameter as a Postman
  variable of the same name (`{{workspace-id}}`). The environment ships those identifier variables
  **disabled**; `analytics-domain`, `accounts-domain`, the OAuth variables and `organization-id` are
  enabled.
- `ZANALYTICS-ORGID` is added when the operation declares it; optional ones say so. Other header
  parameters are added disabled when optional.
- `CONFIG`: GET → query parameter (enabled with the first example when mandatory, disabled with the
  parameter's description when optional); POST/PUT/DELETE → `urlencoded` form field with the first
  example pretty-printed; imports → `formdata` with `CONFIG`, `FILE` (file) and `DATA` (disabled).
- The `_postman_id` of the committed collection is carried over so re-importing updates in place.
