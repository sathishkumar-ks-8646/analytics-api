# okf - Open Knowledge Format bundle tooling

Generates and validates the OKF v0.2 bundle of one API version from that version's source
documents. The bundle lives at `<repo>/<VERSION>/okf/` and is committed; it is deleted and rebuilt on
every run, so every rebuild appears as a reviewable diff.

| Script | Reads | Writes | Purpose |
|---|---|---|---|
| `build_okf.py [--version vN.N]` | `<VERSION>/md/`, `<VERSION>/zenesis-oas/` (+ `common/`), `<VERSION>/zenesis-oas-samples/`, `<VERSION>/manifest.json`, `handwritten/<VERSION>/` | `<VERSION>/okf/` (deleted and recreated) | Generates the bundle. Prints `endpoints=… groups=… errors=… sdk=…` on success and `WARN` lines when markdown and OpenAPI disagree. `OKF_BUNDLE_VERSION=x.y.z` sets the bundle's content version; otherwise the version already in `okf/manifest.json` is kept. |
| `validate_okf.py <dir>` | the bundle directory | nothing | OKF v0.2 conformance, YAML frontmatter, reserved files, `resource` provenance, links and anchors, empty permission cells. Must end with `errors=0 warnings=0 broken_links=0`. The public repository runs the same script as `tools/validate.py`. |

```bash
python3 tools/okf/build_okf.py --version v2.0
python3 tools/okf/validate_okf.py v2.0/okf
```

**Publishing.** Copy `<VERSION>/okf/` as is into `<VERSION>/` of zoho/analytics-okf. The `llms.txt`
links are already built against that repository's raw URL (`publish.okf.raw_base` in the root
`manifest.json`). That repository's own root files (`llms.txt`, `manifest.json` version index, README,
CHANGELOG, `tools/validate.py`) are maintained there; `validate_okf.py` is the same validator.

## Folders

| Folder | Role |
|---|---|
| [`handwritten/<VERSION>/`](handwritten/README.md) | **Input.** Hand-authored concepts (overview, usage guide, foundations, workflow playbooks) copied into the bundle on every build. One directory per API version. |
| [`agent-guide/`](agent-guide/README.md) | Maintainer manual for agents and humans: layout, bundle structure, the source document format the parser expects, change playbooks, builder internals, release checklist. Internal; never published. |

## How the bundle is shaped

- Body links are **relative to the document that contains them**, so they resolve on GitHub, in a
  clone and under any raw-file base. Frontmatter paths (`resource`, `sources[].resource`,
  `api.openapi.file`, `api.sdk_examples`) stay bundle-root paths (`/references/...`) by contract.
- `<VERSION>/okf/llms.txt` is generated with absolute links under `publish.okf.raw_base` of this
  version's entry in the root `manifest.json`, so the bundle is copy-ready for the public repository
  (override with `OKF_RAW_BASE`).
- The domain / group structure comes from the `okf` blocks of `<VERSION>/manifest.json`, so a new
  group or domain starts there. The remaining configuration tables (`TITLE_MAP`, `MD_ONLY_OPS`,
  `CANONICAL`, `ID_SOURCES`, ...) are in `build_okf.py` and documented in
  [`agent-guide/05-builder-internals.md`](agent-guide/05-builder-internals.md).
