---
type: API Endpoint
title: Create Alert
description: Creates an alert on the specified report and returns its id.
resource: "https://analyticsapi.zoho.com/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts"
tags:
  - zoho-analytics
  - rest-api-v2
  - schedules-and-alerts
  - data-alerts
  - post
  - modeling
api:
  operation_id: createAlert
  method: POST
  path: "/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts"
  domain: schedules-and-alerts
  group: data-alerts
  oauth_scopes:
    - ZohoAnalytics.modeling.create
  org_id_header: required
  config_parameter:
    location: form
    required: true
  request_content_type: application/x-www-form-urlencoded
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the view's workspace, or hold the CREATEALERT (Manage Data Alerts) permission on that specific view."
  error_codes:
    - 7103
    - 7104
    - 7301
    - 7319
    - 7387
    - 8060
    - 8078
    - 8079
    - 8080
    - 8083
    - 8119
    - 8241
    - 8245
    - 8504
    - 8535
  openapi:
    file: "/references/openapi/schedules-alerts-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1alerts/post"
    config_schema: CreateAlertConfig
    response_schema: CreateAlertResponse
  sdk_examples: "/sdk-examples/schedules-and-alerts/data-alerts/create-alert.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/schedules-alerts-grouped-api.json"
    title: OpenAPI 3 specification - schedules-alerts-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-26T10:54:58Z
generated:
  by: process:build_okf
  at: 2026-10-27T19:31:48Z
status: stable
---

# Summary

**POST `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts`** - Create Alert (Data Alerts / Schedules & Alerts).

