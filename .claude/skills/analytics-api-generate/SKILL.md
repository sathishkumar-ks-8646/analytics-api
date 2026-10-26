---
name: analytics-api-generate
description: Regenerate every Zoho Analytics API knowledge base in the analytics-api repository from the markdown reference in <VERSION>/md/ - the OpenAPI specifications, the SDK samples, the vendor-neutral OAS, the OKF bundle and the Postman collection. Use when markdown API documentation was added or changed and the artefacts must be brought back in step, when asked to "rebuild the artefacts", "run the pipeline", "regenerate everything", "the pipeline is red", "add a new endpoint/group/domain", or when you need to decide which of the five per-knowledge-base skills applies and in what order.
---

# Generate every analytics-api knowledge base from the markdown

The markdown reference in `<VERSION>/md/` is the **only** source of truth for API facts. Five
knowledge bases are derived from it. This skill routes to the right one and runs the whole chain.

Work in the repository root. `<VERSION>` is `v2.0` unless told otherwise — read `latest` from
`manifest.json`:

```bash
python3 -c "import json;print(json.load(open('manifest.json'))['latest'])"
```

## 0. Orient before you touch anything

```bash
cat manifest.json                                       # which versions exist, which is latest
cat <VERSION>/manifest.json                             # domains, groups, tags, okf/postman slugs
python3 tools/api-agent/pipeline.py --check             # is the tree green right now?
```

If `--check` is already red, fix that first and say so — otherwise you cannot tell your change from
the pre-existing breakage.

## 1. The five knowledge bases, and which skill owns each

| # | Knowledge base | Directory | Kind | Skill |
|---|---|---|---|---|
| 1 | OpenAPI 3.1 + `x-zenesis-*` specifications, one per domain | `<V>/zenesis-oas/` | **authored** from `md/` | `analytics-zenesis-oas` |
| 2 | SDK snippets per path+method, nine languages | `<V>/zenesis-oas-samples/` | **authored** from `md/` | `analytics-oas-samples` |
| 3 | Vendor-neutral OpenAPI 3.1 (published to `zoho/analytics-oas`) | `<V>/oas/` | **built** by a converter | `analytics-oas` |
| 4 | Open Knowledge Format v0.2 bundle (published to `zoho/analytics-okf`) | `<V>/okf/` | **built** by a generator | `analytics-okf` |
| 5 | Postman collection + environment | `<V>/postman/` | **built** by a generator | `analytics-postman` |

**Authored vs built is the distinction that matters.** 1 and 2 have no deriving script: you read the
markdown section and write the operation and the snippets by hand, to a fixed contract. 3, 4 and 5
are deleted and rewritten by scripts — never hand-edit them; change the source and rebuild.

### Route by what you were asked

| Request | Go to |
|---|---|
| "Here is markdown describing new/changed endpoints" | **this skill, phase 2** (then skills 1 → 2 → 3 → 4 → 5) |
| "Write / fix the OpenAPI operation, schema, CONFIG, error codes, vendor keys" | `analytics-zenesis-oas` |
| "Write / fix the cURL, Python, Java, Deluge… snippets" | `analytics-oas-samples` |
| "`make compare` differs", "overlays changed", "regenerate `oas/`", "the common file" | `analytics-oas` |
| "`WARN no OAS operation for markdown endpoint`", "unresolved links", "bundle version", "foundations", "workflows/playbooks" | `analytics-okf` |
| "collection is STALE", "request has no description", "add the API reference link", "environment variables" | `analytics-postman` |
| "Add a new API group or a new domain" | **this skill, phase 1b** (manifest first), then 1 → 5 |
| "Just rebuild everything" | **this skill, phase 3** |

## 2. The full procedure, from input markdown to green tree

### Phase 1a — plan

```bash
python3 tools/api-agent/plan.py --version <V> <input1.md> [<input2.md> ...] --json /tmp/plan.json
```

`plan.py` finds every endpoint the input describes and classifies it **NEW** (no such method+path)
or **EXISTING** with the differences it could detect — title, scopes, CONFIG fields missing from the
schema, error codes missing from `x-zenesis-statuscodes` — plus the group it belongs to and the
files to edit. It is a starting point, not the truth: it cannot see a changed sentence, a renamed
field or a behavioural note. **Read the input yourself for those.**

An empty plan means the input is not about endpoints (a shared rule, a new OAuth scope, a new data
centre, a glossary term) → go straight to `analytics-okf`, "hand-written foundations".

### Phase 1b — manifest first, if the shape of the API changed

`<VERSION>/manifest.json` is the spine every tool reads. Add the entry **before** creating any file.

A new **group** goes into the right domain's `groups[]`:

```json
{ "md": "WIDGETS", "tag": "Widgets", "okf": { "slug": "widgets", "title": "Widgets" } }
```

