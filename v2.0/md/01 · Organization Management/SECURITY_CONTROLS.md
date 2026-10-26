# Zoho Analytics V2 REST API — Security Controls

This document covers the V2 **Access Restriction** REST APIs of Zoho Analytics — the APIs that read and update the organisation-level and workspace-level controls governing who may receive shared views, whether private links, public views, exports and emailed views are allowed, and which email domains are trusted for each.

## What is an "Access Restriction" in Zoho Analytics?

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

> **The single most important behaviour:** a workspace either follows the organisation or has its **own complete set** of settings — never a mix — and switching a workspace to its own settings does **not** copy the organisation's values. See [Organisation and Workspace Settings Lifecycle](#organisation-and-workspace-settings-lifecycle) before writing any integration that calls [Update Workspace Access Restrictions](#4-update-workspace-access-restrictions).

## How Section Updates Are Validated

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

> **Never PUT a GET response back.** A response from [Get Org Access Restrictions](#1-get-org-access-restrictions) or [Get Workspace Access Restrictions](#3-get-workspace-access-restrictions) reports every attribute of every section, including attributes on features that are disabled. Sending it back verbatim fails whenever a feature is disabled (`8194` for `privateLinks`, `publicViews` or `emailViews`, `8195` for `emailViews` when export is disabled), and the workspace response carries `configurationSource`, which is not a CONFIG attribute. Send only the attributes you intend to change.

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`). The read APIs use `ZohoAnalytics.metadata.read`; the update APIs use `ZohoAnalytics.metadata.update` — see [Appendix B](#appendix-b--oauth-scope-summary).
> - All four APIs are **organisation-scoped** (`/restapi/v2/security-controls/...`) and require the `ZANALYTICS-ORGID` header. The two workspace APIs additionally carry `<workspace-id>` in the path, and the workspace must belong to the organisation named in the header.
> - `ZohoAnalytics_Server_URI` depends on the data centre (`analyticsapi.zoho.com`, `.eu`, etc.).
> - **All four APIs are disabled in Client Portal / White Label request contexts** and return `7301`.
> - **Only Account Admins and Organization Admins may call them.** Workspace Admins and custom-role users are refused with `7301` — see [Permission Model](#permission-model).
> - Each call is registered with 1 API unit (Metadata group).
> - None of these APIs accepts a `criteria` attribute. There is no search, filter, sort or paging parameter; every response is a single small object.
> - IP restriction, trusted email IDs and Client Portal / White Label domain restrictions are **not** configurable through these APIs.

---

## Index

| # | API Name | Method | URL |
|---|----------|--------|-----|
| 1 | [Get Org Access Restrictions](#1-get-org-access-restrictions) | GET | `/restapi/v2/security-controls/access-restrictions` |
| 2 | [Update Org Access Restrictions](#2-update-org-access-restrictions) | PUT | `/restapi/v2/security-controls/access-restrictions` |
| 3 | [Get Workspace Access Restrictions](#3-get-workspace-access-restrictions) | GET | `/restapi/v2/security-controls/workspaces/<workspace-id>/access-restrictions` |
| 4 | [Update Workspace Access Restrictions](#4-update-workspace-access-restrictions) | PUT | `/restapi/v2/security-controls/workspaces/<workspace-id>/access-restrictions` |

> **Note on method overloading:** the read and update APIs of each level share a path and differ only by method. `GET` never changes anything; `PUT` changes live security settings immediately. There is no `POST` or `DELETE`.

---

## Organisation and Workspace Settings Lifecycle

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

1. **Read before you override.** Call [Get Org Access Restrictions](#1-get-org-access-restrictions), then name in the first `useOrganizationSettings: false` request every section whose organisation setting you want to keep: send `enabled` and, for a section with an active domain restriction, `domainRestrictionEnabled: true` with its `trustedDomains`. Do not send domain attributes for a feature the organisation has disabled (`8194`). A bare `{"useOrganizationSettings": false}` leaves the workspace unrestricted.
2. **`configurationSource` tells you which values you are looking at.** On a workspace that follows the organisation, [Get Workspace Access Restrictions](#3-get-workspace-access-restrictions) returns the **organisation's** values, not stored workspace values.
3. **Reverting is reversible.** Setting `useOrganizationSettings: true` does not delete workspace settings; there is no API that deletes them. To make a workspace's own settings take effect again, set `useOrganizationSettings: false` and omit all sections.
4. **Changing the organisation later does not update an overridden workspace.** Once `configurationSource` is `WORKSPACE`, changes to the organisation's sections have no effect on that workspace.

Design integrations so that the organisation's settings are the default, and use workspace overrides only for named exceptions.

---

## Limitations

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

## Permission Model

| Role | May do | Notes |
|------|--------|-------|
| Account Admin / Organization Admin | All four APIs. | The `ZANALYTICS-ORGID` header must name an organisation the caller administers. |
| Workspace Admin | Nothing in this document. | Refused with `7301`, even for a workspace they administer. |
| Custom role, any permission | Nothing in this document. | Refused with `7301`. |
| Any user on a Client Portal / White Label domain | Nothing in this document. | Refused with `7301`; the APIs are disabled on those domains. |

---

## 1. Get Org Access Restrictions

Returns the organisation's access restriction settings: the master switch and the five sections. Feeds [Update Org Access Restrictions](#2-update-org-access-restrictions) and supplies the values to copy when overriding a workspace.

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/security-controls/access-restrictions` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the organisation to read. |
| **Permission Required** | The authenticated user must be an Account Admin or Organization Admin of the organisation. Workspace Admins and custom-role users are refused (`7301`). |

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

### Sample Requests

**Case 1 — Read the organisation's settings**

```http
GET /restapi/v2/security-controls/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
GET /restapi/v2/security-controls/access-restrictions HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Sample Responses

**HTTP 200 OK — Restrictions enabled, private links disabled, domain restrictions on sharing and email**

```json
{
    "status": "success",
    "summary": "Get org access restrictions",
    "data": {
        "accessRestrictionEnabled": true,
        "shareViews": {
            "domainRestrictionEnabled": true,
            "trustedDomains": [
                "example.com",
                "partner.example.org"
            ]
        },
        "privateLinks": {
            "enabled": false,
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        },
        "publicViews": {
            "enabled": true,
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        },
        "exportViews": {
            "enabled": true
        },
        "emailViews": {
            "enabled": true,
            "domainRestrictionEnabled": true,
            "trustedDomains": [
                "example.com"
            ]
        }
    }
}
```

**HTTP 200 OK — Organisation that has never configured access restrictions**

```json
{
    "status": "success",
    "summary": "Get org access restrictions",
    "data": {
        "accessRestrictionEnabled": false,
        "shareViews": {
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        },
        "privateLinks": {
            "enabled": true,
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        },
        "publicViews": {
            "enabled": true,
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        },
        "exportViews": {
            "enabled": true
        },
        "emailViews": {
            "enabled": true,
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        }
    }
}
```

**HTTP 403 Forbidden — Failure paired with Case 2**

```json
{
    "status": "failure",
    "summary": "SECURITY_NOT_PERMITTED",
    "data": {
        "errorCode": 7301,
        "errorMessage": "You (WL_DBAdmin) do not have the permission to do this operation. "
    }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get org access restrictions"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.accessRestrictionEnabled` | Boolean | The master switch. **Always present.** `false` for an organisation that has never configured access restrictions. When `false`, none of the settings below are enforced. |
| `data.shareViews` | JSONObject | Sharing restriction. **Always present.** |
| `data.shareViews.domainRestrictionEnabled` | Boolean | `true` when views can be shared only to users from `trustedDomains`. **Always present.** |
| `data.shareViews.trustedDomains` | JSONArray of String | Trusted domains for sharing. **Always present**; `[]` when none. Returned even when `domainRestrictionEnabled` is `false`. |
| `data.privateLinks` | JSONObject | Private link settings. **Always present.** |
| `data.privateLinks.enabled` | Boolean | `true` when private links can be generated. **Always present.** |
| `data.privateLinks.domainRestrictionEnabled` | Boolean | `true` when private links admit only users from `trustedDomains`. **Always present.** |
| `data.privateLinks.trustedDomains` | JSONArray of String | Trusted domains for private links. **Always present**; `[]` when none. |
| `data.publicViews` | JSONObject | Public view settings. **Always present.** |
| `data.publicViews.enabled` | Boolean | `true` when views can be made public. **Always present.** |
| `data.publicViews.domainRestrictionEnabled` | Boolean | `true` when public views admit only users from `trustedDomains`. **Always present.** |
| `data.publicViews.trustedDomains` | JSONArray of String | Trusted domains for public views. **Always present**; `[]` when none. |
| `data.exportViews` | JSONObject | Export settings. **Always present.** |
| `data.exportViews.enabled` | Boolean | `true` when views and data can be exported. **Always present.** |
| `data.emailViews` | JSONObject | Email view settings. **Always present.** |
| `data.emailViews.enabled` | Boolean | `true` when views can be emailed. **Always present.** Reports `false` after export has been disabled. |
| `data.emailViews.domainRestrictionEnabled` | Boolean | `true` when emails can go only to `trustedDomains`. **Always present.** |
| `data.emailViews.trustedDomains` | JSONArray of String | Trusted domains for email. **Always present**; `[]` when none. |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Read-only and idempotent** | Changes nothing. Repeating the call returns the current state. |
| **All sections, always** | Every section and every attribute is returned on every call, including attributes of disabled features. There is no way to request a subset. |
| **Stored values are returned even when not enforced** | With `accessRestrictionEnabled: false`, the sections still show their stored values. Read the master switch first. |
| **Domain order is not guaranteed** | Compare `trustedDomains` as sets. |
| **Never-configured organisation** | Returns the second sample above — not an error. |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Organization Info and Settings](ORG_INFO_AND_SETTINGS.md) → `ZANALYTICS-ORGID` → Get Org Access Restrictions → current values for [Update Org Access Restrictions](#2-update-org-access-restrictions). |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| 8084 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

---

## 2. Update Org Access Restrictions

Switches the organisation's access restrictions on or off and updates any of the five sections. Returns no body. Read the current state first with [Get Org Access Restrictions](#1-get-org-access-restrictions).

| Attribute | Value |
|-----------|-------|
| **Method** | PUT |
| **URL** | `/restapi/v2/security-controls/access-restrictions` |
| **OAuth Scope** | `ZohoAnalytics.metadata.update` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the organisation to update. |
| **Permission Required** | The authenticated user must be an Account Admin or Organization Admin of the organisation. Workspace Admins and custom-role users are refused (`7301`). |

### CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `accessRestrictionEnabled` | Boolean | No* | Unchanged | Master switch for the organisation. `false` stops enforcement everywhere, for the organisation and every workspace, without deleting any setting. Cannot be combined with sections when set to `false` (`8200`). While the switch is off, sections are accepted only if this attribute is `true` in the same request (`8196`). |
| `shareViews` | JSONObject | No* | Unchanged | Sharing restriction. See [`shareViews` Fields](#shareviews-fields). |
| `privateLinks` | JSONObject | No* | Unchanged | Private link settings. See [`privateLinks` Fields](#privatelinks-fields). |
| `publicViews` | JSONObject | No* | Unchanged | Public view settings. See [`publicViews` Fields](#publicviews-fields). |
| `exportViews` | JSONObject | No* | Unchanged | Export settings. Setting `enabled` to `false` also disables email views. See [`exportViews` Fields](#exportviews-fields). |
| `emailViews` | JSONObject | No* | Unchanged | Email view settings. Present at all while export is disabled → `8195`. See [`emailViews` Fields](#emailviews-fields). |

\* At least one of the six attributes must be present, and a section must contain at least one attribute to count; otherwise error `8080`. Cross-attribute rules are in [How Section Updates Are Validated](#how-section-updates-are-validated).

> `useOrganizationSettings` and `configurationSource` are workspace-level concepts and are not CONFIG attributes of this API.

#### `shareViews` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `domainRestrictionEnabled` | Boolean | No | Unchanged | `true` allows sharing of views only to users from `trustedDomains`. Turning it on requires at least one trusted domain, sent now or already stored (`8193`). |
| `trustedDomains` | JSONArray of String | No | Unchanged | Complete list of trusted domains, 0–100 entries, each a domain such as `example.com`. **Replaces** the stored list. See [How Section Updates Are Validated](#how-section-updates-are-validated) for `8192` and `8193`. |

#### `privateLinks` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `enabled` | Boolean | No | Unchanged | `false` stops private links from being generated. Domain attributes cannot be changed while private links are disabled (`8194`), except to switch the restriction off and clear the list in the same request. |
| `domainRestrictionEnabled` | Boolean | No | Unchanged | `true` makes private links prompt for login and admit only users from `trustedDomains`. Same list requirements as in `shareViews`. |
| `trustedDomains` | JSONArray of String | No | Unchanged | Complete list of trusted domains, 0–100 entries. **Replaces** the stored list. |

#### `publicViews` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `enabled` | Boolean | No | Unchanged | `false` stops views from being made public. Domain attributes cannot be changed while public views are disabled (`8194`), except to switch the restriction off and clear the list in the same request. |
| `domainRestrictionEnabled` | Boolean | No | Unchanged | `true` makes public views prompt for login and admit only users from `trustedDomains`. Same list requirements as in `shareViews`. |
| `trustedDomains` | JSONArray of String | No | Unchanged | Complete list of trusted domains, 0–100 entries. **Replaces** the stored list. |

#### `exportViews` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `enabled` | Boolean | **Yes** | — | `false` disables exporting of views and data **and** disables email views. `true` re-enables export but does **not** re-enable email views. `exportViews` has no other attribute, so an empty `exportViews` object is rejected. |

#### `emailViews` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `enabled` | Boolean | No | Unchanged | `false` stops views from being emailed. Cannot be `true` in the same request that disables export (`8195`). |
| `domainRestrictionEnabled` | Boolean | No | Unchanged | `true` limits email recipients to `trustedDomains`. Same list requirements as in `shareViews`. |
| `trustedDomains` | JSONArray of String | No | Unchanged | Complete list of trusted domains, 0–100 entries. **Replaces** the stored list. |

### Sample Requests

**Case 1 — Switch access restrictions on, change nothing else**

```http
PUT /restapi/v2/security-controls/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "accessRestrictionEnabled": true
}
```

**Case 2 — Configure several sections at once**

```http
PUT /restapi/v2/security-controls/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "shareViews": {
        "domainRestrictionEnabled": true,
        "trustedDomains": ["example.com", "partner.example.org"]
    },
    "privateLinks": {
        "enabled": false
    },
    "exportViews": {
        "enabled": true
    },
    "emailViews": {
        "enabled": true,
        "domainRestrictionEnabled": true,
        "trustedDomains": ["example.com"]
    }
}
```

**Case 3 — Disable access restrictions and change a section in the same request (rejected)**

```http
PUT /restapi/v2/security-controls/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "accessRestrictionEnabled": false,
    "publicViews": {
        "enabled": false
    }
}
```

### Sample Responses

**HTTP 204 No Content — Cases 1 and 2. No response body is returned on success.**

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — Failure paired with Case 3**

```json
{
    "status": "failure",
    "summary": "SECTIONS_NOT_ALLOWED_WHEN_DISABLING_ACCESS_RESTRICTION",
    "data": {
        "errorCode": 8200,
        "errorMessage": "Other settings updates are not allowed while disabling access restriction"
    }
}
```

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success is 204 with no body** | The change is committed before the response is sent. Call [Get Org Access Restrictions](#1-get-org-access-restrictions) to read it back. |
| **Idempotent** | Sending the same CONFIG twice leaves the same state and returns `204` both times. |
| **Partial update** | Omitted attributes keep their stored value. **Nothing clears on omission.** |
| **All-or-nothing** | The request runs in one transaction. A validation failure in any section, including the last, discards the whole request. |
| **Domain lists replace, not merge** | See [How Section Updates Are Validated](#how-section-updates-are-validated). Resend every domain you want to keep. |
| **Master switch off blocks section edits** | While `accessRestrictionEnabled` is `false`, a request with sections but without `accessRestrictionEnabled: true` is rejected (`8196`). Enable and configure in a single request, or enable first. |
| **Disabling the master switch is exclusive** | `accessRestrictionEnabled: false` cannot share a request with any non-empty section (`8200`). |
| **Empty section objects** | `"privateLinks": {}` changes nothing and does not count as a change for the `8080` check, but still passes through validation. |
| **Stored settings survive the master switch** | Turning the switch off retains every section value; turning it on again re-applies them. |
| **Workspace overrides are unaffected** | Changes here do not alter workspaces whose `configurationSource` is `WORKSPACE`. |
| **No dry run** | There is no validate-only mode. Settings take effect on commit. |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Responses are extensible** | Ignore unrecognised keys on error bodies rather than validating against a closed schema. |
| **Dependency chain** | [Organization Info and Settings](ORG_INFO_AND_SETTINGS.md) → `ZANALYTICS-ORGID` → [Get Org Access Restrictions](#1-get-org-access-restrictions) → Update Org Access Restrictions. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation. |
| 8077 | `EMPTY_JSON_CONFIGURATION` — `CONFIG` is present but empty. | Send a JSON object in `CONFIG`. |
| 8080 | `INVALID_JSON_CONFIGURATION` — `CONFIG` is not valid JSON, or it contains neither `accessRestrictionEnabled` nor a non-empty section. | Send valid JSON with at least one attribute to change. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| 8084 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| 8192 | `TRUSTED_DOMAINS_WITHOUT_DOMAIN_RESTRICTION` — `trustedDomains` was sent for a section whose domain restriction is off or is being switched off. | Send `domainRestrictionEnabled: true` with the list, or send `domainRestrictionEnabled: false` with `trustedDomains: []` to clear it. |
| 8193 | `TRUSTED_DOMAINS_EMPTY` — The domain restriction is on, or being switched on, but the section has no trusted domains. | Send at least one domain in `trustedDomains`, or switch the restriction off. |
| 8194 | `DOMAIN_RESTRICTION_NOT_ALLOWED_WHEN_DISABLED` — Domain attributes were sent for `privateLinks`, `publicViews` or `emailViews` while that feature is disabled or is being disabled. | Enable the feature in the same request, or remove the domain attributes. |
| 8195 | `EMAIL_NOT_ALLOWED_WHEN_EXPORT_DISABLED` — `emailViews` was sent while export is disabled or is being disabled, and email views would stay enabled. | Enable export in the same request, or send `emailViews: {"enabled": false}` when disabling export. |
| 8196 | `ACCESS_RESTRICTION_DISABLED` — Access restriction is off for the organisation and the request carries sections without turning it on, including `accessRestrictionEnabled: false` sent with sections while it is already off. | Include `accessRestrictionEnabled: true` in the same request. |
| 8200 | `SECTIONS_NOT_ALLOWED_WHEN_DISABLING_ACCESS_RESTRICTION` — `accessRestrictionEnabled: false` was sent together with a non-empty section. | Send `accessRestrictionEnabled: false` on its own. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.update`. |

---

## 3. Get Workspace Access Restrictions

Returns the access restriction settings in effect for one workspace and whether they come from the organisation or from the workspace. Feeds [Update Workspace Access Restrictions](#4-update-workspace-access-restrictions).

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/security-controls/workspaces/<workspace-id>/access-restrictions` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the organisation that owns the workspace. |
| **Permission Required** | The authenticated user must be an Account Admin or Organization Admin of the organisation. Workspace Admins of the workspace and custom-role users are refused (`7301`). |

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

### Sample Requests

**Case 1 — Read a workspace's effective settings**

```http
GET /restapi/v2/security-controls/workspaces/137687000271334001/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Workspace that belongs to a different organisation (rejected)**

```http
GET /restapi/v2/security-controls/workspaces/137687000271339999/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Sample Responses

**HTTP 200 OK — Workspace that follows the organisation (`configurationSource` is `ORG`)**

```json
{
    "status": "success",
    "summary": "Get workspace access restrictions",
    "data": {
        "accessRestrictionEnabled": true,
        "configurationSource": "ORG",
        "shareViews": {
            "domainRestrictionEnabled": true,
            "trustedDomains": [
                "example.com",
                "partner.example.org"
            ]
        },
        "privateLinks": {
            "enabled": false,
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        },
        "publicViews": {
            "enabled": true,
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        },
        "exportViews": {
            "enabled": true
        },
        "emailViews": {
            "enabled": true,
            "domainRestrictionEnabled": true,
            "trustedDomains": [
                "example.com"
            ]
        }
    }
}
```

**HTTP 200 OK — Workspace with its own settings (`configurationSource` is `WORKSPACE`)**

```json
{
    "status": "success",
    "summary": "Get workspace access restrictions",
    "data": {
        "accessRestrictionEnabled": true,
        "configurationSource": "WORKSPACE",
        "shareViews": {
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        },
        "privateLinks": {
            "enabled": true,
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        },
        "publicViews": {
            "enabled": false,
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        },
        "exportViews": {
            "enabled": false
        },
        "emailViews": {
            "enabled": false,
            "domainRestrictionEnabled": false,
            "trustedDomains": []
        }
    }
}
```

**HTTP 400 Bad Request — Failure paired with Case 2**

```json
{
    "status": "failure",
    "summary": "DBID_NOT_BELONGS_TO_ZSOID",
    "data": {
        "errorCode": 7387,
        "errorMessage": "Workspaces(s) does not belongs to current Organization"
    }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get workspace access restrictions"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.accessRestrictionEnabled` | Boolean | The **organisation's** master switch, not a workspace setting. **Always present.** When `false`, nothing below is enforced. |
| `data.configurationSource` | String (enum) | Where the values below come from. **Always present.** See [`configurationSource` Values](#configurationsource-values). |
| `data.shareViews` | JSONObject | Sharing restriction in effect. **Always present.** Fields as in [Get Org Access Restrictions](#1-get-org-access-restrictions). |
| `data.privateLinks` | JSONObject | Private link settings in effect. **Always present.** |
| `data.publicViews` | JSONObject | Public view settings in effect. **Always present.** |
| `data.exportViews` | JSONObject | Export settings in effect. **Always present.** |
| `data.emailViews` | JSONObject | Email view settings in effect. **Always present.** |

Every section has the same attributes as in [Get Org Access Restrictions](#1-get-org-access-restrictions): `shareViews` carries `domainRestrictionEnabled` and `trustedDomains`; `privateLinks`, `publicViews` and `emailViews` carry `enabled`, `domainRestrictionEnabled` and `trustedDomains`; `exportViews` carries `enabled`. All are **always present**; `trustedDomains` is `[]` when empty.

#### `configurationSource` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `ORG` | The workspace follows the organisation. The sections hold the **organisation's** values. | Also returned for a workspace that has never been configured. |
| `WORKSPACE` | The workspace has its own settings. The sections hold the **workspace's** values. | Set only by [Update Workspace Access Restrictions](#4-update-workspace-access-restrictions) with `useOrganizationSettings: false`. |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Read-only and idempotent** | Changes nothing. |
| **Effective values, not stored values** | When `configurationSource` is `ORG`, any values previously stored for the workspace are ignored and **not** shown. They reappear only after the workspace is switched back to `WORKSPACE`. |
| **Available while the master switch is off** | Succeeds when `accessRestrictionEnabled` is `false`; the values it returns are not enforced. |
| **Workspace must belong to the organisation** | A workspace ID from another organisation is rejected with `7387`, not `404`. A non-existent ID gets the same error. |
| **Round-trip warning** | Do not send this response back to [Update Workspace Access Restrictions](#4-update-workspace-access-restrictions). See [How Section Updates Are Validated](#how-section-updates-are-validated). |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Workspace Operations](../03%20%C2%B7%20Workspace%20Management/WORKSPACE_OPERATIONS.md) → `<workspace-id>` → Get Workspace Access Restrictions → `configurationSource` and current values for [Update Workspace Access Restrictions](#4-update-workspace-access-restrictions). |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation. |
| 7387 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not exist in the organisation named in `ZANALYTICS-ORGID`. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches the organisation that owns it. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| 8084 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

---

## 4. Update Workspace Access Restrictions

Switches one workspace between following the organisation and having its own settings, and updates the workspace's own sections. Returns no body. Read the current state first with [Get Workspace Access Restrictions](#3-get-workspace-access-restrictions), and read [Organisation and Workspace Settings Lifecycle](#organisation-and-workspace-settings-lifecycle) before the first override.

| Attribute | Value |
|-----------|-------|
| **Method** | PUT |
| **URL** | `/restapi/v2/security-controls/workspaces/<workspace-id>/access-restrictions` |
| **OAuth Scope** | `ZohoAnalytics.metadata.update` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the organisation that owns the workspace. |
| **Permission Required** | The authenticated user must be an Account Admin or Organization Admin of the organisation. Workspace Admins of the workspace and custom-role users are refused (`7301`). The organisation's `accessRestrictionEnabled` must be `true` (`8197`). |

### CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `useOrganizationSettings` | Boolean | No* | Current mode | `false` gives the workspace its own settings; `true` makes it follow the organisation. When omitted, the workspace's current mode is kept — which means omitting it on a workspace that follows the organisation is the same as sending `true` (`8199` if sections are present). `true` cannot be combined with sections (`8198`). Setting `true` keeps the workspace's own values but ignores them. |
| `shareViews` | JSONObject | No* | Unchanged | Sharing restriction. See [`shareViews` Fields](#shareviews-fields-1). |
| `privateLinks` | JSONObject | No* | Unchanged | Private link settings. See [`privateLinks` Fields](#privatelinks-fields-1). |
| `publicViews` | JSONObject | No* | Unchanged | Public view settings. See [`publicViews` Fields](#publicviews-fields-1). |
| `exportViews` | JSONObject | No* | Unchanged | Export settings. Setting `enabled` to `false` also disables email views. See [`exportViews` Fields](#exportviews-fields-1). |
| `emailViews` | JSONObject | No* | Unchanged | Email view settings. Present at all while export is disabled → `8195`. See [`emailViews` Fields](#emailviews-fields-1). |

\* At least one of the six attributes must be present, and a section must contain at least one attribute to count; otherwise error `8080`. The check applies only to a workspace that follows the organisation; on a workspace that already has its own settings, an empty-but-valid `CONFIG` such as `{}` is accepted and changes nothing. Sections are accepted only when the workspace has, or is being given, its own settings.

> `accessRestrictionEnabled` is the organisation's master switch and is not a CONFIG attribute of this API. `configurationSource` appears in the response of [Get Workspace Access Restrictions](#3-get-workspace-access-restrictions) only and is not a CONFIG attribute.

#### `shareViews` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `domainRestrictionEnabled` | Boolean | No | Unchanged | `true` allows sharing of views in this workspace only to users from `trustedDomains`. Turning it on requires at least one trusted domain, sent now or already stored for the workspace (`8193`). |
| `trustedDomains` | JSONArray of String | No | Unchanged | Complete list of trusted domains, 0–100 entries, each a domain such as `example.com`. **Replaces** the workspace's stored list; the organisation's list is never copied or merged. See [How Section Updates Are Validated](#how-section-updates-are-validated) for `8192` and `8193`. |

#### `privateLinks` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `enabled` | Boolean | No | Unchanged | `false` stops private links from being generated in this workspace. Domain attributes cannot be changed while private links are disabled (`8194`), except to switch the restriction off and clear the list in the same request. |
| `domainRestrictionEnabled` | Boolean | No | Unchanged | `true` makes private links prompt for login and admit only users from `trustedDomains`. Same list requirements as in `shareViews`. |
| `trustedDomains` | JSONArray of String | No | Unchanged | Complete list of trusted domains, 0–100 entries. **Replaces** the workspace's stored list. |

#### `publicViews` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `enabled` | Boolean | No | Unchanged | `false` stops views in this workspace from being made public. Domain attributes cannot be changed while public views are disabled (`8194`), except to switch the restriction off and clear the list in the same request. |
| `domainRestrictionEnabled` | Boolean | No | Unchanged | `true` makes public views prompt for login and admit only users from `trustedDomains`. Same list requirements as in `shareViews`. |
| `trustedDomains` | JSONArray of String | No | Unchanged | Complete list of trusted domains, 0–100 entries. **Replaces** the workspace's stored list. |

#### `exportViews` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `enabled` | Boolean | **Yes** | — | `false` disables exporting of views and data in this workspace **and** disables email views. `true` re-enables export but does **not** re-enable email views. `exportViews` has no other attribute, so an empty `exportViews` object is rejected. |

#### `emailViews` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `enabled` | Boolean | No | Unchanged | `false` stops views in this workspace from being emailed. Cannot be `true` in the same request that disables export (`8195`). |
| `domainRestrictionEnabled` | Boolean | No | Unchanged | `true` limits email recipients to `trustedDomains`. Same list requirements as in `shareViews`. |
| `trustedDomains` | JSONArray of String | No | Unchanged | Complete list of trusted domains, 0–100 entries. **Replaces** the workspace's stored list. |

### Sample Requests

**Case 1 — Give the workspace its own settings, naming the sections explicitly**

```http
PUT /restapi/v2/security-controls/workspaces/137687000271334001/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "useOrganizationSettings": false,
    "shareViews": {
        "domainRestrictionEnabled": true,
        "trustedDomains": ["example.com", "partner.example.org"]
    },
    "privateLinks": {
        "enabled": false
    },
    "publicViews": {
        "enabled": false
    },
    "exportViews": {
        "enabled": true
    },
    "emailViews": {
        "enabled": true,
        "domainRestrictionEnabled": true,
        "trustedDomains": ["example.com"]
    }
}
```

**Case 2 — Update one section on a workspace that already has its own settings**

```http
PUT /restapi/v2/security-controls/workspaces/137687000271334001/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "exportViews": {
        "enabled": false
    },
    "emailViews": {
        "enabled": false
    }
}
```

**Case 3 — Return the workspace to the organisation's settings**

```http
PUT /restapi/v2/security-controls/workspaces/137687000271334001/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "useOrganizationSettings": true
}
```

**Case 4 — Sections sent to a workspace that follows the organisation, without `useOrganizationSettings: false` (rejected)**

```http
PUT /restapi/v2/security-controls/workspaces/137687000271334001/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "publicViews": {
        "enabled": false
    }
}
```

### Sample Responses

**HTTP 204 No Content — Cases 1, 2 and 3. No response body is returned on success.**

```
HTTP/1.1 204 No Content
```

**HTTP 400 Bad Request — Failure paired with Case 4**

```json
{
    "status": "failure",
    "summary": "WORKSPACE_SETTINGS_NOT_ENABLED",
    "data": {
        "errorCode": 8199,
        "errorMessage": "Workspace-level access restriction is not enabled for the given workspace"
    }
}
```

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Success is 204 with no body** | The change is committed before the response is sent. Call [Get Workspace Access Restrictions](#3-get-workspace-access-restrictions) to read it back. |
| **Idempotent** | Sending the same CONFIG twice leaves the same state. |
| **Check order** | Caller role (`7301`) → workspace ownership (`7387`) → organisation master switch (`8197`) → empty request (`8080`) → sections without an override (`8199`) → `useOrganizationSettings: true` with sections (`8198`) → per-section rules (`8192`–`8195`). |
| **Requires the organisation master switch** | If `accessRestrictionEnabled` is `false` for the organisation, every request fails with `8197`, including `useOrganizationSettings: true`. Enable it with [Update Org Access Restrictions](#2-update-org-access-restrictions) first. |
| **First override starts from defaults** | Switching a workspace that follows the organisation to `useOrganizationSettings: false` does not copy the organisation's sections. Unnamed sections start allowed and unrestricted; named sections inherit at most the organisation's flag values, never its `trustedDomains`. See [Organisation and Workspace Settings Lifecycle](#organisation-and-workspace-settings-lifecycle). |
| **Sections without the switch are rejected** | A workspace that follows the organisation cannot receive sections unless the same request sets `useOrganizationSettings: false` (`8199`). |
| **Reverting keeps workspace values** | `useOrganizationSettings: true` keeps the workspace's own values, ignores them, and cannot be sent with sections (`8198`). |
| **Partial update** | Omitted attributes keep their stored value. **Nothing clears on omission.** |
| **All-or-nothing** | One transaction; a validation failure in any section discards the whole request, including the mode switch. |
| **Domain lists replace, not merge** | See [How Section Updates Are Validated](#how-section-updates-are-validated). |
| **Organisation changes do not propagate** | A workspace with `configurationSource` `WORKSPACE` ignores later changes to the organisation's sections. |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Responses are extensible** | Ignore unrecognised keys on error bodies rather than validating against a closed schema. |
| **Dependency chain** | [Workspace Operations](../03%20%C2%B7%20Workspace%20Management/WORKSPACE_OPERATIONS.md) → `<workspace-id>` → [Get Workspace Access Restrictions](#3-get-workspace-access-restrictions) → Update Workspace Access Restrictions. For the first override, also [Get Org Access Restrictions](#1-get-org-access-restrictions) for the values to copy. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not an Account Admin or Organization Admin, or the request came through a Client Portal / White Label domain. | Call from the standard API host as an Account Admin or Organization Admin of the organisation. |
| 7387 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not exist in the organisation named in `ZANALYTICS-ORGID`. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches the organisation that owns it. |
| 8077 | `EMPTY_JSON_CONFIGURATION` — `CONFIG` is present but empty. | Send a JSON object in `CONFIG`. |
| 8080 | `INVALID_JSON_CONFIGURATION` — `CONFIG` is not valid JSON, or the workspace follows the organisation and the request has neither `useOrganizationSettings` nor a non-empty section. | Send valid JSON with at least one attribute to change. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| 8084 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Use the `orgId` returned by the organisation listing API. |
| 8192 | `TRUSTED_DOMAINS_WITHOUT_DOMAIN_RESTRICTION` — `trustedDomains` was sent for a section whose domain restriction is off or is being switched off. | Send `domainRestrictionEnabled: true` with the list, or send `domainRestrictionEnabled: false` with `trustedDomains: []` to clear it. |
| 8193 | `TRUSTED_DOMAINS_EMPTY` — The domain restriction is on, or being switched on, but the section has no trusted domains. | Send at least one domain in `trustedDomains`, or switch the restriction off. |
| 8194 | `DOMAIN_RESTRICTION_NOT_ALLOWED_WHEN_DISABLED` — Domain attributes were sent for `privateLinks`, `publicViews` or `emailViews` while that feature is disabled or is being disabled. | Enable the feature in the same request, or remove the domain attributes. |
| 8195 | `EMAIL_NOT_ALLOWED_WHEN_EXPORT_DISABLED` — `emailViews` was sent while export is disabled or is being disabled, and email views would stay enabled. | Enable export in the same request, or send `emailViews: {"enabled": false}` when disabling export. |
| 8197 | `ORG_ACCESS_RESTRICTION_NOT_ENABLED` — The organisation's `accessRestrictionEnabled` is `false`. | Enable access restrictions for the organisation with [Update Org Access Restrictions](#2-update-org-access-restrictions), then retry. |
| 8198 | `SECTIONS_NOT_ALLOWED_WHEN_APPLYING_ORG_SETTINGS` — `useOrganizationSettings: true` was sent together with a non-empty section. | Send `useOrganizationSettings: true` on its own. |
| 8199 | `WORKSPACE_SETTINGS_NOT_ENABLED` — The workspace follows the organisation, and the request would update it without `useOrganizationSettings: false`. | Send `useOrganizationSettings: false` in the same request to give the workspace its own settings. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.update`. |

---

## Appendix A – Common HTTP Headers

| Header | Value | Required | Description |
|--------|-------|----------|-------------|
| `Authorization` | `Zoho-oauthtoken <oauth-token>` | **Mandatory** | OAuth 2.0 access token of the calling user. Must carry the scope matching the operation (see [Appendix B](#appendix-b--oauth-scope-summary)). |
| `ZANALYTICS-ORGID` | Organization ID string | **Mandatory** | Organization ID of the organisation whose settings are read or changed. Obtainable from listing API responses as the `orgId` field. Missing → `8083`; unknown → `8084`. |
| `Content-Type` | `application/x-www-form-urlencoded` | Conditional | Required only for the APIs that send a CONFIG body: [Update Org Access Restrictions](#2-update-org-access-restrictions) and [Update Workspace Access Restrictions](#4-update-workspace-access-restrictions). The two GET APIs send no payload. |
| `Host` | `analyticsapi.zoho.com` (or the DC equivalent) | **Mandatory** | Requests sent through a Client Portal / White Label domain are rejected with `7301`. |

> **`ZANALYTICS-DEST-ORGID` is not used by any API in this document.**

Example:

```http
PUT /restapi/v2/security-controls/access-restrictions HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"accessRestrictionEnabled":true}
```

---

## Appendix B – OAuth Scope Summary

| API | HTTP Method | Scope |
|-----|-------------|-------|
| Get Org Access Restrictions | GET | `ZohoAnalytics.metadata.read` |
| Update Org Access Restrictions | PUT | `ZohoAnalytics.metadata.update` |
| Get Workspace Access Restrictions | GET | `ZohoAnalytics.metadata.read` |
| Update Workspace Access Restrictions | PUT | `ZohoAnalytics.metadata.update` |

> All four APIs use the `metadata` scope group, and the update APIs need `update`, not `create`. A token that holds only `ZohoAnalytics.metadata.read` can read both levels but cannot change either; an integration that must both read and write needs both scopes at consent time.

---

## Appendix C – API-Specific Notes and Behaviours

### Get Org Access Restrictions

- **Treat `accessRestrictionEnabled` as the gate.** The section values are reported whether or not they are enforced.
- **Use it as the source of values for a workspace override.** The first `useOrganizationSettings: false` request does not copy them for you.
- **Dependency chain:** [Organization Info and Settings](ORG_INFO_AND_SETTINGS.md) → `ZANALYTICS-ORGID` → Get Org Access Restrictions.

### Update Org Access Restrictions

- **Send only what you change.** Verbatim GET payloads fail whenever a feature is disabled (`8194`, `8195`).
- **Disabling export implies disabling email views.** `emailViews: {"enabled": false}` is accepted alongside it; an `emailViews` that would leave email views enabled is rejected (`8195`).
- **To switch everything off, send `accessRestrictionEnabled: false` alone.** Stored section values remain and apply again when you switch it back on.
- **Dependency chain:** [Get Org Access Restrictions](#1-get-org-access-restrictions) → Update Org Access Restrictions → read it back with Get Org Access Restrictions.

### Get Workspace Access Restrictions

- **Check `configurationSource` before interpreting the sections.** `ORG` means they are the organisation's values.
- **Dependency chain:** [Workspace Operations](../03%20%C2%B7%20Workspace%20Management/WORKSPACE_OPERATIONS.md) → `<workspace-id>` → Get Workspace Access Restrictions.

### Update Workspace Access Restrictions

- **The organisation master switch gates everything.** With it off, even a revert to `useOrganizationSettings: true` fails (`8197`).
- **Name every section on the first override.** Unnamed sections start unrestricted.
- **Dependency chain:** [Get Workspace Access Restrictions](#3-get-workspace-access-restrictions) → Update Workspace Access Restrictions → read it back with Get Workspace Access Restrictions.

---

## Appendix D – General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Which endpoints return 204** | [Update Org Access Restrictions](#2-update-org-access-restrictions) and [Update Workspace Access Restrictions](#4-update-workspace-access-restrictions) return `204 No Content` with no body. The two GET APIs return `200 OK`. |
| **Failure responses always carry a body** | Even for the 204 APIs, errors return `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name, not a localised sentence. |
| **No IDs in the responses** | The GET APIs return settings only; neither echoes the organisation or workspace ID. |
| **Booleans are JSON booleans** | Every flag is `true` or `false`, never a string. |
| **Empty array, never a missing key** | Every `trustedDomains` is always present, `[]` when empty. |
| **Key order is not guaranteed** | Read by name, not position. |
| **`exportViews` has only `enabled`** | It carries no domain attributes in requests or responses. |
| **Responses are extensible** | Some builds return additional fields. Ignore unrecognised keys rather than validating against a closed schema. |

---

## Appendix E – Enum and Value Reference

#### `configurationSource` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `ORG` | The workspace follows the organisation; the response holds the organisation's values. | Response only. |
| `WORKSPACE` | The workspace has its own settings; the response holds the workspace's values. | Response only. Set by `useOrganizationSettings: false`. |

---

## Appendix F – CONFIG Attribute Availability by API

| Attribute | Update Org Access Restrictions | Update Workspace Access Restrictions |
|-----------|---|---|
| `accessRestrictionEnabled` | ✔ | — |
| `useOrganizationSettings` | — | ✔ |
| `shareViews` | ✔ | ✔ |
| `privateLinks` | ✔ | ✔ |
| `publicViews` | ✔ | ✔ |
| `exportViews` | ✔ | ✔ |
| `emailViews` | ✔ | ✔ |
