# Changelog

All notable changes to the Zoho Analytics API documents in this repository are recorded here.
Versions follow semantic versioning and describe the documentation, not the API: major for a removed
or renamed endpoint or a layout change, minor for additions (including a new API version directory),
patch for corrections. The OKF bundle's own content version is in `vN.N/okf/manifest.json`.

## Unreleased

### Added - a consumer-facing migration guide

`migration/v2-mandatory-org-context/` — eight chapters explaining this change to an external developer:
why organization context is mandatory, what changed, endpoint-by-endpoint migration with full
before-and-after payloads, SDK migration for all seven languages, how each knowledge base and tool
adopts it, the deprecation timeline to **March 2027**, and a troubleshooting/FAQ chapter.

Markdown is the authored form; `build.py` renders an `.html` sibling for each chapter with shared
navigation, and `--check` validates every internal link and anchor. `migration/` is the first tree in
this repository written for API consumers rather than for the repository itself.

### Removed - the user-scoped listings that were not bound to an organization

The listings that reported across every organization the caller belongs to, and that did not mandate
the `ZANALYTICS-ORGID` header, are gone. Source: `v2.0/temp/ORG_LEVEL_LISTINGS.md` (API team hand-off).

| Removed endpoint | Method | Path | Replacement |
|---|---|---|---|
| Get Org List (`Get Organizations`) | GET | `/restapi/v2/orgs` | Read the Organization ID from **Settings → Organisation** in the Zoho Analytics UI. |
| Get Owned Workspace List | GET | `/restapi/v2/workspaces/owned` | Get Org Workspaces |
| Get Shared Workspace List | GET | `/restapi/v2/workspaces/shared` | Get Org Workspaces |
| Get Owned Dashboards | GET | `/restapi/v2/dashboards/owned` | Get Org Dashboards |
| Get Shared Dashboards | GET | `/restapi/v2/dashboards/shared` | Get Org Dashboards |
| Get Recent Views | GET | `/restapi/v2/recentviews` | Get Org Recent Items |
| Get All Workspace List | GET | `/restapi/v2/workspaces` | Get Org Workspaces |
| Get All Dashboards | GET | `/restapi/v2/dashboards` | Get Org Dashboards |

`POST /restapi/v2/workspaces` (Create Workspace) is unaffected - only the `GET` on that path is gone.
Every remaining v2 endpoint now mandates the `ZANALYTICS-ORGID` header; there is no user-scoped
cross-organization endpoint left in the surface.

### Added - `Org Level Listings`, a new API group in Organization Management

`v2.0/md/01 · Organization Management/ORG_LEVEL_LISTINGS.md`, the tag `Org Level Listings` in
`org-management-grouped-api.json`, and the OKF group `organization-management/org-level-listings`.
All three endpoints take a mandatory `ZANALYTICS-ORGID` header and `ZohoAnalytics.metadata.read`.

| Endpoint | Method | Path | CONFIG |
|---|---|---|---|
| Get Org Workspaces | GET | `/restapi/v2/orgs/workspaces` | none |
| Get Org Dashboards | GET | `/restapi/v2/orgs/dashboards` | optional - `workspaceIds`, `pageNo`, `recordsPerPage`, `searchKey` |
| Get Org Recent Items | GET | `/restapi/v2/orgs/recentitems` | none |

### Changed - `ZANALYTICS-ORGID` is now mandatory on Get Workspace Info and Get View Details

Both resolved their target across organizations; both are now scoped to the organization named in the
header, and both gained `8083` and `8084` in their error tables. In the SDKs they move off
`AnalyticsClient`:

- `getWorkspaceDetails` moves to **WorkspaceAPI** and loses its `workspaceId` argument (the instance
  carries it); it now accepts the optional `config` with `withUserRoleInfo`.
- `getViewDetails` moves to **OrgAPI** and keeps `(viewId, config)`.

### Changed - the organization ID no longer comes from an API

