# 04 - Change playbooks

Each playbook lists the files to touch, in order, and ends with the same two commands:

```bash
cd <repo-root>
python3 tools/okf/build_okf.py --version <VERSION>     # must print endpoints=… groups=… errors=… sdk=… with no WARN lines
python3 tools/okf/validate_okf.py <VERSION>/okf        # must end errors=0 warnings=0 broken_links=0
```

Or run every tool at once: `python3 tools/api-agent/pipeline.py --version <VERSION>`.

Never edit `<VERSION>/okf/` or `dist/` directly — see [01-repository-layout.md](01-repository-layout.md).

Every path under `<VERSION>/` is in this repository. After editing the sources run
`python3 tools/validate_api_docs.py --strict` (it must end with `errors=0 warnings=0`) before the two commands above.

---

## A. Add a new endpoint

1. **Pick the domain and group.** Find the group's markdown file under `<VERSION>/md/<domain folder>/`.
   If the group or domain doesn't exist yet, do playbook D first.
2. **Add the markdown section.** Append a new `## N. <Title>` section at the end of the group file
   (appending avoids renumbering every later section and its `#N-slug` links). Follow the endpoint
   skeleton in [03-source-document-format.md §A.1](03-source-document-format.md): intro paragraph(s),
   attribute table, a request block (`### CONFIG Parameters` or whichever name fits), `### Sample
   Requests`, `### Sample Responses`, `### Response Fields`, `### Notes & Behaviour`, `### Error Codes`.
   Use the exact block names from the classifier table in 03 — an unrecognised name lands under
   generic Notes & Behaviour instead of its intended section.
3. **Update the group's `## Index` table** with the new row, and add the new row's `<N>` in any spot
   you actually inserted-in-the-middle-of (again, prefer appending).
4. **Add the OpenAPI operation** to `<VERSION>/zenesis-oas/<domain>-grouped-api.json`:
   - `operationId` unique across every file.
   - `x-zenesis-title` (or `summary`) equal to the markdown `## N. Title`, character for character —
     otherwise add a `TITLE_MAP` entry in `tools/okf/build_okf.py` (see
     [05-builder-internals.md](05-builder-internals.md)).
   - `tags[0]` set to the group's tag; `parameters[]` for path/header/query values; `requestBody` with
     a `CONFIG` property under the correct content type if the endpoint takes one; `responses` with a
     200/201/204 success entry and `4XX`/`500` pointing at the common file's `CommonErrorResponse`/
     `UnexpectedErrorResponse` (use the same `$ref` form the other operations already use).
   - Add `x-zenesis-security.throttles[0]` if the endpoint is rate-limited.
5. **No OpenAPI yet?** Add a `MD_ONLY_OPS` entry (markdown title -> synthesized operation ID) in
   `tools/okf/build_okf.py` instead of skipping the endpoint. Remove the entry once the real operation
   exists.
6. **Add SDK samples** (optional but expected) to
   `<VERSION>/zenesis-oas-samples/<domain>-grouped-api-samples.json`, keyed by the exact OpenAPI path
   template and lower-case method, using the language keys in `LANG_FENCE`/`LANG_TITLE` order. No
   entry simply means no SDK Example document is generated for that operation.
7. **New identifiers or error codes introduced?** See playbooks B/C below.
8. Rebuild and validate. Fix any `WARN no OAS operation for markdown endpoint`, `WARN OAS operation
   without markdown section`, or `unresolved links:` output before moving on.

## B. Add or change a CONFIG attribute or response field

1. Edit the relevant `###` block in the endpoint's markdown section — the request block (`CONFIG
   Parameters` or whichever name the file already uses) or `Response Fields` — adding or editing a
   table row: Parameter, Type, Mandatory, Default, Description (match the surrounding rows' style).
2. If the value has a fixed set of options, add or update the `#### <field> Values` sub-table (H4,
   becomes H3 in the bundle).
3. Mirror the change in the OpenAPI operation's `requestBody` schema properties (for a request
   attribute) or the response schema in `components.schemas` (for a response field), so the two
   sources stay in step — see "Two pairs that must stay in step" in
   [01-repository-layout.md](01-repository-layout.md).
4. Check `### Sample Requests`, `### Sample Responses`, and `### Notes & Behaviour` in the same
   section for stale examples that no longer match the new attribute/field, and update them.
5. Rebuild and validate.

## C. Add or change an error code

1. Add or edit a row in the endpoint's `### Error Codes` table. First cell is the numeric code
   (`7104`, `**7104**`, or several like `8085 / 8086`); a backticked `UPPER_SNAKE` constant at the
   start of the reason cell becomes that code's summary constant.
2. To have the catalog record the right HTTP status from evidence, add a `### Sample Responses` block
   whose bold line reads `**HTTP NNN <reason> — description**` immediately above a &#96;&#96;&#96;json
   block containing `"errorCode": N`. Without that, the status falls back to the `DEFAULT_HTTP` table
   entry for the code, or 400.
3. If the code is reused across many operations and the aggregated wording would be misleading, add or
   edit a `CANONICAL` entry (code -> `(meaning, resolution)`) in `tools/okf/build_okf.py` — this overrides
   the per-operation aggregation for that code everywhere.
