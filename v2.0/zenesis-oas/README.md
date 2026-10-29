# zenesis-oas - OpenAPI specifications

One OpenAPI 3.1 document per domain, carrying the `x-zenesis-*` vendor extensions the Zenesis
documentation renderer needs. These are valid OpenAPI: vendor extensions are legal anywhere and any
conformant tool ignores `x-` keys. They are hand-edited; nothing generates them.

| File | Groups | Operations |
|---|---|---|
| `org-management-grouped-api.json` | 3 | 10 |
| `user-groups-grouped-api.json` | 4 | 26 |
| `workspace-management-grouped-api.json` | 6 | 35 |
| `data-modeling-schema-grouped-api.json` | 7 | 33 |
| `data-operations-grouped-api.json` | 6 | 20 |
| `views-management-grouped-api.json` | 5 | 26 |
| `reports-dashboards-grouped-api.json` | 2 | 6 |
| `share-publish-grouped-api.json` | 4 | 20 |
| `schedules-alerts-grouped-api.json` | 2 | 16 |
| `dsml-grouped-api.json` | 1 | 11 |
| | **40** | **203** |

## Naming

`<domain-slug>-grouped-api.json`, in this directory. The one subdirectory is
[`common/`](common/zoho-analytics-api-common.json), the components all ten share.
 The slug is the stable identifier of a domain: the samples file is
`<domain-slug>-grouped-api-samples.json`, and both the converter and the OKF builder key off it. It is
deliberately not the markdown folder name - `schedules-alerts` against `09 · Schedules & Alerts` - and
the two are paired in the `domains` list of [`../manifest.json`](../manifest.json).

## Structure of a document

```jsonc
{
  "openapi": "3.1.0",
  "info":    { "title": "Zoho Analytics API", "version": "v2", "description": "…" },
  "servers": [ … ],
  "tags":    [ { "name": "Email Schedules" } ],      // one per API group
  "paths":   { "/restapi/v2/workspaces/{workspace-id}/emailschedules": { … } },
  "components": { … }
}
```

Every operation must carry a `tag` that the document declares, and a title in `x-zenesis-title` (or
`summary`). Security schemes and the OAuth scopes they grant come from
[`common/zoho-analytics-api-common.json`](common/zoho-analytics-api-common.json), not from these
files. Every reference to it is an absolute raw-file URL, the `common_ref` declared in
[`../manifest.json`](../manifest.json); the validator rejects a `$ref` that points anywhere else, and
the converter rewrites that URL to the published repository's copy on the way out.

## Error responses

Every operation models its responses the same way, and the validator enforces it:

```jsonc
"responses": {
  "200": {                                   // exactly one of 200 / 201 / 204
    "description": "…",
    "x-zenesis-statuscodes": [ … ],          // the error-code table rides on the success response
    "content": { … }
  },
  "4XX": { "$ref": "<common_ref>#/components/responses/CommonErrorResponse" },
  "500": { "$ref": "<common_ref>#/components/responses/UnexpectedErrorResponse" }
}
```

`4XX` covers every client error (400, 401, 403, 404 - the exact status is chosen per error code at
runtime) and `500` the server error; both reference the shared responses so the envelope and examples
are defined once. A `default` response is not used. The error-code table sits on the success response
rather than on `4XX` because that is where the converter folds it from and where the OKF builder
reads it.

## Vendor extensions

Ten keys are in use. Each one has a matching rule in `rules.json` in
[tools/zenesis-oas](../../tools/zenesis-oas/README.md), which is what turns
these documents into vendor-neutral OpenAPI:

| Key | What the converter does with it |
|---|---|
| `x-zenesis-title` | Dropped after verifying it equals `summary` |
| `x-zenesis-doc` | Dropped |
| `x-zenesis-usecase-tag` | Dropped |
| `x-zenesis-description-pageName` | Dropped |
| `x-zenesis-shared-note`, `x-zenesis-shared-notes` | Dropped |
| `x-zenesis-sections` | Folded into the operation description under a "Notes" heading |
| `x-zenesis-statuscodes` | Folded into the description as an "Error codes" table |
| `x-zenesis-security` | Folded into the description as "Rate limit" - the unit cost, the category ceiling and each throttle, one bullet apiece |
| `x-zenesis-enums-desc` | Rewritten to `x-enumDescriptions` and `x-enum-varnames` |

