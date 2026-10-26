# `tools/okf/build_okf.py` — the configuration tables

A single-file generator, standard library only. It runs top to bottom: load configuration, load
OpenAPI and samples, parse markdown, aggregate error codes, render, write indexes. `main()` **deletes
and recreates** the bundle directory.

**Edit these tables; avoid editing the functions** unless the source format itself changed.

| Table | What it does | When to touch it |
|---|---|---|
| `DOMAINS` | derived from `<V>/manifest.json` at start-up: `(md folder, domain slug, domain title, oas file, [(md stem, group slug, group title), …])`. Drives directory names, titles, index order and the markdown↔OpenAPI file join | **never here — edit the manifest** |
| `LEGACY_ALIAS` | the stem of a legacy cross-file link name (`X_API_DOC_INFO.md`) → a group slug, when `kebab(stem)` is not already the slug | a new markdown file whose legacy link name differs from its slug |
| `TITLE_MAP` | OpenAPI operation title → markdown `## N. Title`, when the two genuinely differ | the build warns `no OAS operation for markdown endpoint` / `OAS operation without markdown section` |
| `MD_ONLY_OPS` | markdown title → a synthesised operation ID, for endpoints with no OpenAPI operation | documenting an endpoint before its operation exists. **Remove the entry once the operation lands** |
| `LANG_FENCE`, `LANG_TITLE` | sample language key → code fence and display name, in output order | a new SDK language |
| `DEFAULT_HTTP` | error code → HTTP status when no sample response shows one. Everything else defaults to **400** | a new cross-cutting code with a non-400 status and no sample |
| `ID_SOURCES` | path/header parameter name → `(human label, [endpoint titles that return it])`. Drives `/foundations/identifiers.md` | a new path parameter, or a new endpoint that returns an existing ID. **Titles must match markdown titles exactly** |
| `CANONICAL` | error code → `(meaning, resolution)`, overriding the aggregated text for codes that appear in many operations (7005, 7103, 7104, 7301, 8083, 8535, 8080) | a code whose per-operation reasons are too specific to serve as the catalog headline |
| `ANCHOR_ALIASES` | old heading slug → new slug, for headings the renderer renames (e.g. `response-field-reference` → `response-fields`) | renaming a rendered section heading |
| `FOUNDATION_TITLES` | foundation path → the label used when relabelling `[Appendix A]` / `[Appendix B]` links | adding another appendix redirect |
| `BASE_URL`, `OKF_VERSION`, `BUNDLE_VERSION` | constants. `BUNDLE_VERSION` reads `OKF_BUNDLE_VERSION`, else the version already in `<V>/okf/manifest.json`, else `1.0.0` | releases |
| `SOURCE_AUTHOR` | the author string on `sources` entries | never, unless the authoring team changes |

## Pipeline functions, for orientation

