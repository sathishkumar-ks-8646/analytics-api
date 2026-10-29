---
description: Install this migration as a skill your AI coding agent can use - four Agent Skills, a machine-readable mapping, a scanner and an AGENTS.md, each one copyable and downloadable on its own.
---

# AI agent skills

Everything in this guide, packaged for the tools you already code with. Copy a single file, download one skill, or take the whole set as an archive.

:::info Why this exists
Chapter 05 asks you to update the artefacts that *describe* the API. This page is the other direction: it gives your coding agent the migration itself, so the assistant writing your code stops suggesting endpoints that switch off in **March 2027**.
:::

## 1. Take the whole set

<div class="asset-all">
  <div class="asset-all__text">
    <strong>Everything on this page, in one archive.</strong> The four skills, the mapping, the scanner and <code>AGENTS.md</code>. Unzip it anywhere; the layout is already correct.
  </div>
  <a class="asset__btn" href="assets/zoho-analytics-v2-agent-skills.zip" download>Download .zip</a>
</div>

For Claude Code and anything else that reads Agent Skills, the four skill directories go in your project's skills folder:

```bash
unzip zoho-analytics-v2-agent-skills.zip
cp -r agent/skills/* .claude/skills/
```

Install them together. The three task skills reach their shared references through `../zoho-analytics-v2-org-context/references/`, so a task skill installed on its own still works but loses that material.

## 2. Which one do you need?

| You are | ^Take |
|---|---|
| Just getting your agent on the right side of the change | The router skill, plus whichever task skill matches your stack |
| Calling the REST API over raw HTTP | `zoho-analytics-v2-endpoint-migration` |
| Using an official SDK in any of the seven languages | `zoho-analytics-v2-sdk-migration` |
| Looking after specs, collections, RAG indexes or MCP servers | `zoho-analytics-v2-artifact-migration` |
| On Cursor, Copilot, Codex, Zed or anything that reads `AGENTS.md` | `AGENTS.md` — one file, no skill support needed |
| Wanting a number before you plan | `scan.py` |

## 3. The skills

:::asset agent/skills/zoho-analytics-v2-org-context/SKILL.md
**The router.** Carries the four facts every other part depends on — the header is mandatory everywhere, the Organization ID comes from configuration, `8083`/`8084` are not retryable, the dashboard listing is paged — then points at the task skill that matches what the user is doing. Install this one even if you only want one of the others.
:::

:::asset agent/skills/zoho-analytics-v2-endpoint-migration/SKILL.md
**Chapter 03 as a task.** The old-to-new path table, the response-shape changes that a URL rewrite does not cover, CONFIG parameters and limits, the 100-workspace cap, and the errors to handle. Fires on raw HTTP call sites.
:::

:::asset agent/skills/zoho-analytics-v2-sdk-migration/SKILL.md
**Chapter 04 as a task.** The ten moved methods, the per-language build error each one produces, and the runtime trap no compiler catches — `getOrgDashboards` returns an object where the old method returned an array. Fires on SDK code in Java, Python, C#, Go, PHP, Node.js and Ruby.
:::

:::asset agent/skills/zoho-analytics-v2-artifact-migration/SKILL.md
**Chapter 05 as a task.** OpenAPI, the OKF bundle and its vector index, Postman, SDK docs, MCP tool definitions, wikis, Deluge and monitoring. Fires when the thing being changed is a contract rather than code.
:::

## 4. Shared references

These sit inside the router skill. An agent loads them on demand rather than carrying them in context, which is why chapters 01, 02, 06 and 07 are references and not skills of their own — their descriptions would match almost any question about the migration and win the trigger away from the chapter that says what to type.

:::asset agent/skills/zoho-analytics-v2-org-context/references/shared-facts.md
Chapters 01 and 02, condensed: what the header does, where the Organization ID lives, what the removed discovery call returned and where each field went, and what did **not** change.
:::

:::asset agent/skills/zoho-analytics-v2-org-context/references/timeline.md
Chapter 06, condensed: what "deprecated" means in practice, a five-step schedule, and the three checks that together mean you are finished.
:::

:::asset agent/skills/zoho-analytics-v2-org-context/references/troubleshooting.md
Chapter 07, condensed: the symptom-first table, every error code with its symbolic name, and the questions people ask first.
:::

## 5. Data and tooling

:::asset agent/migration-map.json
**The mapping as data.** Eight replaced endpoints, ten SDK methods in both casings, the three new endpoints with scopes and API units, response field mappings, all seventeen error codes with their symbolic names, CONFIG parameters with limits, and the scan patterns. Point an agent at this when you want an exact value rather than prose — and build your own codemod on it.
:::

:::asset agent/scan.py
**The scanner.** Finds every deprecated path, SDK method and response key in a codebase, with file and line. Patterns come from `migration-map.json`, so it holds no facts of its own. Standard library only.

```bash
python3 scan.py /path/to/project          # human-readable
python3 scan.py /path/to/project --json   # for an agent to parse
```

Exits non-zero when something will break, so it works as a CI gate. A `warn` is `getWorkspaceDetails` or `getViewDetails` — correct when already called on a `WorkspaceAPI` or `OrgAPI` instance, broken when still on `AnalyticsClient`.
:::

:::asset agent/AGENTS.md
**For agents that do not read `SKILL.md`.** Cursor, GitHub Copilot, Codex, Zed and others. The same mapping and the same eight rules in one file. Put it at your project root.
:::

:::asset agent/README.md
How the folder is laid out, why it is four skills rather than eight, and how `scan.py --self-check` keeps the mapping honest against these chapters.
:::

## 6. Keeping your copy current

The scanner doubles as a drift guard:

```bash
python3 scan.py --self-check
```

It checks the deadline against this guide's own constant, that every endpoint path and SDK method in the mapping appears in the chapter it claims to come from, that every error code is documented, and that no scan pattern has gone dead. It exits non-zero on any of those.

:::warn Re-download after a guide update
These files are generated from the chapters you are reading. If this guide changes, your copy does not. Re-download rather than hand-patching, for the same reason chapter 05 tells you to re-import a Postman collection rather than merge it.
:::
