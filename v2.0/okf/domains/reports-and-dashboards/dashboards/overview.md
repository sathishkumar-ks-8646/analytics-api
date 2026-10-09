---
type: API Group
title: Dashboards
description: "APIs for creating a dashboard, reading its stored layout, settings and themes, replacing any of those three sections, and listing the dashboards a user owns or can see."
tags:
  - zoho-analytics
  - rest-api-v2
  - reports-and-dashboards
  - dashboards
  - api-group
api:
  domain: reports-and-dashboards
  group: dashboards
  endpoint_count: 6
  endpoints:
    - operation_id: createDashboard
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/dashboards"
      doc: "/domains/reports-and-dashboards/dashboards/create-dashboard.md"
    - operation_id: getDashboardMetadata
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}/metadata"
      doc: "/domains/reports-and-dashboards/dashboards/get-dashboard-metadata.md"
    - operation_id: updateDashboard
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}"
      doc: "/domains/reports-and-dashboards/dashboards/update-dashboard.md"
    - operation_id: getDashboards
      method: GET
      path: "/restapi/v2/dashboards"
      doc: "/domains/reports-and-dashboards/dashboards/get-dashboards.md"
    - operation_id: getOwnedDashboards
      method: GET
      path: "/restapi/v2/dashboards/owned"
      doc: "/domains/reports-and-dashboards/dashboards/get-owned-dashboards.md"
    - operation_id: getSharedDashboards
      method: GET
      path: "/restapi/v2/dashboards/shared"
      doc: "/domains/reports-and-dashboards/dashboards/get-shared-dashboards.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T13:04:25Z
generated:
  by: process:build_okf
  at: 2026-10-09T13:05:37Z
status: stable
---

# Summary

A **dashboard** is a canvas of cards. Each card occupies a rectangle on a fixed 80-unit-wide grid and
holds either a saved report, a block of HTML, a title, an image, an embedded URL, or the interactive
user-filter panel. Dashboards are stored as three independent sections — **layout** (the cards and their
geometry), **settings** (viewer behaviour flags) and **themes** (background, card styling, typography) —
and the APIs in this document let you create a dashboard, read those three sections back, and replace any
of them.

> **The three sections are replaced wholesale, never merged.** Update Dashboard deletes every stored row
> for a section before writing the new one. Sending `settings` with a single key does not patch the
> existing settings — it discards them. Always read, modify, then write back.

> **Tabbed dashboards are out of scope.** Read and Update both reject a tabbed dashboard with error
> **7511**. Only single-canvas dashboards can be managed through these APIs.

---