- `md` — the `UPPER_SNAKE_CASE` stem of the file in `<V>/md/<domain folder>/`
- `tag` — the OpenAPI tag, declared in that domain's spec `tags[]` **and** on every operation
- `okf.slug` / `okf.title` — the bundle directory and heading; the Postman group folder name

A new **domain** is a new object in `domains[]`:

```json
{
  "folder": "11 · Widgets",
  "slug": "widgets",
  "groups": [ ... ],
  "okf":     { "slug": "widgets", "title": "Widgets" },
  "postman": { "emoji": "🧩", "title": "Widgets", "covers": "Widget CRUD, placement, refresh" }
}
```

- `folder` — `NN · Title` with a **middle dot U+00B7**, numbered consecutively from `01` in manifest
  order. The validator checks both.
- `slug` — decides the file names `<slug>-grouped-api.json` and `<slug>-grouped-api-samples.json`.
  **It is a contract with every consumer — never rename an existing one.**

Then create, in this order: the markdown group file, the spec (tag + operations), the samples file.
`python3 tools/validate_api_docs.py --strict --version <V>` names whatever is still missing.

### Phase 2 — write the markdown, then the two authored knowledge bases

Per endpoint, in this order:

1. **`<V>/md/<domain folder>/<GROUP>.md`** — the narrative section. Append `## N. <Title>` at the end
   so no existing `## N.` moves, and add its row to the `## Index` table. The exact shape the
   parsers expect is `tools/okf/agent-guide/03-source-document-format.md`; copy a neighbouring
   section in the same file rather than inventing a layout.
2. **`analytics-zenesis-oas`** — the operation + schemas in `<V>/zenesis-oas/<slug>-grouped-api.json`.
3. **`analytics-oas-samples`** — the nine snippets in
   `<V>/zenesis-oas-samples/<slug>-grouped-api-samples.json`.

A skeleton for all three, already wired to the conventions:

```bash
python3 tools/api-agent/scaffold.py --version <V> \
  --title "Create Widget" --method POST \
  --path "/restapi/v2/workspaces/{workspace-id}/widgets" \
  --group "Widgets" --scope ZohoAnalytics.modeling.create \
  --config form --success 200 --org required
```

It prints; it never edits. Paste each skeleton into the file named above it and fill every `TODO`.

Also curate `tools/postman/api-reference-links.json` — endpoint title → public docs page — if the
endpoint has one. Without it the Postman request says "newly added" and links the OpenAPI file.

### Phase 3 — build the three generated knowledge bases

```bash
python3 tools/api-agent/pipeline.py --version <V>
```

Runs every stage in dependency order and **stops at the first failure**, printing that stage's
output in full:

| Stage | Commands | Must end with |
|---|---|---|
| `sources` | `tools/validate_api_docs.py --strict --version <V>` | `errors=0 warnings=0` |
| `oas` | `make -C tools/zenesis-oas check` → `to-analytics` → `compare` | `All checks passed`, then `No differences.` |
| `okf` | `tools/okf/build_okf.py --version <V>` → `tools/okf/validate_okf.py <V>/okf` | no `WARN`, no `unresolved links:`, then `errors=0 warnings=0 broken_links=0` |
| `postman` | `tools/postman/build_postman.py --version <V>` | `requests=N domains=N sections=N` |
| `status` | `git status --short <V>` | the files you changed, for review |

Useful flags:

```bash
python3 tools/api-agent/pipeline.py --version <V> --check                  # validate only, write nothing
python3 tools/api-agent/pipeline.py --version <V> --only okf postman       # a subset
python3 tools/api-agent/pipeline.py --version <V> --from okf               # this stage and later
python3 tools/api-agent/pipeline.py --version <V> --from okf --bundle-version 1.5.0
```

Or one knowledge base at a time: `make oas`, `make okf`, `make postman`, `make sources`,
`make check`, `make build` (each takes `VERSION=`).

**Fix the source for every failure and re-run.** Never patch the output.

### Phase 4 — review and hand over

```bash
git diff --stat                                         # sources + regenerated artefacts, nothing else
git diff -- <V>/md <V>/zenesis-oas <V>/zenesis-oas-samples    # re-read your own edits as the parser would
```

Nothing under `<V>/oas/common/` may change. A diff in `tools/zenesis-oas/overlays/<V>/` is expected
**only** after a vendor-key edit — see `analytics-oas`.

Add a `CHANGELOG.md` entry under *Unreleased*: what changed in terms of endpoints and attributes,
and which input document it came from. Then report:

- the endpoints added or changed,
- **every contradiction you resolved** between the input and the repository,
- **every `TODO` you had to leave**,
- the pipeline's final line.

Commit only when asked — sources and regenerated artefacts in **one** commit, so history says which
source produced which output. Nothing in this repository pushes anywhere.

## 3. Rules that hold across all five knowledge bases

