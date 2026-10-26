---
type: API Domain
title: Schedules & Alerts
description: "API for Schedules & Alerts in Zoho Analytics — covering creation, management, and triggering of email schedules, and the full lifecycle of data alerts on a view."
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - api-domain
api:
  domain: schedules-and-alerts
  groups:
    - group: email-schedules
      title: Email Schedules
      doc: "/domains/schedules-and-alerts/email-schedules/overview.md"
      endpoint_count: 6
    - group: data-alerts
      title: Data Alerts
      doc: "/domains/schedules-and-alerts/data-alerts/overview.md"
      endpoint_count: 10
  endpoint_count: 16
  openapi: "/references/openapi/schedules-alerts-grouped-api.json"
sources:
  - id: openapi-spec
    resource: "/references/openapi/schedules-alerts-grouped-api.json"
    title: OpenAPI 3 specification - schedules-alerts-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-20T17:34:40Z
generated:
  by: process:build_okf
  at: 2026-10-23T07:58:54Z
status: stable
---

# Summary

API for Schedules & Alerts in Zoho Analytics — covering creation, management, and triggering of email schedules, and the full lifecycle of data alerts on a view.

# API Groups

| Group | Endpoints | Description |
|---|---|---|
| [Email Schedules](email-schedules/overview.md) | 6 | APIs for creating, updating, triggering, and deleting email schedules, and retrieving schedule details. |
| [Data Alerts](data-alerts/overview.md) | 10 | APIs for creating, listing, updating, running and deleting data alerts on a view, changing their status and reading their event history. |

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Email Schedules](email-schedules/get-email-schedules.md) | GET | `/restapi/v2/workspaces/{workspace-id}/emailschedules` | `getEmailSchedules` | `ZohoAnalytics.metadata.read` | 200 |
| [Create Email Schedule](email-schedules/create-email-schedule.md) | POST | `/restapi/v2/workspaces/{workspace-id}/emailschedules` | `createEmailSchedule` | `ZohoAnalytics.modeling.create` | 200 |
| [Update Email Schedule](email-schedules/update-email-schedule.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}` | `updateEmailSchedule` | `ZohoAnalytics.modeling.update` | 200 |
| [Delete Email Schedule](email-schedules/delete-email-schedule.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}` | `deleteEmailSchedule` | `ZohoAnalytics.modeling.delete` | 204 |
| [Change Email Schedule Status](email-schedules/change-email-schedule-status.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}/status` | `changeEmailScheduleStatus` | `ZohoAnalytics.modeling.update` | 204 |
| [Trigger Email Schedule](email-schedules/trigger-email-schedule.md) | POST | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}` | `triggerEmailSchedule` | `ZohoAnalytics.modeling.create` | 204 |
| [Get Alerts In Workspace](data-alerts/get-alerts-in-workspace.md) | GET | `/restapi/v2/workspaces/{workspace-id}/alerts` | `getAlertsInWorkspace` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Alerts In View](data-alerts/get-alerts-in-view.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts` | `getAlertsInView` | `ZohoAnalytics.metadata.read` | 200 |
| [Get View Metadata For Alert](data-alerts/get-view-metadata-for-alert.md) | GET | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts/metadata` | `getViewMetadataForAlert` | `ZohoAnalytics.metadata.read` | 200 |
| [Get Alert Configuration](data-alerts/get-alert-configuration.md) | GET | `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}` | `getAlertConfiguration` | `ZohoAnalytics.metadata.read` | 200 |
| [Create Alert](data-alerts/create-alert.md) | POST | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts` | `createAlert` | `ZohoAnalytics.modeling.create` | 200 |
| [Update Alert](data-alerts/update-alert.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}` | `updateAlert` | `ZohoAnalytics.modeling.update` | 204 |
| [Delete Alerts](data-alerts/delete-alerts.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/alerts` | `deleteAlerts` | `ZohoAnalytics.modeling.delete` | 204 |
| [Change Alert Status](data-alerts/change-alert-status.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/alerts/status` | `changeAlertStatus` | `ZohoAnalytics.modeling.update` | 204 |
| [Run Alert](data-alerts/run-alert.md) | POST | `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/execute` | `runAlert` | `ZohoAnalytics.modeling.create` | 204 |
| [Get Alert Events](data-alerts/get-alert-events.md) | GET | `/restapi/v2/workspaces/{workspace-id}/alerts/{alert-id}/events` | `getAlertEvents` | `ZohoAnalytics.metadata.read` | 200 |

# Related

- [All domains](../index.md)
- [OpenAPI specification for this domain](../../references/openapi/schedules-alerts-grouped-api.json)
- [Foundations](../../foundations/index.md)