Every place that told a reader to call Get Org List for `orgId` - the `ZANALYTICS-ORGID` parameter
descriptions in all ten specifications, `foundations/identifiers.md`, the bootstrap workflow, the
Postman collection and folder descriptions, and the header rows of nine group documents - now points
at **Settings → Organisation** in the Zoho Analytics UI.

### Changed - all seven SDKs

Removed from `AnalyticsClient`: `getOrgs`, `getWorkspaces`, `getOwnedWorkspaces`,
`getSharedWorkspaces`, `getRecentViews`, `getDashboards`, `getOwnedDashboards`,
`getSharedDashboards` (plus `getWorkspaceDetails` and `getViewDetails`, which moved).
`AnalyticsClient` now carries only configuration and the four `get*Instance` factories.
Added to `OrgAPI`: `getOrgWorkspaces`, `getOrgDashboards(config)`, `getOrgRecentItems`,
`getViewDetails(viewId, config)`. Added to `WorkspaceAPI`: `getWorkspaceDetails(config)`.
Sample programs, `ruby/README.md` and `<lang>/docs/` are regenerated to match.

The OKF bundle goes to **2.0.0** (endpoints removed). Counts: 10 domains, 40 groups, 134 paths,
203 operations, 205 bundle endpoints.

### Fixed - Go SDK parity and three defects in the SDK reference generator

A cross-language comparison of all seven SDK surfaces (Go against Python, Node.js, Java, C#, PHP and
Ruby) turned up four real defects, all now fixed:

- **Go carried three misspelled duplicate methods** - `GetDashboars`, `GetOwnedDashboars` and
  `GetSharedDashboars`, byte-identical to the correctly spelled `GetDashboards` trio that was added
  later. Both sets were live public API and both were published in `go/docs/`. The misspelled trio is
  removed from `go/source/` and from `go/sample/test.go`, which defined callers for both.
- **Go was the only SDK missing `ImportRawData` and `ImportRawDataInNewTable`** (present in the other
  six). Both are added to Go's `BulkAPI`, with a `sendRawImportAPIRequest`/`submitRawImportRequest`
  transport pair that posts the payload as a `DATA` multipart field, matching the Java client.
  `go/sample/test.go` gained the two matching sample functions.
- **`tools/sdkdocs/extract.py` silently dropped every method whose parameter list wrapped across
  lines.** The parsers match `name(args)` on one physical line, so 30+ public methods - the whole
  AutoML family in Java/Go/C#/PHP/Node.js, plus `sortDataByColumns`, `exportDataUsingSQL`,
  `getWorkspaceMetadata`, `importDataInBatches`, C#'s `ExportData` and Python's two
  `import_*_as_batches` - existed in the sources but appeared in no reference page. A `_fold_signatures`
  helper now joins wrapped declarations before parsing, keeping line indexes stable. Documented method
  counts: Java 218->225, C# 215->222, PHP 219->221, Node.js 218->220, Python 214->216, Go 205->210.
- **The Python sample raised `NameError`** in `import_raw_data` and `import_raw_data_in_new_table`:
  both assigned `raw_bulk` and passed `raw_data`.

Every Go snippet in `v2.0/zenesis-oas-samples/` was verified against the Go package's real exported
surface, and all 1,687 snippets across the seven languages now resolve to a method that exists. The
Go package and `go/sample/test.go` both build and vet clean.

Note for anyone verifying Go locally: a stale copy of this SDK at `/usr/local/go/src/zoho/` shadows
the repository source in both GOPATH and module mode, which makes current methods look undefined.
Build against a GOROOT that excludes it.

### Changed - workspace access restrictions move from `OrgAPI` to `WorkspaceAPI` in all seven SDKs

