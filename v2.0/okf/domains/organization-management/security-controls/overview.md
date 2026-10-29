---
type: API Group
title: Security Controls
description: "APIs for reading and updating the access restriction settings of an organisation and of an individual workspace - sharing, private links, public views, export and email."
tags:
  - zoho-analytics
  - rest-api-v2
  - organization-management
  - security-controls
  - api-group
api:
  domain: organization-management
  group: security-controls
  endpoint_count: 4
  endpoints:
    - operation_id: getOrgAccessRestrictions
      method: GET
      path: "/restapi/v2/security-controls/access-restrictions"
      doc: "/domains/organization-management/security-controls/get-org-access-restrictions.md"
      api_units: 1
      api_units_action: GET_ORG_ACCESS_RESTRICTIONS
      api_units_category: METADATA
    - operation_id: updateOrgAccessRestrictions
      method: PUT
      path: "/restapi/v2/security-controls/access-restrictions"
      doc: "/domains/organization-management/security-controls/update-org-access-restrictions.md"
      api_units: 1
      api_units_action: UPDATE_ORG_ACCESS_RESTRICTIONS
      api_units_category: METADATA
    - operation_id: getWorkspaceAccessRestrictions
      method: GET
      path: "/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions"
      doc: "/domains/organization-management/security-controls/get-workspace-access-restrictions.md"
      api_units: 1
      api_units_action: GET_WORKSPACE_ACCESS_RESTRICTIONS
      api_units_category: METADATA
    - operation_id: updateWorkspaceAccessRestrictions
      method: PUT
      path: "/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions"
      doc: "/domains/organization-management/security-controls/update-workspace-access-restrictions.md"
      api_units: 1
      api_units_action: UPDATE_WORKSPACE_ACCESS_RESTRICTIONS
      api_units_category: METADATA
sources:
  - id: openapi-spec
    resource: "/references/openapi/org-management-grouped-api.json"
    title: OpenAPI 3 specification - org-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T10:58:51Z
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

This document covers the V2 **Access Restriction** REST APIs of Zoho Analytics — the APIs that read and update the organisation-level and workspace-level controls governing who may receive shared views, whether private links, public views, exports and emailed views are allowed, and which email domains are trusted for each.

APIs for reading and updating the access restriction settings of an organisation and of an individual workspace - sharing, private links, public views, export and email.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success | API units |
|---|---|---|---|---|---|---|
| [Get Org Access Restrictions](get-org-access-restrictions.md) | GET | `/restapi/v2/security-controls/access-restrictions` | `getOrgAccessRestrictions` | `ZohoAnalytics.metadata.read` | 200 | 1 |
| [Update Org Access Restrictions](update-org-access-restrictions.md) | PUT | `/restapi/v2/security-controls/access-restrictions` | `updateOrgAccessRestrictions` | `ZohoAnalytics.metadata.update` | 204 | 1 |
| [Get Workspace Access Restrictions](get-workspace-access-restrictions.md) | GET | `/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions` | `getWorkspaceAccessRestrictions` | `ZohoAnalytics.metadata.read` | 200 | 1 |
| [Update Workspace Access Restrictions](update-workspace-access-restrictions.md) | PUT | `/restapi/v2/security-controls/workspaces/{workspace-id}/access-restrictions` | `updateWorkspaceAccessRestrictions` | `ZohoAnalytics.metadata.update` | 204 | 1 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is an "Access Restriction" in Zoho Analytics?

Access Restrictions are the **Security Controls → Access Restriction** settings of an organisation. They limit how views leave the organisation: who they can be shared with, whether they can be opened without login, whether they can be exported, and where they can be emailed. They are configured once for the organisation and can optionally be overridden, as a complete set, for an individual workspace.

