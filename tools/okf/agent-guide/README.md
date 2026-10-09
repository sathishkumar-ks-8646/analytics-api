# Agent guide for maintaining the Zoho Analytics OKF bundle

This folder is **internal**. It is never packaged or published. Its only purpose is to let an AI agent
(or a human) update the Open Knowledge Format bundle correctly when the Zoho Analytics REST API v2
changes: a new endpoint, a new CONFIG attribute, a changed behaviour, a new error code, a new API group.

All paths in this guide are relative to the repository root of **analytics-api** (the folder that holds
`manifest.json`, `tools/` and one `vN.N/` directory per API version). `<VERSION>` stands for the version
directory being worked on, `v2.0` today. The repository may be cloned anywhere; nothing here depends on
its absolute location.

The API source documents live **in this repository**, under `<VERSION>/md/`, `<VERSION>/zenesis-oas/`
(with `common/zoho-analytics-api-common.json`) and `<VERSION>/zenesis-oas-samples/`. Where a playbook
says to edit one of them, edit it here, run `python3 tools/validate_api_docs.py --strict`, then rebuild
the bundle. There is no submodule and no pin to move.

## The one rule

**Never edit anything under `<VERSION>/okf/` by hand.** That directory is deleted and
regenerated on every build. Change the *inputs*, run the build, validate, and the bundle follows.

```
inputs                                                    generator                          outputs
<VERSION>/md/**/*.md                                   ─┐
<VERSION>/zenesis-oas/*.json                            ├──►  tools/okf/build_okf.py  ──►  <VERSION>/okf/   (the OKF bundle)
<VERSION>/zenesis-oas/common/zoho-analytics-api-common.json │       --version <VERSION>            │
<VERSION>/zenesis-oas-samples/*.json                    │                                         ▼
<VERSION>/manifest.json  (domains, groups, okf slugs)   │                               tools/okf/validate_okf.py <VERSION>/okf
tools/okf/handwritten/<VERSION>/**/*.md                ─┘                               (must print errors=0 broken_links=0)
```

## Where to start, by task

| I need to... | Read | Then edit |
|---|---|---|
| Understand the folder layout and pipeline | [01-repository-layout.md](01-repository-layout.md) | - |
| Understand what each bundle file contains and where it comes from | [02-bundle-structure.md](02-bundle-structure.md) | - |
| Write or edit a source markdown section so the parser picks it up | [03-source-document-format.md](03-source-document-format.md) | `<VERSION>/md/...` |
| Add a new endpoint | [04-change-playbooks.md](04-change-playbooks.md#a-add-a-new-endpoint) | `<VERSION>/md`, `<VERSION>/zenesis-oas`, samples, maybe `tools/okf/build_okf.py` config |
| Add or change a CONFIG attribute or response field | [04-change-playbooks.md](04-change-playbooks.md#b-add-or-change-a-config-attribute-or-response-field) | `<VERSION>/md`, `<VERSION>/zenesis-oas` |
| Add or change an error code | [04-change-playbooks.md](04-change-playbooks.md#c-add-or-change-an-error-code) | `<VERSION>/md`, maybe `CANONICAL` in the builder |
| Add a new API group or domain | [04-change-playbooks.md](04-change-playbooks.md#d-add-a-new-api-group-or-domain) | `<VERSION>/manifest.json` `domains`, new MD file, new or existing OAS file |
| Change a shared rule (auth, headers, criteria, roles...) | [04-change-playbooks.md](04-change-playbooks.md#f-change-a-foundation-document) | `tools/okf/handwritten/<VERSION>/foundations/` |
| Add a workflow playbook | [04-change-playbooks.md](04-change-playbooks.md#g-add-a-workflow-playbook) | `tools/okf/handwritten/<VERSION>/workflows/` |
| Deprecate or remove an endpoint | [04-change-playbooks.md](04-change-playbooks.md#e-deprecate-or-remove-an-endpoint) | `<VERSION>/md`, `<VERSION>/zenesis-oas` (`deprecated: true`) |
| Know which builder table to touch | [05-builder-internals.md](05-builder-internals.md) | `tools/okf/build_okf.py` |
| Release: version, changelog, publish | [06-rules-and-release-checklist.md](06-rules-and-release-checklist.md) | `OKF_BUNDLE_VERSION`, copy `<VERSION>/okf/` |

## The standard loop

```bash
cd <repo-root>
python3 tools/validate_api_docs.py --strict        # the sources themselves: naming, completeness, join keys
python3 tools/okf/build_okf.py --version v2.0      # regenerates v2.0/okf/ ; prints endpoints=… groups=… errors=… sdk=…
python3 tools/okf/validate_okf.py v2.0/okf         # must end with errors=0 warnings=0 broken_links=0
git diff --stat v2.0/okf                           # review what the rebuild changed
```

Publishing is a copy: `v2.0/okf/` goes as is into `v2.0/` of the public analytics-okf repository.

Both scripts need only Python 3.8+ and the standard library. The build takes a few seconds.

If `build_okf.py` prints `WARN no OAS operation for markdown endpoint: <title>` or
`WARN OAS operation without markdown section: <title>`, the markdown and OpenAPI titles disagree;
fix the title or add a `TITLE_MAP` entry (see [05-builder-internals.md](05-builder-internals.md)).
If it prints `unresolved links:`, a markdown link points at a heading or file the resolver cannot find.

## Files in this folder

| File | Purpose |
|---|---|
| `README.md` | This page. Entry point and task router. |
| `01-repository-layout.md` | Every folder in the repository, what it holds, who writes it. |
| `02-bundle-structure.md` | Every directory and concept type in the bundle, the frontmatter contracts, and the source of each body section. |
| `03-source-document-format.md` | The exact markdown, OpenAPI and sample-file conventions the generator parses. |
| `04-change-playbooks.md` | Step-by-step procedures for each kind of API change. |
| `05-builder-internals.md` | The configuration tables and functions inside `tools/okf/build_okf.py`, and the validator and packager. |
| `06-rules-and-release-checklist.md` | Invariants that must hold, things that must never appear, versioning, and the release checklist. |
