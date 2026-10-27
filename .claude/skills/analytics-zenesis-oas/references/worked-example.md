# One endpoint, end to end

The real `Update Email Schedule` endpoint, followed from the markdown section through every
knowledge base. Use it as the shape to copy. Domain: `09 · Schedules & Alerts`, slug
`schedules-alerts`, group `EMAIL_SCHEDULES`, tag `Email Schedules`.

---

## 1. The manifest entry (the spine)

`v2.0/manifest.json`:

```json
{
  "folder": "09 · Schedules & Alerts",
  "slug": "schedules-alerts",
  "groups": [
    { "md": "EMAIL_SCHEDULES", "tag": "Email Schedules",
      "okf": { "slug": "email-schedules", "title": "Email Schedules" } }
  ],
  "okf":     { "slug": "schedules-and-alerts", "title": "Schedules & Alerts" },
  "postman": { "emoji": "⏰", "title": "Schedules & Alerts", "covers": "…" }
}
```

It fixes every name downstream:

| Name | Comes from | Used as |
|---|---|---|
| `v2.0/md/09 · Schedules & Alerts/EMAIL_SCHEDULES.md` | `folder` + `md` | the markdown source |
| `v2.0/zenesis-oas/schedules-alerts-grouped-api.json` | `slug` | the specification |
| `v2.0/zenesis-oas-samples/schedules-alerts-grouped-api-samples.json` | `slug` | the SDK snippets |
| `v2.0/oas/schedules-alerts-grouped-api.json` | `slug` | the published spec |
| `v2.0/okf/domains/schedules-and-alerts/email-schedules/` | `okf.slug` ×2 | the bundle directory |
| Postman folder `⏰ Schedules & Alerts` → `Email Schedules` | `postman` + `okf.title` | the collection tree |

---

## 2. The markdown section (SOURCE — written first)

`v2.0/md/09 · Schedules & Alerts/EMAIL_SCHEDULES.md`, abridged:

```markdown
## 3. Update Email Schedule

Updates an existing schedule's name, run period, recipients, or email content. **Read [Schedule ID
Lifecycle](#schedule-id-lifecycle) first** — this call can replace the schedule's ID.

| Attribute | Value |
|-----------|-------|
| **Method** | PUT |
| **URL** | `/restapi/v2/workspaces/<workspace-id>/emailschedules/<schedule-id>` |
| **OAuth Scope** | `ZohoAnalytics.modeling.update` |
| **ZANALYTICS-ORGID Header** | **Mandatory** — Organisation ID of the workspace. |
| **Permission Required** | The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with Create Email Schedule permission on the workspace. … |

### CONFIG Parameters

CONFIG is **mandatory**, but every field inside it is optional: **omitted fields retain their current values**.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `scheduleName` | String | No | unchanged | New name for the schedule. … **Changing this regenerates `scheduleId`.** |
| `scheduleDetails` | JSONObject | No | unchanged | New run frequency and time. … See [`scheduleDetails` Fields](#scheduledetails-fields). |
| `emailIds` | JSONArray of String | No | unchanged | **Replaces** the recipient list, 0–1000 entries. |
| `validateSystemTags` | Boolean | No | `true` | If `true`, the request is rejected with `8241` when … |

### Sample Requests

**Case 2 — Rename and re-schedule to daily (`scheduleId` is regenerated)**

```http
PUT /restapi/v2/workspaces/137687000271334001/emailschedules/137687000010815003 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={"scheduleName":"Daily Sales Overview","scheduleDetails":{"calendarFrequency":"daily","hour":10,"minute":30}}
```

### Sample Responses

**HTTP 200 OK — Schedule updated**
```json
{ "status": "success", "summary": "Update email schedule", "data": { "scheduleId": "1767024000010887001" } }
```

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7812 | `SCHEDULE_DELETED` — No schedule exists with the given `<schedule-id>`. | Re-resolve the current ID via Get Email Schedules. |
| 8000 | `DUPLICATE_SCHEDULE` — Another schedule already uses the requested `scheduleName`. | Choose a different name. |
```

Note `## 3.` — the number resolves intra-document links such as `(#3-update-email-schedule)`, so the
numbering must stay contiguous and the `## Index` table must be updated with it.

---

## 3. The Zenesis operation (knowledge base 1 — `analytics-zenesis-oas`)

`v2.0/zenesis-oas/schedules-alerts-grouped-api.json`:

