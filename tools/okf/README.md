# okf - Open Knowledge Format bundle tooling

Generates, validates and packages the OKF v0.2 bundle of one API version from that version's source
documents. The bundle lives at `<repo>/<VERSION>/okf/` and is committed; it is deleted and rebuilt on
every run, so every rebuild appears as a reviewable diff.

| Script | Reads | Writes | Purpose |
|---|---|---|---|
| `build_okf.py [--version vN.N]` | `<VERSION>/md/`, `<VERSION>/zenesis-oas/` (+ `common/`), `<VERSION>/zenesis-oas-samples/`, `<VERSION>/manifest.json`, `handwritten/<VERSION>/` | `<VERSION>/okf/` (deleted and recreated) | Generates the bundle. Prints `endpoints=… groups=… errors=… sdk=…` on success and `WARN` lines when markdown and OpenAPI disagree. `OKF_BUNDLE_VERSION=x.y.z` sets the bundle's content version; otherwise the version already in `okf/manifest.json` is kept. |
| `validate_okf.py <dir>` | the bundle directory | nothing | OKF v0.2 conformance, YAML frontmatter, reserved files, `resource` provenance, links and anchors, empty permission cells. Must end with `errors=0 warnings=0 broken_links=0`. Copied into the standalone distribution as `tools/validate.py`. |
| `package_okf.py [--versions vN.N ...] [--tarball]` | every `<VERSION>/okf/`, `publish/` templates, `validate_okf.py` | `dist/analytics-okf/` (+ `.tar.gz`) | Assembles the standalone public repository layout used by zoho/analytics-okf: root `README.md`, `llms.txt`, `manifest.json` (version index), `LICENSE.md`, `CHANGELOG.md`, `tools/validate.py`, CI workflow, one `vN.N/` per bundle with `llms.txt` links rebased to the public raw URL. Preserves an existing `dist/analytics-okf/.git`. Never pushes. |

```bash
python3 tools/okf/build_okf.py --version v2.0
python3 tools/okf/validate_okf.py v2.0/okf
python3 tools/okf/package_okf.py --tarball        # only when publishing the standalone repository
```

## Folders

| Folder | Role |
|---|---|
| [`handwritten/<VERSION>/`](handwritten/README.md) | **Input.** Hand-authored concepts (overview, usage guide, foundations, workflow playbooks) copied into the bundle on every build. One directory per API version. |
| [`agent-guide/`](agent-guide/README.md) | Maintainer manual for agents and humans: layout, bundle structure, the source document format the parser expects, change playbooks, builder internals, release checklist. Internal; never published. |
| `publish/` | `README.md`, `CHANGELOG.md`, `LICENSE.md` templates for the standalone distribution (`package_okf.py`). The README carries `{{latest}}` and `{{counts.*}}` placeholders. |

## How the bundle is shaped

- Body links are **relative to the document that contains them**, so they resolve on GitHub, in a
  clone and under any raw-file base. Frontmatter paths (`resource`, `sources[].resource`,
  `api.openapi.file`, `api.sdk_examples`) stay bundle-root paths (`/references/...`) by contract.
- `<VERSION>/okf/llms.txt` is generated with absolute links under `raw_base` of the root
  `manifest.json` (override with `OKF_RAW_BASE`).
- The domain / group structure comes from the `okf` blocks of `<VERSION>/manifest.json`, so a new
  group or domain starts there. The remaining configuration tables (`TITLE_MAP`, `MD_ONLY_OPS`,
  `CANONICAL`, `ID_SOURCES`, ...) are in `build_okf.py` and documented in
  [`agent-guide/05-builder-internals.md`](agent-guide/05-builder-internals.md).
