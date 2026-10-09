---
type: API Endpoint
title: Create AutoML Analysis
description: Creates an analysis and immediately starts training one model per configured algorithm.
resource: "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/{workspace-id}/analysis"
tags:
  - zoho-analytics
  - rest-api-v2
  - dsml
  - automl
  - post
  - modeling
api:
  operation_id: createAutoMLAnalysis
  method: POST
  path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis"
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
    - 7005
    - 7103
    - 7301
    - 7319
    - 8078
    - 8079
    - 8119
    - 8504
    - 8535
    - 8547
  openapi:
    file: "/references/openapi/dsml-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1automl~1workspaces~1{workspace-id}~1analysis/post"
    config_schema: CreateAutoMLAnalysisConfig
    response_schema: CreateAutoMLAnalysisResponse
  sdk_examples: "/sdk-examples/dsml/automl/create-auto-ml-analysis.md"
sources:
  - id: openapi-spec
    resource: "/references/openapi/dsml-grouped-api.json"
    title: OpenAPI 3 specification - dsml-grouped-api.json
    author: team:zoho-analytics-api-docs
    last_modified: 2026-10-09T14:14:03Z
generated:
  by: process:build_okf
  at: 2026-10-09T14:14:46Z
status: stable
---

# Summary

**POST `/restapi/v2/automl/workspaces/{workspace-id}/analysis`** - Create AutoML Analysis (AutoML / Data Science & Machine Learning (AutoML)).