| Part | CONFIG attribute(s) | Notes |
|------|--------------------|-------|
| **Master switch** | `accessRestrictionEnabled` | Organisation level only. When `false`, **none** of the settings below are enforced for the organisation or any of its workspaces. Stored values are retained. |
| **Share views** | `shareViews` | Restricts sharing of views to users whose email domain is in `trustedDomains`. Sharing itself cannot be switched off — there is no `enabled` attribute. |
| **Private links** | `privateLinks` | `enabled` switches generation of private links (links that open without login) on or off. A domain restriction makes them prompt for login and admits only users from `trustedDomains`. |
| **Public views** | `publicViews` | `enabled` switches the ability to make views public on or off. A domain restriction makes public views prompt for login and admits only users from `trustedDomains`. |
| **Export views** | `exportViews` | `enabled` switches exporting of views and data on or off. **Disabling export also disables email views.** |
| **Email views** | `emailViews` | `enabled` switches emailing of views (including email schedules) on or off. A domain restriction limits recipients to `trustedDomains`. |
| **Workspace override** | `useOrganizationSettings` | Workspace level only. `true` — the workspace follows the organisation. `false` — the workspace has its own settings. |

> **The single most important behaviour:** a workspace either follows the organisation or has its **own complete set** of settings — never a mix — and switching a workspace to its own settings does **not** copy the organisation's values. See [Organisation and Workspace Settings Lifecycle](overview.md#organisation-and-workspace-settings-lifecycle) before writing any integration that calls [Update Workspace Access Restrictions](update-workspace-access-restrictions.md).

# How Section Updates Are Validated

`shareViews`, `privateLinks`, `publicViews`, `exportViews` and `emailViews` are **sections**. Both update APIs process them in that fixed order, inside a single transaction: if any section fails validation, **nothing** from the request is saved.

Every section is **partially updated**. An omitted section is untouched. Within a section, an omitted attribute keeps its stored value, and the rules below are evaluated against the **resulting** state (stored value overlaid with the request).

| Rule | Applies to | Triggered when | Code |
|------|-----------|----------------|------|
| **Trusted domains need an active domain restriction** | `shareViews`, `privateLinks`, `publicViews`, `emailViews` | `trustedDomains` is non-empty while the resulting `domainRestrictionEnabled` is `false`; **or** `trustedDomains` (even `[]`) is sent while the restriction is currently off and `domainRestrictionEnabled` is not in the same request. | `8192` |
| **Trusted domains must not be empty while restricting** | `shareViews`, `privateLinks`, `publicViews`, `emailViews` | The resulting `domainRestrictionEnabled` is `true` and `trustedDomains` is `[]`; **or** the restriction is being switched on, the request carries no `trustedDomains`, and none are stored. | `8193` |
| **No domain settings on a disabled feature** | `privateLinks`, `publicViews`, `emailViews` | The feature is currently disabled and not re-enabled in this request, and the request carries `domainRestrictionEnabled` or `trustedDomains`; **or** `enabled` is `false` in this request together with `domainRestrictionEnabled: true` or a non-empty `trustedDomains`. | `8194` |
| **Email views depend on export** | `emailViews` | Export is currently disabled and the request does not enable it, and `emailViews` is present at all; **or** export is being disabled in this request and `emailViews.enabled` does not resolve to `false`. | `8195` |

**What a domain list does when you send it:**

- `trustedDomains` **replaces** the stored list. Domains in the request but not stored are added; domains stored but not in the request are removed. Matching is exact and **case-sensitive**, so `Example.com` and `example.com` are different entries.
- An omitted `trustedDomains` leaves the stored list untouched. Switching `domainRestrictionEnabled` to `false` **keeps** the stored list; it stops being enforced and is reused if you switch the restriction on again without sending a list.
- To clear the list, send `domainRestrictionEnabled: false` together with `trustedDomains: []`.
- Blank strings and `null` entries are dropped and surrounding whitespace is trimmed **before** validation, so `[""]` is treated as `[]`.

**Disabling export disables email views.** Sending `exportViews: {"enabled": false}` also sets email views to disabled, even when `emailViews` is omitted. Re-enabling export does **not** re-enable email views; send `emailViews: {"enabled": true}` in the same request or a later one.

