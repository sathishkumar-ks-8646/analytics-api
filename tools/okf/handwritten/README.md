# handwritten - hand-authored bundle concepts (input)

Concept files that no API document supplies: cross-cutting rules and end-to-end playbooks. **One
directory per API version**, named like the version directory it belongs to (`v2.0/`), because the
rules an API version shares are specific to that version. Every file under `<VERSION>/` is copied
verbatim into `<repo>/<VERSION>/okf/` on each build, with `{{NOW}}` and `{{BUILDER}}` placeholders
substituted.

| Here (`tools/okf/handwritten/<VERSION>/`) | In the bundle (`<repo>/<VERSION>/okf/`) |
|---|---|
| `overview.md` | `/overview.md` |
| `how-to-use-this-bundle.md` | `/how-to-use-this-bundle.md` |
| `foundations/<name>.md` | `/foundations/<name>.md` (authentication, request conventions, response envelope, filter criteria, roles, data centers, enums, glossary...) |
| `workflows/<name>.md` | `/workflows/<name>.md` (multi-endpoint playbooks) |

Each file is a full OKF concept: YAML frontmatter starting with `type`, then `title`, `description`,
`tags`, `sources`, and a markdown body. Links in the body may be written bundle-root-relative
(`/foundations/...`); the builder rewrites them to document-relative paths on copy. Quote any
frontmatter scalar that contains `: ` (the validator rejects frontmatter that is not valid YAML).
Copy an existing file of the same kind as the template. Some foundations (`error-codes.md`,
`error-codes-quick-reference.md`, `oauth-scopes.md`, `rate-limits-and-quotas.md`,
`permission-matrix.md`, `identifiers.md`) are **generated** by the builder, not kept here.

A new API version starts by copying the previous version's directory
(`cp -r v2.0 v3.0`) and revising every file for what changed.

Procedures: [../agent-guide/04-change-playbooks.md](../agent-guide/04-change-playbooks.md) sections
F (change a foundation document) and G (add a workflow playbook). Frontmatter contract:
[../agent-guide/02-bundle-structure.md](../agent-guide/02-bundle-structure.md).
