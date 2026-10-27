# Zoho Analytics V2 REST API — Org-Level Listings

This document covers the V2 **Org-Level Listing** REST APIs of Zoho Analytics — the APIs that list, for one organisation, the workspaces the calling user can reach, the dashboards across those workspaces, and the views the user opened most recently.

## What is an "Org-Level Listing" in Zoho Analytics?

An org-level listing answers "what can **I** see in this organisation?" without naming a workspace first. The organisation is chosen with the `ZANALYTICS-ORGID` header; everything else is worked out from the caller's identity. The three listings build on each other: the recent-item listing — and the dashboard listing, unless you name the workspaces yourself with `workspaceIds` — is computed from the workspaces that [Get Org Workspaces](#1-get-org-workspaces) would return for the same caller.

| Listing | What it returns | Scope of the result | Paging |
|---------|-----------------|---------------------|--------|
| **Workspaces** | Workspaces of the organisation. | Every active workspace for an Account Admin or Organization Admin; only workspaces shared with the caller for anyone else. [Exceptions](#visibility-and-access-scoping) apply. | None. |
| **Dashboards** | Dashboards across those workspaces, newest-modified first. | Dashboards the caller may read, in the caller's visible workspaces, or in the workspaces named in `workspaceIds`. | `pageNo`, `recordsPerPage`. |
| **Recent items** | The caller's most recently opened views of any type. | The caller's own history, limited to the caller's visible workspaces. | None; fixed at 20 items. |

> **The single most important behaviour:** the same request returns **different results for different callers**. These APIs never describe the organisation as a whole — they describe the organisation *as seen by the authenticated user*. A short or empty list is not an error and does not mean the organisation is empty. See [Visibility and Access Scoping](#visibility-and-access-scoping) before using any of these lists as an inventory.

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`). All three APIs use `ZohoAnalytics.metadata.read` — see [Appendix B](#appendix-b--oauth-scope-summary).
> - All three APIs are **organisation-scoped** (`/restapi/v2/orgs/...`) and require the `ZANALYTICS-ORGID` header. None has a workspace or view ID in its path.
> - `ZohoAnalytics_Server_URI` depends on the data centre (`analyticsapi.zoho.com`, `.eu`, etc.).
> - **Any user of the organisation may call them**, whatever the role. What a caller sees depends on that role and on what has been shared with them. [Get Org Workspaces](#1-get-org-workspaces) and [Get Org Recent Items](#3-get-org-recent-items) accept active users only. See [Permission Model](#permission-model).
> - API-unit cost per call: [Get Org Workspaces](#1-get-org-workspaces) 0.1, [Get Org Dashboards](#2-get-org-dashboards) 0.1, [Get Org Recent Items](#3-get-org-recent-items) 1 (Metadata group).
> - **Client Portal / White Label:** [Get Org Dashboards](#2-get-org-dashboards) is disabled on those domains and returns `7301`. The other two are allowed, and return only the workspaces enabled for that domain.
> - There is no sort parameter on any of these APIs and none accepts a `criteria` attribute.
> - These APIs are **distinct from** the user-scoped listings (`/restapi/v2/workspaces`, `/restapi/v2/dashboards`), which report across every organisation the caller belongs to and take no `ZANALYTICS-ORGID` header. Those listings are **deprecated**: they answer until March 2027, and the matching SDK methods were removed in 2.10.0. The APIs in this document replace them. The titles in this document carry the word "Org" to keep them apart.

---

## Index

| # | API Name | Method | URL |
|---|----------|--------|-----|
| 1 | [Get Org Workspaces](#1-get-org-workspaces) | GET | `/restapi/v2/orgs/workspaces` |
| 2 | [Get Org Dashboards](#2-get-org-dashboards) | GET | `/restapi/v2/orgs/dashboards` |
| 3 | [Get Org Recent Items](#3-get-org-recent-items) | GET | `/restapi/v2/orgs/recentitems` |

> **Note:** all three are read-only. There is no `POST`, `PUT` or `DELETE` on these paths.

---

## Visibility and Access Scoping

Every API here starts from the same question — "which workspaces can this caller reach in this organisation?" — and then narrows further.

| Caller | Workspaces returned by [Get Org Workspaces](#1-get-org-workspaces) |
|--------|----------------------------------------------------|
| Account Admin of the organisation | Every active workspace of the organisation. |
| Organization Admin of the organisation | Every active workspace of the organisation. |
| Any other user | Only the workspaces **shared with** the caller (directly, or by an email address matching the caller's account). Workspaces of the organisation that were not shared with the caller are absent. |
| An Organization Admin or other user whose primary email address is **not verified** | No workspaces — the list is empty. This is a server default. It does not apply to the Account Admin. |

> Workspaces created by certain internal services are not listed for any caller, whatever the role.

**Workspaces are the first filter, views are the second.**

- [Get Org Recent Items](#3-get-org-recent-items) works out the caller's workspaces exactly as above and keeps only the history entries from those workspaces; so does [Get Org Dashboards](#2-get-org-dashboards) when `workspaceIds` is omitted. When `workspaceIds` is sent, those IDs are used as given — after checking that each one belongs to the organisation — and the view-level access described next still applies.
- [Get Org Dashboards](#2-get-org-dashboards) applies **view-level** access: a caller sees a dashboard only if they administer the workspace, have a custom role in it, or it has been shared with them (as a user, group or email) or made public. Account Admins, Organization Admins and the workspace admins see every dashboard in their workspaces.
- [Get Org Recent Items](#3-get-org-recent-items) applies **no** view-level check. It reads the caller's own history and keeps the entries whose workspace is visible. See the Notes of that API.

**Access Restrictions can empty or narrow the dashboard list.** When Access Restrictions are active for the organisation ([Security Controls](SECURITY_CONTROLS.md)), a caller whose email domain is not a trusted domain for sharing receives an empty dashboard list, and a caller who is barred from public views no longer receives public dashboards.

**Client Portal / White Label.** [Get Org Dashboards](#2-get-org-dashboards) is not available on such a domain. The other two lists are further limited to workspaces enabled for that domain.

**Three consequences for integrators:**

1. **Do not use these lists as an inventory.** Only an Account Admin or Organization Admin sees the whole organisation from [Get Org Workspaces](#1-get-org-workspaces).
2. **Results are per user.** A response cached for one user must not be served to another.
3. **An empty list is a valid answer.** It means "nothing visible to this caller", not "nothing exists".

---

## Limitations

These are the limits that apply with **default settings**.

| Limitation | Value | Enforced by |
|------------|-------|-------------|
| **Callers** | Active users of the organisation named in `ZANALYTICS-ORGID` ([Get Org Workspaces](#1-get-org-workspaces), [Get Org Recent Items](#3-get-org-recent-items)); members of it ([Get Org Dashboards](#2-get-org-dashboards)). | `7301` |
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

> **Request-format limits are enforced before the request reaches the handler.** A `pageNo` or `recordsPerPage` outside its range, a value of the wrong type, an unknown `CONFIG` key, or an over-long value is refused by the request filter. The codes are listed in the Error Codes table of [Get Org Dashboards](#2-get-org-dashboards).

---

## Permission Model

| Caller | May do | Notes |
|--------|--------|-------|
| Account Admin / Organization Admin | All three APIs. | [Get Org Workspaces](#1-get-org-workspaces) returns every active workspace, unless an Organization Admin's primary email address is not verified. |
| Any other user of the organisation — Workspace Admin, custom-role user, or a user with items shared with them | All three APIs. | Results are limited to what is shared with, or administered by, the caller. |
| A user who is not an active user of the organisation | Nothing. | [Get Org Workspaces](#1-get-org-workspaces) and [Get Org Recent Items](#3-get-org-recent-items) refuse the call with `7301`. [Get Org Dashboards](#2-get-org-dashboards) refuses a non-member with `7301`, apart from the exception in its Notes. |
| User on a Client Portal / White Label domain | [Get Org Workspaces](#1-get-org-workspaces) and [Get Org Recent Items](#3-get-org-recent-items). | Limited to workspaces enabled for the domain. [Get Org Dashboards](#2-get-org-dashboards) is refused with `7301`. |

---

## 1. Get Org Workspaces

Returns the workspaces of one organisation that the caller can reach. Supplies the `workspaceId` values used by [Get Org Dashboards](#2-get-org-dashboards) and by every workspace-scoped API.

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/orgs/workspaces` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the organisation whose workspaces are listed. |
| **Permission Required** | The authenticated user must be an active user of the organisation. Account Admins and Organization Admins see every active workspace; other users see only the workspaces shared with them. |

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

### Sample Requests

**Case 1 — List the workspaces visible to the caller**

```http
GET /restapi/v2/orgs/workspaces HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal: request sent through the portal domain (list limited to the portal's workspaces)**

```http
GET /restapi/v2/orgs/workspaces HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Sample Responses

**HTTP 200 OK — Two workspaces, one of them the caller's default**

```json
{
    "status": "success",
    "summary": "Get org workspaces",
    "data": {
        "workspaces": [
            {
                "workspaceId": "137687000271334001",
                "workspaceName": "Sales Analysis",
                "workspaceDesc": "Quarterly sales dashboards",
                "orgId": "700000123456",
                "createdTime": "1718361737000",
                "createdBy": "jane.doe@example.com",
                "isDefault": true
            },
            {
                "workspaceId": "466206000000071000",
                "workspaceName": "Support Metrics",
                "workspaceDesc": "",
                "orgId": "700000123456",
                "createdTime": "1707286805000",
                "createdBy": "jane.doe@example.com",
                "isDefault": false
            }
        ]
    }
}
```

**HTTP 200 OK — Nothing visible to the caller**

```json
{
    "status": "success",
    "summary": "Get org workspaces",
    "data": {
        "workspaces": []
    }
}
```

**HTTP 404 Not Found — No organisation exists with the ID in the header**

```json
{
    "status": "failure",
    "summary": "ORGID_NOT_EXIST",
    "data": {
        "errorCode": 8084,
        "errorMessage": "Organization id 700000999999 is not exist."
    }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get org workspaces"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.workspaces` | JSONArray | The workspaces visible to the caller. **Always present**; `[]` when none. |
| `data.workspaces[].workspaceId` | String | Workspace ID. Returned as a string. |
| `data.workspaces[].workspaceName` | String | Workspace name. |
| `data.workspaces[].workspaceDesc` | String | Workspace description; `""` when none. |
| `data.workspaces[].orgId` | String | ID of the organisation that owns the workspace. |
| `data.workspaces[].createdTime` | String | Creation time as **epoch milliseconds, returned as a string**, for example `"1718361737000"`. |
| `data.workspaces[].createdBy` | String | Email address of the workspace owner. The key is omitted when no address can be resolved. |
| `data.workspaces[].isDefault` | Boolean | `true` when this is the **calling user's** default workspace. It is a per-user setting, not a property of the workspace. At most one entry is `true`, and none is when the caller has no default workspace or the default is in another organisation. |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Read-only and idempotent** | Changes nothing. Repeating the call returns the current list. |
| **Per-caller result** | Account Admins and Organization Admins receive every active workspace. Everyone else receives only workspaces shared with them. Workspaces created by certain internal services are never listed. The same URL and header therefore return different lists for different tokens. |
| **Empty list is not an error** | A user with nothing shared, or an Organization Admin or other user whose primary email address is not verified, receives `"workspaces": []`. |
| **Order** | Newest workspace first, by creation time. There is no sort parameter. |
| **No paging** | The whole list is returned in one response. |
| **`isDefault` belongs to the caller** | Two users see different `isDefault` flags for the same workspace. Do not store it as a workspace attribute. |
| **Ids are strings** | `workspaceId`, `orgId` and `createdTime` are JSON strings. Keep them as strings; do not parse IDs as 32-bit integers. |
| **Client Portal / White Label** | Allowed. The list holds only the workspaces enabled for the requesting domain. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | Organization ID (Zoho Analytics UI → **Settings → Organisation**) → `ZANALYTICS-ORGID` → Get Org Workspaces → `workspaceId` for [Get Org Dashboards](#2-get-org-dashboards) and for every workspace-scoped API. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not an active user of the organisation named in the header. | Use the organisation the user belongs to, or ask an Account Admin to add the user to the organisation. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| 8084 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Read the Organization ID from **Settings → Organisation** in the Zoho Analytics UI. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

---

## 2. Get Org Dashboards

Returns the dashboards of one organisation that the caller can read, across all of the caller's workspaces or across the workspaces named in `workspaceIds`. Most recently modified first, in pages.

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/orgs/dashboards` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the organisation whose dashboards are listed. |
| **Permission Required** | The authenticated user must be a member of the organisation. Only dashboards the user may read are returned. Not available on Client Portal / White Label domains (`7301`). |

### CONFIG Parameters

CONFIG is **optional** for this API. Omit it to list the first 100 dashboards across every workspace the caller can see.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `workspaceIds` | JSONArray of String | No | All workspaces visible to the caller | IDs of the workspaces to list dashboards from. 0–1,000 entries, at most 10,000 characters in all. Duplicates are ignored. Every ID must belong to the organisation in the header (`7387`). The IDs are used as given: they are not checked against the workspaces [Get Org Workspaces](#1-get-org-workspaces) returns for the caller. An empty array behaves like an omitted one. Supplying IDs does **not** bypass view-level access: dashboards the caller may not read are still left out. |
| `pageNo` | Integer | No | `1` | Page to return, `1–1000`. |
| `recordsPerPage` | Integer | No | `100` | Page size, `1–500`. |
| `searchKey` | String | No | None (no filter) | Returns only dashboards whose **name contains** this text. Up to 100 characters. The text is matched as **one phrase**; it is not split on spaces. Leading and trailing spaces are trimmed. An empty or whitespace-only string, or `null`, is refused with `8539`; omit `searchKey` to apply no filter. |

> A `CONFIG` that is not valid JSON, or a `workspaceIds` that is not a JSON array, is refused with `8534`. A key other than the four above is refused with `8542`. A key set to `null` or to an empty or blank string, or a `workspaceIds` entry that is, is refused with `8539`: leave the key out instead.

### Sample Requests

**Case 1 — First page of every dashboard the caller can read**

```http
GET /restapi/v2/orgs/dashboards HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — Two workspaces only, ten per page, page two**

```http
GET /restapi/v2/orgs/dashboards?CONFIG={"workspaceIds":["137687000271334001","466206000000071000"],"pageNo":2,"recordsPerPage":10} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 3 — Search by name**

```http
GET /restapi/v2/orgs/dashboards?CONFIG={"searchKey":"Sales"} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 4 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
GET /restapi/v2/orgs/dashboards HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Sample Responses

**HTTP 200 OK — Two dashboards, more pages available**

```json
{
    "status": "success",
    "summary": "Get dashboards",
    "data": {
        "views": [
            {
                "viewId": "466206000000106002",
                "viewName": "Support Overview",
                "viewDesc": "Open tickets by priority",
                "viewType": "Dashboard",
                "parentViewId": "",
                "folderId": "466206000000071005",
                "createdTime": "1718361737000",
                "createdBy": "jane.doe@example.com",
                "lastModifiedTime": "1720000000000",
                "lastModifiedBy": "jane.doe@example.com",
                "isFavorite": true,
                "sharedBy": "jane.doe@example.com",
                "workspaceId": "466206000000071000",
                "orgId": "700000123456"
            },
            {
                "viewId": "466206000000106003",
                "viewName": "Support Backlog",
                "viewDesc": "",
                "viewType": "Dashboard",
                "parentViewId": "",
                "folderId": "null",
                "createdTime": "1707286805000",
                "createdBy": "jane.doe@example.com",
                "lastModifiedTime": "1719000000000",
                "lastModifiedBy": "john.roe@example.com",
                "isFavorite": false,
                "sharedBy": "jane.doe@example.com",
                "workspaceId": "466206000000071000",
                "orgId": "700000123456"
            }
        ],
        "pageDetails": {
            "pageNo": 1,
            "recordsPerPage": 2,
            "hasNextPage": true
        }
    }
}
```

**HTTP 200 OK — No dashboards visible to the caller**

```json
{
    "status": "success",
    "summary": "Get dashboards",
    "data": {
        "views": [],
        "pageDetails": {
            "pageNo": 1,
            "recordsPerPage": 100,
            "hasNextPage": false
        }
    }
}
```

**HTTP 400 Bad Request — A workspace ID belongs to a different organisation, or does not exist**

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

**HTTP 400 Bad Request — Too many workspaces to scan**

```json
{
    "status": "failure",
    "summary": "ORG_LEVEL_VIEWS_WS_MORE_THAN_ALLOWED_LIMIT",
    "data": {
        "errorCode": 7476,
        "errorMessage": "Workspace count is more than the allowed limit. Kindly specify the workspace id's to get the views."
    }
}
```

**HTTP 403 Forbidden — Request sent through a Client Portal / White Label domain**

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
| `summary` | String | Localised operation summary. `"Get dashboards"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.views` | JSONArray | The dashboards on this page. **Always present**; `[]` when none. The array is named `views` even though every entry is a dashboard. |
| `data.views[].viewId` | String | Dashboard ID. |
| `data.views[].viewName` | String | Dashboard name. |
| `data.views[].viewDesc` | String | Dashboard description; `""` when none. |
| `data.views[].viewType` | String | Always `Dashboard` in this API. See [`viewType` Values](#viewtype-values). |
| `data.views[].parentViewId` | String | ID of the parent view; `""` when the dashboard has no parent. |
| `data.views[].folderId` | String | ID of the folder that holds the dashboard. A dashboard with no folder entry is reported as the string `"null"`. |
| `data.views[].createdTime` | String | Creation time as epoch milliseconds, returned as a string. |
| `data.views[].createdBy` | String | Email address of the dashboard's owner. `""` when the caller is not an active user of the owning organisation. The key is omitted when no address can be resolved. |
| `data.views[].lastModifiedTime` | String | Last modification time as epoch milliseconds, returned as a string. |
| `data.views[].lastModifiedBy` | String | Email address of the user who last modified the dashboard. Follows the same `""` and omission rules as `createdBy`. |
| `data.views[].isFavorite` | Boolean | `true` when **the caller** has marked the dashboard as a favourite. |
| `data.views[].sharedBy` | String | Email address of the user who shared the dashboard with the caller. Follows the same `""` and omission rules as `createdBy`; the key is omitted whenever no address is available for the sharer. |
| `data.views[].workspaceId` | String | ID of the workspace that holds the dashboard. |
| `data.views[].orgId` | String | ID of the organisation that owns the workspace. |
| `data.pageDetails` | JSONObject | Paging information. **Always present.** |
| `data.pageDetails.pageNo` | Integer | The page returned. |
| `data.pageDetails.recordsPerPage` | Integer | The page size used. |
| `data.pageDetails.hasNextPage` | Boolean | `true` when at least one more dashboard exists after this page. |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Read-only and idempotent** | Changes nothing. |
| **Dashboards only** | Only dashboards are returned, whatever the workspace holds. For every other view type use the workspace-level APIs. |
| **Per-caller result** | Visibility follows the caller's permissions; see [Visibility and Access Scoping](#visibility-and-access-scoping). The same request returns different dashboards for different users. |
| **Who may call** | A member of the organisation. A user who is not a member is also admitted when they belong to the same Zoho organisation as the Account Admin; for them the usual visibility rules apply. Everyone else receives `7301`. |
| **Order** | Most recently modified first (the later of the last data change and the last design change). There is no sort parameter. |
| **Paging** | `hasNextPage` is worked out after duplicate entries, and entries a custom role in the workspace does not allow, have been removed from the page. A page can therefore hold fewer than `recordsPerPage` entries, and on such a page `hasNextPage` can be `false` although later pages still hold dashboards. Keep requesting pages while `hasNextPage` is `true`, and do not treat a short page as proof that the list has ended. |
| **Workspace limit** | When `workspaceIds` is omitted, the server first counts the caller's workspaces. More than 100 fails with `7476`; name the workspaces in `workspaceIds` to proceed. The same cap applies to the number of IDs you send. |
| **`workspaceIds` is validated, not filtered** | An ID from another organisation, or one that does not exist, fails the whole request with `7387`. It is not skipped. IDs you send replace the caller's visible-workspace scan: they are not compared with what [Get Org Workspaces](#1-get-org-workspaces) returns, and dashboards the caller may not read are still left out. |
| **Switched off for the organisation** | An organisation can have org-level dashboard listing blocked. The Account Admin receives `7430` (contact support); every other caller receives `7431` (contact the account admin). |
| **`searchKey`** | A substring match on the dashboard name, applied before paging, so `pageDetails` reflects the filtered set. |
| **Email fields are conditional** | `createdBy`, `lastModifiedBy` and `sharedBy` are filled only when the caller is an active user of the owning organisation; otherwise they are `""`. A key is left out when no address can be resolved for it. |
| **`isFavorite` belongs to the caller** | It is not a property of the dashboard. |
| **No `isLive` flag** | The `isLive` field returned for other view types is never sent for dashboards. |
| **Client Portal / White Label** | Disabled; rejected with `7301`. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get Org Workspaces](#1-get-org-workspaces) → `workspaceId` (optional) → Get Org Dashboards → `viewId` and `workspaceId` for the workspace-scoped view APIs. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not a member of the organisation named in the header, or the request came through a Client Portal / White Label domain. | Call from the standard API host as a member of the organisation named in the header. |
| 7387 | `DBID_NOT_BELONGS_TO_ZSOID` — A `workspaceIds` entry does not belong to the organisation in the header, or does not exist. | Take workspace IDs from [Get Org Workspaces](#1-get-org-workspaces) for the same organisation. |
| 7430 | `ORG_LEVEL_VIEWS_NOT_ALLOWED` — Org-level view listing is blocked for the organisation; reported to its Account Admin. | Use the workspace-level APIs, or contact support. |
| 7431 | `ORG_LEVEL_VIEWS_NOT_ALLOWED_WL_USERS` — Org-level view listing is blocked for the organisation; reported to every caller other than the Account Admin. | Use the workspace-level APIs, or contact the account admin. |
| 7476 | `ORG_LEVEL_VIEWS_WS_MORE_THAN_ALLOWED_LIMIT` — More workspaces are in scope than the limit allows. | Send `workspaceIds` listing the workspaces you want, within the limit. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| 8084 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Read the Organization ID from **Settings → Organisation** in the Zoho Analytics UI. |
| 8507 | `MORE_THAN_MAX_LENGTH` — `searchKey` exceeds 100 characters, `workspaceIds` exceeds 10,000 characters, or `CONFIG` exceeds 11,000 characters. | Shorten the value, or send fewer workspace IDs per call. |
| 8516 | `UNABLE_TO_PARSE_DATA_TYPE` — `pageNo` or `recordsPerPage` is not a number. | Send a plain number. |
| 8534 | `JSON_PARSE_ERROR` — `CONFIG` is not valid JSON, or `workspaceIds` is not an array. | Fix the JSON and URL-encode it correctly; send `workspaceIds` as an array of strings. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |
| 8539 | `INVALID_VALUE_NOT_ALLOWED` — `CONFIG` is sent empty, or a `CONFIG` value (`searchKey`, `pageNo`, `recordsPerPage`, `workspaceIds` or one of its entries) is `null` or an empty or blank string. | Leave the key out instead of sending an empty value, and send only non-empty workspace IDs. |
| 8542 | `EXTRA_KEY_FOUND_IN_JSON` — `CONFIG` holds a key other than `workspaceIds`, `pageNo`, `recordsPerPage` and `searchKey`. | Remove the key. |
| 8544 | `OUT_OF_RANGE` — `pageNo` is outside 1–1,000, or `recordsPerPage` is outside 1–500. | Use a value inside the range. |
| 8547 | `ARRAY_SIZE_OUT_OF_RANGE` — `workspaceIds` holds more than 1,000 entries. | Send at most 1,000 IDs — in practice no more than the workspace limit (`7476`). |

---

## 3. Get Org Recent Items

Returns the views the caller opened most recently in one organisation, of any view type, newest first. At most 20 items.

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **URL** | `/restapi/v2/orgs/recentitems` |
| **OAuth Scope** | `ZohoAnalytics.metadata.read` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the organisation whose recent items are listed. |
| **Permission Required** | The authenticated user must be an active user of the organisation. Only the caller's own history is returned. |

> This API has no CONFIG parameter. All inputs are provided via URL path parameters only.

### Sample Requests

**Case 1 — The caller's recent items in one organisation**

```http
GET /restapi/v2/orgs/recentitems HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal: request sent through the portal domain (list limited to the portal's workspaces)**

```http
GET /restapi/v2/orgs/recentitems HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

### Sample Responses

**HTTP 200 OK — Three recent items**

```json
{
    "status": "success",
    "summary": "Get recent views",
    "data": {
        "views": [
            {
                "viewId": "466206000000106002",
                "viewName": "Support Overview",
                "viewType": "Dashboard",
                "workspaceId": "466206000000071000",
                "workspaceName": "Support Metrics",
                "viewLastAccessedTime": "1720100000000"
            },
            {
                "viewId": "137687000006991601",
                "viewName": "Revenue by Region",
                "viewType": "AnalysisView",
                "workspaceId": "137687000271334001",
                "workspaceName": "Sales Analysis",
                "viewLastAccessedTime": "1720090000000"
            },
            {
                "viewId": "466206000000105001",
                "viewName": "Tickets",
                "viewType": "Table",
                "workspaceId": "466206000000071000",
                "workspaceName": "Support Metrics",
                "viewLastAccessedTime": "1720000000000"
            }
        ]
    }
}
```

**HTTP 200 OK — No recent items in the caller's visible workspaces**

```json
{
    "status": "success",
    "summary": "Get recent views",
    "data": {
        "views": []
    }
}
```

**HTTP 404 Not Found — No organisation exists with the ID in the header**

```json
{
    "status": "failure",
    "summary": "ORGID_NOT_EXIST",
    "data": {
        "errorCode": 8084,
        "errorMessage": "Organization id 700000999999 is not exist."
    }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get recent views"` for this API — the same text as the workspace-level recent-views API; the endpoint is told apart by its URL, not by `summary`. |
| `data` | JSONObject | Response payload wrapper. |
| `data.views` | JSONArray | The caller's recent items, newest first. **Always present**; `[]` when none. |
| `data.views[].viewId` | String | View ID. |
| `data.views[].viewName` | String | View name as recorded in the recent-items entry. |
| `data.views[].viewType` | String | The view's type. See [`viewType` Values](#viewtype-values). |
| `data.views[].workspaceId` | String | ID of the workspace that holds the view. |
| `data.views[].workspaceName` | String | Workspace name as recorded in the recent-items entry. |
| `data.views[].viewLastAccessedTime` | String | When the caller last opened the view, as epoch milliseconds returned as a string. |

### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Read-only and idempotent** | Changes nothing. Costs 1 API unit, ten times the other two APIs. |
| **The caller's own history** | Each user has an independent list. The request cannot read another user's recent items. |
| **Workspace-filtered only** | Entries are kept when their workspace is visible to the caller ([Get Org Workspaces](#1-get-org-workspaces)). This API does not re-check view-level access, so an entry can refer to a view the caller can no longer open. Treat the `viewId` as a hint and handle a refusal when you open it. |
| **Fixed size** | At most 20 entries. There is no paging, `limit` or type filter. |
| **All view types** | Tables, reports, dashboards and the other types listed in [`viewType` Values](#viewtype-values) appear together. |
| **Names come from the history entry** | `viewName` and `workspaceName` are stored in the recent-items record; they are not looked up live. |
| **Nothing visible → empty list** | When the caller has no visible workspace in the organisation, the list is `[]`; the organisation's existence is still checked (`8084`). |
| **Client Portal / White Label** | Allowed. Entries are limited to workspaces enabled for the requesting domain. |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | Organization ID (Zoho Analytics UI → **Settings → Organisation**) → `ZANALYTICS-ORGID` → Get Org Recent Items. |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7301 | `SECURITY_NOT_PERMITTED` — The caller is not an active user of the organisation named in the header. | Use the organisation the user belongs to, or ask an Account Admin to add the user to the organisation. |
| 8083 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — The `ZANALYTICS-ORGID` header is missing or empty. | Add the `ZANALYTICS-ORGID` header with your Organization ID. |
| 8084 | `ORGID_NOT_EXIST` — No organisation exists with the given ID. | Read the Organization ID from **Settings → Organisation** in the Zoho Analytics UI. |
| 8535 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

---

## Appendix A – Common HTTP Headers

| Header | Value | Required | Description |
|--------|-------|----------|-------------|
| `Authorization` | `Zoho-oauthtoken <oauth-token>` | **Mandatory** | OAuth 2.0 access token of the calling user. Must carry `ZohoAnalytics.metadata.read` (see [Appendix B](#appendix-b--oauth-scope-summary)). |
| `ZANALYTICS-ORGID` | Organization ID string | **Mandatory** | Organization ID of the organisation to list. Read the Organization ID from **Settings → Organisation** in the Zoho Analytics UI. Missing → `8083`; unknown → `8084`; a caller outside the organisation → `7301`. |
| `Content-Type` | — | Not used | All three are `GET` requests with no body. [Get Org Dashboards](#2-get-org-dashboards) takes its optional CONFIG as the `CONFIG` query parameter. |
| `Host` | `analyticsapi.zoho.com` (or the DC equivalent) | **Mandatory** | [Get Org Dashboards](#2-get-org-dashboards) sent through a Client Portal / White Label domain is rejected with `7301`. |

> **`ZANALYTICS-DEST-ORGID` is not used by any API in this document.**

Example:

```http
GET /restapi/v2/orgs/dashboards?CONFIG={"recordsPerPage":50} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

---

## Appendix B – OAuth Scope Summary

| API | HTTP Method | Scope |
|-----|-------------|-------|
| Get Org Workspaces | GET | `ZohoAnalytics.metadata.read` |
| Get Org Dashboards | GET | `ZohoAnalytics.metadata.read` |
| Get Org Recent Items | GET | `ZohoAnalytics.metadata.read` |

> All three APIs use the `metadata` scope group and need only `read`. None of them can change anything.

---

## Appendix C – API-Specific Notes and Behaviours

### Get Org Workspaces

- **Do not treat the list as an inventory unless the caller is an Account Admin or Organization Admin.**
- **`isDefault` is the caller's own default workspace.**
- **Dependency chain:** Organization ID (Zoho Analytics UI → **Settings → Organisation**) → `ZANALYTICS-ORGID` → Get Org Workspaces.

### Get Org Dashboards

- **A short page is not necessarily the last page.** `hasNextPage` is worked out after duplicates and role-restricted entries are removed, so keep requesting pages while it is `true`.
- **Name the workspaces if you get `7476`.** Send `workspaceIds`, at most 100 by default.
- **A bad workspace ID fails the whole call (`7387`).**
- **Dependency chain:** [Get Org Workspaces](#1-get-org-workspaces) → Get Org Dashboards.

### Get Org Recent Items

- **Open a recent item defensively.** The list is checked against workspace access, not view access.
- **Dependency chain:** Organization ID (Zoho Analytics UI → **Settings → Organisation**) → `ZANALYTICS-ORGID` → Get Org Recent Items.

---

## Appendix D – General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Which endpoints return 200** | All three return `200 OK` with the JSON envelope `{"status", "summary", "data"}`. There is no `204`. |
| **Failure responses always carry a body** | `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name, not a localised sentence. |
| **IDs and times are strings** | `workspaceId`, `viewId`, `orgId`, `folderId`, `createdTime`, `lastModifiedTime` and `viewLastAccessedTime` are JSON strings. Times are epoch milliseconds. |
| **Empty array, never a missing key** | `workspaces` and `views` are always present, `[]` when empty. |
| **Per-caller fields** | `isDefault` and `isFavorite` describe the caller, not the object. |
| **Array name `views`** | Used by both [Get Org Dashboards](#2-get-org-dashboards) and [Get Org Recent Items](#3-get-org-recent-items), but the two entry shapes differ. |
| **Booleans are JSON booleans** | Never strings. |
| **Key order is not guaranteed** | Read by name, not position. |
| **Responses are extensible** | Some builds return additional fields. Ignore unrecognised keys rather than validating against a closed schema. |

---

## Appendix E – Enum and Value Reference

#### `viewType` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `Table` | A table. | [Get Org Recent Items](#3-get-org-recent-items) only. |
| `Report` | A tabular view. | [Get Org Recent Items](#3-get-org-recent-items) only. |
| `AnalysisView` | A chart view. | [Get Org Recent Items](#3-get-org-recent-items) only. |
| `Pivot` | A pivot view. | [Get Org Recent Items](#3-get-org-recent-items) only. |
| `SummaryView` | A summary view. | [Get Org Recent Items](#3-get-org-recent-items) only. |
| `QueryTable` | A query table. | [Get Org Recent Items](#3-get-org-recent-items) only. |
| `Dashboard` | A dashboard. | The only value [Get Org Dashboards](#2-get-org-dashboards) returns. |
| `PipelineTable` | A pipeline table. | [Get Org Recent Items](#3-get-org-recent-items) only. |
| `DataModelObject` | A data model object. | [Get Org Recent Items](#3-get-org-recent-items) only. |

> Response only; no API in this document accepts a view type.

---

## Appendix F – CONFIG Attribute Availability by API

| Attribute | Get Org Workspaces | Get Org Dashboards | Get Org Recent Items |
|-----------|---|---|---|
| `workspaceIds` | — | ✔ | — |
| `pageNo` | — | ✔ | — |
| `recordsPerPage` | — | ✔ | — |
| `searchKey` | — | ✔ | — |

> Only [Get Org Dashboards](#2-get-org-dashboards) takes a CONFIG.
