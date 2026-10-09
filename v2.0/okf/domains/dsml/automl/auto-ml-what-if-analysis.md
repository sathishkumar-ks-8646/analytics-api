---
type: API Endpoint
title: AutoML What If Analysis
description: "Generates a single prediction for a hypothetical set of feature values — a live \"what if I changed these inputs?\" query against a trained model."
resource: "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/whatif"
tags:
  - zoho-analytics
  - rest-api-v2
  - dsml
  - automl
  - post
  - modeling
api:
  operation_id: autoMLWhatIfAnalysis
  method: POST
  path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/whatif"
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
    - 8078
    - 8079
    - 8504
    - 8535
  openapi:
    file: "/references/openapi/dsml-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1automl~1workspaces~1{workspace-id}~1analysis~1{analysis-id}~1models~1{model-id}~1whatif/post"
    config_schema: AutoMLWhatIfAnalysisConfig
    response_schema: AutoMLWhatIfAnalysisResponse
  sdk_examples: "/sdk-examples/dsml/automl/auto-ml-what-if-analysis.md"
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

**POST `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/whatif`** - AutoML What If Analysis (AutoML / Data Science & Machine Learning (AutoML)).

Generates a **single prediction for a hypothetical set of feature values** — a live "what if I changed these inputs?" query against a trained model. Nothing is stored and no table is written.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `autoMLWhatIfAnalysis` |
| HTTP method | POST |
| URL | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}/models/{model-id}/whatif` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.modeling.create`](../../../foundations/oauth-scopes.md#zohoanalyticsmodelingcreate) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body - **mandatory** |
| Request Content-Type | `application/x-www-form-urlencoded` |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`dsml-grouped-api.json`](../../../references/openapi/dsml-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1automl~1workspaces~1{workspace-id}~1analysis~1{analysis-id}~1models~1{model-id}~1whatif/post`; CONFIG schema `AutoMLWhatIfAnalysisConfig`; response schema `AutoMLWhatIfAnalysisResponse` |

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
| `features` | JSONObject | **Yes** | — | Feature name → hypothetical value. **Every feature the model was trained on must be present** (`21000050` otherwise); omitting even one is rejected. Keys must be feature column names from the training table; values must match each column's data type. An empty object is rejected with `8078`, and a missing `features` key with `8079`. |

> `features` is a free-form object — the valid keys are exactly the entries of `analysis.features` from [Get AutoML Analysis Details](get-auto-ml-analysis-details.md). Read that list first rather than guessing.

## Notes from the OpenAPI specification

- Each key inside **features** must be the name of a feature column used when the model was trained.
- The prediction is generated in memory and is not written to any table.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"AutoML what if analysis"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.predictions` | String | The value the model predicts for the supplied feature values, **returned as a string** even for a numeric regression target. For a classification model this is the predicted class label. |
| `data.targetColumn` | String | Name of the column being predicted — the analysis's `targetColumn`, echoed for convenience. |

# Examples

## Sample Requests

**Case 1 — Predict a price for a hypothetical property**

```http
POST /restapi/v2/automl/workspaces/137687000271334001/analysis/137687000000061115/models/137687000000198124/whatif HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "features": {
        "City": "Bengaluru",
        "Bedrooms": "3",
        "Bathrooms": "2",
        "Garage": "1"
    }
}
```

**Case 2 — Same model, one input changed, to compare outcomes**

```http
POST /restapi/v2/automl/workspaces/137687000271334001/analysis/137687000000061115/models/137687000000198124/whatif HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "features": {
        "City": "Bengaluru",
        "Bedrooms": "5",
        "Bathrooms": "4",
        "Garage": "2"
    }
}
```

**Case 3 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
POST /restapi/v2/automl/workspaces/137687000271334009/analysis/137687000000061119/models/137687000000198140/whatif HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
Content-Type: application/x-www-form-urlencoded

CONFIG={
    "features": {
        "Region": "East"
    }
}
```

## Sample Responses

**HTTP 200 OK — Prediction generated (Case 1)**

```json
{
    "status": "success",
    "summary": "AutoML what if analysis",
    "data": {
        "predictions": "7250000",
        "targetColumn": "Price"
    }
}
```

**HTTP 400 Bad Request — A feature used in training is missing from the input**

```json
{
    "status": "failure",
    "summary": "FEATURE_MISSING_IN_WHATIF",
    "data": {
        "errorCode": 21000050,
        "errorMessage": "One or more features used in training the model is missing in the input.Please ensure that all features used in training are included."
    }
}
```

**HTTP 400 Bad Request — The model is still training**

```json
{
    "status": "failure",
    "summary": "MODEL_TRAINING_INPROGRESS",
    "data": {
        "errorCode": 21000043,
        "errorMessage": "Training in progress for the model.Please try again once training is completed."
    }
}
```

**HTTP 400 Bad Request — `features` sent as an empty object**

```json
{
    "status": "failure",
    "summary": "EMPTY_JSON_ATTRIBUTE_FOUND",
    "data": {
        "errorCode": 8078,
        "errorMessage": "The attribute 'features' has an empty value. Kindly provide a valid JSON configuration."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for AutoML What If Analysis](../../../sdk-examples/dsml/automl/auto-ml-what-if-analysis.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **Read-only despite being a POST** | Nothing is persisted: no table is written, no deployment is needed, and the model is unchanged. It uses POST only because the feature values travel in a body. |
| **No deployment required** | This is the one way to get a prediction out of a model without creating a deployment — useful for interactive exploration and for validating a model before committing to deploy it. |
| **All training features are mandatory** | Partial input is rejected with `21000050`; the model cannot infer missing values. Read `analysis.features` from [Get AutoML Analysis Details](get-auto-ml-analysis-details.md) and supply every one. |
| **Extra keys are tolerated** | Feature names that were not part of training are ignored rather than rejected, so a superset of the training features is accepted. |
| **The model must be trained** | Calling it while `trainingStatus` is `"In Progress"` fails with `21000043`. |
| **Not every algorithm supports What-If** | Algorithms without What-If capability fail with `21000054`, naming the algorithm. Clustering models in particular are not universally supported. |
| **Values are sent and returned as strings** | Send numeric features as JSON strings, and expect `predictions` back as a string; convert on your side. |
| **Wrongly typed values surface as `21000006`** | A value that cannot be coerced to the column's data type fails as a deployment/scoring failure rather than a specific type error. |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | [Get AutoML Analysis Details](get-auto-ml-analysis-details.md) → `models[].id` (with `trainingStatus: "Completed"`) + `analysis.features` → What If Analysis. |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — Portal-domain request, or the caller does not own this workspace. | Call from the standard API host as an owner of the workspace. |
| [8078](../../../foundations/error-codes.md#error-8078) | 400 | `EMPTY_JSON_ATTRIBUTE_FOUND` — `features` was sent as an empty object. | Supply every training feature and its value. |
| [8079](../../../foundations/error-codes.md#error-8079) | 400 | `ATTRIBUTE_NOT_PRESENT_IN_JSON_CONFIGURATION` — `features` is missing from CONFIG. | Include the `features` object. |
| [8504](../../../foundations/error-codes.md#error-8504) | 400 | `LESS_THAN_MIN_OCCURANCE` — CONFIG is absent. | Send a CONFIG object containing `features`. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.modeling.create`. |

# Related

- [AutoML overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Science & Machine Learning (AutoML)](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get AutoML Analysis In Org](get-auto-ml-analysis-in-org.md), [Get AutoML Analysis In Workspace](get-auto-ml-analysis-in-workspace.md), [Get AutoML Analysis Details](get-auto-ml-analysis-details.md), [Get Deployments For A Model](get-deployments-for-model.md), [Create AutoML Analysis](create-auto-ml-analysis.md), [Delete AutoML Analysis](delete-auto-ml-analysis.md), [Delete AutoML Analysis Model](delete-auto-ml-analysis-model.md), [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md), [Run AutoML Analysis](run-auto-ml-analysis.md), [Delete AutoML Analysis Model Deployment](delete-auto-ml-analysis-model-deployment.md).
- [SDK examples](../../../sdk-examples/dsml/automl/auto-ml-what-if-analysis.md).
