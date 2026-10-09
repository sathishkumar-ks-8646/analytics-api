# v2.0 - Zoho Analytics REST API v2

Everything for the [Zoho Analytics REST API v2](https://www.zoho.com/analytics/api/v2/): the authored
source documents and the artefacts built from them. This is the `current` version in
[`../manifest.json`](../manifest.json).

**10 domains, 35 API groups, 119 paths, 180 operations** (182 endpoints in the OKF bundle and the
Postman collection: two Embed URL endpoints are documented from the API reference only).

## Layout

```
v2.0/
├── manifest.json            the inventory below, machine-readable: domains, groups, (md, tag) pairs,
│                            okf and postman names, common_ref
├── md/                      SOURCE  narrative reference               -> md/README.md
├── zenesis-oas/             SOURCE  OpenAPI 3.1 + x-zenesis-*         -> zenesis-oas/README.md
│   └── common/zoho-analytics-api-common.json    shared by all ten specifications
├── zenesis-oas-samples/     SOURCE  SDK snippets, 9 languages         -> zenesis-oas-samples/README.md
├── oas/                     BUILT   vendor-neutral OpenAPI 3.1, one file per domain, + common/ (hand-placed)
├── okf/                     BUILT   Open Knowledge Format v0.2 bundle -> okf/index.md, okf/llms.txt
└── postman/                 BUILT   Zoho Analytics REST APIs.postman_collection.json + the environment
```

| Directory | Built by | Consumed by |
|---|---|---|
| `oas/` | `make -C tools/zenesis-oas to-analytics VERSION=v2.0` | [zoho/analytics-oas](https://github.com/zoho/analytics-oas) `v2.0/`, Swagger UI, Redoc, SDK generators, MCP servers |
| `okf/` | `python3 tools/okf/build_okf.py --version v2.0` | [zoho/analytics-okf](https://github.com/zoho/analytics-okf) `v2.0/`, AI assistants via `okf/llms.txt` |
| `postman/` | `python3 tools/postman/build_postman.py --version v2.0` | Postman |

## Domains

| # | Domain folder (`md/`) | Groups | Specification (`zenesis-oas/`, `oas/`) | Samples (`zenesis-oas-samples/`) | OKF domain (`okf/domains/`) |
|---|---|---|---|---|---|
| 01 | `01 · Organization Management` | 1 | `org-management-grouped-api.json` | `org-management-grouped-api-samples.json` | `organization-management` |
| 02 | `02 · User & Groups` | 4 | `user-groups-grouped-api.json` | `user-groups-grouped-api-samples.json` | `users-and-groups` |
| 03 | `03 · Workspace Management` | 4 | `workspace-management-grouped-api.json` | `workspace-management-grouped-api-samples.json` | `workspace-management` |
| 04 | `04 · Data Modeling & Schema` | 7 | `data-modeling-schema-grouped-api.json` | `data-modeling-schema-grouped-api-samples.json` | `data-modeling-and-schema` |
| 05 | `05 · Data Operations` | 6 | `data-operations-grouped-api.json` | `data-operations-grouped-api-samples.json` | `data-operations` |
| 06 | `06 · Views Management` | 5 | `views-management-grouped-api.json` | `views-management-grouped-api-samples.json` | `views-management` |
| 07 | `07 · Reports & Dashboards` | 2 | `reports-dashboards-grouped-api.json` | `reports-dashboards-grouped-api-samples.json` | `reports-and-dashboards` |
| 08 | `08 · Share & Publish` | 4 | `share-publish-grouped-api.json` | `share-publish-grouped-api-samples.json` | `share-and-publish` |
| 09 | `09 · Schedules & Alerts` | 1 | `schedules-alerts-grouped-api.json` | `schedules-alerts-grouped-api-samples.json` | `schedules-and-alerts` |
| 10 | `10 · DSML` | 1 | `dsml-grouped-api.json` | `dsml-grouped-api-samples.json` | `dsml` |

The `(markdown file, OpenAPI tag)` pairs inside each domain, and the slugs and titles the OKF bundle
and the Postman collection use for them, are in [`manifest.json`](manifest.json); the validator, the
OKF builder and the Postman generator all read them from there. A new group or domain starts there.

## The two common files

[`zenesis-oas/common/zoho-analytics-api-common.json`](zenesis-oas/common/zoho-analytics-api-common.json)
holds what every specification of this version shares and lives beside them:

| Component | Pointer | Purpose |
|---|---|---|
| OAuth 2.0 security scheme | `#/components/securitySchemes/iam-oauth2-schema` | Authorization-code flow and the full scope list |
| Error schema | `#/components/schemas/Error` | Shape of every failure response |
| Client error response | `#/components/responses/CommonErrorResponse` | Referenced by every operation as `4XX` |
| Server error response | `#/components/responses/UnexpectedErrorResponse` | Referenced by every operation as `500` |

Every specification - the Zenesis source in `zenesis-oas/` and the published copy in `oas/` - references
the shared components file by the same absolute URL, its published location (`manifest.json` → `common_ref`):

```
https://raw.githubusercontent.com/zoho/analytics-oas/refs/heads/main/v2.0/common/zoho-analytics-api-common.json
```

`zenesis-oas/common/` is the authored copy of that file; `oas/common/` is the published copy, **placed
by hand** (`make -C tools/zenesis-oas common-diff` shows what the converted Zenesis common file would
change in it). The converter writes only the ten domain files. The validator rejects any remote `$ref`
in `zenesis-oas/` that points elsewhere.

## Making a change

Edit the group document in `md/`, the operation in `zenesis-oas/` and the snippets in
`zenesis-oas-samples/` together, then rebuild and validate everything:

```bash
python3 tools/api-agent/pipeline.py --version v2.0
```

With an AI agent and an input document: [`../tools/api-agent/AGENT.md`](../tools/api-agent/AGENT.md).
