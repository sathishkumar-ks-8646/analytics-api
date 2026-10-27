# Release notes drafts — Zoho Analytics V2 API 2.10.0

Two HTML fragments, written to drop straight into the existing Release Notes page under
`<h2>Recent Updates</h2>`, above the current "Version 2.9.0" block.

| File | Contents |
|---|---|
| `01-newly-added-apis.html` | The `Version 2.10.0` heading, the SDK download row, **35 new endpoints** grouped by feature, and the Enhancements block. |
| `02-removed-apis.html` | The **8 removed endpoints** with replacements, the **2 SDK methods that moved class**, the **2 endpoints that changed in place**, and links into the migration guide. |

Paste `01` then `02` — together they form one complete `Version 2.10.0` section.

## Before publishing — three things to settle

### 1. Help-page slugs for the new APIs are predicted, not confirmed

None of the 35 new endpoints has a published help page yet, so no canonical slug exists to copy.
The hrefs in `01-newly-added-apis.html` follow the house convention observed across the existing
178 help URLs:

- read / `GET` → `/analytics/api/v2/metadata-api/<kebab-name>.html`
- mutation / `POST`,`PUT`,`DELETE` → `/analytics/api/v2/modeling-api/<kebab-name>.html`

**Confirm every slug against the published pages before this goes live.** The two links in
`02-removed-apis.html` that point at existing pages — `metadata-api/workspace-details.html` and
`metadata-api/view-details.html` — were verified against the current URL set and are correct.

### 2. `MIGRATION_GUIDE_BASE` is a placeholder

`02-removed-apis.html` links the migration guide six times using the literal token
`MIGRATION_GUIDE_BASE`. Replace it with the hosted base path of
`analytics-api/migration/v2-mandatory-org-context` once that is published.

### 3. The SDK still reports `client_version = "2.9.0"`

All seven SDKs carry `2.9.0` in the version constant that feeds the `User-Agent` header. The merge
did not change it, because cutting the version is a release decision rather than part of the merge.
If 2.10.0 should report itself as 2.10.0, these are the lines:

| Language | File | Symbol |
|---|---|---|
| Java | `java/source/com/zoho/analytics/client/AnalyticsClient.java` | `client_version` |
| C# | `csharp/source/AnalyticsClient.cs` | `_clientVersion` |
| Go | `go/source/zoho/pkg/analyticsclient/analyticsclient.go` | `ClientVersion` |
| Node.js | `nodejs/source/AnalyticsClient.js` | `clientVersion` |
| PHP | `php/source/AnalyticsClient.php` | `CLIENT_VERSION` |
| Python | `python/source/AnalyticsClient.py` | client version constant |
| Ruby | `ruby/source/lib/zoho_analytics_client.rb` | client version constant |

Note the SDK download links in `01-newly-added-apis.html` already point at the `2.10.0` CDN path.

## Counts

- **35** new endpoints = **34** distinct SDK method names. `getLinkedWorkspaces` is the one name
  serving two endpoints — it exists on both `OrgAPI` (organization-wide) and `WorkspaceAPI`
  (one master workspace).
- **8** endpoints removed, **2** methods moved class, **2** endpoints changed in place.
- Deprecated endpoints answer until **March 2027**; the SDK methods are gone **now**, by design.
