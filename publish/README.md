# publish/

Everything in this tree is written **for API consumers**, not for this repository. The rest of
`analytics-api/` documents the API to itself — specs, bundles, generators, SDK sources. What lands
here is the prose an external developer actually reads when a release changes something under them.

Nothing in `publish/` is generated from `vN.N/`. These are authored documents, kept next to the
specs so a breaking change and its explanation move in the same commit.

```
publish/
├── README.md                          you are here
├── release-notes/                     fragments for the hosted Release Notes page, one dir per version
│   ├── README.md                      fragment format, slug convention, paste target
│   └── 2.10.0/
│       ├── 01-newly-added-apis.md
│       └── 02-removed-apis.md
└── guides/                            standalone migration guides, one dir per breaking change
    └── v2-mandatory-org-context/      v2: every endpoint now requires ZANALYTICS-ORGID
        ├── build.py                   renders each *.md into an *.html sibling
        ├── index.md / index.html       start here; 8 chapters, Markdown and HTML
        └── agent/                     AI-agent skills + migration-map.json for the same change
```

## The two subtrees, and who publishes them where

| Subtree | Form | Published by | Published where |
|---|---|---|---|
| `release-notes/<version>/` | Short markdown fragments, no build step, no links | Whoever updates the help site for a release | Pasted into the existing **Release Notes** page, newest version on top |
| `guides/<slug>/` | A self-contained static site; markdown is authored, `build.py` renders the HTML | The guide's own author, by handing over the rendered folder | Hosted as its own page set, linked from the release notes and from the affected API pages |

The split is about lifetime. A release-notes fragment is read once, in the week of the release, and
then becomes history — so it is a flat list, it names things, and it stops. A guide is read for as
long as the deprecation window is open — so it is paginated, navigable, repeats its warnings on every
page, and carries a deadline constant that must stay accurate.

## Adding to either tree

**A new release** gets a sibling directory under `release-notes/`, named for the version:
`release-notes/2.11.0/`. It does not get a new top-level directory, and it does not replace 2.10.0 —
the fragments for a shipped version stay as published. See `release-notes/README.md` for the
fragment format and the paste target.

**A new breaking change** gets a sibling directory under `guides/`, named for the change rather than
the version — `v2-mandatory-org-context`, not `v2.10.0` — because a reader arrives looking for the
problem they have, and because one change can span several releases. Copy an existing guide's
`build.py` and assets; each guide builds independently with no shared tooling.

## Checking before you hand anything over

```bash
cd publish/guides/v2-mandatory-org-context
python3 build.py --check        # every internal link and anchor resolves
python3 agent/scan.py --self-check   # the deadline and SDK-version constants have not drifted
```

Release-notes fragments have no build and no validator. What they do have is facts that go stale —
endpoint counts, version numbers, whether a deprecation date has moved. Re-read them against
`CHANGELOG.md` for the release before publishing.