APIs for creating a dashboard, reading its stored layout, settings and themes, replacing any of those three sections, and listing the dashboards a user owns or can see. A dashboard is a canvas of cards on a fixed 80-unit-wide grid; `layout` travels as a JSON-encoded string on write and comes back as an object on read. Tabbed dashboards cannot be managed through these APIs (7511).

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Create Dashboard](create-dashboard.md) | POST | `/restapi/v2/workspaces/{workspace-id}/dashboards` | `createDashboard` | `ZohoAnalytics.modeling.create` | 200 |
| [Read Dashboard Metadata](get-dashboard-metadata.md) | GET | `/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}/metadata` | `getDashboardMetadata` | `ZohoAnalytics.modeling.read` | 200 |
| [Update Dashboard](update-dashboard.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}` | `updateDashboard` | `ZohoAnalytics.modeling.update` | 204 |
| [Get All Dashboards](get-dashboards.md) | GET | `/restapi/v2/dashboards` | `getDashboards` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Owned Dashboards](get-owned-dashboards.md) | GET | `/restapi/v2/dashboards/owned` | `getOwnedDashboards` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Shared Dashboards](get-shared-dashboards.md) | GET | `/restapi/v2/dashboards/shared` | `getSharedDashboards` | `ZohoAnalytics.metadata.read` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# The layout model

## `layout` is a JSON **string**, not a JSON object

This is the single most common integration mistake. The `layout` attribute inside `CONFIG` is declared as
text and is parsed by the server as a second, nested JSON document:

```
CONFIG={"displayName":"Sales Overview","layout":"{\"1\":{\"type\":\"VIEW\",\"viewName\":\"Sales Chart\",\"width\":80,\"height\":20,\"left\":0,\"top\":0}}"}
```

`themes` and `settings`, by contrast, *are* ordinary nested JSON objects — they are declared
`type="JSONObject"` in the request schema, while `layout` is declared as text. Send `layout` as a string.

> Note the asymmetry with Read Dashboard Metadata, which returns `layout` as a **genuine nested JSON
> object**. A read response cannot be fed straight back into Create or Update; the `layout` value has to
> be re-serialised to a string first. See [Round-tripping a dashboard](overview.md#round-tripping-a-dashboard).

## Card addressing and geometry

The decoded `layout` is an object keyed by arbitrary string card IDs (`"1"`, `"2"`, …). The keys carry no
meaning beyond uniqueness — they are not persisted and the read API renumbers cards from `"1"` in storage
order. Every card carries five positional fields:

| Field | Type | Mandatory | Description |
|-------|------|-----------|-------------|
| `type` | String | **Yes** | Card kind. See [Card types](overview.md#card-types). Must be a JSON string. |
| `width` | Integer | **Yes** | Width in grid units. Must satisfy `left + width <= 80`. |
| `height` | Integer | **Yes** | Height in grid units. |
| `left` | Integer | **Yes** | Zero-based horizontal offset from the left edge of the grid. |
| `top` | Integer | **Yes** | Zero-based vertical offset from the top of the canvas. |

Rules enforced in order, each with its own error code:

1. All five fields present — else **7479**.
2. `width`, `height`, `left`, `top` are JSON integers and `type` is a JSON string — else **7486**.
   Quoted numbers, floats and `null` are all rejected.
3. `type` is one of the eight recognised card types — else **7485**.
4. `left >= 0`, `top >= 0`, `width > 1`, `height > 1`, `left + width <= 80` — else **7480**.
5. The card meets the **per-type minimum size** — else **7512**.
6. Non-`VIEW`, non-`USERFILTERS` cards carry a non-empty `content` — else **7483**.
7. `VIEW` cards resolve to a view that exists (**8027**) and that the caller can read (**7481**).
8. No two cards overlap — else **7482**.
9. At most 100 cards — else **7484**.
10. At least one card is not a `USERFILTERS` card — else **9001**.

## Card types

| `type` | Extra fields | Min height | Min width | Notes |
|--------|--------------|-----------:|----------:|-------|
| `VIEW` | `viewName` (String) | 5 | 10 | Embeds a saved report. `viewName` is matched **case-insensitively** against view display names in the workspace. |
| `HTML` | `content` (String) | 1 | 5 | Free HTML block. Content is XSS-filtered with the `antisamyfilter_reports` profile before storage. |
| `TITLE` | `content` (String) | 3 | 5 | Heading card. |
| `PARA` | `content` (String) | 1 | 5 | Paragraph / text card. |
| `IMAGE` | `content` (String) | 3 | 5 | Image card. A `content` value consisting only of digits is treated as a stored file ID. |
| `EMBED` | `content` (String) | 5 | 5 | External URL / iframe embed. |
| `USERFILTERS` | — | 1 | **80** | The interactive filter panel. Must span the full grid width. |
| `DELETED` | `viewId` (String, optional) | 5 | 10 | Placeholder left behind when an embedded view is removed. Present in read responses; accepted on write for round-tripping. |

> **`properties` on a `VIEW` card is ignored.** The server overwrites it with `{}` on every write. You do
> not need to send it, and sending it has no effect. On non-`VIEW` cards, `properties` and
> `image_properties` *are* stored as card-level key/value properties — values must be strings, and
> `htmlBgColor` is discarded unless it matches `rgb(r, g, b)`.

> **`content` must be non-empty.** An absent key, an explicit `null`, and `""` are all treated the same
> and raise **7483**.

## Generated layouts (`layoutType`)

Setting the top-level `layoutType` attribute to **1, 2, 3 or 4** switches the server into auto-layout
mode. In this mode the geometry you supply is **discarded** and a fresh layout is generated:

1. A full-width `USERFILTERS` card (width 80, height 3) is placed at the top.
2. One full-width `HTML` card (height 5) for every `content` value found anywhere in your input,
   stacked in order.
3. One `VIEW` card (height 20) for every distinct `viewName` found in your input, flowed across
   `layoutType` columns of equal width (the last card in each row absorbs any remainder).

Omitting `layoutType`, or sending `0`, keeps your layout exactly as submitted. Values outside `1-4` are
rejected by the schema with **8509**.

---

# Round-tripping a dashboard

[Read Dashboard Metadata](get-dashboard-metadata.md) is an **inspection** endpoint. Its response is not
a valid Create or Update payload, and several things you write are never read back. Transform the
response as follows before using it as the basis of an update, and keep your own copy of the CONFIG you
submitted for anything in the "lost" list.

## Transformations required

| Difference | What to do |
|---|---|
| `layout` is written as a **string** but returned as a nested **object** | Re-serialise it: `CONFIG.layout = JSON.stringify(response.data.dashboardConfig.layout)`. |
| `objId` is returned but not accepted | Delete it. Otherwise **8542**. |
| `displayName` is returned but rejected by Update | Delete it before an update. Otherwise **8542**. |
| `description` is returned but rejected by Update | Delete it before an update. Otherwise **8542**. |
| Theme numbers are returned as **strings** (`"4"`, `"0.9"`, `"2"`) | `card.blur`, `card.radius`, `card.margin` and `image.transparency` are declared `type="int"`, and `image.flip` as `type="boolean"`. Convert those five back to numbers/booleans before writing. The remaining theme keys are regex-validated and accept the string form. |
| Card IDs are **renumbered** `"1"`…`"N"` in storage order | Do not key your own state off a card ID across a write. |
| `allowExport` always comes back with all six sub-keys | Expected — sub-keys you omit on write are stored as `"false"`. |

## Written but never returned

These are silently lost by a read-modify-write cycle:

| Key | Note |
|---|---|
| `layoutType` (1–4) | Auto-layout is not recorded in the read response. Omit it on update to preserve the stored geometry. |
| Card `properties` | Accepted and stored on non-`VIEW` cards, never returned. (On `VIEW` cards it is overwritten with `{}` at write time, so nothing is lost there.) |
| Card `image_properties` | Accepted and stored, never returned. |
| `allowAllExport` | Reads back as `allowExport`; the alias itself is not recoverable. |

## Returned but not writable

| Key | Note |
|---|---|
| `respContent` on `DELETED` cards | A localised explanation of why the card is a placeholder. Not a write key; drop it. |

## Values that change across a round trip

| Key | Behaviour |
|---|---|
| `viewName` | Matched case-insensitively on write; returned in the view's stored casing. |
| `content` | Passed through the `antisamyfilter_reports` XSS filter on write, and rewritten on read so that stored file IDs become URLs. The string you read is not necessarily the string you wrote — writing it back can change an `IMAGE` or `EMBED` card. |
| `themes.card.border.width` | One submitted value is stored on all four edges and collapses back to one key on read. |
| Background colour | `solid.background`, `gradient.background` and `image.background` share one storage row, re-expanded on read using the stored background type. If that type row is absent the read defaults to `solid.background`. |

---

# Card Type Quick Reference

| `type` | Needs `viewName` | Needs `content` | Min H × W | Returned by Read |
|--------|:----------------:|:---------------:|----------:|:----------------:|
| `VIEW` | Yes | No | 5 × 10 | Yes, with `viewName` |
| `HTML` | No | Yes | 1 × 5 | Yes, with `content` |
| `TITLE` | No | Yes | 3 × 5 | Yes, with `content` |
| `PARA` | No | Yes | 1 × 5 | Yes, with `content` |
| `IMAGE` | No | Yes | 3 × 5 | Yes, with `content` |
| `EMBED` | No | Yes | 5 × 5 | Yes, with `content` |
| `USERFILTERS` | No | No | 1 × 80 | Yes, positional only |
| `DELETED` | No | No | 5 × 10 | Yes, with `viewId` and `respContent` |

---

# Operational Notes and Failure Cases

| Scenario | Behaviour |
|----------|-----------|
| `layout` sent as a nested JSON object instead of a string | Rejected by schema validation. Encode the layout as a string. |
| Two cards reference the same `viewName` | Permitted. The name is resolved once and both cards point at the same view. |
| `viewName` differs only by case from the stored display name | Resolves correctly — lookup is case-insensitive. |
| `layoutType` set to 2 with hand-placed cards | The hand-placed geometry is discarded and a two-column layout is generated from the view names and content strings found in the input. |
| `settings` supplied with one key on Update | The dashboard ends up with exactly one stored setting. Always write the full section. |
| `themes` omitted on Create | The default theme `{"default":"true","type":"2"}` is written. |
| `themes` omitted on Update | The existing theme is left untouched. |
| A `VIEW` card points at a view the caller cannot read | **7481**. The card is not silently dropped. |
| A card is exactly 1 unit tall or wide | **7480** — the minimum is strictly greater than 1, before the per-type minimum is even checked. |
| A `USERFILTERS` card narrower than 80 units | **7512**, not 7480 — the per-type minimum width for the filter panel is the full grid. |
| Dashboard contains only `USERFILTERS` cards | **9001** `DASHBOARD_EMPTY`. |
| Create fails after partial validation | Nothing is written. Create validates the whole CONFIG before persisting, and Update runs inside a transaction. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7018](../../../foundations/error-codes.md#error-7018) | 400 | Malformed URL — the ID is not a valid numeric path segment. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | METADBOBJECTNAMEDUPLICATED — An object with this tableName already exists. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7309](../../../foundations/error-codes.md#error-7309) | 400 | SECURITYNEEDSLOGIN — No authentication was supplied. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7479](../../../foundations/error-codes.md#error-7479) | 400 | A card is missing one or more of type, width, height, left, top. |
| [7480](../../../foundations/error-codes.md#error-7480) | 400 | Negative offset, width/height of 1 or less, or left + width > 80. |
| [7481](../../../foundations/error-codes.md#error-7481) | 400 | The referenced view exists but the caller cannot read it. |
| [7482](../../../foundations/error-codes.md#error-7482) | 400 | Two cards overlap. |
| [7483](../../../foundations/error-codes.md#error-7483) | 400 | A HTML, TITLE, PARA, IMAGE or EMBED card has absent, null or empty content. |
| [7484](../../../foundations/error-codes.md#error-7484) | 400 | More than 100 cards in the layout. |
| [7485](../../../foundations/error-codes.md#error-7485) | 400 | Unrecognised card type. |
| [7486](../../../foundations/error-codes.md#error-7486) | 400 | A positional field has the wrong JSON type. |
| [7487](../../../foundations/error-codes.md#error-7487) | 400 | displayName or layout is absent, null or empty. |
| [7488](../../../foundations/error-codes.md#error-7488) | 400 | A settings or themes key has an empty or null value, or an unrecognised key reached the server. |
| [7491](../../../foundations/error-codes.md#error-7491) | 400 | The sub-object required by themes.type is missing, or card is absent. |
| [7492](../../../foundations/error-codes.md#error-7492) | 400 | A required field inside the type sub-object or inside card is missing. |
| [7493](../../../foundations/error-codes.md#error-7493) | 400 | A sub-object belonging to a different theme type is present, or a forbidden key accompanies default. |
| [7507](../../../foundations/error-codes.md#error-7507) | 400 | displayName exceeds 100 characters, or description exceeds 250. |
| [7510](../../../foundations/error-codes.md#error-7510) | 400 | layout is not parseable JSON, or a themes sub-object is null. |
| [7511](../../../foundations/error-codes.md#error-7511) | 400 | The target is a tabbed dashboard. |
| [7512](../../../foundations/error-codes.md#error-7512) | 400 | INVALIDDATEFORMAT — A date pattern could not be parsed. |
| [7513](../../../foundations/error-codes.md#error-7513) | 400 | chartEffect.type supplied while chartEffect.apply is 1. |
| [7514](../../../foundations/error-codes.md#error-7514) | 400 | chartEffect.apply is 2 but chartEffect.type is absent. |
| [8027](../../../foundations/error-codes.md#error-8027) | 400 | One or more VIEW cards name a view that does not exist in this workspace, or viewName is absent / null / non-string. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | LESSTHANMINOCCURANCE — CONFIG was not sent. |
| [8509](../../../foundations/error-codes.md#error-8509) | 400 | PATTERNNOTMATCHED — roleName contains disallowed characters, or accessType is not one of the three values. |
| [8517](../../../foundations/error-codes.md#error-8517) | 400 | A field has the wrong JSON data type — exclude: "yes", isAxisMerge: "maybe", compType: 123. |
| [8534](../../../foundations/error-codes.md#error-8534) | 400 | JSONPARSEERROR — CONFIG is not valid JSON. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |
| [8542](../../../foundations/error-codes.md#error-8542) | 400 | An unknown key is present in CONFIG, or a windowFunction is mis-configured. |
| [9001](../../../foundations/error-codes.md#error-9001) | 400 | Every card in the layout is a USERFILTERS card. |

# Related

- [Reports & Dashboards](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
