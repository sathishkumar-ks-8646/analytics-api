---
type: Reference
title: Response envelope
description: The JSON envelope returned by Zoho Analytics REST API v2 on success and failure, the 204 no-body pattern, file responses from export endpoints, and the value conventions inside data.
tags:
  - zoho-analytics
  - rest-api-v2
  - response
  - envelope
  - json
sources:
  - id: openapi-common
    resource: /references/openapi/zoho-analytics-api-common.json
    title: Shared OpenAPI components (Error schema, CommonErrorResponse, UnexpectedErrorResponse)
  - id: markdown-docs
    resource: /domains/index.md
    title: API domain and group overviews in this bundle
generated:
  at: {{NOW}}
status: stable
---

# Summary

Zoho Analytics v2 has exactly three response shapes:

| Shape | HTTP status | Body |
|---|---|---|
| **Success with data** | 200 | `{"status":"success","summary":"<operation summary>","data":{...}}` |
| **Success without data** | 204 | Empty. Used by most create/update/delete style endpoints that have nothing to return. |
| **Failure** | 400, 401, 403, 404, 409, 500 | `{"status":"failure","summary":"<ERROR_CONSTANT>","data":{"errorCode":<int>,"errorMessage":"<text>"}}` |

Synchronous export and download endpoints are the exception: on success they return the **file itself** (CSV, JSON, XML, XLS, PDF, HTML, PNG or JPEG) with a matching `Content-Type`, and only on failure do they return the JSON failure envelope.

# Success Envelope

```json
{
  "status": "success",
  "summary": "Get meta details",
  "data": {
    "workspaces": {
      "workspaceId": "320862000000625871",
      "workspaceName": "Sales Analytics",
      "workspaceDesc": "",
      "orgId": "106044221"
    }
  }
}
```

| Field | Type | Meaning |
|---|---|---|
| `status` | String | Always `"success"`. |
| `summary` | String | Short, human-readable operation name (localized). Do not branch on it. |
| `data` | Object | The payload. Its fields are documented per endpoint under `Response Fields`. Some endpoints return `data` as an array (for example `data.views[]`) inside the object. |

# Failure Envelope

```json
{
  "status": "failure",
  "summary": "SECURITY_NOT_PERMITTED",
  "data": {
    "errorCode": 7301,
    "errorMessage": "You (<user-name>) do not have the permission to do this operation. "
  }
}
```

| Field | Type | Meaning |
|---|---|---|
| `status` | String | Always `"failure"`. |
| `summary` | String | Stable upper-case error constant, for example `INVALID_OAUTHTOKEN`, `META_OBJECT_NOT_PRESENT`. |
| `data.errorCode` | Integer | The error code. Branch on this. Look it up in [Error code catalog](/foundations/error-codes.md#error-7301) (anchor `#error-<code>`). |
| `data.errorMessage` | String | Localized, sometimes parameterized text. Log it, do not parse it. |

The OpenAPI files model every 4xx as `CommonErrorResponse` and 500 as `UnexpectedErrorResponse`; both reference the same `Error` schema.

# Value Conventions Inside `data`

- **IDs are strings.** `workspaceId`, `viewId`, `columnId`, `orgId`, `jobId` and every other identifier is a JSON string even though it looks numeric.
- **Empty collections are empty arrays**, never missing keys and never errors (for example an organization with no admins returns `"orgAdmins": []`).
- **Optional objects may be absent.** For example `data.views` appears only when a `viewName` was requested; test for the key.
- **Row values are strings** in the Row and import APIs, including numbers and booleans.
- **Timestamps** are usually epoch milliseconds as strings (for example `expiryTime`) or human-readable strings (`billingDate`); each endpoint document states the format.
- **Two different `status` fields can coexist**: the envelope `status` (`success`/`failure`) and a domain field such as `jobStatus` or a user `status` inside `data`.

# Handling Pattern

```text
if http_status == 204: success, nothing to parse
elif content_type is not JSON: success, body is the exported file
else:
    body = parse JSON
    if body.status == "success": use body.data
    else: handle body.data.errorCode (see the error catalog); retry only 5xx and concurrency guards
```

# Related

- [HTTP status codes](/foundations/http-status-codes.md)
- [Error code catalog](/foundations/error-codes.md)
- [Request conventions](/foundations/request-conventions.md)
