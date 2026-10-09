---
type: API Domain
title: Schedules & Alerts
description: "API for Schedules & Alerts in Zoho Analytics — covering creation, management, and triggering of email schedules."
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
  endpoint_count: 6
  openapi: "/references/openapi/schedules-alerts-grouped-api.json"
sources:
  - id: openapi-spec
    resource: "/references/openapi/schedules-alerts-grouped-api.json"
    title: OpenAPI 3 specification - schedules-alerts-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T08:50:41Z
status: stable
---

# Summary

API for Schedules & Alerts in Zoho Analytics — covering creation, management, and triggering of email schedules.

# API Groups

| Group | Endpoints | Description |
|---|---|---|
| [Email Schedules](email-schedules/overview.md) | 6 | APIs for creating, updating, triggering, and deleting email schedules, and retrieving schedule details. |

# Endpoints

| Endpoint | Method | Path | Operation ID | OAuth scope | Success |
|---|---|---|---|---|---|
| [Get Email Schedules](email-schedules/get-email-schedules.md) | GET | `/restapi/v2/workspaces/{workspace-id}/emailschedules` | `getEmailSchedules` | `ZohoAnalytics.metadata.read` | 200 |
| [Create Email Schedule](email-schedules/create-email-schedule.md) | POST | `/restapi/v2/workspaces/{workspace-id}/emailschedules` | `createEmailSchedule` | `ZohoAnalytics.modeling.create` | 200 |
| [Update Email Schedule](email-schedules/update-email-schedule.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}` | `updateEmailSchedule` | `ZohoAnalytics.modeling.update` | 200 |
| [Delete Email Schedule](email-schedules/delete-email-schedule.md) | DELETE | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}` | `deleteEmailSchedule` | `ZohoAnalytics.modeling.delete` | 204 |
| [Change Email Schedule Status](email-schedules/change-email-schedule-status.md) | PUT | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}/status` | `changeEmailScheduleStatus` | `ZohoAnalytics.modeling.update` | 204 |
| [Trigger Email Schedule](email-schedules/trigger-email-schedule.md) | POST | `/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}` | `triggerEmailSchedule` | `ZohoAnalytics.modeling.create` | 204 |

# Related

- [All domains](../index.md)
- [OpenAPI specification for this domain](../../references/openapi/schedules-alerts-grouped-api.json)
- [Foundations](../../foundations/index.md)