| Stage | Functions | Notes |
|---|---|---|
| helpers | `slugify`, `overview_anchor`, `kebab`, `yq`, `yaml_dump`, `frontmatter`, `first_sentence`, `strip_md`, `write`, `shift_headings`, `md_table`, `html_to_md` | `frontmatter()` drops empty values, adds `generated.at` and keeps `status` last. `write()` collapses 3+ blank lines. `kebab()` is acronym-aware |
| load OpenAPI | a module-level loop filling `OAS` (file → doc) and `OPS` (markdown title → operation record) | uses `deref()` for `$ref` parameters; records `config_loc` (`query`/`form`/`multipart`/`none`), `success`, `resp_ct`, `statuscodes`, `throttles`, `sections`, `samples`, `pointer` |
| parse markdown | a module-level loop filling `GROUPS` and `ENDPOINTS`; `parse_table`, `split_h3`, `parse_attr_table`, `remove_attr_table`, `parse_error_rows` | also fills `heading_owner` (slug → which endpoint or overview owns it), `anchor_map`, `anchor_title` for link resolution |
| endpoint helpers | `ep_opid`, `ep_dir`, `ep_path`, `sdk_path`, `ep_method`, `ep_url`, `norm_org_header`, `config_info`, `classify_block`, `split_response_fields` | `classify_block` **is** the list of recognised `###` names |
| links | `legacy_group`, `resolve_anchor`, `relabel`, `rewrite_links`, `link_error_codes` | `rewrite_links(text, group, current_ep)` rewrites `#N-slug`, `#anchor`, `FILE.md#…`; with `current_ep=None` every link becomes absolute. `link_error_codes` links backticked known codes **outside tables and fences**. Unresolved targets are counted in `UNRESOLVED` and printed at the end |
| error aggregation | a module-level loop filling `ERRORS[code]` with `rows`, `oas`, `constants`, `http`, `messages`, `ops`; `error_http`, `error_meaning`, `error_resolution` | **meaning precedence:** `CANONICAL` > most common OpenAPI description > most common markdown reason > sample `errorMessage` |
| render | `render_endpoint`, `render_sdk`, `render_group_overview`, `render_domain_overview`, `render_error_catalog`, `render_error_quick_reference`, `render_scopes`, `render_rate_limits`, `render_permission_matrix`, `render_identifiers`, `render_endpoint_catalog`, `catalog_json`, `bundle_manifest` | each returns `(bundle path, text)` |
| assemble | `main`, `write_indexes`, `write_root_index`, `write_log` | copies `references/openapi`, copies `handwritten` expanding `{{NOW}}` and `{{BUILDER}}`, then writes indexes ordered by `SLUG_ORDER` and titled by `SLUG_TITLES` |

## Reading the output line

```
endpoints=182 groups=35 errors=352 sdk=180
```

| Count | Means | If it is wrong |
|---|---|---|
| `endpoints` | markdown sections successfully turned into endpoint documents | a new endpoint did not raise it → the `## N. Title` heading is malformed, or the file is not in the manifest |
| `groups` | group overviews written | a new group did not raise it → the manifest entry or the markdown file is missing |
| `errors` | **distinct error codes in the catalog**, not failures | a new code did not raise it → the first table cell is not a bare numeric code |
| `sdk` | operations with an SDK Example | did not rise → the samples path template or lower-case method does not match the spec |

`endpoints` minus `sdk` is the number of endpoints with no samples. Any `WARN` line or
`unresolved links:` block means the sources need fixing before the result is trusted.

## Invariants

Enforced by `tools/okf/validate_okf.py` unless marked *convention* — a rule the generator relies on
but does not independently check.

| Invariant | Enforced by |
|---|---|
| every non-reserved `.md` has frontmatter with a non-empty `type` | validator |
| `index.md` and `log.md` carry no frontmatter, except the root `index.md` (`okf_version: "0.2"`) | validator |
| no `{{` placeholder survives into the built bundle | validator |
| no `generated.by` in any frontmatter | validator + `frontmatter()` |
| every `resource:` is an `http(s)` URL or a bundle path that exists | validator |
| every markdown link resolves, and every `#anchor` resolves to a heading (`#error-<code>` trusted) | validator |
| every directory has an `index.md` | validator *(warning)* |
| `operationId` is unique across every OpenAPI file | **convention** — it is the join key for file names, catalog, SDK docs and manifest |
| `## N.` numbering in a group file is contiguous | **convention** — `#N-slug` intra-file links depend on it |
| `## N. Title` == `x-zenesis-title` (or `summary`), or a `TITLE_MAP` entry bridges them | **convention** — otherwise a `WARN` and no join |
| samples JSON keys match the OpenAPI path template and lower-case method | **convention** — otherwise no SDK Example |
| `<V>/okf/` is never hand-edited | **convention** — it is deleted and regenerated |

## Things that must never appear

- internal system details in prose — Java class names, XML security attribute names, template names,
  or file names of the authoring system;
- hand-written links to the error catalog (use a backticked code and let `link_error_codes` do it);
- `generated.by` in any frontmatter;
- unexpanded `{{NOW}}` / `{{BUILDER}}` outside `handwritten/**`;
- edits inside `<V>/okf/`;
- content from outside this repository (older `PRD/` folders, zip archives) — not sources.
