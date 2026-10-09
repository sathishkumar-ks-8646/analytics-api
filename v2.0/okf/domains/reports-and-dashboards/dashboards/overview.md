---
type: API Group
title: Dashboards
description: "APIs for listing dashboards accessible to a user, and for creating, reading and updating dashboards inside a workspace."
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
sources:
  - id: openapi-spec
    resource: "/references/openapi/reports-dashboards-grouped-api.json"
    title: OpenAPI 3 specification - reports-dashboards-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

This document describes the V2 **Dashboards** REST APIs of Zoho Analytics — covering dashboard listing, creation, metadata retrieval, and updates.
APIs are documented with URL, method, OAuth scope, permissions, sample requests/responses, and error codes.

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`).
> - `ZohoAnalytics_Server_URI` depends on the data center (`analyticsapi.zoho.com`, `.eu`, etc.).
> - **Get All Dashboards, Get Owned Dashboards, and Get Shared Dashboards** (the listing APIs) operate at the **user service level** — they return dashboards across all organizations the caller belongs to. No `ZANALYTICS-ORGID` header is required.
> - **Create Dashboard, Get Dashboard Metadata, and Update Dashboard** (the workspace-scoped APIs) operate on a specific workspace. The `ZANALYTICS-ORGID` header is **mandatory**.
> - The three listing APIs are user-scoped — the OAuth token must be issued with user-level scope.
> - Get All Dashboards and Get Owned Dashboards are disabled on custom domains. Get Shared Dashboards works on custom domains. The three workspace-scoped APIs are accessible on custom domains, subject to permission checks.

---

APIs for listing dashboards accessible to a user, and for creating, reading and updating dashboards inside a workspace.

The module splits into two families that behave differently.

- **Listing APIs** - Get All Dashboards, Get Owned Dashboards and Get Shared Dashboards. These operate at user service level and return dashboards across every organization the caller belongs to. No `ZANALYTICS-ORGID` header is needed, and the OAuth token must be issued with user level scope.
- **Workspace-scoped APIs** - Create Dashboard, Get Dashboard Metadata and Update Dashboard. These operate on one workspace and require the `ZANALYTICS-ORGID` header.

## Common request conventions

| Header | Value | Required |
|---|---|---|
| `Authorization` | `Zoho-oauthtoken <oauth-token>` | Mandatory for every API |
| `ZANALYTICS-ORGID` | Organization ID owning the workspace | Workspace-scoped APIs only |
| `Content-Type` | `application/x-www-form-urlencoded` | Create and Update only |

Get Shared Dashboards works on custom domains. Get All Dashboards and Get Owned Dashboards are disabled on custom domains. The workspace-scoped APIs are reachable on custom domains subject to additional permission checks.

## OAuth scopes

| API | Method | Scope |
|---|---|---|
| Get All Dashboards | GET | `ZohoAnalytics.metadata.read` |
| Get Owned Dashboards | GET | `ZohoAnalytics.metadata.read` |
| Get Shared Dashboards | GET | `ZohoAnalytics.metadata.read` |
| Create Dashboard | POST | `ZohoAnalytics.modeling.create` |
| Get Dashboard Metadata | GET | `ZohoAnalytics.modeling.read` |
| Update Dashboard | PUT | `ZohoAnalytics.modeling.update` |

## Response envelope

- **status** - `success` or `failure`.
- **summary** - human readable description of the completed operation.
- **data.ownedViews** and **data.sharedViews** - Get All Dashboards only.
- **data.views** - Get Owned Dashboards and Get Shared Dashboards; a single list, owned-only or shared-only depending on the endpoint.
- **data.dashboardId** and **data.displayName** - Create Dashboard only.
- **data.dashboardConfig** - Get Dashboard Metadata only.

`viewId`, `workspaceId` and `orgId` are returned as strings even though the underlying values are long integers. `createdTime` and `lastModifiedTime` are epoch timestamps in milliseconds, as strings - divide by 1000 for epoch seconds. `sharedBy` is present on every entry, empty in owned items and populated with an email in shared ones. `isFavorite` is user specific and reflects the requesting user.

`dashboardConfig.objId`, `data.dashboardId` and `viewId` are the same value under three different names.

## Update replaces sections wholesale

Update Dashboard does not merge. When `layout`, `themes` or `settings` is included, every stored row for that section is deleted and exactly what was sent is stored in its place. Sending `{"settings":{"enableGlobalUF":"true"}}` reverts every other setting to its system default. A section left out of the CONFIG is not touched.

**Read-modify-write**

1. `GET .../metadata?CONFIG={"include":"settings"}` to fetch just the section being changed.
2. Merge the change into the returned object, keeping every key that came back.
3. `PUT` the complete section.

**Adding a layout card without losing the others**

The layout is a complete card map keyed by index string. Fetch it with `include=layout`, append the new card under the next sequential key, and PUT the whole map back.

**Cloning a dashboard**

Fetch the full metadata, take `layout`, `themes` and `settings` from `dashboardConfig`, drop `objId`, `displayName` and `description` (they are read-only in the response and are not valid Create CONFIG fields other than `displayName`/`description`, which must be supplied fresh), then POST with a new `displayName`. The `viewName` values inside `layout` must match views that exist in the target workspace.

## Behaviour worth knowing before the first call

| Case | Behaviour | Recommendation |
|---|---|---|
| Partial `settings` on Update | Only the keys sent are stored; the rest revert to defaults. | Send the full settings object fetched via GET. |
| Section omitted on Update | Left unchanged. | Include only the sections being replaced. |
| `layoutType` grid preset (1-4) | The server auto-injects a USERFILTERS card at index `"1"` and rearranges view cards into columns, renumbering the input. | Omit `layoutType`, or send 0, for free form layouts; confirm with a GET afterwards. |
| `viewName` in a layout card | Identifies an analysis view by display name, not ID. A renamed or deleted view renders as a broken card. | Verify view names through the Reports APIs first. |
| Resetting the theme | `{"themes":{"default":"true"}}` clears all theme customization in one call. | Use it to undo theme changes without knowing the original values. |
| Tabbed dashboards | Get Dashboard Metadata and Update Dashboard fail with error 8102. | Check the dashboard type first. |
| `include` with several sections | `include=themes,layout` returns both sections but omits `objId`, `displayName` and `description`. | Use `include=all` when identity fields are needed, such as for clone workflows. |
| Scalar types in the response | Theme and settings scalars come back as strings even where the CONFIG accepts numbers. | Coerce before comparing, and send back the form the CONFIG documents. |

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get All Dashboards](get-dashboards.md) | GET | `/restapi/v2/dashboards` | `getDashboards` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Owned Dashboards](get-owned-dashboards.md) | GET | `/restapi/v2/dashboards/owned` | `getOwnedDashboards` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Shared Dashboards](get-shared-dashboards.md) | GET | `/restapi/v2/dashboards/shared` | `getSharedDashboards` | `ZohoAnalytics.metadata.read` | 200 |
| [Create Dashboard](create-dashboard.md) | POST | `/restapi/v2/workspaces/{workspace-id}/dashboards` | `createDashboard` | `ZohoAnalytics.modeling.create` | 200 |
| [Get Dashboard Metadata](get-dashboard-metadata.md) | GET | `/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}/metadata` | `getDashboardMetadata` | `ZohoAnalytics.modeling.read` | 200 |
| [Update Dashboard](update-dashboard.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/dashboards/{dashboard-id}` | `updateDashboard` | `ZohoAnalytics.modeling.update` | 204 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# Response Payload Notes

