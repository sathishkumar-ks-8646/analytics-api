---
type: API Group
title: Slideshow Management
description: "APIs for creating, updating, deleting, and listing slideshows and their URLs."
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - slideshow-management
  - api-group
api:
  domain: share-and-publish
  group: slideshow-management
  endpoint_count: 6
  endpoints:
    - operation_id: getSlideshows
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/slides"
      doc: "/domains/share-and-publish/slideshow-management/get-slideshows.md"
    - operation_id: getSlideshowUrl
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}/publish"
      doc: "/domains/share-and-publish/slideshow-management/get-slideshow-url.md"
    - operation_id: getSlideshowDetails
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}"
      doc: "/domains/share-and-publish/slideshow-management/get-slideshow-details.md"
    - operation_id: createSlideshow
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/slides"
      doc: "/domains/share-and-publish/slideshow-management/create-slideshow.md"
    - operation_id: updateSlideshow
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}"
      doc: "/domains/share-and-publish/slideshow-management/update-slideshow.md"
    - operation_id: deleteSlideshow
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}"
      doc: "/domains/share-and-publish/slideshow-management/delete-slideshow.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/share-publish-grouped-api.json"
    title: OpenAPI 3 specification - share-publish-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

This document covers the V2 **Slideshow** REST APIs of Zoho Analytics — the APIs that create, list, inspect, update, and delete slideshows within a workspace, and that build the URL through which a slideshow is presented.

APIs for creating, updating, deleting, and listing slideshows and their URLs.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Slide List](get-slideshows.md) | GET | `/restapi/v2/workspaces/{workspace-id}/slides` | `getSlideshows` | `ZohoAnalytics.embed.read` | 200 |
| [Get Slide URL](get-slideshow-url.md) | GET | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}/publish` | `getSlideshowUrl` | `ZohoAnalytics.embed.read` | 200 |
| [Get Slide Info](get-slideshow-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}` | `getSlideshowDetails` | `ZohoAnalytics.embed.read` | 200 |
| [Create Slide Show](create-slideshow.md) | POST | `/restapi/v2/workspaces/{workspace-id}/slides` | `createSlideshow` | `ZohoAnalytics.embed.create` | 200 |
| [Update Slide Show](update-slideshow.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}` | `updateSlideshow` | `ZohoAnalytics.embed.update` | 204 |
| [Delete Slide Show](delete-slideshow.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}` | `deleteSlideshow` | `ZohoAnalytics.embed.delete` | 204 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is a "Slideshow" in Zoho Analytics?

A **slideshow** is a named, ordered collection of views (charts, pivots, summaries, dashboards, tables, query tables) belonging to a single workspace, presented one after another on a stand-alone page at `https://<analytics-domain>/ZDBSlideshow.cc?SLIDEID=<slide-id>&SLIDEKEY=<slide-key>&...`.

Two identifiers matter:

| Identifier | Purpose |
|------------|---------|
| **`slideId`** | The permanent numeric ID of the slideshow. Used in every URL path of these APIs. Safe to store and share internally. |
| **`slideKey`** | A 32-character hexadecimal secret embedded in the presentation URL. It is what allows the slideshow page to be opened. Rotating it (`regenerateSlideKey`) instantly invalidates every URL previously handed out. |

