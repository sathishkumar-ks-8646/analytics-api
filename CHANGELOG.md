# Changelog

All notable changes to the Zoho Analytics API documents in this repository are recorded here.
Versions follow semantic versioning and describe the documentation, not the API: major for a removed
or renamed endpoint or a layout change, minor for additions (including a new API version directory),
patch for corrections. The OKF bundle's own content version is in `vN.N/okf/manifest.json`.

## Unreleased

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
- `tools/okf/package_okf.py` now assembles the versioned layout of the standalone `analytics-okf`
  repository (root `llms.txt`, version index, one `vN.N/` per bundle).
- A `**Permission Required**` row for the 24 endpoint sections that lacked one (Custom Roles, Tags,
  synchronous and asynchronous export, data sync and connectivity); the OKF permission matrix no
  longer has empty cells.
- Root `Makefile`, `.github/workflows/validate.yml`, `LICENSE.md`.
