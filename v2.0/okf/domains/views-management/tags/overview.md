---
type: API Group
title: Tags
description: "APIs to create, update, delete and list the tags of a workspace, and to attach those tags to views."
tags:
  - zoho-analytics
  - rest-api-v2
  - views-management
  - tags
  - api-group
api:
  domain: views-management
  group: tags
  endpoint_count: 10
  endpoints:
    - operation_id: getTags
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/tags"
      doc: "/domains/views-management/tags/get-tags.md"
    - operation_id: getTaggedViews
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views"
      doc: "/domains/views-management/tags/get-tagged-views.md"
    - operation_id: getViewTags
      method: GET
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags"
      doc: "/domains/views-management/tags/get-view-tags.md"
    - operation_id: createTag
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/tags"
      doc: "/domains/views-management/tags/create-tag.md"
    - operation_id: updateTag
      method: PUT
      path: "/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}"
      doc: "/domains/views-management/tags/update-tag.md"
    - operation_id: deleteTag
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}"
      doc: "/domains/views-management/tags/delete-tag.md"
    - operation_id: addTagToViews
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views"
      doc: "/domains/views-management/tags/add-tag-to-views.md"
    - operation_id: removeTagFromViews
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views"
      doc: "/domains/views-management/tags/remove-tag-from-views.md"
    - operation_id: addTagsToView
      method: POST
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags"
      doc: "/domains/views-management/tags/add-tags-to-view.md"
    - operation_id: removeTagsFromView
      method: DELETE
      path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags"
      doc: "/domains/views-management/tags/remove-tags-from-view.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/views-management-grouped-api.json"
    title: OpenAPI 3 specification - views-management-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

This document covers the ten **Tag** REST APIs of Zoho Analytics — the APIs that create the coloured labels a workspace uses to organise its views, and that attach those labels to tables, reports, dashboards, and every other view type.

APIs to create, update, delete and list the tags of a workspace, and to attach those tags to views. A tag is a workspace-scoped label with a name and a hex colour code, used to organise tables, reports, dashboards and other views. Tags carry no permissions - attaching one neither grants nor restricts access. The tag-side APIs attach or detach one tag across many views and require workspace administration; the view-side APIs attach or detach many tags on a single view and are also open to the view owner and to users with Edit Design permission. A view can carry at most 10 tags.

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Tags List](get-tags.md) | GET | `/restapi/v2/workspaces/{workspace-id}/tags` | `getTags` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Tagged Views](get-tagged-views.md) | GET | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views` | `getTaggedViews` | `ZohoAnalytics.metadata.read` | 200 |
| [Get View Tags](get-view-tags.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags` | `getViewTags` | `ZohoAnalytics.metadata.read` | 200 |
| [Create Tag](create-tag.md) | POST | `/restapi/v2/workspaces/{workspace-id}/tags` | `createTag` | `ZohoAnalytics.modeling.create` | 200 |
| [Update Tag](update-tag.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}` | `updateTag` | `ZohoAnalytics.modeling.update` | 204 |
| [Delete Tag](delete-tag.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}` | `deleteTag` | `ZohoAnalytics.modeling.delete` | 204 |
| [Add Tag To Multiple Views](add-tag-to-views.md) | POST | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views` | `addTagToViews` | `ZohoAnalytics.modeling.create` | 204 |
| [Remove Tag From Multiple Views](remove-tag-from-views.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/tags/{tag-id}/views` | `removeTagFromViews` | `ZohoAnalytics.modeling.delete` | 204 |
| [Add Multiple Tags To View](add-tags-to-view.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags` | `addTagsToView` | `ZohoAnalytics.modeling.create` | 204 |
| [Remove Multiple Tags From View](remove-tags-from-view.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/tags` | `removeTagsFromView` | `ZohoAnalytics.modeling.delete` | 204 |

All endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](../../../foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](../../../foundations/request-conventions.md)).

# What a tag is

A tag is a **workspace-scoped label** with two properties: a `name` and a `colorCode`. On its own it does nothing. Its value comes from being **associated** with views, so that a workspace with hundreds of objects can be filtered down to "everything tagged Finance" or "everything tagged Deprecated".

That gives the family two halves that are easy to confuse:

