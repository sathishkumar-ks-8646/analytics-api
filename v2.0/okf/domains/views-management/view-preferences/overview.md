---
type: API Group
title: View Preferences
description: APIs to mark a view as a favorite for the authenticated user and to remove it from the favorites list.
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - view-preferences
  - api-group
api:
  domain: views-management
  group: view-preferences
  endpoint_count: 2
  endpoints:
    - operation_id: addFavoriteView
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/favorite"
      doc: "/domains/views-management/view-preferences/add-favorite-view.md"
    - operation_id: removeFavoriteView
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/favorite"
      doc: "/domains/views-management/view-preferences/remove-favorite-view.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

This document describes the V2 **View Preferences** REST APIs of Zoho Analytics — specifically, marking and unmarking individual views (reports, tables, dashboards, etc.) as favourites for the authenticated user.

> Notes that apply to every API in this document:
> - All requests are authenticated via OAuth (`Authorization: Zoho-oauthtoken <token>`).
> - Both APIs are **workspace-scoped** and require the `ZANALYTICS-ORGID` header.
> - `ZohoAnalytics_Server_URI` depends on the data centre (`analyticsapi.zoho.com`, `.eu`, etc.).
> - Favourite status is **per-user** — marking a view as a favourite only affects the authenticated user's preference. Other users are not affected.
> - Both APIs have **no request body or CONFIG parameter**.
> - Both APIs return **HTTP 204 No Content** on success (empty body).

---

APIs to mark a view as a favorite for the authenticated user and to remove it from the favorites list. The favorite status is stored per user.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Add Favourite View](add-favorite-view.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/favorite` | `addFavoriteView` | `ZohoAnalytics.metadata.update` | 204 |
| [Remove Favourite View](remove-favorite-view.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/favorite` | `removeFavoriteView` | `ZohoAnalytics.metadata.update` | 204 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# Behaviour Notes

| Topic | Detail |
|-------|--------|
| **User-scoped preference** | Favourite status is stored per user (keyed by the authenticated user's ID). Marking or unmarking a view as a favourite does not affect any other user's view of the same resource. |
| **Reflected in listing APIs** | After a successful Add, the `isFavorite` field in listing API responses (e.g., Get All Dashboards, Get Shared Dashboards) returns `true` for the same user. After a Remove, it returns `false` or is absent. |
| **Idempotent operations** | Both APIs are safe to call multiple times. Adding a view that is already a favourite, or removing one that is not, succeeds without error. |
| **Applicable view types** | Any view type that a user can access with Read Only or higher permission can be marked as a favourite: Tables, Analysis Views (charts), Pivot Tables, Summary Views, Dashboards, Query Tables, and others. |
| **No CONFIG parameter** | Neither API accepts a CONFIG request parameter. The only inputs are the URL path parameters `<workspace-id>` and `<view-id>`. |
| **HTTP method choice** | `POST` is used for Add (not `PUT`) because the favourite entry is a new association being created. `DELETE` removes the association. Both use the same URL path with the `/favorite` suffix. |
| **Response** | Both APIs return HTTP 204 No Content with an empty body on success. There is no JSON response envelope for these operations. |

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | The view does not belong to the specified workspace. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |

# Related

- [Views Management](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