Creates an analysis and **immediately starts training one model per configured algorithm**. Returns as soon as the training job is queued — it does not wait for training to finish.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `createAutoMLAnalysis` |
| HTTP method | POST |
| URL | `/restapi/v2/automl/workspaces/{workspace-id}/analysis` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`dsml-grouped-api.json`](../../../references/openapi/dsml-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1automl~1workspaces~1{workspace-id}~1analysis/post`; CONFIG schema `CreateAutoMLAnalysisConfig`; response schema `CreateAutoMLAnalysisResponse` |

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

## CONFIG Parameters

CONFIG is **mandatory** for this API.

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `name` | String | **Yes** | — | Name of the analysis. Must be **unique within the workspace** (`21000003` otherwise) and **at most 50 characters** (`21000020` otherwise). An empty string is rejected with `21000023`. |
| `trainingTableId` | Long | **Yes** | — | ID of the table the model is trained on. Must belong to `<workspace-id>` (`7319` otherwise). |
| `predictionType` | String (enum) | **Yes** | — | `REGRESSION`, `CLASSIFICATION`, or `CLUSTERING`. Case-insensitive on input. Determines which algorithm keys are valid in `algorithms`. See [`predictionType` Values](#predictiontype-values). |
| `targetColumn` | String | Conditional | — | Name of the column to predict. **Mandatory for `REGRESSION` and `CLASSIFICATION`; not used by `CLUSTERING`**, which is unsupervised. Must exist in the training table (`21000030` otherwise) and must **not** also appear in `features` (`21000048` otherwise). |
| `features` | JSONArray of String | **Yes** | — | Input feature column names from the training table. **Minimum 3, maximum 20** (`21000026` / `21000027`). Duplicates are rejected (`21000047`). Every name must exist in the training table (`21000028`). The one exception is the `maxEntropy` algorithm, which requires **exactly one** feature (`21000024`). |
| `serverOption` | Integer (enum) | **Yes** | — | Server memory for the training job: `1` = 8 GB, `2` = 16 GB, `3` = 32 GB. Any other value fails with `8119`. |
| `algorithms` | JSONObject | **Yes** | — | Algorithm keys mapped to their hyperparameters. **One model is trained per key.** Up to 15 algorithms. See [`algorithms` Values](#algorithms-values). |
| `description` | String | No | — | Free-text description. Maximum 1,000 characters (`21000021` otherwise). |

### `predictionType` Values

| Value | Meaning | `targetColumn` | Valid algorithm keys |
|-------|---------|----------------|----------------------|
| `REGRESSION` | Predicts a continuous numeric value (e.g. a price). | **Required** | `decisionTreeRegression`, `randomForestRegression`, `olsRegression`, `lassoRegression`, `ridgeRegression`, `svmRegressor`, `gradientBoostingRegression` |
| `CLASSIFICATION` | Predicts a discrete class label (e.g. churn yes/no). | **Required** | `gradientBoostingClassification`, `adaptiveBoost`, `decisionTreeClassification`, `randomForestClassification`, `logisticRegression`, `linearDiscriminantAnalysis`, `maxEntropy` |
| `CLUSTERING` | Groups similar records without a labelled outcome. | **Not used** | `kMeansPP`, `kModes`, `kPrototypes`, `xMeans`, `gMeans` |

> Using an algorithm key that does not belong to the chosen `predictionType` fails with `21000016` `INVALID_ALGORITHM`, naming the offending key.

### `algorithms` Values

`algorithms` is a JSONObject whose **keys are algorithm names** and whose values are that algorithm's hyperparameter object. Sending three keys trains three models under the same analysis. Every hyperparameter is optional — omitting the object entirely (`{}`) trains the algorithm with its defaults.

| Algorithm key | Prediction type | Hyperparameters |
|---------------|-----------------|-----------------|
| `decisionTreeRegression` | Regression | `minimumSampleSplit` (Integer), `maximumDepth` (Integer) |
| `randomForestRegression` | Regression | `minimumSampleSplit` (Integer), `maximumDepth` (Integer), `numberOfTrees` (Integer) |
| `olsRegression` | Regression | `intercept` (Boolean), `allowAlternateModel` (Boolean) |
| `lassoRegression` | Regression | `tolerance` (Decimal), `shrinkage` (Integer), `maximumIterations` (Integer) |
| `ridgeRegression` | Regression | `shrinkage` (Integer) |
| `svmRegressor` | Regression | `epsilon` (Decimal), `softMargin` (Decimal), `tolerance` (Decimal), `epochs` (Integer) |
| `gradientBoostingRegression` | Regression | `lossFunction` (`LEASTSQUARES` \| `QUANTILE` \| `LEASTABSOLUTEDEVIATION` \| `HUBER`), `maximumDepth`, `maximumNodes`, `nodeSize`, `numberOfTrees` (Integer), `shrinkage`, `subSample` (Decimal) |
| `gradientBoostingClassification` | Classification | Same set as `gradientBoostingRegression` |
| `adaptiveBoost` | Classification | `maximumDepth`, `maximumNodes`, `nodeSize`, `numberOfTrees` (Integer) |
| `decisionTreeClassification` | Classification | `minimumSampleSplit` (Integer), `maximumDepth` (Integer) |
| `randomForestClassification` | Classification | `minimumSampleSplit` (Integer), `maximumDepth` (Integer), `numberOfTrees` (Integer) |
| `logisticRegression` | Classification | `lambda` (Decimal), `maximumIterations` (Integer), `tolerance` (Decimal) |
| `linearDiscriminantAnalysis` | Classification | `tolerance` (Decimal) |
| `maxEntropy` | Classification | `lambda` (Decimal), `maximumIterations` (Integer), `tolerance` (Decimal) |
| `kMeansPP` | Clustering | `clustersCount` (Integer), `kMax` (Integer), `chIndexBasedOptimalK` (Boolean), `calculatePerformanceMetrics` (Boolean) |
| `kModes` | Clustering | `clustersCount`, `minimumClusterCount`, `maximumClusterCount` (Integer), `dissimilarityMeasure` (`BINARY` \| `GLOBAL_FREQUENCY` \| `RELATIVE_FREQUENCY` \| `JARO_WINKLER` \| `LEVENSHTEIN` \| `JACCARD`) |
| `kPrototypes` | Clustering | `clustersCount` (Integer), `kMax` (Integer), `chIndexBasedOptimalK` (Boolean), `gamma` (Decimal) |
| `xMeans` | Clustering | `kMax` (Integer), `maximumIterations` (Integer), `tolerance` (Decimal) |
| `gMeans` | Clustering | `kMax` (Integer), `maximumIterations` (Integer), `tolerance` (Decimal) |

> **`maxEntropy` is exclusive.** If `maxEntropy` is present it must be the **only** key in `algorithms` (`21000025` otherwise), and `features` must contain **exactly one** column (`21000024` otherwise). Every other algorithm requires at least 3 features.
>
> Unknown hyperparameter names fail with `21000018`; out-of-range or wrongly typed values fail with `21000031`–`21000035`.

## Notes from the OpenAPI specification

- The algorithm keys sent inside **algorithms** must belong to the group that matches the selected **predictionType**.
- More than one algorithm can be configured in a single request. A model is built for each algorithm that is configured.
- **targetColumn** applies to the **REGRESSION** and **CLASSIFICATION** prediction types only.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Create autoML analysis"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.id` | String | ID of the newly created analysis, as a string. Note the key is **`id`**, not `analysisId`. Use it as `<analysis-id>` everywhere else. |

> **No model IDs are returned.** Models are created asynchronously as training starts — fetch them from [Get AutoML Analysis Details](get-auto-ml-analysis-details.md).

# Examples

## Sample Requests

**Case 1 — Regression with a single algorithm, minimal configuration**

```http
POST /restapi/v2/automl/workspaces/137687000271334001/analysis HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "name": "PricePredictionAnalysis",
    "trainingTableId": 137687000000061002,
    "predictionType": "REGRESSION",
    "targetColumn": "Price",
    "features": ["City", "Bedrooms", "Bathrooms"],
    "serverOption": 1,
    "algorithms": {
        "randomForestRegression": {}
    }
}
```

**Case 2 — Regression with description, larger server, and two algorithms with tuned hyperparameters (two models are trained)**

```http
POST /restapi/v2/automl/workspaces/137687000271334001/analysis HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "name": "PricePredictionTuned",
    "description": "Predicts property price from listing attributes",
    "trainingTableId": 137687000000061002,
    "predictionType": "REGRESSION",
    "targetColumn": "Price",
    "features": ["City", "Bedrooms", "Bathrooms", "Garage"],
    "serverOption": 2,
    "algorithms": {
        "randomForestRegression": {
            "minimumSampleSplit": 2,
            "maximumDepth": 20,
            "numberOfTrees": 25
        },
        "ridgeRegression": {
            "shrinkage": 1
        }
    }
}
```

**Case 3 — Classification with a boosted algorithm**

```http
POST /restapi/v2/automl/workspaces/137687000271334001/analysis HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "name": "ChurnPredictionAnalysis",
    "trainingTableId": 137687000000061004,
    "predictionType": "CLASSIFICATION",
    "targetColumn": "Churned",
    "features": ["Region", "Tenure", "MonthlyCharges"],
    "serverOption": 2,
    "algorithms": {
        "gradientBoostingClassification": {
            "lossFunction": "HUBER",
            "numberOfTrees": 50,
            "maximumDepth": 6,
            "shrinkage": 0.1
        }
    }
}
```

**Case 4 — Clustering, with no `targetColumn`**

```http
POST /restapi/v2/automl/workspaces/137687000271334001/analysis HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "name": "SegmentationAnalysis",
    "trainingTableId": 137687000000061002,
    "predictionType": "CLUSTERING",
    "features": ["City", "Bedrooms", "Bathrooms"],
    "serverOption": 1,
    "algorithms": {
        "kMeansPP": {
            "clustersCount": 5,
            "chIndexBasedOptimalK": false,
            "calculatePerformanceMetrics": true
        }
    }
}
```

## Sample Responses

**HTTP 200 OK — Analysis created and training queued**

```json
{
    "status": "success",
    "summary": "Create autoML analysis",
    "data": {
        "id": "137687000000061115"
    }
}
```

**HTTP 400 Bad Request — Duplicate analysis name**

```json
{
    "status": "failure",
    "summary": "ANALYSISNAME_DUPLICATED",
    "data": {
        "errorCode": 21000003,
        "errorMessage": "A similar analysis named PricePredictionAnalysis already exists in this workspace. Please choose a different name."
    }
}
```

**HTTP 400 Bad Request — Algorithm not valid for the chosen prediction type**

```json
{
    "status": "failure",
    "summary": "INVALID_ALGORITHM",
    "data": {
        "errorCode": 21000016,
        "errorMessage": "supportVectorRegression is not a valid algorithm. Please choose a supported algorithm."
    }
}
```

**HTTP 400 Bad Request — AutoML not enabled for the organization**

```json
{
    "status": "failure",
    "summary": "AUTOML_NOT_ENABLED",
    "data": {
        "errorCode": 21000014,
        "errorMessage": "The AutoML Feature is not enabled. Please enable the features from Org Settings > Feature Controls > DSML."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Create AutoML Analysis](../../../sdk-examples/dsml/automl/create-auto-ml-analysis.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Asynchronous — 200 means "queued", not "trained"** | The call returns as soon as the analysis row and its training job exist. Poll `models[].trainingStatus` via [Get AutoML Analysis Details](get-auto-ml-analysis-details.md) until it reads `"Completed"`. |
| **One algorithm key = one model** | The `algorithms` object is a fan-out: three keys produce three independently trained, independently scored, independently deployable models. This is how you compare algorithms in a single request. |
| **Analyses are immutable** | There is no update API. Changing the training table, target column, feature list, algorithms, or server option means deleting the analysis and creating a new one. |
| **`name` max length is 50, not 60** | The published request template allows 60 characters, but the server rejects anything over 50 with `21000020`. Budget for 50. |
| **Feature count is 3–20** | Below 3 fails with `21000026`; above 20 fails with `21000027`. This is stricter than the 1–100 range in the published schema. The sole exception is `maxEntropy`, which requires exactly 1. |
| **`targetColumn` must not be a feature** | Including the predicted column among the inputs fails with `21000048` — a common mistake that would leak the answer into the model. |
| **`CLUSTERING` takes no `targetColumn`** | It is unsupervised; the attribute is ignored rather than required. |
| **Training table must be in the workspace** | A table from another workspace fails with `7319`, and a non-existent ID surfaces as `7005`. |
| **No `criteria`** | The training set is the whole table. To train on a subset, build a filtered query table or view first and use that as `trainingTableId`. |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get View List](../../views-management/view-operations/get-views.md) → `trainingTableId` → Create AutoML Analysis → `data.id` → [Get AutoML Analysis Details](get-auto-ml-analysis-details.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | `COMMON_INTERNAL_SERVER_ERROR` — Surfaces when `trainingTableId` does not identify a real table. | Verify the ID via [Get View List](../../views-management/view-operations/get-views.md). |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — Portal-domain request, or the caller does not own this workspace. | Call from the standard API host as an owner of the workspace. |
| [7319](../../../foundations/error-codes.md#error-7319) | 400 | `OBJID_NOT_BELONGS_TO_DB` — The training table belongs to a different workspace. | Use a table from `<workspace-id>`. |
| [8078](../../../foundations/error-codes.md#error-8078) | 400 | `EMPTY_JSON_ATTRIBUTE_FOUND` — A mandatory attribute was sent empty. | Supply a value. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — A mandatory attribute is missing. | The message names the attribute. |
| [8119](../../../foundations/error-codes.md#error-8119) | 400 | `INVALID_VALUE_FOR_ATTRIBUTE` — `serverOption` or `predictionType` is outside its allowed set. | The message names the attribute and permitted values. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — CONFIG is absent, or a required key is missing at the template level. | Send a complete CONFIG object. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |
| [8547](../../../foundations/error-codes.md#error-8547) | 400 | `ARRAY_SIZE_OUT_OF_RANGE` — `features` is empty or exceeds the allowed array size. | Send between 3 and 20 feature names. |

# Related

- [AutoML overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Science & Machine Learning (AutoML)](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get AutoML Analysis In Org](get-auto-ml-analysis-in-org.md), [Get AutoML Analysis In Workspace](get-auto-ml-analysis-in-workspace.md), [Get AutoML Analysis Details](get-auto-ml-analysis-details.md), [Get Deployments For A Model](get-deployments-for-model.md), [Delete AutoML Analysis](delete-auto-ml-analysis.md), [Delete AutoML Analysis Model](delete-auto-ml-analysis-model.md), [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md), [Run AutoML Analysis](run-auto-ml-analysis.md), [Delete AutoML Analysis Model Deployment](delete-auto-ml-analysis-model-deployment.md), [AutoML What If Analysis](auto-ml-what-if-analysis.md).
- [SDK examples](../../../sdk-examples/dsml/automl/create-auto-ml-analysis.md).
