---
type: API Endpoint
title: Get AutoML Analysis Details
description: "Retrieves the detailed information of a specific AutoML analysis, including the training table, the target column, the input features and every model trained under the analysis with its score and hyperparameters."
resource: "https://analyticsapi.zoho.com/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}"
tags:
  - zoho-analytics
  - rest-api-v2
  - dsml
  - automl
  - get
  - metadata
api:
  operation_id: getAutoMLAnalysisDetails
  method: GET
  path: "/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}"
  domain: dsml
  group: automl
  oauth_scopes:
    - ZohoAnalytics.metadata.read
  org_id_header: required
  config_parameter:
    location: none
    required: false
  success_status: 200
  response_content_types:
    - application/json
  permission_required: "The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace."
  error_codes:
    - 7103
    - 7301
    - 8535
  openapi:
    file: "/references/openapi/dsml-grouped-api.json"
    pointer: "#/paths/~1restapi~1v2~1automl~1workspaces~1{workspace-id}~1analysis~1{analysis-id}/get"
    config_schema: null
    response_schema: GetAutoMLAnalysisDetailsResponse
  sdk_examples: "/sdk-examples/dsml/automl/get-auto-ml-analysis-details.md"
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

**GET `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}`** - Get AutoML Analysis Details (AutoML / Data Science & Machine Learning (AutoML)).

Returns the full definition of one analysis **together with every model trained under it** — including each model's ID, score, training status, and hyperparameters. This is the pivotal read in the family: it is the only source of `modelId`.

> This API has no CONFIG parameter.

From the OpenAPI specification:

Retrieves the detailed information of a specific AutoML analysis, including the training table, the target column, the input features and every model trained under the analysis with its score and hyperparameters.

# Endpoint

