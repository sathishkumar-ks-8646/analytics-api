---
name: analytics-okf
description: Build, validate, extend and publish the Open Knowledge Format v0.2 bundle in <VERSION>/okf/ of the analytics-api repository - the AI-agent-facing knowledge base generated from <VERSION>/md/, <VERSION>/zenesis-oas/, <VERSION>/zenesis-oas-samples/ and the hand-written concepts in tools/okf/handwritten/. Use when rebuilding or validating the bundle, when the build prints WARN "no OAS operation for markdown endpoint" / "OAS operation without markdown section" / "unresolved links", when a foundation, workflow playbook, error code, identifier or permission row needs changing, or when stamping a bundle version for release.
---

# Build the OKF bundle from the markdown, the specs and the samples

`<VERSION>/okf/` is an **Open Knowledge Format v0.2 bundle**: the whole API as linked Markdown
concepts with YAML frontmatter, built for AI agents. It is published to `zoho/analytics-okf` and
pointed at by `llms.txt`.

**It is deleted and recreated on every build.** Anything written there by hand is silently
discarded. Fix the sources.

```bash
python3 tools/okf/build_okf.py --version <V>        # → endpoints=182 groups=35 errors=352 sdk=180
python3 tools/okf/validate_okf.py <V>/okf           # → errors=0 warnings=0 broken_links=0
```

Both must be clean — **and the build must print no `WARN` and no `unresolved links:`** — before the
result is trusted. A `WARN` is not advisory here; it means an endpoint lost its schema or a link
points nowhere.

> `build_okf.py` takes no `--help`. Any invocation **runs the build**, rewriting `<V>/okf/`.

## 1. What goes in

| Input | Supplies |
|---|---|
| `<V>/manifest.json` | the `DOMAINS` table: domain folders, slugs, titles, spec files, group `(md stem, slug, title)` — directory names, titles, index order, and the markdown↔OpenAPI join |
| `<V>/md/<domain>/<GROUP>.md` | every endpoint's narrative, attribute table, CONFIG tables, samples, notes, error rows; the group overview |
| `<V>/zenesis-oas/*.json` | operation IDs, scopes, parameters, CONFIG location, success status, schemas, `x-zenesis-*`; copied verbatim into `/references/openapi/` |
| `<V>/zenesis-oas-samples/*.json` | the SDK Example concepts |
| `tools/okf/handwritten/<V>/` | `overview.md`, `how-to-use-this-bundle.md`, 13 `foundations/`, 8 `workflows/` playbooks |
| the common file | the full OAuth scope list, summary constants for common error codes |

## 2. What comes out

```
<V>/okf/
├── index.md                    root listing (carries okf_version: "0.2")
├── log.md                      update log
├── manifest.json               name, version, okf_version, counts, entry points
├── llms.txt                    AI entry point; links built against publish.okf.raw_base
├── overview.md                 API Overview        ← handwritten
├── how-to-use-this-bundle.md   Guide               ← handwritten
├── endpoint-catalog.md         API Catalog         ← generated
├── foundations/                15 handwritten + 6 generated + index.md
├── domains/<domain>/<group>/   API Domain / API Group overviews + one API Endpoint per operation
├── workflows/                  Playbooks           ← handwritten
├── sdk-examples/<domain>/<group>/   one SDK Example per operation with samples
└── references/
    ├── openapi/*.json          copies of the Zenesis specs + the common file
    └── endpoint-catalog.json   machine-readable catalog — Postman's primary input
```

Generated foundations (rebuilt every run, never edit): `error-codes.md`,
`error-codes-quick-reference.md`, `oauth-scopes.md`, `rate-limits-and-quotas.md`,
`permission-matrix.md`, `identifiers.md`, plus the root `index.md` of the directory.

Hand-written foundations (copied as is, **not** regenerated — review them whenever a rule they
describe changes): `authentication`, `data-centers`, `request-conventions`, `response-envelope`,
`http-status-codes`, `roles-and-permissions`, `custom-roles`, `filter-criteria-syntax`,
`asynchronous-jobs`, `white-label-client-portal`, `export-formats-and-enums`,
`import-options-and-enums`, `report-and-dashboard-enums`, `glossary`, `sdk-clients`.

Every directory gets an `index.md` listing `overview.md` first, then concepts (title and description
from their frontmatter), then subdirectories.

The complete section-by-section map of an API Endpoint document, its frontmatter contract and the
naming rules are in [`references/endpoint-document-map.md`](references/endpoint-document-map.md).
The builder's configuration tables are in
[`references/builder-tables.md`](references/builder-tables.md). The exhaustive originals live in
`tools/okf/agent-guide/02-bundle-structure.md` and `05-builder-internals.md`.

