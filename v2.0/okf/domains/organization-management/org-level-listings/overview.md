---
type: API Group
title: Org-Level Listings
description: "APIs that list, for one organisation, the workspaces the calling user can reach, the dashboards across those workspaces, and the views the user opened most recently."
tags:
  - zoho-analytics
  - rest-api-v2
  - organization-management
  - org-level-listings
  - api-group
api:
  domain: organization-management
  group: org-level-listings
  endpoint_count: 3
  endpoints:
    - operation_id: getOrgWorkspaces
      method: GET
      path: "/restapi/v2/orgs/workspaces"
      doc: "/domains/organization-management/org-level-listings/get-org-workspaces.md"
    - operation_id: getOrgDashboards
      method: GET
      path: "/restapi/v2/orgs/dashboards"
      doc: "/domains/organization-management/org-level-listings/get-org-dashboards.md"
    - operation_id: getOrgRecentItems
      method: GET
      path: "/restapi/v2/orgs/recentitems"
      doc: "/domains/organization-management/org-level-listings/get-org-recent-items.md"
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

This document covers the V2 **Org-Level Listing** REST APIs of Zoho Analytics — the APIs that list, for one organisation, the workspaces the calling user can reach, the dashboards across those workspaces, and the views the user opened most recently.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Org Workspaces](get-org-workspaces.md) | GET | `/restapi/v2/orgs/workspaces` | `getOrgWorkspaces` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Org Dashboards](get-org-dashboards.md) | GET | `/restapi/v2/orgs/dashboards` | `getOrgDashboards` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Org Recent Items](get-org-recent-items.md) | GET | `/restapi/v2/orgs/recentitems` | `getOrgRecentItems` | `ZohoAnalytics.metadata.read` | 200 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What is an "Org-Level Listing" in Zoho Analytics?

An org-level listing answers "what can **I** see in this organisation?" without naming a workspace first. The organisation is chosen with the `ZANALYTICS-ORGID` header; everything else is worked out from the caller's identity. The three listings build on each other: the recent-item listing — and the dashboard listing, unless you name the workspaces yourself with `workspaceIds` — is computed from the workspaces that [Get Org Workspaces](get-org-workspaces.md) would return for the same caller.