| Attribute | Value |
|---|---|
| Operation ID | `getAutoMLAnalysisDetails` |
| HTTP method | GET |
| URL | `/restapi/v2/automl/workspaces/{workspace-id}/analysis/{analysis-id}` |
| Base URL | `https://analyticsapi.zoho.com` (data-center specific, see [Data centers](../../../foundations/data-centers.md)) |
| OAuth scope | [`ZohoAnalytics.metadata.read`](../../../foundations/oauth-scopes.md#zohoanalyticsmetadataread) |
| ZANALYTICS-ORGID header | **Required** - Organisation ID of the workspace. |
| Permission required | The authenticated user must be an Account Admin or Organization Admin, or the Workspace Admin (owner) of the specified workspace. See [Roles & permissions](../../../foundations/roles-and-permissions.md). |
| CONFIG parameter | No CONFIG parameter |
| Success response | HTTP 200 - `application/json` |
| OpenAPI | [`dsml-grouped-api.json`](../../../references/openapi/dsml-grouped-api.json) - pointer `#/paths/~1restapi~1v2~1automl~1workspaces~1{workspace-id}~1analysis~1{analysis-id}/get`; response schema `GetAutoMLAnalysisDetailsResponse` |

# Request

## Headers

| Header | Value | Required | Notes |
|---|---|---|---|
| `Authorization` | `Zoho-oauthtoken <access-token>` | Required | OAuth 2.0 access token carrying `ZohoAnalytics.metadata.read`. See [Authentication](../../../foundations/authentication.md). |
| `ZANALYTICS-ORGID` | `<org-id>` | Required | Organization ID. Obtain it from [Get Org List](../../organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](../../../foundations/identifiers.md). |

## Path Parameters

| Parameter | Type | Description | Source |
|---|---|---|---|
| `{workspace-id}` | string | ID of the workspace. | [How to obtain](../../../foundations/identifiers.md#workspace-id) |
| `{analysis-id}` | string | ID of the AutoML analysis. | [How to obtain](../../../foundations/identifiers.md#analysis-id) |

## CONFIG Parameters

This endpoint takes no CONFIG parameter.

# Response

## Success Response

HTTP `200` with content type `application/json`. JSON responses use the standard envelope `{ "status": "success", "summary": ..., "data": {...} }` described in [Response envelope](../../../foundations/response-envelope.md).

## Response Fields

| Field | Type | Description |
|-------|------|--------------|
| `status` | String | `"success"` on a successful call, `"failure"` on error. |
| `summary` | String | Localised operation summary. `"Get autoML analysis details"` for this API. |
| `data` | JSONObject | Response payload wrapper. |
| `data.analysis` | JSONObject | The analysis definition. Always present on success. |
| `analysis.id` | String | ID of the analysis, as a string. |
| `analysis.name` | String | Name of the analysis. |
| `analysis.description` | String | Free-text description supplied at creation. |
| `analysis.predictionType` | String | `"Regression"`, `"Classification"`, or `"Clustering"` — title case. |
| `analysis.trainingTable` | String | Name of the training table. |
| `analysis.trainingTableId` | String | ID of the training table, as a string. |
| `analysis.targetColumn` | String | The column being predicted. Not meaningful for `Clustering` analyses, which are unsupervised. |
| `analysis.features` | JSONArray of String | Names of the input feature columns, in the order supplied at creation. |
| `analysis.stack` | String | Server memory the analysis runs on, in human-readable form (`"8 GB"`, `"16 GB"`, `"32 GB"`). Corresponds to the numeric `serverOption` that was sent at creation. |
| `analysis.status` | String | Status of the **analysis**, e.g. `"In progress"`, `"Completed"`. **Distinct from the top-level `status` field**, which reports the outcome of the API call itself. |
| `analysis.models` | JSONArray | One entry per algorithm configured at creation. **The only place `modelId` is exposed.** |
| `models[].id` | String | ID of the model, as a string. This is the `<model-id>` for [Get Deployments For A Model](get-deployments-for-model.md), [Delete AutoML Analysis Model](delete-auto-ml-analysis-model.md), [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md), [AutoML What If Analysis](auto-ml-what-if-analysis.md). |
| `models[].name` | String | Display name of the algorithm, e.g. `"Random Forest Regression"`. This is a label, not the `algorithms` key used on the request — that key appears inside `algorithm`. |
| `models[].scoreParamName` | String | Name of the scoring metric, e.g. `"Classification Accuracy"`. The metric depends on the prediction type. Present once the model has been scored. |
| `models[].score` | String | The metric value, **returned as a string** even though it is numeric. Not meaningful until `trainingStatus` is `"Completed"`. |
| `models[].trainingStatus` | String | Training state of this individual model, e.g. `"In Progress"`, `"Completed"`, `"Failed"`. **Poll this field** — a model can only be deployed or used for What-If once it reads `"Completed"`. |
| `models[].lastTrainingTime` | String | When the model was last trained, in `dd MMM yyyy HH:mm:ss` format. |
| `models[].algorithm` | JSONObject | Single-key object: the algorithm key (e.g. `randomForestRegression`) mapped to its hyperparameters. |
| `models[].algorithm.<algorithm>.<parameter>` | String | Each hyperparameter's configured value, **returned as a string** even for parameters documented as Integer or Decimal on the request side. |
| `models[].isDeployed` | Boolean | `true` when a deployment already exists for this model. Because a model may hold only one deployment, `true` means [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) will fail with `21000051`. |

## Notes from the OpenAPI specification

- One model is returned for each algorithm that was configured when the analysis was created.
- The hyperparameter values inside **algorithm** are returned as strings.
- **stack** is the human-readable form of the **serverOption** that was sent when the analysis was created.

# Examples

## Sample Requests

**Case 1 — Standard workspace**

```http
GET /restapi/v2/automl/workspaces/137687000271334001/analysis/137687000000061115 HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
```

**Case 2 — White Label / Client Portal: request sent through the portal domain (rejected)**

```http
GET /restapi/v2/automl/workspaces/137687000271334009/analysis/137687000000061119 HTTP/1.1
Host: portal.customdomain.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000654321
```

## Sample Responses

**HTTP 200 OK — Regression analysis whose two models are still training**

```json
{
    "status": "success",
    "summary": "Get autoML analysis details",
    "data": {
        "analysis": {
            "id": "137687000000061115",
            "name": "PricePredictionAnalysis",
            "description": "Predicts property price from listing attributes",
            "predictionType": "Regression",
            "trainingTable": "RealEstate_TrainData",
            "trainingTableId": "137687000000061002",
            "targetColumn": "Price",
            "features": [
                "City",
                "Bedrooms",
                "Bathrooms",
                "Garage"
            ],
            "stack": "8 GB",
            "status": "In progress",
            "models": [
                {
                    "id": "137687000000198124",
                    "name": "Random Forest Regression",
                    "score": "0",
                    "trainingStatus": "In Progress",
                    "lastTrainingTime": "28 Jan 2026 20:31:24",
                    "algorithm": {
                        "randomForestRegression": {
                            "minimumSampleSplit": "2",
                            "maximumDepth": "100",
                            "numberOfTrees": "25"
                        }
                    },
                    "isDeployed": false
                },
                {
                    "id": "137687000000198125",
                    "name": "Decision Tree Regression",
                    "score": "0",
                    "trainingStatus": "In Progress",
                    "lastTrainingTime": "28 Jan 2026 20:31:24",
                    "algorithm": {
                        "decisionTreeRegression": {
                            "minimumSampleSplit": "2",
                            "maximumDepth": "100"
                        }
                    },
                    "isDeployed": false
                }
            ]
        }
    }
}
```

**HTTP 200 OK — Classification analysis, training complete and one model already deployed**

```json
{
    "status": "success",
    "summary": "Get autoML analysis details",
    "data": {
        "analysis": {
            "id": "137687000000061116",
            "name": "ChurnPredictionAnalysis",
            "description": "Predicts customer churn",
            "predictionType": "Classification",
            "trainingTable": "Churn_TrainData",
            "trainingTableId": "137687000000061004",
            "targetColumn": "Churned",
            "features": [
                "Region",
                "Tenure",
                "MonthlyCharges"
            ],
            "stack": "16 GB",
            "status": "Completed",
            "models": [
                {
                    "id": "137687000000198130",
                    "name": "Random Forest Classification",
                    "scoreParamName": "Classification Accuracy",
                    "score": "38.95",
                    "trainingStatus": "Completed",
                    "lastTrainingTime": "28 Jan 2026 20:31:24",
                    "algorithm": {
                        "randomForestClassification": {
                            "minimumSampleSplit": "2",
                            "maximumDepth": "6",
                            "numberOfTrees": "25"
                        }
                    },
                    "isDeployed": true
                }
            ]
        }
    }
}
```

**HTTP 400 Bad Request — The analysis belongs to a different workspace**

```json
{
    "status": "failure",
    "summary": "ANALYSIS_NOT_BELONGS_TO_DB",
    "data": {
        "errorCode": 21000009,
        "errorMessage": "The given analysis does not belong to this workspace."
    }
}
```

## SDK Examples

Code samples in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby, Deluge (Zoho scripting) are in [SDK examples for Get AutoML Analysis Details](../../../sdk-examples/dsml/automl/get-auto-ml-analysis-details.md). Client construction is described in [SDK clients](../../../foundations/sdk-clients.md).

# Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **The only source of `modelId`** | Neither list API returns models. Any deploy, model-delete, or What-If workflow must call this API first. |
| **This is the polling endpoint** | Training is asynchronous: [Create AutoML Analysis](create-auto-ml-analysis.md) returns as soon as the job is queued. Poll `models[].trainingStatus` until it reads `"Completed"` before attempting a deployment or a What-If. |
| **Two different `status` fields** | `data.analysis.status` is the training state of the analysis; the top-level `status` is `"success"`/`"failure"` for the HTTP call. Do not confuse them. |
| **Per-model status, not just per-analysis** | Models train independently, so one model may be `"Completed"` while another under the same analysis is still `"In Progress"` or has `"Failed"`. Always check the individual `models[].trainingStatus`. |
| **All numbers come back as strings** | `score` and every hyperparameter value are strings in the response, even though `algorithms` accepts them as numbers on the request. Round-tripping requires converting types. |
| **`isDeployed` is the deployability flag** | Check it before calling [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md) rather than catching `21000051`. |
| **Case asymmetry on `predictionType`** | Returned title case (`"Regression"`), accepted upper case (`REGRESSION`). |
| **Not callable from a portal domain** | See [White Label / Client Portal Behaviour](overview.md#white-label--client-portal-behaviour). |
| **Dependency chain** | [Create AutoML Analysis](create-auto-ml-analysis.md), [Get AutoML Analysis In Org](get-auto-ml-analysis-in-org.md), or [Get AutoML Analysis In Workspace](get-auto-ml-analysis-in-workspace.md) → `analysisId` → Get AutoML Analysis Details → `models[].id` → [Get Deployments For A Model](get-deployments-for-model.md), [Delete AutoML Analysis Model](delete-auto-ml-analysis-model.md), [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md), [AutoML What If Analysis](auto-ml-what-if-analysis.md). |

# Error Codes

Every failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](../../../foundations/error-codes.md).

| Code | HTTP | Reason | Solution |
|---|---|---|---|
| [7005](../../../foundations/error-codes.md#error-7005) | 500 | Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload. | Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request. |
| [7103](../../../foundations/error-codes.md#error-7103) | 404 | `META_OBJECT_NOT_PRESENT` — Workspace not found. | Verify `<workspace-id>` and the `ZANALYTICS-ORGID` header. |
| [7301](../../../foundations/error-codes.md#error-7301) | 403 | `SECURITY_NOT_PERMITTED` — Portal-domain request, or the caller does not own this workspace. | Call from the standard API host as an owner of the workspace. |
| [8535](../../../foundations/error-codes.md#error-8535) | 401 | `INVALID_OAUTHTOKEN` — Invalid or expired OAuth token. | Provide a valid token with scope `ZohoAnalytics.metadata.read`. |

# Related

- [AutoML overview](overview.md) - concepts, limits and behaviours shared by this API group.
- [Data Science & Machine Learning (AutoML)](../overview.md) - the parent API domain.
- [Request conventions](../../../foundations/request-conventions.md), [Response envelope](../../../foundations/response-envelope.md), [Error code catalog](../../../foundations/error-codes.md).
- [OAuth scopes](../../../foundations/oauth-scopes.md), [Roles & permissions](../../../foundations/roles-and-permissions.md), [Permission matrix](../../../foundations/permission-matrix.md).
- Other endpoints in this group: [Get AutoML Analysis In Org](get-auto-ml-analysis-in-org.md), [Get AutoML Analysis In Workspace](get-auto-ml-analysis-in-workspace.md), [Get Deployments For A Model](get-deployments-for-model.md), [Create AutoML Analysis](create-auto-ml-analysis.md), [Delete AutoML Analysis](delete-auto-ml-analysis.md), [Delete AutoML Analysis Model](delete-auto-ml-analysis-model.md), [Create AutoML Analysis Deployment](create-auto-ml-analysis-deployment.md), [Run AutoML Analysis](run-auto-ml-analysis.md), [Delete AutoML Analysis Model Deployment](delete-auto-ml-analysis-model-deployment.md), [AutoML What If Analysis](auto-ml-what-if-analysis.md).
- [SDK examples](../../../sdk-examples/dsml/automl/get-auto-ml-analysis-details.md).