Each slideshow also carries an **access type** that decides whether a viewer must be signed in to Zoho Analytics — see [`accessType` Values](overview.md#accesstype-values). A slideshow set to "access without login" behaves like a private link and is therefore subject to the same plan and security-control gating as private links.

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`). All six APIs use the **`embed`** scope family.
> - All six APIs are **workspace-scoped** (`/workspaces/<workspace-id>/slides...`) and require the `ZANALYTICS-ORGID` header.
> - The API host (`ZohoAnalytics_Server_URI`, e.g. `analyticsapi.zoho.com`, `analyticsapi.zoho.eu`) is **not** the host that appears in the returned `slideUrl`. The returned URL always points at the Zoho Analytics **application** domain (e.g. `analytics.zoho.com`) or, for Client Portal / White Label workspaces, at the workspace's portal domain.
> - All six APIs are available in **Client Portal / White Label** contexts.
> - The three mutating APIs (Create Slide Show, Update Slide Show, Delete Slide Show) additionally require the calling user's **primary email to be verified** — otherwise error [`7565`](../../../foundations/error-codes.md#error-7565).
> - Slideshows are a **plan-gated feature**. Every API in this family — including the read-only ones — runs the plan check first and fails with [`6063`](../../../foundations/error-codes.md#error-6063) on plans where slideshows are unavailable.
> - **No API in this family accepts a `criteria` attribute.** Row-level filtering is not part of the slideshow contract; a slideshow presents each view exactly as that view is defined. Filter the underlying views (or use [Update Publish Configurations](../publish/update-publish-configurations.md) for a published view) instead.

---

# `accessType` Values

`accessType` appears both as a CONFIG input ([Create Slide Show](create-slideshow.md), [Update Slide Show](update-slideshow.md)) and as a response field ([Get Slide List](get-slideshows.md), [Get Slide Info](get-slideshow-details.md)). It has exactly two meaningful values:

| Value | Name | Meaning |
|-------|------|---------|
| `0` | Access with login | The default. A viewer opening the slideshow URL must be signed in to Zoho Analytics **and** must already have access to the views in the slideshow. Nothing new is exposed. |
| `1` | Access without login | The slideshow URL renders for anyone who holds it, with no sign-in. This is the private-link equivalent for slideshows, and it is therefore gated by the plan's private-link entitlement (`6054`/`6056`) and by the organization's private-link security control (`8088`). |

> **Only `1` selects "without login".** The server tests `accessType == 1` and treats every other integer — including values outside the documented set — as `0` (access with login). No error is raised for an out-of-range value; it silently means "with login". Send only `0` or `1`.

---

# API-Specific Notes and Behaviours

## Get Slide List

- **The entry point for the whole family.** Every other slideshow API needs a `<slide-id>`, and this is the only way to discover one. Treat it as the first call in any slideshow workflow.
- **Unfiltered and unpaged by design.** The response always contains every slideshow in the workspace. There is no query parameter for search, sort, or paging — do that client-side on `slideName` / `accessType`.
- **Withholds the secret deliberately.** `slideKey` is excluded so a broad listing cannot leak presentation URLs. That makes this the safe API to expose to a listing UI; [Get Slide Info](get-slideshow-details.md) is the one that needs tighter access control.
- **`accessType` shape differs from the legacy client APIs.** V2 returns the integers `0`/`1`; the older non-V2 APIs return the strings `"withLogin"`/`"withoutLogin"` for the same field. Do not write code that accepts either without normalising.
- **A read that can fail on plan.** Because the slideshow entitlement check runs before the list is built, [`6063`](../../../foundations/error-codes.md#error-6063) is a realistic failure mode even for this read-only call — handle it rather than assuming reads always succeed.
- **Dependency chain:** [Get Workspace List](../../workspace-management/workspace-operations/overview.md) → Get Slide List → `<slide-id>` for every other API here.

## Get Slide URL

- **The only stateless API in the family.** It reads the slideshow and returns a decorated URL; nothing is written. Two consumers can hold two differently configured URLs for the same slideshow at the same time, which makes it safe to call per-consumer rather than per-slideshow.
- **Rendering options live here, not on the slideshow.** There is no stored presentation configuration for a slideshow (contrast [Update Publish Configurations](../publish/update-publish-configurations.md) for a published view). If a caller needs consistent options, it must send the same CONFIG every time.
- **`autoplay` defaults to `true`.** A bare call returns an auto-advancing URL at 25-second intervals. This is easy to get wrong when porting from documentation that lists the default as `false` — send the flag explicitly if it matters.
- **`slideInterval` is the one hard-validated field.** Outside `10-300` it raises [`8119`](../../../foundations/error-codes.md#error-8119) rather than clamping, and the error message names both the value and the range.
- **`withCustomDomain` can be ignored without telling you.** Non-Organization-Admin callers, or workspaces with no portal domain, get a normal-domain URL and HTTP 200. Inspect the host in `slideUrl` to know which form you received.
- **`domainName` is accepted and dead.** The request template allows the key but the URL builder never reads it. Do not use it to target a portal domain; use `withCustomDomain`, or simply call through the portal host.
- **Dependency chain:** [Get Slide List](get-slideshows.md) → `<slide-id>` → Get Slide URL.

## Get Slide Info

- **The only source of `slideKey` and `viewIds`.** It is therefore both the most useful read in the family and the most sensitive — for an `accessType: 1` slideshow, `slideId` + `slideKey` is all that is needed to view the content with no sign-in. Restrict who may call it accordingly.
- **The mandatory read-before-write step for updates.** Because [Update Slide Show](update-slideshow.md) replaces `viewIds` wholesale, any add/remove/reorder operation has to start here to obtain the current, correctly ordered list.
- **`viewIds` order carries meaning.** It is presentation order, not sort order. Round-tripping it through an unordered collection will silently reshuffle the slideshow.
- **Workspace-level permission only.** The call does not verify that the caller can read each view listed in `viewIds`, so the response can name views the caller cannot open individually.
- **Error precedence matters when debugging.** [`7351`](../../../foundations/error-codes.md#error-7351) (wrong workspace / no such slideshow) is raised before the slide-details lookup, so [`7396`](../../../foundations/error-codes.md#error-7396) indicates a genuinely inconsistent record rather than a bad ID.
- **Dependency chain:** [Get Slide List](get-slideshows.md) → Get Slide Info → [Get View Details](../../views-management/view-operations/get-view-details.md) per `viewIds` entry.

## Create Slide Show

- **Order of `viewIds` is the product.** A slideshow is fundamentally an ordered list; the array as sent is the sequence viewers see. There is no separate reorder API — reordering means resending the full list through [Update Slide Show](update-slideshow.md).
- **Names are a uniqueness constraint, not a label.** A duplicate `slideName` is a hard failure ([`7196`](../../../foundations/error-codes.md#error-7196)), never an implicit update. Combined with the restrictive character set (letters, digits, whitespace and non-Basic-Latin only — no `-`, `_`, `:`, `/`, `&`, `.`), name generation is the most common source of [`8080`](../../../foundations/error-codes.md#error-8080)/[`7196`](../../../foundations/error-codes.md#error-7196) on this API.
- **`accessType: 1` changes the risk profile of the call.** It turns the slideshow into a login-free link, which is why it pulls in the private-link plan entitlement ([`6054`](../../../foundations/error-codes.md#error-6054)/[`6056`](../../../foundations/error-codes.md#error-6056)) and the organization's private-link security control ([`8088`](../../../foundations/error-codes.md#error-8088)). A create with `accessType: 0` bypasses both and will succeed on plans where `1` fails.
- **Workspace membership is checked; per-view readability is not.** All `viewIds` must live in `<workspace-id>` ([`7319`](../../../foundations/error-codes.md#error-7319)), but the caller's read access to each view is not re-verified on this path.
- **The returned URL is a convenience with fixed options.** It always carries the defaults; there is no way to influence it from this API. Call [Get Slide URL](get-slideshow-url.md) when the presentation options matter.
- **Dependency chain:** [Get View List](../../views-management/view-operations/get-views.md) → `viewIds` → Create Slide Show → `slideId` → [Get Slide URL](get-slideshow-url.md).

## Update Slide Show

- **204 No Content, no body.** Verified against the implementation and the recorded request samples. Never parse a JSON success body, and never expect the rotated `slideUrl` back — fetch it from [Get Slide URL](get-slideshow-url.md).
- **Genuinely partial, unlike the publish-config API.** Omitted attributes retain their values, so a minimal CONFIG is safe here. This is the opposite of [Update Publish Configurations](../publish/update-publish-configurations.md), which resets every omitted field — do not carry a read-merge-write habit from one API to the other assuming it is required.
- **`viewIds` is the one field that *is* a full replace.** It swaps the entire ordered list. "Add a view" therefore means [Get Slide Info](get-slideshow-details.md) → append → resend everything.
- **Partial application is possible on failure.** The four operations are applied in sequence (name, access type, views, key rotation) and each can fail on its own. A request that renames and then hits [`7319`](../../../foundations/error-codes.md#error-7319) on a view ID leaves the rename in place. Always re-read with [Get Slide Info](get-slideshow-details.md) after an error on a multi-field update.
- **Two fields trigger private-link gating.** `accessType: 1` and `regenerateSlideKey: true` both run the plan check ([`6054`](../../../foundations/error-codes.md#error-6054)/[`6056`](../../../foundations/error-codes.md#error-6056)) and the security-control check ([`8088`](../../../foundations/error-codes.md#error-8088)); a rename-only update runs neither.
- **`regenerateSlideKey` is an irreversible revocation.** Every URL distributed earlier dies immediately, with no grace period and no recovery of the old key. Treat it as break-glass, not routine hygiene.
- **Dependency chain:** [Get Slide Info](get-slideshow-details.md) → merge → Update Slide Show → [Get Slide Info](get-slideshow-details.md) / [Get Slide URL](get-slideshow-url.md) to verify.

## Delete Slide Show

- **204 No Content, no body.** Verified against the implementation and the recorded request samples.
- **Destroys the grouping, not the content.** The views keep their own definitions, sharing, and publish state. Nothing in [Sharing](../sharing/overview.md) or [Publish](../publish/overview.md) is affected by deleting a slideshow.
- **No trash, no restore.** Unlike views, a deleted slideshow does not land in the [Trash](../../views-management/trash-management/overview.md) — it is gone, and so is its slide key. Recreating it produces a new `slideId` and a new key, so previously shared URLs cannot be revived.
- **Not idempotent.** A repeat delete fails with [`7351`](../../../foundations/error-codes.md#error-7351). Check existence via [Get Slide List](get-slideshows.md) if a caller may retry.
- **One at a time.** There is no bulk payload; clearing several slideshows means iterating over [Get Slide List](get-slideshows.md).
- **Dependency chain:** [Get Slide List](get-slideshows.md) → Delete Slide Show.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Two of six APIs return 204 with no body** | [Update Slide Show](update-slideshow.md) and [Delete Slide Show](delete-slideshow.md) return HTTP **204 No Content** on success — treat the 2xx status code as the success indicator and never expect or parse a JSON body for these two. The other four return the standard `{"status", "summary", "data"}` envelope with HTTP 200. |
| **Failure responses always carry a body** | Even for the 204 APIs, errors return `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name (e.g. `SECURITY_NOT_PERMITTED`, `SLIDESHOW_NOT_BELONGS_TO_DB`), not a localised sentence. |
| **All IDs are strings** | `slideId` and every entry of `viewIds` are JSON **strings** in every response, even though they are numeric. Parse them as strings or longs — never as native JSON numbers — to avoid precision loss on large IDs. |
| **`accessType` is a native number** | It is the only numeric field in these payloads: the integer `0` or `1`, not a string and not a boolean. Everything else in the responses is a string or an array of strings. |
| **Empty array, never a missing key** | `data.slideshows` is always present in a successful [Get Slide List](get-slideshows.md) response, empty (`[]`) when the workspace has no slideshows. Likewise `slideInfo.viewIds` is always present in [Get Slide Info](get-slideshow-details.md). No key in these responses is ever `null` or conditionally omitted. |
| **The returned URL host is not the API host** | `data.slideUrl` points at the Zoho Analytics **application** domain (e.g. `analytics.zoho.com`) or, in a Client Portal / White Label context, at the workspace's portal domain — never at the `analyticsapi.*` host the request was sent to. Do not construct these URLs client-side from the API host. |
| **`slideUrl` shape is stable and fully populated** | It is always `https://<domain>/ZDBSlideshow.cc?SLIDEID=<id>&SLIDEKEY=<key>&AUTOPLAY=<bool>&INTERVAL=<seconds>&INCLUDETITLE=<bool>&INCLUDEDESC=<bool>&SOCIALWIDGETS=<bool>` — all seven parameters, in that order, whether or not they were supplied. This makes the URL safe to parse, but it also means the key is always embedded. |
| **`slideKey` is a credential** | It appears in `slideInfo.slideKey` and inside every `slideUrl`. For an `accessType: 1` slideshow it grants sign-in-free access to the content, so avoid logging these values and restrict who may call [Get Slide Info](get-slideshow-details.md) and [Get Slide URL](get-slideshow-url.md). |
| **Create echoes only the identifiers** | [Create Slide Show](create-slideshow.md) returns `slideId` and `slideUrl` only — not `slideName`, `accessType`, or `viewIds`. Confirm what was stored with [Get Slide Info](get-slideshow-details.md) rather than assuming the request was applied verbatim. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [6054](../../../foundations/error-codes.md#error-6054) | 400 | The current plan does not allow this publish operation. |
| [6056](../../../foundations/error-codes.md#error-6056) | 400 | A shared user attempted a plan-restricted private-link creation. |
| [6063](../../../foundations/error-codes.md#error-6063) | 400 | The workspace owner's plan does not include the slideshow feature. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7196](../../../foundations/error-codes.md#error-7196) | 404 | Another slideshow in this workspace already uses slideName. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7351](../../../foundations/error-codes.md#error-7351) | 400 | The slideshow does not exist, or belongs to a different workspace. |
| [7396](../../../foundations/error-codes.md#error-7396) | 400 | The slideshow record exists but no slide details could be read for it. |
| [7565](../../../foundations/error-codes.md#error-7565) | 400 | The calling user's primary email address is not verified. |
| [8078](../../../foundations/error-codes.md#error-8078) | 400 | A mandatory attribute was sent with an empty value. The error message names the attribute. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | A mandatory attribute is missing from the configuration. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | CONFIG is not valid JSON, was not URL-encoded correctly, contains an unsupported key, or violates a type or length constraint. |
| [8088](../../../foundations/error-codes.md#error-8088) | 400 | Export is disabled for the organization. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | Invalid value for attribute. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | The view carries a restricted DATAWARNING system tag. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |

# Related

- [Share & Publish](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
