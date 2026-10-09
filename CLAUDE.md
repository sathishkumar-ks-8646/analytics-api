# analytics-api - agent instructions

This repository holds the Zoho Analytics REST API documents and everything built from them, **one
directory per API version** (`v2.0/` today; `manifest.json` names them and the `latest`). Inside a
version: `md/`, `zenesis-oas/`, `zenesis-oas-samples/` are the **authored sources**; `oas/`, `okf/`,
`postman/` are **generated** and never edited by hand. `tools/` builds and validates all of it.

**If you were given markdown describing an API change (new or changed endpoints, attributes, error
codes, groups), read and follow [`tools/api-agent/AGENT.md`](tools/api-agent/AGENT.md).** It is the
complete procedure: plan with `tools/api-agent/plan.py`, edit the three source files per endpoint,
then run `python3 tools/api-agent/pipeline.py --version v2.0` until every stage is green.

The rules that matter most:

1. An API fact lives in three source files - the group document in `md/`, the operation in
   `zenesis-oas/`, the snippets in `zenesis-oas-samples/` - change all three together.
2. Never edit `oas/` (other than `oas/common/`, which a human places), `okf/` or `postman/`; rebuild them.
3. Never change `https://raw.githubusercontent.com/zoho/analytics-oas/...` `$ref` URLs or
   `oas/common/zoho-analytics-api-common.json`.
4. The markdown heading `## N. Title` and the operation's `x-zenesis-title` are the join key; they
   must match exactly.
5. Only the `x-zenesis-*` keys listed in `tools/zenesis-oas/rules.json` may appear in a specification.

```bash
python3 tools/api-agent/pipeline.py --version v2.0 --check   # is the tree green?
python3 tools/api-agent/pipeline.py --version v2.0           # rebuild everything, stop at the first failure
```

Nothing in this repository pushes anywhere. Commit sources and regenerated artefacts together, only
when asked.
