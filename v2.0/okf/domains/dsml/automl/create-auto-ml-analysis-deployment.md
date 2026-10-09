---
type: API Endpoint
title: Create AutoML Analysis Deployment
description: Creates a deployment for an AutoML analysis model.
resource: "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments"
tags:
  - zoho-analytics
  - rest-api-v2
  - dsml
  - automl
  - post
  - modeling
api:
  operation_id: createAutoMLAnalysisDeployment
  method: POST
  path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments"
  domain: dsml
  group: automl
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
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace."
  error_codes:
    - 7103
    - 7301
    - 7319
    - 8050
    - 8079
    - 8119
    - 8504
    - 8535
    - 8544
  openapi:
    file: "/references/openapi/dsml-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1automl~1workspaces~1{workspace-id}~1analysis~1{analysis-id}~1models~1{model-id}~1deployments/post"
    config_schema: CreateAutoMLAnalysisDeploymentConfig
    response_schema: CreateAutoMLAnalysisDeploymentResponse
  sdk_examples: "/sdk-examples/dsml/automl/create-auto-ml-analysis-deployment.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/dsml-grouped-api.json"
    title: OpenAPI 3 specification - dsml-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T08:29:02Z
generated:
  by: process:build_okf
  at: 2026-10-09T09:09:11Z
status: stable
---

# Summary

**POST `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments`** - Create AutoML Analysis Deployment (AutoML / Data Science & Machine Learning (AutoML)).

