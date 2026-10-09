# api-agent - update the whole repository from input markdown

The tool an AI agent uses to turn **any markdown description of Zoho Analytics REST API endpoints**
(a hand-off from the API team, a draft reference page, release notes - one file or many) into a
complete, validated change across this repository: the authored sources (`md/`, `zenesis-oas/`,
`zenesis-oas-samples/`) and every artefact generated from them (`oas/`, `okf/`, `postman/`), for one
API version.

The agent does the reading and the writing; the scripts here make the deterministic parts
deterministic and run every other tool in the right order.

| File | What it is |
|---|---|
| [`AGENT.md`](AGENT.md) | **The instructions.** Rules, then four phases: orient, decide, edit the sources, build and make it green. An agent given input markdown starts here. |
| `plan.py` | Reads the input markdown(s), finds every endpoint they describe, matches each against the version's specifications and prints what is new, what exists and differs, and which files to edit. Writes nothing. |
| `scaffold.py` | Prints the three skeletons a new endpoint needs (markdown section, OpenAPI operation with `x-zenesis-*` keys and the right common-file `$ref`, SDK samples entry), wired to the group's files. |
| `pipeline.py` | Runs every build and validation tool for one version in dependency order and stops at the first failure: sources → oas → okf → postman → status. `--check` validates without writing. |

```bash
python3 tools/api-agent/plan.py --version v2.0 Dashboard_API.md Visual_API.md
python3 tools/api-agent/scaffold.py --version v2.0 --title "Clone Dashboard" --method POST \
    --path "/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}/clone" --group Dashboard
python3 tools/api-agent/pipeline.py --version v2.0
```

For an agent running in this repository, `CLAUDE.md` and `AGENTS.md` at the root point here.
