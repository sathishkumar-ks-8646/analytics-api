---
type: Reference
title: HTTP status codes
description: Which HTTP status codes Zoho Analytics REST API v2 returns, what each one means, and how it maps to the application error codes in the failure envelope.
tags:
  - zoho-analytics
  - rest-api-v2
  - http-status
  - errors
sources:
  - id: openapi-common
    resource: /references/openapi/zoho-analytics-api-common.json
    title: Shared OpenAPI components (CommonErrorResponse, UnexpectedErrorResponse)
  - id: markdown-docs
    resource: /domains/index.md
    title: API domain and group overviews in this bundle
generated:
  at: {{NOW}}
status: stable
---

# Summary

The HTTP status tells you the *class* of outcome; the `errorCode` inside the body tells you the *cause*. Always read both.

| Status | Meaning | Body | Typical error codes | Retry? |
|---|---|---|---|---|
| **200 OK** | Success with a payload. | JSON success envelope, or the exported file for export/download endpoints. | - | - |
| **204 No Content** | Success with nothing to return. | Empty. | - | - |
| **400 Bad Request** | The request itself is wrong: missing or invalid CONFIG, bad parameter values, validation failures, business-rule violations, name conflicts, limits exceeded. | Failure envelope. | `8080`, `8504`, `8507`, `8119`, `8079`, `8547`, `7330`, `7331`, `8000`, most 6xxx/7xxx/8xxx codes | No. Fix the request. |
| **401 Unauthorized** | Authentication failed. | Failure envelope. | `8535` | Only after refreshing the token. |
| **403 Forbidden** | Authenticated, but not allowed: missing role or view permission, feature not enabled for the organization or plan, organization security control blocks the operation. | Failure envelope. | `7301`, `8023`, `8088`, `6063`, `6054` | No. Change the caller or the configuration. |
| **404 Not Found** | The organization, workspace, view or other object in the path or CONFIG does not exist. | Failure envelope. | `7103`, `7104`, `7138`, `8120` | No. Fix the identifier. |
| **409 Conflict** | The request needs explicit confirmation or conflicts with current state. | Failure envelope. | `8241` (system-tag data warning, resend with `validateSystemTags: false`) | Yes, after acknowledging. |
| **500 Internal Server Error** | Unexpected server-side failure on an otherwise valid request. | Failure envelope. | `7005` | Yes, after a short delay; escalate if persistent. |

Notes:

- The OpenAPI files describe all client errors with a single `4XX` response and the server error with `500`; the exact 4xx status is chosen per error code at runtime.
- Some concurrency guards (job already running, copy in progress) come back as 400 with codes such as `18072`, `7429`, `8132`; they are retryable after the running operation finishes even though 400 is normally final.
- Throttling (see [Rate limits and quotas](/foundations/rate-limits-and-quotas.md)) rejects requests during the lock period; back off for the documented lockout duration.

# Related

- [Response envelope](/foundations/response-envelope.md)
- [Error code catalog](/foundations/error-codes.md)
