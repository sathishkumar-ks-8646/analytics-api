# Zoho Analytics REST API - documents, specifications and developer tools

Everything about the [Zoho Analytics REST API](https://www.zoho.com/analytics/api/v2/) in one
repository, **one directory per API version**: the authored reference documents, the OpenAPI
specifications in both of their shapes, the Open Knowledge Format bundle for AI agents, the Postman
collection, and the tools that build, convert and validate all of it - including an AI-agent workflow
that takes any markdown description of an API change and carries it through every artefact.

| Version | API | Status | Sources | Built artefacts |
|---|---|---|---|---|
| [`v2.0/`](v2.0/README.md) | v2 | current | 10 domains, 35 API groups, 119 paths, 180 operations | [OpenAPI](v2.0/oas) · [OKF bundle](v2.0/okf/index.md) (182 endpoints, 306 error codes) · [Postman](v2.0/postman) |

[`manifest.json`](manifest.json) is the machine-readable form of that table: every version directory,
which is `latest`, and where each version's sources and artefacts are. Tooling starts there rather
than hard-coding a directory, so a future `v3.0/` is an addition, not a change.

## Layout

```
analytics-api/
├── manifest.json                  version index: every vN.N/, which is latest, where its artefacts are
├── README.md · CHANGELOG.md · LICENSE.md
├── CLAUDE.md · AGENTS.md          AI coding agents start here -> tools/api-agent/AGENT.md
├── Makefile                       shortcuts for the commands below
├── .github/workflows/validate.yml CI: sources, OpenAPI round trip, OKF conformance, Postman freshness
│
├── v2.0/                          ← one directory like this per API version
│   ├── manifest.json              inventory: domains, groups, (markdown, OpenAPI tag) pairs, OKF/Postman names, common_ref
│   ├── README.md                  the version's overview
│   ├── md/                        SOURCE   narrative reference: one folder per domain, one Markdown file per API group
│   ├── zenesis-oas/               SOURCE   OpenAPI 3.1 + x-zenesis-* extensions, one file per domain
│   │   └── common/zoho-analytics-api-common.json      OAuth scheme and scopes, shared error responses
│   ├── zenesis-oas-samples/       SOURCE   SDK snippets per path + method in 9 languages
│   ├── oas/                       BUILT    vendor-neutral OpenAPI 3.1; copied as is to zoho/analytics-oas; oas/common/ is placed by hand
│   ├── okf/                       BUILT    Open Knowledge Format v0.2 bundle; copied as is to zoho/analytics-okf
│   └── postman/                   BUILT    Postman collection + environment
│
└── tools/
    ├── validate_api_docs.py       naming, completeness and integrity of the SOURCES of every version
    ├── zenesis-oas/               zenesis-oas <-> oas converter (Makefile, rules.json, overlays/vN.N/, tests)
    ├── okf/                       OKF builder and validator; handwritten/vN.N/ concepts; the maintainer agent-guide
    ├── postman/                   Postman generator (+ curated API-reference links and templates)
    └── api-agent/                 AI-agent workflow: plan.py, scaffold.py, pipeline.py, AGENT.md
```

**Sources are authored; everything else is built from them.** An API fact is corrected in `md/`,
`zenesis-oas/` and `zenesis-oas-samples/` of its version, and flows outward:

```
vN.N/md + zenesis-oas + zenesis-oas-samples          tools/validate_api_docs.py --strict
        │
        ├──► tools/zenesis-oas  (make to-analytics)  ──►  vN.N/oas/        ──►  zoho/analytics-oas, Swagger UI, SDK generators, MCP
        │        ▲   └── make to-zenesis carries a fix made in oas/ back into zenesis-oas/
        ├──► tools/okf/build_okf.py                  ──►  vN.N/okf/        ──►  zoho/analytics-okf, AI agents (llms.txt)
        │                                                     │
        └──► tools/postman/build_postman.py  ◄────────────────┘  (endpoint catalog + oas examples)  ──►  vN.N/postman/
```

## Quick start

Python 3.8+ and `make`; standard library only, nothing to install.

```bash
git clone https://github.com/sathishkumar-ks-8646/analytics-api.git
cd analytics-api

make check                      # validate everything for the latest version without writing (CI's view)
make build                      # rebuild oas/, okf/ and postman/ of the latest version from the sources
make build VERSION=v2.0         # one version explicitly

# the same, stage by stage
python3 tools/validate_api_docs.py --strict                       # sources
make -C tools/zenesis-oas check to-analytics compare VERSION=v2.0 # zenesis-oas -> oas, and prove they agree
python3 tools/okf/build_okf.py --version v2.0                     # okf
python3 tools/okf/validate_okf.py v2.0/okf
python3 tools/postman/build_postman.py --version v2.0             # postman
```

Reading an endpoint: open the version directory, find the group in `md/` for the behaviour and the
CONFIG attributes, then the matching operation in `zenesis-oas/` for the exact schema. The two are
joined by title (`## N. Title` in the markdown equals `x-zenesis-title` in the operation).

Consuming the API: point Swagger UI, Redoc, `openapi-generator` or an MCP server at `v2.0/oas/`;
point an AI assistant at `v2.0/okf/llms.txt`; import the two files in `v2.0/postman/` into Postman.

## Changing the API documentation

Two ways, same result.

**With an AI agent.** Give the agent the markdown that describes the change - any layout, one file
or many - and point it at [`tools/api-agent/AGENT.md`](tools/api-agent/AGENT.md). It plans
(`plan.py`: what is new, what exists and differs, which files to touch), edits the three source
files per endpoint (`scaffold.py` prints the skeletons for a new one), then runs `pipeline.py`
until every stage is green. `CLAUDE.md` and `AGENTS.md` route an agent opening this repository
there automatically.

**By hand.** Edit the group document in `md/`, the operation in `zenesis-oas/` and the snippets in
`zenesis-oas-samples/` of the version - all three, in one commit - then:

```bash
python3 tools/api-agent/pipeline.py --version v2.0    # sources -> oas -> okf -> postman, stops at the first failure
git diff --stat                                        # your edits plus the regenerated artefacts
```

Procedures for each kind of change (new endpoint, attribute, error code, group, deprecation, shared
rule) are in [`tools/okf/agent-guide/04-change-playbooks.md`](tools/okf/agent-guide/04-change-playbooks.md);
the exact markdown and OpenAPI shapes the parsers expect are in
[`03-source-document-format.md`](tools/okf/agent-guide/03-source-document-format.md).

## Conventions that hold everywhere

- **Version directories** are `vN.N`, listed in `manifest.json`; exactly one is `current`. Nothing
  under a version moves when another is added.
- **Domain folders** are `NN · Title` (middle dot U+00B7); **group files** are `UPPER_SNAKE_CASE.md`,
  one per OpenAPI tag; **specification files** are `<domain-slug>-grouped-api.json` and samples
  `<domain-slug>-grouped-api-samples.json`. The slug is a contract with every consumer - never rename.
- **Titles are the join key** between markdown and OpenAPI. Rename both or neither.
- **Vendor extensions** are the ten `x-zenesis-*` keys in `tools/zenesis-oas/rules.json`; an unknown
  key fails validation before it can be dropped silently downstream.
- **Error responses** are `4XX` and `500`, each a `$ref` to the shared responses in the version's
  common file; never `default`.
- **The two common files.** `zenesis-oas/common/` is referenced by the URL in the version manifest's
  `common_ref` (this repository). `oas/common/` is referenced by
  `https://raw.githubusercontent.com/zoho/analytics-oas/refs/heads/main/v2.0/common/zoho-analytics-api-common.json`
  and is **placed by hand**, never regenerated; the converter writes the ten domain files only and
  `make -C tools/zenesis-oas common-diff` shows what the hand-placed copy would need (nothing is written).
- **Generated directories are never edited by hand**: `oas/` (except `oas/common/`), `okf/`, `postman/`.

## Publishing

| What | Where it goes | How |
|---|---|---|
| `vN.N/oas/` | [zoho/analytics-oas](https://github.com/zoho/analytics-oas) `vN.N/` | copy as is after `make -C tools/zenesis-oas compare` reports no differences |
| `vN.N/okf/` | [zoho/analytics-okf](https://github.com/zoho/analytics-okf) `vN.N/` | copy as is; `okf/llms.txt` links are already built against that repository's raw URL (`publish.okf.raw_base` in `manifest.json`). Root files of that repository (`llms.txt`, `manifest.json` version index, README, CHANGELOG) are maintained there |
| `vN.N/postman/` | Postman workspace | import the collection and the environment |
| `vN.N/md`, `zenesis-oas`, `zenesis-oas-samples` | the documentation site (Zenesis renderer) | read directly from this repository |

## Versioning

API versions are directories. The documentation itself is versioned in [`CHANGELOG.md`](CHANGELOG.md)
with semantic versioning: major for a removed or renamed endpoint or a layout change, minor for
additions (including a new API version directory), patch for corrections. The OKF bundle carries its
own content version in `vN.N/okf/manifest.json`, bumped deliberately with `OKF_BUNDLE_VERSION` at
build time.

## Licence

See [LICENSE.md](LICENSE.md).