> **Never PUT a GET response back.** A response from [Get Org Access Restrictions](get-org-access-restrictions.md) or [Get Workspace Access Restrictions](get-workspace-access-restrictions.md) reports every attribute of every section, including attributes on features that are disabled. Sending it back verbatim fails whenever a feature is disabled ([`8194`](../../../foundations/error-codes.md#error-8194) for `privateLinks`, `publicViews` or `emailViews`, [`8195`](../../../foundations/error-codes.md#error-8195) for `emailViews` when export is disabled), and the workspace response carries `configurationSource`, which is not a CONFIG attribute. Send only the attributes you intend to change.

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`). The read APIs use `ZohoAnalytics.metadata.read`; the update APIs use `ZohoAnalytics.metadata.update` — see [OAuth scopes](../../../foundations/oauth-scopes.md).
> - All four APIs are **organisation-scoped** (`/restapi/v2/security-controls/...`) and require the `ZANALYTICS-ORGID` header. The two workspace APIs additionally carry `<workspace-id>` in the path, and the workspace must belong to the organisation named in the header.
> - `ZohoAnalytics_Server_URI` depends on the data centre (`analyticsapi.zoho.com`, `.eu`, etc.).
> - **All four APIs are disabled in Client Portal / White Label request contexts** and return [`7301`](../../../foundations/error-codes.md#error-7301).
> - **Only Account Admins and Organization Admins may call them.** Workspace Admins and custom-role users are refused with [`7301`](../../../foundations/error-codes.md#error-7301) — see [Permission Model](overview.md#permission-model).
> - Each call is registered with 1 API unit (Metadata group).
> - None of these APIs accepts a `criteria` attribute. There is no search, filter, sort or paging parameter; every response is a single small object.
> - IP restriction, trusted email IDs and Client Portal / White Label domain restrictions are **not** configurable through these APIs.

---

# Organisation and Workspace Settings Lifecycle

**A workspace that has its own settings does not inherit anything from the organisation — and one that has just been switched to its own settings starts from defaults, not from a copy of the organisation's values.**

| What you do | What happens |
|-------------|--------------|
| `PUT` workspace with `useOrganizationSettings: false` on a workspace that follows the organisation, no sections | The workspace gets its own settings. Every section starts at its **default**: feature allowed (`enabled: true`), domain restriction off, no trusted domains. This is **less restrictive** than a restricted organisation. |
| Same, with one or more sections | Only the sections you name are written. Sections you do not name start at their defaults. For a section you name, an omitted attribute may inherit the organisation's current value, but the organisation's `trustedDomains` list is **never** copied. |
| `PUT` workspace with `useOrganizationSettings: true` on a workspace that has its own settings | The workspace follows the organisation again. Its own values are **kept but ignored**, and reappear if you later set `useOrganizationSettings: false`. |
| `PUT` workspace with sections but without `useOrganizationSettings: false` on a workspace that follows the organisation | Rejected with `8199`. The omitted `useOrganizationSettings` is treated as `true`. |
| `PUT` workspace with `useOrganizationSettings: true` **and** sections | Rejected with `8198`. |
| `PUT` org with `accessRestrictionEnabled: false` | The master switch goes off. No setting is enforced for the organisation or any workspace; every stored value is retained and still returned by the GET APIs. |
| `PUT` workspace while the organisation master switch is off | Rejected with `8197`. |

The rule the server applies is: **a workspace's `configurationSource` is `WORKSPACE` only if its own settings were switched on by an earlier `useOrganizationSettings: false`; otherwise it is `ORG`, and the GET API reports the organisation's values.**

Practical consequences:

1. **Read before you override.** Call [Get Org Access Restrictions](get-org-access-restrictions.md), then name in the first `useOrganizationSettings: false` request every section whose organisation setting you want to keep: send `enabled` and, for a section with an active domain restriction, `domainRestrictionEnabled: true` with its `trustedDomains`. Do not send domain attributes for a feature the organisation has disabled ([`8194`](../../../foundations/error-codes.md#error-8194)). A bare `{"useOrganizationSettings": false}` leaves the workspace unrestricted.
2. **`configurationSource` tells you which values you are looking at.** On a workspace that follows the organisation, [Get Workspace Access Restrictions](get-workspace-access-restrictions.md) returns the **organisation's** values, not stored workspace values.
3. **Reverting is reversible.** Setting `useOrganizationSettings: true` does not delete workspace settings; there is no API that deletes them. To make a workspace's own settings take effect again, set `useOrganizationSettings: false` and omit all sections.
4. **Changing the organisation later does not update an overridden workspace.** Once `configurationSource` is `WORKSPACE`, changes to the organisation's sections have no effect on that workspace.

Design integrations so that the organisation's settings are the default, and use workspace overrides only for named exceptions.

---

# Limitations

These are the limits that apply with **default settings**.

| Limitation | Value | Enforced by |
|------------|-------|-------------|
| **Callers** | Account Admins and Organization Admins only. | `7301` |
| **Workspace overrides require the master switch** | `accessRestrictionEnabled` must be `true` for the organisation. | `8197` |
| **`trustedDomains` entries per section per request** | **0–100.** Because the list replaces the stored one, this is also the most a section can hold. | — |
| **Length of one trusted domain** | **250** characters. | — |
| **Format of one trusted domain** | A fully qualified domain name such as `example.com` or `mail.example.org`: dot-separated labels of letters, digits and hyphens (1–63 characters, not starting or ending with a hyphen) ending in an alphabetic top-level domain of 2–15 letters. No scheme (`https://`), no wildcard (`*.`), no `@`, no port, no path. | — |
| **`CONFIG` length** | **21,000** characters. | — |
| **Settings not covered** | IP restriction, trusted email IDs, per-view and per-user overrides. | — |
| **Deleting workspace settings** | **Not possible.** A workspace can only be switched back to the organisation's settings. | — |

> **Request-format limits are enforced before the request reaches the handler.** A malformed `trustedDomains` entry, a non-boolean flag, or an over-long `CONFIG` is rejected at that layer, not by one of the codes in the Error Codes tables below.

---

# Permission Model

| Role | May do | Notes |
|------|--------|-------|
| Account Admin / Organization Admin | All four APIs. | The `ZANALYTICS-ORGID` header must name an organisation the caller administers. |
| Workspace Admin | Nothing in this document. | Refused with `7301`, even for a workspace they administer. |
| Custom role, any permission | Nothing in this document. | Refused with `7301`. |
| Any user on a Client Portal / White Label domain | Nothing in this document. | Refused with `7301`; the APIs are disabled on those domains. |

---

# API-Specific Notes and Behaviours

## Get Org Access Restrictions

- **Treat `accessRestrictionEnabled` as the gate.** The section values are reported whether or not they are enforced.
- **Use it as the source of values for a workspace override.** The first `useOrganizationSettings: false` request does not copy them for you.
- **Dependency chain:** [Organization Info and Settings](../org-info-and-settings/overview.md) → `ZANALYTICS-ORGID` → Get Org Access Restrictions.

## Update Org Access Restrictions

- **Send only what you change.** Verbatim GET payloads fail whenever a feature is disabled ([`8194`](../../../foundations/error-codes.md#error-8194), [`8195`](../../../foundations/error-codes.md#error-8195)).
- **Disabling export implies disabling email views.** `emailViews: {"enabled": false}` is accepted alongside it; an `emailViews` that would leave email views enabled is rejected ([`8195`](../../../foundations/error-codes.md#error-8195)).
- **To switch everything off, send `accessRestrictionEnabled: false` alone.** Stored section values remain and apply again when you switch it back on.
- **Dependency chain:** [Get Org Access Restrictions](get-org-access-restrictions.md) → Update Org Access Restrictions → read it back with Get Org Access Restrictions.

## Get Workspace Access Restrictions

- **Check `configurationSource` before interpreting the sections.** `ORG` means they are the organisation's values.
- **Dependency chain:** [Workspace Operations](../../workspace-management/workspace-operations/overview.md) → `<workspace-id>` → Get Workspace Access Restrictions.

## Update Workspace Access Restrictions

- **The organisation master switch gates everything.** With it off, even a revert to `useOrganizationSettings: true` fails ([`8197`](../../../foundations/error-codes.md#error-8197)).
- **Name every section on the first override.** Unnamed sections start unrestricted.
- **Dependency chain:** [Get Workspace Access Restrictions](get-workspace-access-restrictions.md) → Update Workspace Access Restrictions → read it back with Get Workspace Access Restrictions.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Which endpoints return 204** | [Update Org Access Restrictions](update-org-access-restrictions.md) and [Update Workspace Access Restrictions](update-workspace-access-restrictions.md) return `204 No Content` with no body. The two GET APIs return `200 OK`. |
| **Failure responses always carry a body** | Even for the 204 APIs, errors return `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name, not a localised sentence. |
| **No IDs in the responses** | The GET APIs return settings only; neither echoes the organisation or workspace ID. |
| **Booleans are JSON booleans** | Every flag is `true` or `false`, never a string. |
| **Empty array, never a missing key** | Every `trustedDomains` is always present, `[]` when empty. |
| **Key order is not guaranteed** | Read by name, not position. |
| **`exportViews` has only `enabled`** | It carries no domain attributes in requests or responses. |
| **Responses are extensible** | Some builds return additional fields. Ignore unrecognised keys rather than validating against a closed schema. |

---

# Enum and Value Reference

### `configurationSource` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `ORG` | The workspace follows the organisation; the response holds the organisation's values. | Response only. |
| `WORKSPACE` | The workspace has its own settings; the response holds the workspace's values. | Response only. Set by `useOrganizationSettings: false`. |

---

# CONFIG Attribute Availability by API

| Attribute | Update Org Access Restrictions | Update Workspace Access Restrictions |
|-----------|---|---|
| `accessRestrictionEnabled` | ✔ | — |
| `useOrganizationSettings` | — | ✔ |
| `shareViews` | ✔ | ✔ |
| `privateLinks` | ✔ | ✔ |
| `publicViews` | ✔ | ✔ |
| `exportViews` | ✔ | ✔ |
| `emailViews` | ✔ | ✔ |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7387](../../../foundations/error-codes.md#error-7387) | 400 | DBID_NOT_BELONGS_TO_ZSOID - The workspace does not belong to the organisation in ZANALYTICS-ORGID. |
| [8077](../../../foundations/error-codes.md#error-8077) | 400 | EMPTY_JSON_CONFIGURATION - CONFIG is present but empty. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | CONFIG is not valid JSON, was not URL-encoded correctly, contains an unsupported key, or violates a type or length constraint. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | The ZANALYTICS-ORGID header is missing from a request that requires it. |
| [8084](../../../foundations/error-codes.md#error-8084) | 404 | ORGID_NOT_EXIST - No organisation exists with the given ID. |
| [8192](../../../foundations/error-codes.md#error-8192) | 400 | TRUSTED_DOMAINS_WITHOUT_DOMAIN_RESTRICTION - trustedDomains was sent for a section whose domain restriction is off or is being switched off. |
| [8193](../../../foundations/error-codes.md#error-8193) | 400 | TRUSTED_DOMAINS_EMPTY - The domain restriction is on, or being switched on, but the section has no trusted domains. |
| [8194](../../../foundations/error-codes.md#error-8194) | 400 | DOMAIN_RESTRICTION_NOT_ALLOWED_WHEN_DISABLED - Domain attributes were sent for privateLinks, publicViews or emailViews while that feature is disabled or is being disabled. |
| [8195](../../../foundations/error-codes.md#error-8195) | 400 | EMAIL_NOT_ALLOWED_WHEN_EXPORT_DISABLED - emailViews was sent while export is disabled or is being disabled, and email views would stay enabled. |
| [8196](../../../foundations/error-codes.md#error-8196) | 400 | ACCESS_RESTRICTION_DISABLED - Access restriction is off for the organisation and the request carries sections without turning it on, including accessRestrictionEnabled: false sent with sections while it is already off. |
| [8197](../../../foundations/error-codes.md#error-8197) | 400 | ORG_ACCESS_RESTRICTION_NOT_ENABLED - The organisation's accessRestrictionEnabled is false. |
| [8198](../../../foundations/error-codes.md#error-8198) | 400 | SECTIONS_NOT_ALLOWED_WHEN_APPLYING_ORG_SETTINGS - useOrganizationSettings: true was sent together with a non-empty section. |
| [8199](../../../foundations/error-codes.md#error-8199) | 400 | WORKSPACE_SETTINGS_NOT_ENABLED - The workspace follows the organisation, and the request would update it without useOrganizationSettings: false. |
| [8200](../../../foundations/error-codes.md#error-8200) | 400 | SECTIONS_NOT_ALLOWED_WHEN_DISABLING_ACCESS_RESTRICTION - accessRestrictionEnabled: false was sent together with a non-empty section. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |

# Related

- [Organization Management](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