| | Tag lifecycle | Tag ↔ view association |
|---|---|---|
| **What it manages** | The tag object itself | The link between a tag and a view |
| **APIs** | [Create Tag](create-tag.md), [Update Tag](update-tag.md), [Delete Tag](delete-tag.md), [Get Tags List](get-tags.md) | The remaining six |
| **Deleting the tag** | Removes the tag everywhere | — |
| **Removing an association** | — | Leaves both the tag and the view intact |

Associations are a plain many-to-many relationship: one tag can label many views, and one view can carry up to ten tags.

---

# How the Ten APIs Relate

[Create Tag](create-tag.md) is the only source of a `tagId`, and it is the ID every other tag-side API needs. Everything else either reads the graph or edits one edge of it.

```
          4. Create Tag  ──►  data.tagId
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
   5. Update Tag            6. Delete Tag          ┌── association ──┐
   (rename / recolour)      (removes the tag       │                 │
                             AND every one of      ▼                 ▼
                             its associations)  7. Add Tag      9. Add Multiple
                                                To Multiple      Tags To View
                                                Views            (view side)
                                                (tag side)            │
                                                   │                  │
                                                   ▼                  ▼
                                                8. Remove Tag    10. Remove Multiple
                                                From Multiple        Tags From View
                                                Views
        ┌──────────────────── read back ────────────────────┐
        ▼                          ▼                        ▼
  1. Get Tags List        2. Get Tagged Views        3. Get View Tags
  (every tag in the       (which views carry         (which tags a
   workspace)              this tag)                  view carries)
```

