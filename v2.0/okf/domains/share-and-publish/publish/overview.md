---
type: API Group
title: Publish
description: "APIs for making views public, managing private URLs, and updating publish configurations."
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - publish
  - api-group
api:
  domain: share-and-publish
  group: publish
  endpoint_count: 7
  endpoints:
    - operation_id: makeViewsPublic
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/public"
      doc: "/domains/share-and-publish/publish/make-views-public.md"
    - operation_id: removePublicPermission
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/public"
      doc: "/domains/share-and-publish/publish/remove-public-permission.md"
    - operation_id: getPrivateUrl
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink"
      doc: "/domains/share-and-publish/publish/get-private-url.md"
    - operation_id: createPrivateUrl
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink"
      doc: "/domains/share-and-publish/publish/create-private-url.md"
    - operation_id: removePrivateAccess
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink"
      doc: "/domains/share-and-publish/publish/remove-private-access.md"
    - operation_id: getPublishConfigurations
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config"
      doc: "/domains/share-and-publish/publish/get-publish-configurations.md"
    - operation_id: updatePublishConfigurations
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config"
      doc: "/domains/share-and-publish/publish/update-publish-configurations.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/share-publish-grouped-api.json"
    title: OpenAPI 3 specification - share-publish-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

This document covers the V2 **Publish** REST APIs of Zoho Analytics — the APIs that expose a view (table, chart, pivot, summary, dashboard, query table, etc.) outside the normal shared-user model, either as a **Public URL** or as a **Private URL**, and the APIs that read/update the **presentation configuration** of the published page.