| Field | Description |
|-------|-------------|
| `status` | `success` or `failure`. Standard Zoho Analytics V2 response envelope. |
| `summary` | Human-readable description of the completed operation. |
| `data.ownedViews` | (Get All Dashboards only) Dashboards created/owned by the requesting user. |
| `data.sharedViews` | (Get All Dashboards only) Dashboards shared with the requesting user by others. |
| `data.views` | (Get Owned Dashboards and Get Shared Dashboards) Single unified list — owned-only or shared-only based on the endpoint. |
| `viewId` | Returned as a **string** even though the underlying value is a long integer. |
| `workspaceId` | Returned as a **string**. Use this as `<workspace-id>` in workspace-scoped API calls. |
| `orgId` | Returned as a **string**. Corresponds to the `ZANALYTICS-ORGID` header value in workspace-scoped APIs. |
| `createdTime` / `lastModifiedTime` | Epoch timestamps in **milliseconds** as strings. Divide by 1000 to convert to Unix epoch seconds. |
| `sharedBy` | Present in all dashboard entries; empty string (`""`) in owned items, populated with email in shared items. |
| `isFavorite` | User-specific: `true` if the **requesting user** has marked this dashboard as a favorite. |
| `data.dashboardId` | (Create API only) ID of the newly created dashboard, returned as a string. |
| `data.displayName` | (Create API only) Display name of the newly created dashboard as stored. |
| `data.dashboardConfig` | (Get Metadata API only) Wrapper object containing full dashboard configuration. |
| `data.dashboardConfig.objId` | Dashboard ID as a string. |
| `data.dashboardConfig.themes` | Object describing the active visual theme (type, background, fonts, cards, palette, effects). |
| `data.dashboardConfig.settings` | Object describing dashboard behaviour settings (export, drill-down, UF, etc.). |
| `data.dashboardConfig.layout` | Object where each key is a card index string (`"1"`, `"2"`, …) and each value is a card configuration. |