| Relationship | Detail |
|--------------|--------|
| **`tagId` has exactly one origin** | [Create Tag](create-tag.md) returns it as `data.tagId`. [Get Tags List](get-tags.md) and [Get View Tags](get-view-tags.md) return it afterwards as `tags[].id`. Every other tag-side API takes it in the path or in `tagIds`. |
| **`viewId` comes from outside this family** | No tag API creates a view. Get view IDs from [Get View List](../view-operations/get-views.md), or read them back from [Get Tagged Views](get-tagged-views.md) as `views[].id`. |
| **The tag-side and view-side association APIs edit the same table from opposite ends** | [Add Tag To Multiple Views](add-tag-to-views.md) attaches **one tag to many views**; [Add Multiple Tags To View](add-tags-to-view.md) attaches **many tags to one view**. The resulting associations are indistinguishable. Their **permission rules differ** — see [The Two Sides of an Association](overview.md#the-two-sides-of-an-association). |
| **The two read-back APIs are inverses** | [Get Tagged Views](get-tagged-views.md) answers "which views carry tag X"; [Get View Tags](get-view-tags.md) answers "which tags does view Y carry". Together they let you walk the association graph in either direction. |
| **[Delete Tag](delete-tag.md) cascades; the removal APIs do not** | Deleting a tag removes the tag *and* every association it had. [Remove Tag From Multiple Views](remove-tag-from-views.md) removes associations only — the tag survives and can be re-attached. |
| **[Update Tag](update-tag.md) never touches associations** | Renaming or recolouring a tag leaves every association in place. Views tagged before the rename are still tagged after it. |
| **The ten-tag ceiling is enforced on both add paths** | Both [Add Tag To Multiple Views](add-tag-to-views.md) and [Add Multiple Tags To View](add-tags-to-view.md) validate it before writing anything. See [Limitations](overview.md#limitations). |
| **Verification is always a read-back** | Six of the ten APIs return `204` with no body. The only way to confirm what changed is [Get Tags List](get-tags.md), [Get Tagged Views](get-tagged-views.md), or [Get View Tags](get-view-tags.md). |
| **Tags are metadata, not data** | They never affect rows, sharing, or permissions. A tag is a label for organising a workspace; it does not grant or restrict access to anything. |

## Typical sequences

**Create a tag and apply it across a set of views**

```
Create Tag {"name":"Finance","colorCode":"#1da043"}  →  data.tagId
   → Add Tag To Multiple Views {"viewIds":[...]}     →  204
   → Get Tagged Views                                →  confirm the list
```

**Label one dashboard with several existing tags**

```
Get Tags List                                        →  tags[].id
   → Add Multiple Tags To View {"tagIds":[...]}      →  204
   → Get View Tags                                   →  confirm
```

**Retire a tag completely**

```
Delete Tag   →  204   (tag and all its associations disappear together)
   → Get Tags List  →  the tag is gone
```

**Strip one view back to no tags at all**

```
Remove Multiple Tags From View {"dissociateAll": true}  →  204
   → Get View Tags  →  {"tags": []}
```

---

# The Two Sides of an Association

The tag-side and view-side association APIs write the same association table, but they are **not** interchangeable, because they check different permissions.

| | Tag side — [Add Tag To Multiple Views](add-tag-to-views.md) / [Remove Tag From Multiple Views](remove-tag-from-views.md) | View side — [Add Multiple Tags To View](add-tags-to-view.md) / [Remove Multiple Tags From View](remove-tags-from-view.md) |
|---|---|---|
| **Path** | `/tags/<tag-id>/views` | `/views/<view-id>/tags` |
| **Fixed end** | One tag | One view |
| **CONFIG carries** | `viewIds` | `tagIds` |
| **Who may call it** | An Account Admin or Organization Admin, or a Workspace Admin | Any of those, **or** the View Owner, **or** any user with Edit Design permission on the view |
| **Batch shape** | Many views at once | Many tags at once |

The consequence in practice: **a View Owner who is not a Workspace Admin can tag their own view, but cannot use the tag-side APIs at all** — even to attach a tag to that very same view. If your integration runs as a non-admin user, it must use the view-side APIs.

> Read-only users are blocked from all four association APIs regardless of any other permission, with error [`8180`](../../../foundations/error-codes.md#error-8180).

---

# Limitations

These are the limits that apply with **default settings**.

| Limitation | Value | Enforced by |
|------------|-------|-------------|
| **Tags per view** | **10.** Counted across all tags on the view, not per request. | `8181` |
| **`viewIds` per request** | **1–1000** entries. | `8547` |
| **`tagIds` per request** | **1–1000** entries. | `8547` |
| **Tag name length** | **100** characters. | `8507` |
| **Tag name uniqueness** | A tag name must be unique **within the workspace**. | `8174` |
| **`colorCode` format** | A hex colour only — `#RRGGBB` or `#RGB`. Colour keywords are not accepted. | `8509` |
| **`CONFIG` length — association APIs** | **1,000,000** characters, with the `viewIds` / `tagIds` array itself capped at **50,000** characters. | `8507` |
| **`CONFIG` length — Get Tagged Views** | **1,000** characters. | `8507` |
| **Cross-workspace association** | **Not possible.** Every view in `viewIds` must belong to `<workspace-id>`, and every tag in `tagIds` must exist in it. | `8184` |
| **Tag creation from the view side** | **Not supported.** [Add Multiple Tags To View](add-tags-to-view.md) only accepts IDs of tags that already exist. Create them first with [Create Tag](create-tag.md). | `8184` |
| **Bulk tag creation** | **Not supported.** [Create Tag](create-tag.md) creates exactly one tag per call. |  — |
| **Renaming via Create** | **Not possible.** A second [Create Tag](create-tag.md) with an existing name fails rather than returning the existing tag. | `8174` |

> **The ten-tag ceiling counts what is already there.** A view holding 8 tags accepts 2 more; a request adding 3 fails outright with [`8181`](../../../foundations/error-codes.md#error-8181) and **nothing is written** — the check runs before the insert, so the operation is all-or-nothing.

---

# Permission Model

| API | Who may call it |
|-----|-----------------|
| [Get Tags List](get-tags.md) | Any user with access to the workspace — Account Admin, Organization Admin, Workspace Admin, or any shared user, including custom roles. |
| [Get Tagged Views](get-tagged-views.md) | Any user with access to the workspace. The returned list is **filtered to the views that caller can see**. |
| [Get View Tags](get-view-tags.md) | Any user with **Read** permission on the view. |
| [Create Tag](create-tag.md) | An Account Admin or Organization Admin, or a Workspace Admin. |
| [Update Tag](update-tag.md) | An Account Admin or Organization Admin, or a Workspace Admin. |
| [Delete Tag](delete-tag.md) | An Account Admin or Organization Admin, or a Workspace Admin. |
| [Add Tag To Multiple Views](add-tag-to-views.md) | An Account Admin or Organization Admin, or a Workspace Admin. **Not** the View Owner. |
| [Remove Tag From Multiple Views](remove-tag-from-views.md) | An Account Admin or Organization Admin, or a Workspace Admin. **Not** the View Owner. |
| [Add Multiple Tags To View](add-tags-to-view.md) | An Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with **Edit Design** permission on the view. |
| [Remove Multiple Tags From View](remove-tags-from-view.md) | An Account Admin or Organization Admin, or a Workspace Admin, or the View Owner, or any user with **Edit Design** permission on the view. |

| Gate | Behaviour |
|------|-----------|
| **Read-only users** | Blocked from all four association APIs (7, 8, 9, 10) with `8180`, whatever else they hold. They can still call the three read APIs. |
| **Client Portal / White Label** | All ten APIs are **available** through a custom domain, subject to the same permissions. |

> **Reading is broad, writing is narrow.** Any user who can open the workspace can list its tags; only administrators can change them. This is deliberate — tags are a shared organising vocabulary, so they are readable by everyone and editable by few.

---

# The `colorCode` Attribute

`colorCode` is a hex colour string, and it is validated twice — first against the accepted pattern, then by the tag service.

**Accepted:** `#` followed by exactly **6** hex digits (`#e72d35`) or exactly **3** hex digits (`#f90`). Case-insensitive.

**Rejected:** colour keywords (`red`, `blue`), `rgb()` notation, 8-digit values with alpha (`#e72d35ff`), and a bare hex value with no leading `#` (`e72d35`). All fail with [`8509`](../../../foundations/error-codes.md#error-8509) before the request reaches the tag service.

Colours observed in real workspaces include `#e72d35`, `#f5a623`, `#55acee`, and `#1da043`. Zoho Analytics does not restrict you to a palette — any valid hex value is stored and returned exactly as sent.

```json
{ "name": "Finance", "colorCode": "#1da043" }
```

> `colorCode` is presentation only. It affects how the tag is drawn in the Zoho Analytics interface and nothing else — two tags may share a colour, and the colour plays no part in matching or filtering.

---

# API-Specific Notes and Behaviours

## Get Tags List

- **It is the cheapest way to resolve a tag name to an ID.** There is no lookup-by-name endpoint, so name-driven integrations list all tags and match client-side.
- **It shows tags, not usage.** A tag attached to nothing looks identical to one attached to five hundred views. Pair it with [Get Tagged Views](get-tagged-views.md) if usage matters.
- **Readable by everyone with workspace access**, including custom roles — verified against real responses for account-admin, org-admin, workspace-admin, and custom-role callers, all identical.
- **Dependency chain:** Get Tags List → `tags[].id` → every tag-side API.

## Get Tagged Views

- **The result is permission-filtered, which makes it a poor audit tool.** A non-administrator sees only the tagged views shared with them, so "how many views carry this tag" can only be answered reliably by an administrator.
- **`limit` / `offset` paging is blind.** No total and no cursor come back, so you cannot tell whether another page exists without asking for one.
- **A missing tag raises [`8184`](../../../foundations/error-codes.md#error-8184) rather than returning an empty list**, which distinguishes "tag gone" from "tag unused" — a useful signal worth branching on.
- **`type` is a name, never a number.** `Table`, `AnalysisView`, `Dashboard`, and so on — see [View `type` values](get-tagged-views.md#view-type-values).
- **Dependency chain:** [Create Tag](create-tag.md) / [Get Tags List](get-tags.md) → `<tag-id>` → Get Tagged Views → `views[].id`.

## Get View Tags

- **It is the pre-flight check for the ten-tag ceiling.** The length of `tags[]` tells you how many slots are free before you call [Add Multiple Tags To View](add-tags-to-view.md).
- **It needs only Read on the view**, so a shared user can always see how their view is labelled even when they cannot change it.
- **Its response shape is identical to [Get Tags List](get-tags.md)**, so one parser serves both.
- **Dependency chain:** [Get View List](../view-operations/get-views.md) → `<view-id>` → Get View Tags → `tags[].id`.

## Create Tag

- **This is the only place a `tagId` is minted.** Capture `data.tagId` from the response; there is no create-and-associate shortcut.
- **The response key is `tagId` while every read API calls the same value `id`.** The inconsistency is real — normalise it in your client.
- **It is not idempotent and not an upsert.** Re-running a create script fails on the second pass with [`8174`](../../../foundations/error-codes.md#error-8174) instead of quietly succeeding. Read [Get Tags List](get-tags.md) first if your script must be re-runnable.
- **`summary` is `"Create Tag"` with a capital `T`**, unlike the lower-case summaries the read APIs return. Do not match on summary text.
- **Dependency chain:** Create Tag → `data.tagId` → [Add Tag To Multiple Views](add-tag-to-views.md).

## Update Tag

- **It is one of the few genuine partial updates in the V2 surface.** Send only what changes; the rest is preserved. Most sibling update APIs replace the whole definition, so do not generalise this behaviour.
- **[`8182`](../../../foundations/error-codes.md#error-8182) is misleadingly worded.** Its message reads as a permission denial, but it means the CONFIG had neither `name` nor `colorCode`. A real permission failure is [`8179`](../../../foundations/error-codes.md#error-8179).
- **Renaming never breaks associations.** The link is by ID, so every tagged view stays tagged.
- **Dependency chain:** [Get Tags List](get-tags.md) → `<tag-id>` → Update Tag → [Get Tags List](get-tags.md).

## Delete Tag

- **It is the only destructive API in the family**, and it cascades: the tag and all of its associations go together, with no report of how many links were removed.
- **Check the blast radius first.** [Get Tagged Views](get-tagged-views.md) is the only way to see what will be unlinked, and it must be called before the delete.
- **If you only want to clear the links, this is the wrong API.** Use [Remove Tag From Multiple Views](remove-tag-from-views.md) with `dissociateAll: true`.
- **Dependency chain:** [Get Tags List](get-tags.md) → `<tag-id>` → [Get Tagged Views](get-tagged-views.md) → Delete Tag.

## Add Tag To Multiple Views

- **Its permission rule is the trap in this family.** It needs workspace administration, so a View Owner cannot use it even on their own view. If your integration runs as a non-admin, use [Add Multiple Tags To View](add-tags-to-view.md) instead — one call per view rather than one call per tag.
- **The batch is validated as a whole.** One bad view ID, or one view already at ten tags, and nothing is written for any view in the request.
- **It is safely re-runnable.** Existing pairs are skipped rather than rejected, so a retry after a network failure is harmless.
- **[`8181`](../../../foundations/error-codes.md#error-8181) names the offending views in the error message**, which is what makes it recoverable — drop those views and resend.
- **Dependency chain:** [Create Tag](create-tag.md) → `<tag-id>`; [Get View List](../view-operations/get-views.md) → `viewIds` → Add Tag To Multiple Views.

## Remove Tag From Multiple Views

- **`dissociateAll: true` is the widest-reaching operation here.** It strips the tag from every view in the workspace in one call, with no confirmation and no count returned. Treat it as a workspace-level action.
- **The error message tells you to use `removeAll`, which does not exist.** The attribute is `dissociateAll`; ignore the message text.
- **It is the non-destructive alternative to [Delete Tag](delete-tag.md)** when you want to keep the tag for reuse.
- **Administrators only**, like its sibling.
- **Dependency chain:** [Get Tagged Views](get-tagged-views.md) → `views[].id` → Remove Tag From Multiple Views.

## Add Multiple Tags To View

- **This is the API to reach for when the caller is not an administrator.** The View Owner and anyone with Edit Design permission can call it, which is the practical difference from [Add Tag To Multiple Views](add-tag-to-views.md).
- **Already-attached tags are free.** They are skipped, and they do not count towards the ten-tag check — so re-sending a superset of the current tags is safe.
- **It cannot create tags.** Every ID in `tagIds` must already exist; a typo surfaces as [`8184`](../../../foundations/error-codes.md#error-8184), not as a silently created tag.
- **Read-only users are blocked even on views they own**, with [`8180`](../../../foundations/error-codes.md#error-8180).
- **Dependency chain:** [Get Tags List](get-tags.md) → `tagIds` → Add Multiple Tags To View → [Get View Tags](get-view-tags.md).

## Remove Multiple Tags From View

- **`dissociateAll: true` here is narrow and safe** — it clears one view — which is the opposite of the same flag on [Remove Tag From Multiple Views](remove-tag-from-views.md). Read the endpoint, not just the flag.
- **It is how you make room at the ten-tag ceiling** before adding more.
- **The same `removeAll` wording bug appears in its error message**; the attribute is `dissociateAll`.
- **Dependency chain:** [Get View Tags](get-view-tags.md) → `tags[].id` → Remove Multiple Tags From View.

---

# General Response Payload Notes

| Field / Behaviour | Detail |
|-------------------|--------|
| **Four APIs return a body, six return 204** | [Get Tags List](get-tags.md), [Get Tagged Views](get-tagged-views.md), [Get View Tags](get-view-tags.md), and [Create Tag](create-tag.md) return `200` with the standard envelope. The six mutating association and lifecycle APIs return `204 No Content` with an empty body. |
| **A 204 carries no confirmation of scope** | None of the six reports how many rows changed. Verification is always a follow-up read. |
| **Failure responses share one shape** | `{"status": "failure", "summary": "<ERROR_NAME>", "data": {"errorCode": <n>, "errorMessage": "<text>"}}`. `summary` on failure is the error's symbolic name (for example `TAG_COUNT_EXCEEDS`), not a localised sentence. |
| **Success `summary` values differ per API** | `"Get tags"`, `"Get tagged views"`, `"Get view tags"`, and `"Create Tag"`. Only the last is capitalised. Do not branch on summary text. |
| **Every value inside `data` is a string** | `id`, `tagId`, and `views[].id` are all JSON strings, never numbers, even though they are numerically longs. |
| **Empty collections are successes** | `{"tags": []}` and `{"views": []}` both come back with HTTP 200. They mean "nothing matched", never "not found". |
| **The two tag-shaped responses are interchangeable** | [Get Tags List](get-tags.md) and [Get View Tags](get-view-tags.md) both return `data.tags[]` with `id`, `name`, and `colorCode`. |
| **`colorCode` round-trips exactly** | It is returned in the same case and form it was stored in. |
| **Ordering is never guaranteed** | Neither `tags[]` nor `views[]` has a defined order. Sort client-side. |
| **There is no `count` field anywhere** | Neither read API reports a total, so array length is the only measure available. |

---

# Enum and Value Reference

**`type`** — returned by [Get Tagged Views](get-tagged-views.md) as `views[].type`

| Value | View type |
|-------|-----------|
| `Table` | A table |
| `Report` | A tabular view |
| `AnalysisView` | A chart view |
| `Pivot` | A pivot view |
| `SummaryView` | A summary view |
| `TableView` | A table view |
| `QueryTable` | A query table |
| `Dashboard` | A dashboard |
| `WIDGET` | A dashboard widget |
| `Tab` | A dashboard tab |
| `PipelineTable` | A pipeline table |
| `DataModelObject` | A data model object |

**`colorCode`** — accepted by [Create Tag](create-tag.md) and [Update Tag](update-tag.md)

| Form | Example | Accepted |
|------|---------|:--------:|
| Six hex digits with `#` | `#e72d35` | ✓ |
| Three hex digits with `#` | `#f90` | ✓ |
| Colour keyword | `red` | – |
| Hex without `#` | `e72d35` | – |
| Eight hex digits with alpha | `#e72d35ff` | – |
| `rgb()` notation | `rgb(231,45,53)` | – |

**`dissociateAll`** — accepted by [Remove Tag From Multiple Views](remove-tag-from-views.md) and [Remove Multiple Tags From View](remove-tags-from-view.md), default `false`

| Value | Behaviour on Remove Tag From Multiple Views | Behaviour on Remove Multiple Tags From View |
|-------|--------------------|---------------------|
| `false` | Detach the tag from the views named in `viewIds`. | Detach the tags named in `tagIds` from the view. |
| `true` | Detach the tag from **every view in the workspace**; `viewIds` is ignored. | Detach **every tag** from this one view; `tagIds` is ignored. |

**`status`** — present on every response that has a body

| Value | Meaning |
|-------|---------|
| `success` | The request succeeded. |
| `failure` | The request failed; `data.errorCode` carries the reason. |

---

# CONFIG Attribute Availability by API

`✓` accepted, `–` not accepted by that API.

| Attribute | 1 Get Tags List | 2 Get Tagged Views | 3 Get View Tags | 4 Create Tag | 5 Update Tag | 6 Delete Tag | 7 Add Tag To Views | 8 Remove Tag From Views | 9 Add Tags To View | 10 Remove Tags From View |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `name` | – | – | – | ✓ **mandatory** | ✓ conditional | – | – | – | – | – |
| `colorCode` | – | – | – | ✓ **mandatory** | ✓ conditional | – | – | – | – | – |
| `viewIds` | – | – | – | – | – | – | ✓ **mandatory** | ✓ conditional | – | – |
| `tagIds` | – | – | – | – | – | – | – | – | ✓ **mandatory** | ✓ conditional |
| `dissociateAll` | – | – | – | – | – | – | – | ✓ | – | ✓ |
| `limit` | – | ✓ | – | – | – | – | – | – | – | – |
| `offset` | – | ✓ | – | – | – | – | – | – | – | – |

[Get Tags List](get-tags.md), [Get View Tags](get-view-tags.md), and [Delete Tag](delete-tag.md) take no CONFIG at all.

---

# Tag Object Model and Association Rules

**The tag object**

| Field | Type | Description |
|-------|------|-------------|
| `id` / `tagId` | String | Identifier of the tag. Returned as `tagId` by [Create Tag](create-tag.md) and as `id` by the read APIs — the same value under two names. |
| `name` | String | Display name, 1–100 characters, unique within the workspace. |
| `colorCode` | String | Hex colour, `#RRGGBB` or `#RGB`. Presentation only. |

**Association rules**

1. A tag is **workspace-scoped**. It can only be attached to views in the same workspace; there is no cross-workspace or organization-wide tag.
2. A single view carries at most **10** tags.
3. A single tag may label any number of views, subject only to the 1000-per-request batch size.
4. Attaching an already-attached `(view, tag)` pair is a **no-op**, not an error.
5. Detaching a pair that was never attached is likewise a no-op.
6. Deleting a tag removes every association it had.
7. Deleting a view removes every association that view had.
8. Renaming or recolouring a tag leaves all associations intact.
9. Tags carry no permissions. Attaching one neither grants nor restricts access to the view.

# Error Codes Used in This Group

| Code | HTTP | Meaning |
|---|---|---|
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource. |
| [7390](../../../foundations/error-codes.md#error-7390) | 400 | WORKSPACENOTBELONGSTOORG — The workspace does not belong to the organization in ZANALYTICS-ORGID. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | A required attribute (expression or formulaName) is missing from CONFIG. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | The ZANALYTICS-ORGID header is missing from a request that requires it. |
| [8174](../../../foundations/error-codes.md#error-8174) | 403 | DUPLICATETAGNAMEFOUND — A tag with this name already exists in the workspace. |
| [8179](../../../foundations/error-codes.md#error-8179) | 403 | DONTHAVEPERMISSIONTOCREATETAGS — The caller is not an Account Admin, Organization Admin, or Workspace Admin. |
| [8180](../../../foundations/error-codes.md#error-8180) | 403 | DONTHAVEPERMISSIONTOASSOCIATEANDUNASSOCIATETAGS — The caller is a read-only user. |
| [8181](../../../foundations/error-codes.md#error-8181) | 403 | TAGCOUNTEXCEEDS — One or more views would exceed 10 tags. The message lists them. |
| [8182](../../../foundations/error-codes.md#error-8182) | 403 | resetSort: true and sortOrder cannot be used together. |
| [8184](../../../foundations/error-codes.md#error-8184) | 403 | VIEWORTAGNOTPRESENTINDBTOTAG — The tag does not exist in this workspace. |
| [8185](../../../foundations/error-codes.md#error-8185) | 400 | CANNOTDELETEORUPDATETAG — The update matched no row. |
| [8187](../../../foundations/error-codes.md#error-8187) | 400 | TAGNOTPRESENTINDB — The tag does not exist in this workspace. |
| [8201](../../../foundations/error-codes.md#error-8201) | 400 | INVALIDCONFIGURATIONREMOVEVIEWSLINKEDWITHTAG — viewIds is empty or absent and dissociateAll is not true. |
| [8202](../../../foundations/error-codes.md#error-8202) | 400 | INVALIDCONFIGURATIONREMOVETAGSFORVIEW — tagIds is empty or absent and dissociateAll is not true. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | LESSTHANMINOCCURANCE — CONFIG was not sent. |
| [8507](../../../foundations/error-codes.md#error-8507) | 400 | MORETHANMAXLENGTH — roleName exceeds 30 characters, or permissions exceeds its size limit. |
| [8509](../../../foundations/error-codes.md#error-8509) | 400 | PATTERNNOTMATCHED — roleName contains disallowed characters, or accessType is not one of the three values. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation. |
| [8547](../../../foundations/error-codes.md#error-8547) | 400 | ARRAYSIZEOUTOFRANGE — selectedColumns is empty or holds more than 300 entries. |

# Related

- [Views Management](../overview.md) - parent domain.
- [Foundations](../../../foundations/index.md) - authentication, conventions, error codes, roles, identifiers.
- [Endpoint catalog](../../../endpoint-catalog.md) - every endpoint in one table.