1. **An API fact lives in three source files; change all three together** — the section in `md/`,
   the operation in `zenesis-oas/`, the snippets in `zenesis-oas-samples/`. A fact in one and not
   the others produces artefacts that contradict each other.
2. **Never edit generated directories by hand** — `oas/` (except `oas/common/`), `okf/`, `postman/`.
   They are deleted and rewritten; hand edits are silently discarded on the next run.
3. **Never touch `<V>/oas/common/zoho-analytics-api-common.json`.** A maintainer places it by hand.
   Edit `<V>/zenesis-oas/common/` instead and show the delta with
   `make -C tools/zenesis-oas common-diff`.
4. **One common-file URL, everywhere.** Every remote `$ref`, Zenesis and published alike, is
   `common_ref` from `<V>/manifest.json`:
   `https://raw.githubusercontent.com/zoho/analytics-oas/refs/heads/main/v2.0/common/zoho-analytics-api-common.json`.
   Any other remote `$ref` is a hard error.
5. **Titles are the join key.** `## N. Title` in the markdown == `x-zenesis-title` in the operation,
   character for character. Rename both or neither; if they genuinely must differ, add a `TITLE_MAP`
   entry in `tools/okf/build_okf.py`.
6. **Only the ten vendor keys that have rules** (`tools/zenesis-oas/rules.json`, mirrored by
   `KNOWN_VENDOR_KEYS` in `tools/validate_api_docs.py`). An unknown `x-zenesis-*` key fails
   validation rather than being dropped silently downstream.
7. **Error responses are `4XX` and `500`**, each a `$ref` to the shared responses. Never `default`.
8. **Write for an external developer.** No internal class names, XML attribute names, template names
   or authoring-system file names in any prose, in any knowledge base.
9. **Do not guess facts.** If the input does not state a scope, permission, status or error code,
   copy the fact from a sibling endpoint in the same group *and say so*, or leave a clearly marked
   `TODO`. The validators cannot catch an invented value.
10. **Keep the sources' voice.** Copy the shape of the neighbouring section, operation or snippet
    exactly — table columns, bold case headings, `**HTTP NNN**` response labels, example naming.

## 4. Troubleshooting index

| Message | Meaning | Skill |
|---|---|---|
| `folder name must be "NN · Title" with a middle dot` | ASCII `·` substituted, or wrong number | this skill, 1b |
| `group is not listed in <V>/manifest.json` | file created before the manifest entry | this skill, 1b |
| `tag 'X' has no markdown group` / `tag 'X' is expected ... but is not declared` | manifest `tag` ↔ spec `tags[]` mismatch | `analytics-zenesis-oas` |
| `x-zenesis-... is used but has no rule in the converter` | unknown vendor key | `analytics-zenesis-oas` |
| `must have exactly one success response` / `is missing the "4XX" error response` / `uses a "default" response` | response modelling | `analytics-zenesis-oas` |
| `x-zenesis-statuscodes sits on the "4XX" response` | it belongs on the **success** response | `analytics-zenesis-oas` |
| `remote $ref targets ...` | wrong common-file URL | `analytics-zenesis-oas` |
| `samples for X, which the spec does not define` / `no SDK samples for X` | samples key ≠ spec path/method | `analytics-oas-samples` |
| `round trip lost data` / overlays diff | a vendor-key edit; regenerate overlays | `analytics-oas` |
| `make compare` prints differences | `oas/` is stale or hand-edited | `analytics-oas` |
| `WARN no OAS operation for markdown endpoint` / `OAS operation without markdown section` | titles differ (rule 5) | `analytics-okf` |
| `unresolved links:` | a markdown link the builder cannot resolve | `analytics-okf` |
| `empty api.permission_required` / `empty permission cell` | the section has no `**Permission Required**` row | `analytics-okf` |
| `frontmatter is not valid YAML` | a hand-written concept title/description contains `: ` — quote it | `analytics-okf` |
| Postman `--check` reports `STALE` | a source changed after the last build | `analytics-postman` |
| request says "newly added" | no entry in `api-reference-links.json` | `analytics-postman` |

## 5. Publishing

| What | Where | How |
|---|---|---|
| `<V>/oas/` | `zoho/analytics-oas` `<V>/` | copy as is, after `make -C tools/zenesis-oas compare` reports no differences |
| `<V>/okf/` | `zoho/analytics-okf` `<V>/` | copy as is; `llms.txt` links already use `publish.okf.raw_base`. That repo's own root files are maintained there |
| `<V>/postman/` | Postman workspace | import the collection and the environment |
| `<V>/md`, `zenesis-oas`, `zenesis-oas-samples` | the documentation site (Zenesis renderer) | read directly from this repository |

Document versioning lives in `CHANGELOG.md` (semver: major for a removed/renamed endpoint or a
layout change, minor for additions, patch for corrections). The OKF bundle carries its own content
version — see `analytics-okf`.
