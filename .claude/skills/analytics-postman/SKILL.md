---
name: analytics-postman
description: Build and maintain the Zoho Analytics Postman collection and environment in <VERSION>/postman/ of the analytics-api repository, generated from the OKF bundle, the published OAS, the markdown and the manifest. Use when regenerating the collection, when build_postman.py --check reports STALE, when a request has no description, a wrong CONFIG example, a missing header or a missing identifier variable, when curating tools/postman/api-reference-links.json so a request stops saying "newly added", or when editing the collection or folder description templates.
---

# Build the Postman collection from the already-built artefacts

`<VERSION>/postman/` holds two generated, committed files:

```
Zoho Analytics REST APIs.postman_collection.json
Zoho Analytics REST Variables.postman_environment.json
```

**Nothing there is edited by hand.** Re-running regenerates both.

```bash
python3 tools/postman/build_postman.py --version <V>          # writes <V>/postman/
python3 tools/postman/build_postman.py --version <V> --check  # build in memory, exit 1 if the files on disk differ
python3 tools/postman/build_postman.py --version <V> --out /tmp/pm
```

A successful write run ends with the counts, e.g. `requests=182 domains=10 sections=35`.
`--check` instead prints one line per file — `ok <path>` when it matches, `STALE <path>` when it
does not — and exits 1 on any `STALE`.

This is the **last** stage of the chain: it reads what the OKF and OAS builds produced, so
`tools/okf/build_okf.py` must have run first. `tools/api-agent/pipeline.py` enforces the order.

## 1. What it reads, and what each input controls

| Input | Controls |
|---|---|
| `<V>/okf/references/endpoint-catalog.json` | **the request list** — title, method, path, scopes, organization header, CONFIG location, success status, permission, document paths |
| `<V>/okf/domains/**/*.md` | endpoint one-line descriptions and group descriptions, from the frontmatter |
| `<V>/okf/workflows/*.md` | the **playbook tables** on domain and section folders: title, description, step labels, the endpoints each one uses |
| `<V>/oas/*.json` | the ready-to-send **CONFIG example** on each request (the *first* example), the other example names, header parameters such as `ZANALYTICS-DEST-ORGID`, multipart parts |
| `<V>/md/<domain>/<GROUP>.md` | the opening paragraph of each section folder |
| `<V>/manifest.json` | domain order, and each domain's `postman` block: `emoji`, `title`, `covers` |
| `tools/postman/templates/authentication-folder.json` | the 🔐 Authentication folder (generate, refresh, revoke), carried verbatim |
| `tools/postman/templates/collection-skeleton.json` | collection-level auth (`Bearer {{access-token}}`) and the pre-request script that URL-encodes `CONFIG` on GET requests |
| `tools/postman/templates/collection-description.md`, `version-folder-description.md` | the long descriptions; counts and the per-domain table are regenerated into them |
| `tools/postman/api-reference-links.json` | endpoint title → page in the public API reference. **Curated by hand** |

So: to change a **request**, change the source that produced its catalog entry — the markdown
section or the Zenesis operation — and rebuild the chain. Nothing in `<V>/postman/` is a source.

## 2. What it produces

```
Zoho Analytics REST APIs
├── 🔐 Authentication            ← templates/authentication-folder.json, verbatim
└── 2️⃣ v2.0
    ├── 🏢 Organization Management        ← manifest `postman.emoji` + `postman.title`
    │   └── Organization Info & Settings  ← the group's `okf.title`
    │       └── Get Resource Details      ← the markdown `## N. Title`
    ├── 👥 Users & Groups
    └── … one folder per domain, in manifest order
```

Conventions in the output:

- **Request names are the endpoint titles** of the API reference — the markdown `## N. Title`.
  Domain folders are `emoji title`; section folders are the OKF group title.
- **URLs** are `https://{{analytics-domain}}/restapi/v2/…` with every path parameter as a Postman
  variable of the same name (`{{workspace-id}}`).
- `ZANALYTICS-ORGID` is added when the operation declares it; optional ones say so. Other header
  parameters are added **disabled** when optional.
- **CONFIG**, by location:
  - `query` (GET) → a query parameter. Enabled with the first example when mandatory; **disabled**,
    carrying the parameter's description, when optional.
  - `form` (POST/PUT/DELETE) → an `urlencoded` form field with the first example pretty-printed.
  - `multipart` (imports) → `formdata` with `CONFIG`, `FILE` (type `file`) and `DATA` (disabled).
- A collection-level **pre-request script** URL-encodes the `CONFIG` query value on every GET,
  because Postman keeps query values verbatim and the API requires them encoded.
