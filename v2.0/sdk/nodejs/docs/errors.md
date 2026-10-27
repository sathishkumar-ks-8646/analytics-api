# Errors

## The failure surface

A rejected Promise carrying `errorCode` and `errorMessage`.

```javascript
async function listViews() {
    var workspace = ac.getWorkspaceInstance(orgId, workspaceId);
    try {
        var views = await workspace.getViews();
        console.log(views);
    } catch (error) {
        // error.errorCode is the stable value to branch on.
        switch (error.errorCode) {
            case 8535: break;   // token invalid or under-scoped
            case 7301: break;   // caller lacks permission
            case 7103: break;   // workspace does not exist
        }
        console.log(error.errorCode, error.errorMessage);
    }
}
```

## The response envelope

The API has exactly three response shapes.

| Shape | HTTP | Body |
|---|---|---|
| Success with data | 200 | `{"status":"success","summary":"...","data":{...}}` |
| Success, nothing to return | 204 | Empty. |
| Failure | 4xx, 5xx | `{"status":"failure","summary":"<CONSTANT>","data":{"errorCode":<int>,"errorMessage":"..."}}` |

Synchronous export endpoints are the exception: on success they return the file
itself with a matching `Content-Type`, and only use the JSON envelope on failure.

### A failure response

```json
{
  "status": "failure",
  "summary": "SECURITY_NOT_PERMITTED",
  "data": {
    "errorCode": 7301,
    "errorMessage": "You (user@zylker.com) do not have the permission to do this operation."
  }
}
```

Branch on `errorCode`. `summary` is a stable constant you can log, and
`errorMessage` is localised prose — log it, do not parse it.

## HTTP status codes

| Status | Meaning | Retry? |
|---|---|---|
| **200** | Success with a payload. | — |
| **204** | Success, nothing to return. | — |
| **400** | The request is wrong: bad config, validation failure, business-rule violation, limit exceeded. | No. Fix the request. |
| **401** | Authentication failed — token missing, expired, revoked, under-scoped or from the wrong region. | Only after refreshing. |
| **403** | Authenticated but not allowed: missing role or permission, or a feature not on your plan. | No. |
| **404** | The organization, workspace or view in the path does not exist. | No. Fix the identifier. |
| **409** | Needs explicit confirmation, or conflicts with current state. | Yes, after acknowledging. |
| **500** | Unexpected server-side failure. | Yes, after a short delay. |

## Codes worth branching on

| Code | Constant | Meaning | What to do |
|---|---|---|---|
| `8535` | `INVALID_OAUTHTOKEN` | Token missing, expired, revoked, under-scoped, or issued in another region. | Check scopes and region. See [Authentication](authentication.md). |
| `8083` | `ORGID_NOT_PRESENT_IN_THE_HEADER` | Organization id missing. | The SDK sets this; it usually means the instance was built without an org id. |
| `7301` | `SECURITY_NOT_PERMITTED` | Authenticated user lacks the role or permission. | Change the caller or grant permission. Not retryable. |
| `7103` | — | Workspace does not exist, or is not visible to this user. | Check the workspace id and the user's access. |
| `7104` | — | View does not exist, or is not visible to this user. | Check the view id. |
| `8241` | — | Operation would touch system-tagged data. | Resend with `validateSystemTags: false` once you have confirmed. |
| `8132` | — | Too many concurrent export jobs (limit is 5 per organization). | Wait for a running job to finish. |
| `8133` | — | Resource is restricted for synchronous export: over one million rows, from a live connect workspace, or a dashboard or query table. | Use the asynchronous job flow. |
| `18072` | — | A refetch is already running for this table. | Wait; do not retry in a loop. |
| `7429` | — | A copy is already running for this workspace. | Wait for it to finish. |
| `7005` | — | Unexpected server error. | Retry after a short delay; escalate if persistent. |

::: warning Not every 400 is permanent
Concurrency guards (`18072`, `7429`, `8132`) come back as HTTP 400 but *are*
retryable once the operation they are guarding finishes. Retrying them
immediately in a tight loop will not help; waiting will.
:::

## A retry policy that works

- **Retry** 500s and the concurrency guards above, with exponential backoff.
- **Retry once** after a 401, having refreshed the token — but if you are
  constructing one client and reusing it, the SDK has already done this.
- **Never retry** 400 (other than the guards), 403 or 404. The request or the
  caller is wrong; repeating it just burns API units.
- **Back off for the full lockout** when throttled. See [Limits](limits.md).

## Related

- [Limits](limits.md) — throttles, quotas and concurrency guards.
- [Authentication](authentication.md) — the token throttle, which reports through
  Zoho Accounts rather than this envelope.