APIs for making views public, managing private URLs, and updating publish configurations.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Make View Public](make-views-public.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/public` | `makeViewsPublic` | `ZohoAnalytics.embed.create` | 200 |
| [Remove Public Permission](remove-public-permission.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/public` | `removePublicPermission` | `ZohoAnalytics.embed.delete` | 204 |
| [Get Private URL](get-private-url.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink` | `getPrivateUrl` | `ZohoAnalytics.embed.read` | 200 |
| [Create Private URL](create-private-url.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink` | `createPrivateUrl` | `ZohoAnalytics.embed.update` | 200 |
| [Remove Private Access](remove-private-access.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink` | `removePrivateAccess` | `ZohoAnalytics.embed.delete` | 204 |
| [Get Publish Configurations](get-publish-configurations.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config` | `getPublishConfigurations` | `ZohoAnalytics.embed.read` | 200 |
| [Update Publish Configurations](update-publish-configurations.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config` | `updatePublishConfigurations` | `ZohoAnalytics.embed.update` | 204 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is "Publishing" in Zoho Analytics?

Publishing makes a single view reachable through a stand-alone URL of the form `https://<analytics-domain>/open-view/<view-id>[/<private-key>]`, without adding the visitor as a shared user of the workspace. There are two independent publish channels, and a view can have **both active at the same time**:

| Channel | URL shape | Who can open it | Managed by |
|---------|-----------|-----------------|------------|
| **Public URL** | `https://<analytics-domain>/open-view/<view-id>` | Anyone with the link (or everyone in the organization / business organization, depending on `publicPermLevel`) | [Make View Public](make-views-public.md) / [Remove Public Permission](remove-public-permission.md) |
| **Private URL** | `https://<analytics-domain>/open-view/<view-id>/<private-key>` | Only holders of the secret 32-character key, optionally additionally gated by a password and/or an expiry date | [Get Private URL](get-private-url.md) / [Create Private URL](create-private-url.md) / [Remove Private Access](remove-private-access.md) |

Internally both channels are modelled as a share to a reserved pseudo-user — **`Public Visitor`** (`sharedToZuId: "-20"`) for the public channel and **`Private Link`** (`sharedToZuId: "-30"`) for the private channel. This is why the effect of these APIs is visible in the [Get Shared Details](../sharing/get-shared-details-for-views.md) response, and why the permission set accepted here is a read-only subset of the normal sharing `permissions` object.

Separately, [Get Publish Configurations](get-publish-configurations.md) and [Update Publish Configurations](update-publish-configurations.md) control **how the published page renders** (title, toolbar, search box, size, auto-refresh, legend position, URL-level criteria, Ask Zia, …). That configuration is shared by both channels and by the embed URL.

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`). All seven APIs use the **`embed`** scope family.
> - All seven APIs are **view-scoped** (`/workspaces/<workspace-id>/views/<view-id>/publish/...`) and require the `ZANALYTICS-ORGID` header.
> - The API host (`ZohoAnalytics_Server_URI`, e.g. `analyticsapi.zoho.com`, `analyticsapi.zoho.eu`) is **not** the host that appears in the returned `publicUrl` / `privateUrl`. The returned URL always points at the Zoho Analytics **application** domain (e.g. `analytics.zoho.com`) or, for Client Portal / White Label workspaces, at the workspace's portal domain.
> - All seven APIs are available in **Client Portal / White Label** contexts.
> - The five mutating APIs (Make View Public, Remove Public Permission, Create Private URL, Remove Private Access, Update Publish Configurations) additionally require the calling user's **primary email to be verified** — otherwise error [`7565`](../../../foundations/error-codes.md#error-7565).
> - Publish links are always **read-only**. Row-write permissions (`addRow`, `updateRow`, `deleteRow`, imports) and `share` can never be granted to a public or private link — they are forced to `false` server-side.

---

# API-Specific Notes and Behaviours

## Make View Public

- **Create and update in one endpoint.** Despite the `create` operation type, re-calling this API on an already-public view overwrites the existing public share's permissions, criteria, and column restrictions instead of failing. There is no separate "update public link" API — plan integrations around a single idempotent upsert call.
- **Audience level must be pre-flighted.** `publicPermLevel` `2` and `3` are plan- and organization-gated. Read `publicViewConfig.isOrgPublicAllowed` / `isBussOrgPublicAllowed` from [Get Publish Configurations](get-publish-configurations.md) before requesting them, rather than catching [`7531`](../../../foundations/error-codes.md#error-7531)/[`7500`](../../../foundations/error-codes.md#error-7500) after the fact. In a Client Portal / White Label context the level is silently forced to `1`.
- **Read-only by construction.** The permission array is sanitised to a read-only set server-side; row-write permissions and `share` are dropped silently rather than rejected, so a caller cannot tell from the response that they were ignored. Only the seven fields in [`permissions` Fields](make-views-public.md#permissions-fields) have any effect.
- **`isListed` lives elsewhere.** The public-listing flag is *not* part of this API's CONFIG even though it is a public-channel concern — it is set through [Update Publish Configurations](update-publish-configurations.md).
- **Dependency chain:** [Get View List](../../views-management/view-operations/get-views.md) → [Get Publish Configurations](get-publish-configurations.md) (check allowed audience levels) → Make View Public → verify via [Get Shared Details](../sharing/get-shared-details-for-views.md) (`sharedTo: "Public Visitor"`).

## Remove Public Permission

- **204 No Content, no body.** Verified against the implementation and the recorded request samples. Never parse a JSON success body for this API.
- **Fails on a view with no shares at all.** [`8032`](../../../foundations/error-codes.md#error-8032) `VIEW_NOT_SHARED` is raised when the view has no share records whatsoever — this is a "nothing to remove" condition, not a permission problem. On a view that has other shares but is not public, the call completes silently.
- **Surgical.** Only the `Public Visitor` share record is removed. An active private link, user shares, group shares, and the publish configuration all survive.
- **Dependency chain:** [Get Publish Configurations](get-publish-configurations.md) (confirm `publicViewConfig.publicPermLevel > 0`) → Remove Public Permission.

## Get Private URL

- **Strictly read-only.** This is the only private-link API that will not create or mutate anything — it fails with [`8115`](../../../foundations/error-codes.md#error-8115) rather than lazily generating a key. Use it for retrieving an already-distributed URL, not for provisioning.
- **Returns a secret.** The response embeds the live private key. Treat `data.privateUrl` with the same care as a credential; it is the sole access token for the private channel.
- **Does not reveal the link's guards.** Password state, expiry date, and expiry status are not in this response — a URL returned here may still be password-gated or already expired. Pair with [Get Publish Configurations](get-publish-configurations.md) when presenting link status to a user.
- **Two portal-domain mechanisms, different bars.** `domainName` needs portal-domain admin rights; the legacy `withCustomDomain` additionally needs Organization Admin / Super Admin. Prefer `domainName`.
- **Dependency chain:** [Create Private URL](create-private-url.md) → Get Private URL.

## Create Private URL

- **The only publish API whose write semantics are conditional.** The key is created if absent (or rotated with `regenerateKey`), but `permissions` / `criteria` / `vudColumns` / `drillColumns` are only rewritten when `permissions` is present in the request. Sending `criteria` alone against an existing link is a silent no-op — always include `permissions` when updating.
- **`regenerateKey` is an irreversible revocation.** It invalidates every URL previously handed out for the view, with no grace period and no way to recover the old key. Treat it as a break-glass operation, not a routine refresh.
- **Password handling has two side effects worth knowing.** Setting or changing the password clears all live private-link sessions, and the password can later be read back **in clear text** through [Get Publish Configurations](get-publish-configurations.md) — restrict who may call that API accordingly.
- **`drillThrough` is unavailable on this channel.** Public links accept it; private links force it to `false`. This is the one permission difference between the two channels.
- **Plan-limited resource.** New links consume the organization's private-link allotment ([`6121`](../../../foundations/error-codes.md#error-6121)/[`6122`](../../../foundations/error-codes.md#error-6122) when exhausted). Freeing one requires [Remove Private Access](remove-private-access.md).
- **A sibling PUT endpoint exists but is out of scope here.** `PUT /publish/privatelink` updates an existing link only. This POST endpoint covers both create and update, so most integrations never need the PUT variant.
- **Dependency chain:** [Get View List](../../views-management/view-operations/get-views.md) → Create Private URL → [Get Private URL](get-private-url.md) / [Get Publish Configurations](get-publish-configurations.md).

## Remove Private Access

- **204 No Content, no body.** Verified against the implementation and the recorded request samples.
- **Not idempotent.** A second call fails with [`8115`](../../../foundations/error-codes.md#error-8115) `VIEW_NOT_PUBLISHED_AS_PRIVATE`. Guard repeats with a `privateLinkConfig.isPrivate` check rather than relying on a silent success.
- **Its permission check differs from the other private-link APIs.** The Publish permission is evaluated at the **workspace** level here, whereas [Get Private URL](get-private-url.md) and [Create Private URL](create-private-url.md) evaluate it **per view**. A user with view-scoped Publish permission but no workspace-level grant may therefore be able to create a link and not remove it (a custom-role user with view-level Publish/Make Public permission, or Share permission on the view, is also accepted).
- **Releases a plan allotment.** After removal, a previously blocked [Create Private URL](create-private-url.md) may succeed.
- **Dependency chain:** [Get Publish Configurations](get-publish-configurations.md) (confirm `privateLinkConfig.isPrivate`) → Remove Private Access.

## Get Publish Configurations

- **The pre-flight call for this entire family.** It is the only API that reports, in one round trip, whether the view is public and at what audience level, whether a private link exists and whether it is password-gated or expired, and which audience levels the plan permits. Call it first in almost every publish workflow.
- **Two of its three top-level blocks are permission-conditional.** `publicViewConfig` requires Make Public permission on the workspace; `privateLinkConfig` requires private links to be permitted **and** Publish permission on the workspace. A Free-plan response typically omits `privateLinkConfig` entirely. Never index into these keys without checking for their presence.
- **Returns the private-link password in clear text.** `privateLinkConfig.password` is decrypted for this response (sentinel `"-1"` when unset). This makes the endpoint materially more sensitive than the other read APIs in this document.
- **`publicPermLevel: 0` is output-only.** It signals "not public" on read but is not a legal input to [Make View Public](make-views-public.md); un-publishing goes through [Remove Public Permission](remove-public-permission.md).
- **Its `publishConfig` defaults are not the update API's defaults.** Before any [Update Publish Configurations](update-publish-configurations.md) call, `includeSearchBox` reads as `false` and `includeAskZia` as `true`; the update API's own defaults for those fields are `true` and `false`. Do not treat a read as a safe round-trippable payload without setting both explicitly.
- **Dependency chain:** [Get View List](../../views-management/view-operations/get-views.md) → Get Publish Configurations → the appropriate publish/un-publish API.

## Update Publish Configurations

- **204 No Content, no body.** Verified against the implementation and the recorded request samples.
- **Full replace — the single most important behaviour in this document.** The stored configuration is rebuilt from scratch on every call, so omitted fields are reset to their defaults, not preserved. The safe pattern is always read → merge → write. `isListed` is the only field that is left alone when omitted.
- **Two fields flip on a bare call.** Because of the read-default/write-default asymmetry, calling this API with a minimal body turns `includeSearchBox` on and `includeAskZia` off on a view that had never been updated before. Send both explicitly.
- **`URLCriteria` is a different concept from the channels' `criteria`.** `URLCriteria` is a URL-level filter that applies to the public URL, the private URL, and the embed URL alike; the `criteria` of [Make View Public](make-views-public.md) / [Create Private URL](create-private-url.md) is a per-channel share filter. When both exist, both apply — a common source of "the published page shows fewer rows than I expected".
- **Some fields are view-type-scoped.** `isInteractive` and `legendPosition` are honoured only for chart views (`isInteractive` is forced to `true` for everything else); `includeSearchBox`, `includeDatatypeSymbol`, and `includeShowHideOption` are honoured only for table-type views and tabular reports. Out-of-scope values are accepted and ignored rather than rejected.
- **`autoRefresh` is validated, not clamped.** A positive value below 120 seconds raises [`8152`](../../../foundations/error-codes.md#error-8152) instead of being rounded up.
- **Dependency chain:** [Get Publish Configurations](get-publish-configurations.md) → merge → Update Publish Configurations → [Get Publish Configurations](get-publish-configurations.md) to verify.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Three of seven APIs return 204 with no body** | [Remove Public Permission](remove-public-permission.md), [Remove Private Access](remove-private-access.md), and [Update Publish Configurations](update-publish-configurations.md) return HTTP **204 No Content** on success — treat the 2xx status code as the success indicator and never expect or parse a JSON body for these three. The other four return the standard `{"status", "summary", "data"}` envelope with HTTP 200. |
| **Failure responses always carry a body** | Even for the 204 APIs, errors return `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name (e.g. `SECURITY_NOT_PERMITTED`), not a localised sentence. |
| **The returned URL host is not the API host** | `data.publicUrl` and `data.privateUrl` point at the Zoho Analytics **application** domain (e.g. `analytics.zoho.com`) or, in a Client Portal / White Label context, at the workspace's portal domain — never at the `analyticsapi.*` host the request was sent to. Do not construct these URLs client-side from the API host. |
| **`publicUrl` and `privateUrl` differ only by the appended key** | Both are `https://<domain>/open-view/<view-id>`; the private form appends `/<32-char-hex-key>`. Nothing else in the URL encodes the permission set, criteria, or audience level — those are enforced server-side when the URL is opened. |
| **Conditional top-level keys, not empty placeholders** | [Get Publish Configurations](get-publish-configurations.md) **omits** `publicViewConfig` / `privateLinkConfig` when the caller lacks the corresponding permission or the feature is unavailable — unlike the sharing APIs, which return empty containers. Always test for key presence before reading into them. |
| **`"-1"` is the "unset" sentinel, not `null`** | `privateLinkConfig.password` and `privateLinkConfig.expiryDate` use the string `"-1"` to mean "not configured". Similarly `publishConfig.autoRefresh` uses the number `-1` to mean "no auto-refresh". No field in these responses is ever `null`. |
| **Booleans are native, numbers are native, dates are strings** | Unlike the sharing APIs (where `inheritParentFilterCriteria` is serialised as the string `"true"`/`"false"`), every boolean in `publicViewConfig` / `privateLinkConfig` / `publishConfig` is a native JSON boolean, and `publicPermLevel`, `width`, `height`, and `autoRefresh` are native JSON numbers. `expiryDate` is a `dd/MM/yyyy` string in GMT. |
| **View IDs in the URL are numeric path segments** | Unlike the sharing APIs' response payloads, which return IDs as JSON strings, the publish APIs carry the view ID only inside the returned URL text — extract it as a string to avoid precision loss on large IDs. |
| **Effects are observable through the Sharing APIs** | Because both channels are modelled as shares to reserved pseudo-users, [Get Shared Details](../sharing/get-shared-details-for-views.md) is the canonical way to audit what a public or private link actually grants: look for `sharedTo: "Public Visitor"` / `sharedToZuId: "-20"` (with `publicPermLevel` set) and `sharedTo: "Private Link"` / `sharedToZuId: "-30"` (with `publicPermLevel: 0`), plus the resolved `permissionString`, `criteria`, `vudColumns`, and `drillColumns`. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [6054](../../../foundations/error-codes.md#error-6054) | 400 | PUBLISHCNTVIOLATION — The current plan does not allow this publish operation. |
| [6055](../../../foundations/error-codes.md#error-6055) | 400 | REGENERATEVIOLATION — The current plan does not allow regenerating a private-link key. |
| [6056](../../../foundations/error-codes.md#error-6056) | 400 | SHAREDUSRPUBLISHCNTVIOLATION — A shared user attempted a plan-restricted private-link creation. |
| [6057](../../../foundations/error-codes.md#error-6057) | 400 | SHAREDUSRREGENERATEVIOLATION — A shared user attempted a plan-restricted key regeneration. |
| [6121](../../../foundations/error-codes.md#error-6121) | 400 | EXCEEDINGUSRPLNPRIVATELINKS — The organization has used all private links allowed by its plan. |
| [6122](../../../foundations/error-codes.md#error-6122) | 400 | EXCEEDINGUSRPLNPRIVATELINKSDM — Same limit, reported to a non-super-admin caller. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7138](../../../foundations/error-codes.md#error-7138) | 400 | baseTableName does not resolve to a table in this workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [7500](../../../foundations/error-codes.md#error-7500) | 400 | UNAUTHORIZEDORGCANNOTMAKEPUBLIC — publicPermLevel: "3" requested but the caller does not belong to the workspace admin's business organization. |
| [7531](../../../foundations/error-codes.md#error-7531) | 400 | PUBLICTOORGNOTSUPPORTEDINFREE — publicPermLevel 2 or 3 is not supported on the Free plan. |
| [7565](../../../foundations/error-codes.md#error-7565) | 400 | UNVERIFIEDEMAIL — The calling user's primary email address is not verified. |
| [8032](../../../foundations/error-codes.md#error-8032) | 400 | VIEWNOTSHARED — The view is not currently shared with the specified user. |
| [8054](../../../foundations/error-codes.md#error-8054) | 400 | INVALIDFILTERCRITERIA — criteria could not be parsed. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | The specified domainName does not exist. |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | The specified domainName does not belong to the org's Account Admin. |
| [8074](../../../foundations/error-codes.md#error-8074) | 400 | READPERMSHOULDBETRUEFORSHARING — permissions.read was sent as false. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | CONFIG is not valid JSON, was not URL-encoded correctly, contains an unsupported key, or violates a type or length constraint. |
| [8088](../../../foundations/error-codes.md#error-8088) | 400 | SECURITYCONTROLSFEATUREDISABLED — Export is disabled for the organization. |
| [8115](../../../foundations/error-codes.md#error-8115) | 404 | VIEWNOTPUBLISHEDASPRIVATE — The view has no private link. |
| [8152](../../../foundations/error-codes.md#error-8152) | 400 | INTERVALSHOULDBE120ORABOVE — autoRefresh is a positive value below 120 seconds. |
| [8154](../../../foundations/error-codes.md#error-8154) | 400 | COLUMNNOTPRESENTINTABLE — A column in vudColumns / drillColumns (or in criteria) does not exist in the given table. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | SYSTEMTAGDATAWARNINGV2VALIDATIONCONFIRMATION — The view carries a restricted DATAWARNING system tag. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |
| [12052](../../../foundations/error-codes.md#error-12052) | 400 | WORKSPACENOTENABLEDFORDOMAINACCESS — The workspace is not enabled for access through the requested portal domain. |

# Related

- [Share & Publish](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