Creates an alert on the specified report and returns its id. The view must be a Chart (`AnalysisView`), `Pivot` or `SummaryView`; the alert is created **live**, with its schedule registered immediately.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createAlert` |
| HTTP method | POST |
| URL | `/restapi/v2/workspaces/{workspace-id}/views/{view-id}/alerts` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be the DB Owner (Account Admin, Organization Admin or Workspace Admin) of the view's workspace, or hold the CREATEALERT (Manage Data Alerts) permission on that specific view. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`schedules-alerts-grouped-api.json`](../../../references/openapi/schedules-alerts-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1workspaces~1{workspace-id}~1views~1{view-id}~1alerts/post`; CONFIG schema `CreateAlertConfig`; response schema `CreateAlertResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID, shown in the Zoho Analytics UI under Settings > Organisation. See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{view-id}` | string | ID of the view. | [How to obtain](../../../foundations/identifiers.md#view-id) |

## CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Max Length | Description |
|-----------|------|-----------|---------|------------|-------------|
| `alertName` | String | **Yes** | — | 100 | Display name of the alert. Must be **unique within the view** (`32000011` otherwise) and non-blank (`32000005`). It can be changed later through [Update Alert](update-alert.md). |
| `summaryType` | String (enum) | Conditional | `data` | 50 | Which slice of the report the rules are evaluated against. **Mandatory when the view is a Pivot Table** — omitting it there is `8079`. For Chart and Summary views it defaults to `data`. See [`summaryType` Values](#summarytype-values). |
| `rowAxis` | String | Conditional | — | — | `viewColumnIndex` of the row-axis column of a Pivot / Summary report. **Mandatory when `summaryType` is `subTotal`** on a Pivot or Summary view (`32000044` otherwise); meaningless and ignorable elsewhere. Must resolve to a column of this view (`32000041` / `32000029`). Send it as a **string**. |
| `columnAxis` | String | No | — | — | `viewColumnIndex` of the column-axis column of a Pivot / Summary report. Same validation as `rowAxis`, but never mandatory. |
| `conditionExpression` | String | Conditional | `(1)` | 1000 | Boolean expression combining the rules by their 1-based position in `rules[]`. Allowed tokens are rule numbers, `AND`, `OR`, `(` and `)` — e.g. `"(1 AND 2) OR 3"`. **Mandatory when `rules` has more than one entry** (`8079` otherwise); with a single rule it defaults to `(1)`. The grammar is validated strictly: unbalanced parentheses or a dangling operator is `32000024`, a reference outside `1..rules.length` is `32000020`, a blank value is `32000015`. |
| `notifyOnChange` | Boolean | No | `false` | — | When `true`, a notification is sent only when the alert's state **changes** (the condition turning true after having been false) rather than on every matching evaluation. |
| `isAnomaly` | Boolean | No | — | — | **Accepted but ignored.** The server derives it from whether `rules[]` carries `anomaly` objects and overwrites whatever you send. It is returned by [Get Alert Configuration](get-alert-configuration.md) so that response can be posted back unchanged. |
| `scheduleDetails` | JSONObject | **Yes** | — | 5000 | How often the alert is evaluated. See [`scheduleDetails` Fields](#scheduledetails-fields). |
| `email` | JSONObject | No\* | — | 10000 | E-mail notification channel. See [`email` Fields](#email-fields). |
| `notification` | JSONObject | No\* | — | 10000 | In-product (WMS) notification channel. See [`notification` Fields](#notification-fields). |
| `slack` | JSONObject | No\* | — | 50000 | Slack incoming-webhook channel. See [`slack` and `msteams` Fields](#slack-and-msteams-fields). |
| `msteams` | JSONObject | No\* | — | 50000 | Microsoft Teams incoming-webhook channel. Identical shape to `slack`. |
| `webhook` | JSONObject | No\* | — | 100000 | Generic HTTPS webhook channel. See [`webhook` Fields](#webhook-fields). |
| `workflows` | JSONArray of JSONObject | No | — | 10000 | **Rejected by this API** with `32000049`. Zoho Flow workflow mappings can only be re-asserted through [Update Alert](update-alert.md), because the mapping cannot exist before the alert does. |
| `actionsByFlow` | JSONArray of JSONObject | No | — | 100000 | **Rejected by this API** with `32000049`, for the same reason as `workflows`. |
| `rules` | JSONArray of JSONObject | **Yes** | — | 100000 | The evaluation rules. **1–10 entries** — more is `32000018`, none is `32000006`. See [`rules` Fields](#rules-fields). |
| `validateSystemTags` | Boolean | No | `true` | — | When `true` (the default) and the alert attaches the report to an e-mail, the view's **Data Warning** system tags are checked and creation is refused with `8241` if a restricted tag is present. Set it to `false` to create the alert anyway. It has no effect when no report is attached. |

\* **At least one notification channel is required.** `email`, `notification`, `slack`, `msteams` and `webhook` are each individually optional, but the request must produce at least one *stored* channel or it fails with `32000001` — and a channel object that resolves to no recipient (an `email` with `notifyAdmins: false` and empty `emailIds` / `groupIds`, or a `notification` with both flags `false`) is discarded with `32000013` rather than stored.

> **`cliq` is not accepted.** The Zoho Cliq channel exists in the product's legacy alert model but is deliberately not exposed by the V2 API; sending it has no effect.

### `summaryType` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `data` | Evaluate the rules against the report's data rows. | The default for Chart and Summary views. |
| `subTotal` | Evaluate against sub-total rows. | Pivot / Summary views only. Requires `rowAxis` (`32000044`). |
| `grandTotal` | Evaluate against the single grand-total row. | Pivot / Summary views only. |

Any other value is [`8119`](../../../foundations/error-codes.md#error-8119).

### `scheduleDetails` Fields

| Field | Type | Mandatory | Default | Description |
|-------|------|-----------|---------|-------------|
| `calendarFrequency` | String (enum) | **Yes** | — | `hourly`, `daily`, `weekly`, `monthly` or `yearly`. Case-insensitive on input, normalised to lower case. Any other value is `8119`. See [`calendarFrequency` Values](#calendarfrequency-values). |
| `interval` | Integer | **Yes** for `hourly` | `1` | "Repeat every N units of `calendarFrequency`". Permitted values depend on the frequency: `hourly` → `1`, `2`, `3`, `4`, `6` or `12`; `daily` → 1–7; `weekly` → 1–4; `monthly` → 1–12; `yearly` → 1–5. Out of range is `8119`. |
| `timeZone` | String | No | Caller's profile time zone, else `GMT` | IANA time zone id used to evaluate the schedule — `Asia/Kolkata`, `America/New_York`, `Europe/London`, `UTC`. An unrecognised id, or an explicit `null` / empty string, is `32000045`. |
| `hour` | Integer | **Yes** except for `hourly` | — | Hour of day, **0–23**. Out of range is `8119`. Not applicable to `hourly` (`32000052`). |
| `minute` | Integer | **Yes** except for `hourly` | — | Minute of hour. Must be a **multiple of 5 in the range 0–55**; `9` is `8119`. Not applicable to `hourly`. |
| `skipWeekends` | Boolean | No | `false` | Skip the evaluations that fall on weekend days. **You do not choose the days** — they are the weekend of the schedule time zone's locale (Sunday for `Asia/Kolkata`; Saturday and Sunday for `America/New_York` and `UTC`; Friday and Saturday for `Asia/Riyadh`). Applicable only to `hourly` and `daily` (`32000052` elsewhere). |
| `weekDays` | JSONArray of Integer | **Yes** for `weekly` | — | Days of the week, **1 = Sunday … 7 = Saturday**. More than one may be selected (`[2, 4]` = Monday and Wednesday); a single day is still a one-entry array (`[6]`). Duplicates are dropped. Applicable only to `weekly`. |
| `monthDays` | JSONArray of Integer | Conditional | — | Dates of the month, **1–31**, or the single-entry list `[99]` meaning "last day of the month" (`99` cannot be combined with other dates). For `monthly` several dates may be selected (`[1, 15]`); for `yearly` the array must carry **exactly one** entry, because a yearly schedule stores one date per selected month. One of `monthDays` or (`weekOfMonth` + `dayOfWeek`) is mandatory for `monthly` and `yearly` — see below. |
| `weekOfMonth` | Integer | Conditional | — | Which occurrence of `dayOfWeek` within the month: **1 = first … 4 = fourth, 5 = last**. Used together with `dayOfWeek`. Applicable only to `monthly` and `yearly`. |
| `dayOfWeek` | Integer | Conditional | — | Day of the week for the "Nth weekday" form, **1 = Sunday … 7 = Saturday**. `weekOfMonth: 2, dayOfWeek: 3` reads "the second Tuesday of the month". Used together with `weekOfMonth`. |
| `months` | JSONArray of Integer | **Yes** for `yearly` | — | Months in which the alert runs, **1 = January … 12 = December**. More than one may be selected (`[1, 7]`). Applicable only to `yearly`. |

**Which field applies to which `calendarFrequency`** — a field sent for a frequency it does not apply to is rejected with `32000052` (`SCHEDULE_ATTRIBUTE_NOT_APPLICABLE`) rather than silently ignored:

| Field | `hourly` | `daily` | `weekly` | `monthly` | `yearly` |
|---|---|---|---|---|---|
| `calendarFrequency` | ✔ | ✔ | ✔ | ✔ | ✔ |
| `interval` | ✔ | ✔ | ✔ | ✔ | ✔ |
| `timeZone` | ✔ | ✔ | ✔ | ✔ | ✔ |
| `hour` | — | ✔ | ✔ | ✔ | ✔ |
| `minute` | — | ✔ | ✔ | ✔ | ✔ |
| `skipWeekends` | ✔ | ✔ | — | — | — |
| `weekDays` | — | — | ✔ | — | — |
| `monthDays` | — | — | — | ✔ | ✔ |
| `weekOfMonth` | — | — | — | ✔ | ✔ |
| `dayOfWeek` | — | — | — | ✔ | ✔ |
| `months` | — | — | — | — | ✔ |

**Monthly and yearly take exactly one of two day forms.** Supplying both, or neither, is `32000051` (`INVALID_SCHEDULE_ATTRIBUTE_COMBINATION`):

| Form | Fields | Reads as |
|---|---|---|
| By date | `monthDays` | "on the 1st and the 15th", or "on the last day" (`[99]`) |
| By weekday | `weekOfMonth` **and** `dayOfWeek` | "on the second Tuesday", or "on the last Friday" (`weekOfMonth: 5`) |

**Complete shapes, one per frequency:**

| Frequency | `scheduleDetails` |
|---|---|
| Hourly | `{"calendarFrequency": "hourly", "interval": 6, "skipWeekends": true}` |
| Daily | `{"calendarFrequency": "daily", "interval": 3, "hour": 9, "minute": 30, "skipWeekends": true}` |
| Weekly | `{"calendarFrequency": "weekly", "interval": 2, "hour": 9, "minute": 30, "weekDays": [2, 4]}` |
| Monthly — by date | `{"calendarFrequency": "monthly", "hour": 9, "minute": 30, "monthDays": [1, 15]}` |
| Monthly — by weekday | `{"calendarFrequency": "monthly", "interval": 3, "hour": 9, "minute": 30, "weekOfMonth": 5, "dayOfWeek": 6}` |
| Yearly — by date | `{"calendarFrequency": "yearly", "hour": 9, "minute": 30, "months": [1, 7], "monthDays": [15]}` |
| Yearly — by weekday | `{"calendarFrequency": "yearly", "interval": 2, "hour": 6, "minute": 0, "months": [4], "weekOfMonth": 1, "dayOfWeek": 2}` |

### `calendarFrequency` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `hourly` | Every N hours, around the clock. | Carries no `hour` / `minute`. `interval` is **mandatory** and limited to 1, 2, 3, 4, 6 or 12. |
| `daily` | Every N days at a fixed time. | `interval` 1–7. |
| `weekly` | Every N weeks on the selected `weekDays`. | `interval` 1–4. `weekDays` mandatory. |
| `monthly` | Every N months, on a date or an Nth weekday. | `interval` 1–12. Exactly one day form. |
| `yearly` | Every N years, in the selected `months`. | `interval` 1–5. `months` mandatory, exactly one day form, `monthDays` limited to a single entry. |

### `email` Fields

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `subject` | String | **Yes** | — | 500 | E-mail subject line. A blank value is `32000012`. |
| `message` | String | **Yes** | — | 5000 | E-mail body. HTML is permitted and filtered through AntiSamy. When `systemMailId` is `true` a stricter filter that strips all HTML is applied instead. |
| `notifyAdmins` | Boolean | No | `false` | — | Include the workspace admins / DB Owner in the recipient list. |
| `emailIds` | JSONArray of String | No | `[]` | — | Explicit recipient addresses. **Maximum 25 entries** — the request template permits 1,000, but the server refuses more than 25 with `32000007`. Blank entries are skipped. |
| `groupIds` | JSONArray of String | No | `[]` | — | Workspace group ids whose members receive the e-mail, as numeric **strings**. 1–1000 entries. |
| `includeReport` | Boolean | No | `false` | — | Attach or inline the report itself. When `true`, `attachmentType` becomes mandatory (`8079`). |
| `attachmentType` | String (enum) | **Yes** when `includeReport` is `true` | — | — | `inline` or `attachment`. Any other value is `8119`. Ignored when `includeReport` is `false`. See [`attachmentType` Values](#attachmenttype-values). |
| `attachFilteredDataset` | Boolean | No | `false` | — | Also attach the dataset filtered to the rows that matched the alert criteria. Independent of `includeReport` — it may be set on its own. |
| `systemMailId` | Boolean | No | `false` | — | `true` sends from the Zoho Analytics system mail id; `false` sends from the alert creator's address. Organisation-level display-e-mail settings can override this. |

> **The channel must resolve to a recipient.** If `notifyAdmins` is `false` and both `emailIds` and `groupIds` are empty, the channel is not stored and the request fails with `32000013`.

### `attachmentType` Values

| Value | Meaning |
|-------|---------|
| `inline` | The report is rendered inside the e-mail body. |
| `attachment` | The report is sent as a file attachment. |

### `notification` Fields

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `notifyAdmins` | Boolean | **Yes** | — | — | Notify the workspace admins / DB Owner. |
| `notifySharedUsers` | Boolean | **Yes** | — | — | Notify every user the view is shared with. |
| `subject` | String | **Yes** | — | 500 | Notification title. A blank value is `32000012`. |
| `message` | String | **Yes** | — | 5000 | Notification body. HTML is filtered through AntiSamy. |

> **Both flags are mandatory and at least one must be `true`.** `{"notifyAdmins": false, "notifySharedUsers": false}` is not stored and fails with `32000013`.

### `slack` and `msteams` Fields

Both channels take the same object.

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `url` | String | **Yes** | — | 5000 | Incoming-webhook URL of the channel. **Must start with `https://`** — anything else is `32000025`. |
| `messageType` | String (enum) | **Yes** | — | — | `STANDARD` or `CUSTOM`. Case-insensitive on input, normalised to upper case. See [`messageType` Values](#messagetype-values). |
| `subject` | String | **Yes** when `messageType` is `STANDARD` | — | 500 | Message subject. Blank or absent under `STANDARD` is `32000026`. Stored as `""` under `CUSTOM`. |
| `message` | String | No | `""` | 5000 | Message body, used only under `STANDARD`. |
| `payload` | String | **Yes** when `messageType` is `CUSTOM` | — | 50000 | The raw body POSTed to the webhook, supplied as a **JSON document serialised into a string**. It must parse as a JSON object or array, otherwise `32000027`. Ignored under `STANDARD`. |

### `messageType` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `STANDARD` | Zoho Analytics composes the message from `subject` and `message`. | `subject` mandatory (`32000026`). `payload` is discarded. |
| `CUSTOM` | Your own `payload` is POSTed verbatim, letting you use Slack Block Kit or a Teams message card. | `payload` mandatory and must be valid JSON (`32000027`). `subject` and `message` are discarded. |

### `webhook` Fields

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `url` | String | **Yes** | — | 5000 | Target URL. **Must start with `https://`** — anything else is `32000025`. |
| `method` | String (enum) | No | `POST` | 10 | HTTP method used to invoke the webhook. See [`method` Values](#method-values). |
| `body` | String | No | `""` | 50000 | Raw request body sent with the call. Not parsed or validated. |
| `params` | JSONArray of JSONObject | No | — | 50000 | Query / form parameters appended to the request, **0–10** entries. See [`params` and `headers` Fields](#params-and-headers-fields). |
| `headers` | JSONArray of JSONObject | No | — | 10000 | Additional HTTP headers sent with the request, **0–10** entries. Same entry shape as `params`. See [`params` and `headers` Fields](#params-and-headers-fields). |

### `method` Values

| Value | Meaning |
|-------|---------|
| `GET` | Invoke the webhook with an HTTP `GET`. |
| `POST` | Invoke the webhook with an HTTP `POST`. The default. |
| `PUT` | Invoke the webhook with an HTTP `PUT`. |
| `PATCH` | Invoke the webhook with an HTTP `PATCH`. |
| `DELETE` | Invoke the webhook with an HTTP `DELETE`. |

### `params` and `headers` Fields

Both arrays carry the same entry shape.

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `name` | String | **Yes** | — | 255 | Parameter or header name. Minimum 1 character. |
| `value` | String | **Yes** | — | 5000 | Parameter or header value. Stored encrypted and returned decrypted by [Get Alert Configuration](get-alert-configuration.md). |

### `rules` Fields

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `operator` | String | **Yes** | — | 50 | The comparison. It must appear in the column's `allowedOperators` from [Get View Metadata For Alert](get-view-metadata-for-alert.md) — anything else is `8119`. Full catalogue in [Enum and Value Reference](overview.md#enum-and-value-reference). |
| `viewColumnIndex` | String | **Yes** for non-anomaly rules | — | — | The column the rule tests, as a `viewColumnIndex` **string**. **Must be omitted on anomaly rules** (`32000046`); the column is resolved from `anomaly.name` instead. An index that does not resolve is `32000041`. |
| `type` | String (enum) | No | `constant` | — | What the column is compared against: `constant`, `column` or `threshold`. It must appear in the column's `allowedRuleTypes` (`8119` otherwise). See [`type` Values](#type-values). |
| `values` | JSONArray of String | Conditional | — | 5000 | The comparison value(s), always **strings**, **1–300** entries. How many are required depends on the operator and the column — see the value-shape table below. Supplying values for a no-value operator is `32000047`. |
| `anomaly` | JSONObject | No | — | 10000 | Turns the rule into an **anomaly rule**. When any rule carries it, **every** rule must (`32000017`), and the alert must be on a Chart view (`32000019`). See [`anomaly` Fields](#anomaly-fields). |

**The shape of `values` is decided by the column as much as by the operator:**

| Case | `values` | Error if wrong |
|---|---|---|
| `type` is `column` | Exactly one entry: the `viewColumnIndex` of another **NUMBER** column of the same view. | `32000035` (missing), `32000036` (not numeric), `32000041` / `32000037` (not in this view) |
| `type` is `threshold` | Exactly one entry: the threshold **display name** from `viewColumns[].thresholds`, e.g. `"T1"`. | `32000035` (missing), `32000038` (unknown threshold) |
| `btw` / `notbtw` | Exactly two entries — lower bound, then upper bound. | `32000039` |
| `is` / `isnot` on a **categorical or date-bucket** column | One or more entries (multi-select). A comma inside a categorical token is escaped automatically. | `32000040` |
| `is` / `isnot` on a **NUMBER**, `DATE` or `TIMESTAMP` column | Exactly **one** entry — these are scalar comparators here, not multi-select. | `32000053` |
| `isn`, `notisn`, `sinceLastAlert` and the no-value date buckets (`curYear`, `prevMonth`, `today`, …) | **Omit `values` entirely.** | `32000047` if supplied |
| `prevN…` / `lastN…` / `nextN…` date buckets | Exactly one entry: the N, as a numeric string. | `32000040`, `32000053` |
| Every other scalar operator (`gt`, `lt`, `gte`, `lte`) | Exactly one entry. | `32000040` (none), `32000053` (more than one) |

**Date and timestamp columns:** when the rule column's operation is `DATE` or `TIMESTAMP` and the operator is one of `is`, `isnot`, `gt`, `lt`, `gte`, `lte`, `btw`, `notbtw`, every value must be `yyyy-MM-dd HH:mm:ss` or `yyyy-MM-dd` (the time then defaults to `00:00:00`). Any other shape is `32000028`. The server normalises these into its internal form on write and converts them back on [Get Alert Configuration](get-alert-configuration.md), so the value round-trips.

### `type` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `constant` | Compare the column against a literal value. | Always available. The default when `type` is absent or blank. |
| `column` | Compare the column against another NUMBER column of the same view. | Only when the view has **at least two** NUMBER columns. Chart views only (`32000019`). |
| `threshold` | Compare the column against a chart threshold (`T1`, `T2`, …). | Only when the column has at least one threshold. Chart views only (`32000019`). |

### `anomaly` Fields

| Field | Type | Mandatory | Default | Max Length | Description |
|-------|------|-----------|---------|------------|-------------|
| `name` | String | **Yes** | — | 100 | Name of an anomaly definition configured on the view, taken verbatim from `anomalies[].anomalyName` of [Get View Metadata For Alert](get-view-metadata-for-alert.md). An unknown name is `32000042`. This is also what resolves the rule's column, which is why `viewColumnIndex` must be absent. |
| `value` | String | No | `""` | 1000 | The operator's argument, when the chosen anomaly operator takes one (for example the N of `lastNMonths`). |
| `comboType` | String (enum) | No | `""` | 5 | How matched anomalies are aggregated: `top` or `all`. See [`comboType` Values](#combotype-values). |
| `comboTypeValue` | String | **Yes** when `comboType` is `top` | `""` | 10 | The number of top anomalies to consider, as a numeric string. Must parse to a **positive** integer, otherwise `32000021`. |

### `comboType` Values

| Value | Meaning | Restrictions |
|-------|---------|--------------|
| `top` | Consider only the N most significant anomalies. | `comboTypeValue` must be a positive integer (`32000021`). |
| `all` | Consider every detected anomaly. | `comboTypeValue` is ignored. |

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | `"Create alert"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.alertId` | String | Id of the alert just created, numeric but serialised as a **string**. This is the `<alert-id>` for [Get Alert Configuration](get-alert-configuration.md), [Update Alert](update-alert.md), [Change Alert Status](change-alert-status.md), [Run Alert](run-alert.md), [Get Alert Events](get-alert-events.md), and the `alertIds` array of [Delete Alerts](delete-alerts.md). |

# Examples

## Sample Requests

**Case 1 — Minimal valid alert: one rule, one channel, daily schedule**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Sales Drop Alert",
    "scheduleDetails": {
        "calendarFrequency": "daily",
        "hour": 9,
        "minute": 0
    },
    "email": {
        "notifyAdmins": true,
        "subject": "Sales dropped below threshold",
        "message": "Please review the report."
    },
    "rules": [
        {
            "operator": "lt",
            "viewColumnIndex": "2",
            "type": "constant",
            "values": ["1000"]
        }
    ]
}
```

**Case 2 — Three rules combined by a custom `conditionExpression`, with an inline report attachment**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Sales / Profit / Discount Monitor",
    "summaryType": "data",
    "conditionExpression": "(1 AND 2) OR 3",
    "notifyOnChange": false,
    "scheduleDetails": {
        "calendarFrequency": "daily",
        "interval": 1,
        "hour": 9,
        "minute": 0,
        "timeZone": "Asia/Kolkata",
        "skipWeekends": true
    },
    "email": {
        "notifyAdmins": true,
        "emailIds": ["jane.doe@example.com", "manager@example.com"],
        "subject": "Sales / Profit / Discount alert",
        "message": "One of the configured rules has been breached. Please review.",
        "includeReport": true,
        "attachmentType": "inline",
        "attachFilteredDataset": true,
        "systemMailId": false
    },
    "rules": [
        {
            "operator": "lt",
            "viewColumnIndex": "2",
            "type": "constant",
            "values": ["1000"]
        },
        {
            "operator": "lt",
            "viewColumnIndex": "3",
            "type": "constant",
            "values": ["100"]
        },
        {
            "operator": "gt",
            "viewColumnIndex": "4",
            "type": "constant",
            "values": ["25"]
        }
    ]
}
```

**Case 3 — Threshold rule and column-vs-column rule, hourly schedule, in-app notification**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Sales above T1 or below Profit",
    "conditionExpression": "(1 OR 2)",
    "notifyOnChange": true,
    "scheduleDetails": {
        "calendarFrequency": "hourly",
        "interval": 3,
        "timeZone": "Asia/Kolkata",
        "skipWeekends": true
    },
    "notification": {
        "notifyAdmins": true,
        "notifySharedUsers": true,
        "subject": "Sales crossed T1",
        "message": "Sales has crossed threshold T1 on the Sales By Region chart."
    },
    "rules": [
        {
            "operator": "gt",
            "viewColumnIndex": "2",
            "type": "threshold",
            "values": ["T1"]
        },
        {
            "operator": "lt",
            "viewColumnIndex": "2",
            "type": "column",
            "values": ["3"]
        }
    ]
}
```

**Case 4 — Anomaly alert: no `viewColumnIndex`, every rule carries `anomaly`**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Sales spike anomaly",
    "notifyOnChange": false,
    "scheduleDetails": {
        "calendarFrequency": "daily",
        "hour": 7,
        "minute": 0
    },
    "notification": {
        "notifyAdmins": true,
        "notifySharedUsers": false,
        "subject": "Sales spike detected",
        "message": "An anomaly was detected on Sales."
    },
    "rules": [
        {
            "operator": "sinceLastAlert",
            "anomaly": {
                "name": "Sales Spike",
                "value": "",
                "comboType": "top",
                "comboTypeValue": "5"
            }
        }
    ]
}
```

**Case 5 — Pivot report, sub-total slice: `summaryType` and `rowAxis` are both required**

```http
POST /restapi/v2/workspaces/137687000271334001/views/466206000000105001/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Region sub-total monitor",
    "summaryType": "subTotal",
    "rowAxis": "1",
    "columnAxis": "5",
    "notifyOnChange": true,
    "scheduleDetails": {
        "calendarFrequency": "weekly",
        "interval": 2,
        "hour": 9,
        "minute": 0,
        "weekDays": [2, 4]
    },
    "email": {
        "notifyAdmins": true,
        "groupIds": ["137687000002108009"],
        "subject": "Regional sub-total alert",
        "message": "Regional sub total has crossed the configured limit.",
        "includeReport": true,
        "attachmentType": "attachment"
    },
    "rules": [
        {
            "operator": "btw",
            "viewColumnIndex": "2",
            "type": "constant",
            "values": ["10000", "50000"]
        }
    ]
}
```

**Case 6 — Multi-select dimensional rule, a date rule, and a no-value rule across three channels**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Recent East/West orders",
    "conditionExpression": "(1 AND 2) AND 3",
    "scheduleDetails": {
        "calendarFrequency": "monthly",
        "hour": 7,
        "minute": 15,
        "monthDays": [1, 15],
        "timeZone": "Europe/London"
    },
    "slack": {
        "url": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXX",
        "messageType": "STANDARD",
        "subject": "New East/West orders",
        "message": "Orders from the East and West regions were detected."
    },
    "msteams": {
        "url": "https://example.webhook.office.com/webhookb2/00000000-0000-0000-0000-000000000000",
        "messageType": "CUSTOM",
        "payload": "{\"text\":\"New East/West orders detected\"}"
    },
    "webhook": {
        "url": "https://example.com/zoho-analytics/alert-hook",
        "method": "POST",
        "body": "{\"event\":\"newOrders\",\"severity\":\"info\"}",
        "params": [
            {"name": "source", "value": "analytics"}
        ],
        "headers": [
            {"name": "X-Source", "value": "ZohoAnalytics"}
        ]
    },
    "rules": [
        {
            "operator": "is",
            "viewColumnIndex": "1",
            "type": "constant",
            "values": ["East", "West"]
        },
        {
            "operator": "gte",
            "viewColumnIndex": "6",
            "type": "constant",
            "values": ["2026-01-01 00:00:00"]
        },
        {
            "operator": "notisn",
            "viewColumnIndex": "7",
            "type": "constant"
        }
    ]
}
```

**Case 7 — Yearly "by weekday" schedule, every 2 years, delivered to a webhook**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Biennial audit trigger",
    "summaryType": "grandTotal",
    "scheduleDetails": {
        "calendarFrequency": "yearly",
        "interval": 2,
        "hour": 6,
        "minute": 0,
        "months": [4],
        "weekOfMonth": 1,
        "dayOfWeek": 2
    },
    "webhook": {
        "url": "https://example.com/zoho-analytics/audit-hook",
        "method": "POST",
        "body": "{\"event\":\"biennialAudit\"}"
    },
    "rules": [
        {
            "operator": "gte",
            "viewColumnIndex": "4",
            "type": "constant",
            "values": ["1000000"]
        }
    ]
}
```

**Case 8 — `workflows` supplied on create (rejected)**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Alert with workflow",
    "scheduleDetails": {
        "calendarFrequency": "daily",
        "hour": 9,
        "minute": 0
    },
    "email": {
        "notifyAdmins": true,
        "subject": "Alert",
        "message": "Body."
    },
    "workflows": [
        {"id": "137687000012564035"}
    ],
    "rules": [
        {
            "operator": "lt",
            "viewColumnIndex": "2",
            "type": "constant",
            "values": ["1000"]
        }
    ]
}
```

**Case 9 — `skipWeekends` on a weekly schedule (rejected)**

```http
POST /restapi/v2/workspaces/137687000271334001/views/137687000006991601/alerts HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "alertName": "Weekly with weekend skip",
    "scheduleDetails": {
        "calendarFrequency": "weekly",
        "hour": 9,
        "minute": 0,
        "weekDays": [6],
        "skipWeekends": true
    },
    "email": {
        "notifyAdmins": true,
        "subject": "Alert",
        "message": "Body."
    },
    "rules": [
        {
            "operator": "lt",
            "viewColumnIndex": "2",
            "type": "constant",
            "values": ["1000"]
        }
    ]
}
```

## Sample Responses

**HTTP 200 OK — Alert created**

```json
{
    "status": "success",
    "summary": "Create alert",
    "data": {
        "alertId": "137687000010815003"
    }
}
```

**HTTP 400 Bad Request — Failure paired with Case 8**

```json
{
    "status": "failure",
    "summary": "WORKFLOWS_NOT_ALLOWED_IN_CREATE",
    "data": {
        "errorCode": 32000049,
        "errorMessage": "The attribute 'workflows' is not supported in Create Alert. This attribute is allowed only in Update Alert."
    }
}
```

**HTTP 400 Bad Request — Failure paired with Case 9**

```json
{
    "status": "failure",
    "summary": "SCHEDULE_ATTRIBUTE_NOT_APPLICABLE",
    "data": {
        "errorCode": 32000052,
        "errorMessage": "The attribute 'skipWeekends' is not applicable when calendarFrequency is 'weekly'."
    }
}
```

**HTTP 400 Bad Request — No channel resolved to a recipient**

```json
{
    "status": "failure",
    "summary": "NOCHANNELINPUT",
    "data": {
        "errorCode": 32000001,
        "errorMessage": "Please select any one action to send alert notification."
    }
}
```

**HTTP 409 Conflict — The view carries a restricted Data Warning tag and the alert attaches the report**

```json
{
    "status": "failure",
    "summary": "SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION",
    "data": {
        "errorCode": 8241,
        "errorMessage": "To skip system tag validation, add the validateSystemTags parameter as 'false'."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create Alert](../../../sdk-examples/schedules-and-alerts/data-alerts/create-alert.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Nothing is echoed back** | The response carries the id only. To see how the server normalised what you sent — resolved column indexes, the canonical `scheduleDetails`, the defaulted `type` and `conditionExpression` — call [Get Alert Configuration](get-alert-configuration.md) with the returned `alertId`. |
| **The alert is created live** | Its schedule is registered immediately and it starts enabled, so an evaluation can occur before you have read the configuration back. Create it paused by following up with [Change Alert Status](change-alert-status.md) if that matters. |
| **Not idempotent** | A repeat of the same request fails on the unique-name check with `32000011`. There is no upsert mode. |
| **Every reference is validated against the live view** | Column indexes must resolve (`32000041`), threshold names must exist on that column (`32000038`), anomaly names must exist on the view (`32000042`), and a `type: "column"` rule must point at a NUMBER column of the same view (`32000036` / `32000037`). |
| **`type` defaults to `constant`** | An absent or blank `type` is treated as `constant`, which is also the only type always available. |
| **`isAnomaly` is derived, not accepted** | The server sets it from whether the rules carry `anomaly` objects. Anomaly rules are all-or-nothing (`32000017`), must not carry `viewColumnIndex` (`32000046`), and — like `threshold` rules — are valid only on Chart views (`32000019`). |
| **`workflows` and `actionsByFlow` are rejected here** | Both describe mappings that cannot exist before the alert does (`32000049`). Create the alert first, map the workflow in Zoho Flow, then re-assert it through [Update Alert](update-alert.md). |
| **`conditionExpression` silently defaults to `(1)`** | With several rules and no expression the request fails with `8079` rather than defaulting — but with exactly one rule the default applies. Always send an explicit expression when `rules` has more than one entry. |
| **`skipWeekends` does not let you choose the days** | They come from the schedule time zone's locale. Two alerts with the same flag but different `timeZone` values skip different days. |
| **Quota is not checked here** | The organisation's alert-schedule plan limit is enforced at **run** time (`6079`), not at creation. An alert can be created on a plan that cannot run it. |
| **System-tag gate** | With `validateSystemTags` left at `true` and an e-mail attachment configured, a restricted Data Warning tag on the view blocks creation with `8241` (HTTP 409). |
| **Responses are extensible** | Ignore unrecognised keys rather than validating against a closed schema. |
| **Dependency chain** | [Get View List](../../views-management/view-operations/get-views.md) → `<view-id>` → [Get View Metadata For Alert](get-view-metadata-for-alert.md) → `viewColumnIndex` → Create Alert → `data.alertId`. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and that the `ZANALYTICS-ORGID` header matches it. |
| [7104](../../../foundations/error-codes.md#error-7104) | 404 | `META_OBJECT_NOT_PRESENT` — View not found. | Verify `<view-id>` via [Get View List](../../views-management/view-operations/get-views.md). |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — The caller is neither the DB Owner nor a holder of `CREATEALERT` on this view, or the request arrived through a custom domain the workspace is not bound to. | Authenticate as the DB Owner or a user with Manage Data Alerts on that view, from the standard API host. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The view does not belong to the workspace in the URL. | Make `<workspace-id>` and `<view-id>` consistent. |
| [7387](../../../foundations/error-codes.md#error-7387) | 400 | `DBID_NOT_BELONGS_TO_ZSOID` — The workspace does not belong to the organisation in `ZANALYTICS-ORGID`. | Send the organisation id that owns the workspace. |
| [8060](../../../foundations/error-codes.md#error-8060) | 400 | `DOMAIN_NOT_EXIST` — The custom domain in the request host is not provisioned. | Use a domain you have purchased from Zoho Analytics, or the standard API host. |
| [8078](../../../foundations/error-codes.md#error-8078) | 400 | `EMPTY_JSON_ATTRIBUTE_FOUND` — A mandatory CONFIG attribute was sent with an empty value. | Give the named attribute a non-empty value. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — A mandatory attribute is missing: `alertName`, `scheduleDetails`, `rules`, `summaryType` on a Pivot view, `conditionExpression` with more than one rule, or `attachmentType` when `includeReport` is `true`. | Add the named attribute. |
| [8080](../../../foundations/error-codes.md#error-8080) | 400 | `INVALID_JSON_CONFIGURATION` — An attribute that must be a JSON string was sent as another type, typically `viewColumnIndex`, `rowAxis`, `columnAxis` or a `values` entry sent as a bare number. | Quote numeric identifiers and rule values: `"viewColumnIndex": "2"`, `"values": ["1000"]`. |
| [8083](../../../foundations/error-codes.md#error-8083) | 400 | `ORGID_NOT_PRESENT_IN_THE_HEADER` — `ZANALYTICS-ORGID` is missing. | Add the `ZANALYTICS-ORGID` request header. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE` — A value is outside its permitted set: an `operator` or `type` not in the column's `allowedOperators` / `allowedRuleTypes`, an unknown `summaryType` or `messageType`, an `attachmentType` other than `inline` / `attachment`, or a `scheduleDetails` number out of range (`hour`, `minute`, `interval`, `weekDays`, `monthDays`, `months`, `weekOfMonth`, `dayOfWeek`). | Take operators and rule types from [Get View Metadata For Alert](get-view-metadata-for-alert.md) and keep schedule numbers within the ranges in [`scheduleDetails` Fields](#scheduledetails-fields). |
| [8241](../../../foundations/error-codes.md#error-8241) | 409 | `SYSTEM_TAG_DATA_WARNING_V2_VALIDATION_CONFIRMATION` — The view carries a restricted Data Warning system tag and the alert attaches the report to an e-mail. HTTP 409. | Resolve the data warning, or resend with `"validateSystemTags": false`. |
| [8245](../../../foundations/error-codes.md#error-8245) | 404 | `INVALID_VIEW_TYPE_FOR_OPERATION` — The view is not a Chart, Pivot Table or Summary View. | Create the alert on a supported report type. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — The `CONFIG` parameter was not sent, or a templated attribute is below its minimum occurrence. | Send `CONFIG` as a URL-encoded form parameter containing a valid JSON object. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |

# Related

- [Data Alerts overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Schedules & Alerts](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get Alerts In Workspace](get-alerts-in-workspace.md), [Get Alerts In View](get-alerts-in-view.md), [Get View Metadata For Alert](get-view-metadata-for-alert.md), [Get Alert Configuration](get-alert-configuration.md), [Update Alert](update-alert.md), [Delete Alerts](delete-alerts.md), [Change Alert Status](change-alert-status.md), [Run Alert](run-alert.md), [Get Alert Events](get-alert-events.md).
- [SDK examples](../../../sdk-examples/schedules-and-alerts/data-alerts/create-alert.md).