```jsonc
"/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}": {
  "put": {
    "operationId": "updateEmailSchedule",                 // ← camelCase of the title, unique everywhere
    "summary": "Update Email Schedule",                   // ← == the markdown "## 3. <Title>"
    "description": "Updates an existing schedule's name, run period, recipients, or email content. Read Schedule ID Lifecycle first — this call can replace the schedule's ID.",
    "tags": ["Email Schedules"],                          // ← the manifest `tag`
    "x-zenesis-title": "Update Email Schedule",           // ← == summary, character for character
    "security": [ { "iam-oauth2-schema": ["ZohoAnalytics.modeling.update"] } ],   // ← | **OAuth Scope** |
    "parameters": [
      { "$ref": "#/components/parameters/org-id" },       // ← | **ZANALYTICS-ORGID Header** | Mandatory
      { "$ref": "#/components/parameters/workspace-id" }, // ← <workspace-id> in the URL
      { "$ref": "#/components/parameters/schedule-id" }   // ← <schedule-id> in the URL
    ],
    "requestBody": {
      "required": true,                                   // ← "CONFIG is **mandatory**"
      "content": {
        "application/x-www-form-urlencoded": {            // ← Content-Type of the sample request
          "schema": {
            "type": "object",
            "required": ["CONFIG"],
            "properties": { "CONFIG": { "$ref": "#/components/schemas/UpdateEmailScheduleConfig" } }
          },
          "encoding": { "CONFIG": { "contentType": "application/json" } },
          "examples": {
            "changeFrequency": {                          // ← camelCase slug of "Case 2 — …"
              "description": "Change frequency",          // ← the LABEL goes in `description` (swapped)
              "summary": "Renames the schedule and switches it to run every day at 10:30.",
              "value": { "CONFIG": { "scheduleName": "Daily Sales Overview",
                                     "scheduleDetails": { "calendarFrequency": "daily", "hour": 10, "minute": 30 },
                                     "subject": "Daily Sales Overview" } }
            }
          }
        }
      }
    },
    "responses": {
      "200": {
        "description": "Successfully updated the email schedule.",
        "content": { "application/json": {
          "schema": { "$ref": "#/components/schemas/UpdateEmailScheduleResponse" },
          "examples": { "scheduleUpdated": {
            "description": "Schedule updated",
            "summary": "Returns the ID of the email schedule that was updated.",
            "value": { "status": "success", "summary": "Update email schedule",
                       "data": { "scheduleId": "1767024000010887001" } }
          } }
        } },
        "x-zenesis-statuscodes": [                        // ← the ### Error Codes table, ON THE SUCCESS RESPONSE
          { "name": "7812",
            "description": "SCHEDULEDELETED — No schedule exists with the given <schedule-id>. Commonly a stale ID after an earlier update regenerated it.",
            "resolution": "Re-resolve the current ID via Get Email Schedules." },
          { "name": "8000",
            "description": "DUPLICATESCHEDULE — Another schedule in the workspace already uses the requested scheduleName.",
            "resolution": "Choose a different name." }
        ]
      },
      "4XX": { "$ref": "https://raw.githubusercontent.com/zoho/analytics-oas/refs/heads/main/v2.0/common/zoho-analytics-api-common.json#/components/responses/CommonErrorResponse" },
      "500": { "$ref": "https://raw.githubusercontent.com/zoho/analytics-oas/refs/heads/main/v2.0/common/zoho-analytics-api-common.json#/components/responses/UnexpectedErrorResponse" }
    }
  }
}
```

with the CONFIG schema, derived row by row from the `### CONFIG Parameters` table:

```jsonc
"UpdateEmailScheduleConfig": {
  "type": "object",
  "title": "UpdateEmailScheduleConfig",
  "description": "JSONObject that holds the configuration to be applied to the existing email schedule.",
  "properties": {
    "scheduleName":    { "type": "string", "description": "Name of the schedule." },
    "scheduleDetails": { "$ref": "#/components/schemas/ScheduleDetails" },
    "emailIds":        { "$ref": "#/components/schemas/ScheduleEmailIds" },
    "subject":         { "type": "string", "description": "Subject of the email." },
    "validateSystemTags": {
      "type": "boolean",
      "description": "Controls whether the request has to be validated against the System Tags applied to the views. …",
      "default": true,
      "enum": [true, false]
    }
  }
}
```

No `required` list here, because every markdown Mandatory cell says `No`. Nested JSONObject /
JSONArray rows become named components (`ScheduleDetails`, `ScheduleEmailIds`) referenced locally,
not inline objects.

And the shared parameters, defined once per file:

```jsonc
"components": { "parameters": {
  "org-id":       { "name": "ZANALYTICS-ORGID", "in": "header", "required": true,
                    "schema": { "type": "string" },
                    "description": "Organization ID. It is shown in the Zoho Analytics UI under Settings > Organisation." },
  "workspace-id": { "name": "workspace-id", "in": "path", "required": true,
                    "schema": { "type": "string" }, "description": "ID of the workspace." },
  "schedule-id":  { "name": "schedule-id", "in": "path", "required": true,
                    "schema": { "type": "string" }, "description": "ID of the email schedule." }
} }
```

