# 05 - Builder, validator and packager internals

## `tools/okf/build_okf.py`

Single-file generator, standard library only. Runs top to bottom: load configuration, load OpenAPI and
samples, parse markdown, aggregate error codes, render, write indexes. `main()` deletes and recreates
the bundle directory.

### Configuration tables (edit these; avoid editing the functions unless the format itself changes)

| Table | What it does | When to touch it |
|---|---|---|
| `DOMAINS` | Derived from `<VERSION>/manifest.json` at start-up: `(md folder, domain slug, domain title, oas file, [(md file stem, group slug, group title), ...])` from each domain's `folder`, `slug` and `okf` block. Drives directory names, titles, order in indexes, and the join of markdown files to OpenAPI files. | Never here - edit the manifest. |
| `LEGACY_ALIAS` | Maps the stem of a legacy cross-file link name (`X_API_DOC_INFO.md`) to a group slug when `kebab(stem)` is not already the slug. | A new markdown file whose legacy link name differs from its slug. |
| `TITLE_MAP` | OpenAPI operation title -> markdown `## N. Title` when they differ. | The build warns `no OAS operation for markdown endpoint` or `OAS operation without markdown section`. |
| `MD_ONLY_OPS` | Markdown title -> synthesized operation ID for endpoints that have no OpenAPI operation. | Documenting an endpoint before its OpenAPI exists. Remove the entry once the operation is added. |
| `LANG_FENCE`, `LANG_TITLE` | Sample language key -> code fence language and display name, in output order. | A new SDK language. |
| `DEFAULT_HTTP` | Error code -> HTTP status used when no sample response shows it. Everything else defaults to 400. | A new cross-cutting code with a non-400 status and no sample. |
| `ID_SOURCES` | Path or header parameter name -> `(human label, [endpoint titles that return it])`. Drives `/foundations/identifiers.md`. | A new path parameter, or a new endpoint that returns an existing ID. Titles must match markdown titles exactly. |
| `CANONICAL` | Error code -> `(meaning, resolution)` overriding the aggregated text for codes that appear in many operations (7005, 7103, 7104, 7301, 8083, 8535, 8080). | A code whose per-operation reasons are too specific to serve as the catalog headline. |
| `ANCHOR_ALIASES` | Old heading slug -> new slug for headings the renderer renames (for example `response-field-reference` -> `response-fields`). | Renaming a rendered section heading. |
| `FOUNDATION_TITLES` | Foundation path -> label used when relabelling `[Appendix A]`/`[Appendix B]` links. | Adding another appendix redirect. |
| `BASE_URL`, `OKF_VERSION`, `BUNDLE_VERSION` | Constants. `BUNDLE_VERSION` reads the `OKF_BUNDLE_VERSION` environment variable, else the version already in `<VERSION>/okf/manifest.json`, else `1.0.0`. | Releases: set the variable or pass `--version` to the packager. |
| `SOURCE_AUTHOR` | Author string on `sources` entries. | Never, unless the authoring team changes. |

### Pipeline functions