One root-level key is also in use and is **not** a `x-zenesis-*` key: `x-api-unit-categories`, described
in [API units and frequency limits](#api-units-and-frequency-limits) below. It is already
vendor-neutral, so the converter passes it through unchanged and no rule is needed for it.

**Introducing an eleventh key is a two-repository change.** `python3 tools/validate_api_docs.py` (run
from the repository root) fails on any `x-zenesis-*` key it does not know, because the converter would
otherwise either warn and stall a release or - if the policy is ever relaxed - drop your content
silently. Add the key to `KNOWN_VENDOR_KEYS` in `tools/validate_api_docs.py` here and a rule to
`rules.json` there, in that order.

## API units and frequency limits

Every call deducts **API units** from the organisation's plan allowance and is counted against a
**per-minute request ceiling**. Both are keyed off the internal gateway action (`api-id`) that the
request's method and path resolve to, so both live on the operation, in `x-zenesis-security` - the key
that already owned "how often may I call this". No eleventh vendor key was introduced.

```jsonc
"x-zenesis-security": {
  "api-id": 2037,                                  // gateway action id - the join key
  "action": "CREATE_QT",                           // gateway action name
  "units": {
    "category": "METADATA",                        // DML | BULK | METADATA
    "cost": 15,
    "basis": "request",                            // "request" or "rows"
    "rows-basis": 1000,                            // present only when basis is "rows"
    "variable": true,                              // present only when the cost depends on the payload
    "note": "15 units per request"
  },
  "frequency": { "category-limit-per-minute": 60 },
  "throttles": [                                   // present only when the URL carries a throttle
    { "duration": 60, "threshold": 20, "lock-period": 600, "per-user": true }
  ]
}
```

The three category ceilings are stated once per document, at the root:

```jsonc
"x-api-unit-categories": {
  "description": "…how the cost is computed…",
  "categories": {
    "DML":      { "frequencyLimitPerMinute": 100 },
    "BULK":     { "frequencyLimitPerMinute": 40  },
    "METADATA": { "frequencyLimitPerMinute": 60  }
  }
}
```

**Derived, not authored.** The source of truth is two configuration files in the product repository:

| File | What it supplies |
|---|---|
| `webapps/db/WEB-INF/gatewayxmls/zagateway-restapi.xml` | `<api TYPE LIMIT>` - the unit category and its per-minute ceiling. `<action ID NAME UNITS ROWS>` - the per-`api-id` cost. `ROWS="1000"` means the cost is per 1000 rows. |
| `webapps/db/WEB-INF/securityxmls/security-restapi.xml` | `<url api-id method path>` - binds each `api-id` to a method and path (a missing `method` means GET). `duration` / `threshold` / `lock-period` / `user` - the per-endpoint throttle, in **minutes**; `x-zenesis-security` carries them in **seconds**. |

The `<internal-services>` and `<units-exempted-apis>` blocks of the gateway configuration are
internal-only and are excluded. The cost formula, from `ZAAPIUnitsHandler.getUnitsSpendForAPICall`, is
`units = (rowsProcessed / rowsBasis) * cost` when a row basis is set and `cost` otherwise - never
rounded up to a whole block. Four operation families resolve to a `0`-cost action and charge against a
second action chosen from the payload (export format, `importType`, `copyData`); for those,
`units.variable` is `true` and `units.note` spells out the real cost.

### What the converter must emit

The published documents in [`../oas/`](../oas/) carry the same facts in two places, because a cost is
both something a human reads and something a rate limiter configures:

- `x-api-units` on each operation - the machine-readable form, camelCase, no `zenesis` prefix, same
  shape as the block above with `windowSeconds` / `lockPeriodSeconds` / `perUser` on the throttle.
- A `**Rate limit**` section in the operation `description`, one bullet for the unit cost, one for the
  category ceiling and one per throttle. The throttle bullet reads
  `Up to {threshold} requests [per user ]per {duration} seconds. Exceeding this blocks further calls
  for {lock-period} seconds.` - the `per user` clause appears only when `per-user` is true, and the
  second sentence only when a lock period is set.
- `x-api-unit-categories` at the document root, passed through unchanged.

## When editing

- Keep the JSON valid and the indentation as the exporter writes it (two spaces, no trailing newline),
  so diffs stay readable.
- Unit costs, categories, ceilings and throttles are derived, not authored. If a cost or a throttle
  changes, it changes in `zagateway-restapi.xml` or `security-restapi.xml` first; regenerate
  `x-zenesis-security` here and the `x-api-units` and `**Rate limit**` output in
  [`../oas/`](../oas/) from the same pass, so the two never disagree.
- A correction made downstream in the published OpenAPI (zoho/analytics-oas) comes back here through
  `make to-zenesis` in the converter, which carries the edit into these files and rebuilds
  `x-zenesis-enums-desc` from `x-enumDescriptions`. Prose that the converter folded into a description
  from `x-zenesis-sections`, `x-zenesis-statuscodes` or `x-zenesis-security` cannot come back that way;
  edit those keys here.
- If you change an operation's title, change the matching `## N. Title` heading in
  [`../md/`](../md/README.md) too. They are joined by that string.
- `x-zenesis-title` and `summary` must be identical. The validator warns when they diverge, because the
  converter drops the title and the difference is lost.
- Add or update the snippets in [`../zenesis-oas-samples/`](../zenesis-oas-samples/README.md) for any
  path or method you add; samples referring to an operation that no longer exists are an error.
