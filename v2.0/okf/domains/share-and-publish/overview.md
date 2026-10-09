---
type: API Domain
title: Share & Publish
description: "API for Share & Publish in Zoho Analytics — covering view sharing, publish configurations, embed URLs, and slideshow management."
tags:
  - zoho-analytics
  - rest-api-v2
  - share-and-publish
  - api-domain
api:
  domain: share-and-publish
  groups:
    - group: sharing
      title: Sharing
      doc: "/domains/share-and-publish/sharing/overview.md"
      endpoint_count: 6
    - group: publish
      title: Publish
      doc: "/domains/share-and-publish/publish/overview.md"
      endpoint_count: 7
    - group: embed-url
      title: Embed URL
      doc: "/domains/share-and-publish/embed-url/overview.md"
      endpoint_count: 3
    - group: slideshow-management
      title: Slideshow Management
      doc: "/domains/share-and-publish/slideshow-management/overview.md"
      endpoint_count: 6
  endpoint_count: 22
  openapi: "/references/openapi/share-publish-grouped-api.json"
sources:
  - id: openapi-spec
    resource: "/references/openapi/share-publish-grouped-api.json"
    title: OpenAPI 3 specification - share-publish-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

API for Share & Publish in Zoho Analytics — covering view sharing, publish configurations, embed URLs, and slideshow management.

# API Groups

| Group | Endpoints | Description |
|---|---|---|
| [Sharing](sharing/overview.md) | 6 | APIs for sharing workspaces and views with users, and retrieving share details and permissions. |
| [Publish](publish/overview.md) | 7 | APIs for making views public, managing private URLs, and updating publish configurations. |
| [Embed URL](embed-url/overview.md) | 3 | APIs for retrieving embeddable view URLs. |
| [Slideshow Management](slideshow-management/overview.md) | 6 | APIs for creating, updating, deleting, and listing slideshows and their URLs. |

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Workspace Shared Details](sharing/get-workspace-shared-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/share` | `getWorkspaceSharedDetails` | `ZohoAnalytics.share.read` | 200 |
| [Share Views](sharing/share-views.md) | POST | `/restapi/v2/workspaces/{workspace-id}/share` | `shareViews` | `ZohoAnalytics.share.create` | 204 |
| [Update Shared Details](sharing/update-shared-details-for-view.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share` | `UpdateSharedDetailsForView` | `ZohoAnalytics.share.update` | 204 |
| [Get Shared Details](sharing/get-shared-details-for-views.md) | GET | `/restapi/v2/workspaces/{workspace-id}/share/shareddetails` | `getSharedDetailsForViews` | `ZohoAnalytics.share.read` | 200 |
| [Remove Shared Views](sharing/remove-share.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/share` | `removeShare` | `ZohoAnalytics.share.delete` | 204 |
| [Get My Permissions](sharing/get-user-permissions.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/share/mypermissions` | `getUserPermissions` | `ZohoAnalytics.share.read` | 200 |
| [Make View Public](publish/make-views-public.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/public` | `makeViewsPublic` | `ZohoAnalytics.embed.create` | 200 |
| [Remove Public Permission](publish/remove-public-permission.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/public` | `removePublicPermission` | `ZohoAnalytics.embed.delete` | 204 |
| [Get Private URL](publish/get-private-url.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink` | `getPrivateUrl` | `ZohoAnalytics.embed.read` | 200 |
| [Create Private URL](publish/create-private-url.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink` | `createPrivateUrl` | `ZohoAnalytics.embed.update` | 200 |
| [Remove Private Access](publish/remove-private-access.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/privatelink` | `removePrivateAccess` | `ZohoAnalytics.embed.delete` | 204 |
| [Get Publish Configurations](publish/get-publish-configurations.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config` | `getPublishConfigurations` | `ZohoAnalytics.embed.read` | 200 |
| [Update Publish Configurations](publish/update-publish-configurations.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/config` | `updatePublishConfigurations` | `ZohoAnalytics.embed.update` | 204 |
| [Get Embed URL](embed-url/get-embed-url.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embed` | `getEmbedUrl` | `ZohoAnalytics.embed.read` | 200 |
| [Fetch All Embed URLs](embed-url/get-embed-urls.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embedurls` | `getEmbedUrls` |  | 200 |
| [Delete Embed URL](embed-url/delete-embed-url.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/publish/embed` | `deleteEmbedUrl` |  | 200 |
| [Get Slide List](slideshow-management/get-slideshows.md) | GET | `/restapi/v2/workspaces/{workspace-id}/slides` | `getSlideshows` | `ZohoAnalytics.embed.read` | 200 |
| [Get Slide URL](slideshow-management/get-slideshow-url.md) | GET | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}/publish` | `getSlideshowUrl` | `ZohoAnalytics.embed.read` | 200 |
| [Get Slide Info](slideshow-management/get-slideshow-details.md) | GET | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}` | `getSlideshowDetails` | `ZohoAnalytics.embed.read` | 200 |
| [Create Slide Show](slideshow-management/create-slideshow.md) | POST | `/restapi/v2/workspaces/{workspace-id}/slides` | `createSlideshow` | `ZohoAnalytics.embed.create` | 200 |
| [Update Slide Show](slideshow-management/update-slideshow.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}` | `updateSlideshow` | `ZohoAnalytics.embed.update` | 204 |
| [Delete Slide Show](slideshow-management/delete-slideshow.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/slides/{slide-id}` | `deleteSlideshow` | `ZohoAnalytics.embed.delete` | 204 |

# Related

- [All domains](../index.md)
- [OpenAPI specification for this domain](../../references/openapi/share-publish-grouped-api.json)
- [Foundations](../../foundations/index.md)