> **Custom domain note:** Get Shared Dashboards works on custom domains. Get All Dashboards and Get Owned Dashboards are disabled on custom domains. Create Dashboard, Get Dashboard Metadata, and Update Dashboard are accessible on custom domains but subject to additional permission checks.

---

# Working with Get, Create, and Update Together

## Why Get Dashboard Metadata Before Update

The **Update Dashboard** API performs a **full section replacement** — not a merge. When you include `layout`, `themes`, or `settings` in an Update request, the server:

1. Deletes **all** stored rows for that section
2. Stores exactly what you sent

If you only send `{"settings": {"enableGlobalUF": "true"}}`, every other setting reverts to the system default. To avoid unintended data loss, always **fetch first, modify, then update**.

---

## Workflow 1 — Read-Modify-Write (Safe Update)

**Step 1: Fetch only the section you need to change**

Use `include` to avoid fetching the full config when you only need one section:

```http
GET /restapi/v2/workspaces/320873000000001001/dashboards/320873000000597763/metadata?CONFIG={"include":"settings"}
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 320873000000000001
```

Response — only the stored (non-default) settings are returned:

```json
{
  "data": {
    "dashboardConfig": {
      "settings": {
        "smartAlignCharts": "true",
        "fitToWidth": "true",
        "allowDrillDown": "true",
        "allowExport": { "pdf": "true", "excel": "true", "csv": "true", "html": "true", "image": "true", "zohoSheet": "true" }
      }
    }
  }
}
```

**Step 2: Modify the desired key(s) in the returned object**

Add `enableGlobalUF` to the settings object from the response:

```json
{
  "smartAlignCharts": "true",
  "fitToWidth": "true",
  "allowDrillDown": "true",
  "enableGlobalUF": "true",
  "allowExport": { "pdf": "true", "excel": "true", "csv": "true", "html": "true", "image": "true", "zohoSheet": "true" }
}
```

**Step 3: Send the complete modified object in the Update**

```http
PUT /restapi/v2/workspaces/320873000000001001/dashboards/320873000000597763
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 320873000000000001
Content-Type: application/x-www-form-urlencoded

CONFIG={"settings":{"smartAlignCharts":"true","fitToWidth":"true","allowDrillDown":"true","enableGlobalUF":"true","allowExport":{"pdf":"true","excel":"true","csv":"true","html":"true","image":"true","zohoSheet":"true"}}}
```

> Apply the same pattern for `themes` and `layout` — always send the full section back, not just the changed keys.

---

## Workflow 2 — Layout Update Without Losing Cards

The layout is a complete card map. Sending a partial layout (e.g., only 2 cards) replaces the entire layout with those 2 cards. To add a card without removing others:

**Step 1: Fetch the current layout**

```http
GET .../metadata?CONFIG={"include":"layout"}
```

**Step 2: Append the new card to the returned layout object**

The card index key must be the next sequential number. Existing card indices from the GET response are preserved:

```json
{
  "1": { "type": "USERFILTERS", "width": 80, "height": 3, "left": 0, "top": 0 },
  "2": { "type": "VIEW", "width": 40, "height": 20, "left": 0, "top": 3, "viewName": "Sales_Report" },
  "3": { "type": "VIEW", "width": 40, "height": 20, "left": 40, "top": 3, "viewName": "Revenue_Chart" }
}
```

**Step 3: PUT the full layout back**

```http
PUT .../dashboards/320873000000597763
...
CONFIG={"layout":{"1":{"type":"USERFILTERS","width":80,"height":3,"left":0,"top":0},"2":{"type":"VIEW","width":40,"height":20,"left":0,"top":3,"viewName":"Sales_Report"},"3":{"type":"VIEW","width":40,"height":20,"left":40,"top":3,"viewName":"Revenue_Chart"}}}
```

---

## Workflow 3 — Cloning a Dashboard (Get → Create)

Use the full metadata of an existing dashboard as a template for a new one:

**Step 1: Fetch full metadata of the source dashboard**

```http
GET /restapi/v2/workspaces/320873000000001001/dashboards/320873000000597763/metadata
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 320873000000000001
```

**Step 2: Take `layout`, `themes`, `settings` from the response `dashboardConfig` object**

Strip out `objId`, `displayName`, `description` — these are read-only fields in the GET response and are not valid CONFIG fields for Create.

**Step 3: POST to Create Dashboard with a new `displayName`**

```http
POST /restapi/v2/workspaces/320873000000001001/dashboards
Content-Type: application/x-www-form-urlencoded

CONFIG={
  "displayName": "Sales Overview - Copy",
  "description": "Cloned from Sales Overview dashboard",
  "layout": { <layout from GET response> },
  "themes": { <themes from GET response> },
  "settings": { <settings from GET response> }
}
```

> **Note:** `viewName` values inside `layout` must match the display names of existing analysis views in the **target workspace**. If cloning across workspaces, update the `viewName` values accordingly before posting.

---

## Special Cases and Caveats

| Case | Behaviour | Recommendation |
|------|-----------|----------------|
| **Partial settings in Update** | If you send `settings` with only some keys, all other settings revert to system defaults. Only explicitly-set values are stored. | Always send the full settings object (fetched via GET) with your changes merged in. |
| **Omitting a section in Update** | If `layout`, `themes`, or `settings` is absent from the CONFIG, that section is **not changed**. Safe to omit sections you are not modifying. | Only include the section(s) you intend to replace. |
| **`layoutType` preset in Create/Update** | When `layoutType` is `1`–`4` (grid preset), the server **auto-injects** a USERFILTERS card at position `"1"` and rearranges view cards into columns. Your input card order may be renumbered. | Omit `layoutType` (or set to `0`) for free-form layouts. Use GET after Create/Update to confirm the final stored layout. |
| **`viewName` in layout cards** | Identifies an analysis view by its **display name** (not ID). If the referenced view is renamed or deleted, the card will show as broken in the dashboard. | Always verify view names using the Reports API before sending layout. |
| **Reset theme to defaults** | Send `{"themes": {"default": "true"}}` in Update to clear all custom theme settings and restore the system default theme. | Use this to undo theme customizations in a single call without needing to know the original values. |
| **`objId` in GET response** | The `dashboardConfig.objId` field is the dashboard ID. Use it directly as `<dashboard-id>` in the Update URL. | `objId` = `dashboardId` (Create response) = `viewId` (listing API response). Same value, different field names. |
| **Tabbed dashboards** | Error `8102` is returned if you call Get Metadata or Update on a tabbed dashboard. These are not supported via the V2 API. | Use the UI or check the dashboard type before calling these APIs. |
| **`include` with comma-separated values** | Requesting `include=themes,layout` returns both sections without `objId`, `displayName`, or `description`. These top-level identity fields are only included when `include=all` (or omitted). | Always use `include=all` (default) when you need identity fields for clone workflows. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7111](../../../foundations/error-codes.md#error-7111) | 400 | A view with the given viewName already exists in this workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [8072](../../../foundations/error-codes.md#error-8072) | 400 | The target object is not a valid dashboard. |
| [8102](../../../foundations/error-codes.md#error-8102) | 400 | Dashboard view type not supported for this operation. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | Invalid value for attribute. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |

# Related

- [Reports & Dashboards](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
