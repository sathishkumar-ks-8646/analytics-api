---
type: API Group
title: Embed URL
description: APIs for retrieving embeddable view URLs.
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - embed-url
  - api-group
api:
  domain: share-and-publish
  group: embed-url
  endpoint_count: 3
  endpoints:
    - operation_id: getEmbedUrl
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embed"
      doc: "/domains/share-and-publish/embed-url/get-embed-url.md"
    - operation_id: getEmbedUrls
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embedurls"
      doc: "/domains/share-and-publish/embed-url/get-embed-urls.md"
    - operation_id: deleteEmbedUrl
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embed"
      doc: "/domains/share-and-publish/embed-url/delete-embed-url.md"
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

This document covers the V2 **Embed URL** REST APIs of Zoho Analytics — the APIs that mint short-lived, login-free URLs for embedding a single view inside an external application, list the embed URLs already issued for a view, and revoke them.

APIs for retrieving embeddable view URLs.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Embed URL](get-embed-url.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embed` | `getEmbedUrl` | `ZohoAnalytics.embed.read` | 200 |
| [Fetch All Embed URLs](get-embed-urls.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embedurls` | `getEmbedUrls` |  | 200 |
| [Delete Embed URL](delete-embed-url.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embed` | `deleteEmbedUrl` |  | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is an "Embed URL" in Zoho Analytics?

An **embed URL** is a signed, time-limited URL of the form `https://<analytics-domain>/open-view/<view-id>?RSCONFIG=<config-key>&FS=OS` that renders one view inside an `<iframe>` in a host application. It differs from every other publish channel in three important ways:

| | Embed URL | [Public URL](../publish/make-views-public.md) | [Private URL](../publish/create-private-url.md) |
|---|---|---|---|
| **Lifetime** | Expires after `validityPeriod` seconds (default 1 hour, maximum 1 day) | Never expires until revoked | Never expires unless an `expiryDate` is set |
| **Config storage** | Each call mints a **new** URL with its own permission set, filter criteria, and column restrictions | One shared configuration per view | One shared configuration per view |
| **How many per view** | Many, concurrently — one per call | One | One |
| **Availability** | **Embedded Analytics (OEM) customers only** | All plans (subject to plan gating) | Plan-gated |

Because each call produces an independent, self-contained URL, embed URLs are the mechanism for **multi-tenant embedding**: a host application can issue one URL per end customer, each pre-filtered with its own `criteria` and scoped to its own columns, without creating any Zoho Analytics users.

The `RSCONFIG` value in the URL is the opaque key under which that URL's configuration is stored. It is also the identifier used to revoke a single URL through [Delete Embed URL](delete-embed-url.md), and the value returned as `rsConfig` by [Fetch All Embed URLs](get-embed-urls.md).

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`). All three APIs use the **`embed`** scope family.
> - All three APIs are **view-scoped** (`/workspaces/<workspace-id>/views/<view-id>/publish/...`) and require the `ZANALYTICS-ORGID` header.
> - **All three APIs require the organization (or the specific workspace) to be enabled for Embedded Analytics (OEM).** On an ordinary organization every call fails with [`8023`](../../../foundations/error-codes.md#error-8023) `OEM_OPERATION_NOT_ALLOWED` (HTTP 403) regardless of the caller's role.
> - **All three APIs are disabled in Client Portal / White Label request contexts.** A request that arrives through a custom domain is rejected with [`7301`](../../../foundations/error-codes.md#error-7301) before any business logic runs — see [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour).
> - The API host (`ZohoAnalytics_Server_URI`, e.g. `analyticsapi.zoho.com`, `analyticsapi.zoho.eu`) is **not** the host that appears in the returned `embedUrl`. The returned URL always points at the Zoho Analytics **application** domain (e.g. `analytics.zoho.com`) or, when `domainName` is supplied by a Client Portal admin, at that portal domain.
> - None of these APIs requires the caller's primary email to be verified.

---

# White Label / Client Portal Behaviour

All three APIs are blocked in Client Portal / White Label request contexts. This is the **opposite** of the [Publish](../publish/overview.md) and [Slideshow](../slideshow-management/overview.md) families, and it has two distinct consequences that are easy to conflate:

| Scenario | Result |
|----------|--------|
| The API request itself arrives **through** a Client Portal / White Label custom domain | **Rejected with `7301`** before any business logic runs. The embed APIs cannot be invoked from a portal-domain context at all. |
| A Client Portal admin calls the API **from the standard API host** and passes `domainName` in CONFIG ([Get Embed URL](get-embed-url.md) only) | **Allowed.** The generated `embedUrl` is built on that portal domain, so the iframe renders under the white-labelled host. |

So a white-labelled deployment embeds views by calling the standard `analyticsapi.zoho.*` host with `domainName`, never by calling the portal host. The [`7301`](../../../foundations/error-codes.md#error-7301) responses shown in this document's White Label samples are the first scenario.

---

# API-Specific Notes and Behaviours

## Get Embed URL

- **A factory, not an accessor — this is the single most important thing to understand.** Unlike every other publish API, each call creates a *new* persisted configuration and returns a *new* URL. Nothing is idempotent and nothing about the view changes. An integration that calls it on every page load will accumulate one stored configuration per page load; pair it with [Delete Embed URL](delete-embed-url.md) or a short `validityPeriod` to keep that bounded.
- **`criteria` is what makes multi-tenant embedding work.** The filter is bound to the URL rather than to the view or to a user, so one view can serve many customers with one URL each. This is the reason `criteria` is the most-used attribute of the whole family, and why it is stored encrypted.
- **The default lifetime is one hour.** Without `validityPeriod` the URL dies after 3600 seconds, and the maximum it can be raised to is 86400 seconds (1 day). The value is *validated*, not clamped — anything larger raises [`8177`](../../../foundations/error-codes.md#error-8177).
- **`domainName` supersedes `withCustomDomain`.** Both target a Client Portal / White Label domain, but the legacy flag additionally requires the caller to be an Organization Admin or Super Admin, and it fails silently when that is not the case. Prefer `domainName` in new integrations.
- **Exclude beats include for column restrictions.** Sending both `vudColumns` and `vudColumnsToExclude` silently uses the exclude list. Same for the drill pair. Pick one model per restriction.
- **Treat `embedUrl` as opaque.** The URL is only `?RSCONFIG=<key>&FS=OS`; every option requested in CONFIG lives server-side against that key. Do not parse it beyond extracting `RSCONFIG` when you need the revocation key, and do not try to change behaviour by editing the query string.
- **Dependency chain:** [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>` → Get Embed URL → [Fetch All Embed URLs](get-embed-urls.md) to audit → [Delete Embed URL](delete-embed-url.md) to revoke.

## Fetch All Embed URLs

- **The only way to see what has been handed out.** Because [Get Embed URL](get-embed-url.md) returns nothing but the URL itself, this is the sole API that reveals a URL's permissions, filter criteria, column restrictions, creator, and expiry after the fact. It is the audit backbone of the embed channel.
- **Its default view is incomplete on purpose.** Expired entries are filtered out unless `includeExpiredUrls: true` is sent, so a `[]` response does not mean nothing was ever issued. Always use the flag for a genuine audit.
- **It returns decrypted `criteria`.** That makes the response materially more sensitive than the other reads in this family — a tenant-scoped filter can name the tenant. Restrict access and avoid logging.
- **Expiry is raw milliseconds with no helper flag.** There is no `isExpired` boolean and no formatted date; compare `expiryTime` against the current time yourself.
- **Columns come back as IDs while the request side takes names.** The asymmetry with [Get Embed URL](get-embed-url.md)'s `tableName`/`columnNames` shape means a read-modify-remint workflow must resolve IDs through [Get Columns](../../data-modeling-and-schema/columns/overview.md) first.
- **Higher role bar than Get Embed URL.** Minting is available to workspace owners and OEM-enabled users; listing and revoking are restricted to Account Admins and Organization Admins. An integration user that can create URLs may well be unable to enumerate them.
- **Dependency chain:** [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>` → Fetch All Embed URLs → `rsConfig` → [Delete Embed URL](delete-embed-url.md).

## Delete Embed URL

- **204 No Content, no body.** Verified against the implementation and the recorded 0-byte response samples. Never parse a JSON success body, and note that the response does not report how many URLs were removed.
- **The only API in this family that requires CONFIG.** Both of the GET APIs work with no CONFIG at all; here CONFIG is mandatory and must express exactly one of the two modes. Omitting it entirely, or sending both modes, is rejected with [`8178`](../../../foundations/error-codes.md#error-8178) rather than defaulting to something.
- **Neither mode is idempotent.** Targeted repeats fail with [`8175`](../../../foundations/error-codes.md#error-8175), bulk repeats with [`8176`](../../../foundations/error-codes.md#error-8176). Both mean "nothing matched", which is arguably a success from the caller's point of view but is reported as a 404-class error — wrap retries accordingly.
- **Bulk delete destroys the audit trail.** `deleteAllUrls: true` removes expired configurations too, so anything [Fetch All Embed URLs](get-embed-urls.md) would have shown with `includeExpiredUrls: true` is gone as well. Export the listing first if the history matters.
- **Revocation cannot be undone.** A replacement URL must be minted, and it will carry a different `RSCONFIG` key — so any host application holding the old URL must be updated, not just refreshed.
- **Scope-isolated from the other publish channels.** Public URLs, private URLs, slideshows, and user/group shares on the same view are untouched; each has its own removal API.
- **Dependency chain:** [Fetch All Embed URLs](get-embed-urls.md) → `rsConfig` → Delete Embed URL → [Fetch All Embed URLs](get-embed-urls.md) to verify.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **One of three APIs returns 204 with no body** | [Delete Embed URL](delete-embed-url.md) returns HTTP **204 No Content** on success — treat the 2xx status code as the success indicator and never expect or parse a JSON body. The two GET APIs return the standard `{"status", "summary", "data"}` envelope with HTTP 200. |
| **Failure responses always carry a body** | Even for the 204 API, errors return `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name (e.g. `OEM_OPERATION_NOT_ALLOWED`, `OEM_VIEW_HOLD_NO_KEYS`), not a localised sentence. |
| **403 is the normal outcome on a non-OEM organization** | Because all three APIs are gated on Embedded Analytics entitlement, `8023` (HTTP 403) — not `7301` — is what an ordinary organization sees, whatever the caller's role. Do not interpret it as a permission-configuration problem. |
| **Timestamps are millisecond epoch strings** | `embedUrls[].expiryTime` is a string containing epoch **milliseconds**. There are no formatted dates anywhere in these payloads, and no `isExpired` convenience flag. |
| **All IDs are strings** | `vudConfig.vudTables`, `vudConfig.vudColumns`, and `drillConfig.drillColumns` are arrays of **strings** even though the values are numeric IDs. Parse them as strings or longs — never as native JSON numbers — to avoid precision loss. |
| **Conditional keys, not empty placeholders** | `vudConfig` and `drillConfig` are **omitted entirely** when the URL carries no such restriction. This differs from the sharing APIs, which return empty containers. Always test for key presence. |
| **`criteria` is `""`, never `null` or absent** | An unfiltered embed URL reports `"criteria": ""`. `embedUrls` itself is likewise always present, empty (`[]`) when nothing matches the filter. |
| **`permissions` in the embed channel is a fixed five-key object** | Exactly `read`, `export`, `vud`, `drillDown`, `insight`, all booleans, `read` always `true`. It is a strict subset of the [sharing `permissions` object](../sharing/share-views.md#permissions-fields) and of the [publish `permissions` object](../publish/make-views-public.md#permissions-fields) — code against the narrow shape, not the wide one. |
| **The returned URL host is not the API host** | `data.embedUrl` points at the Zoho Analytics **application** domain (e.g. `analytics.zoho.com`) or, when `domainName` was supplied, at that portal domain — never at the `analyticsapi.*` host the request was sent to. Do not construct these URLs client-side from the API host. |
| **`rsConfig` and `embedUrl` are credentials** | `rsConfig` appears in the listing response and inside every `embedUrl` as the `RSCONFIG=` parameter. Anyone holding the full URL can view the data, with the baked-in permissions and filter, until it expires. Avoid logging these values and restrict who may call [Fetch All Embed URLs](get-embed-urls.md). |
| **Configuration is never echoed on mint** | [Get Embed URL](get-embed-url.md) returns only `embedUrl` — not the permissions, criteria, validity, or column restrictions that were applied. Confirm what was stored with [Fetch All Embed URLs](get-embed-urls.md) rather than assuming the request took effect verbatim. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7138](../../../foundations/error-codes.md#error-7138) | 400 | A tableName in vudColumns / drillColumns is not a table involved in this view. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [8023](../../../foundations/error-codes.md#error-8023) | 403 | The organization/workspace is not enabled for Embedded Analytics. |
| [8054](../../../foundations/error-codes.md#error-8054) | 400 | criteria could not be parsed. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | The specified domainName does not exist. |
| [8061](../../../foundations/error-codes.md#error-8061) | 400 | The specified domainName does not belong to the organization's Account Admin. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | CONFIG is not valid JSON, was not URL-encoded correctly, contains an unsupported key, or violates a type or length constraint. |
| [8154](../../../foundations/error-codes.md#error-8154) | 400 | A column in vudColumns / drillColumns (or in criteria) does not exist in the given table. |
| [8175](../../../foundations/error-codes.md#error-8175) | 404 | No embed URL on this view matches the supplied rsConfig. |
| [8176](../../../foundations/error-codes.md#error-8176) | 404 | deleteAllUrls was requested but the view has no embed URLs. |
| [8177](../../../foundations/error-codes.md#error-8177) | 400 | validityPeriod exceeds the maximum of 86400 seconds (1 day). |
| [8178](../../../foundations/error-codes.md#error-8178) | 400 | Both rsConfig and deleteAllUrls: true were sent, or neither was. |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | The view carries a restricted DATAWARNING system tag. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |
| [9102](../../../foundations/error-codes.md#error-9102) | 400 | language is not one of the supported language names. |
| [12052](../../../foundations/error-codes.md#error-12052) | 400 | The workspace is not enabled for access through the requested portal domain. |

# Related

- [Share & Publish](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
