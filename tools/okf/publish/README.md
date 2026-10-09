# Zoho Analytics REST API - Open Knowledge Format bundles

Machine-readable, agent-friendly knowledge base for the [Zoho Analytics REST API](https://www.zoho.com/analytics/api/v2/).
It packages every public endpoint, the conventions they share, and their error codes, OAuth scopes
and permissions as an [Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format)
([OKF v0.2 specification](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md))
bundle: a directory of markdown files with YAML frontmatter.

Each API version is a self-contained bundle in its own top-level directory. **The current version is
[{{latest}}]({{latest}}/index.md)**, bundle version {{bundle_version}} - {{counts.endpoints}} endpoints, {{counts.domains}} domains, {{counts.groups}} groups, {{counts.error_codes}} error codes,
{{counts.oauth_scopes}} OAuth scopes, {{counts.workflow_playbooks}} workflow playbooks, {{counts.sdk_example_documents}} SDK example documents in 9 languages.

This is documentation, not a client library. For the SDKs themselves see the
[Zoho Analytics API documentation](https://www.zoho.com/analytics/api/v2/).

## Quick start

Two files at the repository root are the stable entry points. Their paths never change and their
contents always describe whatever versions exist, so link to these rather than to a version
directory.

```
https://raw.githubusercontent.com/zoho/analytics-okf/main/llms.txt          agent entry point; names the latest version
https://raw.githubusercontent.com/zoho/analytics-okf/main/manifest.json     version index for tooling; `latest` names the version to use
```

**For an AI assistant or agent.** Point it at [`llms.txt`](https://raw.githubusercontent.com/zoho/analytics-okf/main/llms.txt)
and let it follow the links. Inside a bundle, links between documents are relative to the linking
document, so they resolve both on GitHub and in a local clone.

**For tooling** such as SDK generators, Postman collections and MCP servers. Read the root
`manifest.json`, take `latest` (or the version the caller pinned), and follow that entry's
`path`, `manifest` and `endpoint_catalog_json`. Everything below is then reachable from the bundle
manifest's `entry_points`.

**For a human.** Start at [`v2.0/overview.md`](v2.0/overview.md), then
[`v2.0/endpoint-catalog.md`](v2.0/endpoint-catalog.md) to find an endpoint, then the endpoint document.

```bash
git clone https://github.com/zoho/analytics-okf.git
```

Resolved against the current `latest`, the per-version files are:

```
.../main/v2.0/manifest.json                         version, counts, entry points
.../main/v2.0/llms.txt                              curated entry point for this version
.../main/v2.0/overview.md                           what the API is, five shared conventions
.../main/v2.0/how-to-use-this-bundle.md             frontmatter contract and navigation rules
.../main/v2.0/references/endpoint-catalog.json      every endpoint, machine-readable
.../main/v2.0/references/openapi/                   request and response schemas
```

Hard-code these only when you deliberately want to pin to v2.0. See [Versions](#versions).

## Repository layout

Each Zoho Analytics REST API version is a self-contained OKF bundle in its own top-level
directory. The two root files route agents and tooling to the right one.

| Path | Contents |
|---|---|
| `llms.txt` | AI agent entry point. Names the latest version and links to every available one. |
| `manifest.json` | Machine-readable version index. Read this rather than hard-coding a version directory. |
| `v2.0/` | The Zoho Analytics REST API **v2** bundle: current and stable. |
| `tools/` | Maintainer tooling. Shared across versions. |
| `CHANGELOG.md` | Bundle version history across all API versions. |
| `LICENSE.md` | Licence. |
| `.github/` | CI that validates every `v<N>/` bundle and the root manifest. |

### Inside a version bundle (`v2.0/`)

| Path | Contents |
|---|---|
| `v2.0/index.md` | Bundle root. Declares `okf_version`. Lists everything below. |
| `v2.0/overview.md` | What the API is, the object model, the five conventions every call shares. |
| `v2.0/how-to-use-this-bundle.md` | Directory layout, the `api:` frontmatter contract, navigation rules for agents. |
| `v2.0/endpoint-catalog.md` | All {{counts.endpoints}} endpoints in one table. |
| `v2.0/foundations/` | Rules shared by every call: authentication, data centers, request conventions and CONFIG encoding, response envelope, HTTP statuses, error catalog, OAuth scopes, roles and permissions, permission matrix, identifiers, filter criteria syntax, asynchronous jobs, rate limits, export and import enumerations, White Label, glossary, SDK clients. |
| `v2.0/domains/` | One document per domain, per API group and per endpoint. |
| `v2.0/workflows/` | Step-by-step playbooks for multi-endpoint tasks. |
| `v2.0/sdk-examples/` | Code samples per endpoint in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby and Deluge. |
| `v2.0/references/` | The OpenAPI 3 specifications and the machine-readable endpoint catalog. |
| `v2.0/log.md` | OKF update log for this bundle. |
| `v2.0/manifest.json` | Bundle name, version, OKF version, counts and entry points. |
| `v2.0/llms.txt` | Curated entry point for this version, with the full link list. |

## How the documents are structured

Every endpoint document carries an `api:` block in its frontmatter so tools never have to parse prose:

```yaml
type: API Endpoint
title: Share Views
api:
  operation_id: shareViews
  method: POST
  path: /restapi/v2/workspaces/{workspace-id}/share
  oauth_scopes: [ZohoAnalytics.share.create]
  org_id_header: required
  config_parameter: { location: form, required: true }
  success_status: 204
  error_codes: [7301, 7307, 7320]
  openapi: { file: /references/openapi/share-publish-grouped-api.json, pointer: "#/paths/..." }
```

The body always uses the same H1 sections in the same order: Summary, Endpoint, Request, Response,
Examples, Notes and Behaviour, Error Codes, Related. Full contract in
[`v2.0/how-to-use-this-bundle.md`](v2.0/how-to-use-this-bundle.md).

## OKF conformance

The bundle satisfies every clause of [OKF v0.2 §11](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md):
every non-reserved `.md` file has parseable YAML frontmatter with a non-empty `type` (§4.1), and the
reserved files follow §8 and §9 - `index.md` carries no frontmatter except the bundle root, which
declares `okf_version: "0.2"` (§12), and `log.md` is a newest-first list under ISO 8601 date
headings. Concepts use the recommended `title`, `description`, `resource` and `tags` fields, the
provenance and lifecycle families `sources`, `generated` and `status` (§5), the §7 actor convention,
and the `references/` convention (§6.3).

One deliberate deviation. §6.1 recommends bundle-absolute links beginning with `/`, but a leading
slash resolves against the *site* root in every markdown renderer, so those links 404 as soon as the
bundle sits in a subdirectory of a repository, which is exactly the layout here. Links in document
bodies are therefore document-relative, and bundle-absolute paths appear only in the path-valued
frontmatter fields `resource`, `sources[].resource` and `api.openapi.file`, where §6.2 defines them
against the bundle root. `tools/validate.py` enforces this split.

## Versions

Each API version ships as a self-contained OKF bundle in its own top-level directory.
Adding a version never moves an existing one, so a URL you have already resolved stays valid.

| Version | Status | Path | Manifest |
|---|---|---|---|
| v2.0 | stable, latest | [`v2.0/`](v2.0/index.md) | [`v2.0/manifest.json`](v2.0/manifest.json) |

### Resolving the version to use

Read the root [`manifest.json`](manifest.json) and follow `latest` to the matching `versions[]`
entry, or join `raw_base` with `latest_path`. Do not assume `v2.0/`. `latest` is the one thing in this
repository whose value is meant to change; everything it points at is immutable.

Pin a version deliberately - by writing `v2.0/` into a URL, or by cloning a tag - when you need
reproducibility, for instance in a generator's golden files or a cached agent context. Pinning is
the supported case, not a workaround; it is only hard-coding `v2.0/` *while meaning "current"* that
breaks when v3 ships.

### Lifecycle

`versions[].status` takes one of four values, defined in the manifest's `status_vocabulary`:

| Status | Meaning |
|---|---|
| `beta` | Published for early access. Content may change without a major bundle version bump. |
| `stable` | Ready for production use and actively maintained. |
| `deprecated` | Still served and still correct, but superseded. Migrate before `sunset_on`. |
| `sunset` | No longer maintained. Retained for link stability and history only. |

When a new API version ships it is added as a sibling directory and a new `versions[]` entry, and
`latest` and `latest_path` move to it. The superseded version stays exactly where it is and gains
`status: deprecated`, a `deprecated_on` date, a `sunset_on` date and a `superseded_by` pointer, so a
consumer can detect the change and plan a migration from the manifest alone. A deprecated bundle is
never deleted and never moved; `sunset` means maintenance has stopped, not that the files went away.

### Version numbers

Two version numbers are in play and they move independently.

- The **API version** is `v2` - the `/restapi/v2` prefix every path carries, and the value of
  `api_version` in the root manifest. It changes only when Zoho ships a new REST API version.
- The **bundle directory** is `v2.0/`, and it is what `latest`, `latest_path` and `versions[].version`
  name. It is not the same string as the API version: the directory carries a revision suffix so a
  future re-cut of the same API version can land beside it rather than overwrite it.
- The **bundle version** is semantic versioning applied to the documentation itself, recorded in
  `v<N>/manifest.json`. Each version directory carries its own.

Bundle version bumps within a single API version:

| Change | Bump |
|---|---|
| An endpoint is removed or renamed, or the layout inside the bundle changes | major |
| Endpoints, scopes or documents are added | minor |
| Content corrections and clarifications | patch |

Pin a version by cloning a tag or downloading the release tarball. `main` always holds the newest bundle.

The bundle has moved twice, both times as repository-layout changes rather than content changes: from
`okf/` to `v2/`, and then from `v2/` to `v2.0/`. No document, link or frontmatter path was altered by
either move, because links inside a bundle are document-relative and never name the bundle directory.

Raw URLs pinned to `okf/` or to `v2/` must be rewritten to `v2.0/`. **This is a breaking change for
anyone who pinned `v2/` while it was published**, and it is the one exception to the rule stated at the
top of this section - that adding a version never moves an existing one. From `v2.0/` onward that
rule holds.

## Provenance and trust

Concepts are derived from the Zoho Analytics API reference documents and the OpenAPI specifications
shipped in `v2.0/references/openapi/`. Each concept records `generated.by` and `generated.at` and,
where applicable, `sources`. `generated.by` is `process:build_okf`, the OKF §7 actor for the
generator that produced the bundle. No concept carries a `verified` entry yet, so the bundle's OKF
trust tier is **unverified** (§5.3): content is faithful to the source documents but has not been
re-confirmed against the live service. Reviewers should add
`verified: { by: human:<id>, at: <timestamp> }` to the concepts they check, which raises those
concepts to **human-reviewed**.

## Feedback and contributions

Open an issue for anything wrong, missing or ambiguous. Include the bundle version from
`v2.0/manifest.json` and the path of the document.

If you send a pull request, run the validator first. It is the same check that CI runs, and it is the
only thing in this repository aimed at maintainers rather than consumers. You do not need it to *use*
the bundle.

```bash
python3 tools/validate.py        # finds the newest v<N>/ automatically; needs Python 3.8+, no dependencies
python3 tools/validate.py v2.0   # or name a bundle directory explicitly
```

It verifies OKF v0.2 conformance including the `generated`/`verified` actor forms, that no `resource`
points outside the bundle, and that every internal link and anchor resolves. It exits non-zero on any
error. CI runs it over every `v<N>/` directory and additionally checks that the root `manifest.json`
agrees with what is on disk, that `latest` and `latest_path` name a version that is neither
deprecated nor sunset, and that any deprecated version carries its lifecycle dates.

## Licence

See [LICENSE.md](LICENSE.md).

---

Canonical copy: [https://github.com/zoho/analytics-okf](https://github.com/zoho/analytics-okf).