Binds a trained model to an input table and an output table so that predictions can be generated — on a recurring schedule, on demand, or both. Returns the new deployment ID and the ID of the output table it created.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createAutoMLAnalysisDeployment` |
| HTTP method | POST |
| URL | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/deployments` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`dsml-grouped-api.json`](../../../references/openapi/dsml-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1automl~1workspaces~1{workspace-id}~1analysis~1{analysis-id}~1models~1{model-id}~1deployments/post`; CONFIG schema `CreateAutoMLAnalysisDeploymentConfig`; response schema `CreateAutoMLAnalysisDeploymentResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.modeling.create`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |
| `Content-Type` | `application/x-www-form-urlencoded` | Required | The CONFIG JSON is sent as a form field named `CONFIG`. |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{analysis-id}` | string | ID of the AutoML analysis. | [How to obtain](../../../foundations/identifiers.md#analysis-id) |
| `{model-id}` | string | ID of the AutoML analysis model. | [How to obtain](../../../foundations/identifiers.md#model-id) |

## CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `inputTableId` | Long | **Yes** | — | ID of the table whose rows are scored. Must belong to `<workspace-id>` (`7319` otherwise) and must contain **every feature column the model was trained on** (`21000001` otherwise). |
| `outputTable` | String | **Yes** | — | Name of the table the predictions are written to. Created automatically if it does not exist. Must be non-empty (`21000037`) and at most 100 characters (`21000039`). |
| `outputColumns` | JSONArray of String | **Yes** | — | Columns copied from the input table into the output table alongside the prediction. 1–100 entries; must not be empty (`21000041`) and every name must exist in the input table. |
| `predictionColumn` | String | **Yes** | — | Name of the new column that holds the predicted value. Must be non-empty (`21000036`) and at most 100 characters (`21000040`). |
| `importType` | String (enum) | **Yes** | — | How results are written to the output table. `APPEND`, `TRUNCATEADD`, or `UPDATEADD`. Case-insensitive on input; an unrecognised value fails with `21000022`. See [`importType` Values](#importtype-values). |
| `serverOption` | Integer (enum) | **Yes** | — | Server memory for the scoring job: `1` = 8 GB, `2` = 16 GB, `3` = 32 GB. Any other value fails with `8119`. |
| `scheduleDetails` | JSONObject | **Yes** | — | When the deployment runs automatically. Send `{"calendarFrequency": "none"}` for an on-demand-only deployment. See [`scheduleDetails` Fields](#scheduledetails-fields). |
| `matchingColumns` | JSONArray of String | Conditional | — | **Mandatory when `importType` is `UPDATEADD`**, ignored otherwise. Columns used to match existing output rows. Must be non-empty (`21000038`), exist in the input table, and be a **subset of `outputColumns`** (`21000042` otherwise). 1–100 entries. |
| `timezone` | String | No | Organization default | Timezone the schedule runs in, e.g. `Asia/Kolkata`. Must be a recognised timezone name (`8050` otherwise). |

### `importType` Values

| Value | Behaviour |
|-------|-----------|
| `TRUNCATEADD` | Deletes all existing rows in the output table, then writes the new predictions. Use for a full refresh. |
| `APPEND` | Adds the new predictions to the output table as additional rows, keeping the existing ones. Use to accumulate a history of runs. |
| `UPDATEADD` | Updates rows whose `matchingColumns` values match, and inserts the rest. Use to keep one current prediction per entity. **Requires `matchingColumns`.** |

### `scheduleDetails` Fields

| Field | Type | Mandatory | Description |
|-------|------|-----------|--------------|
| `calendarFrequency` | String (enum) | **Yes** | `none`, `hourly`, `daily`, `weekly`, or `monthly`. `none` creates a deployment with no automatic schedule — run it with [Run AutoML Analysis](run-auto-ml-analysis.md). |
| `interval` | Integer | **Yes** for `hourly` | Hours between runs. Only `1`, `2`, `3`, `6`, and `12` are accepted (`8119` otherwise). |
| `hour` | Integer | **Yes** for `daily`, `weekly`, `monthly` | Hour of the day, **0–23** (`8119` otherwise). |
| `minute` | Integer | **Yes** for `daily`, `weekly`, `monthly` | Minute within the hour. Must be a **multiple of 5 in the range 0–55** (`8119` otherwise). |
| `day` | Integer | **Yes** for `weekly`, `monthly` | For `weekly`, the day of the week, `1` = Sunday … `7` = Saturday. For `monthly`, the day of the month, `1`–`31`, or `99` for the last day of the month. **See the caveat below.** |
| `skipFrequency` | Integer | No | Number of periods to skip between runs. Defaults to `0` (every period). |

> **Caveat on weekly and monthly schedules.** The published request template declares `weekDay`, `monthDay`, and `hourInterval`, but the server does not read any of them — it reads `day` for weekly/monthly and `interval` for hourly. Sending `monthDay` for a monthly schedule fails with [`8079`](../../../foundations/error-codes.md#error-8079) *"Attribute 'day' not present in the JSON configuration"*, and `day` itself is not among the template's declared keys. **Only `none`, `daily`, and `hourly` (using `interval`) are confirmed working.** Until this is resolved, create weekly/monthly deployments with `{"calendarFrequency": "none"}` and drive them from your own scheduler through [Run AutoML Analysis](run-auto-ml-analysis.md).

## Notes from the OpenAPI specification

- **matchingColumns** is mandatory only when **importType** is set to **UPDATEADD**. It is ignored for the other import types.
- The **scheduleDetails** attributes that apply depend on the value of **calendarFrequency**.
- Set **calendarFrequency** to **none** to create a deployment that is not run on a recurring schedule, and trigger it using the Run AutoML Analysis API.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Create autoML analysis deployment"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.deployments` | JSONObject | Details of the deployment just created. A single object, not an array. |
| `deployments.deploymentId` | String | ID of the new deployment, as a string. Use as `<deployment-id>` in [Run AutoML Analysis](run-auto-ml-analysis.md) and [Delete AutoML Analysis Model Deployment](delete-auto-ml-analysis-model-deployment.md). |
| `deployments.outputTableId` | String | ID of the output table, as a string — newly created if `outputTable` did not already exist. Read the predictions from it with the [Row / Export APIs](../../data-operations/row-operations/overview.md). |

> Only these two IDs are returned. The full deployment definition can be read back with [Get Deployments For A Model](get-deployments-for-model.md).

# Examples

## Sample Requests

**Case 1 — On-demand deployment (no schedule), full refresh each run**

```http
POST /restapi/v2/automl/workspaces/137687000271334001/analysis/137687000000061115/models/137687000000198124/deployments HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "inputTableId": 137687000000061003,
    "outputTable": "PricePredictionOutput",
    "outputColumns": ["City", "Bedrooms", "Bathrooms", "Garage"],
    "predictionColumn": "PricePrediction",
    "importType": "TRUNCATEADD",
    "serverOption": 1,
    "scheduleDetails": {
        "calendarFrequency": "none"
    }
}
```

**Case 2 — Daily schedule with a timezone, appending each run's predictions**

```http
POST /restapi/v2/automl/workspaces/137687000271334001/analysis/137687000000061115/models/137687000000198124/deployments HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "inputTableId": 137687000000061003,
    "outputTable": "PricePredictionHistory",
    "outputColumns": ["City", "Bedrooms", "Bathrooms", "Garage"],
    "predictionColumn": "PricePrediction",
    "importType": "APPEND",
    "serverOption": 2,
    "timezone": "Asia/Kolkata",
    "scheduleDetails": {
        "calendarFrequency": "daily",
        "hour": 10,
        "minute": 30
    }
}
```

**Case 3 — Hourly schedule with UPDATEADD and matching columns clubbed together**

```http
POST /restapi/v2/automl/workspaces/137687000271334001/analysis/137687000000061115/models/137687000000198124/deployments HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "inputTableId": 137687000000061003,
    "outputTable": "PricePredictionCurrent",
    "outputColumns": ["City", "Bedrooms", "Bathrooms", "Garage"],
    "predictionColumn": "PricePrediction",
    "importType": "UPDATEADD",
    "matchingColumns": ["City", "Bedrooms"],
    "serverOption": 3,
    "timezone": "Asia/Kolkata",
    "scheduleDetails": {
        "calendarFrequency": "hourly",
        "interval": 3
    }
}
```

**Case 4 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
POST /restapi/v2/automl/workspaces/137687000271334009/analysis/137687000000061119/models/137687000000198140/deployments HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "inputTableId": 137687000000061013,
    "outputTable": "PortalPredictions",
    "outputColumns": ["Region"],
    "predictionColumn": "Prediction",
    "importType": "TRUNCATEADD",
    "serverOption": 1,
    "scheduleDetails": {
        "calendarFrequency": "none"
    }
}
```

## Sample Responses

**HTTP 200 OK — Deployment created**

```json
{
    "status": "success",
    "summary": "Create autoML analysis deployment",
    "data": {
        "deployments": {
            "outputTableId": "137687000000198129",
            "deploymentId": "137687000000198176"
        }
    }
}
```

**HTTP 400 Bad Request — The model already has a deployment**

```json
{
    "status": "failure",
    "summary": "MODEL_ALREADY_DEPLOYED",
    "data": {
        "errorCode": 21000051,
        "errorMessage": "A deployment already exists for this model."
    }
}
```

**HTTP 400 Bad Request — `serverOption` outside the allowed set**

```json
{
    "status": "failure",
    "summary": "INVALID_VALUE_FOR_ATTRIBUTE",
    "data": {
        "errorCode": 8119,
        "errorMessage": "Invalid value '5' provided for the attribute 'serverOption'. Only '1, 2 and 3' are allowed."
    }
}
```

**HTTP 400 Bad Request — Unrecognised timezone**

```json
{
    "status": "failure",
    "summary": "INVALID_VALUE",
    "data": {
        "errorCode": 8050,
        "errorMessage": "Invalid input: invalid_timezone."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create AutoML Analysis Deployment](../../../sdk-examples/dsml/automl/create-auto-ml-analysis-deployment.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **The model must be trained first** | Deploying a model that is still training fails with `21000052`; one whose training failed fails with `21000053`. Poll `models[].trainingStatus` via [Get AutoML Analysis Details](get-auto-ml-analysis-details.md) until it reads `"Completed"`. |
| **One deployment per model** | A second deployment on the same model fails with `21000051`. To change a deployment's configuration, delete it with [Delete AutoML Analysis Model Deployment](delete-auto-ml-analysis-model-deployment.md) and create a new one — there is no update API. |
| **The output table is created for you** | If `outputTable` does not exist it is created in the workspace, and its ID comes back as `outputTableId`. If it does exist, `importType` decides whether its rows are replaced, appended to, or merged. |
| **The input table must carry the model's features** | Every feature column the analysis was trained on must exist in `inputTableId`, or the call fails with `21000001`. The input table does **not** need the target column. |
| **`matchingColumns` must be a subset of `outputColumns`** | A matching column that is not also written to the output table fails with `21000042` — the merge key has to be present in the destination. |
| **Creating a deployment does not run it** | Nothing is scored until either the schedule fires or [Run AutoML Analysis](run-auto-ml-analysis.md) is called. With `calendarFrequency: "none"` the deployment only ever runs on demand. |
| **Weekly and monthly schedules are currently unusable** | See the caveat under [`scheduleDetails` Fields](#scheduledetails-fields). |
| **No `criteria`** | The whole input table is scored. To score a subset, point `inputTableId` at a filtered query table or view. |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get AutoML Analysis Details](get-auto-ml-analysis-details.md) → `modelId` (with `trainingStatus: "Completed"`, `isDeployed: false`) + [Get View List](../../views-management/view-operations/get-views.md) → `inputTableId` → Create Deployment → `deploymentId` → [Run AutoML Analysis](run-auto-ml-analysis.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — Portal-domain request, or the caller does not own this workspace. | Call from the standard API host as an owner of the workspace. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The input table belongs to a different workspace. | Use a table from `<workspace-id>`. |
| [8050](../../../foundations/error-codes.md#error-8050) | 400 | `INVALID_VALUE` — `timezone` is not a recognised timezone name. | Use a standard timezone identifier such as `Asia/Kolkata`. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — A required attribute is missing; for weekly/monthly schedules this reports `'day'`. | The message names the attribute. See the schedule caveat above. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE` — `serverOption`, `hour`, `minute`, or `interval` is outside its permitted set. | The message names the attribute and the allowed values. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — CONFIG is absent or a mandatory key is missing at the template level. | Send a complete CONFIG object. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |
| [8544](../../../foundations/error-codes.md#error-8544) | 400 | `OUT_OF_RANGE` — A schedule value is outside its declared range. | Correct the value. |

# Related

- [AutoML overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Science & Machine Learning (AutoML)](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get AutoML Analysis In Org](get-auto-ml-analysis-in-org.md), [Get AutoML Analysis In Workspace](get-auto-ml-analysis-in-workspace.md), [Get AutoML Analysis Details](get-auto-ml-analysis-details.md), [Get Deployments For A Model](get-deployments-for-model.md), [Create AutoML Analysis](create-auto-ml-analysis.md), [Delete AutoML Analysis](delete-auto-ml-analysis.md), [Delete AutoML Analysis Model](delete-auto-ml-analysis-model.md), [Run AutoML Analysis](run-auto-ml-analysis.md), [Delete AutoML Analysis Model Deployment](delete-auto-ml-analysis-model-deployment.md), [AutoML What If Analysis](auto-ml-what-if-analysis.md).
- [SDK examples](../../../sdk-examples/dsml/automl/create-auto-ml-analysis-deployment.md).