| Stage | Functions | Notes |
|---|---|---|
| Helpers | `slugify`, `overview_anchor`, `kebab`, `yq`, `yaml_dump`, `frontmatter`, `first_sentence`, `strip_md`, `write`, `shift_headings`, `md_table`, `html_to_md` | `frontmatter()` drops empty values, adds `generated.at`, keeps `status` last. `write()` collapses 3+ blank lines. `kebab()` is acronym-aware. |
| Load OpenAPI | module-level loop filling `OAS` (file -> doc) and `OPS` (markdown title -> operation record) | Uses `deref()` for `$ref` parameters. Records `config_loc` (`query`/`form`/`multipart`/`none`), `success`, `resp_ct`, `statuscodes`, `throttles`, `sections`, `samples`, `pointer`. |
| Parse markdown | module-level loop filling `GROUPS` and `ENDPOINTS`; helpers `parse_table`, `split_h3`, `parse_attr_table`, `remove_attr_table`, `parse_error_rows` | Also fills `heading_owner` (slug -> which endpoint or the overview owns it), `anchor_map`, `anchor_title` for link resolution. |
| Endpoint helpers | `ep_opid`, `ep_dir`, `ep_path`, `sdk_path`, `ep_method`, `ep_url`, `norm_org_header`, `config_info`, `classify_block`, `split_response_fields` | `classify_block` is the list of recognised `###` names. |
| Links | `legacy_group`, `resolve_anchor`, `relabel`, `rewrite_links`, `link_error_codes` | `rewrite_links(text, group, current_ep)` rewrites `#N-slug`, `#anchor`, `FILE.md#...`; with `current_ep=None` all links become absolute. `link_error_codes` links backticked known codes outside tables and fences. Unresolved targets are counted in `UNRESOLVED` and printed at the end. |
| Error aggregation | module-level loop filling `ERRORS[code]` with `rows` (markdown), `oas` (statuscodes), `constants`, `http`, `messages`, `ops`; `error_http`, `error_meaning`, `error_resolution` | Meaning precedence: `CANONICAL` > most common OpenAPI description > most common markdown reason > sample `errorMessage`. |
| Render | `render_endpoint`, `render_sdk`, `render_group_overview`, `render_domain_overview`, `render_error_catalog`, `render_error_quick_reference`, `render_scopes`, `render_rate_limits`, `render_permission_matrix`, `render_identifiers`, `render_endpoint_catalog`, `catalog_json`, `bundle_manifest` | Each returns `(bundle path, text)`. |
| Assemble | `main`, `write_indexes`, `write_root_index`, `write_log` | Copies `references/openapi`, copies `handwritten` expanding `{{NOW}}` and `{{BUILDER}}`, then writes indexes (ordered by `SLUG_ORDER`, titled by `SLUG_TITLES`). |

### Output of a successful run

```
endpoints=168 groups=33 errors=278 sdk=166
```

Any `WARN` or `unresolved links:` lines mean the sources need fixing before the result is trusted.

## `tools/okf/validate_okf.py`

Run with the bundle path or with no argument (it finds `okf/`, `<VERSION>/okf/` or the
current directory by looking for an `index.md` that declares `okf_version`). Checks:

- every non-reserved `.md` has frontmatter with a non-empty `type`;
- `index.md` has no frontmatter except at the bundle root;
- no `{{` placeholder survived; no `generated.by`;
- every `resource:` is an `http(s)` URL or a bundle path that exists;
- every markdown link resolves to a file, and every `#anchor` to a heading in the target (error catalog
  anchors `#error-<code>` are trusted);
- every directory has an `index.md` (warning).

Exit code 1 on any error. The published repo carries a copy as `tools/validate.py` and runs it in CI.

## `tools/okf/package_okf.py`

Assembles `dist/analytics-okf/`: copies the bundle to `okf/`, writes `README.md`, `llms.txt`,
`LICENSE.md`, `CHANGELOG.md`, `.gitignore`, `.github/workflows/validate-okf.yml`, copies the validator
to `tools/validate.py`, runs it, and optionally writes `dist/analytics-okf-<version>.tar.gz`.

Flags: `--version` (overrides the manifest version in the copy), `--repo-url`, `--site-url`,
`--docs-url`, `--base-url`, `--ref`, `--out`, `--tarball`. Their defaults are the `DEFAULT_*` constants at
the top of the file, so a plain run reproduces the published README and `llms.txt` exactly:
`DEFAULT_REPO` and `DEFAULT_SITE` are the intended permanent homes (used by the `git clone` line and the
"Canonical copies" footer); `DEFAULT_BASE_URL` is where the raw files are actually served from today
(used by every raw-file link in README and `llms.txt`). When the repository moves to `DEFAULT_REPO`, set
`DEFAULT_BASE_URL = None` and the raw base is derived from `--repo-url` again. Re-packaging preserves `dist/analytics-okf/.git`, so
commit history survives; the working tree is otherwise replaced wholesale.

The README and `llms.txt` text are templates inside `package_okf.py` (`readme()`, `llms_txt()`,
`changelog()`, `license_md()`). The changelog template only describes the first release; for later
releases edit `CHANGELOG.md` in `dist/analytics-okf/` directly after packaging, or extend the template.