## 3. The joins that must hold

The builder stitches three sources together. Each join has one key, and a broken join is silent
except for a `WARN`.

| Join | Key | Breaks as |
|---|---|---|
| markdown section ↔ OpenAPI operation | `## N. Title` == `x-zenesis-title` (else `summary`), character for character | `WARN no OAS operation for markdown endpoint: <title>` / `WARN OAS operation without markdown section` → the endpoint document has **no schema** |
| operation ↔ SDK samples | the exact path template + lower-case method | no SDK Example document, no `api.sdk_examples`, silently |
| manifest ↔ files | domain `folder`/`slug`, group `md`/`tag`/`okf.slug` | the source validator errors first |
| intra-document links | `[Title](#N-slug)`, with contiguous `## N.` numbering | `unresolved links:` |
| cross-file links | the **legacy** name pattern `<GROUP>_API_DOC_INFO.md#N-slug` | `unresolved links:` |

**Cross-file links use legacy file names, not the current ones** — `VIEW_OPERATIONS_API_DOC_INFO.md`,
`COLUMNS_API_DOC_INFO.md`, `ROW_API_DOC_INFO.md`, `ORG_INFO_API_DOC_INFO.md`,
`TRASH_API_DOC_INFO.md`, `SLIDESHOW_API_DOC_INFO.md`, `EMBEDURL_API_DOC_INFO.md`,
`DOMAIN_AND_WHITELABEL_API_DOC_INFO.md`, `AUTOML_API_DOC_INFO.md`; otherwise
`<MD FILE STEM>_API_DOC_INFO.md`. The builder rewrites them to bundle paths and replaces the label
when it is the file name. `#appendix-a--common-http-headers` and `#appendix-b--oauth-scope-summary`
resolve to the foundations.

If a title genuinely must differ between the two sides, add a `TITLE_MAP` entry in
`tools/okf/build_okf.py`. If an endpoint has no OpenAPI operation yet, add a `MD_ONLY_OPS` entry —
and remove it the moment the operation lands.

## 4. Changing the bundle: always change a source

| What you want to change | Edit |
|---|---|
| anything about one endpoint | the markdown section and/or the Zenesis operation — never the endpoint document |
| the group overview prose | the markdown file's preamble and its non-endpoint `##` sections (Appendix C/D are copied in; Index, Appendix A, Appendix B are skipped) |
| the domain overview prose | `info.description` and `tags[].description` of the domain's Zenesis spec |
| a cross-cutting rule (auth, headers, criteria syntax, roles, data centres, enums, glossary, SDK clients) | the file under `tools/okf/handwritten/<V>/foundations/` |
| a multi-endpoint procedure | a file under `tools/okf/handwritten/<V>/workflows/` — these also become the **playbook tables in the Postman collection** |
| the headline counts in `overview.md` | by hand — they are typed, not generated |
| a new OAuth scope | `<V>/zenesis-oas/common/zoho-analytics-api-common.json` (drives `/foundations/oauth-scopes.md`) |
| the catalog headline for a code used by many operations | `CANONICAL` in `build_okf.py` |
| the HTTP status of a code with no sample response | `DEFAULT_HTTP` in `build_okf.py` (everything else defaults to 400) |
| an identifier's label, or which endpoints return it | `ID_SOURCES` in `build_okf.py` — **the titles must match markdown titles exactly** |

### Hand-written concept frontmatter

```yaml
---
type: Reference          # or Concept, Authentication, Guide, Playbook, API Overview
title: Filter Criteria Syntax
description: How criteria expressions are written, escaped and combined.
---
```

- `type` must be non-empty — the validator errors otherwise.
- **A `title` or `description` containing `: ` must be quoted**, or the build fails with
  `frontmatter is not valid YAML`.
- `{{NOW}}` and `{{BUILDER}}` are expanded during the copy. They are valid **only** inside
  `handwritten/**`; one surviving into the bundle is a validation error.
- Never write `generated.by`.
- Every `resource:` must be an `http(s)` URL or a bundle path that exists.

## 5. Bundle versioning

Two numbers; do not conflate them.

| Name | Meaning | Lives in | Changes when |
|---|---|---|---|
| `OKF_VERSION` | the OKF **spec** version the bundle conforms to (`0.2`) | root `index.md` frontmatter, `manifest.json` | only on adopting a newer OKF spec — not a routine action |
| `BUNDLE_VERSION` | this bundle's **content** version | `<V>/okf/manifest.json` | per release |

`BUNDLE_VERSION` is read from `OKF_BUNDLE_VERSION`, else the version already in
`<V>/okf/manifest.json`, else `1.0.0`. Without the variable the builder **keeps** the existing
version, so a routine rebuild does not bump it.