4. Also add the code to the OpenAPI operation's `responses.*.x-zenesis-statuscodes[]` as
   `{name, description, resolution}` if it should appear even without a markdown row. Merge order is:
   markdown rows first, then OAS statuscodes not already present, then 8535 and 7005 if still absent.
5. Never hand-write a link to the error catalog. Any backticked 4-to-6-digit number that is a known
   code is auto-linked by `link_error_codes`; hand-written links will not match the generator's anchor
   scheme.
6. Rebuild and validate; confirm the `errors=` count in the build output changed as expected.

## D. Add a new API group or domain

1. **New group in an existing domain:** create `<VERSION>/md/<domain folder>/<GROUP>.md` following the
   file skeleton in [03-source-document-format.md §A](03-source-document-format.md) (H1, preamble,
   optional concept sections, `## Index`, `## 1. …` endpoint sections, Appendices A–D as needed). Add
   `{ "md": <stem>, "tag": <OpenAPI tag>, "okf": { "slug": ..., "title": ... } }` to that domain's `groups` in
   `<VERSION>/manifest.json`.
2. **New domain:** create the markdown folder under `<VERSION>/md/`, create or choose the OpenAPI file
   `<VERSION>/zenesis-oas/<domain>-grouped-api.json`, and add a full new entry to `domains` in `<VERSION>/manifest.json`:
   `folder`, `slug` (the OpenAPI file is `<slug>-grouped-api.json`), `groups`, and the `okf` and `postman` blocks.
3. Set `info.description` and the relevant `tags[].description` in the domain's OpenAPI file — these
   feed `render_domain_overview` for `/domains/<domain>/overview.md`.
4. If any markdown file will link to this group using the legacy `<STEM>_API_DOC_INFO.md` pattern and
   `kebab(stem)` doesn't already equal the new group slug, add a `LEGACY_ALIAS` entry in
   `tools/okf/build_okf.py`.
5. Create the matching `<VERSION>/zenesis-oas-samples/<domain>-grouped-api-samples.json` (can start
   with no entries and be filled in per operation later).
6. Add each endpoint following playbook A.
7. Rebuild and validate; confirm the new domain/group shows up in `endpoint-catalog.md`,
   `/domains/<domain>/`, and the root index, and that `groups=`/`endpoints=` in the build output moved
   as expected.

## E. Deprecate or remove an endpoint

**Deprecate (keep it, mark it):**
1. Set `deprecated: true` on the OpenAPI operation — this becomes `status: deprecated` in the endpoint
   frontmatter automatically.
2. Optionally note the replacement in the markdown `### Notes & Behaviour` block.

**Remove entirely:**
1. Delete the `## N. Title` section from the markdown group file, delete the OpenAPI operation, and
   delete its entry in the SDK samples file.
2. Renumber the remaining `## N.` sections in that file if the removed one wasn't last, and fix every
   `#N-slug` link that pointed at it or at sections after it. Update the `## Index` table.
3. Remove any now-dangling entries in `MD_ONLY_OPS`, `TITLE_MAP`, or `ID_SOURCES` in
   `tools/okf/build_okf.py` that existed only for this endpoint.
4. Search other group files for "Dependency" notes or cross-links referencing the removed endpoint's
   title or anchor, and fix or remove them.
5. Rebuild and validate — `validate_okf.py` will surface any link it can no longer resolve.

## F. Change a foundation document

1. **Generated foundations** (`error-codes.md`, `error-codes-quick-reference.md`, `oauth-scopes.md`,
   `rate-limits-and-quotas.md`, `permission-matrix.md`, `identifiers.md`) are never edited directly.
   Change their sources instead: error tables (playbook C), scopes in
   `<VERSION>/zenesis-oas/common/zoho-analytics-api-common.json`, `x-zenesis-security.throttles` or `**Rate Limit**` rows,
   `**Permission Required**` rows, or the `ID_SOURCES` table / OpenAPI parameters.
2. **Hand-written foundations** (the other 13 files listed in
   [02-bundle-structure.md](02-bundle-structure.md)) are edited directly under
   `tools/okf/handwritten/<VERSION>/foundations/<name>.md`. They are copied verbatim on every build, not regenerated,
   so whenever a rule they describe changes elsewhere in the sources, review the matching foundation
   file by hand.
3. Leave `{{NOW}}` / `{{BUILDER}}` placeholders in place where present — they're expanded at copy time.
4. Rebuild and validate — the validator checks structure (frontmatter, links), not the accuracy of
   hand-written prose, so read your change back before committing.

## G. Add a workflow playbook

1. Add a new `.md` file under `tools/okf/handwritten/<VERSION>/workflows/`. Match the style and frontmatter of the
   existing playbooks in that folder.
2. It is copied verbatim to `/workflows/<name>.md` in the bundle on the next build — no config table
   entry is needed.
3. Link to real endpoint files using bundle-relative paths (e.g.
   `/domains/<domain>/<group>/<endpoint-file>.md`), not the legacy `<GROUP>_API_DOC_INFO.md#N-slug`
   syntax used inside `<VERSION>/md` — that syntax only applies to source markdown, not files that are
   already inside the generated bundle.
4. Rebuild and validate.
