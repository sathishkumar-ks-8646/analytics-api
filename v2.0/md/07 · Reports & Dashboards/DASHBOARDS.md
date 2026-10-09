# Zoho Analytics V2 REST API — Dashboards

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

## Index

| # | API Name | Method | URL |
|---|----------|--------|-----|
| 1 | [Create Dashboard](#1-create-dashboard) | POST | `/restapi/v2/workspaces/<workspace-id>/dashboards` |
| 2 | [Read Dashboard Metadata](#2-read-dashboard-metadata) | GET | `/restapi/v2/workspaces/<workspace-id>/dashboards/<dashboard-id>/metadata` |
| 3 | [Update Dashboard](#3-update-dashboard) | PUT | `/restapi/v2/workspaces/<workspace-id>/dashboards/<dashboard-id>` |
| 4 | [Get All Dashboards](#4-get-all-dashboards) | GET | `/restapi/v2/dashboards` |
| 5 | [Get Owned Dashboards](#5-get-owned-dashboards) | GET | `/restapi/v2/dashboards/owned` |
| 6 | [Get Shared Dashboards](#6-get-shared-dashboards) | GET | `/restapi/v2/dashboards/shared` |

---

## The layout model

### `layout` is a JSON **string**, not a JSON object

This is the single most common integration mistake. The `layout` attribute inside `CONFIG` is declared as
text and is parsed by the server as a second, nested JSON document:

```
CONFIG={"displayName":"Sales Overview","layout":"{\"1\":{\"type\":\"VIEW\",\"viewName\":\"Sales Chart\",\"width\":80,\"height\":20,\"left\":0,\"top\":0}}"}
```

`themes` and `settings`, by contrast, *are* ordinary nested JSON objects — they are declared
`type="JSONObject"` in the request schema, while `layout` is declared as text. Send `layout` as a string.

> Note the asymmetry with Read Dashboard Metadata, which returns `layout` as a **genuine nested JSON
> object**. A read response cannot be fed straight back into Create or Update; the `layout` value has to
> be re-serialised to a string first. See [Round-tripping a dashboard](#round-tripping-a-dashboard).

### Card addressing and geometry

The decoded `layout` is an object keyed by arbitrary string card IDs (`"1"`, `"2"`, …). The keys carry no
meaning beyond uniqueness — they are not persisted and the read API renumbers cards from `"1"` in storage
order. Every card carries five positional fields:

| Field | Type | Mandatory | Description |
|-------|------|-----------|-------------|
| `type` | String | **Yes** | Card kind. See [Card types](#card-types). Must be a JSON string. |
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

### Card types

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

### Generated layouts (`layoutType`)

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

## Round-tripping a dashboard

[Read Dashboard Metadata](#2-read-dashboard-metadata) is an **inspection** endpoint. Its response is not
a valid Create or Update payload, and several things you write are never read back. Transform the
response as follows before using it as the basis of an update, and keep your own copy of the CONFIG you
submitted for anything in the "lost" list.

### Transformations required

| Difference | What to do |
|---|---|
| `layout` is written as a **string** but returned as a nested **object** | Re-serialise it: `CONFIG.layout = JSON.stringify(response.data.dashboardConfig.layout)`. |
| `objId` is returned but not accepted | Delete it. Otherwise **8542**. |
| `displayName` is returned but rejected by Update | Delete it before an update. Otherwise **8542**. |
| `description` is returned but rejected by Update | Delete it before an update. Otherwise **8542**. |
| Theme numbers are returned as **strings** (`"4"`, `"0.9"`, `"2"`) | `card.blur`, `card.radius`, `card.margin` and `image.transparency` are declared `type="int"`, and `image.flip` as `type="boolean"`. Convert those five back to numbers/booleans before writing. The remaining theme keys are regex-validated and accept the string form. |
| Card IDs are **renumbered** `"1"`…`"N"` in storage order | Do not key your own state off a card ID across a write. |
| `allowExport` always comes back with all six sub-keys | Expected — sub-keys you omit on write are stored as `"false"`. |

### Written but never returned

These are silently lost by a read-modify-write cycle:

| Key | Note |
|---|---|
| `layoutType` (1–4) | Auto-layout is not recorded in the read response. Omit it on update to preserve the stored geometry. |
| Card `properties` | Accepted and stored on non-`VIEW` cards, never returned. (On `VIEW` cards it is overwritten with `{}` at write time, so nothing is lost there.) |
| Card `image_properties` | Accepted and stored, never returned. |
| `allowAllExport` | Reads back as `allowExport`; the alias itself is not recoverable. |

### Returned but not writable

| Key | Note |
|---|---|
| `respContent` on `DELETED` cards | A localised explanation of why the card is a placeholder. Not a write key; drop it. |

### Values that change across a round trip

| Key | Behaviour |
|---|---|
| `viewName` | Matched case-insensitively on write; returned in the view's stored casing. |
| `content` | Passed through the `antisamyfilter_reports` XSS filter on write, and rewritten on read so that stored file IDs become URLs. The string you read is not necessarily the string you wrote — writing it back can change an `IMAGE` or `EMBED` card. |
| `themes.card.border.width` | One submitted value is stored on all four edges and collapses back to one key on read. |
| Background colour | `solid.background`, `gradient.background` and `image.background` share one storage row, re-expanded on read using the stored background type. If that type row is absent the read defaults to `solid.background`. |

---

## 1. Create Dashboard

Creates a dashboard in the given workspace and returns its ID.

| Attribute | Value |
|-----------|-------|
| **Method** | POST |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/dashboards` |
| **OAuth Scope** | `ZohoAnalytics.modeling.create` |
| **ZANALYTICS-ORGID Header** | **Mandatory** |
| **Content-Type** | `application/x-www-form-urlencoded` |
| **Permission Required** | Workspace Admin / Organization Admin, or a shared or group user holding **Create Report** permission on the workspace. A Custom Role user must have the Create Report permission explicitly granted, otherwise the call is rejected before any validation runs. |
| **Custom domain** | Permitted, but only when the target workspace is mapped to the calling white-label domain. A mismatch raises **7301**. |
| **Throttle** | 10 requests per minute per user; 10-minute lock-out on breach. |

### CONFIG Parameter

`CONFIG` is a JSON object sent as a form-encoded body parameter. Maximum encoded size 5,000,000
characters.

| Field | Type | Mandatory | Constraints | Description |
|-------|------|-----------|-------------|-------------|
| `displayName` | String | **Yes** | 1–100 characters; unique within the workspace | Name of the dashboard. |
| `layout` | String | **Yes** | JSON-encoded string, max 1,000,000 characters | The card layout. See [The layout model](#the-layout-model). |
| `description` | String | No | Max 250 characters | Free-text description. |
| `themes` | JSONObject | No | Max 10,000 characters | Visual theme. See [Themes](#themes). Omitting it writes the default theme `{"default":"true","type":"2"}`. |
| `settings` | JSONObject | No | Max 10,000 characters | Viewer behaviour flags. See [Settings](#settings). Omitting it writes the full default settings object. |
| `layoutType` | Integer | No | 1–4 | Generate a 1/2/3/4-column layout instead of using the supplied geometry. See [Generated layouts](#generated-layouts-layouttype). |

### Settings

Every flag below is optional. Boolean flags are stored as the strings `"true"` / `"false"`; the request
schema declares them as booleans, so JSON `true` / `false` is the form to send and is what the read API
returns as `"true"` / `"false"`.

Supplying a partial `settings` object writes **only** those keys — it does not merge with the defaults,
so unspecified flags fall back to whatever the dashboard renderer treats as unset rather than to the
values in the Default column.

| Field | Values | Default | Description |
|-------|--------|---------|-------------|
| `allowDrillDown` | `"true"` / `"false"` | `"true"` | Allow drill-down on chart data points. |
| `hideColumnOptions` | `"true"` / `"false"` | `"true"` | Hide column-level options from viewers. |
| `smartAlignCharts` | `"true"` / `"false"` | `"true"` | Auto-align chart elements across cards. |
| `enableSortMenu` | `"true"` / `"false"` | `"true"` | Show the sort menu on embedded reports. |
| `reportAsFilter` | `"true"` / `"false"` | `"false"` | Clicking a data point filters the other cards. |
| `showContextualOptions` | `"true"` / `"false"` | `"true"` | Show contextual action menus on cards. |
| `allowVUD` | `"true"` / `"false"` | `"true"` | Enable View Underlying Data on embedded reports. |
| `allowInsights` | `"true"` / `"false"` | `"true"` | Enable Zia Insights on embedded reports. |
| `allowEmbedInsights` | `"true"` / `"false"` | `"true"` | Enable Insights in embedded/published views. |
| `fitToWidth` | `"true"` / `"false"` | `"true"` | Scale embedded reports to the card width. |
| `enableGlobalUF` | `"true"` / `"false"` | `"false"` | Enable the global user filter. |
| `enableGlobalValueUF` | `"true"` / `"false"` | *(unset)* | Enable value-based global user filters. |
| `applyImmediateUF` | `"true"` / `"false"` | `"true"` | Apply user-filter changes without a confirm click. |
| `timeSlicer` | `"true"` / `"false"` | `"false"` | Enable the time-slicer widget. |
| `mapSync` | `"true"` / `"false"` | *(unset)* | Synchronise pan/zoom across map cards. |
| `layoutType` | `web` \| `custom_width` \| `tabloid_1056` \| `letter_816` \| `a4_797` \| `a3_1123` | `"web"` | Target page layout. **`mobile` is not a valid value.** |
| `layoutWidth` | String of 1–4 digits | `"1279"` | Fixed layout width in pixels. |
| `allowExport` | JSONObject | `"true"` (all formats) | Per-format export control. Sub-keys `csv`, `excel`, `html`, `image`, `pdf`, `zohoSheet`, each `"true"` / `"false"`. Any sub-key you omit is stored as `"false"`. |
| `allowAllExport` | `"true"` / `"false"` | — | Alias of `allowExport` used as a single master switch. |

### Themes

`themes` is a nested JSON object. Its shape is driven by `type`.

**Mode A — default theme.** Send `{"default": "true"}` (or `"unset"`). When `default` is present,
`type`, `solid`, `gradient`, `image`, `card`, `chartEffect` and `palette` must all be **absent**
(**7493** otherwise).

**Mode B — explicit theme.** `type` is mandatory and selects which sub-object is required:

| `type` | Required in the type object | Required in `card` | Must be absent |
|--------|-----------------------------|--------------------|----------------|
| `solid` | `background` | `background` | `gradient`, `image` |
| `gradient` | `background`, `startColor`, `endColor`, `mode` | `background`, `opacity`, `blur` | `solid`, `image` |
| `image` | `url`, `background` | `background`, `opacity`, `blur` | `solid`, `gradient` |

For `gradient`, exactly one of `linear` / `radial` must be present and it must match `mode` — supplying
both, neither, or the one that does not match `mode` raises **7492** / **7493**.

Accepted keys and their ranges:

| Key | Type / range |
|-----|--------------|
| `default` | `"true"` \| `"unset"` |
| `layoutType` | `1`–`6` |
| `type` | `solid` \| `gradient` \| `image` |
| `solid.background` | Colour |
| `gradient.background`, `gradient.startColor`, `gradient.endColor` | Colour |
| `gradient.mode` | `linear` \| `radial` |
| `gradient.linear.angle` | `-270`–`270` |
| `gradient.radial.x`, `gradient.radial.y` | `0`–`180` |
| `image.url` | External URL |
| `image.background` | Colour |
| `image.brightness`, `image.contrast` | `-100`–`100` |
| `image.transparency` | `0`–`100` |
| `image.flip` | Boolean |
| `image.fitType` | `1`–`3` |
| `font.color` | Colour |
| `font.family` | Letters, digits, spaces, apostrophes, hyphens; max 50 |
| `font.size` | `7`–`24` |
| `font.style` | `plain` \| `bold` \| `italic` |
| `card.background` | Colour |
| `card.opacity` | `0`–`1` decimal, e.g. `0.85` |
| `card.blur` | `0`–`50` |
| `card.radius` | `0`–`20` |
| `card.margin` | `0`–`10` |
| `card.shadow` | `1`–`3` |
| `card.paletteType` | `1`–`6` |
| `card.border.color` | Colour |
| `card.border.width` | `0`–`5` |
| `card.title.background` | Colour |
| `card.title.border.color` | Colour |
| `card.title.border.width` | `0`–`5` |
| `card.title.font.{color,family,size,style}` | As `font.*` |
| `card.desc.font.{color,family,size,style}` | As `font.*` |
| `chartEffect.apply` | `1` \| `2` — **mandatory** when `chartEffect` is present |
| `chartEffect.type` | `1`–`3` — forbidden when `apply` is `1` (**7513**), required when `apply` is `2` (**7514**) |

> **Colour format.** Only `#RRGGBB` or `#RGB` is accepted (`^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$`).
> 8-digit hex, `rgb()` and named colours are rejected with **8509**. A non-string colour value is
> likewise rejected with **8509**.

> **Border widths are not per-edge.** A single `card.border.width` (or `card.title.border.width`) is
> written to the left, right, top and bottom edges simultaneously.

> **`palette` is accepted but unsupported.** `themes.palette.*` passes schema validation and is written
> to storage, but the conditional validation for it is disabled in the current build. Do not depend on
> it.

### Sample Requests

**Case 1 — Minimal dashboard with one report**

```http
POST /restapi/v2/workspaces/466206000000071000/dashboards HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"displayName":"Sales Overview","layout":"{\"1\":{\"type\":\"VIEW\",\"viewName\":\"Sales Chart\",\"width\":80,\"height\":20,\"left\":0,\"top\":0}}"}
```

**Case 2 — Filter panel, a heading and two side-by-side reports**

```http
POST /restapi/v2/workspaces/466206000000071000/dashboards HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
  "displayName": "Regional Performance",
  "description": "Quarterly regional roll-up",
  "layout": "{
     \"1\": {\"type\":\"USERFILTERS\",\"width\":80,\"height\":3,\"left\":0,\"top\":0},
     \"2\": {\"type\":\"TITLE\",\"width\":80,\"height\":3,\"left\":0,\"top\":3,\"content\":\"<b>Q3 Performance</b>\"},
     \"3\": {\"type\":\"VIEW\",\"width\":40,\"height\":20,\"left\":0,\"top\":6,\"viewName\":\"Sales by Region\"},
     \"4\": {\"type\":\"VIEW\",\"width\":40,\"height\":20,\"left\":40,\"top\":6,\"viewName\":\"Margin by Region\"}
  }",
  "settings": {"allowDrillDown":"true","fitToWidth":"true","reportAsFilter":"true","layoutType":"web"},
  "themes": {
    "layoutType": 2,
    "type": "solid",
    "solid": {"background": "#333542"},
    "card": {"background":"#3E3F4D","border":{"color":"#6F738E","width":2},"title":{"border":{"color":"#6F738E"}}}
  }
}
```

**Case 3 — Let the server lay the cards out in two columns**

Only the view names matter here; the geometry is replaced.

```http
POST /restapi/v2/workspaces/466206000000071000/dashboards HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"displayName":"Auto Layout","layoutType":2,"layout":"{\"1\":{\"type\":\"VIEW\",\"viewName\":\"Sales Chart\",\"width\":40,\"height\":20,\"left\":0,\"top\":0},\"2\":{\"type\":\"VIEW\",\"viewName\":\"Margin Chart\",\"width\":40,\"height\":20,\"left\":40,\"top\":0}}"}
```

**Case 4 — Gradient theme**

```
CONFIG={
  "displayName": "Gradient Demo",
  "layout": "{\"1\":{\"type\":\"VIEW\",\"viewName\":\"Sales Chart\",\"width\":80,\"height\":20,\"left\":0,\"top\":0}}",
  "themes": {
    "type": "gradient",
    "gradient": {"background":"#1B1C28","startColor":"#2A2D3E","endColor":"#13141C","mode":"linear","linear":{"angle":135}},
    "card": {"background":"#22242F","opacity":0.9,"blur":4}
  }
}
```

### Sample Response

**HTTP 200 OK**

```json
{
  "status": "success",
  "summary": "Create dashboard",
  "data": {
    "dashboardId": "466206000000106002",
    "displayName": "Sales Overview"
  }
}
```

### Error Codes

| Error-Code | Reason | Solution |
|-----------:|--------|----------|
| 7487 | `displayName` or `layout` is absent, `null` or empty. | Supply both. Remember `layout` is a JSON-encoded **string**. |
| 7111 | A dashboard with this `displayName` already exists in the workspace. | Choose a different name. |
| 7507 | `displayName` exceeds 100 characters, or `description` exceeds 250. | Shorten the value. |
| 7510 | `layout` is not parseable JSON, or a `themes` sub-object is `null`. | Validate the JSON you embed in the `layout` string; never send `null` for `card`, `solid`, `gradient` or `image`. |
| 7479 | A card is missing one or more of `type`, `width`, `height`, `left`, `top`. | Add the missing positional fields. |
| 7486 | A positional field has the wrong JSON type. | `width`, `height`, `left`, `top` must be integers; `type` must be a string. |
| 7485 | Unrecognised card `type`. | Use one of the eight values in [Card types](#card-types). |
| 7480 | Negative offset, `width`/`height` of 1 or less, or `left + width > 80`. | Keep every card inside the 80-unit grid. |
| 7512 | A card is smaller than the minimum for its type. | See the min height/width columns in [Card types](#card-types). |
| 7482 | Two cards overlap. | Reposition so no two rectangles intersect. |
| 7483 | A `HTML`, `TITLE`, `PARA`, `IMAGE` or `EMBED` card has absent, `null` or empty `content`. | Supply a non-empty `content` string. |
| 7484 | More than 100 cards in the layout. | Split the dashboard. |
| 8027 | One or more `VIEW` cards name a view that does not exist in this workspace, or `viewName` is absent / `null` / non-string. | Check the view display names. Matching is case-insensitive but the view must exist. |
| 7481 | The referenced view exists but the caller cannot read it. | Have the view shared with the caller, or remove the card. |
| 9001 | Every card in the layout is a `USERFILTERS` card. | Add at least one content-bearing card. |
| 7491 | The sub-object required by `themes.type` is missing, or `card` is absent. | Add the required sub-object. |
| 7492 | A required field inside the type sub-object or inside `card` is missing. | See the required-fields table in [Themes](#themes). |
| 7493 | A sub-object belonging to a different theme type is present, or a forbidden key accompanies `default`. | Remove the conflicting key. |
| 7513 | `chartEffect.type` supplied while `chartEffect.apply` is `1`. | Remove `type`, or set `apply` to `2`. |
| 7514 | `chartEffect.apply` is `2` but `chartEffect.type` is absent. | Supply `chartEffect.type`. |
| 7488 | A `settings` or `themes` key has an empty or `null` value, or an unrecognised key reached the server. | Remove the key or give it a valid value. |
| 8509 | An enumerated or pattern-constrained value does not match — a malformed colour, an out-of-range number, `layoutType` outside 1–4, a non-string colour. | Check the ranges in [Themes](#themes) and [Settings](#settings). |
| 8517 | A value has the wrong JSON data type for its schema declaration. | Match the declared types. |
| 8534 | A theme sub-object was supplied as an array, or `CONFIG` is malformed JSON. | Use `{}` for objects. |
| 8504 | The `CONFIG` parameter is missing from the request body. | Send `CONFIG` as a form-encoded parameter. |
| 8542 | An unknown key is present in `CONFIG`. | Only `displayName`, `description`, `layout`, `themes`, `settings`, `layoutType` are accepted. |
| 7103 | Workspace not found. | Verify `<workspace-id>`. |
| 7301 | The caller lacks Create Report permission on the workspace, or is calling from a white-label domain that is not mapped to this workspace. | Grant the permission, or call the standard data-centre domain. |
| 7309 | `Authorization` header absent. | Send `Authorization: Zoho-oauthtoken <token>`. |
| 8535 | Invalid or expired OAuth token. | Refresh the token with scope `ZohoAnalytics.modeling.create`. |

---

## 2. Read Dashboard Metadata

Returns the stored configuration of a dashboard. This is the read half of the read-modify-write cycle
that [Update Dashboard](#3-update-dashboard) requires.

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/dashboards/<dashboard-id>/metadata` |
| **OAuth Scope** | `ZohoAnalytics.modeling.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** |
| **Permission Required** | **Read Only** or higher on the dashboard. Owners, Workspace Admins, Organization Admins, shared users and group members with read access all qualify. |
| **Custom domain** | Permitted when the workspace is mapped to the calling domain. |
| **Throttle** | 20 requests per minute per user. |

### CONFIG Parameter

Optional. Sent as a query parameter.

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `include` | String | No | `all` | Which section to return. Exactly one of `all`, `layout`, `themes`, `settings`. Comma-separated lists are **not** accepted. |

When `include` is `all`, the response carries `objId`, `displayName`, `description` and all three
sections. When `include` names a single section, only that section is returned — the identity fields are
omitted.

### Behaviour

- The returned `layout` is renumbered from `"1"` in storage order; the card IDs you supplied on create
  are not preserved.
- `VIEW` cards are returned with `viewName` resolved to the view's current display name.
- `DELETED` cards carry a `respContent` message explaining whether the underlying view was deleted or
  permanently removed.
- A tabbed dashboard raises **7511** rather than returning a body.
- The response is **not** a valid Update payload. See
  [Round-tripping a dashboard](#round-tripping-a-dashboard) for the transformations required and the
  list of attributes that are never returned.

### Sample Requests

**Case 1 — Full configuration**

```http
GET /restapi/v2/workspaces/466206000000071000/dashboards/466206000000106002/metadata HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Layout only**

```http
GET /restapi/v2/workspaces/466206000000071000/dashboards/466206000000106002/metadata?CONFIG={"include":"layout"} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Sample Responses

**Case 1 — `include=all` (default)**

```json
{
  "status": "success",
  "summary": "Get dashboard metadata",
  "data": {
    "dashboardConfig": {
      "objId": "466206000000106002",
      "displayName": "Regional Performance",
      "description": "Quarterly regional roll-up",
      "themes": {
        "default": "true",
        "layoutType": "2"
      },
      "settings": {
        "allowDrillDown": "true",
        "hideColumnOptions": "true",
        "smartAlignCharts": "true",
        "enableSortMenu": "true",
        "reportAsFilter": "false",
        "showContextualOptions": "true",
        "allowVUD": "true",
        "allowInsights": "true",
        "allowEmbedInsights": "true",
        "fitToWidth": "true",
        "enableGlobalUF": "false",
        "applyImmediateUF": "true",
        "timeSlicer": "false",
        "layoutType": "web",
        "layoutWidth": "1279",
        "allowExport": {
          "csv": "true", "excel": "true", "html": "true",
          "image": "true", "pdf": "true", "zohoSheet": "true"
        }
      },
      "layout": {
        "1": { "type": "USERFILTERS", "width": 80, "height": 3, "left": 0, "top": 0 },
        "2": { "type": "TITLE", "width": 80, "height": 3, "left": 0, "top": 3, "content": "<b>Q3 Performance</b>" },
        "3": { "type": "VIEW", "width": 40, "height": 20, "left": 0, "top": 6, "viewName": "Sales by Region" },
        "4": { "type": "VIEW", "width": 40, "height": 20, "left": 40, "top": 6, "viewName": "Margin by Region" }
      }
    }
  }
}
```

**Case 2 — `include=layout`**

```json
{
  "status": "success",
  "summary": "Get dashboard metadata",
  "data": {
    "dashboardConfig": {
      "layout": {
        "1": { "type": "USERFILTERS", "width": 80, "height": 3, "left": 0, "top": 0 },
        "2": { "type": "VIEW", "width": 80, "height": 20, "left": 0, "top": 3, "viewName": "Sales Chart" }
      }
    }
  }
}
```

### Error Codes

| Error-Code | Reason | Solution |
|-----------:|--------|----------|
| 7103 | Workspace not found. | Verify `<workspace-id>`. |
| 7104 | The dashboard does not exist, or `<dashboard-id>` is `0`. | Verify `<dashboard-id>`. |
| 7319 | The dashboard exists but belongs to a different workspace. | Make `<workspace-id>` and `<dashboard-id>` consistent. |
| 7511 | The target is a tabbed dashboard. | Tabbed dashboards cannot be read through this API. |
| 7018 | Malformed URL — the ID is not a valid numeric path segment. | Use the numeric dashboard ID only. |
| 8509 | `include` is not one of `all`, `layout`, `themes`, `settings`. | Use a single valid section name. |
| 7301 | The caller lacks read permission on the dashboard, or is on an unmapped white-label domain. | Share the dashboard with the caller. |
| 7309 | `Authorization` header absent. | Send the OAuth header. |
| 8535 | Invalid or expired OAuth token. | Refresh with scope `ZohoAnalytics.modeling.read`. |

---

## 3. Update Dashboard

Replaces one or more sections of an existing dashboard.

| Attribute | Value |
|-----------|-------|
| **Method** | PUT |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/dashboards/<dashboard-id>` |
| **OAuth Scope** | `ZohoAnalytics.modeling.update` |
| **ZANALYTICS-ORGID Header** | **Mandatory** |
| **Content-Type** | `application/x-www-form-urlencoded` |
| **Permission Required** | **Design Modify** on the dashboard — the owner, a Workspace Admin, an Organization Admin, or a shared user granted edit rights. |
| **Custom domain** | Permitted when the workspace is mapped to the calling domain. |
| **Throttle** | 10 requests per minute per user; 10-minute lock-out on breach. |

### CONFIG Parameter

Maximum encoded size 5,000,000 characters. **Only four keys are accepted** — this is the key difference
from Create.

| Field | Type | Mandatory | Description |
|-------|------|-----------|-------------|
| `layout` | String | No | Replaces the entire layout. Same rules and validation as Create. |
| `themes` | JSONObject | No | Replaces the entire theme. Same required-field rules as Create. |
| `settings` | JSONObject | No | Replaces the entire settings block. |
| `layoutType` | Integer | No | 1–4; triggers auto-layout generation for the supplied `layout`. |

### What differs from Create

| Aspect | Create | Update |
|--------|--------|--------|
| `displayName` | Required | **Not accepted** — raises **8542**. A dashboard cannot be renamed through this API. |
| `description` | Optional | **Not accepted** — raises **8542**. |
| `layout` | Required | Optional; omit to leave the layout untouched. |
| `themes` | Optional; omission writes the default theme | Optional; omission leaves the existing theme untouched. |
| `settings` | Optional; omission writes the default settings | Optional; omission leaves the existing settings untouched. |
| Response | 200 with `data.dashboardId` | **204 No Content**, empty body. |

> **Each supplied section is deleted and rewritten.** `DashLayoutDeletion`, `DashThemeDeletion` and
> `DashSettingDeletion` run before the new rows are inserted. There is no field-level patching: a
> `settings` object containing one key leaves the dashboard with exactly one setting stored. Read the
> current configuration first, merge your change into it, then write the whole section back — after
> applying the transformations in [Round-tripping a dashboard](#round-tripping-a-dashboard).

> **Partial layouts fail in confusing ways.** Sending three of a dashboard's six cards does not move
> those three — it replaces the layout with three cards. If the subset happens to violate a rule (for
> example by containing only `USERFILTERS` cards) you will get **9001** or an overlap error rather than
> a clear message.

> The whole update runs inside a single transaction, so a validation failure in any section leaves the
> dashboard untouched.

### Sample Requests

**Case 1 — Change only the theme**

```http
PUT /restapi/v2/workspaces/466206000000071000/dashboards/466206000000106002 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"themes":{"type":"solid","solid":{"background":"#FFFFFF"},"card":{"background":"#F4F5F7"}}}
```

**Case 2 — Replace the layout**

```http
PUT /restapi/v2/workspaces/466206000000071000/dashboards/466206000000106002 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"layout":"{\"1\":{\"type\":\"USERFILTERS\",\"width\":80,\"height\":3,\"left\":0,\"top\":0},\"2\":{\"type\":\"VIEW\",\"viewName\":\"Sales by Region\",\"width\":80,\"height\":25,\"left\":0,\"top\":3}}"}
```

**Case 3 — Reset to the default theme**

```
CONFIG={"themes":{"default":"true"}}
```

### Sample Response

**HTTP 204 No Content** — no response body is returned on success.

```
HTTP/1.1 204 No Content
```

### Error Codes

Update runs the same layout, theme and settings validation as Create, so every code in the
[Create Dashboard error table](#error-codes) can be returned here. The codes specific to Update or with
different triggers are:

| Error-Code | Reason | Solution |
|-----------:|--------|----------|
| 7104 | The dashboard does not exist in this workspace. | Verify `<dashboard-id>`. |
| 7319 | The dashboard belongs to a different workspace. | Make the two path IDs consistent. |
| 7511 | The target is a tabbed dashboard. | Tabbed dashboards cannot be modified through this API. |
| 8542 | `displayName`, `description`, or any other key outside `layout` / `themes` / `settings` / `layoutType` is present in `CONFIG`. | Remove the key. Renaming is not supported here. |
| 7301 | The caller lacks Design Modify permission on the dashboard. | Grant edit access. |
| 8535 | Invalid or expired OAuth token. | Refresh with scope `ZohoAnalytics.modeling.update`. |

---

> The three listing APIs below are **user-scoped**: they return dashboards across every organization the caller belongs to and take no `ZANALYTICS-ORGID` header. They are kept here so that every Dashboard API is documented in one place.

## 4. Get All Dashboards

| Attribute | Value |
|-----------|-------|
| **API NAME** | Get All Dashboards |
| **URL** | `GET https://<ZohoAnalytics_Server_URI>/restapi/v2/dashboards` |
| **METHOD** | GET |
| **DESCRIPTION** | Returns all dashboards accessible to the authenticated user — both dashboards owned by the user and dashboards shared with the user — across all organizations and workspaces. The response groups results into two separate lists: `ownedViews` and `sharedViews`. |
| **OAUTHSCOPE** | `ZohoAnalytics.metadata.read` |
| **PERMISSION REQUIRED** | The authenticated user must be any active **Zoho Analytics user**. |

> This API has no request body parameters. All context is derived from the OAuth token.

### Sample Requests

**Case 1: Retrieve all dashboards for the authenticated user**

```http
GET /restapi/v2/dashboards HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

**Case 2: Same request from a different data center (EU)**

```http
GET /restapi/v2/dashboards HTTP/1.1
Host: analyticsapi.zoho.eu
Authorization: Zoho-oauthtoken 1000.aaaaaa.bbbbbb
```

### Sample Responses

**Case 1 – Success: user has both owned and shared dashboards**

```http
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8

{
  "status": "success",
  "summary": "Get all dashboards",
  "data": {
    "ownedViews": [
      {
        "viewId": "466206000000105001",
        "viewName": "Executive Sales Dashboard",
        "viewDesc": "High-level sales KPIs for the executive team",
        "viewType": "Dashboard",
        "parentViewId": "",
        "folderId": "466206000000071005",
        "createdTime": "1719820800000",
        "createdBy": "alice@example.com",
        "lastModifiedTime": "1722499200000",
        "lastModifiedBy": "alice@example.com",
        "isFavorite": true,
        "sharedBy": "",
        "workspaceId": "466206000000071000",
        "orgId": "700000123456"
      },
      {
        "viewId": "466206000000108003",
        "viewName": "Marketing Campaign Overview",
        "viewDesc": "",
        "viewType": "Dashboard",
        "parentViewId": "",
        "folderId": "466206000000071000",
        "createdTime": "1720080000000",
        "createdBy": "alice@example.com",
        "lastModifiedTime": "1720080000000",
        "lastModifiedBy": "alice@example.com",
        "isFavorite": false,
        "sharedBy": "",
        "workspaceId": "466206000000071000",
        "orgId": "700000123456"
      }
    ],
    "sharedViews": [
      {
        "viewId": "466206000000200010",
        "viewName": "Finance Overview",
        "viewDesc": "Finance team quarterly dashboard",
        "viewType": "Dashboard",
        "parentViewId": "",
        "folderId": "466206000000190001",
        "createdTime": "1718640000000",
        "createdBy": "bob@example.com",
        "lastModifiedTime": "1721001600000",
        "lastModifiedBy": "bob@example.com",
        "isFavorite": false,
        "sharedBy": "bob@example.com",
        "workspaceId": "466206000000190000",
        "orgId": "700000123456"
      }
    ]
  }
}
```

**Case 2 – Success: user has only owned dashboards (empty shared list)**

```json
{
  "status": "success",
  "summary": "Get all dashboards",
  "data": {
    "ownedViews": [
      {
        "viewId": "466206000000105001",
        "viewName": "Executive Sales Dashboard",
        "viewDesc": "High-level sales KPIs",
        "viewType": "Dashboard",
        "parentViewId": "",
        "folderId": "466206000000071005",
        "createdTime": "1719820800000",
        "createdBy": "alice@example.com",
        "lastModifiedTime": "1722499200000",
        "lastModifiedBy": "alice@example.com",
        "isFavorite": true,
        "sharedBy": "",
        "workspaceId": "466206000000071000",
        "orgId": "700000123456"
      }
    ],
    "sharedViews": []
  }
}
```

**Case 3 – Success: user has no dashboards at all**

```json
{
  "status": "success",
  "summary": "Get all dashboards",
  "data": {
    "ownedViews": [],
    "sharedViews": []
  }
}
```

### Response Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success` or `failure`. |
| `summary` | string | Always `"Get all dashboards"` on success. |
| `data.ownedViews` | JSONArray | List of dashboards owned by the authenticated user. |
| `data.sharedViews` | JSONArray | List of dashboards shared with the authenticated user. |

Each item in `ownedViews` and `sharedViews` has the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `viewId` | string | Unique ID of the dashboard. |
| `viewName` | string | Display name of the dashboard. |
| `viewDesc` | string | Description of the dashboard. Empty string if none. |
| `viewType` | string | Always `"Dashboard"` for dashboard entries. |
| `parentViewId` | string | ID of the parent view, if any. Empty string if none. |
| `folderId` | string | ID of the folder containing the dashboard. |
| `createdTime` | string | Dashboard creation timestamp in epoch milliseconds. |
| `createdBy` | string | Email address of the dashboard owner/creator. |
| `lastModifiedTime` | string | Last modification timestamp in epoch milliseconds. |
| `lastModifiedBy` | string | Email address of the user who last modified the dashboard. |
| `isFavorite` | boolean | `true` if the dashboard is marked as a favorite by the requesting user. |
| `sharedBy` | string | Email of the user who shared this dashboard. Present in shared entries; empty string in owned entries. |
| `workspaceId` | string | ID of the workspace containing the dashboard. |
| `orgId` | string | ID of the organization the workspace belongs to. |

### Error Codes

| Error-Code | Reason | Solution |
|-----------:|--------|----------|
| 7301 | User does not have permission to retrieve dashboards. | Ensure the request uses a valid OAuth token for an active Zoho Analytics user. |
| 8535 | Invalid OAuth token. | Provide a valid, non-expired OAuth token in the `Authorization` header. |

---

## 5. Get Owned Dashboards

| Attribute | Value |
|-----------|-------|
| **API NAME** | Get Owned Dashboards |
| **URL** | `GET https://<ZohoAnalytics_Server_URI>/restapi/v2/dashboards/owned` |
| **METHOD** | GET |
| **DESCRIPTION** | Returns the list of dashboards owned by the authenticated user across all organizations. Only accessible to Account Admin users. The response contains a single `views` array listing all owned dashboards. |
| **OAUTHSCOPE** | `ZohoAnalytics.metadata.read` |
| **PERMISSION REQUIRED** | The authenticated user must be an **Account Admin**. |

> This API has no request body parameters. All context is derived from the OAuth token.

### Sample Requests

**Case 1: Account Admin retrieves all owned dashboards**

```http
GET /restapi/v2/dashboards/owned HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

**Case 2: Same request from the India data center**

```http
GET /restapi/v2/dashboards/owned HTTP/1.1
Host: analyticsapi.zoho.in
Authorization: Zoho-oauthtoken 1000.cccccc.dddddd
```

### Sample Responses

**Case 1 – Success: Account Admin owns multiple dashboards across workspaces**

```http
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8

{
  "status": "success",
  "summary": "Get owned dashboards",
  "data": {
    "views": [
      {
        "viewId": "466206000000105001",
        "viewName": "Executive Sales Dashboard",
        "viewDesc": "High-level sales KPIs for the executive team",
        "viewType": "Dashboard",
        "parentViewId": "",
        "folderId": "466206000000071005",
        "createdTime": "1719820800000",
        "createdBy": "admin@example.com",
        "lastModifiedTime": "1722499200000",
        "lastModifiedBy": "admin@example.com",
        "isFavorite": true,
        "sharedBy": "",
        "workspaceId": "466206000000071000",
        "orgId": "700000123456"
      },
      {
        "viewId": "466206000000305020",
        "viewName": "HR Headcount Overview",
        "viewDesc": "",
        "viewType": "Dashboard",
        "parentViewId": "",
        "folderId": "466206000000300000",
        "createdTime": "1716912000000",
        "createdBy": "admin@example.com",
        "lastModifiedTime": "1720339200000",
        "lastModifiedBy": "admin@example.com",
        "isFavorite": false,
        "sharedBy": "",
        "workspaceId": "466206000000300000",
        "orgId": "700000998877"
      }
    ]
  }
}
```

**Case 2 – Success: Account Admin owns dashboards in multiple organizations**

```json
{
  "status": "success",
  "summary": "Get owned dashboards",
  "data": {
    "views": [
      {
        "viewId": "466206000000105001",
        "viewName": "Sales Performance Dashboard",
        "viewDesc": "Monthly and quarterly sales metrics",
        "viewType": "Dashboard",
        "parentViewId": "",
        "folderId": "466206000000071000",
        "createdTime": "1715990400000",
        "createdBy": "admin@example.com",
        "lastModifiedTime": "1722499200000",
        "lastModifiedBy": "admin@example.com",
        "isFavorite": false,
        "sharedBy": "",
        "workspaceId": "466206000000071000",
        "orgId": "700000123456"
      }
    ]
  }
}
```

**Case 3 – Success: Account Admin has no owned dashboards**

```json
{
  "status": "success",
  "summary": "Get owned dashboards",
  "data": {
    "views": []
  }
}
```

### Response Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success` or `failure`. |
| `summary` | string | Always `"Get owned dashboards"` on success. |
| `data.views` | JSONArray | List of dashboards owned by the authenticated Account Admin user. Each item follows the same field structure as in [Get All Dashboards](#4-get-all-dashboards) (see [Response Field Reference — per-dashboard item](#4-get-all-dashboards)). |

### Error Codes

| Error-Code | Reason | Solution |
|-----------:|--------|----------|
| 7301 | User does not have permission to retrieve owned dashboards. | Ensure the authenticated user is an **Account Admin**. |
| 8535 | Invalid OAuth token. | Provide a valid, non-expired OAuth token in the `Authorization` header. |

---

## 6. Get Shared Dashboards

| Attribute | Value |
|-----------|-------|
| **API NAME** | Get Shared Dashboards |
| **URL** | `GET https://<ZohoAnalytics_Server_URI>/restapi/v2/dashboards/shared` |
| **METHOD** | GET |
| **DESCRIPTION** | Returns all dashboards that have been shared with the authenticated user across all organizations and workspaces. The response contains a single `views` array. Unlike [Get All Dashboards](#4-get-all-dashboards), this endpoint returns only shared dashboards (not owned ones), and it is also available on custom domains. |
| **OAUTHSCOPE** | `ZohoAnalytics.metadata.read` |
| **PERMISSION REQUIRED** | The authenticated user must be any active **Zoho Analytics user**. |

> This API has no request body parameters. All context is derived from the OAuth token.

### Sample Requests

**Case 1: Retrieve all dashboards shared with the authenticated user**

```http
GET /restapi/v2/dashboards/shared HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

**Case 2: Same request on a custom domain**

```http
GET /restapi/v2/dashboards/shared HTTP/1.1
Host: analytics.example.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
```

### Sample Responses

**Case 1 – Success: user has multiple shared dashboards**

```http
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8

{
  "status": "success",
  "summary": "Get shared dashboards",
  "data": {
    "views": [
      {
        "viewId": "466206000000200010",
        "viewName": "Finance Overview",
        "viewDesc": "Finance team quarterly dashboard",
        "viewType": "Dashboard",
        "parentViewId": "",
        "folderId": "466206000000190001",
        "createdTime": "1718640000000",
        "createdBy": "bob@example.com",
        "lastModifiedTime": "1721001600000",
        "lastModifiedBy": "bob@example.com",
        "isFavorite": false,
        "sharedBy": "bob@example.com",
        "workspaceId": "466206000000190000",
        "orgId": "700000123456"
      },
      {
        "viewId": "466206000000410055",
        "viewName": "Supply Chain Dashboard",
        "viewDesc": "Inventory and logistics metrics",
        "viewType": "Dashboard",
        "parentViewId": "",
        "folderId": "466206000000400000",
        "createdTime": "1714780800000",
        "createdBy": "carol@example.com",
        "lastModifiedTime": "1719993600000",
        "lastModifiedBy": "carol@example.com",
        "isFavorite": true,
        "sharedBy": "carol@example.com",
        "workspaceId": "466206000000400000",
        "orgId": "700000998877"
      }
    ]
  }
}
```

**Case 2 – Success: user has one shared dashboard marked as favorite**

```json
{
  "status": "success",
  "summary": "Get shared dashboards",
  "data": {
    "views": [
      {
        "viewId": "466206000000200010",
        "viewName": "Regional Sales Tracker",
        "viewDesc": "Sales performance by region",
        "viewType": "Dashboard",
        "parentViewId": "",
        "folderId": "466206000000190000",
        "createdTime": "1720512000000",
        "createdBy": "dave@example.com",
        "lastModifiedTime": "1722067200000",
        "lastModifiedBy": "dave@example.com",
        "isFavorite": true,
        "sharedBy": "dave@example.com",
        "workspaceId": "466206000000190000",
        "orgId": "700000123456"
      }
    ]
  }
}
```

**Case 3 – Success: no dashboards have been shared with the user**

```json
{
  "status": "success",
  "summary": "Get shared dashboards",
  "data": {
    "views": []
  }
}
```

### Response Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success` or `failure`. |
| `summary` | string | Always `"Get shared dashboards"` on success. |
| `data.views` | JSONArray | List of dashboards shared with the authenticated user. Each item follows the same field structure as in [Get All Dashboards](#4-get-all-dashboards) (see [Response Field Reference — per-dashboard item](#4-get-all-dashboards)). The `sharedBy` field is always populated for shared dashboards. |

### Error Codes

| Error-Code | Reason | Solution |
|-----------:|--------|----------|
| 7301 | User does not have permission to retrieve shared dashboards. | Ensure the request uses a valid OAuth token for an active Zoho Analytics user. |
| 8535 | Invalid OAuth token. | Provide a valid, non-expired OAuth token in the `Authorization` header. |

---

---

## Appendix A – Common HTTP Headers

| Header | Value | Required | Notes |
|--------|-------|----------|-------|
| `Authorization` | `Zoho-oauthtoken <oauth-token>` | **Mandatory** | OAuth 2.0 access token of the calling user. |
| `ZANALYTICS-ORGID` | Organization ID | **Mandatory** for the workspace-scoped APIs (1–3) | Organization ID that owns the workspace. Not used by the three listing APIs (4–6). |
| `Content-Type` | `application/x-www-form-urlencoded` | POST / PUT | `CONFIG` is a form-encoded body parameter on Create and Update. On Read it is a query parameter. |

---

## Appendix B – OAuth Scope Summary

| API | Method | Scope |
|-----|--------|-------|
| Create Dashboard | POST | `ZohoAnalytics.modeling.create` |
| Read Dashboard Metadata | GET | `ZohoAnalytics.modeling.read` |
| Update Dashboard | PUT | `ZohoAnalytics.modeling.update` |
| Get All Dashboards | GET | `ZohoAnalytics.metadata.read` |
| Get Owned Dashboards | GET | `ZohoAnalytics.metadata.read` |
| Get Shared Dashboards | GET | `ZohoAnalytics.metadata.read` |

---

## Appendix C – Card Type Quick Reference

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

## Appendix D – Operational Notes and Failure Cases

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
