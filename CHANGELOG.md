# Changelog

All notable changes to the Zoho Analytics API documents in this repository are recorded here.
Versions follow semantic versioning and describe the documentation, not the API: major for a removed
or renamed endpoint or a layout change, minor for additions (including a new API version directory),
patch for corrections. The OKF bundle's own content version is in `vN.N/okf/manifest.json`.

## Unreleased

### Changed - every artefact re-aligned to `v2.0/md/` (the source of truth)

A full audit of all 182 documented endpoints against the Zenesis OpenAPI, the samples and the
generated artefacts, before the initial release. Findings and the scripts that applied them are kept
outside the repository (`../analytics-api-audit/`).

- **Reports and Dashboards rewritten.** `REPORTS.md` and `DASHBOARDS.md` were replaced by the API
  team's new documents (new titles `Create Report`, `Read Report Metadata`, `Update Report`,
  `Read Dashboard Metadata`; a layout model, round-tripping rules and appendices). The OpenAPI was
  rebuilt from them: titles, descriptions, 57 chart types, every accepted axis-type spelling,
  the full operation / filter / user-filter vocabularies, `layout` as a JSON-encoded string with
  `contentSchema`, `displayName` max 100, card and theme ranges, `include` as a single section,
  Read Report Metadata's lossy response schemas, 41 + 30 error codes, throttles, examples, notes.
  The three dashboard listing APIs, which the new document did not cover, were re-added to
  `DASHBOARDS.md` as sections 4-6 from the previous revision so no published endpoint disappears.
  Dashboard code samples send `layout` as a string; the enumerations foundation of the OKF bundle
  was rewritten from the appendices.
- **Error codes.** Every row of every section's Error Codes table is now an `x-zenesis-statuscodes`
  entry on the operation (171 operations touched); the OKF error catalog grows accordingly.
- **Descriptions.** The opening paragraph of 142 operation descriptions now equals the section's
  opening paragraph.
- **Schemas.** 56 CONFIG fields documented in markdown but missing from the schemas were added
  (report bursts, tabbed-dashboard tabs, embed/publish/share permission flags, import overrides and
  more); 7 response fields were added; `importType`, `onError` and `exportType` enumerations and
  examples use the upper-case values the documents use; `required` lists follow the Mandatory
  column (Share Views, Remove Shared Views, Update Shared Details, Update Email Schedule, batch
  import, Get Shared Details, Create AutoML Analysis).
- Get My Permissions is `/share/userpermissions`; `/share/mypermissions` is the deprecated alias.
- OKF bundle 1.5.0, Postman collection and `v2.0/oas/` regenerated from the above.

## 3.0.0 - 2026-10-09

### Changed

- **One repository.** The Zoho Analytics API documents and every artefact built from them now live
  here, one directory per API version (`v2.0/`), replacing four repositories and the git-submodule
  wiring between them:
  - `v2.0/md`, `v2.0/zenesis-oas` (with `common/`), `v2.0/zenesis-oas-samples`, `v2.0/manifest.json`
    from `analytics-api-docs` (documentation version 2.0.0, at its latest working state);
  - `v2.0/oas` from `zoho/analytics-oas` `v2.0/`, regenerated from the Zenesis source
    (`reports-dashboards-grouped-api.json` picked up the axis-type wording the source already had);
    `v2.0/oas/common/` is the hand-placed copy and keeps its `zoho/analytics-oas` raw URL;
  - `v2.0/okf` rebuilt from the sources (bundle 1.4.0: 182 endpoints, 35 groups, 306 error codes,
    adds the Custom Roles and Tags groups that the published 1.3.0 bundle predates);
  - `v2.0/postman` regenerated from the OKF endpoint catalog and the OpenAPI examples.
- **Tools read and write inside the repository.** `tools/zenesis-oas` (formerly
  `zenesis-oas-convertor`) converts `vN.N/zenesis-oas` into `vN.N/oas` in place; `tools/okf`
  (formerly `okf-bundle`) builds `vN.N/okf`; both take `VERSION` / `--version`. The OKF domain and
  group inventory moved from the builder's `DOMAINS` table into `v2.0/manifest.json` (`okf` and
  `postman` blocks per domain and group). Hand-written OKF concepts are per version
  (`tools/okf/handwritten/v2.0/`), as are the converter's overlays (`overlays/v2.0/`).
- The Zenesis specifications' 361 `$ref`s to the shared components file now point at this
  repository's raw URL (`.../analytics-api/refs/heads/main/v2.0/zenesis-oas/common/...`);
  `common_ref` in `v2.0/manifest.json` and `source` in `tools/zenesis-oas/rules.json` follow.
- OKF bundle body links are relative to the containing document (frontmatter paths stay
  bundle-root), directory links target `index.md`, and every bundle ships a `llms.txt`.

### Added

- `tools/postman/build_postman.py`: the Postman collection and environment are generated, not
  maintained by hand. Curated input: `tools/postman/api-reference-links.json`.
- `tools/api-agent/`: `AGENT.md` (the AI-agent procedure for applying any input markdown to every
  artefact), `plan.py`, `scaffold.py`, `pipeline.py`.
- Publishing is a copy: `v2.0/oas/` goes as is into zoho/analytics-oas and `v2.0/okf/` as is into
  zoho/analytics-okf (`okf/llms.txt` is built against that repository's raw URL, `publish.okf.raw_base`
  in the root `manifest.json`). The former OKF packager and its `dist/` output are gone.
- A `**Permission Required**` row for the 24 endpoint sections that lacked one (Custom Roles, Tags,
  synchronous and asynchronous export, data sync and connectivity); the OKF permission matrix no
  longer has empty cells.
- Root `Makefile`, `.github/workflows/validate.yml`, `LICENSE.md`.
