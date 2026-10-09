# tools

Everything that builds, converts or validates the API documents, organised by the artefact it
produces. All tools are standard-library Python 3.8+ (the converter also uses `make`). Every tool
takes the API version as a parameter and reads and writes inside `<repo>/<VERSION>/` only; the
default version is `latest` in `<repo>/manifest.json`.

| Tool | Reads | Writes | Run |
|---|---|---|---|
| [`validate_api_docs.py`](validate_api_docs.py) | `manifest.json`, every `vN.N/manifest.json`, `vN.N/md/`, `vN.N/zenesis-oas/` (+ `common/`), `vN.N/zenesis-oas-samples/` | nothing | `python3 tools/validate_api_docs.py --strict [--version v2.0]` |
| [`zenesis-oas/`](zenesis-oas/README.md) | `vN.N/zenesis-oas/` (and `vN.N/oas/` for `compare` / `to-zenesis`) | `vN.N/oas/` domain files; `dist/oas/vN.N/common/` for review; `overlays/vN.N/` | `make -C tools/zenesis-oas check to-analytics compare VERSION=v2.0` |
| [`okf/`](okf/README.md) | `vN.N/md/`, `vN.N/zenesis-oas/`, `vN.N/zenesis-oas-samples/`, `vN.N/manifest.json`, `tools/okf/handwritten/vN.N/` | `vN.N/okf/` (deleted and rebuilt); `dist/analytics-okf/` when packaging | `python3 tools/okf/build_okf.py --version v2.0 && python3 tools/okf/validate_okf.py v2.0/okf` |
| [`postman/`](postman/README.md) | `vN.N/okf/references/endpoint-catalog.json`, `vN.N/okf/**`, `vN.N/oas/`, `vN.N/md/`, `vN.N/manifest.json`, `tools/postman/templates/`, `api-reference-links.json` | `vN.N/postman/` (collection + environment) | `python3 tools/postman/build_postman.py --version v2.0` |
| [`api-agent/`](api-agent/README.md) | input markdown from anywhere, then everything above | nothing itself; drives the tools above | `python3 tools/api-agent/plan.py in.md` → edit → `python3 tools/api-agent/pipeline.py` |

## Order of operations

The artefacts depend on each other, so this is the order (what `tools/api-agent/pipeline.py` runs):

```
vN.N/md + zenesis-oas + zenesis-oas-samples      the authored sources
        │  validate_api_docs.py --strict          naming, completeness, join keys, $ref targets
        ▼
vN.N/oas                                         make -C tools/zenesis-oas check to-analytics compare
        │
        ▼
vN.N/okf                                         build_okf.py, validate_okf.py        (reads the sources, copies zenesis-oas into okf/references)
        │
        ▼
vN.N/postman                                     build_postman.py                     (reads okf's endpoint catalog + oas examples)
```

## Adding an API version

Create `vN.N/` with `manifest.json`, `README.md`, `md/`, `zenesis-oas/` (with `common/`) and
`zenesis-oas-samples/`; add the version to the root `manifest.json`; copy
`tools/okf/handwritten/<previous>/` to `tools/okf/handwritten/vN.N/` and revise it; then run the
pipeline with `--version vN.N`. The converter's `rules.json` names the `v2.0` common-file URLs in
`common_ref`; give the new version its own copy of the rules (`--rules`) or extend the Makefile.
Add the version to the matrices in `.github/workflows/validate.yml`.