```bash
OKF_BUNDLE_VERSION=1.5.0 python3 tools/okf/build_okf.py --version <V>
python3 tools/api-agent/pipeline.py --version <V> --from okf --bundle-version 1.5.0
```

The tooling defines no semver policy — the repository's convention is minor for additions, patch for
corrections, major for removals or renames.

## 6. Validation

`tools/okf/validate_okf.py` (run with the bundle path, or with no argument from inside it) checks:

- every non-reserved `.md` has frontmatter with a non-empty `type`;
- `index.md` and `log.md` carry no frontmatter, except the root `index.md` which declares
  `okf_version`;
- no `{{` placeholder survived; no `generated.by` anywhere;
- every `resource:` is an `http(s)` URL or a bundle path that exists;
- every markdown link resolves to a file, and every `#anchor` to a heading in that file
  (`#error-<code>` anchors are trusted);
- every directory has an `index.md` *(warning)*.

Exit code 1 on any error. The published repository carries a copy as `tools/validate.py` and runs it
in CI.

## 7. Troubleshooting

| Message | Meaning | Fix |
|---|---|---|
| `WARN no OAS operation for markdown endpoint: <title>` | the title does not match any `x-zenesis-title` | make the two identical, or add `TITLE_MAP` / `MD_ONLY_OPS` |
| `WARN OAS operation without markdown section` | an operation nothing in `md/` documents | write the section, or fix the title |
| `unresolved links:` | a link to a heading, a legacy file name or an anchor the builder cannot resolve | fix the link; check the `## N.` numbering and the legacy name pattern (§3) |
| `API Endpoint has empty api.permission_required` / `empty permission cell` | the section has no `\| **Permission Required** \|` row | add it; copy a sibling endpoint's wording if the input is silent, and say so |
| `frontmatter is not valid YAML` | a hand-written `title`/`description` contains `: ` | quote the value |
| `{{NOW}}` in the bundle | a placeholder outside `handwritten/**` | move it, or remove it |
| `sdk=` did not rise after adding an endpoint | the samples key does not match the spec path/method | → `analytics-oas-samples` |
| the endpoint document has no CONFIG section | the markdown `###` block name is not one the classifier recognises | use one of: `CONFIG Parameter(s)`, `URL Parameters`, `FIELDS FOR CONFIG JSON`, `Sample values for CONFIG parameter`, `Query Parameters`, `Request Parameters`, `Request Body` |
| a note landed under "Notes & Behaviour" unexpectedly | an unrecognised `###` block name — that is the fallback bucket | rename the block |
| the error catalog shows HTTP 400 for a code that returns 403 | no sample response shows the status | add a `**HTTP 403 Forbidden — …**` line above a ```json block containing `"errorCode": N`, or add `DEFAULT_HTTP` |
| a dangling `TITLE_MAP` / `MD_ONLY_OPS` / `ID_SOURCES` entry after a removal | stale builder config | delete the entry |

**Never hand-write a link to the error catalog.** A backticked 4-to-6-digit known code in prose is
auto-linked to `#error-<code>`; a hand-written link will not match reliably.

**Never put internal system details in the prose** — Java class names, XML security attribute names,
template names, or file names of the authoring system. Endpoint text reads as if written for an
external API consumer.

## 8. Release and publish

```bash
# 1. rebuild from current sources, stamping the content version
OKF_BUNDLE_VERSION=X.Y.Z python3 tools/okf/build_okf.py --version <V>     # no WARN, no unresolved links

# 2. validate
python3 tools/okf/validate_okf.py <V>/okf                                 # errors=0 warnings=0 broken_links=0

# 3. review and commit here, sources and bundle together
git diff --stat <V>/okf

# 4. publish: copy as is
cp -r <V>/okf/. ../analytics-okf/<V>/
```

`<V>/okf/llms.txt` is already built with absolute links under the public repository's raw URL
(`publish.okf.raw_base` in the root `manifest.json`), so nothing is rewritten on copy. That
repository's own root files — `llms.txt` version index, `manifest.json`, `README.md`,
`CHANGELOG.md`, `LICENSE.md`, `tools/validate.py` — are maintained **there**, by hand, when the
bundle version or the counts change. Nothing in this repository pushes anywhere.

`tools/okf/package_okf.py` assembles a standalone `dist/analytics-okf/` with its own README,
`llms.txt`, licence, changelog, CI workflow and a copy of the validator; it preserves
`dist/analytics-okf/.git` so history survives re-packaging.

Finally, `okf/` is **Postman's primary input** — continue with
`python3 tools/api-agent/pipeline.py --version <V> --only postman` (→ `analytics-postman`).