| Listing | What it returns | Scope of the result | Paging |
|---------|-----------------|---------------------|--------|
| **Workspaces** | Workspaces of the organisation. | Every active workspace for an Account Admin or Organization Admin; only workspaces shared with the caller for anyone else. [Exceptions](overview.md#visibility-and-access-scoping) apply. | None. |
| **Dashboards** | Dashboards across those workspaces, newest-modified first. | Dashboards the caller may read, in the caller's visible workspaces, or in the workspaces named in `workspaceIds`. | `pageNo`, `recordsPerPage`. |
| **Recent items** | The caller's most recently opened views of any type. | The caller's own history, limited to the caller's visible workspaces. | None; fixed at 20 items. |

> **The single most important behaviour:** the same request returns **different results for different callers**. These APIs never describe the organisation as a whole — they describe the organisation *as seen by the authenticated user*. A short or empty list is not an error and does not mean the organisation is empty. See [Visibility and Access Scoping](overview.md#visibility-and-access-scoping) before using any of these lists as an inventory.

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`). All three APIs use `ZohoAnalytics.metadata.read` — see [OAuth scopes](../../../foundations/oauth-scopes.md).
> - All three APIs are **organisation-scoped** (`/restapi/v2/orgs/...`) and require the `ZANALYTICS-ORGID` header. None has a workspace or view ID in its path.
> - `ZohoAnalytics_Server_URI` depends on the data centre (`analyticsapi.zoho.com`, `.eu`, etc.).
> - **Any user of the organisation may call them**, whatever the role. What a caller sees depends on that role and on what has been shared with them. [Get Org Workspaces](get-org-workspaces.md) and [Get Org Recent Items](get-org-recent-items.md) accept active users only. See [Permission Model](overview.md#permission-model).
> - API-unit cost per call: [Get Org Workspaces](get-org-workspaces.md) 0.1, [Get Org Dashboards](get-org-dashboards.md) 0.1, [Get Org Recent Items](get-org-recent-items.md) 1 (Metadata group).
> - **Client Portal / White Label:** [Get Org Dashboards](get-org-dashboards.md) is disabled on those domains and returns [`7301`](../../../foundations/error-codes.md#error-7301). The other two are allowed, and return only the workspaces enabled for that domain.
> - There is no sort parameter on any of these APIs and none accepts a `criteria` attribute.
> - These APIs are **distinct from** the user-scoped listings (`/restapi/v2/workspaces`, `/restapi/v2/dashboards`), which report across every organisation the caller belongs to and take no `ZANALYTICS-ORGID` header. Those listings are **deprecated**: they answer until March 2027, and the matching SDK methods were removed in 2.10.0. The APIs in this document replace them. The titles in this document carry the word "Org" to keep them apart.

---

# Visibility and Access Scoping

Every API here starts from the same question — "which workspaces can this caller reach in this organisation?" — and then narrows further.

| Caller | Workspaces returned by [Get Org Workspaces](get-org-workspaces.md) |
|--------|----------------------------------------------------|
| Account Admin of the organisation | Every active workspace of the organisation. |
| Organization Admin of the organisation | Every active workspace of the organisation. |
| Any other user | Only the workspaces **shared with** the caller (directly, or by an email address matching the caller's account). Workspaces of the organisation that were not shared with the caller are absent. |
| An Organization Admin or other user whose primary email address is **not verified** | No workspaces — the list is empty. This is a server default. It does not apply to the Account Admin. |

> Workspaces created by certain internal services are not listed for any caller, whatever the role.

**Workspaces are the first filter, views are the second.**

- [Get Org Recent Items](get-org-recent-items.md) works out the caller's workspaces exactly as above and keeps only the history entries from those workspaces; so does [Get Org Dashboards](get-org-dashboards.md) when `workspaceIds` is omitted. When `workspaceIds` is sent, those IDs are used as given — after checking that each one belongs to the organisation — and the view-level access described next still applies.
- [Get Org Dashboards](get-org-dashboards.md) applies **view-level** access: a caller sees a dashboard only if they administer the workspace, have a custom role in it, or it has been shared with them (as a user, group or email) or made public. Account Admins, Organization Admins and the workspace admins see every dashboard in their workspaces.
- [Get Org Recent Items](get-org-recent-items.md) applies **no** view-level check. It reads the caller's own history and keeps the entries whose workspace is visible. See the Notes of that API.

**Access Restrictions can empty or narrow the dashboard list.** When Access Restrictions are active for the organisation ([Security Controls](../security-controls/overview.md)), a caller whose email domain is not a trusted domain for sharing receives an empty dashboard list, and a caller who is barred from public views no longer receives public dashboards.

**Client Portal / White Label.** [Get Org Dashboards](get-org-dashboards.md) is not available on such a domain. The other two lists are further limited to workspaces enabled for that domain.

**Three consequences for integrators:**

1. **Do not use these lists as an inventory.** Only an Account Admin or Organization Admin sees the whole organisation from [Get Org Workspaces](get-org-workspaces.md).
2. **Results are per user.** A response cached for one user must not be served to another.
3. **An empty list is a valid answer.** It means "nothing visible to this caller", not "nothing exists".

---

# Limitations

These are the limits that apply with **default settings**.

| Limitation | Value | Enforced by |
|------------|-------|-------------|
| **Callers** | Active users of the organisation named in `ZANALYTICS-ORGID` ([Get Org Workspaces](get-org-workspaces.md), [Get Org Recent Items](get-org-recent-items.md)); members of it ([Get Org Dashboards](get-org-dashboards.md)). | `7301` |
| **Workspaces in the dashboard scan** | **100** workspaces. Applies to the workspaces the caller can see when `workspaceIds` is omitted, and also to the number of IDs in `workspaceIds`. The limit is a server setting and can be changed per organisation. | `7476` |
| **Dashboards blocked for the organisation** | An organisation can have org-level dashboard listing switched off. | `7430`, `7431` |
| **`workspaceIds` entries** | **0–1,000** IDs, and at most **10,000** characters in all. Duplicates are ignored. | `8547`, `8507` |
| **`pageNo`** | **1–1,000.** | `8544` |
| **`recordsPerPage`** | **1–500.** | `8544` |
| **`searchKey` length** | **100** characters. | `8507` |
| **`CONFIG` length** | **11,000** characters. | `8507` |
| **Recent items returned** | **20**, newest first. Not configurable. | — |
| **Sorting** | None configurable. Workspaces: newest-created first. Dashboards: most recently modified first. Recent items: most recently accessed first. | — |
| **Favourites** | Not covered here. `/restapi/v2/orgs/favorites` is a separate API. | — |

> **Request-format limits are enforced before the request reaches the handler.** A `pageNo` or `recordsPerPage` outside its range, a value of the wrong type, an unknown `CONFIG` key, or an over-long value is refused by the request filter. The codes are listed in the Error Codes table of [Get Org Dashboards](get-org-dashboards.md).

---

# Permission Model

| Caller | May do | Notes |
|--------|--------|-------|
| Account Admin / Organization Admin | All three APIs. | [Get Org Workspaces](get-org-workspaces.md) returns every active workspace, unless an Organization Admin's primary email address is not verified. |
| Any other user of the organisation — Workspace Admin, custom-role user, or a user with items shared with them | All three APIs. | Results are limited to what is shared with, or administered by, the caller. |
| A user who is not an active user of the organisation | Nothing. | [Get Org Workspaces](get-org-workspaces.md) and [Get Org Recent Items](get-org-recent-items.md) refuse the call with `7301`. [Get Org Dashboards](get-org-dashboards.md) refuses a non-member with `7301`, apart from the exception in its Notes. |
| User on a Client Portal / White Label domain | [Get Org Workspaces](get-org-workspaces.md) and [Get Org Recent Items](get-org-recent-items.md). | Limited to workspaces enabled for the domain. [Get Org Dashboards](get-org-dashboards.md) is refused with `7301`. |

---

# API-Specific Notes and Behaviours

## Get Org Workspaces

- **Do not treat the list as an inventory unless the caller is an Account Admin or Organization Admin.**
- **`isDefault` is the caller's own default workspace.**
- **Dependency chain:** Organization ID (Zoho Analytics UI → **Settings → Organisation**) → `ZANALYTICS-ORGID` → Get Org Workspaces.

## Get Org Dashboards

- **A short page is not necessarily the last page.** `hasNextPage` is worked out after duplicates and role-restricted entries are removed, so keep requesting pages while it is `true`.
- **Name the workspaces if you get [`7476`](../../../foundations/error-codes.md#error-7476).** Send `workspaceIds`, at most 100 by default.
- **A bad workspace ID fails the whole call ([`7387`](../../../foundations/error-codes.md#error-7387)).**
- **Dependency chain:** [Get Org Workspaces](get-org-workspaces.md) → Get Org Dashboards.

## Get Org Recent Items

- **Open a recent item defensively.** The list is checked against workspace access, not view access.
- **Dependency chain:** Organization ID (Zoho Analytics UI → **Settings → Organisation**) → `ZANALYTICS-ORGID` → Get Org Recent Items.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Which endpoints return 200** | All three return `200 OK` with the JSON envelope `{"status", "summary", "data"}`. There is no `204`. |
| **Failure responses always carry a body** | `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name, not a localised sentence. |
| **IDs and times are strings** | `workspaceId`, `viewId`, `orgId`, `folderId`, `createdTime`, `lastModifiedTime` and `viewLastAccessedTime` are JSON strings. Times are epoch milliseconds. |
| **Empty array, never a missing key** | `workspaces` and `views` are always present, `[]` when empty. |
| **Per-caller fields** | `isDefault` and `isFavorite` describe the caller, not the object. |
| **Array name `views`** | Used by both [Get Org Dashboards](get-org-dashboards.md) and [Get Org Recent Items](get-org-recent-items.md), but the two entry shapes differ. |
| **Booleans are JSON booleans** | Never strings. |
| **Key order is not guaranteed** | Read by name, not position. |
| **Responses are extensible** | Some builds return additional fields. Ignore unrecognised keys rather than validating against a closed schema. |

---

# Enum and Value Reference

### `viewType` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `Table` | A table. | [Get Org Recent Items](get-org-recent-items.md) only. |
| `Report` | A tabular view. | [Get Org Recent Items](get-org-recent-items.md) only. |
| `AnalysisView` | A chart view. | [Get Org Recent Items](get-org-recent-items.md) only. |
| `Pivot` | A pivot view. | [Get Org Recent Items](get-org-recent-items.md) only. |
| `SummaryView` | A summary view. | [Get Org Recent Items](get-org-recent-items.md) only. |
| `QueryTable` | A query table. | [Get Org Recent Items](get-org-recent-items.md) only. |
| `Dashboard` | A dashboard. | The only value [Get Org Dashboards](get-org-dashboards.md) returns. |
| `PipelineTable` | A pipeline table. | [Get Org Recent Items](get-org-recent-items.md) only. |
| `DataModelObject` | A data model object. | [Get Org Recent Items](get-org-recent-items.md) only. |

> Response only; no API in this document accepts a view type.

---

# CONFIG Attribute Availability by API

| Attribute | Get Org Workspaces | Get Org Dashboards | Get Org Recent Items |
|-----------|---|---|---|
| `workspaceIds` | — | ✔ | — |
| `pageNo` | — | ✔ | — |
| `recordsPerPage` | — | ✔ | — |
| `searchKey` | — | ✔ | — |

> Only [Get Org Dashboards](get-org-dashboards.md) takes a CONFIG.

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7387](../../../foundations/error-codes.md#error-7387) | 400 | DBID_NOT_BELONGS_TO_ZSOID - The workspace does not belong to the organisation in ZANALYTICS-ORGID. |
| [7430](../../../foundations/error-codes.md#error-7430) | 400 | Org-level view listing is blocked for the organisation. This code is reported to the Account Admin. |
| [7431](../../../foundations/error-codes.md#error-7431) | 400 | Org-level view listing is blocked for the organisation. This code is reported to every caller other than the Account Admin. |
| [7476](../../../foundations/error-codes.md#error-7476) | 400 | More workspaces are in scope than the limit allows. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | The ZANALYTICS-ORGID header is missing from a request that requires it. |
| [8084](../../../foundations/error-codes.md#error-8084) | 404 | ORGID_NOT_EXIST - No organisation exists with the given ID. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | MORETHANMAXLENGTH — roleName exceeds 30 characters, or permissions exceeds its size limit. |
| [8516](../../../foundations/error-codes.md#error-8516) | 400 | UNABLETOPARSEDATATYPE — A CONFIG value has the wrong JSON type. |
| [8534](../../../foundations/error-codes.md#error-8534) | 400 | JSONPARSEERROR — CONFIG is not valid JSON. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |
| [8539](../../../foundations/error-codes.md#error-8539) | 400 | CONFIG is sent empty, or a CONFIG value - searchKey, pageNo, recordsPerPage, workspaceIds or one of its entries - is null or an empty or blank string. |
| [8542](../../../foundations/error-codes.md#error-8542) | 400 | CONFIG holds a key other than workspaceIds, pageNo, recordsPerPage and searchKey. |
| [8544](../../../foundations/error-codes.md#error-8544) | 400 | OUT_OF_RANGE - An integer is outside its range: percentileVal outside 0-100, a mergeAxisInfo index outside 0-100. |
| [8547](../../../foundations/error-codes.md#error-8547) | 400 | ARRAYSIZEOUTOFRANGE — selectedColumns is empty or holds more than 300 entries. |

# Related

- [Organization Management](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
