# Changelog

All notable changes to this bundle are recorded here. Versions follow semantic versioning: major for a
removed or renamed endpoint or a layout change, minor for additions, patch for corrections.

## Unreleased

### Added

- **`v2.0/foundations/report-and-dashboard-enums.md`.** The enumerated CONFIG vocabulary shared by
  the six report and dashboard endpoints, following the pattern of the existing export and import
  enumeration references: the complete 47-value `chartType` list, the axis-type to report-type
  matrix, the operation to column-data-type matrix, `geoRole` and `sort` values, the eight dashboard
  card types, and the layout grid rules (80-unit canvas, `left + width <= 80`, no overlapping cards,
  100-card maximum, integer-only dimensions). Built from an API-team hand-off document for the
  Dashboard and Visual APIs together with the OpenAPI enumerations already shipped in the bundle.
  Linked from all six endpoint documents, both group overviews, the bundle and foundations indexes,
  `v2.0/llms.txt` and the usage guide.
- **39 error codes**, taking the catalog from 278 to 317. They are raised by Create/Read/Update
  Dashboard and Create/Read/Update Visual and were previously undocumented: 7016, 7018, 7309, 7362,
  7479, 7480, 7481, 7482, 7483, 7485, 7486, 7487, 7488, 7491, 7492, 7493, 7507, 7510, 7534, 7701,
  7703, 7727, 8008, 8027, 8051, 8057, 8059, 8144, 8145, 8162, 8166, 8167, 8168, 8170, 8191, 8250,
  8253, 8517, 8534, 8542. Each carries its summary constant, trigger condition, per-operation
  attribution and, where the source supplied one, the server message or the documented solution.
  Added to the catalog, its quick index and the quick reference; counts updated everywhere.

### Changed

- `chartType` in Create Visual named six example values and a 50-character limit. It now points at
  the full 47-value enumeration, which the shipped OpenAPI specification already validated against.
- Create Dashboard now states the layout grid rules, which were previously implicit in the examples.

### Fixed

- **Restored `v2.0/log.md`.** The OKF §9 update-history file was lost between the `v2/` to `v2.0/`
  rename and the move to this repository, so the first commit here shipped without it. Recovered
  from the previous repository's history and brought up to date.

### Changed - corrected against the source of truth

The API team's **Dashboard APIs** and **Visual APIs** documents are the source of truth for this
endpoint family. Five points where the OpenAPI enumerations disagreed with them were resolved in
the documents' favour, in both this bundle and `zoho/analytics-oas`:

| Field | Was | Now |
|---|---|---|
| `axisColumns[].operation` | `average`, `distinctCount`, `stdDev`, `monthYear`, `dateTime` | `avg`, `dc`, `std`, `monthyear`, `datetime` |
| `axisColumns[].operation` | no date sub-types beyond `year`/`quarter`/`month` | adds `quarteryear`, `weekyear`, `week`, `weekday`, `fulldate`, `day`, `hour` |
| `axisColumns[].type` | `sizeaxis` | `sizeAxis` |
| dashboard `displayName` | `maxLength: 100` | `maxLength: 200` |
| report `title`, `axisColumns` | optional | required on create |
| dashboard card `width`, `height` | `minimum: 1` | `minimum: 2` |

The operation rename applies to **all five** schemas that carry an operation enum, not just
`AxisColumn`: `ReportFilter.operation`, `UserFilter.operation`, `WindowFunction.baseFunction` and
`ReportMetadataAxisColumn.operation` were corrected alongside it, together with their
`x-enumDescriptions` maps and every inline example.

`ReportMetadataAxisColumn.type` additionally moved from an all-lowercase "canonical" form
(`xaxis`, `yaxis`, `coloraxis`, `sizeaxis`, `textaxis`, `groupby`) to the camel-case form, because
the source document's own Read Visual Metadata sample response returns `"type": "xAxis"`.

Also added to the specification: `DashboardLayout.maxProperties: 100`, the documented card ceiling.

`MovingCalculation.calculation` still uses `average`. It is a window-function field that the source
documents do not cover, so it was left alone.

> **This is a breaking change for anything generated from the previous OpenAPI enumerations.** An
> SDK or validator built before this emits `average`, `distinctCount`, `stdDev`, `monthYear`,
> `dateTime` or `sizeaxis`, none of which are accepted vocabulary any more. Regenerate.

`tooltip` and `custom` (axis types) and `PARA` and `DELETED` (card types) are carried by the
specification but not described in the source documents. They were **kept**: the documents
enumerate what a caller may send rather than asserting nothing else is accepted, so removing them
could reject a request the service still honours. They are flagged as unverified in the reference.

## Previously unreleased

### Added

- **`v2.0/foundations/custom-roles.md`.** Organization-defined custom roles: the three access
  permission levels, the full permission catalogue by category (Create, Data, Design, Interaction,
  Share and Collaborate, Publish, Data Source), a mapping from those labels onto the permission
  vocabulary the endpoint documents use, the comparison against the predefined roles, and the rules
  for assigning a custom role through the workspace-user endpoints. It records that the REST API can
  **assign** a custom role but cannot create, list, modify or delete one, and that role names cannot
  be enumerated from the API. Derived from the Zoho Analytics help documentation rather than the API
  reference; the document states this in its body and lists both help pages in `sources`.
  Cross-linked from the bundle index, the foundations index, `v2.0/llms.txt`, the roles, permission
  matrix, how-to-use, Workspace Users and user-management-workflow documents.

### Fixed

