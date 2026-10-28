# agent/ — the migration guide, for AI agents

The chapters one directory up are written for a developer reading them. This
folder is the same migration packaged for the tools that developer works with:
their coding agent, their CI, their editor.

Nothing here is a second source of truth. **The chapters are authoritative**;
everything in this folder restates them as data or as instructions, and
`scan.py --self-check` fails if the two drift apart.

```
agent/
├── README.md              you are here
├── AGENTS.md              cross-vendor pointer — Cursor, Copilot, Codex, Zed
├── migration-map.json     every mapping as structured data
├── scan.py                finds deprecated usage; also the drift guard
└── skills/
    ├── zoho-analytics-v2-org-context/        router + shared references
    │   ├── SKILL.md
    │   └── references/
    │       ├── shared-facts.md               from chapters 01, 02
    │       ├── timeline.md                   from chapter 06
    │       └── troubleshooting.md            from chapter 07
    ├── zoho-analytics-v2-endpoint-migration/ chapter 03 as a task
    ├── zoho-analytics-v2-sdk-migration/      chapter 04 as a task
    └── zoho-analytics-v2-artifact-migration/ chapter 05 as a task
```

## Why four skills and not eight

A skill fires on a **task**. The eight chapters are a mix of tasks and reference
material, and only three of them are tasks someone sits down to do:

| Chapter | Becomes |
|---|---|
| 01 why, 02 what changed | `references/shared-facts.md` |
| **03 endpoint migration** | **`zoho-analytics-v2-endpoint-migration`** |
| **04 SDK migration** | **`zoho-analytics-v2-sdk-migration`** |
| **05 knowledge bases** | **`zoho-analytics-v2-artifact-migration`** |
| 06 timeline | `references/timeline.md` |
| 07 troubleshooting | `references/troubleshooting.md` |

The three tasks have non-overlapping triggers — a reader is calling raw HTTP, *or*
using an SDK, *or* maintaining a spec or collection — so an agent can tell them
apart. Chapters 01, 02, 06 and 07 would match almost any question about the
migration, which is exactly why they are references rather than skills: an agent
reaches them on demand, but they never win a trigger away from the chapter that
says what to type.

## Using it

**Find the work.** Nothing else should happen first; the result tells you which
skills apply and gives the user a number to work down.

```bash
python3 agent/scan.py /path/to/project          # human-readable
python3 agent/scan.py /path/to/project --json   # for an agent to parse
```

Exit code is 1 when anything in the `error` class is present, so it works as a CI
gate. `warn` means a human look is needed — in practice `getWorkspaceDetails` and
`getViewDetails`, which are correct when already called on a `WorkspaceAPI` or
`OrgAPI` instance and broken when still on `AnalyticsClient`.

**Install the skills.** Copy the four directories into the project's skills
folder — for Claude Code, `.claude/skills/`:

```bash
cp -r agent/skills/* /path/to/project/.claude/skills/
```

They install as four siblings and expect to stay siblings: the task skills reach
the shared references through
`../zoho-analytics-v2-org-context/references/`. Installing only one of the three
task skills works; installing a task skill *without* the router one costs it
those references.

The skills also link the chapters through `../../../0N-*.md`, which resolves when
the whole `v2-mandatory-org-context/` directory travels together. Shipping
`agent/` on its own leaves those links dangling — package the folder, not the
subfolder.

**For agents that do not read `SKILL.md`,** put `AGENTS.md` at the project root
instead. It carries the same rules in one file.

## Keeping it true

`migration-map.json` duplicates facts that already exist in the chapters, which
is a drift risk — the same risk the chapters' own README warns about for the
`v2.0/` sources. The guard is:

```bash
python3 agent/scan.py --self-check
```

It verifies that the deadline matches `REMOVAL_DEADLINE` in `build.py`, that
every endpoint path and SDK method in the map appears in the chapter it claims to
come from, that every error code is documented, that every chapter anchor the
scan patterns point at resolves, and that no pattern has gone dead. It exits
non-zero on any of those, so it belongs next to `build.py --check` in CI.

**Run it in the same commit as any chapter edit.** If a fact changes in the
prose and not here, this is what catches it.

## How this reaches end users

`build.py` renders **`08-agent-skills.md` → `08-agent-skills.html`**, the
"AI agent skills" tab in the guide. Every file in this folder appears there as a
panel with **Copy**, **Download** and **View source**, driven by the `:::asset`
directive, which reads the file at build time and inlines it — there is no
server and no `fetch()`, so all three work with the guide opened straight from
the filesystem.

The same build writes **`assets/zoho-analytics-v2-agent-skills.zip`** from this
whole directory, for users who want the set in one go. The archive is
deterministic — sorted entries, fixed timestamps — so an unchanged tree
rebuilds byte-identical and does not churn in git.

Adding a file here puts it in the archive automatically. Giving it a panel on
the page is one `:::asset` block in `08-agent-skills.md`.

## Still worth doing

**Generate the skills' fact tables from `migration-map.json`** at build time.
Today the tables are written out in each `SKILL.md` and `--self-check` catches
drift after the fact; generating them would make drift impossible rather than
merely detectable.