- Collection auth is `Bearer {{access-token}}`.
- **The `_postman_id` of the committed collection is carried over**, so re-importing updates the
  collection in place rather than creating a duplicate. Never clear it by hand.

### The environment

`Zoho Analytics REST Variables` — enabled variables are the ones a user must fill or already has:

```
analytics-domain = analyticsapi.zoho.com     accounts-domain = accounts.zoho.com
client-id   client-secret   redirect-uri   access-token   refresh-token   expiry-time
organization-id
```

Every **identifier** variable ships **disabled**, so an unfilled ID is visible rather than silently
sent empty: `workspace-id`, `view-id`, `column-id`, `folder-id`, `group-id`, `role-id`,
`querytable-id`, `formula-id`, `variable-id`, `job-id`, `datasource-id`, `tag-id`, `dashboard-id`,
`slide-id`, `schedule-id`, `analysis-id`, `model-id`, `deployment-id`, `dest-organization-id`.

A new path parameter adds a new disabled variable automatically — it comes from the catalog.

## 3. `api-reference-links.json` — the one curated input

```json
{
  "Add Aggregate Formula": "https://www.zoho.com/analytics/api/v2/modeling-api/add-aggregate-formula.html",
  "Update Email Schedule":  "https://www.zoho.com/analytics/api/v2/…"
}
```

- Keyed by the **endpoint title**, exactly as the markdown `## N. Title` spells it.
- A request whose title is absent says **"newly added"** and links the OpenAPI file instead. That is
  correct behaviour for an endpoint with no public page yet — leave it out rather than guessing a URL.
- **Renaming an endpoint title means renaming the key here too**, or the link silently disappears.
- Add the entry when the endpoint gets a public documentation page, then rebuild.

## 4. Changing anything

| What you want to change | Edit | Then |
|---|---|---|
| a request's name | the markdown `## N. Title` **and** `x-zenesis-title` **and** the key in `api-reference-links.json` | full pipeline |
| a request's description | the OpenAPI `description` (→ OKF frontmatter `description`) | `--from okf` |
| the CONFIG body shown | the **first** example on the operation in `<V>/zenesis-oas/` | full pipeline |
| a header on the request | the operation's `parameters` (`in: header`) | full pipeline |
| a multipart part | the operation's `requestBody` properties (`FILE`, `DATA`) | full pipeline |
| the section-folder blurb | the opening paragraph of `<V>/md/<domain>/<GROUP>.md` | `--only postman` |
| the domain folder emoji / title / "covers" line | the domain's `postman` block in `<V>/manifest.json` | `--only postman` |
| the playbook tables on folders | `tools/okf/handwritten/<V>/workflows/*.md` | `--from okf` |
| the Authentication folder | `tools/postman/templates/authentication-folder.json` | `--only postman` |
| collection auth or the GET pre-request script | `tools/postman/templates/collection-skeleton.json` | `--only postman` |
| the long collection / version descriptions | `tools/postman/templates/collection-description.md`, `version-folder-description.md` (counts and the per-domain table are regenerated into them) | `--only postman` |
| the public docs link on a request | `tools/postman/api-reference-links.json` | `--only postman` |

Because the CONFIG example comes from `<V>/oas/`, a change to the **first** example on an operation
needs the whole chain — `to-analytics` must run before the Postman build sees it.

## 5. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `--check` reports `STALE` | a source changed after the last build | rebuild and commit both files |
| a new endpoint is missing from the collection | it is not in `okf/references/endpoint-catalog.json` | rebuild OKF; if it is missing there too, the markdown↔OpenAPI title join failed → `analytics-okf` |
| a request says "newly added" | no entry in `api-reference-links.json` | add it if a public page exists; otherwise correct |
| a request has no description | the OKF endpoint frontmatter `description` is empty | give the operation a `description` in `<V>/zenesis-oas/` |
| the CONFIG field is empty or wrong | the operation has no example, or the wrong one is first | add/reorder `examples` on the operation — the **first** one wins |
| a GET sends an unencoded CONFIG | the pre-request script was removed | restore `templates/collection-skeleton.json` |
| a path variable is missing from the environment | the parameter is not declared `in: path` on the operation | fix the operation's `parameters` |
| re-importing creates a duplicate collection | `_postman_id` changed | restore it from git; the generator carries over the committed one |
| the domain folder has no emoji | the domain's `postman` block is missing from `<V>/manifest.json` | add `emoji`, `title`, `covers` |
| folder playbook tables are missing | no `workflows/*.md` referenced those endpoints | add or extend a playbook under `tools/okf/handwritten/<V>/workflows/` |

## 6. Publish

Import both files into the Postman workspace: the collection and the environment. The carried-over
`_postman_id` makes the import update the existing collection in place. Nothing in this repository
pushes to Postman.