`GET`/`PUT /restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions` is a
workspace-scoped operation, but the `security-controls` path prefix had placed it on the
organization surface. `getWorkspaceAccessRestrictions` and `updateWorkspaceAccessRestrictions` now
live on `WorkspaceAPI` in all seven SDKs (Java, Python, C#, Go, PHP, Node.js, Ruby) and take the
workspace from the instance instead of a `workspaceId` argument. Each `WorkspaceAPI` gained a
`securityControlsEndPoint` field (`/restapi/v2/security-controls/workspaces/<id>`) alongside the
existing `workspaceEndPoint`, mirroring how `BulkAPI` already carries its `/restapi/v2/bulk/...`
prefix. **This is a breaking change for SDK callers.** The SDK snippets in
`v2.0/zenesis-oas-samples/`, the sample programs under `v2.0/sdk/<lang>/sample/` and every
generated page (`v2.0/sdk/<lang>/docs/`, `v2.0/okf/sdk-examples/`) were rebuilt to match. The
REST endpoint, its path and its API group are unchanged.

An audit of the remaining surfaces found no other misplacement: the `/restapi/v2/automl/workspaces/`
and `/restapi/v2/bulk/workspaces/` operations already sit on `WorkspaceAPI` and `BulkAPI`, and
`getWorkspaceDetails`/`getViewDetails` stay on `AnalyticsClient` because they do not require the
organization header.

### Added - four new API groups (28 endpoints) from the API team's `new_md` hand-off

`v2.0/new_md/` was merged into `v2.0/md/` and removed. Four new group documents introduced four new
API groups and 28 endpoints; every generated artefact was rebuilt from them. The inventory moves to
**10 domains, 39 API groups, 138 paths, 208 operations, 210 OKF endpoints and Postman requests**
(from 35 groups, 119 paths, 180 operations, 182 endpoints).

- **`01 · Organization Management/SECURITY_CONTROLS.md`** - new group `Security Controls`
  (tag `Security Controls`, OKF/Postman slug `security-controls`), 4 endpoints: Get/Update Org
  Access Restrictions and Get/Update Workspace Access Restrictions, covering the master switch and
  the `shareViews`, `privateLinks`, `publicViews`, `exportViews` and `emailViews` sections.
- **`03 · Workspace Management/LINKED_WORKSPACES.md`** - new group `Linked Workspaces`, 8 endpoints:
  listing linked workspaces for an organisation and for a master workspace, linkable workspaces,
  linking compatibility, Link, Sync, sync details and Unlink.
- **`03 · Workspace Management/WORKSPACE_BACKUP_AND_RESTORE.md`** - new group
  `Workspace Backup & Restore`, 6 endpoints: list backups, back up now, download a backup
  (`application/x-zip-compressed` stream), restore, and the backup and restore status polls.
- **`09 · Schedules & Alerts/DATA_ALERTS.md`** - new group `Data Alerts`, 10 endpoints: alerts in a
  workspace and in a view, view metadata for an alert, alert configuration, Create, Update, Delete,
  Change Status, Run and alert events.
- New path parameters `backup-id`, `restore-id` and `alert-id`; new OAuth scope entries registered
  in the affected specifications. The Postman environment ships the three new identifier variables
  disabled, as it does for every identifier.
- SDK snippets added for all 28 endpoints in all nine languages.

### Changed - `REPORTS.md` rewritten by the API team

Same three endpoints, same methods, paths and scopes; substantially expanded behavioural
documentation (new concept, limitation, permission-model and enum/availability appendices).

- `CreateReportConfig` drops `settings`, `drillActionConfig` and `modifiedPaths`;
  `UpdateReportConfig` drops `settings`, `folderId` (now rejected with `8145`) and `objId`.
  Nine schemas orphaned by those removals were pruned.
- Error-code catalogues reworked: Create Report 41 -> 56 codes, Update Report 44 -> 54,
  Read Report Metadata 7 -> 8. Update Report's table is written as a delta of Create Report's
  ("every code in that table except 7111, 7137, 7138, 7324, 7362, 8201 and 8504"), so its
  `x-zenesis-statuscodes` is the composed set, not the nine rows printed in the document.

### Fixed - three dashboard listing endpoints kept

`DASHBOARDS.md` as delivered in the hand-off had dropped **Get All Dashboards**
(`GET /restapi/v2/dashboards`), **Get Owned Dashboards** (`GET /restapi/v2/dashboards/owned`) and
**Get Shared Dashboards** (`GET /restapi/v2/dashboards/shared`). The API team confirmed the removal
was unintended, so all three were restored from the reference document and re-appended to
`DASHBOARDS.md` as sections 4-6 with their index rows.

They are present in every knowledge base: the three markdown sections, the three operations and six
schemas in `zenesis-oas/` and `oas/`, SDK snippets in all nine languages, the OKF endpoint and SDK
example documents, the endpoint catalog (markdown and JSON), the permission matrix, the
`dashboard-id` identifier sources, the Postman requests, and their `api-reference-links.json` pages.

### Changed - OKF bundle version 1.6.0 -> 1.7.0

Minor: the release is additive at the endpoint level. No endpoint is removed or renamed.

### Changed - `v2.0/md/` replaced by the API team's revised documents

All 35 group documents were replaced with the revised revision supplied by the API team, and every
generated artefact was rebuilt from them. The endpoint inventory is unchanged: **10 domains,
35 API groups, 119 paths, 180 operations, 182 OKF endpoints and Postman requests.**

- **Editorial pass across every group.** Normalised H1s, linked index tables, `Error-Code` ->
  `Code` error-table headers with the rows sorted by code, `Method` and `ZANALYTICS-ORGID Header`
  rows added to the endpoint attribute tables that lacked them, and new `Response Fields` and
  `Notes & Behaviour` sections on 20 endpoints. `REPORTS.md` appendices renumbered (the common
  headers, scope summary and failure-case appendices now lead as A-C). No error code, CONFIG
  attribute, URL, method, scope or permission changed anywhere.
- **The three Dashboard listing APIs were kept.** The revised `DASHBOARDS.md` again omitted
  `Get All Dashboards` (`GET /restapi/v2/dashboards`), `Get Owned Dashboards`
  (`GET /restapi/v2/dashboards/owned`) and `Get Shared Dashboards`
  (`GET /restapi/v2/dashboards/shared`). All three are still live and publicly documented, so they
  were restored as sections 4-6 - re-styled to match the revised document (prose description, the
  `Method` / `OAuth Scope` / `ZANALYTICS-ORGID Header` / `Permission Required` / `Custom domain`
  attribute table, `Code` error headers) with their samples, responses and error codes unchanged.
  The index table, the `ZANALYTICS-ORGID` row of Appendix A and the Appendix B scope summary
  distinguish the workspace-scoped APIs (1-3) from the user-scoped listings (4-6) again.
- **Cross-file links now name the real files.** The documents link to `COLUMNS.md` and to
  `../04 · Data Modeling & Schema/COLUMNS.md` rather than the legacy `COLUMNS_API_DOC_INFO.md`, so
  `tools/okf/build_okf.py` resolves a link by the markdown stem in the version manifest
  (`MD_STEM_ALIAS`) and accepts a repository-relative path, not only a bare legacy file name.
  This cleared ~100 unresolved and 60+ broken links in the OKF bundle.
- OKF bundle **1.6.0** (minor: documented response fields and behaviour notes added), Postman
  collection regenerated. `v2.0/oas/` is byte-identical to the previous revision.

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
- **One common-file URL.** Every `$ref` to the shared components file, in the Zenesis source as well
  as the published specifications, now uses the published location
  `https://raw.githubusercontent.com/zoho/analytics-oas/refs/heads/main/v2.0/common/zoho-analytics-api-common.json`
  (`common_ref` in `v2.0/manifest.json`; `rules.json` names it on both sides, so the converter's
  `$ref` swap is a no-op). The source validator accepts that URL for `common_ref`.

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