Those `description` strings become the rows in `/foundations/identifiers.md`.

---

## 4. The SDK samples (knowledge base 2 — `analytics-oas-samples`)

`v2.0/zenesis-oas-samples/schedules-alerts-grouped-api-samples.json` — keyed by the **exact path
template** and the **lower-case method**, with all nine languages:

```jsonc
{
  "/restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}": {
    "put": {
      "Curl":   { "snippets": [ { "code": "curl \"https://analyticsapi.zoho.com/restapi/v2/workspaces/35130000001055707/emailschedules/35130000001056601\" -X 'PUT' -H 'ZANALYTICS-ORGID: <org-id>' -H 'Authorization: Zoho-oauthtoken <access_token>' --data-urlencode 'CONFIG={\"scheduleName\":\"Monthly Sales Report\",…}'" } ] },
      "C#": {}, "Go": {}, "Java": {}, "Php": {}, "Python": {}, "Node": {}, "Ruby": {}, "Deluge": {}
    }
  }
}
```

The snippets use the house illustrative IDs (`orgId` 55522777, `workspaceId` 35130000001055707),
not the markdown's sample IDs. See that skill's `references/language-templates.md`.

---

## 5. What the generated knowledge bases make of it

### `v2.0/oas/schedules-alerts-grouped-api.json` (`analytics-oas`)

The same operation with: `x-zenesis-title` removed; `x-zenesis-statuscodes` folded into the
`description` as an `Error codes` table; the example's `description`/`summary` **un-swapped** back to
the OpenAPI convention; the first example copied onto `components.schemas.UpdateEmailScheduleConfig`
as `examples: [ … ]`; and the `4XX`/`500` `$ref`s rewritten to the published URL.

### `v2.0/okf/domains/schedules-and-alerts/email-schedules/update-email-schedule.md` (`analytics-okf`)

One `API Endpoint` concept, filename `kebab(operationId)`, with frontmatter

```yaml
type: API Endpoint
title: Update Email Schedule
api:
  operation_id: updateEmailSchedule
  method: PUT
  path: /restapi/v2/workspaces/{workspace-id}/emailschedules/{schedule-id}
  domain: schedules-and-alerts
  group: email-schedules
  oauth_scopes: [ZohoAnalytics.modeling.update]
  org_id_header: required
  config_parameter: { location: form, required: true }
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  permission_required: The authenticated user must be an Account Admin or …
  error_codes: [7103, 7301, 7812, 8000, …]
  sdk_examples: /sdk-examples/schedules-and-alerts/email-schedules/update-email-schedule.md
status: stable
```

and a body assembled from both sides: `# Summary`, `# Endpoint`, `# Request`, `# Response`,
`# Examples`, `# Notes & Behaviour`, `# Error Codes`, `# Related`. Plus an `SDK Example` concept at
`/sdk-examples/schedules-and-alerts/email-schedules/update-email-schedule.md`, a row in
`/endpoint-catalog.md` and `/references/endpoint-catalog.json`, rows in
`/foundations/error-codes.md`, `permission-matrix.md`, `oauth-scopes.md`, and a line in the group
and domain overviews.

### `v2.0/postman/Zoho Analytics REST APIs.postman_collection.json` (`analytics-postman`)

One request named **Update Email Schedule** in `⏰ Schedules & Alerts › Email Schedules`:
`PUT https://{{analytics-domain}}/restapi/v2/workspaces/{{workspace-id}}/emailschedules/{{schedule-id}}`,
header `ZANALYTICS-ORGID: {{organization-id}}`, body `urlencoded` with `CONFIG` pretty-printed from
the operation's **first** example, and a description built from the OKF frontmatter plus the
`api-reference-links.json` entry for the title.

---

## 6. The chain of identity

One rename can break four knowledge bases. These must move together:

| If you change… | …you must also change |
|---|---|
| the markdown `## N. Title` | `summary` **and** `x-zenesis-title`; the `## Index` row; `tools/postman/api-reference-links.json`; `ID_SOURCES` in `build_okf.py` if the endpoint returns an identifier |
| `operationId` | nothing else by hand — but the OKF endpoint and SDK-example filenames change, so links to them change |
| the path template | the samples key; the `## Index` row; the markdown `| **URL** |` row |
| the domain `slug` | **don't.** It renames four files and breaks every published consumer |
| a group's `okf.slug` | the bundle directory, every link into it, and `LEGACY_ALIAS` if the legacy link name no longer kebabs to it |
