# publish/release-notes

Release-notes copy for the hosted Zoho Analytics V2 API **Release Notes** page. One directory per
released version, named for the version itself.

```
release-notes/
├── README.md        you are here — format, slugs, paste target
└── 2.10.0/
    ├── 01-newly-added-apis.md
    └── 02-removed-apis.md
```

A new release is a **sibling** directory — `2.11.0/` next to `2.10.0/`, never a replacement for it
and never a new top-level folder. What shipped stays as published, because the page keeps every
version block and readers arrive at old ones from search.

## Fragment format

Each file is a **fragment**, not a page: plain markdown, authored to be read in order and pasted into
an existing page that already has its own chrome. So:

- **No front matter, no build step, no renderer.** Unlike `../guides/`, nothing here is compiled.
- **The numeric prefix is paste order.** `01` then `02`, concatenated, form one complete version
  section. The split exists so additions and removals can be reviewed separately, not because they
  publish separately.
- **`01` opens with the version `# H1`; `02` opens at `## H2`.** One version, one heading.
- **No links.** The fragments name endpoints and SDK methods in prose and tables; they do not link
  them. Links are added on the published page, where the real slugs are known — see below.
- **`##` sections only below the version heading.** The page nests the whole block under its own
  "Recent Updates" heading, so starting deeper than `##` breaks its outline.

## Paste target

The published Release Notes page, under `<h2>Recent Updates</h2>`, **above** the previous version's
block. Newest version first. Paste `01` then `02`.

## Slug convention for the links added at publish time

None of the endpoints named in a fragment has a published help page at the time the fragment is
written, so no canonical slug exists to copy. When the links go on the page, follow the convention
observed across the existing 178 help URLs:

- read / `GET` → `/analytics/api/v2/metadata-api/<kebab-name>.html`
- mutation / `POST`, `PUT`, `DELETE` → `/analytics/api/v2/modeling-api/<kebab-name>.html`

**Confirm every slug against the published pages before the page goes live.** The convention predicts
the slug; it does not guarantee it.

Two slugs are already verified against the current URL set and are correct:
`metadata-api/workspace-details.html` and `metadata-api/view-details.html` — the two endpoints in
`2.10.0/02-removed-apis.md` that changed in place rather than being removed.

Where a fragment describes a change that has a migration guide, link the guide too. For 2.10.0 that
is `../guides/v2-mandatory-org-context/` — use its hosted base path, which does not exist until the
guide is published.

## 2.10.0

- **35** new endpoints = **34** distinct SDK method names. `getLinkedWorkspaces` is the one name
  serving two endpoints — it exists on both `OrgAPI` (organization-wide) and `WorkspaceAPI`
  (one master workspace).
- **8** endpoints removed, **2** methods moved class, **2** endpoints changed in place.
- Deprecated endpoints answer until **March 2027**; the SDK methods are gone **from 2.10.0**, by
  design. On 2.9.0 and below they are still present and still work.

### The SDK version constant — settled as of 2026-10-29

All seven SDKs now carry `2.10.0` in the version constant that feeds the `User-Agent` header, so the
client identifies itself as the release it is:

| Language | File | Symbol |
|---|---|---|
| Java | `java/source/com/zoho/analytics/client/AnalyticsClient.java` | `client_version` |
| C# | `csharp/source/AnalyticsClient.cs` | `_clientVersion` |
| Go | `go/source/zoho/pkg/analyticsclient/analyticsclient.go` | `ClientVersion` |
| Node.js | `nodejs/source/AnalyticsClient.js` | `clientVersion` |
| PHP | `php/source/AnalyticsClient.php` | `CLIENT_VERSION` |
| Python | `python/source/AnalyticsClient.py` | `CLIENT_VERSION` |
| Ruby | `ruby/source/lib/zoho_analytics_client.rb` | `CLIENT_VERSION` |

Because the constant is now truthful, the migration guide tells readers to check it to find out which
version they are on — see `../guides/v2-mandatory-org-context/04-sdk-migration.md`, section 1. If the
constant ever drifts from the release again, that instruction starts misleading people.