- **Ten endpoints had an empty `api.permission_required`**, so their rows in
  `v2.0/foundations/permission-matrix.md` rendered as `-` — which reads as "this call needs no
  permission". Affected: Export Data from a View; the four asynchronous export operations; and all
  five Data Sync & Connectivity operations. Each value was taken from its own group's
  **Permission Model** table, which had the answer all along, and the placeholder
  `| Permission required | See group overview |` row in each document body was filled in too.
- `tools/validate.py` now rejects an `API Endpoint` with an empty `api.permission_required`, an
  unresolved "See group overview" placeholder in a document body, and an empty permission cell in
  the permission matrix, so the gap cannot reappear silently.

- **`generated.by` is now present on every concept.** OKF v0.2 §5.2 marks `by` as required inside
  `generated`, and §5.3 derives the trust tier from the actor prefix, but the bundle emitted
  `generated.at` alone and `tools/validate.py` actively rejected `generated.by` as if it were
  forbidden. The check was inverted: it now requires `generated.by` and validates that it, and every
  other actor, matches an OKF §7 form (`<producer>/<version>`, `human:<id>` or `process:<id>`). All
  407 concepts and `v2.0/manifest.json` now carry `generated.by: process:build_okf`. The generator in
  the maintainer repository must be updated to emit it.
- Dead links in `README.md`: the clone URL pointed at `github.com/zoho/analytics-okf` and the
  canonical-copy footer at `zoho.com/analytics/api/v2/okf`, both of which 404.
- `v2.0/how-to-use-this-bundle.md` referred to `tools/validate_okf.py`; the validator is
  `tools/validate.py`.

### Changed

- **Root `manifest.json` states the version contract explicitly** (`schema_version` 1.1). Added
  `latest_path` so a consumer can resolve the current bundle without joining strings, a `resolution`
  note, a `status_vocabulary` defining `beta`/`stable`/`deprecated`/`sunset`, per-version
  `deprecated_on`, `sunset_on` and `superseded_by` fields, an `okf_spec` link and a per-version
  `api_reference` link. No existing key changed meaning.
- CI additionally checks that `latest_path` agrees with `latest`, that every `status` is in the
  vocabulary, that `latest` is neither deprecated nor sunset, and that a deprecated or sunset version
  carries `deprecated_on` and a `superseded_by` that names a listed version.
- `README.md` is no longer written as if the repository held only v2. It leads with the two
  unversioned entry points, marks the `v2.0/` URLs as the pin-deliberately case, documents the
  lifecycle vocabulary and the deprecation path, and records OKF conformance clause by clause
  including the one deliberate deviation from §6.1 (document-relative body links).
- `llms.txt` states the "use `latest` unless pinned" rule in its body rather than in the `## Optional`
  section, whose defined meaning is "links an agent may skip when short on context". `## Optional`
  now holds the changelog, log and licence, which are genuinely skippable.

- **Repository layout.** The bundle moved from `okf/` to `v2/`, and then from `v2/` to `v2.0/`, so
  future API versions can live alongside it in the same repository. Bundle content is unaffected by
  either move: no document, link or frontmatter path changed, because links inside a bundle are
  document-relative and never name the bundle directory. The directory name is the value of
  `latest`, `latest_path` and `versions[].version`; the **API version stays `v2`** (`api_version`,
  and the `/restapi/v2` path prefix).
- `llms.txt` at the repository root is now a version router. The full link list for the current
  version moved to `v2.0/llms.txt`.
- `tools/validate.py` discovers `v<N>/` bundle directories instead of a hardcoded `okf/`, and CI
  validates every `v*/` directory, so adding `v3/` needs no further change.

### Added

- Root `manifest.json`: a machine-readable index of every available API version, its status and its
  bundle manifest. Tools should read this instead of hard-coding `v2.0/`.
- A CI check that the root `manifest.json` stays in sync with the version directories on disk.

### Migration

- Replace `.../main/okf/<path>` **or** `.../main/v2/<path>` with `.../main/v2.0/<path>` in any pinned
  raw URL. The bundle content at the new path is byte-identical, so nothing but the prefix changes.
- **The `v2/` → `v2.0/` rename is a breaking change for anyone who pinned `v2/` while it was
  published on `main`.** It is the one exception to the guarantee that a published version directory
  never moves; from `v2.0/` onward that guarantee holds. Consumers that read `latest` from the root
  `manifest.json` rather than hard-coding a directory are unaffected.
- `tools/validate.py` and the CI workflow needed no change: both discover bundles by globbing
  `v[0-9]*`, which matches `v2.0` as well as `v2`.

## 1.0.0 - 2026-09-16

### Added

- First public release of the Zoho Analytics REST API v2 Open Knowledge Format bundle (OKF v0.2).
- 168 endpoint concepts across 10 domains and 33 API groups.
- Foundations covering authentication, data centers, request conventions, response envelope, HTTP statuses,
  OAuth scopes, roles and permissions, the permission matrix, identifiers, filter criteria syntax,
  asynchronous jobs, rate limits and quotas, export and import enumerations, White Label behaviour,
  the glossary and SDK clients.
- Error catalog with 278 codes plus a compact quick reference.
- 8 workflow playbooks for multi-endpoint tasks.
- 166 SDK example documents covering 9 languages.
- Machine-readable `manifest.json` and `references/endpoint-catalog.json`, and the OpenAPI 3 specifications.

### Known limitations

- Trust tier is `unverified`: no concept carries a `verified` entry yet.
- Two endpoints, Fetch All Embed URLs and Delete Embed URL, are documented from the API reference only.
  They are absent from the OpenAPI specifications and their documents say so.
