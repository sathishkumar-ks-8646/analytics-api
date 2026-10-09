---
type: Playbook
title: Schedule a recurring email delivery of a report or dashboard
description: Create an email schedule with recipients and calendar frequency, trigger it once to test, enable or disable it, and update it safely.
tags:
  - zoho-analytics
  - rest-api-v2
  - workflow
  - playbook
  - email-schedules
  - scheduling
sources:
  - id: markdown-docs
    resource: /domains/index.md
    title: API domain and group overviews in this bundle
generated:
  at: {{NOW}}
status: stable
---

# Goal

Deliver one or more views as CSV, XLS, PDF, HTML or image attachments on a recurring calendar.

# Prerequisites

- Token scope `ZohoAnalytics.modeling.create` (create), `.read`, `.update`, `.delete` as documented per endpoint.
- Create Email Schedule permission on the workspace or an admin role, plus **Export** permission on every view scheduled.
- `workspaceId` and the `viewIds`; optional `groupIds`.
- Plan quota: scheduled emails are a plan resource (see [Get Resource Details](/domains/organization-management/org-info-and-settings/get-resource-details.md)).

# Steps

1. **Create** with [Create Email Schedule](/domains/schedules-and-alerts/email-schedules/create-email-schedule.md), `POST /restapi/v2/workspaces/{workspace-id}/emailschedules`:

```json
{
  "scheduleName": "Weekly Sales PDF",
  "viewIds": ["137687000006991601"],
  "exportType": "PDF",
  "emailIds": ["sales-team@example.com"],
  "subject": "Weekly sales",
  "scheduleDetails": { "calendarFrequency": "weekly", "weekDays": [2], "hour": 8, "minute": 0 }
}
```

   Rules: `scheduleName` unique in the workspace (`8000`); at least one recipient across `emailIds`, `groupIds`, `cc` (`8033`); `minute` a multiple of 5; a dashboard schedule holds one view and uses `PDF` or `HTML` (`8034`/`8035`); `XLS` allows one view (`8037`); `IMG` needs chart views (`8036`). The time zone is the Account Admin's and cannot be set. Keep the returned `scheduleId`.
2. **Test** with [Trigger Email Schedule](/domains/schedules-and-alerts/email-schedules/trigger-email-schedule.md) to send immediately.
3. **List and inspect** with [Get Email Schedules](/domains/schedules-and-alerts/email-schedules/get-email-schedules.md).
4. **Pause or resume** with [Change Email Schedule Status](/domains/schedules-and-alerts/email-schedules/change-email-schedule-status.md).
5. **Update** with [Update Email Schedule](/domains/schedules-and-alerts/email-schedules/update-email-schedule.md). `viewIds` and `exportType` cannot change after creation; changing `scheduleName` may regenerate the schedule ID (read the group overview's Schedule ID Lifecycle section and re-read the ID from the response).
6. **Delete** with [Delete Email Schedule](/domains/schedules-and-alerts/email-schedules/delete-email-schedule.md).

# Notes

- `applyShareCriteria: true` sends each recipient their own share-filtered export and consumes one quota unit per recipient.
- `reportBurstConfig` sends one personalized email per row of a distribution-list table.

# Related

- [Email Schedules](/domains/schedules-and-alerts/email-schedules/overview.md)
- [Export formats and enumerations](/foundations/export-formats-and-enums.md)
